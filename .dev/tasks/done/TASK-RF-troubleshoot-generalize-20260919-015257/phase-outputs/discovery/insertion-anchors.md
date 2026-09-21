# Insertion anchors (item 0.8)

Each seam's `old_string` is the live line at the cited line number in the worktree (or a unique substring for named seams).
Count = `str.count` of that needle in the file.

| file | seam id | old_string (verbatim, truncated) | count | note |
|---|---|---|---|---|
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:43 | \| `status` \| string \| `success`, `partial` (some findings dropped for grounding), `failed` \| | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:62 | \| `contract_version` \| semver string \| Output-contract semver, default `1.1.0`. Additive version stamp for the Pipeline Hardening Closure | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:63 | \| `pipeline_hardening_applicable` \| bool \| `true` when Wave 4.5 H0 classifies the issue as a pipeline escape / boundary change; default ` | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:64 | \| `pipeline_hardening_verdict` \| enum `pass \\| blocked \\| advisory \\| not_applicable` \| Deterministic aggregation of the H0–H5 statuse | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:67-71 | \| `off_path_review_decision` \| enum `required \\| performed \\| waived_with_rationale \\| not_required` \| Wave 4.5 H5 off-path-review dec | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:73 | \| `recommended_escalation` \| enum `none\\|retry\\|escalate_depth\\|halt` \| TFEP adapter field (contract v1.1.0+). Forward-looking recomme | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:77 | \| `solution_summary` \| string \| TFEP adapter field (contract v1.1.0+). One-to-three sentence proposed-solution summary, extracted from th | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:97 | Wave 1: Tier 1 — Real-Code Grounding  ← always; loads refs/triage-checklist.md on demand (grounding + reproduce only) | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:104 | Wave 4.5: Pipeline Hardening Closure ← conditional, when pipeline_hardening_applicable=true (issue topology); runs gates H0-H5; loads the 6  | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:106 |                                     Wave 1.6 hard-stop edge: → Wave 5 (skip Waves 1.7-4); sets diagnosability_hard_stop=true and status=part | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:167/168 |    - If `--no-mcp` or both MCPs are unavailable: fall back to `Glob` + `Grep` on the issue keywords; note the fallback in the audit log. | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:168 | 2. **Reproduce or observe** (when feasible and cheap): | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:230 | 1. **S1.6.0 — Component identification**. Before any branch fan-out, identify the smallest component whose output the failure asserts agains | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:240 | 5. **S1.6.4 — Apply sufficiency rubric + complexity gate**. Compute `diagnosability_verdict ∈ {sufficient \| partial \| insufficient \| unkn | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:241 |    - `insufficient` AND `non-trivial` AND NOT `--no-escalate` → **hard-stop**: emit `diagnosability-tasklist.md`, set `diagnosability_hard_s | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:248 | **Per-defect patch-round counter**: the Wave 1.6 orchestrator maintains `<output-dir>/diagnosability-rounds.json` keyed by the Wave 0 `issue | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:255 | - Emit `Wave 1.6 complete: verdict=<v> complexity=<c> hard_stop=<bool> round=<N>/3`. | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:266 | \| 3-round diagnosability cap reached for an `issue_slug` \| Per-defect counter at `<output-dir>/diagnosability-rounds.json` reached 3 hard- | 2 | cap-row duplicate SKILL:266==:570 |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:280 | 1. **Form one hypothesis** — spawn the `root-cause-analyst` agent via `Task` with a focused brief: the symptom, the grounding from Wave 1 st | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:281 | 2. **Calibrate confidence (independently)** — spawn the `confidence-calibrator` agent via `Task` with `card_path=<output-dir>/tier1-hypothes | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:282 |    - **Fallback**: if `confidence-calibrator` fails (subprocess crash, malformed output, agent unavailable), fall back to inline orchestrato | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:336 |    - `mcp__auggie__codebase-retrieval` with a more targeted query than Tier 1 (e.g. "find every call site of `<symbol>` and how they handle  | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:342 |    - An instruction to produce **at most one proposed fix** with: claim, evidence (cited file:line or command output), proposed fix, confide | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:345 | 3.5. **Calibrate each card independently** — spawn N `confidence-calibrator` instances in parallel (one per Tier 2 card), each with `card_ti | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:346 | 4. **Distill candidate fixes**: cluster the hypothesis cards by proposed fix. If 2 or more agents propose substantively different fixes, mar | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:348 | #### Tier 2 calibration completeness gate (hard precondition for report publishing) | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:358 | Verification command (run before publishing): for each `tier2-*-hypothesis.md` (excluding `*-calibration.md`), assert a matching `*-calibrat | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:372 | \| All agents converge with high confidence \| Skip Wave 4 (adversarial); jump to Wave 5 \| None \| | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:381 | **Preconditions**: Wave 3 marked ≥ 2 fixes as `competing` (or `--depth deep` + ≥ 2 distinct proposals, even if consensus). | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:408 | **Goal**: When the diagnosed issue is a *pipeline escape* (a defect at a runtime / generated-artifact / shared-contract / review-input bound | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:410 | **Trigger**: Topology-driven, **not** a CLI flag (NFR-5). This wave runs after Tier-1 diagnosis is settled (and after any Tier-2 waves) and  | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:414-420 | 1. **H0 — Applicability + mechanism** (`refs/pipeline-hardening-closure.md`): emit the typed boundary-scan rows, a feature-agnostic mechanis | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:439 |    - Evidence (cited `file:line` and command outputs) | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:444 |    - Pipeline Hardening Closure (only when `pipeline_hardening_applicable=true` from Wave 4.5): render `pipeline_hardening_verdict` (`pass`/ | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:450 |    When `diagnosability_hard_stop=true`, replace the Diagnosis section with a "Halted — instrumentation required" prose block referencing th | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:451 | 3. **File:line validation pass (non-negotiable)** — spawn the `evidence-validator` agent via `Task` with `report_draft_path=<output-dir>/REP | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:452 |    - **Fallback**: if `evidence-validator` fails (subprocess crash, malformed output, agent unavailable), inline-validate citations in the o | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:457 | status: <success\|partial> | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:460 | escalation_reason: <none\|low_confidence\|multi_domain\|forced_by_depth_deep\|intermittent> | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:462 | adversarial_invoked: <bool> | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:509 | \| `mcp__context7__query-docs` \| — \| ✓ when framework/library named \| — \| | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:512 | \| `Task` (agent spawn) \| ✓ (root-cause-analyst + confidence-calibrator; Wave 1.6: 2 parallel audit branches A/B + 1 orchestrator synthesis | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:515 | \| `Bash` \| ✓ (repro when cheap) \| ✓ (diagnostic commands) \| — \| | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:529 | - Halt Waves 1.7-4 when `diagnosability_verdict=insufficient` AND `issue_complexity=non-trivial` AND `--no-escalate` is not set (sets `diagn | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:545 | - Allow the diagnosability tasklist to target the failing component's own source code — every task MUST target an invocation site (test scri | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:570 | ## Token Cost Profile | 1 | 570 is byte-duplicate of 266; region marker unique |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:582 | These are targets, not hard caps. Auggie tokens are offloaded to a free / low-cost retrieval tier; Claude tokens are the constrained resourc | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:595-600 | \| `refs/pipeline-hardening-closure.md` \| Wave 4.5 (mode skeleton, H0 applicability + boundary-scan schema, H5 off-path-reviewer rule) \| | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md | SKILL:600 | \| `refs/effective-input-proof.md` \| Wave 4.5 (H4 fail-closed effective-input manifest) \| | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md | da:150 | \| **S13**: Intermittent keywords present AND 3-W's `when_answerable != yes` \| `insufficient` (intermittent-with-no-trace short-circuit) \| | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md | da:242-247 | ### Hard constraints (non-negotiable) | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md | da:247 | 4. **Revert annotation**: Patches added by the tasklist carry the comment `# Diagnosability-tasklist instrumentation: revert after defect cl | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md | da:255 | - **Add env override OR add fixture wrapper OR wrap subprocess.run**: the concrete code change (additive, invocation-site-only, with the rev | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md | da:263 | **Verdict**: <verdict>  **Complexity**: <complexity>  **failing_component**: <path>  **Round**: <N> of 3 | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md | da:260-278 | ### Worked tasklist skeleton | 1 | unique heading for Task 6 region |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md | da:284 | The orchestrator maintains a per-defect counter at `<output-dir>/diagnosability-rounds.json` keyed by Wave 0 `issue_slug`. The counter incre | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md | da:338 | ## Loading discipline | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md | hct:32 | **Consistency with docs**: <aligned \| conflicts \| not_applicable \| no_docs_found> | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md | hct:44 | - `path/to/test_file.py:88` — the failing test that exercises this code path | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md | hct:80-82 | ## Falsification standard | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md | hct:91 | Filling rule: an empty or "Not applicable" value on `evidence_class` is a defect; cards with `claim_class: runtime_behavior` AND `evidence_c | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md | hct:118-123 | ## Filling the card | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md | rt:67 | The single chosen hypothesis. Format: | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md | rt:73 | **Detailed explanation**: 1–2 paragraphs. Why this code produces the observed symptom. Reference the evidence section, don't restate it. | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md | rt:161 | status: <success\|partial\|failed> | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md | rt:230-235 | - **H0 Applicability + Boundary Scan**: <PASS\|FAIL\|N/A> — <one-line> | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md | rt:316 | - **Emit `NOT PROVEN` blockers for absent required proof.** When the verdict is `blocked` (any H1–H5 `FAIL`, a latched waiver with a mandato | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md | triage:44 | If none of these are available, the hypothesis card is marked `unverified` and the confidence dimension "Evidence grounding" is scored 0.0. | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md | rub:69 |    - `claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_check < 0.5` → ESCALATE (`escalation_reason: source_only_dynamic | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md | hoc:13 | \| `contract_version` \| semver string \| yes \| `1.0.0` \| non-null \| FR-13 \| Treat missing as legacy contract; do not infer hardening pa | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md | hoc:25 | `contract_version` is the **contract semver** (default `1.0.0`); it is monotonic and additive-only within a major version. It is **distinct  | 1 |  |
| src/superclaude/agents/confidence-calibrator.md | cal:51 | - `output_path`: where to write your calibration report | 1 |  |
| src/superclaude/agents/confidence-calibrator.md | cal:62 | 5a. **Apply the verdict-direction modifier** per the rubric: when `claim_class: runtime_behavior` and `runtime_check < 1.0`, cap calibrated  | 1 |  |
| src/superclaude/agents/confidence-calibrator.md | cal:88-96 | \| Step \| Value \| Notes \| | 1 |  |
| src/superclaude/agents/confidence-calibrator.md | cal:108 | - **Reason**: `none` \| `low_confidence` \| `multi_domain` \| `intermittent` \| `not_reproducible` \| `forced_by_depth_deep` \| `security_ca | 1 |  |
| src/superclaude/agents/confidence-calibrator.md | cal:111-115 | ## Notes | 1 |  |
| src/superclaude/agents/evidence-validator.md | val:44 | - `allow_command_reexec`: bool, whether you may re-run cited commands. Default and recommended: `false`. Only `true` when the orchestrator h | 1 |  |
| src/superclaude/agents/evidence-validator.md | val:55 |    - Verdict per citation: `verified` / `line-mismatch` / `file-missing` / `snippet-mismatch`. | 1 |  |
| src/superclaude/agents/evidence-validator.md | val:63-97 | ```markdown | 1 |  |
| src/superclaude/agents/evidence-validator.md | val:72 | **Suggested report status**: <success \| partial> | 1 |  |
| src/superclaude/agents/evidence-validator.md | val:99-103 | ## Status Decision | 1 |  |
| src/superclaude/commands/troubleshoot.md | cmd:69 | 4. **On skill return**, surface: REPORT path, tier reached, confidence, chosen fix, (if `--fix`) the Tier 3 remediation offer, and (if `pipe | 1 |  |
| src/superclaude/commands/troubleshoot.md | cmd:103 | - **`Bash`**: cheap reproducer commands (Tier 1) and diagnostic commands (Tier 2) | 1 |  |
| tests/troubleshoot/test_hardening_verdict.py | tv:51 |     assert "pass \| blocked \| advisory \| not_applicable" in OC | 1 |  |
| tests/troubleshoot/test_hardening_h1.py | th1:46 |     assert "satisfy h1" in low | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md | da:complexity-signal (R-15) | ## Section 5: Complexity gate | 1 | unique heading |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md | rt:rendering-rules (R-13) | The **Pipeline Hardening Closure** section (inside the template block) renders the Pipeline Hardening Closure mode's verdict and evidence. | 1 | unique R-13 body at RT:312 |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md | triage:refuse-clause | refuse | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md | triage:cause-class (R-15) | ## Cause-class scan | 1 | unique heading |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md | hoc:enum-rows 43-48 | pass \| blocked \| advisory \| not_applicable | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md | hoc:rename-set (D11) | Once `latched`, `pipeline_hardening_verdict ∈ {blocked, advisory}` and no later | 1 | HOC:68 preserve-baseline |
| .pre-commit-config.yaml | pre-commit:fixtures-exclude | tests/troubleshoot/fixtures/.* | 1 |  |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md | rename-only:pipeline-hardening-closure.md | # Pipeline Hardening Closure | 1 | unique H1 title |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md | rename-only:unmask-and-sweep.md | # Unmask and Sweep (H3) | 1 | unique H1 title |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md | rename-only:runtime-entrypoint-verification.md | # Runtime-Entrypoint Verification (H1) | 1 | unique H1 title |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md | rename-only:contract-enumeration.md | # Contract Enumeration (H2) | 1 | unique H1 title |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md | rename-only:effective-input-proof.md | # Effective-Input Proof (H4) | 1 | unique H1 title |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/primitive-differential.md | NEW:primitive-differential.md | (file absent) | 0 | ABSENT — safe to create |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/agent-assertions.md | NEW:agent-assertions.md | (file absent) | 0 | ABSENT — safe to create |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/environment-deltas.md | NEW:environment-deltas.md | (file absent) | 0 | ABSENT — safe to create |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md | NEW:probe-packs/read-parse.md | (file absent) | 0 | ABSENT — safe to create |
