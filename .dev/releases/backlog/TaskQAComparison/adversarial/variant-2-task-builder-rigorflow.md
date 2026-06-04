# Variant 2: /task-builder QA Architecture (Rigorflow F1 Builder)

## 1. Architectural Identity

`/task-builder` is a **plan-time** QA architecture. It validates artifacts as they are SYNTHESIZED — verifying the research that informs the task file, the structural shape of the task file, and the operational soundness of the resulting plan. It does NOT validate execution.

## 2. Three-Layer Zero-Trust Verification Stack

### Layer 1 — A.8 Research Quality Gate (after parallel researcher fan-out)

- **Agents**: `rf-analyst` (completeness-verification) + `rf-qa` (research-gate) in PARALLEL
- **Stance**: ADVERSARIAL — "0 issues requires evidence you thoroughly checked"
- **Authority**: `fix_authorization: false` — read-only; CANNOT modify research files
- **DNSP Synthetic Finding Protocol** (PR-03): when a partition agent's escalation ladder exhausts (WebSearch → /rf:opinion → team-lead → retry), the orchestrator synthesises a HIGH-severity finding with byte-exact contract:
  - `severity: HIGH` (non-overridable across merge — R-126)
  - `source: "synthetic-dnsp"` (literal sentinel)
  - `affected_range`: failed agent's `assigned_files` slice verbatim
  - `evidence`: spawn-log path or `<!-- evidence-absence: ... -->` stub
  - `recommendation`: literal `"Manual review required — partition agent failed twice"` (R-117)
  - `dedup_key`: 2-tuple `(assigned_files_range, escalation_ladder_exhaust_point)` with closed-vocabulary second element from `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` (R-118)
  - `found_n_times`: positive integer, default 1, increment by exactly 1 per within-cycle collision (R-119)
- **INV-021** N-1 cohort concurrency: when one partition exhausts, the remaining N-1 siblings CONTINUE concurrently — never serialized behind the synthesis
- **All-agents-fail guard** (R-122): zero-partitions-succeeded → existing fix-cycle escalation; never emit synthetic (informationally equivalent + adds O(N) noise)
- **Gap-fill cycle**: max 3 rounds on FAIL findings; after 3, surface remaining gaps as Open Questions

### Layer 2 — A.10 Task File Structural Validation

- **Agent**: `rf-qa` (qa_mode: task-integrity)
- **Authority**: `fix_authorization: true` — auto-fixes structural defects in-place
- **9-item base checklist**: frontmatter shape, mandatory sections, item self-containment, granularity, evidence-based file paths, no CODE-CONTRADICTED/UNVERIFIED basis, Open Questions documented, phase dep DAG, reasonable item count
- **TB-Add structural additions** (catalogue grows over time via INV-010 dynamic enumeration):
  - TB-Add-1 placeholder scan (no TBD/TODO/FIXME, no title-only items)
  - TB-Add-2 item-count bounds (track ≥3 ≤40; single-track ≥3 ≤50; ADVISORY until empirical calibration)
  - TB-Add-3 clarification adjacency (blocked items reference blocking Open Question by index)
  - TB-Add-4 circular-dependency detection (item-to-item DAG)
  - TB-Add-5 XL splitting (complex/multi-file items either split or carry justifying comment)
  - TB-Add-6 confidence/verification format consistency
  - TB-Add-7 Execution Context source areas reappear in items
  - TB-Add-8 per-item Context evidence binding (file:line citation OR `<!-- evidence-absence: ... -->` justified-absence comment)

### Layer 3 — A.10.5 Task File Qualitative Validation

- **Agent**: `rf-qa-qualitative` (qa_phase: task-qualitative)
- **Authority**: `fix_authorization: true`
- **DM-005 Phase Contract** (frozen wire ABI for inter-agent handoff):
  - Producer: rf-qa; Consumer: rf-qa-qualitative
  - Artifact: `## Inherited Structural Verdict` block byte-spliced into consumer spawn prompt at the API-002 wire-contract position
  - Schema version: 1.0.0 (major-bump required for any field add/rename/semantic change)
  - Freshness rule (INV-002): re-extract verdict on every fix-cycle re-spawn; stale-verdict-rejection guard via SHA ledger
  - Enumeration rule (INV-010): dynamically enumerate TB-Add-* IDs from rf-qa.md's live "Structural Gate Additions" section so future additions auto-extend the passthrough — orphan TB-Add-N in producer table → FAIL with `INV-010-orphan-tb-add`
- **Anti-inflation rule** (`rf-qa-qualitative.md:766-775`, byte-stable): consumer's Self-Audit MUST list (a) which rf-qa PASS items it relied on AND (b) ≥1 semantic check where rf-qa PASS was insufficient and consumer's own tool work was required. "Reliance is not verification." Preserved byte-identical across releases.
- **15-item operational checklist + 5 Adversarial Axes (PR-07)** — every row's Axis column carries exactly one value from `{AX-1 drift, AX-2 contradictions, AX-3 omissions, AX-4 weakened-criteria, AX-5 invented-content, none}`. FAIL rows MUST cite most-specific firing axis; PASS rows carry `none` (positive statement that all 5 axes applied and none fired). `N/A`/blank in Axis column is FORBIDDEN.
- **Drift axis (AX-1)** requires BUILD_REQUEST.GOAL verbatim baseline; if absent, emit `drift-axis-inactive` annotation and proceed with other 4

## 3. Architectural Invariants

- **Zero-trust verification at every layer**: assume errors until independently verified
- **3 layers check ORTHOGONAL properties**: research completeness ≠ structural shape ≠ operational soundness
- **Partition-failure handling is formal**: DNSP is not "best effort" — it's a contract with named rejection symbols
- **Producer/consumer wire shape is frozen**: DM-005 schema is versioned; consumers refuse non-matching schema_version

## 4. Operational Characteristics

- Token cost: ~30-50K total (research-gate ~5-10K, A.10 ~5-8K, A.10.5 ~8-15K)
- Wall-clock: parallelizable within each gate; gates run sequentially
- Applicable to: MDTM task-file BUILD requests only; does NOT validate execution
- Failure modes: partition-agent exhaustion → DNSP synthetic; calibrator disjoint-set violation → degrade telemetry but proceed

## 5. Theory of Defects

Defects in TASK FILES propagate to expensive execution-time failures. Plan-time validation is the cheapest place to catch them. Three orthogonal gates compose: input-completeness (research-gate) × structural-shape (A.10) × operational-soundness (A.10.5). The anti-inflation rule structurally prevents Self-Audit gaming where the consumer rubber-stamps producer findings.

## 6. Documented Limitations

- Plan-time only — cannot validate execution behavior
- A.8 research-gate is read-only (no fix authority); structural fixes only happen at A.10/A.10.5
- DNSP synthetic-finding protocol applies only at A.8/A.10/A.10.5 partition spawns; not to non-partitioned spawns
- No evidence-validator final gate against the BUILT task file (citations in the task file are not independently re-Read)
- Token budget can exceed 50K for high-complexity builds
- Heavy reliance on rf-qa.md's "Structural Gate Additions" section as the live-catalogue source-of-truth — coupling failure mode if rf-qa.md is corrupted
