# Hypothesis (Tier 2, system-architect): per-row process spawning plus a `local LC_ALL=C` that never reaches grep; ship a staged fix: a bash quick win that also becomes the fallback, then one python3 batch helper

(Persisted by the parent from the troubleshoot-analyst return, lens system-architect (fix design under constraints); condensed, no claim changed. I = /home/coder/.claude/skills/ccsession-tag/ccsession (2072 lines).)

**Tier**: 2   **Timestamp**: not supplied to the worker
**Cause class**: Performance/resource (N+1 process spawning; the `LC_ALL=C` intent not reaching grep)
**Claim class**: `runtime_behavior`; **Evidence class**: `runtime_trace` (parent-captured trace and probes; savings below are derived arithmetic, not executed); **Verdict direction**: AFFIRM
**Consistency with docs**: aligned for the output contract (constraints C1-C21 in wave1_5-branch-C.md); `no_docs_found` for any speed target; README:190 stays true (the helper only reads and returns data)
runs-in=coder workspace, one bash process

## Claim

The 27.07 s is about 14 process spawns per row (6,860 trace lines for 477 rows; the 457 `pwd` lines are builtins, so about 6,400 real forks) plus a `grep -oE` that runs in the UTF-8 locale. Fix in two stages: first the safe bash quick wins, which also become the fallback; then one python3 helper called once per list that does the transcript index and the head/tail working-directory scan. Bash keeps ownership of row text, grouping, glob order, session_place, colours and exit codes. The helper returns data, not formatted lines, so the pinned formats (C9, C10) are untouched by construction.

## Evidence

- Probe arms: Arm 1 1.442 s, Arm 2 6.460 s, Arm 3 13.227 s (tier1-observation.md).
- I:1383 `local store want cwd first="" LC_ALL=C` and I:1403 `local b LC_ALL=C`; the parent's probe `bash -c 'f() { local x LC_ALL=C; env | grep -c "^LC_ALL="; }; f'` printed 0.
- I:1594-1618 per-row spawn set: `head -n 1`, `dirname`, `ls -t | head`, session_home, session_place, two `stat` and two `date` per row.
- Precedents: I:520 `python3 - "$PROJECTS_DIR" <<'PY'` (inline python3 heredoc inside this script); I:1674-1675 (`[ -f "$CCSESSION_DIR/retention.py" ] || return 0`, then `python3 ... 2>/dev/null) || return 0`, guarded helper file); I:934 and I:1851 use `IFS=$'\x1f'` as a record separator.
- I:2054-2055 also call session_transcript and session_home on the resume path; those functions must stay as they are. I:132 is `set -e` (worker did not check for `set -u`).
- Behaviour-definition rows the parent should write: bash `local` does not export to children (observed by the parent); GNU `date -r` takes a file (observed by the parent); Python on Linux has no birth time (worker knowledge, unverified here); BSD `date -d` behaviour (unverified).

## Design comparison (worker arithmetic; captured numbers only, proxies marked)

Common basis: self times sum to 26.50 s plus 0.57 s unattributed = 27.07 s.

| | A: python3 helper + bash fallback (recommended) | B: bash only | C: lazy `--ask` list | D: other |
|---|---|---|---|---|
| Expected saving | A-core (helper does index and scan; bash keeps one `stat` and one `date -d` per timestamp): 0.75 + 0.87 + 1.05 + 1.95 = 4.62 s lower bound for the remaining wall time (about 5.9x). A-full (helper also does stat and dates): 0.75 + 1.95 = 2.70 s (about 10x) | about 14.6 s remaining (lower bound, additive, optimistic) | linear in rows shown: 27.07 x N/477 s (N=50: 2.84 s; N=20: 1.14 s); only if the contract changes | D1 head-first early exit at most 0.73 x 0.8 = 0.58 s inside the helper; D2-D4 rejected |
| Contract risk | low-medium: the helper must reproduce the unescape rule, byte-wise folder match, first-cwd fallback and newest-copy rule | low; only the locale fix changes behaviour for non-ASCII input | high: changes the row set, the "N more sessions in other worktrees" count and adds an "older sessions hidden" line; README:192, 206-212, D08 and pinned tests change | D3 parallel jobs need temp files (breaks README:190); D4 cache file breaks README:190 |
| Files touched | 3 (`ccsession`, new helper in src/superclaude/skills/ccsession-tag/, `tests/unit/test_ccsession_tag.py`); an inline heredoc (I:520 style) would make it 2 | 2 (`ccsession`, the test file) | 5 or more | n/a |
| Users without python3 | get stage 1 speed (about 14.6 s remaining); row text unchanged | no python3 dependency | n/a | n/a |

B itemised (additive): locale 6.460/13.227 = 0.488 so 12.16 s becomes 5.94 s, saving 6.22 s; failing `date -r` 1.1 s; one `stat` per row 0.87 s; builtins for dirname/basename/`head -n 1` (1872 + 477 forks x 1.2 ms proxy from the `date -d` loop, not a measurement of these commands) 2.82 s; index built once on the first miss with one grep per row 2.03 - 477 x 1.2 ms = 1.46 s; total 12.47 s saved, so 27.07 - 12.47 = 14.6 s remaining. B alone cannot reach single digits: the Arm 2 scan (5.94 s) stays unless the byte volume drops; reading the head first and the tail only when no store-matching folder is found is order-preserving (the stream is head, newline, tail, and the first match in stream order is in the head if the head has one).

## Proposed Fix, staged

Stage 1 (ccsession only, about 14.6 s remaining; becomes the fallback of stage 2): prefix `LC_ALL=C` on the grep and awk in session_home and session_branch (keep the `local LC_ALL=C` for bash's own byte-wise matching); probe the `date` flavour once with `date --version` and use `date -d` only on GNU (keep the BSD-first order on non-GNU so C6 holds); one `stat -c '%W %Y'` per row, GNU first (C5), keeping get_btime and get_mtime intact; replace basename/dirname/`head -n 1` with `${x##*/}`, `${x%/*}` and `IFS= read -r uuid < file || true` (the `|| true` because of `set -e`); build one `ls -t "$PROJECTS_DIR"/*/*.jsonl` index in memory on the first miss and pick the first line ending in `/<uuid>.jsonl` (newest copy per C4; no file written); keep every construct bash 3.2 safe (no associative arrays, `mapfile` or `printf '%(...)T'`).

Stage 2 (the helper): bash first collects topic files and uuids into indexed arrays in the same glob order; calls `python3 "$CCSESSION_DIR/<helper>.py" "$PROJECTS_DIR" "$ws_dir" uuid...` once, inside the `first` block so the lazy heading (C8) holds; the helper prints one `\x1f`-separated record per input uuid, in input order (path, then `was`; the own-folder copy preferred when it is a regular file, else the newest copy); the scan works on bytes: head 256 KiB then tail 1 MiB, each line matched separately with `"cwd":"(?:[^"\\]|\\.)*"`, the two replacements in the order of I:1388-1389 (`\"` to `"`, then `\\` to `\`), not `json.loads`; folder match is `re.sub(rb'[^A-Za-z0-9]', b'-', ...)` per byte against the folder name; the first-cwd fallback and dedup follow I:1390-1398; read the head first and skip the tail when a store-matching folder is found; bash captures the output in `if out=$(...); then` and a missing helper or any failure runs stage 1 unchanged; nothing is written and stderr is discarded; birth time stays in `stat -c '%W'`; mtime, if ever moved, must use `st_mtime_ns // 10**9`, not `int(st_mtime)`.

Stage 3 (optional): move `stat` and the date strings into the helper only if the stage 2 trace still shows more than about 2 s there; that puts C6 formatting in python and needs its own parity test.

Tests: all `_listed` tests and those at 4474, 4522, 4551, 4585, 3465 must pass unchanged (worker only grepped them). New: parity A/B/C (fixture store, helper present vs python3 hidden from PATH, all three views, byte-identical stdout, stderr and exit code; cases: transcript missing; transcript only elsewhere; two copies (newest wins); store folder only in the tail; first cwd not matching; escaped `"` and `\` in a cwd; a non-ASCII cwd; a file under 256 KiB (overlap) and over 1.25 MiB (gap); a deleted folder; `%W` printing 0 giving "(times unavailable)"); a spawn-count shim test N=10 vs N=60 for date, head, stat, ls, dirname, basename; a locale shim asserting `LC_ALL=C` in grep's environment; a test that no file appears under HOME or TMPDIR (README:190); a static test rejecting bash 4 constructs in the changed region (no 3.2 binary runs in tests, C11).

## Confidence

Self-reported: 0.72. Evidence grounding 1.0; runtime check 0.5 (savings derived, no patch executed); symptom coverage 0.5 (not the 5-10% CPU); reproducibility fit 1.0; fix directness 0.5 (helper unwritten, cold-cache cost unknown); domain coherence 1.0.

## Risks

Helper drift (unescape order, bytes against characters, first-cwd fallback, ties in `ls -t` ordering, symlinked or directory-named `*.jsonl`, a file deleted between index and `stat`); locale fix restores the intended byte-wise behaviour (a UTF-8 grep may treat a transcript with invalid UTF-8 as binary: worker knowledge of GNU grep, unverified); timing window: `--ask` budget is 60 - 30 = 30 s, the list at 27.07 s leaves 2.93 s so a store about 11% larger already makes an unanswered question outlast Orca's 60 s window (C12), which is the argument for shipping stage 1 first; python startup where `python3` is the macOS stub (unverified).

## If I'm wrong, it's probably because

The 12.16 s in session_home is mostly cold-cache disk reads of the 554 MB, which a helper also pays; then stage 2 is smaller than the prototype's 0.75 s suggests and only the head-first early exit helps.

## Falsification standard (worker)

If `ccsession --here` with the stage 2 helper still takes 13.5 s or more (27.07 / 2) on the same store, with load recorded, the spawn-and-scan mechanism is not dominant and A is false. If stage 1 alone cuts `--here` by less than 1 s, the locale and fork mechanism is false.

# Discriminator: LC_ALL reaching grep in session_home
Hypothesis A: `LC_ALL=C` in a `local` declaration is not exported, so grep in session_home runs in LANG=C.UTF-8. Hypothesis B: `LC_ALL=C` reaches grep and Arm 3 vs Arm 2 is cache or load noise.
Observable: `child-lacks-LC_ALL` (boolean), from `env | grep -c "^LC_ALL="` printing 0.
Probe: `bash -c 'f() { local x LC_ALL=C; env | grep -c "^LC_ALL="; }; f'` (count 0 = true, 1 = false; an empty capture or error is unobserved).
Primitive under dispute: I:1383 `local store want cwd first="" LC_ALL=C`; the bash manual text on `local` and export was not fetched; the only support is the parent's captured probe.
Reference-context value: false (`LC_ALL=C env | grep -c "^LC_ALL="` should print 1; the parent has not captured the reference arm).
Outcomes: true -> A consistent, B refuted; false -> A refuted, B consistent (it does not by itself explain Arm 3 vs Arm 2).
Falsifier: "If child-lacks-LC_ALL=false on the next run, A is false." The parent captured count 0 (true) once; the reference arm is unobserved.

## Alternatives considered

B alone (about 14.6 s remaining lower bound; kept as stage 1 and as the fallback); C lazy list (rejected as a contract change); a hook that records the start folder at session start (promising but needs a hook and store-format change and a migration for the 477 existing sessions: follow-up only; hooks not read).

## Grounding gaps (worker)

Not read: bodies of the tests in tests/unit/test_ccsession_tag.py (grep only), README (README:190 taken from wave1_5-branch-C.md), the `plugins/superclaude/` mirror, `ensure_names_migrated` before line 505 (it runs a python3 scan over all transcripts at I:520 and may add cost on a first `--ask`: unverified). Unverified: cold-cache cost; python startup and the macOS python3 stub; BSD `date -d` behaviour; Python birth-time support on Linux; the 1.2 ms per-fork proxy for dirname/basename/head; the share of sessions whose head holds a store-matching folder; bash 3.2 runs (none exist). Diagnosability verdict partial. Codegraph does not index shell.

## How to measure success (worker; parent to run)

Re-run the same `bash -x` Task 1 trace on the same store (record `uptime` first; load was 11.9); `time ccsession --here` and `time ccsession --list` three times each, compared to 27.069 s and 14.473 s; targets are derived lower bounds, not promises (stage 1 about 14.6 s for `--here`; stage 2 A-core 4.6 s; A-full 2.7 s; no `--list` bound is derivable); spawns per row must fall from about 13 (6,400 / 477) to a constant that does not grow with N.
