"""Check existence and bounds of named citations in two assigned research files."""
import json
import pathlib
import re

root=pathlib.Path.cwd()
out=pathlib.Path(__file__).resolve().parent
pattern=re.compile(r'(?P<path>[A-Za-z0-9_./-]+\.(?:md|py|txt|json|toml|yml|jsonl|sh|patch)|Makefile|VERSION):(?P<ranges>[0-9]+(?:-[0-9]+)?(?:,[0-9]+(?:-[0-9]+)?)*)')
records=[]
for name in ('foundation-migration.md','docs-memory-releases.md'):
    text=(out/name).read_text()
    for match in pattern.finditer(text):
        prefix=text[max(0,match.start()-45):match.start()]
        if re.search(r'[0-9a-f]{7,40}:$',prefix):
            continue
        path=pathlib.Path(match.group('path'))
        if str(path).startswith('.dev/') or '/' in str(path) or str(path) in ('Makefile','VERSION','pyproject.toml','package.json','README.md','CHANGELOG.md','KNOWLEDGE.md','CLAUDE.md'):
            path=root/path
        else:
            path=out/path
        spans=[]
        for fragment in match.group('ranges').split(','):
            values=[int(x) for x in fragment.split('-')]
            spans.append((values[0],values[-1]))
        lines=path.read_text(errors='replace').splitlines() if path.is_file() else []
        valid=path.is_file() and all(1<=a<=b<=len(lines) for a,b in spans)
        records.append(dict(report=name,report_line=text[:match.start()].count('\n')+1,citation=match.group(),resolved_path=str(path.relative_to(root)),source_lines=len(lines),valid=valid))
result=dict(total=len(records),invalid=[x for x in records if not x['valid']],records=records)
(out/'review-foundation-docs-citations.json').write_text(json.dumps(result,indent=2)+'\n')
print('Named citations checked:',len(records))
print(json.dumps(result['invalid'],indent=2))
