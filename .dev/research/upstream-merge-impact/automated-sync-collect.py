"""Collect read-only sync evidence; outputs stay within this research directory."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
root = Path.cwd()
out = Path(__file__).resolve().parent
units = json.loads((out/'units.json').read_text())
unit = next(u for u in units if u['id'] == 'automated-sync-copies')
records = []
patches = []
source_lines = []
for r in unit['commits']:
    patch = subprocess.check_output(['git','show','--no-ext-diff','--format=fuller',r['sha']],text=True)
    patches += [patch]
    for p in r['files']:
        body = subprocess.check_output(['git','show',r['sha']+':'+p],text=True)
        assert isinstance(body,str)
for p in unit['files']:
    path = root/p
    if not path.exists():
        records.append(dict(path=p,exists=False,changes=[r['sha'][:8] for r in unit['commits'] if p in r['files']]))
        continue
    text = path.read_text()
    headings = [f'{i}:{line}' for i,line in enumerate(text.splitlines(),1) if line.startswith('#')]
    refs = [f'{i}:{line}' for i,line in enumerate(text.splitlines(),1) if '/sc:sc:' in line or 'Skill(' in line or 'SKILL.md' in line or 'sequential' in line.lower()]
    if p.startswith('commands/sc-'):
        canon = 'src/superclaude/commands/'+Path(p).name.removeprefix('sc-')
    elif p.startswith('agents/sc-'):
        canon = 'src/superclaude/agents/'+Path(p).name.removeprefix('sc-')
    else:
        canon = None
    canon_text = (root/canon).read_text() if canon and (root/canon).exists() else None
    records.append(dict(path=p,exists=True,lines=len(text.splitlines()),sha256=hashlib.sha256(text.encode()).hexdigest(),changes=[r['sha'][:8] for r in unit['commits'] if p in r['files']],canonical_path=canon,canonical_exists=canon_text is not None,canonical_identical=text==canon_text,heading=headings[0] if headings else '',namespace_duplication_lines=refs))
    source_lines += [f'===== {p} =====']+[f'{i:04d} {line}' for i,line in enumerate(text.splitlines(),1)]
queries = ['sc-backend-architect','commands/sc-','agents/sc-','.framework-sync-commit','resolve_target(','clean_command_names','PluginJsonGenerator']
searches=[]
for pattern in queries:
    args=['git','grep','-n','-F',pattern,'--','.',':(exclude).dev/**',':(exclude).claude/**',':(exclude)agents/**',':(exclude)commands/**',':(exclude)PROJECT_INDEX*']
    r=subprocess.run(args,capture_output=True,text=True)
    assert r.returncode in (0,1),r.stderr
    searches.append(dict(pattern=pattern,returncode=r.returncode,stdout=r.stdout))
checks = [r for r in json.loads((out/'reverse-checks.json').read_text()) if r['unit']==unit['id']]
result=dict(unit=unit['id'],snapshot=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),file_count=len(unit['files']),current_file_count=sum(r['exists'] for r in records),records=records,searches=searches,checks=checks)
(out/'automated-sync-evidence.json').write_text(json.dumps(result,indent=2)+'\n')
(out/'automated-sync-patches.txt').write_text('\n'.join(patches))
(out/'automated-sync-content.txt').write_text('\n'.join(source_lines)+'\n')
print('Historical paths',len(records),'Current paths',sum(r['exists'] for r in records))
print('Root prompt line count',sum(r.get('lines',0) for r in records))
for r in records:
    print(r['path'],'exists='+str(r['exists']),r.get('heading',''), 'canon='+str(r.get('canonical_identical')))
for q in searches:
    print('SEARCH',q['pattern'],q['stdout'][:5000])
