model: claude-opus-5-5 family: claude rung: top family-fallback: GPT T1 model gpt-6.1-sol (T1Model02) has no verified spawn path on this install (refs/retry.md "GPT spawn path: none verified"); spawned on the strongest reachable model, Agent model=opus
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T9.AC1 | The review found every required literal present (`review-2.md:3`). The block was a scope finding against the Safe apply bullet "Every failure path leaves the specification byte-identical..." (`attempt-2.diff:37`, `review-2.md:5`). A1 copied that line from the design (`.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:47`), and A2 kept it while fixing a different sentence (`attempt-2.diff:36`). The live script does not do what the line says. The spec is replaced at `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:877`. Then `apply-log.md` and `closed-minor.txt` are written with no handler (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:898-901`). The state was already set to `checked` (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:732`, reached from `:785`). | Keep every literal. Replace the blanket line with one sentence per path, each matching its code. (1) A check failure or an `APPLY_STOP` happens before the spec is written, so the spec stays byte-identical to `current-before-audit.md` (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:785-794`, `:859-870`). (2) If the spec write or its read-back fails, the script copies `current-before-audit.md` back over the spec and stops (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:876-882`). (3) The writes after a successful spec write are not guarded. If writing `apply-log.md` or `closed-minor.txt` fails, the spec stays edited and `state.json` still says `checked`. The fix is to copy `current-before-audit.md` over the spec (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:898-903`). |
| T9.AC2 | It was not missed: 11 tests passed (`review-2.md:4`, `extras-2.log:2-4`). The rewrite only has to keep it passing. | Run `uv run pytest tests/docs -q` after the rewrite and save the output to `./artifacts/t9-pytest-3.log`. |

differs-by: the note states each failure path's outcome separately and names the unguarded writes after the spec is replaced, instead of repeating the design's blanket "every failure path" claim (`.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:47`).

steps:
1. Recreate `docs/designs/spec-panel-ponytail.md` with A2's structure and headings (`attempt-2.diff:7-87`). Keep these as they are, since the review found nothing wrong in them (`review-2.md:3`):
   - the title and status (`:7-9`); `.dev/brainstorms/346-ponytail/SPEC.md` exists, so the pointer is accurate;
   - "What it is" and the loop table with the trigger sentence (`:11-29`);
   - verdict (`:39-41`), owner count (`:43-45`), placement (`:47-49`) and the four owner decisions (`:51-56`);
   - variant base and Unattended-mode deviation (`:58-60`) and files (`:62-75`);
   - install and the T08a section (`:77-87`).
2. Copy the T08a command line byte for byte from `.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:257` into a `text` fence. Type nothing by hand.
3. In "What it is" (`attempt-2.diff:13`), change "makes every edit, all or nothing" to "applies every accepted edit in one atomic write of the specification" (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:871-877`). This keeps "all or nothing" from covering the log writes.
4. In Safe apply, keep the bullets of `attempt-2.diff:33-36`, with one change to the first bullet: "the auditor writes only `fix-audit/audit.md`" becomes "the auditor brief allows only `fix-audit/audit.md`; check K1 fails the audit if the spec's sha256 changed since `prepare`" (`src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:586-587`).
5. Replace `attempt-2.diff:37` with the three sentences in the T9.AC1 row. Do not use "every", "always" or "never" about failure paths.
6. Grep the note for `every failure`, `byte-identical` and `all or nothing`. Each remaining hit must sit in a sentence that names a guarded path from step 5.
7. Check that these literals are present: `/sc:spec-panel-ponytail`, `--fix-audit`, `sc-fix-audit`, `fix_audit.py verdict`, `owner count`, `spec-panel-post427-95f2c6e4.md`, the Unattended-mode sentence, and the T08a line. For the T08a line, `grep -cxF` against the note must print 1.
8. Run `uv run pytest tests/docs -q` and save the output to `<pkg>/artifacts/t9-pytest-3.log`. Change no file other than `docs/designs/spec-panel-ponytail.md`, and leave `fix_audit.py` as it is.

Not checked: `.dev/brainstorms/346-ponytail/INSTALL.md` does not exist yet, so the note points to a file a later task creates. The restore at `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:881` can fail too, which is why step 5 says what the script does there rather than promising the result.
