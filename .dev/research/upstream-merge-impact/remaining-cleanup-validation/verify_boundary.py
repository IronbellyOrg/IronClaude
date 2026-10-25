"""Fresh read-only comparison of validation baseline, not a product test."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path.cwd()
out = Path(__file__).resolve().parent
baseline = json.loads((out / 'baseline.json').read_text())
changed = []
for name, expected in baseline['outside_evidence_hashes'].items():
    path = root / name
    if path.is_symlink():
        actual = {'symlink': str(path.readlink())}
    elif path.is_file():
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
    else:
        actual = None
    if actual != expected:
        changed.append(name)
head = subprocess.check_output(['git', 'log', '-1', '--format=%H%n%s'], text=True)
tracked = subprocess.check_output(['git', 'diff', '--name-status', 'HEAD'], text=True)
index = subprocess.check_output(['git', 'diff', '--cached', '--name-status'], text=True)
old_paths = set(baseline['outside_evidence_hashes'])
current_paths = set(subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z']).decode().split('\0'))
added = sorted(name for name in current_paths - old_paths if name and not (root / name).is_relative_to(out))
record = {'head_unchanged': head == baseline['head']['stdout'], 'tracked_diff': tracked, 'index_diff': index, 'changed_preexisting_outside_files': changed, 'new_outside_nonignored_paths': added, 'outside_new_path_owner': 'UNVERIFIED', 'verdict': 'PASS' if head == baseline['head']['stdout'] and not tracked and not index and not changed and not added else 'FAIL'}
(out / 'validation-boundary.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
