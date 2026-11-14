4166c9ee4d33606af931ae9a0455b22bef4f9f85
## family index-path-resolution (from r1-1)
defect form: a candidate path token is resolved by the parent-directory 'created' rule before the existing-file suffix match, so shorthand references to existing or Task-created files are kept as wrong root paths
command: grep -n -E -e "scripts/retrigger-review.sh|scripts/set-draft-state.sh|commands/issue.md" .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-designSpec-20261107-075614.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-design-20261108-041415.json .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-index.sh
before:
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-design-20261108-041415.json:4:    "commands/issue.md",
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-design-20261108-041415.json:44:    "commands/issue.md": [
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-designSpec-20261107-075614.json:6:    "scripts/retrigger-review.sh",
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-designSpec-20261107-075614.json:7:    "scripts/set-draft-state.sh",
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-designSpec-20261107-075614.json:81:    "scripts/retrigger-review.sh": [
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/index/TASK-WF-designSpec-20261107-075614.json:84:    "scripts/set-draft-state.sh": [
coupled sites: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-index.sh:30-37 (resolution loop), .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_index.py (T-2 assertions), .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/cand/candidate.md (fixture needs a shorthand case), the three index/*.json files (rebuilt)
after:
(no hits = fixed)
