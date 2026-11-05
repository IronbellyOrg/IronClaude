"""Update only the protocol's diagnostic round metadata under a file lock."""
import fcntl
import json
import os
from pathlib import Path
import tempfile

root = Path('/home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption')
store = root / '.dev/troubleshoot/diagnosability-rounds.json'
out = root / '.dev/troubleshoot/untyped-install-core-files-skips-files-20261031153823'
branch = 'feat/codegraph-adoption'
venue = 'install_core_files skips files (no repro command supplied)'
with (store.parent / (store.name + '.lock')).open('a') as lock:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    data = json.loads(store.read_text()) if store.exists() else {}
    if not isinstance(data, dict):
        raise ValueError('Corrupt counter mapping')
    bucket = data.setdefault(branch, {})
    old = bucket.get(venue, 0)
    if type(old) is not int or old < 0:
        raise ValueError('Invalid round')
    bucket[venue] = old + 1
    with tempfile.NamedTemporaryFile(mode='w', dir=store.parent, prefix='.rounds-', delete=False) as tmp:
        json.dump(data, tmp, indent=2)
        tmp.write('\n')
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name
    os.replace(temp_name, store)
    snapshot = {'branch': branch, 'repro-venue-id': venue, 'round': old + 1, 'previous': old, 'identity_limitation': 'No repro venue supplied; retain existing issue-based unknown-venue key.'}
    (out / 'diagnosability-rounds.json').write_text(json.dumps(snapshot, indent=2) + '\n')
    print(json.dumps(snapshot))
