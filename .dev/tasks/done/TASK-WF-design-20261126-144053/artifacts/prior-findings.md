# Reflect report (UC-1, pre-execution): plan TASK-WF-design-20261126-134817

```yaml
contract_version: 1.9.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.79      # mean of the three blind card calibrations (0.80, 0.70, 0.87); the base card alone is 0.87
citations_total: 115
citations_revalidated: 115
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

- Spec: `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md`; tasklist: `.dev/tasks/to-do/TASK-WF-design-20261126-134817/TASK-WF-design-20261126-134817.md`
- Verdict: the plan has 3 blocking defects and must be repaired before it is implemented. Coverage: parsed 0, inferred 54, union 0.6667, S_dev_density 0.3333 (the matcher counts words; by hand 9 of the 18 unmapped rows are paraphrases covered by Tasks 1 to 7 and 9 are guide rules pinned only through the key phrases).
- Tier 2 ran because the parse-density guard fired (the design's labels DD-n, K-n, AC-n are not read by the ID pattern) and because the blind Tier 1 calibration gave C = 0.77 (below 0.85). Reviewers: analyzer (sonnet), qa (haiku), refactorer (opus); calibrator opus (`calibrator_diversity: degraded`); merge: sc-adversarial-protocol Mode A, standard depth, convergence 1.00 by majority.
- Warnings: `executor_class_resolved: false` (no executor class known, so the anti-self-confirmation guarantee is weakened); `t2_vendor_diversity: single`.
- Merged verdict file: `.dev/reflect/pre-TASK-WF-design-20261126-134817-20261126135219/adversarial/merged-output.md`; debate: `adversarial/adversarial/`.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | New guide section "Worktrees and branches" (at most 400 words, ASCII) | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:14` | matched Task 1 (containment 1.0) |
| INF-002 | The sentence about removal timing points at K1 | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:15` | none (best Task 2, 0.2) |
| INF-003 | Byte-identical mirror | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:16` | matched Task 2 (containment 1.0) |
| INF-004 | New policy tests | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:17` | matched Task 7 (containment 1.0) |
| INF-005 | Replaced worktree card and updated build footer | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:18` | none (best Task 5, 0.5) |
| INF-006 | the claim launcher and its `issue-<N>` naming, the cleanup script and its rules, the issue watcher, the `CLAUDE.md` examples at lines 318-341, the issue 290 card (525-528), the slide intro (516-518), and any extraction tool for lessons. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:20` | none (best Task 4, 0.43) |
| INF-007 | K1 is an unnumbered `## Worktrees and branches` heading between the end of the routing table (line 350) and `## Orca coordination` (line 352). It holds no marker. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:26` | matched Task 1 (containment 0.94) |
| INF-008 | K1 has bullets only, no table, so the word count is plain and the text is easy to test. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:27` | none (best Task 6, 0.44) |
| INF-009 | The checker for names lives only in the new test file. No production naming code. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:28` | matched Task 6 (containment 0.78) |
| INF-010 | K2 replaces the "(item 4 of issue 289)" clause with a pointer to K1. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:29` | none (best Task 2, 0.44) |
| INF-011 | K5 changes lines 520-524 only. The intro (516-518), the 290 card (525-528) and the "Being worked out" heading stay. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:30` | matched Task 4 (containment 0.8) |
| INF-012 | The footer at line 579 becomes the 8-character hash of the branch HEAD at the time of the edit. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:31` | matched Task 5 (containment 0.82) |
| INF-013 | The gate and the "no PR" stop apply to a fix to delivered work. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:32` | none (best Task 1, 0.43) |
| INF-014 | The guide says the issue watcher claims by itself when a Project Status moves, and that the same checks come first. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:33` | none (best Task 1, 0.29) |
| INF-015 | The text below is normative for content; the implementer may tighten wording but must keep every rule and stay at or under 400 words | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:37` | matched Task 1 (containment 0.67) |
| INF-016 | Orca creates every worktree, with an agent, at its default location (never raw `git worktree add`). | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:43` | none (best Task 1, 0.36) |
| INF-017 | One writer per worktree; a second writer gets its own. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:45` | none (best Task 1, 0.57) |
| INF-018 | reuses the original worktree while it still exists, after these checks | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:46` | matched Task 1 (containment 0.86) |
| INF-019 | Then `git fetch origin`, `git merge --ff-only origin/<base>`, check that HEAD moved, and run `orca agent launch`. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:46` | none (best Task 5, 0.33) |
| INF-020 | Any other state (PR closed unmerged, no PR, several worktrees, a worktree missing from `orca worktree list`, anything unknown): stop and ask. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:46` | none (best Task 1, 0.35) |
| INF-021 | A re-run of the claim's own earlier run (no `launch` entry in its `worktree.json`) is exempt. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:47` | none (best Task 1, 0.42) |
| INF-022 | Words are lowercase letters and digits with no run of 2 to 4 digits (cleanup reads it as an issue). | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:48` | matched Task 1 (containment 0.64) |
| INF-023 | if even `<login>/issue-<N>` is over 24, create nothing and ask the owner. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:48` | matched Task 1 (containment 0.67) |
| INF-024 | The owner pins the worktree in the Orca app when the PR opens. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:49` | none (best Task 1, 0.5) |
| INF-025 | After the merge the owner posts a Lessons comment on the issue | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:49` | matched Task 1 (containment 0.67) |
| INF-026 | A person runs `/sc:worktrees archive`, `retire` and `--apply`, and checks that comment first, because cleanup reads none. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:49` | none (best Task 1, 0.43) |
| INF-027 | Rules the text must keep (each is one test phrase in section 5) | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:53` | matched Task 4 (containment 0.75) |
| INF-028 | The row must stay ASCII and keep its 2 table cells. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:61` | matched Task 2 (containment 1.0) |
| INF-029 | The phrase "every verb is a dry run" must not appear | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:61` | matched Task 1 (containment 0.6) |
| INF-030 | `cmp` of the two files must print nothing | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:63` | matched Task 3 (containment 0.6) |
| INF-031 | Every command and flag inside `<code>` must be in the guide | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:75` | matched Task 4 (containment 1.0) |
| INF-032 | Lines 516-518 and 525-528 stay byte-identical. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:75` | matched Task 4 (containment 0.88) |
| INF-033 | File: `tests/core/test_how_we_work_worktree_policy.py`. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:79` | matched Task 6 (containment 1.0) |
| INF-034 | Fails with a clear message when the heading is missing or appears more than once. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:85` | matched Task 7 (containment 1.0) |
| INF-035 | when the bare form `<login>/issue-<N>` is itself over 24 the error text contains the word `stop` | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:87` | matched Task 6 (containment 1.0) |
| INF-036 | `16 - len(login) - digits` (the budget W). | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:88` | matched Task 6 (containment 0.67) |
| INF-037 | one heading, positioned before `## Orca coordination`, no `<!--` marker inside | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:94` | matched Task 1 (containment 0.83) |
| INF-038 | `len(_section().split()) <= 400` | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:95` | matched Task 1 (containment 0.75) |
| INF-039 | none of "Every verb is a dry run", "every verb is a dry run", "Verbs (a dry run unless --apply is given)" | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:96` | matched Task 1 (containment 0.92) |
| INF-040 | each key phrase from the list in section 3 occurs in the section | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:97` | none (best Task 4, 0.57) |
| INF-041 | `clayphi/issue-289-wtrule` (24), `clayphi/issue-834-clean` (23), `ironbelly/issue-517-orca` (24) | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:98` | matched Task 6 (containment 1.0) |
| INF-042 | `clayphi/issue-289-wtrules` (25), a name with a space, `clayphi/issue-0289` | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:99` | matched Task 6 (containment 1.0) |
| INF-043 | `averylonglogin1/issue-289` (25) gives an error containing `stop` | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:100` | matched Task 6 (containment 0.88) |
| INF-044 | `max_words_length("clayphi", 3) == 6`; `("clayphi", 4) == 5`; `("longloginname", 3) == 0` | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:101` | matched Task 6 (containment 1.0) |
| INF-045 | at least one exists; each has no `branch_errors` | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:102` | matched Task 7 (containment 0.75) |
| INF-046 | remove one key phrase from a copy of the section and assert | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:103` | matched Task 7 (containment 0.71) |
| INF-047 | `_GUIDE.read_bytes() == _TWIN.read_bytes()` | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:104` | none (best Task 6, 0.5) |
| INF-048 | the `/sc:worktrees` row contains "Worktrees and branches" and not "item 4 of issue 289" | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:105` | matched Task 2 (containment 1.0) |
| INF-049 | the deck holds "Worktree and branch protocol" and not "is being worked out in" | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:106` | matched Task 4 (containment 0.83) |
| INF-050 | `new worktree and branch`, `One writer per worktree`, `original worktree while it still exists` | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:108` | matched Task 1 (containment 1.0) |
| INF-051 | Stage only the changed files and `.dev/tasks`; never `.claude/` or `.dev/issues/`. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:112` | matched Task 7 (containment 0.78) |
| INF-052 | `make lint` on the new test file. | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:112` | matched Task 2 (containment 0.6) |
| INF-053 | Write K4 first (the tests fail on the missing section). | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:112` | none (best Task 1, 0.43) |
| INF-054 | Owner questions that stay open and go into the pull request body, not into the guide | `.dev/tasks/to-do/TASK-WF-design-20261126-134817/source.md:117` | none (best Task 2, 0.44) |

## Deviations

| # | Category | Location | What diverged | Evidence (file:line) | Severity |
|---|----------|----------|---------------|----------------------|----------|
| D-1 | Drift | PLAN:79 (Task 4 acceptance, bullet 1); PLAN:112 and SRC:106 (`test_deck_card_is_replaced_and_neighbours_untouched`) | Blocking (Decision): a broken plan check, inherited from the design (SRC:106; A-001). Task 4's acceptance and the planned deck test both require that the whole page no longer contains "is being worked out in". But the issue 290 card, which DD-5, SRC:75 and PLAN:74 all say must stay byte-identical, contains that exact phrase (the page holds it twice before the edit). Both checks therefore fail whenever the design is followed. An executor who edits the card correctly fails Task 4's acceptance and the Task 7 deck test, and may then "fix" it by editing the 290 card, which the plan and design forbid. The other half of the deck test cannot show the card was replaced either: "Worktree and branch protocol" is already the old card's heading. Affected action: Task 4's acceptance check (PLAN:79) and the Task 7 pytest run (PLAN:115, 117). Repair: requirement 6 below. | `docs/onboarding/ironclaude-onboarding.html:527` (290 card holds "is being worked out in"), `:523` (the 289 sentence), `:521` (heading already present); SRC:30, :75, :106; PLAN:74 (the plan preserves lines 525-530), PLAN:79 | HIGH |
| D-2 | Drift | PLAN:119 (Task 7 last acceptance) | Blocking (Decision): a broken plan check. The criterion says "`git status --short` lists only the guide, the mirror, the onboarding page, the new test file and files under `.dev/tasks`". The tree already has untracked `.dev/issues/289/`, `.dev/brainstorms/20261126-worktree-branch-protocol/` and `.dev/reflect/pre-TASK-WF-design-.../`. None of these is gitignored, and PLAN:26 forbids staging `.dev/issues/`. So `git status --short` will always list them and the check cannot pass. Affected action: Task 7 completion (its last acceptance criterion, PLAN:119). The first proposed fix (allow every change under `.dev/`) would hide a stray new file under `.dev/`, so the repair is the stateless check in requirement 7 below. | `.gitignore` (no `.dev/issues`, `.dev/brainstorms` or `.dev/reflect` entry; only `.dev/eval-runs`, `.dev/worktrees`, `.dev/pr-monitor`, `.dev/sprint-state`, `.dev/sweeps` at :239-256); session git status shows the three untracked paths; PLAN:26, PLAN:119 | HIGH |
| D-3 | Drift (DD-7 part b not realized in the text and not checked) | SRC:32 (DD-7 b); K1 bullets 1 to 3 (SRC:45-47); PLAN Task 1 (PLAN:32, :39) | Blocking (Decision): DD-7(b) decides that a sequential handoff of unfinished work is not caught by the claim gate or the "no PR" stop. The K1 text never states the handoff rule. Bullet 1 only says "One writer per worktree; a second writer gets its own." The gate bullet ("Check before `/sc:issue --claim`...") names no scope and no checks, so a reader applies bullet 2's checks. Those checks require a merged PR, and "no PR" means "stop and ask". A claim on a worktree holding unfinished work therefore still stops. This is the same T1 defect, whose second half is not fixed by the text. The design itself says the handoff words "were cut" (SRC:32). The plan says "use it verbatim", so it builds the defect, and no Task 1 or Task 7 check can notice. Affected action: claiming or handing off an issue whose worktree holds unfinished work with no PR (Task 1 text and acceptance). The fix adds words to a section that is 389 of 400 words by `str.split()` (recounted), so named cuts must pay for it (requirements 1 to 3 below). The step from "unscoped gate bullet" to "a reader applies bullet 2's checks to a handoff" is the reviewer's reading; the calibrator verified that the handoff rule is absent from the K1 text. Added from variant 1; variant 3 missed it. | `source.md:32` (DD-7 b), `:45` (bullet 1 has no handoff sentence), `:46` (the "no PR ... stop and ask" row), `:47` (unscoped gate); PLAN lines 32 and 39; brainstorm record of the defect: `.dev/brainstorms/20261126-worktree-branch-protocol/adversarial/adversarial/independent-check-3.md:38` | HIGH |
| D-4 | Drift | PLAN:39 (Task 1 key-phrase list); PLAN:112, :116 (Task 7 parametrization) | Medium (regraded from Blocking after Round 2; all three advocates and both blind calibrators hold Medium): the planned tests cannot notice the loss of several rules. The design says every rule has a test phrase (SRC:53) and that each test fails if its rule is removed (SRC:90). It says the key-phrase test covers "FR-002 to FR-013, FR-019, AC-4" (SRC:97). The 13 phrases (SRC:108, copied to PLAN:39) do not cover: the five reuse checks (including "no other live agent" and "no uncommitted changes"), "the watcher claims by itself" (DD-8), the re-run exemption of DD-7(a) ("is exempt"), the Orca default location (FR-004; AC-4 names "Orca location" as a key statement) and "Supervised workers follow" (FR-010). Task 1 lets the implementer "tighten the wording" (PLAN:32), so removing any of these passes Task 1's acceptance and every Task 7 test; the deletion test exercises only the 13 phrases. Why Medium and not Blocking: the plan copies the design's own list (PLAN:39 equals SRC:108), PLAN:32 still says to keep every rule, and no decision or acceptance check changes (a regression guard is weak, not a check that cannot pass). The re-run exemption and the new handoff sentence are pinned as part of requirement 4 (they repair row 3); the other groups stay a follow-up. Fix for the rest: add phrases that are already in the draft, for example `at its default location`, `Supervised workers follow`, `same repository, issue and branch`, `no uncommitted changes`, `the watcher claims by itself`; this does not change the word count. The T1 card graded only the exemption part, as Medium. | SRC:43, :45, :46, :47 (the unpinned sentences); SRC:53, :90, :97, :108; SRC:37 (the implementer may "tighten wording"); SRC:32 (DD-7 names the exemption as the repair of the earlier blocking defect); PLAN:32, :39, :112, :116; `.dev/brainstorms/20261126-worktree-branch-protocol/merged-requirements.md:266` (AC-4 "Orca location"); `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:61` (`launch` writes a `launch` entry into `worktree.json`) | MEDIUM |
| D-5 | Drift | PLAN:105 (Task 6 acceptance) | Medium: the design's `test_budget_formula` row also requires "overflow of the bare form exactly when `len(login) + digits >= 18`" (SRC:101). The Task 6 body points at that table, but its acceptance lists only the three `max_words_length` values. None of the accepted names has a bare form of exactly 24 characters (the longest accepted bare form is `longloginname/issue-289` at 23). So an off-by-one checker that says stop at 24 instead of over 24 passes every Task 6 criterion. | SRC:101, :98; PLAN:104-105 | MEDIUM |
| 6 | Documented deviation (taxonomy class not established) | PLAN:25 | Note: the plan writes the policy tests last (after Task 5); the design writes them first (SRC:112: "Write K4 first (the tests fail on the missing section)"). The plan gives a reason (each task's criteria must pass when that task finishes) and repeats the key checks by hand in Task 1's acceptance (PLAN:37-39). The cost is that no test is ever seen failing against the unchanged guide; only `test_deletion_is_detected` shows a failing case. Why a Note: the test file is delivered in Tasks 6 and 7 (moved, not omitted), nothing later rests on seeing the baseline failure, and necessity is not established, so the label is "documented deviation", not "Necessary deviation". Variant 2 first graded this Blocking (Missing) and moved to Note in Round 2; variant 1 held it is not a deviation. No repair. | SRC:112; PLAN:25, :37-39; PLAN:96-100 (test creation depends on Task 5), PLAN:100, :112, :116; SRC:103 | LOW |
| 7 | Authorized expansion | PLAN:65, :117 | Note: the plan adds `tests/skills/test_issue_protocol.py`, `test_review_brief_placement.py` and `test_spec_panel_review_loop.py` to the run list in section 6 of the design. All three read the guide or the mirror, so the extra coverage is justified. | SRC:112 | LOW |
| 8 | Necessary deviation | PLAN:106, :118 | Note: the design says "`make lint` on the new test file". `make lint` takes no file argument: it runs `lint-architecture` and then `uv run ruff check .`. The plan instead runs targeted `ruff check` and `ruff format --check` on the new file, which meets the intent. | `Makefile:48-50`; SRC:112 | LOW |
| 9 | Audit inventory gap (not a deviation of the plan) | `.dev/reflect/pre-TASK-WF-design-20261126-134817-20261126135219/artifacts/coverage-matrix.md:22-32` | Note: the reflect run's coverage inventory omits requirement-bearing spans rather than merely leaving them unmatched: creator ownership and no self-created worktree; the supervised-worker contract; the actual reuse preconditions; login lookup; creation flags and prefix fallback; branch verification, rename-before-push and no switching; lesson-comment contents and the "no reusable lesson" alternative; closeout-before-unpin ordering. Task 1 incorporates these through the normative block, so this is not evidence that their text is absent from the planned deliverable. It concerns the audit's own list, not the plan. | Omitted obligations at SRC:43-49; matrix excerpts at coverage-matrix.md:22-32 | LOW |

## Repair requirements for the plan

The repaired plan carries all ten items. Items 1 to 5 and 10 repair row 3 (and rows 1 and 2 where named); items 6 and 7 repair rows 1 and 2; item 8 completes row 1; item 9 follows from any guide edit.

1. **Row 3, exact final guide text and recount (INV-001).** The repaired plan must carry the exact final text of the guide section, with the handoff sentence and the named cuts, and a recount by `str.split()`. The recount of SRC:41-49 is 389 words (heading 4, intro 42, bullets 23, 118, 44, 96, 62); the probe counted 14 added tokens for the repairs, so at least 3 words must go, aiming at 395 or fewer against the 400 cap. `live-agent` counts as one token. The exact text is to be fixed and recounted by the plan repair; this verdict does not supply it.
2. **Row 3, what may be cut (INV-002).** The cuts must keep the backticked branch example `clayphi/issue-289-wtrule`: it is the only backticked branch example (a span of the form `x/issue-...`, SRC:48) without `<` or `>`, and Task 7's "at least one exists" test (SRC:102) fails if it goes. The plan must name the cuts, not leave them to the implementer.
3. **Row 3, scope of the handoff sentence (INV-005).** The sentence must exempt a handoff from the claim gate and from the "no PR ... stop and ask" row only, as DD-7(b) says (SRC:32). It must keep the live-agent check and the same-repository/issue/branch check. It must stand outside the "New work" sentence. Wordings rejected in the debate: "skips the checks below" and "the delivered-work gate does not apply" (too broad); "only the live-agent check applies" (also too wide; it would drop same repository/issue/branch, issue open, no uncommitted changes and ff-only).
4. **Rows 3 and 4, key phrases and the word "thirteen" (INV-004).** Add key phrases for the re-run exemption and for the new handoff sentence (the key-phrase list goes from 13 to 15; the number of tests stays 13). The exact phrases are fixed by the plan repair and must be exact substrings of the final text (variant 1 suggested a phrase built on the `launch` entry; variant 3 suggested `is exempt`). "Thirteen" means both the key-phrase count (PLAN:39, :112, :116) and the test count (PLAN:115); the repair must edit each use by hand, because a blanket replace breaks PLAN:115.
5. **Rows 1 to 3, the repaired plan overrides the design (INV-003).** PLAN:32 and PLAN:112 defer to the design. The repaired plan must say in its own text that it overrides SRC:106 (page-wide absence check), SRC:53 (rules the text must keep) and SRC:108 (the 13-phrase list). Repairing the plan alone does not fix rows 1 and 3 while it still defers to the unrepaired design.
6. **Row 1, deck check (Change 3).** Replace the page-wide absence check in Task 4's acceptance (PLAN:79) and in the Task 7 deck test with: the issue 289 sentence ("how they are named is being worked out") is gone; the phrase "is being worked out in" appears exactly once, and that occurrence is in the issue 290 card (`issues/290` still present, `issues/289` gone); the example `clayphi/issue-289-wtrule` is present. Label the defect as inherited from SRC:106 (A-001). The probe found the pair safe: before the edit the phrase occurs only at html:523 and :527, and "Being worked out" at html:517 does not match (INV-010).
7. **Row 2, git status check (Change 3; INV-006, INV-007).** Replace the last Task 7 acceptance (PLAN:119) with a stateless check that does not hide new files: `git status --short -- . ':(top,exclude).dev'` run with the repo root (the `top` form is safe from a subdirectory; INV-006), listing only the four deliverables; `git diff --cached --name-only` piped to a grep that finds nothing under `.claude/` or `.dev/issues/` (an empty `git diff --cached` proves nothing on its own, so the grep is paired with it); and a listing of the changes under `.dev/tasks`, which the pathspec hides. INV-007 also notes `uv.lock` drift is unchecked; `uv.lock` is gitignored (`.gitignore:169`, `:222`), so no `git status` check can see it, and the plan repair need not add one.
8. **Row 1, Task 4 hunk check (INV-008).** Replace plain `git diff` in Task 4 with `git diff -U0 HEAD` and say when it is run: "one changed hunk" is true only after Task 4 and before Task 5, because plain `git diff` shows only unstaged changes.
9. **Any guide edit, re-run Task 3 (INV-013, LOW).** The 400-word test is created in Task 7, and the mirror copy is made in Task 3. After any later guide edit (including the repairs above), re-run Task 3's copy, or the mirror test fails.
10. **Sufficiency (INV-014).** Repairing rows 1 to 3 makes the plan executable only if items 1 to 9 are carried, the handoff sentence does not exceed DD-7(b), and the checks run in the right state. The probe did not open `tests/core/test_claude_md_worktree_rule.py`, `test_orca_session_launch_guidance.py`, `tests/skills/test_sc_recommend_routing_contract.py` or `tests/recommend`; the repaired plan must not rely on them being unaffected until they are read.

## Follow-up candidates (Medium and advisory, not repaired)

None of these gates the plan. The verdict does not require the plan repair to fix them.

- **Unpinned phrase groups (row 4, Medium).** Reuse checks, the watcher sentence (DD-8), the Orca default location (FR-004) and "Supervised workers follow" (FR-010) have no key phrase. Candidate phrases are listed in row 4. Evidence: SRC:43, :45, :46, :47; SRC:53, :90, :97, :108.
- **Task 6 overflow value (row 5, Medium).** Add the `len(login) + digits >= 18` boundary to Task 6's acceptance, with a name whose bare form is exactly 24 characters. Evidence: SRC:101, :98; PLAN:104-105.
- **Login digit run (correctness gap 1).** The planned `branch_errors` (SRC:87; PLAN:100) looks for a 2-to-4-digit run only in the words part. Cleanup's `numbers_in_name` scans the whole branch name and the folder name, so a login with a digit run (for example `dev42/issue-289-x`) passes the checker, but cleanup reads 42 as an issue. The guide's stated reason ("cleanup reads it as an issue") applies to the login too. What cleanup then does with such a worktree was not checked by any reviewer. Evidence: `scripts/worktree_cleanup.py:1511-1514`, `:1470-1472`.
- **Hand-copied regex (correctness gap 2).** `_NUMBER_RUN` (SRC:86) copies `_NAME_NUMBER_RE` by hand and nothing ties the two together; if cleanup's bound changes, the guide's rule and the checker drift apart silently. The script already loads in tests through importlib, so the test could reuse it or assert that the two patterns match the same strings (the originals differ: `_NAME_NUMBER_RE` has a capture group, `_NUMBER_RUN` has none), without adding production code. Evidence: `scripts/worktree_cleanup.py:1462`; SRC:86; `tests/worktree_cleanup/conftest.py:20-31`.
- **Deletion-test helper (structure note).** `test_deletion_is_detected` needs a helper shared with `test_section_states_each_rule` that returns the missing phrases; neither the design's helper table (SRC:83-88) nor Task 7 (PLAN:112) names it. If the deletion test re-checks `phrase in copy` on its own, it proves nothing about the real check (pattern to copy: `_unknown_tokens`, `tests/docs/test_onboarding_deck.py:69`). The probe adds that it proves one case unless parametrized over all phrases, and that each phrase must occur once in the section (INV-012).
- **Other structure notes (not graded).** `test_mirror_is_byte_identical` is a third copy of the byte check (allowed duplication, AC-3). The deck test checks only that "Contributing rules" is present while AC-9 asks for the 290 card and intro to be byte-identical; only Task 4's `git diff` acceptance (PLAN:80) checks that. The deck card says "a person pins the worktree" (SRC:71) while K1 says "The owner pins" (SRC:49); the card shows the words as required while K1 marks them optional.
- **Low probe items.** `git rev-parse --short=8 HEAD` can print more than 8 characters; the deck regex takes 7 to 40 (INV-009). The plan never says the new deck card must stay 5 lines, so the anchors 520-524, 579, 299, 350 and 352 may move (INV-011).

## Changes not made

| Diff point | Non-base approach | Why the base approach is better |
|---|---|---|
| C-002 / X-002 | Variant 2: Blocking for promised coverage | After Round 2 variant 2 itself moved to Medium; both calibrators agree |
| C-003 / X-001 | Variant 2: Blocking (Missing) for tests-last | The test file is delivered in Tasks 6 and 7, and nothing later rests on seeing the baseline failure (variant 2 conceded) |
| C-003 | Variant 1: not a deviation | A documented deviation is recorded as a Note |
| U-001 repair | Variant 3: allow every change under `.dev/` | Hides a stray new file under `.dev/` (variant 2); replaced by the check in requirement 7 |
| X-003 repair | Variant 1 and 2 wording "skips the checks below", "the delivered-work gate does not apply" | Too broad (variant 3, INV-005): drops same repository/issue/branch and the live-agent check |

## Open owner question

Should a handoff of unfinished work also skip the same-repository/issue/branch check? The repair in requirement 3 keeps that check, because DD-7(b) (SRC:32) only exempts a handoff from the claim gate and the "no PR" stop. A handoff to another issue or branch might need it skipped; the design does not say, and the debate did not settle it. The owner decides; the answer belongs in the pull request body. No grade above depends on it.

## Recommendations

### Recommendation R-001: Replace the page-wide absence check of the deck card
- **File:** `.dev/tasks/to-do/TASK-WF-design-20261126-134817/TASK-WF-design-20261126-134817.md` (Task 4 acceptance, Task 7 deck test)
- **Change:** Replace "no longer holds the phrase 'is being worked out in'" with: the issue 289 sentence is gone, the phrase appears exactly once and in the issue 290 card, the example `clayphi/issue-289-wtrule` is present; say the plan overrides `source.md:106`.
- **Verifier:** `uv run pytest tests/docs/test_onboarding_deck.py -q` and the planned deck test pass on a correct card edit.
- **Linked deviation(s):** D-1
- **Priority:** P0

### Recommendation R-002: Replace the git-status acceptance of Task 7
- **File:** same plan (Task 7, last acceptance criterion; Task 4 hunk check)
- **Change:** Use a stateless check that hides no new file (`git status --short -- . ':(top,exclude).dev'` lists only the four deliverables; a grep over `git diff --cached --name-only` finds nothing under `.claude/` or `.dev/issues/`; the `.dev/tasks` changes are listed separately); use `git diff -U0 HEAD` for Task 4's hunk check and say when it runs.
- **Verifier:** the `git status` command prints nothing in this worktree before Task 1 starts (every current change is under `.dev/`), and after Task 7 it lists exactly the four deliverables.
- **Linked deviation(s):** D-2
- **Priority:** P0

### Recommendation R-003: State the handoff rule in the guide text and pin it
- **File:** same plan (Task 1 text and acceptance, Task 7 key phrases); draft at `.dev/reflect/pre-TASK-WF-design-20261126-134817-20261126135219/artifacts/k1-repaired-draft.md` (394 words, ASCII, 15 key phrases each once)
- **Change:** Add a sentence that exempts a handoff of unfinished work from the claim check after the first session has stopped; pay for it with named cuts that keep the backticked example; add the key phrases `is exempt` and `handoff of unfinished work`; fix "thirteen" by hand (15 phrases, 13 tests); re-run Task 3 after any guide edit.
- **Verifier:** recount with `len(text.split())` (at most 400); `uv run pytest tests/core/test_how_we_work_worktree_policy.py -v` passes and `test_deletion_is_detected` covers the new phrases.
- **Linked deviation(s):** D-3
- **Priority:** P0

### Recommendation R-004: Pin the remaining unpinned rules and the budget boundary (follow-up)
- **File:** same plan (Task 1 acceptance, Task 6 acceptance)
- **Change:** Add key phrases for the reuse checks, the watcher sentence, the Orca location and supervised workers; add the `len(login) + digits >= 18` value and a name whose bare form is exactly 24 characters to Task 6.
- **Verifier:** the policy tests list the extra cases and pass.
- **Linked deviation(s):** D-4, D-5
- **Priority:** P1 (Medium findings; not repaired by the workflow)

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 115` = 0.00

## Evidence validation (Wave 5)

- Validator: `evidence-validator` (opus) re-read 61 `file:line` citations in the Deviations, Repair requirements, Follow-up, Recommendations and header sections; 58 verified, 0 unfounded, 3 line ranges were off on true statements. The orchestrator re-read all 54 Pass 2 quotes by script against `source.md`: 0 dropped. Total 115 citations, 115 re-read, 0 dropped (`citation_budget_policy: full_reread`, although the count is above 20: every citation was re-read).
- Corrected after validation (no drop): the guide recount range (`SRC:41-49`), the coverage-matrix range of row D-9 (`:22-32`) and the conftest range (`:20-31`); one claim narrowed (the example span in requirement 2 is the only backticked branch example, not the only backticked span); the regex-equality suggestion reworded (the two patterns differ by a capture group); an unsupported claim about what cleanup does with a login that has a digit run removed; a note added that `uv.lock` is gitignored; the verifier of R-002 made consistent.
- Zero drops on 115 citations is flagged for meta-eval (`zero-drop-flag: true`); the validator itself rechecked the riskiest claims twice.
- Not checked: no reviewer or validator could run `git`; the untracked-folder claims rest on the session-start `git status` and were confirmed again by the orchestrator at 14:14 (`git status --short` listed four untracked `.dev/` paths, `git check-ignore` printed nothing).
