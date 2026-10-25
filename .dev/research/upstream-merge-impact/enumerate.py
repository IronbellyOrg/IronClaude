"""Collect local Git provenance without modifying Git or the checkout."""
import collections
import datetime as dt
import json
import pathlib
import subprocess

OUT = pathlib.Path(__file__).resolve().parent

def git(*args):
    return subprocess.check_output(['git', *args], text=True)

head = git('rev-parse', 'HEAD').strip()
raw = git('log', 'HEAD', '--format=%H%x09%P%x09%aI%x09%cI%x09%an%x09%ae%x09%s')
all_rows = []
for line in raw.splitlines():
    sha, parents, authored, committed, author, email, subject = line.split('\t', 6)
    all_rows.append(dict(sha=sha, parents=parents.split(), authored=authored, committed=committed, author=author, email=email, subject=subject))
start = dt.datetime.fromisoformat('2025-10-23T00:00:00+00:00')
end = dt.datetime.fromisoformat('2026-10-24T00:00:00+00:00')
rows = [r for r in all_rows if start <= dt.datetime.fromisoformat(r['committed']) < end]
merges = [r for r in rows if len(r['parents']) > 1 and 'SuperClaude-Org' in r['subject']]
upstream_tips = [r['parents'][1] for r in merges]
upstream = set(git('rev-list', *upstream_tips).splitlines())
selected = [dict(r, provenance='upstream-parent-ancestry') for r in rows if r['sha'] in upstream]
syncs = [dict(r, provenance='framework-sync-message') for r in rows if 'automated sync and namespace isolation from framework' in r['subject']]
unknown = [r for r in rows if r['sha'] not in upstream and not r['email'].endswith('@ironbelly.com') and r['author'] != 'github-actions[bot]']
for r in merges:
    r['introduced_commits'] = git('rev-list', r['parents'][0]+'..'+r['parents'][1]).splitlines()
    r['net_files'] = git('diff', '--name-only', r['parents'][0], r['sha']).splitlines()
for r in selected + syncs + unknown:
    r['files'] = git('diff-tree', '--root', '--no-commit-id', '--name-only', '-r', r['sha']).splitlines()
refs = git('for-each-ref', '--format=%(refname) %(objectname)', 'refs/remotes')
data = dict(head=head, window_basis='committer timestamp; author timestamp preserved', merges=merges, upstream_commits=selected, sync_commits=syncs, external_candidates=unknown, refs=refs, shallow=git('rev-parse','--is-shallow-repository').strip())
(OUT/'inventory.json').write_text(json.dumps(data, indent=2)+'\n')
(OUT/'reachable-log.tsv').write_text(raw)
print('HEAD', head, 'upstream',len(selected),'syncs',len(syncs),'external candidates',len(unknown))
for r in merges:
    print('MERGE',r['sha'][:8],len(r['introduced_commits']),'introduced',len(r['net_files']),'files')
for r in reversed(selected):
    print('UPSTREAM',r['sha'][:8],r['authored'][:10],r['author'],r['subject'],'FILES',','.join(r['files']))
for r in reversed(syncs):
    print('SYNC',r['sha'][:8],len(r['files']),'files',','.join(r['files']))
for r in unknown:
    print('CANDIDATE',r['sha'][:8],r['author'],r['subject'],'FILES',','.join(r['files']))
print('AUTHORS',dict(collections.Counter(r['author'] for r in selected)))
