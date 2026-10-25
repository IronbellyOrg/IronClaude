"""Read-only Git and filesystem evidence collection; writes only adjacent txt evidence."""
from pathlib import Path
import json
import subprocess
ROOT = Path('/config/workspace/IronClaude/.dev/worktrees/ci-followup')
OUT = ROOT / '.dev/research/upstream-merge-impact'
unit = next(u for u in json.loads((OUT/'units.json').read_text()) if u['id']=='docs-memory-releases')
def git(*args):
    p = subprocess.run(['git', '-C', str(ROOT), '--no-pager', *args], capture_output=True, text=True, timeout=20)
    return f'COMMAND git {" ".join(args)}\nRETURN {p.returncode}\n{p.stdout}{p.stderr}'
for c in unit['commits']:
    (OUT/f'docs-memory-patch-{c["sha"][:8]}.txt').write_text(git('diff', '--no-ext-diff', '--find-renames', c['parents'][0], c['sha'], '--', *c['files']))
checks=[c for c in json.loads((OUT/'reverse-checks.json').read_text()) if c['unit']==unit['id']]
(OUT/'docs-memory-reverse.txt').write_text(json.dumps(checks, indent=2)+'\n')
parts=[]
for f in unit['files']:
    p=ROOT/f
    parts.append(f'\n===== PATH {f} | EXISTS {p.exists()} =====\n')
    if p.is_file():
        lines=p.read_text().splitlines()
        parts.append(f'LIVE LENGTH {len(lines)}\n')
    parts.append(git('log', '-8', '--format=%h %aI %cI %s', '--', f))
(OUT/'docs-memory-path-history.txt').write_text(''.join(parts))
(OUT/'docs-memory-unit-manifest.txt').write_text(json.dumps(unit, indent=2)+'\n')
print('Collected 14 full patches, filtered reverse checks, 30 path histories and unit manifest.')
