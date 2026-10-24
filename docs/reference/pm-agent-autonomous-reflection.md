# PM Agent: Autonomous Reflection & Token Optimization

**Version**: 2.0
**Date**: 2025-10-17
**Status**: Historical design document (2025-10-17), not a description of verified current behavior. The `pm.md` sections it cites by line number are historical and belong to an earlier version: `plugins/superclaude/commands/pm.md` is now 112 lines and contains no confidence-check, self-check or evidence section (related Python helpers live in `src/superclaude/pm_agent/`). Every savings, detection-rate, accuracy and token figure below is a design target, an estimate or a number quoted from a paper or vendor; none was measured in this repository.

---

## 🎯 Overview

PM Agentの自律的振り返りとトークン最適化システム。**間違った方向に爆速で突き進む**問題を解決し、**嘘をつかず、証拠を示す**文化を確立。

### Core Problems Solved

1. **並列実行 × 間違った方向 = トークン爆発**
   - 解決: Confidence Check (実装前確信度評価)
   - 効果: Low confidence時は質問、無駄な実装を防止

2. **ハルシネーション: "動きました！"(証拠なし)**
   - 解決: Evidence Requirement (証拠要求プロトコル)
   - 効果: テスト結果必須、完了報告ブロック機能

3. **同じ間違いの繰り返し**
   - 解決: Reflexion Pattern (過去エラー検索。明示的に呼び出す `ReflexionPattern` API で、自動ではない)
   - 効果: 未測定 (94% は論文の数値で、このシステムで測定した値ではない / unverified: the 94% figure comes from the paper, not from this system)

4. **振り返りがトークンを食う矛盾**
   - 解決: Token-Budget-Aware Reflection
   - 効果: 複雑度別予算 (200-2,500 tokens)

---

## 🚀 Quick Start Guide

### For Users

**What Changed?**

- PM Agentが**実装前に確信度を自己評価**します
- **証拠なしの完了報告はブロック**されます
- 過去の失敗を**明示的な API で記録・検索**できます (自動学習ではありません)

**What You'll Notice:**

1. 不確実な時は**素直に質問してきます** (Low Confidence <70%)
2. 完了報告時に**必ずテスト結果を提示**します
3. 記録済みの似たエラーは `get_solution()` で検索できます (最初に一致した記録を返すだけで、自動適用や即時解決の保証はありません)

### For Developers

**Integration Points**:

```yaml
# Historical: these line ranges refer to an earlier pm.md (now 112 lines, none of these sections).
pm.md (plugins/superclaude/commands/):
  - Line 870-1016: Self-Correction Loop (拡張済み; historical)
    - Confidence Check (Line 881-921)
    - Self-Check Protocol (Line 928-1016)
    - Evidence Requirement (Line 951-976)
    - Token Budget Allocation (Line 978-989)

Implementation (as claimed on 2025-10-17 for that earlier pm.md; not re-verified):
  ✅ Confidence Scoring: 3-tier system (High/Medium/Low)
  ✅ Evidence Requirement: Test results + code changes + validation
  ✅ Self-Check Questions: 4 mandatory questions before completion
  ✅ Token Budget: Complexity-based allocation (200-2,500 tokens)
  ✅ Hallucination Detection: 7 red flags with auto-correction
```

---

## 📊 System Architecture

### Layer 1: Confidence Check (実装前)

**Purpose**: 間違った方向に進む前に止める

```yaml
When: Before starting implementation
Token Budget: 100-200 tokens

Process:
  1. PM Agent自己評価: "この実装、確信度は？"

  2. High Confidence (90-100%):
     ✅ 公式ドキュメント確認済み
     ✅ 既存パターン特定済み
     ✅ 実装パス明確
     → Action: 実装開始

  3. Medium Confidence (70-89%):
     ⚠️ 複数の実装方法あり
     ⚠️ トレードオフ検討必要
     → Action: 選択肢提示 + 推奨提示

  4. Low Confidence (<70%):
     ❌ 要件不明確
     ❌ 前例なし
     ❌ ドメイン知識不足
     → Action: STOP → ユーザーに質問

Example Output (Low Confidence):
  "⚠️ Confidence Low (65%)

   I need clarification on:
   1. Should authentication use JWT or OAuth?
   2. What's the expected session timeout?
   3. Do we need 2FA support?

   Please provide guidance so I can proceed confidently."

Result:
  ✅ 無駄な実装を防止
  ✅ トークン浪費を防止
  ✅ ユーザーとのコラボレーション促進
```

### Layer 2: Self-Check Protocol (実装後)

**Purpose**: ハルシネーション防止、証拠要求

```yaml
When: After implementation, BEFORE reporting "complete"
Token Budget: 200-2,500 tokens (complexity-dependent)

Mandatory Questions:
  ❓ "テストは全てpassしてる？"
     → Run tests → Show actual results
     → IF any fail: NOT complete

  ❓ "要件を全て満たしてる？"
     → Compare implementation vs requirements
     → List: ✅ Done, ❌ Missing

  ❓ "思い込みで実装してない？"
     → Review: Assumptions verified?
     → Check: Official docs consulted?

  ❓ "証拠はある？"
     → Test results (actual output)
     → Code changes (file list)
     → Validation (lint, typecheck)

Evidence Requirement:
  IF reporting "Feature complete":
    MUST provide:
      1. Test Results:
         pytest: 15/15 passed (0 failed)
         coverage: 87% (+12% from baseline)

      2. Code Changes:
         Files modified: auth.py, test_auth.py
         Lines: +150, -20

      3. Validation:
         lint: ✅ passed
         typecheck: ✅ passed
         build: ✅ success

  IF evidence missing OR tests failing:
    ❌ BLOCK completion report
    ⚠️ Report actual status:
       "Implementation incomplete:
        - Tests: 12/15 passed (3 failing)
        - Reason: Edge cases not handled
        - Next: Fix validation for empty inputs"

Hallucination Detection (7 Red Flags):
  🚨 "Tests pass" without showing output
  🚨 "Everything works" without evidence
  🚨 "Implementation complete" with failing tests
  🚨 Skipping error messages
  🚨 Ignoring warnings
  🚨 Hiding failures
  🚨 "Probably works" statements

  IF detected:
    → Self-correction: "Wait, I need to verify this"
    → Run actual tests
    → Show real results
    → Report honestly

Result (intended; not measured here):
  ✅ 94% hallucination detection rate (figure quoted from the Reflexion paper, not measured in this system)
  ✅ Evidence-based completion reports
  ✅ No false claims
```

### Layer 3: Reflexion Pattern (エラー時)

**Purpose**: 過去の失敗から学習、同じ間違いを繰り返さない

> **Status**: explicit API only (`src/superclaude/pm_agent/reflexion.py`). The PM agent does not call it, nothing loads it at session start, and no fix is applied automatically. The earlier "automatic tool selection", MindBase semantic search and automatic storage described here were never implemented. Full contract: [docs/user-guide/memory-system.md](../user-guide/memory-system.md).

```yaml
When: You (or code you write) call ReflexionPattern. The only automatic use is the
      opt-in pytest recorder (see below).
Token Budget: unmeasured (the "0 tokens" and "1-2K tokens" figures of earlier versions are
              design targets from the class docstring, not measurements)

Process:
  1. Check past errors (explicit call):
     → reflexion.get_solution(error_info)
       * Builds a signature from error_type, error_message (digits become N, first
         100 characters) and test_name
       * Reads solutions_learned.jsonl from the top, in file order
       * Returns the first stored row whose word-set overlap is 0.7 or higher
         ({solution, root_cause, prevention, timestamp}), or None
       * MindBase semantic search is NOT implemented (the hook is a stub returning None)

  2. IF a row is returned:
     → Read it and decide whether it applies. Nothing applies it for you, and a returned
       row may have no solution (its fields come back as None).

  3. ELSE (None):
     → Root cause investigation (WebSearch, docs, patterns)
     → Record what you learned: reflexion.record_error({... solution, root_cause, prevention})

  4. Self-Reflection (a working practice, not something the code produces):
     "Reflection:
      ❌ What went wrong: JWT validation failed
      🔍 Root cause: Missing env var SUPABASE_JWT_SECRET
      💡 Why it happened: Didn't check .env.example first
      ✅ Prevention: Always verify env setup before starting
      📝 Learning: Add env validation to startup checklist"

Storage:
  → <memory_dir>/solutions_learned.jsonl (default docs/memory/; one JSON object per line)
  → <memory_dir>/../mistakes/<test_name>-YYYY-MM-DD.md (default docs/mistakes/; written only
    when root_cause or solution is non-empty)
  → no other backend (MindBase is not implemented)

Record fields (synthetic samples: docs/memory/reflexion.jsonl.example):
  error_type, error_message, test_name, traceback, solution, root_cause, prevention, timestamp

Marked pytest capture:
  → A test marked @pytest.mark.reflexion whose call phase raises is recorded by the plugin
    (test_name, test_file, error_type, error_message, traceback). It does not call
    get_solution() and adds no solution.

Privacy:
  → Nothing is redacted. Callers must redact before recording.

Result (design targets, UNVERIFIED; nothing has been measured):
  · lower recurrence of a repeated error (earlier versions claimed "<10%")
  · fewer tokens spent re-investigating a recorded error
```

### Layer 4: Token-Budget-Aware Reflection

**Purpose**: 振り返りコストの制御

```yaml
Complexity-Based Budget:
  Simple Task (typo fix):
    Budget: 200 tokens
    Questions: "File edited? Tests pass?"

  Medium Task (bug fix):
    Budget: 1,000 tokens
    Questions: "Root cause fixed? Tests added? Regression prevented?"

  Complex Task (feature):
    Budget: 2,500 tokens
    Questions: "All requirements? Tests comprehensive? Integration verified? Documentation updated?"

Token Savings:
  Old Approach:
    - Unlimited reflection
    - Full trajectory preserved
    → 10-50K tokens per task

  New Approach:
    - Budgeted reflection
    - Trajectory compression (90% reduction)
    → 200-2,500 tokens per task

  Savings: 80-98% token reduction on reflection (estimate; not measured)
```

---

## 🔧 Implementation Details

### File Structure

```yaml
Core Implementation:
  plugins/superclaude/commands/pm.md:
    - Line 870-1016: Self-Correction Loop (historical; that version of pm.md no longer exists, the file is now 112 lines)
    - Confidence Check + Self-Check + Evidence Requirement

Research Documentation:
  docs/research/llm-agent-token-efficiency-2025.md (historical; this file no longer exists in the repository):
    - Token optimization strategies
    - Industry benchmarks
    - Progressive loading architecture

  docs/research/reflexion-integration-2025.md (historical; this file no longer exists in the repository):
    - Reflexion framework integration
    - Self-reflection patterns
    - Hallucination prevention

Reference Guide:
  docs/reference/pm-agent-autonomous-reflection.md (THIS FILE):
    - Quick start guide
    - Architecture overview
    - Implementation patterns

Memory Storage:
  docs/memory/solutions_learned.jsonl:
    - Error records written by ReflexionPattern.record_error() (append-only log)
    - Format: {"error_type":"...","error_message":"...","test_name":"...","solution":"...","root_cause":"...","prevention":"...","timestamp":"..."}
    - It also holds older pattern-style rows that the lookup never matches; leave them in place
    - Synthetic samples: docs/memory/reflexion.jsonl.example

  docs/memory/workflow_metrics.jsonl:
    - Documented design for task metrics; no tracked code writes this file
    - Format: {"task_type":"...","tokens_used":N,"success":true}
```

### Integration with Existing Systems

```yaml
Progressive Loading (Token Efficiency):
  Bootstrap (150 tokens) → Intent Classification (100-200 tokens)
  → Selective Loading (500-50K tokens, complexity-based)

Confidence Check (This System):
  → Executed AFTER Intent Classification
  → BEFORE implementation starts
  → Prevents wrong direction (60-95% potential savings; estimate, not measured)

Self-Check Protocol (This System):
  → Executed AFTER implementation
  → BEFORE completion report
  → Prevents hallucination (94% detection rate quoted from the Reflexion paper; not measured here)

Reflexion Pattern (This System):
  → Executed only when called explicitly (plus the opt-in pytest recorder)
  → Lookup: local solutions_learned.jsonl, first match at 0.7 word-set overlap (no MindBase)
  → Effect on error recurrence: unmeasured

Workflow Metrics (documented design; nothing in this repository writes the file):
  → Would track: task_type, complexity, tokens_used, success
  → Intended to enable: A/B testing, workflow optimization
  → Result: unmeasured; no automatic adoption exists
```

---

## 📈 Expected Results

Every figure in this section is a design target, an estimate, or a number quoted from a paper or vendor. None was measured in this repository.

### Token Efficiency

```yaml
Phase 0 (Bootstrap):
  Old: 2,300 tokens (auto-load everything)
  New: 150 tokens (wait for user request)
  Savings: 93% (2,150 tokens; estimate, not measured)

Confidence Check (Wrong Direction Prevention):
  Prevented Implementation: 0 tokens (vs 5-50K wasted)
  Low Confidence Clarification: 200 tokens (vs thousands wasted)
  ROI: 25-250x token savings when preventing wrong implementation (estimate, not measured)

Self-Check Protocol:
  Budget: 200-2,500 tokens (complexity-dependent)
  Old Approach: Unlimited (10-50K tokens with full trajectory)
  Savings: 80-95% on reflection cost (estimate, not measured)

Reflexion (Error Learning) - design targets, NOT measured:
  Known Error: 0 tokens (target for a local file lookup)
  New Error: 1-2K tokens (target for investigation + documentation)
  Second Occurrence: lookup returns a stored row; applying it is up to the caller
  Savings: unmeasured (earlier versions claimed 100% on repeated errors)

Total Expected Savings (design targets, NOT measured):
  Ultra-Light tasks: 72% reduction
  Light tasks: 66% reduction
  Medium tasks: 36-60% reduction (depending on confidence; the error-learning share is unmeasured)
  Heavy tasks: 40-50% reduction
  Overall Average: 60% reduction (design target taken from an industry benchmark; not measured here)
```

### Quality Improvement

```yaml
Hallucination Detection (figure quoted from the Reflexion paper; not measured here):
  Baseline: 0% (no detection)
  With Self-Check: 94% (Reflexion benchmark)
  Result: 94% reduction in false claims (target, not a measured result)

Error Recurrence (historical estimates, UNVERIFIED; nothing here has been measured):
  Baseline: 30-50% (estimate: same error happens again)
  With Reflexion: <10% (target)
  Result: 75% reduction in repeat errors (derived from the two numbers above)

Confidence Accuracy (targets, NOT measured):
  High Confidence → Success: >90%
  Medium Confidence → Clarification needed: ~20%
  Low Confidence → User guidance required: ~80%
  Result: Honest communication, reduced rework
```

### Cultural Impact

```yaml
Before:
  ❌ "動きました！" (no evidence)
  ❌ "たぶん大丈夫" (guessing)
  ❌ "テストは後で" (never tested)
  ❌ 同じエラーを3回繰り返す

After:
  ✅ "Tests: 15/15 passed. Coverage: 87%. Complete."
  ✅ "わかりません。教えてください。" (honest)
  ✅ "過去に似たエラーの記録あり。記録を確認して適用可否を判断。" (explicit lookup; the fix is not applied automatically)
  ✅ Evidence-based, honest communication
```

---

## 🎓 Usage Examples

### Example 1: High Confidence Implementation

```yaml
User: "README誤字修正"

PM Agent:
  Intent: Light task (typo fix)
  Confidence Check:
    ✅ Simple change, high confidence (95%)
    → Proceed

  Implementation:
    - Read README.md
    - Fix typo
    - Run spell check

  Self-Check:
    ❓ Tests pass? → Spell check OK
    ❓ Requirements met? → Typo fixed
    ❓ Evidence? → git diff shows change

  Report:
    "✅ Typo fixed in README.md

     Changes:
     - Line 42: "environemnt" → "environment"

     Validation:
     - Spell check: ✅ passed
     - Build: ✅ success"

Tokens Used: 1,250 (Old: 2,300) = 46% savings (illustrative numbers, not a measurement)
```

### Example 2: Low Confidence → Clarification

```yaml
User: "認証機能実装"

PM Agent:
  Intent: Heavy task (feature implementation)
  Confidence Check:
    ⚠️ Multiple approaches possible
    ❌ Unclear: JWT vs OAuth?
    ❌ Unclear: Session timeout policy?
    → Confidence: 65% (Low)

  Action: STOP → Ask user

  Report:
    "⚠️ Confidence Low (65%)

     Before implementing authentication, I need clarification:
     1. Authentication method: JWT, OAuth, or Supabase Auth?
     2. Session timeout: 1 hour, 24 hours, or 7 days?
     3. 2FA required: Yes or No?
     4. Password policy: Minimum length and complexity?

     Please provide guidance so I can implement correctly."

User: "Use Supabase Auth with JWT. 24 hour sessions. No 2FA for now."

PM Agent:
  Confidence: 95% (High) → Proceed with implementation

Tokens Saved: 15-30K (prevented wrong implementation; illustrative estimate, not a measurement)
```

### Example 3: Hallucination Detection

```yaml
PM Agent (Internal):
  Implementation complete...
  About to report success...

  Self-Check Triggered:
    ❓ "テストは全てpassしてる？"
       → Run pytest...
       → Result: 12/15 passed (3 failing)

    🚨 RED FLAG: Tests failing, can't report "complete"

  Self-Correction:
    "Wait, tests are failing. I can't report success."

  Honest Report:
    "Implementation incomplete:
     - Tests: 12/15 passed (3 failing)
     - Failures: test_edge_cases.py (3 tests)
     - Reason: Empty input validation missing
     - Next: Add validation for empty inputs"

Result:
  ✅ Hallucination prevented
  ✅ Honest communication
  ✅ Clear next action
```

### Example 4: Reflexion Learning

```yaml
Error: "ValueError: invalid port value 9090 in config file" (test_load_config)

Explicit lookup (illustrative; uses the synthetic sample row, not real data):
  reflexion = ReflexionPattern(memory_dir=<isolated test directory>/docs/memory)
  known = reflexion.get_solution({"error_type": "ValueError",
                                  "error_message": "invalid port value 9090 in config file",
                                  "test_name": "test_load_config"})

  If solutions_learned.jsonl holds the first row of docs/memory/reflexion.jsonl.example
  (9 of 10 distinct words shared = 0.90, above the 0.7 threshold), `known` is:
    {"solution": "Validate the port is an integer in 1-65535 before binding",
     "root_cause": "Config loader accepted any string for the port",
     "prevention": "Add a range check to the config schema",
     "timestamp": "2026-01-15T10:00:00.123456"}
  Otherwise `known` is None: investigate, then record the result with record_error().

What happens next is up to the caller. The lookup returns a stored row; it does not
apply the fix. No time or token savings are claimed (none were measured).
```

---

## 🧪 Testing & Validation

### Testing Strategy

```yaml
Unit Tests:
  - Confidence scoring accuracy
  - Evidence requirement enforcement
  - Hallucination detection triggers
  - Token budget adherence

Integration Tests:
  - End-to-end workflow with self-checks
  - Reflexion pattern with memory lookup
  - Error recurrence prevention
  - Metrics collection accuracy

Performance Tests:
  - Token usage benchmarks
  - Self-check execution time
  - Memory lookup latency
  - Overall workflow efficiency

Validation Metrics (targets; no measurement exists for any of them):
  - Hallucination detection: >90%
  - Error recurrence: <10%
  - Confidence accuracy: >85%
  - Token savings: >60%
```

### Monitoring

Design sketch only: nothing in this repository writes `workflow_metrics.jsonl`, the record below uses fields that are not in its documented schema, and workflow metrics are separate from error learning (`solutions_learned.jsonl`).

```yaml
Real-time Metrics (workflow_metrics.jsonl):
  {
    "timestamp": "2025-10-17T10:30:00+09:00",
    "task_type": "feature_implementation",
    "complexity": "heavy",
    "confidence_initial": 0.85,
    "confidence_final": 0.95,
    "self_check_triggered": true,
    "evidence_provided": true,
    "hallucination_detected": false,
    "tokens_used": 8500,
    "tokens_budget": 10000,
    "success": true,
    "time_ms": 180000
  }

Weekly Analysis:
  - Average tokens per task type
  - Confidence accuracy rates
  - Hallucination detection success
  - Error recurrence rates (unmeasured; the metrics file has no such field)
  - A/B testing results
```

---

## 📚 References

### Research Papers

1. **Reflexion: Language Agents with Verbal Reinforcement Learning**
   - Authors: Noah Shinn et al. (2023)
   - Key Insight: 94% error detection through self-reflection
   - Application: PM Agent Self-Check Protocol

2. **Token-Budget-Aware LLM Reasoning**
   - Source: arXiv 2412.18547 (December 2024)
   - Key Insight: Dynamic token allocation based on complexity
   - Application: Budget-aware reflection system

3. **Self-Evaluation in AI Agents**
   - Source: Galileo AI (2024)
   - Key Insight: Confidence scoring reduces hallucinations
   - Application: 3-tier confidence system

### Industry Standards

4. **Anthropic Production Agent Optimization**
   - Achievement: 39% token reduction, 62% workflow optimization
   - Application: Progressive loading + workflow metrics

5. **Microsoft AutoGen v0.4**
   - Pattern: Orchestrator-worker architecture
   - Application: PM Agent architecture foundation

6. **CrewAI + Mem0**
   - Achievement: 90% token reduction with vector DB
   - Application: background reading only; no MindBase integration is implemented

---

## 🚀 Next Steps

### Phase 1: Production Deployment (marked complete on 2025-10-17; not re-verified)

The boxes below record the 2025-10-17 author's claims. The pm.md sections they referred to no longer exist, and no test of these items was run for this document.

- [x] Confidence Check implementation
- [x] Self-Check Protocol implementation
- [x] Evidence Requirement enforcement
- [x] Reflexion Pattern: explicit `ReflexionPattern` API and opt-in pytest recorder (no automatic PM Agent use, no MindBase)
- [x] Token-Budget-Aware Reflection
- [x] Documentation and testing

### Phase 2: Optimization (Next Sprint)

- [ ] A/B testing framework activation
- [ ] Workflow metrics analysis (weekly)
- [ ] Auto-optimization loop (90-day deprecation)
- [ ] Performance tuning based on real data

### Phase 3: Advanced Features (Future)

- [ ] Multi-agent confidence aggregation
- [ ] Predictive error detection (before running code)
- [ ] Adaptive budget allocation (learning optimal budgets)
- [ ] Cross-session learning (pattern recognition across projects)

---

**End of Document**

For implementation details, see `plugins/superclaude/commands/pm.md` (the originally cited Line 870-1016 refer to an earlier version; the file is now 112 lines and has no such section).
For research background, see `docs/research/reflexion-integration-2025.md` (historical; no longer in the repository) and `docs/research/llm-agent-token-efficiency-2025.md` (historical; also no longer in the repository). The current error-record contract is in [docs/user-guide/memory-system.md](../user-guide/memory-system.md).
