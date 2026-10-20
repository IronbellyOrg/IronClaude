# Design Spec: `/sc:auggie-review --revagent <model>`

- **Type**: component (command + protocol skill contract)
- **Baseline**: `origin/master` @ `c4606ce7` (branch `feature/auggie-review-revagent`)
- **Date**: 2026-10-20
- **Out of scope baseline**: `feat/litellm-gateway-tool-names` @ `713d8e42` (NOT merged; its "auggie-reviewer at all depths" Wave 2 is not part of this change). The globally installed `~/.claude` copies are not touched.

## 1. Problem

`/sc:auggie-review` spawns an internal Claude reviewer agent (`auggie-reviewer`) whose model comes only from its frontmatter (`model: opus`). The user cannot choose a cheaper or different reviewer model per run. Evidence (`.dev/eval-workspaces/review-comparison-20261020/`) shows Sonnet-led runs still paid for Opus children.

## 2. Goal

Add one flag, `--revagent <model>`, that selects the model of every **internal review-agent spawn** for that invocation, overriding the agent frontmatter. It does not change the lead session model and does not change the external Auggie CLI model (`--auggie-model` stays separate).

## 3. Grounded facts (baseline)

| Fact | Source |
|---|---|
| Only internal reviewer spawn on master: Wave 2 step 5, `auggie-reviewer` via `Task`, `--depth deep` only | `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` Wave 2 step 5 |
| Deep per-persona passes on master are **Auggie CLI** calls, not internal agents | same, Wave 2 step 4 |
| Reviewer frontmatter default `model: opus` | `src/superclaude/agents/auggie-reviewer.md` |
| `--auggie-model` (default `prism-b`) is the external CLI model | `src/superclaude/commands/auggie-review.md` Options |
| Native Agent tool `model` parameter is an enum: `sonnet`, `opus`, `haiku`, `fable` | Agent tool schema in this Claude Code session |
| Per-invocation `model` overrides definition `model`, which overrides `CLAUDE_CODE_SUBAGENT_MODEL`; `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` overrides both | https://code.claude.com/docs/en/sub-agents |
| Alias -> concrete model is resolved by Claude Code / provider (`ANTHROPIC_DEFAULT_*_MODEL`, gateway mapping); a family alias matching the session family reuses the session's exact model | https://code.claude.com/docs/en/model-config , sub-agents doc |

## 4. Interface

### 4.1 Flag

| Flag | Default | Accepted values |
|---|---|---|
| `--revagent <model>` | unset = reviewer agents use their frontmatter model (today `opus`) | exactly `opus`, `sonnet`, `haiku`, `fable` (lowercase; the native Agent tool `model` enum) |

Examples: `--revagent opus`, `--revagent sonnet`.

### 4.2 Validation (Wave 0, before any Auggie call, diff fetch, or agent spawn)

| Input | Behavior |
|---|---|
| flag omitted | `revagent = default`; spawn without a `model` argument (frontmatter wins, current behavior byte-for-byte) |
| `--revagent <v>` with `v` in the set | `revagent = v` |
| `--revagent` with no value (end of args, or next token starts with `--`) | **STOP**: `--revagent requires a value: one of opus, sonnet, haiku, fable.` |
| `--revagent <v>` with `v` not in the set (e.g. `connect`, `Opus`, `claude-sonnet-4-6`, `inherit`) | **STOP**: `--revagent: unsupported value '<v>'. Supported: opus, sonnet, haiku, fable (native Agent tool model aliases). Full model IDs and backend/gateway aliases are not accepted; map them to a backend model via your Claude Code / gateway alias configuration instead.` |

No silent substitution and no fallback to default on a bad value. `connect` is a literal user example that is **not** a supported Agent tool value, so it gets the STOP above (resolved by the supported-value rule; no user decision required).

### 4.3 Propagation

- Every internal review-agent spawn passes `model: <revagent>` when `revagent != default`. On this baseline that is the Wave 2 step 5 `auggie-reviewer` spawn.
- Any re-spawn of a reviewer agent in the same run (retry, re-run after a failed/invalid output) passes the **same** `model` argument. No new retry policy is introduced.
- `--revagent` is never passed to `auggie` and never changes `--auggie-model`/`AUGGIE_MODEL`.
- Depth `quick`/`standard`: no internal reviewer agent exists. The value is still validated; the run records `revagent_effect: none (no internal reviewer at depth=<d>)` in the audit log and prints one WARN line. Not silent.

### 4.4 Audit

Wave 0 TARGET header gains `revagent: <opus|sonnet|haiku|fable|default>`. Wave 3 `audit.log` records, per reviewer spawn, the model argument passed (or `frontmatter`). REVIEW.md `Audit` section gains `Reviewer agent model: <value|frontmatter default>`.

### 4.5 Backend alias note (docs only)

`--revagent` picks the request alias. What concrete model that alias resolves to is Claude Code / provider configuration (e.g. `ANTHROPIC_DEFAULT_SONNET_MODEL`, a LiteLLM gateway alias). If `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` is set, Claude Code ignores the per-invocation model; that is outside this command.

## 5. Files

| File | Change |
|---|---|
| `src/superclaude/commands/auggie-review.md` | `argument-hint` adds `[--revagent opus\|sonnet\|haiku\|fable]`; Options row; Usage example; Tool Coordination `Task` line mentions model; backend-alias note |
| `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` | Wave 0 validation step + STOP rows; TARGET header field; Wave 2 step 5 model propagation incl. re-spawn; quick/standard WARN; Wave 3 audit line + REVIEW.md Audit line; Error Handling rows |
| `src/superclaude/agents/auggie-reviewer.md` | unchanged (frontmatter stays the default) |
| `tests/commands/test_auggie_review_revagent.py` | new content-contract tests |
| `.claude/**` | regenerated by `make sync-dev`; never staged |

No plugin mirror of `auggie-review.md` exists under `plugins/` (verified with `find plugins -path '*auggie*'`).

## 6. Acceptance criteria

1. AC1 omitted: docs state no `model` argument is passed and frontmatter default applies.
2. AC2 valid: options row and protocol list exactly `opus, sonnet, haiku, fable`; examples use `opus` and `sonnet`.
3. AC3 invalid: protocol STOPs before expensive work with the unsupported-value message; `connect` named as an invalid example in tests.
4. AC4 missing value: protocol STOPs with the requires-a-value message.
5. AC5 propagation: Wave 2 reviewer spawn and any re-spawn pass `model: <revagent>`; never passed to `auggie`.
6. AC6 quick/standard: WARN + audit `revagent_effect: none`.
7. AC7 existing contract tests (`tests/pr_submit/test_static_grep.py`) still pass; `make verify-sync` passes.
8. AC8 live smoke: an `auggie-reviewer` Agent spawn with `model: sonnet` reports a Sonnet model; an Agent call with `model: connect` is rejected by the tool schema.

## 7. Non-goals

No model-routing framework, no new transport/provider, no frontmatter re-pin, no change to the gateway migration or the systemic-review plan, no change to `--auggie-model`.

## 8. Review Feedback (rev 2, from /sc:reflect --mode pre on plan TASK-WF-designSpec-20261020-052113)

Evidence: `.dev/reflect/pre-revagent-20261020052301/reviewer-cards.yaml`. Each item below is now a requirement.

- RF1 Command file Behavioral Flow step 1 ("Parse arguments") also validates `--revagent` so a bad value STOPs before step 2's environment checks; the protocol Wave 0 validation is the authoritative re-check and runs before `command -v auggie`.
- RF2 Command Tool Coordination `Task` line must name only the Wave 2 step 5 `auggie-reviewer` spawn (baseline text wrongly says per-persona deep passes go to `auggie-reviewer`; per-persona deep passes are Auggie CLI calls) and say the `model` parameter is passed when `--revagent` is set. Wording keeps the baseline "`Task` tool" name.
- RF3 Missing-value detection predicate is stated explicitly: no following token, or the next token starts with `--`. Validation is not conditioned on `--depth` (an invalid value STOPs at `quick` too).
- RF4 The command Options row also includes the sentence "`--revagent` picks the request alias" with the backend-alias note.
- RF5 Tests assert exact literals: the accepted list parsed from the Options row and from the protocol rule equals `{opus, sonnet, haiku, fable}` (set equality, not substring); the unsupported-value STOP sentence contains `connect`; both exact STOP messages; the missing-value predicate text; `revagent: <opus|sonnet|haiku|fable|default>` in the TARGET header; the per-spawn `audit.log` model record (argument or `frontmatter`) in Wave 3 step 8; `Reviewer agent model: <value|frontmatter default>` in the REVIEW.md Audit block; `revagent_effect: none (no internal reviewer at depth=<d>)` and the WARN; two Error Handling rows; `model: <revagent>` inside Wave 2 step 5 with the re-spawn rule; no `revagent` inside Wave 2 step 4 or the fenced `auggie` bash block; validation text precedes `command -v auggie`; `auggie-reviewer.md` still has `model: opus`. Removing any of those literals fails a test.
- RF6 Live smoke pass criteria: record `CLAUDE_CODE_SUBAGENT_MODEL` / `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` presence first; a `model: sonnet` `auggie-reviewer` spawn passes only if its reported id contains `sonnet` (self-report is corroboration, not proof); a `model: connect` Agent call passes only if rejected by the tool schema with the rejection text recorded. If the environment blocks the smoke (FORCE set, agent type unavailable), record `BLOCKED-ENV` with the reason; never fake a pass.
- RF7 Regression run also includes `tests/core/test_how_we_work_routing_table.py` and `tests/cli/reflect/test_remediation_source_template.py`; a failure that reproduces on unmodified `origin/master` is recorded as pre-existing, not counted.
- RF8 Only the three `src/` files plus the new test (and `.dev/` planning artifacts) change in the commit; no `.claude/` path.

## 9. Review Feedback (rev 3, from /sc:reflect --mode pre on plan TASK-WF-designSpec-20261020-052949)

Evidence: `.dev/reflect/pre-revagent-rev2-20261020053124/return-contract.yaml`.

- RF9 Clarifies RF8: because `src/superclaude/agents/auggie-reviewer.md` is unchanged (section 5), the commit's non-`.dev/` paths are exactly `src/superclaude/commands/auggie-review.md`, `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, and `tests/commands/test_auggie_review_revagent.py`.
- RF10 The command Behavioral Flow step 1 acceptance check requires text saying an invalid or missing `--revagent` value STOPs there, before step 2 environment checks (a bare mention is not enough), and a test asserts it.
- RF11 The quick/standard WARN line is a fixed literal, `WARN: --revagent <value> has no effect at --depth <d> (no internal reviewer agent)`, and a test asserts it.
- RF12 The unsupported-value examples (`connect`, `Opus`, `claude-sonnet-4-6`, `inherit`) live in the same Wave 0 bullet as the unsupported-value STOP message; the test asserts `connect` appears in that bullet. The live smoke record states that the reported model id is corroboration only, not proof.
