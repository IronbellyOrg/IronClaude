## Troubleshoot findings: root cause and remediation (from `/sc:troubleshoot --type performance --fix --depth deep`)

Status: partial. The root cause is measured and reproduced. The remediation below is the adversarial merge of three fix proposals with the corrections of its independent review applied (one blocking finding, F1, fixed in the text; the corrected text has not been re-reviewed).

Notation: `I:<n>` means line n of `~/.claude/skills/ccsession-tag/ccsession`, the installed copy. It is byte-identical to `src/superclaude/skills/ccsession-tag/ccsession` on origin/master 10f6ec670 (2072 lines; ccsession is unchanged through e3e9d636a). The checkout of a branch cut before that is older (1902 lines), so line numbers do not map to it.

### Root cause (measured on the reporter's kind of store: 477 saved names, 439 transcripts, 437 workspace folders, 28 cores)

`ccsession --ask` (run by `ccsession-orca` for every new plain Claude tab, `ccsession-orca:204`) builds the list with `list_sessions` (I:1554-1663) in worktree mode (the same code as `ccsession --here`). For every saved name it runs about 13 external processes plus a transcript scan, and prints nothing until the whole list is built (`sessions=$(... list_sessions ...)`, I:1718); only then the 30 s question starts, inside Orca's 60 s readiness window (I:1733-1735).

- `ccsession --here`: 27.069 s at load average 11.9 (user 5.823 s, sys 13.566 s, 405 lines); 22.5 to 24.7 s at lower load (23.586, 24.663, 22.471 s). `ccsession --list` 14.473 s. The model-data refresh is not the cause (0.17 s).
- Self time per function (bash -x trace with a timestamp, 27.08 s): session_home 12.16 s (I:1377-1399, 439 calls), list_sessions loop body 5.12 s, format_epoch 2.68 s (I:1533-1537), session_transcript 2.03 s (I:1480-1483), session_place 1.95 s, get_btime + get_mtime 1.22 + 1.20 s. At least 6,403 external processes for 477 rows: date 1756, head 972, dirname 936, basename 936, stat 878, ls 477, grep 448.
- Defect 1, design: one `head | tail | grep | awk` pipeline per session (I:1396-1397), one `ls -t */<uuid>.jsonl` per session (I:1482, because the transcripts live under per-cwd folders, not the repo-keyed folder, I:1595-1599), two `stat` and two `date` per row (I:1610-1617).
- Defect 2, bug: `local store want cwd first="" LC_ALL=C` (I:1383) and `local b LC_ALL=C` (I:1403) never reach `grep`, because a `local` variable that was not already exported is not passed to child processes (probe: `bash -c 'f() { local x LC_ALL=C; env | grep -c "^LC_ALL="; }; f'` prints 0). So grep runs in the user's UTF-8 locale. Isolated pipeline over the 439 transcripts: 13.227 s in UTF-8 vs 6.460 s with `LC_ALL=C` (head and tail alone: 1.442 s). End to end, alternating runs: plain 23.586, 24.663, 22.471 s vs `env LC_ALL=C` 16.657, 16.244, 16.597 s: median gap 6.99 s (this exports LC_ALL=C for the whole script, not only for grep).
- `format_epoch` runs `date -r <epoch>` first, which on GNU takes a file and always fails (`date: 1794941650: No such file or directory`, exit 1), then `date -d @`: 878 wasted processes, about 1.1 s.
- A one-process prototype of the transcript index plus the same head 256 KiB + tail 1 MiB scan took 0.75 s for the 439 sessions (554 MB, warm cache, without session_place's git calls).
- Not explained: the reported 5-10% CPU (measured 19.4 s CPU in 27.1 s wall, about 0.7 of one core, about 2.5% of this 28-core machine).

### Remediation (hand this section to `/sc:workflow`)

Ship in two changes. Stage 1 is a standalone change of 2 files (`src/superclaude/skills/ccsession-tag/ccsession`, `tests/unit/test_ccsession_tag.py`) and stays in place afterwards as the fallback of Stage 2. Stage 2 touches 3 to 4 files. First rebase the branch onto origin/master. After editing run `make sync-dev`, and `make verify-sync` before committing; never stage `.claude/` paths.

**Stage 1 (bash 3.2 safe: no associative arrays, no `mapfile`, no `printf '%(...)T'`):**

1. Locale: prefix `LC_ALL=C` on the `grep` and the `awk` in session_home (I:1396-1397) and on the `grep` in session_branch (I:1405). Keep the `local ... LC_ALL=C` lines (they only affect bash's own matching). Measured effect: about 7 s of 23.6 s.
2. Hoist work out of the per-row command substitutions (review finding F1, blocking): the transcript index, the `date` flavour probe and any other cache must be built in the parent shell before the row loop, because `$(...)` runs in a subshell and discards variables. Today the row loop calls `$(session_transcript ...)` (I:1599), `$(get_btime ...)` (1610), `$(get_mtime ...)` (1611) and `$(format_epoch ...)` (1616, 1617). Replace them with calls that set named variables (`printf -v` or plain assignment) without `$(...)`. Keep the existing functions for the resume path (I:2054-2055) and as the fallback.
3. Transcript lookup (F2, F3): build the index once before the loop: `idx=$(ls -t "$PROJECTS_DIR"/*/*.jsonl 2>/dev/null) || true` (the `|| true` because of `set -e`, I:132). If the index is empty or `ls` failed, fall back to the existing per-uuid glob (I:1480-1483). Look up a uuid by parameter expansion (no bash loop over the index per row; for example `pre=${idx%%"/$uuid.jsonl"*}` and take the text after the last newline), keep the rule "own repo-keyed folder first, newest copy otherwise" (I:1595-1600), and keep the newest-copy rule (I:1481): the first match in `ls -t` order is the newest copy.
4. Dates: probe once, in the parent shell, with `date --version`; on GNU use `date -d "@$epoch"` first; elsewhere keep the BSD-first order (`date -r`). Do not use `printf '%(...)T'` (macOS bash 3.2 lacks it, I:1690, 1823). The text `%Y-%m-%d %H:%M` must not change (I:1533-1537).
5. Stat: one `stat -c '%W %Y' "$jsonl"` per row, GNU first (BSD `stat -f '%B %m'` only when the GNU form fails, I:1490, 1516), split into two variables with parameter expansion. An empty or 0 birth time must still give `(times unavailable)`.
6. Per-row string work: replace `basename`, `dirname` and `head -n 1` with parameter expansion; for the uuid use `uuid=""` first, then `IFS= read -r uuid < "$topic_file" || true` (F4: a failed redirect must not leave the previous row's uuid).
7. Optional, only if the trace shows it and the output stays byte-identical: classify a row as `other` before the time and duration work (rows later discarded, I:1610-1627, 1636; about 0.9 s on assumptions about the count of `other` rows).

**Stage 2 (python3 batch helper, bash fallback is Stage 1):** add `scan_sessions.py` beside `retention.py` in `src/superclaude/skills/ccsession-tag/` (precedent: I:1674-1675 calls a python3 helper in `$CCSESSION_DIR`; `install.sh:40` and `src/superclaude/cli/install_skill.py:52` copy the whole skill folder, so no manifest edit). Call it once per list, inside the `first` block so the lazy heading holds. Bash passes the topic files' uuids in its own glob order and the repo-keyed folder. For each uuid the helper prints one `\x1f`-separated record in input order (transcript path, session start folder). Rules it must keep (F6): prefer the file in the repo-keyed folder, newest copy otherwise (I:1595-1600); run the cwd scan only for the worktree filter (I:1606-1609), never for `--list`; read bytes, head 256 KiB then tail 1 MiB, head first and skip the tail when a store-matching folder is found; apply the two unescapes in the order of I:1388-1389 (`\"` to `"`, then `\\` to `\`), not `json.loads`; per-byte folder match against the store folder, first-cwd fallback and dedup as in I:1390-1398; write no file; birth time stays in `stat -c '%W'` (Python has no portable Linux birth time). Bash captures the output inside `if out=$(...); then`; any failure, or short output, runs Stage 1 unchanged.

**Stage 3 (optional):** move stat and date strings into the helper, only if the Stage 2 trace still shows more than about 2 s in stat and date; needs its own parity test.

**Out of scope:** bounding the list to the N newest rows (changes the output contract); a cache file (README:190 "Listing never writes any file"); printing rows as they are built (changes the `show_saved` contract, I:1715-1731; separate follow-up); the hook that would record each session's start folder; `session_place`'s git calls (1.95 s).

### Tests (add to `tests/unit/test_ccsession_tag.py`; run them through the real entry points `ccsession --here`, `--list` and `--ask`, not by calling the helper directly)

- All existing `_listed` tests and the pinned-format tests (4474, 4522, 4551, 4585, 3465, 2740) pass unchanged; output text, exit codes (0, 1, 3, 130), the stdout/stderr split and the here/gone/other classification stay byte-identical.
- Spawn count: counting shims for `date`, `stat`, `head`, `ls`, `basename`, `dirname`, `grep`, `awk` first on PATH; N=10 vs N=60 topic files; the count must not grow with N; fails if the transcript index is built more than once (F1).
- Locale shim: a `grep` on PATH that records `$LC_ALL` and must see `C`.
- Parity (Stage 2): helper vs python3 hidden from PATH, all three views, byte-identical stdout, stderr and exit code. Fixtures: transcript missing; transcript only in another folder; two copies (newest wins); store folder only in the tail; first cwd not matching; escaped quote and backslash in a cwd; non-ASCII cwd; cwd with invalid UTF-8 bytes; file under 256 KiB and over 1.25 MiB; a cwd that straddles the 256 KiB cut; a tail that starts mid-line; deleted folder; `%W` printing 0 giving "(times unavailable)"; topic names with spaces and `%2F` escapes; a topic file whose uuid has no transcript; an unreadable (mode 000) topic file; an empty store and a one-row list.
- Date probe: GNU, BSD (a shim whose `--version` fails) and busybox; `${x##*/}` and `${x%/*}` against `basename` and `dirname` (trailing slash, a `.txt` name, no slash).
- `|| true` under `set -e` for the `read` and for the `ls` index; the empty-index fallback.
- No file appears under HOME or TMPDIR while listing (README:190).
- A static test that rejects bash 4 constructs in the changed region (no test runs under bash 3.2).

### Success measure and gates

- Re-run on the same store: the `bash -x` PS4 timestamp trace (`PS4='+T ${EPOCHREALTIME} ${FUNCNAME[0]:-main} ' bash -x ~/.local/bin/ccsession --here`, sum the gap per function) and `time ccsession --here` / `--list` three times each with `uptime` recorded; compare with 27.069 s and 14.473 s (and 22.5-24.7 s at lower load).
- Derived targets, not executed: Stage 1 about 14.6 s remaining (12.47 s itemised savings; it uses a 1.2 ms per-fork proxy for dirname, basename and head that was not measured), Stage 2 A-core about 4.62 s (helper does the index and scan; bash keeps one `stat` and one `date -d` per timestamp) or A-full about 2.70 s (helper does stat and date strings as well). The three proposals disagreed on the remaining time (about 13.6 s helper only, 11.6-14.1 s bash only, 14.6 s Stage 1): measure before claiming one.
- Gates (open assumptions): A-001 capture the reporter's `locale` and number of saved names, or reproduce with `LANG=en_US.UTF-8`; A-002 measure Stage 2 once on a cold page cache (all timings and the 0.75 s prototype ran warm); A-004 measure the per-spawn cost of `dirname`, `basename` and `head` (200 iterations) before relying on the 2.8 s saving; the cost of the index lookup of item 3 must be measured (F3).
- Orca window: the `--ask` budget is 60 - 30 = 30 s and the list takes 27.07 s here, leaving 2.93 s: a store about 11% larger already makes an unanswered question outlast Orca's 60 s readiness limit, so ship Stage 1 first.

### Constraints that must hold (from README and the code)

Only the start and end of a transcript are read (I:1380); the session's start folder is the first recorded cwd whose sanitised name equals the transcript's folder, else the first one (I:1378); GNU `stat -c` first (I:1490, 1516); `last` is the transcript's change time and nothing touches transcript files (README:275); bash 3.2 compatibility (I:1690, 1823); "Listing never writes any file" (README:190); the pinned output formats and the first two lines that `show_saved` drops.

### Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Helper drift against the pinned cwd rule | Medium | wrong start folder, so the here/gone/other class changes | parity tests above |
| `read < file` leaves the previous uuid on failure | Low | a row shows another session | `uuid=""` first; chmod-000 fixture |
| `ls` index aborts under `set -e` or is empty | Low | script exits or rows read "(transcript missing)" | `|| true` and the per-uuid fallback; empty-store fixture |
| Locale change alters output for folders with invalid UTF-8 bytes (UTF-8 grep may drop them, C-locale grep keeps them; GNU grep behaviour, unverified) | Low | output differs for those folders only | fixture |
| python3 missing or the macOS stub | Low to Medium | helper path fails or is slow | Stage 1 fallback; test with python3 hidden |
| `date --version` probe on BSD | Low | wrong date text on macOS | probe once; keep BSD-first order elsewhere |
| Stage 1 alone leaves about 14.6 s (derived) | Medium | a store 11% larger than 27.07 s breaks the 60 s Orca window if unfixed | ship Stage 2; gates above |

### Follow-ups noticed (not part of this fix)

- The listing runs before the question and prints nothing until it ends (I:1718); printing rows as they are built, or starting the 30 s clock earlier, are contract changes.
- A hook that records each session's start folder at session start would remove the transcript scan; it needs a store-format change and a migration for existing sessions.
- `src/superclaude/agents/troubleshoot-analyst.md` lacks the `mcp__litellm__augment_code-augment_code_search` tool that the installed troubleshoot protocol lists in its closed roster (the project and src copies list only the auggie tool); decide whether to add it.
- The reported 5-10% CPU was not reproduced (about 2.5% of this 28-core machine); ask the reporter for core count and store size.

### How to claim and run this

Whoever claims this issue: invoke `/sc:workflow` on the "Remediation" section above (for example `/sc:workflow "Implement the remediation in the 'Troubleshoot findings' section of issue 607 (ccsession --ask list speed): Stage 1 first, then Stage 2" --depth standard --handoff none`), read the plan and its pre-execution review, and only then `/sc:implement <printed plan path>`. Do not skip the review: the first draft of this plan had a blocking mistake (per-row caches built inside `$(...)` subshells are lost) that an independent reviewer caught; the corrected text should be re-reviewed by `/sc:workflow`'s own `/sc:reflect --mode pre`. A written plan is required: more than one source file changes.
