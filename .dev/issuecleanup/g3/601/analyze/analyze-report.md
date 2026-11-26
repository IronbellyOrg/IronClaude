# Architecture analysis: troubleshoot remediation

## Scope and grounding
Command: `/sc:analyze src/superclaude/skills/sc-troubleshoot-protocol --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/601/analyze`.
Static architecture review of the troubleshooting protocol, the narrowest source package that owns issue #601's route. Supporting references and tests were read without running or editing them.
Codegraph: index_state=fresh, checked_at=2026-11-24T13:22:52Z; degraded: graph:empty
The scoped graph layout returned no files. This package is Markdown, excluded by the installed codegraph guide. Used Glob, Grep and Read instead; no graph initialization or source edits.

## Findings and impact
- Requested architecture is present. `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:580-597` selects one plan route at every permitted depth. It preserves explicit acceptance, workflow planning with `--depth standard --handoff none`, consumption of the built-in pre-review, a stop before user-run implement, and user-triggered post-review.
- Safety carry is specified, not runtime-proven here. `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md:93-103` carries the hardening verdict and waiver latch in both source snapshot and tasklist. `src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md:52-56` forbids workflow and implement from upgrading blocked/advisory results. `SKILL.md:588` blocks unattended remediation rather than assuming permission.
- Low severity documentation residue: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:102` describes `task_file_path` as a Tier-3 MDTM file, although line 83 retires that field. This can confuse readers about compatibility; it does not restore the removed route.
- Existing static checks in `tests/troubleshoot/test_hardening_verdict.py:84-126` pin replacement consumers, latch carry, no task-builder call and the user-run boundary. `tests/troubleshoot/test_diagnostic_worker_contract.py:59-68` parses only the plan branch, not the old MDTM heading.

## Metrics and limits
19 Markdown files discovered in the target package. Focused review covered SKILL.md's route and the remediation, hardening and report references, plus supporting route tests. No active MDTM branch or task-builder invocation was found in the route-bearing documents searched. No runtime, tests, build, installer or sync command was run: the dispatch forbids environment creation and writes outside the report directory. Test passing and installed runtime behavior are UNVERIFIED. Merged PR #653 reports historical test/sync results, not fresh verification here. One cross-file search was rejected because its glob used nested alternatives; later individual-path searches replaced it.

Report authoring initially hit the freshness hook because Write does not register a tracked Read. Read the stubs and resumed through Edit; no bypass was used.

## Recommendations
Do not rebuild the route: it already exists. Reconcile the retired-field description and check the issue's explicitly named documentation before proposing closure. Preserve acceptance, hardening carry and no-auto-execution boundaries. Implementation and GitHub changes are outside this task.
