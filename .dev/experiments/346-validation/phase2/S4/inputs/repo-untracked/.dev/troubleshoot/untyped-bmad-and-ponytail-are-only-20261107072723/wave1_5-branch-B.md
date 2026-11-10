# Wave 1.5 Branch B: architectural-doc lookup (returned by troubleshoot-analyst; persisted by parent, summaries condensed by parent, quotes verbatim)

All currency verdicts are preliminary `unknown` (worker cannot run stat). Parent finalization below.

```json
[
  {"doc_path": "templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml",
   "summary": "welcome_message: \"If this workspace has a seed repo, BMad is already set up there (hidden from git via the repo's info/exclude). For any other repo, run from its root: bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output\". scope: hybrid; install_disposition: image-baked; class: installed-only. CLI is image-baked; per-project setup only for the seed repo.",
   "currency_verdict": "unknown", "reason": "no markers found (YAML manifest)"},
  {"doc_path": "templates/VSCode-AIDev02/image/catalogue/bmad/install.sh",
   "summary": "Header: \"runs a per-repo `bmad install` into the seed repo (hidden via info/exclude)\". Reads ~/.aidev/status/seed-repo-path (\"AD-7: written only by startup §8\"). No seed repo -> \"no seed repo recorded; nothing to configure\". Existing _bmad/ or tracked bmad skills left alone. Nothing creates BMAD directories in any other project.",
   "currency_verdict": "unknown", "reason": "no markers found (shell script)"},
  {"doc_path": "templates/VSCode-AIDev02/image/catalogue/ironclaude/manifest.yaml",
   "summary": "IronClaude is user-global: \"Its commands, agents, skills and hooks live in ~/.claude, so every new Claude Code session has them.\" scope hybrid, image-baked. No mention of Ponytail or BMAD.",
   "currency_verdict": "unknown", "reason": "no markers found (YAML manifest)"},
  {"doc_path": "templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh",
   "summary": "Runs `superclaude install` into ~/.claude once per provenance git_sha; touches ~/.claude/CLAUDE.md, settings.json, commands/sc/help.md. Only 'ponytail' hit is a code comment. Plugin enablement is not in this script.",
   "currency_verdict": "unknown", "reason": "no markers found (shell script)"},
  {"doc_path": "docs/operations/upstream-monitor.md",
   "summary": "Only documentation hit for Ponytail the plugin (line 62): Renovate on IronbellyOrg/IronClaude watches \"Claude Code plugins IronClaude pins in its own marketplace (Ponytail: release tag and commit, rewritten together)\" in src/superclaude/cli/user_settings_defaults.json. Does not say how it is activated per workspace/project. Also lists bmad-method under Renovate.",
   "currency_verdict": "unknown", "reason": "no markers found"},
  {"doc_path": "docs/operations/aidev02-operator.md",
   "summary": "Describes user-global IronClaude state (seed /etc/skel/.claude/CLAUDE.md copied to ~/.claude/CLAUDE.md; mcp-bundle-core registers litellm at user scope). Line 1977 names \"IronClaude, BMad, MCP\" as v2 catalogue slugs. No section on BMAD/Ponytail per-project scoping; none on Ponytail.",
   "currency_verdict": "unknown", "reason": "no markers found"},
  {"doc_path": "templates/VSCode-AIDev02/README.md",
   "summary": "Line 241: Tooling profile Default (Orca, IronClaude, BMad, core MCP servers; pre-selected) or Minimal (Claude Code only). Line 239: seed repo optional. Silent on BMAD seed-repo-only setup, on Ponytail, and on running bmad install elsewhere. Still uses stale AIDev01 path /config/workspace/.",
   "currency_verdict": "unknown", "reason": "no markers found (YAML front matter display_name)"},
  {"doc_path": "templates/VSCode-AIDev02/image/catalogue/README.md",
   "summary": "Lines 24-28: orca profile (Default, pre-selected) selects Claude Code, Orca, IronClaude, BMad, mcp-bundle-core; only other profile is minimal. §9 installs slugs; contract is manifest.yaml, install.sh, module.tf. No BMAD per-project scoping or Ponytail.",
   "currency_verdict": "unknown", "reason": "no markers found"},
  {"doc_path": "templates/VSCode-AIDev02/image/catalogue/profiles.yaml",
   "summary": "Source of truth: default_profile orca = [claude-code, orca, ironclaude, bmad, mcp-bundle-core]; minimal = [claude-code]. Ponytail is not a slug.",
   "currency_verdict": "unknown", "reason": "no markers (YAML comment header)"},
  {"doc_path": "docs/diagrams/startup-sections.md",
   "summary": "Boot order §1-§12: §8 seed-repo-clone, §9 catalogue-installs (subshell per slug, workspace/hybrid only). Shows BMAD path §8 -> §9 into seed repo. No mention of BMAD/Ponytail by name or user-global scope.",
   "currency_verdict": "unknown", "reason": "no markers found"},
  {"doc_path": "docs/architecture.md", "summary": "Lists slugs and says agent CLI is IronClaude SHA-pinned. Nothing on user-global versus per-project scoping or Ponytail.", "currency_verdict": "unknown", "reason": "no markers found"},
  {"doc_path": "docs/component-inventory.md", "summary": "Slug table: ironclaude, bmad image-baked; orca (profile orca). No scope info; nothing on Ponytail.", "currency_verdict": "unknown", "reason": "no markers found"},
  {"doc_path": "docs/generated/PROJECT_INDEX.md", "summary": "Session-start map; no BMAD or Ponytail content.", "currency_verdict": "unknown", "reason": "Generated/Last Updated 2026-09-25 (not the strict marker form)"}
]
```

Worker finding relayed: no document describes a contract where BMAD works in a never-set-up project. Automatic BMAD setup happens only in the seed repo; any other repo is manual. No document says how Ponytail is installed/activated; only docs/operations/upstream-monitor.md:62 (plugin pinned in IronClaude's user_settings_defaults.json). Gaps: Ponytail install mechanism undocumented in this repo; stale /config/workspace/ paths in templates/VSCode-AIDev02/README.md.

Harness note: the subagent output tripped an instruction-shaped pattern filter (settings-json) because it names user_settings_defaults.json; it contained no directive to the parent. No instruction followed.

## Parent currency finalization (Section 2)
Mtime metadata not collected for these docs; all verdicts remain `unknown` (CAUTION: advisory, not authoritative). The code-bearing entries (manifest.yaml, install.sh, profiles.yaml) were read directly by the parent in Wave 1 (see tier1-observation.md) and are treated as code evidence, not as documentation.
