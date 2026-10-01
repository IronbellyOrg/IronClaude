# Phase-6 QA Gate — Consolidated Findings + Triage + Fix Round (I20 serialized)

Date: 2026-06-11. Six adversarial lenses spawned in parallel (3 rf-qa structural + 3 rf-qa-qualitative content), all `fix_authorization: false` (report-only). The executor consolidated and applied the serialized fix round.

## Lens verdicts (raw)

| Lens | Agent | Verdict | Findings |
|------|-------|---------|----------|
| Contract-conformance | A (rf-qa) | FAIL | F1 `--output` not in §2 minimal shape (CRITICAL); F2/F3 forbidden-token prose in blocks (IMPORTANT); F4/F5 PRE permits `quick` (IMPORTANT) |
| NFR-7 + skip-guard | B (rf-qa) | **PASS** | none — O1/O2 blocks `Task(`=0/`subagent_type`=0; marker spelled exactly; exit codes documented |
| Structural-integrity | C (rf-qa) | FAIL | C1 sibling `### Checkpoint:` headings in phase-template (IMPORTANT) + parser smoke PASS |
| Operational-correctness | D (rf-qa-qual) | FAIL | D1 frontmatter omission allowed vs wrapper writeback (IMPORTANT); D2 remove xfail (MINOR) |
| Completeness / orphan | E (rf-qa-qual) | FAIL | E1 stale `Sub-Agent Delegation | Required` metadata (IMPORTANT) |
| Test-correctness | F (rf-qa-qual) | FAIL | F1 xfail reason mentions `Mode 2`/`§6.3` markers (IMPORTANT) + test xpassed, suite 77p/1xp |

## Adversarial triage (executor)

**ACCEPTED (2 real findings → fixed in serialized round):**

- **D1 (frontmatter required-when-gating-on).** SKILL:100 + struct-check #5 said the leading frontmatter was "optional". But when reflect gating is enabled (default), the O2 gate runs `superclaude reflect run` on each phase file and the wrapper needs the frontmatter block as its `reflect_post` writeback target (`runner.py:146-148` → `frontmatter-missing` → BLOCKED/exit-2 on a clean PASS). **Fix:** both assertions now state the block is REQUIRED when reflect gating is enabled (the O2 writeback target), omittable ONLY under `--no-reflect`.
- **E1 (stale `Sub-Agent Delegation` metadata).** The O2 per-phase reflection task's metadata still read `Sub-Agent Delegation | Required (fresh-session reflect ensemble)` — a relic of the old spawn-directive form — contradicting the new flat Bash shell-out body ("no agent-spawn directive"). **Fix (both SKILL:1061 + phase-template:154):** `Sub-Agent Delegation | No (flat superclaude reflect run Bash shell-out; the wrapper spawns the executor-disjoint reflect ensemble internally)`.

**REJECTED (false positives — rationale):**

- **A.F1 `--output`** — `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` is MANDATED by item 3.1 + research GAP-3: the wrapper's default output dir (`<dir>/reflect/post/<sha>/`, `config.py:207-213`) would orphan the declared `**Reflect Report Path:**` and its Acceptance Criterion. `--output` is a real, contract-allowed flag (the §2 "MUST NOT emit" list is `--reflect`/`--max-turns`/`<base>..HEAD` only). Agent A applied an overly-literal "byte-identical to the §2 minimal line" reading.
- **A.F2/F3 forbidden-token prose** — the literal tokens appear only in NEGATIVE prohibition prose ("Emit NO `--reflect`, NO `--max-turns`, NO `<base>..HEAD`") and base-resolution explanation (`start_commit..HEAD` as the wrong-form contrast). They are NOT emitted as command arguments; Agent A acknowledged this. The Layer-A test only forbids `Task(`/`subagent_type` in the O1 block (both 0).
- **A.F4/F5 PRE `quick`** — the PRE gate uses `/sc:reflect --mode pre --depth <pre_depth>` (a DIFFERENT command than the wrapper's `superclaude reflect run`). The contract's `--depth standard|deep` constrains the WRAPPER; `/sc:reflect` PRE legitimately allows `quick`. The PRE gate is explicitly OUT OF SCOPE / INTACT (task framing + item 2.7), and `quick` for PRE is intended ("no diff exists pre-execution").
- **C1 sibling `### Checkpoint:` headings** — PRE-EXISTING in the human-review template (not in `git diff origin/master`); research 02 SURFACE 3 marked the checkpoint section "KEEP, no change". A pre-existing template simplification (the template uses illustrative `### Checkpoint:` while struct #18 mandates `### T<PP>.<NN> -- Checkpoint:` for ACTUAL generated files). Out of scope for this reflect-gate-wiring task; logged as a pre-existing observation.
- **D2 remove xfail** — contradicts OQ-1 (operator chose to KEEP `@pytest.mark.xfail(strict=False)` → XPASS, 2026-06-11). Agent D lacked the OQ-1 context.
- **F.F1 xfail reason mentions `Mode 2`/`§6.3`** — OQ-1 EXPLICITLY directed the reason to "record the stale-marker migration", which inherently names the abandoned markers in past-tense/historical context. The assertion + anchor logic is clean of Mode markers; the documentary reason string intentionally records the migration provenance.

## Re-verification after the fix round

- `make sync-dev` → OK; `make verify-sync` → exit 0.
- D1 fix landed at 2 sites (SKILL:100 + struct #5); E1 fix landed in both O2 files.
- Named acceptance test `test_layer_a_wrapper_branch_is_bash_shellout` → **xpassed**.
- Parser smoke (seeded frontmatter): `count_tasks_in_file`=2, `parse_tasklist`=[T02.01,T02.02], `_extract_phase_name`='- Wiring' (frontmatter-transparent, unchanged by D1/E1).

## Gate result

**QA gate PASS** — Lens B clean; all ACCEPTED findings (D1, E1) fixed and re-verified; all REJECTED findings are documented false-positives (overly-literal criteria, OQ-1/GAP-3 context gaps, or pre-existing out-of-scope template content). One serialized fix round (well within the 3-cycle cap). `make verify-sync` + the named test green post-fix.
