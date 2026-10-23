# QA Report: Orphaned or Contradictory Instructions Sweep

**Topic:** sc:pr-submit cleanup (P1 origin-first target, P2 --pr, P3 hook refs, P4 --yes)
**Date:** 2026-10-24
**Phase:** doc-qualitative (orphan/contradiction lens)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Base:** HEAD 070399eb; change under review = uncommitted working tree

## Verdict

**FAIL.** There are 6 real orphans or contradictions: 2 IMPORTANT and 4 MINOR.

- F1: `auggie-review.md:160` still says "hook-driven".
- F2: the `fsm.py:480` docstring still states the old gh-first resolution order.
- F3, F4: `augment-poll.md:8` and `ci-poll.md:8-9` say the pin is "origin's `nameWithOwner`".
- F5, F6: in `test_static_grep.py`, the comment at :32-34 and the T-105 assertion at :180-183 still treat `gh repo view` as the primary resolution.

The hook registrations, the `--yes` removal, the `--pr` wiring and the contract-status READY command are all clean.

## Search log

All searches ran on the working tree with `git grep -n -i` (tracked files, so the
staged deletion of `tests/pr_submit/test_hook_update.py` is excluded), excluding
`.dev/` and `.claude/` unless stated. Counts are raw line hits before judging.

| # | Search | Scope | Hits | Real problems |
|---|---|---|---|---|
| S1 | `offer-pr-review` | repo | 1 | 0 (CHANGELOG removal note) |
| S2 | `PR-creation hook` | repo | 1 | 0 (same CHANGELOG line) |
| S3 | `post-PR-create` | repo | 0 | 0 |
| S4 | `pr-creation` | repo | 1 | 0 (same CHANGELOG line) |
| S5 | `post-pr` | repo | 43 | 0 (all `--no-post-pr` / `--post-pr` flags, "post-process", "post-PR #66" etc.) |
| S6 | `PostToolUse` | repo | 58 | 0 (freshness / auggie-flag hooks and eval suites; none registers a `gh pr create` matcher) |
| S7 | `after .*gh pr create` | repo | 1 | 0 (contributing-code.md fallback sentence) |
| S8 | `offer.*pr-submit`, `offer.*auggie-review` | repo | 2 each | 0 (CHANGELOG; SKILL.md:196 Wave 6b `--no-remediation-offer` text) |
| S9 | `three activation`, `two activation`, `activation path` | repo | 0 / 1 / 6 | 0 (pr-submit.md:16 now "two"; reflect.md is unrelated) |
| S10 | `hook` in pr-submit + auggie-review command/skill/package/tests | targeted | 11 | **1** (auggie-review.md:160) |
| S11 | `hook-driven`, `pr[- ]creation`, `after ... PR created` phrases | repo | 4 | **1** (auggie-review.md:160, same as S10) |
| S12 | `offer\|pr-review\|gh pr` in `.claude/settings.json`, both `hooks.json`; `.sh"` lists in `install_hooks.py` | targeted (incl. tracked `.claude/settings.json`) | 0 | 0 |
| S13 | `offer-pr-review` in `~/.claude/settings.json`, main-checkout `.claude/settings.json`, `~/.claude/hooks/` | read-only outside worktree | 0 | 0 |
| S14 | plugin mirrors of pr-submit / auggie-review (`git ls-files plugins`) | plugins/ | 0 copies | 0 |
| S15 | `gh repo view` | repo | 22 | **2** (test_static_grep.py:32-34, :180-183) |
| S16 | `defaultBranchRef` | repo | 3 | 0 (all name `"$REPO"` or are pure prose in fsm.py:527) |
| S17 | `nameWithOwner` | repo | 18 | **3** (fsm.py:480, augment-poll.md:8, ci-poll.md:8-9) |
| S18 | `resolv\|remote get-url\|origin` in `refs/*.md`, `pr_submit/`, `tests/pr_submit` | targeted | ~60 | 0 new (confirms S17 set) |
| S19 | `--yes\b` near pr-submit/monitor | repo | 4 | 0 (CHANGELOG + D3 rejection test) |
| S20 | `--yes\b` in AC3 scope + docs/user-guide + plugins | targeted | 3 | 0 (D3 test; `/sc:swarm-wizard --yes` is a different command) |
| S21 | `\.yes\b\|\byes=\|"yes"` in pr_submit, cli, skill | targeted | 22 | 0 (installer `yes=yes` in cli/main.py, swarm verdicts; none in pr_submit) |
| S22 | `one-time confirm\|confirm before push\|interactive confirm` | pr-submit skill, command, docs, core | 1 | 0 (state-machine.md:157, updated) |
| S23 | `sc:pr-submit` invocations carrying a PR number or `--pr` | repo | ~50 | 0 (all `--pr <N>` / `--pr 42` / `--pr <number>`; none use a positional number or `#N`) |
| S24 | `--pr\b\|pr-submit` in `contract_setup/`, `cli/reflect/`, their tests | targeted | ~40 | 0 |
| S25 | `existing PR\|attach (to )?(the\|an\|a) \|already-open PR` | pr-submit surfaces, core, docs, plugin HOW-WE-WORK, CLAUDE.md | 8 relevant | 0 (all name `--pr <N>` or are unrelated "attach" commands) |
| S26 | `pr-submit\|auggie-review` x `hook\|offer\|activat\|--yes\|attach\|gh repo` | docs, core, KNOWLEDGE, README, plugin sc-recommend | 4 | 0 |
| S27 | `pr-submit\|auggie-review` in other commands/agents/skills | src/superclaude | 10 | 0 |
| S28 | `test_hook_update\|_skill_and_hook_files\|HOOK\b` | tests, src | 9 | 0 (other hooks' tests; nothing imports the deleted helper) |
| S29 | Runtime parse of the contract-status READY string via `parse_args` | `uv run --no-sync python -B` | 3 cases | 0 (`--pr 42` -> pr=42; `--pr <number>` placeholder rejected as expected; `--yes` rejected) |

## Findings

| # | Severity | Location | Quoted text | Why it is a problem | Suggested replacement |
|---|---|---|---|---|---|
| F1 | IMPORTANT | `src/superclaude/commands/auggie-review.md:160` (Boundaries, "Will Not") | "Activate on conversational keywords ("review", "audit", "check") — explicit invocation or hook-driven only" | Orphaned P3 reference. The "hook-driven" path is the removed `offer-pr-review.sh` activation. It contradicts the same file's Triggers list (lines 15-18, now only "Direct invocation" and "Programmatic call"), and the matching skill line `sc-auggie-review-protocol/SKILL.md:361` was updated by C6 but this sibling line was missed. The spec lists C4/C5 for this file but not line 160, so AC1 accuracy and AC8 fail here, and AC2's grep misses it because it does not contain "PR-creation hook". | "Activate on conversational keywords ("review", "audit", "check") — explicit invocation or a programmatic call from another `/sc:*` command only" |
| F2 | IMPORTANT | `src/superclaude/pr_submit/fsm.py:479-481` (`pr_target_ok` docstring) | "the SKILL resolves it at runtime (origin's ``nameWithOwner``, fallback the origin remote URL) and passes it in." | Unchanged pre-P1 text that states the OLD order: `nameWithOwner` (the `gh repo view` result) first, origin URL as fallback. It now contradicts SKILL.md Wave 0 (line 189), the four scripts, `test_pre_pr_checks.py:6-7`, and the CHANGELOG. The sibling `origin_ok` docstring (line 495-496) is neutral and fine. | Note that `fsm.py` is in the T-N50 core-pure set, so the text must not contain the words `gh` or `git`. For example: "the SKILL resolves it at runtime (the `owner/repo` parsed from the origin remote URL, with the host CLI's repo lookup only as a fallback when origin has no URL) and passes it in." |
| F3 | MINOR | `src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md:8` | "pins the RESOLVED `--repo <owner/repo>` (origin's `nameWithOwner`, FR-1.3 / AC-7)" | `nameWithOwner` is the JSON field of `gh repo view`. Wave 0 now parses `$REPO` from `git remote get-url origin` and uses `gh repo view` only as a fallback. This is the "origin's nameWithOwner" wording that A2/A3 removed from SKILL.md and pr-submit.md, left behind in the refs. A reader of the ref is told the pin is gh's value. | "(origin's `owner/repo`, parsed from `git remote get-url origin`, FR-1.3 / AC-7)" |
| F4 | MINOR | `src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md:8-9` | "pins the RESOLVED `--repo <owner/repo>` (origin's `nameWithOwner`, FR-1.3 / AC-7)" | Same as F3, in the CI poller contract. | Same replacement as F3. |
| F5 | MINOR | `tests/pr_submit/test_static_grep.py:32-34` (comment above `_REPO_RESOLVE`) | "The `gh repo view` resolution idiom — the de-hardcoding primitive. It reads the CURRENT checkout's `owner/repo` (so downstream calls can pin `--repo "$REPO"`)" | After P1, `gh repo view` is only the fallback. The primary resolution is `git remote get-url origin`. Calling gh "the de-hardcoding primitive" that "reads the CURRENT checkout's owner/repo" also goes against the P1 reasoning, because gh can report the upstream parent. The module docstring (lines 4-8) was updated by A8 and this comment was not, so the two now disagree in the same file. | "The `gh repo view` fallback resolution idiom (used only when the origin remote has no URL). It names no PR target itself, so it counts as repo-scoped on its own." |
| F6 | MINOR | `tests/pr_submit/test_static_grep.py:180-183` (T-105 body) | `assert "nameWithOwner" in script_text, ("poll script does not resolve the target repo (expected `gh repo view --json nameWithOwner`)")` | Its own docstring (line 173, updated by A8) says the script resolves "the origin remote, fallback `gh repo view`". The assertion still treats the gh fallback as the proof that the script resolves the repo. If the gh fallback were dropped, which P1 allows, T-105 would fail with a misleading message. If the origin line were dropped, T-105 would still pass. The new ordering test covers the origin line, so this is a stale contradiction, not a coverage gap. | `assert "git remote get-url origin" in script_text, ("poll script does not resolve the target repo from the origin remote (expected `git remote get-url origin`)")` |

## Hits judged fine

| Location | Reason |
|---|---|
| `CHANGELOG.md:7,11,12,16,17` | The E1 record of P1-P4. It names `offer-pr-review.sh`, `gh repo view` and `--yes` only as removed or replaced behaviour. AC2 expects exactly this line. |
| `CHANGELOG.md:25` | Updated by E1; it no longer claims `/sc:pr-submit` takes its target from `gh repo view`. |
| `CHANGELOG.md:27` | Updated by E1; the `--yes` clause is gone. |
| `CLAUDE.md:46` | Updated (A7): "`<repo>` comes from the `origin` remote". |
| `CLAUDE.md:60` (pre-PR check 1, `gh repo view --json nameWithOwner` must print the fork) | Spec section 3 keeps this on purpose. It protects any bare `gh` use and no longer claims the skill depends on it. |
| `CLAUDE.md:62` "After PR creation, verify the returned URL" | A manual post-create check, not a hook. |
| `src/superclaude/commands/pr-submit.md:16-19` | "two activation paths": Direct and Programmatic. The count matches the list. |
| `src/superclaude/commands/pr-submit.md:7,26,53,76` | `--pr <N>` is in the argument-hint, Required Input, Options and handoff context. |
| `src/superclaude/commands/pr-submit.md:29` | STOP rule now says "parsed from `git remote get-url origin`". |
| `src/superclaude/commands/pr-submit.md:51` | `gh repo view "$REPO" --json defaultBranchRef` names the repo explicitly. |
| `src/superclaude/commands/pr-submit.md:89` | "(offered together by the post-PR-create hook)" removed. |
| `src/superclaude/commands/pr-submit.md:18` "runs `/sc:pr-submit --monitor {0,1,2,3}` to open a PR" | It describes the main path. Attaching is documented in the Required Input and Options rows, so this does not contradict `--pr`. |
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:136,143-146,148,189` | Required Input has `--pr <N>`. The STOP rule says origin parsed via `git remote get-url origin`. The CI preflight covers "attaching to an existing PR". Wave 0 resolves origin first, uses `gh repo view` only as a fallback, reads the base with `gh repo view "$REPO"`, rebases before create, and the hook sentence is gone. |
| `SKILL.md:143-146` / Wave 0 "confirm `git remote -v` shows origin = `$REPO`" | Now nearly a self-comparison, because `$REPO` comes from origin. It is still meaningful on the `gh repo view` fallback path, where origin has no URL and the check HALTs. The spec (A1) keeps it on purpose. This is not a contradiction. |
| `SKILL.md:196` "`--no-remediation-offer`" | Wave 6b's auggie fallback flag, unrelated to the removed hook. |
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/*.sh` lines 19-20 / 34-35 / 52-56 / 44-48 | All four scripts try origin first and `gh repo view` second. The comments in reply-resolve and retrigger say "(the origin remote, then gh repo view)". The headers at reply-resolve-thread.sh:15 and retrigger-review.sh:15 already say "origin's owner/repo". |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:157` | `--yes` clause removed; "Wave 6 has no confirm step" stays. |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md:4`, `review-retrigger.md:28` | Say "RESOLVED origin repo" / "origin's `owner/repo`". Neutral, so they match the new order. |
| `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:361` | Updated (C6) to "explicit ... invocation or a programmatic call from another `/sc:*` command only". |
| `src/superclaude/commands/auggie-review.md:15-18` | Two activation items, renumbered (C4). The hook example section was removed (C5). |
| `src/superclaude/cli/install_hooks.py:76-77` | Comment now names only `reject-workspace-writes.sh`. No script list (`_FRESHNESS_SCRIPTS`, lines 42-78) contains `offer-pr-review.sh`, so the installer installs nothing that is gone. |
| `.claude/settings.json` (tracked, 28 lines), `src/superclaude/hooks/hooks.json`, `plugins/superclaude/hooks/hooks.json`, `~/.claude/settings.json` | No registration of `offer-pr-review.sh` and no `gh pr create` matcher. `src/superclaude/hooks/scripts/` and `plugins/superclaude/hooks/scripts/` contain no such script. |
| `src/superclaude/pr_submit/fsm.py:64,97,118-119,132` | `pr: int \| None`, `--pr type=int`, `< 1` rejection, `pr=ns.pr`. `yes` is gone everywhere. |
| `src/superclaude/pr_submit/fsm.py:492-503,524-528` (`origin_ok`, `needs_rebase` docstrings) | They say "resolves it from origin" / "resolved ... from the repo's `defaultBranchRef`", which does not depend on the order. |
| `src/superclaude/pr_submit/contract_setup/diagnosis.py:374,380` and `src/superclaude/cli/reflect/commands.py:194-200` | The READY command `/sc:pr-submit --monitor 3 --pr <N>` now parses (verified at runtime: `pr=42`). The `--pr <number>` placeholder is rejected by argparse (`type=int`), as a placeholder should be: the operator fills in the number. Pinned by `test_contract_setup_diagnosis.py:290,311` and `test_detection_contract.py:98-106`. |
| `src/superclaude/commands/reflect.md:77-82`, `sc-reflect-protocol/SKILL.md:63-67`, `plugins/superclaude/commands/reflect.md:73` | Describe `reflect contract-status --pr <number>` (a different CLI's flag). The "next command" is not restated here, so there is nothing to contradict. |
| `docs/user-guide/commands.md:368` | Syntax gains `[--pr <N>]` (B4); no `--yes`. |
| `docs/user-guide/commands.md:542` `/sc:swarm-wizard ... [--yes]` | A different command's flag. |
| `docs/user-guide/commands.md:184`, `HOW-WE-WORK.md:201,253,323` (core + plugin mirror), release guides | `--post-pr` / `--no-post-pr` flags of auggie-review, not the hook. |
| `src/superclaude/cli/main.py:339` `yes=yes` | The installer's own confirm flag, unrelated to pr-submit. |
| `tests/pr_submit/test_static_grep.py:1-14,106,124,173,533-551,577` | The module docstring and T-105 docstring are updated (A8). `_repo_scoped`'s docstring and the D3 case at line 577 test that the fallback idiom is classified as scoped, which is still true. The new ordering test exists (A6). |
| `tests/pr_submit/test_pre_pr_checks.py:6-8` | Updated to "``git remote get-url origin``, fallback ``gh repo view``". |
| `tests/pr_submit/test_skill_parse.py:94-105` | B5 and D3 tests; the only `--yes` mentions in AC3 scope. |
| `tests/pr_submit/test_validation_gate.py:45` | The path now points to an existing script (`src/superclaude/hooks/scripts/reject-workspace-writes.sh`, confirmed by `ls`). |
| `tests/hooks/*` `HOOK = ...` | Constants for other hooks (auggie-first, auggie-flag-clear), unrelated. |
| `.github/PULL_REQUEST_TEMPLATE.md:21`, `docs/developer-guide/contributing-code.md:185,194`, PRD/TDD release guides | Tell the user to open PRs with `/sc:pr-submit --monitor 3 --head ...`. No hook, `--yes` or target-order claim. |
| `.claude/` dev copies, `.dev/` history | Out of scope (spec section 3). |

## Self-Audit

There are six findings, so the zero-finding justification does not apply. What was checked:

- **Hook (P3):** 11 phrasing variants (S1-S11), plus every hook-registration surface: the tracked `.claude/settings.json`, both `hooks.json` files, the installer script lists, `~/.claude/settings.json`, and the hook script directories (S12-S14). Only F1 survived, and only because it says "hook-driven" without the strings that AC2 greps for.
- **Target (P1):** every `gh repo view`, `defaultBranchRef` and `nameWithOwner` hit (S15-S18), each read in context. F2-F6 are text the A-series edits did not touch. The four scripts, SKILL.md Wave 0 and the STOP rules are correct.
- **`--yes` (P4):** clean (S19-S22).
- **`--pr` (P2):** clean (S23-S25). The contract-status READY string was run through the real `parse_args` (S29).

**(a) Reliance list (rf-qa PASS items skipped for structural re-check):**
- No Inherited Structural Verdict was supplied. Nothing was relied on; every check above was run independently.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Contract-status READY string vs parser: ran `parse_args(["--monitor","3","--pr","42"])`, which gave `pr=42`; `--yes` gave argparse exit 2.
- fsm.py core-purity constraint on the F2 fix: read `test_static_grep.py:132-143`, where the `\bgh\b|\bgit\b` token ban covers `fsm.py`. The suggested replacement therefore avoids both words.
- Hook absence on disk: `ls src/superclaude/hooks/scripts plugins/superclaude/hooks/scripts` shows no `offer-pr-review.sh`. The C10 replacement path `reject-workspace-writes.sh` exists.
- Activation-count consistency: read `auggie-review.md:15-18` against `:160` and `sc-auggie-review-protocol/SKILL.md:361`. This is how F1 was found.
- Unchanged pre-P1 docstring: `git show HEAD:src/superclaude/pr_submit/fsm.py` confirms that lines 479-481 are unchanged from the base (F2).

**Confidence:** Verified: 8/8 lens items (gh-repo-view-first text, bare defaultBranchRef, hook mentions, hook registration, activation counts, `--yes`, `--pr` attach forms, contract-status vs parser) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 2 | Grep: 0 (searches done with git grep via Bash) | Glob: 0 | Bash: 21. No web research was needed, so Tavily was not used.
**Limitations:** `.claude/` dev copies were not checked, by instruction. `make verify-sync` was not run (no `make`). Tests were not run, because this is a report-only orphan sweep.
