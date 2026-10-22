# Reviewer 1 card — analyzer

Requested model slot: sonnet. Evidence is current source/test-body reading only; no execution. This preserves the reviewer's corrected conclusions and explicit unread regions. Earlier brief-offset citations were withdrawn, not accepted as source coordinates. Parent has not adjudicated these claims.

## Assigned completion

- T2 (7 ACs): source-conforming, qualified. Current shared function src/superclaude/cli/install_mcp.py:815-899 is the one native path; scope/platform:819-821, Claude readiness:829-842, notice/acquisition:844-848, absolute/version check:849-855, lookup:857-862, no-op:864-865, remove:867-880, add/verify:881-884, restore:885-899. Native dispatch:1011-1014. Registry/dispatch test bodies: tests/cli/test_install_mcp_registry.py:192-239; current registration tests: tests/cli/test_install_mcp_tavily.py:479-818. These cover no-op/repair/upstream-created entry, shadowing, drift, malformed/read errors, absence, readiness, failure, restoration, timeout and concurrent preservation. Fixtures and separate spaces/Auggie/Tavily compatibility cases were not read; mock fidelity/that portion of AC coverage is unverified by this reviewer.
- T4 (8 ACs): source-conforming except disputed W1-D1 menu slice. Whole-validation native check: src/superclaude/cli/install_mcp.py:1311-1314; uninstall restriction:1306-1310; scope/platform gate:486-496; selected native prerequisites:571-583. The aggregation loop and some main exit handling were read in brief hunks, not independently reread source coordinates. Current tests read: tests/cli/test_install_codebase_memory.py:856-879,944-1014. Other menu, consent, non-TTY and dry-run test bodies remain unverified by this reviewer.
- T5 (7 ACs): source-conforming with test-body qualification. Current main native call is src/superclaude/cli/main.py:255; MCP definition:310; update:352. Native aggregate exit was observed in supplied source hunk, not fully direct-reread. Tests read: tests/cli/test_update_command.py:254-277,293-342,345-375,386-424. Shared-phase repeats are delegation tests, not independent upstream proof. native_phase_guard and installer-stub fixture definitions were not read; isolation remains unverified by this reviewer. Native Mac/Windows required-phase failure follows operator/source platform policy and is authorized, not a separate defect.

## W1-D1 — qualified, split disposition

Explicit mixed selections with native under project/local scope or non-Linux: necessary/contract-consistent; this regression slice is refuted. Full selection validation must precede effects, and invalid native setup cannot be silently dropped. Tests directly assert no calls for project/local and Darwin: tests/cli/test_install_codebase_memory.py:964-988.

Menu option 0 under those same contexts: regression candidate, MEDIUM, but spec-conflicted/debate-open. Option 0 selects every registry entry at src/superclaude/cli/install_mcp.py:1284-1285; native validation at:1311 blocks the entire selection. Earlier non-native install-all could process project scope. Claimed anchors conflict: source §3 preserves existing installation invocations, but also requires option 0 to include native and invalid native scope to reject before writes. Existing option-0 positive test covers Linux/user only (:944-952). The operator direction concerns native portability, not other-server support. Reviewer does not assert the candidate is finally adjudicated.

## W1-D2 — qualified conditional drift, not confirmed regression

Mechanism: src/superclaude/cli/install_codebase_memory.py:85-100,102-116 rejects group/other write for proof identity. Receipt writer:173-201. Discovery/executable inspection at:482-526 uses canonical owner rather than the same mode predicate. Framework ccsession creates the bin directory with process-umask mkdir at src/superclaude/cli/install_ccsession.py:37.

If directories are 0775 and upstream leaves them that way, acquisition can complete upstream, then fail proof creation; shared caller returns false at src/superclaude/cli/install_mcp.py:847-848. The exact provenance call/catch was only brief-confirmed by this reviewer. Retry follows native reuse at:597-605 without adoption; docs/user-guide/mcp-installation.md:223 discloses no receipt on reuse, so automatic removal remains unavailable.

Reviewer classification: conditional drift candidate, not necessity, because fatal provenance is not explicitly in the spec's acquisition/verification/registration failure list; receipt itself is necessary. Reviewer also reasons a new feature has no prior behavior to regress; this rationale is retained for independent taxonomy calibration rather than adopted by parent. Real upstream modes are unknown; the recollection that umask 002 is Ubuntu default is unverified and must not become a factual report claim. No group-writable/umask fixture was observed.

## W1-D3 — regression refuted

Canonical uses Path.home().absolute at native source:54-55; resolve mismatch at:88,:539 makes discovery ambiguous. The resulting discovery failure at:606-607 precedes download. T1 ambiguity and T3 symlink/ownership fail-closed clauses authorize this behavior. It can also block external reuse when a HOME ancestor is symlinked; that is an advisory compatibility limitation, not a demonstrated deviation. Generic prerequisite messaging omits the offending path (:577-579). No symlinked-HOME fixture was seen.

## Other observations / gaps

- Advisory permission-predicate mismatch: provenance/removal versus discovery/reuse.
- A prior entry's secret values may travel in add-json argv during restore. Tests verify messages/captured diagnostics stay clean (tests/cli/test_install_mcp_tavily.py:736-757), not process-table visibility. This is a no-spec advisory, not an asserted diagnostic leak.
- AcquisitionResult.acquired was not consumed in the reviewed shared function; no repository-wide absence search was completed.
- No fresh checks, no actual upstream mode/companion/handshake observation. Live smoke remains an intentional separate release gate.
- Metadata correction replaced wrong shared-function and ccsession offsets with actual current coordinates. Any remaining [brief-only] claim is explicitly unverified, not an invented source read.

## Evidence-only next steps

Adjudicate full-contract menu semantics before any fix. Isolated option-0 project/platform, 0775 preflight/proof/retry and HOME-symlink cases would resolve the identified compatibility gaps. Unread fixture/compatibility-test bodies need source review before claiming complete test fidelity. No fixes or live execution were authorized/performed by this card.
