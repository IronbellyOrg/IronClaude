"""Read-only checkout/evidence capture; output stays beside this script."""

import hashlib
import json
import subprocess
from pathlib import Path

root = Path.cwd()
out = Path(__file__).resolve().parent
assert root == Path('/config/workspace/IronClaude/.dev/worktrees/ci-followup')


def git(*args):
    result = subprocess.run(['git', *args], capture_output=True, text=True)
    return {'command': ['git', *args], 'exit_code': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr}


record = {
    'cwd': str(root),
    'head': git('log', '-1', '--format=%H%n%s'),
    'status': git('status', '--short', '--branch'),
    'tracked_worktree': git('diff', '--name-status', 'HEAD'),
    'index': git('diff', '--cached', '--name-status'),
    'cleanup_commit': git('show', '--format=fuller', '--stat', 'HEAD'),
    'legacy_references': git('grep', '-n', '-E', 'uninstall[_-]legacy|uninstall_legacy\\.sh', '--', '.', ':!.dev'),
}
pkg = root / '.dev/tasks/done/TASK-WF-ripOutTheFramewo-20261023-134610'
files = [pkg / (pkg.name + '.md'), pkg / 'source.md', pkg / 'progress.md', pkg / 'return-contract.yaml']
files += sorted(p for p in (pkg / 'artifacts').rglob('*') if p.is_file())
files += [root / '.dev/tasks/to-do/TASK-WF-ripOutTheFramewo-20261023-134610']
record['completed_artifacts'] = []
for path in files:
    row = {'path': str(path.relative_to(root)), 'exists': path.exists(), 'is_symlink': path.is_symlink()}
    if path.is_file():
        data = path.read_bytes()
        row.update(sha256=hashlib.sha256(data).hexdigest(), lines=len(data.splitlines()), bytes=len(data))
    record['completed_artifacts'].append(row)
record['all_nonignored_untracked_paths'] = git('ls-files', '--others', '--exclude-standard')
record['outside_evidence_hashes'] = {}
tracked = subprocess.check_output(['git', 'ls-files', '-z']).decode().split('\0')
untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z']).decode().split('\0')
for name in sorted(set(tracked + untracked)):
    if not name:
        continue
    path = root / name
    if path.is_relative_to(out):
        continue
    if path.is_symlink():
        record['outside_evidence_hashes'][name] = {'symlink': str(path.readlink())}
    elif path.is_file():
        record['outside_evidence_hashes'][name] = hashlib.sha256(path.read_bytes()).hexdigest()
    else:
        record['outside_evidence_hashes'][name] = None
(out / 'baseline.json').write_text(json.dumps(record, indent=2) + '\n')
print('Captured live HEAD/index/worktree and artifact inventory without running acceptance checks; outside-evidence hashes:', len(record['outside_evidence_hashes']))
