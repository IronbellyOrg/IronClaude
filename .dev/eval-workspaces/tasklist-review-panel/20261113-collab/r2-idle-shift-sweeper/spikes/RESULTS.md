# Gate 0 spike results

One line per spike run: `<UTC> <spike> PASS|FAIL evidence=<path> <detail>`.

- 2026-11-13T21:08:03Z H3 FAIL evidence=spikes/out/h3/h3.log 3/4 masked lines absent from the designSpec base; reflect 3/3 clean
- 2026-11-13T21:08:30Z H3 PASS evidence=spikes/out/h3/h3.log 4/4 masked lines absent from their package's base (2 because the file does not exist there yet); .dev/reflect absent 3/3
- 2026-11-13T21:08:35Z Catalogue PASS evidence=spikes/out/catalogue.json audits.py catalogue: violations=0 against the three real ground-truth files
- 2026-11-13T21:10:10Z S0[muse-ember-1.0] PASS evidence=spikes/out/s0/muse-ember-1.0/s0.json tool_use=10 hook_calls=10 order='seal deliver ' p95_ms=73 max_ms=73 delivered_in_transcript=true 
- 2026-11-13T21:10:49Z S0[gpt-6-luna] PASS evidence=spikes/out/s0/gpt-6-luna/s0.json tool_use=10 hook_calls=10 order='seal deliver ' p95_ms=81 max_ms=81 delivered_in_transcript=true 
- 2026-11-13T21:10:49Z S0 PASS evidence=spikes/out/s0 both models
- 2026-11-13T21:14:38Z S2[muse-ember-1.0] PASS evidence=spikes/out/s2/muse-ember-1.0/s2.json resume_model=muse-ember-1.0 stream_lines=16 first_line_ms=1052 wall_ms=4184 result='beta' 
- 2026-11-13T21:14:46Z S2[gpt-6-luna] PASS evidence=spikes/out/s2/gpt-6-luna/s2.json resume_model=gpt-6-luna stream_lines=15 first_line_ms=997 wall_ms=3564 result='beta' 
- 2026-11-13T21:14:59Z S2[claude-sonnet-5-5] PASS evidence=spikes/out/s2/claude-sonnet-5-5/s2.json resume_model=claude-sonnet-5-5 stream_lines=15 first_line_ms=1077 wall_ms=5094 result='beta' 
- 2026-11-13T21:15:06Z S2[claude-haiku-5-5] PASS evidence=spikes/out/s2/claude-haiku-5-5/s2.json resume_model=claude-haiku-5-5 stream_lines=18 first_line_ms=1094 wall_ms=4006 result='beta' 
- 2026-11-13T21:15:06Z S2 PASS evidence=spikes/out/s2 four models
- 2026-11-13T21:22:24Z SW-1[TASK-WF-designSpec-20261107-075614] PASS evidence=spikes/out/sw1/TASK-WF-designSpec-20261107-075614 accepted=4 by_from={"sw-1":4} rejected={"bad_cmd":1} model_ok=true
- 2026-11-13T21:22:24Z SW-1[TASK-WF-makeTheAliasOnly-20261105-051649] PASS evidence=spikes/out/sw1/TASK-WF-makeTheAliasOnly-20261105-051649 accepted=4 by_from={"hv-1":1,"sw-1":3} rejected={"bad_cmd":1,"over_cap":1,"too_long":1} model_ok=true
- 2026-11-13T21:22:25Z SW-1[TASK-WF-design-20261108-041415] PASS evidence=spikes/out/sw1/TASK-WF-design-20261108-041415 accepted=4 by_from={"sw-1":4} rejected={} model_ok=true
- 2026-11-13T21:22:25Z SW-1 PASS evidence=spikes/out/sw1 packages_with_fact=3/3 model_ok=3/3
- 2026-11-13T21:32:18Z REQ-S3[muse-ember-1.0/probe] FAIL evidence=spikes/out/reqs3/muse-ember-1.0/probe/summary.json act_rate=0/4 model_ok=5/5
- 2026-11-13T21:32:18Z REQ-S3[muse-ember-1.0/finish] PASS evidence=spikes/out/reqs3/muse-ember-1.0/finish/summary.json act_rate=0/5 model_ok=5/5
- 2026-11-13T21:32:18Z REQ-S3[gpt-6-luna/probe] PASS evidence=spikes/out/reqs3/gpt-6-luna/probe/summary.json act_rate=4/5 model_ok=5/5
- 2026-11-13T21:32:18Z REQ-S3[gpt-6-luna/finish] PASS evidence=spikes/out/reqs3/gpt-6-luna/finish/summary.json act_rate=5/5 model_ok=5/5
- 2026-11-13T21:32:18Z REQ-S3 FAIL evidence=spikes/out/reqs3 rates recorded per model and mode
- 2026-11-13T21:32:55Z REQ-S3[muse-ember-1.0/probe] PASS evidence=spikes/out/reqs3/muse-ember-1.0/probe/summary.json act_rate=0/4 model_ok=5/5
- 2026-11-13T21:32:55Z REQ-S3[muse-ember-1.0/finish] PASS evidence=spikes/out/reqs3/muse-ember-1.0/finish/summary.json act_rate=0/5 model_ok=5/5
- 2026-11-13T21:32:55Z REQ-S3[gpt-6-luna/probe] PASS evidence=spikes/out/reqs3/gpt-6-luna/probe/summary.json act_rate=4/5 model_ok=5/5
- 2026-11-13T21:32:55Z REQ-S3[gpt-6-luna/finish] PASS evidence=spikes/out/reqs3/gpt-6-luna/finish/summary.json act_rate=5/5 model_ok=5/5
- 2026-11-13T21:32:55Z REQ-S3 PASS evidence=spikes/out/reqs3 rates recorded per model and mode
- 2026-11-13T21:39:26Z S3 FAIL evidence=spikes/out/s3/check.json AC-2=true AC-2b=true AC-4=false AC-5=false AC-6=false AC-7=true AC-9=false AC-10=true
- 2026-11-13T21:55:56Z S3 FAIL evidence=spikes/out/s3/check.json AC-2=true AC-2b=true AC-8=false AC-9=true AC-10=true
- 2026-11-13T23:01:47Z S3 FAIL evidence=spikes/out/s3/check.json AC-2=true AC-2b=true AC-4=false AC-5=true AC-6=false AC-7=true AC-8=false AC-9=true AC-10=true
- 2026-11-13T23:02:08Z S3 PASS evidence=spikes/out/s3/check.json re-check after audit rule fix (no new model runs): AC-2=true AC-2b=true AC-4=true AC-5=true AC-6=true AC-7=true AC-8=true AC-9=true AC-10=true
