# QA Report: Task-Integrity / Task-Research Alignment

**QA mode:** task-integrity
**Lens:** task-research-alignment
**Date:** 2026-11-08
**Task file:** .dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/TASK-RESEARCH-pre-push-guard-20261108-095046.md (416 lines)
**Research inputs:** research/research-notes.md (85 lines), BUILD-REQUEST.md (84 lines)
**Stance:** adversarial (assume dropped or misrepresented findings)

---

## Method

- Read the full research notes, BUILD-REQUEST.md, the task file's References and Constraints (lines 100-116), every Phase 2 item (lines 173, 176, 179, 182), both Phase 4 items (lines 210, 213), the synthesis items' input lists (lines 220-229) and the staleness notes (lines 410-411).
- Spot-checked every source line the task cites against the real files (results in section 3).
- Read design section 19 in full (docs/designs/sc-issue-launch-level-hook.md lines 489-578), because the goal names it as a code input and Step 2.3 must tag it.
- Read `identify()`/`store()` in launch-job-identity.sh (lines 87-124, 215-248) to test whether the environment questions in the task are complete.
- Grepped the task file for coverage tokens (other tools, libgit2, dulwich, programmatic, sha256, object-format, non-fast-forward, source-only, push.default, HOME, PATH, 19.x, migrat, foreign). Grepped the earlier qa/ reports to avoid repeating findings already raised (none of the findings below were raised before).

## 1. Coverage of goal sub-questions (a)-(f)

| Sub-question | Task items acting on it | Status |
|---|---|---|
| (a) stdin records for create/update/delete/force/HEAD:main/multi/--mirror/--all/--tags, empty stdin, $1/$2 | 2.4 (line 182), 4.1 (line 210) | PARTIAL: the listed forms are covered, but design 19.3/19.5 forms that change the records (mapped source-only refspec, sha256 oid width, non-fast-forward rejection) are not tested (Finding 3) |
| (b) --no-verify, core.hooksPath, send-pack, **other tools** | 2.2 (line 176), 2.4 (line 182), 4.1 (line 210) | PARTIAL: "other tools" has no item (Finding 1) |
| (c) hook lookup in linked worktrees | 2.3 (line 179), 2.4 (line 182), 4.1 (line 210) | COVERED |
| (d) ancestry and environment from a linked worktree | 2.1 (line 173), 2.4 (line 182), 4.1 (line 210) | PARTIAL: environment narrowed to `GIT_*` with HOME overridden; the selector's HOME/PATH dependency is not examined (Finding 2) |
| (e) no-replace publication, executable bit | 2.1 (line 173), 2.4 (line 182), 4.2 (line 213) | COVERED (Finding 5 is MINOR) |
| (f) versions per behaviour and the installed git | 2.4 (`git --version`), 4.1 version table, 4.2 renameat2 kernel version | COVERED |

## 2. Coverage of research-notes findings

| Research-notes finding (line) | Task item | Status |
|---|---|---|
| L1 regexes at 528, 532, 661, refusal text at 59; no `.git/hooks` token (26) | 2.2 (line 176) | COVERED |
| `identify`, `proc`, `publish`, `setsid` at 215, 202-207, 164-174, 292 (27) | 2.1 (line 173) | COVERED |
| Design 19.1-19.8 contract (28) | 2.3 (line 179) | COVERED, but notes and task omit 19.6 (Finding 6) |
| `l2_status` 1012-1029, REMEDY 789, WHY 796, use 1311 (29) | 2.3 (line 179) | COVERED |
| install_hooks.py has no git-hook path, U28 (30) | 2.3 (line 179) | COVERED |
| Pattern: no-replace publish already exists (34) | 2.1, 4.2, 5.3 | COVERED |
| Pattern: session membership, not PPID; hook inherits git's session unless setsid (35) | 2.1, 2.4 | COVERED |
| Pattern: resolve paths through git, never assume `.git` is a directory, design 19.2 (36) | 2.3 | COVERED for current state; the 19.2 placement limits are dropped from the options item (Finding 4) |
| SOLUTION_RESEARCH git-push forms incl. `--atomic`, `--porcelain` (42) | 4.1 only | PARTIAL (Finding 8) |
| Hook environment GIT_DIR, GIT_EXEC_PATH, cwd (46) | 2.4, 4.1 | COVERED for GIT_*; see Finding 2 for non-GIT variables |
| Linux primitives and find_hook/advice.ignoredHook (47) | 4.2, 2.4 | COVERED |
| Version hypotheses (48) | 4.1, staleness note line 411 | COVERED, correctly tagged as unverified |
| 4 agent assignments and 2 web topics (66-74) | 2.1-2.4, 4.1-4.2 | COVERED; the 2.4 list matches the notes' item 4 one-for-one |
| Synthesis mapping (76) | 5.1-5.4 | COVERED (synth-01 reads 01-04; synth-02/03/04 read all six plus gaps) |
| Ambiguity: design dry-run and Q-artifact claims [UNVERIFIED] (84) | 2.3, 2.4 (`--dry-run`), staleness note line 410 | COVERED |

## 3. Fabrication check (cited source lines against real files)

| Task claim | Real file | Result |
|---|---|---|
| `publish()` 164-174: O_EXCL temp, fchmod, os.link | launch-job-identity.sh 164-174 | MATCH (also O_NOFOLLOW; fchmod mode is 0o400, see Finding 5) |
| `proc()` 202-207 reads session from /proc stat | 202-207 (`fields[3]` after the comm split = stat field 6) | MATCH |
| `identify(pid)` at 215; validates pid, start, boot_id, uid | 215-244 (uid check at 236) | MATCH |
| supervisor `os.setsid()` at 292 | 291-292 | MATCH |
| L1 regex at 528, 532 (hookspath, alias, pushurl, insteadof), 661 canonical push, 59 refusal text | launch-level-guard.sh 528, 532, 661, 59 | MATCH (verbatim) |
| `l2_status` 1012-1029 runs `rev-parse --git-path hooks/pre-push`, joins relative answer to wt | orca_worktree.py 1012-1029 | MATCH |
| REMEDY W-L2-ABSENT 789, L2_ABSENT_WHY 796, use 1311-1312 | 789, 796, 1312 | MATCH |
| Design section 19 at 489-578 | design 489-578 | MATCH |
| web-02 `find_hook` `access(X_OK)`, `.exe` fallback, advice.ignoredHook | not in repo; external | PLAUSIBLE, not fabricated (git hook.c has a STRIP_EXTENSION branch); the item requires quoting v2.47.3 lines, which guards it |

No fabricated file, function or line was found. Items that go beyond the notes (fchmod(2) man page, O_TMPFILE+linkat, Python `os` docs in 4.2; `/usr/lib/git-core/git-push` spelling and env-prefix candidates in 2.2) are reasonable extensions of sub-questions (b) and (e), not fabrications.

## 4. Findings

### Finding 1 — IMPORTANT: sub-question (b) "push via other tools" has no checklist item

- **Evidence:** the phrase "other tools" appears only in the Task Overview (line 66). Step 2.2's candidate list (line 176), Step 2.4's experiment list (line 182) and Step 4.1's source list (line 210) cover `--no-verify`, `core.hooksPath`, `send-pack` and `http-push`, but no item asks whether pushers that do not run the git CLI (libgit2-based clients, JGit, dulwich, GitPython, `gh api` or curl ref writes against the hosting API) run a local pre-push hook. Grep for `libgit2|dulwich|JGit|GitPython|programmatic` in the task file returns nothing.
- **Why it matters:** design 19.3 (line 520) states "API/programmatic ref writes can bypass local pre-push". That is a git-behaviour claim Step 2.3 must leave [UNVERIFIED], and no later item can confirm it. The seed brief (`.dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md` line 49) also says curl and API writes are not L2-coverable, so the brainstorm will need a cited answer.
- **Required fix:** add a research area to Step 4.1 (official docs and project docs for libgit2, JGit, dulwich, GitPython, and the GitHub REST refs API) asking, for each, whether a local pre-push hook runs, with source URL and relevance rating; add a row for these to the web-01 Key External Findings; and add "push via other tools" to the Step 2.2 candidate list (`curl`, `gh api`, `uv run python` with a git library) so the L1 coverage of those spellings is known.

### Finding 2 — IMPORTANT: the hook environment (sub-question d) is narrowed to `GIT_*`, and the selector's HOME/PATH dependency is dropped

- **Evidence:** Step 2.4 (line 182) records only `env | grep ^GIT_ | sort` and forces `HOME=$SANDBOX/home` for every git command. Step 2.1 (line 173) asks which validation fields "(start ticks, boot_id, uid) could fail inside a hook process", but not about HOME or PATH.
- **Code facts the task does not reach:** `store()` reads `$HOME` (launch-job-identity.sh lines 102-106) and walks `.claude/state/launch-level` (lines 111-117). In `identify()`, a `FileNotFoundError` from `store()`/`subdir()`/`read_file()` returns `{'status': 'ordinary'}` (lines 220-225). So a hook whose HOME differs from the agent's resolves as ordinary, which means the push is allowed. The bash wrapper exits 2 when `uv` is not on PATH (lines 25-53). Design 19.7 says "callers must preserve that execution context" (line 557) and lists UV as a runtime prerequisite (line 561). Design 19.1 (line 493) names `CCSESSION_LAUNCH_ID` and `CLAUDECODE` as variables that must never be authority, and the `GIT_*` filter does not record them.
- **Why it matters:** whether the hook inherits HOME and PATH unchanged from the agent's shell decides whether `identify` can give a governed verdict at all. This is the core of the brainstorm's open question "How does the hook find the identity script at run time" (seed brief line 78).
- **Required fix:** (i) Step 2.1: add the questions "what does `identify` return when HOME is unset, relative, or points to a home without the launch-level store (cite lines 102-106 and 220-225)" and "what does the wrapper do when `uv` is absent from PATH (lines 25-53)". (ii) Step 2.4: record `HOME`, `PATH`, and the names (not values) of all non-`GIT_*` variables the hook receives. Add one experiment that sets a marker variable and a distinct HOME on the push command and records whether the hook sees them unchanged. (iii) Step 2.2: add `HOME=<dir> git push ...`, `env -i git push ...` and `env -u HOME git push ...` as L1 candidates.

### Finding 3 — IMPORTANT: the 2.3 to 2.4 handoff of [UNVERIFIED] design git claims is broken by parallel ordering, and several design push forms are never tested

- **Evidence:** Step 2.3 (line 179) says git-behaviour claims "stay [UNVERIFIED] here and are listed for the empirical agent and the web agents to confirm". Step 2.3 and Step 2.4 are spawned in the same message (line 170), and Step 2.4 has a fixed experiment list. No later item takes 03's D19-n [UNVERIFIED] list and runs experiments for claims 04 did not cover. Step 3.4 (line 203) only compiles gaps, and Phase 4 is web-only.
- **Design git claims missing from the Step 2.4 list (and from any other item):**
  - a source-only refspec configured to resolve to a protected head, for example `remote.<name>.push` or `push.default=upstream` with upstream `main` (design line 520 "field 3 is authoritative"; line 530 "mapped source-only refspec"). This is a stdin form for sub-question (a) where the command never names main.
  - SHA-format independence (lines 518 and 530). A `git init --object-format=sha256` sandbox changes the oid width and the zero oid in the stdin record, which is part of "exact record format" in (a).
  - non-fast-forward rejection not reaching pre-push (line 534 "fixture refs that actually reach pre-push (not up-to-date/nonfastforward rejection)"). Step 2.4 tests up-to-date but not a plain non-fast-forward push without force.
  - mixed protected and unprotected updates with the protected ref last, and record ordering (line 530). Step 2.4's "mixed push" is one update plus one delete with no protected-last ordering.
  - exact-name edges `refs/heads/mainline` and `refs/heads/feature/main` (line 520). Only `--tags` is tested.
- **Required fix:** add the five forms above to the Step 2.4 experiment list, each with remote refs before and after. Also add one item after Phase 2 (before Gate 1, or as part of Step 3.4) that cross-checks every [UNVERIFIED] git-behaviour claim in research/03 against research/04. Each uncovered claim either gets a follow-up sandbox experiment under the same safety rules or is routed explicitly to web-01 in gaps-and-questions.md.

### Finding 4 — IMPORTANT: the options item (Step 5.3) drops the design 19.2 placement limits

- **Evidence:** Step 5.3 (line 226) gives example placement options: the common-dir hooks directory, "a dedicated core.hooksPath directory", or "a per-worktree core.hooksPath with extensions.worktreeConfig". Design 19.2 (line 512) says "Install only if effective hooks lookup is the supported default, there is no foreign pre-push ... Do not enable `extensions.worktreeConfig`, migrate `core.hooksPath`, shadow foreign hooks, generate name-only stubs". The seed brief repeats this (line 58). Grep on line 226 for `19.`, `migrat` and `foreign` returns zero hits. The research notes carry 19.2 as a pattern (line 36).
- **Why it matters:** two of the three example options are excluded by the contract this research feeds. Without an instruction to label them, Section 7 could recommend a design-excluded placement without saying it reopens a design decision.
- **Required fix:** in the Step 5.3 prompt, require every option to state whether it complies with design 19.2 (line 510-514), citing the research/03 tag. Options that need `core.hooksPath` or `extensions.worktreeConfig` must be labelled "excluded by design 19.2; would reopen the decision". Section 7 must recommend a compliant option, or state explicitly that it recommends reopening 19.2 and why. Also add "foreign pre-push present" and "core.hooksPath already set" to the conflict cases that Section 8 must handle with W-L2-ABSENT (design line 514).

### Finding 5 — MINOR: the reuse of `publish()` for an executable hook is not questioned

- **Evidence:** `publish()` fchmods the file to `0o400` (launch-job-identity.sh line 171), which is not executable. It writes a hidden `.<uuid>` temp file in the parent directory (line 165), uses `dir_fd` (lines 166, 172), and its parameters are a JSON value, not bytes. Step 2.1 (line 173) asks only for "exact syscalls and flags". Step 4.2 (line 213) and Step 5.3 (line 226) present `publish()` as the reusable pattern. No ensuring clause asks what must change for an executable hook (mode, content type), or how the ownership check and self-test of design 19.2 (line 512, "recheck exact owned version/content"; "A header alone is not sufficient ownership proof") would work.
- **Required fix:** add to Step 2.1 or 4.2: "state whether `publish()` can be reused unchanged for an executable hook (mode at line 171, JSON-only payload at line 169), and what the ownership/self-test check after publication must compare."

### Finding 6 — MINOR: design 19.6 and the prior Q artifacts are not routed

- **Evidence:** the research notes (line 28) list 19.1-19.5, 19.7 and 19.8 and skip 19.6 (provenance, design lines 536-545). Step 2.3's rationale (line 179) copies that list. The Q artifacts that 19.6 cites (`.dev/brainstorms/20261106-l2-prepush-decisions/q1..q4/run-4/...`, lines 540-543) are not present in this worktree (`ls` reports no such directory) and have no history in `git log --all`. Design claims rest on them (line 524 worktree removal; line 534 "Q artifacts report local hook invocation"). Step 2.3's "EVERY statement" wording covers 19.6 in principle.
- **Required fix:** in Step 2.3, name 19.6 explicitly. Tell the agent to Glob for the four artifact paths and tag claims resting on them [UNVERIFIED: source artifact absent from checkout] when they are missing.

### Finding 7 — MINOR: depth label disagreement

- **Evidence:** the frontmatter `reflect_pre.depth: "deep"` (line 22) disagrees with the research notes' "Depth Tier: Standard" (line 5). The QA intensity is standard in both. The two values may measure different things (reflect TCS band versus research tier), but nothing says so.
- **Required fix:** add a one-line comment that the reflect depth is the TCS band, not the research depth tier, or align the values.

### Finding 8 — MINOR: push options listed in the notes are tested only through docs

- **Evidence:** the research notes (line 42) list `--atomic` and `--porcelain` among the git-push forms to research. Step 4.1 includes them, but Step 2.4 does not run them. `--force-with-lease` (a stale-rejection path that, like non-fast-forward, may keep a record off the hook's stdin) is absent everywhere.
- **Required fix:** add `--atomic` with one protected and one unprotected ref, and `--force-with-lease` with a stale lease, to the Step 2.4 list. Record whether the hook ran and what stdin held.

### Finding 9 — MINOR (informational): the owner decision on `unknown` is not reflected

- **Evidence:** Step 2.1 (line 173) asks "whether unknown should fail closed". The seed brief (line 73) records an owner decision dated 2026-11-08: refuse only pushes to main or master, with a diagnostic, and allow everything else. The research notes predate this (09:52 versus seed-brief mtime 10:21), so this is not a builder fabrication. It is a drift risk: synth-04 could list a decided question as open.
- **Required fix:** in Step 5.4 / Section 9, cite the seed brief decision and treat `unknown` handling as decided, not open.

## 5. Phase-ordering and dependency check

- Phase 2 then Gate 1 then Phase 4 (web reads gaps-and-questions and 01/03/04 summaries) then Phase 5 (synth-04 after 5.1-5.3) then Phase 6: the order is consistent with the research-notes mapping (line 76).
- Broken dependency: 2.3 to 2.4 (Finding 3). Step 2.3 promises a handoff to a parallel sibling that cannot receive it.

## 6. Summary

| Severity | Count | Findings |
|---|---|---|
| CRITICAL | 0 | none |
| IMPORTANT | 4 | 1 (other-tools bypass), 2 (hook environment, HOME/PATH), 3 (broken 2.3 to 2.4 handoff, untested design push forms), 4 (options ignore design 19.2) |
| MINOR | 5 | 5, 6, 7, 8, 9 |

Blocking findings: 4 (IMPORTANT). All cited source lines in the task match the real files, so nothing was fabricated. The failures are omissions: one goal element, one environment dimension, and several design git-behaviour claims have no item, plus one design constraint was dropped from the options item.

VERDICT: FAIL
