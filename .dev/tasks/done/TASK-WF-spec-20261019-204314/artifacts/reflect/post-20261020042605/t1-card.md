# Tier 1 candidate reflection card

Independent root-cause analyst return, condensed without adjudicating its findings. **Candidate classifications and totals below are not the final audit verdict.** No fresh test/command execution was performed by this reviewer.

## Claim and evidence classes

The reviewer declares source-reading conclusions on the current tree, not runtime proof. Evidence S = current source Read; T = test bodies Read but not run; D = docs Read; H = archived execution artifacts not rerun; I = index/LSP context not proof. The historical 242-pass/1-skip result is H. Pyright cannot-resolve-click/native-import messages are unresolved analyzer import context, not evidence that code is absent.

The reviewer read all eleven delivery files under the exact worktree plus plan/source/operator direction, per-hunk evidence, review context and t1/t6/t7 artifacts. Its caller regex search used a main-checkout index over src/tests/scripts/plugins, not the working-tree existence oracle; the reviewer explicitly disclaims index-based absence proof. It read the actual main.py caller and found the new signature consumed. It did not use augment_code_search.

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

## Grounding and production wiring

- Native discovery: src/superclaude/cli/install_codebase_memory.py:529-568; acquisition:571-701; argv runner:429-479; HTTPS download:631-651; full Bash script with explicit directory and no config suppression:663-666; absolute version probe:674; isolated Linux supervisor:359-426. Current test bodies: tests/cli/test_install_codebase_memory.py:48-203,249-300,323-461.
- Registry/native dispatch: src/superclaude/cli/install_mcp.py:101-108,1011-1014. Shared install/read/reconcile/restore:815-899. Registration fixture/cases: tests/cli/test_install_mcp_tavily.py:382-818.
- Native preview/removal: src/superclaude/cli/install_codebase_memory.py:225-349. User-only residual cleanup/orchestration: src/superclaude/cli/install_mcp.py:902-993.
- MCP flat options: src/superclaude/cli/main.py:285-343; selection orchestration: src/superclaude/cli/install_mcp.py:1229-1359; mixed execution aggregation:1335-1359.
- Framework native phase and exit aggregation: src/superclaude/cli/main.py:254-275. Update is unchanged:352-431. Read-only list:161-186.

Source wiring: main.install calls shared native setup after user setup and consumes native_success in exit status. main.mcp consumes orchestration success/message. install_mcp_server returns the native boolean, which the selection loop aggregates. RemovalResult.remaining and RemovalPreview.state are consumed. No sentinel-only required capability was found by source reading. Cross-entry tests and real local supervisor fixtures exercise production coordination but do not prove upstream behavior.

## Candidate deviations

### W1-A1: Linux-only automation

Reviewer category: **authorized**. macOS/Windows reject before effects at src/superclaude/cli/install_codebase_memory.py:582-595 and src/superclaude/cli/install_mcp.py:486-496. Authority: artifacts/operator-direction.md exact operator quote and declared interpretation; documentation: docs/user-guide/mcp-installation.md:9. The original macOS wording is frozen provenance, not silently rewritten.

### W1-N1: Receipt-gated removal and provenance acquisition stage

Reviewer category: **necessary**. Anchors: never guess ownership; T3 AC2 fails closed on ambiguity. Existing/manual/reused canonical binaries are not adopted, per tests/cli/test_install_codebase_memory.py:558. Preview may be ambiguous at native source:258; removal is refused. Docs disclose the stricter eligibility at docs/user-guide/mcp-installation.md:223. Reviewer notes an operator could judge the stricter interpretation drift because the original source calls canonical installations removable; no definitive drift classification is asserted here.

### W1-N2: Read user JSON rather than unscoped CLI get

Reviewer category: **necessary**. Anchors: exact user scope and shadowing safety. src/superclaude/cli/install_mcp.py:730-736 reads the default or CLAUDE_CONFIG_DIR .claude.json layout. The reviewer did not independently reverify this external CLI layout/grammar; that is an evidence limitation, not demonstrated invalid syntax.

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

## Reviewer recommendations pending calibration/debate

- Decide W1-D1 semantics using full source before requesting any change; proposed verifier would be isolated CliRunner install-all project/Windows cases.
- Evaluate W1-D2/W1-D3 against security constraints before loosening permissions or resolving symlinked HOME. Proposed verifier would use isolated chmod/symlink fixtures; none were executed.
- Keep receipt eligibility explicit; a CLI refusal-message case could improve visibility if needed.
- Use fresh scoped verification only through the protocol's available sanctioned surface; the live upstream procedure remains separately authorized. The parent has no exposed Serena execute_shell_command, so source-only results must not be represented as fresh test execution.

No final calibrated confidence is assigned by this card. No product edits or remediation are authorized.
