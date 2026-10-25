"""Independent read-only checks for two completed upstream analyses."""
import json
import os
import pathlib
import re
import subprocess

os.environ['GIT_OPTIONAL_LOCKS']='0'
root=pathlib.Path.cwd()
out=root/'.dev/research/upstream-merge-impact'
units=json.loads((out/'units.json').read_text())
endpoints=json.loads((out/'endpoint-inventory.json').read_text())
checks=json.loads((out/'reverse-checks.json').read_text())
result={'units':[],'source_citations':[],'source_citation_issues':[],'git_records':[]}
for unit in units:
    if unit['id'] not in ('commands-framework','sync-protection'):
        continue
    paths=set()
    details=[]
    for rec in unit['commits']:
        raw=subprocess.check_output(['git','diff','--no-renames','--name-only',rec['parents'][0],rec['sha']],text=True)
        files=raw.splitlines()
        paths.update(files)
        detail={'sha':rec['sha'],'parents':rec['parents'],'path_count':len(files),'strict_check_rc':next(c['returncode'] for c in checks if c['sha']==rec['sha'])}
        details.append(detail)
    expected=next(e for e in endpoints if e['id']==unit['id'])
    report=out/(unit['id']+'.md')
    text=report.read_text()
    result['units'].append({'unit':unit['id'],'exact_endpoint_match':paths==set(expected['files']),'endpoint_count':len(paths),'currently_present':sum((root/p).is_file() for p in paths),'currently_absent':sum(not (root/p).is_file() for p in paths),'all_commits_named':all(rec['sha'][:8] in text for rec in unit['commits']),'has_placeholder':'{{RF_PLACEHOLDER:' in text,'details':details})
    pattern=re.compile(r'(?P<path>(?:src/|tests/|docs/|scripts/|plugins/|commands/|\.github/|\.claude-plugin/)[A-Za-z0-9_./@+\-]+|pyproject\.toml|Makefile):(?P<line>[0-9]+)(?:-(?P<end>[0-9]+))?')
    for m in pattern.finditer(text):
        if re.search(r'[0-9a-f]{7,40}:$',text[max(0,m.start()-42):m.start()]):
            continue
        p=root/m.group('path')
        line=int(m.group('line'))
        end=int(m.group('end') or line)
        n=len(p.read_text(errors='replace').splitlines()) if p.is_file() else 0
        item={'report':unit['id'],'report_line':text[:m.start()].count('\n')+1,'path':m.group('path'),'start':line,'end':end,'source_lines':n,'range_valid':1<=line<=end<=n}
        result['source_citations'].append(item)
        if not item['range_valid']:
            result['source_citation_issues'].append(item)
for sha in ['de177847','de04670a','238d6583','3dfac2c0','051f39fe','246acd7b','b31111a9','6dc56b1a','3ad7e207','3ae238b1','abdc4cdf','bb66aa7c','053b7566','f7ea213a','38ca920d']:
    meta=subprocess.check_output(['git','show','--no-patch','--format=%H %P %an <%ae> %s',sha],text=True).strip()
    anc=subprocess.run(['git','merge-base','--is-ancestor',sha,'HEAD'],capture_output=True).returncode
    result['git_records'].append({'commit':meta,'ancestor_of_HEAD':anc==0})
result['imported_merge_file_equality']={}
for path in ['scripts/sync_from_framework.py','.github/workflows/pull-sync-framework.yml']:
    a=subprocess.check_output(['git','show','b061b2f7:'+path])
    b=subprocess.check_output(['git','show','1e8c6e16:'+path])
    result['imported_merge_file_equality'][path]=a==b
(out/'review-commands-sync-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='source_citations'},indent=2))
