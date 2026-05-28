# Research Output 01 — Change F Source Spec Extraction

**Track:** 3 of 4 (Change F — sc-troubleshoot-protocol Tier 2 audit-layer gate)
**Researcher:** spec-extraction
**Source:** `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` (main checkout), lines 374-401
**Status:** Complete

## 2. Paste-Ready Insertion Block (diff `+` markers stripped)

The proposal's diff sketch (L384-396) is a single insert. With each `+` and the single leading space stripped, the paste-ready block is:

```markdown
## Tier 2 calibration completeness gate (hard precondition for report publishing)

After all Tier 2 hypothesis cards are written and the calibrator subagents have been dispatched, the orchestrator MUST verify on disk:

- For every `tier2-h<N>-*.md` card written in this run's output directory, a sibling `tier2-h<N>-*-calibration.md` artifact MUST exist and parse as a Calibration Report (per the agent's Output Format).
- If any sibling calibration artifact is missing or malformed, the orchestrator MUST NOT publish `REPORT.md` with the un-calibrated card's confidence. Instead:
  - Log `calibration: missing` for each missing sibling in `audit.log` with the absolute card path.
  - Re-dispatch the calibrator subagent for the missing card with the same inputs and a 2-minute extended timeout (one retry only).
  - If retry still fails, write the card into `REPORT.md` with confidence force-degraded to `min(self_reported, 0.65)` and a `calibration_status: failed_to_calibrate` annotation on the card's REPORT.md entry. Self-reported confidence is NEVER passed through unmodified.

Verification command (run before publishing): for each `tier2-h*.md` (excluding `*-calibration.md`), assert a matching `*-calibration.md` exists or apply the force-degrade path.
```

**Note on heading level:** the proposal emits the subsection at `##` (H2). Wave 3 in the live skill is already an `###` (H3) subsection ("### Wave 3: Tier 2 — Parallel Hypotheses" at L230), so when inserting **inside** Wave 3 the heading level must be promoted to `####` (H4) to preserve nesting. The verbatim text of the heading "Tier 2 calibration completeness gate (hard precondition for report publishing)" is preserved unchanged; only the `#` count is adjusted. This deviation is unavoidable for structural consistency and should be flagged in the integration-points researcher's output (Researcher 4).

---

## 3. Anchor Decomposition (a)-(e)

Per task instructions, the block decomposes into 5 captured pieces:

### (a) Subsection heading (verbatim)

> `## Tier 2 calibration completeness gate (hard precondition for report publishing)`

(Proposal L385. Promote `##` → `####` on insertion per §2 note above.)

### (b) Intro paragraph (verbatim, proposal L387)

> "After all Tier 2 hypothesis cards are written and the calibrator subagents have been dispatched, the orchestrator MUST verify on disk:"

### (c) First bullet (verbatim, proposal L389)

> "For every `tier2-h<N>-*.md` card written in this run's output directory, a sibling `tier2-h<N>-*-calibration.md` artifact MUST exist and parse as a Calibration Report (per the agent's Output Format)."

### (d) Second bullet with 3 nested sub-bullets (verbatim, proposal L390-393)

Parent bullet:

> "If any sibling calibration artifact is missing or malformed, the orchestrator MUST NOT publish `REPORT.md` with the un-calibrated card's confidence. Instead:"

Sub-bullet (1) — audit log:

> "Log `calibration: missing` for each missing sibling in `audit.log` with the absolute card path."

Sub-bullet (2) — retry-once with extended timeout:

> "Re-dispatch the calibrator subagent for the missing card with the same inputs and a 2-minute extended timeout (one retry only)."

Sub-bullet (3) — force-degrade if retry fails:

> "If retry still fails, write the card into `REPORT.md` with confidence force-degraded to `min(self_reported, 0.65)` and a `calibration_status: failed_to_calibrate` annotation on the card's REPORT.md entry. Self-reported confidence is NEVER passed through unmodified."

### (e) Closing paragraph — verification command (verbatim, proposal L395)

> "Verification command (run before publishing): for each `tier2-h*.md` (excluding `*-calibration.md`), assert a matching `*-calibration.md` exists or apply the force-degrade path."

---

## 4. MUST / MUST NOT / NEVER Statements (verbatim, cited)

| # | Statement | Polarity | Location |
|---|-----------|----------|----------|
| 1 | "the orchestrator MUST verify on disk" | positive obligation | proposal L387 |
| 2 | "a sibling `tier2-h<N>-*-calibration.md` artifact MUST exist and parse as a Calibration Report (per the agent's Output Format)" | positive obligation (per-sibling) | proposal L389 |
| 3 | "the orchestrator MUST NOT publish `REPORT.md` with the un-calibrated card's confidence" | negative obligation | proposal L390 |
| 4 | "Self-reported confidence is NEVER passed through unmodified." | negative obligation (absolute, all-caps NEVER) | proposal L393 |

**Cross-reference (statement #4):** the same prohibition is restated in Change C's calibrator agent spec (per the task instructions). The audit-gate (Change F) is the orchestrator-side enforcement; the calibrator's Output Format (Change C) is the agent-side contract. Both must agree. Track 2 (Change C) owns the calibrator-side restatement; Track 3 (this track) owns the orchestrator-side gate that makes the prohibition observable.

---

## 5. The 3-Step Retry-Then-Force-Degrade Ladder

The second-bullet sub-bullets define a strict 3-step ladder triggered when *any* sibling calibration artifact is **missing or malformed**:

| Step | Action | Inputs | Side effects | Stopping condition |
|------|--------|--------|--------------|--------------------|
| 1. Log | "Log `calibration: missing` for each missing sibling in `audit.log` with the absolute card path." | absolute path to the un-calibrated `tier2-h<N>-*.md` card | append-only audit.log line | always runs; never blocking |
| 2. Retry once | "Re-dispatch the calibrator subagent for the missing card with the same inputs and a 2-minute extended timeout (one retry only)." | same inputs as original dispatch; timeout extended to 2 minutes | one additional calibrator subagent run | **one retry only** — no second retry permitted |
| 3. Force-degrade | "If retry still fails, write the card into `REPORT.md` with confidence force-degraded to `min(self_reported, 0.65)` and a `calibration_status: failed_to_calibrate` annotation on the card's REPORT.md entry. Self-reported confidence is NEVER passed through unmodified." | the un-calibrated card's self-reported confidence | REPORT.md entry includes degraded confidence + `calibration_status: failed_to_calibrate` annotation | terminal — card is published, but with degraded confidence and explicit failure annotation |

**Key invariants:**

- "one retry only" — the loop has a hard cap of 1 retry; there is no exponential backoff, no second attempt, no manual escalation step. Failure of step 2 deterministically triggers step 3.
- "2-minute extended timeout" — this is a per-spawn override, not the default calibrator timeout. The retry receives more wallclock budget than the original dispatch.
- "same inputs" — the retry is **idempotent** in spirit: identical card, identical context, identical agent definition. The only delta is the timeout.
- `min(self_reported, 0.65)` — strict floor on degradation. If the self-reported confidence was already ≤ 0.65, the value is unchanged; if higher (e.g. the original 0.95 / 0.85 self-reports from the T4 run), it is clamped to 0.65. The clamp is one-sided (never upgrades).
- `calibration_status: failed_to_calibrate` — explicit annotation on the REPORT.md entry, making the degradation observable to downstream readers (no silent pass-through).

---

## 6. Verification Command Pattern (closing paragraph)

Proposal L395 (verbatim):

> "Verification command (run before publishing): for each `tier2-h*.md` (excluding `*-calibration.md`), assert a matching `*-calibration.md` exists or apply the force-degrade path."

**Pattern decomposition:**

- **Trigger timing:** "run before publishing" — the gate is a *pre-publication* check, not a post-hoc audit. REPORT.md MUST NOT be written until this check passes (or the force-degrade ladder runs to completion).
- **Iteration scope:** "for each `tier2-h*.md`" — glob over tier-2 hypothesis cards in the run's output directory.
- **Exclusion:** "(excluding `*-calibration.md`)" — the glob must filter out the calibration sidecars themselves (otherwise the pair-matching trivially self-satisfies).
- **Assertion:** "assert a matching `*-calibration.md` exists" — pair matching by filename stem.
- **Fallback:** "or apply the force-degrade path" — failure of the assertion deterministically triggers the 3-step ladder from §5.

**Note on implementation choice (Glob vs Bash):** the proposal's wording is illustrative. Researcher 4 (wave3-integration) is responsible for choosing between `Glob` tool semantics and a literal `Bash` `ls`/`find` command, based on existing Wave 3 filesystem-check conventions. The spec only mandates the *behavior*, not the tool surface.

---

## 7. Rationale Block (verbatim, proposal L398)

> "**Rationale**: The empirical fact from the original T4 run is that `tier2-*-calibration.md` artifacts were absent — the calibrator did not execute and the 0.95 / 0.85 self-reports passed through unguarded. **No formula refinement closes this; only an audit gate does.** This is the most-load-bearing V2 contribution and the largest cross-environment finding: pr86 substrate could not surface this defect because pr86's substrate was a structural analogue, not the original artifact set."

**Rationale anchor points:**

- **Empirical evidence:** missing `tier2-*-calibration.md` sidecars in the T4 run.
- **Failure mode:** calibrator non-execution → self-reported confidences (0.95 / 0.85) passed through unguarded.
- **Closure claim:** "No formula refinement closes this; only an audit gate does." (Bolded in source.) This directly justifies why Changes A (rubric) / B (card) / C (calibrator scoring) do not on their own close Cause #1 — they all assume the calibrator *runs*. Change F is the only change that defends against the calibrator *not running*.
- **Load-bearing weight:** "the most-load-bearing V2 contribution and the largest cross-environment finding" — Change F is identified as the highest-impact item in the merged proposal.
- **Provenance pedigree:** "pr86 substrate could not surface this defect" — Change F originated in the V2 cross-env compare, not in the original pr86 brainstorm. The provenance tag `[V2 MERGED — closes Cause #1]` (L374) encodes this.

---

## 8. Cause → Fix Mapping (Cause #1 row, proposal L406)

From the Cause→Fix coverage matrix at L406:

> "| **Cause #1** — Calibrator non-execution (T4 dominant) | — | — | — | — | — | **direct closure** | **closes (V2-merged)** |"

**Interpretation:** Change F is the **only** change with non-empty cells against Cause #1. Changes A, B, C, D, E all show `—` (no contribution). Verdict column: "closes (V2-merged)".

This confirms the load-bearing claim from §7 — Cause #1 is closed exclusively by Change F.

---

## 9. Summary

This document extracts the Change F spec from `CROSS-ENV-PROPOSAL-MERGED.md` L374-401 into a paste-ready insertion block plus structured anchors. Key deliverables:

- **§2** — paste-ready markdown block (with heading-level promotion note `##` → `####` for Wave 3 nesting).
- **§3** — five named anchors (a)–(e) for downstream cross-reference: heading / intro / first-bullet / second-bullet+3-sub-bullets / verification-command-paragraph.
- **§4** — 4 normative statements captured verbatim with proposal line citations: 2 MUST (orchestrator-disk-verify; sibling-exists-and-parses), 1 MUST NOT (no REPORT.md publish with un-calibrated confidence), 1 NEVER (self-reported confidence never passed unmodified — also restated in Change C, owned by Track 2).
- **§5** — the 3-step ladder (Log → Retry-once-with-2-min-extended-timeout → Force-degrade-to-min(self_reported, 0.65)+annotate) with invariants: one retry only, idempotent inputs, one-sided clamp.
- **§6** — verification-command pattern decomposed: pre-publication trigger, glob-with-exclusion, pair-matching assertion, force-degrade fallback. Tool-surface choice (Glob vs Bash) deferred to Researcher 4.
- **§7** — Rationale captures the empirical anchor (missing T4 sidecars + 0.95/0.85 unguarded self-reports), the bolded closure claim ("only an audit gate does"), and the load-bearing/provenance pedigree.
- **§8** — Cause→Fix matrix confirms Change F is the sole closer of Cause #1.

**Provenance line for executor:** `[V2 MERGED — closes Cause #1]` (proposal L374) — migrated from V2's wrong `/config/.claude/skills/...` to the correct `src/superclaude/skills/...` SoT path (proposal L376). Executor MUST land edits in `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` then run `make sync-dev`.

**Out of scope (other Track 3 researchers):**

- Byte-level current state of SKILL.md Wave 3 + exact insertion anchor — Researcher 2 (target-file-state).
- Audit-log path/format and REPORT.md card-entry schema — Researcher 5 (audit-log-and-report).
- Glob-vs-Bash tool-surface choice for verification command — Researcher 4 (wave3-integration).
- Template 02 + Makefile + pre-commit conventions — Researcher 3 (template-conventions).

---

## 1. Provenance & Section Header

**Verbatim heading line (proposal L374):**

> `## Change F — `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (Tier 2 audit-layer gate) [V2 MERGED — closes Cause #1]`

**Provenance annotation (proposal L376):**

> `[Provenance: V2 Change 4 — migrated from V2's wrong `/config/.claude/skills/...` path to the correct `src/superclaude/skills/...` SoT path]`

**Section affected (proposal L378):**

> "Wave 3 / Tier 2 fan-out section, after the calibrator dispatch step."

**Shape (proposal L380):**

> "insert — new \"Tier 2 calibration completeness gate\" subsection."

Source-of-truth path is `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (the V2 path `/config/.claude/skills/...` is the dev-mirror, not the SoT). All edits must land in `src/superclaude/...` then `make sync-dev`.

---
