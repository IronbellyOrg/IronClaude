"""Save concise reproducible command-unit evidence without altering Git."""
import json
import os
from pathlib import Path
import subprocess
os.environ['GIT_OPTIONAL_LOCKS']='0'
out=Path('.dev/research/upstream-merge-impact/commands-framework-evidence')
unit=next(u for u in json.loads(Path('.dev/research/upstream-merge-impact/units.json').read_text()) if u['id']=='commands-framework')
checks=[c for c in json.loads(Path('.dev/research/upstream-merge-impact/reverse-checks.json').read_text()) if c['unit']=='commands-framework']
def git(*args):
    return subprocess.check_output(['git',*args],text=True)
lines=['# Commands/framework Git evidence','','## Exact historical changes','']
for c in unit['commits']:
    sha=c['sha']
    lines += [git('show','--no-patch','--format=fuller',sha).strip(),git('diff','--shortstat',c['parents'][0],sha).strip(),git('diff','--name-status',c['parents'][0],sha).strip(),'']
lines += ['## Strict reverse checks','']
for c in checks:
    lines += [c['sha']+' returncode='+str(c['returncode']),c['method'],c['stderr'].strip(), '']
lines += ['## Fork-authored later changes on command/core/agent surfaces','']
paths=['src/superclaude/commands','src/superclaude/core','src/superclaude/agents','src/superclaude/cli/install_core.py','src/superclaude/cli/install_agents.py','src/superclaude/skills/sc-recommend','src/superclaude/skills/sc-implement-protocol','src/superclaude/skills/sc-workflow-protocol']
lines += [git('log','--reverse','--format=%h %H %cI %an <%ae> %s','--author=@ironbelly.com','3762d6ab..HEAD','--',*paths).strip(),'']
lines += ['## Focused fork commit changes','']
for sha in ['de177847','de04670a','238d6583','246acd7b','b31111a9','3ae238b1','051f39fe','5c6a7d91']:
    lines += [git('show','--format=%h %H %an <%ae> %s','--stat',sha).strip(),'']
lines += ['## Plugin-build manifest source presence','',str(Path('plugins/superclaude/manifest').exists()),'This is a static source dependency analysis, not an executed plugin-build success claim.']
(out/'git-history.txt').write_text('\n'.join(lines)+'\n')
print('checks',[(c['sha'][:8],c['returncode'],len(c['stderr'].splitlines())) for c in checks])
print('history written')
