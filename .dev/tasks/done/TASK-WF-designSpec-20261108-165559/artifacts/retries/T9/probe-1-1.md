423b71c73ce63d71db2e7b853b96978b0f71e62d

## family=doc-claim-overreach (F1.1, review r1-1)

- Defect form: delivered text claims every config transport that disables the hook names `core.hooksPath` or `hook.pre-push`; `include.path` (and similar indirect config) disables it without naming either, and the guard denies it as UNKNOWN, not TAMPER.
- Command: `grep -n -i -E -e 'disables the hook|still names|still adds|left to their L1' -- .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md src/superclaude/hooks/scripts/launch-level-guard.sh plugins/superclaude/hooks/scripts/launch-level-guard.sh tests/hooks/test_launch_level_guard_l2_tokens.py docs/designs/sc-issue-launch-level-hook.md`
- Before:
  - `spec-deviations.md:22` ... "A transport that disables the hook still names `core.hooksPath` or `hook.pre-push`, so it still adds `TAMPER`." (the false sentence)
  - `src/superclaude/hooks/scripts/launch-level-guard.sh:710` "transports (--config-env, GIT_CONFIG_*) are left to their L1 classes (SD-2)." (true)
  - `plugins/superclaude/hooks/scripts/launch-level-guard.sh:710` same (true)
- Coupled sites: commit C body lines 8-10 ("The config transports --config-env and GIT_CONFIG_* keep their existing L1 classes and message ids") is true and makes no all-transports claim; no edit.
- after: `spec-deviations.md:22` now says only a transport that names `core.hooksPath` or `hook.pre-push` adds TAMPER; the `include.path` forms are denied as UNKNOWN (pinned by two new `TRANSPORT_ONLY` rows in `tests/hooks/test_launch_level_guard_l2_tokens.py`, 139 passed).
- after: guard :710 (both copies) unchanged and true.
