# Position B — Alternative: explicit pre-phase resume-cursor breadcrumb file

## Claim
Derive-only is too fragile to be the SOLE cursor source. Add a tiny, atomically-written
`resume-cursor.json` (single field: `{"phase": N, "ts": ...}`) written via tmp+rename
BEFORE each phase's `phase_start`, overwritten each phase. The planner reads it as the
authoritative cursor and uses the ledger only to refine intra-phase progress.

## Mechanism
- Reuse the exact atomic write convention already proven in the codebase:
  `_write_phase_result_json` (`executor.py:2070-2072`) does `tmp.write_text(...)` then
  `tmp.replace(out)`. A breadcrumb written the same way is crash-atomic by construction —
  `os.replace` is atomic on POSIX, so the file is either the old phase or the new phase,
  never torn.
- Contrast: the JSONL append (`logging_.py:265-267`) is `open(...,"a"); f.write(json+"\n")`
  with NO fsync and NO atomic rename. A hard crash (SIGKILL/OOM/power-loss) mid-write can
  leave a torn final line, and a crash after `f.write` returns but before the OS flushes
  the page cache can leave the `phase_start` line entirely absent on disk.

## Arguments for
1. **Torn-line immunity.** The whole DD-1 thesis ("phase number always survives") depends
   on the last `phase_start` line being intact. A torn JSONL tail is exactly the hard-crash
   case DD-1 claims to handle — and the append path has no atomicity guarantee. A breadcrumb
   via tmp+rename removes this class entirely.
2. **Single-writer authority.** One canonical 2-field file is trivially parseable; no
   "scan all events, pair starts with closes" loop that itself can be confused by an
   interleaved or duplicated ledger (concurrent runs, manual replays).
3. **Symmetry with the codebase's own crash-safety pattern** — the result JSON already
   chose atomic write precisely "so a crash mid-write never leaves a truncated file"
   (`executor.py:2056-2057`). The cursor deserves the same guarantee.
4. The seed-brief's own R2 mitigation (`merged-requirements.md:175-178`) explicitly
   proposed "emit/confirm a pre-spawn breadcrumb (OQ1) so the interrupted phase is always
   inferable." DD-1 overrides that mitigation; Position B keeps it.

## Cost
One new small file + one new atomic write per phase. Net write-path surface: +1 file,
same proven convention. Backward-compatible (absent ⇒ fall back to ledger derivation).
