# Round 1 advocate: Variant B (reviewer 2, qa persona)

Citation key: as in `diff-analysis.md` (A:N, B:N, C:N for the cards; TL:N plan; SRC:N spec; qa.md:N and SKILL.md:N for the executor rules). Every TL, SRC, qa.md and repo line below was opened for this round. Checks I ran myself are marked "(ran)".

## Position summary

Variant B's PASS verdict does not survive. Its central claim, "no task instruction breaches the plan's own Constraints" (B:81-82), is false against TL:21 and TL:90, and the executor's real QA rules make that conflict a reachable halt that no repair can close. I concede the verdict to Variant C (FAIL, R3-F1 blocking). Variant B still contributes two verified findings no other card has (R2-1, R2-2), the only executor-halt-path inventory framed for QA, and the test I propose for grading every other item: a plan defect is blocking only when it opens a halt path that no in-run repair can close.

## Steelman

**Variant A (analyzer, PASS).** A's strongest case is breadth with precision. It is the only card to catch the repo's ABSOLUTE RULE against `src/superclaude/...` paths in installed primitives (R1-F4), and that defect is real: SRC:59 carries `src/superclaude/cli/install_core.py:36,56,65-70`, and the spec has 29 lines mentioning `src/superclaude` (ran). A Task 1/2 "restate" could copy those into a file installed to `~/.claude/`. A is also the only card that names the concrete off-spec phrase in Task 5: "at most 10" appears in TL:56 and TL:112, while SRC:122 says "maximum of 10 inputs" (ran: `grep 'at most 10' source.md` finds nothing). A checked the live environment for Task 7 (A:110-112), which B and C did not. Its PASS rests on a defensible reading: TL:24 already allows "their plugin copies" of `HOW-WE-WORK.md` to carry Orca text, so a reviewer can read TL:21 as aimed at command, `SKILL.md` and agent files, as its own citation "no command edits" suggests.

**Variant C (refactorer, FAIL).** C's strongest case is that it reasons from the executor's actual severity rules, not from the reviewer's sense of what is serious. It quotes the constraint (TL:21), the mandatory write (TL:90, with the `cmp` AC at TL:93), and the mechanical rules: a B4 answer is confirmed when "the quoted text is byte-present in the plan Constraints or a task instruction" (qa.md:61), and the reviewer's own label is never read (qa.md:79). C also shows the conflict is self-inflicted: the spec's P0 row says only "(no command edits)" (SRC:220), and the plan added "skill or agent". C honestly reports its 0.6 confidence as doubt about R3-F1's severity, not about card quality (C:211-212, C:230). It also covers the most tasks with the most findings (11 findings across Tasks 1-6 and 8).

## Strengths claimed

1. **R2-1 is a verified false statement in the plan's scope block.** TL:19 says "AC-0.8 is a P1 check (section 7.3)". There is no AC-0.8 in the spec (ran: `grep -n 'AC-0\.8' source.md` exits 1). The P0 rows go AC-0.7 (SRC:304) then AC-0.9 (SRC:305), and P1 starts at AC-1.1 (SRC:306). No other card caught it. My calibrator re-verified it (B:94).
2. **R2-2 is the only finding on the static-to-live handoff.** The spec puts the phase report in the live plan (SRC:238), and AC-0.6 and AC-0.7 results must appear "in the phase report" (SRC:303, SRC:304). Task 8 ends with next steps only (TL:154) and never obliges the live plan to carry `p0-static-report.md` or the AC-0.7 and AC-C6 artifacts. Diff analysis rates its value Medium (U-004), above its card label of minor.
3. **B's halt-path inventory is the right frame for the debate.** B is the only card that lists the executor's halt paths by name and asks whether any defect reaches them (B:82-84: E-NO-AC, E-HALT-QA ladder, quoted-constraint breach, FINAL issues). The frame is correct; B applied it wrongly to TL:21. Applied correctly, it gives the grading test I use below: blocking at plan stage means a reachable halt (qa.md:280-286) that no repair inside the run can close.
4. **B's structural checks hold.** Every pytest target named in Tasks 3 and 4 exists (B:68-72; calibrator confirmed, B:97). The Depends-on graph is satisfied by source-order execution (B:73-74), which matches SKILL.md:97 ("Default sequential in source order"). Shared assumption A-002 rests on this.
5. **R2-3 and the empty-hunk observation.** B is the only card that noticed grounding hunk H4 (the plugin build script) is empty (B:47-50), an evidence gap in the reflect run itself. I concede below that A's R1-F5 is the better finding on the same Task 3 question.
6. **`matrix_omissions` (B:58-64)** records two spec spans (SRC:236, SRC:188) with no coverage-matrix anchor. This is bookkeeping, not a plan defect, and should be carried as a note only.

## Weaknesses identified in others

1. **A's PASS ignores the route its own calibrator half-saw.** A's calibrator notes that qa.md:52 makes breach of "an explicit task instruction" a blocking trigger and that A "under-states this route" for R1-F1 and R1-F3 (A:132). A never applies the same rule to the Constraints block, so it misses TL:21 against TL:90.
2. **A's R1-F3 and C's R3-F5 under-state one edge case.** TL:125 requires "the phase that converts its command" for every allowlist entry. For a hit no phase converts (pr-submit and git are never workers, SRC:61, SRC:201), the executor must either omit the phase (an explicit-instruction breach, qa.md:52) or invent one (a false claim in delivered text, qa.md:50). Both are `yes` answers. This is repairable in practice (write "none: never a worker"), so it stays should-fix, but it is the next-nearest halt risk after R3-F1 and should be fixed in the same pass.
3. **C's R3-F1 overstates certainty.** C says a strict reviewer "ends the run" (C:15-17). The Read-back only checks that the quote is byte-present (qa.md:61). Whether the diff "violates" the constraint is still the reviewer's yes or no (qa.md:52, qa.md:56). So the halt is conditional, as C's calibrator says (C:223). This does not lower the grade (see X-002), but the merged text should say "can halt", not "will halt".
4. **C's R3-F6 has a wrong citation.** C cites `tests/core/test_how_we_work_routing_table.py:290` for the "### 3.14 " to "## 4. " slice; line 290 holds the marker-order assertion and the slice is at line 1091 (diff-analysis C-005; C's calibrator, C:227). The claim stands; the citation must be corrected in the merge.
5. **C's R3-F3 deviation class is loose.** It is an inconsistency inside the plan (Task 5 against Tasks 1-2), not a departure from the spec, so `drift` is arguable (C's calibrator, C:226). A's R1-F1 is the concrete, spec-departing instance (TL:112 says "as written in section 2.3" for a phrase the spec does not contain). The merged finding should lead with A's instance.
6. **Neither A nor C checked Task 7's environment in a finding.** A checked it in its self-audit only. I confirmed it today (ran): `/opt/Orca/resources/app.asar.unpacked/out` exists and `~/.config/orca/profiles/local-default/orca-data.json` exists. So A-004 holds and no finding is needed.

## Concessions

1. **B's verdict is wrong.** B:81-82 says no task instruction breaches the Constraints. TL:21 forbids editing any "skill ... file"; TL:90 orders a byte-for-byte write to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, a file inside a skill package that also holds `SKILL.md` (ran: `ls plugins/superclaude/skills/sc-recommend/`). TL:93 makes that write an AC. B also claimed the halt paths were "not reachable from any defect I could locate" (B:84). That is false for this defect.
2. **B missed the strongest gate.** Even if the Task 4 reviewer reads TL:21 leniently, the managed FINAL is a fresh subagent that reads "the plan's `## Constraints`" and returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310). That blocks archiving as `E-ARCHIVE-BLOCKED` (qa.md:286). Two independent readers each get a chance to say yes.
3. **No inherited cap rescues it.** The cap applies only to text present in `$start` (qa.md:153-154). The new Orca lines in the plugin copy are written by Task 4, so their origin is `new` and a confirmed B4 is `blocking` (qa.md:41, qa.md:81).
4. **R2-3 is subsumed by A's R1-F5.** A names the deciding line (`scripts/build_superclaude_plugin.py:75`, no `core` in the copied folders) and the parity test (`tests/commands/test_routing_plugin_parity.py:3-4`). My calibrator noted my recommendation was largely redundant because TL:69 already orders a full read (B:96). Merge R2-3 into R1-F5 at minor.
5. **R2-1 is lower impact than its label.** B2 (`false-claim`) covers "delivered text or code" (qa.md:50); plan text is not delivered, so the false AC-0.8 sentence cannot trigger a halt. I accept a downgrade from should-fix to minor; the class stays `drift` because the plan states something the spec does not.
6. **B missed Task 7's environment risk** (my calibrator, B:99) and the verify-sync baseline gap (C-004). Both turn out to be low: the paths exist today, and C-004 is minor.

## Positions on diff points

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

## Shared-assumption responses

- **A-009: ACCEPT.** `install_core_files` takes `target_path` and returns a `(bool, str)` pair, exactly as TL:72 unpacks it. Verified at `src/superclaude/cli/install_core.py:30-32` (ran: `def install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`).
- **A-010: ACCEPT.** The merge base is `c118b5a5` and `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md` prints nothing today (ran). No task before Task 4 touches that file (TL:31-74), so AC-0.3 (TL:94) starts clean.
- **A-011: ACCEPT.** The AC-C1 pipeline from SRC:246-253, run read-only on the current tree, printed nothing (ran; the pipeline exited 1, meaning no lines). The two files this plan adds Orca text to, and their plugin copies, are excluded by name (SRC:250-253), and the new test file lives under `tests/`, which the scan does not cover. So only an unintended Orca verb in a command, skill or agent file could fail it.
