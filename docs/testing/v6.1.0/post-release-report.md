<!-- SC:POST-RELEASE:RESULT
status: partial
run_mode: additive
install_surface_class: package
report_path: /home/coder/workspaces/worktrees/IronClaude/v61-post-release/docs/testing/v6.1.0/post-release-report.md
manifest_path: /home/coder/workspaces/worktrees/IronClaude/v61-post-release/docs/testing/v6.1.0/post-release-manifest.json
workstream_results: {"A":{"updated":12,"created":0,"gaps":6,"verified":true},"B":{"updated":7,"created":0,"gaps":5,"verified":true},"C":{"updated":0,"created":2,"gaps":4,"verified":true},"D":{"updated":0,"created":0,"gaps":1,"verified":false},"E":{"updated":0,"created":0,"gaps":1,"verified":false}}
c_e2e_result: green
gap_list: [{"workstream":"A","gap":"observe, review and issue-pipeline have a listing only","evidence":"docs/user-guide/cli-groups.md","remedy":"write a guide per group"},{"workstream":"A","gap":"the new ccsession options (--agents, --mark, --classify, --prune) are in the skill README only, no docs/ page","evidence":"src/superclaude/skills/ccsession-tag/README.md; docs/getting-started/installation.md:372","remedy":"add a section to docs/user-guide/session-management.md"},{"workstream":"A","gap":"docs for /sc:issue (beyond the template sentence), ccsession 6.0.0 changes, Ponytail, pr-submit conflicts not checked line by line","evidence":"manifest present-unverified cells","remedy":"follow-up check"},{"workstream":"A","gap":"/sc:code-review, /sc:create, /sc:review, /sc:close named in docs but not shipped","evidence":"scan-unshipped-commands.txt","remedy":"replace or mark as examples"},{"workstream":"A","gap":"CHANGELOG [6.0.0] lacks entries for observe, review, issue-watch, issue-pipeline, /sc:issue","evidence":"CHANGELOG.md [6.0.0]","remedy":"owner to approve entries"},{"workstream":"A","gap":"release notes v6.0.0 manual-validation numbers differ from the 6.0.0 run","evidence":"docs/releases/v6.0.0.md","remedy":"orchestrator to correct or accept"},{"workstream":"B","gap":"no technical doc for superclaude observe","evidence":"src/superclaude/cli/observe/","remedy":"write a design or reference note"},{"workstream":"B","gap":"orchestration reference: other citations have an unknown baseline; lines 317 and 2197 keep research-time counts","evidence":"check_citations.py output","remedy":"re-verify against its own baseline"},{"workstream":"B","gap":"git-standards-protocols.md is another project's doc","evidence":"docs/developer-guide/git-standards-protocols.md","remedy":"remove or replace"},{"workstream":"B","gap":"root VERSION file says 3.7, pyproject says 6.1.0","evidence":"VERSION","remedy":"update or delete"},{"workstream":"B","gap":"citation checker lives in a worktree evidence folder and misses CHANGELOG.md and .github citations","evidence":".dev/issues/v61-post-release/check_citations.py","remedy":"move into scripts/ and extend"},{"workstream":"C","gap":"ccsession agent-session hiding and --prune --apply not run with seeded sessions","evidence":"transcript lines 873-897","remedy":"seed sessions in a later run"},{"workstream":"C","gap":"retention write branch shown only with CCSESSION_MANAGED_SETTINGS_DIR (host managed value 90 equals the target)","evidence":"transcript lines 847-875","remedy":"none needed"},{"workstream":"C","gap":"installer exits 1 when claude is replaced by its auto-updater mid-run (6.0.0 run); the script pins a copy","evidence":"docs/testing/v6.0.0/post-release-report.md","remedy":"optional installer retry"},{"workstream":"C","gap":"offline install and upgrade not tried; 5.0.0 or 4.x straight to 6.1.0 not run","evidence":"scope","remedy":"try in a later release"},{"workstream":"D","gap":"no hand-test guides for the 6.0.0 and 6.1.0 changes","evidence":"decision 6.1.0-5","remedy":"deferred by decision"},{"workstream":"E","gap":"no sysop guides for observe, issue-watch, issue-pipeline, launch-level hooks, WORKER-CONTRACT.md, ccsession --prune","evidence":"decision 6.1.0-5","remedy":"deferred by decision"}]
duration_sec: 655
-->

# Post-Release Report — `v6.1.0`

- **Version / tag:** `v6.1.0` (`v6.1.0`, annotated tag object `d7cbc0238b58ac0010502a6598ca6049083355b5` on commit `64dfc0e8622281a56d6c4e6826c63d50c6959da8`, tagger date 2026-11-19 01:57:19 UTC)
- **Previous release:** `v6.0.0`
- **Run mode:** `additive`: evidence a prior manifest exists at `docs/testing/v6.0.0/post-release-manifest.json` (the v6.0.0 run, itself additive on v5.0.0). The delta is `v6.0.0..v6.1.0`: 197 changed paths outside `.dev/` (saved in the run's evidence folder as `delta-name-status.txt`), every one categorized in `CONSOLIDATED-PLAN.md`: the removal of nine skills, `/sc:tdd` and one eval suite, the plan route at every depth, ccsession agent sessions and the 90-day retention target (#641), the installer comparison fix (#646), the review seat labels (#660) and the `/sc:issue` template sections (#661) touch the external surface; tests, templates, plugin mirror and skill references are internal.
- **Install-surface class:** `package`
- **Date:** 2026-11-19
- **Branch:** `clayphi/v61-post-release`

## Summary

The user and technical documentation was brought in line with the tagged 6.1.0 tree: 12 user-facing files edited (CHANGELOG, release notes, README, the upgrade page, installation, quick start, two reference pages, three user-guide pages), 7 technical notes re-anchored or corrected, no new page. The install path was run for real in throwaway homes and is **green**: a new user (`pipx install` from the tag: 34 commands, 48 agents, 26 skills), an upgrade from a genuine 6.0.0 (the retire step removed 8 skills and kept the edited `/sc:tdd` and the `task-builder` folder with an extra file; after the two printed `rm` commands the counts are 34 / 48 / 26 and `doctor` is healthy), and `./update.sh` from a clone. The real home was not touched. Workstreams D and E were skipped by decision 6.1.0-5. The honest bottom line: scoped work is done and every number in the upgrade page is backed by the transcript, but 17 gaps remain (most carried from 6.0.0; the new ones are the ccsession options having no `docs/` page and not being run with seeded sessions), and the review of this work is mechanical, by its author with tools, until the pull request reviews finish.

## Scope of this run

Authorized by Clay (user clayphi) on 2026-11-19 01:18 UTC, relayed by the coordinating session GeneralIronFlow ("run post-release as for 6.0.0"); the task prompt is `.dev/releases/current/v6.1.0/prompts/post-release.md` in the `ic6-orchestrator` worktree (decision 6.1.0-5).

- **In scope:** A (user documentation), B (technical documentation), C (install and deploy scripts, proven by a real end-to-end run: a fresh install of 6.1.0 and the upgrade from a genuine 6.0.0, in throwaway homes only).
- **Out of scope by decision 6.1.0-5:** D (user-facing human-test guides) and E (sysop-facing human-test guides). Nothing was scanned for them and none were written. `docs/testing/v5.0.0/` and `docs/testing/v6.0.0/` are unchanged.
- **Also required by the task (not part of the skill):** CHANGELOG entries for #660 and #661 and the release date `2026-11-19` in the `## [6.1.0]` heading; the same two items and the date in `docs/releases/v6.1.0.md`; version labels, install lines and counts moved to 6.1.0 in the files the task lists; a search for 6.0.0 used as the current version; the install script started from the 6.0.0 one, with `unset NOTRACK EXPECT_RC` and a one-command negative check.
- **Not touched, by instruction:** `docs/testing/v5.0.0/`, `docs/testing/v6.0.0/`, `docs/designs/`, `docs/releases/v5.0.0.md`, `docs/releases/v6.0.0.md`, every other CHANGELOG entry.

## Release-integrity findings

1. **Tag and lineage (OK).** `v6.1.0` is an annotated tag (`git cat-file -t v6.1.0` prints `tag`) on the master merge commit `64dfc0e8`, an ancestor of `origin/master` (`git merge-base --is-ancestor`). The GitHub release exists (published 2026-11-19 01:57:25 UTC, neither draft nor pre-release). `pyproject.toml` says 6.1.0 and `superclaude --version` prints `SuperClaude, version 6.1.0` (transcript lines 29, 1242 and 2134).
2. **Tag equals the branch base (OK).** `git diff v6.1.0 HEAD` was empty before the first edit, so reading the working tree was the same as reading the tag. Where a claim needed a tag-only fact (counts, removed files) it was read with `git ls-tree` and `git show v6.1.0:<path>`.
3. **Release date was 2026-11-18 in the notes and the CHANGELOG heading (fixed on instruction).** The tag and release are dated 2026-11-19 (tagger date above). The notes' "Release Date" line and the `## [6.1.0]` heading now say 2026-11-19. The front-matter `last_updated` of the notes was moved to 2026-11-19 because the file was edited; `created_date` and the review dates are unchanged.
4. **CHANGELOG `[6.1.0]` lacked #660 and #661 (fixed on instruction).** Both were merged into `master` after the notes were written and are inside the tag. Entries were added from the pull requests and their diffs.
5. **Stale `CHANGELOG.md:<line>` citations in two developer-guide notes (finding, fixed).** `codegraph-integration.md` cited lines 87, 92, 93 and 113 and `review-severity-rule.md` cited 33, 278-282, 279, 280 and "starts at line 256". Those were lines of the 5.0.0-era file; at the tag the cited lines hold other text. They now point at the real entries (394, 399, 400, 420 and 336-340, 337, 338, 340, section start 314), counted after this run's CHANGELOG insertion. The 6.0.0 run's citation checker only matches `src/`, `tests/`, `docs/`, `scripts/` and `plugins/` paths, which is why they survived.
6. **`docs/developer-guide/review-severity-rule.md` quoted fixture counts of 140 and 125 (finding, fixed).** At the tag the fixtures hold 58 and 25 rows (`tests/skills/test_review_severity_rule.py:281,288`; counted by `old:` keys: 58 and 25). 6.1.0 removed the document skills the guard test used to check, which also shortened the test file by 11 lines after line 366; the line ranges of checks (g), (h), (i) and (k) were re-derived.
7. **Root `VERSION` file still says `3.7` (finding, not fixed).** `pyproject.toml` says 6.1.0. Only `scripts/build_superclaude_plugin.py` reads it. Carried from the 6.0.0 report.

## Coverage matrix (headline)

Delta capabilities only (the full carried-forward matrix is in `post-release-manifest.json`). D and E columns are out of scope (decision 6.1.0-5) and are left out here.

| Capability | User doc (A) | Tech doc (B) | Install (C) |
|---|---|---|---|
| `superclaude --version` prints 6.1.0 | ✅ updated (7 pages) | ✅ | ✅ run (3 scenarios) |
| Nine skills and `/sc:tdd` removed; counts 34 / 48 / 26 | ✅ updated (`upgrading.md`, `README.md`) | ✅ updated (`technical-architecture.md`, orchestration reference) | ✅ run (retire step: 8 removed, 2 kept, then 0 left) |
| Upgrade 6.0.0 to 6.1.0 (retire step, saved copies, doctor) | ✅ updated (`upgrading.md`, new "From 6.0.0 to 6.1.0" table) | ✅ | ✅ run (scenario 2) |
| Plan route at every depth; three-level routing guide; `--handoff task` removed | ✅ already current (`commands.md`, `brainstorm.md`, `how-we-work.md`; checked, not edited except `upgrading.md`) | ✅ updated (`session-memory.md`: reflect no longer writes `handoff-*.md`) | n/a |
| ccsession agent sessions (`--agents`, `--mark`, `--classify`, `--prune`) and 90-day retention target (#641) | ⚠️ in the skill's own `README.md` and `installation.md` (retention); no `docs/` page for the new flags | n/a | ⚠️ run on an empty home: options exist and answer, hiding and pruning not shown with seeded sessions; retention 90 / 365 / 500 / 7 / bad file run |
| Installer comparison fix (#646) | n/a (internal; one-shot installs behave as before) | ✅ (CHANGELOG entry present) | ✅ run (second install and `update` change nothing) |
| Review seat labels `review-seat-5a/5b/5c` (#660) | ✅ `docs/reference/review-panel-live7.md` (updated by the PR); CHANGELOG and notes entries added | n/a | ✅ run (installed tier file has version 1.2.0 and the new labels) |
| `/sc:issue` templates end with Priority, Fix approach, Test plan (#661) | ✅ created text in `commands.md` ("What `--create` writes"); CHANGELOG and notes entries added | ✅ (`docs/designs/sc-issue-command.md` updated by the PR; not touched here) | ✅ run (all four installed templates end with the three headings, in order) |
| Kept on purpose: `/sc:task`, `/sc:validate-tests`, eight `rf-*` agents | ✅ `upgrading.md`, `README.md`, `agents.md` | ✅ | ✅ run (all present after install) |

✅ present-and-current (updated or created this run, or checked and already current) · ⚠️ present but only partly covered or not shown end to end · ❌ missing · n/a not applicable

---

## Workstream A — User documentation

Since `v6.0.0`: the cleanup pull requests (#650, #653, #656, #657) had already rewritten the user pages that name the removed skills and commands (`commands.md`, `brainstorm.md`, `how-we-work.md`, `agents.md` text); a search of `README.md`, `docs/getting-started/`, `docs/user-guide/`, `docs/reference/`, `docs/developer-guide/`, `docs/swarm/`, `docs/eval/` and `docs/mcp/` for the removed names (`/sc:tdd`, `/task`, `/task-builder`, `/roadmap`, `/prd`, `/readme`, the other skill names, `--handoff task`) found hits only in `upgrading.md` (intended: the upgrade record), `brainstorm.md` (already says "removed in 6.1.0") and unrelated text. What was stale was the version, the counts and the upgrade page.

- **Scanned:** the files above, by search for 6.0.0 used as the current version (55 hits, `scan-600.txt`, each judged), removed names (`scan-removed.txt`), count claims (`scan-counts.txt`), and every `/sc:<name>` token against the 34 shipped commands (`scan-unshipped-commands.txt`).
- **Updated (12 files):**
  - `docs/getting-started/upgrading.md`: title and intro for 6.1.0 (what 6.1.0 removes: the nine skills and `/sc:tdd`; what it keeps: `/sc:task`, `/sc:validate-tests`, all eight `rf-*` agents), install line `@v6.1.0`, clone checkout `v6.1.0`, counts 12 / 34 / 48 / 26, the retire step's real output from the 6.0.0 to 6.1.0 run (the 6.0.0 excerpt is kept under "For 6.0.0"), saved-copies numbers (7 commands, 1 rule, 1 output style), a new "From 6.0.0 to 6.1.0" table in Step 6, the 6.0.0 table's `--handoff task` row marked as removed in 6.1.0, the see-also list. The retire-step section is kept.
  - `README.md`: "Upgrading to 6.1.0" with the tag URL and the removed and kept items; the documentation-map entry. `docs/getting-started/installation.md` (badge, version line), `quick-start.md`, `docs/reference/common-issues.md` (two lines), `docs/reference/troubleshooting.md` (four lines), `docs/user-guide/cli-groups.md` (title and intro; the 16 group names match `superclaude --help` of the tag), `docs/user-guide/agents.md` (48 agent files, none removed).
  - `docs/user-guide/commands.md`: a paragraph on what `/sc:issue --create` writes (#661), from `refs/create.md` of the skill. `docs/user-guide/flags.md`: the `--force` row names 6.1.0 among the upgrades that need it.
  - The 6.0.0 search after the edits (`scan-600-after.txt`): 39 hits remain, all history ("from 6.0.0", "removed in 6.0.0", the 6.0.0 release notes, the 6.0.0 record, the review rule "unchanged since 6.0.0"); none names 6.0.0 as the installed or current version.
  - `docs/releases/v6.1.0.md` and `CHANGELOG.md`: the task's items 1 and 2 (entries for #660 and #661, the release date; the two items in the "Other pull requests" row, "Changed" and "Related Issues").
- **Not changed, checked:** the retention paragraph of `installation.md` already says 90 days and "releases before 6.1.0 used 365"; it matches `retention.py` (`MIN_DAYS = 90`) and the run (90 written under the override, 365 and 500 kept, 7 raised).
- **Gaps found:** see the gap list, items 1 to 6.
- **Created:** none (no new user page was needed; `docs/testing/v6.1.0/` holds the run's own outputs).
- **Verification:** mechanical only (see "How this run was done"): the end-to-end run checks every number and command quoted in `upgrading.md` (counts against `git ls-tree v6.1.0`); a link check of the edited pages (`check_links.py`: only the not-yet-written report link was missing, now present); the 6.0.0, removed-name and count searches re-run after the edits.

## Workstream B — Technical documentation

Since `v6.0.0`: installer files `install_core.py` (#646: one import line added, so every line after it moved by +1), `install_keep.py`, `install_retired_data.py`, `install_ccsession.py`, `retention.py` (target 90); the new `session_keep.py`; the removal of nine skills and one command; `HOW-WE-WORK.md` (levels 4 to 6 removed: 360 lines instead of 385); `review-tiers.default.json`; the skill and agent text of `/sc:issue`; `tests/skills/test_review_severity_rule.py` and its fixtures.

- **Scanned:** `docs/developer-guide/`, `docs/architecture/`, `docs/reference/`, `docs/dev/`, `docs/swarm/`, `docs/user-guide/`, `README.md`. Staleness protocol: every `src/`, `tests/`, `docs/`, `scripts/` or `plugins/` citation with a line number was compared between the two tags with `check_citations.py` (adapted from the 6.0.0 run to tags v6.0.0 and v6.1.0, `.dev/issues/v61-post-release/check_citations.py`; 58 docs, 10 drifted citations, all in the orchestration reference). Citations into files removed by 6.1.0: none (`removed-files.txt` against `cited-paths.txt`). Citations of other kinds (`CHANGELOG.md:<line>`, `.github/...`, counts, fixture sizes) were checked by hand.
- **Stale claims reconciled (`[CODE-CONTRADICTED]` then fixed):**
  - `technical-architecture.md`: "35 slash commands" and "35 skill folders" are 34 and 26 (counts from the real install, transcript lines 560-562 of the run and `git ls-tree v6.1.0`).
  - `review-severity-rule.md`: fixture rows 140 and 125 are 58 and 25; the line ranges of checks (g), (h), (i) and (k) moved by -11 (and (g) lost five listed skills); "as of 6.0.0" and "line numbers are from tag v6.0.0" now say 6.1.0 and "unchanged since 6.0.0" (the rule text at `pragmatic.md:240-244` did not change: `output-styles/` is not in the delta); five `CHANGELOG.md` citations pointed at other text and were re-anchored.
  - `codegraph-integration.md`: four `CHANGELOG.md` citations (see release-integrity finding 5). No cited `src/` or `tests/` line moved between the tags.
  - `session-memory.md`: it said `/sc:reflect` "writes `reflect/handoff-{slug}-{timestamp}.md` once"; 6.1.0 removed that route and `sc-reflect-protocol/SKILL.md:588` says nothing writes them now. Corrected, with the new line numbers (`:581`, `:588`).
  - `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`: "24 of 35 command files carry `## Unattended mode`" (three places) is 23 of 34 at the tag (loop over `git show v6.1.0:<file>` in `.dev/issues/v61-post-release/`; `/sc:tdd` carried the section); `install_core.py` citations moved by +1 (`:27`, `:14-29`, `:70-72`, `:70-75`, `:94-105`, `:70`), `HOW-WE-WORK.md:396-406`, `:398-403` and `:400` are now `:350-360`, `:352-358` and `:354` (the "Orca coordination" section; re-anchored by what each citation says, not by a checker), `installation.md:497-504` is `:511-518`, and three `test_worker_contract.py` ranges moved by -16 or -42.
  - `documentation-index.md` and `SuperClaude-Developer-Guide-Commands-Skills-Agents.md`: "re-read at tag v6.0.0", "Upgrading to IronClaude 6.0.0" and "not part of 6.0.0" now say 6.1.0.
- **Gaps found:** see the gap list, items 7 to 11. One gap from 6.0.0 is closed: `docs/reference/nfr-conv-2-prose-determinism.md` (3 moved citations) was deleted by 6.1.0.
- **Created:** none.
- **Verification:** the same two scripts plus a re-read of every edited citation against the tagged file (for example `sed -n 931p tests/skills/test_worker_contract.py` for the re-anchored test ranges: both ends match the old text). The orchestration reference was not re-verified as a whole: its other citations have an unknown baseline (gap 8).

## Workstream C — Install & deploy (e2e-validated)

- **Surface class:** `package`. Evidence: `pyproject.toml` console scripts (`superclaude`, `ic`), `update.sh` (a three-line wrapper: `pipx install --force ./`, `superclaude install --force`, `make sync-dev`, `superclaude doctor`), no `install.sh` at the repository root, no VM runbook, no container build.
- **Install surface changed since 6.0.0:** yes (`git diff --stat v6.0.0 v6.1.0` over the installer files: `install_core.py`, `install_keep.py`, `install_retired_data.py`, `install_ccsession.py`, the ccsession skill's `retention.py` and new `session_keep.py`, `pyproject.toml` version), so the end-to-end run was **re-run, not carried forward**. `update.sh` is unchanged.
- **E2E target:** fresh `pipx` virtual environments installed from `git+https://github.com/IronbellyOrg/IronClaude@v6.1.0`, and throwaway homes `/tmp/ic6-e2e.<random>/<scenario>/home` started with `env -i` (no variable of the real session reaches a command), with a private pinned copy of the `claude` binary (2.1.328). The real `~/.claude`, `~/.local`, `~/.codegraph` and pipx were only read before and after: `REAL_HOME_UNCHANGED` (transcript line 2151). The throwaway root was deleted with a literal path.
- **Result:** **GREEN**, on the first full run of the adapted script (transcript line 2154, `script exit=0`). Exit codes (transcript line 2152): new-user `pipx` 0, `install` 0, `doctor --verbose` 0 (`✅ SuperClaude is healthy`), second `install` 0; upgrade from a genuine 6.0.0: 6.0.0 seed install 0, `pipx install --force` 0, `install --force` 0, doctor 1 while the edited `/sc:tdd` and the `task-builder` folder with an extra file were kept (`Missing command-required skill(s): tdd`; expected, documented) and 0 after the printed `rm` commands and after deleting the saved copies; second forced install 0, `update` 0; `./update.sh` from a clone 0.
- **Facts the run established** (used in the docs; the script checks the counts against `git ls-tree` of each tag and fails the run if they differ):

| | 6.0.0 seed | After 6.1.0 upgrade (edited `tdd`, `task-builder` kept) | After the two `rm` commands | Fresh 6.1.0 install | `./update.sh` from a clone |
|---|---|---|---|---|---|
| commands | 35 | 35 | 34 | 34 | 34 |
| agents | 48 | 48 | 48 | 48 | 48 |
| skills | 35 | 27 | 26 | 26 | 26 |
| core files | 12 | 12 | 12 | 12 | 12 |
| hook files | 18 | 18 | 18 | 18 | 18 |

  - The retire step printed `Removed skill` for 8 skills (`operational-guide`, `prd`, `readme`, `roadmap`, `task`, `tdd`, `tech-reference`, `tech-research`), `Kept /sc:tdd` (edited) and `Kept skill task-builder` (extra file `my-notes.txt`), each kept item with its exact `rm` command; a second forced install printed `No retired commands, skills or agents present.`
  - `install --force` saved 7 commands (`analyze`, which the run edited, plus `brainstorm`, `implement`, `recommend`, `reflect`, `troubleshoot` and `workflow`, which 6.1.0 changed), 1 rule file and 1 output style as `<name>.bak.<UTC time>`, plus 2 `settings.json` backups; an edited `CLAUDE.md` was overwritten with 0 copies (the same as 6.0.0).
  - Fresh install: none of the nine removed skills or `tdd.md` is installed; `/sc:task`, `/sc:validate-tests`, their two protocol skills and all eight `rf-*` agents are; the four `/sc:issue` templates end with `## Priority`, `## Fix approach`, `## Test plan`; the installed tier file is version 1.2.0 with `review-seat-5a/5b/5c`; `superclaude eval list` shows 15 suites and not `workflow_vs_task_builder`.
  - Removed groups: `superclaude roadmap --help` and `superclaude sprint --help` exit 2; `superclaude sweep --help` exits 0.
  - Retention: this host's managed settings set `cleanupPeriodDays` to 90, which equals the 6.1.0 target, so the installer wrote nothing and printed no warning; with `CCSESSION_MANAGED_SETTINGS_DIR` pointing at an empty folder the installer wrote 90, and `retention.py ensure` kept 365 and 500, raised 7 to 90 and left a file that is not JSON untouched (exit 3).
  - ccsession (#641): `ccsession --list`, `--list --agents`, `--classify` and `--prune` all answer with exit 0 in a home with no sessions. **This shows the options exist; it does not show the hiding of agent sessions or pruning, which need seeded sessions (gap 12).**
- **Updated/created scripts:** no install script needed a change. Created `c-e2e-run.sh` (adapted from the 6.0.0 script) and `c-e2e-transcript.txt` (its output, paths normalised, no secrets: scanned for token, key, password and bearer shapes; only the word "task" matched).
- **What the script does that the 6.0.0 one did not** (review findings of the 6.0.0 pull request were not repeated): `unset NOTRACK EXPECT_RC` at the top (a variable left in the caller's shell cannot hide a failing step); expected counts come from `git ls-tree` of the tags and are checked with `chk`; the retire step's lines, the saved `rm` commands, the version line, the doctor lines, the eval suite count, the installed templates and the tier file are checked with `chk`/`chkgrep`; the doctor exit code while an item is kept is checked against its own output instead of being assumed; the harness has two self-test modes (below); the pinned `claude` copy is kept.
- **Negative check of the harness (run once, evidence in `.dev/issues/v61-post-release/negative-check-*.txt`):** `bash docs/testing/v6.1.0/c-e2e-run.sh --selftest-red` runs one step that ends as expected and one that ends in 7 when 0 is expected: it printed `RESULT: RED: [sh -c exit 7 exit=7 want 0]` and exited 1, and it did so with `NOTRACK=1 EXPECT_RC=5` set in the caller's environment (the `unset` works). `--selftest-expected-nonzero` runs a step declared as meant to end in 7: `RESULT: GREEN`, exit 0. Both touch nothing outside a temporary folder and need no network.

### E2E transcript

The full transcript is `docs/testing/v6.1.0/c-e2e-transcript.txt` (2,155 lines; run it again with `bash docs/testing/v6.1.0/c-e2e-run.sh` from the repository root). Scenario markers: scenario 1 at line 11, scenario 2 at line 942, scenario 3 at line 1845, summary at line 2152, final lines `RESULT: GREEN` and `script exit=0` (the last line is added by the command that ran the script, not by the script). It is the only full run of this script: there was no earlier red run to keep.

## Workstream D — User-facing e2e test guides

**Out of scope by decision 6.1.0-5** (the same scope as 6.0.0: A, B and C only). No feature surface was scanned for guides, none were created, and the coverage figure is not computed. Consequence: the v5.0.0 user guides under `docs/testing/v5.0.0/user/` (D01 to D16) are unchanged historical records, and some of them describe commands that 6.0.0 or 6.1.0 removed (for example D10 sprint, D11 roadmap and tasklist, D13 prd, portify and cleanup-audit, and anything that used `/task` or `/sc:tdd`); the capabilities added since 5.0.0 have no hand-test guide.

## Workstream E — Sysop-facing e2e test guides

**Out of scope by decision 6.1.0-5.** The sysop surface was not re-scanned. For the record: the v5.0.0 run found two sysop capabilities (ccsession tier policy and model-data publishing; guides E01 and E02, unchanged); 6.0.0 added sysop-facing items without a guide (`superclaude observe`, `superclaude issue-watch`, `superclaude issue-pipeline`, the launch-level hooks, `WORKER-CONTRACT.md`); 6.1.0 adds `ccsession --prune --apply` (it deletes sessions) and the retention target. This is a deferral, not a statement that no sysop surface exists.

---

## Regression gate (baseline and after)

Command: `pytest -n auto --ignore=tests/cli/test_verify_sync_hooks.py` (no `--maxfail`), plus `make lint`, `uv run ruff format --check src/ tests/` (ruff 0.15.20, pinned in the virtualenv) and `make verify-sync`. The branch changes documentation only: no file under `src/` or `tests/` is in the diff.

| Check | Before the first edit (`f7dcf031d`, the base) | After (all edits, report and manifest in place) |
|---|---|---|
| Full suite, parallel | 26 failed, 7 errors, 22,580 passed, 69 skipped (12 min 18 s, host under heavy load) | 2 failed, 22,611 passed, 69 skipped (5 min 40 s) |
| The failures re-run | the 10 files that held them, run serially (`-n 0`): 4,995 passed, 3 skipped, 0 failed | the 2 failed tests (`tests/cli/eval/test_schema_id_rejection.py`), run alone: 20 passed |
| `make lint` | pass | pass |
| `ruff format --check src/ tests/` | 983 files already formatted | 983 files already formatted |
| `make verify-sync` | pass | pass |
| `git diff --check` | not applicable | clean |

- **Reading.** No failure is new and none comes from this branch. The baseline failures are in `tests/hooks/` (launch-job-identity, launch-level-guard and pre-push), `tests/skills/test_issue_l2_install.py`, `tests/skills/test_issue_orca_worktree.py`, `tests/cli/eval/`, `tests/observe/`, `tests/pr_submit/`, `tests/swarm/` and one `tests/unit/test_ccsession_tag.py` test. They pass when their files run alone, which points to host load: other sessions were running full suites on the same host (the 15-minute load average read 25.6 right after the baseline and 4.7 before the after run). That is the likely cause, not a proven one. The two failures after are the `/tmp` scratch-folder tests that the merged pull request #661 also names as flaky; they pass alone. The 31 more passing tests after are the baseline's load failures passing.
- **The eight known `test_ccsession_tag.py` failures** of the task prompt (a LiteLLM shim on 127.0.0.1:4555) did not appear in either full run here (one ccsession test failed in the baseline and passed alone).
- Logs: `.dev/issues/v61-post-release/baseline-*.txt` and `.../after/` (not committed).

## How this run was done

- **Inline, no subagents.** The task and the project's rules forbid launching agents, so the skill's scanner, consolidator and writer roles were all done by this one session: scans were `rg`, `git diff v6.0.0 v6.1.0`, `git show <tag>:<path>`, `git ls-tree`, `superclaude --help` and the real install runs. The skill's optional task-decomposition and reflection tooling was not used.
- **The consolidated plan was written to disk before the first edit** (`.dev/issues/v61-post-release/CONSOLIDATED-PLAN.md`: delta categorized, required edits, expected counts). That fixes the process gap the 6.0.0 report admitted. The audit log and the RUN header, however, were opened after Wave 2 and after the install run had started, not in Wave 0 as the skill says; the RUN header is the first line of `audit.log`, but it carries a later time than the work it precedes. Recorded here rather than back-dated.
- **Verification was mechanical, not independent.** A fresh-context reviewer would need an agent, which was not allowed. What was done instead: every number and command in `upgrading.md` was taken from or checked against the end-to-end transcript; the run itself checks the installed counts against the tagged tree; a citation checker and a link checker ran over the edited pages; the 6.0.0, removed-name and count searches were re-run after the edits; the full suite and the lint, format and sync checks ran before and after. Treat A and B as "checked by their author with tools", not "reviewed". The pull request's Augment and Codex reviews are the first independent read.
- **Evidence kept but not committed** (`.dev/issues/v61-post-release/`): the delta file list, the plan, the scans, the baseline and after logs, the first (and only full) run's raw output and the files of its throwaway root, the harness negative checks, the citation and link checker outputs, the process notes.
- **Tools that pushed back:** the freshness hook blocked edits to files not read in the session (correctly, each time, fixed by a read); the bare-python hook blocked `.venv/bin/python` in a Bash call (correctly), so the 6.0.0 seed interpreter call lives inside the script file as the task described.
- **Shared host.** Other sessions ran test suites at the same time. The baseline full run therefore had 26 failures and 7 errors, all load-sensitive; see the regression section.

## Honest gap list (all workstreams)

| # | Workstream | Gap | Evidence | Proposed remedy |
|---|---|---|---|---|
| 1 | A | `observe`, `review` and `issue-pipeline` have only a listing and the `--help` options, no task-oriented guide | `docs/user-guide/cli-groups.md` | Write a guide per group when owners say who uses them (carried from 6.0.0) |
| 2 | A | The new ccsession options (`--agents`, `--mark`, `--classify`, `--prune`) are documented in the skill's `README.md` and `SKILL.md` only; no `docs/` user page names them (`installation.md` mentions `--prune` once) | `src/superclaude/skills/ccsession-tag/README.md:300-345`; `docs/getting-started/installation.md:372` | Add a short ccsession section to `docs/user-guide/session-management.md` |
| 3 | A, B | Docs for `/sc:issue` (beyond the new template sentence), ccsession 6.0.0 changes, Ponytail and pr-submit conflicts exist but were not checked against the code line by line | manifest cells `present-unverified` | A follow-up check of those four (carried) |
| 4 | A | `/sc:code-review` named in `docs/swarm/README.md`, `lens-catalog.md`, `user-guide.md`, `release-notes-v1.md`; `/sc:create` and `/sc:review` in `docs/user-guide/agents.md`; `/sc:close` in the developer guide: none is a shipped command (same at 6.0.0 and 5.0.0) | `.dev/issues/v61-post-release/scan-unshipped-commands.txt` | Replace with shipped commands or mark as examples (carried) |
| 5 | A | CHANGELOG `[6.0.0]` has no entries for `observe`, `review`, `issue-watch`, `issue-pipeline` and `/sc:issue` itself | `CHANGELOG.md` `[6.0.0]` section | Owner to approve entries; this task allowed only #660 and #661 (carried) |
| 6 | A | The 6.0.0 release notes' manual-validation numbers (39/37/37) differ from the 6.0.0 run (38/36/36) and its Known Issues says `upgrading.md` is stale | `docs/releases/v6.0.0.md`; `docs/testing/v6.0.0/post-release-report.md` | Orchestrator to correct or accept; `docs/releases/v6.0.0.md` was off limits here (carried) |
| 7 | B | No technical doc for `superclaude observe` (13 source files) | `src/superclaude/cli/observe/` | Write a design or reference note (carried) |
| 8 | B | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`: this run fixed the 10 citations and 3 counts that differ between v6.0.0 and v6.1.0, but its other citations have an unknown baseline, and lines 317 and 2197 still say "25 command files carry `## Unattended mode`" (24 at 6.0.0, 23 now) as research-time counts | `check_citations.py` output; the document's own dated notes | Re-verify the document against its own baseline commit (carried, narrowed) |
| 9 | B | `docs/developer-guide/git-standards-protocols.md` is another project's document (v5.0.0 deferred item 71) and cites `scripts/check-secrets.sh`, `validate-commit-msg.sh`, `check-env-sync.sh`, which do not exist here | `docs/testing/v5.0.0/post-release-manifest.json`; `cited-paths.txt` | Remove or replace (carried) |
| 10 | B | Root `VERSION` file says `3.7`; `pyproject.toml` says 6.1.0 | `VERSION`; `scripts/build_superclaude_plugin.py:25` | Update or delete (carried) |
| 11 | B | The citation checker used by this and the 6.0.0 run lives in a worktree evidence folder and matches only `src/`, `tests/`, `docs/`, `scripts/` and `plugins/` paths, so `CHANGELOG.md:<line>` and `.github/` citations were checked by hand | `.dev/issues/v61-post-release/check_citations.py` | Move it into `scripts/` with bare `CHANGELOG.md` and `.github/` patterns |
| 12 | C | ccsession agent-session hiding and `--prune --apply` were not run with seeded sessions (the run's home has none) | transcript lines 873-897 | Seed one agent-marked and one human session in a later run |
| 13 | C | The retention write branch could only be shown with `CCSESSION_MANAGED_SETTINGS_DIR` set (host managed value 90 equals the target, so the installer writes nothing here) | transcript lines 847-875 | None needed; note for readers (carried) |
| 14 | C | If `claude` is replaced by its auto-updater during `superclaude install`, the codegraph step reports `Claude CLI is unavailable` and exits 1 (seen in the 6.0.0 run; not seen in this one because the script pins a private copy) | `docs/testing/v6.0.0/post-release-report.md` | Optional: retry once in the installer (carried) |
| 15 | C | An offline install and upgrade were not tried; an upgrade straight from 5.0.0 or 4.x to 6.1.0 was not run | scope | Try in a later release (carried, extended) |
| 16 | D | No hand-test guides for the 6.0.0 and 6.1.0 changes; v5.0.0 guides D10, D11, D13 describe removed commands | decision 6.1.0-5 | Deferred by decision |
| 17 | E | No sysop guides for `observe`, `issue-watch`, `issue-pipeline`, launch-level hooks, `WORKER-CONTRACT.md`, `ccsession --prune` | decision 6.1.0-5 | Deferred by decision |

Closed since 6.0.0: `nfr-conv-2-prose-determinism.md` (3 moved citations) no longer exists.

## Artifacts

- Report: `docs/testing/v6.1.0/post-release-report.md`
- Manifest: `docs/testing/v6.1.0/post-release-manifest.json`
- Audit log: `docs/testing/v6.1.0/audit.log`
- Index of the folder: `docs/testing/v6.1.0/README.md`
- E2E script and transcript: `docs/testing/v6.1.0/c-e2e-run.sh`, `docs/testing/v6.1.0/c-e2e-transcript.txt`
- Test guides: none (D and E out of scope, decision 6.1.0-5)
- Edited docs: see Workstreams A and B and `git diff --stat`
- Evidence, not committed: `.dev/issues/v61-post-release/` (baseline and after logs, the raw run output, the harness negative checks, citation and link checks, scans, `PROCESS-NOTES.md`)

## Suggested next step

Review the gap list, then run the review loop of the pull request on the fork (never the upstream). The pull request is opened with `gh pr create --repo IronbellyOrg/IronClaude --base integration --head clayphi/v61-post-release` because `/sc:pr-submit` has no `--base` or `--repo` flags, and its monitor loop is run by hand (re-trigger Augment with the comment `augment review` and Codex with `@codex review` after each push). Do not stage `.claude/` and do not commit `.dev/issues/v61-post-release/` (the evidence folder); everything under `docs/testing/v6.1.0/` is committed. Do not merge: the orchestrator decides.
