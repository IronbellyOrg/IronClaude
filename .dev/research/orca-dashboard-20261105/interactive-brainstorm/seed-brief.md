---
topic: "Five visually distinct interactive terminal dashboards alongside Orca"
domain: product
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: "2026-11-05T21:23:47Z"
---

# Seed Brief: Interactive Dashboard Visual Design

## Problem Statement
Orca already orchestrates dozens of worktrees and agent sessions. The user needs a visually compelling, readable terminal dashboard beside its chat, where important requests do not disappear into routine updates. The previous research overemphasized agent-manager forks and process detail; the user explicitly corrected the direction to TUI frameworks and mainly visual inspiration.

## Known Context
- Existing primary-source research: ../REPORT.md. The framework comparison at the beginning of section 6 supersedes the earlier agent-product fork comparison.
- Candidate building blocks: Textual (Python, terminal CSS and widgets); Bubble Tea + Lip Gloss (Go, event/model/view and custom composition/styling); Ratatui (Rust, constraint layout and drawing widgets). No runtime benchmarks performed.
- Visual references: otel-tui tree/timeline/detail/log proportions; btop panel geometry and compact charts; Dolphie dense metric placement; gh-dash calmer list/preview/whitespace. Borrow visual composition, not their orchestration or domain logic.
- Earlier snapshot design: ../snapshot-brainstorm/merged-requirements.md. Provisional; its five HIGH corrective changes are not independently rechecked. Do not treat it as approved or copy its identifier-heavy screen wholesale.
- Orca observations expose worker attention, liveness, scope and cursor paging. Complete non-consuming decision enumeration remains unverified (inspected message checks capped at 100).
- Quick dialogue answered from user: dashboard not orchestrator; framework reuse; five visually distinct complete screens; read-only observation first, later deliberate actions through Orca.

## Constraints
- Product/design output only. No implementation, installation, scheduling, or live actions. No agent-manager fork recommendation.
- Five whole-screen compositions must differ visibly in panel geometry/hierarchy, not merely titles or widgets. Include each as a compact ASCII mockup plus its optional ANSI color treatment. No mandatory emoji/fonts.
- Favor actual readable content over raw internal IDs; put exact identity in selected details. Show concise scope/freshness/partial-coverage information without drowning out the visual design.
- Common synthetic scene: 24 observed workers (16 active, 4 waiting, 3 reported complete, 1 unavailable), 3 observed human requests (schema choice waiting 42m, API target waiting 18m, review waiting 7m), 2 distinct reported blockers, inbox partial. These dimensions overlap and must not be summed. No measured spend/tokens.
- Selection stays stable while updates arrive. Pause freezes rendering with a visible queued-update indicator, not orchestration. Missing data is unknown, not zero. Reply/acknowledge/resolve are separate proposed actions.
- Layouts should specify wide/default/narrow behavior, key focus, filtering/search, update placement and thread/detail inspection. Later action controls use explicit target and current authority confirmation; read-only mockups do not imply a working integration.
- Each proposal <=180 lines including its five compact screens. At most eight material debate points. No repeated research or sprawling new requirements catalogue.

## Success Criteria
- Five clearly distinguishable terminal compositions with sample screens and visual rationale.
- One recommended visual default, plus the circumstances each alternative suits.
- Framework comparison ties layout needs to verified building blocks; no false measured-performance ranking.
- A reader immediately sees requests needing attention and can imagine the navigation/preview behavior.
- Unknown/capped/stale data and synthetic labels are visible but succinct. A selected request has its question, age, owner, impact and source detail.

## Open Questions
- Which composition best matches the user's desired visual character? Present alternatives rather than treating the debate as user approval.
- Which framework best balances styling flexibility and implementation constraints? Make a provisional recommendation only.
- Exact live observation API, refresh rate and durable human-state storage require later validation, not another design-research sweep now.

## Enrichment Context
Both new sweeps skipped by explicit flags. Use existing research only.
