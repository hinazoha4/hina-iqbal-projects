
import argparse
import socket
import threading
import sys

def reader(sock: socket.socket):
    while True:
        data, addr = sock.recvfrom(65535)
        print(f"\n[UDP2] recv: {data.decode(errors='replace')}")
        print("> ", end="", flush=True)

def main():
    ap = argparse.ArgumentParser(description="UDP endpoint 2")
    ap.add_argument("--bind-port", type=int, default=5002)
    ap.add_argument("--bridge-host", default="127.0.0.1")
    ap.add_argument("--bridge-port", type=int, default=6002)
    args = ap.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", args.bind_port))

    threading.Thread(target=reader, args=(s,), daemon=True).start()
    print(f"[UDP2] Bound on :{args.bind_port}, sending to bridge {args.bridge_host}:{args.bridge_port}")
    try:
        while True:
            msg = input("> ")
            if not msg:
                continue
            s.sendto(msg.encode(), (args.bridge_host, args.bridge_port))
    except KeyboardInterrupt:
        print("\nbye.")
        sys.exit(0)

if __name__ == "__main__":
    main()
