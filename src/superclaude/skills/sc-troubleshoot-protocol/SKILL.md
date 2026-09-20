---
name: sc:troubleshoot-protocol
description: "Tiered debugging protocol — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate in Tier 2, and an opt-in task-builder remediation chain in Tier 3. Use this skill whenever the user reports a broken build, runtime error, performance regression, deployment problem, or failing test, even when they don't explicitly say 'troubleshoot' — phrases like 'why is X broken', 'this used to work', 'something's off with...', a pasted stack trace, or a failing-command transcript should all activate it."
allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__tavily__tavily_search, mcp__sequential-thinking__sequentialthinking
---

<!-- Extended metadata (for documentation, not parsed):
category: utility
complexity: advanced
mcp-servers: [auggie, serena, context7, tavily, sequential]
personas: [analyzer, performance, security, qa, refactorer, devops]
-->

# Troubleshoot Protocol

## Purpose

Diagnose a reported issue with the smallest amount of work that produces a high-confidence answer. The protocol is deliberately tiered so that small bugs stay cheap and only complex ones unlock the parallel + adversarial machinery.

**Core contract — quick first, deep when needed.** Tier 1 is intended to feel close to "just look at it" — a single grounded hypothesis returned in roughly 1-2 minutes. Tier 2 is the escape valve for cases where the symptom is ambiguous, spans multiple domains, or where one hypothesis is not enough. Tier 3 closes the loop by turning the chosen fix into an executable task. The user never has to know upfront which tier is needed; the rubric in `refs/escalation-rubric.md` decides.

**Why this works.** Most reported bugs cluster around a small set of common causes: missing imports, off-by-one, stale state, type mismatches, N+1 queries, environment drift. A single experienced agent grounded in real code finds these quickly. The hard cases — flaky tests, regressions after refactors, multi-system performance issues, security findings — benefit from multiple independent hypotheses generated in parallel and then *debated*, because the "obvious" cause is often a red herring and the cost of being wrong is much higher than the cost of fanning out.

**Hallucination contract.** Every claim in the final report must cite a real `file:line` or a real diagnostic command and its output. Findings that cannot be grounded are dropped, not downgraded. A diagnosis built on invented line numbers is worse than no diagnosis at all.

## Required Input (STOP if missing)

The skill receives at least one of:

- An **issue description** (free text, error message, stack trace, log excerpt)
- A **`--scope`** (file, directory, or symbol) paired with at least a brief description

**STOP** if neither is present — without a symptom and a scope the skill has nothing to triage.

**STOP** if `--depth deep` is requested but the issue description is under 10 words and no scope was given — too vague for a deep pass to add value; ask the user to add detail first.

## Output Contract

The skill returns a structured dictionary on completion:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success`, `partial` (some findings dropped for grounding), `blocked` (a Wave 1.6 hard-stop that cannot proceed without an external action — `capability-verdict: blocked`, `blocked-on-authorization`, the 3-round cap, or an unobservable CI verdict (validator A8); the tasklist is still written and Wave 5 still renders), `failed` (the run itself errored) |
| `tier_reached` | int | 1, 2, or 3 |
| `report_path` | string | Absolute path to `REPORT.md` |
| `audit_log_path` | string | Absolute path to `audit.log` |
| `confidence` | float | 0.0-1.0, calibrated via `refs/escalation-rubric.md` |
| `escalation_reason` | string | If Tier 2 ran: which rubric condition triggered it (or `forced_by_depth_deep`) |
| `test_is_wrong` | bool | `true` when the diagnosis concludes the failing test is the bug (test asserts wrong behavior, stale invariant, or inverted policy claim) rather than the code under test. Set independent of tier. Asymmetric-cost flag — downstream automation MUST NOT auto-apply a fix to the code when this is `true`; the remediation target is the test file. |
| `test_file_path` | string \| null | When `test_is_wrong=true`, the **repo-relative** path of the test file that must be updated (e.g., `tests/api/test_foo.py`), resolved against the repo root containing `.git/`. `null` otherwise. The format is intentionally fixed to repo-relative so downstream automation can compare/join paths without ambiguity; if the report is consumed outside the repo, the consumer is responsible for joining against the repo root recorded in the audit log. |
| `behavior_is_documented` | bool | `true` when the diagnosis concludes the reported behavior is the documented behavior (i.e., a code change would regress the documented contract). Set independent of tier; mutually exclusive with `test_is_wrong=true`. Asymmetric-cost flag — downstream automation MUST NOT auto-apply a code fix when this is `true`; the remediation target is the spec/docs file(s), or a stakeholder-level discussion. Derived from the chosen hypothesis card's `consistency_with_docs=aligned` AND the Diagnosis section concluding the observed symptom IS the documented behavior. When the failing artifact is a test (Case B in the derivation rule), `test_is_wrong=true` is the correct flag and this flag stays false — the docs are not the bug. |
| `doc_context_card_path` | string \| null | When Wave 1.5 ran, the **repo-relative** path of the Documentation Context Card (e.g., `.dev/troubleshoot/bug-foo-20260522/doc-context.md`). `null` ONLY when `--no-doc-discovery` was set (the wave is skipped entirely). When the wave runs but produces no relevant docs across all three branches, the field still points to an empty card whose sections all read "None found" — distinguished downstream from the skip case via the hypothesis card's `consistency_with_docs=no_docs_found` value. Format is repo-relative, same convention as `test_file_path`. |
| `hypothesis_cards` | list[path] | Paths to per-agent hypothesis cards (Tier 2) |
| `adversarial_artifacts_dir` | string | `sc:adversarial` artifacts dir (Tier 2 only, when 2+ fix proposals were debated) |
| `task_file_path` | string | MDTM task file path (Tier 3 only) |
| `remediation_offered` | bool | Whether Tier 3 was offered |
| `remediation_accepted` | bool | If offered, user's response |
| `diagnosability_verdict` | string | one of `sufficient`, `partial`, `insufficient`, `unknown` (default `unknown` when audit could not run — auggie + Grep fallback empty, failing_component not localizable, or `--no-diagnosability-audit` set; never silently skipped) |
| `diagnosability_context_card_path` | string \| null | repo-relative path to `<output-dir>/diagnosability-context.md`; `null` only when `--no-diagnosability-audit` was set or Wave 1.6 was not reached |
| `diagnosability_tasklist_path` | string \| null | repo-relative path to `<output-dir>/diagnosability-tasklist.md`; populated whenever the tasklist was emitted this run, including a later sufficient verdict, bypass followed by Wave 3 emission, or unknown verdict; `null` only when no tasklist exists for this run. Every creation/append path queues pending rows for Wave 5 Next Steps |
| `diagnosability_hard_stop` | bool | `true` when Wave 1.6 fired the hard-stop and skipped Waves 1.7–4.5; hard-stop still writes Wave 5; status is `partial` unless S1.6.4 precedence / 3-round cap / A8 contributes `blocked` (or `failed` wins) |
| `contract_version` | semver string | Output-contract semver, default `1.2.0`. Additive version stamp: `1.0.0` = Pipeline Hardening Closure fields (FR-13); `1.1.0` = TFEP adapter fields (`recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`); `1.2.0` = `execution_locus_card_path` plus the `status: blocked` and `pipeline_hardening_verdict: blocked-on-authorization` enum values; existing consumers reading only the prior fields are unaffected (NFR-6). Distinct from `target_release`. |
| `pipeline_hardening_applicable` | bool | `true` when Wave 4.5 HC0 classifies the issue as a pipeline escape / boundary change; default `false`. Set exactly once by HC0. |
| `pipeline_hardening_verdict` | enum `pass \| blocked \| advisory \| not_applicable \| blocked-on-authorization` | Deterministic aggregation of the HC0–HC5 statuses + `waiver_status` per `refs/hardening-output-contract.md` §5.4; default `not_applicable`. `blocked-on-authorization` is set only by the Wave 1.6 S1.6.4 status-precedence rule (an emitter row exists in the tasklist AND `re-run permitted: no`). Closed table for `re-run permitted`: `yes` = authorized same-shell/remote-command already granted this run; `no` = issue/flags/prior artifact explicitly refuse a re-run; otherwise `unknown`. `unknown` maps to pending rows and never sets `blocked-on-authorization`. Never AskUserQuestion. It bypasses the §5.4 aggregation, carries `status: blocked`, and the tasklist is still written. Once a waiver is latched the verdict is `blocked`/`advisory` and is never re-greened to `pass`/`success` by a downstream stage. |
| `waiver_status` | enum `none \| latched` | One-way latch; default `none`. `none`→`latched` only; once `latched`, `pipeline_hardening_verdict` ∈ {blocked, advisory}. |
| `backtest_status` | enum `not_run \| partial \| complete` | E1–E5 replay coverage state; default `not_run`. Production-facing pipeline-health signoff stays `advisory` until `complete`. |
| `off_path_review_decision` | enum `required \| performed \| waived_with_rationale \| not_required` | Wave 4.5 HC5 off-path-review decision; default `not_required`. |
| `runtime_entrypoint_card_path` | string \| null | Absolute path to the HC1 runtime-entrypoint card; `null` before HC1 runs. |
| `contract_ledger_path` | string \| null | Absolute path to the HC2 contract-enumeration ledger; `null` before HC2 runs. |
| `unmask_sweep_path` | string \| null | Absolute path to the HC3 unmask/sweep/classifier card; `null` before HC3 runs. |
| `effective_input_card_path` | string \| null | Absolute path to the HC4 effective-input manifest; `null` before HC4 runs. |
| `known_escapes_caught` | list | List of `{escape_id, wave, card_path, status}` objects; default `[]`. Membership requires a cited passing wave/card (`status=PASS`) per the anti-inflation rule. |
| `recommended_escalation` | enum `none\|retry\|escalate_depth\|halt` | TFEP adapter field (contract v1.1.0+). Forward-looking recommendation to the caller, synthesized from `status` + `tier_reached` + `confidence` + the Wave 5 Next Steps section. `none` = remediation ready; `retry` = re-run at same depth; `escalate_depth` = re-run deeper; `halt` = full stop. `status: blocked` always derives `halt` (a same-depth or deeper re-run cannot lift an external block) and, like `halt`, sets `tasklist_insertion_path: null`, `remediation_target: none`, `solution_summary: ""`. |
| `tasklist_insertion_path` | string \| null (abs path) | TFEP adapter field (contract v1.1.0+). Path to the adjudicated remediation-plan block the caller (task-protocol) should insert into its tasklist; null when no remediation is proposed (e.g. `recommended_escalation: halt`). Distinct from `task_file_path` (Tier-3 MDTM file) and `diagnosability_tasklist_path` (instrumentation tasklist). |
| `remediation_target` | enum `test\|code\|docs\|none` | TFEP adapter field (contract v1.1.0+). Which artifact the proposed remediation targets, composed from the asymmetric-cost gates: `test` when `test_is_wrong` is true (paired with `test_file_path`); `docs` when `behavior_is_documented` indicates a doc gap; `code` otherwise; `none` when `recommended_escalation: halt`. |
| `root_cause_summary` | string | TFEP adapter field (contract v1.1.0+). One-to-three sentence root-cause summary, extracted verbatim or condensed from the REPORT.md **Diagnosis** section (Wave 5). Empty string when diagnosis is inconclusive. |
| `solution_summary` | string | TFEP adapter field (contract v1.1.0+). One-to-three sentence proposed-solution summary, extracted from the REPORT.md **Proposed Fix** / **Next Steps** section (Wave 5). Empty string when no fix is proposed (e.g. `recommended_escalation: halt`). |
| `execution_locus_card_path` | string | Absolute path to `<output-dir>/execution-locus.md` (Wave 1 step 1b; re-derived every invocation). Contract v1.2.0+. |
| `verdict_source` | string \| null | Provenance of the failing-arm verdict (CI job-log marker line, non-CI artifact source/run, or `unobservable`). `null` when no verdict was read. |
| `return_contract_path` | string \| null | Absolute path to `<output-dir>/return-contract.yaml` when `caller=task-unified`; `null` otherwise. |

**`test_is_wrong` derivation rule** (applied during Wave 5 synthesis): set `test_is_wrong=true` when the chosen diagnosis names a test file (not production code) as the file requiring change, AND one of these conditions holds:

1. The test asserts an invariant that the cited spec / requirements doc explicitly contradicts (e.g., test claims policy rejects X but the policy doc allows X)
2. The test was authored before a feature change that legitimately altered the asserted behavior, and was not updated alongside the feature
3. The test mis-models the requirement (typo'd assertion, wrong fixture, wrong expected value)

If the diagnosis says "the test is incorrect but the code is also missing a guard" — surface BOTH in `Files to change` but keep `test_is_wrong=false` since the code is the load-bearing fix.

The prose REPORT.md is still the human-readable source of truth; this flag exists so downstream automation (Tier 3 task-builder, fleet auto-apply wrappers, telemetry) can short-circuit on the asymmetric-cost case without parsing prose.

**`behavior_is_documented` derivation rule** (applied during Wave 5 synthesis): set `behavior_is_documented=true` when the chosen hypothesis card's `consistency_with_docs=aligned` AND the Diagnosis section concludes the observed symptom IS the documented behavior (not the user's expected behavior). If the docs say the system should do X and the user reports it does X but expected Y, the bug is in the user's expectation (or the docs) — set the flag and recommend a spec change or stakeholder discussion. If `consistency_with_docs=conflicts`, the docs side with the user — keep the flag false and proceed with normal code remediation. Mutually exclusive with `test_is_wrong=true` by construction (not by tiebreaker), via this 3-case decomposition: **Case A** (user expectation diverges) — observed behavior matches docs AND failing artifact is NOT a test → `behavior_is_documented=true`, `test_is_wrong=false`; remediate via spec change or stakeholder discussion. **Case B** (test contradicts docs+code consensus) — `consistency_with_docs=aligned` AND failing artifact IS a test → `test_is_wrong=true`, `behavior_is_documented=false`; the docs are not the bug, remediate by updating the test to match the docs. **Case C** (code violates docs) — `consistency_with_docs=conflicts` → both flags false, normal code remediation.

This flag exists so downstream automation knows to NOT auto-apply a code fix when the observed behavior is the contracted behavior — the remediation target is the spec, the docs, or a stakeholder discussion.

## Wave Structure

```text
Wave 0: Parse + Validate Input
Wave 1: Tier 1 — Real-Code Grounding  ← always; loads refs/triage-checklist.md on demand (grounding + locus + reproduce only)
Wave 1.5: Documentation Grounding    ← always; loads refs/doc-discovery.md on demand; skipped only by --no-doc-discovery
Wave 1.6: Diagnosability Audit       ← always; loads refs/diagnosability-audit.md on demand; skipped only by --no-diagnosability-audit; may hard-stop to Wave 5
Wave 1.7: Tier 1 — Hypothesis Formation ← always; consumes Wave 1.5 Documentation Context Card; produces single hypothesis card + calibration
Wave 2: Confidence Gate              ← decides escalation via refs/escalation-rubric.md
Wave 3: Tier 2 — Parallel Hypotheses (conditional)
Wave 4: Tier 2 — Adversarial Fix Debate (conditional, requires ≥2 viable fixes)
Wave 4.5: Pipeline Hardening Closure ← conditional, when pipeline_hardening_applicable=true (issue topology); runs gates HC0-HC5; loads the 6 hardening refs
Wave 5: Synthesis + Report        ← always finalises; loads refs/report-template.md
                                    Wave 1.6 hard-stop edge: → Wave 5 (skip Waves 1.7–4.5; hardening does not run on diagnosability hard-stop); sets diagnosability_hard_stop=true and status=partial (or blocked per the S1.6.4 precedence rule)
Wave 6: Tier 3 — Remediation Chain (conditional, requires --fix + user accept)
```

Each wave has explicit entry/exit criteria. Refs are loaded per-wave, never pre-loaded.

---

### Wave 0: Parse + Validate Input

**Preconditions**: command invocation with at least an issue description or `--scope`.

**Steps**:

1. Parse flags. Required: issue description OR `--scope`. Optional: `--type`, `--depth`, `--fix`, `--no-escalate`, `--models`, `--output-dir`, `--no-mcp`, `--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds`, `--context`, `--caller`.
2. Auto-detect `--type` if not provided. Use keyword + structural cues from the issue description:
   - Stack trace, exception name, `undefined`/`null`/`NameError` → `bug`
   - "tsc", "ts(", "compiled", "lint", "build", `make`, CI log fragments → `build`
   - "slow", "latency", "p99", "memory", "leak", profiler output → `performance`
   - "production", "deploy", "container", "env var", "service won't start" → `deployment`
   - "auth", "token", "leak", "exposed", "CVE", "vulnerab" → `security`
   - "pytest", "jest", "flake", "intermittent", "passing locally" → `test`
   - On ambiguity, leave `--type` unset and treat all agent specialties as candidates for Tier 2.
3. Resolve `--scope` to a concrete path/symbol. If given, narrow auggie/serena queries to that target.
4. Compute output slug: `<type-or-untyped>-<first-5-words-of-issue-or-scope>-<YYYYMMDDHHMMSS>` and create `<output-dir>/`.
5. Open audit log; emit machine-readable header:

```text
<!-- SC:TROUBLESHOOT:TARGET
issue: <first 80 chars>
type: <type|auto>
depth: <quick|standard|deep|auto>
scope: <path|symbol|none>
fix_authorized: <bool>
no_escalate: <bool>
mcps_available: <auggie|serena|context7|tavily|sequential|none>
output_dir: <abs-path>
caller: <name|none>
context_path: <abs-path|none>
-->
```

6. If `--caller` is set, record it in the audit header `caller:` field (see the TARGET header below). If `--context <path>` is set, read it (the caller brief) and resolve it to an absolute path; STOP if the path is unreadable. When `caller=task-unified`, mark Wave 5 to emit `return-contract.yaml` (see Wave 5).

**Exit criteria**: input validated, output dir created, audit log opened. Emit "Wave 0 complete: type=<type> depth=<depth>".

**STOP conditions**: missing input, conflicting flags (`--depth quick` with `--fix`), `--depth deep` on under-specified input, `--output-dir` not writable, `--context` path unreadable.

---

### Wave 1: Tier 1 — Real-Code Grounding

**Goal**: Ground the symptom in real code and capture the reproducer/observation, BEFORE Wave 1.5 documentation grounding and BEFORE hypothesis formation (which moves to Wave 1.7). Splitting Wave 1 this way makes the Wave 1.5 dependency edge explicit: the Documentation Context Card produced by Wave 1.5 step 4 is guaranteed to exist when Wave 1.7's root-cause-analyst consumes it.

**Preconditions**: Wave 0 complete.

**Steps**:

1. **Ground the symptom in real code** — issue two parallel MCP calls (or fall back to native tools):
   - `mcp__auggie__codebase-retrieval` with query: "Find the code involved in: `<issue description, capped at ~300 chars>`. Include the function or module that produces this behaviour, recent changes near it, and any related test." Scope to `--scope` if set.
   - `mcp__serena__get_symbols_overview` on the target file or `mcp__serena__find_symbol` on a specific function if the issue names one.
   - If `--no-mcp` or both MCPs are unavailable: fall back to `Glob` + `Grep` on the issue keywords; note the fallback in the audit log.
1b. **Write the execution-locus card** — `<output-dir>/execution-locus.md`, on every invocation including pasted-log issues, re-derived each run and never carried over. One line each; `unknown` is legal, blank is illegal:
   - `PRINT-SITE:` the file / stream / job / terminal where the failing line appeared. Copy verbatim from the issue.
   - `RUN-SITE:` the `file:line` from step 1 that emits that line, `@` the process/host/environment label under which it executes. Initial value `pending-producers` if step 1 found none; overwritten by S1.6.0b step 4 with the surviving producer's `file:line`. Validator A7 rejects the sentinel at finalize **only when `producers.md` has ≥1 producer row**; otherwise the sentinel is legal with `status: partial`.
   - `SAME-ENV:` `yes` / `no` / `unknown`. Derivation: `no` if the issue text or the step-1 grounding (CI matrix, workflow file) names more than one machine, process, job, or environment label; `yes` if exactly one is named and RUN-SITE is in it; otherwise `unknown`.
   - `OBSERVE-VIA:` `same-shell` / `remote-command` / `artifact-file` / `nobody` — how RUN-SITE's stdout and exit status can be read from here.
   - If the issue names more than one arm (matrix, "works in X, fails in Y"): repeat the four lines per arm, then per *passing* arm add `CONTROL-PROOF:` `yes: <file:line>` / `no: <file:line>` / `unknown` — the line where that arm executes the RUN-SITE producer.
   - Rules:
     - `SAME-ENV ≠ yes` ⇒ every probe result and every hypothesis card carries `runs-in=<RUN-SITE label>`; a card without it is returned unread (exactly like a card without `consistency_with_docs`, Wave 1.7 step 1). `runs-in=unknown` is legal but the calibrator caps Runtime check ≤ 0.5 with Notes `locus_unknown` (C3b, refs/agent-assertions.md).
     - `SAME-ENV ≠ yes` ⇒ read the optional ref `refs/environment-deltas.md` (a generic per-delta prompt table); deltas the model cannot prove identical are candidate discriminator rows for S1.6.4 and Wave 1.7. Loading is locus-triggered, never `--type`-triggered. Absent ref ⇒ audit line `optional_ref_absent: refs/environment-deltas.md`, no Grounding Gap.
     - **Execution gate (all repros, discriminator rows, and brackets)**: `OBSERVE-VIA` describes read access, not permission or an execution transport. Closed table for `re-run permitted`: `yes` = authorized same-shell/remote-command already granted this run; `no` = issue/flags/prior artifact explicitly refuse a re-run; otherwise `unknown`. Execute only safe read-only diagnostic commands through a reachable `same-shell` or `remote-command` transport with existing authorization; `re-run permitted: no` forbids execution on every branch, even under `--no-escalate`. `unknown` is not consent and never sets `blocked-on-authorization`: leave that row pending with a reason, without adding an approval loop. Never AskUserQuestion. `artifact-file` consumes captured evidence only; new probes remain pending (`could-not-run: artifact-only`). `nobody` ⇒ record "no repro available: run-site unobservable" and continue to reporting. Fix/instrumentation diffs remain proposals, never auto-applied by a probe. S1.6.4 records the blocked-on-authorization status only when `re-run permitted: no`.
     - **Verdict source**: only when the failing arm is an identified CI job, fetch the failing arm's job log to `<output-dir>/job-<id>.log` *before* reading any verdict; the verdict is the last line in that log matching the harness's result marker, never the workflow- or job-level conclusion; no marker line ⇒ `verdict: unobservable`, `status: blocked` (not a fabricated failing test result). Non-CI artifacts retain their source/run provenance and use their own result format; an absent verdict is unknown, not FAIL, and requires no job-log download. Worked example only (not a mandatory tool): `gh run view <run-id> --json jobs --jq '.jobs[]|[.databaseId,.name,.conclusion]'` then `gh api repos/<owner>/<repo>/actions/jobs/<id>/logs > <output-dir>/job-<id>.log`; marker `^RESULT:` (a `--log-failed` view is empty under continue-on-error). Validator A8 checks the log exists at finalize.
     - A passing arm may be cited as a control only with `CONTROL-PROOF: yes: <file:line>`; otherwise Symptom coverage ≤ 0.5, Notes `control_unproven` (calibrator C3).
     - Probe packs: if `refs/probe-packs/<kind>.md` exists for any primitive kind listed for a surviving producer, load it at S1.6.4 — the load set is kind-based, never runtime- or `--type`-based.
     - Pasted logs use the same evidence-derived rules as all other issues; pasting never proves locality. Only a proven local single-process observation with reachable local execution may use `SAME-ENV: yes`, `OBSERVE-VIA: same-shell`; otherwise derive both fields normally and load the optional deltas ref when `SAME-ENV ≠ yes`.
   - Never block on `unknown`, ask the user, add a flag or an approval step, mandate an environment-specific cell, or duplicate the producer/transformer/consumer schema of refs/runtime-entrypoint-verification.md.
2. **Reproduce or observe** (when feasible and cheap; every repro obeys the step-1b execution gate; drive repro only through OBSERVE-VIA; never AskUserQuestion):
   - If OBSERVE-VIA is `nobody` or `artifact-file` and no command is already in the issue/transcript: write `no repro available: run-site unobservable` and continue. Artifact-file may consume captured evidence only.
   - If OBSERVE-VIA is `same-shell` or `remote-command` and a command is already in the issue/transcript: run it through the execution gate.
   - For build failures with a reachable transport and existing authorization: re-run the build command and capture the first error.
   - For performance issues: take the user's reported metric as the observation; do not run benchmarks in Tier 1.

**Exit criteria**: Real-code grounding complete (auggie + serena results captured in audit log, or `Glob`/`Grep` fallback noted); observation captured at `<output-dir>/tier1-observation.md` (or "no repro available" recorded in audit). Emit "Wave 1 complete: grounding done; handing off to Wave 1.5".

**Token budget for Wave 1**: target ≤ ~3k Claude tokens (MCP retrieval offloads the bulk of the work). Hypothesis formation's separate token budget is in Wave 1.7.

---

### Wave 1.5: Documentation Grounding

**Goal**: Surface release-doc context, currency-validated architectural docs, and semantic restrictions that constrain the affected surface, BEFORE any hypothesis is formed.

**Preconditions**: Wave 1 (real-code grounding) is complete; `--no-doc-discovery` is NOT set. When `--no-doc-discovery` IS set, skip this entire wave, record `doc_context_card_path: null` in the output contract, and surface a Grounding Gaps line in Wave 5's REPORT.md.

**Steps**:

1. **Load `refs/doc-discovery.md`** — read the Section 1 Auggie query templates, the Section 2 Branch B currency-check procedure, the Section 3 per-branch output schemas, and the Section 4 Documentation Context Card template.
2. **Spawn three discovery branches** in parallel via `Task` (single message with three Task calls). Each branch receives:
   - The original `<issue_description>`, `<scope>`, and `<component_paths>` from Wave 0.
   - The branch-specific Auggie query template from `refs/doc-discovery.md` Section 1 (Branch A = release-doc, Branch B = architectural-doc with Section 2 currency check, Branch C = semantic-restriction).
   - The output path for the branch's structured-output file: `<output-dir>/wave1_5-branch-<A|B|C>.md` per the Section 3 schemas.
   - An instruction to issue ONE `mcp__auggie__codebase-retrieval` call against the branch's query target and emit the schema-conformant output (Branch A: single object or `{ "hit": false }`; Branch B: array of `{ doc_path, currency_verdict, reason }`; Branch C: array of `{ source_file, file_line, quoted_text, applies_to }`).
3. **Wait for all three branches** to complete. Read each output file.
4. **Synthesise the Documentation Context Card** at `<output-dir>/doc-context.md` using the Section 4 template — merging Branch A's release-doc context (Section: Release context), Branch B's architectural-doc list with currency verdicts (Section: Architectural docs consulted; surface CAUTION lines for `stale` / `unknown` verdicts), Branch C's semantic restrictions (Section: Restrictions / decisions that constrain the fix), and a 1-3 bullet Re-frame signals synthesis tying the three findings back to the bug-as-stated.
5. **Set output-contract pointer** — emit `doc_context_card_path: <output-dir>/doc-context.md` in the audit log so Wave 5 can wire it into the report.

**Exit criteria**:

- Three branch outputs written to disk at `<output-dir>/wave1_5-branch-<A|B|C>.md`.
- One synthesised Documentation Context Card written to `<output-dir>/doc-context.md` with all four named sections populated (Release context, Architectural docs consulted, Restrictions / decisions that constrain the fix, Re-frame signals).
- Emit "Wave 1.5 complete: doc_context_card_path=<output-dir>/doc-context.md".

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| `--no-doc-discovery` set | Skip the entire wave; emit `doc_context_card_path: null`; surface in Grounding Gaps | None |
| Auggie unavailable for any branch | Fall back to `Grep`/`Glob` against the branch's query target (release dirs, docs/ dirs, scope source files); mark `degraded: true` in the affected branch's output | None |
| All three branches return empty / no-hit | Write the Documentation Context Card with "None found" in every section; set `doc_context_card_path` to the (still-emitted) card path; record `behavior_is_documented` derivation as `no_docs_found` candidate downstream | None |
| Branch B Section 2 currency check fails (`stat` not available, mtime unobtainable) | Emit `currency_verdict: unknown` for every Branch B hit; surface CAUTION lines in the card | None |
| Branch synthesis times out / one branch crashes | Continue with remaining branch outputs; mark the missing branch's section as "Branch <X> failed — see audit"; do NOT block downstream waves | None |

**Token budget**: Wave 1.5 should consume ≤ 2k Claude tokens (the auggie calls offload heavy retrieval). If it goes over 3k Claude tokens, audit-log the overrun — the wave is meant to be retrieval-offload, not Claude reasoning.

---

### Wave 1.6: Diagnosability Audit

**Goal**: Audit existing instrumentation around the failing component to decide whether the system is observable enough for Tier 1/Tier 2 hypothesis work, or whether the user should instrument first.

**Preconditions**:

- Wave 1 complete (real-code grounding done; `<output-dir>/tier1-observation.md` written).
- Wave 1.5 complete or skipped via `--no-doc-discovery` (`doc_context_card_path` is a real path or `null`).
- `--no-diagnosability-audit` is NOT set. When IT IS set: skip the wave entirely, emit `diagnosability_verdict: unknown`, `diagnosability_context_card_path: null`, `diagnosability_hard_stop: false`. The bypass is logged in REPORT.md's header AND in the audit log.
- Wave 1 has localized at least one `<component_path>` or `<scope>` — Wave 1.6 needs a code surface to inspect.

**Steps**:

1. **S1.6.0 — Component identification**. Before any branch fan-out, identify the smallest component whose output the failure asserts against. Source priority: (a) `--scope` from Wave 0 if set; (b) stack-trace bottom frame from Wave 1's observation; (c) named subsystem in the Wave 0 issue text; (d) named test in the failure transcript. Record as `failing_component` in the audit log. Branches A and B scope queries to this component first; expand outward only if no signal is found.

1b. **S1.6.0b — Producer enumeration**. ALWAYS create `<output-dir>/producers.md` with the header `observation-kind: categorical|string|trace`. When the observation is a categorical value (enum string, status word, exit code):

- Search the repo for the exact token and `<var>=` assignments, excluding markdown; list every hit as a producer row — computed enums (e.g. `rc=$prefix-unavailable`) ⇒ `producer-count=unknown`, treated as `insufficient` and as an S1.6.4 discriminator trigger.
- For each producer inside a function, list every `return`/`exit`/`break` line between the function header and the producer.
- Write the `## Producers` table `id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving=yes|no`. Assign stable `id` values `P1`…`Pn` in grep-hit order. The partition writes `surviving` into the FILE before the S1.6.4 trigger reads it, never from context. Default every grep hit `surviving=yes`. Set `surviving=no` only with a cited taken `return`/`exit`/`break` `file:line` in the exit-statement column observed taken on this failing run; if that observation is absent, leave `yes`. Row count MUST equal the grep hit count and the audit line records both numbers. Zero `surviving=yes` rows while ≥1 producer row exists ⇒ contradiction: record `surviving=re-opened` in the contradiction audit, then restore every row to `surviving=yes` before any consumer runs; retain its prior exclusion as disputed evidence, not a filter, and treat as `producer-count=unknown`. A Wave 3 split (step 4.5) appends to a separate `## Mechanism rows` section that is excluded from the count invariant.
- Primitive targeting: read only data rows of the `## Producers` table in `<output-dir>/producers.md`, stopping at the next heading; ignore table headers/separators, account for an optional leading border, and decode Markdown escapes in the named `line` cell. Require a terminal `:<positive line number>`, remove only that suffix, resolve the remaining path against the repository root, verify it exists, and deduplicate paths. Never pass headings or coordinates as shell paths; quote each resolved path when used as a command argument. Inspect each producer's source expression and immediate call operands, classifying its primitives using refs/primitive-differential.md Section 1 (a classification table, not a regex catalogue); record each identified expression's `file:line` and kind. Queue exact/reference pairs under the single S1.6.4 pair budget, not a separate row limit. Replace `pending-producers` with all surviving producer coordinates and their environment labels (one when unique, an explicitly unresolved candidate set otherwise); do not invent a unique run site.
- A control arm counts only if the locus card records `CONTROL-PROOF: yes: <file:line>` for it (`no: <file:line>` / `unknown` otherwise). Never rank producers by plausibility here; never drop a row without a cited exclusion line; never grep only `failing_component`; agents cite rows by `id` plus `file:line`, they never re-grep (every Wave 1.7/Wave 3 brief pastes the full table).

2. **S1.6.1 — Load `refs/diagnosability-audit.md`** (lazy load, mirroring Wave 1.5's discipline). Read Section 1 (query templates), Section 2 (fallback paths), Section 3 (per-branch schemas), Section 4 (sufficiency rubric + 3-W's synthesis), Section 5 (complexity gate), Section 6 (Diagnosability Context Card template), Section 7 (tasklist rules), Section 8 (T4 worked example).

3. **S1.6.2 — Spawn 2 audit branches in parallel** via `Task` (single message, two Task calls):
   - **Branch A — Log-Call Inspection**: logger/print/exception-handler calls + error-reporter SDK initializations on the `failing_component` and immediate callers. Captures exception-handler richness as a piggyback signal (no separate branch).
   - **Branch B — Log-Config Inspection**: log-config files, env vars, structured-log filters, sampling configuration that governs runtime log emission for the `failing_component`.

4. **S1.6.3 — Wait for branches; synthesize Diagnosability Context Card** at `<output-dir>/diagnosability-context.md`. Synthesis includes the **3-W's coverage scoring** (orchestrator logic): `{ when_answerable, where_answerable, why_answerable } ∈ { yes | partial | no }`, computed against Branch A inventory + Branch B reachability + Wave 1 observation. **Byte-count column** populated from runtime-content sniffs of any log file paths discoverable from the failing-run transcript; `n/a (audit-time only)` when no captured-content is available.

5. **S1.6.4 — Apply sufficiency rubric + complexity gate**. Compute `diagnosability_verdict ∈ {sufficient | partial | insufficient | unknown}` using refs/diagnosability-audit.md Section 4: evaluate S14 first for evidenced loss/substitution of the actual disputed missing datum, then S1–S13 in their existing order. Apply the same priority on recomputation; unrelated hidden fields do not trigger S14. Compute `issue_complexity ∈ {trivial | non-trivial}` from Wave 0 + Wave 1 signals only (no Wave 1.7 dependency). **Discriminator trigger (evaluated before the branch)**: set the audit line `discriminator-required: yes` when `producers.md` has ≥2 `surviving=yes` rows, OR the observed datum is absent from every captured output of the failing run including `job-*.log`, OR `producer-count=unknown` (including the zero-surviving re-open of S1.6.0b step 3); otherwise `discriminator-required: no`. A `NameError` with one producer never enters this step. When `yes`: (i) if `verdict ∈ {sufficient, unknown}` then `verdict := partial` so the tasklist is emitted (`insufficient` unchanged); (ii) write `## Discriminator rows` in `diagnosability-tasklist.md` per refs/diagnosability-audit.md Section 7 — one `<id>-exact` / `<id>-ref` pair per `surviving=yes` producer (`<id>` is the producer table `id` from S1.6.0b) (probe-form from refs/primitive-differential.md), running the Wave 3 step 1 behaviour-definition fetch first for any producer or card whose mechanism asserts what a primitive *does*, one shared budget of at most 8 base pairs (16 probe rows) across enumeration and S1.6.4, nearest to the exit statement first; one separate control row and at most two extra distinguishing rows are outside that budget (maximum 19 core rows, excluding informational pack rows). Append and separately account for optional pack rows under refs/primitive-differential.md Section 2 step 3; never replace a mandatory core row with a pack row. Full core plus the three-row read/parse pack for one producer is 19 + 3 = 22 emitted rows, not a core-budget violation. Overflow ⇒ header `probe-rows-truncated: <n>`, where n counts omitted pairs, despite the legacy field name: 10 proposed pairs → 8 retained, n=2; omitted producer identities remain in the menu and are explicitly untested), one control row (`CONTROL-PROOF: yes: <file:line>` arm, else the table's control column). If `CONTROL-PROOF: yes: <file:line>` AND `SAME-ENV ≠ yes`, copy primitive-differential Section 2 into Discriminator rows; else write `comparator=none` and take the `UNDETERMINED — no comparator` path. Every CONTROL-PROOF site uses `yes: <file:line>` / `no: <file:line>` / `unknown`, measurement preregistrations per Section 7 constraint 6 (`value-if-<claim>-true | value-if-false`, allowing equal predictions or justified unknown; consistent/refuted/inconclusive mappings), and seek at least one pair that differs between any two surviving causes (add at most two rows; no grounded split ⇒ header `indistinguishable: <a>,<b>`, never fabricated values). Enabling tasks link measurement IDs plus operational verification/rollback rather than causal predictions; a `## Fix candidate` row is a proposal only, with its paired verification; applying it requires the existing `--fix` and explicit-confirmation gates and is never part of automatic probing. Before (iii), write the Emitter search block and apply the status-precedence rule below independently of verdict, complexity, and `--no-escalate`; load/increment the shared round counter and enforce its cap before execution. (iii) apply Wave 1 step 1b's execution gate to each read-only diagnostic row; do not execute under an authorization block or the round cap. Capture exit status only and no secrets, with run/arm/command provenance in `tier1-observation.md`; artifact-only access consumes existing evidence and leaves new rows pending with a could-not-run reason. Re-evaluate S14 and recompute `diagnosability_verdict` after any new observation. Pending or executed-but-inconclusive rows both follow the recomputed verdict, not execution success. An authorization/capability/cap block routes directly to Wave 5 with the tasklist retained; otherwise branch on `(verdict × complexity)`:
   - `insufficient` AND `non-trivial` AND NOT `--no-escalate` → **hard-stop** (including probes that ran but left the recomputed verdict insufficient, as well as pending probes): emit `diagnosability-tasklist.md` in the section order of refs/diagnosability-audit.md `Section order (S1.6.4a)`, set `diagnosability_hard_stop=true`, jump to Wave 5 (Waves 1.7–4.5 skipped; hardening does not run on diagnosability hard-stop). No hypothesis work happens in the same turn as the instrumentation patch. Measurement rows and linked enabling tasks obey Section 7 constraint 6; unknown/non-discriminating outcomes never prevent honest pending publication. The tasklist MUST contain `## Emitter search` (Section 7 constraint 5), with truthful raw `emitters-found` / `already-read-files` counts, candidate exclusions and separate `usable-capture-routes` count. A route requires actual datum access through a technically viable permitted-site capture path, not a source hit, sink or annotation alone. Shared rule for EVERY emitted tasklist, including later first creation, evaluated before execution and these branches: an emitter row plus `re-run permitted: no` ⇒ `pipeline_hardening_verdict: blocked-on-authorization`, `status: blocked`; zero usable routes with documented channel/candidate exclusions ⇒ `capability-verdict: blocked`, `status: blocked`. A viable route with yes/unknown permission leaves required measurements pending until the execution gate permits capture; unknown is not consent. Refusal is not absence of capability. Unresolved relevant core evidence contributes partial, but optional pending pack cells never independently contribute partial. Preserve failed-over-blocked status merge.
   - `insufficient` AND `non-trivial` AND `--no-escalate` → soft-warn (suppressed by user assertion). Emit tasklist, surface in REPORT.md, continue to Wave 1.7.
   - `insufficient` AND `trivial` → soft-warn: emit tasklist (informational), continue to Wave 1.7.
   - `partial` → continue to Wave 1.7; surface in REPORT.md's Diagnosability Context section.
   - `sufficient` OR `unknown` → continue to Wave 1.7; surface in Diagnosability Context (or Grounding Gaps for `unknown`).
   - **`--depth deep` modifier**: does NOT force the hard-stop, BUT when `verdict ∈ {insufficient, partial}` under `--depth deep`, the soft-warn becomes mandatory and prominent — REPORT.md gains a top-of-report banner: "Your hypothesis depth was constrained by insufficient evidence — see Diagnosability Context."

**Shared tasklist creation/append (all waves, including audit bypass):** lazily load refs/diagnosability-audit.md Section 7 and only the needed primitive-differential sections. First creation materializes the complete Section order with stable branch/venue identity, emitter route assessment, preregistered measurement/linked enabling rows, execution eligibility/authorization and pending reasons. Set `discriminator-required: yes` for definition-failure/splitting measurements and consume the shared locked counter once before any execution; an existing tasklist reuses that invocation's increment, or increments once when its requirement first changes to yes. Never rerun the bypassed audit or fabricate its Context Card. Every append preserves pending rows for Wave 5; authorization/capability/cap blocks go to the common epilogue, retaining the artifact.

**Per-defect patch-round counter**: the authoritative store is `<repo-root>/.dev/troubleshoot/diagnosability-rounds.json`, independent of the timestamped or custom output directory; `<output-dir>/diagnosability-rounds.json` is only this run's snapshot. Read the authoritative store before every counted emission; create its parent directory as needed and initialize an absent store to an empty mapping under the same lock (an existing unreadable/corrupt store is never treated as absent). Entries are logically keyed `<branch>:<repro-venue-id>` but stored as nested JSON objects keyed by branch then venue, avoiding delimiter collisions. Preserve the failing arm's stable matrix/job label (or exact repro command) with digits stripped so re-numbered runs of the same venue share one 3-round key; do not use a transient run ID. Record that identity in the tasklist and snapshot. Increment once per run that emits a tasklist with `discriminator-required: yes`, not per rewrite, append, probe or bracket round; later Wave 3 emissions use the same rule. Serialize read/update/snapshot under a store lock and replace the store atomically; unreadable/corrupt/locked state is a reported block, never a silent reset. At round 3 or later still write the tasklist, emit the cap message with `status: blocked`, skip automatic reruns and suppress their recommendation. `--reset-diagnosability-rounds` clears only the current branch/venue entry under the same lock before increment; other entries survive. With three fresh output directories the same identity records 1, 2, 3, not 1, 1, 1.

**Exit criteria**:

- Two branch outputs at `<output-dir>/wave1_6-branch-<A|B>.md`.
- Diagnosability Context Card at `<output-dir>/diagnosability-context.md`.
- Diagnosability tasklist at `<output-dir>/diagnosability-tasklist.md` (when verdict ∈ {partial, insufficient}).
- Emit `Wave 1.6 complete: verdict=<v> complexity=<c> hard_stop=<bool> round=<N>/3 discriminator-required: <yes|no>`. (Activation metric: `yes` on more than 20% of `bug`-type runs ⇒ tighten the trigger to the datum-absent clause only.)

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| `--no-diagnosability-audit` set | Skip Wave 1.6 entirely | Emit `diagnosability_verdict: unknown`, `diagnosability_context_card_path: null`, `diagnosability_hard_stop: false`; log bypass in REPORT.md header AND the audit log |
| Auggie unavailable (Wave 1.6) | Fall back to Glob/Grep per `refs/diagnosability-audit.md` Section 2 | Set Branch A/B `degraded: true`; cap verdict at `partial` (never `sufficient`) |
| Both Wave 1.6 branches return empty | Cannot compute 3-W's coverage | Set verdict = `insufficient` if complexity non-trivial; `partial` if trivial; surface in Grounding Gaps |
| `failing_component` not localizable | S1.6.0 cannot identify the smallest failing component | Set verdict = `unknown`; add Grounding Gaps line; continue to Wave 1.7 without hard-stop |
| Heisenbug detected on Wave 1.6 re-run | Instrumentation altered timing — bug no longer reproduces | Downgrade next-round tasklist to env-vars-only (no `--debug` flag changes, no log-level overrides); record Heisenbug finding in audit card |
| 3-round diagnosability cap reached for a counter key | Authoritative counter at `<repo-root>/.dev/troubleshoot/diagnosability-rounds.json` reached 3 tasklists with `discriminator-required: yes` for the same `<branch>:<repro-venue-id>` (digits stripped) | Write the tasklist anyway; emit the 3-round cap message (refs/report-template.md hard-stop variant + cap-specific prose) with `status: blocked`; suppress the re-run recommendation (not the file) until `--reset-diagnosability-rounds` is set |

**Token budget**: ≤ 2-3k Claude tokens (auggie offloads retrieval bulk). Hard-stop case yields a net token saving over the full Tier 2 pipeline.

---

### Wave 1.7: Tier 1 — Hypothesis Formation

**Goal**: Form one calibrated Tier 1 hypothesis card, consuming the Wave 1.5 Documentation Context Card (when produced) so the hypothesis is doc-grounded from the start.

**Preconditions**: Wave 1 (real-code grounding) is complete; Wave 1.5 has produced a Documentation Context Card at `<output-dir>/doc-context.md` (or `--no-doc-discovery` was set and `doc_context_card_path` is `null`); Wave 1.6 did NOT fire its hard-stop (or was skipped via `--no-diagnosability-audit`, or fired soft-warn under `--no-escalate`). When Wave 1.6 hard-stopped, this wave is skipped entirely.

**Steps**:

1. **Form one hypothesis** — spawn the `root-cause-analyst` agent via `Task` with a focused brief: the symptom, the grounding from Wave 1 step 1, the observation from Wave 1 step 2, the Documentation Context Card path (`<output-dir>/doc-context.md`, or `null` when Wave 1.5 was skipped via `--no-doc-discovery`), and `--scope` if any. The agent's job is to produce one hypothesis card (template in `refs/hypothesis-card-template.md`) — not three, not the full tree. The hypothesis card MUST set `consistency_with_docs` to one of `aligned | conflicts | not_applicable | no_docs_found` based on the Documentation Context Card (or `not_applicable` when the card path is `null`). When the execution-locus card (`<output-dir>/execution-locus.md`) derives `SAME-ENV ≠ yes`, the card MUST also carry a plain `runs-in=<RUN-SITE label>` line (`unknown` is legal; the calibrator then caps Runtime check ≤ 0.5 with `locus_unknown`); a card without it is returned unread, exactly like a card without `consistency_with_docs`. The brief pastes the full `## Producers` table of `<output-dir>/producers.md` verbatim when it exists; only when that table contains at least one `surviving=yes` row is a card naming the categorical value but citing none of those rows returned unread (refs/triage-checklist.md, Producer citation). If the table is missing or has no surviving rows, log `producer-citation-check: skipped — menu absent or empty`; require ordinary grounded `file:line` or captured-command-output citations and continue behaviour binding and independent calibration. This bypass skips only producer-row citation, not the documentation, locus, evidence or confidence checks; never invent a producer row.
1.5. **Bind behaviour evidence after receipt** — run the shared Wave 3 step 1 behaviour-definition procedure on the Tier 1 card (including inline formation), attach its row citation, and persist the card before step 2 captures `card_mtime`; reuse matching producer-definition rows from S1.6.4.
2. **Calibrate confidence (independently)** — spawn the `confidence-calibrator` agent via `Task` with `card_path=<output-dir>/tier1-hypothesis.md`, `rubric_path=<skill-dir>/refs/escalation-rubric.md`, `card_tier=1`, `flags_context=<wave 0 parsed flags>`, `output_path=<output-dir>/tier1-calibration.md`, `now_iso=<ISO-8601 from this turn's`date -u +%Y-%m-%dT%H:%M:%SZ`>`, `card_mtime=<ISO-8601 mtime of card_path>` (GNU: `date -u -d "@$(stat -c %Y "<card_path>")" +%Y-%m-%dT%H:%M:%SZ`; BSD: `date -u -r "<card_path>" +%Y-%m-%dT%H:%M:%SZ`; missing mtime ⇒ drop that citation / omit `card_mtime`), `behaviour_definitions_path=<output-dir>/behaviour-definitions.md` (omit/null if the file does not exist), `tasklist_path=<output-dir>/diagnosability-tasklist.md` (omit/null if the file does not exist so skip rules fire), `locus_path=<output-dir>/execution-locus.md` (omit/null if the file does not exist), `assertions_path=<skill-dir>/refs/agent-assertions.md`. The agent re-grades the hypothesis card against the 6-dimension rubric without the formation context (anchoring is reduced, not eliminated). Its calibrated confidence and verdict feed Wave 2 directly.
   - **Fallback**: if `confidence-calibrator` fails (subprocess crash, malformed output, agent unavailable), fall back to inline orchestrator calibration against the rubric and mark `calibration: inline-fallback` in the audit log. The inline path applies the identical C-rule list in `refs/agent-assertions.md` (C1-C8, C3b) with the same inputs the spawn would have received and records `structural_flags: <fired flags or none>` beside the `calibration: inline-fallback` audit line. Persist the full agent Output Format at the normal per-card `output_path`, not just the audit: adjusted per-dimension scores and evidence, Stage-2 trace, canonical structural table including skipped rows, final confidence, recommendation/provenance, restrictions and Notes. The orchestrator persists returned agent reports too; neither read-only agent mutates input files or needs Bash/Write tools.
   - **Receipt gate**: apply the shared calibration completeness/failure ladder below (under Wave 3) to this Tier 1 card before Wave 2, and to each Tier 2 card before weighting/distillation. A valid inline artifact satisfies the gate without a retry; an audit-only result does not. Carry retained scores/caps and C1 through retries and all downstream consumers.

**Exit criteria**: One hypothesis card at `<output-dir>/tier1-hypothesis.md`, a valid calibration report at `<output-dir>/tier1-calibration.md` (agent or full-schema inline), and the calibrated confidence in the audit log. Emit "Wave 1.7 complete: confidence=<x>" only on this success path. Terminal calibration failure follows the shared ladder directly to Wave 5's failed diagnostic epilogue, not Wave 2.

**Failure handling**: If the `root-cause-analyst` agent fails entirely (subprocess crash, no output card produced), fall back to inline orchestrator hypothesis formation against `refs/hypothesis-card-template.md` and mark `hypothesis_source: inline-fallback` in audit. Wave 2 confidence gate proceeds normally with whatever was produced.

**Token budget for Wave 1.7**: target ≤ ~3k Claude tokens (excluding the agent subprocess; the agent's own budget is governed by `--models` if overridden).

---

### Wave 2: Confidence Gate

**Goal**: Decide whether to stop or escalate.

**Decision logic** (from `refs/escalation-rubric.md`, summarised here for traceability):

- `--depth quick` OR `--no-escalate` → STOP at Tier 1 regardless of confidence; emit warning in report if confidence < threshold.
- `--depth deep` → ALWAYS escalate to Tier 2.
- Otherwise (`--depth standard` or unset):
  - `confidence ≥ 0.85` AND symptom is single-domain → STOP at Tier 1.
  - `confidence < 0.85` → escalate.
  - Multi-domain symptom (e.g. perf + correctness, security + build) → escalate even if confidence is high (because one hypothesis cannot cover both domains adequately).
  - Reproducibility unclear or "intermittent" mentioned → escalate.

**On STOP**: jump to Wave 5 (synthesis + report) with `tier_reached=1`.

**On escalate**: record the `escalation_reason` in the audit log and proceed to Wave 3.

---

### Wave 3: Tier 2 — Parallel Hypotheses

**Goal**: Cast a wider net with multiple independent perspectives, then surface the strongest candidate fixes.

**Preconditions**: Wave 2 decided to escalate.

**Agent selection** — pick 2-4 agents based on `--type` and signal mix. Each agent runs in its own context, in parallel, via `Task`:

| Signal / type | Agents to spawn |
|---------------|------------------|
| `bug` (default) | `root-cause-analyst`, `quality-engineer` (edge cases), + 1 of {`refactoring-expert` if recent refactor signals, `system-architect` if multi-component} |
| `performance` | `performance-engineer`, `root-cause-analyst`, `system-architect` (if cross-component) |
| `security` | `security-engineer`, `root-cause-analyst`, `quality-engineer` |
| `build` | `root-cause-analyst`, `devops-architect`, `refactoring-expert` |
| `deployment` | `devops-architect`, `root-cause-analyst`, `system-architect` |
| `test` | `quality-engineer`, `root-cause-analyst`, `refactoring-expert` (if test is brittle by structure) |

Cap at 4 agents. If `--type` is unset and signals point in multiple directions, spawn 3 from the union of relevant rows.

**Steps**:

1. **MCP enrichment in parallel with agent spawn** — issue any of the following that match the signals (parallel calls, all kicked off in the same turn):
   - `mcp__context7__resolve-library-id` + `mcp__context7__query-docs` when the issue mentions a framework / library by name or the stack trace is in third-party code
   - `mcp__tavily__tavily_search` for the exact error message string + "github issue", or for `<library> <version> <symptom>` (rate-limited — at most 2 queries in this wave; for the error-string query use `search_depth: advanced` with recommended `include_domains: [github.com, stackoverflow.com]` — only hard cases reach Tier-2, and the ≤2-query cap bounds cost)
   - `mcp__auggie__codebase-retrieval` with a more targeted query than Tier 1 (e.g. "find every call site of `<symbol>` and how they handle the error case")
   - **Behaviour-definition fetch (conditional, never a halt)** — Shared procedure callable before S1.6.4 pair construction and after card receipt in both tiers. Input is a producer assertion (with its source coordinate) OR a hypothesis card; reuse an existing definition row only for the same primitive and asserted behaviour. Trigger: an input whose `claim_class` is `environment_dependent`, or whose assertion/mechanism sentence says what a primitive (library call, config loader, scheduler, protocol, runtime builtin) *does*, when that behaviour has not been directly observed in this run. For each such input append one row (`# | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status`) to `<output-dir>/behaviour-definitions.md` **before** issuing the fetch:
     - *Asserted behaviour* = the verb phrase copied verbatim from the producer assertion or card's mechanism sentence
     - *Defining artifact* = the thing that makes that verb true (function body, spec/RFC clause, schema rule, doc section whose heading contains the verb) — never an example, sample output, format string, tutorial, or web-search summary
     - *Fetch query* built only from the words in column 3, phrased as "the code or clause that implements/specifies `<asserted behaviour>`" — adding words about output appearance or format is a violation
     - Fetch verbatim: `mcp__context7__query-docs` → remote URL fetch → raw source fetch (e.g. `gh api`); paste the returned lines into `tier1-observation.md` under `## Behaviour definitions` with source coordinates; Status `fetched:<source>`
     - If the return is an example rather than a definition, or every fetch fails: Status `recalled, not load-bearing`, and add a probe row observing the asserted behaviour directly to `diagnosability-tasklist.md` `## Discriminator rows` (create/append via the Shared tasklist creation/append rule above, including after audit bypass)
     - The card's evidence section MUST cite its row as `behaviour-definition: row N`; the calibrator (C8) and the inline fallback assert the row exists with a non-empty Status — missing/empty caps the card at 0.5 and logs `behaviour-cite: missing`. Never substitute a web-search summary for the artifact; never make the fetch mandatory when the behaviour was observed in this run.
2. **Spawn hypothesis agents** in parallel via `Task` (single message with multiple Task calls). Each agent receives:
   - The original issue + Tier 1 hypothesis card (so they can agree, disagree, or extend)
   - The **Documentation Context Card** at `<output-dir>/doc-context.md` (the same single card produced by Wave 1.5 — agents do NOT re-run discovery). If `--no-doc-discovery` was set, this path is `null` and agents set `consistency_with_docs: not_applicable` in their hypothesis cards.
   - The MCP enrichment results
   - The output path for their own hypothesis card: `<output-dir>/tier2-<agent-name>-hypothesis.md`
   - An instruction to produce **at most one proposed fix** with: claim, evidence (cited file:line or command output), proposed fix, confidence, risks, `consistency_with_docs` (see `refs/hypothesis-card-template.md`), and a one-line "if I'm wrong it's probably because...".
   - When `<output-dir>/producers.md` exists, paste its full `## Producers` table verbatim (never summarised), with `observation-kind`/`producer-count`; also paste tasklist discriminator rows when present. **Menu-equality check** before spawning: compare the SET of surviving producer identities (table row ID plus `file:line`) in the prompt with the SET in the on-disk table; the sets must match, even when several producers emit the same token. Separately require coverage of every surviving enum value; never equate distinct-token count with producer count. Repair missing identities before spawning. If the audit was bypassed and no table exists, explicitly record the absent menu and skip only this table-dependent check, not grounding/calibration; never invent a producer file.
   - Use the agent's default model. If `--models` overrides per-tier, apply (e.g. `hypothesis:opus` forces all hypothesis agents to opus).
3. **Wait for all agents** to complete. Read each card. Before step 3.5, run the shared behaviour-definition procedure on every newly received or inline-formed card, bind its evidence citation to the definition row, and persist the completed card before capturing its mtime. Parallel enrichment alone does not satisfy this post-receipt binding.
3.5. **Calibrate each card independently** — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card), each with the full Wave 1.7 step 2 kwarg set: `card_path=<output-dir>/tier2-<agent-name>-hypothesis.md`, `rubric_path=<skill-dir>/refs/escalation-rubric.md`, `card_tier=2`, `flags_context=<wave 0 parsed flags>`, `output_path=<output-dir>/tier2-<agent-name>-calibration.md`, `now_iso`, `card_mtime` (per card; same GNU/BSD capture as Wave 1.7), `behaviour_definitions_path` (omit/null if absent), `tasklist_path` (omit/null if absent), `locus_path` (omit/null if absent), `assertions_path=<skill-dir>/refs/agent-assertions.md`. Use the calibrated scores (not the agents' self-reports) when weighting consensus/competing/outlier in step 4. Fallback rule from Wave 1.7 applies per-card.
4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mark them as **competing**. If they all converge on one fix, mark as **consensus**.
4.5. **Same-evidence divergence → splitting experiment** — when two cards cite the same `file:line` and assert different mechanisms:
   - Write both mechanisms as one row each under `<output-dir>/producers.md` `## Mechanism rows` (excluded from the S1.6.0b count invariant).
   - Fill one discriminator form (refs/hypothesis-card-template.md, Falsification standard) per pair: when a grounded discriminator exists, name its command and evidence-backed differing outcomes (archetype: the `read/parse` row of refs/primitive-differential.md Section 1 — exact idiom vs bulk read, same input, exit status each). Otherwise record `No discriminating falsifier established`, the missing-evidence reason and an honest unknown/non-discriminating measurement plan; never invent a command or differing predictions. Such a plan keeps Diagnosis UNDETERMINED and root_cause_summary empty until independent discriminating evidence exists.
   - Append the grounded probes OR the pending unknown/non-discriminating plan as rows to `<output-dir>/diagnosability-tasklist.md` `## Discriminator rows` (use Shared tasklist creation/append, including its complete schema/counter/gates if Wave 1.6 emitted none).
   - Mark the cluster `split-pending` — it is excluded from Wave 4's competing set (the pair decides, not a debate) and refs/escalation-rubric.md escalates it with `escalation_reason: split_pending`. Cluster/index token is `split-pending`; `escalation_reason` is `split_pending` (underscore alias; do not collapse them). Wave 4 debates only fix mechanism for a shared diagnosis. One archetype row, not a library. Never require both probes to return before Wave 5; never block on the debate; never add a third hypothesis agent to break ties.

#### Tier 2 calibration completeness gate (hard precondition for report publishing)

**Shared receipt/failure ladder (both tiers):** after calibration/fallback, before Wave 2 or Wave 3 distillation, verify each current-run card's normal sibling calibration on disk (`tier1-calibration.md` or `tier2-<agent-name>-calibration.md`). Agent and inline results use the same full Output Format. Require six justified adjusted dimensions, Stage-2 trace and recomputation, finite final confidence in [0,1], recommendation/reason/provenance, and the canonical nine-row C-rule table when assertions were supplied. Marker presence alone is not validity.

- Persist known independently computed scores, dimension adjustments, fired caps and C1 provenance on receipt, including a valid inline result whose file write failed; retain that history before any retry replaces an artifact. Across fallback/retry/degradation for the same card, never increase the known score, loosen an adjustment/cap, or lose a fired C1 recommendation. Merge retained adjustments before recomputation; the effective score is the minimum of the new recomputed result, all retained scores and all fired caps. Record any retained-score bound separately from the unchanged rubric derivation. Re-evaluate C1 at the effective final score; preserve forced ESCALATE while quick/no-escalate still suppress actual fan-out. Unverified values from malformed output are not known calibration evidence. Before any downstream consumption, persist the merged effective report at the normal sibling path with the adjusted dimensions, recomputed trace, retained-bound provenance, structural rows, final score and recommendation consistent throughout; read it back. A raw higher retry score must never remain the disk value consumed by weighting or validation. Failure to persist/read back the effective report follows the same one-retry/terminal-failure ladder, not a fresh retry budget.
- If the normal artifact is missing or invalid after initial fallback:
  1. Log `calibration: missing` or `calibration: malformed` with the absolute card path and actual failure/provenance; do not synthesize evidence.
  2. Re-dispatch the `confidence-calibrator` `Task` once with the same inputs, wait up to 2 minutes, persist and validate its result under this same gate. There is exactly one retry, not a new retry allowance after fallback; no third dispatch. A valid result inherits the retained bounds above.
  3. If that retry cannot yield a valid persisted calibration, record `calibration_status: failed_to_calibrate` and the retained known scores/flags/recommendation in `audit.log` and at the normal sibling path as an explicitly labelled calibration FAILURE record (not a successful Calibration Report; unavailable dimensions remain unavailable). If persistence itself fails, record the unavailable path rather than inventing a file. Set effective output confidence to conservative `0.0`, explicitly a failure sentinel, not a fabricated rubric score or self-report. Keep known C1 provenance; unknown rule inputs remain unknown, never fabricated passes or flags. Contribute `failed`, skip confidence-based selection/debate and route to Wave 5's common failed diagnostic epilogue. Publish only UNDETERMINED/noncausal failure information, Grounding Gaps and pending work; no normal partial card publication, causal fix, or escalation that bypasses user restrictions.

Verification command: run one initial on-disk completeness check per tier over the cards actually written (markers `# Calibration Report`, `## Per-dimension scores`, `## Confidence`, `## Escalation recommendation`, `**Verdict**` STOP/ESCALATE and `**Calibrated (this report)**` plus the full-schema/numeric checks above). After the single retry, validate only its changed output; this required receipt check is not a cosmetic repeated marker grep. A terminal FAILURE record takes the failed diagnostic branch and is never accepted as a valid calibration. Wave 5 receives only existing calibration/failure paths and retains their explicit failure status; absence never becomes a successful calibration.

**Exit criteria**:

- ≥ 1 hypothesis card written to disk
- A `candidate-fixes.md` index file written listing each unique fix proposal, the supporting agent(s), and a quick verdict (`consensus` / `competing` / `outlier` / `split-pending`); persist `split-pending` and exclude it from every Wave 4 eligibility path, including `--depth deep`

**Failure handling**:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Agent subprocess fails | Continue with remaining agents; record failure in audit | If < 2 agents complete, downgrade to "Tier 1 only" and add a warning to the report |
| MCP call fails (auggie/serena) | Fall back to `Grep`/`Glob`; note in audit | None — proceed without that enrichment |
| MCP call fails (context7/tavily) | Continue without external docs; note in audit | None |
| All agents converge with high confidence | Skip Wave 4 (adversarial) only if the converged variable was *observed* in this run; otherwise mark the cluster `split-pending` (step 4.5) and append its probe pair to the tasklist; then jump to Wave 5 | None |
| All agents diverge with low confidence | Proceed to Wave 4; warn in audit that no fix is strongly supported | None |

---

### Wave 4: Tier 2 — Adversarial Fix Debate

**Goal**: When Wave 3 produced ≥2 competing strong fix proposals (cap is the Tier-2 agent cap of 4, not a debate min/max of 3), let `/sc:adversarial` debate them so the chosen fix has earned its position.

**Preconditions**: Wave 3 marked ≥ 2 fixes as `competing` (or `--depth deep` + ≥ 2 distinct proposals, even if consensus), and no mechanism disagreement remains un-probed — clusters marked `split-pending` by Wave 3 step 4.5 are excluded from the competing set (their probe pair decides, not a debate); Wave 4 debates only fix mechanism for a shared diagnosis.

**Steps**:

1. **Materialise each candidate fix as a standalone file** — write `<output-dir>/fix-proposals/fix-<N>.md` for each, structured as a self-contained proposal (problem statement, proposed change, evidence, risks, test plan). **When a Documentation Context Card exists at `<output-dir>/doc-context.md` (i.e., `--no-doc-discovery` was NOT set)**, append a final `## Documented constraints to honor` section to every `fix-<N>.md` containing a verbatim copy of the Card's Restrictions and Re-frame signals sections. This embed makes the debate doc-context-aware via the `--compare` artifact channel without introducing any new flag on `/sc:adversarial`. The debate agents, instructed to read each fix proposal in full, will weight proposals against the embedded constraints naturally. A fix that violates an embedded constraint must be either rejected outright by the debate, or wrapped as a **doc-update + fix bundle** (see step 3 output mode).
2. **Invoke `/sc:adversarial` in compare mode** via `Skill`:

   ```text
   Skill sc:adversarial-protocol with --compare fix-1.md,fix-2.md[,fix-3.md] \
       --depth quick (when source signals are strong) | standard (default) \
       --focus correctness,risk,test-coverage \
       --output <output-dir>/adversarial/
   ```

   - Use `--depth quick` if all proposals share the same diagnosis and only differ in the fix mechanism (fast debate is sufficient).
   - Use `--depth standard` otherwise.
3. **Collect adversarial output** — `<output-dir>/adversarial/` will contain the standard 6 artifacts (`diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `merged-output.md`). The merged output is the **chosen fix proposal**. If the debate flagged that the winning proposal requires a doc update to remove or rewrite a documented constraint (surfaced via the embedded `## Documented constraints to honor` section in the source fix-<N>.md), the merged output is structured as a **doc-update + fix bundle**: the bundle lists the doc file(s) to update alongside the code change(s), and Wave 5's Proposed Fix section renders both atoms.
4. **Sanity-check the merge** — spawn `self-review` via `Task` against the merged fix proposal with the four standard self-check questions (tests? edge cases? requirements? follow-up?). Record the result in the audit log. If self-review flags a blocker, surface it and STOP — do not proceed to Wave 5 with a known-broken proposal.

**Exit criteria**: `adversarial/merged-output.md` exists, `self-review` produced an OK or a documented blocker.

**Skip conditions**: only one viable fix proposal (skip and proceed to Wave 5), or all proposals failed sanity in Wave 3.

---

### Wave 4.5: Pipeline Hardening Closure

**Goal**: When the diagnosed issue is a *pipeline escape* (a defect at a runtime / generated-artifact / shared-contract / review-input boundary), prove the invariant at the same boundary where the escape can recur — before the report closes. This wave closes the E1–E5 escape class via reusable, mechanism-based gates HC0–HC5. Full mode spec: `refs/pipeline-hardening-closure.md`.

**Trigger**: Topology-driven, **not** a CLI flag (NFR-5). This wave runs after Tier-1 diagnosis is settled (and after any Tier-2 waves) and before report closure. HC0 sets `pipeline_hardening_applicable=true` when the issue touches a trigger boundary (CLI/subprocess, file/stdin/prompt delivery, generated-artifact parser, gate/severity/status enum, duplicated evaluator, persisted/resume state, review/audit selector, sibling pipeline, prior-escape unmask); otherwise it sets `false` and records the boundary scan that justifies the skip. When `applicable=false`, skip HC1–HC5 and proceed to Wave 5.

**Steps** (when `pipeline_hardening_applicable=true`):

1. **HC0 — Applicability + mechanism** (`refs/pipeline-hardening-closure.md`): emit the typed boundary-scan rows, a feature-agnostic mechanism statement, and the candidate `known_escapes_caught` set (each ID justified by the wave/card that catches it). A bare "looks local" rationale is invalid. HC1–HC5 cannot be silently skipped — each emits `PASS` / `FAIL` / `N/A` with a rationale/waiver.
2. **HC1 — Runtime-entrypoint verification** (`refs/runtime-entrypoint-verification.md`): build the runtime-entrypoint card; the replay must reach the production boundary (not a helper/mock), with a negative witness (fix-reverted → FAIL) for every forbidden interpretation. Record `runtime_entrypoint_card_path`.
3. **HC2 — Contract enumeration** (`refs/contract-enumeration.md`): build the producer/transformer/consumer ledger and sweep sibling pipelines / duplicate evaluators. FAIL on an empty ledger, an unclassified live consumer, or generic proof used for a product path without proving the product path reaches it. Record `contract_ledger_path`.
4. **HC3 — Unmask and sweep** (`refs/unmask-and-sweep.md`): run full generated artifacts through the small formal allow-list grammar (word-boundary matching; substring containment is never behavior-controlling), with positive + sibling-negative + full-artifact-mixed fixtures and per-consumer HALT/WARN/CONTINUE assertions; document `K_true`/`K_swept`. Record `unmask_sweep_path`.
5. **HC4 — Effective-input proof** (`refs/effective-input-proof.md`): when an independent review/audit/reflect gate consumes an indirect selector, prove `|included_files ∩ runtime_surface_claim|` is correct (fail closed on absent / empty-despite-changes / non-reproducible / non-empty-but-wrong-surface — `E>0` is not sufficient). Record `effective_input_card_path`.
6. **HC5 — Off-path reviewer rule** (`refs/pipeline-hardening-closure.md`): set `off_path_review_decision` ∈ `required | performed | waived_with_rationale | not_required`. A waiver is invalid if it merely says tests pass / reviewer independent / command exists / issue looks local. A valid `waived_with_rationale` sets the one-way `waiver_status` latch.
7. **Verdict aggregation** (`refs/hardening-output-contract.md`): compute `pipeline_hardening_verdict` ∈ `pass | blocked | advisory | not_applicable | blocked-on-authorization` deterministically from the HC0–HC5 statuses + `waiver_status` per the §5.4 truth table. `FAIL` is sticky; a `latched` waiver forces the verdict into `{blocked, advisory}` and can never be re-greened to `pass`/`success` by a downstream stage. Populate the additive Output Contract fields (see Output Contract above). `blocked-on-authorization` is never produced by this aggregation — it is written by the Wave 1.6 S1.6.4 precedence rule and takes precedence over the §5.4 table when set.

**Exit criteria**: `pipeline_hardening_verdict` computed, `waiver_status` set, the four `*_card_path`/`*_path` fields recorded for every wave that ran, and `known_escapes_caught` populated (membership earned per the anti-inflation rule). The verdict + evidence paths are carried into the Wave 5 report (Pipeline Hardening Closure section). When `applicable=false`, the recorded reason + boundary scan are carried into Wave 5 instead.

---

### Wave 5: Synthesis + Report

**Goal**: Produce one diagnosis report at `<output-dir>/REPORT.md` regardless of which tier ran.

**Steps**:

**Common epilogue and status merge:** every report exit, including cosmetic option (a) invoked in an earlier wave, runs draft composition → validation (or identical inline fallback) → shared post-validation consequence consumer (step 3.25) → final status merge → report/footer → conditional return-contract. No final publication, including fallback/cosmetic exits, precedes step 3.25. Preserve the highest status reached: `failed` > `blocked` > `partial` > `success`. All assignments below are contributions to that merge, never overwrites; validator suggestions, dropped/missing citations, inline fallback and cosmetic finalization cannot lower an existing block/failure. Derive REPORT frontmatter, audit footer and TFEP from this same merged status. For `blocked` or `failed`, recommend `halt`, set insertion path null, remediation target none and solution summary empty; do not recommend a rerun that cannot lift the block.

1. Load `refs/report-template.md` (not before now — lazy load).
2. Compose the draft for `REPORT.md` (not the final publication) filling in:
   - Header (target, tier reached, confidence, escalation reason)
   - Summary (2-4 sentences; if inconclusive, no unique cause established, missing observation and next discriminating action, never a candidate promoted to the answer)
   - Documentation Context (≤6-line summary of the Wave 1.5 Documentation Context Card at `<output-dir>/doc-context.md`; omit this section entirely and add a line to Grounding Gaps when `--no-doc-discovery` was set)
   - Diagnosability Context (≤6-line summary of the Wave 1.6 Diagnosability Context Card at `<output-dir>/diagnosability-context.md`; omit this section entirely and add a line to Grounding Gaps when `--no-diagnosability-audit` was set; when Wave 1.6 hard-stopped, render the section as the hard-stop block from refs/report-template.md instead)
   - Diagnosis (evidence-established hypothesis, or UNDETERMINED for hard-stop/inconclusive/unobserved/both-consistent outcomes; calibration alone is not causal proof)
   - Evidence (cited `file:line` and command outputs). When a discriminator form (refs/hypothesis-card-template.md) is present: first exempt exact `n/a` only with an evidenced per-probe `first_instrumented_run=true`; otherwise `Reference-context value` MUST be one numeric/boolean/null literal or one quoted string. Validator A6 rejects blank values, conditional prose, unquoted alternatives/lists and later-run `n/a`, not slashes or commas inside quoted literal data — compare a literal reference with the actual captured reference arm on any run, including the first. A mismatch marks THAT PROBE `suspect` under Grounding Gaps (A9); skip its outcome table, not refute the hypothesis. A failing-arm mismatch alone does not mark suspect. Skip comparison for evidenced first-run n/a or unobserved reference; neither proves a control. Empty/incomplete/error results remain unobserved and never enter the binary table
   - Proposed Fix (for established diagnosis, the proposed change, including both atoms of a Wave 4 doc-update + fix bundle; otherwise `No causal fix established`, missing observation and next discriminating action, with any proposal explicitly conditional and never promoted to TFEP causal remediation)
   - Alternative Fixes Considered (Tier 2 only — the losing proposals from the debate, with one-line reason each)
   - Risk + Rollback (what to watch after applying)
   - Next Steps: always include pending tasklist rows from any creation path, even if the audit later became sufficient or was bypassed. A blocked/failed status explains the external action required and suppresses automatic rerun/remediation advice. Otherwise an inconclusive run suggests evidence gathering, not causal remediation; a diagnosed Tier 1 run may suggest `--depth deep`, and diagnosed Tier 2 may offer the existing `--fix`/confirmation flow. Preserve optional pending rows without a partial contribution solely from those cells.
   - Pipeline Hardening Closure: first render any `blocked-on-authorization` result, tasklist/refusal evidence and explicit authorization blocker regardless of applicability. If HC0 has not run, state `HC0 not run — applicability unassessed` rather than inventing cards or a not-applicable boundary scan. Preserve that fifth value/blocker downstream per refs/hardening-output-contract.md. Otherwise, when `pipeline_hardening_applicable=true` from Wave 4.5, render `pipeline_hardening_verdict` (`pass | blocked | advisory | not_applicable | blocked-on-authorization`), `waiver_status`, `off_path_review_decision`, the HC0–HC5 evidence-card paths (`runtime_entrypoint_card_path`/`contract_ledger_path`/`unmask_sweep_path`/`effective_input_card_path`), and `known_escapes_caught`; use `NOT PROVEN` blockers when any required proof is absent. When HC0 actually decided `applicable=false` and no authorization result supersedes it, render its one-sentence reason + boundary scan instead. Section template in `refs/report-template.md`.

   **Sprint-failure recovery hint.** When the diagnosed target is a `superclaude sprint run` phase that failed on a *subset* of its tasks from a transient cause (API outage, timeout, rate limit — not a logic defect), the Proposed Fix / Next Steps SHOULD surface `superclaude sprint rerun-tasks <tasklist-index.md> --phase N --tasks T<…>` as the surgical recovery: it re-executes only the named failed tasks and merges results back, instead of re-running the whole phase via `--start N`. Recommend `--dry-run` first to preview the plan, and note `--restore` rolls back a botched merge. (Per-task statuses live in `phase-N-result.json`; tasks classified `fail_recoverable` are the usual candidates.)

   When `--no-doc-discovery` was set, omit the Documentation Context section entirely AND populate the Grounding Gaps section with: "Documentation grounding skipped by `--no-doc-discovery` — diagnosis is not weighted against documented behavior or restrictions."

   When `diagnosability_hard_stop=true`, put the halt explanation in Diagnosability Context, retain UNDETERMINED Diagnosis with empty root_cause_summary and every pending Next Steps row, and follow refs/report-template.md's status/cap/authorization-conditioned advice. Do not replace Diagnosis or render an exclusive Next Steps block. When `--depth deep` is set AND `diagnosability_verdict ∈ {insufficient, partial}`, render the top-of-report Diagnosability Caveat banner above the Summary section (template in refs/report-template.md).

   **Headline-confidence coupling** (every report, hard-stop or not): if calibrated confidence < 0.5 (a missing or non-numeric confidence counts as 0.0) OR the headline value is absent from the captured failing-run observation corpus (`observation_paths`, each bound to a run, arm, command/stream and observed output). Search only captured output spans, including matching job logs; exclude report drafts, hypothesis cards, producer tables, tasklists, behaviour definitions and analysis prose even when embedded in `tier1-observation.md`. Passing-arm output cannot prove a failing-arm value; an empty corpus means unobserved. If either the confidence or observation condition fails, the Diagnosis section MUST use the UNDETERMINED form of refs/report-template.md — it begins `UNDETERMINED — among {<surviving producer identities>}`, including every `surviving=yes` row of producers.md followed by the measurement predictions/outcome mappings copied from `diagnosability-tasklist.md` `## Discriminator rows` when present, preserving consistent/refuted/inconclusive semantics. Use the report template's Core/Optional forms: optional pending cells are informational, not status prerequisites; linked enabling tasks have operational checks rather than invented falsifiers. A both-consistent result without independent discrimination keeps UNDETERMINED regardless of numeric confidence. If no nonempty producer menu exists (including audit bypass), use `UNDETERMINED — producer menu unavailable`; if no tasklist exists, state that no discriminator was emitted and the missing observation, without fabricated rows; the word "probable" before an enum value is forbidden; `root_cause_summary` is the empty string. Sibling forms rendered the same way: `UNDETERMINED — among {a,b}` (tasklist header `indistinguishable: a,b`), `UNDETERMINED — no comparator` (refs/primitive-differential.md Section 2 step 3; orchestrator cap 0.4 on calibrated confidence), `UNDETERMINED — CI verdict unobserved` (validator A8). Agent backstop: validator A1 ⇒ `partial`; validator A8 ⇒ `blocked`; calibrator C1 ⇒ forced ESCALATE (refs/agent-assertions.md). Exactly 0.50 clears only the confidence threshold; a definite headline still requires the observation and causal-discrimination guards. Do not lower the escalation threshold or change the calibrator formula.
2.5. **Materialize validator inputs before spawn** — write `<output-dir>/REPORT.md.draft`. Persist all captured outputs on receipt before citing them. Build `observation_paths` from captured failing-run output spans with run/arm provenance, not generated prose; record evidenced `first_instrumented_run` per discriminator probe (unknown does not earn the exemption). For each cited artifact capture its actual ISO-8601 mtime before dispatch (GNU: `date -u -d "@$(stat -c %Y "<absolute-path>")" +%Y-%m-%dT%H:%M:%SZ`; BSD: `date -u -r "<absolute-path>" +%Y-%m-%dT%H:%M:%SZ`); a missing artifact or missing mtime is a dropped citation, not a fabricated timestamp. Pass null/omit for absent optional producer/tasklist/locus files so skip rules fire.
3. **File:line validation pass (non-negotiable)** — spawn the `evidence-validator` agent via `Task` with `report_draft_path=<output-dir>/REPORT.md.draft`, `evidence_section_locator="## Evidence"`, `output_path=<output-dir>/evidence-validation.md`, `now_iso=<ISO-8601 from this turn's`date -u +%Y-%m-%dT%H:%M:%SZ`>`, `allow_command_reexec=false`, `calibration_paths=[existing current-run calibration artifacts only]`, `diff_path=<path of the instrumentation or fix diff written this run, else null>`, `artifact_mtimes={<abs path>: <ISO-8601 mtime>}` for every `<output-dir>` file the draft cites (captured in step 2.5), `observation_paths=<step-2.5 provenance-bound spans>`, `first_instrumented_run=<per-probe boolean or unknown map>`, `producers_path=<output-dir>/producers.md` (null/omit if absent), `tasklist_path=<output-dir>/diagnosability-tasklist.md` (null/omit if absent), `locus_path=<output-dir>/execution-locus.md` (null/omit if absent), `output_dir=<output-dir>`, `assertions_path=<skill-dir>/refs/agent-assertions.md`. The agent Reads every cited `file:line`, drops mismatches, and returns the verified evidence set plus a `Suggested report status` (success/partial/blocked), merged with prior state per the common epilogue. Pass the entire returned result, not only its suggested status/citation counts, to step 3.25 before final publication. Expand `calibration_paths` to actual existing current-run artifacts (including explicit failure records); record absent/failed calibrations as gaps, never invent a path or confidence. Write `evidence-validation.md` to disk *on receipt* (before modifying the draft or finalizing `REPORT.md`); persist `job-*.log` and `bracket.md` on receipt. The final `REPORT.md` may only cite `<output-dir>` paths that exist on disk at write time: run one `ls <all cited paths>` before writing `REPORT.md` and drop missing cites — this final `ls` is an existence check only, not the mtime source. Metadata capture, the final existence check and report write are exempt from the step 3.5 counter. Every timestamp written into `REPORT.md` or the audit footer is copied from a `date -u +%Y-%m-%dT%H:%M:%SZ` Bash result captured in this same turn (or `git log --format=%cI`), never from memory.
   - **Fallback**: if `evidence-validator` fails (subprocess crash, malformed output, agent unavailable), inline-validate citations in the orchestrator context (the original Wave 5 step 3 behavior) and add a Grounding Gap entry noting the validator was unavailable. Do not assign `status` here — the common-epilogue merge decides. The inline path is the fallback — never ship without validation. The inline path applies the identical A-rule list in `refs/agent-assertions.md` (A1-A10) with the same inputs the spawn would have received and writes the same `## Structural assertions` table into `<output-dir>/evidence-validation.md`.
3.25. **Shared post-validation consequence consumer (agent AND inline)** — Read the persisted validation result and apply EVERY fired row and citation drop to the draft, even with zero dropped citations. Merge the three-value suggested status and each structural contribution with all prior status; keep structural FAIL separate from that enum. Record each disposition in audit/Grounding Gaps, including skipped-input limitations; a missing/malformed result or required table is a validation failure, not success (use step 3 fallback; if inline also cannot validate, take the failed diagnostic disposition below).
   - Remove dropped citations and their unsupported claims; contribute partial. For A1/A2/A4/A5/A10 consume each partial contribution and its gap: suppress unsupported definite headlines/consensus, publish missing linked measurement/pending information when evidenced, and never invent an enum, capture route or causal proof. Reapply step 2's noncausal headline/fix guards to the edited draft.
   - A3: remove the identified invalid timestamp line from the draft wherever it appears, independently of citation removal; do not change source artifacts or substitute an invented timestamp. A8: contribute blocked and make Diagnosis begin `UNDETERMINED — CI verdict unobserved`, retaining that prefix even with structural FAIL or a prior failed status; clear root_cause_summary and causal fix claims.
   - A9: mark the affected probe row suspect in the report, add its reference-mismatch Grounding Gap and suppress that probe's outcome table and dependent causal inference; preserve raw observations as observations. No independent status contribution and no automatic refutation; failing-arm-only mismatch does not trigger this action. Do not mutate the validator's input artifacts to hide the finding.
   - A6/A7: do NOT publish a normal partial/blocked diagnostic while structural FAIL remains. If grounded repair is possible within existing permissions, the orchestrator repairs the literal/reference or locus mapping using actual evidence (an unresolved candidate set is not a fabricated unique site), rematerializes the draft/changed input metadata and re-runs step 3 with identical input semantics. Run the returned result through this SAME consumer; only successful revalidation clears the structural FAIL, never merely changing suggested status or deleting the finding. Permit one repair/revalidation attempt, then use the failed disposition if unresolved or validation fails. Retain all prior status contributions and all other consequences, including A8/A9.
   - **Failed diagnostic disposition** (unrepairable/persistent structural FAIL, exhausted calibration, or unavailable validation): contribute failed, explicitly label the report diagnostic-only with the failure IDs/input gaps, retain only verified noncausal observations and pending work, suppress invalid forms/outcome tables and causal claims across Summary/Diagnosis/Proposed Fix/TFEP, and set root_cause_summary and solution_summary empty. Diagnosis stays UNDETERMINED (A8's prefix wins when applicable); derive halt/null/none for recommendation/insertion/remediation. Preserve evidence-validation failure history, never certify this artifact as validated success or normal partial publication. If even noncausal content cannot be verified, publish only the execution-failure notice and known artifact availability, not an unvalidated diagnostic claim.
   - **Publication barrier**: after all consequences above are applied, ensure no suppressed line/table/claim reappears during rendering, and every retained/new citation has been checked (substantive repairs require the revalidation above). Perform step 3's cited-path existence check first; any new missing citation is removed with its unsupported claim, contributes partial and re-applies the noncausal guards. Then finalize the status merge for REPORT frontmatter/footer/TFEP, write final `REPORT.md` and proceed to step 4. Cosmetic exits and inline results cannot bypass this barrier; revalidation does not reset any prior blocked/failed contribution.
3.5. **Cosmetic-loop counter (a nudge, never a halt)** — run-wide monitor from Wave 1 onward; Wave 5 is the last check. After **5** consecutive `Read`/`Glob` calls on `<output-dir>/` with no Read/Bash on a source file or downloaded artifact, do exactly one of (instead of another cosmetic Read; never a halt):
   - Stop cosmetic work, contribute `partial` to the status merge and continue the current wave into the common epilogue (compose/materialize draft → validate → merge status → report/footer → return-contract), never publish an unvalidated report or skip the footer.
   - Issue one Read/Bash on source or artifact.
   `ls`, `Write`, and persist-on-receipt calls are exempt. Exempt reads inside `<output-dir>`: `job-*.log`, `*.stream.jsonl`, `<output-dir>/artifacts/**`, and any file whose content is written into a probe row. The counter resets on a source/artifact Read or Bash inspection. At the initial threshold and each re-fire audit-log `cosmetic_overrun=<n>`, where n is the consecutive cosmetic-call streak length: 5, then 10, then 15 if no corrective action is taken. This is neither excess over five nor number of events; footer aggregation takes the maximum logged streak. The run continues. The Wave 3 marker verification is a single command run once — a second marker grep in the same wave is a counter hit. Calibration reports are consumed from disk, never re-typed. Never AskUserQuestion; never count reads of the failing artifact as cosmetic; never add a token cap that stops diagnosis mid-wave. May fire in any wave; Wave 5 is the last check.

4. Append the machine-readable footer to the audit log:

```text
<!-- SC:TROUBLESHOOT:SUMMARY
status: <success|partial|blocked|failed>
tier_reached: <1|2|3>
confidence: <float>
escalation_reason: <none|low_confidence|multi_domain|forced_by_depth_deep|intermittent|not_reproducible|security_caution|source_only_dynamic_claim|split_pending>
hypothesis_count: <N>
adversarial_invoked: <bool>
cosmetic_overrun: <n>
fix_authorized: <bool>
duration_sec: <N>
caller: <name|none>
context_path: <abs-path|none>
return_contract_path: <abs-path|none>
-->
```

`cosmetic_overrun` = the highest overrun value logged this run, `0` when the counter never fired.

4.5. **Emit TFEP return-contract (conditional, when `caller=task-unified`)** — write `<output-dir>/return-contract.yaml` mapping the Output Contract fields to the TFEP-consumed schema: `status`, `test_is_wrong`, `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary`. Source the asymmetric-cost gates from `test_is_wrong`/`test_file_path`/`behavior_is_documented`; copy the already-derived `root_cause_summary` from step 2, preserving the empty string for every UNDETERMINED/inconclusive form rather than copying its prose and `solution_summary` from the REPORT.md Proposed Fix / Next Steps; derive `recommended_escalation` from `status`+`tier_reached`+`confidence`. Derivation clarifications: copy `status` from the Output Contract `status` finalized by step 3.25 (values `success|partial|blocked|failed`); use only its post-disposition report content, never a pre-validation draft. Default `tasklist_insertion_path` to `null` in this diagnosis-only TFEP mode — under the remediation-ownership decision the task-protocol composes the `## Failure Remediation Plan (Adjudicated)` block from `remediation_target`/`root_cause_summary`/`solution_summary`, so this field is non-null ONLY if troubleshoot itself wrote a standalone adjudicated remediation-plan file under `<output-dir>/` (do not invent a new mandatory artifact; the default is `null`). `test_file_path` is intentionally NOT duplicated into this 7-field wire set: when `remediation_target=test` the test path remains available via the broader Output Contract / REPORT.md, and the consumer's asymmetric-cost branch presents to the user (it does not auto-fix), so the path need not be in the wire contract. Path-valued fields in the emitted `return-contract.yaml` are ABSOLUTE paths. For `recommended_escalation` use this deterministic tie-break hint: `status=failed` or `status=blocked` or a hard-stop → `halt`; `status=partial` with low confidence → `escalate_depth`; `status=partial` at tier < 2 → `retry`; `status=success` → `none` (the consumer-side action mapping lives in the task-protocol consumer, Phase 5). Record `return_contract_path` in the audit footer (SUMMARY block). NOTE: TFEP invokes troubleshoot for DIAGNOSIS ONLY and does NOT pass `--fix` (per the task-protocol remediation-ownership decision) — this step emits the contract but does NOT apply any remediation. The same fields are ALSO rendered as the `## TFEP Consumer` section of REPORT.md (per `refs/report-template.md`) when `caller=task-unified`.

5. Surface to the user in chat:
   - One-paragraph summary
   - Path to `REPORT.md`
   - The supported fix, or no causal fix established plus next discriminating observation (concise)
   - Tier reached + confidence
   - Next-step recommendation
   - (if `caller=task-unified`) the emitted `return-contract.yaml` path.

**Exit criteria**: `REPORT.md` written, audit log finalized, user notified. If `--fix` is not set, return the output contract and STOP. When `caller=task-unified`, `return-contract.yaml` is written and its path returned.

---

### Wave 6: Tier 3 — Remediation Chain

**Preconditions**: `--fix` is set AND `REPORT.md` is `success` (not `partial`) AND user explicitly accepts the remediation offer.

**Steps**:

1. **Present the remediation offer** to the user — read the prompt template in `refs/remediation-handoff.md`. Ask one yes/no question. Wait.
2. On accept:
   - **Phase A — Build the task file**: invoke the `task-builder` skill via `Skill` with a `BUILD_REQUEST` whose GOAL is "Apply the fix described in `<REPORT.md path>`", WHY is the summary section, WHERE is the cited file(s), and TEMPLATE is generic (template 01) unless the fix involves > 3 files or > 2 hours of work (then template 02).
   - **Phase B — Pre-execution review**: after `task-builder` returns the task file path, invoke `/sc:reflect --type task --analyze` (if available) against the new task file. If reflect flags issues, surface them; ask the user whether to refactor the tasklist or proceed as-is.
   - **Phase C — Execution gate**: do NOT auto-execute. Surface the task file path and the literal command (`/task <path>`) the user can run. Stop here — the user runs it.
   - **Phase D — Post-execution validation** (only if the user reports back after `/task` completion): invoke `/sc:reflect --type task --validate` (or `self-review` agent as fallback) before the user commits.
3. On decline: return success; the report is the final deliverable.

**Exit criteria**: task file path returned (or decline recorded). Output contract finalized.

---

## Tool Coordination Summary

| Tool | Tier 1 | Tier 2 | Tier 3 |
|------|--------|--------|--------|
| `mcp__auggie__codebase-retrieval` | ✓ (one focused query + Wave 1.5 doc-grounding fan-out: 3 parallel branch queries; Wave 1.6 audit fan-out: 2 parallel branch queries (A log-call, B log-config)) | ✓ (per-hypothesis queries) | — |
| `mcp__serena__find_symbol` / `find_referencing_symbols` / `get_symbols_overview` | ✓ | ✓ | — |
| `mcp__context7__query-docs` | Conditional behaviour-definition fetch before S1.6.4 pairs and Tier 1 calibration; same fallback chain as Tier 2 | ✓ when framework/library named; behaviour-definition fetch (Wave 3 step 1; fallback `WebFetch` → raw source fetch, e.g. `gh api`) | — |
| `mcp__tavily__tavily_search` | — | ✓ rate-limited (≤2 queries) | — |
| `mcp__sequential-thinking__sequentialthinking` | — | ✓ for synthesis | — |
| `Task` (agent spawn) | ✓ (root-cause-analyst + confidence-calibrator (C-rule structural assertions via `assertions_path`); Wave 1.6: 2 parallel audit branches A/B + 1 orchestrator synthesis) | ✓ (2-4 hypothesis agents in parallel + per-card confidence-calibrator + evidence-validator at Wave 5 (A-rule structural assertions)) | ✓ (self-review for post-exec) |
| `Skill` | — | ✓ (`sc:adversarial-protocol`) | ✓ (`task-builder`, `/sc:reflect`) |
| `Read` / `Grep` / `Glob` | ✓ (Wave 1.6 Grep/Glob fallback when auggie unavailable) | ✓ | — |
| `Bash` | ✓ (repro when cheap, run via `OBSERVE-VIA` from the execution-locus card; failing-arm job-log fetch; S1.6.4 read-only rows only through the shared authorization/transport gate, never by executing artifact-file access) | ✓ (diagnostic commands) | — |
| `Write` | ✓ (hypothesis + report) | ✓ (hypothesis cards, fix proposals) | — |

## Will Do

- Always run Tier 1 first; respect the "quick first option" contract
- Auto-escalate only when the rubric in `refs/escalation-rubric.md` says so, or when `--depth deep` is set
- Fan out 2-4 specialist agents in parallel in Tier 2, chosen by signal mix
- Use auggie/serena every tier for in-repo grounding; use context7/tavily for relevant Tier 2 enrichment, with the conditional behaviour-definition fetch also permitted in Tier 1 before pair construction or calibration
- Run `/sc:adversarial` only when Tier 2 produces ≥2 competing strong fixes (cap is the Tier-2 agent cap of 4, not a debate min/max of 3) (not when there is consensus — that wastes the debate)
- Run `self-review` after the adversarial merge to catch obvious regressions before reporting
- Validate every `file:line` citation in the report against the real file
- Stop at the natural off-ramp for each tier; never silently proceed to a deeper tier than the user authorized
- Run Wave 1.6 Diagnosability Audit by default; opt-out via `--no-diagnosability-audit` (bypass is logged in REPORT.md header and audit log).
- Halt Waves 1.7–4.5 when `diagnosability_verdict=insufficient` AND `issue_complexity=non-trivial` AND `--no-escalate` is not set (sets `diagnosability_hard_stop=true` and `status=partial`, or `status=blocked` per the S1.6.4 precedence rule; hardening does not run on diagnosability hard-stop).
- Emit an instrumentation tasklist at `<output-dir>/diagnosability-tasklist.md` instead of hypothesis work when the hard-stop fires — no hypothesis work happens in the same turn as an instrumentation patch; the user re-runs after instrumenting.

## Will Not Do

- Apply code changes without `--fix` and explicit user confirmation
- Skip Tier 1 and jump straight to Tier 2 (even with `--depth deep`, Tier 1 still runs first — it's cheap and its output feeds Tier 2)
- Spawn Tier 2 hypothesis agents on consensus single-domain Tier 1 results
- Spawn more than 4 hypothesis agents in Tier 2 (token waste; signal already saturated)
- Call tavily without a focused query (the rate cap exists for a reason)
- Trust agent-reported confidence without independent re-grading (the `confidence-calibrator` agent or the inline fallback applies the rubric in a fresh context)
- Ship a `REPORT.md` whose `file:line` citations have not passed through `evidence-validator` (or the inline fallback)
- Auto-execute the Tier 3 task file — that is always a separate user-initiated `/task` invocation
- Auto-commit after Tier 3 — `/sc:reflect --type task --validate` is the final gate the user runs before committing
- Auto-apply the diagnosability tasklist — it is a proposal that requires user review (opt-in MDTM packaging via `--diagnosability-handoff` invokes `task-builder` against the tasklist).
- Force the Wave 1.6 hard-stop when `--no-escalate` is set — the flag suppresses the hard-stop and downgrades it to a soft-warn while still emitting the tasklist informationally.
- Allow the diagnosability tasklist to target the failing component's own source code — every task MUST target an invocation site (test script, CI workflow YAML, dev harness, container entrypoint, dev-mode config override). Diagnostic code in production source leaks into release artifacts.
- Spend 5 consecutive `Read`/`Glob` calls on `<output-dir>/` without one Read/Bash on a source file or downloaded artifact — the cosmetic-loop counter (run-wide from Wave 1; Wave 5 step 3.5 is the last check) fires after 5 consecutive, re-fires at 10, 15. Forces exactly one of: stop cosmetic work and enter the common validation/status/footer/return epilogue with a `partial` contribution, or one source/artifact inspection. Exempt: `ls`, `Write`, persist-on-receipt calls, and reads of `job-*.log`, `*.stream.jsonl`, `<output-dir>/artifacts/**`, or any file whose content is written into a probe row.
- Halt a wave on the cosmetic counter or on any token cap — an overrun is audit-logged as `cosmetic_overrun=<n>` at every multiple of 5 and the run continues; the counter is a nudge, not a gate.
- Re-type a calibration report into context, or grep the calibration markers a second time in the same wave — reports are consumed from disk; the Wave 3 marker verification is one command, run once.
- Infer consent from `re-run permitted: unknown` or from a missing approval — never AskUserQuestion; unknown maps to pending rows, not `blocked-on-authorization`.
- Write a timestamp into any artifact from memory or from a model-generated value — every timestamp is copied from a `date -u +%Y-%m-%dT%H:%M:%SZ` Bash result in the same turn or from `git log --format=%cI`, no other source; evidence-validator (A3) and confidence-calibrator (C5) drop any `Timestamp|Date|pushed_at` line later than the artifact mtime + 5 min or equal to `T00:00:00Z` as `timestamp_invalid`.

## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| All MCPs unavailable | Run in `--no-mcp` mode; warn user that triage quality is degraded; native tools only | None |
| auggie unavailable (others OK) | Fall back to `Grep` + `Glob` for grounding; mark in audit | None |
| auggie unavailable in Wave 1.5 (others OK) | Fall back to `Grep`/`Glob` against the per-branch query targets (`.dev/releases/`, `docs/`, `<scope>`); mark `degraded: true` per branch; do NOT block the Tier 1 hypothesis | None |
| All three Wave 1.5 branches return empty / no-hit | Write Documentation Context Card with "None found" in every section; set `doc_context_card_path` to the (still-emitted) empty card; mark `behavior_is_documented` derivation as `no_docs_found` candidate | None |
| `--no-doc-discovery` set by user | Skip Wave 1.5 entirely; emit `doc_context_card_path: null`; record skip-line in Wave 5 Grounding Gaps | None |
| root-cause-analyst agent fails in Tier 1 | Skill produces a degraded Tier 1 (Claude inline) and recommends `--depth deep` | None |
| All Tier 2 agents fail | Downgrade to Tier 1 result; report `partial`; recommend rerun | None |
| `sc:adversarial-protocol` fails in Wave 4 | Pick the highest-confidence Tier 2 fix proposal as the chosen fix; note in audit and report header | None |
| `self-review` flags blocker on adversarial merge | STOP at Wave 5 with `partial` status; report includes the blocker; recommend rerun with `--depth deep` or different focus | None |
| `task-builder` unavailable in Wave 6 | Surface the fix proposal path; recommend manual task creation; don't fail the whole skill | None |
| User declines remediation offer | Return success; report stands | None |
| `--depth deep` requested on under-specified input | STOP at Wave 0; ask user to add detail | None |
| `evidence-validator` agent fails (subprocess crash, timeout, or malformed report) | Inline-validate citations in the orchestrator context (the original Wave 5 step 3 behavior); add a Grounding Gap entry noting the validator was unavailable; do not assign `status` (common-epilogue merge decides) | None — the inline path is the fallback |
| `confidence-calibrator` agent fails for any card | Use Wave 1.7's full-schema persisted inline fallback and the shared calibration receipt/failure ladder; preserve known bounds/C1; terminal failure routes to the failed diagnostic epilogue, never escalation from a missing calibration | One retry per shared ladder |
| `--no-diagnosability-audit` set | Skip Wave 1.6 entirely | Emit `diagnosability_verdict: unknown`, `diagnosability_context_card_path: null`, `diagnosability_hard_stop: false`; log the bypass in REPORT.md's header AND the audit log |
| Auggie unavailable (Wave 1.6) | Fall back to Glob/Grep per refs/diagnosability-audit.md Section 2 | Set Branch A/B `degraded: true`; cap verdict at `partial` (never `sufficient`) |
| Both Wave 1.6 branches return empty | Cannot compute 3-W's coverage | Set verdict = `insufficient` if complexity non-trivial; `partial` if trivial; surface in Grounding Gaps |
| `failing_component` not localizable (Wave 1.6) | S1.6.0 cannot identify the smallest failing component | Set verdict = `unknown`; add Grounding Gaps line; continue to Wave 1.7 without hard-stop |
| Heisenbug detected on Wave 1.6 re-run | Instrumentation altered timing — bug no longer reproduces | Downgrade next-round tasklist to env-vars-only (no `--debug` flag changes, no log-level overrides); record Heisenbug finding in audit card |
| 3-round diagnosability cap reached for a counter key | Authoritative counter at `<repo-root>/.dev/troubleshoot/diagnosability-rounds.json` reached 3 tasklists with `discriminator-required: yes` for the same `<branch>:<repro-venue-id>` (digits stripped) | Write the tasklist anyway; emit the 3-round cap message (refs/report-template.md hard-stop variant + cap-specific prose) with `status: blocked`; suppress the re-run recommendation (not the file) until `--reset-diagnosability-rounds` is set |

## Token Cost Profile

| Tier reached | Auggie tokens (offloaded) | Claude tokens (orchestration + agents) | Wall clock |
|--------------|---------------------------|----------------------------------------|------------|
| Tier 1 only | ~2-5k | ~3-6k | 1-3 min |
| Tier 2 (no adversarial) | ~5-15k | ~15-30k | 4-7 min |
| Tier 2 (with adversarial) | ~10-25k | ~30-60k | 8-15 min |
| Tier 3 added | +0 (auggie not used) | +20-40k (task-builder) | +5-10 min |
| Wave 1.6 added | +1-2k auggie | +1-2.5k Claude | +30-60s wall clock |

These are targets, not hard caps. The cosmetic counter is a non-blocking threshold, never a hard cap; overrun is audit-logged as `cosmetic_overrun=<n>` and the run continues. Auggie tokens are offloaded to a free / low-cost retrieval tier; Claude tokens are the constrained resource. The escalation gate exists specifically to keep the Tier-1-only path inside the 3-9k Claude-token band for the common case. (Wave 1.6 hard-stop case yields a net token *saving* vs the full Tier 2 path — early halt prevents Tier 2 hypothesis-round token spend on blind code.)

## Refs

| File | When loaded |
|------|-------------|
| `refs/escalation-rubric.md` | Wave 2 (confidence gate) and Wave 1.7 (calibration) |
| `refs/triage-checklist.md` | Wave 1 (real-code grounding load) AND Wave 1.7 (passed to root-cause-analyst as part of the brief) |
| `refs/doc-discovery.md` | Wave 1.5 (documentation grounding — Auggie query templates, currency-check procedure, output schemas, Documentation Context Card template) |
| `refs/hypothesis-card-template.md` | Wave 1.7 and Wave 3 (passed to agents) |
| `refs/report-template.md` | Wave 5 |
| `refs/remediation-handoff.md` | Wave 6 |
| `refs/diagnosability-audit.md` | Wave 1.6 (audit query templates, fallback paths, sufficiency rubric, complexity gate, context card template, tasklist rules + hard constraints, T4 worked example) |
| `refs/pipeline-hardening-closure.md` | Wave 4.5 (mode skeleton, HC0 applicability + boundary-scan schema, HC5 off-path-reviewer rule) |
| `refs/hardening-output-contract.md` | Wave 4.5 (verdict-aggregation truth table, output-contract field schema, waiver / no-re-greening latch) |
| `refs/runtime-entrypoint-verification.md` | Wave 4.5 (HC1 runtime-entrypoint card + negative-witness rule) |
| `refs/contract-enumeration.md` | Wave 4.5 (HC2 contract ledger + empty-ledger FAIL + sibling sweep) |
| `refs/unmask-and-sweep.md` | Wave 4.5 (HC3 classifier + allow-list grammar + word-boundary/near-miss fixtures) |
| `refs/effective-input-proof.md` | Wave 4.5 (HC4 fail-closed effective-input manifest) |
| `refs/primitive-differential.md` | Wave 1.6 S1.6.4 discriminator rows (probe-form table copied per surviving producer) and S1.6.0b source-expression classification (no pattern column) |
| `refs/agent-assertions.md` | Wave 1.7 / Wave 3 (passed to `confidence-calibrator` as `assertions_path`) and Wave 5 (passed to `evidence-validator`; read by the orchestrator's inline fallback) |
| `refs/probe-packs/read-parse.md` | Wave 1.6 S1.6.4, only when a `surviving=yes` producer's primitive kind is `read/parse` — **optional**, informational, never a decision input |
| `refs/environment-deltas.md` | Wave 1 step 1b, only when the locus card derives `SAME-ENV ≠ yes` — **optional**; absent ⇒ audit line `optional_ref_absent`, no Grounding Gap |
| `refs/probe-packs/<kind>.md` | Wave 1.6 S1.6.4, only when a `surviving=yes` producer's primitive kind matches `<kind>` — **optional**, informational, never a decision input |

Each ref is loaded only by the wave that needs it. Do not pre-load.
