---
title: "Local Project File Structures"
type: reference
created: 2026-03-22
updated: 2026-03-22
tags: [projects, file-structure, reference, local]
---

# Local Project File Structures

Complete file-level documentation of all local projects under `~/Documents/Projects/`.

---

## Discovered Project Directories

```
~/Documents/Projects/
├── Personal/
│   ├── webapp/                    # Sidepocket frontend PWA
│   ├── nextblog/                  # Blog platform (completed)
│   ├── sp-backend-api-testing/    # Cypress API test harness
│   └── sp-endorser-cms/           # Endorser CMS (Payload CMS)
├── HackHarvard2025/
│   ├── frontend/                  # Boston Energy Insights dashboard
│   └── backend/                   # Flask + FastAPI microservices
├── Sidepocket/
│   ├── Test/sp-endorser-cms/      # Duplicate/test clone of endorser CMS
│   ├── sp-endorser-cms/           # Another clone of endorser CMS
│   └── hello.txt                  # Placeholder file
└── College/
    ├── oracle-todo-app/           # Oracle Cloud todo app (Spring Boot + React)
    └── TC3005B/M6/
        ├── game-hub/              # React game hub app
        └── online-store/          # React online store app
```

**NOTE:** `sp-app/` (Sidepocket backend) is referenced in CLAUDE.md but was NOT found under `~/Documents/Projects/Personal/`. It may have been removed or is accessed only via SSH.

---

## 1. webapp (Sidepocket Frontend)

**Path:** `/home/brmz/Documents/Projects/Personal/webapp/`
**Stack:** Next.js 15.5.7, React 19, TypeScript 5.5, Bun, tRPC 10, Zustand 4, Tailwind 3, PWA
**Package manager:** Bun (v1.0.31)
**Purpose:** Sidepocket investment platform PWA frontend

### Root Config Files

| File | Purpose |
|------|---------|
| `package.json` | Dependencies, scripts (`bun run dev`, `bun run build`) |
| `next.config.mjs` | PWA config (workbox), image domains, webpack externals, custom headers |
| `.eslintrc.cjs` | ESLint config (Airbnb TypeScript + Prettier) |
| `postcss.config.cjs` | PostCSS with autoprefixer |
| `prettier.config.mjs` | Prettier formatting rules |
| `tailwind.config.ts` | Tailwind theme, custom animations |
| `tsconfig.json` | TypeScript config |
| `src/env.mjs` | Environment variable validation (t3-env) |

### Route Structure (`src/app/`)

#### Auth Route Group `(AuthPages)/`
- `(InitialForm)/InitialForm/` -- Initial user onboarding questionnaire
  - `DOB/`, `EnterCode/`, `IntroFormBackup/`, `InvestingExperience/`, `InvestmentGoal/`, `LiquidNetWorth/`, `LiquidityNeeds/`, `Name/`, `NetWorth/`, `PhoneNumber/`, `TimeHorizon/` -- each with `layout.tsx`, some with `page.tsx`
- `(LoginPages)/`
  - `(CreateUserFlow)/IntroForm/` -- New user intro form
  - `(SigninSignup)/Signin/`, `Signup/` -- Authentication pages
- `InitialSupport/` -- Support during initial flow

#### Dashboard Route Group `(Dashboard)/`
- `Dashboard/`
  - `(Settings)/Settings/Accounts/`, `Security/` -- Account and security settings
  - `AccountValue/` -- Portfolio value display
  - `Details/`, `Details/MySidepockets/` -- Sidepocket details views
  - `Funding/` -- Deposit/withdrawal funding
  - `Invest/` -- Investment marketplace
  - `Premier/` -- Premium tier features
- `InvestigationCategories/types.ts` -- Investigation category type definitions
- `layout.tsx` -- Dashboard-wide layout with sidebar

#### Endorser Route Group `(Endorser)/`
- `(AuthPages)/endorser/[endorserName]/`
  - `EmailVerification/`, `Signin/`, `Signup/` -- Per-endorser auth flows

#### Fund Sidepocket Route Group `(FundSidepocket)/`
- `ConfirmTransaction/` -- Transaction confirmation page

#### Standalone Routes
- `AccountStatus/` -- Account status/CIP issues
- `FundingSchedule/` -- Recurring deposit schedule
- `Onboarding/(OnboardingForm)/` -- Full account onboarding (35+ form steps):
  - `AccountSummary`, `AccountType`, `AddBeneficiaries`, `AddBeneficiary`, `Address`, `AnnualIncome`, `BeneficiaryAddress`, `BeneficiaryAllocation`, `BeneficiaryDOB`, `BeneficiaryRelationship`, `BeneficiarySSN`, `BrokerageAccount`, `Citizenship`, `ConfirmAddress`, `ConfirmBeneficiaryAddress`, `ConfirmSSN`, `ConflictDisclosure`, `CountryCitizenship`, `CurrentVisa`, `EmployerInfo`, `EmploymentStatus`, `EstateAllocation`, `Inconvenience`, `InvestingExperience`, `InvestmentGoal`, `IraDistribution`, `LiquidNetWorth`, `LiquidityNeeds`, `NativeCountry`, `NetWorth`, `PositionInfo`, `ProvideTrustedContact`, `RetirementAccount`, `RiskTolerance`, `SelectTaxWithholding`, `TaxFillingStatus`, `TaxWithholding`, `TimeHorizon`, `TrustedContact`, `VerifyIdentity`, `VisaExpiration`
- `Support/` -- Support page
- `Transaction/` -- Transaction flow (`TransactionStatus/`, `TransferFrom/`, `TransferTo/`)

#### API Routes (`src/app/api/`)
- `check-session/route.ts` -- Session validation endpoint
- `subscription-check/route.ts` -- Subscription fee acceptance check
- `profile-check/route.ts` -- Profile onboarding status check
- `trpc/[trpc]/route.ts` -- tRPC API handler

### Middleware (`src/middleware.ts`)
Complex authentication/routing middleware that:
- Validates sessions via internal API calls
- Handles logout race conditions
- Enforces subscription fee acceptance
- Guards onboarding flow (redirects incomplete profiles)
- Blocks duplicate account creation (brokerage, IRA)
- Allows public pages, static assets, service worker files

### Server (`src/server/`)

#### tRPC Setup
- `api/trpc.ts` -- tRPC context and procedure definitions
- `api/root.ts` -- Root router combining all sub-routers
- `spApi.ts` -- Base Sidepocket API client

#### tRPC Routers (`src/server/api/routers/`)
| Router | Purpose |
|--------|---------|
| `account.ts` | Account management queries/mutations |
| `app.ts` | App-level queries (market, sidepockets) |
| `auth.ts` | Authentication operations |
| `cash.ts` | Cash transfers, deposits, withdrawals |
| `cms.ts` | CMS content queries |
| `cookies.ts` | Cookie management |
| `notifications.ts` | Push notification management |
| `plaid.ts` | Plaid bank linking integration |
| `portfolio.ts` | Portfolio and sidepocket operations |
| `example.ts`, `staticExample.ts` | Template/example routers |

#### Service Layer (`src/server/api/services/`)
| Service | Purpose |
|---------|---------|
| `accountService.ts` | Account API calls |
| `authService.ts` | Auth API calls |
| `cashService.ts` | Cash transfer API calls |
| `cmsService.ts` | CMS content fetching |
| `cookieService.ts` | Session cookie management |
| `depositService.ts` | Deposit operations |
| `documentService.ts` | Document management |
| `holdingService.ts` | Portfolio holdings data |
| `lookUpService.ts` | Lookup/reference data |
| `marketService.ts` | Market data (indices, hours) |
| `notificationService.ts` | Push notification service |
| `onboardingService.ts` | Onboarding flow API calls |
| `plaidService.ts` | Plaid integration service |
| `pushNotificationService.ts` | Web push notifications |
| `sidepocketService.ts` | Core sidepocket operations |
| `userService.ts` | User profile management |

#### Server Actions (`src/server/actions/`)
- `authActions.ts` -- Authentication server actions
- `forgotPasswordActions.ts` -- Password reset flow
- `oneTimeTransactionActions.ts` -- One-time transaction processing

### Components (`src/components/`)
| Directory | Key Components |
|-----------|----------------|
| `AccountValue/` | `ChartHeader.tsx` -- Portfolio chart header |
| `Auth/` | `GeneralInput`, `PasswordInput`, `LogoutButton`, `AuthFooter`, `PasswordRequirements`, `EnhancedPasswordInput`, `EnhancedGeneralInput`, `BigButtonNew`, `InvalidEndorser`, `ChangePasswordIssues`, `RedLogoutButton` |
| `Dashboard/` | `BottomNav`, `SideNavigation`, `WebLeftSidebar`, `MobileSidebar`, `ProfileButton`, `NotificationButton`, `SearchInput`, `InvestBanner`, `PlaidWrapper`, `SidepocketInfo`, `Sidepockets`, `StockInfo`, `Spreadsheet`, `SpreadsheetSearch`, `USMarket`, `ChecklistFlow`, `DesktopMessage`, `InvestFilterModal`, `InvestSortModal`, `IraContributionModal`, `ProSidepocketModal`, `SidepocketPendingModal`, `SessionStorageIndicator`, `TooltipFAQ`, `AdvertisementCarousel`, `PositionsAndBreakdown`, `TransferButton`, `TabButton`, `ThemeButton` |
| `Details/` | `DonutChart`, `Overview`, `FundButton`, `PendingButton`, `PendingButtonCard`, `AccountPending` |
| `EnhancedInputs/` | `EnhancedDateInput`, `EnhancedMoneyInput`, `EnhancedPercentageInput`, `EnhancedSSNInput`, `EnhancedTextInput`, `EnhancedPhoneInput` |
| `Endorsers/` | `Tooltip`, `MediaPlayer`, `TooltipModal` |
| `FundSidepocket/` | `SidepocketButton`, `DeleteSPButton`, `DeleteSPModal`, `SignUpIssues` |
| `FundingSchedule/` | `FundingScheduleActionButton`, `FundingButton`, `CalendarModal`, `AmounInput`, `NoSidepocketsLink` |
| `Icons/` | `PortfolioIcon`, `SettingsIcon`, `AccountsIcon`, `FundingIcon`, `InvestIcon`, `BellEmptyIcon` |
| `Shared/` | `ChartSkeleton`, `LoadingSkeleton`, `PostHogPageView` |
| `Transactions/` | `ProgressMarker`, `GrayLine` |
| `ui/` | `form`, `input`, `label`, `progress` (Radix-based primitives) |

### Hooks (`src/hooks/`)
| Hook | Purpose |
|------|---------|
| `useSignupSubmit.ts` | Signup form submission logic |
| `useLoginSubmit.ts` | Login form submission logic |
| `useInsight.ts` | Insight/tooltip content |
| `useOptimisticValueStatus.ts` | Optimistic UI for value updates |
| `useProfileUpdate.ts` | Profile update operations |
| `useSessionTimeout.tsx` | Session timeout detection |
| `useAutoLoginAfterVerification.ts` | Auto-login after email verification |
| `usePostLoginHandler.ts` | Post-login redirect logic |
| `usePostLoginHandlerMarketing.ts` | Marketing-specific post-login |
| `usePendingOrdersPolling.ts` | Poll for pending order status |
| `usePostSignupHandler.ts` | Post-signup flow handler |
| `useOnboardingSubmit.ts` | Onboarding form submission |

### Utilities (`src/utils/`)
| File | Purpose |
|------|---------|
| `MobileUtils.ts` | Mobile device detection |
| `accountUtils.ts` | Account helper functions |
| `endorserUtils.ts` | Endorser-related utilities |
| `errorHandlingMiddleware.ts` | Error handling middleware |
| `errorHandlingToaster.ts` | Toast notification for errors |
| `metadata.ts` | Page metadata utilities |
| `numberUtils.ts` | Number formatting helpers |
| `onboardingUtils.ts` | Onboarding flow utilities |
| `rateLimiter.ts` | Client-side rate limiting |
| `stringUtils.ts` | String manipulation helpers |
| `createApplicationForm.ts` | Application form construction |
| `chartUtils/` | Chart rendering utilities (assertion, bands-indicator, closest-index, min-max-in-range, plugin-base, simple-clone) |
| `trpcUtils/api.ts` | tRPC client setup |
| `trpcUtils/trpcClient.ts` | tRPC client configuration |
| `wrappers/apiProvider.tsx` | API context provider |
| `wrappers/PostProvider.tsx` | PostHog analytics provider |
| `wrappers/welcomeVideoModal.tsx` | Welcome video modal wrapper |
| `wrappers/welcomeVideoPatch.tsx` | Welcome video patch |

### Types (`src/types/`)
- `EndorserTypes.ts` -- Endorser-related type definitions
- `FormTypes.ts` -- Form field type definitions
- `types.d.ts` -- Global type declarations

---

## 2. nextblog (Blog Platform)

**Path:** `/home/brmz/Documents/Projects/Personal/nextblog/`
**Stack:** Next.js 16.0.0, React 19.2, TypeScript 5, Prisma 6.18, PostgreSQL, Better-Auth, TipTap 3, Shadcn/ui, Tailwind 4, UploadThing
**Package manager:** npm
**Purpose:** Full-featured blog platform with admin panel (completed)

### Route Structure (`app/`)

#### Admin Route Group `(admin)/`
- `layout.tsx` -- Admin layout with sidebar
- `dashboard/page.tsx` -- Admin dashboard with stats/charts
- `categories/page.tsx` -- Category management list
- `categories/client/` -- `categories-client.tsx`, `cell-actions.tsx`, `columns.tsx` (data table)
- `posts/page.tsx` -- Post management list
- `posts/[id]/page.tsx` -- Post editor (create/edit)
- `posts/clients/` -- `cell-actions.tsx`, `columns.tsx` (data table)

#### Auth Route Group `(auth)/`
- `layout.tsx` -- Auth pages layout
- `sign-in/page.tsx` -- Sign in form
- `sign-up/page.tsx` -- Sign up form

#### Blog Routes
- `blog/layout.tsx` -- Blog public layout
- `blog/posts/[slug]/page.tsx` -- Individual blog post view
- `blog/category/[id]/page.tsx` -- Posts filtered by category
- `blog/tag/[name]/page.tsx` -- Posts filtered by tag

#### Root
- `layout.tsx` -- Root layout
- `page.tsx` -- Homepage
- `loading.tsx` -- Loading skeleton
- `not-found.tsx` -- 404 page

#### Server Actions (`app/actions/`)
- `blog.ts` -- Blog listing/fetching actions
- `categories.ts` -- Category CRUD actions
- `posts.ts` -- Post CRUD actions (create, update, delete, publish/draft)
- `search.ts` -- Global search action

#### API Routes (`app/api/`)
- `auth/[...all]/route.ts` -- Better-Auth catch-all handler
- `uploadthing/core.ts` -- UploadThing file router config
- `uploadthing/route.ts` -- UploadThing API route

### Components (`components/`)
| File | Purpose |
|------|---------|
| `app-sidebar.tsx` | Admin sidebar navigation |
| `dashboard-card.tsx` | Dashboard stat card |
| `dashboard-categories.tsx` | Dashboard category breakdown |
| `dashboard-chart.tsx` | Dashboard analytics chart |
| `data-table.tsx` | Reusable data table component |
| `header.tsx` | Page header with breadcrumbs |
| `navbar.tsx` | Public blog navigation bar |
| `global-search-modal.tsx` | Full-text search modal (Cmd+K) |
| `image-uploader.tsx` | Image upload component (UploadThing) |
| `pagination.tsx` | Pagination controls |
| `post-card.tsx` | Blog post card for listings |
| `post-form.tsx` | Post create/edit form (title, slug, content, category, tags, image, status) |
| `rich-text-viewer.tsx` | TipTap read-only content renderer |
| `signin-form.tsx` | Sign-in form component |
| `signup-form.tsx` | Sign-up form component |
| `skeleton-card.tsx` | Loading skeleton for post cards |

#### TipTap Editor Toolbars (`components/toolbars/`)
`editor.tsx` (main editor), `toolbar-provider.tsx`, `bold.tsx`, `italic.tsx`, `strikethrough.tsx`, `code.tsx`, `code-block.tsx`, `blockquote.tsx`, `bullet-list.tsx`, `ordered-list.tsx`, `hard-break.tsx`, `horizontal-rule.tsx`, `undo.tsx`, `redo.tsx`, `image-placeholder-toolbar.tsx`

#### TipTap Extensions (`components/extensions/`)
- `image.tsx` -- Custom image node extension
- `image-placeholder.tsx` -- Image placeholder extension for uploading

#### UI Components (`components/ui/`)
Full Shadcn/ui kit: accordion, alert, alert-dialog, aspect-ratio, avatar, badge, breadcrumb, button, button-group, calendar, card, carousel, chart, checkbox, collapsible, command, context-menu, dialog, drawer, dropdown-menu, empty, field, form, hover-card, input, input-group, input-otp, item, kbd, label, menubar, navigation-menu, pagination, popover, progress, radio-group, resizable, scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner, switch, table, tabs, textarea, toggle, toggle-group, tooltip

### Library (`lib/`)
| File | Purpose |
|------|---------|
| `auth.ts` | Better-Auth server configuration |
| `auth-client.ts` | Better-Auth client instance |
| `auth-utils.ts` | Auth helper functions |
| `db.ts` | Prisma client singleton |
| `uploadthing.ts` | UploadThing configuration |
| `utils.ts` | General utility functions (cn, etc.) |

### Database Schema (`prisma/schema.prisma`)
Models: **User**, **Session**, **Account**, **Verification**, **Post**, **Category**
- Posts have: title, slug (unique), content, imageUrl, views, tags[], status (published/draft)
- Categories: name, userId (owner)
- Better-Auth integration: Session, Account, Verification tables

---

## 3. sp-backend-api-testing

**Path:** `/home/brmz/Documents/Projects/Personal/sp-backend-api-testing/`
**Stack:** Cypress 13.13, JavaScript
**Package manager:** npm
**Purpose:** E2E API test suite for Sidepocket backend microservices

### Configuration
- `cypress.config.js` -- Multi-environment config (dev/prod) with service URLs for auth, app, accounts, billing, cash, portfolio
- `package.json` -- Scripts: `cy:open-dev`, `cy:open-prod`, `cy:run-dev`, `cy:run-prod`, `cy:run-dev-full-test`

### Test Structure (`cypress/e2e/`)

#### Accounts Tests
| Test File | Purpose |
|-----------|---------|
| `accountLookUp.cy.js` | Account lookup queries |
| `allAccountAplication.cy.js` | All account application flows |
| `createDirectBrokerageApplication.cy.js` | Brokerage account creation |
| `createIRARothApplication.cy.js` | Roth IRA account creation |
| `createIRATraditionalApplication.cy.js` | Traditional IRA creation |
| `investigation.cy.js` | Account investigation tests |
| `investorDocument.cy.js` | Investor document tests |
| `listActiveAccount.cy.js` | Active account listing |
| `updateDirectBrokerageApplication.cy.js` | Brokerage update tests |

#### App Tests
| Test File | Purpose |
|-----------|---------|
| `appLookUp.cy.js` | App lookup queries |
| `exploreModelSidepocket.cy.js` | Model sidepocket exploration |
| `getMarketHours.cy.js` | Market hours query |
| `liveUserAccountBalances.cy.js` | Live balance queries |
| `liveUserAccountNav.cy.js` | Live account NAV |
| `marketIndexDetails.cy.js` | Market index details |
| `marketIndexSnapshot.cy.js` | Market snapshot |
| `modelSidepoceketDetail.cy.js` | Model sidepocket detail |
| `modelSidepocketHolding.cy.js` | Model sidepocket holdings |
| `securityDetails.cy.js` | Security details lookup |
| `userFilterSidepocket.cy.js` | User sidepocket filtering |

#### Auth_v2 Tests
`authLookUp.cy.js`, `changePassword.cy.js`, `getUserPreference.cy.js`, `getUserProfile.cy.js`, `loginTest.cy.js`, `sendPasswordResetEmail.cy.js`, `signUpTest.cy.js`, `updateUserPreference.cy.js`, `updateUserProfile.cy.js`

#### Billing Tests
`createEndorserUserRelationship.cy.js`, `editEndorserTiers.cy.js`, `endorserAUM.cy.js`, `getAllPlans.cy.js`, `getCurrentUserSubscription.cy.js`, `getStripeInfo.cy.js`, `subscriptionFlow.cy.js`, `toggleEndorserUserActivity.cy.js`, `viewEndorserTiers.cy.js`

#### Cash Tests
`cashLookUp.cy.js`, `createCashTransfer.cy.js`, `createIRARothCashTransfer.cy.js`, `createIRATraditionalCashTransfer.cy.js`, `getAccountConstraint.cy.js`, `getAllCashActivity.cy.js`, `getNonCachedAccountBalances.cy.js`, `getPlaidAccountInfo.cy.js`, `getStateWithholding.cy.js`, `getUserCashTransfer.cy.js`, `getUserCashTransferForAccount.cy.js`, `plaidAccount.cy.js`, `recurringDeposit.cy.js`

#### Portfolio Tests
`checkTradeStatus.cy.js`, `createLiveUserSidepocket.cy.js`, `createSPOrderRequest.cy.js`, `deleteUserSidepocket.cy.js`, `getLiveSidepocketHoldings.cy.js`, `listSPOrderRequests.cy.js`, `liveUserSidepocketDetail.cy.js`, `liveUserSidepocketsList.cy.js`, `portfolioLookUp.cy.js`

#### Shared Data & Request Helpers
- `allData/data.js` -- Test data constants
- `allData/lookUpData.js` -- Lookup test data
- `allData/utils.js` -- Test utility functions
- `requests/accountsRequests.js` -- Account API request builders
- `requests/appRequests.js` -- App API request builders
- `requests/authRequests.js` -- Auth API request builders
- `requests/billingRequests.js` -- Billing API request builders
- `requests/cashRequests.js` -- Cash API request builders
- `requests/portfolioRequests.js` -- Portfolio API request builders

#### Meta-Test Files
- `allGetRequestTests.cy.js` -- Runs all GET request tests
- `e2eTests.cy.js` -- Full E2E test suite
- `end2EndTesting.cy.js` -- End-to-end testing orchestrator
- `getRequestTests.cy.js` -- GET request test runner

---

## 4. HackHarvard2025 (Boston Energy Insights)

**Path:** `/home/brmz/Documents/Projects/HackHarvard2025/`
**Purpose:** Hackathon project -- Boston municipal energy, weather, and traffic insights dashboard

### Backend

**Path:** `backend/`
**Stack:** Flask 3.1, FastAPI, Python 3.13, Supabase, Google Generative AI (Gemini), scikit-learn, SendGrid, Gunicorn
**Entry points:** `main.py` (production), `app.py` (Flask factory with CORS, error handlers, health check)

#### Backend Source Files
| File | Purpose |
|------|---------|
| `app.py` | Flask app factory -- creates app, registers routes, CORS, error handlers, health check (connects to Supabase) |
| `main.py` | Production entry point (port 5000) |
| `config.py` | Unified config: Supabase credentials, Boston geo bounds, energy costs, fuel types, building categories, weather/traffic settings, Gemini API key, insight thresholds |

#### Routes (`routes/`)
| File | Purpose |
|------|---------|
| `__init__.py` | Route registration |
| `dashboard_routes.py` | Dashboard aggregate endpoints |
| `energy_routes.py` | Energy consumption/building endpoints |
| `insights_routes.py` | AI-generated insights endpoints |
| `sim_routes.py` | Simulation endpoints |
| `traffic_routes.py` | Traffic congestion endpoints |
| `weather_routes.py` | Weather data endpoints |

#### Models (`models/`)
| File | Purpose |
|------|---------|
| `energy.py` | Energy building/consumption data models |
| `insights.py` | Insight generation models |
| `traffic.py` | Traffic intersection/congestion models |
| `weather.py` | Weather station/observation models |

#### Utilities (`utils/`)
| File | Purpose |
|------|---------|
| `email_service.py` | SendGrid email integration |
| `external_apis.py` | External API client wrappers |
| `helpers.py` | General helper functions |
| `supabase_client.py` | Supabase database client |

#### Weather Microservice (`weather/`)
**Stack:** FastAPI, httpx, uvicorn
**Entry:** `weather/main.py` (port 8002)
Separate microservice providing OpenMeteo weather data for Boston:
- `GET /weather/openmeteo_current` -- Current weather (temperature, cloud cover, solar radiation, precipitation)
- `GET /weather/openmeteo_forecast` -- Hourly forecast (24h)
- `GET /health` -- Health check

### Frontend

**Path:** `frontend/`
**Stack:** React 19.1, Vite 7, TypeScript 5.9, TanStack Router + React Query, Clerk auth, Shadcn/ui, Tailwind 4, Mapbox GL, Recharts, Axios, Zustand 5
**Package manager:** pnpm (v10.18)
**Name:** `shadcn-admin` (v2.1.0) -- based on shadcn-admin template

#### Frontend Source Structure (`src/`)

##### Layout Components (`src/components/layout/`)
`app-sidebar.tsx`, `app-title.tsx`, `authenticated-layout.tsx`, `header.tsx`, `main.tsx`, `nav-group.tsx`, `nav-user.tsx`, `team-switcher.tsx`, `top-nav.tsx`, `types.ts`

##### Shared Components
`command-menu.tsx`, `coming-soon.tsx`, `confirm-dialog.tsx`, `config-drawer.tsx`, `date-picker.tsx`, `layer-selector.tsx`, `learn-more.tsx`, `long-text.tsx`, `navigation-progress.tsx`, `password-input.tsx`, `profile-dropdown.tsx`, `search.tsx`, `select-dropdown.tsx`, `sign-out-dialog.tsx`, `skip-to-main.tsx`, `stats-cards.tsx`, `theme-switch.tsx`

##### Data Table Components (`src/components/data-table/`)
`bulk-actions.tsx`, `column-header.tsx`, `faceted-filter.tsx`, `index.ts`, `pagination.tsx`, `toolbar.tsx`, `view-options.tsx`

##### UI Components (`src/components/ui/`)
Shadcn/ui kit: alert, alert-dialog, avatar, badge, button, calendar, card, checkbox, collapsible, command, dialog, dropdown-menu, form, input, input-otp, label, popover, radio-group, scroll-area, select, separator, sheet, sidebar, skeleton, sonner, switch, table, tabs, textarea, tooltip

##### Context Providers (`src/context/`)
`direction-provider.tsx`, `font-provider.tsx`, `layout-provider.tsx`, `search-provider.tsx`, `theme-provider.tsx`

##### Config
`src/config/fonts.ts` -- Font configuration

##### Assets (`src/assets/`)
- `logo.tsx`, `clerk-logo.tsx`, `clerk-full-logo.tsx`
- `brand-icons/` -- Discord, Docker, Facebook, Figma, GitHub, GitLab, Gmail, Medium, Notion, Skype, Slack, Stripe, Telegram, Trello, WhatsApp, Zoom
- `custom/` -- Layout icons, sidebar icons, theme icons

---

## 5. sp-endorser-cms (Endorser CMS)

**Path:** `/home/brmz/Documents/Projects/Personal/sp-endorser-cms/`
**Stack:** Next.js 15, Payload CMS 3.9, React 19, PostgreSQL, AWS S3, Lexical editor, Cloudflare Stream, Shadcn/ui, Tailwind 3, SendGrid
**Package manager:** pnpm (v9.15)
**Purpose:** Content management system for Sidepocket endorsers (financial advisors)

**NOTE:** Duplicate/test clones exist at `~/Documents/Projects/Sidepocket/Test/sp-endorser-cms/` and `~/Documents/Projects/Sidepocket/sp-endorser-cms/`.

### Source Structure (`src/`)

#### Payload CMS Collections
- `collections/APIKeys.ts` -- API key management
- `collections/Contents.ts` -- Content/insights collection
- `collections/Media.ts` -- Media uploads collection
- `collections/Users.ts` -- User management collection

#### Payload CMS Blocks
- `blocks/Banner/config.ts` -- Banner block
- `blocks/Code/config.ts` -- Code block
- `blocks/MediaBlock/config.ts` -- Media block

#### Access Control (`src/access/`)
`admins.ts`, `adminsAndReviewers.ts`, `adminsOrPublished.ts`, `anyone.ts`, `endorsers.ts`, `reviewers.ts`

#### Routes (`src/app/`)
- `(payload)/admin/[[...segments]]/` -- Payload admin panel (page + not-found)
- `(payload)/api/[...slug]/route.ts` -- Payload REST API
- `(payload)/api/graphql/route.ts` -- GraphQL endpoint
- `(payload)/api/graphql-playground/route.ts` -- GraphQL playground
- `(payload)/api/upload/[[...params]]/route.ts` -- File upload API
- `(payload)/endorser/(AuthPages)/` -- Endorser auth (login, layout)
- `(payload)/endorser/dashboard/` -- Endorser dashboard
  - `insights/` -- Content/insights management
  - `audience/` -- Audience analytics
  - `media/` -- Media management
  - `settings/` -- Account settings
- `(payload)/endorser/forgotpassword/` -- Password reset
- `(payload)/endorser/verifyemail/` -- Email verification (with `VerifyEmail.tsx`)
- `(payload)/endorser/passwordrecoveryemail/` -- Password recovery email
- `(payload)/endorser/support/` -- Support page
- `my-route/route.ts` -- Custom API route

#### Components
- `admin/` -- Payload admin customizations: `BeforeLogin.tsx`, `DashboardInfo.tsx`, `DashboardOnboard.tsx`, `Icon.tsx`, `Logo.tsx`, `ProfileAvatar.tsx`
- `auth/` -- `GeneralInput.tsx`, `PasswordInput.tsx`, `LogoutButton.tsx`, `AuthFooter.tsx`, `LargeInput.tsx`, `Message.tsx`
- `dashboard/` -- `SideNavigation.tsx`, `SideSubNavigation.tsx`, `ProfileButton.tsx`, `NotificationButton.tsx`, `DekstopMessage.tsx`, `LogoUpload.tsx`, `Spreadsheet1Row.tsx`
- `insights/` -- `CustomRichTextEditor.tsx`, `DropZone.tsx`, `InsightSidebar.tsx`, `MediaPlayer.tsx`
- `onboarding/` -- `FormLayout.tsx`, `FormText.tsx`
- `settings/` -- `AccountForm.tsx`
- `shared/` -- `Button.tsx`, `BlurredBackground.tsx`, `Component.tsx`, `EmailTemplate.tsx`, `GoBackButton.tsx`, `Gutter.tsx`, `HR.tsx`, `Input.tsx`, `LinkButton.tsx`, `LoadingScreen.tsx`, `RenderParams.tsx`, `Select.tsx`, `XIcon.tsx`
- `ui/` -- Shadcn/ui: alert, alert-dialog, aurora-background, card, checkbox, dialog, dropdown-menu, form, input, label, progress, separator, table

#### Other
- `constants/positions.ts` -- Position constants
- `helpers/checkRole.ts` -- Role checking helper
- `helpers/stringHelpers.ts` -- String utilities
- `hooks/ensureFirstUserIsAdmin.ts` -- First-user admin hook
- `lib/utils.ts` -- General utilities (cn, etc.)
- `lib/tus.ts` -- TUS resumable upload client
- `store/MediaStore.ts` -- Zustand media state store
- `utilities/cors.ts` -- CORS configuration
- `utilities/errorHandlingToaster.ts` -- Error toast notifications

---

## 6. College Projects (Archived)

**Path:** `/home/brmz/Documents/Projects/College/`
**Status:** Archived coursework -- not actively maintained

### oracle-todo-app
**Path:** `College/oracle-todo-app/MtdrSpring/`
**Stack:** Spring Boot (Java, Maven) backend + React (CRA) frontend
**Purpose:** Oracle Cloud todo application -- college coursework project

### TC3005B/M6/game-hub
**Path:** `College/TC3005B/M6/game-hub/`
**Stack:** React + TypeScript
**Purpose:** Game hub application -- college module 6 coursework

### TC3005B/M6/online-store
**Path:** `College/TC3005B/M6/online-store/`
**Stack:** React + TypeScript
**Purpose:** Online store application -- college module 6 coursework

---

## 7. Sidepocket Directory (Duplicates)

**Path:** `/home/brmz/Documents/Projects/Sidepocket/`
**Status:** Contains duplicate/test clones of sp-endorser-cms

- `Test/sp-endorser-cms/` -- Test branch clone (on `qa` branch)
- `sp-endorser-cms/` -- Another clone
- `hello.txt` -- Placeholder file

These appear to be scratch copies and can potentially be cleaned up.
