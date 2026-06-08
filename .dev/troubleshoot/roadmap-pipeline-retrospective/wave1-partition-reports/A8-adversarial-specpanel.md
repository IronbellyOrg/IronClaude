# Partition A8 — Adversarial + Spec Panel Retrospective

**Partition scope:** `v1.7-adversarial/`, `v2.09-adversarial-v2/`, `v2.10-spec-panel-v2/`
**Focus:** Adversarial debate as a gating step — when it has caught real issues vs. rubber-stamped, and the spec-panel relationship.
**Analyst:** retrospective subagent (Wave 1)
**Date:** 2026-05-31

---

## Executive Framing

This partition spans three releases that together implement and harden the `sc:adversarial` debate pipeline plus the closely-coupled `sc:spec-panel` correctness review. The adversarial pipeline is the same machinery the current `superclaude roadmap run` invokes between its `diff` and `merge` steps (`executor.py:2068-2128`), so failures and successes here translate directly to roadmap-pipeline behaviour.

Across the three releases, adversarial review demonstrably caught **at least one critical pipeline-correctness bug** (`--file` flag misuse, file-passing-debate transcript), produced **structurally non-trivial integration of two divergent variants** (v2.09 merge log applied 9 changes with full provenance), and **enforced a convergence-failure-with-fallback workflow** (v2.09 base-selection at 79%, below the 80% threshold). It also surfaces clear failure-mode classes the pipeline still risks today: sycophantic convergence (R1), formulaic compliance with forcing functions ("correctness theater"), shared-assumption blind spots (entire v2.09 motivation), and an empirically-observed "diff-only analysis" structural bias.

The spec-panel relationship is one of upstream-feeder-with-shared-pathology: spec-panel and adversarial debate both operate on differences/disagreements and both miss the same class of bugs (boundary, zero-is-valid, pipeline dimensional mismatch), which is why the v2.09 and v2.10 releases were co-designed with a shared cross-cutting analysis.

---

## Findings

### F-A8-001: Adversarial debate caught real critical bug (--file flag misuse)
- **Type:** SUCCESS
- **Pipeline step:** debate (Step 4) — debate transcript surfaced factual error before merge
- **Symptom:** A roadmap pipeline subprocess invocation passing `--file /absolute/path` to `claude -p` was structurally wrong: Claude CLI's `--file` flag is a cloud download mechanism expecting `file_id:relative_path`, not a local-file injector. The adversarial debate on "file passing strategy" identified this as a factual error in the prevailing "Approach A" argument. Approach A scored 8/30; Approach B (inline embedding) scored 22/30 in Round 1, then 25/90 vs 80/90 in the final weighted scoring — a decisive 95% confidence verdict.
- **Root cause (claimed):** Misreading of `claude --help` output and assuming the flag's name (`--file`) implied local-path semantics. Pre-existing executor at `executor.py:68` (per debate transcript) used the incorrect form.
- **Remediation applied:** Switched the executor to inline embedding via `_embed_inputs` (cf. `executor.py:531`, `executor.py:1033-1072`). The current code includes the explicit comment "`--file` is broken (cloud download mechanism, not local file injector)" at line 1033-1034.
- **Outcome:** Fix landed; portability restored. `_embed_inputs` reads files into the prompt with `<file path="...">` labels and warns if combined prompt exceeds the large-prompt threshold (`executor.py:1075-1081`).
- **Still possible today (Auggie check):** NO — Auggie/grep confirms `executor.py:1033` carries the inline-embedding remediation and `executor.py:8-9` documents in module-level comments that "--file is a cloud download mechanism and does not inject local file content." Regression would require deleting these lines and re-adding `--file` to `extra_args`.
- **Source artifacts:** `v2.09-adversarial-v2/adversarial/file-passing-debate/debate-transcript.md` lines 1-359; current `src/superclaude/cli/roadmap/executor.py:8-9,531,1033-1072`.

---

### F-A8-002: Adversarial debate non-converged (79% vs 80% threshold) but still produced shippable merge
- **Type:** REMEDIATION (graceful-failure of convergence gate)
- **Pipeline step:** debate → score (convergence detection); merge proceeded with documented partial status
- **Symptom:** v2.09 adversarial roadmap merge had convergence of 79% — explicitly below the 80% gate (`base-selection.md:3`). Rather than halt, the orchestrator selected Variant 1 (opus) as base on the 7-of-14 score advantage, marked the merge as carrying "Partial" status, and the resulting `test-strategy.md` documents the unresolved contention: "Adversarial convergence: 79% (PARTIAL). Unresolved: X-002 M5 dependency model (62% confidence)" (`test-strategy.md:115`).
- **Root cause (claimed):** The threshold-versus-actual margin (1 percentage point) was within noise. The contested points (X-002, S-002) genuinely had two defensible answers — the debate could not force closure. UNDOCUMENTED whether 80% was empirically calibrated or chosen by convention.
- **Remediation applied:** Documented fallback in the merge artifact (M5 fallback provision "exploratory-grade mode using M1+M4-v0 if M3 is delayed, with mandatory upgrade pass" — `merge-log.md:46-47`). The release shipped without forcing a re-debate.
- **Outcome:** Operational acceptance, but the threshold became advisory rather than enforcing.
- **Still possible today (Auggie check):** YES — current `executor.py:2068-2128` wires debate→score→merge unconditionally; the convergence percentage is computed but the merge step is not gated on it crossing 80%. The `MERGE_GATE` (referenced at `executor.py:2118`) enforces structural completeness, not debate convergence. INFERENTIAL on the gate having no convergence floor: confirmed by reading the gate plumbing in the Auggie excerpt; no `CONVERGENCE_GATE` constant appears in the recovered code.
- **Source artifacts:** `v2.09-adversarial-v2/adversarial/base-selection.md:3,38-42`; `v2.09-adversarial-v2/adversarial/merge-log.md:46-47`; `v2.09-adversarial-v2/test-strategy.md:115`; current `executor.py:2107-2128`.

---

### F-A8-003: Debate surfaced a structural blind spot: "agreement = no scrutiny"
- **Type:** FAILURE (acknowledged in spec; remediation designed)
- **Pipeline step:** diff (Step 3) — diff-only analysis structurally cannot surface shared assumptions
- **Symptom:** v2.09's release-spec section 2.3 documents that the protocol's "entire analytical pipeline — diff analysis, debate rounds, convergence detection, scoring — operates on *differences* between variants. When all variants share an assumption (explicitly or implicitly), that assumption receives zero scrutiny regardless of how critical it is" (`adversarial-release-spec.md:32`). Two real production bugs (Index Tracking Stall, Replay Guard Bypass) escaped because both lived in areas of implicit agreement across all variants.
- **Root cause (claimed):** Three structural factors: diff-only analysis (Step 1), comparative debate (Step 2), agreement-as-convergence metric (`adversarial-release-spec.md:50-56`).
- **Remediation applied:** Designed four AD-* proposals (AD-1 Failure Mode Enumeration, AD-2 Consensus Assumption Extraction, AD-3 Edge Case Scoring, AD-5 Debate Topic Taxonomy). Backward-compat regression report (`backward-compat-regression-report.md`) confirms these landed as additive extensions (e.g., `SKILL.md L792-L890` for shared assumption extraction, L122-L165 for taxonomy).
- **Outcome:** SKILL-level protocol additions are in place per the regression report. Whether they propagate into the **current sc:roadmap-invoked** debate prompt at `prompts.py::build_debate_prompt` is UNKNOWN from this partition's evidence.
- **Still possible today (Auggie check):** YES (partially) — `executor.py:2078-2086` invokes `build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth)` which takes only the diff file as primary input, mirroring the "diff-only" architecture. Whether `build_debate_prompt` internally also asks for shared-assumption extraction (AD-2) was not retrievable in the Auggie excerpt; INFERENTIAL that the structural pattern remains diff-centric.
- **Source artifacts:** `v2.09-adversarial-v2/adversarial-release-spec.md:30-60`; `v2.09-adversarial-v2/tasklist/backward-compat-regression-report.md:76-87`; current `executor.py:2068-2086`.

---

### F-A8-004: Diff-analysis correctly enumerated 14 structural/content/contradiction items across two variants
- **Type:** SUCCESS
- **Pipeline step:** diff (Step 3)
- **Symptom:** v2.09's `diff-analysis.md` produced an 8-row structural diff table, 8-row content diff table, 5-row contradiction table, and 11-row unique-contribution table — 32 enumerated divergences in total, each with severity ratings (Critical/High/Medium/Low). v2.10's diff produced 14 differences. Both diff outputs were structurally consumable by the downstream debate step.
- **Root cause (claimed):** N/A (success).
- **Remediation applied:** N/A.
- **Outcome:** The diff stage produced a high-fidelity catalogue that the debate stage could engage with point-by-point.
- **Still possible today (Auggie check):** YES — `executor.py:2068-2075` wires `build_diff_prompt(roadmap_a, roadmap_b)` to produce `diff_file`. The pattern is structurally the same; whether the prompt template still elicits this richness is UNKNOWN from the Auggie excerpt but the API surface matches.
- **Source artifacts:** `v2.09-adversarial-v2/adversarial/diff-analysis.md:1-91`; `v2.10-spec-panel-v2/adversarial/diff-analysis.md:1-59`; current `executor.py:2068-2076`.

---

### F-A8-005: Merge-executor produced 9 successful integrative changes with provenance + post-merge validation
- **Type:** SUCCESS
- **Pipeline step:** merge (Step 6)
- **Symptom:** v2.09 `merge-log.md` documents 9 distinct changes applied to the base variant. Each change records: source diff ID, before/after state, provenance annotation method (HTML comments), and validation result. Post-merge validation enumerated structural integrity (heading hierarchy, table consistency, YAML frontmatter), internal reference consistency (D1.1-D6.4, R1-R8, SC1-SC8+S9 sequences), contradiction re-scan, and provenance completeness — all PASS (`merge-log.md:85-110`).
- **Root cause (claimed):** N/A.
- **Remediation applied:** N/A.
- **Outcome:** Merge fidelity at this level addresses R3 (Merge Execution Corruption, scored Low-High in v1.7 risk assessment) — confirms the dedicated `merge-executor` agent + post-merge structural validation was a working mitigation.
- **Still possible today (Auggie check):** YES — `executor.py:2107-2128` invokes `build_merge_prompt` and writes to `merge_file` with `MERGE_GATE`. The gate function `_validate_merge_completeness` (`executor.py:856`) confirms structural completeness checking is still in place ("inspect a merge-step output file and return a list of missing or schema-violating items"). Tool-write mode + template (`tool_write_mode=_roadmap_template is not None`) enforces section-by-section tooling, which `executor.py:861-864` notes is needed because the merge step "can be silently truncated if the LLM's turn budget runs out mid-sequence."
- **Source artifacts:** `v2.09-adversarial-v2/adversarial/merge-log.md:1-111`; current `executor.py:856-866, 2107-2128`.

---

### F-A8-006: Risk register R1 (Sycophantic Convergence) — Medium-High, never empirically falsified
- **Type:** REMEDIATION (designed-in mitigations; effectiveness unverified)
- **Pipeline step:** debate (Step 4)
- **Symptom:** v1.7 risk assessment identifies R1 sycophantic convergence (probability Medium, impact High, score 6) as the top risk to monitor. Mitigations enumerated: steelman protocol, "maintain distinct positions" meta-prompt, longer advocate prompts, different personas per advocate, convergence detection at <10% diff (`risk-assessment.md:14-26`). Detection: "Monitor Round 1 agreement rate — if >90% agreement on first round, flag as potential sycophancy."
- **Root cause (claimed):** "Research confirms LLMs exhibit sycophantic agreement, especially same-model debates."
- **Remediation applied:** Mitigations encoded in SKILL.md (per backward-compat report referencing L939-L967 advocate prompt template with ACCEPT/REJECT/QUALIFY).
- **Outcome:** UNKNOWN. The two surviving debate transcripts in this partition (file-passing-debate, v2.09 adversarial-scoring-debate) both show **genuine disagreement** — Agent A vs Agent B disputed multiple dimensions and the debates reached real reconciliation. So in those instances, R1 did NOT manifest. But there is no telemetry artifact showing the "Round 1 agreement rate" detector firing or not firing.
- **Still possible today (Auggie check):** YES — the current pipeline uses the **same** two-model split (opus + sonnet or opus + haiku) that the risk assessment warned about for same-model sycophancy. The cross-model setup is the only documented mitigation actually in place at the orchestration layer; SKILL-level prompt mitigations are inside `build_debate_prompt` which was not retrievable.
- **Source artifacts:** `v1.7-adversarial/risk-assessment.md:14-26`; `v2.09-adversarial-v2/adversarial-scoring-debate.md:1-494`; `v2.09-adversarial-v2/adversarial/file-passing-debate/debate-transcript.md:1-359`.

---

### F-A8-007: Cross-cutting analysis identified "forcing functions outperform analytical enhancements" — pipeline's primary failure mode is omission, not superficiality
- **Type:** SUCCESS (meta-finding from cross-cutting analysis)
- **Pipeline step:** OTHER (post-pipeline retrospective)
- **Symptom:** Cross-cutting analysis (identical content in v2.09 and v2.10 — `cross-cutting-analysis.md:185`) explicitly states: "Proposals that make it structurally impossible to skip reasoning (boundary tables, taxonomy gates, risk categories) consistently outperform proposals that try to make the reasoning deeper (invariant agents, stress tests). This suggests the pipeline's primary failure mode is omission, not superficiality." This crystallises the empirical lesson from v0.04 bugs.
- **Root cause (claimed):** Analysts have limited capacity to go deeper than their prompts; they can be reliably forced to enumerate.
- **Remediation applied:** Phase 1 of cross-cutting roadmap implemented the cheapest, most-forcing changes first (RM-5, SP-2, AD-5, AD-2 — `cross-cutting-analysis.md:159-163`).
- **Outcome:** Frames the bias for all future pipeline-quality work.
- **Still possible today (Auggie check):** N/A (meta-finding).
- **Source artifacts:** `v2.09-adversarial-v2/cross-cutting-analysis.md:181-189`; `v2.10-spec-panel-v2/process-improvement/cross-cutting-analysis.md:181-189`.

---

### F-A8-008: Adversarial scoring debate exposed wide inter-agent score divergence (Composite gaps up to 2.15)
- **Type:** REMEDIATION (debate convergence working as designed)
- **Pipeline step:** score / debate
- **Symptom:** `adversarial-scoring-debate.md` Round 1 found 7 proposals (SP-4, SP-6, AD-1, AD-2, AD-4, RM-1, RM-2) with composite-score deltas > 0.75 between Agent A (Architect/Pragmatist) and Agent B (Quality Advocate). Largest delta: AD-1 at 2.15 points (`adversarial-scoring-debate.md:119`). All seven were contested in Round 2; all seven reached reconciled scores by Round 3.
- **Root cause (claimed):** Two agents with deliberately divergent philosophies. The debate methodology converged them.
- **Remediation applied:** N/A — by design.
- **Outcome:** Demonstrates the debate mechanism works on the meta-level (debating scoring of proposals) just as well as on the object level (debating roadmap variants).
- **Still possible today (Auggie check):** YES — `executor.py:2087-2105` invokes `build_score_prompt(debate_file, roadmap_a, roadmap_b, ...)` which produces `score_file`. The mechanism is in place.
- **Source artifacts:** `v2.09-adversarial-v2/adversarial-scoring-debate.md:88-123,336-358`.

---

### F-A8-009: Spec-panel diff identified a single contradiction (X-001 SP-4 dependency on SP-1)
- **Type:** SUCCESS
- **Pipeline step:** diff (Step 3) — spec-panel variant
- **Symptom:** v2.10 spec-panel diff-analysis reduced to 4 structural diffs, 5 content diffs, 1 contradiction (X-001 SP-4 dependency), 4 unique contributions — 14 items total (`diff-analysis.md:5-7`). The single contradiction was correctly flagged as "High" severity because it directly affected execution parallelism and critical-path length.
- **Root cause (claimed):** Spec ambiguity — "Phase 3 items share dependencies on Phase 1+2 but the spec does not mandate M5 depends on M4."
- **Remediation applied:** Base-selection resolved by selecting V1 (opus:scribe) on a 10.9% combined-score margin (`base-selection.md:69-76`) — well above the 5% tiebreaker threshold.
- **Outcome:** Clean variant selection, no fallback needed (contrast with v2.09's 79% convergence).
- **Still possible today (Auggie check):** YES — same `build_diff_prompt` → `build_score_prompt` mechanism. Confirms the spec-panel-vs-adversarial pipelines share infrastructure.
- **Source artifacts:** `v2.10-spec-panel-v2/adversarial/diff-analysis.md:1-59`; `v2.10-spec-panel-v2/adversarial/base-selection.md:1-96`.

---

### F-A8-010: Test-strategy generation correctly threaded convergence-failure status into downstream artifact
- **Type:** SUCCESS
- **Pipeline step:** test-strategy (Step 8)
- **Symptom:** v2.09 test-strategy YAML frontmatter records `validation_philosophy: continuous-parallel`, `interleave_ratio: "1:2"`, `complexity_class: MEDIUM`, and the final line of the file documents the unresolved adversarial contention from the merge step (`test-strategy.md:115` — "Adversarial convergence: 79% (PARTIAL). Unresolved: X-002 M5 dependency model (62% confidence).").
- **Root cause (claimed):** N/A.
- **Remediation applied:** N/A.
- **Outcome:** The test strategy authors explicitly built a regression-input pair (Index Tracking Stall, Replay Guard Bypass) targeting the bugs that escaped v0.04 (`test-strategy.md:101-111`). This is the planning-stage validation that demonstrates the entire spec-panel + adversarial co-design correctly back-tested against the bugs that motivated it.
- **Still possible today (Auggie check):** YES — `executor.py:2139-2156` wires test-strategy as Step 8 with the merge_file and extraction as inputs. Whether the prompt template still propagates convergence-failure metadata is UNKNOWN.
- **Source artifacts:** `v2.09-adversarial-v2/test-strategy.md:1-116`; current `executor.py:2139-2156`.

---

### F-A8-011: Backward-compat regression report PASSED 8/8 invariants after Phase 2 additions
- **Type:** SUCCESS
- **Pipeline step:** OTHER (release verification — adversarial SKILL.md update)
- **Symptom:** `backward-compat-regression-report.md` verified all 8 canonical invocations (Mode A 2-10 files, Mode B with agent specs, depth flags, conflict errors) still routed correctly after adding pipeline-mode, shared-assumption extraction, A-NNN promotion, ACCEPT/REJECT/QUALIFY advocate template, three-level taxonomy, taxonomy coverage gate, and convergence-formula update. Phase 2 additions explicitly gated behind `pipeline_mode == false` or `pipeline_mode == true` (`backward-compat-regression-report.md:76-87`). Return contract verified all 9 mandatory fields present.
- **Root cause (claimed):** N/A.
- **Remediation applied:** N/A.
- **Outcome:** Demonstrates that the discipline of "gate new behavior behind a mode flag and additive sub-steps" successfully prevented regressions in 8 routing paths. Template for safe protocol evolution.
- **Still possible today (Auggie check):** N/A (process artifact). The mechanism (gate-and-additive) is reusable.
- **Source artifacts:** `v2.09-adversarial-v2/tasklist/backward-compat-regression-report.md:1-129`.

---

### F-A8-012: Risk R2 (Quantitative Metrics Inconsistency) — designed mitigations include deterministic grep/regex
- **Type:** REMEDIATION (designed; effectiveness depends on implementation)
- **Pipeline step:** score (Step 5)
- **Symptom:** R2 (probability Medium, impact Medium, score 4) flagged that the 5 quantitative metrics (RC, IC, SR, DC, SC) "require text analysis that may produce different results on different artifact types (specs vs. roadmaps vs. code). Vague/concrete statement classification (SR) is particularly subjective" (`risk-assessment.md:28-39`).
- **Root cause (claimed):** LLM-judgment in a quantitative-claiming step.
- **Remediation applied:** "Use deterministic grep/regex patterns for quantitative layer (no LLM judgment)" and "Run scoring twice on same inputs — quantitative scores must be bit-identical" (`risk-assessment.md:35-39`).
- **Outcome:** v2.10's base-selection table (`base-selection.md:5-12`) reports quantitative scores like RC=0.95, IC=1.00, SC=1.00 — but with no evidence shown that these were produced by deterministic regex vs. LLM-judged. INFERENTIAL: the score values look round/coarse (0.95, 0.85, 0.82, 1.00) which is consistent with LLM-coarse output rather than fine-grained regex counts.
- **Still possible today (Auggie check):** YES — `executor.py:2087-2105` invokes `build_score_prompt` which delegates scoring to a Claude subprocess (not a deterministic Python scorer). The mitigation "use deterministic grep/regex" was not preserved in code architecture.
- **Source artifacts:** `v1.7-adversarial/risk-assessment.md:28-39`; `v2.10-spec-panel-v2/adversarial/base-selection.md:5-12`; current `executor.py:2087-2105`.

---

### F-A8-013: Risk R7 (Scope Creep into Domain-Specific Validation) — explicit out-of-scope discipline
- **Type:** REMEDIATION (designed; sustained discipline)
- **Pipeline step:** merge (Step 6) / certify (terminal)
- **Symptom:** R7 warned the merge-executor agent might add "domain-specific validation (e.g., 'is this roadmap technically feasible?') during merge execution. Spec explicitly excludes this" (`risk-assessment.md:94-99`).
- **Root cause (claimed):** Helpful-LLM bias.
- **Remediation applied:** "Strict adherence to spec boundaries — sc:adversarial validates process and structure, not domain correctness." Merge-log post-merge validation explicitly includes "No content added that was not specified in the refactoring plan" (`merge-log.md:105`).
- **Outcome:** v2.09's merge ran cleanly within scope; no documented domain-creep findings.
- **Still possible today (Auggie check):** YES — `_validate_merge_completeness` (`executor.py:856`) checks structural completeness but does not check "no content additions beyond the plan." The structural check is the operational replacement for the discipline check.
- **Source artifacts:** `v1.7-adversarial/risk-assessment.md:94-99`; `v2.09-adversarial-v2/adversarial/merge-log.md:105`; current `executor.py:856-866`.

---

### F-A8-014: Spec-panel + adversarial = co-designed, shared cross-cutting analysis
- **Type:** SUCCESS (pipeline-relationship finding)
- **Pipeline step:** OTHER (release coordination)
- **Symptom:** Both v2.09 (`cross-cutting-analysis.md`) and v2.10 (`process-improvement/cross-cutting-analysis.md`) contain the **identical** cross-cutting analysis document — 193 lines of synergies, conflicts, dependency map, MVI sets across all 15 SP/AD/RM proposals. The clusters in §1 explicitly chain spec-panel proposals (SP-1..SP-4) with adversarial proposals (AD-1, AD-2, AD-5) and roadmap proposals (RM-1, RM-3, RM-4) — e.g., Cluster A "Force Invariant Reasoning About State" combines SP-1+SP-3+AD-1+RM-1+RM-4.
- **Root cause (claimed):** N/A (intentional design).
- **Remediation applied:** N/A.
- **Outcome:** Confirms the spec-panel and adversarial debate were treated as a single pipeline-improvement programme, not independent commands. The "Cross-Command Dependency Map" (`cross-cutting-analysis.md:60-80`) draws explicit arrows: SP-2→AD-5, SP-3→RM-1, AD-2→AD-1, RM-1+RM-3→RM-4.
- **Still possible today (Auggie check):** N/A (release-process finding). The implication for roadmap pipeline: SP-output should be available to AD-input should be available to RM-input. Whether the runtime pipeline preserves this artifact handoff is UNKNOWN from this partition.
- **Source artifacts:** `v2.09-adversarial-v2/cross-cutting-analysis.md:60-80,114-150`; `v2.10-spec-panel-v2/process-improvement/cross-cutting-analysis.md` (identical).

---

### F-A8-015: Risk R3 (Merge Corruption) successfully mitigated by tool-write mode + template
- **Type:** REMEDIATION (working as designed)
- **Pipeline step:** merge (Step 6)
- **Symptom:** R3 (probability Low, impact High, score 3) warned: "The merge executor may produce structurally broken output when integrating changes from non-base variants into the base, especially with complex cross-section dependencies" (`risk-assessment.md:41-52`). Designed mitigations: post-merge structural validation, preserved variants in `adversarial/` directory, merge-log.md documents each change.
- **Root cause (claimed):** LLM turn-budget can truncate mid-sequence when writing 200-400 line merged artifacts.
- **Remediation applied:** Current code adds `tool_write_mode=_roadmap_template is not None` and `template_path=_roadmap_template` for the merge step (`executor.py:2126-2127`); plus `_validate_merge_completeness` (`executor.py:856`) explicitly documented to handle the "silently truncated if the LLM's turn budget runs out mid-sequence" failure mode.
- **Outcome:** Post-merge validation in v2.09 (`merge-log.md:85-110`) PASSED across structural integrity, internal reference consistency, contradiction re-scan, provenance completeness. Mitigation is layered (preserve variants + structural check + tool-write enforcement + merge-log audit trail).
- **Still possible today (Auggie check):** NO (for the truncation-class) — `executor.py:2126-2127` mandates tool-write mode for merge when template is present, and `_validate_merge_completeness` is wired into `MERGE_GATE`.
- **Source artifacts:** `v1.7-adversarial/risk-assessment.md:41-52`; `v2.09-adversarial-v2/adversarial/merge-log.md:85-110`; current `executor.py:856-866, 2107-2128`.

---

### F-A8-016: "Correctness theater" / forcing-function-fatigue risk explicitly named, mitigation acknowledged as weak
- **Type:** FAILURE (acknowledged unmitigated risk)
- **Pipeline step:** debate / score (cross-cutting)
- **Symptom:** Cross-cutting analysis explicitly flagged: "Multiple forcing functions (boundary table + quantity flow + assumption extraction + invariant analysis + negative ACs) could cause 'checklist fatigue' where the generator produces formulaic, low-quality entries to satisfy structural requirements" (`cross-cutting-analysis.md:102`). Mitigation: "Quality validation at each stage... filters low-quality output. But the validators themselves have limited capacity to distinguish genuine from formulaic analysis" — explicitly acknowledged as weak.
- **Root cause (claimed):** Validators built from the same model family suffer the same blind spots they're meant to catch.
- **Remediation applied:** None structural; relies on the validator quality being "good enough."
- **Outcome:** Pre-existing risk; no documented occurrence in this partition but no mechanism to catch it either.
- **Still possible today (Auggie check):** YES — same Claude-on-Claude validation pattern in `executor.py:2078-2105`. INFERENTIAL: the asymmetric-model pairing (opus + sonnet/haiku) provides some perspective diversity, but does not address the formulaic-compliance risk when both models are nudged into the same checklist.
- **Source artifacts:** `v2.09-adversarial-v2/cross-cutting-analysis.md:102-104`; `v2.10-spec-panel-v2/process-improvement/cross-cutting-analysis.md:102-104`.

---

## Cross-cutting patterns within this partition

- **Pattern 1 — Debate works best when forced to be concrete about a single factual claim.** The file-passing-debate decisively resolved (95% confidence) because Argument B1 (Portability) was a single checkable fact ("`--file` does not accept local paths"). When the debate was about a multi-dimensional design choice (v2.09 M5 dependency, X-002), convergence stalled at 62%. Cites: F-A8-001, F-A8-002.
- **Pattern 2 — Convergence threshold (80%) is advisory, not enforcing.** v2.09 shipped a merge at 79% convergence with documented fallback; current code (`executor.py:2107-2128`) has no `CONVERGENCE_GATE`. Cites: F-A8-002, F-A8-005.
- **Pattern 3 — The spec-panel pipeline and the adversarial pipeline share architecture, shared cross-cutting analysis, and shared pathology (diff-only blind spot).** Improvements are co-designed (15 SP/AD/RM proposals scored together). Cites: F-A8-003, F-A8-007, F-A8-014.
- **Pattern 4 — Forcing functions outperform analytical-depth improvements; primary failure mode is omission, not superficiality.** Highest-ROI proposals (RM-4 implement/verify decomposition at composite 10.00, SP-6 consumed-vs-produced at 8.00) are the cheapest, most-mechanical. Cites: F-A8-007, F-A8-016.
- **Pattern 5 — Merge-step structural integrity is well-protected; debate-step assumption-coverage is not.** F-A8-005 (merge validation PASS) vs F-A8-003 (shared-assumption blind spot). The pipeline hardens what's easy to check (structure) and leaves what's hard to check (assumption coverage) as a design problem.
- **Pattern 6 — Risks documented in v1.7 risk-assessment (R1 sycophancy, R2 metric inconsistency, R7 scope creep) are still present in current code as unverified mitigations.** None of these have telemetry or post-hoc validation artifacts in this partition. Cites: F-A8-006, F-A8-012, F-A8-013.
- **Pattern 7 — "Quantitative" scoring is LLM-judged, not deterministically computed, contrary to R2's mitigation intent.** v2.10 base-selection's RC/IC/SR/DC/SC numbers look round-coarse; current `build_score_prompt` delegates to a Claude subprocess. Cites: F-A8-012.

## Brittleness drivers identified

- **Driver 1 — No convergence-based gate between debate and merge.** The `MERGE_GATE` is structural-completeness only; a 0%-convergence debate can still progress to a merged artifact with no halt. This makes adversarial scrutiny non-binding by mechanism, not by choice. Structural property: merge step's gate predicate does not consume the score step's convergence output.
- **Driver 2 — Diff-only analysis architecture.** `build_diff_prompt(roadmap_a, roadmap_b)` and `build_debate_prompt(diff_file, ...)` together establish that all downstream analysis operates on differences. Shared assumptions cannot become "diff points" without an explicit shared-assumption-extraction sub-step. The fix (AD-2) lives in SKILL.md (per backward-compat report) but the orchestration-layer wiring does not enforce its inclusion.
- **Driver 3 — Same-family validator-on-generator pairing.** Both variants and the scoring/merge agents are Claude models. There is no out-of-family validator (e.g., deterministic Python checker, different vendor LLM) at the debate or score steps. R1 (sycophancy) and "correctness theater" both flow from this property.
- **Driver 4 — Score step delegates "quantitative" metrics to LLM judgment.** R2's mitigation was "deterministic grep/regex patterns for quantitative layer (no LLM judgment)" — this is a Python-implementation pattern, but `build_score_prompt` is a prompt-builder that produces an LLM-judged score. The pipeline architecture lacks a Python-side scorer between debate and merge.
- **Driver 5 — Cross-command artifact propagation is implicit, not enforced.** Cross-cutting analysis identifies SP-3→RM-1, AD-2→AD-1, RM-1+RM-3→RM-4 as critical handoffs, but the pipeline orchestration (`executor.py:2000+`) wires only its own 8 steps; spec-panel outputs are not pulled into the adversarial debate step as an input, and adversarial outputs are not threaded into roadmap downstream commands beyond the in-pipeline merge.
- **Driver 6 — No telemetry/observation layer for the documented "monitor for sycophancy" recommendations.** R1 detection ("Monitor Round 1 agreement rate — if >90% agreement on first round, flag as potential sycophancy") requires an artifact that captures Round-1 agreement rate. No such artifact is produced by `executor.py`'s score or debate steps. The detection mechanism exists only as documentation, not as code.
- **Driver 7 — Convergence-threshold default (80%) is a magic number without empirical calibration.** Risk assessment and base-selection both use it; no artifact in this partition documents why 80% vs 75% vs 90%. INFERENTIAL: lack of calibration means threshold tuning is reactive (loosen when something fails) rather than principled.
