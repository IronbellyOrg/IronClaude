#!/usr/bin/env python3
"""Detect finished workers, ingest, run the A/B 3 state machine and print the prompts that still need an Agent launch.

  advance.py             marks every printed prompt as launched (use only when you really launch them)
  advance.py --dry-run   writes the prompt files, prints WOULD-LAUNCH lines, marks nothing launched

Output lines: LAUNCH <absolute path> model=<sonnet|haiku> | RUNNING n | MANUAL <run> <step> <reason> | WARN ... | ALL DONE
Nothing here stops, skips or truncates work because of token or dollar cost (owner decision D6); the only caps are
the review/fix-cycle ceilings and the stall rule of the design.
"""
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h  # noqa: E402

QUIET_SECONDS = 180      # no transcript found: output unchanged this long means finished
STALE_MINUTES = 60
ORDER = {s: i for i, s in enumerate(h.STEPS)}


def _iso_age_minutes(iso):
    import datetime
    t = datetime.datetime.fromisoformat(iso)
    return (datetime.datetime.now(datetime.timezone.utc) - t).total_seconds() / 60


def _out_path(run, step):
    base = h.out_base(run, step)
    return base / (h.AUD_OUT if step in ("AUD", "AUD2") else h.OUT[step])


def _since(cands, launched_iso):
    """Drop transcripts that started before this launch (an earlier attempt of the same step)."""
    import datetime
    if not launched_iso:
        return cands
    lim = datetime.datetime.fromisoformat(launched_iso) - datetime.timedelta(seconds=90)
    keep = []
    for c in cands or []:
        s = c.get("start")
        try:
            ts = datetime.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None
        except Exception:
            ts = None
        if ts is None or ts >= lim:
            keep.append(c)
    return keep


def finished(run, step, transcripts, out, launched_iso=None):
    """-> ('done'|'running'|'missing', tokens).  Rule 6: output exists AND (transcript DONE, or no transcript and quiet 180 s)."""
    cands = _since(transcripts.get((run, step)), launched_iso)
    c = h.pick(cands, h.expected_model(run, step), f"{run} {step}") if cands else None
    if c is not None and c["done"] and not out.exists():
        return "missing", c["tokens"]
    if not out.exists():
        return "running", None
    if c is not None:
        return ("done" if c["done"] else "running"), c["tokens"]
    if time.time() - out.stat().st_mtime >= QUIET_SECONDS:
        return "done", None
    return "running", None


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    dry = "--dry-run" in argv
    transcripts = h.scan_transcripts("p12/ab3/runs", h.run_re_ab())
    runs = h.all_runs()
    # 1. ingest finished workers --------------------------------------------------------------
    for run in runs:
        for step in list(h.load(run)["launched"]):
            st = h.load(run)
            if st.get("lost") or step in st["done"] or step not in st["launched"]:
                continue
            status, toks = finished(run, step, transcripts, _out_path(run, step), st["launched"][step])
            if status == "missing":
                st["retries"] = st.get("retries", {})
                st["retries"][step] = st["retries"].get(step, 0) + 1
                st["launched"].pop(step)
                if st["retries"][step] > 1:
                    st["lost"] = True
                    print(f"MANUAL {run} {step} worker returned without output twice: run marked lost")
                else:
                    st["manual"].append({"step": step, "reason": "no output; relaunch once", "at": h.now()})
                    print(f"MANUAL {run} {step} worker returned without output: unlaunched, relaunch once")
                h.save(run, st)
                continue
            if status != "done":
                age = _iso_age_minutes(st["launched"][step])
                if age > STALE_MINUTES and not _out_path(run, step).exists():
                    print(f"WARN stale {run} {step}")
                continue
            rec = h.ingest(run, step)
            st = h.load(run)
            if toks is not None:
                st["log"][step]["output_tokens"] = toks
                h.save(run, st)
            print(f"[{run}] {step} done: verdict={rec.get('verdict')} blocking={[(b['id'], b['theme']) for b in rec.get('blocking', [])]} "
                  f"out_exists={rec['output_exists']}")
    # 2. state machine ---------------------------------------------------------------------------
    for run in runs:
        st = h.load(run)
        if st.get("lost"):
            continue
        p = h.plan(run)
        if p["manual"]:
            kind = p.get("kind")
            last = p.get("at") or _last_review(st)
            if kind == "verdict":
                st.setdefault("retries", {})
                n = st["retries"].get(last, 0)
                if n >= 1:
                    st["lost"] = True
                    print(f"MANUAL {run} {last} {p['manual']} again after one relaunch: run marked lost")
                else:
                    st["retries"][last] = n + 1
                    st["manual"].append({"step": last, "reason": p["manual"] + "; relaunch once", "at": h.now()})
                    st["done"].remove(last); st["log"].pop(last, None); st["launched"].pop(last, None)
                    old = _out_path(run, last)
                    if old.exists():
                        old.rename(old.with_name(old.name + f".attempt{n + 1}"))
                    print(f"MANUAL {run} {last} {p['manual']}: unlaunched, relaunch once")
                h.save(run, st)
            else:
                print(f"MANUAL {run} {last} {p['manual']}: read the report's Reviser brief, then `harness.py setids {run} {last} \"F1, F2\"`")
            continue
        if "G" in st["done"] and st.get("stall") is None and st["log"]["G"].get("verdict") == "FAIL":
            st["stall"] = h.stall_check(run)
        if p["loop_end"] and st.get("loop_end") != p["loop_end"]:
            st["loop_end"] = p["loop_end"]
        h.save(run, st)
    # 3. launch list -----------------------------------------------------------------------------
    running = 0
    for run in runs:
        st = h.load(run)
        if st.get("lost"):
            continue
        running += sum(1 for s in st["launched"] if s not in st["done"])
    slots = max(0, h.MAX_CONCURRENT - running)
    cand = []
    for run in runs:
        st = h.load(run)
        if st.get("lost"):
            continue
        p = h.plan(run)
        for step in p["next"]:
            if step in st["launched"] and step not in st["done"]:
                continue
            if step in st["done"]:
                continue
            cand.append((h.run_key(run), ORDER[step], run, step))
    cand.sort()
    printed = 0
    for _, _, run, step in cand[:slots]:
        model = h.model_for(run, step)
        if step in ("AUD", "AUD2"):
            assert model == "sonnet", "Haiku never audits"
        path = h.prep(run, step)
        if dry:
            print(f"WOULD-LAUNCH {path} model={model}")
        else:
            st = h.load(run)
            st["launched"][step] = h.now()
            h.save(run, st)
            print(f"LAUNCH {path} model={model}")
        printed += 1
    running_after = running + (0 if dry else printed)
    complete = all(h.load(r).get("lost") or h.plan(r)["complete"] for r in runs) if runs else False
    if complete and running_after == 0 and not cand:
        print("ALL DONE")
    else:
        print(f"RUNNING {running_after}")
    return 0


def _last_review(st):
    for s in ("GR", "G", "R3", "R2", "R1"):
        if s in st["done"]:
            return s
    return "R1"


if __name__ == "__main__":
    sys.exit(main())
