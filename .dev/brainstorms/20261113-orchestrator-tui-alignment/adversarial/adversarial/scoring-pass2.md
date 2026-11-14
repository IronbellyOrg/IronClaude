# Qualitative Scoring: Pass 2 (reverse order: V3, V2, V1)

Step 3 (Hybrid Scoring and Base Selection), qualitative layer only. Template: `refs/artifact-templates.md` Section 3 (qualitative parts); rubric: `refs/scoring-protocol.md` A.2 and SKILL.md `qualitative_scoring` (30 criteria, 6 dimensions). Evaluation order: V3 (`variant-3-haiku-backend.md`), then V2 (`variant-2-opus-analyzer.md`), then V1 (`variant-1-opus-architect.md`). `scoring-pass1.md` was not read.

## Sources and method

- Variants read in full, in reverse input order: `variant-3-haiku-backend.md` (662 lines), `variant-2-opus-analyzer.md` (719), `variant-1-opus-architect.md` (751). Citations "Vn:L" are line numbers in those files as read in this pass.
- Requirements: the 12 Success Criteria and the Constraints of `seed-brief.md`.
- Correctness evidence: `diff-analysis.md` (spot checks SC-01 to SC-42, contradictions X-001 to X-015, assumptions A-001 to A-007) and `invariant-probe.md` (Round 2.5, INV-001 to INV-028). Two project-rule facts behind INV-001 were re-read this pass: `src/superclaude/core/WORKER-CONTRACT.md:23` (never-as-worker list includes `/sc:pr-submit`) and `:243` (PRs "run in an ordinary top-level session ... never as a worker").
- Mechanical checks run this pass (read-only grep on the three variant files): vague qualifiers (should consider, might, as appropriate, as needed, as required, if needed, if convenient, where possible); probability words (probab, likelihood, likely); first use of FU-1, QUESTION-LINK, WC-16, AC-S, OB-H1, NFR-014.
- Not read: `scoring-pass1.md` (independence rule). The adjudicated document was not re-read in full; its facts enter only through the diff-analysis spot checks and invariant-probe rows that cite it.
- Rules applied: CEV per criterion; MET only with a cited quote or line reference; no partial credit. A vague qualifier tied to a stated condition (for example V2:499 "only if needed" where the condition is Q14's answer) is not counted under CLAR-1; a discretionary one is. Each finding from the probe is charged to one criterion only (feasibility findings under CORR-2, self-contradictions under CORR-4, wrong facts under CORR-1).

## Completeness (5 criteria)

Criteria: COMP-1 covers all explicit requirements (the 12 seed Success Criteria and the Constraints); COMP-2 edge cases and failure scenarios; COMP-3 dependencies and prerequisites; COMP-4 success or completion criteria; COMP-5 explicit out-of-scope.

### V3 (backend)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| COMP-1 | Covers all 12 seed criteria and the Constraints | V3:637-652 "Coverage of the twelve required outcomes", one row per criterion; each system has Scope, Current state, Target state, register, Risks (e.g. V3:99-124) | MET (1) |
| COMP-2 | Addresses edge cases and failure scenarios | V3:620 "Edge-case runbook" (owner silent, build differs, truncated list, interrupted launch); V3:118 "Failure and retry" | MET (1) |
| COMP-3 | Dependencies and prerequisites | Register "Blocked-by" / "Blocks" columns (V3:106); Section 4 graph V3:350-391 | MET (1) |
| COMP-4 | Success or completion criteria | "Checkable acceptance criteria" column per item; V3:80 "acceptance statement is aligned contracts, accurate roadmaps, and gated reads"; XC-08 V3:246 | MET (1) |
| COMP-5 | Explicit out-of-scope | V3:82-84 "Deferred boundaries": "No persisted sweep JSON sidecar, observer sweep reader, ... enters PR #539" | MET (1) |
| **Subtotal** | | | **5/5** |

### V2 (analyzer)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| COMP-1 | Covers all 12 seed criteria and the Constraints | Per-system Scope/Current/Target/items/Risks with a "Rev." column (V2:75, 79-118); Q table with recommended, default, gates, wave (V2:300-325); graph (V2:333-476); waves (V2:490-509); chain (V2:58-71); coordinator needs (V2:511-612); INV coverage, INV-008 first (V2:682-688) | MET (1) |
| COMP-2 | Edge cases and failure scenarios | V2:666-680 "7.3 Edge cases and what the spec does" (Q1 never answered, seeded message missing, join mismatch, build change, early sibling removal) | MET (1) |
| COMP-3 | Dependencies and prerequisites | V2:364-439, 70 numbered edges "each with its evidence" and a kind (FILE, PIN, GATE, DEC, PROC, SOFT) | MET (1) |
| COMP-4 | Success or completion criteria | V2:46 "Acceptance criteria each name how a reviewer observes them"; every row ends "Observe:" (e.g. V2:102 SW-06) | MET (1) |
| COMP-5 | Explicit out-of-scope | V2:55 "Multi-host, TUIBBS and building any code are out of scope"; "Deferred until later" column V2:62; V2:595-605 never-do list | MET (1) |
| **Subtotal** | | | **5/5** |

### V1 (architect)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| COMP-1 | Covers all 12 seed criteria and the Constraints | Per-system Scope/Current/Target/items/Risks with an "undo" column (V1:62, 109-152); Q table with default, gates, "Wave needed by" (V1:342-367); graph and checks (V1:371-497); waves (V1:499-545); chain (V1:75-103); coordinator needs (V1:547-641); INV coverage map, INV-008 first (V1:645-651) | MET (1) |
| COMP-2 | Edge cases and failure scenarios | V1:727-738 "7.4 Edge cases the schedule must handle" (Q1 never answered, F3 chosen, revert after merge, sibling cleaned, Orca upgraded) | MET (1) |
| COMP-3 | Dependencies and prerequisites | V1:407-488 graph with hard `->` and soft `~>` edges; V1:490-497 "Graph checks" (no dangling reference, no cycle, roots, sinks) | MET (1) |
| COMP-4 | Success or completion criteria | V1:62 "acceptance criteria (each one checkable by a reviewer reading a file, a PR, an issue or a command output)"; wave "Exit check" column (V1:505) | MET (1) |
| COMP-5 | Explicit out-of-scope | V1:92-99 "1.3 What stays out of scope until later" (runtime link, watcher panel, session-starting listener, TUIBBS, one trust design) | MET (1) |
| **Subtotal** | | | **5/5** |

## Correctness (5 criteria)

Criteria: CORR-1 no factual errors or hallucinated claims; CORR-2 approaches feasible under the stated constraints; CORR-3 terminology consistent; CORR-4 no internal contradictions; CORR-5 claims supported by evidence or rationale. Correctness evidence is checked against `diff-analysis.md` (spot checks SC-01 to SC-42, contradictions X-001 to X-015) and `invariant-probe.md` (INV-001 to INV-028).

### V3 (backend)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| CORR-1 | No factual errors found | diff-analysis spot checks on V3 claims all CONFIRMED (SC-02, SC-07, SC-21, SC-22, SC-30, SC-31); the only WRONG row (SC-01) is V1's. V3 does not assign `/sc:pr-submit` to workers (invariant-probe INV-001 cites only V1:575 and V2:563/610); V3:656 "This variant ran no live Orca, GitHub or code tests" keeps live facts historical | MET (1) |
| CORR-2 | Approach is NOT feasible as written | (a) Hard edit order plus defaults stall: V3:240 XC-02 "sequence #450, Coder#477, #409, #339 comment, #423", V3:138 OB-04 blocked by CO-01, while V3:296 Q3 default "No #477 rewrite" (invariant-probe INV-003: no skip rule, the chain never advances). (b) V3:485 "Explicit authorization for every outward write" alongside mandated `/sc:pr-submit --monitor 3` (V3:520), which pushes and resolves without asking (diff-analysis X-011, A-002). (c) V3:333 one M-APPROVAL node reused for seven items cannot carry per-PR scope (INV-013) | NOT MET (0) |
| CORR-3 | Terminology consistent | Labels defined once at V3:8-20 (PLAN INFERENCE, UNVERIFIED, Adjudicated, Seed) and used the same way throughout; worktree roles S/O/W/C/K/F/L/R fixed at V3:97 and reused in Sections 5 and 6; V3 does not use "Phase 2" in two senses (diff-analysis X-010: "Silent") | MET (1) |
| CORR-4 | Internal contradictions present | V3:444 W1 schedules "XC-03 draft in K" but register V3:241 blocks XC-03 on SW-03 and SW-05 with no draft item; V3:77 "SW-04, SW-05 and XC-07 retain follow-ups" while SW-05 is the capture item (V3:112) (diff-analysis X-015) | NOT MET (0) |
| CORR-5 | Claims carry evidence or rationale | Nearly every paragraph ends with a source tag, e.g. V3:102 "[E-07 to E-09; X-010; NFR-001; NFR-014.]"; inferences labelled "[PLAN INFERENCE ...]" (V3:118) | MET (1) |
| **Subtotal** | | | **3/5** |

### V2 (analyzer)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| CORR-1 | Factual error about project rules | V2:563 Workers do "PR via `/sc:pr-submit --monitor 3`" and V2:610 PR waits "owned by `/sc:pr-submit --monitor 3` in the worker that opened it"; `WORKER-CONTRACT.md:23` puts `/sc:pr-submit` on the never-as-worker list and `:243` says it runs "never as a worker" (re-read this pass; invariant-probe INV-001). Also V2:562 asserts "The worker in `issue-339-orchestrator-mode`" as #539 author with no source (diff-analysis A-004) | NOT MET (0) |
| CORR-2 | Approach is NOT feasible as written | (a) Worker-run PR monitoring is forbidden (INV-001, above). (b) Coordinator home: V2:278 XC-01 lives in "the orchestrator session's checkout", but V2:537 marks the main checkout "Not used by this program" and every other checkout is bound to another issue (invariant-probe INV-002). (c) V2:601 "Post, edit or comment on any issue or PR without the owner's go-ahead" conflicts with mandated `/sc:pr-submit --monitor 3`, which pushes and resolves without asking (diff-analysis X-011) | NOT MET (0) |
| CORR-3 | Terminology inconsistent | V2:64 L1 gate "SW-12 (Phase 2 of #339) started" with the sub-orchestrator package as "Nearest design", while V2:65 defines "Phase 2 `/sc:close`"; "Phase 2" used in two senses with no marker (diff-analysis X-010) | NOT MET (0) |
| CORR-4 | Internal contradictions present | V2:507 "What never waits for #539" lists XC-05, while V2:499 schedules XC-05 in Wave 3, whose gate is "SW-06 merged" (diff-analysis X-015) | NOT MET (0) |
| CORR-5 | Claims carry evidence or rationale | V2:366 "An edge is drawn only if its evidence column names a shared file, a test pin, a gate, an owner decision or a process rule"; OBS-NOW checks each name their command (V2:43); Weak points W1-W8 each name settling evidence (e.g. V2:118) | MET (1) |
| **Subtotal** | | | **1/5** |

### V1 (architect)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| CORR-1 | Factual errors present | V1:57 the two task packages "were **not found in this checkout**" (diff-analysis SC-01: WRONG, both exist). V1:575 Worker does "PR via `/sc:pr-submit --monitor 3`", against `WORKER-CONTRACT.md:23` and `:243` (re-read this pass; invariant-probe INV-001) | NOT MET (0) |
| CORR-2 | Approach is NOT feasible as written | (a) V1:322 XC-04 JOIN blocked only by "Q24; LIVE" and run "with the sweep from PR #539's head", so the unfixed `git status` runs before the INV-008 ruling (diff-analysis X-002). (b) Hard edit chain V1:436 plus V1:603 "apply section 3's default" with Q3 default V1:346 "CO-01 not posted" stalls OB-08, SW-09, V2-01 (invariant-probe INV-003). (c) Worker-run PR monitoring is forbidden (INV-001) | NOT MET (0) |
| CORR-3 | Terminology consistent | V1:103 "CONTRADICTION MARKER (numbering)" keeps the two "Phase 2" senses apart (SW-12 vs SW-13); markers defined once at V1:30-32 and used the same way | MET (1) |
| CORR-4 | Internal contradictions present | V1:319 ledger at "`.dev/brainstorms/20261113-orchestrator-tui-alignment/decision-ledger.md`" (a path in the #539 checkout) vs V1:332 "This checkout IS PR #539's head; a note committed here joins #539" (diff-analysis X-012). V1:346 Q3 default "nothing in IronClaude waits" vs V1:183 OB-08 blocked by "CO-01 (cross-issue order)" | NOT MET (0) |
| CORR-5 | Claims carry evidence or rationale | V1:26 states which file was opened and at which lines; V1:28 "File:line citations are ADJ's unless this spec says it opened the file"; every current-state bullet carries an E/INV id (e.g. V1:115-122) | MET (1) |
| **Subtotal** | | | **2/5** |

## Structure (5 criteria)

Criteria: STRU-1 logical ordering; STRU-2 consistent hierarchy depth; STRU-3 separation of concerns; STRU-4 navigation aids; STRU-5 artifact-type conventions (the seed's per-system plus graph, waves, chain, coordinator layout).

### V3 (backend)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| STRU-1 | Logical ordering | V3:51 "Section 2 is the work register; Section 3 owns decision defaults; Sections 4 and 5 are the dependency and execution views of that same register" (register before graph before waves before operator contract) | MET (1) |
| STRU-2 | Consistent hierarchy | Sections 0-7 at H2; subsections at H3 (e.g. V3:99 "### Orchestrator mode and sweep (SW)", V3:556); per-system sub-blocks use one bold-label pattern ("**Scope.**", "**Current state.**", "**Risks.**") | MET (1) |
| STRU-3 | Separation of concerns | Register (Section 2), decisions (3), graph (4), waves (5), operator contract (6), invariants (7) are distinct; interface/failure/idempotency contracts kept in their own per-system blocks (V3:116-124) | MET (1) |
| STRU-4 | Navigation aids | No table of contents; V3:49-51 "Reading the plan" maps every section; V3:637-652 maps each seed criterion to its section | MET (1) |
| STRU-5 | Follows the artifact type | The seed's Success Criteria layout: per-system Scope/Current/Target/items/deps/Q/risks, then graph (Section 4), waves (5), chain (1), coordinator needs (6), convergence (XC-08, Section 7) | MET (1) |
| **Subtotal** | | | **5/5** |

### V2 (analyzer)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| STRU-1 | Logical ordering | Status and reading guide (V2:12-56) precede chain (V2:58), register (V2:73), decisions (V2:296), graph (V2:333), waves (V2:490), operator needs (V2:511), invariants (V2:614) | MET (1) |
| STRU-2 | Consistent hierarchy | Numbered H3 subsections throughout: 0.1-0.4, 2.1-2.6, 4.1-4.4, 6.1-6.7, 7.1-7.4 (e.g. V2:14, V2:77, V2:335, V2:515, V2:616) | MET (1) |
| STRU-3 | Separation of concerns | Disagreements with the source isolated in "Weak point" blocks (V2:118, 158, 160) and in 4.4 (V2:478-488), apart from the register and graph | MET (1) |
| STRU-4 | Navigation aids | V2:41-47 "How to read this spec"; numbered cross-references such as "see Weak point W5 in 2.5" (V2:66) and "Section 4.2" (V2:75) | MET (1) |
| STRU-5 | Follows the artifact type | Frontmatter with source and status (V2:1-8) and the seed's layout: per-system blocks, Q table, graph, waves, chain, coordinator section, invariants | MET (1) |
| **Subtotal** | | | **5/5** |

### V1 (architect)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| STRU-1 | Logical ordering | V1:107 "Six systems, in the order of their first gating dependency: SW (sweep, gated by INV-008), OB ..."; register (Section 2) precedes decisions (3), graph (4), waves (5) | MET (1) |
| STRU-2 | Consistent hierarchy | Numbered H3 subsections throughout: 0.1-0.6, 1.1-1.4, 2.1-2.6, 4.1-4.3, 5.1-5.4, 6.1-6.9, 7.1-7.5 (e.g. V1:15, V1:79, V1:375, V1:503, V1:551, V1:645) | MET (1) |
| STRU-3 | Separation of concerns | Architectural stance (V1:66-73) and extension scaffolding (V1:740-751) kept apart from the register; serial constraints in their own table (V1:518-529) | MET (1) |
| STRU-4 | Navigation aids | V1:60-62 "How to read a work item"; V1:107 "Every row's blocked-by and blocks ids resolve in section 4"; V1:567 "Section 5.4" back-reference | MET (1) |
| STRU-5 | Follows the artifact type | Frontmatter with source and status (V1:1-9) and the seed's layout: per-system blocks, Q table, graph, waves, chain, coordinator section, invariants | MET (1) |
| **Subtotal** | | | **5/5** |

## Clarity (5 criteria)

Criteria: CLAR-1 unambiguous language (no "should consider", "might", "as appropriate" or equivalent vague qualifiers); CLAR-2 concrete actions; CLAR-3 each section has a clear purpose; CLAR-4 acronyms and domain terms defined on first use; CLAR-5 next steps or decision points identified.

### V3 (backend)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| CLAR-1 | Vague qualifiers present | V3:114 SW-07 "trust and authority as required"; V3:443 W0 "ask subsequent owner decisions only as needed"; V3:521 "synchronize as required" (grep for should consider / might / as appropriate / as needed / as required) | NOT MET (0) |
| CLAR-2 | Concrete actions | Acceptance criteria name concrete checks, e.g. V3:136 OB-02 "record run-current before/after; create probe Run without run-use; seed question, worker_done and heartbeat" | MET (1) |
| CLAR-3 | Each section has a purpose | Each system opens with "**Scope.**" (V3:100, 127, 153, 180, 205, 231); each numbered section opens with a one-paragraph purpose (V3:58, 290, 326, 439, 471, 554) | MET (1) |
| CLAR-4 | Terms NOT defined on first use | V3:13 defers all E/X/A/INV/BC/Q ids to the adjudicated document; QUESTION-LINK first used V3:34 with no definition; FU-1 first used V3:157 undefined; OB-H1, OB-H2, OB-H3 at V3:161 undefined | NOT MET (0) |
| CLAR-5 | Next steps and decision points identified | V3:5 "First action: the owner rules on the unresolved sweep security finding (INV-008)"; V3:319 "Decision runbook ... Q1 is first" | MET (1) |
| **Subtotal** | | | **3/5** |

### V2 (analyzer)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| CLAR-1 | Vague qualifier present | V2:498 Wave 2 lane "OB-05, with OB-08 if convenient" leaves scheduling to discretion (the two "if needed" hits at V2:499, 551 are tied to a stated condition and are not counted) | NOT MET (0) |
| CLAR-2 | Concrete actions | Each criterion names a command, e.g. V2:102 "`gh pr view 539 --repo IronbellyOrg/IronClaude --json state,mergedAt`"; V2:620 I-S1 check command | MET (1) |
| CLAR-3 | Each section has a purpose | "**Scope.**" opens every system (V2:79, 122, 164, 202, 229, 262); V2:513 states Section 6's audience; V2:492 defines "Lockstep" for Section 5 | MET (1) |
| CLAR-4 | Terms NOT defined on first use | V2:44 "All other ids (E-nn, X-nnn, A-nnn, INV-nnn, BC-nn, D-x) are the adjudicated document's"; QUESTION-LINK at V2:31 and OB-H1/OB-H2/OB-H3 at V2:175 undefined; "MERGE-EXECUTOR NOTE" (V2:146) undefined | NOT MET (0) |
| CLAR-5 | Next steps and decision points identified | V2:16 "it is the first action of this spec"; V2:503 "What can run today, before any owner answer"; V2:509 critical path | MET (1) |
| **Subtotal** | | | **3/5** |

### V1 (architect)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| CLAR-1 | No vague qualifiers | Grep of V1 for "should consider / might / as appropriate / as needed / as required / if needed / if convenient / where possible": 0 hits; uncertainty is labelled instead (e.g. V1:57 "Their location is UNVERIFIED") | MET (1) |
| CLAR-2 | Concrete actions | e.g. V1:132 SW-02 "a regression test that reproduces the probe experiment (temp repo, linked worktree, both keys set once) and fails on the current argv" | MET (1) |
| CLAR-3 | Each section has a purpose | "**Scope.**" opens every system (V1:111, 156, 198, 234, 265, 298); V1:549 states Section 6's subject; V1:373 defines the graph notation | MET (1) |
| CLAR-4 | Terms NOT defined on first use | V1:28 "Ids defined in ADJ Part 0.3 are used unchanged"; QUESTION-LINK at V1:40 and OB-H1/OB-H2/OB-H3 at V1:215 undefined; "W-02" and "R2-V2 5.6" (V1:215, 219) undefined | NOT MET (0) |
| CLAR-5 | Next steps and decision points identified | V1:17 "INV-008 is UNRESOLVED and is the first action"; V1:340 "Ask in this order: Q1 to Q4 first"; V1:514-516 "What may run today" | MET (1) |
| **Subtotal** | | | **4/5** |

## Risk Coverage (5 criteria)

Criteria: RISK-1 at least 3 risks with probability and impact; RISK-2 mitigation per risk; RISK-3 failure modes and recovery; RISK-4 external dependencies and their failure; RISK-5 monitoring or validation for risk detection.

### V3 (backend)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| RISK-1 | No probability assessment | Per-system "**Risks.**" paragraphs (V3:122, 150, 177, 202, 228, 287) state impact in prose but no probability or likelihood; grep "probab/likelihood/likely" in V3: 0 hits | NOT MET (0) |
| RISK-2 | Mitigation per risk | Risks are paired with controls, e.g. V3:287 "A prose contract without XC-04 drifts"; Section 7 table V3:558-578 gives an "Invariant/check" for each claimed outcome and the falsifying condition | MET (1) |
| RISK-3 | Failure modes and recovery | V3:118 "Failure and retry"; V3:171 "Interruption runbook"; V3:464-468 "Wave interruption rule"; V3:551 restart rule | MET (1) |
| RISK-4 | External dependencies and their failure | V3:623 "Orca full build differs: stop build-dependent gates"; V3:283 issue edit route "has no etag"; V3:630 "Stopped/deleted remote workspace". Residual: no "Orca app not running" trigger (invariant-probe INV-009) | MET (1) |
| RISK-5 | Monitoring or validation for detection | V3:246 XC-08 independent invariant/coverage gate; V3:242 XC-04 comparison test "deliberate mutation demonstrates failing check"; V3:436 graph integrity check | MET (1) |
| **Subtotal** | | | **4/5** |

### V2 (analyzer)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| RISK-1 | Impact given, probability not | Named risks carry a severity label, e.g. V2:112 "R-SW1 (security, HIGH)", V2:192 "R-WA1 (security, HIGH carry-forward)", but none states a probability or likelihood (grep "probab/likelihood/likely": one hit, V2:207, about the meaning of "TUI Panel", not a risk) | NOT MET (0) |
| RISK-2 | Mitigation per risk | Each risk names its control, e.g. V2:192 "WA-05 (b) and (c) make it explicit"; V2:252 "V2-05's typed-field rule is the control"; V2:292 "hence the TB-1 edge" | MET (1) |
| RISK-3 | Failure modes and recovery | V2:580-593 "6.5 Stop and escalation rules" (upstream URL, `updatedAt` drift, seeded message missing, master test failure) | MET (1) |
| RISK-4 | External dependencies and their failure | V2:675 "The Orca build changes mid-program"; V2:661 "`gh issue edit` has no etag"; V2:678 "A second host appears". Residual: no "Orca app not running" trigger (invariant-probe INV-009) | MET (1) |
| RISK-5 | Monitoring or validation for detection | V2:616-646 every invariant has a "Check" column (e.g. I-G5 "Orca worktree list shows every worktree created by the coordinator"); XC-09 build-string rule checked at each record's exit (V2:286) | MET (1) |
| **Subtotal** | | | **4/5** |

### V1 (architect)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| RISK-1 | No probability assessment | Per-system "**Risks.**" bullets (V1:145-152, 186-194, 223-230, 255-261, 288-294, 329-336) name impact but no probability; grep "probab/likelihood/likely": one hit (V1:239, meaning of "TUI Panel"), not a risk rating | NOT MET (0) |
| RISK-2 | Mitigation per risk | e.g. V1:149 "SW-02 criterion (2) guards it"; V1:189 "OB-04 is the guard"; V1:292 "V2-03 (4) forbids it"; V1:332 "XC-05 runs in a separate master-based worktree" | MET (1) |
| RISK-3 | Failure modes and recovery | V1:596-613 "6.5 Stop and escalation rules"; V1:731 "#539 needs further changes after merge. Revert PR undoes the squash commit" | MET (1) |
| RISK-4 | External dependencies and their failure | V1:733 "Orca is upgraded mid-plan. OB-05's check fails; OB-03 and XC-03 must be re-run"; V1:309 `gh issue edit` "has no version check"; V1:260 Coder facts "rest on one review". Residual: no "Orca app not running" trigger (invariant-probe INV-009) | MET (1) |
| RISK-5 | Monitoring or validation for detection | V1:490-497 graph checks performed; V1:324 XC-06 "fails when any of them changes without the note"; V1:180 OB-05 "a build check or a test fails when the build string changes" | MET (1) |
| **Subtotal** | | | **4/5** |

## Invariant & Edge Case Coverage (5 criteria)

Criteria: INV-1 collection boundaries (empty, single, maximum); INV-2 state interactions across component boundaries; INV-3 guard condition gaps; INV-4 count divergence (off-by-one, inclusive/exclusive); INV-5 interaction effects when components combine.

### V3 (backend)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| INV-1 | Collection boundaries addressed | V3:624 "Worker list truncated: mark PARTIAL"; V3:627 "Duplicate/empty row identity: exclude from joins"; V3:129 "513 rows against a 500-row cap" | MET (1) |
| INV-2 | Cross-component state interactions | V3:565 "Snapshot is current" falsified by "another observer overwrote file"; V3:569 watcher unknown state vs relaunch; V3:144 "Multiple producers can replace one another's snapshot" | MET (1) |
| INV-3 | Guard gaps identified | V3:561 "Another path reads the question mailbox or a global flip exceeds owner scope"; V3:323 "Authority not granted by these questions". Residual not identified: single M-APPROVAL node (INV-013), `filter.<driver>.process` beyond the two named keys (INV-004) | MET (1) |
| INV-4 | Count divergence | V3:563 "six-call cycle is described as five total"; V3:265 "first 50 worker-show in list order" | MET (1) |
| INV-5 | Interaction effects | V3:567-568 "Interaction" rows (claim-only launch, launch receipt vs governed handoff); V3:537 "Several observers multiply load"; V3:460 rule 8 capture vs seeded test need separate consent | MET (1) |
| **Subtotal** | | | **5/5** |

### V2 (analyzer)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| INV-1 | Collection boundaries addressed | V2:631 I-C2 "513 rows means PARTIAL"; V2:636 I-L1 join "excludes empty and duplicate-flagged rows"; V2:674 join "mismatches or is partial" | MET (1) |
| INV-2 | Cross-component state interactions | V2:644 I-I4 "The two programs resolve `XDG_STATE_HOME` differently"; V2:645 I-I5 "`paths` feeds git status, the contract allow-list and transcript scans" | MET (1) |
| INV-3 | Guard gaps identified | V2:627 I-G3 "a `--run <id>` outside the owner's scope sentence is refused by code, not by documentation"; V2:652 F1 falsifier "(c) a worktree whose `.gitattributes` triggers a filter the fix does not cover" (closest of the three to invariant-probe INV-004) | MET (1) |
| INV-4 | Count divergence | V2:630-635 count invariants I-C1 to I-C6, incl. "at most 5 `worker-list` calls per cycle (6 with `--questions`)" and "first 50 in Orca list order" | MET (1) |
| INV-5 | Interaction effects | V2:641-646 interaction invariants I-I1 to I-I6 (shared `CHANGELOG.md`, one shared design file, unmeasured simultaneous Orca load, Run-less sessions invisible to both) | MET (1) |
| **Subtotal** | | | **5/5** |

### V1 (architect)

| Id | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|
| INV-1 | Collection boundaries addressed | V1:698 count row "host past 500 rows (513 now)"; V1:699 "a Run with more than 50 workers"; V1:702 join "excluding empty and duplicate-flagged rows" | MET (1) |
| INV-2 | Cross-component state interactions | V1:693 snapshot "last-writer-wins and has no liveness flag" read as live by CO-03 or OB-09; V1:704 Run-less sessions vs "a reader that treats absence as 'no sessions'" | MET (1) |
| INV-3 | Guard gaps identified | V1:695 "`check_run_id` checks syntax only"; V1:714 F1 falsifier "another git config key ... or the environment (`GIT_*` variables inherited)" | MET (1) |
| INV-4 | Count divergence | V1:698-701 count invariants (5 x 100 rows, 6 calls with `--questions`, 50 `worker-show` rows, one sweep per 5 minutes, 6 sessions a day) | MET (1) |
| INV-5 | Interaction effects | V1:705-708 interaction invariants; V1:735 "Two coordinators or several observers run at once. Load multiplies (INV-032)" | MET (1) |
| **Subtotal** | | | **5/5** |

## Qualitative Summary

| Dimension | V3 (backend) | V2 (analyzer) | V1 (architect) |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 3/5 | 1/5 | 2/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 3/5 | 3/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.833** | **23/30 = 0.767** | **25/30 = 0.833** |

Ranking (qualitative only, pass 2): V3 = V1 (0.833) > V2 (0.767). V3 leads V1 on Correctness (3 against 2), which is the protocol's second tiebreak key if the combined scores also tie; V1 leads V3 on Clarity (4 against 3).

What separates them:
- **Correctness carries all the spread.** All three fail CORR-2 (feasibility) and CORR-4 (internal contradictions). V3 keeps CORR-1 because it has no WRONG spot check and does not hand `/sc:pr-submit` to workers; V1 loses CORR-1 (SC-01 wrong "not found" claim, plus INV-001); V2 loses CORR-1 (INV-001, twice) and CORR-3 ("Phase 2" in two senses, X-010).
- **Clarity:** only V1 is free of discretionary qualifiers (CLAR-1). All three defer domain ids to the adjudicated document and leave QUESTION-LINK and OB-H1 undefined (CLAR-4 NOT MET for all).
- **Risk:** no variant gives a probability for any risk (RISK-1 NOT MET for all); all three miss an "Orca app not running" trigger (invariant-probe INV-009), noted as a residual under RISK-4 but not scored against it.
- **Residual invariant gaps not charged as NOT MET** (the rubric criteria are met by other cited coverage): INV-004 `filter.<driver>.process` (V2:652 comes closest; V1:714 names other keys and `GIT_*` env; V3 names only the two keys); INV-013 single M-APPROVAL node (V3 only); INV-002 coordinator home (V1 names the main checkout as PLAN INFERENCE at V1:327; V2 forbids the main checkout at V2:537; V3 leaves it to the execution package).

## Edge Case Floor Check

| Variant | Invariant & Edge Case Coverage | Floor (at least 1/5) | Eligible as base |
|---|---|---|---|
| V3 (backend) | 5/5 | met | yes |
| V2 (analyzer) | 5/5 | met | yes |
| V1 (architect) | 5/5 | met | yes |

The floor is not suspended (no variant scores 0/5).

## Machine-readable verdict table

1 = MET, 0 = NOT MET. Columns in input order for diffing against pass 1.

```text
criterion | V1 | V2 | V3
COMP-1    | 1  | 1  | 1
COMP-2    | 1  | 1  | 1
COMP-3    | 1  | 1  | 1
COMP-4    | 1  | 1  | 1
COMP-5    | 1  | 1  | 1
CORR-1    | 0  | 0  | 1
CORR-2    | 0  | 0  | 0
CORR-3    | 1  | 0  | 1
CORR-4    | 0  | 0  | 0
CORR-5    | 1  | 1  | 1
STRU-1    | 1  | 1  | 1
STRU-2    | 1  | 1  | 1
STRU-3    | 1  | 1  | 1
STRU-4    | 1  | 1  | 1
STRU-5    | 1  | 1  | 1
CLAR-1    | 1  | 0  | 0
CLAR-2    | 1  | 1  | 1
CLAR-3    | 1  | 1  | 1
CLAR-4    | 0  | 0  | 0
CLAR-5    | 1  | 1  | 1
RISK-1    | 0  | 0  | 0
RISK-2    | 1  | 1  | 1
RISK-3    | 1  | 1  | 1
RISK-4    | 1  | 1  | 1
RISK-5    | 1  | 1  | 1
INV-1     | 1  | 1  | 1
INV-2     | 1  | 1  | 1
INV-3     | 1  | 1  | 1
INV-4     | 1  | 1  | 1
INV-5     | 1  | 1  | 1
TOTAL     | 25 | 23 | 25
QUAL      | 0.833 | 0.767 | 0.833
```
