# Section A — Forensic Spec & Vision Analysis

**Source slice**: Group A (Spec & Vision)
**Inputs**:
- `/config/workspace/IronClaude/.dev/releases/backlog/v5.xxforensic/forensic-spec.md` (2324 lines)
- `/config/workspace/IronClaude/.dev/releases/backlog/v5.xxforensic/forensic-explore.md` (532 lines)
- `/config/workspace/IronClaude/.dev/releases/backlog/v5.xxforensic/spec-review-proposals.md` (221 lines)
- `/config/workspace/IronClaude/.dev/releases/backlog/v5.xxforensic/proposal-verdicts.md` (961 lines)

Citations use `file_basename:line` convention against the four source files above.

---

## Purpose

`/sc:forensic` is a **generic forensic QA & debug pipeline** for any codebase or feature release — auto-discovers investigation domains, runs parallel model-tiered root-cause analysis, delegates hypothesis and fix validation to the existing adversarial debate protocol, delegates implementation to specialist agents, and produces an evidence-backed report (`forensic-spec.md:48-51`; explore origin at `forensic-explore.md:132-147`).

**In scope** (`forensic-spec.md:54-66`):
- Automated codebase reconnaissance + domain discovery
- Parallel root-cause investigation with structured hypothesis output
- Adversarial hypothesis validation via `sc:adversarial-protocol`
- Fix proposal generation with **tiered aggressiveness** (`minimal | moderate | robust`)
- Adversarial fix validation
- Delegated implementation via specialist agents
- Delegated validation (lint, test, self-review)
- Checkpoint/resume
- **Quick/triage mode** for `sc:task-unified` TFEP integration
- **Caller-provided context** interface bypassing Phase 0
- **Tiered operating modes** (`light | standard | deep`) orthogonal to debate depth

**Out of scope** (`forensic-spec.md:68-72`): production deployment, git operations, domain-specific correctness validation beyond lint/test, UI/visual testing (no Playwright).

**Activation trigger**: command file invokes the `sc:forensic-protocol` skill as MANDATORY pre-execution step (`forensic-spec.md:397-404`). Auto-invoked by `task-unified` on TFEP escalation (`forensic-spec.md:1849-1854`, escalation gradient at `forensic-spec.md:1990-1993`).

**Origin / weaknesses being mitigated** (10 W-rows in `forensic-spec.md:76-89`, matching the exploration's weakness table at `forensic-explore.md:90-129`): hardcoded codebase (W-1), orchestrator reads everything ~50-80K (W-2), no model tiering (W-3), ad-hoc debates (W-4), MCP underutilized (W-5), no recon phase (W-6), sequential debate bottleneck (W-7), no checkpoint/resume (W-8), fixed 10 agents (W-9), orchestrator implements directly (W-10).

---

## Strategy

Six design principles drive the architecture (`forensic-spec.md:231-237`; mirrored verbatim from explore at `forensic-explore.md:136-147`):

1. **Generic-first** — domains auto-discovered, never hardcoded (`forensic-spec.md:231`).
2. **Orchestrator-as-dispatcher** — Opus orchestrator NEVER reads source code; only structured JSON summaries and Markdown selection files. Total orchestrator budget capped at **≤8,000 tokens** across the pipeline (`forensic-spec.md:215-216` NFR-001, `:309-322` orchestrator constraints table).
3. **Model tiering** — Haiku for surface scans, Sonnet for deep analysis, Opus reserved for synthesis and coordination only (`forensic-spec.md:233`, decision matrix at `:1509-1527`).
4. **Leverage existing infrastructure** — delegates to `/sc:adversarial`, borrows `sc:cleanup-audit-protocol` batch-checkpoint pattern, borrows `/sc:spawn` Epic→Story→Task decomposition (`forensic-spec.md:234`, `:1811-1855`).
5. **Checkpoint-resumable** — every phase writes artifacts; any phase restartable via `progress.json` (`forensic-spec.md:235`, schema at `:1448-1503`, resume logic at `:1659-1682`).
6. **MCP-aware** — explicit MCP routing table assigns each server to the phases where its capabilities are most valuable (`forensic-spec.md:236`, routing table `:1552-1573`).

**Orthogonal-axes design** (a key strategic refinement layered onto the original explore concept): `--tier light|standard|deep` controls **pipeline scope** (which phases execute, agent count) and is independent of `--depth quick|standard|deep` which controls **adversarial debate depth only** (`forensic-spec.md:108-110` glossary, `:199-202` FR-038 + FR-056, phase behavior matrix at `:276-307`).

**Token-efficiency targets** (`forensic-spec.md:1876-1888` Section 16.1):
- Orchestrator: ~50-80K → ~5-8K (~90% reduction)
- Phase 2 debate: ~15K → ~8K (~47% reduction)
- Phase 3b debate: ~10K → ~5K (~50% reduction)
- Light tier total: ~5-8K vs Standard ~50-60K (`forensic-spec.md:1889-1903`).

---

## Approach

**Eight-phase pipeline** (Phases 0, 1, 2, 3, 3b, 4, 5, 6) with phase-architecture diagram at `forensic-spec.md:240-274`. Data flow: Phase 0 (3× Haiku recon) → `investigation-domains.json` → Phase 1 (N× Sonnet/Haiku investigation, one per domain) → `findings-domain-{N}.md` → Phase 2 (adversarial debate) → `base-selection.md` → Phase 3 (M× Sonnet fix proposals) → `fix-proposal-H-{N}.md` → Phase 3b (adversarial debate) → `fix-selection.md` → Phase 4 (specialist implementation + quality-engineer test creation) → manifests → Phase 5 (lint + test + self-review, 3 agents) → reports → Phase 6 (Opus final report).

**Phase 0 reconnaissance** (`forensic-spec.md:488-575`): 3 parallel Haiku agents — 0a structural inventory (Glob/Read, no logic analysis), 0b dependency graph (Serena `find_referencing_symbols` for hot paths), 0c risk-surface scan (error handling, subprocess, signals, env-dependent paths, untested branches, concurrency). Orchestrator then synthesizes `investigation-domains.json` containing 3-10 domains with risk scores, suggested agent type, and suggested model tier (Haiku if risk <0.7, Sonnet if ≥0.7) — capped at 500 tokens (`forensic-spec.md:556-575`).

**Phase 1 root-cause discovery** (`forensic-spec.md:577-626`): one agent per domain, parallelism bounded by `--concurrency`, each agent produces a `findings-domain-{N}.md` with the Hypothesis Finding Schema (id, summary, evidence as `file:line` excerpts, confidence 0-1, falsification criterion, severity, category).

**Phase 2 hypothesis debate** (`forensic-spec.md:628-666`): **fully delegates** to `/sc:adversarial --compare findings-domain-*.md --depth deep --convergence {threshold} --focus "evidence-quality,reproducibility,severity"`. Reuses the existing 5-step adversarial pipeline: diff analysis with cross-domain contradiction detection + duplicate merging, parallel debate round 1 with steelman-critiques, sequential debate round 2 with rebuttals, 25-criterion rubric scoring **per hypothesis** (not per file), ranked selection (`forensic-spec.md:144-146`, `:650-657`).

**Phase 3 fix proposals** (`forensic-spec.md:668-716`): one Sonnet agent per surviving hypothesis cluster produces three tiers (minimal/moderate/robust), each with changes list, risk text, side-effects array, confidence; plus a `test_requirements` block typed unit/integration/e2e. Uses Serena `find_referencing_symbols` for impact tracing, Context7 for idiomatic patterns.

**Phase 3b fix debate** (`forensic-spec.md:718-751`): re-invokes `/sc:adversarial --compare fix-proposal-H-*.md --depth standard --focus "correctness,risk,side-effects"`. Output `fix-selection.md` is the **primary orchestrator decision point** — orchestrator builds implementation plan, greenlights fixes by combined confidence/risk score (capped at 800 tokens).

**Phase 4 implementation** (`forensic-spec.md:753-802`): two parallel agents — 4a specialist (python-expert / backend-architect / frontend-architect, selected by file-extension dominance per `forensic-spec.md:895-905`) using Serena `replace_symbol_body` for surgical edits; 4b quality-engineer creating regression tests guided by Context7. Worktree isolation recommended.

**Phase 5 validation** (`forensic-spec.md:804-849`): three parallel agents — 5a Haiku lint, 5b Sonnet quality-engineer test execution + failure correlation, 5c Sonnet self-review running 4 mandatory self-check questions against original hypotheses (`forensic-spec.md:843-847`).

**Phase 6 final report** (`forensic-spec.md:851-870`): Opus orchestrator synthesizes from summary artifacts only (~2,000 tokens). Output sections: Ranked Root Causes (with evidence), Rejected Hypotheses, Chosen Fixes, Files Changed, Test/Lint Results, Residual Risks + Follow-ups, Domain Coverage Map.

**Light-tier path** (TFEP triage) (`forensic-spec.md:276-308`, `:1616-1649`, `:1919-2042`): Phase 0 SKIP (caller provides `--context <file>` YAML); Phase 1 fixed at 2 Sonnet agents using `/sc:troubleshoot` prefix (diagnosis only); Phase 2 `--depth quick`; Phase 3 fixed at 2 Sonnet agents using `/sc:brainstorm` prefix (proposal only); Phase 3b `--depth quick`; Phases 4 and 5 SKIP; Phase 6 produces abbreviated `tfep-report.md` + `tasklist-insertion.md` returned to caller for `sc:task-unified --compliance strict` consumption.

**Caller-aware defaults** (`forensic-spec.md:304-307`): `--caller task-unified` ⇒ `--tier light --intent triage --depth quick`. Otherwise `--tier standard --intent auto --depth standard`.

**Escalation gradient** (`forensic-spec.md:1986-1998`): 1st TFEP trigger → light tier (~5-8K); 2nd trigger → standard tier (~15-20K); 3rd trigger → FULL STOP, report to user. "Same failure" tracked via `escalation_count` in failure context schema (`forensic-spec.md:1283-1288`).

---

## Techniques

**Domain auto-discovery algorithm** (`forensic-spec.md:556-575`, panel resolution at `:2062-2065`): clustering by natural risk signals; each distinct risk category with ≥1 file generates a candidate domain; domains merged when file overlap >50%; `--focus` hints become forced domains with `risk_score: 0.5` if no auto-match (FR-047).

**Hypothesis confidence scoring**:
- Evidence-backed scores 0.0-1.0 per finding (`forensic-spec.md:1335-1338`).
- Calibration normalization happens **inside adversarial debate** via the 25-criterion rubric — pre-debate scores are agent-subjective, post-debate scores are rubric-normalized (`forensic-spec.md:2174-2175`).
- Default filter threshold 0.7; configurable via `--confidence-threshold 0.0-1.0` (`forensic-spec.md:205-206` FR-041).

**Hypothesis ID scheme**: `H-{domain_index}-{sequence}`, regex-validated `^H-\d+-\d+$` (`forensic-spec.md:1320-1323`). `{domain_index}` is the 1-based position in `investigation-domains.json` (`forensic-spec.md:2174`). **(Note**: P-009 in proposal-verdicts.md:159-176 has accepted this be replaced by a stable `domain_id` hash for resume safety.)

**Fix-tier rubric**: exactly three tiers per fix proposal — `minimal` (smallest safe change), `moderate` (balanced), `robust` (comprehensive redesign) (`forensic-spec.md:99`, `:1361-1399`). `--fix-tier` selects default aggressiveness (`forensic-spec.md:206`).

**Adversarial integration pattern**: forensic delegates to the existing 5-step protocol (diff → debate round 1 parallel → debate round 2 sequential → 25-criterion rubric → ranked selection), consuming standard outputs `debate-transcript.md` + `base-selection.md` with no modifications to the adversarial protocol (`forensic-spec.md:1813-1826`).

**Model-tier decision matrix** (`forensic-spec.md:1509-1527`):
- Haiku: Phase 0 (all 3 recon agents), Phase 1 low-risk domains (risk <0.7), Phase 5a lint.
- Sonnet: Phase 1 high-risk (risk ≥0.7), Phase 2/3b advocates, Phase 3 fix proposals, Phase 4 implementation/tests, Phase 5b/5c.
- Opus: Phase 0 domain synthesis, Phase 2/3b debate-orchestrator, Phase 6 final report.
- Light tier: simplified — all 4 agents Sonnet, no Haiku/Opus (`forensic-spec.md:1529-1540`).

**MCP routing table** (`forensic-spec.md:1552-1573`):
- Serena: Phase 0 `get_symbols_overview`, Phase 1 `find_referencing_symbols`/`find_symbol`, Phase 4 `replace_symbol_body`.
- Context7: Phase 0 framework detection (`resolve-library-id`, `get-library-docs`), Phase 1 framework patterns, Phase 4 test framework patterns.
- Sequential: `sequentialthinking` in Phases 1, 2, 3.

**MCP fallback / circuit-breaker** (`forensic-spec.md:1568-1572`, `:1786-1799`): Serena OPEN ⇒ Edit/MultiEdit (loses symbol precision); Sequential OPEN ⇒ auto-downgrade adversarial to `--depth quick`; Context7 OPEN ⇒ WebSearch.

**Graceful degradation levels** (`forensic-spec.md:1800-1807`): Full → Reduced precision (Serena down) → Reduced depth (Sequential down) → Minimal (all MCP down, `--depth quick` enforced).

**Agent prompt prefix conventions** (`forensic-spec.md:2003-2026`): Light-tier Phase 1 prompts MUST begin with `/sc:troubleshoot`; light-tier Phase 3 prompts MUST begin with `/sc:brainstorm`.

**Specialist-agent selection signals** (`forensic-spec.md:897-905`): `.py` dominance → `python-expert`; backend/API/infrastructure focus → `backend-architect`; `.jsx/.tsx/.vue` dominance → `frontend-architect`; mixed → `python-expert` default.

**Self-review 4-question checklist** (`forensic-spec.md:843-847`): (1) Tests/validation executed? (2) Edge cases covered? (3) Requirements matched (tie back to hypothesis)? (4) Follow-up or rollback steps needed?

**Worktree isolation**: Phase 4 SHOULD use git worktrees for parallelism; sequential fallback (concurrency capped at 1) when worktrees unavailable (`forensic-spec.md:222-223` NFR-008, `:2079-2080`).

**Per-agent token bounds** (`forensic-spec.md:2127`): Phase 1 Sonnet 2-3K, Haiku 1-2K; total Phase 1 = N × avg.

**Per-MCP-server concurrency cap** (`forensic-spec.md:2127`, NFR-010): ≤3 simultaneous requests per server regardless of `--concurrency`.

**Return contract** (`forensic-spec.md:1953-1984`): YAML structure with `status` (`success|partial|failed`), `root_cause_path`, `solution_plan_path`, `tasklist_insertion_path`, `recommended_resume_mode`, `recommended_escalation`, `requires_user_review`, `test_is_wrong` (critical flag: when adversarial debate concludes test expectations are outdated rather than code being wrong, caller MUST present to user). Write-on-failure required.

**Pre-flight validation** (`forensic-spec.md:2247-2248` FR-054): output dir writable, target paths exist, required tools available; MCP availability checked lazily at first use.

**Stale-codebase detection** (`forensic-spec.md:2246-2247` FR-053): compare `git rev-parse HEAD` (or mtime fallback) on resume.

**Secret redaction in final report excerpts** (`forensic-spec.md:2095-2096` FR-049): redact common secret patterns to `[REDACTED]`. (Note: P-020 in proposal-verdicts.md:803-823 widens this to all artifacts via pipeline-level post-processing.)

---

## Deliverables

**Artifacts produced** (standard tier directory tree `forensic-spec.md:1580-1614`):

| Phase | Artifact(s) |
|-------|-------------|
| 0 | `phase-0/structural-inventory.json`, `phase-0/dependency-graph.json`, `phase-0/risk-surface.json`, `investigation-domains.json` |
| 1 | `phase-1/findings-domain-{1..N}.md` |
| 2 | `phase-2/adversarial/diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md` |
| 3 | `phase-3/fix-proposal-H-{1..M}.md`, `fix-selection.md` |
| 4 | `phase-4/changes-manifest.json`, `phase-4/new-tests-manifest.json` |
| 5 | `phase-5/lint-results.txt`, `phase-5/test-results.md`, `phase-5/self-review.md` |
| 6 | `final-report.md` |
| Cross-cut | `progress.json` (checkpoint) |

**Light-tier artifacts** (`forensic-spec.md:1620-1649`): `context.md`, `phase-1/rca-alpha.md`, `phase-1/rca-bravo.md`, `phase-2/adversarial/*`, `rca-verdict.md`, `phase-3/solution-alpha.md`, `phase-3/solution-bravo.md`, `phase-3b/adversarial/*`, `solution-verdict.md`, `tasklist-insertion.md`, `tfep-report.md`, `progress.json`. All MUST be git-committed.

**Final-report template** (`forensic-spec.md:1690-1758`): 7 sections — Ranked Root Causes (rank/ID/summary/severity/confidence/evidence table), Rejected Hypotheses (with rejection reason + debate score), Chosen Fixes (with per-fix breakdown), Files Changed, Test/Lint Results (status + counts + analysis), Residual Risks + Follow-ups, Domain Coverage Map (per-domain risk/hypotheses-found/survived/fixes-applied + uninvestigated areas + coverage percentage).

**Tasklist-insertion format** (`forensic-spec.md:1923-1945`): `## Failure Remediation Plan (Adjudicated)` block with per-task File(s)/Change/Expected outcome/Test criteria + implementation step checkboxes, with provenance comment.

**Quality metrics targets** (`forensic-spec.md:1906-1915`): orchestrator ≤8K tokens; 100% hypothesis evidence coverage; 100% falsifiability; ≥80% domain coverage; greenlit fixes confidence > threshold; 0 lint errors in changed files; 100% new-regression-test pass rate.

**Per-phase orchestrator token budgets** (`forensic-spec.md:2308-2320` Appendix B): P0=500, P1=1000, P2=500, P3=0, P3b=800, P4=0, P5=0, P6=2000 → total ~4,800 tokens (within 8K hard cap).

---

## Rejected proposals (per proposal-verdicts.md)

**Headline**: 22 proposals submitted (`spec-review-proposals.md:1-221`), **0 outright REJECTed**, **14 ACCEPTed**, **8 MODIFIed** (`proposal-verdicts.md:14-16`). The MODIFY verdicts trim or refocus the proposal — the rejected sub-portions reveal the spec's design boundaries.

**Rejected sub-elements (the design boundaries)**:

- **P-007 — `secrets_exposure` risk category REJECTED** (`proposal-verdicts.md:117-125`): no FR drives it, vague panel reference, oracle testing gap (no fixture corpus for secret-detection ground truth). Deferred to future iteration backed by formal FR + fixtures. Only the `overall_risk_score` calculation alignment was accepted.

- **P-008 — `progress.json` field additions partly REJECTED** (`proposal-verdicts.md:148-157`): `spec_version` deferred post-v1.0 (YAGNI); `run_id` deferred (observability, not correctness); `phase_status_map` rejected outright (duplicates `completed_phases` + `current_phase`, no unique information). Only 3 of 5 fields accepted: `target_paths` (required), `flags` (promoted to required), `git_head_or_snapshot` (optional).

- **P-010 — "Exactly 3 fix tiers" REJECTED** (`proposal-verdicts.md:194-203`): forces filler content when fewer tiers are meaningful (architect: too rigid); ~500-1000 tokens of padding per proposal × N hypotheses (analyzer: disproportionate); cannot distinguish genuine tiers from filler in automated tests (QA: false positives in quality checks). `minItems` stays at 1. Only uniqueness constraint accepted; orchestrator `--fix-tier` fallback added to handle missing tiers.

- **P-019 — `--clean=archive|delete` variant REJECTED** (`proposal-verdicts.md:782-799`): over-engineered for <5% probability scenario. Reduced to one-sentence guard clause in FR-052 ("`--clean` is a no-op unless all phases completed successfully").

- **P-022 — Full MCP scheduler REJECTED** (`proposal-verdicts.md:446-481`): semaphores + exponential backoff + deterministic queue ordering rejected as infrastructure that doesn't exist in Claude Code runtime. Replaced with **prompt-based MCP access budgets per agent type** (e.g., Phase 1 investigation: 3 Serena calls + 1 Context7 call per domain; Phase 4a: 5 Serena + 2 Context7 per fix) and `--concurrency` default reduced from 10 → 5.

- **P-005 — Migration fallback for legacy fix-selection.md path REJECTED** (`proposal-verdicts.md:626-633`): spec is v1.0.0-draft with no existing implementations; migration logic adds complexity for non-existent concern. Canonical path becomes `phase-3b/fix-selection.md`.

- **P-012 — Runtime token monitoring REJECTED** (`proposal-verdicts.md:300-331`): replaced with **static per-phase rules** (SHOULD soft target + MUST hard stop + deterministic overflow action) since runtime token monitoring is not enforceable in the harness. Adds `budget_status` field to `progress.json` for observability.

- **P-011 — Orchestrator-direct-ranking fallback REJECTED** (`proposal-verdicts.md:268-290`): the original spec's adversarial-failure fallback ("orchestrator reads all findings and ranks by confidence score directly") violates the Section 4.3 invariant. Replaced with three-level degradation chain: (1) retry adversarial `--depth quick`, (2) spawn single Sonnet scoring agent with 60s hard timeout + 1K-token cap, (3) emit findings as-is with `debate_status: "skipped"` and let all surviving hypotheses proceed.

- **P-003 — `skipped_by_mode` per-phase status enum REJECTED** (`proposal-verdicts.md:637-661`): replaced with a `skipped_phases` array in `progress.json` (self-describing, doesn't extend the status enum).

- **P-020 — Per-agent prompt-level redaction REJECTED** (`proposal-verdicts.md:816-823`): agents cannot reliably self-redact. Replaced with **pipeline-level post-processing pass** after each phase write. `--redaction-config` flag deferred; ships with fixed default pattern set (AWS keys, GCP service-account keys, `password=`/`secret=`/`token=`/`api_key=`, PEM private key blocks).

- **P-007 cross-cut — `phase_status_map`** (see P-008) — duplicates existing fields.

**Cross-cutting finding CCF-1** (`proposal-verdicts.md:845-857`): the recurring rejection pattern is **aspirational vs enforceable**. Spec language that mandates behavior unenforceable in the current Claude Code runtime (hard token ceilings, model-tier verification, MCP semaphores) gets replaced with **observability hooks** (`requested_tier`, `actual_tier`, `budget_status`) and **deterministic fallback chains**, never silent assumption.

**Cross-cutting finding CCF-3** (`proposal-verdicts.md:871-877`): Section 17 normativity split — FR-047..FR-055, NFR-009, NFR-010, Schema 9.9 currently live in commentary section but contain normative requirements (notably security-relevant FR-053/FR-054). P-001 (Tier 1 priority) requires mechanical integration into normative sections 3, 5, 7, 9, 12 before any other spec edit work.

**Cross-cutting finding CCF-4** (`proposal-verdicts.md:879-888`): resume safety is the most recurring weak point — `progress.json` must be **self-describing**; every recoverable state explicitly encoded, never inferred from flag combinations or absent entries.
