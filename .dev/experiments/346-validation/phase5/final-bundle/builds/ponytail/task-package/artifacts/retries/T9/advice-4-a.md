model: claude-opus-5-5 family: claude rung: top (T1Model01; Agent model=opus)
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T9.AC1 | No attempt missed this one. Review 3 found every required literal, the T08a line and the Unattended sentence (review-3.md:3; attempt-3.diff:65, :89 matches `.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:257`). The attempts failed on scope instead: each one put the script's runtime behaviour into its own words. A3 said a failed exact-once check prints `APPLY_STOP` (attempt-3.diff:40). In fact the re-run check catches that case first (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:509-511`, `:785-787`), so `:859-860` is never reached (review-3.md:5). A3 has a second false claim the reviewer did not flag: "adds every held id that review 2 labelled CRITICAL or MAJOR" (attempt-3.diff:50). The script skips a held id that review 3 already counts as a new critical or major finding (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:1058-1062`). | Keep every AC1 literal exactly as attempt-3.diff:7-29, :44-92 has it. Remove the whole failure-path list (attempt-3.diff:37-42). Correct the owner-count clause. |
| T9.AC2 | No attempt missed this one either: `tests/docs` passed every time (review-3.md:4; extras-3.log:2). | Change nothing for AC2. Run `uv run pytest tests/docs -q` again after the rewrite. |

differs-by: The note says nothing about what any step does on failure, neither as a general claim nor step by step. It keeps only design decisions, each matched to a script line before it is written, and points to the `sc-fix-audit` skill for what each step prints.

Steps:
1. Confirm `docs/designs/spec-panel-ponytail.md` is absent. Edit no other file.
2. Write the title, status line and "What it is" paragraph word for word from attempt-3.diff:7-13. These claims hold: K1 is at `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:586`, and the single atomic write is at `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:757-766`, `:877`.
3. Write "The loop, step by step" (the table plus the trigger sentence) word for word from attempt-3.diff:15-29. The trigger sentence holds against `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:215-217`, `:319-343`.
4. Write "Safe apply" with exactly the four decision bullets of attempt-3.diff:33-36 and nothing else. They hold against `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:357`, `:553-577`, `:653-656`, `:673-684`, `:811-846`. Then add one sentence: "What each step prints, on success and on failure, is listed in the `sc-fix-audit` skill (`~/.claude/skills/sc-fix-audit/SKILL.md`); this note does not repeat it." Do not copy `src/superclaude/skills/sc-fix-audit/SKILL.md:37`. Its "only when" is false, because a write failure also prints `APPLY_STOP` (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:880-882`).
5. Write "How the verdict is computed" word for word from attempt-3.diff:44-46. It holds against `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:1025-1053`, `:1077-1092`.
6. Write "Owner count" from attempt-3.diff:48-50, with one change. Replace "which adds every held id that review 2 labelled CRITICAL or MAJOR" with "which adds each held id that review 2 labelled CRITICAL or MAJOR, unless review 3 already counts that id as a new critical or major finding". This matches `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:1057-1062`. Keep "Nothing in the script lowers the owner count" (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:1018-1020`).
7. Write Placement, Owner decisions applied, Variant base and the Unattended-mode deviation, Files, and Install and the experiment Task word for word from attempt-3.diff:52-92. Compare the T08a line byte for byte with `.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:257`.
8. Search the new note. Each of these must give zero hits: `APPLY_STOP`, `CHECK_FAIL`, `nothing written`, `byte-identical`, `every failure`, `on failure`, `Not covered`, `adds every`. The one allowed hit is the pointer sentence from step 4. If anything else matches, delete that sentence; do not reword it.
9. Check each AC1 literal (`.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md:168`) with a fixed-string search, then run `uv run pytest tests/docs -q` and save the output.

The review finding holds up, so I see no grounds to dispute it. The only file to change is `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/docs/designs/spec-panel-ponytail.md`.

| DONE | NEXT |
|---|---|
| Found two false script claims in A3 (the `APPLY_STOP` one and the owner-count one) and wrote a rewrite plan that drops all failure-path wording | The executor follows steps 1-9 and runs the review again |

I did not check that the verdict paragraph's "same tolerant parse as `prepare`" holds for every grade format. I only confirmed that both steps call `parse_report`. `src/superclaude/skills/sc-fix-audit/SKILL.md:37` is still slightly wrong, but T9 is not allowed to change it.
