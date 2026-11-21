"""Deterministic coverage match for the UC-1 reflect run (Step 1B.0 Pass 2 rows).

Reads the spec snapshot and the tasklist, checks every inferred row's quote is
verbatim inside its cited line, applies the containment rule of
refs/coverage-mapping.md (case-fold, fixed stopwords, threshold 0.6, best ratio,
first task wins ties) and writes coverage-matrix.json and coverage-matrix.md.
"""

import json
import re
import sys
from pathlib import Path

PKG = Path(sys.argv[1])
OUT = Path(sys.argv[2])
SPEC = (PKG / "source.md").read_text(encoding="utf-8").splitlines()
PLAN = (PKG / "TASK-WF-specWorktreeClea-20261120-173546.md").read_text(
    encoding="utf-8"
)

STOP = set(
    "a an the and or but of to in on at by for with from as is are was were be been "
    "it its that this these those not no never any all so if then than which who has "
    "have had do does can may must only same into one per each".split()
)

ROWS = [
    (16, "It never uses `--force` on a worktree removal, never `git branch -D`, never `rm`, never pushes to a source repo and never deletes a remote branch."),
    (16, "Its only push goes to the evidence repo."),
    (16, "Tracked edits and commits made after the pull request always keep the worktree."),
    (78, "Dry run is the default for every verb that could remove something; `--apply` is the only way to remove."),
    (82, "Prints a table of every git worktree of every repo of ours, one decision (keep or removable) and one reason per row."),
    (83, "Runs only the evidence step of section 7 on one worktree: copy, push, check against GitHub."),
    (84, "Removes one worktree whose work is safe, run from outside it, usually right after its pull request merges."),
    (85, "Runs the same decision on all worktrees and removes the removable ones."),
    (87, "One row per worktree: repo, folder, branch, in Orca (yes or no), pull request and state, issue(s) and state, idle days, size, saved copy (none needed, saved and checked, or failed), decision and reason."),
    (89, "Each step fails closed: if any step cannot be completed or read back, the worktree is kept and the reason is shown."),
    (91, "Without a `VERIFIED` result the worktree is kept and nothing below happens."),
    (92, "An `unverifiable` or failed close keeps the worktree."),
    (93, "Any change since the save and any process still inside the worktree keeps it."),
    (94, "Never a path that is not in the manifest, never `-d` on a folder as a whole, never a tracked file (decision 2)."),
    (95, "For a worktree Orca lists: `orca worktree rm --worktree id:<id>` without `--force`."),
    (95, "For a worktree Orca does not list (the 13 removable ones today): `git worktree remove <path>` without `--force`."),
    (96, "**Remove the local branch with `git branch -d`, never `-D`.**"),
    (97, "Confirm the folder is gone, `git worktree list` no longer shows it and `orca worktree list` no longer shows it."),
    (99, "In a dry run (no `--apply`) steps 1 to 7 are not run"),
    (102, "a repo whose `origin` belongs to IronbellyOrg or IronbellyGroup, found from `orca repo list` plus `git worktree list` in each repo (so worktrees Orca does not list are covered), wherever they sit"),
    (105, "As a second guard the script skips any worktree whose folder name starts with `orca-port-`, `orca-recipe-` or `orca-pristine-`, or is `orca-old-patched`, even if git lists it."),
    (112, "One Orca automation per Coder workspace, once a day at 2:00 AM Central (08:00 UTC), switched on by that workspace's owner."),
    (112, "The name must not start with `coordinator-`."),
    (116, "The cron string is `0 8 * * *` (UTC)."),
    (124, "Python standard library only, no model call anywhere."),
    (125, "It is a command, not a skill: a skill installs for everyone and would break the opt-in schedule."),
    (126, "The automation definition, written and switched off, modelled on `scripts/merged_pr_log_orca_automation.md`."),
    (131, "a precheck command that exits non-zero makes Orca skip the run and start no agent session."),
    (137, "Name: `worktree-cleanup-daily`. Trigger: `0 8 * * *` (UTC; 2:00 AM Central in winter, decision 11). Status: written, not switched on."),
    (144, "`GH_TOKEN` (never read from a file by the script; it is passed to `gh` and to `git push` through the environment)."),
    (146, "One lock file per repo in the output folder, so two runs cannot remove the same worktree twice; a second run after a removal finds nothing more to do."),
    (148, "Each run writes `<out dir>/prune-<UTC timestamp>.md` (the table) and a `.json` of the same rows"),
    (148, "Exit codes follow Jay's: 0 means the run completed (some worktrees may be kept; read the table), 64 means a usage error or a `retire` of a worktree that is not removable, 69 means a lookup or a removal failed (the table still shows what happened)."),
    (148, "No output names an agent or a model."),
    (150, "Clay switches it on in his workspace and for the first week it only writes the table (no `--apply`)"),
    (154, "A worktree is removed only when ALL eight rules hold."),
    (154, "Every rule fails closed: if the script cannot tell, it keeps the worktree."),
    (158, "It is a linked worktree of one of our repos that this run may touch."),
    (159, "Its own pull request is MERGED."),
    (160, "Nothing was added after the pull request."),
    (161, "The issue it was for is CLOSED."),
    (162, "Nothing unsaved is in it."),
    (163, "Nothing but its own Orca terminals is using it."),
    (164, "It has been idle for at least 7 days and was not created in the last 7 days."),
    (165, "It is not pinned and nobody asked to keep it."),
    (170, "Decision 1 allows `git clean -f -x` for the exact paths saved and verified in the evidence repo and for nothing else"),
    (171, "Close an Orca terminal of a worktree that has not passed every other rule and whose save is not verified."),
    (173, "Run `git worktree prune`, because a missing folder can mean a disk is not mounted (Jay's guard); it reports such a worktree and leaves it."),
    (175, "Create, move or change a file inside a worktree it keeps (the archive step reads and copies; it never edits)."),
    (176, "Read a credential from a file, print a credential, or name an agent or a model in any output."),
    (186, "Needs the merged pull request of rule 2. Without one it refuses (nothing is saved for unmerged work)."),
    (188, "Pack the ignored files under `.dev/` (not `__pycache__`) into `ignored.tar.gz`, split into parts of 85 MB when larger"),
    (188, "Write `saved-paths.txt`, one exact path per line"),
    (188, "Write `MANIFEST.md`: source repo, branch, pull request link and title, merge date, worktree head and pull request head, worktree folder, time saved, count of files, and a SHA-256 of each archive file and of `saved-paths.txt`."),
    (189, "Commit in the evidence repo with the message `archive(<repo>): <date> pr<N> <subject>`."),
    (190, "If the push is refused, repeat from the fetch up to 3 times"),
    (191, "Print `VERIFIED <folder> files=<n>`."),
    (192, "It never overwrites a folder."),
    (194, "`<source-repo>/<pr-author>/<YYYY-MM-DD>_pr<number>_<subject>/`."),
    (212, "after the save is pushed and verified against GitHub, do whatever is needed to make the worktree removable, for the saved untracked and ignored files only."),
    (235, "YES: a names-only secret check before pushing."),
    (244, "They never touch a real worktree. Each case must fail if its rule is removed."),
    (249, "Decision 3: a worktree that passes every rule and has Orca terminals open and a process inside is removed in `--apply` only after `orca terminal close --worktree id:<id> --all` is confirmed"),
    (251, "A squash-merged pull request whose commits are not on the base is judged landed from pull request state, not ancestry."),
    (252, "A pull request that is merged but whose branch was later reused for new commits keeps the worktree."),
    (255, "A test records every command the script runs, in every verb and every branch"),
    (257, "A second run after a removal finds nothing more to do; two runs at once do not both remove the same worktree (one lock per repo)."),
    (259, "No output names an agent or a model (a test greps the table, the summary and the log)."),
    (264, "An ignored archive larger than 85 MB is split into parts that join back to the same bytes."),
    (266, "Two clones pushing different folders at the same time both end up on `origin/main` after the rebase and retry."),
    (268, "Decision 1: exactly the paths in `saved-paths.txt` are cleared (including a name with a space) and nothing else"),
    (269, "Decision 2: a merged worktree with a tracked edit or a commit after the pull request is kept, nothing is cleared, no terminal is closed and nothing is archived by `prune`."),
    (271, "`git worktree remove` without force refuses a worktree with an untracked file and one with a modified tracked file, and removes one that holds only ignored files"),
    (274, "A dry run in Clay's workspace prints a table whose counts match `git worktree list`"),
    (275, "Jay's files that are adapted keep his Apache-2.0 notice and say what was changed"),
    (276, "The regression gate passes: the full test suite, `make lint` and the sync checks that `/sc:pr-submit` runs."),
    (276, "No em or en dashes in new files."),
    (373, "on throwaway worktrees only, and write the findings to `.dev/research/worktree-cleanup-proofs.md`."),
    (375, "registered where the repo lists commands. Reuse the landed check of #668."),
    (376, "A provenance block with Jay's Apache-2.0 notice at the top of the script."),
    (377, "**Retire the manual tool** in the evidence repo (its `tools/archive-workspace.sh` becomes a pointer to the script)"),
    (379, "**Pull request** with `/sc:pr-submit --monitor 3`."),
]


def words(text: str) -> set:
    toks = re.findall(r"[a-z0-9]+", text.casefold())
    return {t for t in toks if t not in STOP}


# Section lines in the snapshot are 1-based and equal the spec line numbers.
bad = []
for i, (ln, quote) in enumerate(ROWS, 1):
    if quote not in SPEC[ln - 1]:
        bad.append((f"INF-{i:03d}", ln, quote[:60]))
if bad:
    print("QUOTE NOT VERBATIM IN CITED LINE:")
    for b in bad:
        print(b)
    sys.exit(1)

tasks = []
for m in re.finditer(r"^## Task (\d+):.*?(?=^## (?:Task|Phase) \d+:|\Z)", PLAN, re.M | re.S):
    tasks.append((int(m.group(1)), words(m.group(0))))

matrix = []
for i, (ln, quote) in enumerate(ROWS, 1):
    w = words(quote)
    best = (0.0, None)
    for tid, tw in tasks:
        ratio = len(w & tw) / len(w) if w else 0.0
        if ratio > best[0] + 1e-12:
            best = (ratio, tid)
    matched = best[0] >= 0.6
    matrix.append(
        {
            "requirement_id": f"INF-{i:03d}",
            "source": "inferred",
            "citation": f"source.md:{ln}",
            "quote": quote,
            "matched_task_ids": [f"Task {best[1]}"] if matched else [],
            "match_method": "containment" if matched else "none",
            "best_ratio": round(best[0], 3),
        }
    )

total = len(matrix)
hit = sum(1 for r in matrix if r["match_method"] == "containment")
un = [r["requirement_id"] for r in matrix if r["match_method"] == "none"]
summary = {
    "parsed_count": 0,
    "inferred_count": total,
    "coverage_pct": None,
    "coverage_pct_union": round(hit / total, 4),
    "unmapped_requirements": [],
    "unmapped_requirements_union": un,
    "S_dev_density": round(len(un) / total, 4),
    "coverage_degraded": "parsed-sparse" if total > 0 else None,
}
(OUT / "coverage-matrix.json").write_text(
    json.dumps({"summary": summary, "rows": matrix}, indent=1), encoding="utf-8"
)
lines = ["# Coverage matrix (UC-1, Pass 2 inferred rows)", ""]
lines.append(f"Parsed rows: 0. Inferred rows: {total}. coverage_pct_union: {summary['coverage_pct_union']}. S_dev_density: {summary['S_dev_density']}.")
lines.append("")
lines.append("| id | cite | matched | method | ratio | quote |")
lines.append("|---|---|---|---|---|---|")
for r in matrix:
    q = r["quote"].replace("|", "\\|")
    lines.append(
        f"| {r['requirement_id']} | {r['citation']} | {', '.join(r['matched_task_ids']) or 'none'} | {r['match_method']} | {r['best_ratio']} | {q} |"
    )
(OUT / "coverage-matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=1))
print("tasks parsed:", len(tasks))
