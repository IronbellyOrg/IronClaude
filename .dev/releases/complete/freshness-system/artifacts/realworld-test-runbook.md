# Real-World Test Runbook — Freshness System v1

Step-by-step guide for running `freshness-realworld-test.sh` and interpreting
the results.

## What this test does (and doesn't)

Each scenario spawns a real Claude Code session via `claude -p` and observes:
- What Claude does (response content, tools called)
- What the hooks observed (new telemetry rows, state-file mutations)
- Whether Claude's behavior matches the expected v1 contract

This is the test that catches the things `freshness-test-suite.sh` (the unit
test) cannot: Claude Code firing the hooks, the assistant respecting exit 2,
the `<session-context>` envelope reaching the assistant's view.

## Pre-flight

```bash
# Are the hooks installed?
ls ~/.claude/hooks/freshness-*.sh
# Expect: 7 files (freshness-session-start, -user-prompt, -pre-edit, -post-read,
# -file-changed, -subagent-start, -subagent-stop)

# Are they registered in settings.json?
jq -r '.hooks | keys[]' ~/.claude/settings.json
# Expect: PostToolUse, PreToolUse, SessionStart, SubagentStart, SubagentStop, UserPromptSubmit
# (FileChanged should NOT be present — see CHANGELOG v1 known limitation)

# Snapshot the telemetry log size so you can see what's "new" after the test
PRE_ROWS=$(wc -l < ~/.claude/logs/freshness-hook.jsonl 2>/dev/null || echo 0)
echo "Telemetry baseline: $PRE_ROWS rows"
```

If any of these fails, run `cd /config/workspace/IronClaude && make sync-dev && uv run superclaude install --force` first.

## Cost estimate

Each scenario is capped at $2 via `--max-budget-usd 2`. Typical actual usage:
- Scenario 1 (read-only, short): ~$0.10–0.30
- Scenario 2 (block-then-recover, multi-step): ~$0.30–0.80
- Scenario 3 (envelope quote, short): ~$0.05–0.20
- Scenario 4 (state init, trivial): ~$0.05–0.15
- Scenario 5 (Task subagent): ~$0.50–1.50

**Total realistic: $1–3 for all five.**

## Quick run

```bash
.dev/releases/current/freshness-system/artifacts/freshness-realworld-test.sh
```

Runs all 5 scenarios sequentially, cleans up synthetic session state at the
end, prints a summary. Exit 0 if all pass, 1 if any fail.

For one scenario at a time, replace with the scenario number:

```bash
.dev/releases/current/freshness-system/artifacts/freshness-realworld-test.sh 2
```

## Per-scenario walkthrough

### Scenario 1 — Read-only request

**Question being answered:** when Claude is asked to Read a file (no edit),
does `PostToolUse(Read)` actually fire and record the Read in `reads.jsonl`?
Does the gate stay quiet?

**Command:**

```bash
.dev/releases/current/freshness-system/artifacts/freshness-realworld-test.sh --verbose 1
```

**What the script does behind the scenes:**

1. Creates `/tmp/rwtest1-XXXX/notes.txt` containing `Port: 8080` and other fields
2. Generates a fresh UUID for `--session-id`
3. Invokes:
   ```
   claude -p --session-id <UUID> --add-dir /tmp/rwtest1-XXXX \
     --dangerously-skip-permissions --output-format json \
     --max-budget-usd 2 --no-session-persistence \
     "Read the file /tmp/rwtest1-XXXX/notes.txt and tell me what port the project uses. Don't edit anything."
   ```
4. Parses the JSON response and the new telemetry rows for this UUID

**Expected PASS output (abbreviated):**

```
=== Scenario 1: Read-only request ===
  → claude -p --session-id 7a4b… --add-dir /tmp/rwtest1-AB12
    prompt: Read the file …notes.txt and tell me what port the project uses. …
    ✓ response mentions port 8080 contains '8080'
    ✓ reads.jsonl rows for this session = 1 (≥ 1)
    ✓ PreToolUse rows for this session = '0'
    PASS
```

**What PASS means:**
- Claude actually used the Read tool (`reads.jsonl` gained a row for this session)
- The session-context envelope correctly told Claude not to need re-Reads after the fresh Read (no `PreToolUse` blocks fired)
- Claude correctly extracted "8080" from the file content

**What FAIL would tell you:**
- "response does NOT contain 8080" → either Claude didn't Read the file at all, or Read failed
- "reads.jsonl rows = 0" → `freshness-post-read.sh` didn't fire (matcher misconfigured? script not executable?)
- "PreToolUse rows ≥ 1" → the gate fired during a no-Edit prompt (matcher too broad?)

---

### Scenario 2 — Stale-read forces block-then-recover (the canonical test)

**Question being answered:** when the freshness gate sees a Read that's older
than the 30-minute horizon, does it block the Edit with `read_too_old`, and
does Claude recover by re-Reading?

**Why this scenario, not the obvious "Edit without Read" scenario:** earlier
versions of this test tried "Edit a file you haven't Read yet → expect
no_prior_read block". That scenario passed in spirit but didn't fire the
block path, because Claude Code's built-in Edit/Write tools require a prior
Read in the conversation (the tool description says: "This tool will error
if you attempt an edit without reading the file first"). So Claude always
Reads first, and the gate's allow path fires immediately. The freshness gate
is a **safety net BELOW Claude's own discipline** — to exercise the block
path, we need a scenario where Claude HAS Read (so the Edit tool's check
passes) but the gate's specific conditions still trigger a block.

The realistic v1 trigger is **`read_too_old`**: Claude Read the file in a
prior turn, then time passed beyond the 30-min horizon, then Claude tries
to Edit. The Edit tool's "Read once in conversation" check passes (because
Claude's conversation memory holds the Read), but the gate sees the stale
`reads.jsonl` entry and blocks.

**Command:**

```bash
.dev/releases/current/freshness-system/artifacts/freshness-realworld-test.sh --verbose 2
```

**What the script does (3 steps within one scenario):**

1. **Turn 1**: spawns `claude -p --session-id <UUID>` with prompt "Read X and tell me the first word." Claude Reads; `reads.jsonl` gains a row.
2. **Backdate**: uses `jq` to mutate that row's `ts_unix` to 7200 seconds ago (atomic in-place rewrite).
3. **Turn 2**: spawns `claude -p --resume <UUID>` (same session, conversation memory carries over) with prompt "Now edit X to change 'hello' to 'howdy'." Expected Claude flow:
   - Claude calls Edit (tool's built-in Read-check passes because turn 1 had a Read)
   - PreToolUse hook fires; gate sees `reads.jsonl` entry is 7200s old → exits 2 with `read_too_old` message
   - Claude sees the stderr, calls Read again → fresh `reads.jsonl` row
   - Claude retries Edit → gate allows (`recent_read`)
   - Edit applies; file content changes

**Expected PASS output:**

```
=== Scenario 2: Stale-read forces block-then-recover (read_too_old) ===
  step 1/3 Claude Reads the file (turn 1)
    ✓ reads.jsonl rows for this session after Read = 1 (≥ 1)
  step 2/3 Backdate the Read timestamp by 7200s (forces read_too_old)
  step 3/3 Resume same session, request Edit
    --- turn 2 response (first 400 chars) ---
    Done.
    --- end ---
    ✓ file content changed contains 'howdy'
    ✓ block rows (read_too_old) in turn 2 = 1 (≥ 1)
    ✓ allow rows (recent_read) after recovery = 1 (≥ 1)
    --- All turn-2 telemetry rows for <UUID>: ---
    {"decision":"block","reason":"read_too_old","tool":"Edit","path":"…","recent_read_age_sec":7200}
    {"decision":"allow","reason":"recent_read","tool":"Edit","path":"…","recent_read_age_sec":3}
    PASS
```

**What PASS means:**
- The gate's `read_too_old` branch fires correctly (block + factual stderr)
- Claude understands the stderr and corrects course (re-Reads the file)
- The post-Read state heals the gate's view (retried Edit allowed)
- The full block-then-recover loop works end-to-end in production

**What FAIL would tell you:**
- "file content does NOT contain 'howdy'" → Claude gave up after the block instead of retrying. Check that `~/.claude/CLAUDE.md` "Context freshness discipline" section is present and intact (Claude needs to understand the stderr).
- "block rows (read_too_old) = 0" → either the gate's `read_too_old` branch isn't firing (likely `freshness-pre-edit.sh` has a bug in its Δ math or horizon constant), OR Claude pre-emptively Re-Read before its first Edit attempt (which would make `recent_read_age_sec` low and the gate allow). Inspect telemetry: if you see only allow rows, Claude re-Read pre-emptively — that's still a working system, but the test couldn't verify the block path.
- "allow rows = 0" → gate blocked but Claude didn't recover. Either the stderr message is wrong, or Claude isn't seeing it, or CLAUDE.md discipline isn't loaded.
- "reads.jsonl rows after Read = 0" → turn 1 didn't fire `freshness-post-read.sh`. Check the PostToolUse matcher in settings.json.

**Cost:** ~$0.50–1.50 (two `claude -p` calls; both small).
- "allow rows = 0" → Read happened but the gate still blocked on retry. Bug in the recent_read branch logic, or `reads.jsonl` wasn't appended.

**This is the single most important test in the suite.** If only one passes, this should be it.

---

### Scenario 3 — Envelope visibility

**Question being answered:** does the `<session-context>` block injected by
`freshness-user-prompt.sh` actually reach the assistant's prompt context?

**Command:**

```bash
.dev/releases/current/freshness-system/artifacts/freshness-realworld-test.sh --verbose 3
```

**What happens:**

1. Prompt: "Without using any tools, tell me exactly what the value of 'turn=' is in the `<session-context>` block injected before this prompt. Reply with just the number, nothing else."
2. Claude should be able to see (via its prompt context) the envelope text and quote `1` (this is turn 1).

**Expected PASS output:**

```
=== Scenario 3: Envelope visibility ===
  → claude -p --session-id 1d8f… --add-dir /tmp/rwtest3-EF56
    prompt: Without using any tools, tell me exactly what the value of 'turn=' …
    --- response ---
    1
    --- end ---
    ✓ response cites turn=1
    PASS
```

**What PASS means:**
- `freshness-user-prompt.sh` is firing on every prompt
- Its stdout JSON `hookSpecificOutput.additionalContext` is being injected into Claude's view
- Claude can read and quote from the envelope (the discipline layer has the data it needs)

**What FAIL would tell you:**
- "response did NOT cite turn=1" → either the hook isn't firing, OR its output isn't being injected, OR Claude doesn't see it in its prompt context. Run `tail -F ~/.claude/logs/freshness-hook.jsonl` and re-test interactively to triage.

**Heads-up:** this scenario is the most subjective — Claude might phrase its
answer in unexpected ways ("Turn number is 1", "1", "Turn: 1"). The check is a
regex word-boundary `\b1\b` which is loose. If Claude refuses to introspect
or hallucinates a different number, it FAILs.

---

### Scenario 4 — Fresh-session state initialization

**Question being answered:** when a new session starts (the very first user
prompt), does `freshness-session-start.sh` create the per-session state
files (`turns/<uuid>.txt`, `tool-call-counter/<uuid>.txt`, `bg-agents/<uuid>.txt`)?

**Command:**

```bash
.dev/releases/current/freshness-system/artifacts/freshness-realworld-test.sh --keep-state 4
```

(The `--keep-state` flag retains the synthetic session's state files for
inspection after the test.)

**Expected PASS output:**

```
=== Scenario 4: Fresh-session state initialization ===
  → claude -p --session-id 5a9c… --add-dir /tmp/rwtest4-GH78
    prompt: Reply with 'ok' and nothing else.
    ✓ turns/5a9c….txt exists
    ✓ tool-call-counter/5a9c….txt exists
    ✓ bg-agents/5a9c….txt exists
    ✓ turn counter after 1 user prompt = '1'
    PASS
```

**After PASS, manually inspect:**

```bash
SID=<the UUID printed in the test output>
ls -la ~/.claude/state/{turns,tool-call-counter,bg-agents}/$SID.txt
cat ~/.claude/state/turns/$SID.txt    # expect: 1
```

**What FAIL would tell you:**
- "turns/<uuid>.txt MISSING" → `freshness-session-start.sh` did not create state, OR was not invoked. Check the file is executable, jq is installed, and the SessionStart matcher in settings.json is `*` or `startup|resume`.
- "turn counter ≠ 1" → either UserPromptSubmit didn't fire, OR the counter starts somewhere weird. Walk through the script logic.

---

### Scenario 5 — Subagent counter

**Question being answered:** does the Task tool actually trigger `SubagentStart`/`SubagentStop` events?

**Command:**

```bash
.dev/releases/current/freshness-system/artifacts/freshness-realworld-test.sh --verbose 5
```

**What happens:**

1. Prompt: "Use the Task tool with subagent_type 'general-purpose' to count the number of files in $fixture. Then tell me the count. Use exactly one Task call."
2. Expected: SubagentStart fires (counter 0→1), the Task agent runs and completes, SubagentStop fires (counter 1→0).
3. After `claude -p` returns (Task agent finished), counter should be 0.

**Expected PASS output:**

```
=== Scenario 5: Subagent counter ===
  → claude -p --session-id 2f7b… --add-dir /tmp/rwtest5-IJ90
    prompt: Use the Task tool with subagent_type 'general-purpose' to count …
    ✓ bg-agents counter after Task completion = '0'
    PASS
```

**What FAIL would tell you:**
- "counter = 1" → SubagentStart fired but SubagentStop didn't. Check the registration of SubagentStop in settings.json.
- "counter = ?" (empty file) → neither event fired, OR no Task was used by Claude. Re-run with `--verbose` and inspect Claude's response — did it actually invoke Task?
- "counter = -1" → there's a sign bug in subagent-stop.sh (should be impossible per the floor-at-0 design, but worth a check). Run unit-test scenario 12 to confirm: `freshness-test-suite.sh 12`.

**Caveat:** the most expensive scenario (~$0.50–1.50). Skip via `1 2 3 4` if budget is tight.

---

## Forensics: what to do when a scenario fails

### Inspect telemetry filtered by failed session_id

The test prints the UUID at the top of each scenario:
```
  → claude -p --session-id <UUID>
```

Then:

```bash
SID=<that UUID>
jq -c --arg s "$SID" 'select(.session_id == $s)' ~/.claude/logs/freshness-hook.jsonl
```

You'll see every gate decision Claude triggered, with timestamps and reasons.

### Inspect Claude's actual response (full text, not just our assertion)

Re-run with `--verbose`:

```bash
.dev/releases/current/freshness-system/artifacts/freshness-realworld-test.sh --verbose <N>
```

### Inspect state files for that session

```bash
SID=<that UUID>
for d in turns last-prompt-ts bg-agents tool-call-counter; do
    echo "--- $d ---"
    cat ~/.claude/state/$d/$SID.txt 2>/dev/null || echo "(missing)"
done
```

### Reproduce the prompt manually (in an interactive session)

For each scenario, the test prints the exact prompt and session-id flags.
You can replay them by hand in a fresh interactive session to watch Claude's
turn-by-turn behavior:

```bash
cd <fixture_dir>
claude --session-id <new-uuid> --add-dir <fixture_dir> --dangerously-skip-permissions
# Then paste the prompt
```

Set `tail -F ~/.claude/logs/freshness-hook.jsonl` in another terminal to watch
telemetry rows land in real time.

## Summary expected outcomes

| # | Scenario | Validates | If FAIL |
|---|---|---|---|
| 1 | Read-only | Read tracker fires, gate quiet | Hook script broken or matcher wrong |
| 2 | Block-then-recover | Full block→retry loop end-to-end | Gate / Claude communication broken |
| 3 | Envelope visibility | UserPromptSubmit envelope reaches Claude | `additionalContext` mechanism broken |
| 4 | Fresh-session init | SessionStart creates state files | session-start script broken or skipped |
| 5 | Subagent counter | SubagentStart/Stop fire on Task | Task tool not triggering events as expected |

**If all 5 pass:** the v1 system is doing exactly what it's documented to do.

**If only Scenario 2 passes:** you have a working gate + recovery loop —
the most important guarantee. The other tests are nice-to-haves.

**If Scenario 2 fails but 1, 3, 4 pass:** the hooks fire correctly but Claude
isn't recovering from blocks. Likely cause: stderr message phrasing or
CLAUDE.md discipline section misalignment. Read `~/.claude/CLAUDE.md` and
confirm the "Context freshness discipline" section is present and intact.

## After the test

Append the test run to your project's incident log if anything failed:

```bash
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) realworld-test run: PASS=$PASS FAIL=$FAIL" \
    >> .dev/releases/current/freshness-system/realworld-test-log.txt
```

Or commit the test artifact if you're capturing a "this passed" milestone:

```bash
cd /config/workspace/IronClaude
git add .dev/releases/current/freshness-system/realworld-test-log.txt
```

## Where to put the v1.5 fixes when a test surfaces something

Edit `CHANGELOG.md` → `### v1.5 work items (freshness-system)` and add a
specific entry. The probe-finding.md template shows the format.
