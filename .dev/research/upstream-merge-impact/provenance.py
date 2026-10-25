"""Record Git-only scope evidence and per-commit strict-check results."""
import collections
import json
import os
import pathlib
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
out = pathlib.Path(__file__).resolve().parent
data = json.loads((out/'inventory.json').read_text())
units = json.loads((out/'units.json').read_text())
checks = json.loads((out/'reverse-checks.json').read_text())

def git(*args):
    return subprocess.check_output(['git', *args], text=True)

def ancestor(a, b):
    result = subprocess.run(['git','merge-base','--is-ancestor',a,b], capture_output=True)
    assert result.returncode in (0,1)
    return result.returncode == 0

lines = ['# Local Git evidence', '', 'Snapshot HEAD: '+data['head'], 'Window: 2025-10-23T00:00:00Z <= committer date < 2026-10-24T00:00:00Z.', 'Repository shallow: '+data['shallow'], '', '## Explicit upstream merge commits', '']
for r in reversed(data['merges']):
    lines += [f"Merge {r['sha']}; author date {r['authored']}; committer date {r['committed']}", 'Subject: '+r['subject'], 'First parent: '+r['parents'][0], 'Upstream second parent: '+r['parents'][1], 'Newly reachable upstream commits: '+', '.join(r['introduced_commits']), 'Net files: '+', '.join(r['net_files']), '']
lines += ['## Base history and external author classification', '']
base_tip = data['merges'][1]['parents'][0]
for r in data['external_candidates']:
    lines += [f"External-author candidate {r['sha']} ({r['author']} <{r['email']}>): NOT in either explicit upstream parent ancestry; subject: {r['subject']}", 'Full commit metadata follows:', git('show','--no-patch','--format=fuller',r['sha']).strip(), '']
for r in data['upstream_commits']:
    r['reachable_before_first_upstream_merge'] = ancestor(r['sha'], base_tip)
counts=collections.Counter(r['reachable_before_first_upstream_merge'] for r in data['upstream_commits'])
lines += ['Upstream in-window commits already present before February merge: '+str(counts[True]), 'Upstream in-window commits introduced by named February/March merges: '+str(counts[False]), '']
first_fork = git('log','HEAD','--reverse','--format=%H %cI %an <%ae> %s','--author=@ironbelly.com').splitlines()[:8]
lines += ['First eight fork-owned commits by Git reverse traversal:', *first_fork, '', '## Local remote refs and pending sync', data['refs'].strip(), '']
for ref in ('origin/master','origin/sync/framework'):
    sha=git('rev-parse',ref).strip()
    lines += [f'{ref}: {sha}; ancestor of HEAD={ancestor(sha,"HEAD")}; HEAD ancestor of ref={ancestor("HEAD",sha)}', 'Commits unique to ref relative to HEAD:',git('log','HEAD..'+ref,'--format=%H %cI %an %s').strip(), '']
lines += ['## Author counts for in-window upstream ancestry', json.dumps(dict(collections.Counter(r['author'] for r in data['upstream_commits'])),sort_keys=True), '', '## Per-record unit and strict reverse check', '']
by_sha={r['sha']:r for r in checks}
for unit in units:
    lines += [f"### {unit['id']}: {unit['title']}", f"{len(unit['commits'])} records; {len(unit['files'])} distinct paths", '']
    for r in unit['commits']:
        c=by_sha[r['sha']]
        lines += [f"{r['sha']} | authored={r['authored']} | committed={r['committed']} | {r['author']} | {r['subject']} | strict_reverse_rc={c['returncode']}"]
    lines += ['']
lines += ['## Date boundary cross-check', 'Author/committer window disagreement among selected records:']
for r in data['upstream_commits']+data['sync_commits']:
    if not ('2025-10-23' <= r['authored'][:10] <= '2026-10-23'):
        lines.append(json.dumps(r))
lines += ['End of evidence.']
(out/'git-evidence.md').write_text('\n'.join(lines)+'\n')
print('Upstream base / named-merge counts:',dict(counts))
print('Strict reverse check codes:',dict(collections.Counter(c['returncode'] for c in checks)))
print('Author counts:',dict(collections.Counter(r['author'] for r in data['upstream_commits'])))
print('Evidence written:',out/'git-evidence.md')
