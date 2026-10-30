# Option A: Phase 1 rewrites every load-bearing step to a named native floor

Read `context.md` first.

Phase 1 edits each load-bearing SYM/REF/DIAG/ALLOW row so the step names only tools that exist after Phase 1:

- symbol lookup / outline -> `Grep` for the definition (`rg -n "def name|class name|function name"`) then `Read` the range; auggie first where the primitive already uses it.
- references / callers -> `rg -n -w <symbol>` over the repo, then `Read` call sites.
- implementations / type hierarchy -> `rg` for `class .*\(<Base>\)` / `implements <Iface>`; mark the step "best effort".
- diagnostics -> the project's own linter/type-checker via Bash (already the second leg of reflect's verification triangle); drop `get_diagnostics_for_file`.
- `tools:` / `allowed-tools:` lose the `mcp__serena__*` names; troubleshoot-analyst roster and its pinning test change together.
- reflect: the symbol chain becomes Grep/Read with the existing fail-open wording; Serena degraded tokens are removed from the contract (separate, already decided).

Phase 1 also writes a "codegraph slots" ledger (one row per rewritten step: file, step, former Serena tool, native floor used) into the Phase 3 handoff under `.dev/`, so Phase 3 can insert codegraph as a tier above the floor without re-searching.

For: no dangling step at any commit; behaviour after Phase 1 is fully specified and testable; independent of whether Phase 3 merges with Phases 1-2; the floor stays useful permanently (codegraph can be absent in some projects, so Phase 3 needs a floor anyway).
Against: most edit work (about 20 load-bearing rows plus their mirrors); some steps are touched twice (Phase 1 floor, Phase 3 codegraph tier); rg-based reference tracing is weaker than Serena's LSP, so reflect/troubleshoot quality dips until Phase 3.
