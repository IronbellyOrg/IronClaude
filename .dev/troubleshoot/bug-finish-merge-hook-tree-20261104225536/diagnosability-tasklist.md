# Diagnosability tasklist (informational; verdict partial, trivial)
discriminator-required: no
## Emitter search
- none required: probe-c4.out observes the committed tree and the validated tree directly.
## Pending rows
- P-1: regression test, a pre-commit hook that rewrites and stages an unrelated file: predicted true outcome FINISH_FAIL tree_dirty naming the commit, exit 2, nothing pushed; false outcome (exit 0 with a merge_sha) means the comparison is missing. re-run permitted: yes. Status: observed (P-1 fails on 62121669, passes with the fix; see audit.log)
- P-2: a hook that changes nothing: predicted exit 0 with the merge commit (the comparison does not false-positive); false outcome tree_dirty means the recorded tree is wrong. re-run permitted: yes. Status: observed (P-1 fails on 62121669, passes with the fix; see audit.log)
