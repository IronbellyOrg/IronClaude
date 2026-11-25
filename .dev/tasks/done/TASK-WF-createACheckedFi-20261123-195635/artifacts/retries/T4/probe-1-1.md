start=06ccf7288c46958c354806c28c54ed8695f301fe

## Family doc-table-split
Defect form: a new pipe row separated by a blank line is not part of the preceding Markdown table.
Command: git grep -n -F -e '| `done.json` |' -e '| `return-contract.yaml` |' -- docs/swarm/README.md docs/swarm/command-reference.md docs/swarm/user-guide.md
Before-output: README contract row :112 and marker row :114; command-reference contract row :265 and marker row :267; user-guide has no table rows of this shape. Read confirmed one intervening blank line at README:113 and command-reference:266.
Coupled sites: the two new marker rows in the AC-named README and command reference; no third row or unrelated doc table is affected. Repair only those two separators.
after: Same literal probe now shows adjacent README contract/marker rows :112-113 and command-reference rows :265-266. The runnable documentation check now asserts that adjacency and reports TABLE OK for both. Claim search/link checks pass and all 25 quickstart tests pass after the repair.
