# Cross-Validation Report — sc-bare-review M8/M9 Migration Research

**Analysis type:** completeness-verification
**Lens:** cross-validation (claims BETWEEN research files)
**Date:** 2026-06-16
**Track goal:** Corrective MDTM tasklist for sc-bare-review M8/M9 migration

**Files analyzed:**
- 01-skill-and-scripts-inventory.md (R1)
- 02-swarm-cli-thin-caller-surface.md (R2)
- 03-parity-test-and-swarm-test-conventions.md (R3)
- 04-docs-and-release-notes-staleness.md (R4)
- 05-mdtm-template-and-sync-discipline.md (R5)

---

## Status: IN PROGRESS — cross-validating

---

## Check 1 — Does the inline `swarm run --lens bare-review` path currently produce normalized output + return-contract? (R1 vs R2 vs R3)

**Verdict: CONSISTENT (no contradiction). R1's framing reconciles with R2/R3.**

The three files agree on the underlying mechanical fact and are NOT in conflict:

- **R2 B-5 (headline)** — the inline (non-resume) `run_cmd` body "calls **only `dispatch_wave1`** and emits a **stdout stub line**. It does **NOT** call `normalize_wave2`, `reduce_wave3`, or `emit_contract`, and it dispatches with an **empty prompt** (`prompt=""`)." Evidence: `commands.py:1554-1578` (stub) vs `commands.py:1930-1977` (resume path fully wired). The recipe `bare_review_v1` "exists but is never invoked on the inline path." (R2 lines 24-32, 196-225, 243-248)
- **R3 §3.3 (BLOCKER)** — "fresh `swarm run` is dispatch-only — it does NOT normalize/reduce or persist worker content." Evidence: `commands.py:1558-1577`; pinned by `test_e2e_user_guide.py:104-114` (`test_quickstart_does_not_emit_m5_artifacts`); normalize/reduce wired only on `--resume` (`commands.py:1949-1977`). (R3 lines 124-134, 202)

**R2 B-5 and R3 §3.3 AGREE** — both cite the same code seam (`commands.py:1554-1577` stub vs resume-only normalize/reduce) and reach the identical conclusion: the inline path emits no `return-contract.yaml`, no `merged.md`, no normalized per-reviewer bodies; the recipe never runs inline. This is the single strongest cross-file corroboration in the set — two independent researchers, same evidence, same verdict.

**R1's "the replacement already exists" framing is RECONCILED, not contradictory.** R1 is making a narrower, accurate claim: the lens (`bare_review.py`), the recipe (`bare_review_v1.py`), the entry point (`swarm run --lens bare-review`), and the swarm-aware template (`refs/templates/bare-review-output.md`) all **exist as artifacts** (R1 lines 30-34, 191). R1 never claims the inline path is functionally wired end-to-end. Critically, R1 explicitly DEFERS the CLI surface to R2: "R1 confirms the legacy surface; R2 confirms the CLI surface that replaces it" (R1 line 34) and "the swarm CLI surface (R2's scope)" (R1 line 33). R1 also flags the parity/contract-reproduction risk as a builder must-verify ("the builder must verify the swarm CLI emits a byte-compatible contract", R1 line 86) rather than asserting it is already done.

**Synthesis of the three:** "The components exist (R1) but the inline CLI plumbing that would invoke them is a stub (R2 B-5 = R3 §3.3 BLOCKER)." This is a coherent, non-contradictory picture. The only nuance a builder must carry forward: R1's headline "MIGRATION HEADLINE: The swarm CLI replacement already exists" (R1 line 30) is true at the artifact level but could be MISREAD as "the migration is functionally ready." R2/R3 supply the corrective that the inline path is NOT functional. The tasklist must treat B-5 / the M5 wiring as a hard prerequisite, which both R2 (B-5) and R3 (§4.5 sequencing) already state. **No gap — agreement is strong.**

---

## Check 2 — Do the script paths agree across R1/R3/R4 (skill-dir `scripts/` vs repo-root `scripts/`)?

**Verdict: CONSISTENT. All three refer to the SKILL-DIR scripts; R4's "still present in scripts/" means the skill-dir path. No path collision in the migration target.**

The three legacy scripts being migrated live at the **skill-dir** path, and all three files agree:

- **R1** — `src/superclaude/skills/sc-bare-review/scripts/{t2_preflight.sh, t2_dispatch.sh, t2_normalize.py}` (R1 lines 15-21, directory inventory; restated lines 118-185).
- **R3** — `LEGACY_SCRIPT = <repo>/src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py` (R3 lines 34-35, citing `test_bare_review_parity.py:111-119`).
- **R4** — "`ls src/superclaude/skills/sc-bare-review/scripts/` shows `t2_dispatch.sh` (5068 B), `t2_normalize.py` (10429 B), `t2_preflight.sh` (9976 B)" (R4 line 89). **R4's summary phrase "scripts/*.sh still present" (R4 lines 92, 154) unambiguously refers to the SKILL-DIR scripts** — the `ls` command it cites is the full skill-dir path. CONFIRMED: R4 does not mean repo-root `scripts/`.

**Important disambiguation the builder MUST carry — there are TWO different `scripts/` directories in play, and they are NOT the same:**

1. **Skill-dir `scripts/`** = `src/superclaude/skills/sc-bare-review/scripts/` — holds the 3 LEGACY scripts to be DELETED by the migration (R1, R3, R4 all reference this).
2. **Repo-root `scripts/`** = `scripts/` at repo root — holds UNRELATED tooling that the migration ADDS to or depends on, specifically:
   - R4 OPS-002 requires a NEW `scripts/swarm_env_readiness.sh` at **repo-root `scripts/`, NOT `docs/`** (R4 lines 129, 25).
   - R5 references repo-root pre-commit hook scripts `scripts/precommit_block_claude_mirrors.sh` and `scripts/precommit_verify_bare_review_sync.sh` (R5 lines 210, 217, 220).

Cross-file byte/size agreement on the skill-dir scripts: R1 gives `t2_dispatch.sh` 5068 B / `t2_normalize.py` 10429 B / `t2_preflight.sh` 9976 B (R1 lines 17-19) — **byte-identical to R4's `ls` figures** (R4 line 89: 5068 / 10429 / 9976). Line counts also agree: R1 `t2_normalize.py` = 316 lines (line 19); R3 treats the same file as the importlib legacy reference. **No contradiction; the two `scripts/` dirs are distinct and consistently used.** Builder note: when the tasklist says "delete `scripts/*.sh`" it MUST scope to the skill-dir path and MUST NOT touch repo-root `scripts/` (which is where OPS-002's new script lands and where the pre-commit hooks live).

> MINOR observation (not a contradiction): the phrase "delete `scripts/*.sh`" is itself imprecise — the skill-dir holds two `.sh` files (`t2_preflight.sh`, `t2_dispatch.sh`) PLUS one `.py` file (`t2_normalize.py`). A literal `scripts/*.sh` glob would leave `t2_normalize.py` behind. R1 (line 21), R3 (the `t2_normalize.py` legacy reference), R4 (line 89), and R5 (line 307 lists all three) all correctly enumerate the THREE files. The builder should write deletion items per-file (3 items) per R5's A3 granularity rule, not as a `*.sh` glob.

---

## Check 3 — SKILL.md line count (231) consistent across R1/R4/R5?

**Verdict: CONSISTENT. All three independently report 231 lines.**

| File | Claimed SKILL.md line count | Evidence cited |
|------|-----------------------------|----------------|
| R1 | **231** | "SKILL.md  231 lines / 11185 B" directory inventory (R1 line 16); restated "SKILL.md (231 lines)" (R1 line 38) and throughout §1.11 region table (R1 lines 101-114) |
| R4 | **231** | "`wc -l src/superclaude/skills/sc-bare-review/SKILL.md` = **231 lines**, not ~60" (R4 line 88); restated R4 lines 92, 154 |
| R5 | **231** | "`wc -l … SKILL.md` = **231 lines** (verified this session)" (R5 line 304) |

All three agree exactly on **231**, each with independent verification (R1 via `wc -l` in directory inventory, R4 via explicit `wc -l`, R5 via `wc -l` "verified this session"). R1 additionally supplies the byte count (11185 B). The shared use of 231 to contradict the release-note's "~60-line thin caller" claim is consistent across R1 (implicit — documents the 231-line thick orchestrator), R4 (explicit CODE-CONTRADICTED, line 88), and R5 (T08.01 "NOT done", line 301-304).

**Ownership note (handled correctly, no conflict):** R4 explicitly defers the authoritative SKILL.md figure to R1 — "R1 owns SKILL.md/scripts. The 231-line figure here is cross-validation for the doc claim" (R4 line 96). R1 owns it, R4 and R5 corroborate. The target line count for the migrated thin caller is also consistent: R1 "~60-line thin caller" (line 6, 114), R4 "~60-line" (the contradicted claim's target, line 77), R5 validation gate "`wc -l SKILL.md ≤ 80`" (lines 282, 319, 374). The ~60 target vs ≤80 validation ceiling is NOT a contradiction — ≤80 is a conservative pass threshold for a ~60-line goal (it allows headroom), and R5 sources it from the prior phase-8 tasklist's own validation (`wc -l … ≤80 lines`, R5 line 282 / phase-8 T08.01). **No gap.**

---

## Check 4 — Parity-test characterization (library-vs-library) consistent R2/R3?

**Verdict: CONSISTENT. R2 and R3 agree the current parity test is library-vs-library, neither drives the CLI subprocess.**

- **R3 (owner)** is unambiguous and self-evidenced: the current `test_bare_review_parity.py` "compares **`t2_normalize.py` (legacy lib) vs `BareReviewV1` recipe + `determine_status` (new lib)**. Both halves are library-level; neither drives `superclaude swarm run`." The test's own docstring admits it ("Why not drive the actual CLI subprocess", `test_bare_review_parity.py:38-51`). The thin-caller side is "a direct in-process call to the recipe class plus the reducer function… No `swarm run`, no `CliRunner`, no `JobSpec`, no preflight, no transport." (R3 lines 15-38)
- **R2** corroborates from the recipe angle: the `bare_review_v1` recipe "is an **intentional byte-identical port** of the per-reviewer transform from the legacy `t2_normalize.py`" and references the A/B parity gate "`tests/swarm/test_recipe_bare_review.py` (bare_review_v1.py:14-22) — (R3's domain to confirm it passes)." (R2 lines 132-148). R2 explicitly defers parity-test confirmation to R3 (line 148) and never claims the parity test drives the CLI.

**Cross-file consistency on the consequence:** both identify that deleting `t2_normalize.py` breaks the gate. R3 §1.3 — the `skipif(LEGACY_SCRIPT.exists())` guard means "this entire module **self-deactivates silently** (whole-module skip)" when WS-C deletes the script (R3 lines 41-53). R2's B-5 and R3's §3.3/§4.5 both flag that a true CLI-driven gate is BLOCKED on M5 wiring landing normalize/reduce on the fresh path — R3 explicitly says "Coordinate with R2 (swarm CLI surface)" (R3 line 179, 202). The two files are mutually referential and consistent.

**One filename nuance to flag for the builder (not a contradiction, but a naming spread the tasklist must resolve):** the research set references THREE different parity/recipe test filenames, and they are NOT interchangeable:
- `tests/swarm/test_bare_review_parity.py` — the CURRENT library-vs-library A/B gate (795 lines, 17 tests). Cited by R1 (line 97, 195), R3 (the whole §1), R5 (lines 311-314).
- `tests/swarm/test_recipe_bare_review.py` — the byte-identity recipe parity gate (TEST-003 / M8). Cited by R1 (line 180, "byte-identity parity gate against legacy `t2_normalize.py`"), R2 (line 147), R5 (line 314, present on disk).
- `tests/swarm/test_recipe_no_judging.py` — the AC-011 no-judging boundary test. Cited by R1 (line 179).

R1 itself notes the two-filename spread: "(Note: the swarm template ref also cites `test_recipe_bare_review.py` byte-identity parity — §1.11 / R3.)" (R1 line 97). This is consistent across files (each cites the same filenames for the same purpose) but the builder MUST be precise about WHICH test it is hardening/replacing: R3's design (§4) replaces `test_bare_review_parity.py` with a frozen-golden CLI gate; `test_recipe_bare_review.py` is a separate recipe-level byte-identity test. **No contradiction — flagged as a precision requirement.**

> MINOR cross-file inconsistency (test-count, non-blocking): R5 line 310 says `test_bare_review_parity.py` "collects 17 tests this session" / "collected 17 tests cleanly" (R5 lines 311, 334). R3 line 60 enumerates "7 tests (all but two parametrized over the 3 scenarios)." These are reconcilable, not contradictory: 7 test FUNCTIONS × parametrization over 3 SCENARIOS = ~17 collected test ITEMS (5 of the 7 parametrize ×3 = 15, plus 2 non-parametrized = 17). R3 counts functions; R5 counts pytest-collected items. The builder should use R3's per-function breakdown (§1.4) for the test design and R5's "17 collected" only as a smoke figure. No action required beyond noting the two numbers measure different things.

---

## Check 5 — OPS-doc counts + lens-contribution-policy location consistent? (within R4, cross-checked vs R1)

**Verdict: CONSISTENT internally; one cross-file location nuance to surface.**

R4 is the sole owner of the OPS-doc inventory; no other assigned file makes competing OPS-doc claims, so this check is primarily an internal-consistency audit of R4 plus a cross-check of the lens-policy location against R1/R2.

**OPS-doc counts — internally consistent in R4:**
- "6 OPS docs" requirement (OPS-001..006) — R4 lines 16, 20-29 (the OPS ID → deliverable table), restated line 153 "0/6 OPS docs + 0/2 checkpoints."
- Audit verdict "0/8 SHIPPED" (R4 line 17) reconciles with "0/6 OPS docs + 0/2 checkpoints" (R4 line 153): 6 OPS docs + 2 checkpoints = 8 deliverables, all absent. **Internally consistent.**
- Per-OPS classification table (R4 §4, lines 126-133) covers exactly OPS-001..006 + 2 checkpoints = 8 rows of disposition. 5 NET-NEW (OPS-001/002/003/004/006), 1 RELOCATE/cross-ref (OPS-005), plus 2 NET-NEW checkpoints. Counts add up.

**lens-contribution-policy location — consistent, with a deliberate two-path distinction the builder must preserve:**
- R4 establishes the canonical policy ALREADY EXISTS at **`docs/dev/lens-contribution-policy.md`** (515 lines, Jun 8) and is a strict SUPERSET of OPS-005's requirement (R4 lines 100-120). It covers C1-C5 criteria + validator reference + PR checklist + suspect:true scrutiny.
- The OPS-005 REQUIRED path is **`docs/swarm/lens-contribution-policy.md`** (R4 line 28, 132) — a DIFFERENT directory (`docs/swarm/` not `docs/dev/`).
- R4's recommendation (cross-reference or relocate, lines 115-120, 132) correctly handles the `docs/dev/` vs `docs/swarm/` split. **Internally consistent.**

**Cross-check vs R2 (lens registry):** R4's policy doc governs entries in `cli/swarm/lenses/__init__.py::LENSES` (R4 line 104). R2 independently confirms the `bare-review` lens IS registered in `LENSES` (R2 lines 117-124, `lenses/__init__.py:106`). The lens-policy doc's subject (the LENSES registry) and R2's lens-registration evidence are consistent — same registry, same file. No contradiction.

**Cross-check vs R1 (the lens-contribution C-criteria):** R4's C2 criterion is "§11.5 injection-guard substring" (R4 line 108). R1 references the same injection guard from the prompt side — the `<<<TARGET>>>…<<<END TARGET>>>` injection guard "(§11.5)" (R1 line 168) — and R2 confirms the lens appends `CANONICAL_INJECTION_GUARD_SENTENCE` (R2 line 107). The §11.5 injection-guard concept is consistently referenced across R1, R2, and R4. **No gap.**

> MINOR (builder decision, already flagged by R4): R4 line 118 notes the phase-9-tasklist "was authored unaware the dev-side policy already existed" (grep for `docs/dev` returned no hits), which is WHY OPS-005 says author-from-scratch. This is a reconciliation note, not a cross-file contradiction within the research set — all files that touch the lens policy (R4 primary; R1/R2 corroborating the §11.5 guard + registry) agree.

---

## Check 6 — Any divergent claim about the 4 missing CLI flags?

**Verdict: CONSISTENT. R2 is the sole authoritative source for the 4-flag gap; R1 corroborates the flag SURFACE without contradiction.**

**R2 (owner)** is unambiguous: exactly **4** legacy flags have no `swarm run` CLI equivalent — `--reviewers`, `--timeout-sec`, `--target-line-cap`, `--label` (R2 lines 18-21 TL;DR; blockers B-1..B-4 at lines 79-82; net findings lines 230-241). R2 backs this with a negative grep (R2 line 57) and per-flag evidence anchors. The two flags that DO map directly are `--target` and `--output` (R2 lines 77-78). So of 6 legacy preflight flags, 2 map directly and 4 are missing.

**R1 corroborates the flag surface (no contradiction).** R1 §1.4 documents the caller-facing flag contract as **6 primary flags**: `--target`, `--reviewers`, `--output`, `--target-line-cap`, `--timeout-sec`, `--label` (R1 lines 60-70), plus the `--c7*` no-op trio. This is the SAME 6-flag legacy surface R2 enumerates from `t2_preflight.sh` (R2 lines 64-71). R1 does not claim these are already present on the swarm CLI — it says "The thin caller's job is to MAP them onto the swarm CLI lens flags (R2 owns the target flag names)" (R1 line 70). **R1 explicitly defers the swarm-side flag-name authority to R2**, which is exactly where the 4-missing-flag finding lives. No divergence.

**Cross-check the specific defaults (consistent):**
| Flag | R1 default (legacy) | R2 lens/spec value | Consistent? |
|------|---------------------|--------------------|-------------|
| `--reviewers` | 3 (range 2-4) | `lens.default_workers=3`; legacy range [2,4] (R2 line 79) | YES — both cite default 3, range 2-4 |
| `--target-line-cap` | 4000 | `lens.default_target_line_cap=4000` (R2 line 80) | YES |
| `--timeout-sec` | 180 / `T2Timeout` | spec hardcodes `timeout_sec=180` (R2 line 81) | YES |
| `--label` | empty | `caller.invocation_label=f"swarm-run-lens-{lens_name}"` (R2 line 82) | YES (both: caller-supplied label, lens supplies a default) |

All four defaults agree between R1 (legacy semantics) and R2 (lens/spec values). The migration nuance R2 adds — that the lens DEFAULTS supply fixed values so a thin caller "cannot vary them from the CLI without writing a full spec file" (R2 lines 20-21) — is consistent with R1's framing that the flags must be "mapped onto" the swarm CLI (R1 line 70). The builder must add the 4 missing CLI options (B-1..B-4) so the thin caller can pass them through; both files support this. **No gap.**

---

## Cross-Validation Summary

| # | Cross-validation check | Files | Result |
|---|------------------------|-------|--------|
| 1 | Inline path produces normalized output + contract? | R1/R2/R3 | CONSISTENT — R2 B-5 = R3 §3.3 (inline = stub); R1 "replacement exists" is artifact-level, explicitly defers CLI to R2. Reconciled, not contradictory. |
| 2 | Script paths (skill-dir vs repo-root) | R1/R3/R4 | CONSISTENT — all = skill-dir `src/.../sc-bare-review/scripts/`; R4 "still present in scripts/" = skill-dir; byte sizes match across R1/R4. |
| 3 | SKILL.md line count = 231 | R1/R4/R5 | CONSISTENT — all three independently report 231; R4 defers authority to R1. |
| 4 | Parity test = library-vs-library | R2/R3 | CONSISTENT — both agree neither half drives the CLI; R2 defers confirmation to R3. |
| 5 | OPS-doc counts + lens-policy location | R4 (+R1/R2 cross-check) | CONSISTENT — 6 OPS + 2 checkpoints = 8; `docs/dev/` (exists) vs `docs/swarm/` (required) split handled; §11.5 guard + LENSES registry corroborated. |
| 6 | The 4 missing CLI flags | R2 (+R1 cross-check) | CONSISTENT — R2 authoritative (4 missing); R1 documents same 6-flag surface and defers flag names to R2; all 4 defaults agree. |

### Contradictions found
**NONE.** No cross-file claim contradicts another. Every divergence examined resolved to either (a) a deliberate ownership split where one file defers to the authoritative owner, or (b) two files measuring different things consistently (e.g. test-functions vs collected-items).

### Minor (non-blocking) observations surfaced for the builder
1. **`scripts/*.sh` is an imprecise glob** — the skill-dir holds 3 files including `t2_normalize.py` (`.py`, not `.sh`). Write 3 per-file deletion items, not a `*.sh` glob (Check 2).
2. **Two distinct `scripts/` directories** — skill-dir (3 legacy scripts to DELETE) vs repo-root (OPS-002's NEW `swarm_env_readiness.sh` + pre-commit hooks to PRESERVE). Deletion items must scope to skill-dir only (Check 2).
3. **Three parity/recipe test filenames** — `test_bare_review_parity.py` (current lib gate, to be replaced by R3's CLI golden gate), `test_recipe_bare_review.py` (recipe byte-identity, M8/TEST-003), `test_recipe_no_judging.py` (AC-011). Builder must name the exact test per item (Check 4).
4. **Test-count 7 (R3 functions) vs 17 (R5 collected items)** measure different things; use R3's per-function breakdown for design (Check 4).
5. **~60 target vs ≤80 validation ceiling** for migrated SKILL.md — not a contradiction; ≤80 is the conservative pass threshold (Check 3).

### Cross-cutting dependency that all relevant files agree on (builder MUST sequence)
The **M5 inline-pipeline wiring (R2 B-5)** is a hard prerequisite for **R3's permanent CLI-driven parity gate** (R3 §4.5 explicitly: "Coordinate with R2"). And **R5's L5 conditional-action pattern** must gate the **legacy script deletion (R1/R4)** behind the parity test passing — mirroring the prior phase-8 T08.07-after-T08.11 ordering (R5 §3.1). These three dependencies are stated consistently across R1, R2, R3, and R5; no file contradicts the sequencing.

---

## VERDICT: PASS

All 6 cross-validation checks returned CONSISTENT. Zero contradictions between the 5 research files. The apparent tension in Check 1 (R1 "replacement already exists" vs R2/R3 "inline path is a stub") resolves cleanly: R1's claim is artifact-level (lens/recipe/template exist) and R1 explicitly defers the CLI-functional question to R2 — R2 B-5 and R3 §3.3 agree the inline path is non-functional. Counts (231 SKILL.md lines; 3 legacy scripts; 6 OPS docs + 2 checkpoints; 4 missing CLI flags) and paths (skill-dir vs repo-root `scripts/`; `docs/dev/` vs `docs/swarm/` lens policy) are consistent across every file that touches them. The 5 minor observations above are precision notes for the builder, not blocking gaps.

**Status: Complete**
