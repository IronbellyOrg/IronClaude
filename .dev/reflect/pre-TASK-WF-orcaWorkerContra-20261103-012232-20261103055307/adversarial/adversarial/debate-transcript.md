# Adversarial Debate Transcript

## Metadata
- Mode: A (compare three existing reviewer cards); non-interactive
- Variants: A = `variant-1-original.md` (reviewer 1, analyzer, PASS), B = `variant-2-original.md` (reviewer 2, qa, PASS), C = `variant-3-original.md` (reviewer 3, refactorer, FAIL) (DA:6-8)
- Depth: standard
- Rounds completed: 2 (Round 1 and Round 2)
- Round 2.5 (invariant probe): ran (INV:1-2)
- Round 3: skipped, because depth=standard
- Convergence achieved: 100% (21 of 21 diff points agreed by at least a 2-of-3 majority)
- Convergence threshold: 80%
- Convergence status: **BLOCKED_BY_INVARIANTS** (INV-001 is HIGH and UNADDRESSED, INV:5)
- Focus areas: correctness, coverage, deviation-classification (DA:9)
- Advocate count: 3 (default model; personas analyzer, qa, refactorer)
- Orchestrator: debate-orchestrator; it did not take part in the debate and spawned no agents

## Citation Key
The orchestrator's own sections (everything outside the copied round text) use these keys. Every line cited was opened by the orchestrator for this step.

| Key | File |
|---|---|
| `VA:N`, `VB:N`, `VC:N` | `variant-1-original.md`, `variant-2-original.md`, `variant-3-original.md` in this directory |
| `DA:N` | `diff-analysis.md` in this directory |
| `R1a:N`, `R1b:N`, `R1c:N` | `round1-advocate-{a,b,c}.md` in this directory |
| `R2a:N`, `R2b:N`, `R2c:N` | `round2-advocate-{a,b,c}.md` in this directory |
| `INV:N` | `invariant-probe.md` in this directory |
| `TL:N` | `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md` (the plan) |
| `SRC:N` | `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md` (the spec) |
| `qa.md:N` | `~/.claude/skills/sc-implement-protocol/refs/qa.md` |
| `SK:N` | `~/.claude/skills/sc-adversarial-protocol/SKILL.md` |

The round statements below are copied in full from the round files. Their own headings are moved down three levels so they sit under this transcript's headings; no other text is changed. Their internal citations use the keys each statement defines.

Ground-truth spot checks made by the orchestrator for this step (all match the advocates' quotes):
- TL:21 reads "P0 edits no command, skill or agent file"; TL:90 orders the byte copy to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; TL:93 makes `cmp` an acceptance criterion; TL:24 names "their plugin copies".
- SRC:220 says only "(no command edits)" and requires "its two mirrored copies".
- qa.md:52 makes a quotable Constraints or task-instruction breach a blocking trigger; qa.md:61 reads back only byte presence; qa.md:79 says the reviewer's label is never read; qa.md:310 makes the managed FINAL return `issues` for a violated plan Constraint and when "a log cited on a task's latest `complete` line shows a failure at its outcome line"; qa.md:286 maps FINAL `issues` to `E-ARCHIVE-BLOCKED`; qa.md:294 says the FINAL returns `issues` "only for a blocking defect".
- TL:112 says "at most 10" "(as written in section 2.3)"; SRC:122 says "maximum of 10 inputs" and "never exceeds 10".
- TL:125 requires "the phase that converts its command" and defines a `gh api` post to include `-f` and `-F`; SRC:305 asks only for "an explicit allowlist with a reason" and also allows "refused under `--unattended`".
- TL:19 names "AC-0.8"; SRC:304 (AC-0.7) is followed by SRC:305 (AC-0.9) and SRC:306 (AC-1.1).

## Round 1: Advocate Statements

### Variant A Advocate (default model, persona analyzer)
<!-- Source: round1-advocate-a.md (copied in full; headings moved down three levels) -->
#### Round 1 Advocate: Variant A (reviewer 1, analyzer, PASS)

Citation key as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` are card lines; `TL:N` is the plan; `SRC:N` is `source.md`; `qa.md:N` is `~/.claude/skills/sc-implement-protocol/refs/qa.md`; `retry.md:N` is the same skill's `refs/retry.md`. I opened every line cited below in this round. Checks I ran today are marked "(run today)".

##### Position summary

Variant A's five findings are the best-grounded set. They include the only check against a repo ABSOLUTE RULE (R1-F4) and the only concrete instance of an off-spec phrase the tests must pin (R1-F1). But A's PASS verdict is wrong. I concede that Variant C's R3-F1 is a real conflict that no repair can close, and that two separate executor gates can turn it into a halt. The merged verdict should be FAIL with R3-F1 as its single blocking item, fixed by rewording one constraint, and A's findings should anchor the should-fix list.

##### Steelman

**Variant B (qa, PASS).** B is the leanest card, and each of its claims was checked. R2-1 is a real false statement: "AC-0.8" occurs only at TL:19, and the spec's P0 rows run AC-0.1 to AC-0.7 and then AC-0.9 (SRC:298-305), with P1 starting at AC-1.1 (SRC:306). B is the only card that explicitly walks the executor's halt paths in its self-audit (B:80-85) and the only one that records coverage-matrix omissions (B:58-64). Its PASS has a defensible reading: TL:24 names "their plugin copies" as allowed carriers of Orca text. The plugin `refs/HOW-WE-WORK.md` is a byte copy of a core document, not an authored skill file. The constraint's own citation, "no command edits" (TL:21, quoting SRC:220), suggests the narrower meaning.

**Variant C (refactorer, FAIL).** C is the most thorough card and the only one that derives severity from the executor's actual rules rather than from a guess about how lenient a reviewer will be (C:14-16, C:23-24, C:65). It spotted that the plan made the spec's wording wider: SRC:220 says only "(no command edits)", while TL:21 says "no command, skill or agent file". That change is what creates the conflict with TL:90. C's fix is one sentence (C:26-28). Its self-confidence of 0.6 openly says the result depends on a reviewer reading the constraint literally (C:211-212). Its other ten findings cover Tasks 1-6 and 8, and several cite tests that I or the calibrator could confirm (Makefile verify-sync scope, `test_retired_docs_absent.py:40`, `test_how_we_work_routing_table.py:341`).

##### Strengths claimed

1. **R1-F1 names the concrete defect behind C's general R3-F3.** TL:112 tells Task 5 to assert "at most 10" "(as written in section 2.3)". That claim is false. A grep across the package found "at most 10" only at TL:56 and TL:112 (run today). SRC:122 says "the merge command's maximum of 10 inputs" and "never exceeds 10". TL:104 requires each assertion to use "a phrase quoted from `./source.md`". So the plan contradicts itself: following TL:112 breaks TL:104. A contract written in the spec's own words fails the test TL:112 describes. C's R3-F3 (C:52-59) describes the mechanism but gives no instance. The merged finding needs A's instance as its anchor.
2. **R1-F4 (U-001) is the only check against a repo ABSOLUTE RULE.** CLAUDE.md:76 forbids pointing installed primitives in `src/superclaude/{commands,skills,agents,core,...}` at `src/superclaude/...` paths. CLAUDE.md:87 says package code (`src/superclaude/cli/`) is not installed: "Do not add new references to them from a primitive". The text Task 1 must restate carries exactly such references. SRC:59 cites `src/superclaude/cli/install_core.py:36,56,65-70` and `CAPS:130`. The WC rows carry `INV-A:`, `CAPS:` and `sk/...` evidence (SRC:70-81). TL:37-40 says to write the rules "from these source sections" and never says to drop the evidence citations. The plan's Constraints (TL:17-27) carry the source-of-truth rule (TL:23) but not the installed-path rule. AC-C1 checks only Orca verbs (SRC:246). The managed FINAL checks plan Constraints, not repo CLAUDE.md (qa.md:310). So no gate in this run catches it, and the file installs into other projects (SRC:59, `~/.claude/WORKER-CONTRACT.md`). No other card raised this.
3. **R1-F2 (U-002) is a real path to a QA failure.** TL:157 requires "a PASS or FAIL line with an evidence file for each of the eleven checks". No task saves an artifact for AC-0.1 (TL:47, TL:72), AC-0.2 or AC-0.3 (TL:93-94), and Task 8 re-runs only the common checks (TL:147-152). Under the executor's Evidence-type AC rule, "the evidence artifact is absent" means `ac-outcome-missing=yes` (qa.md:85), which blocks (qa.md:41). The executor can still save the files inside Task 8, so should-fix is the right grade.
4. **R1-F3 is grounded in the spec, not only in a hit count.** SRC:61 puts `/sc:pr-submit` on the never-as-worker list. SRC:174 says the pr-submit row "applies only if D3 (b) is ever adopted". SRC:201 says pr-submit gets "no `--unattended` mode and no Phase 4 changes". So for these hits, TL:125's "the phase that converts its command" has no true value. C's R3-F5 (C:96-101) adds a second cause (read-only `gh pr` hits; H9 counts 40 `gh pr` hits) and the keying problem. The two together make one finding.
5. **R1-F5 names the line that decides Task 3, which B's R2-3 does not.** `scripts/build_superclaude_plugin.py:75` copies `["agents", "commands", "hooks", "scripts", "skills"]` and no `core` (opened today). B's evidence is the empty hunk H4 (B:56; `grounding-hunks.md` H4 is empty). The grounding is worse than B says. H5 reports `plugins/superclaude/core` as "(no matches)", but a Glob today lists `RESEARCH_CONFIG.md`, `BUSINESS_PANEL_EXAMPLES.md`, `RULES.md`, `PRINCIPLES.md`, `BUSINESS_SYMBOLS.md`, `CODEGRAPH.md` and `__init__.py` there. The executor should be pointed at the build-script line, not left to work from an absence.
6. **A is the only card that checked Task 7's environment.** A's self-audit checked that the `/opt/Orca` files exist and that the profile holds `"nestedWorkerMaxDepth":1` (A:110-112). The B and C calibrators both flag this as the gap in their cards (B:99, C:229). A's self-audit also recorded the missing `make verify-sync` baseline (A:117-118), which C later filed as R3-F11.

##### Weaknesses identified in others

1. **B:81-82 asserts a check whose result the plan text contradicts.** "No task instruction breaches the plan's own Constraints" is false on the literal text: TL:21 says "P0 edits no command, skill or agent file", and TL:90 orders a write to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. That directory also holds the skill's `SKILL.md` (listed today). B's PASS rests on a lenient reading it never states.
2. **B's R2-3 is mostly redundant.** TL:69 already tells the executor to "Read `scripts/build_superclaude_plugin.py`", and B's own calibrator says so (B:96). The useful part, naming line 75, is in A's R1-F5.
3. **B's R2-1 is over-graded.** No task, AC or gate reads the AC-0.8 sentence. The FINAL tests whether a Constraints item is violated (qa.md:310), not whether it is true, and nothing can violate a scope note about a check that does not exist. It is a real false statement and should be fixed, but at minor.
4. **C's R3-F3 has the wrong deviation class.** It is a conflict inside the plan (Task 5 against Tasks 1-2), not a departure from the spec, as C's calibrator notes (C:226). Merged with A's R1-F1, the class is drift on firmer ground: TL:112 attributes to section 2.3 a phrase that section 2.3 does not contain (SRC:122).
5. **C's R3-F6 has a wrong citation and an inflated grade.** Line 290 of `tests/core/test_how_we_work_routing_table.py` holds the marker-order assertion, not the `"### 3.14 "` to `"## 4. "` slice C quotes (C:227; diff-analysis C-005 places the slice at line 1091). Task 4's own AC runs those tests (TL:93), so a breach shows up in the same task and costs one repair round, not a halt. That is minor.
6. **C's R3-F4 depends on a copy the evidence argues against.** The build script does not ship `core/` (`build_superclaude_plugin.py:75`). The verify-sync gap C cites (Makefile:170, 202, 228, 254, 280) is real, but it matters only if Task 3 adds the copy. It should be a conditional clause on R1-F5 ("if you add a copy, add a byte-identity test like `test_plugin_mirror_matches_src`"), not a standalone should-fix.
7. **C under-cited its own blocker.** C names only the Task 4 reviewer gate (qa.md:52, qa.md:61). The managed FINAL is a second, independent gate: it returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310), which ends in `E-ARCHIVE-BLOCKED` (qa.md:286). This makes C's case stronger, not weaker.

##### Concessions

1. **A missed the one blocking defect.** A's "I found no blocking defect" (A:112) is wrong. A's self-audit never claims it checked each Constraint against each task body. That was the gap, and C filled it (C:204-205).
2. **Under the executor's real rules, R3-F1 can halt the run and no repair closes it.** Here is the chain, with each step's source:
   - The Task 4 reviewer is asked: "does the diff violate a quoted plan constraint ... or an explicit task instruction?" (qa.md:339). The diff adds a file under `plugins/superclaude/skills/sc-recommend/`, next to that skill's `SKILL.md`.
   - If the reviewer says yes and quotes TL:21, the parent's only check is that "the quoted text is byte-present in the plan Constraints" (qa.md:61). It is. The reviewer's own label is never read (qa.md:79).
   - The inherited cap does not apply, because the file change is new in Task 4's diff, not text present in `$start` (qa.md:154, qa.md:166).
   - A repair cannot satisfy both rules. Dropping the copy fails AC-0.2's `cmp` (TL:93), which is B1. Keeping it keeps the B4 breach. The ladder ends in `E-HALT-QA` (qa.md:280). If the adviser disputes the contradictory AC instead (retry.md:72), the run ends in a `dispute` halt (qa.md:281).
   - If the Task 4 reviewer is lenient, the managed FINAL gets an independent second chance (qa.md:310, qa.md:286).

   The one step that needs judgment is the reviewer's yes. TL:24 ("and their plugin copies") gives a lenient reviewer cover. But two separate fresh reviewers each get a chance, the consequence is a halt that needs the user, and the fix costs one line. A pre-execution review should rate a reachable, unrepairable halt as blocking. I concede the merged verdict is FAIL.
3. **C's R3-F5 improves on A's R1-F3.** It adds the read-only `gh pr view/list/checks` hits and the problem of line-number keys. Its recommendation (key by path, verb and stripped line; a closed category set, C:108-110) is better than A's reason format alone (A:65-66). The merged fix should combine them.
4. **A noted the verify-sync baseline gap but did not file it** (A:117-118). C's R3-F11 rightly files it, and it adds the uncovered `tests/docs` and `tests/unit` scans (`test_retired_docs_absent.py:40`).
5. **R1-F5 overstates one piece of evidence.** A says "two tests that pin plugin core copies of CODEGRAPH.md" (A:95). I confirmed only one: `tests/commands/test_impact_command.py:309` parametrizes the plugin copy for a dollar-safety check. It does not check that the copy matches the source byte for byte, and the citation at :308 is one line off (A:130). The merged finding should say "one test reads the plugin core copy of CODEGRAPH.md".

##### Positions on diff points

| Point | Preferred variant or merged position | Reason (citations) |
|---|---|---|
| S-001 | C: FAIL, 1 blocking | R3-F1 is unrepairable and reachable through qa.md:52/61 and qa.md:310 (Concession 2) |
| S-002 / S-003 | Merged list: 1 blocking, about 8 should-fix, the rest minor, after dedup | C's count is inflated by R3-F4 and R3-F6 (Weaknesses 5-6); B's undercounts |
| S-004 | Merged: drift for R3-F1, R3-F2, R1-F1+R3-F3, R1-F3+R3-F5, R2-1; none for the others | Drift means the plan departs from the spec. R3-F3 on its own is internal to the plan (C:226) |
| S-005 | Keep B's matrix_omissions as a minor appendix | SRC:236 and SRC:188 are real spans; no task in this plan depends on them (B:61) |
| S-006 | C's method is right | qa.md decides severity mechanically (qa.md:41, 56-61, 79); card-level grading should cite it |
| S-007 | File a Constraints defect under the task it collides with | TL:21 only harms through Task 4 (TL:90), so `tasks: [4]` is more useful than `[0]` |
| S-008 | Add a Task 7 risk line from A's self-audit (no finding) | A checked that the `/opt/Orca` files exist (A:110-112); a note keeps the environment dependency visible |
| S-009 | No action | Calibration does not change any severity |
| C-001 | Merge R1-F3 and R3-F5, should-fix, drift | Spec causes (SRC:61, 174, 201) plus read-only hits and keying (C:96-101, H9) |
| C-002 | A's R1-F5, minor, with C's R3-F4 as a conditional clause | `build_superclaude_plugin.py:75` decides it; H4 is empty and H5 is wrong (Strength 5) |
| C-003 | Merge: A's instance (TL:112 against SRC:122) plus C's mechanism and fix (C:66-70), should-fix, drift | TL:104 and TL:112 conflict; the FINAL route via "a later change contradicts it" (qa.md:310) is real but needs two conditions (C:225) |
| C-004 | C's R3-F11, minor | A recorded the gap (A:117-118); C filed it with extra test-scope evidence |
| C-005 | R3-F6 at minor, with the citation fixed to the right lines | Self-surfacing in Task 4 (TL:93); the line 290 citation is wrong (C:227) |
| X-001 | C: FAIL | Concession 2 |
| X-002 | C: blocking; fix before execution with C's reword (C:26-28) | TL:21 against TL:90/TL:93; two gates (qa.md:52/61, qa.md:310); the plan widened SRC:220 |
| X-003 | C: should-fix, drift, not blocking; fold it into the same constraint edit | SRC:84 brings in "every flag section 3 lists as required", and SRC:59/SRC:220 name the brief template, so a reviewer has textual cover; the "from P1" marker (TL:58) is the weak spot |
| X-004 | A, with C's precedent noted | The build script never copies core (:75); `plugins/superclaude/core/` does hold six core `.md` files (Glob today), so a copy is possible but serves no distribution purpose |
| U-001 | Keep A's R1-F4, should-fix (the highest-value should-fix) | CLAUDE.md:76, 87; SRC:59; TL:17-27 and qa.md:310 do not catch it |
| U-002 | Keep A's R1-F2, should-fix | TL:157 against TL:47, 72, 93-94, 147-152; qa.md:85 |
| U-003 | Keep B's R2-1, minor | A false scope note; no gate reads it (Weakness 3) |
| U-004 | Keep B's R2-2, minor | SRC:238 and SRC:303-304 require results "in the phase report"; TL:154 gives no handoff |
| U-005 | Keep as an appendix | Bookkeeping only |
| U-006 | Keep C's R3-F1, blocking, drift | Concession 2 |
| U-007 | Keep C's R3-F2, should-fix | X-003 |
| U-008 | Fold into R1-F5 as a conditional clause | Weakness 6 |
| U-009 | Keep C's R3-F7, minor | TL:115 against SRC:306 |
| U-010 | Keep C's R3-F8, minor | TL:58; there is a precedent check at `test_how_we_work_routing_table.py:258` |
| U-011 | Keep C's R3-F9, minor | TL:15 against TL:90 |
| U-012 | Keep C's R3-F10, minor | TL:154 against SRC:90; TL:19 partly covers it already |

##### Shared-assumption responses

- **A-009: ACCEPT.** `src/superclaude/cli/install_core.py:30-32` reads `def install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`, which matches the call at TL:72. Its docstring (line 36) says it copies all `.md` files from `src/superclaude/core/`. The worktree's `.venv` installs `superclaude` in editable mode from this worktree (`direct_url.json`: `"editable":true`, url = this worktree; the `.pth` points at `<worktree>/src`), so `uv run` will read the new file and not a stale installed copy. If it did not, Task 3's own AC would fail loudly rather than pass silently.
- **A-010: ACCEPT.** `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md` printed nothing against merge base `c118b5a5` (run today). The check compares against the merge base, so later commits on `master` do not change the result unless the branch is rebased onto a `master` that deleted guide lines. Nothing in this plan rebases.
- **A-011: ACCEPT.** The SRC:246-253 pipeline, run read-only on today's tree, printed nothing and grep exited 1 (run today). The pipeline excludes `plugins/superclaude/core/WORKER-CONTRACT.md` by name (SRC:252), so the scan stays clean whichever way Task 3 decides (A-008). Any later hit can only come from this plan's edits.


### Variant B Advocate (default model, persona qa)
<!-- Source: round1-advocate-b.md (copied in full; headings moved down three levels) -->
#### Round 1 advocate: Variant B (reviewer 2, qa persona)

Citation key: as in `diff-analysis.md` (A:N, B:N, C:N for the cards; TL:N plan; SRC:N spec; qa.md:N and SKILL.md:N for the executor rules). Every TL, SRC, qa.md and repo line below was opened for this round. Checks I ran myself are marked "(ran)".

##### Position summary

Variant B's PASS verdict does not survive. Its central claim, "no task instruction breaches the plan's own Constraints" (B:81-82), is false against TL:21 and TL:90, and the executor's real QA rules make that conflict a reachable halt that no repair can close. I concede the verdict to Variant C (FAIL, R3-F1 blocking). Variant B still contributes two verified findings no other card has (R2-1, R2-2), the only executor-halt-path inventory framed for QA, and the test I propose for grading every other item: a plan defect is blocking only when it opens a halt path that no in-run repair can close.

##### Steelman

**Variant A (analyzer, PASS).** A's strongest case is breadth with precision. It is the only card to catch the repo's ABSOLUTE RULE against `src/superclaude/...` paths in installed primitives (R1-F4), and that defect is real: SRC:59 carries `src/superclaude/cli/install_core.py:36,56,65-70`, and the spec has 29 lines mentioning `src/superclaude` (ran). A Task 1/2 "restate" could copy those into a file installed to `~/.claude/`. A is also the only card that names the concrete off-spec phrase in Task 5: "at most 10" appears in TL:56 and TL:112, while SRC:122 says "maximum of 10 inputs" (ran: `grep 'at most 10' source.md` finds nothing). A checked the live environment for Task 7 (A:110-112), which B and C did not. Its PASS rests on a defensible reading: TL:24 already allows "their plugin copies" of `HOW-WE-WORK.md` to carry Orca text, so a reviewer can read TL:21 as aimed at command, `SKILL.md` and agent files, as its own citation "no command edits" suggests.

**Variant C (refactorer, FAIL).** C's strongest case is that it reasons from the executor's actual severity rules, not from the reviewer's sense of what is serious. It quotes the constraint (TL:21), the mandatory write (TL:90, with the `cmp` AC at TL:93), and the mechanical rules: a B4 answer is confirmed when "the quoted text is byte-present in the plan Constraints or a task instruction" (qa.md:61), and the reviewer's own label is never read (qa.md:79). C also shows the conflict is self-inflicted: the spec's P0 row says only "(no command edits)" (SRC:220), and the plan added "skill or agent". C honestly reports its 0.6 confidence as doubt about R3-F1's severity, not about card quality (C:211-212, C:230). It also covers the most tasks with the most findings (11 findings across Tasks 1-6 and 8).

##### Strengths claimed

1. **R2-1 is a verified false statement in the plan's scope block.** TL:19 says "AC-0.8 is a P1 check (section 7.3)". There is no AC-0.8 in the spec (ran: `grep -n 'AC-0\.8' source.md` exits 1). The P0 rows go AC-0.7 (SRC:304) then AC-0.9 (SRC:305), and P1 starts at AC-1.1 (SRC:306). No other card caught it. My calibrator re-verified it (B:94).
2. **R2-2 is the only finding on the static-to-live handoff.** The spec puts the phase report in the live plan (SRC:238), and AC-0.6 and AC-0.7 results must appear "in the phase report" (SRC:303, SRC:304). Task 8 ends with next steps only (TL:154) and never obliges the live plan to carry `p0-static-report.md` or the AC-0.7 and AC-C6 artifacts. Diff analysis rates its value Medium (U-004), above its card label of minor.
3. **B's halt-path inventory is the right frame for the debate.** B is the only card that lists the executor's halt paths by name and asks whether any defect reaches them (B:82-84: E-NO-AC, E-HALT-QA ladder, quoted-constraint breach, FINAL issues). The frame is correct; B applied it wrongly to TL:21. Applied correctly, it gives the grading test I use below: blocking at plan stage means a reachable halt (qa.md:280-286) that no repair inside the run can close.
4. **B's structural checks hold.** Every pytest target named in Tasks 3 and 4 exists (B:68-72; calibrator confirmed, B:97). The Depends-on graph is satisfied by source-order execution (B:73-74), which matches SKILL.md:97 ("Default sequential in source order"). Shared assumption A-002 rests on this.
5. **R2-3 and the empty-hunk observation.** B is the only card that noticed grounding hunk H4 (the plugin build script) is empty (B:47-50), an evidence gap in the reflect run itself. I concede below that A's R1-F5 is the better finding on the same Task 3 question.
6. **`matrix_omissions` (B:58-64)** records two spec spans (SRC:236, SRC:188) with no coverage-matrix anchor. This is bookkeeping, not a plan defect, and should be carried as a note only.

##### Weaknesses identified in others

1. **A's PASS ignores the route its own calibrator half-saw.** A's calibrator notes that qa.md:52 makes breach of "an explicit task instruction" a blocking trigger and that A "under-states this route" for R1-F1 and R1-F3 (A:132). A never applies the same rule to the Constraints block, so it misses TL:21 against TL:90.
2. **A's R1-F3 and C's R3-F5 under-state one edge case.** TL:125 requires "the phase that converts its command" for every allowlist entry. For a hit no phase converts (pr-submit and git are never workers, SRC:61, SRC:201), the executor must either omit the phase (an explicit-instruction breach, qa.md:52) or invent one (a false claim in delivered text, qa.md:50). Both are `yes` answers. This is repairable in practice (write "none: never a worker"), so it stays should-fix, but it is the next-nearest halt risk after R3-F1 and should be fixed in the same pass.
3. **C's R3-F1 overstates certainty.** C says a strict reviewer "ends the run" (C:15-17). The Read-back only checks that the quote is byte-present (qa.md:61). Whether the diff "violates" the constraint is still the reviewer's yes or no (qa.md:52, qa.md:56). So the halt is conditional, as C's calibrator says (C:223). This does not lower the grade (see X-002), but the merged text should say "can halt", not "will halt".
4. **C's R3-F6 has a wrong citation.** C cites `tests/core/test_how_we_work_routing_table.py:290` for the "### 3.14 " to "## 4. " slice; line 290 holds the marker-order assertion and the slice is at line 1091 (diff-analysis C-005; C's calibrator, C:227). The claim stands; the citation must be corrected in the merge.
5. **C's R3-F3 deviation class is loose.** It is an inconsistency inside the plan (Task 5 against Tasks 1-2), not a departure from the spec, so `drift` is arguable (C's calibrator, C:226). A's R1-F1 is the concrete, spec-departing instance (TL:112 says "as written in section 2.3" for a phrase the spec does not contain). The merged finding should lead with A's instance.
6. **Neither A nor C checked Task 7's environment in a finding.** A checked it in its self-audit only. I confirmed it today (ran): `/opt/Orca/resources/app.asar.unpacked/out` exists and `~/.config/orca/profiles/local-default/orca-data.json` exists. So A-004 holds and no finding is needed.

##### Concessions

1. **B's verdict is wrong.** B:81-82 says no task instruction breaches the Constraints. TL:21 forbids editing any "skill ... file"; TL:90 orders a byte-for-byte write to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, a file inside a skill package that also holds `SKILL.md` (ran: `ls plugins/superclaude/skills/sc-recommend/`). TL:93 makes that write an AC. B also claimed the halt paths were "not reachable from any defect I could locate" (B:84). That is false for this defect.
2. **B missed the strongest gate.** Even if the Task 4 reviewer reads TL:21 leniently, the managed FINAL is a fresh subagent that reads "the plan's `## Constraints`" and returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310). That blocks archiving as `E-ARCHIVE-BLOCKED` (qa.md:286). Two independent readers each get a chance to say yes.
3. **No inherited cap rescues it.** The cap applies only to text present in `$start` (qa.md:153-154). The new Orca lines in the plugin copy are written by Task 4, so their origin is `new` and a confirmed B4 is `blocking` (qa.md:41, qa.md:81).
4. **R2-3 is subsumed by A's R1-F5.** A names the deciding line (`scripts/build_superclaude_plugin.py:75`, no `core` in the copied folders) and the parity test (`tests/commands/test_routing_plugin_parity.py:3-4`). My calibrator noted my recommendation was largely redundant because TL:69 already orders a full read (B:96). Merge R2-3 into R1-F5 at minor.
5. **R2-1 is lower impact than its label.** B2 (`false-claim`) covers "delivered text or code" (qa.md:50); plan text is not delivered, so the false AC-0.8 sentence cannot trigger a halt. I accept a downgrade from should-fix to minor; the class stays `drift` because the plan states something the spec does not.
6. **B missed Task 7's environment risk** (my calibrator, B:99) and the verify-sync baseline gap (C-004). Both turn out to be low: the paths exist today, and C-004 is minor.

##### Positions on diff points

| Point | Preferred variant or merged position | Reason (with citation) |
|---|---|---|
| S-001 | C: merged verdict FAIL, 1 blocking (R3-F1) | The only finding that opens a halt no repair can close: drop the copy and TL:93 fails; keep it and TL:21 is breached. A failed repair ends in `E-HALT-QA` `ladder-end` or a `dispute` halt (qa.md:280-281). |
| S-002 / S-003 | Merged list, about 15 findings after dedup | Keep C's coverage, A's unique R1-F2 and R1-F4, and B's R2-1 and R2-2; merge the pairs in C-001, C-002, C-003, C-004. |
| S-004 | Classes as merged below | Drift only where the plan departs from the spec (R3-F1, R3-F2, R1-F1, R1-F3/R3-F5, R2-1). |
| S-005 | B, as a note | Matrix omissions are bookkeeping; no plan task is affected (B:61). |
| S-006 | C's method | Severity must come from qa.md, because the parent derives it mechanically and never reads the reviewer's label (qa.md:37, qa.md:79). |
| S-007 | File under the task that collides (C) | The defect shows up in Task 4's review, so `tasks: [4]` tells the fixer where the halt happens. |
| S-008 | Note the gap | No card has a Task 7 finding; that is correct, since its environment holds today (ran). |
| S-009 | No action | Calibration numbers do not change grades. |
| X-001 | C: FAIL | See S-001 and X-002. |
| X-002 | C: R3-F1 blocking, must be fixed before execution | Two gates can confirm it: Task 4 QA (qa.md:52, qa.md:61) and the managed FINAL (qa.md:310, leading to `E-ARCHIVE-BLOCKED`, qa.md:286). The halt needs one reviewer's literal reading, but the plan cannot be repaired from inside the run and the fix is one reworded sentence that also restores SRC:220's wording. Record it as "can halt", not "will halt". |
| X-003 | C: R3-F2 should-fix, drift; fix in the same pass as R3-F1 | Same shape as R3-F1 but defensible: TL:22 limits the contract to sections 2.1-2.3, and section 2.3 itself brings in "every flag section 3 lists as required" (SRC:84); SRC:220 adds "a coordinator brief template listing the section 3.1 flags". The "from P1" marker (TL:58) is the one piece with no by-reference cover, so add C's wording (C:46-47). |
| X-004 | A on the evidence; minor | The build script never copies `core` (`scripts/build_superclaude_plugin.py:75`), but `plugins/superclaude/core/` already holds core files (diff-analysis X-004). Either outcome passes TL:74. Merge R2-3 into R1-F5. |
| U-001 (A, R1-F4) | Keep, should-fix, high priority | Real ABSOLUTE RULE defect (repo `CLAUDE.md`, installed-primitive path rule; SRC:59 carries `src/` paths). Not blocking because the rule is not in the plan's Constraints (TL:17-27), and qa.md:52 and qa.md:310 read only plan Constraints and task text. That same fact is why it must be fixed: nothing in the run would catch it. Add A's Constraints line (A:84-85). |
| U-002 (A, R1-F2) | Keep, should-fix | A missing evidence file is `ac-outcome-missing=yes` (qa.md:85), but Task 8 can save the re-run outputs in a repair, so it is closable inside the run. |
| U-003 (B, R2-1) | Keep, downgrade to minor, drift | False scope sentence at TL:19; cannot halt (qa.md:50 covers delivered text only). |
| U-004 (B, R2-2) | Keep, minor | Spec-silent handoff (SRC:238, SRC:303-304 against TL:154); no task in this run fails. |
| U-005 (B) | Note only | Bookkeeping. |
| U-006 (C, R3-F1) | Blocking | See X-002. |
| U-007 (C, R3-F2) | Should-fix | See X-003. |
| U-008 (C, R3-F4) | Should-fix, conditional on Task 3 adding the copy | `make verify-sync` does not cover core (diff-analysis U-008, Makefile lines cited there). |
| U-009 to U-011 (C) | Minor | Maintainability and wording; TL:115, TL:58, TL:15 against TL:90. |
| U-012 (C, R3-F10) | Minor | TL:154 stages before the archive move; TL:19 already gives the commit-time AC-C4 to the coordinator. |
| C-001 (R1-F3 + R3-F5) | Merge, should-fix, drift | SRC:305 asks only for "an explicit allowlist with a reason"; TL:125 adds a phase. Use A's closed reason format (A:65-66) plus C's path-verb-text keying (C:108-110). Add the edge case in Weakness 2. |
| C-002 (R1-F5 + R2-3) | A's version, minor | See X-004. |
| C-003 (R1-F1 + R3-F3) | Merge, should-fix | Lead with A's concrete case (TL:112 against TL:104 and SRC:122) and keep C's ownership and FINAL consequence (qa.md:310). |
| C-004 (A note + R3-F11) | C's R3-F11, minor | No verify-sync baseline before the first edit (TL:33-35); a pre-existing drift would surface as an AC-C2 failure at TL:96. |
| C-005 (R3-F6) | Should-fix, with the citation corrected to line 1091 | Each failure costs a repair round; repairable, so not blocking. |

##### Shared-assumption responses

- **A-009: ACCEPT.** `install_core_files` takes `target_path` and returns a `(bool, str)` pair, exactly as TL:72 unpacks it. Verified at `src/superclaude/cli/install_core.py:30-32` (ran: `def install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`).
- **A-010: ACCEPT.** The merge base is `c118b5a5` and `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md` prints nothing today (ran). No task before Task 4 touches that file (TL:31-74), so AC-0.3 (TL:94) starts clean.
- **A-011: ACCEPT.** The AC-C1 pipeline from SRC:246-253, run read-only on the current tree, printed nothing (ran; the pipeline exited 1, meaning no lines). The two files this plan adds Orca text to, and their plugin copies, are excluded by name (SRC:250-253), and the new test file lives under `tests/`, which the scan does not cover. So only an unintended Orca verb in a command, skill or agent file could fail it.


### Variant C Advocate (default model, persona refactorer)
<!-- Source: round1-advocate-c.md (copied in full; headings moved down three levels) -->
#### Round 1 Advocate: Variant C (reviewer 3, refactorer, FAIL)

Citation key as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` are variant-card lines; `TL:N` is the plan; `SRC:N` is `source.md`; `qa.md:N` is `~/.claude/skills/sc-implement-protocol/refs/qa.md`. Every line cited below was opened in this round.

##### Position summary

The merged verdict should be FAIL with one blocking finding, R3-F1: the plan's own Constraint (TL:21, "P0 edits no command, skill or agent file") contradicts a mandatory write in Task 4 (TL:90, checked by `cmp` at TL:93), no repair can satisfy both, and the executor has two gates that can turn one literal reading into a halt. The fix is one sentence and puts back the spec's own wording (SRC:220, "no command edits"). C also brings the most should-fix coverage, but it missed U-001 (installed-path rule) and R2-1 (AC-0.8), and both belong in the merged list.

##### Steelman

**Variant A (analyzer, PASS).** A is the most environment-grounded card. It is the only card that checked Task 7's inputs, `/opt/Orca` and the profile file (A:110-112). It verified the installer manifest and the `KNOWN_CORE_FILES` set-equality test (A:107-109, A:134). It found the one repo-rule defect no other card saw: the installed-path rule (R1-F4, A:67-85). It also gives the concrete off-spec phrase "at most 10" (R1-F1; verified: TL:56 and TL:112 say "at most 10", SRC:122 says "maximum of 10 inputs" and "never exceeds 10"). The best case for its PASS on R3-F1 runs like this. TL:21 cites its own authority, "no command edits" (SRC:220), so its intent is command files. TL:24 says that HOW-WE-WORK.md "and their plugin copies" may describe the coordinator side, so the plan expects the plugin copy to receive Orca text. Task 4 is the more specific instruction and should govern the general one. A reviewer who reads the whole plan would see an expected, spec-mandated copy (SRC:212, SRC:299), not a breach.

**Variant B (qa, PASS).** B is the only card that states the Constraints-versus-tasks check outright and walks the closed interrupt list (B:80-85, matching qa.md:276-288). It found a false statement in the Constraints: AC-0.8 does not exist (R2-1; verified: TL:19 names AC-0.8, and SRC:298-305 run AC-0.1 to AC-0.7 then AC-0.9, with P1 starting at AC-1.1 on SRC:306). It also found the cross-plan handoff gap to the live plan's phase report (R2-2; SRC:238, SRC:303-304). The strongest form of B's "no breach" claim for R3-F1: in this repo, a "skill file" usually means a skill's `SKILL.md`, and the file Task 4 writes is a byte copy of a core document that only happens to sit in a `refs/` folder. On that reading no Constraint is breached, and B's halt-path analysis holds.

**Strongest case that R3-F1 is not blocking (combined).** (1) TL:24 names "their plugin copies". (2) TL:21's parenthetical limits its source to "no command edits". (3) B4 needs a reviewer to judge that "the diff violates" the Constraint (qa.md:52), and a reviewer applying the task's own instruction is unlikely to call the mandated output a breach. (4) My card's self-confidence was 0.6 for exactly this reason (C:209-212), and my calibrator called blocking "conditional on a reviewer reading the constraint literally" (C:223).

##### Strengths claimed

1. **R3-F1 is a literal, unrepairable contradiction in the plan itself.** TL:21: "P0 edits no command, skill or agent file". TL:90: "copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`". TL:93 makes the `cmp` an acceptance check. Dropping the copy fails TL:93, and keeping it keeps the breach. No repair satisfies both, so a confirmed finding ends in `ladder-end` or a `dispute` halt (qa.md:280-281).
2. **The target is part of a skill package by the repo's own words.** `tests/commands/test_routing_plugin_parity.py:3-4`: "the guide ships inside the plugin's sc-recommend skill as refs/HOW-WE-WORK.md". The same folder holds `plugins/superclaude/skills/sc-recommend/SKILL.md` (Glob). This undercuts the "skill file means only SKILL.md" reading.
3. **Severity is derived mechanically, not by intent.** The parent's Read-back for B4 checks only that "the quoted text is byte-present in the plan Constraints or a task instruction" (qa.md:61). The reviewer's label is never read (qa.md:79). Any confirmed `yes` is `blocking` (qa.md:81). The inherited cap does not save it: Task 4's new section in the plugin copy is text absent from `$start`, so its origin is `new`, not `inherited` (qa.md:154, qa.md:166).
4. **A second gate exists that does not depend on the Task 4 reviewer.** The diff analysis added this and I adopt it: the managed FINAL reads "the plan's `## Constraints`" and returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310), which ends as `E-ARCHIVE-BLOCKED` (qa.md:286). Two independent model readings each get a chance to read TL:21 literally.
5. **The plan made the conflict; the spec did not.** SRC:220 says only "(no command edits)" and requires "its two mirrored copies". SA-5 (SRC:212) says the guide's "two mirrored copies are updated as the repo requires". The plan widened the wording to "skill or agent". This is drift by the plan from its source, which is why I classed it as drift (C:9).
6. **C's should-fix set covers the plan's other self-contradictions.** R3-F2 (TL:22 vs TL:58), R3-F3 (TL:104 vs TL:45/TL:61, with the FINAL "a later change contradicts it" route, qa.md:310), and R3-F9 (TL:15 "every copy" vs TL:90 leaving the CLAUDE.md copy unchanged) are all internal-consistency defects of the same kind. Neither A nor B checked Constraint-by-task consistency systematically (A:105-118; B's check at B:81-82 missed TL:21 vs TL:90).
7. **C names maintainability risks that later phases inherit.** R3-F4: `make verify-sync` covers skills, agents, commands, hooks and templates, not core (Makefile sections cited at C:81-85), so an added plugin core copy would go stale; `tests/commands/test_impact_command.py:308-309` shows the repo already pins a plugin core copy (CODEGRAPH.md) by test, which is the pattern to follow. R3-F7 and R3-F8 make the P0 test extendable by data, not by rewriting, which AC-1.1 needs (SRC:306: "Each later phase extends the list").
8. **R3-F6's ASCII risk is real.** `tests/core/test_how_we_work_routing_table.py:341` is `test_guide_is_ascii_except_the_ruling_example`, and the spec text that Task 4 will paraphrase uses non-ASCII characters (for example the `→` mapping arrows at SRC:72). A section copied from the spec fails that test.

##### Weaknesses identified in others

1. **B's central claim is false on the text.** B:81-82: "no task instruction breaches the plan's own Constraints". TL:21 against TL:90 and TL:93 is a direct counterexample. B lists "quoted-constraint-breach" as a halt path (B:83) but does not test TL:21 against Task 4.
2. **A never states the Constraints-versus-tasks check.** A:112 says "I found no blocking defect", but A's self-audit (A:105-118) lists no check of the Constraints block against task bodies. A's PASS on R3-F1 is by silence, not by argument.
3. **Both PASS cards rely on a lenient reading they never state.** Neither cites TL:24 or the "no command edits" parenthetical. The diff analysis says the same (diff-analysis.md:141). An unstated lenient reading is not evidence that two independent reviewers will share it.
4. **B's coverage is thin.** Three findings (B:7-57). B missed the Task 6 phase problem (R1-F3 / R3-F5, verified at TL:125 vs SRC:305), the "at most 10" off-spec phrase (TL:112 vs SRC:122), and the installed-path rule (U-001). B's R2-3 is largely redundant, because TL:69 already tells the executor to read the build script, as B's own calibrator notes (B:96).
5. **A's R1-F5 under-weights the precedent.** A says core is not distributed (A:91-93), which is true for the build script (`scripts/build_superclaude_plugin.py:75`). But `plugins/superclaude/core/` already holds six `.md` core files (Glob: RESEARCH_CONFIG, BUSINESS_PANEL_EXAMPLES, RULES, PRINCIPLES, BUSINESS_SYMBOLS, CODEGRAPH), one is pinned by a test (`test_impact_command.py:309`), and the spec's own AC-C1 already excludes `plugins/superclaude/core/WORKER-CONTRACT.md` by name (SRC:252). The spec expects the copy may exist. So the copy is a live option, and R3-F4's sync risk applies.
6. **A's R1-F3 and C's R3-F5 overlap, but A's fix leaves the keying problem open.** A's closed reason format (A:65-66) fixes the phase slot. It does not say how entries are keyed, and line-number keys break on the roughly 121 hit sites at any later edit (C:100-101).

##### Concessions

1. **R3-F1's halt is conditional.** It needs one model reading TL:21 literally. TL:24 and the "no command edits" parenthetical give a lenient reader a clear hook. My 0.6 self-confidence (C:5) was honest about that. I hold "blocking" because the contradiction cannot be repaired inside the plan, two gates can confirm it, and the fix is one sentence. A merged list that grades it "must fix before execution" with a stated probability would capture the same thing.
2. **My card did not cite the managed FINAL route** (qa.md:310, qa.md:286). The diff analysis found it. It strengthens R3-F1, but the omission is mine.
3. **I missed U-001.** A's installed-path finding is real. The repo rule covers core files (`CLAUDE.md:74`, `CLAUDE.md:76`) and says package code "is NOT installed" and "Do not add new references to them from a primitive" (`CLAUDE.md:87`). SRC:59 carries `src/superclaude/cli/install_core.py:36,56,65-70`, and TL:22 tells the executor to restate SRC 2.1-2.3. My self-audit never checked this.
4. **I missed R2-1 (AC-0.8 phantom) and R1-F2 (Task 8 evidence files).** Both are verified: TL:19 versus SRC:298-306, and TL:157 versus TL:47, TL:72 and TL:93, which name no evidence artifacts.
5. **R3-F3 is the general mechanism; A's R1-F1 is the concrete instance.** A found the actual off-spec phrase and I did not. Merge them, with A's instance as the lead evidence. My calibrator was right that R3-F3 is an intra-plan inconsistency (C:226). The concrete part (TL:112 claims "as written in section 2.3" for wording SRC:122 lacks) is drift. The general part is class `none`.
6. **R3-F6 cites the wrong line for the heading slice.** `test_how_we_work_routing_table.py:290` is not the `"### 3.14 "` to `"## 4. "` slice; that slice is at line 1091 (Grep). The ASCII part (line 341) stands.
7. **R3-F1 and R3-F2 share one mechanism, and my split grading is not sharp** (C:224). R3-F2 is weaker because SRC:84 brings the section 3 flags into section 2.3 by reference and SRC:59 says "including its brief template". I keep R3-F2 at should-fix and would accept minor.
8. **R3-F10 is partly covered.** TL:19 already gives AC-C4 to the coordinator at commit time. Keep it minor; it could be folded into R2-2's handoff fix.
9. **R3-F5 duplicates R1-F3.** A's grounding on D3 (a) (SRC:61, SRC:174, SRC:201, SRC:224) is stronger on the phase slot. Merge them as one should-fix with A's reason slots and my keying rule.

##### Positions on diff points

| Point | Preferred variant or merged position | Reason with citation |
|---|---|---|
| S-001 (verdict) | C: FAIL, 1 blocking (R3-F1) | TL:21 vs TL:90/TL:93 cannot both hold; B4 Read-back is byte-presence only (qa.md:61); any confirmed yes is blocking (qa.md:81). |
| S-002 / S-003 (counts, severity spread) | Merged list, deduplicated | Union after merging R1-F3+R3-F5 and R1-F1+R3-F3; A and C each add unique items, B adds R2-1 and R2-2. |
| S-006 (executor rules as evidence) | C | Severity in this executor is derived from qa.md:41-81, so a finding that claims or denies a halt should cite it. |
| S-007 (where a Constraints defect is filed) | Merged: file under the colliding task, cross-reference Constraints | The halt fires in the task's review (qa.md:52); B's `tasks: [0]` is fine for R2-1, which collides with no task. |
| S-008 (coverage) | Merged | No card files on Task 7; A's self-audit (A:110-112) is the only check that its inputs exist. |
| C-001 (Task 6 phase slot) | Merged R1-F3 + R3-F5, should-fix, drift | TL:125 adds "the phase that converts its command"; SRC:305 asks only for "an explicit allowlist with a reason". Use A's reason slots (A:65-66) and C's path/verb/line-text keys (C:108-110). |
| C-002 (Task 3 evidence) | A's evidence, plus SRC:252 and the existing plugin core files | Build script line 75 copies no core; the parity test says plugin installs get no core (`test_routing_plugin_parity.py:3`); but six plugin core files exist and SRC:252 anticipates the copy. Minor. |
| C-003 (Task 5 phrases) | Merged, A's instance leads, should-fix | TL:112 claims "as written in section 2.3" for "at most 10"; SRC:122 says otherwise. General risk per C:52-59. |
| C-004 (verify-sync baseline) | C, minor | TL:33-35 records no verify-sync baseline; TL:96 makes AC-C2 an acceptance check. |
| C-005 (routing-guide tests) | C, should-fix, with the corrected line 1091 | ASCII test at line 341; heading slice at line 1091. Each failure costs a repair round on Task 4. |
| X-001 | C | See Strengths 1-5. A and B rely on an unstated lenient reading. |
| X-002 | C: blocking, conditional, must fix before execution | Two gates (Task 4 QA via qa.md:52/61; managed FINAL via qa.md:310/286); one-line fix restores SRC:220's wording. |
| X-003 | C: should-fix (accept minor) | TL:22 limits the file to 2.1-2.3; TL:58 adds 3.1 flags and a section 6 marker; SRC:59 and SRC:84 weaken but do not remove the conflict, because nothing in 2.3 covers the "from P1" marker. |
| X-004 | Merged: copy is a live option; R3-F4 stays conditional should-fix | A's build-script evidence and C's precedent (`plugins/superclaude/core/` holds six core files; `test_impact_command.py:309`; SRC:252) are both true. Task 3 should cite both; if a copy is added, Task 5 pins it with a byte-identity test. |
| U-001 (installed paths) | Accept A, should-fix, High value | `CLAUDE.md:74,76,87` cover core files and forbid new references to package code; SRC:59 carries `src/superclaude/cli/install_core.py:36,...`; TL:22 says "restates"; the Constraints (TL:17-27) do not carry the rule, so neither per-task QA nor FINAL will catch it. Not blocking: nothing halts, and the defect is in shipped text, not run flow. |
| U-002 (Task 8 evidence files) | Accept A, should-fix | TL:157 needs an evidence file per check; TL:47, TL:72 and TL:93 name none for AC-0.1 to AC-0.3; an absent evidence artifact is `ac-outcome-missing=yes` (qa.md:85). |
| U-003 (AC-0.8 phantom) | Accept B, should-fix, drift | TL:19 names AC-0.8; SRC:298-306 has none. |
| U-004 (live-plan handoff) | Accept B, minor | SRC:238 and SRC:303-304 put results in the phase report; TL:154 does not hand them over. Fold R3-F10's re-staging step into the same fix. |
| U-005 (matrix omissions) | Accept B as note | Bookkeeping only; B says it is harmless here (B:61). |
| U-006 (R3-F1) | C, blocking | As X-002. Fix: "P0 edits no command file, no SKILL.md and no agent file; the only file written under a skills directory is the byte-for-byte copy of HOW-WE-WORK.md that Task 4 makes" (C:26-28). |
| U-007 (R3-F2) | C, should-fix | As X-003. |
| U-008 (R3-F4) | C, should-fix, conditional on Task 3 adding the copy | verify-sync does not cover core; the repo already pins a plugin core copy by test. |
| U-009 (R3-F7) | C, minor | SRC:306 requires each later phase to extend a positive list. |
| U-010 (R3-F8) | C, minor | Template flags drift when P1 changes command flags; the routing guide already has this kind of check (`test_how_we_work_routing_table.py:258`, per C:152). |
| U-011 (R3-F9) | C, minor | TL:15 "every copy" vs TL:90 leaving the CLAUDE.md copy unchanged. |
| U-012 (R3-F10) | C, minor, merge with U-004 | Partly covered by TL:19. |

##### Shared-assumption responses

- **A-009: ACCEPT.** `src/superclaude/cli/install_core.py:30-32` reads `def install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`, so TL:72's keyword call and `ok, msg` unpacking match. The installer copies every `*.md` in `core/` (SRC:59), so the new file is picked up without another change.
- **A-010: ACCEPT.** I ran `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md | awk '$2 != 0'` and it printed nothing; the merge base is `c118b5a5`. The check compares against the merge base, so a later master move without a rebase does not change it, and a rebase moves the base with it. The branch's working-tree changes (git status at session start) do not touch HOW-WE-WORK.md.
- **A-011: ACCEPT.** I ran the SRC:246-253 pipeline read-only on the current tree and it printed nothing. Every file this plan writes with Orca text is excluded by name (SRC:250-253), and Task 4 leaves `src/superclaude/core/CLAUDE.md` unchanged (TL:90), so only an unplanned edit could make AC-C1 fail in Task 4 or Task 8.


## Round 2: Rebuttals

### Variant A Rebuttal
<!-- Source: round2-advocate-a.md (copied in full; headings moved down three levels) -->
#### Round 2 Rebuttal: Variant A advocate (reviewer card 1, analyzer)

Citation key as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` are card lines; `TL:N` is the plan; `SRC:N` is `source.md`; `qa.md:N` and `SKILL.md:N` are the `sc-implement-protocol` executor files under `~/.claude/skills/`; `retry.md:N` is that skill's `refs/retry.md`. `R1-A`, `R1-B`, `R1-C` are the Round 1 statements. I opened every line I cite in this round. Checks I ran in this round are marked "(run today)".

Position in one line: the verdict stays FAIL with R3-F1 as the only blocking finding, and it is not over-graded. None of the three named candidates (R1-F4, R3-F3, R1-F2) reaches a halt that no repair can close. The finding nearest to a second blocker is one no one nominated: R1-F3/R3-F5 (Task 6's phase slot). It and R3-F2 should be fixed in the same plan revision as R3-F1.

##### 1. Responses to criticisms of Variant A

**1.1 "A's PASS missed R3-F1; A never ran the Constraints-against-tasks check"** (R1-B Weakness 1, R1-C Weakness 2, diff-analysis X-001). **Conceded, as in Round 1.** One new fact makes the conflict sharper than any card said: Task 4 does not create a file inside the skill package, it overwrites one. `plugins/superclaude/skills/sc-recommend/` already holds `SKILL.md` and `refs/HOW-WE-WORK.md` (listed today), and the repo test says "the guide ships inside the plugin's sc-recommend skill as refs/HOW-WE-WORK.md" (`tests/commands/test_routing_plugin_parity.py:3-4`, opened today). So TL:90 orders an edit to an existing file in a skill package, and TL:21 says "P0 edits no command, skill or agent file". In plain words, "edits" fits that act.

**1.2 "A's calibrator saw the qa.md:52 route for R1-F1 and R1-F3, and A under-stated it"** (R1-B Weakness 1, quoting A:132). **Half conceded.** For R1-F3 the criticism is right, and section 2.5 shows the route is stronger than my card said. For R1-F1 it is weaker than it looks: a repair exists (section 2.3), so the route ends in a repair round, not a halt.

**1.3 "R1-F3 under-states the edge case: omit the phase and you breach the instruction, invent one and you write a false claim"** (R1-B Weakness 2). **Conceded and extended.** I checked the hits that have no converting phase (run today). Write verbs appear in `src/superclaude/agents/learning-guide.md` (an agent; no phase converts agents), `src/superclaude/skills/task-builder/SKILL.md` and `src/superclaude/skills/sc-crash-recovery/SKILL.md` (no command row converts them), and `src/superclaude/commands/git.md` (never a worker, SRC:61). There are also 25 read-only `gh pr view|list|checks` lines in the scan roots, which TL:125 puts on the list because it names `gh pr` as a verb. For each of these, TL:125's "the phase that converts its command" has no true value. Section 2.5 grades the result.

**1.4 "R1-F5 under-weights the precedent for a plugin core copy"** (R1-C Weakness 5). **Partly conceded.** The precedent is real: `tests/commands/test_impact_command.py:309` reads `plugins/superclaude/core/CODEGRAPH.md` (opened today), and SRC:252 excludes `plugins/superclaude/core/WORKER-CONTRACT.md` by name, so the spec allows a copy. The distribution evidence also stands: `scripts/build_superclaude_plugin.py:75` loops over `["agents", "commands", "hooks", "scripts", "skills"]` only (opened today), and the parity test says "Plugin installs never receive core/ files". Task 3 should cite both sides. I also withdraw my Round 1 proposal to fold R3-F4 into R1-F5 as a conditional clause. R3-F4 has a route inside this run: if Task 3 adds the copy and a later task edits the contract, then Task 3's `cmp` check (TL:74) fails at the end state. The managed FINAL returns `issues` when "a later change contradicts" an acceptance check (qa.md:310), and that ends as `E-ARCHIVE-BLOCKED` (qa.md:286). R3-F4 stands alone at should-fix.

**1.5 "A's reason format leaves the keying problem open"** (R1-C Weakness 6). **Conceded.** The merged fix uses my reason slots (A:65-66) and C's keys: path, verb and stripped line text, never line numbers (C:108-110).

**1.6 "Two tests pin the plugin core copy of CODEGRAPH.md"** (A:95). **Conceded in Round 1.** One test reads the copy (`test_impact_command.py:309`). It checks only that the copy is dollar-safe, not that it is byte-identical to the source.

**1.7 "A judged the routing-guide test risk not worth a finding"** (diff-analysis C-005, A:110-111). **Conceded, upgraded to should-fix.** In Round 1 I graded R3-F6 minor. That is not consistent with my grade for R1-F2, which also costs at most one repair round. `tests/core/test_how_we_work_routing_table.py:341` is the ASCII test, and line 1091 holds the `"### 3.14 "` to `"## 4. "` slice (both opened today). Should-fix, with C's citation corrected from 290 to 1091.

##### 2. Stress test of the consensus

###### 2.1 Is R3-F1 over-graded?

**The best case that it is over-graded.** (a) A halt needs a reviewer to answer yes on question 4 (qa.md:52, qa.md:339). That reviewer reads Task 4, which orders the copy (TL:90), and the Constraints, which allow "their plugin copies" to carry Orca text (TL:24). TL:21's parenthetical also names its source as "no command edits". (b) Nobody runs the copy as a skill. It is a byte mirror of a core document. (c) No card measured how often reviewers read constraints literally.

**Why the grade holds.**
1. **No repair closes it.** If the copy is dropped, AC-0.2's `cmp` (TL:93) is unmet, which is B1. If the copy is kept, the B4 breach stays. The ladder ends in `ladder-end` (qa.md:280). If the adviser disputes the contradictory AC instead (retry.md:72), the run ends in a `dispute` halt (retry.md:107, qa.md:281). The adviser also cannot call the finding "not supported by its own citations", because the quote is byte-present (qa.md:61).
2. **Every review is a fresh subagent.** Reviews run inline only when N≤3 (qa.md:314, SKILL.md:101). This plan has 8 tasks, so every Task 4 review is a fresh subagent working from the closed template, which says "Do not trust the implementer's report" (qa.md:331). That reviewer has not watched the executor reason through TL:24.
3. **Several readers each get a chance.** These include the Task 4 A1 review, any re-review, and the managed FINAL, which reads the Constraints afresh (qa.md:310). The literal reading needs only one yes from all of them.
4. **The literal reading is the plain one.** The target path contains `skills/`, the file already exists in that skill's folder, and the act is an edit (section 1.1).
5. **Expected cost against fix cost.** A yes costs up to five attempts, a halt, and a user Ruling. The fix is one reworded sentence (C:26-28), and it restores the spec's own wording at SRC:220.

**Verdict on 2.1:** not over-graded. The report should say "can halt", not "will halt", as R1-B Weakness 3 asked. Confidence 0.75.

###### 2.2 R1-F4 (spec `src/` paths and evidence ids copied into an installed core file): not blocking

- **No gate in the run reads the rule.** It lives in repo `CLAUDE.md:72-87`, not in the plan's Constraints (TL:17-27). B4 fires only on plan Constraints and task instructions (qa.md:52, SKILL.md:93). B2 fires when a claim is "false against live source" (qa.md:50), but in this checkout `src/superclaude/cli/install_core.py:36` is a true pointer. The managed FINAL reads the plan's Constraints, not repo `CLAUDE.md` (qa.md:310). No test scans core files for `src/superclaude` paths: `tests/skills/test_primitive_dual_surface_lookup.py` has no match for "core" (run today). So the executor finishes cleanly and the defect ships.
- **That is why it is the top should-fix, not a blocker.** It is the only finding where the run passes and the output is wrong in other projects (`CLAUDE.md:74`: "run in OTHER projects, where `src/superclaude/` does not exist"). Two plan lines raise the odds of literal copying. TL:22 says the file "restates only what" sections 2.1-2.3 say. TL:104 makes Task 5 pin "a phrase quoted from `./source.md`" for each rule. Some of the rule text itself names `src/` and skill paths: SRC:59 cites `src/superclaude/cli/install_core.py:36,56,65-70`, and WC-9 lists by path the skills that defer staging (SRC:77, `sk/sc-implement-protocol/refs/managed-workspace.md:36` and others). A faithful restatement has to turn those into `~/.claude/skills/...` paths (`CLAUDE.md:80`).
- **One check outside the plan remains.** The owner reviews the commit before it is made (TL:20, TL:154). That is a human gate, not an executor gate, and nothing in the plan points the owner at this rule.
- **Grade:** should-fix, listed first. Fix: my Constraints line (A:84-85). That line makes the rule quotable, so B4 can then catch a breach.

###### 2.3 R3-F3 with R1-F1 (Task 5's quoted-phrase rule, Tasks 1-2 paraphrase, the FINAL "later change contradicts" rule): not blocking

- **The fan-in instance is repairable.** TL:112 orders the assertion "at most 10" "(as written in section 2.3)". TL:104 orders a phrase quoted from source.md, and SRC:122 says "maximum of 10 inputs" and "never exceeds 10". The test can assert both phrases. TL:104 asks for "at least one" quoted phrase, so both instructions are met. The contract can carry both, because TL:22 forbids a new rule, not a second wording of the same rule. If the executor copies "(as written in section 2.3)" into a test comment, that is a false claim in delivered code (B2, qa.md:50). Rewording the comment closes it.
- **The general paraphrase case is repairable.** If Tasks 1-2 paraphrase a rule, Task 5 can add the spec phrase to the contract. Adding text breaks none of Tasks 1-2's acceptance checks (TL:45, TL:61), which ask for presence, not exact wording.
- **The FINAL route needs three conditions.** The paraphrase must happen, Task 3 must add a plugin copy (which the build-script evidence argues against, section 1.4), and Task 5 must edit the contract without re-copying it. Only then does Task 3's `cmp` (TL:74) fail at the end state (qa.md:310). R3-F4's byte-identity test removes even that route.
- **Grade:** should-fix, drift for the "at most 10" instance (the plan attributes to section 2.3 wording that SRC:122 lacks), none for the general mechanism.

###### 2.4 R1-F2 (Task 8 evidence files): not blocking

TL:157 is an evidence-type acceptance check, unmet only when "the evidence artifact is absent" (qa.md:83-85). The Task 8 executor can save the missing outputs (AC-0.1's three commands, AC-0.2, AC-0.3, AC-C1, AC-C2), and nothing in TL:147-154 forbids it. If it does not, the A1 review raises B1, and the A2 fix pass closes it by saving the files. That costs at most one repair round, so it stays should-fix.

###### 2.5 The nearest second blocker is one nobody nominated: R1-F3 with R3-F5 (Task 6 phase slot)

- **Its structure matches R3-F1.** TL:125 requires each allowlist entry to carry "a one-line reason and the phase that converts its command". For the phase-less hits verified in section 1.3, the executor has two options. It can leave the phase out, which a reviewer can flag as B4 by quoting TL:125. Or it can name one, which is B2 against SRC:61 and SRC:201 ("no `--unattended` mode and no Phase 4 changes"), and against SRC:224 (pr-submit converts only under D3 (b)). The plan also dropped the spec's third category: SRC:305 allows a hit that is "refused under `--unattended`", and TL:125 removes it ("At P0 no command is refused under `--unattended` yet").
- **Why I still grade it should-fix (confidence 0.6).** A truthful entry such as "no converting phase: never a worker (section 4)" answers a question whose premise is false. It does not ignore the instruction. Task 6's acceptance checks (TL:127-131) do not ask for a phase, and AC-0.9 asks only for "an explicit allowlist with a reason" (SRC:305). So a reviewer has a reading that reconciles the plan and the spec. R3-F1 has a weaker reconciling reading, because the act literally edits a file in a skill folder (section 2.1, point 4).
- **R3-F2 is in the same bundle.** Its mechanism is the same. Its cover is better for the section 3.1 flags: SRC:59 assigns the brief template to the file, SRC:84 brings in "every flag section 3 lists as required", and SRC:220 says "a coordinator brief template listing the section 3.1 flags". Its cover is weaker for the "from P1" marker, which TL:58 itself sources to section 6. Should-fix.
- **Consequence.** The plan has to be revised anyway because of R3-F1. That revision should also apply, in the same pass, R3-F2's added clause (C:46-47), the merged Task 6 reason format with its keys, the "at most 10" wording fix, and R1-F4's Constraints line. Each is one to three lines of plan text. If the panel prefers a strict rule (any unrepairable conflict that a reviewer can reach is blocking), then R1-F3/R3-F5 also qualifies, and I would not contest that upgrade.

##### 3. Final severity for every finding

| Merged finding | Cards | Final severity | Class | Basis |
|---|---|---|---|---|
| Constraint TL:21 against the Task 4 skill-folder write (TL:90, TL:93) | R3-F1 | **blocking** | drift | Section 2.1. Fix: C:26-28 |
| Installed-path rule missing from the Constraints | R1-F4 | should-fix (fix first) | none | Section 2.2. Fix: A:84-85 |
| Task 6 phase slot, read-only hits, keying | R1-F3 + R3-F5 | should-fix (same revision as R3-F1) | drift | Sections 1.3 and 2.5. Fix: A:65-66 plus C:108-110 |
| Constraint TL:22 against the Task 2 template (3.1 flags, "from P1") | R3-F2 | should-fix (same revision) | drift | Section 2.5. Fix: C:46-47 |
| "at most 10" and the quoted-phrase rule | R1-F1 + R3-F3 | should-fix | drift (instance), none (mechanism) | Section 2.3 |
| Task 8 evidence files | R1-F2 | should-fix | none | Section 2.4 |
| An added plugin core copy has no sync check | R3-F4 | should-fix (conditional on Task 3 adding it) | none | Section 1.4; the qa.md:310 route inside this run |
| Routing-guide ASCII and heading-slice tests | R3-F6 | should-fix | none | Section 1.7; citation corrected to :341 and :1091 |
| Task 3 deciding evidence | R1-F5 + R2-3 | minor | none | Build script line 75 plus the precedent (section 1.4) |
| Phantom AC-0.8 in the Constraints | R2-1 | minor | drift | No gate reads it; B2 covers delivered text only (qa.md:50); B and C agree |
| Handoff to the live plan, re-staging | R2-2 + R3-F10 | minor | none | SRC:238, SRC:303-304 against TL:154; TL:19 partly covers re-staging |
| Hard-coded negative for `## Unattended mode` | R3-F7 | minor | none | TL:115 against SRC:306 |
| Template flags unchecked against command files | R3-F8 | minor | none | TL:58; precedent at the routing test's line 258 |
| Goal says "every copy" | R3-F9 | minor | none | TL:15 against TL:90 |
| No verify-sync baseline; tests/docs and tests/unit not covered | R3-F11 | minor | none | TL:33-35, TL:96 |
| Coverage-matrix omissions | B matrix_omissions | drop (keep as an appendix note) | none | Bookkeeping; B:61 |
| Task 7 environment (`/opt/Orca`, profile file) | A self-audit; B and C calibrators | drop (note only) | none | A:110-112 checked it, and R1-B Weakness 6 confirmed it again |

##### 4. Shared assumptions A-009, A-010, A-011

- **A-009: ACCEPT (re-checked today).** `src/superclaude/cli/install_core.py:30-32` defines `install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`, which matches TL:72's `ok, msg = install_core_files(target_path=d)`. Line 36 says it copies every `.md` file in `core/`, so the new file needs no other registration in order to install. The `KNOWN_CORE_FILES` entry (lines 13-27) is a separate requirement, met by Task 1.
- **A-010: ACCEPT (re-checked today).** The merge base is `c118b5a59d365b894c5f2caa2270ec9986812934`. `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md | awk '$2 != 0'` printed nothing. No task before Task 4 touches that file (TL:31-74).
- **A-011: ACCEPT, with one refinement (re-checked today).** The full SRC:246-253 pipeline printed nothing (stage exits `0 1 1 1 1 1`). The first stage does find hits, though, and they all sit in `src/superclaude/skills/ccsession-tag/` (`ccsession`, `models.py`, `README.md`), which line 249 excludes. So the scan is clean today only because of its exclusions. Any new hit can come only from this plan's edits outside the five excluded paths.

##### 5. Still-contested points

| ID | My current position | Confidence |
|---|---|---|
| X-001 / S-001 (verdict) | FAIL, one blocking finding (R3-F1) | 0.85 |
| X-002 (is R3-F1 blocking, or over-graded?) | Blocking, recorded as "can halt"; not over-graded (section 2.1) | 0.75 |
| R1-F3 + R3-F5 (second blocker?) | Should-fix, fixed in the same revision; I would not contest an upgrade under a strict rule | 0.60 |
| X-003 / R3-F2 | Should-fix, fixed in the same revision | 0.65 |
| U-001 / R1-F4 | Should-fix, first priority; not blocking because no executor gate reads the rule | 0.80 |
| C-003 / R1-F1 + R3-F3 | Should-fix; repairable inside the run | 0.80 |
| U-002 / R1-F2 | Should-fix; one repair round at most | 0.75 |
| U-008 / R3-F4 | Standalone should-fix, conditional (my Round 1 fold withdrawn) | 0.70 |
| C-005 / R3-F6 | Should-fix (moved up from my Round 1 minor), citation :1091 | 0.65 |
| U-003 / R2-1 | Minor (C still says should-fix) | 0.75 |
| X-004 / C-002 / R1-F5 + R2-3 | Minor; Task 3 cites the build-script line and the precedent | 0.80 |
| A-011 | Accept, noting that the scan's exclusions do the work | 0.90 |


### Variant B Rebuttal
<!-- Source: round2-advocate-b.md (copied in full; headings moved down three levels) -->
#### Round 2 Rebuttal: Variant B advocate (reviewer card 2, qa persona)

Citation key as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` are card lines. `TL:N` is the plan. `SRC:N` is `source.md`. `qa.md:N` and `retry.md:N` are files under `~/.claude/skills/sc-implement-protocol/refs/`. `R1-A`, `R1-B`, `R1-C` and `R2-A` are the earlier statements. I opened every line I cite in this round. Checks I ran in this round are marked "(run today)".

Position in one line: the verdict stays FAIL. R3-F1 is blocking. R1-F3/R3-F5 also meets the blocking test I proposed in Round 1, so I nominate it as a second blocker. It is recorded as "can halt", at lower confidence than R3-F1, because only one kind of gate can catch it. I agree with A's grade on every other finding. I correct two of A's example hits, which are false matches and not write verbs.

##### 1. Responses to criticisms of Variant B

**1.1 "B:81-82 says no task instruction breaches the Constraints. TL:21 against TL:90 shows that is false."** (R1-A Weakness 1, R1-C Weakness 1, diff-analysis X-001.) **Conceded, as in Round 1.** I re-checked it today. TL:21 says "P0 edits no command, skill or agent file". TL:90 says "copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`". That folder holds `SKILL.md` and an existing `refs/HOW-WE-WORK.md` (listed today), so Task 4 edits an existing file inside a skill package.

**1.2 "B listed quoted-constraint-breach as a halt path but did not test TL:21 against Task 4."** (R1-C Weakness 1.) **Conceded.** The method was right and I applied it badly. Section 2 applies the same method strictly to Task 6. That is why I now nominate a finding that my own card missed.

**1.3 "B's coverage is thin: it missed the Task 6 phase slot, the 'at most 10' phrase and the installed-path rule."** (R1-C Weakness 4.) **Conceded.** All three are real, and I verified them in Round 1.

**1.4 "R2-3 is redundant: TL:69 already orders a full read of the build script."** (R1-A Weakness 2, R1-C Weakness 4, my calibrator at B:96.) **Conceded.** R2-3 merges into A's R1-F5 at minor. The useful evidence is `scripts/build_superclaude_plugin.py:75`, not my empty hunk. The empty hunk H4 belongs in the report's notes on evidence gaps, not in the finding list.

**1.5 "R2-1 is over-graded."** (R1-A Weakness 3.) **Conceded in Round 1. I keep it at minor, against C's should-fix.** TL:19 still says "AC-0.8 is a P1 check (section 7.3)", and SRC:298-306 has no AC-0.8. No gate can act on that sentence. B2 covers "delivered text or code" (qa.md:50), and plan text is not delivered. The managed FINAL returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310), and no edit can violate a scope note about a check that does not exist. The class stays drift.

**1.6 "B's PASS rests on a lenient reading it never states."** (R1-C Weakness 3, diff-analysis X-001.) **Conceded.**

**1.7 "B missed Task 7's environment risk."** (My calibrator, B:99.) **Conceded.** I checked it in Round 1: both Orca paths exist, so it needs a note only.

**1.8 "B's self-audit cites a 452-line spec."** (B:100.) **Conceded.** `wc -l source.md` prints 451 (run today).

**1.9 Points that still stand.** No one disputed B's structural checks. Every pytest target that Tasks 3 and 4 name exists, and source-order execution satisfies the Depends-on graph (B:68-74). R2-2 also stands at minor, and I accept C's proposal to fold R3-F10's re-staging step into it. Its value is the handoff itself: the phase report lives in the live plan (SRC:238), AC-0.6 and AC-0.7 results must appear "in the phase report" (SRC:303-304), and Task 8 hands nothing over (TL:154).

##### 2. Ruling on R1-F3 / R3-F5 (the Task 6 phase slot)

###### 2.1 Can TL:125 be met for every hit? No.

TL:125 says that each hit "must be either allowed by WC-9 ... or listed on an explicit allowlist in the test, with a one-line reason and the phase that converts its command." That is a closed choice between two options, and the second option needs a phase. I grouped today's hits by file (run today; 109 matching lines across the three scan roots with a plain regex).

| Group | Files and lines (run today) | Is there a true "phase that converts its command"? |
|---|---|---|
| (a) A command on the never-as-worker list, with no phase at all | `commands/git.md:67` (`/sc:git commit --smart-commit`) and `:75` (`/sc:git merge ...`) | **No.** Section 4 commands "are never dispatched as workers and get no `--unattended` mode" (SRC:188). `/sc:git` is on the list (SRC:61, SRC:193). |
| (b) pr-submit | `commands/pr-submit.md:30` and 45 lines under `skills/sc-pr-submit-protocol/` (46 of the 109 lines) | **Only a conditional one.** P4 converts pr-submit "only if D3 (b) is chosen" (SRC:224, SRC:234). The approved text says it gets "no `--unattended` mode and no Phase 4 changes" (SRC:201). A bare "P4" is false. "P4, only if D3 (b) is adopted" is true. |
| (c) A file that no command owns | `skills/sc-crash-recovery/SKILL.md:4` (`Bash(git stash *)` in allowed-tools); `skills/task-builder/SKILL.md` (a standalone skill; WC-9 says its CLI-mode `git add -A` "is refused", SRC:77) | **No.** No command file exists for crash-recovery (Glob today: `commands/` has `task.md`, but no `crash-recovery.md` and no `task-builder.md`). For task-builder, the true category is the spec's "refused under `--unattended`" (SRC:305), which TL:125 removes ("At P0 no command is refused under `--unattended` yet"). |
| (d) Read-only lines and false matches | 26 `gh pr view\|list\|checks\|diff\|status` lines; `task-builder/SKILL.md:1087, 2169` (`git merge-base`, read-only); `agents/learning-guide.md:3, 34, 42, 50` ("throu**gh pr**actical" contains `gh pr`) | It depends. A read-only line inside a command that some phase converts (for example auggie-review, P2) has a phase. A false match has neither a write verb nor a meaningful phase. |

**Correction to R2-A section 1.3.** A says "Write verbs appear in `src/superclaude/agents/learning-guide.md`". They do not. Its four hits are the substring `gh pr` inside "through practical". The two `git merge` hits in task-builder are `git merge-base`, which is read-only. This makes the finding wider, not weaker. A scanner without word boundaries produces hits that fit neither of TL:125's two categories. The solid phase-less examples are groups (a) and (c), plus group (b) unless the entry uses the conditional wording.

###### 2.2 What QA does with each choice

The executor has three options for a hit in groups (a) or (c).

1. **Write a truthful "none".** For example: "phase: none; never a worker (section 4)". A reviewer is asked "does the diff violate ... an explicit task instruction?" (qa.md:339) and can quote "with a one-line reason and the phase that converts its command" from TL:125. The Read-back checks only that "the quoted text is byte-present in the plan Constraints or a task instruction" (qa.md:61). It is. Any confirmed yes is blocking (qa.md:81). The inherited cap does not apply, because Task 6 creates the test text, so its origin is `new` (qa.md:166).
2. **Invent a phase.** That is B2, "a claim in delivered text or code is false against live source" (qa.md:50). The anchor does not even need the spec. Task 1 writes the never-as-worker list, including `/sc:git` and `/sc:pr-submit`, into `WORKER-CONTRACT.md` (TL:45). That file is live source in the same tree. SRC:201 and SRC:188 also contradict an invented phase.
3. **Add a third category.** For example: "never a worker". This leaves TL:125's "either ... or" choice, so it is the same B4 breach as option 1.

**No repair closes it.** No entry text for groups (a) and (c) is both true and gives a phase. A repair can only swap a B4 breach for a B2 false claim. If the adviser disputes the finding or the instruction, the run ends in a `dispute` halt (retry.md:72, retry.md:107, qa.md:281). Otherwise the ladder ends in `ladder-end` (qa.md:280). One point that no one has raised also applies to R3-F1: once a reviewer flags the finding, every later reviewer must mark it "resolved, open or regressed from the diff" (qa.md:333). An unchanged "none" entry reads as `open`, so a lenient re-reviewer cannot clear a finding that a strict one raised.

**Would an invented phase pass?** It passes only if no Task 6 reviewer checks the phase values against the contract or the spec. In that case the run completes and ships a false classification into the test that every later phase extends (SRC:306: "Each later phase extends the list"). The P1 plan would then build on a test that says pr-submit or git converts at some phase, which contradicts D3 (a). That is a silent defect, so it is worse than a halt.

###### 2.3 Grade: second blocker, recorded as "can halt" (confidence 0.6)

In Round 1, I proposed this test: a plan defect is blocking when it opens a halt that no in-run repair can close. R1-F3/R3-F5 meets both mechanical conditions that make R3-F1 blocking. The breach is quotable, so it passes the Read-back. And no delivered text is both true and compliant. To grade R3-F1 blocking and this finding should-fix, the panel would have to weigh reviewer leniency. Under the panel's own method, reviewer leniency does not set severity: the reviewer's label is never read (qa.md:79).

A's reason for keeping it at should-fix is that a truthful "none" answers a question whose premise is false, and that SRC:305 asks only for "a reason" (R2-A section 2.5). That cover is real, and it is why my confidence is 0.6 and not higher. But it lives in the spec, not in the review input. The reviewer gets the task brief and the plan Constraints (qa.md:323-324), and nothing in either one says a hit may lack a phase. R3-F1 has better cover inside the review input: TL:24 names "their plugin copies".

Two facts pull in opposite directions, and I state both.
- **Weaker than R3-F1:** only the per-task reviews of Task 6 can catch it. The managed FINAL returns `issues` for an unmet AC, missing evidence, a later contradiction, a violated plan Constraint or a failed log (qa.md:310). A breached task instruction is not on that list. Task 6's acceptance checks (TL:128-131) never mention the phase, so B1 cannot fire either.
- **Stronger than R3-F1:** R3-F1 is one copied file. Here every phase-less entry is its own quotable breach, and with pr-submit counted as an unconditional entry, that is about half of all hits.

If the panel decides that one gate type is not enough for blocking, I accept "should-fix, must be fixed in the same revision as R3-F1". The verdict and the work are the same either way.

**Fix.** Restore the spec's categories in TL:125, and use C's keys (path, verb and stripped line text, never line numbers; C:108-110):
1. allowed by WC-9;
2. refused or deferred under `--unattended` in the phase that converts its command (name the phase);
3. never a worker (section 2.1 list, section 4, D3 (a)), with no phase;
4. no command converts this file (standalone skill or agent), with a reason;
5. read-only or a false match. Better still, scan with word boundaries and leave out read-only subcommands (`git merge-base`, `gh pr view|list|checks|diff|status`).

###### 2.4 Why R3-F2 stays should-fix under the same test

TL:22 limits the contract to what sections 2.1 to 2.3 say. Task 2 must list the section 3.1 flags and mark `--report-dir` "from P1" (TL:58, AC at TL:62). For the flags, a delivered text that is both true and compliant does exist. Section 2.3 itself requires "every flag section 3 lists as required" (SRC:84), so listing those flags restates section 2.3. The section TL:22 points the reviewer to removes the conflict. Only the "from P1" label lacks that cover. It is one label in one template, and section 2.3 does carry the idea of a phase ("where the command accepts it at this phase", SRC:84). R3-F2 has the FINAL route, because TL:22 is a Constraint. Under a purely mechanical rule, I would accept blocking for the label alone. I grade it should-fix at 0.6, fixed in the same revision with C's added clause (C:46-47).

##### 3. Severity for every finding (agree or dispute R2-A section 3)

| Merged finding | R2-A grade | My position | Basis |
|---|---|---|---|
| R3-F1: TL:21 against the Task 4 skill-folder write (TL:90, TL:93) | blocking | **Agree**, recorded as "can halt" | Two gate types (qa.md:52/61, qa.md:310/286); unrepairable; plus the qa.md:333 point in section 2.2 |
| R1-F4: installed-path rule missing from the Constraints | should-fix, fix first | **Agree** | Nothing in the run halts on it, and it ships broken text; A's Constraints line (A:84-85) makes it quotable |
| R1-F3 + R3-F5: Task 6 phase slot | should-fix | **Dispute: blocking, can halt (0.6)**; I accept should-fix in the same revision as a fallback | Section 2 |
| R3-F2: TL:22 against the Task 2 template | should-fix | **Agree** (0.6) | Section 2.4 |
| R1-F1 + R3-F3: "at most 10" and the quoted-phrase rule | should-fix | **Agree** | TL:104 asks for "at least one" quoted phrase, so the test can assert both "at most 10" (TL:112) and "maximum of 10 inputs" (SRC:122). A repair closes it. |
| R1-F2: Task 8 evidence files | should-fix | **Agree** | An absent evidence file is unmet (qa.md:85), but the executor can save it, so one repair round at most |
| R3-F4: no sync check if Task 3 adds a plugin core copy | should-fix, conditional | **Agree** | The route through qa.md:310 ("a later change contradicts it") exists only if the copy is added |
| R3-F6: routing-guide ASCII and heading-slice tests | should-fix | **Agree** | Test line 341 and slice line 1091; Task 4's own run catches them, which costs a repair round |
| R1-F5 + R2-3: Task 3 deciding evidence | minor | **Agree** | Section 1.4 |
| R2-1: phantom AC-0.8 | minor | **Agree** (my own finding, downgraded) | Section 1.5 |
| R2-2 + R3-F10: handoff to the live plan, re-staging | minor | **Agree** | Section 1.9 |
| R3-F7, R3-F8, R3-F9, R3-F11 | minor | **Agree** | No route to a halt; all maintainability or wording issues |
| B matrix_omissions | drop, keep as an appendix note | **Agree** | Bookkeeping only (B:61) |
| Task 7 environment | drop, note only | **Agree** | Both paths exist (checked in Round 1) |

##### 4. Shared assumptions

- **A-009: ACCEPT (re-checked today).** `src/superclaude/cli/install_core.py:30-32` defines `install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`. That matches TL:72's keyword call and its `ok, msg` unpacking. Line 36 says the function copies every `.md` file in `core/`. `KNOWN_CORE_FILES` (lines 13-27) does not list `WORKER-CONTRACT.md` yet. Task 1 adds it, which is a separate requirement.
- **A-010: ACCEPT (re-checked today).** The merge base is `c118b5a59d365b894c5f2caa2270ec9986812934`. The AC-0.3 deletion check on `src/superclaude/core/HOW-WE-WORK.md` printed nothing. No task before Task 4 touches that file (TL:31-74).
- **A-011: ACCEPT, with A's refinement (re-checked today).** The full SRC:246-253 pipeline printed nothing (stage exits `0 1 1 1 1 1`). The first stage does find matches, but only in `src/superclaude/skills/ccsession-tag/` (`ccsession`, `models.py`, `README.md`), which SRC:249 excludes. The scan is clean today because of that exclusion. Any new hit can come only from this plan's edits outside the five excluded paths.

##### 5. Still-contested points

| ID | My position | Confidence |
|---|---|---|
| X-001 / S-001 (verdict) | FAIL | 0.90 |
| X-002 / U-006 (R3-F1) | Blocking, recorded as "can halt"; not over-graded | 0.80 |
| C-001 (R1-F3 + R3-F5) | Second blocker, recorded as "can halt". The instruction cannot be met truthfully for groups (a) and (c). Fallback: should-fix in the same revision. | 0.60 |
| R2-A section 1.3 example hits | Corrected: the learning-guide hits and the task-builder `git merge-base` hits are false matches. The solid phase-less hits are git.md, crash-recovery, task-builder, and pr-submit unless its entry uses the conditional wording. | 0.90 |
| X-003 / U-007 (R3-F2) | Should-fix, fixed in the same revision. I would accept blocking for the "from P1" label only under a purely mechanical rule. | 0.60 |
| U-001 (R1-F4) | Should-fix, fix first | 0.80 |
| C-003 (R1-F1 + R3-F3) | Should-fix; a repair closes it inside the run | 0.80 |
| U-002 (R1-F2) | Should-fix | 0.75 |
| U-008 (R3-F4) | Should-fix, conditional on Task 3 adding the copy | 0.70 |
| C-005 (R3-F6) | Should-fix, citations at lines 341 and 1091 | 0.65 |
| U-003 (R2-1) | Minor, drift (C still says should-fix) | 0.75 |
| U-004 + U-012 (R2-2 + R3-F10) | Minor, merged | 0.75 |
| C-002 / X-004 (R1-F5 + R2-3) | Minor, A's evidence | 0.85 |
| A-011 | Accept; the scan is clean only because of its exclusions | 0.90 |


### Variant C Rebuttal
<!-- Source: round2-advocate-c.md (copied in full; headings moved down three levels) -->
#### Round 2 Rebuttal: Variant C advocate (reviewer card 3, refactorer)

Citation key as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` are card lines. `TL:N` is the plan. `SRC:N` is `source.md`. `qa.md:N` and `retry.md:N` are files under `~/.claude/skills/sc-implement-protocol/refs/`. `R1-A`, `R1-B`, `R1-C`, `R2-A` and `R2-B` are the earlier statements. I opened every line I cite in this round. Checks I ran in this round are marked "(run today)".

Position in one line: the verdict is FAIL with R3-F1 as the only blocking finding. B is right that TL:125 cannot be met truthfully for some hits, and that a strict Task 6 reviewer could halt the run on it. I still grade R1-F3/R3-F5 should-fix, to be fixed in the same plan revision as R3-F1, because it can be caught at only one gate and the executor can write a true answer into the slot. I concede R2-1 to minor and accept every other grade in R2-A section 3.

##### 1. Responses to criticisms of Variant C

**1.1 "R3-F1 overstates certainty: C says a strict reviewer 'ends the run'"** (R1-B Weakness 3). **Conceded.** C:15-17 does say "strict", but the merged report should say "can halt", not "will halt". The halt needs one reviewer to answer yes to question 4 (qa.md:339). The grade does not change. No repair can satisfy both TL:21 and TL:90/TL:93: drop the copy and the `cmp` check at TL:93 fails, keep it and the breach stays. The ladder then ends in `ladder-end` (qa.md:280), or an adviser dispute ends in a `dispute` halt (retry.md:72, retry.md:107).

**1.2 "C under-cited its own blocker: the managed FINAL is a second gate"** (R1-A Weakness 7, diff-analysis X-002 point 7). **Conceded, as in Round 1.** TL:21 is a `## Constraints` item. The managed FINAL reads the plan's Constraints and returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310), and that ends in `E-ARCHIVE-BLOCKED` (qa.md:286). I also accept B's added point: once any reviewer flags the finding, every later reviewer must mark it "resolved, open or regressed from the diff" (qa.md:333). An unchanged copy reads as `open`.

**1.3 "R3-F3 has the wrong deviation class and overstates the trap"** (R1-A Weakness 4, R1-B Weakness 5, my calibrator at C:226). **Conceded.** The class is drift for A's concrete instance: TL:112 says "at most 10" is "as written in section 2.3", but SRC:122 says "maximum of 10 inputs". The class is none for the general mechanism. I also withdraw one claim in my card. C:55-57 says Task 5's "only way out is to edit WORKER-CONTRACT.md, a file Task 5 does not own". Task 5 does not own that file, but nothing in TL:104-119 forbids Task 5 to add to it. Adding a spec phrase breaks none of Tasks 1-2's acceptance checks, which ask for presence, not exact wording (TL:45, TL:61). So a repair closes it, as R2-A section 2.3 says. The FINAL route through "a later change contradicts it" (qa.md:310) needs three things at once: a paraphrase, a plugin copy from Task 3, and a contract edit without re-copying. Should-fix.

**1.4 "R3-F6 cites the wrong line and is over-graded"** (R1-A Weakness 5, R1-B Weakness 4). **Citation conceded.** The `"### 3.14 "` to `"## 4. "` slice is at `tests/core/test_how_we_work_routing_table.py:1091`, and a second slice, `"### 3.13 "` to `"### 3.14 "`, is at line 819 (grep, run today). The ASCII test is at line 341. **The grade question is settled:** A moved R3-F6 up to should-fix (R2-A section 1.7), and B agrees (R2-B section 3).

**1.5 "R3-F4 depends on a copy the evidence argues against; fold it into R1-F5"** (R1-A Weakness 6). **Settled in my favour.** A withdrew the fold (R2-A section 1.4) because there is a route inside the run: if Task 3 adds the copy and a later task edits the contract, Task 3's `cmp` check (TL:74) fails at the end state, and the FINAL returns `issues` (qa.md:310). R3-F4 stays a standalone should-fix that matters only if Task 3 adds the copy.

**1.6 "R3-F5 under-states the edge case: leave the phase out and you breach the instruction; invent one and you write a false claim"** (R1-B Weakness 2). **Conceded.** Section 2 rules on it. I also correct my own card. C:97-99 says the scan "also matches hits in agents ... that no phase converts". That is wrong. The only agent hits are four lines in `src/superclaude/agents/learning-guide.md` (lines 3, 34, 42 and 50), where "throu**gh pr**actical" contains `gh pr` (grep, run today). They are false matches, not write verbs. B made the same correction to A (R2-B section 2.1). My counts of 40 `gh pr` hits and about 121 hit sites came from the grounding hunk's regex. B counts 109 lines with a plain regex. The count depends on the regex, and no grade depends on the count. The correction supports my fix: classify hits by path, verb and stripped line text, and scan with word boundaries (C:108-110).

**1.7 "X-004: C treats an added plugin core copy as a live option"** (diff-analysis X-004). **Kept, and now agreed.** SRC:252 excludes `plugins/superclaude/core/WORKER-CONTRACT.md` by name, so the spec expects a copy may exist. `scripts/build_superclaude_plugin.py:75` shows that core is not distributed. A and B both now say Task 3 should cite both facts (R2-A section 1.4, R2-B section 1.4).

**1.8 "R2-1 (phantom AC-0.8) is minor, not should-fix"** (R2-A and R2-B tables, against my Round 1 grade). **Conceded.** TL:19 is plan text, and B2 covers only "delivered text or code" (qa.md:50). No edit can violate a scope note about a check that does not exist, so the FINAL's Constraints check (qa.md:310) cannot fire either. Minor, class drift.

**1.9 R3-F2.** In Round 1 I said I would accept minor. Both A and B grade it should-fix, and I keep should-fix. The section 3.1 flags have cover: section 2.3 itself says "every flag section 3 lists as required" (SRC:84). The "from P1" marker (TL:58) has weaker cover, and TL:22 is a Constraint, so the FINAL can read it (qa.md:310).

##### 2. Ruling on B's second blocker (R1-F3 + R3-F5, the Task 6 phase slot)

###### 2.1 Can the executor meet TL:125 without inventing a phase? Not literally.

TL:125: each hit "must be either allowed by WC-9 ... or listed on an explicit allowlist in the test, with a one-line reason and the phase that converts its command." I checked the hits that have no true phase (run today):

| Hit | Why no phase converts it |
|---|---|
| `src/superclaude/commands/git.md:67` (`/sc:git commit --smart-commit`) and `:75` (`/sc:git merge feature-branch --interactive`) | `/sc:git` is never a worker and gets no `--unattended` mode (SRC:61, SRC:188, SRC:193). These lines are usage examples of the slash command, not shell git calls, but a plain `git commit` / `git merge` match finds them. |
| `src/superclaude/skills/sc-crash-recovery/SKILL.md:4` (`Bash(git stash *)` in `allowed-tools`) | No command file exists: `commands/` has `git.md`, `task.md` and `pr-submit.md`, but no `crash-recovery.md` (Glob, run today). The phrase "its command" has nothing to refer to. |
| `src/superclaude/skills/task-builder/SKILL.md:408` (`git add .dev/tasks`) and `:2237` (CLI-mode `git add -A`) | No `task-builder.md` command exists. WC-9 says the line 2237 call "is refused" (SRC:77), which is the spec's third category, "refused under `--unattended`" (SRC:305). TL:125 removes that category ("At P0 no command is refused under `--unattended` yet"). |
| pr-submit hits | A bare phase is false: pr-submit gets "no `--unattended` mode and no Phase 4 changes" (SRC:201). A conditional phase is true: "P4 only if D3 (b) is chosen" (SRC:224, SRC:234). |

For the first three groups, the only true value for the slot is "none". "The phase that converts its command" assumes that such a phase exists. So the instruction cannot be met both literally and truthfully. Would "no phase converts it" satisfy it? It fills the slot with a true value, but it names no phase. Whether that counts as compliance is up to the reviewer. **I concede B's factual claim.**

###### 2.2 Does qa.md:52 make the gap a halt? It makes a halt reachable, not certain.

- qa.md:52 lets B4 fire on "an explicit task instruction", and TL:125 is one.
- The Read-back checks only that "the quoted text is byte-present in the plan Constraints or a task instruction" (qa.md:61). TL:125's text will pass.
- Task 6 creates the test, so the origin is `new` and the inherited cap does not apply (qa.md:169). Any confirmed yes is blocking (qa.md:81).
- A blocking finding fails the attempt. It does not halt by itself. A halt comes only when the ladder cannot close the finding (qa.md:280), or when the adviser disputes it because the AC is "contradictory or infeasible" (retry.md:72, retry.md:107). No repair can supply a true phase, so a strict yes that persists does end in a halt.

So the mechanism is the same as R3-F1's: one reviewer's yes, then a conflict no repair can close.

###### 2.3 Why I still grade it should-fix (confidence 0.6)

B's Round 1 test says a defect is blocking when it opens a halt that no in-run repair can close. This finding passes that test. I do not think the test alone is enough to grade a plan before it runs, because any instruction that can be read strictly passes it. The grade should also weigh how plain the breach is and how many gates can catch it. On both counts this finding is clearly weaker than R3-F1.

1. **The kind of conflict differs.** In R3-F1, two plan texts order and forbid the same act. Every possible output breaches one of them (TL:21 against TL:90 and TL:93), and the diff does what TL:21 forbids in plain words: it writes a file under `skills/`. Here, one instruction assumes something that is false for some hits, and a true null value fills its slot. To answer yes, a reviewer must decide that an honest "none" is a breach, not the correct answer. That is a harder yes to give.
2. **Only one gate can catch it.** R3-F1 can be caught by the Task 4 review and by the managed FINAL. This finding can be caught only by the Task 6 reviews. The FINAL returns `issues` for an unmet AC, missing evidence, a later change that contradicts an AC, a violated plan Constraint, or a failed log (qa.md:310). A breached task instruction is not on that list. Task 6's acceptance checks (TL:128-131) never mention the phase, so the FINAL's unmet-AC route cannot fire either. B agrees (R2-B section 2.3). If the Task 6 A1 review passes, nothing else reads the slot.
3. **The executor can put the reason in the diff.** It can write each entry as "phase: none; never a worker (source.md section 4)", and keep the same reasons in `./artifacts/ac-0.9-hits.txt`, which TL:125 already requires. The reviewer receives the diff (qa.md:326). In R3-F1, nothing the executor writes can change where TL:90 puts the copy.
4. **B's "stays open" point (qa.md:333) raises the cost once the finding is triggered, not the chance that it is triggered.** It applies only after a first strict yes.

Two facts keep my confidence at 0.6. B's mechanical test is met. And the other outcome is a silent defect: an executor that invents a phase writes a false claim (B2) against the never-as-worker list that Task 1 puts in `WORKER-CONTRACT.md` (TL:45). That false claim then ships into the test that every later phase extends (SRC:306). Neither fact makes this a likely halt, but both make it a must-fix.

**Ruling:** should-fix, fixed in the same revision as R3-F1. The report records: "can halt, through the Task 6 review only". If the panel adopts B's mechanical test as its rule, the finding is blocking, and I would not contest that. The verdict (FAIL) and the work (one plan revision) are the same either way.

**Fix:** use B's five categories (R2-B section 2.3) and my keys: repo-relative path, verb and stripped line text, never line numbers (C:108-110). Scan with word boundaries. Record slash-command usage lines (`/sc:git commit`) and read-only subcommands (`git merge-base`, `gh pr view|list|checks|diff|status`) as "not a write call", so they are not counted as write-verb hits.

##### 3. Final grade for every finding

I accept R2-A's section 3 table with one change: R2-1 is minor (section 1.8), as A already has it.

| Merged finding | Cards | Final grade | Class | My position |
|---|---|---|---|---|
| TL:21 against the Task 4 skill-folder copy (TL:90, TL:93) | R3-F1 | **blocking**, recorded as "can halt" | drift | Confirm. Two gates (qa.md:52/61, qa.md:310/286). Fix: C:26-28 |
| Installed-path rule missing from the Constraints | R1-F4 | should-fix, fix first | none | Confirm. No gate in the run reads repo `CLAUDE.md` (qa.md:310 reads plan Constraints); the defect ships into other projects |
| Task 6 phase slot, read-only and false-match hits, keying | R1-F3 + R3-F5 | should-fix, same revision as R3-F1, "can halt (Task 6 review only)" | drift | Confirm should-fix against B's blocking (section 2) |
| TL:22 against the Task 2 template | R3-F2 | should-fix, same revision | drift | Confirm (section 1.9) |
| "at most 10" and the quoted-phrase rule | R1-F1 + R3-F3 | should-fix | drift (instance), none (mechanism) | Confirm (section 1.3) |
| Task 8 evidence files | R1-F2 | should-fix | none | Confirm. A missing evidence file is unmet (qa.md:85), but Task 8 can save it in one repair round |
| An added plugin core copy has no sync check | R3-F4 | should-fix, applies only if Task 3 adds the copy | none | Confirm (section 1.5) |
| Routing-guide ASCII and heading-slice tests | R3-F6 | should-fix | none | Confirm, with citations at lines 341, 819 and 1091 |
| Task 3 deciding evidence | R1-F5 + R2-3 | minor | none | Confirm; cite the build-script line 75 and SRC:252 |
| Phantom AC-0.8 | R2-1 | minor | drift | Confirm (conceded from should-fix) |
| Live-plan handoff and re-staging | R2-2 + R3-F10 | minor | none | Confirm the merge |
| Hard-coded negative for `## Unattended mode` | R3-F7 | minor | none | Confirm |
| Template flags unchecked against command files | R3-F8 | minor | none | Confirm |
| Goal says "every copy" | R3-F9 | minor | none | Confirm |
| No verify-sync baseline; tests/docs and tests/unit not covered | R3-F11 | minor | none | Confirm |
| Coverage-matrix omissions | B matrix_omissions | drop; keep as an appendix note | none | Confirm |
| Task 7 environment | A self-audit; B and C calibrators | drop; note only | none | Confirm; A and B both found the paths present |

##### 4. Shared assumptions A-009, A-010, A-011

- **A-009: ACCEPT (re-checked today).** `src/superclaude/cli/install_core.py:30-32` defines `install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`. That matches TL:72's keyword call and its `ok, msg` unpacking. Line 36 says the function copies all `.md` files from `src/superclaude/core/`, so the new file installs with no other change.
- **A-010: ACCEPT (re-checked today).** The merge base is `c118b5a59d365b894c5f2caa2270ec9986812934`. `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md | awk '$2 != 0'` printed nothing. No task before Task 4 touches that file (TL:31-74).
- **A-011: ACCEPT, with A's and B's refinement (re-checked today).** The full SRC:246-253 pipeline printed nothing, with stage exits `0 1 1 1 1 1`. The first stage does match lines, so the scan is clean only because line 249 excludes `src/superclaude/skills/ccsession-tag/`. Any new hit in Tasks 4 or 8 can come only from this plan's edits outside the five excluded paths.

##### 5. Still-contested points

| ID | My position | Confidence |
|---|---|---|
| X-001 / S-001 (verdict) | FAIL | 0.90 |
| X-002 / U-006 (R3-F1) | Blocking, recorded as "can halt"; not over-graded | 0.80 |
| C-001 (R1-F3 + R3-F5, B's second blocker) | Should-fix, fixed in the same revision as R3-F1, recorded as "can halt through the Task 6 review only". TL:125 cannot be met literally and truthfully for the git.md, crash-recovery and task-builder hits, but a true "none" fills the slot and only one gate can catch it. I would not contest blocking if the panel adopts B's mechanical test. | 0.60 |
| C-001 example hits | The agent hits are false matches (learning-guide "through practical"); my card's claim about agent hits is withdrawn. The solid hits with no phase are git.md:67/75, crash-recovery SKILL.md:4 and task-builder SKILL.md:408/2237, plus pr-submit unless the entry uses the conditional wording | 0.90 |
| X-003 / U-007 (R3-F2) | Should-fix, fixed in the same revision | 0.65 |
| U-003 (R2-1) | Minor, drift (conceded from should-fix) | 0.80 |
| C-003 (R1-F1 + R3-F3) | Should-fix; repairable inside the run; my "only way out" claim withdrawn | 0.80 |
| U-008 (R3-F4) | Standalone should-fix, applies only if Task 3 adds the copy | 0.70 |
| C-005 (R3-F6) | Should-fix; citations at lines 341, 819 and 1091 | 0.70 |
| U-001 (R1-F4) | Should-fix, fix first | 0.80 |
| A-011 | Accept; the scan is clean only because of its exclusions | 0.90 |


## Round 2.5: Invariant Probe (fault-finder)
Round 2.5 ran because depth=standard does not skip it (SK:1478-1481 skips it only at depth quick). The fault-finder's table is copied in full below. It found 18 items: 8 ADDRESSED and 10 UNADDRESSED (1 HIGH, 5 MEDIUM, 4 LOW) (INV:24-26). The advocates did not see these items; none of them was debated.

<!-- Source: invariant-probe.md (copied in full; headings moved down three levels) -->
#### Invariant Probe Results
##### Round 2.5 — Fault-Finder Analysis
| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | sufficiency_challenge | "Fix R3-F1 and the should-fixes, and the plan passes per-task QA and the managed FINAL." Hidden premise: the test logs the plan orders saved and cited as evidence show no failure. | UNADDRESSED | HIGH | **Falsifier (run today).** The Task 1 wider baseline command (TL:35) `uv run pytest tests/core tests/commands tests/recommend tests/cli -q -rf` ends `8 failed, 3009 passed, 5 skipped, 1 xpassed`. The failures were in `tests/cli/eval/test_ban_import_rule.py` (3), `tests/cli/eval/test_claude_process_adapter.py` (2) and `tests/cli/test_verify_sync_hooks.py` V1/V2/V7. TL:35 saves "its full output" to `./artifacts/t1-baseline-wider.txt`, and TL:48 makes that file a Task 1 AC, so T1's `complete` line will cite it. Task 4 (TL:95) re-runs the same suite. qa.md:310 tells the managed FINAL to return `issues` when "a log cited on a task's latest `complete` line shows a failure at its outcome line". That ends in `E-ARCHIVE-BLOCKED` (qa.md:286, managed-workspace.md:61), and no task can repair it without going out of scope. qa.md:294 ("return `issues` only for a blocking defect") points the other way, so the outcome depends on which line the FINAL reviewer follows, the same "one literal reader" mechanism that made R3-F1 blocking. tests/skills is clean today (`608 passed`), so the AC-C3 logs are safe; only the wider log is exposed. No card or advocate ran either baseline. **Gate enumeration, start to archive (inline, no branch-trace.md):** (1) parse and flag ban, SKILL.md:50-52; (2) managed path-shape and Detection, SKILL.md:55-56 and managed-workspace.md:7-12 (needs return-contract.yaml, see INV-004); (3) Location resolution, managed-workspace.md:18-27; (4) ledger and `PLAN:` pin, managed-workspace.md:31,37-43 (see INV-005); (5) task enumeration, `## Task N` gives T1-T8, `## Phase` headings are not tasks, Depends-on ignored, SKILL.md:71-79; source order satisfies TL:52,80,102,123,145; (6) AC QUALIFY, every task has an "Acceptance criteria:" block, SKILL.md:85; (7) Q0 private-index snapshot and pin, SKILL.md:110-115; (8) Q1/Q2 touched set, which includes Bash-modified files, SKILL.md:118-125 (see INV-002); (9) Q3 review by a fresh subagent because N=8>3, SKILL.md:101 and qa.md:314, against the Constraints, SKILL.md:93 and qa.md:52; (10) Q4 derivation, qa.md:56-81; (11) Q5 fix, repair, ladder, halts, qa.md:245-247 and 280-281; (12) Q6 extras, never the gate, SKILL.md:132,152; (13) archive gate: --print-state, fresh FINAL, re-check, append FINAL, managed-workspace.md:49-61, with the FINAL rules at qa.md:294,310; (14) helper: contract 1.1, success or partial, pin matches disk, every task complete, FINAL pass bound to state, Linux renameat2 (archive_workspace.py:322-330,346,402-427; managed-workspace.md:73). Gate 13 is where INV-001 bites. **Fix:** in TL:35 and TL:95, state that pre-existing failures are expected. Cite the per-test comparison files (t4-wider-compare.md) as evidence, not the raw logs. List the 8 failing test ids in the plan as the accepted baseline. |
| INV-002 | state_variables | Running the plan's test commands changes no tracked file, so each task's diff holds only its own edits. | UNADDRESSED | MEDIUM | My read-only probe run of the TL:35 wider suite rewrote the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json` (mtime 06:46:59 during the run; its diff changed host, python and timing values). I restored it with `git restore --worktree --source=HEAD`. The writer is `tests/cli/eval/test_perf_home_setup.py:32,103-117`. Tasks 1 and 4 both run that suite (TL:35, TL:95). The Q1 touched set covers files "modified via ... Bash" (SKILL.md:118), so the change reaches the Task 1 and Task 4 diffs. A reviewer can then answer `harmful-effect` yes: the task "writes ... tracked ... data" outside its declared outputs (qa.md:51). managed-workspace.md:35 tells the executor to remove byproducts, but it names caches and temp files, not tracked evidence. If the change is not reverted, Task 8's list of "every repo path this plan created or changed" (TL:154) must either include junk perf data or be false (B2). Each case costs a repair round at least. Fix: add `--deselect tests/cli/eval/test_perf_home_setup.py` or a `git restore` of that path after each wider run, and say so in TL:35 and TL:95. |
| INV-003 | guard_conditions | `make verify-sync` is clean today, or drift is only possible (C-004, R3-F11 graded minor). | ADDRESSED | LOW | It is certainly not clean today. `.claude/` holds only `settings.json` and `cache/` (`ls -la .claude`), so verify-sync reports every skill MISSING (Makefile:174-176), and `tests/cli/test_verify_sync_hooks.py:140-141` (V1, which runs the real `make verify-sync`) fails today. Task 4 runs `make sync-dev` (TL:90) before its AC-C2 check (TL:96), and sync-dev builds those copies (Makefile:126-157), so AC-C2 should pass. Side effect: the V1/V2/V7 tests flip from fail to pass between the TL:35 baseline and the TL:95 re-run, which the "no passed test now failing" comparison tolerates. The debate's minor grade is right, but its stated reason ("may already drift") understates the facts. |
| INV-004 | guard_conditions | The package passes managed detection when `/sc:implement` is invoked. | ADDRESSED | LOW | Today the package holds only the plan and `source.md` (`ls` of `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/`). Detection requires a sibling `return-contract.yaml` with `contract_version: "1.1"`, the same slug and `status: success` or `partial` (managed-workspace.md:10; archive_workspace.py:322-330); without it the run stops at `E-MANAGED-INVALID`. The workflow writes the contract in Wave 5, after this reflect (sc-workflow-protocol SKILL.md:58,66), and a reflect FAIL never changes `status` (SKILL.md:60; refs/return-contract.md:21). The sibling package `...20261102-231950/return-contract.yaml` shows `status: success` with a reflect FAIL under `unresolved`. This holds only if the workflow run reaches Wave 5. The slug matches the detection regex (16-character subject). |
| INV-005 | state_variables | Someone applies the agreed plan fix (reword TL:21, plus the should-fixes) before execution. | UNADDRESSED | MEDIUM | No transcript names who edits the plan, or when. The workflow is forbidden to do it: "never edit, delete, or regenerate `<id>.md` from findings" (sc-workflow-protocol SKILL.md:60, and "Will Not ... modify the plan from reflect findings", SKILL.md:74). The executor pins the plan hash: before the first `T<id>: start` line a changed hash is re-pinned, and afterwards any change is `E-PLAN-CHANGED`, with "no repair, no new pin" (managed-workspace.md:43). So the fix works only as a hand edit by the person (or a fresh `/sc:workflow` package) before the first `/sc:implement` start. An edit made after an interrupted first run is fatal to that package. The merged report should state this owner and timing. |
| INV-006 | guard_conditions | The Orca install and profile that Task 7 reads exist, and AC-C6 prints the expected value. | ADDRESSED | LOW | Run today: the AC-0.7 grep (SRC:342) lists `out/shared/nested-worker-depth.js`, `out/cli/bundled-skill-guides.js` and one `out/main/chunks/...` file. The AC-C6 grep (SRC:278) prints exactly `"nestedWorkerMaxDepth":1` for the one profile, `local-default`. `orca` and `orca-ide` are on PATH. TL:140-141 can pass. Residual: the `path:line` cites will point into minified bundles with very long lines. |
| INV-007 | state_variables | Only the executor writes in this worktree during the run, so HEAD, the plan and the touched-file diffs stay its own. | UNADDRESSED | MEDIUM | git status shows uncommitted edits by other sessions in this same worktree (` M .dev/orca-command-refactor/decisions/APPROVED.md`, ` M .dev/orca-command-refactor/specs/orca-worker-contract-spec.md`), and eight other agents are active in this session. managed-workspace.md:85 says non-cooperating checkout writers are "unsupported; not claimed". The ladder halts on `head-moved` (qa.md:280), and the spec itself requires a separate worktree for `/sc:implement` when other writers may write (SRC:79, WC-11). A commit by a sibling agent during the run, or an edit to the package, ends the run in `head-moved` or `E-PLAN-CHANGED`, whatever the plan text says. Fix: run the plan with no other writer in this worktree, or in its own worktree. |
| INV-008 | count_divergence | The fixed counts agree across the plan and the spec: 12 ready commands, 7 never-as-worker, 11 report checks, three reason texts plus a prefix for four conditions. | ADDRESSED | LOW | 12: TL:58 names adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, reflect, release-split, tdd, troubleshoot and workflow, which match the SRC:141-152 rows and the "(12)" in SRC:136. 7: TL:45 matches SRC:61 (six from section 4, plus pr-submit under D3). 11: TL:154 lists AC-0.1, 0.2, 0.3, 0.7, 0.9 and AC-C1 to C6, which is 5+6=11, as TL:157 says. Guard: SRC:60 has four conditions (case 1, case 2, copies disagree, case 3), three exact texts for the first three, and the bare `guard refused:` prefix for case 3, which TL:38 and TL:106 copy correctly. 45 = 12+27+6 (SRC:132) and 39 = 12+27 (SRC:236) both hold. |
| INV-009 | count_divergence | "About 121 write-verb hits" is a stable number that Task 6's "list every hit" (TL:125, TL:130) can be checked against. | ADDRESSED | LOW | Run today with a plain `grep -o` over the three scan roots: 137 occurrences (gh pr 44, gh api 31, git add 30, git merge 9, git update-ref 7, git commit 6, git stash 4, git worktree add 3, git push 2, git worktree remove 1). R2-B counts 109 lines (round2-advocate-b.md:31), and R3-F5 counts about 121 (round2-advocate-c.md:19). The unit (line or occurrence) and the matcher are unfixed in TL:125, so a FINAL reviewer with a different regex can find "unlisted" hits. The merged fix keys entries by path, verb and stripped line text, with word boundaries (round2-advocate-c.md:64; round2-advocate-b.md:66-71), which closes this, provided the fix also names the regex in the plan. |
| INV-010 | interaction_effects | The merged Task 6 category "read-only or a false match" fits the plan's own definition of a `gh api` post. | UNADDRESSED | MEDIUM | TL:125 defines a post as "a `gh api` call with `-X POST`, `--method POST`, `-f`, `-F` or `--input`". Six hits are reads that pass `-F` with `--method GET`: `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:53-55` and `refs/augment-poll.md:19-21` (run today). Under the plan's definition they are posts. Under the merged fix's fifth category they are reads. Classifying them as reads contradicts a quotable task instruction (B4, qa.md:52), and classifying them as posts makes the test assert a false fact (B2, qa.md:50). This is the same one-gate mechanism as the 2-1 Task 6 item, and no advocate saw it, because the debate covered only `gh pr view/list/checks` and `git merge-base`. Fix: reword the definition to "a `gh api` call whose method is not GET". |
| INV-011 | collection_boundaries | The P0 assertion "no file in `src/superclaude/commands/` has an `## Unattended mode` section" (TL:115) checks something real. | UNADDRESSED | LOW | Today zero such sections exist in `src/superclaude/commands` or `plugins/superclaude/commands` (grep exit 1), so the assertion holds. But a wrong or relative scan path that matches zero files also passes it. The plan's negative checks cover only the contract rules (TL:119) and the audit's tmp root (TL:129); neither proves that the real commands directory was scanned. Fix: also assert that the scan found at least 45 command files (SRC:132). |
| INV-012 | collection_boundaries | An empty `./artifacts/ac-c4-index.txt` proves AC-C4 on the final index. | ADDRESSED | LOW | TL:158 makes the empty file the pass state. TL:154 runs the check before `git add .dev/tasks`, so it does not see the final index. Staging `.dev/tasks` cannot add a `.claude/` path, and TL:19 gives the commit-time re-run to the coordinator. The empty-file evidence is weak but correct. R3-F10 and R2-2 (minor) cover the restaging. |
| INV-013 | collection_boundaries | The "no plugin copy added" outcome of Task 3 leaves no dangling check. | ADDRESSED | LOW | The cmp check in TL:74 is conditional ("if a copy was added"). AC-C1 excludes the plugin copy by name either way (SRC:252). Task 8's list says "any plugin copy from Task 3" (TL:154). `plugins/superclaude/core/` holds six core `.md` files plus `__init__.py` today, and no CLAUDE.md or HOW-WE-WORK.md, which matches TL:69. |
| INV-014 | interaction_effects | Task 5's rule (a quoted spec phrase per WC id that "carries that rule's meaning, not only its label") is compatible with TL:22's "only the IronClaude-specific rule" for the worker-session duties. | UNADDRESSED | MEDIUM | SRC:59 lists the IronClaude-specific worker-session rules: outcome mapping, WC-5's P0 override, top-level only, ask only when the brief allows it. It names none for WC-12, WC-13 or heartbeats. Yet TL:45 requires WC-2 to WC-13 in the file, and TL:105 requires "each WC identifier ... with its rule's key phrase". WC-12's body is Orca verb behaviour taken from Orca's own guide: "runs `check` ... `consumer_fenced` ... `worker_done`" (SRC:80, citing CAPS:66-67). TL:46 forbids copying Orca verb syntax into the worker-session part. A safe reading exists (assert "at natural checkpoints", SRC:80, and "at the cadence its preamble sets", SRC:78), but a strict reviewer can quote TL:22, a Constraint, so the FINAL route at qa.md:310 is also open. If the agreed R1-F1/R3-F3 fix is worded as "copy the spec's wording", it collides outright: WC-10 carries a fixed cadence, "5 minutes in current preambles" (SRC:78), and TL:46 bans any "fixed heartbeat cadence". No debate file mentions WC-12, WC-10 or the cadence (grep of all rounds). Fix: the phrase rule must say "a phrase", exempt the worker-session duties from verbatim copying, and name the phrase to pin for WC-12, WC-13 and heartbeats. |
| INV-015 | interaction_effects | The R1-F4 installed-path Constraint and the quoted-phrase rule can both be met. | UNADDRESSED | LOW | Several spec rule sentences embed repo paths: SRC:59 (`src/superclaude/cli/install_core.py:36,56,65-70`) and SRC:77 (WC-9's list of skills that defer staging, all `sk/...:N`). Both rules can be met only if Task 5 pins path-free phrases and Tasks 1-2 translate paths to `~/.claude/...`. The merged fixes for R1-F4 (A:84-85) and R1-F1 are drafted separately, and neither says so. The risk is low, because the phrase choice is free. |
| INV-016 | interaction_effects | Task 5 can safely add missing spec phrases to WORKER-CONTRACT.md, the repair route that made R1-F1/R3-F3 should-fix (round2-advocate-a.md:47-49; round2-advocate-c.md:13). | UNADDRESSED | LOW | qa.md:52 also counts as B4 "editing text the plan reserves for another task", and Tasks 1-2 own the file's content (TL:37, TL:54). Nobody tested the repair against this clause. It is low because the per-task reviewer gets only Task 5's brief plus the Constraints (qa.md:355), and the FINAL list has no task-instruction breach (qa.md:310). Exposure remains through SKILL.md:119 (a drive-by file, minor) and through Task 3's cmp check if a plugin copy exists (already noted by R2-A). Putting the phrase rule in Tasks 1-2 removes the route. |
| INV-017 | interaction_effects | Rewording TL:21 to "P0 edits no command file" creates no new literal breach. | UNADDRESSED | LOW | Tasks 3 and 4 run `make sync-dev` (TL:69, TL:90), which writes `.claude/commands/sc/*.md` copies (Makefile:131-136). A literal reader could call those command-file edits. They are gitignored, so they are absent from the Q0 snapshot and `git diff "$start"` (SKILL.md:110-111, 123), and the reviewer never sees them. The original TL:21 had the same exposure for `.claude/skills/`. Harmless, but the reworded line can say "no command source file under `src/superclaude/commands/`". |
| INV-018 | guard_conditions | The Task 6 2-to-1 grade (should-fix, not blocking) holds once the merged categories are adopted. | ADDRESSED | LOW | All three advocates agree that the fix goes in the same plan revision as R3-F1 (round2-advocate-a.md:61; round2-advocate-b.md:64; round2-advocate-c.md:62), so the verdict and the work do not depend on the grade. Only Task 6's reviews can catch it, because the FINAL list has no task-instruction breach (qa.md:310). The grade is safe only if the revision also fixes INV-010's `-F` definition, which is the same family. |
##### Summary
- Total findings: 18.
- ADDRESSED: 8 (INV-003, INV-004, INV-006, INV-008, INV-009, INV-012, INV-013, INV-018).
- UNADDRESSED: 10. HIGH: 1 (INV-001). MEDIUM: 5 (INV-002, INV-005, INV-007, INV-010, INV-014). LOW: 4 (INV-011, INV-015, INV-016, INV-017).
- Effect on the merged verdict: FAIL still holds, and R3-F1 is still the right blocker. The sufficiency claim, "fix R3-F1 plus the should-fixes and the plan passes", is false as stated. INV-001 opens an archive block at the managed FINAL that no fix in the consensus touches. INV-002 and INV-010 add quotable defects the per-task QA can raise. INV-005 and INV-007 are run conditions that the merged report must state.
- Method note: every count and baseline above was run today, read-only, in this worktree. The one exception is the INV-002 side effect: my test run rewrote one tracked file, and I restored it at once with `git restore --worktree --source=HEAD`. It was the only change.


## Round 3: Final Arguments
Skipped. The configured depth is standard, and Round 3 runs only at depth deep. No forced round was needed, because all three taxonomy levels are covered after Round 2 (see "Taxonomy Tagging and Coverage Gate"; SK:1416-1421 forces a round only when a level has zero coverage).

## Shared-Assumption Responses and Omission Check
The promoted shared assumptions are A-009, A-010 and A-011 (DA:120-130). A-001 to A-008 are STATED by at least one card and were not promoted (DA:112-119), so they are not debate points. The omission rule (SK:996-1002) requires each advocate to answer every promoted A-NNN with ACCEPT, REJECT or QUALIFY.

| A-NNN | Advocate A | Advocate B | Advocate C |
|---|---|---|---|
| A-009 | R1: ACCEPT (R1a:85); R2: ACCEPT, re-checked (R2a:87) | R1: ACCEPT (R1b:76); R2: ACCEPT, re-checked (R2b:98) | R1: ACCEPT (R1c:82); R2: ACCEPT, re-checked (R2c:92) |
| A-010 | R1: ACCEPT (R1a:86); R2: ACCEPT (R2a:88) | R1: ACCEPT (R1b:77); R2: ACCEPT (R2b:99) | R1: ACCEPT (R1c:83); R2: ACCEPT (R2c:93) |
| A-011 | R1: ACCEPT (R1a:87); R2: ACCEPT with refinement: the scan is clean only because SRC:249 excludes `ccsession-tag/` (R2a:89) | R1: ACCEPT (R1b:78); R2: ACCEPT with A's refinement (R2b:100) | R1: ACCEPT (R1c:84); R2: ACCEPT with A's and B's refinement (R2c:94) |

**[OMISSION] flags: none.** Every advocate answered A-009, A-010 and A-011 in both rounds.

Non-A-point gap noted for completeness (not an omission under SK:996-1002): Advocate C's Round 1 table has no row for S-004, S-005 or S-009 (R1c:53-57). C's Round 2 grades table covers S-004 through its class column and S-005 through the "Coverage-matrix omissions" row (R2c:70-87). S-009 is never addressed by C; it is decided by the A and B majority.

## Taxonomy Tagging and Coverage Gate
Levels follow SK:136-170: L1 is surface (presentation, naming, format), L2 is structure (organization, component, interface, dependency), L3 is state mechanics (state, guard, boundary, validation rule, transition). When a point fits more than one level, the higher one wins (SK:174).

| Point | Level | Why (diff-analysis line) |
|---|---|---|
| S-001 | L3 | The verdict turns on whether a Constraint breach moves the run into a halt (DA:25, DA:57) |
| S-002 | L1 | A count of card items (DA:26) |
| S-003 | L2 | How findings are organized across severity tiers (DA:27) |
| S-004 | L2 | How findings are organized across deviation classes (DA:28) |
| S-005 | L1 | An extra card block (DA:29) |
| S-006 | L3 | Severity derived from the executor's validation rules (DA:30) |
| S-007 | L1 | Which `tasks:` label a Constraints finding carries (DA:31) |
| S-008 | L2 | Which plan components the findings reach (DA:32) |
| S-009 | L1 | Calibration metadata (DA:33) |
| C-001 | L3 | The audit's classification guard and its match boundaries (DA:43) |
| C-002 | L2 | Plugin distribution of a core module; dependency on the build script (DA:44) |
| C-003 | L3 | A test validation rule and the FINAL "a later change contradicts it" state (DA:45) |
| C-004 | L3 | Baseline state before the first edit (DA:46) |
| C-005 | L3 | The ASCII validation rule and fixed heading-slice boundaries (DA:47) |
| X-001 | L3 | Halt transition (DA:57) |
| X-002 | L3 | A Constraint guard against a mandated write (DA:58) |
| X-003 | L3 | A scope Constraint guard against Task 2's content (DA:59) |
| X-004 | L2 | Plugin distribution of a core module (DA:60) |
| A-009 | L2 | The installer's interface signature (DA:120) |
| A-010 | L3 | Precondition state of the merge-base diff (DA:121) |
| A-011 | L3 | Precondition state of the AC-C1 scan (DA:122) |

Coverage per level, after Round 2:

| Level | Points | Debated in | Covered |
|---|---|---|---|
| L1 | 4 (S-002, S-005, S-007, S-009) | R1a:54, 56, 58, 60; R1b:47, 49, 51, 53; R1c:54, 56 | yes |
| L2 | 6 (S-003, S-004, S-008, C-002, X-004, A-009) | R1a:54-55, 59, 62, 69, 85; R1b:47-48, 52, 57, 69, 76; R1c:57, 59, 66, 82 | yes |
| L3 | 11 (S-001, S-006, C-001, C-003, C-004, C-005, X-001, X-002, X-003, A-010, A-011) | R1a:53, 57, 61, 63-68, 86-87; R1b:46, 50, 54-56, 68-72, 77-78; R1c:53, 55, 58, 60-65, 83-84; R2a:25-61; R2b:27-75; R2c:27-62 | yes |

Taxonomy gate (SK:1405-1414): all three levels have at least one addressed point, so the gate passes and no forced round is triggered.

## Scoring Matrix
One row per S, C, X and A point (9 + 5 + 4 + 3 = 21). Confidence follows SK:1511-1526: unanimous 90-100%, majority 60-89%, split 50%, plus 10 points when the losing advocates conceded, never 100% unless every advocate conceded, and lower when the evidence is only moderate. "Agreed" uses SK:1429-1432: unanimous, or a 2-of-3 majority.

| Point | Level | Winner | Confidence | Agreement | Evidence summary |
|---|---|---|---|---|---|
| S-001 | L3 | C (FAIL, 1 blocking) | 95% | Unanimous; A and B conceded | All three choose FAIL with R3-F1 as the one blocker (R1a:53, R1b:46, R1c:53), and A and B concede their PASS (R1a:36, R1b:35). Held in Round 2 (R2a:95, R2b:106, R2c:100); not 100% because the halt is "can halt", not "will halt" (R2a:36). |
| S-002 | L1 | C (its 11 findings are the core of the merged list) | 90% | Unanimous | All three want one deduplicated list (R1a:54, R1b:47, R1c:54). A withdrew its Round 1 claim that C's count was inflated (R2a:15, R2a:21), and all three grade the same 15 merged rows (R2a:67-81, R2b:81-92, R2c:72-86). |
| S-003 | L2 | C (1 blocking, then should-fix, then minor) | 80% | Majority (A, C) | All agree on exactly one adjudicated blocker (R2a:67, R2b:81, R2c:72), giving 1 blocking, 7 should-fix and 7 minor (R2a:67-81, R2c:72-86). B would add C-001 as a second blocker (R2b:83). |
| S-004 | L2 | C (R3-F3's general mechanism re-classed none) | 90% | Unanimous; C conceded the class fix | Drift goes to R3-F1, R3-F2, the "at most 10" instance, the Task 6 phase slot and R2-1; everything else is none (R1a:55, R1b:48, R2c:72-86). C conceded R3-F3's general part is class none (R1c:43, R2c:13). |
| S-005 | L1 | B (kept as an appendix note) | 90% | Unanimous | A keeps it as an appendix (R1a:56), B and C as a note (R1b:49, R1c:71). All three drop it from the finding list (R2a:82, R2b:93, R2c:87). |
| S-006 | L3 | C (cite executor rules as severity evidence) | 95% | Unanimous; A and B adopted C's method | A: "C's method is right" (R1a:57); B: "C's method" (R1b:50); C (R1c:55). The executor derives severity mechanically and never reads the reviewer's label (qa.md:79). |
| S-007 | L1 | C (file under the task the defect collides with) | 90% | Unanimous | A, B and C all file a Constraints defect under the colliding task (R1a:58, R1b:51, R1c:56); `tasks: [0]` stays valid for R2-1, which collides with no task (R1c:56). |
| S-008 | L2 | A (Task 7 environment kept as a note from A's self-audit) | 90% | Unanimous | Only A checked Task 7's inputs (VA:110-112; R1c:57). B re-confirmed the paths exist (R1b:31). All three keep it as a note, not a finding (R2a:83, R2b:94, R2c:88). |
| S-009 | L1 | No variant (no action) | 75% | Majority (A, B); C silent | A and B say calibration changes no severity (R1a:60, R1b:53). C never addresses S-009 (R1c:53-57, R2c:70-87). |
| C-001 | L3 | C (R3-F5 merged with A's R1-F3; should-fix, drift) | 65% | Majority 2-1 on severity (A, C should-fix; B blocking); unanimous on the merge and the class | All merge the two findings as drift (R1a:61, R1b:68, R1c:58). A and C grade should-fix at 0.60 (R2a:97, R2c:102); B grades blocking at 0.60 and accepts should-fix as fallback (R2b:108, R2b:64). **Dissent recorded: B (blocking).** |
| C-002 | L2 | A (R1-F5, with B's R2-3 merged in) | 92% | Unanimous; B conceded | A names the deciding line, `build_superclaude_plugin.py:75` (R1a:62). B concedes R2-3 is subsumed (R1b:38, R2b:15); C adds SRC:252 and the existing plugin core files (R1c:59). All minor (R2a:75, R2b:89, R2c:80). |
| C-003 | L3 | A (the "at most 10" instance leads; C's mechanism kept) | 92% | Unanimous; C conceded the lead | All merge A's instance with C's mechanism (R1a:63, R1b:70, R1c:60). C concedes and withdraws its "only way out" claim (R1c:43, R2c:13). Should-fix by all (R2a:71, R2b:85, R2c:76); TL:112 against SRC:122 confirmed. |
| C-004 | L3 | C (R3-F11, minor) | 92% | Unanimous; A conceded | A concedes it noted but did not file the gap (R1a:46); B and C agree (R1b:71, R1c:61). All minor (R2a:81, R2b:92, R2c:86). |
| C-005 | L3 | C (R3-F6, should-fix; citations moved to lines 341, 819 and 1091) | 90% | Unanimous after Round 2 | A moved from minor to should-fix (R2a:21); B and C grade should-fix (R2b:88, R2c:79). C conceded the wrong line-290 citation (R1c:44, R2c:15). |
| X-001 | L3 | C (FAIL) | 95% | Unanimous; A and B conceded | Same verdict in all three statements (R1a:66, R1b:54, R1c:63), with A's and B's concessions (R1a:36-44, R1b:35-37). TL:21 against TL:90 and TL:93 confirmed by the orchestrator. |
| X-002 | L3 | C (R3-F1 blocking, recorded as "can halt") | 90% | Unanimous | All grade it blocking (R2a:96 at 0.75, R2b:107 at 0.80, R2c:101 at 0.80). Two gates can confirm it: Task 4 QA (qa.md:52, qa.md:61) and the managed FINAL (qa.md:310, leading to qa.md:286). |
| X-003 | L3 | C (R3-F2 should-fix, drift) | 80% | Unanimous on the grade; each advocate's own confidence is 0.60-0.65 | All grade should-fix in the same revision (R2a:98, R2b:110, R2c:104). SRC:84 brings the section 3 flags into section 2.3, but the "from P1" marker has no such cover (R2b:75). Set below the unanimous band because the evidence is moderate (SK:1522). |
| X-004 | L2 | A (core is not distributed), with C's precedent noted | 85% | Majority (A, B) on the winner; all three agree to cite both facts | A and B side with the build-script evidence (R1a:69, R1b:57); C calls the copy a live option (R1c:66). By Round 2 all three say Task 3 cites both facts (R2a:15, R2c:21). |
| A-009 | L2 | No variant (assumption accepted) | 95% | Unanimous | ACCEPT by all three in both rounds (R2a:87, R2b:98, R2c:92); the signature is recorded at DA:128. |
| A-010 | L3 | No variant (assumption accepted) | 95% | Unanimous | ACCEPT by all three in both rounds (R2a:88, R2b:99, R2c:93); DA:129. |
| A-011 | L3 | No variant (accepted, with the refinement that the scan is clean only because of its exclusions) | 93% | Unanimous | ACCEPT with the same refinement by all three (R2a:89, R2b:100, R2c:94); the `ccsession-tag` exclusion is at SRC:249. |

Diff points won: A 4 (S-008, C-002, C-003, X-004), B 1 (S-005), C 12 (S-001 to S-004, S-006, S-007, C-001, C-004, C-005, X-001 to X-003), no variant 4 (S-009, A-009 to A-011).

### Supplementary: unique contributions (outside the convergence denominator)

U-NNN items are not counted in the convergence formula (SK:1386-1387). Their outcomes feed the refactor plan.

| U-NNN | Card item | Outcome | Evidence |
|---|---|---|---|
| U-001 | R1-F4 installed-path rule | should-fix, fix first; unanimous | R2a:68, R2b:82, R2c:73 |
| U-002 | R1-F2 Task 8 evidence files | should-fix; unanimous | R2a:72, R2b:86, R2c:77 |
| U-003 | R2-1 phantom AC-0.8 | minor, drift; unanimous after C conceded | R2a:76, R2b:90, R2c:81 |
| U-004 | R2-2 live-plan handoff | minor; merged with U-012; unanimous | R2a:77, R2b:91, R2c:82 |
| U-005 | B's matrix_omissions | appendix note; unanimous | R2a:82, R2b:93, R2c:87 |
| U-006 | R3-F1 | blocking (see X-002) | R2a:67, R2b:81, R2c:72 |
| U-007 | R3-F2 | should-fix (see X-003) | R2a:70, R2b:84, R2c:75 |
| U-008 | R3-F4 plugin core copy has no sync check | should-fix, only if Task 3 adds the copy; unanimous | R2a:73, R2b:87, R2c:78 |
| U-009 | R3-F7 hard-coded negative | minor; unanimous | R2a:78, R2b:92, R2c:83 |
| U-010 | R3-F8 template flags unchecked | minor; unanimous | R2a:79, R2b:92, R2c:84 |
| U-011 | R3-F9 Goal says "every copy" | minor; unanimous | R2a:80, R2b:92, R2c:85 |
| U-012 | R3-F10 re-staging | minor; merged into U-004; unanimous | R2a:77, R2b:91, R2c:82 |

## Convergence Assessment
Formula (SK:1385-1388): convergence = agreed points / (S + C + X + A).

- Denominator: S 9 + C 5 + X 4 + A 3 = 21 (DA:10-11, DA:135-139; A counts only the three promoted points, DA:120-122)
- Agreed points: 21 (17 unanimous; 4 by a 2-of-3 majority: S-003, S-009, C-001, X-004)
- Points resolved: 21 of 21
- Alignment: 21 / 21 = **1.00 (100%)**
- Round 1 alignment: 21 of 21 already had a majority (for example C-005: B and C should-fix, R1b:72, R1c:62); Round 2 alignment: 21 of 21
- Threshold: 80%
- Taxonomy gate: passed (L1, L2 and L3 all covered)
- Termination: stable majority above threshold for 2 consecutive rounds, all levels covered (SK:1440-1443); Round 3 is not part of depth standard
- Unresolved points: none
- Contested but agreed: C-001 (severity 2-1 for should-fix; B dissents with blocking at 0.60, R2b:108)
- Status before the invariant gate: would be CONVERGED (agreement at or above threshold and taxonomy covered, SK:1493)
- **Final status: BLOCKED_BY_INVARIANTS** (see next section; SK:1496)

## Invariant-Probe Gate
Gate rule (SK:1455-1468): after Round 2.5, any row with Status UNADDRESSED and Severity HIGH blocks convergence whatever the agreement score; UNADDRESSED MEDIUM rows are logged as warnings; LOW rows need no action.

Rows read from the probe table (INV:3-22; summary INV:24-26):
- UNADDRESSED and HIGH: 1 (INV-001, INV:5)
- UNADDRESSED and MEDIUM: 5 (INV-002 INV:6, INV-005 INV:9, INV-007 INV:11, INV-010 INV:14, INV-014 INV:18)
- UNADDRESSED and LOW: 4 (INV-011, INV-015, INV-016, INV-017; INV:15, INV:19-21); no action
- ADDRESSED: 8 (INV:25); no action

```
CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

```
WARNING: 5 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-002, INV-005, INV-007, INV-010, INV-014
These items do not block convergence but should be reviewed.
```

What the blocking item says, in plain words: the Task 1 wider baseline (TL:35) fails today with 8 failed tests, Task 1's acceptance criterion makes that log evidence (TL:48), and the managed FINAL returns `issues` when "a log cited on a task's latest `complete` line shows a failure at its outcome line" (qa.md:310). That can end in `E-ARCHIVE-BLOCKED` (qa.md:286), although qa.md:294 points the other way (INV:5). No advocate saw or debated it, so the debate's claim that fixing R3-F1 and the should-fixes is enough is not established (INV:27).

Effect on later steps: the 100% diff-point agreement stands as the convergence score, the status is BLOCKED_BY_INVARIANTS, and the merged verdict must carry INV-001 as an unadjudicated item. The run is non-interactive, so no further debate round is dispatched; the block is handed on to base selection and the refactor plan.
