# QA Report — Research Depth

**Topic:** Final MCP hardening research readiness
**Date:** 2026-09-11
**Phase:** research-depth
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

The research now resolves the previously unknown Serena launcher, Morph successor, and key-preserving compatibility choices. It is nevertheless not execution-ready: its claimed exhaustive direct-document disposition excludes active project documentation that still gives the deprecated Serena command, and its Tavily test plan omits source/docstring/eval literals that the mandatory scan will fail on. The stated baseline policy for the pre-existing sync failure is otherwise usable.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Selected vendor commands are evidence-backed | PASS | `research/03-official-releases.md:10-14`, `05-serena-launcher-gap-fill.md:5-19`, and `06-morph-migration-gap-fill.md:7-24` specify the five selected commands. Tavily-first extraction independently confirmed Tavily 0.2.22, Serena 1.7.0, Auggie 0.36.0, and MorphMCP package availability; `research/08-scope-dispositions.md:10-14` supplies a consolidated command table. |
| 2 | Same-name command migration preserves client compatibility | PASS | `research/06-morph-migration-gap-fill.md:7-15` retains `morphllm-fast-apply`; `install_mcp.py:623-685` reconciles command drift only after exact lookup of that same registration name. The successor launcher can therefore replace Fast Apply without an unimplemented cross-name removal. |
| 3 | Root Auggie configuration preserves required namespace | PASS | `research/07-config-ownership-gap-fill.md:70-94` retains `auggie-mcp` while changing only launcher tokens. The root file currently uses that key (`.mcp.json:2-10`), and hooks/eval consumers explicitly preserve it per the targeted `git grep` inventory. |
| 4 | Required direct documentation scope is complete | FAIL | Although `research/08-scope-dispositions.md:20-26` says *every* current project-owned source/docs command surface must be updated, its closed list excludes `docs/troubleshooting/serena-installation.md:25-51,112-151` and `docs/reference/mcp-server-guide.md:510-519`. Both actively direct users to the deprecated floating Git Serena launcher. |
| 5 | Tests cover every required Tavily pin update | FAIL | The scanner in `tests/docs/test_tavily_doc_alignment.py:76-85` scans all text under `src/superclaude` and `docs`. The independent stale-literal inventory found omitted in-scope strings in `install_mcp.py:29,521-528` and `cli/eval/suites/real.yaml:1629-1631`; the Tavily test file itself has many literal assertions at `test_install_mcp_tavily.py:3-375`. Research 08's documentation list does not assign these sources or require an exhaustive pre/post scanner inventory. |
| 6 | Tests are isolated and test the intended behavior | PASS | `tests/cli/test_install_mcp_tavily.py:60-74,171-194` intercepts subprocesses and captures generated argv; the current focused baseline passed `20 passed, 1 skipped`. Research 04 also identifies dedicated registry and root-config tests for new behavior (`04-integration-impact.md:54-60`). |
| 7 | Validation baseline is executable without expanding scope | PASS | `research/08-scope-dispositions.md:28-30` mandates pre-change capture, `make sync-dev`, then a post-change comparison against the pre-existing baseline. Independent `make verify-sync` exited 2 solely for unrelated `.claude` drift/missing mirrored artifacts; `Makefile:108-163` shows sync only copies generated classes and `Makefile:165-279` verifies them. The policy correctly forbids repairing or staging unrelated generated output. |
| 8 | Scope exclusions and packaged-template rationale are explicit | PASS | `BUILD-REQUEST.md:12-17` excludes named integrations and user/machine configuration. `research/07-config-ownership-gap-fill.md:34-48,89-105` shows packaged JSON templates are shipped reference artifacts, not runtime installer inputs; retaining `auggie-mcp` avoids a broad hook/eval migration. |

## Summary
- Checks passed: 6 / 8
- Checks failed: 2
- Critical issues: 0
- Important issues: 2
- Issues fixed in-place: 0 (report-only review)
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 29 | Grep: 1 | Glob: 0 | Bash: 4
- Tool-engagement summary: Tavily MCP was attempted first for current external package/release verification (`tavily_extract`: 1 successful batch). No fallback was used. Dedicated Grep was attempted once and failed because its vendored `rg` executable was unavailable (`ENOENT`); targeted `git grep` was then used as the local fallback.
- UNCHECKED items: none.
- UNVERIFIABLE items: none.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `research/08-scope-dispositions.md:20-26`; `docs/troubleshooting/serena-installation.md:25-51,112-151`; `docs/reference/mcp-server-guide.md:510-519` | The research calls its four-file list an exhaustive disposition for every affected project-owned source/docs surface, but it deliberately omits two active user-facing Serena instructions that retain the floating Git source and obsolete `ide-assistant` context. A task executor following the list leaves users with contradictory, non-reproducible installation advice. | Add these two documents to the bounded direct-document update list and replace/remove every outdated Serena install/re-registration example with the primary-verified `serena-agent==1.7.0` launcher and `claude-code` context. If either is intentionally historical, add an explicit deprecation banner and canonical-guide link instead; do not leave a runnable stale command. |
| 2 | IMPORTANT | `research/01-registry-tests.md:76-80`; `research/08-scope-dispositions.md:18-26`; `tests/docs/test_tavily_doc_alignment.py:76-85`; `src/superclaude/cli/install_mcp.py:29,521-528`; `src/superclaude/cli/eval/suites/real.yaml:1629-1631`; `tests/cli/test_install_mcp_tavily.py:1-375` | The selected update list will not satisfy the repository's own single-pin guard. It omits all in-scope implementation comments/docstrings, the E16 eval comment, and the full set of literal test expectations that still say `0.2.20`. Updating only the registry, guide, and scanner expected value leaves either test failures or stale user/developer claims. | Require a pre-change `git grep -n 'tavily-mcp@0.2.20' -- src/superclaude docs tests` inventory; update every normative or explanatory literal in the scanner roots plus all focused test expectations; then run the alignment test and repeat the inventory, allowing no `0.2.20` result outside deliberately excluded history. Keep the scanner's expected version at `0.2.22`. |

## Actions Taken
- Performed a report-only readiness review; no source, configuration, generated `.claude/`, or user/machine configuration was changed.
- Read research files 01–08, the build request, registry/reconciliation path, direct docs, packaged configs, tests, root configuration, Makefile, package manifests, and compatibility consumers.
- Ran `uv run pytest tests/cli/test_install_mcp_tavily.py tests/docs/test_tavily_doc_alignment.py -q`: **20 passed, 1 skipped**.
- Ran `make verify-sync`: **exit 2**, with only unrelated existing mirror drift/missing source counterparts. This validates the need for the baseline/no-new-drift policy; this review did not run mutating `make sync-dev`.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No inherited structural verdict was provided; no structural result was relied upon.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Migration compatibility — verified by Read of `src/superclaude/cli/install_mcp.py:623-685`; same-name command drift is exact-name reconciled, which independently validates retaining the Morph client name.
- Root-config namespace continuity — verified by Read of `.mcp.json:1-13` and targeted `git grep` of the hooks, CLI evaluation suite, and tests that consume `auggie-mcp`.
- Tavily test-plan completeness — verified by Read of `tests/docs/test_tavily_doc_alignment.py:41-85`, `tests/cli/test_install_mcp_tavily.py:1-375`, and `real.yaml:1621-1644`, plus the stale-literal inventory.
- Validation feasibility — verified by Read of `Makefile:108-279` and an independent `make verify-sync` baseline run.

## Recommendations
- Do not hand this research package to a task executor yet.
- Resolve both IMPORTANT findings by expanding the direct-document and complete Tavily-literal dispositions, while retaining the confirmed minimal compatibility decisions: keep `morphllm-fast-apply` and `auggie-mcp`; do not migrate hooks/evaluations, plugin templates, or user configuration.
- Preserve the stated validation order: capture baseline → targeted tests → `make sync-dev` → `make verify-sync` with a no-new-drift comparison → `make lint` and the relevant suite. Generated `.claude/` output remains unstaged.

## QA Complete
