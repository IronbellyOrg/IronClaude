# Architectural Analysis: task-builder vs sc:tasklist-protocol

**Source**: digest-synthesis (skill-invoke degraded — /sc:analyze returned its own help text rather than performing analysis; synthesis below derived from Buckets A–F + FINAL-REPORT §3–4)
**Date**: 2026-05-14
**Scope**: Architecture-focus comparison of `src/superclaude/skills/task-builder` and `src/superclaude/skills/sc-tasklist-protocol`, optimised for the inverse-direction merge (sc:tasklist → task-builder).

---

## Executive overview

**sc:tasklist-protocol** is a **deterministic, single-pass, 10-stage transform** that converts roadmap text into a Sprint-CLI-compatible multi-file bundle (`tasklist-index.md` + N `phase-N-tasklist.md`). Its defining property is reproducibility: keyword-scored tier classification (STRICT > EXEMPT > LIGHT > STANDARD with compound-phrase overrides), appearance-order ID assignment (`R-###` → `T<PP>.<TT>` → `D-####`), explicit 4-rule tiebreakers, and a 17-point pre-write quality gate gated by write-atomicity (Bucket A SKILL.md:14, 36–37, 156–280, 374–391, 981–1042). Validation is a fan-out of 2N parallel `Task`-tool agents (one A and one B per phase) that check drift / contradictions / omissions / weakened criteria / invented content; patch application is delegated to `sc:task` so the orchestrator never edits files itself (Bucket A SKILL.md:1091–1106, 1248–1258). Stage 10 is single-pass spot-check with no loop. Token cost is low (50–80K) and wall-clock 2–15 minutes (FINAL-REPORT §4).

**task-builder** is an **agent-team-orchestrated, multi-stage, evidence-bound builder** that produces an MDTM task file at `.dev/tasks/to-do/TASK-RF-<timestamp>/` from a GOAL or BUILD_REQUEST. The skill is itself the orchestrator and spawns `general-purpose` researchers, `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, and `rf-task-builder` agents — never builds the file directly (Bucket C SKILL.md:10, 80–82, 398, 720). Its defining property is **adversarial evidence binding**: every checklist item embeds context+action+output+verification+completion-gate self-contained, every claim must cite file:line, and four sequential QA gates (A.5 self-review, A.8 research-gate, A.10 task-integrity, A.10.5 qualitative) operate under a zero-trust stance — "assume the work contains errors" (Bucket C SKILL.md:900, 1452–1457, 1530, 621/878/895/929). Research artifacts persist in `.dev/tasks/research/` as the evidence trail. Token cost is very high (500K–1M+) and wall-clock 15–45 minutes (FINAL-REPORT §4).

---

## Architectural axes

| Axis | sc:tasklist-protocol | task-builder | Source |
|---|---|---|---|
| **Determinism** | Full: same roadmap → same output (explicit claim) | None claimed; explicit non-determinism via agent exploration | Bucket A SKILL.md:36–37, 14 / Bucket C SKILL.md:88, 201 |
| **Generation Model** | Deterministic transform (keyword scoring + appearance-order IDs + tiebreakers) | Agent-team orchestration (parallel researchers → analyst+QA gate → builder agent) | Bucket A SKILL.md:156–280, 374–391 / Bucket C SKILL.md:10, 398–401 |
| **Output Path** | `TASKLIST_ROOT` derived via 3-rule cascade → `.dev/releases/current/<segment>/`; emits N+1 files + 2 validation artifacts | `.dev/tasks/to-do/TASK-RF-YYYYMMDD-HHMMSS/<TASK_ID>.md` + `research/*.md` + `qa/*.md` persistent | Bucket A SKILL.md:64–94 / Bucket C SKILL.md:107–116, 120–129 |
| **Quality Gates** | Single 17-point pre-write gate (8 Sprint + 4 semantic + 8 structural checks) executed once before any Write | 4 sequential gate stages: A.5 (7), A.8 (9 analyst + 10 QA), A.10 (9), A.10.5 (15); plus 18 Critical Rules | Bucket A SKILL.md:983–1032 / Bucket C SKILL.md:357–363, 594–602, 898–906, 961, 1526–1564 |
| **Validation** | 2N parallel `Task` agents (one A + one B per phase) checking 5 categories; merge+dedupe; retry once on agent failure | Adversarial rf-analyst + rf-qa run in parallel on research files; rf-qa-qualitative on assembled task file | Bucket A SKILL.md:1091–1106, 1112–1117, 1150 / Bucket C SKILL.md:574–654, 923–1000 |
| **Patch Loop** | Single-pass: delegate to `sc:task --compliance strict`; Stage 10 spot-check is single-pass, does NOT loop on UNRESOLVED | Multi-cycle: research-gate gap-fill max 3, RESEARCH_NEEDED max 2, MALFORMED max 2; 5 QA fix cycles per gate type in rf-task-builder | Bucket A SKILL.md:1244–1260, 1266, 1288 / Bucket C SKILL.md:651, 859, 865, 870 / Bucket D rf-task-builder.md:336–359 |
| **Traceability** | Full chain `R-### → T<PP>.<TT> → D-####` surfaced in three index registries (Roadmap Item Registry, Deliverable Registry, Traceability Matrix) | Absent — no matrix; only `TASK_ID` and template-numeric `1.1`/`1.2` checklist items; per-item evidence binding to file:line citations | Bucket A SKILL.md:596–600, 672–707 / Bucket C SKILL.md:69–71, 1452, 1530 |
| **Tier Classification** | Deterministic 4-tier (STRICT/STANDARD/LIGHT/EXEMPT) for artifact-compliance; compound-phrase overrides + keyword scoring + context boosters + confidence formula | Rule-based 3-tier (Quick/Standard/Deep) for *research depth*; sets researcher count 3 / 4–5 / 6–8 | Bucket A SKILL.md:505–575, rules/tier-classification.md:33–71 / Bucket C SKILL.md:90–101 |
| **Agent Delegation** | Stage 7: 2N parallel adversarial agents (anonymous `Task` tool). Stage 9: delegates to `sc:task` skill | rf-* named agent ecosystem (analyst, qa, qa-qualitative, task-builder, researchers); explicit message vocab RESEARCH_NEEDED / MALFORMED / TASK_READY | Bucket A SKILL.md:1091–1106, 1248–1250 / Bucket D rf-team-lead.md:54–75, 193–243 |
| **Token Cost** | Low: 50–80K typical | Very high: 500K–1M+ | FINAL-REPORT §4 |
| **Wall-clock** | 2–15 minutes | 15–45 minutes per task | FINAL-REPORT §4 |

---

## Architectural deltas

**Delta 1 — Generation paradigm (deterministic transform vs adversarial assembly).** sc:tasklist treats the roadmap as the only source of truth and asserts "no discretionary choices" (Bucket A SKILL.md:14). Tier scores, IDs, and tiebreakers are mechanically derived; the orchestrator does the work. task-builder treats the codebase as the source of truth (Bucket C SKILL.md:706, 1528) and delegates almost everything — research, analysis, QA, building — to spawned agents whose outputs feed back as evidence files. The two skills are doing categorically different jobs: one mechanically renders a plan from prose; the other constructs an executable plan from a live codebase.

**Delta 2 — Quality assurance scope and topology.** sc:tasklist runs one 17-point gate *before* any write (write-atomicity), then validates *after* writing via parallel agents. task-builder runs four sequential gates *during* the build, each adversarial and each empowered to fail the whole task. sc:tasklist's gate is **structural**; task-builder's gates are **structural + semantic + qualitative**. The 17 checks and the 7/9/10/15 checks are not 1:1 comparable (CB-3 advisory), but task-builder consistently demands more *kinds* of validation while sc:tasklist demands more *exhaustive* coverage in a single pre-write pass.

**Delta 3 — Patch and recovery semantics.** sc:tasklist explicitly does not loop on UNRESOLVED findings (Bucket A SKILL.md:1288); it delegates one patch pass and one spot-check. task-builder caps RESEARCH_NEEDED at 2, MALFORMED at 2, research-gate gap-fills at 3, and rf-task-builder QA fix cycles at 3 per gate type (Bucket C SKILL.md:651, 859, 865; Bucket D rf-task-builder.md:336–359). The two architectures encode opposite philosophies about when to give up: sc:tasklist accepts UNRESOLVED as a fact and logs it for human review; task-builder retries within budgets and then surfaces remaining gaps as Open Questions.

**Delta 4 — Persistence and traceability artifacts.** sc:tasklist produces a *renderable* artifact: an index file with three matrix-style registries that the Sprint CLI consumes. task-builder produces an *audit trail*: research notes, QA reports, and the final task file all coexist in `.dev/tasks/` and "must NOT be deleted" (Bucket C SKILL.md:1536, 1608). sc:tasklist's traceability is structural (ID chains); task-builder's traceability is evidentiary (file:line citations + persisted intermediate artifacts).

**Delta 5 — Input contract and execution context.** sc:tasklist requires roadmap text plus optional `--spec` (TDD) / `--prd-file` enrichment (Bucket A SKILL.md:47–202). task-builder requires a free-form GOAL or a structured BUILD_REQUEST.md, with WHY/WHERE optional (Bucket C SKILL.md:30–47). sc:tasklist is one stage in a pipeline (roadmap → tasklist → sprint); task-builder is a complete end-to-end task production line that operates without an upstream artifact.

---

## Inverse-direction feasibility

For each major sc:tasklist capability, this section judges whether it could be imported into task-builder's architecture and whether doing so would violate one of task-builder's five protected invariants (Bucket C G6: **self-contained-item**, **evidence-bound-item**, **persistent .dev/tasks/ artifact**, **zero-trust QA**, **parallel research**).

**Implementable in task-builder's architecture:**

- **17-point quality gate (as additive content rules).** Many of the 17 checks already overlap task-builder's 9-item task-integrity (Bucket C SKILL.md:898–906) and 15-item validation checklist (SKILL.md:1491–1507). Importing residual checks (e.g., placeholder/TBD scan, circular dependency detection, XL splitting) as new entries in rf-qa's task-integrity checklist preserves zero-trust QA — they become more adversarial checks, not fewer. (CB-3: "must classify per-check, not in bulk".)
- **2N-parallel adversarial validation** (CB-3 / FINAL-REPORT §3.1). task-builder already runs analyst+QA in parallel on research files and partitions when >6 research files exist (Bucket C SKILL.md:643, 1544). Generalising to "split task checklist into two halves and adversarially validate each" is consistent with parallel-research invariant and with rf-qa's existing partition support (Bucket D rf-qa.md:50–77).
- **Drift / contradictions / omissions / weakened-criteria / invented-content checks.** These map cleanly onto rf-qa-qualitative's existing qualitative checklist topics (Bucket D rf-qa-qualitative.md:110–176) and onto rf-qa's adversarial stance. Preserves zero-trust QA.
- **DNSP synthetic-finding behavior (FINAL-REPORT R1).** Adopt as rf-analyst's failure-mode: when a partition agent fails, synthesize a conservative HIGH-severity finding flagging the un-analysed range (Bucket D rf-analyst.md as candidate host per Bucket D §"Surfaces relevant"). Preserves all five invariants — synthetic findings still cite evidence (the failed-agent range), still feed the persistent QA trail, and explicitly surface gaps rather than hiding them.
- **Gate-results passthrough (FINAL-REPORT R3).** Feed rf-qa's structural results to rf-qa-qualitative so it skips re-checking ("All PASS items are machine-verified — focus on semantic quality"). Preserves zero-trust QA so long as rf-qa-qualitative's adversarial stance is maintained over passes that rf-qa already cleared.
- **Tier-calibration advisory (FINAL-REPORT R5, advisory-only form).** Could live as a section in the task file header listing observed override patterns. Advisory-only behavior preserves task-builder's evidence-bound invariant because the data source is itself an evidence file.
- **Dual-mode patch recovery (FINAL-REPORT R4).** task-builder already has retry budgets; formalising them with monotonicity guards and a `--non-interactive` flag is additive.
- **Task-execution-context block (FINAL-REPORT R2).** task-builder already requires self-contained items embedding context; importing the "no specific file paths — source areas only" framing is compatible — but only with care, since task-builder's evidence-bound invariant demands file:line citations *somewhere* (just not in the executor's context block).
- **Appearance-order IDs and explicit tiebreakers** (within a single task file). Importing `T<PP>.<TT>` ID scheme as the canonical numbering for checklist items inside a task file is compatible with template numbering already used (`1.1`/`1.2`).

**Violates task-builder's invariants if imported as-is:**

- **Full determinism guarantee** (CB-5). task-builder explicitly relies on agent exploration — Bucket C SKILL.md:201 calls out non-determinism as the model. Asserting blanket determinism would contradict the parallel-research invariant. Per CB-5, only *scoped* determinism (e.g., "frontmatter-stable" or "ID-stable") is feasible.
- **Single-pass spot-check no-loop** (Bucket A SKILL.md:1288). task-builder is built on multi-cycle correction; importing a no-loop policy violates the zero-trust QA invariant (which depends on fix-cycle retries — Bucket D rf-qa.md:310–313).
- **Write atomicity** (Bucket A SKILL.md:1042). task-builder *mandates* incremental writes ("INCREMENTAL TASK FILE WRITING (MANDATORY — NEVER ONE-SHOT)" — Bucket C SKILL.md:819–832). Importing atomic-write would directly contradict the persistent-.dev/tasks/-artifact invariant and the "no one-shotting" rule (#8, SKILL.md:1542).
- **Orchestrator-does-not-apply-patches** (Bucket A SKILL.md:1258). task-builder's rf-task-builder agent *is* the file writer; delegating patches to a separate `sc:task` skill is a re-architecture, not an import. Violates the self-contained-item invariant (the builder owns the file lifecycle end-to-end).
- **Full R-### → T<PP>.<TT> → D-#### traceability matrix as a hard requirement**. Could be additive (CASE-B per CB-6) but only if task-builder retains its "GOAL or BUILD_REQUEST" input contract — there is no `R-###` namespace without a roadmap. A *partial* matrix (T<PP>.<TT> → D-#### inside a single task file) is feasible; the upstream `R-###` half requires a roadmap input that task-builder does not consume.
- **Tier classification keyword scoring** (CB-4). task-builder's tier already controls a different thing (research depth, not artifact compliance). Importing the keyword algorithm would either replace a working rule-based system or introduce a parallel scoring system whose output has no consumer. Conflicts with task-builder's invariant that tier == research depth.
- **Fidelity gate CLI** (Bucket B B-sc-tasklist-cli). task-builder has no CLI surface; importing the Python `tasklist validate` flow would require building a CLI from scratch. The skill itself can adopt the *prompt content* of `build_tasklist_fidelity_prompt` (Bucket B prompts.py:17–148) without the Python harness, but doing so adds no value over the existing rf-qa adversarial stance.

---

## Summary table — inverse-direction disposition

| sc:tasklist capability | Importable? | Protected invariant at risk |
|---|---|---|
| 17-point gate (per-check import) | YES (additive to rf-qa) | none (strengthens zero-trust QA) |
| 2N-parallel adversarial validation | YES | none (extends parallel research) |
| Drift/contradiction/omission checks | YES (into rf-qa-qualitative) | none |
| DNSP synthetic-finding | YES (rf-analyst host) | none |
| Gate-results passthrough | YES (rf-qa → rf-qa-qualitative) | none |
| Tier-calibration advisory | YES (advisory only) | none |
| Dual-mode patch recovery (monotonicity guard) | YES (formalize existing budgets) | none |
| Task-execution-context block | YES (but adapt) | self-contained-item (evidence still needs file:line elsewhere) |
| Appearance-order IDs | YES (within task) | none |
| Explicit 4-rule tiebreakers | YES (additive) | none |
| Full determinism guarantee | NO | parallel-research |
| Single-pass no-loop spot-check | NO | zero-trust QA |
| Write-atomicity | NO | persistent .dev/tasks/ artifact (incremental writes) |
| Orchestrator does not apply patches | NO | self-contained-item (builder owns file) |
| Full R-### → T → D matrix as required | PARTIAL | input contract (no roadmap input) |
| Tier classification (keyword scoring for compliance) | NO | tier == research-depth in task-builder |
| Fidelity gate CLI | NO (no value) | n/a (architectural mismatch) |

evidence_status: complete (synthesis from 6 digests + FINAL-REPORT §3, §4, §6, §7 with file:line citations preserved).
