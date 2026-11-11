#!/usr/bin/env python3
"""Detect finished workers, ingest them, run the script steps (merge, ledger revise), prepare the next prompts.

Prints one `LAUNCH <model-alias> <absolute PROMPT path>` line per worker to launch (C9.5), at most MAX_CONCURRENT - running,
in run order then step order. Records the launches in each run's state (the launch ledger) unless --dry-run.
Options:  --dry-run            print what would be launched; record and change nothing
          --stratum S          sonnet (default), haiku, or all
Cost never stops anything here (D6): no token or dollar check exists in this driver.
"""
import sys, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import harness as h


def main(argv):
    dry = "--dry-run" in argv
    stratum = argv[argv.index("--stratum") + 1] if "--stratum" in argv else "sonnet"
    strata = {"sonnet", "haiku"} if stratum == "all" else {stratum}
    wants = []
    for run in h.all_runs(strata):
        for key, alias, prompt in h.advance_run(run, dry_run=dry):
            wants.append((run, key, alias, prompt))
    running = 0
    for run in h.all_runs():
        st = h.load(run)
        running += sum(1 for k in st["launched"] if k not in st["done"] and k not in st["lost"])
    room = max(h.MAX_CONCURRENT - running, 0)
    n = 0
    for run, key, alias, prompt in wants[:room]:
        print(f"LAUNCH {alias} {prompt}")
        n += 1
        if not dry:
            st = h.load(run)
            st["launched"][key] = {"alias": alias, "prompt": str(prompt), "t": h.now(), "t_epoch": time.time()}
            h.save(run, st)
    held = len(wants) - n
    print(f"# running {running}, launched now {n}, waiting for a free slot {held}" + (" (dry run: nothing recorded)" if dry else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
