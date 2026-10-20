# Reflect post-execution report: TASK-WF-spec-20261019-204314

```yaml
contract_version: 1.8.0
status: partial
needs_human_decision: true
mode: post
tier_reached: 2
confidence_calibrated: 0.76
citations_total: 22
citations_revalidated: 22
citations_dropped: 0
citations_inferred: 5
citation_budget_policy: full_reread
reachability_gate_ran: false
reachability_ledger_path: null
reachability_requirements_scanned: 0
reachability_unreachable: 0
reachability_unproven: 0
reachability_real_boot_ran: false
reachability_skip_reason: no-side-effect-requirements
```

## Summary

Post-execution audit of the Codebase Memory MCP default-install and lifecycle work (seven tasks, eleven delivery files) against `source.md`, the archived plan, and `progress.md`. Tier 2: three restricted reviewers on different model classes, independent blind calibration (0.71, 0.78, 0.80), adversarial merge (`merge_method: adversarial`, convergence 1.0).

Verdict: **partial**. No Regression. Three Drift findings (one LOW-MEDIUM, two conditional on host state), one Necessary deviation, one Authorized expansion. Five grounding gaps remain, including the unexecuted live smoke release gate (source.md:151), so the work is mock-conformant but not release-verified.

Report deviation numbers map to the merged verdict and ledger IDs as: D-1 = D1, D-2 = D1-explicit, D-3 = D2, D-4 = D3, D-5 = D5. Merged candidate D4 is Gap G-5.

## Deviations

Counts: authorized 1, necessary 1, drift 3, regression 0. No Regression was established by the Tier 2 ensemble. Full register: `deviation-ledger.yaml`.

### Deviation D-1: Menu option 0 at project/local scope or non-Linux rejects the whole install-all selection

- **Location:** src/superclaude/cli/install_mcp.py:1311-1314
- **Mapped tasklist item:** T4
- **Spec section:** source.md §3 MCP menu (source.md:78, source.md:80); §7 acceptance (source.md:143)
- **Evidence:** Option `0` sets `selected = list(MCP_SERVERS)` (src/superclaude/cli/install_mcp.py:1284-1285); when `codebase-memory-mcp` is in the selection and `_native_selection_error(scope)` returns a message, the function returns `False, invalid` for the whole selection (src/superclaude/cli/install_mcp.py:1311-1314). That helper rejects any non-user scope and any non-Linux amd64/arm64 host (src/superclaude/cli/install_mcp.py:486-496). Spec: "Installation option 0 includes the new individual server" (source.md:78); "Other servers retain their existing scopes" (source.md:80); "install-all includes it" (source.md:143). The only option-0 test runs at user scope (tests/cli/test_install_codebase_memory.py:944-952).
- **Classification:** drift
- **Classification rationale:** Behavior not mapped to any task criterion and no inline rationale; a compliant reading exists (install the other servers and visibly skip Codebase Memory). It contradicts no explicit acceptance criterion, so not Regression. Merged confidence 0.57; one reviewer dissents with Regression-LOW.
- **Default remediation:** Decide whether option 0 should install the other servers with a printed skip, or document the limit in the guide.

### Deviation D-2: Explicit native-plus-other selection at an unsupported scope or platform is rejected before effects

- **Location:** src/superclaude/cli/install_mcp.py:1311-1314
- **Mapped tasklist item:** T4
- **Spec section:** source.md §3 (source.md:78, source.md:80)
- **Evidence:** Tests assert that `-s airis-mcp-gateway -s codebase-memory-mcp` at project/local scope, or on Darwin, exits nonzero with no calls or processes (tests/cli/test_install_codebase_memory.py:964-988).
- **Classification:** necessary
- **Classification rationale:** The spec asks both to process explicit gateway-plus-native selections (source.md:78) and to reject project/local Codebase Memory scope before any effect (source.md:80). Rejecting before effects satisfies the safety requirement. Unanimous across reviewers.
- **Default remediation:** Add a guide note that a mixed explicit selection with an unsupported scope is rejected as a whole.

### Deviation D-3: A group-writable canonical directory makes native install and removal fail closed

- **Location:** src/superclaude/cli/install_codebase_memory.py:85-99
- **Mapped tasklist item:** T2, T3
- **Spec section:** source.md §5 step 7 (source.md:114)
- **Evidence:** `_check_install_directory` raises when `~/.local` or `~/.local/bin` has `st_mode & 0o022` (src/superclaude/cli/install_codebase_memory.py:85-99); `_binary_identity` applies the same rule to the executable (src/superclaude/cli/install_codebase_memory.py:110-116). The spec sanctions failing closed on "Ambiguous discovery or failed probes" (source.md:114) but states no permission-mode rule.
- **Classification:** drift
- **Classification rationale:** An unstated strictness rule with no fixture covering it. Reachable only when the host directory is group- or world-writable (for example created under umask 002), which was not observed. Conditional label, merged confidence 0.60; one reviewer holds advisory-only.
- **Default remediation:** Document the permission rule and recovery, or add a 0775 fixture and decide whether to relax it.

### Deviation D-4: The user-facing error for a symlinked HOME ancestor drops the offending path

- **Location:** src/superclaude/cli/install_mcp.py:572-579
- **Mapped tasklist item:** T3, T4
- **Spec section:** source.md §5 step 7 (source.md:114)
- **Evidence:** Discovery records `f"Symlinked canonical directory: {directory}"` (src/superclaude/cli/install_codebase_memory.py:539-544), but the prerequisite error shown to the user is the fixed sentence "Native executable discovery is ambiguous or externally non-runnable; resolve it before installation" (src/superclaude/cli/install_mcp.py:572-579).
- **Classification:** drift
- **Classification rationale:** Unmapped, no rationale, contradicts no criterion. Conditional on a symlinked HOME ancestor. Merged confidence 0.60; one reviewer holds advisory-only. (Wave 5 re-read narrowed the merged claim: the path is recorded by discovery and lost at the user-facing message.)
- **Default remediation:** Append the discovery message to the prerequisite error.

### Deviation D-5: Automated Codebase Memory lifecycle is Linux-only

- **Location:** src/superclaude/cli/install_mcp.py:486-496
- **Mapped tasklist item:** T1
- **Spec section:** source.md §4 acquisition step 1 (source.md:90)
- **Evidence:** The spec lists "Initial automated support: Linux and macOS" (source.md:90). Operator direction: "there is absolutely no reason to overcomplicate anything in order to preserve macOS portability", and "automated macOS support may be excluded and documented" (artifacts/operator-direction.md:5-7). Cost: the default install exits 1 when the native phase fails (src/superclaude/cli/main.py:255-275), which includes macOS.
- **Classification:** authorized
- **Classification rationale:** Scope narrowing explicitly permitted by recorded operator direction. Merged confidence 0.88.
- **Default remediation:** None; keep the macOS limitation documented.

## Grounding Gaps

Five rows in `grounding-gaps.yaml`; each forces `status: partial`, and G-4 and G-5 need a user decision.

### Gap G-1

- **Hunk ref:** all eleven delivery files (current audit verification surface)
- **Evidence missing:** A fresh scoped test/lint/type-check run through the protocol's sanctioned execution tool; that tool is not exposed in this context and the project read-only setting cannot be fingerprinted.
- **Why not classifiable:** Historical passing tests do not establish a fresh verified result; this is a capability gap, not proof of a regression.
- **Next evidence needed:** A sanctioned execution-capable audit context, or separately recorded fresh verification.

### Gap G-2

- **Hunk ref:** src/superclaude/cli/main.py command decorators (`install`, `mcp`)
- **Evidence missing:** Sound dynamic Click registration reachability.
- **Why not classifiable:** Click decorator registration is a dynamic oracle case; static analysis must degrade rather than claim reachability.
- **Next evidence needed:** A dependency-aware resolver context or an observed entrypoint run in an authorized isolated environment.

### Gap G-3

- **Hunk ref:** src/superclaude/cli/install_codebase_memory.py:85-116 (D-3 reachability, invariant INV-002)
- **Evidence missing:** Observed modes of `~/.local` and `~/.local/bin` on target hosts, upstream `install.sh` directory-mode behavior, and a 0775 fixture.
- **Why not classifiable:** D-3's severity depends on unobserved host state.
- **Next evidence needed:** A 0775 canonical-directory fixture covering first install, retry, and removal.

### Gap G-4

- **Hunk ref:** source.md:151 (live smoke release gate, invariant INV-005)
- **Evidence missing:** The separately authorized live smoke test in a disposable user environment. No task criterion anchors it and it has not run.
- **Why not classifiable:** The spec says "mocked tests cannot prove upstream merge safety" (source.md:151); all task criteria are mock-conformant only.
- **Next evidence needed:** Run the live smoke in a disposable HOME and record companion-file preservation, idempotent reinstall, and index-retaining uninstall.

### Gap G-5

- **Hunk ref:** src/superclaude/cli/main.py:326-330 (deviation candidate D4)
- **Evidence missing:** A contract decision on whether `--list` may combine with `--dry-run` or `--scope`.
- **Why not classifiable:** Code rejects `--list` combined with `--dry-run` or a non-user scope, among other combinations (src/superclaude/cli/main.py:326-330). The spec only forbids combining `--list` "with mutation modes" (source.md:76), and dry-run performs no downloads, config changes, deletion or prompts (source.md:117, source.md:145). Reviewers split at confidence 0.55 between harmless tightening and Drift.
- **Next evidence needed:** A user decision on accepting `--list --scope project`; then classify against it.

## Reachability & Oracle Admissibility

Contracted-sink gate skipped: `reachability_skip_reason: no-side-effect-requirements` (no `durable_sink:` / `@sink` annotation in the spec or plan; telemetry only, not a gap). Required-capability pass (static): the default `superclaude install` path invokes the Codebase Memory phase and consumes its result, exiting 1 on failure (src/superclaude/cli/main.py:255-275). Reached; `reachability_unreachable: 0`.

## Runtime-surface reachability

Sweep ran over two Click command callbacks (`install` for T5, `mcp` for T4). Both reduce to DEGRADE under the decorator oracle; none UNREACHED (`runtime_surface_unreached: 0`, `unreached_surfaces: []`). Recorded as Gap G-2. Ledger: `artifacts/runtime-surface-ledger.yaml`.

## Per-Task Verdicts

All seven tasks are logged complete in `progress.md`. Every task is mock-conformant only: no fresh verification ran and the live smoke gate (G-4) is outstanding, so none is `success`.

### Task T1

- **Status:** partial
- **Deviation class:** authorized
- **Citations dropped:** 0
- **Per-task validation strength:** 0.76
- **Evidence anchor:** src/superclaude/cli/install_mcp.py:486-496

### Task T2

- **Status:** partial
- **Deviation class:** drift
- **Citations dropped:** 0
- **Per-task validation strength:** 0.60
- **Evidence anchor:** src/superclaude/cli/install_codebase_memory.py:85-99

### Task T3

- **Status:** partial
- **Deviation class:** drift
- **Citations dropped:** 0
- **Per-task validation strength:** 0.60
- **Evidence anchor:** src/superclaude/cli/install_mcp.py:572-579

### Task T4

- **Status:** partial
- **Deviation class:** drift
- **Citations dropped:** 0
- **Per-task validation strength:** 0.57
- **Evidence anchor:** src/superclaude/cli/install_mcp.py:1311-1314

### Task T5

- **Status:** partial
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** 0.76
- **Evidence anchor:** src/superclaude/cli/main.py:255-275

### Task T6

- **Status:** partial
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** 0.76
- **Evidence anchor:** tests/cli/test_install_codebase_memory.py:944-952

### Task T7

- **Status:** partial
- **Deviation class:** none
- **Citations dropped:** 0
- **Per-task validation strength:** 0.76
- **Evidence anchor:** (no evidence anchor re-read in Wave 5; see adversarial/merged-verdict.yaml tasks.T7)

Validation strength is the mean Tier 2 calibrated confidence (0.76) for tasks without a deviation, and the merged label confidence for tasks carrying a Drift.

## Advisories (not deviations)

Carried from the merged verdict (`adversarial/merged-verdict.yaml` correctness_advisories); not re-read in Wave 5, so each is tagged inferred:

- [INFERRED] `claude --version` runs twice on the user/Linux install path.
- [INFERRED] Registration restore through `add-json` passes the prior entry, which may hold secret values, on the process argument list.
- [INFERRED] `AcquisitionResult.acquired` is consumed only by tests.
- [INFERRED] The canned `mcp_cli` fixture proves dispatch only; the `& 0o022` branches are never exercised by a test.
- [INFERRED] The user guide never names option 0's limits or the group-writable permission rule.

## Inferred-claim audit

- `citations_inferred: 5`
- Inferred-fraction: `5 / 22` = 0.23
- Evidence-validator: 22 of 22 citations re-read, 0 dropped, verdict PASS (`artifacts/evidence-validator.yaml`). A zero-drop pass is recorded as `zero-drop-flag: true` in `audit.log` for meta-eval spot-check.

## Recommendations

### Recommendation R-001: Run the live smoke release gate

- **File:** n/a (disposable user environment per source.md:151)
- **Change:** Perform default setup, inspect companion-file changes, register and query the server, reinstall for idempotence, then uninstall while retaining index sentinels.
- **Verifier:** A recorded smoke log showing preexisting hooks preserved and index sentinels retained; Gap G-4 closed.
- **Linked deviation(s):** none (Gap G-4)
- **Priority:** P0

### Recommendation R-002: Make menu option 0 skip Codebase Memory visibly instead of rejecting install-all

- **File:** src/superclaude/cli/install_mcp.py
- **Change:** When option 0 is chosen and `_native_selection_error(scope)` is non-empty, drop `codebase-memory-mcp` from the selection with a printed skip notice instead of returning at lines 1311-1314; or, if the rejection is intended, document it in docs/user-guide/mcp-installation.md.
- **Verifier:** New test: option 0 at `--scope project` and on Darwin installs the other servers and prints the skip; `uv run pytest tests/cli/test_install_codebase_memory.py -v` passes.
- **Linked deviation(s):** D-1
- **Priority:** P1

### Recommendation R-003: Cover and document the group-writable directory rule

- **File:** tests/cli/test_install_codebase_memory.py
- **Change:** Add a 0775 canonical-directory fixture for first install, retry, and removal; document the permission rule and its recovery in the guide.
- **Verifier:** The new test asserts the chosen behavior; `uv run pytest tests/cli/test_install_codebase_memory.py -v` passes.
- **Linked deviation(s):** D-3
- **Priority:** P1

### Recommendation R-004: Show the offending path in the discovery prerequisite error

- **File:** src/superclaude/cli/install_mcp.py
- **Change:** Append `found.message` to the error added at lines 577-579.
- **Verifier:** A symlinked-HOME-ancestor test asserts the directory path appears in the output.
- **Linked deviation(s):** D-4
- **Priority:** P2

### Recommendation R-005: Decide the `--list` combination contract

- **File:** src/superclaude/cli/main.py
- **Change:** After the user decides, either keep the rejection at lines 326-330 and document it, or accept `--dry-run` and `--scope` with `--list`.
- **Verifier:** Gap G-5 closed and a CLI test locks the chosen behavior.
- **Linked deviation(s):** none (Gap G-5)
- **Priority:** P2

## Run limits and promotion

- Resumed run: Waves 0-4 were completed by an earlier session; the input drift recheck matched (`input_tree_sha256` 5142787c..., 62 files), so they were not redone.
- No fresh tests, lint, or build ran: the sanctioned execution tool is not exposed, and no Bash substitute was used (`verification_skip_reason: tool-unavailable`).
- Calibrator diversity degraded (the opus calibrator shares a class with one reviewer); executor model class unresolved.
- Serena project memory was not written: the earlier memory listing pointed at the main checkout, not this worktree (`memory_persist_failed: true`).
- Wave 6 skipped (no `--remediate`). Wave 7 not applicable: the package is already archived under `.dev/tasks/done/`; nothing was moved (`promotion_action: not-applicable`).
