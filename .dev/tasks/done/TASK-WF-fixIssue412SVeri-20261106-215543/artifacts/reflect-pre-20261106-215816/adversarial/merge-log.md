# merge-log

<!-- STUB 2026-11-06T22:15:48Z: populated incrementally -->

## Metadata

- Base: Variant 3 (`variant-3-original.md`, reviewer-3-card, opus/refactorer), combined score 0.8113 (`base-selection.md`)
- Other inputs: `variant-1-original.md`, `variant-2-original.md`, `invariant-probe.md`, `debate-transcript.md`, `diff-analysis.md`
- Refactoring plan: `refactor-plan.md` (8 planned changes, 6 rows in "Changes NOT Being Made")
- Plan under review: `.dev/tasks/to-do/TASK-WF-fixIssue412SVeri-20261106-215543/TASK-WF-fixIssue412SVeri-20261106-215543.md` (53 lines)
- Output: `merged-review.md`
- Date: 2026-11-06
- Execution scope: files read and two files written (`merged-review.md`, this log). No tests, installs, Git, GitHub or Orca commands were run.

## Changes Applied

| # | Change | Status | Provenance | Before -> After |
|---|---|---|---|---|
| 1 | Merge V1's empty-output case and INV-005/INV-006 into the R3-2 verifier | applied | Base, modified; V1 `variant-1-original.md:16`; Invariant probe INV-005, INV-006 | One stdout-skip fixture -> three forced, exit-0, three-files-present fixtures: (a) stdout skip, (b) stderr-only skip, (c) empty output, where a presence-only line is acceptable and "refreshed"/"updated" is not. Anchors ius:230-263 and plan:45-51 kept; plan:24 added. Orca exit-0 skip labelled as documented help (orca-discovery.md:21, :25). |
| 2 | Add R1-3 + X-001 as a minor note on Task 1 terminal-surface wording | applied | V1 R1-3 (`variant-1-original.md:20-22`); X-001, C-003; INV-018 | New note placed after R3-2. plan_ref plan:30, plan:35; evidence `source.md:1`, orca-discovery.md:12-16; verifier as planned, plus the INV-018 AC-alignment refinement. |
| 3 | Trim R3-1 to its verified reader and attach plan:52 | applied | Base, modified; V3 Round 2 defense; INV-016, INV-017, INV-019 | Four evidence items (one verified reader, three leads) -> one verified reader `tests/core/test_codegraph_guide.py:137-174` with assertion lines 149, 155, 162-166 and 173. plan_ref plan:52 added. The two unverified leads were dropped. The routing-table test and `tests/cli/test_update_command.py` were added as run-it recommendations, with the routing-table file labelled not a verified defect. |
| 4 | Add INV-009 (forced-path deadline spend) as a minor note | applied | Invariant probe INV-009, INV-010 | New note: ius:39, :40, :436, :213, :397-399; `main.py:404`. Labelled nonfatal and honestly reported. Verifier asks that the Task 2 evidence record the plugin outcome on a mocked forced run and name the update path. |
| 5 | Add a LOW note on force passed by keyword and on message accuracy | applied | Invariant probe INV-011, INV-014, INV-015, INV-007 refinement; A-004 | New combined LOW note: ius:230-232, :441, :252-256, :258-262; `tests/cli/test_update_command.py:47-51`; `tests/cli/test_install_user_setup.py:264-287`, :307-308. Verifier: force after deadline, default False, keyword at ius:441; `"--force" not in command`; pin the failure-message wording when the guides exist. |
| 6 | Carry V2's preservation checklist and the mocked/live separation as self-audit context | applied | V2 U-003 (`variant-2-original.md:12-14`) | New self-audit subsection labelled "context, not a finding", anchored to plan:45 and plan:52. Placed in the self-audit, not among the minors, as the plan's Target specifies. |
| 7 | Keep R1-1 as an optional ordering note | applied | V1 R1-1 (`variant-1-original.md:9-12`); C-002 | One line at the end of the minors, labelled optional, with id, claim, plan_ref (plan:47, plan:52), evidence (plan:47) and verifier. |
| 8 | Report coverage both ways, kept separate | applied | `diff-analysis.md` (lexical); V2 (`variant-2-original.md:8-9`) | New Coverage section: lexical 13/21 = 0.6190 (measured; plan:19-24 Constraints outside the matcher) kept separate from the reviewer-judgment 21/21 (V2, not independently checked). The same distinction is repeated in the limitations. |

Applied: 8. Skipped: 0.

Orchestrator-required items also applied (not refactor-plan changes):
- Verdict section (PASS), the empty blocking-findings section, and the header provenance comments.
- Base limitations modified:
  - added plan-level-only scope;
  - added runtime causation UNDETERMINED (plan:19);
  - added the documented-not-observed qualifier for orca-discovery.md:21 and :25;
  - base limitation 1 (V3 did not read the full spec or Orca help) restated as a source-card reading-scope line;
  - base limitation 2 (the brief-local plan-line citation) removed under the exclusion rule.

Changes NOT made (honored, per `refactor-plan.md:113-122`):
- S-002: V1's wrong helper range and V3's brief-local plan-line pair are both excluded from the output.
- C-004: the two unverified test-file leads are dropped.
- C-005: 21/21 appears only as labelled reviewer judgment.
- X-002: V1's "not precisely defined" wording is not carried.
- Verdict: no blocking finding was added.

## Post-Merge Validation

### (a) Structural integrity

PASS. The headings in `merged-review.md` (grep `^#+ `), in order:
- H1 at line 5;
- H2 at lines 7, 17, 24 and 30;
- H3 at lines 34, 46, 61, 73, 84 and 100, under Minor Findings;
- H2 at line 106 (Self-Audit), with H3 at lines 110 and 120;
- H2 at lines 129 and 136.

No level is skipped. Each H2 and H3 section carries a `<!-- Source: ... -->` tag: 15 tags for 15 sections. The three required header comments are at lines 1-3.

### (b) Internal references

PASS.

Plan citations (grep `plan:[0-9]+(-[0-9]+)?`): 19, 19-24, 23, 24, 30, 35, 45, 45-51, 47, 50, 51 and 52. All are within 1-53. Content spot checks against the plan file:
- 19: "Runtime incident causation remains UNDETERMINED"
- 24: "Do not treat a safe skip as proof that the guide refreshed"
- 30: Task 1 Inputs, "the explicit launch requirement in source.md"
- 35: "explicitly distinguish Claude (CLI) ... from New Terminal"
- 45: "reuse existing result fields without a new parser"
- 47: sync recorded as part of Task 2
- 52: the named regression list, and mocked evidence kept apart from dry-run evidence

ius citations, each re-read with Read on 2026-11-06:

| Cited | Content found |
|---|---|
| ius:39 | `_ORCA_TIMEOUT = 25` |
| ius:40 | `_NETWORK_BUDGET = 30` |
| ius:213 | `timeout=10,` (the Orca probe in `_find_orca`) |
| ius:230-232 | `def install_orca_skills(home: Path \| None = None, deadline: float \| None = None) -> Tuple[bool, str]:` |
| ius:230-263 | the `install_orca_skills` body, ending with the success return at 263 |
| ius:252-256 | the `except (OSError, subprocess.SubprocessError)` branch returning "Orca skills: not installed (...); rerun" |
| ius:258-262 | `if result.returncode != 0 or len(installed) != len(_ORCA_SKILLS):` returning "installed N/3; rerun" |
| ius:397-399 | `remaining = deadline - time.monotonic()`; `if remaining < 2:`; `failed.append(f"{name} (time limit)")` |
| ius:436 | `deadline = time.monotonic() + _NETWORK_BUDGET` |
| ius:441 | `install_orca_skills(deadline=deadline),` |

Other anchors, each re-read:
- `src/superclaude/cli/main.py:404`: `install_user_setup(force=True)`.
- `tests/cli/test_update_command.py:47-51`: the `install_orca_skills` stub `lambda **kwargs`.
- `tests/core/test_codegraph_guide.py`: line 137 is `_CORE_CLAUDE`; the assertions are at 149, 155, 162-166 and 173.
- `tests/cli/test_install_user_setup.py`: 264-287 is the argv-capturing test; 307-308 is the prefix-only assertion.
- `artifacts/reflect-pre-20261106-215816/artifacts/orca-discovery.md`:
  - 4-7: provenance;
  - 12-16: the agent-launch excerpt;
  - 21: the skipped/reported note;
  - 25: exits 1 only on failure, and skipped folders are warnings.
- `variant-2-original.md`: 8-9 is the 21/21 count; 12-14 is the self-audit coverage list.

### (c) Contradiction re-scan

PASS. No contradictions were introduced. These pairs were checked:
- Verdict PASS against the six minor notes: every note is labelled a verification refinement or LOW, not a plan defect.
- Base self-audit "preserves existing positional callers" against INV-011, "a positional argument would break the stub": consistent. The new parameter goes after `deadline` and is passed by keyword.
- Base self-audit "Task 2 sync delivers the Task 1 README edit" against R1-1 "sync is part of Task 2 by design": consistent. R1-1 is labelled optional.
- Coverage 21/21 against 13/21: both are labelled, and the measured figure is not replaced.
- The limitation "V3 did not read the Orca help" against the card citing orca-discovery.md: the card attributes the Orca text to an earlier read-only discovery (orca-discovery.md:4-7), not to reviewer 3.
- R3-2 "documented help, not observed" against the limitations: the same qualifier is used in both places.

### (d) Exclusion check

PASS. Grep on `merged-review.md` for `113-119|81-82|test_bash_inspection_policy|test_issue_body_templates|install_user_setup\.py:113` returned 0 matches. That pattern covers `install_user_setup.py:113-119`, `plan lines 81-82`, `test_bash_inspection_policy.py:32` and `test_issue_body_templates.py:18`. No emojis were written, and Orca message text is quoted without its emoji prefixes.

## Summary

- 8 of 8 planned changes applied, 0 skipped, and no escalation needed.
- `merged-review.md` is a merged reviewer card with:
  - plan_verdict PASS and no blocking findings;
  - six minor notes (R3-1, R3-2, R1-3, INV-009, the combined INV-011/014/015 LOW note, and the optional R1-1);
  - the base self-audit plus V2's checklist as context;
  - lexical coverage 13/21 = 0.6190 kept separate from the reviewer-judgment 21/21;
  - limitations stating plan-level-only scope and runtime causation UNDETERMINED (plan:19).
- Validation: (a) structure PASS, (b) references PASS, (c) contradictions PASS, (d) exclusions PASS.
