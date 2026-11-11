# S3 inputs: where each file came from

Scenario S3 = incident I3 of the logs team's phase-1 report: the launch-level hook refactoring plan for issue 394 (three adversarial plan reviews).

Short names used below:

- `H4` = `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-hook-launch-level-394/42ae46e0-b8b8-4840-aafe-9b182be079c9` (so `H4.jsonl` is the main session log, 7,453 lines; `H4/subagents/agent-<id>.jsonl` are the subagent logs). Line numbers are 1-based jsonl line numbers.
- `SV` = `/home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook/.dev/brainstorms/20261105-170229-launch-level-hook` (the surviving copy of the original worktree's brainstorm folder; the original worktree `hook-launch-level-394` no longer exists).
- `BR` = `inputs/brainstorm/adversarial/adversarial` in this package (mirrors the folder the agents worked in).

All copies were made read-only (`cp`, `git show`, `git archive`, `jq`, a replay script). Nothing under `~/.claude` or in another worktree was changed. `inputs/MANIFEST.sha256` lists the sha256 of every file in `inputs/` (check with `cd inputs && sha256sum -c MANIFEST.sha256`).

## How exact is each file?

| Class | Meaning |
|---|---|
| BYTE-EXACT | Copied from a file that existed unchanged on disk, and the agents' own Read results in the logs match it line for line (checked by `tools/reads_vs_disk.py`: `identical_full`). |
| REPLAYED | Rebuilt by re-applying the recorded Write and Edit calls from the logs; verified against what the reviewers' own Read calls returned, line for line (`tools/crosscheck_reads.py`: 0 mismatched lines). |
| INSTALLED-COPY | A copy of `~/.claude` content as it is today. It equals the git tree at the original base commit 8b4858f7 (stated per file). |
| REPO-AT-BASE | `git show 8b4858f7:<path>`. The logs show the agents read the same lines (every line the agent saw occurs, in order, in this file). |

## Files

| File in this package | Class | Original path or log line |
|---|---|---|
| `brainstorm/adversarial/adversarial/refactor-plan.md` (the STARTING DOCUMENT, version v0: 136,216 bytes, 1,053 lines, sha256 c130ba4d...) | REPLAYED | Write at `H4/subagents/agent-a6b78088fe4e8a5aa.jsonl` L193, then Edits (the log repeats each tool call as two records; the first Edit of `<!-- FILL:OVERVIEW -->` at L201/L205 was refused by the freshness hook and did not apply, the retry at L214/L219 did). Last applied Edit L332. Original path: `.../hook-launch-level-394/.dev/brainstorms/20261105-170229-launch-level-hook/adversarial/adversarial/refactor-plan.md`. Line-for-line equal to review 1's three Read results (`H4/subagents/agent-a13bab688a9d224f8.jsonl`, Reads with limit 400, offset 400 limit 300, offset 700 limit 400). Only the line text is confirmed by that cross-check; the byte count is derived from the replay. The same replay run on the next two agents ends in a file whose sha256 equals the plan on disk today (`baseline/plans/`), which supports the method. |
| `BR/base-selection.md`, `BR/convergence-tally.md`, `BR/diff-analysis.md`, `BR/invariant-probe.md` | BYTE-EXACT | `SV/adversarial/adversarial/<same name>`; read by the drafter (`agent-a6b78088fe4e8a5aa.jsonl`) and by reviewers. |
| `BR/round-1-advocate-1.md`, `-2.md`, `-3.md`, `BR/round-2-advocate-1.md`, `-2.md`, `-3.md` | BYTE-EXACT | `SV/adversarial/adversarial/<same name>`; read by the drafter (review 1 also ran Grep on round-2-advocate-1). |
| `BR/variant-1-opus-architect.md`, `BR/variant-2-sonnet-refactorer.md`, `BR/variant-3-haiku-qa.md` | BYTE-EXACT | `SV/adversarial/adversarial/<same name>`; read by the drafter. |
| `BR/scoring-pass-1.md`, `BR/scoring-pass-2.md` | BYTE-EXACT | `SV/adversarial/adversarial/<same name>`; present in the folder when the drafter listed it (not read by any loop agent); kept so that the folder the agents see has the same 18 files as the original (the drafter's own `find` listing, first Bash call of `agent-a6b78088fe4e8a5aa.jsonl`). |
| Size check of all of the above | independent evidence | The drafter's first Bash call also ran `wc -c` on 17 of these files plus `issue-body.md`. All 19 byte counts in that output equal the byte counts of the files in this package (checked 2026-11-08, 0 mismatches). |
| `brainstorm/seed-brief.md` | BYTE-EXACT | `SV/seed-brief.md`; read by the drafter. |
| `brainstorm/enrichment/research-light.md`, `brainstorm/enrichment/codebase-context.md` | BYTE-EXACT | `SV/enrichment/<same name>`; read by the drafter; research-light also by review 1. |
| `issues/394/issue-body.md` | BYTE-EXACT | `/home/coder/workspaces/IronClaude/.dev/issues/394/issue-body.md` (53 lines; read by the drafter and all three reviewers; each Read result equals this file). It holds acceptance criteria AC-1 to AC-8. |
| `owner/hook-session-prompt.md` | BYTE-EXACT (the session's Read result equals the file, `diff` empty) | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/hook-session-prompt.md` (6,771 bytes, sha256 1ae2b0a0...). The session's first user message is `H4.jsonl` L12: "Read /home/coder/workspaces/IronClaude/.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/hook-session-prompt.md and follow it." The session's Read result of it (6,900 characters including line-number prefixes) is in `H4.jsonl` shortly after L12; with the prefixes removed it equals this file line for line (checked 2026-11-08). This file is NOT needed for the review loop; it frames the pipeline that produced the plan. |
| `owner/output-style-pragmatic-L15.md` | BYTE-EXACT (extracted from the log) | `H4.jsonl` L15, `attachment.style.prompt` (output style "Pragmatic" in force for the orchestrator). Its "Completion, testing, and quality gates" section is where the severity rule and the cap of 2 fix cycles come from (see ANALYSIS.md section 4). |
| `installed-skills/sc-adversarial-protocol/refs/artifact-templates.md` | INSTALLED-COPY | `~/.claude/skills/sc-adversarial-protocol/refs/artifact-templates.md` (11,520 bytes, mtime 2026-11-05 13:13, before the run). sha256 prefix 26167953a653ffc0 equals `git show 8b4858f7:src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md`. The drafter read it (first 55 lines only). |
| `installed-skills/sc-pr-submit-protocol/` (21 files), `installed-skills/sc-implement-protocol/` | INSTALLED-COPY | `~/.claude/skills/<name>/` without `__pycache__`. `diff -r` against `git archive 8b4858f7 src/superclaude/skills/<name>` is empty for both. Reviews 2 and 3 and fix cycle 2 grepped and read these directories (review 3 read `sc-implement-protocol/refs/retry.md`). |
| `installed-core/WORKER-CONTRACT.md` | INSTALLED-COPY | `~/.claude/WORKER-CONTRACT.md`; `cmp` with `git show 8b4858f7:src/superclaude/core/WORKER-CONTRACT.md` is equal. Review 1 listed it (Bash `ls`) and the owner prompt names it. |
| `repo-at-8b4858f7/src/superclaude/hooks/hooks.json`, `repo-at-8b4858f7/src/superclaude/cli/install_hooks.py` | REPO-AT-BASE | `git show 8b4858f7:<path>`. The drafter read hooks.json (154 lines) and review 1 read install_hooks.py (160 lines); every line they saw occurs in order in these files (`not_found_in_order=0`). They differ from the same files at 95f2c6e4 (see REPLAY.md, "Drift"). |
| `supplemental/drafter-read-parent-grep-result.txt` | BYTE-EXACT | `H4/tool-results/toolu_0165onTHY31DmuqrzNYoTimz.txt`, a 28,214-byte tool result of the parent session that the drafter fed to `sed` (`agent-a6b78088fe4e8a5aa.jsonl`, Bash call near L26). Not needed to re-run; kept so the drafter's research step can be repeated. |

## Not in inputs/ on purpose

- `baseline/` (a sibling folder of `inputs/`) holds the OUTPUTS of the original run: plan versions v0, v1, v2, the three review reports and per-agent costs. They must not be shown to the re-run's agents.
- The brainstorm's `merged-requirements.md`, `merge-log.md` and `return-contract.yaml` did not exist yet when the loop ran (they are written after Step 5), so they are not inputs.
- The surviving brainstorm folder SV also holds the finished plan and reviews. A replay worktree must NOT contain SV (answer leak); see REPLAY.md, "Leakage and drift".

## Inputs the original agents touched that are NOT frozen here

- `~/.claude/settings.json` (host configuration; it holds environment values, so it is deliberately not copied). The agents used the path mostly as an attack string (`echo x > ~/.claude/settings.json`); fix cycle 2 and review 2 also ran `ls`/`grep` on it. The replay host's own file will differ; this is a small fidelity gap, listed in REPLAY.md.
- `~/.claude/state/launch-level/...` paths: reviewers created throwaway files under it in `/tmp`, not in the real store (the paths in the attack strings are text).
- The repo state the agents grepped (`Makefile`, `src/superclaude/skills/sc-pr-submit-protocol`, `sc-implement-protocol`, `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/hooks/`, `src/superclaude/cli/install_hooks.py`): these are `git show 8b4858f7:<path>` (the worktree was clean at 8b4858f7 apart from the new brainstorm files, until the first commit 9aa7b4f9 at 2026-11-05T22:28:14Z, which is after the loop). `tools/prepare_replay_worktree.sh` restores the ones that changed before 95f2c6e4.
- The live host tools: the reviewers ran real git, bash, GNU sed, tr and jq in `/tmp`. Versions used by the original (from the review files): bash 5.2, GNU sed 4.9, GNU tr 9.7, jq 1.7, git 2.47.3. The host today has exactly: bash 5.2.37, sed 4.9, tr (coreutils) 9.7, jq-1.7, git 2.47.3 (checked 2026-11-08).
