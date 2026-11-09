# Task 3 specification round-trip evidence

Governing structure: Task 3 Outputs and Acceptance criteria, expected input, parsed selection and native-argument outcome per trace vector.

## Evidence boundary

Manual traces below apply the live prose contracts in the builder's Model-Rotation, Serialization and Validation sections and adversarial's shared Parsing Rules and Mode B generation. They are expected protocol outcomes, not execution of a parser or a live native dispatch. The tests inspect source contracts only; no second parser implementation or paid model experiment was created. Requested aliases/markers are not served-backend or permission evidence.

## Trace vectors

| Expected input | Parsed selection/persona/instruction | Expected native argument |
|---|---|---|
| `default` | default / absent / absent | model omitted |
| `default:architect` | default / architect / absent | model omitted |
| `default:qa:'check edges'` | default / qa / check edges | model omitted |
| `default:qa,sonnet:architect,haiku` | ordered default, sonnet, haiku with qa, architect, absent personas | omit, sonnet, haiku respectively |
| `default:qa,default:qa` | two preserved identical specs; duplicate INFO only | omit for both |
| `default:qa:'don\'t split: commas, either'` | default / qa / don't split: commas, either | model omitted; punctuation remains instruction data |
| `sonnet:qa:"say \"yes\": then, check"` | sonnet / qa / say "yes": then, check | model=sonnet; legacy double quotes accepted |
| `default:qa:'keep \\ path'` | default / qa / keep one backslash then space then path | model omitted; decode once |
| `opus:architect,fable:qa` | explicit opus and fable with personas | model=opus then model=fable, subject to actual role check |
| empty entry, `default,,sonnet` | reject empty agent | STOP before dispatch |
| `default::'text'`, `default:qa:'x':extra` | reject empty/extra field | STOP before dispatch |
| `default:qa:'unclosed`, trailing backslash in a quoted field, `default:qa:'x'junk` | reject unmatched quote, dangling escape, trailing text | STOP before dispatch |
| `inherit`, full backend ID, arbitrary gateway alias | unsupported selection | STOP before dispatch |

Serialized strings are never shell-executed. Quotes delimit only the instruction field. Matching quote/backslash escapes decode once; other backslashes and the other quote character stay data. Sanitized interpolation cannot create commas, colons, quotes or control characters. The marker is interpreted only in the first field.

## Counts and preservation

Manual assignment traces, with all model choices kept separate from persona selection:

- Code quick, proposals=2, omitted models: default:architect,default:refactorer. Existing proposals=2 rule omits generated custom instructions.
- Code standard, proposals=3, omitted models: default:architect,default:refactorer,default:qa, with the existing per-persona templates.
- Incident deep, proposals=5, omitted models: default:analyzer,default:devops,default:qa,default:architect,default:backend, with templates unchanged.
- Code deep, proposals=5, explicit --models sonnet,haiku: sonnet:architect,haiku:refactorer,sonnet:qa,haiku:backend,sonnet:frontend. No first-two promotion.
- Code deep, proposals=3, explicit --models default,opus: default:architect,opus:refactorer,default:qa.
- Quick caps at 2, standard at 5, deep at 7. Adversarial still requires 2-10 agents. Auto-excluded security stays excluded unless explicitly requested; priority ordering, backfill, truncation and instruction parameter stripping remain intact.

The single `default` vector describes parsing, not a valid one-agent adversarial run: the unchanged minimum count rejects that run.

## Observed static checks

Command: PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest tests/skills/test_brainstorm_protocol.py tests/skills/test_native_model_defaults.py -q

Initial outcome: 1 failed, 10 passed in 0.08s. The builder's validation described single quotes and compatible double quotes separately, while the shared contract test required the explicit phrase 'single or double quotes'. Its split rule was clarified to name both matching delimiters directly.

Rerun observed exit 0: 11 passed in 0.07s. Scoped ruff check: All checks passed! git diff --check: no output. These are pre-review static checks; not parser execution or live dispatch.

After the independent review, corrected the command's three stale implicit-rotation claims and made its blind multi-model example explicitly request sonnet,haiku. Added section-scoped builder/producer escaping assertions, default-marker examples and command boundary checks. Observed focused rerun: 14 passed in 0.13s, scoped ruff All checks passed!, git diff --check empty. The plugin command mirror remains reserved for Task 5. No executable parser or live dispatch was run.

On 2026-11-09 the user explicitly instructed: "Override the review requirement and move on with those fixes in place." Applied the remaining consumer parse/validate regression as a test-only correction. Observed 15 passed in 0.07s; scoped ruff passed; git diff --check clean. The user override ends this task's pending adviser/revert and re-review requirement, including its ordinary ruling-eligibility restriction. No adviser, revert or additional Task 3 review was performed. The earlier missing verdict remains recorded unchanged as user-accepted, not upgraded to independently compliant. Later tasks and the final verification retain their existing checks.
