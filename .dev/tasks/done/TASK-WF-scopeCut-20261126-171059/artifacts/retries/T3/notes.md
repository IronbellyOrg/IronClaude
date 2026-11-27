7d3fba74c50116cec2c2962153a7011f26bb0d72
A1 r1-1 F1.1 minor scripts/apply_org_rulesets.py:453 ac=T3.AC2 amiss=n,false=n,harm=n,constraint=n the commits fallback applies the 90-day cutoff only through the since= query: no client-side date check and no test of an old commit on that source; the AC is met by the server-side filter the plan describes
