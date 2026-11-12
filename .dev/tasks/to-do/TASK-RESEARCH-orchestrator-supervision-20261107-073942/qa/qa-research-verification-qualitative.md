# QA Report — Research Gate Fix-Cycle Verification (Qualitative)

**Topic:** Orchestrator mode Phase 1 (issue #339) — research coherence after gate fixes
**Date:** 2026-11-07
**Phase:** fix-cycle (qualitative, report-qualitative lens)
**Fix cycle:** 1
**Fix authorization:** false (no research file edited)

---

## Overall Verdict: FAIL

Open blocking findings: 3. Two of them are original qualitative findings that are still open (B-05, B-13). The third is a new contradiction that a fix introduced (NB-3). The other eight qualitative findings are resolved. No fix breaks WC-10, and none builds on option A4.

Sources read: `qa/qa-consolidated-findings-phase3.md`, `qa/qa-research-fix-log.md`, every file in `research/` (research-notes, scope-01..04, 05, 06, 07), and the Orca handler `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-check-handler.js` (read-only `sed`).

## Original qualitative findings: status

| ID | Status | Evidence (re-read this cycle) |
|---|---|---|
| B-01 | RESOLVED | `research-notes.md:188` declares Section C the one canonical vocabulary; `scope-02:99-103` supersedes the draft bullets; `05:167` gives only the Orca half and defers to Section C. |
| B-02 | RESOLVED | `research-notes.md:192` puts the contract read first: `worker_status: blocked` is waiting on a person, never finished (WC-5 `WORKER-CONTRACT.md:58`); `05:167` repeats it. |
| B-05 | **OPEN** (see NB-1) | Rule 3 (`research-notes.md:194`) says fenced is "never stalled", but rule 2 (`:193`) is evaluated first and matches "`exited` liveness with no `worker_done`". A fenced worker whose process has exited therefore classifies as stalled, so the fix does not hold. |
| B-12 | RESOLVED | `scope-04:320-332` gives each class a home in the skeleton and counts it; the minor count mismatch is noted below. |
| B-13 | **OPEN** (see NB-2) | `scope-03:99` adds the argv-allowlist test, but the allowlist contains an argv the handler rejects (`check --all` with `--peek`), allows `check` unconditionally against the design default in `06:72`, and states an UNVERIFIED claim as fact. |
| B-22 | RESOLVED | `06:33`, `:50`, `:56`, `:81`, `:151` consistently say the check modes are help-documented, and they mark runtime read-marking UNVERIFIED. |
| B-24 | RESOLVED | `06:16` relabel is in place; `07` C(a)-(g) supports it with handler line evidence. |
| B-26 | RESOLVED | `scope-02:99-103` and `:237` make safe-to-close a separate two-part REVIEW dimension, not a class. `scope-01:64` still says "class" (minor note below). |
| B-27 | RESOLVED | `scope-03:143-150` lists lint-architecture Checks 1-11 correctly. |
| B-28 | RESOLVED | The class names at `research-notes.md:188` are used in `05:170-178`, `scope-04:316` and `06:137`. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| NB-1 | IMPORTANT (contradiction; keeps B-05 open) | `research-notes.md:190-194`; mirrored at `05-orca-row-schema.md:172-173` and `06-orca-open-questions.md:137` | Precedence is "first rule that matches" (`:190`). Rule 2 (stalled, `:193`) matches "`exited` liveness with no `worker_done`" and runs before rule 3 (fenced, `:194`). WC-12 (`WORKER-CONTRACT.md:60`) says a fenced worker stops **without** `worker_done`, so once its process exits it has exactly that signal and rule 2 classifies it as stalled. That contradicts rule 3's "never stalled", `scope-02:86` ("fenced, never stalled (Section C rules 2-3)") and `scope-01:62`. `05:172-173` lists stalled before fenced in the same order, and the superseded Q4 mapping at `06:137` derives stalled from `exited` with no fenced exclusion. | Evaluate fenced before stalled: either swap rules 2 and 3, or add to rule 2 "and no `consumer_fenced` evidence in the transcript or `check` result". Apply the same order or exclusion to `05:172-173` and `06:137`. |
| NB-2 | IMPORTANT (wrong behaviour plus a cross-file contradiction; keeps B-13 open) | `scope-03-cli-patterns.md:99` | (1) The allowlist permits "`orchestration check --all` (with `--peek`)". The handler rejects any combination of read modes: `if ([flags.has('unread'), peek, flags.has('all')].filter(Boolean).length > 1) throw ... 'Choose at most one message read mode: --unread, --peek, or --all.'` (`message-check-handler.js`, verified by `sed`; also `07` C(c) `:18-20`). A test built from this allowlist pins an argv that always fails. (2) It allows `check --peek` and `check --all` unconditionally. `06:72` constraints (2) and (3) and `07` say any check may change state, that `--peek` is trusted only after a probe, and that the design default reads contracts only. (3) It states "plain `check` marks messages read" as fact, but `06` Gap 1 marks runtime read-marking UNVERIFIED. | Replace the allowlist entry with `check --peek` and `check --all` as separate argv. Gate both behind the probe and constraint rule of `06:72`, with no `check` call as the default. Tag the read-marking clause UNVERIFIED and cite `06` Gap 1. |
| NB-3 | IMPORTANT (cross-file contradiction introduced by the B-19 fix) | `research-notes.md:157` (option A1) and `scope-03-cli-patterns.md:209` (OQ4) versus `scope-03-cli-patterns.md:208` (OQ3, B-19 decision) | OQ3 now decides that the skill calls the bare `superclaude sweep ...` on PATH first, with `uv run superclaude sweep ...` as the dev-checkout fallback, and that `allowed-tools` lists both forms. Option A1 at `research-notes.md:157` still says "the skill calls `uv run superclaude sweep ...`", and OQ4 at `:209` suggests only `Bash(uv run superclaude sweep *)`. A plan built from the synthesis file or from OQ4 would ship the uv-only form that B-19 rejected. | Update `research-notes.md:157` to the PATH-first and uv-fallback wording, and change OQ4 `:209` to list both `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)`. |

### Minor notes (non-blocking; not rechecked in later cycles)

- `research-notes.md:175` ends "Critical gap G-A below" and `:196` says "see G-A" for the pending-`ask` read path. That gap is G-B (`:271`, `:329`, `06:1`). The same row's "`agentWait` is the only non-consuming wait signal found" is stale now that `07` B lists other plain reads.
- `research-notes.md:225` still says "Needs a human" for the first report section, which is residue of the old vocabulary; Section C says "waiting on a person".
- `research-notes.md:182` "consumes messages, assumed; UNVERIFIED" is acceptable, but it should cite `06` Gap 1 so the source is the same as the B-13 text.
- `05-orca-row-schema.md:165` says "because `agentWait` is only on worker-show", while `:157` says it is UNVERIFIED that the row lacks it. The design outcome is the same (call worker-show per row), so this is wording only.
- `05-orca-row-schema.md` lists Gap 10 before Gap 9 (ordering).
- `05-orca-row-schema.md:178` gives worker-show as the source for a missing contract; the contract is a file read (`research-notes.md:176`).
- `scope-01-contract.md:64` calls safe-to-close "A 'safe to close' class"; it is a dimension (`scope-02:237`).
- `scope-04-409-layout.md:290` shows three counts in the Retained problems section, while `:332` says stalled (proved) and could not determine are also listed there.
- `06-orca-open-questions.md:187`: the original Summary still says inbox and `--unread` are undocumented and names `worktree ps --agent-wait`. The `:189` update supersedes it, but the stale paragraph should be marked superseded.

## WC-10 and option A4 checks

- **WC-10 (absence of a signal is never proof of death): HOLDS.** Rule 2 accepts only positive stop proof and sends an unproved latest turn to could not determine (`research-notes.md:193`). Rule 5 says `agentWait` null is never stall proof (`:198`). Rule 7 is could not determine, `06:73` treats an unreachable source as could not determine, and `scope-04:320` and `:344` show absence as "could not determine", never as stalled. NB-1 is a precedence defect between two positive-evidence rules, not a WC-10 break: `exited` liveness is positive evidence of a stop.
- **Option A4: NOT BUILT ON.** `research-notes.md:160` keeps A4 CODE-CONTRADICTED. `:162` borrows only the report shape and the SAFE/REVIEW vocabulary "without its scripts". `scope-02:241` contains no A4 dependency, and no fix references `bootstrap_scan.sh` or the 72 h default as an input.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | B-01 single canonical vocabulary | PASS | `research-notes.md:188`; `scope-02:99`; `05:167` |
| 2 | B-02 contract read first, blocked is not finished | PASS | `research-notes.md:192`; `WORKER-CONTRACT.md:58` |
| 3 | B-05 fenced is never stalled | FAIL | NB-1: `research-notes.md:190-194`; `05:172-173`; `06:137` |
| 4 | B-12 every class has a report home | PASS | `scope-04:320-332` |
| 5 | B-13 Orca read-only proof test | FAIL | NB-2: `scope-03:99` against the handler `sed` and `06:72` |
| 6 | B-22 check-mode wording | PASS | `06:33`, `:50`, `:56`, `:81`, `:151` |
| 7 | B-24 relabel | PASS | `06:16`; `07` C |
| 8 | B-26 safe-to-close is a dimension | PASS | `scope-02:99-103`, `:237` |
| 9 | B-27 lint-architecture checks | PASS | `scope-03:143-150` |
| 10 | B-28 vocabulary used everywhere | PASS | `05:170-178`; `scope-04:316`; `06:137` |
| 11 | No new cross-file contradiction from fixes | FAIL | NB-3: `research-notes.md:157` and `scope-03:209` against `scope-03:208` |
| 12 | WC-10 intact | PASS | `research-notes.md:193`, `:198`; `06:73`; `scope-04:320`, `:344` |
| 13 | Nothing builds on A4 | PASS | `research-notes.md:160-162`; `scope-02:241` |
| 14 | `07-gate-gap-fill.md` consistent with what cites it | PASS | `07` B used at `research-notes.md:171-174`; `07` D used at `:179`; `07` C(f) `--format` is a boolean switch, consistent with the `scope-03:99` forbidden list |

**Items that PASS:** 1, 2, 4, 6, 7, 8, 9, 10, 12, 13, 14 (resolved findings B-01, B-02, B-12, B-22, B-24, B-26, B-27, B-28; WC-10; A4; consistency of 07).

## Summary

- Checks passed: 11 / 14
- Checks failed: 3 (B-05 via NB-1, B-13 via NB-2, new NB-3)
- Critical issues: 0; Important (blocking): 3; Minor notes: 9
- Issues fixed in-place: 0 (fix authorization false)
- Issue trend: the 10 qualitative blocking findings fell to 3 open blocking findings, so the count is going down.

## Recommendations

- Fix NB-1, NB-2 and NB-3 in the research files (cycle 2 is the last allowed fix cycle), then re-run this verification once.
- The minor notes are optional; the G-A/G-B label at `research-notes.md:175` and `:196` is the cheapest one to fix together with NB-1.

## Confidence

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 28 | Grep: 8 | Glob: 0 | Bash: 1 (read-only `sed` of `message-check-handler.js`; no orca, ccsession, sweep or close command run)
- Web research: none performed (no Tavily or WebSearch call needed; every claim checked is local).
- UNCHECKED items: none. UNVERIFIABLE items: none.

## Self-Audit

1. Factual claims verified independently: 14 checklist items, plus about 30 file:line citations re-read this cycle (Section C rules 1-7, the scope-03 allowlist, OQ3 and OQ4, the 05 Orca-half table, the 06 constraints and Q4, the 07 sections, and the scope-04 skeleton).
2. Files read: `qa/qa-consolidated-findings-phase3.md`, `qa/qa-research-fix-log.md`, `research/research-notes.md`, `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, `research/07-gate-gap-fill.md`, and the Orca `message-check-handler.js`.
3. Not a zero-issue review: 3 blocking findings and 9 minor notes, each cited at file:line.
4. No web research was done, so the Tavily-first rule did not apply.

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` was supplied, so this review ran standalone. The fix log's "applied" claims were used only as pointers to where to look; every fix was re-read at its file:line.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Handler read-mode rejection: verified by `sed` of `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-check-handler.js`, which shows "Choose at most one message read mode: --unread, --peek, or --all." This disproves the `scope-03:99` allowlist entry (NB-2).
- Section C precedence: read `research-notes.md:190-194` ("first rule that matches"; rule 2 matches `exited` with no `worker_done`) against WC-12 `WORKER-CONTRACT.md:60` (fenced ends without `worker_done`) and rule 3's "never stalled" (NB-1).
- B-19 propagation: read `scope-03:208` (PATH form first, both forms in allowed-tools) against `scope-03:209` and `research-notes.md:157` (uv form only) (NB-3).
- G-A/G-B labels: Grep over `research/` shows G-A defined as the row schema (`research-notes.md:270`) and G-B as the question read (`:271`), against the mislabels at `:175` and `:196`.

## QA Complete

## Verdict: FAIL
