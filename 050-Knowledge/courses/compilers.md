---
title: "Course: Compilers"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, compilers, programming-languages, parsing]
prerequisites: [automata-computation, data-structures, discrete-math]
---

# Compilers

> Back to [[../cs-syllabus|CS Syllabus]] | Related: [[automata-computation]], [[software-engineering]]

## Motivation

Compilers are one of the most elegant intersections of theory and practice in computer science. Understanding how programming languages are translated into machine code illuminates everything from language design to performance optimization. Even if you never build a production compiler, the concepts — parsing, type systems, optimization, code generation — appear everywhere: linters, query engines, template systems, configuration languages, and domain-specific languages (DSLs). This course follows the classic compiler pipeline from source text to executable code.

## Prerequisites

- Formal languages and automata (regular expressions, context-free grammars, finite automata)
- Data structures (trees, graphs, hash tables, stacks)
- Assembly language basics (understanding of registers, instructions, memory)
- Discrete mathematics (sets, relations, induction)

---

## 1. Overview: The Compiler Pipeline

```
Source Code
    │
    ▼
┌──────────────┐
│ Lexical      │  Characters → Tokens
│ Analysis     │
└──────┬───────┘
       ▼
┌──────────────┐
│ Parsing      │  Tokens → Parse Tree / AST
│              │
└──────┬───────┘
       ▼
┌──────────────┐
│ Semantic     │  Type checking, scope resolution
│ Analysis     │
└──────┬───────┘
       ▼
┌──────────────┐
│ IR Generation│  AST → Intermediate Representation
│              │
└──────┬───────┘
       ▼
┌──────────────┐
│ Optimization │  IR → Optimized IR
│              │
└──────┬───────┘
       ▼
┌──────────────┐
│ Code         │  IR → Target Machine Code
│ Generation   │
└──────────────┘
```

**Compiler vs. Interpreter:** A compiler translates the entire program before execution; an interpreter executes the program statement by statement. Many modern systems are hybrids (e.g., Java compiles to bytecode, then JIT-compiles to native code).

---

## 2. Lexical Analysis (Scanning)

### 2.1 Purpose
- Transform a stream of characters into a stream of **tokens** (lexemes with categories)
- Strip whitespace and comments; report lexical errors (unterminated strings, invalid characters)

### 2.2 Regular Expressions
- Define token patterns: identifiers `[a-zA-Z_][a-zA-Z0-9_]*`, integers `[0-9]+`, operators `[+\-*/=]`
- Keywords are identifiers with reserved meaning (recognized after initial classification)
- Longest match rule: prefer the longest matching token
- Priority rule: when two patterns match same length, prefer the one listed first (keywords over identifiers)

### 2.3 Finite Automata
- **NFA (Nondeterministic Finite Automaton):** Multiple transitions from one state on same input; ε-transitions
- **DFA (Deterministic Finite Automaton):** Exactly one transition per state per input; no ε-transitions
- Thompson's construction: regex → NFA
- Subset construction: NFA → DFA (exponential worst case, manageable in practice)
- DFA minimization: Hopcroft's algorithm; produces minimal equivalent DFA

### 2.4 Lexer Generators
- **Flex/Lex:** Define patterns in regex, generate C scanner
- **ANTLR:** Combined lexer/parser generator; generates Java/Python/JavaScript/etc.
- **Hand-written scanners:** Often faster and more flexible; used in production compilers (GCC, Clang, V8)

### 2.5 Practical Example
```
Input:  "if (x >= 42) return x;"
Tokens: [IF, LPAREN, IDENT("x"), GEQ, INT(42), RPAREN, RETURN, IDENT("x"), SEMICOLON]
```

---

## 3. Parsing (Syntax Analysis)

### 3.1 Context-Free Grammars (CFGs)
- Four-tuple: (terminals, non-terminals, production rules, start symbol)
- Derivation: leftmost vs. rightmost
- Parse tree vs. AST (parse tree retains all grammar symbols; AST is simplified)
- Ambiguity: a grammar is ambiguous if a string has multiple parse trees
  - Resolution: operator precedence, associativity rules, grammar rewriting

### 3.2 Top-Down Parsing
- **Recursive Descent:** One function per non-terminal; manual implementation
  - Predictive parsing: choose production based on lookahead token
  - Backtracking variant: try alternatives, undo on failure (less efficient)
- **LL(k) Parsing:** Left-to-right scan, Leftmost derivation, k tokens lookahead
  - LL(1): most practical; requires FIRST and FOLLOW set computation
  - Left recursion elimination and left factoring required for LL grammars
  - LL(1) parse table: rows = non-terminals, columns = terminals

### 3.3 Bottom-Up Parsing
- **Shift-Reduce Parsing:** Build parse tree from leaves to root
  - Shift: push next token onto stack
  - Reduce: replace top of stack with non-terminal per production rule
- **LR(k) Parsing:** Left-to-right scan, Rightmost derivation (in reverse), k lookahead
  - LR(0): simplest; items are productions with a dot position
  - SLR(1): LR(0) items + FOLLOW sets for reduce decisions
  - **LALR(1):** Merge LR(1) states with same core; most practical (yacc/bison use this)
  - **CLR(1):** Full canonical LR; most powerful but largest tables
- **Conflicts:** Shift-reduce and reduce-reduce conflicts indicate grammar ambiguity

### 3.4 PEG (Parsing Expression Grammars)
- Ordered choice (`/`) instead of ambiguous alternation (`|`)
- Always deterministic; no ambiguity by construction
- Packrat parsing: memoize all intermediate results (linear time, linear space)
- Cannot express some CFLs; can express some non-context-free languages

### 3.5 Error Recovery
- Panic mode: skip tokens until a synchronizing token (`;`, `}`)
- Phrase-level: insert/delete/replace tokens to fix locally
- Error productions: add grammar rules for common mistakes

---

## 4. Abstract Syntax Trees (ASTs)

### 4.1 AST Design
- Nodes represent language constructs: expressions, statements, declarations
- Strip syntactic sugar: parentheses, semicolons, commas are not nodes
- Typed nodes: `BinaryExpr(op, left, right)`, `IfStmt(cond, then, else)`, `FnDecl(name, params, body)`

### 4.2 Visitor Pattern
- Separate operations (type checking, code generation) from tree structure
- Each visitor implements methods for each node type
- Enables adding new operations without modifying AST classes
- Alternative: pattern matching (Rust `match`, OCaml `match`)

### 4.3 AST Transformations
- Desugaring: rewrite syntactic sugar into core constructs (e.g., `for` → `while`)
- Macro expansion: expand macros before semantic analysis
- Constant folding at AST level (preliminary optimization)

---

## 5. Semantic Analysis

### 5.1 Symbol Tables
- Map identifiers to their declarations (type, scope, memory location)
- Scope management: stack of scopes; nested scopes shadow outer declarations
- Implementation: hash table per scope, linked list of scopes

### 5.2 Type Checking
- **Static typing:** Types checked at compile time (Java, Rust, Haskell)
- **Dynamic typing:** Types checked at runtime (Python, JavaScript)
- Type rules: each expression has a type derivable from its sub-expressions
- Type compatibility: structural (types match by structure) vs. nominal (types match by name)
- Coercion: implicit type conversion (int → float); widening vs. narrowing

### 5.3 Type Inference
- **Hindley-Milner:** Algorithm W; used in ML, Haskell, Rust (partially)
  - Unification: find substitution that makes two types equal
  - Let-polymorphism: generalize types at `let` bindings
- **Local type inference:** Infer within expressions, require annotations at boundaries (Go, Kotlin, TypeScript)
- Bidirectional type checking: combine checking (push type down) and inference (push type up)

### 5.4 Other Semantic Checks
- Definite assignment: variables must be assigned before use
- Reachability: detect unreachable code
- Exhaustiveness: switch/match must cover all cases
- Lifetime analysis: Rust's borrow checker (ownership, borrowing, lifetimes)

---

## 6. Intermediate Representations (IR)

### 6.1 Levels of IR
- **High-level IR:** Close to source language; retains loops, conditionals, high-level types
- **Mid-level IR:** Language-independent; three-address code, SSA form
- **Low-level IR:** Close to target machine; virtual registers, machine-like instructions

### 6.2 Three-Address Code (TAC)
- Each instruction has at most three operands: `t1 = a + b`
- Forms: `x = y op z`, `x = op y` (unary), `x = y` (copy), `goto L`, `if x goto L`
- Quadruples: (op, arg1, arg2, result) — easy to reorder
- Triples: (op, arg1, arg2) with implicit result numbering — saves space

### 6.3 Static Single Assignment (SSA)
- Every variable is assigned exactly once; new versions for reassignment
- φ (phi) functions at control flow join points: `x₃ = φ(x₁, x₂)`
- Benefits: simplifies many optimizations (dead code elimination, constant propagation)
- Construction: insert φ-functions at dominance frontiers; rename variables
- Used by: LLVM IR, GCC (GIMPLE), HotSpot JIT

### 6.4 LLVM IR
- Typed, SSA-based, infinite virtual registers
- Three forms: human-readable (.ll), bitcode (.bc), in-memory
- Target-independent optimizations run on IR before lowering to machine code
- `clang -emit-llvm -S file.c` to see LLVM IR

---

## 7. Optimization

### 7.1 Local Optimizations (within a basic block)
- **Constant folding:** `3 + 5` → `8` at compile time
- **Constant propagation:** If `x = 5`, replace uses of `x` with `5`
- **Dead code elimination:** Remove code whose result is never used
- **Common subexpression elimination (CSE):** Compute `a + b` once, reuse result
- **Strength reduction:** Replace expensive operations with cheaper ones (`x * 2` → `x << 1`)
- **Algebraic simplification:** `x + 0` → `x`, `x * 1` → `x`

### 7.2 Global Optimizations (across basic blocks)
- **Data flow analysis:** Compute information at each program point
  - Reaching definitions: which assignments reach a given point
  - Live variable analysis: which variables are live (used later) at a point
  - Available expressions: which expressions are already computed
- **Global CSE and constant propagation:** Extend local versions across blocks
- **Copy propagation:** Replace uses of `y` with `x` after `y = x`
- **Dead store elimination:** Remove writes that are never read

### 7.3 Loop Optimizations
- **Loop-invariant code motion (LICM):** Move computations that don't change inside the loop to before it
- **Induction variable elimination:** Replace loop variable arithmetic with simpler updates
- **Loop unrolling:** Duplicate loop body to reduce branch overhead and enable more optimization
- **Loop fusion/fission:** Combine or split loops for better cache behavior
- **Vectorization:** Convert scalar loop operations to SIMD instructions (auto-vectorization)

### 7.4 Interprocedural Optimizations
- **Inlining:** Replace function call with function body; eliminates call overhead, enables further optimization
- **Tail call optimization:** Reuse stack frame for tail-recursive calls
- **Link-time optimization (LTO):** Optimize across translation units at link time
- **Profile-guided optimization (PGO):** Use runtime profiling data to guide optimization decisions

### 7.5 Register Allocation
- Map virtual registers (unbounded) to physical registers (limited)
- **Graph coloring:** Build interference graph (edges = simultaneously live variables); color with k colors (k = registers)
- **Linear scan:** Faster, simpler; used in JIT compilers; process live intervals in order
- Spilling: when not enough registers, store variables on the stack

---

## 8. Code Generation

### 8.1 Instruction Selection
- Pattern matching on IR: map IR operations to target machine instructions
- Tree-pattern matching: tile the expression tree with instruction patterns
- LLVM: TableGen descriptions of target instructions; SelectionDAG or GlobalISel

### 8.2 Instruction Scheduling
- Reorder instructions to minimize pipeline stalls and maximize ILP (instruction-level parallelism)
- Respect data dependencies; software pipelining for loops
- List scheduling: priority-based topological sort of dependency graph

### 8.3 Calling Conventions
- How functions pass arguments and return values: registers vs. stack
- Caller-saved vs. callee-saved registers
- Stack frame layout: return address, saved registers, local variables, arguments
- Platform-specific: System V AMD64 ABI (Linux), Microsoft x64 (Windows)

### 8.4 Object File and Linking
- Object files: code sections (.text), data sections (.data, .bss, .rodata), symbol table, relocation entries
- Linker: resolves symbol references, performs relocations, produces executable
- Static linking: copy library code into executable
- Dynamic linking: resolve at load time or lazily; shared libraries (.so, .dll)

---

## 9. Runtime Systems

### 9.1 Garbage Collection
- **Reference counting:** Increment/decrement counters; immediate reclamation; cycle problem (weak refs or cycle detection)
- **Mark-and-sweep:** Mark reachable objects from roots, sweep unmarked; causes pauses
- **Generational GC:** Most objects die young; separate young/old generations; minor/major collections
- **Concurrent/incremental GC:** Reduce pause times; tri-color marking (white/gray/black)
- **Region-based:** Allocate in regions, free entire region at once (arena allocation)

### 9.2 JIT Compilation
- Compile hot code paths at runtime based on profiling
- Tiered compilation: interpreter → baseline compiler → optimizing compiler
- Speculative optimization: assume types/values based on profiling; deoptimize if assumption violated
- Examples: V8 (Turbofan), HotSpot JVM (C1/C2), PyPy (RPython toolchain)

### 9.3 Memory Layout
- Stack: function frames, local variables, automatically managed
- Heap: dynamically allocated objects, managed by allocator or GC
- Static/global: lifetime of the program
- Virtual memory: each process has its own address space; pages mapped by OS

---

## 10. Practical: Building a Simple Language

### 10.1 Project Outline — "Calc" Language
A minimal expression language with variables, functions, and control flow:
```
let x = 10;
let double = fn(n) { n * 2 };
if (x > 5) { double(x) } else { 0 }
```

### 10.2 Implementation Steps
1. **Lexer:** Hand-written scanner; enumerate token types (LET, IDENT, INT, FN, IF, ELSE, operators)
2. **Parser:** Recursive descent; Pratt parsing for expressions (handles precedence elegantly)
3. **AST:** Define node types; pretty-printer for debugging
4. **Evaluator (tree-walk interpreter):** Recursively evaluate AST nodes; environment for variable bindings
5. **Type checker (optional):** Infer types; report mismatches
6. **Bytecode compiler (optional):** Emit bytecode instructions; stack-based VM to execute
7. **LLVM backend (advanced):** Generate LLVM IR; compile to native code

### 10.3 Recommended Tools
- **Rust:** `logos` (lexer), `chumsky` (parser combinator), `inkwell` (LLVM bindings)
- **Python:** PLY (lex/yacc), Lark (Earley/LALR), `llvmlite` (LLVM)
- **TypeScript:** Hand-written lexer/parser; compile to JavaScript or WASM
- **C:** Flex + Bison (classic); LLVM C API

---

## Key Concepts Summary

1. Compilers are a **pipeline of transformations**: source → tokens → AST → IR → optimized IR → machine code
2. **Lexing uses finite automata**; parsing uses context-free grammars and pushdown automata
3. **SSA form** is the dominant IR for modern optimizers
4. Optimization is about **eliminating redundancy** and **exploiting hardware** (caches, pipelines, SIMD)
5. **Register allocation** is graph coloring — an NP-complete problem solved by heuristics
6. Runtime systems (GC, JIT) are as important as the compiler itself for modern languages

---

## References

- Aho, A., Lam, M., Sethi, R., Ullman, J. *Compilers: Principles, Techniques, and Tools* (2nd ed., 2006) — "The Dragon Book"
- Cooper, K. & Torczon, L. *Engineering a Compiler* (3rd ed., 2022)
- Appel, A. *Modern Compiler Implementation in ML/Java/C* (1998)
- Nystrom, R. *Crafting Interpreters* (2021) — [craftinginterpreters.com](https://craftinginterpreters.com)
- [LLVM Language Reference Manual](https://llvm.org/docs/LangRef.html)
- [Writing a C Compiler (Nora Sandler)](https://norasandler.com/2017/11/29/Write-a-Compiler.html)
