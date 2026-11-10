#!/usr/bin/env python3
"""Detect finished workers, ingest, prep the next steps, print the prompts that still need a launch.
  advance.py [--dry-run]
Prints `LAUNCH <absolute prompt path> model=<sonnet|haiku>` (AUD/AUD2 always sonnet), `RUNNING n`,
`MANUAL <run> <step> <reason>`, `WARN ...` or `ALL DONE`.  At most MAX_CONCURRENT workers run at once (launch ledger in state.json).
--dry-run writes the first prompts (R1 of every run that has not started) and marks nothing.
State machine (plan B6):  R -> PASS: audits | FAIL: VF -> none confirmed: VERIFIED-PASS + audits | confirmed: V -> next R
(VF3 with a confirmed id: ESCALATED + audits).  D6: there is no token or cost check anywhere in this file."""
import contextlib
import io
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h  # noqa: E402

QUIET_SECS = 180
STALE_SECS = 60*60


def is_finished(run, step, st, found):
    outp = h.out_path(run, step)
    if not outp.exists():
        return False
    cands = found.get((run, step))
    c = h.pick_transcript(cands, h.loop_model_of(st, step), key=f"{run} {step}") if cands else None
    if c is not None:
        return c["done"]
    return time.time() - outp.stat().st_mtime >= QUIET_SECS


def queue(run, steps):
    for s in steps:
        h.prep(run, s)
        st = h.load(run)
        if s not in st["pending"]:
            st["pending"].append(s)
        h.save(run, st)


def finish_loop(run, end):
    st = h.load(run); st["loop_end"] = end; h.save(run, st)
    print(f"[{run}] loop_end={end}")
    queue(run, ["AUD", "AUD2"])


def transitions(run, step, rec):
    if step in ("R1", "R2", "R3"):
        v = rec.get("verdict")
        if v == "PASS":
            finish_loop(run, "PASS")
        elif v == "FAIL":
            ids = rec.get("ids") or []
            if ids:
                queue(run, [f"VF{step[1]}"])
            else:
                st = h.load(run); st["awaiting_ids"] = step; h.save(run, st)
                print(f"MANUAL {run} {step} no blocking ids parsed")
        else:
            print(f"MANUAL {run} {step} verdict {v}")
            h.requeue(run, step, f"verdict {v}")
    elif step.startswith("VF"):
        n = int(step[2:]); conf = rec.get("confirmed") or []
        if not rec.get("parse_ok", True):
            print(f"WARN {run} {step} verifier reply not parseable: every finding confirmed (fail closed)")
        if not conf:
            finish_loop(run, "VERIFIED-PASS")
        elif n < 3:
            queue(run, [f"V{n}"])
        else:
            finish_loop(run, "ESCALATED")
    elif step in ("V1", "V2"):
        queue(run, [f"R{int(step[1]) + 1}"])
    elif step in ("AUD", "AUD2"):
        if rec.get("verdict") not in ("PASS", "FAIL"):
            print(f"MANUAL {run} {step} audit verdict {rec.get('verdict')}")
            h.requeue(run, step, f"audit verdict {rec.get('verdict')}")
            return
        st = h.load(run)
        if "AUD" in st["done"] and "AUD2" in st["done"]:
            st["complete"] = True; h.save(run, st)
            print(f"[{run}] COMPLETE loop_end={st['loop_end']}")


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    dry = "--dry-run" in args
    found = h.ab_transcripts()
    runs = h.run_names()
    if dry:
        for run in runs:
            st = h.load(run)
            if st.get("lost") or st.get("complete") or st["launched"] or st["done"] or st["pending"]:
                continue
            p = h.prep(run, "R1")
            print(f"DRYRUN would launch {p} model={h.loop_model_of(st, 'R1')}")
        return 0
    for run in runs:
        st = h.load(run)
        if st.get("lost") or st.get("complete"):
            continue
        for step in [s for s in h.STEPS if s in st["launched"] and s not in st["done"]]:
            st = h.load(run)
            if st.get("lost"):
                break
            if is_finished(run, step, st, found):
                with contextlib.redirect_stdout(io.StringIO()):
                    rec = h.ingest(run, step)
                print(f"[{run}] {step} done: verdict={rec.get('verdict')} ids={rec.get('ids')} confirmed={rec.get('confirmed')} "
                      f"rejected={list((rec.get('rejected') or {}).keys())} spec={rec.get('spec_after', {}).get('bytes')} out_exists={rec['output_exists']}")
                if not rec["output_exists"]:
                    print(f"MANUAL {run} {step} output missing")
                    h.requeue(run, step, "output missing")
                    continue
                transitions(run, step, rec)
            else:
                t0 = st["launched"][step]
                age = time.time() - __import__("datetime").datetime.fromisoformat(t0).timestamp()
                if age > STALE_SECS and not h.out_path(run, step).exists():
                    print(f"WARN stale {run} {step}")
        st = h.load(run)
        if st.get("awaiting_ids") and st["awaiting_ids"] in st.get("manual_ids", {}):
            step = st["awaiting_ids"]; st.pop("awaiting_ids"); h.save(run, st)
            queue(run, [f"VF{step[1]}"])
        st = h.load(run)
        if st.get("awaiting_ids"):
            print(f"MANUAL {run} {st['awaiting_ids']} no blocking ids parsed (use: harness.py setids {run} {st['awaiting_ids']} \"F1, F2\")")
        if not st.get("lost") and not st["launched"] and not st["done"] and not st["pending"] and not st.get("awaiting_ids"):
            queue(run, ["R1"])
    # launch phase: ledger and concurrency
    running = 0
    cand = []
    for i, run in enumerate(runs):
        st = h.load(run)
        if st.get("lost"):
            continue
        running += sum(1 for s in st["launched"] if s not in st["done"])
        for s in st["pending"]:
            cand.append((i, h.STEPS.index(s), run, s))
    cand.sort()
    slots = max(0, h.MAX_CONCURRENT - running)
    for _, _, run, s in cand[:slots]:
        st = h.load(run)
        model = h.loop_model_of(st, s)
        assert not (s.startswith("AUD") and model != "sonnet"), "Haiku never audits"
        print(f"LAUNCH {h.run_dir(run) / ('PROMPT-' + s + '.md')} model={model}")
        st["launched"][s] = h.now_iso(); st["pending"].remove(s); h.save(run, st)
        running += 1
    live = [r for r in runs if not (h.load(r).get("lost") or h.load(r).get("complete"))]
    if not live and running == 0:
        print("ALL DONE")
    else:
        print(f"RUNNING {running}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
