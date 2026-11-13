#!/bin/bash
# usage: alog.sh <out> <wave> <step> <outcome> <evidence_ref|null> [note]
printf '{"wave": "%s", "step": "%s", "timestamp": "%s", "outcome": "%s", "evidence_ref": "%s", "note": "%s"}\n' "$2" "$3" "$(date -u +%FT%TZ)" "$4" "$5" "${6:-}" >> "$1/audit.log"
