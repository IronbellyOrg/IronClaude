# Bucket E — sc-adversarial-protocol content digest

## Files read

| Path | Lines | Status |
|------|-------|--------|
| src/superclaude/commands/adversarial.md | 167 | complete |
| src/superclaude/skills/sc-adversarial-protocol/SKILL.md | 2952 | complete (chunked) |
| src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md | 378 | partial (template structure confirmed) |
| src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md | 229 | partial (spec format confirmed) |
| src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md | 258 | partial (5-step overview confirmed) |
| src/superclaude/skills/sc-adversarial-protocol/refs/scoring-protocol.md | 230 | partial (quant layer confirmed) |

## Command wrapper (`commands/adversarial.md`)

- **Mode A — Compare**: 2-10 existing files via `--compare file1,file2[,...,fileN]` (`adversarial.md:14, 21-22, 36-37`).
- **Mode B — Generate + Compare**: from `--source <file> --generate <type> --agents <spec>` (`adversarial.md:15, 25, 39-42`).
- **Pipeline (inline shorthand)**: `--pipeline "<shorthand>"` (`adversarial.md:16, 28, 45-46`).
- **Pipeline (YAML)**: `--pipeline @pipeline.yaml` (`adversarial.md:31, 47`).
- **Argument parsing per mode**: documented at `adversarial.md:35-49`. Mutual exclusivity stated at `adversarial.md:48`.
- **Activation**: MANDATORY skill invocation `Skill sc:adversarial-protocol` before any protocol execution (`adversarial.md:131-135`).

### Flag reference table (Options block `adversarial.md:50-69`)

| Flag | Type | Default | Allowed values | Source line |
|------|------|---------|----------------|-------------|
| `--compare` (`-c`) | comma-separated paths | — (required Mode A) | 2-10 existing files | `adversarial.md:54` |
| `--source` (`-s`) | path | — (required Mode B) | existing file | `adversarial.md:55` |
| `--generate` (`-g`) | string | — (required Mode B) | artifact type (roadmap, spec, design, …) | `adversarial.md:56` |
| `--agents` (`-a`) | comma-separated specs | — (required Mode B) | `model[:persona[:"instruction"]]` | `adversarial.md:57` |
| `--depth` (`-d`) | enum | `standard` | quick / standard / deep | `adversarial.md:62` |
| `--convergence` | float | `0.80` | 0.50-0.99 | `adversarial.md:63` |
| `--interactive` (`-i`) | flag | `false` | true/false | `adversarial.md:64` |
| `--output` (`-o`) | path | Auto | any path (forbidden under `.claude/skills|agents|commands/`) | `adversarial.md:65`; guard at `SKILL.md:41` |
| `--focus` (`-f`) | comma-separated | All | any list (e.g., structure,completeness) | `adversarial.md:66` |
| `--blind` | flag | `false` | true/false | `adversarial.md:67` |
| `--auto-stop-plateau` | flag | `false` | true/false | `adversarial.md:68` |
| `--pipeline` | string | — | inline shorthand or `@path.yaml`; mutually exclusive w/ `--compare`/`--source` | `adversarial.md:58` |
| `--pipeline-parallel` | int | `3` | 1-10 | `adversarial.md:59` |
| `--pipeline-resume` | flag | `false` | true/false | `adversarial.md:60` |
| `--pipeline-on-error` | enum | `halt` | halt / continue | `adversarial.md:61` |

## Skill protocol (SKILL.md)

- **5-step pipeline overview**: declared at `SKILL.md:80-82`; Step 1 Diff Analysis (`:84-123`), Step 2 Adversarial Debate (`:125-208`), Step 3 Hybrid Scoring & Base Selection (`:210-273`), Step 4 Refactoring Plan (`:275-309`), Step 5 Merge Execution (`:311-328`).
- **Mode A behavior — compare 2-10 artifacts**: `SKILL.md:55-65` ("Accepts 2-10 existing files… 2-10 file count enforced"). Validation reinforced at `:554-561` (count_check: `2 ≤ file_count ≤ 10`).
- **Scoring protocol — 5 focus areas, 1-10 scale, max 50/proposal**: NOT present in this form. The skill uses a different scoring structure: hybrid quant (5 metrics RC/IC/SR/DC/SC, 50% weight) + qual (30-criterion additive binary rubric across 6 dimensions, 50% weight) (`SKILL.md:216-269`, `:1546-1692`). The "5 focus areas, 1-10, max 50" description from the prompt does not match the actual skill — flagged in evidence_status.
- **Convergence threshold semantics — `--convergence 0.80`**: Formula `convergence = agreed_points / total_diff_points` (`SKILL.md:1335-1340`). `total_diff_points = count(S-NNN) + count(C-NNN) + count(X-NNN) + count(A-NNN)`. Default 0.80, range 0.50-0.99 (`SKILL.md:1341-1344`, `:334`). Gate condition (`SKILL.md:1365`): "convergence requires: (all_levels_covered == true) AND (score >= threshold) AND (no_high_unaddressed_invariants == true)".
- **Round structure**: Round 1 parallel advocate statements (`SKILL.md:183-187, 1039-1069`); Round 2 sequential rebuttals when depth=standard/deep (`SKILL.md:188-192, 1071-1097`); Round 2.5 invariant probe single-agent fault-finder when depth=standard/deep (`SKILL.md:1099-1242`); Round 3 conditional final arguments when depth=deep AND not converged (`SKILL.md:193-196, 1307-1329`).
- **Standard depth = Round 1 (parallel) + Round 2 (sequential) + Round 2.5 (invariant probe)**: confirmed at `SKILL.md:1075-1076` (Round 2 condition: `--depth standard OR --depth deep`) and `:1104-1105` (Round 2.5 condition: standard or deep). Quick skips Round 2/2.5 (`SKILL.md:1076, 1105`).

## Return contract — output artifacts

**Artifact Output Structure (FR-005)** at `SKILL.md:371-389`:

```
<output-dir>/
├── <merged-output>.md              # Final unified artifact
└── adversarial/
    ├── variant-1-<agent>.md        # Mode A: variant-N-original.md
    ├── variant-2-<agent>.md        # Mode B: variant-N-<model>-<persona>.md
    ├── ...                         # Up to 10 variants
    ├── diff-analysis.md            # Step 1
    ├── debate-transcript.md        # Step 2
    ├── base-selection.md           # Step 3
    ├── refactor-plan.md            # Step 4
    └── merge-log.md                # Step 5
```

Also emitted: `invariant-probe.md` (Round 2.5 output, when depth standard/deep) (`SKILL.md:1244-1305`). Pipeline mode additionally writes `pipeline-manifest.yaml` at `<pipeline_output>/pipeline-manifest.yaml` (`SKILL.md:2714-2715`).

- **Per-proposal verdict file format**: There is no per-proposal verdict file. Per-variant scoring lives in `base-selection.md` with CEV (Claim-Evidence-Verdict) per criterion (`SKILL.md:1677-1689`, `:1769-1806`). The per-diff-point scoring matrix lives in `debate-transcript.md` (`SKILL.md:1452-1485, 1520-1523`).
- **`merge-log.md`**: produced by merge-executor in Step 5; sections (`SKILL.md:2022-2029`): Metadata, Changes Applied (with before/after, provenance tag, validation), Post-Merge Validation, Summary. Template ref: `refs/artifact-templates.md` Section 5 (`SKILL.md:328, 2024`).
- **`refactor-plan.md` emission rules**: produced in Step 4 before merge (`SKILL.md:308, 2012-2021`). Sections: Overview, Planned Changes (per-change: title, source_variant, target_location, integration_approach=replace|append|insert|restructure, rationale, risk_level), Changes NOT Being Made (rejected alternatives with rationale), Risk Summary, Review Status (auto-approved | user-approved). Auto-approved by default; `--interactive` pauses for user (`SKILL.md:303-306, 1847-1851, 1895-1905`).

### Return contract JSON fields (`SKILL.md:424-459`)

| Field | Description | Source line |
|-------|-------------|-------------|
| `merged_output_path` | `string\|null` — path to merged output; null if merge not reached | `SKILL.md:432, 450` |
| `convergence_score` | `float\|null` — 0.0-1.0; null if debate not reached | `SKILL.md:433, 451` |
| `artifacts_dir` | `string` — path to adversarial/ (always set) | `SKILL.md:434, 452` |
| `status` | enum `success` / `partial` / `failed` | `SKILL.md:435, 453` |
| `base_variant` | `string\|null` — model:persona that won; null if not reached | `SKILL.md:436, 454` |
| `unresolved_conflicts` | integer count; 0 on success | `SKILL.md:437, 455` |
| `fallback_mode` | boolean — true if any fallback path used | `SKILL.md:438, 456` |
| `failure_stage` | `null` on success, else `variant_generation` / `debate` / `merge` / `validation` / `transport` | `SKILL.md:439, 457` |
| `invocation_method` | enum `skill-direct` / `task-agent` / `manual` | `SKILL.md:440, 458` |
| `unaddressed_invariants` | list — HIGH-severity UNADDRESSED items from invariant probe; `[]` when none or Round 2.5 skipped; items shape `{id, category, assumption, severity}` | `SKILL.md:441, 459` |

**Write-on-failure mandate**: Contract MUST be written on every invocation including failures, with `status: "failed"`, `failure_stage` set, unreached fields `null` (`SKILL.md:444`).

## Mode A specifics

- **File count limits**: confirmed 2-10 (`SKILL.md:55-65`, parser validation `:554-561`, error messages `:557-560`).
- **Per-proposal scoring**: Hybrid quant+qual combined formula `variant_score = (0.50 × quant_score) + (0.50 × qual_score)` (`SKILL.md:262, 1738`). Edge-case floor: variants scoring <1/5 on Invariant & Edge Case Coverage are ineligible as base (`SKILL.md:250-253, 1671-1675`).
- **Winner semantics**: Highest combined score becomes base variant (`SKILL.md:1740-1741`). Tiebreaker (within 5% margin): Level 1 debate performance, Level 2 correctness criteria count, Level 3 input order (`SKILL.md:264-269, 1743-1759`).
- **Convergence formula**: `convergence = agreed_points / total_diff_points` where `total_diff_points = count(S-NNN) + count(C-NNN) + count(X-NNN) + count(A-NNN)` (`SKILL.md:1336-1340`).
- **Iteration / round caps**: depth controls rounds — quick = Round 1 only; standard = Rounds 1+2+2.5; deep = Rounds 1+2+2.5+3 (`SKILL.md:188-196, 332, 1075-1076, 1105, 1311-1314`). No explicit "max iterations" beyond depth-defined rounds.

## Halt / failure / non-terminal

- **`status = partial` (non-convergence)**: when max rounds reached without meeting threshold — "Force-select by combined score; Document non-convergence; Flag for user review" → `status='partial'` (`SKILL.md:2123-2129`). Also returned when post-merge validation fails (`SKILL.md:2001-2005`) or debate skipped due to substantial similarity.
- **`status = failed`**: pipeline aborted: merge executor failure (`SKILL.md:1938-1942, 2131-2137`); single variant remaining (<2 viable) (`SKILL.md:419-421, 2139-2145`); agent failures dropping below 2 advocates (`SKILL.md:400-403, 1063-1066, 2107-2111`); output-path policy violation refuses BEFORE any write (`SKILL.md:41, 395-398`).
- **Crash / timeout behavior**: Task tool defaults inherit for advocate timeouts (`SKILL.md:1067-1068`). MCP circuit breakers: Sequential 3 failures/30s → fall back to native reasoning with depth reduction (deep→standard→quick) (`SKILL.md:2187-2195, 490`); Serena 4/45s → skip persistence; Context7 5/60s → skip domain validation.

## Refs/ contents

- **artifact-templates.md** (378 lines): Output format specifications for the 6 pipeline artifacts. Section 1 = diff-analysis.md template with ID schemes S-NNN/C-NNN/X-NNN/U-NNN and horizontal-table scaling rule for >2 variants (`refs/artifact-templates.md:7-60`). Sections 2-5 cover debate-transcript.md (round-by-round structure, scoring matrix `:64-100+`), base-selection.md, refactor-plan.md, merge-log.md. Section 6 covers the merged output document template. SKILL.md references this file as the source-of-truth template for each step (`SKILL.md:123, 208, 273, 309, 328`).
- **agent-specs.md** (229 lines): Agent spec format `<model>[:persona[:"instruction"]]` (`refs/agent-specs.md:8-15`). Tables for supported models (opus/sonnet/haiku, `:22-26`) and personas (architect/security/analyzer/frontend/backend/performance/qa/scribe, `:33-42`). Instruction examples and parsing rules at `:46-60+`. Referenced by `SKILL.md:570-585` (mode B agent parsing) and `:950-1014` (advocate instantiation, persona activation map).
- **debate-protocol.md** (258 lines): Detailed 5-step protocol with explicit ordering diagram (`refs/debate-protocol.md:9-15`). Step 1 sub-protocols (structural/content diff, contradiction detection) at `:19-50+`. Provides expanded process descriptions complementing SKILL.md's embedded YAML. Convergence and rounds described per-step.
- **scoring-protocol.md** (230 lines): Complete hybrid algorithm. A.1 Quantitative Layer (`:7-50+`) with 5 metrics table (RC 0.30 / IC 0.25 / SR 0.15 / DC 0.15 / SC 0.15) and explicit formula `quant_score = (RC × 0.30) + (IC × 0.25) + (SR × 0.15) + (DC × 0.15) + (SC × 0.15)`. Subsequent sections cover qualitative 30-criterion rubric, position-bias mitigation (dual-pass forward+reverse), combined scoring (0.5/0.5 weights), and tiebreaker protocol. Referenced authoritatively from `SKILL.md:273`.

## evidence_status:

`partial (missing: prompt-described "5 focus areas, 1-10 scale, max 50/proposal" scoring model not present in skill — actual skill uses 50/50 quant+qual hybrid with 5 quant metrics and 30-criterion qual rubric; per-proposal verdict files not emitted as separate artifacts — per-variant verdicts live inside base-selection.md and debate-transcript.md scoring matrix; refs files read partially (first 50-100 lines each) — sufficient to confirm structure and SKILL.md cross-references)`
