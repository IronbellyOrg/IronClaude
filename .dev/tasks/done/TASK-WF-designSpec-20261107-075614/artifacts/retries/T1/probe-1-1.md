69f360d58d89456f559ad3de21ea75027cd72bb0
family o3-pin-completeness
defect form: the O3 list in the gate record omits tests that pin exact SKILL.md or refs text, and describes two test files as pinning only a python fence and the event count.
command: grep -n -E -e "test_skill_states_the_a5_rules|test_protocol_refs_pin_live_boundaries_and_existing_gates|test_spec_byte_identical_fragments_survive|test_ec16_base_branch_halt_documented|test_impact_command" -- .dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/pre-build-gate.md
before: (no output; exit 1)
coupled sites: the bullet "tests/pr_submit/test_cosmos_protocol.py and test_codex_reviews.py: one python fence in SKILL.md; the len(EventType) pin (Task 2)" in section 3 O3 of the same file (states the false claim); the lead sentence of section 3 O3 ("pins and line-content rules the additive edits must respect").
after:
  57:- `tests/pr_submit/test_codex_reviews.py`: `test_skill_states_the_a5_rules` pins these exact `SKILL.md` fra
  58:- `tests/pr_submit/test_cosmos_protocol.py`: `test_protocol_refs_pin_live_boundaries_and_existing_gates` pi
  59:- `tests/pr_submit/test_conflict_sync_protocol.py`: `test_spec_byte_identical_fragments_survive` pins, in `
  60:- Other readers of the pr-submit files, satisfied by additive edits that leave existing text unchanged: `te
