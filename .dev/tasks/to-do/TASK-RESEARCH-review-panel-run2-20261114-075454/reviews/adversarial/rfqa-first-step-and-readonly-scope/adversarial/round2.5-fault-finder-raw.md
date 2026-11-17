# Round 2.5: Invariant probe, fault-finder (slot C-11, rfqa-first-step-and-readonly-scope)

Probed: the EMERGING CONSENSUS (the "Proposed resolution" of `round2-advocate-A.md:117-130` and `round2-advocate-B.md:159-172`, plus B's "Response to A's proposed resolution", `round2-advocate-B.md:144-157`). Not an advocate for either variant.
Method: code read-only under `src/` and `tests/` of the `brainstorm-reflect-panel` worktree; three read-only `uv run --no-project python` scripts over `/home/coder/.claude/projects/*/*/subagents/*.meta.json` and sibling `.jsonl` (tool calls de-duplicated by `tool_use` id; results matched by `tool_use_id`; scratch only in `mktemp -d /tmp/ff-c11*.XXXXXXXX` dirs removed by exit traps). Every transcript containing the run-1 task id or the queued-run file name was skipped before parsing: 117 (rf-qa 74, rf-qa-qualitative 43), the same count both advocates report.
Tags: [CODE-VERIFIED] read at the cited path:line this session; [RUN-VERIFIED] observed by the scripts this session; [UNVERIFIED].

ID: INV-001
CATEGORY: state_variables
ASSUMPTION: Arm 0 (current lens agents) in the replay oracle behaves like the same agents at a real `/task` gate, so arm 0 versus arm 1a measures production recall and production write behaviour.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The spawn `mode` argument is ignored and "Subagents inherit the parent session's permission mode" (diff-analysis.md:50, X-004, both advocates accept). So what arm 0 may write or run depends on the permission mode of the session that runs the oracle, not on `task/SKILL.md:225, 241`. Every subagent also receives the installed SubagentStart hook context (`src/superclaude/hooks/hooks.json:159-175` registers `freshness-subagent-start.sh` and `pragmatic-subagent.js`; the latter injects `~/.claude/output-styles/pragmatic.md` whole) [CODE-VERIFIED]. Neither resolution pre-registers the oracle's parent permission mode, the installed hook set or the model alias as fixed conditions. An oracle run from a default-mode headless session would show arm 0 with blocked or prompted writes that a bypass-mode production gate does not have, and the tree-hash metric for arm 0 would then under-state production mutation.

ID: INV-002
CATEGORY: guard_conditions
ASSUMPTION: The lens-identity check ("a report whose first line names another lens is a blocker", `round2-advocate-B.md:137, 167`) reliably detects a mis-dispatched reviewer, which is the only defence left against N1's failure once persistence is keyed by slot (B's own NB3, `round2-advocate-B.md:54, 66`).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: (1) Guard undefined for the common case: the rule fires on a first line that names ANOTHER lens; a first line that names NO lens is neither pass nor fail, so a misdirected reviewer that starts with prose slips through and the vacuous case recreates N1 as a silent coverage gap. (2) The closest analogue does not keep a mandated first line: `reflect-reviewer.md:73-76` mandates line 1 `# Reflect Reviewer — Deviation Findings` with the persona on line 3; across 517 reflect-reviewer returns only 37 start with that heading, 160 start with a code fence, 89 with another heading, 229 with prose, 2 are empty; the persona appears in the first 6 lines of 217 (42%) [RUN-VERIFIED]. The `/task` report format puts the lens in line 1 (`task/SKILL.md:475`, `# QA Report — [Lens Name]`) [CODE-VERIFIED], but model compliance with a "first line" rule is not measured anywhere in the consensus. Either the check is lenient (vacuous) or strict (most returns become blockers and force re-spawns). (3) Identity is self-declared: the N1 agent believed it was the design-correctness lens (NB1), so the check works there only because the agent declared its mistaken lens; an agent that declares the dispatched lens but reviews another item's text passes.

ID: INV-003
CATEGORY: guard_conditions
ASSUMPTION: The tree-hash no-mutation check on every replay run detects the write classes that matter (A-R2 item 4, B-R2 item 4).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Arm 0 agents legitimately write their own report into the gate's `qa/` folder (`task/SKILL.md:238`) [CODE-VERIFIED], so a whole-tree hash always differs for arm 0 unless own-report paths are excluded; excluding the `qa/` folder blinds the check to N1's class (another lens's report inside `qa/`, `round2-advocate-B.md:86-90`). The scope (per-path hashes with a per-agent allowlist of exactly one own path) is not specified. A working-tree hash also misses git-state changes: the git stash stack is shared by every worktree of the repository, so a reviewer's `git stash` changes repository state with no working-tree hash change; M-B1's class (c) covers git state for the audit (`round2-advocate-B.md:165`), the replay check does not. `/tmp` scratch is outside any repository tree hash, which is intended but means arm 0's mutation-testing work is invisible to the metric.

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: A guard that the new agent file's `tools` list is a subset of a named read-only set proves the agent that actually runs is read-only.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: (1) The guard reads the source file (`tests/cli/reflect/test_reviewer_readonly_tools.py:25` reads `src/superclaude/agents/reflect-reviewer.md`) [CODE-VERIFIED]; at runtime agents resolve from the project `.claude/agents/` first, then `~/.claude/agents/` (repo CLAUDE.md, "Dual surface" rule). `make verify-sync` compares `src/` with `.claude/` only; the installed copy under `~/.claude/agents/` and copies in other projects are not covered, so a stale or user-edited same-name agent with a wider list runs while the guard passes. An uninstalled new agent in another project makes the `subagent_type` unresolvable; what the prose `/task` executor then spawns instead (for example `rf-qa` or `general-purpose`) is unspecified. (2) Parser form: the reflect guard parses only the inline `tools: a, b` form (`test_reviewer_readonly_tools.py:37, 53-56`); `rf-qa.md:6-34` uses the YAML-list form, under which `_parse_tools` returns None. A body copied from `rf-qa.md` with its frontmatter style fails the copied guard (fail-closed, so a build break, not a hole); a hand-written YAML-aware parser must also reject `disallowedTools`-only definitions and an empty list. `tests/agents/test_tavily_tool_parity.py:87-100` (`_declared_tools`) already parses both forms and is the reusable helper.

ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: The named mutator set must contain the spawn and message tools, not only file tools (A-R2 item 3; B-R2 item 3 adds TaskOutput, TaskStop, MultiEdit).
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: Confirmed as a real exposure, not a theoretical one: across rf-qa / rf-qa-qualitative transcripts (fix and non-fix) there are 15 successful `Agent` calls, 9 `SendMessage`, 4 `Skill`, 18 `TaskStop` [RUN-VERIFIED]. Among non-fix lens transcripts, 3 spawned children; one ("Phase 3.1 gaps QA p2", no `fix_authorization: true`) spawned a write-capable `rf-qa` child "QA research gaps partition 2" [RUN-VERIFIED]. `rf-qa.md:20-31` grants Agent, Task, TaskOutput, TaskStop, SendMessage, Task*, TeamCreate/Delete, Skill [CODE-VERIFIED]. B's subset-of-a-named-read-only-set formulation excludes all of them, including `Skill`, `TeamCreate` and `AskUserQuestion` that neither mutator list names, because a subset test rejects any unlisted name.

ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: Copying the `reflect-reviewer.md:5` allowlist gives the new agent the read-only tools it is told to use, and N5's "two calls refused across 517 runs" describes allowlist behaviour.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: Over 517 reflect-reviewer transcripts, 7 calls were refused, not 2: `pool_Read` x4, `mcp__razor_culture__pool_Write` x1, `pool_Read_placeholder` x1, and `mcp__codegraph__codegraph_explore` x1 [RUN-VERIFIED]. The last is a read-only tool refused only because it is not on the list (`reflect-reviewer.md:5` names codegraph search, node, callers, impact), while the codegraph MCP server's own instructions tell agents to use `codegraph_explore` first. The `pool_*` names come from harnesses that expose built-in tools under renamed MCP names; they fail closed. Safety holds (refusal is the point); the drift is recall and turns: the named read-only set and the agent list need a rule for adding read-only tools (codegraph_explore) as tool names change, and arm 1a inherits the same refusals.

ID: INV-007
CATEGORY: count_divergence
ASSUMPTION: "The standard eight lens dimensions at `/task` steps 3-4 switch" maps one-to-one onto what a gate spawns, and "if arm 1a passes for a dimension" yields a coherent gate.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Floors are 3+3, 4+4, 5+5, 6+6 (`task/SKILL.md:196-201`) [CODE-VERIFIED]. At the 6 tier only 6 of the 8 standard dimensions run (which 2 are omitted is not specified); at the 10 and 12 tiers 2-4 lenses per gate are "Additional structural lenses as needed for the tier" (`:230, :246`), which are not standard dimensions, have no arm 1a and therefore keep `rf-qa` with self-persistence. A per-dimension switch (A-R2 item 7 "for a dimension", B-R2 item 7 "for a standard lens dimension") can pass, say, 5 of 8 dimensions, so one gate mixes executor-persisted and self-persisted reports, and the rewritten step 10 must check both modes. Eight separate per-dimension pass decisions with a small pre-registered repeat count and no multiplicity control (none is named in either resolution) make it likely that at least one dimension passes or fails by run-to-run variance alone.

ID: INV-008
CATEGORY: count_divergence
ASSUMPTION: The full M-B1 audit, classified per transcript by the write and Bash calls of the selected agent, counts every write a report-only lens caused.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: (1) Nested spawns: a lens that spawns a child (INV-005: one non-fix lens spawned a write-capable `rf-qa` child) has its child's writes in a different transcript whose own prompt may carry no `fix_authorization` literal; per-transcript classification does not attribute them to the lens, and B's "counted per spawn source" (`round2-advocate-B.md:165`) lists `/task` steps 3-4, task-file items and skill gates, not nested agents. (2) Tool-name drift: write and Bash calls also appear under renamed names (`wrestle_Bash` 19, `wrestle_Bash_placeholder` 35, `cook_Write` 2, `fever_Edit` 2, `mcp__razor_culture__bash_placeholder` 2) [RUN-VERIFIED]; all 66 were refused or errored today, so no write was missed, but a classifier keyed on the literal names Write/Edit/Bash would miss a successful renamed call. (3) The evidence counts are regex-dependent and already diverge between advocates (366 vs 278 report-only; 118 vs 107 standard-lens-named; pytest 74 vs 77; N5 "2 refused" vs 7 refused calls, INV-006); the consensus quotes them as decision inputs without pinning the classifier.

ID: INV-009
CATEGORY: collection_boundaries
ASSUMPTION: Executor persistence "to the dispatched slot's path" gives each returned report a unique path (A-R2 A-003: "executor-keyed paths plus a hash give both uniqueness and fidelity").
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The only path pattern `/task` defines is per lens name: `${TASK_DIR}qa/qa-structural-[lens-name]-report.md` / `qa-content-[lens-name]-report.md` (`task/SKILL.md:238, 260`) [CODE-VERIFIED]. Above 6 output files the gate spawns "multiple instances of each lens agent type with `assigned_files` subsets" and merges "each lens's partitioned reports before consolidation" (`:264`); above 3000 lines each lens gets a section range (`:273-275`); post-completion partitions above 15 files (`:344`). 79 of 571 non-fix lens prompts mention `assigned_files` or partition [RUN-VERIFIED]. No slot id exists in `/task` (the per-slot key was withdrawn with C-003), so "the dispatched slot's path" for two partition instances of one lens is the same file: the second executor write overwrites the first, which is N1's loss re-created by the executor. The identity check (INV-002) passes because both reports name the same lens, and the recorded sha256 is of the surviving file. The consensus needs a partition index in the persisted path and in step 10's expected-path list.

ID: INV-010
CATEGORY: collection_boundaries
ASSUMPTION: Carrying rf-qa's Confidence Gate into a read-only agent keeps the gate well defined and the UNVERIFIABLE-share metric guards against hidden capability loss.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `confidence = VERIFIED / (TOTAL - UNVERIFIABLE) * 100` and "confidence >= 95% AND UNCHECKED == 0: eligible for PASS" (`rf-qa.md:505, 509`) [CODE-VERIFIED]. TOTAL = UNVERIFIABLE divides by zero; A's original plan fixed that case in a test (diff U-002), but that rule left with the checklist mode (C-004 to B) while the formula stays in the new agent body. Near the boundary the formula rewards loss of capability: a read-only lens that marks 5 of 6 items UNVERIFIABLE (for example items that needed Bash) and verifies 1 scores 100% and is PASS-eligible. The UNVERIFIABLE share is measured only in the oracle; no production cap (for example "UNVERIFIABLE > k is not PASS-eligible") is in either resolution.

ID: INV-011
CATEGORY: collection_boundaries
ASSUMPTION: An empty or unreadable transcript corpus must not read as evidence of safety, and the run-1 skip set is applied consistently.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: B-R2 item 5 states "an empty corpus gives no verdict" (`round2-advocate-B.md:165`), answering A-R1's point (`round1-advocate-A.md:37`). The skip set reproduces: 117 transcripts skipped (rf-qa 74, rf-qa-qualitative 43) [RUN-VERIFIED], matching both advocates; 571 non-fix lens transcripts remain [RUN-VERIFIED]. Residual: the audit is blind by construction to the 117 skipped runs, which A-R2 item 12 and B-R2 item 12 record as an open evidence-quality condition.

ID: INV-012
CATEGORY: interaction_effects
ASSUMPTION: Moving persistence to the executor and adding hash and lens-line checks to step 10 protects the gate's consolidation and its proceed decision.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Step order in `task/SKILL.md`: step 6 consolidates "After ALL lens agents (Steps 3-5) return" (`:252`), step 7 fixes (`:254`), step 8 verifies (`:256`), step 9 "IF both verification agents report PASS, proceed to the next phase" (`:258`), and only then step 10 "Verify all QA reports exist on disk" (`:260`) [CODE-VERIFIED]. A rewritten step 10 that checks files, hashes and lens lines (A-R2 item 7, B-R2 item 7) therefore runs after a wrong-lens or clobbered report was already consolidated, fixed against and, on a PASS, after the gate has proceeded. Meanwhile step-5 domain and task-file lenses stay write-capable (`rf-qa.md:6-34`) and run in parallel with steps 3-4 (`:250`) into the same `qa/` folder; N1 was exactly such a lens writing another lens's path (`round2-advocate-B.md:86-90`). An executor-persisted standard report can be overwritten by a domain lens after its hash is recorded, and the mismatch surfaces only at step 10. B's per-report no-clobber check is deferred to "a separate change" (`round2-advocate-B.md:170`). The checks must run between the last return and step 6, not in step 10.

ID: INV-013
CATEGORY: interaction_effects
ASSUMPTION: The new agent's restated rule text is protected by the existing pins (B-R2 item 2: S1-S3 text "copied verbatim (`test_c_s1_s3_copied_verbatim`)"), and the scope check "passes with no test edited" (item 9) is compatible with that.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `test_c_s1_s3_copied_verbatim` is parametrized over a fixed 10-file tuple (`tests/skills/test_review_severity_rule.py:181-197`) [CODE-VERIFIED]; a new agent file is not in it, so the pin does not reach the copy unless that tuple is edited, and `test_review_severity_rule.py` is one of the suites item 9 requires to pass "with no test edited". The same holds for the independent-stance pin (`tests/skills/test_review_prompt_overrides.py:256-268`, three named files) and for the about 23 `tests/audit/*` files that pin `rf-qa.md` / `rf-qa-qualitative.md` text (for example the byte-exact halt messages in `test_monotonicity_halt_F_5_5_5.py`, `_halt_emitter.py`; NFR-CONV.9 PASS/FAIL bullets "byte-identical" in `test_nfr_conv_9_zero_trust.py:23-25`) [CODE-VERIFIED]. Copies in the new agent drift with no regression net. Naming trap: if the file is named `rf-*`, `test_rf_fallback_provenance_present` requires `mcp__tavily__tavily_search`, "Tavily-first", "fallback" and "WebSearch" in it (`tests/agents/test_tavily_tool_parity.py:142-159`) and `test_documenting_files_have_exact_parity` then requires the Tavily tool declared in frontmatter (`:65-84`), which the read-only named set does not contain; a non-`rf-` name avoids both. `src/superclaude/agents/` has 49 agents and the plugin mirror `plugins/superclaude/agents/` 21, with none of rf-qa, rf-qa-qualitative or reflect-reviewer [RUN-VERIFIED], so no plugin-mirror edit is implied.

ID: INV-014
CATEGORY: interaction_effects
ASSUMPTION: A read-only agent whose body is rf-qa's verification text returns its full report as data for the executor to persist.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Instructions the agent will receive push it to write or to return only a pointer: `rf-qa.md:540` Critical Rule 1 "Create the file immediately with a header (Write), then append ... (Edit)"; Completion Protocol "Verify the report file exists ... (Read it back)" and "return the report path and verdict as your final output" (`rf-qa.md:467-480`); and the installed SubagentStart hook injects into every subagent "Each agent MUST create its output file as a header stub on disk" and "An inter-agent return MUST be defined as a file written to disk ... MUST NOT be carried only by an in-band message" (`src/superclaude/output-styles/pragmatic.md:191, 196`, injected by `src/superclaude/hooks/scripts/pragmatic-subagent.js`) [CODE-VERIFIED]. Observed effect in the analogue: a reflect-reviewer attempted `mcp__razor_culture__pool_Write` on a reviewer-card path and was refused [RUN-VERIFIED]. A reviewer that returns "report written to X, verdict FAIL" gives the executor a two-line text to persist with a valid sha256 and possibly a valid lens line. Which of rf-qa's sections are carried (INV-016) decides whether Rule 1 and the Completion Protocol come along; the hook applies regardless.

ID: INV-015
CATEGORY: sufficiency_challenge
ASSUMPTION: "The executor persists each returned report unedited to the dispatched slot's path and records its sha256" resolves A-003 (fidelity of the persisted report to the returned text).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Falsifier 1, the hash is computed over the executor's own output: the executor is the prose `/task` orchestrator, which must re-emit each return as a Write argument; a sha256 taken of the file it just wrote proves later non-clobber, never equality with the returned text. Truncation or paraphrase at write time produces a self-consistent hash. Falsifier 2, volume: non-fix lens returns already run median 2,327, p90 12,230, max 45,774 characters; report Writes p90 10,805, max 20,713 [RUN-VERIFIED]. At a 12-lens tier plus partition instances (INV-009), the orchestrator must re-emit on the order of 150 KB per gate per phase through its output, the failure mode `rf-qa.md:540` names ("One-shotting hits max token output limits"). Falsifier 3, state window: today a lens's report is on disk when the lens finishes; under executor persistence a returned-but-not-yet-written report exists only in the orchestrator's context, so a crash, context compaction or `/task` resume between return and write loses it, and step 10 reports it missing only after step 9 (INV-012). Enumeration of what would make fidelity hold, none present in either resolution: a mechanical copy of the return from the subagent transcript or tool result by a script, or a hash computed from the tool result before the executor writes.

ID: INV-016
CATEGORY: sufficiency_challenge
ASSUMPTION: Arm 0 (current lens agents) versus arm 1a (new agent, same lens text, prose consolidation) isolates the read-only effect, so "arm 1a passes" means "read-only costs no recall".
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Branch enumeration of what differs between the arms besides the tool list: (a) Content lenses (step 4) run `rf-qa-qualitative` in arm 0, whose body is a different file with document-type QA phases (`rf-qa-qualitative.md:144` prd-qualitative, `:244` report-qualitative, `:295` tdd-, `:366` tech-ref-, `:433` ops-guide-, `:504` readme-, `:571` task-qualitative) [CODE-VERIFIED]; arm 1a gets "`rf-qa.md`'s verification, zero-trust and Confidence Gate sections" (A-R2 item 2, B-R2 item 2), so 4 of the 8 dimensions change body as well as tools. (b) "Zero-trust section" does not exist in `rf-qa.md`: its headings (`:43-538`) contain no such section, and the only body occurrence of "zero-trust" is `rf-qa.md:418` inside "QA Phase: Fix Cycle" (`:381-418`), a section the consensus drops as a "fix section"; the body is therefore not pinned and two implementers would build different arm-1a bodies. (c) Sections a structural lens may rely on are outside the named three: "Parallel Partitioning" with synthetic-dnsp emission for partition instances (`:54-86`), "Output Format (All Phases)" (`:422`), which `task/SKILL.md:426` says lens output "is inherited from". So arm 1a measures "read-only plus a different and unspecified prompt", the confound A-004 named and both advocates meant to close.

ID: INV-017
CATEGORY: sufficiency_challenge
ASSUMPTION: "Standard lenses get pre-computed counts in the brief where they used Bash" (A-R2 A-004) lets arm 1a's result transfer to production.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: In the oracle the pre-computed evidence is authored by the oracle builder against seeded documents; at a real gate someone must compute it. Enumeration of the gate steps the consensus changes: steps 3, 4, 10 and conditionally 8 (A-R2 item 7, B-R2 item 7). None adds a pre-computation step; steps 1-2 only collect output files, their size and the "ensuring..." clauses (`task/SKILL.md:221, 223`) [CODE-VERIFIED]. N3 shows 86 of 118 (A) or 79 of 107 (B) standard-lens-named transcripts used Bash, mostly for counting and parsing (`round2-advocate-A.md:53`). So either production briefs carry no pre-computed counts (arm 1a's condition does not hold in production and the measured recall does not transfer), or the prose executor computes them unmeasured (a new, untested producer of the evidence a lens trusts). Single-document seeds also cannot exercise the multi-file checks of the standard lenses ("All phases contributed their expected outputs", "No items silently dropped between phases", `task/SKILL.md:450`; cross-phase chains, `:461`) or the partitioned path (INV-009).

ID: INV-018
CATEGORY: sufficiency_challenge
ASSUMPTION: The conditional steps 3-4 switch (with or without step 8) closes INV-G for the `/task` standard lenses and the gate's verification protocol survives it.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Enumeration of every lens or verifier spawn site in `task/SKILL.md` [CODE-VERIFIED]: step 3 `:225` (switched); step 4 `:241` (switched); step 5 domain lenses `:250` (excluded, spawned "exactly as written"); step 8 verification pair `:256` (A: switched; B: only with its own arm); post-completion Step 1 `:307` and Step 2 `:320`, which spawn the same eight standard lenses with `qa_phase: "report-validation"` / `"task-qualitative"` and `mode: "bypassPermissions"`; Serialized Fix Protocol verification `:365`; fidelity agents `:395`; cross-source contradiction agent `:403`; fidelity verification `:409`. Neither resolution names `:307`, `:320` or `:365`, so whether the "standard eight lens dimensions" switch also applies to the final gate is undefined; the prose at `:359` ("They do NOT modify any files") and `:426` ("Output format is inherited from the rf-qa/rf-qa-qualitative agent definitions") stays as written and becomes false or ambiguous for switched lenses. On step 8: the verifier protocol in `rf-qa.md` is "QA Phase: Fix Cycle" (`:381-418`), with regression and monotonicity halt guards and byte-exact halt messages pinned by `tests/audit/test_monotonicity_halt_F_5_5_5.py`, `test_regression_halt_pass1_fail2.py`, `_halt_emitter.py` [CODE-VERIFIED]; a body "without the fix sections" drops it, so A's step-8 switch would lose the verifier's halt guards unless that section is kept, and B's NB6 (24 of 169 verifiers executed tests or `sed -i`) adds a capability loss. Plus the 93 report-only spawn markers in 8 skill files (diff X-001) and the N1 site, which both resolutions leave unchanged in the first change.

## Summary

- Findings: 18. ADDRESSED 2 (INV-005, INV-011); UNADDRESSED 16.
- By severity: HIGH 6 (INV-002, INV-009, INV-012, INV-015, INV-016, INV-017; all UNADDRESSED); MEDIUM 9 (INV-001, INV-003, INV-004, INV-007, INV-008, INV-010, INV-013, INV-014, INV-018; all UNADDRESSED); LOW 3 (INV-005 ADDRESSED, INV-006 UNADDRESSED, INV-011 ADDRESSED).
- By category: state_variables 1 (INV-001; the persistence-window state risk is carried inside INV-015); guard_conditions 5 (INV-002 to INV-006); count_divergence 2 (INV-007, INV-008); collection_boundaries 3 (INV-009 to INV-011); interaction_effects 3 (INV-012 to INV-014); sufficiency_challenge 4 (INV-015 to INV-018).
- On the three wording disputes: (1) step-8 switch: INV-018 shows the step-8 verifier protocol lives in the section the consensus drops, which supports B's "own arm" condition and adds a body condition; (2) exclusion scope: INV-005 and INV-008 (nested spawns, executing verifiers) support B's wider "every lens or verifier that runs tests or mutates scratch copies"; (3) write-probe form: INV-001 and INV-004 show a single probe, in any form, covers one harness, one permission mode and one installed copy only.
- Not verified: Claude Code's behaviour when a `subagent_type` does not resolve; whether reflect-reviewer briefs overrode the mandated first line (41 of 517 briefs mention a YAML fence or an output format); the content of the 3 non-fix nested spawns beyond their descriptions.

Status: Complete
