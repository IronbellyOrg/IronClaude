# Wave 1.5 Branch A (release docs), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

- release_slug: none (controlling artifact: design package TASK-WF-design-20261104-164423 in .dev/tasks/done/)
- artifact_paths: [.dev/tasks/done/TASK-WF-design-20261104-164423/source.md]
- summary (citations are source.md):
  - Step 3 (:816) requires the index to equal the validated work tree; step 5 (:818) "proves the commit changes nothing beyond the auto-merge result plus the resolved paths": a claim about the index before the commit, not the commit made.
  - Step 6 (:819) commits "with hooks on"; the only hook outcome handled is a non-zero exit (`hook_rejected`).
  - Every other hook mention is about rejection: J-60 hooks stay on, no hook-skipping flag (:1306); J-61 hook output verbatim (:1307); J-63 no amend (:1308); INV-032 check-merge-conflict rejecting (:120, :1181, :1480); OQ-19/J-53 merge left in progress on rejection (:997, :1157, :1304); test F9 only a failing pre-commit hook (:1387).
  - Step 7 (:820) checks only the parents; step 8 (:821) checks `git status --porcelain=v1 --untracked-files=no` empty and `git diff --quiet HEAD`, mapped to merge_preflight_dirty (:824, :1113, :1203): no uncommitted tracked change after the commit.
  - Nothing compares HEAD^{tree} with the index tree validated before the commit; a hook that edits and stages a file leaves the tree clean, so step 8 cannot catch it. A design gap the script follows.
  - Prior card for steps 4-5: .dev/troubleshoot/bug-finish-merge-marker-gate-20261104215930/wave1_5-branch-A.md.
- confidence: 0.8
- re-frame: a post-commit comparison of HEAD^{tree} with the index tree recorded after step 5; turning hooks off is ruled out by J-60.
