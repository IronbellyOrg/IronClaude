"""Independent static audit; no imports of project code or Git mutations."""
import ast
import hashlib
import json
import os
import pathlib
import re
import subprocess

os.environ['GIT_OPTIONAL_LOCKS']='0'
root=pathlib.Path.cwd()
out=root/'.dev/research/upstream-merge-impact'
units=json.loads((out/'units.json').read_text())
endpoints={x['id']:x for x in json.loads((out/'endpoint-inventory.json').read_text())}
central={x['sha']:x for x in json.loads((out/'reverse-checks.json').read_text())}

def git(*args):
    return subprocess.check_output(['git',*args])

results={'snapshot':git('rev-parse','HEAD').decode().strip(),'units':[],'format_ast':[],'citations':[]}
for unit in units:
    if unit['id'] not in ('quality-ci','mcp-installation'):
        continue
    report=(out/(unit['id']+'.md')).read_text()
    paths=set()
    commits=[]
    for rec in unit['commits']:
        sha=rec['sha']; parent=rec['parents'][0]
        patch=git('diff','--binary','--no-ext-diff',parent,sha)
        names=git('diff','--no-renames','--name-only',parent,sha).decode().splitlines()
        paths.update(names)
        checked=subprocess.run(['git','apply','--reverse','--check','--whitespace=nowarn','-'],input=patch,capture_output=True)
        commits.append({'sha':sha,'named_in_report':sha[:8] in report,'first_parent':parent,'path_count':len(names),'reverse_rc':checked.returncode,'matches_central_rc':checked.returncode==central[sha]['returncode'],'patch_bytes':len(patch),'sha256':hashlib.sha256(patch).hexdigest()})
    results['units'].append({'id':unit['id'],'complete_path_count':len(paths),'endpoint_manifest_matches':paths==set(endpoints[unit['id']]['files']),'commits':commits,'placeholders':re.findall(r'\{\{RF_PLACEHOLDER:[^}]+\}\}',report)})
    pattern=r'(?P<path>(?:src/|tests/|docs/|scripts/|\.github/|\.dev/)[\w./@+\-]+|pyproject\.toml|CLAUDE\.md|README\.md):(?P<start>\d+)(?:-(?P<end>\d+))?'
    for match in re.finditer(pattern,report):
        path=root/match['path']; start=int(match['start']); end=int(match['end'] or start)
        lines=path.read_text(errors='replace').splitlines() if path.is_file() else []
        results['citations'].append({'report':unit['id'],'report_line':report[:match.start()].count('\n')+1,'path':match['path'],'start':start,'end':end,'valid':path.is_file() and 1<=start<=end<=len(lines),'line_count':len(lines)})
sha='b00547ad'
for file in git('diff','--name-only',sha+'^',sha).decode().splitlines():
    before=git('show',sha+'^:'+file).decode(); after=git('show',sha+':'+file).decode()
    same=ast.dump(ast.parse(before),include_attributes=False)==ast.dump(ast.parse(after),include_attributes=False)
    results['format_ast'].append({'path':file,'equal':same})
results['mcp_case_rename']=git('diff','--summary','ab0bb0f5^','ab0bb0f5','--','docs/User-Guide/mcp-installation.md','docs/user-guide/mcp-installation.md').decode()
results['mcp_merge_patch_same']=git('diff','55c658c7^','55c658c7')==git('diff','0ceb2955^1','0ceb2955')
results['empty_commit_tree_equal']=git('rev-parse','67449770^{tree}')==git('rev-parse','67449770^1^{tree}')
results['invalid_citations']=[x for x in results['citations'] if not x['valid']]
assert all(x['endpoint_manifest_matches'] for x in results['units'])
assert all(c['matches_central_rc'] and c['named_in_report'] for x in results['units'] for c in x['commits'])
assert len(results['format_ast'])==14 and all(x['equal'] for x in results['format_ast'])
assert results['mcp_merge_patch_same'] and results['empty_commit_tree_equal']
(out/'review-quality-mcp-evidence.json').write_text(json.dumps(results,indent=2)+'\n')
print('Units, endpoints:',[(x['id'],x['complete_path_count']) for x in results['units']])
print('All14 formatting ASTs equal; February patch identical; empty commit tree identical.')
print('Invalid citation ranges:',results['invalid_citations'])
print('Case rename:',results['mcp_case_rename'].strip())
