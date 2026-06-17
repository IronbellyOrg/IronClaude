# QA Report — Content Actionability (Phase 3 / Page 3)

**Topic:** Wave 0 step 6 (`--context`/`--caller` resolve sub-step) + Wave 0 STOP conditions in sc-troubleshoot-protocol/SKILL.md
**Date:** 2026-06-16
**Phase:** doc-qualitative (actionability lens — instruction-level executability)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)

---

## Overall Verdict: FAIL

The actionability lens fails. The most load-bearing new instruction — `When caller=task-unified, mark Wave 5 to emit return-contract.yaml (see Wave 5)` — is **unexecutable** because Wave 5 contains no emit step, no schema, no path, and no consumption of the "mark Wave 5" flag. Two further instructions are non-actionable (read-but-never-consumed caller brief; ambiguous "mark Wave 5" mechanism). The simpler instructions called out in the spawn prompt (`--caller` → header field; `--context` unreadable → STOP) do pass.

## Instructions Reviewed
| # | Instruction (verbatim target) | Result | Evidence |
|---|-------------------------------|--------|----------|
| 1 | "If `--caller` is set, record it in the audit header `caller:` field" | PASS | Target field exists in the Wave 0 TARGET header at SKILL.md:138 (`caller: <name\|none>`) and again in the Wave 5 SUMMARY footer at :460. Clear action (record) + clear target (named field). Executable. |
| 2 | "If `--context <path>` is set, read it ... resolve it to an absolute path; STOP if the path is unreadable" | PARTIAL-FAIL | The read/resolve/STOP mechanics are clear and binary (a path either reads or it does not). BUT the read result — "the caller brief" — is never consumed by any downstream wave (see Finding F2). The instruction is locally executable but produces a dead value. |
| 3 | "When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml` (see Wave 5)" | FAIL | The `(see Wave 5)` cross-reference is dangling. Wave 5 (SKILL.md:421-472) has zero emit step for `return-contract.yaml`. The string `return-contract.yaml` appears exactly ONCE in the entire file — here at :143. See Finding F1. |
| 4 | New STOP condition "`--context` path unreadable" | PASS | Present at SKILL.md:147 in the Wave 0 STOP list; trigger is binary and matches the step-6 STOP clause at :143. Clear trigger. |
| 5 | "mark Wave 5 to emit" — the marking mechanism itself | FAIL | No state-passing mechanism is defined. There is no flag in the TARGET header, no output-contract field, and no Wave 5 precondition that reads such a mark. See Finding F3. |

## Summary
- Instructions passing actionability: 2 / 5 (items 1, 4)
- Instructions failing/partial: 3 / 5 (items 2, 3, 5)
- CRITICAL findings: 1 (F1)
- IMPORTANT findings: 2 (F2, F3)
- MINOR findings: 1 (F4)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | CRITICAL | SKILL.md:143 → Wave 5 (:421-472) | Dangling forward-reference. Line 143 instructs "mark Wave 5 to emit `return-contract.yaml` (see Wave 5)", but Wave 5 contains NO step that emits it. `grep -c "return-contract.yaml"` over the whole file = **1** (only the instruction at :143; the pointed-to implementation does not exist). The agent reaches "(see Wave 5)" and finds nothing to do — unexecutable. The Wave 5 SUMMARY footer at :461 declares `return_contract_path: <abs-path\|none>` but no step ever populates that path or writes the file. | Add an explicit Wave 5 step (gated on the `caller=task-unified` mark) that: (a) names the output path (e.g. `<output-dir>/return-contract.yaml`), (b) defines the YAML schema/fields the file must contain, (c) sets `return_contract_path` in the footer/output contract to that path. Without a schema the instruction cannot be executed deterministically. |
| F2 | IMPORTANT | SKILL.md:143 | Read-but-never-consumed value. The step reads `--context` "(the caller brief)" and resolves it to an absolute path, but no wave consumes the brief content. `grep` for `brief` shows it is referenced only at :31 (`--scope` description), :143 (this step), and :275/:580 (the root-cause-analyst's OWN brief, unrelated to `--context`). The caller brief is loaded into nothing — there is no instruction to inject it into Wave 1 grounding, Wave 1.7 hypothesis formation, or any agent spawn. An operator cannot tell WHAT to do with the brief after reading it. | Specify the consumer: e.g. "pass the resolved caller-brief content into the root-cause-analyst brief in Wave 1.7" or "include it in the Wave 1 grounding context". Tie the read to a downstream use, or the read is pure overhead. |
| F3 | IMPORTANT | SKILL.md:143 | Underspecified mechanism: "mark Wave 5". The verb "mark" names no concrete mechanism. There is no flag field in the TARGET header (:128-141) for this mark, no output-contract field, and Wave 5's preconditions (:421-427) read no such mark. An executing agent cannot deterministically know HOW to set the mark or HOW Wave 5 detects it. (Distinct from F1: F1 is the missing emit step; F3 is the missing state-passing channel that would gate that step.) | Define the mark as a concrete, inspectable signal — e.g. add `emit_return_contract: <bool>` to the TARGET header or output contract, set it in Wave 0 step 6, and add it to Wave 5's preconditions as the gate for the new emit step from F1. |
| F4 | MINOR | SKILL.md:62-72 (output-contract table) | The output-contract field table does NOT list `return_contract_path` even though the Wave 5 footer (:461) emits it. Consumers reading the documented contract table would not know the field exists. (Structural-adjacent, but it directly weakens the actionability of "emit return-contract.yaml" because nothing in the documented contract surfaces the result.) | Add a `return_contract_path` row to the output-contract table (string \| null; populated only when `caller=task-unified`), mirroring the `task_file_path` / `doc_context_card_path` convention. |

## Actions Taken
None — `fix_authorization: false`. All findings reported only.

## Self-Audit
1. **Claims independently verified against source:** 6 — (a) `caller:` field exists in TARGET header (:138); (b) `caller:` exists in Wave 5 footer (:460); (c) `return-contract.yaml` occurs exactly once file-wide (`grep -c` = 1, only :143); (d) Wave 5 body (:421-472) has no emit step; (e) `--context` path-unreadable STOP present in both step 6 (:143) and the STOP list (:147); (f) "caller brief" is never consumed downstream (`grep brief` → only :31, :143, :275, :580, none consuming `--context`).
2. **Files read:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (lines 1-200, 418-479, 440-462); `refs/` directory listing + grep across all refs for `return-contract|return_contract|task-unified` (zero hits).
3. **Why trust this found issues:** It did not return 0 — it found a CRITICAL dangling forward-reference proven by a file-wide occurrence count of exactly 1 for `return-contract.yaml`, plus two never-consumed-value defects proven by grep of the consumer surface. Each verdict cites a line number or a grep count.
4. **Web research:** None performed — this review is entirely local-file-bound (instruction-to-source verification). No Tavily/fallback needed.

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 3 | Grep(bash grep): 4 | Glob: 0 | Bash(ls): 1

## Recommendations
1. **Block Phase 3 sign-off until F1 is resolved.** The `caller=task-unified` → `return-contract.yaml` path is the integration contract between /sc:troubleshoot and task-unified (the whole point of wiring `--caller`). A dangling "(see Wave 5)" means the return-contract path is wired in name only; a real `task-unified` caller would get no contract file.
2. Resolve F2 and F3 together with F1 — they are the same broken seam (read context → mark → emit) viewed from three angles (consume / signal / write).
3. F4 is a 1-line table addition; bundle it with the F1 fix.

## QA Complete
