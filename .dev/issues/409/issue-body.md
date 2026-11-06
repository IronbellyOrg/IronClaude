<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

Create a human-observation terminal companion for Stably.ai Orca in the existing IronClaude/Coder environment. It is not github.com/orca-cli/orca, a scheduler, or a session manager.

## Problem Statement

One human supervising 5-10 orchestrators and 50-100 sessions/worktrees can miss important decisions, meaningful updates, and evidence in noisy chats. They need to distinguish verified outcomes from activity and understand what needs attention and why.

## User Story

As a human supervising orchestrators, I want a read-only view of attention, affected work, changes, and evidence, so that I can find decisions and inspect their supporting facts without confusing activity with outcomes.

## Proposed Solution

After a human selects a visual direction, develop an observer that shows attention items and reasons, affected missions/orchestrators/sessions/worktrees, meaningful changes since the last look, and evidence freshness and completeness. Permit inspection of underlying evidence and disclose unknown, stale, unavailable, or partial data rather than implying completeness. Keep lifecycle, report status, acceptance, current tests, and human approval distinct. A dirty worktree is not automatically dangerous, stale is not failed, shared paths do not establish a conflict, and inspectable evidence is not admission.

The source-to-dashboard schema is proposed, not an Orca API contract. Complete non-consuming message enumeration, cross-host ownership joins, admission and revision-pinned evidence feeds, accounting coverage, durable event replay and native deep links remain unverified. Orca and coordinator policies retain authority.

### Design artifacts and frameworks

The current offline design package contains two galleries and ten-page PDF portfolios, two contact sheets, twenty designs, fixture/scenario JSON, source ledger, data dictionary, renderer, tests, and PNG/SVG/ANSI/plain/ASCII exports at 160, 116 and 80 columns. The complete local archive is `orca-observer-design-package.zip` (405 files, 14,435,766 bytes); its upload is not established. The designs and records are synthetic and have no live integration. User selection precedes production integration.

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

![Observation concepts contact sheet](./attachments/observation-contact-sheet.png)
![Agent supervision contact sheet](./attachments/agent-supervision-contact-sheet.png)

**First set**

![Signal Bridge](./attachments/signal-bridge.png)
![Fleet Quilt](./attachments/fleet-quilt.png)
![Time Loom](./attachments/time-loom.png)
![Worktree Atlas](./attachments/worktree-atlas.png)
![Decision Desk](./attachments/decision-desk.png)
![Proof Gate](./attachments/proof-gate.png)
![Budget Engine](./attachments/budget-engine.png)
![Relay Map](./attachments/relay-map.png)
![Delta Deck](./attachments/delta-deck.png)
![Watchkeeper](./attachments/watchkeeper.png)

**Agent-supervision set**

![Leverage Board](./attachments/leverage-board.png)
![Attention Ledger](./attachments/attention-ledger.png)
![Handoff Switchboard](./attachments/handoff-switchboard.png)
![Loop Detector](./attachments/loop-detector.png)
![Collision Lens](./attachments/collision-lens.png)
![Outcome Ledger](./attachments/outcome-ledger.png)
![Revision Drift](./attachments/revision-drift.png)
![Mission Pulse](./attachments/mission-pulse.png)
![Owner Load](./attachments/owner-load.png)
![Shift Brief](./attachments/shift-brief.png)

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
