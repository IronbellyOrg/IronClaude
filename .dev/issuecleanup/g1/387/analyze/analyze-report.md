# Bare-Python hook architecture analysis

Structure: Analysis template in ../../362/report-template.md, read before creating this stub.

## Scope and grounding
Command: `/sc:analyze src/superclaude/hooks/scripts/block-bare-python.sh --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/387/analyze`.

The single hook is the narrowest source target covering both issue 387 paths. Read all 344 lines plus relevant test, registration, installer and changelog excerpts. Checkout HEAD: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:06:37Z; degraded: graph:empty.

Access: mcp. The shell file is not indexed: its outline lookup returned no indexed file, and the directory listing returned only one JavaScript file. Static conclusions therefore use direct source reads and searches, not graph caller counts.

## Architecture and metrics
The hook extracts a Bash command from JSON with jq, scans text using one embedded awk state machine, then returns 2 only for a recognized bare Python/pip command and otherwise returns 0. Input commands are data, not executed by the scanner. See /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/block-bare-python.sh:331-344.

The script has 344 lines. Parsing uses command-position, wrapper, quote, arithmetic, substitution and heredoc states; shell-fed heredocs take a special route that bypasses heredoc expansion scanning. The registration is a Bash PreToolUse hook with a 3-second timeout (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:95-102), and the installer lists the script (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_hooks.py:81-85). Source and plugin mirror compare byte-identical. The last hook/test change is original merge `605da2ffb83b93302ca51d654e9c2075e85217a7` (PR 359).

Regression tables distinguish blocked/allowed/fail-open inputs; dedicated tests cover 100 KB under one second and 200 KB input (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_block_bare_python.py:250-268). No test count or timing was measured during this static command.

## Severity-rated findings
1. **Medium, policy-enforcement defect: unquoted shell heredocs miss parent-shell substitutions.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/block-bare-python.sh:136-141 skips heredoc handling when the recipient is a shell. Its body is consequently treated as shell commands, where single quotes suppress substitution scanning (:261-264). In an unquoted heredoc, those quotes are literal to the parent shell, which still expands `$(...)` and backticks. Existing heredoc expansion handling (:286-292) is not reached for this branch.
2. **Medium, policy-enforcement defect: named coprocess consumes the name as the executable.** The same file :84-86 classifies coproc as a normal wrapper; :130-134 then consumes `worker` as the command word and clears command-needed state. The opening brace cannot reset that state, so a first bare Python command in the body is missed. This is distinct from an unnamed coprocess, whose brace can still be skipped while command-needed state remains active.
3. **Medium, coverage gap: the failing combinations have no regression entries.** /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_block_bare_python.py:80-143 covers an unquoted heredoc into cat, a quoted heredoc into bash and function bodies, but not the reported unquoted shell-heredoc combination or any coproc case. Current header text (:41-45 in the hook) describes both shell-body and parent-expansion handling without identifying their interaction gap.

These are local development-policy failures, not evidence of a remotely exploitable security boundary. Other documented ceilings and fail-open behavior remain intentional scope limits.

## Recommendations and roadmap
Follow the owner's 2026-11-17 issue comment: repair the two parser paths, not a broader word-matching redesign. Handle parent expansion and child-shell interpretation as separate heredoc obligations; handle coproc as shell syntax with an optional name rather than as a generic executable wrapper. Add focused blocked/allowed regressions, retain performance/fail-open checks and byte-identical plugin mirroring, and update the hook header and changelog. No source was changed.

## Verification limits
Static quick architecture review only; no compilation, application execution, test suite or fuzzing ran as part of this command. Graph call-path and impact evidence is unavailable for this unindexed shell file. Installed user-home behavior and remote default-branch freshness are UNVERIFIED; the review uses this supplied checkout. Task-level supplemental scanner-only probes and regression tests, if run afterward, are recorded separately in findings.md.
