# Implement-time amendments (from the advisory /sc:reflect pre-review)

The plan file is not edited (the /sc:workflow protocol forbids editing it from reflect findings). These amendments come from the merged reflect verdict
`.dev/reflect/pre-TASK-WF-implementIronbel-20261104-130647-20261104130837/adversarial/merged-verdict.yaml` and are applied during /sc:implement inside the task they belong to. Kept outside `progress.md` so the ledger stays strictly in the ledger grammar.

| Id | Grade | Applied in | Amendment |
|----|-------|-----------|-----------|
| AMD-01 | blocking | T4 | `tests/hooks/test_freshness_subagent_start_policy.py:102-105` asserts no PreToolUse `matcher == "Bash"` registration; Task 3 adds one. Replace the assertion with an allowlist (Bash-matcher PreToolUse commands == {block-bare-python.sh}), keeping the "no Bash counter hook" intent; run `tests/hooks/` in Task 4. Named as a Necessary deviation in the PR body. |
| AMD-02 | blocking | T2 | Add allowed `;`-chained cases (`ls; uv run python x.py`, `echo a; echo python3`, `uv run python a.py && echo python3`) so Task 2's chained-forms criterion is met. |
| AMD-03 | blocking | T1, T2 | Tokenizer is one stateful awk scanner reading the command on stdin (not `awk -v`, not env), `LC_ALL=C`: quote states incl. `$'...'`; `#` comments; per-state backslash-newline; `$(` and backticks (also inside double quotes) as nested contexts whose `)` resumes the outer word; `$((`/case `)` not command contexts; heredocs `<<`, `<<-` (tab-stripped terminator), not `<<<`; quoted-delimiter bodies literal unless fed to a shell command word; unquoted-delimiter bodies with literal quotes but scanned `$(`/backticks; dequoted command word. Tests for each. |
| AMD-04 | blocking | T1, T2 | `x="$(python3 -c 1)"` and backtick/nested forms are blocked (ships with AMD-03). |
| AMD-05 | blocking | T2 | Every Done-when bullet holds against the full scanner (all listed E-cases blocked; `ls -d $(pwd)/bin/python3` and the multi-line `git commit -m "$(cat <<'EOF' ...)"` form allowed). |
| AMD-06 | medium | T2 | Keep the under-1-second timing case with the full scanner; add a ~200 KB stdin command ending in `; python3 x` that must exit 2. |
| AMD-07 | medium | T1, T2, T6 | Exit 2 only on a positive scanner block, exit 0 otherwise; PATH-shim jq-missing test asserting exit 0 and a jq-branch-only stderr marker; jq precondition stated in the CHANGELOG entry. |
| AMD-08 | medium | T7 | Live check with `--allowedTools` instead of `bypassPermissions`, `--append-system-prompt` to drive the bare call, no `--bare`; a refusal or rewrite is recorded as blocked, never a pass; review jsonl artifacts before staging. |
| M-CONSTRAINTS | minor | all | Constraints line 20 "Task 6" means Task 7 (the live check). |
| R1-F7 | minor | order | Run Task 1 before Task 5 and Task 5 before Task 6 (source order already does this). |
| R1-F10 | minor | T4 | Install test also runs with HOME monkeypatched to tmp_path and no target_path. |
| M-CEILINGS | minor | T1, T6 | Documented ceilings (bash -c/sh -c strings, eval, xargs, find -exec, option-taking and path-form wrappers, leading redirections, heredoc piped to a shell, Monitor tool, jq missing, `claude --bare`) listed in the hook header and CHANGELOG. |
