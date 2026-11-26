import json
R = json.load(open("/tmp/audit-F/rows.json"))
L = []
for k, v in R.items():
    m = v["m"]
    if m and m["blk"] != m["blk_true"]:
        L.append(f"1-blocking-semantics\t{k}\tdefect-rich(both)\tna\tWARN\tjudge gt_covered_blocking={m['blk']} but only {m['blk_true']} of those GTs are blocking_in_implement in ground-truth.json (report '/8' column mixes the two definitions)")
stale = [
("L114,L132-133,L144", "n2-sonnet-src 8/14, 5/8 still in batch-4/5 table, headline and 'best quality' line; retracted at L146-148 (recomputed 2/14, 0/8, 1 wb)"),
("L163,L167", "'muse-ember is a WEAKER reviewer than muse-wonder' unqualified; only partially qualified at L172 (4 comparisons, n=1 each, within the r2 variance); also L167 'r2-sonnet-src (muse-wonder version)' retracted at L173"),
("L151,L155,L163", "r2-sonnet-ember treated as muse-ember swap of a muse row; r2 has no muse (corrected L170-174, table not amended)"),
("L189-190,L192-193", "'adding haiku or grok bought no measurable catches', 'second run never caught a defect the first lacked (18 cases)', 'haiku overlap 8 of 8' and per-reviewer rates (attrib.py) left unstruck; retracted L195-200"),
("L282", "'second same-model run adds little on defect-rich' cited as row-level evidence; rests on the retracted analysis (batch 8 gives only within-noise deltas, n=4-6)"),
("L53,L67,L102,L21-43,L45,L59-63", "recommendations/rankings/efficiency view still cite pre-source.md rows with luna: r1-haiku-luna2, r3-luna2-grok, c1-haiku-luna, c3-luna-grok, c4-haiku-luna-grok, r4-haiku-luna2-grok, n1-muse-haiku-luna, n3-muse-luna-grok, n5-muse-glm-luna, n5-sonnet; L107 says superseded but text not marked"),
("L86-102", "batch-3 terra/sol rows (r2-terra, r2-sol, n2/n4/n5-terra, n2/n4/n5-sol) and conclusion 'terra and sol return thin incomplete reports ... pure cost' come from the missing-source.md era; not citable for terra/sol"),
("L148,L280,L283", "'r2-sonnet-src 4/8 best blocking recall' and 'c3 cheapest high blocking result 3/8' use judge blocking; true blocking-in-implement GTs caught by a blocking row: r2-sonnet-src 3, c3-luna-grok-src 1"),
("L206-244", "batch-8 'Delta blocking' (+0.50 etc.) uses judge blocking; with true-blocking GTs ember+2x luna is 0.17 vs 0.50 for ember+luna (direction reverses)"),
("L238-240,L244", "'beyond noise' control deltas: 2nd luna survives Welch (p=0.004) and permutation (p=0.048, borderline); 2nd ember (+0.60) does not (Welch 0.070, perm 0.167)"),
("L261-262", "b9 'beyond noise': +1.25 blocking (haiku) Welch p=0.076/perm 0.171; +0.75 control (haiku) 0.058/0.143; +1.25 control (sonnet) Welch 0.017/perm 0.086: only the sonnet control delta passes Welch and none passes permutation at 0.05"),
]
for ref, why in stale: L.append(f"4-stale-claim\t{ref}\tna\tna\tWARN\t{why}")
for p in ("i1-grok-sonnet-r1..r4", "i2-haiku-sonnet-r1..r4"):
    L.append(f"3-completeness\t{p}\tna\tna\tWARN\treviews exist but no scoring dir; names are not valid-era per the stated rule and not in report")
L.append("6-pitfall-elapsed\tall rows\tna\tna\tWARN\t'elapsed' = sum over packages of slowest reviewer assumes full parallelism; quarantined re-runs (h1-r1 alias, h2-r1 design, 42-min Qwen run) excluded from cost.json; load-dependent gateway time")
L.append("6-pitfall-tokens\tall rows\tna\tna\tWARN\tonly output tokens; no input tokens/price; 'found per 100k tokens' favors low-output models")
L.append("6-pitfall-stats\tfamilies\tna\tna\tWARN\truns r1..r4 reuse the same 3 packages (pseudo-replication: generalizes over reviewer sampling only); ~48 tests in 12 comparisons x 4 metrics -> 2-3 false positives expected at 0.05; pooled rows span batches/eras (b4-, e2, e3, n5-sonnet-ember, r1-src)")
open("/tmp/audit-F/flags.tsv", "a").write("\n".join(L) + "\n")
print(len(L))
