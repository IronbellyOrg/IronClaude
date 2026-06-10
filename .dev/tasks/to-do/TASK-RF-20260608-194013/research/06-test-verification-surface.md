# Research 06 — Test & Verification Surface

**Status: In Progress**

**Topic:** Realistic verification approach for the `--reflect auto|1|2` POST-gate markdown
(SKILL.md / rf-qa.md) refactor.

**Scope:** `tests/` (esp. `tests/skills/`, `tests/audit/`), Makefile test/lint targets,
spec §13 Acceptance Test Matrix.

**Goal:** De-risk the BUILD_REQUEST `TESTING_REQUIREMENTS` decision — determine whether
§13 ATs (AT-FR1..AT-PLUMBING-1) have a realistic automated (fixture-based) surface, or
whether verification is self-consistency review + `make verify-sync` + markdownlint +
manual AT walkthrough.

---

## 1. Existing task-builder / skill test coverage

### `tests/skills/test_task_builder_merge.py` (519 lines)

**Pattern — content-level markdown assertion test (NO CliRunner, NO subprocess).**
The module docstring (lines 1-12) states it plainly: *"content-level assertion tests
over the source-of-truth markdown files in src/superclaude/skills/task-builder/SKILL.md
and src/superclaude/agents/rf-*.md … the test surface here is 'does the documented
behavior contain the required markers introduced by each landing?' — equivalent to a
content gate."*

Mechanics:
- Module-scope fixtures read the **src/ side** of each spec into a string
  (`SKILL_PATH.read_text()`, `RF_QA_PATH.read_text()`, etc.) — file:22-52.
  It verifies the **source of truth only** because `src/superclaude/` is canonical
  (docstring lines 9-11).
- Tests are plain **`in` / `not in` / `.count() >= N`** string assertions plus
  `pytest.mark.parametrize` over marker lists. Examples:
  - `assert "#### Checklist (28 items)" in rf_qa_text` (line 69) — pins a literal
    count string.
  - `assert tag in rf_qa_text` parametrized over `TB-Add-1..8` (lines 71-101).
  - `assert skill_text.count("TB-Add-8") >= 2` (line 201) — "appears in BOTH the A.10
    prompt and the validation checklist."
  - `assert "| # | Check | axis | Result | Evidence |" in rf_qa_qualitative_text`
    (line 326) — pins an exact table-header literal.
  - Section-scoped assertion via `.split()` to isolate a rule block, then assert a
    cross-reference inside it (lines 420-422 — Rule 7 block).

**This is the direct precedent for the `--reflect` refactor's verification.** A new test
class (e.g. `TestReflectPostGate`) in this same file would assert the SKILL.md / rf-qa.md
markers the refactor introduces: `reflect_post_mode`, the `superclaude reflect run
{TASK_FILE}` wire string, `/sc:reflect --mode post --depth standard`, the V1–V16 table
literals, the §9.3 MODE-MATCH block, `REFLECT_POST_MODE` precedence text, etc.

### grep for POST-reflect-gate tokens across `tests/`

```
grep -rniE 'reflect_post|POST_REFLECT_GATE|reflect_post_mode|--reflect|reflect run|superclaude reflect' tests/
→ (zero matches; exit 0 / no output)
```

**Confirmed: NO existing test exercises the POST reflect gate, `reflect_post`,
`POST_REFLECT_GATE`, `reflect_post_mode`, the wrapper string, or the emitted POST-item
shape.** This refactor is greenfield from a test standpoint — there is no regression
suite to keep green, only new assertions to (optionally) add.

## 2. `tests/audit/` fixture-based markdown-assertion pattern

Two distinct sub-patterns coexist in `tests/audit/` (75 test files). Both are viable
models; the second is the strong match for V1–V16 / MODE-MATCH.

### Pattern A — committed-fixture `.md` + Python re-impl of the gate rule + verdict matrix
`tests/audit/test_evidence_bound_tb_add_8.py` (290 lines):
- Reads **committed fixture `.md` files** from
  `tests/audit/fixtures/execution_context/{evidence_bound_bare_path,_file_line,
  _justified_absence}.md` (file:25-29). I read `evidence_bound_file_line.md` — it is a
  hand-frozen MDTM tasklist with a `## Execution Context` header + a per-item
  `**Context**:` bullet carrying a `file:line` citation (fixture lines 44-61).
- Re-implements the gate rule in Python (`tb_add_8(text)`, file:121-175) — regex-parses
  per-item Context paragraphs and returns PASS/FAIL.
- Asserts a **verdict matrix**: `bare=FAIL, file:line=PASS, absence=PASS`
  (`TestTBAdd8VerdictMatrixMatchesM1Baseline`, file:270-289).
- ALSO statically asserts the rule's source-of-truth wording survives in SKILL.md /
  rf-qa.md (the docstring pins `rf-qa.md:310`, `SKILL.md:1073`, `SKILL.md:1826`).

**This is the exact shape AT-VALIDATION-1 / AT-MISMATCH-1 want:** a fixture tasklist with
`reflect_post_mode: 1` whose POST item wrongly contains `superclaude reflect run` must
fail V6; a `mode: 2` fixture with inline `/sc:reflect` must fail V8; a `mode: 1` fixture
with `--remediate` must fail V9. You commit ~5-7 small fixture `.md` files under
`tests/audit/fixtures/reflect_post/` and a `validate_reflect_post(text)` Python re-impl
of the V1–V16 / MODE-MATCH assertions that returns the failing V# — then assert the
expected (mode, fixture) → V# matrix.

### Pattern B — pure static SKILL.md wording guards (no fixture)
Same file's `TestSkillInv012Documented` (test_synthetic_dnsp_dedup_not_regression.py:227-263)
and `test_evidence_bound_tb_add_8.py`'s static block: assert literal clauses survive in
the source markdown (`assert "contributes \`1\` (not \`2\`)" in skill_text`). This guards
against the spec text silently regressing.

### Pattern C — runtime emitter helper (overkill here)
`test_synthetic_dnsp_dedup_not_regression.py` imports a Python `_halt_emitter` helper
(`run_fix_cycle`, `CycleState`) via `sys.path.insert` (file:71-77) and drives a state
machine, comparing against canonical `.log` fixtures in `.dev/releases/complete/…`. This
models the *retry-loop runtime*, which the `--reflect` POST-gate refactor does NOT touch
(it emits a single penultimate item; there is no new loop). **Not needed for this refactor.**

**Infra notes:** `tests/audit/` has NO `conftest.py`; helpers are imported via
`sys.path.insert(0, str(Path(__file__).resolve().parent))`. Fixture `.md` files are
plain committed files under `tests/audit/fixtures/<topic>/` with an `__init__.py`.

## 3. Spec §13 AT matrix → testability classification

Source: `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md`
§13 (L931-957) + §9.1 V1–V16 (L716-739) + §9.3 MODE-MATCH (L752-771) + §9.4
AT-VALIDATION-1/AT-MISMATCH-1 (L776-786).

Classification key:
**(a)** mechanically testable via fixture+assert (Pattern A) or static-wording guard (Pattern B).
**(b)** testable only by manual / self-consistency walkthrough of the skill spec prose.
**(c)** requires the actual builder (an LLM-driven markdown emitter described in prose) to
RUN — there is NO Python entry point that emits a tasklist, so this is not a unit test.

| AT | What it asserts | Class | Realistic surface |
|----|-----------------|-------|-------------------|
| AT-FR1 (parse `none\|0\|1\|2\|auto`, `foo`→MALFORMED) | flag-token → mode `m` mapping | **(a)** Pattern A: a `parse_reflect_flag(tok)` Python re-impl mirrored from the spec's resolution table, asserting each token→m and `foo`→MALFORMED. Cheap & deterministic. | unit-testable |
| AT-FR2 (`--reflect none` suppresses item) | no POST item; `reflect_post:` absent; `reflect_post_mode: none` | **(a)** fixture `mode:none` tasklist + V3 assertion (0 items, key absent). | fixture-assert |
| AT-FR3 (Mode 1 inline emission shape) | `/sc:reflect --mode post --depth standard`, no `--remediate`/`superclaude reflect run`/Agent/Task; penultimate | **(a)** fixture `mode:1` + V5∧V6∧V9∧V4. Strong fixture match. | fixture-assert |
| AT-FR4 (Mode 2 wrapper emission, default) | Bash `superclaude reflect run {TASK_FILE}`, not Agent/Task; penultimate | **(a)** fixture `mode:2` + V7∧V8∧V4. | fixture-assert |
| AT-FR5 (`auto` determinism, Examples A/B/C) | two implementers agree on 3 worked examples; `auto-resolved-{1,2}` stamped | **(c)** for the "two implementers agree" framing (needs the LLM builder to run); **(a)** partial: if §11 gives the 3-term predicate explicitly, a Python re-impl of the predicate can assert Examples A/B/C resolve to the documented mode. The *human-agreement* clause is (b)/(c). | predicate (a); agreement (c) |
| AT-FR6 (old→new total map round-trip; `--reflect` wins) | each legacy cell → one `m` → one item | **(a)** Pattern A: a Python map of legacy alias → m, asserted exhaustive + `--reflect` precedence. | unit-testable |
| AT-FR7 (HALT + write-back) | non-`none` item Completion-gate has HALT + `reflect_post` write-back; no self-resolve | **(a)** fixture + V11∧V12 string assertions on the item body. | fixture-assert |
| AT-FR8 (`--remediate` scope) | Mode 1 no `--remediate`; Mode 2 completion-gate routes Tier-3 → Open Questions, no auto-exec | **(a)** for V9 (Mode-1 no `--remediate`, mechanical); **(b)** for "routes Tier-3 → Open Questions, no auto-exec" — that's prose behavior best checked by static-wording guard (Pattern B) + self-consistency. | partial (a)+(b) |
| AT-FR9 (single-producer / MODE-MATCH) | `reflect_post_mode` and item shape mutually consistent | **(a)** THE central fixture assertion (§9.3): read frontmatter mode, assert item Action shape matches per V-subset. This is the AT-VALIDATION-1/MISMATCH-1 engine. | fixture-assert (highest value) |
| AT-FR10 (wrapper-absent fallback) | `--reflect 2` + `W=false` → §6.4 manual-HALT + `reflect_post_mode: 2-degraded-halt` | **(a)** fixture `2-degraded-halt` + V15∧V16; **(b)** the *decision* to degrade depends on a runtime wrapper probe (W) — the fixture pins the post-degradation artifact, not the probe. | fixture-assert (artifact) + (c) for probe |
| AT-FR11 (Mode 1 nesting guard) | Mode-1 Verification has top-level precondition + nested-executor HALT (`mode1-nested-executor`) | **(b)** static-wording guard: assert the literal `mode1-nested-executor` HALT clause survives in SKILL.md/rf-qa. | static-wording (b) |
| AT-FR12 (`--spec` threading) | `--spec {SPEC_PATH}` present iff `spec_path` resolves | **(a)** two fixtures (spec set / unset) + V13. | fixture-assert |
| AT-FR13 (Fixed-1 advisory) | `--reflect 1` + (S6=1 ∨ S5>0) → build-log WARNING; item still Mode-1 | **(b)/(c)** the WARNING is emitted by the *builder at runtime* against computed signals; only the static rule wording is (a)/(b). | static-wording (b) + (c) |
| AT-AUTO-1 (3-term predicate determinism) | Examples A/B/C identical across implementers; INV-002 ladder for W=false | **(a)** if predicate is explicit: Python re-impl asserts A/B/C; **(c)** for cross-implementer agreement. | predicate (a) |
| AT-KNOB-1 (old→new equivalence) | `POST_REFLECT_GATE: DISABLED` ≡ `--reflect none` (no item, no key) | **(a)** two fixtures both yield V3 "no item / key absent" — assert structural equivalence. | fixture-assert |
| AT-DEPTH-1 (O4 depth preservation) | Mode 1 always `standard`; Mode 2 respects TCS floored at `standard`; no mode yields `quick` | **(a)** Mode-1 `--depth standard` literal is fixture-assertable (V5); **(b)** "Mode 2 respects TCS floored at standard / no `quick`" is partly a builder-runtime computation — static-wording guard on the floor rule + a "`--depth quick` never appears" negative grep across fixtures. | partial (a)+(b) |
| AT-WRAPPER-1 (wrapper detection) | probe exits 0 when `reflect` subcommand registered; non-zero when absent | **(a)** but this is the SIBLING CLI's surface, not this markdown refactor. A `superclaude reflect --help`/registration probe test belongs with the wrapper implementation, not the skill-spec PR. Out of scope for THIS track's tests. | (a) but sibling-owned |
| AT-FALLBACK-1 (unified INV-002 ladder) | resolved Mode 2 + W=false → `*-degraded-halt`; resolved Mode 1 + W=false → Mode 1 | **(a)** fixtures for both degraded outcomes (V15/V16 + mode marker); **(c)** the W=false branch decision is runtime. | fixture-assert (artifacts) |
| AT-VALIDATION-1 (mode/item mismatch) | `mode:1`+wrapper→V6; `mode:2`+inline→V8; `mode:1`+`--remediate`→V9 | **(a) STRONGEST FIXTURE MATCH.** Exactly Pattern A: 3 malformed fixtures + `validate_reflect_post()` returns the expected failing V#. | fixture-assert (highest value) |
| AT-MISMATCH-1 (MALFORMED on swap) | swapped Mode-1/Mode-2 templates fail with specific V# (V6 or V8) | **(a)** same engine as AT-VALIDATION-1 (a swapped fixture). | fixture-assert |
| AT-PLUMBING-1 (precedence + defaults) | `--reflect` > `REFLECT_POST_MODE` field > legacy alias map > default 2 | **(a)** Python re-impl of the resolution function, parametrized over precedence combinations. | unit-testable |

**Summary of distribution:** Of 22 ATs — roughly **13 have a clean mechanical (a) surface**
(parse/precedence re-impls + frontmatter-mode→item-shape fixtures: AT-FR1/2/3/4/6/7/9/12,
AT-KNOB-1, AT-VALIDATION-1, AT-MISMATCH-1, AT-PLUMBING-1, predicate-half of AT-FR5/AUTO-1);
**~5 are static-wording-guard / self-consistency (b)** (AT-FR8 routing, AT-FR11, AT-FR13,
AT-DEPTH-1 floor, parts of FR10/FALLBACK); **~2-3 have a (c) runtime-builder core** that no
unit test can reach (cross-implementer agreement in FR5/AUTO-1, the live wrapper-probe
decision W, AT-WRAPPER-1 which is sibling-owned anyway).

**Crucial realism caveat:** Even the "(a)" fixture tests do NOT test the builder. They test
a **Python re-implementation of the V1–V16 validation rule** applied to **hand-frozen
fixture tasklists**. They prove "IF the builder emits this shape, the validator verdict is
X" — they do NOT prove the builder actually emits that shape (that is the (c) gap, the same
gap that exists for ALL of `tests/skills/` and `tests/audit/` today). This is acceptable
and is exactly how the existing TB-Add-8 / DNSP suites work: the value is regression-locking
the documented rule + the canonical good/bad shapes, not end-to-end builder execution.

## 4. Gate / verification commands (quoted)

`Makefile`:
- `lint: lint-architecture` then `uv run ruff check .` (L48-50). **`ruff check` does NOT
  lint `.md`** — it only lints Python. So `make lint` does nothing for a pure SKILL.md /
  rf-qa.md edit except the architecture policy checks in `lint-architecture` (bidirectional
  command↔skill links, command size limits, skill frontmatter completeness). task-builder
  is a plain skill (not an `sc-*-protocol` command-paired skill), so most lint-architecture
  checks don't touch it.
- `format: uv run ruff format .` (L53-55) — Python only.
- `test: uv run pytest` (L13-15) — full suite; `tests/audit/` + `tests/skills/` run here.
- `verify-sync` (L166+) — `diff -rq` between `src/superclaude/{skills,agents,commands}` and
  `.claude/` mirrors; exits 1 on drift. **This is the load-bearing gate for this refactor:**
  any SKILL.md/rf-qa.md edit must be followed by `make sync-dev` or verify-sync fails CI.

CI (`.github/workflows/`):
- `quick-check.yml`: `pytest tests/unit/ -v --tb=short -x` (L33) — **unit only**;
  `ruff check src/ tests/` (L37); `ruff format --check src/ tests/` (L41);
  `make verify-sync` (L49); `make lint-architecture` (L53). **Note: quick-check runs ONLY
  `tests/unit/`, so a new test under `tests/skills/` or `tests/audit/` runs in `test.yml`,
  NOT in quick-check.**
- `test.yml`: full `pytest -v --tb=short` (L56) + `pytest --cov` (L61) + `ruff check`/`ruff
  format --check` (L96-100). **This is where `tests/skills/` + `tests/audit/` reflect tests
  would execute.**

Pre-commit (`.pre-commit-config.yaml`):
- `markdownlint` v0.38.0 with `--fix` (L71-75) — **but `exclude:` matches `\.dev/.*`
  (L81)**. So the SPEC in `.dev/brainstorms/…` is NOT markdownlinted, but the edited
  `src/superclaude/skills/task-builder/SKILL.md` and `src/superclaude/agents/rf-qa.md`
  ARE markdownlinted on commit. The refactor must keep those two files markdownlint-clean
  (the existing recurring discipline — never pivot to mdformat/sed to escape; re-edit).
- `yamllint`, `shellcheck`, and the `block-claude-generated-mirrors` local hook (L102-107)
  which rejects staging `.claude/` mirrors.

**Realistic CI surface for THIS docs/skill change:** (1) markdownlint on the two edited
`src/` markdown files at commit time; (2) `make verify-sync` (src↔.claude parity) — the
single highest-probability failure if `make sync-dev` is forgotten; (3) `ruff
check/format` only if any `.py` test file is added; (4) full `pytest` in `test.yml` if any
new test is added. A pure prose edit with no new test only meaningfully hits markdownlint +
verify-sync.

## 5. Recommendation

### TESTING_REQUIREMENTS value: **UNIT (small, fixture-based) — but SCOPED, not exhaustive**

Rationale:
- The repo has a **strong, in-repo precedent** for exactly this kind of test:
  `tests/skills/test_task_builder_merge.py` (content-marker assertions) and
  `tests/audit/test_evidence_bound_tb_add_8.py` (fixture `.md` + Python rule re-impl +
  verdict matrix). The `--reflect` refactor is the *same class of change* (it edits the
  same SKILL.md + rf-qa.md and adds a structured V1–V16 validation contract). Declaring
  NONE would break parity with how every prior task-builder landing (TB-Add-1..8, DNSP,
  monotonicity) was regression-locked.
- A **clean assertion surface exists** for the highest-value ATs (AT-VALIDATION-1,
  AT-MISMATCH-1, AT-FR9/MODE-MATCH, AT-FR1/FR6/PLUMBING precedence). These are deterministic
  Python, no LLM, no flakiness.
- BUT the builder-runtime ATs (cross-implementer `auto` agreement, live wrapper probe,
  build-log WARNING emission) are **(c)-class and NOT worth faking** with a unit test — they
  are correctly verified by self-consistency walkthrough + the sibling CLI's own tests.

### Concrete VERIFICATION approach (in priority order)

1. **MANDATORY, zero-cost:** `make sync-dev` then `make verify-sync` (src↔.claude parity) +
   markdownlint-clean on the two edited `src/` files. These are the gates that actually
   gate CI for a prose edit. Put a verification item for each.
2. **MANDATORY self-consistency item (the cheapest high-value check):** a single task item
   that walks the §9.1 V1–V16 table against the §9.2 per-mode active-assertion map against
   the §13 AT matrix against the EMITTED Mode-1/Mode-2/none/degraded templates in the
   edited SKILL.md — confirming every V# referenced in §9.2/§9.3 is defined in §9.1, every
   AT in §13 traces to a V# or a documented prose rule, and the literal wire strings
   (`superclaude reflect run {TASK_FILE}`, `/sc:reflect --mode post --depth standard`,
   `reflect_post_mode` value set) are byte-consistent across SKILL.md ↔ rf-qa.md ↔ §13. This
   is the same internal-consistency discipline the memory note `feedback_sc_reflect_vs_inline_rfqa`
   describes (spec-LITERAL enum tokens + invariant arithmetic), and it is what catches the
   real bugs in a prose refactor (enum drift, a V# named but undefined, a wire string that
   differs by one token between the two files).
3. **RECOMMENDED, bounded automated surface (model on `test_evidence_bound_tb_add_8.py`):**
   add ONE test file `tests/audit/test_reflect_post_mode_match.py` (or a `TestReflectPostGate`
   class appended to `tests/skills/test_task_builder_merge.py`) that:
   - Commits ~5-7 frozen fixture tasklists under `tests/audit/fixtures/reflect_post/`:
     `mode1_inline_ok.md`, `mode2_wrapper_ok.md`, `none_suppressed.md`,
     `mode1_with_wrapper_BAD.md` (must fail V6), `mode2_with_inline_BAD.md` (must fail V8),
     `mode1_with_remediate_BAD.md` (must fail V9), `degraded_halt.md` (V15/V16).
   - Implements `validate_reflect_post(text) -> list[(item, failing_V#)]` as a Python
     re-impl of the §9.3 MODE-MATCH / §9.1 V-subset rule (reads frontmatter
     `reflect_post_mode`, asserts the penultimate item Action shape).
   - Asserts the (fixture, mode) → expected-V# matrix (directly satisfies AT-VALIDATION-1
     + AT-MISMATCH-1, and exercises AT-FR2/3/4/9).
   - PLUS static-wording guards (Pattern B) that the new SKILL.md/rf-qa.md retain the
     load-bearing literals (`superclaude reflect run`, `reflect_post_mode`, the V1–V16 table
     header, `mode1-nested-executor`, `2-degraded-halt`) — covering AT-FR11/FR13 wording and
     regression-locking the spec text.
   - OPTIONALLY a tiny `parse_reflect_flag()` / `resolve_reflect_mode()` re-impl test for
     AT-FR1/FR6/PLUMBING precedence (pure, deterministic).

### Is full automated coverage worth it here? — NO; targeted is right.
Attempting to mechanically test ALL 22 ATs is **overkill and partly impossible**: ~7-8 ATs
have a (b)/(c) builder-runtime core with no Python entry point (the builder is an
LLM-driven markdown emitter described in prose — there is literally no `build_tasklist()`
function to call). Faking those with mock fixtures tests the fixture, not the builder, and
adds maintenance drag. The **right cost/value cut** is: verify-sync + markdownlint
(free) + ONE self-consistency walkthrough item (catches the real prose-refactor bugs) +
ONE bounded fixture-based pytest covering the deterministic core (AT-VALIDATION-1,
AT-MISMATCH-1, MODE-MATCH, parse/precedence). That mirrors precisely how TB-Add-8 and DNSP
were verified and keeps the suite honest about the (c) gap rather than papering over it.

**One-line BUILD_REQUEST steer:** `TESTING_REQUIREMENTS: UNIT` — scoped to a single
fixture-based `tests/audit/`-style file (AT-VALIDATION-1/AT-MISMATCH-1/MODE-MATCH +
parse/precedence) plus static-wording guards; primary verification is `make verify-sync` +
markdownlint + a §9/§13 self-consistency walkthrough item. Do NOT attempt end-to-end
builder execution tests (no Python entry point exists; that surface is (c)).

---

**Status: Complete**

## Summary

- **No existing test touches the POST reflect gate** (grep for
  `reflect_post|POST_REFLECT_GATE|reflect_post_mode|--reflect|superclaude reflect` across
  `tests/` = zero hits). Greenfield: no regression suite to preserve, only new assertions.
- **The repo already has the exact test pattern this refactor needs.**
  `tests/skills/test_task_builder_merge.py` = content-marker string assertions over the
  src/ SKILL.md + rf-*.md (no CliRunner, no subprocess). `tests/audit/test_evidence_bound_tb_add_8.py`
  = committed fixture `.md` files + a Python re-impl of the gate rule + a verdict matrix —
  a 1:1 model for AT-VALIDATION-1 / AT-MISMATCH-1 / MODE-MATCH ("mode:1 + wrapper string →
  fail V6", etc.).
- **§13 AT classification:** ~13 of 22 ATs have a clean mechanical (a) surface
  (parse/precedence re-impls + frontmatter-mode→item-shape fixtures); ~5 are static-wording
  / self-consistency (b); ~3 have a (c) builder-RUNTIME core no unit test can reach
  (cross-implementer `auto` agreement, live wrapper probe, build-log WARNING). AT-WRAPPER-1
  is the sibling CLI's surface, not this markdown track's.
- **Critical realism caveat:** even the (a) tests verify a *Python re-impl of the V1–V16
  rule against hand-frozen fixtures*, NOT the LLM builder (no `build_tasklist()` entry
  point exists). Same (c) gap as every existing task-builder test — acceptable, and the
  honest framing.
- **Gates that actually fire for a SKILL.md/rf-qa.md edit:** markdownlint pre-commit on the
  two `src/` files (`.dev/` spec is excluded), `make verify-sync` (src↔.claude parity — the
  most likely failure if `make sync-dev` is skipped), full `pytest` in `test.yml` (NOT
  quick-check, which is `tests/unit/`-only). `make lint`/`ruff` do nothing for pure markdown.
- **RECOMMENDATION — `TESTING_REQUIREMENTS: UNIT`, scoped:** (1) mandatory `make verify-sync`
  + markdownlint-clean items; (2) one mandatory §9/§13 self-consistency walkthrough item
  (V-table ↔ active-assertion map ↔ AT matrix ↔ emitted templates; byte-consistent wire
  strings across both files) — this catches the real prose-refactor bugs (enum drift,
  undefined-but-referenced V#, wire-string skew); (3) ONE bounded fixture-based pytest
  modeled on `test_evidence_bound_tb_add_8.py` covering the deterministic core
  (AT-VALIDATION-1, AT-MISMATCH-1, MODE-MATCH, parse/precedence) + static-wording guards.
  Full automated coverage of all 22 ATs is OVERKILL and partly impossible (the (c) builder
  surface has no Python entry point); targeted fixture+self-consistency is the right cut and
  matches how TB-Add-8 / DNSP were verified.

Research file: `.dev/tasks/to-do/TASK-RF-20260608-194013/research/06-test-verification-surface.md`
