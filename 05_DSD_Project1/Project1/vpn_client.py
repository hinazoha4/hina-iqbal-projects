

import argparse
import base64
import hashlib
import hmac
import json
import secrets
import socket
import struct
import threading
import time
from typing import Tuple

# ===== Diffie–Hellman (2048-bit group) =====
P_HEX = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A63A36210000000000090563", 16
)
G = 2

def dh_generate_keypair() -> Tuple[int, int]:
    a = secrets.randbelow(P_HEX - 2) + 2
    A = pow(G, a, P_HEX)
    return a, A

def dh_shared_secret(their_pub: int, my_priv: int) -> bytes:
    s = pow(their_pub, my_priv, P_HEX)
    return hashlib.sha256(str(s).encode()).digest()

# ===== Ciphers =====
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

# ===== TCP framing =====
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

# ===== Manager =====
def manager_menu():
    print("\n=== VPN CLIENT – Manager Menu ===")
    print("Choose symmetric cipher: 1) caesar (default)  2) xor")
    csel = input("Selection [1/2]: ").strip() or "1"
    cipher = "caesar" if csel == "1" else "xor"

    print("Choose integrity: 1) none (default)  2) sha256")
    isel = input("Selection [1/2]: ").strip() or "1"
    integrity = "none" if isel == "1" else "sha256"

    print(f"Active config -> cipher={cipher}, integrity={integrity}")
    return cipher, integrity

# ===== Bridge loops =====
def udp_to_tcp(udp_sock: socket.socket, tcp_sock: socket.socket, crypto: CryptoSuite):
    while True:
        data, addr = udp_sock.recvfrom(65535)
        payload = json.dumps({"dir": "c2s", "b64": base64.b64encode(data).decode()}).encode()
        enc = crypto.protect(payload)
        send_msg(tcp_sock, enc)

def tcp_to_udp(udp_peer, udp_sock: socket.socket, tcp_sock: socket.socket, crypto: CryptoSuite):
    while True:
        enc = recv_msg(tcp_sock)
        if not enc:
            print("TCP closed.")
            break
        try:
            payload = crypto.unprotect(enc)
            obj = json.loads(payload.decode())
            data = base64.b64decode(obj["b64"])
            udp_sock.sendto(data, udp_peer)
        except Exception as e:
            print(f"[WARN] drop tcp packet: {e}")

def main():
    ap = argparse.ArgumentParser(description="VPN Client – UDP<->TCP bridge")
    ap.add_argument("--server-host", required=True)
    ap.add_argument("--server-port", type=int, required=True)
    ap.add_argument("--udp-listen", type=int, default=6001, help="UDP port to receive from prog_udp1")
    ap.add_argument("--udp-peer-host", default="127.0.0.1", help="Where to send UDP (toward UDP2)")
    ap.add_argument("--udp-peer-port", type=int, default=5002, help="UDP port of prog_udp2")
    ap.add_argument("--manager", choices=["interactive", "none"], default="interactive")
    args = ap.parse_args()

    if args.manager == "interactive":
        cipher, integrity = manager_menu()
    else:
        cipher, integrity = "caesar", "none"

    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("0.0.0.0", args.udp_listen))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.server_host, args.server_port))

    send_msg(s, b"HELLO_CLIENT")
    a, A = dh_generate_keypair()
    send_msg(s, json.dumps({"A": str(A)}).encode())
    resp = json.loads(recv_msg(s).decode())
    B = int(resp["B"])
    key = dh_shared_secret(B, a)

    suite = {"cipher": cipher, "integrity": integrity}
    send_msg(s, json.dumps({"suite": suite}).encode())
    ok = recv_msg(s)
    if ok != b"OK":
        raise SystemExit("Suite rejected by server")
    crypto = CryptoSuite(key, cipher=cipher, integrity=integrity)
    print(f"[CLIENT] Handshake complete. Suite={suite}")

    t1 = threading.Thread(target=udp_to_tcp, args=(udp_sock, s, crypto), daemon=True)
    t2 = threading.Thread(target=tcp_to_udp, args=((args.udp_peer_host, args.udp_peer_port), udp_sock, s, crypto), daemon=True)
    t1.start()
    t2.start()

    try:
        while t1.is_alive() and t2.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        s.close()

if __name__ == "__main__":
    main()
