"""Independent read-only verification of the executed removal task."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

root = Path.cwd()
out = root / '.dev/research/upstream-merge-impact'
task = root / '.dev/tasks/done/TASK-WF-ripOutTheFramewo-20261023-134610'
os.environ['GIT_OPTIONAL_LOCKS'] = '0'
baseline = (task / 'artifacts/t1-baseline.txt').read_text().splitlines()[0].split('=', 1)[1]

def run(args):
    p = subprocess.run(args, cwd=root, capture_output=True, text=True)
    return dict(command=args, returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)

def original(path):
    return subprocess.check_output(['git', 'show', f'{baseline}:{path}'], cwd=root)

expected_status = {'M\t.github/workflows/README.md', 'D\t.github/workflows/pull-sync-framework.yml', 'M\t.github/workflows/test.yml', 'D\tdocs/.framework-sync-commit', 'D\tscripts/sync_from_framework.py'}
status = run(['git', 'diff', '--name-status', baseline, '--', '.', ':!.dev'])
assert status['returncode'] == 0
assert set(status['stdout'].splitlines()) == expected_status
absent = {}
for path in ('.github/workflows/pull-sync-framework.yml', 'scripts/sync_from_framework.py', 'docs/.framework-sync-commit'):
    absent[path] = not os.path.lexists(root/path)
assert all(absent.values())
readme_path = '.github/workflows/README.md'
old = original(readme_path).decode()
remove = [
    '  - Upload coverage to Codecov\n',
    '### 4. **pull-sync-framework.yml** - Framework Sync\n\nScheduled (every 6 hours) and manual sync from the upstream SuperClaude_Framework repository. The sync does not push to master: it force-pushes to the `sync/framework` branch and opens a pull request into master, reusing an open one if there is one.\n\n',
    '### Coverage upload fails\n\n- This is non-blocking (fail_ci_if_error: false)\n- The upload step passes `secrets.CODECOV_TOKEN`, so the `CODECOV_TOKEN` repository secret must exist\n\n',
    "5. **Non-blocking coverage**: Don't fail on coverage upload errors\n",
]
for block in remove:
    assert old.count(block) == 1, repr(block)
    old = old.replace(block, '', 1)
for before, after in (
    ('Coverage reports are generated on Python 3.10 and uploaded to Codecov.', 'Coverage reports are generated on Python 3.10.'),
    ('6. **Manual triggers**: Add `workflow_dispatch` for debugging', '5. **Manual triggers**: Add `workflow_dispatch` for debugging'),
):
    assert old.count(before) == 1
    old = old.replace(before, after, 1)
assert (root/readme_path).read_text() == old
search = run(['git','grep','-n','-i','-E','pull-sync-framework|sync_from_framework|framework-sync-commit|codecov','--','.',':!.dev',':!src/superclaude/templates/documents/readme_template.md'])
assert search['returncode'] == 1 and not search['stdout'] and not search['stderr']
diff_check = run(['git','diff','--check'])
assert diff_check['returncode'] == 0
immutable = {}
for path in ('pyproject.toml','src/superclaude/templates/documents/readme_template.md'):
    immutable[path] = (root/path).read_bytes() == original(path)
assert all(immutable.values())
checker_env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', UV_CACHE_DIR=str(out/'.uv-cache'))
checker_cmd = ['uv','run','--no-sync','python',str(task/'artifacts/check_test_workflow.py')]
checker = subprocess.run(checker_cmd, cwd=root, capture_output=True, text=True, env=checker_env)
assert checker.returncode == 0, checker.stderr
branch = run(['git','branch','--show-current'])
head = run(['git','rev-parse','HEAD'])
assert branch['stdout'].strip() == 'feature/remove-framework-sync-codecov'
assert head['stdout'].strip() == baseline
logs = {}
for name in ('t1-removal.log','t2-workflow-check.log','t3-reference-check.log'):
    path=task/'artifacts'/name
    body=path.read_bytes()
    logs[name]=dict(exists=True,lines=len(body.splitlines()),sha256=hashlib.sha256(body).hexdigest())
result=dict(status='PASS',baseline=baseline,branch=branch,head=head,exact_five_path_diff=status,three_targets_absent_without_symlinks=absent,exact_readme_transform=True,protected_files_unchanged=immutable,stale_reference_search=search,diff_check=diff_check,workflow_checker=dict(command=checker_cmd,returncode=checker.returncode,stdout=checker.stdout,stderr=checker.stderr),retained_logs=logs,commit_or_remote_effects='HEAD equals baseline: no resulting commit in this branch. Remote mutation history and live PR/branch state UNVERIFIED; no remote operation performed by review.',runtime='Only task-owned static YAML/file assertions executed. No project test suite, hosted Actions, installer, sync script, build or real revert executed.')
(out/'executed-cleanup-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
