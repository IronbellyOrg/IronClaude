# Diff Analysis: fix-proposal Comparison (ccsession session list speed)

## Metadata
- Generated: 2026-11-17T19:12:50Z
- Variants compared: 3 (variant-1 = python3 batch helper + fixed bash fallback; variant-2 = bash-only locale and builtin fixes; variant-3 = staged: bash quick win first, then the helper)
- Mode: A (compare existing files); depth quick; focus: correctness, risk, test-coverage
- Total differences found: 25 (structural 2, content 11, contradictions 2, unique 5, shared assumptions 6 of which 4 promoted)
- Convergence denominator (S + C + X + promoted A): 2 + 11 + 2 + 4 = 19
- Categories: structural (2), content (11), contradictions (2), unique (5), shared assumptions (6)
- Common ground of all three (not a difference): same problem statement and measurements; all fix the unexported `LC_ALL=C` (prefix `LC_ALL=C` on grep and awk in session_home and session_branch); all keep the output text, exit codes, glob row order, here/gone/other classification and "Listing never writes any file"; all embed the same "Documented constraints to honor" block; all require a spawn-count shim test, a locale shim test and unchanged pinned-format tests.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity | Taxonomy |
|---|---|---|---|---|---|---|
| S-001 | Delivery shape of the change | one change-set: helper plus fixed fallback, shipped together | one change-set in one file, no helper | two or three stages: stage 1 bash quick win (also the fallback), stage 2 helper, stage 3 optional | Medium | L2 |
| S-002 | Where the shape-defining facts sit | proposal text only | proposal text only | adds the 60 s Orca timing-window argument to Evidence to justify the stage order | Low | L1 |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Variant 3 approach | Severity | Taxonomy |
|---|---|---|---|---|---|---|
| C-001 | Per-session cwd scan (12.16 s of 27.07 s) | python3 helper does the head 256 KiB + tail 1 MiB scan once per run | keep the bash `head \| tail \| grep \| awk` pipeline, only fix the locale (Arm 2: about 6.5 s remains for the scan) | stage 1 as variant 2, stage 2 moves the scan into the helper | High | L2 (architecture) |
| C-002 | Timestamps (878 `date -r` failures first) | fallback: `date -d "@$e"` first on GNU; main path keeps one `stat` per row | `printf -v ... '%(%Y-%m-%d %H:%M)T'` when `BASH_VERSINFO` >= 4.2 else current path; or stop trying `date -r` first | probe `date --version` once, `date -d` on GNU only; explicitly no `printf '%(...)T'` | Medium | L2 |
| C-003 | Transcript lookup (`ls -t */<uuid>.jsonl` x 477) | helper's one directory scan, newest wins | builtin glob plus `-nt` (tie-break versus `ls -t` unverified) | one `ls -t "$PROJECTS_DIR"/*/*.jsonl` index in memory on the first miss, first line ending in `/<uuid>.jsonl` (newest copy rule kept exactly); the invariant that the newest copy wins must hold | Medium | L3 |
| C-004 | Guard when python3 or the helper is missing or fails | fall back to the existing per-row code (fixed for locale and date order) | not applicable (no helper) | stage 1 is the fallback; bash captures helper output inside `if out=$(...); then` and any failure runs stage 1 unchanged | Medium | L3 |
| C-005 | Locale fix scope and guard on output | prefix on grep/awk in session_home and session_branch | same, and notes an output nuance for working folders with invalid UTF-8 bytes (UTF-8 grep drops them, C grep keeps them) | same; keep `local LC_ALL=C` for bash's own matching | Low | L3 (state of an environment variable) |
| C-006 | `stat` | one `stat -c '%W %Y'` per row | one `stat -c '%W %Y'` per file (alternative: one stat over all files) | one per row; optional stage 3 moves stat and date strings into the helper | Low | L2 |
| C-007 | `dirname`, `basename`, `head -n 1` per row | not changed | parameter expansion and `read -r`, hoist `dirname "$ws_dir"` | `${x##*/}`, `${x%/*}`, `IFS= read -r uuid < file \|\| true` (`\|\| true` because of `set -e`) | Medium | L2 |
| C-008 | Tests | parity (helper vs python3 hidden), spawn count N=10 vs 60, locale shim, no file written | locale shim, spawn count, static bash-4 construct check | parity A/B/C with 11 fixtures, spawn count, locale shim, no file under HOME or TMPDIR, static bash-4 check | Low | L2 |
| C-009 | Helper name and place | `scan_sessions.py` beside `retention.py` | no helper | `<helper>.py` unnamed; inline heredoc (I:520 style) was named as an alternative by a worker, not in this file | Low | L1 (naming) |
| C-010 | Expected remaining wall time of the 27.07 s | about 13.6 s (derived) | 11.6-14.1 s (derived; unmeasured per-spawn proxies) | stage 1 about 14.6 s; stage 2 A-core 4.62 s, A-full 2.70 s (derived, not executed) | Medium | L2 |
| C-011 | Files touched | 3, possibly 4 (script, helper, tests, README) | 2 (script, tests) | stage 1: 2; stage 2: 3 to 4 | Medium | L2 |

## Contradictions

| # | Point of Conflict | Variant A position | Variant B position | Impact |
|---|---|---|---|---|
| X-001 | `printf '%(...)T'` on bash 3.2 (macOS floor) | Variant 2: allowed when guarded by `BASH_VERSINFO` >= 4.2, "bash 3.2 untouched" | Variant 3: "no ... `printf '%(...)T'`" in any construct kept bash 3.2 safe | Medium |
| X-002 | Remaining time after the same quick-win changes | Variant 2 (a+b together): 11.6-14.1 s remaining | Variant 3 (stage 1, same changes minus `printf` and `-nt`): about 14.6 s remaining | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 3 | argues stage order from the Orca window: the list at 27.07 s leaves 2.93 s of the 30 s margin (60 - 30 s question), so a store about 11% larger already breaks the guarantee; ship the quick win first | High |
| U-002 | 3 | head-first early exit in the helper: skip the tail when a store-matching folder is found in the head | Medium |
| U-003 | 2 | skip time and duration work for rows later discarded as `other` (about 0.9 s on assumptions) and `printf '%(...)T'` for dates | Medium |
| U-004 | 1 | helper receives uuids in bash's glob order so row order is preserved; names the one-record-per-line pairing risk with odd file names | Medium |
| U-005 | 3 | `\|\| true` for `set -e`, static test rejecting bash 4 constructs, a no-file-written test, 11 named parity fixtures | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | The reporter's environment has the same non-C UTF-8 locale and a comparable store size, so the locale defect and the 20 s figure transfer from this machine (22.5-27.1 s here) | all three fix the locale first | UNSTATED | yes |
| A-002 | Cache state is not a boundary condition for the savings: all measurements and the 0.75 s prototype ran warm; cold reads of 554 MB (3,848 MB of transcripts in total) are assumed not to dominate | all three claim large savings | UNSTATED | yes |
| A-003 | python3 exists where the helper runs, with the bash fallback as the guard where it does not (macOS stub unverified) | variants 1 and 3 | STATED (variant 3 risks; variant 1 fallback) | no |
| A-004 | Per-spawn cost of `dirname`, `basename` and `head` equals `date`'s 1.53 ms (a proxy) so the builtin replacements save about 2.8 s | variants 2 and 3 | UNSTATED | yes |
| A-005 | Pinned output (row text, glob order, exit codes, stdout/stderr split, here/gone/other) must stay byte-identical | all three | STATED | no |
| A-006 | session_place (1.95 s), the `$(...)` forks and the held-back output (nothing printed until the list is built, I:1718) are acceptable to leave as they are; no variant touches them | all three | UNSTATED | yes |

## Summary
- Total structural differences: 2
- Total content differences: 11
- Total contradictions: 2
- Total unique contributions: 5
- Total shared assumptions surfaced: 6 (UNSTATED: 4, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001 (High), U-001 (High)
- Taxonomy coverage in the denominator: L1 (S-002, C-009), L2 (S-001, C-001, C-002, C-006, C-007, C-008, C-010, C-011), L3 (C-003, C-004, C-005, X-001, A-001, A-002, A-004, A-006)
- Similarity check: variants share the problem statement and constraints but differ materially in mechanism (helper vs builtins vs staged): not substantially identical; debate proceeds.
