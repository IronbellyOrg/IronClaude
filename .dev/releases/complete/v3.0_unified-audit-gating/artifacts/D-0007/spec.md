---
deliverable: D-0007
phase: 2
task: T02.06
status: committed
date: 2026-03-19
---

# D-0007: ast_analyze_file() Utility

## Artifact
- `src/superclaude/cli/audit/wiring_analyzer.py`

## Function
`ast_analyze_file(file_path: str, content: str) -> FileAnalysis`

Drop-in replacement for ToolOrchestrator's default line-based analyzer.
Populates `references` field (previously always empty).

## Capabilities
- Import extraction via AST (import and from-import)
- Export detection (__all__ or public top-level defs)
- Reference collection (call targets, attribute chains)
- SyntaxError graceful handling with error metadata
- Zero pipeline/* imports (NFR-007)
