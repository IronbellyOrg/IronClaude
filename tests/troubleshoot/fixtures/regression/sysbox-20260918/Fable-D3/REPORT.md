---
status: partial
tier_reached: 2
confidence: 0.72
escalation_reason: forced_by_depth_deep
test_is_wrong: false
behavior_is_documented: false
doc_context_card_path: null
diagnosability_verdict: partial
pipeline_hardening_applicable: false
---

# PR170 sysbox-runc public arm — §8 `runner-unavailable`

**Target**: `templates/VSCode-AIDev02/scripts/startup.sh` §8 (`aidev_seed_now` / `aidev_seed_attempt`), `startup-git-askpass.sh` `remaining_time`.
**Decisive artifact**: run 35372133385, job 105704643590, artifact 10562464724 (`tier1-observation.md`).
**Grounding**: native Read/Grep + WebFetch of upstream sources (auggie/serena not invoked — degraded; Wave 1.5 doc discovery and Wave 1.6 audit folded into the Tier-2 cards; no formal cards → `partial`).

## Summary
The sysbox public arm records `runner-unavailable` in <1 s with no checkout because `aidev_seed_attempt` returns at its very first gate: `aidev_seed_now` cannot read `/proc/uptime`. Under sysbox-runc that file is served by sysbox-fs as a direct-I/O, **non-seekable** FUSE node that returns EOF for any offset > 0 and ignores the request size; bash's `read` builtin detects the ESPIPE fd and falls back to 1-byte reads, which can never consume the line. The DinD arms read kernel procfs (seekable, buffered 128-byte reads) and the sysbox blank arm never calls the gate (§8 skipped). The fix replaces the `read` idiom with a single bulk read `$(</proc/uptime)` at all six clock sites; behaviour on kernel procfs is unchanged (verified locally).

## Diagnosis
Path P1 from `tier1-observation.md`, narrowed to the clock read:

1. startup.sh:583 `command -v setsid … && command -v git … && aidev_seed_now || return 1` — first statement of the attempt, before `mktemp` (:585) and before any `&`.
2. `aidev_seed_now` (pre-fix :504) `IFS=' ' read -r uptime rest < /proc/uptime || return 1`.
3. sysbox-fs `handler/implementations/procUptime.go`: `Open()` returns `nonSeekable=true` ("/proc/uptime is not seekable"); `readUptime()`: `if req.Offset > 0 { return 0, io.EOF }`, `fmt.Sprintf("%.2f %.2f\n", …)`, `req.Data = []byte(uptimeStr)`, `req.Size` never consulted. `fuse/file.go`: `resp.Flags |= fuse.OpenDirectIO` unconditionally, `OpenNonSeekable` when the handler says so, `resp.Data = handlerReq.Data[:n]` (no clamp to `req.Size`).
4. bash 5.2 `builtins/read.def`: `input_is_pipe = (lseek (fd, 0L, SEEK_CUR) < 0) && (errno == ESPIPE)` → `unbuffered_read = 1` → `zread (fd, &c, 1)`. Non-seekable FUSE open clears `FMODE_LSEEK`, so `lseek` → ESPIPE.
5. First 1-byte `read(2)` either fails (12-byte reply for a 1-byte request → kernel rejects → EIO) or returns one byte after which the second read at offset 1 hits the handler's EOF → `read` returns non-zero (EOF before delimiter). Either way `|| return 1` fires → :765-766 `aidev_seed_outcome=runner-unavailable`.

Corroboration: same idiom at (pre-fix) :614/:680 (leader), :1620/:1662 (tool-floor probe, `aidev_tf_now || exit 125` at :1655 → every tool-floor probe fails on sysbox, marker `tool-floor-verify-pass` absent — not asserted by any test, so it has been silently failing), askpass :37 (`return 27` → category `runner-unavailable`). `/proc/<pid>/stat`, `/proc/sys/kernel/random/uuid` (startup.sh:80-81, passes on sysbox blank) are kernel procfs, not emulated.

## Evidence
- startup.sh:575 `rc=runner-unavailable` default; :583 first gate; :585 mktemp; :758 top-level default; :765-766 attempt-failed branch; :724 mid-loop path; :1655 tool-floor `exit 125`.
- startup-git-askpass.sh:38 (post-fix) clock read; category map `27) category=runner-unavailable` (askpass :23).
- Artifact rows (tier1-observation.md:5-13): `runner-unavailable`, `section8-status=fail`, dns/https `true`, checkout-dir/toplevel `false`.
- Upstream sources fetched 2026-09-18: nestybox/sysbox-fs master `handler/implementations/procUptime.go`, `fuse/file.go`; GNU bash 5.2 `builtins/read.def` (quotes in `candidate-fixes.md`).
- Local check `/tmp/fable-seed-diag-check.sh`: post-fix `aidev_seed_now` and askpass `remaining_time` produce the same values as the old idiom on kernel procfs; collector rows project; probe leaves no `/tmp/aidev-seed.*` residue; `SEED_HANDSHAKE` replica = `owned-group`.

## Proposed Fix (applied in working tree)
`uptime=$(</proc/uptime) || …; uptime=${uptime%% *}` replacing `IFS=' ' read -r uptime rest < /proc/uptime || …` at startup.sh:507, :618, :685, :1626, :1669 and startup-git-askpass.sh:38. Regex, arithmetic, deadlines, exit codes, ownership/identity handshake, signal discipline, secret region: unchanged.

Collector (CI invocation site, `test-startup-boot.sh`) gains three discriminators on the next run: `seed-diag-uptime-regex` (old idiom; predicted `false` on sysbox, `true` on DinD), `seed-diag-uptime-bulk-regex` (new idiom; predicted `true` everywhere), `seed-diag-tmp-writable` (guards the rank-2 alternative). Plus the previously staged `setsid-present`, `git-present`, `tool-floor-pass`, `started-line`, `seed-handshake-observed`.

## Alternative Fixes Considered
- `/tmp` unwritable under sysbox (mktemp/auth-lock at :585-589): identical signature, no evidence for it; `tmp-writable` row falsifies. Not applied.
- Handshake / `/proc/<pid>/stat` / setsid under sysbox: ruled out from code (kernel procfs; seccomp-notify does not trap setsid; child is a non-leader direct child on both arms). `seed-handshake-observed` row confirms.
- Relaxing the uptime regex or switching to `EPOCHREALTIME`: rejected — the failure is at `read`, not the parse, and askpass must share the same monotonic clock.

## Risk + Rollback
- Host sysbox-fs may be older/different from master; falsifier on the next sysbox public run: `seed-diag-uptime-regex=true` (then the mechanism is wrong and `tmp-writable`/`started-line`/handshake rows point elsewhere).
- Fixing the clock read un-masks the tool-floor probe on sysbox (previously all-125); real tool failures could now surface there. Marker still not asserted by tests.
- Rollback: revert the six two-line hunks; no state or enum changes.

## Grounding Gaps
- auggie/serena not used (native tools); Wave 1.5/1.6 not run as formal branches; `confidence-calibrator` and `evidence-validator` not spawned — inline fallbacks (citations re-Read after edit: :507/:575/:583/:585/:618/:685/:724/:758/:765-766/:1626/:1655/:1669, askpass :38 verified by grep this pass).
- Kernel FUSE oversize-reply handling recalled, not fetched; not load-bearing (both branches fail).
- No runtime observation on a sysbox host (forbidden by scope).

## Next Steps
Push the coherent repair (layer workaround + collector rows + clock-read fix) to PR170; the existing PR-triggered Actions run is the validation. Expected: sysbox public `seed-outcome-observed=cloned`, `seed-diag-uptime-regex=false`, `seed-diag-uptime-bulk-regex=true`, `seed-diag-tool-floor-pass=true`.
