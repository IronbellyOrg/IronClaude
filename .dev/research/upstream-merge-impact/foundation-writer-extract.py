"""Produce bounded source excerpts and path accounting for foundation review."""
import json
import os
import pathlib
import subprocess
from collections import Counter
os.environ['GIT_OPTIONAL_LOCKS']='0'
p=pathlib.Path(__file__).resolve().parent

def git(*args):
    return subprocess.check_output(['git',*args],text=True)

out=[]
for rev,path in [
 ('c733413d','pyproject.toml'),('c733413d^','pyproject.toml'),
 ('c733413d','src/superclaude/cli/main.py'),('c733413d','src/superclaude/pytest_plugin.py'),
 ('c733413d','src/superclaude/__init__.py'),('c733413d','plugins/superclaude/hooks/hooks.json'),
 ('c733413d','scripts/build_superclaude_plugin.py'),
 ('c733413d^','superclaude/cli/app.py'),('c733413d^','superclaude/core/pm_init/init_hook.py'),
 ('c733413d^','setup/cli/commands/install.py'),('c733413d^','setup/utils/security.py'),
 ('c733413d','DELETION_RATIONALE.md'),('c733413d','.claude/settings.json'),
]:
    text=git('show',rev+':'+path)
    out += ['\n### '+rev+':'+path]+[f'{i}: {line}' for i,line in enumerate(text.splitlines(),1)]
(p/'foundation-source-excerpts.txt').write_text('\n'.join(out)+'\n')
rows=json.loads((p/'foundation-path-coverage.json').read_text())
for sha in ('c733413d','10844490','ab0bb0f5'):
    rr=[r for r in rows if r['commit'].startswith(sha)]
    print(sha,len(rr),Counter(r['status'] for r in rr),Counter(r['class'] for r in rr))
    if sha=='ab0bb0f5':
        print('\n'.join(r['path'] for r in rr))
history=[]
commands=[
 ('Fork feature adding swarm dispatch and CLI registration', ['show','--format=%H %cI %an <%ae> %s','--stat','b0de1479','--','src/superclaude/cli/main.py','src/superclaude/cli/swarm/dispatch.py']),
 ('Fork feature adding installed core files to inherited CLI', ['show','--format=%H %cI %an <%ae> %s','--stat','de177847','--','src/superclaude/cli/main.py','src/superclaude/cli/install_core.py']),
 ('Fork feature adding required native MCP phase', ['show','--format=%H %cI %an <%ae> %s','--stat','d594babb','--','src/superclaude/cli/main.py','src/superclaude/cli/install_codebase_memory.py']),
 ('Fork cleanup strengthening pytest plugin provenance tests', ['log','--format=%H %cI %an <%ae> %s','--author=@ironbelly.com','HEAD','--','tests/integration/test_pytest_plugin.py']),
 ('All commits touching optional legacy script', ['log','--format=%H %cI %an <%ae> %s','HEAD','--','scripts/uninstall_legacy.sh']),
 ('Fork fixture isolation patch', ['show','--format=%H %cI %an <%ae> %s','--stat','d36591ee','--','src/superclaude/pm_agent/reflexion.py','src/superclaude/pytest_plugin.py','tests/conftest.py']),
 ('Legacy uninstall documentation provenance', ['blame','-L','343,367','HEAD','--','docs/getting-started/installation.md']),
 ('Later fork retirement of migration documentation and translations', ['show','--format=%H %cI %an <%ae> %s','--stat','4e5e3759','--','docs/user-guide-jp','docs/user-guide-kr','docs/user-guide-zh','docs/research','docs/architecture']),
]
for label,args in commands:
 history += ['## '+label,'git '+' '.join(args),git(*args),'']
result=subprocess.run(['git','grep','-n','-E','uninstall-legacy|uninstall_legacy','HEAD','--','.',':!.dev'],capture_output=True,text=True)
history += ['## All tracked-source search roots for legacy uninstall consumers','git grep -n -E uninstall-legacy|uninstall_legacy HEAD -- . :!.dev (all tracked paths except research/task artifacts)',result.stdout,result.stderr,'Search return code: '+str(result.returncode),'Earlier attempt to invoke rg through UV subprocess PATH failed with FileNotFoundError; recovered using git grep against tracked HEAD.']
(p/'foundation-live-dependencies.txt').write_text('\n'.join(history)+'\n')
endpoints=json.loads((p/'endpoint-inventory.json').read_text())
# The authoritative endpoint audit is read separately; reconstruct directly too.
allpaths={}
for c in next(u for u in json.loads((p/'units.json').read_text()) if u['id']=='foundation-migration')['commits']:
 for line in git('diff','--name-status','--no-renames',c['parents'][0],c['sha']).splitlines():
  status,path=line.split('\t',1)
  allpaths.setdefault(path,[]).append(c['sha'][:8]+':'+status)
assert len(allpaths)==269
coverage=['# Complete foundation changed-path endpoint ledger','','Method: git diff --no-renames --name-status FIRST_PARENT COMMIT for all three commits. A=added, M=modified, D=deleted. Classification is structural accounting; semantic inspection is limited to report citations. Every uncited historical document/primitive detail remains UNVERIFIED.','','| Path | Commit:status | Consequence class | Current path exists |','|---|---|---|---|']
for path,changes in sorted(allpaths.items()):
 rr=next((r for r in rows if r['path']==path),None)
 cls=rr['class'] if rr else 'docs-case (rename source endpoint)'
 coverage.append('| `'+path+'` | '+', '.join(changes)+' | '+cls+' | '+str(pathlib.Path(path).is_file())+' |')
coverage += ['', 'Distinct old/new endpoints: '+str(len(allpaths)),'Commit/path occurrences: '+str(sum(len(v) for v in allpaths.values()))]
(p/'foundation-complete-path-ledger.md').write_text('\n'.join(coverage)+'\n')
print('EXCERPT LINE COUNT',len(out))
print('CURRENT TRACKED COUNTS')
files=git('ls-files').splitlines()
for prefix in ('src/superclaude/cli/','tests/','src/superclaude/pm_agent/','src/superclaude/execution/'):
 print(prefix,len([f for f in files if f.startswith(prefix)]))
