"""Read-only Git evidence collection for MCP installation unit."""
import json
from pathlib import Path
import subprocess

root = Path('/config/workspace/IronClaude/.dev/worktrees/ci-followup')
out = root / '.dev/research/upstream-merge-impact'
unit = next(u for u in json.loads((out / 'units.json').read_text()) if u['id'] == 'mcp-installation')

def git(*args):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, timeout=30)
    return f'COMMAND: git {" ".join(args)}\nRETURN: {p.returncode}\n{p.stdout}{p.stderr}'

for c in unit['commits']:
    sha = c['sha']
    content = git('show', '-s', '--format=fuller', sha)
    content += git('diff', '--find-renames', c['parents'][0], sha, '--', *c['files'])
    (out / f'mcp-patch-{sha[:8]}.txt').write_text(content)

content = git('log', '--format=%h %aI %cI %an %s', '--first-parent', 'HEAD', '--', *unit['files'])
content += '\nCURRENT PATH STATUS\n'
for path in unit['files']:
    content += f'{path}: {"EXISTS" if (root / path).exists() else "MISSING"}\n'
content += git('log', '--format=%h %aI %cI %an %s', '--first-parent', 'HEAD', '--', 'src/superclaude/cli/install_codebase_memory.py', 'tests/cli/test_install_mcp_registry.py')
(out / 'mcp-history-evidence.txt').write_text(content)
print('Saved 9 parent-to-commit patches and current/history evidence under authorized output directory.')
