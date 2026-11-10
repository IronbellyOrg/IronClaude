model: claude-opus-5-5 family: claude rung: top (critique adviser, adviser A's model, ladder entry T1Model01, Agent model=opus)
outcome: ready
| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T2.AC1 | The AC's listed tests exist and pass (review-2.md:2, extras-2.log:6). The blocker is F2.1 (review-2.md:5), a scope failure against the brief's rule that "id-shaped tokens R neither defines nor lists are ignored" (TASK-WF-spec-20261108-181547.md:58; source.md:39). A2's `MARKER_RE` strips `-`, `*` and `+` bullet markers (attempt-2.diff:29). `lead_ids` then takes whatever id comes first (attempt-2.diff:28, 83-86). So a bullet such as "- WC-3: ... Not blocking" becomes a graded record. `BLOCKING_RE` (attempt-2.diff:38, 128) reads "Not blocking" as blocking. WC-3 then joins the blocking set that feeds the disposition lines (attempt-2.diff:345-346) and `classify` (attempt-2.diff:285). The comment at attempt-2.diff:162 says free text defines nothing, and that is not true. The fixture has no bullet under a finding (attempt-2.diff:796-807). Its WC-3 assertion (attempt-2.diff:812) is satisfied only by the `Totals:` line. | A prose line defines an id only when the raw line opens with one of three record-lead shapes from F2.1's fix: `**Nk.`, `Nk (` or `Nk.`. Any `-`, `*` or `+` bullet line defines nothing. Rewrite the two grade-format test lines whose leads stop being accepted, and add bullet fixtures plus a `prepare` test of the WC-3 disposition effect. |
| T2.AC2 | Not missed. The byte copy is at attempt-2.diff:349 and `filecmp.cmp(..., shallow=False)` is at attempt-2.diff:607-609. The review marks it met (review-2.md:3). | No change. Re-create it as is. |
| T2.AC3 | Not missed. The imports at attempt-2.diff:17-23 fit the allowlist test (attempt-2.diff:520-540) and the constraint (TASK-WF-spec-20261108-181547.md:31). The review marks it met (review-2.md:4). | No change. The fix uses only `re`. |

differs-by: Neither attempt checked the raw line for a fixed set of allowed record shapes. A2 removed every marker, bullets included, and then accepted the first id left. This approach rejects bullet lines outright and leaves `parse_grade` unchanged. Once bullets are excluded, the "Not blocking" text never reaches a record, so the grade parser needs no change.

steps:
1. Start from Q0. Re-create `src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py` from attempt-2.diff:7-411 and `tests/skills/test_fix_audit_script.py` from attempt-2.diff:418-839.
2. Delete `MARKER_RE` (attempt-2.diff:29). Keep the id-list part of `LEAD_RE` (attempt-2.diff:28), without its `(?![\w-])` tail, as a string `LEAD`. Write it with a literal `&amp;`. Both rejected advice files carry HTML-escaped `&amp;amp;` and `&amp;lt;` in their regexes. Copied as written, those either fail to match `N1 &amp; N2` or fail to compile. Add `BULLET_RE = re.compile(r"^\s*[-*+]\s")` and `RECORD_RE = re.compile(rf"^\s*(?:#+\s*)?(?:[0-9]+[.)]\s+)?(?:\*\*({LEAD})\.|({LEAD})\s*\(|({LEAD})\.(?:\s|$))")`. `**N1.**` is not caught by `BULLET_RE`, because its second character is `*`, not whitespace.
3. Rewrite `lead_ids` (attempt-2.diff:83-86). Return `[]` if `BULLET_RE.match(line)`. Otherwise match `RECORD_RE` and return `id_tokens(&lt;first non-empty group&gt;)`, or `[]` when nothing matches. Its docstring names the three shapes and says that bullets and `ID:` lines define nothing. Replace the comment at attempt-2.diff:162 with "a prose record is a non-bullet line opened by `**ID.`, `ID (` or `ID.`; bullets, totals and notes define nothing". Leave `parse_grade`/`BLOCKING_RE` (attempt-2.diff:38, 122-140) as they are. Making "not blocking" read as minor would make more ids revertible, and no AC asks for it.
4. In the four-format test, change attempt-2.diff:666-668 to `"**C9.** Severity MAJOR, blocking. The table is wrong."`, `"N4 (MAJOR, B): the cap is wrong"` and `"N5 (MINOR, M): wording"`. These keep the "Severity MAJOR, blocking" and keyed `MAJOR, B` formats the AC requires. `KEYED_RE` still matches `B)`. Lines 664-665 and 669 need no change.
5. Insert `"- WC-3: same output location. Not blocking because 2.3 covers it.\n"` right after the `**N1.**` line (attempt-2.diff:800). Then the assertion at attempt-2.diff:812 fails under A2 and passes only with the fix.
6. Add a test parametrized over the markers `-`, `*` and `+`. It parses `R2_HEAD + "**N9.** MINOR, non-blocking: wording.\n" + f"{m} WC-3: the location rule. Not blocking because 2.3 covers it.\n" + R2_TAIL` and asserts that `"WC-3" not in graded` and that `graded["N9"]["blocking"] is False`.
7. Add a `prepare` test:
   - base `"p1\nk1\np2\n"`, current `"p1 N9 tweak\nk1\np2 WC-3 note\n"`, and the step-6 report with the `-` marker;
   - dispositions `"| id | Where |\n|---|---|\n| N9 | SPEC':1 |\n| WC-3 | SPEC':3 |\n"`;
   - assert that `"WC-3" not in state["ids"]`, that the classes are `["minor-only", "unattributed"]`, and that `state["audit"] == "prepared"`.

   Under A2 the second hunk would be `blocking-involved`.
8. Run `uv run ruff check` on both files and `uv run pytest tests/skills/test_fix_audit_script.py -q`. Expect the 46 existing tests (extras-2.log:6) plus the new ones to pass. Save the output to the package artifacts as before.

I ran no code, so the regex is untested. A real report that opens graded records with `ID:` or as bullets would now leave those hunks `unattributed`, which can trip the skip guard. F2.1 prescribes exactly this narrowing (review-2.md:5).

| DONE | NEXT |
|---|---|
| Confirmed that F2.1 is supported by attempt-2.diff and the brief. Wrote the attempt-3 approach using only allowed citations, and found the `&amp;amp;`/`&amp;lt;` escaping defect in both rejected advice files. | The parent hands these steps to the attempt-3 executor, starting from Q0. |

Relevant files:
- /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/artifacts/retries/T2/attempt-2.diff
- /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/artifacts/retries/T2/review-2.md
- /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md
- /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md
