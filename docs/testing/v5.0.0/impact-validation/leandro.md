# Leandro: v5.0.0 impact validation (issue #354)

This document is your full set of instructions for issue [#354](https://github.com/IronbellyOrg/IronClaude/issues/354). You have four jobs: decide on 17 known bugs, check whether review loops are ending sooner, check how `/sc:pr-submit` has behaved since the upgrade, and survey the team's workspaces for half-finished upgrades. Everything you need is in this file. Discussion and results go on the issue, not here.

## Before you start

### Work in a new workspace, except where noted

Create a new Coder workspace for the bug work. A new workspace installs IronClaude automatically, pinned to a version that includes 5.0.0, so there is nothing to install or check out, and nothing you do there touches your everyday setup.

Run these two checks first:

```bash
superclaude --version   # should print 5.0.0
claude mcp list         # should list codegraph
```

If either one is wrong, post what you see on issue #354 and stop. Do not try to fix the install yourself.

Two parts of your work must NOT be done in the new workspace, because they look at history and at older workspaces that a new one does not have:

- Part 2 (a), (b) and (d), the review-loop counts: run them in repos where reviews really ran after 2026-11-02. On a fresh clone every file carries the clone date, so the date filter would count everything.
- Part 4, the upgrade survey: it exists to look at the team's existing workspaces.

Part 3 (`gh` queries) works from anywhere.

### The source code

The bug locations below point into the IronClaude source code. If `~/workspaces/IronClaude` is not in your new workspace, get it with:

```bash
git clone https://github.com/IronbellyOrg/IronClaude.git ~/workspaces/IronClaude
cd ~/workspaces/IronClaude && git remote -v   # must show only origin = IronbellyOrg/IronClaude (no upstream remote)
```

Use `git clone`, not `gh repo clone`. `gh repo clone` adds an `upstream` remote that points at the public parent repository, which is how a PR once landed in the wrong place.

Line numbers in this document are as of commit `5e513796` (the v5.0.0 post-release merge). master has moved since, so a line may have shifted. To see the exact lines, run `git show 5e513796:<path>`.

## How to report

- For each bug that is real, file one new GitHub issue and post its link on #354. Copy `~/.claude/ISSUE-BACKLOG.md` (the template installed with IronClaude; if it is missing, use `src/superclaude/core/ISSUE-BACKLOG.md` from the source), fill in its four sections, and run `gh issue create --repo IronbellyOrg/IronClaude --body-file <your copy>`. Do not fix the bugs yet.
- For each bug, say which of three things it is: real (file an issue), intended (say why), or you cannot reproduce it (say what you tried). Several are marked unverified or "may be intended" in the report.
- Post one comment per check with: which check, date, who ran it, the measured value, the baseline, PASS or FAIL against the limit, and the evidence (command output).
- Re-run Part 2, Part 3 and Part 4 on 2026-11-18 and 2026-12-16 and post the results the same way.
- Keep a workflow ledger as a markdown file. For each step, write which SC command or skill you used, why, what it gave you, and what you changed afterward. Post it on #354 when you finish.

## Part 1: the 17 bugs

For each one, decide: real bug (file an issue and post the link on #354), intended (say why), or you cannot reproduce it (say what you tried). The "report name" at the end of each is its label in [the post-release report](../post-release-report.md), in case you want to look it up. Paths are from the repository root.

- [ ] **`--max-convergence` is not connected to anything.** The option exists, but the convergence engine (the loop that decides when a run has settled and can stop) does not use it. It is already a known follow-up: `.dev/releases/current/v5.0.0/DECISIONS.md` item B4 (amended), `docs/releases/v5.0.0.md` line 229, and issue #343. Report name: O6.
- [ ] **An environment variable can make `reflect` look like it passed.** If `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` is exported in your shell, every `reflect` subcommand exits 0 without doing anything, which looks like a pass. The report calls this a design risk. Code: `src/superclaude/cli/reflect/commands.py` lines 44 and 62-73. Report name: O8.
- [ ] **tmux mode may drop your flags.** In tmux mode, sprint rebuilds the inner worker's command from the original arguments and does not pass along `--resume`, `--task-parallelism`, `--handoff/--no-handoff` or `--yes`. Found by reading the code only, not by running it. Code: `src/superclaude/cli/sprint/tmux.py` lines 178-217, with a comment at 210-214. Report name: O9.
- [ ] **Roadmap may allow more fix rounds than the new limit.** The roadmap convergence loop allows up to 3 runs, but 5.0.0 caps review loops at 2 fix cycles. The changelog does not name roadmap, so it is not clear whether it was meant to be covered. Code: `src/superclaude/cli/roadmap/convergence.py` lines 440 and 446. Report name: O10.
- [ ] **The installer reads and writes different config folders.** It reads MCP registrations from `$CLAUDE_CONFIG_DIR/.claude.json` but always writes its files to `$HOME/.claude/`. If `CLAUDE_CONFIG_DIR` is set but empty, registration fails. Code: `src/superclaude/cli/install_mcp.py` lines 721-726, `src/superclaude/cli/install_core.py` line 47, `src/superclaude/cli/install_hooks.py` line 136. Report name: O15.
- [ ] **Is the 3-fix-loop limit in the cli-eval skill meant to be 2?** `sc-cli-eval-protocol` allows "max 3 fix loops" for manifest loader errors. Decide whether the new 2-fix-cycle rule and its test (`tests/skills/test_review_severity_rule.py`) are meant to cover loops that are not reviews. It may be intended. Code: `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md` line 204 and `src/superclaude/skills/sc-cli-eval-protocol/refs/create-pipeline.md` line 50. Report name: O18.
- [ ] **A fresh swarm run never writes `done.json`.** Only `swarm kill --output` writes it. Seen on a live stub run (post-release scan A2) and in `src/superclaude/cli/swarm/reduce.py` line 139. What happens on resume is unclear and unverified. Report name: O19.
- [ ] **`/sc:graph init` may not find `codegraph`.** The command's allowed-tools entry is `Bash(codegraph init --yes *)`, which uses the bare command name. If `~/.local/bin` is not on your PATH, the command may not resolve. Unverified. Code: `src/superclaude/commands/graph.md` line 9 and `src/superclaude/cli/install_codegraph.py` lines 155-163. Report name: O20.
- [ ] **The upgrade leaves old codebase-memory pieces behind without listing them.** After the upgrade the skill `codebase-memory` and 3 agents stay. The retire step says "binary and companions stay" but does not say where they are. This is by design, and the suggestion is to print the paths. Evidence: `docs/testing/v5.0.0/c-e2e-transcript.txt` lines 729-736 and 771-773. Report name: O21.
- [ ] **Sprint `--resume` skips nothing with the default settings.** The gate mode defaults to `off`, so every handoff record stays `pending` and there is nothing for `--resume` to skip. Report name: N2.
- [ ] **`roadmap validate` says "0 blocking" when its review failed.** If the review session fails, it still prints `0 blocking` and exits 0, so a failure looks like a pass. Report name: N3.
- [ ] **`reflect run --fix` can never fix anything.** No 5.0.0 run can return `halted` (exit code 10), so `--fix` never reaches `/sc:implement` or `/task`. Report name: N5.
- [ ] **Three `reflect run` oddities.** `--print-command` prints a prompt the real run never sends. With the default `openai_compat` transport and no proxy credentials, the exit code is 1, not 2. `--transport stub` still starts one real `claude` session. Report name: N6.
- [ ] **Real `cli-portify` runs misbehave.** A real run always stops at `user-review-p1` but exits 0. `--max-convergence 3` still gives only one review pass. `--pass` does not change the steps. Report name: N8.
- [ ] **`swarm run --detached` loses its output.** It writes only `.swarm-detached-spec.json`, because the tmux child process gets no `--output` option. The swarm wizard recommends `--detached`. Code: `src/superclaude/cli/swarm/commands.py` lines 1297-1304 and `src/superclaude/cli/swarm/preflight.py` lines 1871-1873. Report name: N9.
- [ ] **Five swarm problems.** `--resume` empties the contract's lens and next command. The contract lists `.raw.md` files that are never written. The stub transport labels every worker `lens-default-model-0`. `--tui` can show fewer workers than exist. The help still names `--custom-prompt-dir`. Report name: N10.
- [ ] **The eval coverage gate blocks nearly every suite.** With IronClaude's hooks installed, it stops every suite except `real` with exit code 2, under a wrong `eval doctor:` prefix. Separately, `eval run` creates the run folder before it validates the suite or eval id. Report name: N11.

## Part 2: measurement, are review loops ending sooner?

The 5.0.0 rule says minor findings never fail a review, and every review loop stops after 2 fix cycles (3 reviews), then hands the open serious findings to a person. This check asks whether that is what is happening.

Two terms: a "QA gate" is one piece of work being reviewed. Its numbered report files (`...-report-1.md`, `...-report-2.md`) show how many reviews it took. An "attempt" is one try at a task inside `/sc:implement`.

Run (a) and (b) in each project repo where reviews ran since the upgrade (not in the new workspace, see above). Run (c) from the IronClaude clone.

```bash
# (a) numbered QA reports created after the tag date
find .dev -name 'qa-*report-[0-9]*.md' -newermt 2026-11-02 -printf '%h %f\n' \
  | sed -E 's/-report-([0-9]+)\.md$/ \1/' \
  | awk '{k=$1" "$2; if($3>m[k]) m[k]=$3} END{for(k in m){t++; if(m[k]>=4){h++; print "4+ reviews:", k}} print "qa_gates="t+0, "gates_with_4plus_reviews="h+0}'
# (b) /sc:implement ledgers: highest attempt per task, and halts, only for ledgers changed after the tag date
#     (plan packages under .dev/tasks/, and runs on a file or prompt under .dev/implement/)
LEDGERS=$(find .dev/tasks/to-do .dev/tasks/done .dev/implement -mindepth 2 -maxdepth 2 -name progress.md -newermt 2026-11-02 2>/dev/null)
for f in $LEDGERS; do
  awk -v f="$f" '/^T[0-9A-Za-z.-]+: retry n=/{t=$1; sub(":","",t); match($0,/n=[0-9]+/); n=substr($0,RSTART+2,RLENGTH-2)+0; if(n>m[t]) m[t]=n}
    /^T[0-9A-Za-z.-]+: (complete|blocked)/{t=$1; sub(":","",t); c[t]=1}
    END{for(t in c){tot++; if(m[t]>=4) hi++} printf "%s tasks=%d attempt4plus=%d\n", f, tot, hi+0}' "$f"
done
[ -n "$LEDGERS" ] && grep -H 'halt review=' $LEDGERS
# (c) static guard, from the IronClaude clone
uv run pytest tests/skills/test_review_severity_rule.py -q
```

Command (b) differs from the one in the issue's runbook, which has no date filter. Without the filter, old ledgers from before the upgrade would count against the 2% limit, and old successful tasks would hide new failures. Like (a), it picks ledgers by file date, so run it where the files keep their real dates, not on a fresh clone.

- **(d) Re-grade the minors.** Take 10 findings that were graded "minor" after 2026-11-02 (from `artifacts/retries/T*/notes.md` in plan packages, or QA reports that passed with notes). Re-grade each against the definition in `src/superclaude/output-styles/pragmatic.md` line 225.
- **(e) The guide.** Run guide [D06](../user/D06-plan-implement-review-cap.md) Steps 1 and 2. Optionally run Step 9, a seeded defect that cannot be fixed. `/sc:implement` keeps its own ladder, so the expected result is a last ledger line `T1: halt review=<2-5>` with no `complete` line.

**Baseline.** Measured in the IronClaude repo on 2026-11-03 with the same commands but without the date filter:

- 2 of 14 numbered QA gates had 4 or more reviews.
- In the `/sc:implement` records, 3 of 8 tasks in `TASK-WF-implementTheAppr-20261024-060449` reached attempt 4 or more under the old rule. Two of them ended `halt review=5 reason=ladder-end`.
- 0 of 175 tasks in the other 14 records (8 plan packages, 6 under `.dev/implement/`).
- From `.dev/releases/current/v5.0.0/QA-LOOP-FINDINGS.md`: 4 of 60 tasks had 4 or more rounds under the old #277 rule, 0 of 45 under #297, and two ad hoc loops ran 7 and 8 rounds.

**Pass.**

- (a) 0 gates with a 4th review.
- (b) At most 2% of tasks reach attempt 4 or more, and each one is held up by a blocking finding, never a minor one.
- (c) All tests pass.
- (d) None of the 10 re-graded minors is a real defect.
- (e) Step 9 matches its expected result.

## Part 3: measurement, has `/sc:pr-submit` behaved since the upgrade?

Before 5.0.0 the guides said `--monitor 1` (propose only), and a PR once landed on the public upstream parent repository (2026-05-25). 5.0.0 makes `--monitor 3` the default, which pushes fixes without asking, and makes the PR target come from the `origin` remote. Look at the history instead of running the guide.

```bash
gh pr list --repo IronbellyOrg/IronClaude --state all --limit 500 --search "created:>=2026-11-02" --json number,url --jq '.[].url'
gh pr view <N> --repo IronbellyOrg/IronClaude --json commits --jq '.commits[].messageHeadline'   # each PR where /sc:pr-submit pushed
```

Also check the URL printed by every `/sc:pr-submit` you run yourself.

**Pass.**

- Every PR URL starts with `https://github.com/IronbellyOrg/IronClaude/pull/`.
- No push adds more than one commit on top of the PR head.
- No auto-pushed fix commit was reverted in the window. Each one that was gets its own issue.

## Part 4: measurement, which workspaces are half-upgraded?

This asks which team workspaces have 5.0.0 files but no codegraph, or still have old registrations. Run it on each existing team workspace, not in your new one. Existing workspaces keep the IronClaude version baked into their image until they are updated, so some will be behind. For example, a workspace built from the image pinned at commit `539e2414` reports version 4.3.5, still has Serena and codebase-memory registered, and has no `~/.claude/CODEGRAPH.md`.

```bash
superclaude --version
superclaude install --list | grep -iE 'codegraph|User registration|Ready for Serena|serena|codebase-memory'
superclaude doctor --verbose | grep -iE 'codegraph|legacy|retired'
ls ~/.claude/ORCHESTRATOR.md ~/.claude/COMMANDS.md ~/.claude/PERSONAS.md ~/.claude/MODES.md ~/.claude/FLAGS.md ~/.claude/MCP.md 2>/dev/null
ls -d ~/.claude/skills/codebase-memory 2>/dev/null
cmp ~/.claude/CLAUDE.md <path to an IronClaude clone at master>/src/superclaude/core/CLAUDE.md && echo "CLAUDE.md is the 5.0.0 copy"
```

- **Baseline:** none exists. This first run is the baseline.
- **A fully upgraded workspace shows:** version 5.0.0, a `User registration:` line that is not `absent`, `Ready for Serena retirement: yes`, and no `no codegraph registration` line.
- **Pass:** list every half-upgraded workspace on #354 and tell its owner. On 2026-12-16 none should remain. Leftover retired core files and the `codebase-memory` skill are harmless. List them and let the owner decide.
- **What to tell the owner:** the runbook says to run `superclaude install --force`. On a Coder workspace the IronClaude version comes from the workspace image, so `install --force` would only reinstall the old baked version. The likely fix is to update the workspace to the current template version and restart it, as the image changelog describes for other changes. This is an inference, so confirm it with Clay before you tell anyone.
