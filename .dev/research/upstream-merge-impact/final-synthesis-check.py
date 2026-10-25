"""Independent static synthesis checks; no project imports or Git mutations."""
import collections
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
root = pathlib.Path.cwd()
out = pathlib.Path(__file__).resolve().parent

def git(*args):
    return subprocess.check_output(['git', *args], text=True)

def ancestor(a, b):
    rc = subprocess.run(['git', 'merge-base', '--is-ancestor', a, b], capture_output=True).returncode
    assert rc in (0, 1)
    return rc == 0

inventory = json.loads((out/'inventory.json').read_text())
units = json.loads((out/'units.json').read_text())
endpoint_units = {u['id']:u for u in json.loads((out/'endpoint-inventory.json').read_text())}
central = {r['sha']:r for r in json.loads((out/'reverse-checks.json').read_text())}
start = dt.datetime.fromisoformat('2025-10-23T00:00:00+00:00')
end = dt.datetime.fromisoformat('2026-10-24T00:00:00+00:00')
records = []
for line in git('log','HEAD','--format=%H%x09%P%x09%aI%x09%cI%x09%an%x09%ae%x09%s').splitlines():
    sha, parents, authored, committed, author, email, subject = line.split('\t',6)
    records.append(dict(sha=sha, parents=parents.split(), authored=authored, committed=committed, author=author,email=email,subject=subject))
window = [r for r in records if start <= dt.datetime.fromisoformat(r['committed']) < end]
merges = [r for r in window if len(r['parents'])>1 and 'superclaude-org' in r['subject'].lower()]
upstream_ancestors = set(git('rev-list',*[r['parents'][1] for r in merges]).splitlines())
upstream = [r for r in window if r['sha'] in upstream_ancestors]
syncs = [r for r in window if 'automated sync and namespace isolation from framework' in r['subject'].lower()]
assert len(merges)==2 and len(upstream)==47 and len(syncs)==5
assert collections.Counter(r['author'] for r in upstream)['mithun50']==27
assert {r['sha'] for r in upstream}=={r['sha'] for r in inventory['upstream_commits']}
assert {r['sha'] for r in syncs}=={r['sha'] for r in inventory['sync_commits']}
assigned=[r['sha'] for u in units for r in u['commits']]
assert len(assigned)==len(set(assigned))==54
assert set(assigned)=={r['sha'] for r in merges+upstream+syncs}
all_endpoints=set()
unit_results=[]
for u in units:
    actual=set()
    checked=[]
    text=(out/(u['id']+'.md')).read_text()
    for r in u['commits']:
        actual.update(git('diff','--no-renames','--name-only',r['parents'][0],r['sha']).splitlines())
        patch=subprocess.check_output(['git','diff','--binary','--no-ext-diff',r['parents'][0],r['sha']])
        check=subprocess.run(['git','apply','--reverse','--check','--whitespace=nowarn','-'],input=patch,capture_output=True)
        assert check.returncode==central[r['sha']]['returncode'], r['sha']
        assert r['sha'][:8] in text, r['sha']
        checked.append(dict(sha=r['sha'],returncode=check.returncode))
    assert actual==set(endpoint_units[u['id']]['files']),u['id']
    assert '{{RF_PLACEHOLDER:' not in text,u['id']
    all_endpoints.update(actual)
    unit_results.append(dict(unit=u['id'],records=len(u['commits']),endpoints=len(actual),strict_checks=checked))
assert len(all_endpoints)==563
report=(out/'REPORT.md').read_text()
assert '{{RF_PLACEHOLDER:' not in report
rows=[line for line in report.splitlines() if line.startswith('| ') and not line.startswith('| Unit ')]
assert len(rows)==8
assert all(len(re.split(r'(?<!\\)\|',row)[1:-1])==6 for row in rows)
expected_verdicts=['revert','partial','keep','keep','partial','keep','partial','partial']
for row, verdict in zip(rows,expected_verdicts):
    cells=re.split(r'(?<!\\)\|',row)[1:-1]
    assert '**'+verdict+'**' in cells[3], row
for name in ('provenance-review','review-commands-sync','review-quality-mcp','review-foundation-docs','review-packaging-sync-copies'):
    text=(out/(name+'.md')).read_text()
    assert '**Verdict:** PASS' in text,name
citation_pattern=re.compile(r'(?P<path>(?:[A-Za-z0-9_.@+\-]+/)*[A-Za-z0-9_.@+\-]+\.(?:py|md|txt|json|toml|yml|yaml|sh)|Makefile|VERSION):(?P<ranges>[0-9]+(?:-[0-9]+)?(?:,[0-9]+(?:-[0-9]+)?)*)')
citations=[]
for m in citation_pattern.finditer(report):
    rel=m.group('path')
    source=root/rel
    if not source.is_file():
        source=out/rel
    assert source.is_file(),rel
    source_lines=source.read_text(errors='replace').splitlines()
    for span in m.group('ranges').split(','):
        fields=span.split('-')
        lo=int(fields[0]); hi=int(fields[-1])
        assert 1<=lo<=hi<=len(source_lines),(rel,lo,hi,len(source_lines))
        citations.append(dict(path=str(source.relative_to(root)),start=lo,end=hi,excerpt='\n'.join(source_lines[lo-1:hi])))
first_merge=next(r for r in merges if r['sha'].startswith('0ceb2955'))
base_count=sum(ancestor(r['sha'],first_merge['parents'][0]) for r in upstream)
assert base_count==45
assert not ancestor('d3cf5938','HEAD') and not ancestor('d3cf5938','origin/master')
assert ancestor('d3cf5938','origin/sync/framework')
reverse_counts=dict(collections.Counter(c['returncode'] for u in unit_results for c in u['strict_checks']))
assert reverse_counts=={0:5,1:48,128:1}
head_now=git('rev-parse','HEAD').strip()
tracked_diff=git('diff','--name-only','HEAD')
assert head_now==inventory['head'] and not tracked_diff
summary=dict(head=head_now,tracked_diff=tracked_diff,window_records=len(window),upstream_count=len(upstream),mithun_count=27,base_count=base_count,merge_count=len(merges),sync_count=len(syncs),unique_records=len(set(assigned)),unique_endpoints=len(all_endpoints),table_rows=len(rows),unit_results=unit_results,strict_result_counts=reverse_counts,citation_range_count=len(citations),citations=citations,pending_sync_landed=False,case_rename_summary=git('show','--format=','--summary','ab0bb0f5','--','docs/User-Guide/mcp-installation.md','docs/user-guide/mcp-installation.md'))
reviewed_paths = [out/'REPORT.md'] + [out/(u['id']+'.md') for u in units]
summary['reviewed_artifacts'] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in reviewed_paths}
completion_prefixes = ('- **Status:**', '- **Final independent synthesis verification:**')
substantive_report = '\n'.join(line for line in report.splitlines() if not line.startswith(completion_prefixes)) + '\n'
summary['report_content_sha256_excluding_completion_markers'] = hashlib.sha256(substantive_report.encode()).hexdigest()
summary['excluded_completion_line_prefixes'] = list(completion_prefixes)
summary['hash_basis'] = 'Exact file bytes for all nine reviewed artifacts; normalized report hash excludes only the two declared completion-line prefixes.'
(out/'final-synthesis-evidence.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('unit_results','citations')},indent=2))
