# Phase 1 -- Authentication & Credential Migration

Phase 1 produces the three sandbox security and migration documents named in the roadmap. The phase is deliberately STRICT/critical-path heavy so pre-reflect depth is floored to deep/tier 2.

### T01.01 -- Design token-refresh authentication flow document

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | The roadmap requires a token-refresh authentication flow written to `.dev/e2e-reflect/tl-3/work/auth-design.md`. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, auth, critical path |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0001/spec.md`
- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0001/notes.md`
- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0001/evidence.md`

**Deliverables:**

- Token-refresh authentication flow design at `.dev/e2e-reflect/tl-3/work/auth-design.md`.

**Steps:**

1. **[PLANNING]** Load the roadmap item R-001 and identify the token-refresh scope.
2. **[PLANNING]** Check that sandbox output remains under `.dev/e2e-reflect/tl-3/work/`.
3. **[EXECUTION]** Write the token-refresh authentication flow design to `.dev/e2e-reflect/tl-3/work/auth-design.md`.
4. **[EXECUTION]** Include security-sensitive and critical-path notes from the roadmap.
5. **[VERIFICATION]** Use STRICT verification for the auth design document.
6. **[COMPLETION]** Record evidence under `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0001/evidence.md`.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-3/work/auth-design.md` exists.
- File `.dev/e2e-reflect/tl-3/work/auth-design.md` describes token-refresh authentication flow.
- File `.dev/e2e-reflect/tl-3/work/auth-design.md` states the security-sensitive critical-path scope.
- Evidence is linkable from `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0001/evidence.md`.

**Validation:**

- Manual check: reviewer confirms `.dev/e2e-reflect/tl-3/work/auth-design.md` contains token-refresh authentication flow content.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Critical Path Override: Yes because the roadmap item contains authentication and security-sensitive critical path.

### T01.02 -- Document credential store schema migration and rollback

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | The roadmap requires legacy credential store schema migration documentation with rollback content. |
| Effort | L |
| Risk | High |
| Risk Drivers | credentials, migration, data, schema, rollback, breaking-change, critical path |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0002/spec.md`
- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0002/notes.md`
- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0002/evidence.md`

**Deliverables:**

- Credential migration and rollback document at `.dev/e2e-reflect/tl-3/work/credential-migration.md`.

**Steps:**

1. **[PLANNING]** Load roadmap item R-002 and identify migration and rollback scope.
2. **[PLANNING]** Check that sandbox output remains under `.dev/e2e-reflect/tl-3/work/`.
3. **[EXECUTION]** Write credential store schema migration content to `.dev/e2e-reflect/tl-3/work/credential-migration.md`.
4. **[EXECUTION]** Add rollback content to `.dev/e2e-reflect/tl-3/work/credential-migration.md`.
5. **[VERIFICATION]** Use STRICT verification for migration, schema, and credential content.
6. **[COMPLETION]** Record evidence under `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0002/evidence.md`.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-3/work/credential-migration.md` exists.
- File `.dev/e2e-reflect/tl-3/work/credential-migration.md` documents legacy credential store schema migration.
- File `.dev/e2e-reflect/tl-3/work/credential-migration.md` documents rollback.
- Evidence is linkable from `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0002/evidence.md`.

**Validation:**

- Manual check: reviewer confirms `.dev/e2e-reflect/tl-3/work/credential-migration.md` contains migration and rollback sections.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** As stated in roadmap
**Notes:** Critical Path Override: Yes because the roadmap item contains credential, migration, schema, rollback, and critical path.

### T01.03 -- Document password-hashing parameters

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | The roadmap requires password-hashing parameter documentation for a security-sensitive item. |
| Effort | M |
| Risk | High |
| Risk Drivers | password, security-sensitive |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0003/spec.md`
- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0003/notes.md`
- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0003/evidence.md`

**Deliverables:**

- Password-hashing parameter document at `.dev/e2e-reflect/tl-3/work/hashing-params.md`.

**Steps:**

1. **[PLANNING]** Load roadmap item R-003 and identify password-hashing documentation scope.
2. **[PLANNING]** Check that sandbox output remains under `.dev/e2e-reflect/tl-3/work/`.
3. **[EXECUTION]** Write password-hashing parameter content to `.dev/e2e-reflect/tl-3/work/hashing-params.md`.
4. **[EXECUTION]** Include the security-sensitive label from the roadmap.
5. **[VERIFICATION]** Use STRICT verification for password and security-sensitive content.
6. **[COMPLETION]** Record evidence under `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0003/evidence.md`.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-3/work/hashing-params.md` exists.
- File `.dev/e2e-reflect/tl-3/work/hashing-params.md` documents password-hashing parameters.
- File `.dev/e2e-reflect/tl-3/work/hashing-params.md` states the security-sensitive scope.
- Evidence is linkable from `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0003/evidence.md`.

**Validation:**

- Manual check: reviewer confirms `.dev/e2e-reflect/tl-3/work/hashing-params.md` contains password-hashing parameter content.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Critical Path Override: Yes because the roadmap item contains password and security-sensitive scope.

### T01.04 -- Checkpoint: End of Phase 01

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Gate: verify outputs of Phase 1 before reflection. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01 |

**Checkpoint Report Path:** `.dev/e2e-reflect/tl-3/bundle/checkpoints/CP-P01-END.md`

**Purpose:** Confirm the three Phase 1 security and migration documents are ready for reflect gating.

**Verification:**

- Confirm `.dev/e2e-reflect/tl-3/work/auth-design.md` is planned by T01.01.
- Confirm `.dev/e2e-reflect/tl-3/work/credential-migration.md` is planned by T01.02.
- Confirm `.dev/e2e-reflect/tl-3/work/hashing-params.md` is planned by T01.03.

**Exit Criteria:**

- T01.01 has evidence path coverage.
- T01.02 has evidence path coverage.
- T01.03 has evidence path coverage.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-3/bundle/checkpoints/CP-P01-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01..T01.03
**Rollback:** N/A (checkpoints are read-only verifications)

### T01.05 -- Post-Execution Reflection: Phase 1

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002, R-003 |
| Why | Reflect gating is enabled by default and must evaluate the STRICT/critical-path-heavy phase after execution. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-RF01 |

**Artifacts (Intended Paths):**

- `.dev/e2e-reflect/tl-3/bundle/artifacts/D-RF01/evidence.md`

**Deliverables:**

- Phase 1 post-execution reflection evidence.

**Steps:**

1. **[PLANNING]** Load Phase 1 task outcomes and depth-map entry.
2. **[PLANNING]** Check the override basis for `n_cpo` and `n_strict`.
3. **[EXECUTION]** Record reflection findings for Phase 1.
4. **[EXECUTION]** Reference deep/tier 2 reflect routing for Phase 1.
5. **[VERIFICATION]** Confirm the reflection evidence references Phase 1 task IDs.
6. **[COMPLETION]** Store reflection evidence under `.dev/e2e-reflect/tl-3/bundle/artifacts/D-RF01/evidence.md`.

**Acceptance Criteria:**

- File `.dev/e2e-reflect/tl-3/bundle/artifacts/D-RF01/evidence.md` exists.
- Reflection evidence references T01.01, T01.02, and T01.03.
- Reflection evidence records `depth: deep` and `tier: 2` for Phase 1.
- Reflection evidence states the override basis from `n_cpo` or `n_strict`.

**Validation:**

- Manual check: reviewer confirms Phase 1 reflection evidence references depth-map routing.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.04
**Rollback:** N/A (reflection is read-only verification)
