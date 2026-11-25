"""Materialize the protocol's exact closed review prompt and pin its tree."""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ARTIFACTS = Path(__file__).resolve().parent
PKG = ARTIFACTS.parent
ROOT = ARTIFACTS.parents[4]
number = int(sys.argv[1])
start = sys.argv[2]
paths = sys.argv[3:]
attempt = 1
review_index = 1
operator_review = False
while paths and paths[0].startswith('--'):
    option = paths.pop(0)
    if option.startswith('--attempt='):
        attempt = int(option.split('=', 1)[1])
    elif option.startswith('--review-index='):
        review_index = int(option.split('=', 1)[1])
    elif option == '--operator-review':
        operator_review = True
    else:
        raise ValueError(option)
plan = (PKG / (PKG.name + ".md")).read_text()
constraints = plan.split("## Constraints\n", 1)[1].split("## Phase", 1)[0].strip()
constraints += '\nCurrent-conversation instruction from the user at 2026-11-23T20:53:20Z: "go ahead and include the launcher change and finish the fix". This explicitly supersedes only the restriction excluding the detached launcher output-directory handoff in commands.py. It is not acceptance of missing behavior. The pinned plan and source remain unchanged; all original AC and other exclusions still apply.'
task = re.split(r"^## Task \d+: ", plan, flags=re.M)[number].split("## Phase", 1)[0].strip()
a, b = task.split("Acceptance criteria:\n", 1)
criteria = [line[2:] for line in b.splitlines() if line.startswith("- ")]
brief = a + "\nAcceptance criteria:\n" + "\n".join(f"T{number}.AC{i}: {line}" for i, line in enumerate(criteria, 1))
def git(*args, env=None):
    return subprocess.check_output(["git", *args], cwd=ROOT, env=env, text=True).strip()
fd, idx = tempfile.mkstemp(); os.close(fd)
try:
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    git("read-tree", "HEAD", env=env); git("add", "-A", env=env)
    tree = git("write-tree", env=env)
finally:
    os.unlink(idx)
git("update-ref", f"refs/superclaude/implement/{PKG.name}/retry/T{number}/r{attempt}-{review_index}", tree)
diff = git("diff", start, "--", *paths)
context = "\nCodegraph context\nindex_state: fresh\nchecked_at: 2026-11-23T20:14:00Z\nworktree_root: " + str(ROOT) + "\nprojectPath: " + str(ROOT) + "\ncall codegraph only when index_state: fresh, never to widen scope\nDependents outside this diff: CLI registration; resume continuation; detached child; unchanged writer and kill callers; existing TUI/input/status tests. Source call sites were Read in implementation context. These are context, not extra requirements.\n"
if number >= 4:
    context = context.split('Dependents outside this diff:', 1)[0] + 'Documentation context: Markdown is not indexed, so Q1a/Q2b use Read/Grep. Related links and current completion call sites were Read; Task 5 owns monitoring, observability and operator guidance. Context never widens the AC.\n'
ref = Path('/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md').read_text()
template = ref.split('```\nReview one task for spec compliance.\n',1)[1].split('\n```',1)[0]
template = 'Review one task for spec compliance.\n' + template
prior = ''
delta = ''
recheck = ''
if attempt > 1:
    review = (ARTIFACTS / 'retries' / ('T'+str(number)) / ('review-'+str(attempt if operator_review else attempt-1)+'.md')).read_text()
    prior = '\n'.join(line for line in review.splitlines() if line.startswith('F') and 'sev=blocking' in line)
    previous_tree = re.search(r'tree=([0-9a-f]{40})', review)[1]
    delta = git('diff', previous_tree, '--', *paths)
    if number == 3:
        recheck = 'src/superclaude/cli/swarm/commands.py:1297,1311,1718,1741,3706; src/superclaude/cli/swarm/preflight.py:1872'
    elif number == 4:
        recheck = 'docs/swarm/README.md:112-113; docs/swarm/command-reference.md:265-266'
slots = dict(task_brief=brief,global_constraints=constraints,start_sha=start,diff=diff+context,delta_diff=delta,prior_findings=prior,recheck_list=recheck)
for key, value in slots.items():
    template = template.replace('{'+key+'}',value)
folder = ARTIFACTS / 'retries' / ('T'+str(number))
folder.mkdir(parents=True,exist_ok=True)
prompt = folder / ('prompt-'+str(attempt)+'-'+str(review_index)+'.md')
with prompt.open('x') as stream:
    stream.write(start+'\n'+template+'\n')
print('PROMPT:',prompt)
print('TREE:',tree)
