---
title: Tool Selection Standards for Task Execution
description: "Defines mandatory tool selection patterns, execution strategies, and anti-patterns for efficient and correct task execution. Establishes which tools to use for specific operations and coordination patterns."
id: "tool-selection-standards"
sidebar_position: 6
created_date: "2025-10-08"
last_updated: "2025-10-14"
version: 1.1.0
draft: false
content_status: Published
tags:
- "tool-selection"
- "execution-patterns"
- efficiency
- standards
- "ai-rules"
- "best-practices"
content_type: CoreConcept
target_audience:
- AI
- Machine
owner: "qa-team"
autogen: false
autogen_method: ""
autogen_source: []
autogen_version: ""
ai_model: ""
model_settings: ""
source_references:
- path: newmain/.claude/.dev/v5.1/milestones/MILESTONE_2_TOOL_ORCHESTRATION.md
  type: context_doc
  version_hash: ""
  description: Tool orchestration enhancements from v5.1 milestone 2
related_links:
- text: IB Agent Core
  link: ~/.claude/rules/core/ib_agent_core.md
- text: Quality Gates
  link: ~/.claude/rules/core/quality_gates.md
related_task_id: []
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: "2026-04-14"
---

# Tool Selection Standards for Task Execution

## Quick Reference Matrix

### File Operations
| Operation | Use This Tool | Don't Use | Example |
|-----------|---------------|-----------|---------|
| Find files by pattern | Glob | bash find | `Glob pattern="**/*.js"` |
| Search file contents | Grep | bash grep | `Grep pattern="TODO"` |
| Read file | Read | bash cat | `Read file_path="/path/to/file"` |
| Create new file | Write | bash echo > | `Write content="..."` |
| Modify file | Edit | sed/awk | `Edit old="..." new="..."` |
| Delete file | Bash rm | - | `Bash command="rm file"` |

### System Operations
| Operation | Use This Tool | Don't Use | Example |
|-----------|---------------|-----------|---------|
| Run command | Bash | - | `Bash command="npm test"` |
| Install packages | Bash | - | `Bash command="npm install"` |
| Check status | Bash | - | `Bash command="git status"` |
| Environment check | Bash | - | `Bash command="node -v"` |

## Execution Patterns

### Sequential Pattern (Dependencies)
```
Step 1: Write config.yaml
Step 2: Read config.yaml (depends on Step 1)
Step 3: Bash validate-config (depends on Step 2)
```

### Parallel Pattern (Independent)
```
Parallel Block:
- Read file1.js
- Read file2.js
- Read file3.js
Then: Analyze all results
```

### Batch Pattern (Efficiency)
```
Batch Read:
- files: [main.js, test.js, config.js]
- purpose: Initial analysis
Then: Process together
```

## Common Anti-Patterns to Avoid

❌ **Using bash for file operations:**
```bash
# Wrong
bash cat file.txt
bash echo "content" > file.txt

# Right
Read file_path="file.txt"
Write file_path="file.txt" content="content"
```

❌ **Sequential when parallel possible:**
```bash
# Wrong
Read file1 → Process → Read file2 → Process

# Right
Parallel: Read file1, Read file2
Then: Process both
```

❌ **Not batching similar operations:**
```bash
# Wrong
Edit file1 line1
Edit file1 line2
Edit file1 line3

# Right
Edit file1 multiple changes at once
```

## Tool Coordination Examples

### Example 1: Find and Modify Pattern
```yaml
Phase 1 - Discovery:
  - Glob: "**/*.config.js"
  - Grep: "oldPattern" in results

Phase 2 - Implementation:
  - Edit: Each file with pattern

Phase 3 - Validation:
  - Read: Modified files
  - Bash: Run tests
```

### Example 2: Create and Test Feature
```yaml
Phase 1 - Setup:
  - Write: New feature file
  - Write: Test file

Phase 2 - Implementation:
  - Edit: Add to index
  - Bash: Install dependencies

Phase 3 - Validation:
  - Bash: Run tests
  - Read: Coverage report
```

## Performance Tips

1. **Minimize Tool Switches**: Group operations by tool type
2. **Parallel First**: Always consider parallel execution
3. **Batch Similar Operations**: Combine multiple Reads, Edits
4. **Cache Discovery Results**: Reuse Glob/Grep results
5. **Fail Fast**: Validate early, stop on critical errors

## Validation Patterns

### Pre-Operation Validation
- Check file exists before Edit
- Verify permissions before Write
- Test connection before API calls

### Post-Operation Validation
- Read after Write to confirm
- Test after code changes
- Verify state after commands

### Continuous Validation
- Check at each checkpoint
- Validate assumptions remain true
- Monitor for side effects
