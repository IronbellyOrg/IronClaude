# Round 2 findings: issue #787 (C6) Each step names the Orca verbs it may call, checked against the refusal list

Checked against master `f2894fc44`, 2026-11-24. Read-only. Plan files: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`. R38 is at `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64` in this worktree. Round 1: `.../Analyze716/.dev/issuecleanup/a716/2/787/findings.md`. Umbrella #716, its backlog review and closing review were read.

## Alignment with architectural decisions

- **R38 (requirements.md:64): in conflict for the `refuse(argv)` half, aligned for the per-step list.** R38 says "no element of Clay's orchestrator design for issue 655 is adopted" and "supersedes the 'Clay strengths adopted' rows of the unification spec (section 7...)". `refuse(argv)` is row D8 of section 7 (SPEC.md:459, "closed 'may do' list, `refuse(argv)`", ADOPT+CHANGE, carrier "PB"). SPEC.md:435-437 defines "PB" as "Clay's unbuilt coordinator verb group (PR B)". So the refusal list that C6 checks against is a voided row, and it is not built (SPEC.md:62 lists `refuse(argv)` NOT BUILT; `tests/coordinator/` does not exist). R38 does not name `refuse(argv)` explicitly among its rejected items (it names registry, wake file, tier keys, merge gate, flags); whether the owner keeps it is UNVERIFIED. The backlog review on #716 (2026-11-24, step 1) says "Keep retained engineering requirements distinct from rejected architecture" and also lists C6 among the items to start with, so the owner's own review keeps the per-step list but did not settle the list it is checked against.
- **FR-26 (SPEC.md:228) and D15 verdict row D8 (debates/D15/VERDICT.md:92): partly aligned.** They define one closed `refuse(argv)` list "with a failing test per pattern". C6's per-step lists must be subsets of that one list; if they become a second authority they would contradict D8. With the list voided, the safe form is: one allowed-verb table inside the skill, per-step lists as subsets.
- **FR-40 (SPEC.md:242: never interrupt a worker, never approve a prompt), WC-13 (WORKER-CONTRACT.md:63), WC-8 (:40): aligned.** The test must fail on any step that lists an interrupt verb, a permission approval, `worker-stop`, `worker-abandon`, or a worker-side use of `worker-start`, `dispatch`, `task-create`.
- **S14 "skill-text scan" (SPEC.md:498): aligned as the home of the check.** C6 defines what that scan extracts. S14 also holds merge-path rows that R38 (D: "a person's typed go for every push and merge; the coordinator never merges") voids, so the scan is the part of S14 that survives.
- **D08 / FR-62 (name `coordinator`):** aligned; no effect.
- **Existing verb lists on master: partly aligned, risk of drift.** Three exist now: launch guard `src/superclaude/hooks/scripts/launch-level-guard.sh:495-506`, observer forbidden prefixes `src/superclaude/cli/observe/adapter.py:34-50`, sweep allowlist `src/superclaude/cli/sweep/probes.py:49-58`. C6 would add a fourth. The sweep names the binary `orca-ide` (probes.py:43) while the guard and contract text use `orca`; the per-step check must state which binary name it matches (analyze report, finding 4).
- Searched: DECISIONS.md, SPEC.md and the D04, D05, D15 verdicts for `refuse(argv`, `may do`, `skill-text scan`, `verb`: all hits are the Clay rows above; no owner-approved decision defines a per-step verb list.

## Complementary issues

- **#782 (C1):** defines the steps and the wave table that the per-step extraction reads; #806 (template tests) was merged into #782 on 2026-11-24, so #782 now owns the skill-text file-table and template tests. Interface: same parser.
- **#783 (C2, STOP codes):** a second test that reads the same skill files for a closed table. Interface: share one parser and one "closed table versus text" helper.
- **#785 (C4):** a loaded Orca guide can name verbs the plan does not allow; C6 is the check. Interface: C6's per-step lists win over the guide.
- **#786 (C5):** `run-use` and `run-create` are allowed in the coordinator's Run step only and stay forbidden in observer and sweep.
- **#788 (C7), #793 (C12), #800 (C19), #794 (C13):** each adds verbs to a step; they must update the table, they do not block the mechanism.
- **#757 (model-free scheduled task):** its read-only verbs belong in the sweep list, not the coordinator's.

## Closest overlap

**#783 (C2) "Named STOP codes table with a two-way test".** Shared: both are tests that read the coordinator skill's text, extract tokens (`E-` codes versus Orca verbs), and check them against one closed table, in both directions. Estimate: #783 covers about 20 percent of #787's done-when (the parser and the two-way table-versus-text test pattern, not the verb extraction, the per-step lists, or the refusal-list check).
Next two: **#782 (C1)**, about 15 percent (its file-table test and, since #806, template tests read the same files; it defines "step"); **#785 (C4)**, about 10 percent (the load is the case the verb check guards).

## Standalone or merge

**Verdict: stand alone, with the lowest priority of the three and a changed scope.** Tested against #783:
- Owner: same builder (skill tests). Favours merging.
- Acceptance test: different content. C2 checks codes in text versus a table; C6 checks verbs per step versus an allowed list, and needs a list that does not exist.
- Files touched: C2 adds a table and a test; C6 adds per-step verb lists in every wave ref and a test. C6 touches every ref file, C2 touches the table and a few lines.
- Build phase: C2 is Phase 1; C6 is in the same group in the review, but its check cannot be complete until the later items (C7, C12, C19) add their verbs.
- Risk if merged into #783: the two merge on "shared parser", but C6 carries the unmade owner decision on `refuse(argv)`; merged, it would hold C2 (a simple item) behind that decision.
Deciding reason: the open owner decision on the refusal list and a different breadth (every ref file) argue against merging. Merging would be right if the owner drops `refuse(argv)` for good: then C6 shrinks to "each step lists its verbs from one allowed table in the skill, and a test compares text to table", which is the same pattern as C2 and should be one pull request with it (or with #782's tests). Treat that as the likely end state and re-check after the owner answers.

## Closed issues and merged PRs checked

- **#806 (closed, merged into #782, 2026-11-24):** round 1 asked C6 to share a parser with C25 (#806); that issue is now part of #782, so the shared parser belongs to #782's test code.
- **#796 (C15, closed not planned), #804 (C23, closed), #798 (C17, merged into #797), #809 (W1, merged into #716):** all closed under R38. This is the same reasoning that questions C6's dependency, and #798 was merged because it "has no consumer without the merge gate", the same shape as a check with no list to check against.
- **PR #539 (merged):** the sweep's 10-template allowlist is the nearest shipped example of a closed verb list with a test.
- **PR #432 and #469 (merged, launch-level guard and L2 pre-push):** the guard's allowed-orca list is the second shipped list; it classifies text, not skill steps.
- **PR #591 (merged, Plan B):** added guard G2 (`orchestration send` and `ask` only to the coordinator); a per-step list for workers' lifecycle verbs would repeat it.
- **PR #503, #514 (observer, merged):** observer's `FORBIDDEN_PREFIXES` is the shipped model for "forbidden verbs by prefix".
- **PR #700, #701 (merged):** the 655 build including its `coordinator` verb group was rolled back; nothing of `refuse(argv)` exists on master.
- **#444 (closed):** deferred sub-orchestrator work; no verb list.

## Updated recommendation

- **Action:** keep open with changes. (1) Say what "step" means by pointing to #782's wave table instead of "wave". (2) Replace "checked against the refusal list" by "checked against one allowed-verb table in the skill; if the owner keeps `refuse(argv)`, the table is its source", and ask the owner for that decision before build (R38 does not name it). (3) State that per-step lists are subsets of one list and the test is S14's skill-text scan, not a second scan. (4) Share one skill-text parser with #783 and #782's tests. (5) State the binary name matched (`orca` versus the sweep's `orca-ide`).
- **Priority:** P3. **Complexity:** medium, size M. If the owner drops `refuse(argv)`, complexity falls to simple and size to S.
- **Change from round 1:** priority and size unchanged. Changed: the dependency on S13/S14 and `refuse(argv)` is now a recorded conflict with R38's section 7 supersession (round 1 treated them as blockers to wait for), the shared-parser partner moved from #806 to #782, and a fourth verb list is flagged.

## Scan record

- Lists read in full (titles): open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Search terms: refuse, verb, allowlist, forbidden, guard, skill-text scan, STOP, template tests, coordinator skill, sweep, observer, closed list.
- Opened in full: open #716, #782, #783, #788, #755, #793, #794, #800, #761, #770, #757, #725, #771, #805, #807; closed #806, #796, #798, #804, #809, #444, #507. Merged PRs opened: #591, #514, #539, #735, #736, #683; #432, #469, #503, #700, #701 read by title and #716's review text only.
- Command run: `/sc:analyze src/superclaude/cli/sweep --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/2/analyze` (its findings 1 to 4 are the evidence for the verb lists).
- UNVERIFIED: whether the owner keeps `refuse(argv)` (R38 does not name it); whether S13 is re-staged; the Coder launch prompt (other repository).
