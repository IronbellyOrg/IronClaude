import json, re, collections
rows = [json.loads(l) for l in open('p17/findings.jsonl')]
ID = r"(WC-\d+|SA-\d+|AC-C\d|AC-[0-4]\.\d|NFR-\d+|D[1-6]\b|UNVERIFIED \d+)"
def key(r):
    h = r['heading']; b = r['body'][:1500]
    for src in (h, b):
        m = re.search(ID, src)
        if m:
            k = m.group(1)
            if k.startswith('AC-C'): k = 'AC-C'
            if re.match(r'AC-[0-4]\.', k): k = k[:4]  # AC-1., AC-0.
            return k
    for src in (h, b):
        m = re.search(r"/sc:([\w-]+)", src)
        if m: return 'cmd:' + m.group(1)
    for src in (h, b):
        m = re.search(r"\b(load|workflow|tdd|troubleshoot|adversarial|cleanup-audit|index-repo|pr-submit|post-release|implement|reflect|tasklist|roadmap|research|spec-panel)\b", src)
        if m: return 'cmd:' + m.group(1)
    if re.search(r"live check|7\.2", h + b, re.I): return '7.2'
    return 'misc'
cnt = collections.Counter(); bk = collections.defaultdict(list)
for r in rows: k = key(r); r['bucket'] = k; bk[k].append(r['gid'])
for k, v in sorted(bk.items(), key=lambda kv: -len(kv[1])): print(k, len(v))
json.dump(bk, open('p17/buckets.json', 'w'))
