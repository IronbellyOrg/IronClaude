# Task 4 dispatch coverage

Governing structure: Task 4 Outputs and Acceptance criteria in the sibling plan.

## Selection and dispatch traces
Manual prose-contract traces, not parser execution or live model requests:

| Input | Parsed requested selections | Native dispatch contract |
|---|---|---|
| Brainstorm omitted models, three personas | default:architect,default:refactorer,default:qa | Generation and each advocate omit model, including retries; coordinator/merge independently omit model |
| Brainstorm explicit sonnet,haiku at deep depth | sonnet:architect,haiku:refactorer,sonnet:qa | Preserve the order; pass explicit aliases to generation and advocacy, not coordinator/merge |
| Mixed default:qa,sonnet:architect | default then sonnet; personas/instructions retained | First omits model; second passes sonnet; no promotion during debate or retry |
| Direct compare, two files, no agents | default per input file | Two advocates omit model; parent session choice is not substituted |
| Cli-eval create omitted agents | default,default,default | Three designs and advocates, not one design; Mode A receives the same resolved list for three files |
| Cli-eval create explicit sonnet:architect,haiku:qa | List forwarded unchanged to Mode B, or Mode A with two matching files | Both explicit aliases retained; count mismatch in Mode A rejects before dispatch |

In tier mode each omission reaches Task 1's child environment binding: workspace ANTHROPIC_MODEL, else saved user model, validated through role policy and its fallback before parent-only overrides. A deliberate child setting and administrative force retain their established semantics. Every explicit resolved destination remains subject to the shim guard. Outside tier mode native behavior is unchanged. An alias or default marker is never backend proof; observed backend is unknown unless runtime evidence exists.

## Contract coverage and scope
Changed the named advocate dispatch, Mode A optional-agent parsing/assignment, coordinator/merge descriptions, merge dispatch, requested-selection provenance and default-label blind handling. Tests independently slice those sections, the shared instantiation reference, command arguments/options and cli-eval input/W3/help/integration. Mode B generation's existing conditional rule and retry wording remain covered by Task 3 assertions. Repeated defaults retain variant number/persona and original output layout; blind copies remove selection metadata, not ordinary prose uses of 'default'. Contract keys are unchanged. No evaluation runner, suite schema, loader, existing suite, run-pipeline policy, debate scoring or merge validation was changed. No new coordinator/merge override flag was added.

Auggie branch retrieval returned BRANCH_NOT_FOUND for ironbelly/issue-462 (only master indexed); direct source Reads/Grep supplied current context. No remote branch publication was attempted. One command edit was refused by the freshness hook after the long pause; the command was re-read and the identical surgical edit then succeeded.

## Observed checks and limits
Observed pre-review command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/skills/test_native_model_defaults.py tests/skills/test_brainstorm_protocol.py tests/commands/test_auggie_review_revagent.py -q. Exit 0, 31 passed in 0.12s; full output in task4-tests-initial.log. Scoped ruff: All checks passed! git diff --check: empty. No initial failures in this task. These static protocol checks do not prove live LLM compliance, a served backend, or historical cause. No model experiment was run. Typecheck is not applicable to prose; previously unavailable mypy was not installed.
