# Actor-context feasibility gate

## Scope and result
2026-11-06. B-CTX result: BLOCKED, not PASS. Task 1 delivered log-only feasibility work, not enforcement. No global hook, Claude settings, repository hooksPath or claim launch was changed. Three controlled assertions passed; actual session-reset/resume identity is not proven. Production enforcement Tasks 2-6 have not started.

## Reproducible probe and observations
Run `bash ./artifacts/actor-context-probe.sh` from this package directory. It uses `uv run --no-project python -I -`, reads kernel stat/comm/boot identity, prints JSON to stdout, and closes/reaps its two controlled children in finally. It neither reads nor emits argv/environment secrets. `bash -n` passed and the actual run exited 0. The first capture is `./artifacts/actor-context-observed.json`. Its `removed_membership_rejected` label was wrong: the assertion checks PID zero, not removal. The corrected script was rerun successfully; current output is `./artifacts/actor-context-observed-2.json`, labelled `nonmatching_pid_rejected`. The original capture remains unchanged for provenance. Both runs exit 0 with three controlled assertions; neither proves release or actual session reset.

The observed current ancestry reached the root in nine rows: diagnostic Python -> UV -> Bash -> actual Claude -> Bash -> Orca processes -> container init. The actual Claude PID in that capture is 563897 with start_ticks 84673165. This proves the current Bash-tool process is a Claude descendant; it does not prove any other actor or lifecycle behavior.

The controlled probe created two simultaneously live child processes under one controller. Both matched the same registered ancestor (PID and start ticks). A wrong start identity did not match, and a nonmatching PID (zero) did not match. That assertion does not test membership removal or release. These are three assertion-based self-checks. No actual PID reuse or reboot was induced. The 64-hop traversal cap is a diagnostic bound, not a measured safe production bound. Exhaustion is returned explicitly, never interpreted as a trusted human.

## Required lifecycle cases
| Case | Evidence | Result |
|---|---|---|
| Current main Bash tool ancestry | actor-context-observed.json current_ancestry | observed Claude ancestor |
| Main claim-launched session binding | no implemented pipeline launcher in this checkout | unavailable |
| Subagent and nested Git/hook identities | no real pre-push hook/event capture | unavailable |
| Background Bash/Monitor descendants | only controlled Python children captured | actual harness behavior unavailable |
| Concurrent same-worktree human push | no independent human terminal fixture executed | unavailable |
| Ordinary Claude session in same worktree | not launched/observed by this probe | unavailable |
| Detached/reparented actual agent job | not observed | unavailable |
| Exit and PID reuse / boot change | wrong start and nonmatching PID rejected synthetically | actual reuse/reboot unavailable |
| Resume into a new Claude process | not observed | unavailable |
| /clear/fork with an old live governed child | controlled siblings share one ancestor; actual Claude reset not observed | decisive distinction unproven |
| Release with old background child alive | no membership removal or release was exercised | actual session lifecycle unavailable |
| Traversal bound exhaustion | explicit stop field in probe | production bound unproven |

## Missing integration contract and implementation stop
The candidate registers a Claude ancestor by session ID, PID, start identity and boot identity. Kernel parentage does not itself carry a logical Claude session ID. If one Claude process is reused for an ordinary session while an old governed child survives, both descendants can still match that one ancestor. Keeping registration can restrict the ordinary session; deleting it can release the old governed child. This is a conditional design limitation, not a claim that a real /clear was observed here.

The missing contract must bind each supported tool-execution process/job to its actual logical session generation, preserve that identity for its descendants, refresh it on resume, and distinguish new ordinary work after reset from old governed children. Release and detached/reparented-job behavior need explicit lifetime semantics. An agent-editable environment label or a worktree marker is not proof. Existing session-name.sh explicitly treats /clear and resume as the same launch for naming and fails open on unreadable process data; that naming helper is not this authorization contract.

New launcher/harness integration to supply the distinction is not authorized by the current plan's constraints. A real bounded harness experiment could establish that the unsupported topology never occurs, but no such evidence is present and synthetic siblings cannot establish that result. Therefore B-CTX remains BLOCKED. Stop before Task 2; do not install the text guard as a supposedly complete feature and do not weaken same-worktree human isolation. Full Task 1 acceptance is not claimed solely because this report exists.
