---
type: "📦 Release Scope"
release: "roadmap-cli-skill-converge"
forked_from: "/sc:analyze run 2026-05-15 — Section B"
priority: "primary (Release B; Release A = guide-side doc updates deferred)"
status: "scoping — claims pending verification"
date: "2026-05-15"
---

# Release: Roadmap CLI ↔ Skill / Command Convergence

> **Purpose:** The `/sc:roadmap` and `/sc:validate-roadmap` slash commands plus their backing skills (`sc-roadmap-protocol`, `sc-validate-roadmap-protocol`) describe a flag set, pipeline taxonomy, and validation philosophy that diverge from the shipped `superclaude roadmap` CLI. This release converges the inference layer (skills + slash commands) back to the CLI's deterministic surface — or, where intentional divergence is justified, makes the divergence explicit.
>
> **Out of scope (deferred to Release A):** Release-guide rewrites at `docs/guides/roadmap-cli-tools-release-guide.md`. The guide will be updated separately to document the actually-shipped CLI (TDD/PRD inputs, compression, deviation→remediate→certify cycle, additional gate checks, convergence budget constants).

---

## 1. Source of Claims

All items below originated from the `/sc:analyze` run of 2026-05-15 (Section B "Skill / Command Files Out of Sync With CLI"). Each claim is **pending independent verification** before any file edits are authorized.

Inputs to the analyzer:

- Release guide: `/config/workspace/IronClaude/docs/guides/roadmap-cli-tools-release-guide.md` (1302 lines, v3.05 reference)
- Current CLI: `src/superclaude/cli/roadmap/*.py` (28 files)
- Skills: `src/superclaude/skills/sc-roadmap-protocol/`, `src/superclaude/skills/sc-validate-roadmap-protocol/`
- Slash commands: `src/superclaude/commands/roadmap.md`, `src/superclaude/commands/validate-roadmap.md`
- Synced copies under `.claude/` (repo-local) and `/config/.claude/` (global)

---

## 2. Design Decision Required Up-Front

Before any file edits land, **one design question must be answered** because it determines whether each item below is a large rewrite or a small disclaimer:

- **Option 1 (CLI-mirroring).** Rewrite skills and commands so flags, pipeline taxonomy, and outputs mirror the CLI 1:1. CLI becomes the single source of truth; skills become an inference counterpart that walks the same conceptual pipeline.
- **Option 2 (Parallel inference surface).** Accept that the slash commands and CLI are two distinct tools with different design centers. Keep skill behavior as-is; add explicit headers/disclaimers calling out the divergence; update the release guide to document both surfaces.

Each item in §3 has both an "Option 1 update" and an "Option 2 update" so that the choice can be made once and applied consistently.

---

## 3. Drift Items (Claims Pending Verification)

### B-1 — `src/superclaude/commands/roadmap.md` flag-set drift

**Claim.** The slash command exposes flags that do not exist in the CLI, and is missing flags that do:

- **Command has, CLI does not:** `--specs`, `--template/-t`, `--multi-roadmap`, `--interactive/-i`, `--compliance/-c`, `--persona/-p`
- **CLI has, command does not:** `--no-convergence`, `--input-type {auto,tdd,spec}`, `--tdd-file`, `--prd-file`, `--no-compress`, `--allow-regeneration`, `--resume`, `--max-turns`, `--retrospective`
- **Default output dir mismatch:** command says `.dev/releases/current/<spec-name>/`; CLI defaults to `input_files[0].parent`.

**Verification needed:** read both files end-to-end; produce a one-to-one flag table.

**Option 1 update.** Rewrite the command's usage signature, flag table, and examples block to mirror `superclaude roadmap run` 1:1. Remove `--multi-roadmap` framing (CLI uses `--agents` with a comma list).
**Option 2 update.** Keep command flags as-is; add a "Relationship to CLI" header that links to `superclaude roadmap run --help` for the deterministic counterpart and explicitly enumerates which inference-only flags have no CLI equivalent.

---

### B-2 — `src/superclaude/commands/validate-roadmap.md` frontmatter + flag-set drift

**Claim.**

- **Frontmatter inconsistency:** `name: validate-roadmap` (no `sc:` prefix) — inconsistent with `name: sc:roadmap` in the sibling command file.
- **Command has, CLI does not:** `--specs`, `--exclude/-x`, `--max-agents`, `--skip-adversarial`, `--skip-remediation`, `--report/-r`, `--prior-taxonomy`
- **CLI has, command does not:** `--model`, `--max-turns`, `--debug`
- **Output dir mismatch:** command writes to `{roadmap-dir}/validation/`; CLI writes to `<OUTPUT_DIR>/validate/`.
- **NFR-006 not stated:** the CLI's `validate` subcommand always exits 0; the command file does not document this.

**Verification needed:** confirm frontmatter `name:` value and the exact flag lists in both files.

**Option 1 update.** Fix `name:` to `sc:validate-roadmap`. Rewrite usage + examples to mirror CLI `validate <OUTPUT_DIR>`. Explicitly state: "Adversarial-merge only runs when N≥2 agents; exit code is always 0 (NFR-006)."
**Option 2 update.** Fix `name:` only. Keep deep-validation flag set as inference layer; add a "Relationship to CLI" section noting the CLI provides a different (simpler) flow.

---

### B-3 — `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` pipeline taxonomy mismatch

**Claim.**

- **Taxonomy:** skill uses "Waves 0–4 + Post-Wave completion"; CLI uses 11+ named steps (`extract → generate-A ∥ generate-B → diff → debate → score → merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate → certify`).
- **Thresholds:** skill cites `convergence_score ≥ 0.6 → PASS`, `≥ 0.5 → PARTIAL`, `< 0.5 → FAIL/abort`; validation aggregate `PASS ≥ 85%`, `REVISE 70–84%`, `REJECT < 70%`. CLI gate criteria only validate `convergence_score ∈ [0.0, 1.0]` (validity check, not pass threshold).
- **Missing CLI step references:** no mention of `anti-instinct`, `spec-fidelity`, `wiring-verification`, `deviation-analysis`, `remediate`, or `certify` steps inside the skill.
- **Agent count range:** skill says 2–10 agents; CLI `validate` uses first 2 from `--agents`, generate uses all N.

**Verification needed:** read SKILL.md fully (~34 KB); confirm wave names and threshold values; grep for the six missing step names.

**Option 1 update.** Replace Wave 0–4 with the 11-step CLI taxonomy; reconcile thresholds (use gate criteria from `cli/roadmap/gates.py` as canonical); add explicit sub-sections for each of the six missing steps as inference equivalents.
**Option 2 update.** Add a "Crosswalk: Waves ↔ CLI Steps" table at the top of SKILL.md and a top-of-file disclaimer "This is the inference surface; the deterministic CLI counterpart is `superclaude roadmap run`. Thresholds in this file are inference-only and may differ from CLI gate criteria."

---

### B-4 — `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` stale CLI cross-reference

**Claim.** File claims to match `cli/roadmap/executor.py:detect_input_type()`. Both TDD detection (`tdd score ≥ 5`) and PRD detection (`prd_score ≥ 5`) are documented in the release guide; the skill ref may have drifted or omitted PRD detection.

**Verification needed:** read both `refs/scoring.md` and `cli/roadmap/executor.py:_detect_input_type` / `detect_input_type` end-to-end; produce a side-by-side of the scoring rules and thresholds.

**Option 1 update.** Re-derive scoring tables directly from `executor.py`; explicitly cite the function name and line number.
**Option 2 update.** Add "as of CLI commit `<hash>`" stamp to the cross-reference; flag that PRD detection must be added or removed depending on actual CLI state.

---

### B-5 — `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` 4-tier discovery vs single-template CLI

**Claim.** Skill describes 4-tier template discovery; CLI `templates.py` (71 lines) has `get_template_path(name)` resolving a single template name (`ROADMAP_TEMPLATE = "roadmap_template.compressed.md"`).

**Verification needed:** read `refs/templates.md` and `cli/roadmap/templates.py`; confirm the 4-tier discovery claim and confirm the CLI's single-template behavior.

**Option 1 update.** Replace 4-tier discovery with the actual CLI behavior; remove inference-only fallback tiers.
**Option 2 update.** Add a header: "The 4-tier discovery below is inference-only. The CLI uses a single template resolved by `get_template_path()`."

---

### B-6 — `src/superclaude/skills/sc-roadmap-protocol/refs/validation.md` sub-agent pattern absent from CLI

**Claim.** Skill spawns `quality-engineer` + `self-review` sub-agents in parallel with a REVISE loop (max 2 iterations). The CLI spawns no sub-agents — it runs subprocess `claude -p` calls per step and uses gate criteria for pass/fail decisions.

**Verification needed:** confirm absence of sub-agent spawn patterns in `cli/roadmap/executor.py` and `cli/roadmap/validate_executor.py`. Confirm the REVISE-loop iteration cap in the skill.

**Option 1 update.** Either (a) remove the sub-agent validation pattern entirely and replace with CLI-style gate criteria, or (b) move the sub-agent pattern into a non-canonical "Optional inference enhancement" appendix.
**Option 2 update.** Add disclaimer "Sub-agent validation is an inference-only enhancement; the CLI uses deterministic gate criteria from `cli/roadmap/validate_gates.py`."

---

### B-7 — `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` 8-step extraction vs single CLI prompt

**Claim.** Skill describes an 8-step extraction pipeline; CLI does a single LLM call via `build_extract_prompt` (or `build_extract_prompt_tdd`) producing `extraction.md` in one shot.

**Verification needed:** read `refs/extraction-pipeline.md`; grep `cli/roadmap/prompts.py` and `executor.py` for any multi-step extraction logic.

**Option 1 update.** Collapse to a single-pass extraction reference mirroring the CLI prompt builder; preserve the per-step rationale as commentary inside the single prompt's design notes.
**Option 2 update.** Mark the 8-step decomposition as an inference-only thinking framework; add a closing note that the CLI consolidates this into a single prompt.

---

### B-8 — `src/superclaude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` `sc:adversarial-protocol` delegation

**Claim.** Skill delegates to `sc:adversarial-protocol` via SKILL-DIRECT invocation (D-0001 reversal); CLI's debate phase is a single LLM call (no protocol delegation).

**Verification needed:** read `refs/adversarial-integration.md`; confirm CLI debate is single-shot in `executor.py` and `prompts.py:build_debate_prompt`.

**Option 1 update.** Remove `sc:adversarial-protocol` delegation; replace with the CLI's `build_debate_prompt` flow and depth-controlled rounds (`_DEPTH_INSTRUCTIONS`).
**Option 2 update.** Mark `sc:adversarial-protocol` delegation as inference-only; document the simpler CLI debate alongside it.

---

### B-9 — `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` entirely different pipeline from CLI

**Claim.** Skill implements a 7-phase pipeline (Pre-Phase 0 + Phases 0–6 + Post-Phase 6) with 4 mandatory cross-cutting agents (CC1–CC4), Auggie + Serena enrichment, and a verdict matrix (GO / CONDITIONAL_GO / NO_GO). The CLI `validate` subcommand runs a simple `reflect → (adversarial-merge if N≥2) → validation-report.md` flow against 7 validation dimensions.

**Verification needed:** read SKILL.md (~56 KB) fully; confirm phase count, sub-agent names, verdict matrix; compare against `cli/roadmap/validate_executor.py` and `validate_gates.py`.

**Option 1 update.** Major rewrite to mirror the CLI's reflect + adversarial-merge flow with the 7 dimensions (Schema, Structure, Traceability, Cross-file consistency, Parseability, Interleave, Decomposition). Preserve any reusable Auggie/Serena enrichment hooks as optional steps.
**Option 2 update.** Add a top-of-file disclaimer: "This is an inference-only deep-validation protocol. The CLI counterpart at `superclaude roadmap validate` runs a simpler reflect + adversarial-merge flow against 7 fixed dimensions. Use this skill for thorough investigative validation; use the CLI for automated CI/CD gating."

---

### B-10 — `sc-validate-roadmap-protocol` packaging shape

**Claim.** Skill ships as a single 56 KB `SKILL.md` with no `refs/`, `rules/`, or `templates/` subdirectories.

**Verification needed:** list directory contents.

**Option 1 update.** Factor SKILL.md into `refs/` (extraction, decomposition, adversarial, remediation) to match the structure of `sc-roadmap-protocol`. Non-blocking.
**Option 2 update.** Leave as-is. Single-file packaging is functional.

---

### B-11 — `.claude/skills/sc-roadmap-protocol/`, `.claude/skills/sc-validate-roadmap-protocol/` global-install gap

**Claim.** Repo-local `.claude/skills/` is byte-identical to `src/superclaude/skills/` (sync OK). The global location `/config/.claude/skills/` does **not** contain either skill. Result: skills are only visible to Claude when run from inside `/config/workspace/IronClaude/`.

**Verification needed:** `ls /config/.claude/skills/` and confirm absence; verify repo-local sync via md5.

**Option 1 update.** Add a global-install step to `make sync-dev` or `superclaude install` so the skills land at `/config/.claude/skills/` for cross-project visibility.
**Option 2 update.** Document the repo-local-only design decision; leave install behavior unchanged.

---

### B-12 — Synced copies will need refresh after src updates

**Claim.** Three locations carry identical copies of `roadmap.md` and `validate-roadmap.md`:

- `src/superclaude/commands/`
- `.claude/commands/sc/` (repo-local)
- `/config/.claude/commands/sc/` (global)

After items B-1 and B-2 land in `src/`, both `.claude/` copies need a re-sync.

**Verification needed:** md5 the three sets of files to confirm identity.

**Option 1 update.** Run `make sync-dev` (re-syncs `.claude/`) and a separate manual copy to `/config/.claude/` after merging B-1, B-2.
**Option 2 update.** Same — sync behavior is mechanical regardless of design choice.

---

## 4. Acceptance Criteria for the Release

The release ships when:

1. Design decision (Option 1 vs Option 2) is recorded in this directory as `design-decision.md`.
2. Each item B-1 through B-12 has either a verified change committed to `src/` (and synced to `.claude/`) OR a documented decision to defer/skip.
3. `make verify-sync` passes (src ↔ `.claude/` parity).
4. A regression check confirms that `/sc:roadmap` and `/sc:validate-roadmap` slash-commands still execute end-to-end against a sample spec.
5. (Option 1 only) A flag table in `src/superclaude/commands/roadmap.md` mirrors `superclaude roadmap run --help` output exactly; same for `validate-roadmap.md`.
6. (Option 2 only) Each skill / command file has an explicit "Relationship to CLI" header.

---

## 5. Open Questions

- **OQ-1.** Should `/sc:roadmap --multi-roadmap` be deprecated in favor of CLI-style `--agents opus,haiku,sonnet`, or retained as an inference-layer concept that compiles down to a multi-agent CLI invocation?
- **OQ-2.** The skill validation thresholds (PASS ≥ 85%, REVISE 70–84%, REJECT < 70%) appear nowhere in the CLI gate criteria. Are these orphan thresholds or are they enforced somewhere I missed?
- **OQ-3.** Should `sc-validate-roadmap-protocol` keep its 4 mandatory cross-cutting agents (CC1–CC4) as an inference enrichment over the CLI's 7-dimension reflect, or be collapsed?
- **OQ-4.** Is global install at `/config/.claude/skills/` intended or are the skills meant to be repo-local only?

---

## 6. Out of Scope (Release A — Deferred)

These items live in the original `/sc:analyze` Section A and are explicitly NOT addressed by this release:

- Release-guide rewrites at `docs/guides/roadmap-cli-tools-release-guide.md` (§1 missing flags, §2 missing steps, §3 missing artifacts, §4 missing prompts, §5 enriched gate checks, §5 new convergence budget section, §9 cross-references, §10 version bump)
- CLI Python code changes (none needed for this convergence; CLI is the canonical surface)

---

## 7. Status Log

| Date | Event |
|---|---|
| 2026-05-15 | Release scoped from /sc:analyze run; claims pending verification |
