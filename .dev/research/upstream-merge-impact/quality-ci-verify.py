"""Read-only Git/static evidence collection for assigned quality commits."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
OUT = Path(__file__).resolve().parent

def git(*args):
    return subprocess.check_output(['git', *args], text=True)

units = json.loads((OUT / 'units.json').read_text())
unit = next(u for u in units if u['id'] == 'quality-ci')
checks = json.loads((OUT / 'reverse-checks.json').read_text())
sha_set = {r['sha'] for r in unit['commits']}
unit['reverse_checks'] = [r for r in checks if r['sha'] in sha_set]
assert len(unit['files']) == 26
assert len(unit['reverse_checks']) == 5
(OUT / 'quality-ci-inputs.json').write_text(json.dumps(unit, indent=2) + '\n')

ast_results = []
for short in ('e2896335', 'b00547ad'):
    record = next(r for r in unit['commits'] if r['sha'].startswith(short))
    for file in record['files']:
        if not file.endswith('.py'):
            continue
        old = git('show', record['sha'] + '^:' + file)
        new = git('show', record['sha'] + ':' + file)
        old_tree = ast.dump(ast.parse(old), include_attributes=False)
        new_tree = ast.dump(ast.parse(new), include_attributes=False)
        ast_results.append({'commit': short, 'path': file, 'ast_equal': old_tree == new_tree})
assert all(r['ast_equal'] for r in ast_results if r['commit'] == 'b00547ad')
assert len([r for r in ast_results if r['commit'] == 'b00547ad']) == 14
(OUT / 'quality-ci-ast-check.json').write_text(json.dumps(ast_results, indent=2) + '\n')

for short in ('32c0086d', '43bfa0aa', '8da05a17'):
    (OUT / ('quality-ci-' + short + '.patch')).write_text(git('show', '--format=fuller', short))

history = ['Snapshot: ' + git('rev-parse', 'HEAD').strip(), '']
for file in unit['files']:
    history += ['PATH: ' + file, git('log', '-n', '10', '--format=%H %cI %an %s', '--', file)]
for short in ('bb66aa7c', '053b7566', '64b730a7', '38ca920d', 'ad72b1bb', '08cbea9e'):
    history += ['FORK CHANGE: ' + short, git('show', '--format=fuller', '--stat', short)]
(OUT / 'quality-ci-history.txt').write_text('\n'.join(history))

path_status = []
for file in unit['files']:
    p = Path(file)
    path_status.append({'path': file, 'exists_at_head': p.is_file(), 'lines': len(p.read_text().splitlines()) if p.is_file() else 0, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None})
(OUT / 'quality-ci-path-status.json').write_text(json.dumps(path_status, indent=2) + '\n')
print('AST formatting equality:', sum(r['ast_equal'] for r in ast_results if r['commit'] == 'b00547ad'), 'of 14')
print('All assigned paths:', len(unit['files']))
for r in unit['reverse_checks']:
    print(r['sha'][:8], 'strict reverse rc=', r['returncode'], r['stderr'][:1400])
