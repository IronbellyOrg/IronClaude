# F-38: Process I/O robustness -- logger no fsync, BrokenPipeError swallowed, no NFS guarantee

**Final severity (Stage 2 preliminary)**: LOW
**Pattern tags**: P4
**Identified by**: D-8, D-9, D-12
**File:line**: `src/superclaude/cli/prd/logging_.py:166-174`; `src/superclaude/cli/pipeline/process.py:140-146`; `src/superclaude/cli/prd/executor.py:502-524`

## Evidence

```python
# logging_.py:166-174 -- append without fsync
def _write_jsonl(self, data: dict) -> None:
    with open(self._jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, default=str) + "\n")

# pipeline/process.py:140-146 -- BrokenPipeError swallowed silently
try:
    if self._process.stdin is not None:
        self._process.stdin.write(self.prompt.encode("utf-8"))
        self._process.stdin.close()
except BrokenPipeError:
    pass  # no log that prompt delivery failed
```

## Trace

- **Logger**: Each call opens in append mode and lets context manager close (flushes to libc buffers but not fsync). Kill -9 mid-write produces partial last line. Recovery code with naive `json.loads(line)` hits JSONDecodeError.
- **BrokenPipeError**: Child dies before reading stdin; parent swallows the error with no diagnostic. User sees generic ERROR with no indication the prompt never reached the child.
- **NFS**: `_resolve_step_content`'s `rglob` searches `task_dir` and `task_dir.parent`. On NFS with delayed metadata visibility, freshly Write'd files may not appear in the parent's directory cache. Local FS safe by POSIX semantics.

## Reproduction sketch

Kill -9 the parent mid-write; tail `execution-log.jsonl`; observe partial last line. Or replace `claude` with `/bin/false`; observe ERROR with no diagnostic that prompt delivery failed.

## Confidence (aggregated)

0.65 -- All three sites verified by Agent D. Low severity because PRD pipeline write cardinality is small and production deployment is local FS.

## Cross-agent corroboration

- **Agent D** identified all three I/O robustness gaps: logger append without fsync, BrokenPipeError swallow, and NFS directory cache timing for freshly-written artifacts.
