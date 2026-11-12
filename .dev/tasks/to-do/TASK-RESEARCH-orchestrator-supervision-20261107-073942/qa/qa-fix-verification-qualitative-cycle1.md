# QA Report — Fix Cycle (qualitative), Phase 6 lens gate, repeat cycle 1

**Topic:** Orchestrator mode Phase 1 (issue #339) research report
**Date:** 2026-11-07
**Phase:** fix-cycle (report-qualitative lens)
**Fix cycle:** 2 (repeat cycle 1, last allowed fix pass)
**Fix authorization:** false (report not edited)
**Inputs:** `RESEARCH-REPORT-orchestrator-mode.md`, `qa/qa-consolidated-findings-phase6-cycle1.md` (C1-01 to C1-05), `qa/qa-fix-log-cycle1.md`, `qa/qa-fix-verification-qualitative.md` (regression baseline)

Line numbers below are for the current 1716-line report (one line longer than the 1715-line version the findings cite, because of the new S3.1 policy bullet at `:391`).

---

## Original findings: RESOLVED / OPEN

Content-lens findings: C1-01 (P6-07), C1-02 (N-2), C1-03 (N-3), C1-05 (N-4). C1-04 came from the structural verifier (P6-18) but changes content (safe-to-close semantics), so it is re-checked here too.

| ID | Status | Verified at | Evidence and adversarial check |
|---|---|---|---|
| C1-01 (P6-07) | RESOLVED | `:900` | Reads "The `/sc:sweep` command and the `sc-sweep-protocol` skill run `superclaude sweep run`; `report.py` renders and writes the dated report and the skill reads the result." Matches the A1 diagram `:932-933`, S7 Recommended approach `:1090` and step 1.15 `:1227` ("no `Write` or `Edit` (`report.py` renders and writes the report, step 1.5; the skill only reads it)"). Grep for "skill writes" finds only `:1001`, which is option A3 (correct for A3, left alone as instructed). The A1 assessment rows `:950-958` make no skill-writes claim. |
| C1-02 (N-2) | RESOLVED | step 1.3 `:1205`; S3.1 `:391`; step 1.8 `:1215`; GQ-96 row `:561` | All four places now say the same thing: the policy dimension ("policy: frozen / not frozen", `data-dictionary.md:27`) is computed for every row independently of the class; a blocked implement contract gets class waiting (a) from rule 1 and policy frozen and is listed under (b) too; rule 4b sets the class only for rows with no earlier match. Step 1.8's fixture now asserts both outputs. The one-class rule (`:360`, "exactly one class ... first rule that matches wins") still holds, because policy is a dimension, not a class. Sources checked: `research/research-notes.md:190` (first match wins), `:192` (rule 1), `:197` ((b) "reported under the policy dimension ... `data-dictionary.md:27`"); `gaps-and-questions.md:119` (GQ-96 resolved, "dimensions are independent"). The freeze is no longer hidden. Residual detail gap recorded as minor note M-1 below. |
| C1-03 (N-3) | RESOLVED | SC-1 `:438` | "How it is checked" now describes the step 1.11 snapshot diff (path, size, `st_mtime_ns`, SHA-256; `HOME` and `XDG_STATE_HOME` inside the isolated root; only the dated report and a new `--output` directory may differ) plus subprocess entry points patched with `side_effect=AssertionError`. Source cell limits `test_contract_status_cli.py:44-66` to the subprocess half and adds "Snapshot diff: plan decision, no in-repo precedent". Matches step 1.11 `:1218` in substance. Other SC-1 references (`:516` gap row, `:1458` Integration Checklist "test_readonly.py passes (step 1.11)") still agree. |
| C1-04 (P6-18) | RESOLVED | step 1.3 `:1205`; S3.1 `:394`; S5 Erlang finding `:680` | All three print the same string: "terminal releasable: could not determine (result read not observable); Orca: reclaimable, next action release", with no proxy for the read. Grep for "releasable" finds only these three places plus the step 1.2 data-model mention (`:1204`), so no place still says a reclaimable + release terminal is "yes". Fits step 1.3's rule-6 note ("contract read ... is a file the sweep reads, not a claim that the worker or coordinator read anything") and WC-10 (nothing inferred). Source checked: `research-notes.md:218`. See note M-2 on the source's "(rule 1/6)" pointer. |
| C1-05 (N-4) | RESOLVED | step 1.0b `:1197`; Rollback `:1279` | Step 1.0b: GQ-11 "with the WC-14 wording, is a hard gate: steps 1.17-1.19 do not start until the owner's answer on GQ-11 is recorded; 'working default accepted' counts only when the owner says it"; the closing sentence limits the working-default rule to "all except GQ-11". Rollback `:1279` repeats the same gate words and points to step 1.0b. The two places no longer give opposite answers. Step 1.17 `:1235` ("WC-14 is the working default ... pending the owner decision") and S9 row 9 `:1505` ("Owner decision (step 1.0b). WC-14 is the working default") are compatible: WC-14 is the draft name, and the draft lands only after the owner answers. Source checked: `gaps-and-questions.md:34` (GQ-11 "open (owner decision)", "WC-14 is the working name"). Wording residues are notes M-3 and M-4. |

Result: 5 of 5 RESOLVED, 0 OPEN.

---

## Fix-introduced checks (the five required by the spawn prompt)

| Check | Result | Evidence |
|---|---|---|
| No new contradiction between sections | PASS | Each fix uses the same wording in every place it touches (C1-02: `:391`, `:561`, `:1205`, `:1215`; C1-04: `:394`, `:680`, `:1205`; C1-05: `:1197`, `:1279`). Read the places next to each fix (S3.1 class table `:360-371`, S3.1 dimensions `:390-406`, SC rows `:436-446`, steps 1.0b-1.19 `:1197-1240`, rollback `:1265-1280`) and found no sentence that now says the opposite. Two wording tensions are recorded as minor notes M-3 and M-4; neither gives a reader a different answer. |
| Section 8 still plans Section 7's recommendation | PASS | S7 recommends A1 (`:1057`, `:1090`); S8 steps 1.0-1.19 build the A1 pieces (`sweep` CLI package, `report.py`, `/sc:sweep` command + skill that only reads). No fix moved a step toward A2, A3 or A4. C1-01 brought the A1 description into line with S8, not away from it. |
| WC-10 (absence of a signal is never proof of death) intact | PASS | C1-04 removes an inference instead of adding one: "could not determine (result read not observable)" refuses to treat a missing read signal as a read. Rule 2 still relies on Orca's state only, rule 3 still only on the synthetic case; no fix adds a timeout, silence or missing-file proof of death. C1-02 adds a dimension computed from the contract file the sweep reads, not from an absent signal. |
| A4 never recommended | PASS | Grep for "A4" finds only option description, assessment and rejected-option rows (`:1014`, `:1152`); none of the five fixes mentions A4. |
| Later phases recorded, not designed | PASS | "Later phases" `:1281-1289` is still one-line entries with no steps, files or acceptance criteria. C1-05's hard gate stops Phase 1 steps 1.17-1.19; it does not plan the Phase 2 work. |
| Kept constraints | PASS | NB-4 exception record at `:13` and `:1644`; [CONTRADICTION] markers at `:1095` (resolution P6-06) and `:1563` (resolution P6-01), both with their resolutions. |

## New blocking findings

None. No fix introduced a wrong statement, a contradiction a reader would act on, or a missing required deliverable.

## Minor notes (not blocking, not to be rechecked)

- **M-1 (C1-02, plan detail).** The rule is clear in prose in four places, but no step 1.3 output names the policy field: the classifier returns one `Classification`, and step 1.2's row model gives `policy` no stated source. Steps 1.5/1.6 do not say the (b) list is built from `policy`, not from the class, and step 1.8's "fixture asserts both outputs" names no test in steps 1.9/1.12. A planner can fill this in from the prose; worth one line in the plan.
- **M-2 (C1-04, source reading).** `research-notes.md:218` says "only after the session's result has been read (rule 1/6)". The "(rule 1/6)" pointer could mean the sweep's own contract read, which would make "yes" reachable. The report takes the stricter reading (the coordinator's read is not observable) without naming the other one. The stricter reading can never print a wrong "yes", so it is safe. Both safe-to-close halves now never say "yes" in Phase 1; the report does not route this to Section 9, which matches how the worktree half is handled. Step 1.9 has no case that asserts the new string (that gap existed before the fix).
- **M-3 (C1-05, wording).** The Rollback opening `:1265` says a change to a shared contract may land "on working defaults"; `:1279` says WC-14 "does not land on the working default alone". These fit together (the owner may accept the default), but the first sentence reads more loosely than the gate.
- **M-4 (C1-05, wording).** S4.4 row `:544` still says GQ-11 is "Decided in the plan", and `:1057`, `:1323`, `:1392` say the plan "uses working defaults for ... GQ-11". With the hard gate, "the plan proposes a default the owner must accept" is the accurate wording. Already accepted as a note in the previous cycle.
- **M-5 (C1-01, wording).** `:900` says "the command and the skill run" the CLI; strictly the command invokes the skill, and the skill runs the CLI. No reader would build it wrong.
- **M-6 (pre-existing).** Module count differs: `:952` "four modules", `:1090` five, rollback "all six modules". Not touched by the fixes.

## Regression check against `qa/qa-fix-verification-qualitative.md`

No regression. The items that previous verifier marked RESOLVED or PASS (G-1 to G-5 and the resolved P6-xx items) were spot-checked where a cycle-1 fix touched the same text: P6-06 and P6-01 resolutions next to the [CONTRADICTION] markers (`:1095`, `:1563`), the step 1.11 snapshot-diff design (`:1218`), SC-7 (`:444`), the rollback table, the A1 recommendation (`:1057`) and the A4 rejection (`:1014`, `:1152`). All still read as they did when they were marked resolved. No previously resolved item reopened.

## Items that PASS

- C1-01, C1-02, C1-03, C1-04, C1-05 (all RESOLVED).
- G-1: Section 8 plans A1, the option Section 7 recommends.
- G-2: A4 is never recommended.
- G-3: WC-10 intact (C1-04 removes an inference; no fix adds one).
- G-4: later phases are recorded only, not designed.
- NB-4 exception record kept; both [CONTRADICTION] markers kept with their resolutions.
- No regression of items resolved in the previous qualitative verification.

## Confidence

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (12 items: C1-01 to C1-05; five fix-introduced checks: contradictions, S8 vs S7, WC-10, A4, later phases; kept constraints; regression check.)
- **Tool engagement:** Read: 11 | Grep: 6 | Glob: 0 | Bash: 12. Read + Grep (17) is at least the item count (12).
- **Web research:** none. Every check was against the report and its research files; no external claim needed checking, so Tavily was not called and no fallback was used.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was in the spawn prompt. I relied on the fix log `qa/qa-fix-log-cycle1.md` only for where each fix was made, then read every location myself.
- Relied on the structural verifier for section numbering and citation format; not re-checked here.

**(b) Independent semantic checks (≥1 required, INV-019):**
- C1-02 precedence vs policy: read `research/research-notes.md:190-199` and `gaps-and-questions.md:119`, then report `:360`, `:391`, `:561`, `:1205`, `:1215`; confirmed the class stays one-valued and the policy dimension is separate, so the freeze shows under (b).
- C1-04 read-not-observable: read `research-notes.md:216-219` and Grep for "releasable" across the report; confirmed no place still prints "yes" from Orca state alone.
- C1-05 owner gate: read `gaps-and-questions.md:34`, then report `:1197`, `:1235`, `:1279`, `:1505`; confirmed the gate and the WC-14 default do not conflict.
- C1-01: Grep for "skill writes" and read `:900`, `:932-933`, `:1090`, `:1227`; only A3 `:1001` still says the skill writes, which is right for A3.
- If I claimed 0 issues: I found six minor notes and checked each fix against its research source, not only against the fix log.

## Issues Found

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| M-1 | MINOR | step 1.2-1.9 | Policy field has no named output, (b) derivation and fixture test unnamed | Name the `policy` field, its source and the test in the plan |
| M-2 | MINOR | S3.1 `:394`, step 1.3 | Other reading of "(rule 1/6)" not named; no test for the new string | Add one sentence and one step 1.9 case |
| M-3 | MINOR | Rollback `:1265` | Opening sentence looser than the gate at `:1279` | Say "on working defaults the owner accepted" |
| M-4 | MINOR | `:544`, `:1057`, `:1323`, `:1392` | "Decided" / "uses working defaults" for GQ-11 | Say "proposes a default the owner must accept" |
| M-5 | MINOR | `:900` | Command vs skill wording | Optional |
| M-6 | MINOR | `:952`, `:1090`, rollback | Module count differs | Use one count |

## Recommendations

- No further fix pass is needed. Carry M-1 and M-2 into the plan stage (`/sc:workflow`) as plan details; the rest are wording.

## QA Complete

## Verdict: PASS

