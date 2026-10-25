"""Partition enumerated changes and record read-only strict reverse checks."""
import json
import pathlib
import subprocess

out = pathlib.Path(__file__).resolve().parent
data = json.loads((out/'inventory.json').read_text())
groups = {
    'foundation-migration': ('Python architecture migration and legacy removal', 'c733413d 10844490 ab0bb0f5'),
    'installer-packaging': ('Installer, update command, wheel resources and installation entry points', '8c0559ca ad80f57f 25785363 c6e72825 2847f755 81343a67 42946f84 18c0e4e1 fd8c67f6 9ca48494 074b9948 323137a9'),
    'quality-ci': ('CI, publication, lint and formatting changes', '32c0086d 43bfa0aa 8da05a17 e2896335 b00547ad'),
    'docs-memory-releases': ('Memory documentation, translations, reference docs and release metadata', 'bea4bfe2 bec0b0c3 a3541f43 16caa494 58008c94 61591211 86a26333 d2a3b58b d11abead 43ca81d1 310136c1 208c66e1 1bd92c91 ad6b2e99'),
    'commands-framework': ('Recommendation command, restored primitives and explicit boundaries', '0ef8ea81 ab8904bc 3762d6ab e61aaba7'),
    'mcp-installation': ('MCP gateway, server descriptors, encoding and February bug fix', '5a685958 67449770 1b14d065 202660b5 6ae5e998 04c9b85c 3294a0ad 55c658c7 0ceb2955'),
    'sync-protection': ('March upstream sync protection fix and merge', 'b061b2f7 1e8c6e16'),
    'automated-sync-copies': ('Five merged bot syncs, namespace copies and sync pointer updates', '465797ad ff5f73ad ec9f066f 66d54204 f14f0cca'),
}
all_records = {r['sha']:r for key in ('upstream_commits','sync_commits','merges') for r in data[key]}
units = []
assigned = set()
checks = []
for uid,(title,shorts) in groups.items():
    records=[]
    for short in shorts.split():
        matches=[r for sha,r in all_records.items() if sha.startswith(short)]
        assert len(matches)==1,short
        r=matches[0]
        assert r['sha'] not in assigned,short
        assigned.add(r['sha'])
        parent=r['parents'][0] if r['parents'] else None
        files=subprocess.check_output(['git','diff','--name-only',parent,r['sha']],text=True).splitlines() if parent else r['files']
        rec=dict(r,files=files)
        records.append(rec)
        patch=subprocess.check_output(['git','diff','--binary','--no-ext-diff',parent,r['sha']])
        result=subprocess.run(['git','apply','--reverse','--check','--whitespace=nowarn','-'],input=patch,capture_output=True)
        checks.append(dict(unit=uid,sha=r['sha'],method='git diff --binary PARENT COMMIT | git apply --reverse --check --whitespace=nowarn -',returncode=result.returncode,stdout=result.stdout.decode(errors='replace'),stderr=result.stderr.decode(errors='replace'),actual_git_revert='UNVERIFIED; no Git state mutation authorized'))
    paths=sorted({p for r in records for p in r['files']})
    units.append(dict(id=uid,title=title,commits=records,files=paths,file_count=len(paths)))
assert assigned==set(all_records),(set(all_records)-assigned)
(out/'units.json').write_text(json.dumps(units,indent=2)+'\n')
(out/'reverse-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(out/'baseline-state.txt').write_text(subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all'],text=True))
for u in units:
    print(u['id'],len(u['commits']),'commits',u['file_count'],'unique files')
print('coverage',len(assigned),'of',len(all_records),'records; no unassigned commits')
