"""Build baseline-metrics.json for S4 (DECISIONS.md D5: M1 to M5 per round) from evidence tables plus read-off finding counts.

Inputs (all inside the S4 folder):
  evidence/m4-sizes.tsv      tools/reconstruct.py checkpoints: file, time, bytes, newline_count, sha16
  evidence/agent-costs.tsv   tools/agent_costs.py output
  the main session log (read-only) for orchestrator tool calls / tokens per round window
Finding counts (M2/M3) are typed in below, each with the file and line it was read from ("read") or marked "derived".
Usage: uv run --no-project python -I build_metrics.py <S4 folder>
"""
import json
import os
import sys
from collections import defaultdict

S4 = sys.argv[1]
MAIN = "/home/coder/.claude/projects/-home-coder-workspaces-worktrees-Coder-bmad-ponytail-global/189f8649-3921-4435-bc6b-a15182a20399.jsonl"
Q = "qa/"  # baseline outputs: S4/evidence/baseline-qa-outputs/

# ---- M4 -------------------------------------------------------------------------------------------------
sizes = defaultdict(dict)  # file -> time -> (bytes, lines)
for line in open(os.path.join(S4, "evidence/m4-sizes.tsv"), encoding="utf-8"):
    f, t, b, n, _ = line.rstrip("\n").split("\t")
    sizes[f][t] = (int(b), int(n))


def docset(files, t):
    return (sum(sizes[f][t][0] for f in files), sum(sizes[f][t][1] for f in files))


R5 = [f"research/{n}.md" for n in ("01-bmad-6-9-0-installer-and-skill-runtime", "02-image-cli-and-catalogue-slug", "03-startup-flow-home-and-user-level-claude", "04-pinned-tests-57-46-19", "05-startup-boot-test-docs-and-decision-trail")]
SY = [f"synthesis/{n}.md" for n in ("synth-01-problem-current-state", "synth-02-target-gaps-external", "synth-03-options-recommendation", "synth-04-plan-questions-evidence")]
RP = ["RESEARCH-REPORT-bmad-first-use.md"]
M4_POINTS = {  # gate -> (files, [(round label, checkpoint time)], end checkpoint)
    "G1": (R5, [("R1", "15:52:20"), ("R2", "16:19:11"), ("R3", "16:37:47")], "18:11:58"),
    "G2": (SY, [("R1", "18:11:58"), ("R2", "18:36:18"), ("R3", "18:45:35")], "19:00:30"),
    "G3": (RP, [("R1", "19:00:30"), ("R2", "19:41:35"), ("R3", "19:55:43")], "20:15:23"),
    "G4": (RP, [("R1", "20:15:23"), ("R2", "20:34:47")], "20:37:58"),
    "G5": (RP, [("R1", "20:37:58"), ("R2", "21:13:42"), ("R3", "21:23:22")], "23:59:59"),
}


def m4(gate):
    files, pts, end = M4_POINTS[gate]
    b0, l0 = docset(files, pts[0][1])
    out = {}
    for lab, t in pts:
        b, n = docset(files, t)
        out[lab] = {"state_reviewed_at_utc": t, "bytes": b, "lines": n}
    b, n = docset(files, end)
    out["end_of_gate"] = {"checkpoint_utc": end, "bytes": b, "lines": n, "note": "state when the next stage started (gate 5: final file); includes the manual exception edits"}
    out["growth_over_gate"] = {"bytes_pct": round(100.0 * (b - b0) / b0, 2), "lines_pct": round(100.0 * (n - l0) / l0, 2)}
    return out


# ---- M5 -------------------------------------------------------------------------------------------------
cost_rows = []
for line in list(open(os.path.join(S4, "evidence/agent-costs.tsv"), encoding="utf-8"))[1:]:
    p = line.rstrip("\n").split("\t")
    cost_rows.append({"stage": p[0].split("_L")[0], "L": int(p[1]), "tool_calls": int(p[3]), "msgs": int(p[4]), "in": int(p[5]), "cc": int(p[6]), "cr": int(p[7]), "out": int(p[8]), "first": p[9], "last": p[10]})


def round_of(stage):
    parts = stage.split("-")
    return parts[0], parts[1]  # gate, R1/C1/F1/R2/F2/R3


agg = defaultdict(lambda: {"agents": 0, "tool_calls": 0, "out_tokens": 0, "fresh_input_tokens": 0, "cache_read_tokens": 0, "first": "99", "last": "00"})
for r in cost_rows:
    if not r["stage"].startswith("G"):
        continue
    g, rd = round_of(r["stage"])
    if rd not in ("R1", "C1", "F1", "R2", "F2", "R3"):
        continue
    a = agg[(g, rd)]
    a["agents"] += 1
    a["tool_calls"] += r["tool_calls"]
    a["out_tokens"] += r["out"]
    a["fresh_input_tokens"] += r["in"] + r["cc"]
    a["cache_read_tokens"] += r["cr"]
    a["first"] = min(a["first"], r["first"])
    a["last"] = max(a["last"], r["last"])


def secs(a, b):
    h1, m1, s1 = map(int, a.split(":"))
    h2, m2, s2 = map(int, b.split(":"))
    return (h2 * 3600 + m2 * 60 + s2) - (h1 * 3600 + m1 * 60 + s1)


# orchestrator (main session) per window
HALT = {"G1": "16:47:59", "G2": "18:49:40", "G3": "20:01:40", "G4": "20:37:58", "G5": "21:31:53"}
orch_msgs = {}
orch_tools = []
with open(MAIN, encoding="utf-8") as fh:
    for line in fh:
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("type") != "assistant" or not o.get("timestamp"):
            continue
        t = o["timestamp"][11:19]
        msg = o.get("message") or {}
        for c in msg.get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use":
                orch_tools.append((c["id"], t))
        u, mid = msg.get("usage"), msg.get("id")
        if u and mid:
            prev = orch_msgs.get(mid, ("", 0, 0, 0, 0))
            orch_msgs[mid] = (t, max(prev[1], u.get("output_tokens", 0)), max(prev[2], u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)), max(prev[3], u.get("cache_read_input_tokens", 0)), 0)
tool_ids = {}
for i, t in orch_tools:
    tool_ids.setdefault(i, t)


def orch(a, b):
    tc = sum(1 for t in tool_ids.values() if a <= t < b)
    ms = [v for v in orch_msgs.values() if a <= v[0] < b]
    return {"tool_calls": tc, "out_tokens": sum(v[1] for v in ms), "fresh_input_tokens": sum(v[2] for v in ms), "cache_read_tokens": sum(v[3] for v in ms)}


def m5(gate):
    rounds = [r for r in ("R1", "C1", "F1", "R2", "F2", "R3") if (gate, r) in agg]
    starts = {}
    for r in ("R1", "F1", "R2", "F2", "R3"):
        if (gate, r) in agg:
            starts[r] = agg[(gate, r)]["first"]
    order = [r for r in ("R1", "F1", "R2", "F2", "R3") if r in starts]
    out = {}
    for r in rounds:
        a = agg[(gate, r)]
        out[r] = {"agents": a["agents"], "agent_tool_calls": a["tool_calls"], "agent_out_tokens": a["out_tokens"], "agent_fresh_input_tokens": a["fresh_input_tokens"], "agent_cache_read_tokens": a["cache_read_tokens"], "agent_wall_secs_first_spawn_to_last_end": secs(a["first"], a["last"])}
    for i, r in enumerate(order):
        end = starts[order[i + 1]] if i + 1 < len(order) else HALT[gate]
        out[r]["orchestrator_window_utc"] = [starts[r], end]
        out[r]["orchestrator"] = orch(starts[r], end)
    return out


# ---- M2 / M3 (read off the baseline outputs; every row names the file) -------------------------------------
def rd(g, tag, verdict, reporters, blocking, ids, **kw):
    d = {"verdict": verdict, "reporters": reporters, "blocking_consolidated": blocking, "blocking_ids": ids}
    d.update(kw)
    return d


GATES = {
    "G1": {
        "name": "Gate 1 research completeness (Phase 3)", "documents": "research/01..05 (+ research-notes.md)", "reviews_run": 3,
        "rounds": {
            "R1": rd("G1", "R1", "FAIL", {"rf-analyst completeness": "C0 I2 m8", "rf-qa evidence": "C0 I5 m4", "rf-qa-qualitative depth": "C0 I5 m2"}, 9, ["consolidated rows 1-9"],
                     raw_important_sum=12, total_findings_after_dedupe=18, severity_downgrades=0,
                     m3={"caused_by_previous_fix": 0, "of": 9, "basis": "first review, nothing to be caused by"},
                     src="qa/qa-gate1-decision.md L11-L16; qa/qa-consolidated-findings-phase3.md L1 (BLOCKING_COUNT: 9)"),
            "R2": rd("G1", "R2", "FAIL", {"rf-qa structural verification": "C0 I2 m3", "rf-qa-qualitative verification": "C0 I4 m8"}, 6, ["F1-a", "F1-b", "F4-a", "X-1", "N1", "N2"],
                     fixes_confirmed_of_prev_round="9 of 9",
                     m3={"caused_by_previous_fix": 6, "of": 6, "introduced": 5, "exposed": 1, "basis": "reviewer text: X-1 'finding 2 passes but introduced X-1' (qa-gate1-decision.md L19); F1-b, F4-a, N1, N2 sit in the fix-written addenda of files 05/03 (qa-consolidated-findings-phase3-cycle2.md rows 2,3,5,6); F1-a is an old line that the new addendum contradicts (my reading). Coordinator also states '6 new blocking issues, all in text the fix agent wrote' (BM L1093)", "source_type": "reviewer tag for X-1; analyst re-derivation for the other five; coordinator statement for all six"},
                     src="qa/qa-gate1-decision.md L18-L19, L23-L30; qa/qa-consolidated-findings-phase3-cycle2.md L1"),
            "R3": rd("G1", "R3", "FAIL (content) / PASS (structural)", {"rf-qa structural verification": "C0 I0 m3", "rf-qa-qualitative verification": "C0 I1 m7"}, 1, ["New-1"],
                     fixes_confirmed_of_prev_round="5 of 6 resolved, finding 5 partly",
                     m3={"caused_by_previous_fix": 1, "of": 1, "residual": 1, "basis": "reviewer text: 'PARTLY RESOLVED, one residual contradiction (see New-1)' (qa-verification-phase3-cycle2-content.md L34)", "source_type": "reviewer tag"},
                     src="qa/qa-gate1-decision.md L36-L40; qa/qa-verification-phase3-cycle2-content.md L34, L55")},
        "ended": "HALT at review 3; user-accepted exception (ask msg_acc5015c9601, BM L1247); executor edited lines 376 and 408 of research/05 itself, no 4th review (qa-gate1-decision.md L42-L48)"},
    "G2": {
        "name": "Gate 2 synthesis quality (Phase 5)", "documents": "synthesis/synth-01..04", "reviews_run": 3,
        "rounds": {
            "R1": rd("G2", "R1", "FAIL", {"rf-analyst accuracy": "C0 I0 m8 (PASS)", "rf-qa structure": "C0 I4 m11", "rf-qa-qualitative coherence": "C0 I5 m10"}, 8, ["consolidated rows 1-8"],
                     raw_important_sum=9, total_findings_after_dedupe=31, severity_downgrades=0, severity_upgrades=1,
                     m3={"caused_by_previous_fix": 0, "of": 8, "basis": "first review"},
                     src="qa/qa-gate2-decision.md L13-L16; qa/qa-consolidated-findings-phase5.md L1"),
            "R2": rd("G2", "R2", "FAIL (content) / PASS (structural)", {"rf-qa structural verification": "C0 I0 m4", "rf-qa-qualitative verification": "C0 I3 m2"}, 3, ["N-1", "N-2", "N-3"],
                     fixes_confirmed_of_prev_round="7 of 8 resolved, finding 6 partly",
                     m3={"caused_by_previous_fix": 3, "of": 3, "introduced": 1, "residual": 2, "basis": "reviewer text: 'finding 6 ... PARTLY RESOLVED, see N-1, N-2, N-3' (qa-verification-phase5-cycle1-content.md L21); N-3 is a contradiction the fix text created (L33); N-1/N-2 are places the fix did not reach", "source_type": "reviewer tag"},
                     src="qa/qa-gate2-decision.md L18-L19, L23-L27; qa/qa-consolidated-findings-phase5-cycle2.md L1"),
            "R3": rd("G2", "R3", "FAIL (content) / PASS (structural)", {"rf-qa structural verification": "C0 I0 m3", "rf-qa-qualitative verification": "C0 I2 m4"}, 2, ["V-1", "V-2"],
                     fixes_confirmed_of_prev_round="N-1..N-3 fixed",
                     m3={"caused_by_previous_fix": 2, "of": 2, "introduced": 1, "residual": 1, "basis": "V-1: 'the cycle-1 contradiction (N-3) was removed by redefining Stage 0, not by evidence' (qa-verification-phase5-cycle2-content.md L32 and L21); V-2: 'same defect class as finding 2' (heading L36); my reading of both", "source_type": "analyst re-derivation from reviewer text"},
                     src="qa/qa-gate2-decision.md L33-L40")},
        "ended": "HALT at review 3; second user-accepted exception (ask at BM L2377); executor made the V-1/V-2 edits in synth-02/03/04 itself, no 4th review (qa-gate2-decision.md L42-L48)"},
    "G3": {
        "name": "Gate 3 report validation, 7 lenses (Phase 6)", "documents": "RESEARCH-REPORT-bmad-first-use.md", "reviews_run": 3,
        "rounds": {
            "R1": rd("G3", "R1", "FAIL", {"template-conformance": "C0 I2 m12", "internal-consistency": "C0 I4 m16", "evidence-quality": "C0 I1 m7", "actionability": "C0 I8 m5", "domain-accuracy": "C0 I1 m10", "crossref-chain": "C0 I9 m10", "finding-reproducibility": "C0 I2 m8"}, 18, ["consolidated rows (69 rows, 18 blocking)"],
                     raw_important_sum=27, total_findings_after_dedupe=69, severity_downgrades=5, note_downgrades="consolidator downgraded 7, orchestrator reversed 2 (TC#1, TC#2)",
                     m3={"caused_by_previous_fix": 0, "of": 18, "basis": "first review"},
                     src="qa/qa-gate3-decision.md L5-L15, L21-L28; qa/qa-consolidated-findings-phase6.md L1"),
            "R2": rd("G3", "R2", "FAIL", {"rf-qa structural verification": "C0 I1 m5", "rf-qa-qualitative verification": "C0 I4 m3"}, 5, ["F-1", "B-1", "B-2", "B-3", "B-4"],
                     fixes_confirmed_of_prev_round="17 of 18 (structural), 18 of 18 in substance (qualitative)",
                     m3={"caused_by_previous_fix": 5, "of": 5, "introduced": 1, "exposed": 3, "residual": 1, "basis": "reviewer text: 'New defects the fixes caused or exposed are in Part B' (qa-fix-verification-qualitative-phase6-cycle1.md L14); B-1 'exposed by the row 8 fix' (L39), B-2 'the row 16 fix records...' (L47), B-3/B-4 'what the re-rating exposed' (L21); F-1 'unfixed part of consolidated row 4' (qa-fix-verification-phase6-cycle1.md L60)", "source_type": "reviewer tags"},
                     src="qa/qa-gate3-decision.md L30-L31, L35-L41; qa/qa-consolidated-findings-phase6-cycle2.md L1"),
            "R3": rd("G3", "R3", "FAIL (qualitative) / PASS (structural)", {"rf-qa structural verification": "C0 I0 m7", "rf-qa-qualitative verification": "C0 I2 m5"}, 2, ["N-1", "N-2"],
                     fixes_confirmed_of_prev_round="rows 1, 2, 4 resolved; rows 3 and 5 only at the places the fix log named",
                     m3={"caused_by_previous_fix": 2, "of": 2, "residual": 2, "basis": "reviewer text: row 3 'PARTLY RESOLVED (residual N-2)', row 5 'PARTLY RESOLVED (residual N-1a, N-1b)' (qa-fix-verification-qualitative-phase6-cycle2.md L17, L19)", "source_type": "reviewer tags"},
                     src="qa/qa-gate3-decision.md L47-L54")},
        "ended": "HALT at review 3; third user-accepted exception (ask at BM L3462); executor made the N-1/N-2 edits itself (12 Edit calls in the main session at 20:14 UTC), no 4th review (qa-gate3-decision.md L58-L62)"},
    "G4": {
        "name": "Gate 4 source-document fidelity (Phase 6)", "documents": "RESEARCH-REPORT-bmad-first-use.md", "reviews_run": 2,
        "rounds": {
            "R1": rd("G4", "R1", "FAIL", {"fidelity agent 1": "C0 I0 m5 (PASS)", "fidelity agent 2": "C0 I0 m10 (PASS)", "fidelity agent 3 (+web check)": "C0 I1 m4"}, 1, ["row 16"],
                     raw_important_sum=1, total_findings_after_dedupe=20, severity_downgrades=0,
                     m3={"caused_by_previous_fix": 0, "of": 1, "basis": "first review"}, src="qa/qa-gate4-decision.md L13-L16"),
            "R2": rd("G4", "R2", "PASS", {"rf-qa structural verification": "C0 I0 m0", "rf-qa-qualitative verification": "C0 I0 m4"}, 0, [],
                     m3={"caused_by_previous_fix": 0, "of": 0, "basis": "no blocking finding"}, src="qa/qa-gate4-decision.md L18-L23")},
        "ended": "clean PASS at review 2 (GATE4_FINAL: PASS, 1 review cycle)"},
    "G5": {
        "name": "Gate 5 anti-omission (Phase 6)", "documents": "RESEARCH-REPORT-bmad-first-use.md (checked against research + synthesis files)", "reviews_run": 3,
        "rounds": {
            "R1": rd("G5", "R1", "FAIL", {"anti-omission slice 1 (task line 447)": "C0 I2 m21", "anti-omission 2 (line 449)": "C0 I0 m35 (PASS)", "anti-omission 3 (line 451)": "C0 I4 m27"}, 4, ["O-5", "O-8a", "OM-1", "OM-2"],
                     raw_important_sum=6, total_findings_after_dedupe=95, severity_downgrades=2, note_downgrades="OM-3 and OM-4 Important to Minor",
                     m3={"caused_by_previous_fix": 0, "of": 4, "basis": "first review"}, src="qa/qa-gate5-decision.md L5-L18"),
            "R2": rd("G5", "R2", "FAIL", {"rf-qa structural verification": "C0 I1 m3", "rf-qa-qualitative content verification": "C0 I3 m7"}, 3, ["I-1", "I-2", "I-3"],
                     fixes_confirmed_of_prev_round="4 of 4 recoveries present",
                     m3={"caused_by_previous_fix": 3, "of": 3, "introduced": 2, "residual": 1, "basis": "I-1: the fixture the fix added makes step 5.3 fail on its own fixture; I-2: fix log says 'qualified everywhere', three places remain (consolidated cycle2 row 2); I-3: the row-66 recovery text written by the fix is an unlabelled inference (row 3); my reading of the consolidated rows", "source_type": "analyst re-derivation"},
                     src="qa/qa-gate5-decision.md L20-L21, L25-L29; qa/qa-anti-omission-consolidated-findings-cycle2.md L1"),
            "R3": rd("G5", "R3", "FAIL (content) / PASS (structural)", {"structural verification": "C0 I0 m1", "content verification": "C0 I1 m2"}, 1, ["N-1"],
                     fixes_confirmed_of_prev_round="I-1, I-2, I-3 fixed",
                     m3={"caused_by_previous_fix": 1, "of": 1, "introduced": 1, "basis": "N-1: the cycle-2 fix text 'assert the same creation as in (a)' makes the skill count N+1 in the new fixture (qa-gate5-decision.md L41); my reading", "source_type": "analyst re-derivation"},
                     src="qa/qa-gate5-decision.md L35-L41")},
        "ended": "HALT at review 3; user-accepted exception (Gate 5 only; ask message msg_8c3d61e635e2, BM L4513); executor made one edit (report L1542) itself, no 4th review (qa-gate5-decision.md L45-L49)"},
}

out = {
    "scenario": "S4", "incident": "I4", "baseline": "ORIGINAL recorded run 2026-11-07 (session 189f8649-3921-4435-bc6b-a15182a20399, BM), not a re-run",
    "definitions": "DECISIONS.md D5: M1 reviews until clean pass; M2 blocking-grade (CRITICAL/IMPORTANT) findings per round; M3 share caused by previous round's fix; M4 document bytes/lines; M5 tool calls and tokens per round",
    "conventions": {
        "round": "a 'round' is one review: R1 = the first independent review, R2 = the verification after fix cycle 1, R3 = the verification after fix cycle 2 (the task file calls R2 and R3 'verification rounds'); F1/F2 = the single fix agent of cycle 1/2; C1 = the consolidation step",
        "blocking": "task file line 130 and 214: only CRITICAL/IMPORTANT fail a gate; MINOR findings are notes and are never rechecked. Same rule in every round",
        "lines": "number of newline characters; files without a final newline are one lower than editor-style line counts (the Gate 1 analyst quotes 365/381/237/268/292 for files that have 364/380/236/267/291)",
        "tokens": "from assistant-message usage in the logs, each message id counted once; fresh_input = input + cache_creation; cache_read reported separately",
        "provenance": "every number carries a 'src' (file and line of the baseline output it was read from) or is marked derived/re-derived",
        "provenance_by_metric": {
            "M1": "READ FROM EVIDENCE: verdicts and review counts from the gate decision files (qa-gate<N>-decision.md); reviews_to_clean_pass is null where no clean pass happened",
            "M2": "READ FROM EVIDENCE: reporters' counts (C/I/m) and BLOCKING_COUNT first lines. DERIVED by me: raw_important_sum (sum of the reporters' Important counts)",
            "M3": "per round, see m3.source_type: 'reviewer tag' = the reviewer's own text names the origin; 'analyst re-derivation' = my reading of the finding text and the consolidated tables (11 of the 23 findings of R2 and R3)",
            "M4": "RE-DERIVED by me: no copy of the document at each round was stored; sizes come from replaying every logged Write/Edit/heredoc (tools/reconstruct.py, evidence/m4-sizes.tsv). The Gate 3 end state equals the stored file-history copy byte for byte; the sizes of the other gate-start states are replay-only (see REPLAY.md section 7)",
            "M5": "RE-DERIVED by me from the agent logs (tools/agent_costs.py, evidence/agent-costs.tsv); the orchestrator window numbers are approximations by time window",
        },
        "agents": "'agents' counts every agent of the round, including the 6 gap researchers (rf-task-researcher) that the Gate 1 fix agent of cycle 1 started itself; they are in evidence/agent-costs.tsv as '-nested-' rows",
        "orchestrator": "the main session's own tool calls and tokens inside the window [first spawn of the round, first spawn of the next round); the last round ends at the HALT question to the user",
    },
    "gates": {},
    "run_level": {
        "gates_run": 5, "gates_passed_clean": 1, "gates_halted_at_cap": 4,
        "gates_halted": ["G1", "G2", "G3", "G5"],
        "m1_note": "M1 (reviews until a clean pass): G4 = 2; G1, G2, G3, G5 = null, no clean pass in 3 reviews (cap), each closed by a user-accepted exception and an unreviewed manual edit",
        "correction_to_phase1": "phase1/REPORT.md lists three gates halted and one exception for Gate 3; the gate decision files show four gates halted (1, 2, 3, 5) and one user exception each, and Gate 4 passed. It also gives report growth as about 1 percent (lines); bytes grew 11.8 percent over Gates 3-5 and the Gate 1 research files grew 67.7 percent in bytes",
        "report_bytes_assembly_to_final": {"start": 364593, "end": 407656, "growth_pct": round(100.0 * (407656 - 364593) / 364593, 2)},
        "wall_clock": "original session 2026-11-07 13:24Z to 22:00Z; gate work 15:52Z to 21:52Z",
    },
}
for g, d in GATES.items():
    gm4, gm5 = m4(g), m5(g)
    rounds = {}
    for r, rv in d["rounds"].items():
        rr = dict(rv)
        rr["m1_review_number"] = int(r[1])
        rr["m4_document"] = gm4.get(r)
        rr["m5"] = gm5.get(r)
        rounds[r] = rr
    out["gates"][g] = {"name": d["name"], "documents": d["documents"], "reviews_run": d["reviews_run"],
                       "m1": {"reviews_to_clean_pass": (2 if g == "G4" else None), "clean_pass_reached": g == "G4", "reason_if_null": None if g == "G4" else "cap of 3 reviews hit with blocking findings open; closed by user exception without a 4th review"},
                       "last_round_blocking": d["rounds"][max(d["rounds"])]["blocking_consolidated"],
                       "rounds": rounds, "m5_fix_and_consolidation": {k: v for k, v in gm5.items() if k in ("C1", "F1", "F2")},
                       "m4_end_and_growth": {"end_of_gate": gm4["end_of_gate"], "growth_over_gate": gm4["growth_over_gate"]}, "ended": d["ended"]}
json.dump(out, open(os.path.join(S4, "baseline-metrics.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("ok", {g: out["gates"][g]["last_round_blocking"] for g in out["gates"]})
