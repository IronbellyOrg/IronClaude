# NFR-CONV.2 — Research-Driven Prose Determinism Boundary

**Scope:** `task-builder-merge` / `roadmap.md` row R-146 / NFR-CONV.2
**Published:** 2026-05-18 (Phase 7 / T07.07 / D-0088)
**Audience:** rf-qa maintainers, GA-tagging committee, future
NFR-CONV.* auditors

This page is the M7 acceptance artifact for NFR-CONV.2 ("Research-driven
prose determinism exclusion documentation"). It enumerates which
parts of a task-builder output are byte-deterministic and which are
not, and pins the structural-vs-prose boundary that the M7 audit
relies on.

---

## 1. Why a determinism boundary exists

The `task-builder` pipeline emits two qualitatively different
artefacts in the same output set:

1. **Structural fields** — the gate fields the rf-qa structural QA
   reads to decide PASS / FAIL (item identifiers, axis labels in
   `axis (PR-07)` columns, table headers, the literal `Self-Audit`
   heading, dedup-key strings, finding counts, verdict labels).
2. **Research-driven prose** — the narrative content produced by LLM
   research and synthesis (paragraph wording, sentence ordering,
   word choice within "Why" / "Notes" / "Rationale" fields).

The structural fields are byte-deterministic by construction
(`NFR-CONV.1`). The research-prose is *intentionally* non-deterministic
(`NFR-CONV.2`): an LLM run-to-run will phrase the same finding two
different ways, and that variance is acceptable because gate verdicts
are driven by the structured fields, not the prose. Full
byte-determinism over the entire output was REJECTED during the
roadmap debate (`roadmap.md:592`) as impossible with an LLM-driven
builder; zero-determinism was REJECTED because gate verdicts must
remain reliable.

The structural side carries the load-bearing signal; the prose side
is the human-readable cover.

---

## 2. The boundary, enumerated

### 2.1 Structural fields (byte-deterministic — NFR-CONV.1)

These MUST be byte-identical across two runs of the same input.

| Field | Producer | Example | Audit surface |
|---|---|---|---|
| Item identifiers (`N.M`) | TB-Add-1 schema | `1.1`, `2.4` | rf-qa.md:114, TB-Add-1 catalogue |
| Schema field names | TB-Add-1 schema | `Context`, `Action`, `Output`, `Verification`, `Completion gate` | rf-qa.md:296 |
| Verdict labels | rf-qa scorer | `PASS`, `FAIL`, `VERIFIED` | rf-qa.md:144-145 (anchor) |
| Severity labels | rf-qa scorer | `CRITICAL`, `IMPORTANT`, `MINOR` | rf-qa.md:145 |
| Self-Audit heading | rf-qa-qualitative producer | `## Self-Audit` | rf-qa-qualitative.md:794+ (INV-019 floor) |
| Inherited-Verdict block header | task-builder A.10.5 template | `## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)` | SKILL.md (API-002 wire-contract) |
| axis (PR-07) labels in Items Reviewed | rf-qa schema | `drift`, `n/a`, etc. | TB-Add-7 column populated check |
| Dedup-key strings | DNSP partition emitter | `dnsp:<partition>:<kind>:<rev>` | DNSP partition spawn-log |
| Finding counts | rf-qa scorer | `Checks passed: N / M` | rf-qa-qualitative.md Output Format |
| Reliance bullets (category-a) | INV-019 schema | `- Relied on rf-qa PASS for TB-Add-N` | rf-qa-qualitative.md:823+ |
| Independent-semantic-check labels (category-b) | INV-019 schema | `semantic counterpart verified`, `verified by <file>:<line>` | rf-qa-qualitative.md:944-951 |

All eleven categories above are exercised by static fixtures under
`tests/audit/` (TEST-007, TEST-009, TEST-023..TEST-025, NFR-CONV.6
fixture, NFR-CONV.9 fixture). The structural surface is observable
via the existing `test_self_audit_inv_019.py` detector
(`_self_audit_present`, `_count_category_b_bullets`,
`_inflation_positive`).

### 2.2 Research-driven prose (nondeterminism acceptable — NFR-CONV.2)

These MAY vary run-to-run without violating any invariant.

| Surface | Producer | Why non-determinism is acceptable |
|---|---|---|
| Item `Why` field wording | task-builder synthesis | Gate driven by presence + `file:line` density, not wording. |
| Item `Notes` paragraphs | task-builder synthesis | Free-form context; not scored by structural QA. |
| Research-file Summary prose | rf-researcher | Density of `file:line` citations is scored; phrasing is not. |
| Gap-description prose in rf-qa reports | rf-qa | Severity label is scored; wording is not. |
| Self-Audit category-(b) bullet *content* | rf-qa-qualitative | The category-(b) `verified by …` pattern is structural (counted); the surrounding prose is free. |
| Issues Found body | rf-qa-qualitative | Issue *count* is structural; the per-issue description is prose. |

---

## 3. Structural annotations embedded inside prose

The interesting boundary lives where a structural token sits inside
a prose paragraph. These tokens MUST remain byte-equal across two
runs of the same input even when the surrounding sentence varies.

| Annotation | Embedded in | Byte-equal requirement |
|---|---|---|
| Axis labels (`axis (PR-07)`) | Items Reviewed table cells | The label string itself is byte-equal; surrounding cell prose may vary. |
| Finding counts (`N / M`) | Summary section | Both numbers are byte-equal; surrounding sentence may vary. |
| Dedup-key strings | DNSP synthetic-finding bodies | The full `dnsp:<partition>:<kind>:<rev>` string is byte-equal; the explanation prose may vary. |
| Verdict labels (`PASS`/`FAIL`/`VERIFIED`) | Verdict lines, Items Reviewed rows | The label is byte-equal; the rationale prose may vary. |
| Severity labels (`CRITICAL`/`IMPORTANT`/`MINOR`) | Gap-severity bullets | The label is byte-equal; the explanation may vary. |
| `file:line` citations | Anywhere in research/QA prose | Path + line number byte-equal; surrounding description may vary. |

The M7-audit acceptance claim from `roadmap.md:425` — "M7 audit
verifies structural annotations within prose remain byte-equal
across 2 runs" — is exercised by
`tests/audit/test_nfr_conv_9_zero_trust.py::TestStructuralAnnotationsByteEqualAcrossRuns`,
which reads each NFR-CONV.9 fixture twice and asserts byte-equality
over the structural surface (verdict label, severity row,
PASS/FAIL bullet presence).

---

## 4. Determinism contracts the boundary preserves

| Contract | Source | Status |
|---|---|---|
| Structural-fields byte-equal | NFR-CONV.1 | Held by TEST-023 (D-0089), NFR-CONV.6 fixture (D-0086). |
| Prose nondeterminism acceptable | NFR-CONV.2 (this page) | Held by design; no test required (negative absence-of-determinism contract). |
| Structural annotations in prose byte-equal across runs | NFR-CONV.2 acceptance row | Held by `test_nfr_conv_9_zero_trust.py` (D-0088). |
| PASS / FAIL bullet text byte-equal pre/post M5+M6 | NFR-CONV.9 invariant anchor | Held by `test_nfr_conv_9_zero_trust.py::TestPassFailBulletsByteIdentical` (D-0088). |
| Self-Audit heading position ≥ rf-qa-qualitative.md:794 | INV-019 / K-003 | Held by `test_self_audit_inv_019.py` (D-0037). |
| Inherited Structural Verdict block header verbatim | API-002 / FR-CONV.3 | Held by `test_inherited_verdict_present.py` (D-0035). |
| Self-Audit category-(b) ≥ 1 per VERIFIED item | INV-019 / NFR-CONV.9 part (b) | Held by `test_nfr_conv_9_zero_trust.py::TestPartB_*` (D-0088). |

---

## 5. What this boundary excludes

- The boundary does **not** require that two LLM runs produce
  identical research-prose. They will not, and forcing them to would
  break NFR-CONV.2 by definition.
- The boundary does **not** weaken the rf-qa structural QA: the gate
  rule at `src/superclaude/agents/rf-qa.md:144-145` ("Any gaps
  exist (CRITICAL, IMPORTANT, or MINOR) → FAIL") applies regardless
  of how the gap is *worded*. The severity label drives the verdict;
  the prose description does not.
- The boundary does **not** apply to free-form output produced
  outside the task-builder pipeline (general agent prose, console
  output, plan-mode text). Those surfaces have no determinism
  contract.

---

## 6. Cross-references

- **PRD anchor:** `roadmap.md:28` ("Determinism scope split
  (NFR-CONV.1 byte-identical structural fields; NFR-CONV.2
  LLM-driven prose nondeterminism acceptable) — gate verdicts driven
  by structured output, semantic prose intentionally excluded from
  determinism scope.")
- **Roadmap row:** `roadmap.md:425` (R-146 / NFR-CONV.2).
- **Roadmap debate:** `roadmap.md:592` (REJECTED alternatives:
  full-byte-determinism and zero-determinism).
- **Invariant anchor:** `src/superclaude/agents/rf-qa.md:144-145`
  PASS/FAIL bullets (line index was 141-142 in the pre-FR-CONV.*
  baseline commit `fd41178`; the bullet text is byte-identical
  across all nine intervening commits through HEAD).
- **Self-Audit floor:** `src/superclaude/agents/rf-qa-qualitative.md:794+`
  (T03.04 / D-0029 / INV-019).
- **Fixture (this M7 audit):** `tests/audit/test_nfr_conv_9_zero_trust.py`
  (D-0088 / T07.07).
- **Companion fixtures:** `tests/audit/test_nfr_conv_6_self_contained.py`
  (D-0086 / T07.04); `tests/audit/test_self_audit_inv_019.py`
  (D-0037 / T03.14); `tests/audit/test_inherited_verdict_present.py`
  (D-0035 / T03.11).
- **Downstream composite:** `tests/audit/test_invariant_preservation_NFR_6_through_10.py`
  (D-0090 / T07.09; will fold this boundary into the 5-invariant
  union check).
