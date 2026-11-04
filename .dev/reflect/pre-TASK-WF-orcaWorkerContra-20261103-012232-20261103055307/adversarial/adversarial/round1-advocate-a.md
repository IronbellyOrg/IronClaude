# Round 1 Advocate: Variant A (reviewer 1, analyzer, PASS)

Citation key as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` are card lines; `TL:N` is the plan; `SRC:N` is `source.md`; `qa.md:N` is `~/.claude/skills/sc-implement-protocol/refs/qa.md`; `retry.md:N` is the same skill's `refs/retry.md`. I opened every line cited below in this round. Checks I ran today are marked "(run today)".

## Position summary

Variant A's five findings are the best-grounded set. They include the only check against a repo ABSOLUTE RULE (R1-F4) and the only concrete instance of an off-spec phrase the tests must pin (R1-F1). But A's PASS verdict is wrong. I concede that Variant C's R3-F1 is a real conflict that no repair can close, and that two separate executor gates can turn it into a halt. The merged verdict should be FAIL with R3-F1 as its single blocking item, fixed by rewording one constraint, and A's findings should anchor the should-fix list.

## Steelman

**Variant B (qa, PASS).** B is the leanest card, and each of its claims was checked. R2-1 is a real false statement: "AC-0.8" occurs only at TL:19, and the spec's P0 rows run AC-0.1 to AC-0.7 and then AC-0.9 (SRC:298-305), with P1 starting at AC-1.1 (SRC:306). B is the only card that explicitly walks the executor's halt paths in its self-audit (B:80-85) and the only one that records coverage-matrix omissions (B:58-64). Its PASS has a defensible reading: TL:24 names "their plugin copies" as allowed carriers of Orca text. The plugin `refs/HOW-WE-WORK.md` is a byte copy of a core document, not an authored skill file. The constraint's own citation, "no command edits" (TL:21, quoting SRC:220), suggests the narrower meaning.

**Variant C (refactorer, FAIL).** C is the most thorough card and the only one that derives severity from the executor's actual rules rather than from a guess about how lenient a reviewer will be (C:14-16, C:23-24, C:65). It spotted that the plan made the spec's wording wider: SRC:220 says only "(no command edits)", while TL:21 says "no command, skill or agent file". That change is what creates the conflict with TL:90. C's fix is one sentence (C:26-28). Its self-confidence of 0.6 openly says the result depends on a reviewer reading the constraint literally (C:211-212). Its other ten findings cover Tasks 1-6 and 8, and several cite tests that I or the calibrator could confirm (Makefile verify-sync scope, `test_retired_docs_absent.py:40`, `test_how_we_work_routing_table.py:341`).

## Strengths claimed

1. **R1-F1 names the concrete defect behind C's general R3-F3.** TL:112 tells Task 5 to assert "at most 10" "(as written in section 2.3)". That claim is false. A grep across the package found "at most 10" only at TL:56 and TL:112 (run today). SRC:122 says "the merge command's maximum of 10 inputs" and "never exceeds 10". TL:104 requires each assertion to use "a phrase quoted from `./source.md`". So the plan contradicts itself: following TL:112 breaks TL:104. A contract written in the spec's own words fails the test TL:112 describes. C's R3-F3 (C:52-59) describes the mechanism but gives no instance. The merged finding needs A's instance as its anchor.
2. **R1-F4 (U-001) is the only check against a repo ABSOLUTE RULE.** CLAUDE.md:76 forbids pointing installed primitives in `src/superclaude/{commands,skills,agents,core,...}` at `src/superclaude/...` paths. CLAUDE.md:87 says package code (`src/superclaude/cli/`) is not installed: "Do not add new references to them from a primitive". The text Task 1 must restate carries exactly such references. SRC:59 cites `src/superclaude/cli/install_core.py:36,56,65-70` and `CAPS:130`. The WC rows carry `INV-A:`, `CAPS:` and `sk/...` evidence (SRC:70-81). TL:37-40 says to write the rules "from these source sections" and never says to drop the evidence citations. The plan's Constraints (TL:17-27) carry the source-of-truth rule (TL:23) but not the installed-path rule. AC-C1 checks only Orca verbs (SRC:246). The managed FINAL checks plan Constraints, not repo CLAUDE.md (qa.md:310). So no gate in this run catches it, and the file installs into other projects (SRC:59, `~/.claude/WORKER-CONTRACT.md`). No other card raised this.
3. **R1-F2 (U-002) is a real path to a QA failure.** TL:157 requires "a PASS or FAIL line with an evidence file for each of the eleven checks". No task saves an artifact for AC-0.1 (TL:47, TL:72), AC-0.2 or AC-0.3 (TL:93-94), and Task 8 re-runs only the common checks (TL:147-152). Under the executor's Evidence-type AC rule, "the evidence artifact is absent" means `ac-outcome-missing=yes` (qa.md:85), which blocks (qa.md:41). The executor can still save the files inside Task 8, so should-fix is the right grade.
4. **R1-F3 is grounded in the spec, not only in a hit count.** SRC:61 puts `/sc:pr-submit` on the never-as-worker list. SRC:174 says the pr-submit row "applies only if D3 (b) is ever adopted". SRC:201 says pr-submit gets "no `--unattended` mode and no Phase 4 changes". So for these hits, TL:125's "the phase that converts its command" has no true value. C's R3-F5 (C:96-101) adds a second cause (read-only `gh pr` hits; H9 counts 40 `gh pr` hits) and the keying problem. The two together make one finding.
5. **R1-F5 names the line that decides Task 3, which B's R2-3 does not.** `scripts/build_superclaude_plugin.py:75` copies `["agents", "commands", "hooks", "scripts", "skills"]` and no `core` (opened today). B's evidence is the empty hunk H4 (B:56; `grounding-hunks.md` H4 is empty). The grounding is worse than B says. H5 reports `plugins/superclaude/core` as "(no matches)", but a Glob today lists `RESEARCH_CONFIG.md`, `BUSINESS_PANEL_EXAMPLES.md`, `RULES.md`, `PRINCIPLES.md`, `BUSINESS_SYMBOLS.md`, `CODEGRAPH.md` and `__init__.py` there. The executor should be pointed at the build-script line, not left to work from an absence.
6. **A is the only card that checked Task 7's environment.** A's self-audit checked that the `/opt/Orca` files exist and that the profile holds `"nestedWorkerMaxDepth":1` (A:110-112). The B and C calibrators both flag this as the gap in their cards (B:99, C:229). A's self-audit also recorded the missing `make verify-sync` baseline (A:117-118), which C later filed as R3-F11.

## Weaknesses identified in others

1. **B:81-82 asserts a check whose result the plan text contradicts.** "No task instruction breaches the plan's own Constraints" is false on the literal text: TL:21 says "P0 edits no command, skill or agent file", and TL:90 orders a write to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. That directory also holds the skill's `SKILL.md` (listed today). B's PASS rests on a lenient reading it never states.
2. **B's R2-3 is mostly redundant.** TL:69 already tells the executor to "Read `scripts/build_superclaude_plugin.py`", and B's own calibrator says so (B:96). The useful part, naming line 75, is in A's R1-F5.
3. **B's R2-1 is over-graded.** No task, AC or gate reads the AC-0.8 sentence. The FINAL tests whether a Constraints item is violated (qa.md:310), not whether it is true, and nothing can violate a scope note about a check that does not exist. It is a real false statement and should be fixed, but at minor.
4. **C's R3-F3 has the wrong deviation class.** It is a conflict inside the plan (Task 5 against Tasks 1-2), not a departure from the spec, as C's calibrator notes (C:226). Merged with A's R1-F1, the class is drift on firmer ground: TL:112 attributes to section 2.3 a phrase that section 2.3 does not contain (SRC:122).
5. **C's R3-F6 has a wrong citation and an inflated grade.** Line 290 of `tests/core/test_how_we_work_routing_table.py` holds the marker-order assertion, not the `"### 3.14 "` to `"## 4. "` slice C quotes (C:227; diff-analysis C-005 places the slice at line 1091). Task 4's own AC runs those tests (TL:93), so a breach shows up in the same task and costs one repair round, not a halt. That is minor.
6. **C's R3-F4 depends on a copy the evidence argues against.** The build script does not ship `core/` (`build_superclaude_plugin.py:75`). The verify-sync gap C cites (Makefile:170, 202, 228, 254, 280) is real, but it matters only if Task 3 adds the copy. It should be a conditional clause on R1-F5 ("if you add a copy, add a byte-identity test like `test_plugin_mirror_matches_src`"), not a standalone should-fix.
7. **C under-cited its own blocker.** C names only the Task 4 reviewer gate (qa.md:52, qa.md:61). The managed FINAL is a second, independent gate: it returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310), which ends in `E-ARCHIVE-BLOCKED` (qa.md:286). This makes C's case stronger, not weaker.

## Concessions

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

## Positions on diff points

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

## Shared-assumption responses

- **A-009: ACCEPT.** `src/superclaude/cli/install_core.py:30-32` reads `def install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`, which matches the call at TL:72. Its docstring (line 36) says it copies all `.md` files from `src/superclaude/core/`. The worktree's `.venv` installs `superclaude` in editable mode from this worktree (`direct_url.json`: `"editable":true`, url = this worktree; the `.pth` points at `<worktree>/src`), so `uv run` will read the new file and not a stale installed copy. If it did not, Task 3's own AC would fail loudly rather than pass silently.
- **A-010: ACCEPT.** `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md` printed nothing against merge base `c118b5a5` (run today). The check compares against the merge base, so later commits on `master` do not change the result unless the branch is rebased onto a `master` that deleted guide lines. Nothing in this plan rebases.
- **A-011: ACCEPT.** The SRC:246-253 pipeline, run read-only on today's tree, printed nothing and grep exited 1 (run today). The pipeline excludes `plugins/superclaude/core/WORKER-CONTRACT.md` by name (SRC:252), so the scan stays clean whichever way Task 3 decides (A-008). Any later hit can only come from this plan's edits.
