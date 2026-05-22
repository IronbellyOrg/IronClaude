# Tier 1 Hypothesis Card

**Issue:** Wave 1 hypothesis formation reads Documentation Context Card before Wave 1.5 produces it (PR #73 auggie review finding 3290499065, severity medium).

**Target file:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

## Claim

The Wave Structure code-block at lines 75-84 of `SKILL.md` lists `Wave 1` and `Wave 1.5` as **fully sequential sibling waves** (Wave 1 ends before Wave 1.5 begins), but the **content** of Wave 1 step 3 (line 144) requires the root-cause-analyst to consume `<output-dir>/doc-context.md` — a file that is **only produced by Wave 1.5 step 4** (line 169). Wave 1.5's stated goal (line 156: "BEFORE any hypothesis is formed") and its preconditions (line 158: "Wave 1 step 1 (real-code grounding) is complete") both clarify the intended **interleaved** sequencing (Wave 1 step 1 → Wave 1.5 → Wave 1 steps 2-3), but the Wave Structure block reads as sequential, so a reader implementing the protocol top-to-bottom would either:

1. Execute Wave 1 entirely first (steps 1-4) → fail at step 3 because `doc-context.md` doesn't exist yet, OR
2. Execute Wave 1.5 entirely first → conflict with the "Wave 1 step 1 is complete" precondition in Wave 1.5

This is a **sequencing ambiguity bug in the protocol documentation**, not a runtime defect. But because skill protocols are read top-to-bottom by Claude when the skill is invoked, the ambiguity will produce inconsistent execution: either a stale/empty card reference at Wave 1 step 3, or a precondition violation in Wave 1.5.

## Evidence

- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:75-84` — Wave Structure code-block listing Wave 1, then Wave 1.5, as siblings:
  ```
  Wave 0: Parse + Validate Input
  Wave 1: Tier 1 — Triage          ← always; loads refs/triage-checklist.md on demand
  Wave 1.5: Documentation Grounding ← always; loads refs/doc-discovery.md on demand; skipped only by --no-doc-discovery
  Wave 2: Confidence Gate          ...
  ```
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:144` — Wave 1 step 3 requires the Card as an input to the root-cause-analyst brief:
  > "spawn the `root-cause-analyst` agent via `Task` with a focused brief: the symptom, the grounding from step 1, the observation from step 2, **the Documentation Context Card path (`<output-dir>/doc-context.md`, or `null` when Wave 1.5 was skipped via `--no-doc-discovery`)**, and `--scope` if any."
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:156` — Wave 1.5 goal:
  > "Surface release-doc context, currency-validated architectural docs, and semantic restrictions that constrain the affected surface, **BEFORE any hypothesis is formed**."
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:158` — Wave 1.5 precondition:
  > "Wave 1 step 1 (real-code grounding) is complete; `--no-doc-discovery` is NOT set."
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:169` — Wave 1.5 step 4 writes the card:
  > "Synthesise the Documentation Context Card at `<output-dir>/doc-context.md` ..."

The internal contradiction is between lines 75-84 (sequential framing) and lines 144 + 158 (interleaved requirement).

## Proposed Fix

**Recommended (Option B from the hint — structurally cleaner):** Rename "Wave 1" to scope it to grounding only, and split hypothesis-formation into a new "Wave 1.7" that explicitly runs after Wave 1.5. This makes the dependency on the Documentation Context Card visually obvious in the Wave Structure block and removes the need for the reader to mentally interleave.

### Diff sketch

**1. Replace the Wave Structure code-block at `SKILL.md:75-84`** with:

```
Wave 0: Parse + Validate Input
Wave 1: Tier 1 — Real-Code Grounding    ← always; loads refs/triage-checklist.md on demand
Wave 1.5: Documentation Grounding       ← always; loads refs/doc-discovery.md on demand; skipped only by --no-doc-discovery
Wave 1.7: Tier 1 — Hypothesis Formation ← always; consumes the Wave 1.5 Documentation Context Card
Wave 2: Confidence Gate                  ← decides escalation via refs/escalation-rubric.md
Wave 3: Tier 2 — Parallel Hypotheses (conditional)
Wave 4: Tier 2 — Adversarial Fix Debate (conditional, requires ≥2 viable fixes)
Wave 5: Synthesis + Report               ← always finalises; loads refs/report-template.md
Wave 6: Tier 3 — Remediation Chain (conditional, requires --fix + user accept)
```

**2. Restructure the "Wave 1: Tier 1 — Triage" section (`SKILL.md:128-150`)** into two sections:

- **Wave 1: Tier 1 — Real-Code Grounding** keeps current step 1 ("Ground the symptom in real code") and current step 2 ("Reproduce or observe"). Goal becomes: "Ground the symptom in actual code and observed behavior; produce the inputs needed for Wave 1.5 and Wave 1.7." Exit criteria: grounding + observation captured in audit. Drop current step 3 and step 4 from this section.

- **Wave 1.7: Tier 1 — Hypothesis Formation** (new section, inserted between current Wave 1.5 and current Wave 2). Preconditions: "Wave 1 grounding + observation complete; Wave 1.5 Documentation Context Card written (or `--no-doc-discovery` set with `doc_context_card_path: null`)." Steps: current Wave 1 step 3 ("Form one hypothesis" — the root-cause-analyst spawn that already references the Card) and current Wave 1 step 4 ("Calibrate confidence"). Exit criteria: hypothesis card + calibration card written.

**3. Update cross-references** in `SKILL.md` that mention "Wave 1" as a hypothesis-producing wave:

- Line 17-18 / Purpose section: no change needed (talks about tiers, not waves).
- Tool Coordination Summary table (line 361-372): the `Task` row currently reads `✓ (root-cause-analyst + confidence-calibrator)` under Tier 1 — keep as-is; both agents still run in Tier 1, just now in Wave 1.7 not Wave 1.
- The Refs table (line 429-436): change `refs/hypothesis-card-template.md | Wave 1 and Wave 3` to `Wave 1.7 and Wave 3`. Change `refs/escalation-rubric.md | Wave 2 (confidence gate) and Wave 1 (calibration)` to `Wave 2 (confidence gate) and Wave 1.7 (calibration)`. Change `refs/triage-checklist.md | Wave 1 (passed to root-cause-analyst as part of the brief)` to `Wave 1.7 (passed to root-cause-analyst as part of the brief)`.
- Wave 1.5 precondition at line 158 (`Wave 1 step 1 (real-code grounding) is complete`) becomes `Wave 1 (real-code grounding) is complete`.
- The "Wave 1 complete: confidence=<x>" emit line (line 148) moves to the new Wave 1.7 exit criteria. Wave 1's new exit-criteria emit becomes "Wave 1 complete: grounding+observation captured".

**4. Don't forget the SoT discipline:** Edit `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (the source of truth in `src/`), then run `make sync-dev` and `make verify-sync` before staging. Per project CLAUDE.md, `.claude/skills/...` is gitignored sync output and must never be staged directly.

### Why Option B over Option A (move Wave 1.5 into the middle of Wave 1)

- Option A keeps the existing wave numbering but makes Wave 1 a non-contiguous block (steps 1-2, then a numbered sub-wave, then steps 3-4). Readers scanning the Wave Structure block still see two sequential entries and have to drill into Wave 1's body to discover the interleaving — i.e., the surface-level ambiguity that prompted the review finding **persists**.
- Option B makes the Card-dependency edge explicit at the Wave Structure level, where readers form their first mental model of the protocol. The cost is one extra wave name; the benefit is that the dependency graph is visible without reading any wave body.
- Option B is also consistent with the existing precedent of `Wave 1.5` as a "between" wave — adding `Wave 1.7` follows the same numbering convention and keeps the gap between integers (Wave 1, Wave 2) for future insertions.

## Confidence

**0.96** — calibrated inline against `refs/escalation-rubric.md` (5 dimensions):

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Evidence specificity | 0.98 | Three exact `file:line` citations, all verified by Read of the full source file; the contradiction is literal text-on-text |
| Reproducibility | 0.95 | Anyone reading `SKILL.md` top-to-bottom can observe the contradiction; doesn't depend on runtime state |
| Single-domain | 1.00 | Pure documentation-consistency bug; no cross-cutting concerns |
| Hypothesis exclusivity | 0.92 | Option B is the cleaner of two named alternatives; the user-provided hint endorses Option B; no third structurally-distinct alternative is obvious |
| Fix predictability | 0.95 | Diff is mechanical (rename + section split + 3-5 cross-ref updates) and contained within one file |

Mean: 0.96. Above the 0.85 Tier 1 STOP threshold and well above the 0.95 security-tier threshold (irrelevant here — this is `--type bug`).

## consistency_with_docs

`not_applicable` — Wave 1.5 was skipped because (a) `--depth quick` was specified and this is a doc-bug in the skill that defines Wave 1.5 itself; running Wave 1.5 against its own source would be circular, and (b) the issue *is* the doc, so the doc cannot serve as an external consistency check.

## Risks

- **Renumbering downstream consumers:** Any external file or memory that references "Wave 1" specifically as "the hypothesis-formation wave" will be wrong after the rename. Mitigation: grep for `Wave 1` across the repo (especially `src/superclaude/agents/root-cause-analyst.md`, `src/superclaude/agents/confidence-calibrator.md`, and any agent-memory MEMORY.md files) before merging; update mentions to point to `Wave 1.7`. Scope this in the task file as a checklist item.
- **Cosmetic-only fix risk:** If only the Wave Structure code-block is updated but the Wave 1 body still contains step 3 (hypothesis formation), the contradiction shifts location but does not resolve. The proposed diff MUST move the steps, not just rename the section heading.
- **Backwards compatibility:** Wave numbering is only a documentation-internal contract; nothing in the Python CLI parses wave numbers. No code-side breakage.

## If I'm wrong it's probably because...

...the design intent was actually Option A (interleave inside Wave 1) and the reviewer (or I) is misreading the Wave Structure code-block as a hard sequencing claim when the maintainers treat it as a checklist with sub-step interleaving documented in the bodies. In that case, the fix is purely a clarifying note inside the Wave Structure block (e.g., a footnote: "Wave 1.5 runs between Wave 1 step 1 and Wave 1 step 3") rather than a restructure. But the hint in the task explicitly endorses Option B as "structurally cleaner", so I am confident the restructure is the desired direction.
