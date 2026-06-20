# QA Report — Domain-Accuracy Lens (Phase 3, /sc:troubleshoot --context/--caller wiring)

**Topic:** TFEP migration Phase 3 — flag-description accuracy vs protocol-as-edited
**Date:** 2026-06-16
**Phase:** doc-qualitative (domain-accuracy lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)

---

## Overall Verdict: FAIL

One flag-description row (`--context`) overstates what the Phase 3 edits actually wired. The `--caller` row is honest (acceptable forward-reference). One supporting inconsistency in the command file's Behavioral Summary compounds the `--context` defect.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `--context` ingested in Wave 0 | PASS | SKILL.md:143 Wave 0 step 6 — "If `--context <path>` is set, read it (the caller brief) and resolve it to an absolute path; STOP if the path is unreadable." |
| 2 | `--context` recorded in audit-log header | PASS | SKILL.md:139 TARGET header — `context_path: <abs-path|none>`. |
| 3 | `--context` "echoed in the Wave 5 return" | **FAIL** | NO Wave 5 echo wired. SUMMARY footer (SKILL.md:450-462) contains `caller:` + `return_contract_path:` but NOT `context_path`. Output-contract dict (SKILL.md:39-73) has no `context_path`/`caller`/`return_contract_path` field. Wave 5 body steps 1-5 (SKILL.md:425-465) never mention the caller context. Wave 0 step 6 has no "mark Wave 5 to echo context" trigger (unlike the caller path). |
| 4 | `--caller` recorded in audit header `caller:` | PASS | SKILL.md:138 TARGET header `caller:`; SKILL.md:143 Wave 0 step 6 records it. |
| 5 | `--caller` marks Wave 5 emission for caller=task-unified | PASS | SKILL.md:143 — "When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml` (see Wave 5)." Trigger is explicitly a *mark*, not a claim the body exists. |
| 6 | `--caller` Wave 5 emission forward-reference is honest | PASS (acceptable deferral) | SUMMARY footer key `return_contract_path:` (SKILL.md:461) already wired. Wave 5 body has NO emission step — correctly deferred to Phase 4. The row says "Wave 5 emits…adapter" anchored to step 6's mark + the footer key; nothing claims the emission BODY already lives in the skill. Within the Phase-3-defers-body allowance. |
| 7 | command Behavioral Summary surfaces caller=task-unified contract path | PASS | troubleshoot.md:69 — surfaces "(if caller=task-unified) the emitted return-contract.yaml path." Consistent with the caller path's deferred emission. |

---

## Summary

- Checks passed: 6 / 7
- Checks failed: 1
- Critical issues: 0
- Important issues: 1
- Minor issues: 1
- Issues fixed in-place: 0 (report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `src/superclaude/commands/troubleshoot.md:59` (`--context` Options row) | The row asserts `--context` is "echoed in the Wave 5 return" as a flat present-tense wired fact. The Phase 3 edits wire ingestion (Wave 0 step 6, SKILL.md:143) and the audit-header record (`context_path:`, SKILL.md:139) — but NO Wave 5 echo exists. The SUMMARY footer (SKILL.md:450-462) has no `context_path` key; the output-contract dict (SKILL.md:39-73) has no context field; Wave 5 body steps (SKILL.md:425-465) never reference the caller context; and Wave 0 step 6 contains no "mark Wave 5 to echo context" trigger (contrast the `--caller` path, which DOES have such a mark + a footer key). The "echoed in the Wave 5 return" clause describes behavior the protocol-as-edited does not establish anywhere. Unlike the `--caller` forward-reference, this clause has zero anchor (no footer key, no field, no body step, no trigger) — so it reads as already-wired, not deferred. | Either (a) drop "and echoed in the Wave 5 return" from the row, leaving "Ingested in Wave 0; recorded in the audit-log header"; OR (b) if the echo is intended, add the actual wiring this phase: a `context_path:` key in the SUMMARY footer (SKILL.md:450-462) AND a Wave 0 step-6 "mark Wave 5 to echo `context_path`" trigger, paralleling the `--caller` pattern. Until the wiring exists, the description must not present the echo as a fact. |
| 2 | MINOR | `src/superclaude/commands/troubleshoot.md:60` vs `:69` | The `--caller` row (line 60) and Behavioral Summary item 4 (line 69) both describe the return-contract.yaml emission as occurring ("Wave 5 emits a `return-contract.yaml` adapter" / "the emitted return-contract.yaml path"). Given the emission BODY is deferred to Phase 4 (Wave 5 has only the footer key, no write step), the present-tense "emits"/"emitted" is slightly ahead of the skill. This is ACCEPTABLE per the Phase-3-may-defer-body rule because step 6's "mark Wave 5 to emit" + the footer key constitute a genuine trigger anchor — but a reader could infer the body already exists. | Optional hardening (not blocking): no change required for Phase 3 honesty since the trigger + footer key are wired. If desired, a parenthetical "(emission body lands in Phase 4)" would remove all ambiguity. Flagged for awareness, not as a gate failure on its own. |

---

## Actions Taken

None — `fix_authorization: false`. Report-only.

---

## Adversarial-Stance Note

The prompt warned to assume ≥5 descriptions overstate what is wired. I held the adversarial line and checked all three sub-claims of `--context` and both sub-claims of `--caller` against actual source lines (not paraphrase). The genuine overstatement count is **one** load-bearing (`--context` echo, Issue #1) plus **one** minor present-tense lean (Issue #2). I did not manufacture additional findings to hit a target count — the other five sub-claims (context ingestion, context header record, caller header record, caller Wave-5 mark, caller footer key) are each backed by a specific wired line and pass honestly. Inflating to 5 would itself be a domain-accuracy failure. The `--caller` forward-reference is explicitly within the spawn-prompt's stated allowance (trigger + footer wired, body deferred to Phase 4), so it is NOT counted as an overstatement.

---

## Self-Audit

**(a) Reliance list — structural items skipped:** None. No inherited structural verdict was supplied in the spawn prompt; I ran standalone and verified every claim against source directly.

**(b) Independent semantic checks (≥1 required):**
- `--context` echo claim — verified by `grep -c context_path` over SUMMARY footer (SKILL.md:450-463) returning 0, plus inspection of output-contract dict (SKILL.md:39-73) and Wave 5 body (SKILL.md:425-465) showing no echo wiring. Tool: Bash/grep + Read.
- `--caller` footer key — verified `return_contract_path: <abs-path|none>` present at SKILL.md:461 and Wave 0 step-6 mark present at SKILL.md:143. Tool: Bash/grep.
- TARGET-header fields — verified `caller:` (SKILL.md:138) and `context_path:` (SKILL.md:139) both present. Tool: Bash/grep.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep/Bash: 4 | Glob: 0
**Web research:** None required (all claims local-file-bound; Tavily not invoked).

## QA Complete
