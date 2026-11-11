# Revise 1: blocking findings of review 1 of 3

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place)
report revised against: .dev/orca-command-refactor/review/round1.md (merged, review: 1 of 3, verdict FAIL; Reviser brief at round1.md:191-196)
IDS revised (17): M1, M2, M4, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16, M17, M18, M19
not in IDS, not revised: M3, M5, M20 (verifier-rejected; kept as noted, unactioned at round1.md:11 and round1.md:157-179)

No PASS is claimed. Each blocking id below is repaired once; the verdict is for the re-review to decide.

## Byte accounting

| Item | Bytes |
|---|---|
| Before (wc -c, before the first edit) | 57763 |
| After (wc -c, after the last edit) | 60613 |
| Net change | +2850 |

Per-id net change, measured with wc -c after each id's edits (the sum of the rows is 2850):

| Id | Net bytes | Applied at (revised spec line) | Change |
|---|---|---|---|
| M1 | +337 (with M9) | 194 | AC-0.4: P0 step 3 checks the existing report, not the WC-4 path; step 4 not evaluated until P1 (round1.md:17-22; INV-B:242, INV-B:272) |
| M2 | +60 | 159 | P1 command list adds brainstorm and init-lite (their 3.1 rows, spec:84 and :87, had no phase) |
| M4 | +147 | 64, 87 | WC-6 permits a per-attempt unique `--output`; init-lite re-run row no longer overwrites (removed clause: "Re-run overwrites its marked report") |
| M6 | +224 | 61, 109 | WC-3: safety-rule gate (implement Ruling) never asked through `ask`; relayed answer never a Ruling; implement row states the same |
| M7 | +219 | 181, 182 | 7.2 step 2: observation every 5 minutes with explicit `agentWait: null`; step 3 waits of 240000 ms (removed: "900000") |
| M8 | +190 | 182 | 7.2 step 3: branches for `question` (reply) and `escalation` (stop and report) |
| M9 | (see M1) | 194 | AC-0.4 per-command existing report: troubleshoot REPORT.md, workflow contract, adversarial contract (INV-A:35, INV-A:60) |
| M10 | +77 | 73 | 2.3: P0 briefs omit `--unattended`, which is added from P1 |
| M11 | +148 | 184 | 7.2 step 5: command must be the first tool call, no Agent or Task before it; pass condition extended |
| M12 | +280 | 62, 92 | WC-4: subdirectory of `<output-dir>` allowed only when the section 3 row names it; workflow row gets `--output-dir` for pre-creation STOP contracts |
| M13 | +300 | 200 | AC-2.2: expected resolution per row (blocked, or documented default or pin); the one-size pass cell is removed (removed: "`worker_done --outcome failed`; contract `status: blocked` ... never shows `agentWait`") |
| M14 | +152 | 76, 112, 195, 196 | load excluded from the contract, the section, AC-1.1 and AC-1.2 (load row now "P1 (usage line only; no contract or section, M14)"); AC-1.1 scoped to P1 (removed: "in sections 3.1-3.2") |
| M15 | +164 | 159 | P1 flag not accepted by auggie-review, task, cli-eval, pr-submit, post-release until their own phase turns their outward defaults off |
| M16 | +110 | 209 | AC-4.2: outward steps listed as `skipped`, plus a process audit (`ps -ef` before and after) |
| M17 | +131 | 172 | AC-C1: excludes `src/superclaude/core/WORKER-CONTRACT.md:` lines only (SA-2 permits one example there) |
| M18 | +239 | 167 | 7.2 preamble: each `ORCA` command takes `--from <handle>` (or `--terminal`) outside an Orca terminal (CAPS:149) |
| M19 | +72 | 63 | WC-5: `failed` when report absent, empty, unparseable, or status outside the four values; `succeeded` only for `succeeded` or `partial` |

Added and deleted bytes are not split per id. Each edit replaced a clause in place, so wc -c checkpoints give the exact net only. The clauses removed for each id are named in the table above.

## Per-finding disposition

Every id in the IDS list is applied. None is rejected. Each added text carries its finding id.

| Id | Disposition | Where (spec line) | Reason or citation |
|---|---|---|---|
| M1 | applied | 194 | round1.md:17-22; spec:182 and spec:194 (before revision) |
| M2 | applied | 159 | round1.md:26-31; spec:84 and :87 lack a phase row; spec:159-162 total 35 |
| M4 | applied | 64, 87 | round1.md:35-40; WC-6 at spec:64 forbids corrupting the first attempt's output |
| M6 | applied | 61, 109 | round1.md:44-49; spec:61 (WC-3), spec:109 (implement row), spec:234-236 (D2); INV-A:66 |
| M7 | applied | 181, 182 | round1.md:51-59; spec:181-182; CAPS:129 (absent versus null agentWait) |
| M8 | applied | 182 | round1.md:61-69; spec:61 (WC-3), spec:182 (types include question); CAPS:62 (reply --id) |
| M9 | applied | 194 | round1.md:70-77; INV-B:242 (REPORT.md), INV-B:272 (workflow contract), INV-A:35 and INV-A:60 (adversarial, filename not fixed) |
| M10 | applied | 73 | round1.md:79-85; spec:73, spec:79, spec:159 |
| M11 | applied | 184 | round1.md:87-93; spec:184 (before revision) checks only AskUserQuestion; spec:43 (gap 1) |
| M12 | applied | 62, 92 | round1.md:95-101; spec:62 (WC-4), spec:92 (workflow row, no output flag), INV-B:272 |
| M13 | applied | 200 | round1.md:103-109; spec:200 (before revision), spec:116 (research pins planning), spec:103 and :110 (approval items) |
| M14 | applied | 76, 112, 195, 196 | round1.md:111-117; spec:112 (load), spec:265 (no report file for load, Decision row; left unchanged), spec:160 (auggie-review is P2) |
| M15 | applied | 159 | round1.md:119-125; spec:159 (P1 flag scope), spec:100 and spec:114 (outward defaults), INV-A:38 (auggie-review posts by default) |
| M16 | applied | 209 | round1.md:127-133; spec:209 (before revision) checks only git log and gh pr list; INV-B:33 (post-release runs installs and VMs) |
| M17 | applied | 172 | round1.md:135-140; spec:147 (SA-2 permitted example), spec:172 (AC-C1 before revision) |
| M18 | applied | 167 | round1.md:142-147; spec:167 (ORCA means orca-ide outside an Orca terminal); CAPS:149 |
| M19 | applied | 63 | round1.md:149-155; spec:63 (WC-5 before revision); CAPS:73 (outcome mandatory) |
| M3 | not revised (not in IDS) | none | Verifier rejected at round1.md:11 and :159-166; the load row and spec:265 are unchanged |
| M5 | not revised (not in IDS) | none | Verifier rejected at round1.md:11 and :168-175; spec:69, :73, :85, :86 are unchanged |
| M20 | not revised (not in IDS) | none | Verifier rejected at round1.md:11 and :179-186; spec:69, :85, :86, :87 are unchanged |

## Checks run on the revised candidate

- `grep -n '(M[0-9]'` on the revised spec lists the finding tags at the lines in the table above, and every id in IDS appears at least once.
- Phase row P1 (spec:159) now names brainstorm and init-lite, so the 3.1 and 3.2 commands total 37 and the phase rows total 37.
- The step-5 edit (spec:184) was corrected once in place to keep its punctuation; the byte totals above include the correction.
- No `src/superclaude/` path was added to any primitive. The added paths are the contract file name and the `.dev` inventory citations only.
- Edits were confined to `specs/orca-worker-contract-spec.md` and this output file. spec-panel was not run, and no other file was changed.

## UNVERIFIED in this revision

- `ps -ef` as the process audit for AC-4.2 (M16): the command is standard, but the revision did not run it.
- The `--output-dir` flag for `/sc:workflow` (M12) and the `--unattended` rejection behaviour for the five outward-default commands (M15) are proposals; the commands do not implement them in this run. The spec states them as P1 and P4 changes, which the coordinator must still check.
- The exit behaviour of a command that rejects `--unattended` (M15) is not tested.
