<!-- TEMPLATE v2 (agent 1; amended 2026-11-22 after ic-planner's Round 1 answers D1, D3). Subject to shared/CONSENSUS.md.
A hand-off packet is a FOLDER: .dev/issues/<feature-issue>/bmad/ containing
  (1) INDEX.md  = this file, filled once per feature, and
  (2) one self-contained story file per story, story-<N>-<M>-<slug>.md, from the second template below in this file.
Why a folder: /sc:workflow snapshots only its one source file and _bmad-output/ is untracked per clone, so each story file must carry everything its plan needs.
Never invent a fact: write "Not known yet". Everything is copied or derived from BMAD outputs; nothing here is new design.
In v0 a person in the BMAD planning session (or the coordinator, checking) builds the files by hand from the epics file; no script is built before the first trial. -->

# PART 1: INDEX.md (one per feature)

---
packet_version: 2
feature_issue: <GitHub issue number of the feature sub-issue>
epic_issue: <GitHub issue number of the epic>
release: <e.g. 1.8>
epic_number: <N, equals the EPIC number>
feature_group: <PRD feature group name>
fr_ids: [<FR ids covered>]
stories: [<N-M-title keys from sprint-status.yaml, in execution order>]
created: <YYYY-MM-DD>
bmad_version: 6.9.0
status: <draft | accepted | rejected: <reason and failing checklist row>>
---

# Hand-off packet: <feature title> (feature issue #<n>, release <x>)

## Binding documents, by role

| Role | Path | Rule |
|---|---|---|
| Spec (wins on conflict) | <SPEC.md and companions> | behaviour source of truth |
| Architecture spine | <ARCHITECTURE-SPINE.md> | the `AD-n` listed per story are binding; do not contradict |
| PRD | <prd.md, addendum.md> | feature group and FR ids above |
| UX (only if UI is touched) | <DESIGN.md, EXPERIENCE.md> | states and widths |
| Project context | <project-context.md> | house rules summary; CLAUDE.md governs |

These originals stay where BMAD keeps them. Story files below carry the rows they need; IronClaude does not read the originals during planning.

## Story order and dependencies

| Order | Story key | Story file | Depends on (story keys) | Complexity (repo rubric) |
|---|---|---|---|---|

## Feature-level constraints (copied into every story file)

<UV only, no bare pip; no `.claude/` staging; `.dev/tasks/` staged; fork-only PR target; plus the SPEC constraints for this feature>

## Gates and staging

| What | Allowed now? | Blocked on |
|---|---|---|

## Open questions and UNVERIFIED items touching this feature

<from the SPEC open_questions and the unverified register; each with an owner and a default>

## Design question open? (decides whether IronClaude adds a design step)

<no | yes: the question, the options BMAD already considered, the decision deadline>. Default: no, because the architecture spine and SPEC companions are BMAD's design; IronClaude adds `/sc:design` only for a story the packet marks open.

## Status mapping used by the write-back (coordinator only; workers never write it)

| Event | sprint-status.yaml key | GitHub |
|---|---|---|
| packet accepted | each story `ready-for-dev` (epic stays `backlog` until the first `in-progress`) | progress comment opened on each story issue |
| first implement task of the story started | that story `in-progress` (epic lifts from `backlog`) | progress comment edited |
| PR opened | each story in the PR `review` | comment with PR link |
| PR merged and closeout done | each story in the PR `done` | story issue closed; comment on the feature issue |
| last story `done` | none (retrospective is the next BMAD step) | feature issue closed |

Rules: never regress a status; one comment per story edited in place, no duplicates. In BMAD terms `ready-for-dev` here means "packet accepted", not "`bmad-create-story` ran" (create-story is skipped by design).

## Acceptance of this packet (filled by the IronClaude coordinator)

- Accepted by: <session> on <date>, or rejected with the failing checklist row number (rows H1.1 to H1.9 in shared/CONSENSUS.md).
- Owner's go for this feature, recorded in chat: <date and wording>.

---

# PART 2: story-<N>-<M>-<slug>.md (one per story; self-contained)

---
story_key: <N-M-title>
story_id: <N.M>
feature_issue: <n>
story_issue: <n or "to be filed at hand-off">
fr_ids: [<FR ids>]
type: <feature | bug>
complexity: <simple | medium | complex>   # repo rubric: simple up to 4 h in one area; medium over 4 up to 16 h; complex over 16 h, more than one subsystem, security or data migration
paths: [<paths this story touches, or "new area: <where>">]
depends_on: [<story keys>]
---

# Story <N>.<M>: <title>

As a <user>, I want <capability>, so that <benefit>.

## Acceptance Criteria

(Copied verbatim from the epics file. Ids are assigned once, in order, and never renumbered; new criteria are appended with the next number.)

- S<N>.<M>-AC1: **Given** ... **When** ... **Then** ...
- S<N>.<M>-AC2: ...

## Architecture decisions that bind this story

| AD id | Rule (one line, copied) |
|---|---|

A needed change to any row is not made in IronClaude: it goes back as a Spec Gap Report to `/bmad-correct-course` and the story waits.

## Constraints

(Copied from the feature-level constraints and the SPEC. Library names and versions the story depends on are stated here.)

## Out of scope

(Copied from the SPEC non-goals that touch this story.)

## Previous story notes

(Written by the coordinator from the previous story's ledger and write-back record. First story of a feature: "none".)

## IronClaude execution

(Filled by the coordinator only: arm taken and trigger, plan package path, ledger path, PR. Empty at hand-off.)
