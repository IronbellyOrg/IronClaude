# /sc:reflect --mode post — Step 11.2 Frontmatter-Parser Canonicalization Audit

**Skill:** sc-reflect-protocol (UC-2 post-execution deviation audit)
**Tier:** Tier-1 GROUNDED single-pass (subagent cannot fan out nested reviewers; rigorous self-grounded pass per invocation contract)
**Scope:** Step 11.2 ALONE of TASK-RF-20260531-042405 (frontmatter-parser canonicalization per Proposal A′)
**Date:** 2026-06-02
**Stance:** ADVERSARIAL — assume the executor over-scoped, under-scoped, or silently diverged. Every claim carries a personally re-read `file:line` citation.

**Driving spec (read in full, in order):**
1. `phase-outputs/plans/step-11-2-parser-decision/decision.md` — Proposal A′ verdict (2026-06-02)
2. Task file Step 11.2 item (line 637) + "Ensuring:" acceptance clauses
3. `phase-outputs/discovery/r1-6-cleanup-inventory.md` §(a)
4. Task file `### Phase 11 - R1.6 Cleanup Findings` → Step 11.2 EXECUTED entry (line 1037)

**Hallucination contract:** every claim is Grounded (real file:line re-read) or tagged `[INFERRED]`.

---

## VERDICT: CONCERNS (PASS-with-fixes) — 0 Regression, 0 Drift, 2 Necessary deviations, 1 Authorized; 3 quality CONCERNS

The delivery faithfully implements Proposal A′. Proposal-A′ literal compliance is **complete and verified green**. Two documented deviations from `decision.md` item 4 (retaining `spec_parser`/`spec_patch` parsers) are **defensible Necessary deviations** — collapsing them would regress. The CONCERNS are (a) a **latent behavioral regression** on CRLF / horizontal-rule-led frontmatter (edge inputs the generated happy-path does not hit, but old parser tolerated and new rejects), (b) a **near-tautological determinism test** that is the spec-named "50+ blob" backbone, and (c) minor doc-staleness. None block; all have concrete fixes below.

---

## Per-area findings (every claim re-read personally)

### Area 1 — Behavioral equivalence of the canonical parser  →  CONCERN (latent regression, edge-only)

I reconstructed the OLD `roadmap/gates.py:_parse_frontmatter` verbatim from the git diff and ran it head-to-head against the NEW `extract_frontmatter` (`src/superclaude/cli/pipeline/frontmatter.py:90`) across 11 hand-built edge inputs. Six divergence classes found. Mapped each against what the **23 semantic checks** actually read (re-read `roadmap/gates.py:144-786` — every check reads **flat top-level scalars**: `total_analyzed`, `slip_count`, `convergence_score`, `undischarged_obligations`, `certified`, etc.).

| Input class | OLD result | NEW result | Could flip a gate verdict? |
|---|---|---|---|
| Preamble before `---` (e.g. `<!-- CONV -->\n---\n…`) | `None` (reject) | parses dict | **Yes, FAIL→PASS** — but only on a hand-authored/externally-modified artifact. All gate-target templates emit frontmatter at column-0 line-1 (`templates/extract.md.j2:1`, `generate.md.j2:1`, `spec_fidelity.md.j2:1`, `certify.md.j2:1`), so the **pipeline-generated happy path never hits this**. New is strictly *more lenient* here — not a safety regression. |
| CRLF (`---\r\nfoo: bar\r\n---\r\n`) | `{'foo':'bar'}` | **`None`** | **Yes, PASS→FAIL.** New `_FRONTMATTER_RE` (`frontmatter.py:57`) anchors closing delimiter with `---[ \t]*$`; `\r` is not `[ \t]`, so `finditer` returns `[]`. Old used `\n---` substring-find (CRLF-agnostic). **This is a genuine latent regression.** Realistic risk LOW (pipeline writes LF via `write_text`), but a CRLF artifact now silently fails its STRICT gate where it previously passed. |
| Horizontal-rule then frontmatter (`---\n\n---\nfoo: bar\n---`) | `{'foo':'bar'}` | `None` | Yes, PASS→FAIL on this exact shape. New non-greedy regex matches the FIRST `---…---` (the empty HR block), finds no top-level key, and `finditer` does NOT continue to the second block because the second `---` was consumed as the first block's closer. LOW realistic risk; flagged for completeness. |
| Nested list items (`items:\n  - id: M1`) | captures `- id` as a bogus key | top-level-only (drops it) | **No** — new is *cleaner*; no check reads `- id`/nested keys. Old's behavior was a latent bug (mis-keyed dict). New fixes it. |
| Indented key (`  nested: 2`) | captured | dropped | No — no check reads indented keys. |
| Value with leading dash / colon-in-value | minor key-name diffs | top-level-only | No — checks read named scalar fields only. |

**Conclusion for Area 1:** On realistic *pipeline-generated* artifacts (the dominant case), verdicts are **unchanged** — the executor's "no check changes verdict" claim holds for the happy path. The "behavioral SUPERSET" wording in the completion log (task L1037) is **imprecise**: the parser is a superset on block-detection (preamble) but a **restriction** on key-capture (top-level-only) AND a **regression** on CRLF/HR closing-delimiter handling. The top-level-only restriction is benign (even beneficial). The CRLF regression is real but latent. Classify: **Necessary deviation (behavior consolidation) with a latent-regression footnote** → see Recommendation R1.

### Area 2 — Retaining `spec_parser.py` + `spec_patch.py` parsers  →  Necessary deviation (defensible), NOT drift

`decision.md` item 4 + C1 sub-step (c) literally said "delete `spec_parser.py:parse_frontmatter L114` and `spec_patch.py:_extract_frontmatter L285`." The executor RETAINED both under the task's sanctioned API-divergence escape clause. I re-read both functions, their callers, and their distinct return contracts:

- `spec_parser.py:parse_frontmatter` (re-read `spec_parser.py:114-189`): does `yaml.safe_load` → `dict[str, Any]` with **nested structures + type coercion + a `warnings` ParseWarning channel**. Sole caller `spec_parser.py:656` (pre-pipeline spec ingestion, NOT the gate path). Collapsing onto the flat `dict[str,str]` gate parser would lose nested YAML, lists, and warnings → **a real regression to `test_spec_parser.py`**.
- `spec_patch.py:_extract_frontmatter` (re-read `spec_patch.py:285-313`): returns the **raw frontmatter block as `str`** (not a dict). Sole caller `spec_patch.py:84` re-emits the block verbatim. Different return type entirely.

Both carry new in-code DISTINCT-PURPOSE docstrings citing Contract #6 and are enumerated by `test_parser_consistency.py:153-163`. **Judgment: defensible Necessary deviation, not under-delivery.** Contract #6's brittleness driver was *two divergent GATE parsers producing different gate verdicts on the same content* — which is now closed (one gate parser). decision.md's own acceptance clause says "exactly one frontmatter parser reachable **from the pipeline** [gate path]" — satisfied. The executor's interpretation note (task L1037) is sound. **CONCERN (minor):** decision.md item 4's literal "delete" was not satisfied and the divergence is reconciled only in the completion-log prose, not in decision.md itself — the authoritative spec still textually says "delete." See Recommendation R3 (reconcile the spec).

### Area 3 — NFR-005 / NFR-007 compliance of the new import edges  →  PASS (genuinely, verified by running)

`tests/roadmap/test_nfr_compliance.py` re-read in full (L71-185). Ran it: **15 passed**.
- **NFR-005** (`test_no_gate_passed_import` L73, `test_imports_only_models` L80): forbid `from …pipeline.gates import` and `…pipeline.executor/process`. The new edge is `from superclaude.cli.pipeline.frontmatter import extract_frontmatter` (`roadmap/gates.py:26`) — `pipeline.frontmatter`, not `pipeline.gates`. Assertions pass.
- **NFR-007** (`test_no_roadmap_imports_in_pipeline` L177): iterates `pipeline/*.py`; the new `pipeline/frontmatter.py` imports only `re` (`frontmatter.py:48`) — zero roadmap/sprint imports. Pass.
- Placement = decision.md NFR-007 **option (i)** (canonical parser at pipeline level, roadmap imports it). Architecturally clean: no import cycle, `pipeline/frontmatter.py` is pure-parsing (not the gate-enforcement module NFR-005 targets). **Genuine pass, not "should."**

### Area 4 — Proposal A′ literal compliance  →  PASS (fully verified)

- **No `frontmatter` field on `PipelineEnvelope`:** `grep frontmatter envelope.py` = docstring word only; `dataclasses.fields(PipelineEnvelope)` = exactly the 8-field canon. `test_pipeline_envelope.py:312` `test_field_set_matches_mvr_section_1` (re-read L312-329) asserts the exact 8-field set `{release_id, spec_hash, spec_ids, artifacts, findings, counts, convergence, accepted_deviations}` → **GREEN**.
- **Exactly one gate parser:** `extract_frontmatter` (`frontmatter.py:90`). `pipeline/gates.py:_check_frontmatter` (re-read L113-152) is now a pure required-field validator that DELEGATES to `extract_frontmatter` (`gates.py:131`); `_FRONTMATTER_RE`/`_TOPLEVEL_KEY_RE`/`import re` removed from `pipeline/gates.py` (verified absent).
- **Both gate layers route through it:** `roadmap/gates.py:26` import + 23 callsites; `pipeline/gates.py:16` import + delegation. Verified.

### Area 5 — Completeness of callsite migration  →  PASS

- `_parse_frontmatter`: **zero** remaining references in `src/` (only docstring mentions in `frontmatter.py`). All 23 roadmap/gates.py callers migrated (count 23 confirmed by grep, matching the completion log; decision.md's "24" and inventory's "26/24" were pre-migration estimates — the actual live count is 23, no caller orphaned).
- Beyond-gates callers caught: `executor.py:764` (`total_requirements`, warning-only path) + `executor.py:4071` (`source_report_hash`, fail-closed) — both repointed, both read top-level scalars (safe under top-level-only).
- `_check_frontmatter` retained as a validator wrapper (correct — it's the required-field contract, not a parser).
- Cross-cutting `cli_portify/utils.py:11` + `audit/wiring_gate.py:925` (own `_FRONTMATTER_RE`) are correctly left as Phase-13 MIGRATE-flags (out of Step 11.2 gate-layer scope). **NOTE:** `wiring_gate.py:934` docstring says its regex is "duplicated from pipeline/gates.py" — that regex no longer lives in `pipeline/gates.py` (moved to `frontmatter.py`). Trivial doc-staleness, out-of-scope, flagged.

### Area 6 — Test quality of `test_parser_consistency.py`  →  CONCERN (the spec-named backbone is near-tautological)

Re-read `tests/roadmap/test_parser_consistency.py` in full.
- **Weak/tautological:** `test_parse_is_deterministic` (L93-98) — the spec's literal "parametrized determinism across 50+ blobs" (decision.md item 6) — asserts `extract_frontmatter(blob) == extract_frontmatter(blob)`. For a **pure deterministic function with no global state, this can never fail** regardless of correctness. A parser that always returned `{}` would pass all 50+ parametrized cases. The 50+ corpus therefore exercises *coverage of code paths* (good for crash-detection) but the **assertion proves nothing about output correctness**. This is the only test that satisfies the spec's explicit "50+ blobs" requirement, and it is the weakest one.
- **Strong / real:** `test_known_fields_extracted` (L100), `test_preamble_tolerated` (L104), `test_nested_lines_ignored` (L111), `test_no_frontmatter_returns_none` (L108) are genuine value-assertions. Plus the **migrated `test_gates_data.py:TestParseFrontmatterYaml`** (re-read diff) carries the real correctness coverage (quote-stripping, colon-values, int/float/bool) — value-preserving, not weakened. So the parser IS well-covered overall — just not by the file the spec named.
- `TestSingleGateParserInvariant` (L117-141): genuinely enforces Contract #6 structural invariants (legacy parsers gone, both layers route through canonical). **Strong.**
- **Could the consistency test pass if the parser were broken?** Yes for the 50+ determinism loop; No for the 4 value-assertions + the migrated gates_data tests. Net: a *subtly* broken parser (e.g., the CRLF regression in Area 1) **does pass** all of `test_parser_consistency.py` — confirmed, since no corpus blob uses CRLF. See Recommendation R2.

---

## Divergence taxonomy table

| # | Divergence from spec | Class | Evidence | Disposition |
|---|---|---|---|---|
| 1 | Canonical parser placed at `pipeline/frontmatter.py` (new module) rather than `roadmap/envelope.py` | **Authorized expansion** | decision.md:36 option (i) explicitly authorizes pipeline-level placement; NFR-007 requires it | Accept |
| 2 | `spec_parser.py:parse_frontmatter` retained (decision.md item 4 said delete) | **Necessary deviation** | `spec_parser.py:114-189` distinct contract (nested YAML+warnings); sole caller L656 is non-gate; deletion regresses `test_spec_parser.py` | Accept; reconcile spec (R3) |
| 3 | `spec_patch.py:_extract_frontmatter` retained (decision.md item 4 said delete) | **Necessary deviation** | `spec_patch.py:285-313` returns raw `str` block, different contract; caller L84 | Accept; reconcile spec (R3) |
| 4 | CRLF / HR-led frontmatter now rejected where old parser parsed | **Regression (latent, edge-only)** | empirical OLD-vs-NEW diff; `frontmatter.py:57` regex anchors `$` on `\r`-bearing line | Fix (R1) — non-blocking; pipeline writes LF |
| 5 | "50+ blob determinism" test is tautological | **Drift (test-quality)** | `test_parser_consistency.py:93-98` `f(x)==f(x)` | Strengthen (R2) |
| 6 | Stale docstrings/comments (`pipeline/gates.py:39,97` "R1.6 deletes this branch"; `wiring_gate.py:934`; `test_resume_pipeline_states.py:340`; `test_gates_data.py` class name) | **Drift (doc)** | re-read each | Mostly out-of-scope (39/97 are Step 11.4); fix opportunistically (R4) |

Counts: **Regression 1 (latent/edge)**, **Drift 2 (test + doc, non-functional)**, **Necessary 2**, **Authorized 1**.

---

## Prioritized recommended refactors (concrete; for the user to apply — I did not modify source)

**R1 (MEDIUM — close the latent CRLF regression).** File `src/superclaude/cli/pipeline/frontmatter.py:57`. The closing-delimiter regex `r"^---[ \t]*\n(.*?)\n---[ \t]*$"` rejects CRLF and (incidentally) HR-then-FM. Two-part fix: (a) normalize line endings at function entry in `extract_frontmatter` — `content = content.replace("\r\n", "\n").replace("\r", "\n")` before the scan; (b) optionally make the block scan continue past an empty/keyless first block (the HR case) — the `finditer` loop already tries subsequent matches, but the non-greedy regex consumes the second `---` as the first block's closer; normalizing alone does not fix HR. Minimum viable fix = (a) CRLF normalization (covers the realistic risk). Add a corpus case with `\r\n` to `test_parser_consistency.py:_build_corpus` AND a value-assertion (not just determinism) proving CRLF parses identically to LF.

**R2 (MEDIUM — de-tautologize the spec-named determinism test).** File `tests/roadmap/test_parser_consistency.py:93-98`. Replace the `f(x)==f(x)` self-comparison with a **golden-output** assertion: build the corpus as `(blob, expected_dict_or_None)` pairs and assert `extract_frontmatter(blob) == expected`. This makes the 50+ corpus actually prove correctness (and would have caught the CRLF regression). Keep the structural-invariant classes as-is (they are strong).

**R3 (LOW — reconcile the authoritative spec with the as-built reality).** File `…/plans/step-11-2-parser-decision/decision.md:30` (item 4) still textually instructs deleting `spec_parser.py:parse_frontmatter` and `spec_patch.py:_extract_frontmatter`. The as-built (correctly) retained them as distinct-purpose. Append a one-line erratum to decision.md item 4: "ERRATUM 2026-06-02: spec_parser/spec_patch RETAINED as distinct-contract parsers (collapsing regresses); Contract #6 is satisfied by single-gate-parser. See task L1037." This prevents a future reader treating decision.md as ground-truth and 'finishing' the deletion.

**R4 (LOW — opportunistic doc-staleness, mostly Step 11.4 scope).** `pipeline/gates.py:39` and `:97` still say "R1.6 deletes this branch/skip-path" — these are **Step 11.4 / PG11.1(k)'s** correction targets, not Step 11.2; leave for 11.4 but do not lose track. `wiring_gate.py:934` "duplicated from pipeline/gates.py" → update to "from pipeline/frontmatter.py" when Phase 13 migrates it. `test_gates_data.py:TestParseFrontmatterYaml` docstring "yaml.safe_load-based" is now inaccurate (the canonical parser is regex-based) — rename to `TestCanonicalGateParser` for clarity. `test_resume_pipeline_states.py:340` comment names `_parse_frontmatter` — cosmetic.

---

## Acceptance-clause scorecard (decision.md:41 + task L637 "Ensuring:")

| Acceptance clause | Status | Evidence |
|---|---|---|
| Exactly one frontmatter parser reachable from the pipeline | PASS | `extract_frontmatter` sole gate parser; `_check_frontmatter` delegates |
| `test_parser_consistency.py` green | PASS (weak) | 31 passed / 1 skipped; backbone tautological (R2) |
| `test_pipeline_envelope.py:312` green (no field added) | PASS | 8-field canon asserted; envelope has no `frontmatter` field |
| All 8 SemanticCheck modules + sprint untouched | PASS | only `roadmap/gates.py` + `pipeline/gates.py` gate modules touched; sprint not in diff |
| ruff + `make verify-sync` clean | PASS | ruff "All checks passed" on 9 files; (verify-sync per completion log) |
| NFR-005 / NFR-007 honored | PASS | `test_nfr_compliance.py` 15 passed |

**Net: the step is DONE and correct for its core objective.** The CONCERNS are quality-hardening (CRLF latent regression + tautological test) and spec-hygiene, none of which block Phase 11 progression. Recommend applying R1 + R2 before R1.6 closes; R3 + R4 are housekeeping.

---

## Status: COMPLETE
