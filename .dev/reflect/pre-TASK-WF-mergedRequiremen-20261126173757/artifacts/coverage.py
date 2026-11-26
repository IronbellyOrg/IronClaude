"""UC-1 coverage matrix for the reflect run (Step 1B.0 Pass 2 rows + deterministic containment match).

Pass 1 (ID_REGEX) found 0 parsed ids in the spec and the tasklist, so every row is inferred.
Each row carries a verbatim quote and a spec line range; the script re-reads the spec and drops
any row whose quote is not found in the cited lines (quote-pinning). Matching is pure string
arithmetic: stopword-stripped content-word containment >= 0.6 against a single task item.
"""
import json
import re
import sys
from pathlib import Path

PKG = Path(".dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239")
SPEC = PKG / "source.md"
PLAN = PKG / "TASK-WF-mergedRequiremen-20261126-173239.md"
OUT = Path(sys.argv[1])

ROWS = [
(10, 10, r'''One new file `src/superclaude/cli/sweep/ledger.py`, command `superclaude sweep ledger`, attached to the existing `sweep_group` (no `main.py` change); pure `decide()`; own Orca runner, not `sweep/probes.py`.'''),
(11, 11, r'''`sweep run` reads the ledger (file read, no Orca call) when no `--run` and no terminal-bound Run; explicit `--run` wins; no new flag; stale header at 90 minutes.'''),
(12, 12, r'''Fixed per-user file `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json`, override `--ledger` or env `SUPERCLAUDE_RUN_LEDGER`. Never under the repo.'''),
(13, 13, r'''`fcntl.flock` sidecar lock, 10 s timeout then exit 3; atomic temp file + `fsync` + `os.replace`; rebuild merges hook entries newer than its own start.'''),
(22, 22, r'''`--dry-run` prints the would-be ledger and writes nothing; `--json` prints the summary as JSON.'''),
(23, 23, r'''append one id (idempotent; validated with the sweep id pattern `probes.RUN_ID_RE`; merges under the lock; no Orca call).'''),
(24, 24, r'''No `show`, `path`, `--timeout`, `--no-ledger`, or sweep `--ledger` flag.'''),
(26, 26, r'''never through `sweep/probes.py`, so the pinned `ALLOWED_ORCA` and `tests/sweep/test_probes_allowlist.py` stay unchanged and green.'''),
(27, 27, r'''use `find_orca` in `src/superclaude/cli/issue_watch/` if its signature fits, else `shutil.which("orca")`.'''),
(42, 42, r'''`generated_at` is captured BEFORE the first Orca call, so the `new` rule cannot miss a Run created mid-build.'''),
(43, 43, r'''`--add` keeps `generated_at` unchanged (so sweep staleness is not masked)'''),
(47, 47, r'''Never infer that a Run exists from `worker-list`'''),
(48, 48, r'''any worker row has `resource.worktreeId` exactly equal (whole string) to an `id` in `worktree list --json` `result.worktrees[].id`.'''),
(49, 49, r'''any Task whose `status` is NOT in the terminal set `{completed, failed, cancelled}`.'''),
(50, 50, r'''With no previous ledger, or an unreadable one, `new` means `created_at` within the last `NEW_FALLBACK_HOURS = 24` (named constant).'''),
(51, 51, r'''A hook-added entry newer than the rebuild start is kept (see Concurrency); an older one is re-evaluated by the three rules like any other Run.'''),
(52, 52, r'''No age cutoff and no main-checkout exclusion is built (over-inclusion is the safe direction); a cutoff is the owner's decision (see Open decisions).'''),
(56, 56, r'''A repeated cursor, or more than 50 pages for one Run, is a failure (exit 1).'''),
(57, 57, r'''Short-circuit: fetch Tasks first; fetch workers only for Runs not already IN by Task or `new`.'''),
(59, 59, r'''Runs admitted only by `ready` or `blocked` Tasks whose `updated_at` is older than 7 days; the count of Runs held in only by `blocked` Tasks.'''),
(63, 63, r'''the old ledger is left untouched, one reason goes to stderr (first word `orca-failure:` or `implausible:`), and the exit is non-zero.'''),
(64, 64, r'''Any Orca call exits non-zero, times out (30 s each), or returns JSON without `"ok": true` (`orca-failure:`).'''),
(65, 65, r'''`worktree list` returns 0 worktrees (the main checkout always exists, so 0 is a broken read) (`implausible:`).'''),
(66, 66, r'''`run-list` returns 0 Runs while a previous ledger exists (`implausible:`).'''),
(67, 67, r'''`--accept-empty` overrides this guard only, never an Orca failure.'''),
(69, 69, r'''Exit codes: 0 written; 1 Orca failure or implausible result; 2 usage (including `--add` with a malformed id); 3 lock timeout. No 20% shrink guard.'''),
(74, 74, r'''blocking up to 10 s, then exit 3 with the ledger untouched'''),
(75, 75, r'''A rebuild does all Orca reads first (about 26 s) without the lock, then takes the lock, re-reads the ledger, and writes the rebuilt set plus every entry with `source == "hook"` and `added_at >= generated_at`.'''),
(76, 76, r'''temp file `run-ledger.json.tmp.<pid>` in the same directory, `fsync`, `os.replace`; readers see the old or the new file, never half.'''),
(77, 77, r'''`--add` on a missing or unreadable ledger writes nothing and exits 1 with `implausible:`'''),
(81, 81, r'''validate each id with `probes.RUN_ID_RE`, and sweep them. Explicit `--run` always wins and the ledger is then not read'''),
(82, 82, r'''When `generated_at` is older than 90 minutes (the #895 threshold, three missed 30-minute builds) the header adds "ledger is N min old"; sweep still runs'''),
(83, 83, r'''Missing or corrupt ledger: exit 2 with the old "no Run bound" message plus `run "superclaude sweep ledger" first`.'''),
(84, 84, r'''Sweep's `ALLOWED_ORCA` is unchanged.'''),
(85, 85, r'''edit `src/superclaude/commands/sc/sweep.md` (the `--run` row and the "no Run is bound" sentence)'''),
(90, 90, r'''PostToolUse, matcher `Bash`; script `run-ledger-record.sh`, delivered to `~/.claude/hooks/` by `superclaude install`'''),
(91, 91, r'''acts only when `tool_input.command` runs `orca orchestration run-create` or `worker-start`.'''),
(92, 92, r'''Always exits 0 (fail open, never blocks).'''),
(93, 93, r'''We never edit `~/.claude/settings.json`.'''),
(96, 96, r'''run exactly one `orca orchestration run-create --objective "scratch Run for the run-ledger hook payload test, safe to ignore" --json`'''),
(97, 97, r'''Run id present in the output means the hook is delivered; absent means the hook is dropped with that reason'''),
(98, 98, r'''a recorded payload under `tests/run_ledger/fixtures/`'''),
(102, 102, r'''Ship `docs/user-guide/run-ledger.md` for Coder#545 to adopt. Nothing is installed or registered by this work.'''),
(103, 103, r'''every 30 minutes at offset minutes (`17,47`), wrapped in `flock -n` on a lock file'''),
(104, 104, r'''Hook registration entry for Coder:'''),
(105, 105, r'''in Coder the crontab is rewritten on every boot, so a hand-edited crontab is lost'''),
(110, 110, r'''`env -i HOME=$HOME PATH=<the cron PATH> superclaude sweep ledger --dry-run` must exit 0.'''),
(119, 119, r'''`test_new_fallback_24h_when_no_previous_ledger`: with no or unreadable previous ledger, a Run under 24 h old is IN and an older one is OUT.'''),
(126, 126, r'''`test_add_idempotent_and_rejects_bad_id`; `test_lock_timeout_exit3`; `test_concurrent_add_and_build_no_lost_append` (multiprocessing, 20 adds during a slow build).'''),
(129, 129, r'''`test_hook_extracts_run_id_from_fixture`; `test_hook_ignores_other_commands`; `test_hook_no_id_logs_and_exits_0`; `test_hook_fails_open_when_superclaude_missing`'''),
(133, 133, r'''edit under `src/superclaude/` only, then `make sync-dev`; never stage `.claude/`'''),
(134, 134, r'''Report in `.dev/issues/895/result.md`: ledger written (path, counts); rebuild wall time against the 26.1 s baseline;'''),
(155, 155, r'''no `orca orchestration reset`, no Run delete; no Orca link flags (`--issue`, `--pr`); no `~/.claude/settings.json` edit; no crontab edit; nothing scheduled; no commit.'''),
(156, 156, r'''Not built: a package of modules, `show`, `path`, `--timeout`, `--no-ledger`, a sweep `--ledger` flag'''),
(157, 157, r'''Not touched: `sweep/probes.py` and `ALLOWED_ORCA`; Windows locking.'''),
]

STOP = set("a an the and or but nor of in on at to for from by with without as is are was were be been being it its this that these those not no then than so if when while which who whom whose into onto over under per via both either each any all only also may must shall should can will would could do does did has have had there their they them we you he she his her our your i".split())

def words(text):
    return {w for w in re.findall(r"[a-z0-9_]+", text.casefold()) if w not in STOP and len(w) > 1}

spec_lines = SPEC.read_text().splitlines()
plan_text = PLAN.read_text()
tasks = {}
for m in re.finditer(r"^## Task (\d+):.*?(?=^## (?:Task|Phase) |\Z)", plan_text, re.S | re.M):
    tasks[int(m.group(1))] = m.group(0)

matrix, dropped = [], []
for i, (ls, le, quote) in enumerate(ROWS, 1):
    block = "\n".join(spec_lines[ls - 1:le])
    rid = f"INF-{i:03d}"
    if quote not in block:
        dropped.append({"id": rid, "line": f"{ls}-{le}", "quote": quote[:80], "reason": "quote not found in cited lines"})
        continue
    qw = words(quote)
    best = (0.0, None)
    for tid, ttext in tasks.items():
        ratio = len(qw & words(ttext)) / len(qw) if qw else 0.0
        if ratio > best[0] + 1e-12:
            best = (ratio, tid)
    matched = best[0] >= 0.6
    matrix.append({"id": rid, "source": "inferred", "citation": f"source.md:{ls}" + (f"-{le}" if le != ls else ""),
                   "quote": quote, "match_method": "containment" if matched else "none",
                   "matched_task_ids": [best[1]] if matched else [], "best_ratio": round(best[0], 3), "best_task": best[1]})

total = len(matrix)
matched_n = sum(1 for r in matrix if r["match_method"] == "containment")
unmapped = [r["id"] for r in matrix if r["match_method"] == "none"]
summary = {
    "parsed_count": 0, "inferred_count": total, "dropped_at_emission": len(dropped),
    "coverage_pct": None, "coverage_pct_union": round(matched_n / total, 4) if total else None,
    "unmapped_requirements": [], "unmapped_requirements_union": unmapped,
    "S_dev_density": round(len(unmapped) / total, 4) if total else None,
    "coverage_degraded": "parsed-sparse" if total > 0 else None,
    "tasks_in_plan": sorted(tasks),
}
OUT.write_text(json.dumps({"summary": summary, "matrix": matrix, "dropped": dropped}, indent=1))
print(json.dumps(summary))
for r in matrix:
    if r["match_method"] == "none":
        print("UNMAPPED", r["id"], r["citation"], "best", r["best_ratio"], "task", r["best_task"], "|", r["quote"][:70])
for d in dropped:
    print("DROPPED", d)
