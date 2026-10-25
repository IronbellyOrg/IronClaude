"""Read-only completeness and unchanged-checkout checks for this research."""
import json
import os
import pathlib
import re
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
root = pathlib.Path.cwd()
out = pathlib.Path(__file__).resolve().parent
units = json.loads((out/'units.json').read_text())
checks = json.loads((out/'reverse-checks.json').read_text())
errors = []
seen = []
results = []
for unit in units:
    path = out/(unit['id']+'.md')
    record = dict(unit=unit['id'], exists=path.is_file())
    if not path.is_file():
        errors.append('Missing unit report: '+unit['id'])
        results.append(record)
        continue
    text = path.read_text()
    missing = [c['sha'] for c in unit['commits'] if c['sha'][:8] not in text]
    placeholders = re.findall(r'\{\{RF_PLACEHOLDER:[^}]+\}\}',text)
    record.update(bytes=path.stat().st_size, missing_commit_ids=missing, placeholders=placeholders)
    if missing:
        errors.append('Missing commit decisions in '+unit['id']+': '+','.join(missing))
    if placeholders:
        errors.append('Unfilled unit report: '+unit['id'])
    if not all(section in text for section in ('## Findings','## Gaps','## Key Takeaways')):
        errors.append('Missing template sections: '+unit['id'])
    results.append(record)
    seen += [c['sha'] for c in unit['commits']]
assert len(checks)==54 and len({c['sha'] for c in checks})==54
if len(seen)!=54 or len(set(seen))!=54:
    errors.append('Expected exactly 54 uniquely covered Git records')
report=(out/'REPORT.md').read_text()
if '{{RF_PLACEHOLDER:' in report:
    errors.append('Final report still has placeholders')
tracked=subprocess.run(['git','diff','--exit-code','HEAD','--'],capture_output=True,text=True)
if tracked.returncode:
    errors.append('Tracked checkout changed or diff command failed: '+tracked.stderr)
baseline=(out/'baseline-state.txt').read_text().splitlines()
current=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all'],text=True).splitlines()
def outside(lines):
    return sorted(s for s in lines if not s[3:].startswith('.dev/research/upstream-merge-impact/'))
if outside(baseline)!=outside(current):
    errors.append('Outside-scope status changed since baseline')
head_now = subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
head_expected = json.loads((out/'inventory.json').read_text())['head']
if head_now != head_expected:
    errors.append('HEAD changed since research snapshot')
result=dict(status='PASS' if not errors else 'FAIL', units=results, unique_records=len(set(seen)), strict_check_records=len(checks), head_unchanged=head_now==head_expected, tracked_checkout_unchanged=tracked.returncode==0, outside_status_unchanged=outside(baseline)==outside(current), outside_status_additions=sorted(set(outside(current))-set(outside(baseline))), outside_status_removals=sorted(set(outside(baseline))-set(outside(current))), outside_delta_authorship='UNVERIFIED; status cannot identify the writer; no outside path was modified or removed by this checker', errors=errors)
(out/'artifact-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(bool(errors))
