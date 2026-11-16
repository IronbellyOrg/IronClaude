e662bf76fc89672773eaf9882410f9c676925370
family=orca-outage-line
defect form: a sentence about the Orca outage that claims more than orca_available false proves (it says the counts come from disk sources only, but Orca calls made before the drop were read).
command: grep -n -E -e 'disk sources only' -- src/superclaude/skills/sc-sweep-protocol/SKILL.md tests/commands/test_sweep_command.py .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command-summary.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command.txt
before-output:
src/superclaude/skills/sc-sweep-protocol/SKILL.md:26: ... In the ordinary reply, when `orca_available` is false, also print the one line `Orca was unavailable; the counts come from disk sources only.` ...
tests/commands/test_sweep_command.py:528: "`Orca was unavailable; the counts come from disk sources only.`"
coupled sites: the SKILL.md step 4 sentence, _OUTAGE_SENTENCE in tests/commands/test_sweep_command.py (:526-529), the pins that quote it, and the fix log FIN-F7 block (:68).

family=yaml-safe-load-exceptions
defect form: a safe_load wrapper that catches yaml.YAMLError (and RecursionError) but lets another exception class that yaml.safe_load can raise (ValueError from a scalar constructor) escape.
command: grep -n -E -e 'yaml\.YAMLError|RecursionError' -- src/superclaude/cli/sweep/probes.py tests/sweep/test_probes_allowlist.py
before-output:
src/superclaude/cli/sweep/probes.py:681:    except (yaml.YAMLError, RecursionError):
coupled sites: the _yaml_top docstring (:673-678), the case list of test_contract_fields_are_read_by_yaml_safe_load (tests/sweep/test_probes_allowlist.py:1769), and the fix log FIN-F9 block (:83-86).

family=stale-result-map
defect form: a result file's case-to-test map that still names a test this task renamed.
command: grep -n -E -e 'test_every_class_name_is_reached|test_rule_5_needs_all_four_conditions' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-classify.txt .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-report.txt .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-probes-allowlist.txt .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-cli-contract.txt .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command.txt .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command-summary.md tests/sweep/test_classify.py
before-output:
.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-classify.txt:190: 2. Every name in CLASSES is reached: test_every_class_name_is_reached
.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-classify.txt:193: 5. Rule 5 four-condition case (SP-24): test_rule_5_needs_all_four_conditions
coupled sites: the other renamed or added tests of this cycle named in the fix log (test_next_inspection_waiting_signal_and_fallback_fit_every_outcome, test_sessions_safe_to_close_cell_carries_its_reason, test_orca_dropping_mid_run_is_not_reported_as_nothing_read, test_settled_orca_row_without_a_contract_names_the_missing_contract, test_a_changed_contract_is_re_read_only_while_the_budget_allows, test_contract_fields_are_read_by_yaml_safe_load): the result files' case maps may not list them.

after (appended after the repair pass):
orca-outage-line: grep -n -E -e 'disk sources only' over the same files returns no match; the new sentence is at SKILL.md:26 and tests/commands/test_sweep_command.py:528.
yaml-safe-load-exceptions: probes.py:682 now lists (yaml.YAMLError, RecursionError, ValueError); tests/sweep/test_probes_allowlist.py holds the rejected-date-scalar case.
stale-result-map: grep -n -E -e 'test_every_class_name_is_reached|test_rule_5_needs_all_four_conditions' over the result files and tests/sweep/test_classify.py returns no match.
