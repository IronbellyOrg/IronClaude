# Hypothesis: the `--ask`/`--here` list is slow because list_sessions does about 14 external-process pipelines per topic file, and the session_home head/tail/grep/awk pipeline alone is 45% of the 27 s

(Persisted by the parent from the troubleshoot-analyst return, lens root-cause-analyst; trimmed for length, no claim changed. I = /home/coder/.claude/skills/ccsession-tag/ccsession; section names refer to tier1-observation.md.)

**Agent**: root-cause-analyst (analytical lens, run by troubleshoot-analyst)
**Tier**: 1
**Cause class**: Performance/resource (N+1 process spawning and per-session file scanning)
**Claim class**: `runtime_behavior`
**Evidence class**: `runtime_trace`
**Verdict direction**: AFFIRM
**Consistency with docs**: no_docs_found (no document sets a speed or CPU target; the output contract is aligned: the fix keeps pinned formats, exit codes and "Listing never writes any file")
runs-in=coder workspace, one bash process

## Claim

list_sessions (I:1554-1663) is a per-topic-file loop that spawns a fresh pipeline per session, 477 times, with no batching. The 477 sessions in this repo's list have transcripts in other folders. The cost is per-session scanning and process creation, not any single slow call. session_home reads the first 256 KiB and last 1 MiB of each transcript through `head`, `tail`, `grep -oE` and `awk` (I:1396-1397): 12.16 s of the 27.07 s wall (44.9%). The remainder is spread over about 14 small processes per row. A single process doing the same index and scan took 0.75 s in the prototype.

## Evidence

- E1, wall time (Wall-clock): `ccsession --here` 27.069 s real, user 5.823 s, sys 13.566 s; CPU 19.4 s, about 0.7 of one core of 28; sys is 70% of CPU. `--list` 14.473 s.
- E2, per-function self time (bash -x trace; shares of the 27.07 s wall): session_home (I:1377-1399, 439 calls) 12.16 s, 44.9%; list_sessions loop body (I:1554-1663) 5.12 s, 18.9%; format_epoch (I:1533-1537, 878 `date`) 2.68 s, 9.9%; get_btime + get_mtime (I:1488-1531) 1.22 + 1.20 = 2.42 s, 8.9%; session_transcript (I:1480-1483) 2.03 s, 7.5%; session_place (I:1430-1478) 1.95 s, 7.2%; format_duration 0.14 s, 0.5%. The `awk` that ends session_home's pipeline carries 9.89 s because a pipeline's cost is booked to its last process.
- E3, process counts (trace): 1756 `date`, 972 `head`, 936 `dirname`, 936 `basename`, 878 `stat`, 477 `ls`, 457 `pwd`, 448 `grep`; about 6,900 external processes for 477 rows, roughly 14 per row.
- E4, prototype (throwaway /tmp/ccs-proto/proto.py): one Python process, same uuid-to-newest-transcript index (1741 transcripts) and same head 256 KiB + tail 1 MiB scan of 439 sessions: 0.75 s total (0.78 s second run), 554 MB read, no per-session process; it omits session_place's git calls.
- E5, failing `date -r` (Primitive behaviour): on GNU `date`, `-r` takes a file, so `date -r <epoch>` fails (exit 1) and `date -d @` then succeeds; 2.6 ms per iteration with the failing attempt vs 1.2 ms without; about 2.2 s vs 1.1 s over 878 timestamps.
- E6, source of the per-session pipeline: I:1594 `uuid=$(head -n 1 "$topic_file")`; I:1595 and I:1598-1600 miss the repo-keyed folder and call session_transcript; I:1482 `ls -t "$PROJECTS_DIR"/*/"$1".jsonl | head -n 1`, a glob across 437 folders (about 208,000 path checks; 0.005 s per call, about 2.4 s for 477, against 2.03 s traced); I:1607-1608 call session_home and session_place per row; I:1610-1611 two `stat` per row; I:1616-1617 two `date` per row; I:1384 spawns `basename` and `dirname` inside session_home.

## What is structural, and what each part explains (shares of the 27.07 s wall; self times overlap and 0.57 s of the trace is unattributed)

| Component | Cost (captured) | Share |
|---|---|---|
| Per-session transcript scan pipeline (session_home) | 12.16 s | 44.9% |
| Per-session helper spawns (loop-body self time, basename/dirname/head/pwd, `$(...)` forks) | 5.12 s | 18.9% |
| Two `stat` per row | 2.42 s | 8.9% |
| format_epoch, both attempts | 2.68 s | 9.9% |
| The failing `date -r` attempt alone | about 1.1 s | about 4.1% |
| Glob across 437 folders (session_transcript) | 2.03 s | 7.5% |
| session_place (git, `pwd -P`) | 1.95 s | 7.2% |

Not the main cost: the glob (about 2 s despite about 208,000 path checks). Real but minor: the failing `date -r` (a pure bug, about 1.1 s). Not separable from captured data: spawn cost versus scan CPU inside the 12.16 s (unverified). CPU share: measured 0.7 core of 28 is about 2.5% of this machine, against the reported 5-10%; consistent only on a smaller machine (unverified).

## Proposed Fix (on src/superclaude/skills/ccsession-tag/ccsession after rebasing onto origin/master; the checkout copy is older and was not read)

1. Batch helper (main change): a python3 helper beside `retention.py` (precedent: I:1674-1675 calls a python3 helper in `$CCSESSION_DIR`), for example `scan_sessions.py`, called once per run from list_sessions: one directory scan maps uuid to newest transcript (rule of I:1481-1482), then the same head 256 KiB + tail 1 MiB scan and the same "first cwd whose sanitised name equals the transcript's folder, else first cwd" rule (I:1378-1397); prints one tab-separated record per uuid; writes no file; still reads only the two ends.
2. Timestamps: one `stat -c '%W %Y'` per row (GNU first, BSD `stat -f` only in the fallback), or one `stat` over all files with `%W %Y %n`; in format_epoch try `date -d "@$epoch"` first and fall back to `date -r` (both primitives kept; text `%Y-%m-%d %H:%M` unchanged).
3. Fallback: if python3 or the helper is missing or fails, run the existing per-session path unchanged (bash 3.2 behaviour kept; no associative arrays in bash); session_place stays per row (needs git and `pwd -P`).

Files: ccsession (list_sessions, format_epoch, stat calls); a new helper in src/superclaude/skills/ccsession-tag/; tests/unit/test_ccsession_tag.py; possibly the installer manifest and README (install of `retention.py` not verified). Three files at minimum, four or more if manifest or README change: flag for the escalation rubric.

Tests: existing `_listed` tests (tests/unit/test_ccsession_tag.py:3897) and the pinned-format tests (4474, 4522, 4551, 4585, 3465, 2740), not read by the worker (unverified); new test A (spawn count does not grow with N=10 vs N=60, counting shims for `date`, `head`, `stat`, `ls`, `dirname`, `basename` on PATH); new test B (byte-identical output with the helper and with python3 hidden from PATH; no new file); re-measurement of Task 1 and `time ccsession --here` against 27.07 s and 14.47 s (expected lower bound derived: the 0.75 s prototype plus session_place's 1.95 s, not a prediction).

## Confidence

Self-reported: 0.8. Evidence grounding 1.0 (self times, process counts, wall times, prototype captured with provenance; cited source lines Read). Runtime check 1.0 (executed trace and timing runs by the parent). Symptom coverage 0.5 (27 s and list-size dependence covered; CPU percentage not; spawn-versus-scan split unresolved). Reproducibility fit 1.0 (27.069 s `--here`, 14.473 s `--list` reproduced). Fix directness 0.5 (prototype shows the speed-up is possible; the real helper is unwritten and must match pinned formats). Domain coherence 1.0.

## Risks

Behaviour drift (the helper must reproduce the cwd-matching rule incl. JSON unescaping at I:1386-1389, the "(transcript missing)" and "(times unavailable)" rows and here/gone/other classification); birth time (Python's `os.stat` has no portable Linux birth time, so the sketch keeps `stat -c '%W'` in bash); python3 availability (the fallback stays slow; `retention_warning` I:1665-1678 already tolerates a missing python3); timeout window (`--ask` runs the list before the 30 s question inside Orca's 60 s readiness window, I:1733-1735).

## If I'm wrong, it's probably because

The 12.16 s in session_home is mostly one pathological cost not isolated (for example `grep -oE` backtracking on long lines, or cold-cache reads of 23G) that a per-session Python scan would also pay; or sys time under load average 11.9 inflates every fork, so the 27 s is partly an artifact of this machine's load.

## Falsification standard

Probe: two arms over the same 439 session transcripts, written and run by the parent at a trusted boundary. Arm 1 loops `{ head -c 262144 "$f"; echo; tail -c 1048576 "$f"; } >/dev/null` (no grep, no awk). Arm 2 loops the same `{ ...; } | grep -oE '"cwd":"([^"\\]|\\.)*"' | awk '!seen[$0]++'` pipeline. No numbers were written by the worker.

| Probe result | Reading |
|---|---|
| Arm 1 time is close to the traced 12.16 s | Cost is spawn and read; the regex is not the issue; claim weakened; the Python prototype's 0.73 s read of 554 MB would probably be a warm-cache artifact and the fix must be re-validated cold. |
| Arm 1 far below 12.16 s and Arm 2 close to 12.16 s | Cost is the regex pipeline per session; supports the claim and the helper fix. |
| Both arms far below 12.16 s | The 12.16 s came from something else (for example the `while read` loop at I:1385-1397 or cache state); the claim is false. |

Falsifier: "If the Arm 1 loop alone reproduces about 12 s on the same store, the claim that regex and per-session pipelines dominate session_home is false, and the prototype's speed-up must be re-established with a cold-cache run."

## Alternatives considered

Failing `date -r` as root cause (rejected, about 1.1 s, 4.1%); glob across 437 folders (rejected, 2.03 s, 7.5%); slow model refresh (rejected, 0.17 s); a cache file (rejected, violates README:190 "Listing never writes any file").

## Grounding gaps

Not Read by the worker: tests/unit/test_ccsession_tag.py, README:190 and README:275, the installer manifest, retention.py, ccsession-orca, the checkout copy of ccsession, any codegraph output (shell not indexed). Unverified: the split of 12.16 s between spawn and regex CPU; cold-cache cost; how the helper would be installed; whether tests stub `python3`; the 5-10% CPU figure on a smaller machine. Diagnosability verdict partial (diagnosability-context.md).
