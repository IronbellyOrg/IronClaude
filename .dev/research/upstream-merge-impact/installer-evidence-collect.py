import json, pathlib, subprocess
root=pathlib.Path('/config/workspace/IronClaude/.dev/worktrees/ci-followup')
out=root/'.dev/research/upstream-merge-impact'
u=next(x for x in json.loads((out/'units.json').read_text()) if x['id']=='installer-packaging')
def git(*args):
 p=subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True,timeout=25)
 return p.returncode,p.stdout,p.stderr
for c in u['commits']:
 rc,text,err=git('diff','--no-ext-diff','--find-renames',c['parents'][0],c['sha'],'--')
 (out/f"installer-patch-{c['sha'][:8]}.txt").write_text(text+err)
rows=[]
for f in u['files']:
 p=root/f
 history=git('log','-8','--format=%h %aI %s','HEAD','--',f)[1]
 rows.append({'path':f,'exists':p.is_file(),'lines':len(p.read_text(errors='replace').splitlines()) if p.is_file() else None,'history':history})
(out/'installer-path-evidence.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Saved 12 parent patches and 76 current-path/history records')
