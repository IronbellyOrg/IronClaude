# Tier 1 observation

## Provenance

runs-in=current-worktree; arm=current-help-parser; captured by parent through Bash using the public uv run superclaude entry point. No model dispatch, custom prompt file read or job execution occurred. Historical revisions from the issue are not equated to this run.

## Captured commands

| Command | Exit | Captured output |
|---|---|---|
| uv run superclaude swarm scaffold --help | 0 | ./scaffold-help.txt |
| uv run superclaude swarm validate-lenses --help | 0 | ./validate-lenses-help.txt |
| uv run superclaude swarm run --help | 0 | ./run-help.txt |
| uv run superclaude swarm run --custom-prompt-dir /tmp | 2 | ./run-rejection.txt |

## Observation

The first help capture contains `whose prompts flow in from --custom-prompt-dir at preflight` (lines 23-25). The second contains `its prompt body flows in from ``--custom-prompt-dir`` at preflight` (lines 6-8). The parser capture is exactly:

```text
Usage: superclaude swarm run [OPTIONS] [SPEC_PATH]
Try 'superclaude swarm run --help' for help.

Error: No such option '--custom-prompt-dir'.
```

The rejected path /tmp was an inert option argument; the parser rejected the option before input resolution or preflight. Public run help advertises a positional SPEC_PATH and --stdin, not the rejected option. No conclusion about successful custom-job execution follows from these captures.

## Grounding limitations

Augment retrieval returned HTTP 403; no alternative Auggie tool is available. Native source reads and codegraph outline/caller leads were used instead. No cross-environment control is claimed. Host/process/user/filesystem/network/clock/permission/version/env equivalence to the November 16 captures is unknown and unnecessary for the narrower current-checkout help mismatch observation.
