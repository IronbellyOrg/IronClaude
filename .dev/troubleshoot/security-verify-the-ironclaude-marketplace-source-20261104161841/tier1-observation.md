# Tier 1 observation

Captured 2026-11-04T16:18:58Z, run=local repro, arm=failing (ironbelly/issue-330-ponytail-pin @ 50123581), command: `timeout 120 uv run python /tmp/t14c-repro2/repro.py` (two throwaway HOMEs via tempfile; subprocess.run and shutil.which replaced by a fake claude CLI that records commands; case 1 seeds known_marketplaces.json with a foreign `ironclaude` github source, case 2 makes `plugin marketplace` commands exit 1), stream=stdout:

```text
foreign ironclaude registered -> ✅ Plugins: installed ponytail@ironclaude
   ran: plugin marketplace update ironclaude
   ran: plugin install ponytail@ironclaude --scope user -y
fresh HOME, marketplace add fails -> ⚠️  Plugins: not installed: ironclaude; rerun `superclaude install` to retry
   ran: plugin marketplace add /tmp/t14c-repro2-home.ok0zz8o9/.claude/ironclaude-marketplace
   ran: plugin install ponytail@ironclaude --scope user -y
```

## Discriminator probe (security-engineer card): add when the name is taken

Captured 2026-11-04T16:27:59Z, run=throwaway HOME (removed), arm=real Claude Code 2.1.318, commands: `claude plugin marketplace add <home>/foreign` (a directory marketplace whose marketplace.json name is ironclaude, no plugins), then `claude plugin marketplace add <home>/.claude/ironclaude-marketplace`, then `claude plugin install ponytail@ironclaude --scope user -y`; stream=stdout plus known_marketplaces.json:

```text
Adding marketplace…✔ Successfully added marketplace: ironclaude (declared in user settings)
foreign add rc=0
{"source":"directory","path":"<home>/foreign"}
  Marketplace 'ironclaude' was already added from dir:<home>/foreign and now points at dir:<home>/.claude/ironclaude-marketplace.
  Plugins already installed from it now update from the new source. To undo, add the previous source again.
our add rc=0
{"source":"directory","path":"<home>/.claude/ironclaude-marketplace"}
install rc=0
```
