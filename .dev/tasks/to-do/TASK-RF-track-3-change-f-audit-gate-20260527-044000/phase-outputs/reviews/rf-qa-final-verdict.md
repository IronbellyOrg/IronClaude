# rf-qa FINAL_ONLY Task-Integrity Verdict — Change F

**Verdict:** PASS
**Date:** 2026-05-27
**Mode:** task-integrity (FINAL_ONLY gate)
**Adversarial stance:** Applied — every claim independently re-verified via Read/Grep/git diff against the actual file at L266-L277, not trusting any Phase 1-4 narrative.

---

## Adversarial Re-verification of 7 Points

### Point 1 — Structural placement inside Wave 3 (between L230 and L295, after L263 calibrator dispatch, before L278 Exit criteria)

**Evidence (independent grep):**

- `grep -n "^### Wave 3\|^### Wave 4" src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` → `230:### Wave 3:` … `295:### Wave 4:`.
- The new `#### Tier 2 calibration completeness gate (hard precondition for report publishing)` heading lands at **L266** — strictly between L230 (Wave 3 start) and L295 (Wave 4 start).
- L263 = step `3.5. Calibrate each card independently` (calibrator dispatch); L264 = step `4. Distill candidate fixes`; L266 = new gate heading; L278 = `**Exit criteria**:`. The gate sits **after** the calibrator dispatch (L263) and **before** the Exit criteria block (L278).
- Note: the spawn prompt's stated insertion target was "immediately after Step 4 (L264) and before the Exit criteria block (L278)" — the actual landing is at L266 (one blank line + heading after L264). This is correct: L265 is the blank-line separator. Structural intent satisfied.

**Verdict:** PASS

### Point 2 — Heading level exactly `####` with verbatim text

**Evidence:**

```
$ grep -n "^#### Tier 2 calibration completeness gate" src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
266:#### Tier 2 calibration completeness gate (hard precondition for report publishing)
```

- Hash count is exactly 4 (`####`), not 2/3/5.
- Heading text matches verbatim, including the parenthetical "(hard precondition for report publishing)".
- No `^##` (Wave-level) or `^###` (within-Wave-section-level) competing match for the same string.

**Verdict:** PASS

### Point 3 — All 4 MUST / MUST NOT / NEVER statements verbatim

**Evidence (grep on L266-L277 slice):**

```
MUST verify on disk
MUST exist and parse as a Calibration Report
MUST NOT publish
NEVER passed through unmodified
```

- L268: "the orchestrator MUST verify on disk" ✓
- L270: "MUST exist and parse as a Calibration Report (per the agent's Output Format)" ✓
- L271: "the orchestrator MUST NOT publish `REPORT.md` with the un-calibrated card's confidence" — note `REPORT.md` pairing is present ✓
- L274: "Self-reported confidence is NEVER passed through unmodified." ✓

All four statements present byte-verbatim within the new subsection. None occur outside the subsection in a way that would make this check a false positive (the `MUST verify on disk` / `MUST NOT publish REPORT.md` strings are unique to the new content).

**Verdict:** PASS

### Point 4 — 3-step ladder complete and correctly ordered

**Evidence (Read L272-L274):**

- **Step 1 (L272):** "Log `calibration: missing` for each missing sibling in `audit.log` with the absolute card path." ✓
- **Step 2 (L273):** "Re-dispatch the `confidence-calibrator` `Task` once for the missing card with the same inputs. Wait up to 2 minutes wall-clock for completion … Do not attempt a third retry." — explicit one-retry cap + 2-minute wall-clock wait + explicit no-third-retry, all present. ✓
- **Step 3 (L274):** force-degrade to `min(self_reported, 0.65)` + handles all four edge cases (missing/null/non-numeric/out-of-range) + clamp-then-floor ordering + `calibration_status: failed_to_calibrate` annotation + Grounding Gaps prose line + NEVER statement. ✓

Ordering is sequential and load-bearing (numbered 1./2./3.), not a checklist. Note the spec's L391-L394 has Step 2 as a single sentence ("one retry only"); the deliverable expands to "2-minute wall-clock wait, no third retry" which is a strict superset of the spec — not a deviation, a refinement. This is correct.

The deliverable also strengthens Step 3 beyond the spec's L393 by adding: explicit handling of `missing|null|non-numeric|out-of-range` edge cases, the `audit.log` annotation format, the Grounding Gaps prose line, and the clamp-then-floor semantics. All are non-conflicting refinements of the spec.

**Verdict:** PASS

### Point 5 — Verification command pattern (L276) with all 6 markers

**Evidence (Read L276):**

The line iterates over `tier2-*-hypothesis.md` (excluding `*-calibration.md`), asserts a matching `*-calibration.md` exists, and lists exactly these 6 Calibration Report markers:

1. `# Calibration Report` ✓
2. `## Per-dimension scores` ✓
3. `## Confidence` ✓
4. `## Escalation recommendation` ✓
5. `**Verdict**: STOP|ESCALATE` ✓
6. `**Calibrated (this report)**:` (with "a parseable float") ✓

Trigger clause "failure triggers the three-step ladder above" correctly back-references the L272-L274 ladder.

**Verdict:** PASS

### Point 6 — Zero `tier2-h<N>` remnants; correct `tier2-<agent-name>-*.md` forms

**Evidence:**

```
$ grep -n "tier2-h<N>\|tier2-h[0-9]" src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
(no matches)
```

- Zero occurrences of `tier2-h<N>` or `tier2-h0`/`tier2-h1`/etc. across the **entire file** — not just the new subsection.
- L270: `tier2-<agent-name>-hypothesis.md` ✓ and `tier2-<agent-name>-calibration.md` ✓ (correct agent-name form).
- L276: `tier2-*-hypothesis.md` ✓ and `*-calibration.md` ✓ (correct glob form).

The spec's L389/L395 used the stale `tier2-h<N>-*.md` / `tier2-h*.md` forms (V2 legacy convention). The deliverable's translation to `tier2-<agent-name>-*.md` is consistent with L259 (`tier2-<agent-name>-hypothesis.md`) and L263 (`tier2-<agent-name>-calibration.md`) which are pre-existing. This is correct naming-convention alignment.

**Verdict:** PASS

### Point 7 — `min(self_reported, 0.65)` paired with `calibration_status: failed_to_calibrate` in Step 3

**Evidence (Read L274):**

- `min(self_reported, 0.65)` appears in three forms within L274: the formula citation, the audit.log annotation `floored=0.65`, and the Grounding Gaps prose line "confidence force-degraded to min(self_reported, 0.65)". ✓
- `calibration_status: failed_to_calibrate` (and the equivalent `calibration_status=failed_to_calibrate` in the audit.log format) appears in: the audit.log annotation, the Grounding Gaps prose line, and the description of the REPORT.md annotation. ✓
- Both are confined to Step 3 of the ladder (L274), the correct step for the force-degrade path.

**Verdict:** PASS

---

## Findings

**No issues found at any severity** (CRITICAL: 0, IMPORTANT: 0, MINOR: 0).

The Change F insertion is structurally clean, content-complete relative to the spec at CROSS-ENV-PROPOSAL-MERGED.md L374-401, and demonstrably strengthens (rather than weakens or contradicts) the spec by adding edge-case handling for the force-degrade path, explicit retry timing, audit-log annotation format, and Grounding Gaps prose discipline.

---

## Phase 3 Blocker Assessment

**Independent verification of the "pre-existing" claim:**

```
$ git diff src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | head -100
```

The git diff shows ONLY a `+`-side insertion at the position corresponding to post-edit lines L266-L277 (12 added lines). The diff contains:

- One `+#### Tier 2 calibration completeness gate ...` heading line.
- One blank line.
- One prose paragraph + bullet list with 3 nested numbered items.
- One blank line.
- One verification-command prose line.
- One blank line.

**Zero new fenced code blocks** are introduced by the diff — every fenced block in the new content uses inline single-backtick formatting (e.g., `` `tier2-<agent-name>-hypothesis.md` ``, `` `min(self_reported, 0.65)` ``). I independently counted:

```
$ awk 'NR>=266 && NR<=277' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | grep -c '^```'
0
```

**Cross-check L75/L110/L306/L347 against gate boundary L266-L277:**

| Violating line | Inside gate (L266-L277)? |
|----------------|--------------------------|
| L75 | No — predates gate by 191 lines (Wave-structure ASCII block) |
| L110 | No — predates gate by 156 lines (Wave 0 audit-log block) |
| L306 | No — falls in Wave 4 (after L295), 29 lines after the gate ends |
| L347 | No — falls in Wave 5 (after L324), 70 lines after the gate ends |

**None** of the 4 MD040 violations fall inside the new gate subsection. The Phase 3 classification of "pre-existing, out-of-scope for Change F" is **correct and independently confirmed**.

The L306 and L347 line numbers in the post-edit file differ from their pre-edit positions by the ~12-line insertion offset — those fences existed before this change (verified: `markdownlint-summary.md` traces them to commits #70/#72/#73). The pre-commit hook did not flag them earlier because either the hook predates them or earlier commits bypassed the gate; this is a separate housekeeping concern.

**Recommendation:** Phase 3 blocker is correctly classified as out-of-scope for Change F. Follow-up housekeeping item (add `text` language hint to L75/L110/L306/L347) is appropriate and should be tracked separately.

---

## Mirror Parity Check

**Evidence:**

```
$ diff src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md .claude/skills/sc-troubleshoot-protocol/SKILL.md
(no output — files are byte-identical)
```

The `src/` source of truth and the `.claude/` dev mirror are **byte-identical**. `make sync-dev` has been run; mirror parity holds. Independent Read of `.claude/skills/sc-troubleshoot-protocol/SKILL.md` L260-L295 confirms the same gate subsection at the same line range with the same content.

**Verdict:** PASS (parity confirmed)

---

## Conclusion

**Final verdict: PASS.**

All 7 mandated re-verification points pass under adversarial re-checking with independent tool evidence (grep, Read, git diff, byte-level diff). Zero defects at any severity (CRITICAL, IMPORTANT, MINOR).

The Change F deliverable:

1. Lands structurally inside Wave 3 between the calibrator dispatch (L263) and the Exit criteria block (L278).
2. Uses the correct `####` heading level with verbatim title text.
3. Contains all 4 MUST / MUST NOT / NEVER statements verbatim.
4. Presents the complete 3-step retry-then-force-degrade ladder with strict ordering, one-retry cap, 2-minute wall-clock wait, no-third-retry guard, and all 4 edge cases for `self_reported`.
5. Includes the verification command pattern with all 6 Calibration Report markers.
6. Has zero `tier2-h<N>` stale remnants and uses the correct `tier2-<agent-name>-*.md` / `tier2-*-*.md` forms aligned with pre-existing L259/L263 conventions.
7. Pairs `min(self_reported, 0.65)` with `calibration_status: failed_to_calibrate` in Step 3 of the ladder.

The Phase 3 markdownlint blocker is independently confirmed as out-of-scope for Change F (pre-existing fences at L75/L110/L306/L347, none inside the new gate subsection at L266-L277, zero new fenced blocks introduced). The mirror parity check between `src/` and `.claude/` passes byte-identical.

**Recommendation:** Mark task as Done. Track the L75/L110/L306/L347 MD040 cleanup as a separate housekeeping follow-up.

---

## Confidence Gate Audit (zero-trust)

- **Verified:** 7/7 mandated points + 3 additional (markdownlint scope, mirror parity, git-diff cross-check) = **10/10**.
- **Unverifiable:** 0.
- **Unchecked:** 0.
- **Confidence:** 10/10 = 100% (well above 95% threshold).
- **Tool engagement:** Read: 5 | Grep: 7 (via bash grep) | Glob: 0 | Bash: 7 (diff/grep/awk/git-diff). Tool engagement (12 verifying calls) ≥ checklist items (10) — adequate.
- **Web research:** Not required for this gate (claims are all source-truth on local files).
- **Self-audit:** Could a verdict of "0 issues found" be defended to the user? Yes — every claim is backed by a specific grep/diff/Read output cited inline above. No item was marked verified by relying on the Phase 4 review files alone; every one was re-checked against the actual `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` content via independent tool call.
