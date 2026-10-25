"""Independent, non-mutating checks for two research units."""
import json
import os
import pathlib
import re
import subprocess

os.environ['GIT_OPTIONAL_LOCKS']='0'
root=pathlib.Path.cwd()
out=root/'.dev/research/upstream-merge-impact'
units=json.loads((out/'units.json').read_text())
endpoints=json.loads((out/'endpoint-inventory.json').read_text())
central={r['sha']:r for r in json.loads((out/'reverse-checks.json').read_text())}

def git(*args):
    return subprocess.check_output(['git',*args],text=True)

selected=[u for u in units if u['id'] in ('installer-packaging','automated-sync-copies')]
records=[]
for u in selected:
    text=(out/(u['id']+'.md')).read_text()
    paths=set()
    rows=[]
    for c in u['commits']:
        sha=c['sha']
        parent=c['parents'][0]
        names=git('diff','--no-renames','--name-only',parent,sha).splitlines()
        paths.update(names)
        patch=subprocess.check_output(['git','diff','--binary','--no-ext-diff',parent,sha])
        check=subprocess.run(['git','apply','--reverse','--check','--whitespace=nowarn','-'],input=patch,capture_output=True)
        assert check.returncode==central[sha]['returncode'],sha
        assert sha[:8] in text,sha
        rows.append(dict(sha=sha,parent=parent,paths=names,stat=git('diff','--stat',parent,sha),reverse_code=check.returncode,reverse_stderr=check.stderr.decode(),central_matches=True))
    ep=next(x for x in endpoints if x['id']==u['id'])
    assert paths==set(ep['files'])
    assert len(paths)==u['file_count']
    missing_in_report=[p for p in sorted(paths) if p not in text]
    assert not missing_in_report,missing_in_report
    records.append(dict(unit=u['id'],commits=len(rows),paths=len(paths),report_missing_paths=missing_in_report,placeholder='{{RF_PLACEHOLDER:' in text,results=rows))

pat=re.compile(r'(?P<path>[A-Za-z0-9_./@+\-]+\.[A-Za-z0-9]+|Makefile|VERSION):(?P<line>[0-9]+)(?:-(?P<end>[0-9]+))?')
citations=[]
for u in selected:
    report=out/(u['id']+'.md')
    text=report.read_text()
    for m in pat.finditer(text):
        source=root/m.group('path')
        if not source.is_file() and (out/m.group('path')).is_file():
            source=out/m.group('path')
        count=len(source.read_text(errors='replace').splitlines()) if source.is_file() else None
        line=int(m.group('line'))
        end=int(m.group('end') or line)
        citations.append(dict(report=u['id'],report_line=text[:m.start()].count('\n')+1,path=m.group('path'),start=line,end=end,source_lines=count,valid=count is not None and 1<=line<=end<=count))

nonblank=git('diff','--ignore-all-space','--ignore-blank-lines','--numstat','ff5f73ad^','ff5f73ad')
result=dict(head=git('rev-parse','HEAD').strip(),tracked_diff=git('diff','--name-only','HEAD'),units=records,citations=citations,invalid_citations=[c for c in citations if not c['valid']],july_nonblank_diff=nonblank,manifest_paths=git('ls-files','.claude-plugin/*','*marketplace*','plugin.json','plugins/superclaude/manifest/*').splitlines(),pending_in_head=subprocess.run(['git','merge-base','--is-ancestor','d3cf5938','HEAD']).returncode,pending_in_master=subprocess.run(['git','merge-base','--is-ancestor','d3cf5938','origin/master']).returncode)
(out/'review-packaging-sync-evidence.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(head=result['head'],tracked_diff=result['tracked_diff'],unit_counts=[{k:r[k] for k in ('unit','commits','paths','report_missing_paths','placeholder')} for r in records],citation_count=len(citations),invalid_citations=result['invalid_citations'],july_nonblank_diff=nonblank,manifest_paths=result['manifest_paths'],pending_in_head=result['pending_in_head'],pending_in_master=result['pending_in_master']),indent=2))
