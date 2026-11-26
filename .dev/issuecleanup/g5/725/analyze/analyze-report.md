# Architecture analysis for issue 725

## Scope and method
Command: `/sc:analyze src/superclaude/core --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g5/725/analyze`.

Checked on 2026-11-24 at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. The narrowest common source directory for the two requested rule surfaces is `src/superclaude/core`. Supplemental searches covered launch-related text in source commands, skills and CLI, the distribution guide, tests, hooks and design notes. No source changed; no runtime tests, environment creation, installation or GitHub writes ran.

Codegraph: index_state=fresh, checked_at=2026-11-24T14:15:26Z; degraded: graph:empty

Graph discovery returned only the core Python initializer; the Markdown guide lookup returned no indexed file. Markdown is not indexed, so source reads and text searches supplied the evidence. Augment semantic search returned unrelated orchestration material, not a coordinator launch builder; it was not used to prove absence.

## Findings
1. **Medium: the required routing rule is absent.** The complete Orca coordination section at `src/superclaude/core/HOW-WE-WORK.md:352-362` describes workers, sweeps and outward-action ownership, but contains no peer discovery, read-only question or human-fallback rule. Issue #725 remains OPEN with no comments in the live read. Its six rules are not implemented by this section.
2. **Medium: the shared contract lacks the peer boundary and template.** `src/superclaude/core/WORKER-CONTRACT.md:69-92` starts the coordinator duties; full-file searches for `peer`, `another project`, `cross.project` and `read.only question` found no match. Existing approval and worker ownership rules do not substitute for the requested peer-first rule, receiving-side refusal or question template.
3. **Medium: coordinator launch coverage remains unresolved, not disproved.** Searches in source commands, skills and CLI did not identify a coordinator standing-launch builder. `src/superclaude/cli/issue_pipeline/brief.py:1-9,52-80` explicitly builds worker Task briefs, not coordinator launches. `docs/designs/issue-watcher-zero-setup-coder-handoff.md:11-13,51-53` places the standing coordinator prompt in the Coder-side handoff tied to Coder issue 516. The actual builder and its current output are UNVERIFIED under this task's repository-read boundary.
4. **Existing tests can be extended, but do not prove delivery.** `tests/skills/test_worker_contract.py:907-909,1073-1080` tests required phrases and their removal. `tests/core/test_how_we_work_routing_table.py:329-334` preserves guide ASCII text. Searches of these test files found no peer rule. This is static test inspection only, not a test run.

## Recommendations and limits
Keep #725 open. Implement the bounded rule and regression checks, keeping the plugin guide copy aligned; obtain the actual coordinator-launch builder paths and tests before claiming that acceptance criterion complete. Do not extend cross-project supervision, introduce a fixed waiting time, or treat peer replies as approval.

Discovery method, wake-up behavior, permission-mode holding and hook enforcement remain research questions. Hook text search found no direct peer-rule match, which is not proof that no general guard applies. No external Coder issue reads or cross-project messages were made. GitHub searches for `725` and for `peer` plus `coordinator` did not identify an implementing PR; the former returned unrelated PR #628 and the latter returned adjacent default-wording PR #508. Search completeness is UNVERIFIED, and no absence claim relies on these searches. A shared-rate-limit warning appeared during related-issue reads; further main-session GitHub reads were stopped, so live details of adjacent PRs and external Coder issues remain UNVERIFIED. The report recommends no GitHub writes.
