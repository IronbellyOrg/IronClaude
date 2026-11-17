#!/usr/bin/env python3
"""E4 assembler (merge executor E4 of 4, step 5 of the compare/merge pipeline).

Builds `MERGED-review-panel-unification.md` from the stage files written by E1-E3:
  - base text: partials/merge-stage/base-corrected.md (E1)
  - run 1 blocks: partials/merge-stage/v1-blocks/*.md (E2)
  - new text: partials/merge-stage/new-blocks/*.md (E3)
Blocks are inserted at HEADING ANCHORS of the corrected base, never at line numbers.
Stage files are read only; every text edit E4 makes is an exact, asserted replacement
applied to the in-memory copy and recorded in partials/merge-stage/e4-edits.json.
Outputs: the merged file, partials/merge-stage/e4-blocks.json (block list with output
line ranges, used for Appendix F and by e4_validate.py) and e4-edits.json.

Run: uv run --no-project python partials/merge-scripts/e4_assemble.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ADV = Path(__file__).resolve().parents[2]          # .../adversarial
STAGE = ADV / "partials" / "merge-stage"
OUT = ADV.parent / "MERGED-review-panel-unification.md"
BLOCKS_JSON = STAGE / "e4-blocks.json"
EDITS_JSON = STAGE / "e4-edits.json"

EDITS: list[dict] = []


def read_lines(p: Path) -> list[str]:
    t = p.read_text(encoding="utf-8")
    if t.endswith("\n"):
        t = t[:-1]
    return t.split("\n")


def replace_once(text: str, old: str, new: str, where: str, item: str, why: str) -> str:
    n = text.count(old)
    assert n == 1, f"{where}: expected 1 occurrence of {old[:80]!r}, found {n}"
    EDITS.append({"file": where, "item": item, "why": why, "before": old, "after": new})
    return text.replace(old, new)


def trim(lines: list[str]) -> list[str]:
    a, b = 0, len(lines)
    while a < b and lines[a].strip() == "":
        a += 1
    while b > a and lines[b - 1].strip() == "":
        b -= 1
    return lines[a:b]


# ---------------------------------------------------------------- stage files
def stage_text(rel: str) -> str:
    return (STAGE / rel).read_text(encoding="utf-8")


def edited_stage() -> dict[str, str]:
    t: dict[str, str] = {}
    for p in sorted((STAGE / "v1-blocks").glob("*.md")) + sorted((STAGE / "new-blocks").glob("*.md")):
        t[p.stem[:4].rstrip("-")] = p.read_text(encoding="utf-8")

    # (d) authoritative debate numbers in the Merge Notes (M00)
    k = "M00"
    t[k] = replace_once(
        t[k],
        "| Points resolved (both advocates name the same winner, `Both (merge)` included) | 218 of 234 |",
        "| Points resolved (both advocates name the same winner, `Both (merge)` included) | 220 of 234 |",
        "new-blocks/M00-merge-notes.md", "(d)", "authoritative count: 220 resolved")
    t[k] = replace_once(
        t[k],
        "| Points still split after Round 2 | 10: 3 real label disputes (C-005, C-076, X-051) and 7 artefacts of cluster inheritance (C-010, C-017, C-018, C-020, C-021, C-024, C-025) | same; `invariant-probe.md` R25-INV-004 |",
        "| Points where the advocates still differ after Round 2 | 8: 3 real label disputes on the core shape (C-005, C-076, X-051) and 5 Medium/Low rows where one advocate's explicit Round 1 exception was not mirrored by the other (C-053, C-065, S-044, C-014, C-025) | same; `partials/convergence-r2.md` |",
        "new-blocks/M00-merge-notes.md", "(d)", "authoritative split: 8 points (3 + 5)")
    t[k] = replace_once(
        t[k],
        "| Strict convergence (resolved points only) | 93.2% (218 of 234); 95.7% if the 6 both-open points are counted as agreement; threshold 80% | `partials/matrix.json` (`strict` = 0.93162) |",
        "| Strict convergence (resolved points only) | 94.0% (220 of 234); 96.6% if the 6 both-open points are counted as agreement; 82.5% after Round 1; threshold 80% | `partials/matrix.json` (`strict` = 0.94017); `partials/scoring-matrix.md` |",
        "new-blocks/M00-merge-notes.md", "(d)", "authoritative convergence 94.0% / 96.6%, Round 1 82.5%")
    t[k] = replace_once(
        t[k],
        "| Points won (strict tally) | Variant 1 (run 1) 26, Variant 2 (run 2) 130, Both (merge) 62, Neither 0 |",
        "| Points won (strict tally) | Variant 1 (run 1) 33, Variant 2 (run 2) 123, Both (merge) 64, Neither 0 |",
        "new-blocks/M00-merge-notes.md", "(d)", "authoritative tally 33 / 123 / 64")
    old_split = t[k][t[k].index("How the 10 split points are read"):]
    old_split = old_split[: old_split.index("\n")]
    new_split = (
        "How the 8 split points are read in this document (refactor-plan rule 4, applied to the regenerated matrix). "
        "C-005, C-076 and X-051 are a dispute about labels only on the core shape: the run 1 advocate holds BOTH "
        "(run 1's superset core kept as the documented one-engine target), the run 2 advocate holds \"Variant 2 governing, "
        "run 1 detail carried\" (`partials/r2-advocate-V1.md:167`; `partials/r2-advocate-V2.md:176`). Both positions are "
        "stated where the core shape is discussed (3.6, 7.4). The other 5 are Medium or Low rows where one advocate's "
        "explicit Round 1 exception was not mirrored by the other advocate (run 1 advocate: `partials/r1-advocate-V1.md`, "
        "\"Inherited verdicts and exceptions\"; run 2 advocate: `partials/r1-advocate-V2.md`, \"Inherited points and "
        "exceptions\" and its cluster table): "
        "C-053 (invalid-block unit of loss): run 1 advocate Variant 1, 65% (`partials/r1-advocate-V1.md:247`); run 2 advocate "
        "Variant 2, its CL-02 cluster verdict, no exception for C-053 (`partials/r1-advocate-V2.md:94`). "
        "C-065 (blocking predicate and severity vocabulary): run 1 advocate Variant 1, 55% (`partials/r1-advocate-V1.md:249`); "
        "run 2 advocate Variant 2, its CL-04 cluster verdict (`partials/r1-advocate-V2.md:96`). "
        "S-044 (post-debate re-rating of options): run 1 advocate Variant 1, 55% (`partials/r1-advocate-V1.md:262`); "
        "run 2 advocate Variant 2, its CL-17 cluster verdict (`partials/r1-advocate-V2.md:109`). "
        "C-014 (future consumers, PR code review and rf-qa): run 1 advocate Variant 1, 55% (`partials/r1-advocate-V1.md:259`); "
        "run 2 advocate Both, 60% (`partials/r1-advocate-V2.md:279`). "
        "C-025 (reflect memory writes): run 1 advocate Variant 2, 70% (`partials/r1-advocate-V1.md:254`); run 2 advocate "
        "MERGE, its CL-09 cluster verdict (`partials/r1-advocate-V2.md:101`). "
        "The matrix (`partials/scoring-matrix.md`, `partials/matrix.json`) applies each advocate's Round 1 exception list "
        "over the inherited cluster label (R25-INV-004); with it, C-010 and C-018 are Variant 1, C-017 is Variant 2, and "
        "C-020, C-021 and C-024 are Both (merge) for both advocates. The first line of `partials/consensus-summary.md` "
        "still reads \"224 of 234 = 0.957\" and \"10 points still disputed\"; the regenerated figures are 220 resolved, "
        "226 counting the both-open points (0.966, `partials/convergence-r2.md`) and 8 split (R25-INV-016)."
    )
    t[k] = replace_once(t[k], old_split, new_split, "new-blocks/M00-merge-notes.md", "(d)",
                        "split-point paragraph rewritten for the 8 split points of the regenerated matrix")
    old_caveat = t[k][t[k].index("A further read-only check made for this merge"):]
    old_caveat = old_caveat[: old_caveat.index("\n") + 2]   # paragraph plus the blank line after it
    t[k] = replace_once(t[k], old_caveat, "", "new-blocks/M00-merge-notes.md", "(d)",
                        "E3 caveat removed: the regenerated matrix applies the advocates' exception lists "
                        "(C-053, C-065 now split; C-056, S-039 now Variant 1)")
    t[k] = replace_once(
        t[k],
        "at tiebreaker level 1 run 2 won 130 of 234 points against run 1's 26 (`base-selection.md`, Combined Scoring).",
        "at tiebreaker level 1 run 2 won 123 of 234 points against run 1's 33, with 64 points Both (merge) "
        "(`base-selection.md`, Combined Scoring).",
        "new-blocks/M00-merge-notes.md", "(d)", "tiebreaker numbers 123 / 33 / 64")
    # (b)/(c) of M00 unchanged.

    # (d) disposition table rows that relied on the old matrix (M08)
    k = "M08"
    t[k] = replace_once(
        t[k],
        "C-056: the matrix records Variant 2 (cluster CL-04), but both advocates give Variant 1 in their Round 1 exceptions",
        "C-056 Variant 1: both advocates give Variant 1 in their Round 1 exceptions",
        "new-blocks/M08-disposition-table.md", "(d)", "regenerated matrix records C-056 Variant 1")
    t[k] = replace_once(
        t[k],
        "C-053: the matrix records Variant 2 (cluster CL-02); the run 1 advocate's Round 1 exception gives Variant 1",
        "C-053: unresolved split in the matrix (run 2 advocate: Variant 2, its CL-02 cluster verdict); the run 1 advocate's Round 1 exception gives Variant 1",
        "new-blocks/M08-disposition-table.md", "(d)", "regenerated matrix records C-053 as an unresolved split")
    t[k] = replace_once(
        t[k],
        "C-065: the matrix records Variant 2 (cluster CL-04); the run 1 advocate's",
        "C-065: unresolved split in the matrix; the run 1 advocate's",
        "new-blocks/M08-disposition-table.md", "(d)", "regenerated matrix records C-065 as an unresolved split")

    # (d) Appendix D row R25-INV-016 (M29)
    k = "M29"
    t[k] = replace_once(
        t[k],
        "| Merge Notes (a) (218 resolved; the 6 both-open points counted apart) |",
        "| Merge Notes (a) (220 resolved; the 6 both-open points counted apart, 226 with them) |",
        "new-blocks/M29-appendices-D-E.md", "(d)", "authoritative count 220 / 226")
    # (b) Appendix E row M-24.9: E4 replaced E1's inline note by a pointer
    t[k] = replace_once(
        t[k],
        "| E1 (base line); the M-02 merge addendum (E3) states the same facts |",
        "| E1 (base line; E4 replaced the inline note by a pointer to the merge addendum); the facts are stated once, in the M-02 merge addendum (E3) |",
        "new-blocks/M29-appendices-D-E.md", "(b)", "M-24.9 row follows the de-duplication at V2:108")
    # marker between D and E becomes a separator plus the Source comment of Appendix E
    t[k] = replace_once(
        t[k],
        "<!-- APPENDIX-E -->\n## Appendix E:",
        "---\n\n<!-- Source: new text — merged per Change #M-29 (Appendix E) -->\n\n## Appendix E:",
        "new-blocks/M29-appendices-D-E.md", "assembly", "generator marker replaced by a separator and the Source comment of Appendix E")

    # (d) M22b pointer to the Merge Notes paragraph that was rewritten
    k = "M22b"
    t[k] = replace_once(
        t[k],
        "(see Merge Notes (a) on the inheritance artefacts in `r2-state.json`)",
        "(see Merge Notes (a) on cluster-label inheritance and the advocates' exception lists)",
        "new-blocks/M22b-compare-artifacts-10B.md", "(d)", "pointer follows the rewritten Merge Notes paragraph")

    # M-30 re-scan (validation failure fixed): two inventory rows repeat the X-025 fact that M-25
    # corrected at V1:204 only; rule 8 (verified value wins, other shown in a note) applied as a note.
    k = "M14"
    note = " [corrected per Appendix C X-025: 3 of 4 Qwen runs timed out; a 4th finished]"
    for old in ("Qwen3.8-max timed out 3000 s on 3 of 3 slots (9000 s wasted)",
                "Qwen3.8-max excluded everywhere (3 of 3 slots timed out at 3000 s)"):
        t[k] = replace_once(t[k], old, old + note, "v1-blocks/M14-sec8-inventory.md", "M-30",
                            "X-025 re-scan: rows R1-V-043 / R1-V-098 keep run 1's text with the verified value as a note")
    for vid in ("R1-V-043", "R1-V-098"):
        row = next(ln for ln in t[k].split("\n") if ln.startswith(f"| {vid} |"))
        t[k] = replace_once(t[k], row, row + " <!-- Variant 1 (modified) — E4, M-30 re-scan: X-025 note -->",
                            "v1-blocks/M14-sec8-inventory.md", "M-30", f"provenance tag on {vid}")

    # (c) M20: verb agreement in the plan's replacement text for V1:4116
    k = "M20"
    t[k] = replace_once(
        t[k],
        "Confirm the branch names (see 8.7 constraint) does not create both",
        "Confirm the branch names (see 8.7 constraint) do not create both",
        "v1-blocks/M20-sec8-risk.md", "(c)", "grammar fix of the plan's replacement text")
    t[k] = replace_once(
        t[k],
        "replaced by 'the branch names (see 8.7 constraint)' (text as the plan gives it) -->",
        "replaced by 'the branch names (see 8.7 constraint)' (plan text; verb agreement 'do not create' fixed by E4) -->",
        "v1-blocks/M20-sec8-risk.md", "(c)", "provenance tag records the grammar fix")
    return t


PROMOTED_A = ["A-002", "A-006", "A-008", "A-012", "A-018", "A-019", "A-024", "A-027", "A-036",
              "A-037", "A-038", "A-041", "A-052", "A-055", "A-056", "A-057", "A-058", "A-059"]

# One line per promoted shared assumption that no other new block names (checked by e4_validate.py).
E3_ROWS = [
    ("A-008", "An unwired but named capability is Critical even when the skill text stages it for a later release",
     "4.7 lead (ratings differ on agreed facts); Appendix C X-011 to X-019 (both ratings shown)"),
    ("A-012", "The two gap logs (run 1: 94 open rows; run 2: 555 rows) are internally accurate and not comparable one to one",
     "each log stays with its report (Section 10, Gaps Log; 10.A, Gaps Log); not merged"),
    ("A-018", "The tier lists in `review-tiers.default.json` describe what the gateway can serve",
     "base 2.6 (dispatch, tiers and model identity); run 1's view in 2.10 (R1 2.2); both advocates reject the assumption"),
    ("A-019", "The installed `~/.claude/` variants represent what consumers see",
     "base 2.4 and 6.10 (installed-only variants); run 1's 2.3 is not carried (M-03); both advocates qualify it"),
    ("A-024", "Counts taken from hand-offs or scope slices carry over unchanged",
     "Baseline and Conventions (run 2 does not cite the slices); 2.10 citation key (run 1's slices as run 1's evidence); Appendix E.2"),
    ("A-027", "The skill panel (engine B) is the Tier 2 path the shared core serves, or the core must pick one engine",
     "7.0.2 C-04; 9.12 Part B (post-gate engine)"),
    ("A-037", "The pinned E2 commit is the right baseline",
     "Merge Notes (e); Baseline and Conventions, merge addendum"),
    ("A-038", "The `tests/review` figure \"651 tests\" counts collected tests",
     "Appendix E.2 (651 collected tests)"),
    ("A-041", "Section 6 numbers about the E1 shadow runs are valid for current behaviour",
     "carried with each report's own tag (base Section 6; run 1's 6.13)"),
    ("A-052", "Debates ended `partial` with HIGH invariants open, yet their winners are adopted with the invariants carried as open risks",
     "7.0.2; 9.12 Part A (R25-INV-028); Appendix D"),
    ("A-055", "E2 harness files are read through `git show` at a pinned commit, not modified",
     "Merge Notes (e); Baseline and Conventions, merge addendum"),
    ("A-056", "The inventory destinations agree with the architecture recommended in Section 7",
     "8.3 translation table (run 1 destinations against run 2's adopted design)"),
    ("A-057", "A v2 citation-only finding reaches the shipped merge path and crashes with `KeyError 'anchor'`",
     "Appendix C X-020, X-049, X-053; Appendix E.1 M-24.1 (base sites corrected)"),
    ("A-059", "The counts of rows, gates, constraints and open questions in each report measure the same unit",
     "Appendix E.2 (counts with units)"),
]


def appendix_e3() -> list[str]:
    winners = json.loads((ADV / "partials" / "matrix.json").read_text())["winners"]
    rows = [
        "",
        "### E.3 Promoted shared assumptions not named elsewhere",
        "",
        "<!-- Source: new text — added by E4 (M-30 validation: every promoted shared assumption is addressed) -->",
        "",
        "Of the 18 shared assumptions the compare promoted to debate points, A-002, A-006, A-036 and A-058 are named in "
        "Appendix D (R25-INV-001, R25-INV-019). The others are listed here with the debate verdict "
        "(`partials/matrix.json`) and the place this document handles them; the assumption text is shortened from "
        "`diff-analysis.md`.",
        "",
        "| A id | Assumption | Debate verdict | Where this document handles it |",
        "|---|---|---|---|",
    ]
    for aid, text, where in E3_ROWS:
        rows.append(f"| {aid} | {text} | {winners[aid]} | {where} |")
    return rows


# ---------------------------------------------------------------- headings, slugs, ToC
FENCE = re.compile(r"^\s*(```|~~~)")
HEAD = re.compile(r"^(#{1,6}) (.*)$")


def headings(lines: list[str]):
    """Yield (index, level, text) for ATX headings outside fenced code."""
    in_fence = False
    for i, ln in enumerate(lines):
        if FENCE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEAD.match(ln)
        if m:
            yield i, len(m.group(1)), m.group(2)


def clean_heading(text: str) -> str:
    return re.sub(r"\s*<!--.*?-->\s*", " ", text).strip()


def gh_slug(text: str) -> str:
    t = clean_heading(text)
    t = re.sub(r"`([^`]*)`", r"\1", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = t.lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def slugs_for(lines: list[str]) -> dict[int, str]:
    seen: dict[str, int] = {}
    out: dict[int, str] = {}
    for i, _lvl, text in headings(lines):
        s = gh_slug(text)
        if s in seen:
            seen[s] += 1
            s2 = f"{s}-{seen[s]}"
        else:
            seen[s] = 0
            s2 = s
        out[i] = s2
    return out


def toc_lines(lines: list[str]) -> list[str]:
    sl = slugs_for(lines)
    res: list[str] = []
    h3_parent = ""
    for i, lvl, text in headings(lines):
        txt = clean_heading(text)
        if lvl == 1 or txt == "Table of Contents":
            continue
        if lvl == 2:
            res.append(f"- [{txt}](#{sl[i]})")
        elif lvl == 3:
            h3_parent = txt
            res.append(f"  - [{txt}](#{sl[i]})")
        elif lvl == 4 and (h3_parent.startswith("6.13 ") or h3_parent.startswith("7.4 ")):
            res.append(f"    - [{txt}](#{sl[i]})")
    return res


# ---------------------------------------------------------------- assembly
def main() -> None:
    base_path = STAGE / "base-corrected.md"
    base = read_lines(base_path)
    assert len(base) == 5098, len(base)

    # slug self-check: regenerate run 2's ToC (H2 + H3) from the unmodified run 2 copy and compare
    # with its own ToC (the corrected base differs only by E1's Section 8 retitle)
    v2 = read_lines(ADV / "variant-2-original.md")
    i_toc0 = v2.index("## Table of Contents")
    i_b0 = v2.index("## Baseline and Conventions")
    orig_toc = [ln for ln in v2[i_toc0 + 1:i_b0] if ln.startswith("- ") or ln.startswith("  - ")]
    regen = [ln for ln in toc_lines(v2) if not ln.startswith("    - ")]
    assert regen == orig_toc, "slug function does not reproduce the base ToC"
    assert len(orig_toc) == 88

    # base edit (a) M-17: two R1-G2 pins appended to the rewrite list of run 2's C18
    c18 = [i for i, ln in enumerate(base) if ln.startswith("| C18 |")]
    assert len(c18) == 1
    i = c18[0]
    old = " with no prompt-file change. [ADJUDICATED CONDITION] |"
    assert base[i].count(old) == 1
    new = (" with no prompt-file change. [ADJUDICATED CONDITION] Merge addition: the rewrite list also takes "
           "`tests/review/test_review_ledger.py:299-304` and `:468-472`, which run 1's gate R1-G2 pins as "
           "\"must NOT change\" only under run 1's verdict design, which is not adopted (8.5; R25-INV-026). |")
    before = base[i]
    base[i] = base[i].replace(old, new) + " <!-- Source: Base (original, modified) — M-17: run 1 R1-G2 pins, R25-INV-026 -->"
    EDITS.append({"file": "base-corrected.md (V2:%d, C18)" % (i + 1), "item": "(a)", "why": "M-17: R1-G2 pins added to C18 rewrite list",
                  "before": before, "after": base[i]})

    # base edit (b): E1's M-24 item 9 note at V2:108 becomes a one-line pointer (the M-02 addendum states the facts)
    i = 107
    s = base[i].index("[Compare-merge baseline note:")
    e = base[i].index("either report.]", s) + len("either report.]")
    old_note = base[i][s:e]
    old_tag = "<!-- Source: Base (original, modified) — M-24 item 9: baseline note: origin/master moved, HEAD ad8f57560, e2f2ac268 -->"
    assert base[i].count(old_tag) == 1
    before = base[i]
    base[i] = base[i].replace(old_note, "[Compare-merge baseline note: `origin/master`, HEAD `ad8f57560` and the later E2 commit "
                              "`e2f2ac268` are stated once, in the merge addendum at the end of this section.]")
    base[i] = base[i].replace(old_tag, "<!-- Source: Base (original, modified) — M-24 item 9: pointer to the merge addendum "
                              "(E4 replaced E1's inline note, which repeated the M-02 addendum) -->")
    EDITS.append({"file": "base-corrected.md (V2:108)", "item": "(b)", "why": "duplicate origin/master facts reduced to a pointer",
                  "before": before, "after": base[i]})

    st = edited_stage()

    def blk(key: str) -> list[str]:
        return trim(st[key].rstrip("\n").split("\n"))

    # M08 goes in place of the marker inside M09; M15 in place of the marker inside M14
    m09 = blk("M09")
    mk = [j for j, ln in enumerate(m09) if ln.startswith("<!-- M-08 insertion point")]
    assert len(mk) == 1
    m09 = m09[:mk[0]] + blk("M08") + m09[mk[0] + 1:]
    m14 = blk("M14")
    mk = [j for j, ln in enumerate(m14) if ln.startswith("<!-- M-15 insertion point")]
    assert len(mk) == 1
    m14 = m14[:mk[0]] + blk("M15") + [""] + m14[mk[0] + 1:]
    m29 = blk("M29") + appendix_e3()

    def idx(pred) -> int:
        hits = [j for j, ln in enumerate(base) if pred(ln)]
        assert len(hits) == 1, hits
        return hits[0]

    a_s1 = idx(lambda l: l == "## 1. Problem Statement")
    a_s3 = idx(lambda l: l.startswith("## 3. "))
    a_s4 = idx(lambda l: l.startswith("## 4. "))
    a_s5 = idx(lambda l: l.startswith("## 5. "))
    a_s6 = idx(lambda l: l.startswith("## 6. "))
    a_s7 = idx(lambda l: l.startswith("## 7. "))
    a_rat = idx(lambda l: l == "### Rationale: the 11 decision axes")
    a_701 = idx(lambda l: l.startswith("### 7.0.1 "))
    assert a_701 < a_rat
    a_s8 = idx(lambda l: l.startswith("## 8. "))
    a_s9 = idx(lambda l: l.startswith("## 9. "))
    a_s10 = idx(lambda l: l.startswith("## 10. "))
    a_apA = idx(lambda l: l.startswith("## Appendix A"))

    def ip(j: int) -> int:
        """Insertion point before heading j: before its blank lines and a `---` separator."""
        while j > 0 and base[j - 1].strip() == "":
            j -= 1
        if base[j - 1].strip() == "---":
            j -= 1
        return j

    parts: list[dict] = []

    def add(name, kind, lines, source=None):
        parts.append({"name": name, "kind": kind, "lines": trim(lines), "source": source})

    def base_part(name, a, b):
        seg = base[a:b]
        lines = []
        segt = trim(seg)
        if segt and segt[0] == "---":
            lines += ["---", ""]
            segt = trim(segt[1:])
        lines += [f"<!-- Source: Base (original), V2:{a + 1}-{b} (lines tagged `Base (original, modified)` carry in-place corrections) -->", ""] + segt
        add(name, "base", lines, f"Base (original), V2:{a + 1}-{b}")

    m00 = blk("M00")
    assert m00[1].startswith("<!-- Provenance:") and m00[2].startswith("<!-- Base:") and m00[3].startswith("<!-- Merge date:")
    i_title = m00.index("# Technical Research Report: Unified Central Review Panel (merged from run 1 and run 2)")
    i_mn = m00.index("## Merge Notes")
    add("Provenance header", "new", m00[1:4], "provenance header (skill format)")
    add("Title", "new", [m00[0], "", m00[i_title]], "new text — M-00 (title)")
    add("Title metadata", "base", ["<!-- Source: Base (original), V2:2-8 (title line V2:1 replaced by the M-00 title) -->", ""] + trim(base[1:8]),
        "Base (original), V2:2-8")
    add("Merge Notes", "new", ["<!-- Source: new text — merged per Change #M-00 (Merge Notes) -->", ""] + m00[i_mn:], "new text — M-00")
    add("Table of Contents", "script", ["---"], "script")      # placeholder, filled below
    base_part("Baseline and Conventions", idx(lambda l: l == "## Baseline and Conventions"), ip(a_s1))
    add("Baseline addendum (M-02)", "new", blk("M02"), "new text — M-02")
    base_part("1. Problem Statement; 2. Current State Analysis (2.1-2.9)", ip(a_s1), ip(a_s3))
    add("2.10 Run 1 current-state material", "v1", blk("M03"))
    base_part("3. Target State (3.1-3.5)", ip(a_s3), ip(a_s4))
    add("3.6 Run 1 target-state material", "v1", blk("M04"))
    base_part("4. Gap Analysis (4.1-4.6)", ip(a_s4), ip(a_s5))
    add("4.7 Run 1 gap rows", "v1", blk("M05"))
    add("4.8 Run 1 contradictions and track coverage", "v1", blk("M06"))
    base_part("5. External Research Findings (5.1-5.5)", ip(a_s5), ip(a_s6))
    add("5.6 Run 1 external findings", "v1", blk("M07"))
    base_part("6. Options Analysis (6.1-6.12)", ip(a_s6), ip(a_s7))
    add("6.13 Run 1 conflict blocks (with 6.13.0 disposition table, M-08)", "v1", m09)
    base_part("7. Recommendation (head, 7.0, 7.0.1)", ip(a_s7), ip(a_rat))
    add("7.0.2 Status of the 15 adjudicated outcomes", "new", blk("M10"), "new text — M-10")
    base_part("7. Recommendation (Rationale to 7.3)", ip(a_rat), ip(a_s8))
    add("7.4 Run 1 recommendation and architecture", "v1", blk("M11"))
    base_part("8. Value Inventory ... (8.1, 8.2)", ip(a_s8), ip(a_s9))
    add("8.3 Run 1 value inventory (with translation table, M-15)", "v1", m14)
    add("8.4 Run 1 migration content", "v1", blk("M16"))
    add("8.5 Run 1 no-regression gates", "v1", blk("M17"))
    add("8.6 Run 1 persisted-format compatibility and rollback rules", "v1", blk("M18"))
    add("8.7 Run 1 branch-structure constraint and facts", "v1", blk("M19"))
    add("8.8 Run 1 risk inputs and integration checklist", "v1", blk("M20"))
    base_part("9. Open Questions (9.1-9.10)", ip(a_s9), ip(a_s10))
    add("9.11 Run 1 open questions", "v1", blk("M21"))
    add("9.12 Open items raised by the compare debate", "new", blk("M21b"), "new text — M-21")
    base_part("10. Evidence Trail", ip(a_s10), ip(a_apA))
    add("10.A Run 1 evidence trail", "v1", blk("M22"))
    add("10.B Compare artifacts", "new", blk("M22b"), "new text — M-22")
    base_part("Appendix A and Appendix B", ip(a_apA), len(base))
    add("Appendix C: Contradiction register", "new", ["---", ""] + blk("M28"), "new text — M-28")
    add("Appendices D and E", "new", ["---", ""] + m29, "new text — M-29 (E.3 added by E4)")
    add("Appendix F: Provenance index", "script", ["---"], "script — M-27, M-29")   # placeholder

    for p in parts:
        if p["source"] is None:
            first = next(ln for ln in p["lines"] if ln.strip())
            m = re.match(r"<!-- Source: (.*?) -->", first)
            assert m, f"{p['name']}: no Source comment"
            p["source"] = m.group(1)

    def appendix_f(positions: list[tuple[int, int]] | None) -> list[str]:
        lines = ["---", "", "<!-- Source: script — generated by partials/merge-scripts/e4_assemble.py per Changes #M-27 and #M-29 -->", "",
                 "## Appendix F: Provenance index", "",
                 "Generated by `adversarial/partials/merge-scripts/e4_assemble.py` from its own block list. Line numbers are lines "
                 "of this merged file; `V2:a-b` are lines of run 2's report before the merge (the corrected base keeps run 2's line "
                 "numbers), and the run 1 ranges are lines of run 1's report.", "",
                 "### F.1 Merged parts and their sources", "",
                 "| # | Merged part | Lines in this file | Kind | Source |", "|---|---|---|---|---|"]
        for n, p in enumerate(parts, 1):
            rng = f"{positions[n - 1][0]}-{positions[n - 1][1]}" if positions else "0-0"
            kind = {"base": "base (run 2)", "v1": "carried run 1 block", "new": "new text", "script": "generated"}[p["kind"]]
            src = p["source"].replace("|", "\\|")
            lines.append(f"| {n} | {p['name']} | {rng} | {kind} | {src} |")
        lines += ["", "### F.2 Run 1 section number to merged heading", "",
                  "Carried run 1 text refers to its own section numbers (for example \"8.3\", \"8.4\", \"6.E.2\", \"7.1.3\"). "
                  "This table maps each run 1 number to the heading that carries it in this document; run 1 headings keep "
                  "their number after the prefix `R1 `.", "",
                  "| Run 1 section | Merged heading |", "|---|---|"]
        static = [
            ("1 (Problem Statement)", "not carried; base Section 1 governs (refactor-plan, Changes NOT made)"),
            ("2 (Current State Analysis)", "2.10 Run 1 current-state material (run 1 2.3 and 2.6 not carried, M-03)"),
            ("3 (Target State)", "3.6 Run 1 target-state material"),
            ("4 (Gap Analysis): gap table", "4.7 Run 1 gap rows"),
            ("4.1 to 4.3", "4.8 Run 1 contradictions and track coverage"),
            ("5 (External Research Findings)", "5.6 Run 1 external findings"),
            ("6 (Options Analysis)", "6.13 Run 1 conflict blocks"),
            ("7 (Recommendation)", "7.4 Run 1 recommendation and architecture (recorded alternative)"),
            ("8 (lead, V1:3099-3104)", "not carried; superseded by the Section 8 lead (M-12)"),
            ("8.1 Value inventory", "8.3 Run 1 value inventory (698 rows)"),
            ("8.2 Migration path", "8.4 Run 1 migration content"),
            ("8.2 track rollback and persisted-format lines", "8.6 Run 1 persisted-format compatibility and rollback rules"),
            ("8.3 No-regression gate list", "8.5 Run 1 no-regression gates"),
            ("8.4 Branch-structure options", "8.7 Run 1 branch-structure constraint and facts (options table dropped, M-19)"),
            ("8.5 Risk register inputs; 8.6 Integration Checklist", "8.8 Run 1 risk inputs and integration checklist"),
            ("9 (Open Questions)", "9.11 Run 1 open questions"),
            ("10 (Evidence Trail)", "10.A Run 1 evidence trail"),
        ]
        for a, b in static:
            lines.append(f"| {a} | {b} |")
        # every carried heading that keeps a run 1 number
        for p in parts:
            if p["kind"] != "v1":
                continue
            top = next(clean_heading(t) for _i, lvl, t in headings(p["lines"]) if lvl == 3)
            for _i, lvl, t in headings(p["lines"]):
                m = re.match(r"R1 (\d+(?:\.[0-9A-Z]+)*) ", clean_heading(t))
                if m and lvl >= 4:
                    lines.append(f"| {m.group(1)} | {clean_heading(t)} (in {top.split(' ')[0]}) |")
        return lines

    # first pass: Appendix F with placeholder positions -> ToC from all headings
    parts[-1]["lines"] = appendix_f(None)

    def join(ps) -> list[str]:
        out: list[str] = []
        for k, p in enumerate(ps):
            if k:
                out.append("")
            out.extend(p["lines"])
        return out

    toc_part = next(p for p in parts if p["name"] == "Table of Contents")
    toc_part["lines"] = ["---", "", "<!-- Source: script — rebuilt per Changes #M-26 and #M-27 from the merged headings -->", "",
                         "## Table of Contents", ""] + ["(placeholder)"]
    doc = join(parts)
    toc = toc_lines(doc)
    toc_part["lines"] = toc_part["lines"][:-1] + toc + ["", "---"]

    # positions, then the real Appendix F (same line count), then re-check positions
    def positions(ps):
        pos, ln = [], 1
        for k, p in enumerate(ps):
            if k:
                ln += 1
            pos.append((ln, ln + len(p["lines"]) - 1))
            ln += len(p["lines"])
        return pos

    pos = positions(parts)
    nF = len(parts[-1]["lines"])
    parts[-1]["lines"] = appendix_f(pos)
    assert len(parts[-1]["lines"]) == nF
    assert positions(parts) == pos
    doc = join(parts)
    assert toc_lines(doc) == toc

    OUT.write_text("\n".join(doc) + "\n", encoding="utf-8")

    # new-text line numbers (for the validator's reference and scope-word scans)
    new_lines: list[int] = []
    for p, (s, e) in zip(parts, pos):
        if p["kind"] in ("new", "script") and p["name"] not in ("Table of Contents", "Appendix F: Provenance index"):
            new_lines += list(range(s, e + 1))
        else:
            for off, ln in enumerate(p["lines"]):
                if "Source: new" in ln or "Merge addition:" in ln or "[Compare-merge baseline note:" in ln:
                    new_lines.append(s + off)
    BLOCKS_JSON.write_text(json.dumps({
        "output": str(OUT),
        "parts": [{"n": n, "name": p["name"], "kind": p["kind"], "source": p["source"], "start": s, "end": e}
                  for n, (p, (s, e)) in enumerate(zip(parts, pos), 1)],
        "new_text_lines": sorted(set(new_lines)),
        "toc_entries": len(toc),
    }, indent=1), encoding="utf-8")
    EDITS_JSON.write_text(json.dumps(EDITS, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT} ({len(doc)} lines, {OUT.stat().st_size} bytes); parts {len(parts)}; ToC entries {len(toc)}; E4 edits {len(EDITS)}")


if __name__ == "__main__":
    main()
