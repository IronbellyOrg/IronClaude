"""Independent read-only Git and citation verification for two research units."""
import collections
import hashlib
import json
import os
import pathlib
import re
import subprocess

os.environ['GIT_OPTIONAL_LOCKS']='0'
root=pathlib.Path.cwd()
out=pathlib.Path(__file__).resolve().parent
units=json.loads((out/'units.json').read_text())
endpoints=json.loads((out/'endpoint-inventory.json').read_text())
checks=json.loads((out/'reverse-checks.json').read_text())
selected=[u for u in units if u['id'] in ('foundation-migration','docs-memory-releases')]
results=[]
for u in selected:
    records=[]
    paths=set()
    for c in u['commits']:
        changed=subprocess.check_output(['git','diff','--no-renames','--name-only',c['parents'][0],c['sha']],text=True).splitlines()
        paths.update(changed)
        patch=subprocess.check_output(['git','diff','--binary','--no-ext-diff',c['parents'][0],c['sha']])
        rc=subprocess.run(['git','apply','--reverse','--check','--whitespace=nowarn','-'],input=patch,capture_output=True)
        stored=next(x for x in checks if x['sha']==c['sha'])
        records.append(dict(sha=c['sha'],path_count=len(changed),paths=changed,strict_reverse_rc=rc.returncode,stored_check_agrees=rc.returncode==stored['returncode'],numstat=subprocess.check_output(['git','diff','--numstat',c['parents'][0],c['sha']],text=True)))
    endpoint=next(x for x in endpoints if x['id']==u['id'])
    text=(out/(u['id']+'.md')).read_text()
    results.append(dict(unit=u['id'],records=records,endpoint_count=len(paths),endpoints_match=paths==set(endpoint['files']),all_hashes_in_report=all(c['sha'][:8] in text for c in u['commits']),placeholders=bool(re.search(r'\{\{RF_PLACEHOLDER:',text))))
case_paths=subprocess.check_output(['git','diff','--no-renames','--name-only','--diff-filter=D','ab0bb0f5^','ab0bb0f5'],text=True).splitlines()
case=[]
for p in case_paths:
    chunks=p.split('/')
    counterpart='/'.join([chunks[0],chunks[1].lower(),*chunks[2:]])
    old=subprocess.check_output(['git','rev-parse','ab0bb0f5^:'+p],text=True).strip()
    new=subprocess.check_output(['git','rev-parse','ab0bb0f5:'+counterpart],text=True).strip()
    case.append(dict(path=p,counterpart=counterpart,equal=old==new))
caller=subprocess.run(['git','grep','-n','-E','uninstall-legacy|uninstall_legacy','HEAD','--',':!.dev'],capture_output=True,text=True)
metadata=subprocess.check_output(['git','log','--format=%H %P %aI %cI %an <%ae> %s','--no-walk',*[c['sha'] for u in selected for c in u['commits']]],text=True)
result=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),units=results,case_deleted_count=len(case),case_identical=sum(x['equal'] for x in case),case_different=sum(not x['equal'] for x in case),case=case,legacy_callers=caller.stdout,metadata=metadata)
(out/'review-foundation-docs-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(units=[{k:v for k,v in x.items() if k!='records'} for x in results],case_counts=[len(case),result['case_identical'],result['case_different']],all_strict_results_agree=all(c['stored_check_agrees'] for u in results for c in u['records']),legacy_callers=caller.stdout),indent=2))
