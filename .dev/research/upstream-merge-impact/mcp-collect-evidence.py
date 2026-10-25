"""Materialize assigned historical patches and read-only consumer discovery."""
import json
import os
import pathlib
import subprocess

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
out = pathlib.Path(__file__).resolve().parent
folder = out / 'mcp-evidence'
folder.mkdir(exist_ok=True)
unit = next(u for u in json.loads((out/'units.json').read_text()) if u['id']=='mcp-installation')
for r in unit['commits']:
    text = subprocess.check_output(['git','show','--format=fuller','--no-ext-diff','--first-parent',r['sha']],text=True)
    (folder/(r['sha'][:8]+'.patch.txt')).write_text(text)
    if len(r['parents'])>1:
        text = subprocess.check_output(['git','diff','--no-ext-diff',r['parents'][0],r['sha']],text=True)
        (folder/(r['sha'][:8]+'.net.patch.txt')).write_text(text)
paths = []
for path in unit['files']:
    paths.append(path+' | exists='+str(pathlib.Path(path).exists()))
(folder/'path-status.txt').write_text('\n'.join(paths)+'\n')
for name, args in {
    'consumers.txt':['git','grep','-n','-I','-E','install_mcp|AIRIS_GATEWAY|MCP_Airis-Agent|MCP_Mindbase|airis-agent.json|mindbase.json','HEAD','--',':!.dev',':!plugins/superclaude',':!src/superclaude/skills'],
    'fork-history.txt':['git','log','--format=%H %cI %an %s','--','src/superclaude/cli/install_mcp.py','src/superclaude/mcp','docs/user-guide/mcp-servers.md'],
    'renames.txt':['git','log','--format=%H %cI %an %s','--name-status','--diff-filter=DR','--','setup/components/mcp.py','docs/Development/install-process-analysis.md','docs/User-Guide/mcp-installation.md','docs/reference/comprehensive-features.md','docs/capability-mapping-v5.md'],
}.items():
    r=subprocess.run(args,capture_output=True,text=True)
    assert r.returncode in (0,1),(name,r.stderr)
    (folder/name).write_text(r.stdout+r.stderr)
print('Wrote evidence for',len(unit['commits']),'records and',len(unit['files']),'paths to',folder)
