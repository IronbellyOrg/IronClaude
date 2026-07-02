# Patterns & Integration Research

Status: Complete

## Initial context from retrieval

- `sc-pr-submit` already documents Wave 1 as an arming-only integration point for `DetectionContract.for_arming()`: the command opens/verifies the PR first, then Wave 1 loads the locked detection contract and arms exactly one in-session monitor at `--monitor >= 1`; `--monitor 0` stays no-monitor.
- The shipped detection contract ref is intentionally unlocked, while the arm path prefers an operator-local gitignored locked override under `.dev/pr-monitor/`.
- `superclaude reflect` is a Click group in `src/superclaude/cli/reflect/commands.py`; current concrete command is `run`, so a new `contract-status` would fit as an additional `@reflect_group.command(...)` sibling rather than inside `run()`.

## Findings

### 1. Current `pr-submit` arming gate pattern

- The protocol-level stop condition is currently documentation-first: `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:52-56` says `--monitor >= 1` must stop if the PR target cannot be confirmed or if `detection-contract.md` is `locked: false`, with the operator instruction framed as T-210 "probe first".
- The wave topology in `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:77-90` places detection-contract loading in Wave 1 only. Wave 0 handles PR creation and target verification; Wave 1 loads `superclaude.pr_submit.DetectionContract.for_arming()`, then initializes output/run-log/baseline and calls the Monitor tool. This is the right seam for a no-monitor-armed halt: it must occur after `for_arming()` fails and before any Monitor call, poll loop, baseline mutation, or downstream FSM side effect.
- The command doc mirrors this in `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:59-74`: `--monitor 0` always works; `--monitor >= 1` requires a locked contract; the shipped ref remains `locked: false`; `DetectionContract.for_arming()` prefers the operator-local override; command file does parse/environment-validation/handoff only and explicitly does not execute the monitor by itself.

### 2. Actual loader and exception text

- The loader lives in `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py`. `DetectionContractLocked` is documented as the T-210 mechanical gate at `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py:71-76`.
- `DetectionContract.load()` resolves explicit path first, then operator-local override only when `prefer_local_override=True`, else the shipped ref; it raises `DetectionContractLocked` on absent file, unparsable YAML, or `locked != true` at `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py:147-188`.
- The current exact unlocked-contract exception text is in `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py:183-187`:
  - `detection contract is locked:false (or absent) — run the R1 probe first and flip locked:true before arming (T-210)`
- `DetectionContract.for_arming()` is the documented arm surface at `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py:190-199`; it is exactly `return cls.load(prefer_local_override=True)`. This is a good low-risk place to reuse for a reflect-side status check, but not a good place to add side effects.

### 3. Existing test coverage for the arming gate

- `/config/workspace/IronClaude/tests/pr_submit/test_detection_contract.py:76-97` asserts shipped `DetectionContract.load()` halts on `locked:false`, explicit unlocked files halt, absent files halt, and `require_locked=False` allows inspection.
- `/config/workspace/IronClaude/tests/pr_submit/test_detection_contract.py:100-125` asserts the local override is honored only on the arm path: default `load()` ignores the override, `DetectionContract.for_arming()` loads it, and missing override falls back to shipped source and halts.
- `/config/workspace/IronClaude/tests/pr_submit/test_monitor_arm.py:26-43` tests Monitor arming cardinality for the pure FSM seam: `--monitor 1` arms once; `--monitor 0` never arms and stays `S0_IDLE`. These tests do not currently assert the locked-contract failure happens before Monitor arming; that is the missing integration behavior for the proposed halt.
- `/config/workspace/IronClaude/tests/pr_submit/test_skill_parse.py:57-68` pins parse-level default behavior: omitted `--monitor` defaults to `2` and `armed is True`; explicit `--monitor 0` gives `armed is False`.

Recommended test placement for exact no-monitor-armed halt text:

1. Add/extend detection-contract tests under `/config/workspace/IronClaude/tests/pr_submit/test_detection_contract.py` for any new helper that converts `DetectionContractLocked` into operator-facing status text.
2. Add an integration-style no-side-effect test under `/config/workspace/IronClaude/tests/pr_submit/test_monitor_arm.py` if the implementation introduces a setup/arm wrapper around `for_arming()` and `arm_monitor`; assert recorder calls remain `0` on locked-contract failure.
3. If the operator-facing status is surfaced through the reflect CLI, add a CLI help/output test under `/config/workspace/IronClaude/tests/cli/reflect/test_cli_smoke.py`; existing patterns already assert group help and subcommand help at `/config/workspace/IronClaude/tests/cli/reflect/test_cli_smoke.py:38-48`.

### 4. Reflect CLI structure and where `contract-status` fits

- The Click group is declared in `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py:47-73`. The group callback currently contains only the recursion breaker and exits before subcommand parse-time path validation when `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE == "1"`.
- The only current subcommand is `run`, declared as `@reflect_group.command()` starting at `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py:76`. Its body executes the post-reflect wrapper and writes `reflect_post:` to a tasklist; it is not the right place for a detection-contract status command because it requires a tasklist argument and launches/derives reflect-run configuration.
- A `contract-status` subcommand should be added as a sibling near the existing `run` command, e.g. another `@reflect_group.command("contract-status")` after the group callback and before or after `run`. It should import `DetectionContract` lazily inside the command body, following the current heavy-import pattern in `run()` (`resolve_config` and `ReflectRunner` are lazy imports at `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py:205-206`).
- Top-level CLI registration is already complete: `/config/workspace/IronClaude/src/superclaude/cli/main.py:440-442` imports `reflect_group` and registers it as `superclaude reflect`. Therefore adding a subcommand to `reflect_group` needs no new top-level registration file change.
- Existing reflect CLI tests import `reflect_group` directly from `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py` (`/config/workspace/IronClaude/tests/cli/reflect/test_cli_smoke.py:14`) and test `reflect_group --help` (`/config/workspace/IronClaude/tests/cli/reflect/test_cli_smoke.py:38-41`). That is the natural place to assert `contract-status` appears in group help and has side-effect-free output.

### 4b. `/sc:reflect` slash-command protocol surface

- [CODE-VERIFIED] `/config/workspace/IronClaude/src/superclaude/commands/reflect.md:111-131` states the command file only parses/validates and hands off; full `/sc:reflect` behavior lives in `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md`.
- [UNVERIFIED design decision] The design recommends implementing the testable CLI surface as `superclaude reflect contract-status [--validate] --repo --pr`, while the requirements examples use `/sc:reflect --contract-status --validate --repo --pr`. The generated task must preserve this as Fork B / OQ-2 before dependent implementation.
- Required reconciliation in the tasklist: if OQ-2 accepts the recommended B1 path, implement the Python CLI subcommand in `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py`, update `/config/workspace/IronClaude/src/superclaude/commands/reflect.md` to document the readiness path, and update `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md` only enough to route/describe contract-status as a readiness bypass rather than launching the normal UC-1/UC-2 audit machinery. If OQ-2 chooses a skill-markdown flag instead, the task must update the command/skill surfaces and tests accordingly and avoid adding an unused CLI command.
- Contract-status behavior must remain diagnose/validate-first: call the `superclaude.pr_submit.contract_setup` facade, render readiness/blockers/next command, do not call `ReflectRunner`, do not launch `ClaudeProcess`, do not write the local lock by default, and do not arm any monitor.

### 5. No-side-effect boundaries

Current boundaries are split cleanly:

- `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py:1-10` says detection consumes injected/fetched payloads and contains no review-fetch command tokens; real review fetch is delegated to the bash poller. `poll_augment_review()` is classification convenience, not arming, and defaults to a neutral unlocked placeholder when no contract is supplied (`/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py:219-250`).
- `/config/workspace/IronClaude/src/superclaude/pr_submit/fsm.py` keeps side effects as injected `RunConfig` seams: `arm_monitor`, `do_push`, `do_reply`, `do_resolve`, `do_retrigger`, and `invoke_auggie_review` all default to no-op in `/config/workspace/IronClaude/src/superclaude/pr_submit/fsm.py:716-759`. The live protocol skill owns actual Monitor/GitHub/Git side effects.
- `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:93-96` documents ordinal side-effect ceilings: L1 proposes no edits, L2 halts before push/reply, only L3 performs push/reply/resolve/retrigger; decline fallback is strict-once.
- `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md:74-80` states the command file must not execute the monitor by itself and will not run headless, push upstream/default branch, auto-lock the contract, apply edits at L1, or push/reply at L2.

Implication for `reflect contract-status`: it should only inspect/parse detection-contract state and emit status. It must not call `Monitor`, `poll_augment_review()` against live gh data, PR mutation scripts, push/reply/resolve/retrigger scripts, `run_skill()`, or resume logic. Prefer using `DetectionContract.load(..., require_locked=False, prefer_local_override=...)` plus existence/source metadata if status must distinguish shipped vs local override. If it calls `DetectionContract.for_arming()`, catch `DetectionContractLocked` and report the halt without letting any monitor seam run.

### 6. Exact operator-facing halt text recommendation

Current exact exception text lacks the explicit "no monitor armed" phrase. For the requested contract-status/pr-submit setup halt, preserve the existing T-210 wording and add the missing side-effect guarantee. Recommended exact operator-facing text:

`HALT: detection contract is locked:false (or absent) — run the R1 probe first and flip locked:true before arming (T-210). No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.`

Why this text:

- First sentence matches the existing loader wording in `/config/workspace/IronClaude/src/superclaude/pr_submit/detection.py:183-187` closely enough to keep current test intent.
- "No monitor armed" directly covers the new operator-facing requirement.
- The enumerated no-side-effect list maps to the requested boundaries and to the protocol side-effect phases in `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:90-96`.

Suggested tests for this exact text:

- `/config/workspace/IronClaude/tests/pr_submit/test_detection_contract.py`: assert a helper/status renderer includes `HALT: detection contract is locked:false (or absent)`, `T-210`, and `No monitor armed` when shipped/local contract is unlocked or absent.
- `/config/workspace/IronClaude/tests/pr_submit/test_monitor_arm.py`: assert the arm wrapper catches locked-contract halt before invoking `arm_monitor` (`calls == 0`).
- `/config/workspace/IronClaude/tests/cli/reflect/test_cli_smoke.py`: assert `superclaude reflect contract-status` exits non-zero or a documented status code for unarmed status, prints the exact no-monitor-armed halt text, and does not construct `ReflectRunner`/`ClaudeProcess` or call any pr-submit side-effect seams.

### 7. Source-of-truth and sync rules

- `/config/workspace/IronClaude/CLAUDE.md:18-29` is explicit that `.claude/{skills,commands,agents,hooks,templates}` is gitignored sync-dev output, only `.claude/settings.json` is tracked, and changes must be moved to `src/superclaude/` first.
- `/config/workspace/IronClaude/CLAUDE.md:141-149` says `src/superclaude/` is canonical for distributable components; edit `src/superclaude/skills/` or `src/superclaude/agents/`, then run `make sync-dev` and `make verify-sync`. The Makefile actually syncs commands too.
- `/config/workspace/IronClaude/Makefile:108-163` shows `make sync-dev` copies `src/superclaude/skills/*`, `src/superclaude/agents/*.md`, `src/superclaude/commands/*.md`, hooks, and templates into `.claude/`.
- `/config/workspace/IronClaude/Makefile:165-249` shows `make verify-sync` checks skills, agents, and commands for drift and reports command files present in `.claude/commands/sc/` but missing from `src/superclaude/commands/` as non-distributable.

Implementation implication: update `/config/workspace/IronClaude/src/superclaude/commands/reflect.md`, `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md`, and `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` first if docs change; then run `make sync-dev` and `make verify-sync`. Do not edit or stage `.claude/commands/sc/reflect.md`, `.claude/commands/sc/pr-submit.md`, or `.claude/skills/sc-pr-submit-protocol/SKILL.md` directly.

## Gaps and Questions

- [UNVERIFIED design decision] OQ-2/Fork B must be resolved before implementation. This research defaults to the design-recommended sibling CLI command `superclaude reflect contract-status [--validate] --repo --pr`, with `/sc:reflect` command/skill docs updated to describe or route that readiness path.
- [UNVERIFIED design decision] OQ-3/V2 live capture is deferred; no task item should add live `gh` capture until file-based evidence loading, validation, and reporting pass.
- [CODE-VERIFIED] The pr-submit missing-contract halt must catch `DetectionContractLocked` before Monitor arming and render the canonical sentence: “No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.”

## Key Takeaways

- [CODE-VERIFIED] Add `contract-status` as a sibling under the existing `reflect_group`, not as flags on `reflect run`, unless OQ-2 is explicitly resolved differently.
- [CODE-VERIFIED] Update `src/superclaude/commands/reflect.md` and `src/superclaude/skills/sc-reflect-protocol/SKILL.md` in source-of-truth to keep slash-command behavior coherent with the CLI readiness surface.
- [CODE-VERIFIED] Setup/readiness paths must not call Monitor, `ReflectRunner`, `ClaudeProcess`, push/reply/resolve/retrigger/resume, or live polling.
