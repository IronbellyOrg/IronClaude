review: 2 of 3

# Re-review (/sc:spec-panel --mode critique --focus requirements,architecture --re-review round1.md --baseline spec-v1.md)

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 06730fb96147b55377f384ee4605e4ba1f6a74c60f4f348ab9d5de3b86c1559f
- baseline: .dev/orca-command-refactor/specs/history/spec-v1.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (equals the candidate hash recorded in the prior report, round1.md:5, so the baseline is the text round 1 reviewed)
- prior: .dev/orca-command-refactor/review/round1.md sha256 7774bbc0491e4f8ccc8434ed3539d59697d73263d2e22d61722f1fb7ea98fff9, header `review: 1 of 3` (round1.md:1), so N = 2
- reviewer model: claude-sonnet-5-5
- roles fixed per the RE-REVIEW prompt table (CANDIDATE = revised file, BASELINE = spec-v1.md, PRIOR = round1.md); never inferred from reading order
- re-check procedure: the project `.claude/agents/rf-qa.md` does not exist in the workspace and `~/.claude/agents/rf-qa.md` does not exist under the sandbox home (only `~/.claude/rules/prompts/document_review_loop_prompts.md` is present), so the rf-qa steps 1-5 were not read; the Review Loop rules and the RE-REVIEW prompt were applied alone, as the command allows
- evidence limits: only files inside the workspace were checked. Citations use `SPEC:n` = the candidate, `BASE:n` = the baseline, `R1:n` = round1.md, `INV-A:n`, `INV-B:n`, `CAPS:n` = the three inventory files. The real `/sc:spec-panel` definition (command.md in the sandbox root, outside the workspace) is cited once as `CMD:n` and is UNVERIFIED for this run.
- brief: the coordinator brief widened nothing; no clause was overridden.

## Step 1. Evidence block (before any finding)

Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md`. Changed hunks: candidate lines 62, 73, 76, 105, 159, 194-196, 200-201 (all other lines identical ignoring whitespace). Byte sizes 57763 -> 58684 (`wc -c`), which matches the reviser's own accounting in review/revise1.md.

BEFORE (baseline), lines starting `<` of `diff -w BASELINE CANDIDATE` (10 lines):

B1. | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |

B2. The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).

B3. The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.

B4. | cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract | contract (fields already defined; file location unnamed) | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields | dispatch only inside an IronClaude checkout (hardcoded template path) | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |

B5. | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |

B6. | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |

B7. | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |

B8. | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |

B9. | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |

B10. | P2 | AC-2.3 | Happy-path run per P2 command with every required flag in the brief | 7.2 passes with `--outcome succeeded` |

AFTER (candidate), lines starting `>` (10 lines):

A1. | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passes as `--report-dir <dir>`, a directory-valued flag every unattended command accepts, separate from any file-valued `--output` (M6; the current spec-panel definition is UNVERIFIED here, no inventory file covers it). A command that creates its own directory (workflow) writes the contract to `--report-dir` for every outcome, pre-creation STOPs included. It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |

A2. The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the `--report-dir` directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).

A3. The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<report-dir>/return-contract.yaml` (`--report-dir`, M6). Every changed command also gains the `## Unattended mode` section (section 2.1) in the phase its row names, not earlier (M5); `load` gets none (M1). Phase numbers refer to section 6.

A4. | cli-portify | each of the three approval gates resolves as blocked with the artifact to review named in the contract; no flag carries an approval, so an unattended run ends blocked at the first gate (M3) | contract (fields already defined; file location unnamed) | add a `--resume <contract>` flag that uses the existing `resume_phase`/`resume_substep` fields | dispatch only inside an IronClaude checkout (hardcoded template path) | `sk/sc-cli-portify-protocol/SKILL.md:69,152,170,393,464-473,517-566,529`; `cmd/cli-portify.md:23,34`; `INV-A:45,68` | P2 |

A5. | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by the P1 commands named in this row (a no-op where a command has no gate); each later command gains it in its own phase (M5); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |

A6. | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-2 and 5-7 pass; step 3 passes on exactly one `worker_done` whose report path is the command's existing report file; step 4 uses that file, since the contract arrives in P1 (M2). Record the results in the phase report; a failure here reopens section 1 |

A7. | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command named in the P1 row of section 6, except `load` (no report, no section; M1, M4, M5), has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |

A8. | P1 | AC-1.2 | 7.2 live check on each P1 command except `load`, with `--unattended --report-dir <dir>` (M4, M6) | all steps pass |

A9. | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file> --report-dir <dir>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |

A10. | P2 | AC-2.3 | Happy-path run per P2 command except cli-portify, with every required flag in the brief; for cli-portify the run stops at the first approval gate | 7.2 passes with `--outcome succeeded`; for cli-portify, `--outcome failed` and contract `status: blocked` naming the gate's artifact (M3) |

Self-check (run): every AFTER line was found verbatim in the candidate and in no case in the baseline; every BEFORE line was found verbatim in the baseline and in no case in the candidate (exact string tests over all 20 diff lines, 20 of 20 matched, no role swap).

## Prior blocking findings (round1.md ids, each decided against the AFTER text only)

| Id | Status | Basis (AFTER text) |
|---|---|---|
| M1 | resolved | The `load` row says report "none (see note)", phase "P1 (usage line only)" (SPEC:112, unchanged) and now AC-1.1 tests "every command named in the P1 row of section 6, except `load` (no report, no section; M1, M4, M5)" (SPEC:195, A9); section 3 says "`load` gets none (M1)" (SPEC:76, A3). The Decisions row "a report file would be an unrequested addition" (SPEC:265) now agrees with the acceptance test. |
| M2 | resolved | AC-0.4 (SPEC:194, A8) no longer applies step 3 as written at SPEC:182: "steps 1-2 and 5-7 pass; step 3 passes on exactly one `worker_done` whose report path is the command's existing report file". A P0 run of troubleshoot (`REPORT.md`, SPEC:91), workflow (SPEC:92) and adversarial (SPEC:83) can now satisfy step 3. Step 4 residue is Medium, see N2. |
| M3 | resolved | The cli-portify row states "no flag carries an approval, so an unattended run ends blocked at the first gate (M3)" (SPEC:105, A4) and AC-2.3 expects, for cli-portify, "`--outcome failed` and contract `status: blocked` naming the gate's artifact" (SPEC:201, A10). WC-5 maps `blocked` to `failed` (SPEC:63), so the two agree. |
| M4 | resolved | Same edits as M1: AC-1.1 (SPEC:195) and AC-1.2 "on each P1 command except `load`" (SPEC:196, A9-A10 context). The two sub-entries M4.a/M4.b named exactly these two criteria. |
| M5 | resolved | AC-1.1 is scoped to the P1 row (SPEC:195); the P1 row limits the flag to "the P1 commands named in this row" and gives each later command the flag "in its own phase (M5)" (SPEC:159, A5); section 3 adds the section "in the phase its row names, not earlier (M5)" (SPEC:76, A3). `implement`, `post-release`, `pr-submit` (SPEC:109,113,114, phase P4) are no longer in AC-1.1's population, so the P1 test no longer needs the answers to D2-D4 (SPEC:154,162). |
| M6 | resolved | WC-4 now fixes the directory as `--report-dir <dir>`, "separate from any file-valued `--output`", and says workflow "writes the contract to `--report-dir` for every outcome, pre-creation STOPs included" (SPEC:62, A1); section 2.3 puts the `--report-dir` directory in the brief (SPEC:73, A2); AC-2.2 gives tdd both `--output <file>` and `--report-dir <dir>` (SPEC:200). The coordinator can now compute `<report-dir>/return-contract.yaml` before dispatch for workflow, research and tdd. The reviser disclosed this as "applied, with one added mechanism" (review/revise1.md, M6 row); the mechanism is the one M6's recommendation asked for (R1:96), so it is within scope. |

No prior blocking finding is open or regressed. No rejected id exists (R1:12, R1:142-144).

## Findings on changed lines

Each carries `origin=changed|unchanged`. No finding below is blocking; each is Medium or minor (grading check applied: none of them has a sentence that holds with no further assumption).

=== REQUIREMENTS ANALYSIS ===

Wiegers / Adzic / Cockburn lens on the changed lines.

- N1. Medium. origin=changed (quotes the changed WC-4 line, SPEC:62). `--report-dir` was added to WC-4, section 2.3, the section 3 "Contract" definition, AC-1.2 and AC-2.2, but two acceptance rows that write a contract keep `--output <dir>` and no `--report-dir`: AC-3.2 `/sc:roadmap <spec> --unattended --output <dir>` ... "contract written" (SPEC:205) and AC-4.2 `/sc:post-release <version> --unattended --output <dir>` ... "the contract lists each skipped outward step" (SPEC:209). Under WC-4 the contract goes to `--report-dir` (SPEC:62), which those commands do not pass, so the pass condition has no path to check. Sentence: an implementer who follows the stated text as written builds a roadmap that writes the contract to `--report-dir` and runs AC-3.2 without it, and the check "contract written" cannot locate the file; the wrong outcome needs a guess about where the contract lands when the flag is omitted, so Medium. The reviser listed the same residue (review/revise1.md, last row: AC-3.2 and AC-4.2 "unreconciled"). The `analyze`/`design` "add `--output`" cells (SPEC:99,106) are consistent with this pattern, not a conflict.
- N2. Medium. origin=changed (SPEC:194, A8). AC-0.4 keeps "step 4 uses that file". Step 4 passes only if `yaml.safe_load` of the contract returns a mapping with `status` in the four-value set and a `command` key (SPEC:183). Troubleshoot's existing report is `REPORT.md` (SPEC:91), a markdown report, not that mapping, and adversarial's file has no fixed name (SPEC:83). AC-0.4 does not say whether step 4 must pass or only be run, so the P0 gate depends on a reading. Sentence: an implementer who applies step 4 literally to `REPORT.md` fails P0 on a correct run; this needs the guess that "uses" means "must pass", so Medium. Fix by narrowing to "step 4 is skipped in P0" (deletion, no new rule).
- N3. Medium. origin=changed (SPEC:73, A2) and inherited (`--unattended`, BASE:73). Section 2.3 and 7.2 step 1 require the P0 brief to carry "the exact command line including `--unattended`" and "the `--report-dir` directory" (SPEC:73, 180), while P0 has "no command edits" (SPEC:158) and AC-0.4 lists the three command lines without either flag (SPEC:194). The three P0 commands accept neither flag until P1 (SPEC:159). A reader must guess whether AC-0.4's listed lines or 2.3's rule wins. Medium.
- N4. Medium. origin=changed (SPEC:62, 76). WC-4 says `--report-dir` is "a directory-valued flag every unattended command accepts" and the contract is `<report-dir>/return-contract.yaml`. Section 3.1 gives brainstorm and init-lite "None" as the change (SPEC:84, 87) and keeps existing contract paths `<output>/return-contract.yaml` (brainstorm SPEC:84, reflect SPEC:88) and `<output>/adversarial/return-contract.yaml` (SPEC:83, AC-1.4 SPEC:198). No phase or acceptance row adds the flag or the section to brainstorm or init-lite, and AC-1.2 would test adversarial's step 3 against `<report-dir>/return-contract.yaml` (SPEC:182, 196) while the P1 fix names a different path. Reading: the existing path covers the non-unattended run and WC-4 the unattended one, but the text does not say so. Medium.
- N5. Medium. origin=changed (SPEC:105, A4). The cli-portify row keeps "add a `--resume <contract>` flag" while saying no flag carries an approval; a resumed run reaches the same first gate again (same row, plus INV-A:45 "always on"). The row is now honest that cli-portify is a worker that cannot finish unattended, but it still counts among the 27 commands "needing a change" (SPEC:76) and in P2 (SPEC:160). No wrong build follows from the text; it is a scope question for the user. Medium.
- N6. minor. origin=changed (SPEC:159, A5). The P1 row's flag clause covers "the P1 commands named in this row", and `load` is named in that row, while SPEC:76 says `load` gets no section and SPEC:112 changes only its usage line. Whether `load` accepts `--unattended` is left open; AC-1.1 and AC-1.2 are not affected because they except `load`.
- N7. minor. origin=changed. Review-loop ids "(M1)" ... "(M6)" now appear in the spec body (SPEC:62, 76, 105, 159, 194-196, 201). The Reviser contract requires them on each addition (Review Loop bullet 6); they should be stripped when the spec is finalized.

=== ARCHITECTURE ANALYSIS ===

Fowler / Newman / Hohpe / Nygard lens on the changed lines.

- Fowler: separating the directory-valued `--report-dir` from file-valued `--output` removes the interface clash M6 found (R1:95) and keeps one rule for every command (SPEC:62). The cost is a third output flag per command next to `--output` and `--output-dir` (auggie-review, SPEC:100); the spec does not say how a command that already has `--output-dir` relates to `--report-dir` (see N4, Medium).
- Newman: no schema version in the contract is still open from round 1 (R1:103); unchanged, not re-reviewed (origin=unchanged, minor note).
- Hohpe: WC-4/WC-5 mapping and the pull model are unchanged by this revision (SPEC:63, 70).
- Nygard: the workflow pre-creation STOP now has a defined location (SPEC:62, A1), which closes the failure path M6 named. Unspecified: a stale `return-contract.yaml` left in `--report-dir` by a prior attempt (WC-6 retry, SPEC:64); recorded in the Guard table as Medium.
- The real spec-panel definition already exposes `--report-dir` for exactly this reason (`CMD:23,460`, UNVERIFIED here, outside the workspace). If it holds, SPEC:120 "add `--output`" for spec-panel is stale against it (INV-B:43 says no `--output`); the spec itself states the definition is UNVERIFIED (SPEC:62). Minor note.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Scoped to changed lines. All findings are Medium or minor and sit under follow-up candidates.

- W1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)**, "known before dispatch", fails when **`--unattended` is passed without `--report-dir`**. Concrete attack: `/sc:analyze src/x.py --unattended` with a brief that omits the flag; section 2.3 requires the flag in the brief (SPEC:73), but WC-2/WC-4 give the command no rule for its absence. Before: no contract path. After: the command writes to the cwd (collides with another worker, WC-11, SPEC:69) or refuses with no contract (breaks "every outcome"). Carried from round 1 W3 (R1:114); the changed WC-4 text still does not state the absent-flag behavior. Medium.
- W2. I can break this specification by **Sequence Attack**. The invariant at **WC-4 and WC-6 (SPEC:62, 64)** fails when **a retry worker reuses a `--report-dir` that already holds `return-contract.yaml`**. Concrete attack: attempt 1 writes `status: failed`; the retry (`--retry-of`) dies before writing; the stale file says `failed` or `succeeded` and WC-5 only covers "no report exists" (SPEC:63). Carried from round 1 W2 (R1:113). Medium.
- W3. I can break this specification by **Divergence Attack**. The invariant at **AC-2.3 (SPEC:201, A10)** fails when **a P2 command's happy path hits a gate the brief cannot pre-answer**, which the new cli-portify exception handles by naming the command. Concrete attack: a second P2 command whose gate has no caller flag; the AC has no general rule, so only cli-portify is excepted and the same command-by-command patch is needed again. Minor.

=== GUARD CONDITION BOUNDARY TABLE ===

Triggered: the changed lines contain conditional logic (flag present or absent, step pass conditions, exceptions). Per the Review Loop, in a re-review the table covers guards on changed lines only. Nygard built it, Crispin checked completeness, Whittaker attacked entries.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--report-dir` present | SPEC:62 | Zero/Empty | `--unattended` with no `--report-dir`, or `""` | flag missing | unspecified (W1) | GAP (Medium: requires a guess about a brief that 2.3 says always carries the flag, SPEC:73) |
| `--report-dir` present | SPEC:62 | Typical | `--report-dir /w/out` | true | contract at `/w/out/return-contract.yaml` | OK |
| `--report-dir` vs `--output` | SPEC:62 | Legitimate Edge Case | both flags, `--output` a file | both given | separate flags; contract to the directory | OK |
| `--report-dir` content | SPEC:62, 64 | Sentinel Value Match | directory already holds `return-contract.yaml` | true | unspecified (W2) | GAP (Medium) |
| workflow pre-creation STOP | SPEC:62 | Legitimate Edge Case | STOP before the package id exists | true | contract written to `--report-dir` | OK |
| AC-1.1 load exception | SPEC:195 | Legitimate Edge Case | command is `load` | excepted | excluded from the section test | OK |
| AC-1.1 population | SPEC:195 | Typical | command in the P1 row | true | has `## Unattended mode` naming `return-contract.yaml` | OK |
| AC-0.4 step 3 | SPEC:194 | Typical | existing report file, one `worker_done` | true | passes | OK |
| AC-0.4 step 4 | SPEC:194, 183 | Legitimate Edge Case | `REPORT.md` is not a YAML mapping | undefined | "step 4 uses that file"; must-pass not stated (N2) | GAP (Medium) |
| AC-2.3 cli-portify exception | SPEC:201 | Legitimate Edge Case | cli-portify happy path | gate reached | `failed` plus `status: blocked` naming the artifact | OK |
| cli-portify approval gate | SPEC:105 | Sentinel Value Match | resumed run with `--resume <contract>` | same gate again | ends blocked again, stated by the row (N5) | OK (scope question, Medium note) |
| P1 flag scope | SPEC:159 | Zero/Empty | P2-P4 command run with `--unattended` before its phase | not accepted | flag arrives "in its own phase" | OK |

Classes left out, with reason: Maximum/Overflow for every guard above (no count or capacity enters these guards); One/Minimal for `--report-dir` (a directory-valued flag has no minimal-length class that differs from Typical); One/Minimal and Sentinel for AC-1.1, AC-0.4 step 3 and AC-2.3 (set-membership tests with no sentinel value).
FR-8 GAP rows: three, all Medium (none names a wrong outcome without an extra guess), listed under follow-up candidates. FR-9 blank behaviors: two "unspecified" entries (W1, W2), graded Medium. FR-10: every guard on a changed line is enumerated and every class has a row or a stated omission.

Quantity Flow Diagram and State Variable Registry: not triggered (no multi-stage count pipeline and no `--focus correctness` in this run).

## Follow-up candidates

Medium (warnings, none blocking): N1, N2, N3, N4, N5, W1, W2, plus the three GAP rows above. Minor notes: N6, N7, W3, the stale `--output` for spec-panel (CMD, UNVERIFIED), and the unchanged round 1 Medium and minor items (FC-x, W1-W4 of round 1, R1:100-141), which this scoped re-review did not reopen (origin=unchanged, no changed line depends on them except as noted in N1 to N4).
Issue-opening question: the coordinator session asks the user once for this loop whether to open an issue for these candidates; this worker creates none.

## Coverage

scoped PASS: changed lines + prior blockers
Covered: the diff of 10 changed baseline lines (candidate lines 62, 73, 76, 105, 159, 194-196, 200-201); the six prior blocking ids M1-M6; the lines that depend on them (SPEC:63, 64, 69, 73, 83-92, 99, 100, 112, 120, 154-162, 180-183, 198, 205, 209, 265). Not covered: whole-document assurance (needs a separate labelled first review; any blocker it finds is escalated and does not start a fourth review).

## Reviser brief

Blocking finding ids: none. No revision is requested, and none of N1-N7, W1-W3 may be edited under this loop (Medium and minor findings never appear in the Reviser brief). Rules restated for any later reviser: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report byte size before and after with bytes added and deleted per finding id.

verdict: PASS
