# QA3 Orphan / Contradiction Sweep — pr-submit default --monitor 3

**Date:** 2026-10-23
**Lens:** Orphaned or contradictory instructions (cycle 3)
**Mode:** report-only (fix_authorization = false)

## Verdict

**FAIL**: one real contradiction (F1, IMPORTANT). The routing guide's section 5 row says to use `--monitor 0` *only* when the Augment app is not on the repository. Workflow 3.11 step 6 in the same guide says to use it also when you are not sure the app is installed. Nothing else still says the default is 2, that level 3 needs an explicit flag, that a bare run only proposes, or that level 3 asks before pushing. No other PR-opening instruction contradicts the `/sc:pr-submit --monitor 3` mandate. No "safe" label is left on the level-3 command, and no slash command sits in a `bash` block. One rendering defect was found mid-sweep (blank lines deleted after two tables). The concurrent 15:07 UTC edit restored those blank lines, so it is not counted.

## Search log

Scope: whole worktree, `git grep` with `':!.dev' ':!.claude'` unless noted. Concurrent edits were observed landing at 15:07 UTC (pr-submit.md, SKILL.md, HOW-WE-WORK.md pair); every finding below was re-checked against the tree after that.

| # | Search | Hits | Outcome |
|---|---|---|---|
| S0 | `git diff origin/master` (all 25 files, full text read) | 25 files | Baseline for every judgement below |
| S1 | `--monitor 1\b` | 5 | All on the AC2 allow-list (CHANGELOG, commands.md:363 level description, pr-submit.md:37 L1 example, test_monitor_arm.py x2) |
| S2 | `--monitor 2\b` | 11 | All describe L2 correctly ("fix locally, stop before pushing") as the opt-out from L3 |
| S3 | `--yes` near pr-submit/push/monitor | 3 | fsm.py:97 parser (dead flag, spec 4.2); state-machine.md:157 and CHANGELOG:15 both say it has no effect |
| S4 | widened AC3 regex `default(s/ed)? ... 2` minus max-rounds | 7 | None refers to the `--monitor` default (reflect cycles, roadmap attempts/agents, MAX_NUDGE, swarm floor) |
| S5 | `DEFAULT_MONITOR` | 6 | fsm.py:30 = 3; :53/:76/:758 read it; test asserts 3 |
| S6 | fsm.py `yes/monitor/explicit/L3` lines | ~30 | `poll_outcome(monitor_ordinal=0)` and `transition()` `ctx.get(...,0)` are fail-low helper defaults the skill always passes explicitly; not a user-facing default |
| S7 | explicit/opt-in L3 phrasing | 1 | Only POST-REFLECT-TASK.md (unrelated reflect "L3" layer) |
| S8 | confirm/ask/prompt near push | 3 | review-retrigger "confirmed re-trigger", state-machine.md:157 (says there is NO confirm), unrelated test docstring |
| S9 | tests pinning confirm/`yes` | 0 | — |
| S10/S11 | INV-016 sources / "requires `--yes`" | 10 / 6 | Only `.dev/` history and unrelated `mcp-installation.md --yes` |
| S12 | pr_submit package confirm/explicit/propose | 18 | None about push confirmation or level default |
| S13 | skill scripts monitor/confirm/default | 5 | No push prompt in any script |
| S14 | `gh pr create` (non-test) | 12 | See "Hits judged fine" |
| S15/S16 | "safe flag/setting/command" labels; `safe` within 120 chars of pr-submit | 20 / 0 | Only historical CHANGELOG:24 routing entry (spec C30 keeps it) |
| S17 | sc-recommend `safe`/`mandatory_flags`/`monitor` | 4 | Reads `mandatory_flags`; no hardcoded level |
| S18 | `pr-submit` mentions outside its own files | 27 | All read; see Findings / fine list |
| S19 | PROJECT_INDEX pr_submit | 2 | No default stated |
| S20 | `safe/propose/monitor` in reflect CLI + contract_setup | 28 | `diagnosis.py:255 "Next safe step:"` investigated (judged fine) |
| S21 | commands.md `/sc:pr-submit` section read | 1 | States L3 default |
| S22 | never-push / push-approval rules in core, agents, hooks, templates, root docs, docs/, plugins | 6 | Only the edited guides/contributing text; no unexceptioned "never push" rule |
| S23 | `/sc:git` push text | 1 | HOW-WE-WORK:272 scoped to `/sc:git` |
| S24 | code-fence language of every block containing `/sc:pr-submit` | 10 | `text` or untyped; no `bash` block holds a slash command |
| S25 | tests pinning changed strings (mandatory command shape, safe flag, proposes fixes, upstream/main, next safe command) | 0 relevant | — |
| S26 | tests reading CLAUDE.md / PR template / release guides | ~25 | Only test_how_we_work_routing_table.py:325 (no @-import check); no test pins the changed prose |
| S27 | `.yes` readers / prompts in scripts | 1 | Only fsm.py:130 stores it; nothing reads it |
| S28 | `L3` / `level 3` / propose-only / never-pushes claims in docs, root docs, core, commands, agents, hooks, plugins | 10 | None about pr-submit except commands.md:363 and pr-submit.md:51 (both correct) |
| S29 | root docs (AGENTS, README*, CONTRIBUTING, KNOWLEDGE, SECURITY) PR/push | 11 | CONTRIBUTING "Before opening a PR" checks only; no PR-opening method |
| S30 | `git push` in docs and primitives | 3 | contributing-code.md:188 (approved push, then L3), skill text, reflect denylist |
| S31 | "next safe" / "safe next" | 3 | diagnosis.py:255 + its test (judged fine) |
| S32 | `--monitor` in other commands/skills | 0 | — |
| S33 | open/create/submit/raise/file a PR phrasing (minus pr-submit lines) | 23 | git-standards-protocols.md, developer-guide/README.md, readme_template, post-release skill, implement.md — judged fine |
| S34 | Reads: HOW-WE-WORK.md 194-301, SKILL.md (all), pr-submit.md (all), state-machine.md 140-171, thread-reply / severity_router greps, PR template (all), contributing-code.md 150-229, commands.md 355-395, test_contract_setup_pr_submit_integration.py 100-239, reflect commands.py 74-213, diagnosis.py 232-263 | — | Fact checks for every new level-3 statement |
| S35 | `cmp` guide pair; `cmp` help.md pair; reflect.md pair vs origin/master | — | Guide and help pairs identical; reflect pair already differed on origin/master (311 vs 287 lines) |
| S36 | `git show 2165ae25` | 1 | CHANGELOG claim "command file already said default 3 since 2165ae25" is true |
| S37 | Blank line after the Options / Required Input tables (pr-submit.md:56, SKILL.md:141) | 2 | Missing at 15:05, restored by the 15:07 edit; re-checked, now fine |

## Findings

### F1 — IMPORTANT (contradiction): section 5 row says `--monitor 0` ONLY when the app is absent; 3.11 step 6 says use it also when unsure

- **Locations (re-checked 15:09 UTC):**
  - `src/superclaude/core/HOW-WE-WORK.md:254` (and byte-identical `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:254`), "What to do" cell of the `/sc:pr-submit` row: "Always pass `--monitor 3`. Use `--monitor 0` **only when** the Augment Code review app is not on the repository."
  - `src/superclaude/core/HOW-WE-WORK.md:205` (same in the plugin copy), 3.11 step 6: "This needs the Augment Code review app on your repository. Without it, **or if you are not sure the app is installed** (the repository's Settings > GitHub Apps page lists it), use `--monitor 0`, which only opens the PR."
- **Why it is a contradiction:** a reader who is not sure whether the app is installed gets two opposite instructions from the same guide: 3.11 says use `--monitor 0`; section 5 says `--monitor 0` is for the app-absent case only, so they must pass `--monitor 3`. The "only" was introduced by this branch (spec C4 text); origin/master's row said "Always pass `--monitor 1`" with no `--monitor 0` clause, so the conflict is new. Runtime harm is low (an L3 run without the app ends `terminal_augment_no_response` after one poke and then waits on CI), but the guide is the routing source `/sc:recommend` reads, and the two sentences cannot both be followed.
- **Suggested replacement for line 254's cell (then re-copy to the plugin file byte-for-byte):** "Always pass `--monitor 3`. Use `--monitor 0` when the Augment Code review app is not on the repository or you are not sure it is (3.11 step 6)." Alternatively drop "or if you are not sure the app is installed" from 3.11 step 6 if the intent is that unsure users should still run level 3; either way the two places must say the same thing. (This text is from spec C4, so the spec row should be updated to match.)

No other real orphan or contradiction was found. One defect seen at the start of this sweep (the blank line after the Options table in `pr-submit.md` and after the Required Input table in `SKILL.md` had been deleted together with the `--yes` row, which makes GitHub-flavoured Markdown pull the following `status` line and the `**STOP**` rule into the table) was restored by the concurrent 15:07 UTC edit; re-checked at `pr-submit.md:56-58` and `SKILL.md:141-143`, both now have the blank line, so it is not counted.

## Hits judged fine

| file:line | Text | Why it is fine |
|---|---|---|
| `CLAUDE.md:41` vs `:46` | NEVER "bare `gh pr create` without `--repo IronbellyOrg/IronClaude`" vs `/sc:pr-submit` using `--repo <repo>` from `gh repo view` | Pre-PR check 1 (`:60`) now requires `gh repo view` to print `IronbellyOrg/IronClaude`, so `<repo>` equals the required value; the call is never bare. Opening-before-checking in Wave 0 is spec 4.3(a). |
| `CLAUDE.md:46` "always use `/sc:pr-submit --monitor 3`" (no `--monitor 0` clause) vs HOW-WE-WORK `--monitor 0` advice | — | CLAUDE.md is specific to this repo, which has the Augment app; the generic guide covers repos without it. The `gh pr create` fallback is labelled "Fallback only". |
| `CLAUDE.md:48-50` | ```` ```text ```` block holding the slash command | Not `bash`; the fallback `gh pr create` stays in `bash` (it is a shell command). |
| `CLAUDE.md:61-62` pre-PR checks 2-3 | rebase onto `origin/master`; close + reopen with `--repo IronbellyOrg/IronClaude` | Consistent with the skill's own HALT-on-wrong-owner (SKILL.md:142-145, Wave 0). |
| `CLAUDE.md` "Git Workflow" (integration branch) vs `--base master` | — | Pre-existing; unrelated to the monitor level or the PR-opening method. |
| `HOW-WE-WORK.md:202` "5. Push. Only after your lead approves." and `:229` push rule | — | `:229` adds the single L3 exception and the `--monitor 2` opt-out; `:202` governs the first push (spec section 3). Consistent with `:205` and `:254`. |
| `HOW-WE-WORK.md:272` `/sc:git` "Still never push without approval" | — | Scoped to `/sc:git` (spec section 3). |
| `HOW-WE-WORK.md:323` routing row `review-pr` | step 6 has no level, `mandatory_flags` = `6: --monitor 3` | sc-recommend rule 2 (`SKILL.md:237`) adds mandatory flags to the step; `--monitor` is in pr-submit.md's argument-hint, so rule R1 keeps it. Matches section 5 "Always pass `--monitor 3`". |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:145` heading "(INV-016, verbatim)" | block now has the edited authorization sentence | "Verbatim" covers the five predicates, which are unchanged and match `fsm.py:179-193` `evaluate_push_decision`; the trailing sentence was rewritten on purpose (spec C28). |
| `state-machine.md:156-159` vs SKILL.md Wave 6 (`:194`) | "no interactive confirmation before a push" | Matches Wave 6 (no confirm step), the scripts (no prompt, S13/S27) and `fsm.py` (stores `yes`, never reads it). |
| `SKILL.md:192-193` L1 PROPOSE / L2 HALT_BEFORE_PUSH | — | Every "use `--monitor 2` to stop before pushing" sentence matches Wave 5 (`S4'_HALT_BEFORE_PUSH`, no commit/push/reply). |
| Level-3 behaviour sentences (CLAUDE.md:46, HOW-WE-WORK:205/229/254, release guides :538/:560, CHANGELOG:11/14) | Medium+ fixed, Low/Nit report-only, failing CI fixed, push without asking, reply+resolve only fixed threads | Checked against SKILL.md Waves 2, 6, 8, `severity_router.py:56-58` (`ROUTE_REPORT_ONLY` for Low/Nit) and `refs/thread-reply.md:17-20`. CI fixes only use the remaining round budget and an L3 CI push does not reply or resolve (SKILL.md:197); none of the texts claim otherwise. |
| `src/superclaude/commands/pr-submit.md:18` "(and optionally arm the monitor)" | — | Still true: `--monitor 0` does not arm. |
| `pr-submit.md:36-40` usage examples (L0-L3 typed explicitly) | `--monitor 1 ... # arm + poll + propose (no edits)` | Spec section 3: per-level examples. |
| `pr-submit.md:19` hook sentence | `offer-pr-review.sh` | The "NEVER implies level-3" clause is gone (C13); the missing hook script is spec 4.3(b). |
| `fsm.py:598` `monitor_ordinal: int = 0`; `fsm.py:645` `ctx.get("monitor_ordinal", 0)` | — | Fail-low defaults of internal helpers; SKILL.md:55 and `run_skill` pass the ordinal explicitly; not the CLI default (`fsm.py:76` uses `DEFAULT_MONITOR`). |
| `fsm.py:97` `--yes` | parsed, unread | Spec 4.2 follow-up; every doc now says it has no effect or does not mention it. |
| `src/superclaude/pr_submit/contract_setup/diagnosis.py:255` "Next safe step:" | prints `diagnosis.next_command` | Only called for the missing-contract HALT (no production caller; its test asserts the command is `reflect contract-status`, not `--monitor`). It cannot carry the READY `/sc:pr-submit --monitor 3` command in practice. The user-facing `contract-status` CLI prints `next_command:` with no "safe" label (`cli/reflect/commands.py:174`). |
| `cli/reflect/commands.py:200`, `diagnosis.py:380` READY → `/sc:pr-submit --monitor 3 --pr <N>` | — | `--pr` not parsed by `fsm.py` is spec 4.3(c). |
| `.github/PULL_REQUEST_TEMPLATE.md:21-23` | — | Matches CLAUDE.md (L3 on the fork, `gh pr create --repo IronbellyOrg/IronClaude` fallback, rebase onto `origin/master`). ":22 ... main" is pre-existing wording. |
| `.github/workflows/pull-sync-framework.yml:115` | `gh pr create --repo "$GITHUB_REPOSITORY" ...` | CI automation in the fork's own Actions, pinned `--repo`; not a human/agent instruction. |
| `src/superclaude/commands/auggie-review.md:18`, `:126-127` | `# After: gh pr create --title ...` | Describes when the post-PR hook fires (an installed primitive used in other repos), inside a `text` comment block; not an instruction for how to open IronClaude PRs. |
| `docs/developer-guide/contributing-code.md:183-195` | approved `git push` in `bash`, then `/sc:pr-submit --monitor 3` in `text` | Matches spec C27'. It points to 3.11 rather than repeating CLAUDE.md's pre-PR checks; CLAUDE.md governs agents in this repo, and the target-resolution order is spec 4.3(a). |
| `docs/developer-guide/contributing-code.md:197-219` "Pull Request Template" | differs from `.github` template | Pre-existing drift; names no way to open a PR and no level. |
| `docs/developer-guide/README.md:189-192` "Fork the repository ... Submit pull request" | — | Method-neutral documentation-contribution steps; do not name another way to open a PR; pre-existing. |
| `docs/developer-guide/git-standards-protocols.md:285-360, 634` "Create PR to feature/* / release/* / main" | — | A GFXAI branching reference (front matter `id: GFXAI-GIT-STANDARDS-PROTOCOLS`) for another project; names no tool or level. |
| `src/superclaude/templates/documents/readme_template.md:420` | "Open a Pull Request against `[base branch]`" | Template for other projects' READMEs, inside an HTML comment. |
| `src/superclaude/skills/sc-post-release-protocol/SKILL.md:340, 348` | open PRs against `origin`, confirm first | Generic installed skill for any repo; names no tool. |
| `src/superclaude/commands/implement.md:133` / plugin copy | "Auto-commit, open PRs, or release" (Will Not) | Boundary of `/sc:implement`, not a PR instruction. |
| `src/superclaude/commands/swarm-wizard.md:96` | `/sc:pr-submit` with no level | Spec section 3. |
| `docs/user-guide/commands.md:363` | "at `--monitor 1` or higher ... With no `--monitor` it runs level 3" | Describes levels; on the AC2 allow-list. |
| `CHANGELOG.md:24` "with which safe flags" | historical routing entry | Spec C30 leaves history as written. |
| `CHANGELOG.md:11-18` new entry | — | Every claim checked: `2165ae25` exists and changed only pr-submit.md:26 to "default 3"; `--yes` unread; file list matches the diff. |
| `CONTRIBUTING.md:28-41` "Before opening a PR" | lint/test commands | Pre-PR checks only, no PR-opening method. |
| `plugins/superclaude/commands/reflect.md` vs `src/.../reflect.md` | not byte-identical | Already different on origin/master (311 vs 287 lines); the C26 line is updated in both. |
| `tests/pr_submit/test_hook_update.py`, `test_static_grep.py`, `test_pre_pr_checks.py` `gh pr create` | — | Test fixtures for the `--repo` pin and hook; none pin a level or the changed prose. |

## Self-Audit

**(a) Reliance list — earlier-cycle results relied on without re-checking:**
- None. The qa/qa2 reports were opened only to see which areas earlier cycles had already judged; every conclusion above comes from this cycle's own greps and reads of the current tree. The concurrent 15:07 UTC edit was detected by mtime and every touched file was re-diffed afterwards; there were no further edits as of 15:10:56 UTC.

**(b) Independent semantic checks:**
- Level-3 facts (Medium+ fixed, Low/Nit report-only, CI fixes, push without a confirm step, reply and resolve only on fixed threads): read SKILL.md Waves 2-8 in full, `severity_router.py:56-58`, `refs/thread-reply.md:17-20`, `fsm.py:170-193`, and grepped every script for prompts (S13/S27).
- `--yes` is dead: `git grep '\.yes\b|\byes='` only finds `fsm.py:130` storing it.
- CLAUDE.md internal consistency: NEVER list `:41`, mandatory paragraph `:46`, block `:48-50`, fallback `:52-56`, pre-PR checks `:60-62`.
- HOW-WE-WORK internal consistency across 3.11 steps 5-6 (`:202-205`), section 4 (`:229`), section 5 row (`:254`), routing row (`:323`), plus `cmp` with the plugin copy. This check produced F1.
- Code-fence type of every block containing `/sc:pr-submit` (awk scan, S24).
- "safe" labels: repo-wide label grep plus a trace of `diagnosis.py:255` to its only callers and test.
- Markdown rendering check after the `--yes` row removal (S37). It was a real defect at 15:05 and was fixed by 15:07.

**Why the result can be trusted:** 37 logged searches cover every surface the brief lists (CLAUDE.md, AGENTS, README*, CONTRIBUTING, docs/, core, commands, skills, agents, hooks, templates, plugins/, .github, tests, package code). Every hit was judged in a table above. The one remaining contradiction (F1) is between two sentences in the same guide that earlier cycles did not compare (no "not sure" / "only when" judgement appears in the qa/qa2 reports).

**Tool engagement:** Read 13 | Grep (via git grep/grep in Bash) ~40 patterns | Bash 30 | Web: none (no external lookups were needed, so Tavily was not used).

**Confidence:** Verified 6/6 lens items (default-is-2 / explicit-L3 / confirm-before-push; PR instructions elsewhere; internal contradictions; safe labels; slash commands in bash blocks; factual accuracy) | Unverifiable 0 | Unchecked 0 | Confidence 100% on coverage. Verdict FAIL because of F1.
