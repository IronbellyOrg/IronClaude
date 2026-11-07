"""Mechanical ledger snapshots and template-exact saved QA prompts for this run."""
from pathlib import Path
import datetime
import hashlib
import os
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[5]
PKG = Path(__file__).resolve().parents[1]
SLUG = PKG.name
LEDGER = PKG / 'progress.md'
FILES = ['src/superclaude/skills/ccsession-tag/models.py', 'src/superclaude/skills/ccsession-tag/ccsession', 'tests/unit/test_ccsession_tiers.py']

def git(*args, env=None):
    return subprocess.check_output(['git', *args], cwd=ROOT, env=env, text=True).strip()

def snapshot():
    fd, idx = tempfile.mkstemp()
    os.close(fd)
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    try:
        git('read-tree', 'HEAD', env=env)
        git('add', '-A', env=env)
        return git('write-tree', env=env)
    finally:
        os.unlink(idx)

def append(text):
    with LEDGER.open('a') as f:
        f.write(text + '\n')

if __name__ == '__main__':
    action, task = sys.argv[1:3]
    text = LEDGER.read_text()
    print(text)
    plan = (PKG / f'{SLUG}.md').read_text()
    pin = 'PLAN: sha256=' + hashlib.sha256((PKG / f'{SLUG}.md').read_bytes()).hexdigest() + ' source_sha256=' + hashlib.sha256((PKG / 'source.md').read_bytes()).hexdigest()
    assert pin in text
    folder = PKG / 'artifacts/retries' / task
    folder.mkdir(parents=True, exist_ok=True)
    if action == 'start':
        assert f'{task}: start' not in text
        tree = snapshot()
        git('update-ref', f'refs/superclaude/implement/{SLUG}/{task}', tree)
        (folder / 'q0-head').write_text(git('rev-parse', 'HEAD') + '\n')
        append(f'{task}: start sha={tree}')
        print(tree)
    elif action == 'review':
        start = re.search(rf'^{task}: start sha=([a-f0-9]{{40}})$', text, re.M).group(1)
        tree = snapshot()
        git('update-ref', f'refs/superclaude/implement/{SLUG}/retry/{task}/r1-1', tree)
        n = task[1:]
        brief = re.search(rf'## Task {n}:.*?(?=\n## Phase|\n## Pipeline|\Z)', plan, re.S).group(0)
        ac = brief.split('Acceptance criteria:\n', 1)[1]
        for i, line in enumerate(ac.strip().splitlines(), 1):
            brief += f'\n{task}.AC{i}: {line.removeprefix("- ")}'
        constraints = plan.split('## Constraints\n', 1)[1].split('\n## Phase', 1)[0]
        paths = [FILES[0], FILES[2]] if task == 'T1' else [FILES[1], FILES[2]]
        if task == 'T4':
            paths += [str((PKG / 'artifacts' / name).relative_to(ROOT)) for name in ('runtime_probe.py', 'capture_shim.py', 't4-runtime.json', 't4-tests-rerun.log', 't4-checks-final.log', 't4-delivery.txt')]
        diff = git('diff', start, '--', *paths)
        qa = Path('/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md').read_text()
        template = qa.split('```\nReview one task for spec compliance.\n', 1)[1].split('\n```', 1)[0]
        template = 'Review one task for spec compliance.\n' + template
        values = {'task_brief': brief, 'global_constraints': constraints, 'start_sha': start, 'diff': diff, 'delta_diff': '', 'prior_findings': '', 'recheck_list': ''}
        for key, value in values.items():
            template = template.replace('{' + key + '}', value)
        prompt = folder / 'prompt-1-1.md'
        assert not prompt.exists()
        prompt.write_text(start + '\n' + template + '\n')
        (folder / 'reviewed-tree').write_text(tree + '\n')
        print('PROMPT', prompt)
    elif action == 'complete':
        acs, evidence, extras = sys.argv[3:6]
        paths = [FILES[0], FILES[2]] if task == 'T1' else [FILES[1], FILES[2]]
        if task == 'T4':
            paths += ['./artifacts/' + name for name in ('runtime_probe.py', 'capture_shim.py', 't4-runtime.json', 't4-tests-rerun.log', 't4-checks-final.log', 't4-delivery.txt')]
        append(f'{task}: complete verdict=compliant ac={acs} evidence={evidence} extras={extras} files={",".join(paths)}')
        for ref in (f'refs/superclaude/implement/{SLUG}/{task}', f'refs/superclaude/implement/{SLUG}/retry/{task}/r1-1'):
            git('update-ref', '-d', ref)
        git('add', '.dev/tasks')
