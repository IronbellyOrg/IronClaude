# Diff Analysis: position paper comparison (D05 launch guard)

## Metadata

- Generated: 2026-11-20 (Step 1 of /sc:adversarial, Mode A, depth standard, unattended)
- Variants compared: 2. Variant 1 = OURS (`variant-1-original.md`, the owner's line: the guard must govern every started worker). Variant 2 = CLAY (`variant-2-original.md`, Clay's line: orchestrator-started workers run without the guard).
- Pre-debate corrections: two factual slips were fixed in the source papers before copying (OURS "three commit attempts" became four: session B twice, C once, D once; CLAY "FS level not observed" was narrowed to the `/sc:pr-submit --monitor 3` cycle, because a plain push and `gh pr create` at level FS ran in session E, pull request 654).
- Total differences found: 17 scored diff points. Categories: structural (2), content (10), contradictions (3), unique contributions (8, listed but not scored for convergence), shared assumptions (2 promoted, 1 stated).
- Note on the task: the two papers answer one question with opposite conclusions, so the content differences are the substance; the structure is deliberately identical (the brief fixed it).

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|---|---|---|---|
| S-001 | Section sequence and formatting: preface, Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right | Same six H2 sections in the same order, same presentation | Same | Low |
| S-002 | Numbered-list presentation: Mechanism 4 items, Cited facts 9 items, bullet lists elsewhere | 4 / 9 | 4 / 9 | Low |

## Content Differences

| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity |
|---|---|---|---|---|
| C-001 | What the launch-level guard governs today, and whether a `worker-start` worker should be inside it | Every started worker must be bound before it runs; the guard replaces "prompt only" | The guard's own scope excludes this worker (LD:23); the design must not wait on it | High |
| C-002 | How hard it is to bind a `worker-start` worker | Cheap: marker line plus `pending` call, helper still on master (`orca_worktree.py:1488`, `:1515`) | Binding has never been observed live; G2 facts 1 to 4 are UNVERIFIED; FU-1 precondition f not tried | High |
| C-003 | How proven the guard is | Live PASS blocks: LL-IMPL, four LL-COMMIT, LL-MERGE, OB-CTX | OB-H1 item 8 FAIL (issue 678), OB-H2 FAIL, protected push never exercised, monitor cycle at FS not observed, status line "not runtime-approved" | Medium |
| C-004 | Meaning of the closed ship gate `GOVERNED_LEVELS_ALLOWED = False` (R33) | Honest gating: no governed launch until proven, "not the guard is proven" | Nothing real is governed today: only `--pipeline none` launches and it writes no launch record | Medium |
| C-005 | What holds a worker back instead of the guard | The prompt and WC-9 are the same layer of defence; the audit reads pull requests only, so a direct push to `master` is invisible to it | The contract section ADD1, the orchestrator's closed "may do" list with `refuse(argv)`, a merge gate pinned to the head commit, audit checks AU1 to AU8 | High |
| C-006 | Friction between the guard and the pull-request workflow | A cost to accept: LL-PUSH-FORM and GHWRITE, one compound command re-issued in split form | `/sc:pr-submit` scripts call `gh api graphql resolveReviewThread`; they work under the guard only through a pinned leak (script path); the two features rub | Medium |
| C-007 | What the owner accepted (G1, first test issue) | One issue only; G2 says bind before any other issue; DQ7 stretches it into the standing rule | The guard's own text already says a coordinator-started worker is not governed; DQ7 adds no exposure the owner's text did not describe | High |
| C-008 | GitHub-side protection of `master` | Notes `protected: false` (re-read live) as the exposure; proposes no ruleset | Notes the same; says the real fix for an unprotected `master` is not a hook; DQ8 treats classic protection as unreadable without admin | Medium |
| C-009 | Which guard level an orchestrated implementation worker would take | FS fits OD1 (feature-branch push, PR, never merge, never force push); F fits WC-9; mapping not yet written, listed as a cost | Not addressed (the worker has no level) | Medium |
| C-010 | Clay's own open items K22 and U42 (a verb denylist does not bind a command the model types; can a hook scope to one session) | The guard is that hook: session-scoped, already built; the design asks for what exists | Listed as a standing risk, open | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|---|---|---|---|
| X-001 | Is binding easy or unproven? (intra-variant tension in OURS) | Mechanism item 2: "one marker line plus one `pending` call, not new code in the hook" | OURS Risks: binding of a `worker-start` worker has never been observed live (G2 facts 1 to 4 UNVERIFIED); CLAY says the same | Medium |
| X-002 | Weight of the OB-H2 FAIL | OURS: the FAIL comes from a verbatim-detail check and "the refusal itself matched" (results lines 471-472) | CLAY lists "OB-H2 FAIL (line 353)" as unproven-guard evidence with no qualification | Medium |
| X-003 | Does the guard "govern every launch" | OURS Claim: nothing the system starts should run ungoverned at a level that can push | LD:23 and IR-1 (LD:349): a coordinator-started worker and `--pipeline none` carry no launch record by design; OURS Mechanism itself adds binding as new work | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | OURS | FS level equals Clay's own OD1 policy and enforces its three prohibitions with existing grid rows (PUSHFORM, PROTECTED, MERGE) | High |
| U-002 | OURS | Clay's U42 and K22 are answered by the existing session-scoped guard | High |
| U-003 | OURS | The audit verb takes `--pr <N>`, so a direct push to `master` is outside it | High |
| U-004 | OURS | Binding machinery survived PR 682 (`cmd_pending`, rule 2, brief nonce slot in the deleted builder) | Medium |
| U-005 | OURS | Live PASS evidence including OB-CTX telling governed, ordinary and human sessions apart in one worktree | Medium |
| U-006 | CLAY | Orchestrator-side controls absent from master: `refuse(argv)` with a test per pattern, merge pinned by `--match-head-commit`, audit AU1 to AU8 | High |
| U-007 | CLAY | `reply-resolve-thread.sh` GraphQL mutation shows a concrete guard versus pr-submit mismatch | Medium |
| U-008 | CLAY | Scale: up to three orchestrated issues at once, each worker with push rights on its branch | Low |

## Shared Assumptions

Agreement points scanned: both papers agree that (a) an unbound `worker-start` worker is allowed by the guard, (b) `master` is unprotected, (c) K12 is rated M / H, (d) the guard is a same-user guardrail, not a sandbox, (e) PR 682 kept guard rule 2, (f) the watcher is `enabled: false` so nothing runs today.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | (a), (e) | The user-level hooks (`~/.claude/settings.json`, `~/.claude/hooks/launch-level-guard.sh`) are registered and effective in the Claude session `worker-start` creates (same `HOME`, same hook list), so binding would take effect if a marker arrived | UNSTATED | Yes |
| A-002 | (a), (b) | The orchestrator session is a trusted, ordinary component: only workers are a risk the guard has to cover, and the orchestrator's own commands are bounded some other way | UNSTATED | Yes |
| A-003 | (c), (d), (f) | The threat is honest drift and one-step workarounds by a worker (guard target TH1, TH2), not deliberate evasion (TH3) | STATED (LD:32) | No |

| # | Assumption | Impact | Status |
|---|---|---|---|
| A-001 | Hooks apply to the started worker | If false, "required guard" binds nothing and the preflight (IR-4) is the only check | Open for debate (tagged L3: guard, state) |
| A-002 | Orchestrator is trusted and ordinary | If false, the orchestrator's typed commands (K22) need a guard of their own | Open for debate (tagged L2: component) |

## Taxonomy tags (debate_topic_taxonomy, AD-5)

Auto-tagging by signal terms, highest level wins. L1 surface: S-001, S-002 (formatting, presentation). L2 structural: A-002 (component), C-008 (no signal, fallback L2). L3 state mechanics: C-001 to C-007, C-009, C-010, X-001 to X-003, A-001 (each text holds "guard", "state" or "invariant"-class signals). All three levels hold at least one point.

## Summary

- Total structural differences: 2
- Total content differences: 10
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Scored diff points for convergence: 17 (S 2 + C 10 + X 3 + A 2)
- Highest-severity items: C-001, C-002, C-005, C-007, U-001, U-002, U-003, U-006
- Similarity check: the variants differ materially on 8 of 10 content points; the 10% similarity skip does not apply, debate proceeds.
