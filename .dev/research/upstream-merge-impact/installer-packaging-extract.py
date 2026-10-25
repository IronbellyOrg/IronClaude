"""Preserve read-only Git evidence for the assigned installer unit."""
import json
import os
from pathlib import Path
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
out = Path(__file__).resolve().parent
units = json.loads((out/'units.json').read_text())
unit = next(u for u in units if u['id'] == 'installer-packaging')
assert len(unit['commits']) == 12 and len(unit['files']) == 76

def git(*args):
    return subprocess.check_output(['git', *args], text=True)

for r in unit['commits']:
    patch = git('show', '--format=fuller', '--find-renames', r['sha'])
    (out/f"installer-packaging-{r['sha'][:8]}.patch").write_text(patch)
paths = []
for path in unit['files']:
    p = Path(path)
    log = git('log', '-8', '--format=%h %cI %an %s', '--', path)
    paths.append({'path': path, 'exists': p.is_file(), 'current_bytes': p.stat().st_size if p.is_file() else None, 'recent_history': log})
(out/'installer-packaging-paths.json').write_text(json.dumps(paths,indent=2)+'\n')
checks = json.loads((out/'reverse-checks.json').read_text())
checks = [r for r in checks if r['unit'] == 'installer-packaging']
assert len(checks) == 12
(out/'installer-packaging-reverse.json').write_text(json.dumps(checks,indent=2)+'\n')
for sha, paths_to_show in {
    'de177847': ['src/superclaude/cli/main.py'],
    'd90bed68': ['src/superclaude/cli/main.py', 'src/superclaude/hooks/hooks.json'],
    '2219545c': ['src/superclaude/cli/install_commands.py'],
    'cbc9321c': ['src/superclaude/cli/main.py'],
    '38c20f88': ['src/superclaude/cli/main.py'],
    '08cbea9e': ['MANIFEST.in', 'setup.py', 'pyproject.toml'],
    '051f39fe': ['src/superclaude/cli/install_commands.py'],
}.items():
    (out/f'installer-packaging-fork-{sha}.patch').write_text(git('show', '--format=fuller', sha, '--', *paths_to_show))
print('12 full commit patches preserved; 76 path states and last 8 history entries recorded.')
for p in paths:
    print(('PRESENT' if p['exists'] else 'ABSENT'), p['path'], p['current_bytes'])
