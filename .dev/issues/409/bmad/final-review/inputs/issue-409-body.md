<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

**Design collaboration: [view all twenty embedded previews](https://github.com/IronbellyOrg/IronClaude/blob/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106/PREVIEWS.md) · [download the complete package](https://github.com/IronbellyOrg/IronClaude/raw/refs/heads/docs/409-orca-dashboard-designs/.dev/issues/409/orca-observer-design-package.zip).** The branch is `docs/409-orca-dashboard-designs`; the original22 image attachments remain embedded below.

Create a human-observation terminal companion for Stably.ai Orca in the existing IronClaude/Coder environment. It is not github.com/orca-cli/orca, a scheduler, or a session manager.

## Problem Statement

One human supervising 5-10 orchestrators and 50-100 sessions/worktrees can miss important decisions, meaningful updates, and evidence in noisy chats. They need to distinguish verified outcomes from activity and understand what needs attention and why.

## User Story

As a human supervising orchestrators, I want a read-only view of attention, affected work, changes, and evidence, so that I can find decisions and inspect their supporting facts without confusing activity with outcomes.

## Proposed Solution

After a human selects a visual direction, develop an observer that shows attention items and reasons, affected missions/orchestrators/sessions/worktrees, meaningful changes since the last look, and evidence freshness and completeness. Permit inspection of underlying evidence and disclose unknown, stale, unavailable, or partial data rather than implying completeness. Keep lifecycle, report status, acceptance, current tests, and human approval distinct. A dirty worktree is not automatically dangerous, stale is not failed, shared paths do not establish a conflict, and inspectable evidence is not admission.

The source-to-dashboard schema is proposed, not an Orca API contract. Complete non-consuming message enumeration, cross-host ownership joins, admission and revision-pinned evidence feeds, accounting coverage, durable event replay and native deep links remain unverified. Orca and coordinator policies retain authority.

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

## Out of Scope

Approving, retrying, terminating, spawning, merging, rebasing, deleting worktrees or instructing workers; a new scheduler or session manager; forks of other agent managers. This issue request does not authorize production code changes or deployment.

## Components Affected (from `/sc:analyze`)

Quick static inspection of the offline prototype: `.dev/design/orca-observer-20261106/render.py` composes and exports fixture-backed screens; `canvas.py` provides character-cell rendering and sanitization; `fixtures.py` supplies synthetic data and metrics. These are prototype components, not a verified production integration. Codegraph and Auggie tools were unavailable in this session; Read was used. No runtime or performance analysis was performed. The future production component paths are not known yet.

## Related Issues/PRs

Potentially related search results, not confirmed duplicates: #331 and #339. Other orchestration search results include #326, #320, #394, #315 and #323.

<!-- sc:issue:create template=issue-feature-simple -->

