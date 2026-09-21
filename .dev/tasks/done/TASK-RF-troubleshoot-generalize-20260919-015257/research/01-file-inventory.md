# Research: File Inventory

**Topic type:** File Inventory (with anchor verification)
**Scope:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, all `refs/*.md` in that skill, `src/superclaude/agents/confidence-calibrator.md`, `src/superclaude/agents/evidence-validator.md`, `src/superclaude/agents/root-cause-analyst.md`, `src/superclaude/commands/troubleshoot.md`
**Spec:** `/config/workspace/Coder/.claude/worktrees/gh-automation-orca-run/.dev/research/sysbox-retrospective-20260918/merged-report-v2.md` §(d) R-01..R-19 (lines 151-660)
**Status:** Complete
**Date:** 2026-09-19

---

## Line counts (wc -l, 2026-09-19)

| File | Lines |
|---|---|
| `SKILL.md` | 602 |
| `refs/calibrator-eval-cases.md` | 81 |
| `refs/contract-enumeration.md` | 30 |
| `refs/diagnosability-audit.md` | 340 |
| `refs/doc-discovery.md` | 182 |
| `refs/effective-input-proof.md` | 27 |
| `refs/escalation-rubric.md` | 90 |
| `refs/hardening-output-contract.md` | 71 |
| `refs/hypothesis-card-template.md` | 154 |
| `refs/pipeline-hardening-closure.md` | 63 |
| `refs/remediation-handoff.md` | 139 |
| `refs/report-template.md` | 319 |
| `refs/runtime-entrypoint-verification.md` | 47 |
| `refs/triage-checklist.md` | 65 |
| `refs/unmask-and-sweep.md` | 52 |
| `agents/confidence-calibrator.md` | 141 |
| `agents/evidence-validator.md` | 128 |
| `agents/root-cause-analyst.md` | 56 |
| `commands/troubleshoot.md` | 204 |

Spec's stated baseline: "SKILL ... (602-line baseline)" (merged-report-v2.md:20) — matches current wc.

## 1. `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (602 lines)

**Purpose**: tiered troubleshooting protocol; frontmatter L1-5 (`name`, `description`, `allowed-tools`); Waves 0-6.

### Section map (heading → line range)

| Heading | Lines |
|---|---|
| frontmatter | 1-5 |
| extended metadata comment | 7-12 |
| `# Troubleshoot Protocol` | 14 |
| `## Purpose` | 16-24 |
| `## Required Input (STOP if missing)` | 26-35 |
| `## Output Contract` (table L41-77; derivation rules L79-91) | 37-91 |
| `## Wave Structure` (code block L95-108) | 93-110 |
| `### Wave 0: Parse + Validate Input` | 114-152 |
| `### Wave 1: Tier 1 — Real-Code Grounding` | 156-175 |
| `### Wave 1.5: Documentation Grounding` | 179-213 |
| `### Wave 1.6: Diagnosability Audit` | 217-268 |
| `### Wave 1.7: Tier 1 — Hypothesis Formation` | 272-288 |
| `### Wave 2: Confidence Gate` | 292-308 |
| `### Wave 3: Tier 2 — Parallel Hypotheses` | 312-373 |
| `#### Tier 2 calibration completeness gate` | 348-358 |
| `### Wave 4: Tier 2 — Adversarial Fix Debate` | 377-402 |
| `### Wave 4.5: Pipeline Hardening Closure` | 406-422 |
| `### Wave 5: Synthesis + Report` | 426-481 |
| `### Wave 6: Tier 3 — Remediation Chain` | 485-499 |
| `## Tool Coordination Summary` | 503-516 |
| `## Will Do` | 518-530 |
| `## Will Not Do` | 532-545 |
| `## Error Handling` | 547-570 |
| `## Token Cost Profile` | 572-582 |
| `## Refs` (table L586-600; closing sentence L602) | 584-602 |

### Anchor verification — SKILL

Every anchor the spec cites (merged-report-v2.md §(c)/§(d)/§(e)/baseline list at L765-778). Line numbers below are the CURRENT file (read 2026-09-19). Tag: [CODE-VERIFIED] = content at that line matches the spec's description; [CODE-CONTRADICTED] = spec description does not match, actual location given.

| Spec anchor | Spec's description | Current line | Verbatim (trimmed) | Tag | Suggested `old_string` for Edit |
|---|---|---|---|---|---|
| `SKILL:41-77` (R-01) | Output Contract table | 41-77 | L41 `\| Field \| Type \| Description \|`; L77 `\| \`solution_summary\` \| string \| TFEP adapter field ...` | [CODE-VERIFIED] | Insert after L77 row — unique tail: `Empty string when no fix is proposed (e.g. \`recommended_escalation: halt\`). \|` |
| `SKILL:62` (R-17) | `contract_version` field, names unchanged | 62 | `\| \`contract_version\` \| semver string \| Output-contract semver, default \`1.1.0\`.` | [CODE-VERIFIED] | `\| \`contract_version\` \| semver string \|` |
| `SKILL:64` (AP-20) | `pipeline_hardening_verdict` enum | 64 | `\| \`pipeline_hardening_verdict\` \| enum \`pass \\\| blocked \\\| advisory \\\| not_applicable\` \|` | [CODE-VERIFIED] | `` enum `pass \| blocked \| advisory \| not_applicable` `` |
| `SKILL:76` (R-10) | `root_cause_summary` empty string when inconclusive | 76 | `\| \`root_cause_summary\` \| string \| TFEP adapter field ... Empty string when diagnosis is inconclusive. \|` | [CODE-VERIFIED] | `Empty string when diagnosis is inconclusive.` |
| `SKILL:97` (R-01) | wave map Wave 1 line | 97 | `Wave 1: Tier 1 — Real-Code Grounding  ← always; loads refs/triage-checklist.md on demand (grounding + reproduce only)` | [CODE-VERIFIED] | `(grounding + reproduce only)` |
| `SKILL:104` (R-17) | wave map Wave 4.5 line mentioning H0-H5 | 104 | `Wave 4.5: Pipeline Hardening Closure ← conditional, when pipeline_hardening_applicable=true (issue topology); runs gates H0-H5; loads the 6 hardening refs` | [CODE-VERIFIED] | `runs gates H0-H5; loads the 6 hardening refs` |
| `SKILL:122-127` (§e) | auto-detect `--type` keyword rows | 122-127 | L122 `- Stack trace, exception name, ... → \`bug\``; L127 `- "pytest", "jest", "flake", ... → \`test\`` | [CODE-VERIFIED] | n/a (read-only cite) |
| `SKILL:167` (R-01) | step-1 fallback bullet | 167 | `   - If \`--no-mcp\` or both MCPs are unavailable: fall back to \`Glob\` + \`Grep\` on the issue keywords; note the fallback in the audit log.` | [CODE-VERIFIED] | `note the fallback in the audit log.` |
| `SKILL:168` (R-01) | "Reproduce or observe (when feasible and cheap)" | 168 | `2. **Reproduce or observe** (when feasible and cheap):` | [CODE-VERIFIED] | `2. **Reproduce or observe** (when feasible and cheap):` |
| `SKILL:230` (R-02) | S1.6.0 `failing_component` sentence | 230 | `1. **S1.6.0 — Component identification**. ... Record as \`failing_component\` in the audit log. Branches A and B scope queries to this component first; expand outward only if no signal is found.` | [CODE-VERIFIED] | `expand outward only if no signal is found.` |
| `SKILL:240-241` (R-04) | S1.6.4 branch | 240-241 | L240 `5. **S1.6.4 — Apply sufficiency rubric + complexity gate**. Compute \`diagnosability_verdict ∈ {sufficient \| partial \| insufficient \| unknown}\`. ... Branch on \`(verdict × complexity)\`:` | [CODE-VERIFIED] | `Branch on \`(verdict × complexity)\`:` |
| `SKILL:241` (R-03, R-04, R-06, AP-07, AP-11) | hard-stop bullet; last sentence "No hypothesis work happens in the same turn as the instrumentation patch." | 241 | `   - \`insufficient\` AND \`non-trivial\` AND NOT \`--no-escalate\` → **hard-stop**: emit \`diagnosability-tasklist.md\`, set \`diagnosability_hard_stop=true\`, jump to Wave 5 with status \`partial\` (Waves 1.7-4 skipped). No hypothesis work happens in the same turn as the instrumentation patch.` | [CODE-VERIFIED] | `No hypothesis work happens in the same turn as the instrumentation patch.` — NOTE: this sentence ALSO appears at L530 (Will Do) as `no hypothesis work happens in the same turn as an instrumentation patch` (lowercase, "an") — different casing, so the L241 string is unique as written. |
| `SKILL:248` (R-04) | counter rule "each hard-stop fires the counter +1" | 248 | `**Per-defect patch-round counter**: the Wave 1.6 orchestrator maintains \`<output-dir>/diagnosability-rounds.json\` keyed by the Wave 0 \`issue_slug\`. Each hard-stop fires the counter +1. After 3 rounds for the same defect, the off-ramp message escalates (see refs/report-template.md hard-stop variant + cap prose). Reset via \`--reset-diagnosability-rounds\`.` | [CODE-VERIFIED] | `Each hard-stop fires the counter +1.` |
| `SKILL:266` (R-04) | 3-round cap row | 266 | `\| 3-round diagnosability cap reached for an \`issue_slug\` \| Per-defect counter at \`<output-dir>/diagnosability-rounds.json\` reached 3 hard-stops \| Emit the 3-round cap message (refs/report-template.md hard-stop variant + cap-specific prose); refuse next tasklist until \`--reset-diagnosability-rounds\` is set \|` | [CODE-VERIFIED] | WARNING: this exact row is DUPLICATED at L570 (Error Handling table). Use `occurrence`/surrounding context — L266 is preceded by the Heisenbug row L265 and followed by L268 `**Token budget**: ≤ 2-3k`. For L266 include preceding row text; `replace_all` only if both should change. |
| `SKILL:270/272` (task-prompt list; not in spec §d) | L270 = `---` separator; L272 = Wave 1.7 heading | 270, 272 | L270 `---`; L272 `### Wave 1.7: Tier 1 — Hypothesis Formation` | [CODE-VERIFIED] (structure only; the spec itself never cites 270/272 — grep L1-780 found no such cite) | `### Wave 1.7: Tier 1 — Hypothesis Formation` |
| `SKILL:276` (task-prompt list) | Wave 1.7 preconditions | 276 | `**Preconditions**: Wave 1 (real-code grounding) is complete; Wave 1.5 has produced a Documentation Context Card ... When Wave 1.6 hard-stopped, this wave is skipped entirely.` | [CODE-VERIFIED] (spec §d does not cite 276 directly) | `When Wave 1.6 hard-stopped, this wave is skipped entirely.` |
| `SKILL:280` (R-01) | `consistency_with_docs` "returned unread" analogue | 280 | `1. **Form one hypothesis** — spawn the \`root-cause-analyst\` agent ... The hypothesis card MUST set \`consistency_with_docs\` to one of \`aligned \| conflicts \| not_applicable \| no_docs_found\` based on the Documentation Context Card (or \`not_applicable\` when the card path is \`null\`).` | [CODE-VERIFIED] | `(or \`not_applicable\` when the card path is \`null\`).` (unique on L280; L339 uses a different phrasing) |
| `SKILL:298-304` (AP-14) | Wave 2 decision logic | 298-304 | L298 `- \`--depth quick\` OR \`--no-escalate\` → STOP at Tier 1 ...`; L304 `  - Reproducibility unclear or "intermittent" mentioned → escalate.` | [CODE-VERIFIED] | n/a (read-only cite) |
| `SKILL:333-336` (R-09, AP-13) | Wave 3 step 1 MCP enrichment; auggie bullet at :336 | 333-336 | L333 `1. **MCP enrichment in parallel with agent spawn** — ...`; L336 `   - \`mcp__auggie__codebase-retrieval\` with a more targeted query than Tier 1 (e.g. "find every call site of \`<symbol>\` and how they handle the error case")` | [CODE-VERIFIED] | `and how they handle the error case")` |
| `SKILL:337-343` (AP-08, R-02) | Wave 3 step 2 spawn; :342 "at most one proposed fix" | 337-343 | L337 `2. **Spawn hypothesis agents** in parallel via \`Task\` ...`; L342 `   - An instruction to produce **at most one proposed fix** with: claim, evidence (cited file:line or command output), proposed fix, confidence, risks, \`consistency_with_docs\` (see \`refs/hypothesis-card-template.md\`), and a one-line "if I'm wrong it's probably because...".`; L343 `   - Use the agent's default model. ...` | [CODE-VERIFIED] | `and a one-line "if I'm wrong it's probably because...".` |
| `SKILL:346` (R-08, AP-06) | "cluster by fix" step | 346 | `4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.` | [CODE-VERIFIED] | `If they all converge on one fix, mark as **consensus**.` |
| `SKILL:348` (R-08) | calibration completeness gate header | 348 | `#### Tier 2 calibration completeness gate (hard precondition for report publishing)` | [CODE-VERIFIED] | `#### Tier 2 calibration completeness gate` |
| `SKILL:358` (R-12) | marker verification command | 358 | `Verification command (run before publishing): for each \`tier2-*-hypothesis.md\` (excluding \`*-calibration.md\`), assert a matching \`*-calibration.md\` exists and contains the Calibration Report markers ...` | [CODE-VERIFIED] | `Verification command (run before publishing):` |
| `SKILL:372` (R-08) | "All agents converge with high confidence → skip Wave 4" | 372 | `\| All agents converge with high confidence \| Skip Wave 4 (adversarial); jump to Wave 5 \| None \|` | [CODE-VERIFIED] | `\| All agents converge with high confidence \| Skip Wave 4 (adversarial); jump to Wave 5 \| None \|` |
| `SKILL:381` (R-08, AP-06) | Wave 4 precondition | 381 | `**Preconditions**: Wave 3 marked ≥ 2 fixes as \`competing\` (or \`--depth deep\` + ≥ 2 distinct proposals, even if consensus).` | [CODE-VERIFIED] | `(or \`--depth deep\` + ≥ 2 distinct proposals, even if consensus).` |
| `SKILL:386-397` (R-08) | `--compare` adversarial invocation | 386-397 | L386 `2. **Invoke \`/sc:adversarial\` in compare mode** via \`Skill\`:`; L389 `   Skill sc:adversarial-protocol with --compare fix-1.md,fix-2.md[,fix-3.md] \\`; L397 `3. **Collect adversarial output** — ...` | [CODE-VERIFIED] | n/a (read-only cite) |
| `SKILL:410` (AP-04) | boundary list in Wave 4.5 Trigger | 410 | `**Trigger**: Topology-driven, **not** a CLI flag (NFR-5). ... H0 sets \`pipeline_hardening_applicable=true\` when the issue touches a trigger boundary (CLI/subprocess, file/stdin/prompt delivery, generated-artifact parser, ...)` | [CODE-VERIFIED] | `H0 sets \`pipeline_hardening_applicable=true\`` |
| `SKILL:410-420` (R-17) | Wave 4.5 H0-H5 steps | 410-420 | L414 `1. **H0 — Applicability + mechanism** (...)`; L415 `2. **H1 — Runtime-entrypoint verification**`; L416 `3. **H2 — Contract enumeration**`; L417 `4. **H3 — Unmask and sweep**`; L418 `5. **H4 — Effective-input proof**`; L419 `6. **H5 — Off-path reviewer rule**`; L420 `7. **Verdict aggregation** (...): compute \`pipeline_hardening_verdict\` ∈ \`pass \| blocked \| advisory \| not_applicable\` deterministically from the H0–H5 statuses ...` | [CODE-VERIFIED] | Each `**H<n> — ` label is unique. NOTE: `H0–H5` (en-dash) at L63, L408, L420, L444; `H0-H5` (hyphen) at L104. R-17 regex `\bH[0-5]\b` must cover both dash forms and L414 "H1–H5 cannot be silently skipped". |
| `SKILL:414` (AP-04) | HC0 step | 414 | see above | [CODE-VERIFIED] | `1. **H0 — Applicability + mechanism**` |
| `SKILL:420` (AP-20) | verdict aggregation step 7 | 420 | see above | [CODE-VERIFIED] | `7. **Verdict aggregation**` |
| `SKILL:433-450` (AP-09) | Wave 5 step 2 compose | 433-450 | L433 `2. Compose \`REPORT.md\` filling in:`; L450 (see below) | [CODE-VERIFIED] | n/a |
| `SKILL:439` (R-07, AP-15) | Evidence bullet | 439 | `   - Evidence (cited \`file:line\` and command outputs)` | [CODE-VERIFIED] | `   - Evidence (cited \`file:line\` and command outputs)` |
| `SKILL:450` (R-10) | "last compose-step bullet, before step 3 validation" | 450 | `   When \`diagnosability_hard_stop=true\`, replace the Diagnosis section with a "Halted — instrumentation required" prose block ... render the top-of-report Diagnosability Caveat banner above the Summary section (template in refs/report-template.md).` | [CODE-VERIFIED] — NOTE: L450 is a paragraph, not a bullet; the last *bullet* is L444 (Pipeline Hardening Closure). L450 is still the last line of step 2 before L451 step 3, so the insertion point "after L450" is correct. | `render the top-of-report Diagnosability Caveat banner above the Summary section (template in refs/report-template.md).` |
| `SKILL:451` (R-11, AP-16) | evidence-validator sentence | 451 | `3. **File:line validation pass (non-negotiable)** — spawn the \`evidence-validator\` agent via \`Task\` with \`report_draft_path=<output-dir>/REPORT.md.draft\`, ... Apply its verdict: remove dropped citations from the final \`REPORT.md\`; if any were dropped, set the report's frontmatter \`status: partial\` and add a "Grounding Gaps" entry referencing them.` | [CODE-VERIFIED] | `and add a "Grounding Gaps" entry referencing them.` |
| `SKILL:452` (R-12) | validator fallback bullet | 452 | `   - **Fallback**: if \`evidence-validator\` fails (subprocess crash, malformed output, agent unavailable), inline-validate citations in the orchestrator context (the original Wave 5 step 3 behavior); mark \`status: partial\` and add a Grounding Gap entry noting the validator was unavailable. The inline path is the fallback — never ship without validation.` | [CODE-VERIFIED] | `The inline path is the fallback — never ship without validation.` |
| `SKILL:491` (AP-12) | Wave 6 step 1 ask one yes/no | 491 | `1. **Present the remediation offer** to the user — read the prompt template in \`refs/remediation-handoff.md\`. Ask one yes/no question. Wait.` | [CODE-VERIFIED] | `Ask one yes/no question. Wait.` |
| `SKILL:512` (task-prompt list) | Task row in Tool Coordination table | 512 | `\| \`Task\` (agent spawn) \| ✓ (root-cause-analyst + confidence-calibrator; Wave 1.6: 2 parallel audit branches A/B + 1 orchestrator synthesis) \| ✓ (2-4 hypothesis agents in parallel + per-card confidence-calibrator + evidence-validator at Wave 5) \| ✓ (self-review for post-exec) \|` | [CODE-VERIFIED] (spec §d does not cite 512 directly) | `\| \`Task\` (agent spawn) \|` |
| `SKILL:532-545` (R-12) | Will Not Do list | 532-545 | L532 `## Will Not Do`; L534 first bullet `- Apply code changes without \`--fix\` ...`; L545 last bullet | [CODE-VERIFIED] | `## Will Not Do` |
| `SKILL:545` (R-03, R-13) | last Will-Not bullet | 545 | `- Allow the diagnosability tasklist to target the failing component's own source code — every task MUST target an invocation site (test script, CI workflow YAML, dev harness, container entrypoint, dev-mode config override). Diagnostic code in production source leaks into release artifacts.` | [CODE-VERIFIED] | `Diagnostic code in production source leaks into release artifacts.` |
| `SKILL:572-582` (AP-17) | Token Cost Profile | 572-582 | L572 `## Token Cost Profile`; L582 (below) | [CODE-VERIFIED] | n/a |
| `SKILL:582` (R-12) | "targets, not hard caps" | 582 | `These are targets, not hard caps. Auggie tokens are offloaded ... (Wave 1.6 hard-stop case yields a net token *saving* vs the full Tier 2 path — early halt prevents Tier 2 hypothesis-round token spend on blind code.)` | [CODE-VERIFIED] | `These are targets, not hard caps.` |
| `SKILL:584-602` (task-prompt list) | Refs section | 584-602 | L584 `## Refs`; L586 `\| File \| When loaded \|`; L602 `Each ref is loaded only by the wave that needs it. Do not pre-load.` | [CODE-VERIFIED] | `## Refs` |
| `SKILL:595-600` (R-17) | hardening refs rows | 595-600 | L595 `\| \`refs/pipeline-hardening-closure.md\` \| Wave 4.5 (mode skeleton, H0 applicability + boundary-scan schema, H5 off-path-reviewer rule) \|`; L596 `... hardening-output-contract.md ...`; L597 `... (H1 runtime-entrypoint card ...)`; L598 `... (H2 contract ledger ...)`; L599 `... (H3 classifier ...)`; L600 `\| \`refs/effective-input-proof.md\` \| Wave 4.5 (H4 fail-closed effective-input manifest) \|` | [CODE-VERIFIED] | each row's `refs/<name>.md` is unique |
| `SKILL:600` (R-05) | last refs row; insert `refs/primitive-differential.md` after | 600 | `\| \`refs/effective-input-proof.md\` \| Wave 4.5 (H4 fail-closed effective-input manifest) \|` | [CODE-VERIFIED] | `\| \`refs/effective-input-proof.md\` \| Wave 4.5 (H4 fail-closed effective-input manifest) \|` |
| `SKILL:602` (task-prompt list) | closing sentence | 602 | `Each ref is loaded only by the wave that needs it. Do not pre-load.` | [CODE-VERIFIED] | `Each ref is loaded only by the wave that needs it. Do not pre-load.` |

### SKILL — H0-H5 occurrences (R-17 rename regression guard)

`grep -nE '\bH[0-5]\b'` on SKILL.md — see §"H-token census" at end of this file (computed after all files read).

### SKILL — other notes for the builder

- `SKILL:4` `allowed-tools` already includes `Bash`, `Write`, `Edit`, `Task` — no frontmatter change needed for R-01..R-19.
- L241 hard-stop sentence also has a near-duplicate at L530 (`## Will Do`, "no hypothesis work happens in the same turn as an instrumentation patch"). R-03/R-06 edits at L241 do not auto-propagate to L530; builder decides whether L530 needs the same edit.
- L266 and L570 are byte-identical rows (3-round cap) — any R-04 edit to the cap row must consider both.
- L262-264 and L566-568 are also duplicated (Wave 1.6 failure table mirrored in Error Handling).
- The spec's "S1.6.0b" insert goes after L230; the next numbered step L232 is `2. **S1.6.1 — Load ...`, with a blank line L231 between.

## 2. `refs/triage-checklist.md` (65 lines) — touched by R-02, R-15

**Purpose**: Wave 1 cause-class checklist passed to `root-cause-analyst` (L3).

| Heading | Lines |
|---|---|
| `# Triage Checklist (Wave 1)` | 1-3 |
| `## Pre-investigation grounding` | 5-14 |
| `## Cause-class scan` (table L20-34) | 16-34 |
| `## Evidence-or-drop check` (bullets L40-42; closing sentence L44) | 36-44 |
| `## Fix sketch` | 46-54 |
| `## When to refuse Tier 1` (bullets L60-63; closing L65) | 56-65 |

| Spec anchor | Spec's description | Current line | Verbatim | Tag | `old_string` |
|---|---|---|---|---|---|
| `:33` (R-15) | "the `Build / packaging` row"; insert new cause-class row after it | 33 | `\| **Build / packaging** \| Module not found at runtime, version mismatch, install step missing \|` | [CODE-VERIFIED] (L34 is `\| **Other** \| ...` — new row lands before Other) | `\| **Build / packaging** \| Module not found at runtime, version mismatch, install step missing \|` |
| `:42` (R-15) | evidence-or-drop, add after line 42 | 42 | `- A pointer to the failing test and the exact assertion that fires` | [CODE-VERIFIED] (last bullet of the list; L43 blank; L44 closing sentence) | `- A pointer to the failing test and the exact assertion that fires` |
| `:44` (R-02) | new section after line 44 | 44 | `If none of these are available, the hypothesis card is marked \`unverified\` and the confidence dimension "Evidence grounding" is scored 0.0.` | [CODE-VERIFIED] (end of Evidence-or-drop section; L46 is `## Fix sketch`) | `"Evidence grounding" is scored 0.0.` |
| `:63` (R-15) | refuse-Tier-1 list, add after line 63 | 63 | `- The user's description is ambiguous in a way that a single hypothesis would have to guess at the actual symptom` | [CODE-VERIFIED] (last bullet; L65 is the closing "Refusal is not failure" line) | `would have to guess at the actual symptom` |
| `:5-14`, `:20-34`, `:36-44`, `:56-65` (baseline) | grounding / table / evidence / refuse | as listed | headings above | [CODE-VERIFIED] | n/a |

Note: if R-15's row is inserted after L33 AND R-02's section after L44, line numbers below L33 shift by +1 after the first edit — use text anchors, not numbers.

## 3. `refs/diagnosability-audit.md` (340 lines) — touched by R-03, R-04, R-06, R-15

**Purpose**: Wave 1.6 audit rules — branches, schemas, S1-S13 sufficiency rubric, complexity gate, context card, tasklist rules + hard constraints, T4 example.

| Heading | Lines |
|---|---|
| `## Section 1: Auggie query templates per branch` | 9-43 |
| `## Section 2: Fallback paths` | 47-74 |
| `## Section 3: Structured-output schemas` | 78-116 |
| `## Section 4: Sufficiency rubric + 3-W's synthesis` | 120-159 |
| `### Sufficiency rubric` (table header L136; S1 L138 … S13 L150) | 134-150 |
| `### Behavior under degradation` | 152-159 |
| `## Section 5: Complexity gate` | 163-188 |
| `### Signal table` (table header L169; rows L171-177) | 167-177 |
| `### Classification rule` | 179-182 |
| `## Section 6: Diagnosability Context Card template` (code block L196-234) | 192-234 |
| `## Section 7: Tasklist generation rules + hard constraints` | 238-284 |
| `### Hard constraints (non-negotiable)` (items 1-4 at L244-247) | 242-247 |
| `### High-specificity per-line task format` | 249-256 |
| `### Worked tasklist skeleton` (code block L260-278) | 258-280 |
| `### Patch-round counter` | 282-284 |
| `## Section 8: T4 worked example` | 288-334 |
| `## Loading discipline` | 338-340 |

| Spec anchor | Spec's description | Current line | Verbatim | Tag | `old_string` |
|---|---|---|---|---|---|
| `:150` (R-03) | row S13; insert S14 after | 150 | `\| **S13**: Intermittent keywords present AND 3-W's \`when_answerable != yes\` \| \`insufficient\` (intermittent-with-no-trace short-circuit) \|` | [CODE-VERIFIED] (L151 blank, L152 `### Behavior under degradation`) | `(intermittent-with-no-trace short-circuit) \|` |
| `:134-150`, `:138-139` (baseline) | S1-S13; S1/S2 | 138, 139 | L138 `\| **S1**: Symptom is a deterministic exception ...`; L139 `\| **S2**: Symptom is a build/compile error ...` | [CODE-VERIFIED] | n/a |
| `:169-177` (baseline) | complexity signal table | 169-177 | L169 `\| Signal \| Source \| Weight \|` … L177 `\| \`--type security\` set \| Wave 0 parse \| **Always non-trivial (override)** \|` | [CODE-VERIFIED] | n/a |
| `:176` (R-15) | signal-table row to replace | 176 | `\| Cause class from Wave 1 triage ∈ {Race/concurrency, Stale state/cache, Performance/resource} \| Wave 1 checklist scan \| +1 \|` | [CODE-VERIFIED] — the spec's replacement text is this row with `, Substituted primitive` appended inside the braces | `∈ {Race/concurrency, Stale state/cache, Performance/resource} \| Wave 1 checklist scan \| +1 \|` |
| `:177` (task-prompt list) | last signal row | 177 | see above | [CODE-VERIFIED] | n/a |
| `:241` (task-prompt list) | "hard constraints" | 241 | **BLANK LINE** | [CODE-CONTRADICTED] — L241 is empty. The Section 7 intro paragraph is L240; the `### Hard constraints (non-negotiable)` header is L242. The spec's own text cites `:242-247` (correct); `:241` appears only in the task prompt's list. Use L242. | `### Hard constraints (non-negotiable)` |
| `:242-247` (R-06, AP-11) | hard constraints 1-4 | 242-247 | L242 `### Hard constraints (non-negotiable)`; L244 `1. **Invocation-site-only**: ...`; L245 `2. **Additive only**: ...`; L246 `3. **Reversible**: ...`; L247 `4. **Revert annotation**: Patches added by the tasklist carry the comment \`# Diagnosability-tasklist instrumentation: revert after defect closed.\` so cleanup is mechanizable.` | [CODE-VERIFIED] | `so cleanup is mechanizable.` |
| `:247` (R-03) | "last hard constraint"; insert constraint 5 after | 247 | see above | [CODE-VERIFIED] (L248 blank; L249 `### High-specificity per-line task format`) | `so cleanup is mechanizable.` |
| `:263` (R-03) | tasklist skeleton header line; append Round/re-run/capability-verdict | 263 | `**Verdict**: <verdict>  **Complexity**: <complexity>  **failing_component**: <path>  **Round**: <N> of 3` | [CODE-VERIFIED] — NOTE: the line ALREADY has `**Round**: <N> of 3`; the spec's paste-ready header repeats `**Round**` — builder should merge, not duplicate. | `**failing_component**: <path>  **Round**: <N> of 3` |
| `:271`, `:328` (baseline) | strace task line (skeleton + T4) | 271, 328 | L271 `### Task 3: Run with strace at invocation (Linux only — skip on non-Linux CI)`; L328 `3. **Task 3**: Wrap \`subprocess.run\` with \`strace -f -e trace=read,write,futex\` ...` | [CODE-VERIFIED] | n/a |
| `:320-334` (baseline) | T4 hard-stop fires … What was saved | 320-334 | L320 `- → **Hard-stop fires.** ...`; L334 `Without Wave 1.6 the protocol would have spent ...` | [CODE-VERIFIED] | n/a |

Also relevant: L284 `### Patch-round counter` prose says "The counter increments +1 each time the hard-stop fires" — R-04's counter rewrite at `SKILL:248` has a sibling here; builder should decide whether to align (`old_string`: `The counter increments +1 each time the hard-stop fires for an \`issue_slug\`.`).

## 4. `refs/hypothesis-card-template.md` (154 lines) — touched by R-01, R-07

| Heading | Lines |
|---|---|
| `## Template` (code block L9-116) | 7-116 |
| card frontmatter fields inside template | 12-32 |
| `## Falsification standard` (inside template) | 80-82 |
| `## Evidence classification [V2 merged]` | 84-91 |
| `## Recommended evidence shape (v2.0 preview)` | 93-105 |
| `## Filling the card` | 118-123 |
| `## Worked example` (code block L127-154) | 125-154 |

| Spec anchor | Spec's description | Current line | Verbatim | Tag | `old_string` |
|---|---|---|---|---|---|
| `HCT:16-22` (baseline) | Claim class enum + glosses | 16-22 | L16 `**Claim class**: \`static_defect\` \| \`runtime_behavior\` \| \`environment_dependent\` \| \`config_value\` \| \`doc_contract\` \| \`mixed\`` | [CODE-VERIFIED] | n/a |
| `:19` (baseline) | `environment_dependent` gloss | 19 | `  — \`environment_dependent\`: claim depends on OS / runtime / feature-flag / network / data state` | [CODE-VERIFIED] | `claim depends on OS / runtime / feature-flag / network / data state` |
| `:76-82` (baseline) | "If I'm wrong" + Falsification standard | 76-82 | L76 `## If I'm wrong, it's probably because...`; L80 `## Falsification standard`; L82 `One sentence. What concrete evidence — an executable command and expected output, ... Runtime check self-scores ≤ 0.5.` | [CODE-VERIFIED] | `## Falsification standard` |
| `HCT:80-82` (R-07) | Falsification standard keeps one sentence; embed 2-hypothesis form when two mechanisms | 80-82 | as above | [CODE-VERIFIED] | insert after L82: `If you cannot name a falsification standard, the claim_class is \`runtime_behavior\` and Runtime check self-scores ≤ 0.5.` |
| `HCT:91` (R-07) | filling rule | 91 | `Filling rule: an empty or "Not applicable" value on \`evidence_class\` is a defect; cards with \`claim_class: runtime_behavior\` AND \`evidence_class ∈ {source_static, doc_static, none}\` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale.` | [CODE-VERIFIED] | `and state the cap in the rationale.` |
| `HCT:93-105` (R-07) | optional typed evidence table stays optional | 93-105 | L93 `## Recommended evidence shape (v2.0 preview)`; L105 `This shape is **OPTIONAL in v1.5** ...` | [CODE-VERIFIED] | n/a (unchanged) |
| R-01 `runs-in:` field | "card template gains a mandatory `runs-in:` field" — no line cited | — | frontmatter block L12-32; last field L32 `**Consistency with docs**: <aligned \| conflicts \| not_applicable \| no_docs_found>` | n/a (new) | `**Consistency with docs**: <aligned \| conflicts \| not_applicable \| no_docs_found>` (unique; worked example L130-133 lacks this field) |

## 5. `refs/escalation-rubric.md` (90 lines) — touched by R-08 (one rule at 63-69); `RUB:20` unchanged

| Heading | Lines |
|---|---|
| `## Confidence calibration (Wave 1.7)` (dimension table L11-18; formula L20) | 5-24 |
| `### Verdict-direction modifier (M3a)` | 26-35 |
| `### Claim-class × evidence-class cross-tab` | 37-50 |
| `## Escalation decision (Wave 2)` | 52-72 |
| `## Why 0.85?` | 74-78 |
| `## What escalation does NOT mean` | 80-82 |
| `## Diagnosability interaction` | 84-90 |

| Spec anchor | Spec's description | Current line | Verbatim | Tag | `old_string` |
|---|---|---|---|---|---|
| `RUB:18` (baseline) | Runtime check dimension row | 18 | `\| **Runtime check** \| Hypothesis includes an executed reproducer ...` | [CODE-VERIFIED] | n/a |
| `RUB:20` (R-14 Must NOT change) | formula | 20 | `**Confidence** = \`min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)\`.` | [CODE-VERIFIED] | n/a (unchanged) |
| `RUB:26-35`, `:37-50`, `:52-72` (baseline) | modifier / cross-tab / decision | as listed | headings above | [CODE-VERIFIED] | n/a |
| `:63-69` (R-08) | signal-driven escalation list; gains one rule | 63-69 | L63 `3. **Signal-driven escalation** (any one triggers escalation)`; L69 `   - \`claim_class ∈ {runtime_behavior, environment_dependent}\` AND \`runtime_check < 0.5\` → ESCALATE (\`escalation_reason: source_only_dynamic_claim\`).` | [CODE-VERIFIED] (L70 blank; L71 `4. **Default**`) | `(\`escalation_reason: source_only_dynamic_claim\`).` |
| `:35` (R-17 census) | "the H3 0.95-REFUTE case" | 35 | `Rationale: a wrong REFUTE on runtime behavior closes the investigation door (the H3 0.95-REFUTE case); ...` | NOTE: `H3` here = calibrator fixture name (Fixture 1 `fixture-h3-style.md`, eval-cases L7), NOT hardening gate H3. R-17's `\bH[0-5]\b` guard will hit it — exclude or rename separately. | n/a |

## 6. `refs/hardening-output-contract.md` (71 lines) — touched by R-16

| Heading | Lines |
|---|---|
| intro + enum sentence | 3-5 |
| `## Output contract field schema (§5.5)` (table L11-23) | 7-25 |
| `## Verdict aggregation truth table (§5.4)` | 27-41 |
| `## H5 decision-to-status mapping (§5.4)` | 43-50 |
| `## Downstream no-override rule` | 52-54 |
| `## Backtest status vs run-level verdict (§5.4)` | 56-64 |
| `## Waiver / no-re-greening latch and anti-inflation (FR-12)` | 66-71 |

| Spec anchor | Spec's description | Current line | Verbatim | Tag | `old_string` |
|---|---|---|---|---|---|
| `:5` (R-16, AP-20) | enum sentence | 5 | `\`pipeline_hardening_verdict\` is the **four-token** enum \`pass \| blocked \| advisory \| not_applicable\`. \`advisory\` is a first-class outcome and MUST NOT be removed: ... Any artifact that drops \`advisory\` or uses a three-token enum is a defect.` | [CODE-VERIFIED] — NOTE: says "**four-token**"; R-16 adds a 5th token so this word must change too. | `is the **four-token** enum \`pass \| blocked \| advisory \| not_applicable\`` |
| `:15` (R-16, AP-20) | schema table row | 15 | `\| \`pipeline_hardening_verdict\` \| enum \`pass\|blocked\|advisory\|not_applicable\` \| yes when applicable known \| \`not_applicable\` \| non-null \| aggregation \| Missing with applicable=true ⇒ \`blocked\` \|` | [CODE-VERIFIED] | `enum \`pass\|blocked\|advisory\|not_applicable\` \| yes when applicable known` |
| `:68` (R-16, AP-20) | one-way latch bullet | 68 | `- **One-way latch (\`waiver_status\`).** A waived or absent mandatory runtime probe sets \`waiver_status\` from \`none\` to \`latched\`. ... Once \`latched\`, \`pipeline_hardening_verdict ∈ {blocked, advisory}\` and no later \`task-builder\`, \`sc:reflect\`, or \`sc:adversarial\` stage may upgrade it to \`pass\`/\`success\`.` | [CODE-VERIFIED] | `- **One-way latch (\`waiver_status\`).**` |
| `:66-71` (baseline) | FR-12 section | 66-71 | L66 header … L71 `- **Anti-inflation.** ...` | [CODE-VERIFIED] | n/a |

Cross-file consistency for R-16: the same 4-token enum also lives at `SKILL:64` (Output Contract), `SKILL:420` (step 7), `report-template.md:223` (`**Closure verdict**: <pass\|blocked\|advisory\|not_applicable>`), and the truth table L31-39 here. Integration researcher covers consumers; listed here only because the enum string is the `old_string`.

## 7. `refs/report-template.md` (319 lines) — touched by R-10 (Diagnosis section), R-13 (rendering rules 255-260)

| Heading | Lines |
|---|---|
| `## Template` (code fence opens L7) | 5-253 |
| `## Diagnosis` (inside template) | 65-73 |
| `## Evidence` | 75-83 |
| `## Next Steps` | 146-154 |
| `## TFEP Consumer` | 156-168 |
| `### Hard-stop variant` (text block L174-206; cap paragraph L208) | 170-208 |
| `## Pipeline Hardening Closure` (inside template; H0-H5 status bullets L230-235) | 218-252 |
| `## Rendering rules` | 255-260 |
| `## Test-is-wrong rule` | 262-281 |
| `## Behavior-is-documented rule` | 283-308 |
| `## Pipeline Hardening Closure rule` | 310-319 |

| Spec anchor | Spec's description | Current line | Verbatim | Tag | `old_string` |
|---|---|---|---|---|---|
| `:170-206` (baseline) | hard-stop variant | 170-206 | L170 `### Hard-stop variant (when \`diagnosability_hard_stop=true\`)`; L206 closing fence | [CODE-VERIFIED] | n/a |
| `:255-260` (R-13) | rendering rules | 255-260 | L255 `## Rendering rules`; L257 `- **No trailing emoji or decorative headers.** ...`; L258 `- **Cite or drop.** Every \`file:line\` in the report must survive the Wave 5 validation pass.`; L259 `- **No reuse of the original error message in the Summary.** ...`; L260 `- **Status \`partial\` is honest.** Marking \`partial\` with a clear "Grounding Gaps" section is far better than marking \`success\` and being wrong.` | [CODE-VERIFIED] | append after: `is far better than marking \`success\` and being wrong.` |
| R-10 Diagnosis section (no line cited) | `UNDETERMINED — among {...}` prefix rule | 65-73 | L65 `## Diagnosis` (first occurrence inside template; a second `## Diagnosis`-like heading does not exist but `Diagnosis` appears in prose elsewhere) | n/a | `## Diagnosis` (occurrence 1) — verify uniqueness before Edit; grep shows only one `^## Diagnosis` heading |

## 8. `refs/calibrator-eval-cases.md` (81 lines) — R-19 landing path only

| Spec anchor | Current line | Verbatim | Tag |
|---|---|---|---|
| `:81` (R-19) | 81 | `Pytest harness invoking this corpus is OUT OF SCOPE for this brainstorm proposal. Expected landing path: \`tests/troubleshoot/test_calibrator_eval_cases.py\`.` | [CODE-VERIFIED] |
| `:7-55`, `:59-65` (baseline) | 7-55, 59-65 | Fixtures 1-9 (L7,13,19,24,29,35,42,47,52); property table P1-P5 L61-65 | [CODE-VERIFIED] |
| `:49`, `:54` (R-17 census) | 49, 54 | "Replays actual H2 card from T4" / "Replays actual H1 card from T4" — these `H1`/`H2` are T4 hypothesis-card labels, not hardening gates; R-17 regex false-positive | note |

## 9. `refs/runtime-entrypoint-verification.md` (47 lines) — R-01 Must-NOT duplicate; unchanged

| Spec anchor | Current line | Verbatim | Tag |
|---|---|---|---|
| `:13-24` (R-01) | 13-24 | L13 `\| Field \| Required \| Meaning \|`; L15 `\| \`producer\` \| yes \| ...`; L16 `\| \`transformers\` \| yes \| ...`; L17 `\| \`consumer_or_evaluator\` \| yes \| ...`; L24 `\| \`accepted_substitute_rationale\` \| ...` | [CODE-VERIFIED] (H1 card schema; read-only) |

## 10. `refs/remediation-handoff.md` (139 lines) — read-only baseline cite

| Spec anchor | Current line | Verbatim | Tag |
|---|---|---|---|
| `:42-48` (baseline; AP-12 "do not infer consent") | 42-48 | L42 `## Decision matrix`; L48 `\| Anything ambiguous \| Treat as "no" — do not infer consent \|` | [CODE-VERIFIED] |

## 11. `src/superclaude/agents/confidence-calibrator.md` (141 lines) — touched by R-14

**Frontmatter (L1-9)**: `name: confidence-calibrator` / `description` / `category: analysis` / `tools: Read` (L5) / `model: sonnet` (L6) / `maxTurns: 25` (L7) / `permissionMode: plan` (L8).

| Heading | Lines |
|---|---|
| `## Triggers` | 13-17 |
| `## Role` | 19-21 |
| `## Independence Instruction` | 23-27 |
| `## Claim-class handling` | 29-33 |
| `## Safety Constraint` | 35-37 |
| `## Behavioral Mindset` | 39-43 |
| `## Inputs` (bullets L47-51) | 45-51 |
| `## Responsibilities` (steps 1, 2, 2a, 3, 3a, 4, 5, 5a, 6 at L55-63) | 53-63 |
| `## Output Format` (code block L67-116) | 65-116 |
| `## Stage-2 trace (REQUIRED)` (inside block; table rows L90-96) | 86-96 |
| `## Notes` (inside block; bullets L113-115) | 111-115 |
| `## Boundaries` (`**Will:**` L120-125; `**Will Not:**` L127-134) | 118-134 |
| `## Failure Modes` | 136-141 |

| Spec anchor | Spec's description | Current line | Verbatim | Tag | `old_string` |
|---|---|---|---|---|---|
| `CAL:3` | description | 3 | `description: Independently re-grades a hypothesis card against a 5-dimension rubric ...` | [CODE-VERIFIED] (note: says "5-dimension" while L55 says "6 dimensions" — pre-existing inconsistency, out of scope) | n/a |
| `CAL:5` (R-14 Must NOT add Bash) | tools | 5 | `tools: Read` | [CODE-VERIFIED] | `tools: Read` (unchanged) |
| `CAL:5-8` | tools/model/maxTurns/permissionMode | 5-8 | as above | [CODE-VERIFIED] | n/a |
| `CAL:45-51` / `CAL:47-51` (R-14, R-13) | Inputs; add `card_mtime`, `behaviour_definitions_path`, `tasklist_path` | 45-51 | L45 `## Inputs`; L47 `- \`card_path\`: absolute path to the hypothesis card to score`; L51 `- \`output_path\`: where to write your calibration report` | [CODE-VERIFIED] | `- \`output_path\`: where to write your calibration report` (unique in CAL) |
| `CAL:53-63` | Responsibilities | 53-63 | L53 `## Responsibilities`; L63 `6. **Apply the escalation decision rules** ...` | [CODE-VERIFIED] | n/a |
| `CAL:58` (baseline) | spot-check step 3 | 58 | `3. **Spot-check the evidence**: for each \`file:line\` cited in the card, Read the file at that range and verify the snippet matches. ...` | [CODE-VERIFIED] | n/a |
| `CAL:62` (R-14) | step 5a; insert 5b after | 62 | `5a. **Apply the verdict-direction modifier** per the rubric: when \`claim_class: runtime_behavior\` and \`runtime_check < 1.0\`, cap calibrated at 0.70 (REFUTE/REJECT) or 0.84 (AFFIRM). Record whether the cap was binding in the Stage-2 trace.` | [CODE-VERIFIED] | `Record whether the cap was binding in the Stage-2 trace.` |
| `CAL:86-96` / `CAL:88-96` (R-14) | Stage-2 trace table; add `structural_flags` row | 86-96 | L86 `## Stage-2 trace (REQUIRED)`; L88 `\| Step \| Value \| Notes \|`; L95 `\| **calibrated** \| <X.XX> \| final \|`; L96 `\| spot_check_unverifiable \| <list of URLs> \| V2-merged WebFetch detection \|` | [CODE-VERIFIED] | `\| spot_check_unverifiable \| <list of URLs> \| V2-merged WebFetch detection \|` |
| `CAL:111-115` (R-14) | Notes section | 111-115 | L111 `## Notes`; L113 `- Any evidence the card cited that did not verify on spot-check ...`; L115 `- Any structural pathology in the card (missing required sections, malformed)` | [CODE-VERIFIED] | `- Any structural pathology in the card (missing required sections, malformed)` |
| `CAL:127-134` (R-14 unchanged) | Will Not | 127-134 | L127 `**Will Not:**`; L130 `- Re-write the card` | [CODE-VERIFIED] | n/a |
| `CAL:108` (R-14 side effect) | escalation Reason enum | 108 | `- **Reason**: \`none\` \| \`low_confidence\` \| \`multi_domain\` \| \`intermittent\` \| \`not_reproducible\` \| \`forced_by_depth_deep\` \| \`security_caution\`` | note: C1 "forced ESCALATE" may need a reason token; not cited by spec | n/a |

## 12. `src/superclaude/agents/evidence-validator.md` (128 lines) — touched by R-14

**Frontmatter (L1-9)**: `name: evidence-validator` / `description` / `category: quality` / `tools: Read, Grep, Glob` (L5) / `model: sonnet` (L6) / `maxTurns: 50` (L7) / `permissionMode: plan` (L8).

| Heading | Lines |
|---|---|
| `## Triggers` | 13-17 |
| `## Role` | 19-21 |
| `## Independence Instruction` | 23-25 |
| `## Safety Constraint` | 27-29 |
| `## Behavioral Mindset` | 31-35 |
| `## Inputs` (bullets L41-44) | 37-44 |
| `## Responsibilities` (step 1 L48-50; step 2 L51-55; step 3 L56-58; step 4 L59) | 46-59 |
| `## Output Format` (code block L63-97) | 61-97 |
| `## Status Decision` | 99-103 |
| `## Boundaries` (`**Will:**` L107-113; `**Will Not:**` L115-122) | 105-122 |
| `## Failure Modes` | 124-128 |

| Spec anchor | Spec's description | Current line | Verbatim | Tag | `old_string` |
|---|---|---|---|---|---|
| `VAL:5` | tools | 5 | `tools: Read, Grep, Glob` | [CODE-VERIFIED] | unchanged |
| `VAL:5-8` | frontmatter runtime fields | 5-8 | as above | [CODE-VERIFIED] | n/a |
| `VAL:37-44` / `VAL:41-44` (R-14) | Inputs; add `calibration_paths`, `diff_path`, `artifact_mtimes`, `producers_path`, `tasklist_path` | 37-44 | L37 `## Inputs`; L41 `- \`report_draft_path\`: absolute path to the draft \`REPORT.md\``; L44 `- \`allow_command_reexec\`: bool, whether you may re-run cited commands. ... (Current v1 of \`sc:troubleshoot-protocol\` always passes \`false\`.)` | [CODE-VERIFIED] | `(Current v1 of \`sc:troubleshoot-protocol\` always passes \`false\`.)` |
| `VAL:48-58` / `VAL:51-58` (R-14) | responsibilities 2-3; add 2b after citation verification | 48-58 | L51 `2. **For each \`file:line\` citation**:`; L55 `   - Verdict per citation: \`verified\` / \`line-mismatch\` / \`file-missing\` / \`snippet-mismatch\`.`; L56 `3. **For each command citation**:` | [CODE-VERIFIED] — 2b lands between L55 and L56 | `   - Verdict per citation: \`verified\` / \`line-mismatch\` / \`file-missing\` / \`snippet-mismatch\`.` |
| `VAL:58` (R-14 Must NOT add Bash) | "toolset deliberately excludes Bash" | 58 | `   - If \`allow_command_reexec=true\` AND the command is read-only (...): the orchestrator would have supplied Bash access. The current toolset deliberately excludes Bash for v1, so this branch is unreachable until a future revision adds Bash.` | [CODE-VERIFIED] | unchanged |
| `VAL:61-97` / `VAL:63-97` (R-14) | Output Format; add `## Structural assertions` table | 61-97 | L61 `## Output Format`; L63 opening fence; L92 `## Notes` (inside block); L96 `- Any draft input pathology (empty file, missing Evidence section).`; L97 closing fence | [CODE-VERIFIED] | insert before `## Notes` inside block: use `## Passed-through citations (command, allow_command_reexec=false)` … or after L96 `- Any draft input pathology (empty file, missing Evidence section).` |
| `VAL:99-103` (baseline) | Status Decision | 99-103 | L101 `- \`success\`: zero dropped citations.`; L102 `- \`partial\`: at least one dropped citation. ...` | [CODE-VERIFIED] | `- \`partial\`: at least one dropped citation.` |

## 13. `src/superclaude/agents/root-cause-analyst.md` (56 lines) — NOT touched by spec

**Frontmatter (L1-5)**: `name: root-cause-analyst` / `description: ...` / `category: analysis`. **CONFIRMED: no `tools:`, no `model:`, no `maxTurns:`, no `permissionMode:` keys** (L1-5 verbatim: `---`, `name`, `description`, `category`, `---`). Headings: `## Triggers` L9, `## Behavioral Mindset` L16, `## Focus Areas` L20, `## Key Actions` L28, `## Outputs` L36, `## Boundaries` L44 (`**Will:**` L46, `**Will Not:**` L52). Zero `\bH[0-5]\b` hits.

## 14. `src/superclaude/commands/troubleshoot.md` (204 lines) — touched by R-18

| Heading | Lines |
|---|---|
| frontmatter (`argument-hint` L8) | 1-9 |
| `## Triggers` | 13-22 |
| `## Required Input` | 24-33 |
| `## Usage` | 35-44 |
| `## Options` (table header L48; rows L50-60) | 46-60 |
| `## Behavioral Summary` (steps 1-4 at L66-69; tier table L73-77) | 62-77 |
| `## Activation` | 79-84 |
| `## MCP Integration` | 86-92 |
| `## Tool Coordination` (bullets L96-104) | 94-104 |
| `## Examples` | 106-156 |
| `## Boundaries` | 158-183 |
| `## CRITICAL BOUNDARIES` | 185-195 |
| `## Related Commands` | 197-204 |

| Spec anchor | Spec's description | Current line | Verbatim | Tag | `old_string` |
|---|---|---|---|---|---|
| `CMD:8` (R-18 unchanged, no new flag) | argument-hint | 8 | `argument-hint: "[<issue description>] [--type bug\|build\|performance\|deployment\|security\|test] [--depth quick\|standard\|deep] [--scope <path\|symbol>] [--no-escalate] [--fix] [--models <tier:model,...>] [--output-dir <path>] [--no-doc-discovery] [--no-mcp] [--context <path>] [--caller <name>]"` | [CODE-VERIFIED] | unchanged |
| `CMD:46-60` (task-prompt list) | Options table | 46-60 | L46 `## Options`; L48 `\| Flag \| Default \| Description \|`; L60 `\| \`--caller\` \| (none) \| ...` | [CODE-VERIFIED] (no `--no-diagnosability-audit` / `--diagnosability-handoff` / `--reset-diagnosability-rounds` rows here although SKILL:120 lists them — pre-existing gap, out of R-18 scope) | n/a |
| `CMD:69` (R-18) | step 4 "On skill return" | 69 | `4. **On skill return**, surface: REPORT path, tier reached, confidence, chosen fix, (if \`--fix\`) the Tier 3 remediation offer, and (if \`pipeline_hardening_applicable\`) the Pipeline Hardening Closure verdict + evidence-card paths, and (if \`caller=task-unified\`) the emitted \`return-contract.yaml\` path.` | [CODE-VERIFIED] — spec's replacement text is a superset (drops the two "and"s, appends grounding-artifacts clause) | `4. **On skill return**, surface:` (unique) — replace whole line |
| `CMD:103` (R-18) | Bash bullet | 103 | `- **\`Bash\`**: cheap reproducer commands (Tier 1) and diagnostic commands (Tier 2)` | [CODE-VERIFIED] | `- **\`Bash\`**: cheap reproducer commands (Tier 1) and diagnostic commands (Tier 2)` |

## 15. Refs the spec does NOT touch (out of scope for the builder)

| File | Lines | Notes |
|---|---|---|
| `refs/contract-enumeration.md` | 30 | H2 ledger; 5 `H[0-5]` hits (R-17 rename would touch it only via the regression-guard grep) |
| `refs/doc-discovery.md` | 182 | Wave 1.5; 0 H-hits |
| `refs/effective-input-proof.md` | 27 | H4; 4 H-hits |
| `refs/pipeline-hardening-closure.md` | 63 | H0/H5; 19 H-hits |
| `refs/unmask-and-sweep.md` | 52 | H3; 7 H-hits |
| `refs/remediation-handoff.md` | 139 | only read-only baseline cite `:42-48` |
| `refs/runtime-entrypoint-verification.md` | 47 | only a Must-NOT-duplicate cite `:13-24`; 6 H-hits |
| `refs/calibrator-eval-cases.md` | 81 | only `:81` landing path cite; T14 "fixtures 1-9 and P1-P5 unchanged" |

Spec says R-17 rename touches "`SKILL:104`, `:410-420`, `:595-600`; refs" — "refs" is unqualified. The H-token census below tells the builder exactly which ref files carry `H0`..`H5` tokens.

New files the spec creates (do not exist today — confirmed by `ls refs/`): `refs/primitive-differential.md`, `refs/environment-deltas.md` (optional), `refs/probe-packs/<kind>.md` (optional), `tests/troubleshoot/**`. `refs/runtime-probe-pack.md` and `refs/discriminator-template.md` do not exist (spec says they must not be created).

## 16. H-token census (R-17 regression guard baseline)

`grep -cE '\bH[0-5]\b'` at 2026-09-19:

| File | Hits | Lines |
|---|---|---|
| `SKILL.md` | 23 | 63, 64, 67, 68, 69, 70, 71, 104, 408, 410, 414-420, 444, 595, 597-600 |
| `refs/hardening-output-contract.md` | 20 | tables + FR-12 |
| `refs/pipeline-hardening-closure.md` | 19 | — |
| `refs/report-template.md` | 7 | 230-235 (status bullets), 316 |
| `refs/unmask-and-sweep.md` | 7 | — |
| `refs/runtime-entrypoint-verification.md` | 6 | — |
| `refs/contract-enumeration.md` | 5 | — |
| `refs/effective-input-proof.md` | 4 | — |
| `refs/calibrator-eval-cases.md` | 2 | 49 ("actual H2 card from T4"), 54 ("actual H1 card from T4") — FALSE POSITIVES: T4 hypothesis-card labels |
| `refs/escalation-rubric.md` | 1 | 35 ("the H3 0.95-REFUTE case") — FALSE POSITIVE: fixture label |
| `refs/diagnosability-audit.md`, `refs/doc-discovery.md`, `refs/hypothesis-card-template.md`, `refs/remediation-handoff.md`, `refs/triage-checklist.md`, `agents/*.md`, `commands/troubleshoot.md` | 0 | — |

Dash variants in SKILL: `H0–H5` (en-dash) L63/64/408/420/444; `H0-H5` (hyphen) L104; `H1–H5` L414. R-17's guard must count both. The spec's exemption "outside contract field names" covers `SKILL:63-71` descriptions only if the builder treats the *description column* as part of the field row; the field *names* themselves (`runtime_entrypoint_card_path` etc.) contain no H-token.

---

## Summary

**Status:** Complete

- Files inventoried: 19 (SKILL, 14 refs, 3 agents, 1 command). Line counts match the spec's 602-line SKILL baseline.
- Anchors checked: **~95** distinct line cites across SKILL/refs/CAL/VAL/CMD.
- [CODE-VERIFIED]: all but one. [CODE-CONTRADICTED]: **1** — `refs/diagnosability-audit.md:241` (task-prompt list) is a blank line; the hard-constraints header is L242 (the spec body itself correctly says `:242-247`). Three further "not-in-spec" cites from the task prompt (`SKILL:270/272`, `:276`, `:512`) verified structurally but the spec never cites them.
- Builder hazards found: (1) `SKILL:266` == `SKILL:570` byte-identical (3-round cap row) and `SKILL:262-264` == `:566-568`; (2) `SKILL:241` sentence has a lowercase near-twin at `SKILL:530`; (3) `diagnosability-audit.md:263` already contains `**Round**: <N> of 3` — spec's paste-ready header would duplicate it; (4) `hardening-output-contract.md:5` says "**four-token**" — must become five with R-16; (5) `\bH[0-5]\b` guard has 3 false positives (`escalation-rubric.md:35`, `calibrator-eval-cases.md:49,54`) that are fixture/T4 labels, not gates; (6) `diagnosability-audit.md:284` counter prose mirrors `SKILL:248` and should be aligned by R-04.
- `root-cause-analyst.md` frontmatter = `name`/`description`/`category` only — no `tools`, no `model` (confirmed L1-5).
