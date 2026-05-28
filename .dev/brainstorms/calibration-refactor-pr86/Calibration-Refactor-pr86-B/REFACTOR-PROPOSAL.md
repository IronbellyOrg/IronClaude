<!-- /sc:brainstorm --depth deep invocation -->
<!-- Skill name resolved: sc:brainstorm (routed to sc-brainstorm-protocol) -->
<!-- Input causes: FINAL-MERGED-CAUSES.md -->
<!-- Touched components: confidence-check skill, confidence-calibrator agent, escalation-rubric, hypothesis-card template -->

# Calibration-Failure Refactor Proposal — Smallest Closing Set

**Scope.** Close the H3-class miss: a Tier 2 REFUTE card with source-only evidence on a runtime-behavior claim scored 0.95 and bypassed audit. Constraint: minimum number of changes that closes the top causes in `FINAL-MERGED-CAUSES.md` without rebuilding the troubleshoot pipeline.

**Depth.** Deep — three proposal vectors (calibrator-hardening-first, rubric-restructure-first, schema-first) debated; convergence on schema-first as load-bearing because it makes the runtime-vs-static dimension *machine-readable*, which lets the calibrator enforce a hard cap mechanically rather than by narrative discipline.

---

## 1. Smallest closing set (6 changes)

### Change 1 — Add `evidence_class` + `claim_class` fields to the hypothesis-card template

- **File:** `/config/.claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`
- **Change kind:** modify
- **Exact text or behavior change:** Add two required frontmatter-style fields to the template header block (after `**Consistency with docs**`), and add a required new section `## Evidence classification` after `## Evidence`. Concrete additions:

  ```markdown
  **Claim class**: <runtime_behavior | static_defect | config_value | doc_contract | mixed>
  **Evidence class**: <runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none>
  ```

  And a new section the agent must fill:

  ```markdown
  ## Evidence classification

  - **Claim class**: <one of the five above> — <one-line reason>
  - **Evidence class**: <one of the six above> — <one-line reason>
  - **Runtime check performed?**: yes | no — <if no, one-line reason why not>
  - **If REFUTE verdict, coverage statement**: <which paths/files/conditions were inspected; explicitly name anything not inspected that could flip the verdict>
  ```

  Filling instructions block: an empty or "Not applicable" value on `evidence_class` is a defect; cards with `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale.

- **Closes:** Cause #2 (rubric evidence-class disjunction, generation layer) — makes the disjunction structurally visible; Cause #3 (refute-vs-confirm asymmetry, generation layer) — coverage statement forces REFUTE cards to enumerate uncovered paths.

- **Loophole-closure logic:** Today the H3 card could claim "Evidence grounding 1.0" with four GitHub source URLs and zero `zellij` invocations because the rubric's 1.0 anchor accepts source OR runtime. Once `claim_class` and `evidence_class` are required *machine-readable* fields, the contradiction (`claim_class: runtime_behavior` with `evidence_class: source_static`) is no longer hidden in prose — it is on the card as a typed field that downstream rules consume. The H3 card cannot be written truthfully under the new template without surfacing this mismatch.

### Change 2 — Add the runtime-vs-static alignment dimension to the escalation rubric

- **File:** `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`
- **Change kind:** modify
- **Exact text or behavior change:** Add a sixth dimension to the rubric table (between "Evidence grounding" and "Symptom coverage"). Update the "Confidence = arithmetic mean of the five dimension scores" line to say six. New dimension row:

  | Dimension | 1.0 (strong) | 0.5 (partial) | 0.0 (weak) |
  |-----------|--------------|---------------|------------|
  | **Claim/evidence alignment** | `claim_class` and `evidence_class` are aligned: runtime claim has runtime_repro or runtime_trace evidence; static claim has source_static or doc_static evidence | One-class drift: runtime claim has log_evidence only (post-hoc), or static claim has runtime_trace only (over-reach) | Mismatch: runtime_behavior claim with source_static / doc_static / none evidence; OR doc_contract claim with source-only evidence |

  Add a paragraph immediately after the table:

  > **Hard cap.** If "Claim/evidence alignment" scores 0.0, the rubric output confidence is capped at 0.65 regardless of the other five dimensions' average. This overrides the arithmetic mean. A 0.0 on this dimension means the card's evidence is structurally the wrong type for the claim — averaging cannot fix that.

- **Closes:** Cause #2 (rubric evidence-class disjunction); Cause #4 (anti-anchoring procedural deficit, design layer) — the cap is structural not procedural.

- **Loophole-closure logic:** Today H3 scores 1.0 on Evidence grounding under the disjunction and 0.95 overall. Under the new rubric, H3's claim_class is `runtime_behavior` (does `start_client_impl` early-return at runtime?) and its evidence_class is `source_static` (four WebFetched source files), so the new sixth dimension scores 0.0 and the hard cap of 0.65 engages — H3 cannot emerge above 0.65, well below the 0.85 STOP threshold. Forces escalation under rule 3 (`low_confidence`).

### Change 3 — Calibrator must enforce the hard cap and four named failure conditions

- **File:** `/config/.claude/agents/confidence-calibrator.md`
- **Change kind:** modify
- **Exact text or behavior change:** Insert a new section between "Independence Instruction" and "Safety Constraint":

  ```markdown
  ## Hard-fail conditions (mechanical, non-negotiable)

  Before computing the arithmetic mean, evaluate these in order. Each fires independently; a card can hit multiple. Surface every hit in the Notes section with the exact rule cited.

  1. **Runtime-claim / static-evidence mismatch.** If the card's `claim_class == runtime_behavior` AND the card's `evidence_class ∈ {source_static, doc_static, none}` AND no command output is shown in the Evidence section, cap final calibrated confidence at 0.65 and record `cap_reason: runtime_static_mismatch`. The "Claim/evidence alignment" dimension scores 0.0 in this case.

  2. **REFUTE-stronger-than-CONFIRM smell (wave-relative).** If this card's verdict is REFUTE with calibrated confidence > the highest sibling CONFIRM card's calibrated confidence in the same Tier 2 wave, require the card's "Risks" section to enumerate at least one specific file/condition not inspected. If it does not, cap at 0.75 and record `cap_reason: refute_asymmetry_unjustified`.

  3. **No-empirical-anything degrade.** If the Evidence section contains zero command outputs AND zero log excerpts AND zero reproducer steps (purely cited file:line and prose), the card is "all-static". Final calibrated confidence is degraded to min(computed, 0.75) and `cap_reason: no_empirical_evidence` is recorded.

  4. **Unverifiable-by-spot-check evidence.** If any evidence citation is a remote URL (e.g., `https://github.com/...`, `https://raw.githubusercontent.com/...`, or any URL the calibrator cannot Read), mark the calibration `spot_check: limited` in the Notes section with one line per unverifiable citation. Do not cap on this alone; the calibrator must explicitly state it cannot validate those citations.

  Rule precedence: lowest cap wins (e.g., if a card hits 1 and 3, the 0.65 cap from rule 1 wins). Caps replace the arithmetic mean if and only if the cap is lower than the mean.
  ```

  Also update the Output Format's Confidence block to add lines:

  ```markdown
  - **Hard-fail conditions hit**: <list of rule numbers, or "none">
  - **Cap applied**: <none | 0.65 | 0.75> — <cap_reason or "n/a">
  ```

- **Closes:** Cause #1 (calibrator non-execution) is not closed here (see Change 5 for the enforcement gate); but when the calibrator DOES run, it now closes Causes #2, #3, #4.

- **Loophole-closure logic:** The narrative-stripping defense at line 21 of the calibrator agent is *procedural* and the FINAL-MERGED §A-α already flags this. Replacing "score one dimension at a time" exhortation with four mechanical IF-THEN rules means an obedient calibrator cannot accidentally let an H3-class card through, even if its prose is exceptionally confident. The rules read the typed fields added in Change 1 and produce arithmetic caps — no narrative judgement involved.

### Change 4 — Audit-layer gate: troubleshoot protocol MUST refuse to publish a Tier 2 wave without all sibling calibration artifacts

- **File:** `/config/.claude/skills/sc-troubleshoot-protocol/SKILL.md`
- **Change kind:** modify
- **Exact text or behavior change:** Add (in the Wave 3 / Tier 2 fan-out section, near the post-calibration step) a hard precondition gate before the report is published:

  ```markdown
  ## Tier 2 calibration completeness gate (hard precondition for report publishing)

  After all Tier 2 hypothesis cards are written and the calibrator subagents have been dispatched, the orchestrator MUST verify on disk:

  - For every `tier2-h<N>-*.md` card written in this run's output directory, a sibling `tier2-h<N>-*-calibration.md` artifact MUST exist and parse as a Calibration Report (per the agent's Output Format).
  - If any sibling calibration artifact is missing or malformed, the orchestrator MUST NOT publish `REPORT.md` with the un-calibrated card's confidence. Instead:
    - Log `calibration: missing` for each missing sibling in `audit.log` with the absolute card path.
    - Re-dispatch the calibrator subagent for the missing card with the same inputs and a 2-minute extended timeout (one retry only).
    - If retry still fails, write the card into `REPORT.md` with confidence force-degraded to min(self_reported, 0.65) and a `calibration_status: failed_to_calibrate` annotation on the card's REPORT.md entry. Self-reported confidence is NEVER passed through unmodified.

  Verification command (run before publishing): for each `tier2-h*.md` (excluding `*-calibration.md`), assert a matching `*-calibration.md` exists or apply the force-degrade path.
  ```

- **Closes:** Cause #1 (calibrator non-execution, audit layer) — the dominant defect.

- **Loophole-closure logic:** The empirical fact from the run is that `tier2-*-calibration.md` artifacts are absent, which means the calibrator did not execute and the 0.95 / 0.85 self-reports passed through unguarded. Today nothing checks for that absence. A precondition gate on report-publishing converts "silently skipped" into "loud failure with force-degrade", making the audit layer self-policing. The force-degrade to 0.65 ensures that even a worst-case "calibrator crashed three times" run cannot ship a >0.85 confidence card.

### Change 5 — confidence-check skill gets a sixth check and a runtime-claim trigger note

- **File:** `/config/.claude/skills/confidence-check/SKILL.md`
- **Change kind:** modify
- **Exact text or behavior change:** Two edits.

  Edit 5a — add a sixth check to the "Confidence Assessment Criteria" section, rebalancing the weights so the new check is 15% and the original five sum to 85%:

  ```markdown
  ### 6. Runtime-vs-static evidence alignment? (15%)

  **Check**: For any claim about runtime behavior (CLI dispatch, PTY interaction, IPC, scheduling, async timing, environment-coupled behavior), the evidence must include at least one of:
  - A command + actual output from running the system
  - A captured log excerpt from the failing run
  - A reproducer the user or CI can execute

  Source reads, GitHub URL fetches, and documentation citations are NECESSARY but NOT SUFFICIENT for a runtime-behavior claim.

  ✅ Pass if claim is static AND evidence is static, OR claim is runtime AND evidence includes ≥1 runtime artifact
  ❌ Fail if claim is runtime AND evidence is source-only / doc-only / URL-only

  **Cap**: if this check fails, the overall confidence is capped at 0.65 regardless of the other five checks' sum. Source-only evidence on a runtime claim cannot achieve high confidence in this skill — period.
  ```

  Edit 5b — adjust the score weights line and the example output. Rebalance to: Check1 25→22%, Check2 25→22%, Check3 20→16%, Check4 15→13%, Check5 15→12%, Check6 NEW 15%. (Total 100%.) Update the "Confidence Score Calculation" math block to reflect six checks.

- **Closes:** Causes #2 and #4 at the pre-implementation surface (i.e., catches the same class of mistake when a developer is about to *act on* a recommendation, not only when calibrating a hypothesis card).

- **Loophole-closure logic:** Cause #2 is upstream of the troubleshoot pipeline — it also fires in everyday recommend/implement turns where a developer cites a source file and claims a runtime behavior follows. Mirroring the cap in the confidence-check skill itself means the same logic applies to plain confidence assertions in any reply, not just hypothesis cards. Defense in depth.

### Change 6 — Update `confidence.ts` to surface the runtime-vs-static cap

- **File:** `/config/.claude/skills/confidence-check/confidence.ts`
- **Change kind:** modify
- **Exact text or behavior change:** Add a sixth `Context` field, a sixth check method, and a cap-applying step in `assess()`.

  Concrete edits:

  - Add to `Context` interface: `claim_class?: 'runtime_behavior' | 'static_defect' | 'config_value' | 'doc_contract' | 'mixed';` and `evidence_class?: 'runtime_repro' | 'runtime_trace' | 'log_evidence' | 'source_static' | 'doc_static' | 'none';`
  - Add private method `runtimeStaticAligned(context: Context): boolean` returning `true` unless `claim_class === 'runtime_behavior'` AND `evidence_class ∈ {'source_static', 'doc_static', 'none'}`.
  - In `assess()`, add Check 6 contributing 15% on pass (with weight rebalance per Change 5b). Then, after computing the running `score`, apply the cap: `if (!this.runtimeStaticAligned(context)) { score = Math.min(score, 0.65); checks.push("⚠️ Runtime claim with static-only evidence — capped at 0.65"); }`.
  - Update `getRecommendation` boundaries are unchanged (still 0.9 / 0.7 thresholds); a capped 0.65 lands in the "STOP - continue investigation" bucket as desired.

- **Closes:** Causes #2 and #4 at the runtime/implementation surface (machine-enforced, not just documented).

- **Loophole-closure logic:** Documentation in SKILL.md is normative but a developer reading it may still skip the check. A code-level cap inside the skill's implementation ensures that any caller wiring `claim_class: 'runtime_behavior'` + `evidence_class: 'source_static'` into the context cannot get a >0.65 score back, no matter what the other five checks return. Mirrors Change 2's rubric cap one layer down.

**Count: 6 changes.**

---

## 2. Cross-cutting schema change — the runtime-vs-static evidence dimension

### Fields added to the hypothesis-card template (per Change 1)

- **Field name:** `claim_class`
  - **Allowed values:** `runtime_behavior | static_defect | config_value | doc_contract | mixed`
  - **Defaults:** none — required field; empty value is a card defect (calibrator scores Evidence-classification dimension 0.0 and notes the omission)

- **Field name:** `evidence_class`
  - **Allowed values:** `runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none`
  - **Defaults:** none — required field; same defect handling

- **Field name:** `runtime_check_performed` (yes/no + reason)
  - Required only when `claim_class == runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` — used to surface that the agent knowingly punted on runtime verification

- **Coverage statement** (REFUTE only)
  - Required only when verdict is REFUTE; agent must explicitly enumerate uncovered paths/files/conditions that could flip the refutation. Closes the negative-existential asymmetry from Cause #3.

### How the calibrator must use it

The calibrator's per-dimension scoring of the new "Claim/evidence alignment" dimension (Change 2) reads these typed fields directly:

- `claim_class == runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` → dimension scores **0.0** and the **hard cap of 0.65** applies (rubric Change 2 + calibrator rule 1 in Change 3).
- `claim_class == runtime_behavior` AND `evidence_class == log_evidence` → dimension scores **0.5** (post-hoc evidence, partial alignment).
- `claim_class == runtime_behavior` AND `evidence_class ∈ {runtime_repro, runtime_trace}` → dimension scores **1.0**.
- `claim_class == static_defect` AND `evidence_class ∈ {source_static, doc_static}` → dimension scores **1.0**.
- `claim_class == static_defect` AND `evidence_class ∈ {runtime_repro, runtime_trace}` → dimension scores **1.0** (over-evidenced is fine).
- `claim_class == doc_contract` AND `evidence_class == doc_static` → dimension scores **1.0**.
- `claim_class == mixed` → dimension scores the lower of the two component classes' scores.

### Where the cap is implemented

Three independent enforcement points (defense in depth, all small):

1. **Rubric file** — `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — the "Hard cap" paragraph after the dimension table (Change 2). This is the normative source.
2. **Calibrator agent prompt** — `/config/.claude/agents/confidence-calibrator.md` — Hard-fail condition #1 in the new section (Change 3). This is the operational enforcement during a troubleshoot run.
3. **Confidence-check code** — `/config/.claude/skills/confidence-check/confidence.ts::assess` — the `Math.min(score, 0.65)` step after Check 6 (Change 6). This is the code-level safety net for non-troubleshoot uses of the confidence skill.

All three implement the same predicate. Any future divergence is a bug, and the three locations are cross-referenced in their respective doc comments.

---

## 3. Calibrator hard-fail conditions

(Concrete detection rules referenced in Change 3.)

1. **Source-only evidence on runtime-behavior claim → cap at 0.65.**
   - **Detection:** Read the card's `Evidence classification` section. Predicate: `claim_class == "runtime_behavior" AND evidence_class IN {"source_static", "doc_static", "none"} AND no command-output blocks (text starting with "Command:" or fenced code blocks containing actual shell output) appear in the "## Evidence" section`.
   - **Action:** Set Claim/evidence alignment dimension to 0.0. Cap final confidence at 0.65. Notes section: `cap_applied: 0.65, cap_reason: runtime_static_mismatch`.

2. **REFUTE confidence > sibling CONFIRM in same Tier 2 wave (asymmetry smell).**
   - **Detection:** Card verdict is REFUTE; calibrated confidence of this card > calibrated confidence of any sibling card with verdict CONFIRM in the same wave (orchestrator passes sibling calibrations to the calibrator as `wave_siblings` input, OR if unavailable, the calibrator flags `wave_relative_check: skipped` and falls back to: "REFUTE confidence ≥ 0.85 AND Risks section does not enumerate any specific uncovered file/condition" → smell fires).
   - **Action:** If Risks section does not name at least one specific uncovered path/file/condition that could flip the refutation, cap at 0.75. Notes section: `cap_applied: 0.75, cap_reason: refute_asymmetry_unjustified`.

3. **No empirical evidence AND no diagnostic command output → degrade to <0.75.**
   - **Detection:** Evidence section contains zero lines matching `Command:` or fenced shell blocks AND zero log-excerpt blocks AND zero reproducer steps. All evidence is file:line citations and/or prose.
   - **Action:** Set final calibrated confidence to `min(computed_mean, 0.75)`. Notes section: `cap_applied: 0.75, cap_reason: no_empirical_evidence`.

4. **GitHub WebFetch URLs in evidence → mark "unverifiable by spot-check".**
   - **Detection:** Any line in Evidence section contains a URL matching `^https?://(raw\.)?github(?:usercontent)?\.com/.*` or any other URL the calibrator cannot Read locally.
   - **Action:** For each such citation, write a line in Notes: `spot_check_unverifiable: <url> — calibrator cannot validate this citation locally`. Do NOT cap on this alone (might combine with rule 1). Set `spot_check: limited` flag in the Confidence block. This forces the unverifiability to be visible in the calibration report rather than silently treated as verified.

5. **Negative-existential REFUTE without coverage enumeration → require justification.**
   - **Detection:** Card claim contains negative-existential language (regex: `\bno (?:[a-z]+ )*(?:exists|present|found|guard|early-return|special-case)\b` OR `\b(?:never|nowhere) (?:checks?|handles?|guards?)\b`) AND verdict is REFUTE AND the new `coverage_statement` field is empty or absent.
   - **Action:** Cap at 0.70. Notes section: `cap_applied: 0.70, cap_reason: negative_existential_no_coverage`. This is a specialization of rule 2 but stands separately because negative existentials are the worst REFUTE shape (Cause #3 specialization).

**Count: 5 hard-fail conditions.**

---

## 4. What this does NOT fix

Out of scope for this refactor (acknowledged from FINAL-MERGED-CAUSES.md):

- **Cause #5 — Agent-domain mismatch (assignment layer).** A `refactoring-expert` agent assigned a runtime CLI-dispatch hypothesis is an *orchestrator-side routing* problem. Fixing the calibrator and rubric makes a mismatched agent's output unable to score >0.65, which is good — but does not stop the mismatch from happening. The orchestrator-side fix (e.g., a routing table that refuses to assign `refactoring-expert` to a card whose `claim_class == runtime_behavior`) is a separate refactor in the Tier 2 fan-out logic of `sc-troubleshoot-protocol`. Not closed here.

- **A-α — "Rubric/calibrator is the right layer to fix."** This refactor accepts that assumption (rubric/calibrator-side fixes). The alternative — a pre-rubric verification gate that requires actual command output for any runtime claim before the card can be written at all — is structurally cleaner but a much larger change (rewrites the card-writing flow). Out of scope.

- **A-γ — Negative-existential cards being gradable.** Rule 5 above caps them at 0.70 but does not reject them at intake. The deeper fix — requiring conversion to a positive falsifiable form — would touch the hypothesis-card-template's "claim shape" rules and the agent prompts. Out of scope; capping is the smaller move.

- **A-δ — Rubric aggregation method (arithmetic mean).** This refactor adds caps that *override* the mean in specific cases but does not switch to worst-dimension-wins or geometric mean. Capping is the targeted intervention; switching aggregation is a broader policy change.

- **INV-003 — Rubric-version pin in audit log.** Adding `rubric_version` and `calibrator_version` lines to `audit.log` would make this refactor's effective version visible per run. Low blast radius; deferred — call it out as a follow-up if a second refactor wave happens.

- **Pre-implementation confidence-check on agents themselves.** The confidence-check skill changes (Changes 5 + 6) apply to manual / orchestrator-level confidence assertions. They do not automatically apply to in-flight Tier 2 agent self-reports — those flow through the calibrator. Both paths are covered by separate enforcement points (Changes 2/3 vs Changes 5/6) but the unification is left to a future cleanup.

---

## 5. Verification plan

Five concrete tests, in order of cheapness, each demonstrates one of the changes closes the H3-class miss.

### V1 — Replay the H3 card through the new calibrator (closes Change 2 + Change 3)

- **Action:** Tag the existing `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md` card. Add the missing schema fields manually (claim_class: runtime_behavior, evidence_class: source_static — both true to the card's actual evidence). Dispatch the *new* calibrator agent against it with the *new* rubric.
- **Pass criteria:** Calibration report MUST show `cap_applied: 0.65` with `cap_reason: runtime_static_mismatch`. Final calibrated confidence MUST be ≤ 0.65. Escalation verdict MUST be ESCALATE with reason `low_confidence`.
- **Why this matters:** The single most diagnostic test — the actual failing card must, after refactor, be caught by the new rules.

### V2 — Replay the H2 card through the new calibrator (closes Change 2 + Change 3 on REFUTE asymmetry)

- **Action:** Same as V1 with the H2 card. H2 has self-reported 0.85, REFUTE verdict, source-only WebFetch evidence on a runtime claim.
- **Pass criteria:** Either rule 1 (runtime-static mismatch) fires for a 0.65 cap, or rule 5 (negative-existential) fires for a 0.70 cap. Final calibrated confidence ≤ 0.70. The 0.85 self-report MUST NOT pass through.

### V3 — Replay the H1 card to confirm no over-correction (closes "we didn't break CONFIRM cards")

- **Action:** Replay H1 (0.82 self-reported, CONFIRM verdict, evidence mix of source reads + artifact log). Add fields: claim_class: runtime_behavior, evidence_class: log_evidence (the artifact log IS in the evidence).
- **Pass criteria:** New "Claim/evidence alignment" dimension scores 0.5 (log_evidence on runtime claim → partial). No hard cap fires (rule 1 requires evidence_class in {source_static, doc_static, none}, log_evidence is not in that set). Final calibrated confidence lands somewhere in 0.70–0.85 range and the H1 card escalates or stops by the rubric's normal rules — H1 should NOT be downgraded as a side effect.

### V4 — Audit-layer gate test (closes Change 4)

- **Action:** Run a synthetic troubleshoot pipeline that writes a Tier 2 card but skips the calibrator dispatch (simulate the original failure mode).
- **Pass criteria:** Orchestrator MUST refuse to publish REPORT.md with the un-calibrated card's self-reported confidence intact. Either it retries the calibrator once and succeeds, or it writes the card with confidence force-degraded to `min(self_reported, 0.65)` and `calibration_status: failed_to_calibrate`. The 0.95 / 0.85 pass-through that caused this failure MUST be structurally impossible.

### V5 — confidence-check skill unit test (closes Changes 5 + 6)

- **Action:** Add a test case to the confidence-check skill's existing test surface: a context with `claim_class: 'runtime_behavior'`, `evidence_class: 'source_static'`, and all five other checks passing.
- **Pass criteria:** `assess()` returns a value ≤ 0.65 (not the unmodified ≥0.90 the original five checks would yield). `getRecommendation()` returns the STOP message. Confirms the code-level cap engages.

**Acceptance.** All five MUST pass. V1 is the load-bearing test — if it passes, the dominant H3-class miss is structurally closed. V2–V5 are coverage / regression-prevention tests.

---

*End of refactor proposal. No file changes have been applied; this is proposal-only per the brief.*
