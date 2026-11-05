# Pipeline Hardening Closure (Wave 4.5)

## HC0 — Applicability + boundary scan
| boundary_type | producer / transformers / consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|
| CLI/subprocess | session -> `uv lock` -> PEP 517 backend named by pyproject.toml | probe-lock-trust.out:6 | the subprocess executes code chosen by untrusted input | applicable | the defect is unvalidated input to a code-executing subprocess |
| gate-status-enum | lock_trust_findings -> step 5 -> `sync_tier3` halt | refs/conflict-mechanical.md step 5, halt table | a gate that passes a dangerous input, or misroutes the halt | applicable | the fix adds a HALT decision |
| file-stdin-prompt | work-tree pyproject.toml -> the session's Read -> lock_trust_findings | refs/conflict-mechanical.md step 5 | the gate could read a different file than `uv lock` reads | applicable | the gate must read the same file uv reads |

pipeline_hardening_applicable: true
Mechanism statement: a mechanical regeneration step treated a tracked manifest as trusted data although the tool it feeds executes code the manifest names; the gate must inspect the same bytes the tool consumes and fail closed when it cannot.
known_escapes_caught: []

## HC1 — Runtime-entrypoint verification: N/A
Rationale: the production boundary is the attended session following step 5; the hermetic tests exercise the core function and pin the step 5 text and order (test_step5_lock_trust_gate_runs_between_the_precheck_and_uv_lock), with a negative witness (red-run.out), but no live session replay of a conflicting PR exists in this run. Live verification is a listed post-release follow-up.

## HC2 — Contract enumeration: PASS
| producer | consumer | contract | status |
|---|---|---|---|
| lock_trust_findings() | refs/conflict-mechanical.md step 5 | ordered list of field names; `pyproject.toml unreadable` when unverifiable | new; unit tests per trigger, clean, malformed, no parser, 3.10 |
| step 5 gate | halt table row `sync_tier3` | abort + Tier 3 message naming the findings | row updated |
| trust limit | refs section 6, SKILL.md Will Not Do, commands/pr-submit.md | documented residual risk | pinned by test_trust_limit_is_documented_in_the_refs_skill_and_command |
contract_ledger_path: this file, section HC2

## HC3 — Unmask and sweep: N/A
Rationale: the gate parses TOML with the stdlib parser and compares keys structurally; no substring or regex classifier controls the decision.

## HC4 — Effective-input proof: N/A
Rationale: no review/audit selector chooses the input; the gate reads one fixed path, the file `uv lock` reads.

## HC5 — Off-path review
off_path_review_decision: performed (independent troubleshoot-analyst self-review lens over the full fix diff; result recorded in audit.log)

## Verdict
waiver_status: none; HC1, HC3, HC4 N/A with rationale, no FAIL -> pipeline_hardening_verdict: advisory (row 6). backtest_status: not_run.
