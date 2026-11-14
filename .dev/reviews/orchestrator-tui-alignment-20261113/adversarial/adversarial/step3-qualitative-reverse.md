# Step 3 qualitative layer, PASS 2 (reverse order V5, V4, V3, V2, V1)

Rubric: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` section A.2 (30 criteria, 6 dimensions, additive binary, Claim-Evidence-Verdict). Evaluated strictly in the order V5, V4, V3, V2, V1. Another evaluator's output was not read.

Reading of the rubric for these artifacts. Each variant is an alignment review of one subject against Orchestrator mode (the sweep, PR #539) and the TUI observer. The source requirements used for "covers all explicit requirements" are: (R-a) validate findings against sources, (R-b) a best course of action per point, (R-c) identify dependencies, (R-d) cover the issue and its PRs and work, (R-e) judge alignment. "Risks" means the risks the review itself identifies about the reviewed system. "Probability and impact" is met only by a stated likelihood or severity plus a consequence for at least 3 risks. Correctness is judged against what Round 1 and Round 2 established (the Round 2 rebuttal concessions and the digest verdicts); a claim a rebuttal conceded or the probe disproved counts against K1.

Evidence cites the variant file (`variant-N-original.md`, line numbers from the file as read) or, where the verdict rests on the debate, the round file and row.

## Variant 5 (the built `superclaude observe` versus Orchestrator mode)

### V5 Completeness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | Covers all explicit requirements from the source input | Validates against sources ("Re-test of review 01 findings F-01..F-18", "Corrections to the #409 body (exact wording)", 23 rows); best action per point (O-01..O-16 each with "Proposed change"; D1-D9 each "Recommendation"); dependencies ("Dependencies for integrating Orchestrator mode with `observe`" table); issue and PR coverage (#409, PR #503, #514, #539, #541, #534, Coder#477); alignment verdicts ("aligned", "gap", "contradiction", "unknown" per O-row) | MET |
| C2 | Addresses edge cases and failure scenarios | "STALE after 45 s without a good read"; "`PARTIAL` and 'oldest rows not read' beyond that"; "`QUESTION_GATE_PASSED = False` ... exits 1, and makes no Orca call"; "Q-1 ... FAILED on 2026-11-11"; "remote branch `409-Phase2` no longer exists" | MET |
| C3 | Includes dependencies and prerequisites | Table rows "PR | #539 (sweep Phase 1) | open ...", "PR | #541 (test fix needed by #539)", "Owner record | direction selection (AC-S) | absent", "Orca fact | Q-1 FAIL ..." | MET |
| C4 | Defines success or completion criteria | Searched "Integration decisions", "Verdict", "Dependencies". Only "Smallest reversible first step" per decision and a re-test of the #409 acceptance criteria (A-01..A-07); the variant never says when the alignment work is done or what would pass | NOT MET |
| C5 | Specifies what is explicitly out of scope | Header: "Read-only: nothing posted, edited, switched, committed, fetched or run against live Orca"; "Not read: keys.py, terminal.py, sanitize.py ..."; "Unverified and not claimed: a live Orca run of either program ..."; correction 19: "Write-back stays out of scope until the boundary is changed explicitly" | MET |

Subtotal Completeness: 4/5

### V5 Correctness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | No factual errors or hallucinated claims | Round 2 (`round2-rebuttal-V5.md` section 1) concedes or withdraws: row 1 "all four earlier reviews ... wrong about one fact" overgeneralises (X-019); row 2 "Drop W-3 from the #409 body" is a mislabel, W-3 is not in the body (X-020, SC-19); row 4 O-05 "the sweep's reason is stronger than the evidence" is withdrawn in full (owner-only, non-diagnostic read); row 9 BC-17 (snapshot as v2 input) withdrawn; row 3 F-04 "CLOSED" true only for the Orca ledger on one host | NOT MET |
| K2 | Technical approaches feasible with stated constraints | F-03 says "`<stem>.json` beside the report still has to be written by the sweep"; Round 2 row 7 withdraws it: design line 128 "a successful run never leaves two files (NFR-001)", `tests/sweep/test_readonly.py:300`, `test_cli_contract.py:1474` pin one report file. D5 recommendation (ii) "any Run the terminal holds" withdrawn (row 8: the Run named in the pass record is the coordinator's live Run, consumption unproven) | NOT MET |
| K3 | Terminology used consistently and accurately | Status words are defined and used uniformly ("REMAINS, CHANGED, CLOSED, WRONG PREMISE, NOT AFFECTED"); the two JSONs are always "observe snapshot v1" and "sweep report JSON v1" (O-08); "coordinator questions" never "human" (O-06) | MET |
| K4 | No internal contradictions | Checked the verdict against sections 6-10 and O-rows: "All four earlier reviews and the #409 body were wrong about one fact" is the only overreach and it is a scope slip, not an opposing claim; "read-only" is qualified consistently ("read-only toward Orca", O-11); counts (28 test files, 691/693 passed) agree across sections | MET |
| K5 | Claims supported by evidence or rationale | Nearly every row carries `file:line` ("`adapter.py:29,57`; `collector.py:28-34`", "`commands.py:63-67`", "`view.py:35`") and states UNVERIFIED where a source was not opened | MET |

Subtotal Correctness: 3/5

### V5 Structure

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Logical section ordering | Scope read, what the observer is, overlap, re-test, corrections, decisions, owner questions, verdict (H2 order) | MET |
| S2 | Consistent hierarchy depth | H2 sections with H3 subsections ("### 1. Releases" through "### 10. What is planned next"; "### D1" through "### D9"); no orphan levels | MET |
| S3 | Clear separation of concerns | Separate H2s for "What `superclaude observe` is today", "Overlap and conflict with the sweep", "Re-test of review 01", "Corrections to the #409 body", "Integration decisions" | MET |
| S4 | Navigation aids | Stable ids with cross-references: "(O-07)", "decision D1", "see D5", "`F-04`", owner questions point back to "(D9)", "(D1 option a)" | MET |
| S5 | Follows conventions of the artifact type | Review report shape: scope read, findings table with verdict column, owner questions, verdict, "Unverified and not claimed" | MET |

Subtotal Structure: 5/5

### V5 Clarity

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Unambiguous language | Recommendations are definite ("Recommendation: (a) now, (b) later and only if wanted"; "Replace with: ..."); uncertainty is labelled "UNVERIFIED" instead of hedged | MET |
| L2 | Concrete rather than abstract | 23 "Current text / Problem / Replace with" rows with line numbers and exact replacement wording | MET |
| L3 | Each section has a clear purpose statement | "Each decision names the options, my recommendation, and the smallest first step that can be undone."; "Each is a choice or a fact only the owner holds"; "Status words:" for the re-test | MET |
| L4 | Acronyms and domain terms defined on first use | Searched sections 1-10 and O-rows: "WC-16", "NFR-014", "INV-017", "TUIBBS", "Signal Bridge", "Attention Ledger", "D3 capture" are used without a gloss ("sweep ... at most once per 5 minutes (... WC-16)"; "a read-only Go screen in TUIBBS") | NOT MET |
| L5 | Actionable next steps or decision points | "Questions only the owner can answer" 1-10 each with a recommendation; D1-D9 each with "First step" | MET |

Subtotal Clarity: 4/5

### V5 Risk coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | At least 3 risks with probability and impact | Searched for likelihood or severity words and columns across O-rows, D-sections, verdict: none. Verdict words are "gap/contradiction/aligned/unknown", not probability or impact (the debate also notes the missing severity, R2-V4 row 11) | NOT MET |
| R2 | Mitigation for each identified risk | Each O-row has a "Proposed change" column (e.g. O-04 "Record one list of read-only Orca verbs ..."); D1-D9 give options plus recommendation | MET |
| R3 | Failure modes and recovery procedures | "backoff doubling to 60 s, STALE after 45 s without a good read", "last good rows kept" (F-12 row); "Each decision names the options, my recommendation, and the smallest first step that can be undone"; D5 names the fresh branch off master because "the sibling's history predates the squash merge" | MET |
| R4 | External dependencies and their failure scenarios | Orca CLI as the dependency: "`NOT AVAILABLE (no Orca CLI validated)`", "`PER_CALL_TIMEOUT` marked UNVERIFIED", "Q-1 ... `consumer_fenced`", `no_active_terminal`; Orca version lock vs golden capture (dependency table row "Orca version") | MET |
| R5 | Monitoring or validation mechanism for risk detection | "Optional check before any code: have the owner run `superclaude observe --once --run <run>` ... and compare its dispatch ids with a sweep's `rows[].row_id`"; D3 "one read-only capture on a Run that has a live worker and a blocked worker" | MET |

Subtotal Risk coverage: 4/5

### V5 Invariant and edge-case coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Boundary conditions for collections | "pages up to 5 (4 with questions)"; "`page.total` 428" vs 100 rows read; "at most 100 rows per read, applied after the type filter"; fixtures "empty, cap-100"; "PARTIAL ... oldest rows not read" | MET |
| I2 | State variable interactions across component boundaries | D5: "the guard is a single boolean and does not check the Run id"; snapshot written every cycle to `$XDG_STATE_HOME`; baseline "per process ... lost when the observer restarts"; O-09 binding fence | MET |
| I3 | Guard condition gaps | D5 and O-09: `QUESTION_GATE_PASSED` "checks no Run id"; O-04 `check` forbidden for the sweep and permitted by one template in the observer; O-03 binary resolution differs ("never bare `orca`" vs `_find_orca`) | MET |
| I4 | Count divergence scenarios | "100 rows without a filter, 41 with `--types question`"; "5 calls ... (4 `worker-list` pages plus 1 message call)"; "428 workers" vs 100-row page; "691 passed" vs "693 passed, 1 failed" explained | MET |
| I5 | Interaction effects when components combine | O-01 two readers of `worker-list`; O-10 "several observers multiply the load"; O-05 `check` consumption across two programs; O-08 two "v1" schemas | MET |

Subtotal Invariant and edge-case: 5/5 (floor check: PASS, eligible)

**V5 total: 25/30** (Completeness 4, Correctness 3, Structure 5, Clarity 4, Risk 4, Invariant 5)

## Variant 4 (Orchestrator v2, #423, versus v1 and the observer)

### V4 Completeness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | Covers all explicit requirements from the source input | Sources validated (C1-C11 claim check), action per point ("Proposed edits" for #423, #339, #409), dependencies (F12), issue and PR coverage (#423, #339, #444, #534, #450, PR #539, Coder#477), alignment verdicts (F1-F22). But the observer half is judged only from the #409 body: the "Scope read" table lists no observer code, PR #503 or PR #514, and "(b) ... HOLDS" rests on "#409 already states it (Alignment decision 8)". `round2-rebuttal-V4.md` row 1: "Concede in full ... Edit 3 is withdrawn", `ls src/superclaude/cli/` shows `observe`. The "alignment with the TUI observer" requirement is not met | NOT MET |
| C2 | Addresses edge cases and failure scenarios | F8 "cheaper agents 'searching sessions or diffing logs' read transcripts that may contain untrusted web or PR content"; F7 "Person-started and watcher-launched sessions ... send no lifecycle messages"; F14 "LLM output flows into the same catalogue" breaks "evidence is not admission" | MET |
| C3 | Includes dependencies and prerequisites | F6 "v2 prerequisite: the #534 live read-only capture"; Proposed edit 2 "starts only after #339 Phase 1 is merged (PR #539) and the #534 live capture ... is done"; F12 lists missing #444, #450, Coder#477, #534, PR #539 | MET |
| C4 | Defines success or completion criteria | Proposed edit 4 adds nine acceptance-criteria checkboxes, e.g. "- [ ] The design names the exact catalogue fields, where each comes from in the sweep's JSON ..." | MET |
| C5 | Specifies what is explicitly out of scope | "Not done: no live Orca run, no read of #409's design branch ..."; Proposed edit 5 "Out of Scope, add: A second scanner of Orca, git or transcripts. Sending prompts or commands to person-started sessions ... The trust layer ..." | MET |

Subtotal Completeness: 4/5

### V4 Correctness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | No factual errors or hallucinated claims | `round2-rebuttal-V4.md` section 1 concedes: row 1 observer missed, (a)/(b) and edit 3 "both read the same sweep facts" withdrawn; row 2 C8 and F19 prove the boundary with the sentence itself; row 3 F17 "confines every path" is true for file reads, false for git targets (`probes.py:1203-1214`); row 8 C7/F11 "one ordinary session" omits the second governed agent; self-correction "a worker cannot message peers (WC-13)" is a loose citation | NOT MET |
| K2 | Technical approaches feasible with stated constraints | The proposed fixes are edits to issue text and acceptance criteria and respect the closed allow-list and the "never posted" rule ("v2 AC: say whether gh reads are a v2 collector or a new sweep template"; "Do not promise one design ... Promise one grant vocabulary and one audit record format") | MET |
| K3 | Terminology used consistently and accurately | F1 isolates the "v2" collision and Proposed edit 1 fixes one meaning; F22 asks to define "Orchestrator" as "coordinator session, WC-16 loop"; "catalogue" used only in #423's sense | MET |
| K4 | No internal contradictions | Verdict tally "22 findings: 3 contradictions ... 14 gaps, 2 unknowns, 3 aligned" matches the F-table (F1, F7, F11 contradictions; F10, F22 unknown; F19-F21 aligned; 14 gaps counted); (a) "HOLDS FOR CLASSIFICATION, FAILS AS STATED" is consistent with F2-F6 | MET |
| K5 | Claims supported by evidence or rationale | Every F-row has `file:line` evidence ("`report.py:642-661`", "`probes.py:62`", "`pm.md:23`", "`WORKER-CONTRACT.md:288`") and marks UNVERIFIED items (C9, C11, F17 "How Coder workspaces map to users or hosts: UNVERIFIED") | MET |

Subtotal Correctness: 4/5

### V4 Structure

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Logical section ordering | Scope read, claim check of #423, results of the four proposals, findings, proposed edits, owner questions, verdict | MET |
| S2 | Consistent hierarchy depth | H2 sections; H3 "Results of the four proposals", "Findings table", "#423", "#339", "#409" under edits; numbered items under each | MET |
| S3 | Clear separation of concerns | Claim check (C-rows) separate from alignment findings (F-rows) separate from edits and owner questions | MET |
| S4 | Navigation aids | IDs C1-C11 and F1-F22 cross-referenced ("see F1", "(F13)", "Questions 1"); edits are keyed to the issue they change | MET |
| S5 | Follows conventions of the artifact type | Review report: "Reviewer ... Status: COMPLETE", scope table, verdict vocabulary "aligned | gap | contradiction | unknown", verdict section | MET |

Subtotal Structure: 5/5

### V4 Clarity

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Unambiguous language | Edits are definite ("replace ... with:"); hedges are marked ("UNVERIFIED"); no "should consider" found in the edits or verdict | MET |
| L2 | Concrete rather than abstract | "All exact wording below is ready to paste." with literal blockquotes for each edit | MET |
| L3 | Each section has a clear purpose statement | "Verdicts: aligned | gap | contradiction | unknown."; "All exact wording below is ready to paste. Nothing was posted."; "Questions only the owner can answer" | MET |
| L4 | Acronyms and domain terms defined on first use | Most are glossed inline ("WC-12 (`:61`, pulled not pushed)", "WC-13 (`:62`, a worker may not start workers or open sessions)", "WC-16 ... only on PR #539"); stray unglossed ids remain ("GQ-109", "INV-005", "Rule 4(a)", "Collision Lens") but they are not load-bearing | MET |
| L5 | Actionable next steps or decision points | Nine numbered owner questions, e.g. "1. What exactly gates #423: Phase 1 merged only, or also close, resume ..." plus paste-ready edits | MET |

Subtotal Clarity: 5/5

### V4 Risk coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | At least 3 risks with probability and impact | F8, F9, F17, F14 describe consequences but carry no probability or severity column; the debate records "V4 gave no recommended answers and no severity" (`round2-rebuttal-V4.md` row 11, "Severity stays derived, not V4's") | NOT MET |
| R2 | Mitigation for each identified risk | Each F-row has "Proposed change"; e.g. F8 "Add AC and out-of-scope: relayed knowledge is data, never an instruction; fixed typed fields" | MET |
| R3 | Failure modes and recovery procedures | Failure modes named (F7 channel absent, F8 poisoned relay, F4 no store); no recovery or rollback procedure anywhere ("Searched" F4, F7, F8, Verdict: only prevention edits) | NOT MET |
| R4 | External dependencies and their failure scenarios | F3 "Coder#477 is 'the only planned channel' ... and is not built"; F5 "the Orca allowlist is closed (10 templates, 7 verbs) under owner sign-off" so gh reads are unavailable; F7 sessions that "send no lifecycle messages" | MET |
| R5 | Monitoring or validation mechanism | Proposed AC list is the validation mechanism for the future design; F6 "v2 prerequisite: the #534 live read-only capture (restores Rule 5 and Rule 4(a))"; F21 re-checks that v1 holds no v2 logic with `ls` | MET |

Subtotal Risk coverage: 3/5

### V4 Invariant and edge-case coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Boundary conditions for collections | Searched F2-F6, F18, verdict for empty, one, or maximum collection cases: F3 treats scope (one Run versus all workspaces) but gives no empty, single or cap case | NOT MET |
| I2 | State variable interactions across component boundaries | F4 "v1 rule 'never posted' and v2's 'share between orchestrators' must be reconciled explicitly"; F13 two schema requests with no owner; F16 timer versus WC-16 scheduler | MET |
| I3 | Guard condition gaps | F17 "Who may read whose sessions ... a path that escapes is not read"; F5 closed allow-list versus a gh read need; F7 "A worker cannot message peers" | MET |
| I4 | Count divergence scenarios | Searched all F-rows for off-by-one, caps, or paging figures: none. The only counts are the review's own tally | NOT MET |
| I5 | Interaction effects when components combine | F18 "Duplicate-mechanism risk ... `shared_package_ids` ... watcher claims one issue per cycle ... Collision Lens"; F14 LLM output into a deterministic catalogue; F16 cadences | MET |

Subtotal Invariant and edge-case: 3/5 (floor check: PASS, eligible)

**V4 total: 24/30** (Completeness 4, Correctness 4, Structure 5, Clarity 5, Risk 3, Invariant 3)

## Variant 3 (Coder#477 workspace listener versus Orchestrator mode and the TUI observer)

### V3 Completeness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | Covers all explicit requirements from the source input | Sources validated ("Claim check of Coder#477", 8 paths plus related issues); best action per point (Edits 1-12, Q1-Q7); dependencies ("What IronClaude must supply or wait for", 7 items); issue and PR coverage (Coder#477, #331, #450, #339, #409, PR #539); alignment verdicts (F1-F17). But the TUI-observer half is judged from the #409 draft only: scope read says of #409 "only checked that its live body contains 'Coder#477'", and `round2-rebuttal-V3.md` row 6 concedes "V3 never checked that a built observer exists or what 'TUI Panel' means" (V5 #6) | NOT MET |
| C2 | Addresses edge cases and failure scenarios | F6 "A Minimal workspace has no Orca and no IronClaude ... #477 has no criterion for a stopped, restarting or deleted workspace, for a stale registration, or for deregistration"; F8 "A held message in an interactive session opens a dialog and is dropped after `dialogExpiry`"; F14 anonymous heartbeat | MET |
| C3 | Includes dependencies and prerequisites | "What IronClaude must supply or wait for": "A decision on option A versus B or C (Q1)", "An identity and ownership envelope for the sweep output", "The trust-grant format"; Edit 12 "Depends on: the owner's decision on ... section 2.3 ..." | MET |
| C4 | Defines success or completion criteria | Edits 4-9 are testable acceptance criteria, e.g. "A live test records that the prompt ran as a slash command and the permission mode of the launched session"; "a test shows this" (Edit 6) | MET |
| C5 | Specifies what is explicitly out of scope | Edit 10: "Reading any supervision data except through the read-only status route ... Choosing or building the trust-grant format ... Reusing the central heartbeat collector ... Sending a prompt to a running session through Claude Code cross-session messaging."; "Not read: the full PRD ... `collector/app.py` ..." | MET |

Subtotal Completeness: 4/5

### V3 Correctness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | No factual errors or hallucinated claims | `round2-rebuttal-V3.md` section 1 concedes: row 1 Edit 5 "produced without any write" is false for `sweep run` (it writes a report; a sidecar JSON breaks `test_readonly.py:400`); row 2 Edit 8 omits the second governed agent of `/sc:issue --claim`; row 3 all `i409-new-body.md:NN` cites are to a stale scratch copy, not the live #409 body | NOT MET |
| K2 | Technical approaches feasible with stated constraints | Edit 5: "A registered workspace returns ... the JSON object printed by `superclaude sweep run` ... The reply is produced without any write". Withdrawn in Round 2 ("drop the sweep JSON as the payload of any #477 route in Phase 1"): the one-report-file rule (NFR-001) and the sweep's own report write make it unachievable | NOT MET |
| K3 | Terminology used consistently and accurately | F3 refuses to equate "monitor" with the #339 management server, the TUI, or the heartbeat collector and lists the three Coder-side "monitors"; F7 separates "orchestrator" from "coordinator" as an address; "listener" used only for the #477 sense | MET |
| K4 | No internal contradictions | Verdict tally "4 contradictions (F1, F2, F8, F17), 10 gaps (F4, F5, F6, F7, F10, F11, F12, F13, F14, F15), 2 unknowns (F3, F9), 1 aligned group (F16)" sums to 17 and matches the table; "Edits 1, 2, 10, 11 and 12 hold whatever the owner answers" is consistent with Q1's "keep option A ... rescope #477" | MET |
| K5 | Claims supported by evidence or rationale | `file:line` throughout ("`launch.py:95-116`", "`issue-watcher.md:47-49`", "`ccsession:135-140`", "`collector/README.md:10`"), docs quoted for Claude Code cross-session rules, UNVERIFIED flags on the Claude Code version and sign-in mode | MET |

Subtotal Correctness: 3/5

### V3 Structure

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Logical section ordering | Scope read, claim check, alignment findings, what IronClaude must supply, proposed edits, owner questions, verdict | MET |
| S2 | Consistent hierarchy depth | H2 sections; one H3 ("What IronClaude must supply or wait for") under "Alignment findings"; edits as numbered bold items | MET |
| S3 | Clear separation of concerns | Claim check (paths and related issues) apart from findings, apart from IronClaude-side dependencies, apart from edits | MET |
| S4 | Navigation aids | IDs F1-F17, "Edit 1" to "Edit 12" and "Q1" to "Q7" referenced from the findings table ("Proposed change: Edit 8", "owner question Q1") | MET |
| S5 | Follows conventions of the artifact type | Review report: reviewer line, scope read, verdict vocabulary "contradiction / gap / unknown / aligned", verdict section | MET |

Subtotal Structure: 5/5

### V3 Clarity

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Unambiguous language | Edits are definite; owner choices are bracketed placeholders ("Text in `[brackets]` is for the owner to fill"); uncertain facts carry "UNVERIFIED" | MET |
| L2 | Concrete rather than abstract | Corrected real paths for five files, literal blockquote edits, exact commands ("`orca agent launch --worktree path:<checkout> --surface terminal --prompt ...`") | MET |
| L3 | Each section has a clear purpose statement | "Points judged: (a) what a registered workspace must expose; (b) read-only boundary; (c) one trust design; (d) Claude Code cross-session rules; (e) what 'monitor' means."; "Each is one decision with a recommendation." | MET |
| L4 | Acronyms and domain terms defined on first use | Options and gates are glossed inline ("D1 option A 'No listener, inbound port or address registry'", "bypass mode ... holds each message"); stray unglossed ids ("FU-1", "FU-2", "NFR22", "R9") are peripheral | MET |
| L5 | Actionable next steps or decision points | "Recommended action: the owner answers Q1 and Q2, then #477 is edited per Edits 1 to 12 (post nothing before the answers)"; seven owner questions with recommendations | MET |

Subtotal Clarity: 5/5

### V3 Risk coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | At least 3 risks with probability and impact | F14 is labelled "gap (risk)" and F8, F11 describe consequences, but no finding carries a likelihood or severity rating; searched the findings table and verdict | NOT MET |
| R2 | Mitigation for each identified risk | Each finding has "Proposed change" (F10 "Edit 6" separate read and send credentials; F14 "Edit 10 (out of scope line)"; F11 "Edit 6, Edit 7") | MET |
| R3 | Failure modes and recovery procedures | Edit 9: "A request for a stopped or stale workspace is refused with a stated reason; it is never queued silently."; "A registration not refreshed for [N minutes: owner decides] shows as stale ... A deleted workspace's registration is removed." | MET |
| R4 | External dependencies and their failure scenarios | F9 Claude Code messaging "If they use a gateway, Claude Code cannot carry a message between two workspaces"; F8 `crossSessionInbound` "all-or-nothing, not per sender"; F14 central collector "anonymous (no auth)" | MET |
| R5 | Monitoring or validation mechanism | Edit 6 "a test shows this"; Edit 8 "A live test records that the prompt ran as a slash command and the permission mode of the launched session"; Edit 7 audit lines "can be joined to the watcher's `audit.jsonl`" | MET |

Subtotal Risk coverage: 4/5

### V3 Invariant and edge-case coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Boundary conditions for collections | F6: "`profiles.yaml:14-21` ... profile `minimal` has only `claude-code`. A Minimal workspace has no Orca and no IronClaude" (the zero-orchestrator member of "every workspace"); Q5 "Should a Minimal-profile workspace register?" | MET |
| I2 | State variable interactions across component boundaries | F4 "All workspaces run the same image with `HOME=/home/coder` ... so a path ... is not unique across workspaces"; F13 "two unconnected records unless both carry the issue number and workspace id" | MET |
| I3 | Guard condition gaps | F10 "no criterion keeps a read credential from reaching the send route"; F11 "does not say that no offer or standing credential may be registered"; F14 anonymous endpoint breaks "unauthorized requests are rejected" | MET |
| I4 | Count divergence scenarios | Claim-check table: "five of the eight paths are wrong"; draft-notes line cites "`module.tf:49-55` holds for the pair app (50-56, off by one)"; "`main.tf:103-108` covers the hash locals, not the image resource (110)" | MET |
| I5 | Interaction effects when components combine | F1 watcher (poller) versus #477 (listener); F8 listener-routed prompt versus Claude Code cross-session rules ("`/sc:issue --claim 396` sent as a peer message ... is plain text"); F13 watcher audit plus listener audit | MET |

Subtotal Invariant and edge-case: 5/5 (floor check: PASS, eligible)

**V3 total: 26/30** (Completeness 4, Correctness 3, Structure 5, Clarity 5, Risk 4, Invariant 5)

## Variant 2 (issue #450 watcher rollout versus Orchestrator mode and the TUI observer)

### V2 Completeness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | Covers all explicit requirements from the source input | Sources validated (W-rows with `file:line`); action per point ("proposed change" column plus "Proposed edits to #450" 1-5); dependencies ("Waits for Orchestrator mode Phase 2 (or #534) ... Does not need to wait: items 1, 2, 4"); issue and PR coverage (#450, #331, #394, Coder#477, PR #425/#447/#448/#485); alignment verdicts (W-01..W-16). The observer is treated only as a future reader: W-10 "Do not build an observer reader before FU-1". `round2-rebuttal-V2.md` row 9 concedes "All of V1 to V4, V2 included, missed the observer in their own checkout" and row 1 concedes the "observer reader" wording | NOT MET |
| C2 | Addresses edge cases and failure scenarios | W-15 "A refused or failed launch (`W-ENFORCEMENT-ABSENT`) therefore still reads as claimed"; W-09 launched session may stall "at the ccsession Session Name prompt"; W-11 "`healthy` is false during the shadow run, the kill switch and `enabled: false`" | MET |
| C3 | Includes dependencies and prerequisites | "Waits for Coder#477: any routing of an approved prompt ..."; W-02 "add to #450 a precondition 'OB-H1 item 1, OB-H2, OB-H3 recorded as passed (#394)'"; "FU-2 cron stays behind FU-1" | MET |
| C4 | Defines success or completion criteria | Proposed edit 1 "Add 'Done when 0: decide the claim level the watcher passes ...'"; edit 3 lists what the FU-1 record must contain (identity fields, before/after `run-list`, permission mode, tab-map entry) | MET |
| C5 | Specifies what is explicitly out of scope | "Not read: the #409 design package on the git ref ..., PR diffs of #447/#448/#485, the hook scripts, `tests/sweep/` ..."; W-05 "No Phase 1 code change"; "a write path and out of the observer's scope" | MET |

Subtotal Completeness: 4/5

### V2 Correctness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | No factual errors or hallucinated claims | `round2-rebuttal-V2.md` section 1 withdraws: row 1 W-10 "observer reader" (the built observer has no watcher input); row 6 "absent by construction" for the Run record (inference, not proof); row 7 cites by line into a `/tmp` scratch copy of #409; row 4 W-05's mislabel claim depends on `session_join`, which V2 did not run | NOT MET |
| K2 | Technical approaches feasible with stated constraints | W-01 fix is a bounded code change ("`/sc:issue --claim <N> --pipeline none` ... Edit `launch.PROMPT_PATTERN`, `build_claim_prompt`, the 12-element argv pin and the NFR-001 property test; the variable part stays an integer"); FU-1 capture steps use read-only verbs only (`run-list`, `worker-list`, `worktree ps --json`) | MET |
| K3 | Terminology used consistently and accurately | "Run-less", "transcript-only row", "person-started", "machine-started" used the same way across W-03, W-04, W-05 and Q3; verdict vocabulary fixed | MET |
| K4 | No internal contradictions | Fact 2 asserts "So the session has no Run and no Dispatch row" and W-04 says "Run binding is absent by construction", while the same fact 2 says "UNVERIFIED: that Orca writes no Run record at all" and W-04 asks to "Mark the sweep's 'no Run' statement in #409 item 9 UNVERIFIED until then" (it applies to #409 a standard it does not apply to its own claim) | NOT MET |
| K5 | Claims supported by evidence or rationale | `launch.py:95-116`, `classify.py:748-767`, `issue.md:43`, `claim.md:131`, live `orca-ide agent launch --help` and `worktree ps --json` key counts | MET |

Subtotal Correctness: 3/5

### V2 Structure

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Logical section ordering | Scope read, "How a watcher-launched session appears to the sweep" (facts first), alignment findings, proposed edits, owner questions, verdict | MET |
| S2 | Consistent hierarchy depth | H2 sections only, numbered facts 1-7 and numbered edits 1-5; no orphan levels | MET |
| S3 | Clear separation of concerns | Facts (7 numbered), judgements (W-table), edits, questions are in separate sections | MET |
| S4 | Navigation aids | W-ids cross-referenced ("(W-01, W-02)", "(W-03, W-04, W-08, W-09)"), Q1-Q4 referenced from findings ("Owner question Q1") | MET |
| S5 | Follows conventions of the artifact type | Review report with scope read, verdict vocabulary "aligned, gap, contradiction, unknown", verdict | MET |

Subtotal Structure: 5/5

### V2 Clarity

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Unambiguous language | "Recommended: change the fixed prompt to `/sc:issue --claim <N> --pipeline none` (claim ends after the comments, no worktree, no agent: exactly decision D2)"; uncertain items carry "UNVERIFIED" | MET |
| L2 | Concrete rather than abstract | Exact runbook step "1.3a: create the watcher worktree with `orca worktree create --name issue-watch --agent claude --prompt \"<task>\"`"; exact capture fields (pane key, terminal handle, session id) | MET |
| L3 | Each section has a clear purpose statement | "Facts first, each with its source."; "Verdicts: aligned, gap, contradiction, unknown."; "Summary: to the sweep, a watcher session is an unowned, Run-less transcript ..." | MET |
| L4 | Acronyms and domain terms defined on first use | Most are glossed where they appear ("FU-1 live test (a claim on a test issue)", "the claim's own ship gate ... OB-H1 item 1, OB-H2 and OB-H3", "path A ... path B" defined in W-03); stray ids ("T-10", "FU-6", "#315 problem") are peripheral | MET |
| L5 | Actionable next steps or decision points | Four owner questions (Q1 "Should the watcher's claim run at `--pipeline none` ... or at the default `worktree`?") and five proposed edits | MET |

Subtotal Clarity: 5/5

### V2 Risk coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | At least 3 risks with probability and impact | W-01, W-02, W-08, W-15 describe consequences; none has a likelihood or severity rating. Only frequency figures ("up to 6 a day") appear, in W-07 | NOT MET |
| R2 | Mitigation for each identified risk | Each W-row has a "proposed change" (W-01 `--pipeline none`; W-02 precondition; W-08 FU-1 text; W-11 show "disabled/planned stop") | MET |
| R3 | Failure modes and recovery procedures | Failure modes are named (W-09 stall at the name prompt, W-15 failed launch reads as claimed, W-11 planned stop reads as a fault) but no recovery step is given for any: searched W-09, W-11, W-15, verdict | NOT MET |
| R4 | External dependencies and their failure scenarios | W-04 `agent launch` is outside the orchestration verbs ("`orca-ide agent launch --help`"); W-09 launch depends on the Orca Claude command being `ccsession-orca`; W-02 the #394 ship gate | MET |
| R5 | Monitoring or validation mechanism | Edit 3 FU-1: "the before/after `run-list` check; the Orca Claude command, the session name behaviour and the tab-map entry; the permission mode"; W-04 "run read-only `orca orchestration run-list` and `worker-list`" before and after the test launch | MET |

Subtotal Risk coverage: 3/5

### V2 Invariant and edge-case coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Boundary conditions for collections | W-07 "All watcher sessions (up to 6 a day, left open) start in one configured worktree"; Q4 "may that one worktree hold up to 6 new sessions a day?"; scope read "29 worktrees and 43 `claude` agent rows" | MET |
| I2 | State variable interactions across component boundaries | W-03 the watcher keeps only `operation_id` while the sweep joins by transcript `sessionId` or tab-map pane key, so the two records cannot be joined; W-15 claimed-detection reads a comment posted before any Orca step | MET |
| I3 | Guard condition gaps | W-01 the fixed prompt pattern `^/sc:issue --claim [1-9][0-9]{0,8}$` omits the pipeline flag so the default level runs; W-08 "outside the #394 launch-level guard" | MET |
| I4 | Count divergence scenarios | W-12 "says 2655 tests where the PR bodies say 2637 and 2653"; "a live call listed 29 worktrees and 43 `claude` agent rows" | MET |
| I5 | Interaction effects when components combine | W-05 the sweep would label a watcher session "person session (active)" through `_person_origin` and rule 8; W-06 diagram and design disagree on a coordinator; W-01 claim plus a governed second agent | MET |

Subtotal Invariant and edge-case: 5/5 (floor check: PASS, eligible)

**V2 total: 25/30** (Completeness 4, Correctness 3, Structure 5, Clarity 5, Risk 3, Invariant 5)

## Variant 1 (issue #409 TUI observer versus Orchestrator mode Phase 1)

### V1 Completeness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| C1 | Covers all explicit requirements from the source input | Sources validated ("Claim check of the new #409 body", 39 claims); action per point ("Smallest change" column, W-1..W-7); dependencies ("Missing for integration", 10 items); issue and PR coverage (#409, #539, #541, #532, #339, #534, #423, #444, #450, Coder#477); alignment verdicts (F-01..F-18, A-01..A-15). The built observer is absent: C-03 "No observer code exists; 20 synthetic designs await a human choice (L16)" is marked "Verified"; `round2-rebuttal-V1.md` row 1: "'No observer exists' is false ... Concede in full" | NOT MET |
| C2 | Addresses edge cases and failure scenarios | Missing item 5 "Error and stale-data handling. Exit 1 and 2 leave no JSON and no report ... a report is complete only if it ends with `Report complete` ... source loss never turns into `finished` or 'all clear'"; F-12 idle or dead coordinator means no new report | MET |
| C3 | Includes dependencies and prerequisites | "Missing for integration: Nothing below exists in #409 or in the Phase 1 design today" followed by 10 numbered prerequisites (data contract, field names with one source each, vocabulary mapping, cadence ...) | MET |
| C4 | Defines success or completion criteria | "Acceptance criteria of #409" table A-01..A-15 with verdicts and four added criteria, e.g. "A-12 (added) Observer shows the same facts as the sweep, or documents every difference" | MET |
| C5 | Specifies what is explicitly out of scope | "Not done: no live `superclaude sweep run` ... and no live Orca call"; "Not read: ... QA.md of the design package"; F-05 cites "#409 Out of Scope (L195) lists terminating and deleting worktrees" | MET |

Subtotal Completeness: 4/5

### V1 Correctness

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| K1 | No factual errors or hallucinated claims | `round2-rebuttal-V1.md` section 1 withdraws C-02, C-03, C-21, C-26, A-01 "aligned", A-05..A-07 as gaps, F-01 "(1) observer reads the JSON", F-04/F-12/F-14/F-15 as observer gaps, Q1 and W-3 (row "Net"); row 9 the `gh pr list --head` method cannot see squash-merged PRs; row 7 cites a stale scratch copy | NOT MET |
| K2 | Technical approaches feasible with stated constraints | Owner Q1 and "Missing for integration" 1: "persist: write `<stem>.json` beside each report (recommended)... same atomic link publish". `round2-rebuttal-V1.md` row 5: NFR-001 "a sweep adds exactly one report file" is pinned by `tests/sweep/test_readonly.py:300-400` and `test_cli_contract.py:1361`; a sibling `.json` needs a second link with its own free-name search, so the "same atomic link publish ... understated" | NOT MET |
| K3 | Terminology used consistently and accurately | Fixed vocabulary "aligned / gap / contradiction / unknown"; "UNVERIFIED means I could not confirm it from a source I opened"; "Body" and "JSON v1" used the same way throughout | MET |
| K4 | No internal contradictions | Verdict "Both are read-only and share the same dimension names" versus F-02 "Gap and contradiction in vocabulary" and C-02 (digest X-008, all five advocates); header tally "2 UNVERIFIED (C-37; C-08 rebase part and the 'not confirmed' label in C-07)" lists three items and counts C-08 twice (digest X-009) | NOT MET |
| K5 | Claims supported by evidence or rationale | Each C-row has an Evidence cell (GraphQL thread counts, `report.py:642-661`, `test_cli_contract.py:992,1016`, blob size and SHA-256 of the ZIP) | MET |

Subtotal Correctness: 2/5

### V1 Structure

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| S1 | Logical section ordering | Scope read, claim check, alignment findings (points, acceptance criteria, proposed wording), missing for integration, owner questions, verdict | MET |
| S2 | Consistent hierarchy depth | H2 sections; H3 "Alignment points", "Acceptance criteria of #409", "Proposed wording" under "Alignment findings" | MET |
| S3 | Clear separation of concerns | Claim check (C-rows) versus alignment (F-rows) versus acceptance criteria (A-rows) versus wording (W-rows) versus prerequisites | MET |
| S4 | Navigation aids | Four id families C-/F-/A-/W- with cross-references ("Fix wording is under Alignment findings (F-07 for C-07 and C-18, F-02 for C-25 ...)", "(W-6)", "(F-03)") | MET |
| S5 | Follows conventions of the artifact type | Review report: status line, conventions, scope read, claim table, findings table, owner questions, verdict | MET |

Subtotal Structure: 5/5

### V1 Clarity

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| L1 | Unambiguous language | "Owner decision, with a recommended answer: allow observation fields ...; do not render `Next inspection`"; "Recommended: persist"; unverified items labelled | MET |
| L2 | Concrete rather than abstract | W-1..W-7 literal replacement sentences; exact field list in Missing item 2 ("`run`, `worktree_path`, `branch` (not read today), `last_activity` ...") | MET |
| L3 | Each section has a clear purpose statement | "Verdict words: aligned / gap / contradiction / unknown."; "Nothing below exists in #409 or in the Phase 1 design today (checked in the files listed under Scope read)."; "Each is a choice, with the recommendation I would make." | MET |
| L4 | Acronyms and domain terms defined on first use | Conventions define "Body" and "UNVERIFIED"; the ten dimensions are enumerated in F-02; "WC-16 is a cap (at most once per 5 minutes) on coordinator wakes" (F-12); "SP-22: person deletes by hand" glossed; stray ids ("FIN-F7", "D-05 to D-12") sit in citation cells | MET |
| L5 | Actionable next steps or decision points | Nine numbered owner questions each with a recommendation; W-1..W-7 | MET |

Subtotal Clarity: 5/5

### V1 Risk coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| R1 | At least 3 risks with probability and impact | Only two items carry a severity word (C-07 "Augment medium"; F-07 "P2 badge, 'Medium' in the summary comment"), and no likelihood is stated for any risk; searched F-rows and verdict | NOT MET |
| R2 | Mitigation for each identified risk | Each F-row has a "Smallest change"; F-07 "fix before merge (limit paths to the selected repository and disable executable git config) or record as accepted in design section 13" | MET |
| R3 | Failure modes and recovery procedures | Missing item 5: "newest report unreadable or truncated (a report is complete only if it ends with `Report complete`), `orca_available: false`, any `sources[].unscanned` ... Last-known data stays qualified with its age"; F-12 "no report or unreadable report is 'unavailable', never 'all clear'" | MET |
| R4 | External dependencies and their failure scenarios | F-07 `git status` runs "with the inherited environment ... `core.fsmonitor` can execute"; F-09 "whether `worktree ps --json` carries linked issue or PR fields is UNVERIFIED (Orca docs not read)"; F-04 remote hosts row `unknown` | MET |
| R5 | Monitoring or validation mechanism | "Test the 80 and 100 session scenarios against the 50-call cap before promising them" (F-04); Missing item 8 "A v1-shaped fixture set ... including `could not determine` rows past the 50-call cap" | MET |

Subtotal Risk coverage: 4/5

### V1 Invariant and edge-case coverage

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| I1 | Boundary conditions for collections | F-04 "rows past 50 are `could not determine` (`bound_reached`), and a 100-row `worker-list` page sets `truncated` with no paging"; scenarios 5/8/10 owners and 50/80/100 sessions; "No matching records. This is not an all-clear." | MET |
| I2 | State variable interactions across component boundaries | F-03 JSON on stdout only versus Markdown on disk, so a reader needs a third copy; F-15 delta "needs two persisted JSON files"; "Exit 1 or 2 prints no JSON and writes no report" | MET |
| I3 | Guard condition gaps | F-07 `_worktree_paths` accepts every path from `worktree ps` and `--no-optional-locks` does not stop `core.fsmonitor`; F-18 header prints fixed `Messages coverage: partial` even when `orca_available` is false; C-25 Policy is a JSON key although the body says no dimension is | MET |
| I4 | Count divergence scenarios | C-07 "6 threads. 4 resolved ... 2 unresolved" against the body's "Five review findings"; C-25 "The test pins nine (DIMENSION_KEYS) ... `policy` is a JSON row key"; C-36 "406 package files plus checksum manifest ... 407 zip entries" | MET |
| I5 | Interaction effects when components combine | F-05 observer "navigation only" rule versus `safe_to_close` and `removable` in JSON; F-02 `unknown` rendered as `not admitted` or `not frozen`; F-13 Markdown-escaped JSON strings versus observer re-sanitising | MET |

Subtotal Invariant and edge-case: 5/5 (floor check: PASS, eligible)

**V1 total: 25/30** (Completeness 4, Correctness 2, Structure 5, Clarity 5, Risk 4, Invariant 5)

## Summary (PASS 2, reverse order)

### Dimension subtotals and totals

| Dimension (5 criteria each) | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| Completeness | 4 | 4 | 4 | 4 | 4 |
| Correctness | 2 | 3 | 3 | 4 | 3 |
| Structure | 5 | 5 | 5 | 5 | 5 |
| Clarity | 5 | 5 | 5 | 5 | 4 |
| Risk coverage | 4 | 3 | 4 | 3 | 4 |
| Invariant and edge-case | 5 | 5 | 5 | 3 | 5 |
| **Total (of 30)** | **25** | **25** | **26** | **24** | **25** |
| qual_score (total / 30) | 0.833 | 0.833 | 0.867 | 0.800 | 0.833 |

### Invariant and edge-case floor check (a variant under 1/5 is ineligible as base)

| Variant | Invariant score | Eligible as base |
|---|---|---|
| V1 | 5/5 | yes |
| V2 | 5/5 | yes |
| V3 | 5/5 | yes |
| V4 | 3/5 | yes |
| V5 | 5/5 | yes |

No variant is under 1/5. The floor is not suspended.

### Per-criterion verdict matrix (for the position-bias reconciliation against the forward pass)

M = MET, N = NOT MET. Order of columns: V5, V4, V3, V2, V1 (evaluation order of this pass).

| Criterion | V5 | V4 | V3 | V2 | V1 |
|---|---|---|---|---|---|
| C1 all explicit requirements | M | N | N | N | N |
| C2 edge cases and failures | M | M | M | M | M |
| C3 dependencies and prerequisites | M | M | M | M | M |
| C4 success or completion criteria | N | M | M | M | M |
| C5 out of scope | M | M | M | M | M |
| K1 no factual errors | N | N | N | N | N |
| K2 feasible approaches | N | M | N | M | N |
| K3 terminology | M | M | M | M | M |
| K4 no internal contradictions | M | M | M | N | N |
| K5 evidence for claims | M | M | M | M | M |
| S1 ordering | M | M | M | M | M |
| S2 hierarchy depth | M | M | M | M | M |
| S3 separation of concerns | M | M | M | M | M |
| S4 navigation aids | M | M | M | M | M |
| S5 artifact-type conventions | M | M | M | M | M |
| L1 unambiguous language | M | M | M | M | M |
| L2 concrete | M | M | M | M | M |
| L3 purpose statements | M | M | M | M | M |
| L4 terms defined on first use | N | M | M | M | M |
| L5 actionable next steps | M | M | M | M | M |
| R1 3 risks with probability and impact | N | N | N | N | N |
| R2 mitigation per risk | M | M | M | M | M |
| R3 failure modes and recovery | M | N | M | N | M |
| R4 external dependencies and failures | M | M | M | M | M |
| R5 monitoring or validation | M | M | M | M | M |
| I1 collection boundaries | M | N | M | M | M |
| I2 state interactions across boundaries | M | M | M | M | M |
| I3 guard condition gaps | M | M | M | M | M |
| I4 count divergence | M | N | M | M | M |
| I5 interaction effects | M | M | M | M | M |

### What drove the scores, and the judgement calls a reconciler should look at

1. Correctness K1 is NOT MET for all five. Each variant has at least one claim a Round 2 rebuttal conceded or withdrew (V1 "no observer exists"; V2 "absent by construction" and the "observer reader"; V3 Edit 5 "without any write"; V4 Edit 3 "both read the same sweep facts" and "confines every path"; V5 O-05, BC-17, X-019, X-020).
2. C1 is MET only for V5. V1 to V4 judge alignment with the TUI observer without examining the built `superclaude observe` (the Round 2 files concede this for V1 row 1, V2 row 9, V3 row 6, V4 row 1). This is the largest judgement call: if a reconciler reads C1 as "covers the requirements for the review's own subject" instead of "also the observer half", V1 to V4 each gain one point (V1 26, V2 26, V3 27, V4 25).
3. K2 (feasibility) splits on the one-report-file rule (NFR-001, `test_readonly.py:300-400`, `test_cli_contract.py:1192,1361,1474`): V1 (persist `<stem>.json`), V3 (Edit 5) and V5 (F-03, D5(ii)) each rest on something the debate showed infeasible or unproven. V2 and V4 do not.
4. K4 (internal contradictions) is NOT MET for V1 (verdict "share the same dimension names" versus F-02; header tally, digest X-009) and V2 ("no Run" stated as fact and as UNVERIFIED in the same section).
5. R1 (probability and impact) is NOT MET for all five: none of the variants rates likelihood and consequence for three or more risks. This is a rubric-versus-artifact mismatch (alignment reviews use verdict words, not probability scales), applied the same way to all.
6. L4 and R3 are the closest calls. L4 is NOT MET for V5 only (WC-16, NFR-014, INV-017 and TUIBBS used without a gloss); the others gloss their load-bearing terms inline and leave only stray ids in citation cells. R3 is NOT MET for V2 and V4, which name failure modes and give prevention edits but no recovery step.
7. V4 is lowest because it has no collection-boundary case (I1) and no count-divergence case (I4); both are genuine absences (searched F2-F6, F18 and the verdict), not scoring severity. V4's 3/5 on this dimension is above the floor.
8. Digest points that depend on this layer: the margin between the top total (V3, 26) and the rest (24 to 25) is one point, inside the 5% tiebreak band of the scoring protocol (0.05 of the combined score), so this layer alone does not decide the base.

### Totals (this pass)

V5 25/30, V4 24/30, V3 26/30, V2 25/30, V1 25/30.
