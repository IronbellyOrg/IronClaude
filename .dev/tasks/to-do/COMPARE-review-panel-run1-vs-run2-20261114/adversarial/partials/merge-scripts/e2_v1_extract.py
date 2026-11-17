#!/usr/bin/env python3
"""Merge executor E2 of 4: extract the transformed Variant 1 (run 1) blocks.

Plan: adversarial/refactor-plan.md (rule 3 id rule, M-03..M-07, M-09, M-11, M-14, M-16..M-22, M-25, M-27).
Reads only variant-1-original.md; writes one file per block under partials/merge-stage/v1-blocks/
and the log partials/merge-stage/E2-extraction-log.md. Run with: uv run --no-project python <this file>.

Order per block (rule 3 and the executor brief): (1) closed-item rename to R1-CLS-nn, (2) range pre-pass,
(3) single-pass id prefix with the anchored alternation (backticks, fenced blocks, URLs and file.ext:line cites
protected), (4) M-25 corrections and per-change edits (dropped lines, modified lines, status column, lead
sentences, legend lines), (5) heading demotion (M-27).
"""
from __future__ import annotations

import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ADV = Path(__file__).resolve().parents[2]
SRC = ADV / "variant-1-original.md"
OUT = ADV / "partials" / "merge-stage" / "v1-blocks"
LOG = ADV / "partials" / "merge-stage" / "E2-extraction-log.md"

V1 = SRC.read_text(encoding="utf-8").split("\n")
assert len(V1) in (4476, 4477), len(V1)


def L(n: int) -> str:
    return V1[n - 1]


# ---------------------------------------------------------------- fences (protected like backticks)
FENCE: set[int] = set()
FENCE_RANGES: list[tuple[int, int]] = []
_open = None
for _i, _l in enumerate(V1, 1):
    if _l.lstrip().startswith("```"):
        if _open is None:
            _open = _i
        else:
            FENCE_RANGES.append((_open, _i))
            FENCE.update(range(_open, _i + 1))
            _open = None
assert _open is None

# ---------------------------------------------------------------- protected spans inside a line
FILE_EXT = r"(?:py|md|json|sh|yaml|yml|tsv|jsonl|txt|toml|csv|html)"
PROT = re.compile(
    r"``.+?``"                      # double-backtick code span
    r"|`[^`\n]*`"                   # code span
    r"|https?://[^\s)\]>|]+"        # URL
    r"|[\w./~-]*\w\." + FILE_EXT + r"(?::\d+(?:[-,]\d+)*)?(?![\w])"  # file.ext[:line] cite
)
PROT_COUNTS: Counter = Counter()


def prot_spans(s: str, count: bool = False) -> list[tuple[int, int]]:
    out = []
    for m in PROT.finditer(s):
        out.append((m.start(), m.end()))
        if count:
            t = m.group(0)
            kind = "code span" if t.startswith("`") else ("URL" if t.startswith("http") else "file cite")
            PROT_COUNTS[kind] += 1
    return out


def inside(pos: int, spans) -> bool:
    return any(a <= pos < b for a, b in spans)


# ---------------------------------------------------------------- step 1: closed-item rename (R1-CLS-nn)
CLOSED_LIST = (4260, 4290)
PINS = {173: {"C-05"}, 238: {"C-10"}, 4476: {"C-25"}}            # plan rule 3 line pins
EXTRA_PINS = {3736: {"C-01", "C-02", "C-04", "C-12"}}             # found by this executor, see log
RE_BARE_C = re.compile(r"(?<![\w-])C-(\d\d)(?![\w])")
RE_GQ = re.compile(r"(GQ[ :])C-(\d\d)(?![\w])")
RE_CLOSED_WORD = re.compile(r"(?i)(closed items?\s+\(?)C-(\d\d)(?![\w])")


def rename_closed(n: int, s: str, rec: list | None) -> str:
    if n in FENCE:
        return s

    def sub(rx, s, kind, grp, pred=lambda m: True):
        spans = prot_spans(s)

        def f(m):
            if inside(m.start(grp), spans) or not pred(m):
                return m.group(0)
            new = m.group(0)[: m.start(grp) - m.start(0)] + "R1-CLS-" + m.group(grp)[2:]
            if rec is not None:
                rec.append((kind, n, m.group(0), new))
            return new

        return rx.sub(f, s)

    if CLOSED_LIST[0] <= n <= CLOSED_LIST[1]:
        s = sub(re.compile(r"(?<![\w-])(C-\d\d)(?![\w])"), s, "list V1:4260-4290", 1)
    s = sub(re.compile(r"(GQ[ :])(C-\d\d)(?![\w])"), s, "GQ C-nn / GQ:C-nn", 2)
    s = sub(re.compile(r"(?i)(closed items?\s+\(?)(C-\d\d)(?![\w])"), s, "after 'closed item(s)'", 2)
    for table, kind in ((PINS, "line pin (plan)"), (EXTRA_PINS, "line pin (extra, executor)")):
        if n in table:
            s = sub(re.compile(r"(?<![\w-])(C-\d\d)(?![\w])"), s, kind, 1,
                    pred=lambda m, want=table[n]: m.group(1) in want)
    return s


# ---------------------------------------------------------------- step 2: range pre-pass
PRE_FAMS = [r"D\d{1,2}", r"X\d{1,2}", r"C\d{1,2}", r"G\d{1,2}", r"H\d{1,2}", r"R\d\d", r"S0[0-5]", r"M[1-4]"]
PRE = re.compile("|".join(rf"(?<![\w-])(?P<a{i}>{f})-(?P<b{i}>{f})(?![\w])" for i, f in enumerate(PRE_FAMS)))

# ---------------------------------------------------------------- step 3: main id pass (rule 3 alternation)
FAMS = [
    ("Cnn-nn", r"C\d\d-\d\d"), ("C-nnn", r"C-\d{3}"), ("X-nnn", r"X-\d{3}"), ("S-nnn", r"S-\d{3}"),
    ("A-nnn", r"A-\d{3}"), ("U-nnn", r"U-\d{3}"), ("Cn", r"C\d{1,2}"), ("C-nn", r"C-\d\d"),
    ("Q-nn", r"Q-\d\d"), ("O-n", r"O-\d{1,2}"), ("OD-n", r"OD-\d+"), ("H-A..C", r"H-[A-C]"),
    ("Hn", r"H\d{1,2}"), ("W0n", r"W0[1-4]"), ("Dn", r"D\d{1,2}"), ("D-nn", r"D-\d\d"), ("D-n", r"D-\d"),
    ("G-nn", r"G-\d\d"), ("Gn", r"G\d{1,2}"), ("G-name", r"G-(?:all|bench|exit|new|pr|replay|skills|sync)"),
    ("BL-nn", r"BL-\d\d"), ("MS-nn", r"MS-\d\d"), ("ENS-n", r"ENS-\d{1,2}"), ("DOC-nn", r"DOC-\d\d"),
    ("OPEN-nn", r"OPEN-\d\d"), ("SC-n", r"SC-\d{1,2}"), ("K-n", r"K-\d{1,2}"), ("Mn-nn", r"M[1-4]-\d\d"),
    ("Mn", r"M[1-4]"), ("S0n", r"S0[0-5]"), ("F-n", r"F-\d{1,2}"), ("V-nnn", r"V-\d{3}"), ("Xn", r"X\d{1,2}"),
    ("A-nn", r"A-\d\d"), ("INV-nnn", r"INV-\d{3}"), ("Rnn", r"R\d\d"), ("CI-n", r"CI-\d"),
]
MAIN = re.compile(r"(?<![\w-])(?:" + "|".join(f"(?:{p})" for _, p in FAMS) + r")(?![\w])")


def family(tok: str) -> str:
    for name, p in FAMS:
        if re.fullmatch(p, tok):
            return name
    raise AssertionError(tok)


# plan rule 3 exemptions: V1:169 `C3` (combo run); probe labels M1-M4 at V1:2704, 2729, 2761
def exempt(n: int, tok: str) -> bool:
    return (n == 169 and tok == "C3") or (n in (2704, 2729, 2761) and re.fullmatch(r"M[1-4]", tok) is not None)


def id_pass(n: int, s: str, rec: dict | None) -> str:
    if n in FENCE:
        return s
    spans = prot_spans(s)

    def fpre(m):
        if inside(m.start(), spans):
            return m.group(0)
        a = next(v for k, v in m.groupdict().items() if k.startswith("a") and v)
        b = next(v for k, v in m.groupdict().items() if k.startswith("b") and v)
        if exempt(n, a) or exempt(n, b):
            if rec is not None:
                rec["exempt"].append((n, m.group(0)))
            return m.group(0)
        new = f"R1-{a}..R1-{b}"
        if rec is not None:
            rec["ranges"].append((n, m.group(0), new))
        return new

    s = PRE.sub(fpre, s)
    spans = prot_spans(s, count=rec is not None)

    def fmain(m):
        tok = m.group(0)
        if inside(m.start(), spans):
            return tok
        if exempt(n, tok):
            if rec is not None:
                rec["exempt"].append((n, tok))
            return tok
        if rec is not None:
            rec["main"].append((n, family(tok), tok, s[max(0, m.start() - 30): m.end() + 30]))
        return "R1-" + tok

    return MAIN.sub(fmain, s)


def ids(n: int, s: str, rec=None, crec=None) -> str:
    return id_pass(n, rename_closed(n, s, crec), rec)


# ---------------------------------------------------------------- probe test (before any block)
PROBES = [
    ("DOC-01", "R1-DOC-01"), ("INV-014", "R1-INV-014"), ("SC-10", "R1-SC-10"), ("C13-22", "R1-C13-22"),
    ("M1-01", "R1-M1-01"), ("GQ C-05", "GQ R1-CLS-05"), ("GQ:C-03", "GQ:R1-CLS-03"), ("D1-D16", "R1-D1..R1-D16"),
    ("Closed item C-01", "Closed item R1-CLS-01"), ("closed item C-08", "closed item R1-CLS-08"),
    ("C-001", "R1-C-001"), ("Decision D-1", "Decision R1-D-1"), ("M3-A-044", "R1-M3-A-044"),
    ("G-sync", "R1-G-sync"), ("X1-X14", "R1-X1..R1-X14"), ("H1-H38", "R1-H1..R1-H38"), ("M1-M4", "R1-M1..R1-M4"),
    ("C05-12 R21", "R1-C05-12 R1-R21"), ("CI-1", "R1-CI-1"), ("O-11", "R1-O-11"), ("ENS-01", "R1-ENS-01"),
    ("`D1`-`D16`", "`D1`-`D16`"), ("panel.py:46,215", "panel.py:46,215"), ("UC-1 EV-1 GT1 R1..Rn", "UC-1 EV-1 GT1 R1..Rn"),
    ("https://arxiv.org/abs/2509.01494 C-01", "https://arxiv.org/abs/2509.01494 R1-C-01"),
]
probe_rows = []
for src, want in PROBES:
    got = ids(0, src)
    again = ids(0, got)
    probe_rows.append((src, want, got, again == got))
    assert got == want, (src, want, got)
    assert again == got, (src, got, again)

# ---------------------------------------------------------------- range assertions
STARTS = {
    108: "**Citation key (used in every Evidence line).**", 129: "Every statement below traces",
    131: "### 2.1 E1: reflect Tier 2", 238: "**Evidence:** `git show 4a22d742:`", 279: "### 2.4 The shared review CLI",
    435: "", 483: "**Conventions used in Sections 3 and 4**", 492: "| Log ids |", 494: "- **Desired behavior:**",
    577: "| Judge calibration |", 579: "## 4. Gap Analysis", 580: "", 733: "| **DOC-71 to DOC-77**",
    735: "### 4.1 Contradictions", 780: "| none (drop) | none |", 783: "## 5. External Research Findings", 784: "",
    1153: "", 1154: "## 6. Options Analysis", 1155: "", 1156: "*(conflict log)*", 2807: "", 2808: "## 7. Recommendation",
    2809: "", 3098: "", 3099: "## 8. Implementation Plan", 3105: "### 8.1 Value inventory (b)", 3821: "",
    3822: "### 8.2 Migration path", 3908: "| M4-07 |", 3909: "", 3910: "#### Gap coverage", 4030: "",
    4031: "### 8.3 No-regression gate list", 4056: "", 4057: "### 8.4 Branch-structure options",
    4059: "**Git constraint (applies to every layout", 4061: "**Facts that shape the options**",
    4063: "| Option | Branch layout |", 4069: "| E. Keep `ironbelly/shadow-runs`", 4071: "### 8.5 Risk register inputs",
    4101: "| Many owner decisions", 4103: "### 8.6 Integration Checklist", 4115: "- [ ] Before any PR:",
    4116: "- [ ] Confirm the chosen branch layout of 8.4", 4120: "- [ ] Hand the owner-decision list", 4122: "",
    4124: "## 9. Open Questions", 4125: "", 4126: "**Source key.**", 4387: "", 4388: "## 10. Evidence Trail", 4389: "",
    4476: "`.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/gaps-and-questions.md`",
    3829: "**Dependencies:**", 3860: "**Dependencies:**", 3879: "**Dependencies:**", 3897: "**Dependencies:**",
    3830: "**Persisted formats and rollback", 3861: "**Rollback (M2;", 3880: "**Rollback (M3;", 3898: "**Rollback (M4;",
}
for n, pre in STARTS.items():
    if pre == "":
        assert L(n) == "", (n, L(n)[:60])
    else:
        assert L(n).startswith(pre), (n, L(n)[:80])

DELETED = {3829: "ordering content (`**Dependencies:**` line of track M1), M-16 (1)",
           3860: "ordering content (`**Dependencies:**` line of track M2), M-16 (1)",
           3879: "ordering content (`**Dependencies:**` line of track M3), M-16 (1)",
           3897: "ordering content (`**Dependencies:**` line of track M4), M-16 (1)"}
MOVED = {3830: "M1", 3861: "M2", 3880: "M3", 3898: "M4"}

# ---------------------------------------------------------------- step 4 data: corrections and edits
UNIT43 = (" [unit not stated by run 1 and not reproducible by grep: `grep -rEn 'subagent_type: *\"?rf-' "
          "src/superclaude/skills` gives 52 lines in 11 files, 44 of them in 8 `SKILL.md` files; Appendix E]")
RE43 = re.compile(r"43 (?:rf-\* )?(?:spawning )?call sites(?: in 11 skill files)?")
READONLY_NOTE = (
    "**Correction (M-24 item 5; R25-INV-006, R25-INV-007).** Where this block names `--allowedTools` as the "
    "restriction, the mechanism is `--tools <read-only set>` or `--restricted`. `--strict-mcp-config` is also needed, "
    "because MCP servers stay available under those flags. `--restricted` refuses `bypassPermissions` and confines "
    "file tools to the working directories. Run 2's C-07 gate G2 must read the MCP server list from the "
    "`system/init` event. The product already has a restricted `claude --print` child "
    "(`src/superclaude/cli/pipeline/process.py:145-154`, `reviewer_profile=True`, used at `runner.py:566` and "
    "`ensemble.py:548`); the \"gated, not built\" launcher must say whether it reuses or replaces it. Flag help text "
    "source: local `claude --help` 2.1.325 (fault-finder row 27)."
)
EDITS = [  # (V1 line, old (post-id-pass text), new, change, note)
    (133, "is three commits ahead (9874d63fb, c2e3347d3, 792cf8c52), and",
     "is three commits ahead (9874d63fb, c2e3347d3, 792cf8c52) at the time of run 1; HEAD `ad8f57560` is now 5 commits past merge-base `d2d8a2d16`, and",
     "M-25", "stale 'three commits ahead' (checked: `git rev-list --count d2d8a2d16..HEAD` = 5, HEAD = ad8f57560, merge-base = d2d8a2d16)"),
    (201, "audit D names 3 plus a merge that lost two blocking findings",
     "audit D names 3 verdict flips (the third is the merge that lost two blocking findings, F1+F2)",
     "M-25", "verdict flips wording (audit D summary)"),
    (204, "timed out 3 of 3 slots", "timed out 3 of 4 runs", "M-25",
     "Qwen3.8-max '3 of 3 slots' corrected to '3 of 4 runs' (checked: `git show 4a22d742:.../combos/SPEC.md` line 3 'on 3 of 4 runs')"),
    (305, "OR refs intersect", "OR (refs intersect or both refs empty)", "M-25",
     "same_defect both-empty-refs branch (checked: `findings.py:367-379`, `if ra & rb or (not ra and not rb)`); line is inside a fence, tag on caption V1:319"),
    (381, "has 37 files and 353 tests", "has 38 files and 353 tests", "M-25", "37 corrected to 38 reflect test files (V1:381 only; checked by fault-finder row 6)"),
    (2332, "(or `claude -p --allowedTools`)",
     "(or `claude -p` with `--tools <read-only set>` or `--restricted`, see the correction below the recommended resolution)",
     "M-25 (M-24 item 5)", "read-only mechanism"),
    (4038, "and `:468-472` (final `verdict:` line)",
     "and `:468-472` (final `verdict:` line) [conditional on run 1's verdict design, which is not adopted; these two pins belong on the rewrite list of run 2's C18 (R25-INV-026)]",
     "M-17", "R1-G2 must-not-change pins marked conditional"),
    (4061, "is 3 commits ahead of `origin/master` touching only",
     "is 5 commits past merge-base `d2d8a2d16` (`origin/master` `d4d1662a8` is 3 commits past the merge-base), touching only",
     "M-19 / M-25", "stale '3 commits ahead' (checked: `git rev-list --count` d2d8a2d16..HEAD = 5, d2d8a2d16..origin/master = 3; `git diff --stat d2d8a2d16 HEAD -- src tests scripts` = SKILL.md, refs/reviewer-spec.md, two reflect tests)"),
    (4116, "Confirm the chosen branch layout of 8.4 does not create",
     "Confirm the branch names (see 8.7 constraint) does not create", "M-20", "'the chosen branch layout of 8.4' replaced by 'the branch names (see 8.7 constraint)' (text as the plan gives it)"),
    (4120, " and mark the steps that wait on each", "", "M-20", "ordering clause dropped"),
]
CAPTION_319 = (" [Correction M-25: the `findings.cluster` line of the diagram now names the both-empty-refs branch "
               "of `same_defect` (`findings.py:367-379`).]")
LINES43 = [410, 616, 624, 716, 2443, 2976, 3567, 3790, 4092, 4348]

# ---------------------------------------------------------------- step-status (M-16, R25-INV-027)
CONFLICTS = OrderedDict([("M1-01", "C-01"), ("M1-05", "C-10"), ("M1-06", "C-01"), ("M1-08", "C-02/C-03"),
                         ("M1-12", "C-08"), ("M1-13", "C-08"), ("M1-21", "X-14"), ("M3-02", "C24"),
                         ("M4-01", None), ("M4-03", None), ("M4-04", "C-10/C23"), ("M4-05", "C-11"), ("M4-07", "C-11")])
UNNAMED = {"M4-01": "the step edits `fsm.py`", "M4-03": "the step edits `severity_router.py`"}
PARTLY = ["M1-02", "M1-04", "M1-07", "M1-09", "M1-10", "M1-16", "M1-17", "M2-02", "M2-04", "M2-08", "M2-10",
          "M3-01", "M4-02", "M4-06"]
assert len(CONFLICTS) == 13 and len(PARTLY) == 14 and not set(CONFLICTS) & set(PARTLY)


def status_text(step: str) -> tuple[str, str]:
    if step in CONFLICTS:
        oid = CONFLICTS[step]
        what = (f"run 2 outcome {oid}" if oid else
                f"run 2's adopted design (R25-INV-027 names no outcome id: {UNNAMED[step]})")
        return "CONFLICTS", (f"CONFLICTS: Carried as the content of run 1's alternative; conflicts with {what}; "
                             "not plan input until re-adjudicated")
    if step in PARTLY:
        return "PARTLY COMPATIBLE", "PARTLY COMPATIBLE (R25-INV-027): re-adjudicate before use as plan input"
    return "COMPATIBLE", "COMPATIBLE (R25-INV-027)"


# ---------------------------------------------------------------- block definitions
LEGEND = "In this merged copy, these ids carry the prefix `R1-` (Merge Notes, id rule). <!-- Source: new (legend line, rule 3) -->"


def new(text: str, change: str) -> str:
    return f"{text} <!-- Source: new (lead per Change #{change}) -->"


BLOCKS = [
    dict(file="M03-sec2.md", change="M-03", sec="2", ranges=[(108, 129), (131, 238), (279, 435)],
         heading="### 2.10 Run 1 current-state material",
         lead=[new("Run 2 Sections 2.1-2.9 govern where they differ; corrections applied inside the block are listed in "
                   "Appendix E. This block carries run 1's Section 2 citation key and its subsections 2.1, 2.2, 2.4 and 2.5 "
                   "(V1:108-129, 131-238, 279-435); run 1's 2.3 (E3) and 2.6 (overlap matrix) are not carried because "
                   "run 2's 2.4 and 2.9 supersede them. Run 1's matrix stance was that no component is implemented "
                   "identically by two efforts (V1:461); run 2's 16-row matrix classifies 11 rows conflicting and 1 "
                   "identical (Ids) (V2:1102).", "M-03")],
         after={129: ["", LEGEND]}),
    dict(file="M04-sec3.md", change="M-04", sec="3", ranges=[(483, 492), (494, 577)],
         heading="### 3.6 Run 1 target-state material",
         lead=[new("Run 2's delta table (V2:1125-1144) governs. The diagram below shows run 1's superset-core target, "
                   "which is the recorded one-engine alternative (run 2 Section 6.1 Option A, trigger T-c). The V1 advocate "
                   "holds that the core-shape difference is a label (MERGE/BOTH); the V2 advocate holds V2 (C-005, C-076, "
                   "X-051, unresolved).", "M-04")],
         after={492: ["", LEGEND]}),
    dict(file="M05-sec4-gaprows.md", change="M-05", sec="4", ranges=[(580, 733)],
         heading="### 4.7 Run 1 gap rows",
         lead=[new("Run 1's gap table is carried with its per-row `Track:` tags. Run 1 counts 145 rows (15 Critical, 66 "
                   "Important, 64 Minor; V1:760-762) and run 2 counts 148 rows (24 Critical, 93 Important, 31 Minor; "
                   "V2:1387); both counts were verified and measure different units. Severity ratings differ on facts "
                   "both reports agree on (Appendix C rows X-011 to X-019). Run 2's rule (V2:1121) and its C8 table "
                   "(V2:1411-1422) govern the ratings in the base.", "M-05")]),
    dict(file="M06-sec4-contradictions.md", change="M-06", sec="4", ranges=[(735, 780)],
         heading="### 4.8 Run 1 contradictions and track coverage",
         lead=[new("Run 1's contradictions table, coverage self-check and Critical and Important rows by track, with the "
                   "`Track` mapping kept. R1-M1 to R1-M4 are run 1's track names for its migration steps (the steps are "
                   "carried in 8.4).", "M-06")]),
    dict(file="M07-sec5.md", change="M-07", sec="5", ranges=[(784, 1153)],
         heading="### 5.6 Run 1 external findings",
         lead=[new("Run 1's external sources (V1:853-1079) and run 2's (V2:1620-2036) are nearly disjoint sets, so run 1's "
                   "Section 5 is carried whole; run 2 Sections 5.1-5.5 are the base text.", "M-07")]),
    dict(file="M09-sec6.md", change="M-09", sec="6", ranges=[(1155, 2807)],
         heading="### 6.13 Run 1 conflict blocks",
         marker="<!-- M-08 insertion point: the 6.13 disposition table (written by another executor) is the first block inside 6.13 (plan M-08 Target); the M-09 head note follows it -->",
         lead=[new("Run 1's status labels are its own; run 2's UNDECIDABLE-BY-EVIDENCE classification governs (Appendix C "
                   "X-052). Ordering words in this block (for example 'build toward Option B through Option A's code', "
                   "V1:2622) are run 1's recommendation, not an order of work in this document.", "M-09")],
         after={2381: ["", READONLY_NOTE + " <!-- Variant 1 (modified) — correction inserted per M-25 (M-24 item 5) -->"]}),
    dict(file="M11-sec7.md", change="M-11", sec="7", ranges=[(2809, 3098)],
         heading="### 7.4 Run 1 recommendation and architecture (recorded alternative)",
         lead=[new("Run 2's adjudicated recommendation governs; this block is run 1's recommendation, kept as the recorded "
                   "one-engine alternative and for its exposure list and blockers table, which run 2 does not have in this "
                   "form. The V1 advocate holds that the core-shape difference is a label (MERGE/BOTH); the V2 advocate "
                   "holds V2 (C-076, unresolved). Ordering words in this block are run 1's recommendation, not an order of "
                   "work in this document.", "M-11")]),
    dict(file="M14-sec8-inventory.md", change="M-14", sec="8", ranges=[(3105, 3821)],
         heading="### 8.3 Run 1 value inventory (698 rows)",
         lead=[new("These 698 rows are not de-duplicated against run 2's 5,950 rows because the units differ: run 1 has 698 "
                   "consolidated items from 13 research files and the scope slices; run 2 has 5,779 ledger rows plus 171 "
                   "defect-register rows. De-duplication is a task for the later plan (R25-INV-020).", "M-14")]),
    dict(file="M16-sec8-migration.md", change="M-16", sec="8", ranges=[(3822, 3908), (3910, 4030)],
         heading="### 8.4 Run 1 migration content",
         extra_prov="<!-- Variant 1 (modified) — V1:3829, 3860, 3879, 3897 (`**Dependencies:**`) deleted as ordering content; V1:3830, 3861, 3880, 3898 carried only in 8.6 (M-18); leading status column added (R25-INV-027) -->",
         lead=[new("Run 1's in-cell prerequisite notes are logical prerequisites as run 1 defines them at its 8.2 lead, not an "
                   "order of work. The first column of each step table gives the step's status against the adopted design, "
                   "copied from the fault-finder enumeration (R25-INV-027): 13 CONFLICTS, 14 PARTLY COMPATIBLE, 21 "
                   "COMPATIBLE. The four `**Dependencies:**` lines of run 1's track introductions are dropped as ordering "
                   "content, and its four persisted-format and rollback lines are carried only in 8.6.", "M-16")],
         after={3912: ["", new("This gap-coverage table keys on run 1 step ids (R1-M1-01 and so on), so each step it names "
                               "carries the status given in the first column of the step tables above.", "M-16")]}),
    dict(file="M17-sec8-gates.md", change="M-17", sec="8", ranges=[(4031, 4056)],
         heading="### 8.5 Run 1 no-regression gates",
         lead=[new("Run 1's 19 gates carry the prefix `R1-`: R1-G1..R1-G11, R1-G-all, R1-G-bench, R1-G-exit, R1-G-new, "
                   "R1-G-pr, R1-G-replay, R1-G-skills and R1-G-sync. Run 2's gates G1-G27 keep their own numbers, and every "
                   "gate cross-reference in run 2's constraints (C19-C27) and gates (G17-G22) means run 2 numbering "
                   "(R25-INV-018). The \"Must NOT change\" pins of R1-G2 on `test_review_ledger.py:299-304` and `:468-472` "
                   "are conditional on run 1's verdict design, which is not adopted; they belong on the rewrite list of "
                   "run 2's C18 (R25-INV-026).", "M-17")]),
    dict(file="M18-sec8-persisted.md", change="M-18", sec="8", lines=[3830, 3861, 3880, 3898],
         heading="### 8.6 Run 1 persisted-format compatibility and rollback rules",
         lead=[new("Run 1's persisted-format and rollback rules from its four track introductions (V1:3830 for R1-M1, "
                   "V1:3861 for R1-M2, V1:3880 for R1-M3, V1:3898 for R1-M4); they are carried only here, not in 8.4.", "M-18")],
         tail=["", "**Correction (R25-INV-003).** \"Keep the schema string and add optional keys\" is safe only for additive "
               "changes. V2's adopted ledger design changes clearing and verdict semantics, which run 1's own debate "
               "(R1-C13-22 R1-INV-014, V1:2657) closed with a `min_writer` field and a `review-ledger/2` bump; an old "
               "installed binary would clear rows by silence on a new ledger and raise `KeyError` on `last[\"verdict\"]` "
               "(`ledger.py:363-372`). This is an open decision with both versions: <!-- Source: new (correction per Change #M-18, R25-INV-003) -->",
               "",
               "- V2 (A-9): keep `review-ledger/1`. <!-- Source: new (M-18) -->",
               "- Run 1 (R1-C13-22 R1-INV-014, V1:2657): a `min_writer` field plus the `review-ledger/2` bump. <!-- Source: new (M-18) -->",
               ""]),
    dict(file="M19-sec8-branch.md", change="M-19", sec="8", ranges=[(4058, 4061)], prov_lines="4057-4061",
         heading="### 8.7 Run 1 branch-structure constraint and facts (options table dropped, M-19)",
         extra_prov="<!-- Variant 1 (modified) — heading V1:4057 \"### 8.4 Branch-structure options\" replaced per M-19; options table V1:4063-4069 (layouts A-E) dropped as a branch plan -->",
         lead=[new("Run 1's five-layout options table (V1:4063-4069) is a branch plan and is not carried; the git "
                   "constraint and the facts are.", "M-19")],
         after={4059: ["", "**The constraint in both reports and for the owner's prefix.** Both reports state it: "
                       "`feat/review-panel` and `feat/review-panel/<name>` cannot both exist, in either creation order "
                       "(run 1 above; run 2 C4, V2:4433). Applied to the owner's chosen prefix: no branch named "
                       "`feat_review-panel` may exist (local, packed or remote-tracking) while any `feat_review-panel/<name>` "
                       "exists; both names are valid alone per `git check-ref-format`; no such refs exist locally or on "
                       "origin (fault-finder row 31). <!-- Source: new (constraint restatement per Change #M-19) -->"]}),
    dict(file="M20-sec8-risk.md", change="M-20", sec="8", ranges=[(4071, 4101), (4103, 4122)], skip={4115},
         heading="### 8.8 Run 1 risk inputs and integration checklist",
         extra_prov="<!-- Variant 1 (modified) — V1:4115 (PR-process item) dropped; V1:4120 clause 'and mark the steps that wait on each' dropped; V1:4116 'the chosen branch layout of 8.4' replaced -->",
         lead=[new("Run 1's 25 rows below are risk inputs, not a risk register (likelihood and impact are qualitative "
                   "readings, as its own lead says). Its integration checklist is carried without the PR-process item "
                   "(V1:4115) and without the clause \"and mark the steps that wait on each\" (V1:4120); the branch item "
                   "(V1:4116) names the branch names of 8.7 instead of a branch layout.", "M-20")]),
    dict(file="M21-sec9.md", change="M-21", sec="9", ranges=[(4125, 4387)],
         heading="### 9.11 Run 1 open questions", lead=[],
         after={4126: ["", LEGEND, "",
                       "In this block `R1-Gn` means gap row n and `R1-C1` to `R1-C3` mean closure effort (V1:4126); closed "
                       "items carry `R1-CLS-nn`. <!-- Source: new (9.11 id note, rule 3) -->"]}),
    dict(file="M22-sec10.md", change="M-22", sec="10", ranges=[(4389, 4476)],
         heading="### 10.A Run 1 evidence trail", lead=[]),
]

# ---------------------------------------------------------------- run
REC = {"main": [], "ranges": [], "exempt": []}
CREC: list = []
edit_log = []
status_log = []
dropped_log = []
inserted_log = []
block_stats = []
self_check = []
idem_ok = []
collapsed: list = []


def tag_line(s: str, comment: str) -> str:
    c = f" <!-- {comment} -->"
    if s.startswith("|") and s.rstrip().endswith("|"):
        body = s.rstrip()
        return body[:-1].rstrip() + c + " |"
    return s + c


def demote(s: str) -> str:
    m = re.match(r"^(#{3,4}) (.*)$", s)
    if not m:
        assert not re.match(r"^#{1,2} |^#{5,} ", s), s
        return s
    txt = m.group(2)
    pre = "R1 " if txt[:1].isdigit() else ""
    return "#" * (len(m.group(1)) + 1) + " " + pre + txt


edits_by_line: dict[int, list] = {}
for e in EDITS:
    edits_by_line.setdefault(e[0], []).append(e)

for B in BLOCKS:
    if "lines" in B:
        nums = list(B["lines"])
    else:
        nums = [n for a, b in B["ranges"] for n in range(a, b + 1)]
    skip = set(B.get("skip", set())) | set(DELETED) | (set(MOVED) if B["change"] != "M-18" else set())
    for n in nums:
        if n in DELETED:
            dropped_log.append((n, B["change"], DELETED[n], L(n)))
        elif n in MOVED and B["change"] == "M-16":
            dropped_log.append((n, B["change"], f"moved: carried only in 8.6 (M-18), track {MOVED[n]} rule", L(n)))
        elif n in B.get("skip", set()):
            dropped_log.append((n, B["change"], "PR-process checklist item dropped (M-20; PR plan out of scope)", L(n)))
    nums = [n for n in nums if n not in skip]
    # idempotence check on the id pipeline (steps 1-3) for this block
    once = [ids(n, L(n)) for n in nums]
    twice = [ids(n, s) for n, s in zip(nums, once)]
    changed_twice = sum(1 for a, b in zip(once, twice) if a != b)
    idem_ok.append((B["file"], len(nums), changed_twice))
    assert changed_twice == 0, (B["file"], changed_twice)
    # real run with recording
    body = []
    for n in nums:
        s = ids(n, L(n), REC, CREC)
        # step 4: corrections and per-change edits
        for (_, old, newt, ch, note) in edits_by_line.get(n, []):
            assert s.count(old) == 1, (n, old, s[:200])
            before = s
            s = s.replace(old, newt)
            s = tag_line(s, f"Variant 1 (modified) — {ch}: {note.split(' (checked')[0]}") if n not in FENCE else s
            edit_log.append((n, B["change"], ch, old, newt, note))
        if n in LINES43:
            m = RE43.search(s)
            assert m, (n, s[:200])
            s = s[: m.end()] + UNIT43 + s[m.end():]
            s = tag_line(s, "Variant 1 (modified) — M-25 (M-24 item 7): unit note on run 1's 43 call sites")
            edit_log.append((n, B["change"], "M-25 (M-24 item 7)", m.group(0), m.group(0) + UNIT43, "43 call sites unit note (checked: 52 lines, 11 files, 44 in 8 SKILL.md)"))
        if n == 319:
            s = tag_line(s + CAPTION_319, "Variant 1 (modified) — M-25: caption notes the fence-line correction at V1:305")
        if B["change"] == "M-16":
            sm = re.match(r"^\| R1-(M[1-4]-\d\d) \|", s)
            if sm:
                step = sm.group(1)
                cls, txt = status_text(step)
                s = "| " + txt + " <!-- Variant 1 (modified): status column added per M-16 --> " + s
                status_log.append((step, cls, txt, n))
            elif s == "| Step | Action | Files | Details | Closes gaps |":
                s = "| Status against the adopted design " + s
            elif s == "|---|---|---|---|---|" and body and body[-1][1].startswith("| Status against the adopted design"):
                s = "|---" + s
        # step 5: heading demotion (M-27)
        s2 = demote(s)
        if s2 != s:
            inserted_log.append((n, B["change"], "heading demoted", L(n), s2))
        s = s2
        body.append((n, s))
        for extra in B.get("after", {}).get(n, []):
            body.append((None, extra))
            if extra:
                inserted_log.append((n, B["change"], "new line inserted after V1 line", "", extra[:160]))
    # assemble
    prov_lines = B.get("prov_lines") or (", ".join(f"{a}-{b}" for a, b in B["ranges"]) if "ranges" in B
                                         else ", ".join(str(x) for x in B["lines"]))
    out = [f"<!-- Source: Variant 1, Section {B['sec']} (lines {prov_lines}) — merged per Change #{B['change']}; ids prefixed R1- -->",
           B["heading"]]
    if B.get("extra_prov"):
        out.append(B["extra_prov"])
    out.append("")
    if B.get("marker"):
        out += [B["marker"], ""]
    for ln in B.get("lead", []):
        out += [ln, ""]
    if B["change"] == "M-14":
        # M-15 marker immediately before the inventory rows' table header
        hdr = next(i for i, (n, s) in enumerate(body) if n is not None and s.startswith("| R1-V-001 |")) - 2
        assert body[hdr][1].startswith("| ") and body[hdr + 1][1].startswith("|---"), body[hdr]
        body.insert(hdr, (None, "<!-- M-15 insertion point: the translation table for run 1 destinations (written by another executor) goes here, immediately before the rows -->"))
        body.insert(hdr + 1, (None, ""))
        inserted_log.append((body[hdr + 2][0] - 1, "M-14", "M-15 insertion marker (HTML comment), directly before the inventory table header", "", ""))
    if B["change"] == "M-18":
        sep = []
        for n, s in body:
            sep += [s, ""]
        out += sep[:-1]
    else:
        bounds = {(b1, a2) for (a1, b1), (a2, b2) in zip(B["ranges"], B["ranges"][1:])}
        prev = None
        for n, s in body:
            if n is not None and prev is not None and (prev, n) in bounds and out[-1] != "" and s != "":
                out.append("")  # one blank line at a seam between two carried ranges
            if s == "" and out and out[-1] == "":
                collapsed.append((B["file"], n))  # never two blank lines in a row
                continue
            out.append(s)
            if n is not None:
                prev = n
    out += B.get("tail", [])
    text = "\n".join(out).rstrip("\n") + "\n"
    (OUT / B["file"]).write_text(text, encoding="utf-8")
    block_stats.append((B["file"], B["change"], prov_lines, len(nums), text.count("\n")))
    # final self-check per block
    lines = text.split("\n")
    a = not any(re.match(r"^## ", x) for x in lines)
    b = ("Closed item R1-C-" not in text) and ("GQ:R1-C-" not in text) and ("GQ R1-C-" not in text) and ("closed item R1-C-" not in text)
    c = all(L(d) not in text for d in DELETED)
    # comment hygiene: no '--' or '->' inside an HTML comment we wrote (the V1 text has no HTML comments)
    for cm in re.findall(r"<!--(.*?)-->", text):
        assert "--" not in cm and "->" not in cm, (B["file"], cm[:120])
    self_check.append((B["file"], a, b, c))

# ---------------------------------------------------------------- global assertions
ck = Counter(k for k, *_ in CREC)
assert ck["list V1:4260-4290"] == 29, ck
assert ck["GQ C-nn / GQ:C-nn"] == 43, ck
assert ck["after 'closed item(s)'"] == 28, ck   # 27 named by the plan + V1:4476 'closed items (C-01'
assert ck["line pin (plan)"] == 3, ck           # V1:173 C-05, V1:238 C-10, V1:4476 C-25
assert ck["line pin (extra, executor)"] == 4, ck
plan_scope = ck["list V1:4260-4290"] + ck["GQ C-nn / GQ:C-nn"] + ck["after 'closed item(s)'"] + ck["line pin (plan)"]
assert plan_scope == 103, plan_scope
assert len(REC["ranges"]) == 37, len(REC["ranges"])
steps = [s for s, *_ in status_log]
assert len(steps) == 48 and len(set(steps)) == 48, len(steps)
want = {f"M1-{i:02d}" for i in range(1, 23)} | {f"M2-{i:02d}" for i in range(1, 11)} | \
       {f"M3-{i:02d}" for i in range(1, 10)} | {f"M4-{i:02d}" for i in range(1, 8)}
assert set(steps) == want
cls = Counter(c for _, c, *_ in status_log)
assert cls == Counter({"COMPATIBLE": 21, "PARTLY COMPATIBLE": 14, "CONFLICTS": 13}), cls
mig = (OUT / "M16-sec8-migration.md").read_text(encoding="utf-8")
d_all = all(re.search(r"^\| (CONFLICTS|PARTLY COMPATIBLE|COMPATIBLE)[^|]*\| R1-" + re.escape(s) + r" \|", mig, re.M) for s in want)
assert d_all
assert all(a and b and c for _, a, b, c in self_check), self_check
assert len(edit_log) == len(EDITS) + len(LINES43)

# ---------------------------------------------------------------- log
fam_counts = Counter(f for _, f, _, _ in REC["main"])
by_fam_first = {}
for n, f, tok, ctx in REC["main"]:
    by_fam_first.setdefault(f, (n, tok, ctx))


def pick(pred, label):
    for n, f, tok, ctx in REC["main"]:
        if pred(n, f, tok):
            return (label, n, tok, "R1-" + tok, ctx.replace("|", "\\|").replace("\n", " "))
    return (label, "-", "(none in carried text)", "-", "-")


spot = [
    pick(lambda n, f, t: f == "DOC-nn", "DOC-"), pick(lambda n, f, t: f == "INV-nnn", "INV-"),
    pick(lambda n, f, t: f == "SC-n", "SC-"), pick(lambda n, f, t: f == "C-nnn", "C-nnn"),
    pick(lambda n, f, t: f == "Cnn-nn", "debate row Cnn-nn"), pick(lambda n, f, t: f == "Mn-nn", "step Mn-nn"),
    pick(lambda n, f, t: f == "G-name", "named gate"), pick(lambda n, f, t: f == "Rnn", "research file Rnn"),
    pick(lambda n, f, t: f == "V-nnn", "inventory V-nnn"), pick(lambda n, f, t: f == "W0n", "web file W0n"),
    pick(lambda n, f, t: f == "H-A..C", "hypothesis H-A"), pick(lambda n, f, t: f == "CI-n", "CI-n"),
    pick(lambda n, f, t: f == "D-n", "decision D-n"), pick(lambda n, f, t: f == "ENS-n", "ENS-"),
    pick(lambda n, f, t: f == "Xn", "exposure Xn"), pick(lambda n, f, t: f == "Q-nn", "question Q-nn"),
]
rng = REC["ranges"][0]
spot.append(("range", rng[0], rng[1], rng[2], "range pre-pass"))
gq = next(x for x in CREC if x[0] == "GQ C-nn / GQ:C-nn")
spot.append(("GQ C- token", gq[1], gq[2], gq[3], "closed-item rename"))
cw = next(x for x in CREC if x[0] == "after 'closed item(s)'" and 3712 <= x[1] <= 3736)
spot.append(("Closed item C- row", cw[1], cw[2], cw[3], "closed-item rename (inventory row)"))
cl = next(x for x in CREC if x[0] == "list V1:4260-4290")
spot.append(("closed list row", cl[1], cl[2], cl[3], "closed-item rename (9.3 list)"))
assert len(spot) == 20

W = []
w = W.append
w("# E2 extraction log (merge executor E2 of 4): transformed Variant 1 blocks")
w("")
w("Status: DONE. Produced by `partials/merge-scripts/e2_v1_extract.py` (run with `uv run --no-project python`). "
  "Source: `variant-1-original.md` (read only). Plan: `refactor-plan.md` with reviews 2 and 3 (rule 3). "
  "All assertions in the script passed (counts, idempotence, 48 statuses, self-check).")
w("")
w("## 1. Blocks written")
w("")
w("| File | Change | V1 lines | V1 lines carried | Output lines |")
w("|---|---|---|---|---|")
for f, ch, pl, nv, no in block_stats:
    w(f"| `v1-blocks/{f}` | {ch} | {pl} | {nv} | {no} |")
w("")
w("## 2. Id pass test (sample probes, then idempotence)")
w("")
w("| Input | Expected | Output | Second run unchanged |")
w("|---|---|---|---|")
for src, want_, got, ok in probe_rows:
    w(f"| `{src}` | `{want_}` | `{got}` | {'yes' if ok else 'NO'} |")
w("")
w("Idempotence on the real blocks (steps 1-3 run twice on every carried line; lines changed by the second run):")
w("")
for f, nl, ch in idem_ok:
    w(f"- `{f}`: {nl} lines, {ch} changed")
w("")
w("Note: the pass is never run on new text. Run on `R25-INV-004` it would give `R1-R25-INV-004` (`R\\d\\d` matches `R25`); "
  "every new sentence (leads, legend lines, notes, status cells) is added after the pass (step 4).")
w("")
w("## 3. Closed-item rename (rule 3, step 1)")
w("")
w("| Kind | Count |")
w("|---|---|")
for k, v in ck.items():
    w(f"| {k} | {v} |")
w(f"| **plan scope total (list + GQ + after 'closed item' + plan line pins)** | **{plan_scope}** (plan: 103) |")
w("")
w("Reconciliation with the plan's split: the plan counts 27 tokens after the words `closed item` (V1:1529, 1982, 3712-3736) "
  "and 2 line-pinned tokens at V1:4476. The regex `(?i)(closed items?\\s+\\(?)C-(\\d\\d)` also matches V1:4476 "
  "\"25 closed items (C-01\", so the regex gives 28 and the V1:4476 line pin renames only `C-25`. Same 103 tokens.")
w("")
w("**Extra, beyond the plan's 103 (flag for the orchestrator).** V1:3736 (inventory row R1-V-614, \"Closed item C-25: eleven "
  "gaps ... answered by sibling files (C-01, C-02, C-04 to C-12)\") holds 4 more closed-item tokens that the plan's "
  "enumeration does not list. Left to the main pass they would become `R1-C-01` etc. (conflict ids) in the same row "
  "as `R1-CLS-25`, the defect R3-B1 describes; the same list at V1:4290 is renamed by the plan. The script renames them "
  "by a line pin (`EXTRA_PINS` in the script; delete that one entry to revert). Total renamed: "
  f"{sum(ck.values())}.")
w("")
w("Left unchanged and logged: V1:3107 `` `GQ:C-01` to `GQ:C-25` `` (code span, protected). V1:2827 \"(C-01 Cons\" and "
  "V1:3841 \"(C-05 Option D\" are conflicts and go to the main pass (`R1-C-01`, `R1-C-05`). V1:114 legend `C-nn` is a "
  "placeholder in a code span.")
w("")
w("All renames:")
w("")
w("| V1 line | Kind | Before | After |")
w("|---|---|---|---|")
for k, n, a, b in CREC:
    w(f"| {n} | {k} | `{a}` | `{b}` |")
w("")
w("## 4. Range pre-pass (rule 3, step 2)")
w("")
w(f"{len(REC['ranges'])} ranges (plan: 37). Each is a mechanical edit.")
w("")
w("| V1 line | Before | After |")
w("|---|---|---|")
for n, a, b in REC["ranges"]:
    w(f"| {n} | `{a}` | `{b}` |")
w("")
w("## 5. Main id pass (rule 3, step 3): replacements per pattern")
w("")
w("| Family | Pattern | Count |")
w("|---|---|---|")
for name, p in FAMS:
    w(f"| {name} | `{p}` | {fam_counts.get(name, 0)} |")
w(f"| **total** | | **{sum(fam_counts.values())}** |")
w("")
w("Exempted by line (rule 3: V1:169 `C3` combo run; probe labels M1-M4 at V1:2704, 2729, 2761):")
w("")
for n, t in REC["exempt"]:
    w(f"- V1:{n} `{t}` kept bare")
w("")
known = [(159, "G3"), (167, "G2"), (167, "G3"), (4270, "G4"), (4270, "X3"), (4170, "D5")]
w("Prefixed tokens whose run 1 meaning is not the family meaning (kept prefixed, as the plan's final rule 3 does not "
  "exempt them; review 3 r3-m3 allowed either): ")
w("")
for n, t in known:
    hit = [x for x in REC["main"] if x[0] == n and x[2] == t]
    if hit:
        w(f"- V1:{n} `{t}` -> `R1-{t}` (context: \"{hit[0][3].strip()}\")")
w("- 9.11 closure-effort tags `C1`-`C3` -> `R1-C1`..`R1-C3`; the 9.11 note line states this meaning (rule 3).")
w("")
w("## 6. Protected spans")
w("")
w(f"- Code spans: {PROT_COUNTS['code span']}; URLs: {PROT_COUNTS['URL']}; `file.ext[:line]` cites: {PROT_COUNTS['file cite']} "
  "(counted on carried lines outside fences, after the pre-pass).")
w(f"- Fenced blocks (protected whole; the legend lines cover their ids): {', '.join(f'V1:{a}-{b}' for a, b in FENCE_RANGES)}.")
w("- Exception: the M-25 correction at V1:305 edits a fence line on purpose (step 4, not the id pass).")
w("")
w("## 7. Spot check (20 replacements)")
w("")
w("| Type | V1 line | Before | After | Context |")
w("|---|---|---|---|---|")
for lab, n, a, b, ctx in spot:
    w(f"| {lab} | {n} | `{a}` | `{b}` | {ctx} |")
w("")
w("## 8. Lines dropped, moved or excluded")
w("")
w("| V1 line | Change | Why | Text (start) |")
w("|---|---|---|---|")
for n, ch, why, t in dropped_log:
    w(f"| {n} | {ch} | {why} | `{t[:90].replace('|', '/').replace('`', '')}` |")
w("| 4057 | M-19 | heading replaced by `### 8.7 ...` (tagged Variant 1 (modified)) | `### 8.4 Branch-structure options` |")
w("| 4062-4069 | M-19 | outside the range: layout table A-E is a branch plan (U-099 exemption, M-23) | table |")
w("| 579, 783, 1154, 2808, 4124, 4388 | M-05, M-07, M-09, M-11, M-21, M-22 | V1 H2 lines outside the ranges, replaced by the new `###` headings | `## n.` |")
w("| 4120 (clause) | M-20 | \"and mark the steps that wait on each\" removed (ordering) | see section 10 |")
w("")
w(f"Blank lines: {len(collapsed)} blank V1 lines were not written because the line before was already blank "
  "(range starts after a new lead, double blanks at V1:781-782, 4121-4122 and the like): "
  + ", ".join(f"{f.split('-')[0]}:V1:{n}" for f, n in collapsed) + ". No text line is affected.")
w("")
w("## 9. Step-status assignment (M-16, R25-INV-027)")
w("")
w(f"Counts: {dict(cls)} (asserted 13 / 14 / 21; 48 distinct step ids M1-01..M1-22, M2-01..M2-10, M3-01..M3-09, M4-01..M4-07).")
w("")
w("| Step | V1 line | Status | Cell text |")
w("|---|---|---|---|")
for step, c, txt, n in status_log:
    w(f"| R1-{step} | {n} | {c} | {txt} |")
w("")
w("## 10. Corrections and per-change edits applied (before / after)")
w("")
w("| V1 line | Block | Change | Before | After | Note |")
w("|---|---|---|---|---|---|")
for n, blk, ch, a, b, note in edit_log:
    w(f"| {n} | {blk} | {ch} | {a.replace('|', '/')} | {b.replace('|', '/') if b else '(removed)'} | {note.replace('|', '/')} |")
w(f"| 319 | M-03 | M-25 | caption | caption + `{CAPTION_319.strip()}` | the fence line V1:305 cannot carry an HTML tag |")
w("| 2381 | M-09 | M-25 (M-24 item 5) | - | new paragraph after the line: the read-only correction | flag text per fault-finder row 27 |")
w("")
w("Not corrected (logged): V1:3843 (R1-M1-10) and V1:3855 (R1-M1-22) name `--allowedTools` inside Details cells of 8.4, "
  "which M-16 forbids editing; V1:4170 (R1-Q-35) names it as an untested open question, not as a working restriction. "
  "V1:2347 is the `--disallowedTools` deny list (Option B), not an allowlist claim. The calibrator 5-vs-6 statement and "
  "run 1's \"16 of 20 DECIDED-BY-EVIDENCE\" stay as run 1 states them (M-25). V1:705 (37 attributed to research/12) is "
  "unchanged (M-25).")
w("")
w("## 11. New text inserted")
w("")
w("Every block starts with the provenance comment, the new `###` heading and the lead the plan prescribes (each lead "
  "line tagged `<!-- Source: new (lead per Change #M-nn) -->`). Other inserted lines:")
w("")
for n, blk, what, a, b in inserted_log:
    if what != "heading demoted":
        w(f"- {blk}, after V1:{n}: {what}: {b}")
w("- M-09: M-08 insertion marker (HTML comment) directly after the `### 6.13` heading, before the head note (plan M-08 Target: first block inside 6.13).")
w("- M-18: the R25-INV-003 correction paragraph and the two versions as a list (text of plan M-18).")
w("")
w("Heading demotion (M-27): " + str(sum(1 for x in inserted_log if x[2] == 'heading demoted')) +
  " headings; `###` -> `####` and `####` -> `#####`, with `R1 ` before a heading that starts with a run 1 section "
  "number (for example `#### R1 2.1 E1: ...`, `##### R1 5.1.1 ...`, `#### R1 6.D ...`). Headings that start with an id "
  "or a word are demoted without `R1 ` (for example `#### R1-C-01: ...` after the id pass, `##### Option A: ...`, "
  "`##### Track R1-M1: ...`, `#### Codebase Research`). No V1 H2 line is carried.")
w("")
w("## 12. Plan points not done, or done with a choice")
w("")
w("1. **V1:3736 closed-item tokens**: renamed as an extra line pin (section 3); the plan's count of 103 is kept for its own enumeration. Revert by removing `EXTRA_PINS`.")
w("2. **R1-M4-01 and R1-M4-03 conflict ids**: plan M-16 and R25-INV-027 give no run 2 outcome id for these two CONFLICTS rows (only \"edits `fsm.py`\" / \"edits `severity_router.py`\"). The cell names no id and says so instead of inventing one.")
w("3. **M-06 \"see M-20\"**: the plan says the track names refer to \"see M-20\"; the steps of R1-M1..R1-M4 are in 8.4 (M-16), so the lead points at 8.4. Check whether M-20 was meant.")
w("4. **M-17 \"add those two pins to the rewrite list of V2 C18\"**: that list is base text (run 2 C18), outside this executor's scope; the R1 block and its lead say the pins belong there (R25-INV-026). The base executor must add them to C18.")
w("5. **M-20 V1:4116 text**: the plan's replacement gives \"Confirm the branch names (see 8.7 constraint) does not create ...\"; kept exactly as the plan words it (grammar \"does\" not changed).")
w("6. **M-19 / M-20 residual references to the dropped layouts**: V1:4061 (\"layouts C and D revert ...\", \"This section states layouts and trade-offs only\") and V1:4086 (risk mitigation \"8.4 layout choice\") still mention run 1's layouts; the plan carries them with only the commit-count update, so they are unchanged.")
w("7. **M-15 and M-08 tables**: not written (other executors); HTML-comment insertion markers are placed in `M14-sec8-inventory.md` (immediately before the inventory table header) and `M09-sec6.md` (after the heading).")
w("8. **Legend lines**: added only under the three legends rule 3 names (V1:108-129, 483-492, 4126). Other carried key tables (V1:2810-2817 Section 7 conventions, V1:3109-3116 inventory abbreviations) get none, per the plan.")
w("9. **M-19 ref check**: `git for-each-ref refs/heads refs/remotes` shows no `feat_review-panel*` or `feat/review-panel*` ref (only `ironbelly/eval-tasklist-review-panel`); `git ls-remote origin` was not run (network), so \"on origin\" rests on fault-finder row 31.")
w("10. **Lead of M-22 (10.A)**: the plan prescribes none; none added. M-21 (9.11) has no lead beyond the kept source key, the legend line and the id note.")
w("")
w("Read-only checks run for this log (no writes outside the outputs): `git rev-parse HEAD` (ad8f57560), `git merge-base HEAD origin/master` (d2d8a2d16), "
  "`git rev-list --count d2d8a2d16..HEAD` (5) and `..origin/master` (3), `git rev-parse --short origin/master` (d4d1662a8), "
  "`git diff --stat d2d8a2d16 HEAD -- src tests scripts` (4 files: reflect SKILL.md, refs/reviewer-spec.md, two reflect tests), "
  "`git show 4a22d742...:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/combos/SPEC.md` (line 3: Qwen3.8-max timed out \"on 3 of 4 runs\"), "
  "`src/superclaude/cli/review/findings.py:367-379` (`same_defect`), `src/superclaude/cli/review/ledger.py:363-372` (`verdict()` returns `last[\"verdict\"]`), "
  "`src/superclaude/cli/pipeline/process.py:140-160` (`reviewer_profile`), `grep -rEn 'subagent_type: *\"?rf-' src/superclaude/skills` (52 lines, 11 files, 44 lines in 8 SKILL.md), "
  "`git for-each-ref` (section 12 item 9), V2:1102 and V2:4433 (read).")
w("")
w("## 13. Final self-check (script)")
w("")
w("| Block | (a) no V1 `## ` line | (b) no `Closed item R1-C-` / `GQ:R1-C-` / `GQ R1-C-` | (c) no deleted `**Dependencies:**` text |")
w("|---|---|---|---|")
for f, a, b, c in self_check:
    w(f"| `{f}` | {'PASS' if a else 'FAIL'} | {'PASS' if b else 'FAIL'} | {'PASS' if c else 'FAIL'} |")
w("")
w(f"(d) all 48 step ids carry a status cell in `M16-sec8-migration.md`: {'PASS' if d_all else 'FAIL'}.")
LOG.write_text("\n".join(W) + "\n", encoding="utf-8")
print("OK", [x[0] for x in block_stats], "main", sum(fam_counts.values()), "ranges", len(REC["ranges"]), "closed", dict(ck))
