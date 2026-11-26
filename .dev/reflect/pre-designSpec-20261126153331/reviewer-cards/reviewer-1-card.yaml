reviewer: analyzer (root-cause and evidence)
model_class: sonnet
findings:
  - id: F-1
    grade: Blocking
    blocking_reason: Missing
    claim: 'The spec says "A person also reads the six definitions once before the freeze." No task, README step or procedure carries it. Task 1''s cue-phrase test is automated and checks only the listed phrases. The README order of work goes straight to `gate.py freeze-corpus`, which hashes `questions.py` into the manifest and cannot be redone.'
    evidence: "source.md:142 (M-5 last sentence); plan lines 197-205 (README order of work) and 181-183 (Task 7) do not mention it. A grep of the package for 'six definitions' and 'definitions once' matched only source.md:142."
    consequence: "Add the human read of the six definitions as a README step before `freeze-corpus`, and a criterion in Task 8 that checks it. Without it the question wording is frozen with no human review."
  - id: F-2
    grade: Blocking
    blocking_reason: Decision
    claim: "The check for 'a twice-failed prompt scored not right' (T-06) does not say which label the prompt has. `right(label, answer)` treats answer `None` as unset, and an unset answer on an `ambiguous` or `none-fit` label is right. A wrong implementation that turns an `error` into answer `None` passes the test when the label is typed. It would score an errored ambiguous prompt as right for Jev, which changes the b and c counts."
    evidence: "plan lines 77-78 (`right`, `None` means unset), 127 (error counts as not right), 138 (T-06 criterion); source.md:75 and 82."
    consequence: "The criterion must require a twice-failed prompt with an `ambiguous` or `none-fit` label to be scored not right, and must say `score()` bypasses `right` for `error` rows."
  - id: F-3
    grade: Medium
    blocking_reason: null
    claim: "Confirms the first-pass F-1. `spend_bound` needs the prompt text, but the plan says gates 'never call the corpus loader' and gives no way to read the prompts. A test patches `load_corpus` to raise and expects both gates to still run. An implementer who calls `load_corpus` fails that test. One who skips the estimate leaves `spend_bound` unimplemented."
    evidence: "plan lines 106, 108 and 115."
    consequence: "Say that Gate 2 reads the corpus file as raw JSON lines, builds each request with `build_questions`, and passes them to `spend.estimate_run_tokens`. Say also how it reads the ledger without `Budget.__init__`, which creates and rewrites `spend.json` and its `.lock` file (budget.py:20-28)."
  - id: F-4
    grade: Medium
    blocking_reason: null
    claim: "Confirms the first-pass F-3 and F-5. `execute` writes `run_end` when `reserve_phase` refuses, and Gate 2 treats any `run_end` as `prior_run`, so a run that posted nothing uses up the go permanently. With `TYPESAFE_API_KEY` unset, the plan does not say what happens. Assigning `None` into `os.environ` raises TypeError. If the key is simply not copied, `KeyMissing` is raised after `first_request` is written (client.py:133-135), which also uses up the go. The design says a missing key in the coordinator's shell is a likely case."
    evidence: "plan lines 152, 156, 159; source.md:149; client.py:133-135."
    consequence: "Specify that a missing key exits non-zero before any event or run folder is written. Specify that a refusal before the first post leaves no `run_end`, or is excluded from `prior_run`."
  - id: F-5
    grade: Medium
    blocking_reason: null
    claim: "`sign_test_passes(b, c)` is specified to read the factor 20 from the rule's `alpha_inverse`, but its signature has no rule argument. Tests call it with two arguments. An implementer will most likely hardcode 20, which contradicts 'policy values live in the rule file' (source.md:113). The verdict boundary tests that use stand-in rule values then have nothing to vary."
    evidence: "plan lines 79, 85 and 137; source.md:113."
    consequence: "Give the function a rule or `alpha_inverse` parameter and make the tests pass it."
  - id: F-6
    grade: Medium
    blocking_reason: null
    claim: "'Answered' is never defined, so the T-08 test and the median cannot be pinned. Constraints say the median is over 'each prompt's final answered attempt', while Task 3 says 'the population `median_population` says'. Neither says whether an `invalid` 200 response counts as answered, or whether a prompt's earlier answered attempt counts."
    evidence: "plan lines 26 and 81; source.md:78."
    consequence: "Define an answered attempt as status `ok`, or as any HTTP response, and state whether the population is all answered attempts or the last one per prompt."
  - id: F-7
    grade: Medium
    blocking_reason: null
    claim: "The `exp` fixture is described as holding synthetic frozen files and a rule copy. `hash_code` and `record-tests` need code files and `jevlib` files under the temporary root, because `Paths.code_files()` is root-relative. The fixture does not say it supplies them, so tests of `hash_code` for 'any code file' have no inputs."
    evidence: "plan lines 59, 94, 105 and 112."
    consequence: "Add synthetic `questions.py`, harness modules and a `jevlib_dir` to the fixture description."
  - id: F-8
    grade: Note
    blocking_reason: null
    claim: "Three smaller points. (a) The '31 importers' claim does not match a grep, which finds about 25 files mentioning `jevlib` outside its own package. (b) The `model_mismatch` check over 'models returned by `ok` rows' cannot fail, because `validate_response` already rejects any other model, so only the `run_end` reason can trigger it. (c) `load_rule` does not say it converts values to numbers. Values such as `attempt_timeout_s` would stay strings and break `min(C.ATTEMPT_TIMEOUT_S, ...)` at client.py:158."
    evidence: "plan lines 129 and 173; validate.py:32-33; client.py:158."
    consequence: "Fix the count, drop the `ok` rows check, and state the number types."
coverage_assessment: "Of the nine unmatched items, only the human read of the six definitions (M-5) lacks a task. INF-001, 002, 003, 005, 006, 014, 018, 021 and 027 are covered by the Constraints or Tasks 3, 4 and 6. INF-018 is covered only by the weak check in F-2."
checked_and_found_clean:
  - "The `ask` order, the `dry_run` refusal before any transport call, and `model` being `None` on non-`ok` results (client.py:128-131, 86-91)."
  - "`MAX_RETRIES` and `ATTEMPT_TIMEOUT_S` are read at call time with defaults 1 and 20.0 (client.py:158, 192; config.py:15-17)."
  - "`estimate_request_tokens` matches the client's formula (client.py:100). `reserve_phase`, `release_phase` and the phase-bound `draw` behave as the plan says (budget.py:63-100). The token ceiling binds at a higher price."
  - "Only `KeyMissing` and `KeyRejected` are raised. `budget_exhausted`, `model_mismatch` and `dry_run` come back as results."
  - "The privacy patterns and the `JEV_API_KEY` env read sit only in `load_corpus`; `redact` and `Journal` handle the key."
  - "Sign test cases 5-0, 4-0, 7-1, 6-1, 8-2, 9-2 and (0,0), and the smallest passing b for c = 0 to 6 (5, 7, 9, 10, 12, 13, 15), recomputed by hand and correct."
  - "The table rows are at SKILL.md lines 153-159. `keyscan.py --fake` takes explicit paths."
recommendations:
  - file: .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md
    change: "Fix F-1 to F-7 in Tasks 3, 4, 5, 6 and 8 as described above."
    verifier: "Grep the plan for a human read of the six definitions before `freeze-corpus`. Grep for a T-06 case with an `ambiguous` label and `error` status. Grep for the Gate 2 prompt source, an `alpha_inverse` parameter, and the definition of 'answered'."
