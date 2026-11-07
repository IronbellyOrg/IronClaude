c637be7c75d269eca8fc89091dce6d9f0005050c
Review one task for spec compliance.

Task brief: ## Task 1: Build and execute the bounded process-context feasibility probe

Read design sections 3, 6-8, 14 and 19.1, the panel report's B-CTX finding, and the actual ccsession/ccsession-orca process-ownership implementation located from repository search. Write a log-only probe and its reproducible commands under ./artifacts/actor-context-probe.sh and ./artifacts/actor-context-report.md. The probe records kernel process parentage, process start identity and boot identity without printing credentials or environment secrets. It must not install a production hook, mutate global Claude settings or configure a real repository's hooks. Use temporary local fixtures and actual supported Claude/Orca process observations where available; record unavailable observations as unavailable, never as passed. Child/background lifetime cases may use bounded controlled processes, but simulated harness behavior cannot replace real session reset/resume proof.

Acceptance criteria:
- ./artifacts/actor-context-report.md enumerates main Claude, subagent and nested tool calls, background Bash/Monitor descendants, same-worktree human terminal, ordinary Claude session, detached/reparented jobs, process exit and PID reuse, resume into a new process, /clear/fork, and release with a live old background child. Each has observed evidence or an explicit unsupported result with the missing interface named.
- The report tests the decisive case: a reused Claude process starts an ordinary session while an old governed background child remains alive. It demonstrates separate identities for both without relying on worktree membership or an agent-editable label. Document the bounded ancestry limit and its exhaustion behavior from evidence.
- PID reuse/boot change cannot inherit authority; release invalidates only the intended session; human pushes and ordinary sessions in the same worktree are never selected merely because another session is governed.
- The report contains a binary B-CTX result. PASS requires observed support for every required actor/lifecycle distinction and no new unauthorized launcher/harness integration. Otherwise record FAIL/BLOCKED, the exact missing binding/reset/child-lifetime contract and the smallest required integration, then halt before Task 2. Producing a report alone does not make the task compliant or authorize a gate waiver.
- Retain runnable probe/evidence on disk, capture exit results and negative evidence, and keep sensitive process arguments redacted. No production script/registration/install changes are present from this task.

Acceptance criteria ids:
T1.AC1: ./artifacts/actor-context-report.md enumerates main Claude, subagent and nested tool calls, background Bash/Monitor descendants, same-worktree human terminal, ordinary Claude session, detached/reparented jobs, process exit and PID reuse, resume into a new process, /clear/fork, and release with a live old background child. Each has observed evidence or an explicit unsupported result with the missing interface named.
T1.AC2: The report tests the decisive case: a reused Claude process starts an ordinary session while an old governed background child remains alive. It demonstrates separate identities for both without relying on worktree membership or an agent-editable label. Document the bounded ancestry limit and its exhaustion behavior from evidence.
T1.AC3: PID reuse/boot change cannot inherit authority; release invalidates only the intended session; human pushes and ordinary sessions in the same worktree are never selected merely because another session is governed.
T1.AC4: The report contains a binary B-CTX result. PASS requires observed support for every required actor/lifecycle distinction and no new unauthorized launcher/harness integration. Otherwise record FAIL/BLOCKED, the exact missing binding/reset/child-lifetime contract and the smallest required integration, then halt before Task 2. Producing a report alone does not make the task compliant or authorize a gate waiver.
T1.AC5: Retain runnable probe/evidence on disk, capture exit results and negative evidence, and keep sensitive process arguments redacted. No production script/registration/install changes are present from this task.
Global constraints: 
- The authoritative design is docs/designs/sc-issue-launch-level-hook.md, including section 19 and owner decisions O-13, O-21 and O-22. The historical merged requirements, corpus and old review verdicts provide traceability, not permission to override the current design. Read the panel report at .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md.
- Human pushes in the same worktree remain unrestricted by launch policy. A worktree marker, environment label, PID alone or an unreadable ancestry chain is not sufficient actor authority. No silently invented launcher/harness contract, root service, managed-policy deployment, server protection or isolation weakening.
- Task 1 is a blocking prerequisite for every later task. A documented unsupported lifecycle is not a compliant gate result. If the candidate cannot meet the required lifecycle distinctions, report the exact missing interface and halt implementation; do not proceed on synthetic payloads or an accepted historical residual.
- Use UV for Python operations. Use disposable local bare repositories for Git experiments; never push protected branches on the real origin. Read-only upstream documentation is allowed except the forbidden SuperClaude upstream, with which no interaction is allowed.
- Preserve the existing dirty design and all pre-existing brainstorm artifacts. No commit, push, issue comment or real global installation is authorized by this plan. Do not activate production enforcement in this live session.
- Source primitives belong under src/superclaude/. Generated .claude/ mirrors are not staged. Stage .dev/tasks, including package evidence, throughout execution. Source changes may remain uncommitted.
- Evidence paths below are package-relative and resolve beside this plan, including after executor archiving. Existing task packages and unrelated source files are not overwritten. Do not change this plan once implementation starts.
- Do not repeat earlier adversarial/spec-panel loops. Run only the executor's prescribed task compliance checks and final review. All claims of runtime proof require observed evidence; no fabricated payload logs.
Start sha: c637be7c75d269eca8fc89091dce6d9f0005050c
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-probe.sh b/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-probe.sh
new file mode 100644
index 00000000..c93d9820
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-probe.sh
@@ -0,0 +1,92 @@
+#!/usr/bin/env bash
+# Log-only Linux feasibility probe. No argv, environment values or enforcement writes.
+set -euo pipefail
+exec uv run --no-project python -I - "$@" <<'PY'
+import json
+import os
+from pathlib import Path
+import subprocess
+import sys
+
+LIMIT = 64  # Diagnostic bound only; not a proven production ancestry limit.
+
+def process(pid):
+    text = Path(f"/proc/{pid}/stat").read_text()
+    # comm can contain spaces and ')'; all following stat fields are numeric.
+    fields = text[text.rfind(") ") + 2:].split()
+    return {"pid": pid, "ppid": int(fields[1]), "start_ticks": int(fields[19]),
+            "comm": Path(f"/proc/{pid}/comm").read_text().strip()}
+
+def ancestry(pid):
+    rows = []
+    seen = set()
+    for _ in range(LIMIT):
+        if pid <= 0:
+            return {"rows": rows, "stop": "root"}
+        if pid in seen:
+            return {"rows": rows, "stop": "cycle"}
+        seen.add(pid)
+        try:
+            row = process(pid)
+        except (OSError, ValueError, IndexError) as exc:
+            return {"rows": rows, "stop": type(exc).__name__}
+        rows.append(row)
+        pid = row["ppid"]
+    return {"rows": rows, "stop": "bound-exhausted"}
+
+def selected(pid, identity):
+    return any((row["pid"], row["start_ticks"]) == identity
+               for row in ancestry(pid)["rows"])
+
+children = []
+try:
+    current = process(os.getpid())
+    identity = (current["pid"], current["start_ticks"])
+    # Both children read stdin until their controller closes it; no fixed sleep.
+    code = "import sys; sys.stdin.buffer.read()"
+    for _ in range(2):
+        children.append(subprocess.Popen([sys.executable, "-I", "-c", code],
+                                        stdin=subprocess.PIPE,
+                                        stdout=subprocess.DEVNULL,
+                                        stderr=subprocess.DEVNULL))
+    results = [selected(child.pid, identity) for child in children]
+    assert results == [True, True]
+    assert not selected(children[0].pid, (identity[0], identity[1] + 1))
+    assert not selected(children[0].pid, (0, identity[1]))
+    payload = {
+        "schema": "actor-context-probe/1",
+        "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip(),
+        "diagnostic_bound": LIMIT,
+        "current_ancestry": ancestry(os.getpid()),
+        "controlled_children": [ancestry(child.pid) for child in children],
+        "controlled_result": {
+            "both_children_match_one_ancestor": results,
+            "different_start_identity_rejected": True,
+            "nonmatching_pid_rejected": True,
+            "session_reset_observed": False,
+            "meaning": "Kernel ancestry alone does not encode two logical session memberships. This is a controlled topology check, not a real Claude reset observation."
+        },
+        "runtime_cases_not_observed": [
+            "real Claude /clear with old governed child and new ordinary session",
+            "real resume/fork across Claude processes",
+            "main/subagent/nested Bash and Monitor hook event identities",
+            "same-worktree human terminal versus actual claim-launched agent",
+            "detached/reparented actual agent job",
+            "actual process ID reuse or reboot",
+            "release of real bound session while old background child remains alive"
+        ],
+        "gate": "BLOCKED",
+        "self_checks": 3,
+        "production_changes": False
+    }
+    print(json.dumps(payload, indent=2))
+finally:
+    for child in children:
+        if child.stdin:
+            child.stdin.close()
+        try:
+            child.wait(timeout=3)
+        except subprocess.TimeoutExpired:
+            child.kill()
+            child.wait(timeout=3)
+PY
diff --git a/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-observed.json b/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-observed.json
new file mode 100644
index 00000000..4fcc69c9
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-observed.json
@@ -0,0 +1,218 @@
+{
+  "schema": "actor-context-probe/1",
+  "boot_id": "0f93183c-c3b0-46fa-b016-088783da8d52",
+  "diagnostic_bound": 64,
+  "current_ancestry": {
+    "rows": [
+      {
+        "pid": 1424084,
+        "ppid": 1424074,
+        "start_ticks": 87237975,
+        "comm": "python3"
+      },
+      {
+        "pid": 1424074,
+        "ppid": 1424072,
+        "start_ticks": 87237966,
+        "comm": "uv"
+      },
+      {
+        "pid": 1424072,
+        "ppid": 563897,
+        "start_ticks": 87237966,
+        "comm": "bash"
+      },
+      {
+        "pid": 563897,
+        "ppid": 563508,
+        "start_ticks": 84673165,
+        "comm": "claude"
+      },
+      {
+        "pid": 563508,
+        "ppid": 1212,
+        "start_ticks": 84673132,
+        "comm": "bash"
+      },
+      {
+        "pid": 1212,
+        "ppid": 454,
+        "start_ticks": 83215916,
+        "comm": "orca-ide"
+      },
+      {
+        "pid": 454,
+        "ppid": 393,
+        "start_ticks": 83215809,
+        "comm": "orca-ide"
+      },
+      {
+        "pid": 393,
+        "ppid": 1,
+        "start_ticks": 83215792,
+        "comm": "orca-ide"
+      },
+      {
+        "pid": 1,
+        "ppid": 0,
+        "start_ticks": 83215682,
+        "comm": "coder"
+      }
+    ],
+    "stop": "root"
+  },
+  "controlled_children": [
+    {
+      "rows": [
+        {
+          "pid": 1424085,
+          "ppid": 1424084,
+          "start_ticks": 87237977,
+          "comm": "python3"
+        },
+        {
+          "pid": 1424084,
+          "ppid": 1424074,
+          "start_ticks": 87237975,
+          "comm": "python3"
+        },
+        {
+          "pid": 1424074,
+          "ppid": 1424072,
+          "start_ticks": 87237966,
+          "comm": "uv"
+        },
+        {
+          "pid": 1424072,
+          "ppid": 563897,
+          "start_ticks": 87237966,
+          "comm": "bash"
+        },
+        {
+          "pid": 563897,
+          "ppid": 563508,
+          "start_ticks": 84673165,
+          "comm": "claude"
+        },
+        {
+          "pid": 563508,
+          "ppid": 1212,
+          "start_ticks": 84673132,
+          "comm": "bash"
+        },
+        {
+          "pid": 1212,
+          "ppid": 454,
+          "start_ticks": 83215916,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 454,
+          "ppid": 393,
+          "start_ticks": 83215809,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 393,
+          "ppid": 1,
+          "start_ticks": 83215792,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 1,
+          "ppid": 0,
+          "start_ticks": 83215682,
+          "comm": "coder"
+        }
+      ],
+      "stop": "root"
+    },
+    {
+      "rows": [
+        {
+          "pid": 1424086,
+          "ppid": 1424084,
+          "start_ticks": 87237977,
+          "comm": "python3"
+        },
+        {
+          "pid": 1424084,
+          "ppid": 1424074,
+          "start_ticks": 87237975,
+          "comm": "python3"
+        },
+        {
+          "pid": 1424074,
+          "ppid": 1424072,
+          "start_ticks": 87237966,
+          "comm": "uv"
+        },
+        {
+          "pid": 1424072,
+          "ppid": 563897,
+          "start_ticks": 87237966,
+          "comm": "bash"
+        },
+        {
+          "pid": 563897,
+          "ppid": 563508,
+          "start_ticks": 84673165,
+          "comm": "claude"
+        },
+        {
+          "pid": 563508,
+          "ppid": 1212,
+          "start_ticks": 84673132,
+          "comm": "bash"
+        },
+        {
+          "pid": 1212,
+          "ppid": 454,
+          "start_ticks": 83215916,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 454,
+          "ppid": 393,
+          "start_ticks": 83215809,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 393,
+          "ppid": 1,
+          "start_ticks": 83215792,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 1,
+          "ppid": 0,
+          "start_ticks": 83215682,
+          "comm": "coder"
+        }
+      ],
+      "stop": "root"
+    }
+  ],
+  "controlled_result": {
+    "both_children_match_one_ancestor": [
+      true,
+      true
+    ],
+    "different_start_identity_rejected": true,
+    "removed_membership_rejected": true,
+    "session_reset_observed": false,
+    "meaning": "Kernel ancestry alone does not encode two logical session memberships. This is a controlled topology check, not a real Claude reset observation."
+  },
+  "runtime_cases_not_observed": [
+    "real Claude /clear with old governed child and new ordinary session",
+    "real resume/fork across Claude processes",
+    "main/subagent/nested Bash and Monitor hook event identities",
+    "same-worktree human terminal versus actual claim-launched agent",
+    "detached/reparented actual agent job",
+    "actual process ID reuse or reboot",
+    "release of real bound session while old background child remains alive"
+  ],
+  "gate": "BLOCKED",
+  "self_checks": 3,
+  "production_changes": false
+}
diff --git a/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-observed-2.json b/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-observed-2.json
new file mode 100644
index 00000000..0a427105
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-observed-2.json
@@ -0,0 +1,218 @@
+{
+  "schema": "actor-context-probe/1",
+  "boot_id": "0f93183c-c3b0-46fa-b016-088783da8d52",
+  "diagnostic_bound": 64,
+  "current_ancestry": {
+    "rows": [
+      {
+        "pid": 1438795,
+        "ppid": 1438775,
+        "start_ticks": 87261796,
+        "comm": "python3"
+      },
+      {
+        "pid": 1438775,
+        "ppid": 1438768,
+        "start_ticks": 87261790,
+        "comm": "uv"
+      },
+      {
+        "pid": 1438768,
+        "ppid": 563897,
+        "start_ticks": 87261789,
+        "comm": "bash"
+      },
+      {
+        "pid": 563897,
+        "ppid": 563508,
+        "start_ticks": 84673165,
+        "comm": "claude"
+      },
+      {
+        "pid": 563508,
+        "ppid": 1212,
+        "start_ticks": 84673132,
+        "comm": "bash"
+      },
+      {
+        "pid": 1212,
+        "ppid": 454,
+        "start_ticks": 83215916,
+        "comm": "orca-ide"
+      },
+      {
+        "pid": 454,
+        "ppid": 393,
+        "start_ticks": 83215809,
+        "comm": "orca-ide"
+      },
+      {
+        "pid": 393,
+        "ppid": 1,
+        "start_ticks": 83215792,
+        "comm": "orca-ide"
+      },
+      {
+        "pid": 1,
+        "ppid": 0,
+        "start_ticks": 83215682,
+        "comm": "coder"
+      }
+    ],
+    "stop": "root"
+  },
+  "controlled_children": [
+    {
+      "rows": [
+        {
+          "pid": 1438796,
+          "ppid": 1438795,
+          "start_ticks": 87261798,
+          "comm": "python3"
+        },
+        {
+          "pid": 1438795,
+          "ppid": 1438775,
+          "start_ticks": 87261796,
+          "comm": "python3"
+        },
+        {
+          "pid": 1438775,
+          "ppid": 1438768,
+          "start_ticks": 87261790,
+          "comm": "uv"
+        },
+        {
+          "pid": 1438768,
+          "ppid": 563897,
+          "start_ticks": 87261789,
+          "comm": "bash"
+        },
+        {
+          "pid": 563897,
+          "ppid": 563508,
+          "start_ticks": 84673165,
+          "comm": "claude"
+        },
+        {
+          "pid": 563508,
+          "ppid": 1212,
+          "start_ticks": 84673132,
+          "comm": "bash"
+        },
+        {
+          "pid": 1212,
+          "ppid": 454,
+          "start_ticks": 83215916,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 454,
+          "ppid": 393,
+          "start_ticks": 83215809,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 393,
+          "ppid": 1,
+          "start_ticks": 83215792,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 1,
+          "ppid": 0,
+          "start_ticks": 83215682,
+          "comm": "coder"
+        }
+      ],
+      "stop": "root"
+    },
+    {
+      "rows": [
+        {
+          "pid": 1438797,
+          "ppid": 1438795,
+          "start_ticks": 87261798,
+          "comm": "python3"
+        },
+        {
+          "pid": 1438795,
+          "ppid": 1438775,
+          "start_ticks": 87261796,
+          "comm": "python3"
+        },
+        {
+          "pid": 1438775,
+          "ppid": 1438768,
+          "start_ticks": 87261790,
+          "comm": "uv"
+        },
+        {
+          "pid": 1438768,
+          "ppid": 563897,
+          "start_ticks": 87261789,
+          "comm": "bash"
+        },
+        {
+          "pid": 563897,
+          "ppid": 563508,
+          "start_ticks": 84673165,
+          "comm": "claude"
+        },
+        {
+          "pid": 563508,
+          "ppid": 1212,
+          "start_ticks": 84673132,
+          "comm": "bash"
+        },
+        {
+          "pid": 1212,
+          "ppid": 454,
+          "start_ticks": 83215916,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 454,
+          "ppid": 393,
+          "start_ticks": 83215809,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 393,
+          "ppid": 1,
+          "start_ticks": 83215792,
+          "comm": "orca-ide"
+        },
+        {
+          "pid": 1,
+          "ppid": 0,
+          "start_ticks": 83215682,
+          "comm": "coder"
+        }
+      ],
+      "stop": "root"
+    }
+  ],
+  "controlled_result": {
+    "both_children_match_one_ancestor": [
+      true,
+      true
+    ],
+    "different_start_identity_rejected": true,
+    "nonmatching_pid_rejected": true,
+    "session_reset_observed": false,
+    "meaning": "Kernel ancestry alone does not encode two logical session memberships. This is a controlled topology check, not a real Claude reset observation."
+  },
+  "runtime_cases_not_observed": [
+    "real Claude /clear with old governed child and new ordinary session",
+    "real resume/fork across Claude processes",
+    "main/subagent/nested Bash and Monitor hook event identities",
+    "same-worktree human terminal versus actual claim-launched agent",
+    "detached/reparented actual agent job",
+    "actual process ID reuse or reboot",
+    "release of real bound session while old background child remains alive"
+  ],
+  "gate": "BLOCKED",
+  "self_checks": 3,
+  "production_changes": false
+}
diff --git a/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-report.md b/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-report.md
new file mode 100644
index 00000000..27dd56f4
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206/artifacts/actor-context-report.md
@@ -0,0 +1,34 @@
+# Actor-context feasibility gate
+
+## Scope and result
+2026-11-06. B-CTX result: BLOCKED, not PASS. Task 1 delivered log-only feasibility work, not enforcement. No global hook, Claude settings, repository hooksPath or claim launch was changed. Three controlled assertions passed; actual session-reset/resume identity is not proven. Production enforcement Tasks 2-6 have not started.
+
+## Reproducible probe and observations
+Run `bash ./artifacts/actor-context-probe.sh` from this package directory. It uses `uv run --no-project python -I -`, reads kernel stat/comm/boot identity, prints JSON to stdout, and closes/reaps its two controlled children in finally. It neither reads nor emits argv/environment secrets. `bash -n` passed and the actual run exited 0. The first capture is `./artifacts/actor-context-observed.json`. Its `removed_membership_rejected` label was wrong: the assertion checks PID zero, not removal. The corrected script was rerun successfully; current output is `./artifacts/actor-context-observed-2.json`, labelled `nonmatching_pid_rejected`. The original capture remains unchanged for provenance. Both runs exit 0 with three controlled assertions; neither proves release or actual session reset.
+
+The observed current ancestry reached the root in nine rows: diagnostic Python -> UV -> Bash -> actual Claude -> Bash -> Orca processes -> container init. The actual Claude PID in that capture is 563897 with start_ticks 84673165. This proves the current Bash-tool process is a Claude descendant; it does not prove any other actor or lifecycle behavior.
+
+The controlled probe created two simultaneously live child processes under one controller. Both matched the same registered ancestor (PID and start ticks). A wrong start identity did not match, and a nonmatching PID (zero) did not match. That assertion does not test membership removal or release. These are three assertion-based self-checks. No actual PID reuse or reboot was induced. The 64-hop traversal cap is a diagnostic bound, not a measured safe production bound. Exhaustion is returned explicitly, never interpreted as a trusted human.
+
+## Required lifecycle cases
+| Case | Evidence | Result |
+|---|---|---|
+| Current main Bash tool ancestry | actor-context-observed.json current_ancestry | observed Claude ancestor |
+| Main claim-launched session binding | no implemented pipeline launcher in this checkout | unavailable |
+| Subagent and nested Git/hook identities | no real pre-push hook/event capture | unavailable |
+| Background Bash/Monitor descendants | only controlled Python children captured | actual harness behavior unavailable |
+| Concurrent same-worktree human push | no independent human terminal fixture executed | unavailable |
+| Ordinary Claude session in same worktree | not launched/observed by this probe | unavailable |
+| Detached/reparented actual agent job | not observed | unavailable |
+| Exit and PID reuse / boot change | wrong start and nonmatching PID rejected synthetically | actual reuse/reboot unavailable |
+| Resume into a new Claude process | not observed | unavailable |
+| /clear/fork with an old live governed child | controlled siblings share one ancestor; actual Claude reset not observed | decisive distinction unproven |
+| Release with old background child alive | no membership removal or release was exercised | actual session lifecycle unavailable |
+| Traversal bound exhaustion | explicit stop field in probe | production bound unproven |
+
+## Missing integration contract and implementation stop
+The candidate registers a Claude ancestor by session ID, PID, start identity and boot identity. Kernel parentage does not itself carry a logical Claude session ID. If one Claude process is reused for an ordinary session while an old governed child survives, both descendants can still match that one ancestor. Keeping registration can restrict the ordinary session; deleting it can release the old governed child. This is a conditional design limitation, not a claim that a real /clear was observed here.
+
+The missing contract must bind each supported tool-execution process/job to its actual logical session generation, preserve that identity for its descendants, refresh it on resume, and distinguish new ordinary work after reset from old governed children. Release and detached/reparented-job behavior need explicit lifetime semantics. An agent-editable environment label or a worktree marker is not proof. Existing session-name.sh explicitly treats /clear and resume as the same launch for naming and fails open on unreadable process data; that naming helper is not this authorization contract.
+
+New launcher/harness integration to supply the distinction is not authorized by the current plan's constraints. A real bounded harness experiment could establish that the unsupported topology never occurs, but no such evidence is present and synthetic siblings cannot establish that result. Therefore B-CTX remains BLOCKED. Stop before Task 2; do not install the text guard as a supposedly complete feature and do not weaken same-worktree human isolation. Full Task 1 acceptance is not claimed solely because this report exists.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
