# Tasklist — events durable persistence

- [x] T1: Wire `EventEmitter.publish()` to persist domain events to the contracted durable
  sink (AC-1, `durable_sink: postgres.events_table`). Verified by the journald `EventEmitted`
  proxy oracle.
