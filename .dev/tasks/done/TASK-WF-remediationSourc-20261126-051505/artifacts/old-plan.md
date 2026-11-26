---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-remediationSourc-20261126-040738
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Make the /sc:implement retry ladder name only advisers the Agent call can start

Source: ./source.md
Goal: In a workspace that sets the model-list variables, every adviser role of the /sc:implement retry ladder is launched with an Agent `model` value the call accepts (`opus`, `sonnet`, `haiku` or `fable`), the value passed is recorded on the advice header, and a new test pins the rule for every adviser role and every executor tier (GitHub issue 393).

## Constraints

- Scope: change only the files named in the tasks below (`src/superclaude/skills/sc-implement-protocol/refs/retry.md`, `src/superclaude/skills/sc-implement-protocol/SKILL.md`, their two copies under `plugins/superclaude/skills/sc-implement-protocol/`, `tests/skills/test_task_workspace_lifecycle.py` and the new `tests/skills/test_implement_launch_alias.py`). Edit nothing under `.claude/` or `.dev/issues/`.
- The rule being written: on the fallback ladder the Agent call's `model` is the rung's own alias; on the primary ladder it is `opus` for every adviser (adviser A, adviser B, the critique adviser and both escalation-2 advisers); an adviser whose picked id does not start with `claude-` is still launched on `opus` and its line 1 carries `family-fallback: <reason>`; this never STOPs and never prompts the user.
- The new text in `retry.md` must not start any line with `GPT spawn path: ` (a test requires exactly one such line, at the pinned line 183), and must keep the backticked phrase `family-fallback: <reason>` and the phrase "never STOPs and never prompts the user" (`tests/skills/test_implement_adviser_family.py`, lines 73 to 85).
- The new text must not contain the words `halt`, `Ruling` or `E-HALT-QA` outside the lines a test already allow-lists (`tests/skills/test_implement_severity_static.py`, lines 296 to 299 and 420 to 434), must not contain the string `claude-gw-tier` (`tests/skills/test_model_alias_policy.py`, lines 104 to 119), and must not put a full model id after `--model` or `--models` (same file, lines 164 to 173).
- The new text must not add a fenced block containing a line that begins with `T` and a digit and has no angle bracket (`tests/skills/test_implement_severity_static.py`, lines 225 to 250), and must not add a table row whose first cell is a backticked lowercase key and whose last cell is only the digits 2 to 5 (`tests/skills/test_workflow_archive.py`, lines 1042 to 1076).
- `retry.md` must keep the four rung names `T2bModel01`, `T2Model02`, `T1Model02` and `T1Model01`, and must not contain any `T`-digit-underscore-`Model` spelling (`tests/skills/test_model_alias_policy.py`, lines 219 to 228).
- Add no flag, no stop reason, no halt reason and no extra adviser spawn (the cap of six stays); do not change the `tier=` ledger token (its value class is letters, digits and underscore) or `src/superclaude/skills/sc-implement-protocol/refs/ledger.md`.
- In table cells and prose copied from the existing worked table, use the multiplication sign `×` and not the letter `x` (the pinned test rows use `1×`).
- Out of scope, separate defects: the executor-tier tie when `T2Model01` and `T1Model02` hold the same id, and family inference from gateway ids such as `claude-gw-tier2`.
- Decided for this work (iteration 3): nothing to decide; build what the issue asks for, within its own scope.
- Observed workspace values the wording must stay true to: `T2bModel01` is `gpt-6.1-terra`, `T2Model02` is `glm-5.3`, `T1Model02` is `gpt-6.1-sol`, `T1Model01` is `claude-opus-5-5`; the three aliases `opus`, `sonnet` and `haiku` resolve to tier ids through `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

## Phase 1: Write the launch rule into the retry ladder reference

## Task 1: Add the Launch alias paragraph, the header grammar and the family-scope sentence to the source retry.md

In `src/superclaude/skills/sc-implement-protocol/refs/retry.md`, inside the `### Model ladder` section (it ends where `### Cost and caps` begins), make these edits and nothing else in this task.

- Keep the sentence "The adviser's effort is pinned by `effort:` in its agent file; do not rely on any per-call effort setting." and delete the sentence that follows it on the same line ("The model tier comes from the Agent call's `model` parameter."). On the next line, after a blank line, add the paragraph below. It sits after the pinned `GPT spawn path: none verified; family-fallback applies` line.
- In the paragraph that starts `**Resolving adviser B.**`, replace the words "the strongest reachable model" with `opus`, and replace "writes it on line 1 of `advice-3-b.md`: `model: <id> family: <claude|gpt> rung: <T1|top>`" with "writes it on line 1 of `advice-3-b.md` in the header form given under Launch alias below". Keep the backticked `family-fallback: <reason>` phrase, the sentence "the final summary lists every such fallback", the sentence "This never STOPs and never prompts the user: a missing model is configuration, not a finding." and the closing words "The verified spawn path for a GPT T1 model on this install:".

Text of the new paragraph (adjust only wording that would break a constraint above):

```text
**Launch alias.** The Agent call's `model` takes only `opus`, `sonnet`, `haiku` or `fable`, never a full model id or the value of a rung variable, so the rung id decides which adviser is picked and is not passed to the call. On the fallback ladder the call's `model` is the rung's own alias. On the primary ladder the call's `model` is `opus` for every adviser: adviser A, adviser B, the critique adviser and both escalation-2 advisers. An adviser whose picked id does not start with `claude-` (a GPT T1 model, any other family, or no reachable model) is still launched on `opus`, and the parent writes `family-fallback: <reason>` on that adviser's line 1. This never STOPs and never prompts the user.

The parent writes line 1 of every `advice-<n>-<x>.md` as `model: <id> family: <claude|gpt> rung: <T1|top> launch: <alias>`. The fields `model`, `family` and `rung` describe the pick the ladder chose, `launch` is the Agent `model` value actually passed, and no header states which family served the call. The id prefix decides `family-fallback` only for primary-ladder rung ids; the fallback ladder passes the rung's own alias, and the family reading of the ids above is unchanged.
```

Acceptance criteria:
- `retry.md` contains exactly one line that starts with `**Launch alias.**`, and it lies after the `GPT spawn path:` line and before the `### Cost and caps` heading.
- The paragraph states the four allowed values, the fallback-ladder rule, the primary-ladder rule for all five adviser roles, the `claude-` prefix test with the `family-fallback` note, and the header form with the `launch:` token; no sentence says which family served a call.
- The words "strongest reachable model" no longer appear in `retry.md`; exactly one line starts with `GPT spawn path: `; the backticked phrase `family-fallback: <reason>` and the phrase "never STOPs and never prompts the user" are still present.
- The new text contains none of the strings the constraints forbid (`halt`, `Ruling`, `E-HALT-QA`, `claude-gw-tier`, a fenced line starting with `T` and a digit); the four rung names are still present.
- `uv run pytest tests/skills/test_implement_adviser_family.py tests/skills/test_model_alias_policy.py tests/skills/test_implement_severity_static.py tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py -q` passes.

## Task 2: Change the four worked-table cells in the source retry.md and the four pinned test rows together

Depends on: Task 1

In `src/superclaude/skills/sc-implement-protocol/refs/retry.md`, in the worked table that follows "Worked example with the fallback ladder:" (four rows: `haiku`, `sonnet`, `opus` (known), unknown), replace the cell text `1× GPT T1` in the third column of every row with ``1× `opus` (GPT T1 not launchable, family-fallback)``. Leave the other columns and the header rows unchanged, so each row still ends with the cell `2× `opus``.

In `tests/skills/test_task_workspace_lifecycle.py`, in the function `test_retry_ref_rules_text` (the `for row in (` block at lines 598 to 604), change the four row strings to the same new text so each is a verbatim substring of `retry.md`. The four rows must read:

```text
| `haiku` | 1× `sonnet` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
| `sonnet` | 1× `opus` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
| `opus` (known) | 1× `opus` (top rung) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
| unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
```

Acceptance criteria:
- The four worked-table rows in `retry.md` equal the four strings above, written with `×`; no row still contains `1× GPT T1`.
- The four assertion strings in `tests/skills/test_task_workspace_lifecycle.py` equal the same four rows and the file has no other change.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_workflow_archive.py -q` passes; in particular the 22-row halt-table check still counts exactly 22 pairs because each new row ends in `2× `opus`` and not in digits alone.

## Task 3: Reword the stale primary-ladder text at lines 168 to 172 of the source retry.md

Depends on: Task 1

Lines 168 to 172 of `src/superclaude/skills/sc-implement-protocol/refs/retry.md` (the `advice-3-b.md` bullet, the bullet that starts "Every GPT adviser at any escalation is a T1 model.", and the paragraph that starts "Escalation 2 = 2 advisers on the top rung, always.") name `T1Model01` as the GPT T1 model and call an executor on `T2Model02` a Claude executor. In the workspace values listed under Constraints `T1Model01` is a Claude id, `T1Model02` is a GPT id and `T2Model02` is not a Claude model, so both statements are wrong.

First write the draft replacement wording of the changed sentences to `./artifacts/t3-wording.md` (package-relative evidence file), then apply it to `retry.md`. The rewording must follow these rules.
- Pick the GPT T1 model by the prefix rule already stated in the `advice-3-b.md` bullet (the id of `T1Model01`, else `T1Model02`, that starts with `gpt-`), and describe executors and picks by the family of the id (`claude-` or `gpt-`) and by rung position, not by a fixed variable name.
- Keep the escalation structure exactly as it is: adviser A is one rung up in the executor's own family (the top rung when the executor is on top or its tier is unknown), adviser B is from the other family, escalation 2 is two advisers on the top rung; add no spawn and no new rule.
- State in the example that every primary-ladder adviser is launched on `opus` (the Launch alias paragraph of Task 1), and that a pick that is not a `claude-` id carries `family-fallback`.
- Keep the lead-in "Worked example with the fallback ladder:" as the last words before the table, keep the four rung names reachable in the section (line 162 already holds them), and do not touch the sentence about `T2Model01` being recognized only as a match for the executor.
- The new text obeys every constraint above (no `halt`, `Ruling`, `claude-gw-tier`, no new line starting with `GPT spawn path: `).

Acceptance criteria:
- No sentence in `retry.md` lines 168 to 172 equates `T1Model01` with a GPT model or an executor on `T2Model02` with a Claude executor; the phrases "an executor on `T2Model02` or `T2Model01` gets adviser A on `T1Model02`" and "adviser A is the GPT T1 model (`T1Model01` when the executor is not already on it" no longer appear.
- The reworded example describes adviser picks by family and rung position, says that each primary-ladder adviser is launched on `opus`, and mentions `family-fallback` for a non-Claude pick.
- `./artifacts/t3-wording.md` exists and holds the draft text that was applied.
- `uv run pytest tests/skills/test_implement_adviser_family.py tests/skills/test_model_alias_policy.py tests/skills/test_implement_severity_static.py tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py -q` passes.

## Phase 2: Make the final summary list the marker from every adviser

## Task 4: Widen the family-fallback sentence in the source SKILL.md

Depends on: Task 1

In `src/superclaude/skills/sc-implement-protocol/SKILL.md`, at line 193, change the words "every `family-fallback:` header line of an `advice-3-b.md`" to "every `family-fallback:` header line of an `advice-<n>-<x>.md`". Leave the rest of the line, including "(`refs/retry.md`, Model ladder)", and every other line unchanged.

Acceptance criteria:
- Line 193 of `SKILL.md` contains "every `family-fallback:` header line of an `advice-<n>-<x>.md`" and no longer contains "of an `advice-3-b.md`"; no other line of the file differs from `HEAD`.
- `uv run pytest tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_severity_static.py -q` passes (both read `SKILL.md`).

## Phase 3: Mirror the changes into the plugin tree

## Task 5: Copy the changed retry.md and SKILL.md into the plugins skill directory

Depends on: Task 1, Task 2, Task 3, Task 4

Copy `src/superclaude/skills/sc-implement-protocol/refs/retry.md` over `plugins/superclaude/skills/sc-implement-protocol/refs/retry.md`, and `src/superclaude/skills/sc-implement-protocol/SKILL.md` over `plugins/superclaude/skills/sc-implement-protocol/SKILL.md`, so each pair is byte-identical. Then run `make sync-dev` (it copies `src/` into the gitignored `.claude/` dev copies) and `make verify-sync`; do not stage anything under `.claude/`.

Acceptance criteria:
- `diff -q` reports no difference for both pairs (src against plugins).
- `uv run pytest tests/commands/test_workflow_command.py -q` passes (it compares the two skill trees byte for byte).
- `make verify-sync` exits 0 after `make sync-dev`, and `git status --short` lists no path under `.claude/`.

## Phase 4: Pin the rule with a regression test

## Task 6: Create tests/skills/test_implement_launch_alias.py

Depends on: Task 1, Task 2, Task 3

Create `tests/skills/test_implement_launch_alias.py`, following the style of `tests/skills/test_implement_adviser_family.py` (module docstring, a `Path(__file__).resolve().parents[2]` root, the text of the source `retry.md` read once at import). It holds these checks.

- Alias set: `AGENT_ALIASES = frozenset({"opus", "sonnet", "haiku", "fable"})`, hard-coded, with a comment warning not to reuse `ALIASES` from `tests/skills/test_model_alias_policy.py`, which includes `inherit` and lacks `fable`. A doc pin reads the one line of `docs/reference/model-aliases.md` that contains "takes the aliases", collects its backticked words, drops `model` and `inherit`, and asserts equality with `AGENT_ALIASES`.
- Paragraph: the section between `### Model ladder` and `### Cost and caps` contains a line starting `**Launch alias.**`; that paragraph does not contain a line starting `GPT spawn path: `; it contains the phrases "takes only `opus`, `sonnet`, `haiku` or `fable`" and "never a full model id", the words "for every adviser", the backticked `family-fallback: <reason>` and the `launch: <alias>` header form. Also assert that the two stale phrases quoted in Task 3 are absent from the section and that the section still contains `T2bModel01`, `T2Model02`, `T1Model02` and `T1Model01`. These pins make a prose rewrite that drops the rule, or that names a GPT model as a startable spawn, fail.
- Worked table: parse the four rows after "Worked example with the fallback ladder:"; every cell of the adviser A, adviser B and escalation 2 columns is either an alias word in backticks (with its count and any short parenthetical) or names a non-launchable pick together with `family-fallback`; no cell contains a string that starts with `gpt-`, `glm-` or `claude-`.
- Resolver: a pure function `plan(executor_tier, env)` that returns, for the five roles (escalation 1 adviser A, escalation 1 adviser B, the critique adviser, escalation 2 first adviser, escalation 2 second adviser), a record with the picked id, the launch value and a `family_fallback` flag, following the selection rules in the Model ladder section: the active ladder is the primary ladder only when `T2bModel01`, `T2Model02`, `T1Model02` and `T1Model01` are all set and non-empty, otherwise the fallback ladder (`haiku`, `sonnet`, `opus`); the family of an id is read from its `claude-` or `gpt-` prefix after stripping a trailing bracketed suffix; adviser A is one rung up in the executor's family (the top rung when the executor is on top or the tier is unknown); adviser B is the other family (the first of `T1Model01`, `T1Model02` whose id starts with `gpt-` for a Claude executor, the Claude top rung for a GPT executor); the critique adviser uses adviser A's pick; both escalation-2 advisers use the top rung; `T2Model01` is never picked. The launch value comes only from the documented rule: the rung's own alias on the fallback ladder, `opus` for every pick on the primary ladder, and a pick that is not a `claude-` id (or has no reachable id) is launched on `opus` with `family_fallback` true.
- Environments, as plain dicts that never read `os.environ`: the observed values (`T2bModel01` `gpt-6.1-terra`, `T2Model02` `glm-5.3`, `T1Model02` `gpt-6.1-sol`, `T1Model01` `claude-opus-5-5`, `T2Model01` `gpt-6.1-sol`); a swapped environment (`T1Model01` a `gpt-` id and `T1Model02` a `claude-` id); an all-claude environment; the observed values with a trailing `[1m]` on every id; a partial environment with `T1Model01` set to the empty string (forces the fallback ladder); and a fallback environment whose `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL` hold tier-style ids.
- Sweep: for every environment, every executor tier of the active ladder plus `unknown`, and the five roles, assert that the launch value is in `AGENT_ALIASES` and contains no `[`, that a non-`claude-` primary-ladder pick has `family_fallback` true and launch `opus`, that the fallback ladder passes the rung's own alias, and that `T2Model01` is never an adviser. Header check: the test builds line 1 for each role as `model: <id> family: <family> rung: <rung> launch: <alias>` and asserts that it never states a served family.
- Negative controls: run the same checks against a resolver that returns the raw picked id as the launch value, and against a resolver that never sets `family_fallback`; each must be flagged (the test asserts that the checks report at least one violation for each).

Evidence for the red-then-green requirement: write to `./artifacts/t6-red-check.txt` the result of running the paragraph pin against the pre-change file read with `git show HEAD:src/superclaude/skills/sc-implement-protocol/refs/retry.md` (it must fail there) and the result of the full test file on the changed tree (it must pass).

Acceptance criteria:
- `uv run pytest tests/skills/test_implement_launch_alias.py -q` passes on the changed tree, and the paragraph-presence check fails when applied to the `retry.md` that `git show HEAD:...` prints (recorded in `./artifacts/t6-red-check.txt`).
- Each of the two negative controls is flagged, and the sweep covers every environment, every executor tier and all five roles.
- The test file does not read `os.environ`, does not import `ALIASES` from `tests/skills/test_model_alias_policy.py`, and passes `uv run ruff check tests/skills/test_implement_launch_alias.py` and `uv run ruff format --check tests/skills/test_implement_launch_alias.py`.
- `uv run pytest tests/skills/test_implement_adviser_family.py tests/skills/test_model_alias_policy.py tests/skills/test_implement_severity_static.py tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_retry_citation.py tests/skills/test_implement_retry_revert.py tests/skills/test_worker_contract.py tests/commands/test_workflow_command.py tests/hooks/test_launch_level_guard.py tests/unit/test_cli_install.py -q` passes.
