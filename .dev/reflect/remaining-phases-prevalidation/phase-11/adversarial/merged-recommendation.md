# Phase 11 (R1.6 Cleanup) — Merged Adversarial Recommendation

<!-- Provenance: sc-adversarial-protocol Mode B (inline), merge of KEEP/REFACTOR/DISCARD advocates -->
<!-- Convergence: 0.88 (BLOCKED by 3 HIGH UNADDRESSED invariants until REFACTORs applied) -->

## Verdict summary

| Step | Verdict | One-line reason |
|---|---|---|
| 11.1 | REFACTOR | Inventory omits the CORRECTED CI-vs-runtime code_assertion split + spec_id_registry.json target |
| 11.2 | REFACTOR | Direction correct (envelope-owned parser) but targets phantom `envelope.frontmatter` field |
| 11.3 | KEEP | Correctly deletes genuine `_cross_refs_resolve` stub; honors VALID-HEURISTIC; does NOT touch the shim |
| 11.4 | REFACTOR | Genuine fail-open deletions correct; fix line 2167→2579; absorb shim-comment correction |
| 11.5 | REFACTOR | `test_no_fragility_stubs` KEEP; `test_gate_empty_target` must be shim-aware |
| 11.6 | KEEP | Contract #7 retry-mutation invariant; framing-independent |
| 11.7 | REFACTOR | Whole-codebase `gate=None`-must-be-0 grep unsatisfiable; scope to roadmap `_build_steps` |
| PG11.1 | REFACTOR | QA item (d) `contracts.parsers` contradicts 11.2; add CORRECTED-scope checks |
| PG11.2 | KEEP | Sound act-on-verdict loop (conditional on PG11.1 refactor) |

## The framing-correction items (the load-bearing finding)

The session's audit warned Phase 11 might carry the wrong "blanket-delete the shim AND plumb envelope so
the code_assertion fires at runtime" framing. **Good news (INV-001): no executable Phase 11 step mandates
deleting the `gate_passed` envelope-None shim.** 11.3 deletes `_cross_refs_resolve`; 11.4 deletes the
fidelity fail-opens + the convergence `gate=None`; 11.7 greps for `gate=None` and annotated `return True`.
None of these name `cli/pipeline/gates.py:93-98`. The genuine fail-open stubs and the legitimate CI-only
shim are NOT conflated in the deletion steps.

**Bad news:** the wrong framing survives in three quieter forms, all HIGH severity:

1. **OMISSION (INV-002):** the CORRECTED High-priority R1.6 deliverable — *split `code_assertions` into
   CI-only (source-tree/AST, e.g. `assert_step_reachable`) vs runtime (artifact checks, e.g.
   `assert_envelope_artifacts_present` + the R1.5 verify-implementation FR→AST checks), fire only the
   runtime kind in the live gate path, and replace the envelope-None shim with explicit per-assertion
   classification* — appears in **no** Phase 11 step. Phase 11 would close without doing the one thing
   the r1-3 audit re-scoped it to do.

2. **In-code wrong-framing comment:** `cli/pipeline/gates.py:39` and `:97` literally instruct
   "R1.6 cleanup deletes this skip-path / R1.6 deletes this branch when all call sites are migrated."
   A cleanup agent acting on 11.7's "tidy the codebase" spirit could delete the branch on the comment's
   authority. The comment must be **rewritten** to state the corrected intent (shim is correct for
   CI-only assertions; replaced by explicit classification, not deleted).

3. **QA criterion contradiction (INV-005):** PG11.1(d) demands "ONE canonical parser exported from
   `superclaude.contracts.parsers`" — a stale framing that contradicts 11.2 (envelope-owned, no
   `contracts.parsers` submodule). This same stale `contracts.parsers` model also appears in Phase 13
   Step 13.3 and the final-acceptance file list (L747) — a **systemic cross-phase contradiction**, flagged
   here for Phase 11 scope and referred to Phase 13 validation.

## Proposed replacement text (REFACTOR items)

### 11.1 — add to the inventory enumeration
> (f) **CORRECTED R1.6 code_assertion split (A3/L1044):** classify each `code_assertions.py` predicate as
> **CI-only** (`assert_step_reachable` — AST-parses `repo_root/src/...`, fail-closed, cannot run in a
> pipx-installed package) or **runtime-safe** (`assert_envelope_artifacts_present`, R1.5 verify-implementation
> FR→AST checks — operate on the run's own artifacts). Record that the `gate_passed` envelope-None shim
> (`cli/pipeline/gates.py:93-98`) is **PRESERVED, not deleted** — its role is reclassified, not removed.
> (g) `spec_id_registry.json` dual-write deletion (`envelope.py:148-150` TODO) once gate logic reads
> `envelope.spec_ids` directly.

### 11.2 — fix the consumer-migration mechanism
> Replace every occurrence of "`envelope.frontmatter` (the typed field on PipelineEnvelope)" with the
> actual typed fields the envelope exposes (`envelope.counts`, `envelope.findings`, `envelope.spec_ids`)
> OR, if a generic frontmatter dict is genuinely needed, **first add a `frontmatter: dict` field to
> `PipelineEnvelope` and its post-extractors** as an explicit sub-step (it does not exist today —
> `envelope.py:128-175`). Keep the canonicalization direction (envelope module owns the single extractor;
> delete both `gates.py:_parse_frontmatter` and `_check_frontmatter`). Add a note that task objective 10
> (L99 "canonicalize on `_check_frontmatter`") is **superseded** by this remediation.

### 11.4 — line fix + shim-comment ownership
> Correct the bypass location to **executor.py:2579** (was 2167). ADD: "Rewrite the wrong-framing comment
> at `cli/pipeline/gates.py:39` and `:97` to state the CORRECTED intent — the envelope-None branch is the
> correct behavior for CI-only/source-tree code_assertions and is replaced by an explicit per-assertion
> CI-only-vs-runtime classification, NOT deleted. Implement that classification + fire only runtime-safe
> assertions in the live gate path (A3/L1044)." Cross-reference the Phase-10 sequencing prerequisite (L603).

### 11.5 — `test_gate_empty_target` shim-awareness
> For gates whose enforcement includes `code_assertions`, the empty-target test MUST pass a valid
> `envelope`+`repo_root` (so the assertion actually fires) OR explicitly scope the NOT-PASS assertion to the
> file-exists / min-lines / semantic tiers and document that code_assertions are covered by their dedicated
> tests (`test_dispatch_reachability.py`, `test_verify_implementation.py`). As written, a code-assertion-only
> gate called without an envelope hits the shim and returns PASS, making the test either spuriously fail a
> correct gate or silently mask the shim.

### 11.7 — scope the gate=None grep
> Replace "full-codebase grep for `gate=None` (must be 0)" with "grep roadmap `_build_steps` for the
> convergence-bypass pattern `gate=None if config.convergence_enabled` (must be 0)." A legitimate
> `gate=None` exists at `sprint/executor.py:85`; the whole-codebase assertion is unsatisfiable.

### PG11.1 — fix QA criteria
> Rewrite item (d) to: "frontmatter is parsed by exactly ONE extractor owned by the **envelope module**
> (`cli/roadmap/envelope.py`); there is NO `superclaude.contracts.parsers` submodule; both legacy parsers
> (`gates.py:_parse_frontmatter`, `_check_frontmatter`) are deleted." Rewrite (e) consumer-count to read
> against the envelope-owned extractor. ADD items: "(j) `code_assertions` are classified CI-only vs runtime
> and only runtime-safe ones fire in the live gate path; (k) the `gate_passed` envelope-None shim is
> PRESERVED with corrected comment (verify it was NOT blanket-deleted); (l) no source-tree assertion
> (`assert_step_reachable`) fires in the live/runtime path." Flag the `contracts.parsers` reference as a
> systemic contradiction to be reconciled in Phase 13 (Step 13.3) and the final-acceptance file list (L747).

## Net

Phase 11 is structurally sound on the parts the warning feared most (11.3/11.4 do not conflate genuine
fail-open stubs with the legitimate CI-only shim). The real defects are (1) the CORRECTED CI-vs-runtime
split is entirely missing, (2) 11.2 targets a non-existent `envelope.frontmatter` field, (3) the wrong
framing persists in code comments + the PG11.1 `contracts.parsers` QA criterion. Six REFACTORs, three KEEPs,
zero DISCARDs.
