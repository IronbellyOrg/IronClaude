# Adversarial Debate Transcript: P3 codegraph opportunities

## Metadata
- Generated: 2026-10-29T17:27:48Z
- Mode: B (generate), source `../seed-brief.md`; ground truth `../../../research/codegraph-evaluation.md` (EVAL)
- Depth: standard
- Rounds completed: 2 (Round 1 advocate statements, Round 2 sequential rebuttals) + Round 2.5 invariant probe (`invariant-probe.md`)
- Round 3: skipped (depth=standard)
- Convergence achieved: 95.7% (67 of 70 scored points)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3 (A = `variant-1-opus-architect.md`, opus:architect; B = `variant-2-sonnet-analyzer.md`, sonnet:analyzer; C = `variant-3-haiku-backend.md`, haiku:backend)
- Status: **BLOCKED_BY_INVARIANTS** (see Convergence Assessment)
- Orchestrator note: the advocate files below are reproduced verbatim from `working/`. The orchestrator did not edit them. Their internal "Variant A/B/C" labels match the labels used here.

## Round 1: Advocate Statements

### Variant A Advocate (opus:architect)

<!-- verbatim: working/round1-A.md -->

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

### Variant B Advocate (sonnet:analyzer)

<!-- verbatim: working/round1-B.md -->

---
round: 1
advocate_for: variant-2-sonnet-analyzer (Variant B)
persona: analyzer
sources: variant-1-opus-architect.md (A), variant-2-sonnet-analyzer.md (B), variant-3-haiku-backend.md (C), diff-analysis.md, seed-brief.md, EVAL (codegraph-evaluation.md)
---

# Round 1 advocate: Variant B (analyzer)

Notation: A/B/C = variants 1/2/3. EVAL = codegraph-evaluation.md. Primitive line citations were re-read for this round (troubleshoot `:218`, `:256`, `:281`, `:286`; reflect `:347`; auggie-review `:218`; cleanup-audit `:75`, `:86`, `:8`; pr-submit `:4`, `:206`; `hooks.json:52,59`; evidence-validator `:5`, `:97`; runtime-surface `:25`, `:61`; implement `qa.md:9`; tasklist `:1326`, `:1658`, `:1670`). All matched what the variants say.

## Position summary

B is the variant whose recommendations follow from what EVAL actually measured: it separates measured mechanism (M) from unmeasured benefit (P) and gates every behaviour-changing step (`affected` in VG-1, the out-of-hunk exemption, the allowlist breadth) on that line. A is the strongest on breadth and on two operational facts B missed (telemetry on the CLI path, Markdown repos get no signal), and C drifts into 1:1 Serena swaps and contains four checkable errors, so the best merge is B's evidence discipline and safety rules with A's lifecycle and telemetry findings.

## Steelman

### Variant A (opus architect)

Strongest version: codegraph is a single-maintainer dependency (EVAL §1: 30 releases, 8 in about 3 months, top contributor 1,535 commits vs 11-18 for the next three), so the right design is one seam that owns the capability map, probe, citation resolution and degraded vocabulary, so a backend swap touches one ref plus allowlist lines (A §1, INV-4, C-1). A also identifies two real facts B omits. First, telemetry: EVAL §7 puts `CODEGRAPH_TELEMETRY=0` only in the MCP entry and the Coder image, so Bash CLI calls on another host send telemetry (A B5, U-002). Second, value depends on the target repo's language; EVAL §5.4 indexed python/yaml/liquid, so Markdown primitives get nothing (A §1, U-003). A also names `/sc:graph` as a user-typed owner for the unowned per-worktree `init` (EVAL §4, §7), refuses it in a nested worktree without `--worktree-local` (matches EVAL §5.8 text), and adds a kill switch (FR-16, NFR-08) and a pre-edit impact check in implement Q1 (I-05) that is truly "before edits". Its tasklist drop cites the exact booster row (`sc-tasklist-protocol/SKILL.md:1326`, ">2 files affected"), which I verified. A is the most complete spec: 19 ideas, 16 FR, 8 NFR, closed `graph:*` vocabulary that can be grep-tested.

Where it is genuinely right against B: pre-edit timing (B's I-07 runs after the diff exists), the lifecycle command, the telemetry blocker, and the grep-testable vocabulary.

### Variant C (haiku backend)

Strongest version: treat codegraph like a backend dependency with a contract, `PROBE -> CALL -> VERIFY -> DEGRADE`, with a run-scoped latch (no retry), caching per run, and "never silence" on empty `affected` for a source diff (C §2 contract block, FR-02, FR-05, FR-07). Its `affected` handling is the most careful on one point: an empty result with a non-empty source diff forces the heuristic, while a docs-only diff may honestly yield no tests (C §8 table, U-022). Its rule "a row that fails re-Read is dropped, never repaired by guessing an offset" (FR-03) is the cleanest statement of the citation contract, and the stale-index rule (HIGH becomes MEDIUM when stale, U-021) is a pragmatic guard on reflect severity. The mutation-exclusion grep (`codegraph (init|index|sync|...)` returns 0, FR-06) is mechanically testable. The edge-case table maps observed EVAL behaviour to a contract response, which is exactly what an implementer needs.

Where it is genuinely right against B: the drop-never-repair rule, the explicit docs-only-diff case, and the test-by-grep mutation exclusion.

## Strengths claimed

1. **Evidence classes make the ranking auditable.** B defines M/P/A before §1 and carries them into the score `V x C / E` with C = 1.0/0.6/0.3 (B §4). Every rank can be recomputed and its confidence challenged. A's formula multiplies by a "Frequency" factor that is also subjective, and C's ranking is qualitative with no formula (diff-analysis C-024). I-08 (`affected`) lands at 0.9 instead of top-3 solely because EVAL never ran `affected` (A-008 says "STATED (B only)").
2. **B is the only variant that gates `affected` on a measurement.** EVAL §3 lists the subcommand but §5 never runs it. B ships an advisory delta first and unions into VG-1 only after a 20-change backtest (FR-13, NFR-08: recall at least that of `<changed-area>`, median 25 files or fewer). A unions immediately (FR-07) and C replaces the heuristic (FR-05: `tests` "is exactly the parsed `affected --json` list", which can narrow the set; X-008). Narrowing a push gate on an unrun tool is the highest-cost error in the field.
3. **B finds the parity hazard the 1:1 swap creates.** EVAL §5.5 shows 20 of 23 callers: 2 production (`install_mcp_server`, `install`) and 18 tests. Reflect's rule is "HIGH if >5 referencing call sites" (`skills/sc-reflect-protocol/SKILL.md:347`), so a naive callers swap trips HIGH on tests alone. B partitions with reflect's own runtime-surface table (`refs/runtime-surface.md:25`, FR-09). A and C do not partition; C's I-05 even keeps tests in the count (X-013).
4. **B's citation resolver is the most precise.** `codegraph query <caller> --json` returns `startLine`/`endLine` (EVAL §5.5), so B Greps the callee only inside that span, then Reads (I-02, N-1 `resolve-callsite.sh`). A greps "after the def line" with no end bound (I-02), which can match a different function in the same file. The measured gap is `main.py:46` vs `:255`; the span closes exactly that.
5. **B's access model matches the constraints that exist.** CLI-first with orchestrator-computed artifacts follows the repo's own precedent: troubleshoot pastes the producers table into briefs (`SKILL.md:281`) and reflect reviewers get pre-computed material (`:355`). This avoids the `CODEGRAPH_MCP_TOOLS` blocker (EVAL §3: only `codegraph_explore` listed) and keeps read-only agents' `tools:` lines untouched (FR-11), so no test pin on `troubleshoot-analyst.md:5` moves.
6. **B has the narrowest safe allowlist.** One pattern per subcommand, never `Bash(codegraph *)` (FR-04). EVAL §3 lists `install`, `uninstall`, `upgrade`, `unlock`, `telemetry` as CLI subcommands, and EVAL §2/§5.9 shows `install` edits `~/.claude.json`, `settings.json` (adds `codegraph prompt-hook`) and `CLAUDE.md`. A wildcard pre-approves that. Existing allowlists are already enumerated (`sc-cleanup-audit-protocol/SKILL.md:8`, `sc-pr-submit-protocol/SKILL.md:4`), so per-subcommand patterns fit the house style.
7. **B alone handles freshness without touching the index.** Probe never syncs; re-run `status` right before queries (B §8); `index_root == realpath(worktree root)` or discard (FR-03). EVAL §5.7 shows `codegraph sync` failing on the writer lock while the daemon runs, which makes A's "try one `sync`" (FR-10) a step that fails whenever an MCP session is open. B also notes the CLI-only case: no watcher without an MCP client (EVAL §4).
8. **B states its unknowns.** Output-format drift (EVAL §3 gives `--json` only for `query` and `affected`) leads to golden fixtures and a `parse_failed` degrade (NFR-04). `status` timing is "UNVERIFIED, measure" (NFR-01), where A asserts "~300 ms" for `status` (X-017) although EVAL §5.5 timed only `query` and `callers`.
9. **B's drop list is reasoned from primitive text.** D-05 (cleanup-audit) cites the read-only charter, `init` writing `.codegraph/`, and MCP unavailability to background subagents (`:86`). D-02 cites the 1 s pre-edit timeout (`hooks.json:52`, verified as the `freshness-pre-edit.sh` entry). D-10 cites `hooks.json:59` (matcher `Read` only), which also kills `node` file mode as a Read replacement; A and C reach the same drop.
10. **B closes the explore question with a budget, not a slogan.** 24,913 characters is about 6K tokens at 4 chars/token (B says it is an estimate) against `~3k` Wave 1 (`SKILL.md:218`, verified). Explore is banned in waves under 8K and in every subagent, but stays usable interactively with `maxFiles <= 5` (FR-10), which the CLI parameter range (1-20, EVAL §3) supports.

## Weaknesses identified in other variants

1. **C breaks the scope (C-001).** Its I-02 ("replace Serena overview/find_symbol rows"), I-04 (replaces `find_declaration`), I-05 (replaces `find_referencing_symbols`) and I-06 (replaces the Serena fallback tier) are exactly the 1:1 swaps INV §4 assigns to Phase 3 and the seed brief says to go beyond (Problem Statement: "where, beyond 1:1 Serena replacement"). Four of C's 13 ideas, three of C's top six, are out of scope.
2. **C contains four checkable errors.** (a) MCP names `mcp__codegraph__search/__callers` (X-018) do not match EVAL §3's `codegraph_search`, so the server-prefixed form is `mcp__codegraph__codegraph_*`; its allowlists would not match. (b) `codegraph_node {file, symbolsOnly:true}` is claimed to work through the CLI "today" (X-019); EVAL §3 lists CLI `node [name]` only. (c) It cites "Wave 1.5 :256" as the Tier-1 budget of 2k (X-015); `:218` is Wave 1 at about 3k and `:256` is Wave 1.5 (verified). (d) It says both "no allowlist change" (§1) and "adding `Bash(codegraph *)` patterns" (§2) while FR-10 forbids the wildcard (X-002).
3. **C's `affected` pipeline is unproven under scoped Bash.** `git diff --name-only | codegraph affected --stdin` (I-09) runs under pr-submit's `Bash(git *)`-style allowlist (`:4`). Whether a pipeline is accepted is UNVERIFIED (A's own Q-2). B passes files as arguments or `--stdin` from a file (C-014).
4. **C and A both treat non-empty caller lists as complete (A-007).** C's I-05 uses `callers --limit 100` as the shared-vs-collision test; A's severity counts "resolved call sites". EVAL verified one symbol (§5.5). B partly shares the problem (see Concessions) but ties the threshold to distinct production symbols and records `shown/total` (FR-08, FR-09).
5. **A's `Bash(codegraph *)` for Class C (X-002).** With EVAL §2 and §3 above, one wildcard line in pr-submit or auggie-review allows `codegraph install`, `upgrade`, `uninit` and `unlock`. A's own FR-09 forbids using them but a grep test on body text does not constrain what a pre-approved allowlist permits.
6. **A grants MCP names to read-only agents in v1 (X-001, X-003).** A's B1 depends on the Phase 2 registration setting `CODEGRAPH_MCP_TOOLS` for a subset, and an explicit allowlist then blocks `explore`/`files` for everyone (A Q-1; EVAL §3 line 94). Seven extra always-loaded schemas have unmeasured cost (U-014). A also lists `evidence-validator` in Class D, which erodes the independent last gate (X-004).
7. **A's "try one `sync`" contradicts EVAL §5.7** (see Strength 7). It also puts an index mutation into read-only flows, which A's D-08 and FR-09 forbid elsewhere (X-006).
8. **A unions `affected` into VG-1 at once (X-008)** on a tool EVAL never ran; at depth 2 an unmeasured union can inflate the set, and A's Q-8 admits the right depth is unknown.
9. **A's 19 ideas include a tail with its own admitted score of 0.7-1** (I-09, I-12, I-15 at ranks 17-19; I-16 "demoted by judgment" from a formula score of 3 to rank 16). A formula the author overrides is not a method.
10. **C's `impact == 0` DELETE logic and "grep misses are not graph misses" (X-012, X-020)** rest on a claim EVAL does not state. C's FR-05 also lets graph results replace the heuristic, so a stale index (A-006) silently narrows tests.

## Concessions

1. **X-021 / EVAL fact-check against B.** B writes that the sample had "23 callers reported" and "the rest were test functions" (B §1, I-05). EVAL §5.5 shows 20 rows: 2 production and 18 tests; the other 3 were never inspected. The inference is still valid (tests inflate the count), but "23 callers, 2 production" overstates it. The correct claim is "20 of 23 inspected: 2 production". Also the whole hazard rests on one symbol (A-007).
2. **X-020 / D-05 reasoning.** B says "Grep sees every static reference the graph sees." EVAL states neither direction. The drop conclusion (graph cannot tighten DELETE, grep is the gate at `:75`) stands on the read-only charter and on FR-07's asymmetry, not on that sentence.
3. **Telemetry (U-002) is a real miss.** B's default is the CLI via Bash, which makes the omission larger for B than for the others. EVAL §7 puts `CODEGRAPH_TELEMETRY=0` only in the MCP entry and the Coder image, and `codegraph telemetry status/off` exists (EVAL §1, §2). The probe should record `telemetry` and flag it, as A does.
4. **Language dependence (U-003).** B never says that Markdown-only repos return nothing. EVAL §5.4 lists python 440, yaml 49, liquid 11.
5. **B's hook rejection is a value judgement.** `hooks.json` already runs SessionStart hooks with 5-10 s timeouts, so A's one-line status hook is feasible. B's D-03 argument that it "adds nothing the probe doesn't give" is arguable, not a proof. The 1 s cited in D-02 applies only to the pre-edit hook.
6. **Pre-edit timing.** B's I-07 runs after the diff exists. A's I-05 (Q1, before edits) matches "impact before edits" better. B has no answer for the Q1 gap (B ranks I-07 last).
7. **FR-12 changes a rule.** `dependent-impact` exempt from the out-of-hunk downgrade (`auggie-review SKILL.md:218`) is a semantic change to a validated rule. It is bounded (only when the call-site line is Read-verified) but it is B's riskiest proposal and A/C's context-only default is the safer first release.
8. **One probe per run (A-006).** B requires "once per run" (FR-01) while also saying to re-run `status` before the queries (§8). Those two statements are in tension for implement/pr-submit, which edit mid-run.
9. **B's scores use subjective V (1-5).** The formula is auditable, the inputs are judgement.
10. **Breadth.** B drops workflow and cleanup-audit and has 10 ideas; A covers more primitives (explain, index-repo, load, reuse-auditor liveness). Some of that breadth is low value, but the reuse-auditor liveness idea (A I-11) is not clearly wrong.

## Shared assumptions

| A-ID | Verdict | Reason |
|---|---|---|
| A-001 | ACCEPT | Seed constraint; B has the same rule (FR-02) and tests it by `codegraph` off PATH (FR-01). |
| A-002 | ACCEPT | Seed citation contract plus EVAL §5.5 gap; B enforces it (FR-06) and keeps `evidence-validator` Read-only. |
| A-003 | QUALIFY | The seed says auggie is unavailable in the run session, but primitives run elsewhere where auggie works; the fallback when auggie is down is Grep/Read. B's D-01 reasoning ("auggie offloads cost, explore adds it") is valid only when auggie is up. |
| A-004 | QUALIFY | The 24,913-character sample is one call with a two-word query; `maxFiles` (1-20, EVAL §3) was not varied. B's ban is on budgeted waves, not on explore generally, which is the right scope. |
| A-005 | ACCEPT as risk | Size of `callers`/`impact` output was never measured. B caps artifacts at 40 rows and 6 KB (FR-10) and 2K tokens per run (NFR-06) instead of claiming "a few hundred tokens". |
| A-006 | REJECT | Implement and pr-submit edit files mid-run; without an MCP client no watcher runs (EVAL §4). B should re-probe before queries (§8) and should reconcile with FR-01, see Concessions 8. |
| A-007 | REJECT | One symbol was verified. B treats non-empty lists as a lead and records `shown/total`; partial: still assumes call edges are complete for Python. |
| A-008 | QUALIFY | Only B marks `affected` unrun. Use it advisory first with the NFR-08 backtest. A and C should not make it a gate. |
| A-009 | ACCEPT | `init` costs about 34 MB and about 1 GB RSS (EVAL §5.4) and writes `.codegraph/`; read-only flows never init. |
| A-010 | ACCEPT | Discard foreign-index answers (B FR-03). The warning text is pinned to v1.6.2; B covers drift with golden fixtures (NFR-04). |
| A-011 | ACCEPT | Per-worktree init has no owner (EVAL §4, §7); B degrades to `uninitialized` and names `/sc:load --index` as a fallback owner, though A's dedicated command is cleaner. |
| A-012 | QUALIFY | Agents can Read refs by path, but the Skill call cost is unmeasured (B Q6). B's mitigation: a shared ref copied into consumers' `refs/` is an alternative to a skill. |

## Per-point positions

| ID | Superior | Reason |
|---|---|---|
| S-001 | none | cosmetic; B's `source_brief` field gives traceability only |
| S-002 | none | identical section order |
| S-003 | B+C | C puts the vector table up front; B adds explicit drops per vector |
| S-004 | A+B | A's seven classes distinguish scoped vs unrestricted Bash; B adds a stance column per blocker |
| S-005 | B | M/P/A classes feed the ranking score |
| S-006 | B | ten ideas cover all nine vectors; A's ranks 16-19 score about 1 |
| S-007 | A+B | A's layer 0 prerequisites with B's recomputable score table |
| S-008 | A+B | table with IDs, as both do; C's unnumbered bullets cannot be cross-referenced |
| S-009 | A+B | one subsection per candidate with fields; C's table loses interface detail |
| S-010 | A+C | invariants (A) and the observed-behaviour to contract-response table (C) |
| S-011 | none | counts do not indicate quality |
| C-001 | A+B | both stay beyond 1:1; C drifts into SYM/REF swaps |
| C-002 | B | artifacts in briefs avoid the listing blocker and keep agents read-only |
| C-003 | B | do not set `CODEGRAPH_MCP_TOOLS` until schema overhead is measured |
| C-004 | B | per-subcommand patterns because EVAL §2/§3 shows `install` edits Claude config |
| C-005 | A+B | A's capability map and kill switch with B's executable resolver script |
| C-006 | A+B | A's closed grep-testable vocabulary with B's `parse_failed` state; C's binary latch hides `stale` |
| C-007 | B | never sync; re-probe before queries (EVAL §5.7 lock failure) |
| C-008 | B | budget-based ban (below 8K, subagents) allows bounded interactive explore |
| C-009 | B | `startLine`/`endLine` span bounds the call-site Grep; C's drop-never-repair rule added |
| C-010 | B+C | evidence-validator stays Read-only; independence is the gate |
| C-011 | A | pre-edit impact at Q1 is truly before edits; B's I-07 is post-edit |
| C-012 | B | names the real blind spot (directory chunking plus out-of-hunk rule), see Concessions 7 |
| C-013 | B | advisory first, union only after backtest; `affected` was never run |
| C-014 | A+B | positional args or `--stdin` from a file; no pipeline under scoped Bash |
| C-015 | A+B | A's callers (limit 10) feeds B's pasted artifact precedent (`SKILL.md:281`); C's I-02 is a 1:1 swap |
| C-016 | A+B | both keep tasklist deterministic (`:1326`, `:1658`); workflow is optional and after a spike |
| C-017 | B | distinct production caller symbols via the runtime-surface table |
| C-018 | B | no new reflect field in v1, only `degraded_components` entries |
| C-019 | B | drop it; the DELETE gate stays grep (`:75`) and the audit is read-only, though B's D-05 sentence is unproven |
| C-020 | B | spike before adopting; A and C depend on an unlisted tool in a read-only agent |
| C-021 | none | all onboarding claims are unmeasured; the 58K to 3K figure is the primitive's own |
| C-022 | B | no new hooks; value judgement (see Concessions 5) |
| C-023 | A | a dedicated user-typed command with a nested-worktree refusal beats folding `init` into `/sc:load` |
| C-024 | A+B | A's frequency factor with B's evidence confidence weight |
| C-025 | A+B | enablers first; add A's troubleshoot callers and B's token guard |
| C-026 | A+B | A's tasklist and graph-scout drops with B's hook and producer-enumeration drops |
| C-027 | A+B | B's probe plus blast-radius candidates with A's `/sc:graph` lifecycle command |
| C-028 | B | blast-radius output has prod/test split, shown/total and call-site status |
| C-029 | A+B | B's wider caller list, trimmed to where the probe pays (not `explain`) |
| C-030 | B | re-query once when total is 100 or less; notes CLI `callers` lacks a documented file argument |
| C-031 | B+C | golden fixtures, byte-identical output (B) and per-run caching (C) |
| C-032 | A+B | A's telemetry and language-dependence risks with B's allowlist blast radius |
| C-033 | A+B | A's kill switch and B's absence equals native path |
| X-001 | B | v1 agents get artifacts; no MCP names until listed and measured |
| X-002 | B | no wildcard; EVAL §2/§3 |
| X-003 | B | do not set the env in v1; measure schema overhead first |
| X-004 | B+C | validator remains `Read, Grep, Glob` (`evidence-validator.md:5`) |
| X-005 | A | only a user-typed command may init; B's `/sc:load --index` mixes mutation into a context command |
| X-006 | B+C | primitives never call `sync` |
| X-007 | B | no SessionStart hook; value judgement, see Concessions 5 |
| X-008 | B | no gate change until the backtest passes |
| X-009 | A+B | keep today's downgrade by default; allow a Read-verified `dependent-impact` exemption |
| X-010 | A+B | both drop tasklist for determinism; C's I-11 conflicts with it |
| X-011 | B | workflow preview is class A (spec text to symbol is judgement) |
| X-012 | B+C | zero callers proves nothing; A's "extra DELETE evidence" violates FR-07 |
| X-013 | B | count distinct production caller symbols |
| X-014 | B | bounded interactive explore only |
| X-015 | A+B | `:218` Wave 1 is about 3k; C cites the Wave 1.5 line (`:256`) |
| X-016 | A+B | A's status line, B's explicit `--index`; C's drop is fine for a rewrite only |
| X-017 | B | `status` latency is UNVERIFIED; EVAL §5.5 timed `query` and `callers` only |
| X-018 | A | correct `mcp__codegraph__codegraph_*` names; B avoids MCP names, C's would not match |
| X-019 | B | CLI outline route uses `query --json` and `startLine`/`endLine`, not `node symbolsOnly` |
| X-020 | none | neither claim is in EVAL; both unverified |
| X-021 | none | B overstates "23 callers, 2 production"; EVAL shows 20 of 23 inspected |

### Variant C Advocate (haiku:backend)

<!-- verbatim: working/round1-C.md -->

# Round 1 — Variant C (backend/haiku) positions

## Position summary

Codegraph is a dependency with a contract, not a tool list: one shared PROBE→CALL→VERIFY→DEGRADE sequence (my §2) makes idempotency, fail-open and rollback free by construction, because primitives only ever hold the read-only five verbs and never touch index state (FR-06, FR-07). My distinctive, defensible core is the asymmetric evidence rule (graph positives act, graph emptiness never does), the mutation-exclusion grep test, and the docs-only-diff escalation key. I concede upfront: C-001 scope drift, the X-002 allowlist self-contradiction, the X-008 "replace can narrow" gate design, X-013 tests-in-severity, and the X-015/X-018/X-019 fact-check losses.

## Steelman

### Variant A (architect)

The strongest version of A: it is the only variant that enumerated the full operational blocker surface — B5 telemetry on the CLI path (Bash calls do not inherit the MCP entry's `CODEGRAPH_TELEMETRY=0`; EVAL §1 says telemetry is default-on), B7 (node file mode is invisible to the `Read` freshness matcher, `hooks.json:59`), U-003 (Markdown-heavy repos get no graph signal, EVAL §5.4: python/yaml/liquid only). Its `resolution: def-line|call-site-verified|unresolved` field is the most engineered citation mechanism, it found `query --json` `endLine` (EVAL §5.5) to bound call-site Grep, and its capability-map seam (consumers name capabilities, not tools) is the right abstraction against a single-maintainer upstream shipping 8 releases/quarter (EVAL §1). A genuinely gets right: the blocker table with owners, `/sc:graph` as a dedicated, user-typed init owner, and pre-fix impact in remediation chains (U-006).

### Variant B (analyzer)

The strongest version of B: its M/P/A evidence classes refuse to rank unmeasured benefit as equal to measured, and that discipline produced the two best catches in the debate — U-009 (the 20-of-23 callers sample held 2 production callers and 18 test functions, EVAL §5.5, so a naive 1:1 swap trips reflect's ">5 referencing call sites" HIGH rule on tests alone) and U-010 (the NFR-08 backtest gate before any VG-1 change, since EVAL never ran `affected`). Its artifact-in-brief access model removes the `CODEGRAPH_MCP_TOOLS` blocker with zero env dependency by following repo precedent (`sc-troubleshoot-protocol/SKILL.md:281` producers table; reflect reviewers audit pre-computed hunks), and its golden fixtures (U-012) are the correct defense against text-output drift. B genuinely gets right: B7 (no documented `--json` for `callers`/`impact`/`status`, EVAL §3), the provenance check (`index_root` == worktree realpath), and the honest "status timing UNVERIFIED".

## Strengths claimed

1. **The contract sequence is the idempotency and rollback story in one artifact.** §2's fenced PROBE→CALL→VERIFY→DEGRADE block with a run-scoped latch (FR-02: one probe, never retried) and FR-07 (cache per run, one affected computation per validation cycle) is the only proposal where re-running a wave is provably side-effect free. EVAL §5.7 ("scripts must not rely on `codegraph sync` succeeding while an agent session is open") makes A's try-one-sync a latent flake; my FR-06 mutation-exclusion grep (`codegraph (init|index|sync|uninit|unlock|upgrade|install)` → 0 hits) is machine-checkable.
2. **Asymmetric evidence is fail-safe where A is fail-risky.** My I-07: `impact > 0` upgrades a DELETE to REVIEW; `impact = 0` proves nothing. A's I-12 uses "zero graph callers is extra evidence for DELETE" — the graph has no text search and misses string/config references (EVAL §6.1), so A's direction can manufacture false DELETEs; mine can only add conservatism. The cleanup-audit grep gate (`sc-cleanup-audit-protocol/SKILL.md:75`, verified) stays untouched either way.
3. **The edge-case table maps every observed EVAL behavior to a contract response** (§8: uninitialized sibling, nested-worktree-with-warning, writer lock, `install` ambiguity, "Showing 20 of 23" truncation, docs-only diff, CLI-vs-MCP latency, connect-time catch-up). Neither A nor B gives a row-per-behavior mapping; U-018/U-021/U-022 (stale→HIGH-as-MEDIUM; docs-only diffs may honestly yield no tests) came out of it.
4. **Nine-vector coverage is declared up front with net positions** (§1 table), so a reader can audit vector coverage before reading ideas. A has no explicit map; B buries it in §4.
5. **`source: graph|heuristic|none` provenance in `/sc:test-scope` (C-3/FR-05)** makes test-selection provenance observable in the run-log next to the VAL gates, and FR-05's escalation keys on source-file diffs so a docs-only diff may honestly yield no tests (U-022) while a src diff with empty graph output can never silently skip tests.
6. **CLI-first for Bash-capable orchestrators is available today.** A's Class A default (MCP for troubleshoot/reflect) is gated on B1, an unowned installer env change (EVAL §7 step 5 sets only telemetry vars). My position needs no blocker resolution for the highest-frequency consumers.
7. **`/sc:ground` (C-4) centralizes FR-03 enforcement**: graph locates, Read verifies, dropped rows carry reasons (`no_match|unverified|ambiguous`). This keeps re-Read-before-cite enforceable in one place rather than re-implemented per consumer.
8. **Dropped ideas include the two hygiene drops others missed**: any primitive running `sync` (writer lock, EVAL §5.7) and splitting `/sc:impact`//`sc:test-scope` into per-skill private scripts, which would recreate the six-divergent-copies drift I-01 exists to remove.

## Weaknesses identified in other variants

1. **A's "try one `sync`" (X-006)** is a mutation from a read path that EVAL §5.7 explicitly warns against; even the success case (CLI-only session, no daemon) makes a "read-only grounding" step write index state, breaking A's own NFR-07 ("no new side effects").
2. **A binds VG-1 to an unmeasured command.** Immediate union (FR-07) is direction-safe (never narrows) but EVAL never ran `affected` (A-008, conceded by B alone); B's advisory→backtest→union sequencing is the operationally correct order. A also claims `status` ≈ 300 ms "EVAL §5.5" (X-017) — §5.5 timed `query`/`callers` (290/297 ms); status timing was not captured.
3. **A edits the evidence-validator and lists it in Class D for MCP names** (X-004). Even as text-only, teaching the independent last gate to treat def-line rows as a special citation class weakens the one validator whose job is disk-truth; B and I keep it `Read, Grep, Glob`.
4. **A's I-17 SessionStart hook** adds a ~300 ms CLI call to every session start, including repos with no `.codegraph/`; B's D-03 (the probe already answers on demand; `freshness-pre-edit.sh` timeout is 1 s) is decisive.
5. **B's `dependent-impact` exemption from the out-of-hunk downgrade (X-009)** is the boldest gate change in the debate, built on Class P (self-admitted UNVERIFIED benefit) and a Python-regex hunk-to-symbol extractor (B's own OQ-7 doubts non-Python). The Read-verified guard is well designed, but it should land behind B's own backtest discipline, not before it.
6. **B's CLI-only-everywhere stance ignores the measured 3-15 ms MCP vs 290-300 ms CLI gap** (EVAL §5.6) for per-hunk loops — reflect Step 1B.3 over ≥3 tasks × hunks at 300 ms per call compounds; my edge-case table names this and prefers MCP where listed.
7. **B's `/sc:load --index` runs `init` inside an onboarding command** (X-005/X-016): a 34 MB, ~1 GB-RSS write path (EVAL §5.4) inside `/sc:load`, however flag-gated, mixes mutation into context-loading; A's dedicated `/sc:graph` that refuses nested worktrees without `--worktree-local` is the cleaner ownership.
8. **B's "Grep sees every static reference the graph sees" (D-05, X-020) is asserted, not measured** — EVAL states neither direction; it reports "Linking dynamic dispatch" at index time (§5.4) and interface→impl dispatch via explore (§6.2). Both B's slogan and mine ("grep misses ≠ graph misses") are UNVERIFIED; the safe operational rule is corroboration-only in either direction, which is what I-07 actually implements.

## Concessions

1. **C-001 scope drift is real.** I-02's "replace Serena overview/find_symbol rows", I-04's `find_declaration` anchoring and I-05's `find_referencing_symbols` replacement overlap the INV §4 1:1 work the seed scoped out; only I-04's diff-hunk→symbol derivation and I-05's severity-semantics change are genuinely "beyond". I-02's framing should be rewritten as a Tier-1 restructure that composes with the 1:1 plan.
2. **X-002 self-contradiction.** My §2 says "no allowlist change beyond adding `Bash(codegraph *)` patterns" and I-07 uses a `;`-joined pattern, while my FR-10 forbids bare `Bash(codegraph *)`. FR-10 is the correct half; B's per-subcommand rule is the resolution I adopt.
3. **X-008/C-013: my test-selection design can narrow the gate.** FR-05's "tests is exactly the parsed affected list" replaces `<changed-area>` and can shrink today's set on an unmeasured command (A-008). B's advisory→backtest→union order is superior; my surviving contribution is the `source:` provenance field and the docs-only-diff rule, which fold into B's union stage.
4. **X-013/C-017: "re-word to caller count (tests included)" is measurably wrong.** EVAL §5.5's sample: 2 production callers among 23. B's prod-only distinct-caller count (FR-09, runtime-surface table) is required; my stale→HIGH-as-MEDIUM demotion (U-021) remains a good addition on top.
5. **X-015: I cited the wrong wave's budget.** Verified: `sc-troubleshoot-protocol/SKILL.md:218` sets Wave 1 (Tier 1) at ~3k tokens; `:256` is Wave 1.5's 2k. My I-02 and NFR-02 both misattribute 2k to Tier 1.
6. **X-018: my MCP tool names would not match.** EVAL §3 names the tools `codegraph_search`, `codegraph_callers`, …, so the server-prefixed names are `mcp__codegraph__codegraph_*` (A's form). My `mcp__codegraph__search`-style entries in read-only-agent `tools:` lines would silently fail.
7. **X-019: CLI `node [name]` does not document file/symbolsOnly mode** (EVAL §3 CLI table); my I-02 claim "skill has Bash → CLI works today" is unsupported for the file-outline path — file-mode node is MCP-only, which is B1-blocked. I-02's CLI path must fall back to `query --json`/Grep outlines.
8. **A-006 bites my design too:** my FR-07 caches graph results for the whole run while implement/pr-submit edit files mid-run, so post-edit queries can read a pre-edit index. FR-03's re-Read drops stale rows, but B's re-probe-before-queries after in-run edits is the stronger freshness floor.

## Shared assumptions

| A-ID | Position | Reason |
|---|---|---|
| A-001 | ACCEPT | Seed constraint; my NFR-01/FR-01 encode it with a degraded key per step |
| A-002 | ACCEPT | EVAL §5.5 definition-line gap; my FR-03 makes re-Read the only citation-grade bridge |
| A-003 | QUALIFY | The policy (explore never a default step) stands on its own measured cost (24,913 chars, EVAL §5.6); the auggie-is-free rationale does not — auggie itself is fallible (troubleshoot already accepts a Glob/Grep floor), so fallbacks must chain to Grep/Read, not to auggie |
| A-004 | QUALIFY | Sample of one; the ban costs nothing so keep it, but a bounded `maxFiles≤5` single-symbol measurement would close the question |
| A-005 | QUALIFY | EVAL §5.5-§5.6 measured latency only, never output size; my ~1k caps are estimates — enforce caps, don't assume cheapness |
| A-006 | QUALIFY | Latch is right for availability, wrong for freshness: no watcher runs in CLI-only sessions (EVAL §4) and orchestrators edit mid-run; re-probe `status` before graph calls that follow in-run writes |
| A-007 | QUALIFY | Verified on one symbol (§5.5); my I-03 already calls the callers list "a floor, not exhaustive" — treat non-empty as partial, never complete |
| A-008 | REJECT (for gates) | EVAL never ran `affected`; usable advisory-only until B's NFR-08 backtest passes — my I-09 as written violates this and must adopt the backtest |
| A-009 | ACCEPT | init writes ~34 MB at ~1 GB peak RSS (EVAL §5.4); read-only flows must never init |
| A-010 | ACCEPT | EVAL §5.8 warning text is pinned behavior; foreign-index rows are citations of another tree |
| A-011 | QUALIFY | No owner exists (EVAL §4, §7); consumers must ship anyway (fail-open), and degraded-key frequency in audit logs is the signal for when to fund an init owner |
| A-012 | QUALIFY | Orchestrators invoke a peer skill; agents Read refs by installed path (EVAL §3: subagents never see server instructions, so ref-by-path is the only channel); B's Skill-call-cost question (Q-6) is real — my C-1 is guidance-only with no args/output to minimize it |

## Per-point positions

| ID | Superior | Reason |
|---|---|---|
| S-001 | A | Traceable front matter incl. ground_truth and date |
| S-002 | none | Identical section order across variants |
| S-003 | C | Nine-vector table with net positions in §1 is auditable before reading ideas |
| S-004 | A | 7 lettered classes + B1-B7 owner table is the most complete access model |
| S-005 | B | M/P/A evidence classes beat raw V/E/R scales and my nothing |
| S-006 | B | 10 ideas, each evidence-classed, no filler |
| S-007 | B | Score table with stated method, sequencing and coverage notes |
| S-008 | A+B | IDed drops cross-reference cleanly; my bullets do not |
| S-009 | A | Per-candidate subsections carry full interface detail |
| S-010 | C | Observed-behavior→contract-response table maps every EVAL edge to a FR |
| S-011 | B | Most specific requirements, incl. golden fixtures and backtest |
| C-001 | A+B | Both exclude the 1:1 swaps; I drifted (conceded) |
| C-002 | B+C | CLI-first orchestrators (C, no blocker) composes with artifact-in-brief agents (B) |
| C-003 | B | Do not set the env in v1; measure schema overhead first |
| C-004 | B | Per-subcommand patterns; my own FR-10 agrees, my §2 text erred |
| C-005 | C | Guidance-only contract, no args/output, lowest coupling; A's capability map is the better backend-swap abstraction and should merge in |
| C-006 | A+B | A's closed vocabulary + B's `parse_failed`; my binary available/unavailable under-discriminates |
| C-007 | C | Never sync; first probe authoritative + stale flag; A's try-one-sync is the flake |
| C-008 | A | Ban explore from primitives entirely; my maxFiles door adds surface for no consumer need |
| C-009 | B | Resolver script with measured `query --json` span + in-span Grep + Read is the most concrete |
| C-010 | B+C | Validator stays Read/Grep/Glob (B and C agree); A's edit risks the independent gate |
| C-011 | A | Pre-edit Q1 impact plus pre-fix impact in remediation chains is the fullest coverage |
| C-012 | B | Blast-radius artifact + Read-verified `dependent-impact` is the only fix for the chunking blind spot |
| C-013 | B | Advisory→backtest→union; my replace-form can narrow the gate (conceded) |
| C-014 | B | Positional args / `--stdin` from file; pipeline matching under scoped Bash is UNVERIFIED |
| C-015 | A | search+node+callers in Wave 1 and 1.6 as one edit; my split is thinner and I-02's CLI claim failed X-019 |
| C-016 | C | Informational risk note in both workflow and tasklist; determinism intact because it never feeds tiering |
| C-017 | B | Prod-only distinct callers; the 2-of-23 sample makes test-inclusive counts wrong |
| C-018 | B | No new reflect field in v1; `degraded_components` only, zero parser risk |
| C-019 | C | Asymmetric: positive upgrades to REVIEW, empty proves nothing; A's zero-callers-DELETE-confidence is fail-risky |
| C-020 | A | Caller-liveness check closes a real false-recommendation class |
| C-021 | B | structure-brief + load --index is the most substantive onboarding move |
| C-022 | B+C | No new hooks; the probe answers on demand (B's D-03 latency argument) |
| C-023 | A | Dedicated `/sc:graph`, user-typed, refuses nested worktrees; I left B2 unowned |
| C-024 | B | Confidence-weighted ranking is the most defensible method |
| C-025 | A | Layer-0 allowlists→contract→citation is the true dependency order; my #2 (affected) was premature |
| C-026 | B | Best-evidenced drops (hook latency vs 1 s timeout, producer enumeration is text search) |
| C-027 | C | Four candidates incl. `/sc:ground`, the shared verify layer that centralizes FR-03 |
| C-028 | B | Prod/test partition, truncated, ambiguous, unmapped_files — richest and best semantics |
| C-029 | B | Widest caller set incl. load, index-repo, explain |
| C-030 | B | Shown/total + one re-query ≤100 + notes CLI callers lacks a file arg |
| C-031 | B | Golden fixtures + backtest are the strongest guards against measured drift risk |
| C-032 | A | Telemetry-on-CLI-path and Markdown-repo honesty are the two highest-value risk finds |
| C-033 | C | Delete-the-text rollback restores today's behavior byte-for-byte; no kill switch to maintain |
| X-001 | B | No MCP names in v1; artifacts by path remove the blocker entirely |
| X-002 | B | Never wildcard; my FR-10 was right, my §2 wording was not |
| X-003 | B | Defer the env decision with a measurement gate |
| X-004 | B+C | Validator keeps Read/Grep/Glob |
| X-005 | A | User-typed dedicated command owns init; B buries it in /sc:load, C forbids all |
| X-006 | B+C | Never sync from primitives (EVAL §5.7) |
| X-007 | B+C | No SessionStart hook |
| X-008 | B | Backtest before any gate change |
| X-009 | B | Read-verified exemption only, landed after the backtest |
| X-010 | C | Risk field is informational; determinism concern applies to tiering, which I do not touch — label it `graph_derived` so reflect never reads it as fact |
| X-011 | A | Adoption plus caller files named in acceptance criteria is more actionable than my count-only field |
| X-012 | C | Asymmetric evidence; empty is never proof |
| X-013 | B | Prod-only distinct caller symbols |
| X-014 | A | Total primitive ban; no step needs explore |
| X-015 | A | Correctly cites :218 ~3k; I cited Wave 1.5's 2k (conceded) |
| X-016 | B | load gains an index owner; A's status line is thinner, my drop orphans B2 |
| X-017 | B | "status timing UNVERIFIED, measure" is the accurate read of EVAL |
| X-018 | A | `mcp__codegraph__codegraph_*` is the correct form; mine would not match |
| X-019 | B | File-mode node is MCP-only; mechanisms resting on `query --json` are measured |
| X-020 | C | Operationally: corroboration-only in both directions; epistemically both slogans are UNVERIFIED |
| X-021 | B | Reads only the 20 shown rows; the 3 hidden stay unknown |


## Round 2: Rebuttals

### Variant A Rebuttal (opus:architect)

<!-- verbatim: working/round2-A.md -->

# Round 2 — Advocate A (variant-1-opus-architect), sequential rebuttal (first)

Notation: A/B/C = variants 1/2/3; EVAL = `research/codegraph-evaluation.md`. Primitive paths are relative to `src/superclaude/` and were re-read for this round: `agents/evidence-validator.md:5,62-66`, `skills/sc-pr-submit-protocol/SKILL.md:203-206`, `skills/sc-implement-protocol/SKILL.md:118-119`, `cli/install_skill.py:47-52`.

## Response to criticisms

**B-1.** "A's formula multiplies by a 'Frequency' factor that is also subjective" (round1-B Strength 1).
Partial concession. Frequency is closer to observable than Value, because it records how often the host primitive runs (every PR, every level-3 run). B concedes its own V is judgement too (B Concession 9). But the real flaw is a different one: A's formula has no confidence term. It ranked I-06 and I-08 at 5 and 6, and both rest on `affected`, which EVAL never ran (EVAL §5 has no `affected` run). B's M/P/A weight would have demoted both. The merged ranking should take B's confidence multiplier on top of A's Layer 0.

**B-2.** "A greps 'after the def line' with no end bound (I-02), which can match a different function in the same file" (B Strength 4).
Mostly wrong on the facts. A's I-02 mechanism column says "`codegraph query <s> --json` gives `startLine`/`endLine` (EVAL §5.5) to bound the search" (variant-1 line 61), and C's Round 1 steelman credits A with exactly this bound. Concession: the bound appears only in the mechanism column. It is missing from the idea's procedure and from FR-04, so an implementer could miss it. B's `resolve-callsite.sh` makes the same mechanism executable and testable, so it is the better delivery. See New evidence 6 for a gap that both A and B share.

**B-3 / B-4 / B-5 / B-8 / B-9.** These cover the wildcard `Bash(codegraph *)`, MCP names in read-only agents, evidence-validator in Class D, "try one `sync`", "~300 ms" for `status`, and "zero callers is DELETE evidence". A conceded all six in Round 1 (round1-A Concessions 1-6), and nothing in B's or C's defenses reopens them. A's Layer 0 I-03 therefore shrinks to per-subcommand CLI patterns in Class C only.

**B-6.** "A unions `affected` into VG-1 at once (X-008) on a tool EVAL never ran" (B Weakness 8). C says the same but calls the union "direction-safe" (C Weakness 2).
Full concession, and a stronger one than Round 1. A's Strength 8 claimed the superset is "safe by construction". That holds only against *missed* tests. VG-1 is `uv run pytest <changed-area>`, and "Any non-zero gate blocks the push" (`sc-pr-submit-protocol/SKILL.md:203-206`). So a union that adds a wrong or uncollectable path from an unparsed `affected` output fails VG-1 and blocks a correct push. (Pytest exits non-zero on a path it cannot find; this is general pytest behaviour, not re-checked here.) A union can therefore produce false blocks as well as extra runtime. B's sequence is required before any gate change: advisory delta first, then the 20-change backtest (NFR-08), then the union. A's `selected ⊇ heuristic` rule (FR-07) survives only as the invariant that governs the union stage.

**B-7.** "A's 19 ideas include a tail with its own admitted score of 0.7-1 … A formula the author overrides is not a method" (B Weakness 9).
Partial concession. The I-16 override was disclosed with its reason ("duplicates I-17/I-19"). Now that I-17 is deferred, that reason is weaker and I-16 rises back to its formula rank. Accepted trims: drop I-15 (score 0.7; Glob already gives the structure). Rewrite I-12 to C's asymmetric rule. Fold I-09 into the review merge as stage 1 (context only). Defer I-11 (see C-020). The architecture value of A is the scaffold (C-1..C-4), not the count of ideas.

**C-3.** "A edits the evidence-validator … teaching the independent last gate to treat def-line rows as a special citation class weakens the one validator whose job is disk-truth" (round1-C Weakness 3).
Counter on "weakens": A's FR-04 test asks the validator to *reject* a def-line row cited as a call site (`line-mismatch`), which makes it stricter, not looser. Concession on the edit itself: it is unnecessary. The validator already Reads ±5 lines and compares the quoted snippet, and rejects semantic differences (`evidence-validator.md:62-66`). A call-site snippet cited at `main.py:46` would face `def install(` there (EVAL §5.5) and fail today. So the validator stays byte-identical, and the `resolution` rule lives only in the producer ref (C-1 `refs/citation-resolution.md`).

**C-4.** "A's I-17 SessionStart hook adds a ~300 ms CLI call to every session start" (C Weakness 4).
Conceded as deferral (Round 1 Concession 8). Note that C's "~300 ms" reuses A's own unverified number (X-017). The cost is unmeasured in both directions.

**C-5.** C-033: "Delete-the-text rollback restores today's behaviour byte-for-byte; no kill switch to maintain" (round1-C per-point).
Partial concession, backed by new evidence (New evidence 1-2). A's FR-16 switch is a source-level switch, not a runtime one. It is still cheaper than a multi-file revert, because flipping one header disables every consumer, which deleting text across about 10 primitives does not. Merge: FR-16 as the release-level switch, plus B's "binary absent equals the native path" as the runtime switch.

**C-6.** C-005: "Guidance-only contract, no args/output, lowest coupling" (C per-point).
Counter. A seam with no output schema pushes every consumer to invent its own degraded keys. C's own §6 shows free-form keys such as `test-scope:codegraph_stale`, which is the drift that C's I-01 says it prevents. Concession: C's PROBE→CALL→VERIFY→DEGRADE block is the clearest procedure text and should be the body of A's C-1 `SKILL.md`.

**C-8.** X-016: "load gains an index owner; A's status line is thinner, my drop orphans B2" (C per-point).
Counter: B itself picks A's dedicated `/sc:graph` over its own `/sc:load --index` (round1-B C-023, X-005), because `init` writes 34 MB at about 1 GB RSS (EVAL §5.4). A one-line status in `/sc:load` that points to `/sc:graph init` gives the visibility without putting a mutation inside a context-loading command.

## Updated assessment of B and C

**B.** B's defenses hold on every gate-safety point, and its concessions are accurate: X-021 (20 of 23 inspected), X-020, telemetry, language scope, and its FR-12 being the riskiest change. B is the superior variant on evidence discipline and on the v1 access model. Its remaining gaps are architectural ones that B partly accepts (round1-B C-005, C-023, C-027 all pick A+B or A): it has no capability map, no lifecycle owner, and no release-level switch. Two of its own claims are in tension and should be reconciled in the merge: "probe once per run" (FR-01) and "re-run `status` before the queries" (§8).

**C.** C's concessions are broad and honest: C-001, X-002, X-008, X-013, X-015, X-018, X-019 and A-006. That leaves three durable contributions: the asymmetric cleanup rule (X-012), the edge-case table with the docs-only-diff rule (U-022), and the mutation-exclusion grep (FR-06). C's remaining positions conflict with its own concessions. C-007 "first probe authoritative" and FR-07 per-run caching both contradict C's A-006 concession, and the tasklist risk note (X-010) still changes tasklist output by index state. C's strongest new point against B is real: MCP calls take 3-15 ms against about 300 ms for the CLI (EVAL §5.5, §5.6). That supports a later MCP stage for loop-heavy orchestrators, and it argues for A's capability map, where switching access path is a one-file change.

## New evidence (not presented in Round 1)

1. **The kill switch is erased by reinstall.** `cli/install_skill.py:47-52` runs `shutil.rmtree` and then `copytree` under `force`, and `./update.sh` runs `superclaude install --force` (EVAL §2). A user who flips `status: disabled` in `~/.claude/skills/sc-graph-grounding/refs/capability-map.md` loses the change on the next update. FR-16 therefore needs a source edit and a release.
2. **A's NFR-08 is partly wrong.** It says "removing the codegraph registration … makes every consumer degrade". Class B/C consumers default to the CLI (A §2.1), and CLI subcommands do not depend on the MCP registration (EVAL §3, §5.5 ran the CLI without MCP). The runtime off switch is the binary being off PATH (B's FR-01 test), not de-registration.
3. **Pinning by file is MCP-only.** CLI `callers <symbol>` takes no file argument, and `node [name]` has no file or `symbolsOnly` mode (EVAL §3 CLI list; B noted the first under C-030). So A's ambiguity rule "always pass `file`" (§8), I-09, and C-2 `--diff` hunk-to-symbol mapping work only on the MCP path, which is B1-blocked. On the CLI path they need `query --json` matches filtered by file, or an IronClaude-side extractor (B's approach). C-2 `--diff` is not v1-ready on the CLI.
4. **A false block is a real failure mode of the union.** See B-6: `sc-pr-submit-protocol/SKILL.md:203-206`.
5. **Pre-edit impact cannot license edits outside the task.** `sc-implement-protocol/SKILL.md:118-119` reads "Implement only that task", and a drive-by file is a minor unless a breach applies. A's I-05 output should therefore feed the Q3 review package and the ledger, not widen Q1 edits. B's post-edit check covers what actually changed. The two are complementary (C-011 becomes A+B).
6. **The span lookup is itself ambiguous.** `query` is a name search. The explore sample matched two unrelated `install` functions (`eval/signal_handler.py:195`, `cleanup_audit/process.py:57`; EVAL §5.6). A resolver that runs `query <caller> --json` must select the match whose file and `startLine` equal the caller row's file and def line, and it must mark the row `unresolved` otherwise. Neither A's I-02 nor B's `resolve-callsite.sh` states this.

## Shared assumptions — changes only

| A-ID | New position | Reason |
|---|---|---|
| A-008 | REJECT (as a v1 gate input; was QUALIFY) | EVAL never ran `affected`, and a union can false-block VG-1 (`sc-pr-submit-protocol/SKILL.md:203-206`), not only inflate it. `affected` is advisory until B's NFR-08 backtest passes |

## Updated per-point positions

| ID | Superior | Changed? |
|---|---|---|
| S-001 | A | no |
| S-002 | none | no |
| S-003 | C | no |
| S-004 | A+B | no |
| S-005 | B | no |
| S-006 | A+B | no |
| S-007 | A+B (Layer 0 + B's confidence-weighted table) | yes |
| S-008 | A+B | no |
| S-009 | A+B | no |
| S-010 | A+C | no |
| S-011 | none | no |
| C-001 | A+B | no |
| C-002 | B+A (B artifacts for v1 agents; A's Class A MCP once listed) | no |
| C-003 | B | no |
| C-004 | B | no |
| C-005 | A+B+C (A's map/schema, B's probe/resolver, C's sequence text) | yes |
| C-006 | A+B | no |
| C-007 | B | no |
| C-008 | A | no |
| C-009 | A+B+C (typed resolution, B's resolver + file/startLine match, C's drop-never-repair) | yes |
| C-010 | B+C (validator unchanged) | yes |
| C-011 | A+B (pre-edit for named symbols, post-edit on the actual diff) | yes |
| C-012 | A+B | no |
| C-013 | A+B (B's sequence, A's invariant at the union stage) | no |
| C-014 | A | no |
| C-015 | A+B | no |
| C-016 | A | no |
| C-017 | B | no |
| C-018 | B | no |
| C-019 | C | no |
| C-020 | B (defer; agents have no MCP in v1, and candidates cannot be precomputed) | yes |
| C-021 | A (minus I-15) | no |
| C-022 | B | no |
| C-023 | A | no |
| C-024 | A+B | no |
| C-025 | A+B | no |
| C-026 | A+B+C (adds C's `sync` drop) | yes |
| C-027 | A+B (A's four slots, B's probe/blast-radius content) | yes |
| C-028 | A+B (A's modes and caps, B's prod/test split; `--diff` MCP-gated) | yes |
| C-029 | A | no |
| C-030 | B | no |
| C-031 | A+B | no |
| C-032 | A+B | no |
| C-033 | A+B (source switch + binary-absent runtime switch) | yes |
| X-001 | B | no |
| X-002 | B | no |
| X-003 | B | no |
| X-004 | B+C | yes |
| X-005 | A | no |
| X-006 | B+C | no |
| X-007 | B | no |
| X-008 | A+B | no |
| X-009 | A+B | no |
| X-010 | A+B | no |
| X-011 | A | no |
| X-012 | C | no |
| X-013 | B | no |
| X-014 | A | no |
| X-015 | A+B | no |
| X-016 | A | no |
| X-017 | B | no |
| X-018 | A | no |
| X-019 | B (A's I-09 and C-2 `--diff` also rely on MCP-only `node symbolsOnly`) | yes |
| X-020 | none | no |
| X-021 | A | no |

### Variant B Rebuttal (sonnet:analyzer)

<!-- verbatim: working/round2-B.md -->

# Round 2 — Advocate B (variant-2-sonnet-analyzer), sequential rebuttal (second)

Notation: A/B/C = variants 1/2/3; EVAL = `research/codegraph-evaluation.md`. Primitive paths are relative to `src/superclaude/`. Re-read for this round: `skills/sc-auggie-review-protocol/SKILL.md:124-141,214-219`, `skills/sc-pr-submit-protocol/SKILL.md:200-209`, `skills/sc-implement-protocol/SKILL.md:116-123`, `cli/install_skill.py:44-55`, `skills/sc-cleanup-audit-protocol/SKILL.md:72-87`, EVAL lines 96, 195, 209-214, and A's variant line 61.

## Response to criticisms

**1.** (round1-A) "B has no capability abstraction (B §6 N-1 interface is readiness-only). Adding MCP later, which B's own Q1 contemplates, means editing every consumer." Repeated in round2-A: "it has no capability map, no lifecycle owner, and no release-level switch."
Partly wrong on the facts, partly right. Consumers do not hold CLI knowledge in B: N-1 owns probe, provenance and `resolve-callsite.sh`, and N-2 owns `callers`/`impact`/`affected` invocation, parsing and the prod/test split (B §6). What each consumer holds is a Step-0 line plus allowlist lines, and those are edits A's capability map would not remove either. The criticism holds in one respect: nothing in B says "capability X is served by CLI form Y today and MCP tool Z once listed", and B's own Q1 leaves that door open. Concession: add a small `refs/capability-map.md` inside N-1 (capability, CLI form, MCP tool name `codegraph_*`, fallback, tested version). It is cheap and also lists the golden-fixture commands. I do not accept it as a "kill switch" (see item 8).

**2.** (round1-A, round1-C, round2-A) "B's FR-17 lets `/sc:load --index` run `init --yes` ... in a session-context command. That breaks separation of concerns." (A); "B's `/sc:load --index` runs `init` inside an onboarding command" (C).
Conceded, as in Round 1 (X-005 = A). EVAL §5.4 puts `init` at about 1 GB peak RSS and 34 MB written. A user-typed `/sc:graph init` with the nested-worktree refusal (EVAL §5.8) is the cleaner owner. I withdraw FR-17 and I-09's `--index` flag. It follows that X-016 should be A's read-only status line and nothing else (changed below).

**3.** (round1-A, round2-A) "B's FR-01 runs 'N-1 once per run' while its §8 says 're-run status immediately before the queries'. That is an internal inconsistency (A-006)." / "Two of its own claims are in tension."
Conceded. I re-read B: FR-01 says "once per run before any other codegraph call"; §8 says "not once per session". Those are not literally contradictory (run vs session), but FR-01 as written does not require a freshness re-check. Resolution for the merge: availability and provenance (`version`, `index_root == realpath`) are latched once per run; `status` freshness is re-run before every query batch that follows an in-run write. Put that split in FR-01 and in N-1's output (`checked_at`).

**4.** (round1-A, round1-C) "B's D-05 claims 'Grep sees every static reference the graph sees'. EVAL does not support this." / "asserted, not measured."
Conceded again (X-020). I also concede the follow-on: B's D-05 rests partly on that sentence, and what remains does not carry the whole drop. The READ-ONLY charter does not forbid a query step (a `callers` query writes nothing), and `:86` ("MCP tools are unavailable to background subagents ... execute in the orchestrator only") only moves the call to the orchestrator. What survives: `:75` keeps grep as the DELETE gate, and the graph's marginal value is unmeasured. I now move C-019 to C's asymmetric rule (nonzero graph callers upgrade DELETE to REVIEW; zero proves nothing), orchestrator-only, low rank, gated on a one-hour spike showing the upgrade ever fires where grep did not. A's "zero = extra DELETE evidence" remains wrong (violates my own FR-07).

**5.** (round1-A) "Its `sc-structure-brief` (N-3) is a new skill for value that B itself rates P-class at 0.6 (rank 9)."
Conceded. B's own score table ranks I-10 at 0.6 with "token claim unmeasured", and the "58K to 3K" figure belongs to the primitive, not to a measurement. Defer N-3. A's lighter in-place edits (explain one-hop, load status line; A's own R2 drops I-15) are cheaper. This leaves B with two candidates, so the merged candidate set has to take A's `/sc:graph` to meet the brief's 3-5 range.

**6.** (round1-A) "B also overstates the sample: 'the rest were test functions'. EVAL §5.5 shows only 20 of 23 rows."
Already conceded (X-021). EVAL line 195 shows "20 of 23"; the 3 hidden rows were not inspected. The hazard stays valid as direction (tests inflate counts) and rests on one symbol.

**7.** (round1-C) "B's `dependent-impact` exemption from the out-of-hunk downgrade (X-009) is the boldest gate change in the debate, built on Class P ... and a Python-regex hunk-to-symbol extractor."
Conceded in Round 1 (Concession 7), and I tighten it. FR-12 has no gate of its own; only `affected` has NFR-08. Merge rule: stage 1 ships the blast-radius artifact as context only (A's I-09 and my I-04 agree on this). Stage 2 ships `dependent-impact` in shadow: it is reported as ordinary "context", and the audit log counts how many Read-verified rows the `:218` downgrade would have dropped over a fixed number of reviews. The exemption is enabled only if that count is nonzero and the false-positive rate is acceptable.
Correction to my own Round 1 wording: I wrote that a broken caller "can never surface today". `:218` says an out-of-hunk finding is "downgraded to 'context' or dropped, depending on severity", so it can surface as context. Also, `:136-137` shows directory chunking happens only for 16-30 files or 1500-5000 diff lines; up to 15 files go to a single Auggie call. My I-04 blind-spot claim applies fully only to that middle band, plus the out-of-hunk rule at every size. I lower I-04's V from 4 to 3: 3 x 0.6 / 2 = 0.9, a tie with I-06 and I-08. On B's own tie-break (lower risk), I-06 (risk L) outranks I-04 (risk M), so I-06 moves to rank 5.

**8.** (round1-A strengths 2 and 3; round2-A "no release-level switch") "B relies on uninstalling the binary, and C relies on deleting text."
Half right. B's runtime switch is real (NFR-07: `codegraph` absent equals the native path, tested per primitive). A's round2-A New evidence 1 shows the other half is weaker than claimed: `install_skill.py:46-48` does `shutil.rmtree` then `copytree` under `force`, so a `status: disabled` edit in an installed ref is erased by `./update.sh`. A's switch is a source edit plus release, which is still cheaper than touching about 10 primitives. Fair combination: A's header as the release-level switch, B's absence-equals-native as the runtime switch. A's NFR-08 text on MCP de-registration is also wrong for CLI-default consumers (A's own point 2), which supports B's FR-01 test.

**9.** (round1-C) "B's CLI-only-everywhere stance ignores the measured 3-15 ms MCP vs 290-300 ms CLI gap (EVAL §5.6) for per-hunk loops — reflect Step 1B.3 over >=3 tasks x hunks at 300 ms per call compounds."
The numbers are right (EVAL lines 188 and 209-214: callers 297 ms by CLI; 3 and 15 ms by MCP). The conclusion does not follow for B's design. B's artifacts are computed once per run per changed symbol, not per hunk per task, and capped (FR-10: 40 rows, 6 KB). Arithmetic from EVAL numbers (an estimate, not a measurement): 30 symbols x 300 ms is about 9 s, inside NFR-01's 15 s. The argument becomes valid when serial CLI queries pass roughly 100 in a run (about 30 s), and then MCP, listed per the capability map, is the better path. Concession: B's "irrelevant at 30-60 calls" (§2.1) is arithmetic, not a measurement, and NFR-01 should log the actual query count so the MCP switch is data-driven. I move C-002 to "B for v1, A's MCP classes after measurement".

**10.** (round2-A New evidence 6) "The span lookup is itself ambiguous ... a resolver ... must select the match whose file and `startLine` equal the caller row's file and def line, and it must mark the row `unresolved` otherwise. Neither A's I-02 nor B's `resolve-callsite.sh` states this."
Accepted, with one detail. B's §8 says "require a unique kind/file match, else `ambiguous[]`", and the script has `--file`, but neither binds the match to the caller row's def line. EVAL line 195-ish and §5.6 show the name-search hazard (two unrelated `install` functions). The binding rule is stricter and correct: match `(file, startLine == def_line)`, else `unresolved`. I also accept A's typed row field as the row-level form of B's `call_site_status`.
Correction to my Round 1: I wrote that A greps "after the def line" with no end bound. A's I-02 mechanism column says "`codegraph query <s> --json` gives `startLine`/`endLine` ... to bound the search" (variant-1 line 61). That claim of mine was wrong on the facts. A's gap is only that FR-04 does not repeat it.

**11.** (round1-A strength 7; round2-A New evidence 5) "Its pre-edit impact runs earlier than B's post-edit context."
Partly conceded. A's own R2 point stands: `sc-implement-protocol/SKILL.md:118` says "Implement only that task", and `:119` makes a drive-by file a minor unless a breach applies, so pre-edit impact cannot widen Q1's edits. Its remaining value is a warning to the implementer and input to Q3. My post-edit check covers the symbols that actually changed. They are complementary, so C-011 becomes A+B, not A alone.

**12.** (round1-A per-point) "C-008: A — simplest grep-enforceable ban." and "C-014: A — positional args avoid unverified pipeline matching."
C-008: conceded in part. My interactive `maxFiles <= 5` allowance (FR-10, §2.1) has no consumer in B's own ideas: I-10 and N-3 use `status`, `files`, `callers`, `callees`. A permission with no user is surplus. Adopt A's "no primitive step names explore" test. Keep my routing block (I-03), because `codegraph_explore` is the one always-loaded tool (EVAL §3) and the model may call it unprompted; a grep over primitives cannot constrain that. C-014: conceded. FR-13 already escalates above 200 files, so positional args always fit and `--stdin` from a file is surplus, with its own unverified redirect matching.

## Updated assessment of A and C

**A.** A's Round 2 is a large honest correction: wildcard, MCP names in agents, validator edit, `sync`, `status` latency, zero-callers-DELETE, union-at-once (now with the VG-1 false-block evidence) are all withdrawn, and it found the reinstall-erases-switch fact against its own FR-16. What remains uniquely A's: the user-typed `/sc:graph` lifecycle owner, the telemetry blocker (U-002), the language-scope honesty (U-003), and the pre-edit step. Weaknesses that remain: A's Class A/D MCP default still waits on B1; A's `--diff` and "always pass `file`" rest on a CLI limitation that is not established (see New evidence 1); and its capability map is only a convention until a second access path exists. I take A for the scaffold's lifecycle command, telemetry, language scope and class table.

**C.** C conceded the right things (C-001, X-002, X-008, X-013, X-015, X-018, X-019). C's surviving contributions are real: the asymmetric cleanup rule (now adopted in my C-019 position), the edge-case table (S-010), the docs-only-diff rule (U-022), and the mutation-exclusion grep (FR-06), which is a good test form for my FR-04. C's W6 latency argument is the strongest point against me and is adopted above as an MCP-stage trigger. C's remaining positions that conflict with its own concessions: C-007 "first probe authoritative" and FR-07 per-run caching against its A-006 concession, and the tasklist risk note, which still changes tasklist output by index state.

## New evidence (not presented in Round 1)

1. **The EVAL CLI list is an abbreviated usage line, so absence from it is not proof.** EVAL line 96 lists `callers <symbol>` with no `--limit`, yet EVAL line 195 prints "Showing 20 of 23; pass --limit to widen." The list shows flags for `query` and `affected` and omits them for `callers`. So "CLI `node` has no file or `symbolsOnly` mode" (X-019; A's R2 point 3; my Round 1) and "CLI `callers` has no `file` argument" are inferences from absence, UNVERIFIED in both directions. C's "CLI works today" claim is equally unverified. B's design survives either way because it depends on neither; A's `--diff` "not v1-ready on the CLI" is also not established. Cheap closure: record `codegraph callers --help` and `codegraph node --help` output before Phase 3. This corrects the diff-analysis premise behind X-019.
2. **The VG-1 false-block applies to B's union stage too.** `sc-pr-submit-protocol/SKILL.md:203-204`: "Any non-zero gate blocks the push", and VG-1 is `uv run pytest <changed-area>` (`:206`). My FR-13 says the union "never removes tests", but NFR-08 measures recall and set size, not collection errors. A stale index (EVAL §4: no watcher without an MCP client) can return a test path that a rename or deletion removed. Add to the union stage: filter to paths present in `git ls-files`; a collection error caused only by an `affected`-only path is logged as advisory and the run falls back to `<changed-area>`; the backtest records the collection-error rate.
3. **B has an unresolved control question between per-subcommand allowlists and bundled scripts.** FR-04 pre-approves per-subcommand patterns, while N-1 and N-2 run codegraph from bundled scripts. If the model invokes a script, the approved pattern is the script path and the inner `codegraph` calls are not separately matched (Claude Code permission matching: UNVERIFIED here). The effective control is then the script body. `BASH_INSPECTION_POLICY.md` also forbids broad wrapper allowlists. Resolution: use exact-path script patterns for closed-Bash consumers (pr-submit, auggie-review, cleanup-audit), and make FR-04's grep test (subcommands outside the read-only set return 0 hits) run over the script bodies as well as the primitives.
4. **I-04's evidence base is narrower than stated** (see item 7): chunking applies only to 16-30 files or 1500-5000 lines (`:136-137`), and out-of-hunk findings become "context" rather than always vanishing (`:218`). This lowers I-04 and raises I-06 in B's own ranking.
5. **Cleanup-audit's drop reasons were partly wrong** (see item 4): a query-only step does not violate READ-ONLY, and the MCP constraint only forces the call into the orchestrator.

## Shared assumptions — changes only

| A-ID | New position | Reason |
|---|---|---|
| A-008 | REJECT (as a v1 gate input; was QUALIFY) | EVAL never ran `affected`, and a union can false-block VG-1 (`sc-pr-submit-protocol/SKILL.md:203-204`), including through B's own FR-13 (New evidence 2). Advisory-only until the NFR-08 backtest, extended with collection-error rate, passes |

All other positions are unchanged from Round 1 (A-001/002/009/010/011 ACCEPT; A-003/004/012 QUALIFY; A-005 ACCEPT as risk; A-006/007 REJECT). New evidence 1 adds a caveat to A-010 (version-pinned text), not a change.

## Updated per-point positions

| ID | Superior | Changed from Round 1? |
|---|---|---|
| S-001 | none | no |
| S-002 | none | no |
| S-003 | B+C | no |
| S-004 | A+B | no |
| S-005 | B | no |
| S-006 | A+B (A's coverage filtered by B's evidence classes; A trimmed its tail) | yes |
| S-007 | A+B | no |
| S-008 | A+B | no |
| S-009 | A+B | no |
| S-010 | A+C | no |
| S-011 | none | no |
| C-001 | A+B | no |
| C-002 | combination: B for v1, A's MCP classes after measurement | yes |
| C-003 | B | no |
| C-004 | B | no |
| C-005 | A+B | no |
| C-006 | A+B | no |
| C-007 | B | no |
| C-008 | A+B (A's no-primitive-names-explore test, B's routing block) | yes |
| C-009 | combination: B resolver, A's typed row and (file, startLine) match, C's drop-never-repair | yes |
| C-010 | B+C | no |
| C-011 | A+B | yes |
| C-012 | A+B (context first, shadow-mode exemption second) | yes |
| C-013 | B | no |
| C-014 | A | yes |
| C-015 | A+B | no |
| C-016 | A+B | no |
| C-017 | B | no |
| C-018 | B | no |
| C-019 | C (asymmetric rule, orchestrator-only, spike-gated) | yes |
| C-020 | B | no |
| C-021 | A (light edits; N-3 deferred) | yes |
| C-022 | B | no |
| C-023 | A | no |
| C-024 | A+B | no |
| C-025 | A+B (B's top five swaps I-04 for I-06) | no |
| C-026 | A+B+C | yes |
| C-027 | A+B | no |
| C-028 | B | no |
| C-029 | A+B | no |
| C-030 | B | no |
| C-031 | B+C | no |
| C-032 | A+B | no |
| C-033 | A+B | no |
| X-001 | B | no |
| X-002 | B | no |
| X-003 | B | no |
| X-004 | B+C | no |
| X-005 | A | no |
| X-006 | B+C | no |
| X-007 | B | no |
| X-008 | B | no |
| X-009 | A+B | no |
| X-010 | A+B | no |
| X-011 | A+B (gated on existing symbols; informational; FR-07 applies) | yes |
| X-012 | B+C | no |
| X-013 | B | no |
| X-014 | A+B | yes |
| X-015 | A+B | no |
| X-016 | A | yes |
| X-017 | B | no |
| X-018 | A | no |
| X-019 | B (both CLI claims unverified; B's design needs neither) | no |
| X-020 | none | no |
| X-021 | none | no |

### Variant C Rebuttal (haiku:backend)

<!-- verbatim: working/round2-C.md -->

# Round 2 — Advocate C (variant-3-haiku-backend), sequential rebuttal (last)

Notation: A/B/C = variants 1/2/3; EVAL = `research/codegraph-evaluation.md`. Re-read for this round: `sc-pr-submit-protocol/SKILL.md:4,201-210`, `sc-implement-protocol/SKILL.md:118-119`, `cli/install_skill.py:46-53`, `sc-auggie-review-protocol/SKILL.md:128-140,214-219`, EVAL lines 96, 188-195. New measurements of my own are marked [measured].

## Response to criticisms

**1.** (round1-A W5, round1-B W1-2) "C drifts into 1:1 Serena swaps... four checkable errors."
Already conceded in Round 1; nothing new reopens it. What survives the concession, and what I defend: I-04's diff-hunk→symbol derivation and I-05's severity-semantics change are genuinely "beyond"; I-02 shrinks to composing with the Phase-3 plan and its MCP-only outline path is dropped (X-019). B's R2 New evidence 1 downgrades X-019 from "C wrong" to "both directions UNVERIFIED" (EVAL line 96 is an abbreviated usage line; line 195 proves `callers` takes an undocumented `--limit`). That does not rehabilitate my claim — EVAL still does not document CLI file mode — but the diff-analysis fact-check verdict should read "unsupported", not "refuted".

**2.** (round1-A W7, round1-B W3) "C's FR-05 can narrow VG-1"; "the `git diff | codegraph affected` pipeline is unproven under scoped Bash."
Conceded then; my New evidence 1 makes the concession stronger, not weaker: my design's failure mode was worse than "narrow" — see below, a replaced list can false-block the push outright. On the pipeline: pr-submit `:4` enumerates `Bash(git *), Bash(uv *), Bash(make *), Bash(jq *)` (re-read), so compound-command matching is exactly the unverified surface A's Q-2 named. Positional args (A) it is: C-014 moves to A.

**3.** (round1-A W8, round1-B W4, both R2 files) "C-007 'first probe authoritative' and FR-07 per-run caching contradict C's own A-006 concession"; "the tasklist risk note still changes tasklist output by index state."
Full concession on both — these are the two places my artifact conflicts with my own concessions, and A and B were right to press them after I half-fixed them in Round 1.
Fix for the first: the latch must split. Availability and provenance (`version`, `index_root == realpath(worktree)`) latch once per run; freshness is re-checked (`status`) before any query batch that follows an in-run write; cached rows are invalidated by that re-check, not held for the run (EVAL §4: no watcher without an MCP client). This is B's R2 item-3 resolution and it is correct; my C-007 moves to B and A-006 moves to REJECT.
Fix for the second: the tasklist file is a committed artifact; an `affects_n_callers` field sourced from local index state makes its bytes machine-state-dependent even when tiering never reads it. The graph number moves to the run ledger and the reviewer package; the task file keeps at most a static flag derivable from the task text alone. X-010 and C-016 move to A+B.

**4.** (round1-A W9, R2-A C-6) "A seam with no output schema pushes every consumer to invent its own degraded keys. C's own §6 shows free-form keys such as `test-scope:codegraph_stale`, which is the drift that C's I-01 says it prevents."
Conceded. A is right and the hit lands on the exact property I marketed. Free-form keys make degradation observable but not parseable, and per-consumer key invention is six divergent copies of the thing I-01 exists to prevent. I accept A's merge as stated in R2-A: C's PROBE→CALL→VERIFY→DEGRADE block becomes the body of the seam skill; A's closed `graph:*` vocabulary becomes its output schema; B's resolver script becomes its executable part. C-005 → A+B+C. My residual point survives inside the merge: the sequence text is the only artifact an implementing engineer can follow step-by-step, which is why A asked for it as the skill body rather than as a ref table.

**5.** (R2-A C-4 note) "C's '~300 ms' reuses A's own unverified number (X-017)."
Conceded — a citation error of mine. My Round 1 weakness 4 argued against A's SessionStart hook using A's unverified figure. EVAL §5.5 timed `query` (290 ms) and `callers` (297 ms); `status` was never timed. The hook deferral stands on the unmeasured-cost and extra-failure-surface grounds, not on a number.

**6.** (round1-B W10, R2-B item 9) "B's CLI-only stance ignores the measured 3-15 ms vs 290-300 ms gap"; B's rebuttal: artifacts are computed once per run per symbol, not per hunk, ~9 s for 30 symbols inside NFR-01's 15 s.
Concession from me: my Round 1 W6 framed the cost as "per-hunk loops (reflect Step 1B.3 over ≥3 tasks × hunks)", which misdescribes B's design — B computes artifacts once per run and pastes them. The arithmetic is B's and it holds for its call counts. What survives is the trigger, which B has now adopted: log the actual query count per run, and when serial CLI queries pass roughly 100 (about 30 s), switch the orchestrator's capability to the listed MCP tool via the capability map. C-002 becomes that combination.

**7.** (round1-B W10, R2-B item 4) "'grep misses are not graph misses' is asserted, not measured."
Split answer. Epistemically: conceded, EVAL states neither direction (X-020 = none as a factual claim). Operationally: I keep the corroboration-only rule, and note that B has now adopted it as the substance of its own C-019 reversal — its R2 moves cleanup-audit to my asymmetric rule precisely because neither coverage direction is proven. A rule both opponents implement is not a slogan anymore.

**8.** (R2-B New evidence 3) Per-subcommand allowlists vs bundled scripts: "the effective control is then the script body."
Accepted, and it is the sharpest operational point in Round 2. Control must attach to the code that actually executes; a pre-approved script path whose body runs any codegraph subcommand is an allowlist laundering surface (and `BASH_INSPECTION_POLICY.md` already forbids broad wrapper allowlists). Adopted: exact-path script patterns for closed-Bash consumers, and the subcommand grep extended to script bodies. My FR-06 mutation-exclusion grep already covers them — see New evidence 4.

**9.** (R2-A New evidence 6) The span lookup must bind `(file, startLine == def_line)` else `unresolved`.
Accepted and folded into FR-03: this is a precise trigger for my `dropped: ambiguous` reason, which I had left prose. The two-unrelated-`install`-functions sample (EVAL §5.6) is exactly the case my drop-never-repair rule exists for; the binding rule makes the drop mechanical.

## Updated assessment of A and B

**A.** Round 2 was a genuine correction pass: six withdrawals plus two findings against its own design (reinstall erasure of its kill switch; its NFR-08 de-registration claim wrong for CLI-default consumers). Its unique survivors are real — the user-typed `/sc:graph` owner, telemetry on the CLI path (U-002), language-scope honesty (U-003), the pre-edit step. Its C-6 counter against my free-form keys is the single most useful hit A landed on me. Remaining weaknesses: Class A/D MCP defaults still wait on B1/Q-4, so A's richest access tier is undeliverable in v1; and the capability map is a convention until a second access path actually exists (B's point, which B's own R2 concession partially answers by adopting the map).

**B.** Still the most disciplined variant, and its Round 2 concessions are all real: FR-17 withdrawn, FR-01 reconciled with §8, the D-05 sentence dropped, my C-019 adopted with a sensible spike gate, and C-002 given a measurement trigger. B's bundled-scripts question is the best new operational finding of the round. Remaining gaps: no lifecycle owner until it accepted A's (now settled), and its probe/resolver content still needs a body of procedure text to live in — which is what my sequence block becomes in the merged seam.

## New evidence (not presented in Round 1)

1. **[measured] The `affected` union can false-block through two distinct pytest exit codes, only one of which B's R2 covered.** B's New evidence 2 handles the stale-index-missing-path case. I ran the other case: `pytest <existing-file-with-no-tests>` exits **5** (no tests collected); `pytest <missing-path>` exits **4**; both non-zero, and `sc-pr-submit-protocol/SKILL.md:203-204` says "Any non-zero gate blocks the push". So an `affected` entry that resolves to a *real* file collecting zero tests also blocks a correct push — `git ls-files` filtering does not catch it, because the file exists. Union-stage guard: pre-pass `pytest --collect-only -q`, drop paths collecting zero tests, fall back to `<changed-area>` on any collection error; the NFR-08 backtest must record both the collection-error and zero-collect rates.
2. **[measured] Rollback-by-deletion is operational fiction after install.** `install_skill.py:47-52` does `shutil.rmtree` + `copytree` under `force`, and `./update.sh` runs `superclaude install --force` (EVAL §2). Any local deletion of codegraph text — my NFR-05 mechanism — is erased on the next update. Rollback must be a source-level revert plus release; the runtime switch is the binary being off PATH (B's NFR-07 test). Partial concession on C-033: my claim holds only inside the dev loop, not as an operational rollback.
3. **Self-correction: my own §8 ambiguity row and I-04 say "pin with `file`", but `file` is documented only on the MCP tools** (EVAL §3: `codegraph_callers`/`codegraph_node` parameter tables); the CLI usage line (EVAL line 96) shows no `file` for either. With B's finding that the usage line is abbreviated, the correct state is: MCP-documented, CLI-UNVERIFIED. Closure is one command per subcommand: capture `codegraph callers --help` and `codegraph node --help` before Phase 3.
4. **[measured] My FR-06 grep already covers skill-bundled scripts.** Eight scripts live under `skills/*/scripts/` (cleanup-audit, crash-recovery ×2, implement, pr-submit ×4), all inside the grep path `src/superclaude/{skills,...}`. Adopting B's extend-the-grep-to-script-bodies costs nothing in my test; it is a wording change.
5. **[measured] Containment baseline is exactly zero.** `grep -i codegraph` over `src/superclaude/` returns 0 hits today. Every codegraph mention after adoption is attributable to the migration PRs by construction, so A's NFR-03 count needs no baseline archaeology and the drift check starts from a clean state.

## Shared assumptions — changes only

| A-ID | New position | Reason |
|---|---|---|
| A-006 | REJECT (was QUALIFY) | As stated ("one probe per run is enough") it is wrong for implement/pr-submit, which edit mid-run, and for CLI-only sessions where no watcher runs (EVAL §4). The split survives: availability latches once, freshness re-checks after in-run writes |

## Updated per-point positions

| ID | Superior | Changed? |
|---|---|---|
| S-001 | A | no |
| S-002 | none | no |
| S-003 | C | no |
| S-004 | A | no |
| S-005 | B | no |
| S-006 | B | no |
| S-007 | A+B (A's Layer 0 + B's confidence weight) | yes |
| S-008 | A+B | no |
| S-009 | A | no |
| S-010 | A+C (A's invariants + C's edge-case table) | yes |
| S-011 | B | no |
| C-001 | A+B | no |
| C-002 | combination: B for v1; A's MCP classes after measurement; logged query count (~100 serial calls) is the switch trigger | yes |
| C-003 | B | no |
| C-004 | B | no |
| C-005 | A+B+C (A's map and closed vocab, B's probe/resolver, C's sequence text as the skill body) | yes |
| C-006 | A+B | no |
| C-007 | B (never sync; availability latched, freshness re-checked after in-run writes) | yes |
| C-008 | A+B (A's no-primitive-step-names-explore grep, B's routing block against unprompted calls to the one always-listed tool) | yes |
| C-009 | A+B+C (typed resolution, B's resolver with the (file,startLine) binding, C's drop-never-repair) | yes |
| C-010 | B+C | no |
| C-011 | A+B (pre-edit as warning/Q3 input, post-edit on the actual diff) | yes |
| C-012 | B (context-only stage 1, shadow-mode counting stage 2) | no |
| C-013 | B | no |
| C-014 | A (positional args; FR-13 escalation makes `--stdin` surplus) | yes |
| C-015 | A | no |
| C-016 | A+B (graph numbers to ledger/reviewer package, not the committed task file) | yes |
| C-017 | B | no |
| C-018 | B | no |
| C-019 | C (asymmetric rule; B's orchestrator-only + spike gate accepted) | no |
| C-020 | B (defer; no MCP in v1 agents, candidates not precomputable) | yes |
| C-021 | A (light edits; N-3 deferred by B itself) | yes |
| C-022 | B | yes |
| C-023 | A | no |
| C-024 | B | no |
| C-025 | A+B | yes |
| C-026 | A+B+C (adds C's `sync` drop) | yes |
| C-027 | A+B (seam, /sc:impact, /sc:test-scope, /sc:graph; `/sc:ground` folds into the seam ref — a command wrapper added nothing once the skill owns the resolver and vocabulary) | yes |
| C-028 | A+B (A's modes and caps, B's prod/test split; `--diff` and `file`-pin need the CLI doc capture) | yes |
| C-029 | B | no |
| C-030 | B | no |
| C-031 | A+B+C (B's fixtures/backtest, A's containment count, C's mutation-exclusion grep over primitives and script bodies) | yes |
| C-032 | A+B | yes |
| C-033 | A+B (source-level revert/release + binary-absent runtime switch; delete-the-text holds only in the dev loop) | yes |
| X-001 | B | no |
| X-002 | B | no |
| X-003 | B | no |
| X-004 | B+C | no |
| X-005 | A | no |
| X-006 | B+C | no |
| X-007 | B | yes |
| X-008 | B (backtest extended with zero-collect and collection-error rates before any union) | no |
| X-009 | B (shadow mode, then enable on counts) | no |
| X-010 | A+B (tasklist artifact stays deterministic; risk data to the ledger) | yes |
| X-011 | A+B (gated on existing symbols, informational, FR-07 applies) | yes |
| X-012 | C | no |
| X-013 | B | no |
| X-014 | A+B | yes |
| X-015 | A | no |
| X-016 | A (status line only; B withdrew FR-17) | yes |
| X-017 | B | no |
| X-018 | A | no |
| X-019 | B (both CLI claims unverified; closure = `--help` capture before Phase 3) | no |
| X-020 | C as an operational rule (corroboration-only, now implemented by all three); none as a factual claim | no |
| X-021 | B | no |


## Round 2.5: Invariant Probe (summary)

The independent fault-finder file is `invariant-probe.md` (not reproduced here). It found 25 items: 6 ADDRESSED and 19 UNADDRESSED. The UNADDRESSED items are 1 HIGH, 10 MEDIUM and 8 LOW.
- HIGH + UNADDRESSED: **INV-001**. The freshness design depends on CLI `codegraph status` reporting pending files when no daemon runs. EVAL never observed this (EVAL §4 says the watcher runs only while an MCP client is connected; §5.4 and §5.7 saw "up to date" only right after indexing or with the daemon running).
- MEDIUM + UNADDRESSED: INV-004, INV-005, INV-009, INV-010, INV-011, INV-018, INV-019, INV-020, INV-023, INV-024.
- LOW + UNADDRESSED: INV-002, INV-003, INV-012, INV-013, INV-016, INV-017, INV-022, INV-025.

## Round 3: Final Arguments

Skipped: depth=standard runs 2 rounds plus the Round 2.5 probe.

## Scoring Matrix

The final positions are each advocate's Round 2 "Updated per-point positions" table. For promoted shared assumptions, the final position is the Round 1 verdict plus any Round 2 "changes only" row. A point is **agreed** when at least 2 of the 3 advocates name the same superior approach (or the same ACCEPT/REJECT/QUALIFY verdict for A-NNN). "A+B" and "B+A" count as the same approach. A differently worded combination with the same parts also counts as the same approach.

Confidence calibration (applied mechanically):
- **Unanimous** (3 of 3): 90. Raised to 100 only when the advocate of every variant left out of the winner made an explicit concession (a numbered Concession, "Conceded" text, or an explicit self-critique in a per-point reason). The source of each concession is cited. When no variant is left out (the winner is A+B+C, "none" or a shared verdict), the score stays at 90.
- **Majority** (2 of 3): 70. Add 5 when the dissenting position is a subset or superset of the winning combination (compatible dissent). Add 10 when the advocate of a left-out variant explicitly conceded. The cap is 89.
- **Split** (no two advocates agree): 50.

Abbreviations: R1/R2 = Round 1/2 file; "Conc n" = numbered concession; Adv = advocate.

| Diff Point | Level | Winner | Confidence | Evidence summary |
|---|---|---|---|---|
| S-001 | L1 | A | 70% | A, C: A's front matter records ground_truth and date. B: cosmetic ("none"). Dissent is not compatible |
| S-002 | L1 | none | 90% | All three: identical section order |
| S-003 | L2 | C | 85% | A, C: C's nine-vector table in §1. B: B+C (superset, +5). A conceded C's table is clearer (R1-A Conc 10, +10) |
| S-004 | L2 | A+B | 75% | A, B: A's 7 classes plus B's stance column. C: A (subset, +5) |
| S-005 | L2 | B | 90% | Unanimous: the M/P/A evidence classes feed the ranking |
| S-006 | L2 | A+B | 75% | A, B: A's coverage filtered by B's evidence classes, with A's tail trimmed. C: B (subset, +5) |
| S-007 | L1 | A+B | 90% | Unanimous in R2: A's Layer 0 plus B's confidence-weighted score (R2-A B-1, R2-C changed) |
| S-008 | L1 | A+B | 100% | Unanimous: tables with IDs. C self-critique: "my bullets do not" (R1-C per-point) |
| S-009 | L1 | A+B | 75% | A, B: one subsection per candidate with fields. C: A (subset, +5) |
| S-010 | L2 | A+C | 90% | Unanimous: A's invariants plus C's observed-behaviour → contract-response table |
| S-011 | L1 | none | 70% | A, B: counts do not indicate quality. C: B |
| C-001 | L2 | A+B | 100% | Unanimous: stay beyond the 1:1 swaps. C conceded the scope drift (R1-C Conc 1) |
| C-002 | L2 | B+A | 100% | Unanimous combination: B's CLI plus artifacts for v1, then A's MCP classes after measurement, triggered by a logged count of about 100 serial CLI calls. C conceded (R2-C #6) |
| C-003 | L2 | B | 90% | Unanimous: do not set `CODEGRAPH_MCP_TOOLS` in v1; measure the schema overhead first. A conceded (R1-A Conc 2); C gave no explicit concession |
| C-004 | L3 | B | 100% | Unanimous: one pattern per subcommand, never `Bash(codegraph *)` (EVAL §3 lists `install`/`upgrade`/`telemetry`). A Conc 1, C Conc 2 (R1) |
| C-005 | L2 | A+B+C | 75% | A, C: A's map and closed vocabulary, B's probe and resolver, C's sequence text as the skill body. B: A+B plus a capability-map ref (subset, +5) |
| C-006 | L3 | A+B | 100% | Unanimous: A's closed vocabulary plus B's provenance check and `parse_failed`. C: "my binary available/unavailable under-discriminates" (R1-C), R2-C #4 |
| C-007 | L3 | B | 100% | Unanimous: never sync; latch availability once, re-check freshness after in-run writes. A Conc 4 (R1), C R2 #3 |
| C-008 | L3 | A+B | 85% | B, C: A's grep ban plus B's routing block. A: A (subset, +5). C conceded "my maxFiles door adds surface" (R1-C per-point, +10) |
| C-009 | L3 | A+B+C | 90% | Unanimous: typed resolution, B's resolver with the (file, startLine == def_line) binding, C's drop-never-repair rule |
| C-010 | L2 | B+C | 100% | Unanimous: evidence-validator stays unchanged (`agents/evidence-validator.md:5,62-66`). A conceded (R1-A Conc 3; R2-A C-3) |
| C-011 | L2 | A+B | 90% | Unanimous: pre-edit impact as a warning and Q3 input (`sc-implement-protocol/SKILL.md:118-119`), plus a post-edit check on the actual diff |
| C-012 | L3 | A+B | 75% | A, B: context first, shadow-mode exemption second. C: B with the same staged content (compatible, +5) |
| C-013 | L3 | B | 85% | B, C: advisory, then backtest, then union. A: A+B (superset, +5). A fully conceded the immediate union (R2-A B-6, +10) |
| C-014 | L2 | A | 100% | Unanimous: positional args. B conceded (R2-B #12), C conceded (R2-C #2) |
| C-015 | L2 | A+B | 85% | A, B: A's Wave 1 callers plus B's pasted artifact. C: A (subset, +5). C self-critique "my split is thinner" (R1-C, +10) |
| C-016 | L2 | A+B | 85% | B, C: graph numbers go to the ledger and reviewer package, and the tasklist stays deterministic. A: A (subset, +5). C conceded (R2-C #3, +10) |
| C-017 | L3 | B | 100% | Unanimous: count distinct production caller symbols (runtime-surface table). A Conc 9, C Conc 4 (R1) |
| C-018 | L3 | B | 90% | Unanimous: no new reflect contract field in v1. A conceded (R1-A Conc 9); C gave no explicit concession |
| C-019 | L3 | C | 100% | Unanimous: asymmetric cleanup rule. A Conc 5 (R1), B R2 #4 |
| C-020 | L2 | B | 90% | Unanimous: defer reuse-auditor. A explicitly deferred I-11 (R2-A B-7); C changed its position without a concession text |
| C-021 | L2 | A | 90% | Unanimous: light onboarding edits, minus I-15. B deferred N-3 (R2-B #5); C gave no explicit concession |
| C-022 | L2 | B | 90% | Unanimous: no new hooks. A conceded (R1-A Conc 8) |
| C-023 | L3 | A | 100% | Unanimous: user-typed `/sc:graph init` with the nested-worktree refusal. B R2 #2; C "I left B2 unowned" (R1-C) |
| C-024 | L2 | A+B | 75% | A, B: prerequisite layer plus confidence weight. C: B (subset, +5) |
| C-025 | L2 | A+B | 100% | Unanimous. C self-critique: "my #2 (affected) was premature" (R1-C) |
| C-026 | L2 | A+B+C | 90% | Unanimous: the union of evidence-backed drops, including C's `sync` drop |
| C-027 | L2 | A+B | 100% | Unanimous: A's four slots with B's content. C: "/sc:ground … added nothing" once the seam owns the resolver (R2-C) |
| C-028 | L2 | A+B | 75% | A, C: A's modes and caps plus B's prod/test split; `--diff` and the `file` pin wait on the `--help` capture. B: B (subset, +5) |
| C-029 | L2 | split | 50% | A: A (callers tied to steps); B: A+B; C: B (widest caller set). Unresolved |
| C-030 | L3 | B | 90% | Unanimous: shown/total, one re-query at ≤100, CLI `file` argument UNVERIFIED |
| C-031 | L2 | split | 50% | A: A+B; B: B+C; C: A+B+C. Unresolved |
| C-032 | L2 | A+B | 90% | Unanimous: telemetry on the CLI path, no signal in Markdown repos, allowlist blast radius |
| C-033 | L2 | A+B | 100% | Unanimous: a release-level header switch plus a runtime switch where an absent binary means the native path. C conceded that deletion-rollback is fiction after install (R2-C NE2) |
| X-001 | L2 | B | 90% | Unanimous: no `mcp__codegraph__*` in read-only agents in v1. A conceded (R1-A Conc 2) |
| X-002 | L3 | B | 100% | Unanimous: never use the wildcard. A Conc 1, C Conc 2 (R1) |
| X-003 | L2 | B | 90% | Unanimous: defer the listing env. A conceded (R1-A Conc 2) |
| X-004 | L2 | B+C | 100% | Unanimous: the validator keeps `Read, Grep, Glob`. A Conc 3 (R1) |
| X-005 | L3 | A | 100% | Unanimous. B withdrew FR-17 (R2-B #2); C conceded B2 was unowned (R1-C) |
| X-006 | L3 | B+C | 100% | Unanimous: no primitive runs `sync` (EVAL §5.7). A Conc 4 (R1) |
| X-007 | L2 | B | 90% | Unanimous: no SessionStart hook. A Conc 8 (R1) |
| X-008 | L3 | B | 85% | B, C: the backtest, extended with zero-collect and collection-error rates, comes before any union. A: A+B (superset, +5). A conceded (R2-A B-6, +10) |
| X-009 | L3 | A+B | 75% | A, B: keep the downgrade; the verified exemption runs in shadow first. C: B (compatible, +5) |
| X-010 | L2 | A+B | 100% | Unanimous: the tasklist artifact stays deterministic. C conceded (R2-C #3) |
| X-011 | L2 | A+B | 75% | B, C: the workflow step is informational and gated on existing symbols. A: A (subset, +5) |
| X-012 | L3 | C | 85% | A, C: zero callers proves nothing. B: B+C (superset, +5). A conceded (R1-A Conc 5, +10) |
| X-013 | L3 | B | 100% | Unanimous: distinct production caller symbols. A Conc 9, C Conc 4 (R1) |
| X-014 | L3 | A+B | 85% | B, C: A's ban plus B's routing block. A: A (subset, +5). C conceded the maxFiles door (R1-C, +10) |
| X-015 | L1 | A+B | 85% | A, B: `SKILL.md:218` is Wave 1 at about 3k tokens. C: A (subset, +5). C Conc 5 (R1, +10) |
| X-016 | L2 | A | 90% | Unanimous: a read-only status line only. B conceded (R2-B #2) |
| X-017 | L2 | B | 100% | Unanimous: `status` latency is UNVERIFIED. A Conc 6 (R1), C R2 #5 |
| X-018 | L3 | A | 100% | Unanimous: `mcp__codegraph__codegraph_*` (EVAL §3). C Conc 6 (R1); B made no contrary claim |
| X-019 | L2 | B | 100% | Unanimous: both CLI claims are UNVERIFIED; close them with a `--help` capture. C Conc 7 (R1), A R2 NE3. Premise corrected by R2-B NE1 (the EVAL usage line is abbreviated) |
| X-020 | L2 | none | 75% | A, B: neither coverage claim is in EVAL. C: none as a factual claim, plus C's operational rule (compatible, +5) |
| X-021 | L1 | split | 50% | A: A; B: none; C: B. Unresolved. EVAL §5.5 fact: 20 of 23 rows shown, 2 production and 18 tests |
| A-004 | L2 | QUALIFY (shared) | 90% | All QUALIFY: one 24,913-character sample. Keep explore out of primitives; it can be reopened after a measurement |
| A-005 | L2 | QUALIFY (shared) | 75% | A, C: QUALIFY (sizes never measured; caps are estimates). B: "ACCEPT as risk" (compatible, +5) |
| A-006 | L3 | REJECT (shared) | 100% | All REJECT after R2. C moved from QUALIFY with an explicit concession (R2-C, "changes only"). The fix (split latch) is the target of INV-001 |
| A-007 | L3 | QUALIFY (shared) | 75% | A, C: QUALIFY (lists are floors). B: REJECT (same direction, compatible, +5) |
| A-012 | L2 | QUALIFY (shared) | 90% | All QUALIFY: the Skill-call cost is unmeasured; agents Read refs by installed path |

Winner tallies (a variant counts as a winner when it is part of the winning approach; "none", split and shared-verdict rows are excluded): 59 points have a variant winner. A wins 35 (59.3%), B wins 48 (81.4%), C wins 10 (16.9%).

## Convergence Assessment

- Scored points: S 11 + C 33 + X 21 + promoted A 5 (A-004, A-005, A-006, A-007, A-012) = **70**
- Agreed points: S/C/X **62 of 65** + promoted A **5 of 5** = **67 of 70**
- Convergence: 67 / 70 = **0.957 (95.7%)**
- Threshold: 75%. Met
- Independent recount: the orchestrator rebuilt the per-point agreement from the three Round 2 tables. S/C/X gives 62 of 65, the same as the Round 2.5 probe. The non-agreeing points are the same three: C-029, C-031, X-021. No difference. The probe did not score the promoted A-points; all 5 reach at least 2-of-3 agreement (A-004 3/3 QUALIFY, A-005 2/3 QUALIFY, A-006 3/3 REJECT, A-007 2/3 QUALIFY, A-012 3/3 QUALIFY).
- Taxonomy coverage gate: L1 has 7 agreed points (S-001, S-002, S-007, S-008, S-009, S-011, X-015). L2 has 37 agreed of 39. L3 has 23 agreed of 23, counting the A-points (7 + 37 + 23 = 67). Every level has at least one addressed point. **PASS**
- Invariant gate: `invariant-probe.md` lists **INV-001** as HIGH + UNADDRESSED. **FAIL**

> **BLOCKED_BY_INVARIANTS**: convergence 95.7% exceeds the 75% threshold, but 1 HIGH-severity invariant is UNADDRESSED: INV-001 (state_variables). The run-state consensus (C-007, A-006 REJECT) re-checks freshness with CLI `codegraph status` and treats pending files as stale. EVAL never observed `status` reporting pending files in a session with no daemon. If it does not, stale caller sets and `affected` lists pass as fresh, and re-Read does not catch counts or sets.

- Blocking IDs: **INV-001**
- Depth standard has no Round 3, so the debate cannot reopen to address INV-001. The run therefore force-selects the base by score (`base-selection.md`). INV-001 is carried into the merge as an **accepted risk with explicit mitigation**. `refactor-plan.md` Change 8 makes a sandbox experiment (E-1) a blocking prerequisite. No freshness-dependent idea may ship beyond advisory or shadow form until E-1 has run. E-1: with no daemon running, edit an indexed file, then record CLI `status` output. If `status` shows the pending list, the design stands. If it does not, any session with no live daemon is `graph:stale`.
- MEDIUM UNADDRESSED items (INV-004, 005, 009, 010, 011, 018, 019, 020, 023, 024) do not block convergence. Each one becomes a requirement, a gate or an explicit accepted risk in `refactor-plan.md`.
- Status: **BLOCKED_BY_INVARIANTS**
- Unresolved points: **C-029, C-031, X-021**. Resolutions are in `refactor-plan.md`: X-021 is a fact correction from EVAL §5.5; C-031 takes the union of the requirement emphases; C-029 keeps callers tied to adopted steps.
