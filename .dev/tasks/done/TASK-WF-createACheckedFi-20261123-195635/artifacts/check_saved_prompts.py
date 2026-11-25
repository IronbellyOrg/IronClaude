"""Mechanically compare saved reviewer instructions outside the seven allowed slots."""
import re
from pathlib import Path

ARTIFACTS = Path(__file__).resolve().parent
qa = Path('/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md').read_text()
template = 'Review one task for spec compliance.\n' + qa.split('```\nReview one task for spec compliance.\n', 1)[1].split('\n```', 1)[0]
def normalized(text):
    return '\n'.join(line.rstrip() for line in text.splitlines() if line.strip())
pattern = re.escape(normalized(template))
for slot in ('task_brief', 'global_constraints', 'start_sha', 'diff', 'delta_diff', 'prior_findings', 'recheck_list'):
    # A blank slot makes its preceding space trailing whitespace, which the
    # protocol explicitly ignores. Preserve all other nonblank template text.
    pattern = pattern.replace(re.escape(' {' + slot + '}'), r'[ \t]*[\s\S]*?')
rows = []
failed = False
for path in sorted((ARTIFACTS / 'retries').glob('T*/prompt-*-*.md')):
    header, body = path.read_text().split('\n', 1)
    passed = bool(re.fullmatch(r'[0-9a-f]{40}', header) and re.fullmatch(pattern, normalized(body)))
    failed |= not passed
    rows.append(('PASS ' if passed else 'FAIL ') + str(path.relative_to(ARTIFACTS)))
rows.append('CHECK: ' + ('FAIL' if failed else 'PASS'))
with (ARTIFACTS / 'prompt-template-check.txt').open('a', encoding='utf-8') as stream:
    stream.write('RECHECK: trailing whitespace before an empty slot is ignored per qa.md\n')
    stream.write('\n'.join(rows) + '\n')
print('\n'.join(rows))
raise SystemExit(failed)
