<!-- SC:POST-RELEASE:RESULT
status: partial
run_mode: additive
install_surface_class: package
report_path: /home/coder/workspaces/worktrees/IronClaude/v6-post-release/docs/testing/v6.0.0/post-release-report.md
manifest_path: /home/coder/workspaces/worktrees/IronClaude/v6-post-release/docs/testing/v6.0.0/post-release-manifest.json
workstream_results: {"A":{"updated":14,"created":1,"gaps":5,"verified":true},"B":{"updated":6,"created":0,"gaps":5,"verified":true},"C":{"updated":0,"created":2,"gaps":3,"verified":true},"D":{"updated":0,"created":0,"gaps":1,"verified":false},"E":{"updated":0,"created":0,"gaps":1,"verified":false}}
c_e2e_result: green
gap_list: [{"workstream":"A","gap":"observe, review and issue-pipeline have a listing only","evidence":"docs/user-guide/cli-groups.md","remedy":"write a guide per group"},{"workstream":"A","gap":"docs for /sc:issue, ccsession changes, Ponytail, pr-submit conflicts not checked line by line","evidence":"manifest present-unverified cells","remedy":"follow-up check"},{"workstream":"A","gap":"/sc:code-review, /sc:create, /sc:review named in docs but not shipped (same at v5.0.0)","evidence":"docs/swarm/README.md:67; docs/user-guide/agents.md:912,928","remedy":"replace or mark as examples"},{"workstream":"A","gap":"CHANGELOG 6.0.0 lacks entries for observe, review, issue-watch, issue-pipeline, /sc:issue","evidence":"CHANGELOG.md [6.0.0]","remedy":"owner to approve entries"},{"workstream":"A","gap":"release notes manual-validation numbers differ from this run; Known Issues says upgrading.md is stale","evidence":"docs/releases/v6.0.0.md; transcript 1197-1199, 1537-1539","remedy":"orchestrator to correct or accept"},{"workstream":"B","gap":"no technical doc for superclaude observe","evidence":"src/superclaude/cli/observe/","remedy":"write a design or reference note"},{"workstream":"B","gap":"orchestration reference: 120 citations differ between tags, baseline unknown","evidence":"check_citations.py output","remedy":"re-verify against its own baseline"},{"workstream":"B","gap":"nfr-conv-2 note: 3 moved citations, pre-existing","evidence":"docs/reference/nfr-conv-2-prose-determinism.md:131,152,156","remedy":"re-anchor or retire"},{"workstream":"B","gap":"git-standards-protocols.md is another project's doc (v5.0.0 item 71)","evidence":"docs/developer-guide/git-standards-protocols.md","remedy":"remove or replace"},{"workstream":"B","gap":"root VERSION file says 3.7, pyproject says 6.0.0","evidence":"VERSION; scripts/build_superclaude_plugin.py:25","remedy":"update or delete"},{"workstream":"C","gap":"retention write branch shown only with CCSESSION_MANAGED_SETTINGS_DIR (host managed value 90)","evidence":"transcript 860-878","remedy":"none needed"},{"workstream":"C","gap":"installer exits 1 when claude is replaced by its auto-updater mid-run; rerun succeeds","evidence":"evidence c-e2e-run*-transcript.txt","remedy":"optional installer retry"},{"workstream":"C","gap":"offline install and upgrade not tried","evidence":"scope","remedy":"try in a later release"},{"workstream":"D","gap":"no hand-test guides for 6.0.0 changes; v5.0.0 guides D10, D11, D13 describe removed commands","evidence":"decision 6.6","remedy":"deferred by decision"},{"workstream":"E","gap":"no sysop guides for observe, issue-watch, issue-pipeline, launch-level hooks, WORKER-CONTRACT.md","evidence":"decision 6.6","remedy":"deferred by decision"}]
duration_sec: 2889
-->

# Post-Release Report — `v6.0.0`

- **Version / tag:** `v6.0.0` (`v6.0.0`, annotated tag object `bf2475fd56c3520c5819a8c36ff3c2fb8be98293` on commit `3f3b34a26280fd3fd64649f5d010f874b1905b65`)
- **Previous release:** `v5.0.0`
- **Run mode:** `additive`: evidence a prior manifest exists at `docs/testing/v5.0.0/post-release-manifest.json` (the v5.0.0 run, ground-up). The delta is `v5.0.0..v6.0.0`: 1,436 changed paths outside `.dev/` (saved in the run's evidence folder), of which the removals of six CLI groups, twelve commands and five skills and the additions of `/sc:issue`, `/sc:sweep`, three issue-worker agents, `WORKER-CONTRACT.md`, five new CLI groups, four hooks and the installer changes (#633, #480, retention) touch the external surface.
- **Install-surface class:** `package`
- **Date:** 2026-11-18
- **Branch:** `clayphi/v6-post-release` (from `origin/integration` at `847cccc1a`; the tree is identical to the tag, checked with `git diff v6.0.0 HEAD`)

## Summary

The user and technical documentation was brought in line with the tagged 6.0.0 tree: 14 files edited (README, installation, upgrading, quick start, two reference pages, six user-guide pages, the release notes, the CHANGELOG entry for #480), 6 developer-guide notes re-anchored or corrected, and one page created (`docs/user-guide/cli-groups.md`, the five `superclaude` groups that had no documentation). The install path was run for real in throwaway homes and is **green**: a new user (`pipx install` from the tag), an upgrade from a genuine 5.0.0 (35 commands, 48 agents, 35 skills after; the retire step removed 11 commands and 4 skills and kept the 1 edited command and 1 edited skill), and `./update.sh` from a clone; the real home was not touched. Workstreams D and E were skipped by decision 6.6. The honest bottom line: scoped work is done, but 5 user-doc gaps, 5 technical-doc gaps and 3 install notes remain (see the gap list), and the release notes' own manual-validation numbers differ from this run.

## Scope of this run

Authorized by the owner on 2026-11-18 through the coordinating session; recorded in the task prompt `.dev/releases/current/v6.0.0/prompts/post-release.md` (decision 6.6: the recommended scope).

- **In scope:** A (user documentation), B (technical documentation), C (install and deploy scripts, proven by a real end-to-end run: install and upgrade from 5.0.0, throwaway home only).
- **Out of scope by decision 6.6:** D (user-facing human-test guides) and E (sysop-facing human-test guides). No new hand-test guides were written for the removed or added items, and nothing under `docs/testing/v5.0.0/` was edited.
- **Also required by the task (not part of the skill):** the CHANGELOG entry for #480; the release-notes edits (scope decision 6.3 with issue #647, and the saved-copies sentence in Migration step 3); `docs/getting-started/upgrading.md` brought to 6.0.0 with the retire-step section kept; and a search for 5.0.0 used as the current version.
- **Not touched, by instruction:** `docs/testing/v5.0.0/`, `docs/designs/`, `docs/releases/v5.0.0.md`, every other CHANGELOG entry.

## Release-integrity findings

1. **Tag and lineage (OK).** `v6.0.0` is an annotated tag (`git cat-file -t v6.0.0` prints `tag`), on the master merge commit `3f3b34a2`, and an ancestor of `origin/master`. The GitHub release exists and is neither draft nor pre-release. `pyproject.toml` says 6.0.0 and `superclaude --version` prints `SuperClaude, version 6.0.0` (transcript line 28).
2. **Tag equals working tree (OK).** `git diff v6.0.0 HEAD` is empty, so scanning the working tree was the same as scanning the tag.
3. **Root `VERSION` file says `3.7` (finding).** Last changed 2026-03-23; it disagrees with `pyproject.toml`. Only `scripts/build_superclaude_plugin.py` reads it. Not fixed (outside the surface this run touches); recommend deleting or updating it.
4. **Release notes' manual-validation numbers differ from this run (finding).** `docs/releases/v6.0.0.md` says the 5.0.0 files were 45 commands, 39 skills and 45 agents and that 37 commands and 37 skills were left. This run (genuine 5.0.0 install, transcript scenario 2) laid down 45 commands, 38 skills and 45 agents and left 36 commands and 36 skills (35 shipped plus one kept edited command, 35 shipped plus one kept edited skill folder). Not edited: the task allows only two edits to that file, and the notes describe the orchestrator's own run.
5. **Release notes' Known Issues is now out of date (finding).** It says `docs/getting-started/upgrading.md` still describes 5.0.0; this run fixed that.
6. **CHANGELOG `[6.0.0]` is incomplete for the new surface (finding).** It has no entries for the `observe`, `review`, `issue-watch` and `issue-pipeline` groups or for the `/sc:issue` command itself (only for its workers), and `WORKER-CONTRACT.md` appears only through the WC-16 rule of the sweep entry. The task allowed one new entry (#480) only.

## Coverage matrix (headline)

Delta capabilities only (the full 61-row matrix is in `post-release-manifest.json`; the v5.0.0 rows are carried forward there). D and E columns are out of scope (decision 6.6) and are left out here.

| Capability | User doc (A) | Tech doc (B) | Install (C) |
|---|---|---|---|
| `superclaude --version` prints 6.0.0 | ✅ updated | ✅ | ✅ run |
| `install` / `update` / `update.sh` (#633 retire step, counts 12/35/48/35) | ✅ updated (`upgrading.md`, `installation.md`, `README.md`) | ✅ updated (`technical-architecture.md`) | ✅ run (all three paths) |
| Saved copies `<name>.bak.<UTC time>` (#480) | ✅ created (`upgrading.md`, `installation.md`, release notes) | ✅ (CHANGELOG entry; `review-severity-rule.md` re-anchored) | ✅ run (27 + 5 + 1 copies) |
| `cleanupPeriodDays` 365 retention | ✅ created (`installation.md`) | ⚠️ unverified (`retention.py` docstring only) | ✅ run (managed value wins; override run writes 365) |
| Removed CLI groups, commands, skills | ✅ current (cleanup PRs; `upgrading.md` Step 6 added) | ✅ | ✅ run (removed group exits 2) |
| `superclaude sweep` / `/sc:sweep` | ✅ current (`commands.md`, new `cli-groups.md`) | ✅ (developer guide) | n/a |
| `superclaude observe` | ✅ created (`cli-groups.md`) | ❌ missing | n/a |
| `superclaude issue-watch` | ✅ created (`cli-groups.md`) | ⚠️ designs only (historical) | n/a |
| `superclaude issue-pipeline`, `superclaude review` | ⚠️ listing only (`cli-groups.md`) | ⚠️ designs and one reference page | n/a |
| `/sc:issue` + `issue-worker-t1..t3` | ⚠️ present, unverified | ⚠️ present, unverified | n/a |
| Hooks: bare-python block, Orca-agent gate, launch-level guard | ✅ created (`freshness-hooks.md`) | ✅ updated (`technical-architecture.md`) | ✅ installed (18 hook files) |
| `WORKER-CONTRACT.md` core file | ✅ (`technical-architecture.md`, counts) | ✅ | ✅ installed |
| ccsession 6.0.0 changes, Ponytail, pr-submit conflicts | ⚠️ present, unverified | ⚠️ present, unverified | ✅ ccsession installed, Ponytail plugin installed |

✅ present-and-current (updated or created this run) · ⚠️ present but not checked against the code this run, or only partly covered · ❌ missing · n/a not applicable

---

## Workstream A — User documentation

Since `v5.0.0`: the cleanup PRs (#615 to #633) had already rewritten or deleted the user pages for the removed groups, commands and skills, so a search of `README.md`, `docs/getting-started/`, `docs/user-guide/`, `docs/guides/`, `docs/reference/`, `docs/swarm/`, `docs/mcp/`, `docs/eval/` for the removed names found stale hits only in `docs/getting-started/upgrading.md` and two historical lines of `KNOWLEDGE.md` (left as records). What was stale was the version, the counts and the installer behaviour.

- **Scanned:** the files above, by search for removed CLI groups, removed slash commands, removed skills, `5.0.0` as the current version, count claims, and every `/sc:<name>` token against the 35 shipped commands.
- **Updated:**
  - `docs/getting-started/upgrading.md`: title, intro, Step 1 (which files are saved and which are not), install line `@v6.0.0`, command table (retire column), counts (12 core files, 35 commands, 48 agents, 35 skills), a "Saved copies of changed files" section, a real retire-step output excerpt, Step 6 table for 5.0.0 to 6.0.0, links; the retire-step section from PR #633 is kept.
  - `docs/getting-started/installation.md`: badge and version line; the `--force` warning (it said "keeps no backup"; commands, rules and output styles are now saved first); a "Conversation retention" paragraph (`cleanupPeriodDays`).
  - `README.md`: "Upgrading to 6.0.0" with the tag URL and the saved-copies note; install description; two "audit" mentions of a removed CLI; documentation map entry.
  - `docs/getting-started/quick-start.md`, `docs/reference/common-issues.md`, `docs/reference/troubleshooting.md`: version output `6.0.0` and link text.
  - `docs/user-guide/agents.md` (48 agent files; issue-worker agents), `codegraph.md` and `modes.md` (version wording), `freshness-hooks.md` (four hooks added since 5.0.0), `flags.md` and `how-we-work.md` (both said `--force` keeps no backup; commands, rules and output styles are now saved first), and the matching sentence in `docs/reference/troubleshooting.md`.
  - `docs/releases/v6.0.0.md`: scope decision 6.3 section (issue #647) and Migration step 3 (saved copies).
  - `CHANGELOG.md`: one `[6.0.0]` entry for #480, read from the pull request and `install_keep.py`.
- **Gaps found:** see gap list items 1 to 5.
- **Created:** `docs/user-guide/cli-groups.md`, derived from `superclaude --help` of each group.
- **Where this run differs from the task's wording:** item 2b of the task says `install --force` saves "every installed file that differs". The code (`install_commands.py:54-75`, `install_user_setup.py:68-126`) and PR #480 ("Not in this PR") limit it to commands, rules and output styles; core files, agents, skills, hooks and templates are overwritten without a copy, which the end-to-end run confirmed (an edited `CLAUDE.md` was overwritten, 0 copies). The docs and release notes say the narrower, verified thing.
- **Verification:** mechanical only (see "How this run was done"): the end-to-end run checks every number and command quoted in `upgrading.md`; a link check of the edited and created pages; no `5.0.0`-as-current hit remains outside historical records.

## Workstream B — Technical documentation

Since `v5.0.0`: installer files `install_keep.py`, `install_retired_*.py`, `install_user_setup.py`, `main.py`, `doctor.py`, `retention.py`; the hook set; the output-style rule text; the core files; and the removal of the roadmap, tasklist, sprint, prd, cleanup-audit and cli-portify code.

- **Scanned:** `docs/developer-guide/`, `docs/dev/`, `docs/architecture/`, `docs/reference/`, `docs/swarm/`. Staleness protocol: every `path:line` citation in the five 5.0.0-era notes was compared between the two tags with `.dev/issues/v6-post-release/check_citations.py` (first cited line equal or not), then the unprefixed ones by hand.
- **Stale claims reconciled (`[CODE-CONTRADICTED]` then fixed):**
  - `technical-architecture.md`: "45 agent files / 45 slash commands / 38 skills / 11 core files" are 48 / 35 / 35 / 12 (counts from the real install, transcript lines 579 to 583); `WORKER-CONTRACT.md` and five hook scripts missing from the tree.
  - `review-severity-rule.md`: the S1, S2 and S5 rule text, its line numbers (`pragmatic.md` 225-229 is now 240-244), "ten-file set" (eleven), the fixture row counts (140 cap rows and 125 sweep rows by `old:` keys; the note said 140 and 137), guard-test section ranges (+18 after section (c)), `hooks.json`, `install_user_setup.py`, CHANGELOG and CI line numbers, and "a plain install overwrites" (now saves copies).
  - `codegraph-integration.md`: eight citation ranges moved (`graph.md`, `sc-graph-protocol`, `sc-impact-protocol`, `doctor.py`, `main.py`, two tests). Most `main.py` ranges had already been updated for step 10 by #633.
  - `session-memory.md`: ten citations into `sc-reflect-protocol` and `sc-task-protocol` moved by 2 to 53 lines.
  - `documentation-index.md`: "5.0.0 install" links, and "one-release fallback to the old Serena folder" (removed in 6.0.0).
  - `SuperClaude-Developer-Guide-Commands-Skills-Agents.md`: "The plugin system is planned for v5.0" (the project's `CLAUDE.md` says a later release, not 6.0.0).
- **Gaps found:** see gap list items 6 to 10.
- **Created:** none.
- **Verification:** the citation checker's remaining output for these notes was reviewed by hand (several "drifts" were false positives because the note had already been updated after 5.0.0). `SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`, written after 5.0.0 with an unknown baseline, was not touched.

## Workstream C — Install & deploy (e2e-validated)

- **Surface class:** `package`. Evidence: `pyproject.toml` console scripts (`superclaude`, `ic`), `update.sh` (a three-line wrapper), no `install.sh` at the repository root (the only `install.sh` is inside the ccsession skill), no VM runbook, no container build.
- **Install surface changed since 5.0.0:** yes (`git diff --stat v5.0.0 v6.0.0` over the installer files, `main.py`, `doctor.py` and `retention.py`: 13 files, +1,114 and -93 lines, including the new retire step, saved copies and retention), so the end-to-end run was **re-run, not carried forward**. `update.sh` and `pyproject.toml` packaging are unchanged apart from the version.
- **E2E target:** fresh `pipx` virtual environments installed from `git+https://github.com/IronbellyOrg/IronClaude@v6.0.0`, and throwaway homes `/tmp/ic6-e2e.<random>/<scenario>/home` started with `env -i` (no variable of the real session reaches a command), with a private pinned copy of the `claude` binary. The real `~/.claude`, `~/.local`, `~/.codegraph` and pipx were only read before and after: `REAL_HOME_UNCHANGED` (transcript line 2199). The throwaway root was deleted with a literal path.
- **Result:** **GREEN.** Exit codes (transcript line 2200): new-user `pipx` 0, `install` 0, `doctor --verbose` 0 (`✅ SuperClaude is healthy`), second `install` 0; upgrade from a genuine 5.0.0: 5.0.0 seed install 0, `pipx install --force` 0, `install --force` 0, doctor 1 while the kept `roadmap` command existed (expected, documented) and 0 after the printed `rm` commands and after deleting the saved copies; second forced install 0, `update` 0; `./update.sh` from a clone 0.
- **Facts the run established** (used in the docs):

| | After 6.0.0 fresh install | 5.0.0 seed | After upgrade (edited `roadmap`, `sc-tasklist-protocol` kept) | After the two `rm` commands |
|---|---|---|---|---|
| commands | 35 | 45 | 36 | 35 |
| agents | 48 | 45 | 48 | 48 |
| skills | 35 | 38 | 36 | 35 |
| core files | 12 | 11 | 12 | 12 |
| hook files | 18 | 13 | 18 | 18 |

  - The retire step printed `Removed` for 11 commands and 4 skills, `Kept` for the edited `/sc:roadmap` and the skill folder with an extra file, each with its exact `rm` command; a second run printed `No retired commands, skills or agents present.`
  - `install --force` saved 27 commands, 5 rule files and 1 output style as `<name>.bak.<UTC time>`, plus 2 `settings.json` backups; an edited `CLAUDE.md` was overwritten with 0 copies. A second forced install added only a `settings.json` backup. Deleting the copies with the documented `find ... -delete` left 0 and `doctor` stayed healthy.
  - Removed group: `superclaude roadmap --help` exits 2 (`No such command`); `superclaude sweep --help` exits 0.
  - Retention: this host's managed settings set `cleanupPeriodDays` to 90, so the installer wrote nothing and printed its warning; with `CCSESSION_MANAGED_SETTINGS_DIR` pointing at an empty folder the installer wrote 365, `retention.py ensure` kept 500, raised 7 to 365 and left a file that is not JSON untouched.
- **Updated/created scripts:** no install script needed a change. Created `c-e2e-run.sh` (the run) and `c-e2e-transcript.txt` (its output, paths normalised, no secrets: scanned for token, key and password shapes).
- **Harness problem found and fixed (not a product defect):** three earlier full runs are kept in the evidence folder. In each of them one installer call (the 5.0.0 seed install in the first, the first 6.0.0 `superclaude install` in the other two) printed `Prerequisites: Claude CLI is unavailable` and exited 1, because Claude Code's own auto-updater replaced the shared `claude` binary at that moment. The package directory time stamps match two of the three failures to the second (17:05:36 and 17:13:59); the first failure has no time stamp evidence. The script now pins a private copy of the binary. The installer's behaviour in that case matches what the docs say (the codegraph step needs `claude`; exit 1; rerun).

### E2E transcript

The full transcript is `docs/testing/v6.0.0/c-e2e-transcript.txt` (2,201 lines; run it again with `bash docs/testing/v6.0.0/c-e2e-run.sh` from the repository root). Scenario markers: scenario 1 at line 10, scenario 2 at line 921, scenario 3 at line 1884, summary at line 2200.

## Workstream D — User-facing e2e test guides

**Out of scope by decision 6.6** (the owner accepted the recommended scope: A, B and C only). No feature surface was scanned for guides, none were created, and the coverage figure is not computed. Consequence: the v5.0.0 user guides under `docs/testing/v5.0.0/user/` (D01 to D16) are unchanged historical records and some of them describe commands that 6.0.0 removed (for example D10 sprint, D11 roadmap and tasklist, D13 prd, portify and cleanup-audit); the new 6.0.0 capabilities have no hand-test guide.

## Workstream E — Sysop-facing e2e test guides

**Out of scope by decision 6.6.** The sysop surface was not re-scanned. For the record: the v5.0.0 run found two sysop capabilities (ccsession tier policy and model-data publishing; guides E01 and E02, unchanged), and 6.0.0 adds sysop-facing items that have no guide: `superclaude observe`, `superclaude issue-watch`, `superclaude issue-pipeline`, the launch-level hooks and `WORKER-CONTRACT.md`. This is a deferral, not a statement that no sysop surface exists.

---

## Regression gate (baseline and after)

Command: `pytest -n auto --ignore=tests/cli/test_verify_sync_hooks.py` (28 CPUs, no `--maxfail`), plus `make lint`, `ruff format --check src/ tests/` (ruff 0.15.20) and `make verify-sync`. The branch changes documentation only (no file under `src/` or `tests/`).

| Check | Before the first edit (`847cccc1a`) | After (rebased on `ffb378630`, the head of the PR) |
|---|---|---|
| Full suite, parallel | 13 failed, 22,688 passed, 70 skipped, 1 xpassed (9 min) | 9 failed, 22,694 passed, 70 skipped, 1 xpassed (5 min 52 s) |
| The failures re-run one at a time | the 13 pass; the known test `test_same_content_is_true_only_for_identical_readable_files` fails alone (1 failed, 26 passed) | the 9 pass, with `tests/cli/test_install_keep.py` (25 passed) |
| `make lint` | pass | pass |
| `ruff format --check src/ tests/` | 984 files already formatted | 984 files already formatted |
| `make verify-sync` | pass | pass |
| `git diff --check` | not applicable | clean |

- **Reading.** No failure is new: every failure after is in the baseline's list of 13, and they are load-sensitive (eight ccsession Ctrl+C and question-timing tests, one eval no-write test). The known failure of the task prompt passed under `-n auto` and failed alone before; after rebasing onto #646 (the fix by another agent) it passes in both modes. The 6 extra passing tests come from #646 (+2) and from the baseline having failed 4 more tests under load.
- **Baseline used `.venv/bin/python -m pytest`; the after runs used `uv run pytest`.** Same interpreter and packages.
- Logs: `.dev/issues/v6-post-release/baseline/` and `.../after/` (not committed).

## How this run was done

- **Inline, no subagents.** The task and the project's rules forbid launching agents, so the skill's scanner, consolidator and writer roles were all done by this one session: scans were `rg`, `git diff v5.0.0 v6.0.0`, `git show <tag>:<path>`, `superclaude --help` and the real install runs. The skill's optional task-decomposition and reflection tooling was not used.
- **Verification was mechanical, not independent.** A fresh-context reviewer would need an agent, which was not allowed. What was done instead: every number and command in `upgrading.md` and the release notes was checked against the end-to-end transcript; a citation checker (`check_citations.py`) and a link checker (`check_links.py`) ran over the edited notes; the `5.0.0`, removed-name and "keeps no backup" searches were re-run after the edits; the full test suite and the lint, format and sync checks ran before and after. Treat A and B as "checked by their author with tools", not "reviewed".
- **The consolidated plan was not written to disk before the first edits.** The required items came straight from the task, and the scan results were held in the session; the gap list below is the plan's residue. The skill says nothing is created before the plan exists; this run did not meet that gate for the first edits (CHANGELOG, release notes, `upgrading.md`).
- **Evidence kept but not committed** (`.dev/issues/v6-post-release/`): the delta file list, baseline and after logs, three earlier end-to-end transcripts, the `--help` captures, the citation and link check outputs, the manifest builder, `PROCESS-NOTES.md`.
- **Tools that pushed back:** the freshness hook blocked edits to files not read in the session (correctly); the bare-python hook blocked `.venv/bin/python` in a Bash call (correctly), so the 5.0.0 seed interpreter call lives inside the script file as the task described.

## Honest gap list (all workstreams)

| # | Workstream | Gap | Evidence | Proposed remedy |
|---|---|---|---|---|
| 1 | A | `observe`, `review` and `issue-pipeline` have only a listing and the `--help` options, no task-oriented guide | `docs/user-guide/cli-groups.md`; `superclaude observe --help` | Write a guide per group when owners say who uses them |
| 2 | A, B | Docs for `/sc:issue`, ccsession 6.0.0 changes, Ponytail and pr-submit conflicts exist but were not checked against the code line by line | manifest cells `present-unverified` | Run a follow-up check of those four |
| 3 | A | `/sc:code-review` named in `docs/swarm/README.md:67`, `lens-catalog.md`, `user-guide.md`; `/sc:create` and `/sc:review` in `docs/user-guide/agents.md:912,928`: not shipped commands, same at v5.0.0 | `git ls-tree v5.0.0 src/superclaude/commands/` | Replace with shipped commands or mark as examples |
| 4 | A | CHANGELOG `[6.0.0]` has no entries for `observe`, `review`, `issue-watch`, `issue-pipeline`, `/sc:issue` itself; `WORKER-CONTRACT.md` appears only as the WC-16 rule | `grep` of the section: 0 hits for the four groups | Owner to approve entries (this task allowed one) |
| 5 | A | Release notes: manual-validation numbers differ from this run (39/37/37 versus 38/36/36); Known Issues still says `upgrading.md` is stale | `docs/releases/v6.0.0.md` Testing and Known Issues; transcript lines 1197 to 1199 and 1537 to 1539 | Orchestrator to correct or accept; two edits only were allowed |
| 6 | B | No technical doc for `superclaude observe` (13 source files) | `src/superclaude/cli/observe/` | Write a design or reference note |
| 7 | B | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`: 120 citations differ between the two tags; baseline unknown | `check_citations.py` output | Re-verify against its own baseline commit |
| 8 | B | `docs/reference/nfr-conv-2-prose-determinism.md`: 3 moved citations (`rf-qa.md:144-145`, `rf-qa-qualitative.md:794`), pre-existing since 2026-05 | `check_citations.py` output | Re-anchor or retire the note |
| 9 | B | `docs/developer-guide/git-standards-protocols.md` is another project's document (v5.0.0 deferred item 71, still open) | `docs/testing/v5.0.0/post-release-manifest.json` | Remove or replace |
| 10 | B | Root `VERSION` file says `3.7`; `pyproject.toml` says 6.0.0 | `VERSION`; `scripts/build_superclaude_plugin.py:25` | Update or delete |
| 11 | C | The retention write branch (`cleanupPeriodDays` 365) could only be shown with `CCSESSION_MANAGED_SETTINGS_DIR` set, because this host's managed settings set 90 | transcript lines 860 to 878 | None needed; note for readers |
| 12 | C | If `claude` is replaced by its auto-updater during `superclaude install`, the codegraph step reports `Claude CLI is unavailable` and exits 1 (seen three times); a rerun succeeds | `.dev/issues/v6-post-release/c-e2e-run*-transcript.txt` | Optional: retry once in the installer; not a doc issue |
| 13 | C | An offline install and upgrade were not tried (codegraph and plugins download from the network) | scope | Try offline in a later release |
| 14 | D | No hand-test guides for the 6.0.0 removals and additions; v5.0.0 guides D10, D11, D13 describe removed commands | decision 6.6 | Deferred by decision |
| 15 | E | No sysop guides for `observe`, `issue-watch`, `issue-pipeline`, launch-level hooks, `WORKER-CONTRACT.md` | decision 6.6 | Deferred by decision |

## Artifacts

- Report: `docs/testing/v6.0.0/post-release-report.md`
- Manifest: `docs/testing/v6.0.0/post-release-manifest.json`
- Audit log: `docs/testing/v6.0.0/audit.log`
- E2E script and transcript: `docs/testing/v6.0.0/c-e2e-run.sh`, `docs/testing/v6.0.0/c-e2e-transcript.txt`
- Test guides: none (D and E out of scope, decision 6.6)
- Created doc: `docs/user-guide/cli-groups.md`
- Edited docs: see Workstreams A and B and `git diff --stat`
- Evidence, not committed: `.dev/issues/v6-post-release/` (baseline and after logs, earlier transcripts, citation and link checks, `PROCESS-NOTES.md`)

## Suggested next step

Review the gap list, then open the pull request on the fork from the feature branch (never the upstream), with the project's monitor command in Claude Code:

```text
/sc:pr-submit --base integration --head clayphi/v6-post-release --monitor 3 --repo IronbellyOrg/IronClaude
```

Do not stage `.claude/` and do not commit `.dev/issues/v6-post-release/` (the evidence folder); everything under `docs/testing/v6.0.0/` is committed.
