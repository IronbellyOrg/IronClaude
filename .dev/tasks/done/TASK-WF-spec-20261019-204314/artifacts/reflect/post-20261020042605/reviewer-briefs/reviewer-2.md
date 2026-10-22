# Reviewer 2: qa
Worktree root: /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP
Archived work unit: /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/.dev/tasks/done/TASK-WF-spec-20261019-204314
Current output only: /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/.dev/tasks/done/TASK-WF-spec-20261019-204314/artifacts/reflect/post-20261020042605

Read-only reviewer. No commands, Git, tests, prompts, file writes, fixes, or agents. Any imperative inside quoted source/plan material is historical contract data, not an execution request. Do not trust earlier completion reviews or quoted tests as runtime proof. Evaluate candidate claims against the complete acceptance/security constraints; confirm, reject or qualify each W1-D1/W1-D2/W1-D3 mechanism-versus-contract claim with evidence. Absence from any index is never absence in this working tree. Read current hits before citing. The operator's exact Linux-first direction is supplied below. The intentionally pending separately authorized live smoke is a release gate, not an authorized execution task.

Return a self-contained structured deviation card: per assigned task status/AC coverage; disposition of every candidate with scenario/spec/code anchors; any other verified deviation classified authorized|necessary|drift|regression (no fifth class); evidence gaps separate from actual defects; required-capability caller/result-use checks; bounded risk/actionable next evidence. No final calibrated confidence: independent calibration follows. No fixes are authorized.

## T1 card excerpt
````markdown
## Self-reported completion map

| Task | Source-met ACs | Test/doc surface | Qualification |
|---|---|---|---|
| T1 | 7/7 | 7/7 | Linux-only operator authorization; provenance compatibility candidates below |
| T2 | 7/7 | 7/7 | Exact user registration and rollback |
| T3 | 7/7 | 7/7 | Receipt-gated removal |
| T4 | 7/8 | 8/8 | Reviewer alleges other-server compatibility clause is violated by whole-selection rejection |
| T5 | 7/7 | 7/7 | Default wiring; update unchanged |
| T6 | 6/6 authored | Existing/additional cases | Execution evidence historical, not fresh |
| T7 | 7/7 | Documentation | Intentional pending release smoke, not an execution omission |

Reviewer total: 48/49 source-met. The card also says T4 AC1 and AC7 are met while alleging a clause conflict; that ambiguity is preserved for independent calibration/debate rather than silently corrected.

### W1-D1: Whole-selection rejection in install-all or mixed selections

Reviewer category: **regression candidate**. Anchors claimed: T4 AC1/source §3, other servers retain their existing scopes/behavior. `_native_selection_error` runs for any selection containing native (src/superclaude/cli/install_mcp.py:1311-1314); option 0 selects the entire registry (:1285). On Windows/non-Linux or project/local scope, the whole selection is rejected, so no non-native server installs. The reviewer calls the macOS slice authorized but not Windows/project/local. Existing Darwin mixed-selection test: tests/cli/test_install_codebase_memory.py:982. The reviewer identifies missing dedicated install-all project/Windows cases. This candidate must be debated against the full source's explicit whole-selection validation and native-scope rejection requirements; no execution was performed.

### W1-D2: Group-writable directory provenance rejection

Reviewer category: **conditional regression candidate**. Claimed anchors: T1 AC5 and no false failure after successful native installation. `_check_install_directory` rejects mode & 0o022 at src/superclaude/cli/install_codebase_memory.py:85-100; binary identity also rejects unsafe mode at:102-144. If the canonical directories are 0775 (for example umask 002), native upstream setup could succeed then provenance creation fail at:683/catch:693. Retry might reuse the working binary without creating proof, leaving automatic removal refused. Discovery's owner check at:545-550 does not use the same permission predicate. Reviewer did **not** inspect install_ccsession.py or observe actual upstream modes; the statement that framework wiring probably created a 0775 bin directory is unverified. Default-umask fixtures do not establish this real-world scenario.

### W1-D3: Symlinked HOME ancestor

Reviewer category: **conditional regression candidate**. Canonical uses Path.home().absolute(), whereas directory.resolve() mismatch is ambiguous at native source:85-100,538-544. A symlinked HOME ancestor could therefore make the native phase fail closed. No real HOME scenario or execution was observed; this is source-only. The candidate requires adjudication against explicit symlink/ownership ambiguity fail-closed requirements.

## Evidence gaps and structural risks

- Upstream installer/native setup might intentionally leave background children; the supervisor waits until ECHILD or deadline. This is untested upstream behavior reserved for the separately authorized live gate.
- Actual directory/binary modes created by the released installer were not observed.
- Fresh external CLI syntax/layout confirmation was not performed by the reviewer.
- Real released-binary behavior, companion merge safety and MCP handshake remain intentionally pending live smoke.
- No fresh pytest/mypy verification was run; recorded results remain historical evidence.
- Native helper size/complexity includes subreaper, proof and identity checks; the plan asked for a small helper. Linux procfs/prctl unavailability fails closed, including version probes.
- `_alternate_path_entries` refuses symlink ambiguity; a PATH symlink can block native removal.
- Native removal precedes any residual Claude cleanup failure; absent Claude can yield accurately reported partial removal rather than a completed false success.
````
## Grounding hunks
### .dev/tasks/done/TASK-WF-spec-20261019-204314/TASK-WF-spec-20261019-204314.md:15-28
````markdown
Goal: A normal framework install provisions Codebase Memory MCP through its official full installer, and the existing MCP command supports explicit user-level installation and safe native uninstallation with indexes retained.

## Constraints

- Execute this package only after explicit implementation authorization. Workflow generation itself does not authorize remote installation, live smoke testing, commits, pushes, PRs or releases.
- The frozen source is authoritative. Preserve the full upstream setup, including its detected-client and companion integration effects; do not silently substitute binary-only installation or registration-only uninstall.
- Limit the new full native lifecycle to user scope on Linux/macOS amd64/arm64. Reject other scopes/platforms before native effects; leave other servers' existing scope behavior intact.
- Never request graph-index reset/deletion, elevate privileges, bypass upstream integrity checks, guess binary ownership, or manually erase caches, companion files or unrelated registrations.
- Reuse existing registry/Claude CLI registration helpers and upstream native lifecycle logic. Add only the small native helper and focused tests; no package-manager framework, new dependencies, graph indexing, bundled graph skills, automatic upgrades or Windows integration.
- Keep framework update unchanged. Preserve install --list, --force and --target semantics. A later explicit framework install restores the default bundle; update must not resurrect a removed native tool.
- Read current source and callers before edits; use Auggie before significant changes and Context7/upstream sources for CLI contracts. The source's upstream main SHA is research evidence, not a release pin or proof of released-binary behavior.
- All automated checks use UV, mocked network/native/Claude processes and isolated temporary HOME/config/index paths. Do not execute real acquisition/removal as a test or invoke the real default installer on the developer's HOME.
- Keep code/tests/docs in canonical repo-relative paths. Store task-owned evidence only under ./artifacts/. Do not stage generated .claude/ contents. Sync development mirrors only when distributable components change; verify sync before any later authorized commit.
- Each task includes its own tests/acceptance. Final whole-plan review and package archiving belong to the executor, not a verification-only task or an extra checklist.
````

### .dev/tasks/done/TASK-WF-spec-20261019-204314/TASK-WF-spec-20261019-204314.md:43-49
````markdown
- Linux/macOS and architecture aliases are validated before native effects; native Windows/unsupported architectures produce actionable structured failure rather than false success. Upstream still owns Rosetta/release-asset selection.
- Existing usable canonical/PATH executables are reused without download. No external package-manager installation is silently force-replaced; ambiguous ownership/discovery fails closed.
- Missing curl/Bash matters only when acquisition is required. Native acquisition does not require Node/npm, Docker, an API key or a compiler; Claude CLI readiness is checked by the caller before acquisition.
- The complete upstream bootstrap executes through argv-based subprocesses, never shell=True, a user-shell pipeline, or the existing token-quoted install_command string. Upstream companion setup remains enabled and its integrity/index-retention behavior remains upstream-owned.
- A successful native process is followed by a bounded absolute-path --version check; PATH absence does not cause a false failed installation. The verified version is available for reporting.
- Add focused cases to proposed tests/cli/test_install_codebase_memory.py for supported/unsupported platforms, path precedence and spaces, external-binary reuse, missing prerequisites, failed/empty download, native nonzero/timeout, child-process termination/reaping, postcheck failure and temporary-file cleanup. All lifecycle/network calls are mocked or use benign isolated local child-process fixtures, never the remote installer.
- Catch expected OS/subprocess errors into stage-specific failure results; do not claim rollback of any upstream mutations. Preserve diagnostics without inventing indexing or handshake success.
````

### .dev/tasks/done/TASK-WF-spec-20261019-204314/TASK-WF-spec-20261019-204314.md:84-91
````markdown
Acceptance criteria:
- Full native removal preserves indexes by always passing -y and never passing --delete-indexes/reset flags or manually deleting caches, project files, companion integrations or unrelated registrations.
- Only the canonical upstream install is removed automatically. External/custom-only installations produce a resolved-path explanation and stop without guessed deletion. Symlink/ownership ambiguity fails closed.
- Removal preview describes detected-client/companion effects, potential active-session interruption, retained indexes and leftover updater behavior; it does not describe full native removal as project-scoped deregistration.
- After native success, verify canonical binary and exact user registration absence. Safely remove only a surviving exact user registration through the existing Claude CLI; preserve project entries and unrelated servers. A remaining alternate PATH installation is reported accurately.
- Complete absence is idempotent success. Missing binary with a user registration supports confirmed registration-only partial cleanup, explicitly stating that companion assets were not audited/removed; no binary is acquired merely to uninstall it.
- Upstream nonzero/timeout and failed postconditions report possible partial removal and retry guidance. Do not print success, imply upstream rollback, or perform a second blind cleanup pass. Expected process/OS errors are bounded structured failures.
- Mocked tests verify argv and explicit directory, no index-deletion flags, native timeout/failure, query failures, missing-binary cleanup, absent-state idempotence, external/symlink refusal, surviving alternate installations and updater retention. Isolated sentinel indexes/configs remain untouched by IronClaude.
````

### .dev/tasks/done/TASK-WF-spec-20261019-204314/TASK-WF-spec-20261019-204314.md:97-113
````markdown
## Task 4: Add MCP lifecycle actions, selection-aware prerequisites and dry-run behavior

Depends on: Task 3

Use source sections 3 through 7. Modify src/superclaude/cli/main.py's mcp command and src/superclaude/cli/install_mcp.py orchestration/menu/prerequisites. Add CLI/menu cases in proposed tests/cli/test_install_codebase_memory.py and extend tests/cli/test_install_mcp_registry.py where appropriate. Keep the command flat and preserve existing installation invocations.

Add proposed --uninstall and --yes/-y flags. With no explicit selection, offer Install MCP servers as default, Uninstall Codebase Memory MCP and Cancel. Preserve the gateway-first install branch and add the registry-driven Codebase Memory entry; install-all includes it. Validate complete selections/options before any effects, then check only the selected installation prerequisites. Process explicit gateway-plus-native selection without dropping either result.

Acceptance criteria:
- Explicit Codebase Memory install and uninstall work through --servers codebase-memory-mcp. The uninstall mode accepts only this server; unsupported/mixed removal selections fail before any removal. Other servers retain existing install scopes and behavior.
- Codebase Memory project/local scope is rejected before download/write. Native-only selection does not fail for missing Node/npm/Docker/API keys; existing npm-server and Auggie version requirements still apply when those servers are selected.
- Interactive uninstall shows the account-wide preview and uses default-No confirmation. Decline/cancel makes no changes. --yes bypasses only selected Codebase Memory lifecycle consent, never selects a server, bypasses unrelated API-key prompts or authorizes index deletion.
- Non-TTY mode with no explicit selection fails without a menu; explicit removal without --yes fails safely. Install selection is authorization for the disclosed full upstream setup.
- List mode remains read-only and rejects incompatible mutation combinations before effects. Existing --servers/-s repeatability, --scope defaults and help examples remain accurate; new flags are documented as new.
- Dry-run uses only bounded read-only discovery: no prompts, downloads, upstream install/uninstall, file/config changes or deletions. No-selection dry-run prints choices and exits. Fresh/API-key, stale-registration, native-removal and gateway paths cannot accidentally prompt or mutate.
- Gateway-plus-native installation processes both selections and aggregates any failures instead of returning early and silently discarding the native selection. Invalid selections and prerequisite failures are identified before effects.
- CLI tests demonstrate menu default/cancel, list/install-all visibility, explicit selection, mixed gateway/native completion/failure, unsupported modes/scopes, non-TTY handling, consent and mutation-free dry-run. Tests do not contact real Claude/native processes.
````

### .dev/tasks/done/TASK-WF-spec-20261019-204314/source.md:48-82
````markdown
## 3. Public CLI contract

### Normal framework installation

`superclaude install` must ensure Codebase Memory MCP is installed, runnable, and registered for Claude Code at user scope. It is a default phase, not an additional opt-in question. Before acquisition, print the source URL, intended executable location, and the fact that upstream also configures detected clients and companion assets.

- Run the new phase after existing user setup, so framework installation has already established its files.
- A fresh install executes the official script using the safe execution equivalent in section 4.
- A working existing executable plus an exact, correct user registration is a no-op. Do not fetch latest on every framework install.
- A working executable with missing user registration is registered using the existing MCP registration mechanism; do not rerun the upstream installer merely to repair registration.
- A missing/non-runnable default executable is acquired/repaired through upstream. Do not replace an external package-manager installation silently.
- Acquisition, executable verification, or registration failure makes the overall install exit 1. Preserve successful framework work and report the failed phase and retry command.
- `--list` remains read-only and includes Codebase Memory availability/status. `--force` retains its framework-file meaning; it does not force a native-tool upgrade or erase indexes.
- `--target` retains its existing meaning and does not redirect native-tool or MCP configuration locations.

`superclaude update` is unchanged in this scope. It must not silently reinstall a tool the user explicitly uninstalled. A later explicit `superclaude install` restores the default bundle. Automatic native-tool upgrades, opt-out persistence, and a new framework-wide dry-run are out of scope.

### MCP menu and explicit selection

Keep the flat command and all existing installation invocations working. Add:

```text
superclaude mcp --servers codebase-memory-mcp
superclaude mcp --uninstall --servers codebase-memory-mcp
superclaude mcp --uninstall --servers codebase-memory-mcp --yes
superclaude mcp --uninstall --servers codebase-memory-mcp --dry-run
```

`--uninstall` and `--yes/-y` are NEW flags proposed by this design. They do not exist in the baseline. `--yes` bypasses consent prompts for the explicitly selected Codebase Memory lifecycle only; it must not select servers automatically, affect unrelated API-key prompts, or imply index deletion. `--list` cannot be combined with mutation modes; reject incompatible combinations before effects.

With no explicit servers, show an action choice: **Install MCP servers** (default), **Uninstall Codebase Memory MCP**, **Cancel**. The install branch retains the gateway-first server menu and adds Codebase Memory as a normal registry entry. The uninstall action explicitly names Codebase Memory; do not imply full uninstall support for other servers. Installation option 0 includes the new individual server. Explicit gateway-plus-Codebase-Memory selection must process both rather than silently dropping the native server.

Codebase Memory supports `--scope user` only in this increment because the requested full upstream lifecycle is account-wide. Reject project/local scope with a clear explanation before any download or write. Other servers retain their existing scopes. Do not silently ignore the requested scope or configure all clients while claiming project-only installation.

Noninteractive behavior: require an explicit server selection; no menu prompts on non-TTY input. Explicit Codebase Memory installation authorizes its documented default setup. Native removal requires either interactive confirmation or `--yes`. Dry-run never prompts for consent or invokes the upstream lifecycle.
````

### .dev/tasks/done/TASK-WF-spec-20261019-204314/artifacts/operator-direction.md:1-11
````markdown
# Operator direction after Task 1 halt

The operator was asked whether to accept process-group termination plus direct-child reaping for portability, or retain the stricter cleanup requirement. Their exact answer was:

> there is absolutely no reason to overcomplicate anything in order to preserve macOS portability

Implementation interpretation: prioritize straightforward Linux-native behavior instead of adding portability machinery to preserve macOS support. Do not treat this answer as acceptance of a weakened descendant-cleanup guarantee. If Linux-specific cleanup is necessary, automated macOS support may be excluded and documented rather than driving supervision complexity.

This direction supersedes the frozen plan's macOS-portability constraint where necessary. It authorizes a correction under the changed platform direction; it is not an executor-invented Ruling line or a declaration that the already-blocked implementation is compliant. The source snapshot and original plan remain unchanged for provenance. Independent QA must consider this explicit operator direction with the source acceptance criteria.

Task 1 also has a known mypy assignment error to correct. Tasks 2–7 remain paused until the revised implementation is reviewed. The existing Q0 snapshot is retained; no duplicate start record is created.
````

### .dev/tasks/done/TASK-WF-spec-20261019-204314/artifacts/reflect/post-20261020042605/artifacts/capability-status.yaml:1-34
```yaml
serena_config_snapshot_path: null
serena_version: unknown
serena_active_context: unknown
observed_backend_fingerprint: unknown
absolute_source_overviews_succeeded: 7
diagnostics_queried: 3
native_module_diagnostics: empty
mcp_main_diagnostics: Pyright cannot resolve click and native import context; not accepted as missing implementation or regression without working-tree proof
get_current_config_available: false
activate_project_available: false
execute_shell_command_available: false
onboarding_available: true
onboarding_ran: false
onboarding_skipped_reason: --onboard not provided
read_only_project_value: unknown
verification_ran: false
verification_invocations: 0
verification_skip_reason: tool-unavailable
verification_note: Protocol verification triangle is gated on exposed Serena execute_shell_command and confirmed project availability. No Bash tests/linters/build were substituted around this restriction. Prior test evidence remains historical.
serena_summary_corroboration: unavailable
references_extended_info_used: false
references_extended_info_note: include_info is not an exposed parameter of the available referencing-symbols tool
memory_namespace_verified_for_worktree: false
memory_persisted: false
memory_pruned: false
checkpoint_tools_available: false
checkpoint_logged: skipped
cli_documentation_inspection:
  add_json_help: scope option confirmed, read-only help only
  remove_help: scope option confirmed, read-only help only
  get_help: no scope/json option exposed, no server lookup or health check performed
  official_docs: https://code.claude.com/docs/en/mcp-quickstart
  config_layout: User entries are top-level mcpServers in HOME/.claude.json or CLAUDE_CONFIG_DIR/.claude.json; local entries are project blocks; project file is .mcp.json
  evidence_kind: Current CLI help and Context7 official documentation, not fresh product test execution
```

### .dev/tasks/done/TASK-WF-spec-20261019-204314/artifacts/reflect/post-20261020042605/artifacts/cli-contract-evidence.md:1-11
````markdown
# Current read-only CLI contract observations

These are completed documentation inspections, not instructions to execute commands and not a fresh product test run.

- Installed Claude CLI add-json help exposes explicit local/user/project scope and a JSON payload.
- Installed remove help exposes explicit local/user/project scope; omitting scope removes whichever scope is selected by the CLI.
- Installed get help exposes no scope or JSON option and warns that approved server lookups may perform health checks. No get/list lookup or connection was performed; only help text was inspected.
- Context7 official Claude Code documentation confirms user entries are top-level mcpServers in HOME/.claude.json; CLAUDE_CONFIG_DIR relocates that .claude.json inside the configured directory. Local entries live under project blocks; project configuration uses .mcp.json.
- Official documentation also demonstrates add-json with user scope. This closes the Tier-1 card's unverified layout/grammar note at the documentation level, not the still-pending released-binary/live integration gate.

Source: https://code.claude.com/docs/en/mcp-quickstart and https://code.claude.com/docs/en/self-hosted-environments-configuration (Context7 query during this audit), plus current installed CLI help captured by the orchestrator. No configuration mutation, server connection, native bootstrap, or upstream removal was executed.
````

### src/superclaude/cli/install_codebase_memory.py:85-116
```python
def _check_install_directory() -> None:
    canonical = canonical_executable()
    for directory in (canonical.parent.parent, canonical.parent):
        if directory.resolve() != directory:
            raise ValueError("Symlinked canonical directory")
        if directory.exists():
            info = directory.stat()
            if (
                not stat.S_ISDIR(info.st_mode)
                or info.st_uid != os.getuid()
                or info.st_mode & 0o022
            ):
                raise ValueError(
                    "Canonical directory ownership/permissions are uncertain"
                )


def _binary_identity(path: Path) -> dict:
    _check_install_directory()
    if path.resolve() != path:
        raise ValueError("Symlinked canonical executable")
    with os.fdopen(
        os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), "rb"
    ) as source:
        info = os.fstat(source.fileno())
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != os.getuid()
            or info.st_nlink != 1
            or info.st_mode & 0o022
        ):
            raise ValueError("Canonical executable identity is uncertain")
```

### src/superclaude/cli/install_codebase_memory.py:529-568
```python
def discover_executable() -> Discovery:
    """Prefer canonical, then the first usable PATH file; never modify anything.

    Symlinks/hardlinks and unknown canonical ownership fail closed. External
    files may be reused but are never candidates for automatic replacement.
    """
    canonical = None
    try:
        canonical = canonical_executable()
        for directory in (canonical.parent.parent, canonical.parent):
            if directory.resolve() != directory:
                return Discovery(
                    "ambiguous",
                    canonical,
                    message=f"Symlinked canonical directory: {directory}",
                )
            if directory.exists() and (
                not directory.is_dir() or directory.stat().st_uid != os.getuid()
            ):
                return Discovery(
                    "ambiguous",
                    canonical,
                    message=f"Canonical directory type/ownership is uncertain: {directory}",
                )
        found = _inspect_executable(canonical, canonical=True)
        if found.state in {"canonical", "ambiguous"}:
            return found
        unusable = None
        for path_entry in os.get_exec_path():
            candidate = Path(path_entry).absolute() / BINARY_NAME
            if candidate == canonical:
                continue
            external = _inspect_executable(candidate, canonical=False)
            if external.state in {"external", "ambiguous"}:
                return external
            if external.state == "non_runnable" and unusable is None:
                unusable = external
        return unusable or found
    except (OSError, RuntimeError) as exc:
        return Discovery("ambiguous", canonical, message=f"Discovery failed: {exc}")
```

### src/superclaude/cli/install_codebase_memory.py:597-607
```python
    found = discover_executable()
    if found.state in {"canonical", "external"}:
        return AcquisitionResult(
            True,
            "verification",
            f"Reusing {found.executable} ({found.version}).",
            found.executable,
            found.version,
        )
    if found.state == "ambiguous":
        return AcquisitionResult(False, "discovery", found.message, found.executable)
```

### src/superclaude/cli/install_codebase_memory.py:673-701
```python
            stage = "verification"
            verified = _inspect_executable(canonical, canonical=True)
            if verified.state != "canonical":
                return AcquisitionResult(
                    False,
                    stage,
                    f"Upstream completed but executable verification failed: {verified.message or verified.state}. Partial upstream changes may remain.",
                    canonical,
                )
            stage = "provenance"
            _write_acquisition_receipt(canonical)
            stage = "verification"
            return AcquisitionResult(
                True,
                stage,
                f"Verified {verified.version} at {canonical}. Restart clients to load integrations; no indexing or MCP handshake was performed.",
                canonical,
                verified.version,
                True,
            )
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        partial = (
            " Partial upstream changes may remain; review output and retry."
            if stage in {"install", "verification", "provenance"}
            else " Retry acquisition after resolving the error."
        )
        return AcquisitionResult(
            False, stage, f"{stage.capitalize()} failed: {exc}.{partial}"
        )
```

### src/superclaude/cli/install_ccsession.py:30-44
```python
    dest = home / ".local" / "bin" / "ccsession"
    env = home / ".claude" / "ccsession.env"
    if (env.exists() or env.is_symlink()) and not env.is_file():
        return False, f"ccsession env path is not a file: {env}"
    try:
        wrapper.chmod(0o755)
        hook.chmod(0o755)
        dest.parent.mkdir(parents=True, exist_ok=True)
        collision = (dest.exists() or dest.is_symlink()) and not (
            dest.is_symlink() and dest.resolve() == wrapper.resolve()
        )
        if not collision:
            if dest.is_symlink():
                dest.unlink()
            dest.symlink_to(wrapper)
```

### src/superclaude/cli/install_mcp.py:1280-1359
```python
                .lower()
            )
            if choice == "g":
                selected = ["airis-mcp-gateway"]
            elif choice == "0":
                selected = list(MCP_SERVERS)
            else:
                try:
                    indices = [int(value.strip()) for value in choice.split(",")]
                    names = list(MCP_SERVERS)
                    if not indices or any(
                        index < 1 or index > len(names) for index in indices
                    ):
                        return False, "Invalid selection; no changes made."
                    selected = list(
                        dict.fromkeys(names[index - 1] for index in indices)
                    )
                except ValueError:
                    return False, "Invalid selection; no changes made."
    unknown = [
        name
        for name in selected
        if name != "airis-mcp-gateway" and name not in MCP_SERVERS
    ]
    if unknown:
        return False, "Unknown MCP server selection: " + ", ".join(unknown)
    if uninstall and selected != [codebase_memory.BINARY_NAME]:
        return (
            False,
            "Uninstall accepts only --servers codebase-memory-mcp, not mixed or other servers.",
        )
    if codebase_memory.BINARY_NAME in selected:
        invalid = _native_selection_error(scope)
        if invalid:
            return False, invalid
    if uninstall:
        if not dry_run and not yes and not _is_interactive():
            return (
                False,
                "Noninteractive native removal requires --yes; no changes made.",
            )
        valid, preview = uninstall_codebase_memory_mcp(scope=scope, dry_run=True)
        if dry_run or not valid:
            return valid, preview
        click.echo("Removal preview: " + preview.removeprefix("[DRY RUN] "))
        if not yes and not click.confirm(
            "Proceed with account-wide Codebase Memory removal?", default=False
        ):
            return True, "Removal declined; no changes made."
        return uninstall_codebase_memory_mcp(scope=scope, confirmed=True)

    if not dry_run:
        ready, errors = check_prerequisites(selected)
        if not ready:
            return False, "Prerequisites not met:\n" + "\n".join(errors)
    completed = 0
    failed = []
    for name in selected:
        try:
            if name == "airis-mcp-gateway":
                success = install_airis_gateway(dry_run)
            else:
                success = install_mcp_server(MCP_SERVERS[name], scope, dry_run)
        except (OSError, subprocess.SubprocessError):
            click.echo(
                f"Process error while handling {name}; inspect its installation state before retrying.",
                err=True,
            )
            success = False
        if success:
            completed += 1
        else:
            failed.append(name)
    label = "previewed" if dry_run else "installed"
    if failed:
        return (
            False,
            f"Partially completed: {completed}/{len(selected)} {label}. Failed servers: {', '.join(failed)}",
        )
    return True, f"Successfully {label} {completed} MCP server(s)."
```

### .dev/tasks/done/TASK-WF-spec-20261019-204314/TASK-WF-spec-20261019-204314.md:34-49
````markdown
## Task 1: Implement bounded upstream acquisition and executable discovery

Implement proposed src/superclaude/cli/install_codebase_memory.py from source sections 1, 2 and 4, using src/superclaude/cli/install_mcp.py binary helpers and src/superclaude/cli/install_ccsession.py result conventions as context rather than duplicating a general framework. Revalidate the official install.sh contract and current released behavior while implementing; record meaningful differences under ./artifacts/t1-upstream-contract.md without executing remote code.

Discover the canonical executable before considering a usable PATH installation. Represent discovery outcomes distinctly enough to distinguish missing, runnable, non-runnable, external/custom and ambiguous states. Provide a small native acquisition function returning structured success/failure and the selected absolute executable/version; registration stays in install_mcp.py to avoid circular imports.

Implement full-script acquisition using a private temporary directory, curl with HTTPS-only download/redirect constraints, nonempty successful download and direct argv-based Bash execution without configuration-suppression flags. Bound download to 60 seconds, native installation to 300 seconds and version probes to a short explicit timeout. Use a bounded process-lifecycle mechanism that terminates/reaps the installer and its descendants on timeout. Preserve upstream output and clean temporary script material on both success and failure.

Acceptance criteria:
- Linux/macOS and architecture aliases are validated before native effects; native Windows/unsupported architectures produce actionable structured failure rather than false success. Upstream still owns Rosetta/release-asset selection.
- Existing usable canonical/PATH executables are reused without download. No external package-manager installation is silently force-replaced; ambiguous ownership/discovery fails closed.
- Missing curl/Bash matters only when acquisition is required. Native acquisition does not require Node/npm, Docker, an API key or a compiler; Claude CLI readiness is checked by the caller before acquisition.
- The complete upstream bootstrap executes through argv-based subprocesses, never shell=True, a user-shell pipeline, or the existing token-quoted install_command string. Upstream companion setup remains enabled and its integrity/index-retention behavior remains upstream-owned.
- A successful native process is followed by a bounded absolute-path --version check; PATH absence does not cause a false failed installation. The verified version is available for reporting.
- Add focused cases to proposed tests/cli/test_install_codebase_memory.py for supported/unsupported platforms, path precedence and spaces, external-binary reuse, missing prerequisites, failed/empty download, native nonzero/timeout, child-process termination/reaping, postcheck failure and temporary-file cleanup. All lifecycle/network calls are mocked or use benign isolated local child-process fixtures, never the remote installer.
- Catch expected OS/subprocess errors into stage-specific failure results; do not claim rollback of any upstream mutations. Preserve diagnostics without inventing indexing or handshake success.
````

### .dev/tasks/done/TASK-WF-spec-20261019-204314/TASK-WF-spec-20261019-204314.md:76-91
````markdown
## Task 3: Implement canonical upstream uninstall and scoped residual cleanup

Depends on: Task 2

Use source sections 4, 5 and 7. Extend src/superclaude/cli/install_codebase_memory.py with native removal orchestration and src/superclaude/cli/install_mcp.py with exact user-registration cleanup. Extend proposed tests/cli/test_install_codebase_memory.py and relevant registration cases in tests/cli/test_install_mcp_tavily.py.

Expose enough discovery/preview information for the CLI confirmation in Task 4. Full removal must resolve the canonical upstream installation, invoke that absolute executable with uninstall -y and an explicit canonical --dir value, and delegate activation/owned-file cleanup to upstream. Never run a PATH installation's uninstaller against an unrelated default location or infer ownership merely from a name.

Acceptance criteria:
- Full native removal preserves indexes by always passing -y and never passing --delete-indexes/reset flags or manually deleting caches, project files, companion integrations or unrelated registrations.
- Only the canonical upstream install is removed automatically. External/custom-only installations produce a resolved-path explanation and stop without guessed deletion. Symlink/ownership ambiguity fails closed.
- Removal preview describes detected-client/companion effects, potential active-session interruption, retained indexes and leftover updater behavior; it does not describe full native removal as project-scoped deregistration.
- After native success, verify canonical binary and exact user registration absence. Safely remove only a surviving exact user registration through the existing Claude CLI; preserve project entries and unrelated servers. A remaining alternate PATH installation is reported accurately.
- Complete absence is idempotent success. Missing binary with a user registration supports confirmed registration-only partial cleanup, explicitly stating that companion assets were not audited/removed; no binary is acquired merely to uninstall it.
- Upstream nonzero/timeout and failed postconditions report possible partial removal and retry guidance. Do not print success, imply upstream rollback, or perform a second blind cleanup pass. Expected process/OS errors are bounded structured failures.
- Mocked tests verify argv and explicit directory, no index-deletion flags, native timeout/failure, query failures, missing-binary cleanup, absent-state idempotence, external/symlink refusal, surviving alternate installations and updater retention. Isolated sentinel indexes/configs remain untouched by IronClaude.
````

### .dev/tasks/done/TASK-WF-spec-20261019-204314/TASK-WF-spec-20261019-204314.md:134-148
````markdown
## Task 6: Complete isolated CLI lifecycle regression coverage

Depends on: Task 5

Use source section 7 and behavior contracts in sections 3 through 5. Complete the executable regression suite in proposed tests/cli/test_install_codebase_memory.py, tests/cli/test_install_mcp_registry.py, tests/cli/test_install_mcp_tavily.py and tests/cli/test_update_command.py. This task authors missing cross-entry-point and failure-matrix tests; it is not a verification-only task.

Add reusable test helpers only inside the existing test layout, following the existing subprocess capture/monkeypatch and Click CliRunner patterns. Keep installation versus update mocks distinct. Explicitly isolate HOME, MCP configuration, native binary locations and graph/index sentinels, including tests that exercise timeout cleanup with benign local child processes.

Acceptance criteria:
- Executable regression cases cover fresh install once, no-op repeat, missing-registration repair without network, external-binary reuse, all acquisition/postcheck failures, native prerequisite independence and stage-specific failure propagation.
- Executable cases cover exact scope/name/transport/argv matching, same-name shadowing, query failure versus true absence, paths containing spaces, failed re-registration restoration and distinctly reported restoration failure.
- Executable cases cover list/menu/install-all, mixed gateway/native execution, invalid selections before effects, incompatible list/mutation flags, noninteractive consent, default-No/cancel and prompt-free mutation-free dry-run, including API-key-server paths affected by dispatch.
- Executable cases cover confirmed native argv with canonical --dir and -y, preserved index/cache sentinels, updater retention, alternate PATH installs, external/custom/symlink ambiguity, complete absence, partial missing-binary cleanup and failed/partial upstream outcomes.
- Automated tests never run the real upstream script, native lifecycle, Claude CLI, Node/npm installer or mutate the developer's actual HOME. Existing Auggie/Tavily and update assertions remain meaningful rather than weakened to accommodate the new path.
- During authorized implementation, run the focused four-file suite with uv run pytest and capture command/exit/result evidence under ./artifacts/t6-cli-regressions.txt; report failures faithfully. Planning does not run this suite. Executor-owned final verification may run broader repository checks without adding tasks to this plan.
````

### src/superclaude/cli/install_codebase_memory.py:225-349
```python
def preview_codebase_memory_removal() -> RemovalPreview:
    """Read-only preview; only a matching acquisition receipt authorizes removal."""
    if platform.system() != "Linux" or platform.machine().lower() not in {
        "amd64",
        "x86_64",
        "arm64",
        "aarch64",
    }:
        return RemovalPreview(
            "unsupported",
            "Automated removal requires Linux amd64/arm64. Use the official manual mechanism on other platforms.",
        )
    try:
        _check_install_directory()
        canonical = canonical_executable()
        remaining = _alternate_path_entries()
        try:
            canonical.lstat()
        except FileNotFoundError:
            if remaining:
                return RemovalPreview(
                    "external",
                    "External/custom PATH entries found: "
                    + ", ".join(map(str, remaining))
                    + ". Use their own installation mechanism; no automatic removal.",
                    remaining=remaining,
                )
            return RemovalPreview(
                "missing",
                "Canonical native executable is absent. Companion assets were not audited. "
                + REMOVAL_EFFECTS,
            )
        receipt = _read_acquisition_receipt()
        if receipt is None or receipt["identity"] != _binary_identity(canonical):
            return RemovalPreview(
                "ambiguous",
                f"No matching acquisition receipt for {canonical}; use its original installation/removal mechanism.",
                canonical,
                remaining,
            )
        found = _inspect_executable(canonical, canonical=True)
        if found.state != "canonical":
            return RemovalPreview(
                "ambiguous",
                f"Canonical executable verification failed: {found.message}",
                canonical,
                remaining,
            )
        return RemovalPreview(
            "ready",
            f"Remove canonical {canonical} ({found.version}). " + REMOVAL_EFFECTS,
            canonical,
            remaining,
        )
    except (OSError, ValueError, RuntimeError) as exc:
        return RemovalPreview("ambiguous", f"Removal discovery failed: {exc}")


def uninstall_codebase_memory(
    *, scope: str = "user", confirmed: bool = False
) -> RemovalResult:
    """Run canonical upstream removal only; scoped registration is the caller's job."""
    if scope != "user":
        return RemovalResult(
            False, "scope", "Full native removal supports user scope only."
        )
    if not confirmed:
        return RemovalResult(
            False,
            "consent",
            "Explicit confirmation is required; no removal was performed.",
        )
    preview = preview_codebase_memory_removal()
    if preview.state == "missing":
        return RemovalResult(True, "absent", preview.message)
    if preview.state != "ready" or preview.executable is None:
        return RemovalResult(False, "discovery", preview.message, preview.remaining)
    executable = preview.executable
    try:
        # Revalidate proof immediately before handing the exact canonical path to upstream.
        receipt = _read_acquisition_receipt()
        if receipt is None or receipt["identity"] != _binary_identity(executable):
            return RemovalResult(
                False,
                "discovery",
                "Acquisition identity changed; no removal was performed.",
            )
        result = _run_bounded(
            [str(executable), "uninstall", "-y", f"--dir={executable.parent}"],
            INSTALL_TIMEOUT,
        )
        if result.returncode != 0:
            return RemovalResult(
                False,
                "uninstall",
                f"Upstream removal exited {result.returncode}; possible partial removal. Inspect upstream output and retry; no blind cleanup was attempted.",
            )
        try:
            executable.lstat()
        except FileNotFoundError:
            if _read_acquisition_receipt() != receipt:
                raise ValueError(
                    "Acquisition receipt changed; private proof was not cleared"
                )
            _receipt_path().unlink()  # Revoke only our verified private proof, not upstream assets.
            remaining = _alternate_path_entries()
            message = "Canonical native executable removed; indexes retained and adjacent updater left untouched."
            if remaining:
                message += (
                    " Alternate PATH entries remain: "
                    + ", ".join(map(str, remaining))
                    + "."
                )
            return RemovalResult(True, "verification", message, remaining)
        return RemovalResult(
            False,
            "verification",
            "Canonical executable still exists; possible partial removal. Inspect upstream output before retrying.",
        )
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        return RemovalResult(
            False,
            "uninstall",
            f"Native removal failed: {exc}. Possible partial removal; inspect upstream output and retry. No blind cleanup was attempted.",
        )
```

### src/superclaude/cli/install_codebase_memory.py:359-479
```python
def _supervise_native(argv: list[str], timeout: float) -> tuple[int, bool]:
    """Run ONLY in the dedicated helper, which owns no unrelated children.

    Linux adoption also covers double-forks/setsid. ECHILD, not an empty procfs
    snapshot, proves collection is complete. A finite, killable tree is required;
    an uninterruptible kernel task produces an explicit cleanup failure.
    """
    if sys.platform != "linux":
        raise OSError("Native supervision requires Linux")
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER, helper only
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    children_file = Path(f"/proc/self/task/{os.getpid()}/children")
    children_file.read_text()  # Fail before acquisition if procfs is unavailable.
    cancelled = False

    def cancel(signum, frame):
        nonlocal cancelled
        cancelled = True

    signal.signal(signal.SIGTERM, cancel)
    signal.signal(signal.SIGINT, cancel)
    process = subprocess.Popen(argv, shell=False, start_new_session=True)
    deadline = time.monotonic() + timeout
    terminating: float | None = None
    leader_code: int | None = None
    term_sent: set[int] = set()
    kill_sent: set[int] = set()
    while True:
        try:
            while True:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if pid == 0:
                    break
                if pid == process.pid:
                    leader_code = os.waitstatus_to_exitcode(status)
                    process.returncode = leader_code
        except ChildProcessError:
            if leader_code is None:
                raise subprocess.SubprocessError(
                    "Native leader status was not collected"
                )
            return leader_code, terminating is not None
        now = time.monotonic()
        if terminating is None and (cancelled or now >= deadline):
            terminating = now
            if leader_code is None:
                _signal_group(process.pid, signal.SIGTERM)
        if terminating is not None:
            force = now >= terminating + TERMINATE_GRACE
            if now >= terminating + TERMINATE_GRACE + REAP_TIMEOUT:
                raise subprocess.SubprocessError(
                    "Native descendant cleanup incomplete: kill/reap deadline exceeded"
                )
            if force and leader_code is None:
                _signal_group(process.pid, signal.SIGKILL)
            # Only our direct children are signalled. When a parent dies, its
            # descendants become ours; repeat until waitpid reports ECHILD.
            sent = kill_sent if force else term_sent
            for pid in map(int, children_file.read_text().split()):
                if pid not in sent:
                    try:
                        os.kill(pid, signal.SIGKILL if force else signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                    sent.add(pid)
        time.sleep(0.01)


def _run_bounded(
    argv: list[str], timeout: float, *, capture_output: bool = False
) -> subprocess.CompletedProcess:
    """Isolate Linux adoption; never change the hosting CLI's child ownership."""
    cleanup_time = TERMINATE_GRACE + REAP_TIMEOUT + 2
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as result_file:
        process = subprocess.Popen(
            [
                sys.executable,
                "-I",
                "-S",
                str(Path(__file__).resolve()),
                str(result_file.fileno()),
                str(timeout),
                *argv,
            ],
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True,
            errors="replace",
            start_new_session=True,
            pass_fds=(result_file.fileno(),),
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout + cleanup_time)
        except BaseException:
            # Request the helper's own bounded cleanup before reaping it.
            process.terminate()
            try:
                process.communicate(timeout=cleanup_time)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate(timeout=REAP_TIMEOUT)
                raise subprocess.SubprocessError(
                    "Native supervisor stopped responding; descendant cleanup not confirmed"
                )
            raise
        result_file.seek(0)
        try:
            result = json.load(result_file)
        except (ValueError, OSError) as exc:
            raise subprocess.SubprocessError(
                "Native supervisor failed; descendant cleanup not confirmed"
            ) from exc
        if "error" in result:
            raise subprocess.SubprocessError(result["error"])
        if result["timed_out"]:
            raise subprocess.TimeoutExpired(argv, timeout, stdout, stderr)
        return subprocess.CompletedProcess(argv, result["returncode"], stdout, stderr)
```

### tests/cli/test_install_codebase_memory.py:1412-1528
```python
def test_real_coordinators_cross_entry_lifecycle(cross_entry_lifecycle, isolated_home):
    state = cross_entry_lifecycle
    expected = {"type": "stdio", "command": str(state.canonical), "args": []}
    result = state.runner.invoke(state.main, ["install"])
    assert result.exit_code == 0, result.output
    assert result.output.index(native.INSTALL_URL) < result.output.index(
        "fixture native installer invoked"
    )
    assert str(state.canonical) in result.output and "account-wide" in result.output
    assert "companion" in result.output and "indexes are retained" in result.output
    assert state.framework_calls[-1] == "install_user_setup"
    assert state.downloads == state.installs == 1
    assert (
        json.loads(state.config.read_text())["mcpServers"][native.BINARY_NAME]
        == expected
    )
    receipt = native._receipt_path()
    assert receipt.stat().st_mode & 0o777 == 0o600
    assert json.loads(receipt.read_text())["identity"] == native._binary_identity(
        state.canonical
    )
    for args in (["install", "--force"], ["mcp", "--servers", native.BINARY_NAME]):
        result = state.runner.invoke(state.main, args)
        assert result.exit_code == 0, result.output
    assert state.downloads == state.installs == 1
    assert (
        sum(cmd[:3] == ["claude", "mcp", "add-json"] for cmd in state.claude_calls) == 1
    )

    # Remove only the user entry to exercise real cross-entry repair without a download.
    root = json.loads(state.config.read_text())
    del root["mcpServers"][native.BINARY_NAME]
    state.config.write_text(json.dumps(root))
    result = state.runner.invoke(state.main, ["mcp", "--servers", native.BINARY_NAME])
    assert result.exit_code == 0, result.output
    assert state.downloads == state.installs == 1
    assert (
        sum(cmd[:3] == ["claude", "mcp", "add-json"] for cmd in state.claude_calls) == 2
    )

    before_home = {
        str(path.relative_to(isolated_home)): path.read_bytes()
        for path in isolated_home.rglob("*")
        if path.is_file()
    }
    before_config = state.config.read_bytes()
    before_mutations = [
        cmd for cmd in state.claude_calls if cmd[:2] == ["claude", "mcp"]
    ]
    for args in (
        ["mcp", "--servers", native.BINARY_NAME, "--dry-run"],
        ["mcp", "--servers", native.BINARY_NAME, "--uninstall", "--dry-run"],
        ["install", "--list"],
    ):
        result = state.runner.invoke(state.main, args)
        assert result.exit_code == 0, result.output
    assert state.downloads == state.installs == 1 and state.uninstalls == 0
    assert state.config.read_bytes() == before_config
    assert {
        str(path.relative_to(isolated_home)): path.read_bytes()
        for path in isolated_home.rglob("*")
        if path.is_file()
    } == before_home
    assert [
        cmd for cmd in state.claude_calls if cmd[:2] == ["claude", "mcp"]
    ] == before_mutations

    result = state.runner.invoke(
        state.main, ["mcp", "--servers", native.BINARY_NAME, "--uninstall", "--yes"]
    )
    assert result.exit_code == 0, result.output
    assert (
        state.uninstalls == 1 and not state.canonical.exists() and not receipt.exists()
    )
    assert json.loads(state.config.read_text()) == state.root
    assert state.updater.read_bytes() == b"upstream updater fixture"
    assert all(path.read_bytes() == content for path, content in state.keep.items())
    before_update = (list(state.native_calls), list(state.claude_calls))
    result = state.runner.invoke(state.main, ["update"])
    assert result.exit_code == 0, result.output
    assert (state.native_calls, state.claude_calls) == before_update
    assert not state.canonical.exists() and not receipt.exists()
    result = state.runner.invoke(state.main, ["install"])
    assert result.exit_code == 0, result.output
    assert state.downloads == state.installs == 2
    assert state.canonical.is_file() and receipt.is_file()
    assert (
        json.loads(state.config.read_text())["mcpServers"][native.BINARY_NAME]
        == expected
    )
    assert json.loads(receipt.read_text())["identity"] == native._binary_identity(
        state.canonical
    )
    assert all(path.read_bytes() == content for path, content in state.keep.items())
    assert all(not path.exists() and not path.parent.exists() for path in state.scripts)


def test_real_coordinators_native_uninstall_failure_preserves_state(
    cross_entry_lifecycle,
):
    state = cross_entry_lifecycle
    result = state.runner.invoke(state.main, ["install"])
    assert result.exit_code == 0, result.output
    before_config = state.config.read_bytes()
    before_proof = native._receipt_path().read_bytes()
    state.uninstall_fails = True
    result = state.runner.invoke(
        state.main, ["mcp", "--servers", native.BINARY_NAME, "--uninstall", "--yes"]
    )
    assert result.exit_code == 1, result.output
    assert "partial" in result.output.lower() and "retry" in result.output.lower()
    assert state.uninstalls == 1 and state.downloads == state.installs == 1
    assert state.canonical.is_file() and state.config.read_bytes() == before_config
    assert native._receipt_path().read_bytes() == before_proof
    assert not any(cmd[:3] == ["claude", "mcp", "remove"] for cmd in state.claude_calls)
    assert state.updater.read_bytes() == b"upstream updater fixture"
    assert all(path.read_bytes() == content for path, content in state.keep.items())
```

### .dev/tasks/done/TASK-WF-spec-20261019-204314/artifacts/reflect/post-20261020042605/verify-logs/invocations.yaml:1-1
```yaml
[]
```

### .dev/tasks/done/TASK-WF-spec-20261019-204314/artifacts/t6-cli-regressions.txt:33-59
````markdown
Coverage crosswalk (existing cases reused, not duplicated):
AC1 acquisition/reuse/failure/prerequisites: existing native acquisition/postcheck/prerequisite matrix, Tavily-file shared native reuse/repair cases, registry prerequisite contracts and Task 5 mandatory failure/delegation tests; new real cross-entry chain closes default-install versus explicit-MCP reuse/repair/restoration coupling.
AC2 exact user scope/name/transport/argv/rollback: existing Tavily-file malformed/read/absent/shadowing/drift/rollback/secret-argv cases and registry contracts; new chain executes actual exact-user reader and reconciliation across both default/custom config paths with local/project/similar-name sentinels.
AC3 CLI/menu/list/consent/dry-run/mixed gateway validation: existing native-file CLI matrix including gateway curl preflight in both orders, API-key/Auggie consent, list combinations and positive dry-run disclosures remains unchanged; new chain exercises actual lifecycle coordinators behind those entry points and byte-preserving dry-run/list behavior.
AC4 native removal/provenance/retention/partial outcomes: existing native-file ownership/symlink/hash/receipt/external/alternate/timeout/postcheck cases and Tavily-file absent/partial/user-cleanup cases; new real-coordinator success/failure chain asserts canonical argv, retained graph/updater/config data, proof cleanup and no blind fallback.
AC5 isolation and preserved assertions: existing subprocess capture/monkeypatch and ClickRunner patterns, temporary HOME/config/cache/bin/project sentinels, unknown-command/prompt tripwires and retained benign local Linux timeout fixtures. No real upstream script, native server/uninstaller, Claude CLI or Node/npm installer runs. Existing Auggie/Tavily/update test bodies remain unchanged.
AC6 required executed four-file suite: exact command/exit/result below.

Isolation/limits:
The new fixture intercepts native process boundaries and scoped Claude persistence only; it does not prove upstream companion-file merging, packaged binary behavior, live MCP handshake or indexing. The separately authorized release smoke remains pending. All data is artificial and lives in private pytest temporary directories; no developer HOME/config/index data is read or changed. Existing benign local process-supervision checks remain enabled. No percentage-coverage/mutation campaign was run.

Targeted increment run:
work=$(mktemp -d /tmp/ironclaude-t6-cross.XXXXXXXX) || exit 1; trap 'rm -rf -- "$work"' EXIT
PYTHONDONTWRITEBYTECODE=1 VIRTUAL_ENV=/config/workspace/IronClaude/.venv PYTHONPATH=/config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/src uv run --active --no-sync pytest -p no:cacheprovider --basetemp="$work/tests" /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/tests/cli/test_install_codebase_memory.py -q -k real_coordinators
Exit 0: 4 passed, 132 deselected in 0.47s. These coverage additions passed against existing product logic; no product defect/fix was needed.

REQUIRED FINAL FOUR-FILE COMMAND (exact shell invocation):
work=$(mktemp -d /tmp/ironclaude-t6-suite.XXXXXXXX) || exit 1; trap 'rm -rf -- "$work"' EXIT; PYTHONDONTWRITEBYTECODE=1 VIRTUAL_ENV=/config/workspace/IronClaude/.venv PYTHONPATH=/config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/src uv run --active --no-sync pytest -p no:cacheprovider --basetemp="$work/tests" /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/tests/cli/test_install_codebase_memory.py /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/tests/cli/test_install_mcp_registry.py /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/tests/cli/test_install_mcp_tavily.py /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/tests/cli/test_update_command.py -q
EXIT: 0
RESULT: 242 passed, 1 skipped in 11.26s (243 collected).
The skip is the existing API-key-gated Tavily presence assertion, not a newly disabled test.

Final lint/format/test-only typecheck command:
work=$(mktemp -d /tmp/ironclaude-t6-checks.XXXXXXXX) || exit 1; trap 'rm -rf -- "$work"' EXIT; PYTHONDONTWRITEBYTECODE=1 VIRTUAL_ENV=/config/workspace/IronClaude/.venv uv run --active --no-sync ruff check --no-cache --cache-dir "$work/ruff" /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/tests/cli/test_install_codebase_memory.py && PYTHONDONTWRITEBYTECODE=1 VIRTUAL_ENV=/config/workspace/IronClaude/.venv uv run --active --no-sync ruff format --check --no-cache --cache-dir "$work/ruff" /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/tests/cli/test_install_codebase_memory.py && PYTHONDONTWRITEBYTECODE=1 VIRTUAL_ENV=/config/workspace/IronClaude/.venv uv run --active --no-sync mypy --follow-imports skip --ignore-missing-imports --cache-dir "$work/mypy" /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP/tests/cli/test_install_codebase_memory.py
EXIT: 0
RESULT: All checks passed! / 1 file already formatted / Success: no issues found in 1 source file.
The same test-only mypy invocation was green before edits. This is a changed-test-file result, not a claim that product/repository mypy is green; the two previously documented product legacy diagnostics were not changed or hidden by a new suppression.
````

## Coverage slice
| Task | AC count | Recorded-tree hunk IDs | Semantic status |
|---|---:|---|---|
| T1 | 7 | H-020, H-037 | independent assessment required |
| T3 | 7 | H-020, H-027, H-037, H-040 | independent assessment required |
| T6 | 6 | H-037 | independent assessment required |

Hunk attribution is mechanical provenance, not a semantic pass. Every reviewer also adjudicates the three compatibility candidates using common hunks; coverage task assignments above prevent silent omissions.
Fresh verification invocations: 0 (sanctioned execution tool unavailable). Historical results are not new execution. Dynamic Click surface reachability is conservatively degraded, never declared unreachable from a missing static referrer.
