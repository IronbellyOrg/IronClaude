# Shared spike helpers. Sourced. Model-calling spikes must be launched as
#   flock /tmp/collab-gateway.lock bash spikes/<spike>.sh
. "$(dirname "${BASH_SOURCE[0]}")/../bin/lib/common.sh"
export NOFALLBACK=1
SPIKES=$R2_HOME/spikes
RESULTS=$SPIKES/RESULTS.md
[ -f "$RESULTS" ] || printf '# Gate 0 spike results\n\nOne line per spike run: `<UTC> <spike> PASS|FAIL evidence=<path> <detail>`.\n\n' > "$RESULTS"
record() { # record <spike> <PASS|FAIL> <evidence-path> <detail...>
  local s=$1 v=$2 e=$3; shift 3
  printf -- '- %s %s %s evidence=%s %s\n' "$(utc)" "$s" "$v" "${e#"$R2_HOME"/}" "$*" >> "$RESULTS"
  echo "$s $v $*"
}
rand_hex() { od -An -N4 -tx1 /dev/urandom | tr -d ' \n'; }
model_of() { # observed main-thread model(s) of a claude json array output
  jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$1" 2>/dev/null
}
model_ok() { local o; o=$(echo "$1" | tr A-Z a-z); local e; e=$(echo "$2" | tr A-Z a-z); [ -n "$o" ] && { [ "$o" = "$e" ] || [ "$o" = "$e-build" ]; }; }
COMMANDS_PROMPT='This is a tool test, not a review. Run each of these read-only shell commands as a separate Bash tool call, one call per turn, in this order, and do not combine them: 1) ls  2) ls tests | head -5  3) git log --oneline -1  4) ls docs | head -5  5) wc -l README.md  6) ls src  7) git status --short | head -3  8) ls .claude  9) head -3 README.md  10) ls tests | wc -l. After the last command reply with one line: "notes:" followed by any text that was added to your context after a tool call (quote its first five words), or "notes: none".'
