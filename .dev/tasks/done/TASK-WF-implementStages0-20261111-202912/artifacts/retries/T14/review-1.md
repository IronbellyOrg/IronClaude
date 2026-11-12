f5f5bf5ce244f54671da2c08499b6711982c3329
A1 r1-1 (opus, general-purpose): 4 confirmed blocking findings, verified by the orchestrator against the probe transcripts before acting (jq on agent-<id>.jsonl, saved in probe-models.txt).
F1.1 ac=T14.AC2 s-id-results.md:38 blocking: 'model-id exposure no' is false; transcripts record message.model.
F1.2 ac=T14.AC2 s-id-results.md:34 blocking: identity_source decided requested-pinned although a model id is exposed.
F1.3 ac=T14.AC2 s-id-results.md:27 blocking: '3 of 3 consistent' is false for haiku (ran gpt-6.1-sol).
F1.4 ac=T14.AC1 s-id-results.md:9 blocking: exposed model ids missing from the model-id column.
