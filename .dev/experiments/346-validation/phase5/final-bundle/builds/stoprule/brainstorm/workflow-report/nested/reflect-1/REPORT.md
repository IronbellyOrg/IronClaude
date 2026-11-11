# Reflect report: pre-execution review of TASK-WF-spec-20261108-181616

```yaml
contract_version: 1.8.0
status: partial   # 1 citation dropped by evidence-validator (source.md:143 in C-018)
mode: pre
tier_reached: 2
confidence_calibrated: 0.72
citations_total: 153
citations_revalidated: 89   # unique targets; the validator re-Read every citation, not only the sample
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

Legend: `plan:N` = `.dev/tasks/to-do/TASK-WF-spec-20261108-181616/TASK-WF-spec-20261108-181616.md` line N; `source.md:N` = `.dev/tasks/to-do/TASK-WF-spec-20261108-181616/source.md` line N; other paths are repo-relative.

## Verdict

The plan covers source.md sections 3 and 4 (34 inferred requirements, 31 matched mechanically, the 3 lexical misses confirmed covered by all reviewers). One blocking defect: the Task 7 replay test cannot pass as written (C-003). 21 minor findings and 3 not-a-defect items follow. Advisory only: this report never edits the plan.

- Tier 2 forced by `coverage_degraded: parsed-sparse` (0 labelled requirement IDs, 34 inferred rows).
- Reviewers: reflect-reviewer x3 (sonnet analyzer, haiku qa, opus refactorer); calibrator opus (`calibrator_diversity: degraded`); merge: sc:adversarial, convergence 0.97, 0 HIGH unaddressed invariants.
- Calibrated confidence: mean of reviewer cards 0.77, 0.63, 0.77 = 0.72 (Tier 1 card 0.63).

## Blocking finding

### C-003: Task 7 replay test cannot pass as written
- **Location:** plan:96, plan:99
- **Claim:** Without `--re-review`, `begin` sets N = 1 and the ratchet is off (plan:57, source.md:62, source.md:64), so the per-claim assertion that claims on text unchanged since v2 come out `late-found` fails; with `--re-review`, `begin` exits 5 because the control-r1 round-2 report carries no sentinel and Task 7's fixture list (plan:96) names no prior report. source.md:193 predicts 3 of 8 claims on unchanged text.
- **Recommendation:** Add to Task 7 a test-scaffold review-2 report with a valid sentinel built in tmp_path (declared as scaffolding, not a substitute for the control files); seal twice or add `checked` lines for the real changed hunks; fix the quote-line rule (the line the report cites, recorded per claim) and do not derive the expected split from the code under test.

## Declared deviations (classified)

### Deviation D-001: `## Unattended mode` removed from the variant
- **Location:** plan:21, plan:123
- **Mapped tasklist item:** Task 9
- **Spec section:** source.md section 3.1 ("Copy of `spec-panel.md`")
- **Classification:** authorized
- **Classification rationale:** owner ruling recorded in the plan Constraints (plan:21); keeping the section would break `tests/skills/test_worker_contract.py:831-839`.
- **Default remediation:** none; see C-004 for the Usage line it leaves behind.

### Deviation D-002: edit of tests/recommend/test_routing_refresh.py
- **Location:** plan:135, plan:141
- **Mapped tasklist item:** Task 10
- **Spec section:** source.md section 3.4 ("Run, do not edit", source.md:129)
- **Classification:** necessary
- **Classification rationale:** `tests/recommend/test_routing_refresh.py:648` asserts `shipped - _POST_REFRESH_ADDITIONS == active`, which any new command file breaks; source.md left the count effect UNVERIFIED.
- **Default remediation:** none; see C-020 for the stale comment.

### Deviation D-003: section-5 brief templates in Task 14
- **Location:** plan:19, plan:184
- **Classification:** drift (minor; C-018)
- **Default remediation:** cite an owner decision for `offline-demotion-audit.md` and `replay-gate.md` or drop them.

## Minor findings (advisory)

| id | claim | evidence | recommendation |
|---|---|---|---|
| C-002 | Task 3's begin must exit 5 on prior-verdict mismatch and seal's prior link needs 'confirmed and open in review N-1', but final-status derivation lands in Task 4 and compute_verdict in Task 5. | plan:57, plan:60, plan:68, plan:77, source.md:62, source.md:64 | Move status/verdict computation into Task 3 (Tasks 4-5 extend it), or move the prior-verdict-mismatch part of begin and its test to Task 5. |
| C-001 | Task 5's finalize label-count line uses 'the same function as Task 6's count', but Task 6 depends on Task 5 (confirms T1 A1). | plan:77, plan:80, plan:83, plan:87 | Define the label-count function (including form-only dropped claims) in Task 5 or Task 3; Task 6 only wraps it as the count subcommand. |
| C-004 | spec-panel.md Usage line 23 advertises --unattended; Task 9 keeps it, so the variant advertises a flag it refuses; Task 10 replaced-block list and Task 9 acceptance do not cover it. Task 10's equality test treats that line as inherited, so a fix would fail it, locking the Usage line in. The E-SKILL-MISSING rule Task 9 adds is, as its own line, not in Task 10's exhaustive replaced-block list, so the equality test against spec-panel.md fails unless the rule is folded into the activation line. | src/superclaude/commands/spec-panel.md:23, src/superclaude/commands/spec-panel.md:451-462, src/superclaude/commands/spec-panel.md:456, src/superclaude/commands/spec-panel.md:459, plan:21, plan:123, plan:135, source.md:115, source.md:256 | Drop the --unattended Usage line (or token) in Task 9, add it to Task 10's replaced blocks, add grep -c -- '--unattended' = 0 to Task 9 acceptance. Also add the E-SKILL-MISSING rule line to Task 10's replaced-block list, or fold the rule into the activation line. |
| C-005 | Spec test 'two claims on one prior counted once' is in no task acceptance list and the rule is stated nowhere in Tasks 3-5. | source.md:128, plan:60, plan:71, plan:80 | Add the case and the rule to Task 3 or Task 5. |
| C-006 | Task 12 stages before Tasks 13-14 create INSTALL.md and briefs; nothing stages them and Task 13's git diff --cached check only sees Task 12's staging. | plan:27, plan:161, plan:172, plan:182 | Stage .dev/brainstorms/346-stoprule/ and .dev/tasks at the end of Tasks 13 and 14. |
| C-010 | Writers of final/verdict ledger lines, the source of sentinel brief=/grader_model=/ratchet=, and parent= (escalation g) are unspecified. | source.md:34, source.md:69-70, source.md:73, plan:77 | Name the writer subcommands and the source of brief= in Task 5; define parent= or drop it. |
| C-011 | apply-audit defines real:true only for claims; a real:true on a seeded unclaimed hunk has no defined outcome. | plan:68, source.md:68 | Define the outcome (e.g. FAIL) with a test in Task 4. |
| C-012 | Task 7's hand-transcribed quotes decide anchored vs late-found; the quote-selection rule is unstated. | plan:96, source.md:93, source.md:193 | Quote the line the report cites and record the choice per claim. |
| C-013 | The stdlib import grep is only in Task 3; Tasks 4-6 extend the script unchecked. test_worker_contract.py scans new primitives for git/gh write verbs. stoprule.py and canaries.json not in the static src/superclaude scan; default --rubric path must be script-relative. | plan:26, plan:61, plan:20, tests/skills/test_worker_contract.py:1940-1951, plan:25, plan:57, plan:135 | Repeat the import grep in Task 6; forbid git/gh write-verb text in new files in Tasks 3 and 8. Scan stoprule.py and canaries.json; build the default --rubric path from Path(__file__); test from a tmp copy. |
| C-008 | Measurement copy not produced by any task (not a plan defect: section 3 omits it); INSTALL.md's 'differ only in lines from master' is unverified. Control r1 files exist in the sibling checkout. | source.md:163, plan:172, plan:96 | Task 13 records the repo copy's line count and diff against the 472-line base instead of asserting; name exact source paths in Task 7. |
| C-009 | Task 3 keeps a withdrawn claim's id and claimed label but not its prior link, which Task 6 needs to exclude withdrawn carried priors from the new-finding count; the fixture does not test this. | plan:57, plan:87, plan:90, .dev/tasks/to-do/TASK-WF-spec-20261108-181616/source.md:173 | Require the first-pass form line to keep prior with id and claimed; add a test with a withdrawn new MAJOR (counted) and a withdrawn carried MAJOR (excluded). |
| C-014 | FR-8/FR-9 rewrite, bullet 7 suffix and no-unattended sentence have no positive check; equality test excludes them. | source.md:105, src/superclaude/commands/spec-panel.md:328, src/superclaude/commands/spec-panel.md:329, plan:126, plan:135 | Assert the new wording in test_spec_panel_stoprule.py. |
| C-015 | test_review_severity_rule.py scans only git-tracked files; Tasks 10 and 12 run it before staging. | tests/skills/test_review_severity_rule.py:35, tests/skills/test_review_severity_rule.py:38, tests/skills/test_review_severity_rule.py:448, plan:140, plan:161, plan:165 | Stage first, then run pytest in Task 12. |
| C-016 | Task 12 omits tests/agents, tests/docs, tests/cli which scan new files. | tests/agents/test_tavily_tool_parity.py:31, tests/agents/test_tavily_tool_parity.py:34, tests/docs/test_retired_docs_absent.py:40, plan:165 | Add them or run the whole suite. |
| C-018 | offline-demotion-audit.md and replay-gate.md are section 5 procedures outside the plan's stated scope. | plan:19, plan:184, source.md:170, source.md:180 | Cite an owner decision or drop them. |
| C-020 | Task 10 allows only the _POST_REFRESH_ADDITIONS line to change, leaving its comment stale. | tests/recommend/test_routing_refresh.py:29, tests/recommend/test_routing_refresh.py:33, tests/recommend/test_routing_refresh.py:648, plan:141 | Allow one comment line naming #346. |
| C-021 | Integration Patterns examples still call plain /sc:spec-panel. | src/superclaude/commands/spec-panel.md:430, src/superclaude/commands/spec-panel.md:436, source.md:104, plan:123 | Decide whether the Integration Patterns examples should call the variant command; as written they follow source.md:104 literally. |
| INV-005 | `check` recomputes every status and the verdict, and `begin` recomputes the prior report's verdict. Recomputing `late-found` needs the baseline, the spec and the N-1 report; recomputing `minor-form` needs the spec and the evidence files under `--root`. The plan gives `check` no argument list, and the coordinator template runs `check` on the report only. `check` must therefore either take unstated inputs or trust recorded `final` lines, which is weaker than "recompute". | plan:77, source.md:74, plan:57, plan:184 | Give check and begin the inputs recomputation needs, or have the ledger store what they need to recompute statuses from the report alone. |
| INV-006 | The review number has two unchecked sources. Bullets 1 and 4 keep the reviewer-written header rule `review: N of 3` verbatim, while the script takes N from the sentinel `review=N/3`. `check` compares the sentinel, the computed block and the last line, not the header. If the header and the sentinel disagree, nothing detects it. | spec-panel.md:258, spec-panel.md:261, plan:123, plan:57, plan:77 | Make one source authoritative for N, or have check compare the header with the sentinel. |
| INV-007 | `m1_open_confirmed` = sentinel `confirmed` + frozen `unresolved-prior`. The never-batched rule names only the frozen prior blockers themselves, so a single new claim with a valid `prior` link is batched, can be graded `confirmed`, and counts again next to its still-open frozen prior: two counts for one defect with only one claim. M1 has a "<= 3" bar and F1a stops the run at M1 >= 4. | plan:87, plan:68, source.md:186, source.md:201 | Count a defect once in m1_open_confirmed when a single claim is linked to an open frozen prior, and state the rule alongside C-005. |
| INV-008 | `begin` sets N = 1 whenever `--re-review` is absent. A dispatch that omits the flags restarts the count, so exit 4 can never fire. The cap therefore still depends on the coordinator passing flags. Inherited from the spec; the plan's install note limits use to Arm B. | plan:57, source.md:62, source.md:150, plan:184, plan:172 | State that the review cap depends on the coordinator passing --re-review, or make begin detect an existing prior report instead of resetting N. |
| INV-009 | An `incomplete`-only FAIL gives the NONE brief and no spec edit, so the next review has an empty changed-line set. A prior link is valid only for a claim confirmed in N-1, so earlier `unconfirmed` claims cannot anchor. Every re-raised defect becomes `late-found` and never loops; only the PASS-time audit can reinstate it. One grader outage therefore turns real defects into items that never loop. Inherited from the spec; no task tests the path. | plan:77, plan:57, plan:68, source.md:71, source.md:243 | Define how claims re-raised after an incomplete-only FAIL anchor, and add a test for the grader-outage path. |

## Not defects

- C-007: Task 13 must list Task 14's templates and Task 14's acceptance requires INSTALL.md to list eleven files, but Task 14 has no instruction to edit INSTALL.md.
- C-017, C-019: settled not-a-defect in the debate (rubric hash literal lives in the test; source.md 3.3 lists exact agent keys).

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Frontmatter `name: spec-panel-stoprule`; `description` ends "(experimental variant: computed review-loop verdict)" | source.md:104 | containment Task 9 (ratio 0.9) |
| INF-002 | Under the title add the activation line `> Skill sc:spec-panel-stoprule-protocol`. | source.md:104 | containment Task 9 (ratio 1.0) |
| INF-003 | FR-10 stays (it feeds the table `sc:adversarial` consumes). | source.md:105 | none  (ratio 0.571) |
| INF-004 | bullets 1 and 7 keep the 427 text (7 adds "and may not change the rubric or its hash"); bullets 2-6 are replaced; bullet 8 is new. | source.md:106 | containment Task 9 (ratio 0.692) |
| INF-005 | stop with `E-SKILL-MISSING`; never run the plain 427 loop under this name. | source.md:115 | containment Task 9 (ratio 0.667) |
| INF-006 | a failure table (grader reply invalid twice or Agent tool unavailable -> claims `unconfirmed`, verdict FAIL `incomplete`, no reviser edits; script exit codes and messages), and a "do not" list (no verdict line, no ledger edit after `seal`, no edit of `refs/rubric.md`). | source.md:118 | containment Task 8 (ratio 0.931) |
| INF-007 | `refs/rubric.md`: the literal text of section 2.3. | source.md:119 | containment Task 1 (ratio 0.833) |
| INF-008 | `refs/canaries.json`: 4 synthetic blocking and 4 synthetic minor claims (`{quote, span, outcome, evidence, answer}`), unrelated to any real spec; rotated by seed. | source.md:120 | containment Task 1 (ratio 0.75) |
| INF-009 | Takes `--rubric` and `--cap` so other loops can reuse it. | source.md:121 | none  (ratio 0.25) |
| INF-010 | Known limit to put in a code comment: "markdown tables and wrapped cells are not normalised; upgrade if `quote-not-found` dominates the audit". | source.md:121 | containment Task 3 (ratio 0.857) |
| INF-011 | Frontmatter `name: finding-grader`, `tools: Read`, `model: sonnet`, `maxTurns: 10`, `permissionMode: plan` (same pattern as `confidence-calibrator`). | source.md:124 | containment Task 2 (ratio 0.929) |
| INF-012 | the variant equals `spec-panel.md` outside the replaced blocks (computed diff, so a later spec-panel change fails the test instead of drifting); `install_skills._has_corresponding_command("sc-spec-panel-stoprule-protocol")` is False. | source.md:127 | containment Task 10 (ratio 0.833) |
| INF-013 | a replay fixture built from control r1's spec v2/v3 and its 8 review-3 claims. | source.md:128 | containment Task 7 (ratio 0.8) |
| INF-014 | `begin` exit 4 on a prior review-3 FAIL; exit 5 on rubric drift, prior-verdict mismatch and baseline hash mismatch; ledger edited after `seal` -> `check` exit 6; `grade-raw` mismatch -> exit 6; `finalize` refuses a hand-typed `verdict:` | source.md:128 | containment Task 5 (ratio 0.762) |
| INF-015 | Run, do not edit: `tests/skills/test_review_severity_rule.py`, `tests/unit/test_cli_install.py`, `tests/recommend/test_routing_refresh.py` | source.md:129 | containment Task 10 (ratio 1.0) |
| INF-016 | New `docs/designs/spec-panel-stoprule.md` (this spec trimmed to the final decision); one sentence in `docs/designs/spec-panel-review-loop.md` section 11 pointing to it. | source.md:132 | containment Task 11 (ratio 0.8) |
| INF-017 | No routing-guide row, `/sc:help` entry or plugin mirror while the variant is experimental. | source.md:132 | containment Constraints (ratio 0.8) |
| INF-018 | Then `make sync-dev`, `make verify-sync`; stage `src/`, `tests/`, `docs/`, `.dev/tasks`, never `.claude/`. | source.md:132 | containment Task 12 (ratio 1.0) |
| INF-019 | `src/superclaude/commands/spec-panel.md`, `~/.claude/commands/sc/spec-panel.md`, the rf-qa agents, `confidence-calibrator`, `evidence-validator`, `sc-implement-protocol`, `WORKER-CONTRACT.md`. | source.md:135 | containment Constraints (ratio 1.0) |
| INF-020 | perl -pe 's#(/?sc:spec-panel)(?![-\w])#$1-stoprule#g' brief.md > brief.stoprule.md | source.md:148 | containment Task 13 (ratio 1.0) |
| INF-021 | Apply it to the **Arm B** briefs (review 2 and 3 pass `--re-review <prior> --baseline <saved copy>`) | source.md:150 | containment Task 14 (ratio 0.9) |
| INF-022 | The measurement copy of the command is built from the exact Arm B base file (472 lines, sha256[:12] `c8d80346a96c`) plus the section 3.1 edits, so the only difference from Arm B is the stoprule change. | source.md:163 | containment Task 13 (ratio 0.81) |
| INF-023 | **Rollback:** delete the three installed paths. | source.md:163 | containment Task 13 (ratio 0.6) |
| INF-024 | Never pass `--force` on the experiment machine: it overwrites every installed command, `spec-panel.md` included. | source.md:165 | containment Task 13 (ratio 0.8) |
| INF-025 | Writes a `begin` marker with a random 16-hex nonce, opens the ledger block in the stub report, prints the rubric and the list of changed hunks (difflib, whitespace-only changes ignored). | source.md:62 | containment Task 3 (ratio 0.95) |
| INF-026 | every changed hunk needs a claim or a `checked` line. | source.md:64 | containment Task 3 (ratio 0.667) |
| INF-027 | Every other form-valid claim, late-found ones included, goes into batches of at most 6 claims plus 2 canaries (one known-blocking, one known-minor, from `refs/canaries.json`), shuffled with seed `sha256(nonce, review, ledger)` and renamed `C1..Cn`. | source.md:65 | containment Task 4 (ratio 0.96) |
| INF-028 | A wrong canary answer rejects the batch (one rerun); a second failure leaves those claims `unconfirmed`. | source.md:67 | containment Task 4 (ratio 1.0) |
| INF-029 | Any `real:true` reinstates the claim (`confirmed-audit`) and the verdict becomes FAIL; the sentinel records `pre_audit=PASS`. | source.md:68 | containment Task 4 (ratio 0.667) |
| INF-030 | Refuses if the report already holds a line starting `verdict:`. | source.md:70 | containment Task 5 (ratio 1.0) |
| INF-031 | Re-extracts the ledger, verifies the seal and every `grade-raw` hash, recomputes every status and the verdict, compares sentinel, computed block and last line. | source.md:74 | containment Task 5 (ratio 0.933) |
| INF-032 | `stoprule.py check-disposition` lists any id the reviser applied outside D1..Dk (reported, never blocking). | source.md:75 | containment Task 14 (ratio 0.818) |
| INF-033 | `stoprule.py verify-transcript --report R --transcript <worker session .jsonl>` checks that each `grade-raw` text appears verbatim as an Agent tool result in the worker's transcript and prints `grader-integrity: verified/mismatch/unverified`. | source.md:76 | containment Task 6 (ratio 0.905) |
| INF-034 | The owner independently labels 5 sampled items (`stoprule.py audit-sample`, k = 5) and auditor-owner agreement is reported as its own number. | source.md:180 | none  (ratio 0.333) |

Mechanical containment left INF-003, INF-009 and INF-034 unmatched; all three reviewers confirmed them covered by Task 9 ("FR-10 stays"), Task 3 (`--rubric`, `--cap`) and Task 6 (`--owner-k 5`). coverage_pct (parsed): null; coverage_pct_union: 0.9118 mechanical, 1.0 after reviewer confirmation.

## Dropped citations

- `source.md:143` (row C-018): the line is the section 4 heading and does not support the claim; the row stands on source.md:170, source.md:180, plan:19 and plan:184 (evidence-validator, 2026-11-08). Forces `status: partial`.

## Grounding Gaps

None.

## Recommendations

- Fix C-003 in plan Task 7 before running `/sc:implement`; the 21 minor findings are optional improvements (C-001/C-002 ordering, C-004 Usage line, C-005 counted-once case and C-009 withdrawn-prior link are the most useful).
