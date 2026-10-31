641d396e6a09e729b663052754cbef7d7a2cd37d
family=floor-on-stale
defect form: a codegraph step that uses stale or non-fresh graph rows instead of falling to the Phase 1 floor, or a floor trigger rewritten
command: grep -n -E -e "fresh. or .stale" -e "auggie and codegraph are both" -e "If .--no-mcp. or auggie is unavailable" -- src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md src/superclaude/commands/troubleshoot.md
before:
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:195:   - Codegraph readiness, once per run (guide section 2; skipped under `--no-mc
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:196:   - If `--no-mcp`, or auggie and codegraph are both unavailable or return noth
coupled sites: src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md tool matrix row for codegraph (Tier 2 analysts "when index_state: fresh"); Native diagnostic delegation run-state bullet; CODEGRAPH.md section 5 rule 2

after (family=floor-on-stale):
src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:196:   - If `--no-mcp` or auggie is unavailable: fall back to `Glob` + `Grep` on th
