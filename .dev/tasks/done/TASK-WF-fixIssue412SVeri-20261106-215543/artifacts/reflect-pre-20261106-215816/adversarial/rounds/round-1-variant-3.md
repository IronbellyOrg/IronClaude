## Advocate: Variant 3 (opus/refactorer)

### Position Summary

Variant 3 returns PASS with no blocking findings and two minor findings. In this statement "card" means a reviewer's finding file and "fixture" means a test's prepared starting state. All three cards agree on PASS, and that is the right verdict: every divergence any card raises is a gap in how the plan will be checked, not drift or a regression. Variant 3's case is that its two minor findings point at real code and test lines that can be re-read. They also name the single most likely way the Task 2 fix could pass its tests while still breaking the plan, which is an exit-0 skip printed as a refresh success. Variant 3 asks for the fix without new machinery: "no keyword parser needed" (card line 18) matches plan line 45, "reuse existing result fields without a new parser".

Nothing here claims that a test, an install or a runtime run took place. Every point below comes from reading files.

### Steelman: Variant 1

Variant 1 (sonnet/analyzer) is the only card that addresses the requirement closest to the user: the instruction text must keep a Claude CLI agent separate from a shell. R1-3 (card lines 19-22) asks for a check that ties the terminal surface to agent creation and forbids shell routes for ccsession sessions. Its limitation note (card line 30) catches the gap between the source and the acceptance criterion: `source.md:1` says "use Claude (CLI), never New Terminal", while plan line 35 only says "explicitly distinguish". R1-2 reaches the same exit-0 skip fixture as Variant 3 (card line 16) on its own, which supports C-001 from a second angle. Variant 1 also records its own wrong citation openly (`evidence_pathology`, card line 18), which is good audit practice. R1-1 is cautious about ordering and admits it is not an omission.

### Steelman: Variant 2

Variant 2 (haiku/qa) took the widest view. It audited 21 semantic requirements against the plan's Inputs and Constraints, not only the acceptance criteria (card lines 8-11). Its self-audit lists the behaviours Task 2 must keep, all present in plan line 45: forced refresh, default skip, no external `--force`, edited-copy protection, executable identification, deadline, and the three-skill list. It also notes that mocked checks are kept separate from live refresh and UI reproduction (card line 14), which plan line 52 requires. Its verifier calls for failures observed before the fix and passes after it across absent, failing, timed-out and incomplete cases (card line 16), which matches plan lines 51-52. Of the three cards, it gives the most complete checklist of what the plan already covers.

### Key Strengths Claimed

1. **R3-2 targets the real failure mechanism, anchored to the correct code range.** In `install_user_setup.py`, line 236 returns "already installed" early whenever all three SKILL.md files exist. Lines 257-263 judge success only by `returncode` and file presence. Once the force gate opens, a forced run with all three files present passes the presence check automatically. If Orca exits 0 after skipping an edited guide (`orca-discovery.md` lines 21 and 25: "skipped and is reported", "skipped folders are warnings", only exit 1 is failure), line 263 prints "✅ Orca skills: ..." and discards `result.stdout` and `result.stderr`. Plan line 24 ("Do not treat a safe skip as proof that the guide refreshed") and plan lines 45 and 51 forbid exactly that. R3-2's verifier (card line 21) is the smallest test that catches it: exit 0, three files present, stdout naming a skipped guide, then assert the text is visible and no refresh-success claim is made.
2. **R3-2 enforces the plan's minimality constraint.** "No keyword parser needed" matches plan line 45 word for word ("reuse existing result fields without a new parser"). The fix needed is to relay `result.stdout` and `result.stderr`, not to classify them. The other two cards leave this open, so an implementer could build a parser for skip keywords, which the plan forbids.
3. **R3-1 names a verified wider-regression reader that the plan does not list.** `tests/core/test_codegraph_guide.py:137` reads `src/superclaude/core/CLAUDE.md`, the same file Task 1 edits. The test asserts exactly one row starting with `| codegraph` (line 149), exactly one marker pair (line 155), the content of the "### Refresh-tool selection" section up to the next `\n### ` heading (lines 162-166), and no "serena" (line 173). Plan line 52 lists `test_claude_md_routing_block.py`, but not this file. A new global rule placed carelessly, for example inside the Refresh-tool section or as a new `| codegraph...` table row, would break these assertions. Adding the file to the Task 2 regression run costs almost nothing.
4. **Correct reading of the sync delivery.** Variant 3's self-audit (card line 25) states that Task 2's sync step delivers Task 1's README edit, which plan line 47 says explicitly ("as part of delivering the changed skill README"). Variant 3 does not turn that into a finding.
5. **Deviation classification is calibrated.** Both findings are verification suggestions, not Drift or Regression. The self-audit (card lines 23-26) confirms the plan keeps the positional callers, the three skills, executable lookup, the timeout and the nonfatal behaviour, and proposes no Orca change, global install, commit or push. This matches plan lines 20 and 23.

### Weaknesses in Variant 1

- **Wrong code anchor.** R1-2's `original_source_ref` points at the wrong range, which Variant 1 itself flags. The real helper is `install_user_setup.py:230-263`. Because R1-2 is not anchored to the helper's code, the citation evidence (S-002) favours Variant 3.
- **R1-1 is a self-retracted non-finding.** Its own note (card line 12) says Task 2 delivers the synchronization, so it is not an omission. Moving the sync checks earlier is optional ordering, not a gap in coverage.
- **R1-2 is broader than the evidence.** "Success-prefix handling … not precisely defined" overstates the gap. Plan lines 24, 45 and 51 do define the requirement; what is missing is the specific fixture. Variant 1's verifier is right, but its claim frames a fixture gap as an unspecified requirement.
- **Confusing limitation wording on X-001.** Card line 30 says the reviewer wording claims the acceptance criterion forbids New Terminal. The prohibition actually reaches Task 1 through its Inputs (plan line 30: "the explicit launch requirement in source.md"), not through the wording of plan line 35. Variant 1 leaves this for the merge to settle instead of resolving it.

### Weaknesses in Variant 2

- **Anchored to the brief, not to the code or plan.** Its only evidence is `reviewer-briefs/reviewer-2.md:49-82` and `:137` (card lines 19-20). A later stage cannot check those claims against the plan or the code without redoing the review.
- **21/21 is a reviewer's judgment, not a measurement.** The lexical check for this run finds 13/21 (0.6190, diff-analysis line 34). Variant 2's own limitation (card line 22) says "full matrix completeness not independently checked", which undercuts the 21/21 figure.
- **Zero minor findings hides the X-002 gap.** Its verifier lists "output" (card line 16) but never names the exit-0 skip with all three files present. A test suite could cover nonzero, missing-file and timeout output, meet Variant 2's verifier, and still let line 263 print success over a skipped edited guide.
- **Accepts the weaker acceptance-criterion wording on X-001.** "Shell distinction" (card line 13) accepts plan line 35's "distinguish" without noting that `source.md:1` says "never New Terminal".

### Concessions

- **Silent on C-003 and X-001.** Variant 3 has no position on the terminal-surface versus New Terminal wording. Variant 1 handles it better.
- **R3-1's other leads are unverified.** `tests/cli/test_bash_inspection_policy.py:32`, `tests/cli/test_issue_body_templates.py:18` and `tests/core/test_how_we_work_routing_table.py` are search leads only. Only `tests/core/test_codegraph_guide.py:137-174` was read. Even there, breakage is conditional on where the new passage is placed, not shown.
- **Citation pathology.** Variant 3's own "plan lines 81-82" refer to line numbers in the reviewer brief and must not be cited. The real plan text is at lines 45-51.
- **Narrow reading.** The persona did not read the full spec or the live Orca help (card lines 29-31). The Orca exit-code semantics come from the help excerpt in `orca-discovery.md`, not from a run.
- **Lower calibrated confidence than Variant 1** (0.68 against 0.72), with degraded calibrator diversity.
- **Container completeness.** Variant 1 attaches a `plan_ref` to every finding. Variant 3's R3-1 has no plan reference.

### Shared Assumption Responses (A-001..A-004)

- **A-001 — QUALIFY.** The Orca help supports it ("skipped and is reported", "skipped folders are warnings", only exit 1 is failure, `orca-discovery.md` lines 21 and 25), but no install was run, so exit 0 on skip is documented help-text behaviour, not observed behaviour.
- **A-002 — ACCEPT.** This is a static fact from the code. Line 257 counts files that exist, and line 258 judges success only on `returncode` and that count. With all three files present before the call, the presence check passes automatically, and line 263's message cannot prove a refresh. Plan line 24 already treats this as a risk.
- **A-003 — ACCEPT.** All three cards' limitations, and plan line 19 ("Runtime incident causation remains UNDETERMINED"), keep the verdict at plan level.
- **A-004 — QUALIFY.** A keyword-friendly `force: bool = False` keeps the existing caller at line 441 (keyword `deadline=`) and any positional `(home, deadline)` call compatible, provided `force` comes last with that default. Whether existing test doubles in `tests/cli/test_install_user_setup.py` accept the new keyword was not checked.

### Per-Point Positions

- **S-001 (finding container): Variant 1.** Every finding carries both `plan_ref` and `verifier`. Variant 3 ties on verifiers but lacks a plan reference on R3-1.
- **S-002 (evidence anchoring): Variant 3.** It is the only card whose code anchors are correct and re-readable (`install_user_setup.py:230-263`, `test_codegraph_guide.py:137-174`). Variant 1's code range is wrong, and Variant 2 cites only the brief.
- **C-001 (exit-0 safe skip, three files present): Variant 3.** Its verifier adds the "no refresh-success claim" assertion tied to plan line 24 and forbids a parser in line with plan line 45. Variant 1 reaches the same fixture with vaguer framing.
- **C-002 (where Task 1 checks run): Variant 3.** It reads plan line 47 correctly as Task 2 delivering the sync, without raising a finding that then has to be retracted. Variant 1's earlier-run suggestion is harmless but optional.
- **C-003 (terminal surface versus New Terminal wording): Variant 1.** It is the only card with a concrete verifier. Variant 3 is silent.
- **C-004 (wider regression readers of core CLAUDE.md): Variant 3.** It is the only card to find a verified reader (`test_codegraph_guide.py:137`) missing from plan line 52's regression list.
- **C-005 (coverage claim): Variants 1 and 3 jointly.** Neither gives an unsupported count. Variant 2's 21/21 conflicts with the lexical 13/21 and its own limitation.
- **X-001 (forbid or distinguish New Terminal): Variant 1.** It raised the contradiction. Ground truth: the prohibition reaches Task 1 through its Inputs (plan line 30, `source.md:1`), while the acceptance criterion at plan line 35 is weaker.
- **X-002 (is the success/skip output specified): Variant 3.** The requirement exists (plan lines 24, 45, 51); only the exit-0 fixture is missing, which is exactly R3-2. Variant 2 overstates the coverage, and Variant 1 overstates how much is unspecified.
- **A-001 (exit 0 can hide a skip): Variant 3.** Its verifier says outright that the mock exits 0. Variant 1 assumes the same thing without saying so.
- **A-002 (presence check passes automatically when files exist): Variant 3.** It is the only card whose verifier ("no refresh-success claim") implies this mechanism at lines 257-263.
