4660f38db5ba6f090b7f9610c6f03aec02c8f139
family=recipe-does-not-fix
defect form: recovery recipe tells the user to run install --force for states install never repairs (user-managed entry; non-runnable user-managed command)
command: grep -n -e "user-managed" -e "install --force" -- docs/developer-guide/testing-debugging.md
before:
149:If `User registration` shows `absent`, `owned but stale` or `user-managed`, or the doctor check fails because the registered command is not an executable, run `superclaude install --force` and check again.
188:superclaude install --force
209:superclaude install --force
330:superclaude install --force
coupled sites: src/superclaude/cli/install_mcp.py:968-980; docs/user-guide/mcp-installation.md codegraph troubleshooting (not touched by this task)
after:
150:If `User registration` shows `absent` or `owned but stale`, or the doctor check fails because the registered command is not an executable while `User registration` is not `user-managed`, run `superclaude install --force` and check again.
152:`user-managed` means the `codegraph` entry was registered by you, not by IronClaude. The installer never replaces it: it keeps a working entry as it is, and it refuses an entry whose command does not run. To let IronClaude manage it, or to repair an entry whose command does not run, remove it with `claude mcp remove codegraph --scope user` and run `superclaude install` again.
191:superclaude install --force
212:superclaude install --force
333:superclaude install --force

family=output-order-claim
defect form: claims the codegraph block is the last block of install --list output
command: grep -n -i -e "last block" -e "at the end" -- docs/developer-guide/testing-debugging.md
before:
133:# The last block of the list output covers codegraph (no download, no claude mcp call)
135:# Expected, at the end:
coupled sites: src/superclaude/cli/main.py:155-168
after:
(no hits)
