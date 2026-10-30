# MCP Integration Policy

Integration policy and usage guidelines for MCP (Model Context Protocol) servers in SuperClaude Framework.

## MCP Server Definitions

### Core MCP Servers

#### Memory & Error Learning

**ReflexionPattern (Built into the Python package, explicit API)**

> The earlier "ReflexionMemory" entry here (automatic use by the PM Agent, `superclaude/core/pm_init/reflexion_memory.py`, `docs/memory/reflexion.jsonl`, 50% overlap) is **superseded** and no longer describes the implementation. See [docs/user-guide/memory-system.md](../user-guide/memory-system.md) for the full contract.

```yaml
Name: ReflexionPattern
Purpose: Error record storage and lookup
Category: Memory Management (built-in Python class, not an MCP server)
Auto-Managed: false (called explicitly; the only automatic use is the opt-in pytest recorder)
PM Agent Role: None (the PM agent definition does not call it)

Capabilities:
  - record_error(): append a caller-supplied error dictionary to solutions_learned.jsonl
  - get_solution(): return the first stored row whose signature overlaps at 0.7 or higher
  - get_statistics(): count rows and rows that have a solution

Implementation:
  Location: src/superclaude/pm_agent/reflexion.py
  Storage: <memory_dir>/solutions_learned.jsonl (default docs/memory/); mistake notes in the sibling mistakes/ directory
  Directory: memory_dir argument > non-empty REFLEXION_OUTPUT_DIR > docs/memory/ under the current directory
  Search: lowercase word-set overlap on error_type + error_message + test_name; 0.7 inclusive; first match in file order

Note: Internal Python class, not an external MCP server. It does not redact secrets;
      callers must redact before recording.
```

**Mindbase MCP (Optional Enhancement via airis-mcp-gateway)**

```yaml
Name: mindbase
Purpose: Semantic search across all conversation history
Category: Memory Management (Optional MCP)
Auto-Managed: false (external MCP server - requires installation)
PM Agent Role: None defined in this repository
Status: Optional external service you install and configure yourself. This repository does
        not install, configure or test it, and its availability is UNVERIFIED. The Python
        class above has a MindBase hook (_search_mindbase) that is an unimplemented stub
        and always returns None.

Capabilities:
  - Persistence of all conversation history (PostgreSQL + pgvector)
  - Semantic search (qwen3-embedding:8b)
  - Cross-project knowledge sharing
  - Learning from all past conversations

Tools:
  - mindbase_search: Semantic search
  - mindbase_store: Conversation storage
  - mindbase_health: Health check

Installation:
  Requires: airis-mcp-gateway with "recommended" profile
  See: https://github.com/agiletec-inc/airis-mcp-gateway

Profile Dependency (as described by the external gateway project; not verified here):
  - "recommended" profile: mindbase included (long-term projects)
  - "minimal" profile: mindbase NOT included (lightweight, quick tasks)

Usage Pattern:
  - If you install it, you call its tools explicitly, or Claude may choose them
  - There is no automatic fallback between it and ReflexionPattern, and no code in this
    repository connects the two

Note: Optional. SuperClaude does not need it; ReflexionPattern works with only the local file.
```

#### Native reasoning

Multi-step analysis uses native model reasoning.

#### Context7 MCP

```yaml
Name: context7
Purpose: 公式ドキュメントとライブラリパターン参照
Category: Documentation Reference
Auto-Managed: false (明示的使用)
PM Agent Role: Pre-Implementation Confidence Check

Capabilities:
  - 公式ドキュメント検索
  - ライブラリベストプラクティス
  - API仕様確認
  - フレームワークパターン

Lifecycle:
  Start: 何もしない
  During: ドキュメント参照時に使用
  End: 情報を返す
  Cleanup: 自動

Usage Pattern:
  Use Cases:
    - ライブラリの使い方確認
    - ベストプラクティス参照
    - API仕様確認
    - 公式パターン学習

  NOT for:
    - プロジェクト固有ドキュメント（docs/使用）
    - 社内ドキュメント
    - カスタム実装パターン

Trigger Conditions:
  - Pre-Implementation: Confidence check時
  - Keywords: "official docs", "best practices", "how to use [library]"
  - New Library: 初めて使うライブラリ

Example:
  Task: "Implement JWT authentication with jose library"
  → Context7: Fetch jose official docs and patterns
  → PM Agent: Verify implementation against official patterns
```

#### Tavily MCP

```yaml
Name: tavily
Purpose: Web検索とリアルタイム情報取得
Category: Research
Auto-Managed: false (明示的使用)
PM Agent Role: Research modeで情報収集

Capabilities:
  - Web検索
  - 最新情報取得
  - 技術記事検索
  - エラーメッセージ検索

Lifecycle:
  Start: 何もしない
  During: 研究・調査時に使用
  End: 検索結果を返す
  Cleanup: 自動

Usage Pattern:
  Use Cases:
    - 最新のライブラリバージョン確認
    - エラーメッセージの解決策検索
    - 技術トレンド調査
    - 公式ドキュメント検索（Context7にない場合）

  NOT for:
    - プロジェクト内情報（Grep使用）
    - コードベース検索（Grep / Read使用）
    - 過去の会話（Mindbase: 任意・手動で導入した場合のみ）

Trigger Conditions:
  - Keywords: "search", "latest", "current"
  - Error: Unknown error message
  - Research: New technology investigation

Example:
  Task: "Find latest Next.js 15 App Router patterns"
  → Tavily: Search web for latest patterns
  → PM Agent: Document findings in docs/patterns/
```

## MCP Selection Matrix

### By Task Type

```yaml
Code Understanding:
  Primary: Grep + Read
  Secondary: Auggie MCP (optional, broader retrieval)
  Example: "Find all authentication-related symbols"

Complex Analysis:
  Native reasoning (simple cases)
  Example: "Design authentication architecture"

Documentation Reference:
  Primary: Context7 MCP
  Secondary: Tavily (if not in Context7)
  Example: "How to use React Server Components"

Research & Investigation:
  Primary: Tavily MCP
  Secondary: Context7 (official docs)
  Example: "Latest security best practices 2025"

Memory & History:
  Primary: None by default; call ReflexionPattern explicitly for error records
  Secondary: Mindbase MCP (optional, manually installed; availability unverified)
  Example: Record a failing test's cause and fix with ReflexionPattern.record_error()

Task Management:
  Primary: TodoWrite (built-in)
  Secondary: None
  Example: Track multi-step implementation
```

### By Complexity Level

```yaml
Simple (1-2 files, clear path):
  MCPs: None (native tools sufficient)
  Tools: Read, Edit, Grep, Bash

Medium (3-10 files, some complexity):
  MCPs: Context7 (if new library)
  Tools: MultiEdit, Glob, Grep

Complex (>10 files, architectural changes):
  MCPs: Auggie (optional)
  Coordination: PM Agent Commander mode
  Tools: Task delegation, parallel execution

Research (information gathering):
  MCPs: Tavily + Context7
  Mode: DeepResearch mode
  Tools: WebFetch (selective)
```

## PM Agent Integration Rules

### Session Lifecycle

```yaml
Session Start:
  Auto-Execute:
    1. git status && git branch
    2. Read CLAUDE.md
    3. Read docs/patterns/*.md (latest 5)
    4. (Superseded: "Mindbase auto-load". No automatic memory load is implemented for
       solutions_learned.jsonl or Mindbase. The PM agent definition restores context
       by reading the .superclaude/memory/ markdown files instead.)

  MCPs Used:
    - Mindbase: not used by default
    - Others: None (wait for task)

  Output: 📍 [branch] | [status] | 🧠 [token]%

Pre-Implementation:
  Auto-Execute:
    1. Read relevant docs/patterns/
    2. Read relevant docs/mistakes/
    3. Confidence check

  MCPs Used:
    - Context7: If new library (automatic)

  Decision:
    High Confidence (>90%): Proceed
    Medium (70-89%): Present options
    Low (<70%): Stop, request clarification

During Implementation:
  Manual Trigger:
    - TodoWrite: Progress tracking
    - Grep + Read: Code understanding (if needed)

  MCPs Used:
    - Context7: On documentation need

Post-Implementation:
  Auto-Execute:
    1. Self-evaluation (Four Questions)
    2. Pattern extraction
    3. Documentation update

  MCPs Used:
    - Mindbase: not used by default (the former "automatic save" is superseded)
    - Error records: call ReflexionPattern.record_error() explicitly if you want one stored
    - Others: None (file-based documentation)

  Output:
    - Success → docs/patterns/
    - Failure → docs/mistakes/
    - Global → CLAUDE.md
```

### MCP Activation Triggers

```yaml
Native reasoning:
  Manual Override: native reasoning

Context7 MCP:
  Auto-Trigger Keywords:
    - "official docs"
    - "best practices"
    - "how to use [library]"
    - New library detected

  Auto-Trigger Conditions:
    - Pre-Implementation confidence check
    - New library in package.json
    - Framework pattern needed

  Manual Override: --c7 flag

Tavily MCP:
  Auto-Trigger Keywords:
    - "search"
    - "latest"
    - "current trends"
    - "find error solution"

  Auto-Trigger Conditions:
    - Research mode active
    - Unknown error message
    - Latest version check

  Manual Override: --tavily flag
```

## Anti-Patterns (禁止事項)

### DO NOT

```yaml
❌ Context7をプロジェクトドキュメントに使用:
  Reason: 公式ドキュメント専用
  Instead: Read docs/ 使用
```

**Superseded prohibitions (historical, NOT current policy).** An earlier version of this
list banned three things. They no longer apply:

```yaml
Former: "Do not operate Mindbase explicitly" (it was described as fully automatic)
  Now: Mindbase is not automatic here. If you installed it, using its tools explicitly is fine.

Former: "Do not read or write memory explicitly"
  Now: Explicit memory use is supported. The PM agent definition itself reads and writes
       the .superclaude/memory/ markdown files (src/superclaude/agents/pm-agent.md), and
       ReflexionPattern is an explicit API.

Former: "Do not create the docs/memory/ directory (duplicates Mindbase)"
  Now: docs/memory/ is the default storage of ReflexionPattern and holds tracked records.
       Do not delete it, and do not move its records to docs/patterns/ or docs/mistakes/.
```

## Best Practices

### Efficient MCP Usage

```yaml
✅ Right Tool for Right Job:
  Simple → Native tools (Read, Edit, Grep)
  Medium → Context7 (new library)
  Complex → Grep + Read, Auggie (optional)

✅ Lazy Evaluation:
  Don't preload MCPs
  Activate only when needed
  Let PM Agent auto-trigger

✅ Clear Separation:
  Memory: ReflexionPattern (explicit API) or optional Mindbase (manual install)
  Knowledge: docs/ (file-based)
  Progress: TodoWrite (session)
  Code: Grep + Read (understanding)

✅ Documentation First:
  Pre-Implementation: Context7 + docs/patterns/
  During: TodoWrite tracking
  Post: docs/patterns/ or docs/mistakes/
```

## Testing & Validation

### MCP Integration Tests

```yaml
Test Cases:

1. (Superseded) "Mindbase Auto-Load":
   - The former case checked automatic loading of past context. That behavior is not
     implemented, so the case has been removed.
   - Error-record behavior is described in docs/user-guide/memory-system.md.

2. Context7 Documentation:
   - Task: "Implement with new library"
   - Verify Context7 auto-triggered
   - Verify official docs referenced

3. Tavily Research:
   - Task: "Find latest security patterns"
   - Verify Tavily auto-triggered
   - Verify web search executed
```

## Migration Checklist

This checklist is historical. Its first two items are **superseded and must not be
followed**: docs/memory/ is live storage and explicit memory calls are supported.

```yaml
From Old System:
  - [ ] (superseded) Remove docs/memory/ references
  - [ ] (superseded) Remove explicit memory read/write calls
  - [ ] Remove MODE_Task_Management.md memory sections
  - [ ] Update pm-agent.md with new MCP policy

To New System:
  - [ ] Add MCP integration policy docs
  - [ ] Update pm-agent.md triggers
  - [ ] Add auto-activation logic
  - [ ] Test MCP selection matrix
  - [ ] Validate anti-patterns enforcement
```

## References

- PM Agent: `~/.claude/superclaude/agents/pm-agent.md`
- Modes: `~/.claude/superclaude/modes/MODE_*.md`
- Rules: `~/.claude/superclaude/framework/rules.md`
- Memory Cleanup: `docs/architecture/pm-agent-responsibility-cleanup.md` (historical; this document no longer exists in the repository)
- Error-record contract: [docs/user-guide/memory-system.md](../user-guide/memory-system.md)
