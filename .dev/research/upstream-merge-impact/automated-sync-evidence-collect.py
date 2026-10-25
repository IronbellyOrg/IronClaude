from pathlib import Path
import json, subprocess

root = Path('/config/workspace/IronClaude/.dev/worktrees/ci-followup')
out = root / '.dev/research/upstream-merge-impact'
unit = next(x for x in json.loads((out/'units.json').read_text()) if x['id']=='automated-sync-copies')
def git(*args):
    p = subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True,timeout=30)
    return p.returncode,p.stdout,p.stderr
for commit in unit['commits']+[{'sha':'d3cf593808f5e5df12da7f0c3e506556fdc34e01'}]:
    sha=commit['sha']
    rc,metadata,err=git('show','--no-patch','--format=fuller',sha)
    rc,patch,err=git('diff','--no-ext-diff',f'{sha}^',sha)
    (out/f'automated-sync-patch-{sha[:8]}.txt').write_text(metadata+'\n'+patch+err)
rows=[]
texts=[]
for path in unit['files']:
    p=root/path
    current=p.read_text() if p.is_file() else None
    target=None
    if path.startswith(('agents/','commands/')):
        category,name=path.split('/',1)
        target=f'src/superclaude/{category}/{name.removeprefix("sc-")}'
    src=root/target if target else None
    status='missing' if current is None else 'present'
    same=src and src.is_file() and current is not None and current==src.read_text()
    rc,log,err=git('log','--format=%h %ad %s','--date=iso-strict','HEAD','--',path)
    rows.append(f'{path}\t{status}\tcanonical={target}\tbyte_identical={bool(same)}\n{log}')
    texts.append(f'===== {path} ({status}) =====\n'+(current or '[ABSENT]\n'))
(out/'automated-sync-path-history.txt').write_text('\n'.join(rows))
(out/'automated-sync-current-paths.txt').write_text('\n'.join(texts))
proof=[]
for sha in [c['sha'] for c in unit['commits']]+['d3cf593808f5e5df12da7f0c3e506556fdc34e01']:
    rc,stdout,stderr=git('merge-base','--is-ancestor',sha,'HEAD')
    proof.append(f'merge-base --is-ancestor {sha} HEAD: rc={rc} {stdout}{stderr}')
rc,stdout,stderr=git('for-each-ref','--contains','d3cf5938','--format=%(refname) %(objectname)')
proof.append('refs containing pending commit:\n'+stdout+stderr)
rc,stdout,stderr=git('show','--no-patch','--format=%H %P','origin/sync/framework')
proof.append('origin/sync/framework:\n'+stdout+stderr)
(out/'automated-sync-ancestry.txt').write_text('\n'.join(proof))
print('Saved six patches, current content of all 54 paths, per-path history/comparison, and ancestry evidence.')
