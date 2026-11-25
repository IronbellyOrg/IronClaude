<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

**Design collaboration: [view all twenty embedded previews](https://github.com/IronbellyOrg/IronClaude/blob/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106/PREVIEWS.md) · [download the complete package](https://github.com/IronbellyOrg/IronClaude/raw/refs/heads/docs/409-orca-dashboard-designs/.dev/issues/409/orca-observer-design-package.zip).** The branch is `docs/409-orca-dashboard-designs`; the original22 image attachments remain embedded below.

Create a human-observation terminal companion for Stably.ai Orca in the existing IronClaude/Coder environment. It is not github.com/orca-cli/orca, a scheduler, or a session manager.

**This issue is the human-facing half of the supervision work.** The agent-facing half is Orchestrator mode ([#339](https://github.com/IronbellyOrg/IronClaude/issues/339)). The two are built to show the same facts in the same way (see "Status and summary" and "How the pieces fit" below). Both are read-only.

## Status and summary (updated 2026-11-13)

> **Correction, 2026-11-13 17:05 UTC.** Several statements below say that no observer code exists. That is wrong. A read-only observer, `superclaude observe`, is already on master: Release 1 ([PR #503](https://github.com/IronbellyOrg/IronClaude/pull/503), merged 2026-11-11) and Release 2, a coordinator-questions panel for one named Run with the live read switched off ([PR #514](https://github.com/IronbellyOrg/IronClaude/pull/514)), plus more work on the `409-Phase2` branch. The status table, "Why this is being done", "Plan" and the alignment items below were written without checking it and are being re-checked against it. Treat any sentence that says the observer is not built as stale until this banner is removed.


**Purpose.** One person supervising 5-10 orchestrators and 50-100 sessions cannot tell, from chat, which work needs them, why, and whether a reported result is real. Two pieces attack this from two ends:

1. **Orchestrator mode ([#339](https://github.com/IronbellyOrg/IronClaude/issues/339))** makes the coordinator session the one place sessions report through, and gives it a read-only sweep that sorts every session into a class with proof and writes a dated report. Phase 1 is built and in review ([PR #539](https://github.com/IronbellyOrg/IronClaude/pull/539)).
2. **This issue** is a read-only terminal observer for the human. No observer code exists yet: there are twenty synthetic designs, waiting for a human to choose a direction.

The sweep report in PR #539 is laid out from this issue's design package (the header, the Attention Ledger and the Shift Brief views, and the ten per-session dimensions), so the report and the future observer are meant to say the same thing.

| Piece | State on 2026-11-13 | Where |
|---|---|---|
| Twenty synthetic designs, galleries, fixtures, tests | Done. No direction chosen. No production integration. | Branch `docs/409-orca-dashboard-designs` (commit `495eb96d`; no PR, not merged) |
| Reviewer feedback on which designs help most | Recorded, not yet turned into a chosen design | [comment of 2026-11-11](https://github.com/IronbellyOrg/IronClaude/issues/409#issuecomment-6798967760) and "Requirements from reviewer feedback" below |
| Orchestrator mode Phase 1: `superclaude sweep run`, `/sc:sweep`, skill `sc-sweep-protocol`, WC-16 coordinator-loop rule, routing rows | Built. [PR #539](https://github.com/IronbellyOrg/IronClaude/pull/539) is open. Five review findings: four fixed, one not confirmed (Augment, `probes.py:1047`, left open). | PR #539 |
| CI on PR #539 | One test fails, `tests/core/test_claude_md_worktree_rule.py`, and it already fails on master since #532 ([PR #541](https://github.com/IronbellyOrg/IronClaude/pull/541) fixes it; its checks are green, not yet merged). PR #539 needs a rebase after #541 merges. | PR #541 |
| Supervised-orchestration technical reference | Merged ([PR #532](https://github.com/IronbellyOrg/IronClaude/pull/532)); lists 19 open owner questions (its section 14.3.1) | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` |
| Phase 1 follow-ups and owner-ruled limits | Recorded | [#534](https://github.com/IronbellyOrg/IronClaude/issues/534) |
| Orchestrator mode Phase 2 (sub-orchestrator mode) | Not planned in detail yet. Its plan starts with a preflight phase that reads the owner's reading list. Sub-orchestrator mode is deferred and was never shipped. | Reading list: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/PHASE2-preflight-input.md` (in PR #539); question: [#444](https://github.com/IronbellyOrg/IronClaude/issues/444) |
| Issue watcher (`superclaude issue-watch`) | Merged ([#447](https://github.com/IronbellyOrg/IronClaude/pull/447), [#448](https://github.com/IronbellyOrg/IronClaude/pull/448)), never run live, ships disabled | Rollout: [#450](https://github.com/IronbellyOrg/IronClaude/issues/450) |
| Workspace listener and monitor registration for every Coder workspace | Not built; requirements only | [IronbellyOrg/Coder#477](https://github.com/IronbellyOrg/Coder/issues/477) |
| Orchestrator v2, proactive and holistic | Not started; a separate release after v1 | [#423](https://github.com/IronbellyOrg/IronClaude/issues/423) |

Status words describe what was checked on 2026-11-13: the GitHub state of the issues and PRs above, and the code and tests in PR #539's branch. Nothing in this table claims a live Orca run of the observer; the observer does not exist.

## Problem Statement

One human supervising 5-10 orchestrators and 50-100 sessions/worktrees can miss important decisions, meaningful updates, and evidence in noisy chats. They need to distinguish verified outcomes from activity and understand what needs attention and why.


On the agent side, sessions that are driven by hand do not scale past about 5-6 at once, and a coordinator needs a trustworthy, read-only picture of its sessions before it can act on them ([#339](https://github.com/IronbellyOrg/IronClaude/issues/339)). Both halves need to agree on what each state means.

### Why this is being done, and why this way

**The problem.** Past about 5-6 concurrent sessions, orchestrated work overwhelms the person: the chat is long, the decisions are buried, and a session that says "done" may only be active. The target is 10-20 concurrent sessions per person ([#339](https://github.com/IronbellyOrg/IronClaude/issues/339)). The person needs to know, quickly, what needs them and why, what changed since they last looked, and what evidence backs a claim.

**Why two pieces, and why read-only first.**

- *Sessions should not be driven by hand.* #339 asks that all sessions report through one orchestrator, so the person does not enter each child session. The sweep is that orchestrator's read-only eyes: it classifies sessions only from proof (for example, Orca's own stall proof, never a guess from silence) and says "could not determine" when it has no proof. Phase 1 changes nothing except writing one dated report; every action (close, resume, cleanup) is a later phase, because acting on a wrong guess about someone's unsaved work is the costly mistake.
- *The person needs a view, not another controller.* This issue is a view with inspectable evidence. It does not schedule, spawn, approve or merge, because those belong to Orca and the coordinator, and a second controller would split authority.
- *Activity is not outcome.* The design rules carried into both pieces keep lifecycle, report status, acceptance, tests and approval separate; a dirty worktree is not dangerous, stale is not failed, overlap is not conflict, tokens are not progress, and a missing cost is not zero.

**Why one shared set of facts (proposal, needs an owner decision: see "Alignment decisions").** The sweep already collects and classifies with a deterministic, bounded, tested pipeline and prints a JSON object with a pinned key set (schema version 1, golden-tested). If the observer built its own collector, two programs would classify the same session and could disagree. Reading the sweep's output keeps one definition of "waiting on a person" or "stalled", and keeps the observer free of any LLM polling loop, which this issue already forbids.

**Why a terminal UI.** The work happens in terminals and Coder workspaces (see the Feature Summary: a terminal companion in the existing IronClaude/Coder environment). The preferred stack (Bubble Tea v2, Lip Gloss v2, Bubbles v2) and the alternatives are recorded below under "Design artifacts and frameworks".

**Why it is phased.** Phase 1 (read-only sweep) lets the classification be checked against real sessions before anything acts on it (its `working` class is inert until Orca's agent-wait names are captured; see Plan item 1). Later phases add the actions and the trust layer they need (see "Plan"). The observer follows the human's choice of design, not the other way round.

## User Story

As a human supervising orchestrators, I want a read-only view of attention, affected work, changes, and evidence, so that I can find decisions and inspect their supporting facts without confusing activity with outcomes.

## Proposed Solution

After a human selects a visual direction, develop an observer that shows attention items and reasons, affected missions/orchestrators/sessions/worktrees, meaningful changes since the last look, and evidence freshness and completeness. Permit inspection of underlying evidence and disclose unknown, stale, unavailable, or partial data rather than implying completeness. Keep lifecycle, report status, acceptance, current tests, and human approval distinct. A dirty worktree is not automatically dangerous, stale is not failed, shared paths do not establish a conflict, and inspectable evidence is not admission.

The source-to-dashboard schema is proposed, not an Orca API contract. Complete non-consuming message enumeration, cross-host ownership joins, admission and revision-pinned evidence feeds, accounting coverage, durable event replay and native deep links remain unverified. Orca and coordinator policies retain authority.

### How the pieces fit

```text
 issue watcher (#331 built, #450 rollout)  --starts a claim session-->  project's orchestrator (coordinator)
        ^                                                                   |  creates Tasks, workers report back
 workspace listener + registration (Coder#477, not built)                   v
        routes an approved prompt to the right workspace          Orca (Runs, Tasks, workers, worktrees)
                                                                            |  read-only reads
                                                              superclaude sweep run  (#339 Phase 1, PR #539)
                                                              one dated Markdown report + one JSON object (schema v1)
                                                                    |                         |
                                                    chat summary: counts + path     this observer (read-only; proposed reader of the JSON)
                                                    (coordinator, WC-16)            Orchestrator v2 catalogue (#423) could reuse it too
```

What the sweep reads today (Phase 1, from the design): Orca worker, task and worktree listings, git state of worktrees, the ccsession tab map, session transcripts, and package ledgers; it writes only its own report. It reads no GitHub (GitHub reads are out of Phase 1), no remote hosts, and uses no Orca write verb. The coordinator runs it on every wake or wait timeout, at most once every 5 minutes (WC-16 in `src/superclaude/core/WORKER-CONTRACT.md`).

What the report has today: header and counts, waiting-on-a-person lists, a sessions table with the ten per-session dimensions from this issue (Lifecycle, Phase, Health, Approval, Freshness, Result, Admission, Evidence packet, Policy, Tests/review), worktrees, historical sessions, a Shift Brief and "what I could not determine". The ten dimensions are Markdown table columns only; they are not keys in the JSON (a test pins this), so a reader of JSON v1 does not get them.

### Requirements from reviewer feedback

The [comment of 2026-11-11](https://github.com/IronbellyOrg/IronClaude/issues/409#issuecomment-6798967760) (a reply to the question whether the dashboard is worth the effort) names what would make it useful. Summarized, not quoted; the comment is the source:

- Fleet Quilt and Decision Desk would be most useful, with a plain-English summary of each task or issue: what is done, what is left, and whether it needs the person, plus a link to the PR or issue when one exists.
- Loop Detector or Mission Pulse, showing the agent's path as named steps (for example "Brainstorm", then the next step in the spec), not "Retry 1", coloured green when done, yellow in progress, red failed.
- Signal Bridge as one line per session: Issue (link), PR (link), lifecycle, phase, with colours for running, done, blocked, stuck and at PR; and the ability to click a session to open it.

None of this is built. What exists today that could feed it, and what is missing, is in "Alignment decisions" (items 3 and 4).

### Plan (what comes next)

1. **Finish Orchestrator mode Phase 1.** Merge #541, rebase and merge #539, and decide the one open Augment finding. Work through the follow-ups in [#534](https://github.com/IronbellyOrg/IronClaude/issues/534), including a live read-only capture of Orca's `worker-show` names for agent-wait, so the `working` class and the agent-wait rule (both inert in Phase 1) can be restored.
2. **Orchestrator mode Phase 2: sub-orchestrator mode.** Start with a preflight phase that reads the owner's reading list (technical reference, sub-orchestrator research report, worker contract, [#444](https://github.com/IronbellyOrg/IronClaude/issues/444) material, hooks, Orca's own skills and source). The 19 open owner questions in the technical reference are questions, not decisions. The exempt-chat-reply limit (FIN-F7) is not part of Phase 2.
3. **Later phases, recorded in the Phase 1 research report, not scheduled:** a `/sc:close` command with strict worktree and branch cleanup; resume of timed-out sessions; a trust layer for cross-session messages (narrow, expiring, signed grants; the open questions in the [#339 comment of 2026-11-05](https://github.com/IronbellyOrg/IronClaude/issues/339#issuecomment-6659559030) go to `/tech-research`, and the macaroon-versus-Biscuit choice to an adversarial debate, per the [comment of 2026-11-07](https://github.com/IronbellyOrg/IronClaude/issues/339#issuecomment-6703399956)); an orchestrator of orchestrators; and relaying information to a "management server" (meaning not settled: it may be Orca itself or this observer).
4. **This observer.** A human picks a design direction; the missing source fields are settled (below); then a read-only observer is built against confirmed source contracts. A human selects the direction before production integration (this issue's first acceptance criterion).
5. **Alongside, owned elsewhere:** issue-watcher rollout ([#450](https://github.com/IronbellyOrg/IronClaude/issues/450)); workspace listener and registration ([Coder#477](https://github.com/IronbellyOrg/Coder/issues/477)); Orchestrator v2 after v1 ([#423](https://github.com/IronbellyOrg/IronClaude/issues/423)).

### Alignment decisions that need the owner

Each item names the two things to align and the proposal. None is decided.

1. **Where the observer gets its facts.** Proposal: read the sweep's JSON, not a second collector. Gap: JSON v1 lacks the ten dimensions, PR and issue links, a step flow, and a session-open link. Decide whether to add them to the JSON (an additive change to schema v1, or a v2) or to have the observer parse the report.
2. **Navigation only versus recommendations.** This issue's design contract says the view shows no approval, dispatch, retry or merge actions, even greyed (navigation only). The sweep report prints a "next inspection" line per session and "safe to close" review lines, and the Phase 1 research recorded this as a contradiction for the owner. Decide whether read-only recommendation text is allowed in the observer.
3. **The reviewer's asks versus Phase 1 data.** Plain-English summary, issue and PR links and named steps need GitHub reads and phase data. Phase 1 excludes GitHub reads, and the sweep has no per-session summary text. Decide which phase adds them and whether the sweep or the observer owns them.
4. **Click to open a session.** Native Orca deep links are unverified (see Proposed Solution). Decide the supported way, or disclose that the view cannot open sessions.
5. **Several workspaces and hosts.** The sweep reads one host's Orca and git state; remote hosts are out of Phase 1. Cross-host ownership joins are unverified in this issue. [Coder#477](https://github.com/IronbellyOrg/Coder/issues/477) is the only planned channel between workspaces and a monitor, and its [owner comment of 2026-11-13](https://github.com/IronbellyOrg/Coder/issues/477#issuecomment-6858608150) asks that it align with Orchestrator mode and the TUI panel. Decide whether the observer reads through that registration. The listener routes prompts (a write path); the observer must stay read-only and must never send through it.
6. **One trust design.** The listener's authentication and authorization (Coder#477) and the cross-session trust layer ([#339 comments](https://github.com/IronbellyOrg/IronClaude/issues/339#issuecomment-6659559030)) both need narrow, expiring, auditable grants. Decide one design, not two.
7. **Chat report versus observer.** #339 asks for a static report in chat every 3-5 minutes "taking inspiration" from this issue. Phase 1's chat summary shows counts and the report path only. Decide which surface the person reads first today, and when the observer replaces or complements it.
8. **Orchestrator v2 ([#423](https://github.com/IronbellyOrg/IronClaude/issues/423)).** v2's catalogue of what every agent is doing overlaps what the sweep already collects. Proposal: v2 reuses the sweep's output instead of a third scanner; settle it in v2's brainstorm. Keep the boundary this issue already states: this observer shows the human what happened, v2 shares knowledge between agents.
9. **Watcher-started sessions ([#450](https://github.com/IronbellyOrg/IronClaude/issues/450)).** A session the watcher launches is an ordinary session to the sweep. Decide whether the observer also shows watcher state (what is waiting in the backlog).
10. **The meaning of "management server"** in #339 (relay information to it): Orca, this observer, or something else. Not known yet.

### Design artifacts and frameworks

The current offline design package contains two galleries and ten-page PDF portfolios, two contact sheets, twenty designs, fixture/scenario JSON, source ledger, data dictionary, renderer, tests, and PNG/SVG/ANSI/plain/ASCII exports at 160, 116 and 80 columns. The [complete downloadable package ZIP](https://github.com/IronbellyOrg/IronClaude/raw/refs/heads/docs/409-orca-dashboard-designs/.dev/issues/409/orca-observer-design-package.zip) is now published on the collaboration branch (406 package files plus per-file checksum manifest, 14,438,526 bytes). The designs and records are synthetic and have no live integration. User selection precedes production integration.

Preferred direction is Bubble Tea v2, Lip Gloss v2 and Bubbles v2, informed by TUIBBS-scp styling and components without extracting AGPL code absent license assessment. Its checked manifest snapshot pins Bubble Tea 2.0.6, Lip Gloss 2.0.3 and Bubbles 2.1.0; these are not claims about latest versions. Textual and Ratatui were compared; Wish, Huh and Harmonica are optional, not first-version requirements. Python, Pillow and wcwidth generate the offline previews, not the production implementation.

The historical inspiration includes heavy frames, timelines, heatmaps and meaningful satellite/patch-panel cabling. The remembered original final artwork was not conclusively recovered. These are references, not proof of an implemented report integration:

- [Historical progress-report template](https://github.com/IronbellyOrg/IronClaude/blob/99bdf77d588a73dbf4cb84ec02095ec945e80f0b/.dev/reflect/progress-report-template.md)
- [Historical TUI upgrade handoff](https://github.com/IronbellyOrg/IronClaude/blob/99bdf77d588a73dbf4cb84ec02095ec945e80f0b/.dev/reflect/tui-report-upgrade-brainstorm-handoff.md)
- [Bubble Tea](https://github.com/charmbracelet/bubbletea), [Lip Gloss](https://github.com/charmbracelet/lipgloss), [Bubbles](https://github.com/charmbracelet/bubbles)
- [TUIBBS-scp manifest at the inspected snapshot](https://github.com/IronbellyOrg/TUIBBS-scp/blob/a6d7e7f0a346a44317a1c3fffdd39dc0e14fab59/go.mod)
- Alternatives researched: [Textual](https://textual.textualize.io/), [Ratatui](https://ratatui.rs/)
- Visual grammar: [otel-tui](https://github.com/ymtdzzz/otel-tui), [Dolphie](https://github.com/charles-001/dolphie), [bashtop](https://github.com/aristocratos/bashtop), [btop](https://github.com/aristocratos/btop), [oxker](https://github.com/mrjackwills/oxker)

Use original compositions or properly licensed upstream library APIs, not an unreviewed transplant of third-party application code/assets.

### Design gallery

**Comparison sheets**

![Observation concepts contact sheet](https://github.com/user-attachments/assets/444dd06f-b408-48e1-bc1a-9f1cb838cebc)
![Agent supervision contact sheet](https://github.com/user-attachments/assets/3eea16f2-7e19-4786-95e7-028d921d5f2d)

**First set**

![Signal Bridge](https://github.com/user-attachments/assets/d9e74e71-d150-40a3-af11-6a76219d2d26)
![Fleet Quilt](https://github.com/user-attachments/assets/4ac0aed0-90bd-4196-a38a-0c85916fc33c)
![Time Loom](https://github.com/user-attachments/assets/05cc530b-4f60-4569-ae4d-a9a93b391968)
![Worktree Atlas](https://github.com/user-attachments/assets/cbb8ee77-1204-4bc8-a377-e13d3a7a8796)
![Decision Desk](https://github.com/user-attachments/assets/ac1f8d27-11b2-438d-813c-8467dd21a08e)
![Proof Gate](https://github.com/user-attachments/assets/17e4796e-edc7-4cf3-9c1b-26da01ecda15)
![Budget Engine](https://github.com/user-attachments/assets/8698f9cf-27e0-421f-8dd5-fc3246e9ba26)
![Relay Map](https://github.com/user-attachments/assets/39de1d6a-1d63-41f3-af3b-e7f628346df4)
![Delta Deck](https://github.com/user-attachments/assets/694d34a8-7a71-4017-b6cd-6fb1f6a90153)
![Watchkeeper](https://github.com/user-attachments/assets/6b7050a6-9633-4b47-8070-603bafcf90e8)

**Agent-supervision set**

![Leverage Board](https://github.com/user-attachments/assets/fd42bd55-cefe-4534-95d4-75de9fa355c5)
![Attention Ledger](https://github.com/user-attachments/assets/6dd3117c-b9c0-4e5e-8140-28a251ecf129)
![Handoff Switchboard](https://github.com/user-attachments/assets/35881c71-fba4-45d6-8a8f-547738e1d297)
![Loop Detector](https://github.com/user-attachments/assets/170f27cd-1fe6-44fe-93b2-dca1dd8569a8)
![Collision Lens](https://github.com/user-attachments/assets/30a30dbd-90d8-41b5-9630-37c03578e0f6)
![Outcome Ledger](https://github.com/user-attachments/assets/0a3e7fe5-83c9-4f38-bf10-738ecf552988)
![Revision Drift](https://github.com/user-attachments/assets/4f024a8a-6b7f-43ba-a919-58039fab78ae)
![Mission Pulse](https://github.com/user-attachments/assets/29b94967-eaa5-4870-a0c1-2d3779683a14)
![Owner Load](https://github.com/user-attachments/assets/31eb514e-af87-4fa5-835c-5ce0ed9535d2)
![Shift Brief](https://github.com/user-attachments/assets/757fc4e9-4979-4d9a-ad08-a81358aa5fd2)

The package records 19 passing automated tests and gallery keyboard/state logic exercised by DOM simulation, not a real browser or physical keyboard. Independent review failed earlier snapshots; corrections were applied, but there is no independent post-correction PASS. No performance, live integration, or user-comprehension claim is made.

## Acceptance Criteria

- [ ] A human selects the visual direction before production integration.
- [ ] The observer identifies human attention items and explains why they matter, shows affected scope and meaningful changes since last look, and provides inspection of underlying evidence.
- [ ] The view distinguishes verified outcomes from activity, displays evidence freshness and completeness, and makes missing, stale and partial information explicit.
- [ ] Lifecycle, report status, acceptance, current tests and human approval remain separate; the display does not infer conflict, failure or admission from insufficient evidence.
- [ ] The selected design supports 160, 116 and 80 column views, stable keyboard selection, NO_COLOR, readable ASCII/text exports and full identifiers in selected detail; no blinking or compulsory motion.
- [ ] Test the 8-orchestrator/80-session base and 5/8/10-orchestrator, 50/80/100-session scenarios, including uneven ownership, shared/unmapped worktrees, historical records, duplicates/out-of-order events, stale sources and missing fields. One-to-one session/worktree mapping is not assumed.
- [ ] Sanitize untrusted ANSI/OSC/control sequences; use display-cell width for safe truncation and keep filtered versus global counts explicit.
- [ ] Tokens are not progress; elapsed time is not completion percentage; missing cost is not zero; a partial subtotal is not total spend; policy-frozen work remains for explicit human handling.
- [ ] Keep collection deterministic and bounded, without a default LLM polling loop or operational controls.
- [ ] Integration uses confirmed source contracts and clearly identifies unsupported or incomplete coverage instead of presenting synthetic fixture fields as established Orca API fields.
- [ ] The twenty primary design images and complete package are provided with the issue, subject to attachment support and an accessible package delivery method.

Added 2026-11-13 from the reviewer feedback and the alignment work above (confirm when a direction is chosen):

- [ ] The observer shows the same facts as the Orchestrator-mode sweep (one collection and classification), or documents every difference and the reason.
- [ ] Each session shows a plain-English summary (what the task is, what is done, what is left, whether it needs the person) with links to its issue and PR where they exist.
- [ ] Each session shows its steps by name with state colours (done, in progress, failed), not a retry count.
- [ ] A session can be opened from the view (navigation only) through a supported Orca mechanism, or the missing support is disclosed.

## Out of Scope

Approving, retrying, terminating, spawning, merging, rebasing, deleting worktrees or instructing workers; a new scheduler or session manager; forks of other agent managers. This issue request does not authorize production code changes or deployment. The observer is not the Orchestrator-mode sweep ([#339](https://github.com/IronbellyOrg/IronClaude/issues/339)), the issue watcher ([#450](https://github.com/IronbellyOrg/IronClaude/issues/450)) or the Coder workspace listener ([Coder#477](https://github.com/IronbellyOrg/Coder/issues/477)), and it must not send prompts or commands through any of them.

## Components Affected (from `/sc:analyze`)

Quick static inspection of the offline prototype: `.dev/design/orca-observer-20261106/render.py` composes and exports fixture-backed screens; `canvas.py` provides character-cell rendering and sanitization; `fixtures.py` supplies synthetic data and metrics. These are prototype components, not a verified production integration. Codegraph and Auggie tools were unavailable in this session; Read was used. No runtime or performance analysis was performed. The future production component paths are not known yet.

Added 2026-11-13: the read-only data source the observer is proposed to read is the Orchestrator-mode sweep in [PR #539](https://github.com/IronbellyOrg/IronClaude/pull/539) (not merged): `src/superclaude/cli/sweep/` (collection, classification, report, models), `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, rule WC-16 in `src/superclaude/core/WORKER-CONTRACT.md`, and its design `docs/designs/orchestrator-mode.md` (JSON schema in section 7.4, report layout in section 7.5). These were read in the PR's branch; no observer path is known yet.

## Related Issues/PRs

Orchestrator mode (the agent-facing half; must stay aligned):

- [#339](https://github.com/IronbellyOrg/IronClaude/issues/339) Orchestrator, to run and manage all sessions in a worktree. Phase 1: [PR #539](https://github.com/IronbellyOrg/IronClaude/pull/539) (open), test fix [PR #541](https://github.com/IronbellyOrg/IronClaude/pull/541) (open). Follow-ups: [#534](https://github.com/IronbellyOrg/IronClaude/issues/534).
- [#444](https://github.com/IronbellyOrg/IronClaude/issues/444) Sub-orchestrator mode evaluation (Phase 2 input). Technical reference: [PR #532](https://github.com/IronbellyOrg/IronClaude/pull/532) (merged).
- [#423](https://github.com/IronbellyOrg/IronClaude/issues/423) Orchestrator v2, proactive and holistic (a separate later release; distinct from this view).

Intake and routing to the orchestrator (must stay aligned):

- [#331](https://github.com/IronbellyOrg/IronClaude/issues/331) Issue watcher (closed; built in [#447](https://github.com/IronbellyOrg/IronClaude/pull/447) and [#448](https://github.com/IronbellyOrg/IronClaude/pull/448)); rollout [#450](https://github.com/IronbellyOrg/IronClaude/issues/450) (open).
- [IronbellyOrg/Coder#477](https://github.com/IronbellyOrg/Coder/issues/477) Workspace listener, monitor registration and secure prompt routing (open). Prior art there: [Coder#195](https://github.com/IronbellyOrg/Coder/issues/195) (closed, automatic Orca pairing).
- [#394](https://github.com/IronbellyOrg/IronClaude/issues/394) Hook that enforces the launch level of claim-launched agents (open; about agents started by `/sc:issue --claim --pipeline`; the watcher starts `/sc:issue --claim <N>` sessions, so the two may need to agree on launch level).

Searched earlier and not confirmed related: [#326](https://github.com/IronbellyOrg/IronClaude/issues/326), [#320](https://github.com/IronbellyOrg/IronClaude/issues/320), [#315](https://github.com/IronbellyOrg/IronClaude/issues/315), [#323](https://github.com/IronbellyOrg/IronClaude/issues/323).

Design collaboration: branch `docs/409-orca-dashboard-designs` (no PR).


<!-- sc:issue:create template=issue-feature-simple -->


