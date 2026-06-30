---
contract_version: "1.0"
artifact: diff-analysis
topic: "PR Review Auto-Remediation Monitor (V1.0)"
source: ../merged-requirements.md
variants_compared: 3
generated: 2026-06-11
---

# Diff Analysis — PR Review Auto-Remediation Monitor (V1.0)

Comparison of three spec variants generated from one merged-requirements source:

- **Variant A** (`opus:architect`) — `variant-1-opus-architect.md` — architecture / FSM-centric, "one machine, four projections", probe-locked detection seam.
- **Variant B** (`sonnet:backend`) — `variant-2-sonnet-backend.md` — process / reliability-centric, durable run-log substrate, 14 canonical states + 12 failure modes.
- **Variant C** (`haiku:qa`) — `variant-3-haiku-qa.md` — test-coverage-centric, 90-test matrix, fence-post loop-guard catalog, 16 edge cases.

## Metadata

| Field | Value |
|-------|-------|
| Generated | 2026-06-11 |
| Variants compared | 3 (A=opus:architect, B=sonnet:backend, C=haiku:qa) |
| Total differences | 41 |
| Structural differences (S) | 7 |
| Content differences (C) | 9 |
| Contradictions (X) | 8 |
| Unique contributions (U) | 9 |
| Shared assumptions (A) | 8 |

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Organizational model | Architecture-FSM-centric: seam diagram → state machine → contracts | Process/reliability-centric: state model → poll/backoff → loop-guard → run-log → failure modes | Test-coverage-centric: FR+testability tables → 90-test matrix → edge catalog → loop-guard tests | High |
| S-002 | Top-level section count | ~13 numbered sections (Overview…SoT discipline) | ~14 sections (Overview…Failure Modes & Recovery) | 14 sections (Overview…QA design decisions) | Low |
| S-003 | Central artifact / spine | The "seam" diagram (§2.1) + 7-state FSM (§3) | The `.jsonl` run-log + `state.snapshot.json` recovery substrate (§"Idempotency & Run-log Schema") | The 90-test coverage matrix (§4.2) + fence-post matrix (§6.2) | High |
| S-004 | Requirement presentation | FR re-labeled FR-A1..A10, prose + architect rationale | FR-1..FR-10, declarative numbered sub-clauses | FR-1..FR-7 in tables, each row carrying a T-xxx testability note | Medium |
| S-005 | State-machine granularity | 7 named states (IDLE…TERMINATED) as a capability-ceiling FSM | 15 canonical states S0_INIT..S14_TERMINAL_FAILED | 7 invariants (INV-1..INV-7) + 3 detection states; no formal state list | Medium |
| S-006 | Risk taxonomy | R1..R5 (adds R5 seam-leakage) | R-1..R-10 (10 backend risks) | R1..R10 with P0/P1/P2/P3 severity + test-coverage column | Medium |
| S-007 | Path convention | Relative SoT paths (`src/superclaude/…`) | Absolute paths throughout (`/config/workspace/IronClaude/…`) | Mixed; test-relative paths (`tests/submit_pr/…`) | Low |

## Content Differences

| # | Topic | A Approach | B Approach | C Approach | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Detection contract | Pluggable YAML constant `detection-contract.md` with `locked:false` hard build-gate; parser is generic (`login == contract.augment_bot_login`) | Centralized config constant `{augment_bot_logins[], augment_author_association[], augment_app_slug}`; "empirically validated before release" | Config constant absent → skill HALTs with "probe first" (T-210/EC-11); three detection states D0/D1/D2 | High |
| C-002 | Loop-guard / round key | `round` keyed on "reviews observed since arm"; SHA self-attribution (L8.3); monotonic, write-ahead | `round_index` = count of post-arm Augment reviews with Medium+ findings not already terminal; explicit "is not" list (polls/comments/pushes/findings) | `round_counter` via 7 invariants + 10-row fence-post matrix; T-626 canonical off-by-one | High |
| C-003 | Autonomy levels | Single FSM, ordinal = capability ceiling checked at exactly 3 gates (G-arm/G-edit/G-push) + 1 override | 4 levels FR-6.1..6.5 as declarative behaviors; `needs_human_decision` halts at all levels | 4 levels as behavioral tests (T-401..T-430) asserting tool-call counts | Medium |
| C-004 | Validation gates | 6 gates VG-1..VG-6 table; VG-3 lint + VG-4 format both mandatory + purity gate | Ordered 5-step gate; targeted→`make test` escalation triggers enumerated; commit/push preconditions list | T-501/502/510/511; explicit format-fails-while-lint-green test (T-511) | Medium |
| C-005 | Idempotency / run-log | RunLog JSONL = forensic + resume checkpoint; write-ahead before side effect; replied-id dedup | Full event-envelope schema (29 event types), `state.snapshot.json` cache, 5 idempotency sets, snapshot-vs-JSONL conflict rule (JSONL authoritative) | Run-log as observability test target (T-N20..N22, valid-JSONL assertion); lighter schema | High |
| C-006 | Severity routing | Re-grade via reused rubric; unknown→Medium; router (C3) split from dispatcher (C3b) for pure unit-testing | Re-grade; normalized set {Critical,High,Medium,Low,Nit}; unknown/malformed/contradictory→Medium; ungrounded findings not auto-fixed at L3 | Rubric tested independently (QD-6) with all 14 category mappings + confidence/locality adjustments; remap tests T-301/302 | Medium |
| C-007 | Monitor host / session | Monitor tool host; RunLog write-ahead enables re-armed resume; V2.0 headless is real fix | Monitor tool host; `--resume <run-log>` is first-class path (FM-1); document V1 limitation | Monitor tool host; session-close = documented limitation, logged `session_closed`, no code assertion (T-230) | Medium |
| C-008 | PR-creation preconditions | FR-A2: PR-open is precondition not state; wrong-owner URL aborts arm | Enumerated: `git remote -v`, `git fetch`, rebase-if-behind, `gh auth status`, URL verify (each "otherwise stop") | T-106/107/108 mock-based: wrong origin HALT, behind→auto-rebase, wrong-owner URL HALT | Low |
| C-009 | Timeout semantics | Timeout default 30 min → `review_state:"timeout"` → graceful TERMINATED | Wall-clock since entering S3 (not cumulative); backoff counts toward deadline; won't sleep past deadline | `--timeout` configurable, fires at deadline (T-221/222); EC-6 timeout-mid-remediation lets current fix finish | Medium |

## Contradictions

| # | Point of Conflict | A Position | B Position | C Position | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | `--max-rounds=0` semantics | Undefined; "default 2, hard ceiling 5", `>5` rejected at parse — 0 not addressed | **Invalid** for `--monitor 2/3`: "Values below `1` are invalid when `--monitor 2` or `--monitor 3`; `--monitor 1` may accept `0` only if … diagnose/report with no remediation loop" (l.224) | **Valid diagnostic mode** (QD-2): "It means 'monitor and report but never remediate' … Equivalent to level 1 regardless of `--monitor` value" (l.718-720); tested T-628/EC-8 | High |
| X-002 | Does validation failure consume a round? | Implicit: "retry≤budget / HALT" in FSM; counter impact not stated | "At monitor level 3, one additional fix attempt may occur only if `round_index < max_rounds`" (l.481) — couples retry to round budget | **Explicit NO** (QD-1/INV-6): "validation failure (T-520) does NOT increment round_counter (retry within same round)" (l.344); "An alternative design (count validation attempt as a round) would waste round budget" (l.715) | High |
| X-003 | Reply dedup keying | Idempotent on tracked replied `comment_id`s in RunLog (NFR-1, l.313) | `replied_comment_ids` keyed on `source_comment_id`; BUT finding dedup uses `finding_id="aug-<comment_id>-<stable_hash>"` (l.260) — two keys | **comment_id, NOT finding hash** (QD-5): "Reply … posted once per thread, not once per finding" (l.733); yet EC-4 dedups *findings* by "`file:line` + finding body hash" (l.250) | Medium |
| X-004 | Detection-contract as build gate vs advisory | **Enforced build-gate**: `locked:false` ⇒ "skill refuses to arm … build BLOCKED" (AC-8, NFR-4 l.320); mechanically enforced sequencing | **Advisory/release-time**: "must be empirically captured before implementation is considered complete" (l.240); "validated before release" (FR-4.5) — no build-lock primitive | **Runtime HALT**: config constant absent → skill HALTs "probe first" (T-210/EC-11); a runtime guard, not a build lock | High |
| X-005 | Round-counter starting value / indexing | "initial review is `round 0`" (L8.1); round increments per AWAIT_REREVIEW→POLLING after push | `round_index` increments to 1 on first actionable review ("increment … exactly once before starting diagnosis", l.217) — first remediation is round 1 | Mixed: "round_counter starts at 0" (INV-1) but T-629 "Rounds executed = 1" for first cycle, and T-630 asserts `round_sequence == [0,1]` then `round_counter == 2` for two cycles (l.408) | Medium |
| X-006 | Where `needs_human_decision` is determined | Override predicate on RoutedFinding evaluated post-routing; HALT_HUMAN at FIXING entry | Classifier OR troubleshoot marks it (FM-10 l.678); ambiguous API/security/migration/user-default → flagged at classify (l.293) | troubleshoot-time finding attribute in fixtures; asserted at gate (T-430/EC-7) | Low |
| X-007 | Timeout clock basis | Single 30-min wait "after the PR is created"/per review (§FR-A3) | **Per-wait wall-clock**: "wall-clock elapsed time since entering `S3_WAITING_FOR_REVIEW` for the current review wait, not cumulative process lifetime" (l.132) — re-clocked each round | Per-`--timeout` deadline, configurable; EC-6 lets in-flight fix finish past deadline | Medium |
| X-008 | Ungroundable / missing file:line finding handling | Not specified (parser captures path,line; no drop rule) | "Findings without a stable path/line may still be reported, but may not be auto-fixed at level 3 unless `/sc:troubleshoot` can ground them" (l.285) — keep + gate | **Drop**: malformed/missing `file:line` → "finding dropped per hallucination contract, reported as 'ungroundable'" (EC-9 l.285-286) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | A | Capability-ceiling FSM: ordinal is one integer at 3 gates, not 4 code paths ("2³=8 reachable combinations" bug-surface argument, §3.3) | High |
| U-002 | A | Purity / seam-leakage CI tests: AC-9 static assertion that no `gh`/`git` token appears in state-machine/router/loop-guard; R5 seam-leakage risk | High |
| U-003 | A | `locked:false` as a mechanically-enforced hard build gate (AC-8) turning R1 from "should" into a sequencing dependency | High |
| U-004 | B | Write-ahead run-log recovery schema: 29 typed events + `state.snapshot.json` cache + "JSONL is authoritative" conflict rule | High |
| U-005 | B | 12 explicit failure modes FM-1..FM-12 with detection/action/recovery (crash-after-push-before-reply, crash-after-reply-before-resolve, corrupt run-log) | High |
| U-006 | B | `--resume <absolute-run-log-path>` as a first-class CLI flag + resume-reconstruction AC-16 | Med |
| U-007 | C | Fence-post test matrix T-620..T-629 (10 rows) with T-626 canonical off-by-one ("assert round_counter==2 NOT 3") | High |
| U-008 | C | EC-1..EC-16 edge catalog (review-arrives-during-fix, review-disappears-transient, multiple-PRs-same-session, `gh`-not-installed, `--base`-nonexistent) | High |
| U-009 | C | "Validation failure does NOT consume a round" as a named, tested design decision (QD-1/INV-6/T-520) + rubric-tested-independently (QD-6) | Med |

## Shared Assumptions

AD-2 protocol: agreement points scanned across all 3 variants; underlying preconditions enumerated and classified STATED / UNSTATED / CONTRADICTED. UNSTATED preconditions promoted to `[SHARED-ASSUMPTION]` diff points. `[L3-DEBATE]` auto-tag applied to points containing state/guard/boundary terms.

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | The Augment App emits its review via a `gh`-visible surface (reviews / review-comments / issue-comments / check-runs) that a poller can read | All three poll `gh pr view --json reviews,comments` + `gh api …/pulls/<N>/reviews,comments` (A §FR-A3, B l.107-117, C T-201..203) | If Augment emits only via a non-gh-visible channel (web UI webhook, app-only API), the entire poller is unbuildable — this is the source's R1 "unknown" | **UNSTATED** `[SHARED-ASSUMPTION]` |
| A-002 | `/sc:troubleshoot --fix` exists and accepts externally-seeded findings (body + file:line + evidence) without re-deriving | All route Medium→`--fix`, High/Crit→`--depth deep --fix` and seed it (A §4.6, B FR-5, C T-320) | If troubleshoot cannot ingest a seeded finding, FR-3.3 grounding fails and every remediation re-investigates from scratch | **UNSTATED** `[SHARED-ASSUMPTION]` |
| A-003 | The Monitor tool can host a ≥30-min poll loop within one live session without being auto-stopped for low event volume | All host the poller in the Monitor tool (A FR-A3, B "Polling host", C T-230) | The Monitor tool spec auto-stops high-volume monitors and times out long ones; a 30-min ≥30s-interval poll may be evicted, silently killing the loop | **UNSTATED** `[SHARED-ASSUMPTION]` `[L3-DEBATE]` |
| A-004 | A re-review is reliably attributable to the monitor's own push (push→re-review causality is observable) | All count monitor-push-triggered re-review as the next round (A L8.3 SHA-match, B FR-7.6, C INV-3/T-630) | If Augment re-reviews on a timer or batches across pushes, SHA self-attribution mis-keys the round counter → off-by-one or stuck loop | **STATED** (A explicit SHA-match; B/C assert causality but don't prove attribution mechanism) `[L3-DEBATE]` |
| A-005 | Augment's self-reported severity is re-gradable by the reused `sc-auggie-review` rubric into {Critical,High,Medium,Low,Nit} | All re-grade and treat Augment label as a hint (A FR-A4, B l.282, C T-301/QD-6) | If Augment findings lack the fields the rubric keys on (category, confidence, diff-locality), re-grading degrades to pass-through and unknown→Medium dominates | **STATED** |
| A-006 | A GitHub review-comment reply + thread-resolve API path exists and is callable (REST reply + GraphQL resolve) | All post a reply then resolve the thread (A §FR-A8 GraphQL `resolveReviewThread`, B FR-8.5, C T-601/602) | B/C flag the REST-vs-thread endpoint difference as unproven; if review-comment threads aren't resolvable via the assumed call, resolve is a no-op | **STATED** (A asserts the exact GraphQL mutation; B FR-8.5 hedges "if … differs … isolate in helper") `[L3-DEBATE]` |
| A-007 | Local validation (targeted tests + `make lint` + `ruff format --check`) is a sufficient proxy for "fix is safe to push" | All gate push on the same validation triple (A VG-1..4, B gate order, C T-501..511) | A test-passing-but-behavior-breaking fix gets auto-pushed + announced resolved (the source R4 blast-radius); validation is necessary, not sufficient | **UNSTATED** `[SHARED-ASSUMPTION]` `[L3-DEBATE]` |
| A-008 | Findings carry a stable per-thread identity (`comment_id` / `thread_id`) that persists across re-reviews, enabling idempotent reply/dedup | All key idempotency on comment/thread IDs (A `thread_id` at parse, B 5 idempotency sets, C QD-5 comment_id) | If Augment re-posts findings as new comment_ids on re-review, dedup-by-comment_id fails and the same fix is replied twice / re-troubleshooted | **UNSTATED** `[SHARED-ASSUMPTION]` `[L3-DEBATE]` |

## Summary

**Category totals:** Structural (S) 7 · Content (C) 9 · Contradictions (X) 8 · Unique (U) 9 · Shared Assumptions (A) 8 — **41 total**.

**Shared-assumption status counts:** UNSTATED 5 (A-001, A-002, A-003, A-007, A-008) · STATED 3 (A-004, A-005, A-006) · CONTRADICTED 0.

**`[L3-DEBATE]`-tagged (state/guard/boundary):** A-003, A-004, A-006, A-007, A-008.

**High-severity IDs:** S-001, S-003, C-001, C-002, C-005, X-001, X-002, X-004, U-001, U-002, U-003, U-004, U-005, U-007, U-008.
