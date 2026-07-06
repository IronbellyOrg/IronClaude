---
contract_version: "1.0"
artifact: adversarial-variant
variant: variant-1-opus-architect
persona_lens: architect
topic: "PR Review Auto-Remediation Monitor (V1.0)"
source: ../merged-requirements.md
created: 2026-06-11
---

# Spec — PR Review Auto-Remediation Monitor (V1.0) · Architect Variant

> **Architect thesis.** This feature is *not* a script — it is a **finite-state remediation
> reactor** wrapped around an unknown external review emitter (the Augment GitHub App). The
> single most consequential architectural decision is to draw a **hard seam** between the parts
> that touch the unknown (detection + parsing) and the parts that are deterministic (state
> machine, routing, loop-guard). Everything below flows from that seam: detection is a
> config-driven, empirically-locked constant; the state machine is pure and testable in
> isolation; autonomy is an *ordinal collapse* of one machine, not four code paths. Build the
> probe-locked detection contract **first or build nothing** — every other component is
> downstream of it.

---

## 1. Overview & Goals

### 1.1 What we are building

A new skill `sc:submit-pr` (+ command `/sc:submit-pr` + a one-line `offer-pr-review.sh` hook
edit) that:

1. Opens a PR on the fork (`IronbellyOrg/IronClaude`) under the existing CLAUDE.md PR-target
   discipline.
2. Arms an **in-session monitor** (hosted by the Monitor tool) that polls the PR for the
   Augment Code review.
3. On review arrival, **re-grades** findings through the reused severity rubric, **routes**
   Medium+ findings to `/sc:troubleshoot`, and — at higher autonomy ordinals — **fixes,
   validates, pushes, replies, and resolves** under a monotonic capped loop-guard.

### 1.2 Goals (architect-weighted)

- **G1 — Isolation of the unknown.** The only place in the system that knows the Augment App's
  GitHub emission shape is a single config module (`detection-contract.md`). No parser logic
  guesses; it reads a locked constant produced by the R1 probe.
- **G2 — One machine, four projections.** The `--monitor` ordinal (0/1/2/3) is a *capability
  ceiling* on a single state machine, not four divergent control flows. This eliminates the
  combinatorial bug surface of "level 2 does X but level 3 forgot to."
- **G3 — Deterministic termination.** The loop-guard round counter is monotonic, keyed on
  "reviews observed since arm," and provably bounded by `--max-rounds`. No infinite remediation.
- **G4 — SoT/build discipline as a first-class constraint.** Every artifact lives under
  `src/superclaude/`; `.claude/` is never staged; every `gh` call pins
  `--repo IronbellyOrg/IronClaude`.

### 1.3 Non-goals (V1.0)

Headless/detached host, GitHub Actions hosting, @bot-mention triggers, reviewing human review
comments, and any merge-state mutation (`--approve`/`--request-changes`). Humans merge.

---

## 2. Architecture & Component Decomposition

### 2.1 The seam (architect's central diagram)

```
                    ┌──────────────── UNKNOWN BOUNDARY ────────────────┐
                    │  detection-contract.md  (probe-locked constant)  │
                    └──────────────▲──────────────────┬────────────────┘
                                   │ reads            │ reads
 ┌─────────┐   PR#   ┌────────────┴───┐  Review   ┌──┴──────────┐  Findings[]  ┌───────────────┐
 │ submit  ├────────►│   poller       ├──────────►│  parser     ├─────────────►│ severity-     │
 │ (PR     │  arm    │ (Monitor host) │  payload  │ (normalize) │  raw         │ router        │
 │  open)  │         └────────┬───────┘           └─────────────┘              └──────┬────────┘
 └─────────┘                  │ state                                                 │ routed
                              ▼                                                        ▼
                       ┌──────────────┐   round/ordinal gates    ┌────────────────────────────┐
                       │ loop-guard / │◄─────────────────────────┤ troubleshoot-dispatcher    │
                       │ state machine│   ──────────────────────►│ (/sc:troubleshoot seeding) │
                       └──────┬───────┘                          └────────────┬───────────────┘
                              │ on validated fix                              │ fix in worktree
                              ▼                                               ▼
                       ┌──────────────┐                          ┌────────────────────────────┐
                       │ validator    │  pass/fail               │ reply/resolve helper       │
                       │ (lint+fmt+   ├─────────────────────────►│ (gh api thread reply +     │
                       │  tests)      │                          │  GraphQL resolveThread)    │
                       └──────────────┘                          └────────────────────────────┘
```

The vertical line is the **only** place that touches the unknown. Everything to its right is
pure-deterministic and unit-testable with fixtures.

### 2.2 Source-tree layout (exact SoT paths)

```
src/superclaude/
├── skills/sc-submit-pr-protocol/
│   ├── SKILL.md                          # C1 — orchestrator: state machine + ordinal gates
│   └── refs/
│       ├── detection-contract.md         # UNKNOWN BOUNDARY — probe-locked constant (R1 gate)
│       ├── state-machine.md              # the 7-state FSM spec (§3) — single source for all ordinals
│       ├── severity-routing.md           # C3 — re-grade + tier map; defers to severity-rubric.md
│       ├── augment-poll.md               # C2 — poller contract (interval, timeout, backoff)
│       ├── troubleshoot-dispatch.md      # finding→/sc:troubleshoot seeding contract
│       ├── thread-reply.md               # C4 — gh api reply + GraphQL resolveReviewThread
│       └── loop-guard.md                 # FR-6 round-counter invariants + run-log schema
│   └── scripts/
│       ├── poll-augment-review.sh        # C2 — single poll → emits one JSON line (Monitor stream)
│       └── resolve-thread.sh             # C4 — GraphQL resolveReviewThread wrapper
├── commands/submit-pr.md                 # C1 — /sc:submit-pr command (frontmatter + triggers)
└── hooks/scripts/offer-pr-review.sh      # C5 — EDIT: add sc:submit-pr --monitor mention
tests/skills/sc_submit_pr/                # C6 — FSM unit tests + AC fixtures
```

After **any** edit under `src/superclaude/`: `make sync-dev` → `make verify-sync`. **Never**
`git add .claude/<anything-but-settings.json>`.

### 2.3 Component responsibilities (single-responsibility cut)

| ID | Component | File | Consumes | Produces | Reuse? |
|----|-----------|------|----------|----------|--------|
| C1 | Orchestrator / FSM | `SKILL.md` + `state-machine.md` | ordinal, max-rounds, PR# | state transitions | New |
| C2 | Poller | `augment-poll.md` + `poll-augment-review.sh` | PR#, detection-contract | one JSON event/poll | New |
| **DET** | **Detection contract** | `detection-contract.md` | R1 probe output | bot-login + emission-shape constant | New (R1-gated) |
| C3 | Severity router | `severity-routing.md` | raw findings | `{finding, severity, tier}` | **Reuse** `severity-rubric.md` |
| C3b | Troubleshoot dispatcher | `troubleshoot-dispatch.md` | routed findings | `/sc:troubleshoot` invocations | New (wraps existing skill) |
| C4 | Reply/resolve helper | `thread-reply.md` + scripts | comment_id, SHA | thread reply + resolved thread | New (mirrors auggie-review gh patterns) |
| LG | Loop-guard | `loop-guard.md` | round counter, events | terminate/continue + run-log | New |
| VAL | Validator | (in `SKILL.md`) | changed files | pass/fail | Reuse repo `make` targets |
| C5 | Hook edit | `offer-pr-review.sh` | — | offer line | **Edit** |
| C6 | Tests | `tests/skills/sc_submit_pr/` | fixtures | green suite | New |

**Architect's decomposition rule:** C3 (router) and C3b (dispatcher) are *separate* refs even
though the source treats routing as one FR. Re-grading severity is a pure function of
(finding, rubric); dispatching to troubleshoot is an I/O-bound side-effecting action. Keeping
them apart lets C3 be unit-tested with zero subprocess mocking.

---

## 3. State Machine — the `--monitor` ordinal as a capability ceiling

### 3.1 The single FSM (all ordinals share it)

```
                    arm(ordinal)
   [IDLE] ───────────────────────────────► [POLLING]
                                                │
                  no review (interval ≥30s, t<timeout)  │ loop back to POLLING
                                                │◄───────┘
            review, 0 Medium+ ┌────────────────┤ review, ≥1 Medium+
                              ▼                 ▼
                        [TERMINATED_CLEAN]   [ROUTING]
                                                │ severity-router (C3)
                                                ▼
                                            [DIAGNOSING]  ← /sc:troubleshoot (diagnose)
                                                │
              ordinal==1 ┌─────────────────────┤ ordinal≥2
                         ▼                      ▼
                  [PROPOSED→HALT]          [FIXING] ── needs_human_decision ──► [HALT_HUMAN]
                  (offer y/n, no edits)        │ (worktree edits)
                                               ▼
                                          [VALIDATING] ── fail ──► [VALIDATION_FAIL]
                                               │ pass                    │ retry≤budget / HALT
              ordinal==2 ┌────────────────────┤ ordinal==3
                         ▼                     ▼
                  [HALT_BEFORE_PUSH]      [PUSHING] → [REPLYING] → [RESOLVING]
                  (ask before commit/push)     │
                                               ▼
                                      [AWAIT_REREVIEW] ── round++ ──► back to [POLLING]
                                               │ rounds==max OR 0 Medium+
                                               ▼
                                      [TERMINATED] (FR-6.4 summary if residual)
```

### 3.2 Ordinal = capability ceiling, not a branch

The architect-distinctive claim: **there are not four implementations**. There is one FSM. The
ordinal is a single integer compared at exactly three transition gates:

| Gate | Predicate | L0 | L1 | L2 | L3 |
|------|-----------|----|----|----|----|
| G-arm | `ordinal ≥ 1` to enter POLLING | ✗ | ✓ | ✓ | ✓ |
| G-edit | `ordinal ≥ 2` to enter FIXING | — | ✗ (→PROPOSED) | ✓ | ✓ |
| G-push | `ordinal ≥ 3` to enter PUSHING | — | — | ✗ (→HALT_BEFORE_PUSH) | ✓ |

Plus one **override** that ignores the ordinal entirely: `needs_human_decision ⇒ HALT_HUMAN`
even at L3 (FR-4.4). This is the only predicate allowed to short-circuit the ceiling.

**L0** is structurally the FSM never leaving IDLE: `/sc:submit-pr --monitor 0` opens the PR and
returns. Byte-for-byte identical to today (AC-1), because the only added code path is `if
ordinal == 0: return after_pr_create`.

### 3.3 Why a machine and not nested ifs

A nested-if implementation of four levels has 2³ = 8 reachable gate combinations and the bug
surface is every forgotten combination. The FSM has **7 states × 3 gate-checks**, each gate a
one-line ordinal comparison, and the entire control flow is expressible as a transition table
that C6 tests directly (AC-2..AC-6 become table-row assertions).

---

## 4. Interfaces & Data Contracts

### 4.1 `DetectionContract` (the locked constant — DET)

Defined in `detection-contract.md`, consumed by the poller and parser. **This is a data
constant, not code** — it is filled by the R1 probe and never guessed:

```yaml
# detection-contract.md — locked by R1 empirical probe (see §11)
augment_bot_login: "<PROBE-LOCKED>"          # e.g. "augment-code[bot]" — NOT hard-guessed
emission_shape: "<review|issue_comment|check_run>"  # which gh surface carries findings
findings_locus: "<reviews[].body|comments[]|check_run.output>"
severity_field_path: "<jsonpath-or-null>"    # Augment's self-reported severity, if any
review_completeness_signal: "<state==COMMENTED|presence-of-summary-marker>"
probe_evidence: "<abs-path to captured gh json>"  # provenance for the lock
locked: false                                 # R1 flips this to true; build BLOCKS while false
```

**Interface invariant:** the parser imports exactly these keys and nothing else. If a future
Augment change breaks detection, only this file changes — the FSM, router, and loop-guard are
untouched. That is the payoff of the seam.

### 4.2 Event stream (poller → FSM)

The poller (`poll-augment-review.sh`) emits **one JSON line per poll** to the Monitor stream:

```json
{"ts":"<iso8601>","poll_n":3,"review_state":"none|clean|findings",
 "augment_review_id":"<id|null>","findings_raw":[...],"rate_limit_remaining":N}
```

`review_state` is computed *only* against `DetectionContract` — the FSM never inspects raw gh
JSON. This is the contract boundary.

### 4.3 Finding (parser → router → dispatcher)

```json
{"comment_id":"<id>","review_id":"<id>","path":"src/...","line":N,
 "body":"<text>","augment_severity_hint":"<str|null>","thread_id":"<graphql-node-id>"}
```

Router adds `severity` (re-graded) and `tier`. `thread_id` (GraphQL node id) is captured **at
parse time** so the reply/resolve helper never re-queries.

### 4.4 RoutedFinding (router → dispatcher)

```json
{"...finding...","severity":"Critical|High|Medium|Low|Nit",
 "tier":"deep|standard|report-only","needs_human_decision":bool}
```

### 4.5 RunLog record (every component → NFR-3 log)

Append-only JSONL at `.dev/brainstorms/.../monitor-run-<PR>.jsonl` (or a stable
`.dev/submit-pr-runs/` dir):

```json
{"ts":"...","round":1,"event":"poll|route|diagnose|fix|validate|push|reply|resolve|halt|terminate",
 "detail":{...},"state_from":"...","state_to":"..."}
```

The RunLog is **also the resume checkpoint** (R3 mitigation): a re-armed monitor reads the last
record to reconstruct `round` and replied-comment set.

### 4.6 Troubleshoot seeding contract (C3b → /sc:troubleshoot)

The dispatcher invokes `/sc:troubleshoot` with the finding pre-loaded so troubleshoot does not
re-derive the problem (FR-3.3). Seed payload = `{body, path, line, severity, evidence}`. Tier
maps directly: `deep` → `--depth deep --fix`; `standard` → `--fix`.

---

## 5. Functional Requirements (elaborated)

- **FR-A1 (was FR-1).** `/sc:submit-pr [--monitor {0,1,2,3}] [--max-rounds N] [--base master]
  [--head <branch>] [--title …] [--body …]`. `--monitor` defaults `0`. Every `gh` call pins
  `--repo IronbellyOrg/IronClaude`. Pre-PR checks (origin verify, rebase-if-behind, URL
  verify) run before arm.
- **FR-A2 — PR-open is a precondition, not a state.** The FSM arms *only after* the URL is
  verified to be `https://github.com/IronbellyOrg/IronClaude/pull/N`. A wrong-owner URL aborts
  arm and reports.
- **FR-A3 — Poller (C2).** Polls via `gh pr view <N> --repo IronbellyOrg/IronClaude --json
  reviews,comments` + `gh api repos/IronbellyOrg/IronClaude/pulls/<N>/reviews` and `…/comments`,
  classifying via `DetectionContract` only. Interval ≥30s; timeout default 30 min → emits
  `review_state:"timeout"` → graceful TERMINATED. Backs off on 403/secondary-limit (NFR-2).
- **FR-A4 — Router (C3).** Re-grades each finding through `severity-rubric.md` (Augment's hint
  is advisory). Unknown severity → Medium (NFR-4 fail-safe). Unknown bot login →
  `review_state:"none"` (never act on non-Augment comments).
- **FR-A5 — Routing matrix.** Medium → `/sc:troubleshoot --fix`; High/Critical → `--depth deep
  --fix`; Low/Nit → report-only. Findings batch by file/area (FR-3.4) but never exceed the
  round budget.
- **FR-A6 — Ordinal gates.** L1 propose-only (zero edits, verbatim offer). L2 fix+validate then
  HALT before any commit/push/reply. L3 fix+validate+push+reply+resolve under loop-guard.
  `needs_human_decision` HALTs even at L3.
- **FR-A7 — Validation (VAL).** "Validated" = targeted tests for changed files pass; escalate to
  `make test` when cross-cutting (decision logged). `make lint` **and** `uv run ruff format
  --check src/ tests/` must pass pre-push (the known green-lint≠green-CI gotcha). Fail ⇒ no push.
- **FR-A8 — Reply/resolve (C4).** Each fix posts a reply on the specific thread via `gh api
  repos/IronbellyOrg/IronClaude/pulls/<N>/comments/<comment_id>/replies` (REST reply) then
  resolves via GraphQL `resolveReviewThread(threadId:<node-id>)`. Reply body carries the fix
  summary + commit SHA. Idempotent (NFR-1): replied comment_ids tracked in RunLog.
- **FR-A9 — Loop termination (LG).** After push, AWAIT_REREVIEW; stop when re-review shows zero
  Medium+ OR `round == max-rounds`. The monitor's own push counts as the *next* round
  (monotonic counter). Residual at max → FR-6.4 summary comment + hand back.
- **FR-A10 — Hook edit (C5).** `offer-pr-review.sh` adds a second invocation hint mentioning
  `/sc:submit-pr --monitor` alongside the existing `/sc:auggie-review` offer. Hook stays
  fail-open, never blocks, never spawns.

---

## 6. Non-Functional Requirements

- **NFR-1 — Idempotency.** Replied comment_ids and resolved thread_ids are de-duped against the
  RunLog before any write. A re-armed monitor never double-posts.
- **NFR-2 — Rate-limit safety.** Poll ≥30s; exponential backoff (30→60→120s, cap 300s) on gh
  403/secondary-limit; surface `rate_limit_remaining` in each event.
- **NFR-3 — Observability = resumability.** The RunLog (§4.5) is both forensic record and resume
  checkpoint. Every state transition writes a record *before* the side effect (write-ahead).
- **NFR-4 — Fail-safe defaults.** Unknown severity → Medium (fix tier). Unknown/absent bot login
  → "review not detected" (never act). `locked: false` in DetectionContract → build BLOCKED.
- **NFR-5 — Output discipline.** All user-facing paths absolute; all paste-ready commands
  single-line (terminal cannot paste heredocs/continuations).
- **NFR-6 — Purity of the deterministic core.** The FSM, router, and loop-guard contain **zero**
  `gh`/`git` calls. All I/O is isolated to poller/dispatcher/helper/validator. This is what
  makes AC-2..AC-6 testable without network.

---

## 7. Detection-Contract Design (DET) — the pluggable constant

The architect's strongest position: **detection is configuration, not logic.** FR-2.2's
three-state classifier (none / clean / findings) is a pure function
`classify(gh_payload, DetectionContract) → review_state`. The contract is a single YAML-fronted
ref filled by the R1 probe (§4.1). Consequences:

1. **The parser is generic.** It does not contain `if login == "augment-code[bot]"`. It contains
   `if login == contract.augment_bot_login`. The string lives in data.
2. **One change point on Augment drift.** If Augment changes from review-comments to check-runs,
   `emission_shape` flips and `findings_locus` re-points; no control-flow code changes.
3. **Build-gated.** `locked: false` is a hard stop. The skill's pre-flight asserts
   `contract.locked == true` and refuses to arm a monitor against an unlocked contract — turning
   R1 from a "should" into a mechanically-enforced sequencing dependency (§11).

---

## 8. Loop-Guard Design (LG)

- **L8.1 — Counter semantics.** `round` is keyed on **"reviews observed since arm"**, not
  "reviews since last poll." Concretely: `round` increments exactly once per AWAIT_REREVIEW→
  POLLING transition that follows a monitor push. The initial review is `round 0`.
- **L8.2 — Monotonic + capped.** `round` only increases; `round ≤ max_rounds` is asserted at
  every AWAIT_REREVIEW exit. Default `max-rounds 2`, hard ceiling 5 (reject `>5` at CLI parse).
- **L8.3 — Self-trigger attribution.** A re-review whose `pushed_sha` matches the monitor's last
  push is attributed to the current round, never treated as a fresh independent arm. The
  matching uses the SHA recorded in the RunLog at PUSHING.
- **L8.4 — Write-ahead.** `round++` is written to the RunLog *before* the next poll begins, so a
  crash mid-round resumes at the correct count (R3).
- **L8.5 — Termination proof obligation.** AC-6 asserts: across a 2-round fixture, the counter
  reaches exactly 2, never re-enters POLLING after `round == max`, and emits the FR-6.4 summary
  on residual findings.

---

## 9. Validation Gates

| Gate | Command | Blocks |
|------|---------|--------|
| VG-1 targeted tests | `uv run pytest tests/<changed-area>/ -v` | push |
| VG-2 cross-cutting escalation | `uv run pytest` (`make test`) when ≥2 packages touched | push |
| VG-3 lint | `make lint` (`ruff check`) | push |
| VG-4 format | `uv run ruff format --check src/ tests/` | push |
| VG-5 sync (skill self-edits only) | `make verify-sync` | commit |
| VG-6 PR-target | URL == `IronbellyOrg/IronClaude` | arm |

VG-3 and VG-4 are **both** mandatory — the memory note "`make lint` ≠ CI ruff format" is encoded
as two distinct gates so green lint alone cannot authorize a push.

---

## 10. Acceptance Criteria (testable)

- **AC-1.** `--monitor 0` ⇒ PR opens, FSM never leaves IDLE, zero monitor side effects
  (regression-identical to today). *Test:* FSM transition table asserts no transition out of
  IDLE when ordinal==0.
- **AC-2.** Fixture PR (1 Medium + 1 High) at L3 ⇒ 2 troubleshoot sessions (1 standard, 1 deep),
  2 validated fixes, 2 thread replies, 2 resolved threads, ≤max-rounds, deterministic
  TERMINATED.
- **AC-3.** L1 ⇒ zero file edits; emits the offer prompt verbatim (string-equality assert).
- **AC-4.** L2 ⇒ changes remain in worktree; zero pushes without approval (assert HALT_BEFORE_
  PUSH reached, no `git push` event in RunLog).
- **AC-5.** A `needs_human_decision` finding ⇒ HALT_HUMAN even at L3 (override predicate test).
- **AC-6.** Loop never exceeds max-rounds; monitor-triggered re-review increments the *same*
  counter; 2-round fixture reaches exactly round 2 then TERMINATED.
- **AC-7.** Every `gh` invocation in the code path carries `--repo IronbellyOrg/IronClaude`
  (static grep assertion over `scripts/` + SKILL.md).
- **AC-8 (architect-added).** `detection-contract.md` with `locked: false` ⇒ skill refuses to
  arm and reports the R1 gate. Proves the build-sequencing dependency is mechanically enforced.
- **AC-9 (architect-added).** Static test: no `gh`/`git` token appears in `state-machine.md`,
  `severity-routing.md`, or `loop-guard.md` — proving the deterministic core's purity (NFR-6).

---

## 11. Risks & Mitigations

- **R1 — Detection is guesswork until probed.** *Mitigation:* DetectionContract `locked:false`
  is a **hard build gate** (AC-8); the skill cannot arm against an unlocked contract. The probe
  (open throwaway PR → capture `gh pr view --json reviews,comments` + `…/reviews` + `…/comments`
  → fill the contract → flip `locked:true`) is sequencing step 0 (§12). *Architect note:* by
  making detection a data constant, a wrong probe is a one-file fix, not a parser rewrite.
- **R2 — Loop-guard correctness.** *Mitigation:* counter keyed on "reviews since arm" + SHA
  self-attribution (L8.3) + write-ahead (L8.4) + AC-6. The monotonic invariant is asserted at
  every AWAIT_REREVIEW exit, not just at termination.
- **R3 — Session-longevity fragility.** *Mitigation:* write-ahead RunLog *is* the resume
  checkpoint; a re-armed monitor reconstructs round + replied-set from the last record. Document
  prominently; V2.0 headless host is the real fix.
- **R4 — Auto-push blast radius (L3).** *Mitigation:* VG-3+VG-4 dual gate, FR-A6 human-decision
  HALT, write-ahead audit log, `--max-rounds 2` default, hard ceiling 5. L3 is opt-in
  per-invocation, never a persisted default.
- **R5 (architect-added) — Seam leakage.** Risk that future maintainers inline a bot-login
  string into the parser, collapsing the seam. *Mitigation:* AC-9 static purity test + AC-7
  forbid raw login strings in the deterministic core; CI fails on regression.

---

## 12. Build Sequencing (dependency-ordered)

The ordering is a **dependency DAG**, not a preference. DET gates everything.

```
[0] R1 PROBE → lock detection-contract.md (locked:true)        ◄── HARD GATE (AC-8)
        │
        ▼
[1] C1 SKILL skeleton + state-machine.md + ordinal 0/1 (POLLING, report; no edits)
        │
        ├──► [2] C3 severity-routing.md (reuse rubric) + C3b dispatcher (L1 diagnose-only)
        │
        ▼
[3] L2: VAL gates (VG-1..VG-4) + FIXING + HALT_BEFORE_PUSH
        │
        ▼
[4] C4 thread-reply.md + resolve-thread.sh + L3 PUSHING/REPLYING/RESOLVING
        │
        ▼
[5] LG loop-guard.md (R2) + AC-6 2-round fixture
        │
        ▼
[6] C5 hook edit + C6 full suite → make sync-dev → make verify-sync
```

**Gate rule:** step 1 cannot begin until `detection-contract.md.locked == true`. Steps 2–5 are
internal-pure and testable with fixtures (no network). Step 6 is the only step that touches
`.claude/` — via `make sync-dev`, **never** a manual `git add`.

---

## 13. SoT & PR-Target Discipline (binding constraints)

1. All component edits originate in `src/superclaude/`; `make sync-dev` regenerates `.claude/`;
   `make verify-sync` confirms parity before commit. **Never** `git add .claude/<not
   settings.json>`; an `-f` on a `.claude/` path is the violation siren — stop.
2. Every `gh` call in the skill, scripts, and command pins `--repo IronbellyOrg/IronClaude`.
   PRs target the fork; `gh pr create` without `--repo` is forbidden (gh defaults to upstream).
3. The eval/iteration workspace (if `skill-creator` is used to scaffold) goes to
   `.dev/eval-workspaces/sc-submit-pr/`, never `.claude/skills/*-workspace/`.
