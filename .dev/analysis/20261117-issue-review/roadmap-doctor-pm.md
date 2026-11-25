# Cluster roadmap-doctor-pm (reviewed 2026-11-17)

| Issue | Title | Verdict | Comment | Evidence |
|---|---|---|---|---|
| 505 | business-panel lacks description field | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/505#issuecomment-6941342323 | master business-panel.md lines 1-7 still `purpose:` only; owner decided to fix, not planned yet |
| 506 | improve and cleanup usage conflicts with examples | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/506#issuecomment-6941342583 | usage lines in improve.md and cleanup.md 19-24 unchanged; owner decided to add options |
| 510 | doctor accepts missing codegraph registration | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/510#issuecomment-6941342876 | doctor.py keeps warning-only (matches decision); main.py 496-499 still hides detail without --verbose |
| 521 | roadmap run --dry-run creates empty dir | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/521#issuecomment-6941343148 | executor.py:3670 mkdir before dry-run check at 3735; owner backlog (headless Claude) |
| 524 | halt retry suggestion omits output dir | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/524#issuecomment-6941343450 | executor.py:2865-2866 still lacks --output; owner backlog |
| 533 | roadmap validate says Complete after failed review | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/533#issuecomment-6941343821 | commands.py:495-512 always prints Complete; owner backlog |
| 536 | PM promises automatic memory restoration | STALE-VALID | https://github.com/IronbellyOrg/IronClaude/issues/536#issuecomment-6941344133 | pm.md:12, pm-agent.md, sc-pm-protocol SKILL.md still promise it; owner decided text-only fix |
| 537 | validation tracebacks for missing inputs | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/537#issuecomment-6941344488 | no FileNotFoundError handler in either commands.py; owner backlog |
| 538 | tasklist validation selects unrelated Markdown | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/538#issuecomment-6941344846 | tasklist/executor.py:47 unfiltered glob; owner backlog |
| 540 | swarm foreground run writes no done.json | BLOCKED | https://github.com/IronbellyOrg/IronClaude/issues/540#issuecomment-6941345165 | emit_done_sentinel only called from reflect/ensemble.py:421; owner swarm hold |

## Close candidates

None. Note: 536 becomes closable once the owner-decided wording fix merges (owner ruled out further PM work); 510 likewise after its small follow-up.

## Owner questions

None. All ten already carry an owner decision comment of 2026-11-16. The only open item is when the headless-Claude hold (521, 524, 533, 537, 538) and the swarm hold (540) are lifted.

Method note: all code was read from origin/master with read-only git. No merged PR in the last 7 days touched any file named in these ten issues. Tests were not run; the reproductions in the issue bodies were not re-run (UNVERIFIED beyond source reading).
