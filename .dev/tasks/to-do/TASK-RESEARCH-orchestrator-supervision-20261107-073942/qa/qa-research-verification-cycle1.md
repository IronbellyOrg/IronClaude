# QA Report — Research Gate Fix-Cycle Verification, repeat cycle 1 (Agent 1, rf-qa)

**Topic:** Orchestrator mode Phase 1 (issue #339), research gate
**Date:** 2026-11-07
**Phase:** fix-cycle
**Fix cycle:** 2 (repeat cycle 1; second and last fix pass)
**Fix authorization:** false (no research file edited)
**Inputs:** `qa/qa-consolidated-findings-phase3-cycle1.md` (NB-1, NB-2, NB-3; |F_1| = 3), `qa/qa-research-fix-log-cycle1.md`, the research files the findings and fix log name, and the 28 RESOLVED findings in `qa/qa-research-verification.md` (regression check)

Status: COMPLETE (written incrementally)

## Overall Verdict: PASS

---

## Per-finding verification (NB-1 to NB-3)

| ID | Status | Evidence |
|----|--------|----------|
| NB-1 (keeps B-05 open) | RESOLVED | Source re-read: `WORKER-CONTRACT.md:60` (WC-12) "if `check` returns `consumer_fenced` it stops without sending `worker_done`". `research-notes.md:193` rule 2 now carries "**Fenced exclusion (second fix pass, NB-1):** rule 2 matches only when there is **no `consumer_fenced` evidence** in the worker's transcript or `check` result ... with fenced evidence present, rule 2 does not match and rule 3 sets the class". Rule 3 (`:194`) unchanged ("never stalled and never finished"), so first-match precedence no longer sends an exited fenced worker to stalled. Mirrors re-read: `05-orca-row-schema.md:172` (stalled row adds "and no `consumer_fenced` evidence") and `:173` (fenced "Takes the row even when liveness is `exited` with no `worker_done`"); `06-orca-open-questions.md:137` (superseded mapping now "with no `consumer_fenced` evidence ... -> stalled (proved); with that evidence the row is fenced"); extra copy `scope-02-orca-recovery.md:107` ("never when the transcript or `check` result shows `consumer_fenced`"). Remaining `\bstalled\b` hits (20 across 6 files) checked: `scope-02:86`, `scope-01:60,62,81`, `scope-04:316,320,332` either cite Section C precedence or say fenced is never stalled; none derives stalled without the exclusion. Rule numbering 1-7 kept stable, so `scope-04:320` and the `research-notes.md:206-214` table stay valid. |
| NB-2 (keeps B-13 open) | RESOLVED | Source re-read: `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-check-handler.js:18-19` (`if ([flags.has('unread'), peek, flags.has('all')].filter(Boolean).length > 1) { throw ... 'Choose at most one message read mode: --unread, --peek, or --all.'`) and `:30` (`callOrchestrationMutation`). `scope-03-cli-patterns.md:99` now: (1) the combined "`check --all` (with `--peek`)" entry is gone; `check --peek` and `check --all` are "two **separate** argv, never combined", and the forbidden list adds "any argv with two or more of `--unread`/`--peek`/`--all`", citing `:18-19` correctly; (2) the default allowlist is `worker-list`, `worker-show`, `worker-read`, `worktree ps` without `--agent-wait`, with "no `check` call at all", and `check --peek`/`--all` are "Gated additions" allowed only after the probe settles `06:72` constraints (2) and (3); the forbidden list adds "any `check` while the probe gate is unsettled". Matches `06-orca-open-questions.md:72` ("Until (2) and (3) are settled the design default is the contracts-only fallback") and Gap 18 (`:175`); (3) read-marking now "plain `check` may mark messages read, [UNVERIFIED] per `06-orca-open-questions.md` Gap 1 (`:158`)", which matches `06:158`. Cross-file: `07-gate-gap-fill.md:59-71` and `scope-04:357` agree (probe-gated `--peek`, any `check` possibly state-changing, Orca questions "could not determine"). |
| NB-3 (introduced by the B-19 fix) | RESOLVED | Decision source re-read: `scope-03-cli-patterns.md:208` (OQ3: bare `superclaude sweep ...` on PATH first, `uv run superclaude sweep ...` dev-checkout fallback, both in `allowed-tools`). `research-notes.md:157` option A1 now says the skill "calls the installed entry point `superclaude sweep ...` on PATH first, with `uv run superclaude sweep ...` as the fallback only inside a dev checkout ... and `allowed-tools` lists both forms"; its Cons cell flags the bare PATH form from a non-uv project as UNVERIFIED until a `superclaude sweep --help` run, consistent with OQ3. `scope-03:209` (OQ4) lists both `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)`; extra copy `scope-03:109` pins both colon-form patterns. Grep of `superclaude sweep` over `research/`: hits only at `research-notes.md:157`, `scope-03:76,109,208,209`; every `uv run` occurrence sits beside the bare form, and `scope-03:76` names only the PATH form (consistent with PATH-first). No uv-only recommendation remains. |

## Regression check against the 28 RESOLVED findings of `qa/qa-research-verification.md`

Scope: only five research files were edited in this fix pass (`research-notes.md`, `05`, `06`, `scope-02`, `scope-03`, per the fix log; file mtimes 19:58-20:00 versus 19:38-19:47 for `scope-01`, `scope-04`, `07`, which predate the cycle-1 verification at 19:56). Earlier-fix anchors in the edited files were re-read:

| Earlier finding | Anchor re-read this pass | Result |
|---|---|---|
| B-01, B-28 | `research-notes.md:188` canonical vocabulary + precedence 1-7; `:206-214` class table; C14 `:332`; `05:167-178` Orca-half table; `scope-02:99-109` superseded note | intact |
| B-02 | `research-notes.md:216-219` safe-to-close two-part dimension; `scope-02:103` | intact |
| B-03 | C13 `research-notes.md:331`; `scope-02:16`, `:222-224`, `:235-236` (`orca-ide orchestration <verb>`; bare form CODE-CONTRADICTED) | intact |
| B-04 | `research-notes.md:94-95` S3 rows citing `07` A.1/A.2 | intact |
| B-05 | rule 2 "proved final" text `research-notes.md:193`; `scope-02:86`, `:157` parser qualification; `05:46` | intact, strengthened by NB-1 |
| B-06 | `05:71` (B-06 note), C15 `research-notes.md:333` | intact |
| B-07 | `scope-02:119` gate-fix pointer to `07` Section B; `research-notes.md:171-174` | intact |
| B-08 | `research-notes.md:168`, C10 `:328`; `05:165`, Gap 1 `:186`; `scope-02:120`, `:223` | intact |
| B-09 | `research-notes.md:179`, C12 `:330` | intact |
| B-10 | rule 5 `research-notes.md:198`; `06:137`, `:144`, Gap 19 `:176` | intact |
| B-11 | rule 4 (a)/(b) `research-notes.md:195-197`; `scope-02:101` | intact |
| B-13 | `scope-03:99` keeps the local-write proof (`test_contract_status_cli.py:44-66`) and the `_orca(*args)` seam test; allowlist now narrower (NB-2) | intact, strengthened |
| B-15, B-16, B-17, B-18 | `06:39`, Gaps 5-6 `:162-163`, Gap 17 `:174`, `:73`, Gaps 10-11 `:167-168` | intact |
| B-19 | `scope-03:208` OQ3 decision unchanged; now propagated to `:109`, `:209`, `research-notes.md:157` | intact |
| B-20 | `05:43-48` verification tags | intact |
| B-21 | `scope-03:152-157`, `:165` | intact |
| B-22, B-23, B-24 | `06:16`, `:26`, `:33`, `:56-63`, `:72`, Gaps 1-3/15/18 `:158-160`, `:172`, `:175` | intact |
| B-25, B-26 | `05:165`; `scope-02:99-109`, `research-notes.md:175`, `:196` | intact (MINOR notes N7/N9 from cycle 1 unchanged, not rechecked) |
| B-12, B-14, B-27 | `scope-04` and `scope-03:143-150` not touched by this pass (`scope-04` mtime 19:47); `scope-03:143-150` Makefile list re-read unchanged | intact |

No earlier finding regressed. No regression halt applies.

## New blocking findings introduced by this fix pass

None. Adversarial search for incomplete fixes (expected at least 5) found two residuals; both are wording or an edge case on a claim whose substance is correct, so graded MINOR by the review severity rule.

## Notes (MINOR, non-blocking, not rechecked in later rounds)

| # | Location | Note |
|---|----------|------|
| M1 | `research-notes.md:193` rule 2 vs `:200` rule 7 | The fenced exclusion keys on "no `consumer_fenced` evidence". If the transcript or `check` result cannot be read, first-match precedence still lets rule 2 fire on `exited` with no `worker_done`, although rule 7 lists "unreadable log" as could not determine. Suggest the plan state that rule 2 requires the transcript to have been read; an unread or unreadable transcript on an exited row gives could not determine. The stop itself is still positively proved (`exited`), so WC-10 is not broken; only fenced vs stalled is undecided. |
| M2 | `scope-03-cli-patterns.md:99` | "`check --unread` is destructive on older runtimes, `message-check-handler.js:17`": the comment at `:17` says the `--unread --peek` combination is destructive. `--unread` is forbidden either way, so wording only (pre-existing text, not introduced by this pass). |

## PASS set (repeat cycle 1)

B-01 to B-28 (28 of 28, unchanged from cycle 1) plus NB-1, NB-2, NB-3. B-05 and B-13, held open by the qualitative verifier through NB-1 and NB-2, are now RESOLVED.

## Counts and cycle control

- Open blocking findings after this fix pass: **|F_2| = 0**.
- Regression check (first): no item in the cycle-1 PASS set fails now. No regression halt.
- Monotonicity check (second): |F_1| = 3, |F_2| = 0. Strictly shrinks; no `[HALT-MONOTONICITY]`.
- Hard cap: this was the second and last fix pass; with |F_2| = 0 from this verifier, no further cycle is needed on its account.

## Confidence

- **Confidence:** Verified: 3/3 findings + 28/28 regression anchors | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 5 | Glob: 0 | Bash: 2 (one directory listing; one batched read-only `sed`/`grep` script under `/tmp`, cleaned up). No web research performed.
- Limits: research files are untracked, so no git diff baseline exists; the regression check relies on re-reading each earlier-fix anchor plus file mtimes. No live Orca command was run.

Status: COMPLETE

## Verdict: PASS
