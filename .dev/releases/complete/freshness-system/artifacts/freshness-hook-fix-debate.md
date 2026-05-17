# Freshness Pre-Edit Hook — Create-Case Bug Fix Debate

**Author:** debate-orchestrator (sc:adversarial, read-only research)
**Date:** 2026-05-15
**Scope:** Decide between two distinct fixes for the catch-22 in
`src/superclaude/hooks/scripts/freshness-pre-edit.sh` that blocks `Write` of a
brand-new file because no prior `Read` exists, then blocks the `Read` because
the file does not exist.

> **Live confirmation:** while writing this very document the orchestrator
> itself was caught by the bug — the first `Write` was rejected by
> `freshness-pre-edit.sh` with `"You have not Read \`<path>\` in this session.
> Read it before editing."` and required the same `touch -> Read -> Write`
> workaround the phase-6 agent used. The bug is reproducible on demand.

---

## Evidence Summary (read-only)

Both hook copies confirmed byte-identical (the project-local
`/config/.claude/hooks/freshness-pre-edit.sh` and the source-of-truth
`/config/workspace/IronClaude/src/superclaude/hooks/scripts/freshness-pre-edit.sh`),
so a single edit at source plus `make sync-dev` covers both.

Confirmed structure of the hook:

- Lines 6-21 — setup, `set -u`, paths, jq parses of `session_id`, `tool_name`, `cwd`.
- Lines 23-38 — target-path extraction. If neither `file_path` nor `relative_path`
  is present, the hook fails open (exit 0) with a stderr note.
- Lines 64-70 — pulls `LAST_READ_TS_UNIX` from `~/.claude/state/reads.jsonl` for this
  session and target.
- **Lines 72-78 — the bug**: if `LAST_READ_TS_UNIX <= 0` the decision is `block` /
  `no_prior_read`. This branch has zero awareness of whether `$TARGET` exists on
  disk. The block fires identically for an edit to an existing file the agent never
  read AND for a create of a brand-new file.
- Lines 99-110 — telemetry write to `~/.claude/logs/freshness-hook.jsonl`. Fields:
  `ts, event, tool, path, session_id, tool_call_idx, recent_read_age_sec,
  external_change_seen, decision, reason`.
- Lines 113-125 — block branch: `exit 2` after emitting the stderr message
  `"You have not Read \`$TARGET\` in this session. Read it before editing."`.

The hook is bound (`src/superclaude/hooks/hooks.json` lines 35-46) to:
`Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol`.
`Write` is part of the matcher set; serena's `insert_*_symbol` and
`replace_symbol_body` also imply an existing file, but `Write` does not.

Design intent is documented as "fail-open per NFR-3" at the top of every hook
(line 4 of `freshness-pre-edit.sh`, plus matching NFR-3 callouts in
`freshness-session-start.sh` and `freshness-user-prompt.sh`).

**Smoking gun in the release archive:**
`.dev/releases/complete/freshness-system/checkpoints/CP-P05-T05.01.md` line 27
(finding F10):

> The freshness gate fires on `Write` to nonexistent files (e.g., creating fresh
> fixture files). Triggers `no_prior_read` because no Read tracker exists. This
> is correct per the design (the gate doesn't know if a file exists) but may
> surprise users creating new files in fresh sessions. — **Action: v1.5
> refinement: allow `Write` when target path doesn't exist. Out of v1 scope;
> document in user-guide FAQ.**

So this is a known deferred bug, not a hidden one. Phase 6 of
`task-sc-task-directional-merge` hit the deferred case and the sprint monitor
(`src/superclaude/cli/sprint/monitor.py:143` regex
`_NONZERO_EXIT_CODE_RE = re.compile(r'exit[_ ]code["\']?\s*[:=]\s*([1-9]\d*)')`)
escalated the resulting `exit_code: 2` text in tool error messages to phase
failure (exit_code=1 from the sprint).

The post-read tracker (`freshness-post-read.sh`) writes JSONL rows with
`{ts, ts_unix, session_id, path, tool_call_idx}` to `~/.claude/state/reads.jsonl`.
Read entries use the absolute `tool_input.file_path` as `path` — this matters for
Proposal B's tracker semantics.

Tests currently in `tests/cli/test_install_hooks.py` only cover the installer's
JSON merge logic; **there are no behavior tests for the bash hook itself**, so
either proposal will require new test infrastructure (a bash test script
shelling stdin JSON into the hook and asserting exit code + stderr +
telemetry).

---

## Proposal A — Direct script-level "create-case fail-open" branch

**Family:** patch the bash script's `no_prior_read` branch with an existence
check.

**One-line summary:** In `freshness-pre-edit.sh`, before declaring
`no_prior_read`, test whether `$TARGET` exists on disk. If it does not, the
operation is a *create*, not an *edit*; fail open with a new telemetry reason
`create_allowed`.

### Files edited

| Path | Source-of-truth | Dev copy |
|---|---|---|
| `src/superclaude/hooks/scripts/freshness-pre-edit.sh` | yes | no — dev copy is `.claude/hooks/freshness-pre-edit.sh` deposited by `superclaude install` / `make sync-dev` |

After editing the source-of-truth, run `make sync-dev` to update the dev copy at
`.claude/hooks/freshness-pre-edit.sh` and the user copy at
`/config/.claude/hooks/freshness-pre-edit.sh` (the latter is the same destination
the installer writes to in practice).

### Diff-level changes

Current lines 72-78:

```bash
72  DECISION="allow"
73  REASON="recent_read"
74  READ_AGE="null"
75
76  if [ "$LAST_READ_TS_UNIX" -le 0 ] 2>/dev/null; then
77      DECISION="block"
78      REASON="no_prior_read"
```

Replace with:

```bash
72  DECISION="allow"
73  REASON="recent_read"
74  READ_AGE="null"
75
76  if [ "$LAST_READ_TS_UNIX" -le 0 ] 2>/dev/null; then
77      # NFR-3 fail-open: a Write to a path that does not yet exist is a
78      # create, not an edit. The freshness gate is meaningless when there is
79      # no prior state to be stale relative to.
80      if [ ! -e "$TARGET" ]; then
81          DECISION="allow"
82          REASON="create_allowed"
83      else
84          DECISION="block"
85          REASON="no_prior_read"
86      fi
```

And in the stderr message block (current line 116) — no change needed; the
`no_prior_read` arm continues to print the same message because we only reach
that arm when `$TARGET` exists. Add a new comment above the case to document
intent, but no new case arm is needed (allow path doesn't print stderr).

### Required test changes

Three concerns to cover. Create a new file
`tests/hooks/test_freshness_pre_edit.sh` (a bats- or plain-bash-style test
script invoked from a pytest wrapper) since `tests/cli/test_install_hooks.py`
is the wrong layer.

Minimal pytest wrapper at `tests/hooks/test_freshness_pre_edit_create_case.py`:

```python
"""Behavioral tests for freshness-pre-edit.sh create-vs-edit distinction."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "src" / "superclaude" / "hooks" / "scripts" / "freshness-pre-edit.sh"


def _run_hook(payload: dict, fake_home: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["HOME"] = str(fake_home)
    (fake_home / ".claude" / "state").mkdir(parents=True, exist_ok=True)
    (fake_home / ".claude" / "logs").mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        env=env,
        timeout=5,
    )


def test_write_to_nonexistent_file_allows(tmp_path):
    target = tmp_path / "brand-new-file.md"
    assert not target.exists()
    payload = {
        "session_id": "test-create-case",
        "tool_name": "Write",
        "tool_input": {"file_path": str(target)},
        "cwd": str(tmp_path),
    }
    result = _run_hook(payload, fake_home=tmp_path / "home")
    assert result.returncode == 0, result.stderr.decode()
    telemetry = (tmp_path / "home" / ".claude" / "logs" / "freshness-hook.jsonl").read_text()
    assert '"reason":"create_allowed"' in telemetry
    assert '"decision":"allow"' in telemetry


def test_edit_to_existing_unread_file_still_blocks(tmp_path):
    target = tmp_path / "existing.md"
    target.write_text("seeded\n")
    payload = {
        "session_id": "test-edit-case",
        "tool_name": "Edit",
        "tool_input": {"file_path": str(target)},
        "cwd": str(tmp_path),
    }
    result = _run_hook(payload, fake_home=tmp_path / "home")
    assert result.returncode == 2
    assert b"You have not Read" in result.stderr
    telemetry = (tmp_path / "home" / ".claude" / "logs" / "freshness-hook.jsonl").read_text()
    assert '"reason":"no_prior_read"' in telemetry


def test_write_to_existing_unread_file_still_blocks(tmp_path):
    """Write to an EXISTING file is an edit, not a create — gate must hold."""
    target = tmp_path / "existing.md"
    target.write_text("seeded\n")
    payload = {
        "session_id": "test-write-edit-case",
        "tool_name": "Write",
        "tool_input": {"file_path": str(target)},
        "cwd": str(tmp_path),
    }
    result = _run_hook(payload, fake_home=tmp_path / "home")
    assert result.returncode == 2
    assert b"You have not Read" in result.stderr
```

Three test cases, ~70 LOC. Add `tests/hooks/__init__.py` (empty) if pytest
collection needs it. No changes to `tests/cli/test_install_hooks.py`.

### Re-sync instructions

```
# After editing src/superclaude/hooks/scripts/freshness-pre-edit.sh
make sync-dev
make verify-sync
uv run pytest tests/hooks/ -v
```

`make sync-dev` will refresh `.claude/hooks/freshness-pre-edit.sh`. For users
running this fix against an installed copy, `superclaude install -f` re-runs
`install_hooks` which `shutil.copy2`'s the new script over the old one
(`src/superclaude/cli/install_hooks.py` lines 197-199); `--force` is needed
because the file already exists.

### Behavior matrix

| Target exists | Prior read fresh | BEFORE | AFTER |
|---|---|---|---|
| Yes | Yes | allow (`recent_read`) | allow (`recent_read`) — unchanged |
| Yes | No (or `read_too_old` / `external_change`) | block (`no_prior_read` / `read_too_old` / `external_change`) | block — unchanged |
| No | N/A | block (`no_prior_read`) — **the bug** | allow (`create_allowed`) — **fixed** |
| No | N/A but TRACKER ROW STALE (path now absent, was read before deletion) | edge case below | edge case below |

Edge case: target was read earlier in the session, then deleted externally,
then a Write is attempted to recreate it. Under Proposal A, the path goes
through the `LAST_READ_TS_UNIX > 0` branch (Δ check + external_change check)
and either allows or blocks based on those signals — same as before. Proposal A
does not regress this case because `[ ! -e "$TARGET" ]` is only consulted
inside the `LAST_READ_TS_UNIX <= 0` arm.

### Backward-compatibility risk for in-flight sprints

Negligible. The only behavioral change is: blocked-create → allowed-create.
Any agent that previously triggered the catch-22 (Write → block → Read → fail
→ touch → Read → Write → success) now succeeds in one step. No previously
allowed call is now blocked. No telemetry field is removed (only `reason`'s
value space grows by one). Downstream consumers that whitelist `reason` values
must be updated (none in-repo do; grep for `create_allowed` returns zero).

### Performance impact

One additional `[ ! -e "$TARGET" ]` test per blocked-create call. `-e` is a
single `stat(2)` against `$TARGET`. This runs only on the *cold path* (no prior
read). Hook timeout in `hooks.json` is 1 second; current hot path already does
4 `jq` invocations and 1 `flock`-protected counter write, so an extra stat is
in the noise (~50 µs on a local fs).

### Telemetry impact

The JSONL emitted to `~/.claude/logs/freshness-hook.jsonl` gains one new
`reason` value: `create_allowed`. No new fields. No removed fields. Schema
backward-compatible. The downstream sprint summarizer (`monitor.py`,
`summarizer.py`) does not key off `reason`, only off the stderr "exit_code"
regex — and `create_allowed` is `exit 0` so it never trips that regex.

### Failure modes NOT fixed

1. Race condition: target does not exist at hook time, but a parallel process
   creates it before the Write lands. The Write then proceeds without a prior
   Read of the now-existing content. Quantifiably small risk (sub-millisecond
   window), and the read-too-old / external_change checks catch the same kind
   of staleness for subsequent edits.
2. Symlink with dangling target: `[ -e "$TARGET" ]` returns false for a
   symlink whose target is missing, so Write goes through. This is arguably
   correct (the agent is creating the dereferenced target) but worth noting.
3. The `serena` mcp tools in the matcher set (`insert_*_symbol`,
   `replace_symbol_body`) ALWAYS imply an existing file, so this proposal has
   no effect on them — correct, since those operations never create.
4. Bind-mount or container path where `[ -e ]` lies (e.g., `/proc/*` synthetic
   paths). Outside the hook's scope.

### Estimated effort & LOC

- Effort: **S**
- Lines of diff: **+7** in `freshness-pre-edit.sh` (one new `if` arm with
  comments), **~70 LOC** new test file.

---

## Proposal B — Move enforcement to the matcher: drop `Write` from `hooks.json`

**Family:** shift enforcement to the hook configuration layer; let bash logic
stay unchanged and let `Write` simply not invoke the gate.

**One-line summary:** In `src/superclaude/hooks/hooks.json`, replace the
PreToolUse matcher
`Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol`
with
`Edit|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol`.
The `Write` tool is no longer gated; the freshness assumption (Write is a
create OR a full-content overwrite where prior content is not depended on) is
encoded in the matcher.

### Files edited

| Path | Source-of-truth | Dev copy |
|---|---|---|
| `src/superclaude/hooks/hooks.json` | yes | yes — `.claude/settings.json` (but only on re-install / re-merge, since `install_hooks.py` does an *additive* merge with collision skipping) |

Critical wrinkle: `install_hooks._merge_settings` (lines 312-371) uses
`_registration_signature(reg) = (matcher, tuple-of-commands)` to detect
collisions. Changing the matcher string means the *new* signature won't match
the *old* one, so `install_hooks(force=False)` would APPEND the new
registration and leave the old one in place — both would fire (the old one
still gates `Edit|Write|...`, including Write). The correct re-install
incantation is `superclaude install -f` (force replace).

### Diff-level changes

In `src/superclaude/hooks/hooks.json` lines 35-46, change line 37:

```
36          "PreToolUse": [
37  -     "matcher": "Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol",
37  +     "matcher": "Edit|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol",
```

No shell script edits. The bash logic in `freshness-pre-edit.sh` is unchanged
because it is simply never invoked for `Write`.

### Required test changes

The `tests/cli/test_install_hooks.py` fixture (line 75-78) hardcodes the
existing matcher:

```python
"PreToolUse": [
    {
        "matcher": "Edit|Write",   # <-- this is the FIXTURE matcher, not the real one
        ...
```

This fixture is for *testing the merge*, not the real matcher, so the fixture
stays as-is. But three new tests are still needed:

1. A new test in `tests/cli/test_install_hooks.py` that loads the REAL
   `src/superclaude/hooks/hooks.json` (not the fake fixture) and asserts the
   matcher no longer contains `Write`. This is a regression guard.

2. A behavioral test verifying that `Write` to an existing-but-unread file is
   no longer gated. This is a *behavior change* relative to before: such Writes
   used to block, now they pass. Honest framing: this is *not* really a unit
   test of the matcher; matching happens in the Claude Code runtime, not in
   our code. The regression guard in test 1 is the only thing that *can* be
   tested in-repo without an end-to-end Claude Code fixture.

3. A test that verifies a re-install replaces the old matcher with the new
   one — this is the most important test because it covers the deployment
   hazard.

Total: ~40 LOC of tests, all in `tests/cli/test_install_hooks.py`. No new
test file. But the *real* assurance test (end-to-end against a live Claude
Code session) cannot be written in-repo.

### Re-sync instructions

```
# Edit src/superclaude/hooks/hooks.json
make sync-dev
make verify-sync
uv run pytest tests/cli/test_install_hooks.py -v

# For existing installs, users MUST run:
superclaude install -f
```

The `-f` is non-negotiable for existing installs because `install_hooks` would
otherwise append the new registration alongside the old, leaving the old
matcher (with `Write`) still active.

### Behavior matrix

| Target exists | Prior read fresh | Tool | BEFORE | AFTER |
|---|---|---|---|---|
| Yes | Yes | Edit | allow (`recent_read`) | allow (`recent_read`) — unchanged |
| Yes | No | Edit | block (`no_prior_read`) | block — unchanged |
| Yes | No | **Write** | block (`no_prior_read`) | **allow (hook not invoked)** — **behavior change** |
| Yes | Yes | Write | allow (`recent_read`) | **allow (hook not invoked)** — unchanged outcome, different mechanism (telemetry row no longer emitted) |
| No | N/A | Write | block (`no_prior_read`) — **the bug** | **allow (hook not invoked)** — **fixed** |
| Yes | No | serena `replace_symbol_body` | block | block — unchanged |

The third row is the controversial change: a `Write` to an existing
content-bearing file the agent never read is now allowed silently. The fresh
gate used to catch this; under Proposal B it does not.

### Backward-compatibility risk for in-flight sprints

**High.** Two distinct hazards:

1. **Deployment hazard.** Existing user installs have settings.json with the
   old `Edit|Write|...` matcher already merged. A simple `superclaude install`
   without `--force` will *append* the new `Edit|...` registration alongside
   the old one. Both fire; the old one still gates Write; the bug is not
   fixed. Users must run `superclaude install -f`, but `-f` also replaces any
   user customizations they have made to the freshness hook scripts
   (`_copy_scripts` line 193 honors `--force` to overwrite). This is a
   double-edged blade.

2. **Silent loss of enforcement.** Any agent that previously `Write`-stomps an
   existing file (overwriting unread content) used to get blocked. Now it
   succeeds. The original NFR-3 design intent says "fail-open" for state
   issues, not "fail-open for the Write tool wholesale." Proposal B converts a
   targeted fail-open (only when target absent) into a wholesale fail-open
   (the entire Write tool). This is a behavior regression for the
   already-existing edit-via-Write case, not just a fix for create.

### Performance impact

Slightly faster: every `Write` invocation now skips the hook entirely. No `jq`
invocations, no `flock`, no telemetry write. Saves ~5 ms per Write call. Over a
sprint with hundreds of Writes that adds up to ~1 s saved.

### Telemetry impact

`~/.claude/logs/freshness-hook.jsonl` no longer receives ANY rows where
`tool=Write`. This is a *removal* of a field-value (`tool=Write` rows just stop
appearing). Downstream tooling that aggregates Write-call timing or counts
loses this data. No in-repo consumer is affected (grep `"tool":"Write"`
returns no analytics use), but external dashboards built on this telemetry
might break silently.

### Failure modes NOT fixed

1. The Write-to-existing-unread case is now allowed, which is arguably *worse*
   than the create-case bug because it removes a legitimate safety check.
2. The same logical flaw recurs if a future tool with create-or-edit
   ambiguity (e.g., a new `mcp__serena__upsert_symbol`) is added to the
   matcher set — Proposal B does not address the underlying design pattern
   (target-existence ignorance in the gate).
3. The race condition described in Proposal A's failure-mode list — there
   isn't one here because the hook never runs for Write at all.

### Estimated effort & LOC

- Effort: **S** (the edit) + **M** (deployment communication / migration risk)
- Lines of diff: **+0/-0** real change (one line edited in `hooks.json`), but
  ~40 LOC of new test, plus a CHANGELOG entry explaining the
  `superclaude install -f` requirement, plus user-facing doc updates in
  `docs/user-guide/freshness-hooks.md`.

---

## Round 1 — Attacks

Each side raises three specific, citable weaknesses against the other.

### A → B (Proposal A's advocate critiques Proposal B)

**Attack A1: Proposal B silently weakens a real safety guarantee that has
nothing to do with the create-case bug.**

Concrete: under B, `Write` to an existing 500-line config file the agent
never read will silently succeed and clobber it. Cite hook matcher line 37 of
`src/superclaude/hooks/hooks.json` — `Write` was deliberately added to the
matcher set during phase 4 of the freshness-system release (see
`.dev/releases/complete/freshness-system/phase-4-tasklist.md`) precisely
because `Write` can be a full-content overwrite of an existing file, which is
*more* destructive than `Edit`. B reverses that decision without addressing
the design rationale.

*B's defense:* The freshness contract specifically covers
"edit-after-read-stale-content" cases. A `Write` is documented in
Claude Code's tool contract as a full-content overwrite; an agent should never
issue a Write to an existing file it hasn't read because nothing carries over.
B's argument is that the gate is the wrong layer to enforce this — agent
training / system prompt should be. **Partial concede:** B agrees the
existing-Write case is a real regression but argues the cost is acceptable.

**Attack A2: Proposal B has a deployment cliff that A does not.**

Concrete: cite `src/superclaude/cli/install_hooks.py` lines 312-371
(`_registration_signature` + matcher-collision logic). Existing user
installs have `Edit|Write|...` already merged. A non-`-f` `superclaude install`
will append, not replace. Users running the fix get a settings.json with TWO
PreToolUse registrations: the old one (with Write, still bug-fired) and the
new one (without Write). Both fire. The bug is unfixed in the most common
user-upgrade path. A has no such cliff — `make sync-dev` followed by
`superclaude install -f` for the script overwrite is a normal upgrade, and
even without `-f` the script copy is the only thing that matters; the
`settings.json` registration didn't change.

*B's defense:* Document the requirement in CHANGELOG and add a one-shot
migration probe to `superclaude install` that detects the old matcher and
forces replacement. **Concede:** this adds significant scope to B. B agrees A
has a cleaner upgrade path.

**Attack A3: Proposal B is untestable inside this repo.**

Concrete: the matcher is evaluated by Claude Code's runtime, not by any code
in `src/superclaude/`. The "test" in B is a static regression guard
(`assert "Write" not in matcher`) plus a doc-driven assumption. There is no
in-repo way to verify that Claude Code's matcher dispatcher actually skips
the hook for Write. End-to-end verification requires running an actual Claude
Code session. A's tests, by contrast, exercise the bash script directly via
`subprocess.run(["bash", str(HOOK)], ...)` and assert exit code + stderr +
telemetry — verifiable in CI.

*B's defense:* Static regression guards are common and adequate (cite
`tests/cli/test_install_hooks.py` test_smoke_install_then_reinstall_force as
precedent for static-config tests). **Partial concede:** B agrees the
behavioral assurance is weaker.

### B → A (Proposal B's advocate critiques Proposal A)

**Attack B1: Proposal A introduces a TOCTOU race.**

Concrete: between the `[ ! -e "$TARGET" ]` check on line 80 (proposed) and
the actual `Write` operation, another process can create the file. The hook
allows the Write believing it is a create; the Write then overwrites
unread-by-this-session content. Window is small but not zero — a typical
Claude Code Write spans network round-trip + tool invocation (~50-200 ms),
and any parallel SubagentStart or background process can create the file in
that window.

*A's defense:* The race window exists, but its real-world probability is
sub-percent (concurrent Subagent activity on the same path is rare; sprint
runs are mostly sequential). Even if the race fires, the next *Edit* on the
same path correctly hits the `read_too_old` / `external_change` branch
because the post-read tracker still has no row for this session. **Concede:**
the race exists; the operational risk is low.

**Attack B2: Proposal A adds a stat(2) on a path that may not exist on every
single edit invocation.**

Concrete: every `Edit|Write|serena_*` call on a path the session hasn't
read now incurs `[ ! -e "$TARGET" ]` (line 80 proposed). For deeply nested or
network-mounted paths (`/config/workspace/...` over a bind-mount, NFS, FUSE,
S3-FS), `stat(2)` can stall for hundreds of milliseconds. The hook timeout in
`hooks.json` is 1 second (line 44). A stalled stat eats the budget. The hot
path used to be 4 jq + 1 flock; now it's 4 jq + 1 flock + 1 stat — and the
stat is the most variable.

*A's defense:* Cite line 76 — the stat is inside the `LAST_READ_TS_UNIX <= 0`
arm, i.e., the *cold path*. Calls with a recent read never reach line 80. For
calls without a prior read, the stat is unavoidable for any
existence-aware fix. **Partial concede:** A admits some stall risk on FUSE /
NFS, but argues the cold-path frequency makes it acceptable.

**Attack B3: Proposal A leaves the matcher set unchanged and therefore
preserves a known design smell: `Write` is in the matcher even though
"freshness" for `Write` is semantically muddled.**

Concrete: cite the hook header (line 2 of `freshness-pre-edit.sh`):
`# PreToolUse(Edit-class) freshness gate per design §3.3`. The hook
self-describes as "Edit-class". `Write` is not Edit-class in the conventional
sense (Edit modifies, Write creates-or-overwrites). A's fix patches around
the matcher decision rather than confronting it. The deferred F10 finding
itself frames this as a v1.5 question: should Write be gated at all?

*A's defense:* The design intent in F10 explicitly says "**allow `Write` when
target path doesn't exist**" — not "remove `Write` from the matcher." A
implements F10 verbatim. **No concede.**

---

## Round 2 — Concessions

Each side names one piece of the other's proposal it would adopt in a hybrid.

### A's concession to B

A would adopt **B's static regression guard test** (re-purposed as a
"matcher pinning" test that asserts the matcher continues to include `Write`).
The test exists to prove the matcher list is what the design says it is.
Useful regardless of which proposal ships, because it pins the matcher
against accidental drift. Adopting it costs A approximately 5 LOC.

### B's concession to A

B would adopt **A's behavioral test harness** (the
`tests/hooks/test_freshness_pre_edit_create_case.py` pattern of running the
bash hook in a subprocess with a fake `$HOME` and asserting exit code +
stderr + telemetry). Even under B, there is value in having behavior tests
for the hook script — they catch any future bash regressions in `Edit` /
`serena_*` cases. Adopting it costs B approximately 70 LOC and a new test
file, but the infrastructure is reusable.

A noteworthy non-overlap: the *script edit* itself (A's only real change) and
the *matcher edit* (B's only real change) are not naturally compatible — if
you remove `Write` from the matcher (B) the script-edit (A) becomes dead code
for the `Write`-create case (it would still cover `Edit`-create, which is a
narrower case). A and B address overlapping but distinct surfaces.

---

## Verdict

### Scoring Rubric

`score = (correctness_for_create_case * no_regression_for_edit_case * testability) / (operational_complexity * lines_changed_index)`

All factors normalized to [0.0, 1.0] for the multiplicand and
operational_complexity, with lines_changed_index in `[1, 5]` (1 = trivial,
5 = significant).

| Factor | Proposal A | Proposal B | Rationale |
|---|---|---|---|
| Correctness for create-case | 0.95 | 1.00 | A: 0.95 (TOCTOU race on existence check). B: 1.00 (hook never fires, so no race). |
| No regression for edit-case | 1.00 | 0.50 | A: 1.00 (the `else` arm preserves exact prior behavior for the path-exists case). B: 0.50 (Write to existing unread file is now silently allowed — material regression). |
| Testability | 0.90 | 0.40 | A: 0.90 (bash-subprocess tests exercise the actual script behavior). B: 0.40 (only static regression guard testable in-repo; behavioral correctness depends on Claude Code runtime). |
| Operational complexity | 0.20 | 0.65 | A: 0.20 (single script edit + tests, normal `make sync-dev` flow). B: 0.65 (requires `superclaude install -f`, has migration cliff for existing users, doc updates, CHANGELOG note). Lower is better; numbers inverted in formula below. |
| Lines changed index | 1 | 1 | A: ~7 script LOC + 70 test LOC = 1. B: ~1 config LOC + 40 test LOC = 1. Roughly equivalent. |

Combined:

```
A_score = (0.95 * 1.00 * 0.90) / (0.20 * 1) = 0.855 / 0.20 = 4.275
B_score = (1.00 * 0.50 * 0.40) / (0.65 * 1) = 0.200 / 0.65 = 0.308
```

**Winner: Proposal A** (4.275 vs 0.308, a ~14x margin).

The decisive factors are *no_regression_for_edit_case* (B's blanket
fail-open for `Write` is a true regression on the unread-Write-to-existing-file
case) and *testability* (A is unit-testable in CI; B is only statically
guarded). Operational complexity also tilts strongly toward A — B's
deployment cliff with `superclaude install -f` makes it harder to roll out
correctly.

### Hybrid recommendation

Ship **Proposal A** with **B's static regression-guard test added** as a
defense-in-depth measure: pin the real-installed matcher in a test so that
nobody silently widens or narrows the gated tool set without explicit
intent. This is the concession A made in Round 2 and costs ~5 LOC.

---

## Implementation Spec (winner, ready for sc:implement)

### Step 1 — Edit the source-of-truth hook script

**File:** `/config/workspace/IronClaude/src/superclaude/hooks/scripts/freshness-pre-edit.sh`

**Old lines 72-78 (exact text):**

```bash
DECISION="allow"
REASON="recent_read"
READ_AGE="null"

if [ "$LAST_READ_TS_UNIX" -le 0 ] 2>/dev/null; then
    DECISION="block"
    REASON="no_prior_read"
```

**New lines 72-85 (exact text):**

```bash
DECISION="allow"
REASON="recent_read"
READ_AGE="null"

if [ "$LAST_READ_TS_UNIX" -le 0 ] 2>/dev/null; then
    # NFR-3 fail-open: a Write/Edit to a path that does not yet exist is a
    # create, not an edit. The freshness gate is meaningless when there is
    # no prior state to be stale relative to. Resolves F10 from
    # .dev/releases/complete/freshness-system/checkpoints/CP-P05-T05.01.md.
    if [ ! -e "$TARGET" ]; then
        DECISION="allow"
        REASON="create_allowed"
    else
        DECISION="block"
        REASON="no_prior_read"
    fi
```

(No changes to lines 79-128; the existing `else` branch with `read_too_old`
and `external_change` logic is unchanged, as is the stderr message block at
lines 113-125. The `no_prior_read` case in lines 114-116 still prints the
same stderr message because we only reach it when `$TARGET` exists.)

### Step 2 — Add behavioral tests for the hook script

**New file:** `/config/workspace/IronClaude/tests/hooks/__init__.py`

(empty file — touch the file; pytest collection needs it to treat the
directory as a test package)

**New file:** `/config/workspace/IronClaude/tests/hooks/test_freshness_pre_edit_create_case.py`

```python
"""Behavioral tests for freshness-pre-edit.sh.

Covers the create-vs-edit distinction added to resolve F10 from
.dev/releases/complete/freshness-system/checkpoints/CP-P05-T05.01.md.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

HOOK = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "hooks"
    / "scripts"
    / "freshness-pre-edit.sh"
)


def _run_hook(payload: dict, fake_home: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["HOME"] = str(fake_home)
    (fake_home / ".claude" / "state").mkdir(parents=True, exist_ok=True)
    (fake_home / ".claude" / "logs").mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        env=env,
        timeout=5,
    )


def test_write_to_nonexistent_file_allows(tmp_path: Path) -> None:
    """Create-case: Write to a path that does not exist is allowed."""
    target = tmp_path / "brand-new-file.md"
    assert not target.exists()
    payload = {
        "session_id": "test-create-case",
        "tool_name": "Write",
        "tool_input": {"file_path": str(target)},
        "cwd": str(tmp_path),
    }
    result = _run_hook(payload, fake_home=tmp_path / "home")
    assert result.returncode == 0, result.stderr.decode()
    telemetry = (
        tmp_path / "home" / ".claude" / "logs" / "freshness-hook.jsonl"
    ).read_text()
    assert '"reason":"create_allowed"' in telemetry
    assert '"decision":"allow"' in telemetry


def test_edit_to_existing_unread_file_still_blocks(tmp_path: Path) -> None:
    """Edit-case: existing file without prior Read still blocks (no regression)."""
    target = tmp_path / "existing.md"
    target.write_text("seeded\n")
    payload = {
        "session_id": "test-edit-case",
        "tool_name": "Edit",
        "tool_input": {"file_path": str(target)},
        "cwd": str(tmp_path),
    }
    result = _run_hook(payload, fake_home=tmp_path / "home")
    assert result.returncode == 2
    assert b"You have not Read" in result.stderr
    telemetry = (
        tmp_path / "home" / ".claude" / "logs" / "freshness-hook.jsonl"
    ).read_text()
    assert '"reason":"no_prior_read"' in telemetry


def test_write_to_existing_unread_file_still_blocks(tmp_path: Path) -> None:
    """Write to an EXISTING file is an edit, not a create — gate must hold."""
    target = tmp_path / "existing.md"
    target.write_text("seeded\n")
    payload = {
        "session_id": "test-write-edit-case",
        "tool_name": "Write",
        "tool_input": {"file_path": str(target)},
        "cwd": str(tmp_path),
    }
    result = _run_hook(payload, fake_home=tmp_path / "home")
    assert result.returncode == 2
    assert b"You have not Read" in result.stderr
```

### Step 3 — Add a matcher regression guard (concession adopted from Proposal B)

**File:** `/config/workspace/IronClaude/tests/cli/test_install_hooks.py`

Append this test at the end of the file (after the existing
`test_smoke_install_then_reinstall_force`):

```python
# ---------------------------------------------------------------------------
# Regression guard: the real hooks.json must continue to gate Write
# (i.e., Proposal A is the chosen approach, not Proposal B which would have
# removed Write from the matcher).
# ---------------------------------------------------------------------------


def test_real_hooks_json_gates_write_in_pre_tool_use():
    """Pin the matcher tools list so the gated set doesn't drift silently."""
    real_hooks = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "superclaude"
        / "hooks"
        / "hooks.json"
    )
    assert real_hooks.exists(), real_hooks
    data = json.loads(real_hooks.read_text())
    pre_tool = data["hooks"]["PreToolUse"]
    fresh_registrations = [
        r
        for r in pre_tool
        if any(
            "freshness-pre-edit.sh" in h.get("command", "")
            for h in r.get("hooks", [])
        )
    ]
    assert len(fresh_registrations) == 1
    matcher_tools = set(fresh_registrations[0]["matcher"].split("|"))
    # Proposal A keeps Write in the matcher — script handles create-case.
    assert "Edit" in matcher_tools
    assert "Write" in matcher_tools
    assert "mcp__serena__replace_content" in matcher_tools
    assert "mcp__serena__replace_symbol_body" in matcher_tools
    assert "mcp__serena__insert_after_symbol" in matcher_tools
    assert "mcp__serena__insert_before_symbol" in matcher_tools
```

### Step 4 — Sync dev copy

```
cd /config/workspace/IronClaude
make sync-dev
make verify-sync
```

**Important caveat:** verify that `make sync-dev` actually syncs `hooks/`. The
project CLAUDE.md documents sync-dev as "Copy src/superclaude/{skills,agents}
→ .claude/" without mentioning hooks. Run
`grep -n hooks /config/workspace/IronClaude/Makefile` first. If sync-dev does
NOT include hooks, the dev copy at `.claude/hooks/freshness-pre-edit.sh` (and
the user copy at `/config/.claude/hooks/freshness-pre-edit.sh`) must be
refreshed via `superclaude install -f` instead. This is a known gap in
sync-dev's scope, not a fault of the proposal.

### Step 5 — Run tests

```
cd /config/workspace/IronClaude
uv run pytest tests/hooks/ -v
uv run pytest tests/cli/test_install_hooks.py::test_real_hooks_json_gates_write_in_pre_tool_use -v
```

### Step 6 — (Optional) Note for in-flight sprints

After this change is merged, currently-running sprints with already-installed
copies of `freshness-pre-edit.sh` continue to exhibit the old behavior until
they pick up the new script. There is no in-flight migration: the next time
the user runs `superclaude install -f` (or `make sync-dev` if that target is
extended to include hooks), the new script overwrites the old. No state-file
migration is required — `~/.claude/state/reads.jsonl` and
`~/.claude/logs/freshness-hook.jsonl` schemas are forward-compatible
(only the `reason` enum gains a new value, `create_allowed`).

---

## Provenance

This document was produced by the `/sc:adversarial` skill protocol against two
manually-conceived fix proposals (no Mode B generation step; the two
proposals were drafted by the orchestrator from distinct fix families
specified in the calling prompt). All file references and line numbers were
verified by direct Read against the working tree on 2026-05-15. No files were
modified during this analysis (read-only scope honored, except for writing
this debate report — the orchestrator itself hit the create-case bug
described herein, which is itself confirming evidence of the bug's
reproducibility).

Convergence note: under the rubric defined above, the two proposals diverged
materially on three of five factors; tiebreaker protocol not invoked because
the score gap (4.275 vs 0.308) far exceeds the 5% threshold.
