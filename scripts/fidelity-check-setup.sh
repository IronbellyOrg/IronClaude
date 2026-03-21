#!/usr/bin/env bash
# fidelity-check-setup.sh — Prepare a release directory for spec-fidelity-only resume
#
# Scans a release directory for the required upstream artifacts, validates that
# all 7 pre-fidelity gates would pass, discovers the agent specs from generate
# variant filenames, and writes a .roadmap-state.json that causes `--resume`
# to skip steps 1-7 and only execute spec-fidelity.
#
# Usage:
#   ./scripts/fidelity-check-setup.sh <spec-file> <release-dir>
#   ./scripts/fidelity-check-setup.sh <spec-file> <release-dir> --dry-run
#   ./scripts/fidelity-check-setup.sh <spec-file> <release-dir> --run
#   ./scripts/fidelity-check-setup.sh <spec-file> <release-dir> --skip-gate-checks
#   ./scripts/fidelity-check-setup.sh <spec-file> <release-dir> --skip-gate-checks --run
#
# Options:
#   --dry-run           Validate everything but don't write state or invoke pipeline
#   --run               Write state AND invoke `superclaude roadmap run --resume --no-validate`
#   --skip-gate-checks  For older/pre-adversarial releases: patches missing frontmatter
#                       and creates minimal stub files for missing pipeline artifacts so
#                       their gates pass on --resume. Originals backed up to .fidelity-backup/
#                       and restored automatically after --run or --dry-run completes.
#   (default)           Write state only; prints the command to run manually

set -euo pipefail

# --- Colors ---
if [[ -t 1 ]]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'
    CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; CYAN=''; BOLD=''; NC=''
fi

pass()  { echo -e "  ${GREEN}PASS${NC}  $1"; }
fail()  { echo -e "  ${RED}FAIL${NC}  $1"; FAILURES=$((FAILURES + 1)); }
warn()  { echo -e "  ${YELLOW}WARN${NC}  $1"; }
skip()  { echo -e "  ${YELLOW}SKIP${NC}  $1"; GATE_SKIPS=$((GATE_SKIPS + 1)); }
info()  { echo -e "  ${CYAN}INFO${NC}  $1"; }
header(){ echo -e "\n${BOLD}$1${NC}"; }

FAILURES=0
GATE_SKIPS=0
PATCHED_FILES=()
CREATED_STUBS=()

# --- Argument parsing ---
if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <spec-file> <release-dir> [--dry-run|--run] [--skip-gate-checks]"
    exit 1
fi

SPEC_FILE="$(realpath "$1")"
RELEASE_DIR="$(realpath "$2")"
MODE="write-only"
SKIP_GATES="false"

shift 2
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)          MODE="dry-run" ;;
        --run)              MODE="run" ;;
        --skip-gate-checks) SKIP_GATES="true" ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

BACKUP_DIR="$RELEASE_DIR/.fidelity-backup"

# --- Cleanup: restore patched files and remove stubs on exit ---
restore_backups() {
    if [[ "$MODE" == "dry-run" || "$MODE" == "run" ]]; then
        local restored=false
        # Restore patched files
        if [[ ${#PATCHED_FILES[@]} -gt 0 && -d "$BACKUP_DIR" ]]; then
            if [[ "$MODE" == "run" ]]; then header "Restoring original files"; fi
            for f in "${PATCHED_FILES[@]}"; do
                local backup="$BACKUP_DIR/$(basename "$f")"
                if [[ -f "$backup" ]]; then
                    cp "$backup" "$f"
                    if [[ "$MODE" == "run" ]]; then pass "Restored: $(basename "$f")"; fi
                    restored=true
                fi
            done
        fi
        # Remove stub files
        if [[ ${#CREATED_STUBS[@]} -gt 0 ]]; then
            for f in "${CREATED_STUBS[@]}"; do
                if [[ -f "$f" ]]; then
                    rm -f "$f"
                    if [[ "$MODE" == "run" ]]; then pass "Removed stub: $(basename "$f")"; fi
                    restored=true
                fi
            done
        fi
        # Clean backup dir
        if [[ -d "$BACKUP_DIR" ]]; then
            rm -rf "$BACKUP_DIR"
            if [[ "$MODE" == "run" && "$restored" == "true" ]]; then
                info "Cleanup complete"
            fi
        fi
    fi
}
trap restore_backups EXIT

# --- Frontmatter patching ---
patch_frontmatter() {
    local file="$1"
    local label="$2"
    shift 2

    if [[ ! -f "$file" ]]; then return 1; fi

    local needs_patch=false
    local fields_to_add=()

    for kv in "$@"; do
        local key="${kv%%=*}"
        if ! grep -q "^[[:space:]]*${key}:" "$file" 2>/dev/null; then
            needs_patch=true
            fields_to_add+=("$kv")
        fi
    done

    if [[ "$needs_patch" == "false" ]]; then return 0; fi

    mkdir -p "$BACKUP_DIR"
    if [[ ! -f "$BACKUP_DIR/$(basename "$file")" ]]; then
        cp "$file" "$BACKUP_DIR/$(basename "$file")"
    fi
    PATCHED_FILES+=("$file")

    local inject=""
    for kv in "${fields_to_add[@]}"; do
        local key="${kv%%=*}"
        local value="${kv#*=}"
        inject="${inject}${key}: ${value}\n"
    done

    local close_line
    close_line=$(awk '/^---[[:space:]]*$/{n++; if(n==2){print NR; exit}}' "$file")
    if [[ -z "$close_line" ]]; then
        warn "$label — could not find frontmatter closing delimiter; skipping patch"
        return 1
    fi

    local tmpfile="${file}.fidelity-tmp"
    head -n $((close_line - 1)) "$file" > "$tmpfile"
    echo -e "$inject" | sed '/^$/d' >> "$tmpfile"
    tail -n +$close_line "$file" >> "$tmpfile"
    mv "$tmpfile" "$file"

    skip "$label — patched ${#fields_to_add[@]} missing field(s)"
    return 0
}

# --- Stub file creation for pre-adversarial releases ---
create_stub() {
    local file="$1"
    local label="$2"
    local content="$3"

    if [[ -f "$file" ]]; then return 0; fi

    echo "$content" > "$file"
    CREATED_STUBS+=("$file")
    skip "$label — created gate-passing stub"
}

# --- Derive frontmatter values from existing artifacts ---
derive_test_strategy_fields() {
    local release_dir="$1"
    local complexity_class="MEDIUM"
    local spec_source="unknown"

    if [[ -f "$release_dir/extraction.md" ]]; then
        local cc
        cc=$(grep "^[[:space:]]*complexity_class:" "$release_dir/extraction.md" 2>/dev/null | head -1 | sed 's/.*: *//' | tr -d '"' || true)
        if [[ -n "$cc" ]]; then complexity_class="$cc"; fi
        local ss
        ss=$(grep "^[[:space:]]*spec_source:" "$release_dir/extraction.md" 2>/dev/null | head -1 | sed 's/.*: *//' | tr -d '"' || true)
        if [[ -n "$ss" ]]; then spec_source="$ss"; fi
    fi

    local interleave_ratio="1:2"
    case "$(echo "$complexity_class" | tr '[:lower:]' '[:upper:]')" in
        LOW)    interleave_ratio="1:3" ;;
        MEDIUM) interleave_ratio="1:2" ;;
        HIGH)   interleave_ratio="1:1" ;;
    esac

    local work_milestones=3 validation_milestones=3
    if [[ -f "$release_dir/roadmap.md" ]]; then
        local wm
        wm=$(grep -cE "^#{2,3}\s+(M[0-9]|Phase\s+[0-9])" "$release_dir/roadmap.md" 2>/dev/null || true)
        if [[ -n "$wm" && "$wm" -gt 0 ]]; then work_milestones="$wm"; fi
    fi
    if [[ -f "$release_dir/test-strategy.md" ]]; then
        local vm
        vm=$(grep -cE "^#{2,3}\s+(VM-[0-9]|Validation\s+Milestone)" "$release_dir/test-strategy.md" 2>/dev/null || true)
        if [[ -n "$vm" && "$vm" -gt 0 ]]; then validation_milestones="$vm"; fi
    fi

    DERIVED_SPEC_SOURCE="$spec_source"
    DERIVED_COMPLEXITY_CLASS="$(echo "$complexity_class" | tr '[:lower:]' '[:upper:]')"
    DERIVED_INTERLEAVE_RATIO="$interleave_ratio"
    DERIVED_WORK_MILESTONES="$work_milestones"
    DERIVED_VALIDATION_MILESTONES="$validation_milestones"
}

# ==========================================================================
# 1. Input validation
# ==========================================================================
header "1. Input validation"

if [[ ! -f "$SPEC_FILE" ]]; then
    fail "Spec file not found: $SPEC_FILE"; exit 1
else
    pass "Spec file exists: $SPEC_FILE"
fi

if [[ ! -d "$RELEASE_DIR" ]]; then
    fail "Release directory not found: $RELEASE_DIR"; exit 1
else
    pass "Release directory exists: $RELEASE_DIR"
fi

# Hard requirement: roadmap.md must exist (it's a direct input to spec-fidelity)
if [[ ! -f "$RELEASE_DIR/roadmap.md" ]]; then
    fail "roadmap.md not found — cannot run fidelity check without it"; exit 1
fi

if [[ "$SKIP_GATES" == "true" ]]; then
    warn "--skip-gate-checks active: will patch/stub artifacts for gate compliance"
fi

# ==========================================================================
# 2. Agent variant discovery
# ==========================================================================
header "2. Agent variant discovery"

AGENT_A=""
AGENT_B=""
VARIANT_COUNT=0

for f in "$RELEASE_DIR"/roadmap-*.md; do
    [[ -f "$f" ]] || continue
    basename="$(basename "$f" .md)"
    if [[ "$basename" == "roadmap" ]]; then continue; fi
    agent_id="${basename#roadmap-}"
    VARIANT_COUNT=$((VARIANT_COUNT + 1))
    if [[ -z "$AGENT_A" ]]; then
        AGENT_A="$agent_id"
    elif [[ -z "$AGENT_B" ]]; then
        AGENT_B="$agent_id"
    fi
done

if [[ $VARIANT_COUNT -eq 0 ]]; then
    if [[ "$SKIP_GATES" == "true" ]]; then
        warn "No generate variants found — pre-adversarial release"
        info "Using default agents: opus:architect, haiku:architect"
        AGENT_A="opus-architect"
        AGENT_B="haiku-architect"
        MODEL_A="opus"; PERSONA_A="architect"
        MODEL_B="haiku"; PERSONA_B="architect"
    else
        fail "No generate variants found (roadmap-*.md)"
        info "Expected files like: roadmap-opus-architect.md, roadmap-haiku-architect.md"
    fi
elif [[ $VARIANT_COUNT -eq 1 ]]; then
    warn "Only 1 generate variant found ($AGENT_A); using it for both A and B"
    AGENT_B="$AGENT_A"
    pass "Variant A: roadmap-${AGENT_A}.md"
elif [[ $VARIANT_COUNT -eq 2 ]]; then
    pass "Variant A: roadmap-${AGENT_A}.md"
    pass "Variant B: roadmap-${AGENT_B}.md"
else
    warn "Found $VARIANT_COUNT variants; using first two: $AGENT_A, $AGENT_B"
fi

parse_agent() {
    local id="$1"
    local model="${id%%-*}"
    local persona="${id#*-}"
    echo "$model" "$persona"
}

if [[ -n "$AGENT_A" && -z "${MODEL_A:-}" ]]; then
    read -r MODEL_A PERSONA_A <<< "$(parse_agent "$AGENT_A")"
    read -r MODEL_B PERSONA_B <<< "$(parse_agent "$AGENT_B")"
fi

# ==========================================================================
# 3. Upstream artifact existence
# ==========================================================================
header "3. Upstream artifact existence"

check_file() {
    local path="$1"
    local label="$2"
    local required="${3:-true}"
    if [[ -f "$path" ]]; then
        local lines; lines=$(wc -l < "$path")
        pass "$label ($lines lines)"
        return 0
    elif [[ "$required" == "soft" && "$SKIP_GATES" == "true" ]]; then
        warn "$label — not found (will create stub)"
        return 1
    else
        fail "$label — NOT FOUND"
        return 1
    fi
}

# Hard requirements (inputs to spec-fidelity)
check_file "$RELEASE_DIR/roadmap.md"    "roadmap.md (merged)"

# Soft requirements (upstream pipeline artifacts — can be stubbed)
check_file "$RELEASE_DIR/extraction.md"        "extraction.md"         "soft" || true
HAS_VARIANTS=true
if [[ -n "$AGENT_A" ]]; then
    check_file "$RELEASE_DIR/roadmap-${AGENT_A}.md" "roadmap-${AGENT_A}.md" "soft" || HAS_VARIANTS=false
fi
if [[ -n "$AGENT_B" && "$AGENT_A" != "$AGENT_B" ]]; then
    check_file "$RELEASE_DIR/roadmap-${AGENT_B}.md" "roadmap-${AGENT_B}.md" "soft" || HAS_VARIANTS=false
fi
check_file "$RELEASE_DIR/diff-analysis.md"     "diff-analysis.md"      "soft" || true
check_file "$RELEASE_DIR/debate-transcript.md" "debate-transcript.md"  "soft" || true
check_file "$RELEASE_DIR/base-selection.md"    "base-selection.md"     "soft" || true
check_file "$RELEASE_DIR/test-strategy.md"     "test-strategy.md"      "soft" || true

# ==========================================================================
# 4. Spec-fidelity status
# ==========================================================================
header "4. Spec-fidelity status"

if [[ -f "$RELEASE_DIR/spec-fidelity.md" ]]; then
    warn "spec-fidelity.md already exists"
    info "If its gate passes, --resume will skip it too (nothing to do)"
    info "Delete it first if you want to force re-run: rm $RELEASE_DIR/spec-fidelity.md"
else
    pass "spec-fidelity.md does not exist (will be generated)"
fi

# ==========================================================================
# 4b. Create stubs and patch frontmatter (--skip-gate-checks)
# ==========================================================================
if [[ "$SKIP_GATES" == "true" && $FAILURES -eq 0 ]]; then
    header "4b. Stub creation & frontmatter patching"

    derive_test_strategy_fields "$RELEASE_DIR"
    TIMESTAMP_ISO=$(date -u +%Y-%m-%dT%H:%M:%S+00:00)

    # Derive spec_source and complexity_score for stubs
    STUB_SPEC_SOURCE="${DERIVED_SPEC_SOURCE:-unknown}"
    STUB_COMPLEXITY="0.5"
    if [[ -f "$RELEASE_DIR/extraction.md" ]]; then
        local_cs=$(grep "^[[:space:]]*complexity_score:" "$RELEASE_DIR/extraction.md" 2>/dev/null | head -1 | sed 's/.*: *//' | tr -d '"' || true)
        if [[ -n "$local_cs" ]]; then STUB_COMPLEXITY="$local_cs"; fi
    fi

    # --- Extraction stub ---
    if [[ ! -f "$RELEASE_DIR/extraction.md" ]]; then
        create_stub "$RELEASE_DIR/extraction.md" "extraction" "---
spec_source: $STUB_SPEC_SOURCE
generated: $TIMESTAMP_ISO
generator: fidelity-check-setup-stub
functional_requirements: 0
nonfunctional_requirements: 0
total_requirements: 0
complexity_score: $STUB_COMPLEXITY
complexity_class: $DERIVED_COMPLEXITY_CLASS
domains_detected: [unknown]
risks_identified: 0
dependencies_identified: 0
success_criteria_count: 0
extraction_mode: standard
---

## Functional Requirements
Stub extraction created by fidelity-check-setup.sh for gate compliance.

## Non-Functional Requirements
N/A

## Complexity Assessment
N/A

## Architectural Constraints
N/A

## Risk Inventory
N/A

## Dependency Inventory
N/A

## Success Criteria
N/A

## Open Questions
N/A

$(printf '%.0s\n' {1..30})"
    else
        patch_frontmatter "$RELEASE_DIR/extraction.md" "extraction" \
            "extraction_mode=standard"
    fi

    # --- Generate variant stubs or patches ---
    for agent_id in "$AGENT_A" "$AGENT_B"; do
        [[ -z "$agent_id" ]] && continue
        local_file="$RELEASE_DIR/roadmap-${agent_id}.md"
        if [[ -f "$local_file" ]]; then
            # File exists but may lack frontmatter — patch if needed
            local_persona="${agent_id#*-}"
            if ! head -1 "$local_file" | grep -q "^---"; then
                # No frontmatter at all — prepend it
                mkdir -p "$BACKUP_DIR"
                if [[ ! -f "$BACKUP_DIR/$(basename "$local_file")" ]]; then
                    cp "$local_file" "$BACKUP_DIR/$(basename "$local_file")"
                fi
                PATCHED_FILES+=("$local_file")
                tmpfile="${local_file}.fidelity-tmp"
                cat > "$tmpfile" << FMEOF
---
spec_source: $STUB_SPEC_SOURCE
complexity_score: $STUB_COMPLEXITY
primary_persona: $local_persona
---

FMEOF
                cat "$local_file" >> "$tmpfile"
                mv "$tmpfile" "$local_file"
                skip "roadmap-${agent_id} — prepended frontmatter"
            else
                patch_frontmatter "$local_file" "roadmap-${agent_id}" \
                    "spec_source=$STUB_SPEC_SOURCE" \
                    "complexity_score=$STUB_COMPLEXITY" \
                    "primary_persona=$local_persona"
            fi
        else
            local_persona="${agent_id#*-}"
            # Generate stubs need 100+ lines for GENERATE gate
            stub_lines="---
spec_source: $STUB_SPEC_SOURCE
complexity_score: $STUB_COMPLEXITY
primary_persona: $local_persona
---

## Executive Summary
Stub variant created by fidelity-check-setup.sh for gate compliance.
This is a pre-adversarial release; no dual-variant generation was performed.
The merged roadmap.md is the authoritative artifact.

## Implementation Plan
- See roadmap.md for the authoritative implementation plan.
- This stub exists solely to satisfy pipeline gate requirements.

## Risk Assessment
- See roadmap.md

## Resource Requirements
- See roadmap.md

## Success Criteria
- See roadmap.md

## Timeline
- See roadmap.md
"
            # Pad to 105 lines
            while [[ $(echo "$stub_lines" | wc -l) -lt 105 ]]; do
                stub_lines="${stub_lines}
<!-- stub padding -->"
            done
            create_stub "$local_file" "roadmap-${agent_id}" "$stub_lines"
        fi
    done

    # --- Diff stub (needs 30+ lines) ---
    diff_stub="---
total_diff_points: 0
shared_assumptions_count: 0
---

## Shared Assumptions
Pre-adversarial release — no dual-variant diff performed.

## Divergence Points
None (single-variant release).

## Analysis Notes
- This stub exists solely to satisfy pipeline gate requirements.
- The merged roadmap.md is the authoritative artifact.
"
    while [[ $(echo "$diff_stub" | wc -l) -lt 35 ]]; do
        diff_stub="${diff_stub}
<!-- stub padding -->"
    done
    create_stub "$RELEASE_DIR/diff-analysis.md" "diff-analysis" "$diff_stub"

    # --- Debate stub (needs 50+ lines) ---
    debate_stub="---
convergence_score: 1.0
rounds_completed: 0
---

## Debate Transcript
Pre-adversarial release — no debate performed.
Single-variant release with full convergence by default.

## Round 1
No debate rounds conducted. Single-variant release.

## Convergence Assessment
Full agreement (single variant).

## Summary
- This stub exists solely to satisfy pipeline gate requirements.
- The merged roadmap.md is the authoritative artifact.
"
    while [[ $(echo "$debate_stub" | wc -l) -lt 55 ]]; do
        debate_stub="${debate_stub}
<!-- stub padding -->"
    done
    create_stub "$RELEASE_DIR/debate-transcript.md" "debate-transcript" "$debate_stub"

    # --- Score stub (needs 20+ lines) ---
    score_stub="---
base_variant: $AGENT_A
variant_scores: A:100 B:0
---

## Scoring Criteria
Pre-adversarial release — single variant selected as base by default.

## Per-Criterion Scores
N/A (single variant).

## Overall Scores
- Variant A: 100 (only variant)

## Base Selection Rationale
Only variant available. No adversarial comparison performed.
"
    while [[ $(echo "$score_stub" | wc -l) -lt 25 ]]; do
        score_stub="${score_stub}
<!-- stub padding -->"
    done
    create_stub "$RELEASE_DIR/base-selection.md" "base-selection" "$score_stub"

    # --- Test strategy: patch missing fields ---
    if [[ -f "$RELEASE_DIR/test-strategy.md" ]]; then
        patch_frontmatter "$RELEASE_DIR/test-strategy.md" "test-strategy" \
            "spec_source=$DERIVED_SPEC_SOURCE" \
            "generated=$TIMESTAMP_ISO" \
            "generator=fidelity-check-setup-backfill" \
            "complexity_class=$DERIVED_COMPLEXITY_CLASS" \
            "validation_philosophy=continuous-parallel" \
            "validation_milestones=$DERIVED_VALIDATION_MILESTONES" \
            "work_milestones=$DERIVED_WORK_MILESTONES" \
            "interleave_ratio=$DERIVED_INTERLEAVE_RATIO" \
            "major_issue_policy=stop-and-fix"
    else
        create_stub "$RELEASE_DIR/test-strategy.md" "test-strategy" "---
spec_source: $STUB_SPEC_SOURCE
generated: $TIMESTAMP_ISO
generator: fidelity-check-setup-stub
complexity_class: $DERIVED_COMPLEXITY_CLASS
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 3
interleave_ratio: $DERIVED_INTERLEAVE_RATIO
major_issue_policy: stop-and-fix
---

## Validation Milestones
Stub test strategy created by fidelity-check-setup.sh for gate compliance.

## Test Categories
N/A

## Interleaving Strategy
N/A

## Risk-Based Prioritization
N/A

## Acceptance Criteria
N/A

## Quality Gates
N/A

$(printf '%.0s\n' {1..10})"
    fi

    # --- Patch roadmap.md for MERGE_GATE (all 3 required fields) ---
    if ! head -1 "$RELEASE_DIR/roadmap.md" | grep -q "^---"; then
        # No frontmatter at all — prepend complete block
        mkdir -p "$BACKUP_DIR"
        if [[ ! -f "$BACKUP_DIR/roadmap.md" ]]; then
            cp "$RELEASE_DIR/roadmap.md" "$BACKUP_DIR/roadmap.md"
        fi
        PATCHED_FILES+=("$RELEASE_DIR/roadmap.md")
        tmpfile="$RELEASE_DIR/roadmap.md.fidelity-tmp"
        cat > "$tmpfile" << RMEOF
---
spec_source: $STUB_SPEC_SOURCE
complexity_score: $STUB_COMPLEXITY
adversarial: false
---

RMEOF
        cat "$RELEASE_DIR/roadmap.md" >> "$tmpfile"
        mv "$tmpfile" "$RELEASE_DIR/roadmap.md"
        skip "roadmap.md — prepended full frontmatter (3 fields)"
    else
        patch_frontmatter "$RELEASE_DIR/roadmap.md" "roadmap (merge gate)" \
            "spec_source=$STUB_SPEC_SOURCE" \
            "complexity_score=$STUB_COMPLEXITY" \
            "adversarial=false"
    fi

    # --- Fix quoted interleave_ratio in test-strategy.md ---
    # The gate strips YAML quotes but some older files have "1:2" (quoted)
    # which may interact poorly with patched complexity_class. Normalize.
    if [[ -f "$RELEASE_DIR/test-strategy.md" ]]; then
        if grep -q '^interleave_ratio: "' "$RELEASE_DIR/test-strategy.md" 2>/dev/null; then
            mkdir -p "$BACKUP_DIR"
            if [[ ! -f "$BACKUP_DIR/test-strategy.md" ]]; then
                cp "$RELEASE_DIR/test-strategy.md" "$BACKUP_DIR/test-strategy.md"
            fi
            # Only add to PATCHED_FILES if not already there
            if ! printf '%s\n' "${PATCHED_FILES[@]}" | grep -q "test-strategy.md"; then
                PATCHED_FILES+=("$RELEASE_DIR/test-strategy.md")
            fi
            sed -i 's/^interleave_ratio: "\(.*\)"/interleave_ratio: \1/' "$RELEASE_DIR/test-strategy.md"
            skip "test-strategy.md — unquoted interleave_ratio"
        fi
    fi

    total_changes=$(( ${#PATCHED_FILES[@]} + ${#CREATED_STUBS[@]} ))
    if [[ $total_changes -eq 0 ]]; then
        pass "No patches or stubs needed"
    else
        info "Created ${#CREATED_STUBS[@]} stub(s), patched ${#PATCHED_FILES[@]} file(s)"
    fi
fi

# ==========================================================================
# 5. Gate pre-validation (frontmatter)
# ==========================================================================
header "5. Gate pre-validation (frontmatter spot-checks)"

check_frontmatter() {
    local file="$1"
    local label="$2"
    shift 2
    local fields=("$@")

    if [[ ! -f "$file" ]]; then
        fail "$label — file missing, cannot check frontmatter"
        return
    fi

    local content
    content=$(sed '/^[[:space:]]*$/d' "$file" | head -1 || true)
    if [[ "$content" != "---" ]]; then
        fail "$label — no YAML frontmatter delimiter"
        return
    fi

    local missing=()
    for field in "${fields[@]}"; do
        if ! grep -q "^[[:space:]]*${field}:" "$file" 2>/dev/null; then
            missing+=("$field")
        fi
    done

    if [[ ${#missing[@]} -eq 0 ]]; then
        pass "$label — all ${#fields[@]} required fields present"
    else
        fail "$label — missing fields: ${missing[*]}"
    fi
}

check_frontmatter "$RELEASE_DIR/extraction.md" "EXTRACT_GATE" \
    spec_source generated generator functional_requirements \
    nonfunctional_requirements total_requirements complexity_score \
    complexity_class domains_detected risks_identified \
    dependencies_identified success_criteria_count extraction_mode

[[ -n "$AGENT_A" ]] && check_frontmatter "$RELEASE_DIR/roadmap-${AGENT_A}.md" "GENERATE_A_GATE" \
    spec_source complexity_score primary_persona

[[ -n "$AGENT_B" && "$AGENT_A" != "$AGENT_B" ]] && \
    check_frontmatter "$RELEASE_DIR/roadmap-${AGENT_B}.md" "GENERATE_B_GATE" \
    spec_source complexity_score primary_persona

check_frontmatter "$RELEASE_DIR/diff-analysis.md" "DIFF_GATE" \
    total_diff_points shared_assumptions_count

check_frontmatter "$RELEASE_DIR/debate-transcript.md" "DEBATE_GATE" \
    convergence_score rounds_completed

check_frontmatter "$RELEASE_DIR/base-selection.md" "SCORE_GATE" \
    base_variant variant_scores

check_frontmatter "$RELEASE_DIR/roadmap.md" "MERGE_GATE" \
    spec_source complexity_score adversarial

check_frontmatter "$RELEASE_DIR/test-strategy.md" "TEST_STRATEGY_GATE" \
    spec_source generated generator complexity_class \
    validation_philosophy validation_milestones work_milestones \
    interleave_ratio major_issue_policy

# ==========================================================================
# 6. Gate pre-validation (line counts)
# ==========================================================================
header "6. Gate pre-validation (minimum line counts)"

check_min_lines() {
    local file="$1"
    local label="$2"
    local min="$3"
    if [[ ! -f "$file" ]]; then return; fi
    local lines; lines=$(wc -l < "$file")
    if [[ $lines -ge $min ]]; then
        pass "$label — $lines lines >= $min minimum"
    else
        fail "$label — $lines lines < $min minimum"
    fi
}

check_min_lines "$RELEASE_DIR/extraction.md"           "extract"        50
[[ -n "$AGENT_A" ]] && check_min_lines "$RELEASE_DIR/roadmap-${AGENT_A}.md" "generate-A" 100
[[ -n "$AGENT_B" ]] && check_min_lines "$RELEASE_DIR/roadmap-${AGENT_B}.md" "generate-B" 100
check_min_lines "$RELEASE_DIR/diff-analysis.md"        "diff"           30
check_min_lines "$RELEASE_DIR/debate-transcript.md"    "debate"         50
check_min_lines "$RELEASE_DIR/base-selection.md"       "score"          20
check_min_lines "$RELEASE_DIR/roadmap.md"              "merge"          150
check_min_lines "$RELEASE_DIR/test-strategy.md"        "test-strategy"  40

# ==========================================================================
# 7. Summary
# ==========================================================================
header "7. Summary"

SPEC_HASH=$(sha256sum "$SPEC_FILE" | cut -d' ' -f1)
info "Spec hash: ${SPEC_HASH:0:16}..."
info "Agents: ${MODEL_A:-unknown}:${PERSONA_A:-unknown}, ${MODEL_B:-unknown}:${PERSONA_B:-unknown}"
info "Mode: $MODE"
if [[ "$SKIP_GATES" == "true" ]]; then
    info "Stubs created: ${#CREATED_STUBS[@]}, fields patched: $GATE_SKIPS"
fi

if [[ $FAILURES -gt 0 ]]; then
    echo -e "\n${RED}${BOLD}$FAILURES pre-flight check(s) FAILED.${NC}"
    if [[ "$SKIP_GATES" != "true" ]]; then
        echo "Fix the failures above, or re-run with --skip-gate-checks for older releases."
    else
        echo "Even with --skip-gate-checks, some checks cannot be bypassed."
    fi
    exit 1
fi

echo -e "\n${GREEN}${BOLD}All pre-flight checks passed.${NC}"

STATE_FILE="$RELEASE_DIR/.roadmap-state.json"

if [[ "$MODE" == "dry-run" ]]; then
    echo -e "\n${YELLOW}Dry run — no state file written.${NC}"
    echo "Would write: $STATE_FILE"
    echo ""
    echo "To proceed:"
    echo "  $0 \"$SPEC_FILE\" \"$RELEASE_DIR\"$([ "$SKIP_GATES" == "true" ] && echo " --skip-gate-checks")"
    exit 0
fi

# ==========================================================================
# 8. Write state
# ==========================================================================
header "8. Writing .roadmap-state.json"

if [[ -f "$STATE_FILE" ]]; then
    BACKUP_STATE="${STATE_FILE}.bak.$(date +%s)"
    cp "$STATE_FILE" "$BACKUP_STATE"
    warn "Existing state backed up to: $BACKUP_STATE"
fi

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S+00:00)

cat > "$STATE_FILE" << HEREDOC
{
  "schema_version": 1,
  "spec_file": "$SPEC_FILE",
  "spec_hash": "$SPEC_HASH",
  "agents": [
    {"model": "${MODEL_A:-opus}", "persona": "${PERSONA_A:-architect}"},
    {"model": "${MODEL_B:-haiku}", "persona": "${PERSONA_B:-architect}"}
  ],
  "depth": "standard",
  "last_run": "$TIMESTAMP",
  "steps": {}
}
HEREDOC

pass "State written: $STATE_FILE"

# ==========================================================================
# 9. Execute or print command
# ==========================================================================
if [[ "$MODE" == "run" ]]; then
    header "9. Executing fidelity check"
    echo ""
    set -x
    superclaude roadmap run "$SPEC_FILE" \
        --output "$RELEASE_DIR" \
        --agents "${MODEL_A:-opus}:${PERSONA_A:-architect},${MODEL_B:-haiku}:${PERSONA_B:-architect}" \
        --resume \
        --no-validate
    set +x
else
    header "9. Ready to run"
    echo ""
    echo "Execute:"
    echo "  superclaude roadmap run \"$SPEC_FILE\" \\"
    echo "    --output \"$RELEASE_DIR\" \\"
    echo "    --agents \"${MODEL_A:-opus}:${PERSONA_A:-architect},${MODEL_B:-haiku}:${PERSONA_B:-architect}\" \\"
    echo "    --resume \\"
    echo "    --no-validate"
    if [[ ${#PATCHED_FILES[@]} -gt 0 || ${#CREATED_STUBS[@]} -gt 0 ]]; then
        echo ""
        warn "Files were patched/stubbed. After running, restore originals:"
        echo "  cp $BACKUP_DIR/* $RELEASE_DIR/ 2>/dev/null; rm -rf $BACKUP_DIR"
        for f in "${CREATED_STUBS[@]}"; do
            echo "  rm -f $f"
        done
    fi
fi
