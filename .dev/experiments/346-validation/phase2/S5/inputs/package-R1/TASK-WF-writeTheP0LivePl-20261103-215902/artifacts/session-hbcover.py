import json, sys, glob, os
from datetime import datetime, timezone
top = sys.argv[1]
def ts(s): return datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()
fmt = lambda x: datetime.fromtimestamp(x, timezone.utc).strftime('%H:%M:%S')
hbs = []; first_user = None; wdone = None
for line in open(top):
    try: o = json.loads(line)
    except Exception: continue
    t = o.get('timestamp')
    if not t: continue
    x = ts(t); c = (o.get('message') or {}).get('content')
    if o.get('type') == 'user' and isinstance(c, str) and first_user is None: first_user = x
    if o.get('type') == 'assistant':
        for b in (c if isinstance(c, list) else []):
            if b.get('type') == 'tool_use' and b['name'] == 'Bash':
                cmd = b['input'].get('command', '')
                if '--type heartbeat' in cmd: hbs.append(x)
                if '--type worker_done' in cmd: wdone = x
sub = glob.glob(os.path.join(os.path.dirname(top), os.path.basename(top)[:-6], 'subagents', '*.jsonl'))
iv = []
for f in sub:
    stamps = []
    for line in open(f):
        try: o = json.loads(line)
        except Exception: continue
        if o.get('timestamp'): stamps.append(ts(o['timestamp']))
    if stamps: iv.append((min(stamps), max(stamps)))
iv.sort(); merged = []
for s, e in iv:
    if merged and s <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], e)
    else: merged.append([s, e])
def cover(a, b): return sum(max(0, min(b, e) - max(a, s)) for s, e in merged)
pts = [first_user] + hbs + ([wdone] if wdone else [])
rows = [(a, b, (b - a) / 60, cover(a, b) / 60, (b - a - cover(a, b)) / 60) for a, b in zip(pts, pts[1:])]
print('## heartbeat gaps with subagent run time removed (cadence 5 min)')
print('Subagent run interval = first to last timestamp of its own session file (%d subagent files); merged into %d intervals' % (len(iv), len(merged)))
print('%-19s %8s %9s %13s' % ('from -> to', 'gap min', 'agent min', 'non-agent min'))
for a, b, g, c, n in rows:
    print('%s -> %s %8.1f %9.1f %13.1f%s' % (fmt(a), fmt(b), g, c, n, '   <-- over 5' if n > 5 else ''))
print('max non-agent stretch since the last heartbeat (or since the brief): %.1f min' % max(r[4] for r in rows))
