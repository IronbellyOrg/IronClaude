# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** Sprint 429 / account-exhaustion recovery — 6-phase MDTM build research
**Date:** 2026-06-15
**Phase:** research-gate
**Lens:** gap-detection (find what researchers MISSED that the builder needs)
**Fix authorization:** false (report-only)
**Fix cycle:** N/A

---

## Method

Adversarial stance. Assume the research is incomplete. Cross-check every spec
requirement (P1-P6, §5 edge cases, §6 test plan) against the research files for
backing. A gap = spec requirement with no actionable research coverage.

_(findings appended incrementally below)_

---

## Coverage matrix — spec requirement → research backing

| Spec unit | Research backing | Actionable? | Verdict |
|---|---|---|---|
| P1 detector (`detect_provider_failure`, enum, regexes, text-core) | 01 FILE-1 (6 symbols + 2 import-adds, insertion zone L250-253), 02 Pattern A/B, 04 §1-2 | YES — per-symbol Edit list w/ exact lines | COVERED |
| P2 TaskStatus + TaskResult fields + `_classify_transcript` align | 01 FILE-2 (member+is_failure+3 fields+to/from_dict), 03 IP-6 (insert above :582), 02 Pattern C/D | YES | COVERED |
| P3 SessionResetPolicy + re-spawn loop + latch + persistence | 01 FILE-3, 03 IP-1 (wrap :986-993, both call sites :1134/:1337), 02 Pattern E, 04 §3 | YES — both call sites + storm bound | COVERED |
| P4 single-session path + PROVIDER_EXHAUSTED | 03 IP-2 (wrap :1815-1956, short-circuit before :1993), IP-3 (B1 bundle guard), 04 F-1 | YES | COVERED (see G-1) |
| P5 aienv + halt UX + `--max-session-resets` 4-hop | 01 FILE-4, 03 IP-9/IP-10 (4-hop chain), 05 §8-9 | YES — but design choice (G-2) | COVERED w/ caveat |
| P6 execution-log events + nominator (G) exclusion | 03 IP-5 (logger._jsonl), IP-7 (nominators) | PARTIAL — see G-3 | GAP |
| §5 edge cases 1-10 | 04 §5 (all 10 mapped w/ mechanism + evidence anchor) | YES | COVERED |
| §6 test plan (6 fixtures, factory scenarios, parity, back-compat) | 05 (all enumerated w/ target paths + worked factory) | YES | COVERED |
| R3 wrinkle: per-task ERROR-vs-PROVIDER_EXHAUSTED phase collapse | 03 IP-3 (per-task continues at :1781 → PhaseStatus.ERROR; phase signal carried via task_results[*].failure_class) | YES — explicitly resolved | COVERED |
| halt_reason/exhausted_model on PhaseResult AND TaskResult | 03 IP-5 (PhaseResult new fields + TaskResult 3 fields, both persisted via :2691) | YES | COVERED |
| single-session path fully traced (executor.py:1815/:1993) | 03 IP-2 line-exact, 04 §0 | YES | COVERED |

**Independent verification performed (adversarial re-test of highest-stakes claims):**
- monitor.py import block — CONFIRMED lacks `enum`/`dataclass` (only json/logging/re/threading/time/Path). 01 FILE-1's "2 import-adds" gap is real.
- `count_turns_from_output` (monitor.py:223) vs spec's `count_turns_from_stream_json` (process.py:32) — CONFIRMED: spec name is wrong; the symbol is in process.py. Research caught this (01/05).
- `TaskResult.from_dict` (models.py:218-240) — CONFIRMED hard-keyed for all result-level fields. Back-compat hazard real.
- No `DriftNominator` — CONFIRMED only Nominator/ManualNominator/ReflectReportNominator. IP-7 correction is right (research-notes line 38 was wrong).
- F-1 (`:2103 if status.is_failure:`) — CONFIRMED runs DiagnosticCollector + FailureClassifier + writes phase-N-diagnostic.md. Spec's "only halts the phase" is FALSE for single-session path.
- 4-hop flag chain — CONFIRMED commands.py :203 option / :255 param / :353 load_sprint_config / models.py :590 SprintConfig field. `--task-parallelism` template exact.
- `--resume`/`resume_task_id` (commands.py:197), `run` subcommand symbol (`:234`) — CONFIRMED. R5's two "UNVERIFIED" items resolve cleanly (minor builder-closes).

---

## Issues Found

| # | Severity | Location | Issue | Required Fix (for builder) |
|---|----------|----------|-------|----------------------------|
| G-1 | MINOR | spec §4 Layer 2 vs 04 F-1 / 03 IP-3 | Spec text claims `is_failure` has "no auto-remediation consumer" — FALSE for single-session path (`:2103` runs DiagnosticCollector). Research SURFACED this correctly in BOTH 04 (F-1) and 03 (IP-3) with resolution options B1/B2. Not a research gap — research over-delivered. Flagged MINOR only so the builder treats the spec sentence as superseded by the research finding, and writes the P4 "assert no phase-N-diagnostic.md written on single-session 429 halt" test. | Builder: encode option B1 (add PROVIDER_EXHAUSTED to is_terminal NOT is_failure, OR guard :2103); add the no-diagnostic-bundle test. Research already specifies this. |
| G-2 | MINOR | aienv reader-vs-parser (01 FILE-4, research-notes (G)/AMBIGUITIES) | The aienv.py os.environ-reader (A) vs file-parser (B) design choice IS flagged as `needs_human_decision`-adjacent in 01 FILE-4 (lines 169-172) and research-notes line 217. Coverage is adequate. The residual gap: the §6 test plan (05 §8.2) writes a FIXTURE `~/.aienv` file and points the parser at an injectable `aienv_path` — which structurally PRESUMES design (B) the file-parser. So the "recommend (A)" guidance in 01 and the testability requirement in 05 are in mild tension. | Builder: resolve in ONE item — if (A) os.environ reader chosen, the test must inject via monkeypatched env, NOT a fixture file; if (B), the suggester needs the `aienv_path` kwarg. Encode the documented default + HALT-on-nontrivial per `feedback_human_decision_items_must_halt`. Both research files name the tension; builder must not let the test item and the impl item silently diverge. |
| G-3 | IMPORTANT | (G) nominator exclusion — 03 IP-7, P6 | IP-7 flagged that the (G) `failure_class=="provider_exhaustion"` exclusion depends on `context` carrying per-task status, marked it UNVERIFIED, and said "builder must trace the call site." **Independent verification found the reality is sharper than IP-7 stated: ALL THREE `nominate()` call sites (`rerun_tasks.py:1419/1421/1433`) pass a literal empty dict `{}`.** `ManualNominator.nominate` returns `list(self.tasks)` and reads NOTHING from context. So the (G) exclusion cannot read `failure_class` from `context` at all without FIRST plumbing `phase-N-result.json` `task_results[*].failure_class` data INTO that empty dict at the call site — a deeper change than "add a filter to the nominator." IP-7's "trace before implementing" is correct in spirit but understates the work: there is no context to filter on; it must be constructed. | Builder: the P6 (G) item MUST be written as `needs_human_decision` with this concrete finding in its Context: "context dict is empty `{}` at all 3 call sites (rerun_tasks.py:1419/1421/1433); ManualNominator ignores it. Exclusion requires loading task_results[*].failure_class from phase-N-result.json into context at the call site first." Per the deferred-decision contract, write PENDING + proceed with the documented fallback (scope contract #4 to the live auto-path, which IP-3(A) already proves needs no bundle), do NOT ship an unreviewed nominator behavior change. This sharper framing should be in the item, not left for the builder to re-discover. |

**Note on G-3 severity:** IMPORTANT (not CRITICAL) because the live per-task path already satisfies contract #4 by construction (IP-3(A): per-task block `continue`s at :1781, never reaching :2103), so (G) only affects the operator-invoked `rerun-tasks` re-entry, and the spec already authorizes deferring it to P6 with a documented fallback. It does not BLOCK the builder — but the empty-`{}` reality must be in the item Context or the executor agent will hit it cold.

---

## Confidence Gate

**Checklist categorization (gap-detection lens, 6 prompt items):**
1. Coverage gaps (P1-P6 / §5 / §6) — [x] VERIFIED via coverage matrix; only P6 (G) is a partial gap (G-3).
2. Findings actionable for builder — [x] VERIFIED: per-symbol Edit lists w/ exact lines, worked factory example, 4-hop chain enumerated.
3. Integration points (single-session :1815/:1993, R3 phase-collapse wrinkle, halt_reason persistence on both PhaseResult+TaskResult) — [x] VERIFIED all three present & line-exact (IP-2, IP-3, IP-5); F-1 independently re-tested.
4. Test/fixture coverage (6 fixtures + factory + parity + back-compat) — [x] VERIFIED all w/ target paths (05 §3-10).
5. Unresolved decisions (aienv reader-vs-parser; (G) nominator dep on context dict) — [x] VERIFIED both flagged; aienv=G-2 (adequate, mild tension), (G)=G-3 (under-stated, empty-`{}` finding added).
6. `--max-session-resets` 4-hop chain traced — [x] VERIFIED independently (commands.py:203/255/353 + models.py:590).

- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 4 (grep/sed via bash: nominators, :2103 gate, 4-hop chain, imports, from_dict, count_turns, resume flag, run symbol — each mapped to a specific checklist claim)
- No web research performed (all claims local-source-bound; Tavily-first N/A this phase).

Tool-engagement note: 12 verification actions (8 Read + 4 Bash-grep) ≥ 6 checklist items. Each Read targeted a specific research/source file; each Bash independently re-tested a named high-stakes claim. No padding.

---

## Verdict rationale

This is **exceptionally strong research** — among the most thorough research sets I have audited. It does not merely cover the spec; it CORRECTS the spec in four material places (count_turns symbol name, no-DriftNominator, F-1 diagnostic gate, cmd/env in pipeline base not sprint), each with independent verification I re-confirmed. Every P1-P6 requirement, all 10 edge cases, the full §6 test plan, the R3 phase-collapse wrinkle, and dual-surface halt_reason persistence are covered with file:line-exact, builder-actionable detail.

Per the research-gate rule ("ALL gaps regardless of severity = overall FAIL; must be resolved before synthesis"), the presence of G-3 (IMPORTANT) + G-1/G-2 (MINOR) means the gate is **FAIL** — but this is a "polish before build" FAIL, not a "research is inadequate" FAIL. The single load-bearing gap is G-3: the (G) nominator exclusion's dependency on an empty `{}` context dict is under-described in IP-7 and must be sharpened in the builder's P6 item Context before the build task is authored. G-1 and G-2 are already surfaced by the research itself and need only a one-line builder acknowledgment each.

Recommended resolution path (cheapest): a single research-notes addendum OR a builder-item Context augmentation capturing G-1/G-2/G-3 — no new research spawns required. The underlying code surface is fully mapped.

---

## VERDICT: FAIL

3 gaps (1 IMPORTANT: G-3 nominator-context-is-empty under-description; 2 MINOR: G-1 spec-vs-F-1 sentence, G-2 aienv test/impl design tension). All are resolvable by sharpening builder-item Context — no re-research needed. Resolve the 3 before synthesis/build per the zero-gap research-gate rule.

## QA Complete
