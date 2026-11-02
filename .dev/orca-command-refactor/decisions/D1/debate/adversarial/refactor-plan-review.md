# Refactor Plan Review (D1, Step 4)

Reviewer: fresh-context analytical reviewer (not the drafter), 2026-11-02. Started from the position that the plan has mistakes.
Plan under review: `refactor-plan.md` (cited below as `PLAN:N`). Citation keys are the plan's own (`SPEC`, `CAPS`, `BSel`, `R1-Vn`, `R2-Vn`, `INV-NNN`, `CORE-CLAUDE`, `WF`, `BS`, `CR01`). `ROOT-CLAUDE:N` = the repository-root `CLAUDE.md:N`. Grading follows K3 (PR #343): only BLOCKING findings fail the review; MINOR findings are notes.

## Scope

Four checks, as the brief asks: (1) coverage of the 17 "Strengths to Incorporate" (`BSel:187-209`) and the five HIGH UNADDRESSED invariants; (2) citation resolution, with the 13 mandatory citations plus a wider sample; (3) contradictions between changes, with SA-1/SA-2 and the non-goals, and with K1-K4; (4) facts stated without an UNVERIFIED mark.

## Check 1: Coverage of strengths and HIGH invariants

- **Strengths 1-17 (`BSel:189-209`)**: each maps one-to-one to changes 1-17 (`PLAN:20-137`), with matching source and intent. No strength is missing. `PLAN:15` gives 24 changes (17 + 5 + 1 + 1), and the count is correct.
- **HIGH invariants**: INV-001 → change 18, INV-005 → change 19, INV-015 → change 20, INV-016 → change 21, INV-020 → change 22. Each has a planned change, and the residuals are listed (`PLAN:203-211`). `PLAN:211` correctly keeps all five under `unaddressed_invariants` with `status: partial`, because no advocate round tested the amendments.
- **Result**: formal coverage is complete. As written, though, changes 18 and 22 do not close INV-001 and INV-020: see B1 and B2.

## Check 2: Citation verification

All 13 mandatory citations were re-read:

| Citation | Plan use | Result |
|---|---|---|
| CORE-CLAUDE:74 | blocking skill-first rule (`PLAN:156`) | CONFIRMED: "invoke the matching skill with the Skill tool before any other output. That step is blocking", triggered "When a message starts with `/sc:<name>`" |
| WF:58 | workflow invokes reflect via Skill with defaults (`PLAN:163`) | CONFIRMED: "via Skill (`sc:reflect-protocol`), defaults for every other flag, no `--remediate`" |
| BS:185 | brainstorm auto-invokes research (`PLAN:170`) | CONFIRMED. Note: `BS:179` says the enrichment runs "in parallel via `Task` agents", so this is Agent-tool nesting, not in-session Skill nesting (see M13) |
| SPEC:79 | brief says "including `--unattended`" (`PLAN:107`) | CONFIRMED |
| SPEC:139 | research pins `--strategy planning` | CONFIRMED |
| SPEC:145 | only the tasklist row propagates the flag | CONFIRMED (a grep for "pass `--unattended`" finds only line 145) |
| SPEC:150-160 | six coordinator-only commands | CONFIRMED (table rows 155-160) |
| SPEC:193 | P2 adds reflect and research | CONFIRMED |
| SPEC:235 | 7.2 disposable worktree under `.dev/worktrees/` | CONFIRMED |
| SPEC:257 | AC-1.1 asserts the sections | CONFIRMED |
| SPEC:341 | D3 (a) coordinator or person only | CONFIRMED |
| CR01:24 | new worktree lacks `.claude/` copies; setup before use | CONFIRMED |
| CR01:41 | Orca default paths, never `.dev/worktrees/` | CONFIRMED |

Wider sample, all re-read: `BSel:44`, `BSel:76`, `BSel:160-161`, `BSel:168-176`; `debate-transcript.md:579, 585, 586, 587, 589, 594, 596, 597, 600, 602, 605, 607, 608, 631-643, 638-653` (each confidence figure matches); `R1-V1:39`, `R1-V1:40`; `R1-V3:16-21`, `:21`, `:42`, `:44`; `R2-V1:33`, `:34`, `:35`, `:76`, `#5`, `#10`; `R2-V2:28` (critique 2), `:86`, New evidence 1 and 2; `R2-V3 #2, #3, #5, #6, #7, #10, #11, #12, #13`, `:33`, `:86-89`; `DA:19`, `DA:100`; `SPEC:53, 55, 58, 71, 73, 123, 155, 158, 162, 169, 170, 182, 187-195, 191, 197, 237-238, 261, 263, 269, 314, 391`; `CAPS:147, 148, 149, 151`; `CR01:42, 45`; `ROOT-CLAUDE:41-66`; `invariant-probe.md:28, 35, 41-44, 50-51, 55-56`; `D3/debate/adversarial/debate-transcript.md:665`; `git show 80f934de` body ("at most 2 fix cycles (3 reviews), then escalate").

Count: 13 mandatory plus about 60 sampled. No citation is wrong. Overstated or untagged uses: `SPEC:391` (M2), `CAPS:149` as "by design" (M3), `SPEC:58` for "nothing loads the file" (M11), `D3 …:665` cited for half the converged position (M8), and the undefined key `CLAUDE.md:41-66` (M10).

## Check 3: Contradictions

- **Change 18 against itself and the coverage table**: (i) picks a load precedence that it calls UNVERIFIED, while `PLAN:205` claims "precedence does not matter for the check". That claim holds only for the 7.2 precondition, not for the guard at run time (B1).
- **Change 22 against WC-4 and WC-11**: propagating `--unattended` to a nested command triggers the nested command's "exactly one report directory" refusal, or it collides with the caller's contract (B2).
- **Change 24 (K1) against SPEC:235 and the repo's commit rule**: an Orca-created worktree from a git base does not hold uncommitted phase edits (B3).
- **Change 23 (INV-017) against K3**: off by one (M1).
- **Changes 9/10 against 21**: consistent. Case 1/2 is keyed to the brief's own `Command:` line, and nested loads are never checked, so WF:58 cannot trigger case 1 in P2.
- **Changes 18 and 20**: consistent. 20 supersedes R2-V3 #7, and 18 supplies the file read.
- **Changes 19 and 9 ("no second phase list")**: consistent. The never-as-worker list changes only with section 4 or D3 (`PLAN:222`).
- **SA-1/SA-2 and non-goals (`SPEC:165-174`, `SPEC:313-323`)**: no violation. All Orca-aware logic stays in the worker session, and change 22 adds no Orca text to commands. One side effect is noted in B1: if change 18 (iii) were done by installing into `~/.claude`, it would overwrite the person's global install.
- **K2**: respected. Nothing in D1 touches GitHub.
- **K4**: consistent, except where B3 applies to child worktrees and the coordinator-versus-worker copy (M9).

## Check 4: Unverified claims

Facts stated without an UNVERIFIED mark: SPEC:391 reflect headless (M2); `ORCA_TERMINAL_HANDLE` "by design" (M3); setup syncing `.claude/` (`CR01:42` is UNVERIFIED, M9); "nothing loads `WORKER-CONTRACT.md` automatically" (M11); that a worker can invoke a `/sc:` command named on a mid-brief `Command:` line and have it count as a direct, top-level run (M6). The plan does mark the command-precedence question and the "Task text starts with `/sc:`" question as UNVERIFIED.

## Findings

### BLOCKING

**B1. The guard reads one command copy chosen by a guessed precedence, so a stale loaded copy can let a flagged brief run attended with outward defaults on.**
- Plan: `PLAN:143` (i) "project `.claude/commands/sc/<name>.md` when it exists, else `~/.claude/...`; precedence ... is UNVERIFIED". `PLAN:205` "7.2 step 1 confirms the section in both copies so precedence does not matter for the check". `PLAN:143` (iii) "the check confirms the section is present in that copy" (singular).
- Evidence: the repo's own rule gives the opposite order for skills, "skills read `~/.claude/skills/` first, then `.claude/skills/`" (`ROOT-CLAUDE:88`). INV-007's harm: an unconverted copy ignores the token and posts by default (`SPEC:123`, `SPEC:169`, `SPEC:193`).
- Failure: the guard reads a fresh project copy (section present, so a flagged brief passes case 2). Claude Code loads the stale `~/.claude` copy, which has no section. The command ignores `--unattended` and runs attended: it stalls, or for auggie-review it posts to the PR. "Precedence does not matter" is true only for the 7.2 precondition, never for production dispatch. The same skew applies to the protocol skill the command loads, which also exists in two copies.
- Fix: in change 18 (i), the guard reads every copy that exists (project and user). Case 1/2 use "section present" only when all existing copies agree. Disagreement is its own refusal: `command copies disagree (stale copy): <paths>`. State in Known weaknesses that the skill copies can skew the same way. In (iii), say the worktree's project copy is made current by `make sync-dev` inside the worktree, and that `~/.claude` is never reinstalled for a 7.2 run. Correct `PLAN:205` so it describes the all-copies rule.

**B2. Change 22's propagation rule makes nested commands refuse or overwrite the caller's contract, because it gives them no report directory.**
- Plan: `PLAN:171` "passes `--unattended` when the invoked command accepts it at this phase".
- Evidence: under `--unattended`, a command with no report directory, or with two, "does no work, writes nothing" (`SPEC:57`, `SPEC:68`). The worker contract lives at `<report-dir>/return-contract.yaml` (`SPEC:68`). Two writers must never write the same file (`SPEC:75`). WF:58 passes no output flag to reflect, and on a reflect `failed`, workflow records it and proceeds (`WF:60`).
- Failure: from P2, a flagged workflow worker passes `--unattended` to reflect. Reflect has no report directory, so it refuses and does nothing. Workflow logs `reflect_status: failed` and proceeds, so the plan check never runs in any unattended workflow, silently. If the caller instead passes its own `--report-dir`, the nested contract overwrites the caller's worker contract. Brainstorm → research (`SPEC:139` says the contract goes in `--report-dir`) has the same problem.
- Fix: add to change 22's integration point: "the nested invocation gets its own report directory, `<caller report-dir>/nested/<command>-<n>/`; the caller lists that contract in `artifacts`; only the top-level contract drives WC-5; AC-2.1 asserts each listed nested invocation passes both tokens." List workflow (reflect, P2) and brainstorm (research, P2) as P2 section edits, because neither is in the `SPEC:183` P2 list.

**B3. Under K1, the 7.2 worktree created by Orca does not contain the phase's uncommitted edits, so the live check tests the wrong code.**
- Plan: `PLAN:193` (K1: "created by Orca (`worker-start --worktree new-top-level` or `orca worktree create`) ... with setup before dispatch"); `PLAN:143` (iii); `PLAN:241`.
- Evidence: Orca creates worktrees from a git base (`CR01:22`; this spec's own Orca worktree has `baseRef = refs/remotes/origin/master`, `CR01:51`). The phase edits are uncommitted during the phase (`SPEC:229`: "this repo commits only when asked"; `ROOT-CLAUDE:37`). `SPEC:235` requires the worktree to "hold the phase's edits".
- Failure: the new worktree holds pre-phase command files. Setup syncs those, and with the symmetric guard every correctly flagged P1 brief is refused (case 2). The plan's rollback ("refusal reason names staleness; fix the setup step", `PLAN:235`) points at the wrong cause. The same applies to CR-01 children, which get only the feature branch's committed state.
- Fix: add to change 24 K1: "before 7.2, the phase's edits are committed to the feature branch (or a scratch branch) with the user's authorization, and the disposable worktree is created with `--base-branch <that branch>`. After step 7 it is removed with `orca worktree rm`, because orchestration verbs never delete worktrees (`CR01:23`)." Flag the commit as a user decision point.

### MINOR

- **M1** `PLAN:184` (INV-017): "after 2 guard refusals ... matching K3's 2-cycle cap". K3 is 2 fix cycles, which is 3 attempts (`git show 80f934de`: "at most 2 fix cycles (3 reviews)"). Escalating after 2 refusals allows only 1 fix. Fix: escalate after the third refusal, or drop "matching K3".
- **M2** `PLAN:65` (change 7): states as fact that reflect's precedent "does not fire for an Orca worker (`SPEC:391`)", but `SPEC:391` is UNVERIFIED item 9 ("assumed not"). Fix: mark it UNVERIFIED (assumed).
- **M3** `PLAN:72`, `PLAN:219`: "marks any live Orca terminal by design" is an inference from an error string (`CAPS:149`) plus one worker observation (`CAPS:151`). Item 13 (`SPEC:395`) is not directly resolved. Fix: say "inferred from Orca's identity error text".
- **M4** `PLAN:217`, `PLAN:232`: "deleting the guard sentence returns exactly (a)" is stale once changes 18, 19, 20 and 23 apply. The guard now has a template layout, a never-as-worker list, a file read, a refusal-reading rule in 2.3 and an escalation cap. Fix: name every part in the rollback.
- **M5** `PLAN:157`, `PLAN:183`: the case-3 live run does not name its command. If the guard fails on `/sc:pm` or `/sc:agent`, the run has real side effects (`SPEC:155`, `SPEC:158`). Fix: use `/sc:help` (read-only, `SPEC:157`) in the disposable worktree, and never use pr-submit, pm, agent or git.
- **M6** `PLAN:157`: the template change ("Task text never starts with `/sc:`") is not carried into the spec wording. The worked example (`SPEC:90`, `SPEC:93`) and the AC-2.2/AC-2.6 briefs start with `/sc:`. Also untagged: whether a worker that invokes the command from a mid-brief `Command:` line (via the Skill tool) still runs it "directly", as WC-7 and AC-0.4 (`SPEC:71`, `SPEC:254`) require. Fix: add both to Spec wording changes and to UNVERIFIED.
- **M7** `PLAN:108`: change 13 amends `SPEC:79`, but `SPEC:329` ("writes it into every worker's command line") repeats the same contradiction. Fix: amend both.
- **M8** `PLAN:206`: D3 converged on (a) as the default plus (c), a person-owned handoff tab (`D3/.../debate-transcript.md:665`). Fix: state that the (c) tab has no preamble, so the guard never applies and change 19 stays valid, and that CR-01 T3 applies to that tab.
- **M9** `PLAN:143` (iii), `PLAN:193`, `PLAN:182`: whether Orca's setup runs `make sync-dev` is UNVERIFIED (`CR01:42`) and is not tagged. INV-002's "coordinator uses the same test" reads the coordinator's copy, which can differ from a child worktree's copy. Fix: tag it, and have the coordinator test the worker's worktree copy.
- **M10** `PLAN:12`: `CLAUDE.md:41-66` is not in the citation key and could mean the root file or `src/superclaude/core/CLAUDE.md`. It resolves correctly to the root file. Fix: add a `ROOT-CLAUDE` key.
- **M11** `PLAN:100`: "Nothing loads `WORKER-CONTRACT.md` automatically (`SPEC:58`)". `SPEC:58` says only where the file is installed; the claim is the debate's inference (R2-V3 #3). Fix: cite R2-V3 #3.
- **M12** `PLAN:181` (INV-018): if WC-3's re-invocation drops the token, the run is attended and unguarded. Fix: add this to Known weaknesses, or check the re-invoked line against the brief's line.
- **M13** `PLAN:164`, `PLAN:170`: brainstorm → research runs through Agent-tool Task agents (`BS:179`), not in-session Skill. Change 22 covers both routes, but change 15's "relies on AC-2.1" overlaps it. Fix: one sentence saying change 22 supersedes change 15 for nested commands.
- **M14** `PLAN:157`, `PLAN:164`, `PLAN:180`: "the `Command:` line" (singular) conflicts with "command line(s)". The endorsed `/sc:load` + command brief (`SPEC:197`) needs a defined layout. Fix: one `Command:` line per command, all checked before any runs, which also closes INV-013.

## Verdict

VERDICT: FAIL (3 BLOCKING: B1, B2, B3; 14 MINOR)

## Self-Audit

- Read in full: `refactor-plan.md`, `base-selection.md`, `invariant-probe.md`, `variant-1/2/3-original.md`, `rounds/r1-variant-3.md`, `rounds/r2-variant-1/2/3.md`, `CR-01`, and spec lines 1-406. Read in part: `debate-transcript.md:565-660`, `rounds/r1-variant-1.md:36-42`, `diff-analysis.md:17-20, 98-101`, the D3 transcript at 660-665 plus its option titles, `CORE-CLAUDE:55-84`, `WF:50-69`, `BS:175-194`, `CAPS:144-153`, and `ROOT-CLAUDE:38-67, 88`. Also ran `git show 80f934de`.
- Checked: all 13 mandatory citations and about 60 more; the one-to-one mapping of the 17 strengths; dispositions for the 5 HIGH invariants; pairwise consistency of changes 9/10/18/20/21/22/23/24; SA-1 to SA-6 and non-goals 1-10; K1-K4 against the commit body and CR-01.
- Not checked: `[G]` lines (`orca-ide` was not run), `TL:1618/1623`, the `scoring/` pass files, and `r1-variant-1/2.md` beyond the cited lines. No Claude Code documentation was consulted for command precedence, so B1 relies on the repo's stated skill precedence and the plan's own UNVERIFIED mark.
- Only this review file was written. No existing file was edited, and there were no commits, pushes or GitHub calls.
