# Phase 9 -- Operational Handoff

**Goal:** Land first-class operational rollout deliverables — operator runbook (OPS-001), environment readiness check + script (OPS-002, aligned with INV-007 env-missing contract), observability procedure (OPS-003), rollback procedure with rehearsed once tabletop (OPS-004), lens contribution policy (OPS-005), and post-release metrics review framework (OPS-006). Exit when operators can run / monitor / resume / troubleshoot swarm jobs using documented commands and contracts, rollback procedure has been validated via tabletop exercise, lens contribution policy is published with review criteria, and post-release metrics review window is scheduled.

### T09.01 -- OPS-001 author operator runbook

| Field | Value |
|---|---|
| Roadmap | R-150 (OPS-001) |
| Deliverables | D-0131 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: doc renders + commands exercised by ops reviewer |

**Deliverables:**
1. `docs/swarm/operator-runbook.md` documenting run/status/logs/watch/resume/kill/attach workflows.

**Steps:**
1. [PLANNING] Enumerate workflows: run, status, logs, watch, resume, kill, attach.
2. [EXECUTION] Author runbook with single-line commands per workflow.
3. [EXECUTION] Document contract paths (return-contract.yaml, manifest, state, logs, done sentinel).
4. [VERIFICATION] Ops reviewer exercises every command against fixture job.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Commands enumerated; single-line examples; contract paths explained; tested by ops reviewer.
- Examples regenerated from final `--help` output to prevent drift.
- Cross-links to OPS-002/003/004.
- Doc passes markdownlint.

**Validation:**
- `markdownlint docs/swarm/operator-runbook.md` exits 0.
- Each example command exits 0 against fixture job.

**Dependencies:** T07.21 (Phase 7 exit), T08.18 (Phase 8 exit). **Rollback:** revert doc.

### T09.02 -- OPS-002 environment readiness check + script

| Field | Value |
|---|---|
| Roadmap | R-151 (OPS-002) |
| Deliverables | D-0132 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit, Bash |
| Sub-Agent | none |
| Verification | smoke: readiness script + doc |

**Deliverables:**
1. `scripts/swarm_env_readiness.sh` checking Python ≥3.10, UV, httpx, Click, Rich, tmux (optional), T2 proxy env vars.
2. `docs/swarm/env-readiness.md` documenting checklist + INV-007 env-missing path.

**Steps:**
1. [PLANNING] Enumerate prerequisites + T2 env vars (`T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`).
2. [EXECUTION] Author bash readiness script asserting each prerequisite.
3. [EXECUTION] Author doc with checklist + INV-007 reference.
4. [VERIFICATION] Run script on clean env; assert clear missing-var output.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Prerequisite checklist; readiness script; INV-007 env-missing path referenced; T2 env vars documented.
- Script exits non-zero on missing prerequisites.
- Doc cross-links to INV-007 failure contract.
- Doc passes markdownlint.

**Validation:**
- `bash scripts/swarm_env_readiness.sh` exits 0 with all vars present.
- `markdownlint docs/swarm/env-readiness.md` exits 0.

**Dependencies:** T02.11 (INV-007), T03.21 (env reader). **Rollback:** revert doc + script.

### T09.03 -- OPS-003 observability procedure

| Field | Value |
|---|---|
| Roadmap | R-152 (OPS-003) |
| Deliverables | D-0133 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: doc renders |

**Deliverables:**
1. `docs/swarm/observability-procedure.md` documenting state file / JSONL log / Markdown log / done sentinel + debugging recipes.

**Steps:**
1. [PLANNING] Enumerate 4 monitoring artifacts.
2. [EXECUTION] Author doc mapping artifacts to debugging workflows.
3. [VERIFICATION] Render doc.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Four monitoring artifacts documented; debugging recipes provided.
- Cross-links to monitoring-patterns doc (T07.10).
- Recipes cover common failure modes (env-missing, timeout, parse-error).
- Doc passes markdownlint.

**Validation:**
- `markdownlint docs/swarm/observability-procedure.md` exits 0.
- Doc references `.swarm-state.json`, `execution-log.jsonl`, `execution-log.md`, `done.json`.

**Dependencies:** T07.10, T07.14. **Rollback:** revert doc.

### T09.04 -- Checkpoint: Phase 9 mid-phase gate (tasks 1-3)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP9-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T09.01..T09.03 marked done in execution-log.
- `phase-9-cp1.md` checkpoint report written.
- Runbook + env-readiness + observability procedure published.
- Ops reviewer sign-off on runbook captured.

**Validation:**
- All 3 docs render cleanly via markdownlint.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T09.01..T09.03.

### T09.05 -- OPS-004 rollback procedure (rehearsed once)

| Field | Value |
|---|---|
| Roadmap | R-153 (OPS-004) |
| Deliverables | D-0134 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: tabletop rehearsal sign-off |

**Deliverables:**
1. `docs/swarm/rollback-procedure.md` describing skill caller rollback, detached disable, artifact preservation.
2. Tabletop rehearsal sign-off captured.

**Steps:**
1. [PLANNING] Define rollback scenarios: thin-caller regression, detached mode failure, parity break.
2. [EXECUTION] Author rollback procedure document.
3. [EXECUTION] Schedule tabletop rehearsal with operator + release owners.
4. [VERIFICATION] Capture rehearsal sign-off + lessons learned in doc.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Skill rollback steps; detached disable steps; artifact preservation rules; rehearsed once.
- Tabletop sign-off captured in doc appendix.
- Procedure references MIG-003 reversal path.
- Doc passes markdownlint.

**Validation:**
- `markdownlint docs/swarm/rollback-procedure.md` exits 0.
- Doc contains "Rehearsal: completed on <date>" line.

**Dependencies:** T08.07 (MIG-003 retired shells), T07.11 (detached). **Rollback:** none — this is the rollback doc itself.
**Notes:** Critical: untested rollback procedures fail when needed (R-016 in roadmap risk register).

### T09.06 -- OPS-005 lens contribution policy

| Field | Value |
|---|---|
| Roadmap | R-154 (OPS-005) |
| Deliverables | D-0135 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: policy doc rendered |

**Deliverables:**
1. `docs/swarm/lens-contribution-policy.md` documenting 5 review criteria + validator reference.

**Steps:**
1. [PLANNING] Enumerate 5 criteria: real caller, §11.5 substring, recipe/template alignment, downstream command, suspect scrutiny.
2. [EXECUTION] Author policy doc with PR checklist.
3. [EXECUTION] Reference U-008 validator (T02.16).
4. [VERIFICATION] Render doc.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Policy doc covers all 5 review criteria; references registry validator.
- PR checklist embedded in policy doc.
- Suspect:true entries flagged for extra scrutiny.
- Doc passes markdownlint.

**Validation:**
- `markdownlint docs/swarm/lens-contribution-policy.md` exits 0.
- Doc references all 5 review criteria explicitly.

**Dependencies:** T02.16, T02.27. **Rollback:** revert doc.

### T09.07 -- OPS-006 post-release metrics review framework

| Field | Value |
|---|---|
| Roadmap | R-155 (OPS-006) |
| Deliverables | D-0136 |
| Effort | S |
| Risk | LOW |
| Tier | LIGHT |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: doc renders |

**Deliverables:**
1. `docs/swarm/post-release-metrics.md` enumerating metrics + review window + backlog-feedback loop.

**Steps:**
1. [PLANNING] Enumerate metrics: validation failures, env-missing contracts, resume usage, custom prompt guard failures.
2. [EXECUTION] Author doc with metric definitions + review window schedule (e.g., 2-week post-release).
3. [EXECUTION] Define backlog-feedback loop.
4. [VERIFICATION] Render doc.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Metrics enumerated; review window scheduled post-release; findings feed backlog.
- Review window date + owner named.
- Backlog-feedback loop documented.
- Doc passes markdownlint.

**Validation:**
- `markdownlint docs/swarm/post-release-metrics.md` exits 0.
- Doc lists ≥4 metrics + review window.

**Dependencies:** T08.18 (Phase 8 exit). **Rollback:** revert doc.

### T09.08 -- Checkpoint: Phase 9 exit gate (end-of-phase + release gate)

| Field | Value |
|---|---|
| Type | CHECKPOINT (end-of-phase) |
| Deliverables | D-CP9-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T09.01..T09.07 marked done in execution-log.
- `phase-9-cp2.md` end-of-phase checkpoint written.
- OPS-001..006 all published; rollback rehearsal completed; ops reviewer sign-off captured.
- Release-readiness criteria met: operators can run/monitor/resume/troubleshoot swarm jobs via documented contracts.

**Validation:**
- All 6 OPS docs render cleanly via markdownlint.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T09.01..T09.07. **Rollback:** none — release gate.
**Notes:** M9 exit marks production-handoff completion for the swarm orchestrator.
