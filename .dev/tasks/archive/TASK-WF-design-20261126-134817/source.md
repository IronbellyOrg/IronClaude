# Design: Worktree and Branch Protocol (component specification)

Grounding: index_state: fresh (checked_at 2026-11-26T13:43:55Z, worktree_root `/home/coder/workspaces/worktrees/IronClaude/issue-289`; tools used: `codegraph_status`, `codegraph_node` with `symbolsOnly` on the three test files). The guide, the onboarding page and the requirements are Markdown or HTML, which the index does not hold, so they were read directly.

Input: `.dev/brainstorms/20261126-worktree-branch-protocol/merged-requirements.md` (adversarial status `partial`, see section 7), `seed-brief.md`, and the decided block of `.dev/issues/289/issue-summary.md` (Clay, 26 Nov 2026: pattern `<login>/issue-<N>-<short-words>`, under 25 characters, no spaces; keep lesson extraction before cleanup).
Type and format: component, spec. Issue: https://github.com/IronbellyOrg/IronClaude/issues/289

## 1. What is built

One documentation component with five deliverables and one new test file. No production code.

| ID | Deliverable | File |
|---|---|---|
| K1 | New guide section "Worktrees and branches" (at most 400 words, ASCII) | `src/superclaude/core/HOW-WE-WORK.md` |
| K2 | The sentence about removal timing points at K1 | same file, the `/sc:worktrees` row (line 299) |
| K3 | Byte-identical mirror | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` |
| K4 | New policy tests | `tests/core/test_how_we_work_worktree_policy.py` |
| K5 | Replaced worktree card and updated build footer | `docs/onboarding/ironclaude-onboarding.html` (lines 520-524 and 579) |

Not built (out of scope, from the requirements): the claim launcher and its `issue-<N>` naming, the cleanup script and its rules, the issue watcher, the `CLAUDE.md` examples at lines 318-341, the issue 290 card (525-528), the slide intro (516-518), and any extraction tool for lessons.

## 2. Design decisions

| ID | Decision | Why (source) |
|---|---|---|
| DD-1 | K1 is an unnumbered `## Worktrees and branches` heading between the end of the routing table (line 350) and `## Orca coordination` (line 352). It holds no marker. | Section 4 is bullets only (`HOW-WE-WORK.md:251-263`); `## Orca coordination` and `## Routing table` are already unnumbered, and `_HEADING_RE` in `tests/core/test_how_we_work_routing_table.py:99` reads only numbered headings. |
| DD-2 | K1 has bullets only, no table, so the word count is plain and the text is easy to test. | FR-016; INV-022. |
| DD-3 | The checker for names lives only in the new test file. No production naming code. | Requirements section 1 (non-goals). |
| DD-4 | K2 replaces the "(item 4 of issue 289)" clause with a pointer to K1. Only the guide and its mirror hold that sentence (grep). | FR-017. |
| DD-5 | K5 changes lines 520-524 only. The intro (516-518), the 290 card (525-528) and the "Being worked out" heading stay. The card keeps the glossary meaning. | X-008, X-009; the intro stays a known limitation (R5). |
| DD-6 | The footer at line 579 becomes the 8-character hash of the branch HEAD at the time of the edit. The commit that will hold the guide change does not exist yet, so a person corrects it when re-publishing the artifact after the merge. | The deck's own rule FR-ONB.7 (`ironclaude-onboarding.html:3-5`); `_FOOTER_RE` accepts 7 to 40 hex characters. Recommended default. |
| DD-7 | Resolution of open defect T1 (the claim gate over-stops). The gate and the "no PR" stop apply to a fix to delivered work. They do not apply to (a) a re-run of a claim whose earlier run made the worktree and launched no agent (`.dev/issues/<N>/worktree.json` names the worktree and has no `launch` entry), or (b) a sequential handoff of unfinished work: the "no PR" stop sits inside the fix bullet and governs only a fix to delivered work, so a handoff is not caught by it (the words for this were cut to meet the 400-word cap). | Requirements, "Open after the review limit", T1. This is a design-level fix: the third review that found T1 was the last one the protocol allows, so it was not re-reviewed. The `/sc:workflow` check and the final `/sc:implement` review are the next independent reads. |
| DD-8 | The guide says the issue watcher claims by itself when a Project Status moves, and that the same checks come first. The owner decision (should the watcher refuse such issues) stays in the pull request body. | R13. |

## 3. K1: the guide section

Placement: after line 351 (the blank line after `<!-- /routing-table -->`), before `## Orca coordination`. The text below is normative for content; the implementer may tighten wording but must keep every rule and stay at or under 400 words (the test counts with `str.split()`; this draft is 389 words by that count and ASCII).

<!-- guide-section:begin -->
```text
## Worktrees and branches

A worktree is a second checkout in its own folder, on its own branch. Orca creates every worktree, with an agent, at its default location (never raw `git worktree add`). The creator owns the agent; no session creates a worktree for itself.

- **New work gets a new worktree and branch.** One writer per worktree; a second writer gets its own. Supervised workers follow `~/.claude/WORKER-CONTRACT.md`.
- **A fix to delivered work reuses the original worktree while it still exists, after these checks:** same repository, issue and branch; the issue is open (a closed one needs a bug issue `#<M>` named in the fix PR); no other live agent (`orca terminal list`); no uncommitted changes; the PR that counts (`gh pr list --repo <owner>/<repo> --head <branch> --state all`: newest merged, else newest) is merged and none is open. Then `git fetch origin`, `git merge --ff-only origin/<base>`, check that HEAD moved, and run `orca agent launch`. Any other state (PR closed unmerged, no PR, several worktrees, a worktree missing from `orca worktree list`, anything unknown): stop and ask. A removed worktree means a new one.
- **Check before `/sc:issue --claim` or a Project Status change.** A claim reuses the worktree it finds and starts its agent at once; the watcher claims by itself. A re-run of the claim's own earlier run (no `launch` entry in its `worktree.json`) is exempt.
- **Names:** `<login>/issue-<N>[-<words>]`, at most 24 characters, no spaces; `<login>` is `gh api user --jq .login`. Create with `--name issue-<N>-<words>`; Orca adds the login (use `--branch` if it does not). Words are lowercase letters and digits with no run of 2 to 4 digits (cleanup reads it as an issue). Example: `clayphi/issue-289-wtrule` (24). Drop the words when they do not fit; if even `<login>/issue-<N>` is over 24, create nothing and ask the owner. After creation the agent checks `git branch --show-current` and may run `git branch -m` before any push; never switch branches in a worktree.
- **Lessons before removal.** The owner pins the worktree in the Orca app when the PR opens. After the merge the owner posts a Lessons comment on the issue (what happened, evidence by PR or commit, action) or "no reusable lesson", runs `/sc:closeout`, then unpins. A person runs `/sc:worktrees archive`, `retire` and `--apply`, and checks that comment first, because cleanup reads none.
```
<!-- guide-section:end -->

Rules the text must keep (each is one test phrase in section 5): new worktree and branch; one writer per worktree; original worktree while it still exists; the checks; ff-only; stop and ask; the claim and the watcher; the name pattern, 24 characters, no spaces; the digit rule; stop when even the bare name is over 24; lessons before removal; the pin; the check before `--apply`.

## 4. K2, K3, K5: exact changes

K2. In the `/sc:worktrees` row of the `<!-- other-commands:v1 -->` table, replace
`When to remove a worktree after its pull request merges (item 4 of issue 289): after the pull request merges and every rule of the cleanup holds.`
with
`When to remove a worktree: after its pull request merges, the lessons are written (see Worktrees and branches below) and every rule of the cleanup holds.`
Keep the rest of the row. The row must stay ASCII and keep its 2 table cells. The phrase "every verb is a dry run" must not appear (`tests/commands/test_worktrees_command.py:124-137` bans three phrasings).

K3. After K1 and K2, copy the guide over the mirror (`cp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`); `cmp` of the two files must print nothing (`tests/skills/test_review_prompt_overrides.py:134-135`). The level table is unchanged, so `src/superclaude/core/CLAUDE.md` needs no recopy; `tests/core/test_claude_md_routing_block.py` confirms it.

K5. Replace lines 520-524 of `docs/onboarding/ironclaude-onboarding.html` (the `<div class="card">` of the worktree card, from its opening tag to its closing `</div>`) with:

```html
    <div class="card">
      <h3>Worktree and branch protocol</h3>
      <div class="term"><b>Worktree:</b> a second checkout of the same repository in its own folder, on its own branch, so parallel sessions do not touch each other's files.</div>
      <p>New work gets a new worktree and branch, made by Orca with an agent. A fix to delivered work reuses the original worktree while it exists, after the checks in the guide. Name: <code>&lt;login&gt;/issue-&lt;N&gt;-&lt;words&gt;</code>, at most 24 characters, no spaces, for example <code>clayphi/issue-289-wtrule</code>. Before removal the owner writes the lessons on the issue, and a person pins the worktree until then. Details: HOW-WE-WORK, "Worktrees and branches".</p>
    </div>
```

Every command and flag inside `<code>` must be in the guide (`test_every_deck_command_and_flag_is_in_the_guide`); the card above has none. Then replace `f3c1ef06` on line 579 with `git rev-parse --short=8 HEAD` taken at the time of the edit (DD-6). Lines 516-518 and 525-528 stay byte-identical. Re-publishing the artifact to the same link is a person's step after the merge.

## 5. K4: the test file

File: `tests/core/test_how_we_work_worktree_policy.py`. Imports: `re`, `pytest`, `pathlib.Path`. Constants `_REPO = Path(__file__).resolve().parents[2]`, `_GUIDE`, `_TWIN` (the mirror), `_DECK`. No fixtures.

Helpers:

| Name | Contract |
|---|---|
| `_section()` | Text of the guide from the line `## Worktrees and branches` up to the next line that starts with `## `. Fails with a clear message when the heading is missing or appears more than once. |
| `_NUMBER_RUN` | `re.compile(r"(?<!\d)\d{2,4}(?!\d)")`, the same bound as `scripts/worktree_cleanup.py:1462`. |
| `branch_errors(branch)` | Returns a list of error strings (empty means valid). Rules: whole string matches `^[A-Za-z0-9]+(-[A-Za-z0-9]+)*/issue-[1-9][0-9]*(-[a-z0-9]+)*$`; `len(branch) <= 24`; the words part has no match for `_NUMBER_RUN`; when the bare form `<login>/issue-<N>` is itself over 24 the error text contains the word `stop`. |
| `max_words_length(login, digits)` | `16 - len(login) - digits` (the budget W). |

Tests (each failing if its rule is removed from the guide or broken in the checker):

| Test | Checks | Requirement |
|---|---|---|
| `test_section_exists_once_before_orca_coordination` | one heading, positioned before `## Orca coordination`, no `<!--` marker inside | FR-001, DD-1 |
| `test_section_is_at_most_400_words` | `len(_section().split()) <= 400` | FR-016, AC-4 |
| `test_section_is_pure_ascii_and_has_no_banned_phrase` | `isascii()`; none of "Every verb is a dry run", "every verb is a dry run", "Verbs (a dry run unless --apply is given)" | FR-015 |
| `test_section_states_each_rule` (parametrized) | each key phrase from the list in section 3 occurs in the section | FR-002 to FR-013, FR-019, AC-4 |
| `test_checker_accepts` (parametrized) | `clayphi/issue-289-wtrule` (24), `clayphi/issue-834-clean` (23), `ironbelly/issue-517-orca` (24), `clayphi/issue-1234-docs` (23), `clayphi/issue-289` (17), `longloginname/issue-289` (23), `Ab-c/issue-5` (12), `a/issue-1-v12345` (16; a 5-digit run is not a 2-4 digit run, so it is allowed) | FR-005, AC-5 |
| `test_checker_rejects` (parametrized) | `clayphi/issue-289-wtrules` (25), a name with a space, `clayphi/issue-0289`, `clayphi/issue-`, `clayphi/issue-289-`, `clayphi/issue-289-py312`, `clayphi/issue-289-v2024`, `a--b/issue-1`, `-a/issue-1`, `a/issue-1-x/y` | AC-6, INV-014 |
| `test_bare_form_over_the_limit_is_a_stop` | `averylonglogin1/issue-289` (25) gives an error containing `stop` | FR-008 |
| `test_budget_formula` (parametrized) | `max_words_length("clayphi", 3) == 6`; `("clayphi", 4) == 5`; `("longloginname", 3) == 0`; overflow of the bare form exactly when `len(login) + digits >= 18` | section 4.1 of the requirements |
| `test_every_backticked_branch_example_in_the_section_passes` | find spans like `` `x/issue-...` `` without `<` or `>`; at least one exists; each has no `branch_errors` | AC-5 |
| `test_deletion_is_detected` | remove one key phrase from a copy of the section and assert `test_section_states_each_rule`'s check function reports it (planted failure, like `tests/docs/test_onboarding_deck.py:94`) | AC-4 |
| `test_mirror_is_byte_identical` | `_GUIDE.read_bytes() == _TWIN.read_bytes()` | FR-014, AC-3 |
| `test_pointer_names_the_section` | the `/sc:worktrees` row contains "Worktrees and branches" and not "item 4 of issue 289" | FR-017 |
| `test_deck_card_is_replaced_and_neighbours_untouched` | the deck holds "Worktree and branch protocol" and not "is being worked out in"; still holds the issue 290 card text "Contributing rules" and the footer pattern | AC-8, AC-9 |

Key phrases for `test_section_states_each_rule` (exact substrings of K1): `new worktree and branch`, `One writer per worktree`, `original worktree while it still exists`, `--ff-only`, `stop and ask`, `/sc:issue --claim`, `at most 24 characters`, `no spaces`, `no run of 2 to 4 digits`, `create nothing and ask the owner`, `Lessons comment`, `pins the worktree`, `checks that comment first`.

## 6. Order of work and checks

1. Write K4 first (the tests fail on the missing section). 2. Add K1 and K2 to the guide until K4's guide tests pass. 3. Copy K3 and run `cmp`. 4. Edit K5 and the footer. 5. Run: `uv run pytest tests/core/test_how_we_work_worktree_policy.py tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_worktree_rule.py tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/docs/test_onboarding_deck.py tests/commands/test_worktrees_command.py tests/commands/test_help_command.py tests/commands/test_routing_plugin_parity.py tests/skills/test_review_prompt_overrides.py tests/skills/test_sc_recommend_routing_contract.py tests/cli/test_how_we_work_install.py tests/recommend -v`. 6. `make lint` on the new test file. Stage only the changed files and `.dev/tasks`; never `.claude/` or `.dev/issues/`.

## 7. Status of the inputs and open items

- The requirements are `partial`: the invariant probe blocked convergence with four HIGH findings; all four were confirmed covered by the third independent review. One blocking defect (T1) was found by that review; DD-7 resolves it in this design.
- Owner questions that stay open and go into the pull request body, not into the guide: R2 (dropping the words when they do not fit and for claim-made names), R12 (where the lessons of issue-less long-lived worktrees go), R13 (whether the watcher or the claim should refuse an issue that already has a worktree), R5 (the slide intro at lines 516-518 still calls the topic open), R10 (the `CLAUDE.md` examples at lines 318-341 use other names), and the footer rule DD-6.
- Dissent on record: one advocate would stop on a name mismatch instead of renaming (R1). K1 keeps the rename before the first push as the recommended default; `git branch -m` leaving Orca's record intact was not exercised.
- Acceptance criteria map: AC-1 to AC-4 to K1, K2, K4; AC-3 to K3; AC-5 to AC-7 to K4 and the existing suites; AC-8 to AC-10 to K5; AC-11 to AC-13 to K1's reuse and lessons bullets and K4's key-phrase test; AC-14 is met by the third review file.
