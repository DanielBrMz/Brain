---
title: "Course: Distributed Systems"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, distributed-systems, consensus, replication]
prerequisites: [operating-systems, networking, data-structures-algorithms]
---

# Distributed Systems

> *Back to [[../cs-syllabus|CS Syllabus]] | Related: [[databases|Databases]], [[operating-systems|Operating Systems]], [[data-structures-algorithms|DSA]]*

## Motivation

A distributed system is a collection of independent computers that appears to its users as a single coherent system. Almost every modern application — web services, databases, messaging platforms, cloud infrastructure — is distributed. Understanding the fundamental constraints and design patterns of distributed systems is essential for building reliable, scalable software.

## Prerequisites

- **Operating Systems:** Processes, threads, IPC, networking fundamentals (see [[operating-systems|Operating Systems]])
- **Networking:** TCP/IP, HTTP, DNS, sockets, latency vs. bandwidth
- **Data Structures & Algorithms:** Hash tables, graphs, complexity analysis (see [[data-structures-algorithms|DSA]])

---

## I. Fundamental Concepts

### 1.1 Why Distribution is Hard

- **No global clock:** Processes cannot agree on the exact time. Clock skew and drift are unavoidable.
- **Partial failure:** Some nodes may fail while others continue operating. Must handle failure independently.
- **Network unreliability:** Messages can be lost, delayed, duplicated, or reordered.
- **The two generals' problem:** Impossibility of reaching agreement over an unreliable channel (no finite number of messages suffices).

### 1.2 System Models

**Timing Models:**
- **Synchronous:** Known upper bounds on message delay and process execution time. Unrealistic but useful for proofs.
- **Asynchronous:** No timing assumptions. Most general model. FLP impossibility result applies here.
- **Partially synchronous:** System is asynchronous but eventually behaves synchronously. Most practical model.

**Failure Models:**
- **Crash-stop:** Process halts and never recovers.
- **Crash-recovery:** Process may crash and restart with durable state.
- **Byzantine:** Process may behave arbitrarily (malicious or buggy). Requires 3f+1 nodes to tolerate f Byzantine failures.
- **Omission:** Process fails to send or receive messages.

### 1.3 The FLP Impossibility Result

- Fischer, Lynch, Paterson (1985): In an asynchronous system with even one crash-stop failure, no deterministic consensus protocol can guarantee termination.
- Implication: All practical consensus protocols must make timing assumptions or use randomization.
- Does NOT mean consensus is impossible in practice — just that it cannot be guaranteed in the pure asynchronous model.

---

## II. Time, Order, and Causality

### 2.1 Physical Clocks

- **Clock synchronization:** NTP (Network Time Protocol) achieves millisecond accuracy over the internet.
- **Google TrueTime:** GPS + atomic clocks providing bounded clock uncertainty [earliest, latest]. Used by Spanner for external consistency.
- **Limitations:** Physical clocks can never be perfectly synchronized; always have some uncertainty interval.

### 2.2 Logical Clocks

**Lamport Timestamps:**
- Each process maintains a counter. On send: increment and attach. On receive: set local clock to max(local, received) + 1.
- Establishes a total order consistent with causality: if a -> b (a causally precedes b), then L(a) < L(b).
- Converse is NOT true: L(a) < L(b) does not imply a -> b (concurrent events may be arbitrarily ordered).

**Vector Clocks:**
- Each process maintains a vector of counters (one per process).
- On send: increment own entry, attach vector. On receive: take element-wise max, then increment own entry.
- VC(a) < VC(b) iff a causally precedes b. VC(a) || VC(b) (incomparable) iff a and b are concurrent.
- Precisely captures causality but O(n) space per message where n = number of processes.

### 2.3 Happens-Before Relation

- Defined by Lamport: a -> b if (1) a and b are in the same process and a precedes b, (2) a is a send and b is the corresponding receive, or (3) transitivity.
- Events not related by -> are concurrent.
- Foundation for reasoning about consistency and conflict detection.

---

## III. The CAP Theorem and Consistency Models

### 3.1 CAP Theorem (Brewer's Theorem)

In the presence of a network partition (P), a distributed system must choose between:
- **Consistency (C):** Every read receives the most recent write or an error.
- **Availability (A):** Every request receives a non-error response (but possibly stale data).

**Clarifications:**
- CAP is about behavior DURING a partition. When the network is healthy, you can have both C and A.
- Not a binary choice — it's a spectrum. Systems make nuanced tradeoffs.
- **CP systems:** Sacrifice availability during partitions (e.g., HBase, MongoDB with majority writes).
- **AP systems:** Sacrifice consistency during partitions (e.g., Cassandra, DynamoDB with eventual consistency).
- **PACELC extension:** If Partition, choose A or C; Else (no partition), choose Latency or Consistency.

### 3.2 Consistency Models (Strongest to Weakest)

**Linearizability (Strong Consistency):**
- Operations appear to take effect instantaneously at some point between invocation and response.
- Equivalent to having a single copy of the data with atomic operations.
- Most intuitive but most expensive to implement in distributed settings.

**Sequential Consistency:**
- Operations appear to execute in some total order consistent with each process's program order.
- Weaker than linearizability: doesn't require real-time ordering between processes.

**Causal Consistency:**
- Causally related operations are seen in the same order by all processes.
- Concurrent operations may be seen in different orders by different processes.
- Captured by vector clocks.

**Eventual Consistency:**
- If no new updates are made, all replicas will eventually converge to the same value.
- No guarantees about when or what intermediate states will be observed.
- **Read-your-writes:** A session will always see its own previous writes (session guarantee).
- **Monotonic reads:** If a process reads value v, subsequent reads will not return a value older than v.

---

## IV. Consensus Protocols

### 4.1 The Consensus Problem

- Multiple nodes must agree on a single value.
- **Properties:** Agreement (all correct nodes decide the same value), Validity (decided value was proposed by some node), Termination (all correct nodes eventually decide).

### 4.2 Paxos

**Basic Paxos (Single-Decree):**
- **Roles:** Proposers, Acceptors, Learners.
- **Phase 1 (Prepare):** Proposer sends Prepare(n) with proposal number n. Acceptors respond with Promise (won't accept proposals with number < n) and any previously accepted value.
- **Phase 2 (Accept):** Proposer sends Accept(n, v) where v is either the highest-numbered previously accepted value or the proposer's own value. Acceptors accept if they haven't promised a higher number.
- **Majority quorum:** Requires responses from a majority of acceptors.
- **Safety:** Guaranteed. **Liveness:** Not guaranteed (dueling proposers can livelock).

**Multi-Paxos:**
- Optimize for repeated consensus: elect a stable leader who skips Phase 1 for subsequent rounds.
- In practice, this is what systems implement. Single-decree Paxos is a building block.

### 4.3 Raft

- Designed for understandability (compared to Paxos).
- **Leader election:** Candidates request votes; first to get majority becomes leader. Term numbers prevent split-brain.
- **Log replication:** Leader appends entries to its log and replicates to followers. Entry committed when majority have it.
- **Safety:** Leader Completeness Property — if an entry is committed, it will be present in all future leaders' logs.
- **Membership changes:** Joint consensus approach for safe cluster reconfiguration.
- Used in: etcd, CockroachDB, TiKV, Consul.

### 4.4 ZAB (Zookeeper Atomic Broadcast)

- Protocol behind Apache ZooKeeper.
- Similar to Raft/Multi-Paxos: leader-based, log replication with majority quorums.
- Differences: designed specifically for primary-backup replication; handles leader recovery differently.
- ZooKeeper provides: distributed locking, configuration management, service discovery, leader election as primitives.

### 4.5 Byzantine Fault Tolerance

- **PBFT (Practical Byzantine Fault Tolerance):** Three-phase protocol (pre-prepare, prepare, commit). Tolerates f faults with 3f+1 nodes.
- **Performance:** O(n^2) message complexity per consensus round.
- Used in permissioned blockchains and safety-critical systems.

---

## V. Replication

### 5.1 Single-Leader Replication

- One node designated as leader (primary/master); all writes go to leader.
- Leader replicates writes to followers (replicas/secondaries).
- **Synchronous replication:** Leader waits for follower acknowledgment before confirming write. Strong consistency but higher latency.
- **Asynchronous replication:** Leader confirms write immediately; replicates in background. Lower latency but risk of data loss on leader failure.
- **Semi-synchronous:** One follower is synchronous; rest are asynchronous. Guarantees at least one up-to-date replica.
- **Failover:** Detect leader failure -> elect new leader -> redirect clients. Complications: split-brain, lost writes.

### 5.2 Multi-Leader Replication

- Multiple nodes accept writes. Each leader replicates to all other leaders.
- **Use cases:** Multi-datacenter operation, offline clients (each device is a "leader").
- **Conflict resolution:** Last-writer-wins (LWW), merge/custom resolution, CRDTs.
- **Topologies:** All-to-all, circular, star. All-to-all is most fault-tolerant.

### 5.3 Leaderless Replication

- Any replica can accept reads and writes. No special leader role.
- **Quorum reads/writes:** Write to w replicas, read from r replicas. If w + r > n, guaranteed overlap ensures reading latest write.
- **Sloppy quorums:** Allow writes to non-home nodes during failures (hinted handoff). Increases availability at the cost of consistency.
- **Anti-entropy:** Background process to synchronize replicas (Merkle trees for efficient comparison).
- **Read repair:** On read, if stale value detected, update the stale replica.
- Used in: Dynamo, Cassandra, Riak.

---

## VI. Partitioning (Sharding)

### 6.1 Hash Partitioning

- Hash the key; assign to partition based on hash value.
- **Consistent hashing:** Ring-based assignment. Adding/removing nodes moves only K/n keys on average (K = total keys, n = nodes).
- **Virtual nodes:** Each physical node has multiple positions on the ring. Improves load balance.
- Destroys key ordering; range queries must scatter-gather across all partitions.

### 6.2 Range Partitioning

- Assign contiguous key ranges to partitions. Preserves sort order for efficient range queries.
- Risk of hot spots if access patterns are skewed (e.g., timestamps as keys).
- **Dynamic splitting/merging:** Split hot partitions, merge cold ones (used by HBase, Spanner).

### 6.3 Secondary Indexes on Partitioned Data

- **Local (document-partitioned) index:** Each partition maintains its own index over local data. Reads require scatter-gather.
- **Global (term-partitioned) index:** Index itself is partitioned across nodes. Reads go to one partition; writes must update multiple index partitions.

---

## VII. Transactions

### 7.1 ACID in Distributed Context

- **Atomicity:** All operations in a transaction succeed or all are rolled back.
- **Consistency:** Transaction moves the database from one valid state to another (application-level invariant).
- **Isolation:** Concurrent transactions don't interfere with each other.
- **Durability:** Committed data survives failures.
- In distributed systems, achieving ACID across multiple nodes is expensive. See [[databases|Databases]] for isolation levels.

### 7.2 Two-Phase Commit (2PC)

- **Phase 1 (Prepare):** Coordinator asks all participants to prepare (vote yes/no). Participants acquire locks, write to WAL.
- **Phase 2 (Commit/Abort):** If all vote yes, coordinator sends commit. If any vote no, coordinator sends abort.
- **Blocking protocol:** If coordinator crashes after prepare, participants holding locks are stuck until coordinator recovers.
- **Three-phase commit (3PC):** Adds a pre-commit phase to reduce blocking. Still not partition-tolerant.

### 7.3 Sagas

- Long-lived transactions decomposed into a sequence of local transactions, each with a compensating transaction.
- If step k fails, execute compensating transactions for steps k-1, k-2, ..., 1.
- **Choreography:** Each service listens for events and triggers the next step.
- **Orchestration:** Central coordinator directs the saga flow.
- No isolation between saga steps (no global locks). Must design for intermediate states being visible.

---

## VIII. Stream Processing

### 8.1 Apache Kafka

- Distributed commit log. Topics partitioned across brokers. Messages within a partition are strictly ordered.
- **Producers** write to partitions (by key hash or round-robin). **Consumers** read from partitions.
- **Consumer groups:** Each partition consumed by exactly one consumer in a group. Parallelism = number of partitions.
- **Retention:** Time-based or size-based. Log compaction retains latest value per key.
- **Exactly-once semantics:** Idempotent producers + transactional consumers.
- **Use cases:** Event sourcing, CDC (change data capture), real-time pipelines, log aggregation.

### 8.2 Stream Processing Frameworks

**Apache Flink:**
- True streaming (event-at-a-time, not micro-batch). Event time processing with watermarks.
- Checkpointing via Chandy-Lamport distributed snapshots. Exactly-once state consistency.
- Windowing: tumbling, sliding, session windows.

**Apache Spark Streaming / Structured Streaming:**
- Micro-batch processing. Higher latency but simpler fault tolerance (rerun the micro-batch).
- Structured Streaming: continuous processing mode for lower latency.

**Key Concepts:**
- **Event time vs. processing time:** Event time is when the event occurred; processing time is when it's processed. Handle late events with watermarks and allowed lateness.
- **Windowing:** Tumbling (non-overlapping fixed-size), sliding (overlapping), session (gap-based).
- **State management:** Keyed state (per-key), operator state (per-parallel instance). Must be checkpointable.

### 8.3 MapReduce

- **Map:** Apply a function to each input record, emit key-value pairs.
- **Shuffle:** Group all values by key across all mappers.
- **Reduce:** Aggregate values for each key.
- Batch processing paradigm. Fault tolerance via re-execution of failed tasks.
- Largely superseded by Spark (in-memory DAG execution) but the conceptual model remains foundational.

---

## IX. Conflict Resolution and CRDTs

### 9.1 Conflict-Free Replicated Data Types (CRDTs)

- Data structures that can be replicated across nodes and updated independently, with mathematical guarantees of convergence.
- **State-based (CvRDTs):** Merge states using a join operation on a semilattice. Require sending full state.
- **Operation-based (CmRDTs):** Broadcast operations. Operations must be commutative (and idempotent for at-least-once delivery).

**Common CRDTs:**
- **G-Counter:** Grow-only counter. Each node maintains its own count; total = sum of all nodes.
- **PN-Counter:** Pair of G-Counters (positive and negative). Value = P - N.
- **G-Set:** Grow-only set. Merge = union.
- **OR-Set (Observed-Remove Set):** Add and remove operations. Each add tagged with unique ID; remove only removes observed tags.
- **LWW-Register:** Last-writer-wins based on timestamp.
- **LWW-Element-Set:** Set with LWW semantics per element.

### 9.2 Gossip Protocols

- Epidemic-style information dissemination. Each node periodically shares state with random peers.
- **Push gossip:** Send updates to random peers.
- **Pull gossip:** Request updates from random peers.
- **Push-pull:** Bidirectional exchange.
- O(log n) rounds to reach all nodes with high probability.
- Used for: failure detection (SWIM protocol), membership, aggregate computation, anti-entropy.

---

## X. Practical Distributed Architecture

### 10.1 Microservices

- Decompose application into small, independently deployable services.
- Each service owns its data (database per service pattern).
- Communication: synchronous (REST, gRPC) or asynchronous (message queues, events).
- **Advantages:** Independent deployment, technology heterogeneity, team autonomy.
- **Challenges:** Network calls, distributed transactions, operational complexity, debugging.

### 10.2 Service Mesh

- Infrastructure layer handling service-to-service communication.
- **Sidecar proxy pattern:** Each service has a proxy (e.g., Envoy) handling traffic management, security, observability.
- **Control plane:** Configures all sidecars (e.g., Istio, Linkerd).
- Features: mutual TLS, traffic splitting, retries, circuit breaking, distributed tracing.

### 10.3 API Gateways

- Single entry point for external clients. Handles: routing, authentication, rate limiting, request transformation, caching.
- Tools: Kong, AWS API Gateway, Nginx, Traefik.
- **Backend for Frontend (BFF):** Separate gateway per client type (web, mobile, IoT).

### 10.4 Circuit Breakers

- Prevent cascade failures by detecting when a downstream service is failing and short-circuiting requests.
- **States:** Closed (normal operation) -> Open (requests fail immediately) -> Half-Open (allow limited requests to test recovery).
- Named after electrical circuit breakers. Implemented in libraries (Hystrix, Resilience4j) or service meshes.

### 10.5 Load Balancing

- **Algorithms:** Round-robin, weighted round-robin, least connections, consistent hashing, random with two choices (power of two choices).
- **Layer 4 (transport):** Route based on IP/port (HAProxy, AWS NLB). Fast but limited routing logic.
- **Layer 7 (application):** Route based on HTTP headers, URL path, cookies (Nginx, AWS ALB). More flexible.
- **Client-side:** Client discovers service instances and balances locally (gRPC client-side LB, Ribbon).

### 10.6 Observability

- **Three pillars:** Metrics (Prometheus, Grafana), Logs (ELK stack, Loki), Traces (Jaeger, Zipkin, OpenTelemetry).
- **Distributed tracing:** Propagate trace IDs across service calls. Visualize request flow and identify bottlenecks.
- **Health checks:** Liveness (is the process alive?) and readiness (is it ready to serve traffic?) probes.

---

## References

1. Kleppmann — *Designing Data-Intensive Applications* (DDIA)
2. van Steen, Tanenbaum — *Distributed Systems*, 4th ed. (free online)
3. Lamport — "Time, Clocks, and the Ordering of Events in a Distributed System" (1978)
4. Ongaro, Ousterhout — "In Search of an Understandable Consensus Algorithm" (Raft, 2014)
5. Brewer — "CAP Twelve Years Later" (2012)
6. Shapiro et al. — "Conflict-Free Replicated Data Types" (2011)
7. Kafka documentation (kafka.apache.org)
8. Google — "Spanner: Google's Globally-Distributed Database" (2012)
9. Amazon — "Dynamo: Amazon's Highly Available Key-value Store" (2007)
10. Jepsen.io — Distributed systems correctness testing and analyses
