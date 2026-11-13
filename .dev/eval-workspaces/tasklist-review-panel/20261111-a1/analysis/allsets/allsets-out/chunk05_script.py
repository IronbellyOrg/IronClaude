import json, csv
leg = list(csv.DictReader(open('/tmp/issue-legend.tsv'), delimiter='\t'))
pk = {'designSpec': 'TASK-WF-designSpec-20261107-075614', 'alias': 'TASK-WF-makeTheAliasOnly-20261105-051649', 'control': 'TASK-WF-design-20261108-041415'}
labels = [r['label'] for r in leg]
sets = json.load(open('/tmp/allsets-chunks/chunk-05.json'))
out = []
notes_dump = {}
for s in sets:
    found = {l: 0 for l in labels}
    bc = {l: 0 for l in labels}
    per = {}
    flags = []
    for r in s['runs']:
        pf, pb = [], []
        sc = {}
        for pid, path in r['scores'].items():
            try:
                sc[pid] = json.load(open(path))
            except Exception as e:
                flags.append(f"{r['run']}: unreadable {pid}: {e}")
        for row in leg:
            d = sc.get(pk[row['package']])
            if d is None:
                continue
            if row['gt_id'] in (d.get('gt_covered_any') or []):
                found[row['label']] += 1; pf.append(row['label'])
            if row['gt_id'] in (d.get('gt_covered_blocking') or []):
                bc[row['label']] += 1; pb.append(row['label'])
        per[r['run']] = {'found': pf, 'blocking_credit': pb}
        notes_dump.setdefault(s['set'], {})[r['run']] = {pid[8:20]: {'any': d.get('gt_covered_any'), 'blk': d.get('gt_covered_blocking'), 'notes': d.get('notes')} for pid, d in sc.items()}
    out.append({'sid': s.get('sid'), 'set': s['set'], 'era': s['era'], 'n_runs': s['n_runs'], 'found': found, 'blocking_credit': bc, 'per_run': per, 'check': '', '_flags': flags})
json.dump(out, open('/tmp/allsets-out/chunk-05.json', 'w'), indent=1)
json.dump(notes_dump, open('/tmp/allsets-out/chunk05_notes.json', 'w'), indent=1)
for o in out:
    print(o['sid'], o['set'], o['n_runs'], o['_flags'])
