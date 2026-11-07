# Round 2: Variant 2 rebuttal (haiku, qa)

Persisted by the orchestrator on receipt, 2026-11-06T22:05:15Z. Citation keys: P = the plan, S = source.md, T = tests/skills/test_worker_contract.py.

## Response to criticisms

Steelman: Variant 1 is right that Task 5's phrase check does not reject the old status rule, and QA-1 is a separate false-pass gap in Task 4 (P:66-70, 76-80).

1. Task 5 clean claim WITHDRAWN. `_artifacts_clause` returns everything after the first `artifacts` token on its line; existing checks ban "failed tool run" and "on a failed run" (T:769-774, 783-797; init-lite.md:92). P3 wording precaution: the existing test catches the prohibited wording.
2. QA-1's report-location demand WITHDRAWN. The brief centralizes that duty in WC-4 (S:13, 19; P:69). Keep the local exclusion relationship, WC-4 reference and `[]`.
3. QA-1 stays P1, narrowed: a clause listing ignored coverage output satisfies WC-4, `[]` and no-write-verb checks while contradicting the AC (P:66, 69). Bounded repair: require "left out" alongside the pointer, as build/workflow (T:798-808).
4. QA-2 stays P3; replace the misleading criterion with relevant verification (P:30, 35; T:1054-1064, 573-574).

## Response to Variant 1's grading rule

AMEND. Use:
- P1: the planned assertion is shown to accept text violating the requirement it protects, or an implementation blocker is shown. Wrong placement does not automatically escape P1.
- P2: a coverage or interpretation defect without a shown false pass (for example an ambiguous instruction that could produce either a scoped or a whole-file assertion).
- P3: cosmetic guidance, owner note, or an irrelevant verification claim with no shown failure of a required outcome.

| Finding | Grade | Reason |
|---|---|---|
| R1-1 | P1 | "exited 0" can coexist with the audit-only success rule (P:76-79; S:24-27) |
| QA-1 | P1 | Admits an ignored-output listing contradicting AC1 (P:66, 69) |
| R1-4 / R3-3 | P2, conditional P1 | Plan says "WC-4 text", not whole-file; ambiguity shown, not the faulty implementation (P:30, 33; T:383-394) |
| QA-2 / R1-3 / R3-2 | P3 | Scan irrelevant to the core file (P:30, 35; T:1054-1058) |
| R1-6 | P3 | Misplacement fails, does not falsely pass (T:769-774; P:66) |

AC review (sc-implement-protocol/refs/qa.md:7-17, 27-31, 49) mitigates but does not erase a shown planned-test false pass.

## Updated assessment of other variants

- V1 strongest on status correctness: tests/cli/test_init_lite.py:238-261 shows non-zero exit after one scaffold write; init_lite.py:348-359 writes the report before scaffold writes.
- V3 strongest on omitted scope: S:14; P:30; orca-worker-contract-spec.md:72. P2 for the unaddressed check, without assuming the spec must be rewritten.
- Accept V1's narrowed workflow finding (P:30, 43; sc-workflow-protocol/refs/return-contract.md:51-52; SKILL.md:60-62).

## New evidence

- Static QA-1 witness: "lists `htmlcov/`; see WC-4; `[]` when none" passes Task 4's three checks (no WRITE_VERB_RE hit, T:1062-1064) while listing excluded output. Not executed.
- Boundary correction: SKILL.md:61 `worker_status` precedes `artifacts`; init-lite.md:92 status follows it. A status check confined to `_artifacts_clause` cannot protect both files.

## Updated per-point positions

| Point | Superior | Reason |
|---|---|---|
| S-001 | Tie | Presentation only |
| C-001 | V1 | Contract-reading verification; P3 (T:573-574, 1054-1058) |
| C-002 | V1/V3 tie | P2 ambiguity, conditional P1 |
| C-003 | V1 | Narrowed compliance gap, P2 |
| C-004 | V2, narrowed | P1 |
| C-005 | V1 | Phrase presence does not reject the old rule |
| C-006 | V3 | Spec-copy check requested |
| C-007 | V3 | Valid, non-gating |
| C-008 | V3, qualified | Command source-path leak already guarded (T:501-517) |
| C-009 | V1 | Partial-write evidence |
| C-010 | Tie | Outside the three follow-ups |
| X-001 | V2/V3 synthesis | Test local exclusion; reporting stays in WC-4 |
| X-002 | V1/V3 | P3 |
| X-003 | V3 | Spec-copy consistency requested |
| A-001 | Tie | Corrections need an authorized route |
| A-002 | Tie | AC review mitigates, does not cure |
