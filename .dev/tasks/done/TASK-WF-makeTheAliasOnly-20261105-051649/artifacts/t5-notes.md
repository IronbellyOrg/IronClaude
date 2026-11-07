# Task 5 notes: retry-ladder variable names (issue #384)

## What changed

`refs/retry.md` and `refs/ledger.md` of `sc-implement-protocol` (and their
`plugins/superclaude/` copies) wrote the primary-ladder variable names with an
underscore after the tier digit. `/etc/aidev02/aienv.d/defaults.sh` does not
export names with that underscore; it exports `T3Model01`, `T2Model01`,
`T2Model02`, `T1Model01` and `T1Model02` (defaults.sh lines 48, 35, 37, 67, 69).
The refs, the two tests that pin the names and the ledger example now use the
exported names. `archive_workspace.py` already accepts `[A-Za-z0-9_]+` for the
tier token and was not touched. `refs/retry.md` also gained one sentence in the
Ladders paragraph: the variables are the tier slots the workspace exports,
`T1Model01` and `T1Model02` are the legacy Tier 1 slots kept for swarm and
reflect, and the fallback ladder applies when they are not all set.

## Behaviour change: the primary ladder now activates

`refs/retry.md:162` says the primary ladder is "active only when the four rung
variables are all set and non-empty". With names the workspace does not export,
that check could not pass here, so the fallback ladder was used. With the
exported names it passes in a workspace like this one, and the primary ladder
replaces the fallback ladder.

Values in this workspace (defaults.sh line in brackets; the session environment
holds the same values):

| Rung | Variable | Model | Family (`refs/retry.md:166`) |
|---|---|---|---|
| 0 | `T3Model01` | `gpt-6.1-terra` (48) | GPT |
| 1 | `T2Model02` | `glm-5.3` (37) | neither (not `claude-` and not `gpt-`) |
| 2 | `T1Model02` | `gpt-6.1-sol` (69) | GPT |
| 3 (top) | `T1Model01` | `claude-opus-5-5` (67) | Claude |

`T2Model01` is also set and is also `gpt-6.1-sol` (35), the same model as
`T1Model02`. An executor on `gpt-6.1-sol` therefore matches both rung 1 (through
`T2Model01`, `refs/retry.md:164`) and rung 2, and `refs/retry.md:164` does not
say which one wins.

GPT T1 model: `T1Model01` is `claude-opus-5-5`, which does not start with
`gpt-`, so the GPT T1 model of `refs/retry.md:168` is `T1Model02`, `gpt-6.1-sol`.

## Effect on adviser selection

A `claude-sonnet-*` executor matches no primary rung, so its tier is `unknown`,
and adviser A takes the top rung. The table gives, for every executor model this
workspace can run, the model each rule picks (rule lines are in `refs/retry.md`).

| Executor model (family) | Tier recorded | Escalation 1, adviser A | Escalation 1, adviser B | Escalation 2 | Rule lines |
|---|---|---|---|---|---|
| `gpt-6.1-terra` (GPT) | `T3Model01` | `gpt-6.1-sol` (the GPT T1 model) | `claude-opus-5-5` (Claude top rung) | 2x `claude-opus-5-5` | 169, 168, 172 |
| `glm-5.3` (neither) | `T2Model02` | `claude-opus-5-5` (top rung) | `gpt-6.1-sol` (the family that is not adviser A's) | 2x `claude-opus-5-5` | 168, 172 |
| `gpt-6.1-sol` (GPT) | `T2Model02` or `T1Model02` (ambiguous, see above) | `gpt-6.1-sol` ("else the same T1 model") | `claude-opus-5-5` | 2x `claude-opus-5-5` | 164, 169, 168, 172 |
| `claude-opus-5-5` (Claude) | `T1Model01` (top rung) | `claude-opus-5-5` (already on the top rung) | `gpt-6.1-sol` (`T1Model01` is not `gpt-`, so `T1Model02`) | 2x `claude-opus-5-5` | 167, 168, 172 |
| a Claude or neither-family model off the ladder, e.g. `claude-sonnet-5-5` (`T1Model03`, defaults.sh 71) or `grok-4.7` (`T2Model03`, defaults.sh 39) | `unknown` | `claude-opus-5-5` (top rung) | `gpt-6.1-sol` | 2x `claude-opus-5-5` | 164, 167, 168, 172 |
| a GPT model off the ladder, e.g. `gpt-6-astra` (`T0Model02`, defaults.sh 20) | `unknown` | `gpt-6.1-sol` (rule 169: the executor is GPT) | `claude-opus-5-5` (rule 168: "Executor is GPT") | 2x `claude-opus-5-5` | 164, 169, 168, 172 |

Notes on the table:

- The `refs/retry.md:172` example "on `T3Model01`, adviser A on `T2Model02`" is
  written for a Claude executor. It cannot happen here, because `T3Model01` is
  the GPT model `gpt-6.1-terra`, so rule 169 applies instead.
- For `gpt-6.1-sol` the advisers are the same whichever rung matched, because
  rule 169 does not depend on the rung.
- For a GPT executor with an unknown tier, rule 167 ("the top rung when ... its
  tier is unknown") and rule 169 point at different models for adviser A, and
  `refs/retry.md` does not say which wins. The table follows rule 169. Reading
  rule 167 instead swaps the two escalation-1 advisers (adviser A
  `claude-opus-5-5`, adviser B `gpt-6.1-sol`); the pair of models is the same.
- In this workspace every adviser, including the critique adviser (which uses
  adviser A's model, `refs/retry.md:170`), runs on `claude-opus-5-5` or
  `gpt-6.1-sol`. No adviser runs on `glm-5.3` or `gpt-6.1-terra`.
- `refs/retry.md:183` records no verified spawn path for a GPT model, so adviser
  B on `gpt-6.1-sol` still goes through the family-fallback of
  `refs/retry.md:181` when that model cannot be reached.

## Before the change

The primary ladder could not activate, because the variable names it needed
were not exported, so the fallback ladder applied (`refs/retry.md:162`). Its
table (`refs/retry.md:176-179`) names the `haiku`, `sonnet` and `opus` aliases,
but each alias resolves to `ANTHROPIC_DEFAULT_<ALIAS>_MODEL`
(`refs/retry.md:164`). In this workspace the `haiku` alias is `glm-5.3`
(defaults.sh 92), a model of neither family, so for an executor on that model
rule 168 sends adviser A to the top rung and not to `sonnet`.

The GPT T1 model was looked up under the old names with an underscore, which
this workspace does not export, so it did not resolve and adviser B took the
family-fallback of `refs/retry.md:181`. After the change it resolves to
`gpt-6.1-sol`, although `refs/retry.md:183` still records no verified GPT spawn
path.

A workspace that does not export all four rung variables keeps the fallback
ladder.

## Not changed

The legacy slots `T1Model01` and `T1Model02` stay exported for readers such as
swarm and reflect (`tests/swarm/test_coder_tier_env_2026_10.py`).
