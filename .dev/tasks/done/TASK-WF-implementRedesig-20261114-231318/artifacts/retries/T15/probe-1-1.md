f76bd67f8f5e0113575b2bf856dad506a59ee6d2
family: metrics-12.5-partial (a metric named in RL/DESIGN.md 12.5 that analysis/analyze.py does not define or report)
defect form: the metrics over_budget, recipe_missing, unknown_item, classes_lost per arm, none_found share per class, and re-ask counts and yield with and without re-asked reviewers are missing or only totals
search: grep -n -E -e 'over_budget' -e 'recipe_missing' -e 'unknown_item' -e 'classes_lost' -e 'none_found' -e 'yield' -- .dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/analysis/analyze.py
coupled sites: arm_metrics (metrics.json, report.md emission) in analysis/analyze.py; EXPECTED and expected.json in fixtures/runs/make_runs.py; tests/test_analyze.py; the rows-per-lens and reach-per-class-per-reviewer metrics of the same 12.5 sentence (check they exist)
before:
11:        REQ-17 over RL run folders: ledger_missing rate, recipe_missing, quote validity, format errors, none_found per class.
641:        if not r["unknown_item"]
642:        and not r["over_budget"]
756:    """The rows of a ledger without the class `drop`, over_budget recomputed for the lens cap in the order written
763:        if r["over_budget"] != "recipe" and not r["unknown_item"]:
765:            r["over_budget"] = "lens" if within > cap else None
862:    """The REQ-17 numbers over RL run folders that have a check: ledger_missing before any re-ask, recipe_missing,
863:    quote validity, format errors and none_found per class."""
889:    recipe_missing, none_found = {}, {}
894:        for c in x["recipe_missing"]:
895:            recipe_missing[c] = recipe_missing.get(c, 0) + 1
897:            if r["none_found"]:
899:                none_found[c] = none_found.get(c, 0) + 1
900:            if r["over_budget"]:
901:                over[r["over_budget"]] += 1
912:        "recipe_missing": dict(sorted(recipe_missing.items())),
921:        "none_found": dict(sorted(none_found.items())),
922:        "over_budget": over,
1285:    print(f"recipe_missing per class: {res['recipe_missing']}")
1291:    print(f"none_found per class: {res['none_found']}")
1293:        f"over_budget: {res['over_budget']}; re-ask: {res['reask']}; rows per reviewer: {res['rows_per_reviewer']}"
after:
11:        REQ-17 over RL run folders: ledger_missing rate, recipe_missing, quote validity, format errors, none_found per class.
127:    "reask_yield",
222:      over_budget      {recipe, lens}: rows flagged over budget, by reason.
223:      recipe_missing   {class: n}: reviewer-runs whose lens recipe for the class has no row.
224:      unknown_item     n: rows whose id is outside the grammar or the reviewer's lens.
225:      none_found_share {class: {none_found, ran, share}}: `ran` is the reviewer-runs that wrote at least one accepted
226:                       (not unknown_item) row of the class; `none_found` is those that wrote a NONE FOUND row for it, so
230:    missing, ran, none_found, rows_by = {}, {}, {}, {}
233:        unknown += len(x["unknown_item"])
236:        for c in x["recipe_missing"]:
240:            if r["over_budget"]:
241:                over[r["over_budget"]] += 1
243:            if c and not r["unknown_item"]:
245:                if r["none_found"]:
250:            none_found[c] = none_found.get(c, 0) + 1
252:        "over_budget": over,
253:        "recipe_missing": dict(sorted(missing.items())),
254:        "unknown_item": unknown,
255:        "none_found_share": {
257:                "none_found": none_found.get(c, 0),
259:                "share": none_found.get(c, 0) / n,
267:def reask_yield(fractions, reasked):
268:    """Found-fraction yield of the runs with a re-asked reviewer and of the runs without one (DESIGN 8 row 23).
465:            for classes in (chk.get("classes_lost") or {}).values():
521:        "classes_lost": dict(sorted(lost.items())),
524:        "reask_yield": reask_yield(fr, reasked),
730:        if not r["unknown_item"]
731:        and not r["over_budget"]
845:    """The rows of a ledger without the class `drop`, over_budget recomputed for the lens cap in the order written
852:        if r["over_budget"] != "recipe" and not r["unknown_item"]:
854:            r["over_budget"] = "lens" if within > cap else None
951:    """The REQ-17 numbers over RL run folders that have a check: ledger_missing before any re-ask, recipe_missing,
952:    quote validity, format errors and none_found per class."""
978:    recipe_missing, none_found = {}, {}
983:        for c in x["recipe_missing"]:
984:            recipe_missing[c] = recipe_missing.get(c, 0) + 1
986:            if r["none_found"]:
988:                none_found[c] = none_found.get(c, 0) + 1
989:            if r["over_budget"]:
990:                over[r["over_budget"]] += 1
1001:        "recipe_missing": dict(sorted(recipe_missing.items())),
1010:        "none_found": dict(sorted(none_found.items())),
1011:        "over_budget": over,
1217:    """The per-arm ledger tables of DESIGN 12.5: checks and re-asks, none_found share, rows per lens, reach per class
1223:        "| arm | over_budget recipe | over_budget lens | recipe_missing | unknown_item | classes_lost | re-asks asked | re-asks accepte
1228:        y = p["reask_yield"]
1230:            f"| {arm} | {p['over_budget']['recipe']} | {p['over_budget']['lens']} | {p['recipe_missing']} | "
1231:            f"{p['unknown_item']} | {p['classes_lost']} | {p['reask_asked']} | {p['reask_accepted']} | "
1237:        "none_found share: reviewer-runs with a NONE FOUND row of the class over reviewer-runs with a row of the class.",
1239:        "| arm | class | none_found | ran | share |",
1243:        for c, v in a["pooled"]["none_found_share"].items():
1245:                f"| {arm} | {c} | {v['none_found']} | {v['ran']} | {fmt(v['share'])} |"
1427:    print(f"recipe_missing per class: {res['recipe_missing']}")
1433:    print(f"none_found per class: {res['none_found']}")
1435:        f"over_budget: {res['over_budget']}; re-ask: {res['reask']}; rows per reviewer: {res['rows_per_reviewer']}"
