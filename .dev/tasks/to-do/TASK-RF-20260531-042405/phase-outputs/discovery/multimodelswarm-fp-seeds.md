# MultiModelSwarm Anti-Instinct False-Positive Seed Inventory

**Phase:** 3 — R0.2 (Step 3.1)
**Source authority:**
- `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/anti-instinct-remediation.md` §1 (6 stub-transport FPs, lines 207/211/213)
- `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/roadmap.md` lines 207–216 (M3 §Dispatch & Concurrency, COMP-033 / FR-023 / IMM-3 rows)
- `master-report.md` §Recurrence #6 (scaffold-vocabulary FP class)
- BUILD-REQUEST §R0 item 2 (verbatim: "stub transport", "stub-worker parallelism test")

**Layer reference:** obligation_scanner.py `_DESCRIPTOR_NOUNS` L109-125, `_DEMOTED_H3_SUBSECTIONS` L137-142, `_is_meta_context` L713-744 (per `research/02-patterns-conventions.md` §4.1).

**Audit re-run (2026-05-31 18:07 UTC):** undischarged_obligations: 0 — the halt has been MANUALLY resolved via roadmap.md rename ("stub transport" → "deterministic-fixture transport"). Phase 3 codifies the allowlist into Contract #10's CI fixture so future runs do not regress if the rename is reverted or the same pattern appears in another release.

---

## Seed cases — verbatim from MultiModelSwarm halt

The 6 historical FP instances all matched SCAFFOLD term `\bstub(?:bed|s)?\b` (vocabulary.py:17) against a **permanent test fixture** (`cli/swarm/transports/stub.py` — module name is architectural, not a temporary scaffold). Per remediation §1.1, "There is no 'discharge' because there is nothing to discharge."

| Line # | Trigger Text (verbatim) | Layer that fired | Should-have-demoted-via | Context (3-line window) | Allowlist entry needed (verbatim) |
|---|---|---|---|---|---|
| 207 (Title col, COMP-033 row, pre-fix) | `stub transport` | Layer 0 (raw SCAFFOLD_TERMS match before any demotion) | A new phrase-allowlist that recognises `stub transport` as a named permanent fixture, not a scaffolding obligation | `\|2\|COMP-007\|dispatch (Wave 1)\|httpx ThreadPoolExecutor...` (L205) / `\|6\|COMP-033\|stub transport\|Deterministic stub for tests\|cli/swarm/transports/stub.py\|COMP-031\|fixed deterministic outputs; enables parallelism test\|S\|P0\|` (L207, pre-fix) / `\|7\|FR-001\|swarm run subcommand\|...` (L211) | `stub transport` |
| 207 (Description col, COMP-033 row, pre-fix) | `Deterministic stub for tests` | Layer 0 (raw match) | Same — phrase allowlist for the test-fixture descriptor | (same row as above — "Deterministic stub for tests" appears in the Description cell) | `deterministic stub for tests` |
| 211 (Title col, FR-023 row, pre-fix) | `stub transport` | Layer 0 (raw match) | Same phrase allowlist | `\|10\|FR-023\|stub transport\|Deterministic stub transport for tests\|transports\|COMP-033\|tests run without network\|S\|P0\|` (L211, pre-fix) | `stub transport` (already covered by row above) |
| 211 (Description col, FR-023 row, pre-fix) | `Deterministic stub transport for tests` | Layer 0 (raw match) | Phrase allowlist | (same row — "Deterministic stub transport for tests") | `deterministic stub transport for tests` |
| 213 (AC col, IMM-3 row, pre-fix) | `stub-worker parallelism test` | Layer 0 (raw match) | Phrase allowlist — `stub-worker` is a fixture-class noun, not an imperative scaffold action | `\|12\|IMM-3\|True-parallel dispatch\|One ParallelGroup, N workers, code-enforced parallelism replacing attention-mediated tool calls\|dispatch\|COMP-007,AC-004\|stub-worker parallelism test: N workers overlap in wall-clock\|M\|P0\|` (L213, pre-fix) | `stub-worker parallelism test` |
| 207–213 (multiple rows reference) | `transports/stub.py` (module path) | Layer 0 (raw match — `\bstub(?:bed|s)?\b` matches the bare `stub` within `stub.py`) | Phrase allowlist — module-path token | The module path appears in the Component column for COMP-033 (L207) and the AC column ("cli/swarm/transports/stub.py", L209) | `transports/stub.py` |

**FP-cluster size:** 6 verbatim occurrences across 3 roadmap lines (207, 211, 213). The remediation §1.2 collapsed all 6 by renaming the prose token `stub transport` → `deterministic-fixture transport`. The module path `cli/swarm/transports/stub.py` was intentionally left untouched because the Python file name is architectural and not visible to the scanner (which reads roadmap prose only).

---

## Allowlist scope decision

The allowlist mechanism must recognise these as **named permanent fixtures**, not as descriptor-noun-adjacent prose (Layer 4) and not as H3-subsection-demoted (Layer 5). The phrase `stub transport` does not sit inside Risk Assessment / Integration Points / Milestone Dependencies / Open Questions, so Layer 5 cannot help. The phrase contains no descriptor noun (outcome / fallback / historical / etc.), so Layer 4 cannot help. The phrase is not in a negation prefix or shell-cmd or table-cell-imperative or parenthetical-phase-label, so Layer 3 cannot help.

→ A **new `_ALLOWLIST_PHRASES: frozenset[str]`** module-level table is the minimal-blast-radius fix. The allowlist is checked in `scan_obligations` immediately after the SCAFFOLD match, before any HIGH/MEDIUM severity assignment — and matched phrases skip emission entirely (not demote to MEDIUM, since these are *not* obligations at all).

---

## Negative-test guard (anti over-broadening)

To prove the allowlist does not silently mask real obligations, a **valid-obligation fixture** at `tests/roadmap/fixtures/recurrence/anti_instinct/valid_obligation_case.md` must contain a roadmap line where:

- The SCAFFOLD term IS a genuine temporary scaffold (e.g., `Build stub authentication module` — Layer 3a/3b absent, Layer 4/5 absent, no allowlist hit)
- The expected behaviour is HIGH severity emission + undischarged status (no later "replace stub" / "wire stub" / "remove stub" discharge)

If this fixture stops emitting HIGH after the allowlist lands, the allowlist over-broadened.

---

## Forward-compatibility note (R1.3)

Per `research/02-patterns-conventions.md` §4.3, the allowlist may move to `superclaude.contracts.vocabulary` in R1.3. The R0.2 implementation keeps the table as a module-level constant in `obligation_scanner.py` with a `# R1.3: move to superclaude.contracts.vocabulary._ANTI_INSTINCT_ALLOWLIST_PHRASES` TODO comment to keep the audit trail visible.

---

## Completeness check

- [x] Every FP from MultiModelSwarm halt enumerated with verbatim quotes (no paraphrasing)
- [x] Every entry maps to a specific Layer with a file:line citation
- [x] "Allowlist entry needed" column proposes concrete additions (5 phrases — 3 minimum required by Contract #10, plus 2 to cover all 6 verbatim FPs)
- [x] No fabrication — every phrase appears verbatim in `roadmap.md` pre-fix or in the remediation report

**Status:** Step 3.1 complete. Proceeding to Step 3.2 (design).
