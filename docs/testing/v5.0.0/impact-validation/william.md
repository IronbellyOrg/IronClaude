# William: v5.0.0 impact validation (issue #354)

This document is your full set of instructions for issue [#354](https://github.com/IronbellyOrg/IronClaude/issues/354). You have two jobs: confirm 16 known bugs, and run two measurements. Everything you need is in this file. Discussion and results go on the issue, not here.

## Before you start

### Work in a new workspace

Create a new Coder workspace for this work instead of using one you already have. A new workspace installs IronClaude automatically, pinned to a version that includes 5.0.0, so there is nothing to install or check out, and nothing you do here touches your everyday setup.

Run these two checks first:

```bash
superclaude --version   # should print 5.0.0
claude mcp list         # should list codegraph
```

If either one is wrong, post what you see on issue #354 and stop. Do not try to fix the install yourself.

### The source code

The bug locations below point into the IronClaude source code. If `~/workspaces/IronClaude` is not in your new workspace, get it with:

```bash
git clone https://github.com/IronbellyOrg/IronClaude.git ~/workspaces/IronClaude
cd ~/workspaces/IronClaude && git remote -v   # must show only origin = IronbellyOrg/IronClaude (no upstream remote)
```

Use `git clone`, not `gh repo clone`. `gh repo clone` adds an `upstream` remote that points at the public parent repository, which is how a PR once landed in the wrong place.

Line numbers in this document are as of commit `5e513796` (the v5.0.0 post-release merge). master has moved since, so a line may have shifted. To see the exact lines, run `git show 5e513796:<path>`.

## How to report

- For each bug you can reproduce, file one new GitHub issue and post its link on #354. Copy `~/.claude/ISSUE-BACKLOG.md` (the template installed with IronClaude; if it is missing, use `src/superclaude/core/ISSUE-BACKLOG.md` from the source), fill in its four sections, and run `gh issue create --repo IronbellyOrg/IronClaude --body-file <your copy>`. Do not fix the bugs yet.
- If something is not a bug, or you cannot reproduce it, say so on #354 and say what you tried.
- After your first three filed issues, post them on #354 and wait for Clay to look before you continue.
- Post one comment per measurement with: which check, date, who ran it, the measured value, the baseline, PASS or FAIL against the limit, and the evidence (command output).
- Keep a workflow ledger as a markdown file. For each step, write which SC command or skill you used, why, what it gave you, and what you changed afterward. Post it on #354 when you finish.

## Part 1: the 16 bugs

For each one, try to make it happen yourself. If you can, file an issue and post the link on #354. If you cannot, or it is not a bug, say so there. After your first three, stop and wait for Clay. The "report name" at the end of each is its label in [the post-release report](../post-release-report.md), in case you want to look it up. Paths are from the repository root.

- [ ] **`superclaude update` help text is wrong.** The help says `update` refreshes five things: core files, commands, agents, skills and hooks. In fact it also updates ccsession, templates and the user setup, and it never installs codegraph. Code: `src/superclaude/cli/main.py` lines 344-345 (what the help says) against lines 365-404 (what it does). Report name: O2.
- [ ] **The `install-skill` help example fails.** The example uses a skill called `pm-agent`, but no skill folder with that name exists, so following the example exits with error 1. Code: `src/superclaude/cli/main.py` lines 448-452 and `src/superclaude/cli/install_skill.py` lines 58-97. Report name: O3.
- [ ] **`sprint status` and `sprint logs` do not work.** The help says they read the sprint log. They are placeholders that print "not yet connected". Code: `src/superclaude/cli/sprint/logging_.py` lines 367-378. Report name: O4.
- [ ] **The `cli-portify run --dry-run` help overpromises.** The help says a dry run executes the early steps. The command actually returns before running any of them (before `run_portify`). Code: `src/superclaude/cli/cli_portify/commands.py` lines 196-204. Report name: O5.
- [ ] **`CI=0` is treated as "yes".** Sprint auto-confirms its prompts when the `CI` or `SUPERCLAUDE_SPRINT_ASSUME_YES` environment variable is set to anything at all, including `0` and `false`. Code: `src/superclaude/cli/sprint/commands.py` lines 323-327 and 891-895. Report name: O7.
- [ ] **A swarm lens hands off to a command that does not exist.** The `refactor-find` lens points you to `/sc:code-review`, which is not a SuperClaude command that ships. Code: `src/superclaude/cli/swarm/lenses/refactor_find.py` line 53. Report name: O11.
- [ ] **`/sc:help` shows "(no description line)" for business-panel.** `src/superclaude/commands/business-panel.md` has no `description:` line. Report name: O12.
- [ ] **Two command docs show flags the commands do not declare.** The examples in `src/superclaude/commands/improve.md` line 89 (`--type security --validate`) and `src/superclaude/commands/cleanup.md` line 73 (`--preview`) use flags that the commands' own syntax lines do not list. Report name: O13.
- [ ] **Plain `superclaude doctor` passes with no codegraph.** It reports healthy when codegraph is not registered and only prints a detail line. Code: `src/superclaude/cli/doctor.py` lines 160-175. The release notes already list this as a known issue (`docs/releases/v5.0.0.md` line 232). Report name: O14.
- [ ] **`sprint verify-checkpoints` writes a file you did not ask for.** It writes `manifest.json` into the output folder even without `--recover`. Code: `src/superclaude/cli/sprint/commands.py` lines 747-748. Report name: O16.
- [ ] **`roadmap run --dry-run` creates a folder.** The output directory is created before the dry-run check, so a dry run still leaves a directory behind. Minor. Code: `src/superclaude/cli/roadmap/executor.py` lines 3670 and 3735-3737. Report name: O17.
- [ ] **The install test's "real home changed" alarm.** The recorded install test reported that the real `~/.claude.json` changed, even though the registration went to the throwaway home and a search of the real file for the test's path found nothing. The most likely cause is another live Claude session writing that file. To confirm, re-run the script from a plain terminal with no Claude session open on that machine. It only runs on a Coder workspace as user `coder`.

  ```bash
  bash docs/testing/v5.0.0/c-e2e-run.sh 2>&1 | tee /tmp/c-e2e-rerun.txt; grep '^SUMMARY' /tmp/c-e2e-rerun.txt
  ```

  Expected: `SUMMARY s1_install=0 s1_doctor=0 s1_second=0 s2_install=0 s2_doctor=0` and no `REAL_HOME_CHANGED`. Evidence: `docs/testing/v5.0.0/c-e2e-transcript.txt` lines 785-798 and `docs/testing/v5.0.0/c-e2e-run.sh` lines 31 and 68-69. Report name: O22.
- [ ] **Running the tests changes a tracked file.** The test suite rewrites `.dev/releases/current/cliEval/evidence/T02.15/perf.json`, which is tracked in git. Report name: O23.
- [ ] **The `pm` memory restore is not wired up.** `src/superclaude/commands/pm.md` says the PM agent restores memory at every session start, but no SessionStart hook reads the memory store. Report name: N1.
- [ ] **Three roadmap and tasklist problems.** When a run halts, the retry command it prints leaves out `--output`. Missing input files crash with a Python traceback. `tasklist validate` run without `--tasklist-dir` reads every `.md` file in the output folder. Report name: N4.
- [ ] **Five `ic`, `init-lite` and `recommend` problems.** (1) `ic` treats the value you give as the name of a shell variable: `ic -H HOME` puts your home path in the model slot. (2) `ic -p` with no value ends with "unbound variable". (3) One bad line in `$AIENV` stops even `ic --help`. (4) `init-lite --dry-run --output CLAUDE.md` exits 0. The report lists this as wrong but does not say what should happen instead, so find out and say. (5) The `python -m` command named in `recommend --help` exits 1. Report name: N12.

## Part 2: measurement, what codegraph costs in tokens

codegraph adds its tool descriptions to every Claude session, and those cost tokens. This measures how many. Run six short calls in a scratch folder, three without codegraph and three with it, and compare the median token counts. It needs codegraph registered in your `~/.claude.json`, which the `claude mcp list` check above confirms. It runs in your new workspace, so the files the installed hooks write under `~/.claude/state/` and `~/.claude/logs/` do not touch your everyday setup.

```bash
# six short headless calls in a scratch repo; compare the medians
mkdir -p /tmp/cg-tok && cd /tmp/cg-tok && git init -q
jq '{mcpServers:{codegraph:.mcpServers.codegraph}}' ~/.claude.json > /tmp/cg-tok/cg.json
for i in 1 2 3; do
  SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude -p "Reply with the word ok." --output-format json --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
    | jq '.usage | .input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens'
  SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude -p "Reply with the word ok." --output-format json --strict-mcp-config --mcp-config /tmp/cg-tok/cg.json \
    | jq '.usage | .input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens'
done
# if jq prints null, read the field names from the `usage` object and sum the input-token fields it shows
```

- **Baseline:** hiding one codegraph tool (`codegraph_explore`) saved about 1,861 tokens per session in four earlier headless runs (`CHANGELOG.md` line 92). No figure exists for all seven registered tools.
- **Pass:** the median difference is 2,000 tokens or less.

## Part 3: measurement, what indexing costs

The first time a repository is opened, codegraph indexes it. This measures how long that takes, how much memory it uses, and how big the index is. Do it on 2 or 3 real team repositories. Use a fresh clone in `/tmp`, never a working repo.

```bash
# run once per repository; each run gets its own new folder under /tmp, so a second repository never reuses the first clone
cg=$(mktemp -d /tmp/cg-cost.XXXXXX) && echo "measuring into $cg" \
  && git clone --depth 1 <repo URL> "$cg/repo" \
  && time uv run --no-project python -c 'import resource,subprocess,sys; subprocess.run(["codegraph","init","--yes",sys.argv[1]],check=True); print("peak_rss_kb", resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)' "$cg/repo" \
  && du -sk "$cg/repo/.codegraph" \
  && codegraph status "$cg/repo"   # only after init has exited; gives the indexed file count
```

Run the block once for each repository. Each run makes its own new folder under `/tmp`, and the `&&` chain stops at the first failed step, so a failed clone cannot be followed by measurements of an earlier repository. The `echo` line shows which folder belongs to which run; write down the folder next to each repository's result. The folders are left in place for you to remove when you are done.

- **Baseline:** about 70 KB per indexed file and up to about 1 GB of memory during the first index (`CHANGELOG.md` line 93).
- **Pass:** peak memory is 1,048,576 KB or less, and the `.codegraph` size divided by the indexed file count is 140 KB or less. Record the time for each repository.
