#!/usr/bin/env bash
# usage: acceptance-search.sh cbm|serena|all [paths...]   (default paths: .)
set -u -o pipefail
cd "$(git rev-parse --show-toplevel)"
which=$1; shift; paths=("${@:-.}")
EX=(--no-ignore --hidden -g '!.git' -g '!.dev/**' -g '!.claude/**' -g '!.specstory/**' -g '!.venv/**')
CBM='codebase-memory|codebase_memory|CodebaseMemory|Codebase Memory|cbm|CBM_|DeusData|search_graph|trace_path|get_code_snippet|query_graph|index_repository|get_architecture|detect_changes|search_code|list_projects|\.superclaude-codebase-memory'
SER='serena|mcp__serena|\.serena|MCP_Serena|find_symbol|find_referencing_symbols|get_symbols_overview|replace_symbol_body|insert_after_symbol|insert_before_symbol|write_memory|read_memory|list_memories|edit_memory|delete_memory|rename_memory|activate_project|check_onboarding_performed|initial_instructions|\bsummarize_changes\b|get_current_config|\bfind_declaration\b|find_implementations|rename_symbol|safe_delete_symbol|think_about_|search_for_pattern|get_diagnostics_for_file|\btype_hierarchy\b|execute_shell_command|prepare_for_new_conversation|--onboard\b'
ALLOW='^(\./)?(CHANGELOG\.md|POST-REFLECT-TASK\.md|docs/memory/patterns_learned\.jsonl|docs/memory/pm_context\.md|src/superclaude/skills/ccsession-tag/install\.sh|tests/skills/test_implement_severity_replay\.py|tests/troubleshoot/fixtures/regression/sysbox-20260918/Fable-D3/REPORT\.md|src/superclaude/cli/install_retired_mcp\.py|tests/cli/test_install_retired_mcp\.py):|^(\./)?\.gitignore:[0-9]+:\.serena/$|^(\./)?src/superclaude/skills/sc-cleanup-audit-protocol/SKILL\.md:[0-9]+:.*\.serena/|^(\./)?(src/superclaude/commands/load\.md|plugins/superclaude/commands/load\.md|commands/sc-load\.md):[0-9]+:.*\.serena/memories|^(\./)?tests/cli/test_install_mcp_registry\.py:[0-9]+:\s*"(serena|codebase-memory-mcp)",'
hits=$( { [ "$which" != serena ] && rg -n -i "${EX[@]}" -e "$CBM" "${paths[@]}"; [ "$which" != cbm ] && rg -n -i "${EX[@]}" -e "$SER" "${paths[@]}"; } | rg -v -e "$ALLOW" | sort -u )
[ -z "$hits" ] && { echo "ACCEPTANCE_SEARCH_OK $which"; exit 0; }
printf '%s\n' "$hits"; echo "ACCEPTANCE_SEARCH_FAIL $which $(printf '%s\n' "$hits" | wc -l)"; exit 1
