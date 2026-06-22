# QA Report — Research Depth (P2: Integration + Meta Cluster)

**Track Goal:** Implement FR-DRS deterministic runtime-surface sweep + integration per the TDD.
**Phase:** research-depth (LENS: research-depth)
**Partition:** P2 of N
**Date:** 2026-06-22
**Fix authorization:** false (report only)
**Stance:** ADVERSARIAL — assume research is superficial until proven otherwise.

**Assigned files:**
- 05-eval-path-grader-cases-materializer.md
- 06-skill-prose-demotion-and-refs.md
- 07-test-patterns-and-verification.md
- 08-mdtm-template-and-examples.md

---

## Items Reviewed

| # | Depth question | Result | Evidence |
|---|----------------|--------|----------|
| 1 | 05: grader dispatch + C-6 consequence + C-5 materializer resolved | PASS | grader.py §1.1-1.4 verified; C-6 bucketing `:448-449` startswith-`with_skill/` verified verbatim; C-5 "what to build, where, wired how" given as Option B (sibling `materialize.py` + `run_sweep` oracle into `with_skill/outputs/`, wired into `make reflect-eval`) |
| 2 | 06: §6.1 prose quoted + PRESERVE verbatim + I6 detection mechanism | PASS | All 5 paragraphs (465/466/487/489/491) quoted verbatim & re-verified against live SKILL.md; P1-P11 PRESERVE list verbatim; I6 = `runtime_surface_sweep_ran` PRESENCE-in-contract branch (verified against TDD D2/§19.1) |
| 3 | 07: actual test idioms (construction, assertion, no-parametrize) | PASS | Zero `parametrize` confirmed by grep; `is Verdict.X` + `exit_code == N` idiom verified; 6 conftest fixtures verified present; both (a) dict→fn→assert and (b) runner-quartet patterns given with file:line |
| 4 | 08: POST gate text + B2 format + A3 4-phase decomposition | PASS | UC2 L363 wrapper item verbatim (verified UC2 exists + L363 matches); B2 6-field paragraph + B4 canonical example reproduced; A3 WRONG/RIGHT decomposition table per phase |
| 5 | Determinism (≥3-run byte-identity) + materializer responsibilities replicable | PASS | AC-2 mechanism specified (run grader ×3, assert grading.json byte-identical, pure-Python/no-network rationale); materializer responsibilities enumerated (flatten evals.json 37-41→eval_metadata.json + copytree cases/uc2-*/) |
| 6 | Builder could create per-case/per-test/per-phase items WITHOUT re-reading source | PASS | All 4 files give exact paths, verbatim quotes, per-case expected verdicts, per-test idioms, per-phase item granularity |

---

## Verification Performed (adversarial spot-checks against live source)

Every load-bearing claim independently re-verified this turn (not relied upon from the research files):

- **grader.py C-6 bucketing** (`:448-449`): confirmed `a.get("target","").startswith("with_skill/"|"old_skill/")` verbatim. R5's "silently never graded" consequence is mechanically correct.
- **`check_yaml_list_len_eq`** (`:191-210`): body matches R5's description exactly (target/list_field/count_field, int-coerce, `len == expected`). Case 41 hosts it (AC-3).
- **grade_eval metadata SKIP** (`:440-443`): confirmed `if not metadata_path.exists(): print("SKIP…"); return {}`. The mandatory `eval_metadata.json` precondition is real.
- **C-5 materializer ABSENCE**: grep for `eval_metadata.*write_text`/`copytree` in `.dev/eval-workspaces/sc-reflect/` → only `aggregate_iteration.py` + `grader.py` reference `eval_metadata.json`, both READ-only (verified). `make reflect-eval` (Makefile:505-512) is grader-only on a fresh empty timestamp dir — confirmed verbatim. R5's "CONFIRMED NOT LOCATED" verdict is accurate and the single most valuable finding in P2 (it converts an assumed-exists dependency into a must-build item).
- **SKILL.md PRESERVE sentences**: 489 ("never emits a clean PASS…", oracle/rootwalk-before-UNREACHED, NEVER STOPs, DEGRADE>UNREACHED>REACHED, count invariant) and 491 + step entries 465/466 all verified verbatim. R6's verbatim PRESERVE list is exact.
- **Contract version 1.6.0** (line 672) + six fields (731-736) + **ensemble.py:59 `"1.0"`** stale stamp: all verified. R6's "no contract_version bump; ensemble reconcile is a CODE change kept OUT of Phase-4 SKILL item" guidance is correct and well-scoped.
- **R7 no-parametrize house style**: grep confirmed ZERO `parametrize` in `tests/cli/reflect/`. Verdict idiom (`is Verdict.X` + exact `exit_code`), 6 conftest fixtures, 15 test files / 13 fixtures at 1.3.0 — all verified. R7's `make lint` = ruff-check-only (Makefile:48-50) and the mandatory separate `ruff format --check` callout verified.
- **UC2 exemplar + L363 POST wrapper** + **MDTM template** (both `.claude/` and `src/` copies): verified present; L363 wrapper item text matches R8's verbatim reproduction.
- **evals.json ids 37-41** + **case 41 expected.yaml** (FR-S9-07, unreached 1, ai_export.handle_ai_export): verified matching R5's table.
- **TDD citations real (not phantom)**: TDD exists (1549 lines); I6 `sweep_ran`-presence detection (D2/§19.1), FR-008 eval-path determinism with the exact 37-41 per-case verdicts, `_audit_once` invocation site — all present in TDD. R5/R6/R7/R8 are citing genuine TDD content.

---

## Per-File Depth Assessment

### 05-eval-path-grader-cases-materializer.md — DEEP
Goes far beyond listing file names. It explains the grader's **dispatch mechanism** (target-string-driven, 19-type flat `if` ladder), the **exact mechanical consequence of C-6** (assertions whose `target` doesn't start with `with_skill/`/`old_skill/` fall into neither bucket and are *silently never graded* — verified verbatim), and the **non-`target` assertion types that hit this trap** (`citation_resolves`, `checkpoint_logged`, etc.). Most importantly it does NOT stop at "materializer not found" — it proves the absence (grep evidence, `make reflect-eval` is grader-only on an empty dir, the prior materialization was LLM-harness-driven) AND prescribes **what to build, where, and how it wires** (Option B: sibling `materialize.py` flatten + `run_sweep` oracle writing `contract.yaml`/ledger into `with_skill/outputs/` upstream of grading, invoked by `make reflect-eval` before the grader). A builder can write the materializer item directly. The C-6-compliance design ("reuse existing `yaml_field*`/`yaml_list_len_eq` against a deterministically-written contract → no new assertion type") is a genuine architectural insight, not a restatement.

### 06-skill-prose-demotion-and-refs.md — DEEP
Quotes the **actual full text** of all five §6.1 paragraphs (465/466/487/489/491) verbatim — not "demote §6.1". Gives an 11-row PRESERVE table (P1-P11) with the load-bearing safety sentences quoted exactly and pinned to current lines (all re-verified). The **conditional-fallback detection mechanism is fully specified**: the I6 branch keys on the *presence* (not the value) of `runtime_surface_sweep_ran` in `return-contract.yaml` — present (true OR false) ⇒ narrate-only; fully-absent ⇒ legacy LLM emission. The exact injected producer sentence is provided. It also correctly scopes out the `ensemble.py:59 "1.0"` reconcile as a CODE change (not part of the Phase-4 SKILL item) and confirms `refs/runtime-surface.md` stays as-is (NG1). A builder can write the demotion item with surgical Edit old_string/new_string targets.

### 07-test-patterns-and-verification.md — DEEP
Shows the **actual house idioms** with file:line, not abstractions: the no-parametrize rule (verified zero usages), `assert result.verdict is Verdict.X` then exact `exit_code == 0/10/11/2`, reason-slug exact-string asserts, the two construction patterns ((a) `_load()`+field-mutation dict→fn→assert, (b) the 4-fixture runner quartet + `_config()` + `patch(ClaudeProcess, side_effect=factory)`), and the conftest fixture catalog. It specifies all 4 test surfaces with per-test tables (6 units + N∈{0,1,2} count invariant + fast-path + §15.4a 4-row truth table + AC-5 4-fixture safety gate) including the literal expected string `"runtime_surface_unreached"`. It correctly flags the `make lint` ≠ `ruff format --check` split and the materializer as an UNVERIFIED precondition (handing to R5). A builder can write conformant tests without opening an existing test file.

### 08-mdtm-template-and-examples.md — DEEP
Gives the **exact POST reflect gate item text** (UC2 L363 reproduced verbatim, with the skip guard, flat wrapper, `--depth deep --fix --promote`, NO-base/range/staging, exit-code consume, HALT-on-10/11/2), the **B2 6-field paragraph format** with the canonical B4 example, and the **A3 granularity decomposition** as an explicit WRONG-vs-RIGHT table for each of the 4 FR-DRS phases (module → product wire → eval wire → SKILL demotion). Frontmatter extension keys (`start_commit`, `executor_model_class`, `reflect_pre`/`reflect_post`) verified against the live UC2 frontmatter. The full QA-gate encoding (M3 ≥6-agent lens gate, I20 serialized fix, M4 fidelity applicability) is present. A builder can assemble the task skeleton + every gate + the terminal items directly.

---

## Minor Observations (NOT FAIL-worthy — recorded for builder awareness)

These do not lower the verdict; they are forward-notes the builder/orchestrator should carry. All are explicitly self-flagged by the researchers (honest gaps), which is the mark of deep research, not shallow:

- **MO-1 (cross-file dependency, handled correctly):** The C-5 materializer is owned by R5 (file 05) but is a hard precondition for R7's determinism test (file 07). Both files cross-reference it correctly and R7 explicitly hands ownership to R5. No conflict; the builder must ensure the materializer item (P3) is ordered before the determinism test item.
- **MO-2 (open design choice, correctly deferred):** R7 leaves the §15.4a derivation-test *home* unpinned (default: unit file `test_runtime_surface.py`; possibly `test_runner_e2e.py` if the derivation is runner-exercised), pending R3's consumer-wiring (a P1 file outside this partition). This is a legitimate "depends on where the function lands" deferral, phrased so the builder can write the item conditionally.
- **MO-3 (Option-A vs Option-B):** R5 recommends Option B (materializer/oracle upstream of grading) but documents Option A (new `runtime_surface_oracle` assertion type) with its C-6 caveat. The builder should encode Option B as the primary item; this is a recommendation, not an ambiguity.

[PARTITION NOTE: Cross-file checks limited to the assigned P2 subset (files 05-08). Full cross-file verification against P1 files 01-04 (esp. R1 module algorithm, R2 invocation site, R3 §5.3 consumer wiring) requires merging all partition reports. MO-1/MO-2 reference P1-owned surfaces and are noted for the orchestrator's merge step.]

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** 18 distinct load-bearing claims across grader.py (4), SKILL.md (6), tests/conftest (4), Makefile (2), evals.json/expected.yaml (2), UC2/template (2), TDD (1) — re-run this turn, not relied upon from the research text.
2. **What specific files did I read/grep?** `.dev/eval-workspaces/sc-reflect/grader.py` (lines 191-210, 318-322, 437-484), `aggregate_iteration.py` (grep), `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (465/466/487/489/491/672/731-736, header grep), `src/superclaude/cli/reflect/ensemble.py:59`, `tests/cli/reflect/conftest.py` + `test_verdict_mapping.py` + parametrize grep, `Makefile` (48-55, 505-516), `.dev/eval-workspaces/sc-reflect/evals/evals.json` (1030-1081), `cases/uc2-surface-test-only-ref/expected.yaml`, UC2 task file (L363, L19-31), MDTM template existence, TDD (281-306, 461, 210-250).
3. **If I found 0 issues, why trust the check?** I found 0 FAIL-worthy issues but 3 minor forward-notes. The adversarial probes targeted the *most likely* failure modes for shallow research: (a) "materializer not found" being a cop-out → disproved, R5 prescribes the build; (b) PRESERVE sentences being paraphrased rather than verbatim → disproved, byte-matched against live SKILL.md; (c) test idioms being asserted not observed → disproved, no-parametrize grep + idiom file:lines; (d) cited TDD/UC2 lines being phantom → disproved, all present. The research passes *because* it survives these probes with verbatim quotes and exact paths, which is precisely the bar for "builder can work without re-reading source."
4. **Web research?** None required — this review is entirely local-file-bound. No Tavily/fallback engaged.

**Confidence:** Verified: 6/6 depth questions | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 5 | Grep/Bash: 6 | Glob: 0 (ls via Bash)

---

## Overall Verdict: PASS

All four assigned P2 research files (05, 06, 07, 08) are DEEP ENOUGH to produce a high-quality integration+meta-cluster task file. The research consistently exhibits the markers of depth — verbatim quotes (not paraphrase), exact file:line/symbol/path citations re-verifiable against live source, mechanical consequence analysis (C-6 silent-skip, materializer-absence-implies-build), per-case/per-test/per-phase decomposition, and honest self-flagging of cross-file dependencies. The single highest-value finding (R5's confirmed C-5 materializer absence) converts a silently-assumed dependency into an explicit must-build task item — exactly the kind of insight a shallow "list the files" researcher would miss. A builder can author per-case (5 eval cases), per-test (4 test surfaces), and per-phase (4-phase) items from this research WITHOUT re-reading source.

No CRITICAL, IMPORTANT, or MINOR issues that block. 3 minor forward-notes (MO-1/2/3) recorded for the builder/orchestrator merge.

## QA Complete
