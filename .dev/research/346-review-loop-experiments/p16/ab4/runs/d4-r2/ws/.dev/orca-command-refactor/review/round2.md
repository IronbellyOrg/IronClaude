review: 2 of 3

# Re-review 2 of 3 (/sc:spec-panel --mode critique --focus requirements,architecture --re-review)

reviewer model: claude-sonnet-5-5
candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 520642eef4a21c603b07d310309b173eed3bbf84e2a66e5c9d61cdc65c86fe24
baseline: .dev/orca-command-refactor/specs/history/spec-v1.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
prior: .dev/orca-command-refactor/review/round1.md sha256 e01f41a78dcef52ab9bbf2924a96ed0e0243ac8f9b6eddfc171247c92fd469ef (header `review: 1 of 3`, final verdict FAIL, so N = 2; below the cap, the review runs)
lint: .dev/orca-command-refactor/review/lint-2.md sha256 9af4519073b297f1a4149392cabd92fc78c10682a71b4c364ba92b7c209a214a, "Checks: REF. Findings: 0." Its first line names the candidate hash 520642ee...6fe24, so it was produced on this candidate. No lint id to address (lint-2.md:1-5).
mode notes: roles fixed by the table in the RE-REVIEW prompt (CANDIDATE = @file, BASELINE = --baseline, PRIOR = --re-review). `~/.claude/agents/rf-qa.md` and `.claude/agents/rf-qa.md` are not in the sandbox, so the re-check follows the Review Loop bullets and the RE-REVIEW prompt alone (they stand alone). No Improve step and no revised specification (Review Loop bullet 4). Baseline given, so no `baseline: missing`.
brief clauses overridden: none. The brief neither widens scope nor grades a minor finding as blocking.

## Step 1. Evidence block

Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md` (non-empty; 10 hunks: 62, 73, 76, 92, 112, 149, 159, 194-196, 198, 200). Lines are copied verbatim from the diff output; the leading `< ` / `> ` marker is the diff marker, not text. Spec line numbers: BEFORE lines are baseline lines, AFTER lines are candidate lines (a hunk header such as `62c62` means baseline 62 became candidate 62).

### BEFORE (baseline)

hunk 62c62 < | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |

hunk 73c73 < The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).

hunk 76c76 < The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.

hunk 92c92 < | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |

hunk 112c112 < | load | no gate | none (see note) | n/a | none: use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |

hunk 149c149 < | SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, adversarial and workflow contract gaps, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |

hunk 159c159 < | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |

hunk 194,196c194,196 < | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |

hunk 194,196c194,196 < | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |

hunk 194,196c194,196 < | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |

hunk 198c198 < | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs |

hunk 200c200 < | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |

### AFTER (candidate)

hunk 62c62 > | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). When `--output` is a file (tdd, init-lite) the contract is `<output-file>.return-contract.yaml`; cleanup-audit and index-repo have fixed output locations, so theirs are `.claude-audit/return-contract.yaml` and `PROJECT_INDEX.return-contract.yaml` at the repository root (M7). Exception: adversarial writes `<output>/adversarial/return-contract.yaml`, the path its section 3.1 row names (its artifacts sit under `adversarial/`, `INV-A:35`) (M6). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Workflow is the one command whose path is not known before dispatch: it holds an id the run generates (`.dev/tasks/to-do/<id>/return-contract.yaml`, `INV-B:272`), so the worker takes the single such file created after dispatch, and a workflow stop before the package exists writes no contract (the worker sends `--outcome failed`, WC-5) (M1). Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |

hunk 73c73 > The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line, with `--unattended` only for a command that already has the section (P0 runs without it) and every flag section 3 lists as required; the contract path from WC-4, so the report path is known before dispatch (M5); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).

hunk 76c76 > The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file, at the path WC-4 gives. Every command whose row names an unattended-mode change in P1-P3 also gains the `## Unattended mode` section (section 2.1); brainstorm and init-lite (no change), load (usage line only) and the P4 commands (decisions D2-D4) do not gain it in P1-P3 (M2). Phase numbers refer to section 6.

hunk 92c92 > | workflow | `--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml` | Fresh package each run | None; its path holds a generated id and a pre-creation STOP writes no contract (WC-4) | `sk/sc-workflow-protocol/SKILL.md:58,66,72`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,39,41`; `INV-B:52,267-275` |

hunk 112c112 > | load | no gate | none (see note) | n/a | none: no `## Unattended mode` section, no `--unattended`, no contract; use it as a step inside another worker's brief, not as its own Task; separately, `--checkpoint` is missing from its Usage line | `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` | P1 (usage line only) |

hunk 149c149 > | SA-4 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. Existing lines change only where section 3 names a defect fix (roadmap and validate-roadmap drift, validate-tests target, the adversarial contract filename, explain tools, business-panel frontmatter, load usage line), and each such fix must keep the standalone behaviour or correct a documented defect. | Keeps the diff reviewable and SA-1 checkable. | Section 3 "Other required change" column |

hunk 159c159 > | **P1. Report files and commands with no gate** | The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command whose row names a P1 change (a no-op where a command has no gate); output flags for commands that lack one; the small fixes to ready commands. | analyze, build, business-panel, design, document, explain, index, test, load (usage line only: no `--unattended`, no section, no contract); fixes to adversarial, cleanup-audit, index-repo | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |

hunk 194,196c194,196 > | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker, without `--unattended` (it arrives in P1); the step-5 transcript search also finds no Agent-tool call wrapping the command | steps 1, 2 and 5-7 pass; in step 3 the report path is the command's existing report file (3.1 "Report today" column) and `--outcome` is `succeeded` when it exists; step 4 is `test -s` on that file only, since the contract and its `status` arrive in P1. Record the results in the phase report; a failure here reopens section 1 |

hunk 194,196c194,196 > | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 whose row names a P1 change (not load, brainstorm, init-lite or the P4 commands) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |

hunk 194,196c194,196 > | P1 | AC-1.2 | 7.2 live check on each P1 command except load, with `--unattended` and the output flag its row names, if any (contract at the WC-4 path) | all steps pass |

hunk 198c198 > | P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | adversarial names `<output>/adversarial/return-contract.yaml`, the WC-4 exception path |

hunk 200c200 > | P2 | AC-2.2 | Gate-trigger run per P2 command whose row resolves a gate as blocked (cli-eval, cli-portify, recommend, review-translation, release-split, tdd, troubleshoot, task, and spec-panel with a TDD input): a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait`. The other six (auggie-review, cleanup, improve, research, reflect, tasklist) never write `blocked`: auggie-review is checked by AC-2.4; cleanup and improve by a run whose contract lists the "Approval Required" items unapplied; research, reflect and tasklist by AC-2.3, with step 2 never showing `agentWait` |

Self-check (run with a script, equivalent to `grep -nF`): each of the 12 AFTER lines was found in the candidate and each of the 12 BEFORE lines in the baseline; 24 of 24 found, none swapped. The candidate and baseline hashes above differ, and the lint hash equals the candidate hash.

## Prior blocking findings

Only the ids in the prior report's `Reviser brief` (M1, M2, M5, M6, M7, M8, M9) are prior blocking findings. M3 and M4 were rejected by the verifier (round1.md:11, :83-90) and are notes, not re-checked.

| id | status | basis (AFTER text only) |
|---|---|---|
| M1 | resolved | WC-4 (spec:62) now gives one rule per brief shape: directory (`<output-dir>/return-contract.yaml`), file `--output` (`<output-file>.return-contract.yaml`), fixed locations (cleanup-audit, index-repo), the adversarial exception, and workflow's generated id with the statement that a pre-creation stop writes no contract and the worker sends `--outcome failed`. Section 3.1 now agrees: adversarial row (spec:83, unchanged) names `<output>/adversarial/return-contract.yaml`; workflow row (spec:92) says "None; its path holds a generated id and a pre-creation STOP writes no contract (WC-4)". Section 2.3 (spec:73) points the brief at the WC-4 path. The three-way contradiction round1.md:20-26 described is gone. |
| M2 | resolved | AC-1.1 (spec:195) is now limited to rows that name a P1 change and excludes load, brainstorm, init-lite and the P4 commands; P1 scope (spec:159) says load takes no `--unattended`, no section, no contract; spec:76 says the same for brainstorm, init-lite, load and the P4 commands. The test no longer demands a section in commands whose rows forbid one, and no longer reaches implement, post-release or pr-submit. See N4 for a residual wording gap (Medium). |
| M5 | resolved | AC-0.4 (spec:194) now runs the three smoke commands without `--unattended`, reads the report from the 3.1 "Report today" column, defines `--outcome` as `succeeded` when that file exists, limits step 4 to `test -s`, and moves the Agent-tool wrapper check into the step-5 transcript search it names. Section 2.3 (spec:73) states `--unattended` only for a command that already has the section, "P0 runs without it". Step 3's original text (spec:182) still names the WC-4 contract path, but AC-0.4 overrides it for P0 in the same row. See N3 for a Medium gap (adversarial's report file has no fixed name). |
| M6 | resolved | WC-4 (spec:62) carries the adversarial exception, citing `INV-A:35`; row 83 and AC-1.4 (spec:198) name the same path, `<output>/adversarial/return-contract.yaml`. WC-4, row 83 and AC-1.4 no longer contradict. |
| M7 | resolved | WC-4 (spec:62) names where the contract goes for tdd and init-lite (`<output-file>.return-contract.yaml`), cleanup-audit (`.claude-audit/return-contract.yaml`) and index-repo (`PROJECT_INDEX.return-contract.yaml`), and workflow; AC-1.2 (spec:196) tests "the output flag its row names, if any (contract at the WC-4 path)" so workflow is no longer a P1 command (row 92 has no phase, P1 list spec:159 drops it). The cleanup-audit and index-repo locations rest on `INV-A:42,53` (fixed output dir, `PROJECT_INDEX.md` implied) and the spec's own rows 85-86. The commands the original finding named all have a stated location. Residual gaps for other commands are N1 and N2 (Medium). |
| M8 | resolved | Load is removed from AC-1.1 (spec:195, "not load") and from AC-1.2 (spec:196, "except load"); its row (spec:112) now states "no `## Unattended mode` section, no `--unattended`, no contract". |
| M9 | resolved | AC-2.2 (spec:200) now covers the nine commands whose rows resolve a gate as blocked and gives the other six a stated check each. I verified the partition against the P2 list (spec:160): 15 commands = 9 (cli-eval, cli-portify, recommend, review-translation, release-split, tdd, troubleshoot, task, spec-panel with a TDD input) + 6 (auggie-review, cleanup, improve, research, reflect, tasklist); each of the 9 rows says "blocked" (spec:104,105,115,117,89,90,91,121,120) and each of the 6 has a non-blocking resolution (spec:100,103,110,116,88,122). No command is dropped or counted twice. |

Prior blocking findings still open: none. Regressed: none.

## Findings on lines changed against the baseline

Grading check applied to each: "An implementer who follows the stated text as written builds X, and X is wrong because Y." Every finding below needs a guess about which of two readings the text allows, or names a requirement the document never states, so each is Medium and goes under follow-up candidates. None is blocking.

=== REQUIREMENTS ANALYSIS ===

N1. origin=changed. MEDIUM. Wiegers (consistency), Cockburn. init-lite is given a contract path by WC-4 and no contract by section 3.
- Changed text: spec:62 "When `--output` is a file (tdd, init-lite) the contract is `<output-file>.return-contract.yaml`". Against the changed text at spec:76 "brainstorm and init-lite (no change) ... do not gain it in P1-P3" and row 87 (unchanged) "Small fix: None", `INV-A:55` (re-run overwrites its marked report). Section 2.3 (spec:73) tells the coordinator to put "the contract path from WC-4" in the brief.
- An implementer who follows spec:76 and row 87 gives init-lite no contract, and a coordinator who follows spec:73 and spec:62 tells the worker to report `<output-file>.return-contract.yaml`, which no phase creates. The worker then has no file to pass and WC-5 ("or no report exists") sends `--outcome failed` for a run that wrote its audit. This needs the guess that the parenthetical in WC-4 is only a list of commands whose `--output` is a file, so it is Medium. No acceptance check (AC-1.1, AC-1.2, AC-2.2) names init-lite, so no check fails.
- Recommendation: delete "init-lite" from the WC-4 parenthetical, or state in row 87 what init-lite's report is for a coordinator (its existing audit file). Priority Low-Medium.

N2. origin=changed (depends on changed spec:76 "'Contract' means the WC-4 file, at the path WC-4 gives"). MEDIUM. Fowler (interface), Hohpe. WC-4 still gives no contract location for commands whose new output flag is not said to be a directory or a file.
- Texts: rows add an output path without a kind: analyze "add `--output`" (spec:99), build "add a report path" (spec:101), business-panel, design, document, explain, index, test (spec:102,106-108,111,123), cleanup and improve "add a report path" (spec:103,110), recommend "write the handoff envelope to a file" (spec:115), spec-panel "add `--output`" (spec:120); cli-portify "file location unnamed" (spec:105); research "contract naming the generated `claudedocs/research_*.md` path" (spec:116); cli-eval (spec:104, "contract for both pipelines") and troubleshoot (`REPORT.md`, spec:91) name no contract location. WC-4 (spec:62) names the file case only for tdd and init-lite and the directory case for "the directory the coordinator passed".
- An implementer adding `--output` to analyze chooses a file or a directory; the first gives no WC-4 path (file case names only tdd and init-lite) and the second gives `<dir>/return-contract.yaml`. The coordinator's brief (spec:73) and AC-1.2 steps 3-4 (spec:196, spec:183) need that path, so the implementer's choice decides whether the check can find the file. This is a requirement the document never states, not a contradiction, so Medium. The same applies to AC-2.2's example `/sc:cli-eval run --unattended` (spec:200), whose brief names no output location.
- Recommendation: add one sentence to WC-4 stating the kind of the new output flag as a directory for every command that adds one, and name the contract location in the cli-portify, cli-eval and troubleshoot rows. Priority Medium.

N3. origin=changed. MEDIUM. Adzic (example), Whittaker (sequence attack). AC-0.4 uses the command's "existing report file" but adversarial's has no fixed name.
- Texts: spec:194 "in step 3 the report path is the command's existing report file (3.1 'Report today' column)... step 4 is `test -s` on that file only"; spec:83 "Report today: contract, but filename not fixed"; `INV-A:60` (two real runs wrote `<output>/adversarial/` and `<output>/adversarial/adversarial/`).
- Concrete attack: the P0 adversarial run writes its contract at `<out>/adversarial/adversarial/return-contract.yaml`. Step 3 needs "that file" to give `worker_done --report-path`, but the coordinator cannot name it before dispatch and the 3.1 column names no path. A worker picks whichever file it finds; step 4 passes for any non-empty file. The check can be passed with the wrong file, so it needs a guess about which file counts. Medium.
- Recommendation: in AC-0.4, say the adversarial report is the one file named `return-contract.yaml` found under `<output>` after the run. Priority Low-Medium.

N4. origin=changed. MEDIUM. Wiegers (traceability). The scope of the new section is stated in two terms.
- Texts: spec:76 "Every command whose row names an unattended-mode change in P1-P3 also gains the `## Unattended mode` section"; spec:159 and spec:195 use "a P1 change". Rows 83, 85 and 86 (adversarial, cleanup-audit, index-repo) name P1 small fixes (a contract filename, a final report name, an output location), none worded as an unattended-mode change; WC-4 (spec:62) still gives each an unattended contract path.
- An implementer who reads spec:76 literally adds no section to these three, and AC-1.1 (spec:195) then fails for them; one who reads AC-1.1 adds it. The text allows both readings, so Medium. Recommendation: use "P1 change" in spec:76. Priority Low.

N5. origin=changed. MINOR note. Nygard. Workflow's "the worker takes the single such file created after dispatch" (spec:62) has no rule for two workflow workers in one worktree (WC-11 gives a fresh package per run, `INV-B:272`, but two files then exist). Only a note: the spec does not state the case and no check runs two workflow workers at once.

=== ARCHITECTURE ANALYSIS ===

No new blocking architectural finding. The changed text keeps the single contract-file shape (WC-4 names `status`, `command`, `report_path`, `artifacts`, `blocked_question`), the WC-5 mapping, and the SA-2 rule (no Orca command in a primitive) intact. AC-C5 (spec:176) and SA-4 (spec:149) stay consistent: the SA-4 list changed from "adversarial and workflow contract gaps" to "the adversarial contract filename", and row 92 and spec:159 drop the workflow fix to match.

N6. origin=unchanged. MINOR note, UNVERIFIED. The spec-panel row says "add `--output`; contract" (spec:120, `INV-B:43`), while the definition of /sc:spec-panel supplied to this run already has an `## Unattended mode` section with `--report-dir` and `<report-dir>/return-contract.yaml` (command.md:455-465). That file is not under `inventory/`, so the claim cannot be checked against the stated evidence; if it is the current command, the row is stale and its contract path differs from WC-4. Not graded; no changed line depends on it.

## Adversarial analysis (Whittaker)

- Sentinel collision attack on WC-4 (spec:62): I can break this specification by **sentinel collision**. The invariant at **WC-4 "`<output-file>.return-contract.yaml`"** fails when **a file `--output` already ends in `.return-contract.yaml` or the coordinator passes a path that is also a directory name**. Concrete attack: before, `--output out/report.md`; after, contract `out/report.md.return-contract.yaml`; if the coordinator instead passes `--output out` and `out` does not yet exist, the rule gives no way to tell a file from a directory (see N2). Severity MINOR (behaviour inferrable).
- Sequence attack on workflow (spec:62): I can break this by **sequence attack**. The invariant fails when two workflow workers share a worktree. Concrete attack: workers A and B start; both create `.dev/tasks/to-do/<id>/return-contract.yaml`; "the single such file created after dispatch" is two files for each worker. Severity MINOR (N5).
- Divergence attack on the AC-0.4 outcome rule (spec:194): "`--outcome` is `succeeded` when it exists" and WC-5 "failed when the report says failed" diverge when troubleshoot writes a REPORT.md that records a failed investigation. In P0 there is no `status` field to read, so the P0 outcome is succeeded while the later phases would read `failed`. The text states P0 explicitly ("since the contract and its `status` arrive in P1"), so this is inferrable. Severity MINOR.

## Guard Condition Boundary Table (changed lines only)

Guards on changed lines: G1 WC-4 location choice, G2 workflow contract discovery, G3 AC-0.4 outcome rule, G4 AC-1.1/P1 row filter, G5 AC-2.2 partition. Classes left out are named with their reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--output` is a file | spec:62 | Zero/Empty | no output flag passed (troubleshoot, cli-eval, research) | n/a | none stated for the contract path | GAP (N2) |
| G1 | spec:62 | Typical | directory | false | `<output-dir>/return-contract.yaml` | OK |
| G1 | spec:62 | Typical (file) | tdd `--output <file>` | true | `<output-file>.return-contract.yaml` | OK |
| G1 | spec:62 | Sentinel Value Match | adversarial `--output <dir>` | n/a | exception `<output>/adversarial/return-contract.yaml` | OK |
| G1 | spec:62 | Legitimate Edge Case | `--output out` not yet created | unknown | no way to tell file from directory | GAP (N2, Medium) |
| G1 | spec:62 | Legitimate Edge Case | init-lite `--output <file>` | true | path given, but spec:76/87 say no contract | GAP (N1) |
| G2 workflow contract found | spec:62 | Zero/Empty | pre-creation STOP, no file | none | no contract; worker sends `--outcome failed` | OK |
| G2 | spec:62 | One/Minimal | one file after dispatch | one | worker takes it | OK |
| G2 | spec:62 | Maximum/Overflow | two files (two workflow workers) | two | none stated | GAP (N5, minor) |
| G3 `--outcome` rule in AC-0.4 | spec:194 | Zero/Empty | existing report file absent | false | WC-5: no report, `failed` | OK |
| G3 | spec:194 | Typical | report file exists | true | `succeeded`, `test -s` | OK |
| G3 | spec:194 | Legitimate Edge Case | adversarial, name not fixed | unknown | file not nameable before dispatch | GAP (N3) |
| G4 row names a P1 change | spec:195 | Zero/Empty | load, brainstorm, init-lite, P4 rows | false | excluded | OK |
| G4 | spec:195 | Typical | analyze, build, ... | true | section required | OK |
| G4 | spec:195 | Legitimate Edge Case | adversarial, cleanup-audit, index-repo | true (P1 fix), but "unattended-mode change" false at spec:76 | two readings | GAP (N4) |
| G5 AC-2.2 partition | spec:200 | Typical / Maximum | 15 P2 commands = 9 + 6 | counted | each in exactly one group | OK |

Left out: G1/G2/G5 Sentinel and Maximum classes marked n/a above cannot occur beyond the rows shown; G3 Maximum cannot occur (one report per run); G5 Zero/Empty cannot occur (the P2 list is fixed at 15, spec:160). No Pipeline Dimensional Analysis trigger: the changed lines describe no multi-stage data flow whose counts diverge, other than the 15 = 9 + 6 partition checked above.

## Coverage

Covered: all 12 changed lines (10 hunks) against the AFTER text; each prior blocking finding (7) re-checked against AFTER only; the lines that depend on the changed text (spec:73, 76, 83-87, 92, 99-125, 159, 176, 182-183, 195-200); inventory lines checked: `INV-A:35,37,60`, `INV-B:272`. Not covered: unchanged parts of the document (a scoped review); any citation into `src/`, `cmd/` or `sk/` that is not reproduced under `inventory/` is UNVERIFIED, including the paths named in the prior-resolution table for cleanup-audit and index-repo locations beyond the spec's own rows.

coverage: scoped PASS: changed lines + prior blockers

## Follow-up candidates (Medium and minor; never trigger a revision)

- N1 (Medium): init-lite contract path in WC-4 vs no contract in spec:76/87.
- N2 (Medium): WC-4 contract location for commands that add an output flag of unstated kind, and for cli-portify, cli-eval, troubleshoot, research.
- N3 (Medium): AC-0.4 adversarial report file has no fixed name.
- N4 (Medium): "unattended-mode change" (spec:76) vs "P1 change" (spec:159, 195).
- N5 (minor): workflow contract discovery with two workers in one worktree.
- N6 (minor, UNVERIFIED, origin=unchanged): spec-panel row vs the supplied command definition.
- Review Loop bullet 3: the session that ran the review asks the user once per loop whether to open an issue for these. This run cannot ask and opened none; the coordinator asks.

## Reviser brief

None. No blocking finding is open. (Restated for any later reader: a reviser revises only text a blocking finding names, adds no rule, mechanism or section that no blocking finding calls for, cites the finding id on each addition, prefers deleting or narrowing, and reports byte sizes before and after with bytes added and deleted per finding id. Medium and minor findings are not part of any reviser brief.)

verdict: PASS
