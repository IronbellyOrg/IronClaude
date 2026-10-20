"""Audit-only input hashing and recorded-tree diff attribution; no product writes."""
import ast
import difflib
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CHECKOUT = Path('/config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP')
UNIT = CHECKOUT / '.dev/tasks/done/TASK-WF-spec-20261019-204314'
OUTPUT = UNIT / 'artifacts/reflect/post-20261020042605'  # pinned before first write
PLAN = UNIT / (UNIT.name + '.md')
LOG = UNIT / 'progress.md'
SOURCE = UNIT / 'source.md'
EXCLUDED_PARTS = {'__pycache__', '.pytest_cache', 'htmlcov', '.mypy_cache', '.ruff_cache', 'target', '.hypothesis'}
EXCLUDED_SUFFIXES = {'.pyc', '.pyo', '.pyd', '.tsbuildinfo'}


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(relative, value):
    target = OUTPUT / relative
    assert target.is_relative_to(OUTPUT)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n')


def audit(wave, step, outcome, evidence, detail):
    with (OUTPUT / 'audit.log').open('a') as stream:
        stream.write(json.dumps(dict(wave=wave, step=step, timestamp=now(), outcome=outcome,
                                     evidence_ref=evidence, detail=detail)) + '\n')


def delivery_records():
    text = LOG.read_text()
    starts = []
    latest = {}
    owners = {}
    for line in text.splitlines():
        match = re.match(r'^T([0-9]+): start sha=([0-9a-f]{40})$', line)
        if match:
            starts.append(('T' + match[1], match[2]))
        match = re.match(r'^T([0-9]+): (complete|blocked) verdict=([^ ]+).* files=(.+)$', line)
        if match:
            task = 'T' + match[1]
            latest[task] = dict(status=match[2], verdict=match[3])
            for name in match[4].split(','):
                candidate = CHECKOUT / name
                if not candidate.resolve().is_relative_to(CHECKOUT) or not candidate.is_file():
                    raise RuntimeError('Unsafe/missing delivery: ' + name)
                owners.setdefault(name, set()).add(task)
    return starts, latest, owners


def inputs():
    # Never retarget OUTPUT. Detect changed symlink components rather than follow them.
    assert UNIT.resolve() == UNIT
    for parent in [OUTPUT, *OUTPUT.parents]:
        if parent.is_relative_to(UNIT) and parent.is_symlink():
            raise RuntimeError('output_symlink_escape')
    _, _, owners = delivery_records()
    paths = {PLAN, LOG, SOURCE}
    paths.update(CHECKOUT / name for name in owners)
    linked = re.findall(r'(?<![A-Za-z0-9_])(?:src|tests|docs)/[A-Za-z0-9_./-]+\.(?:py|md)|\bREADME\.md\b', PLAN.read_text())
    paths.update(CHECKOUT / name for name in linked)
    for item in UNIT.rglob('*'):
        if item.is_relative_to(OUTPUT):
            continue
        if item.is_symlink():
            raise RuntimeError('Unverified symlink input: ' + str(item))
        if item.is_file():
            paths.add(item)
    result = []
    for item in sorted(paths):
        if item.is_relative_to(OUTPUT):
            continue
        relative = item.relative_to(CHECKOUT)
        parts = relative.parts
        if any(part in EXCLUDED_PARTS or part.endswith('.egg-info') for part in parts):
            continue
        if 'node_modules' in parts and '.cache' in parts:
            continue
        if item.suffix in EXCLUDED_SUFFIXES or item.name == '.coverage' or item.name.startswith('.coverage.'):
            continue
        if not item.is_file():
            raise RuntimeError('Input disappeared: ' + str(item))
        result.append([str(relative), sha(item.read_bytes())])
    return result


def snapshot():
    files = inputs()
    digest = sha(json.dumps(files, separators=(',', ':'), ensure_ascii=True).encode())
    return dict(input_tree_sha256=digest, file_list=[dict(path=p, sha256=h) for p, h in files],
                file_count=len(files), output_root=str(OUTPUT), work_unit=str(UNIT),
                exclusions=sorted(EXCLUDED_PARTS), current_output_exclusion=str(OUTPUT))


BLOBS = {}

def blob(tree, name):
    key = (tree, name)
    if key not in BLOBS:
        test = subprocess.run(['git', 'ls-tree', tree, '--', name], cwd=CHECKOUT,
                              capture_output=True, text=True, timeout=10, check=True)
        if not test.stdout:
            BLOBS[key] = ''
        else:
            found = subprocess.run(['git', 'show', tree + ':' + name], cwd=CHECKOUT,
                                   capture_output=True, timeout=10, check=True)
            BLOBS[key] = found.stdout.decode('utf-8')
    return BLOBS[key]


def annotated_lines(name, starts):
    before = blob(starts[0][1], name).splitlines(keepends=True)
    origins = list(range(len(before)))
    owners = [None] * len(before)
    removed = {}
    increments = []
    for index, (task, tree) in enumerate(starts):
        after_text = blob(starts[index + 1][1], name) if index + 1 < len(starts) else (CHECKOUT / name).read_text()
        after = after_text.splitlines(keepends=True)
        next_origins, next_owners = [], []
        changed = []
        for operation, a, b, c, d in difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes():
            if operation == 'equal':
                next_origins.extend(origins[a:b])
                next_owners.extend(owners[a:b])
                continue
            changed.append(dict(operation=operation, before=[a + 1, b], after=[c + 1, d]))
            for origin in origins[a:b]:
                if origin is not None:
                    removed[origin] = task
            next_origins.extend([None] * (d - c))
            next_owners.extend([task] * (d - c))
        if changed:
            increments.append(dict(task_id=task, path=name, changes=changed))
        before, origins, owners = after, next_origins, next_owners
    return owners, removed, increments


def dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = dotted(node.value)
        return prefix + '.' + node.attr if prefix else node.attr
    return '<dynamic>'


def symbols_for(name, text):
    records = []
    class Visitor(ast.NodeVisitor):
        scope = []
        def visit_ClassDef(self, node):
            self.scope.append(node.name)
            records.append(dict(path=name, name='.'.join(self.scope), kind='Class', line=node.lineno, end_line=node.end_lineno,
                                bases=[ast.unparse(base) for base in node.bases]))
            self.generic_visit(node)
            self.scope.pop()
        def visit_FunctionDef(self, node):
            self.scope.append(node.name)
            lines = text.splitlines()
            calls = [dict(name=dotted(call.func), line=call.lineno,
                          statement=lines[call.lineno - 1].strip()[:300]) for call in ast.walk(node) if isinstance(call, ast.Call)]
            records.append(dict(path=name, name='.'.join(self.scope), kind='Function', line=node.lineno, end_line=node.end_lineno,
                                decorators=[ast.unparse(dec) for dec in node.decorator_list], calls=calls))
            self.generic_visit(node)
            self.scope.pop()
        visit_AsyncFunctionDef = visit_FunctionDef
    Visitor().visit(ast.parse(text, filename=name))
    return records


def collect():
    original = snapshot()
    save('artifacts/input-snapshot.yaml', original)
    starts, latest, file_tasks = delivery_records()
    patches, hunks, increments, symbols = [], [], [], []
    for name in sorted(file_tasks):
        before = blob(starts[0][1], name)
        after = (CHECKOUT / name).read_text()
        owners, deleted, changes = annotated_lines(name, starts)
        increments.extend(changes)
        before_lines, after_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
        patches.extend(difflib.unified_diff(before_lines, after_lines, fromfile='a/' + name, tofile='b/' + name, n=3))
        for group in difflib.SequenceMatcher(None, before_lines, after_lines, autojunk=False).get_grouped_opcodes(3):
            associated = set()
            for op, a, b, c, d in group:
                if op == 'equal':
                    continue
                associated.update(owner for owner in owners[c:d] if owner)
                associated.update(deleted[i] for i in range(a, b) if i in deleted)
            hunks.append(dict(hunk_id='H-%03d' % (len(hunks) + 1), path=name,
                              before=[group[0][1] + 1, group[-1][2]], after=[group[0][3] + 1, group[-1][4]],
                              matched_tasks=sorted(associated), method='recorded_start_tree_line_provenance'))
        if name.endswith('.py'):
            symbols.extend(symbols_for(name, after))
    (OUTPUT / 'artifacts/changes.patch').write_text(''.join(patches))
    save('per-hunk-evidence.yaml', hunks)
    save('artifacts/per-task-increments.yaml', increments)
    save('artifacts/symbols.json', symbols)
    domains = sorted({'code' if name.startswith('src/') else 'tests' if name.startswith('tests/') else 'docs' for name in file_tasks})
    unmapped = [h['hunk_id'] for h in hunks if not h['matched_tasks']]
    summary = dict(mode='post', baseline=starts[0][1], baseline_source='first task-log start tree',
                   task_starts=starts, latest_task_records=latest, deliveries=sorted(file_tasks),
                   hunk_count=len(hunks), unmapped_hunks=unmapped,
                   S_scope=len(file_tasks), S_domains=len(domains), domains=domains,
                   S_dev_density=(len(unmapped) / len(hunks)) if hunks else None,
                   deviation_aggregation_mode='per-file' if len(hunks) > 100 else 'per-hunk',
                   input_tree_sha256=original['input_tree_sha256'], input_tree_file_count=original['file_count'],
                   input_sha256=dict(tasklist=sha(PLAN.read_bytes()), spec=sha(SOURCE.read_bytes())),
                   output_root=str(OUTPUT), work_unit=str(UNIT))
    save('artifacts/review-context.json', summary)
    audit(0, '0.4-snapshot', 'ok', str(OUTPUT / 'artifacts/input-snapshot.yaml'),
          'Canonical hash includes whole archived package and linked/current delivery inputs; exact current output subtree excluded.')
    audit(1, '1A-1B-diff-inputs', 'ok', str(OUTPUT / 'artifacts/review-context.json'),
          'Compared recorded task-start trees to actual worktree bytes, including untracked delivery files; line attribution is not a semantic compliance verdict.')
    print(json.dumps(summary, indent=2))


def recheck():
    original = json.loads((OUTPUT / 'artifacts/input-snapshot.yaml').read_text())
    current = snapshot()
    old = {row['path']: row['sha256'] for row in original['file_list']}
    new = {row['path']: row['sha256'] for row in current['file_list']}
    differences = [dict(path=name, old_sha=old.get(name), new_sha=new.get(name),
                        change_kind='added' if name not in old else 'removed' if name not in new else 'modified')
                   for name in sorted(old.keys() | new.keys()) if old.get(name) != new.get(name)]
    result = dict(input_drift_detected=bool(differences), old_sha=original['input_tree_sha256'],
                  new_sha=current['input_tree_sha256'], input_drift_diff=differences,
                  file_count=current['file_count'], output_root=str(OUTPUT))
    save('artifacts/input-recheck.yaml', result)
    audit(5, 'input-drift-check', 'warn' if differences else 'ok', str(OUTPUT / 'artifacts/input-recheck.yaml'),
          'Reused identical pinned output exclusion and verification-artifact filters.')
    print(json.dumps(result, indent=2))
    return 1 if differences else 0


if __name__ == '__main__':
    if sys.argv[1:] == ['--recheck']:
        raise SystemExit(recheck())
    if sys.argv[1:]:
        raise SystemExit('Only --recheck is supported')
    collect()
