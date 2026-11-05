# Tier 1 observation
- Source read (orchestrator): scripts/finish-merge.sh:271-276 runs the one `git commit -F "$MESSAGE_FILE"` with hooks on, after steps 4 and 5 validated the index; :278-286 checks only the parents; :288-292 checks only that the work tree and index equal the new commit. Nothing compares the committed tree with the index the gate validated, so a hook that edits and stages a file changes what is committed after validation.

## Probe (run 2026-11-04T22:55:36Z, same-shell, scratch repos under /tmp via the repository's own test fixtures, script at 62121669; command: uv run python probe_c4.py; full output in probe-c4.out)
    finish stdout: {"merge_sha":"8e6db1fa...","parents":["1abb0e9f...","c2fbf92e..."]}
    exit: 0
    validated index tree: 75418c017f5d2d55bf0710617615f11fd9b218ae
    committed tree:       1eea654f1b8e161e2b2d46bbefd94599c5f39fd5
    unrelated.txt in HEAD: changed by hook

## Behaviour definitions
- (a) observed: a pre-commit hook that rewrites and stages `unrelated.txt` makes git commit that staged change; finish-merge.sh exits 0 and the commit's tree differs from the index validated before the commit (probe-c4.out:2-5).
- (b) observed: after such a hook the work tree is clean against the new commit, so step 8 passes (exit 0 above).
