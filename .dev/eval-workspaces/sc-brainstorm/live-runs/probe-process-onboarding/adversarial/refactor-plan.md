# Refactoring Plan: V2 (base) ← V1 strengths

## Overview

- **Base variant:** V2 (sonnet:analyzer) — diagnosis-first, root-cause-driven
- **Incorporated variant:** V1 (opus:scribe) — documentation-systems discipline
- **Planned changes:** 11 incorporations + 2 hybrid resolutions = 13 changes
- **Rejected (changes NOT being made):** 3
- **Overall risk:** Low (all changes are additive to V2 base; structural reorganization is minor)
- **Review:** Auto-approved (non-interactive mode)

## Planned Changes

### Change #1 — Add NFR layer (split quality concerns from FRs)

- **Source:** V1 §3 (Non-Functional Requirements)
- **Target:** New §3.5 in V2 (between current §3 FRs and §4 Falsification Plan)
- **Integration approach:** Insert NFR-001 through NFR-008 (V1 list), but trim/renumber to retain only quality attributes that don't duplicate V2 FRs: NFR-001 brevity cap, NFR-002 markdownlint, NFR-003 maintenance budget, NFR-004 no new runtime deps, NFR-005 README discoverability, NFR-006 tone neutrality, NFR-007 single-line command discipline, NFR-008 version-pinned tool refs
- **Rationale:** Debate evidence (S-003, confidence 70%) — V2 advocate conceded NFR layer adds value, particularly NFR-007 (terminal-paste constraint). Separation of concerns is also a Structure-rubric criterion V2 lost.
- **Risk:** Low — additive

### Change #2 — Add "Two-click rule" FR

- **Source:** V1 FR-004 + supporting language
- **Target:** Insert as new FR in V2 §3 (before FR-005 SoT-explanation-2-clicks)
- **Integration:** Generalize V2 FR-005 (which only requires SoT explanation in 2 clicks) into a broader rule covering all 5 canonical confusion points (UV-only, SoT, worktrees, skills/agents/commands, MCP roles), each with exactly one authoritative paragraph; other docs link to it.
- **Rationale:** U-001 (confidence 90%) — V2 advocate fully conceded. Highest-leverage discoverability discipline.
- **Risk:** Low

### Change #3 — Add audience-tag header convention

- **Source:** V1 FR-006
- **Target:** Insert as new FR in V2 §3
- **Integration:** "Each onboarding guide MUST open with `**Audience:** <role> | **Time:** <minutes> | **Prereqs:** <list>`. Roles: `first-time-contributor`, `returning-contributor`, `maintainer`."
- **Rationale:** C-005 (confidence 80%) — V2 advocate conceded audience tags add reader-profile value V2 missed.
- **Risk:** Low

### Change #4 — Add `superclaude doctor` integration FR

- **Source:** V1 FR-009
- **Target:** Insert as new FR in V2 §3
- **Integration:** "`superclaude doctor` output MUST be the first diagnostic referenced in any troubleshooting section. New onboarding failure modes MUST be added to `doctor`'s checks rather than to prose-only troubleshooting steps."
- **Rationale:** U-002 (confidence 85%) — programmatic checks over prose; conceded.
- **Risk:** Low

### Change #5 — Add single-line command discipline NFR

- **Source:** V1 NFR-007
- **Target:** Include in §3.5 NFR block (already counted in Change #1) — emphasized here because it has highest evidence grounding
- **Integration:** "NFR — Every command in onboarding docs MUST be runnable as a single pasted line (no heredocs, no `\` continuations) per user terminal constraint (memory `feedback_no_multiline_paste.md`)."
- **Rationale:** U-003 (confidence 95%) — evidence-based; V2 advocate fully conceded.
- **Risk:** Low

### Change #6 — Add DM-as-doc-bug improvement loop

- **Source:** V1 §7 residual mitigation
- **Target:** Insert as a new bullet in V2 §6 (Success Metrics, leading indicators) AND as a §7 closing-rule
- **Integration:** "Maintainer's standing reply protocol: 'See <doc-section>; if that doesn't answer it, open an issue tagged `onboarding-gap` so we can fix the doc.' Any question answered twice = doc bug (file the issue and fix the source paragraph, not the answer)."
- **Rationale:** U-004 (confidence 90%) — V2 advocate: "the single best improvement-loop mechanism in either variant."
- **Risk:** Low

### Change #7 — Add brevity caps + wc-l gate

- **Source:** V1 NFR-001 + M-005
- **Target:** Include in §3.5 NFR block (Change #1) for the cap; add as a falsification step in §4
- **Integration:** "NFR — No guide MUST exceed 400 lines; `CONTRIBUTING.md` MUST be ≤150 lines. Falsifiable: `wc -l docs/contributing/*.md CONTRIBUTING.md` reports each file under its cap."
- **Rationale:** U-005 (confidence 75%) — enforceable discipline preventing the doc-rot V2 diagnosed.
- **Risk:** Low

### Change #8 — Restructure document layout (HYBRID resolution of C-001 / X-001)

- **Source:** Hybrid of V1 (4 files under `docs/contributing/`) and V2 (single `docs/contributor-guide.md`)
- **Target:** V2 §2 INT-1 and INT-4, plus FR-002
- **Integration:** Adopt V1's directory layout (`docs/contributing/`) with 4 audience-tagged files (`01-setup.md`, `02-mental-model.md`, `03-first-pr.md`, `04-troubleshooting.md`), BUT preserve V2's SoT-discipline language: each confusion-point answer lives in exactly one paragraph in one file; other files link to it (V1 FR-004 + V2 anti-duplication spirit). Existing `CONTRIBUTING.md` is rewritten as the single canonical entry (V1 FR-001 retained) that links to the four guides.
- **Rationale:** Both advocates conceded the hybrid is stronger than either pure position. V1's audience-layering serves multiple reader profiles; V2's single-source-of-truth-per-topic prevents cross-file drift.
- **Risk:** Medium — restructures V2's primary artifact list; requires care in falsification rewrite to cover 4 files instead of 1

### Change #9 — Add both Make targets (HYBRID resolution of C-002 / X-002)

- **Source:** Hybrid of V1 `make onboard-check` (CI verification) and V2 `make onboard` (contributor-facing)
- **Target:** V2 §2 INT-2, FR-003, FR-004
- **Integration:** Define BOTH targets:
  - `make onboard` — contributor-facing happy-path runner (V2 FR-003 semantics): verifies UV, runs `make dev` / `make sync-dev` / `make verify-sync` / smoke pytest, prints pass/fail + next-steps message, exits 0 on success
  - `make onboard-check` — CI verification gate (V1 FR-005 semantics): runs the same commands but optimized for CI (no interactive output, machine-parseable result); runs on every PR touching `CONTRIBUTING.md`, `docs/contributing/**`, or `Makefile`
  - `make onboard-check` MAY delegate to `make onboard` under a `--ci` flag to avoid duplication
- **Rationale:** Both advocates conceded both targets are needed (different audiences, different output requirements).
- **Risk:** Low

### Change #10 — Add explicit handling of all 6 seed-brief open questions

- **Source:** V1 §7 (which addresses all 6 open questions explicitly)
- **Target:** New §7.5 in V2 (before existing §7 Open Assumptions becomes §8)
- **Integration:** Add a "Decisions on Seed-Brief Open Questions" subsection answering each of: linear-vs-contextual (linear-with-contextual-depth), setup-vs-concepts priority (setup first), where it lives (in-repo markdown), first-PR sandbox (no), skill integration (no), ceremony tolerance (minimum viable).
- **Rationale:** C-006 (confidence 65%) — V1 covers every seed-brief open question; V2 covers most but leaves some implicit.
- **Risk:** Low

### Change #11 — Add diagnosis-first opening framing (V2 strength reinforced)

- **Source:** V2 (already in base) — no change needed; documented here for transparency
- **Target:** §1 retained as Root-Cause Diagnosis
- **Rationale:** S-002 (confidence 75%) — V2 wins; V1 advocate implicitly conceded.

### Change #12 — Promote shared assumptions to explicit §

- **Source:** Both advocates accepted A-001 (Makefile is right primitive), A-002 (linear path sufficient), A-004 (README as discovery entry)
- **Target:** Add to V2 §8 (renumbered Open Assumptions, formerly §7) or new §9 "Promoted Shared Assumptions"
- **Integration:** Document each promoted shared assumption explicitly as a named assumption to be challenged on re-review.
- **Rationale:** AD-2 protocol — UNSTATED promoted assumptions should be visible in the final spec for future-debate transparency.
- **Risk:** Low

### Change #13 — Add explicit failure recovery for `make onboard` failures

- **Source:** V1 advocate critique (V2 weakness #2 in debate)
- **Target:** §4 Falsification Plan, INT-2 row
- **Integration:** "If `make onboard` step N fails, the printed summary MUST direct the contributor to a specific file:section in `docs/contributing/04-troubleshooting.md` keyed on step N. Falsifiable: simulate failure at each step and verify the output points to a real, addressable troubleshooting entry."
- **Rationale:** Debate (V1 advocate critique #2) — V2 had no recovery story; V1's pre-located answers were the better pattern.
- **Risk:** Low

## Changes NOT Being Made

### Rejected #1 — V1's flat-vs-nested artifact debate

- **Diff:** V1 mandated "no nested subfolders" in `docs/contributing/`
- **Decision:** Adopt V1's flat structure but do not codify "no nested subfolders" as a hard NFR. Future contributors may need subfolders for non-onboarding contributor docs.
- **Rationale:** Over-constraint; the brevity cap (NFR-001) already prevents the failure mode V1 worried about.

### Rejected #2 — V1's "exactly 4 files" hard requirement (FR-003)

- **Decision:** Adopt V1's recommendation of 4 audience-tagged files but soften "exactly" to "at least" — let the spec leave room for an additional file (e.g., `05-release-process.md`) when justified.
- **Rationale:** Excessive prescription; the discipline V1 wants (no proliferation) is captured by the brevity cap and the maintenance budget.

### Rejected #3 — V2's "delete docs/developer-guide entirely" framing

- **Decision:** Adopt V2's RC-1 diagnosis and require removal of *stale content* — but reframe as "rewrite or delete files that contain pre-v4 references" rather than blanket directory removal. Some `docs/developer-guide/` content may be salvageable.
- **Rationale:** V2 FR-001 grep test (zero hits for pip / python3 -m / 3.8 / flat-superclaude/Agents) is the right gate; the deletion-vs-rewrite choice is implementation detail. Per V2's own A5, blanket deletion risks breaking external links.

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| #1 (NFR layer) | Low | Minor structural change | Revert section addition |
| #2 (two-click rule) | Low | Stricter FR than V2 base | Soften to recommendation |
| #3 (audience tags) | Low | Documentation overhead | Drop convention |
| #4 (doctor integration) | Low | Requires `doctor` exists (it does — `make doctor` already in Makefile) | Use prose fallback |
| #5 (single-line discipline) | Low | Backed by user memory; well-grounded | n/a |
| #6 (DM-as-doc-bug) | Low | Operational rule, not code | n/a |
| #7 (brevity caps) | Low | `wc -l` is trivial | Drop cap |
| #8 (hybrid layout) | **Medium** | Requires V2 FR re-write; could leave fragments referring to single-file model | Careful merge-log validation |
| #9 (both Make targets) | Low | One delegates to other | Drop CI gate, keep contributor target |
| #10 (open Q handling) | Low | Pure addition | n/a |
| #11 (diagnosis-first) | Low | Already V2 baseline | n/a |
| #12 (shared assumptions) | Low | Transparency addition | n/a |
| #13 (failure recovery) | Low | Falsification refinement | Soften to "should" |

## Review Status

- Auto-approved (non-interactive mode)
- Timestamp: 2026-05-25T19:32:30Z
