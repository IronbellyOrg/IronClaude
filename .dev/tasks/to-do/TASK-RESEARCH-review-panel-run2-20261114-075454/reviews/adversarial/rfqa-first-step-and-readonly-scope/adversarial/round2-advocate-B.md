# Round 2: Rebuttal of the Variant B advocate (slot C-11, rfqa-first-step-and-readonly-scope)

Advocate: B (Proposal B, `variant-2-original.md`). Round 2, second speaker. Focus: correctness, risk, test-coverage.
Read for this round: `diff-analysis.md`, `variant-1-original.md`, `variant-2-original.md`, `round1-advocate-A.md`, `round1-advocate-B.md` (mine), `round2-advocate-A.md`, row C-11 of `phase-outputs/discovery/undecidable-conflicts.md:28`. No other `round2-*` file was read.
Tags: [CODE-VERIFIED] read at the cited path:line in this session; [RUN-VERIFIED] observed by a read-only `uv run --no-project python` script in this session (scratch only under `mktemp -d /tmp/advB-r2.XXXXXXXX` directories, each removed by an exit trap); [UNVERIFIED].
Transcript rule kept: every transcript whose text contains the run-1 task id or the queued-run file name was skipped before parsing (117 rf-qa / rf-qa-qualitative transcripts skipped, the same number A reports); none is quoted or counted. The issue-331 main session transcript was checked and contains neither string.
Citation shorthand: `A:n` = `variant-1-original.md` line n; `B:n` = `variant-2-original.md` line n; `A-R1:n` = `round1-advocate-A.md` line n; `B-R1:n` = `round1-advocate-B.md` line n; `A-R2:n` = `round2-advocate-A.md` line n. `T331` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-331-github-issue-watcher/c619f49d-c032-4bb0-b1e5-6781bebedb7c` (main session `.jsonl` beside it, subagents under `subagents/`).

## Response to criticisms

### A's Round 1 weaknesses of Variant B (A-R1:37-44)

1. **"Known write path left open; M-B1 may be unrunnable; absence of logs reads as safety" (A-R1:37).** The "unrunnable" half is answered: M-B1 ran in Round 1 and again in Round 2 (278 report-only transcripts under the skip rule, 571 non-fix rf-qa / rf-qa-qualitative transcripts) [RUN-VERIFIED]. The substantive half is CONCEDED: the audit found one event that falls in my own class (b) (N1, verified below), so B-3 as stated ("the `/task` lens agents' tools and mode are not changed in the first change" with no hardening item) is refuted by B's own pre-committed rule (B:84, B-R1:70). I also accept the "absence reads as safety" point as a defect of the rule: an empty or unreadable corpus must give no verdict, not support. That fix is in my resolution, item 5.
2. **"Plan-mode agent is not the control under a bypass parent" (A-R1:38).** CONCEDED. The control is the `tools` allowlist; N5 (two out-of-allowlist calls refused across 517 reflect-reviewer runs) and my Round 1 strength 5 both show the allowlist working. B:17's "a plan-mode agent without Write, Edit or Bash" is replaced by "an agent whose `tools` list is a subset of a named read-only set".
3. **"B's first change replaces nothing and has no host" (A-R1:39).** CONCEDED (B-R1:71, B-R1:73). The document-gate module leaves the first change. What survives of B-2 is the cheap oracle input: seeded single documents with clean twins, which A-R2 adopted (A-R2:93, A-R2:122).
4. **"B's two-implementations argument applies to B" (A-R1:40).** CONCEDED as symmetric. A shadow document gate is a second implementation; so is a new read-only lens agent that coexists with `rf-qa` at every other spawn site under A's resolution. Any staged migration runs two implementations for an interval, so this argument decides nothing for either side and I withdraw it as a reason.
5. **"Schema-change claim wrong on the mechanism" (A-R1:41).** CONCEDED in Round 1 (B-R1:66).
6. **"C-03 condition 7 does not bind A's design" (A-R1:42).** CONCEDED in Round 1 (B-R1:68).
7. **"Install-cost claim contradicted by code" (A-R1:43).** CONCEDED in Round 1 (B-R1:67).
8. **"B's oracle does not test the read-only question" (A-R1:44).** CONCEDED. M-B2 compared "the existing lens gate" with "the panel gate" (B:86), which changes engine, prompt and permissions together. A's arm 0 versus arm 1a (same lens text, prose consolidation, only the agent changes) isolates read-only; I adopt it.

### A's Round 2 claims about my pilot (A-R2 "Pilot re-check", A-R2:61-78)

| A's claim | My answer |
|---|---|
| 366 not reproduced; 278 under the skip rule | ACCEPTED. Round 1 did not state a skip rule for run-1 transcripts; 278 is the count to quote. I reproduced the same 117 skipped transcripts this round [RUN-VERIFIED]. Which of my 366 were run-1 transcripts I did not re-establish. |
| Magnitudes halved by deduplication by `tool_use` id | ACCEPTED. B-R1:32 warned of duplicated records; counts below are deduplicated. |
| "0 to any other path" hides one Write plus four Edits into another lens's report | ACCEPTED and verified (N1 section): Write at 00:12:07Z plus Edits at 00:12:23, 00:12:24, 00:12:26, 00:12:51Z, all successful. My bucket "QA/report paths" did not split own report from another agent's report; that was a classification defect. |
| Bash count not reproduced; no repository-mutating Bash found | ACCEPTED. My own Round 2 screen of every `sed -i` / `perl -pi` call by non-fix agents (28 agents) found only scratch or variable targets (NB7). |
| 4 of 16 issue-331 lens agents wrote mutation harnesses: 2 confirmed, denominator 16 not reproduced | ACCEPTED as stated; I did not re-count the denominator. N1's own agent adds one more execution case (it ran seven `/tmp/gatec-probe` scripts, NB5). |
| Selection on the literal `fix_authorization: false` misses 155 lens-like transcripts | ACCEPTED. My Round 2 classification selects non-fix agents by excluding `fix_authorization: true` and fix-like descriptions, the same rule A used, and gives 571. |
| Report-only held in every observed run: CONTRADICTED | ACCEPTED. One report-only lens destroyed another lens's report on disk (N1). |

### A's new evidence N1-N6

- **N1**: VERIFIED with two corrections on cause and damage (see `## Verification of N1-N3`). It falls in my class (b). I concede B-3.
- **N2**: VERIFIED (zero first prompts use the step-3/4 path pattern with a standard lens name). My regex counts 107 standard-lens-named transcripts against A's 118; same shape.
- **N3**: VERIFIED in shape (571 / 437 / 28 / 15 match exactly; pytest 77 against A's 74; standard-lens subset pytest 2, `sed -i` 1, `/tmp` writes 0).
- **N4**: VERIFIED. `src/superclaude/agents/rf-qa.md:20-24` lists Agent, Task, TaskOutput, TaskStop, SendMessage; `tests/cli/reflect/test_reviewer_readonly_tools.py:30` is `_MUTATORS = frozenset({"Bash", "Edit", "Write", "NotebookEdit", "Task"})` [CODE-VERIFIED]. The guard must treat Agent, TaskOutput, TaskStop and SendMessage as mutators too.
- **N5**: not re-run by me this round; it matches my Round 1 strength 5 (B-R1:36), so I accept it.
- **N6**: not verified by me (`cli/reflect/models.py`, `runner.py` not opened this round) [UNVERIFIED]. It is only named as an open path, so it moves no decision.

## Updated assessment of Variant A

What A's Round 2 now gets right:
- N1 is real and is the first observed failure of the "report-only by prompt" convention with on-disk damage; it fires B's own class-(b) rule, so a hardening item belongs in the first change.
- No gate engine belongs in the first change (A-R2:119). A's withdrawal of the per-slot `lens` key, the checklist completion predicate and the floor parameter (A-R2:91-92, A-R2:99) removes every point where A went past C-01/C-03.
- Q3 goes to the owner (A-R2:19, A-R2:124), as the C-11 row requires ("whether the lens agents are made read-only in the first change (Q3) ... are owner decisions", `undecidable-conflicts.md:28`) [CODE-VERIFIED].
- The arm 0 versus arm 1a oracle isolates the read-only effect; the guard must be a subset test, not a denylist.
- The split of Half 1 by lens kind (standard lenses rarely execute; other lenses do) is supported by the corpus.

What remains wrong or unproven:
1. **A's resolution does not reach the only observed class-(b) event.** N1 occurred at task-file gate items 7.G2-7.G7 of a task-builder-built task, at a non-standard lens (security-invariants). A's item 7 switches only `/task` steps 3-4 and the step-8 pair, and A's item 8 puts "domain and skill-embedded lens spawn sites" out of the first change (A-R2:125-126). A's own N2 says no observed spawn used steps 3-4 with a standard lens. So the one gate edit in A's resolution reaches zero observed spawns and none of the observed failure. The agent definition and the oracle are still worth shipping; the claim that the switch "cures" N1 is not supported.
2. **Executor persistence alone turns N1 from a detected loss into a silent coverage gap.** In the real run the orchestrator noticed because the security-invariants report was missing (NB3). If the executor writes each returned text to the dispatched slot's path, a misdirected reviewer's design-correctness review lands at the security-invariants path, step 10's existence check passes, and the gate silently has no security-invariants coverage. A's A-003 fix (path keyed by slot plus sha256) gives uniqueness and fidelity but not identity. A lens-identity check (the report states its lens; a mismatch with the dispatched lens is a blocker) is needed.
3. **The step-8 verification pair executes.** 24 of 169 non-fix verifier transcripts ran pytest or `sed -i` on scratch copies (NB6). A's item 7 switches the verification pair to the read-only agent on the strength of arm 1a, which measures lens reviewers on seeded documents, not verifiers checking that fixes landed.
4. **N1's damage is overstated and its cause is partly the agent.** The first report was restored byte for byte from the first agent's transcript (00:17:41-44Z); the on-disk window was 00:12:07Z to 00:17:44Z. A says "two blocking findings were lost" (A-R2:34); the record shows 3 blocking replaced by 1, and whether the stray's one blocking finding (deadline exit code, `origin_mismatch` instead of `budget_exhausted`) is the same defect as the first report's C-3 ("wrong exit code and reason under a specified con...") I could not settle. The cause: the dispatch named "Step 7.G7 (task file lines 546-547)"; the agent printed lines 540-550, which hold items 7.G5, 7.G6 and 7.G7, and took the first paragraph (NB1). Both the delegation-by-line-reference prompt and the agent's misreading contributed; the damage mechanism (Write plus a shared folder) is as A says.
5. **A's deterministic no-model arm has nothing to exercise once no engine is wired.** A-R2:122 keeps "a deterministic no-model arm"; with no `resolve`/`merge`/`ledger` in the first change and executor persistence written in prose, the only code to test deterministically is the oracle's scoring script. The arm should be named as that.
6. **A's runtime write-probe "in a `tmp_path` repository" (A-R2:121) cannot be a pytest.** A pytest cannot spawn a Claude Code subagent; the probe is a recorded one-time run with its transcript kept, and the static guard is the regression test.

## New evidence

NB1. **Cause of N1: delegation by line reference into a window holding three lens prompts** [RUN-VERIFIED]. `T331/subagents/agent-abed84d24b847251c.jsonl`: first prompt "fix_authorization: false (report-only). Your complete instructions are the quoted prompt inside the item under "**Step 7.G7:**" (task file lines 546-547) ... Modify no file except your report." First tool call (00:00:02Z) `sed -n '540,550p'` of the task file; its result contains `**Step 7.G5:**` (lens "design-correctness", "Write the report to `.../qa/gate-c/qa-content-design-correctness-report.md`"), `**Step 7.G6:**` (test-adequacy) and `**Step 7.G7:**` (security-invariants). The agent's final message reports the design-correctness path, "FAIL, blocking: 1".

NB2. **N1 is outside every spawn site A's resolution changes** [RUN-VERIFIED for the site; CODE-VERIFIED for the rule]. The spawning items are task-file checklist items (Gate C, "lens agent 4/5/6 (part of the parallel batch of Step 7.G2)"), i.e. gate items written by the skill that built the task. `/task` step 5 spawns such prompts "exactly as written" (`src/superclaude/skills/task/SKILL.md:250`) and step 6 says "Each step below becomes its own `- [ ]` checklist item when encoded in a task file" (`task/SKILL.md:252`) [CODE-VERIFIED]. The orchestrator's actual cure was at the dispatch prompt: the re-spawn (`agent-ad808ee6d7eb36624.jsonl`, 00:17:48Z) names the lens, says "do NOT rely on line numbers", names "Your ONLY output file" and lists the files it must never write.

NB3. **How N1 was detected** [RUN-VERIFIED]. The main session waited for `-s $Q/qa-content-security-invariants-report.md` (00:12:46Z), found 5 files instead of 6 (00:17:16Z), listed `qa/gate-c` with timestamps (00:17:22Z), then copied the stray to `-run2.md`, restored the original (00:17:41-44Z) and re-spawned the lens. Detection relied on the missing file, which executor persistence keyed by slot would not leave missing (consequence is inference).

NB4. **Content restored; damage window about 5.6 minutes** [RUN-VERIFIED]. First report written 00:07:51Z (`agent-a00026ccf75eb50ac.jsonl`, final "FAIL, 3 blocking findings (C-1 to C-3), 9 minor notes"); overwritten 00:12:07Z; restored 00:17:44Z ("restored 15855", 96 lines, verdict FAIL with C-1..C-3). The overwritten path was in the worktree and untracked at the time (`?? .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/gate-c/` in the agent's own `git status` at 00:12:55Z).

NB5. **The misdirected lens is an executing lens** [RUN-VERIFIED]. Between 00:06:36Z and 00:10:05Z the same agent wrote and ran `/tmp/gatec-probe/probe1.py` .. `probe7.py` against the package code and removed them at 00:12:55Z (`rm -rf /tmp/gatec-probe /tmp/gatec-*`). A read-only switch at that spawn site would remove the capability the lens used, so N1's site cannot be cured by the read-only agent without the capability question of A-004.

NB6. **Verifiers execute about as often as non-standard lenses** [RUN-VERIFIED, coarse regex]. Non-fix rf-qa / rf-qa-qualitative transcripts whose description contains "verif": 169, of which 24 ran pytest or `sed -i`/`perl -pi`; all other non-fix: 402, of which 58 did. Standard-lens-named subset: 107, of which about 3 did.

NB7. **Every `sed -i` by a non-fix agent targeted a scratch or variable path** [RUN-VERIFIED screen]. 28 agents; targets such as `$W/m/src/...`, `$M/m2/$S`, `$D/m2/src/...`, `$d/tree/tests/...`, `"$(C M2)"`, `$F`. Executing lenses include non-domain-named skill lenses (sc:sweep QA: command-contract, skill-contract, primitive-path, read-only-claims) and verifiers, not only test-adequacy and security-invariants. Variables were not resolved; classification is by pattern.

NB8. **The cap rows for `task/SKILL.md` do not touch steps 3, 4, 8 or 10** [CODE-VERIFIED]. Rows C-105..C-113 (`tests/skills/fixtures/review_severity_cap_edits.yaml:871-943`) pin cap and at-cap sentences (fixture lines 120, 254, 336, 366, 368, 405, 477, 616 of an older revision; C-107's text is now at `task/SKILL.md:258`). The spawn text of steps 3-4 (`task/SKILL.md:225, 241`), step 8 (`:256`) and step 10 (`:260`) carries no cap row, so a conditional edit of those steps meets only the "no minimum count" pin (`:233`) and the worker-contract paragraph.

## Verification of N1-N3

Method: four read-only scripts over `/home/coder/.claude/projects/**/subagents/*.meta.json` and the sibling `.jsonl` files, plus the issue-331 main session `.jsonl`; tool calls deduplicated by `tool_use` id; results matched by `tool_use_id`; forbidden transcripts skipped before parsing; scratch in `mktemp -d /tmp/advB-r2.XXXXXXXX`, removed on exit.

**N1: VERIFIED, with corrections.**

| Question | Finding |
|---|---|
| Did the overwrite happen? | Yes. `agent-a00026ccf75eb50ac` (rf-qa-qualitative, "Gate C lens design-correctness") created `qa/gate-c/qa-content-design-correctness-report.md` at 00:07:51Z ("File created successfully"). `agent-abed84d24b847251c` (rf-qa-qualitative, "Gate C lens security-invariants", prompt "Modify no file except your report") ran Write on that path at 00:12:07Z (result "The file ... has been updated") and four successful Edits to 00:12:51Z. It never Read the file before the Write. Across the whole corpus, this is the only path written successfully by two distinct non-fix agents [RUN-VERIFIED]. |
| Was content lost? | Temporarily, on disk only. The first report (3 blocking, C-1..C-3) was replaced by a report with 1 blocking for about 5.6 minutes and restored byte for byte from the first agent's transcript by the orchestrator (00:17:41-44Z); the stray was kept as `-run2.md`; the security-invariants lens was re-run (`agent-ad808ee6d7eb36624`, PASS with notes, 0 blocking). Without the manual restore the gate would have consolidated 1 blocking finding in place of 3. "Two lost" (A-R2:34) assumes the stray's single finding duplicates one of the three; I could not confirm that. |
| Cause | Partly the dispatch (instructions by line reference, "lines 546-547"), partly the agent (it printed lines 540-550 holding three lens prompts and followed the first). The damage mechanism is Write access plus self-persistence into a shared `qa/gate-c/` folder. |
| Does it fall in B's class (b)? | Yes. Class (b) is "any repository working-tree path other than the own report" (B-R1:70). The path is inside the worktree (untracked at the time, NB4) and is another lens's report. B-3 as stated is refuted, and B's pre-commitment (B:84, B:105) moves "an agent-definition split only, without the panel" into the first change. |
| Spawn site | Task-file gate items written by task-builder (NB2), not `/task` steps 3-4. |

**N2: VERIFIED.** First prompts that contain `qa-(structural|content)-` followed by a standard lens name: 0 [RUN-VERIFIED]. Standard-lens-named descriptions: 107 by my regex (A: 118; regex difference).

**N3: VERIFIED in shape.**

| Measure | A (A-R2:53) | B re-check |
|---|---|---|
| Non-fix transcripts | 571 | 571 |
| With any Bash | 437 | 437 |
| pytest | 74 | 77 |
| `sed -i` / `perl -pi` | 28 | 28 |
| Write/Edit under `/tmp` | 15 | 15 |
| Standard-lens-named: n / Bash / pytest / `sed -i` / `/tmp` writes | 118 / 86 / 1 / 1 / n.a. | 107 / 79 / 2 / 1 / 0 |

Not re-checked: A's "simple reads only" sub-counts (50 and 18).

## Final position table

| ID | Final | Evidence (one sentence) |
|---|---|---|
| S-001 | HYBRID (same as A-R2): consistency check against C-01/C-02/C-03 first (A's order) plus a separate "what was not verified" section (B) | Neither order changes a claim; the separate list keeps unverified items findable. |
| S-002 | B | The separate falsifiers of B-1..B-3 are what let this round keep B-1/B-2's "no engine swap" while refuting B-3 alone. |
| S-003 | HYBRID (same as A-R2): B's clause-keyed evidence with A's claim/evidence/tag table inside each clause | The table is auditable line by line; clause keying ties each item to a decision. |
| S-004 | B | The synth-06 ids INV-A..INV-N are the ids the C-11 row uses (`undecidable-conflicts.md:28`). |
| S-005 | HYBRID (same as A-R2): A's ordered pipeline with each step labelled with the clause it decides | Both advocates proposed this merge in Round 1. |
| C-001 | HYBRID (same as A-R2): the first change is lens-level (one read-only lens agent definition plus a single-document seeded replay), wires no panel engine into any rf-qa gate, and its only gate edit is the conditional standard-lens switch at `/task` steps 3-4 | N1 refutes "no hardening" while N2 and the one-candidate merge (`ledger.py:107`) rule out a `/task` engine start. |
| C-002 | HYBRID, differs from A-R2: the standard eight lens dimensions at `/task` steps 3-4 switch to the read-only agent only if arm 1a passes and the owner answers Q3 yes, with executor persistence that checks the report's lens line against the dispatched lens; the step-8 verification pair, non-standard lenses and skill or task-file gate items keep their agent | N1 fires class (b), but 24 of 169 verifiers and the N1 lens itself executed code (NB5, NB6), and persistence without an identity check would hide N1's failure (NB3). |
| C-003 | B | The lens travels as free text in the brief (`reflect-reviewer.md:56`); A withdrew the slot key (A-R2:91). |
| C-004 | B | The computed confidence gate stays in the agent body (`rf-qa.md:484-534`); A withdrew the completion predicate (A-R2:92). |
| C-005 | HYBRID, amends A-R2: seeded single documents with clean twins run through arm 0 and arm 1a per standard lens dimension with A's tree-hash, UNVERIFIABLE-share and pre-registered repeat count; the deterministic no-model arm is a pytest of the oracle's scoring script on frozen reports; a verification-pair arm is added only if the pair is to switch | No engine is wired, so the scorer is the only deterministic code (Updated assessment, point 5). |
| C-006 | HYBRID, amends A-R2: Half 1 is separable from Half 2 and limited to the standard eight lenses at steps 3-4; the step-8 pair is excluded unless its own arm passes; Half 2 is not in the first change | X-003 and N3 split Half 1; NB6 shows verifiers execute. |
| C-007 | HYBRID (same as A-R2): no engine swap at any gate in the first change; the only gate edit is the conditional standard-lens switch, guarded by arm 1a and the unedited pinned suites | The gate is mandatory after every phase (`task/SKILL.md:192, 286`). |
| C-008 | HYBRID, differs from A-R2: `task/SKILL.md` stays byte-identical unless the standard-lens switch lands; then only steps 3, 4 and 10 change (step 8 only with a passed verification arm) and the three pinned suites pass with no test edited | NB8: no cap row sits in steps 3, 4, 8 or 10, so the pins that matter are "no minimum count" (`:233`) and the worker-contract paragraph. |
| C-009 | HYBRID (same as A-R2): any later `/task` Half 2 is limited to document outputs, and M-B4 runs before it is widened | Both rest on the one-candidate merge (`merge_cmd.py` `--doc`, `ledger.py:107`). |
| C-010 | HYBRID, amends A-R2: full M-B1 audit before merge, deduplicated, counted per spawn source, with "another agent's report" and "a report whose lens differs from its dispatch" in class (b), an empty corpus giving no verdict, and N1 recorded with its cause; the tree-hash check on every replay | N1 was found by the audit and is invisible to a reviewed-tree hash; NB1 shows the cause must be recorded to choose the cure. |
| C-011 | B | No panel at any gate in the first change, so the prose floors (`task/SKILL.md:196-201`) stay and C-03 INV-003 is not forced. |
| C-012 | HYBRID (same as A-R2): the first change gives PR review the read-only reviewer definition and the replay fixture; per-slot lens and checklist mode wait | M4 and M9 left the first change with C-003 and C-004. |
| X-001 | B | `task/SKILL.md:250` spawns embedded lenses "exactly as written"; N2 and NB2 show lens traffic and the one failure at skill and task-file items. |
| X-002 | A | `_SLOT_KEYS` (`panel.py:46`) is an accept-list and `template_sha256` hashes the template object. |
| X-003 | B | Half 1 rewrites persistence and step 10 (`task/SKILL.md:238, 260`), with no panel code. |
| X-004 | B | The spawn `mode` is ignored; the allowlist is the control (N5). |
| X-005 | HYBRID (same as A-R2): B's statement holds for the whole gate, A's for Half 2 limited to document outputs | Both rest on the one-document merge. |
| X-006 | A | A's confidence is per reviewer (`rf-qa.md:505`); conceded in B-R1:68. |
| X-007 | B | 8 packaged templates (default, live7, six reflect). |
| A-001 | HYBRID, amends A-R2: rely on the `tools` allowlist, not `permissionMode`; record one runtime write-probe run (transcript kept in the task package, not a pytest) and keep the tree-hash check on every replay | A pytest cannot spawn a subagent; N5 shows refusals in practice. |
| A-002 | HYBRID, amends A-R2: the guard asserts the allowlist is a subset of a named read-only set, with Agent, Task, TaskOutput, TaskStop, SendMessage, Bash, Write, Edit, MultiEdit and NotebookEdit as mutators | `rf-qa.md:20-24` grants the task and message tools; `_MUTATORS` (`test_reviewer_readonly_tools.py:30`) omits Agent and SendMessage. |
| A-003 | HYBRID, amends A-R2: the executor persists each returned report unedited to the dispatched slot's path, records its sha256, and rejects as a blocker a report whose first line names a lens other than the dispatched one | Slot-keyed paths stop N1's overwrite but, without an identity check, hide N1's mis-dispatch (NB3). |
| A-004 | HYBRID, amends A-R2: the new agent's body is rf-qa's verification, zero-trust and Confidence Gate sections without the fix sections, standard lenses get pre-computed counts where they used Bash, and every lens or verifier that runs tests or mutates scratch copies is excluded from the switch | N3, NB5, NB6, NB7. |
| A-005 | HYBRID (same as A-R2): pre-register a repeat count per arm and a variance bound before the first model run | Neither variant states one. |
| A-006 | A | `_assert_present` (`test_cli_install.py:502-506`) fails only on a missing listed name. |

Tally: A 3 (X-002, X-006, A-006); B 9 (S-002, S-004, C-003, C-004, C-011, X-001, X-003, X-004, X-007); HYBRID 18 (S-001, S-003, S-005, C-001, C-002, C-005, C-006, C-007, C-008, C-009, C-010, C-012, X-005, A-001, A-002, A-003, A-004, A-005); NEITHER 0. Total 30. The outcome labels match A-R2 on all 30 points; the hybrid text differs on C-002, C-005, C-006, C-008, C-010, A-001, A-002, A-003 and A-004.

## Response to A's proposed resolution

1. **ACCEPT.** Lens-level first change, no engine; B's document gate and A's Half 2 are later steps.
2. **AMEND.** Replace with: "The new agent's `tools` list is exactly Read, Grep, Glob and the read-only search and codegraph tools of `reflect-reviewer.md:5`; its body is `rf-qa.md`'s verification, zero-trust and Confidence Gate sections without the fix sections; any S1-S3 severity or cap text it restates is copied verbatim (`test_c_s1_s3_copied_verbatim`); its report's first line states the dispatched lens and report slot; it names other primitives by installed path; `make sync-dev` and `make verify-sync` run." Reason: the verbatim pin applies to any new primitive that restates the rule (B:71), and the lens line is what the A-003 identity check reads.
3. **AMEND.** Replace with: "A new guard test asserts the agent's allowlist is a subset of a named read-only set (Agent, Task, TaskOutput, TaskStop, SendMessage, Bash, Write, Edit, MultiEdit, NotebookEdit are mutators), with a negative fixture; one runtime write-probe run (a Write attempt in a scratch repository) is recorded once with its transcript kept in the task package; it is not part of `uv run pytest`." Reason: A pytest cannot spawn a Claude Code subagent; TaskOutput and TaskStop are on `rf-qa.md:22-23`.
4. **AMEND.** Replace "with a deterministic no-model arm" by "with a deterministic pytest of the oracle's scoring script on frozen reports (a seeded defect matched in a blocking row; no blocker on a clean twin)", and add: "a verification-pair arm (fixed document, applied fix, the pair asked to confirm it) runs only if item 7 is to switch step 8." Reason: no engine code exists to replay; verifiers execute (NB6).
5. **AMEND.** Replace with: "The full M-B1 audit runs before merge, deduplicated by `tool_use` id, skipping run-1 transcripts, and counted per spawn source (`/task` steps 3-4, task-file gate items, skill gates); own report or `/tmp` scratch = neutral; another agent's report, a report whose lens differs from its dispatched lens, or any other repository working-tree path = class (b); a git state change in the reviewed repository = class (c); a class-(b) or class-(c) event refutes leaving the agents as they are; an empty or unreadable corpus gives no verdict. The issue-331 Gate C overwrite is recorded as the first class-(b) event with its cause (dispatch by line reference into a window holding three lens prompts)." Reason: NB1, NB2, and A-R1:37's valid point that absence must not read as safety.
6. **AMEND.** Append: "The owner is also told that the only class-(b) event occurred at a task-file gate item of a non-standard lens that item 7 does not reach, and that no standard-lens spawn through `/task` steps 3-4 was observed." Reason: NB2 and N2; the owner's answer should rest on where the exposure was seen.
7. **AMEND.** Replace with: "If arm 1a meets the registered rule for a standard lens dimension before merge and the owner says yes, the first change switches that dimension at `/task` steps 3-4 to the new agent, persists each returned report unedited to the dispatched slot's path with its sha256, treats a report whose first line names another lens as a blocker, and rewrites step 10 to check the executor-persisted files, their hashes and their lens lines; the step-8 verification pair switches only if the verification-pair arm of item 4 passes; otherwise `task/SKILL.md` stays byte-identical." Reason: NB3 (identity), NB6 (verifiers execute).
8. **ACCEPT**, with the wording "skill-embedded and task-file gate items" in place of "domain and skill-embedded lens spawn sites", so the exclusion names where N1 occurred.
9. **ACCEPT.** The scope check and the unedited suites are B's M-B3.
10. **AMEND.** Replace with: "Open condition, executing reviewers: every lens or verifier that runs tests or mutates scratch copies keeps its agent until a read-only path (pre-computed evidence, or an isolated execution snapshot, suitability [UNVERIFIED]) is measured against arm 0; skill-embedded and task-file gate items, where N1 occurred, get in a separate change a no-clobber check (sha256 of each lens report recorded when its owner returns and re-checked at consolidation; a mismatch is a blocker) and dispatch prompts that name the lens and report path explicitly instead of by line reference." Reason: NB5-NB7 widen "domain lenses"; the no-clobber check and explicit dispatch cure N1's mechanism at its own site without removing capability, as the orchestrator's re-spawn did (NB2).
11. **ACCEPT.**
12. **ACCEPT.**

## Proposed resolution

1. The first rf-qa change is lens-level: one new read-only lens-reviewer agent definition and a replay oracle; no panel engine (`resolve`/`merge`/`ledger`) is wired into any rf-qa gate; B's document-gate module and A's `/task` Half 2 are later steps.
2. The agent's `tools` list is exactly Read, Grep, Glob and the read-only search and codegraph tools of `reflect-reviewer.md:5`; its body is `rf-qa.md`'s verification, zero-trust and Confidence Gate sections without the fix sections, copies any S1-S3 severity or cap text verbatim, and makes the report's first line state the dispatched lens and slot; it names primitives by installed path; `make sync-dev` and `make verify-sync` run.
3. A guard test asserts the allowlist is a subset of a named read-only set (Agent, Task, TaskOutput, TaskStop, SendMessage, Bash, Write, Edit, MultiEdit, NotebookEdit are mutators) with a negative fixture; one runtime write-probe run is recorded once with its transcript kept in the task package.
4. Before any gate text changes, the oracle runs seeded single documents with clean twins through arm 0 (current lens agents) and arm 1a (new agent, same lens text, prose consolidation) per standard lens dimension, with a pytest of the scoring script on frozen reports, a pre-registered repeat count, variance bound and decision rule, and metrics: per-lens recall in a blocking row, wrong blockers on clean twins, UNVERIFIABLE share, tree-hash no-mutation, tokens, wall-clock; a verification-pair arm runs only if step 8 is to switch.
5. The full M-B1 audit runs before merge (deduplicated by `tool_use` id, run-1 transcripts skipped, counted per spawn source); own report or `/tmp` scratch is neutral; another agent's report, a report whose lens differs from its dispatch, or any other working-tree path is class (b); a git state change is class (c); (b) or (c) refutes leaving the agents unchanged; an empty corpus gives no verdict; the issue-331 Gate C overwrite is recorded as the first class-(b) event with its cause.
6. Owner question Q3 goes to the owner with items 4-5's evidence, including that the only class-(b) event was at a task-file gate item of a non-standard lens and that no standard-lens spawn through `/task` steps 3-4 was observed; the recommendation is yes for the standard eight lens dimensions.
7. If arm 1a passes for a standard dimension and the owner says yes, `/task` steps 3-4 switch that dimension to the new agent; the executor writes each returned report unedited to the dispatched slot's path with its sha256, a report naming another lens is a blocker, and step 10 checks files, hashes and lens lines; step 8 switches only if the verification-pair arm passes; otherwise `task/SKILL.md` stays byte-identical.
8. Out of the first change: per-slot `lens` key, checklist completion predicate, any `/task` panel template, floor parameter, skill-embedded and task-file gate items, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, the ten S1-S3 files, `pr_submit`, `cli/reflect`.
9. Scope check: `git diff --stat` names only the new agent file, its tests, the oracle script and tests, and (only under item 7) `task/SKILL.md`; `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_prompt_overrides.py tests/skills/test_worker_contract.py tests/review -q` passes with no test edited.
10. Open, executing reviewers: lenses and verifiers that run tests or mutate scratch copies keep their agent until a read-only path is measured against arm 0; skill-embedded and task-file gates get, in a separate change, a no-clobber check (each report's sha256 recorded when its owner returns and re-checked at consolidation; a mismatch is a blocker) and dispatch prompts that name lens and report path explicitly, not by line reference.
11. Open, engine: any gate engine swap waits for the M-B4 anchor probe (C-01 T-a), the C-03 floor-owner answer and C-02's `next`/`--resolution` caller rules, and runs in shadow with rf-qa as authority until a replay says otherwise.
12. Open, evidence quality: the transcript audit covers one machine and unknown retention, the N1 damage count (2 or 3 blocking findings) is unsettled, and the "eight lens" set meant by Q5 stays an owner decision.

Status: Complete
