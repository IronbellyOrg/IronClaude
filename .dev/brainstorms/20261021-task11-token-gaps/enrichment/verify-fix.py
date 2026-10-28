"""Scratch: prove the recommended needles are exact substrings and each kills its gap mutation. In-memory only."""
import importlib.util, sys
from pathlib import Path

REPO = Path("/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate")
spec = importlib.util.spec_from_file_location("c11", REPO / "tests/skills/test_auggie_claim_gate_contract.py")
m = importlib.util.module_from_spec(spec); sys.modules["c11"] = m; spec.loader.exec_module(m)
BASE = m.load(REPO)


def extra(t):
    need, gs, sec = m.need, m.gate_section, m.section
    scope = gs(t, "Claim scope")
    need(scope, "The admitted record keeps only supported consequences in `claim.harm`.",
         "at least one consequence is supported and every other table condition holds",
         "and all consequences are listed in `excluded_consequences[]`", where="Claim scope")
    w2 = sec(t["skill"], "### Wave 2: Review Agent Pass", "### Wave 3")
    need(w2, "the status is `failed` with reason `invariant_check_unavailable`",
         "`allowed-tools` is not a prerequisite check", where="Wave 2")
    need(gs(t, "Status mapping"), "or `jq` absent at the preflight (reason `invariant_check_unavailable`)", where="Status mapping")
    need(gs(t, "Invariant check"), "If it is not, the status is `failed` with reason `invariant_check_unavailable`", where="Invariant check")
    r = sec(t["rubric"], "## Admission precedes grading", "## Severity-remap algorithm")
    need(r, "whose category is not `security` or `data-integrity` and whose harm does not meet a Critical definition", where="rubric")
    need(gs(t, "Evidence-source rules"),
         "any row that needs the head object is `unproven` with `head_mismatch_context_unavailable`", where="Evidence-source rules")


extra(BASE)
print("base passes new needles")
MUT = [
    ("G2a", "gate", "keeps only supported consequences in `claim.harm`", "keeps every consequence in `claim.harm`"),
    ("G2b", "gate", ", and all consequences are listed in `excluded_consequences[]`", ""),
    ("G2c", "gate", " and every other table condition holds", ""),
    ("G3a", "skill", "the status is `failed` with reason `invariant_check_unavailable`", "the status is `partial` with reason `invariant_check_unavailable`"),
    ("G3b", "gate", "If it is not, the status is `failed` with reason", "If it is not, the status is `partial` with reason"),
    ("G3c", "gate", "or `jq` absent at the preflight (reason `invariant_check_unavailable`)", ""),
    ("G3d", "skill", " `allowed-tools` is not a prerequisite check.", ""),
    ("G7", "rubric", "whose category is not `security` or `data-integrity`", "whose category is `security` or `data-integrity`"),
    ("G9", "gate", ", and any row that needs the head object is `unproven` with `head_mismatch_context_unavailable`", ""),
]
for n, k, o, new in MUT:
    t = dict(BASE); assert o in t[k], n; t[k] = t[k].replace(o, new, 1)
    try:
        extra(t); print(n, "SURVIVES")
    except AssertionError:
        print(n, "caught")
