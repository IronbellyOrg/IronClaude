# Round 2 rebuttal: advocate C (variant 3, dedicated long-lived git session)

Persona: devops/architect plus analyzer. Date: 2026-11-02. Third rebuttal, after A and B.
Inputs read in full: `round1-advocate-a.md` .. `round1-advocate-e.md`, `round2-advocate-a.md`, `round2-advocate-b.md`, the five variants, `diff-analysis.md`.
Citation keys as in the variants. "Verified" means re-read this round with `sed -n`, `grep -n` or `orca-ide skills get orchestration [--reference references/<name>.md] | cat -n`. Claims I took from another advocate without re-reading are marked UNVERIFIED (by me).

## 1. Response to criticisms

Every criticism of variant 3 in the four other Round 1 files and in A's and B's Round 2 files, grouped where several advocates raised the same point.

| # | Criticism (raised by) | Response |
|---|---|---|
| C1 | Running pr-submit as a worker turns operator HALTs into `blocked` (`SPEC:137`). That removes the person from a loop designed as "attended, in-session" (`sc-pr-submit-protocol/SKILL.md:43`) (A R1 critique 2 and weakness 2; A R2 section 2; B R2) | **Conceded as a real cost of D3 (b). Rebutted as an argument for A's opt-in over C.** Both quotes verified (`SPEC:137`; `SKILL.md:43-45`: "The monitor is an **attended, in-session** loop: closing the session loses it"). Two corrections: (1) The same `SPEC:137` cell says "the worker may use `ask` or `escalation`". So a HALT reaches the coordinator, and through it the person if the person is present. The person is one hop away, not removed. (2) A's own D3 (b) per-PR Task is a pr-submit worker too, so the HALT-to-`blocked` conversion applies to it exactly as it does to C. This objection counts against D3 (b) in any form. It does not separate C from the opt-in A and B now accept. |
| C2 | One git session serializes PR loops anyway, so it gives no parallel monitoring (B R1 weakness 5; A R2 section 2) | **Conceded fully.** My own Round 1 strength 4 proves it: a terminal that already owns an active Dispatch rejects a second one (`[G:rc] 108`, verified). So one git session runs one pr-submit loop at a time. A second, mechanical reason is new evidence N1 below: each pr-submit loop needs a checkout at its own PR head, so N parallel loops need N checkouts. One session in one terminal is the wrong shape. One pr-submit Task per PR, each in its own worktree, is the right one. |
| C3 | The spec recommends D3 (a) "unless parallel PR monitoring is a real need" (`SPEC:343`); C needs D3 (b) as its default (A, B, D, E) | **Conceded.** Verified. With C2 conceded, C's only remaining default-path benefit is coordinator responsiveness during a single PR loop. The spec's (a) already handles that by ordering: pr-submit runs "after the workers finish" (`SPEC:341`, verified). N1 shows that ordering is also needed for correctness, not only convenience. |
| C4 | Retention needs an explicit user request (`[G:rc] 157`). `worker-retain` exists "for debugging". Reuse needs immediate follow-up work (`[G:cl] 48-50`). A standing loop Task breaks the idle rule (`[G:wc] 77-80`). So "long-lived" exists only through user-gated retention (A, B, D, E) | **Conceded; this was my Round 1 concession 3.** All four lines verified in Round 1, and `worker-retain --help` line 5 ("Keep one supervised worker terminal live for debugging") again this round. I withdraw the long-lived session. One part of the mechanics still applies to the opt-in (N3): reuse needs no retention when the follow-up is immediate. |
| C5 | Each fresh git worker pays a readiness start of up to 60 s (`CAPS:44`) for actions that take seconds (A, B, D, E) | **Conceded for local commits and short outward actions** (a comment, a push). Not material for a pr-submit Task, whose per-wait budget alone is 600 s (`commands/pr-submit.md:49`, verified Round 1). That supports confining delegation to pr-submit, as the opt-in does. |
| C6 | Reuse injection into a running Claude session, and final release of a reused terminal, are UNVERIFIED (`CAPS:47` argv only for fresh launches; `[G:rc] 160-161` "Reused ... terminals are retained") (A, D, E) | **Conceded; still UNVERIFIED.** No new evidence this round. Under the opt-in this matters only for N3's optional reuse; a fresh Task with `--resume` needs no reuse. |
| C7 | Authorization takes one hop through a brief. Briefs are immutable (`SPEC:70`), so a revoked grant persists until a new Task replaces it (A weakness 6; D; E weakness 6, "a record of the hop, not a removal of it") | **Conceded on the hop. Rebutted on revocation for C's shape.** `SPEC:70` verified: "A Task's brief cannot change after creation". Under C every action is its own short Task, so a brief lives for one action. Revocation therefore takes effect at the next action, the same timing A claims for itself. Immutability hurts long-running worker Tasks (B's and E's commit lanes) more than per-action Tasks. E's quip is correct: C records the hop and does not remove it. |
| C8 | C does not solve per-task commits (all) | **Conceded (Round 1 concession 2).** E's row with A's four conditions is the answer. |
| C9 | C has no textual advantage under `[G:cl] 62-65`, because the rule is conditional on the user's plan naming an owner (A R1 X-004; A R2 R5) | **Conceded.** Re-read in Round 1: "If the user's plan names a next owner, post-review fixes and PR preparation remain with that owner; the coordinator routes and synthesizes." A is right that this requires *naming* an owner and that C needs the same naming. I move X-004 to A. |
| C10 | Applying `[G] 53-54` (lifecycle authority) to audit is an inference. For outward actions the authoritative record is GitHub (SHA on origin, PR URL) plus pr-submit's write-ahead run-log, which `SPEC:137` already makes the contract artifact (A R2 R7) | **Conceded.** `SPEC:137` verified: the contract "points at `monitor-run-<PR>.jsonl`". I keep only the narrower claim A and B also keep: a per-action Task is the better *Orca* record (C-005, X-002). |
| C11 | A coordinator crash does not lose the record: the Run is durable (`[G] 51-52`) and pr-submit resumes from its run-log (A R2 R8, N1) | **Conceded on the record.** `SKILL.md:44` verified ("Durability comes from the write-ahead JSONL run-log + `--resume`"). C keeps only better crash *detection* (Orca liveness, `CAPS:122-126`), which A concedes. |
| C12 | The git session is a whole Claude session with full Bash and its own permission mode, with no per-actor mechanical restriction (D R1 critique, weakness 3) | **Rebutted in part.** A's N2 reports that settings-level `PreToolUse` hooks run in any Claude session's main conversation (CC-HOOKS; UNVERIFIED by me, I did not fetch it). This repo already registers main-session `PreToolUse` hooks (`.claude/settings.json:3-21`, per A), and a user-level `PreToolUse` freshness hook blocked my own first Edit in Round 1. So a git deny-list can run in a C worker's session as easily as in the coordinator's. D's subagent allowlist is stricter, and the bypass-mode question is UNVERIFIED for every form. |
| C13 | One git actor serving N worktrees is the coordinator-fed form of the quiescence problem (B R1 critique) | **Conceded.** The git session cannot see writers; the coordinator must assert quiescence in each brief (my Round 1 concession 7). P1 (B) and N1 below reduce how often it matters. |
| C14 | C conflicts with the spec twice as written (`SPEC:156`; D3 (b)) (A R2, citing my concession 1) | **Conceded, now moot for local git.** B's and A's evidence (EVAL F0, `issue-326-evaluation.md:50`) shows `SPEC:156`'s "workers make no commits or pushes" cites a run-local rule. Under the merge base, the only worker that pushes is a per-PR pr-submit Task under D3 (b). That needs exactly one carve-out in the `/sc:git` row, the same one A's opt-in needs. |

## 2. Updated assessment

**Does a dedicated long-lived git session still add anything over the per-PR Task opt-in? No.** I withdraw it. My reasons:
- **Parallelism.** The per-PR opt-in gives it; one session cannot (C2, `[G:rc] 108`).
- **Retention.** The opt-in needs none (C4).
- **Pay-off.** The readiness start pays off only for long actions, and pr-submit is the only long one (C5).
- **What survives.** C's per-action audit record (C-005, X-002) and its relay reading (S-004) carry over into a per-action Task unchanged. Nothing C uniquely contributed needs the session to stay alive between actions.
- **Local commits.** A dedicated git session does nothing for local commits that the coordinator, D's optional subagent or E's sole-writer worker cannot do more cheaply.

**Do I accept the merge base? Yes.** It is E's table plus A's four conditions:
1. a default-off, scoped, quoted grant;
2. sole writer as a recorded placement fact;
3. the worker lane dormant until K3;
4. the worker invariant (no user-index writes, commits, HEAD moves or remote actions outside the E row), with distinct slugs.

To that I add the per-PR D3 (b) opt-in, D's guard as an optional tested control, and B's placement rule P1. Each of these matches a concession I have already made.

I ask for three additions. Each comes from new evidence in section 3, and each fills a gap in the opt-in as A and B stated it.

- **M1. Place each pr-submit run on its own PR-head checkout. This applies to the coordinator too.** pr-submit at L1+ requires the checkout to equal the PR head, or it HALTs `pr_head_mismatch` (`SKILL.md:268`, `316`). At L3 it commits one fix commit per cycle in that checkout (`SKILL.md:274`). So every pr-submit run moves HEAD in its checkout. It also treats every file in `git status` at the cycle's first edit as the operator's own pending work (`SKILL.md:272`). It refuses to commit those files, HALTing `fix_commit_failed` (`SKILL.md:318`).
  - Rule: a per-PR Task runs in the worktree whose branch is that PR's head, and no other worker writes there for the whole loop.
  - Under D3 (a), the coordinator's own pr-submit run in a shared worktree waits until no worker writes there, which is what "after the workers finish" (`SPEC:341`) already implies.
  - This is a third P1 trigger, alongside B's (a) granted commits and (b) an implement ladder that shares a worktree.
- **M2. Make the HALT path explicit in the opt-in.** A HALT in a per-PR Task gives `worker_status: blocked` (`SPEC:137`). The worker may `ask` the coordinator first. If it ends blocked, the retry is a new Task with `--resume <run-log.jsonl>` (`SPEC:137` Resume cell; WC-6, `SPEC:70`). A and B both noted that this conversion is the cost of D3 (b). The opt-in should say how a HALT is resumed, so the person is reached through the coordinator and the loop is not lost.
- **M3. Allow same-terminal reuse for the resume, as an optimization only.** If the coordinator holds the answer when it reads the blocked `worker_done`, the resume Task is "immediate follow-up work" for the same agent. It may reuse that terminal (`[G:cl] 48-55`), with no retention request. How the resume text reaches a running Claude session is UNVERIFIED (C6), so a fresh Task is the default.

**On A, B, D and E:**
- **A.** Its Round 2 case against C is correct on serialization, on D3 (a) as default and on retention. I have conceded all three. Its HALT objection (C1) applies equally to its own per-PR opt-in; M2 is the answer for both.
- **B.** P1 is well grounded. I re-read `refs/retry.md:199-221` this round: the domain is a whole-worktree diff from `$start` to `now`, and step 5 restores domain paths from `$start`. I did not separately confirm the `rm -f` branch at line 220 (UNVERIFIED by me). M1 is P1's third trigger.
- **D.** I accept the guard as optional and tested. Under the opt-in, the same settings-level deny-list should also run in each per-PR Task's session (C12).
- **E.** It is the base. My Round 1 recommended merge ("E's table with the outward row delegable to a git worker on request") becomes "E's table, with the D3 (b) per-PR Task opt-in in place of a git session".

## 3. New evidence

None of the following appears in any Round 1 file or in A's or B's Round 2 file as stated here. All was verified this round unless marked.

- **N1. Every pr-submit run is a HEAD-moving writer bound to the PR head checkout.**
  - **Head binding (L1+).** Wave 0 reads `git branch --show-current` and `git rev-parse HEAD` and requires them to match the PR's `headRefName`/`headRefOid`. Otherwise it HALTs `terminal_halted`, reason `pr_head_mismatch` (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:268`; failure table `SKILL.md:316`).
  - **Fix commit (L3).** It commits "exactly one commit" per cycle with `git add -- <paths>` and `git commit --only -- <paths>`, and sets `target_sha := git rev-parse HEAD` (`SKILL.md:274`). That moves HEAD in the checkout.
  - **Operator pending files.** Before a cycle's first edit it records every modified, staged and untracked file (`git status --porcelain=v1 -z --untracked-files=all`) as `OPERATOR_PENDING`, and the fix commit refuses them (`SKILL.md:272`). A fix touching such a file HALTs `fix_commit_failed` (`SKILL.md:318`).
  - **Consequences:**
    - (a) Parallel PR monitoring needs one checkout per PR, because one worktree has one HEAD. This is why a single git session cannot do it (C2), and why each per-PR Task needs its own worktree.
    - (b) A pr-submit run in a worktree where an `/sc:implement` worker runs moves HEAD under it, which triggers that worker's `head-moved` halt (`refs/retry.md:41,44`, verified Round 1). That holds whether the coordinator or a Task runs pr-submit.
    - (c) Other workers' in-flight files in the same checkout become `OPERATOR_PENDING` and can cause spurious `fix_commit_failed` HALTs.
  - So D3 (a)'s "after the workers finish" (`SPEC:341`) is a correctness condition, not only scheduling. M1 states it.
- **N2. The HALT-to-`blocked` cost is shared by every D3 (b) form, and `SPEC:137` already gives the bridge.** The cell reads "operator HALTs resolve as blocked (the worker may use `ask` or `escalation`)", with Resume `--resume <run-log.jsonl>` (`SPEC:137`). The opt-in A and B accept (one pr-submit Task per PR) is a pr-submit worker, so it inherits this unchanged. The person is reached via `ask` to the coordinator. If the Task ends blocked, the loop's state survives in the run-log (`SKILL.md:44`) for a resume Task (M2).
- **N3. Reuse without retention fits the resume case.** Reuse is allowed when "the same exact agent has immediate follow-up work" (`[G:cl] 48-50`, verified Round 1), and needs no user request, unlike retention (`[G:rc] 157`). A blocked pr-submit Task whose answer the coordinator already holds is such a case. This is the one piece of C's persistence mechanics that survives into the merge (M3), with the injection path still UNVERIFIED (C6).
- **N4. pr-submit forbids headless or detached runs, and whether a chat-mode Orca worker counts is UNVERIFIED.** "Run headless / detached, or imply a background daemon" is in the skill's do-not list (`SKILL.md:303`). A terminal Orca worker is an interactive Claude TUI (`CAPS:47`, readiness waits for the agent's input box), which is not headless. But `worker-start --help` line 44 says "Not every worker has a terminal", and how a worker runs follows the user's own setting for new agent tabs (line 42). Whether a chat-tab worker satisfies "attended, in-session" (`SKILL.md:43`) is UNVERIFIED. This applies to every D3 (b) form, including the per-PR opt-in, and should be checked before the opt-in is specified.

## 4. Updated shared-assumption responses

A-002 is unchanged (REJECT: compare porcelain status with the contract and report extras, never sweep). A-004 is unchanged in verdict.

| ID | Response | What changed |
|---|---|---|
| A-001 (coordinator attended) | **QUALIFY** | I no longer claim C's per-Task brief is the best answer when the person leaves. E's handling is better: a default-off grant (`issue-326-evaluation.md:74`, verified) caps unattended exposure at reversible local commits, and every outward action needs an instruction that names it. A per-PR Task is outward, so it needs that named instruction. |
| A-003 (quiescence knowable) | **QUALIFY** | Added: pr-submit needs quiescence for the **whole loop**, not only at commit time, because it moves HEAD each cycle and snapshots `OPERATOR_PENDING` per cycle (N1). This holds for the coordinator under D3 (a) and for a per-PR Task under D3 (b). Like B's implement-ladder point, it is best made true by placement (M1) rather than by a commit-time check. |
| A-005 (standing instruction covers later commits) | **QUALIFY** | Now anchored in `issue-326-evaluation.md:74` (verified Round 1): an authorized option, never a default. A standing grant covers local commits only, for the named run and branch. A per-PR Task needs an instruction naming that PR (D4 (a), `SPEC:346`). I drop my Round 1 claim that per-action quoting was C's distinct advantage, because E's per-Task quoting is the same mechanism. |

## 5. Updated per-point table

| Point | Superior variant | Changed from Round 1? | Reason |
|---|---|---|---|
| S-001 | V5 (E) | No | The per-action owner/condition table is the merge base's form. |
| S-002 | V3 (C) | No | Only C verified Orca reuse, serialization, retention and idle-rule mechanics; they now explain why the session form fails and the per-PR form works. |
| S-003 | V1 (A) | No | GITDEMO is the procedure everyone cites. |
| S-004 | V3 (C) | No | Only C explains why the #326 relay cannot be something commands call; the per-action Task is that relay's honest shape. |
| C-001 | V5 (E), rule originated in V1, with P1 | No (qualified) | Coordinator commits in a shared worktree at quiescence; P1 keeps ladders and pr-submit loops out of it. |
| C-002 | V5 (E) | No | Only E times commits in the ladder-safe window with a sole-writer guard; dormant until K3. |
| C-003 | V1 = V5 | Yes (was V3) | Coordinator main chat by default; one pr-submit Task per PR only on explicit request (C2, C3). |
| C-004 | V5 (E) | Yes (was V1) | Direct for outward; scoped, quoted, default-off grant for reversible local commits (`issue-326-evaluation.md:74`). |
| C-005 | V3 (C) | No | One Task, brief, `worker_done` and contract per action is the best Orca record; carried by the per-PR opt-in. |
| C-006 | V3 (C), realized as the per-PR opt-in | No (qualified) | Taking the pr-submit loop off the coordinator is the largest context saving; the opt-in delivers it without a session. |
| C-007 | V5 (E) | No | Lock confined to one worktree, earlier commits survive; pr-submit resumes from its run-log under any owner (`SKILL.md:44`). |
| C-008 | V5 (E), with P1 and M1 | No (qualified) | Shared default for report-only workers; own worktree for granted committers, implement ladders and pr-submit loops. |
| C-009 | V1 (A) default, per-PR D3 (b) opt-in | Yes (was V3) | One session serializes loops (`[G:rc] 108`) and N loops need N checkouts (N1); per-PR Tasks give parallelism. |
| C-010 | V1 (A) | No | Wording only. |
| C-011 | V5 (E) | No | Only E names the owner and the F3 guard; P1 and M1 add worktrees it must clean up. |
| X-001 | V5 (E) | No | A quoted, scoped grant suffices for a reversible local commit; never for outward actions. |
| X-002 | V3 (C) | No | Per-action Orca records beat a transcript; GitHub and the pr-submit run-log remain the outward record (C10). |
| X-003 | V1 = V4 = V5, with per-PR opt-in | Yes (was V3) | Coordinator main chat matches D3 (a) and pr-submit's top-level rule; D3 (b) only as one Task per PR on request. |
| X-004 | V1 (A) | Yes (was V3) | The rule is conditional on a named owner (`[G:cl] 62-65`); C needs the same naming, so it has no textual edge (C9). |
| X-005 | V4 (D), as amended | Yes (was V4 caveat only) | Per A and B, the frontmatter `hooks` field gives the restriction (CC-SUB, UNVERIFIED by me); bypass-mode behaviour UNVERIFIED for every form. |
| A-001 | V5 (E) | Yes (was V3) | With the person gone, E caps exposure at reversible local commits. |
| A-002 | V5 (E) | No | A sole-writer worker's `git status` is ground truth; shared rows use the porcelain cross-check. |
| A-003 | V5 (E), with P1 and M1 | No (qualified) | Placement makes run-long quiescence true for ladders (B) and pr-submit loops (N1). |
| A-004 | V5 (E) | No | Both E commit paths keep hook rewrites away from concurrent writers; stop and report, never `--no-verify`. |
| A-005 | V5 (E) | Yes (was V3) | E's per-Task quoting of a scoped, default-off grant is the same mechanism I credited to C. |

**Tally:** E 13 alone plus 2 shared (C-003, X-003), C 5 (S-002, S-004, C-005, C-006, X-002; C-009 is counted for A even though the opt-in uses C's per-action shape), A 4 alone (S-003, C-009, C-010, X-004) plus 2 shared, D 1 alone (X-005) plus 1 shared, B 0. Eight points changed (C-003, C-004, C-009, X-003, X-004, X-005, A-001, A-005), all toward E, A's default or D's amended guard.

**Overall:** C as a long-lived session is withdrawn. Its per-action Task shape, its Orca mechanics and its relay reading survive as the D3 (b) per-PR opt-in, which I accept on top of the E merge base with M1 (pr-submit's own placement), M2 (explicit HALT resume) and M3 (reuse without retention for the resume).
