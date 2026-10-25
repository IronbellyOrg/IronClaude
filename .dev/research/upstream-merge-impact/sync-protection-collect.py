"""Capture immutable local Git evidence for the sync-protection analysis."""
import ast
import os
from pathlib import Path
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
out = Path(__file__).resolve().parent
commands = [
    ('metadata', ['git', 'show', '--no-patch', '--format=fuller', 'b061b2f7', '1e8c6e16']),
    ('added-files', ['git', 'diff', '--name-status', 'b061b2f7^', 'b061b2f7']),
    ('merge-net-files', ['git', 'diff', '--numstat', '1e8c6e16^1', '1e8c6e16']),
    ('merge-versus-incoming-tip', ['git', 'diff', 'b061b2f7', '1e8c6e16', '--', '.github/workflows/pull-sync-framework.yml', 'scripts/sync_from_framework.py']),
    ('first-fork-script-change', ['git', 'show', 'f7ea213a', '--', 'scripts/sync_from_framework.py']),
    ('push-and-protection-fix', ['git', 'show', 'abdc4cdf', '--', '.github/workflows/pull-sync-framework.yml']),
    ('checkout-and-path-simplification', ['git', 'show', 'bb66aa7c', '--', '.github/workflows/pull-sync-framework.yml']),
    ('review-before-merge-flow', ['git', 'show', '053b7566', '--', '.github/workflows/pull-sync-framework.yml']),
    ('later-script-history', ['git', 'log', '--format=%H %aI %an %s', '--follow', '--', 'scripts/sync_from_framework.py']),
    ('later-workflow-history', ['git', 'log', '--format=%H %aI %an %s', '--follow', '--', '.github/workflows/pull-sync-framework.yml']),
    ('tracked-sync-consumers', ['git', 'grep', '-n', '-E', 'sync_from_framework|pull-sync-framework|FrameworkSyncer|ContentTransformer|FileSyncer|PluginJsonGenerator|McpMerger|framework-sync-commit', 'HEAD', '--', ':!.dev']),
]
with (out/'sync-protection-git-evidence.txt').open('w') as dest:
    for label, command in commands:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        dest.write(f'===== {label} =====\nCOMMAND: {command!r}\nRETURN_CODE: {result.returncode}\n')
        dest.write(result.stdout)
        dest.write(result.stderr)
        dest.write('\n')
    original = subprocess.check_output(['git', 'show', 'b061b2f7:scripts/sync_from_framework.py'], text=True)
    current = Path('scripts/sync_from_framework.py').read_text()
    # Comments, spelling of quotes, import order and docstrings do not alter runtime AST.
    old_ast, new_ast = ast.parse(original), ast.parse(current)
    old_body = [n for n in old_ast.body if not isinstance(n, (ast.Import, ast.ImportFrom))]
    new_body = [n for n in new_ast.body if not isinstance(n, (ast.Import, ast.ImportFrom))]
    same = ast.dump(ast.Module(body=old_body, type_ignores=[]), include_attributes=False) == ast.dump(ast.Module(body=new_body, type_ignores=[]), include_attributes=False)
    old_imports = sorted(ast.dump(n, include_attributes=False) for n in old_ast.body if isinstance(n,(ast.Import,ast.ImportFrom)))
    new_imports = sorted(ast.dump(n, include_attributes=False) for n in new_ast.body if isinstance(n,(ast.Import,ast.ImportFrom)))
    dest.write(f'===== static-AST-comparison =====\nNon-import AST identical={same}\nWhole AST identical={ast.dump(old_ast, include_attributes=False)==ast.dump(new_ast, include_attributes=False)}\n')
    dest.write(f'Original lines={len(original.splitlines())}; current lines={len(current.splitlines())}\n')
    dest.write(f'Original imports={old_imports!r}\nCurrent imports={new_imports!r}\n')
(out/'sync-protection-original-workflow.yml').write_text(subprocess.check_output(['git','show','b061b2f7:.github/workflows/pull-sync-framework.yml'], text=True))
(out/'sync-protection-original-script.py').write_text(original)
print('Evidence saved to sync-protection-git-evidence.txt and original source snapshots.')
print('Original/current non-import AST identical:',same)
