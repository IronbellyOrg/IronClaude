# QA Consolidated Findings — Phase 2 Gate (8 reports merged)

**Topic:** sc-troubleshoot protocol generalization — Phase 2 SKILL.md gate
**Date:** 2026-09-19
**Phase:** Phase 2 gate consolidation (structural x4 + content x4)
**Fix authorization:** none; consolidation only. No source, task, ref, or originating report modified.
**Target source:** `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (S)
**Task file:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/TASK-RF-troubleshoot-generalize-20260919-015257.md` (T), Phase 2 = T:293–689; Phase 3 = T:690–987; Phase 4 = T:988–1081

## Overall Verdict: FAIL

All 8 reports independently return FAIL. All 8 agree the 52 Phase 2 items (2.1–2.51 + 2.27a) landed textually (zero omissions, zero legacy `H0–H5` tokens, zero forbidden names, protected near-twin intact). The failure is semantic: the composed SKILL has contradictory or unsatisfiable instructions, most of which were **prescribed verbatim by the task/research text** rather than introduced by the implementer.

### Counts

| Metric | Value |
|---|---|
| Source reports | 8 / 8 read in full |
| Raw findings across reports | 95 (12 + 13 + 10 + 11 + 14 + 9 + 12 + 14) |
| Consolidated unique issues | **27** (P2-F01 … P2-F27) |
| (a) Actionable in-scope SKILL.md defects | **25** (P2-F01–F25) |
| (b) Contradictory acceptance criteria — note, do not rewrite checklist | **2** standalone (P2-F26, F27) + 9 of the (a) items carry a (b) note |
| (c) Deferred / pre-existing / out of Phase 2 file scope | 4 clusters (Appendix) |
| Severity (highest preserved) | CRITICAL **5**, IMPORTANT **20**, MINOR **2** |
| Issues fixed | 0 |

**Gate status:** FAIL. Blocking: P2-F01, F02, F04, F18, F21 (CRITICAL) and every IMPORTANT item. F26/F27 are already-false acceptance predicates and cannot be made true without task-owner amendment.

## Source report inventory

Directory: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/qa/`

| # | Report file | Lens | Verdict | Issues (C/I/M) | Local IDs |
|---|---|---|---|---|---|
| R1 | `qa-phase-2-structural-template-report.md` | Template conformance | FAIL | 12 (0/9/3) | TC-01–TC-12 |
| R2 | `qa-phase-2-structural-consistency-report.md` | Internal consistency | FAIL | 13 (1/11/1) | IC-01–IC-13 |
| R3 | `qa-phase-2-structural-evidence-report.md` | Evidence quality | FAIL | 10 (0/10/0) | E01–E10 |
| R4 | `qa-phase-2-structural-completeness-report.md` | Completeness | FAIL | 11 (2/8/1) | F01–F11 (cited as Cm-Fnn) |
| R5 | `qa-phase-2-content-actionability-report.md` | Actionability | FAIL | 14 (3/11/0) | F01–F14 (cited as Ac-Fnn) |
| R6 | `qa-phase-2-content-metrics-report.md` | Numbers/metrics | FAIL | 9 (0/8/1) + 3 baseline notes | M1–M9 |
| R7 | `qa-phase-2-content-chain-report.md` | Cross-ref chain | FAIL | 12 (3/9/0) | F01–F12 (cited as Ch-Fnn) |
| R8 | `qa-phase-2-content-domain-report.md` | Domain accuracy | FAIL | 14 (1/13/0) | D01–D14 |

All eight reports state they read S in full (639 lines) and T:293–689 in full, consulted no peer report, and applied no fixes. Confidence in every report = 100% checklist coverage (not correctness).

## Consolidated issues — (a) actionable in-scope SKILL.md defects

Dedup rule: one row per underlying defect; severity = highest assigned by any report; all originating IDs listed. "Verbatim-pinned" = the defective text was prescribed word-for-word by T and/or research; a fix departs from the prescribed string but (unless noted) still satisfies the item's grep verification. Those rows carry a **(b) note**: the acceptance clause should be annotated, not the checklist rewritten.

| ID | Sev | S lines | Phase 2 items | Origin IDs | Expected vs actual | Required fix |
|---|---|---|---|---|---|---|
| P2-F01 | CRITICAL | 43, 64, 73, 259, 266, 474–476, 499 | 2.1, 2.14, 2.16, 2.20, 2.27a, 2.28–2.30, 2.44, 2.45, 2.50 | TC-01, IC-08, E10, Cm-F05, Ac-F10, M9, Ch-F07, D13 | Expected: `status: blocked` set by S1.6.4 / 3-round cap / capability verdict survives to Output Contract + footer + TFEP (`blocked ⇒ halt`). Actual: Wave 5 step 3 still says validator returns `success/partial`, unconditionally sets `partial` on any dropped citation; inline fallback and cosmetic finalize (step 3.5 option a) also assign `partial`; step 4.5 copies step-3 status. Blocked + dropped citation ⇒ `partial` ⇒ retry/escalate instead of halt. | Add one explicit monotone status-precedence rule in Wave 5 (`failed` > `blocked` > `partial` > `success`); apply it to validator result, citation-drop, inline fallback, and step 3.5(a); enumerate `blocked` in the caller's validator-result description; derive footer/TFEP from the merged status. |
| P2-F02 | CRITICAL | 248, 362 | 2.38, 2.47 | IC-03, E04, Cm-F02, Ac-F03, M2, Ch-F02, D08 | Expected: menu-equality gate is satisfiable by a complete, truthful prompt. Actual: compares *distinct enum values* in prompt to *count of `surviving=yes` rows*; two producers emitting the same token ⇒ 1 ≠ 2, spawn forbidden, no honest repair. | Compare sets of surviving producer identities (`file:line`/row IDs) in prompt vs table; keep enum-value coverage as a separate check. **(b) note:** rule text is verbatim-pinned by 2.38; grep `**Menu-equality check** before spawning` survives the fix. |
| P2-F03 | IMPORTANT | 171, 248, 258, 298, 362, 473 | 2.31, 2.42, 2.46, 2.47, 2.49 | IC-02, E03, Cm-F03, Ac-F04, M3, Ch-F03, D05 | Expected: zero-survivor recovery yields a usable candidate set. Actual: all rows become `surviving=re-opened`; every downstream selector (pair generation, control arm, card citation, UNDETERMINED `among {}`, RUN-SITE overwrite) accepts only `surviving=yes` ⇒ trigger fires with zero eligible rows; A7 still rejects sentinel. | Define one shared active-candidate predicate (`yes` or `re-opened`) used by every consumer, or transition re-opened rows back to `yes` with a separate contradiction annotation before consumers read the table. **(b) note:** 2.47 verbatim-pinned; grep `surviving=re-opened` ≥1 survives. |
| P2-F04 | CRITICAL | 248 | 2.47 | IC-04, E05, Cm-F01, Ac-F01, Ch-F01, D07 | Expected: primitive grep runs over producer source files. Actual: `$(cut -d'\|' -f1 producers.md \| sort -u)` over the whole Markdown yields empty fields / headings / `file:line` coordinates, never paths; relative `producers.md` ignores `<output-dir>`. Reproduced by 5 reports via shell counterexample. | Replace with a rule that parses only `## Producers` data rows, strips `:line`, dedupes, resolves against repo root, quotes paths, and uses `<output-dir>/producers.md`. **(b) note:** verbatim-pinned by 2.47/R-02. |
| P2-F05 | IMPORTANT | 248; `refs/primitive-differential.md:13–20,57` | 2.47 | E06, Ac-F02, Ch-F01 | Expected: "one pattern per row of the primitive-differential Section 1 table". Actual: that table has columns kind/exact form/reference form/control — no pattern column; only `read/parse` has an inline example; 5 kinds require invented patterns. | Either define the per-kind targeting rule in SKILL or replace the claim with a defined source-inspection step. Ref-side fix (adding a pattern column) is outside Phase 2 file scope — see Appendix C3. |
| P2-F06 | IMPORTANT | 474 | 2.29, 2.30 | TC-07, IC-09, E01, Cm-F08, Ac-F09, M7, Ch-F06, D12 | Expected: `artifact_mtimes={<abs path>: <ISO-8601 mtime>}` supplied before validator spawn. Actual: sole producer is `ls <all cited paths>` (names only, no mtimes), described *after* validator receipt. | Add a pre-spawn metadata step using a timestamp-bearing command (e.g. `date -u -r <path> +%Y-%m-%dT%H:%M:%SZ` per path, matching 2.41's `card_mtime` idiom, or `stat`); keep the later `ls` as existence check only. **(b) note:** 2.30 verbatim-pins "the same `ls` supplies `artifact_mtimes`"; item greps survive the fix. |
| P2-F07 | IMPORTANT | 454, 474 | 2.30 | TC-08 | Expected: draft materialised before its consumer. Actual: step 2 composes `REPORT.md`, step 3 passes `REPORT.md.draft`, receipt rule says "before touching `REPORT.md.draft`"; no explicit draft write step. | Add "write `REPORT.md.draft`" at end of step 2; reword receipt clause to "before modifying the draft / finalizing `REPORT.md`". Single-report finding; related to F06. |
| P2-F08 | IMPORTANT | 460; `refs/agent-assertions.md:14` | 2.32 | TC-06, IC-10, E09, Ac-F14, D14 (dissent: R6 §Boundary treats the exception as already explicit) | Expected: `n/a` legal on first instrumented run. Actual: same sentence says A6 rejects any value matching `if\|only\|/\|,`; `n/a` contains `/`; A6 row in ref has no exception. D14 adds: legitimate path literals also rejected. | Order the first-run `n/a` exemption before the A6 test in the sentence; pass a first-run indicator. Ref A6 row lacks the exception — Appendix C3. Item grep survives. |
| P2-F09 | IMPORTANT | 60, 258, 355, 367, 464 | 2.36, 2.39, 2.46 | TC-03, IC-07, Cm-F07, Ac-F11, Ch-F08 | Expected: `diagnosability_tasklist_path` points at any emitted tasklist. Actual: baseline row S:60 says `null` for sufficient/unknown/skipped; new paths (S1.6.4 write-then-recompute-to-sufficient; Wave 3 step 1/4.5 create-if-absent) emit a real file hidden by the null rule. | Edit S:60 (baseline, not pinned): populate whenever the artifact was emitted this run; `null` only when absent. Route pending rows into Next Steps on every creation path. |
| P2-F10 | IMPORTANT | 367, 384, 393, 402 | 2.34, 2.36 | TC-04, IC-12 | Expected: `split-pending` persists in `candidate-fixes.md`. Actual: index vocabulary is `consensus / competing / outlier` only. | Add `split-pending` to the disposition list (baseline text) and carry it through Wave 4 eligibility filter. |
| P2-F11 | IMPORTANT | 248, 258 | 2.46, 2.47 | TC-05, M8 (dissent: R6 check 8 treats the 8-row/8-pair budgets as distinct stages) | Expected: one probe cardinality unit. Actual: S1.6.0b "at most 8 rows" (one pair per hit) vs S1.6.4 "8 pairs" + control + up to 2 extra rows; `probe-rows-truncated: <n>` unit (pairs vs rows) undefined. | State one limit, define pair vs row vs control counting, define `n` with a 10-pair/8-retained example. |
| P2-F12 | IMPORTANT | 476, 574–575, 615 | 2.17, 2.18, 2.27 | TC-09, IC-13, M4 | Expected: one enforcement semantics for the cosmetic counter. Actual: step 3.5 = "a nudge, never a halt"; Will Not Do forbids halting on it; Token Cost Profile = "the one hard cap". | Replace "the one hard cap" with a non-blocking threshold description. **(b) FUNDAMENTAL:** 2.17 verification `grep -cF 'The cosmetic counter is the one hard cap' == 1` makes this fix fail the checklist. Requires task-owner amendment of 2.17. |
| P2-F13 | IMPORTANT | 476, 478–509, 568, 574–575 | 2.24, 2.27 | Ac-F12, Ch-F12 | Expected: any exit runs validation → footer → return contract. Actual: step 3.5 option (a) "finalize `REPORT.md` as-is … and stop" precedes footer (step 4), `cosmetic_overrun` value, and step 4.5 TFEP; counter also applies in Wave 3, so (a) can fire before the mandatory validator. | Change (a) to "stop cosmetic work and jump to the common epilogue (validation → status merge → footer → return contract)". **(b) note:** 2.27 body verbatim-pinned; heading grep survives. |
| P2-F14 | IMPORTANT | 258, 355, 537, 551 | 2.23, 2.46 | TC-10, IC-06 | Expected: tool matrix permits the S1.6.4 (Tier 1) behaviour-definition fetch. Actual: S1.6.4 mandates the Wave 3 fetch (Context7 → WebFetch → raw) before writing a pair; Tool Coordination marks Context7 `—` in Tier 1; Will Do says Context7/Tavily "only in Tier 2". | Add the conditional S1.6.4 fetch to the Tier 1 Context7 cell and carve out behaviour-definition fetching in the Will Do tier restriction (both baseline text). |
| P2-F15 | IMPORTANT | 258, 298–300, 351–365 | 2.37, 2.39, 2.41, 2.46 | IC-05, E07, Cm-F06, Ac-F08, Ch-F05, D10 | Expected: every unobserved primitive claim has a definition row before calibration. Actual: fetch sits in Wave 3 step 1 (parallel with spawn) and needs the card's verb phrase; Tier 2 cards arrive at step 3 and go straight to 3.5 calibration; S1.6.4's early call has producer rows, not cards. | Make the procedure accept a card OR a producer assertion; add a post-receipt/pre-calibration binding pass (steps 3 → 3.5) in both tiers; reuse fetched rows. **(b) note:** T placed the fetch at "Wave 3 step 1"; the item's grep survives relocation/duplication. |
| P2-F16 | IMPORTANT | 172, 176–182 | 2.49 | IC-01, E08, Cm-F10, Ac-F05, Ch-F10, D01 | Expected: SAME-ENV derived from evidence. Actual: pasted-log bullet unconditionally sets `SAME-ENV: yes`, `OBSERVE-VIA: same-shell`, no deltas ref — a pasted remote-CI/prod log satisfies both the derivation rule (`no`) and the shortcut (`yes`). | Restrict the shortcut to proven local single-process observations; otherwise use the normal derivation. **(b) note:** 2.49 block is mandated VERBATIM (T:652); no grep pins this line, but the "verbatim" instruction is contradicted by any fix. Also present in `research/03-spec-extraction.md:130`. |
| P2-F17 | IMPORTANT | 173, 178–179, 184, 258 | 2.46, 2.48, 2.49 | Ac-F06, Ch-F09, D02 | Expected: `OBSERVE-VIA` = how output can be *read*. Actual: S1.6.4(iii) orders probes to *run* via every value except `nobody`; `artifact-file` (a downloaded log from a finished job) cannot execute anything. | Separate read-venue from execution-transport; for `artifact-file`, consume existing captured evidence and leave rows pending with a could-not-run reason. **(b) note:** verbatim-pinned (2.46 Edit 1 / 2.49). |
| P2-F18 | CRITICAL | 64, 258–261, 562, 571 | 2.1, 2.45, 2.46 | Cm-F04, D03 | Expected: a known `re-run permitted: no` is honoured before any execution; fixes need confirmation. Actual: clause (iii) runs rows whenever venue ≠ nobody; refusal is checked only inside the insufficient/non-trivial hard-stop branch; clause (ii) ships a `## Fix candidate` in the same rerun; partial/trivial/no-escalate routes never reach the refusal branch, bypassing `blocked-on-authorization`. | Apply refusal/authorization state before execution; run only read-only diagnostic rows; leave fix diffs as proposals; make `blocked-on-authorization` precedence independent of the rubric branch. Item grep `Status precedence: emitters found ∧ ...` survives. |
| P2-F19 | IMPORTANT | 258–263 | 2.45, 2.46 | Ac-F07, M6, D06 | Expected: a branch for probes that ran but left the verdict `insufficient`. Actual: (iii) recomputes the verdict; hard-stop bullet says it is reached "only if rows could not run or `OBSERVE-VIA = nobody`"; executed-but-inconclusive has no route. | Add an explicit ran-but-still-insufficient transition (status + next wave); branch on the recomputed verdict, not on execution success. Reconcile the same clause in `research/07-gap-fill-reconcile.md` D4 Edit 2. |
| P2-F20 | IMPORTANT | 131, 266, 284, 603; `commands/troubleshoot.md:56` | 2.19, 2.44 | IC-11, Cm-F09, M1, D09 | Expected: 3-round cap accumulates across invocations for one `<branch>:<repro-venue-id>`. Actual: counter file lives in `<output-dir>/diagnosability-rounds.json`; default output dir is timestamped; no prior-state lookup ⇒ every run is round 1. Digit-stripping also conflates distinct jobs (D09). | Define a stable counter location or an explicit prior-run lookup/merge before increment; keep per-run snapshot and reset semantics. **(b) note:** 2.44 paragraph verbatim from reconcile gap-7(c); no planned Phase 3/4 item addresses storage location (3.17 repeats the same design) — design decision needed. |
| P2-F21 | CRITICAL | 248, 298, 454, 473 | 2.31 | E02, Ac-F13, Ch-F11, D11 | Expected: headline value must be *observed* in the failing run. Actual: `grep -F` over "every `<output-dir>` artifact and every `job-*.log`" — includes `producers.md`, hypothesis cards, and the report draft, all of which contain the enum by construction ⇒ the gate certifies its own prose. | Restrict the observation corpus to captured run outputs with run/arm provenance (job logs, probe observations); exclude generated artifacts. **(b) note:** verbatim-pinned by 2.31; both item greps survive. |
| P2-F22 | IMPORTANT | 76, 473, 499 | 2.27a, 2.31 | TC-02 | Expected: UNDETERMINED ⇒ `root_cause_summary` = "". Actual: step 4.5 unconditionally sources `root_cause_summary` from REPORT.md Diagnosis, which now holds non-empty UNDETERMINED/falsifier prose. | In step 4.5, copy the already-derived contract field or state the empty-string override for the UNDETERMINED form. |
| P2-F23 | IMPORTANT | 241, 279, 298, 362, 473–474 | 2.31, 2.38, 2.42 | Ch-F04 | Expected: supported `--no-diagnosability-audit` bypass still executes. Actual: bypass skips the only `producers.md` writer; Tier 1 conditions the paste on existence, but Tier 2 prompt unconditionally requires the full table + menu gate, and low-confidence Wave 5 copies producers/tasklist falsifiers. | Condition Tier 2 paste/menu check and the UNDETERMINED form on artifact existence, or write a minimal `producers.md` outside the skipped wave. |
| P2-F24 | IMPORTANT | 179 | 2.49 | D04 | Expected: verdict-source rule applies to CI jobs. Actual: `OBSERVE-VIA = artifact-file` (any captured file: stderr dump, XML, crash log) mandates `job-<id>.log` download and converts missing marker to FAIL. | Scope job-log retrieval to identified CI jobs; other artifacts keep their provenance; missing marker ⇒ `unobservable`/unknown, never a synthetic FAIL for non-CI artifacts. **(b) note:** verbatim block (2.49). |
| P2-F25 | IMPORTANT | 476, 488, 497 | 2.24, 2.27 | M5 | Expected: `cosmetic_overrun=<n>` has a unit. Actual: at a streak of 10, `n` could be 10, 5, or 1; footer "highest overrun value" cannot aggregate. | Define `n` (e.g. streak length at re-fire), the initial event, and footer aggregation with a 5/10/15 trace. |

## (b) Contradictory acceptance criteria — annotate, do not rewrite the checklist

| ID | Sev | T lines | Items | Origin IDs | Contradiction | Note to record |
|---|---|---|---|---|---|---|
| P2-F26 | MINOR | T:428 vs T:517 | 2.18, 2.30 | TC-11, Cm-F11, E03 (exclusions §), R7 ledger | 2.18 verifies `grep -cF 'git log --format=%cI' == 1`; 2.30 intentionally inserts a second occurrence (S:474, 578). Final file = 2. Both insertions are required. | 2.18's count was true at its execution point; record "final-file count is 2 by design of 2.30". Do not delete either line. |
| P2-F27 | MINOR | T:647 vs T:664 | 2.48, 2.49 | TC-12, Cm-F11, E03 (exclusions §) | 2.48 verifies `grep -cF 'no repro available: run-site unobservable' == 1`; 2.49's verbatim block repeats it (S:178, 184). Final file = 2. | Same: intermediate-witness count; record final count 2. Do not remove either guard. |
| (see P2-F12) | IMPORTANT | T:419–421 vs T:489 | 2.17, 2.27 | TC-09, IC-13, M4 | 2.17 pins and greps "The cosmetic counter is the one hard cap"; 2.27 pins "a nudge, never a halt". Fixing S breaks 2.17's grep. | Task-owner must amend 2.17's wording/verification before the SKILL fix lands. |

Verbatim-pinned rows above whose fix survives their grep but departs from the "verbatim" instruction: P2-F02, F03, F04, F06, F13, F15, F16, F17, F21, F24. Recommend one blanket authorization note: "Phase 2 verbatim blocks may be amended per qa-phase-2-consolidated-findings.md P2-Fnn; item greps remain the verification."

## Fundamental contradictions preventing automatic fixes

1. **P2-F12 / item 2.17** — the only case where a SKILL fix necessarily fails a pinned `grep == 1` verification. Cannot be auto-fixed without task amendment.
2. **P2-F26, P2-F27** — verification predicates that are already false in the final file by the task's own design; no SKILL change can satisfy both items. Task note required.
3. **Verbatim-block mandate (2.46, 2.47, 2.49; T:624, 638, 652)** — 10 of 25 fixes edit text the task says to paste VERBATIM. Greps survive, the instruction does not. Needs explicit authorization, not a checklist rewrite.
4. **P2-F20** — correct fix likely needs a stable-storage design that touches `commands/troubleshoot.md` (Phase 4 file; no planned item covers it) or a new lookup rule. Design decision, not a mechanical edit.
5. **P2-F05, P2-F08** — the complete fix straddles Phase 1 refs (`primitive-differential.md` pattern column; `agent-assertions.md` A6 exception) that no Phase 3/4 item edits. SKILL-side mitigation is possible; ref-side needs a new item.

## Cross-report agreement matrix (top clusters)

| Consolidated | Reports agreeing | Independent counterexample executed |
|---|---|---|
| P2-F01 blocked→partial | 8 / 8 | trace only |
| P2-F02 menu equality | 7 / 8 | R3, R4 (stdlib count) |
| P2-F03 re-opened rows | 7 / 8 | R3 (stdlib) |
| P2-F06 mtimes via `ls` | 8 / 8 | R3, R5, R6, R7, R8 (`ls` on S) |
| P2-F04 `cut` extraction | 6 / 8 | R3, R4, R5, R7, R8 (shell) |
| P2-F15 fetch ordering | 6 / 8 | trace only |
| P2-F16 pasted-log locus | 6 / 8 | trace only |
| P2-F08 first-run `n/a` | 5 / 8 (+1 dissent) | R3, R5 (regex) |
| P2-F09 tasklist pointer | 5 / 8 | trace only |
| P2-F21 circular headline | 4 / 8 | trace only |
| P2-F20 counter persistence | 4 / 8 | R6, R8 (Grep of CMD default) |

## Appendix — (c) Excluded, deferred, and follow-up

### C1. Explicitly excluded by all 8 reports (planned Phase 3/4 work, not Phase 2 defects)

- HC0–HC5 renames inside ref bodies — items 3.6–3.14.
- `contract_version` / `blocked` in HOC, RT — 3.15, 3.16.
- diagnosability-audit.md counter prose, S1.6.4a section order, tasklist header keys, task type 5/6, constraints 5/6, S14 row — 3.17–3.24 (S14 cross-reference in S is intentional per R1).
- report-template UNDETERMINED form, "probable" ban, Next Steps hard-stop line, timestamp rule — 3.25–3.27.
- HCT discriminator form, `runs-in=`, `behaviour-definition: row N`, producer-row citation — 3.28–3.32.
- triage/escalation-rubric additions — 3.33–3.37.
- Calibrator/validator kwargs, C-rule/A-rule sections, `blocked` status decision, `split_pending` — 4.1–4.10.
- Command file — 4.11, 4.12.
- Tests (Phase 7+), sync-dev/verify-sync (Phase 5).

### C2. Pre-existing baseline defects noticed (R6 "Baseline-only observations"; not Phase 2 failures)

| Ref | S line | Observation | Disposition |
|---|---|---|---|
| R6-B1 | 299 | "5-dimension rubric" but rubric has six dimensions. | Separate cleanup; no Phase 2/3/4 item. |
| R6-B2 | 377 | Force-degrade: out-of-range confidence → 0.0 vs clamp-then-bound (1.2 ⇒ 0.0 or 0.65); `min(x,0.65)` called a floor. Also in main-tree baseline. | Separate cleanup. |
| R6-B3 | 319 | Abbreviated Wave 2 summary omits rubric's security 0.95 threshold. | No change; rubric is authoritative. |

### C3. Follow-ups outside Phase 2 file scope but created by this task (no planned item)

| Ref | File | Need | Linked |
|---|---|---|---|
| FU-1 | `refs/primitive-differential.md` (Phase 1) | Section 1 has no pattern column; footer references one. | P2-F05 |
| FU-2 | `refs/agent-assertions.md` A6 (Phase 1) | No first-instrumented-run `n/a` exception. | P2-F08 |
| FU-3 | `research/07-gap-fill-reconcile.md` D4 Edit 2, gap-7(c); `research/03-spec-extraction.md:130, 425–435` | Research encodes P2-F16, F19, F20, F08 defects; should be reconciled so Phase 3 items (3.17, 3.17a) do not re-propagate them. | P2-F08, F16, F19, F20 |
| FU-4 | Planned test phase (Phase 7) | Add the counterexamples every report lists: duplicate-token producers, re-opened rows, bordered Markdown table extraction, first-run `n/a`, post-spawn Tier 2 mechanism, pasted multi-arm log, artifact-only access, refused reachable rerun, blocked + dropped citation, blocked + validator crash, late tasklist after sufficient audit, three fresh output dirs, 10-pair/8-retained truncation, enum present only in a hypothesis. | all |

### C4. Rejected / non-findings (recorded so they are not re-raised)

- `<kind>`, `<output-dir>`, `<N>`, enum alternatives — intentional placeholders (R1).
- S14 sufficiency-row cross-reference — assigned to Phase 3 (R1).
- Markerless CI log — Output Contract already classifies as blocked (R4 self-audit).
- 8-row vs 8-pair budgets as separate stages (R6 check 8) — recorded as dissent on P2-F11; P2-F11 retained because R1 TC-05 and R6 M8 show the units are still undefined.
- First-run `n/a` precedence "already explicit" (R6 §Boundary) — recorded as dissent on P2-F08; retained on 5-report majority with two regex counterexamples.

## Actions Taken

1. Wrote this file header first, then the body.
2. Read all 8 reports in full, T:293–689 in full, Phase 3/4 item headers (T:690–1081), and T:1068–1081.
3. No source, task, research, ref, or originating report modified.

## Cycle 1 independent verification — consolidated residuals

VERDICT: FAIL. Failure set shrank from 27 to 2; no distinct new issues or independently accepted PASS regressions. Sources: `qa-phase-2-verification-structural-cycle-1.md` and `qa-phase-2-verification-content-cycle-1.md`. Their actual findings supersede the fixer's self-reported PASS. User authorized semantic corrections and downstream override notes.

| ID | Severity | Sources | Remaining defect | Required fix / witness |
|---|---|---|---|---|
| P2-F11 | IMPORTANT | structural + content verification | The 19-row maximum omits optional pack additions. The existing three-row read/parse pack can make 22 rows. | Define whether 19 bounds core rows or all rows; separately bound and account for informational pack rows without discarding mandatory discriminators. Align SKILL, primitive ref, and downstream ledger; demonstrate a full core budget plus existing three-row pack. |
| P2-F23 | IMPORTANT | content verification (structural missed this Tier 1 path) | Tier 1 rejects cards lacking producer citations even when audit bypass means no producer menu exists. | Condition the Tier 1 rejection on a nonempty existing producer menu. With no menu, retain ordinary grounding/calibration and log bypass. Bind future bypass tests to exercise Tier 1 before Tier 2. |

Cycle 2 fixes must preserve the 25 independently accepted findings and use one serialized fixer. Final release still requires both verification lenses PASS.

## QA Complete
