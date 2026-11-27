# Rebase note (after the archive)

The plan was written and executed on a base that was 59 commits behind `origin/integration` (base `862384852`). Before the push the commit was rebased onto `origin/integration` (`a98d7b428`); the rebase had no conflict. Two things changed because of the newer base, both made after the package was archived and both recorded here:

1. Integration commit `ce06ed71f` (docs(onboarding): replace the contributing card on slide s12) replaced the issue 290 card. That card no longer contains the phrase "is being worked out in", so the check of Task 4's first acceptance bullet and of Task 7's deck test ("the phrase occurs exactly once, in the issue 290 card") cannot hold on the new base. `test_deck_card_is_replaced_and_neighbours_untouched` now asserts only what still matters: the card heading and the example `clayphi/issue-289-wtrule` are present, the sentence "how they are named is being worked out" and any `issues/289` link are gone, the "Contributing rules" card and the build footer are still there. The slide opening (heading, eyebrow, introduction) changed upstream too and still calls the worktree topic open: that is the open owner question about the slide introduction, not changed here.
2. The footer hash follows Task 5's rule (the 8 characters of `git rev-parse --short=8 HEAD` at the time of the edit): after the rebase HEAD was `a98d7b42`, so the footer reads `a98d7b42` instead of `86238485`. The commit that holds the guide change still does not exist before the merge, so a person corrects the footer when the artifact is re-published.

The line numbers cited in `progress.md` and in the check logs are those of the old base (for example the guide section at line 352; it is at line 357 after the rebase). The ledger is the record of the run as it was executed.

After the rebase and these two edits: the related suites of Task 7 gave 688 passed, and `ruff check` and `ruff format --check` on the new test file pass.
