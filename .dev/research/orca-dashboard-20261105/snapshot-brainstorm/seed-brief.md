---
topic: "Design static ASCII five-minute chat snapshots for an attention-first Orca multi-agent dashboard"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: "2026-11-05T18:59:21Z"
---

# Seed Brief: Static Attention Snapshot

## Problem Statement
Dozens of Orca worktrees, sessions and agents create noisy updates that bury human decisions. Design a read-only static snapshot, pasteable into chat every five minutes, that makes required action and meaningful change immediately visible. This is design only: no scheduling, controls or implementation.

## Known Context
- Main research synthesis: ../REPORT.md, sections 1-5 populated. Pending sections are not evidence.
- The human operator wants five genuinely different complete snapshot concepts, not five widgets. These will accompany a separate, later interactive-terminal brainstorm and a fork/build recommendation.
- Orca worker-list exposes structured attention, nextAction, stage, liveness/source/time, evidence freshness, resource ownership and opaque cursor pagination.
- Non-consuming run message reads are capped at 100 with no advertised paging. An alternate complete observer API is not verified. Counts must say observed/partial when needed.
- Assignment completion, terminal existence, process liveness and independently verified readiness are distinct.
- AgentHUD is a passive observer with JSON reports and NDJSON follow, without verified Orca integration; Agent Deck manages its own sessions. gh-dash queues, otel-tui hierarchical timelines, btop stable inspection and incident acknowledgment semantics are relevant design inspirations.
- Clarify answers from user: operator audience; attention first; chat output; five-minute cadence. Validation answers: uncertainty visible; no writes; no fabricated metrics; success is finding the oldest blocking decision without opening every transcript.

## Constraints
- Plain ASCII fenced output. No ANSI cursor controls, emoji dependence or font dependence. ANSI color may be an optional terminal-export treatment, never required in chat.
- Target a practical 80-column default; alternatives can explicitly use other widths. Keep each report scannable; choose meaningful rows rather than burying decisions in charts.
- Each actionable row needs stable identity, question/reason, owner/requester, age and impact/evidence reference.
- Preserve unanswered context, not merely changes. Suppress heartbeat spam. Root-blocker grouping must not hide distinct decisions or double-count dependent tasks.
- Include as-of timestamp, scope, source freshness, missing sources, paging coverage and omitted rows. Five-minute output is not an urgent-alert guarantee.
- Compare against last successful observation; failed collection never supplies zero baseline. Unknown values are not zero.
- Costs, tokens, trends and percentages require reliable sources and denominators; otherwise omit or mark unknown.
- All mockup numbers and names must be clearly synthetic; never reuse real active-run records as fake evidence.

## Success Criteria
- Enumerated requirements cover decisions, blocked/failing work, communication context, meaningful changes, evidence-backed verification and fleet coverage.
- Five structurally different whole-report concepts with tradeoffs and one recommended default; include at least one actual ASCII screen in each proposal and name the complete five-concept set.
- A reader can locate the oldest observed blocking request and understand the needed action, while detecting partial coverage.
- Designs handle empty/healthy, busy, stale/unavailable, and reported-complete-but-checks-failing cases without false all-clear.
- Requirements include measurable user evaluation tasks and explicit limits; no claims of runtime validation.

## Open Questions
- Which complete non-consuming source will enumerate durable pending decisions? Feasibility gate, not assumed implementation.
- Best default density: attention brief, control board, dependency-oriented, communications-oriented or change-oriented report?
- Where should overflow go when five-minute chat reports cannot show all observed items? Preserve totals and stable references without implying an unavailable drill-down exists.
- Which data sources will later support human ownership/resolution and independent verification?

## Enrichment Context
Both new enrichment sweeps are explicitly skipped (--no-codebase --no-research). Existing research has already been performed and primary evidence checked by the parent. This avoids repeating it, not a claim the available data is complete.
