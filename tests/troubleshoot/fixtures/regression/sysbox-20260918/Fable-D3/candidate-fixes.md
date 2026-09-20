# Candidate fixes — sysbox public §8 `runner-unavailable`

Tier 2 cards: `tier2-root-cause-analyst-hypothesis.md` (self 0.55), `tier2-devops-architect-hypothesis.md` (self 0.70).
Calibration: inline-fallback (confidence-calibrator not spawned; orchestrator re-graded against refs/escalation-rubric.md).

| # | proposal | agents | verdict | calibrated |
|---|---|---|---|---|
| 1 | `aidev_seed_now` fails at the first `/proc/uptime` read → `return 1` at :583 → :765-766. Mechanism: sysbox-fs `/proc/uptime` = direct-I/O **non-seekable** FUSE node, EOF for offset>0, ignores `req.Size`; bash `read` on an ESPIPE fd does `zread(fd,&c,1)` → 1-byte reads → EIO (oversize reply) or 1 byte then EOF → `read` rc≠0. Fix: bulk read `uptime=$(</proc/uptime)` at all six clock sites. | devops-architect (named mechanism), root-cause-analyst rank 1 (same site, mechanism open) | **consensus on site**; devops supplies the mechanism | 0.72 |
| 2 | `mktemp -d /tmp/…` / auth-lock fails at :585-589 (sysbox implicit tmpfs) | root-cause-analyst rank 2 | competing (alternative), not chosen; guarded by `tmp-writable` row | 0.15 |
| 3 | handshake never `owned` (:704-716) | both: ruled out from code (`/proc/<pid>/stat` kernel procfs, no seccomp trap on setsid) | outlier | 0.05 |
| 4 | mid-loop `aidev_seed_now` failure after `go` (:724) | both: unlikely (<1 s, needs 3 prior successful reads); discriminated by `started-line` | outlier | 0.03 |

Wave 4 adversarial: **skipped** — both cards converge on the same failing statement and the same fix site; only the named sub-mechanism differs (devops names it, root-cause leaves it open). No competing strong fixes to debate.

## Inline calibration of proposal 1 (5 dimensions)
- Evidence grounding 0.9 — repo lines Read; upstream sysbox-fs `procUptime.go` (`req.Offset>0 → io.EOF`, `%.2f %.2f\n`, no `req.Size`) and `fuse/file.go` (`OpenDirectIO` unconditional, `OpenNonSeekable` when handler says so, `resp.Data = handlerReq.Data[:n]`) fetched this pass; bash 5.2 `read.def` (`input_is_pipe = lseek(...)<0 && errno==ESPIPE` → `zread(fd,&c,1)`) fetched this pass.
- Runtime check 0.4 — no sysbox host executed (forbidden); kernel FUSE oversize-reply handling recalled (either branch fails, so it is not load-bearing).
- Symptom coverage 1.0 — enum, §8 fail, <1 s, no checkout, DNS/HTTPS true, DinD×2 + sysbox blank pass all predicted.
- Reproducibility 1.0 — deterministic per open()/read() semantics.
- Fix directness 0.8 — changes only the consuming idiom; identical result on kernel procfs (verified locally: `aidev_seed_ms` and askpass `remaining_time` agree with the old idiom).
Calibrated: 0.72 (below 0.85 → the report stays `partial` until the next sysbox public run lands `seed-diag-uptime-regex=false` / `seed-diag-uptime-bulk-regex=true`).
