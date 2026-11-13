# Audit A: model identity and attempts (snapshot 2026-11-13 ~01:12 UTC; eval is still being rerun by others)
Files: /tmp/audit-A/flags.tsv (re-generated without batch 10), /tmp/audit-A/audit.py (repeatable: `uv run --no-project python -I audit.py`), stats.json.
Scope: 890 reviewer runs (batch 10 excluded) (rid files with a final meta.json) across 3 packages, 70 non-contaminated rows; dirs named contaminated/superseded/quarantine skipped.
Runs per family: b4-* 51, c* 30, e* 47, g1-g9 300, h1/h2 120, n* 207, r* 111, terra/sol-alone and terra-* 24 (partial rows hold only their own reviewers; shared reviewers live in sibling rows).

## EXCLUDE (2 runs, 1 root cause)
- b4-muse-luna2 / t2b-1 in makeTheAliasOnly and design: asked for muse-wonder-1.0 (attempt1 init.model and meta.expected_model), served gpt-6.1-terra; model_ok=false in final meta; raw attempt JSON confirms terra. No fallback.log (ran before the ladder). The designSpec copy of the same slot is muse-wonder (cross-package check E10 fires). 
  Paths: <pkg>/reviews/combos/b4-muse-luna2/t2b-1.{md,meta.json,attempt2.json}

## Check results
1 intended == meta.expected == observed (resolution.json, 828 runs): 0 mismatches. For 102 runs with no resolution entry (b4-muse-luna2, c1/c3/c4, e4, i1/i2, n1/n3, n5-muse-glm-luna, n5-sonnet, r1/r3/r4 and slot-shared rows) intended was derived from the row name plus launch scripts /tmp/b10-launch.sh etc: all match, except the b4-muse-luna2 pair above. n5-sonnet t2b/t3 (muse-wonder, glm-5.3) are UNVERIFIED by name but equal the resolved siblings n5-sol/n5-terra.
2 fallback.log present: 0 runs. Caveat: the known overwrite flaw means a silent fallback would hide here; checks E1/E5/E9/E10 below were built to catch that and found only the b4 pair.
3 observed empty, <synthetic> or comma-joined in final meta: 0.
4 independent re-derivation (jq on the final attempt's raw JSON, final attempt = meta.attempt): 0 differences versus meta.json observed_model; final .md byte-identical to attemptN.md in all runs (cmp).
  Method note: "highest attemptN" is wrong for 5 runs, so I used meta.attempt: n5-sol t3-1 (designSpec), n4-sol t3-1 (alias), n5-terra t3-1 (design), r2-terra t4-2 (alias), n4-sol t2b-1 (design). Each has a stale attempt2 left from an earlier run (older mtime, some 0-byte) and a newer attempt1 that produced the final report. Using the highest N would wrongly show a mismatch (e.g. n4-sol t2b-1 stale attempt2 = terra, final attempt1 = muse-wonder). They are WARN stale-attempt-leftover; cost.json in these 5 includes the stale attempts, so their cost totals are inflated.
5 cost.json: attempts count, total tokens and total wall equal the sums of attemptN.meta.json in all 930 runs (0 mismatches); the 5 stale cases above agree internally but over-count.
  Retries (final attempt >= 2): 10 runs WARN. None is an outage (all exit 0/1/124, none 127 or 'native binary'): glm-5.3 t3-1 x7 (attempt1 qwen3.8-max appeared alongside glm in the observed list or timed out at 3000 s; final glm-5.3), b4-muse-luna2 t2b-1 x2 (the EXCLUDE pair), g9-ember-luna-r1 t2b-1 alias (attempt1 ok model, retried on missing findings block).
6 gateway-misrouting signatures: output_tokens_all==0 with model_ok true: 0. Under 400 tokens: 2 WARN (n2-terra designSpec t2-1 347; n5-terra design t2-1 374; terra reports are short, model identity ok). 'unrecognized_model' in .err appears in 744 attempt files: it is a benign Claude Code client warning printed for every non-Claude model name, not a routing error, so not a flag. One other stderr: n5-terra design t3-1 stale attempt2.err (script line error from the earlier run).

## Extra checks I invented
E1 system-init model (the requested model) vs observed, every attempt: differs in 2 runs (the b4 pair). E9 init model varying across attempts of a run: 0.
E2 modelUsage keys beyond the observed model: 59 WARN. 57 are an auxiliary call to alias claude-gw-tier2[1m] (about 512 output tokens, thinking 115, query_source web_fetch_apply) alongside claude haiku/sonnet/grok runs; it is a client side call, not a reviewer turn, but it is counted in output_tokens_all and means a tier2 model touched the run. 2 are the b4 pair.
E3 subagent (parent_tool_use_id != null) turns on another model: 0.
E4 final meta model_ok != true: 2 (b4 pair). E4b findings_block false: 0.
E5 earlier attempt observed a different model from the final: 8 WARN (7 glm 'glm-5.3,qwen3.8-max' attempt1 which is why glm retried; 1 b4 pair row mix of <synthetic>).
E6 identical final report text across different runs (copy contamination): 0.
E7 empty report or 'API Error' report: 0.
E8 report text self-identifying as another model family: 6 WARN, all false positives (phrases like "as GPT" meaning the file under review).
E10 same row+reviewer id uses the same model in all 3 packages: 1 violation (b4-muse-luna2 t2b-1).
E11 run present in sibling packages but missing here: 9 WARN, these are the outage cases below plus e4-haiku2-ember design t2b-1.
R1 resolution lists a reviewer with no run output: 6 WARN (n5-sol, n5-terra t4-1 in each package; shared reviewer lives in another row).

## Batch 10 (i1-grok-sonnet-r*, i2-haiku-sonnet-r*)
Dropped from the study by owner order; skipped entirely in the final flags.tsv. Earlier snapshot only: 8 outage-hit runs sat in quarantine-outage-20261113 dirs (exit 127 or 'native binary not installed', 0 tokens), and their meta expected_model had been overwritten by the fallback ladder.
