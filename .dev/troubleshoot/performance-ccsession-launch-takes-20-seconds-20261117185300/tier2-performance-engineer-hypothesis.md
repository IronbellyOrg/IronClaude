# Hypothesis (Tier 2, performance-engineer): two measured levers in one file, the grep locale (about 6.2 to 6.8 s) and about 6,000 per-row spawns that could be builtins (about 7.5 to 8.7 s); a python3 helper saves about the same and costs more

(Persisted by the parent from the troubleshoot-analyst return, lens performance-engineer; condensed, no claim changed. I = /home/coder/.claude/skills/ccsession-tag/ccsession; all numbers are parent captures in tier1-observation.md.)

**Tier**: 2   **Timestamp**: time of day not observed (parent probe stamps 19:02Z and 19:03Z)
**Cause class**: Performance/resource (N+1 process spawning plus locale-dependent regex cost)
**Claim class**: `mixed`; **Evidence class**: `runtime_trace`; **Verdict direction**: AFFIRM (agrees with Tier 1 on cause, disagrees on the best fix)
**Consistency with docs**: aligned (no speed target documented; fix keeps pinned formats, exit codes and README:190)
runs-in=coder workspace, one bash process

## Claim

The 27.07 s is a sum of per-row costs; no single micro-fix removes more than half. Lever (a): `local LC_ALL=C` (I:1383) is never exported, so `grep -oE` and `awk` in session_home run in LANG=C.UTF-8 and pay the Arm 3 vs Arm 2 penalty (13.227 - 6.460 = 6.767 s). Lever (b): about 6,000 per-row spawns (`date`, `dirname`, `basename`, `head`, `stat`, `ls`) can be builtins or hoisted. Combined estimate: 27.07 s to roughly 11.6-14.1 s. A python3 helper reaches 13.63 s and needs more than 3 files.

## Cost model (derived only from captured numbers)

Self times sum to 26.50 s of the 27.08 s trace wall (0.58 s unattributed). Unit costs: `date` 2.68 s / 1756 = 1.53 ms; `head` in session_transcript 1.12 s / 477 = 2.35 ms; `ls` 0.92 s / 477 = 1.93 ms; `stat` (0.88 + 0.86) s / 878 = 1.98 ms; per row 27.07 s / 477 = 56.7 ms.

| # | Lever | Derivation | Saving | Cost |
|---|---|---|---|---|
| a | real C locale for grep and awk in session_home (I:1396-1397; same fix at I:1405) | Arm 3 - Arm 2 = 6.767 s; scaled to the traced 12.16 s: 12.16 x 6.767/13.227 = 6.22 s | 6.2-6.8 s (23-25%) | 2-3 edited tokens |
| b1 | stop trying `date -r` first on GNU | 878 failing attempts x (2.555 - 1.205 ms) = 1.19 s | 1.1-1.2 s | about 6 lines |
| b1+ | `printf -v ... '%(%Y-%m-%d %H:%M)T'` when BASH_VERSINFO >= 4.2, else current path | removes all 1756 `date` spawns = format_epoch self time | up to 2.68 s | about 8 lines; bash 3.2 untouched |
| b2 | one `stat -c '%W %Y'` per file | 439 x 1.98 ms = 0.87 s up to get_mtime self time 1.20 s | 0.87-1.20 s | about 20 lines |
| b3 | dirname/basename/`head -n 1` become parameter expansion and `read`; hoist `dirname "$ws_dir"` | 1832 per-row spawns x 1.53 ms = 2.80 s (assumes these cost as much as `date`: unverified) | about 2.8 s | about 10 lines |
| b4 | builtin glob plus `-nt` instead of `ls -t \| head -n 1` | at least the `head` spawn 1.12 s; at most the whole self time 2.03 s | 1.12-2.03 s | about 8 lines; tie-break vs `ls -t` unverified |
| b | b1+ to b4 together | low 2.68 + 0.87 + 2.80 + 1.12 = 7.47 s; high 2.68 + 1.20 + 2.80 + 2.03 = 8.71 s | 7.5-8.7 s | about 45 lines, 1 file |
| a+b | both | low 13.69 s, high 15.48 s, minus overlap at most 0.69 s | 13.0-15.5 s, remaining 11.6-14.1 s | 1 file |
| c | python3 helper for index plus head/tail scan | 12.16 + 2.03 - 0.75 = 13.44 s saved; remaining 13.63 s | 13.44 s (49.6%) | new helper, manifest, README, tests, a second code path: more than 3 files |
| d | bound the list to the N newest rows | N=100 gives 100 x 56.7 ms = 5.7 s (saving up to about 21 s, floor 3.23 s to rank by recency) | up to about 21 s | changes row membership, order, counts and the 405-line output: a contract change |
| e | memoize on disk | 0 s allowed: README:190 forbids writing during listing; a cache would go stale (README:275) | 0 s | not allowed |

Worker extra: rows classified `other` (I:1636) are built and then discarded after get_btime, get_mtime and format_epoch ran (I:1610-1627); computing the place first would save about (2.68 + 2.42 + 0.14) x other/439 s; with other around 76 (assumption, not derived exactly) about 0.9 s.

## Evidence

Tier 1 observation timings (`--here` 27.069 s; Arm 1 1.442 s, Arm 2 6.460 s, Arm 3 13.227 s; traced session_home 12.16 s is close to Arm 3, far from Arm 2); I:1383 `local store want cwd first="" LC_ALL=C` and I:1396-1397 (no `LC_ALL=` prefix on grep or awk); I:1594-1627 (the loop spawns head, dirname, ls/head and two stat and calls format_epoch twice per row including rows later discarded as `other`); behaviour-definition: the parent's `bash -c 'f() { local x LC_ALL=C; env | grep -c "^LC_ALL="; }; f'` printed 0.

## Proposed Fix (one change-set, one source file)

Edit `ccsession` only: (1) prefix `LC_ALL=C` on the grep and awk in session_home and on the grep in session_branch, in the same command-prefix form as I:686, 689, 694; (2) replace per-row spawns with parameter expansion, `read -r`, a once-per-list `date` probe or the guarded `printf '%(...)T'`, one `stat` per file, and a builtin glob plus `-nt` in session_transcript; (3) no python3 helper. Files: `ccsession` and `tests/unit/test_ccsession_tag.py` (2 files; test file not read). Why (a)+(b) over (c): about the same saving (13.0-15.5 s vs 13.44 s), no python3 dependency, no second implementation of the cwd-matching rule and JSON unescaping (I:1386-1389), keeps the 256 KiB + 1 MiB head/tail read and GNU-first stat (I:1490, I:1516), stays within bash 3.2 (guards on BASH_VERSINFO; no associative arrays).
Tests (proposed, not run): a shim `grep` on PATH that records `$LC_ALL` and must see `C`; a spawn-count test with counting shims for date, dirname, basename, head, stat and ls at N=10 vs N=60 requiring no growth; existing pinned-format tests stay byte-identical.
Quick win (smallest subset): (a) plus b1 = 7.3-8.0 s saved, 19.1-19.8 s remaining (about the reported 20 s, so it does not fix the symptom alone); adding b3's 2.8 s gives about 16.3-17.0 s.

## Confidence

Self-reported: 0.62 for the cost model and ranking; 0.55 that (a) alone delivers 6.2-6.8 s in the real run; 0.75 that (a)+(b) lands in 11.6-14.1 s. Evidence grounding 1.0; runtime check 0.5 (no run of the proposed change; locale gain measured only on a stand-alone loop); symptom coverage 0.5 (not the 5-10% CPU); reproducibility fit 1.0; fix directness 0.5 (b savings borrow `date`'s per-spawn cost for dirname, basename and head; the glob replacement of `ls` is unmeasured); domain coherence 1.0.
Unresolved inconsistency (worker): whole-run user time is 5.823 s but Arm 3's user time alone is 9.992 s (Arm 2 3.475 s); user-time comparisons suggest the real grep may already be near C speed while wall times point the other way; a possible reason is that `time` does not count grep/awk children of the `< <(...)` process substitution reaped after `return 0` at I:1394 (unverified bash-internals point). Only the discriminator separates these.

## Risks

The locale change alters output only for working folders with invalid UTF-8 bytes (UTF-8 grep drops those names, C grep keeps them; pin in a test); b3 changes dirname/basename semantics only for a path with no slash (transcript paths always contain one); b1+ must keep the `%Y-%m-%d %H:%M` text and local timezone identical to `date` (DST edges unverified); the `-nt` glob may break ties differently from `ls -t` (unverified).

## If I'm wrong, it's probably because

The grep in the real run is already effectively byte-wise (the user-time evidence), so the 12.16 s in session_home is spawn and I/O under load average 11.9, and (a) saves little; the combined estimate then falls to the (b) range alone (7.5-8.7 s).

## Falsification standard (worker)

# Discriminator: locale-gain
Hypothesis A: grep and awk in session_home really run in LANG=C.UTF-8 and that costs about 6.77 s of the 12.16 s. Hypothesis B: the stage's locale is not the cost; session_home time is spawn, I/O and load bound.
Observable: locale-gain = (wall of `ccsession --here`) - (wall of `LC_ALL=C ccsession --here`) >= 3.38 s (half of 6.767 s).
Probe (read-only, parent to run, order alternated): plain, C, C, plain; true only if both ordered pairs give a gain >= 3.38 s; a missing or failed run is unobserved, never false.
Reference-context value: n/a; the stand-alone analogue (Arm 3 - Arm 2 = 6.767 s >= 3.38) reads true.
Outcomes: true -> A consistent, B refuted; false -> A refuted (predicted 6.77 s gain, observed below 3.38 s in both orderings), B consistent.
Falsifier: "If locale-gain is below 3.38 s in both orderings on the next run, A is false and lever (a) must be dropped from the plan; if it is at or above 3.38 s, B is false."

## Alternatives considered

python3 helper as the one fix (saves 13.44 s, needs more than 3 files and a second code path: rejected on cost/benefit, not speed); bounding to N rows (changes the output contract: rejected); disk cache (forbidden by README:190).

## Grounding gaps (worker)

Not read: file_to_name, name_key, show_saved, retention.py, README:190 and README:275, the test file, the installer manifest, macOS behaviour. Unverified: the `local`-not-exported finding rests on the parent's `bash -c` run (the worker did not grep for `export LC_ALL`); the split of Arm 2's 5.02 s between grep and awk; whether dirname/basename/head cost the same as `date` (1.53 ms); the count of `other` rows; cold-cache cost of the 554 MB scan; the "pwd" entry in the Tier 1 process-count table is a trace-line count and `pwd` is a builtin, so "about 6,900 external processes" was overstated (the parent corrected it to at least 6,403 external processes). The CPU share (5-10% reported vs about 2.5% of this 28-core machine) is not explained here.
