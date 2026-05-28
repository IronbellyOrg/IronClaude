# Debate Transcript: REFACTOR-PROPOSAL Cross-Env (Depth: quick)

**Round 1 only** (per `--depth quick`). Round 2/2.5/3 skipped.

## Round 1 — Parallel Advocate Statements

### Advocate for Variant 1 (pr86-substrate run)

**Position summary**: V1 is the more disciplined, ship-ready proposal — it targets `src/superclaude/` (the SoT), it includes the eval-suite (Change E) that prevents regression of all other changes, it explicitly considers and rejects each alternative (including everything V2 proposes), and the gated-minimum formula is mathematically auditable in a way V2's "hard cap overrides mean" is not.

**Steelman of Variant 2**: V2 surfaces the **Cause #1 dominant defect** (calibrator non-execution / artifact absence) and proposes an audit-layer gate (Change 4) that V1 entirely misses. V2 also operates with first-hand knowledge of the original T4 cards (H1, H2, H3) and writes a verification plan that directly replays them — this is concrete evidence V1 cannot match. V2's evidence-class taxonomy (5 values + 1 none) is more granular than V1's binary runtime_check score.

**Strengths claimed**:

1. **Correct SoT discipline** — V1 targets `src/superclaude/*` per the project CLAUDE.md SoT rule, matching the verified `.dev/brainstorms/.../Scope` line 15: "NEVER `.claude/` — that is sync-dev output". V2 targets `.claude/skills/*` which is a direct violation.
2. **Eval suite (Change E)** — 6 fixtures + 5 properties that gate any future regression. V2 has verification tests but no permanent corpus.
3. **Gated-minimum formula is auditable** — `min(mean, evidence_grounding+0.30, runtime_check+0.30)` produces a single, traceable composite. V2's three caps (0.65/0.70/0.75) with rule-precedence ("lowest cap wins") is harder to audit.
4. **Migration table** — explicit v1.0 → v1.5 backward-compat with safe defaults (fail-safe to `runtime_behavior` + `AFFIRM`). V2 has no migration story.
5. **Verdict-direction modifier is a structural rule, not a wave-relative smell** — V2's rule 2 needs `wave_siblings` input (acknowledged fallback when unavailable); V1's M3a is unconditional on the card itself.

**Weaknesses identified in Variant 2**:

1. **File-path violation** — `/config/.claude/skills/...` references the gitignored dev copy, not the source of truth. Every edit V2 proposes lands in the wrong place; `make sync-dev` would clobber them. This is a project-rule-level defect (per CLAUDE.md ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents).
2. **No regression corpus** — V5 tests Check 6 once; nothing prevents Change 1's frontmatter fields from being later weakened. V1's Change E is the corpus.
3. **Change 6 (confidence.ts edit) is scope creep** — Markdown-proposal scope was clear; touching TypeScript code is implementation, not proposal.

**Concessions**:

- V1 misses Cause #1 (calibrator non-execution as orchestrator-level defect). V1 assumes the calibrator will be called — V2 catches the case where it isn't.
- V1's evidence taxonomy (binary runtime_check 0/0.5/1.0) is less expressive than V2's typed evidence_class (5 values).

---

### Advocate for Variant 2 (T4-environment run)

**Position summary**: V2 is the operationally complete proposal — it addresses the **actual dominant cause** (Cause #1: calibrator non-execution evidenced by missing `tier2-h*-calibration.md` artifacts in the original T4 run), it uses real T4 hypothesis-card structure to define `evidence_class` taxonomy, and its three independent enforcement points (rubric / calibrator agent / confidence.ts code) provide defense-in-depth that V1 lacks.

**Steelman of Variant 1**: V1 has correctly identified the SoT target path (`src/superclaude/*`) per the project's CLAUDE.md rule, which V2 missed. V1's eval-suite Change E is a genuine prevention-of-regression artifact that V2 substitutes with one-off V1-V5 replay tests. V1's gated-minimum formula is more mathematically tractable than V2's three-cap rule system. V1's migration table is a real backward-compat asset.

**Strengths claimed**:

1. **Closes Cause #1** — the dominant defect from the original T4 run was that `tier2-*-calibration.md` artifacts were absent. V1 has zero coverage of this. V2's Change 4 (Tier 2 calibration-completeness gate with force-degrade on failure) makes the 0.95 / 0.85 self-report pass-through structurally impossible.
2. **Evidence taxonomy is richer** — `runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none` lets the calibrator distinguish post-hoc log evidence (V2 scores it 0.5) from no-evidence (scored 0.0). V1's runtime_check collapses these.
3. **Defense-in-depth at 3 layers** — rubric (Change 2), agent prompt (Change 3), code (Change 6). V1 only touches rubric + agent.
4. **Verification plan uses real failing cards** — V1-V5 replay actual T4 H1/H2/H3 cards through the new calibrator. V1's fixtures are synthetic.
5. **Negative-existential REFUTE rule** (rule 5) directly addresses Cause #3 (refute-vs-confirm asymmetry).

**Weaknesses identified in Variant 1**:

1. **Cause #1 is entirely uncovered** — the most operationally significant failure (the calibrator didn't run at all) is addressed nowhere in V1. V1 assumes calibrator-side rules suffice; V2's Change 4 catches what V1 misses.
2. **Verdict-direction modifier is fragile** — V1 explicitly relies on the card declaring `verdict_direction: REFUTE` correctly. If the card writer omits or mis-declares it, M3a doesn't fire. V2's hard cap on evidence-class mismatch is structural (reads typed fields, no narrative judgment).
3. **No code-level enforcement** — V1's Markdown-only stance means a developer reading SKILL.md can still skip the check. V2's Change 6 cap inside `confidence.ts::assess()` is mechanical.

**Concessions**:

- V2's file-path violation (`.claude/` instead of `src/superclaude/`) is a real defect that V1 correctly caught. The proposed changes' semantic content is sound, but the path needs to be migrated to `src/superclaude/` before any commit. This is a paste-error class fix, not a design defect.
- V2 lacks a permanent eval-suite analogous to V1's Change E. The V1-V5 tests are one-off; a pin-test corpus would strengthen V2.

---

## Per-Point Scoring Matrix (Round 1 only)

| Diff Point | Winner            | Confidence | Evidence Summary                                                                                                                                                                                                  |
| ---------- | ----------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S-001      | tie               | 0.50       | Both organizations are internally consistent. V1 is more refactor-actionable; V2 is more analysis-actionable.                                                                                                       |
| S-002      | Variant 2         | 0.65       | V2's 6 changes include the audit-gate that V1 missed; V1's 5 changes include the eval-suite V2 missed. Net: V2 covers more ground.                                                                                  |
| S-003      | **Variant 1**     | 0.99       | CLAUDE.md ABSOLUTE RULE: `.claude/skills,commands,agents,hooks` is gitignored sync-dev output of `src/superclaude/`. V2's `/config/.claude/...` paths are a direct violation.                                       |
| S-004      | Variant 1         | 0.70       | True diff fences with +/- markers are more reviewable than markdown-block insertions.                                                                                                                              |
| S-005      | Variant 2         | 0.75       | V2's V1-V5 tests use real failing cards from the original T4 run — strongest possible regression evidence. V1's fixtures are synthetic.                                                                              |
| C-001      | Variant 1         | 0.70       | Gated-minimum is more auditable than three-cap-with-precedence; verdict-direction modifier addresses M3a structurally.                                                                                              |
| C-002      | Variant 2         | 0.70       | 5-value evidence_class is more granular than V1's binary runtime_check + adds expressive power (log_evidence as middle tier).                                                                                       |
| C-003      | Variant 2         | 0.65       | Typed taxonomy + cross-tab is more machine-readable than dimension score.                                                                                                                                          |
| C-004      | Variant 1         | 0.70       | Soft caps via min() preserve mean-as-baseline; V2's "override mean entirely" is more aggressive but harder to reason about.                                                                                         |
| C-005      | **Variant 2**     | 0.95       | V2's Change 4 (audit-layer gate) closes Cause #1, the dominant defect. V1 has no equivalent. This is the most consequential V2-unique contribution.                                                                |
| C-006      | Variant 1         | 0.55       | V1 (Markdown-only) is more scope-disciplined; V2's confidence.ts edit is implementation creep. But V2's edit is operationally stronger.                                                                              |
| C-007      | Variant 1         | 0.65       | V1's Change D (scope-correct the 1.000/1.000 claim) kills cultural-prior recursion at the rhetorical source. V2's Check 6 addition adds defensive coverage but doesn't address the recursion.                       |
| C-008      | Variant 1         | 0.55       | V1's verdict-direction modifier is rule-based and self-contained; V2's rules 2 + 5 are more context-dependent (need wave_siblings or regex-pattern detection).                                                       |
| X-001      | **Variant 1**     | 0.99       | Same as S-003 — SoT discipline. V2 must migrate paths to `src/superclaude/*`.                                                                                                                                       |
| X-002      | Variant 1         | 0.65       | Gated-minimum preserves invariants; "hard cap overrides mean" loses information about the other dimensions.                                                                                                         |
| X-003      | tie               | 0.50       | V1's scope discipline is correct for a brainstorm proposal; V2's code edit is operationally desirable for follow-up.                                                                                                |
| U-001      | adopt (V1 unique) | 0.90       | Change E (eval-suite) is high-value and has no V2 equivalent. Adopt as-is.                                                                                                                                          |
| U-002      | adopt (V1 unique) | 0.85       | Migration table is high-value and has no V2 equivalent. Adopt as-is.                                                                                                                                                |
| U-003      | adopt (V2 unique) | 0.95       | Change 4 (Tier 2 audit gate) closes Cause #1 — the single most-load-bearing V2 contribution. MUST be merged in.                                                                                                     |
| U-004      | adopt (V2 unique) | 0.70       | GitHub WebFetch URL detection is a useful operational signal. Adopt.                                                                                                                                                |
| U-005      | adopt (V2 unique) | 0.80       | V1-V5 replay tests on real T4 cards are high-evidence; can co-exist with V1's Change E fixtures.                                                                                                                    |
| A-001      | shared (ACCEPT)   | 0.95       | Both variants ACCEPT calibrator stays Read-only.                                                                                                                                                                    |
| A-002      | shared (ACCEPT)   | 0.95       | Both variants ACCEPT 6th-dimension on rubric is the right enforcement point.                                                                                                                                       |

**Convergence count**: 23 / 23 diff points have a clear winner or adoption verdict.
**Convergence score**: 1.00 (above 0.80 threshold — CONVERGED).
**Direction convergence**: STRONG — both environments agree on the failure mode and the basic shape of the fix (6th dimension + claim/evidence typing). Disagreement is about enforcement architecture (formula refinement vs audit gate), not about the root cause.

## Note on omitted rounds

`--depth quick` skips Round 2 (rebuttals), Round 2.5 (invariant probe), and Round 3. Per-point scoring above is Round-1-only. Given the high natural convergence (1.00), Round 2 would be unlikely to change verdicts.
