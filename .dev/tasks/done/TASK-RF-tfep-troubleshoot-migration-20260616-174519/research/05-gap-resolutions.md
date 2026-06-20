# Research: Gap Resolutions (orchestrator decisions closing A.8 gate gaps)

**Topic type:** Gap-fill / decision resolution
**Scope:** Resolve G1/G2/G3 raised by the A.8 gap-detection gate so the builder has no dangling decisions.
**Status:** Complete
**Date:** 2026-06-16

---

## G1 (IMPORTANT) — Remediation ownership decision [RESOLVED]

**Decision: Option 1 — `/sc:troubleshoot` authors the adapter `return-contract.yaml` when invoked with `--caller task-unified`.**

Rationale (matches the originating analysis recommendation): troubleshoot best understands its own
REPORT.md semantics (`test_is_wrong`, `behavior_is_documented`, tier_reached, confidence), so it should
map them into the TFEP-shaped contract. `/sc:task-protocol` remains the OWNER of: trigger detection,
freeze, context.yaml authoring, backend selection, consuming the contract, tasklist insertion, and resume.
Troubleshoot is invoked **for diagnosis only — TFEP does NOT pass `--fix`** (the analysis's step-4 decision):
remediation insertion + resume stay with task-protocol. This keeps the freeze invariant (step 6) intact.

**Split-ownership rule the tasklist encodes:** task-protocol owns *when* + *what-next*; troubleshoot owns
*how diagnosis is performed* + *emitting the adapter contract*.

**Builder instruction:** encode step-2 + step-5 items around Option 1. Record the alternative
(task-protocol derives the contract from REPORT.md) in the tasklist `### Open Questions` as a
non-blocking design note, not as an unmade decision.

## G2 (MINOR) — Incident-report artifact re-source mappings [RESOLVED]

The current incident template (sc-task-protocol/SKILL.md ~241–251) sources from forensic-only artifacts.
Re-bind to troubleshoot's REPORT.md sections:

| Old (forensic) field | New (troubleshoot) source |
|---|---|
| Root cause: summary from `rca-verdict.md` | Root cause: the **Diagnosis** section of troubleshoot `REPORT.md` |
| Solution: summary from `solution-verdict.md` | Solution: the **Proposed Fix / Next Steps** section of troubleshoot `REPORT.md` |
| Forensic artifacts: {path to output_dir} | Diagnostic artifacts: troubleshoot `report_path`, `audit_log_path`, hypothesis cards (Tier 2), adversarial artifacts (if any) |
| "committed to git alongside other forensic artifacts" (L253) | "committed to git alongside other diagnostic artifacts" |

**Builder instruction:** encode these as explicit per-line rename/rebind items under step 7.

## G3 (MINOR) — task.md:48 rule + rename convention + file-04 status [RESOLVED]

- **task.md:48 IS an edit target.** Rename the `--no-escalation` description from "structured forensic
  analysis" → "structured diagnostic escalation analysis" (keep the rest of the row verbatim). Add it to
  the step-1 rename worklist. The Boundaries/Activation TFEP mentions (task.md 161/175/176/186) reference
  "TFEP" not "forensic" — leave verbatim (no rename needed).
- **Per-token rename convention** (step 1), applied ONLY inside sc-task-protocol/SKILL.md §4.5 (133–261)
  and task.md:48 — NEVER touch `.dev/releases/archive/**` or `.dev/eval-workspaces/**` historical hits:
  - bare `forensic` (as the pipeline name) → `diagnostic escalation`
  - `/sc:forensic` (invocation) → `/sc:troubleshoot` with the translated flag string (see step 3/§02 research)
  - "the forensic pipeline" / "forensic tier" → "the diagnostic escalation backend" / "diagnostic depth"
  - "Forensic artifacts" → "Diagnostic artifacts"
  - keep `TFEP`, `context.yaml`, `return-contract.yaml` token names (they are structural, not backend-named)
  - "Escalation gradient (within-TFEP, for future forensic integration)" (L172) → drop "forensic", e.g.
    "(within-TFEP, for diagnostic-backend escalation)"
- **Post-rename verification:** `rg -n "/sc:forensic|\\bforensic\\b" src/superclaude/skills/sc-task-protocol/SKILL.md src/superclaude/commands/task.md` MUST return zero live hits; a repo-wide `rg "/sc:forensic" src/ docs/` should return only intentional historical/archive references (none expected under `src/`).
- **File 04 status header** (L3 "In Progress" vs L169 "Complete"): cosmetic intra-file drift in a research
  artifact; content is complete. No action required for the build (noted for completeness only).

## diagnostic_backend declaration value [RESOLVED — minor depth gap from research-depth lens]

Insert a single declaration line at the top of §4.5 (~line 136, single source of truth) reading:

```
**Diagnostic backend:** `troubleshoot` (the `/sc:troubleshoot` skill; see `sc:troubleshoot-protocol`). The TFEP
references below are backend-neutral — swapping the backend changes only this declaration and the invocation string.
```

## Net effect

All A.8 gate gaps (G1 IMPORTANT, G2/G3 MINOR) are now resolved with concrete builder instructions or
accepted as non-blocking Open Questions. The research corpus + these resolutions are sufficient for the
builder to produce a fully granular, self-contained Template-02 tasklist.
