#!/usr/bin/env bash
# setup-selftest.sh — Task 2 cases for setup.sh, run by selftest.sh.
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
root=$(cd -- "$here/../../../.." && pwd)   # scripts -> 442 -> issues -> .dev -> worktree root
RB=$root/.dev/issues/442/observation-runbook.md
failures=0
ck() { if [ "$2" = "$3" ]; then printf 'OK %s\n' "$1"; else printf 'FAIL %s got=<%s> want=<%s>\n' "$1" "$2" "$3"; failures=$((failures+1)); fi; }

# Fake HOME so the script copies stub commands/skills/agents, not the real ones.
FAKE=$(mktemp -d /tmp/ob-setup-fake.XXXXXXXX)
export HOME=$FAKE
mkdir -p "$FAKE/.claude/hooks" "$FAKE/.claude/commands" "$FAKE/.claude/skills" "$FAKE/.claude/agents" "$FAKE/.claude/state/launch-level/sessions" "$FAKE/.claude/state/launch-level/pending"
printf '# launch-level-guard-version: 1\n' > "$FAKE/.claude/hooks/launch-level-guard.sh"
printf 'guard-body\n' >> "$FAKE/.claude/hooks/launch-level-guard.sh"
cp "$FAKE/.claude/hooks/launch-level-guard.sh" "$FAKE/.claude/hooks/launch-job-identity.sh"
printf 'cmd\n' > "$FAKE/.claude/commands/x.md"
printf 'skill\n' > "$FAKE/.claude/skills/x.md"
printf 'agent\n' > "$FAKE/.claude/agents/x.md"
printf 'old-session\n' > "$FAKE/.claude/state/launch-level/sessions/oldsid"

# Temp OB (created by setup.sh itself) and a separate stub-log dir.
T=$(mktemp -d /tmp/ob-setup.XXXXXXXX)
rmdir "$T"
export OB=$T
STUBLOG=$(mktemp -d /tmp/ob-setup-stub.XXXXXXXX)
export OB_STUB_LOG=$STUBLOG

# Before-snapshot of the fake HOME/.claude (for case 5), kept outside $OB.
find "$FAKE/.claude" -printf '%P\n' | LC_ALL=C sort > "$STUBLOG/fake-before-list.txt"
find "$FAKE/.claude" -type f -exec md5sum {} + | LC_ALL=C sort > "$STUBLOG/fake-before-digest.txt"

out=$(bash "$here/setup.sh" 2>&1); rc=$?
ck setup-rc "$rc" 0
ck setup-ok "$(printf '%s' "$out" | tail -1)" "SETUP_OK"

# 1. layout under the test OB
for p in bin bin/log-only-probe.sh logs home/.claude/hooks home/.claude/hooks/launch-level-guard.sh home/.claude/commands home/.claude/skills home/.claude/agents screens repo-a repo-push settings-a2.json baseline-sessions.txt baseline-pending.txt preconditions.txt; do
  if [ -e "$T/$p" ] || [ -L "$T/$p" ]; then ck "layout:$p" ok ok; else ck "layout:$p" missing ok; fi
done
[ -x "$T/bin/log-only-probe.sh" ] && ck probe-executable ok ok || ck probe-executable missing ok
grep -q 'oldsid' "$T/baseline-sessions.txt" && ck baseline-sessions ok ok || ck baseline-sessions missing ok

# 2. refusal without --resume
if bash "$here/setup.sh" >/dev/null 2>&1; then ck rerun-refused called ok; else ck rerun-refused ok ok; fi
# --resume passes the guard
out2=$(bash "$here/setup.sh" --resume 2>&1); rc2=$?
ck rerun-resume-rc "$rc2" 0

# 3. probe files byte-for-byte vs the runbook blocks
extract() {  # extract <start-line> <end-line>: lines between the fences, from the runbook
  sed -n "$1,$2p" "$RB"
}
# ob-probe.sh: runbook lines 62-86; ob-tree.sh: 97-110; settings.json: 121-136.
sed -n '62,86p' "$RB" > "$T/want-probe.sh"; diff -q "$T/want-probe.sh" "$T/bin/ob-probe.sh" >/dev/null && ck probe-bytes ok ok || ck probe-bytes differ ok
sed -n '97,110p' "$RB" > "$T/want-tree.sh"; diff -q "$T/want-tree.sh" "$T/bin/ob-tree.sh" >/dev/null && ck tree-bytes ok ok || ck tree-bytes differ ok
sed -n '121,136p' "$RB" > "$T/want-settings.json"; diff -q "$T/want-settings.json" "$T/home/.claude/settings.json" >/dev/null && ck settings-bytes ok ok || ck settings-bytes differ ok

# 4. A2 settings: guard removed, label h1m
jq -e '(.hooks.UserPromptSubmit[0].hooks | length) == 1 and (.hooks.UserPromptSubmit[0].hooks[0].command | test("h1m$")) and ((.hooks[][]?.hooks[].command // "") | test("launch-level-guard") | not)' \
  "$T/settings-a2.json" >/dev/null && ck a2-settings ok ok || ck a2-settings wrong ok

# 5. nothing written outside OB: the fake HOME/.claude is byte-identical before/after
find "$FAKE/.claude" -printf '%P\n' | LC_ALL=C sort > "$STUBLOG/fake-after-list.txt"
find "$FAKE/.claude" -type f -exec md5sum {} + | LC_ALL=C sort > "$STUBLOG/fake-after-digest.txt"
if diff -q "$STUBLOG/fake-before-list.txt" "$STUBLOG/fake-after-list.txt" >/dev/null \
  && diff -q "$STUBLOG/fake-before-digest.txt" "$STUBLOG/fake-after-digest.txt" >/dev/null; then
  ck fake-claude-clean ok ok
else
  ck fake-claude-clean changed ok
  diff "$STUBLOG/fake-before-list.txt" "$STUBLOG/fake-after-list.txt" | sed 's/^/    /'
  diff "$STUBLOG/fake-before-digest.txt" "$STUBLOG/fake-after-digest.txt" | sed 's/^/    /'
fi

# 6. the login check ran through the stub claude with the isolated HOME
grep -q -- '-p' "$OB_STUB_LOG/claude.log" && ck login-stub-called ok ok || ck login-stub-called missing ok

# 7. repos built: side branch on repo-push, pre-push hook installed
timeout 10 git -C "$T/repo-push" rev-parse --verify -q refs/heads/side >/dev/null && ck repo-push-side ok ok || ck repo-push-side missing ok
[ -x "$T/repo-a/.git/hooks/pre-push" ] && ck prepush-hook ok ok || ck prepush-hook missing ok

# 8. preconditions recorded every check
for id in P1a P2 P3 P4 P5 P6 P7 P8; do
  grep -q "^== $id" "$T/preconditions.txt" && ck "prec:$id" ok ok || ck "prec:$id" missing ok
done

rm -rf "$FAKE"
exit $failures
