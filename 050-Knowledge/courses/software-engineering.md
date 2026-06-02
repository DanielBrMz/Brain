---
title: "Course: Software Engineering"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, software-engineering, design-patterns, testing]
prerequisites: [programming-fundamentals, data-structures]
---

# Software Engineering

> Back to [[../cs-syllabus|CS Syllabus]] | Related: [[system-design]], [[web-development]], [[security-cryptography]]

## Motivation

Writing code is easy; building software that works, evolves, and can be maintained by a team over years is hard. Software engineering is the discipline of applying systematic, rigorous approaches to the development, operation, and maintenance of software. This course covers the principles, patterns, and practices that distinguish professional software development from ad hoc coding.

## Prerequisites

- Proficiency in at least one programming language (OOP and functional concepts)
- Data structures and algorithms fundamentals
- Basic command-line and development environment familiarity

---

## 1. Design Patterns

### 1.1 Creational Patterns
- **Factory Method:** Define interface for creating objects; subclasses decide which class to instantiate
  - Use when: the exact type of object is determined at runtime
  - Example: `createPaymentProcessor("stripe")` returns StripeProcessor
- **Abstract Factory:** Factory of factories; create families of related objects
  - Use when: system must be independent of how products are created
  - Example: UI toolkit factory producing buttons, dialogs, inputs for a given theme
- **Builder:** Construct complex objects step by step; separate construction from representation
  - Use when: object has many optional parameters or configuration steps
  - Example: `QueryBuilder().select("name").from("users").where("active = true").build()`
- **Singleton:** Ensure a class has only one instance; provide global access point
  - Controversy: often a code smell; makes testing difficult; prefer dependency injection
  - Acceptable uses: logger, configuration, connection pool (but inject them)
- **Prototype:** Clone existing objects instead of creating from scratch
  - Use when: creation is expensive; new instances differ slightly from existing ones

### 1.2 Structural Patterns
- **Adapter:** Convert interface of one class to interface expected by client
  - Example: wrapping a third-party API client to match your internal interface
- **Decorator:** Add behavior to objects dynamically without subclassing
  - Example: `LoggingMiddleware(AuthMiddleware(handler))` — wrapping HTTP handlers
  - Python: `@decorator` syntax; TypeScript: decorators proposal
- **Proxy:** Control access to another object (lazy loading, caching, access control, logging)
  - Example: virtual proxy that loads expensive resource only when accessed
- **Facade:** Simplified interface to a complex subsystem
  - Example: `EmailService.send(to, subject, body)` hiding SMTP, templates, queuing
- **Composite:** Tree structure where individual objects and compositions are treated uniformly
  - Example: file system (files and directories), UI component trees

### 1.3 Behavioral Patterns
- **Observer / Pub-Sub:** Object notifies dependents of state changes
  - Example: event emitters, React state updates, message brokers
  - Push (subject sends data) vs. pull (observers query subject)
- **Strategy:** Define a family of algorithms, encapsulate each, make them interchangeable
  - Example: sorting strategies, pricing algorithms, authentication methods
  - In functional languages: just pass a function
- **Command:** Encapsulate a request as an object; enables undo/redo, queuing, logging
  - Example: text editor commands, transaction objects, job queues
- **State:** Object behavior changes based on internal state (state machine)
  - Example: order states (pending → paid → shipped → delivered)
- **Template Method:** Define algorithm skeleton; subclasses implement specific steps
  - Example: data processing pipeline with customizable transform step
- **Iterator:** Provide sequential access to elements without exposing underlying structure
  - Built into most languages: Python generators, JavaScript iterators, Rust iterators

---

## 2. SOLID Principles

### 2.1 Single Responsibility Principle (SRP)
- A class/module should have one reason to change
- Symptom of violation: class with methods that change for different reasons
- Example: separate `UserRepository` (data access) from `UserService` (business logic) from `UserController` (HTTP handling)

### 2.2 Open/Closed Principle (OCP)
- Open for extension, closed for modification
- Add new behavior by adding new code, not changing existing code
- Implementation: strategy pattern, plugin architecture, polymorphism

### 2.3 Liskov Substitution Principle (LSP)
- Subtypes must be substitutable for their base types without altering correctness
- Classic violation: `Square extends Rectangle` breaks if `setWidth` and `setHeight` are independent
- Behavioral contracts: preconditions cannot be strengthened, postconditions cannot be weakened

### 2.4 Interface Segregation Principle (ISP)
- Clients should not depend on interfaces they don't use
- Prefer many small, focused interfaces over one large interface
- Example: `Readable`, `Writable`, `Seekable` instead of one monolithic `Stream`

### 2.5 Dependency Inversion Principle (DIP)
- High-level modules should not depend on low-level modules; both depend on abstractions
- Dependency injection: pass dependencies in rather than creating them internally
- Enables testability (inject mocks) and flexibility (swap implementations)

---

## 3. Clean Architecture

### 3.1 Layered Architecture
- **Presentation / UI:** HTTP controllers, CLI handlers, view templates
- **Application / Use Cases:** Orchestration logic; coordinates domain objects
- **Domain:** Business logic, entities, value objects, domain events
- **Infrastructure:** Database, external APIs, file system, messaging

### 3.2 Dependency Rule
- Dependencies point inward: infrastructure → application → domain
- Domain has zero dependencies on outer layers
- Use interfaces (ports) at boundaries; implementations (adapters) in outer layers

### 3.3 Hexagonal Architecture (Ports and Adapters)
- Application core defines ports (interfaces) for what it needs
- Adapters implement ports: database adapter, HTTP adapter, message queue adapter
- Enables swapping infrastructure without touching business logic
- Testing: use in-memory adapters for fast tests

### 3.4 Domain-Driven Design (DDD) Concepts
- **Entities:** Objects with identity (User, Order)
- **Value Objects:** Immutable, defined by attributes (Money, DateRange, EmailAddress)
- **Aggregates:** Cluster of entities treated as a unit; aggregate root enforces invariants
- **Repositories:** Abstraction over data access for aggregates
- **Domain Events:** Record of something significant that happened (OrderPlaced, PaymentReceived)
- **Bounded Contexts:** Explicit boundary within which a model applies

---

## 4. Testing

### 4.1 Test Pyramid
```
        /  E2E  \        Few, slow, brittle
       /----------\
      / Integration \    Some, moderate speed
     /----------------\
    /    Unit Tests     \  Many, fast, isolated
```

### 4.2 Unit Testing
- Test individual functions/methods in isolation
- Fast (milliseconds), deterministic, no external dependencies
- Arrange → Act → Assert pattern
- One assertion per test (generally); test one behavior per test
- Naming: `test_should_return_total_when_items_in_cart` or `it("returns total for cart items")`

### 4.3 Integration Testing
- Test interactions between components (service + database, API + queue)
- Requires setup/teardown of external resources (test database, Docker containers)
- Slower than unit tests; run in CI, not on every save
- Testcontainers: spin up Docker containers for databases, Redis, Kafka in tests

### 4.4 End-to-End (E2E) Testing
- Test entire application from user perspective (browser automation)
- Tools: Cypress, Playwright, Selenium
- Flaky by nature: network, timing, rendering issues
- Write few but critical path tests (login, checkout, core flows)

### 4.5 Test-Driven Development (TDD)
- Red → Green → Refactor cycle
- Write a failing test → write minimal code to pass → refactor
- Benefits: drives design, ensures coverage, documents behavior
- Not dogma: skip for exploratory/prototype code; apply where it adds value

### 4.6 Mocking and Test Doubles
- **Stub:** Returns predetermined values; no behavior verification
- **Mock:** Records calls; verifies interactions (called with correct args, correct number of times)
- **Fake:** Working implementation with shortcuts (in-memory database)
- **Spy:** Wraps real object; records calls but delegates to real implementation
- Over-mocking: tests become coupled to implementation details; prefer fakes and integration tests

### 4.7 Property-Based Testing
- Generate random inputs and verify properties hold for all inputs
- Example: `for all lists xs: sort(sort(xs)) == sort(xs)` (idempotence)
- Tools: Hypothesis (Python), fast-check (TypeScript), QuickCheck (Haskell), proptest (Rust)
- Finds edge cases that example-based tests miss

---

## 5. Version Control (Git)

### 5.1 Git Internals
- Content-addressable storage: objects identified by SHA-1 hash
- Object types: blob (file content), tree (directory), commit (snapshot + metadata), tag
- Refs: branches are pointers to commits; HEAD points to current branch
- Packfiles: delta compression for storage efficiency

### 5.2 Branching Strategies
- **Git Flow:** main, develop, feature/*, release/*, hotfix/* — heavyweight, suited for versioned releases
- **GitHub Flow:** main + feature branches + PRs — simple, suited for continuous deployment
- **Trunk-Based Development:** Short-lived branches (< 1 day); merge to main frequently; feature flags for WIP
  - Preferred by high-performing teams (DORA research); enables CI/CD

### 5.3 Rebasing vs. Merging
- **Merge:** Creates merge commit; preserves branch history; safe for shared branches
- **Rebase:** Replays commits on top of target; linear history; never rebase shared branches
- **Squash merge:** Combine all branch commits into one; clean main history; loses individual commits
- Interactive rebase: reorder, squash, edit, drop commits (powerful but dangerous on shared history)

### 5.4 Best Practices
- Commit messages: imperative mood, 50-char subject, blank line, body explaining "why"
- Atomic commits: each commit is a single logical change that compiles and passes tests
- `.gitignore`: ignore build artifacts, dependencies, secrets, IDE files
- Signed commits: GPG/SSH signatures for authenticity

---

## 6. Code Review

### 6.1 Purpose
- Catch bugs, improve design, share knowledge, ensure consistency
- Not gatekeeping — collaborative improvement

### 6.2 What to Review
- Correctness: does it do what it's supposed to?
- Design: is it the right approach? Does it fit the architecture?
- Readability: will the next person understand this?
- Tests: are they meaningful? Do they cover edge cases?
- Security: input validation, authorization checks, secret handling
- Performance: obvious bottlenecks, N+1 queries, unnecessary allocations

### 6.3 Best Practices
- Keep PRs small (< 400 lines of meaningful change)
- Review within 24 hours; unblock teammates
- Be specific and constructive: suggest alternatives, explain reasoning
- Distinguish blocking (must fix) from non-blocking (nit, suggestion)
- Approve with comments when minor issues don't warrant another round

---

## 7. CI/CD Pipelines

### 7.1 Continuous Integration (CI)
- Merge code frequently (at least daily); every merge triggers automated build and tests
- Pipeline stages: lint → type check → unit tests → integration tests → build
- Fast feedback: pipeline should complete in < 10 minutes for core checks
- Tools: GitHub Actions, GitLab CI, Jenkins, CircleCI

### 7.2 Continuous Delivery (CD)
- Every commit that passes CI is deployable to production
- Deployment is a business decision, not a technical one
- Requires: comprehensive tests, feature flags, rollback capability

### 7.3 Continuous Deployment
- Every passing commit is automatically deployed to production
- Requires: high confidence in test suite, monitoring, fast rollback
- Canary deployments, blue-green deployments, rolling updates

### 7.4 Pipeline Design
```yaml
# Example GitHub Actions pipeline
jobs:
  lint:
    - eslint, prettier, type-check
  test:
    - unit tests (parallel)
    - integration tests (with test containers)
  build:
    - production build
    - docker image
  deploy:
    - staging (automatic)
    - production (manual approval or automatic)
```

### 7.5 Infrastructure as Code
- Terraform, Pulumi, CloudFormation: define infrastructure in version-controlled code
- GitOps: infrastructure changes via PRs; reconciliation loop (ArgoCD, Flux)

---

## 8. Agile and Process

### 8.1 Scrum
- Roles: Product Owner, Scrum Master, Developers
- Ceremonies: Sprint Planning, Daily Standup, Sprint Review, Retrospective
- Artifacts: Product Backlog, Sprint Backlog, Increment
- Sprints: 1-4 weeks (2 weeks most common)

### 8.2 Kanban
- Visualize workflow; limit work in progress (WIP limits)
- No fixed iterations; continuous flow
- Metrics: cycle time, throughput, lead time

### 8.3 What Actually Matters
- Ship frequently; get feedback early
- Reduce batch size (smaller PRs, smaller features, more frequent deployments)
- Measure lead time (idea → production) and deployment frequency
- Retrospectives: continuous improvement is the only constant

---

## 9. Technical Debt and Refactoring

### 9.1 Technical Debt
- Intentional shortcuts for speed vs. unintentional debt from ignorance
- Interest: debt slows future development; compound effect
- Managing: make debt visible (document, track), pay down incrementally, boy scout rule

### 9.2 Refactoring Patterns
- **Extract Method:** Pull code into a named method for clarity
- **Extract Class:** Split a class that has too many responsibilities
- **Rename:** Names matter; rename when understanding improves
- **Replace Conditional with Polymorphism:** Eliminate type-checking conditionals
- **Introduce Parameter Object:** Group related parameters into a single object
- **Move Method:** Move method to the class that has the data it needs
- **Replace Magic Number with Constant:** Named constants are self-documenting

### 9.3 When to Refactor
- Before adding a feature (make the change easy, then make the easy change)
- When fixing a bug (understand the code, improve it, fix the bug)
- During code review (suggest improvements)
- NOT as a separate project (refactoring should be continuous, not a rewrite)

---

## 10. Documentation

### 10.1 Architecture Decision Records (ADRs)
- Record why decisions were made (not just what was decided)
- Format: Title, Status (proposed/accepted/deprecated), Context, Decision, Consequences
- Store in repository (`docs/adr/`)
- Invaluable for onboarding and understanding historical decisions

### 10.2 API Documentation
- OpenAPI / Swagger for REST APIs; auto-generate from code or code from spec
- GraphQL: self-documenting via introspection; add descriptions to schema
- Examples > descriptions: show complete request/response pairs

### 10.3 Code Documentation
- Code should be self-documenting (good names, clear structure)
- Comments explain "why", not "what" — the code explains "what"
- Docstrings for public APIs: parameters, return values, exceptions, examples
- Architecture diagrams: C4 model (Context, Container, Component, Code)

---

## Key Concepts Summary

1. **Design patterns** are vocabulary, not prescriptions — know them, apply judiciously
2. **SOLID** guides class/module design toward flexibility and testability
3. **Test pyramid:** Many unit tests, some integration tests, few E2E tests
4. **Trunk-based development** with feature flags enables rapid, safe delivery
5. **CI/CD** is not optional — automate everything from lint to deploy
6. **Small PRs, fast reviews** — the highest-leverage process improvement
7. **Refactor continuously** — never let debt compound without a plan

---

## References

- Gamma, E., Helm, R., Johnson, R., Vlissides, J. *Design Patterns* (1994) — "Gang of Four"
- Martin, R.C. *Clean Code* (2008) and *Clean Architecture* (2017)
- Fowler, M. *Refactoring* (2nd ed., 2018)
- Beck, K. *Test-Driven Development: By Example* (2002)
- Forsgren, N., Humble, J., Kim, G. *Accelerate* (2018) — DORA research
- [Conventional Commits](https://www.conventionalcommits.org/)
- [C4 Model](https://c4model.com/) — architecture diagramming
- Evans, E. *Domain-Driven Design* (2003)
