# Evidence Routing for Synthesis (Phase 5)

**Task:** TASK-TECHREF-orchestration-20261110-050239
**Date:** 2026-11-12
**Built from:** Glob of `research/*.md` (14 files, 3595 lines), `gaps-and-questions.md`, `qa/qa-research-gap-fill-decision.md`, `qa/phase-3-consolidated-fix-decision.md`, `qa/phase-4-consolidated-fix-decision.md`.
**Rule:** web evidence (W1, W2) is secondary to code; it states documented host behavior, never observed behavior on this host. A gap file's "Corrections to earlier research" beats research 01-06 for the statements it lists (`gaps-and-questions.md` section A2 precedence block).

## Synthesis outputs and the template sections they own

| Output | Template sections | Notes |
|---|---|---|
| `synthesis/synth-01-overview-architecture.md` | 1 Overview, 2 Architecture (2.1-2.4) | architecture grounded in code; policy identified as normative |
| `synthesis/synth-02-data-flow.md` | 3 Directory Structure (3.1), 4 Data Flow (4.1-4.3) | diagrams only for supported flows; distinguish source provenance |
| `synthesis/synth-03-subsystems.md` | 5 Subsystem Reference (5.1-5.N) | each subsystem: purpose, files, behavior, interfaces, dependencies, consumers, citations |
| `synthesis/synth-04-integration-config.md` | 8 API and Integration Points, 9 Configuration and Environment, 10 Error Handling and Edge Cases, 11 Performance Characteristics | signatures and defaults match source; no invented performance figures |
| `synthesis/synth-05-conventions-debt.md` | 12 Conventions, 13 Extension Guide, 14 Limitations and Debt, 15 Verification (mandatory), 16 Glossary; also marks 6 State Management and 7 Component Inventory N/A with rationale | deferred mode, stale docs, uncertainty, DEFECT register faithfully recorded |

Sections 6 and 7 (frontend state and components) are N/A: supervised orchestration has no frontend; rationale is recorded in synth-05. Section 11 is limits-only (registered timeouts, speed pins, documented cadences); no measured figures exist (`research-notes.md:41`).

## Routing table (every discovered artifact)

Columns: artifact; lines; target synth files (01..05) and template sections; disposition.

| Artifact | Lines | Routed to | Disposition |
|---|---|---|---|
| `research/01-roles-authority.md` (roles, authority, human rulings, ownership wording) | 234 | 01 (1, 2.1-2.3); 03 (5.1 roles and authority); 05 (12.1-12.2 rule IDs, 14.1 stale wording, 16 glossary) | integrate; gap files supersede where listed |
| `research/02-lifecycle.md` (coordinator lifecycle, monitoring, retries, messages, section 11 on contract section 5) | 375 | 01 (2.1); 02 (4.1); 03 (5.2 lifecycle); 04 (8.3, 10.2); 05 (14.1, 16) | integrate; corrections in gap-P3-G01 apply |
| `research/03-guards.md` (hooks, guard, identity, installer registration, probes) | 466 | 01 (2.2); 02 (3, 4.1); 03 (5.3 guards); 04 (8.2, 9.1, 10, 11); 05 (12, 13.2, 14.1, 15) | integrate; C.3 fail-closed wording corrected by gap-P3-G06 |
| `research/04-launchers.md` (claim and worker launch boundaries) | 183 | 01 (2.2); 02 (3, 4.1); 03 (5.4 launchers); 04 (8.2, 9.2, 10); 05 (14.1) | integrate |
| `research/05-orca-provenance.md` (Orca dev-source helper routing, mailbox, run binding) | 226 | 01 (2.2); 02 (4.1, 4.2); 03 (5.5 Orca-side enforcement); 04 (8.3, 9.3); 05 (14.1) | integrate with CHECKOUT / INSTALLED / DEPLOYED labels |
| `research/06-distribution-evidence.md` (distribution, policy, staleness, provenance) | 222 | 01 (1); 02 (3); 04 (8.3, 9.1); 05 (13, 14.1, 15) | integrate |
| `research/gap-P3-G01.md` worker-side lifecycle source (preamble, heartbeat, liveness projection, retired scheduler) | 305 | 02 (4.1, 4.3); 03 (5.2, 5.5); 04 (8.3, 9.3 heartbeat setting, 10.2); 05 (14.1, corrections) | mandatory; supersedes statements listed in its corrections table |
| `research/gap-P3-G02.md` guards recognize only the name `orca` | 236 | 03 (5.3); 04 (8.2, 10.2); 05 (14.1, DEFECT register, 15) | mandatory; DEFECT linked to `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/` |
| `research/gap-P3-G03.md` installer, Orca skills install, doctor | 276 | 02 (3); 03 (5.6 installer and health); 04 (8.3, 9.1, 10.1); 05 (13.1, 14.1) | mandatory |
| `research/gap-P3-G04.md` return-contract channel | 265 | 02 (4.1, 4.3); 03 (5.7 result channel); 04 (8.2, 10.1); 05 (14.1; `/sc:implement` producer deferred under P4) | mandatory |
| `research/gap-P3-G05.md` ccsession and Orca tab writer side, 23 env vars | 332 | 02 (4.1); 03 (5.4); 04 (8.2, 9.2, 10.1); 05 (14.1, 14.2 stale marker) | mandatory |
| `research/gap-P3-G06.md` hook timeouts, design fail-open rows, speed pins | 150 | 04 (10.3, 11.1-11.2); 05 (14.1) | mandatory; qualifies 03 C.3 |
| `research/web-01-claude-code-hook-execution.md` (W1) | 124 | 04 (10.3, 11); 05 (12.2, 14.1) | secondary to code; DOCUMENTED label with URL |
| `research/web-02-claude-code-subagent-hooks.md` (W2) | 201 | 03 (5.3 subagent, bare and settings notes); 04 (8.2, 10.2); 05 (14.1) | secondary to code; DOCUMENTED label with URL |
| `gaps-and-questions.md` (register: A, A2 precedence, A3 remaining gaps, B accepted limits, C owner questions, D defect register, E notes, Phase 4 note) | 151 | 05 (14.1, 14.3, 15, 16); 01 (1 scope and boundaries) | mandatory; owner questions reproduced as open questions, not as decisions |
| `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/` (remediation plan, owner-authorized) | 51 | 05 (14.2 technical debt, DEFECT register); 03 (5.3) | link only; the plan is a draft, not a fix |
| `qa/qa-research-gap-fill-decision.md`, `qa/phase-3-consolidated-fix-decision.md`, `qa/phase-4-consolidated-fix-decision.md` | 24, 15, 12 | 05 (15.1 verification log) | provenance of the gap and fix cycles; cite, do not restate |
| `BUILD-REQUEST.md` and `research-notes.md` | 132, 44 | 01 (1 scope); 05 (14.3 deferred mode) | governing scope; not evidence of behavior |
| Earlier report `RESEARCH-REPORT-sub-orchestrator-mode.md` (read sections 6-9 and cited lines) | n/a | 05 (14.1, 14.3, 16) | historical; cite only as historical, never as current |

## Explicit none-found and exclusion decisions

- **No unresolved gap artifact.** All six blocking gaps P3-G01..G06 have a `Status: Complete` file verified by the Phase 3 gate (structural and content PASS). No gap file is missing.
- **No further web topic.** Phase 4 produced W1 and W2 only; the register records the still-UNVERIFIED host facts (timeout signal, subagent `session_id`, managed hooks under `--bare`, installed Claude Code version).
- **No frontend content:** sections 6 and 7 N/A (see above). Sections 3.1 (naming conventions) and 11 are thin by evidence: build the tree from cited paths only; state the limits.
- **Out of scope by design:** subordinate (sub-orchestrator) mode (deferred, never shipped), any live Orca run, installation rollout, resolution of the future-role question. QA reports under `qa/` other than the three decision files are historical review records and are not routed as content (cited only through the verification log).
- **Precedence reminder for every writer:** (1) code and tests at the stated revision; (2) gap-P3 corrections beat research 01-06 and Phase 3 lens reports for the statements they list; (3) between gap files, the file that read the primary source wins; (4) web files are DOCUMENTED host behavior only; (5) normative text (contract, CLAUDE.md, design docs) is policy, not proof of runtime.
