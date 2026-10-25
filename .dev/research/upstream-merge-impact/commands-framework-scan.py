"""Read all assigned historical changes and inventory current consumers, no Git writes."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
root = Path.cwd()
out = root/'.dev/research/upstream-merge-impact'
evidence = out/'commands-framework-evidence'
evidence.mkdir(exist_ok=True)
units = json.loads((out/'units.json').read_text())
unit = next(u for u in units if u['id']=='commands-framework')

def git(*args):
    return subprocess.check_output(['git',*args])

patches=[]
for commit in unit['commits']:
    sha=commit['sha']
    patch=git('diff','--no-ext-diff','--binary',commit['parents'][0],sha)
    (evidence/(sha[:8]+'.patch')).write_bytes(patch)
    patches.append((sha,len(patch)))

records=[]
for path in unit['files']:
    history=[]
    for c in unit['commits']:
        if path not in c['files']:
            continue
        sha=c['sha']
        blob=git('show',f'{sha}:{path}')
        dest=evidence/'history'/sha[:8]/path
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(blob)
        text=blob.decode('utf-8',errors='replace')
        history.append(dict(commit=sha,lines=len(text.splitlines()),sha256=hashlib.sha256(blob).hexdigest(),headings=re.findall(r'^#{1,3} .+$',text,re.M)[:25],snapshot=str(dest.relative_to(root))))
    current=root/path
    text=current.read_text(errors='replace') if current.is_file() else ''
    mapped=path
    if path.startswith('docs/') and not current.is_file():
        parts=Path(path).parts
        normalized='/'.join(part.lower() if i==1 else part for i,part in enumerate(parts))
        if (root/normalized).is_file():
            mapped=normalized
    elif path.startswith('plugins/superclaude/'):
        mapped=path.replace('plugins/superclaude/','src/superclaude/',1)
    mapped_exists=(root/mapped).is_file()
    family='documentation'
    if '/commands/' in path: family='command'
    elif '/agents/' in path: family='agent'
    elif '/core/' in path: family='core'
    elif '/mcp/configs/' in path: family='MCP configuration'
    elif '/mcp/' in path: family='MCP descriptor'
    elif '/modes/' in path: family='mode'
    elif '/examples/' in path: family='example'
    elif path in ('MANIFEST.in','pyproject.toml'): family='packaging'
    if path.endswith('__init__.py'): family+=' package marker'
    records.append(dict(path=path,family=family,current_exists=current.is_file(),current_lines=len(text.splitlines()),mapped_path=mapped,mapped_exists=mapped_exists,current_sha256=hashlib.sha256(current.read_bytes()).hexdigest() if current.is_file() else None,history=history))
assert len(records)==217
(evidence/'path-inventory.json').write_text(json.dumps(records,indent=2)+'\n')
summary=['# Complete changed-path scan: commands-framework','','Every assigned blob was read in full by the collector. This is a mechanical content/identity scan, not proof of complete semantic review. Historical snapshots and complete patches are retained for verification.','',f'Unique paths: {len(records)}','', '| Path | Family | Current status | Historical commits |','|---|---|---|---|']
for r in records:
    status='present' if r['current_exists'] else ('absent; mapped '+r['mapped_path'] if r['mapped_exists'] else 'absent; no direct mapping')
    summary.append('| `'+r['path']+'` | '+r['family']+' | '+status+' | '+', '.join(h['commit'][:8] for h in r['history'])+' |')
(evidence/'path-coverage.md').write_text('\n'.join(summary)+'\n')
from collections import Counter
print('Families',dict(Counter(r['family'] for r in records)))
print('Current paths present',sum(r['current_exists'] for r in records),'absent',sum(not r['current_exists'] for r in records))
print('Patches',patches)
print('Evidence',evidence)
