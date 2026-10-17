Source excerpt: .dev/tasks/done/TASK-RF-20260604-042055/research-notes.md, line 22

- **S4 TOKEN-SET TRIM (in-scope cleanup, user-mandated):** S4 dependency-token set in the proposal is `{after Phase \d+, blockedBy:, depends on N\.\d+, after N\.\d+}`. TRIM to **drop `blockedBy:` and `after N\.\d+`, KEEP `after Phase \d+` and `depends_on:`** → final S4 set = `{after Phase \d+, depends_on:}`. (Rationale: blockedBy:/after N.N are not real emitted patterns, mirroring the proposal's own S7/multifile drops.) Note `depends_on:` (underscore) replaces the proposal's prose `depends on N.\d+`.
