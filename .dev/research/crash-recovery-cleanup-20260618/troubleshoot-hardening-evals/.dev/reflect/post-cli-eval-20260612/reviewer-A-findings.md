# Reviewer A — Correctness + Schema Fidelity findings

Commit under review: HEAD `09f7d487` (feat(cli-eval): /sc:cli-eval skill for eval-suite create + run lifecycle).
Lens: verify every factual claim the skill/refs/agents/templates make about the `superclaude eval` CLI
against the real source, and verify the 3 new suites are valid + meaningful.

Ground-truth verification performed (all green / as cited):

- `uv run superclaude eval describe --suite {eval_cli_doc_parity,cli_eval_skill_contract,suite_schema_guard}` → **exit 0** for all three (loader accepts them).
- `uv run superclaude eval run --help` → enumerates exactly the **twelve** flags the suites/skill claim: `--suite [required], --parallel, --eval, --no-mcp, --no-pty, --output-dir, --keep-home, --timeout-mult, --max-disk-mb, --json, --verbose, --junit`. Docstring literally says "the twelve FR-CLI1 flags."
- `eval list --json` → array of `{name,version,eval_count}`; a suite named `real` is present (SG1's assertion is grounded).
- `--no-pty` skip path: commands.py:1894-1902 → `if no_pty and spec.no_pty == "skip"` emits SKIPPED + `skip_reason="--no-pty"` + `skip_flag_triggered="--no-pty"`. Skill claim exact.
- FR-G5: `coverage_gate` IS invoked in `eval run` (commands.py:1822) before dispatch; `COVERAGE_GATE_FAILED_EXIT_CODE = USAGE_ERROR = 2` (coverage.py:78); missing/empty settings.json → empty matcher set → passes (coverage.py docstring + body). Empty-HOME workaround is mechanically correct.
- Exit-code map: `exit_codes.py` SUCCESS=0/FAILURES=1/USAGE_ERROR=2/INTERRUPTED=3; `RUN_CLEAN_EXIT_CODE=SUCCESS` covers "PASS/SKIPPED/XFAIL" → all-SKIPPED run exits 0 (skill claim exact).
- summary.json keys: run_report.py / models.py `_RUN_SUMMARY_FIELDS` + `_EVAL_OUTCOME_FIELDS` + `RunCounts`/`RunTotals` fields — every `{{...}}` in run-report.md template maps to a real key (see A4).
- `expect_tool_call` inside `inputs[]` is a REAL parsed key (coverage.py:244), used by real.yaml/installer_sync_drift.yaml — not fabricated.
- house-style `expects` shape (`{stdout:{contains:}}`, `{exit_code:{equals:}}`, `{stdout:{not_contains:}}`) matches eval_smoke.yaml verbatim.

---

## Findings

### A1 — MED — Meaningfulness: the 3 new suites' `expects` assertions are never evaluated by the current harness (null executor, no expects resolver)

- **file:line**: suites `eval_cli_doc_parity.yaml:71-81`, `cli_eval_skill_contract.yaml:66-95`, `suite_schema_guard.yaml:68-95` (every `expects:` block) vs ground truth `src/superclaude/cli/eval/commands.py:1431-1434` and `:1357-1383` (`_NullLifecycleExecutor`).
- **claim_vs_truth**: The suites assert rich, meaningful things (`stdout contains "--no-pty"`, `[required]`, `CLI_EVAL_WIRED`, `not_contains "MISSING:"`, `"name": "real"`). But the harness today wires **an empty `expect_callables` tuple** and the executor is `_NullLifecycleExecutor`, which returns `ObservedRun(exit_code=0, stdout="")`. commands.py:1431-1434 states verbatim: *"The expects resolver (manifest `expects:` row → callable) lands in a follow-up; for now every spec that survives the `--no-pty` short-circuit returns PASS via the null executor."* So at this milestone the suites can only ever produce: (a) all-SKIPPED (run with `--no-pty`), or (b) a canned PASS that checks **none** of the `expects` (run without `--no-pty`, stdout is `""`, exit 0 hard-coded). The assertions are dormant contracts, not live gates.
- **is_real**: TRUE that the assertions are not currently executed. NOT a defect in the suites themselves — they are authored as forward-looking contracts that will fire when the M5/M6 PTY executor + expects-resolver land, and they ARE schema-valid (`eval describe` exit 0). The skill's RUN pipeline is also explicit and honest that a stubbed-executor PASS must be labeled NON-AUTHORITATIVE. Severity MED only because a reader could over-read "3 suites authored + run in parallel" (commit msg) as "3 meaningful gates now enforcing" when today they enforce nothing executably. This is a scope/maturity caveat, not a contradiction with source.
- **suggested_fix**: Add one sentence to each suite's header comment (and/or the create-pipeline ref) noting the `expects` are inert until the production executor + expects-resolver land (cite commands.py:1431-1434), so a future operator doesn't mistake a green plumbing run for an enforced contract. No code change.

### A2 — LOW — `eval run --help` default-output-dir text disagrees with the real default (CLI doc bug the skill does NOT inherit, and the new doc-parity suite does NOT catch)

- **file:line**: `src/superclaude/cli/eval/commands.py:1603` (help text `"Defaults to .dev/eval-runs/<run-id>/"`) vs `commands.py:1331-1339` `_default_output_dir` → `compose_run_dir(Path.cwd(), ...)` → `artifact_layout.py:179` `<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` (WITH date segment).
- **claim_vs_truth**: The CLI's own `--help` advertises a default path **without** the `<YYYY-MM-DD>` date segment; the actual code produces one **with** it. The skill/refs (eval-contracts.md:32, run-report agent, artifact_layout) correctly state the dated form — so the skill is RIGHT and the CLI `--help` is the thing that's stale.
- **is_real**: TRUE as a CLI documentation bug. It is NOT a skill defect (skill matches code). Worth flagging because the just-authored `eval_cli_doc_parity` suite's whole purpose is doc⇆CLI flag parity, yet it only checks flag long-name presence, not help-text *content* accuracy, so it would not catch this real drift in the same `--help` block it inspects.
- **suggested_fix**: (a) Fix commands.py:1603 help to `Defaults to .dev/eval-runs/<YYYY-MM-DD>/<run-id>/`. Out of scope for this skill commit but should be filed. (b) Optionally note in eval_cli_doc_parity's header that it guards flag *names*, not help-text *values*.

### A3 — LOW — `templates/suite-manifest.yaml` `$schema` uses a needlessly indirect path that doesn't match house style and is fragile under the copy instruction

- **file:line**: `src/superclaude/skills/sc-cli-eval-protocol/templates/suite-manifest.yaml:1` (`# yaml-language-server: $schema=../../../cli/eval/suites/suite.schema.json`) + line 3 comment ("copy into src/superclaude/cli/eval/suites/<stem>.yaml") vs every shipped suite e.g. `eval_smoke.yaml:1` (`$schema=./suite.schema.json`).
- **claim_vs_truth**: The template tells the author to copy the file verbatim into `cli/eval/suites/`. Every real suite in that directory uses the simple sibling form `./suite.schema.json`. The template instead ships `../../../cli/eval/suites/suite.schema.json`. Verified both resolutions: from the template's own location it resolves correctly, and (by self-referential coincidence) from `cli/eval/suites/` it ALSO resolves to the right file — so it is not broken, but if copied verbatim the author lands a non-idiomatic 3-level path instead of `./suite.schema.json`. The `$schema` directive is editor-only (yaml-language-server); the loader uses `loader.SCHEMA_PATH`, so this never affects validation either way.
- **is_real**: TRUE as a house-style / template-hygiene mismatch; not a correctness defect (validation unaffected; path resolves in both locations).
- **suggested_fix**: Change template line 1 to `# yaml-language-server: $schema=./suite.schema.json` to match every shipped suite and the eval-suite-author "house style" instruction. (Note: the eval-suite-author agent authors into `cli/eval/suites/` directly, where `./` is correct, so this also de-risks an author copying the wrong form.)

### A4 — LOW — run-report.md template uses `expanded_n′` / `n_prime` shorthand and bundles XFAIL/XPASS implicitly; all `{{}}` keys map to real summary.json keys, but two derived rows aren't first-class keys

- **file:line**: `templates/run-report.md:22-26` (`{{counts.manifest_n}}`, `{{counts.expanded_n_prime}}`, `{{totals.passed|failed|errored|skipped|timeout|interrupted}}`, `{{parallel}}`, `{{duration_sec}}`) vs `models.py:732-738` `_RUN_COUNTS_FIELDS`, `:784-791` `_RUN_TOTALS_FIELDS`, `:820-832` `_RUN_SUMMARY_FIELDS`.
- **claim_vs_truth**: Every templated field name resolves to a real key: `counts.{manifest_n,expanded_n_prime,kept_k,skipped_s,kept_plus_skipped_equals_n_prime}`, `totals.{passed,failed,skipped,errored,interrupted,timeout}`, top-level `{parallel,duration_sec,suite,run_id,...}`, per-eval `{eval_id,title,status,duration_sec,skip_reason,skip_flag_triggered,artifacts,error_class}`. No fabricated key. One nuance: the template's per-eval column "preserved HOME (forensics)" is sourced from `artifacts{}` — correct (models.py:344, the HOME path lives in the per-eval `artifacts` map per the agent contract), but it is not a dedicated key, so a renderer must know to pull the HOME entry out of `artifacts{}`. XFAIL/XPASS have no template row (they roll into passed/failed per `PASSED_STATUSES`/`FAILED_STATUSES`, models.py:70-71) — acceptable but the Surfaced-issues line (`:42`) does list XPASS, so there's no contradiction.
- **is_real**: Borderline / essentially clean. All keys are real; the only "gap" is that two values (HOME path, XPASS surfacing) are derived rather than direct keys, which the reporter agent's contract already explains. Logged at LOW for completeness, not as a true defect.
- **suggested_fix**: None required. Optionally add a one-line note in run-report.md that the forensic HOME is the per-eval `artifacts{}` entry (the agent already knows this), to harden against a naive renderer.

---

## Category sign-off (explicit "found nothing real" where applicable)

- **CLI flag / subcommand / exit-code / schema-field / status-enum / artifact-path claims**: No HIGH disagreements. Every subcommand (`doctor/list/describe/run`), the 12 `eval run` flags, the 4-value exit map (0/1/2/3), the 8-status enum, the FR-G5 exit-2 gate, the `--no-pty`→SKIPPED contract, the run-dir layout (with date segment), and the summary.json key set were verified against source and **agree** with the skill/refs/agents. The only doc-vs-code drift found (A2) is in the CLI's own `--help`, where the skill is correct and the CLI is stale.
- **3 suites (schema-invalid / unpassable assertion / stem≠name / wrong isolation / asserts nothing / dangling ref)**: All three load (`eval describe` exit 0). stem == `name:` for all three (`eval_cli_doc_parity`, `cli_eval_skill_contract`, `suite_schema_guard`). Isolation choices are defensible and documented: `ephemeral` for help/list/describe evals (no HOME/tree dependency), `shared` for the skill-contract evals that grep the working tree (mirrors installer_sync_drift precedent — correct). No referenced flag/suite is missing (`real` exists; all 12 flags exist; `eval_cli_doc_parity` self-reference in SG2 exists). The only meaningfulness caveat is A1 (assertions dormant under the current null executor) — real but a maturity caveat, not an invalid/unpassable assertion.
- **suite-manifest.yaml `$schema` path**: A3 (LOW) — resolves but non-idiomatic / fragile vs house style.
- **run-report.md `{{}}` field names**: A4 — all map to real summary.json keys; effectively clean.

**No HIGH-severity defect found after independent re-testing.** The dig surfaced one real maturity caveat (A1, MED) and three LOW hygiene/doc items (A2 CLI-side, A3 template, A4 template-note). The skill's factual claims about the `eval` CLI are accurate to source.
