# Findings: issue 779 (Orca-ide burns CPU while idle, ~60 fps software compositing)

Checked 2026-11-24 against the live issue (open, label `bug`, no comments, created 2026-11-24T19:13:58Z) and `/opt/aidev/orca/` (analysis: `.dev/issuecleanup/g7/779/analyze/analyze-report.md`).

## Verdict

**still-relevant** (open, not started, and not fixable in this repository).

- The issue is a debug-first investigation: its own text says the frame source "was NOT found", and every step in "Fix approach" is marked UNVERIFIED. No fix, branch or PR exists: `gh pr list --repo IronbellyOrg/IronClaude --state all --search 'orca CPU idle'` returned nothing; issue searches for `orca-ide`, `orca idle CPU frame compositing` and `runtime.sh orca` returned only 779 itself plus unrelated issues.
- The code that would change is outside IronClaude. `/opt/aidev/orca/runtime.sh` (63 lines, root-owned) only takes a lock and runs `runtime.mjs`. No file in this repo outside `.dev/` mentions `runtime.sh` (grep, 2026-11-24).
- `/opt/aidev/orca/runtime.mjs:667-668` starts Orca with only `serve --bind 127.0.0.1 --port 6768 --pairing-address <base> --json`; `serveEnv` (`runtime.mjs:61-83`) passes no Chromium or Electron flag. So the issue's Step 9 ("add the effective Chromium flag to runtime.sh's Orca start") is a new change to the platform image, not an edit of existing flags. UNVERIFIED: whether the Orca binary or `serve` itself applies flags internally.
- Environment matches the issue: live process list shows `Xvfb :99 -screen 0 1280x1024x24` and an Orca `--type=gpu-process ... --ozone-platform=x11`.
- Could not reproduce right now: one 3 s `top` sample at 20:48:39Z showed orca-ide main (pid 528) at 4.3% and no GPU process in the top 7. UNVERIFIED whether this is the issue's workspace or whether a browser client was attached. The load may be intermittent or tied to a connected client.
- The issue's own claim "Related Issues: None found" holds on my search.

## Complexity and size

Complexity **complex**, size **M**: the cause is unknown, needs live profiling (DevTools trace, Chromium flag bisect, perf) on a running Orca, and the likely fix sits in the Orca app or platform image, not in this repo.

## Priority

**P2**: wasted CPU in a workspace with no data loss and the machine stays usable (issue's own severity is medium); it blocks nothing in IronClaude, but it competes with codegraph, the `gh` poll and the issue watcher for CPU.

## Concrete next steps

1. Decide ownership: this belongs to whoever maintains `/opt/aidev` and the Orca derivative, not to IronClaude code. Move it to that owner's tracker or keep it here as a tracking issue (owner's call; I changed nothing on GitHub).
2. Reproduce first: sample main and GPU process CPU with `top -H` for 60 s with a browser client attached and 30 or more terminals, as in the issue's Steps 1 and 6. My single sample without that load was low.
3. Run Step 2 (try `--disable-gpu-compositing` and a frame cap) and Step 3 (smaller display) to split "too many frames" from "each frame too costly".
4. Any restart must go through `runtime.sh stop` and `runtime.sh start "<app address>"`, then confirm `runtime.sh offer` works, as the issue warns.
5. Only then change the start invocation in `runtime.mjs` (outside this repo, root-owned), keeping terminals alive.

## Dependencies

Needs: none in this repo's issue list. Blocks: none found. External: access to change `/opt/aidev/orca/runtime.mjs` (root-owned) or the Orca derivative build. UNVERIFIED: who owns that image.

## Related issues

- None found for the same problem. 757 (run the coordinator sweep outside the session) and 766 (read workers show as Could not Determine) are loosely related only because they concern idle CPU or Orca polling load; no stated link. Related only by search, UNVERIFIED as true relations.

## Related PRs

None found (PR search for Orca idle CPU returned nothing).
