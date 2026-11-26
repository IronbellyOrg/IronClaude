# Reflect report (UC-1, pre-execution), run 2: regenerated plan TASK-WF-designRev1-20261126-141220 against its design

```yaml
contract_version: 1.9.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.70
citations_total: 393
citations_revalidated: 393
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled policy, all citations re-read**
> - `citations_total: 393` = 148 file:line tokens in the findings table (23 rows re-read) and 245 inferred-requirement rows.
> - `citations_revalidated: 393`: the evidence-validator agent re-read every row; a script re-checked that each of the 245 inferred-row quotes still sits inside its cited design lines.
> - `citations_dropped: 0`. One citation was corrected (G-18: SPEC:84 added) and three were reworded (G-01, G-11, G-14); none was unfounded.

## Verdict

**The plan fixes the four defects of the first review, and it still has four Blocking findings of its own.** It keeps every outward write out of its 14 tasks. Run 1's M-01 (pytest ids) and M-02 (`make lint`) are resolved, M-03 (private detail reaching GitHub) and M-04 (runbook gating) only in part. The four now are:

1. **G-01 (Safety)** Following the runbook would stage and push the archived first plan, which names the private tooling path, with nothing that makes the push wait for the lead (`PLAN:184`).
2. **G-02 (Decision)** Task 5's three acceptance lines cannot all hold with a populated guard file and all pass with an empty one (`PLAN:85, 91, 92, 93`).
3. **G-03 (Missing)** No step re-posts the pinned links after a later push (`SPEC:284`).
4. **G-04 (Decision)** Part one runs `/sc:pr-submit --monitor 3` before recording the SHA and posting the comment, and the comment file leaves out the ledger (`PLAN:182, 184`).

Twelve Medium findings and three Notes are reported and are not repaired by workflow. `status: partial` because three HIGH-labelled invariants were carried without a second debate and the calibrator class could not be made disjoint from the reviewer classes (see Tier 2 process).

## Tier and coverage

- **Tier 2** was forced by the Step 1B.2b pre-filter (`coverage_degraded: parsed-sparse`: 0 requirement ids parsed, 245 inferred) and by rule 4 (three areas touched: tests, docs, rulesets JSON); rule 5 also holds (`S_dev_density` 0.2041 > 0.20). The blind-calibrated Tier 1 card scored 0.76. See `artifacts/tier_decision.yaml`.
- **Coverage:** `coverage_pct` (parsed only) is null; `coverage_pct_union` is 0.7959 (195 of 245 inferred requirements matched a plan task by word containment; run 1 scored 0.7108). The Tier 1 analyst sorted the 50 unmapped rows into 33 covered elsewhere in different words, 16 out of the plan by design and 1 real gap (INF-237, the re-pin: G-03).
- **Best-practice grade:** not scored (`best_practice_grade: null`). The protocol gives no scale for it in UC-1 and none was invented.

## Prior blocking findings of run 1

| id | status |
|---|---|
| M-01 wrong pytest ids | Resolved (`PLAN:74`) |
| M-02 lost `make lint` | Resolved (`PLAN:75, 184, 201, 207`) |
| M-03 private detail reaches GitHub | Open in part: G-01, G-02, and the weaker G-07, G-10, G-11 |
| M-04 runbook part one gated | Partly fixed: G-03 and G-04 remain |

## Findings

Source: the merged verdict of the adversarial debate (`adversarial/merged-output.md`, base card V3). Grades follow the review severity rule, not the reviewers' labels or the calibrators' opinions.

Grades follow the rule in the run brief (Blocking, Medium, Note). "Sources" names the card finding, the Tier 1 id (context) or the debate point each row comes from. Every plan, spec, test, archive and gitignore line cited was re-read by at least one advocate and by the orchestrator unless stated.

| id | grade | claim | plan cite | spec cite | evidence | sources | verified |
|---|---|---|---|---|---|---|---|
| G-01 | Blocking (Safety) | Following PLAN:184 publishes the private tooling path. The runbook stages `.dev/tasks` (always staged, `.gitignore:83`), which holds the archived first plan. ARCH:82 gives the private tooling path and function names; ARCH:88 gives the file name. The guard excludes that one folder; the runbook lists it only as "an open item for the lead"; no sentence makes staging, commit or push wait for the lead's answer. Affected action: commit and push to the public `origin`. | PLAN:15, 22, 184 | SPEC:270, 274 | ARCH:82, 88 (shape checked by a masked command; names not copied). The archive folder is untracked (session `git status`). SPEC:270 lists "the archived superseded plan" among the places the ban covers; SPEC:274 permits the guard exclusion, not the publication; a stop before staging satisfies both. The Safety clause is not lowered because the spec permits the exclusion, nor because a stop is a cheap fix. | R2-1, R3-1; T1 F1; V1 treated it as inherited and conceded in round 2 (X-001); C-001 | yes (orchestrator; all three advocates re-read) |
| G-02 | Blocking (Decision) | Task 5's acceptance lines cannot all hold with a populated guard, and all pass with an empty one. PLAN:93 requires the audit's last section to list every command run, which includes the private contents read, whose path holds the folder and file names that PLAN:85 puts in `guard-patterns.txt`; so PLAN:91 (`grep -c -f` prints 0) fails. The three lines hold together only if the guard lacks those names (PLAN:92 requires only that the file "exists", and `grep -c -f` on an empty file prints 0) or the command list omits the read. A guard that passes empty protects nothing at PLAN:184 and PLAN:208. | PLAN:85, 91, 92, 93, 184, 208 | SPEC:272, 274 | PLAN lines re-read by all four; the plan never says to redact the path in the command list; M-03's repair (SPEC:274) rests on the guard. Not graded Safety: no sentence of the plan tells the executor to write an empty guard. | R1-1, R3-2 (conflict); R1-2 (empty or partial); C-002, C-003 | yes |
| G-03 | Blocking (Missing) | No step re-pins the posted links after a later push. SPEC:284 (M-10): "After any later push, the pinned links are re-pinned in a new comment (R6)". PLAN:184 replaces the placeholder once; PLAN:186 imports R0 to R7 "as in section 3.6", and R6 (SPEC:144) is only a `git diff` and a `PUT` for applied files, which runs in part two for `APPLY` rows. The expected run applies nothing (SPEC:239), so a re-pin put into R6 would never run. `/sc:pr-submit --monitor 3` pushes fixes (`~/.claude/commands/sc/pr-submit.md:38`). The comment also inlines commands copied from the guide (PLAN:169), so the repair must refresh the whole posted text, not only the links. PLAN:189-193 pass without it. | PLAN:169, 184, 186, 189-193 | SPEC:144, 239, 264, 284 | grep of PLAN for re-pin, repin, later push, new comment, pinned: 0 hits (orchestrator). The spec's own Medium label for M-10 is information only (run brief); that an old link still resolves is harm, not the test of the rule. | R2-2, R3-3; T1 F5; probe INV-002; C-004 | yes |
| G-04 | Blocking (Decision) | Part one runs in the wrong order and posts the wrong file. PLAN:184 lists the commit and push, then `/sc:pr-submit --monitor 3`, then recording the pushed SHA, then posting the comment. PLAN:182 promises that part one "runs right after the commit and push"; SPEC:151 ("posted right after the push"), SPEC:163 (push, record SHA, post), SPEC:164 (step 10 is `/sc:pr-submit`) and SPEC:275 (part one lists no pull-request step) put the post first. The monitor loop can push fixes (`pr-submit.md:38`), so the SHA would be recorded after them, and a monitor that halts leaves the handoff unposted. PLAN:184 also defines the comment file as "a copy of the handoff text" while the same sentence says the draft ledger is posted, so the ledger is not in the file. PLAN:201 asks the pull request body to say where the comment is, which needs the comment to exist first. PLAN:189 passes in either order. | PLAN:182, 184, 189, 201 | SPEC:151, 163-164, 275 | Clause order re-read by all four. All three advocates graded Blocking after round 2 (V3 conceded its Medium; V1 65%, V2 99%, V3 75%). | R2-3, R3-7; T1 F4; probe INV-006; C-005 | yes |
| G-05 | Medium | The PLAN:92 acceptance "`git status --short .dev/issues/837` is the only place they show" cannot tell the files apart. The folder `.dev/issues/837/` is untracked as a whole, so git prints one `?? .dev/issues/837/` line whether or not `private/` is ignored. `.gitignore:162` (`private/`) ignores the private files; `git check-ignore -v` is the check that proves it. The files stay unstaged anyway because the staging list excludes `.dev/issues/` (PLAN:184). | PLAN:92 | SPEC:271 | The orchestrator ran both commands: `git status --short .dev/issues/837` printed `?? .dev/issues/837/`; `git check-ignore -v .dev/issues/837/private/x.md` printed `.gitignore:162:private/`. | R1-3, R3-5; T1 F8; C-006 | yes (orchestrator) |
| G-06 | Medium | PLAN:85 says to redirect the decoded private text "to a file or a shell variable" and names no file. A file in `/tmp` is outside the worktree (PLAN:19 "only writes files in this worktree") and leaves the decoded text on disk; a shell variable does not survive separate Bash calls; a file in the package would be staged. The destination `private/` is named only for "what matched". | PLAN:19, 85 | SPEC:272 | Wording re-read. The guard would catch a staged path only if its patterns are complete (G-02). | R1-4; T1 F6; probe INV-009; C-007 | yes (wording); the leftover file is [INFERRED] |
| G-07 | Medium | No guard grep covers the text that is posted. PLAN:184's guard scans staged files only. The comment file (PLAN:184), `gates.md` (Task 11, PLAN:156-163; its acceptance has no privacy line), `handoff-ryan.md` (Task 12, PLAN:175, prose only) and the runbook (Task 13, PLAN:193, prose only) get no `grep -c -F -f` that prints 0, though Tasks 5 and 14 have one (PLAN:91, 208). Also unguarded: the commit message, the pull request title and every reply or fix the monitor posts. SPEC:270 bans private detail in "every issue comment". | PLAN:91, 156-163, 175, 184, 193, 208 | SPEC:270, 274 | SPEC:274 asks for the guard on staged files only and the prose bans stand (PLAN:22, 156, 175), so exposure needs an upstream error. | R3-6; T1 F3; probe INV-007; C-008 | yes |
| G-08 | Medium | Ledger wording. PLAN:156 and PLAN:161 name "the first failing gate", but PLAN:156 also assigns G6 to coder_orca's tag ruleset while G3 (the installations read) fails first for every Clay row. The rule is `SKIP(<first failing gate>)` (SPEC:116, 280); SPEC:236 gives `SKIP(G6)` for the same row beside `SKIP(G3)`. Every outcome is SKIP. | PLAN:156, 161 | SPEC:116, 122, 125, 236, 280 | A reading that keeps both exists (G3 concerns the target ref's events, SPEC:122; G6 governs the tag row); inherited from SPEC:236; not forced. Advocate split: V2 Blocking (85%), V1 and V3 Medium; adjudicated Medium. | R3-8; T1 F7; C-009 | yes |
| G-09 | Medium | The short audit-result tables of SPEC:152 reach neither destination for the three Clay repos. The issue comment carries the handoff, whose audits cover Ryan's three repos only (PLAN:169), and the draft ledger (PLAN:184); the pull request body row is a per-repo summary of ledger rows (PLAN:201), which is what SPEC:290 sets. | PLAN:169, 184, 201, 206 | SPEC:152, 163, 275, 290 | Revision 1 wins where it differs from SPEC:152: SPEC:275 and SPEC:290 define the payloads and PLAN matches them; the ledger's decision and first failing gate carry the audit outcome. Advocate split 2 to 1 (V2 and V3 Blocking, V3 at 60%; V1 Medium); adjudicated Medium. | R2-4 (narrowed; the PR-body half was conceded by V2); C-010 | yes |
| G-10 | Medium | PLAN:21 says the package `artifacts/` folder holds only the grounding note, but `/sc:implement` writes reviews, logs and retry prompts there. They are staged (`.gitignore:83-85`) and nothing keeps Task 5's private names out of them. The finished package `.dev/tasks/done/TASK-WF-issueSummary-20261126-044758/artifacts/` holds `T*-review.md`, `FINAL-review.md`, `T*-*.log` and `retries/T1`, `retries/T2`. | PLAN:21, 184 | SPEC:270 | The orchestrator listed the folder. That Task 5's review would quote the names is [INFERRED]; a filled guard would stop the staging, but the runbook gives no way to fix and continue. | R3-4; C-011 | yes (files); inferred (quote) |
| G-11 | Medium | The guard mechanics are weak. PLAN:184 uses `grep -n -f` and PLAN:85 says "fixed strings", but no `-F`: a `.` matches any character and a blank line in the pattern file matches every line; `-n` prints the matched private line into the session; the exit codes (2 for an unreadable file) and an empty file set are not handled. Two of the E-2 function names are ordinary English words and they occur in the executor's own files: 3 of 23 files in one finished package and 9 of 27 in another (retry prompts and the return contract). "Any hit stops the staging" and the plan has no rule for what follows a hit. | PLAN:85, 184, 208 | SPEC:274 | Counts by the orchestrator (names not printed); the retry file layout at `~/.claude/skills/sc-implement-protocol/refs/retry.md:23` (a file-name pattern that carries one of those words) per the probe. V3 graded this Blocking (N-1, 75%) and the probe HIGH; adjudicated Medium: the stop is the spec's rule, it exposes nothing, and the fix changes how strings are matched, not a named decision. | R1-6, R3-9; T1 F9; V3 N-1; probe INV-001, INV-005 | yes |
| G-12 | Medium | Task 3 gives no acceptance for two items of the guide's "Before applying" and "Check" rows: the producer search checklist (SPEC:87) and the tag ruleset check (SPEC:89). PLAN:58 sends the executor to the sub-sections of 3.3 by reference; PLAN:61-65 check neither. | PLAN:58, 61-65 | SPEC:87, 89 | Both texts read. No later step depends on them. | R1-5; C-012 | yes |
| G-13 | Medium | The pre-commit checks and the guard run on an unspecified file set. `git diff --stat` and `git status` ("nothing under `.claude/` or `.dev/issues/` staged") are listed before the staging list is applied, when every new file is untracked; they show only the two tracked files and pass whatever the folders hold; `git status` prints an untracked folder as one line; no step enumerates the files to be staged (`git add -n`, `git diff --cached --name-only`). | PLAN:184 | SPEC:226 | Clause order in PLAN:184; `git status` shows `??` for the new folders. No reviewer card raised it. | T1 F2; probe INV-004 | yes |
| G-14 | Medium | No fetch or rebase check before the push. `CLAUDE.md:73` (pre-PR check 2) requires `git fetch origin && git log HEAD..origin/integration` and a rebase before pushing when `origin/integration` has commits the branch lacks; PLAN:184 says "the commit and push" with no remote, branch or check, and the monitor does not rebase or force-push (`pr-submit.md` "Will Not"), so a late rebase would invalidate the recorded SHA and the posted pins. | PLAN:184 | SPEC:163 | `CLAUDE.md:73` and the pr-submit "Will Not" paragraph read. A project rule, not a requirement of the spec; probe label HIGH, graded Medium. | probe INV-003 | yes |
| G-15 | Medium [INFERRED] | The code searches of Tasks 6 and 7 (`org:IronbellyOrg`) can return paths from other private repositories; Task 6 records "the hit" (PLAN:103); the neutral sentence and the guard patterns cover only coder_orca (PLAN:22, 85), so such a path could reach a ledger reason or the posted text. | PLAN:22, 85, 99, 103, 111 | SPEC:270 | Not shown to carry hit text today. | probe INV-008 | partly |
| G-16 | Medium | R1's scratch pushes run from "the scratch clone" (PLAN:186) with an explicit URL and the clone's location is unnamed; SPEC:139 uses `git push --force origin HEAD~1:zz-ruleset-selftest`. With a wrong working directory the push would send IronClaude's own commit into the target repository. Part two is gated, so this acts outside scope only on a mistake. | PLAN:186 | SPEC:139, 188 | PLAN:186 and SPEC:139 read. | probe INV-010 | yes |
| G-17 | Note | Task 7 says "the same blocks as Task 6" but depends only on Task 5 (PLAN:109, 111); Task 13 posts the Task 12 file but depends only on Task 11 (PLAN:180, 184). No effect: `/sc:implement` runs in source order unless a set is marked independent (`~/.claude/skills/sc-implement-protocol/SKILL.md:110`), and neither task reads the other's output. | PLAN:109-111, 180, 184 | SPEC:169 | SKILL.md:110 read by the orchestrator (A-004 settled). | R3-10; T1 F11; C-013 | yes |
| G-18 | Note | The `_TARGETS` tag entry for the three Ryan repos is not given: PLAN:58 says "conditional" and "in Ryan's handoff", PLAN:71 lists `conditional`, `skip` or `handoff`. SPEC:70 lists the vocabulary (`conditional`, `skip`, `handoff`) and maps none of it to repos; SPEC:84 gives the tag column "apply, skip, handoff", so `handoff` is the likely value. | PLAN:58, 71 | SPEC:70, 84 | Wording. | R1-7; C-014 | yes |
| G-19 | Note | `SKIP(not settled)` (PLAN:156, from SPEC:279) is outside the decision set that PLAN:156 itself states (`APPLY`, `SKIP(<first failing gate>)`, `HANDOFF`; SPEC:280). | PLAN:156 | SPEC:279, 280 | Wording; the spec has the same mix. | T1 calibration (missed minor) | yes |

### Grading notes

- Re-graded from the cards: V2's R2-3, R2-2 and R2-4 carry the label Blocking with severity MEDIUM in its own table (X-003); the rule decides: R2-2 and R2-3 stay Blocking (G-03, G-04), R2-4 becomes Medium (G-09). V3's R3-1 and R3-3 (calibrators: "too high") stay Blocking: the Safety clause is not lowered by the spec's permission, and M-10 is a required step although the spec labels it Medium. V3's R3-7 (Medium) is raised to Blocking (G-04). V1's R1-2 (Blocking, Missing) is merged with R1-1 and R3-2 into G-02 (Decision).
- Dropped after the debate (no finding): R1-8 and C-015 (naming `IronbellyOrg/Coder` is allowed; SPEC:272 forbids only the tooling's file, folder and function names); R2-5 and C-016 (a flaw in the coverage matrix, not in the plan: PLAN:58 and PLAN:99 carry the `START` filter); V2's PR-body half of R2-4 (PLAN:201 meets SPEC:290).
- Citation corrections made before the rows were written: R1's SPEC:391, 396, 404-405, 113 and ~108 do not exist (the spec has 291 lines; real lines SPEC:52-58, 60, 68-69, 87-89, 70); R1's `branch-protection.md:76-77` does not exist (the guide has 67 lines; the strings are at TEST:73-77); R1's "lines 368-372 of the hunk" is `.github/rulesets/protect-master.json:15-19`; R1-8's rule is SPEC:272, not SPEC:270; V1's PLAN:18 in R1-4 is PLAN:19; V2's matrix lines C:1531-1539 end near 1541; T1's M-16 is PLAN:206 (not 205) and T1 F3's "no private detail" wording is PLAN:156 (not 163). All other cited lines were re-read and hold.

Dropped after the debate (not findings): R1-8 and C-015 (naming `IronbellyOrg/Coder` is allowed), R2-5 and C-016 (a flaw of the coverage matrix, not of the plan), the pull-request-body half of R2-4 (met by `PLAN:201`).

## Inferred requirements (Pass 2)

245 rows were extracted from `source.md` by an agent in pass 2 (parsed pass 1 found none). Each row's quote was re-checked by script at Wave 5 against its cited lines: 245 survive, 0 dropped. Match results are by word containment (a row is matched when at least 60 percent of its quote's words appear in one task).

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Phase 1 (files, test, guide, read-only audits, drafts) is what `/sc:implement` executes. | source.md:14-14 | unmapped (best Task 13, containment 0.5) |
| INF-002 | Phase 3 (applying rulesets to GitHub) runs after the pull request monitor settles, from a runbook, not as a plan step. | source.md:14-14 | matched Task 13 (containment 0.769) |
| INF-003 | No script and no render tool. Audits and applies are documented `gh api` commands with variables; results go into per-repo records. | source.md:15-15 | unmapped (best Task 8, containment 0.429) |
| INF-004 | Every possible write has an explicit gate decision, recorded in a ledger: `APPLY`, `SKIP(reason)` or `HANDOFF`. Nothing is applied by default. | source.md:16-16 | unmapped (best Task 11, containment 0.571) |
| INF-005 | Where a decision is missing, the design picks the safe default and says so: the fork branch rulesets and `aidev02` are skipped, and a check that could not run blocks the repo it covers. | source.md:17-17 | unmapped (best Task 3, containment 0.471) |
| INF-006 | The two Ryan-only outputs (handoff text, ruleset ids) are posted to issue 837 and the pull request body, never left only in `.dev/issues/`. | source.md:18-18 | matched Task 13 (containment 0.706) |
| INF-007 | The pull request says `Refs #837`, and issue 837 stays open until Ryan reports. | source.md:19-19 | matched Task 14 (containment 1.0) |
| INF-008 | IronClaude's three JSON files and the live IronClaude rulesets are not touched. | source.md:20-20 | matched Task 3 (containment 0.714) |
| INF-009 | In the guide only the "Tests" paragraph is edited (it must name the new files); every other existing section stays. | source.md:20-20 | matched Task 3 (containment 0.818) |
| INF-010 | In the test, every existing assertion stays and one glob becomes recursive; everything else is added beside them. | source.md:20-20 | unmapped (best Task 4, containment 0.333) |
| INF-011 | State that moves between phases lives in four files under `.dev/issues/837/` (never staged; their content is copied to GitHub, section 3.7): `audit/<repo>.md`, `gates.md`, `handoff-ryan.md`, `apply-runbook.md`. | source.md:44-44 | matched Task 13 (containment 0.625) |
| INF-012 | New folder `.github/rulesets/other-repos/`. The three existing files in `.github/rulesets/` are not changed. | source.md:50-50 | matched Task 13 (containment 0.9) |
| INF-013 | Formatting follows `protect-master.json` (two-space indent, one-line `ref_name` and `bypass_actors`). | source.md:50-50 | matched Task 1 (containment 0.917) |
| INF-014 | `name` becomes `protect-main`; `conditions.ref_name.include` becomes `["refs/heads/main"]`; nothing else changes | source.md:54-54 | matched Task 1 (containment 1.0) |
| INF-015 | `deletion`, `non_fast_forward`, `pull_request` | source.md:54-54 | matched Task 1 (containment 1.0) |
| INF-016 | as `protect-main.json`, then `name` becomes `protect-main-mirror` and the `pull_request` rule object is removed | source.md:55-55 | matched Task 2 (containment 0.9) |
| INF-017 | `deletion`, `non_fast_forward` | source.md:55-55 | matched Task 1 (containment 1.0) |
| INF-018 | only if Clay's written yes for `aidev02` is quoted in `issue-summary.md` | source.md:56-56 | matched Task 11 (containment 1.0) |
| INF-019 | `name` becomes `protect-aidev02`; `include` becomes `["refs/heads/aidev02"]` | source.md:56-56 | matched Task 1 (containment 0.857) |
| INF-020 | Unchanged in all three: `target: branch`, `enforcement: active`, `exclude: []`, `bypass_actors` = the repository admin role (`actor_id` 5, `RepositoryRole`, `bypass_mode: pull_request`), and the five `pull_request` parameters with `required_approving_review_count: 0`. | source.md:58-58 | matched Task 1 (containment 0.889) |
| INF-021 | The tag file `protect-release-tags.json` is applied as it is (name `protect-release-tags`, `refs/tags/v*`, `deletion`, `non_fast_forward`, `update`, no bypass). | source.md:58-58 | matched Task 1 (containment 0.692) |
| INF-022 | The scratch self-test (3.6, R1) creates a copy of the mirror file through `POST`, so it answers this before any real create; if the API refuses it, the mirror file drops the bypass actor and the test, guide and D4 are updated together before anything is applied. | source.md:60-60 | matched Task 13 (containment 0.6) |
| INF-023 | Every existing assertion stays, including the literal guide strings of `test_guide_has_apply_and_check_commands`. | source.md:64-64 | matched Task 3 (containment 0.625) |
| INF-024 | `_RULESETS.glob("*.json")` becomes `_RULESETS.rglob("*.json")` so `other-repos/` is covered | source.md:68-68 | matched Task 4 (containment 0.75) |
| INF-025 | `_RULESETS / "other-repos"`; a loader `_load_other(name)` reads from it (the existing `_load` reads only the root folder and stays as it is). | source.md:69-69 | matched Task 4 (containment 0.833) |
| INF-026 | The target table: for each of the six repos, its applier (`clay` or `ryan`), the candidate branch files, and the tag entry (`conditional`, `skip` or `handoff`). | source.md:70-70 | matched Task 4 (containment 0.933) |
| INF-027 | A fork lists both `protect-main` and `protect-main-mirror`, because the role is chosen on apply day (D7). | source.md:70-70 | matched Task 3 (containment 0.727) |
| INF-028 | `protect-aidev02` is listed for IronOrca and marked optional. | source.md:70-70 | matched Task 4 (containment 1.0) |
| INF-029 | `protect-main` (and `protect-aidev02` if the file exists) equals `protect-master` after replacing only `name` and `ref_name.include`; rule types are `deletion`, `non_fast_forward`, `pull_request`; bypass is the admin `pull_request` actor; zero approvals. | source.md:71-71 | matched Task 4 (containment 1.0) |
| INF-030 | `protect-main-mirror` equals `protect-main` after replacing `name` and removing the `pull_request` rule; rule types are `deletion` and `non_fast_forward`; same bypass. | source.md:72-72 | matched Task 4 (containment 1.0) |
| INF-031 | The mirror has its own expected list and does not join the three-type check. | source.md:72-72 | matched Task 11 (containment 0.714) |
| INF-032 | The set of `*.json` in `other-repos/` equals the set of files named in `_TARGETS`, except that a file marked optional may be absent. A missing, unused or unlisted file fails. | source.md:73-73 | matched Task 4 (containment 0.941) |
| INF-033 | The guide contains the heading "Other IronbellyOrg repos", every repo name in `_TARGETS`, every `other-repos/` file path, `$REPO`, `$BRANCH`, `admin:org`, `ahead_by` and `zz-selftest-`. | source.md:74-74 | matched Task 4 (containment 1.0) |
| INF-034 | Run: `uv run pytest tests/docs/test_branch_protection_rulesets.py -v`. | source.md:76-76 | matched Task 4 (containment 1.0) |
| INF-035 | The codegraph shows no other indexed file depends on this test; that is a lead only, so the full suite is still run before the commit (`uv run pytest tests/docs -q`). | source.md:76-76 | matched Task 4 (containment 0.765) |
| INF-036 | Add one H2, "Other IronbellyOrg repos", after "Break glass" and before "Tests". | source.md:80-80 | matched Task 3 (containment 1.0) |
| INF-037 | Edit one sentence of "Tests" so it also names the new files. | source.md:80-80 | matched Task 3 (containment 1.0) |
| INF-038 | All IronClaude sections and commands stay (the existing test pins them). | source.md:80-80 | matched Task 3 (containment 0.625) |
| INF-039 | The new section is written with variables, never with a repo name in a command: | source.md:80-80 | matched Task 3 (containment 1.0) |
| INF-040 | The target table: repo, applier, role (full, or "mirror when the fork test gives 0"), tag ruleset (apply, skip, handoff), excluded branches (`dev`, `release/v*`, `dot/*`). | source.md:84-84 | matched Task 3 (containment 0.9) |
| INF-041 | For each fork an Owner column holding the standing rule "switch to `protect-main.json` when `ahead_by` is above 0" and the named person. | source.md:84-84 | matched Task 3 (containment 0.857) |
| INF-042 | `REPO`, `BRANCH`, `PARENT_OWNER`, `ID`, `END`, `START`. | source.md:85-85 | matched Task 3 (containment 1.0) |
| INF-043 | The `compare` command that prints `ahead_by` and the rule that follows from it (D7). | source.md:86-86 | unmapped (best Task 3, containment 0.571) |
| INF-044 | Preflight (login, admin, default branch), hooks and keys counts, `branches/main/protection` (404 expected), existing ruleset list (expected empty), the 90-day audit command, the producer search checklist, and the note that the organisation installations command needs the `admin:org` scope. | source.md:87-87 | matched Task 3 (containment 0.833) |
| INF-045 | Create only if the name is absent; tags first, then non-default branches, then `main`. | source.md:88-88 | matched Task 3 (containment 1.0) |
| INF-046 | Rule types per branch, the full read-back of each ruleset, the tag ruleset check. | source.md:89-89 | matched Task 3 (containment 0.889) |
| INF-047 | The scratch ruleset on a throwaway branch (3.6, R1). | source.md:90-90 | matched Task 13 (containment 0.8) |
| INF-048 | The same commands as the IronClaude section with `$REPO` and `$ID`. | source.md:91-91 | matched Task 3 (containment 1.0) |
| INF-049 | The guide holds no dated audit numbers; those live in the audit records and the pull request body. | source.md:93-93 | matched Task 3 (containment 0.6) |
| INF-050 | One file per repo, `.dev/issues/837/audit/<repo>.md`, six in total. | source.md:97-97 | matched Task 14 (containment 0.9) |
| INF-051 | Phase 1 writes all six, read-only (Clay's read access is enough for the activity endpoint, P-3). | source.md:97-97 | unmapped (best Task 5, containment 0.333) |
| INF-052 | `END=$(date -u +%Y-%m-%dT%H:%M:%SZ)` and `START=$(date -u -d "$END - 90 days" +%Y-%m-%dT%H:%M:%SZ)`; both written down. | source.md:101-101 | matched Task 5 (containment 1.0) |
| INF-053 | `gh api user --jq .login` prints `clayphi`; | source.md:102-102 | matched Task 5 (containment 1.0) |
| INF-054 | `gh api repos/IronbellyOrg/$REPO/hooks --jq length`, `.../keys --jq length`, `.../branches/main/protection` (404 expected) | source.md:103-103 | matched Task 8 (containment 0.786) |
| INF-055 | `gh api --paginate orgs/IronbellyOrg/installations` (expected to fail: no `admin:org`; written as "could not run" with the error text). | source.md:103-103 | matched Task 5 (containment 0.786) |
| INF-056 | `gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[] \\| [.id,.name,.enforcement] \\| @tsv'`; empty expected. | source.md:104-104 | matched Task 3 (containment 0.692) |
| INF-057 | `gh api repos/IronbellyOrg/$REPO/git/ref/heads/$BRANCH --jq .object.sha` for `main` and any other audited branch. | source.md:105-105 | matched Task 6 (containment 0.733) |
| INF-058 | `gh api repos/IronbellyOrg/$REPO --jq .parent.full_name`, then `gh api "repos/IronbellyOrg/$REPO/compare/$PARENT_OWNER:main...main" --jq '[.ahead_by,.behind_by] \\| @tsv'`. | source.md:106-106 | matched Task 8 (containment 1.0) |
| INF-059 | `gh api --paginate "repos/IronbellyOrg/$REPO/activity?ref=refs/heads/$BRANCH&time_period=year&per_page=100" --jq | source.md:107-107 | matched Task 5 (containment 0.688) |
| INF-060 | Each kept row is classified: `direct push by human`, `direct push by automation`, `sync` (a parent fast-forward on a fork `main`), `pr_merge`, `branch_creation`. | source.md:107-107 | matched Task 5 (containment 0.8) |
| INF-061 | `time_period=quarter` is not used (its length is UNVERIFIED). | source.md:107-107 | unmapped (best Task 2, containment 0.2) |
| INF-062 | Issue 702's `git log` cross-check is not used on forks (it counts upstream history). | source.md:107-107 | unmapped (best Task 3, containment 0.273) |
| INF-063 | Number of `v*` refs (`gh api repos/IronbellyOrg/$REPO/git/matching-refs/tags/v --jq length`); the statement that the activity endpoint shows no tag events (so tag writes are invisible to this audit, INV-009); | source.md:108-108 | matched Task 5 (containment 0.739) |
| INF-064 | for a repo that has a parent, a check of each recent `v*` tag target against the parent's tag of the same name. | source.md:108-108 | matched Task 6 (containment 0.875) |
| INF-065 | A table "place, hit, how resolved" covering: every workflow of the repo (list them with `gh api repos/IronbellyOrg/$REPO/contents/.github/workflows`, read each; follow called scripts); | source.md:109-109 | matched Task 6 (containment 0.75) |
| INF-066 | every IronbellyOrg repo that holds a release token for the target (E-2: `IronbellyOrg/Coder` for coder_orca); the way tags arrive from the parent. | source.md:109-109 | unmapped (best Task 3, containment 0.5) |
| INF-067 | Search terms: `git push`, `git tag -d`, `push --delete`, `git/refs`, `gh release delete`, `--force`. | source.md:109-109 | matched Task 6 (containment 0.9) |
| INF-068 | A hit is resolved by reading it, never by absence of grep output (names built at run time defeat grep, E-2). | source.md:109-109 | unmapped (best Task 5, containment 0.5) |
| INF-069 | A table "ruleset, missing check or event, who clears it, what clears it". The installations read always appears here for the three Clay repos. | source.md:110-110 | unmapped (best Task 3, containment 0.571) |
| INF-070 | `CLEAR` or `BLOCKED` with the reasons. | source.md:111-111 | matched Task 5 (containment 0.667) |
| INF-071 | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` for each ruleset that may be created, written before the first write on that repo, with the id column empty until apply. | source.md:112-112 | matched Task 3 (containment 0.842) |
| INF-072 | One file, `.dev/issues/837/gates.md`: one row per (repo, ruleset) and one decision per row, `APPLY`, `SKIP(<first failing gate>)` or `HANDOFF`. | source.md:116-116 | matched Task 11 (containment 1.0) |
| INF-073 | The ruleset is applied only when every gate G1 to G9 passes for it. | source.md:116-116 | matched Task 11 (containment 0.667) |
| INF-074 | Phase 1 writes the draft with everything that can be decided read-only; Phase 3 re-evaluates G2 to G9 inside the hour before the first write. | source.md:116-116 | unmapped (best Task 11, containment 0.467) |
| INF-075 | The repo is CPA-Manager-Plus, IronOrca or coder_orca, and Clay's recorded answer (a go on those three, quoted in `issue-summary.md`) is present. | source.md:120-120 | matched Task 11 (containment 0.875) |
| INF-076 | The three Ryan repos are always `HANDOFF`: no write of any kind. | source.md:120-120 | matched Task 11 (containment 0.714) |
| INF-077 | Login is `clayphi`, `admin` is `true`, default branch is `main`, repo is not archived and is public. | source.md:121-121 | matched Task 5 (containment 0.6) |
| INF-078 | `SKIP`; stop that repo. | source.md:121-121 | matched Task 4 (containment 0.667) |
| INF-079 | The audit record's result is `CLEAR` for the target ref: no automation pushes straight to it, every event is classified, and every check that could not run is cleared (an org owner's output of the installations read, or Clay's written acceptance quoted in `issue-summary.md`). | source.md:122-122 | unmapped (best Task 5, containment 0.538) |
| INF-080 | `SKIP`; the block names who clears it. | source.md:122-122 | matched Task 5 (containment 1.0) |
| INF-081 | A non-fork gets `protect-main`. A fork gets `protect-main-mirror` when `ahead_by` is 0 **and** Clay's written acceptance of the mirror's direct-push exposure is quoted in `issue-summary.md`; it gets `protect-main` when `ahead_by` is above 0. | source.md:123-123 | matched Task 3 (containment 0.667) |
| INF-082 | With no acceptance, the fork's branch ruleset is skipped and reported (the fallback of D7). | source.md:123-123 | matched Task 3 (containment 0.625) |
| INF-083 | Clay's written yes is quoted in `issue-summary.md` and `protect-aidev02.json` exists. | source.md:124-124 | matched Task 11 (containment 0.818) |
| INF-084 | `SKIP`; the file is not created. | source.md:124-124 | matched Task 4 (containment 0.667) |
| INF-085 | The producer search of the audit record is `CLEAR` and the repo is not coder_orca. | source.md:125-125 | matched Task 5 (containment 1.0) |
| INF-086 | `SKIP` the tag ruleset (coder_orca always: E-2). | source.md:125-125 | matched Task 5 (containment 0.8) |
| INF-087 | The list is empty at the moment of the snapshot. | source.md:126-126 | unmapped (best Task 5, containment 0.5) |
| INF-088 | `SKIP`; nothing pre-existing is updated or deleted. | source.md:126-126 | unmapped (best Task 5, containment 0.5) |
| INF-089 | The files to apply are at a commit SHA that is pushed to `origin` and equals the branch head; the files have no uncommitted change. | source.md:127-127 | matched Task 13 (containment 0.727) |
| INF-090 | `SKIP` until it holds. | source.md:127-127 | unmapped (best Task 3, containment 0.333) |
| INF-091 | The scratch self-test (3.6, R1) passed for the role about to be applied, and the API accepted the scratch copy. | source.md:128-128 | matched Task 3 (containment 0.6) |
| INF-092 | `SKIP`; stop that repo. | source.md:128-128 | matched Task 4 (containment 0.667) |
| INF-093 | The ledger header also records two statements that are not gates but must be quoted before the issue is treated as done: Clay's written acceptance of the restated done condition (section "Done condition for this pull request" of the merged requirements), and `ironbelly`'s written confirmation of admin on the repo (the revert owner, D7 and Rollback). | source.md:130-130 | matched Task 11 (containment 0.655) |
| INF-094 | Phase 1 writes it as `.dev/issues/837/apply-runbook.md` (the commands above with the variables filled in per repo, plus this order). | source.md:134-134 | matched Task 3 (containment 0.667) |
| INF-095 | Phase 3 follows it per repo, one repo at a time; a stop on one repo does not stop the others. | source.md:134-134 | unmapped (best Task 11, containment 0.571) |
| INF-096 | Re-run the audit and the fork test inside the hour; refresh `END`, tips and `ahead_by`; re-evaluate G2 to G9. | source.md:138-138 | unmapped (best Task 3, containment 0.429) |
| INF-097 | Scratch self-test for each role the ledger says `APPLY`, before the snapshot. | source.md:139-139 | matched Task 11 (containment 0.778) |
| INF-098 | In a scratch clone of the target repo (never IronClaude): create and push the throwaway branch `zz-ruleset-selftest` with two commits; | source.md:139-139 | matched Task 3 (containment 0.6) |
| INF-099 | create the scratch ruleset `zz-selftest-<role>` from the role file with `jq '.name="zz-selftest-<role>" \\| .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' <file> \\| gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -`; | source.md:139-139 | matched Task 3 (containment 0.696) |
| INF-100 | push an empty commit (full role: must be refused with GH013) or `git push --force origin HEAD~1:zz-ruleset-selftest` (mirror: must be refused); | source.md:139-139 | unmapped (best Task 13, containment 0.467) |
| INF-101 | delete the scratch ruleset by id, then the branch (`git push origin --delete zz-ruleset-selftest`); confirm `gh api repos/IronbellyOrg/$REPO/rulesets --jq '.[].name'` shows no name starting `zz-selftest-`. | source.md:139-139 | matched Task 3 (containment 0.667) |
| INF-102 | On IronOrca first read every workflow for an unfiltered `on: push` (Actions are active there, P-6); if one exists, name the branch so it cannot match or skip that repo's self-test and record why. | source.md:139-139 | unmapped (best Task 6, containment 0.579) |
| INF-103 | Result and the API answer to the scratch `POST` (this also settles whether the mirror's bypass actor is accepted, 3.1). | source.md:139-139 | unmapped (best Task 2, containment 0.545) |
| INF-104 | Snapshot: the existing ruleset list; stop the repo if it is not empty (G7). | source.md:140-140 | matched Task 5 (containment 0.625) |
| INF-105 | Apply in order: tag ruleset (if `APPLY`), `aidev02` (if `APPLY`), `main` role. Before each: list the names; the name must be absent. | source.md:141-141 | matched Task 3 (containment 0.917) |
| INF-106 | Then `gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/<file>` from a checkout at the recorded SHA. After a timeout, list again before any retry. | source.md:141-141 | matched Task 3 (containment 0.65) |
| INF-107 | On the first 403, stop that repo and record the partial state (write permission has never been tried). | source.md:141-141 | matched Task 13 (containment 0.636) |
| INF-108 | Id, date, SHA per ruleset. | source.md:141-141 | matched Task 5 (containment 1.0) |
| INF-109 | Read back: `gh api repos/IronbellyOrg/$REPO/rules/branches/$BRANCH --jq '.[].type'`; `gh api repos/IronbellyOrg/$REPO/rulesets/$ID` compared with the file on `name`, `target`, `enforcement`, `conditions.ref_name`, the bypass actors, the rule types and the `pull_request` parameters; for the tag ruleset the rule types. | source.md:142-142 | unmapped (best Task 3, containment 0.586) |
| INF-110 | A ruleset that fails the read-back is deleted by id (this rollout created it) and the repo is reported `SKIP(read-back)`. | source.md:142-142 | unmapped (best Task 5, containment 0.545) |
| INF-111 | Record ids, dates, SHA and read-back in the audit file and the ledger; post the ledger table and ids as a comment on issue 837; add the same to the pull request body (section 3.7). | source.md:143-143 | matched Task 12 (containment 0.684) |
| INF-112 | After the pull request monitor has settled and the last push is made: for each applied file, `git diff --exit-code <SHA> -- .github/rulesets/other-repos/<file>`. | source.md:144-144 | matched Task 13 (containment 0.789) |
| INF-113 | A changed file means `gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID --input <file>` and a new SHA in the record. | source.md:144-144 | matched Task 3 (containment 0.625) |
| INF-114 | For a mirror: name the owner and date of the first Sync fork on issue 837; the status is "pending" until it is run; if it is refused, delete the new ruleset by id and report. | source.md:145-145 | unmapped (best Task 3, containment 0.526) |
| INF-115 | Per Ryan repo: the 90-day audit Clay ran read-only (command, `END`, events, classification); | source.md:151-151 | matched Task 12 (containment 0.917) |
| INF-116 | the admin-only pre-apply checks (hooks, keys, `branches/main/protection`, the installations read, classic protection, Ryan's admin role); | source.md:151-151 | matched Task 12 (containment 1.0) |
| INF-117 | the exact apply, read-back, scratch self-test, revert and break-glass commands with `$REPO` set; | source.md:151-151 | matched Task 12 (containment 1.0) |
| INF-118 | the tag ruleset where D5 allows it, with Clay's read-only workflow search; | source.md:151-151 | matched Task 8 (containment 0.875) |
| INF-119 | links to `.github/rulesets/other-repos/protect-main.json` and `protect-release-tags.json` pinned to the pushed commit SHA; | source.md:151-151 | matched Task 12 (containment 0.857) |
| INF-120 | what Ryan reports back (ruleset ids and the read-back output, as a comment on issue 837). | source.md:151-151 | matched Task 12 (containment 1.0) |
| INF-121 | The text ends with a request that the lead hand it to Ryan. | source.md:151-151 | matched Task 12 (containment 0.833) |
| INF-122 | A comment on issue 837, posted right after the push, and a pointer in the pull request body. | source.md:151-151 | matched Task 13 (containment 0.818) |
| INF-123 | The ledger table and the audit results (a short table per repo) go in the pull request body and an issue 837 comment. The full files stay local. | source.md:152-152 | matched Task 13 (containment 0.706) |
| INF-124 | Summary; the "Decided for this work" block word for word, including Clay's answer; files changed; per-repo result table (applied, skipped with reason, handed to Ryan); what is left (the three Ryan repos; the owner decisions); tests run; last line `Refs #837` (never `Fixes` or `Closes`). | source.md:153-153 | matched Task 14 (containment 0.875) |
| INF-125 | Edited after Phase 3 with `gh pr edit <number> --repo IronbellyOrg/IronClaude --body-file <file>`. | source.md:153-153 | matched Task 13 (containment 0.75) |
| INF-126 | Three lines as the story says. | source.md:154-154 | matched Task 13 (containment 1.0) |
| INF-127 | `outcome` is `partial` when any ruleset is `SKIP` or `HANDOFF`, which is the expected outcome (section 8). | source.md:154-154 | matched Task 11 (containment 0.714) |
| INF-128 | The story's steps 5 to 10 are fixed: plan, `/sc:implement`, confirm, commit and push, pull request. This design maps onto them without changing them. | source.md:158-158 | unmapped (best Task 13, containment 0.562) |
| INF-129 | T1 create `protect-main.json` and `protect-main-mirror.json` (no `protect-aidev02.json` without Clay's yes). | source.md:162-162 | matched Task 3 (containment 0.889) |
| INF-130 | T2 update the pinning test. | source.md:162-162 | unmapped (best Task 11, containment 0.5) |
| INF-131 | T3 add the guide section and edit its "Tests" paragraph. | source.md:162-162 | matched Task 3 (containment 0.857) |
| INF-132 | T4 run the six read-only audits, the fork tests and the tag evidence (3.4). | source.md:162-162 | unmapped (best Task 4, containment 0.556) |
| INF-133 | T5 run the producer search for the tag rulesets of CPA-Manager-Plus and IronOrca (coder_orca is a fixed skip, E-2) and write the "Producer search" block. | source.md:162-162 | matched Task 11 (containment 0.867) |
| INF-134 | T6 write the draft gate ledger. | source.md:162-162 | matched Task 11 (containment 0.8) |
| INF-135 | T7 write the draft handoff for Ryan. | source.md:162-162 | matched Task 11 (containment 0.8) |
| INF-136 | T8 write `apply-runbook.md`. | source.md:162-162 | matched Task 7 (containment 0.8) |
| INF-137 | T9 draft the pull request body. | source.md:162-162 | matched Task 13 (containment 0.8) |
| INF-138 | T10 run `uv run pytest tests/docs -q` and `make lint`. | source.md:162-162 | matched Task 4 (containment 0.875) |
| INF-139 | No. Read-only `gh api` GET calls only. | source.md:162-162 | matched Task 5 (containment 1.0) |
| INF-140 | Confirm the plan's progress file and run the related tests again. | source.md:163-163 | unmapped (best Task 13, containment 0.5) |
| INF-141 | Stage the changed files: `.github/rulesets/other-repos/`, `docs/developer-guide/branch-protection.md`, `tests/docs/test_branch_protection_rulesets.py`, `.dev/tasks`, and this brainstorm folder (brainstorm folders are tracked in this repo by convention); never `.claude/` or `.dev/issues/`. | source.md:163-163 | matched Task 13 (containment 0.889) |
| INF-142 | Commit on a feature branch from `integration`, push to `origin`, record the pushed SHA. | source.md:163-163 | matched Task 13 (containment 0.667) |
| INF-143 | Post the handoff and the draft ledger as a comment on issue 837 with links pinned to the SHA. | source.md:163-163 | matched Task 13 (containment 0.7) |
| INF-144 | Yes, to `origin` and issue 837 of IronClaude only. | source.md:163-163 | matched Task 3 (containment 0.6) |
| INF-145 | `/sc:pr-submit --monitor 3 --head <branch> --base integration --title "..." --body "..."`; the body is the template of 3.7, ending `Refs #837`. | source.md:164-164 | matched Task 13 (containment 0.786) |
| INF-146 | When the monitor reports every check green and every comment handled: follow `apply-runbook.md` for each Clay repo (3.6). Then edit the pull request body and comment on issue 837 with the results. | source.md:165-165 | matched Task 13 (containment 0.684) |
| INF-147 | Yes, to the three Clay repos, only for rulesets whose gates all pass. | source.md:165-165 | matched Task 11 (containment 1.0) |
| INF-148 | `/sc:workflow` should therefore plan Phase 1 in full, include the Phase 2 preparation items (the staging list, the SHA record, the issue comment), and carry Phase 3 as a final "runbook, executed by the session after the pull request monitor settles, never by `/sc:implement`" item with no executable subtasks. | source.md:167-167 | unmapped (best Task 13, containment 0.5) |
| INF-149 | T1 before T2 (the test reads the files) and before T3's table; T4 and T5 are independent of T1 to T3 and can run in parallel with them; T6 needs T4 and T5; T7 needs T4 and T6; T8 needs T6; T9 needs T6 and T7; T10 last. | source.md:169-169 | unmapped (best Task 7, containment 0.286) |
| INF-150 | Every `gh` call names the repository explicitly (`repos/IronbellyOrg/$REPO/...`, `--repo IronbellyOrg/IronClaude`); no call uses a brace placeholder or the fork-parent default, and nothing touches `SuperClaude-Org/SuperClaude_Framework`. | source.md:173-173 | matched Task 13 (containment 0.6) |
| INF-151 | **write** (Phase 3 only, and R1 scratch) | source.md:183-183 | matched Task 11 (containment 0.75) |
| INF-152 | **write** (Phase 3 R6 only) | source.md:184-184 | matched Task 11 (containment 0.667) |
| INF-153 | **write** (revert, scratch cleanup; only rulesets this rollout created) | source.md:185-185 | matched Task 13 (containment 0.714) |
| INF-154 | **write** (IronClaude only) | source.md:187-187 | matched Task 3 (containment 1.0) |
| INF-155 | **write** (R1 only) | source.md:188-188 | matched Task 13 (containment 1.0) |
| INF-156 | Phase 1 uses only the read rows. A write row appears in no Phase 1 task. | source.md:190-190 | matched Task 3 (containment 0.625) |
| INF-157 | Stop that repo, no retry, record the partial state; report the repo as not applied. Other repos continue. | source.md:196-196 | matched Task 13 (containment 0.636) |
| INF-158 | Delete any ruleset already created on that repo by id. | source.md:196-196 | matched Task 13 (containment 0.833) |
| INF-159 | Read the ruleset list before any retry; create only if the name is still absent. | source.md:197-197 | matched Task 3 (containment 0.875) |
| INF-160 | Stop that repo; update and delete nothing that pre-existed. | source.md:198-198 | matched Task 13 (containment 0.714) |
| INF-161 | Delete the ruleset this rollout created, report `SKIP(read-back)`. | source.md:199-199 | matched Task 13 (containment 0.625) |
| INF-162 | The tag ruleset has no bypass; record the state and either apply the branch ruleset on a later run or delete the tag ruleset by id, whichever the revert owner decides in writing on issue 837. | source.md:200-200 | matched Task 13 (containment 0.611) |
| INF-163 | List `zz-selftest-*` rulesets and branches; delete; the real create waits until the list is clean. | source.md:201-201 | matched Task 3 (containment 0.636) |
| INF-164 | Delete the new ruleset by id; report; the fork test and the standing switch rule are reviewed. | source.md:202-202 | matched Task 3 (containment 0.727) |
| INF-165 | `PUT` the new file; record the new SHA. | source.md:203-203 | matched Task 5 (containment 0.8) |
| INF-166 | Delete the tag ruleset by id (the break-glass sequence in the guide); report. | source.md:204-204 | matched Task 3 (containment 0.778) |
| INF-167 | `SKIP` and name who clears it; never treated as clean. | source.md:205-205 | matched Task 5 (containment 0.667) |
| INF-168 | Who reverts: the repo admin. | source.md:207-207 | matched Task 3 (containment 0.667) |
| INF-169 | `ironbelly`'s admin role on the three Clay repos is UNVERIFIED; until `ironbelly` confirms it in writing on issue 837, Clay is the revert owner and must be reachable on the day of the apply (Rollback section of the merged requirements, INV-004). | source.md:207-207 | unmapped (best Task 12, containment 0.478) |
| INF-170 | Test "files match the table"; `ls .github/rulesets/other-repos/`; no `protect-aidev02.json` unless the ledger quotes the yes. | source.md:213-213 | matched Task 3 (containment 0.688) |
| INF-171 | New derivation tests (full, mirror, optional aidev02). | source.md:214-214 | matched Task 4 (containment 0.857) |
| INF-172 | Table test; recursive `~DEFAULT_BRANCH` test; the existing literal-string test still passes. | source.md:215-215 | matched Task 5 (containment 0.625) |
| INF-173 | Guide-section test; reading the section against 3.4 to 3.6. | source.md:216-216 | matched Task 4 (containment 0.8) |
| INF-174 | Six files exist with every block filled; `END` and `START` set; tips recorded. | source.md:217-217 | matched Task 5 (containment 0.6) |
| INF-175 | Audit blocks; ledger gates G2, G3, G6, G7. | source.md:218-218 | matched Task 11 (containment 0.75) |
| INF-176 | Runbook R0 to R7; ledger row per ruleset with id, date, SHA. | source.md:219-219 | matched Task 13 (containment 0.778) |
| INF-177 | Issue 837 comment URL recorded; links contain the pushed SHA. | source.md:220-220 | matched Task 12 (containment 0.778) |
| INF-178 | The body contains the verbatim "Decided for this work" block and the ledger table. | source.md:221-221 | matched Task 14 (containment 0.875) |
| INF-179 | Body's last line; `gh pr view` shows open. | source.md:222-222 | matched Task 13 (containment 0.75) |
| INF-180 | Restated per-repo table in the body; Clay's acceptance quoted or listed as open. | source.md:223-223 | matched Task 14 (containment 0.778) |
| INF-181 | Each is a gate, a runbook step, a record block or a listed open decision; none is left only in the debate files. | source.md:224-224 | unmapped (best Task 13, containment 0.5) |
| INF-182 | Quality checks before the commit: `uv run pytest tests/docs/test_branch_protection_rulesets.py -v`, `uv run pytest tests/docs -q`, `make lint`, `git diff --stat` shows only the staged list of Phase 2, and `git status` shows nothing under `.claude/` or `.dev/issues/` staged. | source.md:226-226 | matched Task 13 (containment 0.88) |
| INF-183 | After Phase 3, for each applied ruleset: the R4 read-back output is in the audit file. | source.md:226-226 | matched Task 13 (containment 0.7) |
| INF-184 | Audit, ledger row `SKIP(G3)` for every ruleset, runbook ready. Nothing written to the repo. | source.md:234-234 | matched Task 11 (containment 0.727) |
| INF-185 | Audit, ledger `SKIP(G3)` for `protect-main`, `SKIP(G6)` for the tag ruleset. | source.md:236-236 | matched Task 11 (containment 1.0) |
| INF-186 | Handoff text and audit posted on issue 837; nothing written to the repos. | source.md:237-237 | matched Task 12 (containment 1.0) |
| INF-187 | So the expected result of this run is: the files, test and guide changed and pushed, six audit records, the ledger, the handoff posted for Ryan, the runbook ready, the pull request open with `Refs #837`, **no ruleset applied**, and `outcome: partial`. | source.md:239-239 | matched Task 13 (containment 0.615) |
| INF-188 | Clearances that unlock Phase 3, each a written statement quoted in `issue-summary.md`. | source.md:241-241 | matched Task 11 (containment 0.889) |
| INF-189 | G3 can pass on the three Clay repos; the rulesets that pass the other gates are applied. | source.md:245-245 | matched Task 11 (containment 0.778) |
| INF-190 | Every ruleset on the three Clay repos stays `SKIP(G3)`. | source.md:245-245 | matched Task 11 (containment 0.857) |
| INF-191 | G4 passes for the forks and the mirror is applied when `ahead_by` is 0. | source.md:246-246 | matched Task 3 (containment 0.667) |
| INF-192 | The forks' branch rulesets stay skipped and reported; the tag rulesets are decided separately. | source.md:246-246 | unmapped (best Task 3, containment 0.556) |
| INF-193 | `protect-aidev02.json` is created and may be applied. | source.md:247-247 | matched Task 3 (containment 0.8) |
| INF-194 | The file does not exist. | source.md:247-247 | matched Task 4 (containment 1.0) |
| INF-195 | `ironbelly` is a named revert owner. | source.md:248-248 | unmapped (best Task 3, containment 0.5) |
| INF-196 | Clay is the only revert owner and must be reachable. | source.md:248-248 | unmapped (best Task 3, containment 0.5) |
| INF-197 | The issue can be closed by hand once Ryan reports. | source.md:249-249 | matched Task 12 (containment 0.667) |
| INF-198 | The issue stays open with the table as its status. | source.md:249-249 | matched Task 13 (containment 0.8) |
| INF-199 | Any write to IronHands-CLI, irondots or ironops-marketplace, or to the archived IronHands repo, or to any repository outside IronbellyOrg. | source.md:255-255 | matched Task 3 (containment 0.818) |
| INF-200 | A render tool, an audit script, a reconciliation framework, a second-pass-zero-changes check, or retry machinery beyond "list, then create if absent". | source.md:256-256 | unmapped (best Task 3, containment 0.294) |
| INF-201 | Protecting `dev`, `release/v*` and `dot/*`; required approvals or status checks; changing IronClaude's three live rulesets or JSON files. | source.md:257-257 | unmapped (best Task 3, containment 0.533) |
| INF-202 | Organisation-level rulesets (plan availability UNVERIFIED) and moving the files out of IronClaude. | source.md:258-258 | unmapped (best Task 3, containment 0.4) |
| INF-203 | Making Sync fork work: the design only tests it after a mirror is applied and reverts if it is refused. | source.md:259-259 | unmapped (best Task 13, containment 0.545) |
| INF-204 | Merging the pull request, closing issue 837, or editing `.claude/`. | source.md:260-260 | matched Task 13 (containment 0.625) |
| INF-205 | ## Revision 1: findings of the plan review that this design must now carry | source.md:262-262 | unmapped (best Task 13, containment 0.429) |
| INF-206 | The review found four Blocking findings, which the new plan must fix, and thirteen Medium findings, which the new plan must not repeat. | source.md:264-264 | unmapped (best Task 4, containment 0.182) |
| INF-207 | Where this section and sections 1 to 9 differ, this section wins. | source.md:264-264 | unmapped (best Task 3, containment 0.5) |
| INF-208 | It adds no phase and no new scope; it changes where evidence is kept, what a few acceptance checks say, and what the runbook contains. | source.md:264-264 | unmapped (best Task 3, containment 0.385) |
| INF-209 | ### Blocking findings to fix | source.md:266-266 | unmapped (best Task 7, containment 0.333) |
| INF-210 | The acceptance check of the task that extends `tests/docs/test_branch_protection_rulesets.py` must name `test_branch_rulesets[protect-master-refs/heads/master]` and `test_branch_rulesets[protect-integration-refs/heads/integration]`, or name the test functions, and its verifier is `uv run pytest tests/docs/test_branch_protection_rulesets.py --collect-only -q`, whose output must list them. | source.md:268-268 | matched Task 4 (containment 0.8) |
| INF-211 | The test task keeps its one-file `uv run ruff check tests/docs/test_branch_protection_rulesets.py`. | source.md:269-269 | matched Task 4 (containment 0.846) |
| INF-212 | A task of Phase 1 or 2 of the plan must also run `make lint` and record its output; a failure on files that this change does not touch is recorded as pre-existing and named, never hidden. | source.md:269-269 | matched Task 13 (containment 0.833) |
| INF-213 | `.dev/tasks` is always staged and pushed, so everything that follows holds for the plan package, the archived superseded plan, every log and QA output written under `.dev/tasks`, the pull request body and every issue comment. | source.md:270-270 | matched Task 13 (containment 0.619) |
| INF-214 | The four state files of section 2 stay where section 2 puts them: `.dev/issues/837/audit/<repo>.md`, `.dev/issues/837/gates.md`, `.dev/issues/837/handoff-ryan.md` and `.dev/issues/837/apply-runbook.md`, never staged. | source.md:271-271 | matched Task 13 (containment 0.7) |
| INF-215 | Task outputs that the design places there are written there and not under the package `artifacts/` folder; the package `artifacts/` folder holds only the codegraph grounding note. | source.md:271-271 | unmapped (best Task 3, containment 0.333) |
| INF-216 | The producer search for coder_orca reads the private repository's release tooling to confirm that it deletes tags (E-2 of the merged requirements). | source.md:272-272 | matched Task 5 (containment 0.923) |
| INF-217 | The task reads it without printing or saving its lines: only a neutral conclusion is recorded in any file under `.dev/` that could be staged and in anything posted to GitHub | source.md:272-272 | unmapped (best Task 5, containment 0.571) |
| INF-218 | Verbatim lines, line numbers, file names, folder names and function names of that tooling are written only to `.dev/issues/837/private/coder_orca-producer-evidence.md`, which is never staged. | source.md:272-272 | matched Task 5 (containment 0.85) |
| INF-219 | The file name, folder and function names themselves are not written in the plan: the plan points to E-2 of `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md` for them. | source.md:272-272 | matched Task 13 (containment 0.652) |
| INF-220 | The staging list of the runbook does not include the brainstorm folder. | source.md:273-273 | matched Task 13 (containment 0.833) |
| INF-221 | Story step 9 names only the changed files and `.dev/tasks`; the folder describes the private tooling (E-2 and D5 of the merged requirements). | source.md:273-273 | matched Task 13 (containment 0.786) |
| INF-222 | Whether to publish it is the user's decision and the runbook says so. | source.md:273-273 | matched Task 13 (containment 1.0) |
| INF-223 | Part one of the runbook gets a pre-stage guard: print `gh repo view IronbellyOrg/IronClaude --json visibility -q .visibility`, then run `git diff --cached` and `grep -n -f .dev/issues/837/private/guard-patterns.txt` over the staged files; any hit stops the staging. | source.md:274-274 | matched Task 13 (containment 0.968) |
| INF-224 | `guard-patterns.txt` is a never-staged file that a Phase 1 task writes from E-2 (the file name, the folder name and the names of the tag-deleting functions). | source.md:274-274 | matched Task 5 (containment 0.867) |
| INF-225 | The only path the guard may exclude is the archived superseded plan folder `.dev/tasks/archive/TASK-WF-design-20261126-130537/`, which names that tooling in two lines and cannot be edited; the runbook lists this as an open item for the lead. | source.md:274-274 | matched Task 13 (containment 0.962) |
| INF-226 | Part one of the apply runbook (staging, the pre-stage guard, recording the pushed SHA, posting the handoff and the draft ledger as a comment on issue 837) runs right after the commit and push, whatever the ledger decides. | source.md:275-275 | matched Task 13 (containment 1.0) |
| INF-227 | Only part two, the gated apply, waits for the pull request monitor and for a ledger decision of `APPLY`. | source.md:275-275 | matched Task 13 (containment 0.9) |
| INF-228 | The expected run applies nothing (section 8), so part one must not depend on `APPLY`. | source.md:275-275 | matched Task 13 (containment 0.778) |
| INF-229 | ### Medium findings the new plan must not repeat | source.md:277-277 | unmapped (best Task 1, containment 0.2) |
| INF-230 | The ledger header cites `.dev/issues/837/accuracy-check.md` line 13 (PR 844 merged, commit 206abea1c; live ruleset 28081842 with `update`) as the verification the lead asked for, and states the rule: if the `update` rule on the release-tag ruleset is not settled, every tag row is `SKIP(not settled)` and only the branch rulesets are copied. | source.md:279-279 | matched Task 11 (containment 0.788) |
| INF-231 | The ledger uses only `APPLY`, `SKIP(<first failing gate>)` and `HANDOFF` (section 3.5). | source.md:280-280 | matched Task 11 (containment 0.889) |
| INF-232 | No `PENDING` value: G8 and G9 give `SKIP` until they hold. | source.md:280-280 | unmapped (best Task 11, containment 0.444) |
| INF-233 | The runbook carries the consequence of section 3.1 for a refused mirror bypass actor: drop the actor from the mirror file and change the file, the test, the guide and D4 together before anything is applied. | source.md:281-281 | matched Task 13 (containment 1.0) |
| INF-234 | The handoff task depends on the guide task, because it takes its commands from the guide section. | source.md:282-282 | matched Task 3 (containment 0.875) |
| INF-235 | With the state files in `.dev/issues/837/`, the R0 to R7 results go into the audit file and the ledger exactly as section 3.6 says; there is no separate apply-results file. | source.md:283-283 | matched Task 13 (containment 0.824) |
| INF-236 | The `<PUSHED-SHA>` placeholder is replaced in the text posted as the issue comment, not in a committed file. | source.md:284-284 | matched Task 12 (containment 0.9) |
| INF-237 | After any later push, the pinned links are re-pinned in a new comment (R6). | source.md:284-284 | unmapped (best Task 13, containment 0.333) |
| INF-238 | The pull request body task names the path of the merged requirements: `.dev/brainstorms/20261126-115959-apply-branch-protection-rulesets-other-repos/merged-requirements.md`, read locally, section "Done condition for this pull request". | source.md:285-285 | matched Task 14 (containment 0.917) |
| INF-239 | The guide check in the test iterates over the `.json` files that exist in `other-repos/`, so an absent optional `protect-aidev02.json` does not fail it; the guide section lists the path of `protect-aidev02.json` in its note on `aidev02`. | source.md:286-286 | matched Task 4 (containment 0.889) |
| INF-240 | The acceptance check of the runbook task says which variables are filled now (`REPO`, `PARENT_OWNER`, `BRANCH` and the file the ledger decides); `ID`, `END` and `START` are set on apply day. | source.md:287-287 | matched Task 13 (containment 0.95) |
| INF-241 | Every write command of the runbook names its repository explicitly, including the scratch-clone pushes of R1: `git push https://github.com/IronbellyOrg/$REPO.git ...` from the scratch clone. | source.md:288-288 | matched Task 13 (containment 1.0) |
| INF-242 | The Targets table and the handoff treat a fork of a Ryan repo like a fork of a Clay repo: the mirror file only when `ahead_by` is 0 and Clay's written acceptance (G4) is quoted, otherwise the full file; the handoff links both role files. | source.md:289-289 | matched Task 3 (containment 0.714) |
| INF-243 | The ledger has one row per ruleset; the pull request body has one row per repository that summarises its rows. | source.md:290-290 | matched Task 14 (containment 0.8) |
| INF-244 | The count of `v*` refs reads every page (`--paginate`) | source.md:291-291 | matched Task 5 (containment 0.8) |
| INF-245 | the handoff text for the tag ruleset says: included where the repository has no `v*` tag and the read-only workflow search found no tag mover, because there is then nothing to break. | source.md:291-291 | matched Task 12 (containment 0.933) |

Postscript: no row was dropped by the Wave 5 re-check, so `coverage_pct_union`, `unmapped_requirements_union` and `S_dev_density` are unchanged by it.

## Checked and found sound

- Execution boundary: every outside call in the 14 tasks is a GET (`search/code` uses `-X GET`, PLAN:99, 111); pytest, ruff and `lint-architecture` only read; writes are runbook instructions for a later session (PLAN:19-28, 182-186).
- Tasks 1 to 4: `protect-master.json:6` and `:8` are the one-line `ref_name` and `bypass_actors`; the five `pull_request` parameters are at `protect-master.json:15-19`; `_BRANCH_FILES` TEST:19-22, `_load` TEST:25-26, `test_branch_rulesets` TEST:30, `test_tag_ruleset` TEST:47, the `glob` TEST:67; the guide is 67 lines with H2s at lines 5, 19, 41, 51, 65, so the new section fits between "Break glass" and "Tests"; the six pages that link to the guide keep their lines (CONTRIBUTING.md:70, README.md:59, documentation-index.md:37 and 168, release-procedure.md:24 and 215).
- Dependencies: Tasks 1, 2, 3, 4 in order (PLAN:44, 56, 69); the audits do not depend on Tasks 1 to 4; the ledger after the audits; the handoff after the guide (PLAN:167); `guard-patterns.txt` is written by Task 5 before Tasks 13 and 14 read it.
- The plan, `source.md` and the grounding note contain none of the E-2 file, folder or function names; the repo name `IronbellyOrg/Coder` appears only at PLAN:22 and in the spec (allowed, SPEC:272). Only ARCH holds them under `.dev/tasks`: ARCH:82 has the path and the function names, ARCH:88 the file name (checked by the orchestrator with strings computed in the shell).
- The staging list excludes `.dev/reflect/` (nothing in PLAN names it) and the brainstorm folder (PLAN:184); both hold the private path, so they do not reach GitHub through the runbook as written.
- `/sc:pr-submit` flags `--base` and `--head` exist (`pr-submit.md:8`, 51; per reviewer-3, not re-read by the orchestrator).
- M-05 to M-09 and M-11 to M-17 of run 1 are carried at PLAN:156, 160, 186, 167, 21, 201, 58, 71, 123, 169, 83, 99, 206 (per the reviewers and T1); M-17's `--paginate` count is at PLAN:83.

## Tier 2 process

| Reviewer | Persona | Model class | Self-reported | Blind-calibrated |
|---|---|---|---|---|
| reviewer-1 | analyzer | sonnet | 0.80 | 0.72 |
| reviewer-2 | qa | haiku | 0.94 | 0.66 |
| reviewer-3 | refactorer | opus | 0.80 | 0.70 |

- Debate (`adversarial/debate-transcript.md`): 3 advocates, 2 rounds plus the invariant probe; 27 diff points; 24 resolved (convergence 0.8889). Unresolved: C-009 and C-010 (advocates split 2 to 1 each way; the orchestrator graded Medium by the rule) and N-1/INV-001 (V3 Blocking, probe HIGH, graded Medium and not re-debated). Base card V3 (`adversarial/base-selection.md`).
- Invariant probe (`adversarial/invariant-probe.md`): three HIGH invariants (INV-001 to INV-003) carried into findings G-11, G-03 and G-14; the adversarial return contract lists them.
- **Degraded components:** the calibrator class could not be made disjoint from the reviewer classes (`calibrator_diversity: degraded`); the executor class is unknown (`executor_class_resolved: false`); the three reviewers ran on three distinct models (full class diversity) through one gateway (`t2_vendor_diversity: single`, effective diversity model-only); the diff analysis and merge ran in one debate-orchestrator agent, not separate analytical and merge-executor agents; the reviewers ground in the live tree (reviewer isolation off).
- One slip is on the record: the merge agent wrote a 952-byte scratch file to `/tmp` outside the output folder (criterion ids and verdicts only) and deleted it.

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: `3 / 393` = 0.01

## Recommendations

Only the Blocking findings are routed to repair (workflow Wave 4R); the Medium findings are listed as one proactive recommendation.

Blocking findings first; Medium and Note items are reported and grouped.

| file | change | verifier |
|---|---|---|
| PLAN Task 13 (PLAN:184), G-01 | Before `git add .dev/tasks`, add a STOP: do not stage, commit or push until the lead's written decision on `.dev/tasks/archive/TASK-WF-design-20261126-130537/` is quoted in `.dev/issues/837/issue-summary.md`; the guard exclusion is not permission to publish. | The runbook shows a STOP line before staging; `git diff --cached --name-only` lists no archive path until the decision is quoted. |
| PLAN Task 5 (PLAN:85, 91, 92, 93), G-02 | List the private contents read in the audit as "contents read of the private release tooling (path in `private/`)", with no path, file or folder name; require `guard-patterns.txt` to be non-empty with one line per E-2 string (file name, folder name, each function name) and no blank line; use `grep -c -F -f` here and at PLAN:184 and PLAN:208. | `test -s` and `wc -l` on the pattern file pass; `grep -c -F -f .dev/issues/837/private/guard-patterns.txt` prints 0 on the audit file and on the package's `artifacts/T5*` files. |
| PLAN Task 13 (PLAN:184, 186, 189-193), G-03 | Add a re-pin step to part one (not R6): after the monitor settles, compare the committed guide and the three ruleset files with the SHA in the posted comment (`git diff --exit-code <SHA> -- <paths>`); if anything changed, post a new comment with links and the copied commands refreshed from the final head. Add an acceptance line that names the step and says it runs when no ruleset is `APPLY`. | A second-push walk-through names the new comment; the acceptance line exists. |
| PLAN Task 13 (PLAN:182, 184), G-04 | Number part one: fetch and rebase check, commit, push, record the SHA, guard-grep the comment file, post one comment file that holds the handoff and the draft ledger, then `/sc:pr-submit --monitor 3`; let the pull request body point to the comment by title or patch it once. | The numbered list shows the post before the pull request command; the comment file definition names both texts. |
| PLAN Task 5 (PLAN:92), G-05 | Replace the `git status` check with `git check-ignore -v` on both private files. | The output names `.gitignore:162`. |
| PLAN Task 5 (PLAN:85), G-06 | Name the only allowed targets: a file under `.dev/issues/837/private/`; forbid `/tmp` and a shell variable carried between calls. | Reading the text; no file outside the worktree. |
| PLAN Tasks 11, 12, 13 (PLAN:156-163, 167-176, 184), G-07 | Add the `grep -c -F -f` check that prints 0 to Tasks 11 and 12 and to the comment file; guard the commit message, the pull request title and each monitor reply, or run the monitor at `--monitor 2`. | The grep prints 0 for `gates.md`, `handoff-ryan.md` and the comment file. |
| PLAN Task 11 (PLAN:156, 161), G-08 | State one rule: the gate named is the first failing one (G3 for every Clay row while the installations read is blocked) and keep G4 to G6 as notes in a reason column; add `not settled` to the stated decision set or drop it. | Every Clay `SKIP` row names the same gate. |
| PLAN Task 13 / 14 (PLAN:184, 201), G-09 | Add a short per-repo audit-result table (`CLEAR` or `BLOCKED` and the first failing gate) for the three Clay repos to the comment file. | The comment file holds six rows. |
| PLAN Task 13 and the guard (PLAN:21, 184), G-10, G-11, G-13 | Make the guard patterns distinguishing strings (for example the file name and the call form of each function name), use `-F -l`, treat exit 0 as a stop and any other non-1 exit as a stop, run it over `git diff --cached --name-only` after staging, and say what the lead does after a hit; tell Task 5's review to leave the names out of `artifacts/`. | The guard prints no hit on the executor's own retry prompts; the order shows the checks after staging. |
| PLAN Task 3 (PLAN:61-65), G-12 | Add one acceptance line each for the producer search checklist and the tag ruleset check. | The guide contains both. |
| PLAN Task 13 (PLAN:184), G-14, G-16, G-15 | Add the fetch and rebase check and name remote and branch on the push; name the scratch clone and run it with `git -C`; record code-search hits from private repositories only under `private/`. | The runbook shows the fetch line; the scratch clone path is named. |
| PLAN (PLAN:109, 180, 58, 71, 156), G-17 to G-19 | Notes only: add `Depends on` lines, state the Ryan repos' tag value, align the decision set. | Reading. |

## Limits

Not verified: the live state of GitHub (nothing was run against it); the live behaviour of `/sc:pr-submit` beyond its documented lines; the guide text below its H2 headings; the admin-only commands that Ryan runs. ARCH:82 and ARCH:88 were checked by shape only (the private names are deliberately not copied into any report). Reviewers read the live tree, not a snapshot.

