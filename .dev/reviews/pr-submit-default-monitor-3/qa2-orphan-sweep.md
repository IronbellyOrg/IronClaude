# QA2 Orphan / Contradiction Sweep (cycle 2) — pr-submit default `--monitor 3`

**Date:** 2026-10-23
**Phase:** doc-qualitative (orphan/contradiction lens), report-only (fix_authorization = false)
**Worktree:** /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-monitor-3

## Verdict

**FAIL** — 7 findings: 3 IMPORTANT (F1, F2, F4) and 4 MINOR (F3, F5, F6, F7). None is in spec section 4.

The default is consistently 3 across the code, command, skill, tests, guides and routing table. No leftover says the default is 2, that level 3 needs an explicit flag, or that a bare run only proposes. The remaining problems come from the revision's own claims:

- the "asks once before its first push" promise is not in the skill's Wave 6 steps (F1);
- `--yes` is not handed from the command to the skill (F2) and is missing from the user-guide syntax (F3);
- the section 4 push-rule exception leaves out the `--yes` qualifier and the CI-fix pushes (F4);
- the level-3 flag is still labelled a "safe flag" (F5);
- the slash command sits in `bash` blocks (F6);
- the `.github` PR template still points at upstream; this one existed before the change (F7).

Tests: 906 passed, 1 xpassed (`tests/pr_submit tests/core tests/cli/reflect`).

## Search log

Scope: `git grep` over the worktree, excluding `.dev/` and `.claude/` (pathspec `':!.dev' ':!.claude'`) unless noted. Hit counts are lines.

| # | Search | Hits | Notes |
|---|---|---|---|
| S1 | `--monitor 2` | 1 | `pr-submit.md:38` level-2 example |
| S2 | `--monitor 1` | 5 | all on the spec AC2 allow-list |
| S3 | `--monitor=2` / `--monitor=1` | 0 | |
| S4 | `DEFAULT_MONITOR` | 7 | fsm.py:30/53/76/758, test_skill_parse.py:15/60, CHANGELOG |
| S5 | `monitor=2`, `monitor == 2`, `defaults to 2`, `default L2`, `default is 2` | 0 | |
| S6 | `default 2` | 7 | all `--max-rounds` or unrelated features |
| S7 | `explicit … (--monitor 3\|level 3\|L3)` and reverse | 0 / 1 | the 1 hit is POST-REFLECT-TASK.md (unrelated L3 = reflect layer) |
| S8 | `never implies`, `opt-in … L3` | 0 | C13 phrase removed |
| S9 | `propose[sd] fixes\|propose-only\|proposes fixes`, `without changing (your )code` | 2 / 0 | both describe L1 only |
| S10 | `no edits` | 12 | all L1 / timeout / unrelated |
| S11 | `never push(es)` | 9 | HOW-WE-WORK:229/272, CHANGELOG, state-machine.md:152, tests |
| S12 | `bare (run\|/sc:pr-submit)` | 7 | CHANGELOG + unrelated CLIs |
| S13 | files mentioning `pr-submit\|pr_submit` (outside the pr_submit package/tests) | 32 files | each opened or grepped |
| S14 | `gh pr create` (excluding tests) | 12 | CLAUDE.md, contributing-code, auggie-review.md, pr-submit.md, SKILL.md, sync workflow |
| S15 | create/open/submit/raise PR / pull request phrasing | ~40 | dev-guide README, git-standards-protocols, release guides, readme_template, post-release skill |
| S16 | root docs (`AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `KNOWLEDGE.md`, `SECURITY.md`) for PR / `gh pr` | 0 instructions on how to open a PR | CONTRIBUTING has "Before opening a PR" checks only |
| S17 | `.github/` tree (template + 4 workflows) | 2 relevant | PULL_REQUEST_TEMPLATE.md, pull-sync-framework.yml |
| S18 | `safe[- ]?flag\|_SAFE_FLAGS\|safe default\|next safe` | 21 | test_how_we_work_routing_table.py:333-344, CLAUDE.md:330, how-we-work.md:3, help.md:91 (src+plugin), diagnosis.py:255 |
| S19 | `--yes` in `src/superclaude/pr_submit`, `sc-pr-submit-protocol` | 5 | fsm.py:64/97/130 parse only; SKILL.md:142; state-machine.md:157 |
| S20 | `state-machine.md\|confirm\|first push\|interactive` in SKILL.md + Wave-6/7/8 refs | 9 | no Wave loads state-machine.md; no confirm step in Wave 6 |
| S21 | `default\|explicit\|opt-in\|arming` × `monitor\|ordinal\|level` in skill refs + scripts | 3 | state-machine.md:159 (C16), detection-contract (unrelated) |
| S22 | `L2 default\|default (ordinal\|level)\|absent --monitor\|no --monitor` in pr_submit src/tests/skill | 2 | test_skill_parse.py:4/58 (updated) |
| S23 | AST scan: `RunConfig(` / `SkillArgs(` / `run_skill(` calls in tests+src that rely on the default ordinal | 0 | no test silently moved from L2 to L3 |
| S24 | `uv run pytest -p no:cacheprovider tests/pr_submit tests/core tests/cli/reflect -q -x` | 906 passed, 1 xpassed | |
| S25 | `cmp` src vs plugin `HOW-WE-WORK.md` | identical | |
| S26 | `monitor\|pr-submit\|safe flag\|mandatory flag` in sc-recommend (src+plugin), recommend.md, help.md | 4 | mandatory-flags rule only |
| S27 | `level (1\|2\|3)\|L[123]` × `pr\|monitor\|push\|review` in docs / core / root | 8 | terminology check ("level 3" process level vs monitor level) |
| S28 | `augment` in docs / core / agents / hooks / templates / plugins | 14 | only the edited pr-submit texts describe L3 |
| S29 | `argument-hint` parity tests; `commands.md` tests | 3 / 0 relevant | no test keeps `commands.md` Syntax in sync with `argument-hint` |
| S30 | `findings_from_logs`, `Finding.severity_hint` default, Wave 8 text | read | L3 also fixes and pushes CI-failure fixes |

## Findings

None of these is listed in spec section 4 (out of scope). F1 is not covered by section 4 item 2: that item covers the missing Python wiring of `--yes`; F1 is about the skill's own wave instructions, which are what the agent actually follows.

### F1 — IMPORTANT — "asks once before its first push" is not in the steps the skill tells the agent to follow

- **Where the claim is made (new text):** `CLAUDE.md:46` ("It asks once before its first push unless you add `--yes`."); `src/superclaude/core/HOW-WE-WORK.md:205`, `:229`, `:254` (and the plugin copy); `docs/guides/prd-skill-release-guide.md:538`; `docs/guides/tdd-skill-release-guide.md:560`; `CHANGELOG.md:11`; `pr-submit.md:57` and `SKILL.md:142` (`--yes` "Skip the one-time confirmation before the first push").
- **What the skill actually instructs:** `SKILL.md:196` (Wave 6, the only place a push happens): "the SKILL performs the actual `git push origin <target_sha>:<target_branch>` … ONLY when the conjunction holds". It has no confirmation step. The one-time confirmation exists only in `refs/state-machine.md:156-159` (§5.3). The wave table (`SKILL.md:177-188`) says refs are "LAZY-loaded per wave, never pre-loaded", and no wave loads `refs/state-machine.md`. Wave 6 loads `thread-reply.md` and `review-retrigger.md`, and neither mentions a confirmation (S20). `fsm.py` parses `--yes` but nothing reads it (spec section 4 item 2).
- **Why it matters:** the new section 4 exception to "Never push without approval" (`HOW-WE-WORK.md:229`) depends on this ask. An agent that follows Wave 6 as written pushes without asking, so the safety promise made in 8 places is not backed by the instructions it runs.
- **Suggested fix:** add to SKILL.md Wave 6, before the push: "**First push of the run:** unless `--yes` was passed or the run is non-interactive, show the files and the diff summary and ask the user once to confirm (`refs/state-machine.md` §5.3). If they decline, record `push_decision.authorized=false` and stop at `halt_before_push`." Alternatively, add `refs/state-machine.md` §5.3 to Wave 6's load list. Either way, record it in spec 2.5 as C28.

### F2 — IMPORTANT — `pr-submit.md` never passes `--yes` to the skill

- **Location:** `src/superclaude/commands/pr-submit.md:74-78` (Activation, "Pass the following context:").
- **Quoted:** "- `--monitor` ordinal … - PR context … - `--output-dir` and `--resume` if supplied."
- **Why:** the revision added `--yes` to `argument-hint` (`:8`) and the Options table (`:57`), but the hand-off list still names every other flag and leaves out `--yes`. A user who types `--yes`, as CLAUDE.md, HOW-WE-WORK and the guides now suggest, may never have it reach the skill. The flag is documented but not handed off.
- **Suggested replacement for line 78:** "- `--output-dir`, `--resume`, and `--yes` if supplied."

### F3 — MINOR — the user-guide Syntax line leaves out `--yes`

- **Location:** `docs/user-guide/commands.md:368`.
- **Quoted:** "/sc:pr-submit [--monitor {0,1,2,3}] … [--output-dir <dir>] [--resume <run-log.jsonl>]"
- **Why:** this line copies `argument-hint`, which now ends with `[--yes]` (`pr-submit.md:8`). Every new PR instruction tells readers to "add `--yes`", but the user-facing syntax reference does not list it. No test keeps the two in sync (S29).
- **Suggested replacement:** add ` [--yes]` to the end of the Syntax line.

### F4 — IMPORTANT — the "Never push without approval" exception leaves out `--yes` and CI-fix pushes

- **Location:** `src/superclaude/core/HOW-WE-WORK.md:229` (plugin copy `:229`).
- **Quoted:** "One exception: after that approved push, `/sc:pr-submit --monitor 3` (workflow 3.11) pushes the review fixes it makes, asking you only once before its first push."
- **Why (two contradictions):**
  1. 3.11 (`:205`), section 5 (`:254`) and `CLAUDE.md:46` all say "unless you add `--yes`". This governing safety rule is the only one of those texts that leaves the qualifier out, and it says it asks "only once" unconditionally. With `--yes` it does not ask at all, and the rule does not warn the reader.
  2. It limits the exception to "the review fixes". At L3, Wave 8 (`SKILL.md:199`) also fixes failing CI checks and pushes those fixes ("After an L3 CI push: do not call `retrigger-review.sh`…"). `findings_from_logs` builds findings with `severity_hint=None`, which routes to Medium, so they are fixed (`ci.py:81-103`, `models.py:161`, `severity_router.py:122-124`). Those pushes fall outside the stated exception, so the rule as written forbids behaviour that the tool it prescribes performs.
- **Suggested replacement:** "One exception: after that approved push, `/sc:pr-submit --monitor 3` (workflow 3.11) pushes the fixes it makes for review findings and failing CI checks, asking you once before its first push (never, if you add `--yes`). If your lead wants to see those fixes before they are pushed, do not add `--yes`, and run it only with their go-ahead." Also consider "fixes … review findings (and failing CI checks)" in `CLAUDE.md:46`, `HOW-WE-WORK.md:205/254` and the two guides.

### F5 — MINOR — the level-3 flag is still labelled a "safe flag"

- **Location:** `tests/core/test_how_we_work_routing_table.py:333-344`: comment "when the guide names a safe flag…", dict `_SAFE_FLAGS = {… "/sc:pr-submit": "--monitor 3", …}`, test `test_named_safe_flags_are_mandatory_on_their_steps`. The guide's flags are also called "safe flags" in `CLAUDE.md:330`, `docs/user-guide/how-we-work.md:3`, `src/superclaude/commands/help.md:91` and `plugins/superclaude/commands/help.md:91`.
- **Why:** `--monitor 1` was a safe, propose-only flag. `--monitor 3` is the most autonomous level: it edits, pushes, replies and resolves. Calling it the "safe flag" contradicts the section 4 push rule, which has to add an exception for it. The task brief lists exactly this case ("'safe' labels attached to the level-3 command").
- **Suggested replacement:** rename to `_MANDATORY_FLAGS` / `test_named_mandatory_flags_are_on_their_steps`, with the comment "when the guide names a required flag for a step, the recommendation must include it". Change "with which safe flags" to "with which required flags" in the four docs. Spec AC1 currently forbids other edits in the C7 test file, so record this as C29 in spec 2.5. Leave `CHANGELOG.md:21` alone (historical entry).

### F6 — MINOR — a slash command is placed inside `bash` code blocks

- **Location:** `docs/developer-guide/contributing-code.md:187-190` (` ```bash ` holding `git push origin …` and then `/sc:pr-submit --monitor 3 …`); `CLAUDE.md:48-50` (` ```bash ` holding only `/sc:pr-submit --monitor 3 …`).
- **Why:** `/sc:pr-submit` is a Claude Code command, not a shell command. A contributor who pastes the contributing-code block into a terminal runs `git push` and then gets "No such file or directory" for `/sc:pr-submit`. That makes the new mandatory instruction fail exactly when someone follows it literally.
- **Suggested replacement:** contributing-code: keep `git push origin feature/your-feature-name` in a `bash` block, then "Then, in Claude Code:" followed by a ` ```text ` block with the `/sc:pr-submit` line. CLAUDE.md: change the block language to `text` (or add "in Claude Code:").

### F7 — MINOR (existed before this change; not listed in spec section 4) — the PR template sends people to upstream

- **Location:** `.github/PULL_REQUEST_TEMPLATE.md:21` "For external contributions: Followed the flow of fork → topic branch → upstream PR." and `:23` "`git rebase upstream/main` completed (no conflicts)."
- **Why:** this checklist is shown for every PR opened in the GitHub web UI on the fork. It tells contributors to open upstream PRs and to rebase on `upstream/main`. That contradicts the `CLAUDE.md` rule (NEVER open PRs against `SuperClaude-Org`; pre-PR check 2 rebases onto `origin/master`) and the new "always use `/sc:pr-submit --monitor 3`" instruction. It is the only PR instruction left in `.github/` that names another way to open a PR. (`/sc:pr-submit` passes `--body`, so the template does not appear in PRs it opens. The template only affects PRs opened by the non-mandated web path.)
- **Suggested replacement:** ":21" → "- [ ] Opened with `/sc:pr-submit --monitor 3` on `IronbellyOrg/IronClaude` (fallback: `gh pr create --repo IronbellyOrg/IronClaude`)." ":23" → "- [ ] Branch rebased onto `origin/master` (no conflicts)." If the team does not want this fixed in this PR, add it to spec section 4 so it is out of scope on record.

## Hits judged fine

| File:line | Text | Why it is fine |
|---|---|---|
| `src/superclaude/commands/pr-submit.md:36-39` | per-level examples `--monitor 0/1/2/3` | Each level is typed explicitly to document all four levels (spec section 3). |
| `src/superclaude/commands/pr-submit.md:18` | "runs `/sc:pr-submit --monitor {0,1,2,3}` to open a PR (and optionally arm the monitor)" | "Optionally" is still true (`--monitor 0`); it makes no claim about the default. |
| `src/superclaude/commands/pr-submit.md:19` | hook "NEVER arms a monitor itself" | The C13 removal is done; "implies level-3 without explicit invocation" is gone (S8 = 0). |
| `src/superclaude/commands/pr-submit.md:26`, `:47`; `SKILL.md:135` | default 3 | Agrees with `fsm.py:30`. |
| `src/superclaude/commands/pr-submit.md:86`, `SKILL.md:229` | "apply edits at L1 or push/reply at L2" | Describes per-level ceilings; does not assume a default. |
| `tests/pr_submit/test_monitor_arm.py:3,27` | `--monitor 1` | Exercises L1 explicitly (spec AC2 allow-list). |
| `docs/user-guide/commands.md:363` | "at `--monitor 1` or higher, arm…; With no `--monitor` it runs level 3." | Describes levels; the default is stated. "Level 3" sits right after "`--monitor`", so it is not mistaken for process level 3 (`commands.md:695`). |
| `CHANGELOG.md:11-17` | new entry | Accurate against SKILL Waves 2-3/6 and the C22/C23 text; no "without asking". (It inherits F4's omission of CI pushes, which is minor and fixed by F4.) |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:78` | "(diagnose/propose-only) verifies before proposing" | Describes L1 troubleshoot routing, not the default. |
| `src/superclaude/pr_submit/fsm.py:672, 937, 1011`; `models.py:209`; `state-machine.md:44,66`; `SKILL.md:194` | "PROPOSED … no edits" | Describe the L1 ceiling only. |
| `src/superclaude/pr_submit/fsm.py:53, 76, 758` | `= DEFAULT_MONITOR` | Read the constant; the AST scan (S23) shows no test relies on the old L2 default of `RunConfig`/`SkillArgs`. |
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:137`, `pr-submit.md:48`, `refs/loop-guard.md` | `--max-rounds` default 2 | Not the `--monitor` default (spec section 3). |
| `src/superclaude/pr_submit/contract_setup/diagnosis.py:255` | "Next safe step:" | Rendered only by `render_pr_submit_missing_contract_halt`, which never yields a READY diagnosis, so it never labels `/sc:pr-submit --monitor 3` as safe (`test_contract_setup_pr_submit_integration.py:238-239` pins `"--monitor" not in next_command`). |
| `src/superclaude/commands/reflect.md:82`, `plugins/superclaude/commands/reflect.md:73`, `sc-reflect-protocol/SKILL.md:67` | "the next command to run" | C26 is done; "next safe command" is gone. |
| `src/superclaude/cli/reflect/commands.py:200`, `diagnosis.py:380` | `/sc:pr-submit --monitor 3{pr_arg}` | Matches C17/C18. The `--pr` flag being unparsed is spec 4.3(c), out of scope. |
| `CLAUDE.md:41` NEVER "bare `gh pr create` without `--repo IronbellyOrg/IronClaude`" vs `:46` "`gh pr create --repo <repo>` where `<repo>` is what `gh repo view` reports" | — | No contradiction: pre-PR check 1 (`:60`) makes `gh repo view` print `IronbellyOrg/IronClaude`, so the command `/sc:pr-submit` runs is the allowed form. Rationale `:66` ("explicit `--repo` on every invocation") still holds. |
| `CLAUDE.md:60` "gh prefers an `upstream` remote over `origin`" | — | Correct for gh's default-repo resolution (remote order `upstream` > `github` > `origin` when no default is set); matches spec 2.5 fact 4. |
| `CLAUDE.md:52-56` fallback `gh pr create --repo IronbellyOrg/IronClaude …` | — | Clearly labelled "Fallback only". `contributing-code.md:185` likewise labels its fallback. |
| `HOW-WE-WORK.md:202` "Push. Only after your lead approves." | — | Governs the first branch push; 3.11 step 6 and the section 4 exception cover the later fix pushes (spec section 3). |
| `HOW-WE-WORK.md:272` `/sc:git` "Still never push without approval." | — | Scoped to `/sc:git` (spec section 3). |
| `HOW-WE-WORK.md:254` "Always pass `--monitor 3`" while the default is already 3 | — | Redundant but consistent (an explicit flag survives a future default change). `--monitor 0` advice matches 3.11 and the routing row notes. |
| `HOW-WE-WORK.md:323` routing row `6: --monitor 3`, notes "`--monitor 0` to only open the PR", `changes_files` = yes | — | Consistent with 3.11 and section 5; plugin copy is byte-identical (S25). |
| Severity / thread claims (`CLAUDE.md:46`, `HOW-WE-WORK.md:205,254`, guides) | "Medium severity or higher (lower ones are only reported)", "resolves the review comments it fixed" | Verified: `severity_router.py:56-58, 202-215` (Medium → `--fix`, High/Critical → deep fix, Low/Nit → report-only); `SKILL.md:193` unverified → REPORT_ONLY; `refs/thread-reply.md` §1/§3 replies to and resolves the remediated finding's own thread. |
| `src/superclaude/commands/auggie-review.md:18,126-128` | bare `gh pr create --title …` in the hook example | Describes when the (missing) hook fires, not how to open a PR; it is an installed primitive used in other repos; `offer-pr-review.sh` absence is spec 4.3(b). |
| `.github/workflows/pull-sync-framework.yml:115` | `gh pr create --repo "$GITHUB_REPOSITORY" …` | CI automation inside the fork's own Actions run; `--repo` is pinned to the fork; not a human instruction. |
| `docs/developer-guide/README.md:189-192` "Fork the repository … Submit pull request" | — | Generic documentation-contribution steps that name no way to open a PR; existed before this change. |
| `docs/developer-guide/git-standards-protocols.md:285-360, 634` "Create PR to feature/* / release/* / main" | — | Imported GFXA process doc (id `GFXAI-GIT-STANDARDS-PROTOCOLS`, status "To Do") describing branch promotion gates for another project; names no way to open a PR. |
| `src/superclaude/templates/documents/readme_template.md:420` | "Open a Pull Request against `[base branch]`" | Template text for READMEs of other projects. |
| `src/superclaude/skills/sc-post-release-protocol/SKILL.md:340,348` | PR target = repo's own `origin` | Generic, for any project; consistent with the fork rule. |
| `src/superclaude/commands/swarm-wizard.md:96` | mentions `/sc:pr-submit` without a level | Spec section 3. |
| `CONTRIBUTING.md:28-41` "Before opening a PR, run…" | — | Lint/test checks only; says nothing about how to open the PR. |
| `AGENTS.md`, `README.md`, `KNOWLEDGE.md`, `PROJECT_INDEX.md/.json` | — | No PR-opening instruction or default-level text (S13/S16). |
| `src/superclaude/core/CLAUDE.md` level table | "level 3" = process level | Does not mention `/sc:pr-submit`; HOW-WE-WORK level table not edited (spec section 3). |
| `SKILL.md:144-147, 190, 217, 226` "origin's `owner/repo` via `gh repo view`" and checks after `gh pr create` | — | Existed before this change; spec 4.3(a), out of scope. |
| `pr-submit.md`/`SKILL.md` `--yes` rows citing `refs/state-machine.md` §5.3 | — | §5.3 heading exists at `state-machine.md:145` and contains the `--yes` sentence (`:157`). (The gap in what the agent executes is F1.) |

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. No Inherited Structural Verdict was supplied, so this ran standalone. I did not trust the cycle-1 reports (`qa-orphan-sweep.md`, `qa-spec-conformance.md`) or the sibling `qa2-spec-conformance.md`; I did not read them.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Default consistency: verified `fsm.py:30` = 3 and all three readers (`:53`, `:76`, `:758`) by Bash `sed`. I AST-scanned every `RunConfig(`/`SkillArgs(`/`run_skill(` call in `tests/` and `src/` for reliance on the default ordinal (0 hits) and ran 906 tests (pass).
- First-push confirmation (F1): read SKILL.md in full; grepped SKILL.md and Wave 6/7/8 refs for `state-machine.md|confirm|first push|interactive`. Only `state-machine.md:157` holds the rule, and no wave loads it.
- `--yes` plumbing (F2, F3): read `pr-submit.md` in full (Activation list `:74-78`) and `commands.md:358-372`; grepped `--yes` across the package and skill.
- Push-rule scope (F4): read `SKILL.md:199` Wave 8, `ci.py:81-130`, `models.py` `Finding` fields and `severity_router.py:56-58, 122-124, 202-215`, which confirm that CI failures route to Medium → fix → L3 push.
- Severity and thread claims: checked against `severity_router.py` and `refs/thread-reply.md` §1/§3 (accurate).
- "Safe" labels (F5): grepped `safe[- ]?flag|_SAFE_FLAGS|next safe`; read `test_how_we_work_routing_table.py:320-358`, `diagnosis.py:235-257` and the integration test that pins the halt's next command (`:238-239`), which cleared `diagnosis.py:255`.
- PR instructions repo-wide: `gh pr create` and create/open/submit-PR phrasing searches; read `.github/PULL_REQUEST_TEMPLATE.md`, `contributing-code.md:161-209`, `prd-skill-release-guide.md:515-539`, `git-standards-protocols.md` header and hits, `auggie-review.md:12-22,115-135`, and the root docs.
- Internal consistency of HOW-WE-WORK: compared `:202`, `:205`, `:229`, `:254`, `:272`, `:323` side by side; `cmp` with the plugin copy (identical).

**Confidence:** Verified: 8/8 lens checks (default leftovers, explicit-L3 leftovers, propose-only leftovers, PR instructions, new-text internal contradictions, `--yes` documentation and parsing, "safe" labels, factual accuracy) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%.
**Tool engagement:** Read: 7 | Grep (via Bash `git grep`/`grep`): ~22 | Glob: 0 | Bash (other: diff, sed, pytest, AST scan, cmp): ~8. No web research was needed (no Tavily/WebFetch calls).
**Not covered:** `.claude/` dev copies and `.dev/` history (excluded by the brief); `make verify-sync` (`make` is unavailable, as spec AC5 notes).
