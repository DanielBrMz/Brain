---
title: "Course: Web Development"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, web-development, frontend, backend, react, nextjs]
prerequisites: [computer-networks, programming-fundamentals, software-engineering]
---

# Web Development

> Back to [[../cs-syllabus|CS Syllabus]] | Related: [[system-design]], [[security-cryptography]], [[software-engineering]], [[computer-networks]]

## Motivation

The web is the universal platform. From SPAs to server-rendered applications, from REST APIs to real-time collaboration tools, web technologies power the majority of modern software. This course covers the full stack — frontend frameworks, backend services, APIs, and the patterns that connect them. It emphasizes the technologies most relevant to modern production systems: React, Next.js, TypeScript, Flask, FastAPI, and GraphQL.

## Prerequisites

- HTML, CSS, and JavaScript fundamentals
- HTTP protocol basics (methods, status codes, headers)
- Basic understanding of client-server architecture
- Programming fundamentals (functions, data structures, async/await)

---

## 1. TypeScript

### 1.1 Type System Fundamentals
- Static types checked at compile time; erased at runtime
- Primitive types: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`
- `any` (escape hatch — avoid), `unknown` (safe alternative — requires narrowing), `never` (impossible values)
- Type annotations vs. type inference: TypeScript infers most types; annotate function signatures and exports

### 1.2 Advanced Types
- **Union types:** `string | number` — value can be either type; use narrowing to distinguish
- **Intersection types:** `A & B` — value has all properties of both types
- **Literal types:** `"success" | "error"` — exact values as types
- **Discriminated unions:** Union of objects with a common literal field for type narrowing
  ```typescript
  type Result = { status: "ok"; data: User } | { status: "error"; message: string };
  ```
- **Generics:** Parameterize types: `function identity<T>(x: T): T { return x; }`
  - Constraints: `<T extends HasId>` — restrict generic to types with specific shape
  - Default type parameters: `<T = string>`

### 1.3 Utility Types
- `Partial<T>`, `Required<T>`, `Readonly<T>` — modify property modifiers
- `Pick<T, K>`, `Omit<T, K>` — select/exclude properties
- `Record<K, V>` — object type with keys K and values V
- `ReturnType<T>`, `Parameters<T>` — extract types from functions
- `Awaited<T>` — unwrap Promise types
- Template literal types: `` type Route = `/api/${string}` ``

### 1.4 Type Guards and Narrowing
- `typeof`, `instanceof`, `in` operator
- Custom type guards: `function isUser(x: unknown): x is User`
- Exhaustive checking with `never`: switch statements that must handle all cases
- `satisfies` operator: validate type without widening

---

## 2. React

### 2.1 Core Concepts
- Components: functions that return JSX (class components are legacy)
- JSX: syntactic sugar for `React.createElement`; auto-escapes strings (XSS protection)
- Props: immutable inputs; children as special prop
- One-way data flow: parent → child via props; child → parent via callback props

### 2.2 Hooks
- **useState:** Local component state; triggers re-render on update
  - Updater function pattern: `setState(prev => prev + 1)` for state depending on previous
- **useEffect:** Side effects (data fetching, subscriptions, DOM manipulation)
  - Dependency array: `[]` = mount only; `[dep]` = when dep changes; omitted = every render
  - Cleanup function: returned from effect; runs before next effect and on unmount
- **useRef:** Mutable reference that persists across renders; no re-render on change
  - DOM refs: `<input ref={inputRef} />`; `inputRef.current.focus()`
- **useMemo:** Memoize expensive computations; recompute only when dependencies change
- **useCallback:** Memoize functions; prevent unnecessary re-renders of children receiving the function
- **useReducer:** Complex state logic; `(state, action) => newState`; alternative to multiple useState
- **useContext:** Access context value without prop drilling

### 2.3 Context API
- `createContext` → `Provider` (wraps tree) → `useContext` (consumes value)
- Use for: theme, locale, authentication state — things that rarely change
- Avoid for: frequently changing state (every consumer re-renders on any context change)
- Optimization: split contexts, memoize provider value

### 2.4 Suspense and Concurrent Features
- `<Suspense fallback={<Loading />}>` — show fallback while children load
- React.lazy: code-split components; load on demand
- `useTransition`: mark state updates as non-urgent; keep UI responsive
- `useDeferredValue`: defer re-rendering expensive components
- Server Components: render on server, stream to client (see Next.js section)

### 2.5 Performance Optimization
- `React.memo`: skip re-render if props haven't changed (shallow comparison)
- Virtualization: render only visible items in long lists (react-window, tanstack-virtual)
- Code splitting: `React.lazy` + `Suspense`; route-based splitting
- Profile with React DevTools Profiler; identify unnecessary re-renders

---

## 3. Next.js

### 3.1 App Router (Next.js 13+)
- File-based routing: `app/page.tsx` → `/`, `app/about/page.tsx` → `/about`
- Layouts: `layout.tsx` wraps child routes; persists across navigation (no re-mount)
- Loading states: `loading.tsx` — automatic Suspense boundary
- Error handling: `error.tsx` — error boundary per route segment
- Route groups: `(auth)/login/page.tsx` — organize without affecting URL
- Dynamic routes: `[id]/page.tsx`; catch-all: `[...slug]/page.tsx`

### 3.2 Server Components vs. Client Components
- **Server Components** (default): render on server; no JavaScript sent to client
  - Can: access database directly, read files, use secrets
  - Cannot: use hooks, browser APIs, event handlers
  - Benefit: smaller bundle, faster initial load, SEO
- **Client Components:** `"use client"` directive at top of file
  - Can: use hooks, interactivity, browser APIs
  - Strategy: push `"use client"` as far down the tree as possible
- Composition: server components can import client components (not vice versa); pass server data as props

### 3.3 Data Fetching
- **Server Components:** `async` components; `await fetch()` directly in component body
- **Server Actions:** `"use server"` functions; called from client via form actions or `startTransition`
  - Replace API routes for mutations; type-safe, progressive enhancement
- **Route Handlers:** `app/api/route.ts` — traditional API endpoints when needed
- Caching: `fetch` extended with `{ next: { revalidate: 60 } }` (ISR) or `{ cache: "no-store" }` (dynamic)

### 3.4 Rendering Strategies
- **SSR (Server-Side Rendering):** Render on every request; `{ cache: "no-store" }` or dynamic functions
- **SSG (Static Site Generation):** Render at build time; `generateStaticParams()` for dynamic routes
- **ISR (Incremental Static Regeneration):** Static with time-based revalidation
- **Streaming:** Server sends HTML progressively; Suspense boundaries define streaming units
- **PPR (Partial Pre-rendering):** Static shell + dynamic holes filled via streaming (experimental)

### 3.5 Middleware
- `middleware.ts` at project root; runs before every request
- Use cases: authentication redirects, geo-routing, A/B testing, request rewriting
- Runs on Edge Runtime: lightweight, fast, limited API surface
- Matcher config: specify which routes trigger middleware

---

## 4. State Management

### 4.1 Zustand
- Minimal, hook-based state management
- Create store: `create((set) => ({ count: 0, increment: () => set(s => ({ count: s.count + 1 })) }))`
- Select specific state to avoid unnecessary re-renders: `useStore(s => s.count)`
- Middleware: `persist` (localStorage), `devtools`, `immer` (mutable updates)
- No providers needed; works outside React (testing, SSR)

### 4.2 Redux / Redux Toolkit
- Single store, unidirectional data flow, reducers, actions
- Redux Toolkit: `createSlice`, `createAsyncThunk`, `configureStore` — reduces boilerplate
- When to use: large applications with complex, interrelated state
- Often overkill for most applications; Zustand or Context suffice

### 4.3 React Query / TanStack Query
- Server state management: caching, background refetching, stale-while-revalidate
- `useQuery`: declarative data fetching with automatic caching and retry
- `useMutation`: mutations with optimistic updates and cache invalidation
- Solves: loading states, error states, deduplication, pagination, infinite scroll
- Increasingly less needed with Next.js Server Components (data fetched on server)

---

## 5. Styling

### 5.1 Tailwind CSS
- Utility-first: `className="flex items-center gap-4 rounded-lg bg-white p-4 shadow"`
- Design system built-in: spacing scale, color palette, typography, breakpoints
- Responsive: `md:flex-row` — mobile-first breakpoints
- Dark mode: `dark:bg-gray-900` with class or media strategy
- Customization: `tailwind.config.js` — extend theme, add plugins
- `@apply` for extracting component classes (use sparingly)

### 5.2 CSS Modules
- Scoped CSS: `import styles from './Button.module.css'`; `className={styles.primary}`
- No global conflicts; composes for reuse
- Works natively with Next.js

### 5.3 Component Libraries
- **shadcn/ui:** Copy-paste components (not a dependency); Radix UI primitives + Tailwind styling
  - Customizable: you own the code; modify freely
  - Components: Button, Dialog, Sheet, Dropdown, Toast, Form, DataTable
- **Radix UI:** Unstyled, accessible primitives (Dialog, Popover, Select, Tooltip)
- **Headless UI:** Similar to Radix; from Tailwind Labs

---

## 6. Build Tools and Testing

### 6.1 Build Tools
- **Vite:** Fast dev server (ESM-based HMR), Rollup for production builds
- **Turbopack:** Rust-based bundler for Next.js; successor to Webpack
- **Bun:** JavaScript runtime + bundler + package manager + test runner
- **esbuild:** Extremely fast transpiler/bundler (Go-based); often used internally by other tools

### 6.2 Frontend Testing
- **Jest / Vitest:** Unit testing; Vitest is Vite-native, faster, compatible API
- **React Testing Library:** Test components by user behavior, not implementation details
  - `render`, `screen.getByRole`, `userEvent.click` — query by accessibility roles
- **Cypress:** E2E testing; runs in real browser; time-travel debugging
  - `cy.visit("/login")`, `cy.get("[data-cy=email]").type("...")`, `cy.contains("Dashboard")`
- **Playwright:** E2E testing; multi-browser (Chromium, Firefox, WebKit); faster than Cypress
  - Auto-waiting, parallel execution, trace viewer

---

## 7. Backend: Flask

### 7.1 Core Concepts
- WSGI micro-framework; explicit and minimal
- Application factory pattern: `create_app()` function for configuration
- Blueprints: modular route grouping; register with app
- Request context: `request`, `g`, `session` — thread-local proxies

### 7.2 Extensions
- **Flask-SQLAlchemy:** ORM integration; models as classes, migrations via Alembic
- **Flask-JWT-Extended:** JWT authentication; token creation, refresh, blacklisting
- **Flask-CORS:** Cross-origin resource sharing configuration
- **Flask-Caching:** Response caching with Redis/Memcached backends
- **Flask-RESTful / Flask-RESTX:** REST API structure with Swagger docs

### 7.3 GraphQL with Graphene
- Schema-first or code-first with Graphene (Python GraphQL library)
- `ObjectType` classes map to GraphQL types
- Resolvers: methods on ObjectType that fetch data
- Mutations: modify data; input types for structured arguments
- DataLoader: batch and cache database queries to solve N+1 problem
- Integration: `flask-graphql` provides `/graphql` endpoint

### 7.4 Production Deployment
- WSGI server: Gunicorn with multiple workers (sync or gevent)
- Reverse proxy: Nginx for static files, SSL termination, load balancing
- Docker: multi-stage builds; slim Python base images
- Configuration: environment-based config classes (dev, qa, uat, prod)

---

## 8. Backend: FastAPI

### 8.1 Core Concepts
- ASGI framework; async by default; built on Starlette + Pydantic
- Path operations: `@app.get("/items/{item_id}")` with type hints
- Automatic OpenAPI documentation (Swagger UI + ReDoc)

### 8.2 Pydantic Models
- Data validation and serialization via type annotations
- `BaseModel` for request/response schemas; automatic validation
- Field validators, computed fields, model inheritance
- `model_dump()`, `model_validate()` for serialization/deserialization

### 8.3 Dependency Injection
- `Depends()` function: declare dependencies in path operation signatures
- Use for: database sessions, authentication, rate limiting, permissions
- Hierarchical: dependencies can have their own dependencies
- Scoped: per-request lifecycle management

### 8.4 Async Support
- Native `async/await`; use `async def` for I/O-bound operations
- `asyncpg` for async PostgreSQL; `aiohttp` for async HTTP clients
- Background tasks: `BackgroundTasks` for fire-and-forget operations

---

## 9. Backend: Express / Node.js

### 9.1 Core Concepts
- Minimal Node.js framework; middleware-based request pipeline
- `app.use()` for middleware; `app.get/post/put/delete()` for routes
- Middleware pattern: `(req, res, next) => { /* ... */ next(); }`
- Error handling middleware: `(err, req, res, next) => { /* ... */ }`

### 9.2 Modern Alternatives
- **Hono:** Ultra-fast, multi-runtime (Node, Deno, Bun, Cloudflare Workers); Web Standard APIs
- **Fastify:** Schema-based validation, plugin architecture, faster than Express
- **tRPC:** End-to-end type safety; define procedures on server, call from client with full type inference
  - Router → Procedure → Context → Middleware chain
  - Client: `trpc.user.getById.useQuery({ id: 1 })` — fully typed
  - Eliminates API contract drift between frontend and backend

---

## 10. GraphQL

### 10.1 Schema Design
- Type system: scalar, object, enum, interface, union, input types
- Schema-first (SDL) vs. code-first (Graphene, TypeGraphQL, Nexus)
- Nullability: fields are nullable by default; `!` marks non-null
- Connections pattern for pagination: `edges { node, cursor }`, `pageInfo { hasNextPage, endCursor }`

### 10.2 Resolvers
- Function that returns data for a field
- Resolver chain: parent → field → child field resolution
- Context: shared per-request data (authenticated user, data loaders, database connection)

### 10.3 DataLoader
- Batches multiple individual database queries into a single query
- Per-request caching: avoids fetching the same entity twice
- Solves the N+1 problem inherent in nested GraphQL queries
- Pattern: collect IDs during resolution phase, batch-fetch in single query

### 10.4 Subscriptions
- Real-time data via WebSocket (graphql-ws protocol)
- Server pushes updates to subscribed clients
- Use cases: chat messages, live notifications, real-time dashboards

---

## 11. Full-Stack Patterns

### 11.1 Authentication Flows
- **Session-based:** Server stores session; client sends session ID cookie
- **JWT-based:** Stateless token; access token (short-lived) + refresh token (httpOnly cookie)
- **OAuth2 + OIDC:** Delegate to identity provider; receive tokens
- **Better-Auth / NextAuth:** Library-level abstraction over OAuth, credentials, magic links

### 11.2 PWA (Progressive Web App)
- Service worker: intercepts network requests; offline caching; background sync
- Web App Manifest: `manifest.json` — app name, icons, theme, display mode
- Installable: "Add to Home Screen" on mobile
- Cache strategies: cache-first, network-first, stale-while-revalidate

### 11.3 WebSockets
- Full-duplex communication; persistent connection
- Use cases: real-time chat, live updates, collaborative editing
- Libraries: Socket.IO (with fallbacks), `ws` (Node.js), native `WebSocket` API
- Scaling: sticky sessions or external pub/sub (Redis) for multi-server

### 11.4 tRPC
- End-to-end type safety from database to UI
- No code generation; types flow through TypeScript inference
- Router composition: merge routers for modular API
- Works seamlessly with Next.js App Router and React Query

---

## Key Concepts Summary

1. **TypeScript** is non-negotiable for professional web development; discriminated unions and generics are essential
2. **Server Components** (Next.js) reduce client JavaScript; use `"use client"` only for interactivity
3. **Server Actions** replace API routes for mutations; progressive enhancement built-in
4. **Zustand** for client state, **React Query** for server state (or Server Components)
5. **GraphQL + DataLoader** solves flexible querying but adds complexity; tRPC is simpler for same-team full-stack
6. **Tailwind + shadcn/ui** is the dominant styling approach for rapid, consistent UI development
7. Test behavior, not implementation; **React Testing Library** + **Playwright** for comprehensive coverage

---

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [tRPC Documentation](https://trpc.io/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GraphQL Specification](https://spec.graphql.org/)
- [Zustand GitHub](https://github.com/pmndrs/zustand)
- Dodds, K.C. [Testing JavaScript](https://testingjavascript.com/)
