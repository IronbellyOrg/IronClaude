"""Inventory plugin namespace and candidate resources without loading a plugin."""
import json
import re
from pathlib import Path

root = Path.cwd()
out = Path(__file__).resolve().parent
worker = json.loads((out / 'plugin-worker-evidence.json').read_text())
pattern = re.compile(r'/sc:(?:sc:)+')
matched = {}
for directory in ('commands', 'agents'):
    for path in sorted((root / directory).glob('*.md')):
        lines = [i for i, line in enumerate(path.read_text().splitlines(), 1) if pattern.search(line)]
        if lines:
            matched[str(path.relative_to(root))] = lines
expected = {'commands/' + name for name in worker['namespace_commands']}
assert set(matched) == expected, 'Namespace inventory differs from worker return'
resources = []
for skill, key in [('sc-reflect-protocol', 'reflection_skill_candidate'), ('sc-adversarial-protocol', 'adversarial_skill_candidate')]:
    for name in worker[key]:
        src = root / 'src/superclaude/skills' / skill / name
        dst = root / 'skills' / skill / name
        resources.append({'source': str(src.relative_to(root)), 'destination': str(dst.relative_to(root)), 'source_exists': src.is_file(), 'destination_exists': dst.exists()})
for name in worker['new_agent_candidates']:
    src = root / 'src/superclaude/agents' / name
    dst = root / 'agents' / name
    resources.append({'source': str(src.relative_to(root)), 'destination': str(dst.relative_to(root)), 'source_exists': src.is_file(), 'destination_exists': dst.exists()})
assert len(resources) == 22 and all(row['source_exists'] for row in resources)
record = {'namespace_pattern': pattern.pattern, 'namespace_matches': matched,
          'command_count': len(list((root / 'commands').glob('*.md'))),
          'agent_count': len(list((root / 'agents').glob('*.md'))),
          'root_skills': sorted(p.name for p in (root / 'skills').iterdir() if p.is_dir()),
          'candidate_resources': resources,
          'retired_present': [name for name in worker['retired_commands'] if (root / 'commands' / name).exists()],
          'runtime_status': 'UNVERIFIED: inventory only, no plugin loader or execution'}
assert not record['retired_present']
(out / 'plugin-inventory.json').write_text(json.dumps(record, indent=2) + '\n')
print('Inventory confirmed: 26 namespace-matched commands, 22 existing source resource candidates; no plugin runtime executed')
