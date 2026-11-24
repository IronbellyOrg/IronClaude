# Runtime Entrypoint Card

## Boundary and replay

producer: commands.py:438 docstring and :3785 option-help literal.
transformers: Click help formatting, public superclaude swarm registration, stdout capture.
consumer_or_evaluator: operator reading full help; public run option parser.
boundary_crossed: CLI help-to-command invocation.
replay_command: uv run superclaude swarm scaffold --help; uv run superclaude swarm validate-lenses --help; uv run superclaude swarm run --custom-prompt-dir /tmp.
production_boundary_reach_proof: captured full public CLI outputs in scaffold-help.txt, validate-lenses-help.txt and run-rejection.txt; no helper/mock. module-origin.txt resolves current checkout commands.py.

## Witnesses

forbidden_interpretation: help suggests a runnable directory flag that run does not accept.
negative_witness_command/result: original public help/parser invocations, captured stale wording and No such option, exits0/0/2. Captured pre-fix replay is accepted as defect witness, not a red regression test.
accepted_substitute_rationale: the unchanged source and real CLI capture expose the defect before any product edit; no literal revert is necessary for this negative observation.
positive_witness_command/result: NOT RUN. No fix applied or regression test authored by diagnosis-only invocation; no repaired CLI output exists.

## Verdict

HC1 FAIL: NOT PROVEN, missing mandatory fix-applied positive witness. waiver_status=latched due absent mandatory repaired-state probe, never converted to pass by calibrated diagnosis. Do not interpret this as uncertainty that the captured help strings exist.
