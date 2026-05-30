#!/bin/sh
# repo-inventory.sh — File inventory for /sc:cleanup-audit
# Usage: repo-inventory.sh [target-path] [batch-size]
# Optional env:
#   SCOPE_FILE=path   — per-project file; one extra regex per line, '#' for comments
#                       (default: $TARGET/.claude-audit/SCOPE.md if present)
# Output: Domain-grouped file inventory with batch assignments

set -e

TARGET="${1:-.}"
BATCH_SIZE="${2:-50}"
SCOPE_FILE="${SCOPE_FILE:-$TARGET/.claude-audit/SCOPE.md}"

# --- Default scope exclusions (apply to every audit in every project) ---
# POSIX-extended regex against path RELATIVE to TARGET.
# Rule 1 — hidden paths: any leading-dot segment.
# Rule 2 — BMAD directories: paths owned by BMAD tooling.
# Rule 3 — audit output: .claude-audit/ is itself an audit-artifact dir.
DEFAULT_EXCLUDES='^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/'

# Per-project SCOPE.md may add extra patterns (lines starting with "EXCLUDE: ")
EXTRA_EXCLUDES=""
if [ -f "$SCOPE_FILE" ]; then
    EXTRA_EXCLUDES=$(grep -E '^EXCLUDE: ' "$SCOPE_FILE" 2>/dev/null \
        | sed -E 's/^EXCLUDE: +//' | paste -sd'|' -)
fi

apply_scope() {
    # Filter stdin through default + per-project regex exclusions.
    # `|| true` guards against grep's exit-1 on empty input under `set -e`.
    if [ -n "$EXTRA_EXCLUDES" ]; then
        grep -E -v "($DEFAULT_EXCLUDES|$EXTRA_EXCLUDES)" || true
    else
        grep -E -v "$DEFAULT_EXCLUDES" || true
    fi
}

# Validate target exists
if [ ! -d "$TARGET" ]; then
    echo "ERROR: Target directory '$TARGET' does not exist" >&2
    exit 1
fi

# --- File Enumeration ---
# Use git ls-files for .gitignore-respecting enumeration
# Fall back to find if not in a git repo
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    FILE_LIST=$(git ls-files -- "$TARGET" 2>/dev/null | apply_scope)
else
    FILE_LIST=$(find "$TARGET" -type f \
        -not -path '*/.git/*' \
        -not -path '*/node_modules/*' \
        -not -path '*/__pycache__/*' \
        -not -path '*/.cache/*' \
        -not -path '*/dist/*' \
        -not -path '*/build/*' \
        -not -path '*/.next/*' \
        -not -path '*/vendor/*' \
        -not -path '*/.venv/*' \
        -not -path '*/venv/*' \
        -not -path '*/.tox/*' \
        -not -path '*/.mypy_cache/*' \
        -not -path '*/.pytest_cache/*' \
        -not -path '*/coverage/*' \
        2>/dev/null | sed 's|^\./||' | apply_scope)
fi

# Echo the active scope rules for transparency
echo "=== ACTIVE SCOPE RULES ==="
echo "  Default excludes: $DEFAULT_EXCLUDES"
if [ -n "$EXTRA_EXCLUDES" ]; then
    echo "  Project excludes (from $SCOPE_FILE): $EXTRA_EXCLUDES"
else
    echo "  Project excludes: (none — no SCOPE.md or no EXCLUDE: lines)"
fi
echo ""

# `grep -c` already prints `0` on a no-match exit-1; use `|| true` to absorb
# that exit without appending a second `0` line (which yields "0\n0" and
# breaks downstream `-gt`/arithmetic with "Illegal number: 0").
TOTAL=$(echo "$FILE_LIST" | grep -c . 2>/dev/null || true)

# --- File Type Distribution ---
echo "=== FILE TYPE DISTRIBUTION ==="
echo "$FILE_LIST" | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
echo ""

# --- Domain Classification ---
# Classify files into domains for batch grouping
classify_domain() {
    file="$1"
    case "$file" in
        *Dockerfile*|*docker-compose*|*.yml|*.yaml|*Makefile|*Justfile|*.sh|*Jenkinsfile|*.tf|*.tfvars)
            echo "infrastructure" ;;
        */.github/*|*/.gitlab-ci*|*/.circleci/*|*/ci/*|*/deploy/*)
            echo "infrastructure" ;;
        *.jsx|*.tsx|*.vue|*.svelte|*.css|*.scss|*.less|*.html|*/components/*|*/pages/*|*/views/*)
            echo "frontend" ;;
        *.py|*.go|*.rs|*.java|*.rb|*.php|*/api/*|*/services/*|*/models/*|*/controllers/*)
            echo "backend" ;;
        *test*|*spec*)
            echo "tests" ;;
        *.md|*.rst|*.txt|*.adoc|*/docs/*|*/doc/*)
            echo "documentation" ;;
        *.json|*.toml|*.ini|*.cfg|*.conf|*.env*|*.config*)
            echo "config" ;;
        *.png|*.jpg|*.jpeg|*.gif|*.svg|*.ico|*.woff*|*.ttf|*.eot|*.mp4|*.webm|*.pdf)
            echo "assets" ;;
        *)
            echo "other" ;;
    esac
}

echo "=== DOMAIN DISTRIBUTION ==="
for domain in infrastructure frontend backend tests documentation config assets other; do
    count=0
    echo "$FILE_LIST" | while IFS= read -r file; do
        d=$(classify_domain "$file")
        if [ "$d" = "$domain" ]; then
            count=$((count + 1))
        fi
    done
    # Use grep-based counting for accuracy
    domain_count=$(echo "$FILE_LIST" | while IFS= read -r file; do classify_domain "$file"; done | grep -c "^${domain}$" 2>/dev/null || true)
    if [ "$domain_count" -gt 0 ]; then
        printf "  %-15s %s files\n" "$domain:" "$domain_count"
    fi
done
echo ""

# --- Batch Assignments ---
echo "=== BATCH ASSIGNMENTS (batch_size=$BATCH_SIZE) ==="
batch_num=1
file_count=0

# Priority ordering: infrastructure > config > tests > backend > frontend > documentation > assets > other
for domain in infrastructure config tests backend frontend documentation assets other; do
    domain_files=$(echo "$FILE_LIST" | while IFS= read -r file; do
        d=$(classify_domain "$file")
        if [ "$d" = "$domain" ]; then
            echo "$file"
        fi
    done)

    if [ -z "$domain_files" ]; then
        continue
    fi

    domain_total=$(echo "$domain_files" | grep -c . 2>/dev/null || true)
    if [ "$domain_total" -eq 0 ]; then
        continue
    fi

    echo ""
    echo "## Domain: $domain ($domain_total files)"

    echo "$domain_files" | while IFS= read -r file; do
        if [ $((file_count % BATCH_SIZE)) -eq 0 ] && [ "$file_count" -gt 0 ]; then
            batch_num=$((batch_num + 1))
        fi
        echo "  [batch-$batch_num] $file"
        file_count=$((file_count + 1))
    done
done

echo ""

# --- Summary ---
BATCH_COUNT=$(( (TOTAL + BATCH_SIZE - 1) / BATCH_SIZE ))
echo "=== SUMMARY ==="
echo "  Total files: $TOTAL"
echo "  Batch size: $BATCH_SIZE"
echo "  Estimated batches: $BATCH_COUNT"
echo "  Target: $TARGET"
