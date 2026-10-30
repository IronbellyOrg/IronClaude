f3031870786d3c3cb79b989671195aec1a8d7167
family retire-step-claim
defect form: text claiming the retire step prints a remove command for every kept entry, or that install registers servers
search: grep -n -F -e "each kept entry" -e "registers and retires" -e "every shape it cannot prove" -- docs/user-guide/mcp-installation.md CHANGELOG.md .github/workflows/test.yml
before: docs/user-guide/mcp-installation.md:9 (each kept entry); CHANGELOG.md:20 (every shape it cannot prove); .github/workflows/test.yml:133 and :155 (registers and retires)
coupled sites: docs/user-guide/mcp-installation.md:9, CHANGELOG.md:20, .github/workflows/test.yml:133,155
