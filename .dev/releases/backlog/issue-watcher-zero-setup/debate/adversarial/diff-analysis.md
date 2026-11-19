# Diff Analysis: single multi-project watcher (V1) vs one watcher per project (V2)

## Metadata
- Generated: 2026-11-18
- Variants compared: 2 (variant-1-original.md = single watcher; variant-2-original.md = per-project)
- Categories: structural (2), content (6), contradictions (3), unique (4), shared assumptions (3)
- Focus: correctness, risk, operability

## Structural Differences
| # | Area | V1 | V2 | Severity |
|---|---|---|---|---|
| S-001 | Section layout | 6 sections, same headings as V2 | 6 sections, same headings | Low |
| S-002 | Depth of evidence | Cites cycle.py/record.py/cli.py lines; 3 of its claims marked UNVERIFIED | Cites more lines (9 arguments); 3 claims marked UNVERIFIED | Low |

## Content Differences
| # | Topic | V1 approach | V2 approach | Severity |
|---|---|---|---|---|
| C-001 | Where the loop lives | A loop INSIDE the watcher (`once --all`): one process lists repos and runs the existing one-project cycle per repo | A loop OUTSIDE the cycle (`run-all` verb) that starts the existing `once` per config file, serially | Low (both are a serial loop over per-repo config) |
| C-002 | State, lock, kill switch | Per-repo `state_dir` kept; "nothing shared" | Per-repo `state_dir` kept; isolation "comes free" | Low (agree) |
| C-003 | Rate limit | Wants one account-level stop shared across repos (new behaviour to design) | Per-instance pause via `next_permitted_at`; serial run plus clamp bounds cost | High (differs on whether a shared account-level stop is required) |
| C-004 | Time budget | Fresh `Deadline` per repo, wall time grows with repos | 240 s per cycle, five repos could be 20 minutes worst case; needs a loop-level cap | Medium |
| C-005 | Approvers | One builder, shared ids plus per-repo maintainers | Per-repo files so one repo's maintainer cannot approve in another | Low (both end with per-repo file content) |
| C-006 | Operability view | One `status` line per repo plus overall health | Five `status` lines, one per repo | Low |

## Contradictions
| # | Point of Conflict | V1 | V2 | Impact |
|---|---|---|---|---|
| X-001 | Does the cycle code need to change? | "`load_config` and `Cycle.run` unchanged" (V1 s3) | "No change to cycle.py logic, record.py or github.py" (V2 s4) | High: both say reuse unchanged. Verified FALSE for both: the watcher is hard-wired to one repo. `github.py:37` `REPO = "IronbellyOrg/IronClaude"` is used at `github.py:187` (issue discovery `--repo`), `:208` and `:259` (comments, issue reads), and `launch.py:50` `ORIGIN_REPO = "ironbellyorg/ironclaude"` is checked at `launch.py:249`. Any design for a second repo must thread the repo through config. |
| X-002 | Is the loop a "rewrite" | "thin loop on top, not a rewrite" | "needs a new schema version and a migration" for a multi-project config | Medium: only true if a single multi-project CONFIG FILE is chosen; V1 itself keeps one config per repo, so V2's schema objection does not apply to V1's own design |
| X-003 | Does one process see account limits whole | V1: a single loop can stop the sweep on the first rate limit | V2: instances back off separately but run serially so spend equals one watcher | Medium: V1 says "nothing shares the wait across state_dirs today (UNVERIFIED)"; both sides agree it is not shared today |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | R8 already forces a single sweeper, so a per-project design needs an outer process too | High |
| U-002 | V1 | One account-level rate stop across repos | Medium |
| U-003 | V2 | Wrong-target safety: `_origin_ok` binds one worktree to one project (`cycle.py:670-678`) | Medium |
| U-004 | V2 | Board overlap: two repos on one Project board could both see one item; mitigate with a repo filter | Medium |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The watcher can be pointed at another repo by config alone | Both say reuse `Cycle.run` unchanged | High | CONTRADICTED by `github.py:37`, `launch.py:50` (see X-001) |
| A-002 | Every watched repo has a GitHub Project and its issues sit on it | Both rely on R3 per-repo project lookup | Medium | UNSTATED (a repo with no Project gets no config, requirement R3) |
| A-003 | A serial loop over five repos finishes inside the 5-minute schedule | Both assume a loop-level cap or serial run | High | UNSTATED (V2 computes 20 minutes worst case; V1 says "acceptable at five") |

## Summary
- Structural: 2. Content: 6. Contradictions: 3. Unique: 4. Shared assumptions: 3 (UNSTATED: 2, STATED: 0, CONTRADICTED: 1).
- Highest-severity items: C-003, X-001, A-001, A-003.
- Both variants converge on one design shape: one scheduled entry, a serial loop, per-repo config and per-repo state directory. The real difference is where the loop sits (inside the watcher or a wrapper around `once`) and whether account-level rate limiting is shared.
