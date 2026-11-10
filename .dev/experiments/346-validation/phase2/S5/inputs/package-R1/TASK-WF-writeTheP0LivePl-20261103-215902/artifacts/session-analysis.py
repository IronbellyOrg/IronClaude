import json, sys, glob, os, re
from datetime import datetime, timezone
d = sys.argv[1]            # project dir with *.jsonl (top-level + subagents)
top = sys.argv[2]          # top-level session file
def ts(s): return datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()
fmt = lambda x: datetime.fromtimestamp(x, timezone.utc).strftime('%H:%M:%S')
ev = []; tally = {}; skills = []; orca = []; hbs = []; notes = []; first_user = None; sidechain_true = 0; agents = []
for line in open(top):
    try: o = json.loads(line)
    except Exception: continue
    t = o.get('timestamp')
    if not t: continue
    m = o.get('message') or {}
    c = m.get('content')
    if o.get('type') == 'user' and first_user is None and isinstance(c, str): first_user = ts(t)
    if o.get('type') == 'user' and isinstance(c, str) and c.startswith('<task-notification>'): notes.append(ts(t))
    if o.get('type') == 'assistant':
        if o.get('isSidechain'): sidechain_true += 1
        for b in (c if isinstance(c, list) else []):
            if b.get('type') != 'tool_use': continue
            n = b['name']; tally[n] = tally.get(n, 0) + 1
            ev.append((ts(t), n, b.get('input', {})))
            if n == 'Skill': skills.append((t, o.get('isSidechain'), b['input'].get('skill')))
            if n == 'Agent': agents.append(ts(t))
            if n == 'Bash':
                cmd = b['input'].get('command', '')
                if 'orca orchestration' in cmd:
                    for mm in re.finditer(r'orca orchestration (send|check)[^;&|]*?(--type [a-z_]+)?(?=\s*(?:[;&|>]|$))', cmd):
                        pass
                    typ = re.search(r'--type ([a-z_]+)', cmd)
                    verb = re.search(r'orca orchestration (\w[\w-]*)', cmd).group(1)
                    orca.append((ts(t), verb, typ.group(1) if typ else ''))
                    if typ and typ.group(1) == 'heartbeat': hbs.append(ts(t))
print('## tool calls by name (top-level session; assistant messages with isSidechain=true: %d)' % sidechain_true)
for k, v in sorted(tally.items(), key=lambda kv: -kv[1]): print('%7d %s' % (v, k))
print('\n## Skill calls')
for t, sc, s in skills: print(t, 'sidechain=%s' % sc, 'skill=%s' % s)
print('\n## orca orchestration commands in the top-level session')
for t, verb, typ in orca: print(fmt(t), verb, typ)
last = max(t for t, _, _ in ev)
done = [t for t, v, y in orca if y == 'worker_done']
print('\n## run length: first user message %s, worker_done %s' % (fmt(first_user), [fmt(x) for x in done]))
if done: print('run length minutes: %.1f' % ((done[0] - first_user) / 60))
print('heartbeats (%d): %s' % (len(hbs), [fmt(h) for h in hbs]))
gaps = [(a, b) for a, b in zip(hbs, hbs[1:])]
print('gaps (min): %s' % [round((b - a) / 60, 1) for a, b in gaps])
if done: print('last heartbeat to worker_done (min): %.1f' % ((done[0] - hbs[-1]) / 60))
print('first heartbeat after first user message (min): %.1f' % ((hbs[0] - first_user) / 60) if hbs else 'no heartbeat')
print('\n## gaps over 5 minutes: top-level activity inside each')
for a, b in gaps:
    if b - a > 300:
        print('gap %s -> %s (%.1f min)' % (fmt(a), fmt(b), (b - a) / 60))
        for t, n, i in ev:
            if a < t < b: print('   %s %s %s' % (fmt(t), n, (i.get('description') or i.get('command') or i.get('file_path') or '')[:70].replace('\n', ' ')))
        print('   task-notifications (background agent finished): %s' % [fmt(x) for x in notes if a < x < b])
print('\n## Agent launches (top-level):', [fmt(x) for x in agents])
# whole project (top-level + subagent sessions)
files = glob.glob(os.path.join(d, '**', '*.jsonl'), recursive=True)
allbash = []; names = {}
for f in files:
    for line in open(f):
        try: o = json.loads(line)
        except Exception: continue
        if o.get('type') != 'assistant': continue
        for b in (o.get('message', {}).get('content') or []):
            if isinstance(b, dict) and b.get('type') == 'tool_use':
                names[b['name']] = names.get(b['name'], 0) + 1
                if b['name'] == 'Bash': allbash.append(b['input'].get('command', ''))
print('\n## all session files: %d; Bash commands: %d' % (len(files), len(allbash)))
pat = re.compile(r'worker-start|orchestration dispatch|task-create|worktree create|agent launch|orca worktree|orca agent')
hits = [c[:160] for c in allbash if pat.search(c)]
print('WC-13 pattern hits: %d' % len(hits)); [print('   ', h) for h in hits]
print('orca verbs in all sessions:', sorted(set(re.findall(r'orca \w+ [\w-]+', ' '.join(allbash)))))
print('tool names containing ask/question (case-insensitive), all sessions:', {k: v for k, v in names.items() if re.search('ask|question', k, re.I)})
