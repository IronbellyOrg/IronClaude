# Patch Checklist
Generated: 2026-05-13
Total edits: 14 across 5 files

## File-by-file edit checklist

- `phase-1-tasklist.md`
  - [ ] L1 -- Name DEP-001 explicitly in T01.04 Exit Criterion bullet 3
  - [ ] L7 -- Soften T01.02 AC bullet 3 to match by content not by line number
- `phase-2-tasklist.md`
  - [ ] M1 -- Replace `--` with em-dash `—` in T02.01 Why field and Step 3
  - [ ] M2 -- Strengthen T02.01 AC bullet 1 to assert full verbatim message
  - [ ] M3 -- Strengthen T02.02 AC bullet 1 to assert full verbatim message
  - [ ] L2 -- Expand T02.02 Notes with inline tie-breaker rationale
  - [ ] L3 -- Convert T02.03 Step 4 to informational note (out of scope)
  - [ ] L4 -- Add T02.03 AC for merge-blocking semantic
- `phase-3-tasklist.md`
  - [ ] L5 -- Annotate T03.03 Notes that unset-SKILL handling is operational hardening
- `phase-4-tasklist.md`
  - [ ] M4 -- Append DEP-005 clause to T04.03 Verification bullet 2 (preserves 3-bullet structural rule)
- `phase-5-tasklist.md`
  - [ ] M5 -- Add T05.04 AC asserting unexpected PLANNING.md/TASK.md matches FAIL
  - [ ] M6 -- Soften T05.05 ACs around prior-run comparison; mark tolerance as conditional
  - [ ] M7 -- Add T05.06 Step for SC-### mapping AND SC-003 / SC-005 sanity checks
  - [ ] L6 -- Name M2/M3 as loopback target in T05.06 Exit Criterion 3

## Cross-file consistency sweep

- [ ] Verify no other tasks weaken roadmap verbatim strings to substrings (sweep all ACs for `substring` / `contains` phrasing).

---

## Precise diff plan

### 1) `phase-1-tasklist.md`

**A. L1 (T01.04 Exit Criterion bullet 3)**

Current: `Phase 2's D2.1 error-message draft can cite \`.dev/README.md\` as the source of truth for the redirect destination.`
Replace with: `DEP-001 satisfied: Phase 2's D2.1 error-message draft can cite \`.dev/README.md\` as the source of truth for the redirect destination.`

**B. L7 (T01.02 AC bullet 3)**

Current: `Edits scoped to the two locations identified in the roadmap (lines 51-53 and 225-227 of the pre-edit file); no other CLAUDE.md content modified.`
Replace with: `Edits scoped to the two location ranges identified in the roadmap (line refs as of roadmap authoring: 51-53 and 225-227; match by content -- the \`PLANNING.md\`/\`TASK.md\` references -- not by line number); no other CLAUDE.md content modified.`

### 2) `phase-2-tasklist.md`

**A. M1 (T02.01 Why field + Step 3) -- em-dash**

Find: `"<name> has no SKILL.md -- not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/."`
Replace with: `"<name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/."`

Apply this replacement twice (once in Why field, once in Step 3).

**B. M2 (T02.01 AC bullet 1)**

Current: `\`make verify-sync\` against a probe \`.claude/skills/_probe-workspace/\` without SKILL.md emits the new message containing the verbatim substring "Move to .dev/eval-workspaces/" and exits non-zero.`
Replace with: `\`make verify-sync\` against a probe \`.claude/skills/_probe-workspace/\` without SKILL.md emits the verbatim message \`<name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/.\` (em-dash exact) and exits non-zero.`

**C. M3 (T02.02 AC bullet 1)**

Current: `\`make lint-architecture\` (or chosen target) with a probe \`*-workspace/\` directory emits the verbatim substring "Workspace directories belong under" and exits non-zero.`
Replace with: `\`make lint-architecture\` (or chosen target) with a probe \`*-workspace/\` directory emits the verbatim message \`Workspace directories belong under \`.dev/eval-workspaces/\`, not \`.claude/skills/\`.\` and exits non-zero.`

**D. L2 (T02.02 Notes)**

Append to Notes: ` Tie-breaker rationale: \`lint-architecture\` is the dedicated architectural-rules target while \`verify-sync\` is sync-verification. Coupling architectural linting with sync verification would change two interfaces; using \`lint-architecture\` changes one.`

**E. L3 (T02.03 Step 4)**

Current: `**[EXECUTION]** Set the job as a required check for PR merge (branch protection setting is repo-admin scoped; document the request in \`notes.md\` if it cannot be done via PR alone).`
Replace with: `**[EXECUTION]** Note (out of task scope): branch-protection / required-check configuration is repo-admin scoped. If it is not already configured for this workflow, record a follow-up request in \`notes.md\` for repo admins; the workflow's non-zero-exit behaviour is the in-scope deliverable.`

**F. L4 (T02.03 ACs)**

After the existing third AC (clean PR passes the workflow), insert: `A failing required workflow status equates to a blocked merge under this repo's standard merge policy (evidence: workflow run + PR \`mergeable=false\` in the GitHub API), OR a repo-admin follow-up note recorded in \`notes.md\` if branch protection is not yet configured.`

### 3) `phase-3-tasklist.md`

**A. L5 (T03.03 Notes)**

Current: `Operational tier STANDARD per the override; behaviour test (target invocation) is the appropriate verification.`
Replace with: `Operational tier STANDARD per the override; behaviour test (target invocation) is the appropriate verification. Note: the unset-SKILL error case (Deliverable item 3, AC bullet 2) is operational hardening beyond roadmap D3.3's literal scope -- retained because the alternative (silent no-op) would create a confusing failure mode.`

### 4) `phase-4-tasklist.md`

**A. M4 (T04.03 Verification bullet 2)**

Current: `\`make sync-dev\` + \`make verify-sync\` exit cleanly with the M4 edits applied (output of T04.01).`
Replace with: `\`make sync-dev\` + \`make verify-sync\` exit cleanly with the M4 edits applied (output of T04.01) AND emit the M2 D2.1/D2.2 messages on the probe inputs per DEP-005 SOFT dep (or record an explicit M4 waiver if M2 has not merged).`

### 5) `phase-5-tasklist.md`

**A. M5 (T05.04 ACs)** -- add a new AC bullet after the first:

`Test FAILS if any unexpected \`PLANNING.md\` or \`TASK.md\` match appears in the grep output (post-T01.02 state must show only \`KNOWLEDGE.md\`).`

**B. M6 (T05.05 AC bullets 1 and 2)**

Bullet 1 current: `\`aggregate_benchmark.py .dev/eval-workspaces/sc-release-split-protocol/\` exits 0 with output equivalent to the prior run (within tolerance documented in \`notes.md\`).`
Replace with: `\`aggregate_benchmark.py .dev/eval-workspaces/sc-release-split-protocol/\` exits 0 and produces valid (non-empty, expected-schema) output. If a prior baseline is available, output is compared and any deltas documented in \`notes.md\`; if no prior baseline exists, comparison is marked N/A.`

Bullet 2 current: `\`generate_review.py .dev/eval-workspaces/sc-release-split-protocol/\` exits 0 with output equivalent to the prior run (within tolerance documented in \`notes.md\`).`
Replace with: `\`generate_review.py .dev/eval-workspaces/sc-release-split-protocol/\` exits 0 and produces valid (expected-schema) output. If a prior baseline is available, output is compared and any deltas documented in \`notes.md\`; if no prior baseline exists, comparison is marked N/A.`

**C. M7 (T05.06 Steps)** -- replace Step 2:

Current: `**[VERIFICATION]** Re-run the five AC sanity checks (open each \`evidence.md\` and confirm the recorded result).`
Replace with: `**[VERIFICATION]** Re-run the five AC sanity checks (open each \`evidence.md\` and confirm the recorded result) AND enumerate SC-001..SC-005 in the checkpoint report with explicit pass status, mapping each to evidence: SC-001 -> AC1-AC5 aggregate (T05.01-T05.05); SC-002 -> T05.02 (CI block); SC-003 -> probe \`superclaude install\` in a clean clone showing no \`*-workspace/\` directories under \`.claude/skills/\`; SC-004 -> T05.04; SC-005 -> \`make sync-dev && make verify-sync\` on a freshly merged branch exits 0 with no drift.`

**D. L6 (T05.06 Exit Criterion 3)**

Current: `Release exit gate: no AC fails. If any AC fails, the checkpoint reports \`Overall: Fail\` and loops back per the discovery-risk handling in the roadmap.`
Replace with: `Release exit gate: no AC fails. If any AC fails, the checkpoint reports \`Overall: Fail\` and loops back to M2 and/or M3 with a revised fix per the M5 Risk Assessment in the roadmap.`

## Suggested execution order

1. `phase-2-tasklist.md` (M1, M2, M3, L2, L3, L4) -- 6 edits, 3 Medium findings.
2. `phase-5-tasklist.md` (M5, M6, M7, L6) -- 4 edits, 3 Medium findings.
3. `phase-4-tasklist.md` (M4) -- 1 Medium finding.
4. `phase-1-tasklist.md` (L1, L7) -- 2 Low findings.
5. `phase-3-tasklist.md` (L5) -- 1 Low finding.
