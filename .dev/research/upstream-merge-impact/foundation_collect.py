"""Read-only Git evidence collector; output restricted to sibling evidence files."""
import json
import subprocess
from pathlib import Path

ROOT = Path('/config/workspace/IronClaude/.dev/worktrees/ci-followup')
OUT = ROOT / '.dev/research/upstream-merge-impact'
unit = next(u for u in json.loads((OUT / 'units.json').read_text()) if u['id'] == 'foundation-migration')

def git(*args):
    r = subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True, timeout=30)
    if r.returncode:
        raise RuntimeError((args, r.returncode, r.stderr))
    return r.stdout

rows = []
for c in unit['commits']:
    sha = c['sha']
    parent = c['parents'][0]
    patch = git('diff', '--no-ext-diff', '--no-renames', parent, sha)
    (OUT / f'foundation-{sha[:8]}.patch').write_text(patch)
    statuses = {line.split('\t',1)[1]:line.split('\t',1)[0] for line in git('diff', '--name-status', '--no-renames', parent, sha).splitlines()}
    nums = {v[2]:v[:2] for line in git('diff', '--numstat', '--no-renames', parent, sha).splitlines() if len(v:=line.split('\t',2)) == 3}
    for path in c['files']:
        current = ROOT / path
        mapped = []
        if path.startswith('superclaude/'):
            mapped = [str(x.relative_to(ROOT)) for x in [ROOT/'src'/path, ROOT/'plugins'/path] if x.is_file()]
        elif path.startswith('docs/'):
            target = ROOT / path.lower()
            if target.is_file() and target != current:
                mapped = [str(target.relative_to(ROOT))]
        elif path.startswith('setup/') or path.startswith('bin/'):
            mapped = ['src/superclaude/cli/main.py']
        category = ('legacy-installer' if path.startswith(('setup/','bin/')) else
                    'legacy-runtime' if path.startswith('superclaude/') and path.endswith('.py') else
                    'legacy-primitives' if path.startswith('superclaude/') else
                    'runtime' if path.startswith('src/') and path.endswith('.py') else
                    'docs-case' if sha.startswith('ab0') else
                    'documentation' if path.startswith('docs/') or path.endswith('.md') and not path.startswith(('src/','plugins/','.claude/','skills/')) else
                    'tests' if path.startswith('tests/') else
                    'primitives' if path.startswith(('plugins/','src/','.claude/','skills/')) else
                    'build-config-tools')
        rows.append({'commit':sha,'path':path,'status':statuses.get(path),'added_deleted':nums.get(path),'class':category,'current_exists':current.is_file(),'mapped_candidates':mapped,'content_inspection':'UNVERIFIED unless specifically cited in analysis'})
(OUT/'foundation-path-coverage.json').write_text(json.dumps(rows,indent=2)+'\n')
summary = []
for c in unit['commits']:
    sha=c['sha']
    summary.append(git('show','-s','--format=fuller',sha))
    summary.append(git('diff','--stat',c['parents'][0],sha))
summary.append('CURRENT TRACKED SOURCE COUNTS\n')
tracked = git('ls-files').splitlines()
for prefix in ['src/superclaude/cli/','src/superclaude/pm_agent/','src/superclaude/execution/','tests/','superclaude/','setup/','bin/']:
    summary.append(f'{prefix}: {sum(p.startswith(prefix) for p in tracked)}\n')
summary.append('FORK-OWNED FIRST PARENT HISTORY (last 100 touching foundation paths)\n')
summary.append(git('log','--first-parent','--format=%H %s','-100','HEAD','--','src/superclaude/cli/main.py','src/superclaude/pytest_plugin.py','src/superclaude/pm_agent','src/superclaude/execution','Makefile','scripts/uninstall_legacy.sh','pyproject.toml'))
(OUT/'foundation-git-evidence.txt').write_text('\n'.join(summary))
print(json.dumps({'unique_paths':len({r['path'] for r in rows}),'path_occurrences':len(rows),'patch_lines':{c['sha'][:8]:len((OUT/f"foundation-{c['sha'][:8]}.patch").read_text().splitlines()) for c in unit['commits']}}))
