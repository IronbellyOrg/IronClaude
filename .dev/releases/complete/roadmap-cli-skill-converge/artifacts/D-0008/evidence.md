# D-0008 — Evidence: `sc-roadmap-protocol/refs/adversarial-integration.md` Replace `sc:adversarial-protocol` Delegation with CLI Debate Prompt Flow

| Field | Value |
|---|---|
| Task | T02.07 |
| Roadmap Item | R-008 |
| Drift Item | B-8 |
| Deliverable | D-0008 |
| Date | 2026-05-26 |
| Source Files Edited | `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`; `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` |
| CLI Reference | `build_debate_prompt` (`src/superclaude/cli/roadmap/prompts.py:878-902`); `_DEPTH_INSTRUCTIONS` dict (`src/superclaude/cli/roadmap/prompts.py:18-37`); single-step wiring (`src/superclaude/cli/roadmap/executor.py:2076-2084`); gate (`DEBATE_GATE` at `src/superclaude/cli/roadmap/gates.py:1155-1166`); chain context (`diff` / `score` / `merge` at `executor.py:2066-2126`); 14-step pipeline registry (`_get_all_step_ids` at `executor.py:2281-2300`); debate output file (`executor.py:1962`). |
| Decision Posture | Option 1 (replace `sc:adversarial-protocol` delegation with CLI debate prompt flow; mention richer `sc:adversarial` usage only as inference-only) — see `design-decision.md` row B-8. |
| Source Claim Status | VERIFIED (`verification.md:151-161`) — skill ref delegated to `sc:adversarial-protocol` via `Skill sc:adversarial-protocol args: "..."` at multiple call sites (`refs/adversarial-integration.md:83, 102, 112, 126, 135, 137` pre-edit); CLI executes adversarial-merge as a single inline `Step(id="debate", prompt=build_debate_prompt(...), gate=DEBATE_GATE)` with depth control encoded by `_DEPTH_INSTRUCTIONS`. No `Skill sc:adversarial-protocol` invocation, no return-contract YAML on disk, no sub-skill forwarding in the CLI. |

## Linkage

- **B-8 → D-0008.** `release-scope.md` and `verification.md:151-161` capture the claim: pre-edit, `refs/adversarial-integration.md` repeatedly instructed the operator to issue `Skill sc:adversarial-protocol args: "..."` with `--compare`, `--source --generate roadmap`, and `--interactive` forwarding (`refs/adversarial-integration.md:83, 102, 112, 126, 135, 137` pre-edit). The skill's own `SKILL.md:417-424` (pre-edit) declared "sc:roadmap-protocol delegates to sc:adversarial-protocol via direct Skill invocation (SKILL-DIRECT per D-0001 reversal)". CLI evidence: `cli/roadmap/prompts.py:878-902` defines `build_debate_prompt` as a single-shot debate prompt builder opening with `"You are a structured debate facilitator..."` and interpolating one `_DEPTH_INSTRUCTIONS` entry (`prompts.py:18-37`) into the embedded `Debate format:` slot. `cli/roadmap/executor.py:2076-2084` constructs **one** `Step(id="debate", ...)` wired between `diff` (`:2066-2074`) and `score` (`:2086-2103`) with `gate=DEBATE_GATE`. `DEBATE_GATE` (`gates.py:1155-1166`) requires the LLM output to declare `convergence_score` and `rounds_completed` in frontmatter, enforces `min_lines=50`, and runs the `convergence_score_valid` semantic check (float in `[0.0, 1.0]`). There is no `Skill sc:adversarial-protocol` invocation in the CLI, no `return-contract.yaml` emitted by the debate step, and no protocol forwarding.
- `design-decision.md:38` row B-8 selected **Option 1**: "Replace direct protocol delegation with the CLI debate prompt flow; mention richer `sc:adversarial` usage only as out-of-band/inference-only if needed." `solutions.md:293` recommends removing `sc:adversarial-protocol` delegation to match the CLI's single debate step.
- **D-0008** is the resulting source-file edit at `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` plus the related SKILL.md updates (D-0001 reversal wording aligned with B-8, `_DEPTH_INSTRUCTIONS` named at Section 5 Depth Mapping and at the Agent Delegation table) and this evidence record.

## Source-file parity check

### CLI canonical debate builder cited in the edit

`src/superclaude/cli/roadmap/prompts.py:878-902`:

```
def build_debate_prompt(
    diff_path: Path,
    variant_a_path: Path,
    variant_b_path: Path,
    depth: Literal["quick", "standard", "deep"],
) -> str:
    """Prompt for step 'debate'.

    Depth controls the number of debate rounds embedded in the prompt.
    """
    depth_instruction = _DEPTH_INSTRUCTIONS[depth]
    return (
        "You are a structured debate facilitator.\n\n"
        "Read the provided diff analysis and both roadmap variants. "
        "Facilitate a structured adversarial debate between the two approaches.\n\n"
        f"Debate format:\n{depth_instruction}\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- convergence_score: (float 0.0-1.0 indicating how much agreement was reached)\n"
        "- rounds_completed: (integer number of debate rounds conducted)\n\n"
        ...
    ) + _OUTPUT_FORMAT_BLOCK
```

The builder accepts the path to `diff-analysis.md` plus both variant roadmaps and a `depth` literal, returns one prompt string, and never calls into `Skill sc:adversarial-protocol`. The convergence-score is produced as YAML frontmatter on the resulting `debate-transcript.md`, not as a structured Skill-return contract.

### CLI canonical depth control cited in the edit

`src/superclaude/cli/roadmap/prompts.py:18-37`:

```
_DEPTH_INSTRUCTIONS = {
    "quick": (
        "Conduct a single focused debate round. ..."
    ),
    "standard": (
        "Conduct two debate rounds:\n"
        "  Round 1: Each perspective states initial positions on divergence points.\n"
        "  Round 2: Each perspective rebuts the other's key claims.\n"
        "Then provide a convergence assessment."
    ),
    "deep": (
        "Conduct three debate rounds:\n"
        "  Round 1: Each perspective states initial positions on divergence points.\n"
        "  Round 2: Each perspective rebuts the other's key claims.\n"
        "  Round 3: Final synthesis -- each perspective identifies concessions and "
        "remaining disagreements.\n"
        "Then provide a convergence assessment."
    ),
}
```

The `--depth` flag selects one entry; the round count is encoded entirely inside the prompt text. The CLI does not iterate Python-side rounds — all rounds happen inside a single `claude -p "<prompt>"` invocation.

### CLI single-step wiring cited in the edit

`cli/roadmap/executor.py:2076-2084` builds the single `Step(id="debate", ...)`:

```
Step(
    id="debate",
    prompt=build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth),
    output_file=debate_file,
    gate=DEBATE_GATE,
    timeout_seconds=600,
    inputs=[diff_file] + _llm_inputs_for(config, roadmap_a, roadmap_b),
    retry_limit=1,
),
```

`debate_file` is `<output_dir>/debate-transcript.md` (`executor.py:1962`). The step's `retry_limit=1` is the standard transport-level retry budget — not a per-round retry, not a "rerun adversarial protocol" budget.

### CLI canonical gate cited in the edit

`cli/roadmap/gates.py:1155-1166`:

```
DEBATE_GATE = GateCriteria(
    required_frontmatter_fields=["convergence_score", "rounds_completed"],
    min_lines=50,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="convergence_score_valid",
            check_fn=_convergence_score_valid,
            failure_message="convergence_score must be a float in [0.0, 1.0]",
        ),
    ],
)
```

The gate validates that the LLM-emitted `debate-transcript.md` declares both frontmatter fields, is at least 50 lines, and that `convergence_score` parses as a float in `[0.0, 1.0]`. There is no PASS / PARTIAL / FAIL threshold routing inside the gate — those thresholds live only in the inference-layer skill prose.

### CLI surrounding chain cited in the edit

`cli/roadmap/executor.py:2066-2126` constructs the surrounding chain in pipeline order:

| Step | Builder | Output | Gate |
|---|---|---|---|
| `diff` | `build_diff_prompt(roadmap_a, roadmap_b)` | `diff-analysis.md` | `DIFF_GATE` |
| `debate` | `build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth)` | `debate-transcript.md` | `DEBATE_GATE` |
| `score` | `build_score_prompt(debate_file, roadmap_a, roadmap_b, tdd_file, prd_file)` | `base-selection.md` | `SCORE_GATE` |
| `merge` | `build_merge_prompt(score_file, roadmap_a, roadmap_b, debate_file, tdd_file, prd_file)` | `roadmap.md` | `MERGE_GATE` |

All four are sequential entries in the flat 14-step pipeline returned by `_get_all_step_ids` at `executor.py:2281-2300`. None of them invokes `Skill sc:adversarial-protocol`.

### Post-edit `refs/adversarial-integration.md` structure (in file order)

| Section | Anchor | Status |
|---|---|---|
| Header lead paragraph | `adversarial-integration.md:3` | ✅ Reframed — now states the canonical surface is the inline CLI debate flow built by `build_debate_prompt` with depth via `_DEPTH_INSTRUCTIONS`; everything else is named as inference-only Skill-delegation material |
| `## CLI Canonical Debate Prompt Flow (B-8, VERIFIED)` | `adversarial-integration.md:9-82` | ✅ New canonical section — opens with "CLI parity" callout citing `prompts.py:878-902`, `:18-37`, `executor.py:2076-2084`, `gates.py:1155-1166`; subsections: CLI prompt builder (with signature), Depth control via `_DEPTH_INSTRUCTIONS` (with per-depth table), Single-step pipeline wiring (quoted from `executor.py`), `DEBATE_GATE` properties (frontmatter fields, min_lines, tier, semantic check), Surrounding chain table (`diff` / `debate` / `score` / `merge`), and "What this means for skill behavior" enumerating the four points where the existing skill prose is inference-only |
| `## Inference-Only Skill-Delegation Mode` | `adversarial-integration.md:86-88` | ✅ New scope header — explicitly marks the SKILL-DIRECT delegation model as inference-only, references the D-0001 reversal as the availability claim (not the canonical-CLI claim), and states the canonical-CLI flow above wins on overlap |
| Mode Detection | `adversarial-integration.md:90-109` | ✅ Preserved verbatim — now sits under the inference-only header. The `Skill sc:adversarial-protocol args: "..."` invocation pattern is retained as inference-only guidance, not canonical CLI behavior |
| Agent Specification Parsing | `adversarial-integration.md:113-156` | ✅ Preserved verbatim — sits under the inference-only header |
| Invocation Patterns | `adversarial-integration.md:160-222` | ✅ Preserved verbatim — the `Skill sc:adversarial-protocol args: "..."` invocation patterns for multi-spec and multi-roadmap remain documented as inference-only |
| `--resume-from` Interaction | `adversarial-integration.md:226-268` | ✅ Preserved verbatim — `return-contract.yaml` consumption sits under the inference-only header |
| Post-Adversarial Artifact Existence Gate (Tier 1) | `adversarial-integration.md:272-289` | ✅ Preserved verbatim — these artifact-existence checks describe inference-mode contract validation, not CLI gate behavior |
| Return Contract Consumption | `adversarial-integration.md:293-395` | ✅ Preserved verbatim — the 9-field return-contract schema and status routing remain as inference-only guidance; the canonical-CLI flow does not emit this contract |
| Divergent-Specs Heuristic | `adversarial-integration.md:399-413` | ✅ Preserved verbatim |
| Frontmatter Population | `adversarial-integration.md:417-437` | ✅ Preserved verbatim |
| Error Handling | `adversarial-integration.md:441-483` | ✅ Preserved verbatim — the "sc:adversarial skill not installed" abort is now an inference-mode error, not a canonical-CLI error |
| `--interactive` Flag Propagation | `adversarial-integration.md:487-503` | ✅ Preserved verbatim |
| Footer | `adversarial-integration.md:502-506` | ✅ Updated — records the CLI parity baseline (B-8, VERIFIED) with source citations for `build_debate_prompt`, `_DEPTH_INSTRUCTIONS`, the executor wiring, and `DEBATE_GATE`; restates that the demoted Skill-delegation sections are inference-only (SKILL-DIRECT per D-0001 reversal) and not implemented by the canonical CLI |

(Line numbers are approximate to the post-edit file; anchors fix the sections by heading. The original numbered call sites for `Skill sc:adversarial-protocol args:` in `verification.md:151-161` (`:83, 102, 112, 126, 135, 137`) all now sit under the "Inference-Only Skill-Delegation Mode" scope header.)

### Post-edit `SKILL.md` adjustments

| Section | Anchor | Status |
|---|---|---|
| Section 5 Depth Mapping | `SKILL.md:358-362` | ✅ Reframed — keeps the existing `--depth quick→1 / standard→2 / deep→3` line and adds a new "**CLI canonical mechanism (B-8, VERIFIED).**" paragraph naming `_DEPTH_INSTRUCTIONS` at `prompts.py:18-37`, `build_debate_prompt` at `prompts.py:878-902`, and `DEBATE_GATE` at `gates.py:1155-1166`. Explicitly states the CLI does not invoke `Skill sc:adversarial-protocol` and that the PASS/PARTIAL/FAIL routing on `convergence_score` is inference-only. |
| Section "Agent Delegation" | `SKILL.md:490-502` | ✅ Reframed — opens with a "**CLI parity (B-8, VERIFIED).**" callout that aligns the D-0001 reversal wording with the B-8 decision: the reversal made SKILL-DIRECT available, **but it did not make SKILL-DIRECT the canonical CLI debate mechanism**. Adds a third row to the delegation table for the CLI-canonical mode (inline `Step(id="debate", ...)` chain `diff → debate → score → merge`). Renames the SKILL-DIRECT call-out to "**SKILL-DIRECT (inference-only)**" and adds the explicit "The canonical CLI does not exercise this path" sentence. |
| Section 4 Execution Vocabulary (Invoke Skill row) | `SKILL.md:94` | ⏸ Left intact — the vocabulary entry already qualifies cross-skill invocation as "valid from both command and skill context per D-0001 reversal" and is not the canonical-CLI claim; the alignment work happens in the dedicated Agent Delegation section per B-8 Option 1's scope. |
| Section 4 Wave 2 / CLI Step Crosswalk row | `SKILL.md:135` | ⏸ Left intact — already names `build_debate_prompt` and `_DEPTH_INSTRUCTIONS` and explicitly states "The CLI does NOT delegate to a separate `sc:adversarial-protocol` skill (see B-8)". This row was the B-3 / T02.01 deliverable and remains consistent with B-8. |
| Section 8 Will Do — "Invoke `Skill sc:adversarial-protocol` for multi-spec consolidation and multi-roadmap generation" | `SKILL.md:435` | ⏸ Left intact — the Will Do list describes inference-mode capabilities. The new CLI-parity wording is concentrated in the Agent Delegation and Depth Mapping sections per the B-8 task scope; the Will Do list does not duplicate the CLI parity claim. |

## Acceptance criteria check (`phase-2-tasklist.md:372-377`)

- ✅ `refs/adversarial-integration.md` describes the CLI debate prompt flow — see "## CLI Canonical Debate Prompt Flow (B-8, VERIFIED)" (`adversarial-integration.md:9-82`). The section quotes the `build_debate_prompt(diff_path, variant_a_path, variant_b_path, depth)` signature, the `_DEPTH_INSTRUCTIONS` dict structure, the `Step(id="debate", ...)` wiring, the `DEBATE_GATE` properties, and the surrounding `diff → debate → score → merge` chain. The "What this means for skill behavior" subsection explicitly states the four points where the prior `Skill sc:adversarial-protocol` delegation prose is now inference-only.
- ✅ `refs/adversarial-integration.md` removes direct `sc:adversarial-protocol` delegation from canonical roadmap protocol behavior and names `build_debate_prompt` — the new canonical section explicitly states "The roadmap CLI does **not** delegate to a separate `sc:adversarial-protocol` skill" (`adversarial-integration.md:11`), and the "Inference-Only Skill-Delegation Mode" header at `:86` re-scopes the retained `Skill sc:adversarial-protocol args: "..."` invocation patterns as out-of-canonical-CLI guidance. `build_debate_prompt` is named in the canonical section's prompt-builder table (`:15-17`), the depth-control subsection (`:23`), the single-step wiring quote (`:38-46`), the surrounding-chain table (`:71`), and the footer CLI parity baseline (`:507-509`).
- ✅ `SKILL.md` represents related D-0001 reversal wording consistently and names `_DEPTH_INSTRUCTIONS` where the source requires it — see Section 5 Depth Mapping (`SKILL.md:360-362`) which adds the "**CLI canonical mechanism (B-8, VERIFIED).**" paragraph naming `_DEPTH_INSTRUCTIONS` at `prompts.py:18-37` and `build_debate_prompt` at `prompts.py:878-902`. The Agent Delegation section (`SKILL.md:490-502`) realigns the D-0001 reversal claim: the reversal established SKILL-DIRECT *availability* but did not make it the *canonical CLI mechanism*; the canonical CLI mechanism is the inline `Step(id="debate", ...)` chain. The Wave 2 / CLI Step Crosswalk row at `SKILL.md:135` already names both `build_debate_prompt` and `_DEPTH_INSTRUCTIONS` (delivered under B-3 / T02.01) and remains consistent with B-8.
- ✅ Evidence at this path links B-8 → D-0008 and records the source's VERIFIED status — see the "Source Claim Status" row of the header table (records VERIFIED + `verification.md:151-161` anchor), the "Linkage" section above (B-8 to D-0008 chain with `verification.md:151-161` + `design-decision.md:38` + `solutions.md:293` citations), and the footer CLI parity baseline that re-anchors B-8 in `refs/adversarial-integration.md` itself.

## Reframed vs. preserved skill content

- **Preserved verbatim** (text identical, semantics demoted to inference-only Skill-delegation mode):
  - Mode Detection — three modes (multi-spec / multi-roadmap / combined), detection logic, implicit `--multi-roadmap` inference, "sc:adversarial skill not installed" prerequisite check.
  - Agent Specification Parsing — `model[:persona[:"instruction"]]` format, parsing algorithm, format examples, validation rules, orchestrator addition at `agent_count ≥ 3`.
  - Invocation Patterns — `Skill sc:adversarial-protocol args: "--compare ..."` for multi-spec, `Skill sc:adversarial-protocol args: "--source ... --generate roadmap --agents ..."` for multi-roadmap, combined-mode chaining.
  - `--resume-from` Interaction — flag validation rules, file-fallback consumption path, session persistence behavior, incompatibility table.
  - Post-Adversarial Artifact Existence Gate (Tier 1) — four-check fail-fast order on `<artifacts_dir>/`, `diff-analysis.md`, `merged-output.md`, `return-contract.yaml`.
  - Return Contract Consumption — 9-field schema, status routing (`success` / `partial` / `failed`), convergence-score threshold routing (`≥ 0.6` / `≥ 0.5` / `< 0.5`), fallback-mode warning, unresolved-conflicts handling, example contracts.
  - Divergent-Specs Heuristic — `convergence_score < 50%` warning.
  - Frontmatter Population — `adversarial:` block schema and population rules.
  - Error Handling — adversarial skill not installed, unknown model identifier, agent count out of range, sc:adversarial invocation failure.
  - `--interactive` Flag Propagation — propagation rules and behavioral impact.
- **Removed from canonical scope** (folded under the "Inference-Only Skill-Delegation Mode" header):
  - The framing of `Skill sc:adversarial-protocol` invocation as the canonical adversarial pathway for sc:roadmap. The post-edit canonical section explicitly states the CLI uses one inline `Step(id="debate", ...)` and does not invoke a separate sub-skill.
  - The framing of `return-contract.yaml` as the canonical adversarial result transport. The CLI emits per-step output files gated by `GateCriteria`; the unified return-contract YAML is inference-only.
  - The framing of `convergence_score` threshold routing (`≥ 0.6 PASS`, `≥ 0.5 PARTIAL`, `< 0.5 FAIL`) as a canonical CLI gate behavior. The canonical `DEBATE_GATE` only validates that the score parses as a float in `[0.0, 1.0]`; pass/fail routing on the score is an inference-layer decision.
  - The framing of D-0001 reversal as "SKILL-DIRECT is the canonical CLI debate mechanism". The reversal established that SKILL-DIRECT is *available*; the canonical CLI mechanism remains the inline `build_debate_prompt` step.
- **Added** (new canonical content for B-8):
  - "CLI Canonical Debate Prompt Flow (B-8, VERIFIED)" section with the prompt-builder signature, depth-control dict with per-depth round counts, single-step pipeline wiring quote, `DEBATE_GATE` property table, surrounding-chain table (`diff` / `debate` / `score` / `merge`), and a four-point "What this means for skill behavior" callout enumerating the inference-only nature of the demoted material.
  - "Inference-Only Skill-Delegation Mode" scope header with explicit "not implemented by the canonical CLI debate flow" / "canonical flow wins on overlap" callouts.
  - Footer CLI parity baseline (B-8, VERIFIED) note with citations for `build_debate_prompt` (`prompts.py:878-902`), `_DEPTH_INSTRUCTIONS` (`prompts.py:18-37`), the executor wiring (`executor.py:2076-2084`), and `DEBATE_GATE` (`gates.py:1155-1166`).
  - SKILL.md Section 5 Depth Mapping: new "**CLI canonical mechanism (B-8, VERIFIED).**" paragraph naming `_DEPTH_INSTRUCTIONS`, `build_debate_prompt`, and `DEBATE_GATE`, and stating that PASS/PARTIAL/FAIL routing on `convergence_score` is inference-only.
  - SKILL.md Agent Delegation: new "**CLI parity (B-8, VERIFIED).**" callout aligning the D-0001 reversal wording (availability ≠ canonical-CLI mechanism), expanded delegation table with the CLI-canonical inline-chain row, and the renamed "**SKILL-DIRECT (inference-only)**" sub-section with explicit "The canonical CLI does not exercise this path" statement.

## Cross-edit linkage

- `SKILL.md:135` (delivered under B-3 / T02.01) already names `build_debate_prompt` and `_DEPTH_INSTRUCTIONS` in the Wave 2 / CLI Step Crosswalk row and explicitly states "The CLI does NOT delegate to a separate `sc:adversarial-protocol` skill (see B-8)". The B-8 cross-reference now resolves directly to the post-edit `refs/adversarial-integration.md` canonical section.
- `SKILL.md:137` (delivered under B-3 / T02.01) marks the Wave 4 `quality-engineer` / `self-review` dispatch as inference-only and non-canonical for CLI parity. The B-8 update reuses the same "inference-only / canonical-CLI-wins" framing for the Wave 1A/2 Skill-delegation prose, keeping the SKILL.md treatment of inference-mode behavior consistent across waves.
- `refs/validation.md` (B-6 / T02.04) already names `REFLECT_GATE` and `ADVERSARIAL_MERGE_GATE` as the canonical CLI gates and demotes sub-agent dispatch / REVISE-loop language as non-canonical. The B-8 update applies the same demotion treatment to the Skill-delegation prose in `refs/adversarial-integration.md`, ensuring the two refs use a consistent "canonical CLI + inference-only Skill-mode" structure.
- `refs/extraction-pipeline.md` (B-7 / T02.05) established the precedent of preserving the verbose pre-edit content as a demoted inference-only section under a new canonical-CLI lead. B-8 applies the same pattern to `refs/adversarial-integration.md`.

## Sync follow-up (B-12)

This edit lives only at `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` and `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`. A subsequent `make sync-dev` is required (tracked under B-12 / Phase 5) before `.claude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`, `.claude/skills/sc-roadmap-protocol/SKILL.md`, `/config/.claude/skills/sc-roadmap-protocol/refs/adversarial-integration.md`, and `/config/.claude/skills/sc-roadmap-protocol/SKILL.md` reflect the change. Per repo rules, `.claude/` mirrors are not staged or committed.

## CLI behavior anchors cited in the edit

- `cli/roadmap/prompts.py:18-37` — `_DEPTH_INSTRUCTIONS` dict (per-depth debate-round instructions for `quick` / `standard` / `deep`).
- `cli/roadmap/prompts.py:878-902` — `def build_debate_prompt(diff_path, variant_a_path, variant_b_path, depth) -> str` — single-shot debate prompt builder; interpolates `_DEPTH_INSTRUCTIONS[depth]` into the embedded `Debate format:` slot; declares the required output-frontmatter fields `convergence_score` and `rounds_completed`.
- `cli/roadmap/executor.py:1962` — `debate_file = out / "debate-transcript.md"` — canonical debate output path.
- `cli/roadmap/executor.py:2066-2074` — `Step(id="diff", prompt=build_diff_prompt(...), gate=DIFF_GATE)` — prior step in the canonical chain.
- `cli/roadmap/executor.py:2076-2084` — `Step(id="debate", prompt=build_debate_prompt(...), gate=DEBATE_GATE, timeout_seconds=600, retry_limit=1)` — canonical inline debate step.
- `cli/roadmap/executor.py:2086-2103` — `Step(id="score", ...)` — next step in the canonical chain.
- `cli/roadmap/executor.py:2104-2126` — `Step(id="merge", ...)` — terminal step of the canonical adversarial-merge chain.
- `cli/roadmap/executor.py:2281-2300` — `_get_all_step_ids` — flat 14-step pipeline registry confirming `debate` is one entry among 14, not a delegated sub-skill invocation.
- `cli/roadmap/gates.py:1155-1166` — `DEBATE_GATE` — `required_frontmatter_fields=["convergence_score", "rounds_completed"]`, `min_lines=50`, `enforcement_tier="STRICT"`, semantic check `convergence_score_valid` (float in `[0.0, 1.0]`).

## Delegation → inline collapse record

Per `phase-2-tasklist.md:374-377` the evidence must record that direct `sc:adversarial-protocol` delegation is removed from canonical roadmap protocol behavior, `build_debate_prompt` is named in the ref, the related SKILL.md D-0001 reversal wording is consistent, and `_DEPTH_INSTRUCTIONS` is named where required. Summary:

- **Behavior moved from "Skill delegation" to "inline LLM step".** Pre-edit `refs/adversarial-integration.md:83, 102, 112, 126, 135, 137` repeatedly instructed `Skill sc:adversarial-protocol args: "..."`. Post-edit, those invocations remain in the file under the "Inference-Only Skill-Delegation Mode" header (`:86-88`), but the canonical section at `:9-82` describes the CLI's inline `Step(id="debate", ...)` flow and explicitly states `"The roadmap CLI does not delegate to a separate sc:adversarial-protocol skill."`
- **Why moved.** CLI grep confirms one `def build_debate_prompt(...)` (`prompts.py:878-902`), one `_DEPTH_INSTRUCTIONS` dict (`prompts.py:18-37`), and one `Step(id="debate", ...)` (`executor.py:2076-2084`). There is no `Skill sc:adversarial-protocol` invocation anywhere in `cli/roadmap/`; grep for `sc:adversarial` returns no matches inside the executor / prompts / gates modules.
- **What the CLI does instead.** Reads the previous `diff-analysis.md` and both variant roadmaps, builds one `build_debate_prompt(diff_path, variant_a_path, variant_b_path, depth)` prompt with the depth-specific round count from `_DEPTH_INSTRUCTIONS[depth]` interpolated inline, fires one LLM call into `debate-transcript.md`, and validates that file with `DEBATE_GATE` (frontmatter `convergence_score` + `rounds_completed`, `min_lines=50`, STRICT, semantic check `convergence_score_valid`). The score then flows to the next inline step (`score` → `merge`). There is no protocol forwarding, no return-contract YAML on disk, and no inference-layer PASS/PARTIAL/FAIL routing at the debate gate itself.
- **D-0001 reversal alignment.** The D-0001 reversal made SKILL-DIRECT (Skill-to-skill invocation without a Task wrapper) available, which the post-edit SKILL.md Agent Delegation section continues to record. B-8 establishes that the *canonical CLI mechanism* is not SKILL-DIRECT — it is the inline debate step. Both statements coexist in the post-edit SKILL.md: SKILL-DIRECT is available (for skill-mode operation); the canonical CLI uses the inline step. The new "**CLI parity (B-8, VERIFIED).**" callout at the top of Agent Delegation makes the distinction explicit.
- **Reintroduction path.** If a future CLI release adds protocol forwarding (i.e., wires `superclaude roadmap run` to invoke `sc:adversarial-protocol` directly rather than running `build_debate_prompt` inline), the "Inference-Only Skill-Delegation Mode" section can be promoted back to canonical and the inline-debate section demoted or deprecated. The B-8 row in `release-scope.md` is the tracking point.
