#!/usr/bin/env python3
"""O1: hand-authored findings-v1 fixtures for the Stage 2 arm-3 reports (a3-r1..a3-r6).

Anchors are the shortest exact spans (12-200 chars) of the reviewed spec version that the report's finding quotes.
Every anchor is verified with findings.locate (loaded from the PN1 clone) and the check is printed.
Prior lines use the report's own ids; replay.py translates them to ledger ids.
"""
import importlib.util, json, pathlib, sys

SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
CLONE = SP / "p13/clones/pn1"
AB = SP / "p13/ab1"
OV = SP / "exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
D = ".dev/orca-command-refactor"

spec = importlib.util.spec_from_file_location("pn1_findings", CLONE / "src/superclaude/cli/review/findings.py")
F = importlib.util.module_from_spec(spec); spec.loader.exec_module(F)

A_AC11 = "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
A_LOAD = "use it as a step inside another worker's brief, not as its own Task"
A_P1 = "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"
A_STEP3 = "its report path is the WC-4 contract path"
A_STEP4 = "step 4 uses the command's existing report file, since the contract arrives in P1"
A_WC4 = "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"
A_TDD = "not a bare topic; `--output <file>` | the TDD at `--output`"
A_WC6 = "writes each run into a fresh output directory so a re-run starts clean"
A_BRIEF = "the output directory, so the report path is known before dispatch (WC-4)"
A_WC2 = "Under `--unattended` the command never calls `AskUserQuestion`"
A_ONLY = "The only command changes are the small fixes in the last column"
A_GREP = "grep -E '^-[^-]'"
A_V2_REUSE = "never reused from an earlier dispatch of the same Task, a `--retry-of` retry included"
A_V2_ROAD = "the explicit resume flag (resume only when passed)"


def f(fid, sev, cat, anchor, refs, claim, anchor2=None, blocking=True):
    d = {"id": fid, "severity": sev, "blocking": blocking, "category": cat, "anchor": anchor}
    if anchor2:
        d["anchor2"] = anchor2
    d["refs"] = refs
    d["claim"] = claim
    return d


def p(pid, status):
    return {"prior": pid, "status": status}


# (run, round) -> (spec version used, [lines])
R1 = {
    "a3-r1": [
        f("F1", "CRITICAL", "unpassable-check", A_STEP3, ["AC-0.4", "WC-4"], "The P0 check demands a contract the same row says does not exist before P1.", A_STEP4),
        f("F2", "CRITICAL", "contradiction", A_AC11, ["AC-1.1", "AC-1.2"], "The load row says no section and no report, but the P1 checks require both for load.", A_LOAD),
    ],
    "a3-r2": [
        f("R1-B1", "CRITICAL", "contradiction", A_P1, ["WC-2", "AC-1.1", "P1"], "P1 puts the flag and section on gated commands that still prompt, so the stall WC-2 forbids is not detected.", A_WC2),
        f("R1-B2", "CRITICAL", "unpassable-check", A_WC4, ["WC-4", "AC-2.2"], "The contract path is undefined for file-valued output flags, so the AC-2.2 contract cannot be located.", A_TDD),
    ],
    "a3-r3": [
        f("F1", "MAJOR", "unpassable-check", A_AC11, ["AC-1.1", "AC-1.2"], "AC-1.1 and AC-1.2 require a report and a section for load, which the spec says gets neither.", A_LOAD),
        f("F2", "MAJOR", "contradiction", A_ONLY, ["AC-1.1"], "Section 3.1 says ready commands change only by their small fix, but P1 adds the flag and a section to all of them.", A_P1),
        f("F3", "MAJOR", "unpassable-check", A_STEP3, ["AC-0.4", "WC-4"], "AC-0.4 step 3 needs a contract that P0 does not have.", A_STEP4),
    ],
    "a3-r4": [
        f("F-01", "CRITICAL", "unpassable-check", A_AC11, ["AC-1.1"], "AC-1.1 cannot pass as written because load and other commands are exempt in their rows.", A_LOAD),
    ],
    "a3-r5": [
        f("F-1", "MAJOR", "contradiction", A_P1, ["AC-1.1", "WC-9", "WC-2"], "P1 adds the flag to commands whose gates and outward defaults are still on until later phases.", A_AC11),
        f("F-2", "MAJOR", "unpassable-check", A_STEP3, ["AC-0.4", "WC-4"], "AC-0.4 requires a WC-4 contract for P0 smoke runs that have no command edits.", A_STEP4),
        f("F-3", "MAJOR", "other", A_GREP, ["AC-C5", "AC-0.3"], "The additive-edit check does not detect a deleted bullet.", None),
    ],
    "a3-r6": [
        f("REQ-1", "MAJOR", "unpassable-check", A_WC4, ["WC-4", "AC-2.3"], "The report-location rule cannot be applied to a dozen commands the spec lists.", A_TDD),
        f("REQ-2", "MAJOR", "contradiction", A_AC11, ["AC-1.1"], "AC-1.1 requires edits that the rows forbid or schedule for later phases.", A_P1),
        f("ARCH-1", "CRITICAL", "contradiction", A_WC6, ["WC-4", "WC-6"], "WC-4 and WC-6 contradict on where a retry writes, so the coordinator reads a stale contract.", A_BRIEF),
    ],
}
R2 = {
    "a3-r1": ("final", [p("F1", "resolved"), p("F2", "resolved")]),
    "a3-r2": ("final", [p("R1-B1", "resolved"), p("R1-B2", "resolved")]),
    "a3-r3": ("final", [p("F1", "resolved"), p("F2", "resolved"), p("F3", "resolved")]),
    "a3-r4": ("final", [p("F-01", "resolved")]),
    "a3-r5": ("final", [p("F-1", "resolved"), p("F-2", "resolved"), p("F-3", "resolved")]),
    "a3-r6": ("v2", [p("REQ-1", "resolved"), p("REQ-2", "resolved"), p("ARCH-1", "resolved"),
                     f("NEW-1", "CRITICAL", "contradiction", A_V2_REUSE, ["WC-6", "AC-3.2"],
                       "Section 2.3 forbids reusing the output directory on a retry, but WC-6 and the roadmap row need the state kept in it.", A_V2_ROAD)]),
}
R3 = {"a3-r6": ("final", [p("NEW-1", "resolved")])}


def spec_text(run, which):
    base = SP / f"p11/runs/{run}/ws/.dev/orca-command-refactor/specs"
    if which == "orig":
        return OV.read_text()
    if which == "v2":
        return (base / "history/spec-v2.md").read_text()
    return (base / "orca-worker-contract-spec.md").read_text()


def main():
    bad = 0
    out_root = AB / "fixtures"
    for run in sorted(R1):
        (out_root / run).mkdir(parents=True, exist_ok=True)
        for n, (which, lines) in ((1, ("orig", R1[run])), (2, R2[run]), *(((3, R3[run]),) if run in R3 else ())):
            text = spec_text(run, which)
            for ln in lines:
                if "prior" in ln:
                    continue
                for key in ("anchor", "anchor2"):
                    if key not in ln:
                        continue
                    q = ln[key]
                    hits = F.locate(text, q)
                    ok = len(F.flat(q)) >= 12 and len(F.flat(q)) <= 200 and len(hits) >= 1
                    print(f"{run} round{n} {ln['id']:6s} {key:7s} len={len(F.flat(q)):3d} hits={len(hits)} spans={hits[:3]} {'OK' if ok else 'BAD'}")
                    bad += 0 if ok else 1
            (out_root / run / f"round{n}.findings").write_text("\n".join(json.dumps(l) for l in lines) + "\n")
    print("anchor check:", "ALL OK" if not bad else f"{bad} BAD")
    sys.exit(1 if bad else 0)


main()
