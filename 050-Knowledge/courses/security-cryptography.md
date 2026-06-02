---
title: "Course: Security & Cryptography"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, security, cryptography, web-security]
prerequisites: [computer-networks, discrete-math, probability]
---

# Security & Cryptography

> Back to [[../cs-syllabus|CS Syllabus]] | Related: [[computer-networks]], [[web-development]], [[system-design]]

## Motivation

Security is not a feature — it is a property of a system. Every application handles sensitive data, authenticates users, and communicates over untrusted networks. Understanding cryptographic primitives, secure protocol design, and common vulnerability classes is essential for building systems that protect users. This course covers cryptographic foundations, web application security, authentication protocols, and network security.

## Prerequisites

- Number theory basics (modular arithmetic, prime numbers)
- Probability and information theory fundamentals
- Networking (TCP/IP, HTTP, TLS handshake overview)
- Web development basics (HTTP, cookies, sessions, JavaScript)

---

## 1. Symmetric Encryption

### 1.1 Fundamentals
- Same key for encryption and decryption
- Key distribution problem: how do both parties get the same key securely?
- Kerckhoffs' principle: security depends on key secrecy, not algorithm secrecy

### 1.2 AES (Advanced Encryption Standard)
- Block cipher: 128-bit blocks; key sizes: 128, 192, or 256 bits
- SubBytes → ShiftRows → MixColumns → AddRoundKey (10/12/14 rounds)
- Hardware acceleration: AES-NI instructions on modern CPUs
- Considered secure for all key sizes; ubiquitous in practice

### 1.3 ChaCha20
- Stream cipher by Daniel Bernstein
- 256-bit key, 96-bit nonce, 32-bit counter
- 20 rounds of quarter-round operations on 4×4 state matrix
- Faster than AES on hardware without AES-NI (mobile, embedded)
- Used in TLS 1.3, WireGuard, SSH

### 1.4 Block Cipher Modes of Operation
- **ECB (Electronic Codebook):** Each block encrypted independently — NEVER use (reveals patterns)
- **CBC (Cipher Block Chaining):** XOR with previous ciphertext block; requires IV; padding oracle attacks
- **CTR (Counter):** Encrypt counter values, XOR with plaintext; parallelizable; no padding needed
- **GCM (Galois/Counter Mode):** CTR + authentication tag (GHASH); provides AEAD
  - AEAD (Authenticated Encryption with Associated Data): confidentiality + integrity + authenticity
  - AES-256-GCM is the gold standard for symmetric encryption
- **ChaCha20-Poly1305:** ChaCha20 stream cipher + Poly1305 MAC; AEAD alternative to AES-GCM

### 1.5 Key Principles
- Never reuse a nonce with the same key (catastrophic for CTR/GCM/ChaCha20)
- Always use authenticated encryption (AEAD) — encryption alone does not prevent tampering
- Generate keys from cryptographically secure random number generators (CSPRNG)

---

## 2. Asymmetric Encryption

### 2.1 Fundamentals
- Key pair: public key (encrypt/verify) + private key (decrypt/sign)
- Computationally expensive compared to symmetric encryption
- Hybrid encryption: use asymmetric to exchange symmetric key, then use symmetric for data

### 2.2 RSA
- Based on difficulty of factoring large semiprimes (n = p × q)
- Key generation: choose primes p, q; compute n = pq, φ(n) = (p-1)(q-1); choose e (typically 65537); compute d = e⁻¹ mod φ(n)
- Encrypt: c = mᵉ mod n; Decrypt: m = cᵈ mod n
- Key sizes: 2048-bit minimum, 4096-bit recommended
- RSA-OAEP for encryption (not raw/textbook RSA); RSA-PSS for signatures
- Slower than ECC for equivalent security; larger key sizes

### 2.3 Elliptic Curve Cryptography (ECC)
- Based on difficulty of Elliptic Curve Discrete Logarithm Problem (ECDLP)
- Smaller keys for equivalent security: 256-bit ECC ≈ 3072-bit RSA
- **ECDSA:** Digital signature algorithm on elliptic curves; used in TLS, Bitcoin
- **Ed25519:** Edwards-curve Digital Signature Algorithm; deterministic (no random nonce), fast, constant-time
  - Preferred over ECDSA: no nonce reuse vulnerability, simpler implementation
- **ECDH / X25519:** Elliptic curve Diffie-Hellman key agreement
  - X25519: Curve25519-based; used in TLS 1.3, WireGuard, Signal

### 2.4 Diffie-Hellman Key Exchange
- Two parties agree on a shared secret over an insecure channel
- Classic DH: based on discrete logarithm in multiplicative group of integers mod p
- ECDH: same concept on elliptic curves; smaller, faster
- Vulnerable to man-in-the-middle without authentication (must be combined with signatures or certificates)
- **Forward secrecy:** Use ephemeral DH keys per session; compromised long-term key doesn't reveal past sessions

---

## 3. Hash Functions and MACs

### 3.1 Cryptographic Hash Functions
- Properties: deterministic, fast, pre-image resistant, second pre-image resistant, collision resistant
- **SHA-2 family:** SHA-256, SHA-384, SHA-512; widely used; no known practical attacks
- **SHA-3 (Keccak):** Different construction (sponge); backup if SHA-2 is broken; not widely deployed
- **MD5, SHA-1:** Broken (collision attacks demonstrated); do not use for security
- Use cases: data integrity, digital signatures, proof of work, content addressing

### 3.2 HMAC (Hash-based Message Authentication Code)
- HMAC(K, m) = H((K' ⊕ opad) || H((K' ⊕ ipad) || m))
- Provides message authentication and integrity
- Used in: API authentication, JWT signatures (HS256), TLS record protocol

### 3.3 Key Derivation Functions (KDFs)
- Derive cryptographic keys from passwords or other key material
- **PBKDF2:** Iterated HMAC; configurable iterations; NIST approved but GPU-friendly
- **bcrypt:** Blowfish-based; fixed memory usage; salt built-in; widely used for password storage
- **scrypt:** Memory-hard; resists GPU/ASIC attacks; configurable CPU and memory cost
- **Argon2:** Winner of Password Hashing Competition (2015)
  - Argon2id: recommended variant (hybrid of data-dependent and data-independent)
  - Parameters: memory, iterations, parallelism
  - Current best practice for new password storage

---

## 4. Digital Signatures and PKI

### 4.1 Digital Signatures
- Sign with private key; verify with public key
- Provides: authentication (who sent it), integrity (not modified), non-repudiation (can't deny sending)
- Process: hash the message, sign the hash (not the raw message)
- Algorithms: RSA-PSS, ECDSA, Ed25519

### 4.2 Certificates and PKI
- X.509 certificate: binds a public key to an identity (domain name)
- Certificate chain: end-entity cert → intermediate CA → root CA
- Root CAs are pre-installed in OS/browser trust stores
- Certificate fields: subject, issuer, validity period, public key, extensions (SAN, key usage)
- **Let's Encrypt:** Free, automated CA using ACME protocol; 90-day certificates
- **Certificate Transparency (CT):** Public logs of all issued certificates; detect rogue certs
- Revocation: CRL (Certificate Revocation List) or OCSP (Online Certificate Status Protocol)
  - OCSP stapling: server fetches OCSP response and staples it to TLS handshake

### 4.3 TLS 1.3 Handshake (Detailed)
1. **Client Hello:** Supported cipher suites, key shares (ECDHE), supported groups, SNI
2. **Server Hello:** Chosen cipher suite, server key share
3. **Encrypted Extensions:** Server sends additional parameters (encrypted)
4. **Certificate + CertificateVerify:** Server proves identity with certificate and signature
5. **Finished:** Server sends MAC of handshake transcript
6. **Client Finished:** Client sends MAC of handshake transcript
- **1-RTT:** Full handshake completes in one round trip
- **0-RTT:** Resumed connections can send data immediately (replay risk — server must handle idempotently)
- Only AEAD ciphers: AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305
- Only ephemeral key exchange: forward secrecy mandatory

---

## 5. Web Security (OWASP Top 10)

### 5.1 Injection Attacks
- **SQL Injection:** Unsanitized user input in SQL queries
  - Mitigation: parameterized queries / prepared statements (NEVER string concatenation)
  - ORM usage reduces risk but does not eliminate it (raw queries, dynamic filters)
- **Command Injection:** User input passed to shell commands
  - Mitigation: avoid shell execution; use language APIs; allowlist inputs

### 5.2 Cross-Site Scripting (XSS)
- **Stored XSS:** Malicious script stored in database, rendered to other users
- **Reflected XSS:** Script in URL parameter reflected in response
- **DOM-based XSS:** Client-side JavaScript manipulates DOM with untrusted data
- Mitigation: output encoding (HTML entities), Content Security Policy (CSP), sanitization libraries (DOMPurify)
- React/Next.js: JSX auto-escapes by default; `dangerouslySetInnerHTML` is the escape hatch (dangerous)

### 5.3 Cross-Site Request Forgery (CSRF)
- Attacker tricks authenticated user into making unintended requests
- Mitigation: CSRF tokens (synchronizer token pattern), SameSite cookies, check Origin/Referer headers
- SameSite=Lax (default in modern browsers): cookies not sent on cross-site POST requests

### 5.4 Server-Side Request Forgery (SSRF)
- Application makes HTTP requests to attacker-controlled URLs
- Can access internal services, cloud metadata endpoints (169.254.169.254)
- Mitigation: allowlist URLs/domains, block private IP ranges, use network segmentation

### 5.5 Broken Authentication
- Weak passwords, credential stuffing, session fixation
- Mitigation: MFA, rate limiting, account lockout, secure session management

### 5.6 Other OWASP Categories
- **Broken Access Control:** IDOR (Insecure Direct Object References), missing authorization checks
- **Security Misconfiguration:** Default credentials, verbose error messages, unnecessary services
- **Vulnerable Dependencies:** Known CVEs in libraries; use `npm audit`, Dependabot, Snyk
- **Cryptographic Failures:** Weak algorithms, hardcoded keys, insufficient entropy
- **Logging & Monitoring Failures:** No audit trail; unable to detect breaches

### 5.7 JWT Security
- Structure: Header.Payload.Signature (base64url encoded)
- Algorithms: HS256 (HMAC-SHA256, symmetric), RS256 (RSA-SHA256, asymmetric), ES256 (ECDSA)
- **"alg": "none" attack:** Never accept unsigned tokens; validate algorithm server-side
- **Key confusion:** HS256 with RS256 public key — always enforce expected algorithm
- Short expiry + refresh tokens; store in httpOnly cookies (not localStorage)
- Token blacklisting via Redis for logout (since JWTs are stateless)

### 5.8 CORS (Cross-Origin Resource Sharing)
- Browser enforces Same-Origin Policy; CORS relaxes it for specific origins
- Headers: `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Credentials`
- Preflight requests (OPTIONS) for non-simple requests
- Never use `Access-Control-Allow-Origin: *` with `credentials: true`

---

## 6. Authentication Protocols

### 6.1 OAuth 2.0
- Authorization framework (not authentication); delegates access without sharing credentials
- **Roles:** Resource Owner, Client, Authorization Server, Resource Server
- **Flows:**
  - **Authorization Code + PKCE:** Recommended for all clients (web, mobile, SPA)
  - **Client Credentials:** Machine-to-machine (no user involved)
  - **Device Code:** For input-constrained devices (smart TVs)
  - **Implicit flow:** Deprecated (token in URL fragment — insecure)
- Access tokens (short-lived) + refresh tokens (long-lived, rotated)

### 6.2 OpenID Connect (OIDC)
- Identity layer on top of OAuth 2.0; adds authentication
- ID token: JWT containing user identity claims (sub, email, name)
- UserInfo endpoint for additional claims
- Discovery document: `/.well-known/openid-configuration`
- Providers: Google, Microsoft, Auth0, Keycloak

### 6.3 SAML 2.0
- XML-based SSO protocol; primarily enterprise
- Identity Provider (IdP) authenticates user; sends signed assertion to Service Provider (SP)
- More complex than OIDC; still common in enterprise environments

### 6.4 Passkeys / WebAuthn
- FIDO2 standard: passwordless authentication using public key cryptography
- Authenticator generates key pair; private key stays on device; public key registered with server
- Challenge-response: server sends challenge, authenticator signs it with private key
- Phishing-resistant: bound to origin (RP ID)
- Passkeys: synced across devices via platform (iCloud Keychain, Google Password Manager)

### 6.5 Keycloak
- Open-source identity and access management
- Supports: OIDC, SAML, OAuth 2.0, LDAP/AD federation
- Features: SSO, MFA, user federation, fine-grained authorization, admin console
- Common in enterprise Java/microservice environments

---

## 7. Network Security

### 7.1 VPN
- Encrypts all traffic between client and VPN server
- Use cases: remote access, site-to-site, privacy
- Protocols: IPsec (complex, kernel-level), OpenVPN (SSL-based), WireGuard (modern, minimal)
- See [[computer-networks]] for protocol details

### 7.2 Firewalls
- Packet filtering: iptables/nftables rules (source/dest IP, port, protocol)
- Stateful: track connections; allow return traffic automatically
- WAF (Web Application Firewall): inspect HTTP traffic; block XSS, SQLi, etc.
- Zero-trust: authenticate every request regardless of network location

### 7.3 IDS/IPS
- Intrusion Detection: monitor and alert (Snort, Suricata, Zeek)
- Intrusion Prevention: monitor, alert, and block inline
- Signature-based vs. anomaly-based detection

### 7.4 DNS Security
- DNSSEC: cryptographic signatures on DNS records; validates authenticity
- DNS over HTTPS (DoH) / DNS over TLS (DoT): encrypt DNS queries
- DNS-based attacks: cache poisoning, DNS amplification DDoS

---

## 8. Secure Development Practices

### 8.1 Principles
- **Least privilege:** Grant minimum permissions necessary
- **Defense in depth:** Multiple layers of security
- **Fail secure:** Default to deny on error
- **Secure by default:** Secure configuration out of the box

### 8.2 Secrets Management
- Never hardcode secrets in source code
- Environment variables (acceptable for dev; not ideal for production)
- Secrets managers: HashiCorp Vault, AWS Secrets Manager, 1Password Secrets Automation
- Rotate secrets regularly; audit access

### 8.3 Dependency Security
- Audit dependencies: `npm audit`, `pip audit`, `cargo audit`
- Lock files: pin exact versions (package-lock.json, Pipfile.lock, Cargo.lock)
- Automated scanning: Dependabot, Snyk, Renovate
- Supply chain attacks: verify package integrity, use SBOMs

### 8.4 Security Headers
- `Strict-Transport-Security` (HSTS): force HTTPS
- `Content-Security-Policy` (CSP): control resource loading
- `X-Content-Type-Options: nosniff`: prevent MIME sniffing
- `X-Frame-Options: DENY`: prevent clickjacking
- `Referrer-Policy`: control referrer information leakage

---

## Key Concepts Summary

1. **Use AEAD** (AES-GCM or ChaCha20-Poly1305) — never roll your own crypto
2. **Forward secrecy** via ephemeral key exchange protects past sessions
3. **Hash passwords with Argon2id** — never SHA-256, never plaintext
4. **Parameterized queries** eliminate SQL injection — always
5. **CSP + output encoding** prevent XSS; **SameSite cookies** prevent CSRF
6. **OAuth 2.0 + PKCE** for authorization; **OIDC** for authentication
7. **Zero trust:** Authenticate everything, encrypt everything, log everything

---

## References

- Ferguson, N., Schneier, B., Kohno, T. *Cryptography Engineering* (2010)
- Rescorla, E. *TLS 1.3 — RFC 8446* (2018)
- OWASP Foundation. [OWASP Top 10](https://owasp.org/www-project-top-ten/) (2021)
- Bernstein, D.J. [Curve25519 Paper](https://cr.yp.to/ecdh/curve25519-20060209.pdf)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- Aumasson, J.P. *Serious Cryptography* (2018)
- [Web Security Academy (PortSwigger)](https://portswigger.net/web-security)
- Biryukov, A., Dinu, D., Khovratovich, D. *Argon2 — RFC 9106* (2021)
