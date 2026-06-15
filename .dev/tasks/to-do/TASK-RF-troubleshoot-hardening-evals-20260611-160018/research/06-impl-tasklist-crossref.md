# R6 — Impl-Tasklist Cross-Reference: NEW-Gate Seam, xfail Guard, Collision Boundary

**Status: Complete**

**Scope:** Cross-reference the sibling implementation tasklist
`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260611-023739/TASK-RF-troubleshoot-hardening-20260611-023739.md`
(the "impl tasklist", 131 KB) to resolve the NEW=CATCH executable seam, the
xfail-guard strategy, and the hard file-collision boundary for OUR backtest
harness under `tests/troubleshoot/backtest/`.

**Method:** Read the impl tasklist Phase 7 (Step 7.1–7.22) + Task Overview +
File-Targets section; confirmed on-disk state of `tests/troubleshoot/`,
`src/superclaude/skills/sc-troubleshoot-protocol/`, the `tests/skills/` pattern,
and the impl branch landing status on origin.

---

## TL;DR (the four answers)

1. **(a) Files the impl CREATES that expose H0–H5 gate logic:** a NEW dir
   `tests/troubleshoot/` containing `__init__.py`, **EXACTLY 7** test modules
   (`test_hardening_h0/h1/h2/h3/h4/verdict/output_contract.py`), and
   `e2e-backtest-scenarios.md`. Plus 6 NEW `refs/*.md` under the OFF-LIMITS skill
   dir. (Full paths + wave/escape mapping in §A below.)

2. **(b) The seam is PURE-MARKDOWN. There is NO importable Python gate helper.**
   The impl's "gate logic" lives entirely in `src/.../sc-troubleshoot-protocol/refs/*.md`
   + `SKILL.md` (markdown the skill runtime reads). The impl's own tests are
   **content-assertion tests over that `src/` markdown** (the `tests/skills/`
   pattern), NOT executions of a gate. **Consequence for us:** there is nothing to
   `import` and call for NEW=CATCH. Our backtest must assert NEW=CATCH the same
   way — by asserting the *catch mechanism is documented* in the impl's `src/`
   refs (e.g. the H3 word-boundary rule, the H1 negative-witness requirement) —
   which only exist once the impl lands. See §B.

3. **(c) xfail guard:** gate on **path existence of the impl's `src/` refs** (not
   our own `tests/troubleshoot/backtest/` files, which always exist). Use a
   module-level `pytest.mark.skipif` keyed on
   `(REPO_ROOT/"src"/.../"refs"/"pipeline-hardening-closure.md").exists()` for the
   NEW=CATCH half; OLD=MISS half stays unconditional/green. See §C.

4. **(d) Collision boundary (DO NOT EDIT):** the entire skill dir
   `src/superclaude/skills/sc-troubleshoot-protocol/**`, `src/superclaude/commands/troubleshoot.md`,
   their `.claude/` sync mirrors, AND the impl's 7 test modules +
   `e2e-backtest-scenarios.md` + `__init__.py` directly under `tests/troubleshoot/`.
   Our harness lives ONLY in the NEW subdir `tests/troubleshoot/backtest/`. Full
   path list in §D.

---

## A. Files the impl tasklist CREATES / MODIFIES (exact paths + wave/escape map)

Evidence: impl tasklist **L67** (Task Overview deliverable set), **L126**
(File-Targets), **Step 7.1–7.18** (L267–L337).

### A.1 — NEW test modules under `tests/troubleshoot/` (impl-owned, content-assertion over `src/`)

The impl creates the dir + `__init__.py` + **EXACTLY 7** modules (L67, L265, L269).
"One checklist item per test MODULE" (L265). Each is a content-assertion test
(`REPO_ROOT = Path(__file__).resolve().parents[2]`) over the `src/` skill markdown
— **not** an execution of gate code (L265, L81).

| impl path | impl step | wave/gate | escape | test fns (verbatim) |
|---|---|---|---|---|
| `tests/troubleshoot/__init__.py` | 7.1 (L269) | — | — | (package marker; reads `tests/skills/test_task_builder_merge.py` for convention) |
| `tests/troubleshoot/test_hardening_h0.py` | 7.2 (L273) | H0 boundary scan / FR-1 §5.6 | applicability | `test_h0_applicability_skip_requires_boundary_scan`, `test_h0_boundary_scan_schema_rejects_bare_local_reason` |
| `tests/troubleshoot/test_hardening_h1.py` | 7.3 (L277) | H1 runtime-entrypoint / FR-3,FR-4 §5.6 | **E1** | `test_h1_runtime_card_requires_negative_and_positive_witness` |
| `tests/troubleshoot/test_hardening_h2.py` | 7.4 (L281) | H2 contract ledger / FR-5,FR-6 §5.6 | **E4** | `test_h2_empty_ledger_fails`, `test_h2_sibling_sweep_required_when_concept_shared` (NEW, reflect gap G-PRE-1) |
| `tests/troubleshoot/test_hardening_h3.py` | 7.6 (L289) | H3 unmask/sweep/classifier / FR-7,FR-8,FR-9 §5.7 grammar §5.6 | **E2, E3** | `test_h3_word_boundary_rejects_incomplete_representation`, `test_h3_small_grammar_rejects_setext_and_decorated_verdicts`, `test_h3_sweep_card_requires_k_true_k_swept_and_mixed_fixture` |
| `tests/troubleshoot/test_hardening_h4.py` | 7.5 (L285) | H4 effective-input manifest / FR-10 §5.6 | **E5** | `test_h4_nonempty_wrong_surface_fails_closed`, `test_h4_manifest_schema_requires_intersection_proof` |
| `tests/troubleshoot/test_hardening_verdict.py` | 7.7–7.9 (L293,L297,L301) | H5 mapping + verdict aggregation + waiver latch / FR-12,FR-13 §5.4 | waiver re-green (NFR-4) | `test_waiver_latch_one_way`, `test_h5_decision_maps_to_status_and_latch`, `test_known_escapes_requires_cited_card`, `test_verdict_aggregation_from_h_statuses`, `test_downstream_success_cannot_override_latched_hardening_verdict` |
| `tests/troubleshoot/test_hardening_output_contract.py` | 7.10–7.12 (L305,L309,L313) | §5.5 output contract / NFR-6, NFR-1, FR-13 AC3 | — | `test_output_contract_backward_compat`, `test_backtest_status_keeps_pipeline_health_advisory_until_complete`, `test_report_closure_section_not_proven_blockers` |
| `tests/troubleshoot/e2e-backtest-scenarios.md` | 7.13–7.18 (L317–L337) | E1–E5 + Waiver re-green | E1,E2,E3,E4,E5 + NFR-4 | **documented scenarios — NOT pytest-collected** (L353: "the E2E scenarios … are documented fixtures, not collected by pytest") |

Totals (L67, L265): **13 unit + 5 integration = 18 collected test functions** across
the 7 modules + **6 documented E2E backtest scenarios** in the `.md`. The impl's
own pytest pass command is `uv run pytest tests/troubleshoot/ -v` (Step 7.22, L353),
PASS-criteria = all 18 collected pass.

### A.2 — NEW `refs/*.md` (the ACTUAL gate-logic source-of-truth; OFF-LIMITS to us)

The H0–H5 catch mechanisms are defined in these 6 NEW refs (L67, L77, Phase 2–4).
These are the markdown our backtest's NEW=CATCH half must assert against (once they
exist):

| impl path | gate | escape | impl step |
|---|---|---|---|
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md` | mode skeleton + H0 boundary scan | applicability | 7.2 read-anchor (L273) |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md` | §5.5 schema + §5.4 7-row truth table + H5 mapping + waiver latch | verdict/NFR-4 | L77, L293 |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md` | H1 (negative+positive witness) | **E1** | 7.3 (L277) |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md` | H2 (ledger + sibling sweep) | **E4** | 7.4 (L281) |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md` | H3 (word-boundary, §5.7 grammar, sweep card) | **E2, E3** | 7.6 (L289) |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md` | H4 (intersection proof, fail-closed) | **E5** | 7.5 (L285) |

### A.3 — MODIFIED existing files (also OFF-LIMITS)

Impl tasklist L67 + L245/L257 + Step 7.10:

- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (append additive Output Contract fields; L245)
- `src/superclaude/commands/troubleshoot.md` (mode wiring; named in L361 inventory)
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` (add `## Pipeline Hardening Closure` section; L257)
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md` (carry hardening fields into BUILD_REQUEST; L301)

---

## B. The NEW=CATCH seam — RESOLVED: pure-markdown, no Python helper

**Finding (high confidence):** There is **no shared Python gate helper** under
`src/superclaude/` for the hardening gates. Evidence:

- Impl tasklist L265 explicitly: *"Each test is a **content-assertion test over
  the SOURCE-OF-TRUTH markdown** under `src/.../sc-troubleshoot-protocol/`
  following the `tests/skills/` pattern … assert markers/schemas in the `src/`
  files."* — i.e. the impl never imports/executes gate code; it asserts the
  *documented* rule exists.
- The `tests/skills/` reference file
  `/config/workspace/IronClaude/tests/skills/test_task_builder_merge.py` confirms
  the convention (verified on disk): *"content-level assertion tests over the
  source-of-truth markdown … The skill … are text artifacts consumed by Claude
  Code at runtime; the test surface here is 'does the documented behavior contain
  the required markers?' — equivalent to a content gate."* Uses
  `REPO_ROOT = Path(__file__).resolve().parents[2]`.
- The skill itself is markdown-only on disk today:
  `src/superclaude/skills/sc-troubleshoot-protocol/` contains `SKILL.md` + `refs/`
  ONLY — no `.py`. (verified: `ls` shows `refs/` + `SKILL.md`, no scripts dir.)

**Mechanical consequence for OUR backtest (NEW=CATCH):**

- We CANNOT `import` a gate function and assert it returns CATCH on the replay
  fixture. The "gate" is a behavioral rule a Claude runtime applies by reading the
  ref markdown. There is no callable.
- Therefore NEW=CATCH must be asserted as a **documentation-presence / content
  proxy**: assert that the impl's NEW refs document the specific catch mechanism
  that would have caught the OLD escape. Concretely, for each replay escape:
  - E1 → assert `runtime-entrypoint-verification.md` documents the
    negative-witness (fix-reverted→FAIL) rule.
  - E2/E3 → assert `unmask-and-sweep.md` documents the §5.7 word-boundary grammar
    + `K_swept == K_true` sweep rule.
  - E4 → assert `contract-enumeration.md` documents empty-ledger=FAIL + sibling
    sweep.
  - E5 → assert `effective-input-proof.md` documents wrong-surface fail-closed
    (`E>0` insufficient; intersection proof required).
- This is the SAME assertion style the impl's own `test_hardening_*` modules use —
  so our backtest is effectively a **redundant cross-validating proxy** keyed to
  the OLD replay fixtures. The OLD=MISS half is the part that runs unconditionally
  green today (assert the replayed artifact reproduces the historical MISS — no
  ref needed); the NEW=CATCH half is the part that depends on the impl refs.

> NOTE for the builder: do not duplicate the impl's `test_hardening_*` modules.
> Our value-add is the **OLD=MISS replay half** (green now) + a thin NEW=CATCH
> proxy guarded to xfail/skip until the refs land. Keep the backtest focused on
> the replay-fixture → escape-class mapping; defer the executable replay suite to
> the impl's own M5 (NFR-1 measurement harness, which the impl tasklist L96 marks
> OUT of scope / deferred — Step 7.13 L317: *"the NFR-1 replay suite, deferred to
> M5, will execute it"*).

---

## C. xfail-guard strategy — RESOLVED

**Branch landing status (verified):**

- `feat/troubleshoot-pipeline-hardening` is **NOT on origin** (`git ls-remote
  origin feat/troubleshoot-pipeline-hardening` → empty).
- `tests/troubleshoot/` does **NOT exist** on `origin/master` (`git ls-tree
  origin/master tests/troubleshoot` → empty) and does NOT exist in the current
  worktree (`ls tests/troubleshoot` → No such file or directory).
- It exists ONLY in the local impl worktree at
  `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening` (branch
  confirmed checked out there) — and even there, Phase 7 is HALTED pending G1
  approval (frontmatter L4: *"Execution is HALTED pending G1 approval; this
  tasklist is PRODUCED ONLY"*). So the refs may not be authored even in the
  worktree yet.

**Recommended guard (skipif on impl-ref path existence, NOT importorskip):**

Because the seam is markdown (nothing importable), `pytest.importorskip` does NOT
apply. Use **`pytest.mark.skipif` keyed on the impl ref file existing** in the
checked-out repo. Anchor on the most foundational ref so a partial landing still
guards correctly:

```python
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]   # tests/troubleshoot/backtest/<file> → repo root
HARDENING_REFS = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "refs"
_IMPL_LANDED = (HARDENING_REFS / "pipeline-hardening-closure.md").exists() \
    and (HARDENING_REFS / "hardening-output-contract.md").exists()

requires_hardening_impl = pytest.mark.skipif(
    not _IMPL_LANDED,
    reason="NEW=CATCH half: sc-troubleshoot-protocol hardening refs not landed yet "
           "(feat/troubleshoot-pipeline-hardening). OLD=MISS half runs unconditionally.",
)
```

- **`parents[3]`** — NOTE the depth difference: our files live at
  `tests/troubleshoot/backtest/<file>.py` → that is 3 levels under repo root
  (`backtest` → `troubleshoot` → `tests` → root), so use `parents[3]`, NOT the
  impl's `parents[2]`. Confirm at build time by asserting `(REPO_ROOT /
  "pyproject.toml").exists()` in a guard test.
- **skipif vs xfail:** prefer **skipif** (clean SKIP, no noise) over
  `xfail(strict=False)`. xfail would surface as XPASS the moment the refs land,
  which is acceptable but louder. The task GOAL phrasing says "xfail until impl
  lands" — if the builder prefers xfail to make the pending state visible in CI,
  use `@pytest.mark.xfail(condition=not _IMPL_LANDED, reason=..., strict=False,
  run=True)`; but skipif is the lower-noise choice and is what the impl's own
  pattern implies (the impl simply doesn't run until authored). **Recommendation:
  skipif on ref-existence for the NEW half; OLD=MISS half unconditional.**
- Apply the marker per-NEW-test-function (or module-level via `pytestmark`), so the
  OLD=MISS assertions in the same file remain unconditionally collected + green.

---

## D. COLLISION BOUNDARY — explicit "DO NOT EDIT" path list

Our harness MUST create files **only** under the NEW subdir
`tests/troubleshoot/backtest/` (per task GOAL). It must NOT create/modify any path
the impl owns. Encode this constraint in the builder.

### D.1 — OFF-LIMITS (impl-owned src/, the skill the impl /task owns)

```
src/superclaude/skills/sc-troubleshoot-protocol/**          # ENTIRE dir off-limits
  ├─ SKILL.md                                               # impl MODIFIES (L245)
  └─ refs/
     ├─ pipeline-hardening-closure.md                       # impl CREATES
     ├─ hardening-output-contract.md                        # impl CREATES
     ├─ runtime-entrypoint-verification.md                  # impl CREATES
     ├─ contract-enumeration.md                             # impl CREATES
     ├─ unmask-and-sweep.md                                 # impl CREATES
     ├─ effective-input-proof.md                            # impl CREATES
     ├─ report-template.md                                  # impl MODIFIES (L257)
     └─ remediation-handoff.md                              # impl MODIFIES (L301)
src/superclaude/commands/troubleshoot.md                    # impl MODIFIES (L361 inventory)
```

(Reading these refs for assertion targets is fine; **editing/creating** them is the
violation. Our backtest only READS them, guarded by skipif.)

### D.2 — OFF-LIMITS (`.claude/` sync mirrors — gitignored, never staged anyway)

```
.claude/skills/sc-troubleshoot-protocol/**
.claude/commands/sc/troubleshoot.md   (or .claude/commands/troubleshoot.md per install layout)
```

(Per CLAUDE.md ABSOLUTE RULE these are sync-dev output of `src/`; never edit/stage.
The impl regenerates them via `make sync-dev`.)

### D.3 — OFF-LIMITS (impl's own test files directly under `tests/troubleshoot/`)

```
tests/troubleshoot/__init__.py                  # impl CREATES (Step 7.1)
tests/troubleshoot/test_hardening_h0.py         # impl CREATES (Step 7.2)
tests/troubleshoot/test_hardening_h1.py         # impl CREATES (Step 7.3)
tests/troubleshoot/test_hardening_h2.py         # impl CREATES (Step 7.4)
tests/troubleshoot/test_hardening_h3.py         # impl CREATES (Step 7.6)
tests/troubleshoot/test_hardening_h4.py         # impl CREATES (Step 7.5)
tests/troubleshoot/test_hardening_verdict.py    # impl CREATES (Steps 7.7-7.9)
tests/troubleshoot/test_hardening_output_contract.py  # impl CREATES (Steps 7.10-7.12)
tests/troubleshoot/e2e-backtest-scenarios.md    # impl CREATES (Steps 7.13-7.18)
```

### D.4 — OURS (the ONLY place we write)

```
tests/troubleshoot/backtest/**                  # NEW subdir, distinct from impl's tests/troubleshoot/test_*.py
```

> **Shared-parent hazard:** both the impl and our harness create files under
> `tests/troubleshoot/`. The impl creates `tests/troubleshoot/__init__.py` and the
> 7 modules directly in that dir; WE create the `backtest/` SUBDIR. **Two
> collision risks the builder must handle:**
>
> 1. **`__init__.py` race.** If our harness runs/lands BEFORE the impl, the impl's
>    `tests/troubleshoot/__init__.py` won't exist, so pytest may not collect our
>    `backtest/` subpackage cleanly. **Recommendation:** our harness should ensure
>    `tests/troubleshoot/backtest/__init__.py` exists, AND it is SAFE for us to
>    create `tests/troubleshoot/__init__.py` IF-AND-ONLY-IF it does not already
>    exist (empty file) — but this is a soft collision: the impl's Step 7.1 also
>    creates it. To avoid a hard collision, prefer making `backtest/` a
>    self-contained package (`tests/troubleshoot/backtest/__init__.py`) and NOT
>    touching the parent `tests/troubleshoot/__init__.py`; rely on pytest rootdir +
>    `conftest`/`__init__.py` in `backtest/` for collection. If collection requires
>    the parent `__init__.py`, document it as a one-time bootstrap that the impl
>    will also (idempotently) create — flag for the builder to decide and encode an
>    explicit "create parent `__init__.py` ONLY if absent; never overwrite" guard.
> 2. **Do NOT redefine the impl's test-function names.** Our `backtest/` modules
>    must use distinct module + function names (e.g. `test_backtest_e1_old_miss`,
>    not `test_hardening_h1...`) to avoid any pytest nodeid confusion across the
>    shared `tests/troubleshoot/` tree.

---

## E. Builder-facing recommendations (encode these as task constraints)

1. **Harness location:** create ONLY `tests/troubleshoot/backtest/` + its own
   `__init__.py`; never write under `src/.../sc-troubleshoot-protocol/`,
   `src/.../commands/troubleshoot.md`, `.claude/**`, or the impl's 8 files directly
   in `tests/troubleshoot/`.
2. **REPO_ROOT depth = `parents[3]`** for files at `tests/troubleshoot/backtest/`
   (verify via a `pyproject.toml` existence assert).
3. **OLD=MISS half:** unconditional, green today — assert each replay fixture
   reproduces the historical escape MISS (no impl ref dependency).
4. **NEW=CATCH half:** `pytest.mark.skipif(not _IMPL_LANDED, ...)` keyed on
   `src/.../refs/pipeline-hardening-closure.md` + `hardening-output-contract.md`
   existence; assert the catch mechanism is DOCUMENTED in the matching NEW ref
   (proxy, since the gate is pure-markdown — no callable to invoke).
5. **No duplication:** do not re-author the impl's `test_hardening_*` assertions;
   our NEW=CATCH proxy is a redundant cross-check keyed to the OLD replay fixtures,
   not a clone of the impl suite.
6. **`__init__.py` collision:** make `backtest/` a self-contained package; if the
   parent `tests/troubleshoot/__init__.py` is required for collection, create it
   ONLY-IF-ABSENT and never overwrite (the impl's Step 7.1 owns it).
7. **Distinct test-fn names** across the shared `tests/troubleshoot/` tree.

---

## F. Citations (impl tasklist line anchors)

- L4 (frontmatter): HALTED pending G1, PRODUCED ONLY.
- L67: deliverable set — 6 new refs, 4 modified, 7 test modules (named), 13+5 tests, 6 E2E scenarios.
- L81 / L265: content-assertion-over-`src/`-markdown pattern; `parents[2]`; `tests/skills/` precedent.
- L96: M5 backtest measurement harness is DEFERRED / OUT of scope of the impl.
- L126: `tests/troubleshoot/` is NEW (does not exist yet); create dir + `__init__.py`.
- L269 (Step 7.1): create dir + `__init__.py`; references `tests/skills/test_task_builder_merge.py`.
- L273/277/281/285/289/293/297/301/305/309/313: per-module test creation + function names + gate/escape mapping.
- L317–L337 (Steps 7.13–7.18): 6 E2E backtest scenarios in `e2e-backtest-scenarios.md` (documented, NOT pytest-collected — L353).
- L245/L257/L301/L361: the 4 modified `src/` files + the consolidated deliverable inventory.

**On-disk / git verifications performed:**
- `tests/troubleshoot/` absent in worktree + absent on `origin/master`.
- `feat/troubleshoot-pipeline-hardening` absent on origin; present in local worktree `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening`.
- `src/.../sc-troubleshoot-protocol/` = `SKILL.md` + `refs/` only (8 existing refs, none of the 6 new ones yet) — no Python.
- `tests/skills/test_task_builder_merge.py` confirms the content-assertion convention + `parents[2]`.
- `src/superclaude/commands/troubleshoot.md` exists (impl will modify it).
