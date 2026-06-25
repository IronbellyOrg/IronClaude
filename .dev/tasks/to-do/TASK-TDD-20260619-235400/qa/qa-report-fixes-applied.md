# QA Report — Report-Validation Fixes Applied (6.12)

**Topic:** sc:reflect Tier-2 Swarm Ensemble TDD (TASK-TDD-20260619-235400)
**Date:** 2026-06-20
**Phase:** report-validation (fix-application pass)
**Fix authorization:** true (in-place)
**Target (pinned, preserved):** `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md`
**Final line count:** 1773 (within 1,200–1,800 budget) ✅

---

## Overall Verdict: ALL FIXES APPLIED & VERIFIED

12 findings (I-A..I-E + M-1..M-7) applied in-place, each verified against shipped worktree source before editing. No fabrication. Pinned path preserved. Non-findings deliberately untouched.

---

## IMPORTANT fixes

| ID | Location | Fix applied | Source verification |
|----|----------|-------------|---------------------|
| I-A | §8.2 `reduce_wave3` signature block | `mode` moved to 2nd POSITIONAL param (before bare `*`); kwarg renamed `policy`→`status_policy`. Now matches §18.2 and §6.1/§11.1 positional calls. | `src/superclaude/cli/swarm/reduce.py:555-561` — `def reduce_wave3(worker_results, mode="normalize+merge", *, output_dir=..., workers_requested=..., status_policy=...)` |
| I-B | §25 / §26 headers | Removed `*(light — CLI infrastructure)*` / `*(light)*` from `## 25.` / `## 26.` header lines; moved qualifier into the `>` note directly beneath each (mirrors §17). Bare headers now match ToC anchors `#25-operational-readiness` / `#26-cost--resource-estimation`. | §17 scope-note pattern (tdd.md:1247); ToC entries tdd.md:184-185 |
| I-C | §1, §2.1, §28 glossary | Standardized to "2–3 heterogeneous reviewers (the `--reviewers` flag accepts [2,4], default 3)". §28 glossary's bare "2–4" reconciled. | spec.md:28 (conceptual "2-3 reviewers on different model classes"); spec.md:406 (`--reviewers` clamped `[2,4]`, default 3) |
| I-D | §15.5 traceability table | Added 4 missing NFR rows: NFR-RH2.1/.2 → `test_no_nesting_guard.py` Layer B extended to `ensemble.py` (U7); .7 → observability (§14.1 done.json / §14.2 --detached/--tui); .8 → `read_env` preflight + §13.2 proxy grep audit. Table now covers all 8 NFRs. | spec.md:470-477 (NFR-RH2.1–.8 + their test mappings) |
| I-E | §15.3 row I6 | "spec §5.4 ordering" → "spec §5.3 ordering" (spec has no §5.4). | spec.md headers: §5.1, §5.3 exist; no §5.4. Ordering/`mn_guard_table` is in spec §5.3 |

---

## MINOR fixes

| ID | Location | Fix applied | Source verification |
|----|----------|-------------|---------------------|
| M-1 | §5.1 FR source-ID note | Corrected the "read straight" claim: now states the Source column is `.1,.2,.3,.4,.9,.5,.6,.7,.8` (not straight numeric) and documents **FR-005 ↔ FR-RH2.9** (with .5/.6/.7/.8 offset following). | spec.md sequences FR-RH2.9 after FR-RH2.4; §5.1 Source column in tdd.md:333 |
| M-2 | §6.5, §21, §27.2 (×2) | Standardized the 3 reused-symbol cites to the `def` line: `dispatch_wave1`→`dispatch.py:334`, `_resolve_run_transport_factory`→`commands.py:612`, `reduce_wave3`→`reduce.py:555`. Removed `:344`/`:619`/`:578` and `L334/344`/`L612/619` variants. | `dispatch.py:334`, `commands.py:612`, `reduce.py:555` (grep `def …`) |
| M-3 | Document Information table | Added `Last Verified` row ("2026-06-20 against current worktree source") → table now has 8 rows. | template requires 8 rows |
| M-4 | §18.4 Dependency Risk Callouts | Added note: `cli/pipeline/process.py` investigated, ORTHOGONAL — a generic `ClaudeProcess` subprocess-lifecycle primitive used by Tier-1 (unchanged); outside the FR-RH2 swarm-seam dependency surface. | `pipeline/process.py:72` (class ClaudeProcess); `reflect/runner.py:31` imports it for Tier-1 |
| M-5 | §13.1 threat-model row | Qualified the "no /v1 literal" claim: "...no `:4000`/`:8317`/`/v1`/`/cli` literal **in executable transport/config code paths (docstring examples in `openai_compat.py` L17/217/219 excepted)**." | `openai_compat.py` L17/217/219 — `/v1` appears only in docstring examples |
| M-6 | §7.1, §18.2, §28, §6.5, §15.4 | Off-by-one def-line cites corrected: ResultContract `876→877`, WorkerResult `1026→1027`, DoneSentinel `1423→1424`, REGISTRY `182→181`, STRATEGIES `209→208`; `mechanical_merge` "8 LOC"→"7 LOC" (9 occurrences incl. ASCII box + mermaid, alignment preserved); §15.4 test counts `277/221/173`→`276/220/172`. | `models.py:877/1027/1424` (class lines vs `@dataclass` decorator); `recipes/__init__.py:181/208` (dict literals); `merge.py:51-57` = 7-LOC body; `wc -l`: test_verdict_mapping.py=276, test_runner_e2e.py=220, test_writeback.py=172 |
| M-7 | §337 amendment, §5.4 refs, §11.2 ref | (a) §337 NFR-7 amendment "(§9)" clarified → "the **spec's §9 (Migration & Rollout)** — NOT TDD §9, which is N/A (State Management)". (b) "spec §5.4"→"spec §5.3" (done via I-E). (c) §11.2 "(§12.2)"→"(§12.2.1)": **already correct** in the doc (refs already cite §12.2.1; no bare "(§12.2)" exists) — no change needed. | spec §9 = Migration & Rollout (spec.md:525); spec L319 instructs recording amendment in spec §9; TDD §9 = State Management/N/A |

---

## Internal-consistency cross-checks (post-fix)

- §8.2 `reduce_wave3` signature now byte-consistent with §18.2 interface column. ✅
- ToC anchors `#25-operational-readiness` / `#26-cost--resource-estimation` resolve to bare `## 25.` / `## 26.` headers. ✅
- Reviewer count consistent in all 3 spots (§1 / §2.1 / §28); zero "2-4"/"2–4 reviewers" remain. ✅
- §15.5 now lists all 8 NFRs (.1–.8). ✅
- Zero residual stale variants: `:344`/`:619`/`:578`, `models.py:876/1026/1423`, `L182`/`L209`, "8 LOC"/"8-LOC", "277/221/173 L", "spec §5.4" — all grep-empty. ✅

## Non-findings preserved (NOT changed, per instruction)

- 9 FRs kept (FR-001..FR-009) — confirmed 9 rows.
- §22 Q5–Q8 kept.
- NFR-7 → spec §9 routing kept (clarified, not re-routed).
- Aspirational-vs-current NET-NEW framing (`ensemble.py` does-not-exist) kept (19 hits).
- §5.4 internal TDD cross-refs at §11.2 / §14.3 left intact (they reference the TDD's own §5.4 section, which exists — only "spec §5.4" attributions were corrected).
- merge.py `L50–57` / `L9-57` physical line-range cites left intact (accurate spans; only the "LOC count" was wrong, now 7).

---

## Confidence

- **Confidence:** "Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%"
- **Tool engagement:** "Read: 9 | Grep/Bash: 9 | Edit: 24 | Glob: 0" (every source claim verified by Read/Bash before its Edit; no web research required — all claims are local-source-bound)
- **Final line count:** 1773 (within 1,200–1,800). ✅
- Every fix was verified against shipped worktree source (`src/superclaude/cli/swarm/*`, `src/superclaude/cli/reflect/*`, `tests/cli/reflect/*`, and the spec) BEFORE the edit was applied. No claim relies on another report.

## QA Complete
