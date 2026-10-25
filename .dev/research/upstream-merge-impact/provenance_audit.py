"""Independent, read-only Git audit of upstream enumeration and unit assignment."""
import collections
import datetime as dt
import json
import os
from pathlib import Path
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
out = Path(__file__).resolve().parent
start = dt.datetime(2025,10,23,tzinfo=dt.timezone.utc)
end = dt.datetime(2026,10,24,tzinfo=dt.timezone.utc)

def git(*args):
    return subprocess.check_output(['git','--no-pager',*args],text=True,timeout=60)

raw = git('log','HEAD','--format=%H%x00%P%x00%aI%x00%cI%x00%an%x00%ae%x00%s%x00%B%x1e')
rows=[]
for item in raw.split('\x1e'):
    if not item.strip():
        continue
    h,p,a,c,n,e,s,b=item.strip('\n').split('\x00',7)
    rows.append(dict(sha=h,parents=p.split(),authored=a,committed=c,name=n,email=e,subject=s,body=b))
window = [r for r in rows if start <= dt.datetime.fromisoformat(r['committed']) < end]
named = [r for r in window if len(r['parents'])>1 and 'superclaude-org' in r['subject'].lower()]
parents = [r['parents'][1] for r in named]
upstream=set(git('rev-list',*parents).splitlines())
expected = {r['sha'] for r in window if r['sha'] in upstream}
syncs=[r for r in window if 'automated sync and namespace isolation from framework' in r['subject'].lower()]
others=[r for r in window if r['sha'] not in upstream and not r['email'].endswith('@ironbelly.com') and r not in syncs]
inv=json.loads((out/'inventory.json').read_text())
units=json.loads((out/'units.json').read_text())
reverse=json.loads((out/'reverse-checks.json').read_text())
assigned=[c['sha'] for u in units for c in u['commits']]
expected_records=expected|{r['sha'] for r in syncs}|{r['sha'] for r in named}
file_mismatches=[]
for u in units:
    for c in u['commits']:
        actual=git('diff','--name-only',c['parents'][0],c['sha']).splitlines()
        if c['files']!=actual:
            file_mismatches.append(c['sha'])
summary=dict(head=git('rev-parse','HEAD').strip(), reachable_commits=len(rows), window_commits=len(window),
    named_merges=named, upstream_count=len(expected), sync_count=len(syncs),
    inventory_upstream_matches=expected=={r['sha'] for r in inv['upstream_commits']},
    inventory_sync_matches={r['sha'] for r in syncs}=={r['sha'] for r in inv['sync_commits']},
    all_54_records_assigned_once=len(assigned)==len(set(assigned))==54 and set(assigned)==expected_records,
    path_list_mismatches=file_mismatches,
    nonfork_outside_upstream_and_sync=others,
    bots_in_window=[r for r in window if 'bot' in r['name'].lower()],
    author_outside_committer_window=[r for r in window if r['sha'] in expected_records and not start<=dt.datetime.fromisoformat(r['authored'])<end],
    committer_outside_author_window=[r for r in rows if r['sha'] in upstream and start<=dt.datetime.fromisoformat(r['authored'])<end and not start<=dt.datetime.fromisoformat(r['committed'])<end],
    upstream_keyword_nonupstream=[r for r in window if r['sha'] not in upstream and any(k in r['subject'].lower() for k in ('upstream','superclaude-org','framework'))],
    cherry_pick_trailers=[r for r in window if r['sha'] not in upstream and any(k in r['body'].lower() for k in ('cherry picked from','cherry-picked from','cherry-pick','upstream commit'))],
    reverse_counts=dict(collections.Counter(r['returncode'] for r in reverse)),
    reverse_empty=[r for r in reverse if not git('diff','--binary',r['sha']+'^1',r['sha'])],
    first_fork_parent=git('rev-parse','9a38d894^1').strip())
for ref in ('HEAD','origin/master','origin/sync/framework'):
    result=subprocess.run(['git','merge-base','--is-ancestor','d3cf5938',ref],capture_output=True)
    assert result.returncode in (0,1)
    summary['pending_sync_ancestor_of_'+ref]=result.returncode==0
endpoint_manifest=json.loads((out/'endpoint-inventory.json').read_text())
endpoint_by_id={u['id']:u for u in endpoint_manifest}
endpoint_audit=[]
all_endpoints=set()
for u in units:
    endpoints=set()
    for c in u['commits']:
        endpoints.update(filter(None,git('diff','--no-renames','--name-only','-z',c['parents'][0],c['sha']).split('\x00')))
    expected_paths=set(endpoint_by_id[u['id']]['files'])
    endpoint_audit.append(dict(unit=u['id'],count=len(endpoints),manifest_matches=endpoints==expected_paths,extra_over_default=sorted(endpoints-set(u['files']))))
    all_endpoints.update(endpoints)
summary['endpoint_audit']=endpoint_audit
summary['all_endpoint_count']=len(all_endpoints)
base_ancestry=set(git('rev-list',summary['first_fork_parent']).splitlines())
summary['base_upstream_count']=len(base_ancestry & expected)
summary['upstream_not_in_original_base']=sorted(expected-base_ancestry)
summary['upstream_author_counts']=dict(collections.Counter(r['name'] for r in window if r['sha'] in expected))
summary['shallow']=git('rev-parse','--is-shallow-repository').strip()
summary['named_merge_net_paths']={r['sha']:git('diff','--name-only',r['parents'][0],r['sha']).splitlines() for r in named}
(out/'provenance-audit-evidence.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('named_merges','nonfork_outside_upstream_and_sync','bots_in_window','upstream_keyword_nonupstream','cherry_pick_trailers')},indent=2))
print('OUTSIDE AUTHORS',[(r['sha'][:8],r['name'],r['subject']) for r in others])
print('CHERRY PICK TRAILERS',[(r['sha'][:8],r['subject']) for r in summary['cherry_pick_trailers']])
print('UPSTREAM KEYWORDS',[(r['sha'][:8],r['subject']) for r in summary['upstream_keyword_nonupstream']])
