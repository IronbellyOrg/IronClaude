# QA Research Evidence - Builder Research Gate

- **Topic:** Issue 463 preliminary evidence supporting research-task construction
- **Date:** 2026-11-09
- **Phase:** research-evidence
- **Fix cycle:** N/A / 2
- **Template:** /home/coder/.claude/templates/modularization-template-review/qa-research-evidence_report_template.md (filled scaffold)
- **Role:** project .claude/agents/rf-qa.md; evidence-quality lens; fix_authorization: false

## Overall Verdict: PASS

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All five assigned inputs plus construction request read in full | PASS | Read research/research-notes.md:1-112, scope-01-launcher-init.md:1-138, scope-02-launcher-selection.md:1-143, scope-03-proxy.md:1-93, scope-04-contracts-tests.md:1-107, and BUILD-REQUEST.md:1-76. Paths in this table are relative to .dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/. |
| 2 | Claimed source paths exist, not proposed outputs mistaken for evidence | PASS | Glob found all 18 repository source/document/test paths cited by the discovery inputs: 12 under src/superclaude/skills/ccsession-tag/, five tests, and src/superclaude/cli/install_ccsession.py. This exceeds the required 20% path spot check. Later report names are explicitly proposals. |
| 3 | Launcher initialization evidence and documentation labels | PASS | scope-01-launcher-init.md:41-73 cites exact paths/ranges; direct Read of ccsession:134-160 and :861-899 verifies captured permissions, conditional env sourcing/restoration and delegated tier activation. README.md:540-541 agrees with the bounded claim, not blanket immutable permission policy. |
| 4 | Explicit/inherited/default selection evidence and documentation labels | PASS | scope-02-launcher-selection.md:43-71 and scope-04-contracts-tests.md:29-43; direct Read of ccsession:1191-1229 shows inherited named model requires no explicit choice plus in-my-tiers, then model-resolve or default-tier/tier-resolve. README.md:525-526 matches. MODEL-TIERS.md:27-42 cannot prove live role deployment, capability, price or quality and is labeled accordingly. |
| 5 | Proxy documentation claims checked against implementation, not assumed compatibility | PASS | Source-inspected local-gateway-alias-proxy.py:190-221, :299-359, :362-425 and :723-823 support picker/access, aliases, window filtering, cooldown, first-byte/error handling and no alternate attempt after successful stream starts. tests/unit/test_ccsession_tiers.py:898-938 asserts signed-thinking/tool-history preservation; :945-965 includes overloaded HTTP 500. README.md:446-449 is correctly qualified by scope-03-proxy.md:45-50. These are inspected bodies/assertions, not executed behavior. |
| 6 | Helper and regression claims retain actual authority boundaries | PASS | Source-inspected models.py:504-524, :568-624, :381-413 and :459-471 establish environment-derived owner/roles, username/first-role/wildcard precedence and parsed-default-file preference. tests/unit/test_ccsession_tiers.py:3302-3328 asserts inherited-default eligibility and explicit overrides; :2485-2498 asserts user effort-settings preservation. No proof of deployed role assignments or real client settings merge is claimed. |
| 7 | Negative evidence and unsupported assumptions are bounded | PASS | Grep effort/reasoning_effort/output_config/budget_tokens/thinking over ccsession, models.py, ccsession-models.json and local-gateway-alias-proxy.py returned only three proxy display/comment hits and one launcher best-effort comment. This corroborates the bounded absence claims; it does not establish absence in clients, gateway translators or other repository files. ccsession-orca:104-108 recognizes an effort option without choosing it. |
| 8 | Preliminary evidence supports task construction, not completion of later research | PASS | research-notes.md:33-47 attributes discovery claims to scope inputs and explicitly defers candidate selection, Jev identity, provider contracts and measurements. BUILD-REQUEST.md:12-38 requires deeper local investigations, later external research and separate independent gates. Proposed paths are not represented as completed deliverables; unresolved external facts do not block constructing this investigation task. |
| 9 | Execution claims and prior installation incident remain honest | PASS | Every input distinguishes inspected assertions from passing tests or measured production behavior. scope-03-proxy.md:57-63 records the failed searches and unintended environment creation/build/27-package installation; research-notes.md:44 and BUILD-REQUEST.md:53 preserve that disclosure. This review did not repeat the command or inspect secrets, run tests, install, change inputs, or clean up the environment. Historical command output was not independently replayed and is treated as disclosed provenance, not new runtime proof. |
| 10 | This reviewer actually uses a Tier1b backend slot | PASS | Orca worker-show for ctx_745ca4de0b13 reports requested/effective model claude-gw-tier1b. Own transcript /home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-463/efc2e615-ab48-41f2-ab6c-119ca71b676d.jsonl yielded 59 assistant records, unique message.model gpt-6.1-sol, latest timestamp 2026-11-09T03:13:36.030Z. Selective printenv returned T1bModel01 claude-sonnet-5-5, T1bModel02 gpt-6.1-sol, T1bModel03 muse-wonder-full-1.0; registry ccsession-models.json:85-91 binds tier1b to these slots. Thus the observed backend belongs to slot 2; no physical-provider guarantee or product default follows. |

## Summary

- **Checks passed:** 10 / 10
- **Checks failed:** 0
- **Critical issues:** 0
- **Blocking findings:** 0; **Minor findings:** 0.
- **Scope:** Evidence quality for building the research task only. No final research, architecture, live client/provider compatibility, cost, latency or quality acceptance is granted.
- **Evidence basis:** All five assigned research files and BUILD-REQUEST were read fully; every technical conclusion was checked for a concrete cited path/range/name or explicit provenance/uncertainty. All 18 cited repository source/document/test paths exist. Direct source spot checks cover both warning cases, documentation-backed selection/permission/picker/fallback claims, and the effort-settings assertion.
- **Process limitation:** The initial dispatch read and one Orca runtime diagnostic exceeded the requested 40-line output budget; subsequent source reads were bounded. This does not change the evidence verdict. No input files were fixed.

**Self-Audit (zero findings):** Started by looking for fabricated paths, unsupported automatic-effort claims, Tier1b treated as a universal product default, false test-pass/production-compatibility claims and suppression of the installation incident. Glob resolved every identified repository evidence path; direct source reads exposed no contradiction that the notes had failed to flag. The overloaded-500 exception and configurable/default-model distinction are already qualified rather than silently accepted. External sources are explicitly future research, and unrun mock assertions are not promoted into observed behavior. Those checks support zero evidence-quality findings for construction, not a claim that the unfinished deep investigation is defect-free.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|---------------|
| None | N/A | Assigned construction inputs | No blocking or minor evidence-quality defect found within the construction gate scope. | None for this lens; retain all planned deeper investigations and independent gates. |

## Confidence Gate

- **Confidence:** "Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Computation:** 10 / (10 - 0) * 100 = 100.0%, measuring verification coverage of the ten review checks, not certainty of future research results or model quality.
- **Tool engagement:** "Read: 44 | Grep: 6 | Glob: 7 | Bash: 14" at the transcript-count checkpoint, plus 18 source reads through codegraph_node at that checkpoint; follow-up report reads/edits and lifecycle calls are additional. Counts were extracted from tool-name metadata, not estimated. No web tools, tests, package commands or child agents.

**Unchecked items (with reason):**
- None within this evidence-quality construction gate. Runtime execution, external candidate/provider claims and final research acceptance were not requested by this gate and remain future work, not unchecked assertions accepted here.

**Unverifiable items (with blocker):**
- None of the ten review checks is blocked. Live deployment/client/provider behavior, Jev identity, candidate internals, prices/scores and unmeasured outcomes remain explicitly unverified in the inputs and must be resolved or bounded by the later research task.

## QA Complete

Report-only evidence review complete. The supervising coordinator must read this report from disk and combine it with the other independent construction-gate lenses before proceeding.

VERDICT: PASS
