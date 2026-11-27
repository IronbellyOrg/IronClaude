# Design: rules for proposing and changing skills, commands and agents (issue 290)

Type: architecture. Format: spec. Input: `.dev/brainstorms/20261126-031900-primitive-contribution-rules/merged-requirements.md` (FR-001 to FR-013).
Grounding: index_state: fresh (checked_at 2026-11-26T04:08:10Z, worktree_root /home/coder/workspaces/worktrees/IronClaude/issue-290); codegraph tool used: `codegraph_status` only. Every target here is Markdown, YAML or HTML, which the graph does not index, so structure was confirmed by Read and Grep (the floor). Facts below were read from the files on 2026-11-26 at `origin/integration` 3cf7e2259.

Note on output: `/sc:design` without `--output` writes no file. This design is saved here because the next step (`/sc:workflow`) needs a path to read.

## 1. Purpose and constraints

Publish the interim rule for contributing skills, commands and agents ("primitives") to IronClaude itself: new team members file an issue; the future gate is marked "not available yet". Documentation, form, template and deck edits only. No code, no new test, no ROI metric, threshold, role or issue number invented.

Hard constraints found in the code:

| Constraint | Source | Effect on the design |
|---|---|---|
| The guide must be ASCII except one "Ruling:" line | `tests/core/test_how_we_work_routing_table.py:329-334` | Draft text below is plain ASCII (straight quotes, hyphens) |
| The plugin copy must equal the guide byte for byte | `tests/commands/test_routing_plugin_parity.py`, `tests/skills/test_review_prompt_overrides.py:134-135` | Copy after every guide edit |
| No sentence may match `find ... at least one/N/digit` or the removed phrases | `tests/skills/test_review_prompt_overrides.py:140-185, 217-226` (scans every `.md` under `src` and `plugins`) | Draft text avoids the word "find" near "at least" |
| Deck commands and flags inside `<code>` or SVG text must exist in the guide; `--plugin` is read from `src/superclaude/commands/recommend.md` | `tests/docs/test_onboarding_deck.py:14-23, 69-87` | New card may use `/sc:help`, `/sc:recommend`, `--plugin` inside `<code>` |
| The deck test checks only that the footer pattern exists, not its value | `tests/docs/test_onboarding_deck.py:90-91` | The footer needs its own check (section 4 below) |
| The PR template line "Branch rebased onto `origin/integration`" is read by a test | `tests/core/test_default_branch_agreement.py:20` | Additions only |
| Section numbers are cited by the deck and tests (`## 4.` ends at `## 5.`) | `tests/core/test_how_we_work_routing_table.py:322-326, 897` | No new heading in the guide |
| New form field ids: letters, digits, `-`, `_`; unique | GitHub issue-form schema | `primitive`, `reuse_search`, `affected_callers` fit |
| A YAML plain scalar containing `: ` breaks parsing | YAML | Quote every new description that contains a colon |
| Never stage `.claude/` or `.dev/issues/`; `.dev/tasks/` is always staged | Project `CLAUDE.md`, story step 9 | Stage source files and `.dev/tasks` only |

## 2. Architecture: one source, short pointers

The full rule lives only in guide section 4. Every other surface repeats the one-line rule and points to it, so a later change (lifting the restriction, filling in the ROI threshold) edits one place.

```
                      HOW-WE-WORK.md  section 4   (source of truth)  --> plugin copy (byte-identical)
                              ^
   +-------------+------------+-------------+--------------+----------------+
   |             |            |             |              |                |
 contributing- CONTRIBUTING  feature_request bug_report   PULL_REQUEST_   onboarding deck
 code.md       .md (1 para)  .yml (3 fields)  .yml (1 line) TEMPLATE.md     slide s12 card
 (notice +                                                  (not-available  (+ footer SHA)
 4 reminders)                                               section)
```

Who reads what (this decides where each rule must be written):

| Reader and route | Sees | Therefore |
|---|---|---|
| New member on the GitHub web | Forms, PR template, `CONTRIBUTING.md` | Form fields and the `CONTRIBUTING.md` line carry the rule |
| Agent or CLI filing (`/sc:issue --create`, `gh issue create`) | No web form | Section 4 states what every proposal issue contains, "however filed" |
| Agent opening a PR (`/sc:pr-submit`, passes `--body`) | No PR template | The PR-template section does not gate anything; say so in the PR body |
| Reader following `/sc:recommend` | Only the three marker blocks of the guide, never section 4 | Accepted risk, owner follow-up 1 (a routing row) |
| Reader entering `contributing-code.md` by a deep link | May skip the top | Reminder under four headings |

## 3. Components

Each component lists the file, the exact edit, draft text, and what guards it. Draft text is for the implementer to finalize; keep it ASCII.

### C1. Guide section 4 (FR-001 to FR-004, FR-006)
File: `src/superclaude/core/HOW-WE-WORK.md`. Insert five bullets after the existing last bullet (line 261, "A `/sc:` command whose file names a skill...") and before the line beginning "Where this guide says" (line 263). No new heading.

```
- **Contributing a skill, command or agent to IronClaude itself: file an issue first.** New team members do not open pull requests that add or change a skill, command or agent yet. File an issue with the "Suggest an improvement" form instead, and say what is missing or broken and why. This covers IronClaude's own skills, commands and agents, not the ones in your project.
- **Look for an existing tool before you propose one.** `/sc:help` lists the commands and skills installed here (not agents). `/sc:recommend "<what you want to do, and why>"` suggests an existing tool, agents included. `/sc:recommend --plugin` searches outside plugins and community skills only, and installs nothing. Put what each search returned, or why it could not run, in your issue.
- **Every proposal issue, however filed, says three things:** what is missing or broken; what the searches above returned, or why one could not run; and which skills, commands or agents you know use the one you want to change, or "not known". No complete list of callers exists yet, so "not known" does not mean there are none.
- **Where changes go (maintainers).** Skill, command and agent files are edited in this repository's `src/superclaude/` and tried locally with `make sync-dev`. They reach users through the installer, which can overwrite local edits.
- **A future change will need evidence, and that gate is not available yet.** When contribution opens, a pull request that changes a skill, command or agent will need before-and-after evidence that the change adds value, not bloat; then a reviewer's approval; then a passing CI evaluation that meets an ROI (value compared with cost) threshold. The metric, the threshold and the approving role are not set, and a green test run does not satisfy this gate. The gate is not available yet; it depends on evaluation work such as issue 487 in IronbellyOrg/IronClaude. A change to one skill can also break the skills that call it.
```

Guards: FR-001 to FR-004 checks of the merged spec (words present; "issue 487 in IronbellyOrg/IronClaude" exactly once; "value compared with cost"; no "only after"; the only `src/superclaude` mention in section 4 is the maintainer sentence); the routing-table test (ASCII, headings); `git diff -U0` hunks lie between `## 4.` and `## 5.`. Then `cp` the guide to the plugin copy (FR-005) and confirm `cmp`. `src/superclaude/core/CLAUDE.md` is not touched (FR-006).

### C2. Contribution guide (FR-007)
File: `docs/developer-guide/contributing-code.md`. Additions only.
- Before `## Table of Contents` (line 7):
```
> **New team members: file an issue; do not open a pull request that changes a skill, command or agent yet.** The rule, the searches to run first, and what a future change will need are in [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows). The rest of this page is maintainer reference.
```
- A one-line reminder directly under `## Context File Guidelines` (line 99), `## Development Workflow` (160), `## Contributing to Components` (237) and `### Issue Reporting` (377): `> Maintainer reference. New team members file an issue first; see [HOW-WE-WORK, section 4](../../src/superclaude/core/HOW-WE-WORK.md#4-rules-everyone-follows).`
- Directly under `### Pull Request Template` (line 203), above the embedded example: `> The template GitHub shows on new pull requests is [.github/PULL_REQUEST_TEMPLATE.md](../../.github/PULL_REQUEST_TEMPLATE.md); the example below is an illustration only.`
Guards: `git diff --stat` zero deletions; every baseline `##` and `###` heading present. Implementer checks that any link-check test accepts the relative paths (the 16-file test run covers it).

### C3. Improvement form (FR-008)
File: `.github/ISSUE_TEMPLATE/feature_request.yml`. Keep `name`, `title`, `type`, `labels` and the ids and `required` values of `problem`, `proposal`, `alternatives`.
- Intro markdown gains: `You can also use this form to propose a skill, command or agent, or to report one that is missing or misbehaves.`
- `proposal` description becomes: `'Describe the change you want to see. If you do not know the solution, write "solution unknown" and describe the outcome you need; that is a valid answer for missing or broken behavior.'`
- After `alternatives`, three fields, all `validations: required: false`:

| id | type | label | description (quote it: it contains `: `) |
|---|---|---|---|
| `primitive` | input | Skill, command or agent (if any) | `'Kind and name, for example: command /sc:recommend. Write "new" if it does not exist yet. A proposal about a skill, command or agent must answer this; leave it blank only for other requests.'` |
| `reuse_search` | textarea | What the reuse search returned | `'What /sc:help, /sc:recommend and /sc:recommend --plugin returned, or "search not available because ...". A proposal about a skill, command or agent must answer this; leave it blank only for other requests.'` |
| `affected_callers` | textarea | Skills, commands or agents that use it | `'The ones you know of, or "not known". No complete list exists yet, so "not known" does not mean none. A proposal about a skill, command or agent must answer this; leave it blank only for other requests.'` |

Guards: `yaml.safe_load` (the loader existing tests use); body ids exactly `problem`, `proposal`, `alternatives`, `primitive`, `reuse_search`, `affected_callers`, unique; the new three `required: false`; validation against GitHub's issue-form schema, with the result recorded in the PR body.

### C4. Bug form pointer (FR-009)
File: `.github/ISSUE_TEMPLATE/bug_report.yml`. In the intro markdown element (lines 8-13), add after the "Use this form for bugs..." line and its blank line: `If a skill, command or agent is missing or misbehaves, use the "Suggest an improvement" form instead; it asks the reuse and caller questions.` Ids `os`, `orca_version`, `details` and their `required` values are unchanged. Additions only.

### C5. PR template (FR-010)
File: `.github/PULL_REQUEST_TEMPLATE.md`. Insert after the `Closes #` line (line 15) and before `## Checklist` (line 17):
```
## Skill, command or agent changes (not available yet)

New team members file an issue instead of opening a pull request that changes a skill, command or agent (see HOW-WE-WORK, section 4). The list shows what such a pull request will need once contribution opens; none of it can be met today.

Not applicable: this PR does not change a skill, command or agent.

- Linked proposal issue.
- Before-and-after evidence that the change adds value, not bloat.
- Known callers listed and rechecked, or "not known".
- Reviewer approval, given before the evaluation.
- CI evaluation passed at the ROI threshold: not available yet (metric, threshold and approving role not set).
```
Plain bullets, no `- [ ]`. Every existing line stays (including line 23). The PR body (not the template) states that the section appears only on PRs opened in the GitHub web interface because `/sc:pr-submit` passes `--body`.

### C6. Root CONTRIBUTING.md (FR-012)
File: `CONTRIBUTING.md`. Add one paragraph after the existing paragraph of `### Claiming and filing issues` (line 77): `New team members: to propose or change a skill, command or agent, file an issue first and do not open a pull request that changes one yet. See [HOW-WE-WORK, section 4](src/superclaude/core/HOW-WE-WORK.md).` This adds two lines (a blank line and the paragraph) and deletes none; read FR-012's "one insertion" as "zero deletions and one added non-blank line". The stale `--base master` on line 66 is not touched (owner follow-up 4).

### C7. Onboarding deck (FR-011)
File: `docs/onboarding/ironclaude-onboarding.html`, slide `s12` (lines 515-530) and the footer (line 579).
- Eyebrow (line 516): `<b>12</b> · Contributing and open topics · GitHub issues #289 and #290`.
- Heading (line 517): `Contributing, and one open topic`.
- Intro (line 518): `The contributing rules are settled for now; the worktree topic is still open in its own issue. Until it is settled, ask your lead.`
- Replace the second card (lines 525-528) with:
```
    <div class="card">
      <h3>Contributing rules</h3>
      <p>For now, file an issue; do not open a pull request that changes a skill, command or agent. Before you file, look for an existing tool with <code>/sc:help</code> and <code>/sc:recommend</code>, and note what the outside-plugin search <code>/sc:recommend --plugin</code> returns. Say what is missing or broken, what the searches returned, and which skills you know use it. A future change will need before-and-after evidence, a reviewer's approval and a passing evaluation; that gate is not available yet. The full rule is in the guide, section 4. History: <a href="https://github.com/IronbellyOrg/IronClaude/issues/290">issue #290</a>.</p>
    </div>
```
- The first card (lines 520-524, worktrees) stays byte-identical.
- Footer (line 579): `Built from HOW-WE-WORK.md at commit <8-character SHA of commit 1>` (same width as the current `f3c1ef06`).
Guards: the deck test (tokens: `/sc:help`, `/sc:recommend`, `--plugin` all resolve); the card contains no "being worked out"; the worktree card block is byte-identical; every other slide is read against the guide at commit 1 before the footer moves (the guide changed in 28 commits since `f3c1ef06`, so the footer certifies the whole deck).

## 4. Commit and footer sequence

| Step | Action | Check |
|---|---|---|
| 0 | On `origin/integration` before editing: run the 16 test files that read the guide, the deck or the PR template (list in section 5) and record the result | Baseline recorded in the PR body |
| 1 | Commit 1: C1 (guide) and the plugin copy | `cmp` exits 0; parity and routing tests pass |
| 2 | Commit 2: C2, C3, C4, C5, C6 | Zero-deletion diff; YAML parse and schema check |
| 3 | If `origin/integration` moved, rebase now (project rule), then recompute commit 1's short SHA | `git rev-parse --short=8 <commit 1>` |
| 4 | Read every deck slide against the guide at commit 1 | Notes in the PR body |
| 5 | Commit 3: C7 with the footer set to the SHA from step 3 | `git diff --quiet <sha> HEAD -- src/superclaude/core/HOW-WE-WORK.md` and `git diff --quiet <sha> -- src/superclaude/core/HOW-WE-WORK.md` both exit 0 |
| 6 | After any later rebase or review-fix commit that touches the guide, repeat steps 3 and 5 | Same two commands |
| 7 | PR body: decisions table (D6 "deferred, no issue yet"), baseline and final test results, schema check, a request for a merge commit (squash and rebase merges rewrite SHAs and both are enabled), the PR-template note, same-link re-publication of the deck as an operator step, the owner follow-ups | Listed in section 6 |

## 5. Verification

- Baseline and final runs: every test file that reads the guide, the deck or the PR template: `tests/unit/test_cli_install.py`, `tests/skills/test_sc_recommend_routing_contract.py`, `tests/skills/test_spec_panel_review_loop.py`, `tests/skills/test_issue_protocol.py`, `tests/skills/test_review_brief_placement.py`, `tests/skills/test_review_prompt_overrides.py`, `tests/recommend/test_routing_refresh.py`, `tests/recommend/test_cache.py`, `tests/docs/test_onboarding_deck.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/commands/test_worktrees_command.py`, `tests/core/test_claude_md_routing_block.py`, `tests/core/test_default_branch_agreement.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/commands/test_help_command.py`, `tests/cli/test_how_we_work_install.py`; run with `uv run pytest <files> -q`.
- `make verify-sync` proves nothing about the guide (its target does not compare core files); do not cite it for the guide.
- Static checks: `cmp` of the guide and plugin copy; `git diff -U0` hunks for the guide inside section 4; `## ` heading list equal to the baseline; `git diff --quiet origin/integration -- src/superclaude/core/CLAUDE.md`; `git diff --stat` zero deletions for the contribution guide, bug form, PR template and `CONTRIBUTING.md`; the form checks of C3; the footer checks of section 4; `git diff --name-only origin/integration...HEAD` lists no `.claude/` path.
- Manual scenarios (recorded in the PR body): a missing-skill request, a broken-skill report answering "solution unknown", a non-primitive request, a primitive PR and a non-primitive PR ("Not applicable"); slide `s12` at narrow, wide and print widths.
- These prove wording, parity and agreement of the five surfaces, not that the future gate works.

## 6. Owner inputs, follow-ups and accepted risks

Owner inputs still missing (named, not filled): evaluation success metric; numeric ROI threshold; approving role and who triages proposal issues; what "new team member" means and when the restriction ends; proof that a CI evaluation runs on primitive PRs (issue 487 is open); owner of caller discovery and revalidation without a registry; issue numbers for the skills registry and the skill-creator fork.

Follow-ups for the owner, not done here: (1) a routing-table row sending "propose or change a skill, command or agent" to `/sc:issue --create` (accepted risk, INV-011: `/sc:recommend` never reads section 4); (2) make `/sc:pr-submit` include the primitive section; (3) the same pointer in root `CLAUDE.md`, `README.md` and `docs/developer-guide/README.md`; (4) fix the stale `--base master` in `CONTRIBUTING.md`; (5) a permanent policy test; (6) the monolith-or-modules question.

Deviations from the issue text, for the owner to see: the bug-form sentence (C4) and the `CONTRIBUTING.md` paragraph (C6) go beyond the files the issue names; both are additive one-liners that stop two entry points from contradicting the rule.

## 7. Traceability

| Requirement | Component | Requirement | Component |
|---|---|---|---|
| FR-001 to FR-004 | C1 | FR-009 | C4 |
| FR-005, FR-006 | C1 (copy, boundaries) | FR-010 | C5 |
| FR-007 | C2 | FR-011 | C7, section 4 |
| FR-008 | C3 | FR-012 | C6 |
| FR-013 | Section 4 step 7 and section 5 | | |

## Revision 1: blocking findings of the review that the new plan must fix

The first plan generated from this design (package `TASK-WF-design-20261126-041053`) was reviewed by `/sc:reflect --mode pre` (report `.dev/reflect/pre-designPlan-20261126041502/REPORT.md`). It had seven blocking findings, listed below as defects the new plan must not repeat, with the fix each needs. The design above is unchanged: the file set, the task order and the draft text of the first plan were judged sound, so keep them. Every fix is acceptance wording or an added item. Plain prose and plain bullets only: no checkbox lines and no numbered lines anywhere in the plan, fenced code included.

Blocking findings to fix:

- B1 ASCII check: the first plan's Task 1 expected `grep -nP '[^\x00-\x7F]'` to print "only the existing 'Ruling:' line". The guide `src/superclaude/core/HOW-WE-WORK.md` has no non-ASCII line (the Ruling text at line 114 is ASCII), so a correct edit failed the check. The acceptance must say the grep prints nothing on the guide and on its plugin twin `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Verifier: the same grep on both files plus `tests/core/test_how_we_work_routing_table.py`.
- B2 Count: the last task listed eight required items for `./artifacts/pr-body-notes.md` but accepted "each of the seven items above". Write "every item listed above", with no count.
- B3 Scope checks: the first plan compared against `origin/integration`, a shared ref any worktree's fetch can move, so the checks failed on changes this branch never made; the final check also failed once `.dev/tasks` was staged, missed untracked files, and said "the files named in Tasks 1 to 7", which a per-task reviewer cannot resolve. Fix: the first step of Task 1, before the baseline test run and before any edit, records `git rev-parse HEAD` in `./artifacts/base-sha.txt`. Task 1's "src/superclaude/core/CLAUDE.md unchanged" check becomes `git diff --quiet <base> -- src/superclaude/core/CLAUDE.md` exits 0, where `<base>` is the SHA in `./artifacts/base-sha.txt`. The final task's scope check becomes: `git diff --name-only <base> -- . ':(exclude).dev/tasks'` lists exactly these eight files and no path under `.claude/`: `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/PULL_REQUEST_TEMPLATE.md`, `docs/onboarding/ironclaude-onboarding.html`; and `git ls-files --others --exclude-standard -- . ':(exclude).dev'` prints nothing. After a rebase the operator checks scope with `git diff --name-only origin/integration...HEAD -- . ':(exclude).dev/tasks'`. Keep the `origin/integration` text where the plan quotes the PR-template "rebased onto" line and the operator rebase step.
- B4 Manual checks: the design requires five manual scenarios (section 5 of this design) and slide `s12` at narrow, wide and print widths, recorded in the PR body; no task carried them. They need the pushed forms and template on GitHub and a browser, so they are operator steps. Add to the final task's list a "Manual checks" item: the five scenarios of section 5 and slide `s12` at narrow, wide and print widths, each marked "operator, after push, not run by the executor" with the result "pending"; the width check exists because the new card is longer than its neighbour in a two-column grid. Plain bullets only.
- B5 Footer and commit-time steps: the footer certifies the whole deck against the guide at the guide commit, but the first plan reviewed the deck before any commit or rebase and never redid it; a recorded mismatch on another slide had no defined outcome; commit 2 and the staging rule were missing; the zero-deletion check would fail on `feature_request.yml`; and the steps did not wait for the archive. Replace the commit-time bullet with this bullet and plain sub-bullets, for the operator: start only after `/sc:implement` reports the package archived; commit 1 is the guide and its plugin copy; commit 2 is `docs/developer-guide/contributing-code.md`, `CONTRIBUTING.md`, both issue forms and the PR template, with a zero-deletion check on all of them except `.github/ISSUE_TEMPLATE/feature_request.yml` (which replaces exactly one line, the `proposal` description), and `yaml.safe_load` plus the schema check on both forms; rebase onto `origin/integration` if it moved, and if the rebase changed the guide copy it over the plugin twin again and re-run `cmp` and the 16 test files, then check scope with the operator form above; redo the slide review in `./artifacts/deck-slide-review.md` against the guide at commit 1; move the footer only when that review is all "consistent" after the rebase (set it to `git rev-parse --short=8` of commit 1), otherwise leave the footer unchanged, mark the footer requirement in the PR notes "pending, blocked by recorded mismatches" and name the follow-up issue to file; commit 3 is the deck; run the two guide-equality checks `git diff --quiet <sha> HEAD -- src/superclaude/core/HOW-WE-WORK.md` and `git diff --quiet <sha> -- src/superclaude/core/HOW-WE-WORK.md` (both must exit 0) and repeat them after any rebase or review-fix commit that touches the guide; stage only the eight files named in the scope check and `.dev/tasks`, never `.claude/` or `.dev/issues/`; re-publishing the deck to the same link is an operator step to verify after merge. The deck task must not say "footer unchanged" as a final-state criterion, because the footer can move at commit time.
- B6 Deck card: the first plan paraphrased the new "Contributing rules" card of slide `s12` although this design gives its exact HTML (design lines 123 to 126, section C7). Paste that HTML verbatim in a fenced block in the deck task and require that the second card block of `s12` equals it byte for byte and contains "not available yet" and "section 4". The tokens `<h3>Contributing rules</h3>` and `issues/290` are already in the unedited card, so they prove nothing.
- B7 "Names no role" checks: Task 1 required "no named role" although section 4 of the guide already says "your lead" and the plan's own bullets say "maintainers" and "a reviewer"; the final task required notes that "name no ROI number, role or person" although its required content names the owner, a reviewer and the input "approving role and who triages proposal issues". Reword both to: "names no ROI number, no person and no invented approving role (the words owner, reviewer, maintainers and the existing 'your lead' are allowed)".

Non-blocking findings (graded Medium; they stay out of the repair, and the new plan must not repeat them):

- The baseline test run sits in Task 1, coupled to the edit: a resumed Task 1 can re-run it on an edited tree. Keep it in Task 1 (no renumbering) with the guard "skip this step if `./artifacts/baseline-tests.log` exists; write it before any tracked file differs from the recorded base".
- The middle commit (commit 2), the staging rule and the ordering after the archive are covered by B5.
- A hand edit to a placed plan skips the gate; do not rely on hand edits after placement.
- Sufficiency of the edits is covered by B5, B7 and the no-renumbering decision.

Notes the new plan may take at no cost: compare guide heading text against `git show <base>:src/superclaude/core/HOW-WE-WORK.md | grep '^## '`; copy `source.md` section 6 verbatim into the owner inputs; name `.dev/brainstorms/20261126-031900-primitive-contribution-rules/merged-requirements.md` as the place where D1 to D6, Q1, M1 to M4 and V1 are defined; keep a blank line after a new YAML block-scalar sentence in both forms; write the `Feature request` form name with its description and link CONTRIBUTING.md section 4 with its anchor.
