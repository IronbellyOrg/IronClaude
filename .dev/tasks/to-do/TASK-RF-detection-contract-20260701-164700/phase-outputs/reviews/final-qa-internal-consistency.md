# QA Report — Report Validation (task-integrity / internal-consistency lens)

**Topic:** TASK-RF-detection-contract — cross-surface internal consistency of the detection-contract readiness surface
**Date:** 2026-07-02
**Phase:** report-validation (lens: internal-consistency)
**Fix cycle:** N/A
**Fix authorization:** false (report-only; no files modified)

---

## VERDICT: PASS

No contradiction found across helper code, the reflect CLI surface, both command docs, both skill docs, and the tests. All four checklist items verified with byte-level evidence.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No contradiction across code / reflect CLI / command docs / skill docs / tests; command shape `superclaude reflect contract-status [--validate] --repo <owner/repo> --pr <number>` identical everywhere | PASS | Bracketed `[--validate]` form byte-identical at `commands/reflect.md:122`, `commands/reflect.md:281`, `commands/pr-submit.md:61`, `skills/sc-pr-submit-protocol/SKILL.md:90`. Two-line non-bracketed form (status / status --validate) byte-identical at `commands/reflect.md:69`, `skills/sc-reflect-protocol/SKILL.md:63`. CLI emits the same tokens via `diagnosis.py::_next_command` (`future_status`/`future_validate`) and `commands.py::_contract_status_next_command`. Tests assert the exact strings (`test_detection_contract.py:90-99`, `test_contract_setup_diagnosis.py:108-160`). |
| 2 | Reflect readiness surface is exactly ONE (sibling CLI); no `/sc:reflect --contract-status` flag alias presented as current | PASS | `grep -rn "--contract-status" src/superclaude/` returns EMPTY. Every readiness reference is the sibling subcommand `superclaude reflect contract-status`, registered once at `commands.py:76` (`@reflect_group.command("contract-status")`) and asserted single-surface at `test_contract_status_cli.py:70-73,291-292`. reflect.md §"Detection-contract readiness bypass" (64-73) and reflect SKILL §2.1 (58-67) both route to the CLI, not a flag. |
| 3 | `--monitor` ordinal behavior consistent: `0` = open-PR-only/no-monitor; `>=1` fail-closes through `DetectionContract.for_arming()` before Monitor arming; canonical no-side-effect sentence identical in code, command doc, skill doc | PASS | `for_arming()` = `load(prefer_local_override=True)` which raises the locked:false HALT BEFORE returning (`detection.py:184-199`); pr-submit SKILL:90 loads via `for_arming()` and STOPs "before ... Monitor arming"; pr-submit.md:61 states `for_arming()` "raises before Monitor arming". `--monitor 0` = FSM never leaves `S0_IDLE` (SKILL Wave 0, line 89) / "open PR only" (pr-submit.md:26,34). Canonical sentence `No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.` is BYTE-IDENTICAL at `diagnosis.py:245`, `commands/pr-submit.md:61`, `skills/sc-pr-submit-protocol/SKILL.md:90`. |
| 4 | Ready-state next command consistent across `diagnosis.py::_next_command`, `commands.py::_contract_status_next_command`, docs, and tests (`/sc:pr-submit --monitor 1 --pr <number>`) | PASS | Both functions return `f"/sc:pr-submit --monitor 1{pr_arg}"` for `ContractState.READY` (`diagnosis.py:375`, `commands.py:200`) with identical `pr_arg` construction (`--pr {n}` / `--pr <number>`). Docs match: pr-submit.md:35,61 and pr-submit SKILL:90 ("`/sc:pr-submit --monitor 1 --pr <number>`"). Tests assert `/sc:pr-submit --monitor 1 --pr 42` and `... --pr <number>` for BOTH functions (`test_detection_contract.py:98-107`, `test_contract_setup_diagnosis.py:290-293`). |

---

## Detailed cross-surface verification

### Command-shape convergence (item 1)

Two rendered forms exist, both intentional and internally consistent:

- **Bracketed reference form** (`[--validate]` optional): used in prose that names the one approved readiness command. Byte-identical across `commands/reflect.md` (×2), `commands/pr-submit.md`, and the pr-submit `SKILL.md`.
- **Two-line usage form** (status line + `--validate` line): used in the reflect command doc and reflect skill doc code fences. Byte-identical between `commands/reflect.md:69-70` and `skills/sc-reflect-protocol/SKILL.md:63-64`.

These are two renderings of the SAME surface (`[--validate]` = "the `--validate` line is optional"); they do not contradict.

### State-by-state parity of the two next-command functions (item 4)

Adversarial check: I diffed `diagnosis.py::_next_command(state, repo, pr_number)` against `commands.py::_contract_status_next_command(diagnosis)` for all 9 `ContractState` members (`states.py:11-19`). They are structurally and byte-for-byte equivalent:

| State | Both functions return |
|-------|-----------------------|
| READY | `/sc:pr-submit --monitor 1{pr_arg}` |
| DECLINED_BY_USER | `cancelled: setup declined by user; existing contract files left untouched` |
| VALIDATION_MISSING / VALIDATION_FAILED / STALE / UNLOCKED / EVIDENCE_MISSING | `superclaude reflect contract-status --validate{repo_arg}{pr_arg}` |
| MISSING / UNPARSEABLE (else) | `superclaude reflect contract-status{repo_arg}{pr_arg}` |

`repo_arg`/`pr_arg` placeholder construction (`--repo <owner/repo>`, `--pr <number>`) is identical in both. In `contract-status` execution, the CLI renders `next_command` via `_contract_status_next_command`, while the `Diagnosis.next_command` field is precomputed via `diagnosis.py::_next_command` — both paths agree, so no double-render divergence is possible.

### No-lock-by-default consistency (item 3 support)

The docs claim "does not write the local lock by default". Verified structurally: the `contract-status` command body imports/uses only `write_report` (validation report, `--validate` path), never `write_lock` (`commands.py:104,130`). `write_lock` itself requires `confirmed=True` and raises `ContractSetupRefused` on gate failure (`writer.py:76-98`). No default lock write is reachable from the readiness surface.

---

## Summary

- Checks passed: 4 / 4
- Checks failed: 0
- Contradictions found: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; fix_authorization: false)

## Issues Found

None.

## Confidence Gate

- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 6 | Glob: 0 | Bash: 6
- Every checklist item was verified with direct tool evidence (byte-match greps, Python literal diff of both functions, source reads of `for_arming`, `writer.py`, `states.py`, and the two cross-validating test files). Tool-call count (20) exceeds the 4 checklist items; no padding — each call targeted a specific claim.
- UNCHECKED items: none.
- UNVERIFIABLE items: none.

## QA Complete
