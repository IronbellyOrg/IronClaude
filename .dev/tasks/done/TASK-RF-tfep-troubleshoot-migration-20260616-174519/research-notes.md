# Research Notes: Replace /sc:forensic with /sc:troubleshoot in TFEP

**Date:** 2026-06-16
**Scenario:** A (explicit — 8 steps + file targets grounded in originating session)
**Depth Tier:** Standard
**Track Count:** 1
**Status:** Complete

---

## EXISTING_FILES

Source-of-truth lives under `src/superclaude/` (CLAUDE.md SoT rule). `.claude/` mirrors are
sync-dev output and MUST NOT be hand-edited or staged. All edits target `src/` then `make sync-dev`.

- `src/superclaude/skills/sc-task-protocol/SKILL.md` — PRIMARY edit target. TFEP lives in section
  `### 4.5 Test Failure Escalation Protocol (TFEP)` spanning ~lines 133–260. Sub-sections:
  - `#### TFEP Prohibition Rules` (~137)
  - `#### Test Baseline Snapshot` (~153)
  - `#### Escalation Trigger Detection` (~164); "Escalation gradient (within-TFEP, for future forensic integration)" at line 172
  - `#### TFEP Execution Flow` (~181): Step 1 freeze (185), Step 2 context.yaml (190), **Step 3 Invoke forensic (205)** with the `/sc:forensic ...` invocation at **line 212**, **Step 4 Consume forensic results (215)** reading `{output_dir}/return-contract.yaml` at **216**, Step 5 tasklist insertion (224), Step 6 resume (231)
  - `#### TFEP Incident Reporting` (~237): "Forensic artifacts" at **250**, "committed to git alongside other forensic artifacts" at **253**
  - `#### Escalation Budget` (~255): `/sc:forensic --tier light` at **258**, `/sc:forensic --tier standard` at **259**, FULL STOP at **260**
- `src/superclaude/commands/task.md` — `--no-escalation` row references "structured forensic analysis" at **line 48**. Boundaries list also names TFEP.
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — diagnosis backend. Wave 0 parses flags
  (issue desc / `--scope` / `--type` / `--depth` / `--fix` / `--no-escalate` / `--output-dir` / `--no-mcp` /
  `--no-doc-discovery` / `--no-diagnosability-audit`). Wave 5 is Synthesis + Report. Output Contract table
  already carries `status`, `tier_reached`, `report_path`, `audit_log_path`, `confidence`,
  `test_is_wrong`, `test_file_path`, `behavior_is_documented`, etc. There is NO `--context`/`--caller`
  flag and NO `return-contract.yaml` emission today.
- `src/superclaude/commands/troubleshoot.md` — thin command. Options table (~lines 48–58). Activation
  hands off to `sc:troubleshoot-protocol`. No `--context`/`--caller`/`--return-contract` flags today.
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` — REPORT.md template; "Next Steps"
  section (~146). No TFEP-consumer block today.

## PATTERNS_AND_CONVENTIONS

- **SoT discipline**: edit `src/superclaude/` → `make sync-dev` → `make verify-sync`. NEVER stage `.claude/`
  (CLAUDE.md ABSOLUTE RULE). This is a hard verification gate for every edited skill/command.
- **Command/skill split**: command files are thin (parse flags → hand off to protocol skill). Behavioral
  spec lives in the `*-protocol/SKILL.md`. So a new `--context`/`--caller` flag must be added in BOTH the
  command Options table AND the skill Wave 0 parse step.
- **Flag table format**: markdown table `| Flag | Default | Description |` (troubleshoot.md), and
  `| `--flag`` | `default` | desc |` rows.
- **Output Contract format**: markdown table `| Field | Type | Description |` in the troubleshoot
  protocol skill; new emitted fields are added as rows + a derivation-rule paragraph.
- **TFEP step style**: numbered bold `**Step N: ...**` headings with a running numbered list; YAML/code
  fences for context.yaml and the incident-report template.
- **Escalation budget block**: a fenced code block mapping trigger count → invocation.
- **Backend-neutral language goal**: the analysis recommends renaming "forensic" → "diagnostic escalation"
  and adding `diagnostic_backend: troubleshoot`, so future backend swaps don't require re-editing prose.

## GAPS_AND_QUESTIONS

- Exact current line numbers in troubleshoot.md Options table and the protocol Wave 0 parse list (researcher R2 to pin).
- Whether the adapter `return-contract.yaml` should be authored BY troubleshoot (when `--caller task-unified`)
  or BY task-protocol after reading REPORT.md. The analysis recommends troubleshoot authors it (option 1);
  the tasklist should encode option 1 but flag the decision in Open Questions.
- Whether `commands/task.md` Boundaries list and any other doc surface (KNOWLEDGE.md, release notes) also
  name `/sc:forensic` and need updating (researcher R3 to sweep repo-wide).
- Whether a separate `refs/tfep.md` should hold the adapter contract vs inline in SKILL.md (skill is small;
  the v5.xxforensic archive suggested an optional `refs/tfep.md`). Tasklist should pick inline unless R3 finds size pressure.
- `make verify-sync` must pass after each skill/command edit — confirm no `.claude/`-only drift introduced.

## RECOMMENDED_OUTPUTS

Researcher files to create in `research/`:
- `01-file-inventory.md` (R1) — exact line ranges of every TFEP sub-section + every `forensic` token in
  sc-task-protocol/SKILL.md and task.md; the full edit-anchor map for the rename (step 1) and steps 4–8.
- `02-troubleshoot-surface.md` (R2) — troubleshoot command Options table + protocol Wave 0 parse step +
  Output Contract fields + Wave 5 report emission point; exact anchors for adding `--context`/`--caller`
  (step 3) and the `return-contract.yaml` emission (steps 2,5).
- `03-integration-and-sync.md` (R3) — every cross-reference between task-protocol and forensic/troubleshoot
  across the repo; report-template TFEP-consumer block location; the sync-dev/verify-sync verification
  contract; repo-wide `/sc:forensic` sweep for residual references.
- `04-template-and-examples.md` (R4) — MDTM template 02 PART 1 rules (A3 granularity, B2 self-containment,
  M3 QA sequence, anti-orphaning) + a recent TASK-RF example for structural patterns.

## SUGGESTED_PHASES

- R1 (File Inventory): scope = `src/superclaude/skills/sc-task-protocol/SKILL.md`, `src/superclaude/commands/task.md`.
  Output `research/01-file-inventory.md`. Covers the rename anchor map + steps 1,4,5,6,7,8 insertion points.
- R2 (Patterns & Conventions / Integration): scope = `src/superclaude/commands/troubleshoot.md`,
  `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`. Output `research/02-troubleshoot-surface.md`.
  Covers steps 2 (adapter contract field shape vs existing Output Contract) and 3 (`--context`/`--caller`).
- R3 (Integration Points): scope = repo-wide grep for `forensic`/`sc:forensic`/`return-contract` + report-template +
  Makefile sync targets. Output `research/03-integration-and-sync.md`. Covers steps 2,7,8 + verification contract.
- R4 (Template & Examples): scope = `.claude/templates/workflow/02_mdtm_template_complex_task.md` + one
  recent `.dev/tasks/to-do/TASK-RF-*` example. Output `research/04-template-and-examples.md`.

Each researcher told the others' scope to avoid overlap. R1 owns task-protocol; R2 owns troubleshoot surface;
R3 owns cross-repo + sync + report-template; R4 owns template mechanics.

## TEMPLATE_NOTES

- **Template 02** (complex): the work is discovery → multi-file surgical edits → per-file verify-sync → a final
  validation phase. Interlocking edits (rename in step 1 changes the strings steps 5/7/8 edit) require ordered phases.
- **Tier Standard**: ~4–5 core files, small but interdependent, no large net-new code — fits Standard.
- Generated tasklist must use: per-edit granular items (one item per `forensic` anchor / per new flag / per
  contract field), B2 self-containment, explicit `make sync-dev` + `make verify-sync` verification items after
  each skill/command edit, and a final QA gate. QA_GATE_REQUIREMENTS = PER_PHASE. TESTING_REQUIREMENTS = NONE
  (docs/skill prose — no Python tests; verification is verify-sync + manual protocol read-through).
  VALIDATION_REQUIREMENTS = "make verify-sync passes; no `.claude/` path staged; rg '/sc:forensic' returns only
  intentional historical/archive references."

## AMBIGUITIES_FOR_USER

1. **Execution branch/location.** This tasklist is being BUILT in the SprintRun429 worktree's sibling main repo
   path but is UNRELATED to the 429 recovery feature. It should be EXECUTED on its own feature branch
   (e.g. `feat/tfep-troubleshoot-backend`), NOT on `SprintRun429`. Flag for the user at A.11.
2. **Adapter ownership** (step 4): the tasklist encodes "troubleshoot authors return-contract.yaml when
   `--caller task-unified`" (analysis option 1). If the user prefers task-protocol to derive the contract from
   REPORT.md instead, the step-2/step-5 items must move ownership. Documented as an Open Question.
3. **Inline vs refs/tfep.md** for the adapter contract — defaulting to inline in sc-task-protocol/SKILL.md
   unless R3 finds the section grows too large.
