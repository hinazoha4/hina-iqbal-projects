# Building a Mini VPN Using Python

## Overview
This project demonstrates how two UDP clients can communicate securely through a VPN tunnel built with Python. The VPN Client and VPN Server form a TCP-encrypted link between the UDP endpoints using Diffie–Hellman key exchange and simple symmetric encryption (Caesar/XOR).

## Files
```
prog_udp1.py       # UDP client 1
prog_udp2.py       # UDP client 2
vpn_client.py      # VPN client (UDP <-> TCP bridge)
vpn_server.py      # VPN server (TCP <-> UDP bridge)
README.md
```

## How to Run

### Step 1: Start VPN Server
```bash
python3 vpn_server.py --tcp-port 9000 --udp-listen 6002 --udp-peer-host 127.0.0.1 --udp-peer-port 5002
```

### Step 2: Start VPN Client
```bash
python3 vpn_client.py --server-host 127.0.0.1 --server-port 9000 --udp-listen 6001 --udp-peer-host 127.0.0.1 --udp-peer-port 5001
```

### Step 3: Start UDP Clients
#### UDP1
```bash
python3 prog_udp1.py --bind-port 5001 --bridge-host 127.0.0.1 --bridge-port 6001
```
#### UDP2
```bash
python3 prog_udp2.py --bind-port 5002 --bridge-host 127.0.0.1 --bridge-port 6002
```

## Communication Flow
```
UDP1 (5001) → VPN Client (6001) → TCP (9000) → VPN Server (6002) → UDP2 (5002)
UDP2 (5002) → VPN Server (6002) → TCP (9000) → VPN Client (6001) → UDP1 (5001)
```

## Test
Type in UDP1 terminal:
```
hello from udp1
```
It will appear in UDP2 terminal, and vice versa.
