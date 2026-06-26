# Tasklist — events durable persistence (gate disabled run)

- [x] T1: Wire `EventEmitter.publish()` to persist domain events to the contracted durable
  sink (`durable_sink: postgres.events_table`). This case runs `/sc:reflect --no-reachability`
  to exercise the telemetry-only operator rollback path.
