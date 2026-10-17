
"""
vpn_client_gui.py
A full Tkinter GUI for the VPN Client (UDP <-> TCP bridge with DH + symmetric crypto).
"""
import base64
import hashlib
import hmac
import json
import queue
import secrets
import socket
import struct
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

P_HEX = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A63A36210000000000090563", 16
)
G = 2

def dh_generate_keypair():
    a = secrets.randbelow(P_HEX - 2) + 2
    A = pow(G, a, P_HEX)
    return a, A

def dh_shared_secret(their_pub: int, my_priv: int) -> bytes:
    s = pow(their_pub, my_priv, P_HEX)
    return hashlib.sha256(str(s).encode()).digest()

def caesar_bytes(data: bytes, shift: int) -> bytes:
    return bytes((b + shift) % 256 for b in data)

def xor_keystream(data: bytes, key: bytes, counter: int) -> bytes:
    out = bytearray()
    i = 0
    while len(out) < len(data):
        ctr = struct.pack(">Q", counter + i)
        out.extend(hashlib.sha256(key + ctr).digest())
        i += 1
    return bytes(a ^ b for a, b in zip(data, out[:len(data)]))

class CryptoSuite:
    def __init__(self, key: bytes, cipher: str = "caesar", integrity: str = "none"):
        self.key = key
        self.cipher = cipher
        self.integrity = integrity
        self.shift = key[0]
        self.tx_counter = 0
        self.rx_counter = 0

    def protect(self, plaintext: bytes) -> bytes:
        if self.cipher == "caesar":
            c = caesar_bytes(plaintext, self.shift)
        elif self.cipher == "xor":
            c = xor_keystream(plaintext, self.key, self.tx_counter)
            self.tx_counter += 1
        else:
            raise ValueError("Unknown cipher")
        if self.integrity == "sha256":
            tag = hmac.new(self.key, c, hashlib.sha256).digest()
            return c + tag
        return c

    def unprotect(self, protected: bytes) -> bytes:
        if self.integrity == "sha256":
            if len(protected) < 32:
                raise ValueError("Truncated")
            c, tag = protected[:-32], protected[-32:]
            good = hmac.compare_digest(tag, hmac.new(self.key, c, hashlib.sha256).digest())
            if not good:
                raise ValueError("Integrity check failed")
        else:
            c = protected
        if self.cipher == "caesar":
            p = caesar_bytes(c, -self.shift)
        elif self.cipher == "xor":
            p = xor_keystream(c, self.key, self.rx_counter)
            self.rx_counter += 1
        else:
            raise ValueError("Unknown cipher")
        return p

def send_msg(sock: socket.socket, blob: bytes) -> None:
    sock.sendall(struct.pack(">I", len(blob)) + blob)

def recv_msg(sock: socket.socket) -> bytes:
    hdr = recvall(sock, 4)
    if not hdr:
        return b""
    (n,) = struct.unpack(">I", hdr)
    return recvall(sock, n)

def recvall(sock: socket.socket, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return b""
        buf.extend(chunk)
    return bytes(buf)

class VPNClientCore:
    def __init__(self, logq: "queue.Queue[str]"):
        self.logq = logq
        self.stop_event = threading.Event()
        self.udp_sock = None
        self.tcp_sock = None
        self.t1 = None
        self.t2 = None
        self.crypto = None

    def log(self, msg: str):
        self.logq.put(msg)

    def start(self, server_host: str, server_port: int,
              udp_listen: int, udp_peer_host: str, udp_peer_port: int,
              cipher: str, integrity: str):
        self.stop_event.clear()
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.bind(("0.0.0.0", udp_listen))
        self.log(f"[UDP] bound on :{udp_listen}")

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect((server_host, server_port))
        self.log(f"[TCP] connected to {server_host}:{server_port}")

        send_msg(self.tcp_sock, b"HELLO_CLIENT")
        a, A = dh_generate_keypair()
        send_msg(self.tcp_sock, json.dumps({"A": str(A)}).encode())
        resp = json.loads(recv_msg(self.tcp_sock).decode())
        B = int(resp["B"])
        key = dh_shared_secret(B, a)
        suite = {"cipher": cipher, "integrity": integrity}
        send_msg(self.tcp_sock, json.dumps({"suite": suite}).encode())
        ok = recv_msg(self.tcp_sock)
        if ok != b"OK":
            raise RuntimeError("Suite rejected by server")
        self.crypto = CryptoSuite(key, cipher=cipher, integrity=integrity)
        self.log(f"[HANDSHAKE] OK | suite={suite}")

        self.t1 = threading.Thread(target=self._udp_to_tcp, args=(self.udp_sock, self.tcp_sock, self.crypto), daemon=True)
        self.t2 = threading.Thread(target=self._tcp_to_udp, args=((udp_peer_host, udp_peer_port), self.udp_sock, self.tcp_sock, self.crypto), daemon=True)
        self.t1.start()
        self.t2.start()
        self.log("[BRIDGE] started")

    def stop(self):
        self.stop_event.set()
        try:
            if self.tcp_sock:
                self.tcp_sock.close()
        except Exception:
            pass
        try:
            if self.udp_sock:
                self.udp_sock.close()
        except Exception:
            pass
        self.log("[BRIDGE] stopped")

    def _udp_to_tcp(self, udp_sock, tcp_sock, crypto: CryptoSuite):
        while not self.stop_event.is_set():
            try:
                data, addr = udp_sock.recvfrom(65535)
            except OSError:
                break
            payload = json.dumps({"dir": "c2s", "b64": base64.b64encode(data).decode()}).encode()
            enc = crypto.protect(payload)
            try:
                send_msg(tcp_sock, enc)
            except OSError:
                break

    def _tcp_to_udp(self, udp_peer, udp_sock, tcp_sock, crypto: CryptoSuite):
        while not self.stop_event.is_set():
            try:
                enc = recv_msg(tcp_sock)
                if not enc:
                    break
                payload = crypto.unprotect(enc)
                obj = json.loads(payload.decode())
                data = base64.b64decode(obj["b64"])
                udp_sock.sendto(data, udp_peer)
            except Exception as e:
                self.log(f"[WARN] drop tcp packet: {e}")

class VPNClientGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VPN Client")
        self.geometry("700x520")
        self.resizable(False, False)
        self.core = VPNClientCore(logq=queue.Queue())
        self._build_ui()
        self.after(100, self._drain_logs)

    def _build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Server Host").grid(row=0, column=0, sticky="w")
        self.server_host = ttk.Entry(frm); self.server_host.insert(0, "127.0.0.1"); self.server_host.grid(row=0, column=1, sticky="ew")

        ttk.Label(frm, text="Server TCP Port").grid(row=1, column=0, sticky="w")
        self.server_port = ttk.Entry(frm); self.server_port.insert(0, "9000"); self.server_port.grid(row=1, column=1, sticky="ew")

        ttk.Label(frm, text="UDP Listen (client side)").grid(row=2, column=0, sticky="w")
        self.udp_listen = ttk.Entry(frm); self.udp_listen.insert(0, "6001"); self.udp_listen.grid(row=2, column=1, sticky="ew")

        ttk.Label(frm, text="UDP Peer Host (server side)").grid(row=3, column=0, sticky="w")
        self.udp_peer_host = ttk.Entry(frm); self.udp_peer_host.insert(0, "127.0.0.1"); self.udp_peer_host.grid(row=3, column=1, sticky="ew")

        ttk.Label(frm, text="UDP Peer Port (server->UDP2)").grid(row=4, column=0, sticky="w")
        self.udp_peer_port = ttk.Entry(frm); self.udp_peer_port.insert(0, "5002"); self.udp_peer_port.grid(row=4, column=1, sticky="ew")

        ttk.Label(frm, text="Cipher").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.cipher = ttk.Combobox(frm, values=["caesar", "xor"], state="readonly"); self.cipher.set("caesar"); self.cipher.grid(row=0, column=3, sticky="ew")

        ttk.Label(frm, text="Integrity").grid(row=1, column=2, sticky="w", padx=(20,0))
        self.integrity = ttk.Combobox(frm, values=["none", "sha256"], state="readonly"); self.integrity.set("none"); self.integrity.grid(row=1, column=3, sticky="ew")

        self.btn_start = ttk.Button(frm, text="Start", command=self.on_start); self.btn_start.grid(row=2, column=2, sticky="ew", padx=(20,0))
        self.btn_stop = ttk.Button(frm, text="Stop", command=self.on_stop, state="disabled"); self.btn_stop.grid(row=2, column=3, sticky="ew")

        ttk.Label(frm, text="Logs").grid(row=5, column=0, columnspan=4, sticky="w", pady=(10,0))
        self.txt = tk.Text(frm, height=18, width=80, state="disabled", bg="#0f172a", fg="#e5e7eb")
        self.txt.grid(row=6, column=0, columnspan=4, sticky="nsew")
        frm.columnconfigure(1, weight=1)
        frm.columnconfigure(3, weight=1)

    def on_start(self):
        try:
            host = self.server_host.get().strip()
            port = int(self.server_port.get())
            ul = int(self.udp_listen.get())
            uph = self.udp_peer_host.get().strip()
            upp = int(self.udp_peer_port.get())
            cipher = self.cipher.get()
            integ = self.integrity.get()
            threading.Thread(target=self._start_core_safe, args=(host, port, ul, uph, upp, cipher, integ), daemon=True).start()
            self.btn_start.config(state="disabled")
            self.btn_stop.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _start_core_safe(self, *args):
        try:
            self.core.start(*args)
        except Exception as e:
            self.core.log(f"[ERROR] {e}")
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")

    def on_stop(self):
        self.core.stop()
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")

    def _drain_logs(self):
        try:
            while True:
                msg = self.core.logq.get_nowait()
                self._append_log(msg)
        except queue.Empty:
            pass
        self.after(100, self._drain_logs)

    def _append_log(self, line: str):
        self.txt.configure(state="normal")
        self.txt.insert("end", line + "\n")
        self.txt.see("end")
        self.txt.configure(state="disabled")

if __name__ == "__main__":
    app = VPNClientGUI()
    app.mainloop()
