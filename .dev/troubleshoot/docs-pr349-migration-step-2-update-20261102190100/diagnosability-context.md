# Diagnosability Context Card

**Issue**: PR #349 Codex finding: release notes migration step 2 uses `superclaude update`, which skips the codegraph phase and the retire step
**failing_component**: docs/releases/v5.0.0.md (Migration Required, steps 2 and 4) describing src/superclaude/cli/main.py:340 `update()`
**Verdict**: partial
**Complexity**: trivial (score 0: --type docs, one-file scope, deterministic, no intermittent/performance keywords, no stack trace)
**Hard-stop fired**: false
**Round**: 0 of 3 (discriminator-required: no; counter not incremented)
**Captured bytes (failing run)**: n/a (audit-time only)

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | yes | deterministic: every upgrade that follows step 2 runs update() (main.py:340-429) |
| Where | yes | docs/releases/v5.0.0.md:146-147 vs main.py:407 and main.py:242-267 |
| Why   | partial | update's output never mentions codegraph (main.py:360-405); doctor's "no codegraph registration" detail is verbose-only (doctor.py:164, main.py:497) and the check passes (doctor.py:158) |

## Branch A — Log-call inventory

Total: 22 hits. click_echo/print: 9, doctor_check: 9, exception_handler: 3, file log: 1. Richness: rich 4, minimal 10, silent 8. `degraded`: true.

## Branch B — Log-config reachability

Effective level: update has no verbosity flag (all stdout); doctor details need --verbose. Reachability: reaches_sink 22, filtered_out 13, unknown 1. `degraded`: true.

## Sufficiency rubric application

Row fired: S2 (deterministic, line-numbered evidence: the doc text and the code it contradicts are both cited by file:line), capped to `partial` by the degradation rule (auggie unavailable, Grep/Read found the signal). S14 does not apply (no disputed runtime datum).

## Implication for diagnosis confidence

Instrumentation that exists: update's phase banners, doctor's codegraph check (verbose details), the legacy-entry notice.
Gap: a user who ran `superclaude update` gets no visible signal that codegraph was skipped (doctor passes, update silent, hook silent).
Consequence: the diagnosis (doc defect) is fully grounded in static code; the gap affects how the release notes must tell users to verify the upgrade, not the root cause.
Next step: proceed to hypothesis; the fix must also make migration step 4's check able to catch a skipped codegraph phase (use `superclaude doctor --verbose` or `superclaude install --list`).

## Tasklist reference

/home/coder/workspaces/worktrees/IronClaude/release-v5.0.0/.dev/troubleshoot/docs-pr349-migration-step-2-update-20261102190100/diagnosability-tasklist.md
