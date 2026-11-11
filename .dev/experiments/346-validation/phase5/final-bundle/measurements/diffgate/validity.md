# S1 diffgate validity

## V1. Review structure and actual invocation
**PASS for observed variant invocation and preserved verdicts; not strict original-instrument equivalence.** All three reviewers actually called `Skill sc:spec-panel-diffgate`: session `0e40ed15` line 92 (round 1), `ba3e4a04` line 143 (round 2), `816a3832` line 88 (round 3). These are tool-call records, not merely report claims or command-file reads. See `reviews/*-session.json` for full session IDs, arguments, command reads and transcript paths.

| Report copy | Review header | Literal `## Reviser brief` | Inline reviser brief | Last nonblank line |
|---|---|---|---|---|
| `reviews/spec-panel.md` | line 3, review 1 of 3 | absent | line 152 | line 154, `verdict: FAIL` |
| `reviews/spec-panel-round2.md` | line 3, review 2 of 3 | absent | line 165 | line 167, `verdict: FAIL` |
| `reviews/spec-panel-round3.md` | line 3, review 3 of 3 | absent | absent, escalation instead | line 163, `verdict: FAIL` |

Round 2 has prior-resolution rows and five new findings; round 3 has prior-resolution rows and three new findings. Machine origin labels are 4 changed/1 unchanged in round 2 and 3 changed/0 unchanged in round 3. Those labels alone are not causal origin measurements. Report 3 escalates two blockers at the cap; no clean PASS occurred. The coordinator, not the reviewers, appended the closing/verdict blocks after checking the reports. `reviews/diffgate-loop/report-rN.md` preserves the pre-append checked report; `reviews/spec-panel*.md` preserves the final report. Absence of a literal heading is a format fact, not silently treated as an absent task-list file.

## V2. Start and endpoint identity
**PASS for frozen-input identity.** SHA-256 was verified before measurement, independently of the report claims:

| Snapshot | Bytes | Newline count | SHA-256 |
|---|---:|---:|---|
| `reviews/spec-v1-draft.md` | 57763 | 285 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| `reviews/spec-v2-after-round1.md` | 62054 | 285 | `6c68d0ece899759096d1d8e35226720deeb59e96e771d6f47232364e4a628d17` |
| `reviews/spec-v3-after-round2.md` | 63717 | 285 | `75a628e35b00eb23bde80d0190f6cf735f3b298c8f3b228caf05f65ee094ac9a` |

Each matches the corresponding loop `doc-rN.md` byte-for-byte by hash. `reviews/spec-final-frozen.md` is another copy of version 3, NOT the live externally replaced specification. The original is an untracked overlay, not a tracked file at base commit `2cb683f5`; no attempt to reconstruct it from that commit was used for this measurement. Source copies retain source timestamps, with their original paths, sizes and hashes in `reviews/sources.json`, `reviews/SHA256SUMS` and `reviews/sizes.txt`.

## V3. Answer-key exposure (covariate)
**PARTIAL as an isolation claim; recorded exposure is a covariate, not an automatic rejection.** Within the five loop dispatch windows, actual inspection calls referencing master/finished-contract material were found in round-1 review and its revision. None were found in round-2 review/revision or round-3 review by the same argument search. This is a lower-bound observation of explicit reads, not proof that surrounding context had no influence.

| Session / step | Transcript line | Material inspected |
|---|---:|---|
| `0e40ed15`, round-1 review | 165 | `git log HEAD..origin/master`, ancestry and current checkout checks, plus global/repo command-invocation rules |
| same | 174 | `git ls-tree origin/master` command names, `git grep` for Orca invocations including new commands, and master commit identity |
| same | 189 | master `WORKER-CONTRACT.md` lines 1-40 and history; master installer registration and routing-guide Orca count |
| same | 235 | master contract Skill and Orca examples; later implementation commit messages `f3c1ef062` and `38eb3c58a` |
| same | 312 | master contract report-directory, `worker_status` and flag-parsing lines |
| `3b1f3d8e`, round-1 revision | 170 | resolved master commit plus contract lines 13, 15, 32, 35 and 101 |

Full commands, timestamps and source transcript paths appear in `reviews/session-metrics.json` under `answer_key_tool_hits`. The raw search additionally catches round-1 `worker_done` message bodies at review line 472/revision line 455; these are outgoing descriptions, NOT reads, and are excluded from the six actual inspection calls above. Multiple master reads inside a single shell command remain one tool call, not one document read.

Three numbered round-1 finding rows explicitly cite master-related corroboration or later implementation: the no-Orca scan finding (R1.5), stale-baseline finding (R1.9), and transcript-evidence finding (R1.12). Round-2 and round-3 new numbered rows contain none under that definition. Generic references to the proposed contract file are not automatically answer-key reuse. The first reviser explicitly says its directory/field/parse choices agree in substance with master in its disposition, so this is genuine exposure, not just a failed lookup.

The frozen-audit report says earlier reviews/loop/live target were not opened; its tool arguments can be checked in the bounded session evidence. The retired mixed audit is retained solely to document failure, never used for endpoint counts. No exposure verdict is inferred from its partial contents.

## V4. Dispatched briefs and substitutions
**PASS for exact delivered-text reconstruction; PARTIAL for historical comparability because the treatment changes both review and revision scope.** All seven first delivered TASK blocks match their saved variant brief after exactly the logged repo-root replacement (one replacement in each loop brief and retired-audit brief; none in frozen-audit brief). Full source/delivered hashes are in `reviews/session-metrics.json`; original and dispatched copies and exact token deltas are in `reviews/briefs/` and `reviews/briefs/substitutions.json`. The source hash prefixes match the dispatch log: `b7489f94743f`, `7c25f73c621e`, `dbbb20fd61c9`, `e8b95d06e844`, `dea0f0af68c5`, `d85a967eb766`, `403e566df869`.

Substitutions relative to the original task-text sources:
1. Every loop reviewer: `/sc:spec-panel` becomes `/sc:spec-panel-diffgate`; append `--diffgate-dir .dev/orca-command-refactor/review/diffgate-loop --expect-round N` for that review.
2. Second reviewer: prior count 24 becomes 13. Third reviewer: old finding range becomes R2.1-R2.5; both overstated citations becomes every overstated citation. The any-severity FAIL sentence remains unchanged.
3. Second reviser: N1-N13 becomes R2.1-R2.5; the 2/both citations becomes every overstated citation. Both revisers receive an additional paragraph making the generated blocking-only reviser task list authoritative instead of the whole report, requiring a fix-map block and successful read-only fixcheck. This is a substantive scope change, not merely a flag rename.
4. Repo root in delivered loop TASK text changes from the historical missing checkout to this worktree. The draft spec's own stale-root text is not rewritten by that substitution.
5. Retired audit's original request incorrectly sought an untracked original via `git show` and equated changed text with a closed finding. It failed. The fresh audit is a new explicit brief with frozen paths/hashes, actual `Skill sc:spec-panel-armb`, no prior reviews, no live target and no such causal assumption. This is a documented audit-protocol deviation, not a resumed successful original audit.

Observed revision scope: first reviser applies 7 blocking findings and rejects 6 minors; second applies 3 blockers including the carried retry issue and 1 minor citation within an already-owned hunk. Its 11 disposition rows contain duplicate citation entries and one no-change-needed entry, so they do NOT mean 11 distinct findings. Neither reviser spawned a sub-review. The historical and control revisers generally acted on all confirmed findings, so smaller growth here cannot be credited to computed review surfaces alone.

## V5. Runtime environment and step isolation
**PARTIAL: loop environment is recorded, but independent-audit environment differs and exclusive work time is not recoverable.** All five loop steps have distinct session IDs and all real assistant messages before their matching completion report identify `claude-opus-5-5`, matching the controlled-comparison loop model. Claude Code version is `2.1.319` in all seven task windows. Orca `1.4.245-aidev02.780594c521aa` is observed in loop help/version receipts (round-2 reviewer line 256, second reviser line 155, round-3 reviewer line 170); setup and live tool availability are not inferred from a model banner.

| Step | Session prefix | Model in real assistant records | Tool calls | Output tokens | Dispatch-window minutes |
|---|---|---|---:|---:|---:|
| Review 1 | `0e40ed15` | claude-opus-5-5 | 34 | 45642 | 7.496 |
| Revise 1 | `3b1f3d8e` | claude-opus-5-5 | 49 | 33674 | 5.184 |
| Review 2 | `ba3e4a04` | claude-opus-5-5 | 39 | 52422 | 7.952 |
| Revise 2 | `efdd7e2a` | claude-opus-5-5 | 37 | 32934 | 5.398 |
| Review 3 | `816a3832` | claude-opus-5-5 | 27 | 42509 | 6.865 |
| Retired mixed audit, excluded | `f7f8a82c` | claude-opus-5-5 then gpt-6.1-sol | 31 | 7315 | 64.712 |
| Fresh frozen audit | `4ea38812` | gpt-6.1-sol | 71 | 37373 | 22.567 |

All seven task windows contain the global minor-never-fails and two-fix-cycle/three-review rules in attached instructions: round-1 reviewer line 18, first reviser line 16, round-2 reviewer line 17, second reviser line 16, round-3 reviewer line 17, retired audit line 17, frozen audit line 18. Thus global grading is a common background condition, not an isolated effect of the variant. User/task text that says any severity FAIL coexists with those instructions; no clean PASS hides that disagreement.

Method: same assistant-only tool-block count and last-usage-per-message-ID sums as REPLAY section 6. Input and both cache-token classes are retained in `reviews/session-metrics.json` and `metrics.json`. Primary windows end at the matching `worker_done` invocation; baseline-form whole-session totals remain separately in that file. This restriction is necessary: the first-review session was later reused for unrelated user-owned amendments. No later tools, tokens, model switches or helper agents are attributed to review 1. None of the five loop workers spawned a helper or reviser-owned review within its window.

The frozen audit did spawn one existing report-quality helper: its separate log identifies gpt-6.1-sol, 21 tools and 5469 output tokens, from 01:46:22 to 01:53:22. It is not included in the audit's 71 main-session tools/37373 tokens, and it was not an extra spec fix round. No additional live-model review was launched by this recorder.

Interruption evidence: the retired audit has terminal 429s at 00:35:08 (line 145) and 00:55:07 (line 164), a coordinator resume at 00:52:14 (line 150), and user model switch/resume at 01:18:16-19. Its first subsequent real model response is 01:18:23: observed error-to-response gap 43.248 minutes, residual wall time 21.464 minutes. The frozen audit also hit a terminal 429 at 01:34:44 (line 51); after user model selection and resume, first real response is 01:35:27, a 0.721-minute observed gap, residual 21.846 minutes. These residuals are not exact active-work measurements: retry/wait time before terminal errors and ordinary idle/tool waits remain unknown. No terminal API error was found within the five core loop windows.

The coordinator shell ran begin/check/fixcheck and history copying, rather than separate worker steps, as the dispatch log explicitly records. Reviewer/reviser dry runs are included in their tools; authoritative script calls and coordinator overhead are not. This limits token/time comparability with pipelines that allocate those script steps to separate workers.

## V6. Install stability and external edits
**FAIL for untouched live-target history; PARTIAL for install stability; frozen-input measurement remains recoverable.** The live target was externally replaced after the loop and during the failed audit. The first review's later user prompt at transcript line 487 (00:41:50) requests seven amendments and explicitly says revise against current master; the same session later writes the live spec at line 933 (01:22:31) and incrementally edits it. The coordinator log describes this as a current-master amendment dated 01:19Z. The actual observed write starts later than that embedded amendment date. The recorder neither opened nor measured nor overwrote the live target. Frozen version 3 and loop `doc-r3.md` remain hash-identical.

**Recorded versus observed installation:** `reviews/provenance/phase5/install-log.md` records the additive variant installs and says WORKER-CONTRACT is present. At recording time, the installed command/script hashes match that log:
- diffgate command: `d144aa097ea1558515848cc44efe6837f9f47e42db20a84fcccc68328fbaa4e1`;
- Arm B audit command: `00cab10e9ffd1a3e908895508cfb0620486c07f25e0222ac5890bee63068dff4`;
- diffgate skill: `4e2adc073525c1a4e6aec77f3bc718369822ff8664e2aac3ff07628fc35df193`;
- diffgate script: `6832190d5c7219357e37dcf7c21c05ad6807ea3068994a8fa5fef0c623b266d0`.

The installed original command is `4115f2a979800af8b3ed8dee9d006cf3a97e25c5d9e02420cfee761e82cbe3c9`; current WORKER-CONTRACT is present with hash `5fbf2f2e201bd40c98d21348814f5b94d3dadc48697722fed1fa8e031b6f7698`. Its presence contrasts with the controls/Arm B isolation design where it was moved aside. Loaded user-message bodies at review-session lines 101, 148 and 93 match the current diffgate command body verbatim, excluding frontmatter and the appended invocation arguments. The frozen auditor's loaded body at line 95 similarly matches the Arm B alias, despite its heading retaining the generic panel title. See `reviews/instrument-hashes.json` and `loaded_command_evidence` in `reviews/session-metrics.json`.

The supplied watcher, `reviews/provenance/phase4/install-watch.log`, ends at 2026-11-08T13:57:47Z, hours before this loop. It cannot establish continuous phase-5 stability of commands or WORKER-CONTRACT. Matching install/current/loaded-body evidence supports instrument identity at observed points, but is NOT a watcher PASS over the whole task span.

**Report history and timestamps:** authoritative checks append closing blocks at 23:56:00, 00:11:03 and 00:25:31, slightly after reviewer completions at 23:55:56, 00:11:01 and 00:25:29. These are explicit coordinator mutations, not hidden post-review revisions. Each final report is compared with its checked snapshot plus closing block in the package check. The two dispositions and three history snapshots have mtimes before final loop completion; final file metadata/hashes are retained in `reviews/sources.json`. A timestamp alone cannot prove no intervening edit-and-restore. Later human input to the completed first-review session and the live-target write are documented deviations.

The retired audit is preserved but excluded from counts; its dispatch ended failed for target drift and missing tracked baseline. A fresh, separately dispatched audit uses frozen endpoint and overlay snapshots, explicitly calls the Arm B alias, and completes after report-only validation corrections. This is a replacement audit, not a claim that the interrupted audit succeeded unchanged.

HEAD was observed as `2cb683f5c1f0dfbd3c5f169a8b64a432931f718e`; the staged-file list is empty and status shows only untracked experiment/overlay directories. The recorder stages nothing, changes no loop file, installs nothing and sends no external publication. All its explicit file writes are inside the assigned evidence directory. The scoped session/tool evidence shows no commit/push in the measured loop; this is not an audit of every unrelated session on the machine.

## Evidence-package self-check
**Self-Audit:** deterministic package assertions independently recompute frozen hash/size identity, numbered severity counts, carried-prior separation, script agreement, changed-line containment, exact growth, threshold arithmetic, source-copy checksums and pointers, exact delivered briefs, model/Skill evidence and token totals. They also prove each final review equals its checked snapshot plus the coordinator closing block. Source reports and frozen snapshots are rehashed against the captured copies before completion. Results and the runnable check are in `reviews/package-check.json` and `reviews/package_check.py`; this is a data-consistency check, not a new live-model specification review.

Manual self-check compares every audit failure mechanism with each of the two endpoint blockers before union arithmetic, separates duplicated citation rows from findings, and verifies that no critical/major deferred/demoted/withdrawn finding is hidden in earlier rounds. No unresolved package defect remained after corrections. The audit union is not silently swapped for the original comparator proxy.

Negative verification evidence retained rather than hidden: the guessed supplemental directory `/tmp/impl/s1v/diffgate` did not exist, so file discovery found the actual briefs directly under `/tmp/impl/s1v/briefs/diffgate`; an initial bounded jq query failed to compile because the optional-field/default operator lacked spacing and was corrected; the first two report edits were rejected by the freshness hook until the freshly written report was read, after which normal Edit calls succeeded. An unnecessary `uv --no-sync` option produced a no-effect warning and was omitted on later runs. A first loaded-body lookup restricted to string messages found nothing because command bodies use text blocks in array messages; the corrected extraction recovered them. The Arm B alias keeps a generic panel heading, so its source was resolved from the actual Skill argument rather than its title. Draft growth decimals were corrected to exact arithmetic before the package checks. A separate `sha256sum -c` check was initially launched from the worktree root although its manifest names paths relative to `reviews/`, so it reported missing files; the deterministic checker had already validated every manifest entry with its explicit base directory, and the shell check was rerun from the manifest directory. None of these failed lookups was turned into a zero measurement or a successful observation.

The quality verdict concerns a complete, internally checked evidence package with disclosed unknowns. It does not approve experimental validity, the specification, or treatment success. No independent additional model review, fix pass, installation, staging, commit, push or publication was performed.
