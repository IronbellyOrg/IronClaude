# /sc:analyze report: /opt/aidev/orca/runtime.sh (issue 779), focus architecture, depth quick

Codegraph: index_state=not-checked, checked_at=2026-11-24T20:48:27Z; degraded: graph:skipped (target /opt/aidev/orca is outside this worktree, so the index cannot cover it; Glob, Grep, Read used)

## Findings
1. INFO: the target is not repository code. /opt/aidev/orca/runtime.sh (63 lines, root-owned, 0755) is a lock-and-env wrapper that runs /opt/aidev/orca/runtime.mjs (700 lines). No file in this repo references runtime.sh (grep outside .dev/ returned nothing).
2. INFO: runtime.mjs starts Orca with `spawn(binary, ['serve','--bind','127.0.0.1','--port','6768','--pairing-address',base,'--json'])` at /opt/aidev/orca/runtime.mjs:667-668. No Chromium flag (--disable-gpu, --disable-gpu-compositing, frame-rate cap) is passed there. serveEnv (runtime.mjs:61-83) sets no Chromium/Electron variable either. So Step 9's "add a flag in runtime.sh" has no existing hook for flags; it would be a new change to a file outside this repo.
3. INFO: live process list shows the Electron GPU process started as `--type=gpu-process --disable-dev-shm-usage --ozone-platform=x11` and Xvfb as `Xvfb :99 -screen 0 1280x1024x24 -nolisten tcp -terminate` (matches the issue's environment).
4. OBSERVATION (single 3 s sample, 2026-11-24T20:48:39Z, not the issue's conditions): orca-ide main pid 528 at 4.3% CPU; no GPU process in the top 7. Cannot reproduce the 32% / 30-60% figures right now. UNVERIFIED whether a browser client was attached or whether this is the same workspace.
## Architecture verdict
Defect location is unknown (issue says frame source not found). Fix, if any, lives in the Orca derivative app or the platform image at /opt/aidev, not in IronClaude source.
