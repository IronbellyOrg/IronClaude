# Phase 1 -- Tier 1 Foundational Detector Trio

**Phase Goal:** Land the three highest-priority `/sc:reflect` refactors (B1, C4, C1) that together cover the causal narrative of the `/opt/jenkins/artifacts/` host-path regression: C4 prevents the regression from being introduced, C1 prevents it from being invisible at the edit site, B1 prevents it from being undetectable after the fact. Per Phase 5 matrix, this trio has zero overlap and the highest leverage per LOC (~130-180 lines total).

### T01.01 -- Track-state audit (canonical/mirror in `git ls-files`)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | Mirror file at `pipeline-script-phase3.1.groovy:289-297` was untracked in git, so `git diff` / `git blame` / `git log -S` could not surface the missed §4.2 hunk. Rank 1 of 14 (Priority 0.937; Likelihood 0.93; Effectiveness 0.95). |
| Effort | M |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [████████--] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0001/spec.md`
- `TASKLIST_ROOT/artifacts/D-0001/notes.md`
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a Track-state audit subroutine that runs `git ls-files <path>` for every canonical and mirror path the protocol touches and emits a `DISCREPANCY: untracked-substrate` block when output is empty for a path that the protocol claims is "in sync".

**Steps:**
1. **[PLANNING]** Load the current `/sc:reflect` skill source and identify every callsite where the protocol reads or claims "in-sync" state for a (canonical, mirror) pair.
2. **[PLANNING]** Confirm no existing track-state guard exists in `/sc:reflect` (grep for `git ls-files` / `untracked` mentions) and record dependencies on substrate-listing routines.
3. **[EXECUTION]** Add a `track_state_audit(canonical_path, mirror_path)` subroutine to the protocol that invokes `git ls-files --error-unmatch <path>` for each path and captures stderr exit-code.
4. **[EXECUTION]** Wire the subroutine into the existing claim-evaluation loop so any "in-sync" assertion against an untracked path is downgraded to `DISCREPANCY: untracked-substrate -- claim cannot be verified by git`.
5. **[EXECUTION]** Add a fixture-style test invocation in the protocol doc: run against `pipeline-script-phase3.1.groovy` (untracked mirror) and confirm the DISCREPANCY emits.
6. **[VERIFICATION]** Execute the protocol against the bug fixture and confirm the DISCREPANCY block names both canonical and mirror paths and quotes the empty `git ls-files` output as evidence.
7. **[COMPLETION]** Document the subroutine, its exit conditions, and the regression test in `TASKLIST_ROOT/artifacts/D-0001/spec.md` and copy the run log to `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `track_state_audit` (or equivalent) subroutine and at least one wiring callsite that downgrades an "in-sync" claim to a DISCREPANCY when `git ls-files <path>` is empty.
- Running the patched protocol against `configurations/jenkins/pipeline-script-phase3.1.groovy` (the untracked mirror) emits a DISCREPANCY block that quotes the empty `git ls-files` output verbatim.
- Two consecutive runs of the protocol on the same fixture produce byte-identical DISCREPANCY blocks (deterministic output).
- Subroutine, regression fixture, and example output are recorded in `TASKLIST_ROOT/artifacts/D-0001/spec.md` and `evidence.md`.

**Validation:**
- Manual check: `git ls-files configurations/jenkins/pipeline-script-phase3.1.groovy` returns empty AND the new `/sc:reflect` run shows a DISCREPANCY: untracked-substrate block referencing that exact path.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0001/`.

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Phase 5 names {B1, C4, C1} as the priority-top-3 trio with zero overlap; landing this first enables `git`-based feedback for any subsequent refactor's verification.

### T01.02 -- Migration substitution-debt audit (registered host-path migrations)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | The §4.2 bind-mount migration changed the semantics of the `/opt/jenkins/artifacts/` literal at L290/L297 from "trivially correct (host==container)" to "incorrect (host now `/opt/docker/jenkins_artifacts/`)". Without this audit, the bug does not exist. Rank 2 of 14 (Priority 0.924). |
| Effort | M |
| Risk | Medium |
| Risk Drivers | data/migration |
| Tier | STRICT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena \| Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0002/notes.md`
- `TASKLIST_ROOT/artifacts/D-0002/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch plus a new artifact-format file (`docs/migrations/*.md` registry frontmatter) that enumerates registered host-path migrations to zero substitution-debt; protocol fails closed if a referenced literal still uses a pre-migration form not declared in the registry.

**Steps:**
1. **[PLANNING]** Load `/sc:reflect` skill source and identify the path-literal handling stage; locate the §4.2 migration spec and `docker-compose.yml:28` bind line as canonical inputs.
2. **[PLANNING]** Define the registry frontmatter schema (fields: `migration_id`, `pre_path`, `post_path`, `applied_date`, `verified_callsites`); create `docs/migrations/` per Phase 5 line 55 if it does not already exist.
3. **[EXECUTION]** Add a `docs/migrations/2026-04-§4.2-jenkins-artifacts.md` entry encoding the `/opt/jenkins/artifacts/` -> `/opt/docker/jenkins_artifacts/` host-path migration with `verified_callsites: []`.
4. **[EXECUTION]** Add a `migration_substitution_debt_audit()` subroutine to `/sc:reflect` that loads every `docs/migrations/*.md`, scans the working tree for `pre_path` literals, and emits `DEBT: <migration_id> -- <file>:<line>` for each unregistered occurrence.
5. **[EXECUTION]** Run the subroutine against the current repo and populate `verified_callsites` for `pipeline-script-phase3.1.groovy:289-297` only after the user confirms each match is post-migrated.
6. **[VERIFICATION]** Spawn quality-engineer sub-agent (per STRICT tier) to review the registry schema, audit subroutine, and zero-debt termination condition; require sub-agent sign-off on rollback path.
7. **[COMPLETION]** Document the registry, the audit subroutine, and the §4.2 entry in `TASKLIST_ROOT/artifacts/D-0002/spec.md`; copy sub-agent review and run log to `evidence.md`.

**Acceptance Criteria:**
- File `docs/migrations/2026-04-§4.2-jenkins-artifacts.md` exists with the required frontmatter fields and references both `/opt/jenkins/artifacts/` (pre) and `/opt/docker/jenkins_artifacts/` (post).
- Running `/sc:reflect`'s migration-substitution-debt audit against the current repo produces zero `DEBT:` rows (all pre-migration literals are either post-migrated or registered).
- Sub-agent (quality-engineer) review report attached at `TASKLIST_ROOT/artifacts/D-0002/evidence.md` and approves the registry schema and audit termination semantics.
- Registry entry, audit subroutine, sub-agent review, and rollback procedure are documented in `TASKLIST_ROOT/artifacts/D-0002/spec.md`.

**Validation:**
- Manual check: re-running the audit after deliberately reintroducing `/opt/jenkins/artifacts/` at any host context produces the expected `DEBT: 2026-04-§4.2 -- <file>:<line>` row.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0002/`.

**Dependencies:** None (but pairs naturally with T01.03 for codebase-hazard coverage)
**Rollback:** TBD (if not specified in roadmap) -- registry entry and protocol patch are reversible by deleting the registry file and reverting the `/sc:reflect` patch.
**Notes:** STRICT tier driven by "migration" keyword + new artifact-format file requirement; sub-agent delegation Recommended (not Required) because Risk is Medium not High.

### T01.03 -- Path-literal duplication scan (bind-mount * literal * non-identity host/ctr)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Same literal `/opt/jenkins/artifacts/`, two semantics, no `HOST_*`/`CTR_*` constants; the §4.2 edit batch missed the SCP-block hunk because the pre-/post- literal was identical. Rank 3 of 14 (Priority 0.878). |
| Effort | M |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [███████---] 70% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0003/spec.md`
- `TASKLIST_ROOT/artifacts/D-0003/notes.md`
- `TASKLIST_ROOT/artifacts/D-0003/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a path-literal duplication scan that cross-references every bind-mount declaration in `docker-compose.yml` against repo grep hits and flags any non-identity (host != container) literal that appears in a non-tagged context as a `HAZARD: ambiguous-path-literal` finding.

**Steps:**
1. **[PLANNING]** Load `/sc:reflect` source and the project `docker-compose.yml`; identify every bind-mount line with non-identity host:container paths.
2. **[PLANNING]** Confirm the scan budget (target file globs) and define the "non-tagged context" rule: any literal use of either side of a non-identity bind-mount that isn't immediately preceded by a `HOST_`/`CTR_` constant. (Implementation may extend with a comment-syntax convention; this is implementation-defined.)
3. **[EXECUTION]** Add a `path_literal_duplication_scan()` subroutine that parses the compose file, builds a `(host_path, container_path, service)` table, and greps the repo for both literals.
4. **[EXECUTION]** Emit `HAZARD: ambiguous-path-literal -- <file>:<line> -- service=<svc>` for every match in a non-tagged context; deduplicate by (file, line).
5. **[VERIFICATION]** Run the subroutine on the project and confirm `pipeline-script-phase3.1.groovy:289-297` is reported as a HAZARD with `service=jenkins`.
6. **[COMPLETION]** Document scan rules, the parser, and the §4.2 fixture in `TASKLIST_ROOT/artifacts/D-0003/spec.md`; copy the run log to `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `path_literal_duplication_scan` subroutine that parses `docker-compose.yml` bind mounts and emits HAZARD findings on the prescribed format.
- Running the patched protocol against the repo emits a HAZARD row for `configurations/jenkins/pipeline-script-phase3.1.groovy:289-297` referencing service `jenkins` and the non-identity bind `/opt/docker/jenkins_artifacts:/opt/jenkins/artifacts`.
- Two consecutive runs produce byte-identical HAZARD output (deterministic ordering).
- Scan rules, parser, fixture, and example output recorded in `TASKLIST_ROOT/artifacts/D-0003/spec.md` and `evidence.md`.

**Validation:**
- Manual check: introducing a fresh non-identity bind and a literal use without `HOST_*`/`CTR_*` tagging produces the expected HAZARD row on the next protocol run.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0003/`.

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Pairs with T01.02 (C4) and T01.01 (B1) as the Tier 1 trio per Phase 5 §"Tier interpretation". Combined estimated cost ~130-180 LOC of `/sc:reflect` per Phase 4 accounting.

### Checkpoint: End of Phase 1

**Purpose:** Confirm the Tier 1 trio (B1+C4+C1) lands together and re-running `/sc:reflect` against the original bug state surfaces the regression with >=0.95 joint confidence as Phase 4 promised.

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`

**Verification:**
- All three Phase 1 tasks (T01.01, T01.02, T01.03) report Acceptance Criteria 1 satisfied with named artifact paths under `TASKLIST_ROOT/artifacts/D-0001/`, `D-0002/`, `D-0003/`.
- A single `/sc:reflect` run against the bug fixture (`pipeline-script-phase3.1.groovy:289-297` pre-fix state) emits at least one finding from each of the three subroutines (`DISCREPANCY: untracked-substrate`, `DEBT: 2026-04-§4.2`, `HAZARD: ambiguous-path-literal`).
- T01.02 sub-agent (quality-engineer) review is approved; no STRICT-tier blockers remain open.

**Exit Criteria:**
- Tier 1 trio merged to its target branch and a single `/sc:reflect` execution produces the three expected finding categories on the bug fixture.
- Combined LOC count of the three patches falls within the Phase 5 estimate of ~130-180 LOC for `/sc:reflect` plus one new `docs/migrations/*.md` registry file.
- Checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P01-END.md` records Pass AND records a joint-confidence attestation >=0.95 for the Tier 1 trio against the §4.2 bug fixture (per Phase 5 line 54), with method documented; Phase 2 (Tier 1.5 A5 add-on) is unblocked.
