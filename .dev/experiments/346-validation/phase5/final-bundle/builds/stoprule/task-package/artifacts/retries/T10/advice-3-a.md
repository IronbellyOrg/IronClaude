model: claude-opus-5-5 family: claude rung: top (ladder entry T1Model01, primary ladder; executor tier T1Model01, so adviser A is the top rung)
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T10.AC1 | Attempt 2 passed it (review-2.md:3, extras-2.log:30), but its test file had the blocking scope finding (review-2.md:7) and is being reverted. The cause was in `drift()`. It dropped any line starting with an inserted prefix or `8. **Procedure**`, wherever that line appeared (attempt-2.diff:60-65, :86-91). It also renamed `/sc:spec-panel-stoprule` back on every line (attempt-2.diff:92). The comment at attempt-2.diff:58-59 and the docstring at attempt-2.diff:75 therefore made false claims. Attempt 1 failed the same way, excusing lines by prefix anywhere in the file (review-1.md:6). | Rebuild the file with a fixed-position equality test. Every planned edit is tied to a base line number. Every other base line must appear at its shifted position, byte for byte. |
| T10.AC2 | Attempt 1 had no case that caught an edit to Examples or Integration Patterns (review-1.md:6). Attempt 2's six negative cases (attempt-2.diff:194-222) never tried an inserted line or the renamed command in the wrong place. Four probe mutations passed its test (review-2.md:7). | Keep the one-character case. Add one negative case for each of the four probes in review-2.md:7, plus a few more (step 4). |
| T10.AC3 | Passed in attempt 2 (review-2.md:5, extras-2.log:34). It is lost only because of the revert. | Re-run the same command and save the output. |
| T10.AC4 | Passed in attempt 2 (review-2.md:6, attempt-2.diff:9-10). It is lost only because of the revert. | Make the same one-line change. |

differs-by: The comparison is by position, not by filter. A table keyed by base line number says where each planned edit may sit (base fixture lines 2, 3, 10, 22, 257-262, 326, 327, 408, 411, 414, 417, 420, plus 6 inserted lines after base 10 and 1 after base 262). Every line in a renamed or computable slot must equal a value worked out from the base line. Nothing is deleted from, or renamed throughout, the variant before comparing.

steps:
1. Restore `tests/recommend/test_routing_refresh.py` with only `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue", "spec-panel-stoprule"}` changed (as in attempt-2.diff:9-10).
2. Create `tests/skills/test_spec_panel_stoprule.py`. Keep attempt 2's non-drift tests, since review-2.md:3-6 found them sound:
   - base sha256, line count of 472, no `## Unattended mode`;
   - frontmatter, title, activation line, `E-SKILL-MISSING`, and both skill paths in order;
   - Review Loop bullets 1-8 in order, with names Mode … Procedure;
   - `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` imported from `tests.skills.test_review_severity_rule`, plus the tokens `stoprule.py`, `sc-spec-panel-stoprule-protocol`, `verdict: PASS` and `verdict: FAIL`;
   - exactly one line containing `--unattended`, and it contains "does not accept `--unattended`";
   - no `src/superclaude` in SKILL.md, refs/rubric.md or finding-grader.md, and the variant's `src/superclaude` count equals the base's;
   - SKILL.md uses `uv run --no-project python "<skill base>/scripts/stoprule.py"`;
   - `install_skills._has_corresponding_command("sc-spec-panel-stoprule-protocol") is False`;
   - the rubric sha256 prefix equals the 12-hex literal copied from `.dev/tasks/to-do/TASK-WF-spec-20261108-181616/artifacts/t1-rubric-sha256.txt`. Read that file; do not copy the value from memory.
3. Replace `drift()` with a builder that works by position. Split both texts with `.split("\n")` so a change to the trailing newline is caught too. Walk the base by 1-based line number `n` and build a list of expected lines, where each entry is either an exact string or a shape check:
   - n=2: exact `name: spec-panel-stoprule`.
   - n=3: exact `base[2][:-1] + ' (experimental variant: computed review-loop verdict)"'`.
   - n in `RENAMED = {10, 22, 408, 411, 414, 417, 420}` (title, Usage, Examples): exact `base_line.replace("/sc:spec-panel ", "/sc:spec-panel-stoprule ", 1)`. Assert the result differs from the base line, so a wrong number fails loudly. Integration Patterns lines 428-434 are not in the set, so a rename there fails.
   - After n=10, insert 6 slots, in order: exact `""`; exact `> Skill sc:spec-panel-stoprule-protocol`; exact `""`; starts with `If the skill is missing at both `; exact `""`; starts with "This variant deliberately has no `## Unattended mode` section".
   - n=257..261 become 5 slots that each start with `f"{k}. **{name}**"` for k=2..6: Grading, Verdict, Cap, Re-review output, Reviser contract.
   - n=262 becomes exact `base_line.removesuffix(".") + ", and may not change the rubric or its hash."`. Then insert 1 slot starting with `8. **Procedure** (critique mode only): `.
   - n=326: exact `base_line.replace("automatically generates a finding with **MAJOR** severity minimum.", RULE)`.
   - n=327: exact `base_line.replace("is classified as **MAJOR** severity minimum.", RULE)`. Here `RULE = "generates a finding; it is blocking only under rubric B1-B3 of the Review Loop, otherwise minor."`.
   - Every other n: exact `base_line`.

   `drift()` returns a line-count mismatch entry if the lengths differ (479 vs 480, for example). It then returns `(line_no, expected, actual)` for every position where the actual line fails its exact value or shape check. Comment and docstring: "planned edits are allowed only at these base line numbers; the same text anywhere else is drift". This keeps both accurate, which F2.1 also required.
4. Positive test: `drift(text(VARIANT), text(BASE)) == []`. Add a parametrized negative test that applies `body.replace(old, new, 1)` to a tmp_path copy. First assert `body.count(old) >= 1`, then assert `drift(...) != []`. Cases:
   - (a) `## Behavioral Flow` → `## Behavioural Flow` (the AC2 one-character case);
   - (b) `--focus requirements,architecture\n` → `--focus requirements\n`;
   - (c) `[--iterations N]` → `[--iteration N]`;
   - (d) `/sc:spec-panel @final_spec.yml` → `/sc:spec-panel-stoprule @final_spec.yml`;
   - (e) `## Integration Patterns\n` → `## Integration Patterns\n\n> Skill sc:spec-panel-stoprule-protocol\n`;
   - (f) the same anchor plus the variant's own bullet-8 line, taken at runtime from `review_loop_bullets(body)[7]`;
   - (g) the same anchor plus the variant's own `If the skill is missing at both ...` line, taken at runtime;
   - (h) `> Skill sc:spec-panel-stoprule-protocol\n` duplicated in place;
   - (i) `## Integration Patterns\n` → `## Integration Patterns\n\n`;
   - (j) `(experimental variant: computed review-loop verdict)` → `(experimental variant)`.
5. Run `uv run pytest tests/skills/test_spec_panel_stoprule.py -v` and save the output to `.dev/tasks/to-do/TASK-WF-spec-20261108-181616/artifacts/t10-static.log`.
6. Run `uv run pytest tests/skills/test_review_severity_rule.py tests/unit/test_cli_install.py tests/recommend/test_routing_refresh.py tests/skills/test_primitive_dual_surface_lookup.py tests/skills/test_worker_contract.py tests/skills/test_spec_panel_review_loop.py -q` and save the output to `.../artifacts/t10-regression.log`. Then run `git diff --stat` to confirm the four protected test files are unedited, and `git diff tests/recommend/test_routing_refresh.py` to confirm only that one line changed. Run `ruff check` on the new file.

| DONE | NEXT |
|---|---|
| Found the cause: both attempts filtered lines by content, so the same text anywhere in the file passed. Checked the new line numbers against the variant (479 lines) and the base (472 lines). | The implementer rebuilds attempt 3 from these steps. |

Not checked: I did not run the new builder, and I did not open `t1-rubric-sha256.txt` (step 2 says to read it). The relevant files are `/home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/src/superclaude/commands/spec-panel-stoprule.md` and `/home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/tests/skills/fixtures/stoprule/spec-panel-armb-base.md`. Risk: the line-number table needs editing whenever the variant or base changes, but that is the point of the test.
