#!/usr/bin/env python3
"""ab5 state machine (PN1 four-reviewer panel as the first review, lint pre-pass, merge, ADJ, cleaned VF, revise, scoped re-reviews).
Copy of $SP/p16/ab4/advance.py, modified where marked "ab5". Detect finished workers, ingest, prep the next steps, print the prompts
that need a launch.

  advance.py [--dry-run] [--variant panel|full]
Prints: LAUNCH <abs path> model=<sonnet|haiku> (the panel launch alias; never a Tier 0 model, OWNER RULE) | RUNNING n | MANUAL ... | WARN ... | LOST ... | ALL DONE.
--dry-run writes the first prompts (PROMPT-R1.<rid>.md + lint-1.md) and prints them; it marks nothing launched and ingests nothing.
Concurrency (ab5): at most MAX_CONCURRENT_RUNS runs (decision.json, 6) have workers in flight; inside a run every prepared step is
launched at once (the four panel reviewers in parallel; ADJ beside VF1; AUD beside AUD2).
No rule here stops, truncates or skips anything because of token cost (owner decision D6); the only stops are
the stall/relaunch rules (a worker that returns without output is relaunched once; then a panel reviewer is lost (two lost reviewers
lose the run, PN1), a lost ADJ is recorded and the run continues, any other step loses the run)."""
import datetime
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h  # noqa: E402
import full  # noqa: E402
import score_themes as sc  # noqa: E402,F401


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
        st = h.load(run)
        if h.is_r1(step) and not st["lost"]:
            print(f"LOST reviewer {run} {step}: {why}; second failure, the panel continues without it ({len(st['r1_lost'])} lost)")
        elif step == "ADJ":
            print(f"LOST ADJ {run}: {why}; second failure, ADJ recorded as lost, the run continues (measurement only)")
        else:
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


def maybe_complete(run):
    st = h.load(run)
    adj_settled = "ADJ" not in st["prepared"] or "ADJ" in st["done"] or st.get("adj_lost")
    if all(s in st["done"] for s in ("AUD", "AUD2")) and adj_settled and not st["complete"]:
        st["complete"] = True
        h.save(run, st)


def after_panel(run):
    """ab5: once every panel reviewer is transitioned or lost: merge (once), then prepare VF1 and ADJ (retried after a MANUAL stop)."""
    st = h.load(run)
    if st["lost"]:
        return
    r1 = h.r1_steps(st)
    if not all(s in st["transitioned"] or s in st["r1_lost"] for s in r1):
        return
    if h.is_full(st):
        return after_panel_full(run)
    if not st["merge"].get("done"):
        mids = h.merge(run)
        if not mids:
            finish_loop(run, "PASS")
            return
    st = h.load(run)
    if st["loop_end"] is None and "VF1" not in st["prepared"]:
        safe_prep(run, "VF1")
    st = h.load(run)
    if st["merge"].get("groups") and "ADJ" not in st["prepared"]:
        safe_prep(run, "ADJ")


def after_panel_full(run):
    """variant full: PN1 rule first (no reviewer's findings block parsed -> relaunch each once), then merge + ledger (M1), ADJ over the
    ledger rows (PN1: whenever M1 exists), VF1 over the brief rows unless M1 says PASS."""
    st = h.load(run)
    used = [s for s in h.r1_steps(st) if s not in st["r1_lost"]]
    if "M1" not in st["log"] and not any(st["log"][s].get("block_ok") for s in used):
        again = [s for s in used if st["relaunch"].get(s, 0) == 0]
        if again:
            for s in again:
                print(f"MANUAL {run} {s}: no panel reviewer's findings block parsed (PN1 rule); relaunching it once")
                h.unlaunch(run, s, quiet=True)
            return
    m = full.merge(run, 1)
    st = h.load(run)
    if len(st["merge"].get("groups") or []) and "ADJ" not in st["prepared"]:
        safe_prep(run, "ADJ")
    st = h.load(run)
    if m["decision"] == "PASS":
        if st["loop_end"] is None:
            finish_loop(run, "PASS")
        return
    if st["loop_end"] is None and "VF1" not in st["prepared"]:
        if h.decision().get("ADJ_GATES_VF1") and "ADJ" in st["prepared"] and "ADJ" not in st["done"] and not st.get("adj_lost"):
            return
        safe_prep(run, "VF1")


def transition(run, step):
    """-> True when handled, False when blocked (MANUAL), 'retry' when the step was unlaunched."""
    st = h.load(run)
    rec = st["log"][step]
    if not rec["output_exists"]:
        return retry(run, step, "no output file")
    if h.is_r1(step) or step in ("R2", "R3") or step in ("AUD", "AUD2"):
        v = rec.get("verdict")
        if v in ("INCOMPLETE", "NONE"):
            return retry(run, step, f"verdict {v}")
    if h.is_full(st) and (h.is_r1(step) or step in ("R2", "R3")):
        full.telemetry_record(run, step)
    if h.is_r1(step):
        if h.is_full(st):
            return True                                   # the ledger merge reads the findings block; ids_from is a recorded cross-check
        if rec["verdict"] == "FAIL" and not h.step_ids(run, step):
            print(f"MANUAL {run} {step} no blocking ids parsed")
            return False
        return True                                       # merge / VF1 / ADJ: after_panel()
    if step == "ADJ":
        maybe_complete(run)
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
        if h.is_full(st):
            full.ledger_revise(run, int(step[1]))        # PN1 `ledger revise` (L<n>) before the re-review
        h.prep(run, "R2" if step == "V1" else "R3")
        return True
    if step in ("R2", "R3") and h.is_full(st):
        n = int(step[1])
        if not rec.get("block_ok") and st["relaunch"].get(step, 0) == 0:
            return retry(run, step, "findings block not parsed (PN1 rule)")
        m = full.merge(run, n)                            # ledger round n; decision PASS / REVISE / ESCALATE
        if m["decision"] == "PASS":
            finish_loop(run, "PASS")
            return True
        return safe_prep(run, f"VF{n}")
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
        maybe_complete(run)
        return True
    raise ValueError(step)


def detect_finished(run, st, idx):
    """Steps launched and not yet ingested whose worker has finished -> list of (step, transcript info or None, failed)."""
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
                out.append((step, best, not exists))
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
    only = argv[argv.index("--variant") + 1] if "--variant" in argv else None      # ab5: restrict to one arm (panel | full)
    runs = [r for r in h.all_runs() if only is None or h.variant_of(h.load(r)) == only]
    if dry:
        print("DRY-RUN (nothing is marked launched, nothing is ingested)")
    idx = {} if dry else h.scan_by_prompt()
    for run in runs:
        st = h.load(run)
        if st["lost"] or st["complete"]:
            continue
        if not st["prepared"]:
            for s in h.r1_steps(st):
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
                s2["log"][step]["output_tokens"] = toks["tokens"]
                s2["log"][step]["observed_model"] = toks["model"]       # ab5 lanes: model from the transcript (telemetry)
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
        after_panel(run)
        maybe_complete(run)
    # launch phase (ab5: run-level slots; every prepared step of an admitted run is launched)
    running = 0
    active = set()
    pending = []
    all_done = True
    for run in runs:
        st = h.load(run)
        if st["lost"] or st["complete"]:
            continue
        all_done = False
        inflight = sum(1 for s in st["launched"] if s not in st["done"])
        running += inflight
        if inflight:
            active.add(run)
        for s in h.STEPS:
            if s in st["prepared"] and s not in st["launched"] and s not in st["done"] and s not in st.get("r1_lost", []):
                if s == "ADJ" and st.get("adj_lost"):
                    continue
                pending.append((run, s, st))
    cap = h.max_runs()
    import os as _os
    agent_cap = int(_os.environ.get("AB_AGENT_CAP") or 0)       # ab5: optional cap on agents in flight (0 = off); keeps launches under the session's 20-agent limit
    for run, s, st in pending:
        if agent_cap and running >= agent_cap:
            continue                                            # stays prepared and unlaunched; the next poll launches it
        if run not in active:
            if len(active) >= cap:
                continue
            active.add(run)
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
    if all_done and runs:
        print("ALL DONE")


if __name__ == "__main__":
    main()
