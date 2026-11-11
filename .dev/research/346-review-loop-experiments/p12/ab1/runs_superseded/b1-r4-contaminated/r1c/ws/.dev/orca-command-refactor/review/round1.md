review: 1 of 3

# /sc:spec-panel critique report, round 1

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given (first review). prior report: none.
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md:29-36`.
- Coverage and limits: all 285 lines of the candidate, the three inventories, and the README were read. In this sandbox I could not start three fresh-context reviewers (no subagent tool), so this is ONE first review, not three plus the MERGE rule (`document_review_loop_prompts.md:34-35`). Its ids are `F1`, `F2`, not merged `M` ids. A coordinator that wants the full three-review ceremony must run two more. Only the inventories can be checked here. Every citation of `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `CLAUDE.md` or Orca source is UNVERIFIED (the files are outside the workspace) unless an inventory quotes it. The inventories are cited as quoted evidence.
- `--iterations`, `--format`, `--experts`: defaults. Format is critique (grouped by bucket). `--unattended` not passed.

Expert order used: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Only findings that survived the grading check are listed. Experts with nothing to add are omitted.

## Grading summary

| id | severity label | grade | one line |
|---|---|---|---|
| F1 | MAJOR | blocking | AC-1.1 requires P1 `## Unattended mode` sections for commands whose behaviour the spec defers to P4 and D2-D4 (and, under recommended D3(a), says pr-submit gets no change) |
| F2 | MAJOR | blocking | AC-0.4 cannot pass: step 3 demands the WC-4 contract path, which the spec says does not exist until P1 |
| (Medium and minor findings) | | follow-up candidates | listed below |

## === REQUIREMENTS ANALYSIS ===

### F1 (blocking) - Wiegers, Cockburn - AC-1.1 contradicts D3(a), the P4 deferral and "Phases 1-3 need no user decision"

Grading sentence: an implementer who follows the stated text as written builds a P1 that adds an `## Unattended mode` section, a `--unattended` flag and a passing test for `pr-submit`, `implement` and `post-release`, and that is wrong because the same document says those three commands' unattended behaviour waits for user decisions D2-D4 in P4, and under the recommended D3(a) pr-submit gets no change at all.

Quoted texts:
1. Spec:159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
2. Spec:195 (AC-1.1, a P1 check): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one".
3. Spec:154 and spec:225: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4."
4. Spec:240 (D3(a), the recommendation): "no pr-submit changes in Phase 4"; spec:139: "`/sc:pr-submit` stays a worker candidate only if the user accepts open decision D3".
5. Spec:109, spec:113, spec:114, spec:162: implement, post-release and pr-submit are rows of section 3.2 with phase P4 and gates that D2 to D4 decide.

Attack (Whittaker, sequence attack): run the phases in the spec's order. After P1, AC-1.1 passes only if pr-submit, implement and post-release each carry the section. pr-submit has real gates (`--monitor 1` y/n, operator HALTs, `INV-B:34`, `INV-B:89`), so a "no-op" flag is not available for it (the text at 159 allows a no-op only "where a command has no gate"). Under D3(a) the section must not exist, so AC-1.1 fails by construction for the recommended path. Under D3(b) it is P4 work done in P1 before the user decided. Two stated texts contradict (AC-1.1 against D3(a) and against 154/225), and an acceptance criterion cannot pass on the recommended path.

Evidence check: inventory confirms pr-submit has default-off gates only at `--monitor 1` and halts handed to "the operator" (`INV-B:89`), and implement's halt cannot be unblocked by another agent (`INV-A:66`; the Ruling rule at `refs/qa.md:238` is quoted in `commands-a.md` notes and is UNVERIFIED against the source here).

Recommendation (narrow, no new rule): scope AC-1.1 and the P1 flag scope to the commands whose phase is P1-P3, and list pr-submit, implement and post-release as P4 only. Priority High.

### F2 (blocking) - Adzic, Crispin - AC-0.4 cannot pass as written

Grading sentence: an implementer who runs AC-0.4 as written on `/sc:troubleshoot` and `/sc:adversarial` builds a P0 whose step 3 can never pass, because step 3 requires the report path to be "the WC-4 contract path" and the spec says that contract does not exist until P1.

Quoted texts:
1. Spec:182 (7.2 step 3): "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
2. Spec:194 (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
3. Spec:62 (WC-4): the contract is `<output-dir>/return-contract.yaml`; spec:91: troubleshoot's report today is `REPORT.md`; spec:83: adversarial's contract filename "not fixed" and the fix is P1 (spec:159, spec:198).

Attack (state trace): P0 smoke run of troubleshoot. Before: no `return-contract.yaml`. Worker sends `worker_done --report-path REPORT.md`. Step 3 pass condition: "report path is the WC-4 contract path" -> false; "outcome matches the contract's status" -> there is no contract to match. AC-0.4 declares steps 1-3 must pass. The text relaxes only step 4. The gate that decides whether section 1 stands (spec:194, "a failure here reopens section 1") therefore fails or is applied by guess.

Recommendation: state in AC-0.4 that step 3 also uses the existing report file for P0 (the same relaxation already given for step 4). Priority High.

## === ARCHITECTURE ANALYSIS ===

No architecture-level finding reached blocking. The decision itself (Orca on top, commands unchanged, section 1.3) is consistent with the inventories: the nesting limit and `worker_done` binding are quoted at `CAPS:97-103` and `CAPS:150`; 43 = 10 + 27 + 6 is consistent with `INV-A` (5 ready, 13 needs-change, 3 coordinator-only, `commands-a.md:94-97` summary) and `INV-B` (5 ready, 14 needs-change, 3 coordinator-only, `commands-b.md:285-299`).

## === Guard Condition Boundary Table ===

Trigger: the spec contains thresholds and guards (heartbeat and wait sizes, readiness limit, nesting depth, circuit breaker, status mapping). Input classes with no meaning for a guard are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` + gate -> blocked report | Spec:60, 62 (WC-2, WC-4) | Zero/Empty | no `--output`/`--output-dir` passed | cannot choose a directory | not specified (2.3, spec:73, says the brief carries it, but no rule for a missing one) | GAP (see M2) |
| same | Spec:60, 62 | Typical | dir passed, gate hit | blocked | contract written with `blocked_question` | OK |
| same | Spec:61, 64 | Legitimate edge case | worker `ask`s, then re-invokes a "fresh dir" command | re-run | which dir is used is not stated | GAP (see M8) |
| wait split (4 min) vs heartbeat (5 min) | Spec:68 (WC-10) | Typical | wait 4 min | true | split and heartbeat | OK |
| same | Spec:68 | Maximum/Overflow | single tool call > 5 min (cli-eval up to 3600 s) | false | must be split to <= 4 min | OK |
| same | Spec:68, 114 | Legitimate edge case | pr-submit poll script runtime unknown | unknown | UNVERIFIED, owned by UNVERIFIED 12 (spec:283) | OK (declared) |
| readiness limit 60 s | Spec:59 (WC-1) | Maximum/Overflow | prompt fallback > ~45 s | startup fails | fallback "well inside" the limit; the numeric budget is from `EVIDENCE.md:45,56` (UNVERIFIED here) | OK |
| nesting depth 1 | Spec:33, 66 (R1, WC-8) | Typical/One | depth-1 worker calls `worker-start` | refused (`CAPS:97-101`) | forbidden by WC-8 | OK |
| same | Spec:66 | Legitimate edge case | depth-1 worker calls `task-create` | unknown | forbidden anyway; UNVERIFIED 5 | OK |
| outcome mapping | Spec:63 (WC-5) | Sentinel value match | contract `status: partial` or audit verdict FAIL | `succeeded` | stated | OK |
| same | Spec:63 | Zero/Empty | no report exists | `failed` | stated | OK |
| circuit breaker 3 failures | Spec:64 (WC-6) | Maximum/Overflow | 3rd consecutive failed `worker-start` | Task failed | retry rule cited from `CAPS:116`, `CAPS:80`; spec relies on it, no own rule | OK |
| task confidence 0.70 | Spec:121 (task row) | Boundary | exactly 0.70 | the source says "< 0.70" blocks | the spec repeats "below 0.70"; behaviour at exactly 0.70 follows the source (UNVERIFIED, `cmd/task.md:93`) | OK |
| AC-1.1 test scope | Spec:195 | Divergence | command in 3.1-3.2 but P4 / D3(a) | test must pass and fail | contradictory | GAP (F1) |
| AC-0.4 step 3 | Spec:182, 194 | Divergence | P0, no contract yet | pass required, impossible | contradictory | GAP (F2) |

Rows left out: "One/Minimal" for the heartbeat and depth guards (a single wait or a single worker behaves as Typical; no distinct rule).

## === Pipeline Dimensional Analysis ===

Trigger: yes (multi-stage count flow: commands -> classes -> phases). Quantity Flow Diagram:

```text
[43 commands: spec:76]
  --> [Classify] --> [10 ready (spec:81-92)]  ----> P0/P1/P2 touch: all 10 get a section (AC-1.1), 4 of them get P2 gate work (reflect, release-split, tdd, troubleshoot)
                 --> [27 needs-change (spec:97-125)] --> P1: 9, P2: 11, P3: 4, P4: 3  (sum 27, matches spec:159-162)
                 --> [6 coordinator-only (spec:130-137)]
  Consumer AC-1.1 (spec:195): expects ALL of 10 + 27 = 37  <-- MISMATCH with P4's 3 (D2-D4 undecided) and D3(a) (F1)
```

Counts reconcile across the three classes and four phases; the one mismatch is the AC-1.1 consumer (F1), not the arithmetic. The inventories give 5+5 ready, 13+14 needs-change, 3+3 coordinator-only (`commands-a.md` summary, `commands-b.md:285-299`).

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium (each needs a guess or is a requirement the document never states):
- M1. Unsupported citation. Spec:69 (WC-11) and spec:73 (2.3) cite `CAPS:115` for "`[G:placement]` lines 8-11: workers share the current worktree by default". `orca-capabilities.md:115` is the "Worktrees are never deleted by these verbs" bullet; no line of the capabilities inventory states the shared-worktree default (grep of `placement` and `share` in `orca-capabilities.md` finds only line 17 and line 122, which concerns liveness verdicts). The claim is UNVERIFIED. WC-11's requirement stands without it.
- M2. Missing requirement: `--unattended` with no output directory. WC-2(c) and WC-4 write the report to the passed directory (spec:60, 62); nothing says what a command does when no directory was passed (for example `analyze` has no `--output` today, `INV-A:37`). The first sentence of 2.3 (spec:73) is a coordinator duty, not a command rule.
- M3. AC-C1 (spec:172) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and must print nothing, but P0 adds `WORKER-CONTRACT.md` with a coordinator brief template and an Orca section to `HOW-WE-WORK.md` (spec:158). If either spells an Orca command, AC-C1 fails; whether they will is not stated. SA-2 (spec:147) allows an Orca mention "inside the contract file" only as an example of a question channel.
- M4. Tasklist departs from its inventory verdict without saying so. Inventory: drop `--remediate`, "the per-phase reflect fan-out must run at the worker's top level, not inside subagents" (`INV-B:215`). Spec:122 keeps the subagent fan-out ("inside Claude Code's nesting limit, `INV-A:14`"). `INV-A:14` states the three-layer limit only; nothing checks tasklist -> reflect -> Tier 2 reviewers -> adversarial depth. Decisions row at spec:268 says "nothing read ... contradicts a verdict", which is not accurate for this row.
- M5. pr-submit "Will Not: run headless / imply a daemon" (`INV-B:90`, citing `cmd/pr-submit.md:85`, `SKILL.md:225`) is never reconciled with a `--unattended` pr-submit (spec:114, D3(b) at spec:241).
- M6. `load` is in 3.2 with report "none" and "use it as a step inside another worker's brief" (spec:112, 265), but AC-1.1 (spec:195) wants a section naming `return-contract.yaml` for every 3.1-3.2 command (also validate-roadmap and validate-tests report "n/a", spec:124-125).
- M7. Window between P1 and P2: P1 ships `--unattended` accepted by commands that still have outward defaults (auggie-review posts by default, `INV-A:62`; task commit/push, spec:121) while their WC-9 off-switch arrives in P2 (spec:160). A brief that passes `--unattended` in that window gets a flag that suggests safety and does nothing. The spec limits the no-op to "no gate" commands (spec:159) but P1 scope names every command.
- M8. WC-3 (spec:61): after a worker `ask`, "re-invoke or resume the command" - for the fresh-dir commands (WC-6, spec:64) the re-run into the same `<output-dir>` is neither allowed nor forbidden, and a re-run would overwrite the blocked contract.
- M9. WC-1 and WC-12 (spec:59, 70) have owners outside the commands but no phase or acceptance check beyond 7.2 step 1; nothing in section 6 delivers WC-1.
- M10. cleanup-audit is "ready" (spec:85) but has a fixed output dir, so it cannot satisfy WC-4's brief-supplied `<output-dir>` or WC-11's slug rule (spec:62, 69); the spec records "one audit per worktree at a time" and treats it as a small fix.
- M11. Self-attested checks are UNVERIFIED here: spec:11 (11 re-read locations) and spec:285 (about 340 citations re-read, 9 defects fixed). The inventory notes they rest on do exist (`commands-a.md:106` says about 290 citations, `commands-b.md:320` says about 270), but they cover only the inventories, not the spec's 340; that second check cannot be reproduced from the workspace.

Minor (notes):
- n1. AC-C1 and AC-C4 (spec:172, 175, 176) show `\|` inside commands; copied literally into `grep -E` a `\|` is a literal pipe. Write the commands in a code block.
- n2. P1 scope list (spec:159) names 9 + 4 commands but AC-1.1 covers all 37; list them in one place.
- n3. Spec:96 says "27 needing a change"; 3.1 rows also need P1/P2 work, so "ready today" means "ready with the stated flags", which spec:79 says.

Question for the user (once per loop; not asked in this sandbox, no issue created): open an issue for the Medium and minor follow-up candidates above? Pending.

## Reviser brief

Applies only to the blocking findings F1 and F2. Rules for the reviser (restating `Review Loop` bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with bytes added and deleted per finding id. Do not edit for Medium or minor findings, and do not award yourself a PASS.

- F1: Spec:159 and spec:195 (and spec:154, 225, 240, 139). Narrow AC-1.1 and the P1 flag scope so they cover only commands whose phase is P1-P3; make P4 commands (implement, post-release, pr-submit) not part of the P1 test. Wrong outcome: P1 requires sections for commands whose behaviour is undecided or, under D3(a), must not change.
- F2: Spec:182 and spec:194. State that in P0 step 3 uses the command's existing report file, as step 4 already does. Wrong outcome: AC-0.4 cannot pass.

verdict: FAIL
