# Severity Rubric

Auggie's `severity_hint` is a starting point, not authoritative. After Wave 3 grounding completes, every finding is remapped through this rubric so the report grades consistently regardless of which Auggie pass produced the finding.

## Why a rubric (and not just trust Auggie)

Severity drift is the most common failure mode of AI code review: each invocation grades slightly differently, two findings in the same report contradict each other on severity, and reviewers lose trust in the report. The rubric exists to make grading reproducible — given two findings with the same factual content, they receive the same severity regardless of which pass found them.

The rubric is intentionally explicit about what each tier means in **decision terms** (block merge? request changes? nit?), not just adjectives. That's what reviewers actually care about.

## The five tiers

### 🔴 Critical — Block merge

A finding is Critical iff at least one of:

- **Exploitable security defect**: anything that lets an unauthenticated or under-authorized actor read, modify, or escalate beyond their intended scope. Examples: SQL injection, missing authz check on a write endpoint, hardcoded production credentials, broken crypto, deserialization of untrusted input into executable types, path traversal in a file-serving endpoint.
- **Data-integrity defect**: anything that can persist incorrect data, lose data, or corrupt invariants. Examples: missing transaction around a multi-step write, race condition in a counter, off-by-one that miswrites array bounds, a migration that drops a column without a backfill plan.
- **Crash-on-startup or crash-on-default-path**: a null-deref, unhandled exception, or import-time failure that fires on the most common code path. Not "this could fail in some edge case" — "this will fail on the first run."
- **Regulatory / compliance defect** for a project that operates under one: PII in logs that the project specifically excludes from logs, audit-trail bypass, anything explicitly called out in the repo's compliance docs.

Critical findings receive both a summary comment (in the main report) AND an inline `gh` comment pinned to the file:line.

### 🟠 High — Should fix before merge

A finding is High iff at least one of:

- **Latent security weakness**: not directly exploitable today but trivially exploitable if a precondition changes (e.g., an internal-only endpoint becomes external; a trusted-input function gets called with untrusted input). Examples: missing rate-limit on a write endpoint, broad CORS, weak password hash (when not user-facing yet), `eval()` of a constructed-but-currently-trusted string.
- **Correctness defect on a non-default path**: edge cases that fire often enough to matter (empty list, max int, timezone DST, leap year, retry storm) but aren't the default path.
- **Resource leak**: file handles, sockets, database connections, goroutines, timers — anything that accumulates without bound.
- **API contract break**: changing a public method signature without bumping a version, breaking a documented invariant, silently changing the meaning of an existing flag.
- **Concurrency hazard**: a race, deadlock potential, or missing synchronization that has a realistic trigger.
- **Significant architectural drift**: introducing a layering violation that the codebase explicitly avoids, adding a new circular dependency, putting business logic in a presentation/transport layer when the convention is to keep it out.

High findings receive inline `gh` comments in `--depth deep` mode; in `--depth standard` they get the summary listing only.

### 🟡 Medium — Fix in this PR if cheap, otherwise file follow-up

A finding is Medium iff at least one of:

- **Code-quality issue with concrete consequences**: a god function that's already showing pain (the diff itself is making it worse), copy-pasted code that creates a maintenance burden, a swallowed exception that will hide future bugs, broad `except` that catches more than intended.
- **Performance concern with no immediate user impact** but with a clear trajectory toward one (N+1 in a path that's currently low-volume but will scale).
- **Anti-pattern manifesting once**: feature envy, primitive obsession, message chains, etc., visible at one site but not yet widespread.
- **Test gap on non-trivial logic**: new branch / new function added without a test, but the function isn't on the critical path.
- **Stale or contradictory docs** introduced by this change.

### 🟢 Low — Nice-to-have

A finding is Low iff:

- The issue is real but the cost of fixing it exceeds the cost of living with it, OR
- The improvement is opportunistic (a refactor adjacent to the diff, not required by it), OR
- The pattern exists elsewhere in the codebase and fixing it only here would be inconsistent.

### 💬 Nit — Style, naming, comments

- Naming: snake_case vs camelCase consistency, abbreviation choices, ambiguous identifiers.
- Comments: typos, comments that explain WHAT instead of WHY, missing trailing punctuation, etc.
- Style: blank line conventions, import ordering — only if the repo has a documented convention and this change diverges. **Skip nits entirely if a linter/formatter (ruff, prettier, etc.) is configured and CI will catch them.**

Nits are condensed into a single sub-section of the report (one-line per nit), never get inline comments, and never block merge.

## Severity-remap algorithm (applied in Wave 3)

For each finding F coming out of Auggie:

1. **Start from Auggie's `severity_hint`**.
2. **Apply category overrides** (the category is more reliable than the hint):

| Category | Floor severity (cannot be downgraded below this without explicit reason) | Ceiling severity (cannot be upgraded above this without explicit reason) |
|---|---|---|
| `security` (when exploitable today) | Critical | — |
| `security` (latent) | High | — |
| `data-integrity` | High | Critical (only if persists corruption) |
| `correctness` | Medium | Critical (only if default-path crash) |
| `concurrency` | Medium | High (only if realistic trigger documented) |
| `resource-leak` | Medium | High |
| `api-contract` | Medium | High (if downstream consumers are in-repo) |
| `performance` | Low | High (only if measured impact) |
| `architecture` | Medium | High (if it adds a new violation; downgrade to Low if pre-existing) |
| `layering` / `coupling` | Medium | High (same as architecture) |
| `anti-pattern` | Low | Medium (Medium if the diff makes the smell worse) |
| `dead-code` | Low | Low |
| `tests` | Medium (if on critical path) / Low (otherwise) | High (only if breaking-change w/o test) |
| `docs` | Low | Medium (if it's a public-API change w/ stale docs) |
| `logging` | Low | High (PII in logs → High) |
| `naming` / `style` | Nit | Low |

3. **Apply confidence adjustment** (Auggie's `confidence` field):
   - `low` confidence → drop severity by one tier (Critical → High, High → Medium, etc.). If Critical and low confidence, downgrade only if the orchestrator's grounding pass also flagged uncertainty.
   - `medium` confidence → no change
   - `high` confidence → no change
4. **Apply diff-locality adjustment** (PR/diff mode only):
   - `in_diff: true` → no change
   - `in_diff: false` AND finding type is correctness/security on a callsite affected by the diff → no change
   - `in_diff: false` AND finding is "pre-existing in code the diff doesn't touch" → drop one tier (this is the "PR scope" principle: don't make the PR author fix unrelated debt)
5. **Apply cross-source agreement bonus** (`--depth deep` only):
   - Finding present in both Auggie main pass AND the `auggie-reviewer` agent's independent pass → no change (already high-confidence)
   - Finding present in only one source → drop one tier UNLESS the rubric's floor for that category prevents it

The remap result is the final severity printed in the report.

## Calibration examples

These exist so the rubric is not just abstract — pin the algorithm to real shapes.

### Example: SQL injection sink

```python
# new code in the diff
def get_user(name):
    return db.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

- Auggie `severity_hint`: `critical`
- Category: `security` (exploitable today)
- Confidence: `high`
- `in_diff`: `true`
- **Remap result**: 🔴 Critical (matches the floor for exploitable security)

### Example: god function getting worse

```python
# diff adds 40 lines to a function that is now 280 lines
```

- Auggie `severity_hint`: `medium`
- Category: `anti-pattern`
- Confidence: `medium`
- `in_diff`: `true`
- **Remap result**: 🟡 Medium (anti-pattern ceiling is Medium when the diff makes the smell worse)

### Example: missing test on a new helper called only once

- Auggie `severity_hint`: `high`
- Category: `tests`
- Function is called from one place, not on the critical path
- Confidence: `high`
- **Remap result**: 🟢 Low (off-critical-path test gaps cap at Low per the table; floor is Medium for critical-path)

### Example: pre-existing layering violation that the diff doesn't touch

- Auggie `severity_hint`: `high`
- Category: `layering`
- `in_diff`: `false` and the diff doesn't increase the violation
- **Remap result**: 🟢 Low (PR-scope adjustment downgrades pre-existing-and-untouched)

### Example: typo in a comment

- Auggie `severity_hint`: `low`
- Category: `style`
- **Remap result**: 💬 Nit (style ceiling is Nit unless there's a Low-tier reason to elevate)

## What NOT to include in the report

- Findings that fail file:line grounding (handled in Wave 3, never reach the rubric)
- Findings about formatting that a configured formatter would fix (`ruff format`, `prettier`, etc.)
- Findings that are restatements of caveats already in the PR description
- Findings that are duplicates of higher-severity findings on the same file:line (dedupe step folds them in)

## Decision-mode summary (for the report header)

After all findings are graded, compute a single recommendation:

| Counts | Recommendation in report summary |
|---|---|
| `critical > 0` | **Block merge** — Critical findings must be resolved or explicitly accepted by the human reviewer |
| `critical == 0 && high > 0` | **Request changes** — High findings should be addressed before merge |
| `critical == 0 && high == 0 && (medium > 0 || low > 0)` | **Approve with comments** — Items worth fixing but not blocking |
| All findings are Nit/Low or no findings | **Looks good** — Minor observations only |

This recommendation is the report's first-paragraph verdict. It does NOT translate into a `gh pr review --approve` or `--request-changes` — those decisions belong to the human. The report is always posted as a `--comment` review.
