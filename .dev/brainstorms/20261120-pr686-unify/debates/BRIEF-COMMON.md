# Common brief for every debate agent (read this first)

You settle ONE topic by an adversarial debate between the owner's line of work ("OURS") and Clay's line of work ("CLAY"). Use "they" for Clay (no source gives pronouns). The repository owner is GitHub login `ironbelly`; Clay is `clayphi`.

## Weighting rule (owner order)
The owner's work and designs take precedence and carry more weight. Concretely: OURS wins unless CLAY shows a clear, evidenced benefit (a capability OURS lacks, a verified defect in OURS, a verified lower risk or cost). If the evidence is a tie, OURS wins. A clear CLAY benefit that is separable from the contested rule is adopted as a HYBRID (take the benefit, keep our rule). Do not call something a conflict, a defect or a benefit without a cited source. Mark anything unverified as UNVERIFIED and do not let it decide the outcome.

## Read first
1. /home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/FULL-REPORT.md and, in the same folder, H-design681-map.md (map of Clay's merged design, line references D:nnn are to `docs/designs/orchestrator.md`), E-pr682.md (what PR 682 deleted), F-clay-inventory.md, G-history.md.
2. Your topic block in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/TOPICS.md.
3. The code and documents your topic names. READ-ONLY exports (plain folders, not git worktrees): /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6; includes Clay's merged design doc and PRs 681-684), /home/coder/.cache/ic-snap-20261120/pr-a (Clay's PR 686 head 8e5ae29ad), /home/coder/.cache/ic-snap-20261120/pr-p (branch issue-655-pr-p). The owner's UNPUSHED local work (zero-setup watcher plan and requirements, owner decision records) is in local worktrees: find them with `git -C /home/coder/workspaces/IronClaude worktree list`; the main ones are `claim-handoff-planb` (branch ironbelly/issue-watcher-zero-setup-plan; requirements at .dev/releases/backlog/issue-watcher-zero-setup/requirements.md inside it) and `issue-339-orchestrator-mode` (owner answers in its brainstorm folder). Code removed by PR 682 can be read with `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>`.
4. Reference tech references when present: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/*.md and the Clay PR inventory /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/inventory/clay-prs.md (may still be in progress; use if complete).

## Procedure (follow it exactly)
1. Create the folder DDIR = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/<TOPIC-ID>/ .
2. Write two position papers as files in DDIR: `position-OURS.md` (the strongest honest case for the owner's line) and `position-CLAY.md` (the strongest honest case for Clay's line). Each: the claim, the mechanism, 5 to 10 cited facts (file path with line, PR or issue number, commit), what it costs, what it risks, what it gets right. Write each as if its author were an expert advocate, but never invent a fact. Create each file as a header stub first and then fill it.
3. Invoke the `/sc:adversarial` skill through the Skill tool (skill: "sc:adversarial") with args: `--compare <DDIR>/position-OURS.md,<DDIR>/position-CLAY.md --depth <DEPTH> --unattended --output <DDIR>/adversarial/` where <DEPTH> is the depth your topic block names. Follow that skill exactly as written, including its nested agents. If the Skill tool or the ability to spawn nested agents is not available to you, do NOT pretend: write the file `<DDIR>/BLOCKED.md` saying what was missing, then perform the strongest substitute you can (a written three-round debate in `<DDIR>/debate-manual.md`, each round answering the other side's strongest point) and say in VERDICT.md that the adversarial skill could not run.
4. Read the debate output from disk. Then write `<DDIR>/VERDICT.md` using EXACTLY these headings:
   - `# Verdict <TOPIC-ID>: <title>`
   - `## Question` (the topic question, verbatim from TOPICS.md)
   - `## Winner` (one of: OURS, CLAY, HYBRID; then one sentence)
   - `## Winning recommendation` (what the spec must say, concrete and testable)
   - `## Strongest points` (three for each side, each with its source)
   - `## Clay strengths to adopt` (list; each item: what, why it is clearly better or fills a gap, and how to merge or override. Write `None` if none)
   - `## Our strengths that must be kept` (list)
   - `## Actions` (a table: Action | Type (LOCAL CHANGE / PR KEEP / PR REVERT / PR KEEP-ADAPT / PR CLOSE / DOC / DECISION) | Target (file, PR or issue number) | Order or dependency)
   - `## Implications` (what follows for the watcher, coordinator or orchestrator, dashboard and claim pipeline; what breaks; what the owner must know)
   - `## Confidence` (percent, and what would change it)
   - `## Unverified` (list)
   - `## Debate artifacts` (paths of the adversarial files)
5. Return ONLY: the path of VERDICT.md, the one-word winner, and a two-line summary.

## Hard rules
- Read-only on the repository, the snapshots and every worktree. Write ONLY under your own DDIR (the adversarial skill's own output goes there too).
- NEVER write to GitHub or Orca: no comment, label, merge, close, push, branch, reaction or dispatch. A "PR REVERT" or "PR CLOSE" is a recommendation written in the verdict, not an action you take.
- Any read-only `gh` call must pass `--repo IronbellyOrg/IronClaude` (for `gh api` the path must spell `repos/IronbellyOrg/IronClaude/...`). Never touch SuperClaude-Org. Never print credentials.
- Do not stage or commit anything. UV only for Python (`uv run python`).
- No em dashes; plain English; every PR or issue number is followed by a few words on what it is the first time it appears.
