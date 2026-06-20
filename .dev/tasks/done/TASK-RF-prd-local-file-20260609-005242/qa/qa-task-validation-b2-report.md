# ADVERSARIAL QA — B2 Self-Containment Lens

**Target task file:** `.dev/tasks/to-do/TASK-RF-prd-local-file-20260609-005242/TASK-RF-prd-local-file-20260609-005242.md`
**Template:** 02 (MDTM Complex Task)
**Research dir:** `.dev/tasks/to-do/TASK-RF-prd-local-file-20260609-005242/research/`
**Lens:** B2 — every checklist item must be self-contained (Context + Action + Output + Verification + Completion gate); paths specific; verification measurable; one-edit granularity; no items on unverified findings; the prompts.py item carries the `Path(p).is_file()` guard + preserve-substrings; constant-deletion gated on a grep-confirm-zero item.
**Stance:** ADVERSARIAL — assume defects exist; find at least 3. Read-only; report-only.
**Date:** 2026-06-09

---

## Method

- Read the full task file (348 lines) and enumerated every actionable checklist item (`- [ ]`).
- Ground-checked the load-bearing anchors against the LIVE source (`src/superclaude/cli/prd/prompts.py`) and against research 01/02/04.
- Scored each item against the five B2 components and the eight lens sub-checks.

**Anchor grounding (live verification performed this session):**
- `prompts.py:120` `def _authoritative_specs_block(` — CONFIRMED.
- `prompts.py:130` `if not spec_paths:` — CONFIRMED.
- `prompts.py:134-135` substrings `AUTHORITATIVE SPECIFICATIONS` + `You MUST Read each one IN FULL` — CONFIRMED present verbatim.
- `prompts.py:34` `_TRUNCATION_MARKER`, `:42` `_read_file`, call sites `:247` / `:919` — CONFIRMED.
- Research 04 Decision 1 (mandatory `is_file()` guard) — CONFIRMED as a hard builder requirement.

So the task's factual substrate is sound; the B2 findings below are about *item-level self-containment*, not bad source facts.

---

## Item inventory (actionable `- [ ]`)

| ID | Phase / Step | One-line |
|----|--------------|----------|
| I-1.1 | 1.1 | Set status Doing + start_date + log |
| I-1.2 | 1.2 | Create phase-outputs subdirs |
| I-1.3 | 1.3 | Capture start_commit + baseline pytest |
| I-1.4 | 1.4 | Re-verify anchors (drift guard) |
| I-2.1 | 2.1 | Pre-deletion grep — 3 constants dead |
| I-2.2 | 2.2 | Remove refs `--file` branch |
| I-2.3 | 2.3 | Remove `--spec` `--file` branch |
| I-2.4 | 2.4 | Remove `_build_file_args` + `__init__` wiring |
| I-2.5 | 2.5 | Delete 3 dead constants (gated on I-2.1) |
| I-2.6 | 2.6 | Update `--file` docstrings |
| I-3.1 | 3.1 | Upgrade `_authoritative_specs_block` w/ `is_file()` guard |
| I-3.2 | 3.2 | Update stale "Phase 1 (paths-only)" docstring line |
| I-4.1 | 4.1 | Invert/replace `TestSpecFileAttach` |
| I-4.2 | 4.2 | Add content/truncation/missing/empty tests |
| I-5.1 | 5.1 | Acceptance grep |
| I-5.2 | 5.2 | PRD pytest subset |
| I-5.3 | 5.3 | sync-dev / verify-sync drift guard |
| I-5.4 | 5.4 | Git-scope confirmation |
| I-6.1 | 6.1 | Aggregate phase outputs |
| I-6.2..6.7 | 6.2–6.7 | QA lens agents + consolidate + fix + verify |
| I-PC.1..PC.5 | Post-Completion | Output-existence, final-state, summary, reflect gate, Done-flip |

---

## Lens sub-check results

### (7) prompts.py item carries `is_file()` guard + preserve-substrings — **PASS**

I-3.1 is exemplary. It explicitly: (a) names `Path(p).is_file()` as the per-path guard and calls it MANDATORY for EVERY path; (b) carries the rationale from research 04 Decision 1 verbatim (unguarded `_read_file` → bare `FileNotFoundError` inside `build_scope_discovery_prompt`, caught only as `MissingArtifactError` → resume crash); (c) requires the leading `\n\n` and the substrings `AUTHORITATIVE SPECIFICATIONS` and `MUST Read each one IN FULL` to survive; (d) preserves the `return ""` empty-input contract; (e) forbids re-implementing truncation. All five B2 components present. Verified against live `prompts.py:134-135` — substrings exist verbatim. No defect.

### (8) constant-deletion gated on grep-confirm-zero — **PASS**

I-2.5 reads the I-2.1 grep report and deletes ONLY constants verdicted `CONFIRMED-DEAD`; any `HAS-EXTERNAL-REF` constant is left in place and recorded. I-2.1 produces that gate (`phase2-deadconst-grep.md`) and additionally cross-checks prompts.py literal-name inlining (Decision 3). The gate dependency is explicit and directional. No defect.

### (3) file paths specific — **PASS (strong)**

Every edit item names the real file and the research-cited line anchors (e.g. `process.py:199`/`:204`, `:169-170`, `:166`, `:95`/`:115`/`:121`; `prompts.py:120-138`, `:34`, `:42`, `:247`/`:919`). No "the relevant file" placeholders anywhere. These match live source.

### (4) verification measurable — **MOSTLY PASS**, one soft spot (see L-3).

### (6) no items on unverified findings — **PASS** (I-2.5 is the only finding-dependent delete and it is gated; I-1.4 re-verifies anchors before Phase 2/3 edits).

### (5) one-edit granularity — **FAIL on two items** (see H-1, H-2).

### (1)/(2) all-5-components / no-reliance-on-prior-context-without-restating — **FAIL on I-2.5 context dependency framing** + minor (see M-1, L-1).

---

## FINDINGS (severity-rated)

### H-1 — HIGH — I-3.1 batches FOUR distinct edits into one item (one-edit granularity, B2 sub-check 5)

I-3.1 ("Upgrade `_authoritative_specs_block`") instructs the executor, in a single checklist item, to make four logically separable changes to the function body:
1. preserve the `if not spec_paths: return ""` guard,
2. add the per-path `Path(p).is_file()` branch with `_read_file` content inlining + per-spec header,
3. add the missing-path fall-back path-only line,
4. preserve/re-emit the header substrings + leading `\n\n`.

While these all touch one function and a single coherent rewrite is defensible, the B2 lens requires "one edit per item, no batch items." This item is the highest-risk edit in the task (it is THE fix), yet it carries no internal sub-gates: a partial implementation (e.g. guard added but truncation path silently re-implemented, or header substring dropped during the rewrite) would still let the executor mark the single checkbox complete. The verification clause is present but is a conjunction of ~6 conditions checked once at the end. **Impact:** the riskiest change has the coarsest granularity in the task. **Recommendation:** either split into 3.1a (add guarded inline branch) / 3.1b (add missing-path fallback) / 3.1c (assert substrings+leading-newline preserved), OR keep as one item but add an explicit post-edit self-verification sub-step (grep the function for `is_file(`, `_read_file(`, `AUTHORITATIVE SPECIFICATIONS`) before marking complete.

### H-2 — HIGH — I-4.1 batches a rewrite + two inversions + three deletions into one item

I-4.1 ("Invert/replace `TestSpecFileAttach`") bundles: (a) rewrite the banner comment, (b) invert `test_scope_discovery_attaches_each_spec`, (c) invert `test_investigation_numbered_step_attaches_specs`, (d) DELETE three `== []` tests that name the removed `_build_file_args`, and (e) conditionally remove the `_spec_config` helper. That is five separable test-file edits across two semantically different operations (invert-to-assert-absence vs delete-dead-symbol-references) in one checkbox. The verification ("contains NO reference to `_build_file_args`, asserts NO `--file`...") is a multi-condition conjunction validated once. **Impact:** a partial inversion (e.g. the executor inverts the two asserting tests but forgets to delete one of the three `_build_file_args`-referencing tests) yields an `AttributeError` at collection time that I-5.2 would catch — but the granularity violation means the test-authoring item has no internal checkpoint. **Recommendation:** split into 4.1a (rewrite banner + invert the two asserting tests) and 4.1b (delete the three `_build_file_args`-referencing tests + prune helper).

### M-1 — MEDIUM — I-2.4 (Action — bundles method deletion + call-site deletion + `__init__` kwarg removal across non-adjacent code regions)

I-2.4 deletes (a) the entire `_build_file_args` method body at `:169-206`, (b) the `file_args = self._build_file_args(...)` call + comment at `:154-155`, and (c) the `extra_args=file_args` kwarg inside `super().__init__(...)` at `:166`. These are three edits in three non-contiguous regions of the file. Unlike I-3.1 (one function) these are physically separate code sites, so the "one edit per item" violation is sharper. The item's verification is sound (constructor still passes all other args, no `extra_args` remains), but if the executor removes the kwarg and the call but leaves a now-orphaned method, or vice-versa, only the downstream pytest/import in Phase 5 catches it. **Impact:** medium — Phase 5 import/pytest is a backstop, but the item itself lacks a self-contained "module still imports" gate. **Recommendation:** add `python -c "import ..."` (UV form) self-check to the item's completion gate, or split call-site removal from method-shell removal.

### M-2 — MEDIUM — I-2.5 relies on I-2.1's report context without restating the dead-determination criteria (B2 sub-check 2)

I-2.5's gate is "read the Step 2.1 grep report ... confirm each ... was verdicted CONFIRMED-DEAD." This is correct gating (sub-check 8 PASS), but the item does NOT restate WHAT makes a constant dead — it defers entirely to the verdict string written by a prior item. If I-2.1 mis-verdicts (e.g. counts a docstring mention as a live reference, or vice-versa), I-2.5 propagates the error with no independent restatement of the criterion ("zero references outside the now-removed `_build_file_args` body"). The B2 self-containment principle wants each item to carry enough context to be checked in isolation; here the deletion item's correctness is fully parasitic on a string in another file. **Impact:** medium — the gate exists but is not self-validating. **Recommendation:** restate the dead criterion inline ("delete iff the only matches in the I-2.1 report fall within the line range of the removed `_build_file_args`, i.e. former `:169-206`").

### M-3 — MEDIUM — I-2.2/I-2.3 "syntactically valid Python" verification is not independently measurable within the item

I-2.2 and I-2.3 each end with "ensuring ... the surrounding method remains syntactically valid Python (no dangling `for`/`if`)." After I-2.2 deletes Branch A but before I-2.3 removes Branch B, the method is in a transient half-edited state, yet the item asks the executor to certify "syntactically valid Python" with no command to prove it (no `python -m py_compile` / import). The verification is an assertion, not a measurement. Across the Phase 2 sequence the first executable proof of validity is I-5.2 (pytest) — four items later. **Impact:** medium — a syntax break introduced in I-2.2 is not caught until Phase 5. **Recommendation:** make the per-item gate measurable, e.g. append a read-only `uv run python -c "import ast,sys; ast.parse(open('src/superclaude/cli/prd/process.py').read())"` check to each Phase 2 edit item.

### L-1 — LOW — Phase 2/3/4 edit items inherit "correct drift first" context from the phase preamble, not the item body (B2 sub-check 2)

The instruction to "use the Phase 1 anchor-reverify report ... to correct any drifted line numbers before each edit" lives ONLY in the Phase 2 parenthetical preamble (line 169) and the Phase 3 preamble (line 199), not inside each edit item. An executor processing items in isolation (the B2 ideal) could act on the research-cited line numbers (`:199`, `:204`, etc.) without consulting the drift report, because no individual edit item re-states "consult phase1-anchor-reverify.md first." The anchors happen to be live-correct today (verified this session), so the practical risk is low, but the self-containment principle is violated: the drift-correction context is phase-scoped, not item-scoped. **Impact:** low (anchors currently hold). **Recommendation:** add "(line numbers per `phase1-anchor-reverify.md`; correct for drift)" to each Phase 2/3 edit item's Context clause.

### L-2 — LOW — I-2.6 verification "no remaining docstring text advertises `--file`" is not gated by a grep within the item

I-2.6 updates three `--file`-advertising docstring locations (module `:4`, GAP-003 line `:11`, class bullet `:133`). Its completion gate is a human-judgment assertion ("no remaining docstring text advertises `--file` arg construction/scoping"). The task already owns a perfect measurable instrument for this — the I-5.1 acceptance grep `grep -rn '"--file"'` — but that grep matches the quoted token `"--file"` (the code literal), NOT the bare-word `--file` appearing in prose docstrings. So a stale docstring saying "phase-aware --file scoping" would NOT be caught by I-5.1 and is NOT independently verified inside I-2.6 either. **Impact:** low (cosmetic — stale docstring, not a functional bug). **Recommendation:** add an item-local `grep -n -- '--file' src/superclaude/cli/prd/process.py` (bare-word) check to I-2.6's gate so the prose-docstring removal is measurable.

### L-3 — LOW — I-5.3 verification clause is internally self-contradicting on what "drift" means

I-5.3 says verify-sync "reports clean regardless" for a cli-only change, AND simultaneously instructs "IF `verify-sync` reports drift ... it MUST NOT be caused by the cli-only edits ... reconciled before marking complete." Because the item also permits "log the blocker ... then mark this item complete" on failure, the completion gate is ambiguous: a real drift both "must be reconciled before marking complete" and "may be logged then marked complete." **Impact:** low (drift is genuinely a no-op for cli-only edits, so the contradiction is unlikely to fire). **Recommendation:** pick one disposition — for a pre-existing/unrelated drift, "log + proceed"; reserve "must reconcile" only for drift in a file this task touched.

### L-4 — LOW — I-1.3 packs three actions (capture SHA + write frontmatter + baseline pytest + two output files) in one item

I-1.3 captures `git rev-parse HEAD`, writes it to frontmatter `start_commit:`, runs baseline pytest, and writes two artifacts. This is a setup item so the batching is lower-stakes than the H findings, but it is still multi-action under one checkbox. Noted for completeness; not independently severity-bearing beyond the H-1/H-2/M-1 granularity theme.

---

## Positive observations (defensible design, not defects)

- **B2 5-component coverage is otherwise strong.** Almost every item has Context (file:line anchors), Action (verb + target), Output (a named `phase-outputs/...md` artifact or a frontmatter mutation), Verification ("ensuring ..."), and a Completion gate ("mark this item complete"). The template's "ensuring ..." idiom is applied consistently.
- **Anti-fabrication clauses are present** ("derived from actual grep hits (not assumed)", "the captured SHA is the real `git rev-parse HEAD` output (not fabricated)").
- **Sub-checks 3, 6, 7, 8 PASS** — paths specific, no ungated finding-dependent action, the prompts.py `is_file()`+substrings item is fully self-contained, and constant deletion is correctly gated.
- **Out-of-scope guards are restated per-item** (`tests/pipeline/test_process.py:78-81` left untouched).

---

## Severity roll-up

| Severity | Count | Item IDs |
|----------|-------|----------|
| HIGH     | 2     | H-1 (I-3.1), H-2 (I-4.1) |
| MEDIUM   | 3     | M-1 (I-2.4), M-2 (I-2.5), M-3 (I-2.2/I-2.3) |
| LOW      | 4     | L-1 (Phase 2/3 edit items), L-2 (I-2.6), L-3 (I-5.3), L-4 (I-1.3) |

The dominant theme is **one-edit granularity (B2 sub-check 5)**: the two riskiest items in the task (the core prompts.py upgrade I-3.1 and the test inversion I-4.1) are the most heavily batched, and several edit items assert "syntactically valid Python" without a measurable in-item proof, deferring all real validation to the Phase 5 pytest backstop.

None of the findings are correctness-fatal: the underlying source facts, anchors, the mandatory `is_file()` guard, the preserve-substrings, and the dead-constant grep gate are all present and correct. But the H/M granularity defects mean a partially-completed risky edit can be marked complete without an in-item gate catching it, which is precisely what the B2 self-containment lens exists to prevent.

---

## VERDICT: FAIL

Two HIGH-severity B2 self-containment defects (H-1 / I-3.1 and H-2 / I-4.1 — the two riskiest edits are over-batched with no internal gate), plus three MEDIUM (M-1 / I-2.4, M-2 / I-2.5, M-3 / I-2.2+I-2.3) and four LOW. Lens sub-checks (7) is_file()+substrings and (8) gated constant-deletion both PASS; the failure is concentrated in sub-check (5) one-edit granularity and sub-check (2) item-isolated context for I-2.5 and the Phase-2/3 drift-correction context.

**Remediation to reach PASS:** split I-3.1 and I-4.1 (or add in-item self-verification sub-gates), add a measurable per-item `py_compile`/import check to the Phase 2 edit items, restate the dead-constant criterion inline in I-2.5, and resolve the I-5.3 drift-disposition contradiction.
