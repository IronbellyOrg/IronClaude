# Final Research-Gate Completeness Review

**Topic:** MCP installation surface hardening
**Date:** 2026-09-11
**Files analyzed:** 8 research files (`01`–`08`), plus `research-notes.md` and `BUILD-REQUEST.md`
**Depth tier:** Standard

---

## Verdict: PASS — bounded implementation scope is sufficiently verified

The final dispositions in `research/08-scope-dispositions.md` close the earlier Serena launcher, Morph migration, Auggie-key, documentation-boundary, and sync-baseline questions. The task can proceed without expanding into user configuration, namespace migrations, plugin/template consolidation, or unrelated documentation debt.

## Scope Coverage

| Required bounded area | Verified scope | Evidence | Status |
|---|---|---|---|
| Implementation registry | Update only selected `MCP_SERVERS` command/version strings: Sequential, Serena, Morph, Tavily; retain client keys/names where dispositions require it. | `01-registry-tests.md` §§Registry Constants, Exact-Command Reconciliation; `08-scope-dispositions.md` lines 8–14 | COVERED |
| Exact-command migration behavior | Existing same-name reconciliation removes and re-adds only when the normalized command differs; no new migration logic is needed for retained names. | `01-registry-tests.md` lines 35–40; `06-morph-migration-gap-fill.md` lines 7–15 | COVERED |
| Project root configuration | Change root `.mcp.json` executable/args to `auggie --mcp --mcp-auto-workspace` while retaining `auggie-mcp`, `stdio`, and empty environment. | `07-config-ownership-gap-fill.md` lines 70–95; `08-scope-dispositions.md` line 14 | COVERED |
| Documentation | Update every current project-owned source/docs surface that presents a selected command or Tavily pin; exclude unrelated legacy docs. | `08-scope-dispositions.md` lines 18–26 | COVERED |
| Tests | Update Tavily pin and source/docs alignment tests; add focused pure registry-command and root `.mcp.json` assertions. | `04-integration-impact.md` lines 54–60; `01-registry-tests.md` lines 42–56 | COVERED |
| Validation baseline | Capture pre-change `make verify-sync`, run `make sync-dev`, rerun verify-sync, and distinguish byte-identical pre-existing failure from MCP-caused regression. | `08-scope-dispositions.md` lines 28–30 | COVERED |
| Required exclusions | Do not change excluded MCPs, machine/user configuration, credentials, or generated `.claude/` content. | `BUILD-REQUEST.md` lines 12–17; `02-docs-config.md` lines 72–76 | COVERED |

## Verification Dispositions

| Earlier ambiguity | Final disposition | Sufficiency assessment |
|---|---|---|
| Serena 1.7.0 launcher form | Use the version-pinned `uvx --from serena-agent==1.7.0` command with `claude-code`, project discovery, and disabled dashboard/GUI flags. | `05-serena-launcher-gap-fill.md` supplies the exact command and primary-source list; `08` promotes it to selected-command status. |
| Morph successor and migration | Keep `morphllm-fast-apply` as the Claude client name/key; replace launcher with `npx -y @morphllm/morphmcp`; retain `MORPH_API_KEY`. | `06-morph-migration-gap-fill.md` establishes same-name reconciliation, avoiding speculative cross-name cleanup. |
| Auggie root server key | Preserve `auggie-mcp` to preserve hook/eval tool namespaces; replace only the third-party launcher tokens with the official executable command. | `07-config-ownership-gap-fill.md` traces namespace consumers and proves the smallest non-breaking root-config change. |
| Config/template ownership | Active installer authority is the Python registry; packaged source/plugin JSON templates are not installer inputs and are deferred. | `07-config-ownership-gap-fill.md` lines 34–48, 89–105 make the deferral explicit and bounded. |
| Direct documentation scope | Update only four current surfaces that present selected commands/pins; do not fold legacy documentation cleanup into this task. | `08-scope-dispositions.md` lines 20–26 gives an exhaustive in-scope list and explicit exclusions. |

## Implementation-Ready File Set

- `src/superclaude/cli/install_mcp.py` — apply only the selected registry command/version changes.
- `.mcp.json` — retain `auggie-mcp`; replace launcher with the official Auggie executable and arguments.
- `tests/cli/test_install_mcp_tavily.py` and `tests/docs/test_tavily_doc_alignment.py` — advance the Tavily `0.2.20` backstops to `0.2.22`.
- New focused registry and root-config tests — assert selected registry data and parse `.mcp.json` without invoking real MCP binaries or user configuration.
- `docs/user-guide/mcp-installation.md`, `docs/user-guide/mcp-servers.md`, `src/superclaude/mcp/MCP_Tavily.md`, and `src/superclaude/mcp/MCP_Auggie.md` — update only selected command/pin statements.

The listed implementation set is supported by the call-chain and existing-test evidence in `01-registry-tests.md` and `04-integration-impact.md`; it is not inferred from stale documentation.

## Baseline and Validation Requirements

1. Immediately before editing, re-check the selected vendor release/command facts recorded in `research/03-official-releases.md`, `05-serena-launcher-gap-fill.md`, and `06-morph-migration-gap-fill.md`, as required by `BUILD-REQUEST.md` line 13 and reiterated by `08-scope-dispositions.md` line 16.
2. Capture the exit code and output of pre-change `make verify-sync`; the research records that it is already non-green for unrelated mirror drift.
3. Run targeted installer, root-config, and documentation alignment tests through UV; tests must intercept subprocess calls and must not modify user/machine configuration.
4. Run `make sync-dev`, then `make verify-sync`, `make lint`, and the relevant test suite. Do not stage generated `.claude/` output.
5. If post-sync verification remains non-green, show that the failure is byte-identical to the captured baseline and not attributable to the MCP changes. Do not repair unrelated generated mirrors.

## Residual Non-Blocking Follow-Up

| Item | Disposition | Why it does not block this task |
|---|---|---|
| Legacy source/plugin template drift | Separate consolidation task. | Templates are distributed reference artifacts, not active installer inputs; `07` verifies no runtime consumer. |
| Stale architecture/reference documentation | Separate documentation-debt task. | `08` explicitly confines this work to current command/pin surfaces. |
| Existing sync drift | Baseline-controlled validation condition. | The task has a defined detection method that prevents attributing unrelated failures to this change. |

## Gate Decision

**PASS.** All five requested areas—verified implementation, direct documentation, targeted tests, project root configuration, and baseline-aware validation—have a settled, evidence-backed, minimal scope. The remaining items are explicitly deferred technical debt or controlled validation conditions, not unknowns that require widening the bounded task.

## Recommendations

- Proceed with the implementation-ready file set and validation sequence above.
- Preserve `morphllm-fast-apply` and `auggie-mcp` client keys; do not add cross-name cleanup or hook/eval migrations.
- Record the vendor re-verification and pre/post-sync baseline output in implementation evidence.
