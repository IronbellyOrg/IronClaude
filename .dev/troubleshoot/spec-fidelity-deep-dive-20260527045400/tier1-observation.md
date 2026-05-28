# Tier 1 — Real-Code Grounding (Wave 1)

## Symptom

`spec-fidelity.md` reports: `Convergence Result: FAIL — Runs Completed: 3 — Final HIGH Count: 54`.

Halt message (verbatim): `Convergence not reached after 3 runs. Remaining active HIGHs: 54. TurnLedger: available=31, consumed=46`.

## Reproducer / observation

No live reproducer needed — failing artifacts are pinned at `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/`:
- `.roadmap-state.json` — pipeline state file; `spec-fidelity` is the only step with status `FAIL`.
- `spec-fidelity.md` — emits 4-line Structural Progress log: Run 1 (catch) structural 0→58; Run 2 (verify) 58→54; Run 3 (backup) 54→54 (NO progress in Run 3).
- `deviation-registry.json` — 58 total findings: 4 FIXED (data_models / spec_file manifest gaps), 54 ACTIVE (all `dimension=signatures, source_layer=structural, mismatch_type=phantom_id`).

## Real-code grounding (from Phase 0 auggie + direct reads)

| Citation | What it shows |
|---|---|
| `src/superclaude/cli/roadmap/structural_checkers.py:380` | `phantom_ids = roadmap_ids - spec_ids` — raw Python set difference of strings. No canonicalization. |
| `src/superclaude/cli/roadmap/structural_checkers.py:381-391` | For each `pid` in the difference, emit a HIGH `phantom_id` finding with `description=f"Roadmap references ID '{pid}' not found in spec"`. |
| `src/superclaude/cli/roadmap/spec_parser.py:329` | `"D": re.compile(r"\bD-?\d+\b")` — matches `D1`, `D01`, `D-01` interchangeably during extraction, but emits them as raw matched strings. |
| `src/superclaude/cli/roadmap/spec_parser.py:340-344` | `extract_requirement_ids` returns `sorted(set(pattern.findall(text)))` — preserves the raw matched form, no normalization. |
| `src/superclaude/cli/roadmap/convergence.py:432-668` | `execute_fidelity_with_convergence` — 3-run loop. Pass condition (line 539): `active_highs == 0`. Halt formatter (line 655-660): "Convergence not reached after {max_runs} runs". |
| `src/superclaude/cli/roadmap/convergence.py:440` | `max_runs: int = 3` (hard default). |
| `src/superclaude/cli/roadmap/remediate_executor.py:309-362` | `check_patch_diff_size` — rejects patches with `ratio > 0.30` of `original_lines`. |
| `src/superclaude/cli/roadmap/structural_checkers.py:270-282` | `_make_finding` — generic `fix_guidance=f"Address {mismatch_type} in {dimension} dimension"`. Not templated per mismatch_type. |

## Mechanical analysis

Direct verification on TUIBBS artifacts:

```
spec D-family IDs   (epics.md grep):   {D1, D3, D5}            # 3 IDs, no zero-pad
roadmap D-family IDs (roadmap.md grep): {D01, D02, ..., D54}    # 54 IDs, all zero-padded
phantom_ids = roadmap_ids - spec_ids = {D01, ..., D54}          # all 54
```

The checker's set difference is exact-string. `'D01' != 'D1'`. The regex at `spec_parser.py:329` is *lenient* (`D-?\d+` matches both forms), but the *comparison* at `structural_checkers.py:380` is *strict* (Python `set` difference is exact-string).

This is a deterministic mechanical bug. It does not depend on LLM behavior, prompt design, or remediation strategy.

## Why remediation can't converge it out

Between Run 2 and Run 3, `roadmap_hash` changes from `8f6eba…` to `d6070e…` — the agent IS editing the roadmap. But:
- The only structurally-correct edit is one of:
  - (a) Rename all 54 roadmap IDs from `D01…D54` to `D1…D54` (no zero-pad). Massive structural rewrite. Diff > 30%. Rejected by `_check_diff_size`.
  - (b) Add `D01`-`D54` to the spec. Agent is not allowed to modify spec (it's an input).
  - (c) Make the checker normalize `D01` ↔ `D1`. Code fix in IronClaude, not in roadmap.
- The generic `fix_guidance="Address phantom_id in signatures dimension"` doesn't disambiguate. The agent makes cosmetic edits (changing 4 doc-manifest rows it CAN fix) and leaves the 54 IDs untouched.

## State at end of Wave 1

- Grounding complete; symptom is structural (deterministic checker bug + non-additive remediation requirement + diff guard rejecting the only correct fix + no escape valve).
- No external repro needed.
- Wave 1.5 will surface release-doc + architectural-doc + semantic-restriction context that wraps this mechanical fact.
