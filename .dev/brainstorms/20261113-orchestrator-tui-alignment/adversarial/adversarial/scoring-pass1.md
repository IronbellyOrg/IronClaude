# Base Selection Report: Scoring Pass 1 (input order V1, V2, V3)

Template: `~/.claude/skills/sc-adversarial-protocol/refs/artifact-templates.md` Section 3; algorithm: `refs/scoring-protocol.md` A.1 to A.4.

Scorer: pass 1 (input order V1, V2, V3). Read-only except this file. Run 2026-11-13.

- V1 = `variant-1-opus-architect.md` (751 lines), V2 = `variant-2-opus-analyzer.md` (719 lines), V3 = `variant-3-haiku-backend.md` (662 lines).
- Requirements: seed brief Success Criteria 1 to 12 (R1 to R12) and the six Constraint bullets (C1 to C6) of `seed-brief.md:55-60`; 18 requirements.
- Evidence used: the three variants (read in full), `diff-analysis.md` (contradictions and SC spot checks), `invariant-probe.md`, `debate-transcript.md` Scoring Matrix (note only), `src/superclaude/core/WORKER-CONTRACT.md:23,243` (read to confirm the INV-001 premise).
- Line numbers below are the variant files' own lines.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (architect) | V2 (analyzer) | V3 (backend) |
|--------|--------|----------------|---------------|--------------|
| requirement_coverage | 0.30 | 1.0000 (18/18) | 1.0000 (18/18) | 1.0000 (18/18) |
| internal_consistency | 0.25 | 0.9946 (1 - 2/368) | 0.9952 (1 - 2/417) | 0.9925 (1 - 2/267) |
| specificity_ratio | 0.15 | 1.0000 (454 / (454 + 0)) | 1.0000 (474 / (474 + 0)) | 0.9917 (360 / (360 + 3)) |
| dependency_completeness | 0.15 | 1.0000 (1169/1169) | 0.9992 (1200/1201) | 1.0000 (768/768) |
| section_coverage | 0.15 | 1.0000 (8/8 H2) | 1.0000 (8/8 H2) | 1.0000 (8/8 H2) |
| **quant_score** | | **0.9986** | **0.9987** | **0.9969** |

Exact values: V1 0.30 + 0.248641 + 0.15 + 0.15 + 0.15 = 0.998641. V2 0.30 + 0.248801 + 0.15 + 0.149875 + 0.15 = 0.998676. V3 0.30 + 0.248127 + 0.148760 + 0.15 + 0.15 = 0.996888.

The quantitative layer barely separates the three (spread 0.0018): all three share one seed and one source, so every grep-level requirement and every internal id resolves in all of them. The decision is carried by the qualitative layer.

### RC: requirement coverage (counting method and raw counts)

Method: one grep pattern per requirement (case-insensitive `grep -c`). A requirement counts as covered when its threshold is met. For R1 to R7 the threshold is 6 hits (one per system), because the seed asks for each item per system.

| Req | Pattern (grep -E) | Threshold | V1 | V2 | V3 |
|---|---|---|---|---|---|
| R1 Scope | `^\*\*Scope\.\*\*` | 6 | 6 | 6 | 6 |
| R2 Current state | `^\*\*Current state` | 6 | 6 | 6 | 6 |
| R3 Target state | `^\*\*Target state` | 6 | 6 | 6 | 6 |
| R4 Work items with ids and AC | `^\| id \| title` (-i) | 6 | 6 | 6 | 6 |
| R5 Blocked-by and blocks | `^\| id \| title.*blocked-by \| blocks` (-i) | 6 | 6 | 6 | 6 |
| R6 Owner decisions | `^\| Q([1-9]\|1[0-9]\|2[0-4]) \|` rows, plus a "default if unanswered" header | 24 rows + 1 | 24 + 1 | 24 + 1 | 24 + 1 |
| R7 Risks and reversibility | `^\*\*Risks` and a work-item header with `undo\|rev\.\|reversibility` | 6 + 6 | 6 + 6 | 6 + 6 | 6 + 6 |
| R8 Dependency graph | `^## 4\. Cross-system dependency graph` (dangling refs: see DC) | 1 | 1 | 1 | 1 |
| R9 Lockstep waves | `^## 5\. Ordered lockstep schedule of waves` | 1 | 1 | 1 | 1 |
| R10 Chain to target | `^## 1\. Chain to target` | 1 | 1 | 1 | 1 |
| R11 Orchestrator session needs | `^## 6\. What an orchestrator session needs` plus 8 keywords (inputs, worktree map, roles, guardrails, stop, escalat, polling, decision ledger) | 1 + 8/8 | 1 + 8/8 | 1 + 8/8 | 1 + 8/8 |
| R12 Invariant-based convergence, INV-008 first | first line containing `INV-008`; `^## 7\. Invariants and edge cases` | first in section 0; 1 | line 7; 1 | line 7; 1 | line 6; 1 |
| C1 Read-only discipline | `changes nothing\|posts nothing\|nothing here was run\|written specification only\|proposal, not authorization` | 1 | 1 | 2 | 2 |
| C2 Project rules | 5 clause keyword sets: `pr-submit --monitor 3` + `IronbellyOrg/IronClaude`; `\.claude/`; `\.dev/tasks`; worktree clause = `--agent`, or one line holding "worktree", "Orca" and "agent"; `WC-13` | 5/5 | 5/5 | 5/5 | 5/5 (no literal `--agent`; worktree clause met by line 163 "creates any required worktree through Orca with agent") |
| C3 Q not the spec's to make; defaults | `default if unanswered\|unanswered default` | 1 | 4 | 2 | 5 |
| C4 Facts stay marked | `PLAN INFERENCE` / `UNVERIFIED` | 1 / 1 | 53 / 13 | 17 / 20 | 38 / 11 |
| C5 Single owner, user, host | `single owner, single OS user, single host\|one owner, one OS user, one host\|one-host, one-owner, one-OS-user` | 1 | 2 | 2 | 1 |
| C6 Nothing new inside PR #539 | `A-004` | 1 | 9 | 9 | 2 |
| **Covered** | | | **18/18** | **18/18** | **18/18** |

### IC: internal consistency (counting method, sample and contradictions)

Denominator (scorable claims): table data rows (all `^\|` rows minus two per table for header and separator) plus list items (`^\s*([-*]\|[0-9]+\.) `). V1: 270 - 2x22 = 226 rows + 142 items = 368. V2: 356 - 2x23 = 310 + 107 = 417. V3: 222 - 2x18 = 186 + 81 = 267.

Contradictions counted: only those shown from the variant's own text (opposing claims, requirement-constraint conflict, impossible sequence). Conflicts that need an outside source (X-011/A-002 for all three; INV-001 for V1, V2) are scored in the qualitative Correctness dimension, not here.

| Id | Variant | Claim A (line) | Claim B (line) | Source |
|---|---|---|---|---|
| IC-V1-1 | V1 | XC-01 ledger at `.dev/brainstorms/20261113-orchestrator-tui-alignment/decision-ledger.md` (319) | "This checkout IS PR #539's head; a note committed here joins #539" (332); 6.9 never adds files to #539 (640) | diff X-012 |
| IC-V1-2 | V1 | Q3 default "CO-01 not posted; nothing in IronClaude waits" (346) | hard chain `XC-02 -> WA-02 -> CO-01 -> OB-08 -> SW-09 -> V2-01` (436); OB-08 blocked-by CO-01 (183) | invariant-probe INV-003 |
| IC-V2-1 | V2 | "What never waits for #539: ... XC-04 to XC-06" (507) | XC-05 scheduled in Wave 3, gate "SW-06 merged" (499) | diff X-015 |
| IC-V2-2 | V2 | "Edits must be one ordered set by one editor (A-011)" (268) | #450 edited by three separate items WA-02, WA-03, WA-04 (182-184) across Waves 1 and 2 (497-498) | diff X-006 |
| IC-V3-1 | V3 | W1 "XC-03 draft in K, no links/commit into S" (444) | XC-03 blocked by SW-03, SW-05 (241); the register has no draft item | diff X-015 |
| IC-V3-2 | V3 | "SW-04, SW-05 and XC-07 retain follow-ups with named owners" (77) | SW-05 is "Shared capture and identity comparison" (112) | diff X-015 |

Sampled claim pairs checked and found consistent (no contradiction), 5 per variant:
- V1: SW-04 blocks OB-06 (134) and OB-06 blocked-by SW-04 (181); 4.3 "critical path ... SW-05 -> XC-06 -> XC-07" against XC-06 blocked-by SW-05 (324); OB-03 before OB-04 in 5.3 and OB-04 blocked-by OB-03 (179); W2 exit "#539 merged (or held on Q1 default)" against Q1 default (344); "46 work items" (377) against register count 46 (SC-41).
- V2: "Work items (50)" (337) against register count 50 (SC-41); edge 20 `XC-03 -> OB-05` against OB-05 blocked-by XC-03 (144); Weak point W3 removes SW-06 -> OB-05 and OB-05 blocked-by has no SW-06 (144); 70 edges numbered contiguously (invariant-probe INV-020); "What waits for #539" OB-06 against edge 25 FILE.
- V3: "33 unique register rows" (644) against count 33 (SC-41); OB-03 blocked-by SW-02 (#541) and rule 5 "It waits for #541" (457); XC-04 blocked-by XC-03 (242) and graph `XC-03 + C-SNAPSHOT + C-SWEEP -> XC-04` (384); Q24 "does not authorize OB-02 writes" (420) and Authority-not-granted line (323); CO-01 before OB-04 in XC-02 sequence (240) and OB-04 blocked-by CO-01 (138).

### SR: specificity ratio (counting method and raw counts)

Substantive lines = all lines minus YAML frontmatter, blank lines, headings (`^#`), table separators and code fences. Concrete line = contains a digit or a backtick (numbers, ids, file:line, named commands). Vague line = matches `\b(appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices?|industry standard)\b` (-i). SR = concrete / (concrete + vague); lines that are neither are excluded, as the protocol formula does.

| | V1 | V2 | V3 |
|---|---|---|---|
| Substantive lines | 508 | 522 | 442 |
| Concrete | 454 | 474 | 360 |
| Vague | 0 | 0 | 3 ("as needed" 443, "Appropriate owner answers" 444, "adequate plans" 517) |
| Neither | 54 | 48 | 82 |

### DC: dependency completeness (counting method and raw counts)

Internal reference = every occurrence (definition sites included) of an internal id family. Resolved = the id has a definition row in the same file. Sets were compared with `grep -o | sort -u | comm`. Section references exclude the three that point into `docs/designs/orchestrator-mode.md` ("Design section 7.5", "section 17", "`.md` section 1"), which are external.

| Family | V1 occ (undefined) | V2 occ (undefined) | V3 occ (undefined) |
|---|---|---|---|
| Work items `(SW\|OB\|WA\|CO\|V2\|XC)-nn` | 1005 (0; 46 defined, 46 used) | 954 (0; 50/50) | 672 (0; 33/33) |
| Graph nodes | K-/TB- 70 (0; 14 defined) | K-/TB- 68 (0; 15 defined) | B-/C-/M- 62 (0; 14 defined) |
| Local ids | chain links L1-L4 28 (0); waves W0-W5 36 (0) | Weak points W1-W8 30 (0); N1-N4 6 (0); I-* 36 (0; 27 defined); R-* 36 (0; 25 defined); L1-L4 24 (0); "Wave n" 5 (0) | waves W0-W6 11 (0) |
| Internal section refs | 30 (0) | 42 (1) | 23 (0) |
| **Total** | **1169 (0)** | **1201 (1)** | **768 (0)** |

The one unresolved V2 reference: XC-01 runs in "the orchestrator session's checkout (Section 6.2)" (278), but Section 6.2 names no checkout for the coordinator; it marks the main checkout "Not used by this program" (537). Diff X-012 records the same gap.

### SC: section coverage

H2 count (`^## `): V1 8, V2 8, V3 8; max 8. (V1's `# ---` lines at 410-487 are inside a code fence and are not H2.)

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV convention: in every row the CLAIM is "<criterion> is met in Vn"; the Evidence cell is the EVIDENCE (a quote of at most 15 words with its line, a section reference, or "No evidence found - searched: ..."); the verdict cell is the VERDICT, MET (1) or NOT MET (0). No evidence for MET means NOT MET. Variants were evaluated in input order V1, V2, V3 within each row.

### Completeness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET (1) | RC 18/18; 4.3 (492) "No dangling reference." | MET (1) | RC 18/18; 4.2 (441) "Every work item appears as a 'To' or as a root" | MET (1) | RC 18/18; 7 (637) table "Coverage of the twelve required outcomes", rows 1-12 |
| Addresses edge cases/failures | MET (1) | 7.4 (729-738), 10 cases, e.g. "Q1 never answered. #539 stays open" | MET (1) | 7.3 (670-680), 11 rows, e.g. "OB-03 shows a seeded message missing" | MET (1) | 7 Edge-case runbook (622-633), e.g. "Interrupted live launch: preserve unknown state" |
| Includes dependencies/prerequisites | MET (1) | 4.2 graph (409-488); blocked-by/blocks in all 6 registers | MET (1) | 4.2 (368-439): 70 edges, each "Evidence that the dependency is real" | MET (1) | 4 (350-391) "Work graph: every work item"; Blocked-by column |
| Defines success/completion criteria | MET (1) | 5.1 (505) "Exit check (all must hold, or the item is recorded...)" | MET (1) | 2 (75) "after 'Observe:', the command, file or record a reviewer uses" | MET (1) | Register header "Checkable acceptance criteria"; 5 "Exit check" column (441) |
| Specifies out-of-scope items | MET (1) | 1.3 (92) "What stays out of scope until later" | MET (1) | 0.4 (55) "Multi-host, TUIBBS and building any code are out of scope" | MET (1) | 1 (84) "No persisted sweep JSON sidecar, observer sweep reader, shared collector..." |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| No factual errors or hallucinated claims | NOT MET (0) | 0.4 item 5 (57): packages "were **not found in this checkout**"; diff SC-01: both exist, WRONG | NOT MET (0) | 6.3 (562) "#539 author | The worker in `issue-339-orchestrator-mode`": no source names it, unmarked (diff A-004; withdrawn in debate) | MET (1) | Diff spot checks on V3 claims SC-02, SC-30, SC-31 all CONFIRMED; no WRONG row; 0 state table (24-35) matches E-ids |
| Feasible with stated constraints | NOT MET (0) | 6.3 (575) Worker "PR via `/sc:pr-submit --monitor 3`"; `WORKER-CONTRACT.md:23` lists pr-submit never-as-worker (INV-001); XC-04 runs the unfixed sweep before the INV-008 ruling (X-002) | NOT MET (0) | 6.7 (610) "owned by `/sc:pr-submit --monitor 3` in the worker that opened it"; contradicts `WORKER-CONTRACT.md:23`, `:243` (INV-001) | MET (1) | Role contract (507-508): Coordinator "perform approved external writes"; Item worker "return artifact/test evidence". Residual X-011 shared by all three |
| Terminology consistent | NOT MET (0) | "SEED" is the seed brief (0.2, 24) and the test "Seeded consumption test (SEED)" (178) | NOT MET (0) | L1 gate (64) "SW-12 (Phase 2 of #339) started" while the seed calls #444 Phase 2; no marker (X-010, conceded) | MET (1) | One short name per source ("Seed", "Adjudicated", 10-12); #444 named, never numbered: "#444 evaluation linked" (113) |
| No internal contradictions (cross-check IC) | NOT MET (0) | IC-V1-1 (319 vs 332), IC-V1-2 (346 vs 436) | NOT MET (0) | IC-V2-1 (507 vs 499), IC-V2-2 (268 vs 182-184) | NOT MET (0) | IC-V3-1 (444 vs 241), IC-V3-2 (77 vs 112) |
| Claims supported by evidence/rationale | MET (1) | 0.2 (28) citation convention; every current-state bullet carries E-/INV- ids | MET (1) | 4.2 evidence column on all 70 edges; OBS-NOW checks name their command (43) | MET (1) | Bracketed source on each paragraph, e.g. (39) "[INV-008; Part 2.2 action 1.]" |
| **Subtotal** | **1/5** | | **1/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| Logical section ordering | MET (1) | Sections 0-7 in seed order; 2 (107) "in the order of their first gating dependency" | MET (1) | Sections 0-7 in seed order: status, chain, register, decisions, graph, waves, session, invariants | MET (1) | 0 (51) "Sections 4 and 5 are the dependency and execution views of that same register" |
| Consistent hierarchy depth | MET (1) | Heading scan: H2 0-7, H3 numbered n.m, none outside its H2 | MET (1) | Heading scan: H2 0-7, H3 numbered n.m, none outside its H2 | MET (1) | Heading scan: H2 0-7, H3 unnumbered, each under its H2 |
| Clear separation of concerns | MET (1) | Systems 2.1-2.6; decisions 3; graph 4; waves 5; session 6 | MET (1) | Same split; edges isolated in 4.2, graph deltas in 4.4 | MET (1) | 0 (51) "Section 2 is the work register; Section 3 owns decision defaults" |
| Navigation aids present | MET (1) | 2 (107) "Every row's blocked-by and blocks ids resolve in section 4." | MET (1) | 0.3 "How to read this spec" (41); 42 internal section references | MET (1) | 0 "Reading the plan" (49-51) maps Sections 1-7 |
| Follows artifact-type conventions | MET (1) | YAML frontmatter with status (1-9); stable ids; AC per item (0.5) | MET (1) | YAML frontmatter with status (1-8); stable ids; AC with "Observe:" | MET (1) | Status line (6) "BLOCKED_BY_INVARIANTS"; stable ids; AC column (no frontmatter; not required) |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | MET (1) | Vague-term grep (SR): 0 hits in 508 substantive lines | MET (1) | Vague-term grep (SR): 0 hits in 522 substantive lines | NOT MET (0) | W1 gate (444) "Appropriate owner answers and separate write consent per lane"; W0 (443) "only as needed" |
| Concrete rather than abstract | MET (1) | SW-02 (132) regression test "fails on the current argv"; pins `test_readonly.py:85,156,453` | MET (1) | SW-02 (98) "Observe: `uv run pytest tests/sweep/ -v` passes" | MET (1) | OB-02 (136) "create probe Run without run-use; seed question, worker_done and heartbeat" (worktrees are role letters only) |
| Section purpose statement | MET (1) | 6 (549) "This section specifies the coordinator session of XC-09" | MET (1) | 6 (513) "This section is for the person-opened coordinator session" | MET (1) | Each H2 opens with a purpose line, e.g. 7 (554) "acceptance tests for the plan" |
| Acronyms/terms defined on first use | NOT MET (0) | First use (40) "release 3 behind QUESTION-LINK (not established)", never defined; 0.2 defers to ADJ Part 0.3 | NOT MET (0) | First use (31) "release 3 gated behind QUESTION-LINK, not established", never defined | NOT MET (0) | First use (34) "QUESTION-LINK is not established", never defined; FU-1 unglossed at first use (157) |
| Actionable next steps/decisions | MET (1) | 5.2 (514) "What may run today, before any owner answer" | MET (1) | 5 (503) "What can run today, before any owner answer" | MET (1) | 3 (319) "Decision runbook ... Q1 is first." |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| >=3 risks with probability and impact | NOT MET (0) | No evidence found - searched the six "Risks" blocks (145-152, 186-194, 225-230, 255-261, 288-294, 329-336): no probability or impact rating | NOT MET (0) | Impact only: (112) "R-SW1 (security, HIGH)"; no probability on any of 25 R-rows | NOT MET (0) | No evidence found - searched every "Risks" paragraph (122, 150, 177, 202, 228, 287): no probability or impact rating |
| Mitigation for each risk | NOT MET (0) | (229) "Host-only facts. ... other hosts UNVERIFIED (INV-011)." states no mitigation | NOT MET (0) | (196) R-WA5 "ClickUp writes made by FU-1 may not be reversible" states no mitigation; 7.4 (712) INV-032 "Gap" | NOT MET (0) | (122) "Full build divergence remains unresolved even if the release prefix matches." states no mitigation |
| Failure modes and recovery | MET (1) | 6.5 (604) "abort the edit; re-read; re-map; ask before retrying" | MET (1) | 6.5 (587) "Abort that write; re-read; re-map locators to quoted sentences; re-prepare" | MET (1) | (466) "At resume, read authoritative state before emitting any write." |
| External dependencies and their failure | MET (1) | 7.4 (733) "Orca is upgraded mid-plan. OB-05's check fails" | MET (1) | 7.3 (675) "The Orca build changes mid-program" | MET (1) | (623) "Orca full build differs: stop build-dependent gates"; (630) stopped remote workspace |
| Monitoring/validation for risk detection | MET (1) | XC-06 (324) "the test fails when any of them changes without the note" | MET (1) | 7.1 each invariant has a "Check", e.g. (620) `git grep -n "QUESTION_GATE_PASSED ="` | MET (1) | XC-04 (242) "deliberate mutation demonstrates failing check"; XC-08 independent gate (246) |
| **Subtotal** | **3/5** | | **3/5** | | **3/5** | |

Note: no variant covers "Orca app not running" as a failure of an external dependency (invariant-probe INV-009); V3 only states "ran no live Orca" (656). Not scored against the criterion, which all three meet through the Orca-build case.

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| Collection boundaries (empty, single, max) | MET (1) | 7.2 (702) "excluding empty and duplicate-flagged rows"; (699) "at most 50 rows" | MET (1) | I-L1 (636) "excludes empty and duplicate-flagged rows"; I-C3 (632) "at most 50" | MET (1) | (627) "Duplicate/empty row identity: exclude from joins"; (624) "Worker list truncated: mark PARTIAL" |
| State interactions across components | MET (1) | 7.2 (705) "Neither program reads the other at runtime in version 1" | MET (1) | I-I4 (644) "The two programs resolve `XDG_STATE_HOME` differently" | MET (1) | (144) "Multiple producers can replace one another's snapshot" |
| Guard condition gaps | MET (1) | 7.2 (695) "`check_run_id` checks syntax only" guarded by OB-06 (a) test | MET (1) | I-G3 (627) "refused by code, not by documentation" | MET (1) | (150) "Global boolean scope can exceed a one-Run pass." |
| Count divergence | MET (1) | 7.2 (698) "at most 5 calls x 100 rows ... (6 calls with `--questions`)" | MET (1) | I-C2 (631) "at most 5 `worker-list` calls per cycle (6 with `--questions`)" | MET (1) | 7 Count row (563) falsifier "six-call cycle is described as five total" |
| Interaction effects when features combine | MET (1) | 7.4 (735) "Two coordinators or several observers run at once. Load multiplies" | MET (1) | I-I2 (642) "SW-08 and XC-07 both edit `docs/designs/orchestrator-mode.md`" | MET (1) | Rule 8 (460) "Shared capture and seeded consumption test are not interchangeable" |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

What the invariant probe found each variant got wrong (recorded for the reconciler; the criteria above are met on the dimension, these are residual gaps):
- Workers running `/sc:pr-submit --monitor 3` (probe INV-001): V1 (575), V2 (563, 610). Not V3. Scored under Correctness criterion 2.
- Coordinator home (probe INV-002): V1 names the main checkout (327, PLAN INFERENCE) but puts the ledger in the #539 checkout (319); V2 names no home (278 vs 537); V3 "no new worktree required" (496), no path. None fully resolves it.
- Order stall under defaults (probe INV-003): V1 states "nothing in IronClaude waits" against a hard chain (IC-V1-2). V3 has the same stall (OB-04 blocked-by CO-01, 138; Q3 default "No #477 rewrite", 296) but states it as "Default-blocked lanes stay blocked" (454), so it is a stall, not a contradiction. V2 avoids it by making the order soft, which the debate rejected (X-005).
- Two-key regression test (probe INV-004): V1 SW-02 (132) and V2 SW-02 (98) fix the test to `core.fsmonitor` plus `filter.*.clean`; V3 SW-01 (108) "regression evidence of the measured experiment". None covers `filter.<driver>.process`; V1 7.3 (714) and V2 7.2 (652) name other keys and inherited env as falsifiers only.

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 1/5 | 1/5 | 4/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 3/5 |
| Risk Coverage | 3/5 | 3/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 | 5/5 |
| **qual_score** | **23/30 = 0.7667** | **23/30 = 0.7667** | **25/30 = 0.8333** |

### Edge-case floor check

| Variant | Invariant & Edge Case | Floor (>= 1/5) | Eligible as base |
|---|---|---|---|
| V1 | 5/5 | pass | yes |
| V2 | 5/5 | pass | yes |
| V3 | 5/5 | pass | yes |

Floor not suspended (no variant scored 0/5).

## Position-Bias Mitigation

This file is pass 1 only (input order V1, V2, V3). Pass 2 (reverse order) and the re-evaluation of any criterion where the passes disagree belong to the reconciler (scoring-protocol A.5). Pass 1 verdicts that turn on a judgment call, and so are the likeliest to disagree, are listed for the reconciler:

| Criterion | Variant | Pass 1 | Why it is a judgment call |
|---|---|---|---|
| Correctness 1 (no factual errors) | V2 | NOT MET | Rests on an unmarked actor claim (562), not a spot-check WRONG row like V1's SC-01 |
| Correctness 2 (feasible) | V3 | MET | X-011 (pr-submit autonomy against "authorization for every outward write", 485) is unstated in V3 too; scored MET because V3 does not give the PR tool to a worker |
| Correctness 3 (terminology) | V1 | NOT MET | One label collision ("SEED", 24 and 178) |
| Clarity 1 (unambiguous) | V3 | NOT MET | Three vague words, one in a wave gate (444) |
| Risk 2 (mitigation for each) | all | NOT MET | Strict "for each": one unmitigated risk found per variant |

Disagreements re-evaluated: n/a in pass 1. Final verdicts changed: n/a in pass 1.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate tiebreaker (outright Round 2 wins of 44 points) |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (opus-architect) | 0.4993 | 0.3833 | **0.8827** (0.882654) | 9 |
| V2 (opus-analyzer) | 0.4993 | 0.3833 | **0.8827** (0.882671) | 11 |
| V3 (haiku-backend) | 0.4984 | 0.4167 | **0.9151** (0.915111) | 4 |

Debate wins are from `debate-transcript.md` Convergence Assessment (1033): MERGE 17, V2 11, V1 9, V3 4, NEITHER 3. Used for this note only.

**Ranking (pass 1):** 1. V3 0.9151; 2. V2 0.8827; 3. V1 0.8827 (V2 ahead of V1 by 0.00002, from IC and DC only).

**Margin:** V3 over V2 = 0.0324 (3.24 points; 3.7 percent of V2's score). This is **below** the 5 percent threshold of scoring-protocol A.4 (|A - B| < 0.05), so the top two are within 5 percent. V2 and V1 are tied to four decimals.

**Tiebreaker applied:** No (deferred to the reconciler as instructed). For the record: A.4 step 1 compares debate wins between the top two; V2 won 11 points and V3 won 4.

## Selected Base: Variant V3 (haiku-backend), provisional, pass 1 only

### Selection Rationale

V3 has the highest pass 1 combined score. The quantitative layer is flat (all three at 0.997 to 0.999, RC 18/18 each), so the result comes from Correctness: V3 4/5 against 1/5 for V1 and V2. V1 states a checked-wrong fact (SC-01) and V2 asserts an unrecorded actor (562); both give `/sc:pr-submit --monitor 3` to workers, which `WORKER-CONTRACT.md:23` and `:243` forbid (invariant-probe INV-001), and each has one terminology collision. V3 loses one Clarity point for vague wave-gate wording (443-444). All three have two internal contradictions and the same Risk gaps (no probability ratings, one unmitigated risk each). The lead is inside the 5 percent band, so this selection is provisional until pass 2 and the A.4 tiebreaker are applied by the reconciler.

### Strengths to Preserve from Base (V3)
1. Interface, failure, retry and idempotency contracts per system (sweep, snapshot, question read, launch, store, remote read, issue edit, PR merge; diff U-010, debate V3 win).
2. XC-08 two-scope independent gate and the contract completion rule (1, 88-92; U-011).
3. "Decision lifetime" and "Authority not granted by these questions" (321-323; U-012); wave interruption rule (464-468).
4. Role contract that keeps PR and external writes with the coordinator, not item workers (507-508).

### Strengths to Incorporate from Non-Base Variants
1. From V2: edge kinds with per-edge evidence (4.2, 70 edges; S-003, U-004), Weak points W1 to W6 (U-005), "Observe:" commands in every AC, the TB-1 -> XC-05 edge (do not run the unfixed sweep for JOIN; X-002), early #423 research (V2-04; X-008), SW-13 conditional `working` class (W5; X-009), the verified worktree map (6.2, SC-27).
2. From V1: one #450 edit set and the hard cross-issue order (X-005, X-006, C-004), the live-layout attempt ordering (OB-03 -> OB-04 -> OB-06; C-003), the 1.4 numbering CONTRADICTION MARKER (X-010), the INV coverage map by severity (7.1), the `/sc:sweep` install caveat (7.3; A-001), named worktrees and the "Wave needed by" column (S-006, A-006).
3. Fixes none of the three has: name the PR actor (INV-001), the coordinator home and ledger branch (INV-002), a skip rule for defaulted links in the hard order (INV-003), widen the regression test to `filter.<driver>.process` (INV-004), keep pr-submit off the INV-008 thread on #539 until Q1 is applied (INV-005).
