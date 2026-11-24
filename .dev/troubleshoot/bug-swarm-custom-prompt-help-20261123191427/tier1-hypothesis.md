# Hypothesis: Two current-checkout help passages name a nonexistent run flag
**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-11-23T19:18:41Z
**Cause class**: Other, help wording contradicts documented configuration.
**Claim class**: `static_defect`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned, proposed correction follows JobSpec interface.
consistency_with_docs=aligned
runs-in=current-worktree
flags: type=bug depth=quick fix=false

## Claim
Two literal help passages describe --custom-prompt-dir as an option while the documented interface is the JobSpec custom_prompt_dir field with lens custom. Both passages appear in parent-captured help, and the public run invocation rejects that option. This is a bounded wording mismatch, not successful custom-job execution or verified repair.

## Evidence
- P1 and P2 in ./producers.md:7-8; src/superclaude/cli/swarm/commands.py:438 says “from ``--custom-prompt-dir`` at preflight”; :3785 says “flow in from --custom-prompt-dir at preflight”.
- docs/swarm/command-reference.md:56-60 says the directory is not a run flag and names JobSpec custom_prompt_dir with lens custom.
- Parent arm current-help-parser: uv run superclaude swarm validate-lenses --help exited0, ./validate-lenses-help.txt:7 contains the stale option. uv run superclaude swarm scaffold --help exited0, ./scaffold-help.txt:24 contains it too.
- Same arm: uv run superclaude swarm run --custom-prompt-dir /tmp exited2; ./run-rejection.txt:4 is `Error: No such option '--custom-prompt-dir'.`

## Proposed Fix
Correct only the two help passages to identify the JobSpec field, custom lens and spec-file invocation. Do not add a flag.
- src/superclaude/cli/swarm/commands.py: revise those passages.
- tests/swarm/test_commands_run.py: add public-group help/parser checks: both help outputs name the field and no longer advertise the option; run still rejects it with exit2.
Existing test_run_cmd_help_lists_all_input_modes (:192-206) and test_run_cmd_help_via_main_swarm_group (:209-216) were read by worker, not run. New checks are proposals.

## Confidence
Self-reported confidence: 0.95, bounded wording defect only.
- Evidence grounding: 1.0, source and captures read.
- Runtime check: 1.0, inherits Evidence grounding for static_defect; parent captures corroborate.
- Symptom coverage: 1.0, both producers and rejecting consumer covered.
- Reproducibility fit: 1.0, public CLI parent captures in named worktree.
- Fix directness: 1.0, wording correction without parser semantics change.
- Domain coherence: 1.0, follows docs and schema/preflight field names.

## Risks
Do not imply every custom spec requires a directory; inline custom prompts remain supported. Leave schema.py:685-734 and preflight.py:1569-1615 unchanged, including guard handling.

## If I'm wrong, it's probably because...
The public entry point resolved a different installation from the inspected checkout.

## Falsification standard
A parent-authorized provenance-bound repetition against unchanged source would refute correspondence if either help command omitted its alleged option text; incomplete capture remains unobserved.

## Evidence classification
Claim static_defect: literal wording contradicts interface. Evidence source_static, with parent runtime corroboration. Runtime checks: yes by parent, no by worker. No repair/test/custom job executed. REFUTE coverage not applicable, AFFIRM.

## Alternatives considered
Adding a flag rejected: changes interface instead of correcting wording.

## Grounding gaps
Diagnosability partial: ./diagnosability-context.md. Augment403; native source reads supplement graph leads. Five tasklist rows pending; no environment comparator, control proof, repaired-state witness or successful custom job. No disputed primitive behavior beyond captured outputs is claimed. Parent persistence of restricted worker result; no worker writes/execution.
