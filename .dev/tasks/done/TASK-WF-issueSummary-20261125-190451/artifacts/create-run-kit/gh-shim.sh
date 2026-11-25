#!/usr/bin/env bash
# gh-shim.sh: a stand-in for the GitHub command line tool, for the controlled
# /sc:issue --create runs of issue 834. It never reaches the real tool and never
# opens a network connection. Link it as an executable named `gh` in the first
# folder of PATH (see README-run.md).
#
# It answers only the calls the create flow makes, each logged to the row's own
# log file ($SHIM_LOG_DIR/gh-calls.log). Every other call, and every call about
# an issue number other than this row's fake number, is logged as REFUSED and
# exits non-zero.
#
# Required environment (set per row, see README-run.md):
#   SHIM_ROW_ID      row id, for example S03-standard
#   SHIM_ROW_NUMBER  row number 1..30; the fake issue number is 900000 + this
#   SHIM_LOG_DIR     absolute path of rows/<row id> inside this kit
#   SHIM_FIXTURES    absolute path of the fixtures folder of this kit
#   SHIM_REPO        owner/repo that the scratch directory's origin names
# Optional: SHIM_ISSUE_TYPE (default Feature) answers the issue-type read-back.
set -u

: "${SHIM_ROW_ID:?set SHIM_ROW_ID}"
: "${SHIM_ROW_NUMBER:?set SHIM_ROW_NUMBER}"
: "${SHIM_LOG_DIR:?set SHIM_LOG_DIR}"
: "${SHIM_FIXTURES:?set SHIM_FIXTURES}"
: "${SHIM_REPO:?set SHIM_REPO}"

mkdir -p "$SHIM_LOG_DIR"
LOG="$SHIM_LOG_DIR/gh-calls.log"
FAKE_N=$((900000 + SHIM_ROW_NUMBER))
OWNER="${SHIM_REPO%%/*}"
ARGS="$*"

log() {
  printf '%s %s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" "${2:-}" >> "$LOG"
}

# value of a long option, for example: opt_value --body-file "$@"
opt_value() {
  local want="$1"
  shift
  while [ "$#" -gt 0 ]; do
    if [ "$1" = "$want" ] && [ "$#" -gt 1 ]; then
      printf '%s' "$2"
      return 0
    fi
    shift
  done
  return 1
}

refuse() {
  log REFUSED "$ARGS"
  echo "gh-shim: refused: $ARGS" >&2
  exit 1
}

case "${1:-}" in
  --version)
    echo "gh-shim (not the real GitHub CLI)"
    exit 0
    ;;
  auth)
    if [ "${2:-}" = "status" ]; then
      log OK-AUTH "$ARGS"
      echo "Logged in to github.com (gh-shim)"
      exit 0
    fi
    refuse
    ;;
  label)
    if [ "${2:-}" = "list" ]; then
      log LOOKUP-LABELS "$ARGS"
      cat "$SHIM_FIXTURES/labels.json"
      exit 0
    fi
    refuse
    ;;
  issue)
    case "${2:-}" in
      list)
        log LOOKUP-DUPES "$ARGS"
        cat "$SHIM_FIXTURES/duplicates.json"
        exit 0
        ;;
      create)
        log CREATE "$ARGS"
        body="$(opt_value --body-file "$@" || true)"
        if [ -n "$body" ] && [ -f "$body" ]; then
          cp "$body" "$SHIM_LOG_DIR/issue-body.posted.md"
        fi
        echo "https://github.com/$SHIM_REPO/issues/$FAKE_N"
        exit 0
        ;;
      view)
        [ "${3:-}" = "$FAKE_N" ] || refuse
        log VIEW-TYPE "$ARGS"
        echo "${SHIM_ISSUE_TYPE:-Feature}"
        exit 0
        ;;
      comment)
        [ "${3:-}" = "$FAKE_N" ] || refuse
        log COMMENT "$ARGS"
        body="$(opt_value --body-file "$@" || true)"
        if [ -n "$body" ] && [ -f "$body" ]; then
          cp "$body" "$SHIM_LOG_DIR/comment.posted.md"
        fi
        echo "https://github.com/$SHIM_REPO/issues/$FAKE_N#issuecomment-1"
        exit 0
        ;;
    esac
    refuse
    ;;
  api)
    if [ "${2:-}" = "-X" ] && [ "${3:-}" = "POST" ]; then
      if [ "${4:-}" = "repos/$SHIM_REPO/issues/$FAKE_N/issue-field-values" ]; then
        log FIELD-POST "$ARGS"
        input="$(opt_value --input "$@" || true)"
        if [ -n "$input" ] && [ -f "$input" ]; then
          cp "$input" "$SHIM_LOG_DIR/field-values.posted.json"
        fi
        echo '{}'
        exit 0
      fi
      refuse
    fi
    case "${2:-}" in
      "repos/$SHIM_REPO/issue-types")
        log LOOKUP-TYPES "$ARGS"
        cat "$SHIM_FIXTURES/issue-types.json"
        exit 0
        ;;
      "orgs/$OWNER/issue-fields")
        log LOOKUP-FIELDS "$ARGS"
        cat "$SHIM_FIXTURES/issue-fields.json"
        exit 0
        ;;
      "repos/$SHIM_REPO/issues/$FAKE_N/issue-field-values")
        log FIELD-READ "$ARGS"
        if [ -f "$SHIM_LOG_DIR/field-values.posted.json" ]; then
          cat "$SHIM_LOG_DIR/field-values.posted.json"
        else
          echo '[]'
        fi
        exit 0
        ;;
    esac
    refuse
    ;;
esac

# Default branch: any call not listed above is refused and logged.
refuse
