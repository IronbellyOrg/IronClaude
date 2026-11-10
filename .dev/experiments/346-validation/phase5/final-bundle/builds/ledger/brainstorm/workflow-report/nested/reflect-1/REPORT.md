# Reflect report: pre-execution audit of the ledger plan (UC-1)

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.76
citations_total: 62
citations_revalidated: 59
citations_dropped: 3
citations_inferred: 4
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 59` — size of the re-Read set (59 of 62 distinct citations in the body and the 7 blocking findings, plus all 190 inferred-requirement rows).
> - `citations_dropped: 3` — drops observed; this forces `status: partial`.
> - `citations_dropped_extrapolated: 3` — round(3 × 62 / 59).
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.

## Grounding Gaps

Citations the Wave-5 evidence-validator dropped (the findings they support survive on other evidence; only the quotes or attributions fail):

### Gap G-1
- **Hunk ref:** T05-R1-reviewer-L11-699ae853.txt (S1 brief; quoted in M-F21)
- **Evidence missing:** T05 says "write ONLY your output file(s)" and "Do NOT edit the spec"; it does not contain "no edits to the spec or any other file".
- **Why not classifiable:** the quote is attributed to T05 verbatim but only T07 holds both strings.
- **Next evidence needed:** cite each brief's own wording in M-F21 (the finding stands: T05 still forbids writes beyond its output file).

### Gap G-2
- **Hunk ref:** T09-R3-reviewer-L11-1c9a7ec8.txt (S1 brief; quoted in M-F21)
- **Evidence missing:** T09 says "write ONLY that file; do not edit the spec"; neither quoted string appears.
- **Why not classifiable:** substance supported, quote not verbatim.
- **Next evidence needed:** quote T09's own words.

### Gap G-3
- **Hunk ref:** TASK-WF-spec-20261108-181649.md:44, :77 (M-F4)
- **Evidence missing:** `close` is built in Task 1 (plan :44), not Task 3; only `verify` is in Task 3 (plan :77).
- **Why not classifiable:** the "needs `close` from Task 3" part is unfounded; the ordering defect holds because round 3 needs `verify`.
- **Next evidence needed:** none; corrected in the Findings table below (M-F4 now reads "needs `verify` from Task 3").

- Spec: `.dev/tasks/to-do/TASK-WF-spec-20261108-181649/source.md` (byte copy of `.dev/brainstorms/346-ledger/SPEC.md`)
- Tasklist: `.dev/tasks/to-do/TASK-WF-spec-20261108-181649/TASK-WF-spec-20261108-181649.md` (11 tasks, 4 phases)
- Scope the plan was given: spec section 3 and section 4, with section 2 as the behaviour section 3 requires; five owner decisions in the plan's `## Constraints` override the spec.
- Tier 2 was forced: the spec has no labelled requirement IDs (Pass 1: 0 parsed, Pass 2: 190 inferred), so `coverage_degraded: parsed-sparse` forbids a Tier 1 stop; also S_domains = 3 and S_dev_density = 0.48.
- Reviewers: 2 (sonnet analyzer, haiku qa); opus excluded as the executor's class, so `t2_model_class_diversity: degraded`; calibrator opus (disjoint from the reviewers).
- Merge: `/sc:adversarial` Mode A, depth standard, `merge_method: adversarial`, diff-point convergence 1.0, status BLOCKED_BY_INVARIANTS (2 HIGH invariant findings, both carried into the verdict as blocking). Artifacts: `nested/adversarial-1/adversarial/`.

## Verdict

**FAIL (advisory).** The plan is not ready to execute as written: 7 blocking findings, 14 minor findings, 4 low notes. Three blocking findings need an owner decision before anyone runs `/sc:implement` (M-F21, M-F1, M-F3). Reflect is advisory here: the plan file is not edited from these findings.

## Coverage

- `coverage_pct`: null (no parsed IDs). `coverage_pct_union`: 0.5158 (98 of 190 inferred rows matched by the deterministic containment rule).
- The unmatched rows split into: 49 out of scope by the caller's limit (sections 1, 5, 6, 7) plus 6 "Later adopters" rows (source.md:127, "not in this change"); and in-scope rows. Reviewer 2 checked all 37 in-scope unmapped rows: 36 are referenced by a task in other words (lexical misses), 1 (INF-134, the heartbeat) is a true gap.
- Under the stricter standard the debate settled on (a row is covered only when an acceptance criterion would fail if it were violated), INF-005, INF-058 and INF-104 (no role flag, no second computed stop, no event log and no git calls) are also gaps: Task 1 points at them but its import check (plan :53) would accept `subprocess`.
- No row has been shown "checked by an acceptance criterion" one by one; the map in the merged verdict is references only.

## Deviations (UC-1 plan vs spec)

### Deviation D-1: Headline counts deferred rows (owner override)
- **Location:** TASK-WF-spec-20261108-181649.md:21
- **Mapped tasklist item:** Constraints; Task 4
- **Spec section:** §5 "How review 3 critical+major is counted" (source.md:163)
- **Classification:** authorized
- **Classification rationale:** recorded owner decision overriding "the bar is applied to the headline without it"; reviewers agree (D1).
- **Default remediation:** none; tighten the U3 definition (M-F10).

### Deviation D-2: Sweep bullet carries both routes
- **Location:** TASK-WF-spec-20261108-181649.md:125
- **Mapped tasklist item:** Task 6
- **Spec section:** §4 "Sweep route" (source.md:144)
- **Classification:** necessary
- **Classification rationale:** the spec leaves the route open pending a smoke check, so the command must carry both; but the heartbeat half of the condition is missing (M-F20).
- **Default remediation:** add the heartbeat condition.

### Deviation D-3: Sweep dispatch brief names an output file the spec does not give
- **Location:** TASK-WF-spec-20261108-181649.md:172
- **Mapped tasklist item:** Task 9
- **Spec section:** §4 "Sweep route" (source.md:144)
- **Classification:** necessary (reviewer 1 reclassified from drift)
- **Classification rationale:** a dispatch brief needs an output file; the name follows the spec-panel-round3.md pattern and the plan declares the deviation.
- **Default remediation:** mark the name as a placeholder the coordinator may change.

### Deviation D-4: Usage block narrower than the body
- **Location:** TASK-WF-spec-20261108-181649.md:124
- **Mapped tasklist item:** Task 6
- **Spec section:** §3 command block 2 (source.md:95)
- **Classification:** authorized (spec-literal)
- **Classification rationale:** the spec says to drop the line; the plan does not note that `--target-release`, `--output`, `--improve` leave Usage (M-F11).
- **Default remediation:** one declaring line.

## Findings (merged verdict)

Blocking (P0):

| ID | Class | Tasks | Finding | Fix |
|---|---|---|---|---|
| M-F21 | necessary | Constraints, 1, 2, 9 | The verbatim review briefs say "write ONLY your output file" and "no edits to the spec or any other file", but the ledger writes `ledger.json`, snapshots, diffs, inputs and plan files, and `--revert-unclaimed` edits the spec; the variant's Precedence bullet lets the brief win, so the replicate would fail the ledger validity check (source.md:104, :155) | Owner decision before execution; record it in Constraints |
| M-F1 | necessary | Constraints, 6, 7 | Byte-identical copy and "no `src/superclaude` path" cannot both hold: `src/superclaude/commands/spec-panel.md:220` names `src/superclaude/examples/release-spec-template.md` outside every changed block (conflict inherited from source.md:83 vs :124-125) | Keep the whole-file pin; rewrite line 220 under an owner decision naming the template (the installed copy differs from the examples copy); exclude that line from the drift test |
| M-F2 | drift | 5, 7, 8 | The spec's "(that test scans all of `src/`)" is false: `tests/skills/test_review_severity_rule.py:36-52` scans `git ls-files` only, so the new files are never checked; Task 7 lacks the two required assertions; once committed, every other tracked-file scan applies | Add both assertions to the command test; state that all tracked-file scans will apply on commit |
| M-F3 | necessary | 8, Constraints | `tests/recommend/test_routing_refresh.py:647-648` pins the command set (exceptions at :33); a new command breaks it; Task 8 does not run it; fixing it edits an existing test | Run it in Task 8; owner decides the fix; list it in Constraints |
| M-F4 | drift | 2, 3 | Task 2's acceptance criteria need `verify` from Task 3 (G-3); E-CAP and E-TERMINAL hit the same fourth `begin` with no stated order | Move the round-3 and E-CAP tests to Task 3; pin the check order |
| M-F5 | drift | 1, 4, 6 | Review-1 PASS skips the sweep without "document unchanged" (source.md:28); Task 1 (:44) and Task 6 (:125) conflict; and `close` decides at a moment when the document cannot have changed, the reviser edits after it, and the sweep copies r1.md | One skip predicate evaluated at `verdict`/before the sweep; define what `close` writes at a review-1 PASS; sweep the live accepted text; define the k=1 ESCALATE tail |
| M-F20 | drift | 6, 9, 11 | The sweep route checks only that a subagent can be spawned; the spec also requires keeping the 5-minute heartbeat (source.md:144); "heartbeat" appears nowhere in the plan | Require a recorded smoke check covering spawn and a heartbeat interval longer than 5 minutes |

Minor (P1/P2): M-F6 third-fix-cycle E-CAP; M-F7 absence rules (no role flag, no second stop, no event log/git) have no acceptance check; M-F8 brief-diff check is weak (one-line briefs); M-F9 INSTALL completeness check trips on pre-existing untracked files; M-F10 U3 counts deferred/outside/sweep rows and sweep challenges may count twice; M-F11 Usage narrower than body; M-F12 old guards (one review per run, no Improve step) not carried; M-F13 reviser rules and byte-size reporting dropped (owner note, spec-origin); M-F14 bytes per claim (owner note); M-F15 no coordinator skip rule after an early loop end; M-F16 no recovery for E-REPORT-EDITED; M-F17 `regressed`/`cannot-verify` target statuses undefined; M-F18 reviser `answer` runs before hunks exist; M-F19 paragraph unit, difflib autojunk and `HUNKS_LARGE` undefined. Low notes: counters relation, sweep context sees counts in `--sweep` mode, description suffix inside the YAML quotes, title and examples still name `/sc:spec-panel`. Full text and file:line evidence: `nested/adversarial-1/adversarial/merged-verdict.yaml`.

## Risk register

- R1 (high): executing the plan as written fails Task 6's own grep on M-F1, and M-F2 and M-F3 surface later (at commit or in the full test suite, since Task 8 runs neither the routing test nor a scan of untracked files); it also produces an experiment arm that may not honour the ledger at all (M-F21).
- R2 (high): the review-1 PASS path can report a delivery PASS for text no one reviewed (M-F5).
- R3 (medium): the sweep route can pick the subagent path on a host where the heartbeat dies mid-sweep (M-F20).
- R4 (medium): spec-internal gaps the plan inherited (M-F13, M-F14, the false premise in M-F2) need owner notes, not executor guesses.

## Inferred-claim audit

- `citations_inferred: 4`
- Inferred-fraction: `4 / 62` = 0.06
- [INFERRED] "Five owner decisions": Constraints has four bullets labelled "Owner decision"; the fifth (sweep kept) sits inside the briefs bullet (plan :22).
- [INFERRED] M-F5 "copies r1.md": plan :91 says "accepted snapshot"; r1.md follows only on a review-1 PASS.
- [INFERRED] M-F20 "a smoke check under 5 minutes passes trivially" is reasoning, not a quoted fact.
- [INFERRED] the earlier R1 wording "fails at Tasks 6-8" (corrected above).
- Validator self-audit: all 190 inferred rows match their cited source.md lines exactly; coverage arithmetic (98/190 = 0.5158) re-derived; D-4 lists three flags where M-F11 lists four (adds `--report-dir`), minor.

## Recommendations

### Recommendation R-001: Get the owner's decision on brief ownership vs ledger writes
- **File:** .dev/tasks/to-do/TASK-WF-spec-20261108-181649/TASK-WF-spec-20261108-181649.md (Constraints)
- **Change:** Record whether the verbatim T05/T07/T09 ownership text permits the ledger folder writes and the scripted spec revert, or how the variant overrides it.
- **Verifier:** a Constraints bullet naming the decision; re-run `/sc:reflect --mode pre` on the regenerated plan.
- **Linked deviation(s):** M-F21
- **Priority:** P0

### Recommendation R-002: Resolve the copy-vs-path conflict at spec-panel.md:220
- **File:** .dev/tasks/to-do/TASK-WF-spec-20261108-181649/TASK-WF-spec-20261108-181649.md (Tasks 6, 7; Constraints)
- **Change:** Owner names the template line 220 should point to; Task 6 rewrites that line; Task 7's drift test excludes it.
- **Verifier:** `grep -n 'src/superclaude' src/superclaude/commands/spec-panel-ledger.md` prints nothing and the drift test passes.
- **Linked deviation(s):** M-F1
- **Priority:** P0

### Recommendation R-003: Fix the test plan for the repo's own scans
- **File:** same plan (Tasks 7, 8; Constraints)
- **Change:** Task 7 asserts banned phrases and cap numbers on the new files; Task 8 runs `tests/recommend/test_routing_refresh.py`; Constraints lists it with the owner's chosen outcome.
- **Verifier:** `uv run pytest tests/skills/test_spec_panel_ledger_command.py tests/recommend/test_routing_refresh.py -q` with the recorded outcome.
- **Linked deviation(s):** M-F2, M-F3
- **Priority:** P0

### Recommendation R-004: Fix task ordering and the review-1 PASS path
- **File:** same plan (Tasks 1-4, 6)
- **Change:** Move round-3/E-CAP tests to Task 3 and pin the E-CAP/E-TERMINAL order; write one skip predicate evaluated at `verdict`, define the review-1 PASS tail, and sweep the live accepted text.
- **Verifier:** the regenerated Task 2 AC lists only behaviours reachable with `init`, `find`, `answer`, `begin`, `close`; Task 1/4/6 text uses the same predicate.
- **Linked deviation(s):** M-F4, M-F5
- **Priority:** P0

### Recommendation R-005: Add the heartbeat condition to the sweep route
- **File:** same plan (Tasks 6, 9, 11)
- **Change:** Subagent route only after a recorded smoke check covering spawn and a heartbeat interval longer than 5 minutes.
- **Verifier:** `grep -n heartbeat` on the regenerated plan finds the condition in Tasks 6, 9 and 11.
- **Linked deviation(s):** M-F20
- **Priority:** P0

### Recommendation R-006: Close the minor gaps when the plan is regenerated
- **File:** same plan
- **Change:** Apply the minor fixes listed for M-F6 to M-F19 (absence-rule checks, INSTALL check scope, U3 definition, carried guards, kernel definitions, owner notes).
- **Verifier:** each fix appears as an acceptance criterion or a Constraints note in the regenerated plan.
- **Linked deviation(s):** M-F6 to M-F19
- **Priority:** P1

## Inferred requirements (Pass 2)

Match result is the deterministic containment rule (>= 0.6 content-word overlap with one task); 'none' can be a wording miss, see Coverage.

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | Theme: find once (review 1), then only verify ledger rows, with a script that owns the rows, the counters and the verdict. | source.md:13 | none (best Task 1 0.583) |
| INF-002 | One stdlib Python script, `review_ledger.py`, is the only writer of the ledger. | source.md:17 | none (best Task 1 0.571) |
| INF-003 | Models never edit ledger state: they write small JSON input files and their own reports, and the script validates and ingests them atomically. | source.md:17 | none (best Task 1 0.526) |
| INF-004 | Every call is `uv run --no-project python "<skill base>/scripts/review_ledger.py" <subcommand> ...` | source.md:17 | containment Task 5 (1.0) |
| INF-005 | The actor is implied by the subcommand; there is no role flag. | source.md:17 | none (best Task 3 0.167) |
| INF-006 | `<doc dir>/<doc stem>.review-ledger/` by default (overridable with `--ledger <dir>`), holding `ledger.json`, `snapshots/r1.md r2.md r3.md` (the exact text each review saw), `diffs/c1.json c2.json`, `inputs/*.json`, `plan-r2.md plan-r3.md` and `.lock`. | source.md:19 | containment Task 1 (0.6) |
| INF-007 | The path is derivable from the document alone, so a session that loses a flag still finds the ledger, and `init` refuses when one exists (`E-EXISTS`): a lost flag can never restart a first review | source.md:19 | none (best Task 1 0.524) |
| INF-008 | For S1: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger/`. | source.md:19 | containment Task 9 (1.0) |
| INF-009 | **Review 1 (FIND, the only full find pass).** Fresh reviewer session. | source.md:23 | containment Task 6 (0.625) |
| INF-010 | `init --doc D --profile spec-panel` snapshots `D` as `r1.md` and prints `review: 1 of 3`. | source.md:23 | containment Task 1 (1.0) |
| INF-011 | The panel runs unchanged over the whole document. | source.md:23 | none (best Task 1 0.2) |
| INF-012 | Each finding becomes a row in `inputs/r1-find.json` with `grade` (CRITICAL/MAJOR/MINOR), `rule` (for example FR-8), `wrong_outcome` and an exact anchor quote; `find` checks each anchor is present once (`E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`), and the profile, not the model, computes `blocking = grade == CRITICAL or rule in {FR-8, FR-9} or (grade == MAJOR and wrong_outcome non-empty)`, which is 427's grading rule (`spec-panel.md:259`) made a formula. | source.md:23 | none (best Task 1 0.556) |
| INF-013 | Non-blocking rows are stored `deferred`. | source.md:23 | containment Task 1 (1.0) |
| INF-014 | `close --report R1` appends the script tail (rendered ledger, Reviser brief, decision line) to the report. | source.md:23 | containment Task 1 (0.846) |
| INF-015 | **Revise 1.** Separate reviser session, brief unchanged. It edits `D` from the Reviser brief in the report. | source.md:24 | none (best Task 1 0.3) |
| INF-016 | Running `answer` (claim hunks per blocking row) is optional, because the S1 reviser briefs run no script. | source.md:24 | containment Task 2 (0.615) |
| INF-017 | Answers on a `deferred` row are refused (`E-ILLEGAL`), so a minor row can never be "fixed" through the ledger. | source.md:24 | containment Task 1 (0.6) |
| INF-018 | **Review 2 (VERIFY).** Fresh reviewer session. | source.md:25 | containment Task 6 (0.667) |
| INF-019 | `begin --doc D` snapshots `r2.md`, diffs it against `r1.md` (difflib, whitespace-insensitive, old and new ranges, deletion tombstones), applies reviser answers, then **auto-claims** every remaining hunk that overlaps an open blocking row's anchor span widened to its enclosing paragraph (this is what lets a cycle progress when the reviser never ran `answer`). | source.md:25 | containment Task 2 (0.795) |
| INF-020 | Hunks no blocking row claims are **unclaimed**: reported with their bytes, and restored to the snapshot text only when the invocation carries `--revert-unclaimed` | source.md:25 | containment Task 2 (0.933) |
| INF-021 | `begin` writes `plan-r2.md`: every blocking row still open, its frozen grade and wrong outcome, its old anchor and the old and new text of its hunks, plus the unclaimed hunks. | source.md:25 | containment Task 2 (0.947) |
| INF-022 | The verifier answers every plan row once with `resolved`, `open`, `regressed` or `cannot-verify`, an evidence quote that must exist in the new snapshot, and `touched_ok` (did the change break the sentence it touched; `no` requires a child row). | source.md:25 | containment Task 3 (0.714) |
| INF-023 | Then one **new-defect check** over this round's hunks only, both diff sides. | source.md:25 | none (best Task 2 0.556) |
| INF-024 | A new row anchored inside a hunk is `scope=in` and can block (`origin=changed`, `caused_by` = the rows that claimed the hunk). | source.md:25 | containment Task 3 (1.0) |
| INF-025 | An allegation outside the hunks is not refused: it is stored `scope=outside`, never blocks, and is counted in the measurement headline, so nothing lives only in report prose. | source.md:25 | containment Task 3 (0.6) |
| INF-026 | `verify` refuses a missing plan answer (`E-INCOMPLETE`). `close` computes the decision. | source.md:25 | containment Task 3 (0.778) |
| INF-027 | **Revise 2.** As revise 1. | source.md:26 | none (best None 0.0) |
| INF-028 | **Review 3 (VERIFY, last).** As review 2 against `r2.md`; the decision can only be PASS or ESCALATE. | source.md:27 | containment Task 3 (0.7) |
| INF-029 | **Final sweep (once, not a review, never looped).** A fresh context that has not read the ledger critiques the whole accepted snapshot, given as a copy in a temporary folder by `sweep --prepare`. | source.md:28 | none (best Task 4 0.474) |
| INF-030 | Its rows are stored `deferred` with `round_found=sweep` and a location class (`in_claimed_span`, `in_unclaimed_hunk`, `outside_hunks`). | source.md:28 | containment Task 4 (1.0) |
| INF-031 | A blocking sweep row, or a sweep challenge to a verified row, makes the **delivery outcome** ESCALATE; it never opens a cycle. | source.md:28 | containment Task 4 (0.75) |
| INF-032 | The sweep is skipped only after a review-1 PASS with the document unchanged. | source.md:28 | containment Task 4 (0.714) |
| INF-033 | **Status transitions (only the script writes; merged s3 has the full T1 to T12 table).** | source.md:30 | none (best Task 1 0.4) |
| INF-034 | \| none \| `open` / `deferred` \| `find` (review 1), `verify` new row (reviews 2, 3), `sweep` (always `deferred`) \| anchor absent or repeated; a verify row outside the hunks becomes `scope=outside`, `deferred` \| | source.md:34 | containment Task 1 (0.667) |
| INF-035 | \| `open`, `reopened` \| `fixed` \| reviser `answer`, or the script's auto-claim at `begin` \| row not blocking or not listed; claim wider than the row's paragraph (`E-CLAIM-WIDE`); a `fixed` answer with no edit in the span (`E-FIXED-NO-EDIT`) \| | source.md:35 | containment Task 2 (0.895) |
| INF-036 | \| `fixed` \| `verified` \| verifier `resolved` \| evidence quote not in the new snapshot; anchor unmappable \| | source.md:36 | containment Task 3 (0.7) |
| INF-037 | \| `fixed` \| `open` or `reopened` \| verifier `open` (`reopened` if the row was ever verified, from history) \| no reason or quote \| | source.md:37 | containment Task 3 (0.9) |
| INF-038 | \| `verified` \| `fixed` \| script at `begin`, when this round's hunk touches the row's span \| never; then `regressed` is allowed \| | source.md:38 | containment Task 2 (0.786) |
| INF-039 | \| `verified` (untouched) \| `reopened` \| nobody \| `E-NOT-CHANGED`: accepted text cannot be re-attacked \| | source.md:39 | none (best Task 3 0.556) |
| INF-040 | \| `deferred` \| anything \| nobody \| `E-ILLEGAL` \| | source.md:40 | none (best Task 1 0.5) |
| INF-041 | \| any frozen field \| changed \| nobody \| `E-FROZEN` (frozen at creation: id, grade, rule, wrong_outcome, blocking, anchor, origin, scope, caused_by, finding text) \| | source.md:41 | containment Task 1 (0.706) |
| INF-042 | \| any loop step after a terminal decision \| \| nobody \| `E-TERMINAL` (only the single sweep and `status` run after it) \| | source.md:42 | containment Task 3 (0.818) |
| INF-043 | A dispute is a flag on a claim, not a status; the verifier rules on it, and an unruled dispute at the cap counts as open. | source.md:44 | containment Task 3 (0.9) |
| INF-044 | `ledger.json` carries `body_sha256`; a hand edit is refused `E-TAMPERED`. | source.md:44 | containment Task 1 (1.0) |
| INF-045 | Mutations hold a nonblocking per-ledger lock and take `--op` and `--expect-seq`; an identical retry returns the committed result instead of using a slot. | source.md:44 | containment Task 1 (0.75) |
| INF-046 | **Termination, computed by the script after each review k (k = 1, 2, 3):** | source.md:46 | containment Task 1 (0.778) |
| INF-047 | U = rows with blocking and scope == in and status in {open, fixed, reopened} | source.md:49 | containment Task 3 (1.0) |
| INF-048 | X = cannot-verify answers this round + unmappable anchors + failed revert preimages | source.md:50 | containment Task 2 (0.778) |
| INF-049 | I = ledger hash valid and snapshots intact and every plan row answered | source.md:51 | none (best Task 1 0.444) |
| INF-050 | loop_decision = ESCALATE  if not I or X > 0 | source.md:52 | containment Task 1 (1.0) |
| INF-051 | PASS      if U == 0 | source.md:53 | containment Task 1 (1.0) |
| INF-052 | CONTINUE  if k < 3 | source.md:54 | containment Task 1 (0.667) |
| INF-053 | ESCALATE  otherwise | source.md:55 | none (best Task 1 0.5) |
| INF-054 | after the sweep: S = blocking sweep rows + blocking sweep challenges to verified rows | source.md:56 | containment Task 4 (1.0) |
| INF-055 | delivery_outcome = ESCALATE if loop_decision == ESCALATE or S > 0, else PASS | source.md:57 | containment Task 1 (0.857) |
| INF-056 | The review counter advances only on a committed `begin`; a fourth review or a third fix cycle is refused (`E-CAP`, constant `CAP_REVIEWS = 3` tied by a test to the pinned text `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`, `tests/skills/test_review_severity_rule.py:215`). | source.md:60 | none (best Task 1 0.516) |
| INF-057 | The sweep is outside the 3-review cap: it cannot start a fix cycle and its report header is `sweep`, never `review: 4 of 3`. | source.md:60 | containment Task 3 (0.643) |
| INF-058 | There is no second computed stop (no "count did not shrink" halt) | source.md:60 | none (best Task 3 0.286) |
| INF-059 | The reviewer may write its own verdict (the S1 briefs ask for one); the script's tail is always the report's last lines: CONTINUE ends `verdict: FAIL`, a terminal review before the sweep ends `loop: PASS (sweep pending)` or `loop: ESCALATE (sweep pending)`, and the sweep report ends `verdict: PASS` or `verdict: FAIL` from the delivery outcome. | source.md:60 | containment Task 1 (0.75) |
| INF-060 | `begin` refuses an edited tail (`E-REPORT-EDITED`). | source.md:60 | containment Task 3 (1.0) |
| INF-061 | The read-only `verdict` subcommand exits 0 PASS, 10 CONTINUE, 11 ESCALATE and, settled here (the merge left it open), **12 PENDING** while the loop is terminal but the sweep has not run, so no caller can read an early loop PASS as a delivery PASS. | source.md:60 | containment Task 1 (0.667) |
| INF-062 | Every other committed operation exits 0 whatever the decision. | source.md:60 | none (best Task 1 0.571) |
| INF-063 | The ledger moves five duties to the script: the row list and statuses (a plan file instead of a re-read report), the origin tag (computed from hunks), the baseline and counter (script snapshots), the scope (rows outside hunks cannot block), and the verdict (computed, last line). | source.md:62 | none (best Task 1 0.429) |
| INF-064 | Grade is frozen per row, so it cannot drift upward between rounds. | source.md:62 | none (best Task 3 0.5) |
| INF-065 | \| Fresh whole-document re-review after each fix \| removed for reviews 2 and 3; replaced by one sweep that cannot loop \| MECHANICAL \| | source.md:68 | containment Task 6 (0.8) |
| INF-066 | \| Severity drift between rounds \| removed for existing rows (`E-FROZEN`); left for new rows, graded once by a model \| MECHANICAL / PROSE \| | source.md:70 | none (best Task 3 0.267) |
| INF-067 | \| Reviser applies minor findings \| removed outside blocking paragraphs (unclaimed, reverted with the flag); LEFT inside a blocking row's paragraph (auto-claim admits it) \| MECHANICAL, with a leak \| | source.md:71 | none (best Task 2 0.55) |
| INF-068 | \| No mechanical stop; verdict is reviewer judgement \| removed: counter, cap, terminal phase, computed last line \| MECHANICAL \| | source.md:73 | none (best Task 1 0.385) |
| INF-069 | **Stateful single reviewer vs file ledger: file ledger, recommended.** | source.md:75 | none (best Task 9 0.429) |
| INF-070 | All additive. Nothing existing is edited: `src/superclaude/commands/spec-panel.md`, its `plugins/` copy, `HOW-WE-WORK.md`, the severity pins and routing stay as they are until S1 proves the variant. | source.md:79 | none (best Task 11 0.4) |
| INF-071 | \| `src/superclaude/commands/spec-panel-ledger.md` (new) \| Copy of `spec-panel.md` with three blocks changed (below). \| | source.md:83 | containment Task 6 (0.818) |
| INF-072 | \| `src/superclaude/skills/sc-review-ledger/SKILL.md` (new) \| Delegate-only skill (no slash command, like `sc-bare-review`): ledger layout, input schemas, `PROFILES`, transition table, CLI, how to add a profile. \| | source.md:84 | containment Task 5 (0.913) |
| INF-073 | \| `src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py` (new) \| The kernel. Stdlib only (`argparse`, `json`, `hashlib`, `difflib`, `fcntl`, `os`, `pathlib`, `re`). \| | source.md:85 | none (best Task 2 0.529) |
| INF-074 | \| `tests/skills/test_review_ledger_script.py` (new) \| Behaviour tests, loading the script by path as `tests/skills/test_workflow_archive.py` does. \| | source.md:86 | containment Task 1 (0.8) |
| INF-075 | \| `tests/skills/fixtures/review-ledger/` (new) \| Tiny documents and input JSON for the edge cases. \| | source.md:87 | containment Task 1 (0.636) |
| INF-076 | \| `tests/skills/test_spec_panel_ledger_command.py` (new) \| Text pins and the drift test. \| | source.md:88 | containment Task 7 (0.75) |
| INF-077 | \| `docs/designs/spec-panel-ledger.md` (new, after approval) \| This design. \| | source.md:89 | containment Task 10 (0.857) |
| INF-078 | so the script reaches `~/.claude/skills/sc-review-ledger/scripts/`. | source.md:91 | containment Task 5 (0.833) |
| INF-079 | The skill must not be named `sc-spec-panel-ledger` | source.md:91 | containment Task 5 (0.667) |
| INF-080 | Frontmatter `name: spec-panel-ledger`, description "... with a script-kept finding ledger (find once, then verify)". | source.md:94 | containment Task 6 (1.0) |
| INF-081 | Usage line: drop `[--re-review <prior-findings-file> --baseline <saved-copy>]`, add `[--ledger <dir>] [--revert-unclaimed] [--sweep]`; drop the `--unattended` usage line. | source.md:95 | containment Task 6 (0.857) |
| INF-082 | `## Unattended mode` is omitted, because `tests/skills/test_worker_contract.py:831-839` requires the set of commands with that heading to equal `UNATTENDED_COMMANDS`; instead the new section's first line refuses a standalone `--unattended` token ("spec-panel-ledger has no unattended mode") so it is never silently ignored. | source.md:95 | none (best Task 6 0.481) |
| INF-083 | `## Review Loop` replaced by `## Review Ledger Loop`, one line per bullet so the repo's line matchers see each whole: | source.md:96 | containment Task 6 (0.667) |
| INF-084 | **Setup**: critique only; invoke `Skill sc-review-ledger` (`~/.claude/skills/` first, then the project `.claude/skills/`); the ledger is `--ledger` or `<doc dir>/<doc stem>.review-ledger/`; run `init` if absent, else `begin`; a refusal stops the run and never falls back to a first review. | source.md:97 | containment Task 6 (0.64) |
| INF-085 | **Find**: the full panel; each finding becomes a row with grade, rule, wrong outcome and an exact anchor quote; the script decides what blocks. | source.md:98 | none (best Task 1 0.529) |
| INF-086 | **Verify**: answer every row in `plan-r<k>.md`; run one new-defect check on this round's hunks; anything else is filed `scope=outside`. | source.md:99 | none (best Task 2 0.556) |
| INF-087 | **Sweep**: run only on the copy that `sweep --prepare` prints; never open the ledger folder. | source.md:100 | containment Task 6 (1.0) |
| INF-088 | **Report**: write what the brief asks; never edit the lines `close` appends. | source.md:101 | containment Task 1 (0.7) |
| INF-089 | **Cap**: `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`, then `HALT and escalate to the user with the open blocking findings` (both verbatim); `review: N of 3` comes from the script. | source.md:102 | containment Task 6 (0.947) |
| INF-090 | **Reviser contract**: revise only text a listed blocking row names; minor rows are not answerable; unclaimed edits are reported and, with `--revert-unclaimed`, restored. | source.md:103 | none (best Task 2 0.562) |
| INF-091 | **Precedence**: a brief may narrow this scope, not widen it, and cannot change a grade or a script verdict. | source.md:104 | none (best Task 1 0.4) |
| INF-092 | Output is one JSON object on stdout (`{ok, seq, phase, review, fix_cycles, counts, loop_decision, delivery_outcome, next_action}` or `{error, detail, next_action}`). | source.md:106 | containment Task 1 (1.0) |
| INF-093 | Exit codes: 0 committed (whatever the decision); 1 usage; 2 input refused (row level); 3 state refused; 4 lock or sequence conflict; `verdict` alone uses 0/10/11/12 (PASS/CONTINUE/ESCALATE/PENDING). | source.md:106 | containment Task 1 (0.862) |
| INF-094 | \| `init --doc D --profile spec-panel [--archive-existing]` \| review 1 \| creates ledger, `r1.md` \| `E-EXISTS` (rerun needs `--archive-existing`, which renames the old folder) \| | source.md:110 | containment Task 1 (0.889) |
| INF-095 | \| `find --input F` \| review 1 \| adds rows, computes `blocking`, defers the rest; accepts `[]` \| `E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`, `E-SCHEMA`, `E-PHASE` \| | source.md:111 | containment Task 1 (0.812) |
| INF-096 | \| `answer --input F` \| reviser (optional) \| claims hunks per blocking row; optional `gap` entries \| `E-ILLEGAL`, `E-CLAIM-WIDE`, `E-FIXED-NO-EDIT`, `E-TERMINAL` \| | source.md:112 | containment Task 2 (1.0) |
| INF-097 | \| `begin --doc D [--revert-unclaimed]` \| reviews 2, 3 \| snapshot, diff, auto-claim, optional revert, writes `plan-r<k>.md` \| `E-TAMPERED`, `E-REPORT-EDITED`, `E-CAP`, `E-TERMINAL` \| | source.md:113 | containment Task 2 (0.85) |
| INF-098 | \| `verify --input F` \| reviews 2, 3 \| applies answers, adds `scope=in` and `scope=outside` rows \| `E-INCOMPLETE`, `E-ANCHOR`, `E-FROZEN`, `E-NOT-CHANGED` \| | source.md:114 | containment Task 3 (0.75) |
| INF-099 | \| `close --report R` \| each review \| computes `loop_decision`, appends the tail and its digest \| `E-PHASE` \| | source.md:115 | containment Task 1 (1.0) |
| INF-100 | \| `sweep --prepare` / `sweep --input F --report R` \| session holding the ledger \| copy for the sweep; ingests sweep rows, sets `delivery_outcome`, re-checks every prior tail \| `E-SWEEP-DONE`, `E-PHASE` \| | source.md:116 | containment Task 4 (0.842) |
| INF-101 | \| `status`, `verdict` \| anyone \| read-only counts, metrics, post-terminal edits by hash \| none \| | source.md:117 | none (best Task 4 0.5) |
| INF-102 | \| `revert-unclaimed [--hunk k]`, `defer --id --quote` \| reviser; coordinator \| restore own unclaimed hunk (preimage-checked); record a user's words (no status change) \| `E-PHASE` \| | source.md:118 | none (best Task 2 0.526) |
| INF-103 | Writes: temp file, fsync, `os.replace`, under `fcntl.flock` on `.lock`; idempotency by request digest within phase and round. | source.md:120 | containment Task 1 (0.846) |
| INF-104 | No event log, no git calls (snapshots are copies because a `.dev/` document may be untracked, `docs/designs/spec-panel-review-loop.md:50`). | source.md:120 | none (best Task 10 0.357) |
| INF-105 | Script: every transition and refusal code | source.md:123 | containment Task 3 (0.75) |
| INF-106 | the blocking formula for CRITICAL, FR-8 with MINOR, MAJOR with and without wrong outcome, MINOR | source.md:123 | containment Task 1 (1.0) |
| INF-107 | auto-claim with zero, one and two rows; paragraph admission on a pure rewrap | source.md:123 | containment Task 2 (1.0) |
| INF-108 | unclaimed hunks kept without the flag and restored with it; failed preimage gives `cannot-verify` | source.md:123 | containment Task 2 (0.778) |
| INF-109 | `scope=outside`; `E-TERMINAL`; empty `find`; zero-hunk round; half-open range and deletion edges; anchor relocation ending missing or ambiguous | source.md:123 | containment Task 2 (0.75) |
| INF-110 | identical retry under a new op id; stale sequence; two writers; `E-TAMPERED`; `E-REPORT-EDITED` | source.md:123 | containment Task 1 (0.727) |
| INF-111 | `verdict` exit 12 before the sweep; `CAP_REVIEWS == 3` tied to `CANONICAL_CAP_TEXT`. | source.md:123 | containment Task 1 (0.889) |
| INF-112 | Command: `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` present (imported from `tests/skills/test_review_severity_rule.py`) | source.md:124 | containment Task 7 (0.889) |
| INF-113 | eight one-line bullets in order; subcommand and flag names present | source.md:124 | containment Task 7 (1.0) |
| INF-114 | the `--unattended` refusal line present; no `## Unattended mode` | source.md:124 | containment Task 7 (1.0) |
| INF-115 | no `src/superclaude` path; dual lookup order | source.md:124 | containment Task 6 (0.667) |
| INF-116 | none of the banned severity phrases and no cap number above 2 (that test scans all of `src/`). | source.md:124 | none (best Task 3 0.364) |
| INF-117 | Drift test: the variant equals `spec-panel.md` outside the frontmatter name and description, the Usage block, the loop section and `## Unattended mode`, so the copied panel cannot silently diverge. | source.md:125 | containment Task 7 (0.75) |
| INF-118 | **Later adopters (not in this change; each a separate change gated on S1).** | source.md:127 | none (best Task 9 0.333) |
| INF-119 | The kernel knows no spec-panel words: an adopter adds one `PROFILES` row (grade vocabulary, blocking predicate, cap, ordered stop guards) and a short adapter section. | source.md:127 | none (best Task 1 0.4) |
| INF-120 | **rf-qa agents** (`src/superclaude/agents/rf-qa.md:379-416`): first adopter after spec-panel. | source.md:128 | none (best Task 1 0.4) |
| INF-121 | the ledger replaces "the previous QA report" with `plan-r<k>.md`, step 5's verdict with `verdict`, and its prose monotonicity halt `\|F_{n+1}\| < \|F_n\|` (`:401`) with a profile guard run in rf-qa's own order (regression first, `:407`). | source.md:128 | none (best Task 6 0.379) |
| INF-122 | **`/sc:reflect`**: rows created only from findings that pass its evidence-validator gate | source.md:129 | none (best Task 11 0.375) |
| INF-123 | A ledger PASS never authorizes promotion. | source.md:129 | containment Task 1 (0.6) |
| INF-124 | **`/sc:implement` final review**: not adopted. | source.md:130 | none (best Task 6 0.4) |
| INF-125 | **Name**: `spec-panel-ledger`, invoked as `/sc:spec-panel-ledger`; source `src/superclaude/commands/spec-panel-ledger.md`; installed copy `~/.claude/commands/sc/spec-panel-ledger.md`, next to the unchanged `~/.claude/commands/sc/spec-panel.md`. | source.md:134 | containment Task 11 (0.733) |
| INF-126 | Its skill installs to `~/.claude/skills/sc-review-ledger/` (with `scripts/review_ledger.py`). | source.md:134 | containment Task 5 (1.0) |
| INF-127 | The original file is never edited by the experiment. | source.md:135 | containment Task 6 (0.6) |
| INF-128 | copy `spec-panel-ledger.md` into `~/.claude/commands/sc/` and the `sc-review-ledger/` folder into `~/.claude/skills/`; record their sha256 in the install watcher. | source.md:136 | containment Task 11 (0.769) |
| INF-129 | Nothing else in `~/.claude/` changes; no `superclaude install`. | source.md:136 | containment Task 11 (1.0) |
| INF-130 | **The one-line substitution** (in the three S1 review briefs only; reviser briefs stay verbatim): | source.md:137 | containment Task 9 (0.778) |
| INF-131 | /sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger --revert-unclaimed | source.md:140 | containment Task 9 (1.0) |
| INF-132 | All other flags on the line (`@<spec> --mode critique --focus requirements,architecture`) stay. No `--re-review`, no `--baseline`. | source.md:143 | none (best Task 9 0.583) |
| INF-133 | `--revert-unclaimed` is the consent that lets `begin` restore edits no blocking row claims; it is part of the treatment and is recorded as such. | source.md:143 | containment Task 2 (0.615) |
| INF-134 | if a throwaway dispatched worker with the T09 wrapper can spawn an Agent-tool subagent and keep its 5-minute heartbeat, the sweep is a subagent of the terminal review session (still 5 dispatches). | source.md:144 | none (best Task 6 0.444) |
| INF-135 | Otherwise it is a sixth dispatch, `/sc:spec-panel-ledger @<spec> --mode critique --focus requirements,architecture --ledger <same path> --sweep`, declared as a deviation. | source.md:144 | containment Task 9 (0.765) |
| INF-136 | identical to Arm B as fixed in `DECISIONS.md` D11 (S1, base commit 2cb683f5, overlay, verbatim briefs T05 to T09, model claude-opus-5-5, `WORKER-CONTRACT.md` moved aside, install watcher), except the three recorded differences: the one-line substitution of section 4, the `--revert-unclaimed` flag inside it, and the sweep route. | source.md:148 | none (best Task 9 0.4) |
| INF-137 | Comparators, reused: control ctl-r1/ctl-r2 and Arm B flg-r1/flg-r2. | source.md:148 | none (best Task 9 0.222) |
| INF-138 | Reruns of an aborted replicate use `init --archive-existing`, never a manual delete. | source.md:148 | none (best Task 1 0.444) |
| INF-139 | Smoke check for the sweep route (section 4). | source.md:151 | containment Task 9 (1.0) |
| INF-140 | Baseline sweeps: run the same sweep (a whole-document `/sc:spec-panel` critique on a copy) on the FINAL spec of all six existing replicates. | source.md:152 | none (best Task 6 0.467) |
| INF-141 | If it is 3 or more, the combined bar cannot be met by the ledger alone, and the loop number and the sweep number are reported separately as the primary result. | source.md:152 | none (best Task 1 0.267) |
| INF-142 | Hunk parity: run the script's diff on the three S1 history pairs (`exp346-ab-flg-r2/.dev/orca-command-refactor/specs/history/`) and fix the paragraph unit and the `HUNKS_LARGE` threshold from them. | source.md:153 | none (best Task 11 0.35) |
| INF-143 | V1-ledger: `ledger.json` shows rounds 1 to 3 (or an earlier terminal decision), the snapshots, and a sweep record; a replicate whose sessions never ran the script is "ledger not honoured" and is not treatment | source.md:155 | none (best Task 1 0.476) |
| INF-144 | A sweep report that cites a ledger row id fails V1-ledger (the sweep read the ledger). | source.md:155 | none (best Task 1 0.556) |
| INF-145 | A blinded audit of `wrong_outcome` texts: more than 30% judged filler marks the replicate "grading not honoured". | source.md:155 | none (best Task 1 0.083) |
| INF-146 | Also recorded: command, skill and script sha256; auto-claim count per cycle; every reviewer-vs-script verdict disagreement; one `status` after the last dispatch. | source.md:155 | none (best Task 4 0.529) |
| INF-147 | D5 M1 to M5 (`DECISIONS.md:23`), read from the ledger, not from report prose | source.md:157 | none (best Task 1 0.222) |
| INF-148 | Plus: unclaimed and reverted bytes per cycle, `minor_touched` (edits inside a deferred row's span, split by "answered" and "auto-claimed"), `scope=outside` count, `X` count, script calls, sessions and wall time per step. | source.md:157 | containment Task 4 (0.68) |
| INF-149 | The headline is therefore the union, each defect counted once: | source.md:159 | none (best Task 3 0.333) |
| INF-150 | `U3`: CRITICAL or MAJOR rows (by grade, as Arm B's proxy counted by grade, `ARMB-REPORT.md:37`) not `verified` after review 3, child rows included; | source.md:160 | containment Task 4 (0.722) |
| INF-151 | `W`: sweep CRITICAL or MAJOR rows plus sweep challenges to verified rows; | source.md:161 | containment Task 4 (1.0) |
| INF-152 | `O`: `scope=outside` CRITICAL or MAJOR rows (verify-time allegations outside the hunks). | source.md:162 | containment Task 4 (0.667) |
| INF-153 | Duplicates between sets are ruled by a blinded analyst; the raw and auto-matched counts are published as bounds. | source.md:163 | none (best Task 1 0.091) |
| INF-154 | that **deferred floor** is published separately, the bar is applied to the headline without it, and the control's comparable number (control MAJOR findings without a concrete wrong outcome) is computed by the same rubric. | source.md:163 | none (best Task 4 0.316) |
| INF-155 | A run that ends early is counted at its terminal review. `U3` alone is the analogue of Arm B's hunk-scoped review 3 and is reported beside the headline. | source.md:163 | none (best Task 3 0.389) |
| INF-156 | (a) **Ledger plus 427 vs control**: headline mean at most 3 (half the control's 6.0), growth after two fix cycles at most 44.4%, effect larger than the larger within-arm spread, and every ledger replicate better than both control replicates on both. | source.md:166 | none (best Task 6 0.333) |
| INF-157 | (b) **The ledger's own effect vs Arm B** (the ledger carries 427's grading, so (a) credits both): headline mean below Arm B's 3.5 and growth at most 30.0%. | source.md:167 | none (best Task 6 0.211) |
| INF-158 | Pre-registered per replicate: B1 (blocking rows after review 1) and r1, r2 (new blocking rows per blocking fix in cycles 1 and 2). | source.md:168 | none (best Task 1 0.5) |
| INF-159 | Headline mean 4 or more, or not below Arm B's 3.5: the ledger adds nothing over 427 with flags on convergence. | source.md:186 | none (best Task 4 0.333) |
| INF-160 | The ledger sweep finds on average 2 or more CRITICAL+MAJOR rows more than the baseline sweeps: verify-only hid defects instead of preventing them. | source.md:187 | none (best Task 1 0.353) |
| INF-161 | Growth above 30.0% after reverted bytes are shown: the minor-row rule did not cut text. | source.md:188 | none (best Task 4 0.273) |
| INF-162 | `minor_touched` above 0 through answered claims with `--revert-unclaimed` on: the scope rule leaked mechanically. | source.md:189 | none (best Task 4 0.455) |
| INF-163 | A loop stalled by a script refusal with no recovery path in either replicate. | source.md:190 | none (best Task 1 0.375) |
| INF-164 | A replicate that fails V1-ledger or the wrong-outcome audit is not treatment (it is rerun), not a failure. Results inside both arms' spreads are "not significant" (D6). | source.md:191 | none (best Task 7 0.133) |
| INF-165 | `U3` below 3.5 in both replicates with growth at most 30%, the sweep no larger than the baseline sweeps, zero `minor_touched` through answers, and zero verdict computed by a model. | source.md:193 | none (best Task 1 0.211) |
| INF-166 | **Cost per loop (estimates; measure as M5).** | source.md:197 | none (best Task 1 0.2) |
| INF-167 | Mitigation: `scope=outside` rows and the sweep enter the headline; baseline sweeps measure the hidden share. | source.md:204 | none (best Task 4 0.417) |
| INF-168 | Measured by the wrong-outcome audit, not prevented. | source.md:205 | none (best None 0.0) |
| INF-169 | Unclaimed hunks and failed reverts never stall (they report or become `cannot-verify`), but one `cannot-verify` ends the loop as ESCALATE. | source.md:209 | containment Task 3 (0.643) |
| INF-170 | Every disagreement is recorded. | source.md:210 | none (best None 0.0) |
| INF-171 | \| Ledger written only by the script; hash refuses hand edits \| MECHANICAL \| detects, does not prevent, a determined editor \| | source.md:217 | none (best Task 1 0.333) |
| INF-172 | \| Blocking computed from grade, rule and wrong outcome; non-blocking rows deferred and unanswerable \| MECHANICAL \| the grade and the wrong-outcome text are still model judgement \| | source.md:218 | none (best Task 1 0.562) |
| INF-173 | \| Grade and anchor frozen \| MECHANICAL \| locks first-pass errors \| | source.md:219 | none (best Task 1 0.429) |
| INF-174 | \| Every plan row answered; evidence quote present in the snapshot \| MECHANICAL \| proves the text was opened, not that it was judged well ("yes, yes" answers) \| | source.md:220 | none (best Task 3 0.4) |
| INF-175 | \| New blocking rows only inside this round's hunks \| MECHANICAL \| interaction defects become non-blocking \| | source.md:221 | none (best Task 2 0.583) |
| INF-176 | \| Unclaimed edits reported; reverted with the flag \| MECHANICAL \| edits inside a blocking paragraph are admitted \| | source.md:222 | containment Task 2 (0.6) |
| INF-177 | \| Counter, cap, terminal phase, computed last line \| MECHANICAL \| a coordinator that ignores refusals and dispatches anyway \| | source.md:223 | none (best Task 2 0.385) |
| INF-178 | \| Verifier does not run a whole-document panel \| PROSE \| it may anyway; its out-of-hunk rows are then counted, not hidden \| | source.md:224 | none (best Task 2 0.3) |
| INF-179 | \| Sweep context does not open the ledger \| PROSE, partly checked \| detected only when the sweep report cites a row id \| | source.md:225 | none (best Task 1 0.538) |
| INF-180 | \| Reviewer, reviser and sweep are different sessions \| PROSE \| the script knows the subcommand, not the session \| | source.md:226 | none (best Task 1 0.3) |
| INF-181 | \| Reviser adds no mechanism inside a blocking fix \| PROSE \| the main remaining cause; bytes per claim are only measured \| | source.md:227 | none (best Task 2 0.462) |
| INF-182 | The cleanest single test: if `U3` (the loop's own count) is not below Arm B's 3.5 in both replicates, the ledger adds nothing to convergence beyond what 427 with flags already does, and only its mechanical stop and honest counting remain as reasons to keep it. | source.md:229 | none (best Task 4 0.226) |
| INF-183 | Decides 5 or 6 sessions and whether S1's dispatch list changes (UNVERIFIED; one smoke check settles it). | source.md:233 | none (best Task 9 0.467) |
| INF-184 | The default without the flag only reports. | source.md:234 | none (best Task 1 0.333) |
| INF-185 | This design applies it without, and publishes the floor beside it; this must be fixed before replicate 1. | source.md:235 | none (best Task 2 0.222) |
| INF-186 | Calibrate on the S1 history pairs. | source.md:237 | none (best Task 1 0.25) |
| INF-187 | Recommended: only on the user's word. | source.md:238 | none (best Task 4 0.5) |
| INF-188 | Can the duplicate ruling, the deferred-floor reading of the control reports and the wrong-outcome audit be staffed before replicate 1? Without them only raw bounds exist. | source.md:239 | none (best Task 7 0.188) |
| INF-189 | Confirm before any adopter work. | source.md:240 | none (best Task 1 0.25) |
| INF-190 | That changes what the arm tests and must be decided before it runs. | source.md:241 | none (best Task 9 0.429) |
