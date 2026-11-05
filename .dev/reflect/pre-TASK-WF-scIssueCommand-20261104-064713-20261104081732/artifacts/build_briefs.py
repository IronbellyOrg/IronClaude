"""Step 3B.0: materialize the three self-contained reviewer briefs (refs/reviewer-spec.md).

Usage: uv run --no-project python -I build_briefs.py <repo_root> <out_dir> <pkg_rel>
Every excerpt is copied verbatim from disk; nothing is paraphrased.
"""

import json
import re
import sys
from pathlib import Path


def lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def hunk(rel, all_lines, start, end, lang="markdown"):
    body = "\n".join(all_lines[start - 1:end])
    return f"### {rel}:{start}-{end}\n\n````{lang}\n{body}\n````\n"


def card_section(card, title):
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", card, flags=re.S | re.M)
    return f"### {title} (verbatim from t1-card.md)\n{m.group(1)}" if m else ""


def main(root, out, pkg):
    root, out = Path(root), Path(out)
    spec_rel = f"{pkg}/source.md"
    plan_rel = f"{pkg}/{Path(pkg).name}.md"
    spec, plan = lines(root / spec_rel), lines(root / plan_rel)
    card = (out / "t1-card.md").read_text(encoding="utf-8")
    matrix = json.loads((out / "artifacts/coverage-matrix.json").read_text(encoding="utf-8"))["matrix"]
    state = (f"codegraph run state: index_state=fresh checked_at=2026-11-04T07:10:00Z "
             f"worktree_root={root} projectPath={root}\n")

    def slice_table(rows):
        head = "| Requirement | Citation | Method | Best task | Ratio |\n|---|---|---|---|---|\n"
        return head + "".join(
            f"| {r['requirement_id']}: {r['quote'].replace('|', '/')} | {r['citation']} | "
            f"{r['match_method']} | {r['best_task']} | {r['ratio']} |\n" for r in rows)

    starts = [i + 1 for i, l in enumerate(spec) if l.startswith("## ")]
    spec_hunks = hunk(spec_rel, spec, 1, starts[0] - 1)
    for i, s in enumerate(starts):
        e = (starts[i + 1] - 1) if i + 1 < len(starts) else len(spec)
        spec_hunks += "\n" + hunk(spec_rel, spec, s, e)

    unmapped = [r for r in matrix if r["match_method"] == "none"]
    common = ("Read-only reviewer. Audit the supplied hunks and matrix; you may Read/Grep/Glob the repo. "
              "Run nothing. Return findings only.\n\n")
    briefs = {
        1: ("analyzer", card_section(card, "Deviation / risk section"),
            hunk(plan_rel, plan, 17, 26) + "\n" + hunk(plan_rel, plan, 203, len(plan)) + "\n"
            + hunk(spec_rel, spec, 465, 476), unmapped),
        2: ("qa", card_section(card, "Coverage section"),
            "Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any "
            "requirement-bearing span absent from the matrix (parsed or inferred) as a finding.\n\n"
            "Coverage matrix artifact: " + str(out / "artifacts/coverage-matrix.json") + "\n\n" + spec_hunks,
            matrix),
        3: ("refactorer", card_section(card, "Structural section"),
            hunk(plan_rel, plan, 1, len(plan)), [r for r in matrix if r["match_method"] != "none"]),
    }
    (out / "reviewer-briefs").mkdir(exist_ok=True)
    for n, (persona, excerpt, hunks, rows) in briefs.items():
        text = (f"# Reviewer {n} brief (persona: {persona})\n\n{common}"
                f"## T1 card excerpt\n\n{excerpt}\n## Grounding hunks\n\n{state}\n{hunks}\n"
                f"## Coverage slice\n\n{slice_table(rows)}")
        (out / f"reviewer-briefs/reviewer-{n}.md").write_text(text, encoding="utf-8")
        print(n, persona, len(text.splitlines()), "lines")


if __name__ == "__main__":
    main(*sys.argv[1:4])
