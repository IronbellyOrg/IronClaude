### F-17 (MINOR, MEDIUM): WC-10 boundary and cadence are not specified at the threshold

- Location: line 68 (WC-10: heartbeat every 5 minutes; split waits "longer than 5 minutes" into at most 4 minutes); line 181 (7.2 step 2: `worker-show` at least once per 5 minutes).
- Issue: a call of exactly 300 s is not covered (the rule says "longer than"). A step of 4 min 59 s plus model time can exceed the 5-minute heartbeat cadence, and the spec does not say whether the heartbeat is sent between calls only.
- Recommendation: say "at most 4 minutes" applies to any call of 5 minutes or more, and state that the heartbeat cannot be sent during a tool call.
- Expert: Nygard (failure and liveness timing).
