"""Build the A.10.5 qualitative prompts for revision R2 (run from the repo root: uv run python -I <file>)."""
import hashlib
import json
import re
from pathlib import Path

P = Path(".dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653")
R2 = P / "revisions/plan-defect-fixes-20261110"
QA = R2 / "qa"
TASK = P / "TASK-RF-sweep-phase1-20261108-072653.md"
lines = TASK.read_text().split("\n")
pres = json.loads((QA / "preservation-check.json").read_text())
changed = pres["changed_by_label"]

# 1. inherited structural block from the cycle-1 verifier (contiguous Part 4 table, byte-for-byte)
v = (QA / "A10-verify1.md").read_text().split("\n")
start = next(i for i, l in enumerate(v) if l.startswith("| Id | Checklist item |"))
end = start
while end < len(v) and v[end].startswith("|"):
    end += 1
table = "\n".join(v[start:end])
cons = QA / "qa-task-validation-consolidated.md"
ctext = cons.read_text()
ctext = ctext.replace(
    "Pending: fresh independent verifier(s) against the cycle-1 plan; table to be recorded below.",
    "Verifier afd6029f1537b52aa (`qa/A10-verify1.md`): VERDICT PASS, blocking 0. B2-1, B2-2 and S16-1 closed; no regression; structural table S1 to S16 PASS (S13, S14, S15 with carried MINOR notes). Plan sha256 verified: eb291f0bdd1a787131a3b5295150b0f109b46943a1c43c638fd2ad4652d29f99.",
)
if "\n## Items Reviewed" not in ctext:
    ctext = ctext.rstrip("\n") + "\n\n## Items Reviewed\n\n" + table + "\n"
cons.write_text(ctext)
block = ctext.split("\n## Items Reviewed\n", 1)[1].strip("\n")
assert block == table.strip("\n"), "inherited block differs from producer table"

# 2. targets per lens
HEAD = re.compile(r"^- \[( |x)\] \*\*(\d+\.\d+[a-z]?) ")
items = {}
cur = None
for i, l in enumerate(lines):
    m = HEAD.match(l)
    if m:
        cur = m.group(2)
        items[cur] = [i, i]
    elif cur and l.startswith("  - **"):
        items[cur][1] = i
PATH = re.compile(r"`([^`\s]*(?:/[^`\s]*|\.(?:md|py|json|txt|yaml|yml|sh))[^`\s]*)`")


def refs(label):
    a, b = items[label]
    seen, out = set(), []
    for l in lines[a : b + 1]:
        for m in PATH.finditer(l):
            p = m.group(1).rstrip(".,;:)")
            if p in seen or "$" in p or "<" in p:
                continue
            seen.add(p)
            e = None if any(c in p for c in "*{}[]") else Path(p.replace("~/", str(Path.home()) + "/")).exists()
            out.append({"path": p, "exists_now": e})
    return out


LENS = {
    "operational": dict(
        phases=[7, 8, 10, 11],
        name="operational-correctness",
        out="qa-qualitative-operational-report.md",
        focus="Trace the changed commands and expected values to a CORRECT run and to a failing run: the F-01 decision-count commands (glob OQ-[1-8], optional OQ-17/OQ-18, expected values) in 7.20, 7.30 and 7.34 against three file sets (the eight prerequisites alone; plus one resolved optional decision; plus both) and against the 7.22/7.25 row rules and the 7.33 regression and monotonicity halts; the F-04 `## Execution authorization (verbatim)` section (written first in 7.10, checked in 7.20, compared with the R2 BUILD-REQUEST authorization section) including a resumed session after a failed check; the F-03 embedded addendum clauses against the 11.4 pins (presence, never absence); the F-05 repair routes in 11.4; the F-07 sha256 guard order; the F-08 style count of 6; the F-09 pointer; the 8.19 and 10.5 GQ-35/GQ-63 wording. Also challenge role and person overlap, the seven clauses, error/injection/no-authority, per-file timing, source vs HOME, and actual tests.",
    ),
    "sufficiency": dict(
        phases=[13, 14],
        name="QA-gate-sufficiency",
        out="qa-qualitative-sufficiency-report.md",
        focus="Check every assigned downstream docs/final/fidelity/POST gate retains full counts, lenses, serialization, 2 cycles, source fidelity and actually validates the new behavior and evidence; no authority-editable fixers, no .dev diff bypass, no lost style/skill/test trace. Specifically: item 13.1 now quotes the DESIGN section 9 row R2 bullet (DESIGN line 716) and uses `grep -nF` and a line-404 placement check; verify the quote against docs/designs/orchestrator-mode.md, that the 13.12 routing lens (TL near 2342) and item 13.2 line shifts agree with it, and that ticked item 5.2 is untouched; item 14.19 wording for the optional OQ-17/OQ-18 decisions; the F-06 Context rewording on every 13.x and 14.x item; and that the F-01 to F-10 edits left each 14.x gate with its agent count, serialized fixer and sha256 guards (compare with the baseline).",
    ),
}
inj = []
for key, d in LENS.items():
    labels = [l for l in changed if int(l.split(".")[0]) in d["phases"]]
    labels.sort(key=lambda s: tuple(int(x) for x in s.split(".")))
    tj = {
        "phases": d["phases"],
        "changed_labels": labels,
        "extraction": "All path-like file references in assigned changed checklist bodies, not a sampled list. Resolve shorthand/globs/installed paths through item context; missing future outputs must have earlier creation prerequisites, not be fabricated as current files.",
        "targets": [],
    }
    seen = set()
    for lab in labels:
        for r in refs(lab):
            if r["path"] not in seen:
                seen.add(r["path"])
                tj["targets"].append({**r, "first_item": lab, "kind": "planned_or_reference_requires_context_resolution"})
    (QA / f"targets-{key}.json").write_text(json.dumps(tj, indent=2))
    prompt = f"""QA_PHASE: task-qualitative
fix_authorization: false
LENS: {d['name']}
assigned_phases: {d['phases']}

WORKTREE: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
P=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653
R2=P/revisions/plan-defect-fixes-20261110
R1=P/revisions/chat-output-exception-20261109-133150
TASK FILE: P/TASK-RF-sweep-phase1-20261108-072653.md (plan sha256 eb291f0bdd1a787131a3b5295150b0f109b46943a1c43c638fd2ad4652d29f99)
RESEARCH DIR: P/research/ and R1/research/ (R2 ran no new research; its basis is R1/reflect/pre/adversarial/merged-verdict.yaml findings F-01..F-10, invariant-probe.md and refactor-plan-review.md)
TRACK GOAL: Second bounded revision of the existing checked task plan for issue #339 (sweep coordinator chat-output exception): fix ten recorded plan-text defects F-01..F-10 in 85 allowed unfinished item bodies, line-stable, preserving all 355 headers/order/titles/checkbox states, 137 completed bodies, ledger, item map, owner decisions (including actual choice (b) for GQ-63) and review history. No execution authority is implied: item 7.10 stays unstarted and needs the result-file authorization the item now requires.

TARGET FILES (verify ALL, no sampling): Read R2/qa/targets-{key}.json, which enumerates every extracted file reference in each assigned changed item. Resolve shorthand/glob/installed references from the complete item text; do not pretend future outputs already exist. For each planned file verify its creating prerequisite or explicit creation action; read all actual existing target sources needed for semantic claims, not research summaries alone. Read every assigned changed item body and its boundary consumers, not a representative sample. The other partition covers the other phases; record cross-phase limitations, with relevant cross-boundary consumers still inspected. R2/baseline/task-before-rev2.md and R2/delta-manifest.md identify the changed scope (`diff` shows every changed line); do not reopen the 137 completed items or old accepted minor findings. Read all assigned source chunks at most 150 lines.

PROJECT CONVENTIONS: Canonical src is source-of-truth; project .claude mirrors must not be edited/staged. make sync-dev copies primitives, NOT HOME output styles; no source edit proves installed activation. Current task has 355 same headers, 137 completed and original T138 start; ledger/map/history/ref immutable in the revision. New source changes/tests/sync/install are NOT performed during this review. Future per-file allocation: style 7.10, skill 11.3, test 11.4, with the explicit early Markdown phase exception. Tests use UV and actual source text; no live Orca/ccsession/model launches. Keep exact runtime tool/fallback/timeout/read/no-advice/report JSON contracts. Owner execution approval is separate and does not waive checks.

## Inherited Structural Verdict (rf-qa A.10 output - DO NOT re-verify)
## Items Reviewed

{table}

The table above is the freshly extracted contiguous Items Reviewed span from the current structural producer (R2/qa/A10-verify1.md, VERDICT PASS after one serialized fix cycle; the cycle-0 FAIL reports are retained as history), preserved byte-for-byte, and it is the same span as in R2/qa/qa-task-validation-consolidated.md. Effective live TB catalogue is ["TB-Add-1", "TB-Add-3", "TB-Add-4", "TB-Add-5", "TB-Add-6", "TB-Add-7", "TB-Add-8"]. Items PASS skip structural rechecking, not semantics; reliance is not verification. S14 (TB-Add-6) is a MINOR formatting note carried from the baseline; do not turn it into a blocker or fix it; any independently demonstrated real defect still blocks. Preserve actual binary-verdict semantics and fresh-source checking.

ADVERSARIAL STANCE: Assume the work contains errors. Find what was missed, not merely confirm a previous PASS. Verify semantic claims exhaustively; zero findings requires a concrete self-audit. Do not invent findings to meet a quota. {d['focus']} Own {len(labels)} changed items plus their boundary consumers.

INSTRUCTIONS: Read R2/BUILD-REQUEST.md (the GOAL is the TRACK GOAL above), R2/delta-manifest.md, R2/qa/qa-task-validation-consolidated.md, R2/qa/qa-task-research-alignment-report.md, R1/design-addendum.md and the actual target sources. Apply all 15 Task File Qualitative checks from your effective agent definition, adapting non-code checks to document/action contracts, never N/A: gate/command preconditions; project conventions; phase order; signature/value verification; module/surrounding context; sibling input shape/downstream consumers; actual artifact test validity; primary use case coverage; error paths; runtime/document followability; honest completion scope; ambient dependencies; kwargs/sequence; existence claims verified; actual template references. Reason through all referenced shell/make/test command preconditions without running them (you may run read-only greps and sha256sum on existing files, and shell-simulate decision-count commands in a temp directory under /tmp). Check all task QA/validation/testing duties from the request remain encoded, with no lost full-intensity lenses, fix serialization, fidelity or POST. Model execution and installed activation are explicitly unverified, not silent passes.

Apply five axes drift, contradictions, omissions, weakened-criteria, invented-content across all 15 checks. Every Items Reviewed row has axis exactly AX-1, AX-2, AX-3, AX-4, AX-5 or none: PASS/no finding => none; FAIL => most-specific AX code; never blank/N/A. A GOAL is available, so drift-axis-inactive is not applicable. Self-Audit must list which producer PASS rows you relied on and at least one semantic check requiring your own tools despite structural PASS. Do not count inherited rows as independent semantic work. Real wrong behavior/false claim/missing required output/security risk is blocking; cosmetic/form/citation-format minor never fails.

OUTPUT FILE: R2/qa/{d['out']}
Read your governing report template. If own writing allowed, stub immediately then populate incrementally and Read back. If higher instructions prohibit report writes, obey them, perform the complete READ-ONLY review and return full concise Markdown for parent persistence with explicit no-file-written. Transport restriction alone is not a semantic FAIL; no fabricated artifact. Required report: assigned scope/partition limitations, 15-row Items Reviewed with axis/PASS or FAIL/citations, findings IDs/blocking-or-minor/evidence/smallest fix, self-audit, exact line `VERDICT: PASS` or `VERDICT: FAIL`, then `Blocking count: <n>`. Complete assessment is required, not just summary. No edits/fixes outside your own report, no task/design/style/product/ledger/map/history changes, tests/sync/install/network/Orca/Git mutations/subagents/team tools/SendMessage. All Python via UV (`uv run python -I`). Return the actual path if saved or the complete body otherwise. Write output then stop.
"""
    pf = QA / f"prompt-qualitative-{key}-cycle0.txt"
    pf.write_text(prompt)
    inj.append(
        {
            "prompt": str(pf),
            "producer": str(QA / "A10-verify1.md"),
            "producer_sha256": hashlib.sha256((QA / "A10-verify1.md").read_bytes()).hexdigest(),
            "injected_block_sha256": hashlib.sha256(table.encode()).hexdigest(),
            "block_in_prompt": table in prompt,
            "block_in_consolidated": table in ctext,
            "live_tb_add": ["TB-Add-1", "TB-Add-3", "TB-Add-4", "TB-Add-5", "TB-Add-6", "TB-Add-7", "TB-Add-8"],
            "labels": len(labels),
            "targets": len(tj["targets"]),
        }
    )
(QA / "qualitative-injection-cycle0.json").write_text(json.dumps(inj, indent=2))
print(json.dumps(inj, indent=1))
