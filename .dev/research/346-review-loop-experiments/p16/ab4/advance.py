#!/usr/bin/env python3
"""ab4 state machine (k=2 first reviews, lint pre-pass). Detect finished workers, ingest, prep the next steps, print the prompts that need a launch.

  advance.py [--dry-run]
Prints: LAUNCH <abs path> model=<sonnet|haiku> | RUNNING n | MANUAL ... | WARN ... | LOST ... | ALL DONE.
--dry-run writes the first prompts and prints them; it marks nothing launched and ingests nothing.
No rule here stops, truncates or skips anything because of token cost (owner decision D6); the only stops are
the stall/relaunch rules (a worker that returns without output is relaunched once, then the run is lost)."""
import datetime
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h  # noqa: E402
import score_themes as sc  # noqa: E402


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


def safe_prep(run, step):
    """prep that turns a contaminated finding list (ValueError) into a MANUAL stop for this run instead of a crash."""
    try:
        h.prep(run, step)
        return True
    except ValueError as exc:
        print(f"MANUAL {run} {step} not prepared: {exc}")
        return False


def transition(run, step):
    """-> True when handled, False when blocked (MANUAL), 'retry' when the step was unlaunched."""
    st = h.load(run)
    rec = st["log"][step]
    if not rec["output_exists"]:
        return retry(run, step, "no output file")
    if step in h.R1S or step in ("R2", "R3") or step in ("AUD", "AUD2"):
        v = rec.get("verdict")
        if v in ("INCOMPLETE", "NONE"):
            return retry(run, step, f"verdict {v}")
    if step in h.R1S:
        if rec["verdict"] == "FAIL" and not h.step_ids(run, step):
            print(f"MANUAL {run} {step} no blocking ids parsed")
            return False
        st = h.load(run)
        ready = set(st["transitioned"]) | {step}
        if all(s in ready for s in h.R1S):
            if not st["merge"].get("done"):
                mids = h.merge(run)
                if not mids:
                    finish_loop(run, "PASS")
                    return True
            st = h.load(run)
            if st["loop_end"] is None and "VF1" not in st["prepared"]:     # also retried after a MANUAL stop
                return safe_prep(run, "VF1")
        return True
    if step.startswith("VF"):
        n = int(step[2])
        confirmed = rec["confirmed"]
        if not confirmed:
            finish_loop(run, "VERIFIED-PASS")
        elif n == 3:
            finish_loop(run, "ESCALATED")
        else:
            h.prep(run, f"V{n}")
        return True
    if step in ("V1", "V2"):
        h.prep(run, "R2" if step == "V1" else "R3")
        return True
    if step in ("R2", "R3"):
        n = int(step[1])
        if rec["verdict"] == "PASS":
            finish_loop(run, "PASS")
            return True
        if not h.step_ids(run, step):
            print(f"MANUAL {run} {step} no blocking ids parsed")
            return False
        return safe_prep(run, f"VF{n}")
    if step in ("AUD", "AUD2"):
        st = h.load(run)
        if all(s in st["done"] or s == step for s in ("AUD", "AUD2")):
            st["complete"] = True
            h.save(run, st)
        return True
    raise ValueError(step)


def detect_finished(run, st, idx):
    """Steps launched and not yet ingested whose worker has finished -> list of (step, tokens, failed)."""
    out = []
    for step, when in list(st["launched"].items()):
        if step in st["done"]:
            continue
        outp = h.out_path(run, step)
        cands = idx.get((run, step))
        best = h.pick(cands, h.expected_model(st, step), f"{run} {step}") if cands else None
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
    idx = {} if dry else h.scan_by_prompt()
    for run in h.all_runs():
        st = h.load(run)
        if st["lost"] or st["complete"]:
            continue
        if not st["prepared"]:
            for s in h.R1S:
                h.prep(run, s)
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
        # transitions for every ingested, not yet transitioned step (also picks up steps unblocked by `setids`)
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
                    if r == "retry":
                        progress = True
                        break
                    # blocked (MANUAL): look at the other steps
    # launch phase
    running = 0
    pending = []
    all_done = True
    for run in h.all_runs():
        st = h.load(run)
        if st["lost"] or st["complete"]:
            continue
        all_done = False
        running += sum(1 for s in st["launched"] if s not in st["done"])
        for s in h.STEPS:
            if s in st["prepared"] and s not in st["launched"] and s not in st["done"]:
                pending.append((run, s, st))
    slots = max(0, h.MAX_CONCURRENT - running)
    for run, s, st in pending[:slots]:
        model = h.expected_model(st, s)
        assert not (s in ("AUD", "AUD2") and model != "sonnet"), "Haiku never audits"
        print(f"LAUNCH {h.run_dir(run) / ('PROMPT-' + s + '.md')} model={model}")
        if not dry:
            s2 = h.load(run)
            s2["launched"][s] = h.now()
            h.save(run, s2)
            with open(h.AB / "launch-ledger.jsonl", "a") as f:        # telemetry record: stratum + model on every launch
                f.write(json.dumps({"t": h.now(), "run": run, "step": s, "stratum": st["stratum"], "model": model}) + "\n")
            running += 1
    if running:
        print(f"RUNNING {running}")
    if all_done and h.all_runs():
        print("ALL DONE")


if __name__ == "__main__":
    main()
