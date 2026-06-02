---
title: "Course: System Design"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, system-design, architecture, scalability]
prerequisites: [computer-networks, operating-systems, databases]
---

# System Design

> Back to [[../cs-syllabus|CS Syllabus]] | Related: [[computer-networks]], [[web-development]], [[security-cryptography]], [[software-engineering]]

## Motivation

Every software engineer eventually faces the question: "How would you design X at scale?" System design is the discipline of translating functional requirements into architectures that are scalable, reliable, maintainable, and cost-effective. Whether you are building a startup MVP or architecting infrastructure for millions of users, understanding distributed systems tradeoffs is essential. This course covers the patterns, principles, and practical reasoning behind large-scale system design.

## Prerequisites

- Solid understanding of networking fundamentals (TCP/IP, HTTP, DNS)
- Database fundamentals (SQL, indexing, transactions)
- Operating systems basics (processes, threads, memory)
- Familiarity with at least one backend framework

---

## 1. Foundational Concepts

### 1.1 Requirements Gathering
- Functional vs. non-functional requirements
- Back-of-the-envelope estimation: QPS, storage, bandwidth
- Identifying read-heavy vs. write-heavy workloads
- SLAs, SLOs, and SLIs — defining "good enough"

### 1.2 CAP Theorem and Beyond
- Consistency, Availability, Partition Tolerance — pick two (in practice, pick between C and A during partitions)
- PACELC extension: during Partition choose A or C; Else choose Latency or Consistency
- Eventual consistency, strong consistency, causal consistency
- Linearizability vs. serializability

### 1.3 Latency Numbers Every Engineer Should Know
- L1 cache: ~1 ns; L2 cache: ~4 ns; RAM: ~100 ns
- SSD random read: ~16 μs; HDD seek: ~4 ms
- Round trip within datacenter: ~500 μs
- Cross-continental round trip: ~150 ms

---

## 2. Architecture Patterns

### 2.1 Monolithic Architecture
- Single deployable unit; shared database
- Advantages: simplicity, easier debugging, single deployment pipeline
- Disadvantages: scaling bottlenecks, long build times, tight coupling
- When to choose: early-stage products, small teams, low complexity domains

### 2.2 Microservices
- Independent services with bounded contexts (Domain-Driven Design)
- Inter-service communication: synchronous (HTTP/gRPC) vs. asynchronous (message queues)
- Service discovery: client-side (Eureka) vs. server-side (Consul, Kubernetes DNS)
- Data ownership: each service owns its database
- Challenges: distributed transactions (Saga pattern), data consistency, operational complexity
- Anti-patterns: distributed monolith, nano-services

### 2.3 Serverless / FaaS
- AWS Lambda, Google Cloud Functions, Cloudflare Workers
- Event-driven execution; pay-per-invocation pricing
- Cold start latency and mitigation (provisioned concurrency, edge runtimes)
- Limitations: execution duration, statelessness, vendor lock-in

### 2.4 Event-Driven Architecture
- Producers, consumers, event brokers
- Event notification vs. event-carried state transfer vs. event sourcing
- Choreography (services react to events) vs. orchestration (central coordinator)
- Benefits: loose coupling, temporal decoupling, auditability

### 2.5 CQRS (Command Query Responsibility Segregation)
- Separate read and write models
- Write side: normalized, optimized for consistency
- Read side: denormalized, optimized for query performance
- Eventual consistency between read and write stores
- When to use: high read/write asymmetry, complex query requirements

### 2.6 Event Sourcing
- Store state as an append-only sequence of events rather than current state
- Reconstructing state by replaying events; snapshots for performance
- Benefits: complete audit trail, temporal queries, debugging
- Challenges: schema evolution, event versioning, eventual consistency
- Combination with CQRS: events drive read model projections

---

## 3. Scalability

### 3.1 Horizontal vs. Vertical Scaling
- Vertical: bigger machines (scale up) — simpler but has ceiling
- Horizontal: more machines (scale out) — requires statelessness or state externalization
- Diagonal scaling: scale up first, scale out when limits are hit

### 3.2 Load Balancing
- **Algorithms:** Round-robin, weighted round-robin, least connections, IP hash, consistent hashing
- **Layer 4 (transport):** TCP-level, faster, no content inspection (HAProxy, AWS NLB)
- **Layer 7 (application):** HTTP-aware, content-based routing, SSL termination (Nginx, AWS ALB)
- Health checks: active (probes) vs. passive (monitoring failures)
- Global load balancing: GeoDNS, Anycast

### 3.3 Caching Strategies
- **Cache-aside (lazy loading):** Application checks cache, falls back to DB, populates cache
- **Write-through:** Write to cache and DB simultaneously
- **Write-behind (write-back):** Write to cache, asynchronously persist to DB
- **Read-through:** Cache sits between application and DB, auto-fetches on miss
- Cache invalidation: TTL-based, event-based, versioned keys
- Cache stampede prevention: locking, probabilistic early expiration
- Tools: Redis, Memcached, application-level (Guava, Caffeine)

### 3.4 CDN (Content Delivery Network)
- Edge caching for static assets; reduces origin load and latency
- Push vs. pull CDNs
- Cache-Control headers: max-age, s-maxage, stale-while-revalidate
- Edge computing: running logic at CDN nodes (Cloudflare Workers, Lambda@Edge)

### 3.5 Database Scaling
- **Read replicas:** Route reads to replicas, writes to primary; replication lag
- **Sharding:** Horizontal partitioning by key; range-based vs. hash-based vs. directory-based
- **Partitioning:** Vertical (split columns) vs. horizontal (split rows)
- Challenges: cross-shard queries, rebalancing, hotspots
- NewSQL: CockroachDB, TiDB, Spanner — distributed SQL

---

## 4. Reliability and Fault Tolerance

### 4.1 Redundancy
- No single points of failure: multi-AZ, multi-region deployments
- Active-active vs. active-passive failover
- Data replication: synchronous vs. asynchronous; quorum writes (W + R > N)

### 4.2 Circuit Breaker Pattern
- States: Closed (normal) → Open (failing, fast-fail) → Half-Open (testing recovery)
- Prevents cascading failures across services
- Implementation: Hystrix (legacy), Resilience4j, Polly

### 4.3 Retry Strategies
- Immediate retry, fixed delay, exponential backoff with jitter
- Idempotency: ensure retries don't cause duplicate side effects (idempotency keys)
- Retry budgets: limit total retry rate across the system

### 4.4 Bulkhead Pattern
- Isolate resources so one failing component doesn't starve others
- Thread pool isolation, connection pool isolation
- Example: separate thread pools for critical vs. non-critical API calls

### 4.5 Rate Limiting
- **Algorithms:** Token bucket, leaky bucket, fixed window, sliding window log, sliding window counter
- Per-user, per-IP, per-API-key limits
- Response: HTTP 429 with Retry-After header
- Distributed rate limiting: Redis-based counters, API gateways

### 4.6 Chaos Engineering
- Principles: steady state hypothesis, introduce real-world failures, run in production
- Tools: Netflix Chaos Monkey, Gremlin, AWS Fault Injection Simulator
- Game days: planned failure injection exercises

---

## 5. API Design

### 5.1 REST
- Resource-oriented; HTTP verbs map to CRUD (GET, POST, PUT, PATCH, DELETE)
- HATEOAS: hypermedia links for discoverability (rarely used in practice)
- Pagination: offset-based, cursor-based (preferred for large datasets)
- Versioning: URL path (`/v1/`), header (`Accept: application/vnd.api.v1+json`), query param

### 5.2 GraphQL
- Single endpoint; client specifies exact data shape
- Schema-first vs. code-first design
- N+1 problem and DataLoader pattern for batching
- Subscriptions for real-time data
- Disadvantages: caching complexity, query cost analysis, over-fetching prevention

### 5.3 gRPC
- Protocol Buffers for serialization; HTTP/2 transport
- Streaming: unary, server-streaming, client-streaming, bidirectional
- Strong typing, code generation, high performance
- Best for: internal service-to-service communication

### 5.4 WebSocket
- Full-duplex communication over single TCP connection
- Use cases: chat, live dashboards, collaborative editing, gaming
- Scaling challenges: sticky sessions, connection state management
- Alternatives: Server-Sent Events (SSE) for one-way streaming

---

## 6. Message Queues and Streaming

### 6.1 Apache Kafka
- Distributed append-only log; topics partitioned across brokers
- Consumer groups: parallel processing with partition assignment
- Exactly-once semantics (idempotent producers + transactional consumers)
- Use cases: event streaming, log aggregation, change data capture (CDC)
- Retention: time-based or size-based; compacted topics for latest-value semantics

### 6.2 RabbitMQ
- AMQP protocol; exchanges (direct, topic, fanout, headers) route to queues
- Acknowledgments, dead-letter exchanges, priority queues
- Use cases: task queues, RPC, pub/sub with complex routing

### 6.3 AWS SQS / SNS
- SQS: managed queue; standard (at-least-once, best-effort ordering) vs. FIFO (exactly-once, ordered)
- SNS: pub/sub fan-out to SQS, Lambda, HTTP endpoints
- Visibility timeout, dead-letter queues, long polling

### 6.4 Choosing a Message System
- Kafka: high throughput, event replay, stream processing
- RabbitMQ: complex routing, low latency, traditional task queues
- SQS: fully managed, no operational burden, AWS-native integration

---

## 7. Observability

### 7.1 Logging
- Structured logging (JSON) with correlation IDs
- Log levels: DEBUG, INFO, WARN, ERROR, FATAL
- Centralized log aggregation: ELK stack (Elasticsearch, Logstash, Kibana), Loki + Grafana
- Retention policies and cost management

### 7.2 Metrics
- Types: counters, gauges, histograms, summaries
- RED method (Rate, Errors, Duration) for services
- USE method (Utilization, Saturation, Errors) for resources
- Tools: Prometheus + Grafana, Datadog, CloudWatch
- Alerting: thresholds, anomaly detection, paging vs. ticketing

### 7.3 Distributed Tracing
- Trace context propagation (W3C Trace Context, B3 headers)
- Spans, traces, and the directed acyclic graph of a request
- Tools: Jaeger, Zipkin, OpenTelemetry (vendor-neutral standard)
- Sampling strategies: head-based, tail-based, adaptive

---

## 8. Capacity Planning

- Traffic estimation: daily active users → QPS → peak QPS (typically 2-5x average)
- Storage estimation: per-record size × records/day × retention period
- Bandwidth estimation: QPS × average response size
- Infrastructure sizing: CPU, memory, disk IOPS, network throughput
- Cost modeling: reserved vs. on-demand instances, spot instances, serverless pricing

---

## 9. System Design Interview Patterns

### 9.1 Framework
1. **Clarify requirements** (5 min): functional, non-functional, constraints
2. **Estimate scale** (5 min): users, QPS, storage, bandwidth
3. **High-level design** (10 min): core components, data flow
4. **Deep dive** (15 min): database schema, API design, specific components
5. **Address bottlenecks** (5 min): scaling, reliability, monitoring

### 9.2 Classic Problems
- **URL shortener:** Hashing, base62 encoding, read-heavy caching, analytics pipeline
- **Twitter/feed:** Fan-out on write (celebrity problem), fan-out on read, hybrid approach
- **Chat system:** WebSocket connections, presence service, message storage, push notifications
- **Notification system:** Priority queues, rate limiting, delivery tracking, multi-channel (email, SMS, push)
- **Rate limiter:** Token bucket with Redis, sliding window, distributed coordination
- **Web crawler:** URL frontier, politeness (robots.txt, crawl delay), deduplication (Bloom filter), distributed work queue
- **Video streaming (YouTube):** Upload pipeline (transcode to multiple resolutions), CDN distribution, adaptive bitrate streaming
- **Distributed cache:** Consistent hashing, replication, eviction policies (LRU, LFU)
- **Search engine:** Inverted index, ranking (TF-IDF, PageRank), sharding by document vs. term
- **Payment system:** Idempotency, exactly-once processing, reconciliation, PCI compliance

---

## 10. Key Takeaways

- There is no single correct architecture — everything is a tradeoff
- Start simple, scale as needed; premature optimization is the root of evil
- Design for failure: assume every component can and will fail
- Data model drives everything; get the data model right first
- Measure before optimizing; observability is not optional

---

## References

- Kleppmann, M. *Designing Data-Intensive Applications* (2017) — the definitive reference
- Newman, S. *Building Microservices* (2nd ed., 2021)
- Burns, B. *Designing Distributed Systems* (2018)
- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/)
- Nygard, M. *Release It!* (2nd ed., 2018) — stability patterns
