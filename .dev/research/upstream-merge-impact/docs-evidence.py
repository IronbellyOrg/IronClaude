"""Collect only this unit's historical patches and current-file inventory."""
import json
import os
from pathlib import Path
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
out=Path(__file__).resolve().parent
unit=next(u for u in json.loads((out/'units.json').read_text()) if u['id']=='docs-memory-releases')

def git(*args):
    return subprocess.check_output(['git',*args],text=True)

patches=[]
for record in unit['commits']:
    patches += [f"===== COMMIT {record['sha']} {record['subject']} =====",git('show','--format=fuller','--no-ext-diff','--find-renames',record['sha'])]
(out/'docs-commit-patches.txt').write_text('\n'.join(patches))
rows=[]
for path in unit['files']:
    p=Path(path)
    commits=[r['sha'][:8] for r in unit['commits'] if path in r['files']]
    history=git('log','HEAD','--format=%h %cI %an %s','--',path)
    rows += [f"===== PATH {path} =====",'Assigned commits: '+', '.join(commits),'Current exists: '+str(p.is_file()), 'Current lines: '+str(len(p.read_text().splitlines()) if p.is_file() else 0),'History:',history]
(out/'docs-path-history.txt').write_text('\n'.join(rows))
print('patch lines',len('\n'.join(patches).splitlines()))
for path in unit['files']:
    p=Path(path)
    print(path, 'lines='+str(len(p.read_text().splitlines())) if p.is_file() else 'MISSING')
