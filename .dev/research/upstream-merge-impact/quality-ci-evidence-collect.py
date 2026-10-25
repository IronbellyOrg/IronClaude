import ast
import json
import subprocess
from pathlib import Path

root = Path('/config/workspace/IronClaude/.dev/worktrees/ci-followup')
out = root / '.dev/research/upstream-merge-impact'
unit = next(u for u in json.loads((out / 'units.json').read_text()) if u['id'] == 'quality-ci')
def git(*args):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, timeout=20)
    return {'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
result = {'head': git('rev-parse', 'HEAD'), 'commits': {}, 'paths': {}}
for c in unit['commits']:
    sha = c['sha']
    patch = git('diff', c['parents'][0], sha, '--')
    (out / f'quality-ci-{sha[:8]}.patch').write_text(patch['stdout'])
    item = {'metadata': c, 'patch_result': patch['returncode'], 'ancestry_to_head': git('merge-base', '--is-ancestor', sha, 'HEAD'), 'ast_comparison': {}}
    for f in c['files']:
        if f.endswith('.py'):
            before = git('show', f'{c["parents"][0]}:{f}')
            after = git('show', f'{sha}:{f}')
            try:
                a = ast.dump(ast.parse(before['stdout']), include_attributes=False)
                b = ast.dump(ast.parse(after['stdout']), include_attributes=False)
                item['ast_comparison'][f] = {'equal': a == b}
            except SyntaxError as e:
                item['ast_comparison'][f] = {'error': str(e)}
    result['commits'][sha] = item
for f in unit['files']:
    p = root / f
    result['paths'][f] = {'exists': p.is_file(), 'line_count': len(p.read_text().splitlines()) if p.is_file() else None, 'history': git('log', '--format=%h %ad %an %s', '--date=short', '-18', 'b00547ad..HEAD', '--', f)}
result['workflow_paths'] = git('ls-files', '.github/workflows')
result['runtime_references'] = git('grep', '-n', '-E', 'superclaude\.execution|from .*execution import|superclaude\.pm_agent|superclaude\.cli\.(install_commands|install_skill|doctor)', '--', 'src', 'tests', 'pyproject.toml', 'Makefile')
(out / 'quality-ci-evidence.json').write_text(json.dumps(result, indent=2))
print(json.dumps({'commits': len(result['commits']), 'paths': len(result['paths']), 'patches': 5, 'output': str(out / 'quality-ci-evidence.json')}))
