---
title: "Course: Computer Networks"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, networking, tcp-ip, protocols]
prerequisites: [operating-systems-basics]
---

# Computer Networks

> Back to [[../cs-syllabus|CS Syllabus]] | Related: [[system-design]], [[security-cryptography]], [[web-development]]

## Motivation

Every modern application is networked. Understanding how data moves from one machine to another — from the electrical signals on a wire to the HTTP request in your browser — is foundational for debugging performance issues, designing distributed systems, and building secure applications. This course covers the full networking stack, from physical transmission to application-layer protocols.

## Prerequisites

- Basic understanding of operating systems (processes, I/O)
- Binary arithmetic and basic data structures
- Familiarity with command-line tools (curl, ping, traceroute, netstat)

---

## 1. The OSI Model and TCP/IP Stack

### 1.1 OSI Seven-Layer Model
| Layer | Name         | Function                          | PDU      | Example          |
|-------|-------------|-----------------------------------|----------|------------------|
| 7     | Application  | User-facing protocols             | Data     | HTTP, DNS, SMTP  |
| 6     | Presentation | Encoding, encryption, compression | Data     | TLS, JPEG, JSON  |
| 5     | Session      | Session management                | Data     | NetBIOS, RPC     |
| 4     | Transport    | End-to-end delivery, reliability  | Segment  | TCP, UDP, QUIC   |
| 3     | Network      | Routing and addressing            | Packet   | IP, ICMP, BGP    |
| 2     | Data Link    | Node-to-node transfer             | Frame    | Ethernet, WiFi   |
| 1     | Physical     | Bit transmission                  | Bit      | Fiber, copper    |

### 1.2 TCP/IP Four-Layer Model
- Application (OSI 5-7), Transport (OSI 4), Internet (OSI 3), Link (OSI 1-2)
- In practice, TCP/IP is the model that matters; OSI is a teaching tool
- Encapsulation: each layer wraps the payload with its own header

### 1.3 Packet Lifecycle
- Application creates data → TCP segments it → IP adds addressing → Ethernet frames it
- At each router: strip link layer, inspect IP, re-frame for next hop
- Destination reverses the process (decapsulation)

---

## 2. Application Layer

### 2.1 HTTP/1.1
- Text-based request/response protocol over TCP
- Persistent connections (Keep-Alive) to avoid TCP handshake per request
- Pipelining: send multiple requests without waiting (but head-of-line blocking)
- Methods: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
- Status codes: 1xx informational, 2xx success, 3xx redirect, 4xx client error, 5xx server error
- Headers: Content-Type, Cache-Control, Authorization, Cookie, ETag, Accept-Encoding

### 2.2 HTTP/2
- Binary framing layer; multiplexed streams over single TCP connection
- Header compression (HPACK): reduces overhead for repetitive headers
- Server push: proactively send resources the client will need
- Stream prioritization and flow control
- Still suffers from TCP head-of-line blocking (one lost packet blocks all streams)

### 2.3 HTTP/3 and QUIC
- QUIC: UDP-based transport with built-in TLS 1.3
- Eliminates TCP head-of-line blocking: independent streams
- 0-RTT connection establishment (for resumed connections)
- Connection migration: survives IP changes (mobile switching WiFi to cellular)
- QPACK for header compression (adapted from HPACK for out-of-order delivery)

### 2.4 DNS (Domain Name System)
- Hierarchical namespace: root → TLD (.com) → SLD (example.com) → subdomains
- Record types: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), NS (nameserver), TXT, SRV, SOA
- Resolution process: recursive resolver → root → TLD → authoritative nameserver
- Caching: TTL-based at every level (resolver, OS, browser)
- DNS over HTTPS (DoH) and DNS over TLS (DoT) for privacy
- DNS-based load balancing: round-robin A records, GeoDNS, weighted records

### 2.5 Other Application Protocols
- **SMTP/IMAP/POP3:** Email delivery and retrieval
- **FTP/SFTP:** File transfer; FTP is legacy (cleartext), SFTP uses SSH tunnel
- **WebSocket:** Upgrade from HTTP; full-duplex, persistent connection
- **SSH:** Secure remote shell; key exchange, authentication, tunneling

---

## 3. Transport Layer

### 3.1 TCP (Transmission Control Protocol)
- **Connection establishment:** Three-way handshake (SYN → SYN-ACK → ACK)
- **Reliability:** Sequence numbers, acknowledgments, retransmission
- **Flow control:** Sliding window; receiver advertises window size
- **Congestion control:**
  - **Slow start:** Exponential growth of congestion window (cwnd) until threshold (ssthresh)
  - **Congestion avoidance:** Linear growth after ssthresh
  - **Fast retransmit:** Retransmit after 3 duplicate ACKs (don't wait for timeout)
  - **Fast recovery:** Halve cwnd instead of resetting to 1 (Reno); CUBIC uses cubic function
  - Modern variants: BBR (Google) — model-based, not loss-based; measures bandwidth and RTT
- **Connection teardown:** Four-way handshake (FIN → ACK → FIN → ACK); TIME_WAIT state
- **TCP options:** MSS, window scaling, timestamps, selective acknowledgments (SACK)

### 3.2 UDP (User Datagram Protocol)
- Connectionless, unreliable, no ordering guarantees
- Minimal overhead: 8-byte header (source port, dest port, length, checksum)
- Use cases: DNS queries, video streaming, gaming, VoIP
- Application must handle reliability if needed (e.g., QUIC built on UDP)

### 3.3 QUIC
- Multiplexed streams without head-of-line blocking
- Integrated TLS 1.3 (encrypted by default, including headers)
- Connection ID allows migration across network changes
- Implemented in user space (not kernel) — faster iteration

### 3.4 Port Numbers
- Well-known ports (0-1023): HTTP=80, HTTPS=443, SSH=22, DNS=53, SMTP=25
- Registered ports (1024-49151): application-specific
- Ephemeral ports (49152-65535): dynamically assigned to client connections

---

## 4. Network Layer

### 4.1 IP (Internet Protocol)
- **IPv4:** 32-bit addresses (4.3 billion); header: version, TTL, protocol, source/dest IP, checksum
- **IPv6:** 128-bit addresses; simplified header, no checksum (delegated to upper layers), flow labels
- **Subnetting:** CIDR notation (e.g., 192.168.1.0/24); subnet mask determines network vs. host bits
- **Private address ranges:** 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

### 4.2 Routing Protocols
- **BGP (Border Gateway Protocol):** Inter-AS routing; path-vector protocol; policy-based
  - eBGP between autonomous systems, iBGP within
  - Internet backbone routing; route announcements and withdrawals
  - BGP hijacking: security concern when routes are maliciously announced
- **OSPF (Open Shortest Path First):** Intra-AS; link-state protocol
  - Each router maintains complete topology map
  - Dijkstra's algorithm for shortest path computation
  - Areas for hierarchical routing; designated routers for efficiency
- **RIP (Routing Information Protocol):** Distance-vector; hop count metric; max 15 hops; largely obsolete

### 4.3 NAT (Network Address Translation)
- Maps private IPs to public IPs; conserves IPv4 address space
- Port-based NAT (NAPT/PAT): many private IPs share one public IP via port mapping
- NAT traversal challenges: peer-to-peer applications, VoIP
- Solutions: STUN, TURN, ICE (used in WebRTC)

### 4.4 ICMP (Internet Control Message Protocol)
- Error reporting and diagnostics; not a transport protocol
- Types: Echo Request/Reply (ping), Destination Unreachable, Time Exceeded (traceroute), Redirect
- traceroute: sends packets with incrementing TTL; each router returns Time Exceeded

### 4.5 IP Fragmentation
- MTU (Maximum Transmission Unit): typically 1500 bytes for Ethernet
- IPv4: routers can fragment; reassembly at destination
- IPv6: no router fragmentation; source must do Path MTU Discovery (PMTUD)

---

## 5. Data Link Layer

### 5.1 Ethernet (IEEE 802.3)
- Frame structure: preamble, dest MAC, source MAC, EtherType, payload (46-1500 bytes), FCS
- MAC addresses: 48-bit, globally unique (OUI + device ID)
- CSMA/CD: collision detection (mostly irrelevant with full-duplex switched Ethernet)

### 5.2 ARP (Address Resolution Protocol)
- Resolves IP addresses to MAC addresses within a LAN
- ARP request (broadcast) → ARP reply (unicast)
- ARP cache/table; ARP spoofing as a security attack vector

### 5.3 Switches and VLANs
- Layer 2 switches: learn MAC addresses, forward frames based on MAC table
- Spanning Tree Protocol (STP): prevents loops in switched networks
- VLANs (802.1Q): logically segment a physical network; trunk ports carry tagged frames

### 5.4 Layer 2 vs. Layer 3
- Switches operate at Layer 2 (MAC addresses); routers at Layer 3 (IP addresses)
- Layer 3 switches: combine switching speed with routing capability

---

## 6. Wireless Networking

### 6.1 WiFi (IEEE 802.11)
- Standards: 802.11a/b/g/n/ac/ax (WiFi 6)/be (WiFi 7)
- CSMA/CA: collision avoidance (can't detect collisions in wireless)
- Frequency bands: 2.4 GHz (longer range, more interference), 5 GHz, 6 GHz (WiFi 6E)
- Security: WEP (broken) → WPA → WPA2 (AES-CCMP) → WPA3 (SAE handshake)
- Roaming, handoff, mesh networking

### 6.2 Cellular Networks
- Generations: 3G (HSPA), 4G LTE, 5G (mmWave, sub-6 GHz)
- Cell towers, handoff between cells, spectrum allocation
- 5G innovations: network slicing, massive MIMO, edge computing integration

---

## 7. Network Security

### 7.1 TLS/SSL
- TLS 1.3 handshake: 1-RTT (client hello with key share → server hello with key share → encrypted)
- Certificate chain: server cert → intermediate CA → root CA
- Cipher suites: key exchange (ECDHE) + authentication (ECDSA/RSA) + encryption (AES-GCM/ChaCha20) + hash (SHA-256)
- Certificate Transparency (CT) logs; OCSP stapling for revocation checking
- See [[security-cryptography]] for detailed cryptographic foundations

### 7.2 VPN and WireGuard
- VPN: encrypted tunnel between client and server; all traffic routed through tunnel
- IPsec: complex, kernel-level; IKE for key exchange
- OpenVPN: SSL/TLS-based, user-space, widely compatible
- **WireGuard:** Modern, minimal (~4000 lines of code), kernel-level
  - Noise protocol framework for key exchange
  - ChaCha20-Poly1305 for encryption
  - Cryptokey routing: associates public keys with allowed IPs

### 7.3 Firewalls
- Packet filtering: rules based on IP, port, protocol (iptables, nftables)
- Stateful inspection: tracks connection state; allows return traffic
- Application-layer firewalls / WAF: inspect HTTP content, block attacks
- Network segmentation: DMZ, internal zones

### 7.4 IDS/IPS
- **IDS (Intrusion Detection System):** Monitor and alert; passive
- **IPS (Intrusion Prevention System):** Monitor, alert, and block; inline
- Signature-based (known patterns) vs. anomaly-based (deviation from baseline)
- Tools: Snort, Suricata, Zeek (formerly Bro)

---

## 8. Socket Programming

### 8.1 Berkeley Sockets API
- `socket()` → `bind()` → `listen()` → `accept()` (server)
- `socket()` → `connect()` (client)
- `send()`/`recv()` for TCP; `sendto()`/`recvfrom()` for UDP

### 8.2 Concurrency Models
- **Process-per-connection:** fork a new process (Apache prefork)
- **Thread-per-connection:** one thread per client (simpler, but thread overhead)
- **Event-driven / I/O multiplexing:** `select()`, `poll()`, `epoll()` (Linux), `kqueue()` (BSD)
  - Single-threaded event loop (Node.js model)
  - Non-blocking I/O with readiness notification
- **Async I/O:** io_uring (Linux), IOCP (Windows)

### 8.3 Practical Considerations
- `SO_REUSEADDR`: allow binding to recently closed port
- `TCP_NODELAY`: disable Nagle's algorithm for low-latency applications
- `SO_KEEPALIVE`: detect dead connections
- Backlog queue: `listen(sockfd, backlog)` — size of pending connection queue

---

## 9. CDN Architecture

- **Points of Presence (PoPs):** Edge servers deployed globally
- **Origin shield:** Intermediate cache layer to reduce origin load
- **Cache key:** URL + headers (Vary); purging and invalidation strategies
- **Anycast:** Same IP announced from multiple locations; BGP routes to nearest
- **TLS at the edge:** Terminate TLS at CDN; re-encrypt to origin or use plain HTTP
- Major providers: Cloudflare, Akamai, Fastly, AWS CloudFront

---

## 10. Practical Tools and Debugging

| Tool        | Purpose                                    |
|-------------|-------------------------------------------|
| `ping`      | ICMP echo; check reachability, measure RTT |
| `traceroute`| Path discovery via TTL expiration          |
| `dig`/`nslookup` | DNS resolution queries               |
| `curl`      | HTTP requests; inspect headers, timing     |
| `netstat`/`ss` | Socket and connection statistics        |
| `tcpdump`   | Packet capture at the command line         |
| `wireshark` | GUI packet analysis; filter by protocol    |
| `nmap`      | Port scanning, service detection           |
| `mtr`       | Combined ping + traceroute                 |
| `iperf`     | Network throughput measurement             |

---

## Key Concepts Summary

1. **Layering** provides abstraction; each layer has a well-defined interface
2. **End-to-end principle:** Put complexity at endpoints, keep the network simple
3. **TCP provides reliability** at the cost of latency; UDP provides speed at the cost of reliability
4. **DNS is the phone book** of the internet; its caching hierarchy is critical for performance
5. **HTTP has evolved** from simple text protocol to multiplexed binary streams (HTTP/3/QUIC)
6. **Network security is defense in depth:** encryption (TLS), access control (firewalls), monitoring (IDS)

---

## References

- Kurose, J. & Ross, K. *Computer Networking: A Top-Down Approach* (8th ed., 2021)
- Tanenbaum, A. & Wetherall, D. *Computer Networks* (6th ed., 2021)
- Stevens, W.R. *TCP/IP Illustrated, Volume 1* (2nd ed., 2011)
- [RFC 9000 — QUIC Transport Protocol](https://www.rfc-editor.org/rfc/rfc9000)
- [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/)
- [WireGuard Whitepaper](https://www.wireguard.com/papers/wireguard.pdf)
