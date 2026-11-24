# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | The C-003 default-detection rule (lens mode, or post-preflight template equals current lens default with no caller compare_files) cannot catch a sibling lens | UNADDRESSED | MEDIUM | After Task 2 (plan:47) refactor-find's template equals edge_case_hunt.py:53 byte for byte; an equality clause read as "the run's own lens default" is true for every lens; rule needs an explicit lens-is-refactor-find condition (lens name at commands.py:2152) or edge-case-hunt loses its `<existing-review>` prefix (commands.py:2141-2144), breaking plan:21/plan:69; plan:69 sibling test should cover edge-case-hunt in spec/stdin mode |
| INV-002 | guard_conditions | The `--lens` mode clause never conflicts with a caller template or substitutions | ADDRESSED | LOW | SPEC_PATH, --stdin and --lens mutually exclusive (commands.py:1107-1117); no run option sets template/substitutions; lens mode builds empty substitutions (commands.py:929-930) |
| INV-003 | state_variables | Local `mode == "lens"` reliably marks a lens-default run | ADDRESSED | LOW | `--lens X --detached` relaunches as `swarm run <snapshot_path>` (commands.py:1297-1304), so child mode is spec-file; only the OR'd equality clause covers it; a mode-only implementation breaks detached runs; plan:64 lists no detached case |
| INV-004 | sufficiency_challenge | Quoting the whole list with shlex.quote and parsing with shlex.split in tests makes the suggestion acceptable to the real consumer | UNADDRESSED | MEDIUM | Consumer only splits on commas plus existence checks (sc-adversarial-protocol SKILL.md:562-565; adversarial.md:15,39,58), no quote stripping; a `'...'` wrapper may survive into first/last path; a shlex.split test proves producer intent, not consumer acceptance; shlex.quote also quotes non-ASCII and `~`; V3 card (double quotes, v3:17) and final proposal (single quotes) disagree |
| INV-005 | interaction_effects | Adding quoting will not change sibling output | UNADDRESSED | LOW | Shared setdefault at commands.py:2141-2144 serves every lens; quoting there would change sibling output for paths with spaces; bare-review golden (tests/swarm/fixtures/bare_review_v1/golden/all-success/return-contract.yaml:28) uses ordinary paths, so no test would catch it; fix should confine quoting to the refactor-find default branch |
| INV-006 | count_divergence | The eight active stale mentions are the complete set | ADDRESSED | LOW | Repo-wide grep (excluding .git, .dev, .claude, .venv) returns exactly the eight; sc-bare-review/SKILL.md:21 separate and out of scope; nothing in KNOWLEDGE.md, HOW-WE-WORK.md or plugins mirror. Note: a literal `code-review` grep also returns docs/dev/lens-contribution-policy.md:190, agents/reuse-auditor.md:3,16, reflect/ensemble.py:77, tests/pr_submit fixtures, docs/testing/v6.0.0/post-release-report.md:170; documentation-check.txt must give each a disposition or narrow the pattern |
| INV-007 | interaction_effects | The Blocking fix (two skill refs and one command definition added to Task 4) fits the plan's other constraints | UNADDRESSED | MEDIUM | Plan:20 limits edits to two production files plus "the matching current documentation named below"; the new targets are installed primitives (test_cli_install.py:99, 262-264); Task 4 title (plan:75) and plan:84 still say "three"; consensus fixes plan:79, :81, :84 count but leaves plan:20 and the "three" wording, so an executor could read the wizard edits as a plan:20 breach. No sync-dev needed (.claude copies absent); plan:26 no-staging rule holds |
| INV-008 | collection_boundaries | "Successful usable reports" (plan:62) equals the existing succeeded_final_paths filter | UNADDRESSED | LOW | final_path set for every worker before normalization (commands.py:1073); file written only when result.text non-empty (normalize.py:456-457); filter checks only status success and non-empty path string (commands.py:2129-2133); a success with empty body counts toward the two-report guard without a readable file; plan:68 checks readability in tests only |
| INV-009 | sufficiency_challenge | The resume refutation leaves nothing user-facing behind | UNADDRESSED | LOW | Resume passes no template (commands.py:2578-2586) so suggestion is empty (reduce.py:460-461); after the fix a fresh run suggests --compare and a resumed run suggests nothing; Task 4 (plan:79) documents only "too few successful reports" as the empty-suggestion reason |
| INV-010 | sufficiency_challenge | Fixing the eight mentions makes wizard and docs agree with "comparison, does not change application code" (plan:79) | UNADDRESSED | LOW | Goal text "Find small safe cleanups I could apply" (interview.md:15, wizard-guide.md:63) now points to a comparison-only follow-up; defensible as goal text, but documentation-check.txt should record it as a deliberate keep |

Fault-finder: general-purpose agent affe001e09f6db0a7, inherited model (identity unverified), read-only. Rows recorded from its returned text, condensed. No branch-trace.md exists; sufficiency evidence is source enumeration. The agent's own header said "4 Medium, 6 Low"; its listed rows contain 3 MEDIUM and 7 LOW, and this table records the rows as listed.

Sufficiency answer recorded: nothing found makes the FAIL verdict or the Blocking finding wrong; downstream conditions that would falsify the consensus fixes as written: equality-only default check reroutes edge-case-hunt (INV-001); consumer keeps shlex quote characters in paths (INV-004); wizard edits flagged as a plan:20 breach (INV-007).

## Summary

- **Total findings**: 10
- **ADDRESSED**: 3 (INV-002, INV-003, INV-006)
- **UNADDRESSED**: 7
  - HIGH: 0
  - MEDIUM: 3 (INV-001, INV-004, INV-007)
  - LOW: 4 (INV-005, INV-008, INV-009, INV-010)

Invariant gate: count(HIGH + UNADDRESSED) = 0, convergence not blocked. WARNING: 3 MEDIUM-severity UNADDRESSED invariant(s) detected. Items: INV-001, INV-004, INV-007. These do not block convergence; they are carried into the refactor plan as merge changes.
