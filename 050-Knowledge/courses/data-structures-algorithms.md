---
title: "Course: Data Structures & Algorithms"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, dsa, algorithms, data-structures]
prerequisites: [discrete-math, basic-programming, proof-techniques]
---

# Data Structures & Algorithms

> *Back to [[../cs-syllabus|CS Syllabus]] | Related: [[databases|Databases]], [[operating-systems|Operating Systems]], [[distributed-systems|Distributed Systems]]*

## Motivation

Data structures and algorithms form the computational backbone of all software. Every program, from a simple script to a distributed database, is ultimately a composition of data organization choices and algorithmic strategies. Mastery of this material enables you to reason about program efficiency, design scalable systems, and solve novel problems by recognizing structural patterns.

## Prerequisites

- **Discrete Mathematics:** Sets, relations, functions, basic combinatorics, mathematical induction
- **Programming fluency:** Comfortable writing and debugging code in at least one language (Python, C/C++, Java)
- **Proof techniques:** Induction, contradiction, and direct proof for correctness arguments

---

## I. Foundational Complexity Analysis

### 1.1 Asymptotic Notation

- **Big-O (O):** Upper bound on growth rate. f(n) = O(g(n)) means there exist constants c > 0 and n0 such that f(n) <= c * g(n) for all n >= n0.
- **Big-Omega (Omega):** Lower bound. f(n) = Omega(g(n)) means f(n) >= c * g(n) for sufficiently large n.
- **Big-Theta (Theta):** Tight bound. f(n) = Theta(g(n)) when f is both O(g(n)) and Omega(g(n)).
- **Little-o and little-omega:** Strict (non-tight) upper and lower bounds.

### 1.2 Common Growth Classes

O(1) < O(log n) < O(sqrt(n)) < O(n) < O(n log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)

### 1.3 Amortized Analysis

- **Aggregate method:** Total cost over n operations divided by n.
- **Accounting method:** Assign artificial "charges" to operations; overcharges stored as credit for future expensive operations.
- **Potential method:** Define a potential function Phi on the data structure state. Amortized cost = actual cost + delta(Phi).
- **Classic example:** Dynamic array doubling — individual insert can be O(n) but amortized O(1).

### 1.4 Recurrence Relations

- **Master theorem:** For T(n) = aT(n/b) + O(n^d):
  - If d < log_b(a): T(n) = O(n^{log_b(a)})
  - If d = log_b(a): T(n) = O(n^d log n)
  - If d > log_b(a): T(n) = O(n^d)
- **Recursion tree method:** Expand recurrence into a tree; sum work across levels.
- **Substitution method:** Guess and verify via induction.

---

## II. Linear Data Structures

### 2.1 Arrays

**Static Arrays:**
- Contiguous memory block with O(1) random access via pointer arithmetic.
- Fixed size determined at allocation time.

**Dynamic Arrays (ArrayList, std::vector, Python list):**
- Grow by doubling capacity when full. Amortized O(1) append.
- Shrink (optionally) when load factor drops below threshold (e.g., 1/4).

**Circular Arrays:**
- Fixed-size buffer with head and tail pointers wrapping around using modular arithmetic.
- Ideal for bounded queues and ring buffers.
- Enqueue/dequeue both O(1). Full vs. empty distinguished by tracking count or leaving one slot unused.

**Sparse Arrays:**
- When most elements are zero/default, store only non-default entries.
- Implementations: hash map of index -> value, or compressed sparse row (CSR) format for matrices.
- Trade random access speed for memory efficiency.

### 2.2 Linked Lists

**Singly Linked List:**
- Each node stores data and a `next` pointer.
- O(1) insertion/deletion at head; O(n) search; O(n) insertion at arbitrary position.
- Memory overhead: one pointer per node. Non-contiguous memory means poor cache locality.

**Doubly Linked List:**
- Each node has `prev` and `next` pointers.
- O(1) deletion given a node reference (no need to find predecessor).
- Used in LRU caches, browser history, text editor buffers.

**Circular Linked List:**
- Tail's `next` points back to head. Useful for round-robin scheduling, circular buffers.
- No null terminator; traversal must detect the starting node to avoid infinite loops.

**Skip List:**
- Probabilistic data structure: multiple layers of linked lists with express lanes.
- Each element promoted to the next level with probability p (typically 1/2).
- Expected O(log n) search, insert, delete. Simpler to implement than balanced BSTs.
- Used in Redis sorted sets, LevelDB/RocksDB memtables.

**XOR Linked List:**
- Each node stores `prev XOR next` in a single pointer field, saving memory.
- Traversal requires knowing the previous node's address to derive the next.
- Rarely used in practice due to complexity and incompatibility with garbage collectors.

### 2.3 Stacks

- **LIFO** principle. Operations: push, pop, peek — all O(1).
- Implementations: array-based (dynamic array) or linked-list-based.
- Applications: function call stack, expression evaluation (postfix/infix conversion), parenthesis matching, DFS, undo systems.
- **Monotonic stack:** Maintains elements in sorted order; used for "next greater element" problems. O(n) amortized for processing n elements.

### 2.4 Queues

**Standard Queue (FIFO):**
- Enqueue at rear, dequeue from front. O(1) both operations.
- Array implementation uses circular buffer to avoid wasted space.

**Circular Queue (Ring Buffer):**
- Fixed-size array with head/tail indices wrapping via modulo.
- Used in OS I/O buffers, network packet queues, producer-consumer patterns.

**Double-Ended Queue (Deque):**
- Insert and remove from both ends in O(1).
- Implementations: doubly-linked list or circular array.
- Applications: sliding window maximum, palindrome checking, work-stealing schedulers.

**Priority Queue:**
- Elements dequeued by priority, not insertion order.
- Typically implemented via a binary heap (see Section IV).
- Operations: insert O(log n), extract-min/max O(log n), peek O(1).
- Applications: Dijkstra's algorithm, Huffman coding, job scheduling, event simulation.

---

## III. Hash Tables

### 3.1 Hash Functions

- Map keys from a universe U to indices in [0, m-1].
- **Division method:** h(k) = k mod m. Choose m as a prime not close to a power of 2.
- **Multiplication method:** h(k) = floor(m * (k * A mod 1)) for irrational A (Knuth suggests A = (sqrt(5)-1)/2).
- **Universal hashing:** Family of hash functions; randomly chosen member guarantees expected O(1) collision probability.
- **Cryptographic hashing** (SHA-256, etc.) — slow but uniform; used for integrity, not performance-critical tables.

### 3.2 Collision Resolution: Chaining

- Each bucket holds a linked list (or balanced BST for worst-case O(log n) per bucket).
- Load factor alpha = n/m. Expected chain length is alpha.
- Simple to implement; performance degrades gracefully.
- Java's HashMap switches from linked list to red-black tree when bucket exceeds 8 entries.

### 3.3 Collision Resolution: Open Addressing

- All entries stored in the table itself. On collision, probe for the next open slot.
- **Linear probing:** h(k, i) = (h(k) + i) mod m. Simple, good cache locality, but suffers from primary clustering.
- **Quadratic probing:** h(k, i) = (h(k) + c1*i + c2*i^2) mod m. Reduces primary clustering, but secondary clustering persists.
- **Double hashing:** h(k, i) = (h1(k) + i * h2(k)) mod m. Best distribution; h2(k) must be coprime to m.
- **Robin Hood hashing:** On collision, the element with the shorter probe distance gives up its slot. Reduces variance in probe lengths.
- **Cuckoo hashing:** Two hash functions, two tables. Insertion evicts existing element to its alternate position. O(1) worst-case lookup.

### 3.4 Perfect Hashing

- For a static set of n keys, construct a hash function with zero collisions.
- **FKS (Fredman-Komlos-Szemeredi):** Two-level scheme. O(n) space, O(1) worst-case lookup.
- **Minimal perfect hashing:** Maps n keys to exactly {0, ..., n-1}. Libraries: CMPH, BBHash.
- Used in compilers (keyword lookup), databases (static index), network routers.

### 3.5 Practical Considerations

- **Rehashing:** When load factor exceeds threshold (e.g., 0.75), allocate a new larger table and re-insert all elements.
- **Consistent hashing:** For distributed systems — minimizes key reassignment when nodes join/leave. See [[distributed-systems|Distributed Systems]].
- **Bloom filters:** Probabilistic membership test. False positives possible, false negatives impossible. Space-efficient.

---

## IV. Trees

### 4.1 Binary Search Trees (BST)

- Each node's left subtree contains only keys less than the node's key; right subtree contains only greater keys.
- Average case: O(log n) search, insert, delete. Worst case (degenerate/linear): O(n).
- In-order traversal yields sorted sequence.

### 4.2 Self-Balancing BSTs

**AVL Trees:**
- Balance factor (height difference of subtrees) maintained in {-1, 0, 1}.
- Rotations (single and double) restore balance after insertion/deletion.
- Guaranteed O(log n) height. More rigidly balanced than red-black trees; faster lookups but slower insertions.

**Red-Black Trees:**
- Each node colored red or black. Five properties enforce approximate balance.
- Height at most 2 * log2(n+1). O(log n) all operations.
- Fewer rotations on insertion/deletion than AVL (at most 2-3 rotations per operation).
- Used in: Linux CFS scheduler, Java TreeMap, C++ std::map.

**Splay Trees:**
- Self-adjusting: recently accessed elements moved to root via splaying (zig, zig-zig, zig-zag rotations).
- No explicit balance information stored. Amortized O(log n) per operation.
- Optimal for non-uniform access patterns (working set theorem).
- Not suitable for real-time systems due to O(n) worst-case individual operations.

### 4.3 B-Trees and B+ Trees

**B-Trees (order m):**
- Each node holds up to m-1 keys and m children.
- All leaves at the same depth. Minimum degree t: each non-root node has at least t-1 keys.
- Designed for disk-based storage: minimizes I/O by maximizing branching factor.
- O(log_t n) search, insert, delete.

**B+ Trees:**
- All data stored in leaves; internal nodes contain only keys for routing.
- Leaves linked in a doubly-linked list for efficient range queries.
- The dominant index structure in relational databases. See [[databases|Databases]].

### 4.4 Segment Trees

- Binary tree over an array for answering range queries (sum, min, max, GCD) in O(log n).
- Build: O(n). Point update: O(log n). Range query: O(log n).
- **Lazy propagation:** Defer updates to subtrees; apply lazily during queries. Enables O(log n) range updates.
- **Persistent segment tree:** Retain previous versions using path copying. O(log n) per version.

### 4.5 Fenwick Trees (Binary Indexed Trees)

- Array-based structure for prefix sums with point updates.
- Build: O(n). Point update: O(log n). Prefix query: O(log n).
- Simpler and lower constant factor than segment trees, but less flexible (primarily prefix operations).
- Index arithmetic uses bitwise operations: `i += i & (-i)` to traverse.

### 4.6 Tries (Prefix Trees)

- Tree where each edge represents a character. Paths from root to nodes spell prefixes.
- O(L) lookup for a string of length L, independent of the number of stored strings.
- **Compressed trie (Patricia/Radix tree):** Merge chains of single-child nodes. Saves space.
- Applications: autocomplete, spell checking, IP routing tables, dictionary implementation.

### 4.7 Other Tree Structures

- **Treap:** BST + heap property using random priorities. Expected O(log n) operations.
- **K-D Tree:** Partition k-dimensional space. Nearest-neighbor queries in O(log n) average.
- **Interval Tree:** Store intervals; query all intervals containing a point in O(log n + k).
- **Suffix Tree:** All suffixes of a string in a compressed trie. O(n) construction (Ukkonen's algorithm). Powerful for substring queries.

---

## V. Heaps

### 5.1 Binary Heap

- Complete binary tree stored in an array. Parent at index i; children at 2i+1, 2i+2.
- **Min-heap property:** parent <= children. **Max-heap property:** parent >= children.
- Insert: O(log n) — add at end, sift up. Extract-min/max: O(log n) — swap root with last, sift down.
- **Heapify (build heap):** O(n) via bottom-up sift-down. NOT O(n log n).
- **Heapsort:** Build max-heap, repeatedly extract max. O(n log n) in-place, not stable.

### 5.2 Fibonacci Heap

- Collection of heap-ordered trees with lazy consolidation.
- **Amortized complexities:** Insert O(1), find-min O(1), decrease-key O(1), delete-min O(log n), merge O(1).
- The O(1) decrease-key makes it theoretically optimal for Dijkstra's algorithm: O(V log V + E).
- Complex implementation; high constant factors. Rarely used in practice despite theoretical advantages.

### 5.3 Binomial Heap

- Collection of binomial trees (B_k has 2^k nodes, root degree k).
- Merge two heaps: O(log n) — analogous to binary addition of binomial trees.
- Insert O(log n) worst case, O(1) amortized. Delete-min O(log n).
- Simpler than Fibonacci heaps; used when frequent merges are needed.

### 5.4 Other Heaps

- **Pairing heap:** Simpler alternative to Fibonacci heaps. Conjectured O(1) amortized decrease-key (proven O(log log n)).
- **d-ary heap:** Generalization with d children per node. Reduces height to log_d(n) but increases sift-down work. Optimal d depends on insert/delete ratio.
- **Leftist heap / Skew heap:** Mergeable heaps based on biased tree structure. O(log n) merge.

---

## VI. Graphs

### 6.1 Representations

- **Adjacency matrix:** O(V^2) space. O(1) edge lookup. Good for dense graphs.
- **Adjacency list:** O(V + E) space. O(degree(v)) to check neighbors. Good for sparse graphs.
- **Edge list:** Simple list of (u, v, w) tuples. Useful for Kruskal's algorithm.
- **Incidence matrix:** V x E matrix. Rarely used; useful for some theoretical analyses.

### 6.2 Traversals

**Breadth-First Search (BFS):**
- Uses a queue. Explores vertices layer by layer.
- O(V + E). Finds shortest paths in unweighted graphs.
- Applications: shortest path, connected components, bipartiteness testing.

**Depth-First Search (DFS):**
- Uses a stack (or recursion). Explores as deep as possible before backtracking.
- O(V + E). Classifies edges: tree, back, forward, cross edges.
- Applications: cycle detection, topological sort, SCC, articulation points, bridges.

### 6.3 Shortest Path Algorithms

**Dijkstra's Algorithm:**
- Single-source shortest paths for non-negative weights.
- Greedy: always expand the nearest unvisited vertex.
- With binary heap: O((V + E) log V). With Fibonacci heap: O(V log V + E).
- Does NOT work with negative edge weights.

**Bellman-Ford Algorithm:**
- Single-source shortest paths, handles negative weights.
- Relax all edges V-1 times. O(V * E).
- Detects negative-weight cycles (if any edge can still be relaxed after V-1 iterations).

**Floyd-Warshall Algorithm:**
- All-pairs shortest paths via dynamic programming.
- O(V^3) time, O(V^2) space. Works with negative weights (no negative cycles).
- dp[i][j][k] = shortest path from i to j using only vertices {1, ..., k} as intermediaries.

**A* Search:**
- Informed search using heuristic h(n) estimating cost from n to goal.
- f(n) = g(n) + h(n), where g(n) is actual cost from start to n.
- Optimal if h is admissible (never overestimates) and consistent (h(n) <= cost(n, n') + h(n')).
- With good heuristic, explores far fewer nodes than Dijkstra.

### 6.4 Minimum Spanning Trees

**Prim's Algorithm:**
- Grow MST from a starting vertex; always add the cheapest edge connecting the tree to a non-tree vertex.
- With binary heap: O(E log V). With Fibonacci heap: O(E + V log V).

**Kruskal's Algorithm:**
- Sort all edges by weight. Add edges in order if they don't create a cycle (checked via Union-Find).
- O(E log E). Best for sparse graphs.

**Union-Find (Disjoint Set Union):**
- Operations: find(x), union(x, y). With path compression and union by rank: nearly O(1) amortized (inverse Ackermann).
- Essential for Kruskal's and dynamic connectivity problems.

### 6.5 Topological Sort

- Linear ordering of DAG vertices such that for every edge (u, v), u appears before v.
- **Kahn's algorithm:** Repeatedly remove vertices with in-degree 0. Uses BFS. O(V + E).
- **DFS-based:** Reverse of DFS finish order. O(V + E).
- Applications: build systems, course prerequisites, task scheduling.

### 6.6 Strongly Connected Components (SCC)

**Tarjan's Algorithm:**
- Single DFS pass using a stack and low-link values.
- When a node's low-link equals its DFS index, it's the root of an SCC; pop the stack to extract the component.
- O(V + E).

**Kosaraju's Algorithm:**
- Two-pass approach: (1) DFS on original graph, record finish order. (2) DFS on transposed graph in reverse finish order.
- Each DFS tree in pass 2 is an SCC. O(V + E).

### 6.7 Network Flow

**Ford-Fulkerson Method:**
- Repeatedly find augmenting paths from source to sink in the residual graph; augment flow along the path.
- Termination guaranteed with integer capacities. Complexity: O(E * max_flow) — can be slow.

**Edmonds-Karp Algorithm:**
- Ford-Fulkerson with BFS for finding augmenting paths (shortest augmenting path).
- O(V * E^2). Polynomial and practical.

**Applications:** Maximum bipartite matching, minimum cut (max-flow min-cut theorem), circulation problems, project selection.

**Advanced:** Dinic's algorithm O(V^2 * E), push-relabel O(V^2 * E) or O(V^3).

---

## VII. Algorithm Paradigms

### 7.1 Divide and Conquer

- Split problem into smaller subproblems, solve recursively, combine results.
- **Examples:** Merge sort O(n log n), quicksort O(n log n) expected, binary search O(log n), Strassen's matrix multiplication O(n^{2.807}), closest pair of points O(n log n), FFT O(n log n).
- Analysis via recurrence relations and the Master theorem.

### 7.2 Dynamic Programming

**Core idea:** Optimal substructure + overlapping subproblems. Store solutions to subproblems to avoid recomputation.

**Top-Down (Memoization):**
- Recursive solution with a cache (hash map or array).
- Natural to write; may have stack overhead for deep recursion.

**Bottom-Up (Tabulation):**
- Iteratively fill a table from base cases upward.
- No recursion overhead; often allows space optimization by keeping only the previous row/layer.

**Common Patterns:**
- **1D DP:** Fibonacci, climbing stairs, coin change (minimum coins), longest increasing subsequence.
- **2D DP:** Edit distance, longest common subsequence, matrix chain multiplication, knapsack (0/1 and unbounded).
- **Interval DP:** Optimal BST, burst balloons, matrix chain.
- **DP on trees:** Subtree problems, tree diameter, tree DP with rerooting.
- **Bitmask DP:** Traveling salesman O(2^n * n^2), assignment problem, Hamiltonian path.
- **Digit DP:** Count numbers in a range satisfying digit constraints.

**Space Optimization:** When dp[i] depends only on dp[i-1], use two arrays or a single array with careful update ordering.

### 7.3 Greedy Algorithms

- Make locally optimal choices hoping for a globally optimal solution.
- **Proof techniques:** Exchange argument, greedy stays ahead, matroid theory.
- **Examples:** Activity selection, Huffman coding, fractional knapsack, interval scheduling, Dijkstra's, Prim's, Kruskal's.
- Greedy does NOT work for: 0/1 knapsack, TSP, general graph coloring.

### 7.4 Backtracking

- Systematic exploration of solution space with pruning.
- Build solution incrementally; abandon ("backtrack") when constraints are violated.
- **Examples:** N-Queens, Sudoku solver, graph coloring, subset sum, permutation generation.
- Time complexity often exponential, but pruning dramatically reduces practical runtime.

### 7.5 Branch and Bound

- Backtracking enhanced with bounding functions.
- Maintain a bound on the best possible solution in each branch; prune branches that cannot improve on the current best.
- Used for optimization problems: TSP, integer linear programming, knapsack.
- Best-first search variant: expand the most promising node first (use priority queue).

---

## VIII. String Algorithms

### 8.1 Pattern Matching

**Knuth-Morris-Pratt (KMP):**
- Precompute failure function (longest proper prefix that is also a suffix).
- O(n + m) where n = text length, m = pattern length. No backtracking on the text.

**Rabin-Karp:**
- Rolling hash over windows of the text. O(n + m) expected; O(nm) worst case.
- Efficient for multiple pattern search (compute hashes for all patterns).
- Hash function: polynomial rolling hash with a large prime modulus.

### 8.2 Multi-Pattern Matching

**Aho-Corasick:**
- Builds a trie of all patterns with failure links (generalization of KMP to multiple patterns).
- O(n + m + z) where z = number of matches, m = total pattern length.
- Used in: intrusion detection systems, DNA sequence matching, text filtering.

### 8.3 Suffix Structures

**Suffix Array:**
- Sorted array of all suffixes of a string. O(n log n) or O(n) construction.
- Combined with LCP array for O(n) substring queries, longest repeated substring, etc.
- More space-efficient than suffix trees.

**Suffix Tree:**
- Compressed trie of all suffixes. O(n) construction (Ukkonen's algorithm).
- Powerful: longest common substring, pattern matching, tandem repeats — all in linear time.

---

## IX. Computational Complexity Theory

### 9.1 Complexity Classes

- **P:** Problems solvable in polynomial time by a deterministic Turing machine.
- **NP:** Problems whose solutions are verifiable in polynomial time. (Equivalently, solvable in polynomial time by a nondeterministic TM.)
- **P vs. NP:** Open question — is P = NP? Widely believed P != NP.
- **NP-Hard:** At least as hard as any problem in NP. May not be in NP (e.g., halting problem).
- **NP-Complete:** In NP AND NP-Hard. The "hardest" problems in NP.

### 9.2 Key NP-Complete Problems

- SAT (Boolean satisfiability) — Cook-Levin theorem: first proven NP-complete problem.
- 3-SAT, vertex cover, independent set, clique, Hamiltonian cycle, TSP (decision version), subset sum, graph coloring (k >= 3), set cover.

### 9.3 Reductions

- To prove problem A is NP-hard: show a known NP-hard problem B reduces to A in polynomial time.
- **Karp reduction (many-one):** Transform instances of B into instances of A.
- If A is in NP and NP-hard, then A is NP-complete.

### 9.4 Coping with NP-Hardness

- **Approximation algorithms:** Guarantee solution within a factor of optimal. E.g., 2-approximation for vertex cover, (1 + epsilon)-approximation for knapsack (FPTAS).
- **Parameterized complexity:** Fixed-parameter tractable (FPT) algorithms. E.g., vertex cover is O(2^k * n) where k = solution size.
- **Heuristics and metaheuristics:** Simulated annealing, genetic algorithms, local search. No guarantees but often good in practice.
- **Special cases:** Restrict input structure (planar graphs, bounded treewidth) for efficient solutions.

---

## X. Practical Examples and Exercises

### Example 1: Two Sum (Hash Table)
Given an array and a target, find two numbers that sum to the target. Use a hash map for O(n) solution: for each element x, check if (target - x) exists in the map.

### Example 2: Merge Intervals (Sorting + Greedy)
Sort intervals by start time. Iterate, merging overlapping intervals. O(n log n).

### Example 3: LRU Cache (Hash Map + Doubly Linked List)
O(1) get and put. Hash map for key lookup; doubly linked list for recency ordering. Move accessed nodes to front; evict from tail.

### Example 4: Shortest Path in Weighted Graph (Dijkstra)
Build adjacency list. Use a min-heap priority queue. Relax edges greedily. Track predecessors for path reconstruction.

### Example 5: Longest Common Subsequence (DP)
Build 2D table dp[i][j] = LCS length of first i chars of X and first j chars of Y. If X[i] == Y[j], dp[i][j] = dp[i-1][j-1] + 1; else max(dp[i-1][j], dp[i][j-1]). O(mn).

---

## References

1. Cormen, Leiserson, Rivest, Stein — *Introduction to Algorithms* (CLRS), 4th ed.
2. Sedgewick, Wayne — *Algorithms*, 4th ed.
3. Kleinberg, Tardos — *Algorithm Design*
4. Skiena — *The Algorithm Design Manual*, 3rd ed.
5. Sipser — *Introduction to the Theory of Computation*, 3rd ed.
6. Erickson — *Algorithms* (free textbook, jeffe.cs.illinois.edu)
7. Competitive programming resources: Codeforces, LeetCode, CP-Algorithms (cp-algorithms.com)
