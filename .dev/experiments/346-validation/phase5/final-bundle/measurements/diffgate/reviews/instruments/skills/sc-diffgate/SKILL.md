---
name: sc-diffgate
description: Infrastructure skill for /sc:spec-panel-diffgate. Its stdlib script diffgate.py computes the re-review surface of a spec review loop, checks the reviewer's machine-readable findings block and the reviser's fix map, and keeps the loop ledger (review count, verdict, blocking findings). Delegate-only, no slash command.
allowed-tools: Read, Bash
---

# sc-diffgate: computed re-review surface and loop ledger

Delegate-only infrastructure skill with no slash command. It is the contract of `scripts/diffgate.py`, which `/sc:spec-panel-diffgate` and the coordinator's loop steps run. The script uses the Python standard library only, writes only inside `--dir` and never writes the reviewed specification.

## Call form

`uv run --no-project python "<diffgate base>/scripts/diffgate.py" <subcommand> ...`, where `<diffgate base>` is `~/.claude/skills/sc-diffgate` if it exists, else the project `.claude/skills/sc-diffgate` copy.

## Who runs what

Owner ruling (issue #346): the review and revision sessions run only the read-only calls `status`, `check --dry-run` and `fixcheck --dry-run`, which write no file anywhere, to self-validate and to use their one repair turn. Every call that writes (`begin`, `check` and `fixcheck` without `--dry-run`) is run by the coordinator as its own step between the review and revision tasks. The reviser keeps its fix map inside its own disposition file as a `## Diffgate fixmap` block; the coordinator's `fixcheck` step passes that file as `--map`. The coordinator's `check` step appends `close-r<N>.md` (which ends with the verdict line) to the review report.

## Subcommands

Subcommands (each prints one JSON object with `ok`, `exit`, `message`, `review` plus the fields shown):

| Subcommand | Writes | Extra stdout fields |
|---|---|---|
| `begin --dir D --doc F [--expect-round N]` | `ledger.json`, `doc-r<N>.md`, `surface-r<N>.md` (N of 2 or more); for N of 2 or more it first re-runs the fix-map check against `doc-r<N-1>.md` and the current spec, and any unmapped hunk exits 1 with the unmapped list and opens nothing | `surface`, `hunks`, `ignored`, `coverage`, `priors` |
| `check --dir D --report R` | `result-r<N>.json`, `reviser-brief-r<N>.md`, `deferred.md`; or `reject-r<N>.txt` | `accepted`, `verdict`, `verdict_line`, `acceptance` (`clean` or `scoped`), `blocking`, `deferred`, `degraded`, `halt` |
| `fixcheck --dir D --doc F [--map M]` | ledger fix record; pre-fills map candidates from inline `R<N>.<j>` tags; exits 1 when the map's `doc_sha` line differs from the spec; the third failure in one cycle records `fix-rejected` | `hunks`, `mapped`, `declined`, `withdrawn` candidates, `bytes_by_id`, `hunks_by_id`, `unmapped` |
| `status --dir D` | nothing | `state` (`open`, `checked`, `fixed`, `closed`, `invalid`), `next` (the one command that should run next) |

Additions to the table: `check` and `fixcheck` accept `--dry-run`, which runs every validation of the real call, prints the same fields plus `dry_run: true`, writes no file anywhere (no ledger, lock, temp file, reject file or map file) and counts as no attempt. `check` also writes `report-r<N>.md` (a byte copy of the checked report, which the replay reads) and `close-r<N>.md` (the closing block for the report). `fixcheck --map` reads only the lines under a `## Diffgate fixmap` heading when the file has one; without `--map` it pre-fills `fixmap-r<N>.txt` from the candidates and checks them. `status` also prints `review`, `halt` and a held lock with its recovery step; with no ledger its state is `none`.

`check` also prints `proxy_all`, the owner-decision count (also in `result-r<N>.json`): the number of distinct finding ids with a CRITICAL or MAJOR label among the findings first raised in this review (deferred, demoted and over-`via`-cap ones included), the prior blocking findings marked `open`, `regressed` or `withdrawn` in this review, and every CRITICAL or MAJOR finding the script deferred, demoted or withdrew at any earlier review of the loop; it is cumulative over reviews 1 to 3.

Exit codes: 0 done (includes an accepted review whose verdict is FAIL); 1 input rejected (`check`: bad report; `fixcheck` or `begin`: unmapped or unknown hunks); 2 usage error or an input over the limits; 3 an input file missing, unreadable or empty; 4 loop closed (`halt: pass`, `halt: escalate`, `halt: invalid`); 5 steps out of order (no accepted check or fix map for the current spec hash, spec edited during a review, or `--expect-round` differs); 6 ledger corrupt or disagreeing with the replay of the recorded report.

## Finding grammar

Report block, under the heading `## Diffgate findings`, one line per item, keyword at column 1:

```text
PRIOR R1.5 resolved by=H2.2
PRIOR R1.9 open quote="still lets WC-7 skip the command file"
PRIOR R1.7 withdrawn quote="..." reason="declined in fixmap-r1.txt: the cited rule does not exist"
FINDING R2.1 sev=major at=60-63 hunk=H2.2 anchor="appears in that worker's worker-read output" outcome="correct launcher runs are recorded as WC-1 not exercised" :: AC-0.4 reads the wrong source
FINDING R2.2 sev=major at=312 via=H2.3 via_quote="7.2 step 1 --worktree current" anchor="places the worker in the current worktree" outcome="..." :: H2.3 now assumes an own worktree
FINDING R2.3 sev=minor at=140 cites=R1.9 anchor="..." :: more evidence for R1.9
```

Line forms: `PRIOR <id> resolved by=H<k>.<n>`; `PRIOR <id> open quote="..."`; `PRIOR <id> regressed by=H<k>.<n> quote="..."`; `PRIOR <id> withdrawn quote="..." reason="..."`; `FINDING <id> sev=<critical|major|minor> at=<line or a-b> hunk=H<k>.<n> anchor="..." [outcome="..."] :: text`, with optional `via=H<k>.<n> via_quote="..."`, `cites=<id>`, `fr=8|9|10` and `side=old` (a finding that anchors through `via=` or `cites=` omits `hunk=`); or the single line `FINDINGS none`. Quoted values are JSON strings (`json.loads` on the token). `at=` refers to lines of `doc-r<N>.md`, 1-based and inclusive. Finding ids are `R<N>.<j>`, `j` from 1 with no gap. The reviewer writes no `verdict:` line.

Review 1 has no computed surface and no prior ids, so a review-1 finding is `FINDING R1.<j> sev=<critical|major|minor> at=<line or a-b> anchor="..." [outcome="..."] [fr=8|9|10] :: text` with no `hunk=`, `via=`, `via_quote=`, `cites=` or `side=`; it gets `origin=full` and is never deferred. With `side=old`, `at=` counts lines of `doc-r<N-1>.md`. `FINDINGS none` replaces only the `FINDING` lines; the `PRIOR` lines stay required beside it. Ids of earlier reviews may appear in the prose; every current-review `R<N>.<j>` in the prose must be a `FINDING` id.

## Files in `<dir>`

`ledger.json` (the only state: per review the document hash, hunks, prior findings, accepted check, fix record, attempt counters, the cumulative counted and scoped sets; flags `closed` and `halt`); `doc-r<N>.md` (byte copy of what review N saw); `surface-r<N>.md` (review N's surface, N of 2 or more); `result-r<N>.json` (accepted findings with derived origin, blocking and verdict); `report-r<N>.md` (the checked report); `close-r<N>.md` (open blocking findings with fix chains, `## Deferred (pre-existing, not looped on)`, the `scoped PASS:` line, or the Reviser brief, then the verdict line); `reject-r<N>.txt`; `reviser-brief-r<N>.md` (blocking ids only); `fixmap-r<N>.txt` (the accepted map); `deferred.md` (each deferred finding with the reviewer's own label and the disclosure sentence); `.lock` (pid of the step holding the lock; a lock whose pid is not running is removed and reported).

## Profiles

`PROFILES` in `diffgate.py` maps a reviewer name to its severity labels and its blocking function. The only profile is `spec-panel`: `critical`, `major`, `minor`; blocking is `sev=critical`, `fr=8` or `fr=9`, or `sev=major` with an `outcome` other than `-`. A later adopter adds its own entry; nothing else in the script knows which reviewer wrote the report.
