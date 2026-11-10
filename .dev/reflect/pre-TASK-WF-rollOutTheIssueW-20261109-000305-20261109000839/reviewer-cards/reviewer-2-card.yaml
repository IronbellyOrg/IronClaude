reviewer: reviewer-2
model_class: haiku
persona: qa
agent_type: reflect-reviewer
brief: reviewer-briefs/reviewer-2.md
mode: pre
findings:
  - id: F2
    severity: medium
    deviation_class: plan-gap
    claim: "T1 F2 confirmed as a validation gap (not an actual leak): captured replies land in the always-staged package, but the only token grep scans tests/issue_watch/fixtures/."
    evidence:
      - "plan:29 redacted copies saved as `./artifacts/captured/<fixture name>` in this package"
      - "plan:118 grep -r -E \"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_\" tests/issue_watch/fixtures/"
    recommendation: "Require owner redaction before files enter the package and run the secret/private-identifier check over ./artifacts/captured/ as well as the fixtures; keep staging task artifacts."
  - id: QA-02
    severity: high
    deviation_class: plan-gap
    claim: "Plan weakens 'replace every guessed fixture' to 'replace whichever were captured'; Task 5 precondition (one capture per fixture, plan:108) contradicts its body (missing captures allowed, plan:110); coverage matrix row 14 overstates coverage."
    evidence:
      - "source.md:22 replaces every guessed `_assumed_shape` fixture with captured output"
      - "plan:110 A fixture with no captured file stays as it is, with `\"_assumed_shape\": true`"
      - "artifacts/coverage-matrix.md:14"
    recommendation: "Partial captures may be recorded, but FU-1 stays blocked until every fixture is replaced unless the owner approves a revised gate; record the every-fixture obligation separately in the matrix."
  - id: QA-03
    severity: medium
    deviation_class: plan-gap
    claim: "Task 5 says replace `payload` with parsed stdout JSON, but the include-response fixture stores status line, headers and body in `raw`, which the test consumes; following the plan literally leaves the tested data unchanged."
    evidence:
      - "plan:110 replace the `payload` value with the captured reply (stdout JSON parsed, or the stderr text ...)"
      - "tests/issue_watch/test_github.py:563 runner = fake_runner({G1_ARGV: result(stdout=fixture[\"raw\"], argv=G1_ARGV)})"
      - "tests/issue_watch/fixtures/_assumed_shape/gh_api_user_include.json:4 raw envelope"
    recommendation: "Name each fixture's capture stream and destination field (raw, payload, stderr, exit status) and verify the field the test consumes holds the sanitized capture."
  - id: QA-04
    severity: medium
    deviation_class: plan-gap
    claim: "A fixture-consuming test hardcodes the guessed Date header timestamp; a real capture fails it even when the shape parses. Task 5 only budgets the metadata-test change."
    evidence:
      - "tests/issue_watch/test_github.py:566-567 assert read.value == Login(\"owner-login\", 1001, datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone.utc)"
      - "plan:112 change `test_every_assumed_shape_fixture_parses_and_is_labelled`"
    recommendation: "Allow fixture-dependent expected-value updates in the permitted test file, kept distinct from parser-shape changes."
confirmed_t1: [F2]
note: "plan = .dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/TASK-WF-rollOutTheIssueW-20261109-000305.md"
self_reported_confidence: 0.95
calibrated_confidence: 0.72
calibration_ref: artifacts/reviewer-2-calibration.yaml
