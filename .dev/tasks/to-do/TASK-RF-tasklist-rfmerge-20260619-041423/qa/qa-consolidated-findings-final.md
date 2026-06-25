# Final-State QA — Consolidated Findings (Cycle 1)

**Generated:** 2026-06-19 (Step 8.G8). Six final-state lens reports consolidated.

## Per-lens verdicts

| Lens | Agent | Verdict | Issues |
|------|-------|---------|--------|
| cross-phase template-conformance | rf-qa | PASS | 0 |
| cross-phase internal-consistency / no-interaction-bugs | rf-qa | PASS | 1 MINOR (loop-mid-failure under-spec) |
| final evidence-quality / full-suite green | rf-qa | PASS | 11 non-blocking (stale artifacts, pre-existing) |
| final actionability / determinism | rf-qa-qualitative | **FAIL** | 7 IMPORTANT, 5 MINOR |
| final no-fork / reuse-fidelity | rf-qa-qualitative | PASS | 0 (all 3 contracts byte-exact) |
| final domain-accuracy vs FR.1–.7 + R-1..R-16 | rf-qa-qualitative | **FAIL** | 1 IMPORTANT, 1 MINOR(non-defect) |

## CONSOLIDATED VERDICT: **FAIL**

The build is structurally complete, full-suite green, all three contracts byte-exact (no fork), and 7/7 FRs +
16/16 R-pins traced. The FAIL is from residual determinism-spec leaks + cross-ref hygiene on my own edits,
plus one P3 evidence-stub that diverges from the canonical DM-003 form. All are bounded, behavior-preserving
precision fixes.

## Deduplicated issue list

| ID | Severity | Lens | Location | Issue | Required fix |
|----|----------|------|----------|-------|--------------|
| CF-01 | IMPORTANT | domain-accuracy Q-1 | SKILL.md P3 merge step 1a (`evidence` stub) | P3 emits `<!-- evidence-absence: spawn-log-unavailable -->`, which does NOT byte-match the canonical DM-003 / R-116 stub `<!-- evidence-absence: no-spawn-log: <reason> -->` (spec §4.5 + task-builder R-116 mandate the parametrized form verbatim). Different sentinel key + drops the `<reason>` slot. | Change the P3 `evidence` stub to `<!-- evidence-absence: no-spawn-log: <reason> -->`. Update the Phase-4 test assert (currently asserts `spawn-log-unavailable`) and the reuse-contracts.md note to match. Keep all other DM-003 fields byte-exact. |
| CF-02 | IMPORTANT | actionability #4/#5 | SKILL.md P4 gate-results (`<check description>`) | The PASS-line description extraction ("first sentence's leading clause" for the 12 prose checks 1-12) has no deterministic boundary → same passing gate serializes different bytes. | Pin a deterministic boundary for ALL 20 checks: "for `<check description>`, use the verbatim check text up to the first colon; if the check line has no colon, use the verbatim check title/first line as written in the Self-Check gate." (No discretionary "leading clause".) |
| CF-03 | IMPORTANT | actionability #6 | SKILL.md §4.1d P1 (`Source areas:`) | The Source-areas trigger is open-ended ("e.g. a backticked name or `module:`/`component:` label") — a backticked function/variable could be mis-classified → non-deterministic. | Pin a CLOSED trigger set: "list ONLY (a) tokens introduced by an explicit `module:`/`component:`/`subsystem:`/`service:` label, OR (b) a backticked token whose immediately-preceding word is one of {module, component, subsystem, service}; nothing else qualifies. Never classify free prose, function names, or variables." |
| CF-04 | IMPORTANT | actionability #7 | SKILL.md §4.1d P1 (resolve predicate) | The resolve predicate borrows §4.1c's FILESYSTEM existence-gate for a non-filesystem `R-###` ref — type-mismatched / inapplicable. | Drop the §4.1c existence-gate analogy; state directly: "a `R-###` ref resolves iff it appears in the task's `Roadmap Item IDs` metadata field (non-empty); absent → does not resolve." |
| CF-05 | IMPORTANT | actionability #2 | SKILL.md P2 iteration-state worked example | The example has the same task IDs in both `F_k` (failing set) and the PASS-set in one pass → self-contradictory, mis-teaches the guard. | Rewrite so PASS-set and `F_k` are DISJOINT per pass (e.g. pass 1: `|F_1|=2`, FAIL={T03.04, T05.09}, PASS={T01.01, T02.03}; pass 2: `|F_2|=1`, T03.04 now PASS). |
| CF-06 | IMPORTANT | actionability #3 | SKILL.md P4 gate-results (L1262) | Stale parenthetical "(today that directory is first created at Stage 8...)" now contradicts the Stage-6-creates-it claim. | Remove/rephrase the stale parenthetical; single source of truth: "Stage 6 (gate-results) creates `validation/` first; the Stage-8 `mkdir -p` is an idempotent no-op." |
| CF-07 | IMPORTANT | actionability #1 | SKILL.md index Metadata table (`<computed per Section 3.1>`) | Dangling cross-ref: no `Section 3.1` exists; the actual algorithm is under `### Tasklist Root (deterministic)`. (Pre-existing template text, but determinism-load-bearing.) | Change `<computed per Section 3.1>` to reference the actual heading (e.g. "per `### Tasklist Root (deterministic)`"). Also fix the index-template mirror if it carries the same dangling ref. |
| CF-08 | MINOR | actionability #8 | SKILL.md Stage Completion Contract ("11 stages") | "11 stages" can be conflated with the per-phase post-reflect task. | Add: "(the per-phase post-execution reflection is an executed task templated into each phase file, NOT a generator stage)." |
| CF-09 | MINOR | actionability #9/#10 | SKILL.md P1 Execution Context block ("a divergence is a halt condition" / "this skill MUST NOT") | "halt condition" implies a runtime gate that doesn't exist; "this skill" self-ref breaks imperative voice. | Reword to an imperative design constraint: "Do NOT introduce a second, incompatible meaning of 'Execution Context'." |
| CF-10 | MINOR | actionability #11 | SKILL.md "11 stages" sentence | Off-by-one read invited (IDs run 1–10 plus 10.5). | Say "11 stage entries (1–10 plus 10.5)". |
| CF-11 | MINOR | actionability #12 | SKILL.md P3 zero-success terminal | "the generator's existing report-validation-error terminal" implies a concrete mechanism the same sentence says is unimplemented. | Reword to "report the validation error and do not return a clean bundle (no typed-error symbol is required by this prose)." |
| CF-12 | MINOR | internal-consistency | SKILL.md Stage-10 P2 gate | Spec silent on whether a fresh agent-failure DURING a P2 loop-back re-run can re-route to the zero-succeeded terminal / emit a new synthetic. | Add a one-sentence clarification at the Stage-10 gate: the loop-back re-run applies the same Stage-7 some-vs-zero gate; a fresh exhaustion emits a synthetic as usual; zero-success on a re-run routes to the report-validation-error terminal. |

## Fix scope for Step 8.G9

- SKILL.md determinism/cross-ref fixes CF-01..CF-07 + the MINOR CF-08..CF-12 — all behavior-preserving precision
  edits (pin extraction boundaries, fix dangling/stale refs, fix the worked example, canonicalize the P3 stub).
  Keep the no-fork contracts byte-exact (only CF-01 touches a DM-003 field — change the `evidence` stub to the
  canonical R-116 form, the OTHER 6 fields stay byte-exact).
- Test updates: CF-01 requires updating the `test_dnsp_synthetic_provenance`/`test_dnsp_excluded_from_patch_checklist`
  assert that references the old stub, plus the reuse-contracts.md note. CF-02/CF-03/CF-04 may require updating the
  P4/P1 determinism-extraction asserts to match the re-pinned prose.
- Index-template mirror: fix CF-07 there too if it carries the dangling §3.1 ref.
- After fixes: `make sync-dev` + `make verify-sync` + the full stay-green set (`tests/tasklist/`,
  `tests/skills/test_task_builder_merge.py`) + `ruff check`/`ruff format` on changed files. Keep all green.
- IMPORTANT: re-read post-fix SKILL.md; every test assert (existing + updated) must byte-match the source.
