# Reflect Report — UC-1 Pre-Execution Audit (comboA-r2, shadow)

**Run**: `pre-TASK-WF-designSpec-20261107-075614-comboA-r2` | **Mode**: pre (UC-1) | **Tier**: 2 (pinned) | **Engine**: shadow (legacy authoritative)
**Spec**: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (sha a865f397…)
**Tasklist**: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (sha 044809e3…) — 13 tasks, 5 phases
**Status**: `success` | **Confidence (calibrated)**: 0.767 (mean of 0.80 / 0.65 / 0.85)
**Verdict**: blocking-findings-present — 4 blocking / 7 non-blocking merged findings; the plan is NOT ready to execute as written.

## Headline

The plan is a high-fidelity implementation of the design spec: all 45 extracted requirement rows resolve to plan coverage (union coverage 1.0 after T1 semantic resolution; the deterministic containment floor alone reports 0.5778), the dependency graph is execution-order complete, and the spec's plan-authoring constraints are restated. But three reviewers on three model classes found four contract-level holes that the plan's own acceptance criteria cannot catch, each of which would ship a wrong or unverified artifact: a guard-record type left unpinned (two implementers can pass their own task's ACs with mutually incompatible modules), a resume re-entry contract missing its inputs and expected result, a fold row that never sets the field `guard_status` branches on, and a halt path that reports `released` instead of `unavailable`. All four are one-to-three-line plan-text fixes, not redesigns.

## Coverage (Step 1B.0, D13)

- Pass 1 (ID_REGEX `R-|REQ-|SPEC-|T-`): **0 parsed IDs** in both documents — the spec labels requirements `FR-1..FR-23`, outside the regex. `coverage_pct` (parsed-only): **null**.
- Pass 2 (quote-pinned inference): **45 rows** INF-001..INF-045 (8-row random spot-check clean; evidence validator later re-verified all 45 quotes at their cited lines).
- `coverage_degraded: parsed-sparse` (45 > 0) — table-wide T1-stop pre-filter; the run is T2-pinned regardless.
- Deterministic containment floor: 26/45 (0.5778), 19 unmapped — all 19 semantically resolved COVERED at T1 (cross-cutting constraints restated at plan Constraints level rather than in one task; resolution table in t1-card.md, pressure-tested by the panel).
- **coverage_pct_union: 1.0** (post-resolution); unmapped_requirements_union: [].
- Matrix limitation (reviewer-2, D13 mandate): the 45-row extraction omits three requirement-bearing spans — loop-guard enumeration (spec:242), state-machine overlay (spec:243), public exports (spec:291) — all covered by Tasks 2, 10, 5 respectively. The 1.0 union coverage measures the extraction, not the full spec body.

## Merged findings (adversarial debate, convergence 1.0 disposition / 0.71 confidence-weighted)

### Blocking (execute-no-further; fix plan text first)

| ID | Sev | Cat | Conf | Claim | Where |
|---|---|---|---|---|---|
| MF1 | MAJOR | missing-requirement | 0.85 | `draft_guard_unavailable` halt reports `released`: engage rows 3/8 halt before any request, the fold is None, and guard_status maps no-record to released; no task places the halt override and no AC tests it (Task 3 even asserts released for no record). | spec:112,135-140; plan:61,124 |
| MF2 | MAJOR | contradiction | 0.80 | Fold type unpinned: spec prose says "dict", decision tables read attributes, Task 5's AC subscripts, Task 3 never pins type or Phase string values — incompatible implementations pass their own ACs. | spec:187-192,118-119; plan:56,90 |
| MF3 | MAJOR | unpassable-check | 0.80 | `resume_decision` row 4 must re-enter `release_decision` but its signature lacks `cycle_id`/`target_sha`/`applied_edits`, and the row-4 AC asserts entry conditions, not the expected result — a wrong RELEASE/HOLD cannot fail any AC. | spec:109,166; plan:70,77 |
| MF4 | MAJOR | missing-requirement | 0.75 | `settled(user_override)` sets no `disabled_cause`, but `guard_status` branches on it; fold ACs omit the user_override row and the status AC uses constructed inputs, so a wrong `merge_guard` value ships. | spec:206,112; plan:60-61 |

### Non-blocking (fix before or during execution; none ship wrong artifacts alone)

MF5 (0.70) byte-identical pins compare start-text only (spec:342,377; plan:33,154) · MF6 (0.65) ready-`not_applied`→RELEASE_PENDING-after-failed-release fold variant untested (spec:201; plan:60) · MF7 (0.70) Tasks 9/10/12/13 consume `pre-build-gate.md` without `Depends on: Task 1` (spec:363; plan:120-199) · MF8 (0.55) Task 9's classification-entry allowance contradicts its own AC's exception list (plan:137 vs 142) · MF9 (0.70) release-gate list G4/G5 vs the five gates G1live/G2live/G4/G5/G6 (spec:326; plan:24-26,182) · MF10 (0.70) the no-`file:NNN` rule is stated but no AC tests it (spec:369; plan:23,124-128,143) · MF11 (0.60) resume reconcile-at-any-ordinal (spec:58) vs row-2 REPORT_HELD precedence (spec:164), vacuous below ordinal 3 but unnoted (plan:76).

Full citations per finding: `adversarial/merged-output.md`; debate reasoning: `adversarial/adversarial/debate-transcript.md`.

## Panel record (shadow telemetry)

- Resolution: t1b-1 sonnet (analyzer), t4-1 haiku (qa), t1a-1 opus (refactorer); parity with the legacy class rotation TRUE.
- Identity: requested-pinned. Reviewer-2 self-reported "OpenAI GPT" against the claude-haiku-5-5 pin → `identity_mismatch_suspected: true` (expected under combo A: HAIKU env = claude-gw-tier2, and the resolution pinned tier4; both observations recorded, neither verified from the transcript).
- Findings-block compliance: **2/3 first-parse** (0.6667) — reviewer-2's block carried an out-of-slice `coverage_rows`; the orchestrator's ad-hoc parse had said 3/3, the cluster parser (authoritative) found the defect. After ONE bounded re-ask: 3/3 valid, 13/13 calibrated, agreement 1.0.
- Calibration: opus calibrator, disjoint set empty → `calibrator_diversity: degraded` (all three classes seated as reviewers). Card scores 0.80/0.65/0.85.
- Evidence validator: 46/46 citations founded, **0 dropped**, 45/45 inferred rows verified → `zero-drop-flag: true` recorded (suspect-pass marker per §11.2; the validator's own adversarial self-check is recorded in artifacts/evidence-validation.yaml and its weakest-case note (card 3 F4's range 190-199) is retained).
- verify-citations precheck: 41/41 not-in-snapshot (input snapshot holds only the 2 frozen files; expected for this corpus; all joined the EV re-read set).
- Judge: the tier3 orchestrator session (skill-direct; no separate judge record in the adversarial contract → `judge_identity` recorded, `judge_class_collision: unknown` per protocol).

## Grounding notes

All facts verified at the spec's temporal pin `e8db2fe6` (EventType exactly 43 members; merge_guard.py absent; no import cycle run_log→merge_guard→conflicts→fsm; FIX_APPLIED/PUSH_* /REREVIEW_REQUESTED present; all named test anchors exist). HEAD carries the landed feature and was excluded; the done-package history (answer key) was not read. One spec wording imprecision found (T1 H1): spec F5 calls `--conflict-max-tier` "the one enum flag (`choices=`)" but `--monitor` also uses `choices=` at the pin — not load-bearing for the plan.

## Recommended action

Fix the four blocking findings in the plan text (pin the fold representation + Phase values in Task 3; extend the row-4 contract and its AC; add the user_override fold row and fold-produced status ACs; place and gate the halt override), then re-run this audit (`/sc:reflect --mode pre` on the amended plan). The seven non-blocking items can ride along in the same edit.
