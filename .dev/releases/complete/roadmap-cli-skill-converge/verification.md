---
type: "🔍 Claim Verification"
release: "roadmap-cli-skill-converge"
date: "2026-05-15"
verifier: "independent sc:analyze pass"
claims_verified: 12
verified_count: 9
partial_count: 2
refuted_count: 1
---

# Independent Verification of B-1 → B-12 Drift Claims

Each claim re-tested by reading the source files directly. Sync state verified by md5sum and ls. Evidence is short verbatim quotes with `file:line` anchors.

---

## Summary Table

| ID | Claim (short) | Status |
|---|---|---|
| B-1 | roadmap.md ↔ CLI flag-set drift | VERIFIED |
| B-2 | validate-roadmap.md frontmatter + flag-set drift | PARTIAL |
| B-3 | sc-roadmap-protocol pipeline taxonomy mismatch | VERIFIED |
| B-4 | scoring.md stale CLI cross-reference | PARTIAL |
| B-5 | templates.md 4-tier vs single-template CLI | VERIFIED |
| B-6 | validation.md sub-agent pattern absent from CLI | VERIFIED |
| B-7 | extraction-pipeline.md 8-step vs single CLI prompt | VERIFIED |
| B-8 | adversarial-integration.md sc:adversarial delegation | VERIFIED |
| B-9 | sc-validate-roadmap-protocol entirely different pipeline | VERIFIED |
| B-10 | sc-validate-roadmap-protocol packaging shape | VERIFIED |
| B-11 | Global-install gap for both skills | REFUTED |
| B-12 | Synced copies need refresh after src updates | VERIFIED |

---

### B-1 — `commands/roadmap.md` flag-set drift

**Status:** VERIFIED

**Evidence:**
- `src/superclaude/commands/roadmap.md:22-37` — flag table lists `--specs`, `--template`, `--multi-roadmap`, `--interactive`, `--validate/--no-validate`, `--compliance`, `--persona`, `--dry-run` (no CLI-equivalent flags).
- `src/superclaude/cli/roadmap/commands.py:34-149` — CLI `run` defines `--agents`, `--output`, `--depth`, `--resume`, `--dry-run`, `--model`, `--max-turns`, `--debug`, `--no-validate`, `--allow-regeneration`, `--no-convergence`, `--retrospective`, `--input-type`, `--tdd-file`, `--prd-file`, `--no-compress`.
- Command-only flags confirmed: `--specs`, `--template/-t`, `--multi-roadmap`, `--interactive/-i`, `--compliance/-c`, `--persona/-p`.
- CLI-only flags confirmed: `--no-convergence`, `--input-type {auto,tdd,spec}`, `--tdd-file`, `--prd-file`, `--no-compress`, `--allow-regeneration`, `--resume`, `--max-turns`, `--retrospective`, `--model`, `--debug`.
- `commands.py:47` — `help="Output directory for all artifacts. Default: parent dir of spec-file."`
- `commands.py:213` — `resolved_output = output_dir if output_dir is not None else input_files[0].parent`
- `commands/roadmap.md:28` — default for `--output` documented as `.dev/releases/current/<spec-name>/`.

**Confidence:** high

---

### B-2 — `commands/validate-roadmap.md` frontmatter + flag-set drift

**Status:** PARTIAL (most verified; one minor refutation)

**Evidence:**
- `commands/validate-roadmap.md:2` — `name: validate-roadmap` (no `sc:` prefix). Confirmed inconsistent with `commands/roadmap.md:2` which has `name: sc:roadmap`.
- `commands/validate-roadmap.md:27-37` — flag table includes `--specs`, `--exclude/-x`, `--max-agents`, `--skip-adversarial`, `--skip-remediation`, `--report/-r`, `--prior-taxonomy`.
- `cli/roadmap/commands.py:295-320` — CLI `validate` exposes only `output_dir` (argument), `--agents`, `--model`, `--max-turns`, `--debug`. None of the command's deep-validation flags exist in CLI.
- CLI-only flags vs command: `--model`, `--max-turns`, `--debug` — confirmed CLI has these and command does not.
- `commands/validate-roadmap.md:30` — default `--output` documented as `{roadmap-dir}/validation/`.
- `cli/roadmap/validate_executor.py:468` — `validate_dir = config.output_dir / "validate"` (NOT `validation/`).
- `cli/roadmap/commands.py:353` — comment: `"# Surface results as CLI output (exit 0 per NFR-006)"`. NFR-006 is implemented in CLI but not documented in the command file (verified: grep for NFR-006 in command file returns nothing).

**Corrections to the original claim:**
- Output-dir mismatch is verified, but the scope doc says CLI writes to `<OUTPUT_DIR>/validate/` — that is correct (matches `validate_executor.py:468`). No correction needed here; flagging as confirmed.
- The "Command has, CLI does not" list is fully verified.
- One minor nit: the scope doc separately states the CLI defaults to `<OUTPUT_DIR>/validate/`; that is also what code does. No drift between scope doc and reality on the CLI side. Status held at PARTIAL only because the frontmatter `name: validate-roadmap` is a YAML-key issue (cosmetic) while the other items are substantive — claim is accurate but lumps together items of very different weight.

**Confidence:** high

---

### B-3 — `sc-roadmap-protocol/SKILL.md` pipeline taxonomy mismatch

**Status:** VERIFIED

**Evidence:**
- `skills/sc-roadmap-protocol/SKILL.md:84` — `## 4. Wave Architecture` and `:102` — `"sc:roadmap executes in 5 waves (0-4)."` Waves 0, 1A, 1B, 2, 3, 4 + Post-Wave (confirmed at `:104, :127, :151, :169, :206, :229, :247`).
- `SKILL.md:143-144` — explicit thresholds: `"convergence_score >= 0.6 → PASS"`, `">= 0.5 → PARTIAL"`, `"< 0.5 → FAIL"`.
- `skills/sc-roadmap-protocol/refs/validation.md:157-161` — aggregate thresholds: `">= 85% | PASS"`, `"70-84% | REVISE"`, `"< 70% | REJECT"`.
- `cli/roadmap/executor.py:2156-2170` — `_get_all_step_ids` returns 14 named step IDs: `extract, generate-{a}, generate-{b}, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification, deviation-analysis, remediate, certify`.
- Grep of `SKILL.md` for the six step names — none of `anti-instinct`, `spec-fidelity`, `wiring-verification`, `deviation-analysis`, `remediate`, `certify` appear in skill file.
- `SKILL.md:290` — `"Range: 2-10 agents"`. CLI `commands.py:298-302` — validate defaults to single agent `opus:architect`; run defaults to `opus:architect,haiku:architect` (2). No 2–10 enforcement in CLI run flow.

**Confidence:** high

---

### B-4 — `refs/scoring.md` stale CLI cross-reference

**Status:** PARTIAL (claim of PRD omission REFUTED; cross-reference accuracy issue VERIFIED)

**Evidence:**
- `refs/scoring.md:18` — `"This algorithm matches the CLI implementation at src/superclaude/cli/roadmap/executor.py:detect_input_type()"`.
- `refs/scoring.md:9-16` — describes TDD detection (4 signals, threshold ≥5).
- `refs/scoring.md:165-171` — PRD section exists ("PRD Supplementary Scoring"), discussing PRD enrichment but **does not document the PRD scoring algorithm itself**.
- `cli/roadmap/executor.py:73-148` — `detect_input_type` checks PRD signals **first** (5 PRD signals, threshold ≥5 returns "prd"), then TDD signals. The skill ref describes TDD-detection but its presentation order and signal set diverge from CLI: skill puts TDD detection at the top of `scoring.md`, omitting that PRD is checked FIRST in CLI.
- PRD-detection rule (5 signals: type field, 12 section headings, user-story pattern, JTBD pattern, tags) is **not** documented in `scoring.md` even though `executor.py:101-138` implements it.

**Corrections to the original claim:**
- The scope-doc claim says "PRD detection may have drifted or omitted" — verified that PRD scoring **rule** is omitted from `scoring.md`; only enrichment behavior is noted. The cross-reference at line 18 thus undersells the algorithm match.

**Confidence:** high

---

### B-5 — `refs/templates.md` 4-tier discovery vs single-template CLI

**Status:** VERIFIED

**Evidence:**
- `refs/templates.md:7-36` — 4 tiers explicitly defined: Tier 1 Local (`.dev/templates/roadmap/`), Tier 2 User (`~/.claude/templates/roadmap/`), Tier 3 Plugin `[future: v5.0]`, Tier 4 Inline generation.
- `cli/roadmap/templates.py:14` — `ROADMAP_TEMPLATE = "roadmap_template.compressed.md"` (single template constant).
- `cli/roadmap/templates.py:21-71` — `get_template_path(name)` tries `importlib.resources` then src-relative; no tier system, no user dir, no plugin marketplace. Resolves a single named template file.

**Confidence:** high

---

### B-6 — `refs/validation.md` sub-agent pattern absent from CLI

**Status:** VERIFIED

**Evidence:**
- `refs/validation.md:8` — `"Dispatch this prompt to a quality-engineer sub-agent."` and `:76` — `"Dispatch this prompt to a self-review sub-agent."`
- `refs/validation.md:171-196` — `## REVISE Loop` with `"Hard limit: 2 iterations"` (`:192`).
- `cli/roadmap/executor.py` — grep confirms NO `Task(`, NO `sub_agent`, NO `quality-engineer`, NO `self-review`, NO `REVISE` substrings (lone match for `agents_spawned` at `:2626` is a metadata field for remediate state, not sub-agent spawning).
- `cli/roadmap/validate_executor.py:122-134` — only spawns subprocess `ClaudeProcess` (NOT `Task` sub-agents).
- `cli/roadmap/validate_gates.py:30-69` — `REFLECT_GATE` and `ADVERSARIAL_MERGE_GATE` use frontmatter checks and semantic checks (gate criteria), not sub-agent dispatches.

**Confidence:** high

---

### B-7 — `refs/extraction-pipeline.md` 8-step extraction vs single CLI prompt

**Status:** VERIFIED

**Evidence:**
- `refs/extraction-pipeline.md:7-9` — `"## 8-Step Extraction Pipeline"` followed by `"Process the specification file in 8 sequential steps."`
- `cli/roadmap/executor.py:1885-1910` — single `Step(id="extract", ...)` constructed with `build_extract_prompt(...)` or `build_extract_prompt_tdd(...)`.
- `cli/roadmap/prompts.py:180` — `def build_extract_prompt(...)` and `:328` — `def build_extract_prompt_tdd(...)`. Both are single-prompt builders that produce one extraction step, not 8 chained steps.

**Confidence:** high

---

### B-8 — `refs/adversarial-integration.md` `sc:adversarial-protocol` delegation

**Status:** VERIFIED

**Evidence:**
- `refs/adversarial-integration.md:83, 102, 112, 126, 135, 137` — multiple `Skill sc:adversarial-protocol args: "..."` invocations.
- `SKILL.md:417-424` — `"sc:roadmap-protocol delegates to sc:adversarial-protocol via direct Skill invocation (SKILL-DIRECT per D-0001 reversal)"`.
- `cli/roadmap/prompts.py:878-902` — `build_debate_prompt` is a single-shot prompt builder: `"You are a structured debate facilitator..."` with depth-controlled rounds via `_DEPTH_INSTRUCTIONS` (`:18-37`). No call out to `sc:adversarial-protocol`.
- `cli/roadmap/executor.py:1960-1968` — `Step(id="debate", prompt=build_debate_prompt(...))` — single CLI step, no protocol delegation.

**Confidence:** high

---

### B-9 — `sc-validate-roadmap-protocol/SKILL.md` entirely different pipeline from CLI

**Status:** VERIFIED

**Evidence:**
- Phase headings grep: `SKILL.md:96` Pre-Phase 0, `:131, :317, :362, :461, :694, :797, :881` Phases 0–6, `:926` Post-Phase 6 = 7 numbered phases + 2 bracketing phases.
- `SKILL.md:341-344` — table lists CC1 Internal Consistency (Roadmap), CC2 Internal Consistency (Spec), CC3 Dependency & Ordering, CC4 Completeness Sweep.
- `SKILL.md:619, 640-645` — `verdict: "GO | CONDITIONAL_GO | NO_GO"` with explicit threshold rows.
- `SKILL.md:244` — `"Orchestrator-only: agents spawned in Phase 2 do NOT call Auggie."` (Auggie/Serena enrichment confirmed throughout).
- `cli/roadmap/validate_executor.py:435-512` — `execute_validate` flow: `_validate_input_files` → build single-agent (`_build_single_agent_steps`) or multi-agent (`_build_multi_agent_steps`) → `execute_pipeline` → `_parse_report_counts`. No phase taxonomy, no CC agents, no GO/NO-GO verdict.
- `cli/roadmap/validate_prompts.py:7, 68, 74-123` — 7 validation dimensions: Schema, Structure, Traceability, Cross-file consistency, Parseability, plus optional Coverage/Proportionality (input-aware) or Interleave/Decomposition.

**Confidence:** high

---

### B-10 — `sc-validate-roadmap-protocol` packaging shape

**Status:** VERIFIED

**Evidence:**
- `ls src/superclaude/skills/sc-validate-roadmap-protocol/` → only `SKILL.md` (56,503 bytes). No `refs/`, no `rules/`, no `templates/`.
- Compare with `ls /config/.claude/skills/sc-roadmap-protocol/` → `__init__.py, refs/, SKILL.md`. The roadmap skill has a `refs/` directory; the validate-roadmap skill does not.

**Confidence:** high

---

### B-11 — `/config/.claude/skills/` global-install gap

**Status:** REFUTED

**Evidence:**
- `ls /config/.claude/skills/sc-roadmap-protocol/` returns: `__init__.py`, `refs`, `SKILL.md` — skill IS present at global location.
- `ls /config/.claude/skills/sc-validate-roadmap-protocol/` returns: `SKILL.md` — skill IS present at global location.
- `md5sum` confirms byte-identical copies:
  - `cf3fe201fd9ae5a7c8995f45a994c4ad` for sc-roadmap-protocol SKILL.md across src, `.claude/`, and `/config/.claude/`.
  - `26e31d8772e1cfc683da8af75e7d5342` for sc-validate-roadmap-protocol SKILL.md across all three locations.

**Corrections to the original claim:**
- The scope-doc statement `"The global location /config/.claude/skills/ does not contain either skill"` is **false** as of 2026-05-15. Both skills are installed globally and are byte-identical to src and the repo-local `.claude/` copy. OQ-4 ("is global install intended?") is answered by current state: yes, both skills are globally installed.

**Confidence:** high

---

### B-12 — Synced copies will need refresh after src updates

**Status:** VERIFIED

**Evidence:**
- `md5sum` for `commands/roadmap.md`: all three copies (`src/`, `.claude/commands/sc/`, `/config/.claude/commands/sc/`) hash to `af661e03f8cf3db1990b53a1165f5ef2` — currently in sync.
- `md5sum` for `commands/validate-roadmap.md`: all three copies hash to `949cbc55b99f8fa52749360d12d47f92` — currently in sync.
- Claim of "three locations carry identical copies" is verified; the follow-on assertion ("after B-1 / B-2 land, both `.claude/` copies need re-sync") is mechanically correct because edits to `src/` would diverge from both synced locations until `make sync-dev` (and a manual copy to `/config/.claude/`) is run.

**Confidence:** high

---

## Verifier Notes

- All grep / md5 / ls evidence was generated in the verification session 2026-05-15.
- The major correction from the original scope doc is **B-11**: both skills are globally installed; the "missing global skills" framing is incorrect. Release planning should not include a "global install gap" workstream.
- **B-4** is partially overstated: the cross-reference statement is accurate for TDD detection but the skill ref omits the PRD detection algorithm that the CLI actually implements (PRD is checked first in CLI).
- **B-2** is accurate but mixes a cosmetic frontmatter `name:` issue with substantive flag/output-dir drift; status held PARTIAL only because the claim's claim of "name: validate-roadmap (no sc: prefix)" is verified and the rest is verified — i.e., the claim itself is accurate, classification reflects mixed-weight items rather than mixed accuracy. A reader could reasonably mark B-2 VERIFIED.
- All sync checks confirm `src/` ↔ `.claude/` ↔ `/config/.claude/` parity for both command files and both skills at the time of verification.
