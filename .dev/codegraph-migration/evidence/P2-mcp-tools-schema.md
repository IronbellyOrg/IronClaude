Bytes delta D: 7597
Model-facing delta: 7107
Instructions bytes run1/run2: 1157/1157
Per-tool bytes: codegraph_explore=1747 (run 1 only), codegraph_search=1132, codegraph_callers=1096, codegraph_callees=1052, codegraph_impact=1028, codegraph_node=2887, codegraph_status=741, codegraph_files=1402
D without node (data only, P3-D1 owns any smaller list): 4710
Band: undecided
Explore hidden: yes
Explore call blocked: yes
Session measurement: run1-default=36980, run2-seven=38841, run3-default=36980, run4-seven=38841 tokens (input+cache_creation+cache_read); T=1861; guards a-d hold (T >= D/5 = 1519)
Deferred: no
Decided by: B
Claude Code version: 2.1.314 (Claude Code)
Model: haiku
INV-015: waived (Leg B used a codegraph-only config; the delta is additive and the retire step removes the codebase-memory registration once codegraph is ready, spec 2.12)
Threshold status: proposed, not user-confirmed
Selected MCP_TOOLS: node,search,callers,callees,impact,files,status
