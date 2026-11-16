Review 1-1 of T175 (fresh subagent, prompt-1-1.md): T175.AC1 unmet behind F1.1.
F1.1 ac=T175.AC1 at=src/superclaude/cli/sweep/probes.py:579 anchor="Every path a reader opens is re-resolved and rejected with `unscanned: outside root` when it escapes." chk=y,n,n,n family=outside-root-report: read_packages calls read_ledger, which returns only the bool, so the `outside root` (and `ledger not readable`) reason is dropped and collect adds no source row for an escaping package ledger.
F1.2 note probes.py:679 chk=n,n,n,n: last_record_ts is None when the last complete record has no timestamp (readable transcript); classify falls back to mtime.
F1.3 note probes.py:331 chk=n,n,n,n: parse_time accepts date-only, no-seconds and basic-format values.
F1.4 note probes.py:1109 chk=n,n,n,n: declaration order differs from the DESIGN 7.1 listing.
F1.5 note probes.py:264 chk=n,n,n,n: OrcaResult.data for ok holds the envelope result object (run-current: the Run id), not the whole parsed JSON.
Review 2-1 of T175 (fresh subagent, prompt-2-1.md): T175.AC1 met. F1.1 resolved. No blocking findings.
