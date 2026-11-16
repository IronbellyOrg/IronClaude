d173296087168f5733efe0d51866ce41427d4f9f
family=after-read-evidence
defect form: a before/after "identical" claim whose table shows no stored after-side bytes and no hash for either side.
command: ls -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe-raw ; grep -n -E 'Payload identical|sha256 of raw before' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md
before-output (state reviewed in review 1):
raw folder: b-tl-all.json b-tl-ready.json b-ws-ctx_*.json (5) m-t2-workerlist.json s1.json (no a-... files)
comparison table header: | Read | Raw bytes identical | Payload identical (envelope id removed) |   (no hash columns)
section 4 table: before-side sha256 only
coupled sites: the section 4 table (one row per Dispatch) and the section 5 text for task-list; both point to the same raw folder.
after:
(the fix stores the seven after-side raw files as a-... next to the b-... files and adds before/after payload sha256 columns to the comparison table)
