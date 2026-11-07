# Round 2 - Advocate for Variant 3 (reviewer-3, refactorer, opus): rebuttal (last in sequence)

Paths are relative to the repo root. "plan:N" is line N of `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md`; "src:N" is `source.md` in the same folder; "spec:N" is `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; "SKILL.md" is `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`; "routing" is its `refs/handoff-routing.md`; "cmd" is `src/superclaude/commands/brainstorm.md`; "lc10" is `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc10-result.md`. Every file:line below was Read (or run, read-only) this round.

## Response to criticisms

Every criticism of V3 made by Advocate 1 (A1) and Advocate 2 (A2) in Rounds 1 and 2.

| # | Criticism | From | Answer |
|---|---|---|---|
| 1 | R3-1's remedy ("decide by the `source` field of `enrichment_used`") cannot work: `source` is only `codebase \| research-light \| research-deep` | A1 R1, A1 R2, A2 R2 | **CONCEDE, plainly: they are right.** SKILL.md:371-373 reads `enrichment_used: - source: codebase \| research-light \| research-deep` / `quality_tier: primary \| fallback_1 \| skipped`. `analyze` is not a legal value. `/sc:analyze` and auggie both record `source: codebase`, and a clean run of either records `primary` (SKILL.md:187,198). No field of the stable contract (SKILL.md:360-377) names the tool. The remedy in my card would have installed a second checker rule with nothing to read, which is the failure class this plan exists to remove. The diagnosis (decide by which tool ran, not by tier) stands; the mechanism I named is wrong. |
| 2 | R3-1 was tagged Grounded although its remedy is refuted by the file it cites | A1 R1, A1 R2, A2 R2 | CONCEDE for the remedy. The premise (SKILL.md:187,198 against plan:81) is Grounded; the prescribed test was asserted without reading four lines that were 170 lines below the ones I cited. S-002 moves to none. |
| 3 | V3's Round 1 weakness 5 said "`source` values are not enumerated anywhere I read" and still did not check them | A2 R2 | CONCEDE. That sentence was false; they are at SKILL.md:372. I flagged the doubt and did not resolve it with one Read. |
| 4 | R3-2 (Task 7 skips `test_codegraph_adoption.py`) is over-rated at P1 | A1 R1, A2 R1, A1 R2, A2 R2 | CONCEDE (already in my Round 1). Re-read: the Tier 2 slice test (`tests/skills/test_codegraph_adoption.py:75-82`) asserts only `codegraph_files`, `codegraph_search` and `Glob for files matching topic keywords`; the other brainstorm checks read the `mcp-servers:` line (`:131`) and the absence of `mcp__serena` (`:143`). A bullet added inside routing lines 25-31 keeps all of them. P2: a coverage gap against src:7, not a missed break. |
| 5 | R3-8 misreads plan:21: the plan says no test requires the src and plugin copies to *match*, not that no test reads the plugin copy | A1 R1, A1 R2, A2 R2 | CONCEDE. plan:21: "no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill)". `test_codegraph_adoption.py:23,39,121` reads the plugin `brainstorm.md` only for its own `mcp-servers:` line and the serena scan, each file on its own; nothing compares the two. R3-8 attacked a claim the plan did not make. I withdraw it. |
| 6 | R3-6's shared phrase "no nested directory" would weaken the pin | A1 R1 | REBUT; A1 retracted this in Round 2 (C-012 row). `no nested directory` is a substring of both `write no nested directory` and `writes no nested directory` and keeps the negation. Still Low. |
| 7 | V3 missed C-001 (Task 7 bullet 3 cannot pass) | A1 R1, A2 R1, A1 R2, A2 R2 | CONCEDE. Re-run today: `git status --porcelain` gives 950 `A `, 3 `R `, 4 `??`; `git ls-files` on this plan's package prints 0. The first clause of plan:98 fails on any reading; "plus this package" describes an untracked package. It is the first criterion that halts execution, and V3 said nothing. |
| 8 | V3 missed C-009 and C-010 | A2 R1, A1 R2 | CONCEDE. routing:30 is `quality_tier`, routing:31 is the Activation bullet, so the Tier 2 list does not end with its `quality_tier` line (plan:39). |
| 9 | R3-5 "wrong spot" overstates; 2.1 is defensible | A1 R1 | PARTIAL. spec:376 maps the 2.1 rule to AC-2.1, so the general sentence belongs in 2.1. The brainstorm live-check sentence is per-command material; spec 7.2 (spec:281-304) and 7.3 (spec:306-327) define no per-command extras, so src:9's second branch ("a note in the P1 section") applies. Both A1 and A2 moved to split; I move to split too. |
| 10 | R3-9 is INFERRED drift speculation about a clause the plan carries elsewhere | A2 R1 | PARTIAL REBUT, with new support from A2 R2. The drift risk is real but runs the other way from my card: plan:30's new clause "a nested contract is listed in `artifacts` only for a nested command that ran" is ambiguous for a failed `/sc:analyze` call (A2 R2), while cmd:157's unconditional "the nested contracts are listed in `artifacts`" is the correct reading under WC-4. The two files can disagree on exactly that clause. Kept as Low, reframed (see Proposed wording). |
| 11 | X-001: V3's "stays untested" was vague | A2 R1 | REBUT; A1 R2 and A2 R2 now both use V3's phrasing. plan:33 scopes Task 1 to the SKILL.md:195 paragraph, which lacks `fallback_1`; SKILL.md:199 is in Wave 2A, so only Task 4's section-wide assertion is vacuous. |
| 12 | My Round 1 claim that V1's "auggie primary" one-word fix was "the smaller fix ... either is acceptable" | self (adversarial duty) | WITHDRAW. Restoring "auggie" fixes the `primary` half only. The `fallback_1` half of plan:81 ("a `primary` or `fallback_1` scan ... with no nested folder") is false at run level when `/sc:analyze` was tried first and failed (New evidence 1). Neither one-word fix is acceptable. |

## Updated assessment

**Variant 1.** Steelman: V1's Round 2 is the most useful statement before this one. It found the `source` refutation, the analyze-failed refinement, and the only remedy that names a record which can tell analyze from auggie (the session file, spec:291-302). Its before/after remedies for C-001 and C-008 survive a changing tree. Critique: (a) its replacement sentence contradicts itself in the analyze-failed case, as A2 showed: both "`/sc:analyze` was invoked, the folder exists" and "the scan ran through codegraph, Glob and Grep, no nested analyze folder is expected" fire on the same run. (b) It is not checkable from the worker's output folder; it needs the session file for every run, including the common auggie and fallback runs where the folder answer is already visible. (c) It reads the session file as one file. Wave 2A runs its enrichment "in parallel via `Task` agents" (SKILL.md:183), and spec 7.2 step 5 puts each subagent's calls in its own file under `subagents/` (spec:292). lc10's analysis lists "two top-level Skill calls" (lc10:13); a top-level-only search would miss an `/sc:analyze` call made inside a Task agent and pass a run whose nested folder is missing.

**Variant 2.** Steelman: V2's Round 2 grounded the analyze-failed case in WC-4 (spec:72, contract "written on success, failure, blocked and partial outcomes") and gave the cheapest Tasks 1-3 patch: say "invoked", including a failed attempt. It also retracted its endorsement of my broken remedy without hedging. I confirm its WC-4 chain from the analyze side: cmd `analyze.md:98` says "`<report-dir>/return-contract.yaml` is written on every outcome ... failed otherwise". Critique: its clause-2 carve-out ("when `/sc:analyze` was not invoked") still leaves the check dependent on the session file for every run; and "the folder exists when invoked" has one narrow exception it did not state: `analyze.md:97` refuses a report directory "that cannot be created or written" and prints in chat only, so an invoked analyze can leave no folder. That edge is rare (brainstorm builds the path, and `<n>` is never reused, cmd:157) but a pass/fail sentence must not claim more than WC-4 gives.

**Variant 3 (own card).** The diagnosis in R3-1 survives every round: plan:81 decides the folder by tier, and tier does not determine the folder. Everything I prescribed for it was wrong (the `source` field) or insufficient (the "auggie" qualifier). V3's other durable contributions are C-002/X-001 phrasing, C-011 and C-012. Its misses (C-001, C-009, C-010) and its two misfires (R3-2's P1, R3-8) stand.

**My Round 1 P1 claims:**

| Claim | Decision | Why |
|---|---|---|
| R3-1 diagnosis: plan:81 fails a correct `/sc:analyze` run because analyze is also `primary` | KEEP at P1, and widen | SKILL.md:187,198 against plan:81. Widened: the same sentence also fails a correct analyze-failed-then-`fallback_1` run (New evidence 1), so both tiers in it are wrong, not only `primary`. |
| R3-1 remedy: decide by `source` | WITHDRAW | SKILL.md:372 (criticism 1). |
| Round 1 strength 2: the dropped "auggie" qualifier is Drift | DOWNGRADE | Dropping the word is still unauthorized loss of a brief constraint, but restoring it does not make the sentence true. The correct fix must knowingly depart from src:9's own sketch ("a fallback_1 or auggie primary scan is recorded as the tier used with no nested folder"), and the plan should record that departure as a Necessary deviation so a reviewer does not read it as drift. |
| R3-2: missing `test_codegraph_adoption.py` run is P1 | DOWNGRADE to P2 | test_codegraph_adoption.py:75-82,131,143 (criticism 4). |

## New evidence

1. **A `fallback_1` run can legitimately hold a nested analyze folder, and the planned "no folder" wording is false at run level.** SKILL.md:187 offers `/sc:analyze` OR auggie for the codebase row; SKILL.md:195 says the analyze call carries `--report-dir <report-dir>/nested/analyze-<n>/`; SKILL.md:199 defines `fallback_1` as "primary failed, used codegraph and native Glob/Grep"; `analyze.md:98` writes the contract "on every outcome", failed included. So: analyze tried, failed, codegraph/Grep used, `enrichment_used` = `{source: codebase, quality_tier: fallback_1}`, and `nested/analyze-1/return-contract.yaml` exists. The run-level table is:

   | What happened | `quality_tier` | `nested/analyze-<n>/` |
   |---|---|---|
   | `/sc:analyze` ran cleanly | `primary` | present |
   | auggie ran cleanly | `primary` | absent |
   | `/sc:analyze` tried, failed, codegraph/Grep used | `fallback_1` | present (failed contract) |
   | auggie tried, failed, codegraph/Grep used (lc10) | `fallback_1` | absent |
   | not invoked | `skipped` | absent |

   Both `primary` and `fallback_1` map to present and absent. No tier rule can be right. The routing ref does not show this because its Tier 1 is auggie only (routing:16) and Tier 2 activates "if Tier 1 returns error OR empty result" (routing:31); `/sc:analyze` appears only in the skill's matrix.

2. **The folder-based check is complete from the output folder in one direction.** In every row above, a present folder holds its own contract and the skill lists it in `artifacts` (SKILL.md:195 today; WC-4 nested rule spec:62). So "every `nested/analyze-<n>/` that exists holds `return-contract.yaml` and is listed in `artifacts`, and every listed one exists" is true for every correct run and needs nothing outside the report directory. What the folder cannot show is a missing folder after an invocation; only the session files can.

3. **The session-file converse must include subagent files.** SKILL.md:183 ("apply in parallel via `Task` agents") plus spec:292 (subagent files under `~/.claude/projects/<dir>/<session id>/subagents/`). lc10:13 recorded only top-level Skill calls ("both with sidechain False"). A live plan that copies lc10's method would not see an analyze call made inside a Task agent. (INFERRED: the exact `tool_use` shape of the call, a `Skill` call naming `sc:analyze`, has not been observed in a run; `analyze.md` names no protocol skill, so `sc:analyze` is the expected name.)

4. **WC-4 has one gap that the converse must allow.** `analyze.md:97`: a report directory "that cannot be created or written, counts as no report directory known (refusal printed in chat only)". So "invoked implies folder" holds except for that refusal. The proposed sentence says so in a few words.

5. **The C-004 half that is unpinned is the contract half.** src:6 asks the skill to say the fallback tier "also writes no nested folder and lists no nested contract in artifacts". plan:33, plan:60 and plan:74 pin only directory phrases. Pinning `write no nested directory and no nested contract` (skill) and `writes no nested directory and no nested contract` (routing, cmd) as single phrases covers both halves with no new test helper.

6. **Baseline re-run (read-only), A-004.** `git status --porcelain`: 950 `A `, 3 `R `, 4 `??`; `git ls-files .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016` prints 0. Identical to A1 R2 and A2 R2.

## Proposed wording

### Task 6 live-check sentence (replaces the second sentence of plan:81)

> A live-check extra for brainstorm therefore reads: "for the codebase-enrichment wave, every `nested/analyze-<n>/` directory in the report directory holds its own `return-contract.yaml` that is listed in `artifacts`, and every `nested/analyze-` path listed in `artifacts` exists; no such directory is required, because neither `quality_tier` nor `source` in `enrichment_used` shows whether `/sc:analyze` was invoked (a scan that tried `/sc:analyze`, failed and fell back is recorded `fallback_1` and keeps the folder), so the directory is required only when the worker's session file or one of its subagent files (7.2 step 5) shows a call to `/sc:analyze` and the chat shows no refused report directory" (P1 check lc10 is the origin of this rule).

Why this form: the first clause is checked from the output folder alone (`ls`, then the `artifacts` list in `return-contract.yaml`) and is true for all five rows of New evidence 1. The second clause forbids the tier-based inference that caused lc10 and its reverse. The third clause is the only way to catch a missing folder; it names the subagent files and the `analyze.md:97` refusal so it claims no more than WC-4 gives. It has no clause overlap: nothing in it says "no folder" for any tier.

Companion edits inside Task 6 (no new files): change the first sentence's "exists only for a nested command that actually ran" to "exists only for a nested command that actually ran, including one that ran and failed" (keeps the pinned phrase, plan:84), and say "the auggie scan and the codegraph/Grep scan themselves write no nested directory" instead of tying "no nested directory" to `primary` or `fallback_1`. Add `session file` to Task 6's pinned phrases. Note in the plan that this departs from src:9's sketch on purpose, citing New evidence 1. Placement: per C-006, the general first sentence stays in 2.1; the live-check sentence may go in the P1 section with a pointer from 2.1 (src:9 second branch).

### Wording rule for Tasks 1-3 (true at run level)

> **Rule:** a "no nested directory" statement takes a tool or tier as its writer (the `mcp__auggie__codebase-retrieval` scan, the `fallback_1` tier), never a run or a recorded `quality_tier`; and the folder's condition is written as invocation, not success: "a nested `analyze` directory exists only when `/sc:analyze` was invoked, also when it failed and the scan fell back to `fallback_1`", and every nested contract written is listed in `artifacts`.

Applied:

- **Task 1** (SKILL.md:195, after "(`<n>` starts at 1)"): "; the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract. A nested `analyze` directory exists only when `/sc:analyze` was invoked, also when it failed and the scan fell back to `fallback_1`, so `enrichment_used` does not show whether it exists. Each nested contract written is listed in `artifacts`." This replaces plan:30's "only for a nested command that ran", which is ambiguous for a failed call (criticism 10). No `src/superclaude/` path, no Orca command (plan:22).
- **Task 2** (routing): the planned bullet ("this tier writes no nested directory and no nested contract; the scan is recorded in `enrichment_used` with this tier's `quality_tier`") already obeys the rule: its writer is the tier. Keep it; place each bullet after the tier's `quality_tier` line (C-009) and scope the test per tier (C-005).
- **Task 3** (cmd:157): change "the nested `analyze` directory exists only when `/sc:analyze` ran" to "exists only when `/sc:analyze` was invoked, also when it failed and the scan fell back to `fallback_1`". Leave "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`" as it is; it is already correct.
- **Pins (Tasks 4-5):** in Task 4, slice the `**Under `--unattended`**` paragraph (not the whole Wave 2A section, which makes `fallback_1` vacuous through SKILL.md:199) and assert `write no nested directory and no nested contract` and `` only when `/sc:analyze` was invoked ``; in Task 5, add `writes no nested directory and no nested contract` and `` only when `/sc:analyze` was invoked `` to `UNATTENDED_EXPECT["brainstorm"]["phrases"]`. This closes C-002, both halves of C-004 and the run-level gap, with the existing helpers.

Self-critique of this proposal: the folder clause alone cannot catch a missing folder after an invocation; the session-file clause is needed for that and inherits step 5's "not verifiable" outcome when the file is missing (spec:300). The `sc:analyze` call name is INFERRED (New evidence 3). The sentence is long; a shorter one that drops the third clause would be checkable from the folder but blind to the missing-folder case.

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | no | Each card has 2 P1; R1-1 and R3-2 were over-rated and R1-10 bundles two findings, so counts do not rank the cards. |
| S-002 | none | yes (was split V1/V3) | R1-5 INFERRED hid a groundable premise (SKILL.md:187,198); R3-1 Grounded carried a remedy SKILL.md:372 refutes; R2-1 "doubly" overreached. |
| C-001 | split (V2 diagnosis, V1 remedy) | yes (was V2) | 950 `A` + 3 `R` tracked today and the package is untracked (`git ls-files` = 0), so plan:98's first clause fails; a before/after status diff works in either tree state. |
| C-002 | V3 | no | Task 4 slices all of Wave 2A, where SKILL.md:199 already has `fallback_1`; Task 1's paragraph (SKILL.md:195) lacks it but nothing pins it. |
| C-003 | split (V1/V2, P2) | yes (was V2) | An added bullet keeps every string `test_codegraph_adoption.py:75-82,131,143` asserts; both missing files should still be run. |
| C-004 | V2 | no | src:6 asks for "lists no nested contract in artifacts"; plan:33,60,74 pin only directory phrases; pin `... no nested directory and no nested contract`. |
| C-005 | split (V1/V3) | no | `grep -c` (plan:42) and "at least twice" (plan:60) are file-wide; slice per tier with `_section` (`test_codegraph_adoption.py:56-59`). |
| C-006 | split (V1 defensible, V3 placement) | yes (was V3) | spec:376 keeps the general rule in 2.1; 7.2/7.3 hold no per-command extras (spec:281-327), so src:9's P1-note branch fits the live-check sentence. |
| C-007 | V3 on diagnosis; remedy is this round's folder-plus-session-file sentence (no card's original remedy works) | yes (V3 remedy withdrawn) | Analyze is `primary` (SKILL.md:187,198); `source` cannot name the tool (SKILL.md:372); a failed analyze leaves a folder under `fallback_1` (SKILL.md:199, analyze.md:98). |
| C-008 | split (V2 number, V1/V3 method) | yes (was V2) | 17 is the recorded baseline (diagnostics.txt:11) but A-004 moves; record the before-count inside Task 5. |
| C-009 | split (V1/V2) | no | routing:30 is `quality_tier`, routing:31 the Activation bullet; V3 missed it. |
| C-010 | split (V1/V2) | yes (was V2) | Test at `test_brainstorm_protocol.py:39`, phrases at `test_worker_contract.py:288`; line 711 is synthetic; V3 silent. |
| C-011 | V3 | no | spec line 142 is under `### 3.1` (spec:136); `## 6` starts at spec:215. |
| C-012 | V3 (Low) | no | `write` is not a substring of `writes` (plan:30 vs 39,47); `no nested directory` is in both; A1 R2 withdrew "weakens the pin". |
| C-013 | split (V1/V2) | yes (was V3) | R3-8 misread plan:21 ("no test requires the two to match"); the plugin file is read only per file (`test_codegraph_adoption.py:121,131,143`). |
| X-001 | split (V2/V3) | yes (was V3) | Only Task 4's assertion is vacuous (SKILL.md:199); Task 1's clause fails on old text (SKILL.md:195) but is unpinned. |
| X-002 | V1/V2 (P2) | no | No assertion in either test touches the new text (`test_codegraph_adoption.py:75-82`; `test_tier2_tavily_consistency.py:40-53` per A1/A2). |
| X-003 | V3 on severity (P1, wider than claimed); remedy: this round's sentence | yes (remedy withdrawn) | plan:81 is wrong for both tiers: analyze-clean is `primary` with folder, analyze-failed is `fallback_1` with folder (New evidence 1). |
| X-004 | split (V1 defensible, V3 placement) | yes (was V3) | Same as C-006. |
| X-005 | V2 (first clause); "doubly" overreaches | no | Staged `A`/`R` are tracked (first clause fails); `A`/`R` are not ` M`, so the `done/` clause depends on reading. |
| A-001 | ACCEPT | no | Re-read `test_codegraph_adoption.py:75-82,115-143`; planned text touches no asserted string; run both tests anyway. |
| A-002 | QUALIFY | no | An LLM reviewer judges each AC (`qa.md:49`, per A1/A2); an infeasible AC reaches `dispute` then `E-HALT-QA` (`retry.md:72,107`), so C-001 still blocks. |
| A-003 | QUALIFY | no | Substring pins are house style (`test_worker_contract.py:508-509`) but prove presence, not run-level truth; they need paragraph/tier scope and phrases written to the run-level rule above. |
| A-004 | QUALIFY | no | Re-run today: 950 `A` / 3 `R` / 4 `??`, package untracked; Tasks 5 and 7 must capture their own before-state. |
