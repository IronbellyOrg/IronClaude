# QA Report — Research Gate Fix-Cycle Verification (Qualitative), repeat cycle 1

**Topic:** Orchestrator mode Phase 1 (issue #339) — research coherence after the second (last) fix pass
**Date:** 2026-11-07
**Phase:** fix-cycle (qualitative, report-qualitative lens)
**Fix cycle:** 2 (repeat cycle 1; findings `qa/qa-consolidated-findings-phase3-cycle1.md`, fix log `qa/qa-research-fix-log-cycle1.md`)
**Fix authorization:** false (no research file edited)

---

## Overall Verdict: FAIL

Open blocking findings: 1 (NB-4, new). NB-1, NB-2 and NB-3 are resolved, so B-05 and B-13 now hold. No fix in this pass reopens a finding the previous qualitative report marked RESOLVED. No fix breaks WC-10, and none builds on option A4. NB-4 is a cross-file contradiction that the NB-2 rewrite of the `scope-03:99` allowlist carries: the allowlist forbids every Orca verb it does not list, and it does not list `task-list`, which Section C rule 4(b) requires. `run-list` and `gate-list` are also missing, and other files name them as sweep sources.

Sources read: `qa/qa-consolidated-findings-phase3-cycle1.md`, `qa/qa-research-fix-log-cycle1.md`, the previous report `qa/qa-research-verification-qualitative.md`, `qa/qa-research-fix-log.md:37` and `qa/qa-consolidated-findings-phase3.md:34` (the cycle-0 B-13 text), and the research files at every edited location: `research-notes.md:88-90`, `:136-138`, `:150-229`, `:266-275`, `:326-333`; `05:160-182`; `06:66-75`, `:128-139`, `:154-189`; `07` (whole file); `scope-01:60-64`; `scope-02:80-109`, `:236-243`; `scope-03:70-111`, `:141-151`, `:200-212`; `scope-04:314-347`. Also the handler `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-check-handler.js` (read-only `grep -n`, lines 18, 19, 30) and `src/superclaude/core/WORKER-CONTRACT.md:60` (WC-12).

## Cycle-1 findings: status

| ID | Status | Evidence (re-read this cycle) |
|---|---|---|
| NB-1 (B-05) | RESOLVED | `research-notes.md:193` rule 2 now carries the "Fenced exclusion": it matches only when there is no `consumer_fenced` evidence in the transcript or the `check` result. With that evidence present, rule 3 (`:194`) sets the class. Rule numbers 1-7 are unchanged, so the citations at `scope-04:320` and `scope-02:86` still hold. Copies match: `05:172` (stalled needs no fenced evidence), `05:173` (fenced "takes the row even when liveness is `exited`"), `06:137` (with that evidence the row is fenced), `scope-02:107` (the first-draft bullet, now excluded) and `scope-01:62`. WC-12 text confirmed at `WORKER-CONTRACT.md:60`. |
| NB-2 (B-13) | RESOLVED | `scope-03:99`. (1) `check --peek` and `check --all` are now two separate argv, and any argv with two or more read modes is forbidden. This matches the handler at `message-check-handler.js:18-19` (grep this cycle: `filter(Boolean).length > 1` and "Choose at most one message read mode"). (2) The default allowlist has no `check`. Both `check` modes are additions gated on 06 constraints (2) and (3) (`06:72`) and Gap 18 (`06:175`), and "any `check` while the probe gate is unsettled" is forbidden. This matches `06:72`, "Until (2) and (3) are settled the design default is the contracts-only fallback". (3) Read-marking is tagged [UNVERIFIED] and cited to `06` Gap 1 (`06:158`). The mutation-path citation `:30` matches the handler grep. |
| NB-3 (B-19 propagation) | RESOLVED | `research-notes.md:157` (A1) now says PATH first, uses the `uv run` form only as the dev-checkout fallback, and lists both forms in `allowed-tools`. `scope-03:209` (OQ4) and `scope-03:109` list both forms. A grep of `superclaude sweep\|uv run superclaude` over `research/` finds no uv-only decision left. `research-notes.md:90`, `:138` and `:273` describe the precedent in other skills or the original gap; none is a sweep decision. `scope-03:76` names only the PATH form, which agrees with OQ3 at `:208`. |

## Previously RESOLVED findings (from `qa-research-verification-qualitative.md`): reopen check

| ID | Still resolved? | Evidence |
|---|---|---|
| B-01 | Yes | `research-notes.md:188` is still the one canonical vocabulary. `05:167` and `scope-02:99` still defer to it. |
| B-02 | Yes | `research-notes.md:192` (rule 1: the contract is read first, and blocked is never finished) is unchanged. `05:171` agrees. |
| B-12 | Yes | `scope-04:320-332` is unchanged. The precedence list at `:320` still matches rule numbers 1-7. |
| B-22 | Yes | `06:72`, `:158` and `:159` still give the check modes as help-documented and runtime read-marking as UNVERIFIED. |
| B-24 | Yes | The `07` C(a)-(g) table (`07:57-65`) is unchanged, and `06:72` constraints (1)-(4) are intact. |
| B-26 | Yes | `scope-02:103` and `:237` still give safe-to-close as a two-part dimension. |
| B-27 | Yes | `scope-03:143-150` still lists lint-architecture Checks 1-11. |
| B-28 | Yes | The edited `06:137` and `05:172-173` use only canonical class names (stalled (proved), fenced, could not determine, working, waiting on a person). |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| NB-4 | IMPORTANT (cross-file contradiction; wrong behaviour) | `scope-03-cli-patterns.md:99` (B-13 argv allowlist, rewritten for NB-2) versus `research-notes.md:172`, `:197`; `05-orca-row-schema.md:175`; `scope-04-409-layout.md:330`, `:339`, `:345`; `07-gate-gap-fill.md:41-47` | The default allowlist is `worker-list`, `worker-show`, `worker-read` and `worktree ps` without `--agent-wait`. The forbidden list ends with "any verb not on the allowlist", so the test fails if one of those verbs is called. Other files need verbs that the allowlist omits. Section C rule 4(b) (`research-notes.md:197`) reads a foreign ready Task "from `task-list --ready`", and `05:175` and `scope-04:330` repeat that. The scope-04 Owner column takes the Run id from `run-list` (`:339`), and the Approval candidate comes from `gate-list` (`:345`). `research-notes.md:171-173` and `07` B list `run-list`, `run-current`, `task-list` and `gate-list` as read sources the sweep uses (all plain `client.call` reads on the CLI side). A plan built from `scope-03:99` either drops "waiting on a person" kind (b) for foreign ready Tasks and loses the Owner source, or ships a test that fails on the first `task-list --ready` call. The gap dates from the cycle-0 B-13 fix (`qa-research-fix-log.md:37` already says "any other verb"). The NB-2 rewrite in this pass restated the default allowlist and the catch-all without adding these verbs, and the previous review did not catch it. | Add `orchestration task-list` (with `--ready` and `--run <id>`), `orchestration run-list`, `orchestration run-current` and `orchestration gate-list` to the default allowlist at `scope-03:99`. Cite `07-gate-gap-fill.md` B for each one being a plain read on the CLI side, and keep `inbox` forbidden. Or, if a verb is left out on purpose, say so at `scope-03:99`, then remove that verb as a source from `research-notes.md` rule 4(b) and Section B, `05:175` and `scope-04:330`, `:339`, `:345`. |

### Minor notes (non-blocking; not rechecked in later cycles)

- `research-notes.md:193` rule 2: the fenced exclusion is keyed on "no `consumer_fenced` evidence in the transcript or `check` result". It does not say what happens when an `exited` row's transcript cannot be read. Under first-match precedence, rule 2 then fires before rule 7's "unreadable log" (`:200`), so a fenced worker with an unreadable transcript would read stalled. The plan should state that, for an `exited` row with no `worker_done` and an unreadable transcript, the class is could not determine. This is not a WC-10 break, because `exited` is positive stop proof.
- `scope-03:99` mixes verb forms: it writes `orchestration check --peek` but bare `worker-list` / `worker-show` / `worker-read`. C13 (`research-notes.md:331`) says every orchestration verb is `orca-ide orchestration <verb>`. A test pinning argv must use the full form.
- The previous minor notes stand and were not rechecked. A grep confirms the G-A label at `research-notes.md:175` and `:196` is still unchanged.

## WC-10 and option A4 checks

- **WC-10 (absence of a signal is never proof of death): HOLDS.** The NB-1 exclusion only narrows rule 2. Rule 2 still needs positive stop proof (`research-notes.md:193`), and rule 3 still sends a settled row with no `worker_done` and no fenced evidence to could not determine (`:194`). Rule 5 still says a null `agentWait` is never stall proof (`:198`), and rule 7 still treats absence as could not determine (`:200`). `06:137` still says the sweep "never infers 'stalled' from silence or a late heartbeat". The NB-2 fix makes the default more conservative (no `check` call at all), and `06:73` still turns a truncated listing into could not determine.
- **Option A4: NOT BUILT ON.** `research-notes.md:160` still tags A4 CODE-CONTRADICTED, and `:162` borrows only the report shape and the SAFE/REVIEW vocabulary, "without its scripts". `scope-02:241` adds no A4 dependency. No edit in this pass names `bootstrap_scan.sh`, the 72 h window or the crash-recovery allowed-tools as an input.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | B-01 single canonical vocabulary | PASS | `research-notes.md:188`; `05:167`; `scope-02:99` |
| 2 | B-02 contract read first, blocked is not finished | PASS | `research-notes.md:192`; `05:171` |
| 3 | B-05 fenced is never stalled (NB-1) | PASS | `research-notes.md:193-194`; `05:172-173`; `06:137`; `scope-02:107`; `WORKER-CONTRACT.md:60` |
| 4 | B-12 every class has a report home | PASS | `scope-04:320-332` |
| 5 | B-13 Orca read-only proof test (NB-2) | PASS | `scope-03:99` against `message-check-handler.js:18-19`, `:30`; `06:72`, `:158`, `:175` |
| 6 | B-22 check-mode wording | PASS | `06:72`, `:158-159` |
| 7 | B-24 relabel | PASS | `07:57-65`; `06:72` |
| 8 | B-26 safe-to-close is a dimension | PASS | `scope-02:103`, `:237` |
| 9 | B-27 lint-architecture checks | PASS | `scope-03:143-150` |
| 10 | B-28 vocabulary used everywhere | PASS | `05:169-178`; `06:137`; `scope-04:316` |
| 11 | No new cross-file contradiction from fixes (NB-3 now resolved) | FAIL | NB-3 resolved (`research-notes.md:157`; `scope-03:109`, `:208-209`), but NB-4 is open: `scope-03:99` against `research-notes.md:172`, `:197`; `05:175`; `scope-04:330`, `:339`, `:345`; `07:41-47` |
| 12 | WC-10 intact | PASS | `research-notes.md:193-200`; `06:73`, `:137` |
| 13 | Nothing builds on A4 | PASS | `research-notes.md:160-162`; `scope-02:241` |
| 14 | `07-gate-gap-fill.md` consistent with what cites it | PASS | `research-notes.md:171-173` cite `07` B correctly; `scope-03:99` cites `07` only through `06`, and its handler lines (`:18-19`, `:30`) match `07` C(a), (c). NB-4 concerns `scope-03`'s own allowlist, not a misquote of `07`. |

**Items that PASS:** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14. Item 11 fails. No item that passed in the previous qualitative report fails now. Items 3 and 5 moved from FAIL to PASS, and item 11 stays FAIL, now because of NB-4 instead of NB-3.

## Summary

- Checks passed: 13 / 14
- Checks failed: 1 (item 11, NB-4)
- Critical issues: 0. Important (blocking): 1. Minor notes: 2 new.
- Issues fixed in-place: 0 (fix authorization false)
- Open blocking count: **1** (previous |F_1| = 3). The count is going down.
- Original findings still open: none of B-05, B-13 or B-19. NB-4 is a new finding, left by the cycle-0 B-13 fix and restated by the NB-2 rewrite in this pass.

## Recommendations

- This was the last allowed fix pass (cap: 2 fix cycles, 3 reviews). Do not run a fourth review. Escalate NB-4 to the user under the cycle-control rule at task-file line 180.
- The cheapest fix for NB-4 is one edit at `scope-03:99`: add `orchestration task-list`, `run-list`, `run-current` and `gate-list` to the default allowlist, cited to `07` B.

## Confidence

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 9 | Glob: 1 | Bash: 1 (read-only `grep -n` of `message-check-handler.js` and `WORKER-CONTRACT.md`; no orca, ccsession, sweep or close command run)
- Web research: none performed, so the Tavily-first rule did not apply.
- UNCHECKED items: none. UNVERIFIABLE items: none.

## Self-Audit

1. Factual claims verified independently: 14 checklist items, plus about 35 file:line citations re-read in this cycle. These cover every edit location in the fix log, the eight previously resolved findings, and the `task-list`, `run-list` and `gate-list` source citations in four files.
2. Files read: the cycle-1 findings file, the cycle-1 fix log, the previous qualitative report, the cycle-0 fix log line 37, the cycle-0 findings line 34, `research-notes.md`, `05`, `06`, `07`, `scope-01`, `scope-02`, `scope-03`, `scope-04` (at the ranges listed above), `message-check-handler.js` and `WORKER-CONTRACT.md:60`.
3. Not a zero-issue review: 1 blocking finding and 2 minor notes, each cited at file:line.
4. No web research was done.

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` was supplied, so this review ran standalone. The fix log's "FIXED" claims were used only as pointers, and every fix was re-read at its file:line.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Handler read-mode rule: a `grep -n` of `message-check-handler.js` shows lines 18-19 (at most one read mode) and line 30 (mutation path). These support the NB-2 fix.
- Allowlist completeness: a grep of `task-list|run-current|run-list|gate-list` over `research/` finds no hit in `scope-03`, while `research-notes.md:172`, `:197`, `05:175`, `scope-04:330`, `:339`, `:345` and `07:41-47` use those verbs. This is the evidence for NB-4.
- Fenced precedence: `research-notes.md:193-194` was read against `WORKER-CONTRACT.md:60` (grep this cycle) and the four mirrored copies (NB-1).
- B-19 propagation: every `superclaude sweep` / `uv run superclaude` hit in `research/` was checked for a uv-only decision; none is left (NB-3).

## QA Complete

## Verdict: FAIL
