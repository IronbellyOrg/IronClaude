---
name: sc:reflect-protocol
description: "Tiered reflection protocol grounded in real code and real citations. UC-1 (pre-execution) validates a proposed strategy/tasklist against its driving spec/PRD for coverage and best-practice compliance. UC-2 (post-execution) audits completed work for 100% adherence and classifies every divergence under a 4-category deviation taxonomy (Authorized expansion / Necessary deviation / Drift / Regression). Tier 1 is a fast single-agent grounded pass; Tier 2 fans out 2-3 heterogeneous reviewer agents on different model classes and merges via sc-adversarial-protocol Mode A; Tier 3 hands off to task-builder for a corrective MDTM remediation. Structural mechanisms — heterogeneous reviewers, blind calibration, mandatory evidence-validator gate — exist specifically to neutralise the representational bias that makes single-agent self-review unreliable."
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories, mcp__serena__search_for_pattern, mcp__serena__activate_project, mcp__serena__get_current_config, mcp__serena__find_implementations, mcp__serena__find_declaration, mcp__serena__delete_memory, mcp__serena__rename_memory, mcp__serena__edit_memory, mcp__serena__summarize_changes, mcp__serena__execute_shell_command, mcp__serena__onboarding, mcp__serena__prepare_for_new_conversation, mcp__serena__type_hierarchy, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily-search, mcp__sequential-thinking__sequentialthinking
---

<!-- markdownlint-disable MD013 MD040 -->

<!-- Provenance: This document was produced by /sc:adversarial via /sc:brainstorm -->
<!-- Base: Variant 2 -->
<!-- Merge date: 2026-05-26T23:02:22Z -->
<!-- Non-base sources incorporated: V1, V3, V4, V5 -->
<!-- unresolved_conflicts: [INV-021_vendor_heterogeneity_v1.1_deferral, INV-023_sufficiency_v1.1_hardening] -->

<!-- Extended metadata (for documentation, not parsed):
category: validation
complexity: advanced
mcp-servers: [serena, auggie, context7, tavily, sequential]
personas: [analyzer, qa, refactorer, architect]
spec: .dev/eval-workspaces/sc-reflect/SPEC.md
supersedes: src/superclaude/commands/reflect.md (legacy think_about_* surface)
-->

# Reflect Protocol

## 1. Purpose & Core Thesis

Reflection that confirms its own conclusions is worse than no reflection. The legacy `/sc:reflect` surface, built on `think_about_task_adherence` / `think_about_collected_information` / `think_about_whether_you_are_done`, runs the *same* representational stack that produced the work as the auditor of the work. Per Mehta (Towards AI, Mar 2026): "the same representational biases that produced the error are present when it re-evaluates." Single-agent self-review is structurally biased, not merely under-prompted.

This protocol is built around three structural mechanisms that single-model self-reflection cannot supply:

1. **Heterogeneous reviewer ensemble at Tier 2** — reviewers run on different model classes (haiku / sonnet / optional qwen-or-kimi) so per-model representational bias does not stack. Empirical support: HDEE, LLM-TOPLA, Wisdom of Silicon Crowd. The merge judge is *deliberately a different class than every debater* (weak-judge-strong-debaters per Khan ICML 2024 Oral, Kenton NeurIPS 2024).
2. **Blind calibration of every reviewer card** — `confidence-calibrator` re-grades each reviewer's findings without the formation context, so the merged verdict weights *calibrated* scores rather than self-reported ones.
3. **Mandatory evidence-validator gate on the final report** — every `file:line` citation in the merged reflection report is independently re-Read; unfounded citations are *dropped, not downgraded*. A report that ships with no dropped citations is treated as suspicious, not clean. Inferred-requirement rows from Step 1B.0 Pass 2 (D13) are citations and are validated identically: a row whose verbatim quote does not match its cited spec lines is dropped (recorded in the Inferred-requirements postscript, counted in `citations_dropped`) AND `coverage_pct_union`, `unmapped_requirements_union`, and `S_dev_density` are recomputed over the surviving union before the report finalizes.

**Two modes, one protocol.**

- **UC-1 (pre-execution)**: input is a *proposed* tasklist/strategy plus its driving spec/PRD/objectives doc. Output is a coverage matrix, a best-practice compliance grade, and a gap registry — *before* token spend on execution. ROI band: 200-500 tokens to potentially save 5,000-50,000 (mirrors confidence-check economics).
- **UC-2 (post-execution)**: input is completed agent work (commit diff, artifact files, task log) plus the tasklist that drove it. Output is a 100%-completion audit, a per-item deviation classification under the 4-category taxonomy in §10, and a remediation recommendation. This is the durable, high-value mode.

**Hallucination contract.** Every claim in the final report is either (a) **Grounded** — backed by a real `file:line` citation, a real diagnostic output, or a real document section that survives evidence-validator re-Read; or (b) **Inferred** — explicitly tagged `[INFERRED]` with a citation chain that the report admits is non-load-bearing. There is no third bucket. Findings that cannot be tagged either way are *dropped*.

---

## 2. Triggers

This skill is invoked ONLY by the `/sc:reflect` command via `Skill sc:reflect-protocol`. Never invoked directly by users.

Activation conditions on the command side:

- User runs `/sc:reflect <args>` in Claude Code.
- Auto-trigger from `sc:troubleshoot-protocol` Wave 6 Phase B (pre-execution review of task-builder output) and Phase D (post-execution validation of `/task` completion).
- Auto-trigger from `sc:task-protocol` end-of-task hook when configured.

Do NOT invoke this skill directly outside the above paths.

---

## 3. Required Input + Mode Selection

The skill MUST resolve a mode (UC-1 or UC-2) before any wave runs.

### 3.1 Inputs

- `--mode pre | post` — explicit mode (RECOMMENDED for non-interactive callers; eliminates auto-detect ambiguity)
- `--spec <path>` — driving spec/PRD/objectives doc (required for UC-1; recommended for UC-2)
- `--tasklist <path>` — tasklist file (strongly recommended for UC-2 — does not STOP if omitted; recommended for UC-1 if a tasklist already exists)
- `--diff <ref-or-path>` — git ref (e.g., `HEAD~1..HEAD`, branch name) or path to a diff file (required for UC-2)
- `--commit-range <ref-range>` — alternative to `--diff` for resolving a post-execution diff via git
- `--scope <path>` — narrowing scope (when resolving to modified files → UC-2 auto-detect)
- `--task-log <path>` — task execution log (optional, UC-2 only)
- `--depth quick | standard | deep` — Tier-1-only / Tier-1-then-rubric / force-Tier-2 (see §5)
- `--tier 1 | 2 | auto` — explicit tier pin (overrides rubric); `auto` is default
- `--reviewers N` — number of Tier 2 reviewers (2-3; default 3, clamped by `--depth`)
- `--output <dir>` — output directory (default `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/`)
- `--coverage-floor <float>` — optional override of the T1 coverage stop floor (default 0.90; high-safety profile may set to 0.95)
- `--no-mcp`, `--no-evidence-validator` (debug only; auto-warns), `--remediate` (offer Tier 3)
- `--no-verify` — disable the UC-2 `execute_shell_command` verification triangle (§6.1 step 5.5). Default is *default-on*: in UC-2, scoped non-mutating verification (tests/linters/type-checkers/build) runs behind the §6.1 safety envelope and feeds the §10.4 Regression detector. When set, sets `verification_skip_reason: --no-verify` and degrades Regression detection to the task-log claim with a Grounding Gap entry. (Subsumes the deprecated `--rerun-tests` alias, which now maps to "verification on" = the default; see §10.4.)
- `--onboard` — opt-in (default OFF) one-shot Serena `onboarding` bootstrap at Wave 0.7b, run ONLY when `list_memories` is empty for the project slug. Seeds the cold-start calibration baseline (§6.3 memory). Never auto-triggers and never creates a `.serena/` directory implicitly; bounded by the NFR-7 context budget. Modeled on `--remediate` (enable-flag for default-off behavior).
- `--with-hierarchy` — opt-in (default OFF) enable `type_hierarchy` transitive supertype/subtype retrieval at §6.1 step 4.5 and Wave 1B.3. Backend-gated: **default OFF on `lsp` backends** (no generic `type_hierarchy` tool there until the OQ-M3 empirical probe confirms per-language support) and **unavailable on `none`**; only a hierarchy-capable (`jetbrains`) backend runs it. Non-OO codebases see zero degradation when unset. Modeled on `--remediate` (enable-flag for default-off behavior).
- `--budget-remaining <int>` *(P5)* — caller-side budget hint (typically `TurnLedger.available()` from a sprint context). When provided, reflect cross-checks against the §15 cost profile and may auto-degrade tier; emits `budget_forced_tier_downgrade: true` in the contract when this happens. See §4.0 step 0.9.
- **Promotion gate flags (UC-2 only — see §14.5):**
  - `--no-promote` — suppress Wave 7 promotion. Default is *default-on*: when the §14.5.2 strict gate passes, the validated work-unit folder moves to its `done` destination.
  - `--promote-anyway` — override `status: partial` gate condition (all other 7 conditions still apply). No effect on `status: failed`.
  - `--promote-dry-run` — print the `mv` command + gate evaluation; perform no mutation.
  - `--promote-mode auto|task|sprint-release|none` — force a specific promotion adapter or disable selection. Default `auto`.
  - `--promote-resume <checkpoint-path>` — resume an interrupted cross-filesystem promotion from a `promotion-checkpoint.yaml`. See §14.5.5 for partial-state recovery semantics.

(See `refs/input-resolution.md` for per-flag expanded semantics and worked examples.)

### 3.2 Mode selection (6-rule first-match order)

Applied in order, first match wins:

1. **`--mode pre | post`** present → use literal value. STOP if value is anything else.
2. **`--diff` OR `--commit-range`** flag present → **UC-2 (post)**.
3. **`--scope`** resolves to a directory whose tracked files overlap `git diff --name-only HEAD~1..HEAD` → **UC-2 (post)**.
4. Input arguments include both a `--tasklist` file AND a completed-work artifact directory (`.dev/tasks/done/`, `.dev/releases/current/results/`, etc.) → **UC-2 (post)**.
5. `--spec` AND `--tasklist` present with no diff / no done-marker artifacts → **UC-1 (pre)**. If only `--spec` is present → UC-1 with a coverage-only pass.
6. None of the above resolve → **STOP** with: `"Reflect requires --mode pre|post OR a resolvable input combination. See refs/input-resolution.md."`

(See `refs/input-resolution.md` for worked examples of each rule.)

### 3.3 Hard STOP conditions

- Neither `--spec`, `--tasklist`, nor `--diff` provided.
- `--mode pre` with no `--spec` (pre-execution reflection has nothing to reflect against).
- `--mode post` with no `--diff` AND no `--task-log` (post-execution reflection has no completed work to audit).
- `--depth deep` with under-specified input (e.g., 1-line spec, empty tasklist).
- `--output` resolves under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` (CLAUDE.md ABSOLUTE RULE — distributable paths are not output sinks).

### 3.4 Environment Prerequisites

The skill resolves model aliases from environment at Wave 0:

- `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

Aliases drive Tier 2 reviewer composition (see §7.1 and the alias-routing table in §4 Wave 0). Missing aliases **do not abort the skill**; they degrade reviewer topology per the §4 Wave 0 routing table (0/1/2/3+ alias rows). The skill emits `degraded_components: ["env-aliases"]` into the audit log and surfaces a WARN to the user when running with fewer than 3 distinct classes. The full degraded-mode envelope (env, MCPs, agents) is documented in §14.

(See `refs/input-resolution.md` "Env routing table" for the 4-row alias→tier routing matrix and grader assertions.)

---

## 4. Wave / Tier Architecture

**Per-step audit emit convention.** Every numbered step within every wave emits one row to `<output>/audit.log` with shape: `{wave: <N>, step: <M>, timestamp: <ISO-8601>, outcome: ok|warn|fail|skip, evidence_ref: <path-or-null>}`. This is the audit-granularity unit that resolves the 9-wave vs 7-wave structural disagreement: each step (not each wave) is the audit row.

```
Wave 0:   Parse + Validate Input + Activate Project + Memory Hydrate
            0.1 Parse flags + apply §3.2 mode-selection
            0.2 Validate input paths (Read existence)
            0.3 Probe sc-adversarial-protocol installation (see §14)
            0.4 Compute input_sha256 snapshot (see §4.0 — Change #10)
            0.5 Resolve env-var aliases + apply 0/1/2/3+ alias routing table (Change #13/#14)
            0.5c get_current_config probe (active context/modes/version fingerprint)
            0.5d verification/adoption availability probe (backend + execute_shell_command + onboarding + read_only — consume 0.5c snapshot)
            0.6 Inspect vendor heterogeneity (Change #18 — warn-only)
            0.7 Activate Serena project + memory hydrate + parse onboarding status
            0.7b onboarding bootstrap (only when --onboard AND list_memories empty)
            0.8 Open audit log + machine-readable header
Wave 1:   Tier 1 — Grounded Single-Agent Reflection
            1A. Real-code grounding (auggie + serena symbolic chain)
            1B. Mode-specific evidence gathering (UC-1: coverage map; UC-2: tasklist-vs-diff map)
                — zero-task guard (Change #12); coverage_undefined route (Change #11)
            1C. Single-agent reflection (root-cause-analyst OR self-review)
            1D. Blind calibration (confidence-calibrator) on the Tier 1 card
Wave 2:   Tier-Decision Gate (rubric — §5; tier_decision.yaml audit artifact — §5.4)
Wave 3:   Tier 2 — Parallel Heterogeneous Reviewers (conditional)
            3A. Compose reviewer agent-spec (model + persona rotation)
            3B. Materialize per-reviewer brief packages (Change #7) + spawn N reviewers in parallel via Task
            3C. Per-card blind calibration (confidence-calibrator × N) — disjoint-set rule (Change #16 / §11.3)
            3D. Distill candidate verdicts
Wave 4:   Tier 2 — Adversarial Merge via sc-adversarial-protocol (conditional)
Wave 5:   Synthesis + Evidence-Validator Gate + Report
            5.0 Pre-invocation probe of sc-adversarial (F1/F2/F3 fallback — Change #15)
            5.x Re-read input + verify input_sha256 matches snapshot (Change #10 drift guard)
Wave 6:   Tier 3 — Remediation Handoff (conditional, opt-in)
Wave 7:   Promotion Mutation (UC-2 only — §14.5 strict gate; default-on, --no-promote to suppress)
          —— SRP boundary: Waves 0-6 are read-only review (write only to <output>/);
              Wave 7 is the SOLE wave that mutates repository state outside <output>/.
              Architecturally a SIBLING phase to the review waves, not an extension.
            7.1 Resolve adapter (task | sprint-release | none)
            7.2 Re-verify all 9 gate conditions (pre-mutation validation sub-step; NOT a mutation)
                  — re-Read cited files if Wave 6 ran
            7.3 Check destination collision rules (§14.5.5) (still validation)
            7.3.5 Write promotion-checkpoint.yaml (cross-fs only) (forensic pre-write, not mutation of repo)
            7.3.6 Append promotion-log entry with pending=true (pre-mv forensic pre-write)
            7.4 MUTATE: move (source → destination — atomic on same-fs; copy+verify+remove on cross-fs)
                  — this is the ONLY repository-mutating step in the entire skill
            7.5 SHA-verify moved tree vs pre-move snapshot (post-mutation validation)
            7.6 Flip pending=false + audit row (forensic finalization, not mutation of repo)
            7.7 Update return-contract promotion_* fields (output-dir write only)
```

Each wave has explicit entry/exit. Refs are loaded on-demand per wave, never pre-loaded. **The 7-wave count is structurally "6 review waves (0-6, all read-only outside `<output>/`) + 1 mutation wave (7)."** Wave 7's SRP boundary is intentional: every mutation-related concern (atomicity, rollback, partial-state recovery, forensic log) is concentrated in §14.5, NOT distributed across the review waves. Implementations MAY ship Wave 7 as a separate code path with its own entry/exit; reflect's contract guarantees that Waves 0-6 never mutate outside `<output>/` regardless.

### 4.0 Wave 0 — Detailed step additions

**Step 0.4 (input_sha256 tree-snapshot).** Compute a **tree-hash** over every file the run treats as input. The tree consists of: (1) the `tasklist_path` itself (always present in UC-2); (2) the `spec_path` (when `--spec` provided); (3) every file referenced by relative or absolute path from the tasklist body (link-following with depth = 1; do NOT recurse into linked-link chains for v1); (4) for UC-2 tasklist inputs that resolve under a work-unit directory (e.g., `.dev/tasks/to-do/TASK-NNN/`), every file under that directory tree (`find <work-unit-dir> -type f`), **filtered through `VERIFICATION_ARTIFACT_EXCLUDES` (below)**.

**`VERIFICATION_ARTIFACT_EXCLUDES` (FR-4.8 / M-COR2).** Because the §6.1 step 5.5 verification triangle runs `pytest`/`mypy`/`ruff`/build inside or adjacent to the work-unit subtree, those tools emit build/test cache artifacts *into the input tree*. An unfiltered `find -type f` would then see them as "added files" and trip the drift guard, STOPping the skill on a successful verify. To prevent this, the following glob set is excluded from the input tree at BOTH construction here AND the Wave-5/Wave-7 recompute below — the SAME set must be applied at both sites or the snapshot and recompute disagree even without a real edit:

```
__pycache__/   *.pyc   *.pyo   *.pyd
.pytest_cache/   .coverage   .coverage.*   htmlcov/
.mypy_cache/   .ruff_cache/
node_modules/.cache/   .tsbuildinfo
target/   .hypothesis/   *.egg-info/
```

The exclusion is scoped to build/test artifacts ONLY — a real source-file change (add/remove/modify/rename of a non-artifact file) still trips the drift guard and STOPs.

The tree-hash is computed as:

```
input_tree   = [p for p in input_tree if not matches_any(p, VERIFICATION_ARTIFACT_EXCLUDES)]
file_list    = sorted([(relative_path, sha256(read(absolute_path))) for path in input_tree])
input_tree_sha256 = sha256(serialize_as_json(file_list))    # canonical serialization for reproducibility
```

Persist the file list AND the tree-hash to `<output>/artifacts/input-snapshot.yaml`:

```yaml
input_tree_sha256: <hex>
file_list:
  - path: <rel-path>
    sha256: <hex>
file_count: <int>
```

Before Wave 5 synthesis AND at Wave 7 step 7.2 (pre-mutation), re-read the input tree (**applying the same `VERIFICATION_ARTIFACT_EXCLUDES` filter as at construction** — FR-4.8) and recompute `input_tree_sha256`. If it differs (any non-excluded file added, removed, modified, or renamed), STOP with `input_drift` flag, emit BOTH SHAs and the per-file diff into the return contract, and route to `status: partial`. Build/test artifacts emitted by the step-5.5 verification run are excluded at both sites, so a successful verify does NOT trip `input_drift`.

**Backward-compat with v1.0-pre contract.** The legacy `input_sha256: {tasklist: <hex>, spec: <hex>}` field in §9.1 is preserved as a derivable subset (first two entries of `file_list`); both fields are emitted in v1.0. The Wave 5 drift guard uses `input_tree_sha256` as the authoritative invariant; the legacy field is recording for backward-compat consumers per §9.4 evolution policy.

**Step 0.5 (env-var alias resolution + 0/1/2/3+ alias routing).** Resolve the three `ANTHROPIC_DEFAULT_*_MODEL` env vars into an alias-set. Apply this routing table to decide Tier 2 reviewer count:

| Aliases resolved | `--tier` flag | Routing | Telemetry |
|------------------|---------------|---------|-----------|
| 0 | (any except `--tier 2`) | T1-only path; WARN "T2 requires ≥1 model class"; degraded | `degraded_components: ["env-aliases"]` |
| 0 | `--tier 2` explicit override | **STOP** with explicit message: `"--tier 2 requires ≥1 alias resolved (zero aliases available — set ANTHROPIC_DEFAULT_*_MODEL env vars or omit --tier 2)"` | `degraded_components: ["env-aliases"]`, `stop_reason: "zero-aliases-tier2-conflict"` |
| 1 | (any) | T1-only path; WARN "T2 requires ≥2 model classes" | `t2_model_class_diversity: degraded` |
| 2 | (any) | T2 with 2 reviewers (degraded) | `t2_model_class_diversity: degraded` |
| ≥3 | (any) | T2 with 3 reviewers (full diversity) | `t2_model_class_diversity: full` |

Grader assertion: `yaml_field` asserts `t2_model_class_diversity` is one of `{full, degraded}` when the skill ran to completion (non-STOP).

The zero-aliases + `--tier 2` row is the only case where alias-resolution itself can STOP the skill — every other zero/one-alias path degrades gracefully. The reasoning: `--tier 2` is a hard override per §5.1, but the rubric cannot satisfy it with zero model classes available; the conflict is irresolvable, so the skill MUST fail loudly rather than silently downgrade against an explicit user request.

(See `refs/input-resolution.md` "Env routing table" for the full 4-row matrix with grader-assertion column.)

**Step 0.5c (active-project config probe, FR-7).** At Wave 0, invoke `mcp__serena__get_current_config` once to fingerprint Serena's own active state — a calibration input reflect currently lacks. The return shape is documented-unstable across Serena v1.0→v1.5 (OQ-4), so parse **defensively**:

1. Invoke `get_current_config`. Using **field-presence checks** (never assume a field exists), extract: `serena_active_context` (active context string), `serena_active_modes` (list), the loaded-tools list (→ `serena_tool_count` and any chain-critical tools excluded by the active context → `serena_excluded_tools`), and the Serena version. Any field whose presence check fails → that derived value is `unknown`.
2. Derive a **three-valued** `serena_version` ∈ `{"<v1.5", ">=v1.5", "unknown"}`. Default `unknown`; `unknown` is treated as `<v1.5` for all downstream gating (C2 — load-bearing for FR-6 and FR-8).
3. Write the parsed snapshot to `<output>/serena-config-snapshot.yaml` and record `serena_config_snapshot_path` in telemetry.
4. **Context-exclusion up-weight (FR-7.3):** when the active context excludes a chain-critical tool (e.g. `get_diagnostics_for_file`), append `"serena:context-excluded"` to `degraded_components` and influence rubric `S_dev_density` upward (the grounding chain is operating with a known capability gap).
5. **Fail-open (OQ-4):** on parse failure, emit `degraded_components: ["get_current_config"]`, set `serena_version: unknown`, skip the snapshot, and continue Wave 0 — never abort.

This step emits one `audit.log` row per the §4 per-step convention with the parsed `serena_context`/`serena_modes`/`serena_tool_count`/`serena_excluded_tools` evidence. Emit `serena_version`, `serena_active_context`, `serena_active_modes`, and `serena_config_snapshot_path` to telemetry when this step runs; `serena_version: unknown` with `degraded_components: ["get_current_config"]` and no snapshot path when skipped (parse failure or Serena unavailable).

**Step 0.5d (verification & adoption availability probe — M-ARC3 four-field contract).** Derive a single cohesive Wave-0 availability surface that the medium-complexity Serena adoptions (FR-1 `type_hierarchy`, FR-2 `onboarding`, FR-4 `execute_shell_command`) CONSUME rather than each re-deriving. The surface has exactly four fields, computed from the Step 0.5c `serena_config_snapshot_path` snapshot plus one project-config read:

```yaml
# Wave-0 availability contract (consumed by FR-1/2/4; field names are a strict subset of FR-7's output)
backend: jetbrains | lsp | none                 # gates FR-1 type_hierarchy step 4.5
execute_shell_command_available: <bool>         # gates FR-4 verification triangle step 5.5
onboarding_available: <bool>                    # gates FR-2 onboarding bootstrap step 0.7b
read_only: <bool>                               # FR-4.7: read_only:true disables the verification triangle
```

1. **`backend`** — parse the Serena language-backend string from the Step 0.5c snapshot (`jetbrains | lsp | none`). When the snapshot is absent (Step 0.5c was skipped / FR-7 not yet merged), perform a minimal inline `mcp__serena__get_current_config` call to read just the backend string; on failure → `backend: none`.
2. **`execute_shell_command_available`** — membership test of `execute_shell_command` against the Step 0.5c active-tools list (NOT the available-but-excluded list). Absent from the active list ⇒ `false` (the common `claude-code`/`ide-assistant` default — the tool is context-excluded).
3. **`onboarding_available`** — membership test of `onboarding` against the same active-tools list.
4. **`read_only`** — the ONE field `get_current_config` does NOT surface. Derive it by reading the `read_only` key from the active project's `.serena/project.yml` (or equivalent project config). Absent / unreadable ⇒ treat verification as unavailable (`read_only` cannot be confirmed `false` → degrade the capability, emit the FR-4.7 skip reason, never STOP). Do NOT fabricate a `read_only` field on the `get_current_config` output — it is a project-config value, not a config-probe value.

**Field-name compatibility (M-ARC3 / OQ-M5):** these four field names are a strict subset of FR-7's snapshot output, so when the low-spec FR-7 substrate is fully merged the inline derivation collapses to a pure read of FR-7's snapshot with no contract change — the swap is non-breaking. The `read_only` project-config read persists either way (FR-7 never emits it).

**Consumption rule (do NOT re-probe downstream):** FR-1's §6.1 step 4.5 / Wave-1B.3 gate (and FR-1's Phase-opening backend probe) READ this Wave-0 `backend` field; FR-2's §4.0 step 0.7b gate READS `onboarding_available`; FR-4's §6.1 step 5.5 gate READS `execute_shell_command_available` and `read_only`. The later runtime probes confirm/refine this Wave-0 baseline — they do not replace it.

**Fail-open (§6.5):** any parse failure of any field → set that field to its unavailable value (`backend: none` / `*_available: false` / `read_only` unconfirmed → treat triangle as disabled), emit the matching skip reason to the consuming FR's telemetry, and continue. This step never STOPs the skill. It emits one `audit.log` row per the §4 per-step convention with the four-field availability evidence.

**Step 0.6 (vendor heterogeneity check).** For each resolved alias, extract the vendor (Anthropic / Qwen / Kimi / DeepSeek / OpenAI-compat / etc.) by alias-name heuristic. Emit one of `t2_vendor_diversity: multi` (≥2 vendors among resolved aliases) or `t2_vendor_diversity: single` (all aliases share one vendor). When `single`, emit a WARN with the suggested env-var override (full message body lives in `refs/ops-integration.md`). This is **warn-only in v1**; behaviour does not block. See §11.0 and the v1.1 deferred-hardening notes in §19.

**Step 0.7 (activate project + memory hydrate + onboarding-status parse, FR-6).** At Wave 0, after `mcp__serena__activate_project` and memory hydrate, derive whether project memory was bootstrapped — an input to `S_dev_density` calibration. The historical standalone onboarding-status tool was **DELETED in Serena v1.5.0**, so it is NOT called and NOT in `allowed-tools`; the signal is derived from the activation message instead:

1. Parse the `mcp__serena__activate_project` response message for the onboarding-status marker (v1.2.0+ always provides the full activation message on `activate_project`).
2. **Fallback proxy:** when the marker is absent from the message, infer bootstrap state from `mcp__serena__list_memories` — presence of the v1.5 `memory_maintenance` seed memory (or any project seed memory) ⇒ bootstrapped.
3. Set `onboarding_status` ∈ `{bootstrapped, not_bootstrapped, unknown}` (default `unknown`), recording `onboarding_status_source` (`activation_msg` | `list_memories_proxy` | `unknown`).
4. **FR-6.4:** `not_bootstrapped` down-weights grounding confidence (the project has no memory to ground against); `unknown` implies **NO `S_dev_density` down-weight** (absence of signal is not negative signal).
5. **Fail-open:** on parse/probe failure, set `onboarding_status: unknown`, emit `degraded_components: ["serena:onboarding-parse"]`, and continue — never abort, and never fall back to the defunct (v1.5.0-deleted) standalone onboarding-status tool.

This step emits one `audit.log` row per the §4 per-step convention recording `onboarding_status` and `onboarding_status_source`. Emit `onboarding_status: bootstrapped | not_bootstrapped` (with its source) when the parse succeeds; `onboarding_status: unknown` (no `S_dev_density` down-weight, per FR-6.4) when the marker and proxy are both absent or the probe fails.

**Step 0.7b (onboarding bootstrap, FR-RV3-MED.2).** A one-shot, opt-in cold-start calibration bootstrap. It runs **ONLY when `--onboard` is set AND `list_memories` returns empty for the project slug** (FR-2.1); it NEVER auto-triggers and NEVER creates a `.serena/` directory implicitly (FR-2.5).

1. **Gate (warm start, FR-2.4):** if `list_memories` is non-empty for the slug, skip with `onboarding_ran: false`, `onboarding_skipped_reason: "memories-present"`.
2. **Availability probe (FR-2.3):** read `onboarding_available` from the Wave-0 step 0.5d availability contract. If the `onboarding` tool is excluded from the active context, emit `onboarding_ran: false`, `onboarding_skipped_reason: "context-excluded"`, and a loud WARN telling the operator to switch context — **never a hard STOP**.
3. **Invoke + silent-fail guard (FR-2.2):** otherwise capture the pre-count from `list_memories`, invoke `mcp__serena__onboarding()`, then re-`list_memories` and compute the delta. Delta ≤ 0 ⇒ `onboarding_succeeded: false` + a WARN ("onboarding completed but no new memories written"). Positive delta ⇒ `onboarding_succeeded: true` with `onboarding_memories_written: [<list>]`.
4. **Precedence (FR-2.6):** do NOT overwrite a present `global/memory_maintenance` memory.
5. **Context budget (NFR-7):** bound the bootstrap by a hard turn/context budget (default = the §15 T1 band, hard-kill at 1.25×). On breach, abort onboarding and emit `onboarding_budget_exceeded: true`, degrade to `onboarding_succeeded: false` (NOT "bootstrapped"), and NEVER consume the reflection waves' budget.
6. One-shot per project; fail-open on any failure (skip + audit row + WARN, never STOP).

Emit `onboarding_ran: true` (with `onboarding_succeeded` and, on success, `onboarding_memories_written`) when the bootstrap executes; `onboarding_ran: false` (with `onboarding_skipped_reason`) when it is gated off (warm start, context-excluded, or `--onboard` not set). This step emits one `audit.log` row per the §4 per-step convention. The bootstrapped memories feed the §6.3 cold-start calibration baseline.

**Step 0.9 (budget pre-flight, P5).** When `--budget-remaining N` is provided, route per this table against the §15 Token Cost Profile (Claude-side band midpoints). Boundaries are stated with explicit inclusive/exclusive operators to remove ambiguity at integer boundary values. The numeric anchors are **T1-midpoint = 6 turns**, **T2-midpoint = 52 turns**, computed from §15's "T1 only ~3-8k Claude" and "T2 ~35-70k Claude" bands via the conversion `1 turn ≈ 1k claude-orchestration tokens at the band midpoint`.

| Budget remaining (N) | Routing | Telemetry |
|---------------------|---------|-----------|
| `N < 5` (strictly below `TurnLedger.minimum_allocation`) | **STOP** with explicit message: `"budget too low for reflect — minimum 5 turns"` | `budget_forced_stop: true` |
| `5 ≤ N < 6` (inclusive 5, exclusive 6 — i.e., only N=5 in integer arithmetic; the T1-only floor) | Run T1 only with WARN; do NOT escalate to T2 even if rubric requests | `budget_forced_tier_downgrade: true`, `forced_tier: 1` |
| `6 ≤ N < 52` (inclusive 6 — N=6 enters this band, NOT the previous) | Allow T1; if rubric escalates to T2 and `N < 65` (i.e., 52 × 1.25), downgrade to T1 with WARN | `budget_forced_tier_downgrade: true` *(only if downgrade applied)* |
| `N ≥ 65` (inclusive — T2-midpoint × 1.25 floor) | No constraint; run as rubric directs | `budget_forced_tier_downgrade: false` |
| `--budget-remaining` unset | Skip; emit `budget_check_skipped: true` | none |

**Boundary clarifications.** N=5 is the T1-only floor (the second row only; T2 cannot fire at N=5 regardless of rubric). N=6 is the first value that enters the third row. N=52 is the first value at which T2 has no downgrade pressure unless the 1.25× kill threshold (N=65) is also crossed. The `≤` vs `<` operators in this table are the authoritative source for boundary classification. This step runs AFTER step 0.5 — alias-degraded routing takes precedence over budget routing for tier selection, but budget routing can still STOP a degraded T1 path if `N < 5`.

### 4.1 Wave 1 — Detailed step additions

**Step 1B.0 (two-pass requirement extraction, UC-1; D13 coverage hardening).** Extraction runs in two passes before any matching. **Pass 1 (deterministic, authoritative for labeled IDs):** run the `ID_REGEX` extraction per `refs/coverage-mapping.md`, unchanged, PLUS range-notation expansion: a parsed token of the form `<PREFIX>-NNN..MMM` (or `<PREFIX>-NNN-MMM` where both sides are numeric and the right exceeds the left) expands to the enumerated ID set (`SPEC-001..021` yields 21 IDs). For dedup purposes each parsed ID also gets a deterministic REQUIREMENT SPAN: a heading-borne ID owns its section (to the next same-or-higher heading or next parsed ID, whichever first); a list-item-borne ID owns that item including indented continuations; an inline-prose ID owns its paragraph. **Pass 2 (inference; the requirements-analyst mandate):** read the FULL spec body and enumerate requirement-shaped content Pass 1 missed: imperative MUST/SHALL/MUST-NOT statements, acceptance criteria, constraint bullets, enumerated deliverables, and requirement-bearing headings. Emit each as a synthetic row with sequential id `INF-NNN`, and EVERY inferred row MUST carry (a) a verbatim quote of the source span (max 2 sentences) and (b) a `file:line` citation into the spec. An inferred row missing either is INVALID and is dropped at emission (it never enters the matrix). Deduplication: an inferred row whose quote overlaps ANY line of a parsed requirement's SPAN is dropped (the parsed row wins); this keeps Pass 2 near-zero-row on well-labeled specs whose ID and body sit on different lines. Matching: the bipartite matching of `refs/coverage-mapping.md` runs UNCHANGED for parsed rows; INF rows (which have no ID token to match) use the deterministic containment rule defined in `refs/coverage-mapping.md` (case-folded content-word containment, threshold 0.6, stopwords removed, single-task best match). Every matrix row carries `source: parsed | inferred`. Contract fields (per the §9.4 additive-evolution policy, contract 1.5.0): `coverage_pct` and `unmapped_requirements` KEEP their pre-D13 parsed-only semantics (no consumer impact); the NEW fields `coverage_pct_union` and `unmapped_requirements_union` carry the union numbers; `S_dev_density` (reflect-internal) uses the union denominator. Inferred rows are listed in the report under an `## Inferred requirements (Pass 2)` table (id, quote, citation, match result). Determinism boundary: Pass 1 and all matching stay LLM-free; inference is confined to Pass-2 enumeration, where every output is quote-pinned and policed by the Wave-5 evidence-validator (an inferred row whose quote does not match its cited lines is dropped AND `coverage_pct_union`, `unmapped_requirements_union`, and `S_dev_density` are recomputed before the report finalizes).

**Step 1B.1 (zero-task guard, UC-1).** Before any coverage-pct computation: if the parsed tasklist contains `total_tasks == 0` and mode is UC-1, STOP with `empty_input` flag and `status: partial`, return `coverage_pct: null` with `coverage_undefined: true` in the contract. Do NOT proceed to T1/T2.

**Step 1B.2 (coverage_undefined route).** If the spec/tasklist parse produces zero requirement IDs across BOTH passes (no `T-NNN`, no checklist items, no headings to map, and Pass-2 inference emitted zero valid rows), set `coverage_undefined: true`, route directly to T2 (no T1 stop possible), and surface in the report header. `coverage_pct` is not computed. The 0.90 T1 floor cannot pass vacuously (0/0 ≠ PASS).

**Step 1B.2b (parse-density guard, UC-1; D13 coverage hardening).** After Step 1B.0, when `inferred_count > parsed_count` (the spec's labeling is sparse relative to its requirement content), emit `coverage_degraded: parsed-sparse` in the report header, `tier_decision.yaml`, and the return contract, and FORBID the Tier-1 stop: the flag is a TABLE-WIDE pre-filter on §5.3 (no STOP row may fire while it is set; see the precedence paragraph after the §5.3 table), routing to Tier 2 (same loud-never-silent posture as the Step 1B.2 zero-ID route). Explicit user pins (`--tier 1`, `--depth quick`) override the pre-filter per §5.1 precedence, with a loud WARN naming the overridden flag. The guard compares row counts only; it never blocks the run and never alters the matrix.

**Step 1B.3 (cross-task interaction-effects scan, UC-2 tasklist-scope only).** When mode is UC-2 AND the tasklist contains ≥3 completed tasks, run the symbol-overlap scan:

1a. (FR-2) For each task's diff hunks, resolve each hunk's canonical declaration site via `mcp__serena__find_declaration` BEFORE deriving touched symbols — this anchors the overlap graph to resolved declarations rather than raw text, cutting false-positive overlap edges from name collisions. On zero matches for a hunk, emit `find_declaration_no_match`. Fail-open per §6.5.

1. For each task in the tasklist, derive its touched symbols via `mcp__serena__find_symbol` against the task's diff hunks.
2. Build a symbol-overlap graph: nodes = symbols, edges = "touched by task X and task Y." Cap at top-30 most-touched symbols (heuristic; full enumeration is bounded at 30 to control cost).
3. For each overlap edge, query `mcp__serena__find_referencing_symbols` to determine whether the symbol is genuinely shared or just transiently named the same.
3a. (FR-RV3-MED.1) When an overlap node is a **shared base-class symbol** flagged as a top-30 hotspot, AND the Wave-0 step 0.5d backend is hierarchy-capable AND `--with-hierarchy` is set, run `mcp__serena__type_hierarchy(hierarchy_type=subtypes)` on it to confirm **genuine shared lineage** (a real common supertype) rather than a name collision. A HIGH-severity interaction edge is raised for such a base class ONLY after this lineage confirmation. Backend not hierarchy-capable / `--with-hierarchy` unset → this sub-step is skipped (no degrade); the edge falls back to the step-3 `find_referencing_symbols` shared-vs-collision determination. Fail-open per §6.5.
4. For each confirmed interaction, check whether either task description explicitly cites the other (textual match on task ID). If neither cites the other, **flag as a cross-task interaction risk**.
5. Each risk becomes a synthetic invariant probe entry tagged `category: cross_task` (in addition to the existing 6 categories — see §11.2). Severity scales with the symbol's call-site count: HIGH if >5 referencing call sites, MEDIUM if 2-5, LOW if 1.

Emit `interaction_effects_scanned: true` in the contract when this step runs; `interaction_effects_scanned: false` when skipped (tasklist < 3 tasks OR mode == UC-1). This is the differentiating value of end-of-tasklist reflect — single-scope review misses interaction effects, and this is where reflect catches them.

### 4.3 Wave 3 — Detailed step addition

**Step 3B.0 (materialize per-reviewer brief packages).** Before spawning N reviewers, materialize one brief per reviewer at `<output>/reviewer-briefs/reviewer-<N>.md` containing: (a) T1 reflection card slice (the section relevant to this reviewer's persona); (b) reviewer-scoped grounding hunks (file:line excerpts from Wave 1A); (c) coverage-matrix slice (only the rows the reviewer is responsible for). Each brief is self-contained, so reviewers run truly in parallel without orchestrator round-trips.

(See `refs/reviewer-spec.md` for the brief template and worked examples.)

### 4.5 Wave 5 — Detailed step addition

**Step 5.0 (sc-adversarial pre-invocation probe and F1/F2/F3 fallback).** Before calling `Skill sc-adversarial-protocol`, probe its existence via `mcp__serena__list_memories` for the skill's existence indicator OR a no-op `Skill('sc-adversarial-protocol', args='--help')`. If the probe returns `skill not found`:

- **F1**: retry the probe once after a short backoff.
- **F2**: on second probe failure, use the highest-calibrated single Tier 2 reviewer verdict as the fallback merged result; mark `merge_method: single-reviewer-fallback`.
- **F3**: route to Tier 3 only if user explicitly opts in (`--remediate`); otherwise surface `adversarial_unavailable: true` and `status: partial`.

The fallback path is **loud, never silent**: every F-step writes to audit.log; the return contract carries `adversarial_unavailable: true`.

### 4.6 Wave 6 — Tier-3 remediation handoff (detailed step addition, FR-RV3-MED.3)

Wave 6 runs ONLY when `--remediate` is accepted (Tier 3). Acceptance is **interactive** (the yes/no opt-in prompt in `refs/remediation-handoff.md`) OR **headless auto-accept** (FR-9): under non-interactive `claude --print` (no TTY — the reflect-wrapper's launch mode), `--remediate` auto-accepts and authors the corrective MDTM WITHOUT the yes/no prompt for **AUTO-FIXABLE** registers (solely Drift/Necessary), while **HUMAN-REQUIRED** registers (any Regression, or `needs_human_decision: true`) author nothing auto-runnable and emit `remediation_task_path: null` (see `refs/remediation-handoff.md` "Headless auto-accept under `--print`"). Either way reflect AUTHORS but NEVER runs `/task` (§"Will Not"). Immediately BEFORE the task-builder invocation, reflect writes a warm-start handoff so the remediation conversation does not re-derive Waves 1-5 context.

**Step 6.0 (handoff write — BEFORE the task-builder spawn).**

1. **Build the handoff payload:** the in-flight rubric scores + deviation set + evidence packet + reviewer verdicts, keyed `reflect/handoff-{slug}-{timestamp}` (§6.3 schema).
2. **Persist (tool-presence-gated, OQ-M1):** if `prepare_for_new_conversation` is exposed in the active Serena context, write the blob via it (its signature confirmed by a live probe at adoption time — **never** wire an assumed parameter shape); emit `handoff_memory_written: true`, `handoff_memory_key: reflect/handoff-{slug}-{timestamp}`, `handoff_persist_method: prepare_for_new_conversation` to `audit.log` (FR-3.1).
3. **Fallback (the realistic default — tool context-excluded, FR-3.3):** write the same inline-built summary blob via `mcp__serena__write_memory` under the same key; emit `handoff_persist_method: write_memory_fallback`; still pass the key to task-builder.
4. **Both-fail (FR-3.4):** if both the tool AND `write_memory` fail, emit `handoff_persist_failed: true`, surface findings to task-builder WITHOUT the handoff key, and NEVER block the report.
5. **Pass the key forward:** invoke task-builder with the handoff key so it `read_memory`s the blob for a warm start.
6. **Capture + emit the authored MDTM path (FR-8):** AFTER the task-builder spawn returns, capture the absolute path of the MDTM file it wrote under `.dev/tasks/to-do/` (`refs/remediation-handoff.md`) and emit it as the §9.1 `remediation_task_path` field. This is the path-EMISSION only — reflect AUTHORS but NEVER runs `/task` (the §"Will Not" invariant is preserved); the reflect-wrapper auto-fix loop is the sole consumer that auto-runs it. Emit `remediation_task_path: null` in the degenerate / not-authored cases (the Authorized/Necessary-only short-circuit per `refs/remediation-handoff.md`, and the not-accepted `handoff_memory_key: null` case below).

**Degenerate no-op (FR-3.5):** when `--remediate` is NOT accepted (no Tier 3), Step 6.0 never runs, `handoff_memory_key: null`, and `remediation_task_path: null`. This is expected, not a failure.

The handoff write is ordered strictly BEFORE the task-builder spawn. The signature of `prepare_for_new_conversation` is unverified (OQ-M1) and the tool is absent in `claude-code`/`ide-assistant` contexts — the `write_memory` fallback is the default path and the implementer is directed to OQ-M1 resolution rather than wiring assumed parameters (FR-3.6).

---

## 5. Tier-Decision Rubric (Wave 2)

The rubric routes work to T1 or T2 by combining a calibrated confidence score with three structural signals. Numeric thresholds are concrete and documented; the rubric is the source of truth for escalation.

### 5.1 Hard overrides (no rubric evaluation)

| Override | Result |
|----------|--------|
| `--tier 1` | STOP at T1 (skip Wave 3+) |
| `--tier 2` | ALWAYS escalate to T2 |
| `--depth quick` | STOP at T1 |
| `--depth deep` | ALWAYS escalate to T2 |
| `--no-escalate` | STOP at T1 with warning if confidence < 0.85 |
| `confidence-calibrator` failed AND no inline fallback verdict | STOP at T1, mark `partial`, recommend re-run |

### 5.2 Rubric inputs

From Wave 1D calibration:

- `C` = calibrated confidence (0.00-1.00), arithmetic mean across 5 dimensions per `refs/reflection-rubric.md`
- Five dimensions: **Citation grounding**, **Coverage completeness**, **Deviation-classification clarity**, **Risk surface coverage**, **Recommendation actionability**

Structural signals from Wave 1B:

- `S_scope` — touched-file count from diff (UC-2) or tasklist-item count (UC-1)
- `S_domains` — distinct domains touched (code, infra, docs, tests, config — counted from file paths)
- `S_dev_density` — for UC-2 only: ratio of unmapped diff hunks to total hunks; for UC-1: ratio of unmapped spec requirements to total requirements (D13: computed over the UNION requirement set, parsed + inferred)

(See `refs/reflection-rubric.md` for full dimension definitions, scoring criteria, and the calibrator-selection algorithm with disjoint-set rule.)

### 5.3 Decision logic (applied in order; first match wins)

| # | Condition | Decision |
|---|-----------|----------|
| 1 | `C ≥ 0.90` AND `S_scope ≤ 5 files` AND `S_domains == 1` AND `S_dev_density ≤ 0.05` AND `coverage_pct ≥ <coverage-floor>` AND NOT `coverage_undefined` AND NOT `coverage_degraded` | **STOP at T1** — high confidence, narrow scope, single domain, near-zero ambiguity |
| 2 | `C ≥ 0.85` AND `S_scope ≤ 10 files` AND `S_domains ≤ 2` AND `S_dev_density ≤ 0.10` AND NOT `coverage_degraded` | STOP at T1 with WARN if `S_dev_density > 0.05` |
| 3 | UC-2 AND any single hunk classified as `Regression` candidate by Wave 1 | **ESCALATE** (regression must be debated by ≥2 reviewers; structural mechanism, not a confidence question) |
| 3a | UC-2 AND a Reuse-Miss at rung L3 mapped to Drift or Regression (§10.8) | **ESCALATE** (a shipped high-confidence duplicate is debated by ≥2 reviewers — same asymmetric-cost logic as rule 3 Regression) |
| 4 | `S_domains ≥ 3` | ESCALATE (multi-domain reflection cannot be reliably done by a single reviewer card) |
| 5 | `S_dev_density > 0.20` | ESCALATE (too many unmapped artifacts for a single-pass verdict) |
| 6 | `C < 0.85` | ESCALATE |
| 7 | `--strategy enterprise` set on caller | ESCALATE (enterprise default per sc-brainstorm convention) |
| 8 | Default | STOP at T1 |

Default `<coverage-floor>` is **0.90**. `--coverage-floor 0.95` is an optional high-safety override.

**Pre-filter precedence (D13).** `coverage_undefined` and `coverage_degraded` are TABLE-WIDE pre-filters, not row conjuncts alone: when either flag is set, NO STOP row (1, 2, or the row-8 default) may fire and the run routes to Tier 2; the row-1/row-2 conjuncts are redundant safeties, the pre-filter is authoritative. Explicit user pins outrank the pre-filter: `--tier 1`, `--depth quick`, and `--no-escalate` (all §5.1) proceed at the pinned tier and emit a loud WARN naming the overridden flag; the §5.1 calibrator-failure row also proceeds at T1 but already forces `status: partial` with a re-run recommendation, and its WARN names the degraded flag too. The coverage-floor comparison in row 1 reads `coverage_pct` (parsed semantics, §9.1).

### 5.4 tier_decision.yaml audit artifact (composite-score recording)

V2's priority-rule logic (§5.3) is the deciding mechanism. V5's 5-signal composite_score is recorded in `<output>/artifacts/tier_decision.yaml` for audit visibility:

```yaml
selected_tier: 1 | 2
fired_rule_number: <int>           # which §5.3 rule fired (deterministic first-match)
coverage_degraded: <string> | null # "parsed-sparse" when the Step 1B.2b guard fired (D13); table-wide pre-filter, explains a forced T2 regardless of which STOP row would have fired
composite_score: <float 0-10>      # V5 5-signal sum
per_signal_breakdown:
  scope_size: <0-2>
  task_count: <0-2>
  blast_radius: <0-2>
  spec_density: <0-2>
  ambiguity_signals: <0-2>
escalation_reason: <string>        # human-readable rationale
```

Grader `yaml_field` asserts both `fired_rule_number` and `composite_score` are present. The composite is *recording*, not deciding.

### 5.5 Why these thresholds

- `0.90` for the strict T1 ceiling matches CLAUDE.md global rule 3 (≥90% confidence to proceed without alternatives). Reflection findings that the reviewer is willing to call ≥0.90 *and* narrowly-scoped *and* single-domain are the cases where ensemble verification is not cost-justified.
- `0.85` is the medium-confidence floor inherited from sc-troubleshoot's Wave 2 gate.
- `S_dev_density > 0.20` is the "structural ambiguity" trigger — at one in five unmapped artifacts, a single reviewer cannot adjudicate without ensemble pressure.
- Regression candidacy at rule 3 is non-negotiable because asymmetric cost: shipping a missed regression is far worse than spending T2 tokens debating one.

### 5.6 Escalation reason logging

The matching rule number + numeric values are written to the audit log:

```
escalation_decision:
  tier_reached: 2
  rule_matched: 3
  confidence_calibrated: 0.91
  S_scope: 8
  S_domains: 2
  S_dev_density: 0.07
  regression_candidate_count: 1
  reason: "regression_candidate_requires_debate"
```

---

## 6. Modern Serena Tool Usage

The protocol replaces every `think_about_*` invocation with a concrete symbol-anchored evidence chain. The `think_about_*` triad is *current* (not deprecated) but is positioned here as scripted mandatory checkpoints, not the load-bearing reflection mechanism.

### 6.1 Mandatory evidence-gathering chain (Wave 1A)

For every touched file in UC-2, or every spec-referenced module in UC-1:

```
1. mcp__serena__activate_project (once, idempotent at Wave 0)
2. mcp__serena__get_symbols_overview <file>            # structural map
2a. mcp__serena__find_declaration <symbol>            # diff-hunk → declaration
3. mcp__serena__find_symbol <relevant-symbol>          # symbol body
3b. mcp__serena__find_implementations <symbol>         # polymorphic surface
4. mcp__serena__find_referencing_symbols <symbol> include_info:true   # downstream impact + signatures
4a. Task(reuse-auditor, candidates=<new/body-changed symbols from 2a/4, ≤12>, stage=post, repo_root, output_path=<output>/artifacts/reuse-audit.yaml)  # FR-REUSE.1 — outward reuse/consolidation neighbour search
    → agent RETURNS findings; orchestrator persists them to output_path, then consumes reuse-audit.yaml
      (per-candidate verdict/tier/neighbours; run-level max_overlap/degraded/sampled). stage=post is fixed here
      (Wave 1A is the UC-2 post-execution chain); the pre-stage path lives in /tdd step 2a. Path matches
      `reuse_audit_path` in the output schema below.
    Orchestrator-level (Wave 1A, Tier 1) — NEVER nested inside a spawned subagent.
    Fallback: agent unavailable → inline serena+ripgrep grep-skeleton degrade, findings CAPPED at advisory L2,
    degraded_components += "neighbour-search:auggie_unavailable"; NEVER STOP.
4.5. mcp__serena__type_hierarchy(hierarchy_type=both|subtypes, depth=0)  # transitive family (backend+--with-hierarchy gated)
5. mcp__serena__get_diagnostics_for_file <file>        # LSP-level issues
5.5. mcp__serena__execute_shell_command (scoped verify) # UC-2 verification triangle (safety envelope §6.1.1)
6. Re-Read each cited file:line range before quoting    # citation-grounding
7. mcp__serena__find_symbol <symbol> search_deps:true   # third-party / dependency surface
7'. mcp__serena__summarize_changes   # UC-2 corroboration vs supplied diff
```

Step 2a (FR-2) resolves a diff hunk to its canonical declaration site before symbol lookup; on zero matches it emits `find_declaration_no_match`. Step 3b (FR-1) enumerates the polymorphic surface and fires for `kind ∈ {Interface, AbstractMethod, Protocol, Trait, Class}` — `Class` is **included** (C3) because non-Python LSPs report `Class` for traits/Protocols; on a `Class` a non-empty result IS the implementor surface and an empty result is "genuinely none" (no degrade). Both new steps are fail-open per §6.5 and emit one `audit.log` row each per the §4 per-step convention.

Step 4's `include_info: true` (FR-3) is a **parameter add to the existing call, not a new step**: the v1.5 "Extended Symbol Information" return shape absorbed the old standalone referencing-snippets tool, so the referencing scan now also yields each referrer's signature/docstring. The run emits `references_extended_info_used: true` to `audit.log`, and the Wave-0 tool-inventory probe (OQ-1, via `serena_info` / `get_current_config`) records to the audit whether that defunct standalone referencing-snippets tool is present — the protocol uses the `include_info` path regardless and never wires the standalone tool.

Step 7 (FR-4) is **conditional**: it fires only on the operationalized trigger predicate — a symbol whose step-2a `find_declaration` resolves to an `<ext:…>` path (a third-party dependency), NOT the vague "cites a third-party API by name". When the LSP has not indexed the dependency (no active venv / unindexed package), it fails open to `degraded_components: ["search_deps:lsp_unindexed"]` and the dependent claim stays marked `[INFERRED]` rather than `[VERIFIED]`. It emits one `audit.log` row per the §4 convention.

Step 7' (FR-5) is **UC-2-only** and **prompt-based** (a corroboration meta-tool, NOT a computed diff — it returns instructions to summarize the session's changes, still model-mediated). It is **session-aware**: it must be invoked in the SAME MCP session as the edits; on a cross-session reflect (fresh session, nothing to summarize) it sets `serena_summary_corroboration: unavailable` and the main verdict is unchanged (FR-5.4). It sets `serena_summary_corroboration` ∈ `{agree, partial, disagree, unavailable}` by comparing the Serena change-summary against the supplied diff. It emits `summarize_changes_invoked: true` and `summarize_changes_path: <output>/serena-change-summary.md` to `audit.log` per the §4 per-step emit convention (SKILL.md per-step audit row) — the same way steps 3b/7 emit their own `<tool>_invoked` rows — so the FR-5 telemetry has an explicit producer in the chain. FR-5 **ships last** and is **pilot-gated** (OQ-3 — its signature is "not surfaced"; treat as zero-arg until the eval-workspace pilot probes the return shape).

Step 4.5 (FR-RV3-MED.1) retrieves a type's **transitive supertype/subtype family** in one call. It runs ONLY when (a) the Wave-0 step 0.5d backend probe reports a hierarchy-capable backend, (b) `--with-hierarchy` is set, and (c) the located symbol is a type (FR-1.1). Backend `none`/`lsp-disabled` → skip with `type_hierarchy_invoked: false` and **NO degrade** (expected absence, FR-1.4). An explicit backend error (distinct from "unsupported") → `degraded: ["type_hierarchy:backend_error"]` and fall back to the `find_implementations`/`find_referencing_symbols` chain (FR-1.5). `--with-hierarchy` defaults OFF on `lsp` (no generic `type_hierarchy` tool there until OQ-M3 confirms per-language support) and is unavailable on `none`; non-OO codebases see zero degradation. The skill MUST never abort because hierarchy is unavailable.

Step 5.5 (FR-RV3-MED.4) is the **verification triangle** — `get_diagnostics_for_file` (step 5, LSP issues) + `summarize_changes` (step 7', what changed) + `execute_shell_command` (step 5.5, does it pass). It is **UC-2 default-on** and gated: it runs only when `execute_shell_command_available` is true (Wave-0 step 0.5d), `read_only` is not set, and `--no-verify` was not passed; otherwise it skips with the matching `verification_skip_reason` and degrades §10.4 Regression detection to the task-log claim with a Grounding Gap entry (never STOP). Every invocation is governed by the consumer-side safety envelope specified in §6.1.1 below. It emits one `audit.log` row per the §4 per-step convention whose `evidence_ref` points at the per-invocation artifact.

Step 4a (FR-REUSE.1) is the **outward reuse/consolidation neighbour search** — the inverse of the inward symbol-walk above. For each new/body-changed symbol (incl. new files), it delegates to the `reuse-auditor` agent (§7), which fingerprints behaviour (capability + skeleton, name-agnostic), fires one capability-keyed auggie query per candidate (cap ≤12/run; overflow → `neighbour_search_sampled: true`), re-Reads each returned neighbour `file:line` before citing it (§6.2), and returns `reuse-audit.yaml` (per-candidate `tier`/`verdict`/composite-scores + run-level `max_overlap`). It is invoked at **orchestrator / Tier-1 level only** — never inside an already-spawned subagent (subagent→agent nesting can fail). The agent returns *findings only*; the skill maps each `confident-duplicate` onto §10.8 Reuse-Miss (Drift/Regression by evidence) and routes `maybe-related`/insufficient-grounding to §10.6 Grounding Gaps. Fail-open: agent or auggie unavailable → inline serena+ripgrep grep-skeleton, findings CAPPED at advisory L2, `degraded_components += "neighbour-search:auggie_unavailable"`; NEVER STOP. Emits one `audit.log` row (`reuse_sweep_invoked`, `candidates_scanned`, `neighbours_found`, `max_overlap`) per the §4 per-step convention.

The chain replaces "think_about_collected_information" — instead of asking the model to self-assess whether it has enough info, the protocol *produces* the evidence and lets the rubric score whether grounding is sufficient.

### 6.1.1 `execute_shell_command` safety envelope (FR-RV3-MED.4)

`execute_shell_command` runs **non-mutating verification only** (tests/linters/type-checkers/build). Serena executes the command via `subprocess.Popen(command, shell=True)` with **no upstream allowlist or sandbox** (Serena Security Audit #380), so the entire safety envelope is **consumer-side**. A first-token allowlist is *necessary but not sufficient* — under `shell=True` an allowlisted first verb still permits a chained mutation (e.g. `pytest ; rm -rf src`). The envelope therefore validates the **whole command structure**, not just the first token. All nine controls are mandatory:

- **(a) Template construction, not prose assembly.** The command MUST be built from a fixed allowlisted-verb template with arguments supplied as a vetted token list. The command string is NEVER assembled from raw spec/tasklist prose (untrusted by definition).
- **(b) Verb allowlist.** The first token MUST be in `{pytest, ruff, mypy, make, uv, npm, tsc, cargo}`; otherwise the command is rejected with `verify_blocked: true` + `verify_blocked_reason: "verb '<v>' not in allowlist"` and is **not** invoked. The allowlist is checked against the **base** verification command's first token, NOT against the fixed protocol-added `timeout` / `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` wrapper prefix from controls (d)/(i) — those wrappers are protocol-authored, never user-supplied verbs, so `timeout` and `env` are never themselves allowlisted as selectable verbs.
- **(c) Structural metacharacter rejection (the load-bearing C1 control).** Reject outright with `verify_blocked: true` + `verify_blocked_reason: "metachar-denied"` any command containing a shell control character — semicolon `;`, pipe `|`, ampersand `&`, dollar `$`, backtick `` ` ``, redirect `>` / `<`, newline, or parentheses `(` `)`. This validates the whole command structure; a denylist of mutation *verbs* alone is insufficient against `shell=True` composition. Such a command is **never** passed to `execute_shell_command`.
- **(d) Per-call timeout.** Wrap every command as `timeout <N> <cmd>` with default **120s, max 600s** (Serena's tool-level timeout is unverified, so the wrap is consumer-side). A timeout kills the command, records `exit_code: 124` + `verify_timeout_hit: true`, classifies it Grounding Gap, and the run continues.
- **(e) Output cap.** Pass `max_answer_chars=51200` (50 KB, tighter than the 200 KB Serena default) plus a defensive tail-truncate of captured stdout/stderr.
- **(f) `cwd` scoping.** Scope `cwd` to the affected subtree (blast-radius reduction).
- **(g) Per-invocation audit artifact (M-ARC1).** Each invocation is appended to `<output>/verify-logs/invocations.yaml` as an array entry `{cmd, exit_code, duration_ms, stdout_path, stderr_path, blocked_reason, deviation_class}`. The step-5.5 audit row references this artifact via its `evidence_ref` field — the per-invocation data is **NEVER inlined** into the fixed 5-field per-step audit row.
- **(h) `--no-verify`.** Disables the verification triangle globally (`verification_skip_reason: --no-verify`).
- **(i) Wrapper-marker strip (verification subprocess only).** After the base verification command passes controls (a)–(c) and the no-mutation gate, the step-5.5 invocation MUST be executed as the fixed protocol-authored wrapper `timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <validated base command>`, so the verification subprocess does NOT inherit `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` from a parent reflect-wrapper run. Without this strip, a verification command that itself invokes `superclaude reflect run` (e.g. the reflect CLI's own tests) trips the `commands.py` recursion-breaker guard and self-suppresses, producing a false degraded/null-convergence outcome on a clean audit. This strip applies **only** to the non-mutating verification/build/test subprocess class governed by this envelope. It does **NOT** authorize clearing, unsetting, or overwriting the marker for reflect audits, emitted reflect gate commands, or auto-run corrective `/task` execution — those children MUST keep `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` so nested-gate suppression remains intact. `env -u` here is a fixed wrapper prefix, **not** a user-selectable allowlisted verb (control (b) still validates the base command's first token). The strip preserves controls (d)–(h): the `timeout <N>` wrap from (d) remains the outer wrapper, the executed command is recorded in `<output>/verify-logs/invocations.yaml` per (g), and when `--no-verify` (h) disables the triangle no marker-stripping wrapper runs at all.

**No-mutation gate.** Independently of (b)/(c), any command matching the mutation denylist (`git commit`/`git push`, `pip install`, `rm`, or any redirect to a repo path outside `<output>/`) is rejected with `verify_blocked_reason: "mutation-denied"` and never invoked. In-test side effects (a test that writes fixtures within its own scope) are best-effort only (OQ-M7) — the gate governs the *command*, not the test internals.

### 6.2 Citation-grounding via re-Read (anti-staleness)

Per CLAUDE.md "Context freshness discipline" S1: before any `file:line` citation enters a draft report, the orchestrator MUST have Read the source file within the last 5 tool calls. The hook layer enforces this at edit time but not for chat citations — the protocol enforces it explicitly by inserting a re-Read step immediately before Wave 5 evidence-validator hands off.

### 6.3 Memory pattern (per-project, expiring)

```
mcp__serena__read_memory  key=reflect/last-pass-{project-slug}      # Wave 0 hydrate
mcp__serena__read_memory  key=reflect/deviation-patterns-{slug}     # Wave 1 (recurring deviation signals)
mcp__serena__write_memory key=reflect/last-pass-{slug} value=<summary>  # Wave 5 persist
mcp__serena__write_memory key=reflect/deviation-patterns-{slug} value=<merged>  # Wave 5 persist
mcp__serena__prepare_for_new_conversation → reflect/handoff-{slug}-{timestamp}   # Wave 6 (when --remediate; write_memory fallback)
mcp__serena__list_memories                                          # Wave 0 inventory
```

Retention rule: keep last 20 entries per key; expire >90 days. Project slug derived from `pwd` basename.

**Handoff schema (`reflect/handoff-{slug}-{timestamp}`, FR-RV3-MED.3).** A Tier-3 bridge memory written at Wave 5/6 — immediately BEFORE the Wave-6 task-builder handoff — carrying the in-flight context the remediation conversation would otherwise re-derive: **rubric scores + deviation set + evidence packet + reviewer verdicts**. It uses the `reflect/<category>-{slug}[-{timestamp}]` naming consistent with the existing `reflect/last-pass-*` / `reflect/deviation-patterns-*` keys. It is written via `prepare_for_new_conversation` when that tool is exposed, **falling back to `mcp__serena__write_memory`** with an inline-built summary blob when the tool is context-excluded (the realistic default — see §4.6 and §14). The `reflect/handoff-*` prefix is included in the retention sweep prefix set (the sweep itself is the low-spec FR-RV3-LOW.8 implementation — see the cross-spec note below).

**Retention sweep (Wave 5/0, FR-8).** The retention rule above was previously specified but unimplemented (`write_memory` accumulated without pruning). At Wave 5 (persist) — or Wave 0 if the prior run never swept — run the CRUD sweep over **Serena memory blobs** (NOT project source):

```
mcp__serena__list_memories                                  # inventory + slug filter
mcp__serena__delete_memory  name=<expired-or-over-cap slug> # prune deletable entries
mcp__serena__rename_memory  old=<slug> new=<migrated-slug>  # slug migration (mem: refs propagate, v1.5+)
mcp__serena__edit_memory    name=<slug> patch=<merge>       # merge/dedupe overlapping entries
```

Sweep rules:

- **Version gate (C2).** `rename_memory`'s `mem:` cross-reference propagation requires Serena **v1.5+**. When `serena_version ∈ {"<v1.5", "unknown"}` (recall `unknown` is treated as `<v1.5`), run **write-only / no-retention**: skip `rename_memory` propagation (renaming would silently break `mem:` refs), and emit `degraded_components: ["serena:pre-v1.5-no-rename-propagation"]`.
- **Unbounded-gap loud flag (C1).** The retention invariant is "keep last 20 **deletable** entries" — read-only entries (those matching `read_only_memory_patterns`) are EXCLUDED from the budget. When `slug_count > 20` AND `(slug_count − readonly_count) ≤ 20` after the sweep (the total exceeds the 20-entry budget but the deletable entries alone are within it, so read-only entries are what make the ≤20-total target unreachable), emit `memory_retention_unbounded: true` and a WARN to `audit.log` (loud, never silent) rather than deleting read-only entries.
- **Zero / degenerate case (C4).** On the first-ever run (no slug memories) or an all-stale set, still emit the sweep-invoked flag with all-zero action counts. The **current-pass entry is protected from the age sweep**: order the Wave-5 `write_memory` AFTER the sweep, or exclude the current pass by recency rank, so a >90-day all-stale sweep never deletes the entry just written.
- **Slug sanitization.** Derived slugs MUST contain no `..` (Serena v1.2.0 path-traversal guard rejects them); sanitize before any CRUD call.
- **Read-only respect.** Never delete or rename entries matching `read_only_memory_patterns`.
- **Handoff-prefix membership (FR-3.7 / M-ARC2).** The sweep prefix set includes `reflect/handoff-*` (alongside `reflect/last-pass-*` and `reflect/deviation-patterns-*`), so FR-3's Wave-6 handoff memories are pruned under the same 90-day-expire / 20-entry-cap policy and do NOT accumulate unbounded across `--remediate` runs. The sweep implementation is the low-spec FR-RV3-LOW.8 mechanism; this records the required prefix extension (cross-spec coordination — see the dependency record).

Every CRUD action is fail-open per §6.5 and emits one `audit.log` row per the §4 per-step convention; the sweep records `memory_retention_actions`, `memory_retention_skipped_readonly`, and `memory_retention_unbounded` to §9.2 telemetry. This sweep mutates Serena memory blobs ONLY — it never touches project source.

### 6.4 `think_about_*` as scripted checkpoints (not load-bearing)

The `think_about_*` tools are cheap meta-cognition prompts. They are wired in as *mandatory scripted nudges*, with their output recorded in the audit log but never used as the load-bearing signal:

| When | Tool | Purpose |
|------|------|---------|
| End of Wave 1A | `think_about_collected_information` | Cheap sanity nudge after evidence-gathering chain — if model surfaces a gap, log it and influence rubric `S_dev_density` upward |
| End of Wave 1C | `think_about_task_adherence` | UC-1 mode only — cheap nudge before calibration |
| End of Wave 5 (after evidence-validator) | `think_about_whether_you_are_done` | Final completion nudge; result logged but does NOT gate ship (evidence-validator gates ship) |

These are scripted, not optional. Their output is captured to `<output>/serena-checkpoints.log` for audit. They are not the reflection — they are a free 200-token nudge layered on top. **They are NOT listed in frontmatter `allowed-tools`** (declaring them as protocol surface would overweight their role).

### 6.5 Fail-open policy

Every Serena call is fail-open per `sc-validate-roadmap-protocol` convention. Missing Serena → fall back to `Grep`/`Glob` with `degraded: true` in the audit. The protocol must never abort because Serena is unavailable.

---

## 7. Agent Delegation Map

Every reusable agent is mapped to a wave; no agent is duplicated inline.

| Agent | Wave | Mode | Role | Fallback |
|-------|------|------|------|----------|
| `root-cause-analyst` | 1C | UC-2 | Investigate any deviation candidate found in Wave 1B; produce hypothesis card with `deviation_class` field | Inline orchestrator card |
| `self-review` | 1C | UC-2 (low-stakes) | Cheap 4-question completion pass (tests / edge cases / requirements / rollback) when `S_scope ≤ 3 files` AND `--depth quick` | Inline 4-question template |
| `requirements-analyst` | 1B | UC-1 | Build the spec-to-tasklist coverage map via the Step 1B.0 two-pass extraction (regex Pass 1 + quote-pinned inference Pass 2, D13); surface unmapped requirements across the union set | Inline orchestrator analysis |
| `confidence-calibrator` | 1D, 3C | both | Blind re-grade per the 5-dim reflection rubric; the dominant anti-anchoring mechanism (calibrator-model ≠ reviewer-model class — see §11.3 disjoint-set rule) | Inline orchestrator calibration with `calibration: inline-fallback` marker |
| `rf-qa` | 3B | UC-2 (structural) | Adversarial-stance structural QA on diff hunks; runs with `fix_authorization: false` (reflection never auto-fixes) | Inline orchestrator pass on `S_scope ≤ 3` |
| `rf-qa-qualitative` | 3B | UC-2 (documents) | Adversarial-stance content-level QA when the artifact under review is a document (PRD, TDD, tech-ref) | Skip; UC-2 still runs with `rf-qa` only |
| `audit-validator` | 5 | UC-2 (large) | When Wave 5 produces ≥20 findings, 10% random spot-check before report ships (lighter alternative to full evidence-validator pass) | Evidence-validator alone (more expensive but stricter) |
| `evidence-validator` | 5 | both | **Non-negotiable final gate**; re-Reads every cited file:line; drops unfounded items | Inline validation with `status: partial` and "validator unavailable" Grounding Gap |
| `task-builder` (skill, not agent) | 6 | UC-2 (post-execution remediation) | Generate corrective MDTM task file from reflection findings | None; surface findings without remediation |
| `socratic-mentor` | 1C | UC-1 (deep) | Optional probing pass for `--depth deep` UC-1 when spec is ambiguous | Skip |
| `reuse-auditor` | 1A | both | Detect reuse/consolidation prior art for new/changed symbols (post) or proposed components (pre); fingerprint behaviour name-agnostically and return findings (verdict + tier + grounded neighbours) — **detection only, never classifies deviations or gates** | Inline grep-skeleton degrade (advisory-capped) |

(See `refs/reviewer-spec.md` for the brief template and reviewer composition rotation details.)

### 7.1 Reviewer composition rules (Wave 3A)

Reviewers are heterogeneous by model class AND by persona, to maximise representational diversity (Wisdom of Silicon Crowd, LLM-TOPLA). Reviewer counts are clamped by the §4 Wave 0 alias-routing table.

**Executor-class exclusion rule (anti-self-confirmation, structural).** The *executor* (the agent whose work is under review) MUST NOT appear in the reviewer pool. Reflect resolves the executor's model class at Wave 0 step 0.5b (a new sub-step inserted between alias resolution and reviewer composition) from `--executor-model <class>` flag, the `EXECUTOR_MODEL_CLASS` env var, or — if neither is set — from the most-recent commit-author hint in the task log (heuristic; emit `executor_class_source: flag | env | log-heuristic | unknown` to telemetry). When the executor's class is in the candidate rotation, it is **removed** from the rotation; if removal drops reviewer count below the gate floor (N=2 minimum for T2), reflect emits `executor_exclusion_degraded: true` and degrades to T1 with WARN: `"executor class collides with reviewer pool; N=2 floor cannot be satisfied with disjoint set."` This rule extends the §11.3 disjoint-set principle (calibrator class disjoint from reviewer classes) to also separate **executor class from reviewer classes** — the three classes (executor, reviewers, calibrator) form a partition where collisions weaken the structural anti-self-confirmation guarantee.

When `executor_class_source == unknown` (no flag, no env var, no log hint), reflect proceeds with the standard rotation and emits `executor_class_resolved: false` + WARN: `"executor class not resolved — anti-self-confirmation guarantee weakened; pass --executor-model to enforce."` This is fail-open by design: missing executor identity is not a STOP condition, but the weakened guarantee is logged loudly.

| Reviewer count | Model rotation (BEFORE executor-class removal) | Persona rotation |
|----------------|----------------|------------------|
| 2 (`--reviewers 2`) | sonnet, haiku | analyzer, qa |
| 3 (default) | sonnet, haiku, (qwen \| kimi \| deepseek if alias available; else opus) | analyzer, qa, refactorer |
| 3 with `--strategy enterprise` | sonnet, haiku, opus | analyzer, qa, architect |

Post-removal: if the executor is `sonnet`, the N=3 default rotation becomes `haiku, (qwen|kimi|deepseek|opus)` and reflect adds the next-available class from the resolved alias set to restore N=3, or degrades to N=2 if no replacement is available. The N=2 minimum is hard — below it, T2 cannot fire.

The merge judge in Wave 4 is `sc-adversarial-protocol`'s internal scoring; per Khan et al. ICML 2024 Oral, the judge being a *different* class than the debaters is the right default. The protocol does not pin a judge model — sc-adversarial owns that selection.

### 7.2 New-agent discipline (one introduced: `reuse-auditor`)

The four hypothetical new agents discussed in enrichment notes (`coverage-mapper`, `deviation-classifier`, `tasklist-vs-diff-comparator`, `reflection-synthesizer`) are *deliberately not introduced* in this variant. Their work is absorbed:

- Coverage-mapping work → `requirements-analyst` agent (UC-1) + inline Wave 1B logic (UC-2).
- Deviation classification → driven by `refs/deviation-taxonomy.md` and applied by `root-cause-analyst` per-card; the taxonomy *is* the classifier.
- Tasklist-vs-diff comparison → inline Wave 1B (`git diff` parse + tasklist parse + bipartite match).
- Reflection synthesis → inline Wave 5 (mirrors sc-troubleshoot's inline Wave 5; new agent introduces bloat without value).

Rationale: keeping the SKILL.md within the sc-troubleshoot/sc-brainstorm band requires keeping inline logic *only* where the inline logic is templated. Where the work is open-ended hypothesis or judgement, agents stay. Where the work is mechanical mapping, inline stays.

**The one new agent — `reuse-auditor` — clears exactly that bar.** Note `deviation-classifier` was rejected above precisely because deviation classification *is* mechanical mapping (the §10 taxonomy is the classifier). Reuse/consolidation detection is the opposite: deciding "do these two symbols do the same thing despite zero shared name tokens?" is **semantic capability/skeleton equivalence** — open-ended judgement, not a lookup. It is also an `extract-shared` unit by its own §4 N≥2 rule: both `sc:reflect` (Wave 1A) and `/tdd` (Stage A.3) consume it, and skill-packaged refs can't be shared across skills, so the detection algorithm lives in one globally-addressable agent rather than being duplicated into each SKILL (cf. `evidence-validator`, "reusable by any skill"). Introducing it is the feature taking its own advice; the gate integration (§10.8 mapping, §14.5.2) stays inline — the agent relocates *detection*, not *gating*.

---

## 8. Cross-Skill Integration

| Skill | When | Why |
|-------|------|-----|
| `sc-adversarial-protocol` (Mode A `--compare`) | Wave 4 (T2 only) | Merge 2-3 reviewer cards into one verdict via the established debate + scoring + merge pipeline. Reflect does NOT re-implement debate. |
| `task-builder` | Wave 6 (T3 only) | Generate corrective MDTM task file from reflection findings; gated on user opt-in. |
| `confidence-check` (skill) | Before any actionable recommendation in Wave 5 chat surface | CLAUDE.md global rule 3 — confidence ≥0.90 to proceed, 70-89% present alternatives, <70% ask. |
| `tech-research` | Wave 1B (optional, `--depth deep` only) | When the spec references frameworks/libraries by name, fetch current best-practice docs (UC-1) or current best-practice patterns to score the implementation against (UC-2). |
| `evidence-validator` (agent, but skill-level dependency) | Wave 5 | Mandatory final gate (see §11.2). |
| `sc-troubleshoot-protocol` | (Reverse direction — sc-troubleshoot invokes us in its Wave 6 Phase B/D) | Pre-exec + post-exec validation of `/task` runs. |

Invocation pattern (all via `Skill <name>`, never `/sc:<command>`):

```
Skill sc-adversarial-protocol with \
  --compare <output>/reviewer-cards/card-1.md,card-2.md,card-3.md \
  --depth standard \
  --focus correctness,coverage,deviation-classification \
  --output <output>/adversarial/
```

Empty-response / partial-parse / missing-file guards apply per `sc-brainstorm-protocol/SKILL.md:280-285` — no synthetic 0.5 fallback; FAIL if response is unparseable or merged_output_path file does not exist on disk. Convergence routing: ≥0.75 PASS, ≥0.60 PARTIAL, <0.60 FAIL.

**Consumer-side field-name remap (`artifacts_dir` → `adversarial_artifacts_dir`).** When reflect Wave 4 consumes sc-adversarial-protocol's output, the producer emits its result-directory path under the field name `artifacts_dir` (sourced from `sc-adversarial-protocol/SKILL.md:435,453,2097`). Reflect's own return contract, however, exposes that same path under the field name `adversarial_artifacts_dir` (per §9.1 stable contract). Reflect MUST perform a mechanical key-rename at the parse boundary: read `artifacts_dir` from the sc-adversarial JSON, then write `adversarial_artifacts_dir` into the merged return contract. This is a concrete consumer-side remap, NOT an open question or a producer-side rename request — sc-adversarial's emitted field name is the source-of-truth and reflect adapts to it.

**Null `convergence_score` handling (F3 path / adversarial-unavailable).** When `adversarial_unavailable: true` (Wave 5 step 5.0 F3 path), `convergence_score: null` enters the return contract. Downstream consumers (sprint, sc-troubleshoot, task) and the §14.5.2 promotion gate MUST treat `null` as a distinct state, NOT silently route as `< 0.60` or `≥ 0.75`:

- The contract requires consumers to route on `merge_method` FIRST: if `merge_method == single-reviewer-fallback`, treat `convergence_score` as inapplicable and use the single-reviewer verdict's calibrated confidence as the routing input instead.
- A null comparison (`null < 0.60`, `null ≥ 0.75`, etc.) is undefined behavior — implementations MUST guard against it explicitly.
- For the promotion gate: per §14.5.2 condition 9, `tier_reached == 2 AND convergence_score == null` blocks promotion regardless of other conditions. A Tier 2 run with no merged adversarial verdict cannot promote.
- For non-promotion routing (e.g., sprint executor.py status routing): null `convergence_score` translates to `status: partial` AND `next_action: halt-phase-for-review`. Consumers MUST NOT route a null as a default-PASS or default-FAIL.

---

## 9. Output Contract (Versioned)

Two-block contract: stable + telemetry. Written to `<output>/return-contract.yaml` AND returned inline. (See `refs/report-template.md` for the human-facing REPORT.md skeleton that renders these fields.)

### 9.1 Stable contract (contract_version: 1.5.0)

```yaml
contract_version: "1.5.0"   # 1.4.0 added remediation_task_path (FR-8); 1.5.0 (D13) ADDITIVE ONLY: +coverage_pct_union, +coverage_degraded, +unmapped_requirements_union; coverage_pct and unmapped_requirements keep parsed-only semantics
status: success | partial | failed | dry-run
mode: pre | post
tier_reached: 1 | 2 | 3
report_path: <abs path to REPORT.md>
audit_log_path: <abs path>
confidence_calibrated: <float 0.00-1.00>
escalation_rule_matched: <int 1-8> | null
onboarding_ran: <bool>                # FR-2 (Wave 0.7b one-shot --onboard bootstrap; false when gated off)

# UC-1 specific
coverage_pct: <float 0.0-1.0> | null            # PARSED-ONLY denominator; pre-D13 semantics UNCHANGED (consumer-safe per the 9.4 additive policy)
coverage_pct_union: <float 0.0-1.0> | null      # NEW (1.5.0, D13): union denominator (parsed + inferred rows) per Step 1B.0; reflect-internal gates read this
coverage_undefined: <bool>           # true when no parseable requirement IDs across BOTH extraction passes
coverage_degraded: <string> | null   # NEW (1.5.0, D13): "parsed-sparse" when inferred_count > parsed_count (Step 1B.2b); table-wide T1-stop pre-filter
unmapped_requirements: [<list>]                 # PARSED-ONLY; pre-D13 semantics unchanged
unmapped_requirements_union: [<list>]           # NEW (1.5.0, D13): union set incl. unmatched INF-NNN rows
best_practice_grade: <int 0-5> | null
implementation_coverage_pct: <float 0.0-1.0> | null   # FR-1 (null when the kind-guard never fired — C5)
missing_implementations:                              # FR-1
  - abstract_name_path: <string>
    expected_count: <int>
    found_count: <int>
hierarchy_slice_path: <abs-path> | null               # FR-RV3-MED.1 (<output>/artifacts/hierarchy-slice.yaml; null when unavailable)
hierarchy_coverage_pct: <float 0.0-1.0> | null        # FR-RV3-MED.1 = registered_subtypes / total_subtypes_in_hierarchy; null when hierarchy empty or backend unavailable

# UC-2 specific
tasklist_completion_pct: <float 0.0-1.0> | null
deviation_count_by_class:
  authorized: <int>
  necessary: <int>
  drift: <int>
  regression: <int>
deviation_register_path: <abs path> | null
grounding_gaps_path: <abs path> | null    # parallel artifact for evidence-insufficient findings
hunk_to_declaration_map_path: <abs path>   # FR-2 (UC-2 only)
third_party_api_grounding:                 # FR-4
  - api_name: <string>
    dep_version: <string>
    resolution_path: <string>
third_party_api_verified: <bool>           # FR-4
serena_summary_corroboration: agree | partial | disagree | unavailable   # FR-5
verification_ran: <bool>                   # FR-4 (UC-2 verification triangle, §6.1 step 5.5)
verification_invocations: <int>            # FR-4 (count of verify-log invocation entries)
verification_failures: <int>               # FR-4 (exit_code != 0 count)
verification_regressions_detected: <int>   # FR-4 (taxonomy-classified Regression exits on a claimed-passing file)
verification_skip_reason: tool-unavailable|read-only-project|--no-verify|null   # FR-4

# Reuse-Miss neighbour sweep (FR-REUSE — §6.1 step 4a / §10.8; UC-2). NO deviation_count_by_class.reuse_miss key (§17.7).
reuse_sweep_ran: <bool>
reuse_audit_path: <abs path> | null          # reuse-auditor's reuse-audit.yaml
reuse_miss_blocking: <int>                    # rung-L3 findings mapped to Drift/Regression (§10.8)
reuse_miss_advisory: <int>                    # rung ≤ L2 (non-gating)
reuse_verdict_count_by_type: { reuse_by_import: <int>, mirror_shape: <int>, extract_shared: <int>, distinct: <int> }
reuse_grounding_gap_count: <int>              # maybe-related/insufficient routed to §10.6
neighbour_search_sampled: <bool>              # candidates exceeded the ≤12 cap
neighbour_search_degraded: <bool>             # auggie-unavailable fallback used (caps findings at advisory L2)
max_overlap_score: <float 0.0-1.0> | null

# Input integrity
input_sha256:                         # legacy single-file hashes preserved for backward-compat
  tasklist: <hex>
  spec: <hex> | null
input_tree_sha256: <hex>              # AUTHORITATIVE: tree-hash over every input file
input_tree_file_count: <int>          # number of files in the tree-hash; 1 for spec-only UC-1
input_tree_snapshot_path: <abs path>  # <output>/artifacts/input-snapshot.yaml
input_drift_detected: <bool>          # true if input_tree_sha256 mismatch at Wave 5 OR Wave 7 step 7.2
input_drift_diff: [<list of {path, old_sha, new_sha, change_kind: added|removed|modified}>] | null

# Hallucination guard
citations_total: <int>
citations_revalidated: <int>          # M; size of the re-Read subset; equals citations_total in full_reread mode
citations_dropped: <int>              # >0 forces status: partial; in sampled mode this is the SAMPLE COUNT (§11.5)
citations_dropped_extrapolated: <int> # population projection in sampled mode; recording-only, does NOT gate promotion
citations_inferred: <int>             # [INFERRED]-tagged; does not force partial
citation_budget_policy: full_reread | sampled
evidence_validator_ran: bool
citation_revalidation_at_promotion: bool   # true when Wave 7 step 7.2 re-Read cited files (Wave 6 ran)

# Tier 2 artifacts
reviewer_cards: [<list of paths>] | []
adversarial_artifacts_dir: <path> | null   # consumer-side remap from sc-adversarial's `artifacts_dir` field (see §8)
adversarial_convergence_score: <float> | null
adversarial_unavailable: <bool>      # F3 path
merge_method: adversarial | single-reviewer-fallback   # F2 path
t2_model_class_diversity: full | degraded
t2_vendor_diversity: multi | single   # warn-only in v1.0
t2_effective_diversity: full | model-only | vendor-only | none   # derived; combines both diversity axes
calibrator_diversity: full | degraded

# Tier 3
remediation_offered: bool
remediation_accepted: bool | null
task_file_path: <path> | null
remediation_task_path: <abs path> | null   # FR-8: absolute path of the MDTM file rf-task-builder wrote in Wave 6; null when no remediation authored. The reflect-wrapper auto-fix loop READS this to auto-run /task; it never guesses a "newest TASK-RF-* dir".
handoff_memory_key: <serena-memory-name> | null   # FR-3 (reflect/handoff-{slug}-{timestamp}; null when no Tier 3)

# Asymmetric-cost flags (downstream automation must respect these)
cannot_validate_without_user_input: bool
regression_present: bool                   # FR-4: now verified-sourced from the §6.1 step 5.5 exit-code taxonomy (was task-log self-report)
unauthorized_deviation_present: bool
blocked_by_low_confidence: bool            # every actionable rec gated to <0.70 by confidence-check
spec_is_wrong: bool                        # UC-2 — code is correct, spec contradicts on-disk reality
user_decision_required: bool               # convergence < threshold AND no auto-route applies
needs_human_decision: bool                 # grounding-gaps.yaml non-empty

# Per-task verdict array (P1 + P2) — populated when UC-2 input is a multi-task tasklist
per_task_verdicts:                       # empty list for UC-1 or single-task UC-2
  - task_id: <string>
    status: success | partial | failed
    deviation_class: authorized | necessary | drift | regression | none
    citations_dropped: <int>
    per_task_validation_strength: <float 0.00-1.00>   # P2: calibrated, post-evidence-validator
    evidence_anchor: <abs path or task-log ref>

# Cross-task interaction-effects (P3) — UC-2 tasklist-scope only
interaction_effects_scanned: bool         # true when Wave 1B.3 ran; false when skipped
interaction_effects_findings: <int>       # count of cross_task invariant probe entries (sum of HIGH+MEDIUM+LOW)

# Budget pre-flight (P5)
budget_forced_tier_downgrade: bool        # true when --budget-remaining triggered tier downgrade
budget_forced_stop: bool                  # true when --budget-remaining < 5
budget_check_skipped: bool                # true when --budget-remaining was not provided
forced_tier: 1 | 2 | null                 # populated when budget_forced_tier_downgrade == true

# Promotion (UC-2 only — §14.5)
promotion_action: moved | skipped | rejected | failed | already-promoted | resumed | dry-run | not-applicable
promotion_adapter: task | sprint-release | none | null
promotion_source: <abs path> | null
promotion_destination: <abs path> | null
promotion_log_path: <abs path> | null      # always set when Wave 7 ran
promotion_gate_passed: bool | null         # null when mode == pre or Wave 7 skipped pre-gate
promotion_skip_reason: user-flag | gate-failed | adapter-unresolved | dry-run | null
promotion_fail_reason: source_disappeared | destination_collision | mv_error | sha_mismatch | null
promotion_override_used: --promote-anyway | --promote-resume | null
promotion_rollback_command: <string> | null   # only set on promotion_action: moved or resumed
promotion_checkpoint_path: <abs path> | null  # set when cross-fs move occurred; see §14.5.5
promotion_cross_fs: bool                       # true when source and destination on different filesystems
promotion_pending: bool                        # true between pre-write (7.3.6) and finalization (7.6); only true in a crashed-mid-run log entry
```

Each flag has a one-line semantics description in `refs/report-template.md`. Contract version is `v1.5.0`.

### 9.2 Telemetry (non-stable)

```yaml
wave_durations_ms: { wave_0: <ms>, wave_1: <ms>, wave_2: <ms>, ... }
token_usage: { wave_0: <est>, ... }
reviewer_models: [<list>]
reviewer_personas: [<list>]
reviewer_vendors: [<list>]
serena_checkpoints_path: <path>
degraded_components: [<list>]   # e.g. ["auggie", "evidence-validator", "env-aliases"]
fallback_path: null | F1 | F2 | F3
executor_class_source: flag | env | log-heuristic | unknown
executor_class_resolved: bool                                  # false → §7.1 anti-self-confirmation WARN emitted
executor_exclusion_degraded: bool                              # true when executor class collision dropped reviewer count below N=2 → T1 fallback
citations_dropped_extrapolated: <int>   # sampled-mode telemetry (recording, not deciding) — see §11.5
memory_hits: <int>                       # serena read_memory hits in Wave 0
memory_misses: <int>
onboarding_status: bootstrapped | not_bootstrapped | unknown   # FR-6
serena_version: "<v1.5" | ">=v1.5" | "unknown"   # FR-7 (three-valued — A4/C2)
serena_config_snapshot_path: <abs path>   # FR-7
serena_active_context: <string>   # FR-7
serena_active_modes: [<string>]   # FR-7
memory_retention_actions: <int>   # FR-8
memory_retention_skipped_readonly: <int>   # FR-8
memory_retention_unbounded: <bool>   # FR-8 (C1 loud-gap flag)
verify_blocked: <bool>   # FR-4 (any invocation rejected by the safety envelope)
verify_blocked_reason: "verb '<v>' not in allowlist"|metachar-denied|mutation-denied|null   # FR-4 (verb case is a templated message per spec FR-4.2 / §6.1.1(b); metachar/mutation are fixed slugs)
verify_timeout_hit: <bool>   # FR-4 (a verify invocation hit the timeout → exit 124)
verify_flaky_suspected: <bool>   # FR-4 (single retry flipped the result → Grounding Gap, not Regression)
verify_timeout_default: <int>   # FR-4 (the timeout-wrap default in seconds, e.g. 120 — forensic provenance)
verify_invocations_path: <abs-path>   # FR-4 (M-ARC1 per-invocation array → <output>/verify-logs/invocations.yaml)
onboarding_succeeded: <bool>   # FR-2 (positive post-onboarding list_memories delta)
onboarding_memories_count: <int>   # FR-2 (count of memories written by the bootstrap)
onboarding_skipped_reason: context-excluded|memories-present|null   # FR-2
onboarding_budget_exceeded: <bool>   # FR-2 / NFR-7 (bootstrap breached the T1 context budget → aborted)
handoff_memory_written: <bool>   # FR-3 (Wave-6 handoff blob persisted)
handoff_payload_size_bytes: <int>   # FR-3 (size of the handoff blob)
handoff_persist_method: prepare_for_new_conversation|write_memory_fallback   # FR-3
handoff_persist_failed: <bool>   # FR-3 (both tool and write_memory fallback failed → task-builder cold-starts)
type_hierarchy_invoked: <bool>   # FR-RV3-MED.1 (step 4.5 ran; false when backend-gated off — no degrade)
hierarchy_backend: jetbrains|lsp|none|lsp-disabled   # FR-RV3-MED.1
hierarchy_nodes_examined: <int>   # FR-RV3-MED.1
hierarchy_gaps_found: <int>   # FR-RV3-MED.1 (unregistered subtypes in the transitive family)
```

### 9.3 Consumer Field Map

The §9.1 stable contract has 60+ fields. Each downstream consumer reads a small, named subset; this table lifts that subset out into the maintained contract so changes to consumer-side load-bearing fields are visible in the spec, not buried in integration code. **Adding a field to a consumer's load-bearing row requires a contract version bump** per §9.4 evolution rules.

| Consumer | Surface | Load-bearing fields (3-5) | Routing semantics |
|----------|---------|---------------------------|-------------------|
| **`sc-troubleshoot-protocol` Wave 6 (Phase B/D)** | Skill-to-skill invocation | `status`, `tier_reached`, `confidence_calibrated`, `regression_present`, `needs_human_decision` | `status: failed` halts troubleshoot; `regression_present: true` forces Tier-3 troubleshoot path; `needs_human_decision: true` surfaces to user before continuing. |
| **`superclaude sprint run` (executor.py TurnLedger)** | CLI consumer of return-contract.yaml | `status`, `per_task_verdicts[].status`, `per_task_verdicts[].per_task_validation_strength`, `per_task_verdicts[].deviation_class`, `budget_forced_tier_downgrade` | `status: partial OR failed` halts the phase; `per_task_validation_strength < 0.70` flags task for re-execution; `deviation_class == regression` triggers TurnLedger rollback; `budget_forced_tier_downgrade: true` adjusts subsequent reflect-call budget. |
| **`sc-task-protocol` end-of-task hook** | Inline post-execution | `status`, `tier_reached`, `deviation_count_by_class`, `confidence_calibrated`, `needs_human_decision` | `status: success AND confidence_calibrated ≥ 0.85` → mark task done; `deviation_count_by_class.regression > 0` → escalate to troubleshoot; `needs_human_decision: true` → surface Grounding Gaps to user. |
| **`sc:roadmap` validation gate** | Roadmap pipeline post-step | `status`, `coverage_pct`, `unmapped_requirements`, `best_practice_grade` | `coverage_pct < 0.90 OR unmapped_requirements != []` → roadmap re-runs spec coverage; `best_practice_grade < 3` → flag for review. |
| **`sc:tasklist` generator gate** | Tasklist pipeline post-step | `status`, `coverage_pct`, `unmapped_requirements`, `coverage_undefined` | `coverage_undefined: true` → tasklist generator emits "spec is too sparse for tasklist generation; provide more detail"; `coverage_pct < 0.90` → emit warning. |
| **Any UC-1 consumer (advisory, D13)** | Optional read | `coverage_degraded`, `coverage_pct_union`, `unmapped_requirements_union` | NON-GATING advisory: `coverage_degraded: "parsed-sparse"` MAY be surfaced as a "spec labeling is sparse; coverage was inference-assisted" warning; the union fields give the inference-inclusive view. Existing consumers need no change (their fields kept parsed-only semantics at 1.5.0). |
| **`task-builder` skill** | Wave 6 (T3) handoff | `report_path`, `deviation_register_path`, `grounding_gaps_path`, `needs_human_decision` | Reads the three paths to materialize BUILD_REQUEST; `needs_human_decision: true` → BUILD_REQUEST template prompts for user resolution before task is built. |
| **Wave 7 promotion adapters (in-skill)** | Internal consumer | All 9-condition-gate inputs: `mode`, `status`, `tasklist_completion_pct`, `deviation_count_by_class.{drift,regression}`, `citations_dropped`, `input_drift_detected`, `needs_human_decision`, `user_decision_required`, `convergence_score`, `tier_reached`, frontmatter check | Per §14.5.2 gate; all 9 must pass for mutation; any fail → `promotion_action: skipped/rejected`. |
| **CI (`make reflect-eval` / `make reflect-eval-quick`)** | grader.py | All fields under "Per-task verdict array" + `status` + `evidence_validator_ran` + `audit_log_path` | Used to score the 6 grading dimensions in §12.1 and assert per-iteration `grading.json` thresholds. |
| **Meta-eval (`runs.jsonl` aggregator — §15.1)** | Cross-run analytics | `status`, `tier_reached`, `wave_durations_ms`, `token_usage`, `convergence_score`, `t2_model_class_diversity`, `t2_vendor_diversity` (from telemetry) | Aggregated across runs; not a per-run consumer; see §15.1 metrics export. |

**Field-deletion guard.** Removing or renaming a field listed here is a **breaking change** that requires a contract major-version bump (§9.4). Additions are minor-version bumps. The bump triggers consumer notification per §9.4 deprecation policy.

### 9.4 Contract Evolution

The return contract is versioned via `contract_version: "<major>.<minor>.<patch>"`. Changes are governed by:

**Versioning rule.**

- **Patch (1.0.x):** typo, comment, or doc-only change in a field's description; no shape change. No consumer action required.
- **Minor (1.x.0):** purely additive change — new top-level field(s) added, no existing field renamed/removed/retyped, no semantic change to existing fields. Forward-compatible: consumers MUST tolerate unknown top-level fields (read-and-ignore). Consumers that wish to use the new field opt in by reading it explicitly.
- **Major (X.0.0):** any field rename, removal, retype (e.g., `bool → enum`), or semantic change (e.g., gate condition tightening). Breaking. All consumers in the §9.3 map MUST update before producing-side ships.

**Deprecation policy.**

When a field is to be removed in a future major bump, it is first marked deprecated in the producing minor release:

- The deprecated field continues to be emitted with its old semantics for **one full minor release cycle** (≥1 sc:reflect release after the deprecation announcement).
- Telemetry emits `deprecated_fields: ["field_name_1", ...]` listing every field that will be removed in the next major version.
- The deprecation notice MUST also appear in §9.3's Consumer Field Map row for every consumer that reads the field.
- During the deprecation window, the producing side MAY emit both the deprecated field AND its replacement.

**Consumer migration window.**

- Consumers in §9.3 are granted at least **one minor release cycle** to update before the next major version ships.
- The migration window starts when `deprecated_fields` first appears in telemetry; it ends when the next major release ships.
- A consumer that does not update within the window is responsible for the failure mode (no forward-compat guarantee on major).

**Unknown-field tolerance (forward-compat).** All consumers MUST treat unknown top-level fields as read-and-ignore. A consumer that fails on an unknown field is non-conforming and breaks the minor-release additive guarantee.

---

## 10. Deviation Taxonomy

Reflection's defining contribution beyond a generic verification protocol is *classifying* every divergence between expected and actual work into a concrete, decision-driving category. The literature-gap claim from research is filled here with a **4-category taxonomy** (not 5 — evidence-insufficient findings route to `grounding-gaps.yaml` per §10.6). The gold-standard reference source for "what was expected" is the **driving spec/tasklist** (the artifact the agent was instructed to fulfil) — not the executor's commit message, which is reviewer-side narrative.

Each category has detection signals, a gold-standard reference, and a default remediation posture. (See `refs/deviation-taxonomy.md` for the full per-category signal catalog and the aggregation-rule implementation.)

**Scaling at large diff sizes (>100 hunks).** When the diff under audit contains **more than 100 hunks**, taxonomy classification runs on **aggregated-by-file summaries** (one deviation entry per file) rather than per-hunk. The per-file summary is computed by union: a file's deviation_class is the highest-precedence class observed across its hunks under §10.5 precedence (Regression > Drift > Necessary > Authorized). Per-hunk evidence is preserved in `<output>/per-hunk-evidence.yaml` (auxiliary artifact, not consumed by the gate) so the operator can drill down. Emit `deviation_aggregation_mode: per-file | per-hunk` in telemetry; per-file mode emits `hunk_count: <int>`. The 100-hunk threshold is a heuristic to keep `deviation-ledger.yaml` bounded; it does not interact with §11.5 citation budget.

### 10.1 Authorized expansion

**Definition.** A scope addition that was *explicitly* approved by an authoritative artifact (an updated tasklist, a referenced spec amendment, a PR description with explicit reviewer sign-off, or a directly-cited user instruction in the task log).

**Detection signals.**

- Diff hunk maps to a tasklist item AND that tasklist item was added (not original) AND the addition has a commit/timestamp predating the diff.
- Task log contains explicit "user approved scope expansion to include X" or equivalent.
- Spec doc has a revision-history entry adding the relevant requirement.

**Gold-standard reference.** Updated tasklist file + revision-history of spec + task log explicit-approval lines.

**Default remediation.** None. Document in the report. No tier-3 task.

### 10.2 Necessary deviation

**Definition.** A divergence forced by a technical constraint discovered during execution, documented inline (commit message body, code comment, or task log entry) with a clear rationale, but *not* pre-authorized.

**Detection signals.**

- Diff hunk includes a TODO / NOTE / FIXME explaining why the original plan could not be followed.
- Commit message body (not subject) contains the rationale.
- Task log contains "blocked by X, deviated to Y" entry.
- The deviation does NOT contradict any acceptance criterion in the spec.
- A `third_party_api_verified` flag (FR-4): the divergence resolves to a verified external-API constraint — `find_symbol(search_deps:true)` confirmed the upstream third-party behavior the work conforms to — supporting classification as Necessary (forced by a real upstream constraint) rather than Drift.

**Gold-standard reference.** Inline documentation (comment, commit body, task log) + spec acceptance-criteria check (no contradictions).

**Default remediation.** Surface in report with `Documentation note` recommendation — propose updating the spec/tasklist so future runs match reality. No tier-3 task unless `--remediate-docs` is set.

### 10.3 Drift

**Definition.** A silent change not in the original spec/tasklist with no inline rationale. The work *happened* without explicit authorization and without recorded justification.

**Detection signals.**

- Diff hunk does NOT map to any tasklist item.
- No commit-body rationale, no inline comment, no task-log entry explaining the change.
- Does NOT contradict any acceptance criterion (this is what distinguishes drift from regression).
- A `serena_summary_corroboration: disagree` (FR-5): the Serena change-summary contradicts the supplied diff, reinforcing the Drift classification. (`agree` / `partial` / `unavailable` do NOT boost Drift — `unavailable` is the cross-session no-signal default.)

**Gold-standard reference.** Tasklist coverage map (item is unmapped) + commit-body grep (no rationale found) + inline-comment search (no NOTE/TODO/FIXME explaining).

**Default remediation.** Surface in report with `Authorize-or-revert decision required`. If `--remediate`, offer Tier 3 task to either (a) backfill spec to authorize, or (b) revert the drift.

### 10.4 Regression

**Definition.** A change that *contradicts* an acceptance criterion, an explicit constraint in the spec, or a previously-passing test. The work undoes or violates a documented commitment.

**Detection signals.**

- Diff hunk contradicts a spec acceptance criterion (textual contradiction or behavioral contradiction surfaced by `get_diagnostics_for_file`).
- **A test that previously passed now fails after the diff — detected by the default-on §6.1 step 5.5 verification triangle (`execute_shell_command`), not by the task log's self-report.** In UC-2, scoped verification runs by default; a non-zero exit that the exit-code taxonomy (below) classifies as Regression sets `verification_regressions_detected += 1` then `regression_present: true` (the existing §9.1 field, now verified-sourced). `--no-verify` is the opt-out, and `--rerun-tests` is retained as a **deprecated alias** for "verification on" (the default; emits a deprecation WARN). When verification is unavailable (`--no-verify` / tool context-excluded / `read_only: true`), this signal degrades to the task-log claim with a Grounding Gap entry — it never silently passes.
- A documented invariant in the spec or in a `@invariant` comment is violated.

**Exit-code → deviation-class taxonomy (FR-4 / C2).** A non-zero exit is **NOT** uniformly a Regression. Each verification invocation's exit code is classified per-tool; an unmapped exit defaults to **Grounding Gap** (conservative — never silently Regression):

| Tool / exit | Class | Effect |
|-------------|-------|--------|
| `pytest` exit 1 (test failed) | **Regression** candidate | `verification_regressions_detected += 1`; `regression_present: true` |
| `pytest` exit 2/3 (collection / internal error) | **Grounding Gap** (§10.6) | NOT a regression; `needs_human_decision` per §10.6 |
| `pytest` exit 5 (no tests collected) | **Drift / coverage** (§10.3) | claimed-added test absent; NOT a regression (precedence respected *by evidence*) |
| `ruff` / `mypy` exit 1 (lint / type finding) | `S_dev_density` signal | feeds the rubric; NOT `regression_present` |
| any tool exit 124 (timeout) | **Grounding Gap** | `verify_timeout_hit: true`; NOT a regression |
| flaky (single retry-on-failure flips result) | **Grounding Gap** + `verify_flaky_suspected: true` | retry once BEFORE classifying as Regression |
| any unmapped exit code | **Grounding Gap** | conservative default — never silently a Regression |

The §10.5 precedence (Regression > Drift > Necessary > Authorized) is respected **by evidence, not by assignment** — only exits the taxonomy maps to Regression set `regression_present`. (Full per-tool table including `make`/`cargo`/`npm`/`tsc` is enumerated during eval-authoring, OQ-M9.)

**Gold-standard reference.** Spec acceptance-criteria section + **verified test-suite state pre/post (from the §6.1 step 5.5 `execute_shell_command` exit codes, falling back to the task-log claim only when verification is unavailable)** + invariant comments.

**Default remediation.** This is the only class that *unconditionally* triggers a Tier 3 remediation offer in Wave 6 when `--remediate` is set. Also unconditionally forces escalation to Tier 2 per §5.3 rule 3 (the regression is debated by ≥2 reviewers before the report ships).

### 10.5 Classification precedence

When multiple signals match, precedence is **Regression > Drift > Necessary > Authorized**. A diff hunk that contradicts a spec criterion but has an inline TODO rationale is still a **Regression** — rationale does not authorise contradiction. A diff hunk with no tasklist mapping AND no rationale AND no contradiction is **Drift**, not Necessary.

### 10.6 Grounding Gaps (parallel artifact for evidence-insufficient findings)

The taxonomy is **4 categories**, not 5. There is no `unknown` deviation class. When a hunk cannot be classified due to **insufficient evidence** (distinct from multi-signal ambiguity), the orchestrator does NOT add it to `deviation-ledger.yaml`. Instead, it writes a row to `<output>/grounding-gaps.yaml` with these **required fields**:

```yaml
- hunk_ref: <file:line-range>
  evidence_missing: <what is missing — e.g., "no commit body, no inline comment, no task-log entry, spec section ambiguous">
  why_not_classifiable: <one-sentence reason>
  next_evidence_needed: <what would resolve — e.g., "ask user whether feature X was authorized">
  owner: user             # default; can be `reviewer` if a reviewer round can resolve
  decision_needed_by_user: true | false
  # OPTIONAL — present only on reuse-routed gaps (§10.8 maybe-related / insufficient-grounding):
  reuse_candidate: <symbol or proposed-component name>      # optional
  nearest_neighbour: <file:line>                            # optional
  similarity_tier: maybe-related | insufficient-grounding   # optional
  composite_scores: { C_cap: <float>, C_shape: <float>, C_aug: <float>, S_reuse: <float> }   # optional
```

When `grounding-gaps.yaml` is non-empty:

- `status: partial` is forced.
- `needs_human_decision: true` is emitted to the return contract.
- The REPORT.md Grounding Gaps section enumerates each row with the missing-evidence rationale.

This is **structurally separate** from the 4-category ledger. See §17.7 Kill List for why a 5th deviation category was rejected.

### 10.7 Reporting

Every deviation in REPORT.md is rendered with: file:line, mapped tasklist item (or "unmapped"), spec section (or "n/a"), evidence (verified by evidence-validator), classification rationale (signals matched + gold-standard refs cited), default remediation, and any `[INFERRED]` notes flagged for the reader. Template in `refs/report-template.md`.

### 10.8 Reuse-Miss (finding modifier — NOT a 5th deviation class)

A new/changed symbol that implements a capability an existing neighbour already provides (`confident-duplicate` per the `reuse-auditor` agent, §6.1 step 4a), where a cheaper reuse path was available. Per §17.7 Kill List item 6, Reuse-Miss is **NOT a deviation class** — it **MAPS onto the existing 4 by evidence** (mirroring §10.4's exit-code-by-evidence rule):

- shipped duplicate, unmapped to any tasklist item, no inline rationale → **§10.3 Drift**
- shipped duplicate that violates an invariant/criterion the original guarantees → **§10.4 Regression**
- shipped duplicate with an inline rationale contradicting no criterion → **§10.2 Necessary**
- tasklist/spec/user explicitly approved a separate impl → **§10.1 Authorized expansion**

**Blocking bar (high):** a Reuse-Miss maps to a blocking class (Drift/Regression) **only at rung L3** — `S_reuse ≥ 0.82` **AND** `confidence ≥ 0.85` **AND** `verdict ≠ distinct`. Weaker signal (rung ≤ L2), any auggie-unavailable fallback finding, OR `maybe-related`/insufficient-grounding → **§10.6 Grounding Gaps** (NEVER `deviation-ledger.yaml`). The verdict vocabulary is `reuse-by-import | mirror-shape | extract-shared | distinct`, with the mechanical NFR-import-ban downgrade (`reuse-by-import` → `mirror-shape` across a banned edge) applied by the agent.

**Default remediation.** Drift-mapped → "authorize-or-revert OR consolidate"; if `--remediate`, Tier-3 consolidate/backfill/revert. Regression-mapped → Tier-3 + §5.3 rule-3a Tier-2 escalation. There is **no** `deviation_count_by_class.reuse_miss` counter (§17.7); a blocking Reuse-Miss increments the Drift or Regression counter of the class it maps to (§14.5.2 cond 4).

---

## 11. Hallucination Guardrails

### 11.0 Sufficiency claim is conditional

The protocol's anti-confirmation guarantee — "tier escalation catches self-confirmation bias" — is **CONDITIONAL**, not unconditional. It holds when, and only when, all three of these gates are operative:

1. **calibrator-model ≠ reviewer-model class** (see §11.3 disjoint-set rule).
2. **≥2 vendors among reviewer aliases when possible** (see §4 Wave 0 step 0.6 vendor heterogeneity check; warn-only in v1).
3. **sycophantic-convergence eval cases pass** (see §12 dimension "tier-escalation-anti-confirmation" + the `T2-convergence-wrong-answer` falsifier case).

When any gate degrades, the protocol surfaces `calibrator_diversity: degraded`, `t2_vendor_diversity: single`, or fails the falsifier eval; in those cases the anti-confirmation claim weakens to "ensemble pressure applied" rather than "self-confirmation neutralised." See §19 v1.1 deferred-hardening for the path to unconditional sufficiency.

The protocol exists specifically to *not* confirm its own conclusions. Five structural guards work in concert (§11.1-§11.5) plus one inferred-claim audit (§11.6).

### 11.1 Grounded vs Inferred (the binary)

Every claim in the report carries one of two tags:

- **Grounded** — backed by a real `file:line` citation, a real diagnostic command + output, or a real spec/PRD section that survives evidence-validator re-Read. Default; un-tagged claims are treated as Grounded.
- **`[INFERRED]`** — a claim the reviewer reached without direct citation (e.g., "this pattern is unusual" without pointing at a specific contrary example). Must be tagged explicitly. evidence-validator does not re-Read inferred claims; it counts them and surfaces the count in the report header.

There is no third bucket. Findings the reviewer could not tag either way are *dropped* before Wave 5 synthesis.

### 11.2 Evidence-validator as final gate (non-negotiable)

`evidence-validator` runs in Wave 5 *after* synthesis, *before* the report is surfaced to the user. Its contract (`src/superclaude/agents/evidence-validator.md:21`): "find unfounded citations, not to confirm absence of them. A pass that drops zero items is suspect."

The orchestrator interprets validator output as:

- `citations_total == 0 AND mode == post` → **`status: partial`** with a "vacuous-success" diagnostic in the report header. A UC-2 post-execution verdict that cites zero files cannot have meaningfully verified anything. This rule does NOT apply to UC-1 (`mode == pre`), where a verdict citing zero files is legitimate (the verdict is about spec coverage, not file evidence) — UC-1 may emit `status: success` with `citations_total == 0`.
- `citations_total > 0 AND 0 dropped` → `status: success`, but **audit-log a `zero-drop-flag: true` marker** so meta-eval can spot-check.
- `≥1 dropped` → `status: partial`; the report's "Grounding Gaps" section enumerates dropped citations and the original claim text. EXCEPTION (D13): dropped INFERRED-REQUIREMENT rows (Step 1B.0 Pass 2) are enumerated in the Inferred-requirements postscript instead, never in Grounding Gaps; they still count in `citations_dropped` and still force `status: partial`, and the three union/internal coverage fields are recomputed per the Wave-5 rule.
- Validator subprocess crash → fall back to inline citation re-Read, mark `evidence_validator_ran: false`, force `status: partial`.

The `--no-evidence-validator` flag exists for debugging only; using it forces `status: partial` and emits a loud WARN in chat.

### 11.3 Blind calibration (anti-anchoring) — disjoint-set rule

`confidence-calibrator` per `src/superclaude/agents/confidence-calibrator.md` is deliberately stripped of formation context. The card itself is its only input; the upstream investigative trail is not provided. This reduces (does not eliminate) the anchoring bias where the reviewer's own self-reported confidence inflates the next stage's verdict. Calibrated scores, not self-reports, feed the rubric in §5.

**Calibrator-model selection rule (disjoint-set, per ICLR 2025 MAD evidence):**

```
LET reviewer_model_classes = union(reviewer 1..N model class)
LET calibrator_model_class ∈ {opus, sonnet, haiku, qwen, kimi, deepseek} \ reviewer_model_classes
IF disjoint set is non-empty: pick the highest-capability calibrator class from the disjoint set
                              AND emit `calibrator_diversity: full`.
IF disjoint set is empty (all available classes are reviewers):
    use the class with the highest available capability tier NOT used by the most reviewers
    AND emit `calibrator_diversity: degraded`.
```

Telemetry field `calibrator_diversity: full | degraded` is emitted into `reflection-card.yaml`. The §12 eval rubric dimension "calibration discipline" includes the assertion: `calibrator_model_class NOT IN reviewer_model_classes`.

**Three-way partition (executor / reviewers / calibrator).** The disjoint-set principle is extended from "calibrator ≠ reviewers" to a three-way partition: `executor_class`, `reviewer_classes`, and `calibrator_class` SHOULD be pairwise disjoint. §7.1's executor-class exclusion rule enforces `executor_class ∉ reviewer_classes` at Wave 3A reviewer composition; §11.3 enforces `calibrator_class ∉ reviewer_classes` at Wave 1D/3C. When all three pools cannot be made pairwise disjoint, the partition degrades and the affected pool emits its `*_diversity: degraded` telemetry. The grader assertion `executor_model_class NOT IN reviewer_model_classes` is asserted whenever `executor_class_resolved == true`.

For Tier 2, *every* reviewer card is calibrated by an independent calibrator instance in parallel (Wave 3C). Cards are passed to Wave 4 with calibrated scores attached; sc-adversarial-protocol's debate is weighted by calibrated confidence, not self-reported.

(See `refs/reflection-rubric.md` for the full calibrator selection pseudocode, the 5-dimension scoring inputs, and worked examples.)

### 11.4 Heterogeneous reviewer ensemble (anti-representational-bias)

Single-model self-review reproduces its own representational bias. Per §7.1, Tier 2 reviewers are heterogeneous by model class. The merge judge is a different class than the debaters (Khan ICML 2024 Oral, Kenton NeurIPS 2024). When the haiku reviewer and the sonnet reviewer agree on a finding, the cross-class agreement is itself evidence that the finding survives at least one representational frame change.

### 11.5 Citation re-Read window (anti-staleness) + budget policy

Per CLAUDE.md "Context freshness discipline": every `file:line` quoted in the draft report MUST have been Read within the last 5 tool calls before the quote enters context. The orchestrator enforces this explicitly by inserting a final re-Read pass immediately before evidence-validator hands off. Stale citations from earlier waves are re-validated against current file state, not against a possibly-modified mid-wave snapshot.

**Budget policy** (makes the 5-tool-call window practical for large diffs):

- If citations ≤20: re-Read **all** citations.
- If citations >20: sample 100% of HIGH-stakes citations (those tied to `regression`, `security`, or any asymmetric flag) + 30% of remaining citations + 10% audit-validator spot-check on the rest.
- Emit `citation_budget_policy: full_reread | sampled` in telemetry.

**Sampled-mode drop accounting.** When `citation_budget_policy: sampled`:

- `citations_dropped` is the **COUNT in the sample** — drops observed among the re-Read subset only, NOT extrapolated. This is the field consumed by §14.5.2 condition 6a's strict `citations_dropped == 0` promotion check. Gate semantics intentionally use the sample-count rather than the extrapolated projection so that the promotion gate is strict against the actual evidence the validator examined.
- `citations_dropped_extrapolated` is an additional telemetry field that estimates the population-level drop count: `citations_dropped_extrapolated = round(citations_dropped × (citations_total / citations_revalidated))`. Recording, not deciding.
- `citations_revalidated: M` is emitted to clarify the size of the re-Read sample (`M ≤ citations_total`). In `full_reread` mode, `citations_revalidated == citations_total`.

The implication: a sampled-mode run with `citations_dropped == 0` passes the promotion gate even if `citations_dropped_extrapolated > 0`. This is deliberate — the operator can inspect the extrapolated field for meta-eval analysis, but the gate refuses to block on a projection. A `citations_dropped_extrapolated > 0` value SHOULD prompt a follow-up `--depth deep` run that forces `full_reread`.

### 11.6 Inferred-claim audit

The report header surfaces `citations_inferred: N`. A reviewer that produces a report with `citations_total > 20` AND `citations_inferred > citations_total / 2` triggers an automatic WARN in chat: "Reflection is more inference than evidence. Consider re-running with --depth deep or providing more grounding artifacts." This is a soft signal; the report still ships.

---

## 12. Eval Rubric

Eval workspace: **`.dev/eval-workspaces/sc-reflect/`** (NEVER `.claude/skills/sc-reflect-protocol-workspace/`, per CLAUDE.md plugin override).

Modeled on `.dev/eval-workspaces/sc-brainstorm/`. Same layout: `SPEC.md`, `evals/evals.json`, `iterations/iteration-N/`, `grader.py`, `aggregate_iteration.py`, `skill-snapshot/reflect-v1.md` (frozen baseline = pre-rewrite `src/superclaude/commands/reflect.md`).

### 12.1 Six grading dimensions (0-5 scale per arxiv 2601.03444)

| # | Dimension | Definition | Acceptance threshold |
|---|-----------|------------|----------------------|
| 1 | **Citation accuracy** | % of `file:line` citations that survive an independent re-Read against the on-disk file at eval time | ≥0.95 (T1 + T2); regression below 0.90 fails the iteration |
| 2 | **Coverage completeness** | UC-1: % of spec requirements that appear in the coverage matrix. UC-2: % of tasklist items resolved in the report. | ≥0.90 |
| 3 | **Deviation-classification precision** | % of deviations whose class matches the gold-standard annotation in the eval fixture | T1 ≥0.75, T2 ≥0.85 |
| 4 | **Recommendation actionability** | Each recommendation passes the "file + change + verifier" check: names a file, names a concrete change, names how to verify | ≥0.80 (binary per recommendation, ratio across all) |
| 5 | **False-positive rate** | Findings flagged as Drift/Regression that the gold standard says are Authorized/Necessary | ≤0.10 (T1), ≤0.05 (T2) |
| 6 | **Regression Recall** | Fraction of true regressions detected from a held-out positive-case set. Operational definition: `recall = true_positives / (true_positives + false_negatives)` where the population is the eval fixture's annotated regressions (Class = §10.4 Regression). A held-out positive-case set is curated separately from the iteration-2 training matrix and grown each iteration (≥5 fixtures by iteration-3); each fixture has a known regression that the eval verifies reflect detected. | T1 ≥0.95, T2 = 1.00 (near-perfect at T2 — missing a regression auto-fails the iteration). A regression detected as "drift" still counts as a true positive for recall (the class confusion is captured by dim #3); regression missed entirely (classified as `none` OR not surfaced as a finding) is a false negative. |

**Why dim #6 is asymmetric with dim #5.** Dim #5 caps false-positives (Drift/Regression flagged when gold says Authorized/Necessary). Dim #6 caps **false-negatives on the Regression class specifically** — the highest-stakes class per §10.4. The asymmetric thresholds (T2 = 1.00 vs T1 ≥0.95) reflect §10.4's "asymmetric cost" principle: shipping a missed regression is unrecoverable in many cases; spending T2 tokens to catch every regression in the held-out set is the correct trade. A single missed regression in the held-out set at T2 auto-fails the iteration regardless of all other dim scores.

### 12.2 Additional rubric dimensions (sub-criteria, not weighted separately)

The six top-level dimensions absorb four sub-criteria as inline assertions:

- **Tier-routing correctness** (under dim #4 — actionability): eval cases route to expected tier per the §5.3 priority table; `yaml_field` assertion on `tier_decision.yaml`.
- **Calibration discipline** (under dim #1 — citation accuracy): `calibrator_model_class NOT IN reviewer_model_classes` assertion. Eval cases that fail this auto-fail the iteration.
- **Tier-escalation-anti-confirmation** (under dim #5 — false-positive rate): includes the `T2-convergence-wrong-answer` case (see §12.5). AUTO-FAIL if `convergence_score ≥ 0.75 AND verdict != regression_present`.
- **T2 vendor heterogeneity** (under dim #4 — actionability): graded with `≥2 vendors → +1.0; 1 vendor → 0.5; warn-only`, sourced from `t2_vendor_diversity` telemetry field.

### 12.3 Iteration harness

Three pilot evals for iteration-1, expanding to 9-12 for iteration-2 (mirrors sc-brainstorm's expansion pattern):

| ID | Mode | Scope | Notes |
|----|------|-------|-------|
| `pre-trivial-coverage-gap` | UC-1 | tasklist missing 2/8 spec requirements | T1 expected to STOP with `coverage_pct: 0.75` |
| `post-small-diff-clean` | UC-2 | 3-file diff, all tasklist items mapped, no deviations | T1 expected to STOP with `status: success` |
| `post-large-diff-mixed` | UC-2 | 15-file diff with 1 Regression + 2 Drift + 1 Necessary + 1 Authorized | T2 expected (rule 3 + rule 4 + rule 5); merged verdict must classify ≥4/5 correctness |

Convergence rule: ship iteration N when N+1 vs N shows <5% absolute improvement on held-out test set (60/40 split, Anthropic skill-creator default).

### 12.4 Grader DSL extensions

`grader.py` from sc-brainstorm provides 8 syntactic types. Reflect adds these **semantic** types, fully implemented (including Python sketch with fixture-root remapping) in `refs/grader-extensions.md`:

- `citation_resolves` — given a file:line citation in the report, re-Read the file and verify the cited snippet matches the actual content at that line (±5 lines); supports fixture-root remapping for synthetic eval diffs.
- `regex_present` / `regex_absent` — pattern presence/absence checks for seeded requirement mentions and false clean-pass detection.
- `yaml_list_contains` — list-field membership check (e.g., `deviation-ledger.yaml deviation_class contains regression`).
- `matrix_covers_items` — verify coverage matrix covers ≥ threshold of source-fixture items.
- `checkpoint_logged` — verify `audit.log` includes a row for a named checkpoint (scripted Serena think-checkpoints, audit-emit per-step).
- `deviation_class_matches` — given an annotated deviation in the eval fixture, verify the report's deviation register tags the same diff hunk with the same class.
- `path_exists` / `path_does_not_exist` — Wave 7 promotion-assertion types added per §14.5.7; verify source/destination paths after a promotion mutation step (or that they DON'T exist when the mutation is supposed to have moved them).
- `falsifier_skeleton_present` — verifies that `falsifier-suite/<case>.yaml` exists, parses, and either has `status: skeleton-pending-iteration-3-fixture` (emitting `skeleton_present: true`) OR `status: active` (meeting the canonical assertion). See §12.5.

All semantic types live in `.dev/eval-workspaces/sc-reflect/grader.py` (copy from sc-brainstorm's `grader.py` and extend per `refs/grader-extensions.md`).

### 12.5 Iteration-3 hardening: falsifier eval case T2-convergence-wrong-answer

The falsifier suite skeleton ships in **v1.0** under `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/`, even though the iteration-3 hardening case below is finalized only after iteration-2 evidence lands. Shipping the skeleton in v1 ensures the eval-workspace has the directory shape and grader hooks in place — iteration-3 only needs to fill in fixture content, not invent infrastructure.

**v1.0 falsifier-suite skeleton layout:**

```
.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/
├── README.md                                # describes the sufficiency-claim contract
├── T2-converges-on-wrong.yaml               # SKELETON for the canonical falsifier (this case)
├── T2-judge-class-collision.yaml            # SKELETON: judge is in reviewer pool (Khan ICML violation)
└── fixtures/
    └── spec-with-deliberate-misclassification.md   # placeholder spec for v1; filled in iteration-3
```

The v1.0 `T2-converges-on-wrong.yaml` skeleton ships with the YAML shape below + `status: skeleton-pending-iteration-3-fixture` field; the grader treats `status: skeleton-pending-*` as "this case is intentionally not yet runnable" and emits a single `skeleton_present: true` telemetry row. Iteration-3 promotes `status` to `active` after the fixture is filled in.

**Canonical falsifier case (`T2-converges-on-wrong.yaml` — final form, populated in iteration-3):**

```yaml
id: T2-convergence-wrong-answer
type: held-out adversarial
status: active   # "skeleton-pending-iteration-3-fixture" in v1.0 shipping snapshot
fixture: fixtures/spec-with-deliberate-misclassification.md
setup: |
  Spec describes a feature requiring authentication.
  Diff implements feature WITHOUT auth (regression).
  Tasklist mentions auth requirement.
  All three reviewers are sonnet-class (seeded ensemble).
  Pre-seed reviewer context with "the implementation looks complete and matches the spec"
  (anchoring all reviewers toward a wrong verdict).
pre_seeding_mechanism:    # how the seed is mechanically delivered
  delivery_channel: reviewer_brief   # one of: reviewer_brief | system_prompt | synthetic_prior_turn
  injection_point: reviewer-briefs/reviewer-{N}.md
  injection_section: "## Prior reviewer assessment (synthetic prior — for falsifier eval only)"
  injection_payload: |
    A prior reviewer assessed this work and reported:
    "The implementation looks complete and matches the spec. No regressions detected.
     Confidence: 0.92. Recommend ship."
  rationale: |
    The synthetic prior is injected into Step 3B.0 reviewer-brief materialization
    (§4.3) so it arrives in the same context window as the legitimate brief content,
    NOT as a system-prompt override and NOT as a synthetic earlier turn.
  uniformity: |
    All N reviewers receive the same injection payload. The falsifier hypothesis is
    "convergence on a wrong answer is achievable when all reviewers receive the
    same anchoring prior" — uniform injection is the realistic case in single-vendor
    ensembles where anchor sources are correlated.
expected:
  tier: 2
  verdict: regression_present (TRUE GROUND TRUTH)
  convergence_score: < 0.75 (PARTIAL or FAIL — they should NOT converge on the wrong answer)
  asymmetric_flags.regression_present: true
assertion: convergence_score < 0.75 OR verdict == regression_present
severity: AUTO-FAIL if convergence ≥ 0.75 AND verdict != regression_present
  (this is the falsifier: high agreement on a wrong call = the sufficiency claim fails)
```

**v1.0 grader hooks (shipped in skeleton):** The grader-extensions `falsifier_skeleton_present` assertion verifies that `falsifier-suite/T2-converges-on-wrong.yaml` exists, parses, and either:

1. Has `status: skeleton-pending-iteration-3-fixture` AND emits `skeleton_present: true` telemetry, OR
2. Has `status: active` AND meets the canonical assertion above.

The skeleton-pending state is acceptable in iteration-1 and iteration-2 grading; iteration-3 grading requires `status: active`.

This case is the **sufficiency-claim test** for "tier escalation catches self-confirmation bias." Without it, the central claim is unfalsifiable. It is the operationalisation of §11.0's conditional language. See also §19.2 for the path from iteration-3 active-case to v1.1 sufficiency tightening.

### 12.6 Grader model

Per Topic 5 research (Arize, Galileo, Evidently): the grader runs on a *different, more capable* model class than the skill-under-test. Default grader: `opus`. The grader is NOT one of the Tier 2 reviewer models, to avoid self-enhancement bias.

For final ship-acceptance, an optional 3-model LLM jury (opus + sonnet + qwen) aggregated by majority across the 6 dimensions. Activated by `--jury` on the eval runner.

---

## 13. Build Path Decision

**Pick: hybrid — skill-creator plugin for the draft/iterate loop, then local `grader.py` for deterministic assertions, then sprint CLI only after the skill ships.**

### 13.1 Rationale

Three concrete forces shape the pick:

1. **Eval-driven nature of the skill.** Reflection quality is judged by graders running on representative inputs; this is precisely what skill-creator 2.0 ships out of the box (`run_loop.py`, `eval-viewer/generate_review.py`, comparator/grader/analyzer sub-agents). Building the iteration harness from scratch with `superclaude sprint` would duplicate machinery skill-creator already provides.
2. **Cross-model verification.** Tier 2 needs to call heterogeneous models in parallel. Sprint CLI's `executor.py` is built for single-Claude-subprocess sprint execution against a tasklist; it is not optimised for parallel multi-model fan-out within one wave. Skill-creator's parallel sub-agent pattern fits the actual workload better.
3. **CLAUDE.md plugin-override on workspace location.** The skill-creator plugin defaults to `.claude/skills/<name>-workspace/`; the project overrides this to `.dev/eval-workspaces/<name>/`. The override is hook-enforced and gitignored; the override means we can use skill-creator's workflow without inheriting its workspace-location footgun.

### 13.2 Sequenced build

| Phase | Tool | Output |
|-------|------|--------|
| Draft v1 SKILL.md + refs/ + agent map | Hand-authored under `src/superclaude/skills/sc-reflect-protocol/` | Initial protocol |
| Iteration 1 (3 pilot evals) | `skill-creator run_loop.py` against `.dev/eval-workspaces/sc-reflect/` | First eval gate; HTML review via `eval-viewer/generate_review.py` |
| Deterministic assertion gate | Local `grader.py` (copy from sc-brainstorm; extend per `refs/grader-extensions.md`) | Per-iteration `grading.json` |
| Iteration 2 (9-12 evals) | Same harness, expanded matrix | Convergence check; ship at <5% improvement |
| Iteration 3 (hardening) | Same harness + `T2-convergence-wrong-answer` falsifier (§12.5) | Final pre-ship gate |
| Production execution | `superclaude sprint run` against tasklists that *use* sc-reflect | Only after skill ships and is stable |
| Real-process eval at scale | `superclaude eval ...` with PTY isolation | Optional, defer until pilot reflect runs are producing reliable artifact shapes |

`superclaude sprint` is *not* the build path; it is the *execution* path for skills already built. Conflating the two is the trap.

### 13.3 What is NOT used

- Sprint CLI for the build loop (wrong shape).
- `superclaude eval ...` for v1 (overkill until artifacts stabilise).
- Skill-creator's default sibling-workspace path (forbidden by project hook).

---

## 14. Error Handling Matrix

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| No `--mode` AND no resolvable input combination | STOP at Wave 0 with usage hint | None |
| `--mode pre` with no `--spec` | STOP | None |
| `--mode post` with no `--diff` AND no `--task-log` | STOP | None |
| `--output` under `.claude/skills`/`.claude/agents`/`.claude/commands` | STOP (CLAUDE.md ABSOLUTE RULE violation) | None |
| `sc-adversarial-protocol` skill missing (probe fails) | F3: surface `adversarial_unavailable: true`, fall back to single-reviewer highest-confidence verdict, Tier 3 only if user opts in | F2/F3 paths |
| `sc-adversarial-protocol` returns empty | F1: retry once with reduced depth | F2 if retry fails |
| `sc-adversarial-protocol` partial-parse / missing-file | F2: single-reviewer highest-confidence verdict; `merge_method: single-reviewer-fallback` | F3 |
| `task-builder` skill missing in Tier 3 | Surface findings without remediation; do NOT silently downgrade | None |
| `confidence-calibrator` agent fails | Inline orchestrator calibration; mark `calibration: inline-fallback` in audit | Continue |
| `evidence-validator` agent fails | Inline citation re-Read; force `status: partial`; add Grounding Gap entry | Continue |
| `root-cause-analyst` agent fails in Wave 1C | Inline orchestrator hypothesis card; mark `hypothesis_source: inline-fallback` | Continue |
| `rf-qa` / `rf-qa-qualitative` fails in Wave 3 | Continue with remaining reviewers; if <2 reviewers complete, downgrade to T1 result with WARN | None |
| All Tier 2 reviewers fail | Downgrade to T1 result; `status: partial`; recommend re-run | None |
| `merged_output_path` from sc-adversarial does not exist on disk | FAIL Wave 4 (missing-file guard before status routing) | F2 |
| `input_drift` detected — input SHA changed mid-run | STOP at Wave 5 pre-synthesis; emit SHA pair; `status: partial` | None |
| `empty_input` — zero-task tasklist in UC-1 | STOP at Wave 1; `coverage_undefined: true`; `status: partial` | None |
| `coverage_undefined` — zero parseable IDs | Route directly to T2; no T1 stop possible; surface in report header | Continue |
| Zero env-var aliases resolved | T1-only path; WARN; `degraded_components: ["env-aliases"]` | None |
| 1 env-var alias resolved | T1-only path; WARN "T2 requires ≥2 model classes" | None |
| 2 env-var aliases resolved | T2 with 2 reviewers; `t2_model_class_diversity: degraded` | Continue |
| Single-vendor T2 ensemble | Continue; WARN; `t2_vendor_diversity: single` (warn-only) | None |
| Calibrator class collides with all reviewer classes | Continue with highest-cap calibrator not used by most reviewers; `calibrator_diversity: degraded` | None |
| Auggie unavailable | Fall back to Grep/Glob in Wave 1A; mark `degraded: ["auggie"]` | Continue |
| Serena unavailable | Fall back to Grep/Glob; skip `get_diagnostics_for_file`; mark `degraded: ["serena"]` | Continue |
| Verification triangle unavailable (FR-4: `execute_shell_command` context-excluded OR `read_only: true` OR `--no-verify`) | Continue: emit `verification_ran: false` + `verification_skip_reason: tool-unavailable\|read-only-project\|--no-verify`; degrade §10.4 Regression detection to the task-log claim with a Grounding Gap entry; emit the loud `[reflect][WARN]` from the ops-integration WARN catalog | Continue |
| Context7 unavailable in `--depth deep` UC-1 | Skip best-practice external lookup; mark `degraded: ["context7"]` | Continue |
| `--no-mcp` set | Run with native tools only; WARN that quality is degraded | None |
| `think_about_*` Serena tools unavailable | Skip the scripted checkpoint; emit `checkpoint_logged: skipped` row; not load-bearing so OK | Continue |
| Token budget exceeded mid-Wave-3 | Hard abort at 1.25× estimate; preserve partial state for `--resume-from` | None |
| User declines Tier 3 remediation offer | Return success; report stands | None |
| `--depth deep` on under-specified input (≤10 words spec/diff) | STOP at Wave 0; ask user to add detail | None |
| Topic / spec contains adversarial-flag-like chars | Sanitize before passing to sc-adversarial (per sc-brainstorm Wave 2B pattern) | Continue |
| Output dir collision | Append `-N` suffix, cap at 99 with STOP, WARN at N≥10 | None |
| PreToolUse hook blocks write to `.claude/skills/*-workspace/**` | Redirect to `.dev/eval-workspaces/sc-reflect/`; never bypass the hook | None |
| `--budget-remaining N` with N < 5 | STOP at Wave 0 step 0.9 with `"budget too low for reflect"`; emit `budget_forced_stop: true` | None |
| `--budget-remaining N` triggers tier downgrade | Run T1 only; emit `budget_forced_tier_downgrade: true`, `forced_tier: 1`; WARN | Continue with T1 only |
| Wave 1B.3 cross-task interaction scan exceeds top-30 symbol cap | Truncate scan at 30; emit `interaction_effects_truncated: true` in audit; symbols beyond cap not analyzed | Continue with truncated scan |
| Wave 1B.3 `find_referencing_symbols` fails for one or more symbols | Skip just that symbol; record per-symbol skip in audit; do NOT abort entire scan | Continue |
| Wave 7 source path no longer exists (external mutation) | `promotion_action: failed`, `promotion_fail_reason: source_disappeared`; verdict unaffected | None |
| Wave 7 destination collision, non-identical content (§14.5.5) | `promotion_action: rejected`; diff captured in promotion-log; source untouched | None |
| Wave 7 destination collision, identical content (idempotent re-run) | `promotion_action: already-promoted`; remove source after second SHA verification | None |
| Wave 7 SHA mismatch after move | `promotion_action: failed`, `promotion_fail_reason: sha_mismatch`; attempt inverse `mv` to restore source | None |
| Wave 7 adapter resolution ambiguous OR neither matches | `promotion_action: skipped`, `promotion_skip_reason: adapter-unresolved` | None |
| Wave 7 strict gate fails | `promotion_action: skipped`, `promotion_skip_reason: gate-failed`; gate_evaluation table shows which condition failed | None |
| Wave 7 `--no-promote` set | `promotion_action: skipped`, `promotion_skip_reason: user-flag` | None |
| Wave 7 `--promote-anyway` used on `status: failed` | Override has NO effect; promotion still skipped with gate-failed | None |
| Wave 7 cross-filesystem mv required | Allowed via copy + remove + fsync; emit `cross_fs_promotion: true`; SHA-verify after copy | None |
| Env-var alias set re-resolves differently between Wave 0 and Wave 3 (race) | STOP at Wave 3A reviewer composition; emit `alias_set_changed_mid_run: true` with old/new alias sets in audit; `status: partial`; recommend re-run with stable env. Wave 0 alias set is canonical. | None |
| All Tier 2 reviewers AND calibrator fail (compound failure) | F3: cannot continue with zero calibrated cards; emit `status: failed` with `failure_reason: "T2_full_collapse"`; do NOT silently emit `status: partial`. Tier 3 remediation handoff disabled. | None |
| Serena `write_memory` fails at Wave 5 (disk full, permission denied, serena down) | Continue: report still ships; emit `memory_persist_failed: true` in telemetry; emit WARN: `"deviation-pattern memory not persisted — next reflect run will not benefit from this run's findings."` Memory persistence is best-effort. | None |
| FR-3 Wave-6 handoff persist (Tier 3) — `prepare_for_new_conversation` context-excluded | Continue: fall back to `mcp__serena__write_memory` with an inline summary blob; emit `handoff_persist_method: write_memory_fallback`; still pass the key to task-builder. | None |
| FR-3 Wave-6 handoff persist — BOTH `prepare_for_new_conversation` AND `write_memory` fail | Continue: report still ships; emit `handoff_persist_failed: true`; surface findings to task-builder WITHOUT the handoff key (task-builder warm-starts cold); WARN. Never block. | None |
| `<output>/audit.log` write failure (filesystem full, permission denied) | Attempt fallback: write to `/tmp/sc-reflect-audit-<pid>.log` AND emit chat WARN. If fallback also fails, continue silently for that step but emit `audit_log_partial: true` in the return contract. Audit-log failure does NOT block the report from shipping but DOES force `status: partial` and blocks Wave 7 promotion. | Fallback path |
| Post-Wave-5 evidence-validator returns partial result (subprocess emitted SOME findings then crashed) | Distinct from full-crash row (which falls back to inline re-Read of all citations). Here the validator processed K of N citations and then crashed. Accept the K processed results; for the remaining N-K, fall back to inline re-Read; emit `evidence_validator_partial: true` with `evidence_validator_processed_count: K`; force `status: partial`; add Grounding Gap entry. | Inline re-Read for the unprocessed N-K |

(See `refs/ops-integration.md` for the operator-facing WARN-message catalog and `refs/promotion-adapters.md` for the full Wave 7 collision-rules table.)

---

## 14.5 Post-Verdict Promotion Mutation (UC-2 only — Wave 7)

Reflect is the **final QA gate** between the executor and the archive. When UC-2 verification passes strictly, the validated work-unit folder moves from its in-progress location to its completed location, closing the loop with `/task-builder` → `/task` → `/sc:reflect` → archive and the analogous loop for `superclaude sprint run`.

**SRP boundary (architectural).** Wave 7 is the **only** wave that mutates repository state outside `<output>/`. Every preceding wave (0-6) is read-only with respect to the repository — they read source files, write artifacts under `<output>/`, and never modify the work-unit tree. Wave 7 is a structural sibling to the review waves, not an extension; it inherits a different correctness regime (atomicity, rollback, partial-state recovery) than the read-only waves. Implementations SHOULD treat Wave 7 as a separately-gated code path: any change to Wave 7's mutation steps (7.4 mv, 7.3.5/7.3.6 pre-writes, 7.5 SHA verification) requires the §14.5.7 acceptance assertions to re-pass; changes to Waves 0-6 do not. The §14.5.2 9-condition gate is the boundary that separates the two regimes.

### 14.5.1 Two registered promotion adapters (v1.0)

| Adapter | Source path glob | Destination path | Trigger signal |
|---------|------------------|------------------|----------------|
| `task` | `.dev/tasks/to-do/TASK-*` | `.dev/tasks/done/TASK-*` | `--tasklist` resolves under `.dev/tasks/to-do/<TASK-DIR>/` AND tasklist frontmatter has a `status` field |
| `sprint-release` | `.dev/releases/current/<release>/` | `.dev/releases/complete/<release>/` | `--scope` or `--tasklist` resolves under `.dev/releases/current/<release>/` |

Adapter selection is deterministic from the resolved input path; if both apply or neither applies, promotion is suppressed (`promotion_action: skipped`, reason logged). Full adapter table lives in `refs/promotion-adapters.md` (load-on-demand at Wave 7).

### 14.5.2 Default-on with strict 9-condition gate

Promotion fires only when ALL of the following hold:

1. **`mode == post`** — UC-1 has no completed work to promote. *(maps to `gate_evaluation.mode_post`)*
2. **`status == success`** — `partial` or `failed` blocks promotion. (Conditional-CONVERGED per §11.0 is NOT eligible.) *(maps to `gate_evaluation.status_success`)*
3. **`tasklist_completion_pct == 1.0`** — every checklist item independently verified done by reflect (not just frontmatter-declared). *(maps to `gate_evaluation.tasklist_completion_pct_1_0`)*
4. **`deviation_count_by_class.drift == 0` AND `deviation_count_by_class.regression == 0`** — Authorized expansion and Necessary deviation are non-blocking; Drift and Regression block. **Exception**: if the only Drift signal is the frontmatter-mismatch from condition 5b AND that mismatch is classifiable as §10.2 Necessary deviation (e.g., frontmatter carries an inline rationale that does not contradict any spec acceptance criterion), it is NOT counted as Drift here — but condition 5b still independently gates promotion. **Reuse-Miss clause (§10.8):** a Reuse-Miss finding mapped to Drift or Regression at rung L3 increments `deviation_count_by_class.drift`/`.regression` like any deviation of that class and gates promotion through this UNMODIFIED condition; advisory Reuse-Miss findings (rung ≤ L2, or any auggie-unavailable fallback) do NOT increment these counters and do NOT gate. *(maps to `gate_evaluation.no_drift_no_regression`)*
5. **Frontmatter agreement** — split into two independent sub-conditions:
   - **5a. Frontmatter is present and parseable** — the tasklist file MUST have a `status` field (or equivalent completion marker per the adapter's frontmatter schema). Missing/unparseable frontmatter fails 5a regardless of value. *(maps to `gate_evaluation.frontmatter_present`)*
   - **5b. Frontmatter status agrees with reflect's verdict** — `status: done` (or equivalent terminal value) MUST be declared. Any other value (including `in-progress`, `partial`, blank, etc.) fails 5b. Disagreement is recorded as Drift (§10.3) in the deviation register regardless of promotion outcome, but does not redundantly increment cond 4 (see cond 4 exception). *(maps to `gate_evaluation.frontmatter_status_matches`)*
6. **`citations_dropped == 0` AND grounding-gaps.yaml is empty** — evidence-validator gate clean. **Empty** is defined precisely (single canonical definition consumed by both §10.6 and §14.5.2): the file is "empty" if and only if (i) `grounding_gaps_path == null` (file was never created), OR (ii) the file exists and parses to a zero-element YAML list (i.e., `findings: []` or a top-level empty document), OR (iii) the file exists with zero non-comment, non-blank lines. Interpretations (a) "empty path string", (b) "zero-byte file alone", or (c) "header-only with no rows but file >0 bytes" are NOT sufficient by themselves — the YAML-parse check (ii) is the authoritative interpretation; (i) and (iii) are accepted only when the YAML parser would also return zero elements. This same definition is referenced by §10.6's "non-empty" predicate (which forces `needs_human_decision: true` and `status: partial`). The two MUST agree on the same file by construction.

   For clarity in the 1:1 mapping, condition 6 is treated as two atomic sub-conditions:
   - **6a. `citations_dropped == 0`** *(maps to `gate_evaluation.no_citations_dropped`)*. In `citation_budget_policy: sampled` mode, this check uses the **sample-count** (`citations_dropped` as defined in §9.1, the COUNT of drops observed in the re-Read sample), NOT the extrapolated projection (`citations_dropped_extrapolated`). The extrapolated field is recorded for telemetry only and does not gate promotion.
   - **6b. grounding-gaps.yaml is empty** per the canonical "empty" definition above *(maps to `gate_evaluation.no_grounding_gaps`)*.
7. **`input_drift_detected == false`** — input SHA stable across the run (§4.0 Step 0.4). *(maps to `gate_evaluation.no_input_drift`)*
8. **`needs_human_decision == false` AND `user_decision_required == false`** — no flagged ambiguity. *(maps to `gate_evaluation.no_user_decision_pending`)*
9. **`convergence_score` not null when Tier 2 ran** — if `tier_reached == 2` AND `adversarial_unavailable == true` (F3 path, `convergence_score: null`), promotion is blocked regardless of other conditions. Tier-1-only runs satisfy this vacuously (`convergence_score` is null by construction at T1, but `tier_reached == 1` means the gate's adversarial-result clause does not apply). Equivalently: a Tier 2 run with no merged adversarial verdict MUST NOT promote. *(maps to `gate_evaluation.adversarial_result_present`)*

When all 9 hold and `--no-promote` is unset, Wave 7 executes. When conditions 1, 3-9 hold but `status == partial`, `--promote-anyway` can override condition 2 only (conditions 1, 3-9 still apply unmodified).

**Citation revalidation when Wave 6 ran.** If Wave 6 (remediation handoff) executed between Wave 5 and Wave 7, condition 6a's `citations_dropped == 0` check at Wave 7 step 7.2 MUST re-Read every cited file:line via the §11.2 evidence-validator (not trust the Wave 5 result). Wave 6 may have mutated cited files, invalidating the Wave 5 citation invariance. A new telemetry field `citation_revalidation_at_promotion: bool` is emitted: `true` if revalidation ran at 7.2, `false` if it was skipped (only legitimate when Wave 6 did not run).

### 14.5.3 Wave 7 — execution

```
Wave 7:   Promotion Mutation (UC-2 only, conditional on §14.5.2 gate)
          —— SRP boundary: the SOLE mutation phase outside <output>/
            7.1 Resolve adapter (task | sprint-release | none) from source path
            7.2 Re-verify all 9 gate conditions immediately before mutation. If Wave 6
                  ran, re-Read every cited file:line via evidence-validator and
                  recompute citations_dropped against current file state (NOT the
                  Wave 5 result); emit `citation_revalidation_at_promotion: true`.
                  See §14.5.2 cond 6a.
            7.3 Re-verify destination collision rules (§14.5.5)
            7.3.5 If cross-filesystem move required, write promotion-checkpoint.yaml
                  with state=pending; see §14.5.5 partial-state recovery.
            7.3.6 Append promotion-log entry with pending=true (BEFORE the mv);
                  see §14.5.5 promotion-log pre-write.
            7.4 Perform move (§14.5.5 mechanics — atomic on same-fs, copy+verify+remove
                  on cross-fs with checkpoint state transitions pending → copy-complete
                  → move-complete)
            7.5 Re-Read moved files and verify SHA invariance vs pre-move
            7.6 Flip promotion-log entry pending=false; finalize checkpoint state to
                  move-complete; append audit.log row
            7.7 Update return-contract.yaml promotion_* fields
```

The mutation step (7.4) is the only filesystem write reflect performs outside `<output>/`. Every other wave reads from the repo and writes only to the reflect output dir. The new pre-write (7.3.5/7.3.6) and finalization (7.6) steps make the forensic record and the partial-state recovery surface independent of any single point of failure between 7.4 and 7.7.

### 14.5.4 Override flags

| Flag | Default | Effect |
|------|---------|--------|
| `--no-promote` | unset | Suppress Wave 7 entirely; `promotion_action: skipped`, `promotion_skip_reason: user-flag`. |
| `--promote-anyway` | unset | Override gate condition 2 for `status: partial`. **Conditions 1, 3-9 still apply** (including condition 9 on `convergence_score` and the split conditions 5a/5b/6a/6b). No effect on `status: failed`. |
| `--promote-dry-run` | unset | Print the exact `mv` command + gate evaluation; perform no mutation. |
| `--promote-mode <auto\|task\|sprint-release\|none>` | `auto` | Force a specific adapter or disable selection. |
| `--promote-resume <checkpoint-path>` | unset | Resume an interrupted cross-fs promotion from `<output>/promotion-checkpoint.yaml`. Mutually exclusive with `--no-promote`, `--promote-anyway`, `--promote-dry-run`. Does NOT re-run the verdict pipeline or re-evaluate the 9-condition gate. See §14.5.5 partial-state recovery. |

### 14.5.5 Mutation mechanics + collision rules

**Move semantics (atomicity is filesystem-dependent).** Use `mv <source> <destination>`. **Atomicity holds where the filesystem permits**: on same-filesystem moves, POSIX `rename(2)` is atomic — the destination either appears in full or not at all, and the source disappears in the same syscall. **On cross-filesystem moves**, the operation is implemented as copy + verify + remove + fsync, which is **NOT atomic**: there is a window between the copy completing and the source removal during which BOTH source and destination exist on disk. NOT `rsync` (non-atomic and not what `mv` invokes). Cross-fs moves emit `cross_fs_promotion: true` into the promotion-log and are gated by the checkpoint mechanism specified below.

**Pre-mutation checkpoint and partial-state recovery (cross-filesystem).** Because cross-fs moves have a non-atomic copy window, Wave 7 step 7.3.5 (inserted between 7.3 collision-check and 7.4 mv) MUST write `<output>/promotion-checkpoint.yaml` BEFORE invoking the copy. The checkpoint shape is:

```yaml
checkpoint_version: "1.0"
adapter: task | sprint-release
source: <abs path>
destination: <abs path>
intended_action: moved
cross_fs: bool
source_sha256_before: <hex>
copy_started_at: <ISO-8601>
copy_completed_at: <ISO-8601> | null   # written after copy succeeds, before remove
state: pending | copy-complete | move-complete | aborted
```

On normal completion, the checkpoint's `state` field transitions `pending` → `copy-complete` (after fsync) → `move-complete` (after source removal). On process crash, the checkpoint persists on disk, and the operator can detect orphan state by checking whether source exists AND destination exists at the recorded paths:

| state at crash | source exists | destination exists | Recovery action |
|----------------|---------------|--------------------|-----------------|
| `pending` (crash during copy) | yes | partial/missing | Operator/reflect deletes partial destination; rerun reflect (idempotent re-promotion will re-check the gate). |
| `copy-complete` (crash between copy and remove) | yes | yes (full, SHA matches) | `--promote-resume` completes the move (verifies SHA, removes source, transitions to `move-complete`). |
| `move-complete` | no | yes | Promotion already succeeded; checkpoint can be archived. No action. |
| `aborted` | indeterminate | indeterminate | Manual operator review — checkpoint records the cause in a `abort_reason` field. |

**`--promote-resume` flag.** When invoked with `--promote-resume <promotion-checkpoint-path>`, reflect reads the checkpoint and performs ONLY the recovery action above — it does NOT re-run the verdict pipeline or re-evaluate the 9-condition gate (the gate was satisfied when the checkpoint was written; re-evaluating could fail if Wave 6 or external mutation has since changed state, leaving the operator with no resolution path). `--promote-resume` is mutually exclusive with `--no-promote`, `--promote-anyway`, and `--promote-dry-run`.

**Promotion-log pre-write (atomicity of the forensic record).** Step 7.6 (append promotion-log) MUST be split: a `pending: true` log entry is written BEFORE step 7.4 (the mv), and is flipped to `pending: false` after step 7.5 (post-move SHA verification). This ensures that if 7.4 succeeds but the 7.6 finalization write fails (disk full, permission denied, process crash), the forensic record still exists with `pending: true` — the next reflect invocation MUST detect a `pending: true` log entry whose `destination` path now exists and `source` path does not, treat it as a `move-complete` state, and emit a one-line warning to the audit log so the operator can reconcile.

**Destination collision rules.**

| Condition | Behavior |
|-----------|----------|
| Destination does not exist | Proceed |
| Destination exists, empty dir | Remove empty destination, then move (audit-logged) |
| Destination exists, non-empty, differs from source | STOP: `promotion_action: rejected`, `destination_collision`; diff captured. Do NOT auto-suffix or overwrite. |
| Destination exists, non-empty, identical to source | Idempotent: `promotion_action: already-promoted`; remove source after second SHA verification |
| Source path no longer exists at Wave 7.4 | FAIL: `promotion_action: failed`, `source_disappeared` |
| Destination parent dir missing | Create parent; emit audit row |
| Both source AND destination exist with matching SHA AND a `pending: true` promotion-log entry references them | Treat as crash recovery: emit `promotion_action: resumed`; complete source removal; flip log entry to `pending: false`. Only fires under `--promote-resume`. |

**Rollback.** Every promotion-log entry includes the inverse `mv` command. Reflect itself never auto-rolls-back (deferred to v1.1 — see §19).

**Git status.** Reflect does NOT `git add` moved files. Operator stages and commits.

### 14.5.6 Output: `promotion-log.yaml`

Written every time Wave 7 runs (even on reject/skip/dry-run):

```yaml
promotion_log_version: "1.0"
adapter: task | sprint-release | none
mode: auto | forced-task | forced-sprint-release | forced-none
action: moved | skipped | rejected | failed | already-promoted | resumed | dry-run
source: <abs path>
destination: <abs path> | null
source_sha256_before: <hex>        # tree-hash via find + xargs sha256sum, sorted
source_sha256_after_move: <hex>    # only on action=moved
sha_match: true | false | null
gate_evaluation:                       # 11 atomic fields, 1:1 with the 9 numbered conditions in §14.5.2 (conditions 5 and 6 each have a/b sub-conditions per the structural split)
  mode_post: pass | fail                            # cond 1
  status_success: pass | fail                       # cond 2
  tasklist_completion_pct_1_0: pass | fail          # cond 3
  no_drift_no_regression: pass | fail               # cond 4
  frontmatter_present: pass | fail                  # cond 5a
  frontmatter_status_matches: pass | fail           # cond 5b
  no_citations_dropped: pass | fail                 # cond 6a
  no_grounding_gaps: pass | fail                    # cond 6b
  no_input_drift: pass | fail                       # cond 7
  no_user_decision_pending: pass | fail             # cond 8
  adversarial_result_present: pass | fail | n/a     # cond 9; "n/a" when tier_reached == 1
gate_evaluation_failures: [<list>]     # derived convenience: names of `gate_evaluation` keys whose value is `fail`. Empty list when `gate_passed: true`. The eval-workspace `yaml_list_contains` assertions consume this; emitted byte-1:1 with the `gate_evaluation` map so the two cannot drift.
gate_passed: bool
citation_revalidation_at_promotion: bool   # true when Wave 6 ran AND step 7.2 re-Read cited files; see §14.5.2 cond 6a
pending: bool                              # true between step 7.4 start and step 7.5 SHA verification; false after; see §14.5.5 promotion-log pre-write
cross_fs_promotion: bool                   # true when source and destination are on different filesystems; see §14.5.5 partial-state recovery
checkpoint_path: <abs path> | null         # path to promotion-checkpoint.yaml when cross_fs_promotion is true; null otherwise
skip_reason: user-flag | gate-failed | adapter-unresolved | dry-run | null
fail_reason: source_disappeared | destination_collision | mv_error | sha_mismatch | null
override_used: --promote-anyway | null
rollback_command: "mv <destination> <source>"   # only on action=moved
timestamp: <ISO-8601>
```

### 14.5.7 Acceptance assertions (eval-workspace)

Wired into `.dev/eval-workspaces/sc-reflect/evals/`:

- **promotion-task-strict-pass**: complete `.dev/tasks/to-do/TASK-EVAL-001/`, all 9 gates pass → `action: moved`, destination exists, source removed.
- **promotion-blocked-by-drift**: 1 Drift entry → `action: rejected`, `no_drift_no_regression: fail`.
- **promotion-blocked-by-frontmatter-missing**: tasklist has no `status` frontmatter field → `action: rejected`, `frontmatter_present: fail`.
- **promotion-blocked-by-frontmatter-mismatch**: reflect verifies done but frontmatter says `in-progress` → `action: rejected`, `frontmatter_status_matches: fail`, Drift entry logged.
- **promotion-blocked-by-grounding-gaps-empty-list**: grounding-gaps.yaml exists with `findings: []` → `action: moved` (canonical "empty" definition); separately, with `findings: [{...}]` → `action: rejected`, `no_grounding_gaps: fail`.
- **promotion-blocked-by-null-convergence**: `tier_reached == 2 AND convergence_score == null` (F3 path simulated) → `action: rejected`, `adversarial_result_present: fail`.
- **promotion-citation-revalidation-after-remediation**: Wave 6 modifies a cited file between Wave 5 and Wave 7 → step 7.2 re-runs evidence-validator and `citations_dropped` is recomputed against current file state; if recomputed `citations_dropped > 0`, `action: rejected`, `no_citations_dropped: fail`, `citation_revalidation_at_promotion: true`.
- **promotion-sprint-release-pass**: `.dev/releases/current/release-X/results/` → destination is `.dev/releases/complete/release-X/`, parent created.
- **promotion-collision-non-identical**: differing destination → `action: rejected`, source untouched, diff captured.
- **promotion-collision-identical**: idempotent re-run → `action: already-promoted`, source removed.
- **promotion-no-promote-flag**: `--no-promote` → `action: skipped`, `skip_reason: user-flag`.
- **promotion-promote-anyway-on-partial**: `status: partial` + `--promote-anyway` → `action: moved`, `override_used: --promote-anyway`.
- **promotion-dry-run**: `--promote-dry-run` → `action: dry-run`, no mutation, mv command printed.
- **promotion-cross-fs-crash-recovery**: simulate process death between step 7.4 copy and step 7.4 remove on cross-fs path → re-invoke with `--promote-resume <checkpoint>` → `action: resumed`, source removed, destination intact, log entry flipped to `pending: false`.
- **promotion-log-pre-write-survives-crash**: simulate crash between step 7.4 (move success) and step 7.6 (finalize) → next invocation detects `pending: true` log entry with destination-exists and source-missing → emit reconciliation warning, flip to `pending: false`, no double-move.

New grader assertion types required (in addition to the 8 inherited): `path_exists` and `path_does_not_exist`. Both are short Python additions to `grader.py` per §17.5.

### 14.5.8 Interaction with §10 Deviation Taxonomy

Frontmatter-vs-verdict mismatch (gate condition 5b) is a first-class **Drift** signal in §10.3 — the gate just consumes it. Reflect's independent verification is canonical; tasklist frontmatter is a *claim* that must agree. Disagreement is executor-side Drift, recorded in the deviation register regardless of promotion outcome. Per the cond 4 exception (§14.5.2), a frontmatter mismatch with inline rationale can be reclassified as §10.2 Necessary deviation — that does NOT bypass cond 5b (which independently gates promotion on the mismatch itself), but it prevents the same mismatch from being double-counted as Drift in cond 4.

---

## 15. Token Cost Profile

| Path | Auggie (offloaded) | Claude (orchestration + agents) | Wall clock | Turn-budget midpoint |
|------|-------------------|---------------------------------|------------|----------------------|
| T1 only | ~2-5k | ~3-8k | 1-3 min | ~6 turns (`T1-midpoint`) |
| T2 (2-3 reviewers + adversarial debate) | ~10-25k | ~35-70k | 8-15 min | ~52 turns (`T2-midpoint`) |
| T3 added | +0 | +20-40k | +5-10 min | +~30 turns |

Targets, not caps. Hard kill at 1.25× estimate per sc-brainstorm convention. (D13 note: in UC-1 the qa-persona reviewer brief now carries the spec body as grounding hunks per `refs/reviewer-spec.md`, adding roughly spec-length tokens to ONE T2 reviewer's brief; the T2 band already absorbs typical spec sizes, but very large specs push toward the band's upper edge.)

**Token-to-turn conversion (consumed by §4.0 Step 0.9 budget routing).** The midpoint values are derived as: `turns ≈ claude_tokens_midpoint / 1000`, i.e., `1 turn ≈ 1k claude-orchestration tokens` at the band midpoint. This conversion is the load-bearing assumption behind §4.0 Step 0.9's `T1-midpoint = 6` and `T2-midpoint = 52` integer anchors. The conversion is approximate (real turn-to-token ratios vary with prompt complexity, tool-call density, and per-call overhead), but is fixed for the purpose of budget-routing arithmetic — callers should NOT recompute it. If §15 band midpoints change, §4.0 Step 0.9 anchors MUST be updated in lockstep. (The machine-readable mirror of this table is `refs/cost-profile.yaml`, regenerated via `make sync-cost-profile`.)

### 15.1 Metrics Export

Reflect emits a structured metrics file at `<output>/metrics.json` (and appends a one-line summary to a global `.dev/reflect/runs.jsonl` for cross-run aggregation per the §9.3 meta-eval consumer row). The metrics file is **separate from the return contract** — the contract is the per-run verdict surface; metrics are the cross-run operational signal.

**Schema (`<output>/metrics.json`):**

```json
{
  "metrics_schema_version": "1.0",
  "run_id": "<ISO-8601-timestamp>-<short-hash>",
  "skill": "sc-reflect",
  "skill_version": "<contract_version from §9.1>",
  "mode": "pre | post",
  "tier_reached": 1 | 2 | 3,
  "status": "success | partial | failed | dry-run",
  "wave_durations_ms": {
    "wave_0": <int>, "wave_1": <int>, "wave_2": <int>,
    "wave_3": <int>, "wave_4": <int>, "wave_5": <int>,
    "wave_6": <int>, "wave_7": <int>
  },
  "wall_clock_ms": <int>,
  "token_usage": {
    "claude_orchestration": <int>,
    "claude_agents": <int>,
    "auggie_offloaded": <int>,
    "total": <int>
  },
  "calibration": {
    "calibrator_diversity": "full | degraded",
    "calibrated_confidence_initial": <float>,
    "calibrated_confidence_final": <float>,
    "calibration_delta": <float>
  },
  "ensemble": {
    "t2_model_class_diversity": "full | degraded",
    "t2_vendor_diversity": "multi | single",
    "t2_effective_diversity": "full | model-only | vendor-only | none",
    "reviewer_count": <int>,
    "executor_class_resolved": <bool>,
    "executor_exclusion_degraded": <bool>
  },
  "evidence_validator": {
    "ran": <bool>,
    "citations_total": <int>,
    "citations_revalidated": <int>,
    "citations_dropped": <int>,
    "citations_dropped_extrapolated": <int>,
    "drop_rate": <float>,
    "budget_policy": "full_reread | sampled"
  },
  "deviation_counts": {
    "authorized": <int>,
    "necessary": <int>,
    "drift": <int>,
    "regression": <int>,
    "total": <int>
  },
  "adversarial": {
    "convergence_score": <float | null>,
    "merge_method": "adversarial | single-reviewer-fallback",
    "adversarial_unavailable": <bool>,
    "fallback_path": "null | F1 | F2 | F3"
  },
  "promotion": {
    "action": "moved | skipped | rejected | failed | already-promoted | resumed | dry-run | not-applicable",
    "gate_conditions_passed": <int>,
    "gate_conditions_total": 9,
    "cross_fs": <bool>
  },
  "degraded_components": [<list of strings>],
  "input_drift_detected": <bool>,
  "needs_human_decision": <bool>
}
```

**Prometheus / StatsD / OpenTelemetry-friendliness.** The schema deliberately uses flat numeric leaves at the inner level (no nested objects below the top-level groups) so that conventional flatteners can produce metric names like:

```
sc_reflect_wave_durations_ms_wave_0
sc_reflect_evidence_validator_citations_dropped
sc_reflect_promotion_gate_conditions_passed
sc_reflect_deviation_counts_regression
sc_reflect_ensemble_reviewer_count
```

Operators using Prometheus's `json_exporter`, StatsD's `dogstatsd-json`, or OpenTelemetry's `json-receiver` can ingest `metrics.json` directly with a 1-line config (consume all top-level groups; flatten with `_` separator). Counter vs gauge classification (for those consumers that care):

- **Counters (monotonic):** `wall_clock_ms`, `token_usage.*`, `evidence_validator.citations_*`, `deviation_counts.*`, `promotion.gate_conditions_passed`.
- **Gauges (snapshot):** `tier_reached`, `calibration.calibrated_confidence_*`, `adversarial.convergence_score`, `evidence_validator.drop_rate`.
- **Strings (labels in PromQL):** `status`, `mode`, `*_diversity` enums, `promotion.action`, `adversarial.merge_method`.

**Cross-run aggregation (`.dev/reflect/runs.jsonl`).** A one-line JSON summary is appended to `.dev/reflect/runs.jsonl` at end-of-run. Schema is a subset of `metrics.json` with only the cross-run-comparable fields:

```json
{"run_id": "...", "timestamp": "...", "skill_version": "1.5.0", "mode": "post", "tier_reached": 2, "status": "success", "wall_clock_ms": 124000, "token_usage_total": 47832, "calibration_delta": -0.03, "convergence_score": 0.82, "evidence_validator_drop_rate": 0.0, "deviation_counts_regression": 0, "promotion_action": "moved"}
```

The `.dev/reflect/runs.jsonl` file is **append-only** and used by:

- Meta-eval (§9.3 row 9) — cross-run trending of calibration drift, convergence-score distribution, drop-rate.
- CI dashboards — long-running visibility into reflect quality regression.
- Operator scripts — `jq` queries like `jq '.[] | select(.status=="failed")' .dev/reflect/runs.jsonl` for failure analysis.

`.dev/reflect/runs.jsonl` is **gitignored** by convention (the path is per-machine, not per-repo state). The append-write is best-effort: if the global file is unwritable, reflect logs a WARN and continues — the per-run `metrics.json` is the authoritative copy.

**Stability guarantee.** The `metrics_schema_version` field is governed by §9.4 contract-evolution rules: additive changes bump minor, renames/removals bump major. The schema is forward-compatible at the consumer level via the same unknown-field-tolerance rule as §9.4.

---

## 16. Refs (loaded on-demand per wave)

| File | Wave | Purpose |
|------|------|---------|
| `refs/input-resolution.md` | Wave 0 | Mode auto-detection rules, STOP conditions, slug generation |
| `refs/reflection-rubric.md` | Wave 1D, Wave 3C | 5-dimension calibration rubric (Citation grounding, Coverage completeness, Deviation-classification clarity, Risk surface coverage, Recommendation actionability) |
| `refs/deviation-taxonomy.md` | Wave 1B (UC-2), Wave 5 | The 4-category taxonomy with detection signals, gold-standard refs, default remediations |
| `refs/coverage-mapping.md` | Wave 1B (UC-1) | Spec-to-tasklist coverage map algorithm; bipartite matching heuristics; `S_dev_density` calculation |
| `refs/reviewer-spec.md` | Wave 3A | Model + persona rotation rules; reviewer card template |
| `refs/report-template.md` | Wave 5 | Final REPORT.md skeleton with Grounded vs [INFERRED] tagging conventions. **(P4) MANDATORY**: when `per_task_verdicts` length ≥ 2, the template emits a `## Per-Task Verdicts` section with one subsection per task (verdict block + deviation attribution + evidence anchor). Lifted directly from the contract array; no separate computation. |
| `refs/remediation-handoff.md` | Wave 6 | Task-builder BUILD_REQUEST template; opt-in prompt |
| `refs/ops-integration.md` | (build-time) | Makefile targets (`make sync-dev`, `make verify-sync`, `make reflect-eval`), CI cadence, PreToolUse hook redirect message body, vendor-heterogeneity WARN body (per §4 Wave 0 step 0.6) |
| `refs/grader-extensions.md` | (eval-time) | Python implementation sketch for `citation_resolves` with fixture-root remapping + the 6 grader DSL semantic types + new `path_exists` / `path_does_not_exist` assertion types (per §14.5.7) |
| `refs/promotion-adapters.md` | Wave 7 | Full adapter table (`task`, `sprint-release`, operator-added); collision-rule mechanics body; `mv` invocation template; rollback command template (per §14.5) |
| `refs/cost-profile.yaml` | (pre-invocation) | **(P7)** Static, machine-readable mirror of the §15 Token Cost Profile table. Callers (sprint TurnLedger, CI) read this BEFORE invoking reflect to pre-flight budget. Reflect itself never reads this at runtime — the file is for caller-side discovery only. Updated in lockstep with §15 by a `make sync-cost-profile` target (see `refs/ops-integration.md`). |

Refs loaded by the wave that needs them; never pre-loaded. Session-start footprint: SKILL.md only (~50 tokens via Claude Code skill loader).

---

## 17. Boundaries

### Will

- Run T1 always; respect "quick first" contract.
- Auto-escalate to T2 only when the rubric in §5 says so, or when `--tier 2`/`--depth deep` is set.
- Fan out heterogeneous reviewers (different model classes) in Tier 2 to break representational-bias self-confirmation.
- Use modern Serena symbolic chain (`get_symbols_overview` → `find_symbol` → `find_referencing_symbols`) for evidence; wire `think_about_*` as scripted nudges captured to audit, never as the gating signal.
- Run `evidence-validator` as a non-negotiable final gate before any report ships; treat a zero-drop pass as a flag, not a clean signal.
- Classify every UC-2 deviation under the 4-category taxonomy in §10 with explicit detection signals and gold-standard references.
- Route evidence-insufficient findings to `grounding-gaps.yaml` (§10.6), NOT to a 5th deviation category.
- Tag every claim as Grounded or `[INFERRED]`; drop claims that fit neither bucket.
- Respect CLAUDE.md ABSOLUTE RULES: source-of-truth is `src/superclaude/`, never commit `.claude/` mirrors, PR target is fork only.
- Fail-open on missing MCPs (auggie, serena, context7, tavily) — fall back to native tools and mark degraded.
- Tavily evidence searches via `mcp__tavily__tavily-search` inherit the server-level DEFAULT_PARAMETERS (C1) baseline — reflect passes no per-call overrides (unlike the troubleshoot Tier-2 advanced override).
- Persist deviation patterns to per-project Serena memory with 90-day expiry.
- Delegate debate / scoring / merge to `sc-adversarial-protocol`; never re-implement.
- **Promote validated work-units** (UC-2 only, Wave 7 Promotion Mutation) via the §14.5 strict 9-condition gate (with 11 atomic gate_evaluation fields — sub-splits 5a/5b/6a/6b per §14.5.6): move `.dev/tasks/to-do/TASK-*` → `.dev/tasks/done/TASK-*` and `.dev/releases/current/<release>/` → `.dev/releases/complete/<release>/` when the gate passes. Default-on, `--no-promote` to suppress. Atomic `mv` where filesystem permits (cross-fs uses checkpoint+copy+verify+remove per §14.5.5), SHA-verified, rollback command preserved in promotion-log.
- Write a `promotion-log.yaml` every time Wave 7 runs (even on skip/reject/fail/dry-run) for forensic transparency.
- Refuse promotion on destination-collision with non-identical content (no auto-suffix, no overwrite); record the diff for human resolution.
- **Emit per-task verdicts** (P1+P2) in the contract when UC-2 input is a multi-task tasklist, including `per_task_validation_strength` (calibrated 0.0-1.0) suitable for downstream credit-allocation logic.
- **Scan for cross-task interaction effects** (P3) in Wave 1B.3 when UC-2 tasklist has ≥3 tasks — the differentiating value of end-of-tasklist reflect vs N per-task reflects.
- **Honor caller-side budget hints** (P5) via `--budget-remaining` and auto-degrade tier per §4.0 step 0.9.
- **Publish a static cost-profile ref** (P7) at `refs/cost-profile.yaml` so callers can pre-flight check before invoking.

### Will Not

- Run reflection on its own intermediate output without explicit `--recursive` flag and a token-budget envelope (prevents unbounded sub-skill recursion).
- Trust agent-reported self-confidence; always re-grade via `confidence-calibrator` (or inline fallback).
- Ship a report whose `file:line` citations have not passed through `evidence-validator` (or the inline fallback with `status: partial` marker).
- Auto-execute a Tier 3 remediation task — task-builder produces a file, the user runs `/task <path>`.
- Auto-commit after Tier 3.
- Silently downgrade missing skills (sc-adversarial, task-builder) — STOP with explicit install instruction (per sc-brainstorm Wave 0 pattern).
- Treat the executor's commit message as the gold-standard reference for "what was expected" — that is reviewer-side narrative, not spec.
- Skip the heterogeneous-model requirement at Tier 2 — 3× the same model class defeats the purpose of escalation.
- Confirm its own conclusions: a zero-drop evidence-validator pass on a non-trivial report is an audit flag, not a green light.
- Use the `think_about_*` triad as load-bearing — they are nudges, not evidence.
- Operate against `.claude/{skills,commands,agents}/*` paths as output sinks (CLAUDE.md ABSOLUTE RULE).
- **Auto-promote a `status: partial` or `status: failed` run** without `--promote-anyway` (and `--promote-anyway` has no effect on `status: failed`). Drift, Regression, citation drops, or grounding gaps hard-block promotion.
- **Promote without verifying frontmatter agreement.** Tasklist frontmatter `status: done` is a claim that must agree with reflect's independent verification.
- **Auto-overwrite or auto-suffix on destination collision.** Identical content = idempotent re-promotion; differing content = hard reject with diff capture.
- **Auto-roll back a successful promotion.** Rollback is operator-driven via the inverse `mv` command preserved in promotion-log. Auto-rollback is v1.1 scope (§19).
- **`git add` after promotion.** Filesystem-level move only; the operator stages and commits.
- **Emit `tasklist_aggregate` enum** (rejected P1 sub-proposal — adversary correctly identified it as redundant with `status` + `deviation_count_by_class`). Downstream computes the gestalt from existing fields.
- **Emit a separate top-level `validation_strength` field** (rejected P2 split — folded into `per_task_verdicts[].per_task_validation_strength` to avoid duplication with `confidence_calibrated`).
- **Stream per-task verdicts as they're emitted** (deferred P6 — see §19.4). Batch-emit at end of run is sufficient for v1.0.
- **Maintain cross-tasklist deviation-pattern memory** (deferred P8 — see §19.5). Existing per-project memory namespace is sufficient for v1.0.
- **Apply caller-side credit policy** (P5/P7 scope boundary). Reflect publishes calibrated numbers (`per_task_validation_strength`) and cost estimates (`refs/cost-profile.yaml`); the caller's ledger owns the credit-allocation arithmetic. Reflect never returns a turn-credit amount.

---

## 17.5 Ops Integration

This section codifies the build/CI/hook discipline that surrounds the skill. Detailed Makefile target tables, full CI cadence, and the full vendor-heterogeneity WARN body live in `refs/ops-integration.md` (load on-demand at build time).

**The `-f` rule (CLAUDE.md ABSOLUTE).** If `git add` requires `-f` on any `.claude/` path (except `.claude/settings.json`), that `-f` is the violation siren. STOP. Move the change to `src/superclaude/`, run `make sync-dev`, stage only the `src/` side. See memory `feedback_claude_dir_gitignored.md`.

**PreToolUse hook awareness.** The `.claude/settings.json` PreToolUse hook rejects writes to `.claude/skills/*-workspace/**` with a redirect to `.dev/eval-workspaces/<skill-name>/`. This skill's eval workspace MUST land at `.dev/eval-workspaces/sc-reflect/` to pass the hook. The `.gitignore` also matches `.claude/skills/*-workspace/`, so any misplaced workspace cannot be committed.

**`make sync-dev` / `make verify-sync` pre-commit workflow.**

1. Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (and/or `src/superclaude/commands/reflect.md`).
2. Run `make sync-dev` to mirror to `.claude/`.
3. Run `make verify-sync` — must exit 0 (the pre-commit hook also runs this).
4. Run `make lint-architecture` to confirm bidirectional command↔skill link + frontmatter completeness.
5. Stage ONLY `src/` and `.dev/` paths. NEVER stage `.claude/` paths.

**CI cadence.** Run `make reflect-eval-quick` (3 pilot cases, <30s) on every PR touching `src/superclaude/skills/sc-reflect-protocol/` or `src/superclaude/commands/reflect.md`. Full `make reflect-eval` (~2 min) runs on release-candidate branches. See `refs/ops-integration.md` for the full Makefile target table (`make sync-dev`, `make verify-sync`, `make lint`, `make lint-architecture`, `make test`, `make reflect-eval`, `make reflect-eval-quick`, `make eval-skill SKILL=sc-reflect-protocol`).

---

## 17.6 Testability Map

Every load-bearing protocol decision maps to at least one deterministic or qualitative eval assertion. Rows where no mapping is feasible should be simplified or removed.

| Protocol decision | Eval assertion type | Target artifact / field |
|-------------------|---------------------|-------------------------|
| Output-dir guard rejects `.claude/{skills,commands,agents}/` | `regex_absent` in audit + STOP fixture | `audit.log` |
| §3.2 mode auto-detection (6-rule first-match) | `yaml_field` | `return-contract.yaml mode` |
| §4 Wave 0 input_sha256 snapshot | `yaml_field` | `input-snapshot.yaml input_sha256.tasklist` |
| §4 Wave 0 input_drift guard | `yaml_field` | `return-contract.yaml input_drift_detected` |
| §4 Wave 0 alias-routing 0/1/2/3+ | `yaml_field` | `tier_decision.yaml t2_model_class_diversity ∈ {full, degraded}` |
| §4 Wave 0 vendor heterogeneity | `yaml_field` | `return-contract.yaml t2_vendor_diversity ∈ {multi, single}` |
| §4 Wave 1 zero-task guard | `yaml_field` | `return-contract.yaml coverage_undefined == true` |
| §4 Wave 1 coverage_undefined route | `yaml_field` | `return-contract.yaml coverage_pct == null AND tier_reached == 2` |
| §4 Wave 3 reviewer-brief packaging | `dir_count` | `<output>/reviewer-briefs/ min_files=N` |
| §4 Wave 5 sc-adversarial pre-invocation probe | `yaml_field` | `return-contract.yaml adversarial_unavailable` |
| §4 per-step audit emit | `yaml_list_contains` | `audit.log step rows` |
| §5.3 tier rubric rule fired | `yaml_field` | `tier_decision.yaml fired_rule_number` |
| §5.4 composite_score recording | `yaml_field` | `tier_decision.yaml composite_score AND per_signal_breakdown` |
| §6.4 Serena scripted checkpoints | `checkpoint_logged` | `audit.log checkpoint=<name>` |
| §10 deviation taxonomy = 4 categories | `yaml_list_contains` | `deviation-ledger.yaml deviation_class ∈ {authorized, necessary, drift, regression}` |
| §10.6 grounding-gaps parallel artifact | `file_exists` + `yaml_field` | `grounding-gaps.yaml hunk_ref AND needs_human_decision` |
| §11.0 sufficiency-conditional gates | (eval composition) | dimensions #1 / #4 / #5 sub-criteria |
| §11.3 calibrator disjoint-set | `yaml_field` | `reflection-card.yaml calibrator_model_class NOT IN reviewer_model_classes` |
| §11.5 citation-budget policy | `yaml_field` | `return-contract.yaml citation_budget_policy ∈ {full_reread, sampled}` |
| §12.5 falsifier T2-convergence-wrong-answer | `yaml_field` + composite | `return-contract.yaml regression_present AND convergence_score < 0.75` |
| §9.1 versioned return contract stability | `yaml_field` | `return-contract.yaml contract_version == "1.5.0"` |
| §14.5.2 9-condition gate (11 atomic fields after a/b splits) | `yaml_field` (per condition) | `promotion-log.yaml gate_evaluation.*` |
| §14.5.5 cross-fs partial-state recovery | `path_exists` / `path_does_not_exist` + `yaml_field` | `promotion-checkpoint.yaml state` |
| §14.5.7 falsifier skeleton presence | `falsifier_skeleton_present` | `cases/falsifier-suite/T2-converges-on-wrong.yaml` |
| Adversarial delegation artifacts | `dir_count` | `<output>/adversarial/ min_files=6` |
| Citation grounding (final report) | `citation_resolves` | `REPORT.md` |
| Recommendation actionability | `yaml_list_contains` | `recommendation-scrutiny.yaml decision` |
| Memory write optionality | `yaml_substring` | `telemetry memory_status` |

A protocol step that cannot map to at least one row here should be simplified or removed. The Testability Map is the manifest the eval workspace consumes; every row references a real protocol decision in §3-§14.5 (no orphan rows, no orphan decisions).

---

## 17.7 Kill List — Features Deliberately Excluded

Features considered and rejected, each with a why-rejected line and a what-replaces-it pointer.

1. **New `coverage-mapper` agent** — the coverage mapping logic is narrow enough to handle inline in Wave 1; a dedicated agent adds coordination overhead without sufficient complexity reduction. *Replaces with:* `requirements-analyst` (UC-1) + inline Wave 1B logic (UC-2). Extract only if eval shows Wave 1 inline logic is fragile.

2. **New `deviation-classifier` agent** — the 4-class taxonomy is a classification rule over commit messages and task logs, not a deep investigation. Inline is cheaper and more auditable. *Replaces with:* `refs/deviation-taxonomy.md` + `root-cause-analyst` per-card.

3. **Streaming / interactive reflection dialogue** — interactive Socratic probing is `sc:brainstorm`'s core value. sc:reflect is a batch review skill. Adding interactive dialogue would duplicate brainstorm's Wave 1 and dilute reflect's identity as a validation tool. *Replaces with:* `Skill sc-brainstorm-protocol` (upstream).

4. **Persistent deviation knowledge graph** — Serena memory stores the last-pass summary. A full deviation graph with deduplication, temporal trending, and cross-project aggregation is a separate product, not a skill feature. *Replaces with:* `mcp__serena__write_memory key=reflect/deviation-patterns-{slug}` with 90-day TTL (§6.3).

5. **Multi-model fan-out in T1** — T1 is intentionally single-agent and cheap. Heterogeneous multi-model review is a T2/T3 feature. Running parallel models at T1 would violate the "quick first" contract that makes sc:troubleshoot's T1 effective. *Replaces with:* §5 rubric escalation path to T2.

6. **5th `unknown` deviation category in deviation-ledger** — Rejected because structural cleanliness requires the 4-category ledger to remain pure; insufficient-evidence findings route to a *separate* artifact (`grounding-gaps.yaml`) with required-field rigor. *Replaces with:* §10.6 Grounding Gaps parallel artifact.

---

## 18. Spec Reference

Full spec at `.dev/eval-workspaces/sc-reflect/SPEC.md` (authored alongside SKILL.md per skill-creator iteration-1). This SKILL.md is the working protocol; SPEC.md is the design rationale + acceptance criteria + iteration history.

---

## 19. v1.1 Deferred Hardening (INV-021 + INV-023)

Two HIGH invariants are deliberately deferred to a future v1.1 release. They are surfaced here so downstream consumers and meta-eval can track the gap.

### 19.1 INV-021 — Vendor heterogeneity v1.1 hardening

**v1.0 posture:** WARN + telemetry (`t2_vendor_diversity: single | multi`) + eval rubric dimension (≥2 vendors → +1.0; 1 vendor → 0.5). Warn-only. See §4 Wave 0 step 0.6 + §12.2.

**v1.1 candidate hardening:** if iteration-2 eval evidence shows convergence-on-wrong-answer cases correlate with single-vendor T2 (i.e., the `T2-convergence-wrong-answer` case fails more often when all reviewers are one vendor), promote single-vendor to a **BLOCK** with WARN before T2 runs unless `--allow-single-vendor` is set.

**Why deferred:** actually requiring cross-vendor would block most users today (who have only Anthropic aliases). The realistic v1 posture is data-collect via telemetry, then harden once evidence justifies the additional friction.

### 19.2 INV-023 — Sufficiency claim v1.1 hardening

**v1.0 posture:** the §11.0 sufficiency claim is **CONDITIONAL** on three gates (calibrator disjoint-set §11.3, ≥2 vendors §4 Wave 0 step 0.6, falsifier eval §12.5). The falsifier eval case ships in iteration-3 hardening; the conditional language is in §11.0. The **falsifier-suite skeleton ships in v1.0** (§12.5) — directory layout, grader hooks, and YAML shape are present from day-1; iteration-3 only populates the fixture content and promotes `status: skeleton-pending-iteration-3-fixture` → `status: active`.

**v1.1 candidate hardening:** based on first-run results of the `T2-convergence-wrong-answer` case across real eval runs:

- If the case passes ≥80% of runs: tighten language in §11.0 from "conditional" to "demonstrated under these gates."
- If the case fails ≥20% of runs: tighten the §11.3 disjoint-set rule from "degrade to non-disjoint" to "BLOCK at Wave 4" when calibrator class cannot be disjoint from reviewer classes.

**Why deferred:** v1 ships the falsifier eval case (operationalises the claim); v1.1 hardens based on the empirical record. Shipping unconditional sufficiency language in v1 without empirical evidence would be exactly the kind of self-confirming claim this protocol exists to prevent.

### 19.3 Auto-rollback of successful promotion (carryover from §14.5)

**v1.0 posture:** promotion-log preserves the inverse `mv` command but reflect never auto-executes it. Operator-driven rollback only.

**v1.1 candidate hardening:** if iteration-2 eval data shows >0 cases where a promotion was followed by a corrective rollback within 1 hour, add an automatic-rollback path triggered by a post-promotion `/sc:reflect --rollback-last <promotion-log-path>` invocation. Still gated on `confidence-calibrator` confirming the rollback rationale.

**Why deferred:** auto-rollback is dangerous without a clear decision rule for when it fires. v1 keeps the operator in the loop; v1.1 adds rollback only after the data shows a pattern.

### 19.4 Streaming per-task verdict emission (deferred P6)

**v1.0 posture:** `per_task_verdicts` array is emitted in the contract at end-of-run. No streaming.

**v1.1 candidate hardening:** if a real downstream consumer materializes that needs early-halt-on-systemic-failure for large (≥30-task) tasklists, add `<output>/streaming-verdicts.jsonl` emitted as each task verifies. New eval assertion `jsonl_line_count_equals_tasks` verifies streaming completeness.

**Why deferred:** the consumer doesn't exist yet. P1's `per_task_verdicts` array gives end-of-run consumers everything they need. Per spec discipline, don't ship a producer without a known consumer.

### 19.5 Cross-tasklist deviation-pattern memory (deferred P8)

**v1.0 posture:** §17 commits to per-project Serena memory with 90-day expiry for deviation patterns. Scope is per-project, not per-template or per-agent.

**v1.1 candidate hardening:** extend the memory namespace to `reflect/cross-tasklist-patterns/<template-slug-or-agent-id>.md` so recurring patterns across tasklists generated from the same template (or executed by the same agent) surface in subsequent reflect runs.

**Why deferred:** speculative — the existing per-project bucket is sufficient until pattern-recurrence is demonstrated by real data. Adding cross-template/cross-agent scoping is a generalization for a problem that hasn't been demonstrated to exist.
