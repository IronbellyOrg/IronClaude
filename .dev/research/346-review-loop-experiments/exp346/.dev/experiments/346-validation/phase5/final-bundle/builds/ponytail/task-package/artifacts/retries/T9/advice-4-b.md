model: claude-opus-5-5 family: claude rung: top (T1Model01; Agent model=opus; escalation 2 uses two top-rung advisers)
outcome: ready

| AC | Why earlier attempts missed it (path:line) | Change |
|---|---|---|
| T9.AC1 | No attempt missed the literals. Attempt 3 met this AC (review-3.md:3): `/sc:spec-panel-ponytail` at attempt-3.diff:7, `--fix-audit` and `sc-fix-audit` at attempt-3.diff:13, `fix_audit.py verdict` at attempt-3.diff:26, `owner count` at attempt-3.diff:50, the T08a line at attempt-3.diff:89 (equal to .dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:257), and the Unattended sentence with `spec-panel-post427-95f2c6e4.md` at attempt-3.diff:65. The run failed on scope. Attempt 3 wrote its own list of failure paths (attempt-3.diff:37-42). One line of it, attempt-3.diff:40, says an exact-once failure prints `APPLY_STOP`, but the re-run check stops it first (src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:785-787, :509-511, :704-707). That failure was flagged as F3.2 (review-3.md:5). The same note has a second unflagged mismatch. attempt-3.diff:50 says the owner count "adds every held id", but the code skips a held id that review 3 already counts (src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:1058-1062). The fix that F3.2 proposes would not work either. It copies SKILL.md's sentence that `APPLY_STOP` appears "only when the apply step itself finds such a failure" (src/superclaude/skills/sc-fix-audit/SKILL.md:37), but apply also prints `APPLY_STOP` when the write fails (src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:880-882). | Keep every literal above in the same wording. Remove all text about failure paths and printed failure lines. Every sentence that is left and describes what the script does must match a fix_audit.py line listed in Steps, or it is deleted. |
| T9.AC2 | Met every time: review-3.md:4, extras-3.log:2 (11 passed). | No change in method. Rerun `uv run pytest tests/docs -q` on the rewritten note. |

differs-by: The note describes no failure path and no failure output at all, neither as one blanket claim nor as a list of steps. It records only the decisions of the listed source sections, and each behaviour sentence that is left is checked against a named fix_audit.py line before it is written.

Steps:
1. Start from an empty `docs/designs/spec-panel-ponytail.md`. Do not use attempt-3.diff as a template. Use the source lines named below and copy only the sentences these steps allow.
2. Title and status line. Use the title from attempt-3.diff:7 (it holds `/sc:spec-panel-ponytail`). The status sentence says the variant is additive and not routed (.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md:28).
3. "What it is" section. Shorten .dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:16 and keep `--fix-audit`, `ponytail:ponytail-review`, `fix_audit.py` and `sc-fix-audit`. You may state:
   - K1 fails if the spec's sha256 changed (fix_audit.py:586-587).
   - Every edit is one temp-file write followed by `os.replace` (fix_audit.py:757-766, :877).
   - A revert puts back the baseline lines, never text the model wrote (fix_audit.py:822-826).

   Do not write "all or nothing", "nothing written" or "byte-identical" anywhere.
4. "The loop" section. Copy the 9-row table from .dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:20-30. Row 8 must contain `fix_audit.py verdict --dir <D> --report <R3>`. Then add one trigger sentence that matches fix_audit.py:328-343: a line starts with `review: 2 of 3`; the last non-empty line is `verdict: FAIL`; spec and baseline can be read; the diff ignoring whitespace-only lines is not empty. Otherwise `prepare` writes `audit: not-triggered(<reason>)` to `fix-audit/state.json` and exits 0. Do not add "changes nothing".
5. "Safe apply: decisions" section. Use exactly four bullets, taken from .dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:121-126:
   - Only `apply` edits the spec. `--fix-audit` is the consent. The pre-audit copy is `fix-audit/current-before-audit.md` (fix_audit.py:357).
   - A hunk is reverted only when every id on it has verdict revert. Otherwise the log shows `REVERT_SHARED <id>` (fix_audit.py:810-817, :839-843).
   - Edit rows are `delete` or `restore`, with exact-once `old` text.
   - Neither a blocking id nor a protected id is ever reverted (fix_audit.py:673-684). A validated-minor grade on an id that review 2 graded blocking is only logged as `DOWNGRADE` (fix_audit.py:653-654).

   Then one plain pointer sentence: "What each step prints and does when it fails is in `src/superclaude/skills/sc-fix-audit/SKILL.md`." Do not quote or paraphrase SKILL.md.
6. "Verdict" section. Allowed content only:
   - The command line with `[--report-rule 427|any-severity]`.
   - Open = prior findings that review 2 graded blocking and review 3 lists `open` or `regressed`, plus new blocking findings (fix_audit.py:1039-1047).
   - A closed id that review 3 grades blocking gives `consistency: DISAGREE` and FAIL (fix_audit.py:1048-1053, :1082-1084).
   - An unreadable or unparseable report gives exit 2 and `verdict: FAIL` (fix_audit.py:1027-1037, :1084, :1092).
   - A report line of FAIL is never turned into a PASS (fix_audit.py:1085-1088).
   - In `any-severity` mode the report's own last line is printed as `t09-verdict:` (fix_audit.py:1077-1078).

   Leave out any clause about how unknown grades are treated.
7. "Owner count" section. State the owner decision (.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md:21) and the three output lines (fix_audit.py:1071-1075). Use this wording: "the owner count adds each held id that review 2 labelled CRITICAL or MAJOR, unless review 3 already counts it as a new critical or major finding" (fix_audit.py:1057-1062). Keep "Nothing in the script lowers the owner count" (fix_audit.py:1018-1019).
8. "Placement" section. Write the recommendation and the bottom line from .dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:155 and :157, then the four owner decisions from .dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md:21-24.
9. "Variant base and Unattended mode" section. Name the 472-line base `spec-panel-post427-95f2c6e4.md`, its sha256 and the fixture copy (TASK-WF-spec-20261108-181547.md:27). Add one sentence saying the variant omits `## Unattended mode` and why: it would fail `tests/skills/test_worker_contract.py`, and the brief guard would refuse the T08a line (TASK-WF-spec-20261108-181547.md:26). It also says `--unattended` is not supported.
10. "Files" table. Use the rows of source.md:180-186 with the plan's additions (fixture, routing test; TASK-WF-spec-20261108-181547.md:28, :136-138). Add "no plugin mirror, no routing row" (TASK-WF-spec-20261108-181547.md:29).
11. "Install" section. Give the steps directly from source.md:253: copy the two paths, `~/.claude/commands/sc/spec-panel.md` is never touched, rollback deletes the two paths. Then say "Full install note: `.dev/brainstorms/346-ponytail/INSTALL.md`." Do not describe what INSTALL.md contains, because Task 11 writes it later.
12. "Experiment Task" section. One sentence saying a name substitution alone does not work, so T08a is inserted between T08 and T09 (source.md:254). Then a fenced `text` block holding source.md:257 byte for byte, then the recorder's verdict line from source.md:260.
13. Self-check before finishing. For every sentence that contains a printed token in backticks (`audit:`, `CHECK_`, `APPLY_`, `verdict:`, `consistency:`, `DOWNGRADE`, `REVERT_SHARED`, `t09-verdict:`) or a verb describing what the script does, find its fix_audit.py line from steps 3-7. Delete the sentence if there is none. Search the note for `nothing written`, `byte-identical`, `APPLY_STOP`, `CHECK_FAIL`, `every failure` and `adds every`; each must return nothing.
14. Grep for the T9.AC1 literals and compare the T08a line with source.md:257. Then run `uv run pytest tests/docs -q`. Edit no other file.

---

| DONE | NEXT |
|---|---|
| Found the cause: attempt 3's own list of failure paths, plus a second wrong owner-count sentence (attempt-3.diff:50) that the review did not flag | The executor reverts the note and rewrites it with steps 1-14 |
| Checked the reviewer's proposed fix: it would copy SKILL.md:37's "only" claim, which the write-failure branch (fix_audit.py:880-882) contradicts | Separately from T9, someone may want to correct SKILL.md:37, which T9 is not allowed to edit |

I did not check fix_audit.py's `parse_report` or `unlabelled_blocking`, so step 6 tells the executor to leave out grade-handling detail. INSTALL.md is not checked yet, so step 11 only points to it.
