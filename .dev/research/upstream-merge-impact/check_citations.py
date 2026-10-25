"""Check exact repository-root file:line citations without claiming semantic validity."""
import json
import pathlib
import re

root=pathlib.Path.cwd()
out=pathlib.Path(__file__).resolve().parent
units=json.loads((out/'units.json').read_text())
paths=[out/(unit['id']+'.md') for unit in units]+[out/'REPORT.md']
pattern=re.compile(r'(?P<path>(?:src/|tests/|docs/|scripts/|plugins/|\.github/|\.claude/|\.dev/)[A-Za-z0-9_./@+\-]+|(?:pyproject\.toml|Makefile|README\.md|CLAUDE\.md|AGENTS\.md|VERSION|package\.json)):(?P<line>[0-9]+)(?:-(?P<end>[0-9]+))?')
results=[]
for report in paths:
    if not report.exists():
        continue
    text=report.read_text()
    for m in pattern.finditer(text):
        prefix=text[max(0,m.start()-45):m.start()]
        if re.search(r'[0-9a-f]{7,40}:$',prefix):
            continue
        rel=m.group('path')
        source=root/rel
        line=int(m.group('line'))
        end=int(m.group('end') or line)
        report_line=text[:m.start()].count('\n')+1
        if not source.is_file():
            status='MISSING_OR_EXPLICIT_HISTORICAL'
            total=None
        else:
            total=len(source.read_text(errors='replace').splitlines())
            status='VALID_RANGE' if 1<=line<=end<=total else 'OUT_OF_RANGE'
        results.append(dict(report=str(report.relative_to(root)),report_line=report_line,path=rel,line=line,end=end,status=status,source_lines=total))
result=dict(note='Range/existence check only; independent reviewer must verify the claim and distinguish explicit historical citations.',total=len(results),invalid_or_historical=[r for r in results if r['status']!='VALID_RANGE'],citations=results)
(out/'citation-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print('Citations checked:',len(results))
print(json.dumps(result['invalid_or_historical'],indent=2))
