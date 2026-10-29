# Refactoring Plan: Merge into Base (Variant B)

## Overview
- Base: Variant B, `variant-2-sonnet-analyzer.md` (sonnet:analyzer). Combined score 0.954; selected by the level-1 debate tiebreaker over A (0.921; margin 0.033 < 0.05). See `base-selection.md`.
- Incorporating strengths from: Variant A, `variant-1-opus-architect.md` (opus:architect), and Variant C, `variant-3-haiku-backend.md` (haiku:backend).
- Planned changes: **32**
- Risk level: **Medium** overall. Change 8 is High, because it gates the release of every freshness-dependent idea. Fourteen changes are Medium; the rest are Low.
- Debate status carried in: **BLOCKED_BY_INVARIANTS** (INV-001). Depth standard has no Round 3, so INV-001 is carried as an accepted risk with explicit mitigation. Change 8 turns it into a blocking prerequisite experiment, E-1.
- Evidence keys: confidence values are from the `debate-transcript.md` Scoring Matrix. "R1/R2-X" means an advocate file under `working/`; "INV-NNN" means `invariant-probe.md`; EVAL means `../../../research/codegraph-evaluation.md`.
- Section references to the base use B's numbering (§1 Summary … §9 Open questions). New merged idea IDs keep B's I-01..I-08 and add I-09..I-14 and P-01..P-03, as Change 28 defines.

## Planned Changes

### Change 1: Scope statement, 1:1 exclusion and ground-truth front matter (from Variant A)
- **Source**: Variant A, line 13 scope paragraph and YAML `ground_truth` field. Variant C line 4 "Planning only".
- **Target**: Base, front matter and the Notation paragraph (**insert**).
- **Content**: Add `ground_truth:` to the front matter. Add one scope sentence: the targets are guidance text, `tools:`/`allowed-tools:` lines, return-contract values and new primitives under `src/superclaude/{skills,commands,agents,core,hooks}`. Not in scope: the installer phase, the IronClaude Python CLI, and the 1:1 Serena SYM/REF swaps that Phase 3 owns (INV §4). Define INV on first use.
- **Rationale**: C-001 A+B (100%); S-001 A (70%). It closes B's one missed RC topic (K-1; `base-selection.md` RC table).
- **Risk**: Low. Additive text only.

### Change 2: Correct every EVAL fact error and overstatement in the base text (from Round 2 concessions)
- **Source**: R2-B #4, #6, #7, #9; R2-A B-2; R1-B Conc 1-2; R2-B NE1; diff-analysis X-017, X-019, X-020, X-021; A-003 (CONTRADICTED).
- **Target**: Base §1 bullet 4, §2.1 row 1, §3 I-04, §5 D-01 and D-05 (**replace**).
- **Content**:
  - X-021: replace "23 callers reported … the rest were test functions" with "EVAL §5.5 shows 20 of 23 rows: 2 production (`install_mcp_server`, `install`) and 18 tests; the 3 hidden rows were not inspected; one symbol only".
  - X-020: delete "Grep sees every static reference the graph sees". EVAL states neither coverage direction.
  - I-04: replace "a broken caller can never surface today" with "an out-of-hunk finding is downgraded to 'context' or dropped by severity (`sc-auggie-review-protocol/SKILL.md:218`); directory chunking applies only at 16-30 files or 1500-5000 diff lines (`:136-137`)".
  - §2.1: relabel "irrelevant at 30-60 calls" as an estimate: "arithmetic from EVAL §5.5, not measured".
  - X-017: keep "`status` timing UNVERIFIED" wherever latency is stated.
  - X-019: write "CLI `node` file/`symbolsOnly` mode and CLI `callers --file` are UNVERIFIED in both directions (the EVAL line-96 usage line is abbreviated; line 195 shows an undocumented `--limit`)". Closed by E-2 (Change 9).
  - A-003: D-01's reason now rests on size and noise against fixed wave budgets, not on auggie being free. When auggie is down, the fallback chain is Grep/Read.
- **Rationale**: Seed SC-4 "every capability claim traceable to EVAL". X-021 split (50%) is resolved as a fact correction. X-020 none (75%). X-019 B (100%). X-017 B (100%). This fixes base Correctness-1 (`base-selection.md`).
- **Risk**: Low. Wording only; no design change.

### Change 3: Nine-vector coverage table in §1 (from Variant C)
- **Source**: Variant C §1 "Nine-vector coverage map".
- **Target**: Base §1, appended after the bullets (**insert**). It replaces the "Vector coverage check" bullets in §4 (**replace**).
- **Content**: one row per seed vector, with columns adopted ideas / explicit drops / net position:

| Vector | Adopted (merged IDs) | Explicit drops |
|---|---|---|
| Token cost | I-03 routing and explore ban; FR-10 caps (40 rows, 6 KB); NFR-06 2K tokens | D-01 explore default; D-10 node file mode |
| Citation accuracy | I-01 provenance; I-02 resolver and typed rows | D-11 validator tools |
| Impact before edits | I-07 implement pre-edit warning and post-edit check; I-11 pre-fix impact; `/sc:impact` | D-02 PreToolUse hook |
| Review scoping (auggie-review, pr-submit, reflect) | I-04 auggie-review stages, plus pr-submit Wave 3 context; I-11 pr-submit Wave 4; I-05 reflect | D-14 graph chunking |
| Test selection (`affected`) | I-08 stage 0 advisory and stage 1 union; I-14 reflect UC-2 | D-26 cleanup-audit test runs |
| Troubleshoot Tier 1 | I-06 | D-09 producer enumeration |
| Planning (workflow, implement, tasklist) | I-13 workflow informational; I-07 implement; I-08 implement Q6 extras | D-06 tasklist; D-07 graph numbers in acceptance criteria or tiering |
| Reflection/audit (reflect, cleanup-audit, reuse-auditor) | I-05, I-14 reflect; I-12 cleanup-audit | D-08 reuse-auditor (deferred) |
| Onboarding (index-repo, explain, load) | I-10 explain one-hop and load status line | D-20 `/sc:load` rewrite; D-21 index-repo stats and `sc-structure-brief` |

- **Rationale**: S-003 C (85%). Seed constraint: cover all nine vectors (success criterion e).
- **Risk**: Low.

### Change 4: Normalize terminology to one state field and one closed vocabulary (from Variant A)
- **Source**: Variant A FR-03 (closed `graph:{…}` tokens) and the C-1 output (`index_state`).
- **Target**: Base §3 I-01, §6 N-1/N-2, FR-01/02/03/05/14/18, and all `degraded` examples (**replace**).
- **Content**: Rename `codegraph_state` and `graph_state` to `index_state`, with values `fresh|stale|not_initialized|foreign_index|absent|disabled|error`. Rename `codegraph:<x>` to `graph:<x>`. The closed vocabulary is `graph:{absent, disabled, unlisted, not_initialized, foreign_index, stale, version_mismatch, provenance_unproven, telemetry_on, empty, ambiguous, truncated, parse_failed, unresolved}`. Consumers record tokens inside their existing `degraded`/`degraded_components` lists and invent none of their own. C's free-form keys are not adopted.
- **Rationale**: C-006 A+B (100%). R2-C #4 concedes free-form keys. This fixes base Correctness-3 (`base-selection.md`).
- **Risk**: Low. Mechanical rename inside one document.

### Change 5: Access model: v1 rules and an explicit MCP-stage trigger (from Variants A and C)
- **Source**: Variant A §2.1 classes A-G; R2-B #9; R2-C #6; INV-025.
- **Target**: Base §2.1 (**replace** rows 1 and 5, **append** one row).
- **Content**: v1 stays as in B. The CLI runs in Bash-capable orchestrators. Agents get artifacts by path. No agent `tools:` line gains `mcp__codegraph__*`. Interactive commands get no explore allowance (Change 15). Add an "MCP stage (deferred)" row. It is eligible only when (1) the installer phase decides globally to set `CODEGRAPH_MCP_TOOLS` (one decision for every session, because listing hides unlisted explore, EVAL §3), (2) the always-loaded schema overhead has been measured (NFR-06), and (3) logged query counts show more than about 100 serial CLI calls per run in some orchestrator (NFR-01 logging). The per-run count is evidence for the global decision, not a per-orchestrator switch. Keep A's distinction between unrestricted-Bash orchestrators (troubleshoot, reflect, implement, workflow) and closed-Bash orchestrators (pr-submit, auggie-review, cleanup-audit) as a column.
- **Rationale**: C-002 B+A (100%); X-001 B (90%); X-003 B (90%); S-004 A+B (75%); INV-025 (LOW) is handled as a reworded trigger.
- **Risk**: Low.

### Change 6: Blocker table additions (from Variant A plus the probe)
- **Source**: Variant A §2.2 B2 and B5; `invariant-probe.md` INV-001, INV-019, INV-020; R2-B NE1.
- **Target**: Base §2.2 (**replace** the B2 owner, **append** B9-B12).
- **Content**:
  - B2: the owner becomes the user-typed `/sc:graph init` (Change 26 K-4). Remove `/sc:load --index`.
  - B9 telemetry: Bash CLI calls do not inherit the MCP entry's `CODEGRAPH_TELEMETRY=0`, and a binary already on PATH skips the installer's `telemetry off` path (EVAL §1, §7 steps 2-3). Owner: installer phase. Stance: Change 12.
  - B10 freshness without a daemon: CLI `status` pending detection without a daemon was never observed (INV-001). Owner: this phase, through E-1 (Change 8).
  - B11 CLI flag documentation gap: `callers`/`node` file pin, `symbolsOnly`, a machine-readable `status` (EVAL line 96 is abbreviated). Owner: this phase, through E-2 (Change 9).
  - B12 allowlist matching: `~` expansion, dual-surface script paths and env-prefixed commands under `Bash(codegraph <sub> *)` are UNVERIFIED (INV-019, INV-020). Owner: this phase, through E-3 (Change 9).
- **Rationale**: U-002 (High value); C-023 A (100%); X-005 A (100%); seed SC-4 "prerequisites called out as blockers".
- **Risk**: Medium. The new blockers widen the gating surface that later changes reference.

### Change 7: Restructure the probe skill into the shared seam `sc-graph-grounding` (from Variants A, B and C)
- **Source**: Variant A §6 C-1 (capability map, refs, output contract, header switch); base N-1 (probe, provenance, resolver script); Variant C §2 fenced contract (PROBE→CALL→VERIFY→DEGRADE); R2-B #1.
- **Target**: Base §6 N-1 and §3 I-01 (**restructure**; rename N-1 `sc-codegraph-probe` to `sc-graph-grounding`, since it now owns more than the probe).
- **Content**:
  - `SKILL.md` body: C's four-step sequence, amended by Change 10 (split latch) and Change 13 (resolver).
  - `refs/capability-map.md`: one row per capability (`callers | callees | impact | definition | search | affected_tests | status`) giving the CLI form, the MCP tool name `mcp__codegraph__codegraph_<tool>` (EVAL §3; not listed in v1), the native fallback, known gaps, the golden-fixture command, and a header with `tested_version: 1.6.2` and `status: enabled|disabled`.
  - `refs/citation-contract.md` and `refs/degraded-vocab.md` (Change 4).
  - `scripts/resolve-callsite.sh`.
  - Output schema: `access: cli|none`, `index_state`, `checked_at`, `version`, `pin_match`, `worktree_root`, `index_root|unknown`, `pending_files|unknown`, `daemon: live|absent|unknown`, `telemetry: on|off|unknown`, `degraded[]`.
  - Lookups name the installed `~/.claude/skills/sc-graph-grounding/…` first, then the project `.claude/skills/…`.
  - Agents Read `refs/citation-contract.md` by installed path. Orchestrators invoke the skill. The Skill-call cost stays an open measurement (A-012).
- **Rationale**: C-005 A+B+C (75%); C-006 A+B (100%); C-009 A+B+C (90%); X-018 A (100%); A-012 QUALIFY (90%); R2-A C-6; R2-C #4.
- **Risk**: Medium. It is the seam every consumer references, so a schema error propagates. Mitigation: the golden fixtures (NFR-04) cover the probe output.

### Change 8: Blocking prerequisite experiment E-1 and the freshness gate G-FRESH (from the invariant probe, INV-001)
- **Source**: `invariant-probe.md` INV-001 (HIGH, UNADDRESSED) and its closure note; EVAL §4, §5.4, §5.7.
- **Target**: Base, new §2.3 "Prerequisite experiments and gates", inserted after §2.2 (**insert**). It is also referenced from every gated idea in §3 and §4.
- **Content**:
  - **E-1** (P-01; effort S): in a sandbox worktree, with no MCP client and no daemon (confirm `.codegraph/daemon.sock` is absent and no `serve --mcp` process runs):
    1. `codegraph init --yes`.
    2. `codegraph status`; record the output.
    3. Append a function to an indexed file.
    4. Run CLI `codegraph status` at once, and again after 5 s; record both outputs verbatim.
    5. Repeat steps 3-4 with a daemon running.
    6. Repeat steps 3-4 with `CODEGRAPH_NO_DAEMON=1`.
    7. Record whether `.codegraph/daemon.sock` exists only while a daemon is live.
    8. Store the transcript as a golden fixture.
  - **Outcome A**: `status` lists pending files without a daemon. The split-latch design (Change 10) stands as written.
  - **Outcome B**: it does not. Every session without a detected live daemon gets `index_state: stale` for its whole run. Graph sets and counts in that session are leads only.
  - **G-FRESH**: an idea is *freshness-dependent* when its output is a set or count that changes a severity, a gate, a verdict or a finding class, or when it runs after an in-run write. Those ideas are I-04 stages 2-3, I-05 severity use, I-07 post-edit check, I-08 stage 1, I-12 and I-14. They may ship only in advisory or shadow form until E-1 has run and its outcome is written into the seam's `refs/capability-map.md`. Under Outcome B they stay advisory except in sessions with a detected live daemon.
  - Freshness-independent ideas (I-01..I-03, I-06, I-09, I-10, I-11, and I-04 stage 1 as labelled context) may ship before E-1. They must label rows with `index_state` and `checked_at`.
- **Rationale**: Debate status BLOCKED_BY_INVARIANTS. Blocking ID INV-001. At depth standard there is no Round 3, so this is the explicit mitigation. A-006 REJECT (100%) chose the split latch, and the split latch rests on this unverified `status` behaviour. Required by success criterion (h).
- **Risk**: **High**. Under Outcome B, five ideas stay advisory and the merged value drops. Mitigation: every gated idea already ships an advisory form, so no idea depends on E-1 to exist, only to gate.

### Change 9: Prerequisite checks E-2 and E-3, and resolver latency measurement E-4 (from Round 2 new evidence and the probe)
- **Source**: R2-B NE1; R2-C NE3; R2-A NE3; INV-011, INV-019, INV-020.
- **Target**: Base new §2.3, after E-1 (**insert**).
- **Content**:
  - **E-2** (P-02; S): capture `codegraph callers --help`, `callees --help`, `node --help`, `impact --help`, `status --help`, `affected --help` and `query --help` for v1.6.2 into the capability map. This closes X-019, the CLI `file` pin, `symbolsOnly` and a machine-readable `status`. Until then, CLI ambiguity is resolved by `query --json` matches filtered by file, and `/sc:impact --file` pinning stays off.
  - **E-3** (P-03; S): test Claude Code permission matching for (a) `Bash(codegraph callers *)` against `CODEGRAPH_TELEMETRY=0 codegraph callers x`, (b) `~/`-prefixed and absolute script paths for both dual-surface locations, (c) a positional-arg `codegraph affected a b`. Until E-3 passes, closed-Bash consumers call subcommands directly with per-subcommand patterns, and bundled scripts run only in unrestricted-Bash orchestrators.
  - **E-4**: time `resolve-callsite.sh` per row on the 500-file index and record it against NFR-01 (Change 31).
- **Rationale**: X-019 B (100%); C-028 A+B (75%, "`--diff` and the file pin wait on a `--help` capture"); INV-019 and INV-020 (MEDIUM) as gates; INV-011 (MEDIUM) as a measurement.
- **Risk**: Low. Read-only checks.

### Change 10: Run-state rule: split latch, debounce and persisted graph numbers (from Round 2 consensus)
- **Source**: R2-B #3; R2-C #3; R1-A Conc 4; INV-002, INV-003.
- **Target**: Base FR-01, FR-05 and §8 "Stale index" (**replace**).
- **Content**:
  - FR-01: availability, provenance and version are latched once per run.
  - `status` freshness is re-checked before every query batch that follows an in-run write. The re-check invalidates cached rows (C's FR-07 caching amended).
  - Pending files make the result `stale: true`, and its rows are leads only.
  - Debounce (INV-002): when a daemon is live and the re-check shows only files written in the last 3 s as pending, wait 3 s once and re-check once. If they are still pending, use `stale`.
  - Persistence (INV-003): any graph number written to a ledger or reviewer package carries `index_state` and `checked_at`. On `/sc:implement` resume it is treated as `stale` until it is re-checked.
  - No primitive runs `sync`.
- **Rationale**: C-007 B (100%); A-006 REJECT (100%); X-006 B+C (100%). INV-002 and INV-003 (LOW) become requirements.
- **Risk**: Medium. It depends on E-1 (Change 8).

### Change 11: Provenance hardening for version mismatch (from the probe, INV-004)
- **Source**: `invariant-probe.md` INV-004; base FR-03, NFR-04, NFR-09; A NFR-05.
- **Target**: Base FR-03 and NFR-09 (**append**).
- **Content**: When `codegraph --version` does not equal the pin, emit `graph:version_mismatch`. The provenance check is then treated as unproven, because it relies on the v1.6.2 warning text being absent: emit `graph:provenance_unproven`, and rows are leads only (no citations, sets or counts) for the run. When the pin changes, re-record the golden fixtures, including the nested-worktree warning, from the live binary in the E-1 sandbox, not from saved text.
- **Rationale**: INV-004 (MEDIUM) becomes a requirement. A-010 QUALIFY on version pinning.
- **Risk**: Low. It reduces graph use only on mismatched versions.

### Change 12: Telemetry handling on the CLI path (from Variant A, INV-005, INV-020)
- **Source**: Variant A §2.2 B5 and §8 "Telemetry"; R1-B Conc 3; INV-005, INV-020.
- **Target**: Base §2.2 B9 (Change 6), the probe output (Change 7), and new FR-22 (**insert**).
- **Content**: The probe records `codegraph telemetry status` (a read) and emits `graph:telemetry_on` without blocking. Primitives never run the `telemetry` subcommand and never prefix calls with `CODEGRAPH_TELEMETRY=0` (INV-020: the prefix may defeat per-subcommand matching). `/sc:graph status` shows the telemetry state and the opt-out the user can apply. Handoff to the installer phase: run `codegraph telemetry off` on every install path, including a binary already on PATH. **Accepted risk** until that handoff lands: on non-Coder hosts with a user-installed binary, CLI calls send anonymous telemetry. Mitigation: visible state plus a user pointer.
- **Rationale**: U-002 (High); C-032 A+B (90%). INV-005 and INV-020 (MEDIUM) are recorded as an explicit accepted risk with a named owner.
- **Risk**: Medium. The privacy exposure stays until the installer phase acts.

### Change 13: Citation resolver and contract rewrite (from Variants A and C plus the probe)
- **Source**: Variant A I-02 and FR-04 (typed `resolution`); R2-A NE6 (binding); Variant C FR-03 (drop-never-repair); INV-011, INV-012, INV-024.
- **Target**: Base §3 I-02, FR-06 and N-1 `resolve-callsite.sh` (**replace**).
- **Content**:
  - Every graph row carries `resolution: def-line|call-site-verified|unresolved`.
  - The resolver runs `codegraph query <caller> --json --limit 20` and keeps only the match where `file` equals the row's file and `startLine` equals the row's `def_line`. Otherwise the row is `unresolved`, and the run records the unresolved count (INV-012).
  - It Greps `\bCALLEE\s*\(` inside `startLine..endLine` and rejects matches inside string literals, comments or docstrings, and bare-name assignment or attribute-only matches (INV-024). With several matches, it cites each as a call-site candidate or cites none.
  - It Reads the line. A failing row is dropped, never repaired (C).
  - `def-line` rows are cited only as definitions.
  - Budget (INV-011): resolve only rows that will be cited, at most 5 per symbol and 20 per run. The remainder stays `unresolved` and contributes to counts only. E-4 records the timing.
  - Consumers whose cited rows do not pass the unchanged evidence-validator (auggie-review, reflect) may use `call-site-verified` rows as context only. Those rows cannot lift a downgrade or raise a severity.
  - evidence-validator stays byte-identical.
- **Rationale**: C-009 A+B+C (90%); C-010 B+C (100%); X-004 B+C (100%); A-002. INV-011 and INV-024 (MEDIUM) become requirements, INV-012 (LOW) a requirement.
- **Risk**: Medium. The resolver is the main accuracy mechanism, and a stricter match lowers recall. That direction is accepted as safe.

### Change 14: Allowlists, mutation-exclusion grep and containment count (from Variants B, C and A)
- **Source**: Base FR-04; Variant C FR-06; R2-B NE3; R2-C #8, NE4, NE5; Variant A NFR-03; INV-019.
- **Target**: Base FR-04 and §7 (**replace** FR-04, **insert** FR-23, NFR-10).
- **Content**:
  - FR-04: one `Bash(codegraph <sub> *)` pattern per read-only subcommand (`version`, `status`, `query`, `callers`, `callees`, `impact`, `affected`, `files`). Never `Bash(codegraph *)`.
  - Remove the `init`-in-`/sc:load` exception. Only the user-typed `/sc:graph init` may run `init` (Change 26).
  - Bundled scripts get exact-path patterns in the path form E-3 verifies.
  - FR-23: `grep -rnE 'codegraph (init|index|sync|uninit|unlock|upgrade|install|uninstall|telemetry)'` over `src/superclaude/{skills,commands,agents,core,hooks}` and every `skills/*/scripts/` body returns 0 hits. The single exception is `init` inside `commands/graph.md`.
  - NFR-10: containment count. Files mentioning `codegraph` stay within the listed set, from today's measured baseline of 0 (R2-C NE5).
- **Rationale**: C-004 B (100%); X-002 B (100%); C-031 split (50%), resolved as the union of the requirement emphases; INV-019 (MEDIUM) is gated through E-3.
- **Risk**: Low.

### Change 15: Explore policy and routing block (from Variants A and B; A-003 and A-004)
- **Source**: Variant A FR-05; base I-03 and FR-10; R2-B #12.
- **Target**: Base I-03, FR-10 and FR-21 (**replace**).
- **Content**: No `tools:` line and no step body in any primitive names `codegraph_explore`, `codegraph explore` or `codegraph context`. The grep test allows one hit: the "do not use" note in the capability map. Remove B's interactive `maxFiles ≤ 5` allowance. Keep the ≤12-line routing block in `core/CLAUDE.md`, because explore is the one always-listed tool and the model may call it unprompted (INV-007). The D-01 reason is reworded per Change 2. Explore stays out, and can be reopened after a measurement of `maxFiles` 1-5 single-symbol output, because the evidence is a single 24,913-character sample (A-004).
- **Rationale**: C-008 A+B (85%); X-014 A+B (85%); A-004 QUALIFY (90%); A-003 CONTRADICTED.
- **Risk**: Low.

### Change 16: Staged test selection through `/sc:test-scope` (from Variants A and C plus Round 2 evidence)
- **Source**: Base I-08 and FR-13; Variant A FR-07 (`selected ⊇ heuristic`); Variant C FR-05 (`source:` field, docs-only rule); R2-C NE1 [measured exit 4/5]; R2-B NE2; INV-017.
- **Target**: Base §3 I-08 and FR-13 (**replace**; I-08 splits into stage 0 and stage 1 in the ranked list).
- **Content**:
  - Inputs are positional args, filtered to paths that exist in the working tree (INV-017).
  - Stage 0 (advisory): print the `affected_tests` not covered by `<changed-area>`. The gate is unchanged.
  - Stage 1 (union, gated by G-FRESH and G-BACKTEST): `selected = heuristic ∪ affected`, always `⊇ heuristic`. Union paths are filtered by `git ls-files`. A `pytest --collect-only -q` pre-pass drops paths that collect zero tests (exit 5). Any collection error from an affected-only path falls back to `<changed-area>` and is logged. Above 200 files, escalate to VG-2.
  - Output: `selection_source: advisory|union|heuristic_only`. The escalation rule keys on source-file diffs, so a docs-only diff may honestly yield no affected tests (U-022).
  - `affected` stays CLI-only.
- **Rationale**: C-013 B (85%); X-008 B (85%); C-014 A (100%). R2-A B-6 and NE4 (false-block). INV-014 and INV-015 are ADDRESSED and preserved. INV-017 (LOW) becomes a requirement.
- **Risk**: Medium. The union stage touches a push gate, which is why it is double-gated.

### Change 17: Redesign the NFR-08 backtest so it can show benefit (from the probe, INV-023 and INV-016)
- **Source**: `invariant-probe.md` INV-023, INV-016; base NFR-08; R2-B NE2; R2-C NE1.
- **Target**: Base NFR-08 (**replace**) and §2.3 as gate **G-BACKTEST** (**insert**).
- **Content**:
  - Sample: at least 20 merged changes that touch indexed languages (python/yaml/liquid, EVAL §5.4). Markdown-only changes are excluded.
  - Each change is replayed against an index built at its parent commit, never today's index.
  - Benefit metric: the count of affected-only tests (in `affected`, not in `<changed-area>`) that fail on the change, or on a seeded mutation of each changed function.
  - Cost metrics: median affected-set ≤25 files, plus collection-error and zero-collect rates.
  - The union is enabled only when the benefit is greater than 0 and the costs are within the caps. Otherwise the stage stays advisory indefinitely.
  - The old recall criterion ("at least that of `<changed-area>`") is deleted, because a union always meets it.
- **Rationale**: INV-023 (MEDIUM) becomes a gate redesign; INV-016 (LOW) a requirement. U-010 (High).
- **Risk**: Medium. The backtest becomes costlier (index per parent commit). It runs once, offline.

### Change 18: Reflect parity: truncation and calibration rules (from the probe, INV-009 and INV-010)
- **Source**: Base I-05, FR-09 and FR-14; INV-009, INV-010; A-007 QUALIFY.
- **Target**: Base §3 I-05 and FR-09 (**append**), and §2.3 gate **G-SHADOW-REFLECT** (**insert**).
- **Content**:
  - Keep the distinct-production-caller-symbol count and add no new contract field.
  - Treat lists as floors (A-007).
  - When a list is `truncated` after the one re-query, or is `stale` or `provenance_unproven`, severity uses today's Grep-based reference count from chain 4b, and the graph only labels prod/test (INV-009). This supersedes C's stale→HIGH-as-MEDIUM rule (U-021).
  - G-SHADOW-REFLECT (INV-010): for the first 10 reflect runs on code changes, compute both today's count and the prod-only count, log both in `degraded_components`-adjacent audit lines, and keep today's severity. Switch only after a written review of the divergences. Add a change note on the calibration shift (base §8).
  - Also gated by G-FRESH.
- **Rationale**: C-017 B (100%); C-018 B (90%); X-013 B (100%). INV-009 and INV-010 (MEDIUM) become a requirement and a gate.
- **Risk**: Medium. Reflect is the heaviest consumer and its contract is CLI-parsed. Mitigated by "no new field" plus shadow mode.

### Change 19: auggie-review staging with a defined enable rule (from Round 2 consensus plus the probe)
- **Source**: Base I-04 and FR-12; Variant A I-09 (context only); R2-B #7; INV-013, INV-024.
- **Target**: Base §3 I-04 and FR-12 (**replace**; I-04 splits into stage 1 and stages 2-3 in the ranked list) and §2.3 gate **G-SHADOW-AUGGIE** (**insert**).
- **Content**:
  - Stage 1: `inputs/blast-radius.md`, produced by `/sc:impact --diff` (Change 26), is passed as context only. Today's out-of-hunk downgrade is unchanged.
  - Stage 2 (shadow): Read-verified `dependent-impact` rows are reported as ordinary context. The audit log counts the rows that `:218` would have downgraded.
  - Stage 3 (enable): only when G-FRESH passes and, over 20 reviews, at least 3 shadow hits were judged true by the PR author or reviewer and the false-positive rate is 20% or less (INV-013). Rows must be `call-site-verified` under Change 13's call-expression check (INV-024).
  - Lower I-04's V to 3 per R2-B #7.
- **Rationale**: C-012 A+B (75%); X-009 A+B (75%). INV-013 (LOW) and INV-024 (MEDIUM) become gate requirements.
- **Risk**: Medium. Stage 3 changes a validated rule. Mitigated by shadow counts and a numeric threshold.

### Change 20: Troubleshoot Tier 1: merged callers step (from Variant A)
- **Source**: Variant A I-04 (`search`/`node`/`callers` limit 10 in Wave 1 and Wave 1.6 Branch A); base I-06 and FR-15.
- **Target**: Base §3 I-06 (**replace** the mechanism column).
- **Content**: In Wave 1, `codegraph query <symbol> --json` and `codegraph callers <symbol> --limit 20` for the failing component are written to `tier1-callers.md` (cap 40 rows, 6 KB) and pasted into the Wave 1.6 Branch A briefs (`:286`), within the Wave 1 budget of about 3k tokens at `SKILL.md:218`. The 2k figure at `:256` is Wave 1.5, not Tier 1. Rows are leads with typed `resolution`. The exit criteria accept the Glob/Grep fallback (`:194`, `:216`).
- **Rationale**: C-015 A+B (85%); X-015 A+B (85%) is a citation fix.
- **Risk**: Low.

### Change 21: Implement: pre-edit warning plus post-edit check (from Variant A)
- **Source**: Variant A I-05; R2-A NE5; base I-07 and FR-16.
- **Target**: Base §3 I-07 and FR-16 (**replace**).
- **Content**:
  - Pre-edit: for tasks that rename, delete or change the signature of an existing symbol, Q1 runs `/sc:impact <symbol>` (cap 10 files). The result is a warning to the implementer and an input to the Q3 package and the ledger. It never widens Q1 edits (`sc-implement-protocol/SKILL.md:118-119` "Implement only that task").
  - Post-edit: `untouched_dependents` on the actual diff (at most 20 rows, context only). It is gated by G-FRESH, because it runs after an in-run write.
- **Rationale**: C-011 A+B (90%).
- **Risk**: Medium. QA scope creep. Mitigated by the context-only rule.

### Change 22: Pre-fix impact in remediation chains (from Variant A)
- **Source**: Variant A I-10, U-006.
- **Target**: Base §3, new idea **I-11** (**insert**).
- **Content**: pr-submit Wave 4 (at ordinal ≥2, before applying edits, `sc-pr-submit-protocol/SKILL.md:194`) and the troubleshoot `--fix` handoff attach the `/sc:impact` report for the symbols the fix touches, as a warning only. Value M; effort S; risk L; fallback: Grep for the symbol name, `graph:absent`.
- **Rationale**: U-006 (Medium); C-028 A+B (75%) for A's `/sc:impact` callers.
- **Risk**: Low.

### Change 23: Cleanup-audit: the asymmetric rule replaces the base drop (from Variant C)
- **Source**: Variant C I-07; R2-B #4, NE5; R1-A Conc 5.
- **Target**: Base §5 D-05 (**replace** with idea **I-12** in §3) and FR-07 (**append** the example).
- **Content**: Orchestrator only (`:86`). Nonzero graph callers move a DELETE candidate to REVIEW. Zero callers prove nothing. The DELETE gate stays the grep proof (`:75`). Gated by **G-SPIKE**: a one-hour spike must show that the upgrade fires on at least one candidate where grep did not. Also G-FRESH. Value L-M; effort S; risk L.
- **Rationale**: C-019 C (100%); X-012 C (85%).
- **Risk**: Low. The rule can only add conservatism.

### Change 24: Workflow informational step; the tasklist stays dropped (from Variant A, with the X-010 resolution)
- **Source**: Variant A I-13; R2-B X-011; R2-C #3.
- **Target**: Base §5 D-07 (**replace**: narrowed) and §3, new idea **I-13** (**insert**). D-06 is kept, with C's concession added to its reason.
- **Content**: workflow Wave 1 runs `codegraph impact <s> --depth 2` only when the source names symbols that already exist. The counts go into the plan's notes, with `index_state` and `checked_at`. They never go into acceptance criteria or tiering. The tasklist file keeps no graph-derived field, because its bytes must not depend on machine state.
- **Rationale**: X-011 A+B (75%); X-010 A+B (100%); C-016 A+B (85%).
- **Risk**: Low.

### Change 25: Onboarding light edits; withdraw `/sc:load --index` and defer `sc-structure-brief` (from Variant A)
- **Source**: Variant A I-14, I-16; R2-B #2, #5; R2-A B-7.
- **Target**: Base §3 I-09 and I-10 (**replace**), FR-17 and FR-18 (**delete**), and §6 N-3 (**move to drops**).
- **Content**:
  - I-09 becomes the `/sc:graph` lifecycle owner (Change 26 K-4).
  - I-10 becomes two light edits. (1) `/sc:explain` one-hop: definition, callers and callees, limit 10, on CLI `query --json`/`callers`/`callees` rows that are re-Read. (2) `/sc:load` one read-only status line (`index_state`, plus a pointer to `/sc:graph init`).
  - The index-repo graph stats (A I-15) and N-3 are dropped (Change 29).
- **Rationale**: C-021 A (90%); X-016 A (90%); X-005 A (100%).
- **Risk**: Low.

### Change 26: Candidate set restructured to four, each with callers (from Variants A and B)
- **Source**: Variant A §6 C-1..C-4; base §6 N-1/N-2; Variant C C-3 fields; R2-C (C-027); INV-022.
- **Target**: Base §6 (**restructure**).
- **Content**:
  - **K-1 `sc-graph-grounding`** (skill, delegate-only; Change 7). Callers: sc-troubleshoot-protocol (Wave 0, Wave 1, Wave 1.6), sc-reflect-protocol (Wave 0, 1B.3, chain 4/4b, UC-2), sc-implement-protocol (Wave 0, Q1, post-edit), sc-pr-submit-protocol (before VG-1, Wave 4), sc-auggie-review-protocol (Wave 1), sc-cleanup-audit-protocol (orchestrator, behind G-SPIKE), sc-workflow-protocol (Wave 1), `/sc:impact`, `/sc:test-scope`, `/sc:graph`, `/sc:explain`, `/sc:load`. Agents (reflect-reviewer, troubleshoot-analyst) read artifacts and `refs/citation-contract.md` by installed path.
  - **K-2 `/sc:impact`** (command). Interface: `<symbol> | --file <path> | --diff [<base>]`, `[--depth 1-3, default 2] [--limit N, default 20, max 100] [--tests] [--output <dir>]`. Output: B's blast-radius fields (`changed_symbols[]` with `mapped_by: hunk|name`, labelled as IronClaude-side mapping; `dependents.prod[]`, `dependents.test[]` with `resolution`; `truncated{shown/total}`; `ambiguous[]`; `unmapped_files[]`; `affected_tests[]|unknown` with `--tests`; `index_state`; `degraded[]`). `--diff` maps hunks through `query --json` spans. The `--file` pin waits on E-2. Callers: sc-implement-protocol Q1 and post-edit, sc-pr-submit-protocol Wave 4, the sc-troubleshoot-protocol `--fix` handoff, sc-auggie-review-protocol Wave 1, sc-reflect-protocol 1B.3 and 4b, sc-workflow-protocol Wave 1, operators. It absorbs base N-2 `sc-blast-radius` and `/sc:blast-radius`.
  - **K-3 `/sc:test-scope`** (command; Change 16). Output: `changed_files[]`, `heuristic_tests[]`, `affected_tests[]|unknown`, `delta[]`, `selected[]` (stage 1 only), `filtered[]` (with reasons `not_tracked|zero_collect|collect_error`), `selection_source`, `pytest_args`, `index_state`, `degraded[]`. Callers: sc-pr-submit-protocol VG-1, sc-implement-protocol Q6 extras, sc-reflect-protocol UC-2 (I-14), `/sc:impact --tests`.
  - **K-4 `/sc:graph [status|init]`** (command). Variant A's C-4 minus `sync` (INV-022, X-006). `init` runs only when the user typed it. It refuses in a nested worktree unless `--worktree-local` is passed, which runs `init -i` (EVAL §5.8). Output: `cli_version`, `pin_match`, `index_state`, `worktree_relation`, `files/nodes/edges`, `pending[]|unknown`, `daemon`, `telemetry`, `next_action`. Callers: users; referenced from the `/sc:load` status line and from the seam's `graph:not_initialized` message.
  - All four use installed paths with the dual surface and contain no `src/superclaude/` path.
- **Rationale**: C-027 A+B (100%); C-028 A+B (75%); C-023 A (100%). C-029 split (50%) is resolved by A's rule, "callers tied to concrete steps": each listed caller maps to an adopted ranked idea, and index-repo is removed because its idea is dropped. This meets success criterion (d) (3-5 candidates with callers).
- **Risk**: Medium. Four new primitives, each needing tests.

### Change 27: Rollback and kill switches that survive updates (from Variants A and B plus the probe)
- **Source**: Variant A FR-16; base NFR-07 and §8 "Rollback"; R2-A NE1, NE2; R2-C NE2; INV-018.
- **Target**: Base §8 "Rollback" (**replace**) and new FR-24 (**insert**).
- **Content**: There are three switches.
  1. Release level: the capability-map header `status: disabled`, applied as a source edit plus a release, because `superclaude install --force` erases local edits (`install_skill.py:47-52`).
  2. Runtime: `codegraph` absent from PATH means the native path (NFR-07). This one is undone by `./update.sh` (EVAL §7 steps 2-3).
  3. User level, survives updates: the probe reads env `IRONCLAUDE_CODEGRAPH=off` with `printenv` and emits `graph:disabled` (INV-018). `/sc:graph status` documents it.
  Delete A's claim that MCP de-registration disables CLI-default consumers. Delete C's "delete the text" rollback as an operational mechanism.
- **Rationale**: C-033 A+B (100%). INV-018 (MEDIUM) becomes a requirement.
- **Risk**: Medium. It adds an env name that must stay stable.

### Change 28: One unified ranked list with single S/M/L effort (from Variants A and B)
- **Source**: Variant A §4 Layer 0; base §4 `V × C ÷ E` (M=1.0, P=0.6, P-minus=0.3; E: S=1, M=2, L=4). Tie order: base rule (measured hazard, then measured mechanism, then lower risk), then A's frequency, then the base's prior rank.
- **Target**: Base §4 (**replace**). Every §3 row gets a single Effort S/M/L.
- **Content**: Fix base I-07, which is labelled Class P but scored with C=0.3, and normalize "S-M" and "S advisory, M union" to single values. The list:

| Rank | ID | Idea | Targets | Value | Effort | Risk | Score | Gates |
|---|---|---|---|---|---|---|---|---|
| 1 | P-01 | E-1 freshness experiment | sandbox only | H (unblocks G-FRESH) | S | L | Layer 0 | blocking |
| 2 | P-02 | E-2 CLI `--help` capture | seam capability map | M | S | L | Layer 0 | none |
| 3 | P-03 | E-3 allowlist matching check | closed-Bash allowlists | M | S | L | Layer 0 | none |
| 4 | I-01 | `sc-graph-grounding` seam | new skill; Step-0 line in each consumer | H | M | L | Layer 0 | none |
| 5 | I-02 | Resolver and citation contract | seam refs/scripts; reflect `:42`; troubleshoot Wave 5; auggie-review `:216-219` | H | M | M | Layer 0 | E-4 timing |
| 6 | I-03 | Allowlists, routing block, explore ban | `core/CLAUDE.md`; consumer allowlist lines | H | S | L | Layer 0 | E-3 for scripts |
| 7 | I-05 | Reflect prod-only parity | sc-reflect-protocol 1B.3, 4/4b; runtime-surface ref | H | M | M | 4×0.6/2 = 1.2 | G-FRESH, G-SHADOW-REFLECT |
| 8 | I-11 | Pre-fix impact in remediation chains | sc-pr-submit-protocol Wave 4; troubleshoot `--fix` handoff | M | S | L | 2×0.6/1 = 1.2 | none (warning) |
| 9 | I-09 | `/sc:graph` lifecycle owner | new `commands/graph.md` | M | S | M | 2×0.6/1 = 1.2 | none |
| 10 | I-06 | Troubleshoot Tier 1 callers | sc-troubleshoot-protocol Wave 1, 1.6 Branch A; `commands/troubleshoot.md` | H | M | L | 3×0.6/2 = 0.9 | none (leads) |
| 11 | I-04 s1 | auggie-review blast radius as context | sc-auggie-review-protocol Wave 1; pr-submit Wave 3 context | M | M | M | 3×0.6/2 = 0.9 | none (context) |
| 12 | I-07 | Implement pre-edit warning and post-edit check | sc-implement-protocol Q1-Q3, `refs/qa.md` | H | M | M | 3×0.6/2 = 0.9 | post-edit: G-FRESH |
| 13 | I-08 s0 | `affected` advisory delta | sc-pr-submit-protocol VG-1; implement Q6 extras | M | S | L | 3×0.3/1 = 0.9 | none (advisory) |
| 14 | I-10 | Explain one-hop and load status line | `commands/explain.md`, `commands/load.md` | M | S | L | 2×0.3/1 = 0.6 | none |
| 15 | I-12 | Cleanup-audit asymmetric corroboration | sc-cleanup-audit-protocol `:75,:83,:86` | L-M | S | L | 2×0.3/1 = 0.6 | G-SPIKE, G-FRESH |
| 16 | I-14 | Reflect UC-2 regression evidence (advisory) | sc-reflect-protocol UC-2 | M | S | L | 2×0.3/1 = 0.6 | G-FRESH |
| 17 | I-04 s2-3 | `dependent-impact` shadow, then exemption | sc-auggie-review-protocol Wave 3 `:218` | M | M | M | 3×0.3/2 = 0.45 | G-FRESH, G-SHADOW-AUGGIE |
| 18 | I-08 s1 | `changed-area ∪ affected` in VG-1 | sc-pr-submit-protocol VG-1 | M | M | M | 3×0.3/2 = 0.45 | G-FRESH, G-BACKTEST |
| 19 | I-13 | Workflow informational impact | sc-workflow-protocol Wave 1 | M | M | L | 2×0.3/2 = 0.3 | existing symbols only |

- **Rationale**: S-007 A+B (90%); C-024 A+B (75%); C-025 A+B (100%); R2-A B-1; R2-B #7 (I-06 above I-04). Success criteria (a) and (b).
- **Risk**: Medium. Ranks drive the Phase 3 sequencing.

### Change 29: Merged drops table with reasons (from Variants A, B and C)
- **Source**: Base §5 D-01..D-12; Variant A §5 D-04, D-06, D-09..D-12; Variant C §5 bullets; Round 2 deferrals.
- **Target**: Base §5 (**replace**).
- **Content**:
  - D-01 explore as a default step (reason per Change 2/15).
  - D-02 PreToolUse impact hook (kept).
  - D-03 SessionStart hook, init or status, including A I-17. Reason: `status` latency is unmeasured, it adds hook failure surface, and B's earlier "adds nothing" was a value judgement (R1-B Conc 5).
  - D-04 `prompt-hook`/`codegraph install` (kept).
  - D-05 zero graph callers as DELETE proof or evidence (A D-06, C §5; X-012). This replaces the base cleanup-audit drop.
  - D-06 tasklist graph input (kept; add C's concession).
  - D-07 graph numbers in workflow acceptance criteria or tiering (narrowed per Change 24).
  - D-08 reuse-auditor co-caller search, liveness check and codegraph fallback tier. Deferred: agents have no MCP in v1, and agent-found candidates cannot be precomputed (C-020 B, 90%). Re-propose after the MCP stage (Change 5).
  - D-09 producer enumeration (kept).
  - D-10 node file mode as Read (kept).
  - D-11 codegraph tools in the evidence-validator, and any edit to it (C-010).
  - D-12 SQLite/data-flow/Cypher (kept).
  - D-13 `codegraph context` for planning (unmeasured; A D-04).
  - D-14 graph-based review chunking (no clusters; A D-09).
  - D-15 replacing reflect LSP diagnostics (A D-10).
  - D-16 codegraph tools in the freshness matchers (A D-11).
  - D-17 `graph-scout` subagent (A D-12).
  - D-18 any primitive running `sync`, including `/sc:graph sync` (EVAL §5.7; X-006; INV-022).
  - D-19 `/sc:load --index` and any `init` outside the user-typed `/sc:graph init` (X-005).
  - D-20 rewriting `/sc:load` around codegraph (C).
  - D-21 `sc-structure-brief` (deferred, R2-B #5) and index-repo graph stats (A I-15; Glob already gives structure, and the 58K→3K figure is unmeasured).
  - D-22 the 1:1 Serena swaps as P3 ideas (C I-02, I-04, I-05, I-06; C-001; Phase 3 owns them).
  - D-23 `/sc:ground` (folded into the seam; R2-C C-027).
  - D-24 private per-skill impact/test-scope scripts (C).
  - D-25 graph routes for `sc-recommend` (C).
  - D-26 cleanup-audit test runs (C; READ-ONLY charter).
  - D-27 interactive explore with `maxFiles ≤ 5` (no consumer; R2-B #12).
  - D-28 `CODEGRAPH_MCP_TOOLS` and agent MCP names in v1 (deferred with the Change 5 trigger).
  - D-29 C's stale→HIGH-as-MEDIUM demotion (superseded by Change 18).
- **Rationale**: C-026 A+B+C (90%). Success criterion (c).
- **Risk**: Low.

### Change 30: Risks, invariants and the edge-case table (from Variants A and C plus the probe LOW items)
- **Source**: Variant A §8 INV-1..INV-4 and the "Markdown-heavy repos" bullet (U-003); Variant C §8 edge-case table; `invariant-probe.md` LOW items.
- **Target**: Base §8 (**append**).
- **Content**:
  - A's four invariants.
  - C's observed-behaviour → contract-response table, with rows corrected to the merged rules: nested worktree → `foreign_index`; "first probe authoritative" → split latch; the CLI vs MCP latency row → the Change 5 trigger.
  - U-003: IronClaude primitives are Markdown, which the graph does not index. The payoff is in code repos.
  - Accepted LOW risks with mitigation: INV-012 (unbounded unresolved count, which is recorded), INV-016 (handled in Change 17), INV-017 (handled in Change 16), INV-022 (handled in Change 26), INV-025 (handled in Change 5), INV-002 and INV-003 (Change 10), INV-013 (Change 19).
- **Rationale**: S-010 A+C (90%); U-003 (High); C-032 A+B (90%).
- **Risk**: Low.

### Change 31: Requirements consolidation (from Variants A and C; C-031 resolution)
- **Source**: Variant A NFR-04 (mirror parity) and NFR-05 (version honesty); Variant C FR-07 (idempotency); base NFR-01, NFR-02, NFR-06; INV-011.
- **Target**: Base §7 (**append** NFR-11..NFR-13, **replace** NFR-01).
- **Content**:
  - NFR-01 restated per phase: probe p95 under 1 s; graph queries for 30 symbols under 15 s; resolver cost tracked separately against the Change 13 budget. Every run logs its actual serial query count. `status` timing stays UNVERIFIED until it is measured.
  - NFR-11 mirror parity with `plugins/superclaude/` (`make verify-sync`).
  - NFR-12 version honesty (Change 11).
  - NFR-13 idempotency: graph results are cached per run, and the cache is invalidated by the Change 10 re-check.
  - Keep NFR-02 BASH-policy batching only for known-target queries. Resolver calls depend on earlier output and are not batched (INV-011).
- **Rationale**: C-031 split (50%) is resolved as the union of the three emphases: B's fixtures and backtest, A's containment count and mirror parity, C's mutation grep and idempotency. All three advocates listed these in their Round 2 positions.
- **Risk**: Low.

### Change 32: Open questions update
- **Source**: Base §9; Variant A §9 Q-4, Q-5, Q-8; Round 2 outcomes.
- **Target**: Base §9 (**replace**).
- **Content**:
  - Closed by the debate: Q1 (deferred, with the Change 5 trigger) and the "probe skill vs copied ref" question (agents Read the seam's refs by path; A-012).
  - Kept: `affected` quality (now the redesigned G-BACKTEST), `status` format (E-2), daemon-on-init (E-1, step 5), non-Python hunk mapping, pin ownership.
  - Added: the Skill-call cost measurement (A-012); whether `.codegraph/daemon.sock` presence reliably means a live daemon (E-1); the installer handoff for `telemetry off` (Change 12); A Q-4 (MCP availability to foreground agents, relevant once the MCP stage opens); A Q-8 (`affected --depth` default 1 or 2, measured in G-BACKTEST).
- **Rationale**: A-012 QUALIFY (90%); C-002 B+A (100%).
- **Risk**: Low.

## Seed-brief Success Criteria and orchestrator requirements: compliance map

| Requirement | Satisfied by |
|---|---|
| (a) every idea has target primitive(s), value, effort S/M/L and risk | Change 28 table (single S/M/L); Changes 22-25 rows; Change 4 terminology |
| (b) one ranked list | Change 28 (Layer 0, then confidence-weighted, in one table) |
| (c) explicit drops with reasons | Change 29 (D-01..D-29) |
| (d) 3-5 candidates with callers | Change 26 (K-1..K-4, each with callers) |
| (e) all nine vectors covered | Change 3 table; Changes 16, 19-25 |
| (f) every Round 2 concession reflected | Concession ledger below |
| (g) every diff-analysis contradiction against EVAL fixed | EVAL-fix ledger below |
| (h) invariant HIGH and MEDIUM UNADDRESSED items handled | Invariant ledger below; INV-001 is the blocking E-1 (Change 8) |

### Concession ledger (Round 2 and carried-forward Round 1 concessions → change)

| Advocate | Concession | Change |
|---|---|---|
| A | R2 B-1: the formula lacks a confidence term | 28 |
| A | R2 B-2: the span bound appears only in the mechanism column; B's script is the better delivery | 13 |
| A | R1 Conc 1 / R2 B-3: wildcard `Bash(codegraph *)` | 14 |
| A | R1 Conc 2: MCP names in agents before listing | 5, 29 D-28 |
| A | R1 Conc 3 / R2 C-3: evidence-validator in Class D and its text edit | 13, 29 D-11 |
| A | R1 Conc 4: "try one `sync`" | 10, 29 D-18 |
| A | R1 Conc 5: zero callers as DELETE evidence | 23, 29 D-05 |
| A | R1 Conc 6: `status` ~300 ms | 2, 31 |
| A | R1 Conc 7: empty-results list sourced beyond EVAL §4 | 30 (marked UNVERIFIED reasoning) |
| A | R1 Conc 8 / R2 C-4: SessionStart hook | 29 D-03 |
| A | R1 Conc 9: reflect severity count and contract field | 18 |
| A | R1 Conc 10: no nine-vector map | 3 |
| A | R2 B-6: immediate union; VG-1 false block | 16, 17 |
| A | R2 B-7: drop I-15, rewrite I-12, fold I-09, defer I-11 | 25/29 D-21, 23, 19, 29 D-08 |
| A | R2 C-5 / NE1 / NE2: kill switch erased by reinstall; NFR-08 de-registration claim wrong | 27 |
| A | R2 C-6: C's sequence text as the skill body | 7 |
| A | R2 NE3: file pin and `--diff` are MCP-only (later held UNVERIFIED) | 9, 26 |
| A | R2 NE5: pre-edit impact cannot widen edits | 21 |
| A | R2 NE6: span-lookup binding | 13 |
| B | R2 #1: add a capability-map ref | 7 |
| B | R2 #2: withdraw FR-17 and `--index` | 14, 25, 29 D-19 |
| B | R2 #3: split latch in FR-01 | 10 |
| B | R2 #4 / NE5: D-05 sentence; adopt the cleanup asymmetric rule | 2, 23 |
| B | R2 #5: defer N-3 | 25, 29 D-21 |
| B | R2 #6 / R1 Conc 1: X-021 "20 of 23" | 2 |
| B | R2 #7 / NE4: FR-12 staged; "can never surface" corrected; I-04 V=3 | 2, 19, 28 |
| B | R2 #8: switch combination | 27 |
| B | R2 #9: "irrelevant at 30-60 calls" is arithmetic; log the query count; MCP trigger | 2, 5, 31 |
| B | R2 #10: binding rule; A's typed row; correction about A's bound | 13 |
| B | R2 #11: C-011 A+B | 21 |
| B | R2 #12: drop the interactive explore allowance; positional args over `--stdin` | 15, 16, 29 D-27 |
| B | R2 NE1: the usage line is abbreviated; `--help` capture | 2, 9 |
| B | R2 NE2: `git ls-files` filter; collection-error rate | 16, 17 |
| B | R2 NE3: exact-path script patterns; grep over script bodies | 14 |
| B | R1 Conc 3-5: telemetry; language scope; hook rejection is a value judgement | 12, 30, 29 D-03 |
| C | R1 Conc 1 / R2 #1: 1:1 scope drift; X-019 verdict "unsupported" | 1, 29 D-22, 2 |
| C | R1 Conc 2 / R2 #8: self-contradictory allowlist; exact script patterns | 14 |
| C | R1 Conc 3 / R2 #2: replace-form narrows VG-1; positional args | 16 |
| C | R1 Conc 4: tests included in the severity count | 18 |
| C | R1 Conc 5: wrong wave budget (X-015) | 20 |
| C | R1 Conc 6: MCP tool names (X-018) | 7 |
| C | R1 Conc 7 / R2 NE3: CLI `symbolsOnly`; file pin CLI-UNVERIFIED | 9 |
| C | R1 Conc 8 / R2 #3: per-run cache vs mid-run edits; tasklist field to ledger | 10, 24, 31 |
| C | R2 #4: free-form keys → closed vocabulary | 4, 7 |
| C | R2 #5: `status` latency citation | 2 |
| C | R2 #6: CLI cost argument → measurement trigger | 5 |
| C | R2 #7: X-020 is epistemically unverified | 2 |
| C | R2 NE1: pytest exit 5 → collect-only pre-pass; zero-collect rate | 16, 17 |
| C | R2 NE2: rollback by deletion is fiction after install | 27 |
| C | R2 NE4 / NE5: grep covers scripts; containment baseline is 0 | 14 |
| C | R2 C-027: `/sc:ground` folds into the seam | 26, 29 D-23 |

### EVAL-fix ledger (diff-analysis fact checks and base-internal errors)

| Item | Error | Fix | Change |
|---|---|---|---|
| X-015 | Tier-1 budget cited as 2k at `:256` | Wave 1 is about 3k at `SKILL.md:218`; `:256` is Wave 1.5 | 20 |
| X-017 | `status` ~300 ms "EVAL §5.5" | UNVERIFIED; measured `query` 290 ms and `callers` 297 ms only | 2, 31 |
| X-018 | `mcp__codegraph__search`-style names | `mcp__codegraph__codegraph_<tool>` in the capability map | 7 |
| X-019 | CLI `node {file, symbolsOnly}` "works today" | UNVERIFIED in both directions; E-2 `--help` capture | 2, 9 |
| X-020 | "Grep sees every static reference the graph sees" / "grep misses ≠ graph misses" | Neither is in EVAL; deleted. Only the corroboration-only rule remains | 2, 23 |
| X-021 | "23 callers … the rest were tests" | "20 of 23 shown: 2 production, 18 tests; 3 uninspected" | 2 |
| A-003 | Explore ban justified by "auggie is free" | Justified by size and noise against wave budgets; fallback chain Grep/Read | 2, 15 |
| Base I-04 | "can never surface today" | Out-of-hunk findings become context; chunking only at 16-30 files | 2, 19 |
| Base §2.1 | "irrelevant at 30-60 calls" | Labelled an estimate; query count logged | 2, 31 |
| Base I-07 | Class P but scored with C=0.3 | Scored with C=0.6 | 28 |
| Base B5/FR-08 | CLI `callers` "has no documented file argument" | Kept as UNVERIFIED; E-2 | 9 |

### Invariant ledger (probe UNADDRESSED items → handling)

| ID | Severity | Handling | Type | Change |
|---|---|---|---|---|
| INV-001 | HIGH | E-1 sandbox experiment; G-FRESH blocks freshness-dependent ideas beyond advisory or shadow form; Outcome B means no daemon = `stale` | **blocking prerequisite + accepted risk until E-1** | 8 |
| INV-004 | MEDIUM | Version mismatch → `provenance_unproven`, leads only; live-binary fixtures on each pin bump | requirement | 11 |
| INV-005 | MEDIUM | Probe records telemetry; installer handoff for every install path | accepted risk + owner | 12 |
| INV-009 | MEDIUM | Truncated, stale or unproven lists → native Grep count for severity | requirement | 18 |
| INV-010 | MEDIUM | G-SHADOW-REFLECT: dual counts for 10 runs, then a review before switching | gate | 18 |
| INV-011 | MEDIUM | Resolve only cited rows, ≤5 per symbol and ≤20 per run; E-4 timing; per-phase NFR-01 | requirement + measurement | 9, 13, 31 |
| INV-018 | MEDIUM | User-level env switch `IRONCLAUDE_CODEGRAPH=off` that survives updates | requirement | 27 |
| INV-019 | MEDIUM | E-3 path-form check; until then no scripts in closed-Bash consumers | gate | 9, 14 |
| INV-020 | MEDIUM | No env-prefixed calls in primitives; E-3 matching test; telemetry at user or install level | requirement + accepted risk | 9, 12 |
| INV-023 | MEDIUM | Backtest redesigned with a benefit metric (affected-only failures or seeded mutations) | gate redesign | 17 |
| INV-024 | MEDIUM | Call-expression check; string, comment and assignment rejection; multi-match rule; context-only without validator | requirement | 13, 19 |
| INV-002, 003, 012, 013, 016, 017, 022, 025 | LOW | See Change 30 list | requirement or accepted risk | 10, 13, 16, 17, 19, 26, 5 |

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-002, X-001, X-003 | A: MCP names in Class A/D allowlists and `CODEGRAPH_MCP_TOOLS` in v1 | B+A 100% / B 90% / B 90%. A conceded (R1-A Conc 2). The listing is global and hides explore (EVAL §3); schema cost unmeasured (U-014) |
| C-004, X-002 | A: `Bash(codegraph *)` in Class C; C §2 wording | B 100%. The wildcard pre-approves `install`/`upgrade`/`telemetry` (EVAL §2-§3) |
| C-007, X-006 | A: "try one `sync`" in the probe | B 100% / B+C 100%. `sync` fails on the writer lock (EVAL §5.7) and writes inside read flows |
| C-010, X-004 | A: evidence-validator text edit and Class D listing | B+C 100%. The validator already rejects def-line rows cited as call sites (`evidence-validator.md:62-66`) |
| C-013, X-008 | A: immediate union; C: `tests` exactly the `affected` list | B 85%. A union on an unrun tool can false-block a push (`sc-pr-submit-protocol/SKILL.md:203-206`); replacing the list can narrow it |
| C-017, X-013 | A: resolved call-site count; C: caller count including tests | B 100%. In the one sample, 18 of 20 shown rows were tests (EVAL §5.5) |
| C-018 | A: `caller_functions` label; C: additive keys plus a `contract_version` bump | B 90%. Reflect's CLI-parsed contract stays untouched; `degraded_components` entries only |
| C-022, X-007 | A: I-17 SessionStart status hook | B 90%. Unmeasured `status` latency and extra hook failure surface; `/sc:graph status` and the `/sc:load` line give visibility |
| C-006 | C: binary `available/unavailable` latch | A+B 100%. Under-discriminates `stale` and `foreign_index` (R1-C self-critique) |
| C-005 | C: guidance-only seam with no args or output | A+B+C 75% takes C's text but A's output schema. A seam with no schema pushes key invention onto consumers (R2-A C-6, R2-C #4) |
| C-001 | C: 1:1 Serena swap ideas | A+B 100%. Out of scope per the seed Problem Statement; Phase 3 owns them |
| C-030 | A: "always pass `file`" on every call | B 90%. `file` is documented only on MCP tools (EVAL §3); the CLI pin waits on E-2 |
| C-020 | A I-11 liveness check; C I-06 fallback tier for reuse-auditor | B 90%. Agents get no MCP in v1, and agent-found candidates cannot be precomputed |
| U-021 | C: stale → treat HIGH as MEDIUM | Superseded. Under Change 18, stale or truncated counts never feed severity |
| C-028 (field shape) | C: `/sc:impact` `{resolved: bool, verified: bool}` rows | A+B 75%. Typed `resolution` (Change 13) carries more states; C's drop-never-repair behaviour is kept |
| X-012 (A side) | A: zero callers add DELETE confidence | C 85%. Zero proves nothing; the base's earlier drop is replaced by C's rule, not A's |
| S-001 (C side) | C: no front matter | A 70%. B's front matter is kept and gains `ground_truth` (Change 1) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1-4 | Low | Wording or terminology drift within the merged doc | Revert to the base text of the cited sections |
| 5 | Low | Trigger misread as a per-orchestrator switch | Revert the row; v1 rules unchanged |
| 6 | Medium | Gates reference blockers that are not defined | Remove B9-B12; Change 8/9 text then cites INV IDs directly |
| 7 | Medium | Seam schema error propagates to every consumer | Revert to base N-1 (probe-only) plus Change 4 terminology |
| 8 | **High** | Outcome B keeps 5 ideas advisory; or E-1 is skipped and stale sets pass as fresh | No rollback: E-1 is mandatory. Without E-1, the gated ideas remain advisory |
| 9 | Low | Phase 3 starts without flag facts | CLI ambiguity falls back to `query --json` file filtering (already specified) |
| 10 | Medium | Re-check semantics wrong if E-1 gives Outcome B | Outcome B rule: no daemon = `stale` |
| 11 | Low | Over-degrades on harmless version bumps | Relax to a warning after fixtures are re-recorded |
| 12 | Medium | Telemetry stays on for user-installed binaries | Accepted risk; the installer handoff closes it |
| 13 | Medium | Lower resolver recall; more `unresolved` rows | Raise budgets after E-4; never relax the binding |
| 14 | Low | Allowlist blocks a needed subcommand | Add the single missing per-subcommand pattern |
| 15 | Low | Interactive users lose a convenience | Reopen after the explore measurement (A-004) |
| 16 | Medium | Union false-blocks a push | Stage 1 is gated; fall back to `<changed-area>` on any collection error |
| 17 | Medium | Backtest too costly to run | Keep the union disabled (advisory forever) |
| 18 | Medium | Reflect severity calibration shift | Shadow mode keeps today's severity until review |
| 19 | Medium | False `dependent-impact` exemptions | Stage 3 disabled; stages 1-2 are context only |
| 20-25 | Low-Medium | Consumer edits add noise or scope creep | Each ships a native fallback and `graph:*` token; remove the step |
| 26 | Medium | New primitives untested | Ship K-1 first; K-2..K-4 are independent |
| 27 | Medium | Env switch name drifts | Pin the name in the capability map and a test |
| 28-32 | Low | Ranking or drop reasons disputed later | Re-score with the stated formula; the inputs are recorded |

## Review Status
- [x] Auto-approved (non-interactive run; `--interactive` not set)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-10-29T17:27:48Z
- Carried condition: Step 5 (merge) must apply Change 8 as written. The merged output must show INV-001 / E-1 as a blocking prerequisite in its ranked list (rank 1) and in §2.3.
