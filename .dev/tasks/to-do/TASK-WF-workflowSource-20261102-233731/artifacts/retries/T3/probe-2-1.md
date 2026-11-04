93bbe43a75e461c1630ac612dd8e86fd66f5771b
family=retire-keep-output
defect form: text claims every kept registration is printed with its reason and a removal command
command: grep -n -E -e "removal command|reason is printed|is printed" docs/getting-started/upgrading.md docs/getting-started/installation.md README.md
before:
docs/getting-started/upgrading.md:98:   is not one of these shapes, are kept, and the reason (with a removal command)
docs/getting-started/upgrading.md:99:   is printed. Each `claude` call has 10 seconds and the
docs/getting-started/installation.md:385:  wrote, and prints the reason (and a removal command) for any entry it keeps.
coupled sites: install_retired_mcp.py:420-425 (kept output), :91-95 TIER_K_LINE (only kept line with a command), :274-283 (other names never classified); upgrading.md "Serena" section removal commands
after:
docs/getting-started/installation.md:388:  removal commands.
