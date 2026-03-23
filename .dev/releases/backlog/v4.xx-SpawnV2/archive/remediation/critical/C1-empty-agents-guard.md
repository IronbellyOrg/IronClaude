# C1: Zero/Empty Attack on `--agents` — Remediation Proposal

## Problem
The guard `STOP if source: agents but --agents not provided on CLI` only checks flag presence, not parsed content. `--agents ""`, `--agents ","`, or `--agents "invalid"` all bypass the guard.

## Step-by-Step Solution

### Step 1: Replace presence check with parsed-count validation
**Location**: SKILL.md → Pipeline Execution → Step 2 (Expand Dynamic Phases)

Current:
```
STOP if `source: agents` but `--agents` not provided on CLI
```

Replace with:
```
1. STOP if `source: agents` but `--agents` flag not provided →
   Error: "--agents required for generate-parallel phase"
2. Parse --agents value using adversarial agent-spec parsing rules
3. STOP if parsed agent list is empty (0 valid specs) →
   Error: "--agents provided but contains no valid agent specifications.
   Expected format: model[:persona[:\"instruction\"]], e.g. opus:architect"
4. WARN if any individual spec failed parsing →
   "Skipped invalid agent spec '<raw>': <reason>. Continuing with N valid agents."
5. STOP if valid agent count < 1 after filtering →
   Error: "All --agents specs were invalid. None could be parsed."
```

### Step 2: Define parsing validation for each degenerate case

| Input | Parse Result | Behavior |
|-------|-------------|----------|
| `""` (empty string) | 0 specs | STOP: "contains no valid agent specifications" |
| `","` (commas only) | 0 specs after split+filter | STOP: same |
| `",,opus,"` | 1 valid (opus), 2 empty | WARN about empties, continue with 1 |
| `"invalid-model"` | 0 valid (model not recognized) | STOP: "All specs invalid" |
| `"opus:invalid-persona"` | 1 valid | WARN: "Unknown persona 'invalid-persona', using model defaults" (per adversarial convention) |
| `"opus:architect:unquoted instruction"` | Parse error | WARN: "Instruction must be quoted", skip this spec |

### Step 3: Align with adversarial agent-spec parsing rules
Import the exact parsing rules from `refs/agent-specs.md`:
- Split on `,` to get individual specs
- For each spec, split on `:` (max 3 segments)
- Segment 1 (model): REQUIRED, must be recognized model name
- Segment 2 (persona): OPTIONAL, WARN if unknown
- Segment 3 (instruction): OPTIONAL, must be double-quoted

### Step 4: Add validation to generate-parallel definition in SKILL.md

Add after the expansion rule:
```
**Post-parse validation**:
- Filter empty strings from split result
- Validate each spec against agent-spec parsing rules
- Collect valid specs and parsing warnings
- STOP if valid_count == 0
- WARN for each skipped spec (with reason)
- Proceed with valid specs only
```

### Step 5: Update error handling matrix
Add row:
```
| `--agents` present but all specs invalid | STOP: "All --agents specs invalid" | None |
| `--agents` has mix of valid/invalid | WARN per invalid, continue with valid | Skip invalid specs |
```

## Files to Modify
- `SKILL.md`: Pipeline Execution Step 2 validation
- `SKILL.md`: generate-parallel Validation section
- `SKILL.md`: Error Handling matrix (add 2 rows)
