a8ecbfea4be60c23f0f77b58fbba35829b0d9747
family owner-measure-count
form: m1_open_confirmed groups leave out a defect kind that compute_verdict counts in confirmed=
command: grep -n -e 'groups' -e 'audit_hunks_real' -- src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py
before:
952:def audit_hunks_real(records):
1007:    ) or audit_hunks_real(records):
1169:    groups = {defect_key(claims.get(cid, {"id": cid}), begin) for cid in confirmed}
1170:    groups.update(
1171:        f"hunk:{a['hunk'][0]}-{a['hunk'][1]}" for a in audit_hunks_real(records)
1179:    if groups:
1193:        "confirmed": len(groups),
1263:    groups = {
1268:    groups.update(
1274:        "m1_open_confirmed": len(groups),
1362:    hunks = audit_hunks_real(records)
1431:    for h in audit_hunks_real(records):
1500:    for h in audit_hunks_real(records):
coupled sites: compute_verdict groups (the definition to match), label_counts groups, cmd_count
after:
952:def audit_hunks_real(records):
1007:    ) or audit_hunks_real(records):
1169:    groups = {defect_key(claims.get(cid, {"id": cid}), begin) for cid in confirmed}
1170:    groups.update(
1171:        f"hunk:{a['hunk'][0]}-{a['hunk'][1]}" for a in audit_hunks_real(records)
1179:    if groups:
1193:        "confirmed": len(groups),
1263:    groups = {
1269:    groups.update(
1270:        f"hunk:{a['hunk'][0]}-{a['hunk'][1]}" for a in audit_hunks_real(records)
1272:    groups.update(
1278:        "m1_open_confirmed": len(groups),
1366:    hunks = audit_hunks_real(records)
1435:    for h in audit_hunks_real(records):
1504:    for h in audit_hunks_real(records):

family audit-sample-probability
form: one inclusion probability recorded for a stratum whose items have different probabilities
command: grep -n -e 'p=round' -e 'chosen.append' -e 'non-blocking' -- src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py
before:
1874:        "non-blocking": [i for i in rest if i["status"] in DEMOTED],
1884:        if name == "non-blocking":  # at least one per non-empty sub-stratum
1888:                    chosen.append(rng.choice(sub))
1893:            dict(i, stratum=name, p=round(len(chosen) / len(pool), 4)) for i in chosen
coupled sites: cmd_audit_sample (non-blocking, confirmed, resolved-prior strata)
after:
1878:        "non-blocking": [i for i in rest if i["status"] in DEMOTED],
1888:        subs = {s: v for s, v in subs.items() if v} if name == "non-blocking" else {}
1889:        # non-blocking: one forced pick per non-empty sub-stratum, the remaining slots
1902:            drawn.append(dict(i, stratum=name, p=round(p, 4)))
