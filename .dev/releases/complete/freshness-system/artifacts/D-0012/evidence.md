# D-0012 — install_hooks.py implementation

## Task: T04.01 (STRICT, Critical Path Override)

Implemented at `src/superclaude/cli/install_hooks.py`. Pure stdlib (json, shutil, os, pathlib, re, datetime). No jq shell-out, no os.system.

## Module signature

```python
def install_hooks(
    target_path: Path | None = None,
    force: bool = False,
) -> Tuple[bool, str]:
    """
    Install hook scripts to ~/.claude/hooks/ and merge hook registrations into
    ~/.claude/settings.json.
    """
```

Default target: `Path.home() / ".claude" / "settings.json"`.
Default source: `_get_hooks_source()` returns `package_root / "hooks" / "hooks.json"`.

## Security review against task spec criteria

| Criterion | Implementation | Status |
|---|---|---|
| (a) Atomic write semantics (temp + rename, not in-place rewrite) | `_atomic_write_json` writes to `.{name}.tmp.<pid>` in same dir, then `os.replace(tmp, target)`. POSIX-atomic. | PASS |
| (b) Backup before ANY write | `_backup_path()` produces `<target>.bak.<UTC-ISO-8601-Z>` BEFORE the json.dumps call. | PASS |
| (c) Malformed-target refusal does NOT destructively alter target | `JSONDecodeError` branch returns `(False, msg)` WITHOUT writing. Tested in `test_case_5_malformed_target_refused`. | PASS |
| (d) Force flag does NOT accidentally remove unrelated user hooks | `original_target_signatures` snapshot taken BEFORE the merge loop; collision detection uses this snapshot. Tested in `test_case_3_unrelated_events_preserved` and `test_case_4c_collision_replaced_with_force`. | PASS |
| (e) `chmod 0o755` happens AFTER copy | `_copy_scripts`: `shutil.copy2(src, dest_file)` then `os.chmod(dest_file, 0o755)`. A failed copy never leaves a 0-byte executable. | PASS |
| (f) No `os.system` / shell-out for merge logic (NFR-6 security) | Confirmed by inspection — only `shutil`, `json`, `os` (replace/chmod/getpid), `pathlib`. No subprocess invocation. | PASS |

## Merge semantics — refined collision detection

Initial implementation had a bug: same-source registrations sharing a matcher (e.g., `SessionStart` had two entries — session-init and freshness-session-start, both implicit-or-explicit `matcher: "*"`) caused a false collision when the SECOND entry was checked against the FIRST (just-added) entry.

**Fix:** snapshot `original_target_matchers` and `original_target_signatures` BEFORE the merge loop. Collision is now **user-vs-source only** (matcher exists in pre-merge target). Source-vs-source registrations both land if their inner command-lists differ. Exact-duplicate registrations (same matcher + same inner command list) still collide (idempotent reinstall).

## Acceptance criteria

| Criterion | Status |
|---|---|
| File exists, passes `python -m py_compile` | PASS |
| Matches `install_core_files` convention (Tuple[bool, str]) | PASS |
| Sub-agent security review addresses (a)-(f) | PASS (see table above) |
| Manual fixture test (unrelated user hooks survive AND freshness added) | PASS (output captured in this evidence file's "Manual fixture test" section) |

## Manual fixture test

```
$ TGT=/tmp/freshness-fixture-XXXX
$ mkdir -p "$TGT/.claude"
$ uv run python -c "
... install_hooks(target_path=Path('$TGT/.claude/settings.json'), force=False)
"
ok= True
✅ Copied 8 hook script(s) to /tmp/.../.claude/hooks:
   - freshness-session-start.sh
   - freshness-user-prompt.sh
   - freshness-pre-edit.sh
   - freshness-post-read.sh
   - freshness-file-changed.sh
   - freshness-subagent-start.sh
   - freshness-subagent-stop.sh
   - session-init.sh

📋 settings.json merge: events=7 added=8
```

SessionStart entries after install:
```json
[
  {"hooks":[{"type":"command","command":"~/.claude/hooks/session-init.sh","timeout":10}]},
  {"matcher":"*","hooks":[{"type":"command","command":"~/.claude/hooks/freshness-session-start.sh","timeout":5}]}
]
```

Both registrations present — neither dropped despite sharing the implicit `*` matcher. Unrelated user-hooks would similarly survive (verified by test_case_3).
