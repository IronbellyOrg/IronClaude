"""Render the issue drafts (epics and feature sub-issues) from plain data.

Run from anywhere:  uv run python <this folder>/render.py
Writes ONLY into ../issue-drafts/ (relative to this file). Files already there are
overwritten, so the output is idempotent. Nothing is filed on GitHub.

Data lives in plan_unique.py (hand-written epics and features) and plan_cycles.py
(the validation-cycle and tests-cycle templates). Keep this file free of content.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "issue-drafts"
sys.path.insert(0, str(HERE))

from plan_cycles import cycle_epics  # noqa: E402
from plan_unique import unique_epics  # noqa: E402

REPO = "IronbellyOrg/IronClaude"
UMBRELLA = 727

PREFACE = (
    "Run each step in a fresh context window (the bmad-help skill advises this). The person in "
    "the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD "
    "workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand "
    "(they are derived from the memlog). After each step, tick its box under Progress and "
    "comment on this issue with the output path."
)

HANDOFF_NONE = (
    "No hand-off to IronClaude from this feature. Its output is a document or a decision made "
    "by people with BMAD. If a story appears that needs code or tests, file it as a new feature "
    "under the epic and use the hand-off text of a build feature."
)

HANDOFF_STORIES = (
    "Hand-off (applies once the stories of this feature exist and are ready):\n"
    "1. Gate: `/bmad-check-implementation-readiness` passes and `/bmad-sprint-planning` lists the "
    "stories (status `backlog`, then `ready-for-dev` when handed over).\n"
    "2. Build the hand-off packet FOLDER `.dev/issues/<this-issue>/bmad/` (template "
    "agent1/templates/handoff-packet.md): one index file for the feature plus one self-contained "
    "story file per story (`story-<N>-<M>-<slug>.md`: the story and its acceptance criteria with "
    "stable ids `S<N>.<M>-AC<n>` copied verbatim, the `AD-n` rows that bind it, constraints, paths "
    "it touches or 'new area', complexity, dependencies, previous-story notes).\n"
    "3. The IronClaude coordinator runs its acceptance checklist on the packet and, on the owner's "
    "go, files one sub-issue per story under this feature. Per story, in order, in one feature "
    "worktree: `/sc:spec-panel @<story file>`, then `/sc:workflow <story file> --depth <quick|standard> "
    "--handoff none`, then the owner's plan approval in chat, then `/sc:implement <plan path>` (run by a "
    "person until `/sc:implement` has an unattended mode). After the last story: "
    "`/sc:pr-submit --monitor 3` in a separate top-level session opened in the feature worktree "
    "(not in the coordinator's session), then `/sc:closeout <PR> --issue <N>`. A code-grounded spec "
    "(`/sc:brainstorm` plus `/sc:adversarial`) is added for a story only when a trigger fires. The "
    "exact chain is settled in shared/CONSENSUS.md.\n"
    "4. Write-back, by the coordinator only (workers never write it): packet accepted = "
    "`ready-for-dev`, first implement task started = `in-progress`, PR opened = `review`, PR merged "
    "and closeout done = `done` (never regress); a progress comment on each story issue at each "
    "event; a BMAD story record `<story_key>.md` when the story is implemented; close each story "
    "issue when its acceptance rows pass and the feature issue with its last story."
)

STORY_LABELS_NOTE = (
    "Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; "
    "`/sc:issue` never creates labels, so a person creates them once or the coordinator drops them."
)


def md_list(items, bullet="- "):
    return "\n".join(f"{bullet}{i}" for i in items)


def render_steps(steps):
    out = []
    for n, s in enumerate(steps, 1):
        out.append(
            f"{n}. `{s['cmd']}`\n"
            f"   - Say first: {s['say'] or 'nothing to add; the skill reads the planning artifacts itself'}\n"
            f"   - Produces: {s['out']}\n"
            f"   - Done check: {s['done']}"
        )
    return "\n".join(out)


def render_feature(epic, f, idx):
    nn, mm = epic["n"], idx
    fid = f"EPIC-{nn:02d}-STORY-{mm:02d}"
    labels = ", ".join(["enhancement", f"release:{epic['version']} (new)"] + f.get("labels", []))
    who = f["who"][0].upper() + f["who"][1:]
    handoff =HANDOFF_NONE if f.get("handoff", "stories") == "none" else HANDOFF_STORIES
    if f.get("handoff_extra"):
        handoff += "\n\nFeature-specific: " + f["handoff_extra"]
    progress = [f"[ ] Step {i}: {s['cmd']}" for i, s in enumerate(f["steps"], 1)]
    if f.get("handoff", "stories") != "none":
        progress += [
            "[ ] Stories pass readiness and are in sprint-status.yaml",
            "[ ] Hand-off packet written and accepted by the coordinator",
            "[ ] Story issues filed under this feature",
            "[ ] IronClaude tasklist package created (path recorded here)",
            "[ ] PR merged and `/sc:closeout` done; sprint-status keys at `done`",
        ]
    body = f"""Title: [FEATURE] {f['title']}
Draft id: {fid}
Parent: {epic['draft_id']} ({epic['release']}); grandparent umbrella #{UMBRELLA}
Labels: {labels}
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): {f.get('cx', 'Medium')}
Needs a person in the session: {f.get('human', 'yes (BMAD workflows ask at menus)')}
Status: DRAFT on disk. Do not file until the owner schedules {epic['release']}.
{STORY_LABELS_NOTE}

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #{UMBRELLA} ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: {f['source']}.

Why this feature exists: {f['why']}

## Relevant files and links

{md_list(f['links'])}

## Done when

{md_list(f['done'])}

## Who it is for

{who}

## Start user-story planning (BMAD)

{PREFACE}

Before step 1: read `{epic['draft_id']}` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

{render_steps(f['steps'])}

## Story seeds (turn these into user stories with BMAD; edit freely)

{md_list(f['seeds'], bullet='- ')}

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

{handoff}

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

{md_list(progress, bullet='- ')}
"""
    return fid, f["slug"], body


def render_epic(e, features):
    nn = e["n"]
    feats = [f"`{e['draft_id']}-STORY-{i:02d}` {f['title']}" for i, f in enumerate(features, 1)]
    loop = e.get("loop", True)
    loop_txt = (
        "BMAD run for this epic (details in agent1/RELEASE-PLAN.md S4.2):\n"
        "1. `/bmad-help` to orient.\n"
        "2. `/bmad-correct-course` when the previous cycle changed scope; `/bmad-prd` (Update) when "
        "requirements change; `/bmad-architecture` (Update) when an invariant changes.\n"
        "3. `/bmad-create-epics-and-stories` for this epic only (stories written just in time from the "
        "previous cycle's output; see risk R1 and R2 in the plan).\n"
        "4. `/bmad-check-implementation-readiness`, then `/bmad-sprint-planning`.\n"
        "5. Hand-off per feature (packet, story issues, IronClaude chain), write-back as stories finish.\n"
        "6. `/bmad-sprint-status` any time; `/bmad-retrospective` at epic end."
        if loop
        else e["loop_text"]
    )
    labels = ", ".join(["enhancement", "epic (new)", f"release:{e['version']} (new)"])
    body = f"""Title: [EPIC] {e['title']}
Draft id: {e['draft_id']}
Parent: umbrella #{UMBRELLA} (native sub-issue)
Labels: {labels}
Issue type: Feature
Complexity (proposed): {e.get('cx', 'Complex')}
Release: {e['release']}
Schedule state: {e['schedule']}
Status: DRAFT on disk. Do not file until the owner schedules this release.
{STORY_LABELS_NOTE}

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #{UMBRELLA}. Owner's item, close to verbatim: {e['owner_item']}

State read on 2026-11-22 (so the next person starts from facts): the observer dashboard (`superclaude observe`) is read-only by design and keeps no database; questions live in process memory; the only stored files are an export record and a snapshot under the observer state folder (issue #{UMBRELLA}, section "State read"). The observer code is on origin/master under `src/superclaude/cli/observe/` with tests in `tests/observe/`.

## Relevant files and links

{md_list(e['links'])}

## Done when

{md_list(e['done'])}

## Pick-up note

{e['pickup']}

Do not build anything from this epic before the owner says go (owner's order in issue #{UMBRELLA}). Release 2 prep (EPIC-01) takes precedence over every other epic.

## Features (sub-issues, in order)

{md_list(feats)}

Each feature body names the BMAD workflow that starts its user-story planning and the hand-off to IronClaude.

## How this epic is planned and run

Split of work (proposed in the pipeline; final text in shared/CONSENSUS.md): BMAD owns the higher-level planning (PRD feature groups, architecture invariants, epics, user stories with acceptance criteria, order, the sprint-status ledger). IronClaude owns implementation planning and execution (design brainstorm, `/sc:workflow` tasklist, `/sc:implement`, tests, PR review, closeout) and rapid iteration. IronClaude does not contradict an architecture `AD-n`; a needed change goes back through `/bmad-correct-course`.

{loop_txt}

## Progress

- [ ] Owner scheduled this release (recorded in chat)
- [ ] Epic and feature issues filed; native sub-issue links made
- [ ] Stories written and ready
{md_list([f'[ ] {t}' for t in e['progress_extra']], bullet='- ') if e.get('progress_extra') else ''}
- [ ] All features closed; `/bmad-retrospective` done; open action items filed
"""
    return body


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    epics = sorted(unique_epics() + cycle_epics(), key=lambda e: e["n"])
    index = []
    nfeat = 0
    for e in epics:
        e["draft_id"] = f"EPIC-{e['n']:02d}"
        features = e["features"]
        (OUT / f"{e['draft_id']}-{e['slug']}.md").write_text(render_epic(e, features))
        index.append((e["draft_id"], e["release"], e["title"], len(features), e["schedule"]))
        for i, f in enumerate(features, 1):
            fid, slug, body = render_feature(e, f, i)
            (OUT / f"{fid}-{slug}.md").write_text(body)
            nfeat += 1
    rows = "\n".join(
        f"| {d} | {r} | {t} | {n} | {s} |" for d, r, t, n, s in index
    )
    readme = f"""# Issue drafts (agent 1, bmad-planner), generated {len(epics)} epics and {nfeat} feature sub-issues

DRAFTS ON DISK. Nothing is filed on GitHub. The coordinator files them after the owner reviews shared/CONSENSUS.md.

File naming follows PROTOCOL.md: `EPIC-NN-<slug>.md` is an epic issue; `EPIC-NN-STORY-MM-<slug>.md` is a feature sub-issue of that epic. In the owner's words the sub-issues are the "features"; the BMAD user stories are written later, by the workflow each sub-issue names (see the story layer in agent1/RELEASE-PLAN.md S3.1).

Each file starts with metadata lines (Title, Draft id, Parent, Labels, Issue type, Complexity, Status), then `---`, then the issue body. The body headings follow the house issue template shape (ISSUE-BACKLOG for epics, ISSUE-HANDOFF for features: What was tried, Relevant files and links, Done when, Pick-up note or Who it is for) plus the sections the owner asked for (start user-story planning with BMAD, hand-off to IronClaude, progress). The repo's `/sc:issue --create` feature templates are an alternative shape; the agreed way (shared/CONSENSUS.md (e)) is plain `gh issue create` for these containers.

How the coordinator files a draft (only after the owner reviews and instructs; flags read in `gh issue create --help`, not run): copy the part below the `---` line into a body file, then `gh issue create --repo {REPO} --title "<Title line>" --body-file <body file> --parent <parent number>` (epics: `--parent {UMBRELLA}`; features: the epic's number). Labels marked (new) need creating once or dropping.

Repo labels that exist today (read with `gh label list --repo {REPO}`): bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix. Labels marked (new) in the drafts do not exist yet.

Regenerate: `uv run python agent1/tools/render.py` (data in agent1/tools/plan_unique.py and plan_cycles.py).

| Draft id | Release | Title | Features | Schedule state |
|---|---|---|---|---|
{rows}
"""
    (OUT / "README.md").write_text(readme)
    print(f"epics={len(epics)} features={nfeat}")


if __name__ == "__main__":
    main()
