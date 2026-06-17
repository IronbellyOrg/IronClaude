# QA Report — Synthesis Gate (Internal-Consistency Lens, PG3)

**Topic:** Wiring `--context`/`--caller` into /sc:troubleshoot (Phase 3 MDTM migration)
**Date:** 2026-06-16
**Phase:** synthesis-gate (internal-consistency cross-surface verification)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)

---

## Overall Verdict: FAIL

Cross-surface internal consistency does NOT hold. The command file makes two claims about `--context`/`--caller` behavior that the skill does not implement, and the skill's own Wave 0 forward-reference to Wave 5 is dangling. Found 5 distinct cross-surface inconsistencies (3 substantive + 2 corroborating/structural).

---

## Surfaces Compared

| ID | Surface | File:Line |
|----|---------|-----------|
| S1 | Command Options `--context` row | troubleshoot.md:59 |
| S2 | Command Options `--caller` row | troubleshoot.md:60 |
| S3 | Command Behavioral-Summary parse step | troubleshoot.md:66 |
| S4 | Command Behavioral-Summary surface-on-return step | troubleshoot.md:69 |
| S5 | Skill Wave 0 flag list | SKILL.md:115 |
| S6 | Skill Wave 0 step 6 (resolve behavior) | SKILL.md:143 |
| S7 | Skill TARGET header keys | SKILL.md:138-139 |
| S8 | Skill Wave 0 STOP conditions | SKILL.md:147 |
| S9 | Skill Wave 5 body (Synthesis + Report) | SKILL.md:421-472 |
| S10 | Skill Wave 5 SUMMARY footer keys | SKILL.md:460-461 |

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `--context` declared in command argument-hint + Options | PASS | troubleshoot.md:8 argument-hint lists `[--context <path>]`; :59 Options row present |
| 2 | `--caller` declared in command argument-hint + Options | PASS | troubleshoot.md:8 lists `[--caller <name>]`; :60 Options row present |
| 3 | `--context`/`--caller` in skill Wave 0 flag list | PASS | SKILL.md:115 lists both under Optional |
| 4 | `caller=task-unified` → Wave 5 emits `return-contract.yaml` stated consistently | FAIL | S2 (cmd:60) + S6 (skill:143) both promise emission "see Wave 5"; **Wave 5 body (S9, SKILL.md:421-472) contains NO emission step**. Dangling forward-reference. |
| 5 | `--context` "echoed in the Wave 5 return" stated consistently | FAIL | S1 (cmd:59) claims context is "echoed in the Wave 5 return"; **no Wave 5 step or SUMMARY-footer key echoes `context_path`** — S10 footer (SKILL.md:460-461) emits only `caller:` and `return_contract_path:`, not the context path |
| 6 | Command does NOT claim it performs the emission itself | PASS | troubleshoot.md:64-69 "command file performs only" parse/validate/handoff/surface; :69 surfaces "the emitted return-contract.yaml path" (skill emits, command surfaces) — correct division |
| 7 | `--context` read in Wave 0 + recorded in audit header | PARTIAL/PASS | S6 (skill:143) reads `--context`, resolves to abs path, STOP if unreadable; S7 TARGET header has `context_path: <abs-path|none>` (SKILL.md:139); command S1 says "recorded in the audit-log header" — agree |
| 8 | TARGET header `caller:`/`context_path:` keys present | PASS | SKILL.md:138 `caller: <name|none>`; :139 `context_path: <abs-path|none>` |
| 9 | SUMMARY footer `caller:`/`return_contract_path:` keys present | PASS | SKILL.md:460 `caller: <name|none>`; :461 `return_contract_path: <abs-path|none>` |
| 10 | Wave 0 forward-ref "(see Wave 5)" resolves to a real Wave 5 anchor | FAIL | SKILL.md:143 says "mark Wave 5 to emit `return-contract.yaml` (see Wave 5)" — Wave 5 (SKILL.md:421-472) has no matching anchor/step. Forward-ref points at nothing. |
| 11 | Refs table lists a return-contract / adapter ref | FAIL (corroborating) | SKILL.md:577-592 Refs table has no `return-contract` / `caller-adapter` ref; consistent with the missing Wave 5 emission step — the emission machinery is undocumented end-to-end |

## Summary
- Surfaces compared: 10
- Checks passed: 6 / 11
- Checks failed: 4 (one is corroborating)
- Substantive cross-surface inconsistencies: 3 (CRITICAL ×1, IMPORTANT ×2)
- Issues fixed in-place: 0 (REPORT ONLY)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | SKILL.md Wave 5 (421-472) vs Wave 0 (143) + cmd:60 | `caller=task-unified` is promised to trigger `return-contract.yaml` emission in Wave 5 by BOTH the command (`--caller` row, line 60) and the skill Wave 0 step 6 ("mark Wave 5 to emit `return-contract.yaml` (see Wave 5)", line 143). The Wave 5 body has **no emission step**. The SUMMARY footer reserves `return_contract_path:` (line 461) but nothing populates it. The feature is advertised on 3 surfaces and implemented on 0. | Add an explicit Wave 5 step: "When `caller=task-unified` (from Wave 0), emit `<output-dir>/return-contract.yaml` adapter and set `return_contract_path:` in the SUMMARY footer." Add the matching anchor the "(see Wave 5)" ref points at. |
| 2 | IMPORTANT | troubleshoot.md:59 vs SKILL.md Wave 5 + footer | Command `--context` row claims the context is "echoed in the Wave 5 return." No Wave 5 step echoes it and the SUMMARY footer (460-461) has no `context_path:` key — only the TARGET header (139) records it. The "echoed in the Wave 5 return" half of the command's promise has no skill-side implementation. | Either (a) add `context_path:` to the SUMMARY footer + a Wave 5 echo step, or (b) soften the command `--context` description to "recorded in the audit-log header" only, dropping the unbacked "echoed in the Wave 5 return" clause. |
| 3 | IMPORTANT | SKILL.md:143 "(see Wave 5)" | Dangling intra-skill forward-reference: Wave 0 step 6 points readers to "Wave 5" for the emission, but Wave 5 has no return-contract anchor/step. A maintainer following the cross-reference lands on nothing. | Resolve by fixing Issue 1 (the anchor appears once Wave 5 gains the emission step). |
| 4 | MINOR | SKILL.md Refs table (577-592) | No ref documents the `return-contract.yaml` adapter shape/schema. Corroborates that the emission path is undocumented end-to-end, not merely under-specified in Wave 5. | Optional: add a `refs/return-contract-adapter.md` entry, or inline the adapter schema in the new Wave 5 step. |

## Points That DID Agree (no issue)
- Both surfaces name `task-unified` as the triggering caller value (cmd:60, skill:143) — token-consistent.
- The command correctly does NOT claim to perform the emission itself; it surfaces the skill-emitted path (cmd:69). No command-vs-skill ownership contradiction.
- `--context` read-in-Wave-0 + TARGET-header `context_path:` recording is consistent across cmd:59, skill:143, skill:139.
- STOP-on-unreadable-`--context` is consistent (cmd implies ingestion in Wave 0; skill:143 + skill:147 both STOP on unreadable path).
- TARGET header (138-139) and SUMMARY footer (460-461) both carry `caller:`; values are token-consistent.

## Confidence
**Verified:** 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 3 | Grep: 2 | Glob: 0 | Bash: 2

All 10 surfaces were read directly (full command file; full SKILL.md across two Read pages covering lines 1-594; two targeted greps confirming the absence of any return-contract/context-echo step in the Wave 5 region 420-472). The CRITICAL finding rests on a confirmed ABSENCE: grep for `return.?contract|emit|context_path|echo` across the Wave 5 body returned only the footer key line 461 and zero emission steps.

## Recommendations
- Resolve Issue 1 (CRITICAL) before this synthesis advances to assembly — the `--caller`→emission contract is the core of the Phase 3 migration and is currently advertised-but-unimplemented across 3 surfaces.
- Resolve Issue 2 (IMPORTANT) by reconciling the command `--context` description with what Wave 5 actually does (echo step OR description softening).
- Issues 3 and 4 are discharged automatically once Issue 1's Wave 5 emission step lands.

## QA Complete
