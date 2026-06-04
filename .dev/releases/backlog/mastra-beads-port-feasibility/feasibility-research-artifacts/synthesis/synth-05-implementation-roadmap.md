# Synthesis 05: Implementation Plan and Phased Roadmap (Report Section 8)

**Research question:** A staged roadmap to port/recreate SuperClaude's CLI orchestration in **Mastra + Backlog.md + Beads** as a multi-tenant company orchestration layer.

**Recommended approach:** **Option A — Hybrid adapter-first.** `synth-04-options-recommendation.md` was not present at synthesis time; Option A is therefore assumed per task instruction, and it is independently corroborated by the data-model evidence in `07-target-data-model-and-ownership.md:173-184` ("Hybrid adapter-first is favored by data-model risk… native Mastra rewrite is higher-risk because it must replace subprocess, parser, telemetry, gates, and artifact ownership at once").

**Status:** Complete
**Date:** 2026-06-02

---

## 8.0 Reading Guide and Ground Rules

This section is a **phased roadmap**, not a code-ready implementation spec. Several prerequisite decisions remain open (primary work-of-record, Mastra Enterprise licensing, governance/control-plane ownership); steps that depend on those decisions are explicitly marked **[DECISION-GATED]** and must not be treated as buildable until the gating decision is made.

**Authority order:**

1. **Codebase is source of truth.** Current SuperClaude CLI contracts (parser shapes, gate semantics, step registries, IDs) are verified in research files 01–11 and govern. They are preserved verbatim across adapters.
2. **External capabilities** (Mastra/Backlog.md/Beads/MCP governance) come from `web-01`..`web-04` (dated 2026-06-02, `provider=tavily`). Every external capability the roadmap depends on is cited to its web source; capabilities flagged HIGH-risk in web research (e.g. Mastra workflow rerun/replay semantics, EE licensing) are surfaced as go/no-go criteria, never assumed.

**Evidence binding:** Steps cite `file:line` for codebase contracts and source URLs for external claims. Claims that remain `[UNVERIFIED]` in upstream research stay `[UNVERIFIED]` here.

**Phase overview:**

| # | Phase | One-line goal | Primary go/no-go |
|---|---|---|---|
| 0 | Discovery & decisions | Pin contracts, choose work-of-record, scope licensing | Decisions D1–D5 recorded |
| 1 | Adapter MVP (read-only) | Import current artifacts into Backlog.md + Beads, round-trip-safe | Parser round-trip parity passes |
| 2 | Hybrid pilot | Wrap ONE real pipeline (`tasklist validate`) behind a Mastra workflow step | Pilot parity vs native CLI passes |
| 3 | Parity port | Wrap `roadmap run` + sprint execution; reproduce gates/checkpoints/hooks | Artifact + gate parity suite passes |
| 4 | Multi-tenant hardening | Add governance/control-plane, tenant identity/audit/cost | EE + governance decisions resolved |
| 5 | Rollout | Progressive production rollout behind the control plane | Operational + recovery gates pass |

---

## 8.1 Phase 0 — Discovery and Foundational Decisions

**Goal:** Lock the contracts that must survive the port, and make the five decisions that gate every later phase, before any adapter or workflow code is written. No execution code in this phase; output is an inventory + a decision record.

**Dependencies:** None (entry phase). Consumes research files 01–11, `web-01`..`web-04`, `07-target-data-model-and-ownership.md`, `09-gap-fill-checkpoint-contract.md`.

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 0.1 | Freeze the **stable-ID contract** as the cross-system reconciliation key | `sprint/config.py:374-377`; `07-...ownership.md:41,100` | IDs `TASK-*`, `R-###`, `T<PP>.<TT>`, `D-####`, `D-CP*` already appear in current files and parsers. Catalog every ID producer/consumer. Rule: adapters preserve IDs verbatim, never regenerate on import/export (`07-...:109`). |
| 0.2 | Inventory the **sprint parser compatibility contract** that any tasklist adapter must satisfy | `sprint/config.py:15-26,28-49,374-492`; `09-...:131-141` | Phase discovery names (`phase-N-tasklist.md` etc.), `### T<PP>.<TT> -- Title` heading regex, `**Dependencies:**`, `**Command:**`, `\| Classifier \|` table, `**Deliverables:**` description, `count_tasks_in_file` count. This is the round-trip acceptance surface for Phase 1. |
| 0.3 | Adopt the **canonical checkpoint contract** as the emit shape | `09-gap-fill-checkpoint-contract.md:127-154` | Numbered checkpoint task entries `### T<PP>.<NN> -- Checkpoint: ...`, one mid-phase per 5 tasks + one end-of-phase last task, each with a `Checkpoint Report Path: TASKLIST_ROOT/checkpoints/...` line. Do NOT emit legacy sibling `### Checkpoint:` headings. Record the known per-task `_verify_checkpoints()` gap (`executor.py:1259-1301`) as a Phase 3 risk. |
| 0.4 | **[DECISION D1 — work-of-record]** Choose primary owner: Backlog.md vs Beads | `web-02:115-118`; `web-03:140`; `07-...:181,193` | Recommended split (hypothesis, `[UNVERIFIED target]`): Backlog.md owns human prose/tasks/docs/decisions (`web-02:115`); Beads owns dependency DAG + ready-queue + claims + memory + gates (`web-03:140`). One canonical status owner — dual owners cause drift (`07-...:107,193`). Backlog.md↔Beads integration is **not mature** (`web-02:93-98`, request #588); pick a narrow import/export sync, not broad integration. |
| 0.5 | **[DECISION D2 — Mastra licensing track]** Decide OSS vs Enterprise track now | `web-01:51-57,78-83,89` | Apache-2.0 core covers workflows/steps/storage/observability/MCP; production RBAC/SSO/FGA/audit/on-prem are EE-gated (`@mastra/core/auth/ee`, `web-01:53`). Local/single-tenant pilot can run OSS; company-wide multi-tenant likely requires an EE conversation. This decision gates Phase 4, not Phases 1–3. |
| 0.6 | **[DECISION D3 — governance/control-plane]** Acknowledge that Mastra+Backlog+Beads is NOT a governance plane | `web-04:93-99,125-127,140` | None of the three provides tenant isolation, per-invocation audit, cost attribution, tool catalog, or policy enforcement. A separate control-plane layer is required before company-wide multi-tenant deployment. Scope it as a Phase 4 deliverable, not a Phase 1–3 dependency. |
| 0.7 | **[DECISION D4 — runtime substrate]** Pick the subprocess/exec seam for the hybrid wrapper | `web-01:30-35,88,91`; `pipeline/process.py:24-35` | Current seam is `claude --print --verbose --output-format ... ` over stdin (`07-...:36`). Candidate target is Mastra Workspace `WorkspaceSandbox.executeCommand()` (`@mastra/core@1.1.0`, `web-01:32`). **Does NOT prove Claude Code hook/permission parity** (`web-01:35,88`) — schedule a safety spike (Phase 2). Hybrid track keeps calling the existing Python CLI first. |
| 0.8 | **[DECISION D5 — Beads deployment mode + version pin]** | `web-03:61-67,68-74,19-25,135` | Embedded mode is single-writer ("database is locked"); multi-agent orchestration requires **server / shared-server mode** (`web-03:66,122`). Pin version and gate upgrades — v1.0.5 carries a sync/migration warning (issue #4259, `web-03:21`). Integrate via `bd ... --json` with envelope compatibility (`web-03:38,133`), never JSONL reads. |
| 0.9 | Produce a **Decision Record + Contract Inventory** artifact and an architecture diagram of the proposed ownership split | output: `discovery/decision-record.md`, `discovery/contract-inventory.md` | Ownership matrix from `07-...:93-102`. This artifact is the input gate to Phase 1. |

**Go/No-Go Gate G0 → Phase 1:** PROCEED only if D1 (work-of-record) and D4 (runtime seam for hybrid) are recorded, and the parser/checkpoint contracts (0.2, 0.3) are inventoried with citations. D2/D3/D5 may remain provisional (they gate Phase 4) but must be logged. NO-GO if work-of-record is unresolved — every adapter mapping depends on it (`07-...:181`).

---

## 8.2 Phase 1 — Adapter MVP (Read-Only, No Ownership Transfer)

**Goal:** Build **read-only importers** that ingest existing `.dev/tasks` and tasklist bundles into Backlog.md (prose) and Beads (dependency graph) **without mutating current files**, and prove the import is round-trip-safe against the sprint parser. This de-risks ID/graph/artifact mapping before any execution or ownership change (`07-...:179-180`).

**Dependencies:** G0 passed. D1 (work-of-record), D5 (Beads mode/version) recorded. Beads server-mode instance provisioned (`web-03:122`); Backlog.md initialized (`backlog init`, `--no-git` if required, `web-02:54`).

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 1.1 | Build a **tasklist-bundle → Backlog.md importer** | reads `tasklist-index.md` + `phase-N-tasklist.md`; writes via `backlog` CLI/MCP | Map per Contract 1 (`07-...:114-125`): phase H1 → milestone/list; `### T<PP>.<TT>` → task with ID as **external ID** (not display text); body sections → `description`/`implementationPlan`/`implementationNotes`; AC → acceptance criteria; `**Dependencies:**` → `dependencies` + retained body text. Mutate only through `task_create`/`task_edit` (`web-02:117`), never hand-edit markdown. |
| 1.2 | Respect Backlog.md schema limits; map non-native metadata explicitly | `web-02:27-38` | MCP task schemas use `additionalProperties:false` (`web-02:33-34`) — SuperClaude-specific fields (tier, classifier, risk, `R-*`/`D-*` IDs) cannot be arbitrary frontmatter. Map to supported fields (`labels`, `milestone`, `references`, `documentation`, `modifiedFiles`) or body sections (`web-02:118`). Use CLI for `decision create` — decisions are not in the current MCP MVP (`web-02:47-49`). |
| 1.3 | Build a **tasklist/Backlog → Beads graph mirror** | `bd create`, `bd dep add`, `bd update --json`; `web-03:27-31,133` | Per Contract 2 (`07-...:127-138`): root issue per tasklist bundle, phase parent issue/epic, one issue per `T<PP>.<TT>`, directed edges from `TaskEntry.dependencies`. Use typed deps (`blocks`, `parent-child`, `web-03:41`). Beads rejects cycles at write (`web-03:42`). Mirror checkpoint tasks as verification nodes, not implementation blockers unless they block the next phase (`07-...:135`). |
| 1.4 | Encode "work-done vs merged/validated" barriers as **Beads gates** | `bd gate`; `web-03:48-52` | Map SuperClaude validation/PR-merge phases to gate issues: `gh:pr` (PR merged), `gh:run` (CI), `human` (manual approval), `timer` (`web-03:49`). This is a direct fit for the certify/wiring/validation distinction in the current pipeline. |
| 1.5 | Make every importer **idempotent and additive** | importer code; `07-...:165` | Re-running an import must not duplicate Backlog rows or Beads edges (`07-...:165`). Key all upserts on stable IDs (0.1). Never silently rewrite human markdown if the Beads graph diverges — emit a **proposed graph-patch report** instead (`07-...:96,134`). |
| 1.6 | Build the **round-trip parity exporter + test** (acceptance gate) | exporter; `sprint/config.py` `discover_phases()`, `parse_tasklist_file()`, `count_tasks_in_file()` | Export Backlog/Beads state back to `tasklist-index.md` + `phase-N-tasklist.md` and assert: (a) `discover_phases()` finds every phase, (b) `parse_tasklist_file()` reads every task, (c) task counts equal `count_tasks_in_file()`, (d) exported dependency lists are identical to parser-extracted `TaskEntry.dependencies` unless a human-approved graph patch exists (`07-...:125,138,180`). |
| 1.7 | Seed a representative corpus mixing both checkpoint shapes | `.dev/releases/complete/cliEval/phase-1-tasklist.md:251` (numbered); `.dev/test-sprints/smoke-test/phase-1-tasklist.md:172` (legacy) | Import must normalize legacy sibling `### Checkpoint:` into numbered checkpoint tasks before re-export (`09-...:152`), proving the importer handles the real mixed corpus. |

**Go/No-Go Gate G1 → Phase 2:** PROCEED only if the round-trip parity test (1.6) passes on the mixed corpus (1.7) AND importers are proven idempotent (1.5). NO-GO if any task is dropped, any dependency edge diverges without an approved patch, or checkpoint normalization is lossy. This phase changes **no execution behavior** — current Python orchestration remains the oracle (`07-...:182`).

---

## 8.3 Phase 2 — Hybrid Pilot (Wrap ONE Real Pipeline)

**Goal:** Prove a Mastra workflow can drive a real SuperClaude pipeline end-to-end by **wrapping the existing CLI as a subprocess step** (hybrid, not native reimplementation), with one pipeline only. Validate durability, gate handling, and trace capture against the native CLI as oracle.

### Pilot recommendation (smallest safe first slice)

**Wrap `superclaude tasklist validate` as the first Mastra-wrapped pipeline.** Rationale, evidence-bound:

- It is the **single smallest pipeline**: one LLM fidelity step with one strict gate, not a generator — `tasklist/executor.py:191-218` wires a single `tasklist-fidelity` step; `tasklist/executor.py:251-276` returns pass only when there are zero HIGH-severity deviations (`02-...:153-154,204-206`).
- It has a **clean, parseable pass/fail contract**: `high_severity_count` parsed from report frontmatter; missing/unparseable report = fail (`tasklist/executor.py:221-248`). That is a trivial Mastra scorer/gate to mirror.
- It is **read-only / non-destructive** — it validates roadmap→tasklist alignment and writes a report; it mutates no source (`tasklist/prompts.py:17-148`). Lowest blast radius for a first wrapped run.
- It reuses the **shared pipeline layer** (`tasklist/executor.py:23-25,259-263` → `execute_pipeline`), so lessons transfer directly to `roadmap run` in Phase 3.

Defer `roadmap run` to Phase 3: it carries parallel generate steps, convergence mode, compression sidecars, deviation registry, trailing gates, and post-run validation (`02-...:40,89-96`) — too much surface for a first slice.

**Dependencies:** G1 passed. D4 (runtime seam) recorded. Mastra OSS instance with composite storage (PostgreSQL/libSQL for snapshots; avoid in-memory, `web-01:103`). A Backlog.md/Beads-derived input or a native roadmap+tasklist input pair.

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 2.1 | Define a Mastra workflow with **one step that shells out** to `superclaude tasklist validate` | `createWorkflow()`/`createStep()` (`web-01:23-28`); `WorkspaceSandbox.executeCommand()` (`web-01:30-35`) | Hybrid wrapper: the Mastra step invokes the existing CLI; SuperClaude stays the execution oracle (`07-...:150,182`). Capture stdout/stderr, exit code, and the written report path. |
| 2.2 | Mirror the CLI's gate as a **Mastra scorer/validator** | mirror of `tasklist/executor.py:221-248`; `web-01:46` (eval/scorer) | Parse `high_severity_count` from the report; map zero-HIGH → workflow PASS, else FAIL. Assert the Mastra verdict equals the native CLI exit code (`tasklist/commands.py:181-185`). |
| 2.3 | Run the **subprocess-safety spike** (gates D4 for later phases) | `web-01:88,91,101-102`; `eval/isolation.py:456-642` | Mastra Workspace exec does NOT replicate Claude Code hooks/permission/freshness/staging discipline (`web-01:35,88`). Reuse the eval harness isolation model — per-run HOME, scratch-root allowlist, containment guard (`eval/isolation.py:224-260,456-642`) — as the parity target for safe command execution. Record gaps; do not claim CLI parity (`web-01:101`). |
| 2.4 | Validate **durability: suspend/resume + failed-step restart** | `web-01:16-22,86` | Test Mastra `suspend()`/`resume()`, snapshot persistence across restart, and partial rerun. Rerun/replay/idempotency semantics are flagged HIGH-risk-unverified (`web-01:86`) — this step exists to verify them empirically, not assume them. Treat `@mastra/temporal` as experimental (`web-01:18,87`). |
| 2.5 | Capture **traces with SuperClaude IDs** as custom attributes | `web-01:44-49`; `07-...:149` | Attach `R-*`, `T<PP>.<TT>`, `D-*`, phase, tier, model, git branch/commit to every span (`07-...:149`; `web-01:105`). This is the join key between Mastra traces and Backlog.md/Beads records and the seed for cost attribution in Phase 4. |
| 2.6 | Reconcile the run result back into Backlog.md + Beads | Contract 4 (`07-...:154-165`) | On PASS: summarize execution-log entry in Backlog, close/check the Beads verification node. On FAIL: failure note + gate report + edge to a remediation issue. Reconciliation must be idempotent (`07-...:165`). |

**Validation/eval strategy for the pilot:** Run the SAME input through (a) native `superclaude tasklist validate` and (b) the Mastra-wrapped workflow; assert identical verdict, identical `high_severity_count`, and equivalent report content. Use the `eval/` harness pattern as the test substrate — capability preflight (`eval/commands.py:119-192`), ordered per-spec outcomes (`eval/orchestrator.py:164-299`), JSONL forensic logs and preserved-on-failure artifacts (`eval/runner.py:537-588,425-473`).

**Go/No-Go Gate G2 → Phase 3:** PROCEED only if (a) Mastra-wrapped verdict == native CLI verdict across the corpus, (b) suspend/resume + failed-step restart behave correctly (2.4), and (c) the subprocess-safety spike (2.3) produced an explicit parity/gap report. **NO-GO if Mastra rerun/recovery semantics cannot be demonstrated** — that is the load-bearing assumption for porting the stateful `roadmap`/`sprint` pipelines (`07-...:189`; `web-01:86`).

---

## 8.4 Phase 3 — Parity Port (Roadmap Run, Sprint Execution, Gates, Checkpoints, Hooks)

**Goal:** Extend the hybrid pattern to the **full orchestration surface**: wrap `superclaude roadmap run` and sprint execution behind Mastra workflows, reproduce the multi-step graph, gates, checkpoints, and Claude Code hooks as Mastra middleware/guards — while keeping the Python CLI as the execution oracle until parity is proven. Native reimplementation of any step happens **only after** that step passes a parity gate (`07-...:175,182`).

**Dependencies:** G2 passed. Mastra durable workflows validated (Phase 2). Beads server mode + gates live (Phase 1). This is the highest-risk phase — sprint Path A/B, isolation, and process supervision are flagged as the hardest port surface (`gaps-and-questions.md` RG-I7).

### 3a. Roadmap run (rich, mostly stateless-per-step pipeline)

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 3.1 | Map the roadmap **step graph** to a Mastra workflow, one node per registry step | `roadmap/executor.py:2003-2204` (`02-...:89`) | Wired order: `extract` → parallel `generate-{a}`/`generate-{b}` → `diff` → `debate` → `score` → `merge` → `anti-instinct` → `test-strategy` → `spec-fidelity` → `wiring-verification` → `deviation-analysis` → `remediate`. Mastra parallel steps for the two generate agents (`web-01:23-26`). Generate the graph from the authoritative step list — do NOT maintain a parallel matrix (avoid the `cli_portify` resume-drift anti-pattern, `04-...:69,75`). |
| 3.2 | Reproduce **gates** as Mastra guards/scorers, preserving gate modes | `roadmap/gates.py`; `pipeline/models.py:69-79` (`07-...:35`) | Preserve `GateMode` blocking vs `TRAILING` semantics. `wiring-verification` uses `WIRING_GATE` + `GateMode.TRAILING` + deterministic `run_wiring_analysis` (`roadmap/executor.py:2175-2184,1011-1031`). **Preserve, do not normalize:** `CERTIFY_GATE` is **defined but not wired in production** (`gates.py:1324-1351`; `executor.py:1947-2208`; `02-...:146`) — the port must not silently "fix" this; flag it as an open parity question. |
| 3.3 | Port **convergence + remediation** state machine | `roadmap/executor.py:1804-1897`; `roadmap/remediate.py:177-288`; `convergence.py:144-255` (`02-...:111,174-175`) | Stateful via `deviation-registry.json`, `spec-deviations.*`, `remediation-tasklist.*`, `.roadmap-state.json` (`02-...:111`). Mastra owns run state only after durability proven (`07-...:108`); until then, these JSON/markdown sidecars remain source of truth. Preserve compression-sidecar behavior (`gaps-and-questions.md` RG-I6). |
| 3.4 | Wrap **post-run auto-validation** | `roadmap/executor.py:3409-3447`; `validate_executor.py:183-236` (`02-...:102,106) | `roadmap run` auto-invokes validation, resolving inputs from `.roadmap-state.json` (`02-...:106`). Preserve release-dir resolution semantics (`sprint/config.py:236-272`, `07-...:82`). |

### 3b. Sprint execution (hardest surface)

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 3.5 | Reproduce **Path A (per-task) vs Path B (freeform)** execution routing | `sprint/executor.py:1118-1133,1259-1301`; `process.py:170,187-195` (`09-...:30-32,56-58`) | Phases with numbered `### T<PP>.<TT>` headings route per-task (`executor.py:1259-1301`); freeform phases use the full-phase prompt (`process.py:170`). Adapter must emit numbered tasks so execution is deterministic per-task (`09-...:153`). |
| 3.6 | Wire **checkpoint verification** into the per-task path (closes the known gap) | `sprint/executor.py:1259-1301` vs `1512-1531`; `checkpoints.py:18-94` (`09-...:106-110`) | Per-task branch does NOT call `_verify_checkpoints()` (`09-...:121`). The port should verify checkpoints after task aggregation (or run `verify-checkpoints` after, `09-...:154`). `checkpoints.py` already accepts numbered + legacy headings (`09-...:48`). Mirror checkpoint reports as Backlog docs + Beads verification-node closure. |
| 3.7 | Map **sprint phases/tasks/checkpoints** to Beads graph + ready-queue scheduler | `bd ready --json`, `bd update --claim`; `web-03:28,133`; Contract 3 (`07-...:140-152`) | Use `bd ready --json` as scheduler input and `bd update <id> --claim --assignee <agent>` for atomic acquisition (`web-03:28,132`). Honor session attribution caveat — `--claim` session-loss bug is actively changing (`web-03:70`). One Mastra stage per phase; phase `Execution Mode` (`claude`/`python`/`skip`, `sprint/config.py:67-119`) selects the Mastra runner type. |
| 3.8 | Preserve **status/result/telemetry/budget models** as Mastra run metadata + summaries | `sprint/models.py` enums (`07-...:50-60`); `web-01:44-49` | Map `StepStatus`/`TaskStatus`/`GateOutcome`/`PhaseStatus`/`SprintOutcome` to Mastra run states; route high-volume telemetry (`MonitorState`, stdout/stderr) to Mastra traces/observability, NOT into Backlog/Beads bodies — only summaries there (`07-...:65,97,163`). |

### 3c. Hooks → Mastra middleware/guards

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 3.9 | Reproduce **Claude Code hooks** as Mastra middleware/guards + governance pre-checks | `web-01:35,104`; `web-01:106` (MCP `requireToolApproval`) | Recreate UV-only Python rule, `.claude/` source-of-truth/staging discipline, fork-PR target, freshness pre-edit checks, safe command execution as explicit Mastra guards or pre-step validators (`web-01:104`). Hook portability is flagged `[UNVERIFIED]` (`gaps-and-questions.md` RG-I5) — verify each hook's trigger surface before claiming parity. Use `requireToolApproval` for human-in-the-loop tool gates (`web-01:60`). |
| 3.10 | Begin **selective native reimplementation** of deterministic steps only | per-step parity gate (3.x) | Deterministic Python steps (`run_wiring_analysis`, remediation generation, classification, audit primitives `04-...:255-258`) can be reimplemented natively in Mastra/TS once their step passes parity. LLM steps stay hybrid (call existing CLI) until explicitly re-validated. Never replace subprocess+parser+telemetry+gates+artifacts in one move (`07-...:173`). |

**Validation/eval strategy (parity suite):** This is the core acceptance machinery for Phase 3.

| Parity dimension | Method | Evidence anchor |
|---|---|---|
| Artifact parity | Diff Mastra-produced artifacts vs native CLI artifacts for the same input (roadmap outputs, tasklist bundle, checkpoint reports, return contracts). | `cli_portify/executor.py:283-372` return-contract; `09-...` checkpoint paths |
| Gate parity | Assert each gate's verdict + mode (blocking/trailing/deferred) matches native. | `roadmap/gates.py`; `pipeline/models.py:69-79` |
| Graph/order parity | Assert executed step order + dependency order equals native + Beads `bd ready` order. | `roadmap/executor.py:2003-2204`; `sprint/config.py` |
| Safe-execution parity | Reuse eval HOME isolation, scratch-root allowlist, JSONL forensics, retry-once, ordered outcome accounting. | `eval/isolation.py:456-642`; `eval/orchestrator.py:164-299`; `eval/runner.py:833-878`; `eval/retry.py:92-165` |
| Recovery parity | Test crash recovery / resume against native sprint recovery + manifest. | `sprint/executor.py:1702-1721`; `09-...:64-66` |

**Go/No-Go Gate G3 → Phase 4:** PROCEED only if the parity suite passes for `roadmap run` AND a representative sprint (artifact + gate + order + safe-execution + recovery parity), AND every hook is reproduced as a verified guard (3.9). NO-GO if any gate verdict, checkpoint enforcement, or recovery path diverges from native behavior, or if hook parity is unproven. Native step reimplementation (3.10) is allowed only for steps that individually passed parity.

---

## 8.5 Phase 4 — Multi-Tenant Hardening

**Goal:** Convert the single-tenant parity port into a company-wide multi-tenant orchestration layer. **This phase is gated on four explicit decisions/builds that Mastra + Backlog.md + Beads do NOT provide on their own.**

> **CRITICAL FLAGS (per task rule 4) — none of these can be skipped:**
>
> 1. **Mastra Enterprise licensing decision (D2).** Production RBAC, SSO, FGA, audit logs, on-prem/VPC, and Studio Auth/Agent Builder are EE-licensed (`@mastra/core/auth/ee`, `web-01:51-57,80-82,89`). OSS Mastra leaves Studio/API public without auth (`web-01:52`). Company-wide multi-tenant deployment **requires an Enterprise conversation** — this is a go/no-go business decision, not an engineering toggle.
> 2. **A separate governance/control-plane layer is required (per `web-04`).** Mastra+Backlog+Beads is an orchestration/task substrate, NOT a governance plane (`web-04:93-99,125-127,140`). The missing layer = tenant isolation, policy enforcement, tool catalog/change control, audit, cost attribution, approvals (`web-04:125,145`).
> 3. **Tenant-aware identity, audit, and cost attribution are net-new.** Current scoped models have NO tenant/actor fields — only a sprint-local `TurnLedger` budget (`07-...:102,197`; `web-04:127`). Multi-tenant agents need **separate trigger / execution / authorization / tenant / attribution identities** (`web-04:66-71`); conflating execution and tenant identity causes silent access-control bugs (`web-04:68`).
> 4. **A primary work-of-record decision between Backlog.md and Beads must be final (D1 from Phase 0).** Dual status owners create drift (`07-...:107,193`); confirm and freeze the canonical owner before scaling to many tenants/teams.

**Dependencies:** G3 passed. D2 (EE track) and D1 (work-of-record) **resolved, not provisional**. D3 (control-plane) scoped.

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 4.1 | **[DECISION-GATED on D2]** Stand up Mastra auth + RBAC/FGA on the EE track (or document OSS limits) | `web-01:53,56,80-82` | If EE: configure `StaticRBACProvider`/`DEFAULT_ROLES`/`MastraFGAPermissions`, Studio Auth SSO, WorkOS FGA. If OSS-only: explicitly bound deployment to non-public/single-tenant and record the gap. Without auth, Agent Builder/Studio are open to anyone reachable (`web-01:80`). |
| 4.2 | **[DECISION-GATED on D3]** Build the governance/control-plane service | `web-04:145` | Tenant registry; user/team/agent identity mapping; RBAC/ABAC policy store; tool/skill catalog + ownership registry; MCP server inventory; approval policy engine; audit/event log; cost + rate/budget attribution; environment separation + rollout controls. This is a **separate service**, not a Mastra config. |
| 4.3 | Add an **MCP/AI gateway** for any remote/shared MCP surface | `web-04:27-35,42,49,146` | Enforce OAuth 2.1 for remote MCP (PRM, resource indicators, audience binding, token validation, `web-04:27`). **Forbid token passthrough** (`web-04:34`). Pin to single issuer/tenant; reject other-realm tokens; never tie auth to session ID (`web-04:42`). Tool-level allowlists, no wildcard scopes (`web-04:49`). |
| 4.4 | Map SuperClaude command/skill privileges to **granular scopes** | `web-04:52,147` | Avoid one broad `superclaude:*` permission. Map commands/skills/tools to read-only / code-edit / git-write / external-search / infra-change / destructive / admin; require progressive elevation + approval for higher-risk actions (`web-04:147`). Aligns with the existing per-skill ownership concept (`web-04:148`). |
| 4.5 | Implement **per-invocation audit records** | `web-04:149` | Every orchestration action: timestamp, tenant, user, agent/client, workflow/task ID, tool/skill name+version+schema, input classification, target system, result, policy decision, approval ID, cost, correlation ID. Feed Mastra observability into the governance plane; join traces with Backlog.md/Beads IDs (`web-04:151`; uses the 2.5 trace-attribute join key). |
| 4.6 | Implement **cost attribution + budget/rate enforcement** | `web-04:150`; `07-...:58,183` | Promote the sprint-local `TurnLedger` (`sprint/models.py:692-777`) to a first-class tenant/team/project/task/agent cost model (model tokens, tool calls, retries, evaluations, workflow runs) with budget alerts/limits (`web-04:150`; `07-...:183`). MCP/FinOps is outside MCP itself (`web-04:80-85`). |
| 4.7 | Promote **Beads to server/shared-server mode** for multi-tenant writers, with per-tenant prefixes | `web-03:66,82-85,122` | Server mode for concurrent writers (`web-03:66`); shared-server with unique per-project/tenant prefix + database name (`web-03:83`). Enforce backup/restore + push/pull smoke tests as adoption gates (`web-03:135`). Keep version pinned (D5). |
| 4.8 | Enforce **one canonical work-of-record** at scale and curate the tool catalog | `web-04:111-115,153`; `07-...:107` | Freeze D1. Do not expose raw MCP server/tool catalogs broadly — publish curated, versioned, reviewed workflow-tools aligned to SuperClaude commands/skills (`web-04:153,111-115`). Backlog.md and Beads each stay scoped; neither owns runtime authorization or tenant isolation (`web-04:152`). |

**Go/No-Go Gate G4 → Phase 5:** PROCEED only if (a) D1 + D2 are final, (b) the governance/control-plane (4.2) and MCP gateway (4.3) enforce tenant isolation + per-invocation audit + cost attribution on a two-tenant test, and (c) granular scopes + approval gates (4.4) are live. NO-GO if any tenant can read another tenant's tasks/traces/costs, if token passthrough is possible, or if EE-gated features are assumed without a licensing decision. **Do not deploy company-wide on Mastra+Backlog+Beads alone** (`web-04:140`).

---

## 8.6 Phase 5 — Rollout

**Goal:** Progressive production rollout of the multi-tenant orchestration layer behind the control plane, starting with the lowest-risk pipeline and tenant, with operational + recovery gates at each expansion.

**Dependencies:** G4 passed. Governance plane, MCP gateway, audit, and cost attribution live. Beads server mode + backup/restore validated. EE licensing (if chosen) procured.

| Step | Action | Files or systems | Details |
|---|---|---|---|
| 5.1 | Roll out the **pilot pipeline (`tasklist validate`) to a single internal tenant** first | Phase 2 workflow + Phase 4 governance | Lowest blast radius, read-only, proven in Phase 2. Validate audit/cost/scope enforcement end-to-end on a real tenant before adding stateful pipelines. |
| 5.2 | Expand to `roadmap run`, then sprint execution, **one pipeline at a time** | Phase 3 workflows | Gate each expansion on its own parity suite (G3 dimensions) re-run in the production-config environment. Honor merge-freeze / release-cut operational constraints. |
| 5.3 | Add tenants progressively with **isolation re-validation per onboarding** | governance plane (4.2); Beads prefixes (4.7) | Re-run the two-tenant isolation test (G4) at each new tenant. Verify per-tenant cost attribution and budget limits actually fire. |
| 5.4 | Operationalize **recovery + backup hygiene** | `web-03:135`; `sprint/executor.py:1702-1721` | Scheduled `bd backup`/`bd dolt push`, tested restore, sprint manifest + crash-recovery drills. Beads is safe for internal use only with tested backup/restore (`web-03:126`). |
| 5.5 | Keep a **native-vs-hybrid fallback** for any step not yet natively reimplemented | Phase 3.10 | Steps still in hybrid mode call the existing CLI; retain the ability to fall back to native Python orchestration if a Mastra path regresses. Decommission the Python oracle per-step only after sustained production parity. |
| 5.6 | Establish **drift detection** between Backlog.md, Beads, and Mastra run state | round-trip test (1.6); reconciliation (2.6) | Run the round-trip parity + idempotent reconciliation continuously in production to catch ownership drift early (`07-...:107,193`). |

**Go/No-Go Gate G5 (production-readiness, recurring):** Each rollout increment PROCEEDS only if parity suite + isolation test + recovery drill pass in the production-config environment. NO-GO / rollback if drift detection (5.6) flags divergence, a recovery drill fails, or cost/audit attribution is incomplete.

---

## 8.7 Consolidated Decision Gates (cross-phase)

| ID | Decision | Owner phase | Gates | Default if unresolved |
|---|---|---|---|---|
| D1 | Primary work-of-record: Backlog.md vs Beads | Phase 0 (final by Phase 4) | G0, G4 | NO-GO to Phase 1 — all mappings depend on it |
| D2 | Mastra OSS vs Enterprise licensing track | Phase 0 (final by Phase 4) | G4 | OSS pilot allowed; multi-tenant NO-GO until resolved |
| D3 | Separate governance/control-plane ownership | Phase 0 (built Phase 4) | G4 | Multi-tenant NO-GO without it |
| D4 | Runtime subprocess/exec seam (hybrid wrapper) | Phase 0 | G0, G2 | Hybrid = keep calling existing CLI |
| D5 | Beads deployment mode + version pin | Phase 0 (server mode by Phase 4) | G1, G4 | Embedded = solo eval only |

## 8.8 Validation and Eval Strategy (cross-phase summary)

The roadmap reuses the existing `cli/eval` harness patterns as the test substrate at every phase, and adds artifact/gate parity tests:

| Capability | Reuse from | Used in |
|---|---|---|
| Round-trip parser parity (import → export → `discover_phases`/`parse_tasklist_file`/`count_tasks_in_file`) | `sprint/config.py`; `07-...:125,180` | Phase 1 (G1), Phase 5 drift |
| Capability preflight (`claude --version`, `~/.claude/` checks) | `eval/commands.py:119-205` | Phases 2–3 |
| Safe parallel execution (per-run HOME, scratch-root allowlist, containment guard) | `eval/isolation.py:224-260,456-642` | Phases 2–3 (G2, G3) |
| Ordered outcome accounting (never drop an outcome, preserve spec order) | `eval/orchestrator.py:164-299` | Phase 3 parity suite |
| Forensic JSONL logs + preserve-failed-HOME | `eval/runner.py:537-588,425-473` | Phases 2–5 |
| Retry-once policy for flaky (MCP) steps | `eval/retry.py:92-165` | Phases 2–3 |
| Return-contract / artifact diffing | `cli_portify/executor.py:283-372` | Phase 3 artifact parity (G3) |
| Gate verdict + mode parity | `roadmap/gates.py`; `pipeline/models.py:69-79` | Phase 3 gate parity (G3) |
| Checkpoint enforcement parity | `09-...:106-110`; `checkpoints.py:18-94` | Phase 3 (G3) |
| Recovery/resume parity | `sprint/executor.py:1702-1721`; `09-...:64-66` | Phases 3, 5 |
| Tenant isolation + audit + cost two-tenant test | net-new (`web-04:125,149-150`) | Phase 4–5 (G4, G5) |

## 8.9 Summary

The recommended path is **hybrid adapter-first** (Option A), corroborated by data-model risk evidence (`07-...:173`): preserve the verified current contracts — stable IDs, sprint parser shapes, numbered-checkpoint contract, shared pipeline/gate models, and the Claude CLI subprocess seam — while adding read-only adapters, then a single wrapped pipeline, then full parity, then multi-tenant governance.

The smallest safe first slice is wrapping **`superclaude tasklist validate`** (a single-step, strict-gate, non-destructive pipeline; `tasklist/executor.py:191-218,221-248`) behind a Mastra workflow. Each phase has an explicit go/no-go gate; the load-bearing early gate is **G2 — proving Mastra rerun/recovery/durability semantics** (`web-01:86`), without which the stateful `roadmap`/`sprint` ports are infeasible.

Multi-tenant hardening is NOT a thin add-on: it requires a **Mastra Enterprise licensing decision**, a **separate governance/control-plane layer** (`web-04:140,145`), **tenant-aware identity/audit/cost attribution** with separated trigger/execution/authorization/tenant/attribution identities (`web-04:66-71`), and a **final primary work-of-record decision between Backlog.md and Beads** (`07-...:193`). Mastra + Backlog.md + Beads alone are an orchestration/task substrate, not an enterprise governance plane.

This roadmap is **phase-gated and decision-gated**, not code-ready: `[DECISION-GATED]` and `[UNVERIFIED]` markers indicate where prerequisite decisions or hands-on validation must precede implementation.
