ca31df5d6d919c809b424aaf8547cad1fb2c8fe5
family=expected-output-wording
defect form: expected result says a name is not mentioned while the same output prints it (re-register hint)
command: grep -n -e "is not mentioned" -e "not printed" -e "no line" -- docs/testing/v5.0.0/user/D01-install-upgrade-doctor.md
before:
216:**Expected result:** The list shows `serena                 will be removed (codegraph is ready)` and `codebase-memory-mcp    absent`. The install prints `Retired MCP registrations (user scope onl
coupled sites: src/superclaude/cli/install_retired_mcp.py:476-484
after:
(no hits = expected)
