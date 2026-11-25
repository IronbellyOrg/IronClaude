# Technical Research Report: Agent Orchestration Dashboard

**Date:** 2026-11-05
**Status:** Research and ten visual mockups assembled for review; design validation incomplete. Static brainstorm partial; interactive coordinator subsequently produced a partial merge despite the budget-stop instruction. The parent retains a failed budget gate. No product implementation authorized or performed.
**Scope:** Terminal-only attention dashboard for many Orca runs, worktrees, sessions and agents; five-minute static snapshots and a later interactive terminal.
**Template:** Installed tech-research skill, Report Structure (ten sections). This document uses that structure; it does not claim execution of the full tech-research skill.
**Research handoff limitation:** The three research agents report higher-priority restrictions against writing findings files. Their message results are discovery leads; primary evidence is checked separately before conclusions are populated here.

## Table of Contents

1. Problem Statement
2. Current State Analysis
3. Target State
4. Gap Analysis
5. External Research Findings
6. Options Analysis
7. Recommendation
8. Implementation Plan
9. Open Questions
10. Evidence Trail

## 1. Problem Statement

An operator supervises dozens of worktrees and agent sessions through Orca. Routine messages and agent updates push decision requests out of the visible chat history. The operator needs a trustworthy view of what needs attention, what is happening, what changed, and which actions are safe to take.

The investigation compares adoption, a fork, and a small purpose-built interface over an existing terminal framework. It must produce five distinct static snapshot concepts and five distinct interactive terminal concepts, not substitute component suggestions for complete layouts. Snapshot delivery every five minutes is a design requirement, not authorization to schedule posting now.

## 2. Current State Analysis

### Verified read-only observation surfaces

The installed CLI was resolved as `orca-ide` after the session exposed no ORCA_CLI_COMMAND or ORCA_DEV_REPO_ROOT override. Its version-matched guide and command help were read on 2026-11-05. No orchestration state was changed.

- `worktree ps`: reports execution-host scope and omissions; its help warns that uncovered hosts must not be treated as empty. An independently read saved response reported 29 workspaces, local-only scope and `truncated:false`. This is a historical sample, not a live fleet count for the mockups.
- `orchestration worker-list`: supports explicit run scope, opaque cursor pagination and limits of 1-100. One independently executed one-row sample reported nine attempts with more pages. Its structured projection contained attention categories, requiresAction, nextAction, outcome, stage, liveness observation time/source, evidence freshness and resource ownership. A completed task can still own a live terminal, as the command help explicitly states.
- `orchestration check --peek` and `--all`: non-consuming observations with no delivery ID. Help states a maximum of 100 rows for --all and run --peek, and advertises no read-only paging. This does not prove another Orca API cannot supply complete history; it is a feasibility gap in the inspected CLI surface.
- `orchestration inbox`: help offers a row limit, terminal filter and full-context flag, but no cursor. Complete unanswered-message counts cannot be promised from that help alone.

### Proposed interpretation, not an existing implementation

Keep work status, terminal/process liveness, observation freshness, message delivery and independent validation as separate fields. A stale source must produce an explicit unknown or partial state, not an all-clear. The dashboard must never consume or acknowledge the coordinator's mailbox merely to observe it.

## 3. Target State

### Design requirements for both surfaces

Lead with decisions requiring the operator, then blockers/failures, changes and fleet context. Keep routine activity in drill-down. Every attention item should state the question, requester, acting owner, affected work, original age, evidence and next useful action. These are proposed product requirements, not claims about existing Orca fields.

The logical hierarchy is run > task > attempt > helper. The execution hierarchy is host > workspace > session/terminal. Do not mistake workspace parentage for a task dependency. Preserve unassociated sessions and superseded attempts without letting their reports override current authority.

Static reports need a stable order, as-of time, per-source freshness, explicit coverage and a delta since the last successful collection. A five-minute sample can miss transitions and is not an urgent-alert channel. Interactive concepts add selection, preview, filtering, thread history and deliberate action; opening a detail view must not acknowledge coordinator messages.

### Proposed metric catalogue

| Metric | Definition and operator use | Data prerequisite / missing-data rule |
|---|---|---|
| Open human decisions | Distinct unresolved decision records explicitly assigned to a human | Complete question/gate enumeration, actor and resolution linkage; otherwise 'at least N observed' |
| Oldest decision wait | Now minus original creation time of the oldest unresolved decision | Reliable timestamps and resolution linkage; otherwise 'oldest observed' or unknown |
| Work blocked by decision | Distinct unfinished descendant tasks, with direct versus indirect impact | Complete dependency graph and decision/task association; never sum overlapping descendants |
| Ready but unassigned | Ready tasks with no active authoritative attempt and no unmet dependencies/gates | Missing dependency or gate data means readiness unknown |
| Failures needing intervention | Failed authoritative attempts without accepted replacement or disposition | Need complete disposition/history; separate unknown outcomes |
| Reported complete, verification unknown | Settled-success assignments without independent acceptance evidence | Independent verification ingestion is proposed; do not label green by default |
| Resource decisions | Settled attempts whose owned resources need a retention/release decision | Exclude explicit user retention; unknown release stays unknown |
| Agent liveness | Live, exited and unverifiable observations, deduplicated by authoritative identity | Distinct from task outcome and PTY existence; unknown is not unhealthy or healthy |
| Coverage and freshness | Covered/omitted hosts, paging status and per-source last successful observation | Unknown expected-host denominator means no coverage percentage |
| Queue movement | Newly actionable and resolved distinct decisions in a stated window | Requires durable decision history; message volume is not interruption count |
| Response latency | Median and upper percentile from decision creation to first durable answer, with window/sample size | Requires complete relationships and human identity; unresolved ages shown separately |
| Retry burden | Replacement attempts per task, separating launch/worker failures from transport replay | Requires reliable predecessor history; repeated API requests are not new attempts |
| Spend and tokens | Provider-recorded usage deduplicated by request, with currency/pricing version | Not verified in sampled Orca surfaces; omit or show unavailable, never estimate from runtime |

Avoid leaderboard totals for messages, tool calls, commits, lines changed or percent busy. They reward activity rather than useful progress. Evidence labels should distinguish a worker claim, accepted settlement, existing artifact, checks for a specified revision, independent review and human approval instead of inventing a confidence percentage.

### Communication and action semantics

Keep enqueued, delivered, coordinator-processed, human-seen, answered and resolved separate. Dashboard seen/claimed/snoozed states require their own proposed storage. A reply is not proof of resolution. Use authoritative thread IDs, retain original questions beside summaries and treat transcript content as untrusted data.

Collapse heartbeats into last-seen, group repeated reports under their root blocker and show one connectivity incident with affected workers. Keep last-known data explicitly stale after collection failure; do not compare against an artificial zero baseline. Future write controls must refresh ownership/attempt/scope and require a confirmation naming the precise target and effect; suggested action arguments are not consent.

## 4. Gap Analysis

| Gap | Current evidence | Required behavior | Priority |
|---|---|---|---|
| Complete decision enumeration | Inspected non-consuming message reads are capped and lack advertised paging | Verify a read-only cursor/event API or explicitly label partial observed attention | Critical for an 'every decision' promise |
| Human-state separation | Read flags do not establish a particular person's acknowledgement | Separate human seen/claimed/snoozed/resolved state from transport/coordinator state | Important before interactive actions |
| Evidence-backed readiness | Worker status and liveness are distinct; research reports worker-result provenance | Bind checks/reviews to the current revision and distinguish assignment completion from release readiness | Important |
| Reliable history | Snapshot polling does not prove all intervening transitions | Preserve successful observations and collection gaps; use replayable events if available | Important for trends/response-time metrics |
| Cross-host completeness | CLI reports host scope and omissions | Verify expected-host inventory and remote behavior; never silently omit failures | Important |
| Write authority | Observation help and worker projections inspected; no write-path tests | Refresh identity/ownership and provide target-specific confirmation, idempotency and durable receipts | Required before enabling control |
| Usage accounting | No authoritative usage integration verified | Use provider usage sources or omit spend/token KPIs | Optional; cannot fabricate |
| Fork suitability | Candidate research pending | Verify license, active maintenance, extensibility, data model fit and modification burden | Required before selection |

These are feasibility/design gaps for a proposed product, not claims that an existing shipped dashboard is defective.

## 5. External Research Findings

### Independently checked interface evidence

Sources were read on 2026-11-05. Documentation verifies advertised capabilities, not performance or compatibility with Orca. Only the otel-tui span screenshot was visually inspected; no candidate application was installed or benchmarked.

| Source | Verified pattern | Transfer to this design | Boundary |
|---|---|---|---|
| [otel-tui README](https://raw.githubusercontent.com/ymtdzzz/otel-tui/main/README.md) and [span screenshot](https://raw.githubusercontent.com/ymtdzzz/otel-tui/main/docs/spans.png) | Trace/metric/log filtering and span-correlated logs are marked completed. Screenshot shows expandable hierarchy, common timeline, right detail tree and bottom logs | Dependency/attempt investigation behind the attention queue | Screenshot is not a runtime benchmark; configurable buffer and refresh remain unchecked in README |
| [gh-dash preview](https://www.gh-dash.dev/getting-started/keybindings/preview/) | Toggle preview, move it right/bottom, page details and switch sidebar tabs | Stable queue selection plus adaptive inspector | GitHub data model, not Orca integration |
| [gh-dash notifications](https://www.gh-dash.dev/configuration/notification-section/) | Configured queues, read/reason/repository filters, incremental fetch; reason filtering after fetch | Saved attention views with honest retrieval coverage | A fetch limit is not the count of matching visible records |
| [btop](https://github.com/aristocratos/btop) | Tree/filter/sort, paused process lists, lazy sorting and optionally retained exited-process usage; 256/16-color fallback | Stable focus and freeze-inspection with explicit stale watermark | TTY mode is not verified strict ASCII; process activity is not task progress |
| [Dolphie](https://github.com/charles-001/dolphie) | Hostgroup tabs, SQLite/Zstandard recording, headless capture, pause/seek/replay | Separate observation, current view and historical replay | Database-specific collectors/model; GPL-3.0 repository label; replay readers can impede recording |
| [Agent Deck](https://github.com/asheshgoplani/agent-deck) | Working/input-needed/ready/error filters, nested groups, separate parent-child lineage, attachment and tool-specific status hooks/polling | First-class input-needed views and group-local navigation | Observes registered Agent Deck sessions; existing Orca-session adoption is not established. Some detection is inferred |
| [agent-tui](https://github.com/tder311/agent-tui) | Git/worktree and session discovery, bounded history, manual/periodic refresh, clone grouping | Read-only inventory candidate | Missing/failing providers can silently return empty results; unsuitable default for trustworthy all-clear; documented launch options are macOS-oriented |
| [PagerDuty incident lifecycle](https://docs.pagerduty.com/incident-management/incidents/overview) | Triggered, acknowledged and resolved are distinct; acknowledgement timeout can retrigger | Ownership and deferral must not resolve unanswered decisions | Behavioral inspiration only, not a terminal fork or an Orca capability claim |

The [awesome-tuis index](https://github.com/rothgar/awesome-tuis) is a discovery source, not a maintenance, license or integration endorsement.

### Plugin discovery, separate from standalone applications

The project researcher invoked `/sc:recommend --plugin` and its backing skill. That discovery uses a 500-star primary-results floor; it is a search filter, not a suitability requirement for this product. The parent independently checked the following product distinctions, without installing them:

- [Claude HUD](https://github.com/jarrodwatts/claude-hud): a Claude Code terminal status-line plugin with context/rate-limit and optional tools/agents/task progress. Cross-session decision aggregation is not established. Useful personal status line, not the fleet dashboard.
- [Agent Deck marketplace manifest](https://github.com/asheshgoplani/agent-deck/blob/main/.claude-plugin/marketplace.json): registers a plugin sourced from the repository root with the `skills/agent-deck` instructions. This plugin is not the separate CLI application or proof that its binary/hooks are installed.
- [agents-observe](https://github.com/simple10/agents-observe): a Claude Code observability plugin with a browser dashboard, not an ANSI terminal dashboard. Recording an event does not establish permission to approve or resolve it. Repository identifies MIT.

No complete terminal-only, Orca-aware decision dashboard was verified in these plugin results. Standalone observer candidates are assessed separately below. The researcher also inspected the official marketplace and reported no complete direct match; this is a scoped negative search result, not proof that no such product exists anywhere.

### Additional integration pattern

[Agent of Empires API documentation](https://www.agent-of-empires.com/docs/api/) verifies read-only mode rejects mutation routes with `403 read_only` while allowing reads, profile-scoped managed-session identity, epoch/revision snapshot fencing, callbacks without retry and sequence reset at daemon restart. These are useful design lessons for the proposed observer: distinguish generation from ordering and reconcile after gaps. They do not establish external Orca-session import.

## 6. Options Analysis

### Revised direction: frameworks and visual inspiration

**User correction, 2026-11-05:** Agent/session-manager forks are rejected as the direction: they duplicate Orca rather than solve the presentation problem. Compare TUI dashboard frameworks and seek primarily visual inspiration. Orca remains the existing orchestration system. Earlier product research below is retained as rejected-option provenance, not a recommendation.

| Framework | Documented dashboard building blocks | Design evaluation |
|---|---|---|
| [Textual](https://textual.textualize.io/) | Python; layouts, terminal CSS, DataTable, Tree, Sparkline, keyboard events and testing documentation | Strong candidate for rapidly iterating structured dashboard screens |
| [Bubble Tea](https://github.com/charmbracelet/bubbletea) + [Lip Gloss](https://github.com/charmbracelet/lipgloss) | Go event/model/view framework plus border, spacing, alignment, table, composition and color-profile tools | Strong candidate for a bespoke terminal visual language |
| [Ratatui](https://ratatui.rs/) | Rust; constraint-based nested layouts, tables, charts, sparklines and gauges | Strong candidate for dense custom-drawn terminal dashboards |

These are documented capabilities, not benchmarked rankings. Compare actual example screens and produce visual alternatives before selecting a framework. Drawing/styling reuse is in scope; importing another agent lifecycle or orchestration system is not. ASCII compatibility must be deliberately implemented/tested, not inferred from low-color mode.

Visual references should inform composition: otel-tui's timeline/detail proportions, btop's compact panel hierarchy, Dolphie's density and metric placement, and gh-dash's whitespace and list/preview balance. Use their visuals as references, not their domain behavior as the specification.

### Actual visual references inspected after the correction

- [Lip Gloss official composition example](https://github.com/user-attachments/assets/92560e60-d70e-4ce0-b39e-a60bb933356b): viewed the image, not just README prose. Generous insets, outlined tabs, a layered central prompt, three aligned text columns and a segmented bottom status strip. Transfer the spacing, tab hierarchy and selective border weight, not its decorative rainbow or sample content. Local inspection image: `/tmp/dashboard-lipgloss.bhzm0W1C/visual.png`.
- [oxker demo](https://raw.githubusercontent.com/mrjackwills/oxker/main/.github/demo_01.webp): viewed a frame with a compact inventory header across the top, a narrow right action rail, a wide middle logs/detail region and three aligned bottom charts. Transfer the contrasting proportions and anchored metric row, not container controls. Local inspection image: `/tmp/dashboard-oxker.IMZh7Tm8/visual.webp`.
- [otel-tui span view](https://raw.githubusercontent.com/ymtdzzz/otel-tui/main/docs/spans.png): directly viewed hierarchy and time-axis pairing with a separate details region and bottom strip. Transfer aligned time and inspection structure rather than trace-specific semantics.
- [Ratatui showcase](https://ratatui.rs/showcase/apps/) supplies further visual leads including bottom, oxker and bandwhich. Only oxker was additionally inspected here; inclusion alone is not visual verification of the others.

A guessed Textual blog URL for a memray demonstration returned HTTP 404. It is not used as evidence; Textual's actual documentation remains the framework-capability source. No downloaded candidate code was executed, and these reference images are not being presented as our mockups.

### Earlier product comparison (superseded)

Maintenance metadata was retrieved directly from GitHub on 2026-11-05. Stars and recent pushes are signals of visibility/activity, not quality guarantees. No candidate was runtime-tested against Orca.

| Candidate | Verified reuse opportunity | Adaptation burden | License/maintenance evidence |
|---|---|---|---|
| [AgentHUD](https://github.com/neochoon/agenthud) | Passive existing-session observation, JSON/Markdown report output, NDJSON follow; package uses Ink/React | Closest snapshot-first shape, but provider interface is synchronous on-disk session discovery/parsing, has a closed provider-name union and intentionally independent provider trees. Orca tasks, cross-provider lineage, decision records and freshness need new modeling | 18 stars; pushed 2026-10-30. package.json says MIT, GitHub license null; inspected tree has no LICENSE-named file. Clarify full license grant before copying |
| [Agent Deck](https://github.com/asheshgoplani/agent-deck) | Input-needed queue/status filters, hierarchy, attachment and events | Full product manages its own sessions/lifecycle; existing Orca adoption not demonstrated. Replacing its authority model is substantial, not a reskin | 1,215 stars; pushed 2026-11-04; GitHub MIT metadata. Full component/license audit not performed by parent |
| [Agent of Empires](https://github.com/agent-of-empires/agent-of-empires) | Rust/Ratatui session/worktree product with CLI and HTTP interfaces | Its managed-session model is not an Orca observer. More control-plane surface than a passive initial product requires | 3,613 stars at retrieval; pushed 2026-11-05. Cargo.toml explicitly MIT AND Apache-2.0, despite GitHub MIT metadata; preserve third-party notices |
| [tmux-agent-status](https://github.com/samleeney/tmux-agent-status) | Persistent unread completion records and park/wait suppression | Pane-local completion inbox, not a durable permission/decision queue; status-file integrations alone do not contribute completion history | 292 stars; pushed 2026-09-28; README MIT, GitHub license null. Full licensing evidence unresolved |
| [agent-tui](https://github.com/tder311/agent-tui) | Passive repository/worktree/session inventory | Provider failures can look like empty data; requires explicit failure/coverage model and Orca-specific identity mapping | README MIT; maintenance not independently quantified |
| [gh-dash](https://github.com/dlvhdr/gh-dash) | Queue and preview interaction design | GitHub-specific state/actions would need broad replacement; borrow patterns rather than whole app | GitHub/README MIT; maintenance not independently quantified |

Source checks for AgentHUD: [provider contract](https://github.com/neochoon/agenthud/blob/main/src/data/providers/types.ts), [follow contract](https://github.com/neochoon/agenthud/blob/main/src/data/followTypes.ts), [package](https://github.com/neochoon/agenthud/blob/main/package.json). Follow events are activity/state/lifecycle with session/subagent/provider/project identifiers; these are not a complete human-decision schema. [Agent of Empires Cargo manifest](https://github.com/agent-of-empires/agent-of-empires/blob/main/Cargo.toml) confirms Ratatui and the combined license expression.

### Option A: Adopt an existing application unchanged

Effort low for a trial, but high mismatch risk for this goal. Existing viewers provide useful session visibility, not verified Orca-wide decisions, partial coverage and authority semantics. No researched candidate qualifies as a verified drop-in. This is rejected as the full solution, not as optional personal tooling.

### Option B: Fork a passive observer

AgentHUD is the closest conceptual fit. Reuse report/follow/rendering infrastructure only after license clarification and a code-level integration spike. Estimated effort medium-to-large, not measured: the Orca adapter is not sufficient by itself because the task/decision/host/evidence model differs. Risk: accumulating a broad upstream fork while still building the central domain model.

### Option C: Fork a session-management product

Agent Deck or Agent of Empires provides richer actions and terminal UX, but risks duplicating Orca's session/worktree/control authority. Estimated effort large and integration risk high unless a verified read-only external-state adapter avoids that duplication. Choose only if requirements intentionally expand to replacing Orca ownership, which this request does not ask for.

### Option D: Small Orca-specific application on a mature terminal framework

Reuse Orca's authoritative observations, a single normalized read model, a plain-text snapshot renderer and an existing TUI framework for the later live view. Candidate frameworks: [Textual](https://github.com/Textualize/textual) (Python/MIT), [Bubble Tea](https://github.com/charmbracelet/bubbletea) (Go/MIT), or Ink already used by AgentHUD. Do not build terminal input/rendering from scratch. Estimated effort medium, chiefly data correctness rather than drawing. Risk: owning the domain adapter, event history and action safeguards, which a fork does not remove.

| Criterion | Adopt unchanged | Passive-observer fork | Session-manager fork | Small application + framework |
|---|---|---|---|---|
| Verified Orca integration | No | No; adapter/model work | No; authority migration risk | New adapter required |
| Snapshot-first fit | Candidate-dependent | Strong | Secondary | Direct |
| Control-plane duplication | None if read-only | Low | High | Low by design |
| Upstream merge burden | Low | Medium | High | Framework upgrades only |
| Decision correctness work avoided | Not established | Little | Not established | None hidden |
| Strict ASCII guaranteed | No | New renderer work | New renderer work | Explicit design requirement |

Effort categories are comparative engineering judgments, not delivery estimates or benchmark results.

## 7. Recommendation

**Build the dashboard with a mature TUI framework; do not fork an agent/session manager.** This follows the user's explicit correction. Orca remains the owner of orchestration, worktrees and sessions. Reuse terminal layout, styling and widgets, and borrow primarily visual composition from the inspected references.

**Provisional framework preference:** Bubble Tea + Lip Gloss when custom terminal composition is the leading criterion: borders, aligned panels, restrained color profiles and reusable styled blocks. Textual is a strong alternative when rapid Python widget/layout iteration is more important; Ratatui fits a Rust implementation with custom charts and constraint layouts. These are fit judgments, not measured speed or maintenance rankings. No framework has been selected by the user or tested here.

**Visual starting pair:** Control Strip (S2) for chat snapshots and Triage Rail (I1) for the adjacent terminal. They combine a legible status ribbon with clear attention and selected details. Instrument Mosaic (I2) is the stronger alternative for a dense monitoring-panel appearance. Aesthetic selection belongs to the user; the sketches expose alternatives rather than declaring consensus.

### Ten mockups delivered for visual review

[MOCKUPS.txt](MOCKUPS.txt) is the canonical plain-ASCII set. All data is synthetic. Five snapshot compositions: Brief, Control Strip, Dependency Card, Correspondence Slip and Five-Minute Journal. Five interactive concepts: Triage Rail, Instrument Mosaic, Wait Timeline, Correspondence Desk and State Board. The interactive concepts document proposed navigation, filters, update behavior and narrow layouts; they are not working applications.

The parent refined these from the preserved proposals after the user redirected the task toward visual design. They are not an approved adversarial merge. Mechanical checks passed for ASCII-only content, ten unique concept headings, lines no wider than 100 columns and the shared 24-worker arithmetic. Usability and live behavior were not tested.

## 8. Implementation Plan

This is a proposed follow-up sequence, not an approved implementation plan or authorization to change Orca.

1. **Prove the observation contract.** Verify complete, non-consuming decision enumeration; exact run/task/attempt/message identities; host scope; freshness; pagination and restart behavior. If completeness remains unavailable, pilot an explicitly partial 'observed attention' view rather than claiming all decisions are captured.
2. **Prototype the shared read model and text export.** Keep collection separate from presentation. Use deterministic fixtures for empty, partial, stale, duplicated, superseded and disconnected states. Export one ASCII snapshot; do not activate automatic chat posting during this design task.
3. **Compare framework prototypes, not product forks.** After the user selects a visual direction, implement one representative screen using the strongest framework candidate and test resizing, focus, ASCII output and realistic observation updates. Compare a second framework only if a material limitation appears. Use the same synthetic fixture; do not duplicate Orca session ownership.
4. **Validate the static design with the operator.** Ask them to locate the oldest blocking decision, identify its owner and evidence, and detect incomplete coverage. Test five-minute repetition and overflow without losing unanswered context.
5. **Add live inspection, still read-only.** Reuse the same collector/read model. Add queues, filters, selection-stable preview, thread/dependency views, pause with backlog and explicit stale state. Batch/cache reads; no subprocess per row per frame.
6. **Add deliberate actions only after authority tests.** Revalidate current attempt/owner/host, distinguish draft/send/answer/resolve, enforce confirmations and durable receipts, and test reconnect/retry idempotency. No bulk destructive actions by default.

Acceptance scenarios include: one decision blocking twelve distinct tasks despite three duplicate reports; completed investigation with failing CI; one unreachable host affecting eight workers; superseded attempt success; collector outage/recovery; oldest question beyond a capped message page; empty data versus failed source; and monochrome/strict-ASCII narrow terminals. Counts are synthetic test requirements, not measured current behavior.

## 9. Open Questions

| Question | Why it matters | Next verification |
|---|---|---|
| Is there a complete non-consuming decision/message API beyond the inspected CLI? | Prevents missing old questions or claiming false all-clear | Inspect source/API contract and exercise pagination/reconnect against a controlled fixture |
| Which records assign a decision to a human rather than the coordinator? | Prevents flooding the human queue with agent-to-agent questions | Verify actor/recipient/gate schema and answer/resolution linkage |
| How are independent checks bound to current revisions? | Prevents completed assignments masquerading as merge-ready work | Ingest check/review evidence with immutable revision identity |
| What are the intended hosts and session count? | Coverage denominator and scale acceptance | Explicit configured scope; benchmark dozens of worktrees and deep helpers |
| Where should dashboard-only seen/claimed/snoozed state live? | Must not consume the orchestrator inbox or imply resolution | Choose an authoritative, durable human-state store during implementation design |
| Which framework best serves the chosen visual direction? | Drawing model, widget reuse and language fit affect build effort | Evaluate the selected screen in Bubble Tea/Lip Gloss, Textual or Ratatui; no agent-product fork |
| What telemetry can provide actual usage and cost? | Avoid misleading estimates and double counting | Provider-authoritative usage records, deduplication and pricing versions |
| Which terminal sizes/input environments are required? | ASCII, keyboard accessibility and layout limits | Human review at narrow/default/wide sizes; SSH/tmux and color-disabled checks |

No user decision is needed to finish these design deliverables. Implementation and adopting a particular fork remain separate decisions.

## 10. Evidence Trail

### Research and verification method

Three requested parallel research agents completed: project/plugin discovery (invoked sc:recommend --plugin), information/KPI exploration (read-only Orca inspection), and interface research (invoked sc:research). Their higher-priority report-file restrictions prevented individual Markdown handoffs. Findings arrived in messages and were treated as leads. The parent checked the primary documents and commands cited in sections 2, 5 and 6. Tavily was unavailable to researchers; they used web search/fetch fallback. No application installation or runtime performance test was performed.

### Primary local evidence

- Installed Orca CLI guide: `orca-ide skills get orca-cli --json`, read on 2026-11-05.
- Independently checked command help: `orca-ide orchestration worker-list --help`, `orca-ide orchestration check --help`, `orca-ide orchestration inbox --help`, `orca-ide worktree ps --help`.
- Independently executed a one-row worker-list observation for a known run: nine attempts, one displayed, more pages explicitly disclosed. This supports pagination/schema claims only, not complete fleet counts.
- Preserved research fleet response: `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/2d488d67-e20f-4135-833d-40e213d2ed99/tool-results/br34lrk2d.txt`, hostScope/count/truncation at lines 1783-1790. Local-only sample, not a final mockup data source.
- Visually inspected otel-tui screenshot: `/tmp/orca-dashboard-interface-images.8dUpSgUX/spans.png`, downloaded by interface researcher from the public source linked in section 5. Not republished as our design.

### External evidence

Primary source URLs are attached to each finding and candidate above. GitHub metadata was read directly for AgentHUD, Agent Deck, Agent of Empires and tmux-agent-status on 2026-11-05. Manifest/source evidence was read for AgentHUD provider/event/package contracts and Agent of Empires framework/license. Metadata is point-in-time, not a guarantee of future maintenance.

### Design execution

The static-snapshot brainstorm was invoked first after all three research tracks completed. Its artifacts are under `snapshot-brainstorm/`; the result is partial. The coordinator confirmed proposed fixes for five HIGH findings appear in merged text, but no independent post-merge re-probe established closure. Report-size and answered-but-unresolved ranking questions remain open.

The interactive brainstorm was then invoked in this main session with quick depth, two proposals and the user's corrected visual/framework direction. Both proposals were read from `interactive-brainstorm/adversarial/adversarial/variant-1-opus-frontend.md` and `variant-2-sonnet-architect.md`. Reported generator usage was 119,633 + 164,978 = 284,611 tokens, exceeding its explicit 230,000 ceiling. The parent instructed the coordinator to stop further delegation and preserve a failed contract rather than spend more or claim consensus. A later completion message and on-disk nested contract show that the coordinator nevertheless completed advocates and merge. Its contract reports partial status, 5/8 agreement (0.625), three unresolved points and a merged artifact at `interactive-brainstorm/adversarial/merged-visual-design.md`. Reported helper usage totals 660,703 tokens, excluding coordinator usage; this is not billing or generated-output-token accounting. The parent budget gate remains failed. The late artifact has not been independently reviewed or substituted for the ten delivered mockups. The prior claim that execution had stopped at the ceiling was incorrect; only a stop instruction had been confirmed.

The parent assembled ten compact visual refinements in `MOCKUPS.txt` from those actual proposals and the saved static concepts, correcting misleading totals/scales, distinguishing human owner from requester and prominently labeling partial observations. These are provisional visual deliverables, not a successful protocol merge. Mechanical text checks passed; no independent design-review pass, usability test or running dashboard is claimed. The research/report/mockup files are available for review despite the incomplete protocol gates.

### Negative and limited evidence

No verified drop-in Orca integration or strict ASCII guarantee was found among the shortlisted products. This is a scoped search result, not an exhaustive market absence claim. Complete message enumeration, independent verification ingestion, write-path behavior, remote completeness, cost accounting and scale performance remain untested. AgentHUD's package-license versus missing root-license evidence and Agent of Empires' combined-license manifest are preserved rather than flattened into a single GitHub badge.
