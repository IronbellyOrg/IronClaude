# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis

Fault-finder: independent general-purpose agent (opus slot), read-only, 2026-11-06T22:12:40Z. Persisted by the orchestrator on receipt. Input: emerging consensus after Round 2 (16/16 points agreed), Round 1 and Round 2 transcripts, diff-analysis.md.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Asserting "exited 0" present and "when the audit finished" absent stops the old status rule returning | UNADDRESSED | MEDIUM | Synonyms ("succeeded once the audit finished", "if the audit finished") pass; "audit finished" cannot be banned outright because the new wording keeps "(the audit finished and every requested scaffold write succeeded)" (plan :76, source.md:25). Fix: pin the exact positive phrase "`succeeded` when `superclaude init-lite` exited 0", as RULE_PHRASES does (test_worker_contract.py:102-108). |
| INV-002 | sufficiency_challenge | A whole-text "exited 0" check on SKILL.md protects the `worker_status` rule | UNADDRESSED | LOW | "exited 0" anywhere (e.g. near SKILL.md:63) passes; scope to the line carrying `worker_status` (SKILL.md:61) and to init-lite.md's Contract line. |
| INV-003 | sufficiency_challenge | Pinning "left out" + "WC-4" + `[]` + no write verb stops a test.md clause listing `htmlcov/` | UNADDRESSED | MEDIUM | "every other file written, `htmlcov/` and `.coverage` included (nothing is left out; WC-4); `[]` when nothing else was written" passes (V3 conceded gaming, round-2-variant-3.md point 4); same weakness in build/workflow pins (:799, :808). Fix: pin an exact phrase such as "paths git ignores are left out", or assert no coverage path precedes "left out". |
| INV-004 | state_variables | `_artifacts_clause` reads the intended line; R1-6 "can only fail" | UNADDRESSED | LOW | First backticked `artifacts` or `artifacts:` line wins (test_worker_contract.py:769-774); an R3-5 pointer placed above return-contract.md:52 with a backticked `artifacts` would hide the YAML line from the check. |
| INV-005 | interaction_effects | "Report-location wording out of per-command text" and "WC-4 report sentence made conditional" both hold | UNADDRESSED | MEDIUM | With a conditional WC-4 sentence, test.md no longer says the coverage output is named in the report, which source.md:19 requires; build likewise if Task 3 drops build.md:104's sentence (plan :54 silent). Fix: commands whose report names the files keep one short local sentence, or WC-4 names workflow as the only exception. |
| INV-006 | interaction_effects | The executor can apply corrections in-task | UNADDRESSED | MEDIUM | The WC-4 wording is an owner decision (source.md:13 asks for the unconditional sentence; Task 1 at plan :30 tells the executor to write it); /sc:workflow cannot edit the plan (sc-workflow-protocol SKILL.md:62). The decision blocks Task 1, and Tasks 2-4 depend on Task 1. |
| INV-007 | interaction_effects | The new global WC-4 exclusion does not conflict with init-lite's `artifacts` rule | UNADDRESSED | MEDIUM | init-lite.md:92 and SKILL.md:61 list every printed `Scaffold:` file with no exclusion; `--project-root` accepts any directory (init_lite.py:294-298, :338); `.dev/` may be ignored in other projects. Fix: one WC-4 sentence that its exclusion applies to every command's list (also covers index-repo.md:189). |
| INV-008 | sufficiency_challenge | WC-4 slice plus two tokens proves the rule | UNADDRESSED | LOW | Slice markers verified (WORKER-CONTRACT.md:31 only "- **WC-4."; :38 WC-8). Assertion ignores polarity; add the phrase to RULE_PHRASES["WC-4"] so `test_rule_check_fails_when_rule_removed` (:586-593) covers it. |
| INV-009 | sufficiency_challenge | `test_every_repo_setup_line_is_gated` (:573) meaningfully replaces Task 1 AC3 | UNADDRESSED | LOW | It reads only lines with setup flags or launcher spans (:429-460); a WC-4 sentence has none. Real guards: WC-4 phrase pins (:102-108) and the slice assertion. |
| INV-010 | count_divergence | Excluding specs/history/ gives a clean search, and the spec decision gets recorded | UNADDRESSED | LOW | ~20 frozen hits also in .dev/tasks/done/, .dev/orca-command-refactor/decisions/, .dev/reflect/; live copies are src/, plugins/, tests/ and the one spec. Name where the decision is recorded (progress.md or commit body). |
| INV-011 | collection_boundaries | "`[]` when nothing else was written" is accurate for test.md | UNADDRESSED | LOW | A `--coverage` run writing only ignored files (.gitignore:37, :40, :44, :48) wrote files yet ends with `[]`; say "when nothing else listable was written". Build has the same edge. |
| INV-012 | guard_conditions | New init-lite.md wording avoids the :792 bans and keeps :795-796 | ADDRESSED | LOW | Consensus names both bans; residual: exact-phrase bans miss "`[]` when the tool failed" (pre-existing). |
| INV-013 | state_variables | Edited lines leave no stale write-verb classification entries | ADDRESSED | LOW | No WRITE_VERB_RE match on any edited line today (:1062-1065); residual: plan :21 covers only command-section text, but return-contract.md under skills/ is scanned too. |
| INV-014 | count_divergence | Only workflow files need plugin byte-copies; cited line numbers current | ADDRESSED | LOW | build/test plugin copies differ and have no Unattended section; no init-lite plugin copy; all cited lines match cb8f2f81. |
| INV-015 | collection_boundaries | "succeeded when exited 0" is right in init-lite edge runs | ADDRESSED | LOW | --dry-run exits 0 with `[]` (init_lite.py:348-352); existing scaffold skipped, exit 0, `[]` (:276-277); report refusal ClickException (:247-262); residual: scaffold OSError (:278) gives a traceback in `reason`. |
| INV-016 | guard_conditions | An exit code always exists for the init-lite status rule | UNADDRESSED | LOW | SKILL.md:63 only prefers the CLI; without it "exited 0" is undefined. Say the tool's exit code is the only basis for `succeeded`. |

## Summary

- **Total findings**: 16
- **ADDRESSED**: 4
- **UNADDRESSED**: 12
  - HIGH: 0
  - MEDIUM: 5 (INV-001, INV-003, INV-005, INV-006, INV-007)
  - LOW: 7 (INV-002, INV-004, INV-008, INV-009, INV-010, INV-011, INV-016)

Invariant gate: no HIGH + UNADDRESSED item, so convergence is not blocked.
WARNING: 5 MEDIUM-severity UNADDRESSED invariant(s) detected. Items: INV-001, INV-003, INV-005, INV-006, INV-007. These do not block convergence; they are carried into the refactoring plan.
