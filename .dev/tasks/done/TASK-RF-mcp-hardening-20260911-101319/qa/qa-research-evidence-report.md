# QA Report — Research Gate

**Topic:** MCP hardening — final evidence-quality gate
**Date:** 2026-09-11
**Phase:** research-gate
**Fix cycle:** 2

---

## Evidence Audit


Independent local and Tavily-first primary-source verification was completed for every command asserted as **[PRIMARY-VERIFIED]** in `research/08-scope-dispositions.md`.

- **Tavily:** npm confirms `tavily-mcp` version `0.2.22`; the vendor README supports the `npx -y tavily-mcp@…` launcher and `TAVILY_API_KEY` contract.
- **Sequential Thinking:** npm confirms `@modelcontextprotocol/server-sequential-thinking` version `2026.8.31`; the official MCP repository documents the unpinned `npx -y @modelcontextprotocol/server-sequential-thinking` invocation. Pinning that documented package command to the verified release is evidence-supported.
- **Serena:** the tagged `v1.7.0` source verifies distribution `serena-agent==1.7.0`, `start-mcp-server`, `--project-from-cwd`, and both boolean flags. Official Serena configuration documentation identifies `claude-code` as a built-in context; no longer an inferred context value. The exact selected launcher is therefore supportable when the combined source set in `03` and `05` is cited claim-by-claim.
- **Morph:** current official Morph Claude Code guidance supports `@morphllm/morphmcp` and `MORPH_API_KEY`; the package page explicitly rejects `--prefer-offline` because stale metadata can cause failures. The older quickstart still recommends it, which is an unresolved documentation contradiction but not a blocker to selecting the current package-page launcher. Retaining `morphllm-fast-apply` is correctly bounded as a local client-name/reconciliation decision, not a vendor identity or tool-contract claim.
- **Auggie:** vendor guidance specifies `auggie --mcp --mcp-auto-workspace`; npm confirms `@augmentcode/auggie@0.36.0`. Local reads prove preserving the root key `auggie-mcp` retains the hook/tested tool namespace while changing only the executable and arguments.

**Evidence-blocker determination:** the former command-evidence blockers are resolved. However, the research set still violates mandatory research-gate structure and disposition requirements, so it is not eligible to create a task file under the zero-tolerance gate.

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | FAIL | Bash listed eight research files. Read confirmed `Status: Complete` in all eight, but `03-official-releases.md`, `05-serena-launcher-gap-fill.md`, and `06-morph-migration-gap-fill.md` have no `## Summary` section. |
| 2 | Evidence density | PASS | Every selected command in `08:10-14` was independently checked against local registry/config consumers and Tavily-first primary sources. The command decisions are sufficiently specific for implementation. |
| 3 | Scope coverage | PASS | Read of `research-notes.md:9-16` and `01`, `02`, `04`, `07`, and `08` verifies coverage for the registry, CLI, tests, docs, Auggie guide, and root `.mcp.json`. |
| 4 | Documentation cross-validation | FAIL | `03:10-14`, `05:5-19`, and `06:7-24` make external/doc-sourced claims without the required `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, or `[UNVERIFIED]` tag. `[PRIMARY-VERIFIED]` in `08` does not satisfy the prescribed three-tag schema. |
| 5 | Contradiction resolution | FAIL | Morph’s official quickstart still specifies `--prefer-offline`, while the current official package page explicitly says examples no longer use it. `06:15` selects the latter but does not record both claims and resolution. The non-Tavily test-home recommendations also conflict across `01:76-79`, `02:57-59`, and `04:58-59`. |
| 6 | Gap severity | PASS | The new `08:10-16` dispositions, independently re-verified above, close the formerly critical Serena command and Morph launcher evidence gaps. Remaining items are research-quality/plan-consistency failures, not unknown command facts. |
| 7 | Depth appropriateness | PASS | This Standard-tier research delivers file-level coverage and traces registry selection through exact-command reconciliation (`01:25-40`; `07:34-40`). |
| 8 | Integration point coverage | PASS | `07:60-94`, root `.mcp.json`, hook matcher/script, and behavioral hook tests establish the live `auggie-mcp` namespace dependency and the key-preserving migration. |
| 9 | Pattern documentation | PASS | The reports document registry authority, exact same-name reconciliation, local namespace preservation, source-of-truth boundaries, and required source/mirror validation. |
| 10 | Incremental writing compliance | FAIL | `05` and `06` are final-form conclusion documents with no investigation/revision log; `03` is likewise a compact result list. Only `07` includes a minimal investigation log. |

## Summary
- Checks passed: 6 / 10
- Checks failed: 4
- Critical issues: 0
- Issues fixed in-place: 0 (fix authorization: false)
- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 21 | Grep: 0 | Glob: 1 (runtime failure) | Bash: 1 | tavily_search: 7 | tavily_extract: 6 | web_search_fallback: 0 | web_fetch_fallback: 0
- Tool-minimum check: 22 local-inspection attempts (Read + Grep + Glob) for 10 checks; minimum met. `Glob` could not execute because the vendored ripgrep binary is absent; its failure is recorded rather than treated as a successful scan.
- UNCHECKED: none.
- UNVERIFIABLE: none.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `research/03-official-releases.md`; `research/05-serena-launcher-gap-fill.md`; `research/06-morph-migration-gap-fill.md` | Three complete research files omit the required `## Summary` section. | Add a concise summary to each stating the decision, source/evidence boundary, and any remaining uncertainty. |
| 2 | IMPORTANT | `research/03-official-releases.md:10-14`; `research/05-serena-launcher-gap-fill.md:5-19`; `research/06-morph-migration-gap-fill.md:7-24` | External documentation claims have no allowed disposition tag. `08`'s aggregate `[PRIMARY-VERIFIED]` label is useful evidence but does not replace per-claim cross-validation tags. | Apply one permitted disposition tag to every externally sourced claim and state its specific source. Retain `[PRIMARY-VERIFIED]` as supplemental evidence if desired. |
| 3 | IMPORTANT | `research/06-morph-migration-gap-fill.md:15`; `research/08-scope-dispositions.md:12` | The selected no-`--prefer-offline` Morph launcher is evidence-supported, but the contradictory official quickstart is not documented or explicitly resolved. | Name both first-party sources, mark their conflict, and state why the current package-page recommendation controls the selected launcher. Preserve the existing local-name/tool-contract boundary. |
| 4 | IMPORTANT | `research/01-registry-tests.md:76-79`; `research/02-docs-config.md:57-59`; `research/04-integration-impact.md:58-59` | The reports prescribe incompatible homes for non-Tavily registry/config tests. A task builder cannot produce a single evidence-backed atomic test plan from conflicting instructions. | Select one concrete test arrangement, update all three research files, and show how it uses the existing test convention without duplicating coverage. |
| 5 | MINOR | `research/03-official-releases.md`; `research/05-serena-launcher-gap-fill.md`; `research/06-morph-migration-gap-fill.md` | These files lack an auditable investigation/revision log, so incremental construction cannot be verified. | Add a short dated investigation/revision log for the evidence-gathering and disposition change. |

## Actions Taken
- No research or implementation files were modified; fix authorization was not provided.
- Read every file in scope (`research/01` through `research/08`), the research inventory, build request, local registry/config/hook consumers, and focused regression tests.
- Used Tavily-first search and extraction for the five selected vendor command sets. No fallback was used.
- Confirmed the tagged Serena CLI accepts the required flags, and official Serena configuration identifies `claude-code` as a built-in context.

## Recommendations
- Do not create the task file yet: resolve all five research findings and re-run this gate.
- The primary-command evidence itself is now adequate: retain the `08` command decisions after adding per-claim disposition/source records.
- Keep the Auggie root key `auggie-mcp` unless a separately scoped hook/evaluation namespace migration is approved; local hooks and behavioral tests make that dependency live.

## QA Complete
