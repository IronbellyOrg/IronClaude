5dc29d23b15eb7db4ead50623bb409f696a0d7d3
Family: inventory-coverage-labels (covers F1.1 of review r1-1)
- Defect form: a line of final-inventory.md labels a file as covering the style and exception tests although the file's diff is unrelated to the style change (here tests/recommend/test_routing_refresh.py).
- Probe command: grep -n -e "Style and exception-test coverage" -e "test_routing_refresh" .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/final-inventory.md
- Before-output: line 133 (the Style and exception-test coverage line, which names test_routing_refresh.py) and the table row for the file.
- Coupled sites: the combined path table lists the file as edited, which is true and stays.
- after: (grep -n -e "Style and exception-test coverage" -e "test_routing_refresh" on the inventory)
  - 19: tests/recommend/test_routing_refresh.py                |  2 +-
  - 100:| `tests/recommend/test_routing_refresh.py` | edited |
  - 133:Style and exception-test coverage: `src/superclaude/output-styles/pragmatic.md` (edited) and `tests/commands/test_sweep_command.py` (new, the style and skill pins).
  - 135:Routing-test edits: `tests/recommend/test_routing_refresh.py` and `tests/core/test_how_we_work_routing_table.py` were edited only to add the new `sweep` command to th
