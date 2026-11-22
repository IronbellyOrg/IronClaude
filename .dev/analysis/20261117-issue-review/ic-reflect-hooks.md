# Cluster ic-reflect-hooks (review of 2026-11-17)

| Issue | Title | Verdict | Comment | Evidence |
|---|---|---|---|---|
| 542 | ic expands unrelated environment variables as model aliases | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/542#issuecomment-6941363507 | ic:41 still substitutes any non-empty variable; fix scheduled in 6.0.0 (#571 decision 6.7, option A); no PR |
| 543 | ic reports an internal shell error when the preset argument is missing | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/543#issuecomment-6941364063 | ic:74 unguarded $2 (also lines 75-77); scheduled in 6.0.0; no PR |
| 544 | ic help fails when its environment file contains a failing command | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/544#issuecomment-6941364769 | source at ic:28 precedes help at ic:80-82 under set -e; scheduled in 6.0.0; no PR |
| 545 | recommend help advertises a Python module command that cannot run | ACTIVE | https://github.com/IronbellyOrg/IronClaude/issues/545#issuecomment-6941365335 | commands.py:40-41 still names python -m; no __main__.py; scheduled in 6.0.0; no PR |
| 556 | reflect: preview prompt, credential exit and stub scorer differ from advertised contracts | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/556#issuecomment-6941365922 | umbrella of 563, 564, 565; backlog by Clay; no reflect code change since 2026-11-12 |
| 563 | reflect command preview shows a different prompt from scorer execution | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/563#issuecomment-6941366476 | runner.py:655-657 vs 540-544 unchanged; backlog |
| 564 | reflect missing credentials exit 1 despite a blocked result requiring exit 2 | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/564#issuecomment-6941367091 | commands.py:442-469 unchanged; answers the "may be stale" comment: not stale |
| 565 | reflect stub transport still dispatches a scorer child despite credit-free guidance | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/565#issuecomment-6941367597 | ensemble.py:424-430, 537-553 unchanged; backlog |
| 332 | /sc:load lists a Write step but has no .superclaude/.gitignore instruction | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/332#issuecomment-6941368212 | load.md still lacks the rule; #571 plans retiring /sc:load (removal PR 6) |
| 333 | sc-crash-recovery bootstrap_scan.sh exits non-zero and prints no JSON | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/333#issuecomment-6941368769 | reproduced on master copy: rc=1, 0 bytes when no session folder; cause is recent_sessions "|| return" (status 1) under pipefail |
| 387 | Hook block-bare-python.sh misses python3 in an unquoted shell heredoc and in a coproc body | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/387#issuecomment-6941369309 | ran master hook copy: both commands exit 0; no commit since #359 |

Duplicates: 563, 564 and 565 are three distinct defects split from the umbrella 556; none duplicates another. 556 can close once all three are closed or dropped.

## Close candidates

None. No issue in this cluster is done, superseded or duplicate today. 332 becomes a close candidate (superseded) only if #571 removal PR 6 retires /sc:load. 556 becomes one when 563 to 565 are resolved.

## Owner questions

None formally. Two open choices without a decision yet:
- 332: is /sc:load retired in 6.0.0 (#571 row 6)? If yes, close 332 as superseded.
- 387: fix the two parser gaps, or switch the hook to a simpler block rule (the issue's alternative)?
