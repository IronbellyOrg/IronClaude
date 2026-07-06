# Research Completeness Verification — Single-Analyst (BREADTH lens)

**Topic:** PR #197 reduce-then-merge tasklist build (single track)
**Date:** 2026-06-28
**Analysis type:** completeness-verification
**Lens:** completeness / BREADTH — does every area the tasklist needs have research coverage?
**Files analyzed:** 4 research files (01–04) + research-notes.md + driving spec (merged-requirements.md)
**Depth tier:** Standard
**Driving spec:** `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/.dev/brainstorms/pr197-final-merge-strategy/merged-requirements.md`

**Assigned files:**
- `research/01-git-disposition.md` (R1)
- `research/02-reflect-skill-hunk-surface.md` (R2)
- `research/03-taskbuilder-clause-flip.md` (R3)
- `research/04-template-tests-validation.md` (R4)

> Note: this is the sole analyst instance (no `assigned_files` partition list beyond the 4 named research files, which constitute the full research set). No PARTITION NOTE required — cross-file checks span the complete research corpus.

---

## Verdict: (pending — appended at end)

---

## Per-Criterion Breadth Coverage (the 7 lens criteria)

### Criterion 1 — All 18 file dispositions + exact git checkout/rm commands

**PASS.**

- R1 (`01-git-disposition.md` §"18-file name-status" + "Per-file disposition matrix") enumerates all 18 files with verified `git diff --name-status origin/master...HEAD`, a type column (M/A), a disposition, and per-row evidence. Counts reconcile: ACCEPT=11, DROP-restore=2, REJECT-restore=2, RM=1, HUNK-SURGERY=2, total=18 (R1 line 71). This matches the spec Appendix matrix (18 rows) and research-notes.md EXISTING_FILES exactly.
- Exact single-line commands are present and stated to have been dry-run executed then reset (R1 §"EXACT single-line commands", lines 88–115):
  - Step 2 DROP restore: `git checkout origin/master -- src/superclaude/cli/reflect/runner.py tests/cli/reflect/test_no_nesting_guard.py`
  - Step 2 RM: `git rm tests/cli/reflect/test_inline_directive.py`
  - Step 3 REJECT refs: `git checkout origin/master -- src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md`
- Existence of each restore target on `origin/master` is independently verified via `git cat-file -e` (R1 lines 73–86), including the ABSENT-as-expected `test_inline_directive.py` and the `git ls-files` confirmation it is tracked on-branch (valid `git rm` target).
- R1 adds a genuinely load-bearing HARD WARNING (lines 117–120): the two HUNK-SURGERY files MUST NOT appear in any `git checkout origin/master` one-liner. This is exactly the failure mode that would collapse the reduce-then-merge premise; flagging it pre-empts it.
- The invalid `--source=origin/master` syntax footgun is documented (R1 lines 113–115) so the builder embeds only the positional form.

**Minor note (not a gap):** R1 carries `Status: In Progress` in its header (line 5) but ends with `## Status: Complete` (line 129). The trailing marker governs; treated as complete. See Completeness table.

### Criterion 2 — Reflect SKILL.md hunk surgery (master restores, EV retains, line ranges, changelog reword, post-surgery greps)

**PASS** (strongest file in the set).

- R2 (`02-reflect-skill-hunk-surface.md`) enumerates all 11/12 hunks with @@ anchors, branch line numbers, section, class (RESTORE-MASTER / RETAIN-BRANCH / RESTORE-PARTIAL / MIXED), and action (§1 table, lines 24–37). H11 is explicitly flagged as MIXED requiring a split at Edit time (lines 36, 39, §2.7).
- Master content to restore is quoted verbatim with master line numbers for every RESTORE hunk (H1 delete-only §2.1; H2 §7.1 core rewrite §2.2 with master lines 620/622/626/630/632; H7 §2.3; H8 telemetry 3 fields §2.4; H9 §11.3 §2.5; H10 fallback-table §2.6; H11(a) metrics fields §2.7).
- EV RETAIN hunks (EV-1 §8, EV-2 §9.2, §12 detector, H11(b) metrics comment, H3 card-naming) are each isolated with branch line numbers and an explicit MUST-NOT-REVERT (R2 §3).
- Changelog reword (H5) is covered with the EXACT branch line to reword (line 699), the master reference line, AND a draft replacement (R2 §4, lines 147–167) — plus the critical rationale that the "removed telemetry" claim becomes FALSE after H8/H11(a) restore and must be dropped, not preserved.
- Post-surgery validation greps V1–V6 with EXPECTED results are tabulated (R2 §5, lines 175–184), INCLUDING two footgun corrections: the V2 literal-substring false-negative (`merge_method legal` does not appear verbatim → broadened alternation recommended) and the V6 line-count inequality (`>1989 AND <1993`, NOT `==1989`).
- The CRITICAL HAZARD (full-file checkout forbidden) and the line-count sanity (+4 net) lead the file (§0).

This file gives the builder per-hunk Edit targets, restore content, retain markers, a reword draft, and validated greps — full Standard-tier depth for the highest-risk step.

### Criterion 3 — task-builder clause flip (clause-1 + dependents, two-family boundary, EV-3/EV-4 retention, validation)

**PASS, with one ambiguity correctly surfaced (see Criterion 7).**

- R3 (`03-taskbuilder-clause-flip.md`) opens with the CRITICAL SCOPE FINDING: the file contains TWO families of instance-level text — Family A = CLI POST cluster (FLIPS: L2170, L2244–2252, L2276, L2382–2383, L2389) and Family B = PRE-gate + skill-mode runner (DO NOT FLIP: L1668, L1678, L2218/2223–2224, L2310, L2371). The boundary is asserted by the file itself (clause 7 "A.10.7 stays byte-for-byte untouched") (R3 §"CRITICAL SCOPE FINDING", TASK 2).
- All 7 clauses are quoted verbatim with line numbers (R3 TASK 1, L2244–2251), and every other instance-level location in both families is quoted with line numbers (TASK 2).
- Proposed exclusion-model rewordings are given per location, internally consistent under A-narrow (R3 TASK 3) — header, clauses 1–7, L2170, L2276, L2389, L2382–2383.
- EV-3/EV-4 are confirmed PRESENT on-branch with verbatim anchors (L2232/2233 EV-3, L2239/2240 EV-4, `waves_attestation` L2231–2233) and marked RETAIN unchanged — and explicitly noted as NOT referencing instance-level vs exclusion, so untouched by the flip (R3 TASK 4).
- `reflect_post_mode`/`--cli`/`CLI_MODE` machinery confirmed present and RETAINED with anchors (L43, L286, L2168, L2169, L2371, L2377–2398) (R3 TASK 5).
- Validation: R3 confirms `make verify-sync` is the user-mandated check AND adds grep validations for the flip landing + a Family-B-edit tripwire (R3 TASK 6, lines 147–175). Note the line-number-shift caveat (prefer content-anchored grep over hardcoded 2244–2251).

### Criterion 4 — Every validation command resolves (make targets, markdownlint, pytest selectors, ruff, gh pr) with known-noise caveats

**PASS** (and unusually rigorous on caveats).

- R4 (`04-template-tests-validation.md` §3) verifies each command against the actual Makefile / config / binaries:
  - Make targets resolved with line numbers: `sync-dev` (Makefile:109, MUTATES), `verify-sync` (Makefile:166, read-only SoT gate), `lint` (Makefile:48), `format` (Makefile:53, WRITE-MODE).
  - `make lint` gotcha documented: runs `lint-architecture` first → can exit non-zero on a PRE-EXISTING unrelated `recommend.md`/`sc-recommend-protocol` mismatch; scope ruff judgment to changed `.py` (R4 §3 + §5 item 2).
  - markdownlint: bare `markdownlint`/`markdownlint-cli2`/`pre-commit` NOT on PATH; `npx` IS; correct single-line `npx -y markdownlint-cli@0.38.0 <6 SKILL.md paths>` form provided; pre-commit hook id `markdownlint` (cli, not cli2) cited; `.dev/` exempt from markdownlint so the generated tasklist itself is not gated (R4 §3 + §5 item 1).
  - pytest selectors resolve with collect-only counts: `tests/cli/reflect` (163), `tests/swarm` (2272), `tests/skills/test_task_builder_merge.py` (68 ref). `test_no_nesting_guard.py` and `test_inline_directive.py` both confirmed present pre-reduction.
  - `uv run ruff format --check src/ tests/`: read-only but exits 1 with 104 noise files (worktree ruff-version mismatch) → scope fixes to changed `.py` only, never write-mode broadly (R4 §3 + §5 item 3).
  - gh pr: `git remote -v` confirms origin = fork; `gh pr comment 197 --repo IronbellyOrg/IronClaude --body "auggie review"` verb verified via `--help`; `gh pr view 197` confirms PR #197 OPEN, head `feat/rf-harness-sync`, URL owner `IronbellyOrg` (R4 §4).
- §5 explicitly lists the commands that do NOT resolve as-written (bare `markdownlint`, `make lint` unreliable, broad `ruff format`, mutating `make sync-dev`/`make format`) so the builder corrects them. This directly satisfies the "known-noise caveats" requirement.

### Criterion 5 — Hard constraints captured

**PASS.**

- SoT (edit `src/` then `make sync-dev`; `make verify-sync`): R1 §".claude/ mirror risk" (lines 122–127), research-notes PATTERNS line 47, R4 §3/§5.
- Never stage `.claude/` except `settings.json`; `-f` = STOP siren: R1 lines 125–127 (cites CLAUDE.md ABSOLUTE RULE + memory `feedback_claude_dir_gitignored.md`); R4 §5 item 4 notes pre-commit `block-claude-generated-mirrors`. `.claude/skills/sc-reflect-protocol/SKILL.md` confirmed gitignored via `git check-ignore`.
- Fork-only PR target: R4 §4 (`git remote -v`, every `gh pr` carries `--repo IronbellyOrg/IronClaude`, URL-owner assertion), research-notes PATTERNS line 48.
- Single-line commands only: research-notes PATTERNS line 49 (memory `feedback_no_multiline_paste`); R4's PR-hygiene commands are all single-line; R3/R2 greps are single-line.
- `/task` not `/sc:task`: **see GAP-1 below** — this specific constraint is NOT explicitly carried in any of the 4 assigned research files. (It is a known project rule, memory `feedback-no-sctask-on-task-builder-tasklists`, but the research did not surface it. It is, however, a *downstream-execution* constraint, not a tasklist-build constraint — the tasklist being BUILT is run with `/task`; the build research need not encode it. Rated Minor.)

### Criterion 6 — Granularity sufficient for per-step checklist items

**PASS.**

- R1 gives copy-paste single-line git commands per step (2 and 3) → atomic per-file or per-restore-group items.
- R2 gives per-hunk Edit targets (11/12 hunks) with restore content and retain markers → one checklist item per hunk is directly authorable (satisfies template A3 granular breakdown / A4 enumerate-then-per-item, per R4 §1).
- R3 gives per-location rewordings (clause-by-clause + provenance lines) → per-clause items.
- R4 supplies the MDTM template-02 rules (frontmatter key set incl. builder-injected `start_commit`/`executor_model_class`, A3/A4/B2/B5, final Post-Completion phase items I11/I13/I17, I18 testing requirement) and a cited house-style reference tasklist (`TASK-RF-tasklist-rfmerge-20260619-041423`). Granularity scaffolding is complete.

### Criterion 7 — Ambiguities documented

**PASS.**

- task-builder clause blast radius: documented in THREE places — research-notes GAPS #2 + AMBIGUITIES_FOR_USER, and R3's CRITICAL SCOPE FINDING with A-narrow (recommended) vs A-wide options and an explicit "DECISION REQUIRED (flag to Step 4 author)". R3 also surfaces the single most important cross-researcher dependency (Residual tension, lines 187–193): if reflect stays exclusion vs instance-level, clauses 4/5 contract-field claims must match R2's actual contract. **This is correctly escalated rather than silently resolved.**
- POST_REFLECT_GATE disabled: documented in research-notes TEMPLATE_NOTES (lines 76) with rationale (self-referential/fragile to run the just-edited reflect skill) and marked a reversible decision note. QA_GATE_REQUIREMENTS: NONE is also justified (lines 75).
- contract changelog reword: research-notes GAPS #3 + R2 §4.

---

## Coverage Audit (spec §7 step spine → research coverage)

| Spec step (§7) | Research coverage | Status |
|----------------|-------------------|--------|
| Step 0 — baseline green (`git fetch && status`; pre-state pytest) | R4 §3 (pytest selectors resolve, counts) + R4 §4 (`git remote -v`, behind-count=0) | COVERED |
| Step 1 — ACCEPT additive (11 files, no edit; sync+verify+markdownlint) | R1 matrix (ACCEPT=11) + R4 §3 (markdownlint npx form, 6 SKILL.md exist) | COVERED |
| Step 2 — DROP Decision-B (runner.py + nesting-guard restore; rm inline test) | R1 §"Step 2" exact commands + existence verify + R4 pytest `tests/cli/reflect` | COVERED |
| Step 3 — REJECT Decision-A refs (full restore) + reflect SKILL.md hunk surgery + changelog reword | R1 §"Step 3" refs restore + R2 (entire file: hunks, restores, retains, reword, greps) | COVERED |
| Step 4 — PORT EV-3/EV-4 + reflect_post_mode/--cli; flip CLI clause-1 | R3 (entire file: families, clauses, rewordings, EV-3/EV-4 + machinery retention, validation) | COVERED |
| Step 5 — full validation gate (sync/verify/pytest/ruff format --check/lint) | R4 §3 + §5 (every command + caveats) | COVERED |
| Step 6 — PR hygiene & re-review (rebase-if-behind, push, auggie review comment, URL assert) | R4 §4 (all single-line commands verified, PR #197 OPEN) | COVERED |
| Completion / Post-Completion phase | R4 §1 (template I11/I13/I17 final-phase items, I18 testing) | COVERED |
| Frontmatter (`start_commit`/`executor_model_class` builder-injected) | R4 §1 (NOT in base template; injected after spec_path; rfmerge example) + R1 baseline `start_commit=cda6e2d4` | COVERED |

All 6 spec steps + baseline + completion + frontmatter have research coverage. No scope item is uncovered.

---

## Completeness (per research file)

| Research File | Status marker | Summary/Findings | Gaps assessed | Key takeaways/Summary-for-author | Rating |
|--------------|---------------|------------------|---------------|----------------------------------|--------|
| 01-git-disposition.md | `## Status: Complete` (L129); header still says "In Progress" (L5) | Yes (matrix + sanity checks) | Yes (HARD WARNING, mirror risk) | Yes (counts + warnings) | Complete |
| 02-reflect-skill-hunk-surface.md | `Status: Complete` (L7) | Yes (§1 table + §2/§3) | Yes (§6 subtle traps) | Yes (§6 Summary for Step 3 author) | Complete |
| 03-taskbuilder-clause-flip.md | `Status: In progress` (L8) AND `**Status: Complete**` (L195) | Yes (TASK 1–7) | Yes (Residual tension, scope caveats) | Yes (R3 recommendation) | Complete |
| 04-template-tests-validation.md | `Status: In progress` (L7) AND `**Status: Complete**` (L169) | Yes (§1–§5) | Yes (§5 non-resolving commands) | Yes (per-section builder notes) | Complete |

**Stale header markers (Minor):** 3 of 4 files (R1, R3, R4) carry a top-of-file `Status: In Progress` that was not updated when the trailing `Status: Complete` was written. All four have a definitive trailing completion marker, full Summary, Gaps, and Key-Takeaways sections, so all are substantively complete. The stale top marker is cosmetic but could confuse a reader scanning headers. Rated Minor.

---

## Cross-Reference Consistency

- **Decision-A direction is consistent across spec + R2 + R3.** Spec §5 recommends KEEP master's executor-class EXCLUSION (reject #197 instance-level). R2 restores master's §7.1/§11.3/§9.3 exclusion blocks (telemetry fields `executor_class_source`/`executor_class_resolved`/`executor_exclusion_degraded` re-added at §2.4/§2.7(a)). R3 flips the task-builder CLI cluster to the exclusion model (clauses 4/5 assert `--executor-model` excludes and the contract emits `executor_class_resolved`/`executor_exclusion_degraded`). **R3's "Residual tension" (the open worry that R3 clause-5's contract-field claims must match what R2 establishes) RESOLVES FAVORABLY:** R2 §2.4 restores exactly those two fields as real telemetry, so the CLI-cluster flip is coherent — `--executor-model` is handed to a reflect skill that genuinely class-excludes. The builder should note this resolution so Step-4 clause-5 wording asserts the field names R2 confirms (not a hypothetical). This is the single most important cross-file dependency and it is satisfied.
- **HUNK-SURGERY exclusion from full-restore is consistent.** R1 forbids `git checkout origin/master` on the two surgery files (lines 117–120); R2 §0 independently forbids it for reflect SKILL.md; R3 confirms task-builder SKILL.md is a RETAIN+flip target, not a restore. No file lists a surgery path in a restore one-liner. Consistent.
- **EV cross-references intact post-restore.** R2 §3.4 verifies master's restored §7.1 keeps the N=2 floor that EV-1/EV-2/§12 reference — so restoring §7.1 does not orphan the retained EV hunks. Internally consistent.

---

## Contradictions Found

**None that block the build.** One consistency point worth the builder's attention (not a contradiction):

- R2 §3.5 (H3) recommends RETAINING the branch reviewer-card naming `reviewer-N-card.yaml` (vs master's `card-N.md`) for consistency with the retained EV-1/§12 detector. This is a deliberate RETAIN of a #197 naming change that is *not* instance-level. It is correctly justified (the EV hunks reference `reviewer-cards/`), but the builder should be aware Step 3 retains a non-EV, non-instance-level #197 cosmetic change for internal consistency — surface it in the tasklist as a deliberate choice (R2 already flags it). Not a contradiction; an intentional, documented exception.

---

## Compiled Gaps

### Critical Gaps (block synthesis/build)

- **None.** Every spec step, every hard constraint load-bearing to the build, and every high-risk edit (reflect hunk surgery, task-builder clause flip) has actionable, evidence-cited research coverage with exact commands/line numbers.

### Important Gaps (affect quality)

- **None.** The two highest-risk steps (3 and 4) are the two most thoroughly researched (R2, R3). Validation-command caveats (R4 §5) are complete enough to prevent the known false-fail footguns.

### Minor Gaps (should still be addressed by the builder)

- **GAP-1 (Minor) — `/task` not `/sc:task` execution constraint not surfaced in research.** Criterion 5 lists this as a hard constraint, but none of the 4 research files mention it (it lives in memory `feedback-no-sctask-on-task-builder-tasklists`). Mitigation: it is a *downstream-execution* rule for running the BUILT tasklist, not a tasklist-build input, so its absence from build research is defensible. Builder action: if the tasklist or its handoff notes mention how to run it, use `/task <path>`, never `/sc:task`.
- **GAP-2 (Minor) — stale top-of-file `Status: In Progress` markers in R1, R3, R4.** Cosmetic only; all four files have trailing `Status: Complete` + full Summary/Gaps/Takeaways. Builder/QA can disregard the top marker; flagged so a header-scan does not misread completion state.
- **GAP-3 (Minor) — Step-4 clause-5 contract-field wording depends on R2's restored telemetry.** R3 caveats clause 5 ("do not invent contract field names not confirmed by R2"). RESOLVED by R2 §2.4 (the fields ARE restored), but the builder must wire the dependency explicitly: Step-4 clause-5 reword should name the exact fields R2 restores (`executor_class_resolved`, `executor_exclusion_degraded`) and not assert any field R2 did not restore.

---

## Depth Assessment

**Expected depth (research-notes):** Standard tier — file-level understanding with key function/line documentation; this is a deterministic git-reduction + targeted-edit task, not a design exploration.

**Actual depth achieved:** Meets-to-exceeds Standard for every step. The two high-risk steps reach effectively Deep tier:
- R2 provides per-hunk line-range mapping, verbatim master restore content, retain markers, a changelog reword draft, and six validated post-surgery greps with footgun corrections — beyond Standard.
- R3 provides a two-family scope boundary, verbatim per-clause quotes, per-location rewordings, EV/machinery retention anchors, and a scope-creep tripwire grep — beyond Standard.
- R1 and R4 are solid Standard: every command resolved against real files/binaries with line numbers, dry-run-then-reset verification, and an explicit non-resolving-commands list.

**Missing depth elements:** None material. The research is appropriately scoped; it did not over-investigate (e.g., it correctly did NOT design Option C, which the spec defers as a non-blocking fast-follow).

---

## Recommendations (for the builder, before authoring the tasklist)

1. Embed R1's exact single-line git commands verbatim into Steps 2 and 3; never list the two HUNK-SURGERY paths in any `git checkout origin/master` one-liner (R1 lines 117–120).
2. Author Step 3 as one checklist item per hunk using R2's §1 table classifications; split H11 into its RESTORE and RETAIN sub-edits (R2 §2.7); use R2 §4's reword draft for the changelog; embed R2 §5's V1–V6 greps with the broadened V2 alternation and the V6 inequality (not `==1989`).
3. Author Step 4 as A-narrow (Family A only); use R3 TASK 3 rewordings; add R3 TASK 6's flip-landed grep AND the Family-B tripwire grep; wire clause-5 field names to R2's restored telemetry (GAP-3).
4. In Step 5 use the read-only/scoped command forms from R4 §5 (npx markdownlint-cli@0.38.0 for the 6 SKILL.md; scope ruff to changed `.py`; treat `make lint`'s `lint-architecture` pre-existing failure as out-of-scope).
5. Bake the hard constraints (SoT, never-stage-`.claude/`, fork-only PR, single-line) into a Prerequisites/Constraints block and restate per-item where load-bearing; add the `/task` (not `/sc:task`) note to any run-instructions (GAP-1).
6. Disregard the stale top-of-file `Status: In Progress` markers (GAP-2); all research is complete.

---

## VERDICT: PASS

All 7 breadth criteria PASS. The research corpus (R1–R4 + research-notes) provides complete, evidence-cited coverage for every one of the spec's 6 phases plus baseline, completion, and frontmatter. Every git command, every hunk-surgery edit, every clause flip, and every validation command is documented with exact paths/line numbers and verified against the real worktree, with the known-noise footguns called out. Cross-file consistency holds (Decision-A exclusion direction is uniform across spec/R2/R3, and R3's one open dependency resolves favorably against R2). No critical or important gaps. Three Minor gaps (GAP-1 `/task` constraint not in research but defensibly out-of-scope; GAP-2 cosmetic stale status headers; GAP-3 a cross-file wiring note already resolved by R2) — none block tasklist authoring.

**The research is sufficient to build the MDTM tasklist.**
