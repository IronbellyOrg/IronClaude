# Spec: Persist domain events to the durable events table

## AC-1 — domain events reach the contracted durable sink

When a domain event is published, the row MUST be persisted to the contracted durable sink.

durable_sink: postgres.events_table

The acceptance/e2e oracle asserts an `EventEmitted` line is written to journald (a PROXY
observable), NOT that the row reaches `postgres.events_table` (the contracted durable sink).
This is the fail-open shape FR-RH1 step 5.6 must catch.
