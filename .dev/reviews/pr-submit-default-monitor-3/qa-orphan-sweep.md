# QA Report — Orphaned or Contradictory Instructions Sweep (doc-qualitative)

**Topic:** `/sc:pr-submit` default `--monitor 3` + repo-wide PR instruction change
**Date:** 2026-10-23
**Phase:** doc-qualitative (orphan/contradiction lens)
**Fix cycle:** N/A
**fix_authorization:** false (report-only)

---

## Verdict

**FAIL**: 5 real contradictions or orphans (3 IMPORTANT, 2 MINOR). None of them is in a C1-C21 edit itself. Each is a statement elsewhere in the repo that the new level-3 default or the new wording now contradicts.

| # | Severity | One-line summary |
|---|---|---|
| F1 | IMPORTANT | HOW-WE-WORK section 4 says "Never push without approval". The same guide now sends users to a command that pushes review fixes on its own. |
| F2 | IMPORTANT | `refs/state-machine.md` section 5.3 requires `--yes` or an interactive confirm before the first push. The new CHANGELOG, HOW-WE-WORK and CLAUDE.md wording says level 3 pushes "without asking" / "on its own". |
| F3 | IMPORTANT | The new CLAUDE.md text says `/sc:pr-submit` targets "origin's `owner/repo`". Wave 0 actually resolves the target with `gh repo view`, and gh ranks an `upstream` remote first. CLAUDE.md itself says an `upstream` remote exists. |
| F4 | MINOR | The reflect docs call the contract-status next command "the next safe command". That command is now the full push/reply/resolve level. |
| F5 | MINOR | `docs/developer-guide/contributing-code.md` still tells contributors to push and "Create PR on GitHub". That bypasses `/sc:pr-submit` and contradicts spec goal 2. |

## Search log

All searches ran inside the worktree. `git grep` excluded `:!.dev` and `:!.claude` unless noted. Hit counts are matching lines.

| # | Search (angle) | Hits | Notes |
|---|---|---|---|
| S1 | `git grep -E -- '--monitor[ =]?[012]\b'` (explicit low levels) | 26 | All reviewed; see Hits judged fine. |
| S2 | `git grep -i -E 'default(s\|ed)?( to\| is\|:\| of\| =)? ?(L\|level \|ordinal )?2\b\|DEFAULT_MONITOR\|default_monitor\|monitor.{0,30}default\|default.{0,30}monitor'` (default-is-2 statements) | 31 | No hit says the `--monitor` default is 2. Every "default 2" hit is about `--max-rounds`, reflect max-cycles, roadmap attempts/agents, `MAX_NUDGE_*` or swarm floor. |
| S3 | `git grep -E 'gh pr create'` (alternative PR paths) | 18 lines / 9 files | Non-test hits reviewed; the CI workflow, the CLAUDE.md fallback and the skill Wave 0 are fine. |
| S4 | `git grep -i -E 'explicit(ly)? .{0,40}(level.?3\|--monitor 3\|L3)\|...\|never (implies\|push)\|without explicit invocation\|typed'` (level 3 needs an explicit flag) | 22 | The "NEVER implies level-3" text is gone (C13). Surfaced HOW-WE-WORK:229 and :272 "never push without approval" (F1). |
| S5 | `git grep -i -E 'propos(e\|es\|ing) (fixes\|edits)\|without changing your code\|no edits\|makes no edits\|only propos\|never pushes\|does not push\|HALT before push\|...'` (bare run only proposes / never pushes) | ~50 | Every remaining hit describes L1/L2 explicitly, auggie-review, or a test of an explicit ordinal. The "proposes fixes without changing your code" text is gone. |
| S6 | `git grep -E 'pr-submit\|pr_submit'` in `src/superclaude/skills/sc-recommend`, `plugins/superclaude/skills/sc-recommend`, `src/superclaude/agents`, `src/superclaude/hooks`, `src/superclaude/templates`, `AGENTS.md`, `README*`, `src/superclaude/core` (excluding HOW-WE-WORK) | 0 | The recommend machinery has no hardcoded level; it reads the routing table. |
| S7 | `git grep -i 'offer.pr.review'` + `git ls-tree origin/master src/superclaude/hooks/scripts` + `ls` (the PR-creation hook's monitor hint) | 7 refs; hook file absent | Out of lens; see Observations. |
| S8 | `git grep 'monitor'` in recommend code/skills and `tests/cli`, `tests/core`, `tests/skills` | 1 | Only `test_how_we_work_routing_table.py:338` (`--monitor 3`, C7). |
| S9 | `git grep -i -E 'safe flag\|safe-flag\|safest\|safe setting\|safe default'` (is level 3 still called "safe"?) | 24 | The "safe flags" framing of HOW-WE-WORK (CLAUDE.md:330, CHANGELOG:19, help.md:91, docs/user-guide/how-we-work.md:3, `_SAFE_FLAGS` test) is judged fine; see below. |
| S10 | `git grep -i -E 'next safe\|safe next\|safe command'` | 7 | Surfaced F4. |
| S11 | `git grep -i -E '(open\|create\|submit\|raise\|file) (a \|the \|your )?(pr\|pull request)\b'` over AGENTS/README/CONTRIBUTING/docs/core/commands/agents/skills/templates/plugins/.github, minus pr-submit lines (other PR instructions) | 21 | Surfaced F5; the rest are judged fine. |
| S12 | `git grep -i -E 'pr-submit\|pr_submit'` across docs, plugins, core, agents, commands, skills (minus pr-submit's own files) | 13 | All reviewed. |
| S13 | `git grep -i -E 'monitor.?(ordinal\|level)\|ordinal.{0,20}(2\|two)\b\|L2 default\|...\|monitor_ordinal=2\|monitor=2'` (code/tests assuming the L2 default) | 40+ | Every `monitor_ordinal=2` is an explicit L2 test. |
| S14 | `git grep -n -A7 -E 'RunConfig\($'` plus the single-line `RunConfig(` list (tests depending on the `RunConfig.monitor_ordinal` default, which is now 3) | 62 constructions | Every construction passes `monitor_ordinal` explicitly. No hidden reliance on the default. |
| S15 | `git grep -i -E 'explicit\|opt.in\|--yes\|confirm'` in the pr-submit skill and command | 33 | Surfaced the state-machine.md:157-159 first-push confirm (F2). |
| S16 | `git grep -i -E 'pr-submit\|monitor [0-3]\b'` in KNOWLEDGE.md, docs/reference, docs/developer-guide, docs/generated, POST-REFLECT-TASK.md | 9 | All are already-reviewed release-guide and commands.md lines. |
| S17 | `git ls-files .github` + `git grep -i 'pr-submit\|monitor' -- .github` | 0 | The PR template has no how-to-open text. |
| S18 | `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | identical | AC4 holds. |
| S19 | `git remote -v`; `git config --get-regexp 'remote\..*\.gh-resolved'` | origin only; no gh-resolved | Background for F3. |
| S20 | Tavily search (gh base-repo resolution) + `tavily_extract` of `cli/cli` `context/remote.go` | `remoteNameSortScore`: upstream=3, github=2, origin=1 | Evidence for F3; Tavily worked, no fallback. |
| S21 | `git diff origin/master` (stat + full diff of CLAUDE.md, CHANGELOG, commands.md, reflect/commands.py, diagnosis.py, HOW-WE-WORK) | 17 files | Confirmed which text is new. |

## Findings

### F1 (IMPORTANT): HOW-WE-WORK's absolute "never push without approval" rule now contradicts the level-3 route the same guide gives

- **Where:** `src/superclaude/core/HOW-WE-WORK.md:229` (and the byte-identical `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:229`).
- **Quoted:** "- **Never push without approval.** Commit locally, show your lead what changed, and push only when they say go."
- **Contradicts:**
  - `HOW-WE-WORK.md:205` (C3): "...fixes the ones it confirms, pushes those fixes to your branch, and replies to and resolves each review comment."
  - `:254` (C4): "...pushes the fixes to your branch ... on its own. | Always pass `--monitor 3`."
  - `:323` (C5): routing row review-pr makes `--monitor 3` mandatory.
  - The same tension repeats inside `docs/guides/prd-skill-release-guide.md:538` and `docs/guides/tdd-skill-release-guide.md:560`: "Push only after your lead approves, then run `/sc:pr-submit`. It fixes the review findings it confirms and pushes those fixes to your branch on its own."
- **Why it is a real contradiction:** section 4 is titled "Rules everyone follows" and states the rule with no exception. The review fixes are new code that no lead has seen. Level 3 pushes them with no approval step. A reader, or `/sc:recommend`, which reads this guide, gets two incompatible instructions. Spec section 3 only justified line 202 ("Push. Only after your lead approves.") as governing the first push. It never considered line 229, which is a general rule, not a step.
- **Line 272 (`/sc:git` "Still never push without approval")** repeats the rule for `/sc:git` only. It is not itself contradictory, but it reinforces F1.
- **Suggested replacement for `:229`** (then re-copy byte-for-byte to the plugin copy; the level table is untouched, so no `core/CLAUDE.md` re-copy is needed):
  > - **Never push without approval.** Commit locally, show your lead what changed, and push only when they say go. One exception: once your lead has approved the push in workflow 3.11, `/sc:pr-submit --monitor 3` pushes the review fixes it verifies without asking again. If your lead wants to see those fixes first, ask before running it.

### F2 (IMPORTANT): "without asking" / "on its own" contradicts the skill's own first-push confirmation rule

- **Where (the rule that still stands):** `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:156-159`.
  > "A one-time per-run confirmation applies: the FIRST push of a run requires `--yes` OR an interactive confirm unless the run is non-interactive, in which case the `push_decision` record + the `--monitor 3` arming (typed or the default) stands as the recorded authorization."
- **New text that contradicts it:**
  - `CHANGELOG.md:11`: "A bare `/sc:pr-submit` now fixes the review findings it verifies, pushes the fixes to your branch, and replies to and resolves the review comments **without asking**."
  - `HOW-WE-WORK.md:254`: "...replies to and resolves the review comments **on its own**."
  - `CLAUDE.md:46`: "...fixes the findings it verifies, pushes the fixes, and replies to and resolves each review comment."
- **Why it is a real contradiction:** this skill is prose executed by the agent in the main, interactive session (SKILL.md:37-39 requires top-level activation). An agent following state-machine.md section 5.3 must stop and ask before the first push unless `--yes` is passed. But:
  - none of the new mandatory command shapes include `--yes` (`CLAUDE.md:49`, `HOW-WE-WORK.md:204`, the release guides at 535/557);
  - `--yes` is not documented in `pr-submit.md:8` argument-hint or the `:45-56` options table, or in the SKILL.md:133-141 input table, even though `fsm.py:97` parses it.

  So the docs promise "without asking" while the controlling ref requires asking. Spec section 4.2 logged the unread `--yes` as pre-existing. The "without asking" claim, however, is new in this change and is what creates the conflict. The C16 edit ("typed or the default") even touched this exact sentence and left the confirm clause standing.
- **Suggested fix (docs only, no behaviour change):**
  - `CHANGELOG.md:11`: change "without asking" to "without asking per finding (the first push of an interactive run still asks once unless you pass `--yes`)".
  - `HOW-WE-WORK.md:254` (+ plugin copy): append "It asks once before its first push unless you add `--yes`."
  - Add a `--yes` row to `pr-submit.md` Options ("Skip the one-time first-push confirmation") and to `argument-hint`.

  If the intent really is no confirmation at all, then instead delete the confirm clause from state-machine.md section 5.3. Pick one; do not leave both.

### F3 (IMPORTANT): the new CLAUDE.md text says the PR targets "origin's owner/repo", but Wave 0 resolves it through gh's default repo, which ranks `upstream` first

- **Where:** `CLAUDE.md:46` (new).
  > "It opens the PR on the fork (`gh pr create --repo` on origin's `owner/repo`)..."
- **What the skill actually does:** `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:189` (Wave 0):
  > "resolve the target repo once (`REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"`, fallback parse `git remote get-url origin`) ... open the PR with `gh pr create --repo "$REPO" ...`; confirm `git remote -v` shows origin = `$REPO` ..."

  `gh repo view` with no argument returns gh's default ("base") repo, not origin:
  - gh's remote ordering scores `upstream`=3, `github`=2, `origin`=1 (`cli/cli` `context/remote.go`, `remoteNameSortScore`, fetched via Tavily).
  - `gh repo clone` of a fork sets the parent as the default repo (gh manual `gh repo set-default`; adamj.eu gh guide).
- **Why it contradicts CLAUDE.md itself:**
  - `CLAUDE.md:37` states the repo has `upstream` = `SuperClaude-Org/SuperClaude_Framework`.
  - `CLAUDE.md:62` (Rationale) states "The mechanical gates (gh's defaults ...) do NOT enforce the right outcome".

  In a clone that has the `upstream` remote CLAUDE.md describes and no `gh repo set-default`, `$REPO` becomes the upstream parent. The PR is opened there, and only afterwards does the origin check HALT ("instruct the operator to close the misrouted PR", SKILL.md:143-146). That is the PR #558 incident the rule exists to prevent. The "mandatory" path is therefore not guaranteed to "open the PR on the fork", which also conflicts with the NEVER list (`CLAUDE.md:42`).
- **Mitigating fact:** this worktree's config has only `origin` (S19), so it resolves correctly here. That is circumstantial and does not make the CLAUDE.md sentence accurate.
- **Same pre-existing claim elsewhere:** `src/superclaude/commands/pr-submit.md:29`, `:62` and `:83` ("computed from origin, never bare"), and SKILL.md:18, :143 and :216. These are pre-existing; CLAUDE.md now amplifies them into the mandatory rule.
- **Suggested replacement for `CLAUDE.md:46`:**
  > **The mandatory way to open a PR:** always use `/sc:pr-submit --monitor 3`. It opens the PR with `gh pr create --repo <repo>`, where `<repo>` is the repository `gh repo view` reports, then checks that it matches `origin`. Run `gh repo set-default IronbellyOrg/IronClaude` once in each clone so that this is the fork. It then waits for the Augment review, fixes the findings it verifies, pushes the fixes, and replies to and resolves each review comment.

  Also add pre-PR check 0: "`gh repo set-default --view` prints `IronbellyOrg/IronClaude`."

  Separate follow-up, a code/skill change outside this spec: make Wave 0 resolve `REPO` from `git remote get-url origin` first, and check it before `gh pr create`, not after.

### F4 (MINOR): contract-status's next command is still labelled "safe", but it is now the full-autonomy level

- **Where:**
  - `src/superclaude/commands/reflect.md:82`, `plugins/superclaude/commands/reflect.md:73`: "...prints readiness/blockers/checked paths/hashes/counts plus the next safe command..."
  - `src/superclaude/skills/sc-reflect-protocol/SKILL.md:67`: "It reports only readiness state, blockers, checked paths, hashes, counts, and the next safe command".
- **Why:** for state READY, that command is now `/sc:pr-submit --monitor 3 --pr <N>` (`src/superclaude/cli/reflect/commands.py:200` and `src/superclaude/pr_submit/contract_setup/diagnosis.py:380`, C17/C18). It pushes, replies and resolves. The old `--monitor 1` really was propose-only, so "safe" was accurate before. Spec section 3 marked these lines "deliberately unchanged" because they "mention `/sc:pr-submit` without a level", which missed the "safe" label. (`diagnosis.py:255` "Next safe step:" only appears in the not-ready halt renderer, so it never prints the READY command and is fine.)
- **Suggested replacement:** in all three files, change "the next safe command" to "the next command to run".

### F5 (MINOR): a contributor-facing PR instruction still opens PRs a different way

- **Where:** `docs/developer-guide/contributing-code.md:183-188`.
  > "3. **Submit Pull Request:** ```git push origin feature/your-feature-name / # Create PR on GitHub```"
- **Why:** spec goal 2 says "Every PR instruction in the repo says to open PRs with `/sc:pr-submit --monitor 3`." This is a step-by-step PR instruction for this fork (line 168 clones `IronbellyOrg/IronClaude`). It sends contributors to push with no review or approval and to open the PR in GitHub's web UI. For a fork, that UI defaults the base to the upstream parent, which is the trap CLAUDE.md:44 warns about. It is not labelled as a fallback.
- **Suggested replacement:**
  > 3. **Submit Pull Request:** follow workflow 3.11 in [`HOW-WE-WORK.md`](../../src/superclaude/core/HOW-WE-WORK.md): push only after approval, then run `/sc:pr-submit --monitor 3 --head feature/your-feature-name --title "..." --body "..."`. Fallback when `/sc:pr-submit` cannot run: `gh pr create --repo IronbellyOrg/IronClaude --base master --head feature/your-feature-name --title "..." --body "..."`.

## Hits judged fine

| File:line | Text (short) | Why it is fine |
|---|---|---|
| `src/superclaude/commands/pr-submit.md:36-39` | per-level usage examples, incl. `--monitor 1 ... # arm + poll + propose (no edits)` and `--monitor 2 ... HALT before push` | Each level is typed explicitly; this documents levels, not a default (spec section 3). |
| `src/superclaude/commands/pr-submit.md:16`, `:18` | "Explicit only — three activation paths" / "(and optionally arm the monitor)" | "Explicit" means the command must be invoked, not that L3 must be typed. "Optionally" stays true because `--monitor 0` opts out. |
| `src/superclaude/commands/pr-submit.md:19` (C13) | "...the hook NEVER arms a monitor itself" | The level-3 clause is gone. The hook itself is missing (see Observations), which is out of this lens. |
| `src/superclaude/commands/pr-submit.md:26`, `:47`; `SKILL.md:135`; `fsm.py:30,53,76,758` | default 3 | Consistent. |
| `pr-submit.md:48`, `SKILL.md:137`, `refs/loop-guard.md:18`, `reflect/commands.py:299`, `docs/guides/reflect-cli-tools-guide.md:65` | "default 2" | About `--max-rounds` / reflect cycles, not `--monitor`. |
| `pr-submit.md:85`, `SKILL.md:194`, `:196`, `:228`, `refs/state-machine.md:32`, `:44`, `:66-67`, `:83-94` | "apply edits at L1 or push/reply at L2", "L2 ceiling ... NO push" | Per-level capability descriptions with the level named. |
| `SKILL.md:153`, `:189`, `:190`; `refs/state-machine.md:23`; `pr-submit.md:66` | `--monitor 0` open-only / skips preflight | `--monitor 0` semantics are unchanged (spec section 3). |
| `docs/user-guide/commands.md:363` | "at `--monitor 1` or higher, arm..." + "With no `--monitor` it runs level 3." | Per-level description; the default is now stated. |
| `docs/user-guide/commands.md:119` | "`/sc:pr-submit --monitor 0` only opens the PR" | Describes the opt-out. |
| `docs/user-guide/commands.md:117` | changes files: "Yes" | Accurate for L3. |
| `docs/user-guide/commands.md:368` | syntax `[--monitor {0,1,2,3}]` | Syntax line (spec section 3). |
| `HOW-WE-WORK.md:202` | "5. **Push.** Only after your lead approves." | A sequence step for the first push of the branch, before `gh pr create --head` needs it; C3 states what L3 does next. The absolute rule at :229 is the conflict (F1). |
| `HOW-WE-WORK.md:198` | "Commit locally ... Do not push yet." | Step 1 of the sequence; consistent. |
| `HOW-WE-WORK.md:250-254` (section 5 "surprising defaults") | "Always pass `--monitor 3`" equals the default | Redundant but explicit; it guards against a future default change and matches the routing row. Not a contradiction. |
| `HOW-WE-WORK.md:323` review-pr row step 5 "push only after approval" | step 5 | Same reasoning as :202. |
| `tests/core/test_how_we_work_routing_table.py:333-340` `_SAFE_FLAGS` incl. `"/sc:pr-submit": "--monitor 3"` | dict named "safe flags" | The test mechanically pins "mandatory flag on the step". The name is historical; behaviour is correct. CLAUDE.md:330, CHANGELOG:19, help.md:91 and docs/user-guide/how-we-work.md:3 use "safe flags" as the guide-wide term for mandated flags. Borderline wording, but it does not instruct anything wrong. Rename optionally. |
| `src/superclaude/skills/sc-recommend/SKILL.md:53`, `:218`, `:237` (+ plugin copy) | emit every `mandatory_flags` entry | It reads the table, so it now emits `--monitor 3`. No hardcoded `--monitor 1` anywhere in `src/superclaude/cli/recommend/` (S6/S8: 0 hits). |
| `CLAUDE.md:41` NEVER list "Run a bare `gh pr create` without `--repo`" | — | Still valid for the fallback; not contradicted by the new mandatory path. |
| `CLAUDE.md:53-56` fallback `gh pr create --repo IronbellyOrg/IronClaude ...` | — | Clearly labelled "Fallback only". |
| `CLAUDE.md:58-62` pre-PR checks 1-3, Exceptions, Rationale | — | Redundant with Wave 0's own checks but consistent; the targeting accuracy issue is F3. |
| `.github/workflows/pull-sync-framework.yml:115` | `gh pr create --repo "$GITHUB_REPOSITORY" ...` | CI automation, not a human/agent instruction; pinned `--repo`. |
| `src/superclaude/commands/auggie-review.md:18`, `:126-127` | after `gh pr create` the hook offers review | Describes the hook trigger, not a recommended way to open PRs. |
| `src/superclaude/skills/sc-post-release-protocol/SKILL.md:340` | "never ... open a PR ... without confirmation" | Scoped to that skill's own autonomous actions. |
| `docs/developer-guide/git-standards-protocols.md:285-360`, `:399`, `:634` | "Create PR to feature/* / release/* / main" | Branch-target policy (which base), not the tool; no mechanism stated. |
| `docs/developer-guide/README.md:189-192` | "Submit pull request with clear description" | Generic, no mechanism (unlike F5). Upstream-inherited. |
| `src/superclaude/templates/documents/readme_template.md:420` | "Open a Pull Request against `[base branch]`" | A template for other projects' READMEs, inside an HTML comment. |
| `src/superclaude/commands/swarm-wizard.md:96`, `src/superclaude/commands/reflect.md:82` (apart from the "safe" label), `plugins/superclaude/commands/reflect.md:73`, `src/superclaude/skills/sc-reflect-protocol/SKILL.md:67` | mention `/sc:pr-submit` with no level | Spec section 3; only the "safe" label is flagged (F4). |
| `src/superclaude/pr_submit/contract_setup/diagnosis.py:255` | "Next safe step:" | Only rendered by the not-ready halt, whose next command is never the READY `--monitor 3` command. |
| `tests/pr_submit/test_monitor_arm.py:3`, `:27`, `:36`; `test_skill_parse.py:65`; `test_contract_setup_pr_submit_integration.py:12`, `:120-124` | explicit `--monitor 1` / `--monitor 0` tests | They test explicit ordinals (AC2). |
| `tests/pr_submit/test_autonomy_gates.py:5`, `:78-100`, `test_finding_verify.py:58`, `:86`, `test_edge_cases.py:116` | `monitor_ordinal=2` → HALT_BEFORE_PUSH | Explicit L2 tests; S14 confirmed no test relies on the `RunConfig` default. |
| `src/superclaude/pr_submit/fsm.py:937-939`, `:996`, `:1011`, `:1037` | per-level docstrings/comments | Name the level explicitly. |
| `CHANGELOG.md:12` | "...instead of `--monitor 1`" | Historical record of the change (AC2). |
| `.dev/**`, `.claude/**` | — | Excluded by scope (records / gitignored dev copies). |

### Observations outside this lens (pre-existing, not counted toward the verdict)

1. **Missing hook.** `src/superclaude/hooks/scripts/offer-pr-review.sh` does not exist on this branch or on `origin/master`; its last appearance was before `a97dfb29` (S7). It is still referenced by:
   - `pr-submit.md:19` (a line C13 edited);
   - `SKILL.md:189`;
   - `auggie-review.md:18` and `:126-127`;
   - the comment at `cli/install_hooks.py:77`;
   - `tests/pr_submit/test_hook_update.py:16` and `test_static_grep.py:28`.

   It is an orphaned activation path, but unrelated to the monitor default.
2. **`--pr` flag the parser does not accept.** The READY next command `/sc:pr-submit --monitor 3 --pr <N>` (`reflect/commands.py:200`, `diagnosis.py:380`) uses `--pr`, which `fsm.py:76-97` does not parse; pr-submit takes "an existing PR number". This was pre-existing with `--monitor 1`.
3. **`--yes` undocumented.** `--yes` is parsed (`fsm.py:97`) but missing from `pr-submit.md:8` and the options tables. This feeds F2.

## Self-Audit

Findings exist (5), so the zero-findings justification does not apply. What was actively checked:

1. **Claims verified against source:** 30+. Examples:
   - `DEFAULT_MONITOR = 3` (fsm.py:30); `RunConfig.monitor_ordinal = DEFAULT_MONITOR` (fsm.py:758).
   - All 62 `RunConfig(` constructions pass `monitor_ordinal`.
   - The two `--monitor 3` next-command returns.
   - The `_SAFE_FLAGS` entry.
   - The state-machine.md section 5.3 confirm clause.
   - The SKILL.md Wave 0 repo resolution order.
   - HOW-WE-WORK :202/:205/:229/:254/:272/:323.
   - CLAUDE.md :37/:41/:46/:55/:62.
   - CHANGELOG :11/:12.
   - Release guides :535/:538/:557/:560.
   - contributing-code.md :168/:183-188.
   - That the hook file is absent; the remotes / gh-resolved config.
   - gh's `remoteNameSortScore`.
2. **Files read:**
   - The spec in full.
   - HOW-WE-WORK.md lines 180-279 (Read) plus its full diff.
   - `commands/pr-submit.md` in full.
   - `sc-pr-submit-protocol/SKILL.md` lines 1-246.
   - `refs/state-machine.md` lines 20-174.
   - `test_how_we_work_routing_table.py` lines 300-357.
   - `diagnosis.py` lines 235-264 and 360-380; `reflect/commands.py` lines 150-215.
   - `install_hooks.py` lines 65-90; `test_hook_update.py` lines 1-40.
   - `commands.md` lines 361-385; `contributing-code.md` lines 150-200; `developer-guide/README.md` lines 180-198.
   - `prd-skill-release-guide.md` lines 525-540; `readme_template.md` lines 410-425.
   - The full diffs of CLAUDE.md, CHANGELOG, commands.md, the reflect next command and diagnosis.py.
3. **Angles covered:** 21 searches (Search log). They cover:
   - default-is-2 phrasing;
   - explicit-L3 / never-push / propose-only claims;
   - alternative PR paths (gh pr create, web UI, generic "open a PR");
   - the recommend machinery and routing tests;
   - "safe" labelling;
   - tests silently relying on the code default;
   - in-file consistency in CLAUDE.md and HOW-WE-WORK;
   - first-push confirmation wording;
   - the accuracy of CLAUDE.md's fork-targeting claim against Wave 0 and gh's real resolution order.
4. **Web research:** Tavily first (`tavily_search`, then `tavily_extract` on `cli/cli` `context/remote.go`). Both worked, so there was no WebSearch/WebFetch fallback.
5. **Not done (constraints):** I did not run pytest, ruff or `make`. Running them writes caches and artifacts, and this review is report-only with no writes outside this file. I did not confirm by execution which repo `gh repo view` reports in a clone that has an `upstream` remote. F3 rests on gh source code plus documented `gh repo clone` behaviour, not on a live run.

**Tool engagement:** Read 9 | Grep (via `git grep` in Bash) ~20 | Glob 0 | Bash 27 | Tavily 2.

**Confidence:** Verified: 5 findings + 30 fine-judgements with tool evidence | Unverifiable: 1 (a live gh run with an upstream remote, which would mutate config) | Unchecked: 0.
