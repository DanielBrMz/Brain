---
title: "Course: Databases"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, databases, sql, postgresql, redis, nosql]
prerequisites: [data-structures-algorithms, discrete-math, operating-systems]
---

# Databases

> *Back to [[../cs-syllabus|CS Syllabus]] | Related: [[distributed-systems|Distributed Systems]], [[data-structures-algorithms|DSA]], [[operating-systems|Operating Systems]]*

## Motivation

Databases are the foundation of nearly all software systems. Whether you're building a web application, an analytics pipeline, or a distributed service, understanding how data is stored, queried, and maintained is essential. This course covers relational theory, SQL mastery, storage engine internals, indexing strategies, transaction management, and practical experience with PostgreSQL, Redis, and modern ORMs.

## Prerequisites

- **Data Structures & Algorithms:** B-trees, hash tables, sorting, complexity analysis (see [[data-structures-algorithms|DSA]])
- **Discrete Mathematics:** Sets, relations, first-order logic
- **Operating Systems:** File systems, I/O, memory management (see [[operating-systems|Operating Systems]])

---

## I. The Relational Model

### 1.1 Foundations

- **Codd's relational model (1970):** Data organized into relations (tables). Each relation has a schema (set of attributes with domains). Tuples (rows) are instances.
- **Keys:**
  - **Super key:** Any set of attributes that uniquely identifies a tuple.
  - **Candidate key:** Minimal super key (no subset is a super key).
  - **Primary key:** Chosen candidate key. Cannot be NULL.
  - **Foreign key:** References the primary key of another relation. Enforces referential integrity.
- **Constraints:** Domain constraints, NOT NULL, UNIQUE, CHECK, foreign key constraints, triggers.
- **Relational algebra:** Select (sigma), project (pi), join, union, difference, rename, division. Foundation for SQL.

### 1.2 Normalization

**Functional Dependencies:**
- X -> Y means the value of X uniquely determines the value of Y.
- **Armstrong's axioms:** Reflexivity, augmentation, transitivity. Sound and complete.

**Normal Forms:**
- **1NF:** All attributes are atomic (no repeating groups, no nested relations).
- **2NF:** 1NF + no partial dependencies (every non-key attribute depends on the FULL primary key).
- **3NF:** 2NF + no transitive dependencies (non-key attributes don't depend on other non-key attributes).
- **BCNF (Boyce-Codd Normal Form):** For every functional dependency X -> Y, X is a super key. Stricter than 3NF. Eliminates all redundancy from functional dependencies.
- **Trade-off:** Higher normalization reduces redundancy and update anomalies but increases join complexity. Denormalization is sometimes necessary for read performance.

---

## II. SQL

### 2.1 Core Statements

```sql
-- DDL
CREATE TABLE, ALTER TABLE, DROP TABLE, CREATE INDEX

-- DML
SELECT, INSERT, UPDATE, DELETE, MERGE (UPSERT)

-- DCL
GRANT, REVOKE

-- TCL
BEGIN, COMMIT, ROLLBACK, SAVEPOINT
```

### 2.2 Joins

- **INNER JOIN:** Only matching rows from both tables.
- **LEFT (OUTER) JOIN:** All rows from left table; NULLs for unmatched right rows.
- **RIGHT (OUTER) JOIN:** All rows from right table; NULLs for unmatched left rows.
- **FULL (OUTER) JOIN:** All rows from both tables; NULLs where no match.
- **CROSS JOIN:** Cartesian product. Every row of table A paired with every row of table B.
- **NATURAL JOIN:** Join on columns with the same name. Generally avoided — fragile.
- **Self-join:** Table joined with itself (e.g., hierarchical data, comparing rows).
- **Lateral join (LATERAL):** Subquery in FROM clause can reference columns from preceding tables. PostgreSQL-specific but powerful.

### 2.3 Subqueries

- **Scalar subquery:** Returns a single value. Can be used in SELECT list or WHERE clause.
- **Correlated subquery:** References columns from the outer query. Evaluated once per outer row (can be slow).
- **EXISTS / NOT EXISTS:** Test for the existence of rows. Often more efficient than IN for large datasets.
- **IN / NOT IN:** Match against a set of values. Beware of NULL handling with NOT IN.
- **ANY / ALL:** Compare against subquery results.

### 2.4 Window Functions

- Perform calculations across a set of rows related to the current row WITHOUT collapsing rows (unlike GROUP BY).
- **Syntax:** `function_name() OVER (PARTITION BY ... ORDER BY ... frame_clause)`
- **Ranking functions:** ROW_NUMBER(), RANK() (gaps for ties), DENSE_RANK() (no gaps), NTILE(n).
- **Aggregate window functions:** SUM(), AVG(), COUNT(), MIN(), MAX() with OVER clause.
- **Navigation:** LAG(expr, offset), LEAD(expr, offset), FIRST_VALUE(), LAST_VALUE(), NTH_VALUE().
- **Frame clauses:** ROWS BETWEEN ... AND ..., RANGE BETWEEN ... AND ..., GROUPS BETWEEN ... AND ...
  - `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` — running total.
  - `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` — 3-row moving average.

### 2.5 Common Table Expressions (CTEs)

```sql
WITH cte_name AS (
    SELECT ...
),
another_cte AS (
    SELECT ... FROM cte_name ...
)
SELECT ... FROM another_cte;
```

- **Recursive CTEs:** For hierarchical/graph traversal (organizational charts, bill of materials, tree structures).
```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, name, 1 AS depth
    FROM categories WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.parent_id, c.name, t.depth + 1
    FROM categories c JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;
```

- **Materialization:** In PostgreSQL, CTEs are optimization barriers by default (materialized). Use `NOT MATERIALIZED` hint to allow the optimizer to push predicates into the CTE.

### 2.6 Advanced SQL

- **GROUPING SETS, CUBE, ROLLUP:** Multi-level aggregation in a single query.
- **FILTER clause:** `COUNT(*) FILTER (WHERE status = 'active')` — conditional aggregation without CASE.
- **ARRAY, JSON/JSONB operations:** PostgreSQL supports querying, indexing, and transforming JSON data natively.
- **Generated columns:** Computed columns stored or virtual.
- **RETURNING clause:** Return affected rows from INSERT, UPDATE, DELETE.
- **UPSERT:** `INSERT ... ON CONFLICT ... DO UPDATE SET ...` (PostgreSQL) or `MERGE` (standard SQL).

---

## III. Indexing

### 3.1 B-Tree Indexes

- The default index type in most RDBMSes. Balanced tree with high branching factor.
- Supports equality and range queries, ORDER BY, and MIN/MAX.
- **Multi-column indexes:** Leftmost prefix of columns can be used. Index on (a, b, c) supports queries on (a), (a, b), and (a, b, c) but NOT (b) or (c) alone.
- **Covering index (index-only scan):** If all columns needed are in the index, no table lookup needed. Use INCLUDE clause in PostgreSQL.
- **Partial index:** Index only rows matching a WHERE condition. Smaller and faster for targeted queries.

### 3.2 Hash Indexes

- O(1) lookup for equality queries only. No range query support.
- In PostgreSQL, hash indexes are now WAL-logged and crash-safe (since PG 10), but B-tree is usually preferred.

### 3.3 GiST (Generalized Search Tree)

- Framework for building custom index types. Supports containment, intersection, nearest-neighbor.
- Used for: geometric data (PostGIS), full-text search, range types, ltree.
- Supports the `@>`, `<@`, `&&`, `<<`, `>>` operators.

### 3.4 GIN (Generalized Inverted Index)

- Inverted index: maps each value to a list of rows containing it.
- Ideal for: full-text search (tsvector), JSONB containment queries, array element queries.
- Faster lookups than GiST for containment but slower updates (pending list).
- `gin_trgm_ops`: Trigram-based index for LIKE and ILIKE queries.

### 3.5 BRIN (Block Range Index)

- Stores summary info (min/max) per block range. Very small index size.
- Effective when data is physically sorted (e.g., time-series data with sequential inserts).
- O(1) size per block range. Scans skip irrelevant block ranges.

### 3.6 Index Design Principles

- Index columns used in WHERE, JOIN, ORDER BY, GROUP BY.
- Consider selectivity: high-cardinality columns benefit most from indexes.
- Avoid over-indexing: each index adds write overhead and storage.
- Use EXPLAIN ANALYZE to verify index usage.
- Composite index column order: most selective first, or match query patterns.

---

## IV. Query Optimization

### 4.1 Query Processing Pipeline

1. **Parsing:** SQL text -> parse tree.
2. **Rewriting:** View expansion, rule application.
3. **Planning/Optimization:** Generate candidate plans, estimate costs, choose cheapest.
4. **Execution:** Execute the chosen plan.

### 4.2 Cost-Based Optimization

- Estimate the cost of each plan based on I/O, CPU, and network costs.
- **Statistics:** Table row counts, column distinct values, histograms, most common values. Updated via ANALYZE.
- **Selectivity estimation:** Fraction of rows matching a predicate. Uniform assumption for unknown distributions.
- **Cardinality estimation:** Estimated number of rows at each stage. Errors compound through joins (the optimizer's biggest challenge).

### 4.3 Join Algorithms

- **Nested Loop Join:** For each row in outer table, scan inner table. O(n*m). Good when inner table is small and indexed.
- **Hash Join:** Build hash table on smaller table, probe with larger table. O(n + m). Best for equality joins without indexes.
- **Merge Join (Sort-Merge):** Sort both tables on join key, merge. O(n log n + m log m). Good when inputs are already sorted.

### 4.4 Join Ordering

- For n tables, there are n!/2 possible join orderings (exponential).
- Optimizer uses dynamic programming (for small n) or heuristics/greedy algorithms (for large n).
- **Left-deep trees:** Only consider left-deep join plans (pipeline-friendly). Reduces search space.

### 4.5 EXPLAIN and EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE SELECT ... ;
```
- **EXPLAIN:** Shows the query plan without executing.
- **EXPLAIN ANALYZE:** Executes the query and shows actual vs. estimated row counts and timing.
- Key things to look for: sequential scans on large tables (missing index?), poor cardinality estimates, unnecessary sorts, nested loops with large tables.
- **Buffers option:** `EXPLAIN (ANALYZE, BUFFERS)` — shows buffer hits vs. reads (cache effectiveness).

---

## V. Transactions and Concurrency

### 5.1 ACID Properties

- **Atomicity:** Implemented via undo log / WAL. All or nothing.
- **Consistency:** Application-level invariants enforced by constraints and triggers.
- **Isolation:** Concurrency control mechanisms (locks, MVCC).
- **Durability:** Write-ahead log (WAL) flushed to disk before commit confirmation.

### 5.2 Isolation Levels (SQL Standard)

| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-------|-----------|-------------------|-------------|
| Read Uncommitted | Possible | Possible | Possible |
| Read Committed | No | Possible | Possible |
| Repeatable Read | No | No | Possible |
| Serializable | No | No | No |

- **PostgreSQL default:** Read Committed.
- **PostgreSQL Repeatable Read:** Actually provides snapshot isolation (stronger than SQL standard's Repeatable Read).
- **PostgreSQL Serializable:** Serializable Snapshot Isolation (SSI). Detects serialization anomalies and aborts conflicting transactions.

### 5.3 MVCC (Multi-Version Concurrency Control)

- Each transaction sees a snapshot of the database at its start time.
- Writers don't block readers; readers don't block writers.
- **PostgreSQL implementation:** Each tuple has xmin (creating transaction) and xmax (deleting transaction). Visibility determined by comparing these with the current transaction's snapshot.
- **Vacuum:** Reclaims dead tuples (old versions no longer visible to any transaction). Critical for PostgreSQL performance. Autovacuum runs periodically.
- **HOT (Heap-Only Tuple) updates:** When update doesn't change indexed columns, new tuple version stored on the same page. Avoids index updates.

### 5.4 Write-Ahead Log (WAL)

- All modifications written to WAL before applying to data pages.
- On crash recovery: replay WAL from last checkpoint to reconstruct committed state.
- Also used for replication (streaming replication sends WAL records to replicas).
- **Checkpoint:** Periodically flush all dirty pages to disk and record a checkpoint in WAL. Bounds recovery time.

### 5.5 Locking

- **Row-level locks:** FOR UPDATE (exclusive), FOR SHARE (shared). Acquired during SELECT for serialization.
- **Table-level locks:** ACCESS SHARE (SELECT), ROW EXCLUSIVE (INSERT/UPDATE/DELETE), ACCESS EXCLUSIVE (DDL).
- **Advisory locks:** Application-level locks managed by the database. Useful for coordinating distributed processes.
- **Deadlock detection:** PostgreSQL detects deadlocks via wait-for graph and aborts one transaction.

---

## VI. PostgreSQL Internals

### 6.1 Storage Architecture

- **Pages (blocks):** 8KB fixed-size units. All I/O operates on pages.
- **Heap files:** Unordered collection of pages containing tuples. Each table is a heap file.
- **TOAST (The Oversized-Attribute Storage Technique):** Large values (>2KB) compressed and/or stored out-of-line in a separate TOAST table.
- **Tablespaces:** Map logical tables to physical disk locations.

### 6.2 System Catalogs

- `pg_class` — tables, indexes, sequences, views.
- `pg_attribute` — columns of all relations.
- `pg_statistic` — column statistics for the optimizer.
- `pg_index` — index metadata.
- `pg_proc` — functions and procedures.
- All queryable via SQL. `information_schema` provides a standard view.

### 6.3 Connection Management

- **Process-per-connection model:** Each client gets a dedicated backend process. Fork-based.
- **Connection pooling:** Essential for high-concurrency applications. Tools: PgBouncer (external), pgpool-II.
- PgBouncer modes: session (1:1), transaction (share connections between transactions), statement (share between statements — limited).

### 6.4 Extensions

- PostgreSQL's extension system enables adding functionality without core changes.
- **Key extensions:** PostGIS (geospatial), pg_trgm (trigram similarity), hstore (key-value), pgvector (vector similarity search), pg_stat_statements (query performance), TimescaleDB (time-series).

---

## VII. NoSQL Databases

### 7.1 Document Stores

- Store semi-structured documents (typically JSON/BSON).
- **MongoDB:** BSON documents, flexible schema, rich query language, aggregation pipeline.
- **Schema design:** Embed related data (denormalize) for read performance vs. reference (normalize) for write consistency.
- **When to use:** Rapidly evolving schemas, hierarchical data, content management.

### 7.2 Key-Value Stores

- Simplest model: get(key), put(key, value), delete(key).
- **DynamoDB:** AWS managed, single-digit millisecond latency, automatic scaling. Partition key + optional sort key.
- **When to use:** Session storage, caching, user preferences, shopping carts.

### 7.3 Column-Family Stores

- Data organized by column families rather than rows. Efficient for analytical queries over specific columns.
- **Cassandra:** Wide-column store, masterless (leaderless replication), tunable consistency, CQL query language.
- **HBase:** Column-family store on HDFS. Strong consistency (CP system). Good for sparse, wide tables.
- **When to use:** Time-series data, IoT sensor data, large-scale analytics.

### 7.4 Graph Databases

- Store nodes and edges as first-class entities. Optimized for traversal queries.
- **Neo4j:** Property graph model, Cypher query language, ACID transactions.
- **Use cases:** Social networks, recommendation engines, fraud detection, knowledge graphs.
- Relational databases CAN model graphs (recursive CTEs, adjacency lists) but graph databases offer better traversal performance.

---

## VIII. Redis

### 8.1 Data Structures

- **Strings:** Basic key-value. SET, GET, INCR, DECR, APPEND. Used for caching, counters, rate limiting.
- **Lists:** Linked lists. LPUSH, RPUSH, LPOP, RPOP, LRANGE. Used for queues, activity feeds.
- **Sets:** Unordered unique elements. SADD, SMEMBERS, SINTER, SUNION, SDIFF. Used for tags, unique visitors.
- **Sorted Sets (ZSETs):** Elements with scores. ZADD, ZRANGE, ZRANGEBYSCORE, ZRANK. Used for leaderboards, priority queues, rate limiters. Implemented via skip list + hash table.
- **Hashes:** Field-value pairs under a key. HSET, HGET, HGETALL. Used for objects, user profiles.
- **Streams:** Append-only log. XADD, XREAD, XREADGROUP. Used for event sourcing, messaging.
- **HyperLogLog:** Probabilistic cardinality estimation. PFADD, PFCOUNT. ~12KB per counter regardless of cardinality.
- **Bitmaps / Bitfields:** Bit-level operations. Used for feature flags, bloom filters, daily active users.

### 8.2 Pub/Sub

- PUBLISH / SUBSCRIBE / PSUBSCRIBE (pattern-based).
- Fire-and-forget: messages not persisted. If subscriber is offline, messages are lost.
- For durable messaging, use Redis Streams instead.

### 8.3 Lua Scripting

- Execute Lua scripts atomically on the server with EVAL / EVALSHA.
- Script sees a consistent snapshot of the database. Other commands blocked during script execution.
- Use for complex atomic operations: compare-and-set, rate limiting with multiple keys, conditional updates.

### 8.4 Persistence

- **RDB (snapshotting):** Periodic point-in-time dumps to disk. Fast restart, but data loss between snapshots.
- **AOF (Append-Only File):** Log every write operation. Configurable fsync (always, every second, never). More durable but larger files.
- **Hybrid:** RDB + AOF. Use RDB for fast loading, AOF for minimal data loss.

### 8.5 Redis Cluster

- Automatic sharding across multiple nodes. 16384 hash slots distributed across masters.
- Each master has one or more replicas for failover.
- Multi-key operations only supported when all keys are in the same hash slot (use hash tags: `{user:1}:profile`, `{user:1}:settings`).

---

## IX. ORMs

### 9.1 SQLAlchemy (Python)

- **Core:** SQL expression language. Table objects, select(), insert(), join(). Close to SQL but programmatic.
- **ORM:** Declarative mapping of Python classes to tables. Session manages identity map and unit of work.
- **Relationship loading:** Lazy (default, N+1 problem), eager (joinedload, subqueryload), selectin (batch loading).
- **Alembic:** Migration tool for SQLAlchemy. Auto-generates migration scripts from model changes.
- Used in the Sidepocket backend (see sp-app).

### 9.2 Prisma (TypeScript/JavaScript)

- **Schema-first:** Define models in `schema.prisma` file. Generates type-safe client.
- **Prisma Client:** Auto-generated, type-safe query builder. `prisma.user.findMany({ where: { ... }, include: { ... } })`.
- **Prisma Migrate:** Schema migration from Prisma schema changes.
- **Prisma Studio:** Visual database browser.
- Used in the nextblog project.

### 9.3 ORM Anti-Patterns

- **N+1 queries:** Loading related objects one by one instead of batch/eager loading. Use query logging to detect.
- **Fat models:** Putting business logic in ORM models. Keep models focused on data mapping.
- **Ignoring raw SQL:** ORMs are not always the best tool. Complex queries, bulk operations, and performance-critical paths often benefit from raw SQL.
- **Migration conflicts:** Coordinate schema changes across team members. Use sequential migration numbering.

---

## X. Database Design Patterns

### 10.1 Schema Design

- **Entity-Attribute-Value (EAV):** Flexible schema at the cost of query complexity. Usually better served by JSONB columns.
- **Polymorphic associations:** Single table inheritance (discriminator column), class table inheritance (table per subtype with shared PK), concrete table inheritance (separate tables).
- **Soft deletes:** `deleted_at` timestamp instead of physical deletion. Allows recovery but complicates queries (must filter).
- **Audit tables:** Track all changes with before/after values, timestamps, and user info. Trigger-based or application-level.
- **Temporal tables:** Track valid-time and transaction-time for bitemporal data. SQL:2011 standard.

### 10.2 Sharding

- Horizontal partitioning across multiple database instances.
- **Shard key selection:** Must distribute data evenly and align with query patterns. Poor shard key = hot spots.
- **Cross-shard queries:** Expensive scatter-gather. Design schema to minimize cross-shard operations.
- **Resharding:** Extremely painful. Plan shard key carefully upfront. Consistent hashing helps.
- See [[distributed-systems|Distributed Systems]] for partitioning strategies.

### 10.3 Replication

- **Streaming replication (PostgreSQL):** WAL records streamed to standby servers. Synchronous or asynchronous.
- **Logical replication:** Replicate specific tables or data subsets. Allows cross-version replication.
- **Read replicas:** Route read queries to replicas for horizontal read scaling. Watch for replication lag.

### 10.4 Connection and Query Patterns

- **Connection pooling:** PgBouncer, HikariCP. Essential for applications with many short-lived connections.
- **Prepared statements:** Parse and plan once, execute many times with different parameters. Reduces CPU overhead.
- **Batch operations:** Use COPY (PostgreSQL) for bulk inserts instead of individual INSERTs. Orders of magnitude faster.
- **Materialized views:** Precomputed query results stored as a table. REFRESH MATERIALIZED VIEW to update. Trade storage and staleness for query speed.

---

## References

1. Ramakrishnan, Gehrke — *Database Management Systems*, 3rd ed.
2. Garcia-Molina, Ullman, Widom — *Database Systems: The Complete Book*
3. Kleppmann — *Designing Data-Intensive Applications* (chapters 2-3, 5-7)
4. PostgreSQL official documentation (postgresql.org/docs)
5. Redis documentation (redis.io/docs)
6. SQLAlchemy documentation (docs.sqlalchemy.org)
7. Prisma documentation (prisma.io/docs)
8. Markus Winand — *SQL Performance Explained* (use-the-index-luke.com)
9. Citus Data blog — PostgreSQL scaling and performance articles
10. PgAnalyze blog — PostgreSQL performance and monitoring
