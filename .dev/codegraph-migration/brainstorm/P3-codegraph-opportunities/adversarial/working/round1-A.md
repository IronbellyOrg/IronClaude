# Round 1 — Advocate A (variant-1-opus-architect, architect persona)

## Position summary

Variant A supplies the most extensible structure: one capability-indexed seam (C-1 `sc-graph-grounding`) with a kill switch, a lifecycle command that owns per-worktree `init` (C-4), and complete output contracts for impact and test scope (C-2, C-3). A gets several access and gate details wrong for v1: the wildcard `Bash(codegraph *)`, MCP names in agents before listing, a `sync` attempt, and "zero callers = DELETE evidence". On those points B's CLI-first artifact model and C's asymmetric cleanup rule are better, and the merge should take them into A's scaffold.

## Steelman

### Variant B (sonnet-analyzer)

Strongest form: give read-only agents no MCP names in v1. The orchestrator computes graph artifacts with narrow CLI patterns and passes them to agents by path. This copies a pattern the repo already uses: troubleshoot pastes the producers table into briefs (B §1, citing `sc-troubleshoot-protocol/SKILL.md:281`). It removes the B1 listing blocker. It also avoids the `sc-cleanup-audit-protocol/SKILL.md:86` constraint, "MCP tools are unavailable to background subagents", which I re-read: it holds. B grades every idea by evidence class (M/P/A) and holds back gate changes that rest on unmeasured behaviour (`affected` backtest NFR-08). B also finds the parity hazard that the other two miss: in the one sample, 2 of the callers are production code and the rest are tests (B §1). Reflect's rule "HIGH if >5 referencing call sites" (`sc-reflect-protocol/SKILL.md:347`, re-read) would then fire on test callers alone. B gets the security point right too: `Bash(codegraph *)` pre-approves `install`/`upgrade`/`telemetry` (B §2.1; EVAL §3 CLI list).

Critique: B treats the v1 shape as the final architecture. It has no capability map, so a backend swap or a newly listed tool means editing every consumer's probe step and parser. B's probe skill (N-1) covers readiness and citations but not "which tool for which question". B's `/sc:load --index` (FR-17) puts a 1 GB-RSS mutation inside a context-loading command (EVAL §5.4). Its `sc-structure-brief` (N-3) is a new skill for value that B itself rates P-class at 0.6 (rank 9). B also overstates the sample: "the rest were test functions". EVAL §5.5 shows only 20 of 23 rows (X-021).

### Variant C (haiku-backend)

Strongest form: express codegraph as a dependency contract, PROBE → CALL → VERIFY → DEGRADE, with a run-scoped latch (C §2 fenced block). Rows that fail re-Read are dropped, never repaired (FR-03). An empty result can never weaken a safety gate (§8). C has the best asymmetric rule for cleanup-audit: `impact > 0` moves DELETE to REVIEW, and `impact = 0` proves nothing (I-07). That rule is right and A's is wrong (X-012). C's edge-case table (§8) is the clearest single place that lists the observed behaviours. Its rule for docs-only diffs (U-022) is correct.

Critique: C drifts into 1:1 Serena swaps (C-001: I-02, I-04, I-05, I-06), which the seed brief puts out of scope. Its MCP names `mcp__codegraph__search` would not match the real names `codegraph_search` (X-018, EVAL §3 table). Its I-02 CLI outline uses `symbolsOnly`, which the CLI does not have (X-019). It contradicts itself on the wildcard (X-002). It lets `/sc:test-scope` narrow VG-1 to exactly the `affected` list (FR-05). That is the least safe gate change of the three, because EVAL never ran `affected`. It also cites the wrong wave for the 2k budget: `:256` is Wave 1.5, and Wave 1 is `:218` ~3k (re-read; X-015).

## Strengths claimed

1. **A capability map gives extension room that B and C lack.** C-1 `refs/capability-map.md` maps each capability (`callers|impact|outline|definition|search|affected_tests|status`) to its MCP tool, CLI subcommand, native fallback and known gaps, under a `tested_version: 1.6.2` header (A §6 C-1). Consumers name a capability, not a tool (A §1 bullet 1, INV-4). Two foreseeable changes then touch one file: the B1 listing landing, and a backend swap (single maintainer, about 8 releases per quarter, EVAL §1). B's probe and C's guidance-only skill each push that knowledge into every consumer.
2. **A has a kill switch and a containment test.** FR-16 (`status: disabled` makes every consumer degrade) and NFR-03 (a pinned count of files that mention `codegraph`) make rollback and drift mechanically checkable. B relies on uninstalling the binary, and C relies on deleting text (C-033).
3. **A names a lifecycle owner for the unowned per-worktree `init` and keeps it apart from read-only flows.** C-4 `/sc:graph init` runs only when the user types it. It refuses in a nested worktree unless the user passes `--worktree-local`, which then runs `init -i` (EVAL §5.8 warning text). B overloads `/sc:load`. C names no primitive owner, so A-011 stays unaddressed.
4. **A treats citation resolution as a typed field.** Every row carries `resolution: def-line|call-site-verified|unresolved` (A I-02, FR-04), and evidence-validator's existing `line-mismatch` check (`agents/evidence-validator.md:97`, re-read) is told how to judge def-line rows. Downstream consumers can then filter rows by type, not by prose.
5. **A is the only variant with the telemetry blocker** (U-002, A B5). Bash CLI calls do not inherit the MCP entry's `CODEGRAPH_TELEMETRY=0` (EVAL §7 step 5 puts it in the `env` object only, and §1 says telemetry is on by default). B's CLI-first model makes this worse, so any merge that adopts B's access model needs A's B5.
6. **A is the only variant with the language-scope reality** (U-003). IronClaude's primitives are Markdown, and EVAL §5.4 indexed only python, yaml and liquid. A says the payoff is in code repos, which bounds expectations for every onboarding idea.
7. **Its pre-edit impact runs earlier than B's post-edit context.** A I-05 and I-10 run impact before symbol-changing edits and before auto-applied pr-submit fixes (`sc-pr-submit-protocol/SKILL.md:194`). B I-07 attaches dependents only after the edit, at Q2/Q3.
8. **The test-selection invariant is safe by construction.** FR-07 `selected ⊇ heuristic_tests` can never narrow VG-1, which C's FR-05 can.
9. **Its citations are accurate.** The MCP names (X-018) and the Wave 1 budget `:218` (X-015) are correct. Workflow's no-fan-out constraint is quoted correctly (`sc-workflow-protocol/SKILL.md:74`, re-read).

## Weaknesses identified in other variants

1. B has no capability abstraction (B §6 N-1 interface is readiness-only). Adding MCP later, which B's own Q1 contemplates, means editing every consumer. That is a maintainability debt.
2. B's FR-17 lets `/sc:load --index` run `init --yes`, which is 34 MB and about 1 GB RSS (EVAL §5.4), in a session-context command. That breaks separation of concerns. A dedicated lifecycle command (A C-4) is the cleaner owner.
3. B's FR-01 runs "N-1 once per run" while its §8 says "re-run status immediately before the queries". That is an internal inconsistency (A-006).
4. B's D-05 claims "Grep sees every static reference the graph sees". EVAL does not support this (X-020): EVAL §5.4 says "Linking dynamic dispatch".
5. C-001 is scope drift: four of C's 13 ideas are the 1:1 swaps the brief excludes.
6. C's allowlist names (X-018) and its CLI `symbolsOnly` (X-019) are not traceable to EVAL. This fails the brief's success criterion "every capability claim traceable to EVAL".
7. C's FR-05 "`tests` is exactly the parsed `affected --json` list" can narrow VG-1 on an unmeasured mechanism (X-008; A-008).
8. C's FR-02 latch says "never retry the probe". After mid-run edits in implement or pr-submit, the latched "available" state reads a pre-edit index in CLI-only sessions (EVAL §4: the watcher runs only with an MCP client).
9. C's C-1 has no arguments and no output, so consumers copy its degraded keys into their own contracts (C §6). That is the same drift C's I-01 says it prevents.

## Concessions

1. **Wildcard allowlist (X-002, C-004):** B is right. `Bash(codegraph *)` would pre-approve `install`, `upgrade`, `uninstall` and `telemetry` (EVAL §3, and §2: `install` edits `~/.claude`). A's Class C and FR-06 should use B's per-subcommand patterns.
2. **MCP names in agents before listing (X-001, C-002, C-003):** for v1, B's artifact-by-path model is better. It works today, avoids B1, and sidesteps the `:86` constraint, which A's own Q-4 leaves open. A's Class D row should become "artifacts in v1; MCP names behind the capability map once B1 and Q-4 resolve".
3. **evidence-validator in Class D (X-004):** listing it for MCP names was wrong. Its tools must stay `Read, Grep, Glob` (re-read `agents/evidence-validator.md:5`). Only A's text edit about def-line rows remains.
4. **`sync` (X-006, C-007):** A's "try one `sync`" is a write inside potentially read-only flows. It also conflicts with cleanup-audit's READ-ONLY charter. Drop it and adopt B's "re-check `status` before queries; pending → stale, leads only".
5. **Cleanup-audit zero callers (X-012, C-019):** A's I-12 says "zero graph callers is extra evidence for DELETE". That contradicts A's own empty-results edge case: "never infer 'unused' from it". C's asymmetric rule (nonzero → REVIEW, zero proves nothing) is correct.
6. **`status` latency (X-017):** EVAL §5.5 times `query` (290 ms) and `callers` (297 ms), not `status`. A's "~300 ms" for `status` in I-17 and NFR-02 is UNVERIFIED and must be measured.
7. **Sourcing of the empty-results list:** A cites EVAL §4 for "dynamic dispatch, registries, decorators, CLI entry points, string invocation". EVAL §4 supports only the over-1 MB and gitignored cases. The rest is reasoning and should be marked UNVERIFIED.
8. **SessionStart hook (X-007, C-022):** given the unmeasured `status` latency and the extra hook failure surface (`freshness-session-start.sh` already branches on MCP config), defer I-17 and keep C-4 as the visibility path.
9. **Reflect severity (X-013, C-017, C-018):** B's prod-only caller count from the runtime-surface table, with no new contract field in v1, is better grounded than A's "resolved call sites". Resolving every call site costs one Grep and one Read per row on hub symbols.
10. **No explicit nine-vector coverage map (S-003):** C's summary table is clearer.

## Shared assumptions

| A-ID | Position | Reason |
|---|---|---|
| A-001 | ACCEPT | Seed constraint; A INV-1 and FR-03 already enforce it with a closed token vocabulary |
| A-002 | ACCEPT | EVAL §5.5 definition-line gap; A I-02 types each row's `resolution` |
| A-003 | QUALIFY | The "auggie is free" reason fails when auggie is down (seed: "auggie MCP not available"). Rest the explore ban on size and noise against fixed wave budgets (`:218`), not on auggie being available |
| A-004 | QUALIFY | One 24,913-char sample (EVAL §5.6). Keep explore out of primitives by default, but make it reopenable after a measurement, as A already does for `context` (D-04) |
| A-005 | QUALIFY | A's "a few hundred tokens" is an estimate. Keep the hard caps (`limit ≤ 20`, `depth ≤ 2`) and add B's NFR-06 measurement |
| A-006 | REJECT | Implement and pr-submit edit mid-run; in CLI-only sessions no watcher runs (EVAL §4). Probe once per run, then re-check `status` before any post-edit query; pending → `graph:stale` |
| A-007 | QUALIFY | Caller completeness was verified for one symbol (EVAL §5.5). Treat non-empty lists as lower bounds (floors), never as complete sets for severity or blast radius |
| A-008 | QUALIFY | EVAL never ran `affected`. Keep A's superset invariant and add B's advisory-then-backtest stage before the union enters VG-1 |
| A-009 | ACCEPT | EVAL §5.4 cost; A FR-09 and D-08 |
| A-010 | QUALIFY | Warning text is pinned to v1.6.2 only. Add B's golden fixtures (NFR-04) and A's `graph:version_mismatch` |
| A-011 | ACCEPT | This is why A proposes C-4 `/sc:graph init` as a named user-level owner (B2) |
| A-012 | QUALIFY | Skill-call cost is UNVERIFIED (B Q6). In A's seam the `refs/*.md` files are the contract, and both orchestrators and agents can Read them by installed path without a Skill call. Agent MCP use still waits on Q-4 |

## Per-point positions

| ID | Superior | Reason |
|---|---|---|
| S-001 | A | Records ground_truth provenance |
| S-002 | none | Identical |
| S-003 | C | Explicit nine-vector map |
| S-004 | A+B | A's 7 classes plus B's stance column |
| S-005 | B | M/P/A evidence classes |
| S-006 | A+B | A's coverage, filtered by B's evidence classes |
| S-007 | A | Layered list with visible formula |
| S-008 | A+B | Both use ID'd tables |
| S-009 | A+B | Per-candidate subsections with fields |
| S-010 | A+C | A's invariants plus C's edge-case table |
| S-011 | none | Counts are not quality |
| C-001 | A+B | Both keep scope beyond 1:1; C drifts |
| C-002 | B+A | B's artifacts for v1, A's class table for later |
| C-003 | B | Do not set listing in v1; measure first |
| C-004 | B | Per-subcommand patterns, no wildcard |
| C-005 | A+B | A's capability-map seam plus B's resolver script |
| C-006 | A+B | A's closed vocab plus B's provenance check and `parse_failed` |
| C-007 | B | Never sync; re-check status before queries |
| C-008 | A | Simplest grep-enforceable ban |
| C-009 | A+B | Typed `resolution` plus span-bounded resolver |
| C-010 | A+B | B: tools unchanged; A: def-line text |
| C-011 | A | Pre-edit beats post-edit |
| C-012 | A+B | Context first; B's verified class as stage 2 |
| C-013 | A+B | Superset invariant plus backtest gate |
| C-014 | A | Positional args avoid unverified pipeline matching |
| C-015 | A+B | A's Wave 1 callers plus B's artifact paste |
| C-016 | A | Workflow when symbols exist; tasklist stays deterministic |
| C-017 | B | Prod-only count, grounded in the sample |
| C-018 | B | No new field in v1 |
| C-019 | C | Correct asymmetric DELETE rule |
| C-020 | A | Agent-found candidates cannot be precomputed (gated on B1/Q-4) |
| C-021 | A | Light edits; no new onboarding skill |
| C-022 | B | No new hooks until status is measured |
| C-023 | A | Dedicated user-typed lifecycle command |
| C-024 | A+B | Prerequisite layer plus confidence weight |
| C-025 | A+B | Seam/resolver first, B's parity fix early |
| C-026 | A+B | Union of evidence-backed drops |
| C-027 | A | Seam, impact, test scope, lifecycle cover the gaps |
| C-028 | A | Fullest contracts; labelled diff mapping |
| C-029 | A | Callers tied to concrete steps |
| C-030 | B | Re-query once; flags CLI file-arg gap |
| C-031 | A+B | Kill switch/containment plus fixtures/backtest |
| C-032 | A+B | Telemetry plus allowlist blast radius |
| C-033 | A | Kill switch without uninstall |
| X-001 | B | Artifacts in v1 |
| X-002 | B | Wildcard pre-approves install |
| X-003 | B | Defer listing |
| X-004 | B | Validator stays Read/Grep/Glob |
| X-005 | A | User-typed `/sc:graph init` |
| X-006 | B+C | No primitive sync |
| X-007 | B | Defer hook |
| X-008 | A+B | Union only, after backtest |
| X-009 | A+B | Keep downgrade; verified exemption later |
| X-010 | A+B | Tasklist determinism |
| X-011 | A | Workflow step gated on existing symbols |
| X-012 | C | Zero proves nothing |
| X-013 | B | Distinct production callers |
| X-014 | A | Ban in primitives |
| X-015 | A+B | `:218` is Wave 1 |
| X-016 | A | Status only, no mutation |
| X-017 | B | Status timing unmeasured |
| X-018 | A | `mcp__codegraph__codegraph_*` names |
| X-019 | A | No CLI `symbolsOnly` claim |
| X-020 | none | Both claims UNVERIFIED |
| X-021 | A | Quotes "20 of 23" without overreach |
