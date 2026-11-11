"""Read-only compatibility inventories; before also preserves a complete approved backup."""
import ast
import hashlib
import json
import os
import re
import sys
import tarfile
from pathlib import Path

root=Path('/home/coder/workspaces/worktrees/IronClaude/issue-441')
pkg=root/'.dev/tasks/to-do/TASK-WF-diagnosticCompat-20261109-141620'
out=pkg/'artifacts'
source=root/'src/superclaude/skills/sc-troubleshoot-protocol'
installed=Path('/home/coder/.claude/skills/sc-troubleshoot-protocol')
expected={'Read','Grep','Glob','mcp__litellm__augment_code-augment_code_search','mcp__auggie__codebase-retrieval','mcp__codegraph__codegraph_search','mcp__codegraph__codegraph_node','mcp__codegraph__codegraph_callers','mcp__codegraph__codegraph_impact'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(folder):
    result={}
    for p in sorted(folder.rglob('*')):
        rel=str(p.relative_to(folder))
        if p.is_symlink(): result[rel]={'symlink':os.readlink(p)}
        elif p.is_file(): result[rel]={'sha256':sha(p),'mode':p.stat().st_mode&0o7777}
    return result

def profile_tools(p):
    match=re.search(r'^tools:\s*(.+)$',p.read_text(),re.M)
    assert match,p
    return set(x.strip() for x in match[1].split(','))

assert installed.is_dir() and not installed.is_symlink()
assert not installed.parent.is_symlink()
assert source.is_dir()
profiles=[root/'src/superclaude/agents/troubleshoot-analyst.md',root/'.claude/agents/troubleshoot-analyst.md',Path('/home/coder/.claude/agents/troubleshoot-analyst.md')]
settings=[root/'.claude/settings.json',root/'.claude/settings.local.json',Path('/home/coder/.claude/settings.json'),Path('/home/coder/.claude/settings.local.json')]
protected={str(p):sha(p) if p.is_file() else None for p in profiles+settings}
other={p.name:hashlib.sha256(json.dumps(inventory(p),sort_keys=True).encode()).hexdigest() for p in sorted(installed.parent.iterdir()) if p.name!=installed.name and p.is_dir() and not p.is_symlink()}
current=inventory(installed)
canonical=inventory(source)
diff=sorted(k for k in set(current)|set(canonical) if current.get(k)!=canonical.get(k))
canonical_text=(source/'SKILL.md').read_text()
active_roster=profile_tools(profiles[1])
canonical_roster=profile_tools(profiles[0])
assert active_roster==canonical_roster==expected
roster_text='`'+', '.join(re.search(r'^tools:\s*(.+)$',profiles[0].read_text(),re.M)[1].split(', '))+'`'
assert roster_text in canonical_text
result={'canonical':canonical,'installed':current,'differing_files':diff,'installed_extras':sorted(set(current)-set(canonical)),'protected_profiles_and_settings':protected,'other_installed_skills':other,'roster':sorted(expected),'normal_refresh_only':True}
phase=sys.argv[1]
if phase=='before':
    assert diff==['SKILL.md','refs/diagnosability-audit.md','refs/doc-discovery.md'],diff
    assert not result['installed_extras']
    assert 'mcp__litellm__augment_code-augment_code_search' not in re.search(r'closed roster `([^`]+)`',(installed/'SKILL.md').read_text())[1]
    backup=out/'installed-skill-before.tar.gz'
    assert not backup.exists(),'Backup already exists; do not replace'
    with tarfile.open(backup,'w:gz') as archive:
        archive.add(installed,arcname=installed.name,recursive=True)
    with tarfile.open(backup,'r:gz') as archive:
        actual={str(Path(m.name).relative_to(installed.name)):hashlib.sha256(archive.extractfile(m).read()).hexdigest() for m in archive.getmembers() if m.isfile()}
    assert actual=={k:v['sha256'] for k,v in current.items() if 'sha256'in v}
    result['backup']={'path':'./artifacts/installed-skill-before.tar.gz','sha256':sha(backup),'all_file_bytes_match':True}
    result['protected_fingerprint']=hashlib.sha256(json.dumps(protected,sort_keys=True).encode()).hexdigest()
    (out/'compatibility-before.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'phase':phase,'differing_files':diff,'backup_file_count':len(actual),'backup_verified':True,'closed_roster_count':len(expected)}))
elif phase=='after':
    before=json.loads((out/'compatibility-before.json').read_text())
    assert not diff,diff
    assert protected==before['protected_profiles_and_settings'],'Profile/permission files changed'
    assert other==before['other_installed_skills'],'Unrelated installed skills changed'
    assert roster_text in (installed/'SKILL.md').read_text()
    result['profiles_permissions_unchanged']=True
    result['unrelated_skills_unchanged']=True
    (out/'compatibility-after.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'phase':phase,'exact_canonical_parity':True,'profiles_permissions_unchanged':True,'unrelated_skills_unchanged':True,'closed_roster_count':len(expected)}))
else: raise ValueError(phase)
