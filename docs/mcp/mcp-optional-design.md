# MCP Optional Design

## 基本原則: 実行時のMCP利用はオプション

**重要**: 実行時は **MCPなしでも基本機能を利用** できます。これはインストールの成功条件とは別です。

### Installation vs Optional Runtime Use

`superclaude install` installs the framework files and then installs and registers codegraph at user scope (`claude mcp add-json codegraph ... --scope user`). codegraph is a required install phase: if it fails, the framework files stay installed and `superclaude install` exits 1. Every other MCP server is optional and is added separately with `superclaude mcp`. If an MCP server is unavailable at runtime, the native-tool fallbacks below apply. See the [MCP installation guide](../user-guide/mcp-installation.md) for the commands.

The examples below describe **runtime fallback behavior**, not permission to suppress installation errors.

```yaml
Core Principle:
  MCPs: Optional enhancements (性能向上のオプション)
  Native Tools: Always available (常に利用可能)
  Fallback: Automatic (自動フォールバック)

Design Philosophy:
  "MCP usage enhances runtime; default provisioning is a separate install requirement"
  "Native tools are the foundation"
  "Graceful degradation always"
```

## Fallback Strategy

### MCP vs Native Tools

```yaml
Code Understanding:
  With MCP:
    - codegraph (構造: シンボル、呼び出し元、影響範囲; installed by default)
    - Auggie (セマンティック検索)
  Without MCP: Grep + Glob + Read (常に利用可能な下限)
  Degradation: 機能維持、速度低下のみ

Complex Analysis:
  Without MCP: Native reasoning (同等品質、トークン増)
  Degradation: トークン使用量増加のみ

Documentation:
  With MCP: Context7 (公式ドキュメント、キュレーション済み)
  Without MCP: WebFetch + WebSearch (生データ、手動フィルタ)
  Degradation: 情報の質が若干低下

Research:
  With MCP: Tavily (最適化検索、構造化結果)
  Without MCP: WebSearch (標準検索)
  Degradation: 検索効率が若干低下

Memory:
  Store: plain markdown files under <project>/.superclaude/memory/ (no MCP needed)
  Cross-session: PM Agent reads them at session start and writes them during work
  Degradation: なし (MCPに依存しない)
```

## PM Agent Without MCPs

### Fully Functional Without Any MCP

```yaml
Session Start:
  With MCPs:
    - Git status ✅
    - Read CLAUDE.md ✅
    - Read docs/patterns/ ✅
    - Read .superclaude/memory/ ✅

  Without MCPs:
    - Git status ✅
    - Read CLAUDE.md ✅
    - Read docs/patterns/ ✅
    - Read .superclaude/memory/ ✅

Result: 完全動作（記憶はファイルなのでMCP不要）

Pre-Implementation:
  With MCPs:
    - Read docs/patterns/ ✅
    - Read docs/mistakes/ ✅
    - Context7 official docs ⚡ (optional)
    - Confidence check ✅

  Without MCPs:
    - Read docs/patterns/ ✅
    - Read docs/mistakes/ ✅
    - WebSearch official docs ✅
    - Confidence check ✅

Result: 完全動作（ドキュメント取得が若干遅い）

During Implementation:
  With MCPs:
    - TodoWrite ✅
    - codegraph structure lookups ⚡ (installed by default)
    - Auggie code understanding ⚡ (optional)

  Without MCPs:
    - TodoWrite ✅
    - Grep + Read code search ✅
    - Native reasoning ✅

Result: 完全動作（大規模コードベースで遅い）

Post-Implementation:
  With MCPs:
    - Self-evaluation ✅
    - docs/patterns/ update ✅
    - docs/mistakes/ update ✅
    - Write .superclaude/memory/ ✅

  Without MCPs:
    - Self-evaluation ✅
    - docs/patterns/ update ✅
    - docs/mistakes/ update ✅
    - Write .superclaude/memory/ ✅

Result: 完全動作（クロスセッション学習もファイルで継続）
```

## Detection & Auto-Fallback

### MCP Availability Detection

```yaml
Runtime Detection:
  Method: Try MCP, catch error, fallback

  Example:
    try:
      auggie.codebase_retrieval("authenticate")
    except MCPNotAvailable:
      fallback_to_grep("authenticate")

  User Impact: None (transparent)
  Performance: Slightly slower on first detection

Startup Check:
  Method: List available MCP servers

  Available MCPs: [codegraph, auggie]
  Missing MCPs: [context7, tavily]

  → Auto-configure fallbacks
  → Log available MCPs
  → Proceed normally
```

### Automatic Fallback Logic

```yaml
Auggie MCP Unavailable:
  Task: "Refactor auth across 15 files"

  Attempt:
    1. Try Auggie codebase retrieval
    2. MCPNotAvailable error
    3. Fallback to Grep + Read

  Execution:
    grep -r "authenticate\|auth\|login" .
    Read all matched files
    Manual symbol tracking (slower but works)

  Output: Same result, slower execution

Context7 MCP Unavailable:
  Task: "How to use React Server Components"

  Attempt:
    1. Try Context7 official docs
    2. MCPNotAvailable error
    3. Fallback to WebSearch

  Execution:
    WebSearch "React Server Components official docs"
    WebFetch relevant URLs
    Manual filtering

  Output: Same info, less curated

codegraph MCP Unavailable:
  Task: "Who calls authenticate()?"

  Attempt:
    1. Try codegraph callers lookup
    2. MCPNotAvailable error (or index not ready)
    3. Fallback to Grep + Glob + Read

  Output: Same answer, slower; graph answers are leads, not citations

Cross-Session Memory:
  Impact: None from MCP availability

  Store:
    - Plain markdown files under <project>/.superclaude/memory/
    - Read at session start, written during work (PM Agent)
```

## Configuration

### MCP Enable/Disable

```yaml
# Illustrative design sketch only: no SuperClaude code reads this file
# or these keys. Register or remove servers with `superclaude mcp` and
# `claude mcp`.
User Configuration:
  Location: ~/.claude/mcp-config.json (illustrative)

  {
    "mcps": {
      "codegraph": "auto",     // enabled if available
      "auggie": "auto",        // enabled if available
      "context7": "disabled",  // explicitly disabled
      "tavily": "enabled"      // explicitly enabled
    },
    "fallback_mode": "graceful"  // graceful | aggressive | disabled
  }

Fallback Modes:
  graceful: Try MCP, fallback silently (default)
  aggressive: Prefer native tools, use MCP only when significantly better
  disabled: Never fallback, error if MCP unavailable
```

### Performance Comparison

```yaml
Task: Refactor 15 files

With Auggie MCP:
  Time: 30 seconds
  Tokens: 5,000
  Accuracy: 95%

Without Auggie (Grep fallback):
  Time: 90 seconds
  Tokens: 5,000
  Accuracy: 95%

Difference: 3x slower, same quality

---

Task: Fetch official docs

With Context7 MCP:
  Time: 10 seconds
  Relevance: 95%
  Curated: Yes

Without Context7 (WebSearch):
  Time: 30 seconds
  Relevance: 80%
  Curated: No

Difference: 3x slower, less relevant
```

## Testing Without MCPs

### Test Scenarios

```yaml
Scenario 1: No MCPs Installed
  Setup: Fresh Claude Code, no MCP servers

  Test Cases:
    - [ ] Session start works
    - [ ] CLAUDE.md loaded
    - [ ] docs/patterns/ readable
    - [ ] Code search via Grep
    - [ ] TodoWrite functional
    - [ ] Documentation updates work

  Expected: All core functionality works

Scenario 2: Partial MCPs Available
  Setup: Only codegraph installed (the install default)

  Test Cases:
    - [ ] Code structure lookups work (codegraph)
    - [ ] Semantic code search fallback (Grep)
    - [ ] Analysis fallback (Native)
    - [ ] Docs fallback (WebSearch)
    - [ ] Session memory works (.superclaude/memory/ files)

  Expected: codegraph and memory work, others fallback

Scenario 3: MCP Becomes Unavailable
  Setup: Start with MCP, MCP crashes mid-session

  Test Cases:
    - [ ] Detect MCP failure
    - [ ] Auto-fallback to native
    - [ ] Session continues normally
    - [ ] User not impacted

  Expected: Graceful degradation

Scenario 4: MCP Performance Issues
  Setup: MCP slow or timeout

  Test Cases:
    - [ ] Timeout detection (5 seconds)
    - [ ] Auto-fallback
    - [ ] Log performance issue
    - [ ] Continue with native

  Expected: No blocking, auto-fallback
```

## Documentation Strategy

### User-Facing Documentation

```yaml
Getting Started:
  "Core runtime functionality has native fallbacks when MCPs are unavailable"
  "MCP runtime usage is optional"
  "superclaude install installs and registers codegraph (required phase); every other MCP server is optional via superclaude mcp"

Installation Guide:
  Default Setup:
    - Clone repo
    - Run installer (installs and registers codegraph)
    - Start using; choose MCP tools or native runtime fallbacks

  Enhanced Setup (Optional):
    - Install Auggie (faster code understanding)
    - Install Context7 (curated docs)
    - Install Tavily (better search)

Performance Comparison:
  "With MCPs: 2-3x faster, 30-50% fewer tokens"
  "Without MCPs: Slightly slower, works perfectly"
  "Recommendation: Start without, add MCPs if needed"
```

### Developer Documentation

```yaml
MCP Integration Guidelines:

Rule 1: Always provide runtime fallback (not suppression of installer failures)
  ✅ try_mcp_then_fallback()
  ❌ require_mcp_or_fail()

Rule 2: Silent degradation
  ✅ Fallback transparently
  ❌ Show errors to user

Rule 3: Test both paths
  ✅ Test with and without MCPs
  ❌ Only test with MCPs

Rule 4: Document fallback behavior
  ✅ "Uses Grep if Auggie unavailable"
  ❌ "Requires Auggie MCP"

Rule 5: Performance expectations
  ✅ "30% slower without MCP"
  ❌ "Not functional without MCP"
```

## Benefits of Optional Design

```yaml
Accessibility:
  ✅ No barriers to entry
  ✅ Works on any system
  ✅ Core runtime has no dependency on MCP availability
  ✅ Easy onboarding

Reliability:
  ✅ No single point of failure
  ✅ Graceful degradation
  ✅ Always functional baseline
  ✅ MCP issues don't block work

Flexibility:
  ✅ Users choose their setup
  ✅ Incremental enhancement
  ✅ Mix and match MCPs
  ✅ Easy testing/debugging

Maintenance:
  ✅ Framework works independently
  ✅ MCP updates don't break framework
  ✅ Easy to add new MCPs
  ✅ Easy to remove problematic MCPs
```

## Migration Path

```yaml
Current Users (No MCPs):
  Status: Already working
  Action: None required
  Benefit: Can add MCPs incrementally

New Users:
  Step 1: Install the framework
  Step 2: Choose MCP usage or native fallbacks at runtime
  Step 3: Add other MCPs if desired (optional)

MCP Adoption:
  Mindset: "Nice to have, not must have"
  Approach: Incremental enhancement
  Philosophy: Core functionality always works
```

## Conclusion

```yaml
Core Message:
  "SuperClaude Framework is MCP-optional by design"
  "MCPs enhance performance, not functionality"
  "Native tools provide reliable baseline"
  "Choose your enhancement level"

User Choice:
  Minimal: No MCPs, full functionality
  Standard: Install only the MCPs you use; runtime usage optional
  Enhanced: All MCPs, maximum performance
  Custom: Pick and choose based on needs

Design Success:
  ✅ No MCP availability requirement for basic runtime operation
  ✅ Graceful degradation always
  ✅ User empowerment through choice
  ✅ Reliable baseline guaranteed
```
