# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Assumption: the vote attaches to the existing question key `(Run id, message.id)` retained by the observer (git show origin/master:src/superclaude/cli/observe/questions.py, `QuestionRecord.key`).
- Assumption: the stored record lives in the observer state directory `$XDG_STATE_HOME/superclaude/observe` using the existing atomic-write helper (git show origin/master:src/superclaude/cli/observe/export.py, `state_dir()`, `write_atomic()`).
- Assumption: the vote is a local file write only and never reaches Orca, matching the module's design (git show origin/master:src/superclaude/cli/observe/commands.py docstring "Read-only"; view.py `Effect` docstring "no effect ever reaches Orca").
- Added beyond the description: concrete files and tests named from origin/master (view.py Decision Desk/`apply_key`/`Effect`, keys.py, tests/observe/test_view.py, test_export.py, test_commands.py).
- Added beyond the description: the acceptance criterion that no approval/dispatch/retry/merge action is added (from #409's stated scope, as relayed by the orchestrator).

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- The observer is read-only by design (git show origin/master:src/superclaude/cli/observe/commands.py, module docstring "Read-only. The only Orca calls are the ones adapter.py makes"; view.py `Effect` "no effect ever reaches Orca"; #409 dashboard scope: no approval, dispatch, retry or merge actions). A vote is the first write-from-input in the dashboard. Not a blocker if it stays a local state file, but the owner must decide this explicitly.
- The description's end goal ("better train when and how the agent should have handled that autonomously") has no consumer in the codebase; only the recording can be specified today, the training side is "Not known yet".
