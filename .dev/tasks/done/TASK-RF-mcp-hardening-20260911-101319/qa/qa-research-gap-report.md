# QA Report — Research Gate

**Topic:** Narrowly bounded MCP hardening — final gap-detection gate
**Date:** 2026-09-11
**Phase:** research-gate
**Fix cycle:** 2

---

## Overall Verdict: FAIL

**Confidence:** Verified: 9/10 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 21 | Grep: 4 (runtime failure) | Glob: 4 (runtime failure) | Bash: 5 | tavily_search: 0 | tavily_extract: 4 | web_search_fallback: 0 | web_fetch_fallback: 0

`Glob` and `Grep` could not execute because their vendored ripgrep binary was absent; neither failed tool result was used as evidence. Tavily was available, so no fallback was used. The four Tavily extracts independently confirmed Tavily 0.2.22, Sequential Thinking 2026.8.31, the Serena 1.7.0 distribution/console script and relevant flags, the Auggie project-scope command shape, and Morph’s successor launcher/API-key contract.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | Read all eight files in `research/`. Each declares `Status: Complete`; `08-scope-dispositions.md` supplies the formerly missing final disposition and sync-baseline policy. |
| 2 | Evidence density | FAIL | Code claims cite concrete files/lines and external sources are URL-bound, but external factual assertions in `03-official-releases.md:10-14`, `05-serena-launcher-gap-fill.md:8-11`, and `06-morph-migration-gap-fill.md:7-15` do not carry one of the required `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` tags. `08` adds `[PRIMARY-VERIFIED]`, which is useful provenance but is not an allowed substitute under this gate’s exact disposition contract. |
| 3 | Scope coverage | PASS | `research-notes.md:9-16` key surfaces are covered by 01/02/04/07/08. `08:20-26` gives a bounded update list for direct user docs while explicitly excluding unrelated legacy docs, templates, plugins, and user/machine config. |
| 4 | Documentation cross-validation | FAIL | Tavily independently verified the external claims; local code was also reread. However the required per-claim disposition syntax remains absent from the earlier release/gap-fill claims, so the contract is not met despite reliable source links. |
| 5 | Contradiction resolution | PASS | The former document-scope contradiction is resolved: `08:20-26` assigns the four directly corresponding project-owned docs to this task and excludes `technical-architecture.md`, `mcp-server-guide.md`, templates, plugins, and user config. The client keys remain `auggie-mcp` and `morphllm-fast-apply` (`07:72-87`; `06:7-13`). |
| 6 | Gap severity | FAIL | The remaining evidence-disposition defect is IMPORTANT: it prevents the task record from mechanically distinguishing code proof, unresolved claims, and externally primary-verified facts. No unresolved command, key-retention, scope, or validation-policy gap remains. |
| 7 | Depth appropriateness | PASS | Standard-tier file-level coverage traces CLI caller → registry → exact-command reconciliation in `01:25-40`; it traces root config/key compatibility in `07:60-87`; and it identifies targeted test/doc surfaces in `04:54-70`. |
| 8 | Integration point coverage | PASS | Same-name reconciliation is live for Morph (`01:35-40`), while retaining `auggie-mcp` preserves the hook/eval namespace (`07:64-87`). The reread registry and root config confirm these are real current edges, not documentation-only assumptions. |
| 9 | Pattern documentation | PASS | Research identifies `MCP_SERVERS` as runtime authority, exact-command drift reconciliation, root config ownership, source-of-truth/sync boundaries, and reusable subprocess-interception tests. |
| 10 | Incremental writing compliance | UNVERIFIABLE | Task-local research files have no trustworthy version-history artifact establishing incremental authorship. This cannot be inferred from polished Markdown and is not relied upon for the technical readiness assessment. |

## Summary
- Checks passed: 6 / 10
- Checks failed: 3
- Unverifiable: 1
- Critical issues: 0
- Issues fixed in-place: 0 (report-only QA)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `research/03-official-releases.md:10-14`; `research/05-serena-launcher-gap-fill.md:5-11`; `research/06-morph-migration-gap-fill.md:7-15` | The research-gate contract requires every documentation/external claim to be labeled exactly `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]`. These claims are source-linked and independently supported, but carry no allowed disposition. `08`’s `[PRIMARY-VERIFIED]` label does not retroactively tag the individual earlier claims and is outside the allowed vocabulary. | Add an allowed disposition to every affected external assertion. For facts validated only from vendor sources, use `[UNVERIFIED]` with the primary URL retained, or revise the gate/template vocabulary to explicitly permit `[PRIMARY-VERIFIED]` before relying on it. Do not label an external release fact `[CODE-VERIFIED]` unless a cited repository surface proves the local implementation fact. |

## Actions Taken
- Read the build request, research notes, and all eight in-scope research files.
- Reread the current runtime registry, root `.mcp.json`, four direct documentation surfaces, relevant focused tests, and Makefile sync targets.
- Independently extracted vendor content with Tavily: Serena v1.7.0’s `serena` console script and CLI flags; Auggie’s project-scope command shape; Tavily 0.2.22; Sequential Thinking 2026.8.31; and Morph’s `@morphllm/morphmcp` command/API-key contract.
- Ran `make verify-sync` as a read-only baseline check. It currently exits 2 because of pre-existing `sc-bare-review` mirror differences, two extra `.claude/skills` directories, and a missing source hook; this supports `research/08`’s baseline-comparison policy and identifies the expected comparison anchors.
- No research content was modified because this is a report-only gate.

## Recommendations
- Resolve the single IMPORTANT evidence-disposition finding, then rerun this gate. All task-shaping technical content is otherwise actionable: retained keys, five target launchers/pins, direct-doc boundary, tests, and the `verify-sync` baseline policy are now concrete.
- During execution, retain `auggie-mcp` in `.mcp.json` and `morphllm-fast-apply` in the registry while changing only their launchers. Do not expand scope into template/plugin consolidation, unrelated legacy guides, or machine/user configuration.
- Capture `make verify-sync` before and after the changes and compare the known baseline failures above; run `make sync-dev` but do not stage generated `.claude/` output.

## QA Complete
