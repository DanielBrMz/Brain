---
title: "Computer Science — Complete Syllabus"
type: reference
status: active
created: 2026-03-22
tags: [knowledge, cs, syllabus]
---

# Computer Science — Complete Syllabus

> Exhaustive CS curriculum expanded from [[academic-taxonomy]] sections 2.1--2.7, with additional coverage of operating systems, compilers, networks, and software engineering. Each entry includes key concepts and practical connections.

See also: [[knowledge-index|Knowledge Index]]

---

## Course Notes

| Section | Course Note |
|---------|------------|
| 1. DSA | [[courses/data-structures-algorithms\|Data Structures & Algorithms]] |
| 2. System Design | [[courses/system-design\|System Design]], [[courses/distributed-systems\|Distributed Systems]] |
| 3. Databases | [[courses/databases\|Databases]] |
| 4. Operating Systems | [[courses/operating-systems\|Operating Systems]] |
| 5. Computer Networks | [[courses/computer-networks\|Computer Networks]] |
| 6. Compilers | [[courses/compilers\|Compilers]] |
| 7. Machine Learning | [[courses/machine-learning\|Machine Learning]], [[courses/deep-learning\|Deep Learning]] |
| 8. NLP | [[courses/nlp\|Natural Language Processing]] |
| 9. Computer Vision | [[courses/computer-vision\|Computer Vision]] |
| 10. Reinforcement Learning | [[courses/reinforcement-learning\|Reinforcement Learning]] |
| 11. Medical Imaging | [[courses/medical-imaging\|Medical Imaging AI]], [[courses/mri-physics\|MRI Physics]] |
| 12. Security | [[courses/security-cryptography\|Cryptography & Security]] |
| 13. Software Engineering | [[courses/software-engineering\|Software Engineering]] |
| 14. Web Development | [[courses/web-development\|Web Development]] |
| 15. Automata & Computation | [[courses/automata-computation\|Automata & Computation]] |
| 16. Formal Verification | [[courses/formal-verification\|Formal Verification]] |
| 17. Quantum Computing | [[courses/quantum-computing\|Quantum Computing]] |

---

## 1. Data Structures & Algorithms

### 1.1 Primitive & Linear Structures

- **Arrays** — Contiguous memory, O(1) random access, O(n) insert/delete. Foundation of nearly every other structure. Fixed-size vs dynamic (ArrayList, Python list).
- **Linked Lists** — Singly, doubly, circular. O(1) insert/delete at known position, O(n) search. Used in LRU caches, adjacency lists, undo history.
- **Stacks** — LIFO. Call stack, expression evaluation, DFS iteration, parenthesis matching. Implemented via array or linked list.
- **Queues** — FIFO. BFS, task scheduling, buffering. Variants: deque (double-ended), circular buffer, priority queue.
- **Hash Tables** — Key-value mapping via hash function. O(1) average lookup/insert. Collision resolution: chaining, open addressing (linear probing, quadratic probing, double hashing, Robin Hood). Load factor, rehashing. Python `dict`, Java `HashMap`.
- **Strings** — Immutable in most languages. Encoding (ASCII, UTF-8, UTF-16). StringBuilder pattern for efficient concatenation.

### 1.2 Trees

- **Binary Trees** — At most two children per node. Traversals: inorder, preorder, postorder, level-order. Used as foundation for BSTs, heaps, expression trees.
- **Binary Search Trees (BST)** — Left < root < right invariant. O(log n) average search/insert/delete, O(n) worst case if unbalanced. Inorder traversal yields sorted order.
- **AVL Trees** — Self-balancing BST using height-based balance factor (-1, 0, +1). Rotations (single, double) restore balance after insert/delete. Guarantees O(log n) worst case.
- **Red-Black Trees** — Self-balancing BST with color invariants. Less strictly balanced than AVL but fewer rotations on insert/delete. Used in `std::map`, `TreeMap`, Linux CFS scheduler.
- **B-Trees / B+ Trees** — Multi-way balanced trees optimized for disk I/O. Each node holds multiple keys. B+ trees store data only at leaves with leaf-level linked list. Foundation of database indexes and filesystems (ext4, NTFS).
- **Segment Trees** — Range query + point update in O(log n). Lazy propagation for range updates. Used in competitive programming and interval-based analytics.
- **Fenwick Trees (Binary Indexed Trees)** — Prefix sums with O(log n) update and query. More memory-efficient than segment trees for simpler range queries.
- **Tries (Prefix Trees)** — Character-by-character tree for string sets. O(m) lookup where m = string length. Autocomplete, IP routing (Patricia/radix tries), spell checkers.
- **Splay Trees** — Self-adjusting BST that moves accessed elements to root via splaying. Amortized O(log n). Good for caches with temporal locality.
- **Treaps** — BST + heap hybrid using random priorities. Expected O(log n) operations. Simpler to implement than AVL/RB.
- **K-D Trees** — Binary space partitioning for k-dimensional points. Nearest neighbor search, range queries in geometric data.
- **Interval Trees** — Stores intervals, supports efficient overlap queries. Used in genomics, scheduling, calendar applications.
- **Merkle Trees** — Hash tree where each leaf is a data hash and each internal node is the hash of its children. Used in Git, blockchain, certificate transparency.

### 1.3 Heaps & Priority Queues

- **Binary Heap** — Complete binary tree satisfying heap property (min or max). O(log n) insert/extract, O(1) peek. Array-backed (parent at i, children at 2i+1, 2i+2). Used in Dijkstra, heapsort, scheduling.
- **d-ary Heaps** — Generalization with d children. Shallower tree decreases extract time at cost of sifting. Used in Dijkstra when decrease-key is frequent.
- **Fibonacci Heaps** — Amortized O(1) insert, merge, decrease-key; O(log n) extract-min. Theoretically optimal for Dijkstra and Prim but high constant factors limit practical use.
- **Binomial Heaps** — Collection of binomial trees with efficient merge in O(log n). Stepping stone to Fibonacci heaps.
- **Pairing Heaps** — Simpler than Fibonacci with competitive practical performance. Amortized O(log n) delete-min, O(1) insert/merge.

### 1.4 Graphs

- **Representations** — Adjacency matrix (O(V^2) space, O(1) edge lookup), adjacency list (O(V+E) space, efficient for sparse graphs), edge list.
- **Traversals** — BFS (level-order, shortest path in unweighted graphs, O(V+E)), DFS (topological sort, cycle detection, connected components, O(V+E)).
- **Shortest Paths** — Dijkstra (non-negative weights, O((V+E) log V) with binary heap), Bellman-Ford (handles negative weights, O(VE), detects negative cycles), Floyd-Warshall (all-pairs, O(V^3), DP on intermediate vertices), A* (heuristic-guided, optimal with admissible heuristic).
- **Minimum Spanning Trees** — Kruskal (sort edges, union-find, O(E log E)), Prim (grow tree from vertex, O((V+E) log V) with heap). Cut property justifies greedy.
- **Topological Sort** — Linear ordering of DAG vertices. Kahn's algorithm (BFS with in-degree), DFS-based (reverse post-order). Used in build systems, dependency resolution, course scheduling.
- **Strongly Connected Components** — Tarjan's algorithm (single DFS, O(V+E)), Kosaraju's (two-pass DFS). Model cycles in directed graphs (deadlock detection, 2-SAT).
- **Network Flow** — Ford-Fulkerson method (augmenting paths), Edmonds-Karp (BFS, O(VE^2)), Dinic's (blocking flows, O(V^2 E)). Max-flow min-cut theorem. Applications: bipartite matching, circulation, project selection.
- **Bipartite Matching** — Hopcroft-Karp (O(E sqrt(V))). Hungarian algorithm for weighted matching. Applications: job assignment, stable matching.
- **Eulerian/Hamiltonian Paths** — Eulerian: visit every edge exactly once (exists iff 0 or 2 odd-degree vertices). Hierholzer's algorithm. Hamiltonian: visit every vertex exactly once (NP-complete in general).
- **Graph Coloring** — Assign colors so no adjacent vertices share a color. Chromatic number is NP-hard to compute. Greedy gives at most Delta+1 colors. Used in register allocation, scheduling.

### 1.5 Algorithm Paradigms

- **Divide & Conquer** — Split problem into independent subproblems, solve recursively, combine. Merge sort, quicksort, Strassen matrix multiplication, closest pair of points. Master theorem for recurrence analysis.
- **Dynamic Programming** — Optimal substructure + overlapping subproblems. Top-down (memoization) vs bottom-up (tabulation). Classic problems: knapsack, LCS, edit distance, matrix chain, coin change, LIS. State compression with bitmask DP.
- **Greedy Algorithms** — Locally optimal choices lead to global optimum (requires proof via exchange argument or matroid theory). Activity selection, Huffman coding, Kruskal/Prim, fractional knapsack.
- **Backtracking** — Explore solution space recursively, prune invalid branches. N-queens, Sudoku, constraint satisfaction, subset generation. Optimization: constraint propagation, forward checking.
- **Branch & Bound** — Backtracking with bounding function to prune. Used in integer programming, TSP. Lower bounds guide exploration priority (best-first search).
- **Randomized Algorithms** — Las Vegas (always correct, random runtime: randomized quicksort), Monte Carlo (bounded error: Miller-Rabin primality). Randomized skip lists, treaps, reservoir sampling.
- **Amortized Analysis** — Average cost per operation over a sequence of operations. Techniques: aggregate, accounting, potential method. Examples: dynamic array doubling (amortized O(1) append), splay tree operations.

### 1.6 String Algorithms

- **KMP (Knuth-Morris-Pratt)** — Pattern matching in O(n+m) using failure function. Avoids re-scanning matched characters.
- **Rabin-Karp** — Rolling hash for pattern matching. Expected O(n+m), worst O(nm). Good for multi-pattern search.
- **Boyer-Moore** — Practical fast matching using bad character and good suffix heuristics. Sublinear average case.
- **Aho-Corasick** — Multi-pattern matching using trie + failure links. O(n + m + z) where z = matches. Used in intrusion detection, grep.
- **Suffix Arrays** — Sorted array of all suffixes. O(n log n) or O(n) construction. LCP array for longest common prefix queries. More cache-friendly than suffix trees.
- **Suffix Trees** — Compressed trie of all suffixes. O(n) construction (Ukkonen's). Solves many string problems in linear time: longest repeated substring, longest common substring.
- **Z-Algorithm** — Computes Z-array (length of longest substring starting at i matching a prefix) in O(n). Pattern matching and string periodicity.
- **Manacher's Algorithm** — Find all palindromic substrings in O(n). Longest palindromic substring.

### 1.7 Computational Geometry

- **Convex Hull** — Gift wrapping (O(nh)), Graham scan (O(n log n)), Andrew's monotone chain. Foundation for many geometric algorithms.
- **Line Sweep** — Process events left-to-right. Segment intersection (Bentley-Ottmann), closest pair, area of union of rectangles.
- **Voronoi Diagrams** — Partition space by nearest site. Dual of Delaunay triangulation. Applications: nearest neighbor, facility location.
- **Range Trees / k-d Trees** — Multi-dimensional range queries. Fractional cascading for speed.

### 1.8 Complexity Theory

- **P** — Problems solvable in polynomial time by a deterministic Turing machine. Sorting, shortest paths, matching.
- **NP** — Problems verifiable in polynomial time. Includes P and NP-complete.
- **NP-Complete** — Hardest problems in NP. Cook-Levin theorem (SAT is NP-complete). Reductions: 3-SAT, vertex cover, clique, Hamiltonian cycle, subset sum, TSP (decision).
- **NP-Hard** — At least as hard as NP-complete; may not be in NP (optimization versions of NP-complete problems, halting problem).
- **PSPACE** — Problems solvable with polynomial space. PSPACE-complete: QBF, generalized chess/Go.
- **Approximation Algorithms** — Polynomial-time algorithms with provable approximation ratios. Vertex cover (2-approx), metric TSP (1.5-approx Christofides), set cover (ln n-approx). PTAS and FPTAS for certain problems.
- **Parameterized Complexity** — FPT algorithms: exponential only in a parameter k, polynomial in input size. Vertex cover in O(2^k * n). Kernelization.

---

## 2. System Design

### 2.1 Distributed Systems

- **CAP Theorem** — A distributed system can guarantee at most two of: Consistency, Availability, Partition tolerance. In practice, partitions are inevitable so the real trade-off is between C and A. PACELC extends this to latency trade-offs.
- **Consensus Protocols** — Raft (leader election, log replication, safety -- understandable alternative to Paxos), Paxos (original, more complex), ZAB (ZooKeeper), PBFT (Byzantine fault tolerance). Impossibility: FLP theorem (no deterministic consensus in async system with one failure).
- **Replication** — Single-leader (simple, potential bottleneck), multi-leader (conflict resolution needed), leaderless (quorum reads/writes, anti-entropy, read repair). Conflict resolution: LWW, vector clocks, CRDTs.
- **Partitioning/Sharding** — Hash-based (consistent hashing for minimal reshuffling), range-based (good for range queries, hotspot risk). Rebalancing: fixed partitions, dynamic splitting. Cross-partition queries are expensive.
- **Vector Clocks & Logical Time** — Lamport timestamps (total order, not causality), vector clocks (capture causality, O(n) size), hybrid logical clocks (physical + logical).
- **Distributed Transactions** — 2PC (blocking, coordinator is SPOF), 3PC (non-blocking but more messages), Saga pattern (compensating transactions for long-running workflows). Exactly-once semantics via idempotency keys.

### 2.2 Databases

- **ACID** — Atomicity (all or nothing), Consistency (valid state transitions), Isolation (concurrent transactions don't interfere), Durability (committed data survives crashes). WAL (write-ahead log) enables atomicity and durability.
- **Isolation Levels** — Read uncommitted (dirty reads), read committed (no dirty reads), repeatable read (no fuzzy reads), serializable (no phantom reads). MVCC enables snapshot isolation without locks (PostgreSQL, MySQL InnoDB).
- **Indexing** — B-tree indexes (range queries, ordered access), hash indexes (equality only), GIN/GiST (full-text, spatial in PostgreSQL), bitmap indexes (low cardinality OLAP), covering indexes, partial indexes. Index-only scans avoid heap access.
- **Query Optimization** — Cost-based optimizer estimates row counts, I/O cost. Join algorithms: nested loop, hash join (equality), merge join (sorted). EXPLAIN ANALYZE in PostgreSQL. Statistics, histograms, query plan caching.
- **NoSQL Patterns** — Key-value (Redis, DynamoDB), document (MongoDB -- flexible schema, denormalized), wide-column (Cassandra -- partition key + clustering key), graph (Neo4j -- traversal-heavy). Choose based on access patterns.
- **CRDTs (Conflict-free Replicated Data Types)** — Convergent data structures for eventual consistency without coordination. G-Counter, PN-Counter, LWW-Register, OR-Set. Used in collaborative editing, mobile offline-first apps.
- **LSM Trees** — Log-structured merge trees. Write-optimized: sequential writes to memtable, flush to sorted SSTables, background compaction. Used in LevelDB, RocksDB, Cassandra. Trade-off: write amplification vs read amplification.
- **Time-Series Databases** — Optimized for append-heavy timestamped data. Compression (delta-of-delta, Gorilla), downsampling, retention policies. InfluxDB, TimescaleDB (PostgreSQL extension).

### 2.3 Architecture Patterns

- **Microservices** — Independently deployable services around business capabilities. Benefits: independent scaling, team autonomy, polyglot. Costs: distributed system complexity, data consistency, operational overhead. Service boundaries via domain-driven design (bounded contexts).
- **Event Sourcing** — Store state changes as an immutable append-only log of events rather than current state. Enables audit trail, temporal queries, event replay. Requires snapshotting for performance. Pairs with CQRS.
- **CQRS (Command Query Responsibility Segregation)** — Separate read and write models. Write model handles commands (domain logic), read model optimized for queries (denormalized, eventually consistent). Reduces contention at cost of complexity.
- **Saga Pattern** — Manage distributed transactions as a sequence of local transactions with compensating actions for rollback. Choreography (events) vs orchestration (central coordinator). Used in order processing, payment workflows.
- **Service Mesh** — Infrastructure layer for service-to-service communication. Sidecar proxy (Envoy) handles mTLS, retries, load balancing, observability. Istio, Linkerd. Separates networking concerns from application code.
- **API Gateway** — Single entry point for clients. Handles routing, authentication, rate limiting, request transformation, response aggregation. Kong, AWS API Gateway. BFF (Backend for Frontend) pattern for client-specific gateways.
- **Hexagonal Architecture (Ports & Adapters)** — Core domain logic surrounded by ports (interfaces) and adapters (implementations). Decouples business logic from infrastructure. Testable: swap adapters for mocks.
- **Strangler Fig Pattern** — Incrementally migrate a monolith to microservices by routing traffic to new services while keeping the old system running. Reduces migration risk.

### 2.4 Scalability

- **Load Balancing** — Distribute traffic across servers. Algorithms: round-robin, weighted, least connections, IP hash, consistent hashing. L4 (TCP) vs L7 (HTTP) balancing. Health checks, draining. HAProxy, NGINX, AWS ALB/NLB.
- **Caching** — Reduce latency and load. Cache-aside (application manages), write-through (cache updated on write), write-behind (async write to DB). Eviction: LRU, LFU, TTL. Redis (in-memory data structure store), Memcached (simpler key-value). Cache stampede prevention (locking, probabilistic early expiration).
- **CDN (Content Delivery Network)** — Edge servers cache static content geographically close to users. Pull (lazy populate) vs push (pre-populate). Cache invalidation via TTL or purge. CloudFront, Cloudflare.
- **Sharding** — Horizontal partitioning across databases. Shard key selection is critical (cardinality, distribution, query patterns). Cross-shard queries are expensive. Resharding (consistent hashing, virtual nodes).
- **Message Queues** — Decouple producers and consumers. Kafka (distributed log, partitions, consumer groups, exactly-once semantics), RabbitMQ (AMQP, exchanges, routing), SQS (managed, at-least-once). Dead letter queues for failed messages.
- **Database Read Replicas** — Scale reads by replicating to read-only copies. Replication lag means eventual consistency. Useful for analytics, reporting workloads.

### 2.5 Reliability

- **Circuit Breakers** — Prevent cascading failures by stopping calls to failing services. States: closed (normal), open (fail fast), half-open (test recovery). Hystrix pattern. Configurable thresholds and timeouts.
- **Retries & Backoff** — Retry transient failures with exponential backoff + jitter to avoid thundering herd. Idempotency keys ensure safe retries. Budget retries to prevent amplification.
- **Bulkheads** — Isolate failure domains (separate thread pools, connection pools, or processes per dependency). Prevents one slow dependency from consuming all resources.
- **Rate Limiting** — Token bucket, leaky bucket, sliding window. Protect services from overload. Response: 429 Too Many Requests with Retry-After header. Distributed rate limiting via Redis.
- **Chaos Engineering** — Proactively inject failures to discover weaknesses. Chaos Monkey (random instance termination), Litmus (Kubernetes). Steady-state hypothesis, blast radius control, automated rollback.
- **Observability** — Three pillars: metrics (Prometheus, Grafana), logs (structured logging, ELK stack, CloudWatch), traces (distributed tracing via OpenTelemetry, Jaeger). SLIs/SLOs/SLAs. Alert on symptoms, not causes.
- **Health Checks & Graceful Degradation** — Liveness (process alive) vs readiness (can serve traffic) probes. Feature flags for degraded mode. Fallback responses when dependencies fail.

### 2.6 Networking

- **TCP/UDP** — TCP: reliable, ordered, connection-oriented (three-way handshake, flow control, congestion control -- CUBIC, BBR). UDP: unreliable, connectionless, low overhead (DNS, video streaming, gaming).
- **HTTP/1.1, HTTP/2, HTTP/3** — HTTP/1.1 (keep-alive, pipelining), HTTP/2 (binary framing, multiplexing, header compression -- HPACK, server push), HTTP/3 (QUIC over UDP, 0-RTT, connection migration).
- **gRPC** — Binary RPC framework using Protocol Buffers over HTTP/2. Streaming (unary, server, client, bidirectional). Efficient for microservice communication. Code generation for multiple languages.
- **WebSockets** — Full-duplex communication over single TCP connection. Upgrade from HTTP. Used for real-time features: chat, live updates, collaborative editing. Socket.io adds fallbacks.
- **DNS** — Hierarchical naming. Record types: A, AAAA, CNAME, MX, NS, TXT, SRV. Resolution: recursive vs iterative. TTL-based caching. DNS-based load balancing, failover.
- **TLS** — Transport Layer Security. Handshake: key exchange (ECDHE), authentication (certificates), symmetric encryption (AES-GCM). Certificate chains, CA trust, certificate pinning. TLS 1.3 reduces handshake to 1-RTT.
- **Load Balancer Internals** — L4 (DSR, NAT) vs L7 (terminates TLS, inspects HTTP). Connection draining, sticky sessions, health checks. Global load balancing via GeoDNS or anycast.

---

## 3. Programming Languages

### 3.1 Python

- **CPython Internals** — Reference implementation. Bytecode compilation (.pyc), evaluation loop (ceval.c), reference counting + cyclic GC. `dis` module to inspect bytecode. Object model: everything is a PyObject with ob_type and ob_refcnt.
- **GIL (Global Interpreter Lock)** — Mutex protecting Python objects from concurrent access. Only one thread executes bytecode at a time. CPU-bound parallelism requires multiprocessing, C extensions, or subinterpreters (PEP 554). I/O-bound code still benefits from threading.
- **Metaclasses** — Classes are instances of metaclasses. `type` is the default metaclass. `__new__` creates the class, `__init__` initializes it. Used in ORMs (SQLAlchemy declarative base), validation frameworks.
- **Descriptors** — Objects defining `__get__`, `__set__`, `__delete__`. Underpin `property`, `classmethod`, `staticmethod`, `__slots__`. Data descriptors (with `__set__`) take precedence over instance `__dict__`.
- **Asyncio** — Event loop, coroutines (`async def`), `await`, `asyncio.gather` for concurrency. `aiohttp`, `asyncpg` for async I/O. Task scheduling, `asyncio.Queue`. uvloop for performance. trio/anyio as alternatives.
- **Type Hints** — PEP 484+. `typing` module: `Optional`, `Union`, `Generic`, `Protocol` (structural subtyping). `TypeVar`, `ParamSpec`. mypy, pyright for static checking. Runtime: `get_type_hints()`, pydantic validation.
- **Memory Model** — Everything is an object on the heap. Small integer caching (-5 to 256), string interning. `__slots__` reduces per-instance memory. `sys.getsizeof()`, `tracemalloc` for profiling. Weak references via `weakref`.
- **Iterators & Generators** — Iterator protocol: `__iter__`, `__next__`. Generators via `yield` (lazy evaluation, memory-efficient). Generator expressions. `itertools` for combinatorial iterators. `yield from` for delegation. Async generators.
- **Context Managers** — `__enter__`/`__exit__` protocol. `contextlib.contextmanager` decorator. Used for resource management (files, locks, DB connections, HTTP sessions). `contextlib.asynccontextmanager` for async.

### 3.2 TypeScript / JavaScript

- **V8 Engine** — JIT compilation: Ignition (interpreter, bytecode) -> TurboFan (optimizing compiler, machine code). Hidden classes for object shape optimization. Inline caching. Deoptimization bailouts.
- **Event Loop** — Single-threaded with non-blocking I/O. Call stack, task queue (macrotasks: setTimeout, I/O), microtask queue (Promises, queueMicrotask). Microtasks drain before next macrotask. Node.js: libuv provides the event loop.
- **Closures** — Function retains reference to its lexical scope even after outer function returns. Foundation of module pattern, callbacks, React hooks. Memory consideration: closed-over variables not GC'd.
- **Prototypes** — Objects inherit from other objects via prototype chain. `__proto__` vs `.prototype`. `Object.create()`. ES6 `class` is syntactic sugar over prototypes. `instanceof` walks the chain.
- **Module Systems** — CommonJS (`require`, synchronous, Node.js default), ES Modules (`import/export`, async, tree-shakeable, native browser support). Dual package hazard. `package.json` `"type": "module"`.
- **TypeScript Type System** — Structural typing (not nominal). Generics, conditional types (`T extends U ? X : Y`), mapped types, template literal types, discriminated unions. `infer` keyword. Type narrowing via control flow analysis. Declaration merging.
- **Concurrency** — Web Workers (true threads, message passing, no shared DOM), SharedArrayBuffer + Atomics (shared memory), Worker Threads (Node.js). `Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any`.
- **Runtime Environments** — Node.js (V8, libuv, npm), Deno (V8, Rust, URL imports, permissions), Bun (JavaScriptCore, Zig, all-in-one toolkit -- package manager, bundler, test runner, runtime). Bun is significantly faster for many operations.

### 3.3 Rust

- **Ownership** — Each value has exactly one owner. When owner goes out of scope, value is dropped (RAII). Prevents double-free and use-after-free at compile time. Move semantics by default; `Copy` trait for stack types.
- **Borrowing & Lifetimes** — References borrow values: `&T` (shared, immutable, multiple allowed) or `&mut T` (exclusive, mutable, only one). Lifetimes (`'a`) tell compiler how long references are valid. Elision rules reduce annotation burden.
- **Traits** — Interfaces with default implementations. Trait bounds for generics (`fn foo<T: Display>(x: T)`). Trait objects (`dyn Trait`) for dynamic dispatch. Derive macros: `Debug`, `Clone`, `Serialize`.
- **Enums & Pattern Matching** — Algebraic data types. `Option<T>` (no null), `Result<T, E>` (no exceptions). `match` is exhaustive. Used with `?` operator for error propagation.
- **Async Rust** — `async fn` returns a `Future`. `.await` drives execution. Runtimes: tokio (most popular, work-stealing), async-std. `Pin` for self-referential types. Streams for async iteration.
- **Unsafe** — Raw pointers, `unsafe fn`, `unsafe impl`, `unsafe trait`. FFI via `extern "C"`. Used in std internals, performance-critical code. Must manually uphold invariants. `#[no_mangle]` for C ABI.
- **Macros** — Declarative (`macro_rules!`) and procedural (derive, attribute, function-like). Compile-time code generation. `serde`, `tokio::main` are proc macros. Hygiene prevents name collisions.

### 3.4 Go

- **Goroutines** — Lightweight green threads multiplexed onto OS threads (M:N scheduling). `go func()` spawns one. Stack starts at ~2KB, grows dynamically. Millions of goroutines are feasible.
- **Channels** — Typed, concurrency-safe communication. Unbuffered (synchronous handoff) vs buffered. `select` for multiplexing. "Don't communicate by sharing memory; share memory by communicating."
- **Interfaces** — Structural (implicit) -- any type implementing the method set satisfies the interface. Empty interface `interface{}` (now `any`) holds any value. Type assertions and type switches.
- **GC** — Concurrent, tri-color mark-and-sweep. Sub-millisecond pause times. GOGC controls heap growth target. No generational collection (as of Go 1.22). Stack scanning, write barriers.
- **Error Handling** — `error` interface, multiple return values. `errors.Is`, `errors.As` for wrapping/unwrapping. `defer`/`panic`/`recover` for exceptional situations (not normal control flow).

### 3.5 C / C++

- **Memory Management (C)** — `malloc`/`calloc`/`realloc`/`free`. Stack vs heap. Buffer overflows, dangling pointers, memory leaks. Valgrind, AddressSanitizer for detection.
- **Pointers & Pointer Arithmetic** — Direct memory address manipulation. Array-pointer duality. Function pointers. `void*` for generic programming. Double pointers for dynamic arrays of strings.
- **RAII (C++)** — Resource Acquisition Is Initialization. Constructors acquire, destructors release. Smart pointers: `unique_ptr` (exclusive ownership), `shared_ptr` (reference counted), `weak_ptr` (non-owning). Eliminates manual memory management.
- **Move Semantics (C++11)** — Rvalue references (`&&`), `std::move`. Transfer ownership without copying. Move constructor, move assignment operator. Enables efficient return of large objects, container operations.
- **Templates (C++)** — Compile-time polymorphism. Function templates, class templates, template specialization. SFINAE (Substitution Failure Is Not An Error). Concepts (C++20) for constrained templates. Variadic templates.
- **Undefined Behavior** — Signed integer overflow, null dereference, out-of-bounds access, data races. Compiler may assume UB never happens and optimize accordingly. `-fsanitize=undefined` for detection.
- **Modern C++ (11/14/17/20/23)** — Lambdas, `auto`, range-for, structured bindings, `std::optional`, `std::variant`, coroutines (co_await/co_yield), modules, ranges, `std::format`.

### 3.6 Language Theory

- **Type Systems** — Static vs dynamic, strong vs weak. Type inference: Hindley-Milner (ML, Haskell). Dependent types (types that depend on values -- Idris, Agda). Gradual typing (TypeScript, Python type hints). Subtyping vs parametric polymorphism.
- **Lambda Calculus** — Foundation of functional programming. Untyped: variables, abstraction, application. Beta-reduction. Church numerals, encodings. Simply typed lambda calculus. System F (polymorphism). Curry-Howard correspondence (proofs = programs).
- **Formal Semantics** — Operational (reduction rules), denotational (mathematical objects), axiomatic (Hoare logic, pre/postconditions). Used in language specification, verification, compiler correctness.
- **Parsing Theory** — Regular languages (regex, DFA), context-free (LL, LR, LALR, PEG, Earley). Parser combinators vs parser generators. Ambiguity, precedence, associativity.
- **Memory Models** — Sequential consistency, happens-before relation, acquire/release semantics. C++ memory model, Java memory model. Critical for concurrent/lock-free programming.

---

## 4. Machine Learning & AI

### 4.1 Foundations

- **Statistical Learning Theory** — Bias-variance trade-off (underfitting vs overfitting). PAC learning (Probably Approximately Correct). VC dimension (capacity of hypothesis class). Regularization as Occam's razor.
- **Loss Functions** — MSE (regression), cross-entropy (classification), hinge loss (SVM), focal loss (class imbalance), contrastive loss, triplet loss. Choice of loss encodes the task objective.
- **Optimization** — SGD, momentum, Nesterov acceleration. Adaptive methods: AdaGrad, RMSprop, Adam (and variants: AdamW, LAMB). Learning rate schedules: warmup, cosine annealing, cyclical. Gradient clipping for stability.
- **Evaluation** — Train/validation/test splits. Cross-validation (k-fold, stratified). Metrics: accuracy, precision, recall, F1, AUC-ROC, mAP. Calibration, confusion matrix. Ablation studies.

### 4.2 Classical Machine Learning

- **Linear Regression** — Minimize MSE via closed-form (normal equations) or gradient descent. Assumptions: linearity, independence, homoscedasticity, normality of residuals. Ridge (L2) and Lasso (L1) regularization. Elastic net combines both.
- **Logistic Regression** — Sigmoid activation, cross-entropy loss. Decision boundary is linear. Maximum likelihood estimation. Multinomial via softmax. Baseline classifier in many production systems.
- **Support Vector Machines** — Maximum margin classifier. Kernel trick: linear, polynomial, RBF. Soft margin (slack variables, C parameter). SMO algorithm for optimization. SVR for regression.
- **Decision Trees** — Recursive partitioning. Splitting criteria: Gini impurity, information gain (entropy), variance reduction. Pruning: pre-pruning (max depth, min samples), post-pruning (cost-complexity). Interpretable but high variance.
- **Ensemble Methods** — Bagging (parallel, reduce variance): Random Forest (feature subsampling + bagging, feature importance). Boosting (sequential, reduce bias): AdaBoost (reweight misclassified), Gradient Boosting (fit residuals), XGBoost (regularized, histogram-based), LightGBM (leaf-wise growth, GOSS), CatBoost (ordered boosting, categorical features). Stacking.
- **Naive Bayes** — Bayes' theorem with feature independence assumption. Gaussian, multinomial, Bernoulli variants. Surprisingly effective for text classification. Fast training and prediction.
- **k-Nearest Neighbors** — Instance-based learning, no training phase. Distance metrics: Euclidean, Manhattan, cosine. Curse of dimensionality. k selection, distance weighting. KD-trees, ball trees for efficient lookup.
- **Clustering** — K-means (iterative centroid update, k-means++ init), DBSCAN (density-based, arbitrary shapes, noise handling), hierarchical (agglomerative with linkage: single, complete, Ward), Gaussian Mixture Models (EM algorithm, soft clustering). Evaluation: silhouette score, adjusted Rand index.
- **Dimensionality Reduction** — PCA (eigenvectors of covariance, variance maximization), t-SNE (pairwise similarity preservation, visualization), UMAP (topological, faster than t-SNE, better global structure), autoencoders (nonlinear, learned). Feature selection: mutual information, L1 regularization.

### 4.3 Deep Learning

- **Backpropagation** — Chain rule applied through computation graph. Forward pass computes activations, backward pass computes gradients. Automatic differentiation (reverse mode) in PyTorch (`autograd`), TensorFlow (`GradientTape`). Gradient issues: vanishing (deep networks, saturating activations), exploding (RNNs).
- **Activation Functions** — ReLU (fast, sparse, dead neuron problem), Leaky ReLU / PReLU, GELU (smooth, used in Transformers), SiLU/Swish, Sigmoid (output layer for binary), Softmax (output layer for multi-class), Tanh.
- **Normalization** — Batch normalization (normalize across batch per feature, reduces internal covariate shift), Layer normalization (across features per sample, used in Transformers/RNNs -- batch-size independent), Group normalization (between LN and IN), Instance normalization (per sample per channel, style transfer).
- **Regularization** — Dropout (randomly zero activations during training, ensemble interpretation), weight decay (L2 penalty), data augmentation, early stopping, label smoothing, mixup/cutmix, stochastic depth.
- **Weight Initialization** — Xavier/Glorot (maintain variance for sigmoid/tanh), He/Kaiming (for ReLU, accounts for half-zeroed activations), orthogonal initialization (RNNs). Poor initialization leads to vanishing/exploding gradients.
- **Learning Rate Strategies** — Warmup (linearly increase from small value), cosine annealing (smooth decay), step decay, reduce on plateau, one-cycle policy, LRRT (learning rate range test).

### 4.4 Deep Learning Architectures

#### 4.4.1 Convolutional Neural Networks (CNNs)

- **Convolution Operation** — Sliding kernel over input, element-wise multiply and sum. Parameters: kernel size, stride, padding (same/valid), dilation. Parameter sharing reduces parameters vs fully connected. Receptive field grows with depth.
- **Pooling** — Max pooling (translation invariance, most common), average pooling (smoother), global average pooling (replace FC layers, reduce overfitting). Stride-2 convolutions as alternative to pooling.
- **Landmark Architectures** — LeNet (original), AlexNet (deep, ReLU, dropout, GPU), VGG (3x3 stacks), GoogLeNet/Inception (multi-scale, 1x1 convolutions), ResNet (skip connections, identity mapping, enabled very deep networks), DenseNet (dense connections), EfficientNet (compound scaling -- depth, width, resolution).
- **Residual Connections** — Skip connections that add input to output of a block. Enable gradient flow through hundreds of layers. Pre-activation vs post-activation ResNet. Foundation of nearly all modern architectures.
- **Depthwise Separable Convolutions** — Depthwise (per-channel) + pointwise (1x1 cross-channel). MobileNet. Reduces parameters and computation by ~8-9x with minimal accuracy loss.

#### 4.4.2 Recurrent Neural Networks (RNNs)

- **Vanilla RNN** — Hidden state updated at each timestep: h_t = tanh(W_h h_{t-1} + W_x x_t). Suffers from vanishing/exploding gradients over long sequences. BPTT (backpropagation through time).
- **LSTM (Long Short-Term Memory)** — Cell state (long-term memory) with three gates: forget (what to discard), input (what to store), output (what to expose). Gradient highway through cell state. Default for sequence modeling before Transformers.
- **GRU (Gated Recurrent Unit)** — Simplified LSTM with two gates: reset and update. Comparable performance with fewer parameters. Merges cell state and hidden state.
- **Bidirectional RNNs** — Process sequence in both directions, concatenate hidden states. Captures both past and future context. Used in NER, POS tagging, encoder of seq2seq.
- **Sequence-to-Sequence** — Encoder-decoder architecture. Encoder compresses input to context vector, decoder generates output. Attention mechanism (Bahdanau, Luong) allows decoder to focus on relevant encoder states.

#### 4.4.3 Transformers

- **Self-Attention** — Query, Key, Value matrices. Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V. Each position attends to all other positions. O(n^2) complexity in sequence length. Captures long-range dependencies without recurrence.
- **Multi-Head Attention** — Multiple attention heads with different learned projections. Each head can attend to different aspects (syntax, semantics, position). Outputs concatenated and projected.
- **Positional Encoding** — Sinusoidal (fixed, generalizes to unseen lengths) or learned embeddings. RoPE (Rotary Position Embedding -- encodes relative position in rotation). ALiBi (linear bias, length generalization).
- **Encoder-Decoder** — Original Transformer (Vaswani 2017, "Attention Is All You Need"). Encoder: self-attention + FFN. Decoder: masked self-attention + cross-attention + FFN. Used in machine translation, T5.
- **Decoder-Only** — GPT family. Causal (autoregressive) attention mask. Language modeling objective. Foundation of modern LLMs: GPT-4, Claude, LLaMA, Mistral.
- **Encoder-Only** — BERT family. Masked language modeling (MLM) + next sentence prediction. Bidirectional context. Fine-tuning for classification, NER, QA. DistilBERT, RoBERTa, ALBERT.
- **Efficient Transformers** — Flash Attention (IO-aware, tiling, no materialization of attention matrix), sparse attention (local + global), linear attention (kernel approximation), Longformer (sliding window + global tokens), multi-query / grouped-query attention (KV cache efficiency).
- **Vision Transformers (ViT)** — Split image into patches, treat as token sequence. Patch embedding + position embedding. Competitive with CNNs at scale. DeiT (data-efficient training), Swin Transformer (shifted windows, hierarchical).
- **FiLM (Feature-wise Linear Modulation)** — Conditioning mechanism: apply learned affine transformation (scale and shift) to feature maps based on external input. gamma * feature + beta. Used for conditioning on metadata, task-specific adaptation. *Relevant to fetal MRI processing -- conditioning segmentation models on gestational age or scan parameters.*

#### 4.4.4 Generative Models

- **GANs (Generative Adversarial Networks)** — Generator vs discriminator in minimax game. Training instability: mode collapse, vanishing gradients. Improvements: WGAN (Wasserstein distance, Lipschitz constraint), progressive growing, StyleGAN (style-based generator, disentangled latent space), conditional GAN (class-conditioned).
- **VAEs (Variational Autoencoders)** — Encoder maps to latent distribution (mean + variance), reparameterization trick enables backprop through sampling. ELBO loss = reconstruction + KL divergence. Smooth latent space, interpolation. VQ-VAE for discrete latents.
- **Diffusion Models** — Forward process adds Gaussian noise over T steps. Reverse process (learned denoising) generates samples. DDPM, DDIM (deterministic, fewer steps). Score matching / score-based models. Classifier-free guidance for conditional generation. Stable Diffusion (latent diffusion in VAE latent space). State-of-the-art image generation.
- **Flow Models** — Invertible transformations with exact likelihood computation. Normalizing flows: RealNVP, Glow. Change of variables formula. Less common than diffusion but useful for density estimation.
- **Autoregressive Models** — Generate one token/pixel at a time, conditioned on previous outputs. PixelCNN, WaveNet, GPT. Exact likelihood, high quality, but sequential generation is slow.

### 4.5 Natural Language Processing

- **Tokenization** — Word-level (vocabulary explosion, OOV), subword (BPE -- byte pair encoding, WordPiece, SentencePiece, Unigram). Byte-level BPE (GPT-2). Trade-off: vocabulary size vs sequence length.
- **Embeddings** — Word2Vec (skip-gram, CBOW), GloVe (global co-occurrence), FastText (subword). Contextual embeddings: ELMo, BERT. Sentence embeddings: Sentence-BERT, E5, text-embedding-ada-002.
- **Language Models** — Autoregressive (predict next token), masked (BERT, predict masked tokens). Perplexity as evaluation metric. Scaling laws (Chinchilla -- compute-optimal training). Emergent capabilities at scale.
- **RLHF (Reinforcement Learning from Human Feedback)** — Train reward model from human preference comparisons, then optimize language model via PPO. Aligns model behavior with human intent. RLAIF, DPO (Direct Preference Optimization) as alternatives.
- **Prompting & In-Context Learning** — Zero-shot, few-shot, chain-of-thought reasoning. System prompts, instruction following. RAG (Retrieval-Augmented Generation) -- retrieve relevant documents to ground responses. Tool use, function calling.
- **Fine-Tuning** — Full fine-tuning (update all parameters), LoRA (low-rank adaptation, update small matrices), QLoRA (quantized base + LoRA), prefix tuning, prompt tuning. PEFT (Parameter-Efficient Fine-Tuning) reduces compute and memory.

### 4.6 Computer Vision

- **Image Classification** — ImageNet benchmark. Transfer learning via pretrained backbones (ResNet, EfficientNet, ViT). Data augmentation: random crop, flip, color jitter, RandAugment, AutoAugment.
- **Object Detection** — Two-stage: Faster R-CNN (region proposal network + classifier). One-stage: YOLO (v5, v8 -- real-time), SSD. Anchor-free: FCOS, CenterNet. Evaluation: mAP (mean Average Precision), IoU thresholds.
- **Semantic Segmentation** — Per-pixel classification. FCN (fully convolutional), U-Net (encoder-decoder with skip connections, *widely used in medical imaging*), DeepLab (atrous convolution, ASPP). PSPNet (pyramid pooling).
- **Instance Segmentation** — Detect + segment individual objects. Mask R-CNN (Faster R-CNN + mask branch). Panoptic segmentation (stuff + things).
- **Image Generation** — See Generative Models (Section 4.4.4). Applications: super-resolution (ESRGAN), inpainting, style transfer (neural style, AdaIN), image-to-image translation (pix2pix, CycleGAN).
- **Self-Supervised Learning** — Pretext tasks to learn representations without labels. Contrastive: SimCLR, MoCo, BYOL. Masked image modeling: MAE, BEiT. DINO (self-distillation with no labels).
- **3D Vision** — Point clouds (PointNet, PointNet++), depth estimation (monocular, stereo), NeRF (Neural Radiance Fields -- novel view synthesis), 3D Gaussian Splatting. Relevant to volumetric medical imaging.

### 4.7 Medical Imaging & Fetal MRI

> *Especially relevant to Daniel's BCH research engineer role -- fetal brain MRI processing with PyTorch.*

- **MRI Physics** — Nuclear magnetic resonance. T1-weighted (anatomy, fat bright), T2-weighted (pathology, water bright), FLAIR (fluid-attenuated). k-space, Fourier transform for image reconstruction. Field strength (1.5T, 3T), SNR, contrast.
- **Fetal MRI Challenges** — Unpredictable fetal motion (limits scan time, causes artifacts), small brain size, rapidly changing anatomy across gestational ages, low SNR, limited training data. Slice-to-volume reconstruction (SVR) to recover 3D from motion-corrupted 2D slices.
- **Slice-to-Volume Reconstruction** — NeSVoR (neural implicit representation for SVR), SVRTK, IRTK. Register 2D slices to a consistent 3D volume despite inter-slice motion. Outlier rejection for corrupted slices.
- **Brain Segmentation** — U-Net and variants (attention U-Net, nnU-Net) for tissue segmentation: cortical plate, white matter, ventricles, cerebellum, brainstem. Multi-atlas approaches. Age-conditioned models using FiLM layers for gestational age.
- **Brain Surface Reconstruction** — Extract cortical surfaces from segmentation. Marching cubes, level sets. Surface inflation, spherical mapping. FreeSurfer (adult), custom pipelines for fetal. Measuring cortical folding (gyrification index, sulcal depth).
- **Registration & Atlases** — Align brain images to a common template. Rigid, affine, deformable (diffeomorphic -- ANTs SyN, VoxelMorph for learning-based). Spatiotemporal atlases for fetal brain development.
- **Harmonization** — Remove site/scanner effects while preserving biological variation. ComBat, deep learning harmonization. Critical for multi-site studies.
- **Data Handling** — NIfTI format (`.nii`, `.nii.gz`), nibabel for Python I/O. DICOM for raw clinical data. Header metadata: voxel dimensions, affine matrix (world coordinates), orientation (RAS/LPS). Resampling, intensity normalization.
- **Evaluation Metrics** — Dice coefficient (overlap), Hausdorff distance (surface accuracy), average symmetric surface distance. Volume measurements, cortical thickness, curvature.
- **PyTorch for Medical Imaging** — MONAI (Medical Open Network for AI): transforms, data loading, losses (Dice, Focal), architectures (U-Net, UNETR, SwinUNETR). TorchIO for 3D augmentations (elastic deformation, bias field, ghosting, spike artifacts). Mixed precision training (`torch.cuda.amp`), distributed training (`DistributedDataParallel`).

### 4.8 Reinforcement Learning

- **Markov Decision Processes** — State, action, reward, transition probability, discount factor. Bellman equation. Policy (state -> action), value function V(s), action-value Q(s,a).
- **Value-Based Methods** — Q-learning (off-policy, tabular), DQN (deep Q-network, experience replay, target network), Double DQN, Dueling DQN, Rainbow (combined improvements).
- **Policy Gradient Methods** — REINFORCE (Monte Carlo policy gradient), actor-critic (policy + value network), A2C/A3C (advantage, async), PPO (clipped surrogate objective, widely used -- RLHF, robotics). TRPO (trust region).
- **Model-Based RL** — Learn environment model, use for planning. World models, Dreamer (learned latent dynamics). MuZero (learned model + MCTS). More sample-efficient but model errors compound.
- **Multi-Agent RL** — Independent learners, centralized training with decentralized execution (QMIX, MAPPO). Communication, cooperation, competition. Applications: multi-player games, traffic, swarm robotics.

### 4.9 MLOps

- **Experiment Tracking** — Weights & Biases (W&B): log metrics, hyperparameters, artifacts, model versioning. MLflow: model registry, experiment tracking, deployment. Neptune, Comet as alternatives.
- **Model Serving** — TorchServe, TensorFlow Serving, NVIDIA Triton (multi-framework, dynamic batching). ONNX for cross-framework portability. Quantization (INT8, INT4) for inference speed. TensorRT optimization.
- **Data Versioning** — DVC (Git for data), LakeFS. Track datasets alongside code. Reproducible pipelines. Data lineage.
- **Feature Stores** — Centralized feature management. Feast, Tecton. Online (low-latency serving) and offline (batch training) stores. Feature engineering, point-in-time correctness.
- **Pipeline Orchestration** — Kubeflow, Airflow, Prefect. DAG-based workflow definition. Containerized steps, caching, retries. CI/CD for ML (CML, GitHub Actions).
- **Monitoring** — Data drift (distributional shift in inputs), model drift (performance degradation), concept drift (target relationship changes). Evidently, Whylabs. Shadow deployment, canary rollouts for model updates.

---

## 5. Tools & Frameworks

### 5.1 Frontend

- **React** — Component-based UI library. Virtual DOM diffing. Hooks: `useState`, `useEffect`, `useContext`, `useReducer`, `useMemo`, `useCallback`, `useRef`. Server Components (RSC) for zero-bundle server rendering. Concurrent features: `useTransition`, `Suspense`.
- **Next.js** — React meta-framework. App Router (RSC-first, layouts, loading/error states, parallel routes). Rendering: SSR, SSG, ISR, client-side. API routes / Server Actions for mutations. Middleware for auth/routing. Image optimization, font optimization. Turbopack (Rust bundler). *Used in Sidepocket webapp and nextblog.*
- **State Management** — Zustand (minimal, hook-based, no providers -- *used in Sidepocket*), Redux Toolkit (centralized, devtools, RTK Query), Jotai (atomic), Recoil (graph-based). Server state: React Query / TanStack Query, SWR.
- **Styling** — Tailwind CSS (utility-first, JIT, design system constraints), CSS Modules (scoped), styled-components (CSS-in-JS, runtime), Vanilla Extract (CSS-in-TS, zero runtime). Radix UI + Shadcn/ui (accessible primitives with copy-paste components -- *used in nextblog*).
- **Build Tools** — Vite (ESM-based dev server, Rollup production build, fast HMR), Webpack (mature, extensive plugin ecosystem), Turbopack (Rust, incremental, Next.js), esbuild (Go, extremely fast bundling). Tree-shaking, code splitting, lazy loading.
- **Testing (Frontend)** — Jest / Vitest (unit/integration), React Testing Library (user-centric, no implementation details), Cypress (E2E, real browser -- *used in Sidepocket*), Playwright (cross-browser E2E). MSW (Mock Service Worker) for API mocking.

### 5.2 Backend

- **Flask** — Python micro-framework. WSGI, Werkzeug routing, Jinja2 templating. Blueprints for modular structure. Extensions: Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended. *Used in Sidepocket backend (sp-app).*
- **FastAPI** — Modern Python framework. ASGI, async-first, Pydantic models for validation/serialization, automatic OpenAPI docs. Dependency injection. Uvicorn/Gunicorn deployment. Higher performance than Flask for I/O-bound.
- **GraphQL** — Query language for APIs. Schema-first vs code-first. Types, queries, mutations, subscriptions. Resolvers, dataloaders (N+1 problem), batching. Graphene (Python -- *used in sp-app*), Apollo (JS). Introspection, fragments, variables.
- **REST Design** — Resource-oriented URLs, HTTP methods (GET, POST, PUT, PATCH, DELETE), status codes, HATEOAS. Versioning (URL, header). Pagination (cursor, offset). Rate limiting. OpenAPI/Swagger specification.
- **tRPC** — End-to-end type-safe APIs without code generation. TypeScript client + server share types. Router, procedures, middleware. React Query integration. *Used in Sidepocket webapp.*
- **Express / Fastify** — Node.js HTTP frameworks. Express: middleware pipeline, wide ecosystem. Fastify: schema-based validation, faster, plugin system.

### 5.3 Databases

- **PostgreSQL** — Advanced relational database. MVCC for concurrency. JSON/JSONB support, full-text search, CTEs, window functions, materialized views, partitioning. Extensions: PostGIS (spatial), pg_trgm (fuzzy matching), TimescaleDB. EXPLAIN ANALYZE for query tuning. *Used in sp-app and nextblog.*
- **Redis** — In-memory data structure store. Strings, lists, sets, sorted sets, hashes, streams, HyperLogLog. Pub/sub, Lua scripting. Persistence: RDB snapshots, AOF log. Cluster mode (sharding), Sentinel (HA). Use cases: caching, session store, rate limiting, job queues, leaderboards. *Used in sp-app for JWT token blacklist.*
- **MongoDB** — Document database (BSON). Flexible schema, embedded documents, arrays. Aggregation pipeline. Indexes: compound, multikey, text, geospatial. Replica sets, sharding. Change streams.
- **Prisma** — TypeScript ORM. Schema-first (`schema.prisma`), auto-generated type-safe client, migrations. Relations, transactions, raw queries. *Used in nextblog.*
- **SQLAlchemy** — Python SQL toolkit and ORM. Core (SQL expression language) and ORM (declarative mapping). Unit of work pattern, identity map. Alembic for migrations. Async support via `asyncpg`. *Used in sp-app (`app_domain/models.py`).*

### 5.4 DevOps

- **Docker** — Container runtime. Images (layered filesystem, Dockerfile), containers (isolated processes). Multi-stage builds (reduce image size). Docker Compose for multi-container applications. Volume mounts, networking. Buildkit, layer caching.
- **Kubernetes (K8s)** — Container orchestration. Pods, Deployments, Services, Ingress, ConfigMaps, Secrets. Horizontal Pod Autoscaler. Helm (package manager), Kustomize (overlays). Namespaces, RBAC. Health probes (liveness, readiness, startup).
- **CI/CD** — GitHub Actions (YAML workflows, marketplace actions, matrix builds -- *used in Sidepocket*), GitLab CI, Jenkins. Pipeline stages: lint, test, build, deploy. Artifact caching, secrets management. Branch protection, required status checks.
- **Terraform** — Infrastructure as Code. HCL declarative language. State management (remote backends: S3 + DynamoDB lock). Plan -> Apply cycle. Modules for reuse. Import existing resources. Drift detection.
- **Monitoring & Logging** — Prometheus (metrics, PromQL, alerting), Grafana (dashboards, visualization), CloudWatch (AWS-native, logs, metrics, alarms). Structured logging (JSON), log aggregation (ELK, Loki). PagerDuty for on-call.

### 5.5 Cloud (AWS)

- **EC2** — Virtual machines. Instance types (compute, memory, GPU optimized). AMIs, launch templates. Auto Scaling Groups. Spot instances for cost savings. Security groups (stateful firewall). *Used in BCH research (GPU instances for training).*
- **ECS (Elastic Container Service)** — Container orchestration on AWS. Tasks, services, task definitions. Fargate (serverless) vs EC2 launch type. Service discovery, load balancing. *Used for Sidepocket deployment.*
- **S3** — Object storage. Buckets, keys, versioning. Storage classes (Standard, IA, Glacier). Pre-signed URLs for temporary access. Event notifications (Lambda triggers). Lifecycle policies. *Sidepocket Redis -> S3 migration context.*
- **RDS** — Managed relational databases. PostgreSQL, MySQL, Aurora. Multi-AZ for HA, read replicas. Automated backups, snapshots. Parameter groups, performance insights.
- **Lambda** — Serverless compute. Event-driven (API Gateway, S3, SQS, EventBridge triggers). Cold starts, provisioned concurrency. Layers for shared dependencies. 15-minute max execution.
- **CloudWatch** — Monitoring: metrics, logs, alarms, dashboards. Log Insights (query language). Custom metrics. Anomaly detection.
- **EFS** — Managed NFS. Shared filesystem for ECS tasks, EC2 instances. Throughput modes, lifecycle management.
- **IAM** — Identity and Access Management. Users, groups, roles, policies (JSON). Least privilege principle. Instance profiles for EC2. Cross-account access. STS for temporary credentials.
- **VPC** — Virtual Private Cloud. Subnets (public, private), route tables, internet gateway, NAT gateway. Security groups (instance-level), NACLs (subnet-level). VPC peering, Transit Gateway. *Relevant to WireGuard VPN setup.*

---

## 6. Security

### 6.1 Cryptography

- **Symmetric Encryption** — Same key for encrypt/decrypt. AES (128/256 bit, block cipher, modes: CBC, CTR, GCM -- authenticated). ChaCha20-Poly1305 (stream cipher, fast on mobile/ARM). Key management is the hard part.
- **Asymmetric Encryption** — Key pair (public encrypts, private decrypts). RSA (factoring hardness, 2048+ bits), ECDSA/Ed25519 (elliptic curve, smaller keys, faster). Key exchange: Diffie-Hellman, ECDHE.
- **Hash Functions** — Deterministic, fixed-size output, one-way, collision-resistant. SHA-256, SHA-3, BLAKE3. NOT for passwords (too fast). Use case: integrity verification, digital signatures, Merkle trees.
- **KDFs (Key Derivation Functions)** — Password hashing: bcrypt (salt, cost factor), Argon2 (memory-hard, resistant to GPU attacks, recommended), scrypt (memory-hard). HKDF for deriving subkeys from master key.
- **Digital Signatures** — Sign with private key, verify with public key. RSA-PSS, ECDSA, Ed25519. Non-repudiation. Used in JWT, code signing, TLS certificates, blockchain transactions.
- **Post-Quantum Cryptography** — Lattice-based (CRYSTALS-Kyber for KEM, CRYSTALS-Dilithium for signatures), hash-based (SPHINCS+). NIST standardization (2024). Migration planning for quantum-vulnerable systems.

### 6.2 Web Security

- **OWASP Top 10** — Injection, broken authentication, sensitive data exposure, XXE, broken access control, security misconfiguration, XSS, insecure deserialization, vulnerable components, insufficient logging.
- **XSS (Cross-Site Scripting)** — Inject malicious scripts into web pages. Stored (persistent), reflected (URL-based), DOM-based. Prevention: output encoding, Content-Security-Policy headers, sanitization libraries (DOMPurify).
- **CSRF (Cross-Site Request Forgery)** — Forged requests from authenticated users. Prevention: CSRF tokens (synchronizer pattern), SameSite cookie attribute, origin/referer header validation.
- **SQL Injection** — Inject SQL via user input. Prevention: parameterized queries (never string concatenation), ORM, input validation. Second-order injection through stored data.
- **JWT Security** — Signing algorithms: HS256 (symmetric, shared secret), RS256 (asymmetric, recommended). Common vulnerabilities: `alg: none` attack, weak secrets, missing expiration, storing in localStorage (XSS-vulnerable). Best practice: short-lived access tokens + refresh tokens, httpOnly cookies. *Relevant to sp-app JWT implementation.*
- **CORS** — Cross-Origin Resource Sharing. Preflight requests (OPTIONS). Headers: `Access-Control-Allow-Origin`, `-Methods`, `-Headers`, `-Credentials`. Misconfigured CORS can expose APIs. Restrict to known origins in production.
- **CSP (Content Security Policy)** — HTTP header restricting resource loading sources. Prevents XSS by controlling script/style/image origins. `script-src 'self'`, nonce-based for inline scripts.

### 6.3 Network Security

- **TLS** — See Networking section 2.6. Certificate lifecycle: generation (CSR), issuance (CA/Let's Encrypt), deployment, renewal, revocation (CRL, OCSP). Certificate transparency logs.
- **VPN** — WireGuard (modern, simple, fast -- UDP, Noise protocol framework, ~4000 lines of code), OpenVPN (SSL-based, more configurable), IPsec (complex, enterprise). *WireGuard used for BCH access.*
- **Firewalls** — Packet filtering (iptables/nftables), stateful inspection, application layer (WAF). UFW (iptables frontend), firewalld. AWS Security Groups, NACLs.
- **IDS/IPS** — Intrusion Detection/Prevention Systems. Signature-based (Snort, Suricata), anomaly-based. Network-based (NIDS) vs host-based (HIDS, OSSEC).

### 6.4 Authentication & Authorization

- **OAuth 2.0** — Authorization framework. Grant types: authorization code (+ PKCE for public clients), client credentials (service-to-service), refresh token. Access token scopes. Token introspection.
- **OIDC (OpenID Connect)** — Identity layer on OAuth 2.0. ID token (JWT with user claims). UserInfo endpoint. Discovery document. Standard claims: sub, email, name.
- **SAML** — XML-based SSO for enterprise. Identity Provider (IdP) <-> Service Provider (SP). Assertions, metadata. Being replaced by OIDC in modern applications.
- **Passkeys / WebAuthn** — FIDO2 standard. Public key cryptography, no shared secrets. Biometric or PIN authentication. Phishing-resistant. Platform authenticators (Touch ID, Windows Hello) and roaming (YubiKey).
- **RBAC / ABAC** — Role-Based Access Control (user -> role -> permissions). Attribute-Based Access Control (policies based on user/resource/environment attributes). RBAC simpler to manage, ABAC more granular.

---

## 7. Theoretical Computer Science

### 7.1 Automata Theory

- **DFA (Deterministic Finite Automaton)** — Finite states, deterministic transitions on input symbols. Recognizes regular languages. Minimization algorithm (Hopcroft). Equivalent to regular expressions.
- **NFA (Nondeterministic Finite Automaton)** — Multiple possible transitions per input (including epsilon transitions). Same expressive power as DFA. Subset construction converts NFA to DFA (exponential state blowup possible).
- **Regular Expressions** — Algebraic notation for regular languages. Operations: union, concatenation, Kleene star. Pumping lemma proves languages non-regular. Used in lexers, text processing, input validation.
- **Context-Free Grammars** — Production rules with single non-terminal on left side. Generates context-free languages (programming languages, XML, natural language syntax). Chomsky normal form, Greibach normal form.
- **Pushdown Automata** — Finite automaton + stack. Recognizes context-free languages. Deterministic PDA recognizes a strict subset (DPDA = LR(1) parsable languages). Non-deterministic PDA = full CFL.
- **Turing Machines** — Infinite tape, read/write head, state transitions. Defines computability. Church-Turing thesis: any effectively computable function is Turing-computable. Multi-tape, non-deterministic variants are equivalent in power.
- **Chomsky Hierarchy** — Type 0 (recursively enumerable, Turing machine), Type 1 (context-sensitive, linear bounded automaton), Type 2 (context-free, PDA), Type 3 (regular, DFA/NFA). Each strictly contains the next.

### 7.2 Computability

- **Halting Problem** — No algorithm can determine whether an arbitrary program halts on given input. Proved by diagonalization (Turing 1936). The foundational undecidability result.
- **Rice's Theorem** — All non-trivial semantic properties of programs are undecidable. "Does this program output 42?" is undecidable. Only trivial properties (always true or always false) are decidable.
- **Recursive vs RE** — Recursive (decidable): membership can be decided by a TM that always halts. Recursively enumerable (semi-decidable): TM halts on accepting inputs, may loop on rejecting. Complement of RE is co-RE. Halting problem is RE but not recursive.
- **Reductions** — Many-one (mapping) reductions: if A reduces to B and B is decidable, so is A. Used to prove undecidability by reducing from known undecidable problems. Turing reductions (oracle access) are more general.
- **Kolmogorov Complexity** — Shortest program producing a string. Incompressible strings exist (most strings). Not computable. Relates to information content, randomness. Berry paradox connection.

### 7.3 Quantum Computing

- **Qubits** — Quantum bit: superposition of |0> and |1> states (alpha|0> + beta|1>, |alpha|^2 + |beta|^2 = 1). Measurement collapses to 0 or 1. n qubits represent 2^n amplitudes simultaneously. Bloch sphere visualization.
- **Quantum Gates** — Unitary operations. Single-qubit: Hadamard (superposition), Pauli-X/Y/Z (rotations), phase (S, T). Multi-qubit: CNOT (entanglement), Toffoli (universal for classical). Gate universality: any unitary from finite gate set.
- **Shor's Algorithm** — Factor integers in polynomial time (threatens RSA). Quantum Fourier transform to find periodicity. Exponential speedup over best known classical algorithms.
- **Grover's Algorithm** — Search unsorted database of N items in O(sqrt(N)). Quadratic speedup. Amplitude amplification technique. Useful for NP-hard search problems.
- **Quantum Error Correction** — Qubits are fragile (decoherence). Shor code, Steane code, surface codes. Logical qubits from physical qubits. Fault-tolerant computation threshold. Major engineering challenge.
- **Quantum Entanglement** — Non-classical correlations. Bell states, EPR pairs. Violation of Bell inequalities. Enables teleportation, superdense coding. No faster-than-light communication.
- **Quantum Supremacy/Advantage** — Demonstrate computation infeasible on classical hardware. Google Sycamore (2019, random circuit sampling). Debated: classical simulation improvements narrow the gap.

### 7.4 Formal Verification

- **Model Checking** — Exhaustive state-space exploration. Temporal logics: LTL (linear time), CTL (branching time). Tools: SPIN (Promela), NuSMV, TLA+ (Lamport -- distributed systems). State explosion problem; symbolic model checking with BDDs.
- **Theorem Provers** — Interactive: Coq (Calculus of Constructions, Curry-Howard, extracted programs), Lean 4 (Mathlib, active community, metaprogramming), Isabelle/HOL. Automated: Z3 (SMT solver), CVC5.
- **SAT/SMT Solvers** — SAT: boolean satisfiability (Cook-Levin NP-complete). DPLL, CDCL algorithms. SMT extends SAT with theories (integers, arrays, bit vectors). Used in verification, program analysis, constraint solving. Z3 (Microsoft), CVC5.
- **Hoare Logic** — {P} C {Q} -- if precondition P holds before command C, postcondition Q holds after. Loop invariants for reasoning about loops. Weakest precondition calculus. Foundation of program correctness proofs.
- **Abstract Interpretation** — Approximate program semantics to extract properties. Over-approximation ensures soundness. Domains: intervals, polyhedra, octagons. Used in static analyzers (Astree, Infer).

---

## 8. Software Engineering

### 8.1 Design Patterns

- **Creational** — Factory Method (defer instantiation to subclasses), Abstract Factory (families of objects), Builder (step-by-step complex objects), Singleton (one instance -- often an antipattern), Prototype (cloning).
- **Structural** — Adapter (interface conversion), Bridge (decouple abstraction from implementation), Composite (tree structures), Decorator (add behavior dynamically), Facade (simplified interface), Proxy (access control, lazy loading).
- **Behavioral** — Observer (pub-sub, event handling), Strategy (interchangeable algorithms), Command (encapsulate requests), Iterator (sequential access), State (behavior changes with state), Template Method (algorithm skeleton), Mediator (centralized communication).
- **Concurrency** — Producer-consumer, thread pool, read-write lock, monitor, active object, reactor (event-driven I/O). Actor model (Erlang, Akka -- message passing, no shared state).
- **Architectural** — MVC, MVVM, Clean Architecture (dependency rule -- inner layers don't know outer), Hexagonal (ports & adapters), Event-Driven Architecture, Pipes and Filters.

### 8.2 Testing

- **Unit Testing** — Test individual functions/methods in isolation. Mocking dependencies. AAA pattern (Arrange, Act, Assert). pytest (Python -- fixtures, parametrize, markers -- *used in sp-app*), Jest/Vitest (JS/TS). Code coverage: line, branch, path.
- **Integration Testing** — Test interactions between components. Database integration (test containers, in-memory DB), API testing, service interactions. Slower than unit tests, higher confidence. *sp-app uses `pytest test/int/`.*
- **End-to-End (E2E) Testing** — Test complete user flows through the system. Browser automation: Cypress (*used in Sidepocket webapp*), Playwright, Selenium. Flakiness mitigation: stable selectors, retry logic, deterministic data.
- **Property-Based Testing** — Generate random inputs, verify properties hold. Hypothesis (Python), fast-check (JS). Finds edge cases humans miss. Shrinking: minimize failing inputs.
- **Test Strategies** — Testing pyramid (many unit, fewer integration, fewest E2E). Testing trophy (static > unit > integration > E2E). TDD (red-green-refactor). BDD (given-when-then).

### 8.3 Version Control

- **Git Internals** — Content-addressable store. Objects: blob (file content), tree (directory), commit (snapshot + parent + message), tag. SHA-1 hashing. Packfiles for compression. Refs: branches (movable pointers), HEAD.
- **Branching Strategies** — Git Flow (develop/feature/release/hotfix), GitHub Flow (main + feature branches, PRs), trunk-based development (short-lived branches, feature flags). Rebase vs merge (linear history vs explicit merge commits).
- **Advanced Operations** — Interactive rebase (squash, reorder, edit), cherry-pick, bisect (binary search for bug-introducing commit), reflog (recovery), stash, worktrees (multiple working directories).
- **Code Review** — Review for correctness, readability, performance, security, test coverage. PR descriptions: what, why, how to test. Small PRs merge faster. Conventional comments (suggestion, question, nitpick).

### 8.4 Development Practices

- **Agile** — Scrum (sprints, standup, retro, backlog refinement), Kanban (WIP limits, flow optimization). Story points, velocity. Sprint planning, estimation (planning poker, T-shirt sizing).
- **Documentation** — ADRs (Architecture Decision Records: context, decision, consequences), API documentation (OpenAPI/Swagger), runbooks, onboarding guides. Docs-as-code (version controlled, reviewed).
- **Code Quality** — Linters (ESLint, Ruff, Pylint), formatters (Prettier, Black), type checkers (mypy, pyright, tsc). Pre-commit hooks. Code complexity metrics (cyclomatic, cognitive). Technical debt tracking.
- **Semantic Versioning** — MAJOR.MINOR.PATCH. Breaking changes increment major, new features increment minor, bug fixes increment patch. Pre-release tags (-alpha, -beta, -rc).

---

## 9. Operating Systems

### 9.1 Processes & Threads

- **Process Model** — Program in execution. Address space (text, data, heap, stack), PCB (process control block). Process states: new, ready, running, waiting, terminated. Context switching (save/restore registers, TLB flush).
- **Process Creation** — `fork()` (copy parent, COW optimization), `exec()` (replace process image), `wait()`. Orphan processes (adopted by init/systemd), zombie processes (terminated but not waited on).
- **Threads** — Lightweight processes sharing address space. User-level (green threads, goroutines) vs kernel-level (pthreads). Benefits: shared memory, fast context switch. Challenges: data races, deadlocks.
- **Scheduling** — Preemptive vs cooperative. Algorithms: FIFO, Round Robin (time quantum), priority (starvation risk, aging), multi-level feedback queue, CFS (Completely Fair Scheduler -- Linux, red-black tree, virtual runtime), EEVDF (replacing CFS in newer kernels).
- **IPC (Inter-Process Communication)** — Pipes (unidirectional), named pipes (FIFO), message queues, shared memory (fastest, needs synchronization), sockets (network/Unix domain), signals. D-Bus for desktop IPC.

### 9.2 Concurrency & Synchronization

- **Race Conditions** — Outcome depends on non-deterministic ordering of operations. Critical section: code accessing shared resources. Mutual exclusion required for correctness.
- **Locks** — Mutex (mutual exclusion, binary), spinlock (busy-wait, short critical sections), read-write lock (multiple readers OR one writer). Lock ordering to prevent deadlock.
- **Semaphores** — Counting semaphore (bounded resource access), binary semaphore (mutex-like). `wait()` (P) decrements, `signal()` (V) increments. Producer-consumer, readers-writers, dining philosophers.
- **Deadlock** — Four conditions: mutual exclusion, hold and wait, no preemption, circular wait. Prevention: break any condition. Detection: resource allocation graph, cycle detection. Recovery: kill process, preempt resource.
- **Lock-Free Programming** — CAS (Compare-And-Swap) atomic operations. ABA problem (solved by hazard pointers, epoch-based reclamation). Lock-free queues (Michael-Scott), stacks (Treiber). Higher throughput under contention but complex to implement correctly.

### 9.3 Memory Management

- **Virtual Memory** — Abstraction giving each process its own address space. Page tables (multi-level), TLB (Translation Lookaside Buffer -- caches page table entries). Demand paging: load pages only when accessed.
- **Page Replacement** — When physical memory full, evict a page. Algorithms: FIFO, LRU (approximated by clock algorithm), LFU. Thrashing: too many page faults, system spends all time swapping. Working set model.
- **Memory Allocation** — `malloc` internals: free list, buddy system, slab allocator (Linux kernel -- object caching). Memory fragmentation: internal (wasted within allocation) vs external (free memory scattered). jemalloc, tcmalloc for performance.
- **Segmentation** — Divide address space into logical segments (code, data, stack, heap). Each with base + limit. Segmentation fault: access outside segment bounds. x86 has segment registers (mostly unused in 64-bit).
- **Memory-Mapped Files** — `mmap()` maps file into address space. Lazy loading, shared mapping (IPC), private mapping (COW). Used for dynamic libraries, database buffer pools.
- **Swap** — Extend virtual memory to disk. Linux: swap partition or swapfile. `swappiness` kernel parameter. Swap-on-NVMe has lower latency. *System uses 8GB swapfile at `/swapfile`.*

### 9.4 File Systems

- **File System Concepts** — Files, directories (as files), inodes (metadata: size, permissions, timestamps, block pointers), superblock. Hard links (multiple names for same inode) vs symbolic links (path reference).
- **Linux File Systems** — ext4 (journaling, extents, delayed allocation, most common), XFS (large files, parallel I/O), Btrfs (COW, snapshots, checksums, RAID), ZFS (pooled storage, deduplication, compression, not mainline). tmpfs (RAM-backed), procfs/sysfs (kernel interfaces).
- **Journaling** — Write-ahead log for metadata (and optionally data) operations. Crash recovery without full fsck. Modes: journal (safest, slowest), ordered (default ext4, metadata journaled, data written first), writeback (fastest, risk of stale data).
- **VFS (Virtual File System)** — Abstraction layer allowing uniform interface for different file systems. System calls (`open`, `read`, `write`, `close`) go through VFS. Everything-is-a-file philosophy.
- **I/O Schedulers** — mq-deadline (default for many devices), BFQ (optimized for interactive workloads), kyber (low-latency), none (NVMe -- hardware handles scheduling). Block layer, bio requests.

### 9.5 Virtualization & Containers

- **Hardware Virtualization** — Hypervisors: Type 1 (bare-metal -- KVM, Xen, VMware ESXi), Type 2 (hosted -- VirtualBox, VMware Workstation). VT-x/AMD-V hardware extensions. Memory: EPT/NPT (nested page tables). I/O: virtio, SR-IOV.
- **Containers** — OS-level virtualization. Linux primitives: namespaces (PID, network, mount, user -- isolation), cgroups (resource limits -- CPU, memory, I/O). OCI (Open Container Initiative) standard. Lower overhead than VMs, shared kernel.
- **Systemd** — Linux init system and service manager. Units (service, timer, mount, socket). `systemctl` management. Journal logging (`journalctl`). Targets (multi-user, graphical). Socket activation, cgroup integration. *Used on this Arch system.*

### 9.6 Linux Internals

- **Kernel Architecture** — Monolithic with loadable modules (`lsmod`, `modprobe`). System call interface (syscall table, `syscall` instruction). Kernel space vs user space. Preemptible kernel (PREEMPT).
- **Boot Process** — Firmware (UEFI/BIOS) -> bootloader (GRUB, systemd-boot) -> kernel (decompress, init hardware) -> initramfs (early userspace, mount root) -> init (systemd PID 1) -> default target.
- **Package Management (Arch)** — pacman (`-S` install, `-R` remove, `-Syu` full upgrade, `-Qi` info, `-Ql` files). AUR helpers: yay, paru. `paccache` for cache management. makepkg for building AUR packages. *59 AUR packages on this system.*
- **Networking Stack** — Netfilter (iptables/nftables), network namespaces, bridge, veth pairs. `ip` command suite. NetworkManager vs systemd-networkd. WireGuard kernel module. Socket programming: `socket()`, `bind()`, `listen()`, `accept()`, `connect()`.

---

## 10. Compilers

### 10.1 Lexical Analysis (Lexing)

- **Tokenization** — Convert character stream to token stream. Tokens: identifiers, keywords, literals, operators, delimiters. Regular expressions define token patterns. Maximal munch principle (longest match wins).
- **Lexer Generators** — Flex/Lex (C), ANTLR (multi-language). Finite automaton drives token recognition. Hand-written lexers for performance and better error messages (Go, Rust, Clang).

### 10.2 Parsing

- **Top-Down Parsing** — Recursive descent (hand-written, easy to understand, good error messages). LL(k) (left-to-right, leftmost derivation, k lookahead). Predictive parsing with FIRST/FOLLOW sets. Parser combinators (nom in Rust, parsec in Haskell).
- **Bottom-Up Parsing** — Shift-reduce. LR(0), SLR, LALR(1) (yacc/bison), LR(1). Handles more grammars than LL. Parser generators: bison, tree-sitter (incremental, used in editors).
- **PEG (Parsing Expression Grammars)** — Ordered choice (no ambiguity), memoized (packrat parsing, O(n) guaranteed). Used in modern tools where CFG ambiguity is problematic.
- **Error Recovery** — Panic mode (skip to synchronization token), phrase-level (insert/delete tokens), error productions. Good error messages are a major usability concern (Rust, Elm are exemplars).

### 10.3 Abstract Syntax Trees (ASTs)

- **AST Design** — Tree representation of program structure stripping syntactic sugar. Nodes for expressions, statements, declarations. Visitor pattern for traversal (accept/visit). Distinguished from CST (Concrete Syntax Tree, includes all tokens).
- **AST Transformations** — Desugaring (reduce language to core constructs), macro expansion, constant folding, dead code elimination at AST level. Tree rewriting.

### 10.4 Semantic Analysis

- **Type Checking** — Verify type correctness. Static (compile-time) vs dynamic (runtime). Type inference (Hindley-Milner: Algorithm W, constraint-based). Bidirectional type checking. Type errors with good diagnostics.
- **Symbol Tables** — Map identifiers to their declarations. Scope management: lexical (static) scoping, dynamic scoping. Nested scopes via stack of symbol tables or persistent data structures.
- **Name Resolution** — Resolve identifiers to declarations. Overloading (same name, different signatures), shadowing (inner scope hides outer). Module systems, qualified names, imports.

### 10.5 Intermediate Representations

- **Three-Address Code** — Statements with at most one operator: `t1 = a + b`. Quadruples (op, arg1, arg2, result), triples. Easy to optimize and translate.
- **SSA (Static Single Assignment)** — Each variable assigned exactly once. Phi functions at join points. Simplifies optimization (constant propagation, dead code elimination). Used in LLVM IR, GCC's GIMPLE.
- **Control Flow Graphs** — Basic blocks (straight-line code) connected by edges (branches). Dominance, dominator trees, natural loops. Foundation for dataflow analysis and optimization.

### 10.6 Optimization

- **Local Optimizations** — Within a basic block. Constant folding (`3+4` -> `7`), algebraic simplification (`x*1` -> `x`), dead store elimination, copy propagation.
- **Global Optimizations** — Across basic blocks within a function. Common subexpression elimination (CSE), loop-invariant code motion (hoist computations out of loops), dead code elimination, strength reduction (`x*2` -> `x<<1`).
- **Interprocedural** — Across function boundaries. Inlining (replace call with function body), tail call elimination, escape analysis, devirtualization.
- **Loop Optimizations** — Unrolling (reduce branch overhead), vectorization (SIMD), tiling/blocking (cache locality), loop fusion/fission, polyhedral analysis (complex loop nest transformations).
- **Register Allocation** — Map variables to registers (limited resource). Graph coloring (interference graph). Linear scan (simpler, used in JITs). Spilling to stack when registers exhausted.

### 10.7 Code Generation

- **Instruction Selection** — Map IR to target instructions. Tree pattern matching, tiling algorithms. LLVM uses DAG-based selection.
- **Target Architectures** — x86-64 (CISC, complex addressing, SSE/AVX SIMD), ARM/AArch64 (RISC, energy-efficient, NEON SIMD), RISC-V (open ISA, extensible). Calling conventions, ABI.
- **LLVM** — Compiler infrastructure. LLVM IR (typed, SSA-form), optimization passes (modular, composable). Backends for many architectures. Used by Clang (C/C++), Rust, Swift, Julia. JIT compilation support (ORC).
- **JIT Compilation** — Compile at runtime with runtime information. Method-based (compile hot methods), trace-based (compile hot paths). Speculative optimization, deoptimization. V8 TurboFan, JVM HotSpot C2.

---

## 11. Computer Networks

### 11.1 OSI Model

- **Physical (L1)** — Bits over physical medium. Ethernet (copper, fiber), Wi-Fi (802.11). Encoding, modulation, signaling. Bandwidth, latency, jitter.
- **Data Link (L2)** — Framing, MAC addressing, error detection (CRC). Ethernet frames, ARP. Switches (MAC address table, forwarding). VLANs (802.1Q tagging). Spanning Tree Protocol (loop prevention).
- **Network (L3)** — IP addressing (IPv4: 32-bit, subnet masks, CIDR; IPv6: 128-bit, SLAAC). Routing: static, dynamic (OSPF -- link state, BGP -- path vector, inter-AS). NAT (Network Address Translation), ICMP (ping, traceroute).
- **Transport (L4)** — TCP (reliable, ordered, flow control -- sliding window, congestion control -- slow start, AIMD, CUBIC, BBR), UDP (unreliable, connectionless, low overhead). Ports, multiplexing. QUIC (UDP-based, multiplexed, 0-RTT).
- **Session/Presentation (L5-6)** — Largely absorbed into application protocols. TLS operates here conceptually. Data encoding/serialization.
- **Application (L7)** — HTTP, SMTP, FTP, DNS, SSH. Application-level protocols define message formats, semantics, procedures.

### 11.2 TCP/IP Deep Dive

- **Three-Way Handshake** — SYN -> SYN-ACK -> ACK. Sequence number synchronization. Connection state: ESTABLISHED, FIN_WAIT, TIME_WAIT (2MSL, prevents stale segments). SO_REUSEADDR, SO_REUSEPORT.
- **Flow Control** — Receiver window (rwnd) advertised by receiver. Prevents sender from overwhelming receiver's buffer. Sliding window protocol.
- **Congestion Control** — Avoid network overload. Congestion window (cwnd). Slow start (exponential growth), congestion avoidance (linear), fast retransmit/recovery (3 duplicate ACKs). CUBIC (default Linux), BBR (bandwidth-based, Google).
- **TCP Optimizations** — Nagle's algorithm (coalesce small segments), delayed ACK, TCP Fast Open (data in SYN), window scaling (>64KB windows), selective acknowledgment (SACK).

### 11.3 HTTP

- **HTTP/1.1** — Text-based, persistent connections (keep-alive), pipelining (HOL blocking at HTTP level). Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD. Status codes: 2xx success, 3xx redirect, 4xx client error, 5xx server error.
- **HTTP/2** — Binary framing layer. Multiplexing (multiple streams on one connection, eliminates HOL at HTTP level). Header compression (HPACK). Server push. Priority/weights.
- **HTTP/3** — QUIC transport (UDP-based). Eliminates TCP HOL blocking (independent streams). 0-RTT connection establishment. Connection migration (change IP without reconnection). QPACK header compression.
- **HTTPS** — HTTP over TLS. Certificate validation, cipher suite negotiation. HSTS (force HTTPS). Certificate pinning (backup). Let's Encrypt (free, automated CA).

### 11.4 DNS

- **Resolution Process** — Client -> recursive resolver (ISP/8.8.8.8) -> root server -> TLD server -> authoritative server. Caching at every level (TTL-based). Iterative vs recursive queries.
- **Record Types** — A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), NS (nameserver), TXT (arbitrary text, SPF/DKIM/DMARC), SRV (service discovery), CAA (certificate authority authorization).
- **DNS Security** — DNSSEC (signing, chain of trust from root). DNS-over-HTTPS (DoH), DNS-over-TLS (DoT) for privacy. DNS rebinding attacks, DNS poisoning.
- **DNS in Production** — Route 53 (AWS), Cloudflare DNS. GeoDNS for latency-based routing. Low TTL for failover (trade-off: more queries). Internal DNS for service discovery.

### 11.5 Sockets

- **Socket API** — `socket()` (create), `bind()` (assign address), `listen()` (passive open), `accept()` (accept connection), `connect()` (active open), `send()`/`recv()`, `close()`. Blocking vs non-blocking.
- **I/O Multiplexing** — Handle many connections efficiently. `select()` (O(n), FD limit), `poll()` (no FD limit, still O(n)), `epoll` (Linux, O(1) for ready events, edge/level triggered), `kqueue` (BSD/macOS). Foundation of event loops (libuv, tokio, asyncio).
- **Unix Domain Sockets** — IPC on same host. Faster than TCP loopback (no network stack overhead). `AF_UNIX`. Used by Docker daemon, PostgreSQL local connections, systemd socket activation.

### 11.6 Routing

- **Interior Gateway Protocols** — OSPF (link-state, Dijkstra, areas, fast convergence), IS-IS (similar to OSPF, used in large ISPs), RIP (distance-vector, hop count, slow convergence -- mostly obsolete).
- **Exterior Gateway Protocol** — BGP (Border Gateway Protocol). Path-vector, AS path. Policy-based routing. Internet backbone. Route leaks and hijacking risks. RPKI for route origin validation.
- **Software-Defined Networking** — Separate control plane from data plane. OpenFlow protocol. Programmable switches. Network functions virtualization (NFV). Cloud networking overlays (VXLAN, GRE).

---

## Cross-Cutting Concepts

### Performance Engineering

- **Profiling** — CPU profiling (sampling: perf, py-spy; instrumentation: cProfile), memory profiling (tracemalloc, Valgrind Massif), I/O profiling. Flame graphs for visualization. Profile before optimizing.
- **Caching** — CPU cache hierarchy (L1/L2/L3, cache lines, false sharing), application caching (memoization, Redis), HTTP caching (ETag, Cache-Control). Cache invalidation is one of the hardest problems.
- **Benchmarking** — Microbenchmarks (timeit, criterion.rs, JMH), macrobenchmarks (end-to-end latency, throughput). Warm-up, statistical significance, percentiles (p50, p95, p99). Load testing (k6, Locust).

### Concurrency Models

- **Shared Memory** — Threads with locks, atomics. Data races, deadlocks. Most common in C/C++, Java, Python.
- **Message Passing** — Channels (Go), mailboxes (Erlang/Elixir actors). No shared state, communicate by sending messages. Easier to reason about correctness.
- **Async/Await** — Cooperative multitasking. Single thread handles many I/O-bound tasks. Event loop (JS, Python asyncio), runtime (tokio for Rust). Not true parallelism for CPU-bound work.
- **CSP (Communicating Sequential Processes)** — Formal model: processes communicate via synchronous channels. Go's concurrency model. Contrast with Actor model (async, buffered mailboxes).

---

## Related

- [[academic-taxonomy|Academic Taxonomy]] -- Full curriculum across all domains
- [[knowledge-index|Knowledge Index]] -- Domain overview and project connections
