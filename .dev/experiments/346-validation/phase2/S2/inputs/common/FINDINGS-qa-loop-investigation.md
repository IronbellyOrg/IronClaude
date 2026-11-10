# FINDINGS — QA loops, codebase-memory-mcp and codegraph

**Date**: 2026-10-31 · **Worktree**: `.dev/worktrees/qa-loop-investigation` (branch `research/qa-loop-codememory-20261031`, base `75d0d1e2`) · **Orca task**: task_b3e713500353
**Problem definition (user, via coordinator, 2026-10-31T19:11Z)**: QA loops in `/sc:workflow` or `/sc:implement` that last more than 3 review rounds where the findings blocking progress were relatively minor (cosmetic, wording, citation format, low-severity, nit-level), not real defects.
**Structure**: sections follow the brief's step 4 (verdict and calibrated likelihood for Q1 and Q2, driving evidence, what would change each verdict, preventive recommendations marked in-master or not, UNVERIFIED items).

## 1. Verdicts

| Question | Verdict | Calibrated likelihood | Source |
|---|---|---|---|
| **Q1**: did codebase-memory-mcp cause or materially contribute to `/sc:workflow` or `/sc:implement` QA loops of more than 3 rounds blocked by minor findings? | **Unlikely.** Probably did not cause any; a minor contributing role through its context-only hooks cannot be excluded for the two loops in the lost container. | **about 15%** materially contributed, plain reading (band 7-25%); **about 9%** strict reading (band 4-15%); **at most 2%** caused | `debate/q1/adversarial/q1-merged-verdict.md` §3-§4 |
| **Q2**: will codegraph cause the same? | **Unlikely by itself.** It does not recreate the observed mechanism; low but real risk inside `/sc:implement` through two protocol gaps it can feed. | inside `/sc:implement`: **about 12%** over 3 months as a necessary cause (band 10-14%); `/sc:workflow` plan check: **about 1%**; loops outside both commands: about 10% necessary, about 35% contributing | `debate/q2/adversarial/merged-output.md` §1-§2 |

**Read with these limits:**

- **The direct evidence for H1 (which lookup tools and hook context the 2026-10-24 reviewers of `TASK-WF-implementTheAppr-20261024-060449` received and called, and the same for I1 and I2) is unrecoverable, so H1's confidence rests on indirect evidence only.**
- Per the coordinator's condition, H1 is not raised above the troubleshoot calibrator's grade for the H1 card (0.33, `evaluation/run3/tier2-root-cause-analyst-calibration.md`); the debate's 9-15% is below it. That 0.33 is a confidence grade on the card, not a probability that H1 is true.
- The Q1 figure is higher than the synthesis's earlier "≤10%" because the debate withdrew two results as tests of the container: the #277 → #297 drop coincides with a move between machines, and the empty hook-output search ran on a host that never had codebase-memory hooks.
- All Q2 figures are estimates built from the protocol text; the master-installed codegraph configuration has an observed sample of zero.

**Main cause of the loops** (run 3 diagnosis, calibrated 0.67): review pass rules that let a minor finding fail a review, a fresh full re-audit every round, and a protocol or orchestrator that kept supplying rounds. See section 4.

## 2. Q1 — did codebase-memory-mcp cause or materially contribute?

**Verdict: unlikely.** About 15% (plain reading: its output shaped at least one blocking finding; band 7-25%), about 9% (strict reading: removing it would have removed a round no other nit would have filled; band 4-15%), at most 2% that it caused a loop. By incident, strict / plain: I1 about 6-7% / 12%, T8 about 4-5% / 8-10% (both in the lost container), I2 about 1-2% / 3% (this host). Source: `debate/q1/adversarial/q1-merged-verdict.md` (converged; base was Option B "pass rule and rounds").

**Direct evidence for H1 is unrecoverable.** Which lookup tools and hook context the 2026-10-24 reviewers of `TASK-WF-implementTheAppr-20261024-060449` (T8) and of I1 received and called is gone with the `/config/workspace` container (transcripts, `~/.claude/settings.json`, tool lists); the I2 transcript is also lost. H1's confidence therefore rests on indirect evidence only, and every figure above is judgement on that evidence. The troubleshoot diagnosability audit was bypassed for exactly this reason (coordinator-approved; `README.md`).

**Evidence that drove it:**

1. **The enabling rule was present wherever the hooks could have been.** The #277 reviewer contract made "any unmet AC → `missing`" with no severity tier, and the ledgers show it ran for I1 and T8 (`halt review=5 reason=ladder-end`, `.dev/tasks/to-do/TASK-WF-implementTheAppr-20261024-060449/progress.md:54`). The same `superclaude install` that would have added codebase-memory hooks first installed the hook that injects the any-severity style rule into every subagent (`d594babb:src/superclaude/cli/main.py:232,251,255`), conditional on `node` being present (unverified for the container).
2. **The blocking findings were prose, claim-matrix rows and log values, not code facts.** I1's Ruling: "claim-matrix wording and missing rows only, low severity"; T8's: "989 passed while t8-final-checks.log records 990". No I1 blocker is a stale-line or symbol finding, and I1's acceptance criterion froze the code its reviewers checked, which neutralizes the wrong-branch graph mechanism.
3. **The only surviving codebase-memory route is weak.** Upstream companion hooks add context without any tool call, so they leave no trace. Their only recorded output in that container era was "coverage unavailable" / "metadata_match", after which reviewers used direct reads (`.dev/tasks/done/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-anti-omission-report-3.md:179`). The PreToolUse Grep/Glob/Bash hook output was never recorded either way.
4. **Where tool use can be measured, the memory server did nothing.** All 15 reviewers in the two out-of-command loops received codebase-memory's server instructions and made 0 codebase-memory calls; this holds for this host only.
5. **What weakens the case against H1** (why it is above the earlier "≤10%"): container exposure to the hooks is put at about 80%; the #277 → #297 drop coincides with the container → host move; the 572-file hook-output search ran on a host without codebase-memory hooks, so it could not come out positive.

**What would change it:**

- **The decisive probe**: install IronClaude from `2f10a0e1^` into a scratch container, read files inside a nested worktree, capture post-Read and PreToolUse Grep/Glob/Bash hook output, and record whether `node` and `pragmatic-subagent.js` fire. Hooks that inject symbol or line facts raise the strict figure to about 11-12%; hooks that inject only "unavailable" or nothing lower it to about 3-4%.
- **Recovering the container's `~/.claude/settings.json`**: codebase-memory hooks present without the Pragmatic SubagentStart entry would raise it to about 13-15%; no codebase-memory hooks would drop it below 1-2%.
- **A recovered I1, T8 or I2 reviewer transcript** where a blocking minor follows codebase-memory hook text would push it above 30%.
- **Not discriminating** (do not run as tests of H1): the post-#329 task sample, any future any-severity loop on this host, and greps of task packages.

## 3. Q2 — will codegraph cause the same?

**Verdict: codegraph will not, by itself, recreate these loops; there is a low but real risk inside `/sc:implement` through two protocol gaps that codegraph can feed.** Source: Q2 debate merged output (`debate/q2/adversarial/merged-output.md` §1-§2; Option B "will not cause" prevailed, qualified; convergence 82.4% against an 80% threshold, fragile: 79.4% if one point counts as unresolved).

**Calibrated likelihood** (chance of at least one qualifying loop in the 3 months from 2026-11-01, about 430 `/sc:implement` tasks; estimates from how the protocol text works, not from observed runs):

| Where | codegraph contributes | codegraph is a necessary cause |
|---|---|---|
| Inside `/sc:implement` | 0.12-0.16 | **about 0.12** (band 0.10-0.14; outer 0.04-0.35) |
| `/sc:workflow` plan check | about 0.01 | **about 0.01** |
| Review loops outside both commands (rf-qa, ad hoc) | about 0.35 | about 0.10 (0.04-0.18) |

**Evidence that drove it:**

1. **The plan check cannot loop.** One advisory, read-only reflect pass (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:58,60`).
2. **Inside `/sc:implement`, minors cannot block within one review** (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:77,113`; `refs/retry.md:146-147`), **but they can across reviews.** A claim one reviewer verified true but left without an evidence row is `minor`; the next reviewer is not told (`refs/qa.md:341` passes only blocking lines forward); a later reviewer who "could not verify" it (for example after an empty codegraph answer) raises a blocking `ac-outcome-missing`, which is never capped (`refs/qa.md:144,151,170`). The retry adviser cannot dispute it (`refs/retry.md:72`), and all 14 recorded adviser answers were `ready`, 0 disputes.
3. **The line-drift boundary is undefined.** A true claim whose cited line moved can be graded `minor` or blocking `false-claim` (`refs/qa.md:42,70,73`); a stale graph row copied without a Read can trigger the second.
4. **Codegraph's own guards do not reach the per-task reviewer.** The closed reviewer template (`refs/qa.md:304-335`) has no codegraph, index-state or "empty is not absence" text, while the codegraph server tells agents "Trust codegraph's results — don't re-verify them with grep". A live probe returned "No results found" for `ladder-end` on a `fresh` index, although the token is on at least 9 lines of 4 tracked files (3 Markdown protocol files and one Python string literal), and Markdown is not indexed (`debate/q2/live-codegraph-probe.md`; `src/superclaude/core/CODEGRAPH.md:7`).
5. **Outside the commands the loops come from the any-severity rule, not the tool.** ADJ-A1 and ADJ-A2 ran 7 and 8 rounds with 0 lookup-tool calls.
6. **Observed record:** 0 of 16 tasks after #329 reached 4 rounds (95% upper bound about 19%); codegraph-era run `fc3c14d8` converged in ≤2 rounds per task while reviewers called codegraph. The master-installed configuration has an effective sample of zero (the one post-#336 task ran on a lagging install).

**What would change it:**

- **Raise (inside `/sc:implement`)**: one post-#336 task with 4+ verdicts whose round-3-or-later blocker is a "could not verify" on a previously verified-true minor, or a `false-claim` on a drifted row copied from a graph row; or tool-use logs showing reviewers citing graph rows without a Read.
- **Lower**: 50+ logged post-#336 tasks with no blocker traced to a codegraph row; measures 2 and 3 in section 5 landing.
- **Plan check**: only rises if a re-review edge (for example `--remediate`) is added to its Wave 4.
- **Outside the commands**: falls if bundle A (section 5) lands; rises with more any-severity loops or code-heavy projects.

## 4. What actually caused the loops

**Incident base** (redefined; `research/incidents-redefined.md` §3, §5; summarized in `evidence-synthesis.md` §10). 27 ledgers, 177 tasks, plus retained transcripts:

| id | where | date | rule in effect | rounds | blocking findings |
|---|---|---|---|---|---|
| I1 | `/sc:implement`, lost `/config/workspace` container | 2026-10-24 | #277 ladder, reviewer-owned verdict | 6 | minor (wording, missing matrix rows, uncited true claim) |
| T8 | `/sc:implement`, same container | 2026-10-24 | #277 | 5 | minor in 2 of its 3 extension rounds (A4, A5, e.g. "989 vs 990 passed"; A3 substantive); possibly MIXED |
| I2 | `/sc:implement`, this host | 2026-10-26 | pre-#297 behaviour from a stale installed protocol (UNVERIFIED) | 4 | contested (one-sentence fixes the reviewer called false statements) |
| ADJ-A1 | outside both commands (ad hoc review loop) | 2026-10-29 | prompt gate "any issue of any severity is FAIL", no cap | 7 | rounds 1-3 substantive; minor in reviews 4-6, then PASS |
| ADJ-A2 | outside both commands | 2026-10-28 | "Any finding of any severity means FAIL", no cap | 8, never passed | minor in reviews 4-6 and 8; review 7 had 1 IMPORTANT |

`/sc:workflow` never produced one: its plan check is a single advisory pass that cannot loop (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:58,60`; 22 packages, 1 pass each).

**Cause, ranked** (run 3 diagnosis, calibrated 0.67; `evaluation/run3/REPORT.md`):

1. **A pass rule that let minor findings fail a review.** Before #297 (merged 2026-10-25T17:20Z) the `/sc:implement` reviewer owned the verdict with no severity tier, and every subagent also received the Pragmatic style's "Any issue of ANY severity … MUST result in a FAIL" through the SubagentStart hook (`src/superclaude/hooks/scripts/pragmatic-subagent.js:7,15`; `src/superclaude/hooks/hooks.json:124`, no matcher). Outside `/sc:implement` that rule still applies today (`src/superclaude/output-styles/pragmatic.md:225`; `src/superclaude/agents/rf-qa.md:159`).
2. **A fresh reviewer re-audits the whole deliverable each round.** Each round found new nits (ADJ-A1 new-finding counts 18, 15, 17, 11, 4, 1, 0; ADJ-A2 fixed all 50 earlier findings and still failed on 6 new minors).
3. **Round supply.** The #277 5-review ladder, halt then resume or operator review (I1 reached round 6 after `halt review=5 reason=ladder-end`), and no cap at all outside the commands.
4. **Installed-copy lag.** I2 ran about 23 hours after #297 merged but behaved like the older protocol; the likely cause is that `superclaude install` had not refreshed that host (UNVERIFIED, no transcript survives).
5. Contributing: moving-target evidence (test counts, file mtimes) and retry advisers who never see severity rules.

**The #277 → #297 drop is descriptive, not a natural experiment.** Inside the codebase-memory window, the #277 regime produced 4 of 60 tasks with 4+ rounds and the #297 regime 0 of 45 (`.dev/tasks/done/TASK-WF-phase1RemovalSpe-20261029-185100/progress.md:4`: 19 compliant, 0 retry, 0 blocked). The Q1 debate showed this cannot isolate the pass rule: all 45 #297 tasks ran on this host and all 4 #277 loops ran in the lost container, so the rule change coincides with a machine change, and #297 also changed repairs, the prior-findings slot and convergence counting. For the Q1 outcome itself (minor-blocked, 2 of 60 vs 0 of 45) one-sided Fisher p ≈ 0.32, effective sample about 2 packages. The conditions above are therefore **enabling and close to necessary, not sufficient**: 56 of 60 #277 tasks did not loop. What selected the looping tasks is a post-hoc hypothesis: acceptance criteria that make per-item evidence records (claim matrices, fixture result rows) part of the deliverable, plus no early operator Ruling (`debate/q1/adversarial/q1-merged-verdict.md` §6.3, §6.6).

## 5. Preventive recommendations

Status is against fork master `75d0d1e2` (= this branch's base, checked 2026-10-31). "Not in master" items are proposals only; this research run changed no source. Sources: run 3 (`evaluation/run3/REPORT.md`, `adversarial/merged-output.md`) and the Q2 debate (`debate/q2/adversarial/merged-output.md` §5).

**Top 3 (ranked by expected effect on the defined symptom):**

| # | Recommendation | Addresses | In master? | Evidence |
|---|---|---|---|---|
| 1 | **Bundle A: stop minor-only loops outside `/sc:implement`.** After a minor-only FAIL, re-review only the listed findings; remove explicit "any severity is FAIL" gates from ad hoc orchestrator review prompts and from rf-qa decisions (whether the style rule also binds reflect reviewers, which have their own HIGH/MEDIUM/LOW scale, is unresolved); give ad hoc loops a round cap. Changes a deliberate style rule, so it needs the user's explicit authorization. | the live route today (ADJ-A1 7 rounds, ADJ-A2 8 rounds) and Q2's outside-commands risk | **No** | `src/superclaude/output-styles/pragmatic.md:225` and `src/superclaude/agents/rf-qa.md:159,171` unchanged; rf-qa's 3-cycle cap (`rf-qa.md:390`) binds only under rf-team-lead |
| 2 | **Close the two `/sc:implement` gaps codegraph can feed.** (a) Stop a verified-true minor being promoted to an uncapped `late` blocker by a later "could not verify": extend the cap in `refs/qa.md:170` or carry verified-true minors in `{prior_findings}` (`:341`). (b) Define the line-drift boundary so a verified-true claim whose cited line or value moved is `minor`, not `false-claim` (`refs/qa.md:42,70,73`; run 3's deferred bundle B). Word both as parent-side rules to avoid the FINAL saved-prompt migration. | Q2's in-command risk; T8's "989 vs 990" shape | **No** | `refs/qa.md:170` caps only findings "with no confirmed `yes`"; `:341` "never minors or notes" |
| 3 | **Keep every host on the shipped rules and make drift visible.** Run `superclaude install` on every host (brings #297, `CODEGRAPH.md` and the new codegraph rows; `~/.claude/CODEGRAPH.md` is missing here); add the test pins P1-P4 on the #297 text (`pragmatic.md:225` exception, `refs/retry.md:146`, `refs/qa.md:77`, `refs/qa.md:331` inside the template) to `tests/skills/test_implement_severity_static.py`; record the installed protocol version in each run's ledger. | I2's installed-copy lag; silent regression of #297 | **No** (install is an ops step; pins: 0 hits in `tests/` for those wordings, the file pins only part of the model; ledger header pins only the PLAN hash, `refs/ledger.md:226,231`) | `evaluation/run3/evidence-validation.md` Notes |

**Further recommendations:**

| # | Recommendation | In master? | Notes |
|---|---|---|---|
| 4 | Add a codegraph line to the per-task reviewer template (graph rows are leads to Read; an empty answer is not "could not verify"; Markdown is not indexed) and require "could not verify" to name its Read or Grep attempt. | **No** (`refs/qa.md:304-335` has no codegraph text) | Changes template question 1, so it needs the FINAL saved-prompt migration (`refs/qa.md:281`) |
| 5 | Let the retry adviser dispute a "could not verify" finding it verifies true by Read. | **No** (`refs/retry.md:72`) | 14 of 14 recorded adviser answers were `ready`, 0 disputes |
| 6 | Log tool use and injected hook context for QA subagents (run 1 tasklist Task 1). Its absence is why H1 is unrecoverable. | **No** | `evaluation/diagnosability-tasklist.md` |
| 7 | Document the Pragmatic-style SubagentStart injection in `docs/user-guide/freshness-hooks.md:20`. | **No** | the file has 0 "pragmatic" matches |
| 8 | Run the scratch-container probe from `2f10a0e1^` if a firmer Q1 number is needed (research, not prevention). | n/a | the only test that can settle the hook route |

**Already in master (keep):**

- #297 severity model inside `/sc:implement`: only `blocking` findings fail, with precedence over the output style and its SubagentStart copy (`refs/qa.md:77,113`); minors never trigger a fix pass, repair or review (`refs/retry.md:146`); convergence ignores minor counts (`:147`).
- Ladder cap and halt (`refs/retry.md:14,189`); FINAL "a moved line number alone is never `issues`" (`refs/qa.md:294`).
- Advisory single-pass `/sc:workflow` plan check (`sc-workflow-protocol/SKILL.md:58,60`).
- rf-qa 3-fix-cycle cap and monotonicity guard, scoped to rf-team-lead (`rf-qa.md:390-391`).
- Codegraph rules in source: "Read before cite or edit", "Empty is not absence" (`src/superclaude/core/CODEGRAPH.md:68,70`), but not installed on this host.
- Partial test pins for the implement severity model (`tests/skills/test_implement_severity_static.py`).

## 6. UNVERIFIED and limits

- **H1's direct evidence is unrecoverable.** Which lookup tools and hook context the 2026-10-24 reviewers of `TASK-WF-implementTheAppr-20261024-060449` (and of I1 in the same container) received and called cannot be recovered: the `/config/workspace` container, its transcripts, `~/.claude/settings.json` hooks, output style and tool list are gone. H1's confidence therefore rests on indirect evidence only. The same applies to I2, whose session transcript is lost.
- **Upstream codebase-memory companion hooks in that container** (PreToolUse on Grep/Glob/Bash, post-Read coverage context): installed by the pre-#329 installer (`2f10a0e1^:src/superclaude/cli/install_codebase_memory.py:668`), but whether they ran there and what they injected is UNVERIFIED. The behaviour description comes from the upstream README, not from an IronClaude host.
- **C297 control and ADJ transcripts come from this host, which had no codebase-memory hooks.** They test the MCP tool route (0 calls), not the hook route in the lost container.
- **I2's installed protocol version** (stale `~/.claude/skills/sc-implement-protocol/`): inferred from artifact shape; UNVERIFIED.
- **Statistics are thin**: 4/60 vs 0/45 for any loop of 4+ rounds (one-sided Fisher p ≈ 0.10); p ≈ 0.32 for the Q1 outcome, minor-blocked 2/60 vs 0/45 (section 4); the denominator of ad hoc review loops outside the commands is unknown.
- **No any-severity loop has been observed after #329** (codebase-memory removed), so the strongest discriminator for H1 (do such loops persist without the tool?) is untested.
- **Codegraph-era sample is small**: 15 tasks after #329, 1 after #336; no codegraph-attributed finding seen; the false-absence route is unobserved.
- **Codegraph rules file not installed on this host**: `~/.claude/CODEGRAPH.md` is missing while `src/superclaude/core/CODEGRAPH.md` exists (checked 2026-10-31), so "Read before cite" and "empty is not absence" may not reach agents here.
- **Aggregates** ("0 of 45", ADJ round counts 7 and 8) rest on `research/*.md` and were not line-verified by the evidence validator; the phase1 control counts were independently re-counted.
- **Process deviations**: the troubleshoot diagnosability audit was bypassed (coordinator-approved, `README.md`); the run-3 Wave 4 delegated agent acted as its own debate orchestrator; `auggie` was not available, so Grep/Glob/Read were used.

## 7. Artifact map

All paths under `.dev/qa-loop-investigation/`.

| Step | Artifact | Notes |
|---|---|---|
| 1 Gather | `research/01-git-history.md`, `02-github.md`, `03-dev-artifacts.md`, `04-transcripts.md` | the 4 parallel research files (old definition) |
| 1 Gather | `research/incidents-redefined-ledgers.md`, `incidents-redefined-transcripts.md`, `incidents-redefined.md` | incident search under the corrected definition |
| 1 Gather | `research/05-severity-rule-history.md` | history of the any-severity rule and #297 |
| 1 Cross-check | `evidence-synthesis.md` | §2-§9 old definition; §10-§13 redefinition |
| 2 Evaluate | `evaluation/REPORT.md`, `evaluation/audit.log` | run 1 (old definition): `blocked`, diagnosability audit found the H1 datum unrecoverable |
| 2 Evaluate | `evaluation/run2-cards/` (`STOPPED.md`) | run 2 (old definition, audit bypassed), stopped cleanly after the scope correction |
| 2 Evaluate | `evaluation/run3/REPORT.md`, `audit.log`, `evidence-validation.md`, hypothesis cards and calibrations, `adversarial/`, `self-review.md`, `hardening-closure.md` | run 3 (redefined problem): `partial`, Tier 2, confidence 0.67 |
| 3 Debate | `debate/q1/v2-option-a-codebase-memory-primary-cause.md`, `debate/q1/v2-option-b-pass-rule-and-rounds.md`, `debate/q1/adversarial/q1-merged-verdict.md`, `debate/q1/adversarial/adversarial/` (transcript, invariant probe, scoring, merge log, return contract) | Q1 debate, default depth, converged (older `option-*` drafts superseded) |
| 3 Debate | `debate/q2/v2-option-a-codegraph-will-cause.md`, `debate/q2/v2-option-b-codegraph-will-not-cause.md`, `debate/q2/live-codegraph-probe.md`, `debate/q2/adversarial/` | Q2 debate |
| 4 Report | `FINDINGS.md` (this file), `findings-validation.md` (independent citation check; 4 fixes applied), `README.md` | README records the command choice, the bypass and the scope correction |
