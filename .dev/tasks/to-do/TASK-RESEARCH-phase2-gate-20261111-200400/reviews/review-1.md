# Review 1: RESEARCH-REPORT-phase2-gate.md

**Verdict: FAIL** (2 blocking findings, both are wording or labelling errors that put an UNVERIFIED item into a recorded result or an owner-facing decision. The evidence itself is sound. Fix the two wordings and this should pass.)

Reviewer: independent, fresh context. Read-only. No `orca` or `orca-ide` command was run. The report was not edited.

## What I checked

1. **Verbatim quotes and line numbers.** Opened `release-gates.md`, `owner-decisions-and-risks.md`, `adapter-contract.md`, `acceptance-tests.md`, `unverified-register.md`, and the cited lines of `prd.md`.
   - `release-gates.md:36-48`, `:38`, `:40`, `:41`, `:42`, `:48`: verbatim and on the stated lines.
   - `owner-decisions-and-risks.md:22` (decision 6) and `:24` (decision 8): verbatim.
   - `adapter-contract.md:17` (forbidden set), `:57` (rotation set), `:64` (`read k of N Runs`): correct.
   - `acceptance-tests.md:57` (T51) and `unverified-register.md:42` (state filter): correct.
   - `prd.md:106` (R2 row) and `prd.md:250` (panel label): correct.
   - Result: no misquotes.
2. **Observed results against evidence files.** Read every file in `research/evidence/` (jq for row shapes, counts, order).
   - Supported by files:
     - `consumer_fenced` (evidence/01, 02) and `no_active_terminal` (evidence/17, 18, 19).
     - Run B rows and `delivered_at` null throughout.
     - Consuming check `deliveryId` `delivery_657cbe0e1ebb` (07), ack `acknowledged` set and `count` 0 (10), `--all` still 2 rows after ack (11), `--peek` `count` 0 after ack (12).
     - `--all` cap: exactly 100 rows, newest first, `cap probe 102` to `cap probe 3`, 100 unique ids, result keys only `acknowledged, count, messages, runId` (evidence/14).
     - `--peek` cap: exactly 100 rows, oldest first, `cap probe 1` to `cap probe 100` (evidence/15).
     - Timings 0.197/0.199/0.200 and 0.189/0.197/0.195 and send 0.201 (evidence/16).
     - `--types` filter (24, 25); `invalid_argument` for a bogus type is in the log only.
     - `inbox` rows add `read` and `sequence` (evidence/20).
     - Run A gen 5 (evidence/22).
   - Folder status (answer 5): confirmed by `ls`/`git`.
     - The old `to-do` folder holds only `return-contract.yaml` (640 bytes) and its `plan_path` target does not exist.
     - The `done/...-164757` folder has the plan, `progress.md` (T1-T10 `complete verdict=compliant` seen in the first 22 lines), `source.md` quoting "Proceed with building the first release".
     - `9e2608b03` touches both.
     - `.dev/reflect/pre-buildRelease1OfT-20261110050109/` exists, has no `REPORT.md`, and is untracked.
3. **Proven versus UNVERIFIED.** Mostly well labelled. Findings below list the exceptions.
4. **Five required questions.**
   - Q1: present for (a), (b), (c), with gate text, result, dates only partly (see M5).
   - Q2: nine steps with files.
   - Q3: decisions 8 and 6 each have 4 options, one recommendation (8-A, 6-A), and the owner is explicitly not settling.
   - Q4: design changes (section 8, three items) and a plan table (8.1-8.8).
   - Q5: answered (abandoned, superseded).
5. **Secrets.** Grepped evidence for token, secret, password, api key, bearer, `sk-`, `ghp_`, authorization and `/home/coder`: no hits. Pane keys are blanked (`<pane-key>`), pty ids null. Only identifiers remain (terminal handle `term_a39d...`, Run ids, a dispatch id `ctx_8558f21b1977` and the live Run id `run_93bfa00cae2b` in evidence/21, request ids). None is a credential. PASS.

## Blocking findings

**B1. "run-use takes the coordinator seat" and "R2 is one Run only / rotation cannot work" are stated as fact but are not proven.**
- Report 2.1(b) says `run-use` "is what a `run-use` on the live Run would do to the real coordinator's seat" and, in the same row, "whether it actually blocks the real coordinator is UNVERIFIED". The observed change (generation rising, `coordinator_handle` null then back) happened on Runs I created, where the same terminal was the coordinator. No takeover of a Run held by another terminal was tested, and the `coordinator_handle` null and B gen 3 values appear only in the "transcript" (no file).
- Despite that, G-2 ("`run-use` takes the seat"), section 8 item 1 ("cannot work: reading another Run needs binding to it ... R2 is therefore one Run only"), section 6.2 and the owner text in section 11 ("cannot read other Runs without taking over the coordinator's seat") assert it. Section 8 item 1 also contradicts the report's own Q-1: a terminal that has a handle but no Run is untested, and if it can read with `--run`, rotation could work without `run-use`.
- Fix: say "the only way found to read another Run is `run-use`; its effect on a coordinator holding the Run is UNVERIFIED (Q-2)"; mark the "one Run only" change as conditional on Q-1; fix section 11 the same way. This is an owner-facing decision text, so it must not carry an unproven premise.

**B2. "The unbound half FAILED" overstates what was tested for gate proof (b).**
- Gate (b) asks whether the read works from an "unbound observer terminal". The test that failed (evidence/17-19) removed the terminal identity altogether (`env -u ORCA_TERMINAL_HANDLE`), which gave `no_active_terminal`. That is "no terminal", not "a terminal bound to no Run". The report's own table row says the latter is UNVERIFIED.
- Yet the headline of fact (b) ("the unbound half FAILED"), G-2 ("unbound caller: `no_active_terminal`") and section 7 item 1 ("(b) partly proven and the unbound half fails") would be recorded in the gate record as a fail of the gate's wording.
- Fix: record "(b) no-terminal caller fails (`no_active_terminal`); terminal with a handle and no Run: UNVERIFIED (Q-1)".

## Minor findings

- **M1. Many claims cite "transcript", but no transcript file is in `research/`.** Unsupported by a file: L-1, L-4, L-5 (send to own handle rewritten to the Run mailbox), L-6, step 5 of fact (a) (bound to A, `--run B` gives `consumer_fenced`), L-11 (B gen 3, `coordinator_handle` null), the `inbox` 100-row "all Run B" count (evidence/20 holds 3 rows), `send --help` types, the version string, `invalid_argument`. Save the transcript, or the key lines, into `research/evidence/`.
- **M2. Non-consumption step 2 is mislabelled.** The report and log call it an "identical second read" of `check --all --run B`. Evidence/04 is `check --all` with no `--run`, so steps 1 and 2 are different forms of the read. The conclusion holds, the wording does not.
- **M3. "delivery is replayed until acked" (step 6) is not shown.** Evidence/08 and 09 are non-consuming reads that still list the rows. No second consuming `check` was run. Also, "`--peek` hides rows once the coordinator has read them" is imprecise: evidence/09 (after the consuming read, before the ack) still shows 2 rows; they disappear only after the ack (evidence/12). Say "after the ack".
- **M4. Evidence/13 has blank values** (`sent 102 in  s`, `read seconds:` empty). Nothing is claimed from the blanks, but the file does not support a timing for the sends.
- **M5. Q1 completeness.** Facts (b) and (c) carry no own date line (only the header date) and fact (c) shows no command line for the cap and timing measurements. Add the commands and dates next to the results.
- **M6. Budget verdict is missing from section 7.** The gate lists "message calls per cycle set by measurement"; the success criteria in section 3 promise a verdict, but it appears only in the "does not change" paragraph of section 8 (about 0.2 s per call, 1 call per cycle) and is based on one probe Run with 104 messages.
- **M7. Probe hygiene.** `inbox --limit 100` was run once without testing whether `inbox` consumes or what its scope is (report keeps it forbidden). It is disclosed and the rows were all Run B, so no cross-Run body was kept. Note that evidence/21 exposes the live Run id; it is not a secret, but redact it if the folder is shared.
- **M8. Message counts differ slightly** (104 at cap time; "about 106" in section 10; the evidence/20 `timing` row shows at least 105). Harmless; align the numbers.

## Not blocking, worth keeping

- Fact (c) is honestly marked UNVERIFIED and not measured.
- Fact (a) is correctly reported as a fence, not a filter, with samples from two Runs (evidence/03, 23) and the fenced response (evidence/01, 02).
- Decisions 8 and 6 are left to the owner with one recommendation each.
