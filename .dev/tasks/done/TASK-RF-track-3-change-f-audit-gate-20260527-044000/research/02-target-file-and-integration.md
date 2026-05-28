# Research 02: Target File State + Wave 3 Integration + Audit-Log/REPORT.md Conventions

**Date:** 2026-05-27
**Track:** 3 of 4 — folded researcher (Target File State + Wave 3 Integration + Audit-Log/REPORT.md Conventions)
**Status:** Complete

---

## Section 1 — File Metadata for SKILL.md

| Field | Value |
|-------|-------|
| Path (source-of-truth) | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` |
| Mirror (dev) | `.claude/skills/sc-troubleshoot-protocol/SKILL.md` (gitignored; produced by `make sync-dev`) |
| Line count | **456 lines** (matches research-notes; verified by Read length) |
| Purpose | Tiered debugging protocol (Tier 1 → Tier 2 parallel hypotheses → Tier 3 remediation chain). Allowed tools include `Task`, `Skill`, `Bash`, `Read`, `Write`, `Edit`, MCP servers (auggie, serena, context7, tavily, sequential). |
| Source-of-truth status | Edit only in `src/superclaude/skills/...`; sync via `make sync-dev`; verify via `make verify-sync` (per CLAUDE.md rule 6 + global memory `feedback_hooks_source_of_truth.md`). |
| Refs directory | `src/superclaude/skills/sc-troubleshoot-protocol/refs/` — 6 files: `doc-discovery.md`, `escalation-rubric.md`, `hypothesis-card-template.md`, `remediation-handoff.md`, `report-template.md`, `triage-checklist.md`. |

The skill body is the orchestrator's narrative — it tells Claude how to drive the wave sequence. There is no Python/CLI counterpart; the gate Change F adds is enforced at orchestrator runtime by the instructions written into this file.

---

## Section 2 — Structural Map of SKILL.md

Verified via `grep -nE "^## |^### " src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`:

| Heading | Line | Approx range |
|---------|------|--------------|
| `## Purpose` | 16 | 16-24 |
| `## Required Input (STOP if missing)` | 26 | 26-35 |
| `## Output Contract` | 37 | 37-72 |
| `## Wave Structure` | 73 | 73-88 |
| `### Wave 0: Parse + Validate Input` | 91 | 91-126 |
| `### Wave 1: Tier 1 — Real-Code Grounding` | 129 | 129-149 |
| `### Wave 1.5: Documentation Grounding` | 152 | 152-187 |
| `### Wave 1.7: Tier 1 — Hypothesis Formation` | 190 | 190-207 |
| `### Wave 2: Confidence Gate` | 210 | 210-227 |
| `### Wave 3: Tier 2 — Parallel Hypotheses` | **230** | **230-281** |
| `### Wave 4: Tier 2 — Adversarial Fix Debate` | 283 | 283-309 |
| `### Wave 5: Synthesis + Report` | 312 | 312-356 |
| `### Wave 6: Tier 3 — Remediation Chain` | 359 | 359-374 |
| `## Tool Coordination Summary` | 377 | 377-390 |
| `## Will Do` | 392 | 392-401 |
| `## Will Not Do` | 403 | 403-413 |
| `## Error Handling` | 415 | 415-432 |
| `## Token Cost Profile` | 434 | 434-443 |
| `## Refs` | 445 | 445-456 |

Wave 3's actual range is **L230-281** (L282 is blank; L283 is the Wave 4 heading). The research-notes' "L230-282" is off by one — the gate insertion happens before L282, not on it.

---

## Section 3 — Wave 3 Detailed Map

Wave 3 (L230-281) sub-structure:

| Subsection | Lines | Content |
|-----------|-------|---------|
| `### Wave 3` heading | 230 | `### Wave 3: Tier 2 — Parallel Hypotheses` |
| `**Goal**` | 232 | one-line goal |
| `**Preconditions**` | 234 | "Wave 2 decided to escalate." |
| `**Agent selection** ... table` | 236-247 | agent-picking rubric |
| `**Steps**:` header | 249 | (the numbered procedure begins) |
| Step 1 — MCP enrichment | 251-254 | parallel MCP calls |
| Step 2 — Spawn hypothesis agents | 255-261 | the `Task` fan-out; produces `<output-dir>/tier2-<agent-name>-hypothesis.md` (L259) |
| Step 3 — Wait + read cards | 262 | "Wait for all agents to complete. Read each card." |
| **Step 3.5 — Calibrate each card independently** | **263** | **the calibrator dispatch step** — spawn N `confidence-calibrator` instances in parallel, write to `<output-dir>/tier2-<agent-name>-calibration.md`. Has an inline fallback clause referencing Wave 1.7's rule. |
| Step 4 — Distill candidate fixes | 264 | cluster cards into consensus/competing/outlier |
| `**Exit criteria**:` | 266-269 | hypothesis card written + `candidate-fixes.md` index |
| `**Failure handling**:` table | 271-279 | table with 5 scenarios |
| (blank) | 280 | |
| `---` separator | 281 | hard rule before Wave 4 |
| (blank) | 282 | |
| Wave 4 heading | 283 | `### Wave 4: Tier 2 — Adversarial Fix Debate` |

**Critical observation:** the calibrator dispatch (Step 3.5, L263) is the dispatch step the spec references. The natural insertion point for the new "calibration completeness gate" is **after Step 3.5 completes and before Step 4 distills candidate fixes** — because Step 4 needs to know which cards have parseable calibrations (force-degraded cards still cluster, but with the suppressed confidence). The gate is conceptually a "Step 3.6" between calibration dispatch and consensus weighting.

Alternative placement: **immediately before "Exit criteria"** (L265), as a new step in the procedure list. This is structurally cleaner — it makes the gate the final precondition for Wave 3 emit — and matches the spec's framing as a "hard precondition for report publishing."

**Recommended anchor: after Step 4 (L264), before the blank line at L265, and before the `**Exit criteria**:` heading at L266.** This positions the gate as the last action Wave 3 takes before exiting — same wave as the calibration dispatch it gates, and the closest possible neighbor to the dispatch step without breaking the existing numbered flow.

---

## Section 4 — Insertion Anchor Candidate

The unique-match boundary for the Edit tool's `old_string` parameter should capture the seam between Step 4 and Exit criteria. Verbatim from the file (L264-266):

```
4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.

**Exit criteria**:
```

This 3-line slice (numbered step 4 + blank + `**Exit criteria**:`) is **unique in the file** — only Wave 3 has this exact sequence (other waves use different exit-criteria phrasing or different preceding-step content). A grep for `**Exit criteria**:` returns multiple hits, but combined with the unique step-4 prefix, the slice is unambiguous.

**Recommended `old_string` (paste-ready, exact whitespace, no leading indentation in the file):**

```text
4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.

**Exit criteria**:
```

The Edit tool replaces this with the same content prefixed by the new gate step (e.g., a `5. **Calibration completeness gate** — ...` block followed by the original `**Exit criteria**:`). Alternative: insert as Step 3.6, but renumbering Step 4 risks breaking refs from other files; appending as Step 5 leaves existing numbering intact.

---

## Section 5 — Run Output Directory Layout

Sourced from SKILL.md Wave 0 (output-dir creation) and Waves 1.5 / 1.7 / 3 (writes).

(a) **Output directory root:** computed in Wave 0 Step 4 (L107):
> `<output-dir>/` where `<output-dir>` = `<--output-dir>/<type-or-untyped>-<first-5-words>-<YYYYMMDDHHMMSS>`

All Wave 3 (and other-wave) writes are children of this single `<output-dir>`. There is **no per-card subdirectory** and **no separate `calibration/` subdirectory** in the current layout.

(b) **Hypothesis-card naming convention** — verified from L259 and L263:

| Spec wording (proposal) | Actual SKILL.md naming |
|-------------------------|------------------------|
| `tier2-h<N>-*.md` | **`tier2-<agent-name>-hypothesis.md`** (L259) |
| `tier2-h<N>-*-calibration.md` | **`tier2-<agent-name>-calibration.md`** (L263) |

**Gap flagged:** the proposal's `tier2-h<N>-*.md` shorthand is illustrative — the actual files are named after the agent (e.g., `tier2-root-cause-analyst-hypothesis.md`, `tier2-quality-engineer-hypothesis.md`), not by a numeric `h<N>` index. The task file MUST translate the spec's `tier2-h<N>-*-calibration.md` sibling pattern to `tier2-<agent-name>-calibration.md` for the implementation. The pairing relationship the spec describes (one calibration sibling per hypothesis card, same `tier2-<X>-` prefix) holds — only the glob suffix differs.

(c) **Calibration artifact location:** siblings in the same `<output-dir>` (not a subdirectory), with `-calibration.md` suffix replacing `-hypothesis.md`. The pairing is by stem: `tier2-root-cause-analyst-hypothesis.md` ↔ `tier2-root-cause-analyst-calibration.md`.

Related artifacts in the same directory:
- `tier1-hypothesis.md` (Wave 1.7 L202)
- `tier1-calibration.md` (Wave 1.7 L199, L202)
- `tier1-observation.md` (Wave 1 L146)
- `doc-context.md` + `wave1_5-branch-{A,B,C}.md` (Wave 1.5)
- `candidate-fixes.md` (Wave 3 exit criteria L269)
- `fix-proposals/fix-<N>.md` (Wave 4 L291)
- `adversarial/` subdirectory (Wave 4 L298)
- `evidence-validation.md` (Wave 5 L331)
- `REPORT.md` + `REPORT.md.draft` (Wave 5)
- `audit.log` (referenced throughout — see Section 6)

---

## Section 6 — audit.log Conventions

**Definitive references in SKILL.md:**

| Line | Context |
|------|---------|
| L46 | Output Contract field: `audit_log_path` — string, absolute path to `audit.log` |
| L50 | `test_file_path` description references "repo root recorded in the audit log" |
| L108 | Wave 0 Step 5: **"Open audit log; emit machine-readable header:"** followed by an HTML-comment-style fenced block `<!-- SC:TROUBLESHOOT:TARGET ... -->` |
| L123 | Wave 0 exit criteria: "audit log opened" |
| L140, L146 | Wave 1: "note the fallback in the audit log" / "captured in audit log" |
| L168 | Wave 1.5: "emit `doc_context_card_path: <output-dir>/doc-context.md` in the audit log" |
| L186 | Wave 1.5 token-budget overrun: "audit-log the overrun" |
| L200, L202 | Wave 1.7: `calibration: inline-fallback` marker in audit log |
| L226 | Wave 2: "record the `escalation_reason` in the audit log" |
| L304 | Wave 4: "Record the result in the audit log" |
| L333 | Wave 5 Step 4: **"Append the machine-readable footer to the audit log:"** followed by `<!-- SC:TROUBLESHOOT:SUMMARY ... -->` |
| L355 | Wave 5 exit: "audit log finalized" |
| L432 | Error Handling: `confidence-calibrator` fallback marks `calibration: inline-fallback` in audit log |

**Path:** `<output-dir>/audit.log` (inferred by symmetry with other `<output-dir>/...` artifacts; the only literal path reference is `audit_log_path` in the output contract, but Wave 0 implies it sits in the run's output directory).

**Format:** prose lines interspersed with HTML-comment-fenced machine-readable blocks. The opening header (Wave 0 L110-121) and closing footer (Wave 5 L335-346) are the only **structured** entries the SKILL.md prescribes. Everything else ("note in audit", "mark with `calibration: inline-fallback`", "record the result") is **free-form append** — the SKILL.md does not specify a field schema for inter-wave entries.

**Writer mechanism:** **not explicitly specified.** Wave 0 says "open audit log" and "emit ... header" — no tool is named. Given the orchestrator's allowed-tools list (`Bash`, `Write`, `Edit`), the most plausible append pattern is `Bash` with `printf >> <output-dir>/audit.log` or repeated `Edit`s. **The task file should NOT introduce a new convention** — Change F's new log entries (`calibration: missing`, retry attempts, force-degrade events) should be added as free-form append lines consistent with the existing pattern, e.g., one-line entries like:

```
calibration: missing card=tier2-quality-engineer-hypothesis.md attempt=1
calibration: retry card=tier2-quality-engineer-hypothesis.md timeout=120s
calibration: force_degraded card=tier2-quality-engineer-hypothesis.md self_reported=0.82 floored=0.65
```

**audit.log is NOT a new concept** introduced by Change F — it is already a first-class output-contract field (L46) and is written to by Waves 0, 1, 1.5, 1.7, 2, 4, 5. Change F adds **new log entries**, not a new log. The task file's setup instruction should reference the existing path convention without redefining it.

---

## Section 7 — REPORT.md Template / Assembly

**Definitive references in SKILL.md and `refs/report-template.md`:**

| Location | Content |
|----------|---------|
| SKILL.md L45 | Output Contract: `report_path` — string, absolute path to `REPORT.md` |
| SKILL.md L314 | Wave 5 goal: "Produce one diagnosis report at `<output-dir>/REPORT.md`" |
| SKILL.md L318 | Wave 5 Step 1: "Load `refs/report-template.md` (not before now — lazy load)" |
| SKILL.md L319-330 | Wave 5 Step 2: composes REPORT.md filling Header / Summary / Documentation Context / Diagnosis / Evidence / Proposed Fix / Alternative Fixes / Risk + Rollback / Next Steps |
| SKILL.md L331 | Wave 5 Step 3: `evidence-validator` agent validates citations; writes to `<output-dir>/REPORT.md.draft` then finalises |
| `refs/report-template.md` L1-141 | The literal markdown template with header fields, sectioned body, and rendering rules |

**REPORT.md card-entry schema** (from `refs/report-template.md` L8-21): the report is a **single document per run**, not one entry per hypothesis card. Hypothesis cards are not individually rendered into REPORT.md — only the **chosen** diagnosis is. The "Audit" section at the bottom (L134-140 of the template) lists hypothesis card paths but does not embed their content.

**Header fields (L9-21 of template):**

```
**Target**, **Type**, **Tier reached**, **Confidence**, **Status**, **Escalation reason**,
**Test is wrong**, **Test file to update**, **Behavior is documented**, **Doc context card**,
**Duration**, **Date**
```

**Slot for `calibration_status: failed_to_calibrate` annotation:**

The existing schema has **no field for per-card calibration status**. Two viable insertion points:

1. **Header field** — add `**Calibration status**: <ok|partial|failed_to_calibrate>` after `**Status**`. Pro: machine-readable, one line. Con: only one value for the whole report — loses per-card granularity.
2. **Audit section** (L134-140 of template) — extend the per-card listing to include a `calibration_status` per hypothesis card path. Pro: per-card fidelity. Con: schema change to a freeform section.
3. **Grounding Gaps** (L112-122) — append a line like "Hypothesis card from `<agent>` could not be calibrated after one retry — confidence force-degraded to `min(self_reported, 0.65)`." Pro: zero schema change; the section already accepts prose entries. Con: less structured for downstream parsing.

**Recommendation for Change F:** the spec's `calibration_status: failed_to_calibrate` annotation is a per-card concept. The least-disruptive integration is **Option 3 (Grounding Gaps prose line)** PLUS a **Confidence note** beside the report-level `**Confidence**` header field when any card was force-degraded (e.g., `**Confidence**: 0.65 (force-degraded — see Grounding Gaps)`). This requires **no schema change** to `refs/report-template.md`. If downstream automation later needs machine-readable per-card calibration status, a follow-up change can add it to the Audit section.

**Schema-change flag:** Change F's annotation as worded ("annotate `calibration_status: failed_to_calibrate` in REPORT.md") is **loose enough** to satisfy Option 3 without a schema bump, but the task file should document the chosen rendering so future readers of REPORT.md know where to look. The task should include a one-line update to `refs/report-template.md`'s Grounding Gaps examples block (L114-121) adding the new failure-mode example.

---

## Section 8 — Calibration Report Parsing Check

From `src/superclaude/agents/confidence-calibrator.md` L57-93 (Output Format section), a valid Calibration Report MUST contain:

| Element | Source line | Verification |
|---------|-------------|--------------|
| Top-level `# Calibration Report` heading | L59 | file starts with `# Calibration Report` |
| `**Card under calibration**:` metadata line | L61 | regex `\*\*Card under calibration\*\*:` present |
| `**Rubric**:` metadata line | L62 | regex `\*\*Rubric\*\*:` present |
| `**Card tier**:` metadata line | L63 | present |
| `**Timestamp**:` metadata line | L64 | present |
| `## Per-dimension scores` heading | L66 | section present |
| Per-dimension table with 5 rows (Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence) | L68-74 | 5 dimension labels present in table body |
| `## Confidence` heading | L76 | section present |
| `**Self-reported (in card)**:` line | L78 | self-reported numeric extractable |
| `**Calibrated (this report)**:` line | L79 | calibrated numeric extractable |
| `**Delta**:` line | L80 | present |
| `## Escalation recommendation` heading | L82 | section present |
| `**Verdict**:` line with `STOP` or `ESCALATE` | L84 | regex `\*\*Verdict\*\*:\s+\`?(STOP\|ESCALATE)\`?` |
| `**Reason**:` line | L85 | present |
| `**Rubric rule fired**:` line | L86 | present |
| `## Notes` heading | L88 | section present (may be empty) |

**Minimum viable check** (what the gate's "must parse as a Calibration Report" verification should enforce):

1. **File exists** at the expected `<output-dir>/tier2-<agent-name>-calibration.md` path AND is non-empty.
2. **Starts with** `# Calibration Report` (first non-blank line).
3. **Contains** `## Per-dimension scores` heading.
4. **Contains** `## Confidence` heading.
5. **Contains** `## Escalation recommendation` heading.
6. **Contains** `**Verdict**:` followed by either `STOP` or `ESCALATE` (case-sensitive, may be backtick-wrapped).
7. **Contains** `**Calibrated (this report)**:` followed by a parseable float in [0.0, 1.0].

If any of steps 1-7 fail, treat the calibration as `missing` (Change F's "missing" condition) and trigger the retry-then-force-degrade ladder.

This minimum check is **grep-able from Bash** — no markdown parser required. The gate can run a chain of `grep -q` invocations against each card's calibration sibling.

---

## Section 9 — Force-Degrade Math

**Formula from spec:** `confidence = min(self_reported, 0.65)`

**Edge cases:**

| Case | Expected behavior |
|------|-------------------|
| `self_reported = 0.82` | `min(0.82, 0.65) = 0.65` — degraded |
| `self_reported = 0.65` | `min(0.65, 0.65) = 0.65` — unchanged (already at floor) |
| `self_reported = 0.40` | `min(0.40, 0.65) = 0.40` — unchanged (below floor; honesty floor only caps high values) |
| `self_reported = 1.0` | `min(1.0, 0.65) = 0.65` — degraded |
| `self_reported = 0.0` | `min(0.0, 0.65) = 0.0` — unchanged |
| `self_reported = null` / missing | **AMBIGUOUS** — the formula does not define this case. **Recommended default:** treat missing self_reported as `0.0` so the final confidence floors at `0.0` (the most pessimistic safe default). Annotate `calibration_status: failed_to_calibrate, self_reported: missing` in the audit log. |
| `self_reported` is non-numeric (parse error) | Same as missing — treat as `0.0` with the parse-error noted in audit. |
| `self_reported > 1.0` (malformed card) | Clamp to `1.0` first, then apply `min(1.0, 0.65) = 0.65`. Annotate the clamp in audit. |
| `self_reported < 0.0` (malformed card) | Clamp to `0.0` first; result is `0.0`. Annotate. |

The hypothesis card's self-reported confidence field name is **not explicitly specified** in the SKILL.md or the calibrator agent (the calibrator reads it from the card per its L25 instruction: "Self-reported confidence on the card is a signal"). The hypothesis-card template at `refs/hypothesis-card-template.md` will define the actual field — that file should be read by the task executor to confirm the field name before implementing the parser. **Action for task:** include a "Read `refs/hypothesis-card-template.md` to confirm the `confidence` field shape" step in the implementation checklist.

---

## Section 10 — 2-Minute Extended Timeout Retry

**Research outcome:** The Claude Code `Task` tool does **not expose a per-spawn wall-clock timeout parameter**. Agent execution is bounded by **`maxTurns`** (set in the agent's frontmatter — `confidence-calibrator.md` L7 sets `maxTurns: 25`) and by orchestrator-side wait behavior. There is no `--timeout` flag on `Task` invocations.

**Implication for the spec's "2-minute extended timeout retry (one retry only)":**

The spec wording maps cleanly to one of three implementations:

1. **No timeout override; pure semantic retry** — orchestrator re-issues the same `Task` call with the same `maxTurns`, relying on the agent to complete within its own budget. The "2-minute extended" wording becomes documentation-only (a hint that the orchestrator should not hard-block waiting for the retry; it should accept up to 2 minutes of wall time before declaring the retry failed). This is the **cleanest match to the existing tool surface**.
2. **maxTurns bump for retry** — re-issue with a temporary `maxTurns` override (e.g., 35 instead of 25) to give the calibrator more headroom. But: `maxTurns` is set in the agent frontmatter, not the `Task` invocation — overriding requires either a per-call argument (which doesn't exist) or a duplicate agent file (e.g., `confidence-calibrator-extended`). **Not recommended** — adds maintenance burden.
3. **Wrap the retry in `Bash` with `timeout 120s`** — only works if the agent is exposed as a subprocess CLI; `Task` agents are not.

**Recommended encoding for task file:** the gate's retry step should say:

> "Re-dispatch the `confidence-calibrator` `Task` once for the missing card with the same inputs. Wait up to 2 minutes wall-clock for completion. If the retry does not produce a parseable Calibration Report within that window, proceed to the force-degrade step. Do not attempt a third retry."

This is implementable today with `Task` as-is — no new tool plumbing required. The "2-minute" budget is enforced by the orchestrator's wait loop, not by a timeout flag.

---

## Section 11 — Sibling-Artifact Naming Recommendation: Glob vs Bash

**Existing skill conventions for filesystem checks** (from SKILL.md):

| Pattern | Lines | Tool used |
|---------|-------|-----------|
| "fall back to `Glob` + `Grep` on the issue keywords" | L140 | Glob mentioned for fallback grounding |
| "Glob / Grep against the per-branch query targets" | L181, L421 | Glob/Grep paired in fallback handling |
| "fall back to `Grep`/`Glob` against the per-branch query targets" | L421 | Glob/Grep paired |
| Wave 0 Step 4 "create `<output-dir>/`" | L107 | implicit Bash (mkdir-style) |
| No explicit `Bash ls` or filesystem-verification pattern is named in any Wave | — | — |

**Allowed-tools list (L4):** `Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, ...` — both `Glob` and `Bash` are available.

**For the Change F gate "verification command (run before publishing)":**

- The verification needs to: (a) enumerate every `tier2-<agent-name>-hypothesis.md` in `<output-dir>/`, (b) check each has a sibling `tier2-<agent-name>-calibration.md`, (c) for each sibling, verify it parses as a Calibration Report (Section 8 checks).
- **Glob** handles (a) cleanly: `Glob` pattern `<output-dir>/tier2-*-hypothesis.md` returns the list. But Glob alone cannot do (b) sibling-existence check or (c) content parsing.
- **Bash** handles all three in one command (e.g., a `for f in tier2-*-hypothesis.md; do sibling="${f%-hypothesis.md}-calibration.md"; [[ -f "$sibling" ]] && grep -q "^# Calibration Report" "$sibling" && grep -q "^## Per-dimension scores" "$sibling" && ... || echo "missing: $f"; done`).

**Recommendation: Bash, with Glob as a pre-step option.** The existing skill uses Glob for **search/fallback** patterns, not for **verification gates**. A verification gate is closer in spirit to Wave 5's `evidence-validator` (which reads and parses) — that's Bash-shaped work. The spec's own wording ("Verification command (run before publishing)") implies a single command, which is Bash idiom.

**Concretely** — the gate's verification step in the SKILL.md insertion should be a Bash one-liner (single-line per global memory `feedback_no_multiline_paste.md`) or a short `Bash` block that:
1. lists `<output-dir>/tier2-*-hypothesis.md`
2. for each hypothesis card, derives the calibration sibling path
3. checks file existence and runs the 5-7 `grep -q` Calibration Report checks from Section 8
4. emits one audit-log line per missing/malformed calibration

If multiple Bash invocations would require multi-line commands (which the user's terminal cannot paste — see memory), the orchestrator should chain the steps via `&&` on a single line, or use a small inline Bash heredoc inside the SKILL.md instruction (the SKILL.md is read by Claude, not pasted by the user, so multi-line is acceptable INSIDE the skill body).

---

## Summary

- **Target file** is `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (456 lines, source-of-truth in `src/`, mirrored to `.claude/` via `make sync-dev`).
- **Wave 3 spans L230-281** (research-notes' "L230-282" is off by one; L282 is blank, L283 begins Wave 4).
- **Calibrator dispatch step** is Wave 3 **Step 3.5 at L263**; it writes calibration siblings to `<output-dir>/tier2-<agent-name>-calibration.md` and has an inline-fallback clause referencing Wave 1.7's rule (also captured in Error Handling table L432).
- **Recommended INSERT anchor**: after Wave 3 Step 4 (L264), before the blank at L265 and the `**Exit criteria**:` heading at L266 — positions the new "calibration completeness gate" as the last Wave 3 action before exit, immediately downstream of the calibration dispatch it gates.
- **Unique-match `old_string` slice** (3 lines): `4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.\n\n**Exit criteria**:`
- **Naming-convention gap flagged**: spec's `tier2-h<N>-*.md` shorthand is illustrative; actual files are `tier2-<agent-name>-hypothesis.md` ↔ `tier2-<agent-name>-calibration.md`. Task file must translate.
- **audit.log** is an existing first-class artifact (output-contract field L46; written to by Waves 0/1/1.5/1.7/2/4/5); Change F adds **new entries**, not a new log. Path is `<output-dir>/audit.log` (inferred by symmetry — only `audit_log_path` field is explicitly named).
- **REPORT.md** is one document per run (template at `refs/report-template.md`, 141 lines). Recommendation: render Change F's `calibration_status: failed_to_calibrate` annotation as a **Grounding Gaps prose line + Confidence header note** (zero schema change); optionally update the template's Grounding Gaps examples block (L114-121).
- **Calibration Report parsing minimum check**: 7 grep-able conditions (Section 8) — file exists, starts with `# Calibration Report`, has `## Per-dimension scores` / `## Confidence` / `## Escalation recommendation` headings, has `**Verdict**: STOP|ESCALATE`, has parseable `**Calibrated (this report)**: <float>`.
- **Force-degrade math** `min(self_reported, 0.65)` is well-defined for normal inputs; **missing self_reported** should default to `0.0` (most pessimistic safe value) with audit annotation. Hypothesis-card `confidence` field name must be confirmed from `refs/hypothesis-card-template.md`.
- **2-minute retry timeout** cannot be enforced via a `Task` flag (no such flag exists); implement as orchestrator-side wall-clock wait of up to 2 minutes for one re-issued `Task` call. "Extended timeout" wording is documentation-only.
- **Verification command tool choice**: **Bash** (with `Glob` optionally used to enumerate hypothesis cards) — matches the gate's content-parsing semantics and is consistent with Wave 5's `evidence-validator` pattern; existing skill uses Glob/Grep only for search/fallback, not for verification gates.

**Output file:** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-3-change-f-audit-gate-20260527-044000/research/02-target-file-and-integration.md`
