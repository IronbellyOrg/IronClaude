# Round 1: Variant 3 Advocate (opus, refactorer)

**Position summary.** Variant 3 is the only card that holds the plan to its scope rules and to the source's "every test that reads the edited files" check. Its blocking point (R3-1) is real but over-rated. Variant 1 found the most important single defect (false bare-/ponytail claim) which Variant 3 missed; the merged verdict should be "revise", carrying R1-F1 plus R3-4 and R3-1.

**Steelman V1.** Checked behaviour claims against upstream and found plan:80 false (`mode-tracker.js:109-119`: on = report only; off = getDefaultMode() = lite; full only when default is off); rated CLAUDE_CONFIG_DIR conditionally. Critique: misses XDG_CONFIG_HOME, the unowned docs tests, and its counting rule leaves deletions unbounded.

**Steelman V2.** Most disciplined coverage audit; explains every unmapped row; checks T5 fails on unfixed code; treats AC-M placement as conformant. Critique: `pass` and "no false claims" contradicted by `mode-tracker.js:117`; "every check owned" wrong (`tests/docs/test_retired_docs_absent.py:40-41` and `tests/docs/test_tavily_doc_alignment.py:13,117` scan docs/**); upstream facts "taken as given"; 4/3 counting rule false-fails a wrapped line.

**Strengths claimed.** (1) R3-4: plan:67 runs only tests/cli + tests/unit; two tests/docs files read installation.md; `.pre-commit-config.yaml:73-88` runs markdownlint --fix on it. (2) R3-1 adds XDG_CONFIG_HOME (`hooks_ponytail-config.js:55-56`); one `env -u` prefix covers both. (3) scope_check shows constraints obeyed. (4) R3-6 JSON expanded form (`user_settings_defaults.json:36-49`). (5) R3-2 counting rule safest (<= 5 ins and <= 5 del inside install_plugins).

**Weaknesses in others.** V2 verdict wrong; docs tests marked owned; 4/3 rule too tight. V1 misses XDG and docs tests; deletions unbounded.

**Concessions.** Missed C-001 as a factual error (R1-F1 should be the blocking item). R3-5 reset clause withdrawn: grounded by `hooks_ponytail-activate.js:193,55`. R3-1 not blocking (variables unset); minor defensive `env -u`. R3-8 "move task" unnecessary; keep only "record Orca on PATH and time used". R3-3 low value.

**Per-point positions.** S-001 equal; S-002 1=3; C-001 1; C-002 3 content / 1 severity; C-003 1=3; C-004 3; C-005 2; C-006 2; C-007 equal; C-008 3 (partly); C-009 3 (informational); C-010 3; C-011 3; X-001 1; X-002 3; X-003 2.

**Shared assumptions.** A-001 QUALIFY: valid for v5.3.3 only; docs should carry a "checked against v5.3.3" note as the CHANGELOG does (plan:99). A-002 ACCEPT: every recommendation becomes an implementation-time instruction (Task 3 wording; Task 4 `env -u CLAUDE_CONFIG_DIR -u XDG_CONFIG_HOME`; add `uv run pytest tests/docs` and markdownlint), not a plan edit.
