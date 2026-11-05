# Round 2 — Variant 3 rebuttal (refactorer, opus)

## Steelman of the criticisms
- Line 40 openly accepts text-only heredoc blocking; grading a stated limit blocking punishes a declared trade-off.
- Line 37 "backslash escapes outside single quotes are honoured" means an escaped newline is not a separator.
- Only one hooks.json reader actually breaks; directory runs are insurance.
- F3 vs F10 inconsistent.

## Response to criticisms
1. R3-F4 / X-001: CONCEDED. Modelled line 37 literally: `uv run --no-project \<nl> python x.py` is one simple command (word `uv`), allowed. Defect only if implemented line-at-a-time (awk default record mode) or newline-split before quote tracking. Regraded minor; one allowed continuation test pins it.
2. R3-F2 text half: PARTLY CONCEDED. Not blocking, but line 40 understates real behaviour: any unquoted backtick, `(`, `;` or `|` in a body line also creates a command word (awk model blocks ``Run `python3 x.py` to reproduce`` inside `cat > notes.md <<'EOF'`). Header comment must describe real behaviour; one pinning test. Apostrophe-desync half stays blocking.
3. R3-F3 vs R3-F10: RESOLVED — F3 blocking only for the quote desync; FP half minor. Correction: read-parse.md:7 and :9 comments contain `;` but produce no python FP (next words `FUSE`, `never`).
4. Missed C-002 and the jq-missing test: CONCEDED (R3-F8 guard is test-runner env, not the hook's branch).
5. Directory-run scope: CONCEDED. Readers checked: test_auggie_flag_clear_mcp_prefix.py:128 (PostToolUse only), test_ccsession_tag.py:3145 (UserPromptSubmit/SessionEnd membership), tests/cli/eval/test_hook_adapter.py (byte checksum), test_install_hooks.py:740 (filters freshness by name). Load-bearing fix: add tests/hooks/ to Task 4.

## New evidence
1. The standard commit form is wrongly blocked under the plan as written, even without R3-F5. Line 37 gives `$(` inside double quotes no new quoting context, so a double quote inside the heredoc body flips the tracker. Awk model on
   ```
   git commit -m "$(cat <<'EOF'
   fix(hooks): block "echo x | python3 -c" calls
   EOF
   )"
   ```
   yields command words `git` and `python3` -> blocked. In bash this is quoted text. Violates Done-when (line 19) and line 37's own commit-message example; the only allowed commit test (line 58) is single-line with no inner quotes.
2. Coupling reversed: the FP already exists, so document-and-pin R3-F5 is insufficient. Fix = one stateful scanner: `$(` and backticks inside double quotes open a nested context with fresh quote state (R3-F5); a quoted-delimiter heredoc whose command word is not a shell has a literal body (R3-F2).
3. jq regex cannot track a context stack; plan should require awk (line 41 offers both). V1's ~12 ms timing makes awk viable; Task 2's 100 KB case guards the budget.
4. R2-F5 independently verified (INF-007 -> Task 1 tie; INF-010 -> Task 3).

## Updated assessment
- V1 strongest Round 2; its line-37 reading confirmed; its C-001 fix is load-bearing.
- V2 accurate, fully verified; lasting: tests/hooks omission, jq-missing PATH-shim test.
- V3 owns lexing; double-quote context causes FPs on the most common agent command form; loses X-001 and C-001 run scope.

## Updated per-point table (changed only)
| Point | New superior | Reason |
|---|---|---|
| C-001 | V1 (assertion and run scope) | tests/hooks/ in Task 4 is load-bearing; supersession in PR body |
| C-003 | V3: desync blocking; text half minor with corrected docs | line 40 understates; commit-form FP |
| C-004 | V3, blocking for desync only | FP half minor |
| C-005 | V1 (minor, one test) | literal rule handles continuation |
| C-006 | V3, blocking; document-and-pin withdrawn | ship with C-003 as one scanner |
| C-008 | V3 design and V2 test | exit 2 only on positive; PATH-shim test |
| C-017 | V2, verified | matrix rows |
| X-001 | V1 | conceded |
| X-003 | V3 desync + commit-form FP; V1 severity for text half | as above |

## Shared assumptions
- A-001: QUALIFY — necessary deviation; narrowed test rejects a Bash registration whose command contains `freshness-`; PR body says so.
- A-002: REJECT — fixes are /sc:implement amendments recorded in progress.md.
- A-003: QUALIFY — pre-passes cheap; nested context and quoted heredocs need a stateful awk scanner; require awk; Task 2's 100 KB case must pass with the full scanner.
