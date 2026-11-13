# Tier 1 reflection card — pre-TASK-WF-analyzeCodegraph-20261111-193557-shadow15

mode: pre (UC-1) | target: tasklist vs spec (package archived under .dev/tasks/done/, post-hoc shadow measurement)

## Coverage matrix (Step 1B.0, two-pass)

Pass 1 (ID_REGEX `\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b`): **0 parsed IDs** — the spec labels requirements `R1`..`R7` (no hyphen); the tasklist labels `Task 1..3`. Pass 2 inference emitted 14 valid quote-pinned rows.

| ID | Quote (spec:line) | Matched task | Method | Source |
|---|---|---|---|---|
| INF-001 | "Exactly one codegraph readiness check per run, done once before the Discover step" (source.md:11) | Task 2 | containment | inferred |
| INF-002 | "use codegraph_search … before the existing Glob/Grep/Read step in Discover, Scan and Evaluate" (source.md:12) | Task 1, Task 2 | containment | inferred |
| INF-003 | "continues on Glob/Grep/Read, records the matching graph:* token … and never stops the run" (source.md:13) | Task 1, Task 2 | containment | inferred |
| INF-004 | "Frontmatter declares the codegraph MCP server the way reflect.md does (mcp-servers: [codegraph])" (source.md:14) | Task 1 | containment | inferred |
| INF-005 | "Every existing behaviour, flag, the Unattended mode section and every Boundary … is kept as written" (source.md:15) | Task 2 | containment | inferred |
| INF-006 | "No new src/superclaude/ read-instruction; the guide is named by its installed path" (source.md:16) | Task 1 | containment | inferred |
| INF-007 | "codegraph stays read-only: no codegraph init, index, sync, explore, context, no codegraph_node file mode without symbolsOnly:true, no wildcard allowlist" (source.md:17) | Task 1, Task 2 | containment (partial note) | inferred |
| INF-008 | "No allowed-tools is added: the file has none today" (source.md:22) | Task 1 | containment | inferred |
| INF-009 | "Keep index_state, checked_at and worktree_root for the whole run with no repeat" (source.md:27) | Task 2 | containment | inferred |
| INF-010 | "Report gets one line: Codegraph: index_state=<state>, checked_at=<UTC>; degraded: <graph:* tokens or none>" (source.md:31) | Task 2 | containment | inferred |
| INF-011 | Tool Coordination bullet naming status-once + six lookup tools (source.md:36) | Task 1 | containment | inferred |
| INF-012 | "New section ## Codegraph (optional) … under about 25 lines" with six rules (source.md:38-46) | Task 1 | containment | inferred |
| INF-013 | "Unattended mode and Boundaries … return-contract.yaml fields do not change" (source.md:48-49) | Task 2, Task 3 | containment | inferred |
| INF-014 | Validation checks (a)-(f): readiness/tools, fresh-only, frontmatter, no-src-path, sync, tests (source.md:53-60) | T1.AC1-3, T2.AC1-3, T3.AC1-3 | containment | inferred |

Summary: parsed=0, inferred=14 → `coverage_degraded: parsed-sparse` (Step 1B.2b; 8th consecutive run in this workspace). `coverage_pct: null` (0 parsed). `coverage_pct_union: 1.0` (14/14 matched). `unmapped_requirements_union: []`. `S_dev_density: 0.0` (union denominator). `implementation_coverage_pct: null` (kind-guard never fired — doc-only target).

## Findings (hypotheses)

- **H1 (coverage note, MINOR).** INF-007's clause "no codegraph_node file mode without symbolsOnly:true" appears nowhere in the tasklist as a prohibition; the tasklist pins `symbolsOnly:true` only as Scan-step usage (Task 2, "file outline with symbolsOnly:true"). Every file-mode use the tasklist names carries `symbolsOnly:true`, so the shipped result conforms, but a future edit adding node file-mode elsewhere would not be gated by any AC. Family: constraint without matching AC (shadow06/shadow10 recurrence).
- **H2 (plan accuracy, MINOR).** Spec ownership (source.md:5) says "the grep over tests/ found none that pins analyze.md content" — true at authoring time (first analyze.md pin landed in the same PR #511 as this package's execution, commit 7764bb623). Not a defect; recorded because Task 3's test-discovery step correctly found and ran `tests/skills/test_codegraph_adoption.py` (t3-test.log: 146 passed).
- **H3 (audit-vantage context, advisory).** Package is archived in done/ and its commit (7764bb623, PR #511) bundles four commands + agents, while the tasklist scope is analyze.md only. Bundling is coordinator-level merge action across sibling packages (issue #504), not executor drift; no before-state baseline exists for a strict byte-diff re-check (shadow08 corpus class — discount to advisory).
- **H4 (verified conformance).** Current HEAD analyze.md satisfies every tasklist AC mechanically: mcp-servers line 6; single readiness instruction line 30 ("exactly once per run"); per-step fresh-only clauses lines 32-34; Codegraph section lines 61-70 (10 lines < 25); no `src/superclaude` reference (grep exit 1); reflect.md parity (reflect.md:6 declares codegraph the same way).

## Structural signals

S_scope = 3 tasks; S_domains = 1 (docs/command file); S_dev_density = 0.0 (union). Pin: `--tier 2` (hard override §5.1); parsed-sparse pre-filter independently forces T2.
