# Effective Input Manifest

## Selector and state

selector_command: none; diagnosis uses explicit source and captured-output paths, not an indirect diff/range selector.
selector_cwd: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s
base_ref/head_ref: n/a, no commit range selected.
dirty_files/staged_files/unstaged_files: existing staged task packages excluded from claimed product surface; only diagnostic counter bookkeeping modified by this invocation. Concurrent other diagnostic counter entries preserved, not claimed as this work.

## Surface

included_files: commands.py help ranges, schema.py685-734, preflight.py1569-1615, docs/swarm/command-reference.md56-61, original scaffold-help.txt, validate-lenses-help.txt, run-help.txt and run-rejection.txt.
excluded_foreign_commits: [] (no commit selector).
runtime_surface_claim: current worktree public help and run option rejection, not custom-job execution or implementation diff.
intersection_proof: no indirect selection; explicit artifacts and literal source paths independently read by hypothesis/calibration workers. Not a machine-checked Git surface manifest.

## Validation and verdict

validation_command/result: public help captures and module-origin.txt bind the current source to output; no selector validation command applicable.
HC4 N/A: no independent gate chooses an implementation surface via an indirect selector. A future post-fix review must account for the actual fix diff; this card does not certify it in advance.
