# Proposal 2 — Refactorer

Integrate flags through narrow seams: one evaluator interface, one config loader, and call-site helpers that make stale flag removal cheap. Require every flag to declare an expiry and fail CI when expired flags are still referenced.
