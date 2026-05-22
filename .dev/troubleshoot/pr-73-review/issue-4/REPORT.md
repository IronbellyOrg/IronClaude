# sc:troubleshoot REPORT — PR #73 review, issue 4

**Status**: success
**Tier reached**: 1 (quick; --depth quick)
**Confidence (calibrated, inline-fallback)**: 0.96
**Auto-apply**: NO (proposal only)
**Scope**: src/superclaude/skills/sc-troubleshoot-protocol/refs (+ SKILL.md Wave 1.5 step 4)
**Type**: bug (schema / contract gap)
**Issue**: Branch B output schema missing `summary` field requested by the Branch B query template and the Card template (auggie review comment 3290499067, severity medium).

---

## Symptom

The Wave 1.5 Documentation Context Card's "Architectural docs consulted" section is specified to render each Branch B finding as:

    - `<doc_path>` — verdict: `<current | stale | unknown>` — <one-line summary>

(refs/doc-discovery.md line 154)

…but the Branch B output schema (refs/doc-discovery.md lines 99-106) only defines three fields — `doc_path`, `currency_verdict`, `reason` — none of which carry the "2-3 sentence summary of the documented behavior" the Branch B query template explicitly asks the auggie agent to return (refs/doc-discovery.md line 26).

Consequence: the Wave 1.5 orchestrator's Section 4 synthesis (SKILL.md line 169 / step 4) has no schema slot to lift the summary from; the Card's `<one-line summary>` slot is structurally unfillable; downstream waves (1, 3, 4, 5) consuming the Card see verdicts but no documented-behavior summary, defeating Branch B's purpose.

---

## Grounding (Tier 1, native Read)

| Citation | Verified content |
|---|---|
| refs/doc-discovery.md:26 | Query asks for "the doc path, **a 2-3 sentence summary of the documented behavior**, and a currency verdict per the procedure in Section 2." |
| refs/doc-discovery.md:99-106 | Schema fields are exactly: `doc_path`, `currency_verdict`, `reason` (line 104 defines `reason` as "one-line rationale tied to Section 2 procedure" — currency-check rationale, NOT documented-behavior summary). |
| refs/doc-discovery.md:154 | Card format: `` - `<doc_path>` — verdict: `<current | stale | unknown>` — <one-line summary> `` — explicit summary slot. |
| SKILL.md:169 (Wave 1.5 step 4) | "merging... Branch B's architectural-doc list with currency verdicts (Section: Architectural docs consulted; surface CAUTION lines for stale / unknown verdicts)" — synthesis step renders the Card per Section 4, which needs `summary`. |
| refs/doc-discovery.md:84 (precedent) | Branch A schema already carries a top-level `summary` field; Branch B should mirror that shape. |

---

## Root cause

**Schema / contract gap.** Branch B's schema was authored with the currency-check feature in mind and re-used `reason` for the currency rationale, but no parallel `summary` field was added for the documented-behavior summary that the query template (line 26) requests and the Card template (line 154) consumes. The query and the Card agree; only the schema is out of sync.

`reason` is **not** a substitute for `summary`:
- `reason` → "why did the branch agent assign verdict X?" (Section 2 mtime / header markers)
- `summary` → "what does this doc actually say about <component_paths>?" (the documented behavior)

Both required, both must remain distinct.

---

## Proposed fix (do NOT auto-apply)

Single source-of-truth edit. Source: `src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md`. After editing, run `make sync-dev && make verify-sync` to propagate to `.claude/`.

### Change 1 (REQUIRED) — Add `summary` to the Branch B schema

**File**: `src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md`
**Location**: Section 3, Branch B schema block (lines 99-106).

**Replace**:

```json
[
  {
    "doc_path": "<absolute path>",
    "currency_verdict": "current",
    "reason": "<one-line rationale tied to Section 2 procedure>"
  }
]
```

**With**:

```json
[
  {
    "doc_path": "<absolute path>",
    "summary": "<2-3 sentence summary of the documented behavior of <component_paths>, per the Section 1 Branch B query>",
    "currency_verdict": "current",
    "reason": "<one-line rationale for the currency_verdict, tied to Section 2 procedure>"
  }
]
```

Rationale: adds the missing `summary` field requested by the line-26 query and rendered by the line-154 Card; tightens `reason`'s description to make explicit it is the currency-check rationale (not a behavior summary), preventing future conflation.

### Change 2 (RECOMMENDED) — Tighten the Card-template summary slot

**File**: same. **Location**: Section 4, line 154.

**Current**:

    - `<doc_path>` — verdict: `<current | stale | unknown>` — <one-line summary>

**Recommended**:

    - `<doc_path>` — verdict: `<current | stale | unknown>` — <one-line summary derived from the schema `summary` field>

Rationale: makes the Card→schema binding explicit so future edits cannot drift the two apart again. Optional — line-99 schema fix alone closes the bug; this is hardening.

### Change 3 — SKILL.md Wave 1.5 step 4 (NO EDIT NEEDED)

**File**: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, line 169.

Wave 1.5 step 4 reads "merging... Branch B's architectural-doc list with currency verdicts". It is silent on the summary because Section 4 of the ref is the authoritative Card template. With Change 1 in place, step 4 works as written (orchestrator pulls `summary` from the schema and drops it in the Card's summary slot). **No SKILL.md edit required**; doc-discovery.md is SoT for the Card structure.

Optional informational edit: append " — including the per-doc `summary` field from the Branch B schema" to the parenthetical at SKILL.md:169. Purely informational; not part of the required fix.

### Change 4 — Sync

After Changes 1 (required) and 2 (recommended):

    make sync-dev && make verify-sync

Per project rules, never edit `.claude/` directly.

---

## Why this is a Tier-1 finding

- Single-domain (schema contract), single-file edit, fully internally consistent: query template + Card template agree, only the schema disagrees. No external-library, runtime, or cross-component reasoning needed.
- Calibrated confidence 0.96. Drivers: every cited line was read directly; the gap is purely structural; the proposed fix is symmetric with Branch A's existing `summary` field (line 84), so no novel design.
- `--depth quick` suppresses Tier 2 by contract.

---

## Remediation chain (`--fix` was set)

Per sc:troubleshoot contract, the remediation chain is **offered but not executed**.

Paste-ready next step (operator's choice — direct Edit is also reasonable given ~4-line change):

    /sc:task-builder build a task to apply the Branch B schema fix in src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md (Changes 1 and 2 from /config/workspace/IronClaude/.dev/troubleshoot/pr-73-review/issue-4/REPORT.md), then run make sync-dev && make verify-sync, then re-run /sc:auggie-review on PR #73 to confirm the auggie finding 3290499067 is resolved

---

## Audit

- Tier 1 only (per `--depth quick`).
- Wave 1 grounding: native `Read` of src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md (full file) and SKILL.md lines 140-200. Auggie/serena not consulted (file:line evidence self-contained in the cited files).
- Wave 1.5 (doc-discovery): SKIPPED — meta-target is the doc-discovery ref itself; running it on its own broken schema would compound the issue.
- Wave 2: STOP at Tier 1 by `--depth quick`.
- Calibration: inline-fallback (no `confidence-calibrator` subprocess spawned in this fast-path).
- Evidence validation: every file:line cited was read in this session before being written into REPORT.md.
- File:line citations checked against the SoT path (src/superclaude/skills/sc-troubleshoot-protocol/...), not the .claude/ mirror.

## Grounding Gaps

- None material. Fix proposal grounded in directly-read source lines; Branch A schema (line 84) provides a working precedent for the proposed `summary` field shape.
