# Task 5 notes: retry-ladder variable names (issue #384)

## What changed

`refs/retry.md` and `refs/ledger.md` of `sc-implement-protocol` (and their
`plugins/superclaude/` copies) named the primary-ladder variables with an
underscore after the tier digit. The workspace environment exports them without
one: `T3Model01`, `T2Model01`, `T2Model02`, `T1Model01`, `T1Model02`. The refs,
the two tests that pin the names and the ledger example now use the exported
names. `archive_workspace.py` already accepts `[A-Za-z0-9_]+` for the tier token
and was not touched.

## Behaviour change: the primary ladder now activates

The ladder rule reads "the primary ladder is active only when the four rung
variables are all set and non-empty". Before this change the refs asked for
variables that no workspace ever exported, so the check could never pass and
the fallback ladder (`haiku`, `sonnet`, `opus`) was always used.

After this change, a workspace that exports the four variables (as
`/etc/aidev02/aienv.d/defaults.sh` and the session environment do:
`T3Model01=gpt-6.1-terra`, `T2Model02=glm-5.3`, `T1Model02=gpt-6.1-sol`,
`T1Model01=claude-opus-5-5`) runs the primary ladder instead:

| Rung | Variable | Model in this workspace | Family |
|---|---|---|---|
| 0 | `T3Model01` | `gpt-6.1-terra` | GPT |
| 1 | `T2Model02` | `glm-5.3` | other (non-Claude, non-GPT) |
| 2 | `T1Model02` | `gpt-6.1-sol` | GPT |
| 3 (top) | `T1Model01` | `claude-opus-5-5` | Claude |

## Effect on adviser selection

- The executor's tier is the rung whose model id equals the executor's own
  model id. A `claude-sonnet-*` executor matches no primary rung, so its tier is
  `unknown`.
- With an unknown tier, adviser A takes the top rung (`T1Model01`) and adviser B
  uses whichever of the Claude top rung and the GPT T1 model is not adviser A's
  family (`refs/retry.md`, "Escalation rule", the `advice-3-a.md` and
  `advice-3-b.md` bullets). Here the top rung is Claude, so adviser B is the GPT
  T1 model `T1Model02` (`gpt-6.1-sol`).
- Rung 1 is a non-Claude model and rungs 0 and 2 are GPT models. Advisers now
  resolve to the primary-rung models: the top rung `T1Model01`
  (`claude-opus-5-5`), the GPT T1 model `T1Model02` (`gpt-6.1-sol`), and
  `T2Model02` (`glm-5.3`) where `refs/retry.md` sends a `T3Model01` executor's
  adviser A. Under the fallback ladder the advisers were `sonnet` (for a `haiku`
  executor) and `opus`, plus the GPT T1 model (`refs/retry.md`, fallback table);
  no adviser ran on `haiku`. A workspace that does not export all four
  variables keeps the fallback ladder unchanged.

## Not changed

The legacy slots `T1Model01` and `T1Model02` stay exported for readers such as
swarm and reflect (`tests/swarm/test_coder_tier_env_2026_10.py`); the new
sentence in `refs/retry.md` says so.
