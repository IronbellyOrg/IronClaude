# QA Report — Structural Verification (PG3 Fix-Cycle)

**Topic:** MDTM migration — wiring `--context`/`--caller` into /sc:troubleshoot
**Date:** 2026-06-16
**Phase:** fix-cycle (structural verification, Phase Gate 3)
**Fix cycle:** 1
**Fix authorization:** false (REPORT ONLY — no files edited)

---

## Overall Verdict: PASS

Both in-scope fixes applied correctly. No new structural issue introduced. Cluster 1 (Wave 5 emission BODY) correctly left deferred. All 9 flag ingestion sites intact.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FIX 1 — `context_path:` in Wave 5 SUMMARY footer, between `caller:` and `return_contract_path:` | PASS | SKILL.md L460 `caller: <name\|none>`, L461 `context_path: <abs-path\|none>`, L462 `return_contract_path: <abs-path\|none>` — exact ordering inside the `SC:TROUBLESHOOT:SUMMARY` block (L451-463). |
| 2 | FIX 1 fulfills the `--context` "echoed in the Wave 5 return" promise | PASS | Command `--context` Options row (troubleshoot.md L59) promises "echoed in the Wave 5 return"; the Wave 5 machine-readable return now carries `context_path:`. Promise reconciled. |
| 3 | FIX 2 — surface clause L69 backticks BOTH tokens | PASS | troubleshoot.md L69 reads ``…and (if `caller=task-unified`) the emitted `return-contract.yaml` path.`` Both `` `caller=task-unified` `` and `` `return-contract.yaml` `` are backticked, matching sibling exemplars `` (if `--fix`) `` and `` (if `pipeline_hardening_applicable`) `` on the same line. |
| 4 | No NEW structural issue introduced | PASS | TARGET header (L138-139) and SUMMARY footer (L460-462) both carry matching `caller:`/`context_path:` keys — additive, symmetric, mirrors existing footer style. No malformed YAML/HTML-comment fences; both blocks well-formed (`<!-- ... -->`). No other lines altered around the edits. |
| 5 | Cluster 1 (Wave 5 emission BODY) correctly LEFT deferred — no spurious emission step added | PASS | Wave 5 body (SKILL.md L421-473) has steps 1-5: load template, compose REPORT.md, evidence-validator pass, append footer, surface to user. NO `return-contract.yaml` emission step exists. Grep for `emit.*return-contract`/`return-contract.yaml` in the skill returns ONLY L143 (Wave 0 step 6 forward-reference "mark Wave 5 to emit … (see Wave 5)"). The "(see Wave 5)" still lands on no body step — exactly as designed; emission BODY is Phase 4 Step 4.7's deliverable. |
| 6 | All 9 flag ingestion sites intact | PASS | See enumeration below. |

## 9 Flag Ingestion Sites — Enumeration

**Command surface (`commands/troubleshoot.md`):**
1. L8 — `argument-hint` includes `[--context <path>] [--caller <name>]`
2. L59 — `--context` Options-table row (default `(none)`, ingested Wave 0, echoed Wave 5 return)
3. L60 — `--caller` Options-table row (Wave 5 emits return-contract adapter; audit header records `caller:`)
4. L66 — Behavioral Summary "Parse arguments" resolves `--context`, `--caller`
5. L69 — Surface clause: `(if `caller=task-unified`) the emitted `return-contract.yaml` path` (FIX 2 site)

**Skill surface (`skills/sc-troubleshoot-protocol/SKILL.md`):**
6. L115 — Wave 0 step 1 parse-flags Optional list includes `--context`, `--caller`
7. L138-139 — TARGET audit header keys `caller:` / `context_path:`
8. L143 — Wave 0 step 6: ingest `--caller` (record), `--context` (read+resolve+STOP-if-unreadable), and `caller=task-unified` → mark Wave 5 emission
9. L147 STOP condition (`--context` path unreadable) + L460-462 SUMMARY footer keys `caller:`/`context_path:`/`return_contract_path:` (FIX 1 site)

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found
None.

## Confidence

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: 2 | Glob: 0 | Bash: 2

- All 6 checks verified with direct tool evidence (Read of all 3 required files + targeted Grep/Bash on footer ordering, backtick rendering, emission-step absence, and flag-site enumeration).
- No UNCHECKED items.
- No UNVERIFIABLE items.

## Recommendations
- Green light: PG3 fix cycle is structurally clean. Proceed to next gate.
- Carry-forward for Phase 4: the Wave 5 emission BODY (Cluster 1) remains the deliverable of Phase 4 Step 4.7; the `(see Wave 5)` forward-reference at SKILL.md L143 still resolves to no body step until then. PG4's contract-producer-consumer + completeness lenses must re-verify the body lands.

## QA Complete
