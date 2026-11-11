model: claude-opus-5-5 family: claude rung: top family-fallback: no GPT spawn path is verified on this install (refs/retry.md, "GPT spawn path: none verified"); the GPT T1 model T1Model02=gpt-6.1-sol could not be reached through the Agent tool, so adviser B ran on the strongest reachable model
outcome: ready
| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T10.AC1 | Both attempts passed (review-2.md:3), but the file still failed review on scope. The drift check undid the planned edits by line text, wherever a line appeared. It dropped any line that started with an inserted prefix or with bullet 8, and mapped the command name back on every line (attempt-2.diff:58-92). So the "any other drift fails" rule in the plan (TASK-WF-spec-20261108-181616.md:136) was not enforced (review-2.md:7). Attempt 1 had the same fault through prefix exemptions (review-1.md:6). | Rebuild the test file. The equality test checks a fixed list of edits, each tied to base line numbers. Re-run and save the log to `artifacts/t10-static.log`. |
| T10.AC2 | The negative cases passed (attempt-2.diff:194-222) only because each one changed a line that no filter matched. A planned line copied somewhere else, or the command renamed outside the title, Usage and Examples, was still excused (review-2.md:7). | The equality test fails on any diff hunk that is not in the edit table, and on a hunk whose base range or variant line count is wrong. Add the AC2 one-character case plus the four cases the reviewer probed and two cases next to the planned edits. |
| T10.AC3 | Met (review-2.md:5; extras-2.log:32-35). This was never the cause of failure. | Re-run the same command after the rebuild and save the output to `artifacts/t10-regression.log`. |
| T10.AC4 | Met (review-2.md:6; attempt-2.diff:9-10). | Make the same one-line change again: add `"spec-panel-stoprule"` to `_POST_REFRESH_ADDITIONS`. |

differs-by: Both earlier attempts edited the variant's text before comparing it (attempt 1 exempted lines, attempt 2 undid edits wherever their text appeared). This attempt leaves the variant text alone, runs `difflib` between base and variant, and requires the diff to be exactly a fixed table of hunks, each tied to base line numbers in the sha256-pinned fixture.

steps:
1. Restore `tests/recommend/test_routing_refresh.py` and change only `_POST_REFRESH_ADDITIONS` to `{"graph", "impact", "issue", "spec-panel-stoprule"}` (the same as attempt-2.diff:9-10).
2. Create `tests/skills/test_spec_panel_stoprule.py`. Keep attempt 2's non-drift tests unchanged in content; review-2 found nothing wrong with them. They are at attempt-2.diff:115-188 and :225-248: base sha256 and 472 lines; frontmatter, title and activation; bullets 1-8 in order; `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]`; the four names; the new wording; no unattended section; no new `src/superclaude`; the uv form; `_has_corresponding_command` False; rubric prefix `dbc4926c7421` (artifacts/t1-rubric-sha256.txt:2); the files exist. Delete `INSERTED_PREFIXES`, `BULLET8`, `REPLACED_IN_PLACE` and the old `drift()`.
3. Add `drift(variant_text, base_text)`. Split both texts with `splitlines()` and get the hunks with `[op for op in difflib.SequenceMatcher(None, base, var, autojunk=False).get_opcodes() if op[0] != "equal"]`. `autojunk=False` is required: with the default, blank lines and code fences count as junk in a 472-line file and the hunks shift. Compare those hunks with a module-level `EXPECTED_HUNKS`, a list of `(i1, i2, [line rules])`. `i1, i2` are 0-based base slice bounds. Each rule is either a literal string or a compiled regex that must match the whole line. Return a list of problems: a hunk not in the table, a table entry with no hunk, a mismatched `(i1, i2)`, a variant slice of the wrong length (`j2 - j1`), or a line that breaks its rule. Build the literals from the base lines, so the test does not copy text from the variant. Define `R = lambda s: s.replace("/sc:spec-panel", "/sc:spec-panel-stoprule", 1)`. The table follows, with base line numbers 1-based from tests/skills/fixtures/stoprule/spec-panel-armb-base.md and the matching variant lines from src/superclaude/commands/spec-panel-stoprule.md:
   - base 2-3 to variant 2-3: literal `name: spec-panel-stoprule`; literal `base[2][:-1] + ' (experimental variant: computed review-loop verdict)"'`.
   - base 10 to variant 10-16 (7 lines): `R(base[9])`, `""`, `"> Skill sc:spec-panel-stoprule-protocol"`, `""`, regex `If the skill is missing at both `~/\.claude/skills/sc-spec-panel-stoprule-protocol/` and `\.claude/skills/sc-spec-panel-stoprule-protocol/` .*`E-SKILL-MISSING`.*`, `""`, regex `This variant deliberately has no `## Unattended mode` section and does not accept `--unattended`.*`.
   - base 22 to variant 28: `R(base[21])`.
   - base 257-262 to variant 263-269 (7 lines): regexes `2\. \*\*Grading\*\*: .+` and the same pattern for `3 Verdict`, `4 Cap`, `5 Re-review output`, `6 Reviser contract`; literal `base[261][:-1] + ", and may not change the rubric or its hash."`; regex `8\. \*\*Procedure\*\* \(critique mode only\): .+`.
   - base 326-327 to variant 333-334: literals `base[325].split(" automatically generates")[0] + " generates a finding; it is blocking only under rubric B1-B3 of the Review Loop, otherwise minor."` and `base[326].split(" is classified")[0] + " generates a finding; it is blocking only under rubric B1-B3 of the Review Loop, otherwise minor."`. Check that both strings equal variant lines 333-334.
   - base 408, 411, 414, 417, 420 to variant 415, 418, 421, 424, 427: `R(base[k])` for each, as five separate 1-line hunks.
   This makes 10 hunks in total. Also assert `len(var) == len(base) + 7`.
4. Run `drift()` once on the real files. If the hunks differ from the table, re-derive only the alignment, so that every hunk is still exactly one planned edit with an exact line count. Never use a regex like `.*`, a range that covers lines with no planned edit, or a text-based exemption. Write the comment and docstring to say only this: "each planned edit is a fixed base line range with an exact variant line count; any other difference adds or widens a hunk." Do not claim the function "removes" anything.
5. Test `test_variant_equals_the_base_outside_the_replaced_blocks`: `assert drift(text(VARIANT), text(BASE)) == []`.
6. Write the negative cases as a parametrized test. Each case edits a tmp_path copy of the variant and asserts `drift(...) != []`:
   - (a) AC2: change one character of an inherited line (`## Behavioral Flow` to `## Behavioural Flow`).
   - (b) an Examples argument change.
   - (c) a Usage flag change.
   - (d) the reviewer's probe: rename `/sc:spec-panel @final_spec.yml` to `/sc:spec-panel-stoprule @final_spec.yml` in Integration Patterns.
   - (e) the reviewer's probe: add a second `> Skill sc:spec-panel-stoprule-protocol` line after `## Integration Patterns\n`.
   - (f) the reviewer's probe: add a copy of the "If the skill is missing at both ..." line in Integration Patterns.
   - (g) the reviewer's probe: add a copy of the bullet-8 line in Integration Patterns.
   - (h) a duplicate activation line right after the existing one.
   - (i) an extra blank line after the no-unattended line.
   - (j) a one-character change in Review Loop bullet 1, which sits next to the replaced block.
   - (k) an extra line right after bullet 8.
   Before each edit, assert that the text being replaced exists.
7. Run `uv run pytest tests/skills/test_spec_panel_stoprule.py -v > artifacts/t10-static.log` and the AC3 regression command `> artifacts/t10-regression.log`. Then run `ruff check tests/skills/test_spec_panel_stoprule.py`. Confirm that `git diff tests/recommend/test_routing_refresh.py` shows the one line only.

Paths:
- /home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/tests/skills/test_spec_panel_stoprule.py
- /home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/tests/recommend/test_routing_refresh.py
- /home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/src/superclaude/commands/spec-panel-stoprule.md
- /home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/tests/skills/fixtures/stoprule/spec-panel-armb-base.md

| DONE | NEXT |
|---|---|
| Found the cause: both attempts excused lines by text, wherever they appeared. Wrote a replacement approach that pins every edit to base line numbers and exact line counts, with 11 negative cases. | Revert attempts 1 and 2, then implement steps 1-7 as attempt 3. |

Not checked: I worked out the hunk alignment by hand and did not run it. Step 4 is there to catch a different alignment, but it must not loosen the table.
