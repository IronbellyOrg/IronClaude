"""Check written-plan structure only; does not execute a cleanup task."""
import json
import re
from pathlib import Path

out = Path(__file__).resolve().parent
expected = {'01-legacy-uninstall.md': 1, '02-root-plugin.md': 4, '03-memory-docs.md': 4, '04-gateway-claims.md': 1}
checks = {}
for name, count in expected.items():
    text = (out / 'plans' / name).read_text()
    sections = re.split(r'^## Task (\d+):[^\n]*\n', text, flags=re.M)
    ids = [int(sections[i]) for i in range(1, len(sections), 2)]
    bodies = [sections[i] for i in range(2, len(sections), 2)]
    checks[name] = {
        'contiguous_task_ids': ids == list(range(1, count + 1)),
        'acceptance_criteria_per_task': len(bodies) == count and all('Acceptance criteria:\n- ' in body for body in bodies),
        'constraints_and_source': '\n## Constraints\n' in text and '\nSource: ' in text,
        'no_placeholders': 'RF_PLACEHOLDER' not in text and '<!-- TODO -->' not in text,
        'no_duplicate_task_syntax': re.search(r'^\s*(?:[-*]\s+\[[ xX]\]|\d+[.)]\s)', text, re.M) is None,
        'not_a_managed_package': 'schema: workflow-plan/' not in text,
        'plain_dashes': '—' not in text and '–' not in text,
    }
    for i, body in zip(ids, bodies):
        for dep in re.findall(r'^Depends on: Task (\d+)$', body, re.M):
            assert int(dep) < i, (name, i, dep)
verdict = 'PASS' if all(all(row.values()) for row in checks.values()) else 'FAIL'
result = {'scope': 'written document structure only, not implementation or runtime acceptance', 'verdict': verdict, 'checks': checks}
(out / 'plan-structure-check.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
assert verdict == 'PASS'
