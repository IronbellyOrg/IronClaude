import json, sys
from datetime import datetime
f = sys.argv[1]
def ts(s): return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
uses = {}   # id -> (start, name, input)
results = {}  # id -> end ts
hbs = []
for line in open(f):
    try: o = json.loads(line)
    except: continue
    t = o.get('timestamp')
    if not t: continue
    msg = o.get('message') or {}
    c = msg.get('content')
    if not isinstance(c, list): continue
    for b in c:
        if b.get('type') == 'tool_use':
            uses[b['id']] = (ts(t), b['name'], b.get('input', {}))
            if b['name'] == 'Bash' and '--type heartbeat' in b['input'].get('command', ''):
                hbs.append(ts(t))
        elif b.get('type') == 'tool_result':
            results[b.get('tool_use_id')] = ts(t)
t0 = min(v[0] for v in uses.values())
fmt = lambda x: datetime.utcfromtimestamp(x).strftime('%H:%M:%S')
print('first tool call', fmt(t0), 'heartbeats', [fmt(h) for h in hbs])
ag = []
for i, (s, n, inp) in uses.items():
    if n == 'Agent':
        e = results.get(i, s)
        ag.append((s, e, inp.get('run_in_background'), inp.get('subagent_type'), inp.get('description')))
ag.sort()
for s, e, bg, st, d in ag:
    print('Agent', fmt(s), '->', fmt(e), 'bg=%s' % bg, st, d)
print('gaps between consecutive heartbeats (minutes):', [round((b - a) / 60, 1) for a, b in zip(hbs, hbs[1:])])
# last heartbeat to worker_done
sends = [v[0] for v in uses.values() if v[1] == 'Bash' and '--type worker_done' in v[2].get('command', '')]
print('worker_done at', [fmt(x) for x in sends])
print('first heartbeat after first tool call: %.1f min' % ((hbs[0] - t0) / 60))
