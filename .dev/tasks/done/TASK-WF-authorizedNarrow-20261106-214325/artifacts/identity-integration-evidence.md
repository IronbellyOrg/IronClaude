# Scoped job identity integration evidence

## Scope and authorization
The owner authorized a narrowly scoped launcher/harness identity integration on 2026-11-06. This package implements that foundation, not the full issue-394 classifier, claim pipeline or production Git-hook deployment. The prior blocked plan is preserved and is not declared compliant.

## Actual isolated CLI observations
Redacted actual events are in ./live-harness-events.jsonl. Rows 1-3 show the governed PreToolUse rewriting the Bash input without a permissionDecision, PostToolUse receiving the changed command hash, selector output matching the original logical session UUID, and CLI exit 0. Rows 4-6 show an ordinary session with unchanged input hash, no rewrite, selector ordinary, and CLI exit 0. Both execute in a disposable fixture, not global settings or the real origin. No nested-session guard was bypassed.

## Runnable lifecycle and real-Git checks
The seven actual local-Git cases passed (integration-tests.log:12-27). Concurrent same-clone human pushes to main and master were selected ordinary and advanced the fixture refs. The old governed background jobs retained origin old and were refused; the fixture refs remained at the human commits. After explicit release, those jobs reported ordinary/released and the fixture refs advanced to their commits. Exact-name edges feature/main and main-extra were accepted. Two newly created jobs for the same logical ID were both recognized and refused, labelled controlled resume rather than CLI resume.

Two limit cases are intentionally not enforcement passes: deliberate setsid escape was unselected and advanced the local fixture main; killed-supervisor identity was unknown and the positive-only TEST policy allowed it, also advancing the fixture. Both are recorded as support ceilings, never trusted-human proofs. The pre-push policy belongs only to the tests; no production O-22 installation is delivered. Logs contain hook selector records and before/after local bare-remote refs, not merely command statuses.

## Supported contract and remaining prerequisites
The adapter uses the actual tool event session ID to invoke a dedicated per-job Linux process-session supervisor. Background descendants retain that immutable origin while the supervisor remains live; new ordinary calls are not retagged by a shared Claude PID. Permission evaluation is not auto-approved, and rejected rewrites create no command-bearing request. Release is deletion of the origin's governed record.

Wrapped internal cd is local to one fresh shell; ordinary background descendants delay completion by design. Intentional new-session daemonization, supervisor killing, malicious same-user state edits, relocated HOME/store context, Monitor, remote jobs and other execution surfaces are outside the supported transparent contract. Unknown identity is not a proven human. Hosts without a usable runtime/parser cannot advertise adaptation.

Actual /clear, resume, auto-mode, concurrent-hook rewrite composition, persistent-cwd tracking, harness background scheduling and nested-subagent event variants were not observed by the two live CLI runs. Direct hook payload/subprocess tests are labelled as such, not upgraded into those observations. Claim launcher provisioning/effective-runtime preflight and production pre-push policy remain the next integration step. No global installation, real protected-ref write or permission override occurred.

## Verification record
UV-run local-Git selection: 7 passed, 129 deselected in 5.76s (integration-tests.log:27). The full affected regression run observed 416 passed in 35.60s (line 459), and serial sync tests observed 7 passed in 6.64s (line 477). The log retains the initial test-fixture Ruff import-spacing issue and its correction before final verification (lines 30-32). Earlier task logs preserve the rejection-ticket and ordinary-missing-UV findings and passing fixes. Source/plugin mirrors and developer sync were verified; generated .claude mirrors are not staged. These are observed scoped checks, not a full-repository test pass or a waiver of remaining lifecycle prerequisites.

The real CLI observation helper is tests/hooks/fixtures/launch_level/live_probe.py. Its captured event set is redacted to identities, field names, command hashes and selector results; credentials, command text, global configuration and unrelated user transcripts are not included. The earlier workflow's advisory reflection remains failed/skipped in its contract due the subagent report-write restriction; no advisory PASS is claimed.
