# M10: Standard Mode Worked Example — Remediation Proposal

## Problem
The spawn v2 spec explains Standard Mode as a 4-wave protocol, but it does not show what a real decomposition output looks like. Users can see invocation examples, yet implementers still have to guess the concrete shape of:
- domain detection output
- Epic/Story/Task hierarchy
- DAG nodes, edges, and parallel groups
- delegation mapping from Tasks to `/sc:*` commands

This makes the spec harder to implement consistently and harder to validate in tests.

## Step-by-Step Solution

### Step 1: Add a dedicated “Worked Example (Standard Mode)” section to the spec

Insert a new section immediately after `## Standard Mode: 4-Wave Execution Protocol` or after the Standard Mode behavior summary.

Purpose:
- show one end-to-end example from invocation to final hierarchy document
- demonstrate the expected output shape, not just the algorithm
- anchor later test assertions against a concrete reference example

Recommended heading:
```md
## Worked Example — Standard Mode (`/sc:spawn "implement user authentication" --depth normal`)
```

### Step 2: Frame the example as Given / When / Then

Use specification-by-example structure so the example is both readable and testable.

Recommended framing:
```md
Given: `/sc:spawn "implement user authentication" --depth normal`
When: Standard Mode runs through Waves 1-4
Then: spawn produces the following classification, hierarchy, DAG, and delegation map
```

This directly addresses the panel feedback and gives implementers a stable acceptance target.

### Step 3: Include the exact classification header for the example

The worked example should begin with the mandatory machine-readable classification block already defined by the spec.

Recommended example block:
```md
<!-- SC:SPAWN:CLASSIFICATION
strategy: adaptive
depth: normal
domains_detected: 4
estimated_tasks: 8
delegation_mode: active
pipeline_mode: none
-->
```

Rationale:
- `adaptive` is a plausible default for a multi-domain feature
- `normal` matches the user invocation
- `domains_detected: 4` matches the documented auth example
- `estimated_tasks: 8` fits normal-depth granularity without forcing orchestrator escalation (`tasks_created > 8`)
- `pipeline_mode: none` distinguishes Standard Mode from Pipeline Mode

### Step 4: Show the Wave 1 domain detection output explicitly

The example must show what Wave 1 actually discovers before decomposition begins.

Recommended content:
```md
### Wave 1 — Domain Detection

Detected domains:
1. `database`
2. `backend-api`
3. `frontend-ui`
4. `testing`

Domain rationale:
- `database`: user records, credential storage, uniqueness constraints
- `backend-api`: login, logout, session/token handling, auth middleware
- `frontend-ui`: login form, auth state, protected route UX
- `testing`: unit, integration, and end-to-end verification across the auth flow

Cross-domain dependencies identified:
- `database -> backend-api` (backend requires user schema and persistence model)
- `backend-api -> frontend-ui` (frontend depends on auth endpoints/contracts)
- `backend-api -> testing` (integration and e2e tests require runnable auth flow)
- `frontend-ui -> testing` (e2e coverage requires login UI)
```

This makes the transition from analysis to decomposition concrete.

### Step 5: Show the full Epic / Story / Task hierarchy for `--depth normal`

The example should model the exact hierarchy conventions described in the spec:
- one Epic per domain
- 2-5 Stories per Epic for `normal`
- each Task maps to exactly one `/sc:*` command

Recommended worked example:

```md
## Example Output

### Epic 1: DATABASE — Design and implement user schema

**Story 1.1 — Define authentication data model**
- `task_1_1_1`: Design `users` schema with unique email and password-hash fields
  - Command: `/sc:design --type database`
- `task_1_1_2`: Implement migration for `users` table and indexes
  - Command: `/sc:implement`

**Story 1.2 — Define persistence constraints for auth workflows**
- `task_1_2_1`: Add schema support for password reset/session invalidation metadata
  - Command: `/sc:design --type database`

### Epic 2: BACKEND-API — Build authentication endpoints

**Story 2.1 — Implement credential authentication flow**
- `task_2_1_1`: Implement login endpoint and password verification flow
  - Command: `/sc:implement`
- `task_2_1_2`: Implement logout/session invalidation behavior
  - Command: `/sc:implement`

**Story 2.2 — Protect application routes**
- `task_2_2_1`: Add auth middleware/guard for protected endpoints
  - Command: `/sc:implement`

### Epic 3: FRONTEND-UI — Build authentication user experience

**Story 3.1 — Create login interaction surface**
- `task_3_1_1`: Build login form with validation and error states
  - Command: `/sc:build --feature`

**Story 3.2 — Integrate authenticated application state**
- `task_3_2_1`: Wire frontend auth state and protected-route handling
  - Command: `/sc:implement`

### Epic 4: TESTING — Establish authentication coverage

**Story 4.1 — Verify backend auth behavior**
- `task_4_1_1`: Add API/integration tests for login, logout, and access control
  - Command: `/sc:test --coverage`

**Story 4.2 — Verify end-to-end user authentication flow**
- `task_4_2_1`: Add end-to-end test for login success/failure and protected navigation
  - Command: `/sc:test --e2e`
```

This produces 8 Tasks total, which is clean, realistic, and aligned with normal-depth decomposition.

### Step 6: Show the resolved DAG as both edges and parallel groups

The spec already defines nodes, edges, and parallel groups. The worked example should show both representations because they answer different questions:
- edge list explains causality
- parallel groups explain execution scheduling

Recommended DAG section:

```md
### Resolved DAG

#### Nodes
- `task_1_1_1` — Design `users` schema
- `task_1_1_2` — Implement `users` migration and indexes
- `task_1_2_1` — Design reset/session metadata
- `task_2_1_1` — Implement login endpoint
- `task_2_1_2` — Implement logout/session invalidation
- `task_2_2_1` — Add auth middleware/guards
- `task_3_1_1` — Build login form
- `task_3_2_1` — Wire auth state and protected routes
- `task_4_1_1` — Add backend integration tests
- `task_4_2_1` — Add end-to-end auth test

#### Hard dependency edges
- `task_1_1_1 -> task_1_1_2` — migration follows schema design
- `task_1_1_1 -> task_2_1_1` — backend login depends on user schema
- `task_1_2_1 -> task_2_1_2` — logout/session invalidation depends on persistence model
- `task_2_1_1 -> task_2_2_1` — route protection depends on auth flow primitives
- `task_2_1_1 -> task_3_2_1` — frontend auth state depends on backend auth contract
- `task_3_1_1 -> task_3_2_1` — protected-route handling depends on login UI entry point
- `task_2_1_1 -> task_4_1_1` — backend tests require login endpoint
- `task_2_2_1 -> task_4_1_1` — access-control tests require middleware/guards
- `task_3_2_1 -> task_4_2_1` — e2e test requires frontend auth integration
- `task_4_1_1 -> task_4_2_1` — backend verification completes before full e2e validation

#### Parallel groups
- `Group 1`: [`task_1_1_1`, `task_1_2_1`, `task_3_1_1`]
  - Reason: schema design, metadata design, and login-form shell can begin independently
- `Group 2`: [`task_1_1_2`, `task_2_1_1`]
  - Reason: migration and backend login implementation can proceed once core schema is defined
- `Group 3`: [`task_2_1_2`, `task_2_2_1`, `task_3_2_1`]
  - Reason: session invalidation, route protection, and frontend auth wiring depend on backend primitives but are parallel-safe with coordination
- `Group 4`: [`task_4_1_1`]
  - Reason: backend integration tests require completed API behavior
- `Group 5`: [`task_4_2_1`]
  - Reason: end-to-end test depends on completed frontend and backend auth flow
```

Important note: if the spec wants strict consistency between the hierarchy count and DAG node count, the hierarchy above should include 10 Tasks instead of 8. To avoid mismatch, choose one of the following and document it explicitly:
- Option A: keep the hierarchy at 8 Tasks and reduce the DAG node list to those same 8 Tasks
- Option B: keep the richer 10-node DAG and update the classification header to `estimated_tasks: 10`

Recommended choice: **Option B**. It is more concrete and gives a clearer worked example.

### Step 7: Normalize the example to one internally consistent final version

To prevent ambiguity, the final inserted example should use one consistent task count across:
- classification header
- hierarchy
- DAG nodes
- delegation map

Recommended final version:
- `estimated_tasks: 10`
- hierarchy includes all 10 tasks shown above
- DAG node list mirrors the hierarchy exactly

That means the classification header should be:
```md
<!-- SC:SPAWN:CLASSIFICATION
strategy: adaptive
depth: normal
domains_detected: 4
estimated_tasks: 10
delegation_mode: active
pipeline_mode: none
-->
```

### Step 8: Add a compact delegation map table

The example should finish with a delegation map that makes the Task-to-command mapping explicit and testable.

Recommended table:

```md
### Delegation Map

| Task ID | Task | Delegated Command | Why this command |
|---|---|---|---|
| `task_1_1_1` | Design `users` schema | `/sc:design --type database` | Schema and persistence design task |
| `task_1_1_2` | Implement migration and indexes | `/sc:implement` | Concrete code/database change |
| `task_1_2_1` | Design reset/session metadata | `/sc:design --type database` | Persistence design extension |
| `task_2_1_1` | Implement login endpoint | `/sc:implement` | Backend feature implementation |
| `task_2_1_2` | Implement logout/session invalidation | `/sc:implement` | Backend behavior implementation |
| `task_2_2_1` | Add auth middleware/guards | `/sc:implement` | Cross-cutting backend code change |
| `task_3_1_1` | Build login form | `/sc:build --feature` | UI component creation |
| `task_3_2_1` | Wire auth state/protected routes | `/sc:implement` | Frontend integration logic |
| `task_4_1_1` | Add backend integration tests | `/sc:test --coverage` | Verification and regression coverage |
| `task_4_2_1` | Add end-to-end auth test | `/sc:test --e2e` | Full user-flow validation |
```

This gives implementers a precise reference for Wave 3 behavior.

### Step 9: Add one short “Why this example matters” note

Close the section with a brief clarification that the example is illustrative, not prescriptive.

Recommended wording:
```md
Note: This example is illustrative of the expected Standard Mode output shape. Exact domain names, story boundaries, and delegated commands may vary by codebase context, but all compliant outputs must include the same structural elements: classification header, domain detection summary, Epic/Story/Task hierarchy, resolved DAG, parallel groups, and delegation map.
```

This preserves flexibility while still making the output contract concrete.

### Step 10: Use the worked example as a validation fixture

After adding the example, update validation guidance so implementers can test against it.

Recommended acceptance checks:
- Standard Mode example emits the classification header first
- detected domains include `database`, `backend-api`, `frontend-ui`, and `testing`
- hierarchy contains one Epic per domain
- each Task maps to exactly one delegated `/sc:*` command
- DAG includes explicit dependency edges and parallel groups
- task count is consistent across classification, hierarchy, DAG, and delegation map

## Proposed Final Insert for the Spec

```md
## Worked Example — Standard Mode (`/sc:spawn "implement user authentication" --depth normal`)

Given: `/sc:spawn "implement user authentication" --depth normal`
When: Standard Mode runs through Waves 1-4
Then: spawn produces the following classification, hierarchy, DAG, and delegation map

<!-- SC:SPAWN:CLASSIFICATION
strategy: adaptive
depth: normal
domains_detected: 4
estimated_tasks: 10
delegation_mode: active
pipeline_mode: none
-->

### Wave 1 — Domain Detection

Detected domains:
1. `database`
2. `backend-api`
3. `frontend-ui`
4. `testing`

Cross-domain dependencies identified:
- `database -> backend-api`
- `backend-api -> frontend-ui`
- `backend-api -> testing`
- `frontend-ui -> testing`

### Wave 2 — Hierarchy Output

#### Epic 1: DATABASE — Design and implement user schema

**Story 1.1 — Define authentication data model**
- `task_1_1_1`: Design `users` schema with unique email and password-hash fields
  - Command: `/sc:design --type database`
- `task_1_1_2`: Implement migration for `users` table and indexes
  - Command: `/sc:implement`

**Story 1.2 — Define persistence constraints for auth workflows**
- `task_1_2_1`: Add schema support for password reset/session invalidation metadata
  - Command: `/sc:design --type database`

#### Epic 2: BACKEND-API — Build authentication endpoints

**Story 2.1 — Implement credential authentication flow**
- `task_2_1_1`: Implement login endpoint and password verification flow
  - Command: `/sc:implement`
- `task_2_1_2`: Implement logout/session invalidation behavior
  - Command: `/sc:implement`

**Story 2.2 — Protect application routes**
- `task_2_2_1`: Add auth middleware/guard for protected endpoints
  - Command: `/sc:implement`

#### Epic 3: FRONTEND-UI — Build authentication user experience

**Story 3.1 — Create login interaction surface**
- `task_3_1_1`: Build login form with validation and error states
  - Command: `/sc:build --feature`

**Story 3.2 — Integrate authenticated application state**
- `task_3_2_1`: Wire frontend auth state and protected-route handling
  - Command: `/sc:implement`

#### Epic 4: TESTING — Establish authentication coverage

**Story 4.1 — Verify backend auth behavior**
- `task_4_1_1`: Add API/integration tests for login, logout, and access control
  - Command: `/sc:test --coverage`

**Story 4.2 — Verify end-to-end user authentication flow**
- `task_4_2_1`: Add end-to-end test for login success/failure and protected navigation
  - Command: `/sc:test --e2e`

### Wave 2 — Resolved DAG

#### Nodes
- `task_1_1_1`
- `task_1_1_2`
- `task_1_2_1`
- `task_2_1_1`
- `task_2_1_2`
- `task_2_2_1`
- `task_3_1_1`
- `task_3_2_1`
- `task_4_1_1`
- `task_4_2_1`

#### Hard dependency edges
- `task_1_1_1 -> task_1_1_2`
- `task_1_1_1 -> task_2_1_1`
- `task_1_2_1 -> task_2_1_2`
- `task_2_1_1 -> task_2_2_1`
- `task_2_1_1 -> task_3_2_1`
- `task_3_1_1 -> task_3_2_1`
- `task_2_1_1 -> task_4_1_1`
- `task_2_2_1 -> task_4_1_1`
- `task_3_2_1 -> task_4_2_1`
- `task_4_1_1 -> task_4_2_1`

#### Parallel groups
- `Group 1`: [`task_1_1_1`, `task_1_2_1`, `task_3_1_1`]
- `Group 2`: [`task_1_1_2`, `task_2_1_1`]
- `Group 3`: [`task_2_1_2`, `task_2_2_1`, `task_3_2_1`]
- `Group 4`: [`task_4_1_1`]
- `Group 5`: [`task_4_2_1`]

### Wave 3 — Delegation Map

| Task ID | Delegated Command |
|---|---|
| `task_1_1_1` | `/sc:design --type database` |
| `task_1_1_2` | `/sc:implement` |
| `task_1_2_1` | `/sc:design --type database` |
| `task_2_1_1` | `/sc:implement` |
| `task_2_1_2` | `/sc:implement` |
| `task_2_2_1` | `/sc:implement` |
| `task_3_1_1` | `/sc:build --feature` |
| `task_3_2_1` | `/sc:implement` |
| `task_4_1_1` | `/sc:test --coverage` |
| `task_4_2_1` | `/sc:test --e2e` |

Note: This example is illustrative of the expected Standard Mode output shape. Exact domain names, story boundaries, and delegated commands may vary by codebase context, but compliant outputs must preserve the same structural elements.
```

## Files to Modify
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec.md` — add the worked example section
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/spec-panel-review.md` — optionally mark M10 addressed after insertion
- `/config/workspace/IronClaude/.dev/releases/backlog/v4.xx-SpawnV2/remediation/major/M10-worked-example.md` — this proposal
