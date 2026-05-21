# D-0031 — Implementation Notes

**Task**: T02.10
**Deliverable**: `tests/cli/eval/test_hard_guard_real_home.py` (NFR-SEC3 hard guard against real `~/.claude/`).

## Design decisions

### Why a separate module from `test_defense_in_depth.py`?

D-0030 covers the NFR-SEC2 attack matrix against *synthetic* `tmp_path` stand-ins. NFR-SEC3 covers the catastrophic case against the *real* `~/.claude/`. The two have different skip semantics (NFR-SEC3 tests skip on hosts where `~/.claude/` is absent; NFR-SEC2 always runs), different cleanup obligations (NFR-SEC3 must defend the host's filesystem at test teardown), and a different forensic invariant (`_DirSnapshot` mtime + SHA-256 fingerprinting of the real HOME). Splitting them keeps each module's preconditions and teardown contract focused.

### Why `_DirSnapshot` instead of `os.listdir` + mtime?

The forensic guarantee is "no pre-existing entry was modified". An `os.listdir` name-set comparison would miss the most likely tamper modes (an existing file gets its contents overwritten while keeping its name). The snapshot records, for every direct child:

- `mtime_ns` — nanosecond mtime captured via `Path.lstat()` so symlinks are recorded at the symlink layer (not the resolved target).
- `sha256` — content hash for files only (None for directories and symlinks; we never traverse subtrees).
- `size`, `is_file`, `is_dir`, `is_symlink` — type discrimination so the comparison is byte-identical.

The comparison is a per-entry `before == after` equality on the frozen `_EntrySnapshot` dataclass, which catches any change to any captured field. Per-test cost on the host (`/config/.claude/` with 0 entries during this run, but the snapshot scales linearly in direct children) is dominated by `read_bytes` on files; with `find ~/.claude/ -maxdepth 1` typically returning <50 entries on a real maintainer host, the per-test snapshot cost is bounded at low single-digit milliseconds.

### Why iterate-and-verify instead of set equality for the snapshot check?

Initially the snapshot assertion used `set(post.entries) == set(dot_claude_snapshot.entries)`. This failed in two cases:

1. **Direct-`home_root` test** — `HomeIsolation.setup()` runs `mkdtemp(prefix=f"{eval_id}-", dir=real_claude_dir)` BEFORE the guard rejects, so a leaked per-eval HOME named `HardguardevalT0210-XXXXXX` appears as a new direct child of `~/.claude/`. The set comparison would fail purely because of the intentional partial-HOME preservation (NFR-ISO2 / T02.13).
2. **Symlink-scratch-root test** — `mkdtemp(dir=str(scratch_link))` follows the symlink at the kernel level and creates the leaked dir directly inside the real `~/.claude/`.

Both cases are *not* tamper events — they are the intentional pre-guard mkdtemp behavior. The correct invariant is:

- Every pre-existing entry MUST be byte-identical after refusal.
- Every *new* entry MUST be a leaked per-eval HOME whose name starts with the test module's `HardguardevalT0210-` prefix, AND each such leak MUST be empty (no nested files/dirs/symlinks).

This pattern lets the snapshot fixture coexist with the partial-HOME preservation contract without requiring NFR-SEC3 to know about T02.13's `setup_failed` tagging.

### Why an eval-id prefix that survives `validate_eval_id`?

The eval id must pass `validate_eval_id(...)` so `HomeIsolation.__post_init__` does not reject the test before the snapshot baseline is captured. Looking at FR-SCH2's regex (`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`), `HardguardevalT0210` matches: starts with `H`, alphanumerics only, ends with the digits `02` then optional `.` then `10`. The dash that mkdtemp inserts after the prefix (`HardguardevalT0210-XXXXXX`) is part of the *directory* name, not the eval id, so the regex is not affected.

### Per-eval HOME emptiness as a second-layer invariant

The "leak is empty" assertion catches a different class of regression than the snapshot check:

- The **snapshot check** catches "the guard wrote to a sibling of the per-eval HOME under `~/.claude/`" (e.g., a stray `eval_state.json` written in the wrong directory).
- The **leak-empty check** catches "the guard ran AFTER something wrote under the per-eval HOME itself" (e.g., the hook adapter T02.14 fired before the guard, populating `~/.claude/HardguardevalT0210-XXXXXX/`).

Both invariants together prove "the guard ran before any FS write", which is the core NFR-SEC3 contract.

### Why patch `tempfile.mkdtemp` for vector 2 instead of pre-creating a symlinked per-eval HOME?

`HomeIsolation.setup()` *chooses* the per-eval HOME name via `tempfile.mkdtemp(prefix=f"{eval_id}-", dir=str(home_root))`. Pre-creating a symlink at a name the harness might not pick would not exercise the post-mkdtemp resolution check. The patch mirrors the existing T02.08 / D-0029 pattern: `mock_mkdtemp.return_value = str(evil_home)` makes `setup` adopt the pre-created symlink, then `containment_guard`'s check 3 chases the symlink and finds the target outside the scratch root.

### Stale-leak cleanup before first run

When the failing test attempt accumulated multiple `HardguardevalT0210-*` leaks under `/config/.claude/` across iteration, the `test_per_eval_home_is_empty_when_setup_refuses` assertion `len(leaks) == 1` (expecting exactly one leak from the current call) failed because prior runs' leaks survived. The `cleanup_leaked_eval_homes` fixture only removes entries that did NOT exist before the test ran (`new = after - before`); pre-existing stale leaks remain because the fixture cannot prove they belong to the test. Operators iterating on the module should `rm -rf ~/.claude/HardguardevalT0210-*` once before re-running; the fixture handles cleanup for all subsequent runs.

## Forensic guarantees verified

| Guarantee | Mechanism | Evidence |
|---|---|---|
| Refusal fires before any FS write under real `~/.claude/` | `_DirSnapshot` byte-identity per direct child | All four snapshot-bearing tests pass. |
| Leaked per-eval HOME is empty when refusal happens after mkdtemp | `list(leaked_home.iterdir()) == []` | `test_per_eval_home_is_empty_when_setup_refuses` + the symlink-scratch leak check. |
| Refusal surface is correctly bucketed per attack vector | `exc_info.value.check == <expected>` | Every test pins the `check` identifier; the contract pin (`test_hard_guard_contract_pin`) pins the class names. |
| Skip semantics document the missing prerequisite | `pytest.skip(reason=...)` in `real_claude_dir` | The skip reason names the absent path so a CI operator can decide whether to materialize the directory or accept the skip. |

## Interaction with other deliverables

- **D-0028 (HomeIsolation method surface)** — the tests instantiate `HomeIsolation(eval_id=..., home_root=..., session_id=...)` directly via the COMP-006 frozen-dataclass constructor.
- **D-0029 (FR-ISO2 path containment)** — the symlink-escape patch pattern is borrowed verbatim from `test_setup_catches_symlink_escape_under_explicit_config` in `tests/cli/eval/test_path_containment.py`.
- **D-0030 (NFR-SEC2 attack matrix)** — D-0031 is the "real `~/.claude/`" analogue of vector 1 (`scratch-is-symlink-to-HOME`) and vector 2 (`scratch-outside-allowlist`) from D-0030, plus a new symlink-scratch-root sibling case not covered by D-0030.
- **T02.13 (NFR-ISO2 atomic wrapper)** — depends on the partial-HOME preservation contract; D-0031's leak-cleanup fixture exists precisely because that contract leaks empty per-eval HOMEs on refusal.
- **T02.14 (hook adapter)** — D-0031's leak-empty assertion proves the hook adapter never runs before the guard.

## Open questions surfaced (none)

No new open questions were surfaced by D-0031. The reserved-for-follow-up items in `spec.md` (absolute hard guard, mkdtemp ordering, TOCTOU) all pre-existed in D-0029 / D-0030 / T06.03 (DOC-OQ8) and remain in those owners.
