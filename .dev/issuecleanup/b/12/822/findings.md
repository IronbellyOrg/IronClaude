# Round 2 findings: issue 822 (W14, check-config refuses a state folder that is not on a local disk, FU-12)

Checked 2026-11-24 against master f2894fc44 in `/home/coder/workspaces/worktrees/IronClaude/Realign`. Sources: issue 822, round 1 findings (`/home/coder/workspaces/worktrees/IronClaude/Analyze717/.dev/issuecleanup/a717/5/822/findings.md`), umbrella #717 and its closing review, `.dev/issuecleanup/b/12/analyze/analyze-report.md`.

Item defect: the body of #822 also carries the whole W15 block (an unchecked box after the W14 text). Same leak as in #821. A text edit fixes it, made by the coordinator after the owner's go.

New fact since round 1: **W5 (#813) was closed not planned on 2026-11-24 at 22:10Z, and its closing comment says "the persistence need is carried by W14 (#822)"**. Round 1 treated W5 as an open sibling to order against. W14 is now the only open home of the persistence need.

## Alignment with architectural decisions

- **R18 and R28** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:44` and `:54`, owner 2026-11-18 and plan review 2026-11-19): the shadow run, lock test and restart test became one automatic first-run check; its restart step is an in-process reload and a second dry run (`src/superclaude/cli/issue_watch/first_run.py:292-308`). Partly aligned: W14 adds a check the first-run restart step cannot make (a folder wiped by a real restart cannot be seen in process), so it fits R18's intent that a failed check leaves the repo `enabled: false`. A refusal in `cycle.load_config` reaches the first-run config step (`first_run.py:233`) and gives exactly that.
- **R38** (`requirements.md:64`): merged design stands. Aligned: W14 extends the merged `state_dir` rule; it needs no element of Clay's design.
- **Design findings DF-23 and DF-53** (`docs/designs/issue-watcher.md:75`, `:143`; tests `tests/issue_watch/test_cycle.py:498-501` and `:520-525`): the rule is a network-filesystem deny-list; tests pin the exact seven types and list `tmpfs` among the types that must load. In conflict with W14 as worded for the non-persistent half: adding tmpfs reverses a recorded finding and flips a pinned test case. It can be done on purpose by a second set beside `NETWORK_FS_TYPES` (`cycle.py:50`).
- **FU-12** (`docs/designs/issue-watcher.md:871`, `docs/designs/issue-watcher-setup.md:679`; techref D-15 `techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1966`, "No code"): the deferred item is an allow-list "when per-host facts are gathered". Aligned for the allow-list form (needs host facts, none in the plan folder); the deny-set form for tmpfs and ramfs needs none.
- **NFR-03** (`SPEC.md:216`, "Read the state root from config `state_dir`; never recompute it"): aligned; the check reads the configured path only.
- **R12 and R5** (`requirements.md:32`, `:31`): the generator writes an explicit absolute `state_dir` per repo, so the live default path is under the home volume. On this host `~/.local/state/superclaude` is on ext4 and `/tmp` is on overlay (`findmnt`), so an overlay-based "non-persistent" rule would be wrong: it cannot tell a wiped overlay from a kept one.
- No DECISIONS.md, SPEC.md, FOLLOW-UPS.md or `debates/*/VERDICT.md` entry decides FU-12 (search returned only the techref rows). `WORKER-CONTRACT.md`: none apply.

## Complementary issues

- **#717** (umbrella): its closing review says "gather W14's persistence facts before W5's restart test"; W5 is now closed, so the order is moot and W14 carries the need.
- **#823 (W15, runbook)**: owns the runbook text. The #813 closing comment also says an optional manual restart proof should be "a one-time runbook check recorded in W15". Interface: when W14 lands, runbook lines `issue-watcher-setup.md:98`, `:283` and `:679` (FU-12 row) change; W15 writes them, or W14's PR edits only the `state_dir` table row and FU-12 row.
- **#816 (W8, alert)**: a persistence warning could be a field in `status`, the same surface as W8's alert; no code in common.
- **#774** (docs refresh): leaves `issue-watcher-setup.md` to W15; no direct link to W14.
- **#821 (W13)**: sister item on the same store folder (size bound); independent code.

## Closest overlap

- **#823 (W15): "Issue watcher W15: Update the owner runbook to the unified design after the live test"**. Shared: the persistence statement of the runbook (`issue-watcher-setup.md:283`, section 8.3) and, since the #813 closing, the optional manual restart proof. About 10 percent of W14's done-when ("`check-config` flags a `state_dir` on a network or non-persistent mount") is touched by W15, and only as documentation of the same fact, not as a code check.
- Next two: **#816 (W8)** (shared `status` surface, 0 percent) and **#821 (W13)** (same folder, 0 percent).
- The network half of W14's done-when is already delivered by master (`cycle.py:293-295`, PR 447), which no open issue duplicates.

## Standalone or merge

Verdict: **stand alone**. Against #823:
- Owner: same owner.
- Acceptance test: W14 is a code test with a mountinfo fixture (a tmpfs `state_dir` is flagged). W15 is a person following the runbook with captured steps. Different tests.
- Files touched: W14 `cycle.py` (or `first_run.py`) and `tests/issue_watch/test_cycle.py`; W15 two runbook files.
- Build phase: W14 is buildable now; W15 waits on a live record.
- Risk if merged: code waits on a live capture that may never exist, or the runbook is edited inside a code PR whose reviewers do not check prose.
Merging would be right only if the owner reduces W14 to the runbook check (drop the code), which is a legitimate alternative: the #813 closing text allows "a one-time runbook check recorded in W15". Under that choice W14 closes and W15 absorbs it. Not recommended: the code is a few lines and the live default already works.

## Closed issues and merged PRs checked

- **#813 (W5)**, closed not planned 2026-11-24: delegates persistence to W14 and the optional manual proof to W15. Changes W14's "Related items: W5" line (stale).
- **#809 (W1)**, closed, merged into #716: no effect.
- **#450**, closed: live since 2026-11-23 with a persisted state folder (ext4); records that the shadow, lock and restart tests were replaced by the first-run check.
- **PR 447** (merged 2026-11-08): delivered the network-filesystem refusal and its tests.
- **PR 707** (merged 2026-11-20): first-run check with lock and restart tests (R18, R28).
- **PR 759** (merged 2026-11-24): retry of a failed first run; the new check would feed the same first-run report.
- **PR 485** (merged): runbook rollout checklist, section 8.3 manual check.
- **#751** (closed): the failed-first-run case W14's refusal would produce on a tmpfs folder.
None contradicts W14 except the pinned tests and the deny-list findings above.

## Updated recommendation

Keep open with changes, **P3**, **simple**, size **S**. Unchanged from round 1 on action, priority, complexity and size. Changes to the changes:
1. Say the network half is done (PR 447; `cycle.py:293-295`) and narrow W14 to non-persistent types (tmpfs, ramfs) as a second set beside `NETWORK_FS_TYPES`; flip the tmpfs test case on purpose.
2. Choose placement on purpose: a refusal in `cycle.load_config` stops every verb and every `run-all` sweep for that repo with exit 2; a warning in `check-config` and a failed first-run step give the same early signal without stopping a live repo.
3. Replace "Related items: W5" with "carries the persistence need of closed W5 (#813)"; delete the wait for "per-host facts" for the deny-set form.
4. Remove the leaked W15 block.
5. Say plainly that overlay and other wiped-on-restart folders cannot be detected by file system type; the runbook check (section 8.3) stays for them.
The owner decides.

## Scan record

Lists read in full: open-issues.tsv 134 of 134, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508. Search terms: state, store, persist, filesystem, restart, first-run, runbook, check-config, config, mount, W-numbers, watch. Opened with gh: open #717, #770, #774, #775, #777, #816, #819, #820, #821, #823, #811, #815 (12 open); closed #813, #809, #450, #751 (4) and merged PRs #447, #485, #707, #729, #759 (5); plus `findmnt` and the live store folder read-only. Plan files read by search as in #821. Command run: the `/sc:analyze` report named above. UNVERIFIED: whether Coder's startup keeps `$HOME` persistent on every workspace (the Coder repo is outside this review's allowed reads); how often a custom `state_dir` is set on tmpfs in practice (no sample).
