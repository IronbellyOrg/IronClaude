# R0.2 Allowlist Design — Anti-Instinct Vocab-Lint (Contract #10)

**Phase:** 3 — R0.2 (Step 3.2)
**Source authority:** BUILD-REQUEST §R0 item 2, §Contract item #10, master:§Recurrence #6, MultiModelSwarm halt artifacts
**Inputs:** `phase-outputs/discovery/multimodelswarm-fp-seeds.md` (Step 3.1)
**Target:** `src/superclaude/cli/roadmap/obligation_scanner.py`

---

## 1. Chosen shape

**NEW module-level `_ALLOWLIST_PHRASES: frozenset[str]`** table (not an extension of `_DESCRIPTOR_NOUNS` or `_DEMOTED_H3_SUBSECTIONS`).

### Rationale (per seed case)

| Seed case | Why not extend `_DESCRIPTOR_NOUNS`? | Why not extend `_DEMOTED_H3_SUBSECTIONS`? | Why new `_ALLOWLIST_PHRASES`? |
|---|---|---|---|
| `stub transport` (L207, L211) | "transport" is not a descriptor noun (outcome/result/behavior/fallback). Adding it would over-broaden Layer 4 to demote unrelated lines like "outcome: transport layer failed". | The FPs appear in the M3 Wave-1 milestone table, not in a Risk Assessment / Integration Points / Milestone Dependencies / Open Questions H3. | Multi-word phrase carrying named-fixture semantics — most surgical. |
| `deterministic stub for tests` (L207) | Same — "tests" is too broad a descriptor; would demote every "outcome: stub fails tests" line which IS a real obligation. | Same — not in a demoted H3. | Multi-word phrase identifies the specific test-fixture description. |
| `deterministic stub transport for tests` (L211) | Same | Same | Same |
| `stub-worker parallelism test` (L213) | "parallelism" / "test" are too broad as descriptor nouns. | Same — appears in AC column of an M3 milestone row, not a demoted H3. | Phrase identifies the fixture's role precisely. |
| `transports/stub.py` (module path) | Module paths are not natural-language descriptors. | Same. | Phrase encodes the file-path token. |

### Conclusion

A phrase-based allowlist is the **minimal-blast-radius** fix. Extending `_DESCRIPTOR_NOUNS` or `_DEMOTED_H3_SUBSECTIONS` would either over-broaden (demoting genuine obligations) or under-cover (missing the FP location). The phrase set is the smallest construct that subtracts exactly the documented FPs.

---

## 2. Data structure

```python
# Layer 6 (R0.2 — Contract #10): Anti-instinct phrase allowlist.
# A SCAFFOLD-term match whose surrounding context substring contains one of
# these allowlist phrases is SKIPPED entirely (not demoted to MEDIUM) — these
# refer to named permanent test fixtures and architectural module paths, not
# scaffolding obligations.
#
# Seed authority:
#   BUILD-REQUEST §R0 item 2 (verbatim "stub transport", "stub-worker
#     parallelism test")
#   .dev/releases/Current/MultiModelSwarm/anti-instinct-remediation.md §1.1
#     (6 FP instances at roadmap.md lines 207, 211, 213 — pre-fix prose)
#   master:§Recurrence #6 (scaffold-vocabulary FP class)
#   Contract #10 (3+ known-false-positive fixtures from documented historical
#     recurrences)
#
# Phrase additions are GATED on:
#   1. A documented historical incident (no fabricated allowlist entries).
#   2. A negative-test fixture proving the allowlist did not silently mask a
#      real obligation (Step 3.4 valid_obligation_case.md).
#   3. A unit test asserting the new phrase is matched verbatim
#      (test_anti_instinct_recurrence.py).
#
# R1.3 forward: move to superclaude.contracts.vocabulary._ANTI_INSTINCT_ALLOWLIST_PHRASES.
_ALLOWLIST_PHRASES: frozenset[str] = frozenset(
    {
        "stub transport",
        "deterministic stub for tests",
        "deterministic stub transport for tests",
        "stub-worker parallelism test",
        "transports/stub.py",
    }
)
```

All entries are **lowercase** because the match function will lowercase the context line first (the existing `_DESCRIPTOR_NOUNS` adjacency check uses `re.IGNORECASE`; this allowlist uses case-folded substring match for cheaper hot-path execution).

---

## 3. Integration point

Inside `scan_obligations(content: str) -> ObligationReport` (currently L209-413).

**Insertion point:** Immediately after `_SCAFFOLD_RE.finditer` yields a match, inside the per-match loop, **before** the existing markdown-heading skip (currently L242-246). This guarantees:

- Allowlist hits do not enter the severity-determination cascade at all (no HIGH→MEDIUM demotion noise).
- Layer 1–5 behaviour is preserved for every non-allowlisted match (the cascade still fires for genuine obligations).
- The check is O(|_ALLOWLIST_PHRASES|) substring search on the context line — cheap.

**Pseudo-code:**

```python
for match in _SCAFFOLD_RE.finditer(phase_content):
    term = match.group()
    context_line = _get_context_line(phase_content, match.start())
    abs_line = start_line + phase_content[: match.start()].count("\n")

    # Layer 6 (R0.2 — Contract #10): Anti-instinct phrase allowlist.
    # SCAFFOLD-term matches whose context contains a documented permanent-fixture
    # phrase are SKIPPED entirely — these are named architectural artifacts,
    # not scaffolding obligations. See _ALLOWLIST_PHRASES docstring for the
    # source authority and addition criteria.
    if _is_allowlisted(context_line):
        continue

    # … existing Layer 1-5 logic unchanged …
```

And the helper:

```python
def _is_allowlisted(line: str) -> bool:
    """True when ``line`` contains a documented anti-instinct allowlist phrase.

    Phrase match is case-insensitive substring containment. Used as a Layer 6
    short-circuit in ``scan_obligations`` to skip emission for SCAFFOLD-term
    matches that refer to named permanent test fixtures or architectural
    module paths rather than scaffolding obligations.

    Per Contract #10, the allowlist subtracts from FPs only — adding a phrase
    requires a documented historical incident and a negative-test fixture
    proving no real obligation is masked.
    """
    lowered = line.lower()
    return any(phrase in lowered for phrase in _ALLOWLIST_PHRASES)
```

---

## 4. Planned test cases (Step 3.5 input)

| # | Test name | Fixture | Expected |
|---|---|---|---|
| 1 | `test_multimodelswarm_fp_demoted[case_207_stub_transport]` | `multimodelswarm_fp_case.md` | Zero HIGH findings (allowlist absorbs `stub transport`) |
| 2 | `test_multimodelswarm_fp_demoted[case_213_stub_worker_parallelism]` | `stub_worker_parallelism_fp_case.md` | Zero HIGH findings (allowlist absorbs `stub-worker parallelism test`) |
| 3 | `test_multimodelswarm_fp_demoted[case_module_path]` | `module_path_fp_case.md` | Zero HIGH findings (allowlist absorbs `transports/stub.py`) |
| 4 | `test_valid_obligation_still_flagged` | `valid_obligation_case.md` | HIGH finding emitted + undischarged (allowlist did NOT over-broaden) |
| 5 | `test_allowlist_provenance` | n/a (introspects module) | `_ALLOWLIST_PHRASES` docstring/comment contains `BUILD-REQUEST §R0 item 2`, `Contract #10`, `master:§Recurrence #6` |

---

## 5. Explicit non-widening confirmation

The allowlist **subtracts** from the set of HIGH findings — never adds. Specifically:

- The `_ALLOWLIST_PHRASES` set contains only phrases sourced verbatim from the MultiModelSwarm halt or from `master:§Recurrence #6` — no speculative additions.
- The Layer 6 short-circuit only fires when a SCAFFOLD term is already matching — it cannot introduce new matches.
- The `continue` skips the obligation emission entirely, so the allowlist cannot promote any line from MEDIUM to HIGH or from skip to MEDIUM.
- Contract #10 forbids fabricated allowlist entries; the unit test `test_allowlist_provenance` (Step 3.5) enforces the documentation invariant.

The negative-test guard (`test_valid_obligation_still_flagged`) is the empirical backstop: a genuine `Build stub authentication module` line continues to emit HIGH after the allowlist lands.

---

## 6. Forward-compatibility note (R1.3)

Per `research/02-patterns-conventions.md` §4.3, the `superclaude.contracts.vocabulary` module will eventually own all scanner-side vocabulary tables. The R0.2 implementation keeps `_ALLOWLIST_PHRASES` as a module-level `frozenset[str]` constant in `obligation_scanner.py` with a `# R1.3: move to superclaude.contracts.vocabulary._ANTI_INSTINCT_ALLOWLIST_PHRASES` TODO comment so the future migration is mechanical (no API change). The `frozenset[str]` shape is preserved across the migration to keep the in-place `in` check identical.

---

## 7. PRESERVE invariants

- `commands.py` — untouched
- `structural_checkers.py` — untouched
- `convergence.py` — untouched
- `cosmetic_remediator.py` — untouched
- Existing Layer 1-5 cascade behaviour — untouched (every non-allowlisted match takes the same code path it does today)
- Public API of `scan_obligations` / `Obligation` / `ObligationReport` — unchanged (allowlist hits become non-events, indistinguishable from no SCAFFOLD match at all)

---

**Status:** Step 3.2 complete. Proceeding to Step 3.3 (implementation).
