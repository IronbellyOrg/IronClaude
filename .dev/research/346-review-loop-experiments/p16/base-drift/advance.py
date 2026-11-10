#!/usr/bin/env python3
"""Drift-check state machine. `$SP/drive.sh p16/base-drift` runs this.  Prints LAUNCH <abs path> model=sonnet | RUNNING n | MANUAL | WARN | LOST | ALL DONE.
  advance.py [--dry-run]   builds sandboxes and writes the R1 prompts; marks nothing launched, ingests nothing.
Flow per run: R1 -> (PASS: both audits) | FAIL: V1 -> R2 -> (PASS: audits) | FAIL: V2 -> R3 -> audits.  AUD and AUD2 are prepared together
when the loop ends and launch in the same call.  Retry: a worker that finishes without its output file (or with verdict INCOMPLETE/NONE
on a review) is unlaunched and relaunched once; a second failure marks the run LOST.  Nothing stops for token cost."""
import datetime
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h  # noqa: E402


def finish_loop(run, end):
    st = h.load(run)
    st["loop_end"] = end
    st["final_spec"] = h.spec_stats(h.ws(run))
    h.save(run, st)
    h.prep(run, "AUD")
    h.prep(run, "AUD2")


def retry(run, step, why):
    n = h.unlaunch(run, step, quiet=True)
    if n > 1:
        print(f"LOST {run} {step}: {why}; second failure, run excluded")
    else:
        print(f"MANUAL {run} {step} {why}: relaunching once (prompt reprinted below)")
    return "retry"


def transition(run, step):
    """-> True handled, 'retry' step was unlaunched."""
    rec = h.load(run)["log"][step]
    if not rec["output_exists"]:
        return retry(run, step, "no output file")
    if step in ("R1", "R2", "R3") + h.AUDS and rec.get("verdict") in ("INCOMPLETE", "NONE"):
        return retry(run, step, f"verdict {rec.get('verdict')}")
    if step in ("V1", "V2"):
        h.prep(run, "R2" if step == "V1" else "R3")
    elif step in ("R1", "R2"):
        if rec["verdict"] == "PASS":
            finish_loop(run, "PASS")
        else:
            h.prep(run, "V1" if step == "R1" else "V2")
    elif step == "R3":
        finish_loop(run, "PASS" if rec["verdict"] == "PASS" else "R3-" + rec["verdict"])
    elif step in h.AUDS:
        st = h.load(run)
        if all(s in st["done"] or s == step for s in h.AUDS):
            st["complete"] = True
            h.save(run, st)
    return True


def detect_finished(run, st, idx):
    out = []
    for step, when in list(st["launched"].items()):
        if step in st["done"]:
            continue
        outp = h.out_path(run, step)
        cands = idx.get((run, step))
        best = h.pick(cands, "sonnet", f"{run} {step}") if cands else None
        exists = outp.exists()
        if best is not None:
            if best["done"]:
                out.append((step, best["tokens"], not exists))
        elif exists and time.time() - outp.stat().st_mtime > 180:
            out.append((step, None, False))
        if not exists:
            age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(when)).total_seconds()
            if age > 3600:
                print(f"WARN stale {run} {step}")
    return out


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    dry = "--dry-run" in argv
    if dry:
        print("DRY-RUN (nothing is marked launched, nothing is ingested)")
    if not h.all_runs():
        h.build()
    idx = {} if dry else h.scan_transcripts()
    for run in h.all_runs():
        st = h.load(run)
        if st["lost"] or st["complete"]:
            continue
        if not st["prepared"]:
            h.prep(run, "R1")
        if dry:
            continue
        for step, toks, failed in detect_finished(run, st, idx):
            if failed:
                retry(run, step, "worker returned without its output file")
                continue
            h.ingest(run, step)
            if toks is not None:
                s2 = h.load(run)
                s2["log"][step]["output_tokens"] = toks
                h.save(run, s2)
            rec = h.load(run)["log"][step]
            print(f"[{run}] {step} done: verdict={rec.get('verdict')} blocking_ids={rec.get('blocking_ids')} out_exists={rec['output_exists']}")
        progress = True
        while progress:
            progress = False
            st = h.load(run)
            if st["lost"]:
                break
            for step in h.STEPS:
                if step in st["done"] and step not in st["transitioned"]:
                    r = transition(run, step)
                    if r is True:
                        s2 = h.load(run)
                        if step not in s2["transitioned"]:
                            s2["transitioned"].append(step)
                        h.save(run, s2)
                    progress = True
                    break
    running, pending, all_done = 0, [], True
    for run in h.all_runs():
        st = h.load(run)
        if st["lost"] or st["complete"]:
            continue
        all_done = False
        running += sum(1 for s in st["launched"] if s not in st["done"])
        for s in h.STEPS:
            if s in st["prepared"] and s not in st["launched"] and s not in st["done"]:
                pending.append((run, s))
    for run, s in pending[:max(0, h.MAX_CONCURRENT - running)]:
        print(f"LAUNCH {h.run_dir(run) / ('PROMPT-' + s + '.md')} model=sonnet")
        if not dry:
            s2 = h.load(run)
            s2["launched"][s] = h.now()
            h.save(run, s2)
            running += 1
    if running:
        print(f"RUNNING {running}")
    if all_done and h.all_runs():
        print("ALL DONE")


if __name__ == "__main__":
    main()
