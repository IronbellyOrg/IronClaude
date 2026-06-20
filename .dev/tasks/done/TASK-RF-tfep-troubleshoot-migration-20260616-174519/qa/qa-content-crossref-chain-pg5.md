# QA Report — Content Crossref-Chain (Phase 5, TFEP flow)

**Topic:** TFEP flow-chain crossref integrity — `sc-task-protocol/SKILL.md` §4.5
**Date:** 2026-06-16
**Phase:** doc-qualitative (crossref-chain lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Lens:** crossref-chain — trigger → freeze → context → dispatch → contract → insertion → resume

---

## Overall Verdict: FAIL

The TFEP chain has **6 broken/inconsistent links** (≥5 as the adversarial stance
predicted). The depth/enum core (standard/deep, none/retry/escalate_depth/halt) is
internally consistent and matches the troubleshoot contract — but the **dispatch
string, two cross-references, two dangling artifact filenames, and the entire
Escalation Budget block** are broken. A reader executing §4.5 literally cannot
resolve the `{context_path}` placeholder, is sent to the wrong step for the depth
mapping, and hits a backend (`/sc:forensic`) that contradicts the declared backend
(`/sc:troubleshoot`).

---

## Chain Trace (link-by-link)

| Link | From → To | Resolves? | Notes |
|------|-----------|-----------|-------|
| L0 | Trigger (Escalation Trigger Detection) → Step 1 freeze | YES | "When TFEP triggers, execute the following steps" → Step 1 STOP/FREEZE (L187-190) |
| L1 | Step 1 → Step 2 writes context.yaml | YES | `{output_dir}/context.yaml` (L205) |
| L2 | Step 2 context.yaml → Step 3 `--context {context_path}` | **NO (C1)** | Dispatch references `{context_path}`; Step 2 wrote `context.yaml`. Placeholder never bound. |
| L3 | Step 3 `{depth}` → tier→depth mapping (standard/deep) | YES (value) / **NO (ref, C2)** | Values standard/deep, no `quick`. But L215 says "the **Step 5** mapping above" — mapping is in **Step 3** (L208-213). |
| L4 | Step 3 dispatch → Step 4 contract read | YES | `{output_dir}/return-contract.yaml` (L219) matches troubleshoot Wave 5 emission (troubleshoot L471). |
| L5 | Step 4 enum (none/retry/escalate_depth/halt) → contract | YES | Exact match to troubleshoot contract `recommended_escalation` (troubleshoot L73). |
| L6 | Step 4 `escalate_depth` → `--depth deep` vs mapping | YES | deep is the deepest mapping value; escalate→deep is coherent (L226). |
| L7 | Step 4 "proceed to Step 5" → Step 5 | YES | Step 5 exists (L229). |
| L8 | Step 4 retry/escalate "re-run /sc:troubleshoot" → re-enter Step 3 | PARTIAL (C6) | Coherent action-wise, but never states "return to Step 3"; contrast Step 6 L242 which explicitly says "return to Step 2". |
| L9 | Step 5 `tasklist_insertion_path` + summary fields + Adjudicated heading | YES | All three contract fields + heading resolve (contract L74-77; troubleshoot L471). |
| L10 | Step 6 resume → inserted remediation tasks | YES | "starting from the inserted remediation tasks" (L239) → Step 5 insertion. |
| L11 | Incident report → rca-verdict.md / solution-verdict.md | **NO (C3)** | Troubleshoot emits `REPORT.md`, not those filenames. |
| L12 | Escalation Budget → backend `/sc:forensic --tier light/standard` | **NO (C4, C5)** | Declared backend is `/sc:troubleshoot` with `--depth standard\|deep`. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| C1 | CRITICAL | §4.5 Step 3, L215 (vs Step 2 L205) | Unbound placeholder: dispatch passes `--context {context_path}` but Step 2 writes `{output_dir}/context.yaml`. `{context_path}` is never defined or bound to the written file. A literal executor cannot resolve it. | Bind it: either write Step 2 as `{context_path} = {output_dir}/context.yaml` and reference that, or change the dispatch to `--context {output_dir}/context.yaml`. Make the producer (Step 2) and consumer (Step 3) name the same token. |
| C2 | IMPORTANT | §4.5 Step 3, L215 | Wrong cross-reference: "where `{depth}` is determined by the **Step 5** mapping above". The tier→depth mapping is in **Step 3** itself (L208-213). Step 5 is "Tasklist insertion" — no depth mapping. Misleads the reader to the wrong step. | Change "the Step 5 mapping above" → "the Step 3 mapping above" (or "the depth mapping in step 5 of this Step 3" — but the numbered bullet is item 5 *within Step 3*; the prose "Step 5" collides with the document's Step 5 heading). Safest: "the depth mapping in the bullets above (this step)". |
| C3 | IMPORTANT | §4.5 Incident Reporting, L254-255 | Dangling artifact references: `{summary from rca-verdict.md}` and `{summary from solution-verdict.md}`. The declared backend (`/sc:troubleshoot`) emits `REPORT.md` (Diagnosis / Proposed Fix sections) and `return-contract.yaml` — not `rca-verdict.md` / `solution-verdict.md`. Those filenames are stale (likely from a prior forensic-backed design). | Replace with the actual contract sources: Root cause → `root_cause_summary` (from return-contract.yaml / REPORT.md Diagnosis); Solution → `solution_summary` (from return-contract.yaml / REPORT.md Proposed Fix). |
| C4 | CRITICAL | §4.5 Escalation Budget, L265-267 | Backend contradiction: the Escalation Budget routes to `/sc:forensic --tier light` / `--tier standard`, but L137 declares the diagnostic backend as `troubleshoot` (`/sc:troubleshoot`) and the entire Execution Flow (Steps 3-6) invokes `/sc:troubleshoot`. `/sc:forensic` appears nowhere else in the chain. The two halves of §4.5 disagree on which skill runs. | Rewrite the Escalation Budget to use the declared backend: `1st → /sc:troubleshoot --depth standard`; `2nd → /sc:troubleshoot --depth deep`; `3rd → FULL STOP`. (This is the "swapping the backend changes only this declaration and the invocation string" promise from L137 — the budget block was not updated when the backend was swapped to troubleshoot.) |
| C5 | IMPORTANT | §4.5 Escalation Budget, L265-266 | Enum contradiction co-located with C4: budget uses `--tier light` / `--tier standard`, but the dispatch + mapping use `--depth standard` / `--depth deep`. Even after the backend name is fixed, the flag (`--tier` vs `--depth`) and the 1st-trigger value (`light` vs `standard`) must be reconciled. Step 3 maps 1st trigger → `--depth standard`; budget maps 1st trigger → `--tier light`. | Align to the dispatch: 1st → `--depth standard`, 2nd → `--depth deep`. Drop `--tier`; the troubleshoot backend has no `--tier` flag (it parses `--depth quick\|standard\|deep\|auto`, troubleshoot L137). |
| C6 | MINOR | §4.5 Step 4, L225-226 | Loose loop-back: retry/escalate_depth say "re-run/re-invoke /sc:troubleshoot" but never name the step to return to. Step 6 (L242) explicitly says "return to Step 2", so the protocol elsewhere uses explicit step-return language. The retry path leaves the re-entry point implicit (it is the Step 3 dispatch action). | Add "(re-enter Step 3)" to the retry and escalate_depth branches for symmetry with Step 6's "return to Step 2", and to make the re-run's `--depth`/`--context` inputs unambiguous. |

---

## Consistency checks that PASSED (evidence the chain was actually traced)

- **No `quick` contamination in the depth mapping.** Step 3 bullets (L210-212) and the
  dispatch prose (L215) use only `standard` / `deep`. `quick` appears in the troubleshoot
  backend's flag surface (troubleshoot L137 `<quick|standard|deep|auto>`) but is correctly
  NOT referenced anywhere in the §4.5 TFEP mapping. PASS.
- **Step 4 enum exact-match.** `none|retry|escalate_depth|halt` (task-protocol L224-227)
  is byte-identical to the troubleshoot Output Contract `recommended_escalation` enum
  (troubleshoot L73). PASS.
- **`escalate_depth → --depth deep` is monotonic.** deep is the deepest value in the
  mapping; escalating to deep (L226) is consistent. There is no value deeper than deep,
  so escalate_depth from an already-deep run correctly has no further depth — consistent
  with the `halt` / 3rd-trigger FULL STOP path. PASS.
- **Step 5 contract-field references all resolve.** `tasklist_insertion_path` (L230),
  `remediation_target` / `root_cause_summary` / `solution_summary` (L233), and the
  `## Failure Remediation Plan (Adjudicated)` heading (L232) all map to real troubleshoot
  contract fields (contract L74-77) emitted by Wave 5 (troubleshoot L471). PASS.
- **Step 6 resume target resolves.** "starting from the inserted remediation tasks"
  (L239) correctly points at Step 5's insertion. PASS.
- **return-contract.yaml producer/consumer agree.** task-protocol reads
  `{output_dir}/return-contract.yaml` (L219); troubleshoot writes
  `<output-dir>/return-contract.yaml` when `caller=task-unified` (troubleshoot L471, L481).
  PASS.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on prior structural QA for §4.5 section/heading numbering and template
  conformance (not re-verified here — this lens is crossref-chain semantics only).

**(b) Independent semantic checks (≥1 required, INV-019):**
- Traced the `{context_path}`/`context.yaml` producer-consumer pair across Step 2 (L205)
  and Step 3 (L215) by direct Read — found the unbound placeholder (C1). Tool evidence:
  Read SKILL.md L133-292; grep `context_path|context.yaml` returned L205 (producer) vs
  L215 (consumer) with non-matching tokens.
- Cross-verified the Step 4 enum and Step 5 fields against the ACTUAL troubleshoot
  contract, not against the task-protocol's own description of it. Tool evidence: grep
  `recommended_escalation|tasklist_insertion_path|...` in sc-troubleshoot-protocol/SKILL.md
  → L73-77, L471. Enum matched (PASS); confirmed `--tier` is NOT a troubleshoot flag
  (troubleshoot L120/L137 parse `--depth`), which is what makes C4/C5 real contradictions
  rather than cosmetic.
- Verified the incident-report filenames `rca-verdict.md`/`solution-verdict.md` are NOT
  emitted by the backend. Tool evidence: grep `rca-verdict|solution-verdict|REPORT.md`
  in sc-troubleshoot-protocol/SKILL.md → only `REPORT.md` + summary fields exist; the two
  verdict filenames have zero hits (C3).

**Self-Audit answers:**
1. Factual claims independently verified against source: 12 chain links + 6 PASS
   consistency checks, each tied to a specific line in one of the two SKILL.md files.
2. Files read: `sc-task-protocol/SKILL.md` (§4.5, L133-292) and
   `sc-troubleshoot-protocol/SKILL.md` (contract L45-89, dispatch L120-152, Wave 5 L443-481).
3. If 0 issues were claimed it should not be trusted — but 6 issues were found, each with
   a line-cited contradiction between two points in the chain. The C1/C4 pair in particular
   are executor-blocking, not stylistic.
4. No web research performed (chain is fully local-file-bound). Tavily-first N/A.

---

## Summary
- Chain links traced: 13 (L0-L12)
- Links PASS: 7 fully + 2 partial-OK
- Links FAIL: 4 (L2, L3-ref, L11, L12) producing 6 distinct findings
- Critical issues: 2 (C1 unbound `{context_path}`, C4 `/sc:forensic` backend contradiction)
- Important issues: 3 (C2 wrong step-ref, C3 dangling verdict filenames, C5 `--tier`/value enum)
- Minor issues: 1 (C6 implicit retry loop-back)
- Issues fixed in-place: 0 (fix_authorization: false)

## Confidence
Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 1 (full §4.5 + surrounding) | Grep: 5 | Glob: 0 | Bash: 5 (grep/ls wrappers)

## Recommendations
- Resolve C1 and C4 before this migration ships — both are executor-blocking (one leaves
  a placeholder unresolved, the other points the operator at a skill that the chain does
  not otherwise use).
- C2/C3/C5 are documentation-integrity contradictions that will mislead anyone reading
  §4.5 as the source of truth; fix in the same pass.
- Root-cause hypothesis for C3/C4/C5: §4.5 was migrated from a `/sc:forensic --tier`
  backend to a `/sc:troubleshoot --depth` backend, and the Escalation Budget + Incident
  Reporting blocks were not updated alongside the Execution Flow. Recommend a grep for
  `forensic` / `--tier` / `-verdict.md` across the whole skill to catch any sibling stragglers.

## QA Complete
