# Task 2 family probe: rejected-call ticket lifecycle

## Scope
The hook publishes a command-bearing request before normal permission checks. Startup traps clean failed starts but cannot clean calls that never start. Any hook test that withholds a successfully rewritten command has the same family defect, not just auto-mode rejection.

## Evidence and excluded fix
Independent reviewer withheld command execution, then consumed the surviving token and executed the saved marker command. Official hooks documentation (fetched 2026-11-06, hooks page PermissionDenied and PostToolUseFailure sections) states PermissionDenied is auto-mode-only and excludes manual denial, deny-rule matches and PreToolUse blocks. PostToolUseFailure excludes pre-execution permission denial. There is no universal documented permission-completion callback; expiry is not synchronous revocation.

## Smallest root-cause fix
Emit only a quoted invocation of a new runner execution mode during PreToolUse, retaining the hook event's session/tool identity and original command as invocation arguments. Do not create requests or jobs until that invocation actually starts after normal permission processing. Inside execution mode, create the one-use private request and consume it immediately using the existing Task 1 runner, with exact-token finally cleanup if startup fails. Preserve original standalone prepare/run interfaces and tests. Reserve the new mode in conflict detection. Bound hook errors stay blocks; ordinary calls stay silent. This is identity binding, not a permission grant.

## Regression family
Withhold a rewritten command and assert zero new request/job files and zero marker side effects; then execute an actually accepted command and assert one-time request consumption and identity selection. Repeat for missing UV/interpreter and release-before-start. Update former tests which assumed pre-publication, rather than pinning the broken lifecycle. Do not add denial-event hooks or permissionDecision allow.
