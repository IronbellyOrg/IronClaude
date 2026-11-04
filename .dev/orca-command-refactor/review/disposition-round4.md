# Disposition, round 4 (combined revision, Task 12)

Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
Frozen baseline: `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md` (89,089 bytes)
Inputs (binding): `.dev/orca-command-refactor/decisions/APPROVED.md`

## 1. Item dispositions
Line numbers are lines of the revised spec (`SPEC:N`, 451 lines) as written on 2026-11-02. "Verbatim" means the text was copied from the named wording source; "adapted" means a named change was needed and is recorded in section 2 or 4.

### Decisions D1-D5 and GIT
| ID | Status | Where applied (section, `SPEC:N`) | Notes |
|---|---|---|---|
| D1 W1 | Applied, verbatim | 2.1 Unattended mode, `SPEC:55` | |
| D1 W2 | Applied, verbatim | 2.1 Contract file, `SPEC:59` | Same line also gains WC-13 (D5 Edit 4). |
| D1 W3 | Applied, verbatim | 2.1 Brief guard, Never-as-worker list, Nested propagation rule, `SPEC:60-62` | |
| D1 W4 | Applied, verbatim | 2.3 first paragraph, `SPEC:84` | Merged in one sentence with D4's authorization wording and GIT 4.3's placement wording. |
| D1 W5 | Applied, verbatim | 2.3 Brief layout, `SPEC:86` | |
| D1 W6 | Applied, verbatim | 2.3 Reading a result, `SPEC:96` | |
| D1 W7 | Applied, verbatim | 2.3 worked example steps 1 and 4, `SPEC:125`, `SPEC:128` | |
| D1 W8 | Applied, verbatim | AC-2.2 and AC-2.6 Check cells, `SPEC:315`, `SPEC:319` | |
| D1 W9, W10, W11 | Superseded, not applied as written | Section 9, `SPEC:390` | They edit the old D1 option bullets, which the brief replaced with a short record of the approved outcome. The outcome (option (c)) is recorded in the D1 row. |
| D1 W12 | Applied, verbatim | UNVERIFIED item 13, `SPEC:437` | |
| D1 W13 | Applied, verbatim | UNVERIFIED items 24-27, `SPEC:448-451` | |
| D1 W14 | Applied, verbatim, merged with CR-01 | 7.2 opening and step 1, `SPEC:282-283` | One edit, as the APPROVED.md D1 row asks. Also closes FDR-D3, PATHS for 7.2, and D4's 7.2 edit. |
| D1 W15 | Applied, verbatim | AC-1.1 `SPEC:307`, AC-1.3 `SPEC:309`, AC-1.7 `SPEC:313`, AC-2.1 `SPEC:314`, AC-2.9 `SPEC:320`, 7.4 rows `SPEC:364-365` | AC-2.9 sits after AC-2.6 as W15 says, so it precedes AC-2.8. |
| D1 W16 | Applied, verbatim | P2 row `SPEC:222`; brainstorm row `SPEC:142`; workflow row `SPEC:152` | |
| D2 4.1 | Superseded by the short record | Section 9 D2 row, `SPEC:391` | The (a) and (c) routes, the Ruling line format and "never relays" are kept in the record; the full option text is not, per the brief. |
| D2 4.2 | Applied, verbatim | WC-3, `SPEC:71` | |
| D2 4.3 | Applied, verbatim | WC-4, `SPEC:72` | |
| D2 4.4 | Applied, verbatim (dagger marks dropped) | 2.3 `failed`/`blocked` bullet `SPEC:95`; "After an `/sc:implement` stop" `SPEC:100-120` | The † marks in the source only flag merge-added rules; they are provenance, not spec text. |
| D2 4.5 | Applied, verbatim | 3.2 implement row, `SPEC:169` | Same cell also carries D4's implement edit. |
| D2 4.6 | Applied, verbatim | AC-4.1 Pass cell, `SPEC:326` | |
| D2 4.7 | Applied | `SPEC:15` (`qa.md:247-256`), P4 row `SPEC:224` (`qa.md:254`), non-goal 6 `SPEC:379` (`qa.md:254`) | Anchors re-read on this branch: `qa.md:247-256`, `:283`; `ledger.md:65,71,153-156`; `retry.md:498` all hold. |
| D3 Edit 1 | Applied, adapted | Section 4 pr-submit paragraph `SPEC:201`; section 9 D3 row `SPEC:392` | Normative text moved to section 4 because section 9 became a short record; L2 sentence added (section 2, C3). |
| D3 Edit 2 | Applied | pr-submit row, `SPEC:174` | Deleted "(the worker may use `ask` or `escalation`)". Re-checked citations against the current skill: `SKILL.md:43-49,51-86,234-248,267-274,313-318` replace `37-39,46-64,66-68,141,170,189-197,237-246` (the old `141` and `170` had no identifiable current target and were dropped); `cmd/pr-submit.md:25,39,49,55-56` re-read and kept. "outward actions per open decision D3" became "this row applies only if D3 (b) is ever adopted". |
| D3 Edit 3 | Applied | WC-7 `SPEC:75` (`:47-49`); WC-10 `SPEC:78` (`:51-80`) | The same stale anchors were fixed at `SPEC:15` (`:47-49`), P4 row `SPEC:224` (`:267,274`) and UNVERIFIED item 12 `SPEC:436` (`:56-58`), under D3's re-check instruction. |
| D3 Edit 4 | Applied, verbatim | AC-4.4, `SPEC:329` | |
| D3 Edit 5 | Applied | P4 row, `SPEC:224` | "35, or 36 with pr-submit" stays conditional as D3 says, renumbered for CMD (37, or 38). |
| D4 block (sections 2 and 5) | Superseded by the short record; rules moved | Section 9 D4 row `SPEC:393`; commit rule in WC-9 `SPEC:77`; coordinator side in 2.3 `SPEC:90` | The block's normative content (outward list, commit conditions and refusals, confirm at the moment of action, review before push) now lives in WC-9 and 2.3. |
| D4 WC-9 | Applied, verbatim core plus GIT 4.1 | WC-9, `SPEC:77` | `README.md:31` citation removed. |
| D4 WC-5 | Applied, verbatim | WC-5, `SPEC:73` | |
| D4 2.3 | Applied | Authorization clause verbatim `SPEC:84`; placement record, absolute report directory inside a child and distinct plan slugs `SPEC:88`; review before push, grant ends at `worker_done`, no commit or merge where a worker runs or an implement Task is frozen `SPEC:90` | Coordinator-duty wording from `decisions/D4/debate/adversarial/merged-output.md:51,58-65`, which D4 section 5 names as the full text. |
| D4 section 3 rows | Applied | auggie-review `SPEC:160`; implement `SPEC:169`; post-release `SPEC:173`; task `SPEC:181` | |
| D4 `/sc:git` row | Applied (GIT 4.4 text, same content) | `SPEC:193` | |
| D4 AC-4.2 | Applied | AC-4.2 `SPEC:327`; new P0 check AC-0.8 `SPEC:305` | |
| D4 7.2 | Applied through D1 W14 | `SPEC:282-283` | |
| D4 "CR-01 edits replace F2" | Applied | see the CR-01 and F2 rows | |
| D5 M10 (D5 entry) | Superseded by the short record | Section 9 D5 row, `SPEC:394` | Precondition and revisit trigger kept in the record. |
| D5 Edit 1 | Applied, verbatim | E4, `SPEC:28` | |
| D5 Edit 2 | Applied, verbatim | R1, `SPEC:37` | |
| D5 Edit 3 | Applied, verbatim | Non-goal 2, `SPEC:375` | |
| D5 Edit 4 (WC-13) | Applied, verbatim | WC-13 `SPEC:81`; contract-file list `SPEC:59` | Evidence "INV-005" given its file path so it resolves. |
| D5 Edit 5 | Applied, verbatim | 2.3 bullet, `SPEC:98` | "(section 9)" added to point at the revisit trigger's new home. |
| D5 Edit 6 | Applied | AC-C1 `SPEC:244` (block verbatim; description written from the plan's stated content, since D5 gives no exact words); AC-C6 `SPEC:276-279`, verbatim | |
| D5 Edit 7 | Applied, verbatim | 7.2 step 5, `SPEC:291` | |
| D5 Edit 8 | Applied, verbatim | AC-0.7 `SPEC:304`; command block `SPEC:341-342` | |
| D5 Edit 9 | Applied, verbatim | 7.4, `SPEC:363` | |
| D5 Edit 10 | Applied, verbatim | UNVERIFIED item 5, `SPEC:429` | |
| GIT 4.1 (WC-9) | Applied, merged with D4 | WC-9, `SPEC:77` | D4 wins on the points section 6 names (section 2, C1). The D3 (b) worker exception is dropped per L1. |
| GIT 4.2 (WC-11) | Applied, adapted | WC-11, `SPEC:79` | "when it runs `/sc:pr-submit`" dropped per L1. Supersedes CR-01's shorter WC-11 sentence (section 2, C4). |
| GIT 4.3 (2.3) | Applied, adapted | Placement clause `SPEC:84`; "Feature worktree and child worktrees" `SPEC:88`; "Git and GitHub ownership" `SPEC:90` | "in its main chat" and "run from the PR-head checkout" replaced by "run as section 4 states" per L1. |
| GIT 4.4 (`/sc:git` row) | Applied, verbatim | `SPEC:193` | Also applies F0. |
| GIT 4.5 (D3 bullets) | Not applied | none | Superseded: section 9 is a short record, and L1 drops the per-PR worker opt-in and the main-chat wording. |
| GIT 4.6 (D4 block) | Not applied | none | D4's own wording wins (APPROVED.md GIT row), and section 9 is a short record. |
| GIT 4.7 | Applied | Section 3 rows: as D4 rows. 7.2: W14. `.dev/tasks` deferral and MDTM `git add -A` refusal: WC-9 `SPEC:77`. CR-01 check: AC-4.5 `SPEC:330`. Write-verb scan test: AC-0.9 `SPEC:306` | AC-0.9 wording from `decisions/git-ownership/debate/adversarial/merged-output.md:131`. Skill staging lines re-read: `managed-workspace.md:36`, `ledger.md:3`, `sc-workflow-protocol/SKILL.md:28`, `task/SKILL.md:35`, `task-builder/SKILL.md:2237`. |

### Loose ends L1-L3
| ID | Status | Where applied | Notes |
|---|---|---|---|
| L1 | Applied | Section 4 pr-submit paragraph `SPEC:201`; WC-9 `SPEC:77` and WC-11 `SPEC:79` (GIT's pr-submit worker exception and trigger dropped); 2.3 `SPEC:90` ("run as section 4 states"); section 9 `SPEC:396` | D3 allows the coordinator's own session only after AC-4.4 (2) passes; that sentence is kept. |
| L2 | Applied | Section 4 pr-submit paragraph `SPEC:201`; section 9 `SPEC:396` | Conflict with D3's child-worktree model resolved in section 2, C3. |
| L3 | Applied | 2.3 Git and GitHub ownership `SPEC:90`; WC-9 `SPEC:77`; section 9 `SPEC:396` | |

### Other items
| ID | Status | Where applied | Notes |
|---|---|---|---|
| CR-01 2.3 placement | Applied through GIT 4.3's placement wording | `SPEC:84` | GIT's wording points at WC-11, which now holds the triggers. |
| CR-01 WC-11 | Applied through GIT 4.2 | `SPEC:79` | T3 (pr-submit worker) dropped per L1. |
| CR-01 Feature worktree paragraph | Applied through GIT 4.3 | `SPEC:88` | "Linked to its issue" not applied: the owner's resolution forbids Orca issue/PR linking until it resolves to the fork; the ban is stated at `SPEC:90`. |
| CR-01 section 7 check | Applied, verbatim | AC-4.5 `SPEC:330`; 7.4 WC-11 row `SPEC:360` | Placed in P4 because implement accepts `--unattended` only from P4. |
| CR-01 owner resolutions | Applied | Orca default paths: `SPEC:88`, `SPEC:282`; no Orca issue/PR linking: `SPEC:90` | |
| CR-01 open question 2 (setup content) | Applied | `SPEC:88`, `SPEC:282`, UNVERIFIED 27 `SPEC:451` | |
| FDR-D1 (blocking) | Applied | WC-6, `SPEC:74` | The three-failure comparison now ignores the report-directory value and says the coordinator, not Orca, makes it. |
| FDR-D2 (blocking) | Applied | WC-3 opening `SPEC:71`; Decisions row "Blocked-gate choice" `SPEC:409` | Took the fix direction "reword the opening sentence to say the worker applies the stated test". |
| FDR-D3 (blocking) | Applied through D1 W14 | 7.2 `SPEC:282-283`; UNVERIFIED 24 and 27, `SPEC:448`, `SPEC:451` | Phase edits are committed to a branch, the worktree is created by Orca from it, `make sync-dev` runs in it, every command copy is checked before dispatch, and copy precedence is listed as UNVERIFIED, as the fix direction asked. |
| F0 | Applied | `/sc:git` row, `SPEC:193` | |
| F1 | Applied, in D4's form | WC-9 `SPEC:77` (a commit is not outward but needs a grant, stages `.dev/tasks`, never pushes, falls between tasks); implement row `SPEC:169` | D4 replaces F1's implement-row sentence with "no commit inside the command; per-task commits wait for #326 K3" (`decisions/D4/debate/adversarial/merged-output.md:90`). |
| F2 | Applied as replaced | WC-11 `SPEC:79` (experiment trigger); `SPEC:88` (setup before dispatch) | Its location `.dev/worktrees/<run>-<n>/` is replaced by Orca's default paths, as APPROVED.md says. |
| F3 | Applied | 2.3 `SPEC:88` (removal guard, widened by GIT 4.3) | |
| F4 | Applied | 2.3 Git and GitHub ownership, `SPEC:90` | Placed in 2.3 rather than the D4 block, because section 9 is now a short record. |
| F5 | Applied per L1 | 2.3 `SPEC:90` ("PRs go only through `/sc:pr-submit --monitor 3` ... run as section 4 states") | `/sc:git` is not named as an outward path. |
| CMD | Applied | Count `SPEC:132`; 3.1 header `SPEC:136`; rows `SPEC:144-145`; WC-4 status mapping `SPEC:72`; P1 row `SPEC:221`; phase table `SPEC:231-234`; total `SPEC:236`; Decisions row `SPEC:415`; shifted citation `src/superclaude/core/CLAUDE.md:65` → `:66` at `SPEC:238` | Classification in section 4. Other cited routing-guide and root `CLAUDE.md` lines re-read and found unshifted: `HOW-WE-WORK.md:22,171,215,221,249,254,280,282,324`; `CLAUDE.md:16,37,50,74,76,83,157,248,334,408`. |
| PATHS | Applied | 7.2 `SPEC:282`; 2.3 `SPEC:88` | The only remaining `.dev/worktrees/` strings (`SPEC:88`, `SPEC:282`) say worktrees are never placed there. The `CLAUDE.md:299` citation is gone. |
| UPSTREAM | Applied | 2.3 Git and GitHub ownership, `SPEC:90` | Every outward action targets `IronbellyOrg/IronClaude`, never the SuperClaude upstream or Orca's issue/PR linking while Orca records the project as upstream. |

## 2. Conflicts resolved
| # | Conflict | Sources | Resolution and rule used |
|---|---|---|---|
| C1 | WC-9 wording: GIT 4.1 lets `/sc:task`'s own commit step run under a grant, records the commit ID in `artifacts`, reports a refused commit as `blocked`/`partial`, and lets installs and paid runs turn on by flag | `decisions/git-ownership/RECOMMENDATION.md:48,104-109`; `decisions/D4/RECOMMENDATION.md:77,81-82` | D4's wording used on each point (command commit step off; commit ID in the `worker_done` body; refused commit = outcome `failed` per WC-5; installs, VM and paid runs never by a worker). Rule: APPROVED.md GIT row, "D4's wording wins where section 6 says so"; git-ownership section 6 adopts D4 on points 1-3, and its section 4.6 keeps installs with the coordinator. |
| C2 | Who runs `/sc:pr-submit`: GIT keeps an opt-in pr-submit worker per PR (O3) and has the coordinator run it in its main chat from the PR-head checkout; D3 uses a separate ordinary session per PR in its own child worktree | `decisions/git-ownership/RECOMMENDATION.md:12-13,48,52,60,70-71`; `decisions/D3/RECOMMENDATION.md:65` | D3's model applied; O3, GIT's WC-11 pr-submit trigger and its "main chat"/"PR-head checkout" wording dropped, keeping D3's coordinator-session route only after AC-4.4 (2). Rule: L1. |
| C3 | Branch the PR comes from: L2 says one PR per feature from the feature branch after merge-back; D3 says the session's checkout is the PR's own child worktree whose own branch is the PR head | APPROVED.md L2; `decisions/D3/RECOMMENDATION.md:65,92` | Both kept: the PR is opened only after every child is merged back into the feature branch (L2), and the PR's child worktree is then created from the feature branch, its own branch being the PR head (D3), because git checks a branch out in one worktree only and the feature worktree holds the feature branch (`SPEC:201`). Rule: L1 (D3's model wins for pr-submit), with L2 deciding which work the PR carries. |
| C4 | WC-11 and 2.3 wording: CR-01 and GIT each give a WC-11 sentence and a "Feature worktree" paragraph | `changes/CR-01-feature-worktree-hierarchy.md:28-30`; `decisions/git-ownership/RECOMMENDATION.md:52,56,58` | GIT's text used: it contains every CR-01 rule and adds the owner's later resolutions (Orca default paths, no issue linking, removal guards). CR-01's "linked to its issue" dropped per CR-01's own open question 5 resolution. One text instead of two (prefer replacing over adding). |
| C5 | Section 9 format: each D source gives a full replacement D-block; the brief asks for a short record | Task 12 brief; D1 W9-W11, D2 4.1, D3 Edit 1, D4 section 5, D5 M10 | The brief wins on format. Normative content of those blocks was moved to the rule sections (D2 freeze in 2.3; D3 model in section 4; D4 commit rule in WC-9, coordinator side in 2.3; D5 precondition in non-goal 2); option analysis stays in the recommendation files the record points to. |
| C6 | Resume selector: GIT says a resume runs in its existing child "selected with `--worktree id:<worktree id>`"; D2 says an implement resume Task starts "by selector (`--worktree path:<absolute worktree path>`)" | `decisions/git-ownership/RECOMMENDATION.md:58`; `decisions/D2/RECOMMENDATION.md:105` | Both kept verbatim (`SPEC:88`, `SPEC:120`): both select the same existing worktree, and D2's sentence is the specific rule for an implement resume. No precedence rule in APPROVED.md covers it, so neither was rewritten. |
| C7 | Brief shape: D5's text says a brief carries one command line; D1's layout allows several `Command:` lines | `decisions/D1/RECOMMENDATION.md:95` | D1's layout used (`SPEC:86`), as D1 recommends; D5's "(the brief carries one command line, section 2.3)" lived only in its option (b) text, which the short record does not carry. |

## 3. Minor defects (FDR-D4..D7) touched
Under PR #343 these are notes; they were touched only where a line was already edited for another item.

| ID | Status | Reason |
|---|---|---|
| FDR-D4 | Not applied | The fan-in paragraph (`SPEC:122`) is not edited by any other item. |
| FDR-D5 | Not applied | The reading-guide line (`SPEC:134`) is not edited by any other item. |
| FDR-D6 | Applied | WC-6 was already edited for FDR-D1; the stall-settle clause is at `SPEC:74`. |
| FDR-D7 | Resolved without an edit | D1 W14 now commits the phase's edits before Orca creates the worktree, so 7.2 step 6 no longer lists them and "step 6 empty" in AC-1.5 can hold. AC-1.5 (`SPEC:311`) was not edited. |

## 4. Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Verdict for `/sc:graph` and `/sc:impact` (CMD) | Section 3.1 ready; section 3.2 change; section 4 coordinator-only | 3.1 ready. Both have a directory-valued `--output-dir` and already write `return-contract.yaml` there (`cmd/graph.md:33`; `cmd/impact.md:37,47-50`), and neither waits on a person: impact "never stops its caller" (`sk/sc-impact-protocol/SKILL.md:15`); graph's flag errors STOP with a written `blocked` contract (`sk/sc-graph-protocol/SKILL.md:23,110`) and its only state-changing step, `init`, runs only when the user's own message starts with `/sc:graph init` (`cmd/graph.md:48`), which a worker brief never does. Section 4 would have grown the never-as-worker list, which D1 ties to section 4's six commands. |
| How their `status: blocked` maps (CMD) | Leave unmapped; map to `blocked`; map to `failed` | `failed` with the STOP in `reason`, added to WC-4's existing mapping list (`SPEC:72`). Their `blocked` is a flag STOP with no question, so mapping it to worker `blocked` would fail 7.2 step 4's `blocked_question` assertion; one clause in the existing list replaces a per-row fix. |
| Where D3's normative text goes | Section 9; section 4 | Section 4, beside the coordinator-only commands, because section 9 is now a short record (C5). |
| Phase for the CR-01 check | P0; P4 | P4 (AC-4.5): it needs an unattended `/sc:implement`, which accepts the flag only from P4. |
| Phase for the write-verb scan (GIT 4.7) | P0; per phase | P0 (AC-0.9), the phase that adds `test_worker_contract.py`; hits not yet refused under `--unattended` go on the allowlist with a reason, as the GIT text allows. |
| D2 dagger marks | Keep; drop | Drop: they mark provenance in the recommendation file, not spec meaning. |
| Header provenance line | Add; omit | Added (`SPEC:7`), same form as the Task 6-10 lines; "Revised last" moved from Task 10's line to it. Not a rule, check or mechanism. |

Residual observations (no item asks for a change, so nothing was edited; listed for the reviewer):
1. D1 W3 and W5 say a WC-3 re-invocation "keeps every token of the brief's `Command:` line ... and only adds the answer", while WC-3 (`SPEC:71`) says the answer becomes the command's argument, for tdd the topic argument. For a bare-topic tdd gate the two readings differ.
2. GIT 4.2's WC-11 sentence (`SPEC:79`) lets workers share the feature worktree "only when they write nothing but their own report directory", but names no placement for a worker that edits source without a child trigger (for example `/sc:cleanup` or `/sc:document`).
3. AC-0.8 (`SPEC:305`) is a P0 check, as D4 asks, but a WC-9 commit needs `worker_status: succeeded`, and worker contracts arrive only in P1.
4. The spec is a tracked file (committed in `ce642492`), so `git status --short` shows it modified; that is the edit this task assigns, not a stray change.

## 5. Final byte count
`wc -c`, run 2026-11-02 after the last edit: **115,819 bytes**, 451 lines (baseline 89,089 bytes, 405 lines; +26,730 bytes). `git diff --no-index --stat`: 137 insertions, 91 deletions. The growth is almost all approved wording (D1 W3/W5/W15, D2 4.4, D3 Edit 1 and 4, GIT 4.1-4.3, D5 Edits 4-8); section 9 shrank from five option blocks to a seven-row record.

## Fix pass 1 (Task 14, round-4 blocking findings B1 and B2)
Inputs: `review/round4-review.md` findings B1 (`:97-101`) and B2 (`:103-106`); `decisions/APPROVED.md:32-36` ("Round-4 review fixes"). Baseline: `specs/history/spec-v5-after-round4.md` (115,819 bytes), byte-identical to the spec before this pass (`cmp`, 2026-11-02). Scope: B1 and B2, plus only the lines that would otherwise contradict them; the 11 minor findings (m1-m11) are notes under PR #343 and were not touched. Line numbers below are `SPEC:N` after this pass (451 lines). Diff: `git diff --no-index --stat` against the baseline: 6 insertions, 6 deletions.

### Rows
| ID | Status | Lines changed (`SPEC:N`) | What changed |
|---|---|---|---|
| B1 | Applied | 7.2 opening, `SPEC:282` | "`~/.claude` is never reinstalled for this check" replaced: before the phase's live checks the coordinator asks the owner for approval, then installs the phase into `~/.claude` by running `superclaude install` from the phase branch; one approval per phase, asked before every phase's install; an abandoned phase is reinstalled from master. One adaptation: "from the phase branch" is spelled out as `uv run superclaude install` inside a checkout of that branch, because the installer copies from the running package's own location (`src/superclaude/cli/install_core.py:117-122`, read 2026-11-02), so a separately installed `superclaude` would install its own files and the copies would still disagree. |
| B2 | Applied | P0 row removed (was `SPEC:305`); new P1 row `SPEC:313` | AC-0.8 moved to P1, after AC-1.7, renumbered AC-1.8 to fit the per-phase ID scheme; Check and Pass cells unchanged word for word. Recorded as a placement adaptation of D4's "one P0 check" in the section 9 D4 row (below) and here. |
| B1 consequence | Applied | Phase gating, `SPEC:216` | "Phases 1-3 need no user decision" became "... no user decision beyond the per-phase approvals of section 7.2"; B1 adds an owner approval to every phase, so the old sentence contradicted it. |
| B1 consequence | Applied | Decisions row "Phase order", `SPEC:414` | "user decisions are needed only at the end" became "user decisions, beyond the per-phase approvals of section 7.2, are needed only at the end", for the same reason. |
| B2 consequence | Applied | 7.4 WC-9 row, `SPEC:358` | `AC-0.8` reference replaced by `AC-1.8` (kept in phase order: AC-0.9, AC-1.8, AC-2.4, AC-4.2). |
| B2 consequence | Applied | Section 9 D4 row, `SPEC:393` | `AC-0.8` replaced by "AC-1.8 (D4's P0 check, placed in P1, the first phase with WC-4 contracts)", which records the adaptation where D4's checks are listed. |
| B1 check, no edit | Not changed | 7.2 step 1 copy check, `SPEC:283` | Still correct: with the phase installed, both the worktree copy (`make sync-dev`) and the `~/.claude` copy carry the section, so the confirmation can pass. No contradiction, so no edit. |
| B1 check, no edit | Not changed | Brief guard stale-copy refusal, `SPEC:60`; UNVERIFIED 24, `SPEC:448` | The refusal now fires only when the install was skipped or is stale, which is the intended behaviour; neither line claims `~/.claude` stays pre-phase. |
| B1 check, no edit | Not changed | Brief layout, `SPEC:86`; coordinator install rule, `SPEC:90`; D4 record, `SPEC:393`; SA-1 hard requirement, `SPEC:204` | `SPEC:86` already has the coordinator test the copies the worker will see. `SPEC:90` and `SPEC:393` give every install to the coordinator with the user's named instruction, which the per-phase owner approval satisfies. `SPEC:204` is about each command's standalone behaviour, which phase edits keep (SA-1, SA-4), so installing a phase does not break it. |
| B2 check, no edit | Not changed | AC-0.4 `SPEC:301`; AC-4.2 `SPEC:327` | AC-0.4 already says the contract arrives in P1; AC-4.2 is the source of the "four records" AC-1.8 cites and does not cite AC-0.8. A spec-wide grep for `AC-0.8` after the pass returns no line. |

### Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| ID of the moved check | Keep `AC-0.8` in the P1 block; renumber to `AC-1.8` | Renumber: every other check ID names its phase (`AC-1.1`-`AC-1.7` in P1), so `AC-0.8` under P1 would mislead; the content is unchanged and both references were updated. |
| Where to record the B2 placement adaptation | A note inside the moved row; the section 9 D4 row; this file only | Section 9 D4 row plus this file: APPROVED.md keeps the row content unchanged, and the D4 row is where the spec lists D4's checks. |
| How "from the phase branch" is written | Bare `superclaude install`; `uv run superclaude install` in a checkout of the phase branch | The latter: `_get_core_source` resolves from `Path(__file__)` (`install_core.py:117-122`), so only the checkout's own package installs the branch's files; a bare pipx `superclaude` would leave `~/.claude` pre-phase and B1 would recur. The master reinstall keeps APPROVED.md's words. |
| Touch the minor findings | Fix any on lines already edited; leave all | Leave all: none of m1-m11 sits on a line this pass edits except m1's mention of `SPEC:283` and AC-0.8, and neither was reworded. |

### Final byte count
`wc -c`, run 2026-11-02 after the last edit: **116,538 bytes**, 451 lines (baseline `spec-v5-after-round4.md` 115,819 bytes, 451 lines; +719 bytes). `git status --short` shows only the spec (already tracked and modified) and this file (untracked) changed by this pass.

## Fix pass 2 (Task 16, recheck finding N1, last allowed fix pass)
Input: `decisions/APPROVED.md:36` (row B1-N1), which requires both B1 install lines to use `superclaude install --force`. Baseline: `specs/history/spec-v6-after-fix1.md` (116,538 bytes), byte-identical to the spec before this pass (`cmp`, 2026-11-02). Sources re-read 2026-11-02: `src/superclaude/cli/install_commands.py:55-57` (`if target_file.exists() and not force:` skips the file) and `update.sh:8` (`superclaude install --force`). Scope: B1-N1 only; no other line touched. Diff: `git diff --no-index --stat` against the baseline: 1 insertion, 1 deletion.

### Rows
| ID | Status | Lines changed (`SPEC:N`) | What changed |
|---|---|---|---|
| B1-N1 | Applied | 7.2 opening, `SPEC:282` (only line changed) | Phase-branch install: `superclaude install` became `superclaude install --force`, and its spelled-out form `uv run superclaude install` became `uv run superclaude install --force`. Master reinstall after an abandoned phase: `superclaude install` became `superclaude install --force`. One sentence added after them giving the reason with citations: without `--force` the installer skips every existing file (`src/superclaude/cli/install_commands.py:55-57`), so the phase would never reach `~/.claude`; `update.sh:8` runs the same command. A grep of the spec for `superclaude install` now returns only these four `--force` forms, all on `SPEC:282`. |

### Final byte count
`wc -c`, run 2026-11-02 after the last edit: **116,815 bytes**, 451 lines (baseline `spec-v6-after-fix1.md` 116,538 bytes, 451 lines; +277 bytes).
