# Discriminator: redelivered
Hypothesis A: consumer acks after side-effect, so a crash between send and ack redelivers
Hypothesis B: producer publishes twice on HTTP retry
Observable that differs: redelivered — message header flag, logged at consumer.py:42
Exact probe: SELECT bool_or(redelivered) FROM consumed_log WHERE invoice_id=:id
Primitive under dispute, fetched verbatim: broker doc "Consumer acknowledgements": "If a consumer's channel closes before an ack is received, the message is requeued with redelivered=true."
Reference-context value: false
Pre-registered outcome table (written before the probe runs):
| Probe result | A | B |
|---|---|---|
| true  | consistent | refuted |
| false | refuted | consistent |
Falsifier sentence: "If redelivered=false on the next duplicate, A is false."
Self-consistency: if Reference-context value ≠ the value actually observed in the reference context, mark THIS PROBE `suspect` under Grounding Gaps; do not read the outcome table for it.
