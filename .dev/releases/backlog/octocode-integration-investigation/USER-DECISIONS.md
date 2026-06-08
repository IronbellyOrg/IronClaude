# User Decisions Log

**Recorded:** 2026-05-31
**Investigation:** TASK-RESEARCH-20260530-044428 (octocode integration)
**Status:** Locked in — awaiting additional planning material from user before further synthesis

---

## Decisions in Response to merged-requirements.md §10 Open Questions

| # | Question | User's Decision |
|---|---|---|
| 1 | Adopt centralized-skill design vs stick with v2 distributed plan? | **v2 distributed** (T1-T6 per `FINAL-RECOMMENDATIONS-v2.md`) |
| 2 | Skill naming if adopting | **`octodive`** (final name — replaces working name `octocode-deep-dive`) |
| 3 | task-mode timing (v1 vs v1.1)? | **v1** (task-mode ships in initial release, not deferred) |
| 4 | Cache invalidation policy? | **Defer** (deferred per prior recommendation) |
| 5 | `/octodive` slash command? | **Yes** (add slash-command discoverability layer) |

## Interpretation Notes

- Decision #1 chooses the v2 **distributed** integration plan as the primary roadmap (T1 deep-research agent, T2 tech-research Phase 4, T3 /sc:research --source, T4 sc-brainstorm Wave 2A, T5 /sc:troubleshoot, T6 /tdd).
- Decisions #2-5 imply the `octodive` skill is still being built — likely as an **additional** integration surface alongside the v2 distributed targets, or as a parallel option, OR as part of a larger architecture the user is about to describe.
- The user explicitly noted: *"I have additional documents pertaining to the planning of this to make it much more than what we have planned"* — additional material will refine/extend these decisions.

## State of Investigation Artifacts

All in-progress documents have been closed out and marked Complete:

| Stage | Artifact | Status |
|---|---|---|
| Stage 1 | `octocode-research.md` | Complete |
| Stage 1 | `research/web-01..03.md`, `research/02-integration-points.md` | Complete |
| Stage 1 | `research/web-04-octocode-skills-marketplace.md` | FAILED (stalled at 600s — coverage filled by web-03 + code-02) |
| Stage 1 | `research/01-existing-tooling-overlap.md` | STUB (covered by web-03 + code-02) |
| Stage 2 | `octocode-fit-analysis.md` | Complete |
| Stage 3 v1 | `brainstorm-v1-lenses-on-deep-research/01..06-*.md` | Complete (preserved as reference) |
| Stage 3 v1 synthesis | `FINAL-RECOMMENDATIONS.md` | Complete |
| Stage 3 v2 | `top-5-targets.md` | Complete |
| Stage 3 v2 | `brainstorm/01..06-*.md` (5 v2 targets + T6 /tdd) | Complete |
| Stage 3 v2 synthesis | `FINAL-RECOMMENDATIONS-v2.md` | Complete (the chosen roadmap) |
| Validate/refute | `/tdd`, `/sc:design`, `/task-builder` analysis | Complete (inline in chat; T6 brainstorm written) |
| Centralization brainstorm | `brainstorm-skill-funnel/seed-brief.md` | Complete |
| Centralization brainstorm | `brainstorm-skill-funnel/adversarial/proposal-a..c-*.md` | Complete |
| Centralization brainstorm | `brainstorm-skill-funnel/adversarial/debate-transcript.md` | Complete |
| Centralization brainstorm | `brainstorm-skill-funnel/merged-requirements.md` | Complete |
| Centralization brainstorm | `brainstorm-skill-funnel/return-contract.yaml` | Complete |

**Total investigation output:** ~8,500+ lines across ~25 files in `.dev/tasks/to-do/TASK-RESEARCH-20260530-044428/`.

## Hold Status

**Awaiting user upload of additional planning documents.** No further synthesis or new agent spawns until the new material is provided. When it arrives, the existing artifacts (especially `FINAL-RECOMMENDATIONS-v2.md` and `brainstorm-skill-funnel/merged-requirements.md`) become the prior context to reconcile against.
