# Issue #346 roadmap

This roadmap carries out `346-plan-merged.md`. Each phase is one small PR. Each phase ends with a test gate that has to pass before the next phase starts. No phase begins until the owner has approved the item it carries out.

## Rules for every phase

- **Scope.** A phase is one PR of about 4 hours or less. It must be revertable on its own and must not depend on a later phase.
- **Gate first.** Write the gate tests at the start of the phase and confirm they fail against current master. Then make the change and confirm they pass.
- **Gate failure.** You get at most 2 fix attempts per gate. After that, stop and bring the failing output to the owner. Never skip, weaken or mark a test xfail to get green.
- **Commands for every gate.** `uv run pytest <listed tests> -v`, `make verify-sync`, `make lint`, plus the CLAUDE.md check `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` (justify every new hit).
- **Desk replays.** A "desk replay" means a person (or a model reading files) re-grades frozen phase-4/5 reports from `exp:` against the new rules. It reads data only and runs no IronClaude workflow, so it fits the current constraint.

## P0: decisions (no code)

| Decision | Options |
|---|---|
| §4 severity mapping | Approve or correct the table |
| D6 | Does the severity policy also apply to `/sc:pr-submit`? |
| A1 | Approve implementation |
| A2 | Approve writing the spec |
| PR route | **Decided (owner, 2026-11-09):** use the documented CLAUDE.md fallback, not `/sc:pr-submit`, because the standing constraint forbids invoking IronClaude. Each phase PR runs the pre-PR checks first (origin is the fork; rebase onto `origin/master` if needed), then `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."`, then confirms the returned URL is `https://github.com/IronbellyOrg/IronClaude/pull/N`. Because pr-submit's automatic Augment/Codex review loop does not run, the phase's single independent review takes its place. |

**Gate G0:** each decision is recorded in the plan with a date and its owner. Exit: P1 is unblocked.

## P1: remove the effective prompts that override #427 (A1-a, A1-b, A1-c, A1-e)

- **Changes:**
  - `pragmatic.md:221-222`: allow a zero-finding result when it is backed by evidence.
  - `pragmatic.md:232-233`: allow deleting or narrowing text.
  - `task/SKILL.md:233` and `:430`: remove the "at least N errors" quotas.
  - `HOW-WE-WORK.md` near `:65`: add the two paste-ready briefs (plan §7), then copy the file to the plugin ref and the core `CLAUDE.md` table as CLAUDE.md requires.
- **Gate G1:**
  - Extend `tests/skills/test_review_severity_rule.py`. Assert that the adversarial-stance, zero-is-suspect and N-error texts are gone, and that the zero-with-evidence and deletion-allowed texts are present.
  - Add a **brief lint** test. Fixtures are the frozen T07 and T09 brief texts (`exp:phase2/S1/briefs/task-text/T07…`, `T09…`) and the new HOW-WE-WORK briefs. The lint must flag "any finding of any severity is FAIL", "assume defects remain", "at least N" and "apply all findings" in T07/T09, and find none of them in the new briefs.
  - Existing routing and HOW-WE-WORK copy tests stay green.
- **Pass condition:** every test above passes and the brief lint catches both historical briefs.

## P2: severity normalization (A1-d, A1-g)

- **Changes:**
  - Apply the approved §4 mapping in `pragmatic.md:225-229` and `spec-panel.md:259`.
  - `spec-panel.md:313` and `:328-329`: change the boundary-table rule from at least 6 rows per guard to one row per applicable input class. A GAP blocks only when it names a concrete wrong outcome; otherwise it is a Medium warning plus a follow-up candidate.
  - Keep FR-10, and keep findings that touch safety, security or data loss blocking regardless of label.
- **Gate G2:**
  - Contract tests in `tests/skills/test_spec_panel_review_loop.py` and `test_review_severity_rule.py` cover the mapping table, the label-independent escalation clause and the follow-up-candidates section.
  - **Desk replay:** re-grade the review-3 reports of flg-r1, flg-r2 and trt-r1/r2 under the new mapping. Record per run how many findings are blocking, Medium and Low, and the resulting verdict. Expected: flg-r1 matches its known 4 blocking findings (out of 6 MAJOR labels). Any severe finding the mapping would demote to Medium is a gate failure.
- **Pass condition:** the tests pass and no seeded or known severe finding is demoted in the replay.

## P3: installer drift (A1-f). Runs in parallel with P2.

- **Changes:**
  - Port #419's "kept file differs from shipped copy" warning (`install_core.py:94-101`) to output styles and commands.
  - On `update` and `--force`, back up any file that differs from the shipped copy before overwriting it.
- **Gate G3:** add cases to `tests/cli/test_install_user_setup.py` and `tests/unit/test_cli_install.py`, each using a temporary home:
  - clean home: installs, no warning;
  - stale but unedited copy: warning on `install`, replaced on `update`;
  - customized copy: warning on `install`; on `update`, a backup exists and its bytes match the original;
  - unreadable target: reports an error and does not overwrite.
- **Pass condition:** all four cases pass, and existing installer tests stay green.

## P4: Review Loop extension (A2). Write the spec, review it once, then implement.

- **Spec step:** add bullets 1-8 from plan §6 to `spec-panel.md:256-264`, with the traceability table. One independent review of the spec. The 2-fix/3-review cap applies to this review too.
- **Gate G4:**
  - Extend `tests/skills/test_spec_panel_review_loop.py` with one assertion per bullet: the precedence clause and the requirement to name any overridden brief clause; the five dispositions, with `deferred` and `withdrawn` counting as open; "missing verdict means FAIL"; the `scoped PASS` coverage line; gross added/deleted bytes per finding id; the provenance header fields; no edits between fix 2 and review 3; Medium findings excluded from the Reviser brief.
  - **Desk replay of the known failure cases:**
    - in ponytail's final report (`exp:phase5/FINAL-REPORT.md:150-152`), the carried MINOR becomes a note and no longer fails the review;
    - ponytail's orphan `R3-N1` reference counts as ambiguous, so the verdict fails closed until it is resolved, and the recorded zero is not accepted as a count;
    - the diffgate final review is labelled `scoped PASS/FAIL` with its coverage;
    - ledger's deferred rows count as open.
- **Pass condition:** the tests pass and all four replay outcomes match.

## P5: replicated validation (A3). Only with exact-run authorization.

- **Prerequisite:** P1-P4 merged, and the installed command bytes verified on the test host (E6).
- **Runs:** three arms (original briefs on #427; new briefs; new briefs plus A2), at least 3 replicates each, using the cases and design in plan §8.
- **Gate G5:** the five checks in plan §8. Success means arm 2 or arm 3 beats arm 1's final blocking count by more than the within-arm spread, with no worse growth and every seeded severe defect visible.
- **Stop rule:** publish the results once. If the result is null or negative, stop. Any further step, including D1 retirement, is a new decision.

## Order and dependencies

```
P0 ─► P1 ─► P2 ─┬─► P4 ─► P5 (authorized only)
            └─► P3 ─┘   (P3 depends only on P0)
```

**Why this order:** P1 targets the cause with the strongest evidence (briefs overriding the command, E4) for the least effort. P2 needs the owner's mapping. P4 builds on P1/P2's vocabulary. P5 is the only phase that needs live runs.

**Effort:** P1 about 4h, P2 about 3h, P3 about 3h, P4 about 4h, plus one independent review per PR.
