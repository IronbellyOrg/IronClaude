# Codebase Context — Reflect Detection Contract Flow

## Relevant surfaces

- `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` Wave 1: monitor ordinal L1+ loads `superclaude.pr_submit.DetectionContract.for_arming()`, prefers `.dev/pr-monitor/detection-contract.locked.md`, falls back to shipped unlocked ref, and refuses to arm if no locked contract resolves.
- `src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md`: shipped contract schema and the existing evidence-first rule. It ships with `locked: false` and instructs the operator to populate probe-locked values from an empirical probe.
- `src/superclaude/pr_submit/detection.py`: `DetectionContract` dataclass, `from_yaml`, `load`, `for_arming`, `_extract_yaml_block`, and `poll_augment_review`. The loader raises `DetectionContractLocked` on absent/unparseable/unlocked contracts. `poll_augment_review` classifies injected payloads and does not itself arm.
- `src/superclaude/pr_submit/fsm.py`: deterministic monitor state machine consumes classified findings and is separate from GitHub I/O.
- `src/superclaude/commands/pr-submit.md`: documents that `--monitor 0` works, but `--monitor >=1` requires the local locked override.
- `src/superclaude/commands/reflect.md` and `src/superclaude/skills/sc-reflect-protocol/SKILL.md`: `/sc:reflect` delegates protocol behavior to the skill and already operates as a structurally independent pre/post audit workflow.

## Architecture implications

1. Keep `DetectionContract.for_arming()` fail-closed. The UX improvement should sit before or adjacent to the arm gate, not weaken it.
2. Add reusable contract-diagnosis/lock tooling under `src/superclaude/pr_submit/` or a neutral CLI helper module so `/sc:reflect` and `/sc:pr-submit` share behavior.
3. Store repo/operator-specific locked contract in `.dev/pr-monitor/detection-contract.locked.md`; store captured probe payload and validation report under `.dev/pr-monitor/probes/<timestamp-or-pr>/`.
4. Validate by invoking existing pure classifier logic over captured GitHub payloads rather than writing a parallel parser in a skill.
5. `/sc:reflect` should diagnose and optionally orchestrate the helper, but `/sc:pr-submit` should remain the owner of monitor arming and resume side effects.
