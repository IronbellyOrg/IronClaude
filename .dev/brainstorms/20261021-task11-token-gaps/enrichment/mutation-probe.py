"""Scratch mutation probe for the Task 11 contract tests. Reads repo files, mutates in memory only."""
import importlib.util, json, re, sys
from pathlib import Path

REPO = Path("/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate")
spec = importlib.util.spec_from_file_location("c11", REPO / "tests/skills/test_auggie_claim_gate_contract.py")
m = importlib.util.module_from_spec(spec)
sys.modules["c11"] = m
spec.loader.exec_module(m)

CHECKS = [getattr(m, n) for n in sorted(dir(m)) if n.startswith("check_at")]
BASE = m.load(REPO)


def run(t):
    """Return names of checks that fail on texts t."""
    failed = []
    for c in CHECKS:
        try:
            c(t)
        except Exception:
            failed.append(c.__name__)
    return failed


assert run(BASE) == [], run(BASE)


def mutate(key, old, new, count=1):
    t = dict(BASE)
    assert old in t[key], f"needle not found: {old[:60]!r}"
    t[key] = t[key].replace(old, new, count)
    return t


NAMED = [
    # id, file, old, new
    ("G1a REQ-012 Any claim", "gate", "A `protocol_literal` claim that a prescribed", "Any claim that a prescribed"),
    ("G1b REQ-012 anchors swapped", "gate", "the prescribing instruction (the entrypoint) and the violated precondition (the producer)",
     "the prescribing instruction (the producer) and the violated precondition (the entrypoint)"),
    ("G2a REQ-008 keeps every consequence", "gate", "keeps only supported consequences in `claim.harm`", "keeps every consequence in `claim.harm`"),
    ("G2b REQ-010 drop 'all consequences listed'", "gate", ", and all consequences are listed in `excluded_consequences[]`", ""),
    ("G2c REQ-009 drop 'every other table condition'", "gate", " and every other table condition holds", ""),
    ("G3a REQ-037 SKILL w2 failed->partial", "skill", "the status is `failed` with reason `invariant_check_unavailable`", "the status is `partial` with reason `invariant_check_unavailable`"),
    ("G3b REQ-037 gate preflight failed->partial", "gate", "If it is not, the status is `failed` with reason `invariant_check_unavailable`", "If it is not, the status is `partial` with reason `invariant_check_unavailable`"),
    ("G3c REQ-037 status map moved to partial", "gate",
     "or `jq` absent at the preflight (reason `invariant_check_unavailable`).\n- `partial` keeps the baseline causes (for example",
     ".\n- `partial` keeps the baseline causes, including `jq` absent at the preflight (reason `invariant_check_unavailable`) (for example"),
    ("G3d allowed-tools sentence deleted (SKILL)", "skill", " `allowed-tools` is not a prerequisite check.", ""),
    ("G3e allowed-tools sentence deleted (gate)", "gate", " `allowed-tools` is not a prerequisite check.", ""),
    ("G4 REQ-004 agent r5 Emit->Move to cross-cutting", "agent", "Emit out-of-diff concerns as candidates with `in_diff: false`", "Move out-of-diff concerns to cross-cutting notes with `in_diff: false`"),
    ("G5a REQ-022 every mode", "gate", "In explicit `--diff` mode the target is committed history.", "In every mode the target is committed history."),
    ("G5b REQ-022 local_read sentence deleted", "gate", " Only implicit dirty-tree diff mode and snapshot mode use `local_read` of uncommitted edits.", ""),
    ("G6a REQ-026 lowest-rank", "gate", "highest-rank member's disposition", "lowest-rank member's disposition"),
    ("G6b REQ-026 count votes", "gate", "never count votes", "count votes"),
    ("G6c REQ-026 non-defect sentence deleted", "gate", "The group takes the highest-rank member's disposition. ", ""),
    ("G7 REQ-018 rubric cap inverted", "rubric", "whose category is not `security` or `data-integrity`", "whose category is `security` or `data-integrity`"),
    ("G7b REQ-018 gate cap inverted", "gate", "whose category is not `security` or `data-integrity` and whose harm", "whose category is `security` or `data-integrity` and whose harm"),
    ("G8a REQ-013 table intro deleted", "gate", "The orchestrator evaluates this table top to bottom for each candidate and records the matching row ids in `disposition_reasons[]`. ", ""),
    ("G8b REQ-013 Verified def (table copy) deleted", "gate", ' "Verified" means the orchestrator Read the cited line in this run.\n\n| Row', "\n\n| Row"),
    ("G9 REQ-021 head-object fallback deleted", "gate", ", and any row that needs the head object is `unproven` with `head_mismatch_context_unavailable`", ""),
    ("G10a REQ-005 SKILL not downgraded -> downgraded", "skill", "dropped into `dropped_ungrounded[]`, not downgraded", "downgraded to `unproven`"),
    ("G10b REQ-005 gate never converted deleted", "gate", " and is never converted to another disposition", ""),
    ("S1 REQ-003 'For every behavioral claim'", "prompts", "for every behavioral claim", "where convenient"),
    ("S2 REQ-014 'The row is then A7'", "gate", "The row is then A7 and", "The row is then A3 and"),
    ("S3 REQ-016 runtime_reproduced exception", "gate", " unless `evidence_kind: runtime_reproduced` with a measured rate", ""),
    ("S4 REQ-019 one entry per applicable row", "gate", "one entry per applicable row A1 to A5", "one entry"),
    ("S5 REQ-023 distinct current ref", "gate", " only when a distinct current ref is known", ""),
    ("S6 REQ-020 snapshot base null", "gate", " Snapshot mode records `base: null`.", ""),
    ("S7 REQ-026 equal rank", "gate", "Equal rank gives `unproven` with `other:mechanism_conflict`.", "Equal rank gives `defect`."),
]

print("== NAMED MUTATIONS ==")
named_out = []
for name, key, old, new in NAMED:
    try:
        t = mutate(key, old, new)
    except AssertionError as e:
        print(f"[NOMATCH] {name}: {e}")
        named_out.append((name, "NOMATCH", []))
        continue
    f = run(t)
    status = "CAUGHT " + ",".join(f) if f else "SURVIVES"
    print(f"{status:40s} {name}")
    named_out.append((name, "caught" if f else "survives", f))

# ---- automated sweep: operator flips and sentence deletions (jq fence excluded)


def jq_span(text):
    m_ = re.search(r"^```jq\n.*?^```$", text, flags=re.S | re.M)
    return (m_.start(), m_.end()) if m_ else (0, 0)


FLIPS = [
    (r"\bnot\b", ""), (r"\bnever\b", ""), (r"\bonly\b", ""), (r"\bevery\b", "any"), (r"\bhighest\b", "lowest"),
    (r"\bstrictly\b", ""), (r"\bmust\b", "may"), (r"\bfirst\b", "last"), (r"\bfailed\b", "partial"),
    (r"\bis required\b", "is optional"), (r"\bmandatory\b", "optional"), (r"\bnon-null\b", "null"),
    (r"\bnon-empty\b", "empty"), (r"\bat least\b", "at most"), (r"\bnone\b", "all"),
    (r"\bnever\b", "always"), (r"\bdefect\b", "unproven"),
]

FILEKEYS = ["skill", "gate", "prompts", "rubric", "handoff", "agent", "command"]
flip_total = 0
flip_surv = []
for key in FILEKEYS:
    text = BASE[key]
    js = jq_span(text) if key == "gate" else (0, 0)
    for pat, rep in FLIPS:
        for mm in re.finditer(pat, text):
            if js[0] <= mm.start() < js[1]:
                continue
            # skip inside code-fence-free headings? keep all
            new = text[: mm.start()] + rep + text[mm.end():]
            t = dict(BASE)
            t[key] = new
            flip_total += 1
            if not run(t):
                line_no = text.count("\n", 0, mm.start()) + 1
                ctx = text[max(0, mm.start() - 50): mm.end() + 50].replace("\n", " ")
                flip_surv.append((key, line_no, pat, ctx))

print(f"\n== FLIP SWEEP: {flip_total} mutants, {len(flip_surv)} survive ({100*len(flip_surv)/max(flip_total,1):.0f}%) ==")
by = {}
for k, ln, pat, ctx in flip_surv:
    by[k] = by.get(k, 0) + 1
print("survivors by file:", by)

# sentence deletion sweep
def segments(text, js):
    out = []
    pos = 0
    for line in text.split("\n"):
        start = pos
        pos += len(line) + 1
        if js[0] <= start < js[1]:
            continue
        s = line.strip()
        if not s or s.startswith("#") or re.fullmatch(r"[|\-: ]+", s) or s.startswith("```") or s.startswith("<!--"):
            continue
        if s.startswith("|"):
            out.append((start, start + len(line)))
            continue
        # split sentences inside line
        for sm in re.finditer(r"[^.;]+(?:\.|;|$)\s*", line):
            seg = sm.group(0)
            if len(seg.strip()) < 25:
                continue
            out.append((start + sm.start(), start + sm.end()))
    return out

del_total = 0
del_surv = []
for key in FILEKEYS:
    text = BASE[key]
    js = jq_span(text) if key == "gate" else (0, 0)
    for a, b in segments(text, js):
        t = dict(BASE)
        t[key] = text[:a] + text[b:]
        del_total += 1
        if not run(t):
            del_surv.append((key, text.count("\n", 0, a) + 1, text[a:b].strip()[:110]))

print(f"\n== SENTENCE-DELETION SWEEP: {del_total} mutants, {len(del_surv)} survive ({100*len(del_surv)/max(del_total,1):.0f}%) ==")
by = {}
tot = {}
for k, ln, s in del_surv:
    by[k] = by.get(k, 0) + 1
print("survivors by file:", by)

Path("/tmp/t11_scratch/out.json").write_text(json.dumps({
    "named": named_out, "flip_total": flip_total, "flip_surv": flip_surv,
    "del_total": del_total, "del_surv": del_surv}, indent=1))
