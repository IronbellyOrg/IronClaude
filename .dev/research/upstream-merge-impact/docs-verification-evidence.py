"""Capture bounded read-only corroboration for documentation conclusions."""
from pathlib import Path
import os
import subprocess

os.environ['GIT_OPTIONAL_LOCKS']='0'
out=Path(__file__).resolve().parent
commands=[
 ['git','diff-tree','--no-commit-id','--name-status','-r','4e5e3759','--','README-ja.md','README-kr.md','README-zh.md','PLANNING.md','KNOWLEDGE.md','CHANGELOG.md','README.md','VERSION'],
 ['git','diff-tree','--no-commit-id','--name-status','-r','d36591ee','--','docs/mistakes/test_database_connection-2025-11-14.md','docs/mistakes/test_reflexion_with_real_exception-2025-11-14.md','docs/mistakes/unknown-2025-11-14.md'],
 ['git','show','--format=short','--unified=0','5d660ca9','--','src/superclaude/__init__.py','pyproject.toml'],
 ['git','show','--format=short','--name-status','fe24f9c5','--','docs/research/llm-agent-token-efficiency-2025.md','docs/research/reflexion-integration-2025.md','docs/research/task-tool-parallel-execution-results.md'],
 ['git','show','--format=short','--name-status','3ae238b1','--','plugins/superclaude/commands/sc.md'],
 ['rg','-n','ReflexionMemory|class Reflexion|reflexion_memory\\.py|error_search_tool|reflexion\\.jsonl\\.example|mindbase_used','src','scripts','tests','--glob','!*.lock'],
 ['rg','-n','memory-system|WORKFLOW_METRICS_SCHEMA|docs/user-guide/commands|mcp-integration-policy|reflexion\\.jsonl\\.example','src','plugins','scripts','tests','docs','--glob','!*.lock'],
 ['rg','-n','Smithery|smithery','README.md','src','tests','scripts','.github'],
 ['rg','-n','docs/memory|mindbase|reflexion','src/superclaude/agents/pm-agent.md','src/superclaude/commands/pm.md','src/superclaude/skills/sc-pm-protocol/SKILL.md'],
]
lines=['Documentation unit: independent source/Git checks. Exit 1 for git grep means no match, not execution failure.','Initial helper attempt could not find an rg executable in subprocess PATH. Recovered with git grep over tracked source. Earlier interactive-shell rg searches also completed; one broader search reported missing retired bin/ directory.','']
for i,cmd in enumerate(commands,1):
    if cmd[0] == 'rg':
        args=cmd[2:]
        if '--glob' in args:
            args=args[:args.index('--glob')]
        cmd=['git','grep','-n','-E',args[0],'--',*args[1:]]
    r=subprocess.run(cmd,text=True,capture_output=True)
    assert r.returncode in (0,1),(cmd,r.stderr)
    lines += [f'===== CHECK {i} =====','Command: '+repr(cmd),'Exit: '+str(r.returncode),r.stdout.rstrip(),r.stderr.rstrip(),'']
for p in ('src/superclaude/core/pm_init/reflexion_memory.py','superclaude/core/pm_init/reflexion_memory.py','bin','plugins/superclaude/manifest/metadata.json'):
    lines.append(f'Filesystem presence: {p} = {Path(p).exists()}')
(out/'docs-verification-evidence.txt').write_text('\n'.join(lines)+'\n')
print('Saved',len(lines),'evidence blocks/lines')
