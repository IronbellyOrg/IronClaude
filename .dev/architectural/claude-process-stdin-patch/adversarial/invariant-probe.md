# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID      | Category              | Assumption                                                                                                       | Status        | Severity | Evidence                                                                                                                            |
|---------|-----------------------|------------------------------------------------------------------------------------------------------------------|---------------|----------|-------------------------------------------------------------------------------------------------------------------------------------|
| INV-001 | state_variables       | Subprocess `_stdout_fh` and `_stderr_fh` are always file descriptors backing real files (not PIPEs)              | ADDRESSED     | HIGH     | A§5 deadlock argument and B§5.2 both rely on this. The contract is enforced at `pipeline/process.py:114-115`; documented in code   |
| INV-002 | guard_conditions      | `claude --print` requires EOF on stdin before it begins processing the prompt                                    | ADDRESSED     | HIGH     | Both proposals close the write end of stdin in `try/finally` (A§3.3 line 269; B§3.1 StdinDelivery.write). Without EOF, child hangs |
| INV-003 | guard_conditions      | `os.setpgrp` is set in child via `preexec_fn` BEFORE the writer thread starts in parent                          | ADDRESSED     | MEDIUM   | B§6 case 10 explicit; preexec_fn fires between fork and exec, writer thread starts after Popen returns. No race                    |
| INV-004 | count_divergence      | Threshold check uses byte length (`len(prompt.encode("utf-8"))`) not character length                            | ADDRESSED     | MEDIUM   | A§3.2 `_use_stdin_for_prompt` encodes; B§3.1 StringPrompt.size_bytes encodes. Multibyte UTF-8 (CJK, emoji) handled correctly       |
| INV-005 | interaction_effects   | Pinned `claude` CLI build accepts a missing positional prompt and reads stdin in `--print` mode                  | ADDRESSED     | HIGH     | **VERIFIED 2026-04-30** on `claude 2.1.123 (Claude Code)`. Three probes: baseline argv (exit 0), stdin-only (exit 0), 200 KB stdin (exit 0). Probe 2 command: `echo "..." \| env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT timeout 60 claude --print --dangerously-skip-permissions --max-turns 1 --output-format text` |
| INV-006 | state_variables       | `subprocess.Popen.stdin` reaches the writer thread before the daemon thread is started                           | ADDRESSED     | LOW      | `proc.stdin` is set during `Popen.__init__`; thread starts after Popen returns. No ordering risk                                    |
| INV-007 | collection_boundaries | Empty-string prompt (`prompt=""`) does not silently switch to stdin (which would block waiting for content)      | ADDRESSED     | MEDIUM   | B§6 case 11 explicit (preserves `-p ""` argv path). A is implicit but `_use_stdin_for_prompt` returns False for size 0             |
| INV-008 | guard_conditions      | Writer thread cleans up stdin handle even if `iter_chunks`/encode raises (no leaked PIPE)                        | ADDRESSED     | HIGH     | A§3.3 closes stdin in `finally`; B§3.1 StdinDelivery.write closes in `finally`. Either way, EOF is delivered                       |
| INV-009 | interaction_effects   | Cancellation polling at `roadmap/executor.py:763-775` continues to function while writer thread streams stdin   | ADDRESSED     | HIGH     | Both proposals run writer in daemon thread. Polling is in main thread; never blocked by writer. SIGTERM path closes pipe → BrokenPipe → writer exits |
| INV-010 | count_divergence      | The `+2` offset in PortifyProcess anchor (A's solution) assumes `--output-format` and its value are adjacent argv elements | ADDRESSED  | MEDIUM   | A§4 explicit; tested. `build_command()` in `pipeline/process.py:81-86` emits them as separate elements. Pinned by Portify regression test |
| INV-011 | guard_conditions      | `PROMPT_MAX_BYTES` check fires BEFORE `Popen` (and before file FDs are opened)                                   | ADDRESSED     | LOW      | A§3.3 lines 211-220: sanity check is the first action in start() if stdin path is chosen. Files opened only after                  |
| INV-012 | interaction_effects   | Stdin daemon thread does not race with `terminate()` to write to a closed pipe                                   | ADDRESSED     | MEDIUM   | A§6 case 1; B§6 case 1. BrokenPipeError caught in writer; `_join_stdin_writer` joins after process exit                            |
| INV-013 | state_variables       | `self.prompt` attribute is consistent with what the writer thread streams (no mutation race)                     | ADDRESSED     | LOW      | A: `prompt_bytes` snapshot captured in closure before thread spawn. B: `frozen=True` dataclass for StringPrompt                    |
| INV-014 | collection_boundaries | Multibyte UTF-8 chunk boundaries do not corrupt the prompt as seen by claude                                     | ADDRESSED     | MEDIUM   | B§6 case 4 explicit. Bytes are reassembled on receiving side; mid-codepoint splits are valid in a byte stream. Test covers emoji  |
| INV-015 | interaction_effects   | Existing `_log.debug("spawn pid=%d cmd=%s", ..., self.build_command()[:3])` log line is unchanged for log-scrapers | ADDRESSED   | LOW      | A§6 case 10 explicit; B§7 explicit ("`cmd[:3]` log unchanged"). New observability is additive                                       |

## Summary

- **Total findings**: 15
- **ADDRESSED**: 15 (was 14; INV-005 resolved 2026-04-30)
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0

## Convergence Gate Decision

**CONVERGED**: All HIGH-severity findings ADDRESSED. INV-005 was verified by external probe on 2026-04-30 against `claude 2.1.123`. Design is cleared for implementation.

Both proposals depend on `claude --print` reading from stdin when the positional prompt argument is omitted. The CLI's `--help` output describes `--print` as "useful for pipes," but no test in either proposal verifies this on the pinned binary. If the assumption is false:
- The build_command() change emits no `-p` argv element, leaving claude with no prompt source it recognizes.
- The child likely either errors with a "missing prompt" message or hangs waiting on a different input channel.
- The daemon writer thread streams bytes into a stdin that claude is not reading; the writer eventually closes the pipe; claude exits with non-zero; the operator sees a confusing failure that looks like the patch is broken.

**Required action before deployment**: a 5-second external probe.

```bash
# On the same host, with the same pinned claude:
echo "respond with exactly OK" | claude --print --tools default --max-turns 1 --output-format text
```

Expected: claude exits 0 with output containing "OK". If it instead errors with "no prompt provided" or similar, the design pivots: keep `-p` in argv but pass a sentinel `"<stdin>"` value, or use `--input-format=stream-json` framing.

The merged design proceeds **conditional on this probe passing**. The probe is documented as a P0 release-gate test in `merge-log.md`.
