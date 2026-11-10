review: 3 of 3

# Spec-panel critique, round 3 (re-review): orca-worker-contract-spec.md

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (290 lines), sha256 `06cb4bcd39e29ea26abacd7521abf23c5e125f1cefda82fb1736f725a01d24b0`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md` (290 lines), sha256 `7f3af35e63f12d24d6eebc453c30497ba2705a10886e04c84b5f7497272961d3` (the text round 2 reviewed; `review/round2.md` header records the same hash)
- prior: `.dev/orca-command-refactor/review/round2.md` (review: 2 of 3), sha256 `f07f9909b9e058e3a8b16fca4384fe8aa93236ed1a2faf5b6f77a32d278c39b9`
- brief: RE-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (the sandbox home copy), sha256 `0bf6d28fbffb08a2ce62010bdabda114a80065090d9fb4fc24beaa06471e7408` (matches the value in round 2's header)
- mode and focus: `--mode critique --focus requirements,architecture --re-review` with `--baseline`
- review number: N = 2 + 1 = 3
- reviewer model: claude-haiku-5-5
- evidence limits: checkable here are the README, the three inventories, the candidate, the baseline, round 2, and the command and prompt files. Citations into `src/`, `cmd/`, `sk/` and `.dev/evals/` are UNVERIFIED because those paths are not in this workspace. Where a changed line quotes one, the inventory line it cites is checked instead.
- sandbox note: one Bash call in this run wrote a scratch redirect to `/tmp/none`, which is outside the sandbox. It has no content of value. The coordinator may remove it. No other path outside the sandbox was touched.

Citation shorthand: `SPEC:N` = line N of the candidate (identical numbering to the baseline for lines 62 and 87); `BASE:N` = line N of the baseline; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `R2:N` = line N of round 2.

## Coverage

- Read in full: the `/sc:spec-panel` command file (`command.md`), the review-loop prompts file, README, round 2, and the candidate (290 lines).
- Diffed in full: `diff -w` of baseline against candidate. The output has two hunks, at SPEC:62 (WC-4) and SPEC:87 (init-lite row). No other line differs.
- Read in part, for the changed-line citations: `INV-B:25-75` and `INV-B:255-285` (load row INV-B:31; load notes INV-B:62 and INV-B:65; workflow INV-B:52 and INV-B:272); `INV-A:30-70` (adversarial INV-A:35; init-lite INV-A:55; adversarial notes INV-A:60).
- Not checked: `CAPS:` lines, `cmd/`, `sk/`, `src/`, `.dev/evals/` and the Orca guides. Every citation into them stays UNVERIFIED here. Unchanged lines were not re-read against them.

## Step 1: evidence block

Command: `diff -w BASELINE CANDIDATE`. Lines are copied verbatim from its output, with the prefix removed.

BEFORE (baseline, `<` lines):

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes its contract to the path that WC-4 or its section 3 row names, and the brief states that exact path (F-01). The default is `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). Two named exceptions: adversarial writes `<output>/adversarial/return-contract.yaml` (INV-A:35), and workflow writes `<dir>/return-contract.yaml` under its new `--output <dir>` flag (INV-B:52, INV-B:272). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
| init-lite | `--output <file>` (under `--unattended`, unique per worker and attempt, F-05, F-07) | `.dev/superclaude/context-audit.md` or `--output` | Fresh file per attempt: a `--retry-of` brief passes a new `--output` path, so the first attempt's report is kept (F-05, WC-6) | Under `--unattended`, the contract goes beside the `--output` file (`<output-dir>` is that file's directory, WC-4), and each worker's own directory keeps two workers from sharing `context-audit.md` (F-07, WC-11) (P1) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```

AFTER (candidate, `>` lines):

```text
| WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes its contract to the path that WC-4 or its section 3 row names, and the brief states that exact path (F-01). `load` is the one section 3 command that writes no file, so it writes no contract (F-02; section 3.2 load row; INV-B:65). The default is `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). Two named exceptions: adversarial writes `<output>/adversarial/return-contract.yaml` (INV-A:35), and workflow writes `<dir>/return-contract.yaml` under its new `--output <dir>` flag (INV-B:52, INV-B:272). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
| init-lite | `--output <file>` (under `--unattended`, in a unique directory per worker and attempt, F-05, F-07) | `.dev/superclaude/context-audit.md` or `--output` | Fresh output directory per attempt (WC-6): a `--retry-of` brief passes a new directory and the `--output` file inside it, so the first attempt's report and contract are kept (F-05) | Under `--unattended`, the contract goes beside the `--output` file (`<output-dir>` is that file's directory, WC-4), and each worker's own directory keeps two workers from sharing `context-audit.md` (F-07, WC-11) (P1) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```

Self-check before the verdict: each quoted AFTER line was matched whole-line (`grep -qxF`) in the candidate, and each quoted BEFORE line in the baseline. All four matched, so the roles are not swapped.

## Prior blocking findings (from R2)

R2 left F-02 and F-05 open and graded every other R1 id resolved. Each is re-checked below against the candidate, as the AFTER text.

| R1 id | R3 status | Basis (candidate text) |
|---|---|---|
| F-01 | resolved (holds) | WC-4 (SPEC:62) still states the default and the two named exceptions; the adversarial row (SPEC:83) and the workflow row (SPEC:92) agree with it. The cli-portify residual (SPEC:105, "file location unnamed") is unchanged text; see R2-06 below. |
| F-02 | resolved | The contradiction is gone. WC-4 (SPEC:62) now says `load` writes no contract, and cites the load row. The load row (SPEC:112) says "none (F-02: no Task, so no contract ...)". AC-1.1 (SPEC:200) exempts `load`. The decision row (SPEC:270) says a report file would be an unrequested addition, which agrees. The inventory basis is INV-B:31 ("None; context in chat") and INV-B:65 ("writes no file"). A narrower residual about checkpoint creation is R3-03. |
| F-03 | resolved (holds) | WC-3 (SPEC:61) is unchanged. The Ruling rule is still stated, with the D2 link at SPEC:109 and SPEC:218. |
| F-04 | resolved (holds) | SA-3 (SPEC:148) is unchanged and still names the adversarial path as the one exception. The adversarial row (SPEC:83) agrees. The two real paths are at INV-A:35 and INV-A:60. |
| F-05 | resolved | The contradiction is gone. The init-lite row (SPEC:87) now says "Fresh output directory per attempt (WC-6): a `--retry-of` brief passes a new directory and the `--output` file inside it". WC-6 (SPEC:64) requires that a re-run "writes each run into a fresh output directory". The contract lands in that directory (SPEC:87, second cell), so the attempt-1 contract is kept. The two texts now agree. |
| F-06 | resolved (holds) | AC-C1 (SPEC:172, SPEC:180) is unchanged. Its positive control is named at SPEC:172. |
| F-07 | resolved (holds) | index-repo (SPEC:86) and init-lite (SPEC:87) both write to a unique directory under `--unattended`. WC-11 (SPEC:69) is unchanged. Its cross-reference to section 2.3 is R2-02, carried below. |

Regressed: none. Open blocking findings after this review: none.

## Findings on changed lines

Only SPEC:62 and SPEC:87 differ from the baseline, so only findings on those lines are `origin=changed`. Grades follow the FIRST-REVIEW grading check.

- **R2-05 (Medium, origin=changed, SPEC:62, carried).** WC-4 still does not say what an unattended run does when it has neither `--output` nor `--output-dir`. The revision did not address it. Grading sentence: an implementer who follows SPEC:62 for a command with no output flag has no `<output-dir>`, so the contract path must be guessed between cwd, a default directory and "blocked". That is an undefined edge case, so Medium, not blocking. Recommendation: resolve such a run as blocked (M-12).
- **R3-01 (Minor, origin=changed, SPEC:62).** The clause "Two named exceptions" is stale. The validate-tests row (SPEC:125) writes the contract to `<dir of --report>/return-contract.yaml`, which WC-4 does not name, and the same sentence adds `load` as a no-contract case, so the count of exceptions is not two. The first sentence of WC-4 lets a section 3 row name the path, so the row governs and no implementer is misled. Recommendation: say "the named exceptions are in the rows" or count them correctly.
- **R3-02 (Minor, origin=changed, SPEC:87).** The init-lite row cites WC-4 for "`<output-dir>` is that file's directory". WC-4 (SPEC:62) defines `<output-dir>` only as "the directory the coordinator passed (`--output` / `--output-dir`)" and says nothing about a file's directory. The row states the rule itself, so the outcome is stated and no implementer is misled. Recommendation: move the rule into WC-4 or fix the citation.
- **R3-03 (Medium, origin=changed, SPEC:62 against INV-B:62).** WC-4 says "`load` is the one section 3 command that writes no file", and cites INV-B:65. INV-B:65 says load "writes no file", but INV-B:62 (d) says "Write is listed for 'checkpoint creation' with no path (`cmd/load.md:52`)". Grading sentence: an implementer who follows SPEC:62 and runs `load --type checkpoint` gets a file with no contract, against "writes no contract"; the sentence is contradicted by the inventory it cites. It is not blocking, because load is never its own Task (SPEC:112; INV-B:65 "use as a brief step"), so no worker report depends on it. Recommendation: state that load writes no contract, and that checkpoint creation, if used, writes a checkpoint file outside the contract; or scope the claim to load as a Task.

Findings on unchanged lines (`origin=unchanged`). Under the re-review rule these are minor notes, because they do not quote a changed line. Their round 2 grades are shown for traceability.

- **R2-01 (was Medium; minor note).** SPEC:86, index-repo `mode=update`. The row does not say where update reads the prior index. The line is unchanged from the baseline.
- **R2-02 (was Medium; minor note).** SPEC:69 (WC-11) says "the coordinator never gives two workers the same output path (F-07; section 2.3)". Section 2.3 (SPEC:73) does not state that rule. The cleanup-audit row (SPEC:85) relies on the same rule.
- **R2-03 (was Medium; minor note).** SPEC:61 (WC-3) states "never" for the implement Ruling. D2 option (b) (SPEC:235) would allow a relayed Ruling and would require rewriting WC-3 and AC-4.1. Recommendation: note in D2 that choosing (b) rewrites WC-3 and AC-4.1.
- **R2-04 (minor).** SPEC:61 cites "INV-A:51-52" for the Ruling rule. INV-A:52 is the improve row (`inventory/commands-a.md:52`). The rule is at INV-A:51 and INV-A:66, which I checked.
- **R2-06 (minor).** SPEC:105, cli-portify, still says "file location unnamed". Its row names no output flag, so the WC-4 default (`<output-dir>` from `--output` / `--output-dir`) cannot be resolved for it. The line is unchanged, so it is a note.

## Mandatory output artifacts (changed guards only)

Covered: the guard conditions on changed lines, per FR-8 to FR-10. Scope is limited to the guards that SPEC:62 and SPEC:87 state or change.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 output dir | SPEC:62 | Zero/Empty | `--unattended` with neither `--output` nor `--output-dir` | n/a | not stated (R2-05) | GAP, Medium |
| WC-4 load | SPEC:62, SPEC:112 | Zero/Empty | `load`, no output | n/a | no contract (stated; F-02 resolved) | OK |
| WC-4 load, checkpoint | SPEC:62 vs INV-B:62 | Typical | `load --type checkpoint`, unattended | a checkpoint file is written; no contract | "writes no file" is stated, checkpoint write is not (R3-03) | GAP, Medium (no worker consequence; load is never a Task) |
| WC-4 adversarial | SPEC:62, SPEC:83 | Typical | adversarial `--output D` | `D/adversarial/return-contract.yaml` | stated | OK |
| WC-4 workflow | SPEC:62, SPEC:92 | Typical | workflow `--output D` unattended | `D/return-contract.yaml` | stated | OK |
| WC-4 validate-tests | SPEC:62, SPEC:125 | Typical | validate-tests `--report R` unattended | `<dir of R>/return-contract.yaml` | named by the row; the "two exceptions" count is stale (R3-01) | OK |
| WC-6 init-lite retry | SPEC:87, SPEC:64 | Typical | `--retry-of` with a new directory and `--output` file inside it | new contract beside the new file; attempt 1 kept | stated (F-05 resolved) | OK |
| WC-6 init-lite first run | SPEC:87 | Typical | unattended, unique directory | contract beside the `--output` file | stated | OK |
| WC-4 init-lite path | SPEC:87 vs SPEC:62 | Legitimate Edge | `--output <file>`, so `<output-dir>` is undefined in WC-4 | file's directory | the row states it; WC-4 does not (R3-02) | OK (citation Minor) |
| SA-3 | SPEC:148 | Typical | standalone default run of `load` | no file written, as today | stated for the default; checkpoint not covered (R3-03) | OK for default |

Pipeline Dimensional Analysis: not triggered by this review. The fan-in text (SPEC:39) did not change.

## Follow-up candidates (Medium and minor; not blocking; not in any reviser brief)

The coordinator asks the user once whether to open an issue for these. No issue has been created.

- R2-05 (Medium, SPEC:62).
- R3-03 (Medium, SPEC:62 against INV-B:62).
- R3-01 (minor, SPEC:62), R3-02 (minor, SPEC:87).
- R2-01, R2-02, R2-03, R2-04, R2-06 (minor notes, unchanged lines).
- M-01 to M-19 from round 1, unchanged lines, carried as round 2 recorded them. Not re-graded here.

## Decisions (this worker)

| Decision | Options | Rationale |
|---|---|---|
| F-02 graded resolved | (1) open, because of the checkpoint claim; (2) resolved, with the checkpoint claim as Medium R3-03 | (2). The F-02 pair is WC-4, the load row, AC-1.1 and SPEC:270. All four agree on "no contract for load". The checkpoint point is a separate claim about a file that is not a Task. |
| F-05 graded resolved | (1) open, because WC-4's `<output-dir>` is not defined for a file; (2) resolved, with the citation as R3-02 | (2). WC-6 and the init-lite row agree on a fresh directory. The row states where the contract goes, so the outcome is set. |
| R2-05 kept Medium | (1) minor, because the revision did not touch it; (2) Medium, because the guard is undefined | (2). An edge case with no stated output path is a Medium under FR-8 and the FIRST-REVIEW grading check. |
| R2 findings on unchanged lines downgraded to minor notes | (1) keep round 2 grades; (2) minor under the re-review rule | (2). The re-review rule says an `origin=unchanged` finding is a minor note unless it quotes a changed line. None of R2-01 to R2-04 or R2-06 quotes SPEC:62 or SPEC:87. |
| Review number | 3 of 3 | Prior header `review: 2 of 3` plus one. The prior file's review number is below 3, so the review runs. |
| Gate review | run it now, or leave it to the coordinator | Left to the coordinator. The brief asks for this re-review only, and the RE-REVIEW prompt says a whole-document claim needs the separate GATE prompt. |

## Reviser brief

Omitted. This report is `review: 3 of 3` and has no open blocking finding. Review step 6 says the brief is omitted at `review: 3`.

Scope of this PASS: changed lines (SPEC:62, SPEC:87) and the prior blocking findings (F-01 to F-07). Whole-document assurance is not claimed. After this PASS, the GATE prompt runs once, as a fresh first review of the complete document (`review: 1 of 3`, labelled as the gate review). A blocking finding there starts one gate loop: one REVISE prompt and one RE-REVIEW. The cap is 5 reviews and 3 fix cycles in all. This run does not perform the gate review.

coverage: scoped PASS: changed lines + prior blockers

verdict: PASS
