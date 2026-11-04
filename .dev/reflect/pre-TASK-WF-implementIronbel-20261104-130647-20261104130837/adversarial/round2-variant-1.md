# Round 2 — Variant 1 rebuttal (analyzer, sonnet)

## Steelman
- V3: three places where line 37 diverges from the Done-when (comments, heredoc bodies, `$(` in double quotes) share one quote-tracking weakness: an apostrophe flips quote state and hides a later real python3 call (undocumented false negative).
- V2: two self-contradictions (R2-F1, R2-F2) plus the only jq-missing test request (line 21 vs line 60).

## Response to criticisms
- R1-F5 mention vs execution: CONCEDED for `$(` and backticks. `x="$(python3 -c ...)"` executes; line 19 exempts only commands that only mention python; line 37 contradicts the Done-when for this form. Upgraded to blocking. `bash -c`, `eval`, `xargs`, `find -exec` stay minor documented ceilings. Must pair with heredoc handling: once `$(` in double quotes is scanned, `git commit -m "$(cat <<'EOF' ... EOF)"` bodies are scanned (line 40).
- C-001 deletes the pin: MOSTLY REBUTTED. Test name (line 91) shows the target is the freshness counter; the positive invariant already exists in Task 4 line 90; V2's extra pin is brittle. Conceded: tighten to "no Bash-matcher registration whose command contains `freshness-`" and name the supersession in the PR body.
- X-001/X-003 severity: CONCEDED for X-003 apostrophe half (blocking: hides a following python3 call; same mechanism for `# don't` comments). Minimal fix: no quote tracking inside heredoc bodies or comments, keep splitting at newlines. X-003 text FP half stays a documented ceiling (minor). X-001 held minor: line 37 "backslash escapes honoured" read literally means escaped newline is not a separator; still needs one allowed and one blocked continuation test.

## Updated assessment
- V3 better than credited; its lexer analysis is the most important set of findings.
- V2 accurate but thin; merge R2-F3 with R3-F7; R2-F5 unverifiable.
- V1 weaker than claimed in Round 1: R1-F5 under-graded; R1-F11, R1-F9 low value.

## New evidence
1. tests/hooks/test_freshness_subagent_start_policy.py:102-105 is the only `matcher == "Bash"` assertion in tests/; other PreToolUse mentions are in tests/cli/eval/* (not checked whether real hooks.json or fixtures); directory runs of tests/hooks and tests/cli are cheap insurance.
2. Quoted-substitution form exists in repo shell: src/superclaude/skills/ccsession-tag/ccsession:1008 `echo "Valid profiles: $(python3 "$CCSESSION_MODELS" profiles | ...)"` (script, not an agent Bash call).
3. Timing: mawk 1.3.4 per-character substr loop with a quote toggle over a 100 KB line ran in ~12 ms (lower bound; no heredoc/comment/nesting logic), ~250x under the 3 s timeout.

## Updated per-point table (changed only)
| Point | New superior | Reason |
|---|---|---|
| C-001 | V1 assertion, V3 run scope | retarget to freshness- Bash registrations; name supersession; run tests/hooks and tests/cli directories |
| C-003 | V3 | apostrophe desync undocumented FN; blocking for that half |
| C-004 | V3 | same desync in comments; blocking for desync only |
| C-006 | V3, blocking | Done-when violated; pair with heredoc handling |
| C-008 | V3 design, V2 test | exit-2-only-on-positive + jq-missing test; add awk-missing case |
| X-002 | V3 | verbatim Done-when governs |
| X-003 | V3 apostrophe half, V1 text half | as above |

## Shared assumptions
- A-001: QUALIFY — Necessary deviation caused by Task 3; must still reject a freshness-counter Bash hook; PR body says so.
- A-002: REJECT — plan not edited from reflect findings; fixes land as implement-time amendments recorded in progress.md.
- A-003: QUALIFY — pre-passes fit; awk state machine viable on timing; plan should say awk is acceptable.
