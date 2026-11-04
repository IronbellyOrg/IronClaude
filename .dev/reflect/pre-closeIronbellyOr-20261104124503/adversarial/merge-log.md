# Merge Log

## Metadata

- Base: Variant 3 (reviewer-3, opus, refactorer), `variant-3-original.md`
- Plan: `refactor-plan.md` (12 planned changes, 5 rejected)
- Executor: merge-executor
- Output: `merged-verdict.yaml`
- Changes applied: 12 of 12
- Status: success (no failed, no skipped, no escalations)
- Timestamp: 2026-11-04T13:25:58Z

## Changes Applied

Changes were applied in plan order.

| # | Status | Before | After | Provenance |
|---|--------|--------|-------|------------|
| 1 | Applied | `verdict: revise` (1 blocking, 8 minor) | `verdict: needs_revision`, driven by M-1 | Variant 1 verdict; S-002 |
| 2 | Applied | No bare-`/ponytail` finding | M-1 inserted as first finding: plan:80 "bare /ponytail switches to full" is false under lite. Class drift, blocking. Evidence `/tmp/ponytail-src-t14b/mode-tracker.js:109-119` plus Variant 1's other two citations. Instruction includes the INV-002 `full`-if-default-is-`off` wording. | Variant 1 R1-F1; C-001, X-001; INV-002 |
| 3 | Applied | No mode-switch scope finding | M-2 inserted as second finding: plan:80 "switches every session in that repo until a new session starts there" is wrong in scope. Class drift, blocking. Evidence: the four INV-001 citations. Instruction: per project directory, any new session, `/clear` or resume resets it, other sessions see it only in subagents. | invariant-probe INV-001 |
| 4 | Applied | R3-1 `severity: blocking`, `env -u CLAUDE_CONFIG_DIR -u XDG_CONFIG_HOME` | R3-1 `severity: minor` (with a comment: both variables verified unset 12:48Z). Instruction extended to `-u PONYTAIL_DEFAULT_MODE -u PONYTAIL_MAP -u PONYTAIL_SUBAGENT_MATCHER HOME=<throwaway>` and a log line that none is set. The INV-016 citations (`hooks_ponytail-config.js:85`, `activate.js:66`, `subagent.js:35`) were added as evidence for the extension. | Variant 1 R1-F2 calibration; C-002; INV-016 |
| 5 | Applied | R3-2 recommendation: `numstat <= 5 insertions and <= 5 deletions, all inside install_plugins` | Same rule kept; recommendation prefixed as an implementation-time instruction; class `grounding_gap: counting rule` | C-003 |
| 6 | Applied | R3-4 recommendation: run `uv run pytest tests/docs` and markdownlint | Recommendation made concrete: after Task 3, run `uv run pytest tests/docs -v` (citing `test_retired_docs_absent.py:41,44`, `test_tavily_doc_alignment.py:45,117`) and markdownlint on `docs/getting-started/installation.md` (`.pre-commit-config.yaml:73-88`). The two new citations were added to the evidence list; base citations unchanged. | C-004, X-002 |
| 7 | Applied | R3-5: AC "every behaviour claim matches the lite facts" cannot hold; reset clause grounded only on the off path | R3-5 restated: reset clause and "PONYTAIL DEFAULT SET" now grounded (`activate.js:193,55`, `mode-tracker.js:71`); the two remaining unsourced claims are "a project .claude/settings.json wins" (plan:81) and "do not only run claude plugin uninstall" (INV-014, `install_user_setup.py:266`). Instruction: source each from Claude Code docs or drop it. | Variant 3 Round 2; INV-014 |
| 8 | Applied | No docs-accuracy finding | M-3 inserted (minor, `grounding_gap`): the six instructions for INV-003, -004, -006, -008, -009, -013. | invariant-probe INV-003, -004, -006, -008, -009, -013 |
| 9 | Applied | No Known Limitation finding | M-4 inserted (minor, `grounding_gap`): the Known Limitation sentence must say the extra clone can also push the other default plugins past the 30 s budget. Evidence `install_user_setup.py:272-284` and `:35,290-293`. | invariant-probe INV-005 |
| 10 | Applied | No coverage block | `coverage` block added: the eight containment-unmapped rows are all owned by plan elements; the goal span is covered at plan:15, 39, 82; T5 fails on unfixed code. Conclusion: accept coverage as complete. | Variant 2 R2-F1, R2-F2, coverage_check; C-005 |
| 11 | Applied | R3-8: proof does not belong in the CHANGELOG task; Orca step can use 25 s of 30 s | R3-8 reduced to diagnostics: the proof stays in Task 4; record whether Orca was on PATH and the time used. `grounding_gap` renamed to "proof budget diagnostics". | X-003 |
| 12 | Applied | No version-scope note | `notes` entry: docs and CHANGELOG say behaviour was checked against Ponytail v5.3.3; M1 records the installed plugin version. | A-001 (QUALIFY, unanimous) |

### Changes not made (per plan)

S-002 (Variant 2 verdict `pass`), C-003 (Variant 2 rule `<= 4 ins / <= 3 del`), C-006 (move proof to its own task), C-008 ("reset clause unsourced"), C-009 (R3-3 dependency change). None was applied. R3-3 stays as in the base, with only the recommendation worded as an implementation-time instruction ("run sequentially as written").

### Unchanged base content carried over

R3-6, R3-7 and R3-9 are verbatim from the base (source label added). `scope_check` is kept from the base card. `reviewer`, `persona`, `model` and `self_reported_confidence` were dropped because they describe a single reviewer and are replaced by `merge_method` and `base_variant`. `verified_adherent` was not carried over: it is a single-reviewer assertion that the plan does not name in any change.

### Judgment calls inside the plan's scope

- M-2 and M-1 `deviation_class: drift`: Change #3 gave no class; drift matches M-1 and the nature of the finding (a plan claim that is false).
- Upstream citations are kept in the form each source used (for example `activate.js:...` in some, `hooks_ponytail-activate.js:...` in others); a YAML header comment says both name the files under `/tmp/ponytail-src-t14b/`.
- The "plan" in claims is `TASK-WF-closeIronbellyOr-20261104-124207.md`; the YAML header comment defines this.
- R3-3's recommendation was reworded from "Sequential execution is still safe; no change needed to run." to an implementation-time instruction with the same meaning.

## Post-Merge Validation

| Check | Result |
|-------|--------|
| YAML parses | PASS. Reviewed by hand, then parsed with PyYAML `safe_load` via `uv run python -I`; no file was written by the check. Top-level keys: merge_method, base_variant, convergence_score, invariant_gate, verdict, scope_check, findings, coverage, notes. |
| Required header comments | PASS: `# Provenance: produced by /sc:adversarial`, `# Base: Variant 3 (opus:refactorer)`, `# Merge date: 2026-11-04T13:25:58Z` are the first three lines. |
| Required top-level values | PASS: `merge_method: adversarial`, `base_variant: "opus:refactorer"`, `convergence_score: 1.0`, `invariant_gate: BLOCKED_BY_INVARIANTS` (comment names INV-001 carried as M-2). |
| Every finding has id, source, claim, evidence, class or gap, severity, recommendation | PASS: 13 findings (M-1, M-2, R3-1 to R3-9, M-3, M-4); parse check confirmed all fields present on each. |
| Severity values | PASS: blocking = M-1, M-2; minor = the other 11. The verdict comment ("2 blocking, 11 minor") matches. |
| Recommendations phrased as implementation-time instructions | PASS: each begins "When implementing / running / checking / After Task 3" or is an imperative ("Use ...", "Link ...", "Accept ..."); none asks for a plan edit. |
| Evidence citations kept exactly as in source | PASS for all base and variant citations. Additions beyond the base are limited to those named by the plan's changes (Changes #4, #6, #7, #8, #9). Citations such as `test_tavily_doc_alignment.py:45,117` keep the form the plan used. |
| No new contradiction versus the variants | PASS. No finding says `pass`. R3-1 is `minor`, not blocking, and the only R3-1 blocking text is in a comment recording the downgrade. The only blocking findings are M-1 and M-2. The notes line stating Variant 2's `pass` is not adopted agrees with the verdict. The coverage block says the matrix gaps need no plan change, which does not conflict with M-1 or M-2 (they concern Task 3 docs wording). |
| No finding outside the plan | PASS: the findings are the base's R3-1..R3-9 plus M-1..M-4 named by Changes #2, #3, #8, #9. |
| Open item (not a contradiction) | INV-007, INV-010 and INV-015 (LOW) appear in the probe but in no planned change, so they are not in the merged card. |

## Summary

- Planned: 12
- Applied: 12
- Failed: 0
- Skipped: 0
- Rejected by plan (not applied, as instructed): 5
- Output files: `merged-verdict.yaml`, `merge-log.md`
