"""Include both endpoints of renames in the complete historical path audit."""
import json
import os
import pathlib
import subprocess

os.environ['GIT_OPTIONAL_LOCKS']='0'
out=pathlib.Path(__file__).resolve().parent
units=json.loads((out/'units.json').read_text())
records=[]
lines=['Historical path endpoint audit','Method: git diff --no-renames --name-status FIRST_PARENT COMMIT','Default manifest counts use git diff --name-only and can omit a rename source. This audit includes every old and new endpoint.','']
all_default=set()
all_endpoints=set()
for unit in units:
    paths=set()
    commits=[]
    for rec in unit['commits']:
        output=subprocess.check_output(['git','diff','--no-renames','--name-status',rec['parents'][0],rec['sha']],text=True)
        changes=[dict(status=line.split('\t',1)[0],path=line.split('\t',1)[1]) for line in output.splitlines()]
        commits.append(dict(sha=rec['sha'],changes=changes))
        paths.update(c['path'] for c in changes)
    default=set(unit['files'])
    assert default <= paths
    extra=sorted(paths-default)
    records.append(dict(id=unit['id'],default_manifest_count=len(default),all_endpoint_count=len(paths),extra_endpoints=extra,files=sorted(paths),commits=commits))
    all_default.update(default)
    all_endpoints.update(paths)
    lines.append(f"{unit['id']}: default={len(default)} complete_endpoints={len(paths)} extra={extra}")
lines += ['',f'Across all units: default={len(all_default)} complete_endpoints={len(all_endpoints)}',f'Globally additional endpoints: {sorted(all_endpoints-all_default)}']
(out/'endpoint-inventory.json').write_text(json.dumps(records,indent=2)+'\n')
(out/'endpoint-summary.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
