# Base Selection

Variants: V1 = Option A (repo-local `.superclaude/memory/`), V2 = Option B (Claude Code auto-memory), V3 = Option C (drop memory).
Scoring inputs: the three option files, `context.md`, `diff-analysis.md` evidence E1-E10, `debate-transcript.md`.
Method note: the quantitative metrics were tallied by hand from the option texts (no script), so counts are listed to make them re-checkable. Source requirements have no formal IDs, so section-level topic matching is used (per the protocol edge case).

## Quantitative Scoring (50% weight)

Source requirement topics (8), from `context.md`: (1) /sc:save and /sc:load, (2) pm-agent, (3) MODE_Task_Management, (4) sc-roadmap persistence, (5) sc-reflect calibration memory, (6) sc-crash-recovery, (7) portability to other projects, (8) tests and routing docs.

| Metric | Weight | V1 (A) | V2 (B) | V3 (C) | Computation |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.625 | 0.500 | 0.750 | Topics named in each text: V1 = 5/8 (1 save/load, 5 reflect, 6 crash-recovery, 7 portability, 8 the "description says file memory" doc edit; the generic "each Serena memory tool call" does not count as naming pm-agent, MODE_Task_Management or roadmap). V2 = 4/8 (1, 2, 7, 8). V3 = 6/8 (1, 2, 3, 4, 5, 8) |
| Internal consistency (IC) | 0.25 | 1.00 | 0.90 | 0.90 | Internal contradictions per ~10 claims: V1 0; V2 1 (X-001); V3 1 (X-002). Disagreement with repo evidence (X-004, X-003) is scored under Correctness, not here |
| Specificity ratio (SR) | 0.15 | 0.857 | 0.600 | 0.786 | concrete/(concrete+vague): V1 12/14; V2 6/10; V3 11/14 |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 0.60 | Internal references resolved: V1 3/3 (docs/memory, .superclaude ignored, tracked reflect file); V2 3/3; V3 3/5 ("Phase 3" and "~12 doc pages" do not resolve) |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | All three have the same three blocks (title, proposal, pros/cons) |
| **quant_score** | | **0.8661** | **0.7650** | **0.8079** | RC x0.30 + IC x0.25 + SR x0.15 + DC x0.15 + SC x0.15 |

Arithmetic: V1 = 0.1875 + 0.2500 + 0.1286 + 0.1500 + 0.1500 = 0.8661. V2 = 0.1500 + 0.2250 + 0.0900 + 0.1500 + 0.1500 = 0.7650. V3 = 0.2250 + 0.2250 + 0.1179 + 0.0900 + 0.1500 = 0.8079.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Two independent passes. Pass 1 (input order A, B, C) was done by the orchestrator. Pass 2 (reverse order C, B, A) was done by an independent agent that was not shown Pass 1. Final verdicts below are the agreed verdicts; disagreements were re-evaluated with both passes' evidence side by side (next section). Only MET verdicts carry evidence; every other criterion is NOT MET ("none found").

### Completeness (5 criteria)
| Criterion | V1 (A) | V2 (B) | V3 (C) | Evidence for MET |
|---|---|---|---|---|
| C1 covers all explicit requirements | 0 | 0 | 0 | none: V1 omits pm-agent, MODE_Task_Management, roadmap; V2 omits five of eight; V3 omits crash-recovery and portability |
| C2 edge cases and failure scenarios | 1 | 1 | 1 | V1 "not shared across worktrees (each worktree has own copy ...)"; V2 "instructions must be conditional on the harness feature being enabled"; V3 "users who rely on /sc:save get a breaking removal" |
| C3 dependencies and prerequisites | 1 | 1 | 1 | V1 "zero dependency", "`.superclaude/` is already gitignored"; V2 "Claude Code specific"; V3 "relies on existing mechanisms: git, `.dev/tasks/` ..." |
| C4 success criteria | 0 | 0 | 0 | none found |
| C5 out of scope | 0 | 0 | 0 | none found |
| Subtotal | 2 | 2 | 2 | |

### Correctness (5 criteria)
| Criterion | V1 (A) | V2 (B) | V3 (C) | Evidence |
|---|---|---|---|---|
| R1 no factual errors | 0 | 0 | 0 | V1 "prompts change by tool name only" is wrong (E9, E10, E1); V2 "slug differs per worktree path" is wrong (E7); V3 reads E4 as obsolescence and "no gap" (X-002, X-003) |
| R2 feasible within constraints | 1 | 0 | 1 | V1 "native tools" work anywhere; V3 meets no-new-MCP, smallest-change and works-anywhere (its capability loss is scored under Completeness); V2 fails the other-projects constraint by its own cons |
| R3 terminology consistent | 1 | 1 | 1 | V1 "Write for write_memory, Read for read_memory ..."; V2 "MEMORY.md index", "slug" used consistently; V3 "docs/memory/ files that pm-agent already documents" is accurate (E6) |
| R4 no internal contradictions | 1 | 0 | 0 | V1 none; V2 X-001; V3 X-002 |
| R5 claims supported by rationale | 1 | 0 | 1 | V1 "Same shape as Serena's own store (flat markdown ...)"; V3 quotes HOW-WE-WORK, names tests; V2's key worktree claim is unsupported and wrong |
| Subtotal | 4 | 1 | 3 | |

### Structure (5 criteria)
| Criterion | V1 (A) | V2 (B) | V3 (C) | Evidence |
|---|---|---|---|---|
| T1 logical ordering | 1 | 1 | 1 | description, then pros, then cons |
| T2 consistent hierarchy | 1 | 1 | 1 | single H1, uniform body |
| T3 separation of concerns | 1 | 1 | 1 | proposal text separate from Pros/Cons line |
| T4 navigation aids | 0 | 0 | 0 | none found |
| T5 artifact conventions | 1 | 1 | 1 | description plus pros and cons, as other option files |
| Subtotal | 4 | 4 | 4 | |

### Clarity (5 criteria)
| Criterion | V1 (A) | V2 (B) | V3 (C) | Evidence |
|---|---|---|---|---|
| L1 unambiguous language | 0 | 0 | 1 | V1 "(or docs/memory/ if it must be shared via git)" left open; V2 "can change", "not guaranteed"; V3 states its deletion list plainly |
| L2 concrete | 1 | 1 | 1 | V1 exact paths and per-tool mapping; V2 `~/.claude/projects/<slug>/memory/`; V3 names git, `.dev/tasks/`, progress.md, `docs/memory/`, ccsession |
| L3 clear purpose per section | 1 | 1 | 1 | each paragraph has one role |
| L4 terms defined on first use | 0 | 0 | 0 | none define Glob, slug, TodoWrite, ccsession |
| L5 actionable next steps | 1 | 0 | 1 | V1 "Replace each Serena memory tool call with native tools on ..."; V3 "Delete /sc:save and /sc:load, ..."; V2 gives no per-consumer steps |
| Subtotal | 3 | 2 | 4 | |

### Risk Coverage (5 criteria)
| Criterion | V1 (A) | V2 (B) | V3 (C) | Evidence |
|---|---|---|---|---|
| K1 at least 3 risks with probability and impact | 0 | 0 | 0 | none found |
| K2 mitigation for each risk | 0 | 0 | 0 | V1 has partial hints only |
| K3 failure modes and recovery | 0 | 0 | 0 | none found |
| K4 external dependencies and their failure | 0 | 1 | 0 | V2 "path and format owned by Anthropic and can change"; V1 "zero dependency" names no failure scenario |
| K5 monitoring or validation mechanism | 0 | 0 | 0 | V1 "testable" is asserted, no mechanism |
| Subtotal | 0 | 1 | 0 | |

### Invariant & Edge Case Coverage (5 criteria)
| Criterion | V1 (A) | V2 (B) | V3 (C) | Evidence |
|---|---|---|---|---|
| I1 collection boundaries (empty store) | 0 | 0 | 1 | V3 "pm-agent 'session start restore context' has nothing to restore" |
| I2 state interactions across component boundaries | 1 | 1 | 0 | V1 "Tracked `.serena/memories/reflect/...` moves to `.superclaude/memory/reflect/`" (tracked versus ignored); V2 "slug differs per worktree path", "writes outside the project folder" |
| I3 guard-condition gaps | 0 | 1 | 0 | V2 "conditional on the harness feature being enabled" |
| I4 count divergence | 0 | 0 | 0 | none found |
| I5 interaction effects when combined | 0 | 0 | 1 | V3 "routing-table tests assert their text; sc-reflect ... and sc-roadmap persistence have no home" |
| Subtotal | 1 | 2 | 2 | |

### Qualitative Summary
| Dimension | V1 (A) | V2 (B) | V3 (C) |
|---|---|---|---|
| Completeness | 2 | 2 | 2 |
| Correctness | 4 | 1 | 3 |
| Structure | 4 | 4 | 4 |
| Clarity | 3 | 2 | 4 |
| Risk Coverage | 0 | 1 | 0 |
| Invariant & Edge Case | 1 | 2 | 2 |
| **Total (of 30)** | **14** | **12** | **15** |
| **qual_score** | **0.4667** | **0.4000** | **0.5000** |

### Edge Case Floor Check
Floor: at least 1 of 5 on Invariant & Edge Case Coverage. V1 = 1 (eligible), V2 = 2 (eligible), V3 = 2 (eligible). Floor not suspended.

## Position-Bias Mitigation

| Variant | Pass 1 total (A,B,C order) | Pass 2 total (C,B,A order) | Disagreeing criteria | Final |
|---|---|---|---|---|
| V1 (A) | 17 | 14 | L4 (P1 1, P2 0), K4 (P1 1, P2 0), I5 (P1 1, P2 0) | 14 |
| V2 (B) | 13 | 12 | L4 (P1 1, P2 0) | 12 |
| V3 (C) | 16 | 8 | C2, C3, R2, R5, L1, I1, I5 (P1 1, P2 0); L4 (P1 1, P2 0) | 15 |

Disagreements found: 12 criterion-variant pairs. Re-evaluation with both passes' evidence, final verdict in bold:

| Criterion | Variant | Pass 1 | Pass 2 | Re-evaluation | Final |
|---|---|---|---|---|---|
| L4 terms defined | V1, V2, V3 | 1 | 0 | No document defines Glob, slug, TodoWrite or ccsession; same standard applied to all three | **0** |
| K4 external dependency failure | V1 | 1 | 0 | "zero dependency" removes the dependency but names no failure scenario | **0** |
| I5 interaction effects | V1 | 1 | 0 | Its only evidence (tracked file versus ignored folder) is already credited under I2; no double credit | **0** |
| C2 failure scenarios | V3 | 1 | 0 | "breaking removal" and "nothing to restore" are named failure consequences; Pass 2 overlooked them | **1** |
| C3 dependencies | V3 | 1 | 0 | Names the mechanisms it relies on (git, `.dev/tasks/`, ccsession, Claude Code resume), same standard as V1 and V2 | **1** |
| R2 feasible within constraints | V3 | 1 | 0 | The criterion tests the stated constraints (no new MCP, smallest change, works anywhere); capability loss is scored under C1 | **1** |
| R5 claims supported | V3 | 1 | 0 | Rationale is present (quoted HOW-WE-WORK text, named tests); wrong inferences are scored under R1 | **1** |
| L1 unambiguous language | V3 | 1 | 0 | Pass 2's reason (reflect/roadmap fate unresolved) concerns completeness, not wording; no hedge words | **1** |
| I1 collection boundaries | V3 | 1 | 0 | "has nothing to restore" is the empty-store case | **1** |
| I5 interaction effects | V3 | 1 | 0 | Removal interacts with routing-table tests and with reflect and roadmap persistence | **1** |

Verdicts changed by re-evaluation: 5 ended below Pass 1 (V1 L4, K4, I5; V2 L4; V3 L4); 7 ended above Pass 2 (all V3: C2, C3, R2, R5, L1, I1, I5). Verdicts on which both passes agreed were kept, including V2 R5 = 0 and V1 R1 = 0.

## Combined Scoring

| Variant | quant (50%) | qual (50%) | Final score |
|---|---|---|---|
| V1 (A) | 0.4331 | 0.2333 | **0.6664** |
| V3 (C) | 0.4040 | 0.2500 | 0.6540 |
| V2 (B) | 0.3825 | 0.2000 | 0.5825 |

Margin V1 over V3: 0.0124 (1.2 percentage points), inside the 5% tiebreak band.

Tiebreaker applied: Yes, level 1 (debate performance). Points won in Round 1: V1 = 9, V3 = 1, V2 = 1 (see `debate-transcript.md` scoring matrix). V1 wins. The tiebreak was needed because the rubric rewards V3 for being short and plainly worded, while the debate showed V3 fails six of the eight source requirements' replacements and was beaten on its own contradictions.

## Selected Base: Variant 1 (Option A, repo-local plain files under `.superclaude/memory/`)

### Selection rationale
- Highest combined score (0.6664) and wins the level 1 tiebreak 9 points to 1.
- Only variant whose approach addresses the portability constraint (C-002, 85% across advocates) and all 14 source files (C-001, E2) using tools that exist in every project.
- Advocates for V2 and V3 both ended up recommending A as the store or as the fallback if the commands stay (V2 advocate: "Choose A as the store"; V3 advocate: "fall back to Option A").

### Strengths to preserve from the base
1. Native Read/Write/Glob/Edit on a flat markdown folder; no MCP, no harness feature, offline, CI-testable.
2. Crash-recovery change is a path swap (E8).
3. Keeps `/sc:save`, `/sc:load` and the pm-agent lifecycle, so the routing rows and docs change by wording, not removal.

### Strengths to incorporate from non-base variants
| Source | Strength | Debate evidence |
|---|---|---|
| V1 advocate and V2 advocate and V3 advocate (unanimous, C-004, 92%) | Tracked home for the reflect calibration memory: `docs/memory/reflect/` (git-tracked today at `.serena/memories/reflect/deviation-patterns-IronClaude.md`, E5) | All three proposed it |
| V2 | Cross-worktree and root-ambiguity concern (C-003, A-003): resolve the project root once so nested `.dev/worktrees/<name>/` sessions use one store | Unresolved as a winner, but all three accept one root-resolution step |
| V3 | Roadmap persistence needs only a default path change: `sc-roadmap-protocol/SKILL.md` lines 326, 419, 443 already write `<output_dir>/.session-memory.md` when Serena is unavailable (verified) | V3 advocate; verified by grep in this run |
| V3 | Delete, do not port, the Serena-only non-memory calls (`think_about_*`, `summarize_changes`, `activate_project`, `onboarding`, `prepare_for_new_conversation`) | A-001 and X-004 accepted by all three |
| V2 | Concurrent-writer guard (A-002): per-key or session-suffixed files, append-only handoffs | All three QUALIFY |
| V1 and V2 | One-release legacy fallback: `/sc:load` reads `.serena/memories/` when the new key is absent (A-004) | 2 QUALIFY, 1 ACCEPT |
| V3 | Test and routing edits are required under every option (A-005): `tests/core/test_how_we_work_routing_table.py` lines 35-36, 1074-1076; fixtures; `tests/sc-roadmap/integration/test_wave5_completion.py` lines 69-78 | Unanimous REJECT of the "only C pays" assumption |

## Residual Risks (orchestrator manual probe, because Round 2.5 was skipped at depth=quick)

This is not the Round 2.5 fault-finder output and does not feed the convergence gate. It records invariant questions no variant answered.

| ID | Category | Assumption probed | Status in all variants | Severity | Evidence |
|---|---|---|---|---|---|
| M-001 | guard_conditions | `.superclaude/` is ignored by git in every project | UNADDRESSED | HIGH | `.gitignore:114` ignores it only in IronClaude (E5). In another project the folder shows as untracked and session notes can be committed. Mitigation to plan: first write creates `.superclaude/.gitignore` (the repo already uses a nested ignore at `.serena/.gitignore`, content `/cache` and `/project.local.yml`) |
| M-002 | sufficiency_challenge | "Option A alone lets Serena be removed with tests green" | UNADDRESSED | HIGH | False as stated: needs HOW-WE-WORK rows 237/327/329, test lines 1074-1076, sc-reflect Steps 0.7/0.7b rewrite, pm-agent/save.md Serena-only calls (E1, E3, E9, E10). The refactor plan lists them |
| M-003 | state_variables | One session owns each key (A-002) | UNADDRESSED | MEDIUM | Parallel sessions and worktrees can overwrite `pm_context` / `last_session` |
| M-004 | guard_conditions | Project root is unambiguous (A-003) | UNADDRESSED | MEDIUM | Sessions run in `.dev/worktrees/<name>/` per project CLAUDE.md |
| M-005 | collection_boundaries | `list_memories` empty-store behaviour (sc-reflect Step 0.7b gate) | UNADDRESSED | MEDIUM | With Glob, an empty or missing folder must be handled as "no memory", not an error |
| M-006 | interaction_effects | Moving the tracked reflect file to `docs/memory/` in projects without that folder | UNADDRESSED | LOW | Create the folder on first write |
