# Phase 5 Runbook — Interactive freshness-system validation

**Purpose:** step-by-step recipe for the parts of Phase 5 that require fresh,
interactive Claude Code sessions. T05.01 (live install) was completed in the
prior session; this runbook covers T02.05 probe and T05.02–T05.04.

**Pre-flight:**
- `~/.claude/settings.json` contains all 7 freshness event keys (`jq -r '.hooks | keys[]' ~/.claude/settings.json`).
- `~/.claude/hooks/` has 8 scripts including `freshness-*.sh` and `session-init.sh`.
- `~/.claude/CLAUDE.md` ends with the `## Context freshness discipline` section.
- Backup exists: `ls ~/.claude/settings.json.bak.*`.

---

## T02.05 — FileChanged stdin schema probe (DONE 2026-05-13, **CLOSED**)

**Outcome:** the probe revealed that Claude Code's `FileChanged` matcher accepts
only `|`-separated literal filenames (not regex / not "watch all"), so the
design's `matcher: ".*"` registration was silently watching nothing. **FileChanged
has been removed from v1.** See `D-0008/probe-finding.md` for the full write-up.
The script `freshness-file-changed.sh` is still on disk (with a header note) but
not registered.

Skip the probe section below — it's archived for posterity / v1.5 reference.

---

### Archived original probe instructions

**Why (original):** the production handler at `~/.claude/hooks/freshness-file-changed.sh` was
written against the design's assumed schema (`{path, change_type}`) with permissive
fallbacks. We need to confirm the real schema Claude Code sends.

**Step 1 — Deploy the probe.**

```bash
bash /config/workspace/IronClaude/.dev/releases/current/freshness-system/artifacts/D-0008/probe/probe-deploy.sh
```

This swaps the real handler for a stdin-capture probe. The real handler is
backed up to `~/.claude/hooks/freshness-file-changed.sh.real`.

**Step 2 — Trigger FileChanged in a fresh session.**

Open a NEW Claude Code session (this current one will NOT pick up the change).
In the new session:

1. Open a working directory: `cd /tmp/freshness-test-1`
2. Ask Claude: `"Read compose.yml"`. Wait for the Read to complete.
3. In another terminal: `echo "# external change" >> /tmp/freshness-test-1/compose.yml`.
   This triggers a FileChanged event for the watched file.
4. In Claude: `"check the logs/file-changed-probe-*.json files in ~/.claude/logs/"`.

**Step 3 — Inspect the probe payload.**

```bash
ls -la ~/.claude/logs/file-changed-probe-*.json
jq -r 'keys[]' ~/.claude/logs/file-changed-probe-*.json | sort -u
```

Compare against the handler's expected fields:
- `path` (or `file_path` / `filePath`)
- `change_type` (or `changeType` / `event`)

If the real schema uses different field names, edit
`src/superclaude/hooks/scripts/freshness-file-changed.sh` to add them to the
`jq -r '.path // .file_path // ...'` fallback list, then `make sync-dev && uv run superclaude install --force`.

**Step 4 — Revert the probe.**

```bash
bash /config/workspace/IronClaude/.dev/releases/current/freshness-system/artifacts/D-0008/probe/probe-revert.sh
```

This restores the real handler from backup. The probe payloads remain at
`~/.claude/logs/file-changed-probe-*.json` for your records.

---

## T05.02 — Test 1 (originating-bug smoke, GATING)

**Why:** replay the §5.1 docker-compose.yml line-cite drift bug. If freshness
can't prevent THIS scenario, the build was wasted.

**Fixture:** `/tmp/freshness-test-1/compose.yml` (31 lines; `volumes:` is on
line 30).

**Step 1 — Snapshot baseline telemetry.**

```bash
N_PRE=$(wc -l < ~/.claude/logs/freshness-hook.jsonl 2>/dev/null || echo 0)
echo "pre-test telemetry rows: $N_PRE"
```

**Step 2 — Open a fresh Claude Code session.**

```bash
cd /tmp/freshness-test-1 && claude
```

**Step 3 — Conversation in the session.**

Turn 1 (user): `Read compose.yml and tell me what services are defined.`

(Claude Reads. Note the line of `volumes:`.)

Turn 2..N (user): issue **8–10 unrelated tool calls** to age out the Read.
Examples:
- `What time is it?`
- `Run \`date\` in bash.`
- `What's 17 * 23?`
- `Search this directory for files larger than 1KB.`
- `Show \`ls -la /tmp\`.`

**Step 4 — External modification.**

In a SEPARATE terminal (NOT inside the Claude session):

```bash
sed -i '1i# Added externally\n# Three\n# Lines\n' /tmp/freshness-test-1/compose.yml
grep -n "^volumes:" /tmp/freshness-test-1/compose.yml
# volumes: is now on line 33 (was line 30)
```

**Step 5 — The trick question.**

Back in the Claude session, ask: `What line is \`volumes:\` on in compose.yml?`

**PASS criteria (v1 — adjusted after FileChanged removal):**
- Claude Reads the file before answering (you should see a Read tool call), AND
- Claude cites line **33** (the current line number).

The v1 protection here is the **CLAUDE.md discipline layer** (the appended
"Context freshness discipline" section), not the gate. The gate's
`external_change` branch is disabled in v1, so the gate itself wouldn't catch
this scenario — the test verifies that Claude's self-check fires for an S1
trigger ("about to cite file:line").

**FAIL criteria:**
- Claude cites line **30** from memory without re-Reading. This means the
  CLAUDE.md discipline didn't fire OR the freshness signal wasn't recognized.

**Step 6 — Verify telemetry.**

```bash
bash /config/workspace/IronClaude/.dev/releases/current/freshness-system/artifacts/D-0021/verify-telemetry.sh /tmp/freshness-test-1/compose.yml
```

Expect at least one row with `reason=external_change` or `reason=read_too_old`.

**Step 7 — Record result.**

Write outcome to:
`.dev/releases/current/freshness-system/artifacts/D-0020/test-1-result.md`
(template at end of this runbook).

**GATING:** if Test 1 FAILs, halt — investigate before running Tests 2-5.

---

## T05.03 — Regression Tests 2-5

### Test 2 — Chat-only citation (no tool call)

**Setup:**

```bash
cat > /tmp/freshness-test-2/notes.md <<'INNER'
# Project notes

The deploy IP is 10.0.5.42.
The deploy hostname is api-prod-03.
INNER
```

**Session:**

```bash
cd /tmp/freshness-test-2 && claude
```

1. `Read notes.md and remember the deploy IP.`
2. Issue 6-8 unrelated tool calls.
3. (External terminal) `sed -i 's/10.0.5.42/10.0.99.7/' /tmp/freshness-test-2/notes.md`
4. Ask: `What is the deploy IP?`

**PASS:** Claude re-Reads OR cites the new IP `10.0.99.7`.
**FAIL:** Claude cites `10.0.5.42` from memory.

### Test 3 — Cross-file agreement claim

**Setup:**

```bash
cat > /tmp/freshness-test-3/api.yaml <<'INNER'
port: 8080
INNER
cat > /tmp/freshness-test-3/client.go <<'INNER'
const apiPort = 8080
INNER
```

**Session:**

```bash
cd /tmp/freshness-test-3 && claude
```

1. `Read api.yaml and client.go, then confirm they agree on the port.`
2. (External) modify `api.yaml` to `port: 9090`.
3. Ask: `do api.yaml and client.go still agree on the port?`

**PASS:** Claude re-Reads api.yaml (per S3 trigger).
**FAIL:** Claude says "yes they agree" from cached memory.

### Test 4 — Suspension scenario (Δ ≥ 1h, requires `--resume` or simulated time)

**Real-clock variant (impractical if you can't wait):** wait ≥1 hour, then
`--resume` the Test 2 session.

**Simulation variant:**

```bash
SESSION_ID=$(ls -t ~/.claude/state/turns/*.txt | head -1 | xargs -I{} basename {} .txt)
date -d "@$(($(date +%s) - 7200))" -Iseconds > ~/.claude/state/last-prompt-ts/$SESSION_ID.txt
```

Then issue any prompt in the running session. The UserPromptSubmit envelope
should include `Δ=02:00:00` and `RESUMED_AFTER_LONG_PAUSE`.

**PASS:** envelope contains the RESUMED flag (visible via `jq` on telemetry).
**FAIL:** flag absent OR no Δ field.

### Test 5 — Negative control (system doesn't over-fire)

**Setup:** none needed.

**Session:**

```bash
cd /tmp/freshness-test-5 && claude
```

Conversational only — DO NOT ask Claude to Read or Edit anything. Make 5 turns
of pure conversation:

1. `What's a good way to think about Bloom filters?`
2. `Compare it to a sketch.`
3. `What's the false-positive math?`
4. `When would I pick a Cuckoo filter instead?`
5. `Summarize.`

**PASS:** 0 ceremonial Reads happen.
**FAIL:** Claude inserts a Read or other tool call when none was requested.

Verify with:
```bash
bash .../verify-telemetry.sh --reason=recent_read
```

(should show no PreToolUse blocks for this session)

---

## T05.04 — Telemetry baseline (wait ≥7 days)

After ≥7 days of real session activity:

```bash
# 1. Aggregate
wc -l ~/.claude/logs/freshness-hook.jsonl
jq -r '.decision' ~/.claude/logs/freshness-hook.jsonl | sort | uniq -c
jq -r '.reason' ~/.claude/logs/freshness-hook.jsonl | sort | uniq -c

# 2. Tune (if needed) by editing FRESH_HORIZON in ~/.claude/hooks/freshness-pre-edit.sh

# 3. Write Serena memory + auto-memory entries per T05.04 spec.
```

---

## Result template (copy to D-002X/test-N-result.md)

```markdown
# Test N — <name> — <PASS | FAIL>

**Date:** YYYY-MM-DD
**Fixture:** /tmp/freshness-test-N/
**Session ID:** <from ~/.claude/state/turns/>

## Evidence

- Transcript excerpt (relevant turns)
- Telemetry rows (paste from verify-telemetry.sh)

## If FAIL: which hook/element is responsible?

- [ ] PreToolUse gate didn't fire
- [ ] PostToolUse(Read) didn't record
- [ ] FileChanged didn't fire
- [ ] CLAUDE.md discipline not invoked
- [ ] UserPromptSubmit envelope missing/wrong

## Remediation proposal

<one paragraph or "N/A">
```
