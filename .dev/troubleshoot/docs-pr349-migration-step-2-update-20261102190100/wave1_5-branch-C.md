# Wave 1.5 Branch C — semantic-restriction extraction (returned by troubleshoot-analyst; persisted by parent on receipt)

degraded: true (Grep/Read only). Every quoted line was Read by the worker.

| source_file:line | applies_to | quoted_text |
|---|---|---|
| src/superclaude/cli/main.py:407 | superclaude update (MCP registrations) | "# Read-only: update never touches MCP registrations." |
| src/superclaude/cli/main.py:50 | superclaude install (codegraph phase) | "Installs the framework to ~/.claude/ and, as a required user-level phase," |
| src/superclaude/cli/main.py:239 | superclaude install (codegraph phase) | "# Step 8: codegraph, a required user-level phase. A failure keeps the framework" |
| src/superclaude/cli/main.py:256 | superclaude install (retire step) | "# Non-fatal by design: nothing here may change the exit code." |
| src/superclaude/cli/main.py:262 | install (retire readiness gate) | "# A failed phase in this run never counts as ready (spec 2.12)." |
| src/superclaude/cli/install_mcp.py:925 | install_codegraph_mcp | "\"\"\"Required install phase: reuse or download the pinned codegraph, then register it.\"\"\"" |
| src/superclaude/cli/install_mcp.py:676 | MCP reconcile | "MUST treat ``None`` as \"cannot confirm up-to-date\" and reconcile — never as a match (fail" |
| src/superclaude/cli/install_retired_mcp.py:3 | run_retire_step | "Runs at the end of ``superclaude install`` and never changes its exit code." |
| src/superclaude/cli/install_retired_mcp.py:391 | run_retire_step callers | "Callers wrap this in ``try/except``: no outcome may change the install exit code." |
| docs/user-guide/mcp-installation.md:70 | update (user docs contract) | "- `superclaude update` keeps its existing framework behavior and never touches MCP registrations; it only prints a notice telling you to run `superclaude install` when a removable legacy entry is present." |
| docs/user-guide/mcp-installation.md:66 | install retire step | "The step is bounded in time, never changes the exit code of `superclaude install`, and never touches binaries, indexes, caches or memories." |
| .dev/codegraph-migration/specs/phase-1-removal-spec.md:353 | update (Phase 1 spec) | "- `superclaude update`: prints only \"legacy registration present: run `superclaude install`\" (keeps its never-touches-MCP contract, `docs/user-guide/mcp-installation.md:24`)." |
| .dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md:53 | update (Phase 2 spec) | "Not changed, with the reason: `superclaude update` (`main.py:346-431`, documented never to touch native/MCP state, `docs/user-guide/mcp-installation.md:24`);" |
| .dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md:848 | update + update.sh (decision D7) | "\| D7 \| `update.sh` and `superclaude update` unchanged \| add a step \| self \| `update.sh:8` already runs `install --force`; `update` is documented never to touch MCP state; `update.sh` is pinned to four commands (`tests/cli/test_update_script.py:13-18`). \|" |
| .dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md:61 | install retire gate | "the current-pin Serena entry is never removed unless codegraph is ready in the same run" |
| .dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md:192 | update.sh upgrade path | "Requirement (user, via the coordinator, `orchestration/README.md` \"Coordinator concerns\"): after `./update.sh` on an existing workspace, Serena and codebase-memory must be completely absent." |
| .dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md:194 | install retire gate | "`install()` passes `codegraph_success and codegraph_ready()` to the retire step, so a failed phase in this run never counts as ready." |
| src/superclaude/rules/core/changelog_maintenance.md:52 | changelog | "All framework changes MUST be documented following Keep a Changelog format and Semantic Versioning standards." |
| src/superclaude/rules/core/changelog_maintenance.md:108 | release notes file | "4. Fill ALL required sections (see template)" |
| src/superclaude/rules/core/changelog_maintenance.md:179 | release notes | "- ❌ **NEVER** use vague descriptions (\"various fixes\")" |
| src/superclaude/rules/core/changelog_maintenance.md:180 | release notes migration | "- ❌ **NEVER** forget migration notes for breaking changes" |

Worker notes: no rule is broken by `update` skipping codegraph/retire; that is the documented design (D7). The design's stated upgrade path is `./update.sh` = `superclaude install --force` (phase-2 spec :192, :848). The specs' citation `mcp-installation.md:24` is stale (now :70).
