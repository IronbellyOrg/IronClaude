review: 3 of 3
> verification (coordinator, VERIFY step VF3; verifier reply .dev/orca-command-refactor/review/verify-3.md): confirmed blocking ids: none. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: N-2 (verifier: Grading sentence A holds: `docs/a.md` and `docs/a.txt` in one worktree both map to `docs/a.return-contract.yaml` under the F-02 clause, which contradicts WC-11 and the N-1 promise on the same line, so the second write replaces the first. Grading sentence B fails: the first sentence names `<output-dir>` as "the directory the coordinator passed", which for `--output <file>` is a file, so it does not supply a parent directory. F-02 is the specific clause for file-valued outputs and names the stem-based path, so `docs/return-contract.yaml` for every file-valued run follows only if the general first sentence is assumed to override F-02, which the text does not say. The finding requires both outcomes, so it is rejected. The A case alone is text-supported and could be restated as a separate finding, but this verification does not add one.). The Reviser brief below is narrowed to the confirmed ids.

# Spec-panel re-review: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `39bbe6871713a48397dee32c0a486174eebbc1b08a14833316eed1593df495bb` (59343 bytes)
- Baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md`, sha256 `bfe20373dae030b64d0ab846cde01958172f4f46786bcfbad746ac335c6b4df6` (59081 bytes). This is the text round2 reviewed, so the baseline is the text before the REVISE step.
- Prior report: `.dev/orca-command-refactor/review/round2.md`, sha256 `94b088570108d2287512334bc7a6f4e8b62f7288e810515229a0f029a6454354` (`review: 2 of 3`, `verdict: FAIL`, so N = 3; the cap check passes because the prior report is below 3).
- Review rule: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (sha256 `e161284648a17d97e22715de0077e971857e78cf30dd3a41ca3ca126bec19ee3`, read in full). Neither `rf-qa.md` copy (project `.claude/agents/` or `~/.claude/agents/`) exists in the sandbox, so the steps it adds are UNVERIFIED here and the command's own Review Loop rules stand alone (bullet 5).
- Reviewer model: claude-haiku-5-5
- Inputs: all readable. `~/.claude/WORKER-CONTRACT.md` is absent and not needed (no `--unattended` run).
- VERIFY: not run in this session (see Decisions). The verdict below is the reviewer's own grading before VERIFY.

## Citation scope

- `SPEC:n` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line n of the candidate. Changed lines keep their numbers in the baseline.
- `INV-A:n`, `INV-B:n`, `CAPS:n` = `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Each cited line was read in this run.
- `RR:n` = `.dev/orca-command-refactor/review/round2.md` line n (prior report).
- `REV2:n` = `.dev/orca-command-refactor/review/revise2.md`; `VER2:n` = `.dev/orca-command-refactor/review/verify-2.md`.
- Repo files outside the workspace (`src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/agents/rf-qa.md`, `~/.claude/WORKER-CONTRACT.md`) cannot be checked here and are UNVERIFIED. No finding below depends on them.

## Scope

Scoped re-review: only lines changed against the baseline, plus the prior blocking findings and the prior report's resolved findings. This is not whole-document assurance.

## Step 1: evidence block

`diff -w BASELINE CANDIDATE` gives two changed pairs, at SPEC:62 and SPEC:87 (4 lines). A plain `diff` gives the same 4 lines, so there is no whitespace-only change to ignore.

BEFORE (baseline):

```text
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). F-02: a file-valued output (`--output <file>`, as in tdd and init-lite; `INV-B:47`, `INV-A:55`) uses the file's parent directory as `<output-dir>`. Workflow creates its `<id>` at run time (`INV-B:52`, `INV-B:273`), so its brief passes the `<id>` by a flag the P1 plan names (section 3.1 row). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
< | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Fresh `--output` per attempt under `--unattended` (WC-6, F-03); a standalone re-run still overwrites its marked report | Contract at `<parent of --output>/return-contract.yaml` (P1; F-02, F-04) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```

AFTER (candidate):

```text
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). F-02: a file-valued output (`--output <file>`, as in tdd and init-lite; `INV-B:47`, `INV-A:55`) uses the file's parent directory as `<output-dir>`, and its contract is `<output-stem>.return-contract.yaml` in that directory, where `<output-stem>` is the file name without its extension (N-1: two file outputs in one directory then write two contracts, not one shared `return-contract.yaml`). Workflow creates its `<id>` at run time (`INV-B:52`, `INV-B:273`), so its brief passes the `<id>` by a flag the P1 plan names (section 3.1 row). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
> | init-lite | `--output <file>` | `.dev/superclaude/context-audit.md` or `--output` | Fresh `--output` per attempt under `--unattended` (WC-6, F-03); a standalone re-run still overwrites its marked report | Contract at `<parent of --output>/<output-stem>.return-contract.yaml` (P1; F-02, F-04, N-1) | `cmd/init-lite.md:32`; `sk/sc-init-lite-protocol/SKILL.md:66,70`; `INV-A:55` |
```

Self-check (`grep -nF` of each quoted line without its prefix): both BEFORE lines occur exactly once in the baseline and both AFTER lines occur exactly once in the candidate. Roles were not swapped.

Unchanged text that the changed lines depend on: SPEC:76 (the "Contract" definition, `<output-dir>/return-contract.yaml`), SPEC:69 (WC-11, "must never write the same file"), SPEC:90 (tdd, `--output <file>`), SPEC:92 (workflow, `<id>` flag). All are byte-identical to the baseline.

## Prior blocking findings

The prior report (`RR:2`, `RR:153`) has one open blocking finding, N-1. Its Reviser brief named N-1 only. Round 2 also marked F-02 to F-05 (round 1's blocking findings) resolved; under the rule for re-review, those are checked here for regression.

| Prior id | Prior status | Status now | Basis (candidate text) |
|---|---|---|---|
| N-1 | open (`RR:75-82`) | resolved for the case it names; its residue is N-2 | The named case, `--output docs/a.md` and `--output docs/b.md`, now writes `docs/a.return-contract.yaml` and `docs/b.return-contract.yaml` (SPEC:62 F-02 clause; SPEC:87). The unchanged first sentence of the same SPEC:62 paragraph still states the shared name `<output-dir>/return-contract.yaml`, and a same-stem pair still collides. Both are carried as the new blocking finding N-2. |
| F-02 | resolved in round 2 (`RR:64`) | resolved (no regression) | The WC-4 path conflict is named and resolved at SPEC:62 for file-valued outputs. The workflow `<id>` flag is still unnamed (SPEC:62, SPEC:92): this is round 2's M-1, a Medium follow-up, not a regression of F-02. |
| F-03 | resolved in round 2 (`RR:65`) | resolved (no regression) | SPEC:69, SPEC:85, SPEC:86 are unchanged. SPEC:87 changed only the contract name; its per-attempt fresh `--output` is unchanged. |
| F-04 | resolved in round 2 (`RR:66`) | resolved (no regression) | SPEC:195 and SPEC:159 are unchanged. The AC-1.1 scope issue is round 2's M-4. |
| F-05 | resolved in round 2 (`RR:67`) | resolved (no regression) | SPEC:63 is unchanged; the parse rule still maps a non-parsing contract to `failed`. |

F-01 is the noted finding rejected at VF1 (`review/round1.md:2`, `RR:71`). It is not a prior blocking finding and its text (SPEC:73, SPEC:79) is unchanged. It is not re-graded.

## Findings on changed lines

### N-2 | BLOCKING | origin=changed | new, introduced by the N-1 fix at SPEC:62 and SPEC:87

- Location: `SPEC:62`, the F-02 clause "its contract is `<output-stem>.return-contract.yaml` ... where `<output-stem>` is the file name without its extension", and the first sentence of the same paragraph ("the command writes `<output-dir>/return-contract.yaml`"); `SPEC:87` (init-lite, "Contract at `<parent of --output>/<output-stem>.return-contract.yaml`"); `SPEC:69` (WC-11, "Two workers in one worktree must never write the same file"); `SPEC:90` (tdd, `--output <file>`, `INV-B:47`).
- Issue: The name `<output-stem>` drops the extension, so two file outputs in one directory that share a stem get the same contract path. The same paragraph also still states the shared name `return-contract.yaml` for a file-valued output, through `<output-dir>`.
- Grading sentence A: An implementer who follows the F-02 clause of `SPEC:62` as written, running `--output docs/a.md` and then `--output docs/a.txt` in one worktree, writes both contracts to `docs/a.return-contract.yaml`. The second write replaces the first, and the coordinator opens that one path for both `worker_done --report-path` calls (`SPEC:62`, last sentences), so the first worker's outcome is lost. `SPEC:69` forbids two workers writing the same file, so the two stated texts conflict and data is lost. Blocking.
- Grading sentence B: An implementer who follows the first sentence of `SPEC:62`, which gives `<output-dir>/return-contract.yaml` with `<output-dir>` the file's parent directory, writes `docs/return-contract.yaml` for every file-valued run in `docs/`. That is the N-1 collision (`RR:78`) that the revision was meant to remove. The paragraph states both names, so the two statements contradict. Blocking.
- Reachability: the case needs two file-valued outputs in one directory. `SPEC:69` names two workers in one worktree as the parallel case the rule protects, and `SPEC:90` (tdd) and `SPEC:87` (init-lite) are both file-valued. The case is narrower than N-1, but it is the same defect class and the same consequence, so it is graded the same way.
- Recommendation (narrowing, for the escalation to the user): name a file-valued contract by the full output file name (for example `<output-file-name>.return-contract.yaml`, giving `a.md.return-contract.yaml` and `a.txt.return-contract.yaml`), or require the brief to pass the contract path explicitly for a file output. Strike the shared `<output-dir>/return-contract.yaml` name for file-valued outputs from the first sentence of `SPEC:62`, and make `SPEC:87` say the same.
- Priority: High.

## Carried-over findings (status only, not re-graded)

- M-1 (Medium, `RR:84-88`): the workflow `<id>` "flag the P1 plan names" is still unnamed at `SPEC:62` and `SPEC:92`. The changed line 62 still contains this text. Follow-up candidate.
- M-2 (Medium, `RR:90-94`): the output flag for index-repo and cleanup-audit under `--unattended` is unnamed (`SPEC:85`, `SPEC:86`, unchanged). Follow-up candidate.
- M-3 (Medium, `RR:96-101`): step-4 actor and `command` mapping (`SPEC:63`, `SPEC:179`, `SPEC:183`, unchanged). Follow-up candidate.
- M-4 (Medium, `RR:103-107`): AC-1.1 scope against the P1 Commands column (`SPEC:159`, `SPEC:195`, unchanged). Follow-up candidate.
- m-1 (Minor, `RR:109-111`): index-repo `mode=update` location (`SPEC:86`, unchanged). Note.

## New notes (origin=unchanged)

- m-2 (Minor): `SPEC:76` still defines "Contract" as `<output-dir>/return-contract.yaml`, which is the shared name that N-2 says file-valued outputs must not use. The text does not quote the changed line, so under bullet 5 it is a note, not a finding. The N-2 fix at `SPEC:62` makes it inconsistent, and the reviser may align it only if N-2 is revised; it is not a blocking item on its own.

## Guard Condition Boundary Table (changed guards only)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 WC-4 contract name | SPEC:62 | One/Minimal | one file output `--output docs/a.md` | parent `docs/`, stem `a` | `docs/a.return-contract.yaml` | OK |
| G1 WC-4 contract name | SPEC:62 | Legitimate Edge Case | two file outputs, distinct stems, `docs/a.md` and `docs/b.md` | distinct contract paths | `docs/a.return-contract.yaml`, `docs/b.return-contract.yaml` | OK (N-1 resolved) |
| G1 WC-4 contract name | SPEC:62 | Legitimate Edge Case | two file outputs, same stem, `docs/a.md` and `docs/a.txt` | same contract path | second write replaces the first; WC-11 forbids it | GAP, N-2 (blocking) |
| G1 WC-4 contract name | SPEC:62 | Typical | file output, first sentence read literally | `<output-dir>` = parent | `docs/return-contract.yaml` shared by every file run in `docs/` | GAP, N-2 (blocking; reading B) |
| G2 init-lite contract | SPEC:87 | Legitimate Edge Case | `--output docs/a.md` and `--output docs/a.txt` | same contract path | collision as G1 | GAP, N-2 (blocking) |
| G2 init-lite contract | SPEC:87 | Zero/Empty | `--output` without a file | n/a | the file-valued rule needs a file; a missing value is a flag error, not a contract case | n/a |
| G3 WC-4 workflow `<id>` | SPEC:62, SPEC:92 | Zero/Empty | no `<id>` flag named | n/a | flag unnamed | GAP, M-1 (Medium follow-up) |

Omitted classes: Maximum/Overflow is not applicable (no numeric limit in the changed text). Sentinel Value Match is not applicable (no sentinel in the changed text). FR-8: the blocking GAP is N-2; the GAP on M-1 is Medium. FR-9: no blank "Specified Behavior" on a changed row. FR-10: every changed guard is enumerated.

## Follow-up candidates (Medium and minor; not revised)

- M-1 (workflow `<id>` flag unnamed), M-2 (output flag for index-repo and cleanup-audit), M-3 (step-4 actor and `command` mapping), M-4 (AC-1.1 vs P1 Commands column), m-1 (index-repo `mode=update` location), m-2 (`SPEC:76` shared contract name).
- F-01 (noted at `review/round1.md:2`; not graded here).
- Round 1 and round 2 Medium and minor items whose text is unchanged remain follow-up candidates from `review/round1.md` and `RR:133`. No user is present in this run, so no issue was created; the list is recorded only.

## Decisions

- Scope: changed lines (SPEC:62, SPEC:87) and prior blocking findings, plus the resolved round-2 findings checked for regression (RE-REVIEW core, bullet 5). No whole-document assurance.
- N-1 graded resolved for the case it names. Its residue, the unchanged first sentence of the same SPEC:62 paragraph, is part of the new blocking finding N-2, because the two statements in one paragraph contradict.
- N-2 graded blocking by the same test as N-1 (two stated texts conflict, and a shared path loses a worker's outcome under the stated parallel rule). The reachability is narrower (same stem, different extension), but no further assumption about the implementer is needed. If the user rules that same-stem file outputs in one directory are out of scope, N-2 drops to Medium and this verdict would change to PASS.
- F-02 to F-05 stay resolved: no regression from the changed lines. The workflow `<id>` flag gap is round 2's M-1, carried as Medium.
- VERIFY: not run in this session. This worker has no fresh-context verifier. Per the VERIFY rule, the coordinator must brief a verifier with only the candidate and the N-2 text, before escalation. If the verifier confirms N-2, or its reply has no `confirmed:` line, the verdict stays FAIL. If it rejects N-2 with `confirmed: none`, the loop ends with no confirmed blocking finding and that counts as PASS.
- The re-check steps of `rf-qa.md` were not applied because neither copy exists in the sandbox.
- No Reviser brief is written. At `review: 3`, Review Loop bullet 6 omits it, and the run escalates to the user.

## Coverage

Read in full: the command (`command.md`), the workspace README, the RE-REVIEW, VERIFY and REVISE sections of the prompt file, `review/round2.md`, `review/revise2.md`, `review/verify-2.md`, and the candidate and baseline (diffed in full; both changed pairs read in full).
Inventory lines read in this run: `INV-A:53, 55, 107`; `INV-B:47, 52, 272-273`; `CAPS:72-79`.
Self-check: all 4 changed lines matched exactly once (grep -nF).

Not covered: whole-document assurance; unchanged lines beyond those cited above; repo files outside the workspace and the `rf-qa.md` steps (UNVERIFIED here); Orca runtime behavior (`CAPS:79`, UNVERIFIED).

verdict: FAIL
