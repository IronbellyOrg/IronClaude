# Merge Log

## Metadata
- Base: Variant 3 (option-c, original), `variant-3-original.md`, score 0.896
- Plan: `refactor-plan.md` (12 changes; "Changes NOT Being Made" honoured)
- Executor: merge-executor (sc:adversarial Step 5)
- Output: `../P2-installer-contract-merged.md`
- Changes applied: 12 of 12
- Status: COMPLETE
- Timestamp: 2026-10-29

## Changes
Line numbers refer to the merged file.

| # | Change | Status | Where in merged file | Provenance tag |
|---|---|---|---|---|
| 1 | Phase banner and failure output | applied | Phase, line 11 | L1 forced round + V2 U-004 |
| 2 | Doctor `codegraph MCP registration` (shutil.which, unknown on unreadable `~/.claude.json`, rationale downgraded) | applied | Doctor, lines 19-21 | C-002 majority, INV-007, INV-008, U-001 |
| 3 | Owned-entry test replacing the env/headers refusal | applied | Phase, line 13 | A-001 + INV-005 |
| 4 | User-managed entry kept or failed with the remove command | applied | Phase, line 14 | INV-006 |
| 5 | Whole-entry matcher | applied | Phase, line 15 | INV-014 |
| 6 | Receipt as a list, written only after a verified download, corrupt receipt rule | applied | Receipt, lines 28-29 | A-002 + INV-010 + INV-011 |
| 7 | Acquisition safety (temp dir then rename; never overwrite unlisted paths; link ownership) | applied | Phase, line 12; Receipt, line 29 | INV-003 + INV-004 |
| 8 | Old version dirs, reference-based deletion replacing the `daemons/` lookup | applied | Old version dirs, lines 32-33 | C-005 + INV-001 |
| 9 | Fixed candidate order; `--list` prints owned/external and resolved link paths | applied | Phase, line 12; Removal, line 25 | INV-002 |
| 10 | Platforms: 4-entry map, named failure | applied | Phase, line 16 | INV-012 |
| 11 | Coder prerequisites and `timeout 60` note | applied | Coder prerequisites, lines 39-40 | INV-015 + INV-009 |
| 12 | Size estimate about 300 lines, about 33 tests | applied | Size, line 36 | base-selection "weaknesses to fix" |

Base content kept: required phase and exit 1 (Phase), advisory doctor (Doctor), documented removal and `--list` ownership examples (Removal). Base content dropped per plan: the `~/.codegraph/daemons/` lookup, the "breaks every Claude session" rationale, the 170-line estimate, the Strengths/Weaknesses sections (superseded by Debate result and Incorporated).

## Post-merge validation
- Heading hierarchy: one H1 (line 1), ten H2 sections in the required order (Phase, Doctor, Removal, Receipt, Old version dirs, Size, Coder prerequisites, Debate result, Incorporated from the losing options, Rejected). No skipped levels. PASS.
- Internal references: `context.md` exists in `P2-installer-contract/`. Source citations `main.py:264-275`, `install_mcp.py:867-873`, `install_mcp.py:486-496`, `update.sh:2,8,10`, `Makefile:42` match the debate transcript and plan. Section cross-reference "Old version dirs rule" (Debate result) resolves to an H2. PASS.
- New contradictions vs. debate outcomes: none found. Doctor reports a missing entry (V2+V3 majority; A's dissent recorded, not adopted). No uninstall flag anywhere. Phase stays fatal. The `daemons/` lookup appears only in Rejected and in a provenance comment. Rejected items in "Changes NOT Being Made" do not appear as adopted content. PASS.
- Line count: `wc -l` on the merged file = 52 (limit: under 60). PASS.

## Summary
- Planned: 12
- Applied: 12
- Failed: 0
- Skipped: 0
