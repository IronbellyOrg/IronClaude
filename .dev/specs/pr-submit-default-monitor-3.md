---
title: "sc:pr-submit defaults to --monitor 3, and every PR instruction uses it"
version: "1.0.0"
status: draft
feature_id: PR-SUBMIT-DEFAULT-L3
spec_type: component
complexity_class: SMALL
created: 2026-10-23
branch: feature/pr-submit-default-monitor-3
base: origin/master @ b0bd8c8b
---

# sc:pr-submit defaults to `--monitor 3`

## 1. Goal

1. `/sc:pr-submit` with no `--monitor` runs level 3: fix verified review findings, push, reply, resolve.
2. Every PR instruction in the repo says to open PRs with `/sc:pr-submit --monitor 3`.
3. No instruction, example, code default, or test is left saying the default is 2, or telling the user to pass `--monitor 1`.

Background: commit `2165ae25` (2026-10-22) already changed `src/superclaude/commands/pr-submit.md:26` to "default 3", but nothing else. The code default (`fsm.py:30`) is still 2, so today the command file and the code disagree. This spec finishes that change.

## 2. Changes (exhaustive)

Line numbers are on `origin/master` @ `b0bd8c8b`. "Old" text must be gone after the change; "New" text must be present.

### 2.1 PR instruction

| ID | File:line | Old | New |
|---|---|---|---|
| C1 | `CLAUDE.md` (repo root) "The mandatory command shape" block (lines ~46-50) | The only command shown is `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."` | Mandatory: `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`, with one sentence saying what level 3 does. The `gh pr create --repo IronbellyOrg/IronClaude ...` line stays, labelled as the fallback for when `/sc:pr-submit` cannot run. The NEVER list, pre-PR checks, exceptions and rationale stay unchanged. |
| C2 | `src/superclaude/core/HOW-WE-WORK.md:204` | `/sc:pr-submit --monitor 1 --head feature/invoice-csv-export ...` | `/sc:pr-submit --monitor 3 --head feature/invoice-csv-export ...` (rest of line unchanged) |
| C3 | `src/superclaude/core/HOW-WE-WORK.md:205` | "...checks each of its findings, and proposes fixes without changing your code." | "...checks each of its findings, fixes the ones it confirms, pushes those fixes to your branch, and replies to and resolves each review comment." Rest of line (Augment app / `--monitor 0`) unchanged. |
| C4 | `src/superclaude/core/HOW-WE-WORK.md:254` | "With no `--monitor` setting it uses `--monitor 2` and edits your code to fix review findings. `--monitor 3` also pushes on its own." / "Always pass `--monitor 1`." | "With no `--monitor` setting it uses `--monitor 3`: it fixes the review findings it confirms, pushes the fixes to your branch, and replies to and resolves the review comments on its own." / "Always pass `--monitor 3`. Use `--monitor 0` only when the Augment Code review app is not on the repository." |
| C5 | `src/superclaude/core/HOW-WE-WORK.md:323` (routing row `review-pr`, mandatory-flags cell) | `4: --no-post-pr; 6: --monitor 1` | `4: --no-post-pr; 6: --monitor 3` |
| C6 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Copy of the old guide | Byte-identical copy of the new `src/superclaude/core/HOW-WE-WORK.md` |
| C7 | `tests/core/test_how_we_work_routing_table.py:338` | `"/sc:pr-submit": "--monitor 1",` | `"/sc:pr-submit": "--monitor 3",` |
| C8 | `docs/guides/prd-skill-release-guide.md:535` and `:538` | `--monitor 1` in the command; line 538 says "then run `/sc:pr-submit`." | `--monitor 3`; line 538 adds after "then run `/sc:pr-submit`.": "It fixes the review findings it confirms and pushes those fixes to your branch on its own." |
| C9 | `docs/guides/tdd-skill-release-guide.md:557` and `:560` | Same as C8 | Same as C8 |
| C10 | `docs/user-guide/commands.md:363` | No default stated | Add after the first sentence: "With no `--monitor` it runs level 3." |

### 2.2 Skill default

| ID | File:line | Old | New |
|---|---|---|---|
| C11 | `src/superclaude/pr_submit/fsm.py:30` | `DEFAULT_MONITOR = 2` | `DEFAULT_MONITOR = 3` (lines 53, 76, 758 read this constant; no change there) |
| C12 | `tests/pr_submit/test_skill_parse.py:4`, `:57`, `:58`, `:60` | "default L2"; `def test_t103_default_monitor_two_armed`; "the default is 2"; `== 2` | "default L3"; `def test_t103_default_monitor_three_armed`; "the default is 3"; `== 3` |
| C13 | `src/superclaude/commands/pr-submit.md:19` | "(the hook NEVER arms a monitor itself, NEVER implies level-3 without explicit invocation)" | "(the hook NEVER arms a monitor itself)" |
| C14 | `src/superclaude/commands/pr-submit.md:47` | `\| --monitor {0,1,2,3} \| 2 \|` | `\| --monitor {0,1,2,3} \| 3 \|` (line 26 already says default 3; leave it) |
| C15 | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:135` | "No (defaults to 2)" | "No (defaults to 3)" |
| C16 | `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:158-159` | "the `push_decision` record + the explicit `--monitor 3` arming stands as the recorded authorization." | "the `push_decision` record + the `--monitor 3` arming (typed or the default) stands as the recorded authorization." |

### 2.3 Contract-readiness next command

| ID | File:line | Old | New |
|---|---|---|---|
| C17 | `src/superclaude/pr_submit/contract_setup/diagnosis.py:380` | `/sc:pr-submit --monitor 1{pr_arg}` | `/sc:pr-submit --monitor 3{pr_arg}` |
| C18 | `src/superclaude/cli/reflect/commands.py:200` | Same as C17 | Same as C17 |
| C19 | `tests/pr_submit/test_contract_setup_diagnosis.py:11`, `:290`, `:311` | `--monitor 1` | `--monitor 3` |
| C20 | `tests/pr_submit/test_detection_contract.py:98`, `:99`, `:106` | `--monitor 1` | `--monitor 3` |

### 2.4 Record

| ID | File | New |
|---|---|---|
| C21 | `CHANGELOG.md`, under `## [Unreleased]` | A new subsection stating: the default is now 3; every PR instruction and the routing guide use `--monitor 3`; the contract-readiness next command is `--monitor 3`; a bare `/sc:pr-submit` now pushes fixes and replies to and resolves review comments without asking; use `--monitor 0` to only open the PR. |

### 2.5 Revision 1 (after QA cycle 1; supersedes the "New" text above where it overlaps)

QA cycle 1 (`.dev/reviews/pr-submit-default-monitor-3/qa-spec-conformance.md`, `qa-orphan-sweep.md`) found that the original wording overstated level 3 and left contradictions elsewhere. Facts the wording must match:
- Level 3 fixes confirmed findings of Medium severity or higher; Low/Nit and unconfirmed findings are report-only (`SKILL.md` Waves 2-3, `severity_router.py` `ROUTE_REPORT_ONLY`).
- It replies to and resolves only the threads it fixed (`refs/thread-reply.md`).
- The first push of an interactive run asks once unless `--yes` (`refs/state-machine.md` §5.3).
- The target repo comes from `gh repo view`, which prefers an `upstream` remote over `origin` (SKILL.md Wave 0).

| ID | File | Required text after revision |
|---|---|---|
| C1' | `CLAUDE.md` mandatory-PR paragraph | Says the PR is opened with `gh pr create --repo <repo>` where `<repo>` is what `gh repo view` reports (pre-PR check 1 ensures it is the fork); fixes confirmed findings of Medium severity or higher (lower ones only reported); pushes; replies to and resolves the comments it fixed; asks once before its first push unless `--yes`. No claim that it targets origin directly. |
| C22 | `CLAUDE.md` pre-PR check 1 | Adds: `gh repo view --json nameWithOwner -q .nameWithOwner` must print `IronbellyOrg/IronClaude`; otherwise run `gh repo set-default IronbellyOrg/IronClaude` (gh prefers `upstream` over `origin`). |
| C3' | `HOW-WE-WORK.md` 3.11 step 6 text | "fixes the confirmed ones of Medium severity or higher (lower ones are only reported), pushes those fixes to your branch, and replies to and resolves the review comments it fixed. It asks you once before its first push unless you add `--yes`." |
| C4' | `HOW-WE-WORK.md` section 5 `/sc:pr-submit` row | Same facts as C3'; no "on its own" / "each review comment". "What to do" cell unchanged from C4. |
| C23 | `HOW-WE-WORK.md` section 4 "Never push without approval" | Keeps the rule and adds the one exception: after the approved push, `/sc:pr-submit --monitor 3` (workflow 3.11) pushes the review fixes it makes, asking once before its first push; if the lead wants to see those fixes first, run it only with their go-ahead. |
| C6' | plugin `HOW-WE-WORK.md` | Re-copied byte-identical after C3'/C4'/C23. |
| C8'/C9' | PRD and TDD release guides, line after the code block | "It fixes the confirmed review findings of Medium severity or higher and pushes those fixes to your branch, asking once before its first push unless you add `--yes`." No "on its own". |
| C24 | `src/superclaude/commands/pr-submit.md` `argument-hint` and Options table | Documents `--yes` (already parsed by `fsm.py`): skips the one-time first-push confirmation of an interactive L3 run (`refs/state-machine.md` §5.3). |
| C25 | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` Required Input table | Same `--yes` row as C24. |
| C26 | `src/superclaude/commands/reflect.md:82`, `plugins/superclaude/commands/reflect.md:73`, `src/superclaude/skills/sc-reflect-protocol/SKILL.md:67` | "the next safe command" becomes "the next command to run" (the READY command is now level 3, which is not propose-only). |
| C27 | `docs/developer-guide/contributing-code.md` "Submit Pull Request" step | Replaces "# Create PR on GitHub" with: follow workflow 3.11, push only after approval, open the PR with `/sc:pr-submit --monitor 3 --head ... --title ... --body ...`; fallback `gh pr create --repo IronbellyOrg/IronClaude`. |
| C21' | `CHANGELOG.md` entry | States the accurate level-3 behaviour (as C3'), the `--yes` documentation, the corrected file list (`contributing-code.md` instead of `commands.md` for "now say to open PRs with `--monitor 3`"; `commands.md` "now states the level-3 default"), the new pre-PR `gh repo view` check (C22), and the push-rule exception (C23). No "without asking". |

### 2.6 Revision 2 (after QA cycle 2; supersedes 2.5 where they overlap)

QA cycle 2 (`qa2-spec-conformance.md`, `qa2-orphan-sweep.md`) found that the "asks once before its first push unless `--yes`" wording was false: no wave of the skill loads `refs/state-machine.md` §5.3, Wave 6 pushes with no confirm step, and no code reads `--yes`. Decision: keep level 3 fully autonomous (the user's request) and make every document say so; point to `--monitor 2` for anyone who wants to see fixes before they are pushed. Also: L3 fixes and pushes failing CI checks too (SKILL.md Wave 8).

| ID | File | Required text after revision |
|---|---|---|
| C1'' | `CLAUDE.md` mandatory-PR paragraph + block | Fixes confirmed findings of Medium severity or higher (lower only reported) and failing CI checks, pushes the fixes without asking, replies to and resolves the comments it fixed. Says it is a slash command run in Claude Code; the block is ` ```text `, not ` ```bash `. No `--yes` / "asks once". |
| C3'' / C4'' | `HOW-WE-WORK.md` 3.11 step 6 and section 5 row | Same facts as C1''; 3.11 adds "To see the fixes before they are pushed, use `--monitor 2` instead: it makes them locally and stops before pushing." |
| C23' | `HOW-WE-WORK.md` section 4 push rule | Exception: after the approved push, `/sc:pr-submit --monitor 3` pushes the fixes for review findings and failing CI checks without asking again; if the lead wants to see them first, use `--monitor 2`. |
| C8''/C9'' | PRD/TDD release guides | "It fixes the confirmed review findings of Medium severity or higher and failing CI checks, and pushes those fixes to your branch without asking (use `--monitor 2` to stop before pushing)." |
| C24'/C25' | `pr-submit.md` argument-hint + Options, `SKILL.md` Required Input | The `--yes` additions from 2.5 are REMOVED (the flag has no effect; documenting it would mislead). Net change vs origin/master for `--yes`: none. |
| C28 | `refs/state-machine.md` §5.3 confirm sentence | Replaced: there is no interactive confirmation before a push (Wave 6 has no confirm step; the parsed `--yes` flag has no effect); the `push_decision` record + `--monitor 3` arming (typed or default) is the recorded authorization; `--monitor 2` stops before any push. (Supersedes C16.) |
| C27' | `docs/developer-guide/contributing-code.md` | `git push` stays in a `bash` block; "Then, in Claude Code:" and the `/sc:pr-submit --monitor 3 ...` line in a separate ` ```text ` block. |
| C29 | `.github/PULL_REQUEST_TEMPLATE.md:21`, `:23` | ":21" becomes "Opened with `/sc:pr-submit --monitor 3` on `IronbellyOrg/IronClaude` (fallback: `gh pr create --repo IronbellyOrg/IronClaude`)."; ":23" becomes "Branch rebased onto `origin/master` (no conflicts)." |
| C30 | "safe flags" naming | `tests/core/test_how_we_work_routing_table.py`: comment says "required flag", `_SAFE_FLAGS` becomes `_MANDATORY_FLAGS`, test becomes `test_named_mandatory_flags_are_on_their_steps`. "with which safe flags" / "with safe flags" becomes "required flags" in `CLAUDE.md:330`, `docs/user-guide/how-we-work.md:3`, `src/superclaude/commands/help.md:91`, `plugins/superclaude/commands/help.md:91` (help copies stay byte-identical). The historical `CHANGELOG.md` routing entry is left as written. |
| C21'' | `CHANGELOG.md` | Matches C1''; adds bullets for C28, C29, C30; no `--yes` / "asks once". |
| C31 (cycle 3) | `pr-submit.md` after Options table; `SKILL.md` after Required Input table | The blank line before the following paragraph is preserved (net diff deletes no blank line), so the `status` line and the `**STOP**` rule do not render inside the tables. |
| C32 (cycle 3) | `HOW-WE-WORK.md` 3.11 step 6 | "and failing CI checks" (no "any"); level 3 fixes CI failures only in some cases (Wave 8 is wait-only once `max_rounds` is reached). |
| C4''' (cycle 3) | `HOW-WE-WORK.md` section 5 `/sc:pr-submit` row, "What to do" cell | "Always pass `--monitor 3`. Use `--monitor 0` when the Augment Code review app is not on the repository or you are not sure it is (3.11 step 6)." Consistent with 3.11 step 6. |

## 3. Deliberately unchanged

| What | Why |
|---|---|
| `src/superclaude/commands/pr-submit.md:26` | Already says "default 3" (commit `2165ae25`). |
| `src/superclaude/commands/pr-submit.md:36-39` (examples for levels 0-3) | Each level is typed explicitly; they document all levels. |
| `src/superclaude/core/HOW-WE-WORK.md:202` ("Push. Only after your lead approves.") | Governs the first push of the branch, before the PR opens. C3 states that level 3 pushes review fixes afterwards. |
| `--max-rounds` default 2 (`fsm.py:31`, `SKILL.md:137`, `refs/loop-guard.md:18`) | Not part of this change. |
| `--monitor 0` open-only tests and text | Still valid. |
| Syntax lines listing `--monitor {0,1,2,3}` | Still valid. |
| `src/superclaude/commands/swarm-wizard.md:96` | Mentions `/sc:pr-submit` without a level. (The three reflect lines originally listed here are now changed by C26.) |
| `src/superclaude/core/HOW-WE-WORK.md:272` (`/sc:git` "Still never push without approval") | Scoped to `/sc:git` only; consistent with C23. |
| `src/superclaude/core/CLAUDE.md` level table | Does not mention `/sc:pr-submit`; the HOW-WE-WORK level table is not edited, so no re-copy is needed. |
| `.dev/` history (old tasks, reports) | Records, not instructions. |
| `.claude/` dev copies | Gitignored; refreshed by `make sync-dev`, never staged. |

## 4. Out of scope (outside this repo or pre-existing)

1. Other projects in this workspace use `~/.claude/` copies and the install at `/opt/uv/tools/superclaude`, pinned to commit `c4606ce7` by `/etc/aidev02/ironclaude-provenance` (workspace setup, not this repo). They keep the old default until that pin moves and `superclaude update` runs.
2. `refs/state-machine.md:156-158` says the first push of a run needs `--yes` or an interactive confirm. `fsm.py` parses `--yes` (lines 64, 97, 130) but no Python code reads it; the confirmation is carried out by the agent following the skill. Revision 2 (C28) makes the docs match that reality instead of documenting the flag; adding a real confirm step or removing the dead flag is a follow-up.
3. Follow-ups found by QA cycle 1, pre-existing, not fixed here: (a) SKILL.md Wave 0 should resolve the target from `git remote get-url origin` first and check it BEFORE `gh pr create`, not after; (b) `offer-pr-review.sh` is referenced (`pr-submit.md:19`, `SKILL.md:189`, `auggie-review.md`) but does not exist; (c) the contract-status READY command uses `--pr <N>`, which `fsm.py` does not parse.

## 5. Acceptance criteria

| ID | Check | Pass when |
|---|---|---|
| AC1 | Every change C1-C21 | Present exactly as specified; nothing else in those files changed. |
| AC2 | `git grep -n -E -- '--monitor 1' -- ':!.dev'` | Only hits are: the level-1 example at `src/superclaude/commands/pr-submit.md:37`; test names/docstrings that exercise level 1 explicitly (`tests/pr_submit/test_monitor_arm.py`); `docs/user-guide/commands.md:363` ("at `--monitor 1` or higher, arm..." describes what each level does); and the C21 `CHANGELOG.md` entry ("instead of `--monitor 1`"). |
| AC3 | `git grep -n -i -E 'default(s)? (to \|is \|L)?2\b\|uses .--monitor 2' -- src/superclaude/pr_submit src/superclaude/commands/pr-submit.md src/superclaude/skills/sc-pr-submit-protocol src/superclaude/core tests/pr_submit tests/core docs` | No hit refers to the `--monitor` default (hits about `--max-rounds` or unrelated features are fine). |
| AC4 | `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Identical. |
| AC5 | `make sync-dev && make verify-sync` | Passes. BLOCKED in the authoring workspace: `make` is not installed and there is no sudo. CI runs `make verify-sync` as the authoritative gate. |
| AC6 | `uv run pytest tests/pr_submit tests/core tests/cli/reflect -q` | Passes, except failures that also fail on `origin/master` without this change. |
| AC7 | `uv run ruff check` on the changed `.py` files | Clean. |
| AC8 | `git diff --name-only origin/master` | Lists only the files in section 2 (including 2.5) plus this spec and the QA reports under `.dev/reviews/pr-submit-default-monitor-3/`; no `.claude/` path. |
| AC9 | Accuracy | Every statement the change adds about level-3 behaviour, `--yes`, or PR targeting matches the facts listed at the top of section 2.5. |
