# Ponytail measurement validity

## V1. Review loading and report markers
**PASS for observed command activation and re-review structure, not experiment success.** Deduplicating tool IDs gives one actual `Skill(sc:spec-panel-armb)` call per review: T05 source log line 43, T07 line 148, T09 line 60. Each result says `Launching skill`. Source paths, result-line pointers and exact arguments are retained in `reviews/session-summary.json` and `reviews/T05-tools.jsonl`, `T07-tools.jsonl`, `T09-tools.jsonl`.

| Report | Review header | Reviser brief | Last nonempty line | Re-review structure |
|---|---|---|---|---|
| `reviews/spec-panel.md` | line 3, `review: 1 of 3` | lines 169-171 | line 173, `verdict: FAIL` | First review, no flags |
| `reviews/spec-panel-round2.md` | line 3, `review: 2 of 3` | lines 202-204 | line 209, `verdict: FAIL` | Status table lines 19-38; all 15 numbered rows tagged changed at lines 167-181; flags honoured |
| `reviews/spec-panel-round3.md` | line 3, `review: 3 of 3` | Absent, cap escalation at lines 189-195 | line 201, `verdict: FAIL` | Seven prior-blocker rows at lines 27-33; zero verified new findings at line 101; prior minor M3 tagged unchanged at line 105; flags honoured within this scope |

New severity-label proxies are 9, 7, 0; blocking grades are 8, 7, 0. Round 3 nevertheless FAILS the original any-severity brief because prior minor M3 remains open. The owner-rule carry-forward additionally retains the partly rejected round-1 MAJOR note N1, giving final owner critical+major count 1, not a clean PASS. No fourth review was performed.

**CONTRADICTION R3-N1:** round-3 line 29 promises a new finding `R3-N1`, but lines 99-105 contain no such finding; lines 110, 111 and 174 explicitly reject that fixed-state-retry hypothesis. Record this orphan cross-reference and unresolved authorial intent. The numbered-list proxy is 0, with one additional ungraded candidate as a sensitivity limit, not a confirmed MAJOR. The automated citation-row blockers and owner zero are invalid measurements (`reviews/fix-audit/final-verdict.md:1-10`).

## V2. Starting document and final endpoint
**PASS for exact byte recovery.** `reviews/source-manifest.json` and `reviews/sizes.txt` preserve sizes, newline counts, source mtimes and SHA-256. Starting `reviews/spec-v1-draft.md` is 57,763 bytes, 285 newlines, SHA-256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`, matching the required frozen input. After cycle 1: 65,568 bytes, 288 newlines, SHA-256 `290d8b515337d4e45a786caa6482b59426384a3d2ccbf15adf64a35262de6da3`. After cycle 2 before audit: 70,579 bytes, 290 newlines, SHA-256 `d87d64ce356122fac14b26e5b25a7eb3109e12706d9d8f55df198b36d14c358f`.

Live spec at recording matches the required endpoint exactly: 70,488 bytes, 290 newlines, SHA-256 `2d74ef94e35ad1f5762ec1e118aec05de6759321cf3bdfff852ab653ebff0509`, copied as `reviews/live-spec-at-recording.md`; no overwrite was needed. `reviews/fix-audit/current-before-audit.md` matches the pre-audit history copy; `state.json:103-104` stores that input and baseline hash; `apply-log.md:25-26` stores the before/after hashes. State's current hash is prepare-time, not final; `state.json:396` records applied status. The audit changes only source lines 68 and 158, net -91 bytes. Report descriptions sometimes count the unterminated final physical line (289/291); comparisons here consistently use newline counting, as `wc -l` does.

## V3. Answer-key exposure (covariate)
**PARTIAL as an exposure assessment; recorded as a covariate, not a voiding verdict.** Scanned the seven mapped logs (setup plus six loop steps), deduplicating tool IDs, for `origin/master`, `git show`, `git log`, `WORKER-CONTRACT.md`, and new review-command paths. No actual tool-input hit reads origin/master or the installed finished WORKER-CONTRACT. No numbered finding in any round cites or reuses those answer sources: observed counts 0/0/0, based on the finding lists, not a claim about inaccessible model context. Original overlay references to a proposed contract are not reads of a completed answer.

| Step | Session prefix | Explicit answer-key read hits | Expected additive-command access |
|---|---|---:|---|
| Setup | 451068bb | 0 | None |
| First review | f952f6b0 | 0 | `sc:spec-panel-armb`, original line 43 |
| First revision | b40038ce | 0 | None |
| Second review | 53f4dc61 | 0 | `sc:spec-panel-armb`, line 148 |
| Second revision | faf6c276 | 0 | None |
| Fix audit | ee16dad7 | 0 | `sc:spec-panel-ponytail`, line 60; `ponytail:ponytail-review`, line 117; fix-audit skill/script read at lines 80,163,178 |
| Third review | 52877e84 | 0 | `sc:spec-panel-armb`, line 60 |

Evidence: `reviews/*-tools.jsonl`, `access-hits.json`, `session-summary.json` map each hit to original session path and original line; `system-context-exposure.json` reports zero WORKER-CONTRACT/origin-master references in stored system-message blobs. The installed master contract was nevertheless present, unlike the controls and flagged Arm B, and remains a possible unobserved exposure route. Its present-state hash at recording is `5fbf2f2e201bd40c98d21348814f5b94d3dadc48697722fed1fa8e031b6f7698`; install presence is logged in `reviews/governing/phase5__install-log.md:2`.

**Audit access:** the T08a handoff forbids review 3 reading `fix-audit/audit.md` (original T08a line 284; retained in `reviews/T08a-tools.jsonl:18`). T09 actually reads `apply-log.md`, `fix-list.md` and `state.json` in its original line 117 Bash call, then reads `apply-log.md` again at original line 518 (`reviews/T09-tools.jsonl:6,51`). No tool input reads `audit.md` itself. Its existence appears in directory/output text, which is not a content read. The reviewer was not blind to the audit's applied result and revert, but that is different from violating the narrower audit.md prohibition; both facts are retained.

## V4. Dispatched briefs and substitutions
**PASS for the stated variant's dispatched brief construction, not literal identity to the old unmodified experiment.** Each actual first task message equals its saved filled brief after exactly one original-repository-root replacement. Full source/dispatched hashes and exact word-level substitutions are in `reviews/brief-comparison.json`; exact dispatched bodies are in `reviews/dispatched/`. The coordinator logged the hash of the pre-root-substitution file, not the actual injected text; the two hash columns must not be mistaken for mismatches.

| Step | Pre-substitution brief SHA-256 prefix | Dispatched text SHA-256 prefix | Substitutions beyond the root |
|---|---|---|---|
| First review | 1840727834a6 | 868b95765763 | `/sc:spec-panel` becomes `/sc:spec-panel-armb` |
| First revision | 28fdd09ed70b | b51ce3fdc5b4 | None |
| Second review | 590d8c620d32 | b036ce08e490 | Count placeholder becomes 16; reviewer command becomes armb; append `--re-review` round-1 report and `--baseline` v1 history |
| Second revision | 2f23d14149b0 | 8583c68a00ac | Both finding-range placeholders become `NF1-NF7 and M1-M8`; citation-count placeholder becomes 2 |
| Inserted audit | 6a3267007db8 | 9b2bc7c1b1dd | Added experimental step, not a historical baseline task |
| Third review | 077e7a13e055 | bf796594bd2b | Finding range becomes `NF1-NF7 and M1-M8`; command becomes armb; append prior round-2 report and v2 baseline |

Saved unfilled variant briefs also show the intermediate replacements: second-review count 22 to 16 (not the original historical 24); second-revision and third-review range `R2-1 to R2-12` to `NF1-NF7 and M1-M8`. The second-reviser brief still says two overstated citations, while its report treats C8 as overstated and C11 as a combined-support note; it explicitly disposes both (`reviews/disposition-round2.md:8,36-39`). No covert switch to a blocking-only reviser range occurred: all eight optional minor rows were still in scope. The final any-finding-of-any-severity FAIL sentence is unchanged (`reviews/dispatched/T09.txt:1`). Sources: copied original task text/templates in `reviews/original-briefs/`, filled and unfilled variants in `reviews/briefs/`, coordinator log lines 20,29,42 and launch receipts in `reviews/driver/`.

## V5. Environment and session efficiency
**FAIL for a same-model controlled comparison; environment is otherwise recorded.** All launch receipts request and initially report `claude-opus-5-5`, but resumed third-review assistant records are labelled `gpt-6.1-sol` starting at original source line 267. The source log records a local `/model` action at lines 243-245 and `resume` at 247. This is observed response metadata, not an inference from the coordinator's requested model. First-review terminal reuse later also shows that response model, after the original first review had already completed, so it is excluded from that review's primary cost.

| Environment fact | Observed evidence |
|---|---|
| Worktree base | `2cb683f5c1f0dfbd3c5f169a8b64a432931f718e`, current HEAD and setup evidence |
| Claude Code | `2.1.319` in all seven source logs (`reviews/environment-evidence.json`) |
| Orca build at recording | `1.4.245-aidev02.780594c521aa`; historical per-step build equality is not proved by the current version command |
| First two reviews, both revisions, audit | Source assistant model `claude-opus-5-5` during assigned work |
| Final review | Opus before interruption; three synthetic rate-limit records; `gpt-6.1-sol` after local model selection |
| Blocking/minor and three-review rule in global prompt | Present in 6/6 loop-step stored system-message blobs, also setup: original source lines T05=33, T06=30, T07=31, T08=30, T08a=31, T09=31; excerpts in `reviews/global-prompt-rule-evidence.json` |
| Audit context isolation | Its own fresh top-level session, separate from both revisions and all three reviews; actual ponytail review Skill call, no Agent call |
| Reviser-spawned sub-review | Zero Agent/Task calls in either revision, and zero in all six loop sessions; no subagent JSONL files found under the mapped project directory |

| Assigned step | Calls | Logged output tokens | Wall minutes |
|---|---:|---:|---:|
| First review, original segment | 24 | 42,466 | 6.8492 |
| First revision | 56 | 45,846 | 7.4239 |
| Second review | 31 | 59,074 | 9.5590 |
| Second revision | 48 | 46,161 | 7.4132 |
| Added audit | 18 | 18,713 | 3.2537 |
| Third review, interrupted/resumed | 97 | 27,368 | 83.5907 |

Total 274 tool calls and 239,628 logged output tokens exclude setup and first-review terminal reuse; all input/cache usage fields remain in metrics.json. Method: baseline's assistant-message-ID grouping with last usage per ID; raw assistant tool-use and unique tool-ID counts agree. Full-session and through-delivery costs are also retained in `reviews/session-summary.json`. The original T05 segment ends at source line 357, not at later API-request metadata line 360. These are provider-reported usage and elapsed spans, not billing-equivalent tokens or active compute time across different providers.

Third-review 429 errors occur at 00:34:57, 00:55:11 and 01:33:24 UTC; same-task resumes are at 00:52:16 and 01:30:22, followed by the local model selection at 01:35:28 and resume at 01:35:29. See `reviews/interruptions-and-later-users.json`. The coordinator driver's three 25-minute stalls are distinct from API error times (`reviews/driver/driver-ponytail.log:17-25`). Same Dispatch was reused, not a new review, but same-model continuity was broken.

## V6. Isolation, install state and later writes
**PARTIAL for continuous isolation/install proof; known parser failure preserved, no observed endpoint drift.** Installed variant hashes now equal the install log: armb `00cab10e9ffd1a3e908895508cfb0620486c07f25e0222ac5890bee63068dff4`, ponytail command `6f5612782eb8b50f86929ade75a096f3b3c9cee53abb4430558eaf3dba6d2137`, audit script `f7d0cfd9238c06d063444c50c13a8576612e7fc648581930fb882590885d4524`. The base spec-panel install log says unchanged `4115f2a979800af8b3ed8dee9d006cf3a97e25c5d9e02420cfee761e82cbe3c9`, and WORKER-CONTRACT was present. `reviews/installed-hashes.json` records the observed variant endpoints. The historical watcher only tracks base spec-panel and contract presence; its last transition is 2026-11-08 13:57:47, well before this 23:47 to next-day 01:46 loop. It does not continuously attest additive variant files or rule out an intervening change-and-restore. No install was run by this recorder.

The last loop worker_done is the third review at 2026-11-09 01:46:21 UTC, confirmed by its successful send result and supplemental lifecycle event (`reviews/driver/last-ponytail-T09.json`; original T09 tool lines 918 and following; `reviews/driver/ponytail-events.jsonl`, original router line 77). The spec mtime is 00:24:48, round-3 report mtime 01:46:05. All copied loop artifacts precede the final delivery EXCEPT `fix-audit/final-verdict.md`, written by the expected coordinator verdict shell step at 01:46:22.651. That later write is disclosed, not silently treated as an untouched loop. At recording the live endpoint hash matches the required final hash; core-loop copies and their source mtimes are in `reviews/source-manifest.json`.

First-review terminal received human text after its earlier delivery: `Run Task 6 to revise the spec for F1-F8` twice at 01:35:05 and 01:35:12, original T05 lines 361 and 392. Later tools read the current spec/reports, but no later Write/Edit/Bash mutation is logged there. Final-review terminal received a local model change before completing, and an automatic visible-output request after delivery; no post-delivery file mutation is logged in that session. This is bounded transcript evidence, not a whole-machine write audit. Human terminal contact therefore exists even though no spec drift was observed.

**Driver and shell exits:** copied `reviews/driver/driver.sh:23-25,51` maps a pause to exit 10, shell failure to 11, stall to 15. Its log shows history-copy steps advance and the three pauses; the three stalls resume the same Dispatch. Six worker_done events report task outcomes succeeded. Final `seq-ponytail.txt:12` runs the verdict script, not another review; `driver-ponytail.log:27-38` preserves its failure output, `status-ponytail` says `SHELL STEP FAILED: verdict`, and `state-ponytail` remains 11 (not sequence complete). The verdict script's no-resolution-row path returns 2 (`reviews/installed/fix_audit.py:1025-1028,1092`); driver then returns 11. History shell success is established by advancement, not a separately logged numeric receipt. No parser rerun, repair or fourth review was performed.

No tracked source change or commit is observed: current HEAD still matches setup and `git status --short` shows only the untracked loop folder and recorder output folder. No commit/push/install command is present in mapped worker tool calls. This recorder did not stage anything, consistent with the task's explicit index prohibition. Continuous monitoring is insufficient to certify that no other process ever touched source or machine-wide files.

## Evidence-package quality verdict
**PASS: evidence-package quality only.** The four required outputs exist, JSON parses, source reports/snapshots are copied with metadata, and 74 executable assertions verified report counts, exact hashes, source stability, audit edits and principal arithmetic (`reviews/count-and-integrity-checks.json`). Final inventory and package checks are retained under `reviews/`. Known validity failures and recovery limits are explicit, not hidden behind a zero-blocker claim. This does not pass the original final report or establish variant success.

## Self-Audit
This is not a zero-issue result: the parser failure, resumed-model mismatch, orphan cross-reference, stale disposition after audit, optional MAJOR carry-forward and incomplete continuous integrity proof were actively sought and retained. Checked original severity rows rather than the script's totals; deduplicated prior aliases; compared all seven final resolution claims with the endpoint's named correction text; checked M3's reverted line and M6's actual trim; verified start/pre-audit/final hashes; inspected actual Skill IDs/results, global system-message excerpts, late user messages, mutation tools, launch receipts and driver exits; checked comparator arithmetic without remeasuring controls. No additional model review, source fix, parser run, install, staging, commit or publication was performed. Rejected Edit attempts on unread report stubs were blocked by the freshness hook; the files were then Read and edited normally, with no bypass. Evidence checks establish the package's fidelity, not future command implementation or runtime correctness.
