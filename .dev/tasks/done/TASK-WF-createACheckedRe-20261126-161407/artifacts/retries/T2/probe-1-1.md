b69f41dfefdb1da4e4828bc306209c3de57c8e1a
family=lazy-transport-construction-after-acceptance
Defect: returned per-slot factory can still construct after acceptance; materialize every remaining slot before retirement.
Search: grep -n -E '_resume_slot_transport|resume_transport_factory|DONE_SENTINEL_FILENAME|constructor' -- src/superclaude/cli/swarm/commands.py tests/swarm/test_resume_crash_recovery.py
Coupled sites: resume transport preparation, its dispatch callback, shared marker retirement, constructor-failure regression, task-owned design/diff/check evidence.
Before:
src/superclaude/cli/swarm/commands.py:145:DONE_SENTINEL_FILENAME: str = "done.json"
src/superclaude/cli/swarm/commands.py:769:                # constructor default (temperature=0.2). Without this forwarding
src/superclaude/cli/swarm/commands.py:1945:    # never forwarded -- the transport always used its 0.2 constructor default,
src/superclaude/cli/swarm/commands.py:2814:            resume_transport_factory = _resolve_run_transport_factory(
src/superclaude/cli/swarm/commands.py:2836:        def _resume_slot_transport(new_pos: int) -> Any:
src/superclaude/cli/swarm/commands.py:2838:            return resume_transport_factory(original_index)
src/superclaude/cli/swarm/commands.py:2845:        (output_path / DONE_SENTINEL_FILENAME).unlink()
src/superclaude/cli/swarm/commands.py:2858:            transport_for_slot=_resume_slot_transport,
src/superclaude/cli/swarm/commands.py:3974:    target = output_dir / DONE_SENTINEL_FILENAME

After:
src/superclaude/cli/swarm/commands.py:145:DONE_SENTINEL_FILENAME: str = "done.json"
src/superclaude/cli/swarm/commands.py:769:                # constructor default (temperature=0.2). Without this forwarding
src/superclaude/cli/swarm/commands.py:1945:    # never forwarded -- the transport always used its 0.2 constructor default,
src/superclaude/cli/swarm/commands.py:2814:            resume_transport_factory = _resolve_run_transport_factory(
src/superclaude/cli/swarm/commands.py:2837:        # Materialize every needed slot now: constructor failure is rejection,
src/superclaude/cli/swarm/commands.py:2840:            index: resume_transport_factory(index) for index in remaining_indices
src/superclaude/cli/swarm/commands.py:2843:        def _resume_slot_transport(new_pos: int) -> Any:
src/superclaude/cli/swarm/commands.py:2851:        (output_path / DONE_SENTINEL_FILENAME).unlink()
src/superclaude/cli/swarm/commands.py:2864:            transport_for_slot=_resume_slot_transport,
src/superclaude/cli/swarm/commands.py:3980:    target = output_dir / DONE_SENTINEL_FILENAME
tests/swarm/test_resume_crash_recovery.py:970:def test_resume_constructor_failure_preserves_prior_attempt(
tests/swarm/test_resume_crash_recovery.py:986:        def constructor(index):
tests/swarm/test_resume_crash_recovery.py:989:                raise RuntimeError("injected delayed transport constructor failure")
tests/swarm/test_resume_crash_recovery.py:992:        return constructor
