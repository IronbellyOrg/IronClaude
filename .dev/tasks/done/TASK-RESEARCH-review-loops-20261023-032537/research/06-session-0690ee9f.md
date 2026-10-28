# Research: credential implementation final-review failures

**Investigation type:** Root-cause analysis  
**Scope:** Frozen manifest index 15 only, with its nested reviewers and historical package evidence  
**Status:** Complete  
**Date:** 2026-10-23


**Persistence note:** Main session transcribed the complete dedicated analyst return verbatim from its on-disk transcript because that agent cannot write reports. No producer-authored disk delivery is claimed.

## 1. Result and counting

This session contains **two independent final-review incidents**, not repeated implementation attempts on one task:

| Package | Observed sequence | What actually changed between final reviews |
|---|---|---|
| Initial five-key shell change, four tasks | Final issues, evidence correction, final pass | A missing durable lint comparison was saved and its ledger citation corrected. No delivery-file change. |
| Key-source documentation follow-up, 17 tasks | Final issues, owner acceptance and evidence corrections, second final issues, further evidence corrections, third final pass | Owner accepted a pre-existing lint exception; ledger pointers were repaired. No delivery-file change. The installed final-review rubric also changed before the third review. |

**Do not classify the second failure as a fix introducing a new code defect.** Its blocking finding was a Task 10 citation that was already wrong before the first final review. The first review missed it.

The package delivery-state digests stayed unchanged throughout their respective final-review sequences:

- Initial package: `7ecdaa02bf2b9f1c7d9acf9fd8a4aae7b73ab1288bb762dd4796f3ef382f6634`
- Follow-up package: `8e0459560c10d2c0a70481ebe3b9c348dbe6581f4b2872a7ed29ee05109f61b2`

These are historical helper results recorded in the original transcript, not fresh claims that the present worktree still has that content.

**Key takeaways**
- The repeated failures concern evidence handling and acceptance-rule interpretation.
- There is one genuine later-task line shift, several citations wrong from their creation, and one known literal criterion accepted prematurely.
- The final pass is not a controlled retry under an unchanged rubric.

## 2. Primary source and integrity

**Original parent transcript**

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl`

- Physical records: **2095**
- Observed SHA-256: `7da194916ee6f359c2c3058ae94bcc00ea599ac507b8a4b1bcbee5d3df8f8a7f`
- Frozen population membership verified at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/session-manifest.txt:16`.
- All record numbers and timestamps below refer to original JSONL records, not extracted-output line numbers.

**Archived package locations**

1. `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/`
2. `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/`

Both archived directories exist. Both corresponding `to-do` directories are absent. Original archive helper results also report `status=archived`, exit 0.

### Package hashes

| Artifact | Initial package SHA-256 | Follow-up package SHA-256 |
|---|---|---|
| Plan | `b6610852ae2e2f7d2e9e89f78c559b9ef97ffdfbe714076cc572bca860942114` | `b50308eeca33b2465f42166a1ab68d65f005843a1360f926cb0a4b606c9405b9` |
| Source request | `f79ef858c8f93eda7ba64d570f65da8d4b55d5ce1619151d79ebad197fccbafe` | `868b5ec0c15638b9177d487cc9a4185b610d82b1b6abfdbeaec4700851e25ca0` |
| Ledger | `a3082878fbac3234bca74e1a9c81feabf548f14901e38fc901022605d6717dca` | `7cfcbec52acc028d167450224bf612db091cfe2600159b098c4a838ec8a225d3` |

**Key Takeaways**

- The plan and source hashes match their historical `PLAN:` ledger records.

## 3. Initial package: correct work, lost durable proof

### Evidence chain

| Original parent record | Timestamp | Verified event |
|---|---|---|
| 15 | 15:32:02.303Z | Actual implementation command for the initial package. |
| 36 | 15:32:07.357Z | Actual implementation protocol invocation. |
| 318 | 15:41:31.954Z | Independent Task 3 reviewer dispatched; expressly told to ignore the ledger and artifacts. |
| 332 | 15:42:07.293Z | Executor appends Task 3 completion, assigning its lint criterion to README line 161. |
| 375 | 15:43:26.516Z | Fresh whole-package final reviewer dispatched. |
| 390 | 15:44:52.068Z | `FINAL: issues`; unchanged delivery-state digest. |
| 396 | 15:51:38.336Z | User explicitly reopens Task 3 evidence only. |
| 411 | 15:51:55.456Z | Saved comparison reports 28 findings before, 28 after, zero on changed lines. |
| 415 | 15:52:05.065Z | Corrected Task 3 completion appended. |
| 419 | 15:52:16.384Z | Second fresh final reviewer dispatched. |
| 435 | 15:54:23.570Z | Final pass and successful archive. |

### Why task QA passed

The Task 3 reviewer genuinely checked the README changes and reran lint. Its original final response records the unchanged 28 findings and refers to temporary before/after lint files:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-abd76ef5e5d22848f.jsonl`, original record **36**, **15:42:01.803Z**.

However:

1. The reviewer was deliberately isolated from the ledger.
2. Its lint evidence used temporary file names without line-number citations.
3. The executor then recorded README line 161 as the evidence for “no new findings.”

That line was a table separator, not lint evidence. I independently confirmed its historical content using preserved Git tree `7ac64e6a91f624362b19daf46ea9544ad8a4edcd`, rather than today's changed README.

### Was the final finding valid?

**Yes, under the rule then loaded.** The final reviewer independently confirmed the lint criterion itself held but found no durable lint log and an unsupported ledger pointer.

Original final conclusion:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a59e9aa6df05118de.jsonl`, record **51**, **15:44:41.129Z**.

It says the delivered work meets the criteria, then identifies the single ledger-evidence defect.

### Actual correction and outcome

The original bad completion remains at:

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/progress.md:8`

The corrected completion is at line **12**, with final issues/pass at lines **11/13**.

The durable comparison is:

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358InTempla-20261022-151058/artifacts/t3-markdownlint.log`

- Line 10: before total 28.
- Line 15: after total 28.
- Line 22: zero findings on changed lines.
- Line 24: comparison result.

Second final conclusion:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a6248e3c9fc51e940.jsonl`, record **50**, **15:54:17.688Z**.

**Key Takeaways**

- **Root cause:** verified temporary proof was not preserved when converting the task review into the durable ledger. The correction repaired evidence, not implementation.

## 4. Follow-up package: inconsistent lint interpretation and incomplete evidence audit

### First final review

The follow-up implementation protocol starts at original parent record **818**, **19:40:25.935Z**.

The first final reviewer was dispatched at **1916**, **20:16:10.434Z**, after 17 task reviews. Its conclusion is:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a9c0c61dd415c2c4d.jsonl`, record **135**, **20:20:21.142Z**.

### Original findings and adjudication

| Finding | Independent assessment | Cause |
|---|---|---|
| Task 6 says no lint finding may occur on a changed line, but two changed operator-guide rows retain findings | **Valid literal criterion failure**, despite unchanged totals | Task reviewer substituted “no new findings” for the written stronger condition |
| Task 8 cites startup line 1309, but the quoted string moved to 1310 | **Valid stale pointer under the old final rule** | Task 15 subsequently added a header line |
| Task 7 cites security lines 421-424 as evidence that gitleaks rows were unchanged | **Wrong supporting location** | Those lines describe refresh behavior, not the gitleaks table |
| Task 17 cites a preamble and one file-list entry to support complete follow-ups and protected-file coverage | **Weak/incomplete evidence pointers** | Executor selected narrower lines than the actual reviewed evidence |

The follow-up plan's literal lint rule is present at:

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/TASK-WF-issue358FollowUp-20261022-193837.md:30`

Task 6 repeats it at line **96**.

### Why Task 6 QA passed despite already knowing the problem

This was not a final reviewer discovering previously unavailable lint information.

- Parent record **1215**, **19:50:46.995Z**: the original comparison reports two changed-line findings and `RESULT: DIFFERENCE FOUND`.
- Record **1219**, **19:51:03.657Z**: probes confirm that the same table rows had those findings before editing.
- Record **1230**, **19:51:13.212Z**: executor changes the log's result wording to “no new findings” and appends the explanatory note.
- The Task 6 reviewer then explicitly acknowledges the literal rule is unmet but accepts a “nothing new” interpretation.

That reviewer conclusion is:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a6d8fbaf69a56dd14.jsonl`, record **61**, **19:52:41.441Z**.

The underlying evidence remains transparent:

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t6-markdownlint.log:18-26`

It records two changed-line findings, unchanged totals of 123, and their pre-existing origin.

**Root cause:** executor and task reviewer knowingly relaxed a written criterion without first obtaining owner acceptance. The first final reviewer applied the literal criterion instead.

### Owner acceptance and first correction

Parent record **1935**, **20:20:43.704Z**, explains the issue and requests acceptance plus correction of Tasks 7, 8 and 17. The user replies “accept and fix” at **1938**, **20:25:19.428Z**.

Record **1968**, **20:25:54.345Z**, contains the actual write of the acceptance note and append-only corrected completions.

Durable record:

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t6-owner-acceptance.md:10-13`

It accepts the unchanged pre-existing findings and specifically authorizes correcting Tasks 7, 8 and 17 only.

### Second failure: an old error the first final review missed

Second final reviewer dispatched at parent record **1979**, **20:26:21.231Z**.

Its conclusion:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-acf0a51e6992c50ee.jsonl`, record **116**, **20:31:27.048Z**.

The blocking finding is Task 10's lint citation to **blank line 10**.

Independent corroboration:

- Original completion at `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/progress.md:22`.
- Actual log at `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t10-markdownlint.log`:
  - Line 9: before total 4.
  - Line 10: blank.
  - Line 14: after total 4.
  - Line 17: no-new-findings result.
- Parent record **1425**, **19:57:50.705Z**, shows the original command creating that incorrect `:10` pointer.
- Parent record **2012**, **20:31:49.683Z**, reports the mechanical result `T10: BLANK …:10-10`.

The original Task 10 reviewer had already read the correct log body, but its final response supplied incorrectly numbered log citations:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-af349dd52cae648a5.jsonl`, records **16** and **33**, **19:57:18.777Z** and **19:57:44.798Z** respectively.

The second reviewer also notices that the first Task 7 repair, lines 45-56, omits the final gitleaks row at line 57. This is a small incompleteness in the repair's evidence range, not a delivery regression.

**Conclusion:** the additional failed final review was caused principally by an existing evidence defect missed in the first full audit.

### Second correction, authorization and missing history

Parent record **2015**, **20:31:58.264Z**, appends corrected Task 10 and Task 7 completions. Record **2016** reports zero blank/missing token problems and the same delivery digest.

Parent record **2028**, **20:32:18.558Z**, admits Task 10 correction went beyond the expressly named Tasks 7, 8 and 17. No intervening user message grants fresh Task 10 permission in this correction sequence.

The ledger omits the second `FINAL: issues`:

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/progress.md`

- Line 37: first final issues.
- Lines 38-40: first corrections.
- Lines 41-42: second corrections.
- Line 43: final pass.
- **No second failed-final record.**

**Key Takeaways**

- The third reviewer prompt says two earlier attempts “recorded” issues, but the on-disk ledger disproves that wording. Counting ledger `FINAL:` records alone undercounts this incident.

## 5. Review-policy changed before the final pass

This is an important control, not speculation about the agent's reasoning.

The second follow-up final reviewer reads the installed rubric through:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-acf0a51e6992c50ee.jsonl`

- Read dispatch record **16**, **20:26:29.621Z**.
- Result record **18**, **20:26:30.085Z**.
- Captured rubric line **79**: “Missing, stale or unverifiable evidence is `issues`.”

The third reviewer reads **different content from the same installed path** through:

`/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a4bfff371c63a6c39.jsonl`

- Read dispatch record **16**, **20:32:18.776Z**.
- Result record **18**, **20:32:19.277Z**.
- Captured rubric line **82**: a moved line number alone is never `issues`; judge current evidence and end-state compliance, including recorded owner acceptance.

The newer text also changes acceptance-recording rules.

Third final conclusion is record **155**, **20:37:13.395Z**. Parent record **2036**, **20:37:22.846Z**, records final pass and successful archive.

**What can be concluded:** the final pass follows both evidence corrections and a changed review policy. This case cannot isolate their separate effect.

**Key Takeaways**

- **What cannot be concluded:** which actor updated the installed rubric, or whether that change alone would have passed the unrepaired package.

## 6. Remaining findings versus actual regressions

The third final reviewer passes while listing eight minor observations.

Independent historical-source checks distinguish them:

- **Cosmetic:** short comment wrapping and a long README line.
- **Authorized by another task:** refresh comment outside Task 15's narrow spans was permitted by Task 17's closing sweep.
- **Equivalent wording:** saying the optional file exists only for file-form secrets preserves the relevant meaning.
- **Real narrow task-body omission:** Task 2 explicitly requests that the manpage load-order entry connect the five key names to the gateway key. Historical load-order line 236 says only optional/sourced-last/wins. The fan-out is explained elsewhere at lines 171-183.

The last item was present before the final loop and did not cause its failures. It means **observed final pass must not be restated as proof that every literal instruction was fulfilled**.

**Key Takeaways**

- This historical content was checked using preserved tree `d9f262a48f82c55b18f883826428f2fd8d2d7be5`. Today's surviving worktree has later edits, including a different startup credential check and shifted source lines.

## 7. Controls, exclusions and gaps

### Controls

- Used actual user commands, assistant tool dispatches, tool results and nested conclusions.
- Did not count injected policies, examples or quoted command strings as execution events.
- Read archived plans, source requests, ledgers, lint logs and acceptance record.
- Checked historical source through preserved Git objects where present-day content had changed.
- Ran no contract tests, builds, deployments or production code; performed read-only transcript parsing, hashing and Git object inspection.
- No nested agents spawned and no report file written.
- These are transcript/artifact-backed conclusions. Graph coverage was unavailable for the relevant historical evidence.

### Exclusions

- Expected negative test failures are not review-loop failures.
- Initial Task 1's unrelated-red extras result is not a failed spec review.
- Follow-up plan regeneration is not another execution retry of these completed packages.
- Cosmetic observations do not establish newly introduced code defects.

### Gaps and questions

1. The updater of the installed review rubric is not established by this assigned session.
2. Historical temporary lint files may not survive; their original tool outputs and later durable comparisons do.
3. The blank-token check establishes pointer existence and nonblank content, not semantic proof that every citation supports its claim.
4. The successful archive is verified. Literal universal compliance is not, because of the accepted lint gap and narrow manpage instruction omission.

### Stale documentation found

The archived follow-up list intentionally records historical source positions. It must not be treated as a current defect inventory after later edits:

`/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t17-followups.md`

**Key Takeaways**

- Historical follow-up positions are not a current defect inventory; accepted gaps and the missing second FINAL record remain explicit.

## 8. Supporting reviewer source hashes

| Original nested transcript | SHA-256 |
|---|---|
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a59e9aa6df05118de.jsonl` | `77745b0aa621a339a8af927311ac5924bf7e18640145d520c63734e925a62f85` |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a6248e3c9fc51e940.jsonl` | `4ca98b54efeca080f472843c9afb692aca96ec30af7dd7e9d15f4637136f37ed` |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a9c0c61dd415c2c4d.jsonl` | `ee78bfd415b166a763910dcce9f3400988917bb935f582f28d5c7c81e9022ba6` |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-acf0a51e6992c50ee.jsonl` | `cec853e54458e3701b5d452937853d46d6bc1239196c48a116803abe4eea28df` |
| `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a4bfff371c63a6c39.jsonl` | `4ae49f385e60368991d2b1bc53db6e37df5fd18980f7f5c9c667ee553b27decb` |


**Key Takeaways**

- These fingerprints identify historical nested reviewer transcripts, not current delivery-file contents.

<!-- phase3-correction: credential-earlier-miss-uncertainty -->
## Limit on explaining the earlier evidence miss

**Key Takeaways**

- Why the first final reviewer missed the already incorrect Task10 blank-line pointer is unknown. The original task reviewer read the correct log body and supplied an incorrectly numbered citation; the evidence does not establish why the first final review missed that pointer. No cognitive cause is inferred.

## Summary and recommended action

The first package failed because valid lint proof was not preserved in the durable evidence record. The follow-up package failed because task QA relaxed a known literal criterion, several ledger pointers were wrong or moved, and the first whole-package audit missed an existing blank citation. The second repair introduced no delivery defect; it fixed the missed citation and extended one evidence range. Final acceptance also coincided with a live rubric change, so these reviews were not governed by one frozen policy throughout.

**Recommended action:** use this case to require durable task evidence and a complete ledger-pointer check before the first final review, while recording every failed review and the exact rubric version it used. This addresses the demonstrated avoidable repeats without confusing evidence repairs with implementation regressions.

## Resume traceability supplement (2026-10-23)

Metadata-only extraction from the original parent transcript verified six requested transition identifiers, and a separate one-record extraction verified the nested second FINAL failure. Both checks guarded selected/output counts and non-null timestamps/UUIDs. This preserves rather than invents the missing ledger event; the historical ledger and original physical JSONL anchors remain unchanged; formatting corrections can move research-file lines.

| Source | Physical line | Original timestamp (UTC) | Message UUID |
|---|---:|---|---|
| Parent transcript above | 390 | 2026-10-22T15:44:52.068Z | b7f1bea0-3652-4876-81b2-95cdc8359c60 |
| Parent transcript above | 435 | 2026-10-22T15:54:23.570Z | 946adb8c-42c2-45e4-8f23-7bdd8327c301 |
| Parent transcript above | 1425 | 2026-10-22T19:57:50.705Z | ba078e83-30eb-4643-b8a3-f662fe3aa73c |
| Parent transcript above | 1938 | 2026-10-22T20:25:19.428Z | 5ba0e40b-4c02-467f-b721-c4c1a12bd189 |
| Parent transcript above | 2015 | 2026-10-22T20:31:58.264Z | 4ea6812e-7d28-400d-8163-01d543ccb6c7 |
| Parent transcript above | 2036 | 2026-10-22T20:37:22.846Z | 5b3ee20a-1d38-4518-a29b-0f92cc1f4821 |
| Nested agent-acf0a51e6992c50ee.jsonl at the full path in Second failure above | 116 | 2026-10-22T20:31:27.048Z | 375a0903-0c0d-4bd0-94d6-0b1faac37cb4 |

**Key Takeaways**

- Original nested evidence preserves the failed FINAL absent from the historical ledger; that ledger remains unmodified.

## Complete third-final eight-observation disposition

**Primary source:** `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a4bfff371c63a6c39.jsonl`, physical record 155, `2026-10-22T20:37:13.395Z`, message UUID `4209789d-084b-4425-9b19-753e01c8bfa1`. It returns `FINAL: pass` and eight observations labelled MINOR. Source positions below are historical delivery-file positions, not this research file's line numbers.

The same nested transcript preserves the loaded plan at record 19, ledger at 21, acceptance artifact at 84, manpage evidence at 42 and 87, load-order line at 99, and sweep classification at 121. The two loaded rubric versions remain in `historical-review-rules.json` and this case's Review-policy section. No historical package or ruling ledger was changed for this accounting.

| Observation | Historical meaning and criterion assessment | Causal class and limits |
|---|---|---|
| 1. Orphan provider comment | `providers.tf:37` leaves the short fragment “sit on top of the”. The reviewer calls it cosmetic; no separately violated functional criterion is demonstrated. | Cosmetic authoring observation. Exact introducing edit is unknown here; unchanged delivery-state digests exclude the evidence-only FINAL repairs as its cause. Not another failed review or verified runtime defect. |
| 2. Long README line | `README.md:37` is long after rewrapping. The reviewer expressly says MD013 is disabled and no lint finding results. | Cosmetic observation, not an established literal lint failure. Exact introducing edit and any earlier-miss reason are unknown; not caused by evidence-only corrections. |
| 3. Refresh comment outside Task 15 spans | `refresh-env:470` lies outside Task 15's named local spans, but the later Task 17 sweep authorizes fixing stale hits in allowed files. Plan record 19, Task 17 body at historical line 190, establishes that broader authority. | Authorized by another task, not extra delivery scope. The third reviewer explicitly accepts it. No final-loop regression is demonstrated. |
| 4. Loose overwrite wording | Historical `aienv.7:183` says “from this file or any other file”. Source record 27 requires overwriting values set elsewhere; delivered wording appears in original tool results 42 and 87. The reviewer assesses it accurate but loose. | Equivalent historical wording, not an established unmet requirement. No separate behavior claim is revalidated here. Exact wording-introduction time and earlier-miss reason are unknown; no evidence-only repair introduced it. |
| 5. Missing load-order fan-out clause | Task 2's body at historical plan line 46 explicitly asks the load-order entry to connect all five key names to the gateway key. Tool result 99 shows line 236 says only optional/sourced-last/wins; fan-out is present elsewhere at 171-183. | Valid narrow preexisting task-body omission, not one of the failed FINAL causes and not introduced by evidence repairs. The historical pass is therefore not proof of universal literal instruction completion. Why the final reviewer did not block on this body-level omission is unknown beyond their note that no AC tests it. |
| 6. Optional file expressed equivalently | `SECURITY.md:434-435` uses “only when created with --file” rather than the literal word “optional” requested by Task 7's AC. The third reviewer expressly judges the meaning equivalent; plan record 19, historical lines 100-103, supplies the requirement. | Accepted equivalent wording, with a literal-token qualification, not a newly proven security defect. Exact introduction and earlier-miss cause are unknown. |
| 7. Acceptance artifact, no ruling ledger line | The Task 6 lint acceptance exists in `t6-owner-acceptance.md` (original result 84), while original ledger result 21 retains `T6: complete verdict=compliant` and contains no `T6: Ruling:`. The newer loaded rubric permits executor recording of scoped human acceptance but still requires a durable ruling and unchanged noncompliant completion. | Real acceptance-record/protocol mismatch, not missing human consent and not a delivery-code regression. It arose in the post-first-FINAL acceptance sequence, not from later delivery edits. The third reviewer explicitly did not re-litigate it; do not claim their pass proves the ruling schema was satisfied. No historical ledger repair is authorized here. |
| 8. Retained restart remark | `aidev02-operator.md:528` says old `GH_TOKEN`/`~/.env` needs a restart. Original sweep result 121 labels that exact retained rotation remark ACCURATE; the third reviewer agrees. Task 17 required classifying accurate versus stale hits, not removing every mention. | Retained accurate historical text, not a new stale-documentation or missing-requirement defect. No runtime restart experiment was performed here; the classification is the recorded historical one. No final-loop repair introduced it. |

**Key Takeaways**

- All eight observations are retained with their historical meanings; they are not eight verified delivery defects.
- The acceptance-record mismatch and narrow task-body omission qualify the observed pass without fabricating another failed FINAL or modifying its historical ledger.
