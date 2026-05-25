# Debate Transcript — Feature Flag System

## Tension 1: Source-backed flags vs hosted UI

Architect argued for source-backed definitions to preserve reviewability. Refactorer agreed for v1 because cleanup automation depends on grep-able definitions. Security rejected a hosted UI until authorization and audit semantics are explicit. Resolution: source-backed registry in v1, UI deferred behind an explicit open question.

## Tension 2: Expressive rules vs safe evaluation

Architect proposed segment predicates. Security rejected arbitrary expressions. Resolution: allow only typed declarative predicates over a whitelisted context schema.

## Tension 3: Kill switch behavior

Refactorer wanted per-call default handling; Security required global emergency override. Resolution: evaluator supports per-flag safe default plus an emergency deny/allow override recorded in audit logs.
