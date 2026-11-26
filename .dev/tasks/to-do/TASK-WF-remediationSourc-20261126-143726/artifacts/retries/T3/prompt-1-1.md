a9fc1ce2ec233f8373318a94053ad56959ea7755
Review one task for spec compliance.

Task brief: ## Task 3: Replace the body of `_free_port()` with the window-aware draw

Depends on: Task 2

Edit `tests/unit/test_ccsession_tiers.py` only. Keep `def _free_port() -> int:` and replace its body with: compute `top = _ephemeral_low() - 1 - models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1)`; if `top >= _FREE_PORT_FLOOR`, loop up to `_FREE_PORT_TRIES` times, draw `base = random.randrange(_FREE_PORT_FLOOR, top + 1)` (call it through the `random` module attribute so a test can patch it) and return `base` when `_window_binds(base)` is true; after the loop, or when `top < _FREE_PORT_FLOOR`, fall back to the original body (`bind(("127.0.0.1", 0))` and return the port). Add a docstring or comment saying why: a `bind(0)` base is in the range the kernel uses for outgoing connections and base + 101 then collides with other processes' connections (issue 352).

Acceptance criteria:
T3.AC1: `_free_port()` keeps its signature and returns an `int`; on this host (range start 32768) every call returns a base with `base + models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1) < 32768`; the three tests that patch the module attribute `_free_port` (`test_free_port_clear_of_skips_a_port_in_the_shim_window`, `test_free_port_clear_of_fails_loudly_at_the_bound`, `test_forced_in_window_shim_port_is_skipped`) pass unchanged.
T3.AC2: Both new tests now pass: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts= -k "free_port_window or free_port_skips"` (output in `./artifacts/t3-green.log`).
T3.AC3: The whole file passes: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts=` (output in `./artifacts/t3-whole-file.log`), including the six launcher tests that call `_free_port_clear_of` (their calls are at lines 1920, 2006, 2282, 2328, 2355 and 2491 of the unmodified file), `test_a_busy_shim_is_never_stopped_by_a_new_launch`, `test_tiers_off_launch_never_takes_over_a_tier_shim`, `test_upgraded_code_starts_a_new_shim_and_keeps_the_old` and `test_relative_defaults_path_keeps_each_directory_on_its_own_shim`.
T3.AC4: Load check, seven shim tests: `taskset -c 0-3 uv run python .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/load_repro.py --repo . --out .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/fixed --tests --rounds 4 --parallel 8 --burners 16 --timeout 700 --tag fixed` ends with 0 failed process-runs of 32 and no `shim failed to start` in any log (the unfixed rate was 8 to 19 percent of process-runs); copy `summary-fixed.json` from that folder to `./artifacts/t3-load-summary.json`. Any process log that shows "shim failed to start" is recorded in the final report with the port it names and whether that port is below the kernel's local-port range start (32768 on this host); such a failure counts against the claim that the fix is sufficient and is reported as it is; the run is never repeated until it passes.
T3.AC5: Load check, whole file: this is the issue's own criterion, 20 consecutive whole-file runs under the same load. The harness takes long under load: create its `--out` folder first with `mkdir -p <its --out folder>` (the harness creates that folder only after the shell has opened the log, so the redirect would fail without it), then start the command detached (for example `nohup <command> > <its --out folder>/harness.log 2>&1 &`) and poll for its `summary-<tag>.json` file with short checks, because a cut-off foreground call leaves the 16 burners running and writes no summary.
  - First check that no leftover test process from an earlier run is still running, and never touch the shared model-alias shim that live sessions use (it runs from `$HOME/.claude/skills/ccsession-tag/`): each of `pgrep -af "$(pwd -P)/.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/.*[s]him-under-test.py"` (the private shim copies of this checkout's harness runs), `pgrep -af "$(pwd -P)/.venv/bin/python[^ ]* -c [w]hile True: pass"` (the burners started from this checkout's interpreter) and `pgrep -af "$(pwd -P)/src/superclaude/skills/ccsession-tag/[l]ocal-gateway-alias-proxy.py"` (the fixture shims of this checkout's tests) prints nothing; every pattern starts with this checkout's own resolved path, so it cannot match another session's processes or the shared shim; kill only the processes these three commands list (the bracket in each pattern keeps `pgrep` from matching its own shell).
  - Then time one loaded whole-file run: `taskset -c 0-3 uv run python .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/load_repro.py --repo . --out .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/fixed-whole-timing --tests --whole-file --rounds 1 --parallel 1 --burners 16 --timeout 1800 --tag timing`, and read its `secs` (with `--parallel 1` that is the true duration).
  - Run the 20 runs: `taskset -c 0-3 uv run python .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/load_repro.py --repo . --out .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/fixed-whole --tests --whole-file --rounds 20 --parallel 1 --burners 16 --timeout <the larger of 600 and twice the timing run's secs, rounded up to a whole number of seconds> --tag wholefile`; the check passes only when all 20 results have `rc` 0. A result with `rc: "timeout"` fails the check; after any timeout or other abort, kill only the processes the three commands of the first step list, before doing anything else.
  - A passed run must not show more skipped tests than the unloaded whole-file run in `./artifacts/t3-whole-file.log`: compare the last line of each process log (a skipped test returns exit code 0 and the summary JSON does not count skips). Copy `summary-wholefile.json` to `./artifacts/t3-wholefile-summary.json`.
  - The earlier shape of 5 rounds of 4 parallel processes (`--rounds 5 --parallel 4 --tag wholefile4`, output folder `.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/fixed-whole4`) may be run as an extra and is not counted toward the criterion; it can share a hash-derived port between processes in `test_show_all_launch_runs_its_own_shim`.
  - A failure of a test that has nothing to do with shims is recorded by name; run that single test alone and unloaded (`uv run pytest <its node id> -q -p no:cacheprovider -o addopts=`); its run counts as a failed run in the 20-run result, the final report names the test and says whether the failure is shim-related, and no run is repeated until it passes; a process log that shows "shim failed to start" is recorded with the port it names and whether that port is below 32768, exactly as for the seven-shim-test check. The wall-clock tests that can fail under load without any port involvement are `test_cooldown_expires_and_repeats` (near lines 1177-1189 of the unmodified test file) and the tests that set `CCSESSION_FIRST_BYTE_TIMEOUT` to 1 (near lines 1204, 1244, 1543, 1554, 1752 and 2212); the final report lists any of them that failed.
T3.AC6: `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py` report nothing new for the changed hunks.
T3.AC7: `git diff --stat` shows only `tests/unit/test_ccsession_tiers.py` changed apart from the files this plan writes under `.dev/tasks/`; no path under `.claude/` or `.dev/issues/` is changed.
Global constraints: ## Constraints

- Only `tests/unit/test_ccsession_tiers.py` changes, plus files this plan writes under `./artifacts/`. No production file changes: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/models.py` and `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` stay as they are.
- No assertion of an existing test is weakened or removed. `_free_port_clear_of` (line 832) and its #443 guard comment (line 833) are untouched. The signature `def _free_port() -> int:` stays, because `_free_port_clear_of`, the `shim` fixture (line 850), the unreachable upstream (line 1213) and the three tests that patch the module attribute `_free_port` (lines 1865, 1879, 1907) rely on it.
- The step and the attempt count are read from `models.SHIM_PORT_STEP` and `models.SHIM_PORT_ATTEMPTS`, never written as 101 and 6.
- Ruff for this repo selects E, F, I, N, W and TID with line length 88 (`pyproject.toml`, `[tool.ruff]`): every added line stays within 88 characters and imports stay sorted. `ruff check` ignores E501, so only `uv run ruff format --check` enforces the 88 columns; run `uv run ruff format` on the file so long names such as the second new test's signature are wrapped.
- Do not use `git stash`. Do not stage or commit anything under `.claude/` or `.dev/issues/`.
- Load-harness output folders go under `.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/` (untracked); only small summary files are copied into `./artifacts/`. `./artifacts/` in this plan always means this package's own `artifacts/` directory (the folder next to this plan file), while commands run from the repository root.
- Known limits to keep visible in the final report, not to hide: a below-range port can still be held by a long-lived service, and two concurrent test processes can draw overlapping windows (estimated about 11 in 22,000 per pair, unmeasured), which the pick-time bind check reduces; on a host whose local-port range starts at or below 10506 the new `_free_port()` falls back to the old behaviour; the single `port 36877 is owned by another service` failure had no identified holder and is only probably reduced; the CI runner and the original release-gate host were never observed, so the fixed-tree load runs are the real measurement.
- Out of scope (separate issues, not part of this plan): the launcher keeping the started shim's stderr and noticing an exited shim, and the macOS-only `e.errno == 48` check at `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:1054`.
- Review record: the two last edits to this plan, the cleanup patterns tied to this checkout's own path and the `mkdir -p` for the log folder of the load runs, were made after the cap of 3 reviews had been reached, with the go of the IronFlow session (which is helping Clay push E2); they were checked by a read-only check of those lines only, not by a fourth full review.
Start sha: a9fc1ce2ec233f8373318a94053ad56959ea7755
Diff against the start snapshot: diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index 76ce9df1b..a05d621ee 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -848,6 +848,15 @@ def _window_binds(base: int) -> bool:
 
 
 def _free_port() -> int:
+    # #352: a bind(0) base lies in the range the kernel uses for outgoing
+    # connections, and base + 101 then collides with other processes' connections.
+    # Draw the base below that range, and keep it only if the whole window binds.
+    top = _ephemeral_low() - 1 - models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1)
+    if top >= _FREE_PORT_FLOOR:
+        for _ in range(_FREE_PORT_TRIES):
+            base = random.randrange(_FREE_PORT_FLOOR, top + 1)
+            if _window_binds(base):
+                return base
     with socket.socket() as s:
         s.bind(("127.0.0.1", 0))
         return s.getsockname()[1]

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-green.log (full contents, line numbers added) ---
1: ..                                                                       [100%]
2: 2 passed, 217 deselected in 0.48s
3: rc=0
4: 

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-ruff.log (full contents, line numbers added) ---
1: $ uv run ruff check tests/unit/test_ccsession_tiers.py
2: All checks passed!
3: $ uv run ruff format --check tests/unit/test_ccsession_tiers.py
4: 1 file already formatted
5: 

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-whole-file.log (full contents, line numbers added) ---
1: ........................................................................ [ 32%]
2: ........................................................................ [ 65%]
3: ........................................................................ [ 98%]
4: ...                                                                      [100%]
5: 219 passed in 188.74s (0:03:08)
6: rc=0
7: 

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-load-summary.json (full contents, line numbers added) ---
1: {
2:  "mode": "tests",
3:  "results": [
4:   {
5:    "round": 0,
6:    "log": "fixed-r0-p0.log",
7:    "rc": 0,
8:    "secs": 83.7,
9:    "failed": [],
10:    "shim_failed_to_start": 0,
11:    "another_shim": 0
12:   },
13:   {
14:    "round": 0,
15:    "log": "fixed-r0-p1.log",
16:    "rc": 0,
17:    "secs": 83.9,
18:    "failed": [],
19:    "shim_failed_to_start": 0,
20:    "another_shim": 0
21:   },
22:   {
23:    "round": 0,
24:    "log": "fixed-r0-p2.log",
25:    "rc": 0,
26:    "secs": 84.3,
27:    "failed": [],
28:    "shim_failed_to_start": 0,
29:    "another_shim": 0
30:   },
31:   {
32:    "round": 0,
33:    "log": "fixed-r0-p3.log",
34:    "rc": 0,
35:    "secs": 84.3,
36:    "failed": [],
37:    "shim_failed_to_start": 0,
38:    "another_shim": 0
39:   },
40:   {
41:    "round": 0,
42:    "log": "fixed-r0-p4.log",
43:    "rc": 0,
44:    "secs": 84.3,
45:    "failed": [],
46:    "shim_failed_to_start": 0,
47:    "another_shim": 0
48:   },
49:   {
50:    "round": 0,
51:    "log": "fixed-r0-p5.log",
52:    "rc": 0,
53:    "secs": 84.3,
54:    "failed": [],
55:    "shim_failed_to_start": 0,
56:    "another_shim": 0
57:   },
58:   {
59:    "round": 0,
60:    "log": "fixed-r0-p6.log",
61:    "rc": 0,
62:    "secs": 84.2,
63:    "failed": [],
64:    "shim_failed_to_start": 0,
65:    "another_shim": 0
66:   },
67:   {
68:    "round": 0,
69:    "log": "fixed-r0-p7.log",
70:    "rc": 0,
71:    "secs": 84.2,
72:    "failed": [],
73:    "shim_failed_to_start": 0,
74:    "another_shim": 0
75:   },
76:   {
77:    "round": 1,
78:    "log": "fixed-r1-p0.log",
79:    "rc": 0,
80:    "secs": 81.6,
81:    "failed": [],
82:    "shim_failed_to_start": 0,
83:    "another_shim": 0
84:   },
85:   {
86:    "round": 1,
87:    "log": "fixed-r1-p1.log",
88:    "rc": 0,
89:    "secs": 81.9,
90:    "failed": [],
91:    "shim_failed_to_start": 0,
92:    "another_shim": 0
93:   },
94:   {
95:    "round": 1,
96:    "log": "fixed-r1-p2.log",
97:    "rc": 1,
98:    "secs": 85.8,
99:    "failed": [
100:     "tests/unit/test_ccsession_tiers.py::test_every_shim_launch_gets_the_port_for_its_settings"
101:    ],
102:    "shim_failed_to_start": 0,
103:    "another_shim": 2
104:   },
105:   {
106:    "round": 1,
107:    "log": "fixed-r1-p3.log",
108:    "rc": 0,
109:    "secs": 85.7,
110:    "failed": [],
111:    "shim_failed_to_start": 0,
112:    "another_shim": 0
113:   },
114:   {
115:    "round": 1,
116:    "log": "fixed-r1-p4.log",
117:    "rc": 0,
118:    "secs": 85.7,
119:    "failed": [],
120:    "shim_failed_to_start": 0,
121:    "another_shim": 0
122:   },
123:   {
124:    "round": 1,
125:    "log": "fixed-r1-p5.log",
126:    "rc": 0,
127:    "secs": 85.7,
128:    "failed": [],
129:    "shim_failed_to_start": 0,
130:    "another_shim": 0
131:   },
132:   {
133:    "round": 1,
134:    "log": "fixed-r1-p6.log",
135:    "rc": 0,
136:    "secs": 85.7,
137:    "failed": [],
138:    "shim_failed_to_start": 0,
139:    "another_shim": 0
140:   },
141:   {
142:    "round": 1,
143:    "log": "fixed-r1-p7.log",
144:    "rc": 0,
145:    "secs": 85.7,
146:    "failed": [],
147:    "shim_failed_to_start": 0,
148:    "another_shim": 0
149:   },
150:   {
151:    "round": 2,
152:    "log": "fixed-r2-p0.log",
153:    "rc": 1,
154:    "secs": 85.1,
155:    "failed": [
156:     "tests/unit/test_ccsession_tiers.py::test_every_shim_launch_gets_the_port_for_its_settings"
157:    ],
158:    "shim_failed_to_start": 0,
159:    "another_shim": 2
160:   },
161:   {
162:    "round": 2,
163:    "log": "fixed-r2-p1.log",
164:    "rc": 0,
165:    "secs": 85.1,
166:    "failed": [],
167:    "shim_failed_to_start": 0,
168:    "another_shim": 0
169:   },
170:   {
171:    "round": 2,
172:    "log": "fixed-r2-p2.log",
173:    "rc": 0,
174:    "secs": 85.1,
175:    "failed": [],
176:    "shim_failed_to_start": 0,
177:    "another_shim": 0
178:   },
179:   {
180:    "round": 2,
181:    "log": "fixed-r2-p3.log",
182:    "rc": 0,
183:    "secs": 85.1,
184:    "failed": [],
185:    "shim_failed_to_start": 0,
186:    "another_shim": 0
187:   },
188:   {
189:    "round": 2,
190:    "log": "fixed-r2-p4.log",
191:    "rc": 0,
192:    "secs": 85.1,
193:    "failed": [],
194:    "shim_failed_to_start": 0,
195:    "another_shim": 0
196:   },
197:   {
198:    "round": 2,
199:    "log": "fixed-r2-p5.log",
200:    "rc": 0,
201:    "secs": 85.1,
202:    "failed": [],
203:    "shim_failed_to_start": 0,
204:    "another_shim": 0
205:   },
206:   {
207:    "round": 2,
208:    "log": "fixed-r2-p6.log",
209:    "rc": 0,
210:    "secs": 85.1,
211:    "failed": [],
212:    "shim_failed_to_start": 0,
213:    "another_shim": 0
214:   },
215:   {
216:    "round": 2,
217:    "log": "fixed-r2-p7.log",
218:    "rc": 0,
219:    "secs": 85.1,
220:    "failed": [],
221:    "shim_failed_to_start": 0,
222:    "another_shim": 0
223:   },
224:   {
225:    "round": 3,
226:    "log": "fixed-r3-p0.log",
227:    "rc": 1,
228:    "secs": 88.1,
229:    "failed": [
230:     "tests/unit/test_ccsession_tiers.py::test_every_shim_launch_gets_the_port_for_its_settings"
231:    ],
232:    "shim_failed_to_start": 0,
233:    "another_shim": 2
234:   },
235:   {
236:    "round": 3,
237:    "log": "fixed-r3-p1.log",
238:    "rc": 0,
239:    "secs": 88.1,
240:    "failed": [],
241:    "shim_failed_to_start": 0,
242:    "another_shim": 0
243:   },
244:   {
245:    "round": 3,
246:    "log": "fixed-r3-p2.log",
247:    "rc": 0,
248:    "secs": 88.1,
249:    "failed": [],
250:    "shim_failed_to_start": 0,
251:    "another_shim": 0
252:   },
253:   {
254:    "round": 3,
255:    "log": "fixed-r3-p3.log",
256:    "rc": 0,
257:    "secs": 88.1,
258:    "failed": [],
259:    "shim_failed_to_start": 0,
260:    "another_shim": 0
261:   },
262:   {
263:    "round": 3,
264:    "log": "fixed-r3-p4.log",
265:    "rc": 0,
266:    "secs": 88.1,
267:    "failed": [],
268:    "shim_failed_to_start": 0,
269:    "another_shim": 0
270:   },
271:   {
272:    "round": 3,
273:    "log": "fixed-r3-p5.log",
274:    "rc": 0,
275:    "secs": 88.1,
276:    "failed": [],
277:    "shim_failed_to_start": 0,
278:    "another_shim": 0
279:   },
280:   {
281:    "round": 3,
282:    "log": "fixed-r3-p6.log",
283:    "rc": 0,
284:    "secs": 88.1,
285:    "failed": [],
286:    "shim_failed_to_start": 0,
287:    "another_shim": 0
288:   },
289:   {
290:    "round": 3,
291:    "log": "fixed-r3-p7.log",
292:    "rc": 0,
293:    "secs": 88.1,
294:    "failed": [],
295:    "shim_failed_to_start": 0,
296:    "another_shim": 0
297:   }
298:  ],
299:  "burners": 16,
300:  "parallel": 8,
301:  "load_before": [
302:   "4.09",
303:   "4.20",
304:   "3.77"
305:  ]
306: }

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-wholefile-summary.json (full contents, line numbers added) ---
1: {
2:  "mode": "tests",
3:  "results": [
4:   {
5:    "round": 0,
6:    "log": "wholefile-r0-p0.log",
7:    "rc": 1,
8:    "secs": 429.1,
9:    "failed": [
10:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
11:    ],
12:    "shim_failed_to_start": 0,
13:    "another_shim": 0
14:   },
15:   {
16:    "round": 1,
17:    "log": "wholefile-r1-p0.log",
18:    "rc": 1,
19:    "secs": 396.6,
20:    "failed": [
21:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
22:    ],
23:    "shim_failed_to_start": 0,
24:    "another_shim": 0
25:   },
26:   {
27:    "round": 2,
28:    "log": "wholefile-r2-p0.log",
29:    "rc": 1,
30:    "secs": 479.8,
31:    "failed": [
32:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
33:    ],
34:    "shim_failed_to_start": 0,
35:    "another_shim": 0
36:   },
37:   {
38:    "round": 3,
39:    "log": "wholefile-r3-p0.log",
40:    "rc": 1,
41:    "secs": 447.4,
42:    "failed": [
43:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
44:    ],
45:    "shim_failed_to_start": 0,
46:    "another_shim": 0
47:   },
48:   {
49:    "round": 4,
50:    "log": "wholefile-r4-p0.log",
51:    "rc": 1,
52:    "secs": 427.7,
53:    "failed": [
54:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
55:    ],
56:    "shim_failed_to_start": 0,
57:    "another_shim": 0
58:   },
59:   {
60:    "round": 5,
61:    "log": "wholefile-r5-p0.log",
62:    "rc": 1,
63:    "secs": 416.2,
64:    "failed": [
65:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
66:    ],
67:    "shim_failed_to_start": 0,
68:    "another_shim": 0
69:   },
70:   {
71:    "round": 6,
72:    "log": "wholefile-r6-p0.log",
73:    "rc": 1,
74:    "secs": 451.7,
75:    "failed": [
76:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
77:    ],
78:    "shim_failed_to_start": 0,
79:    "another_shim": 0
80:   },
81:   {
82:    "round": 7,
83:    "log": "wholefile-r7-p0.log",
84:    "rc": 1,
85:    "secs": 459.6,
86:    "failed": [
87:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
88:    ],
89:    "shim_failed_to_start": 0,
90:    "another_shim": 0
91:   },
92:   {
93:    "round": 8,
94:    "log": "wholefile-r8-p0.log",
95:    "rc": 1,
96:    "secs": 443.7,
97:    "failed": [
98:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
99:    ],
100:    "shim_failed_to_start": 0,
101:    "another_shim": 0
102:   },
103:   {
104:    "round": 9,
105:    "log": "wholefile-r9-p0.log",
106:    "rc": 1,
107:    "secs": 450.2,
108:    "failed": [
109:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
110:    ],
111:    "shim_failed_to_start": 0,
112:    "another_shim": 0
113:   },
114:   {
115:    "round": 10,
116:    "log": "wholefile-r10-p0.log",
117:    "rc": 1,
118:    "secs": 416.2,
119:    "failed": [
120:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
121:    ],
122:    "shim_failed_to_start": 0,
123:    "another_shim": 0
124:   },
125:   {
126:    "round": 11,
127:    "log": "wholefile-r11-p0.log",
128:    "rc": 1,
129:    "secs": 419.5,
130:    "failed": [
131:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
132:    ],
133:    "shim_failed_to_start": 0,
134:    "another_shim": 0
135:   },
136:   {
137:    "round": 12,
138:    "log": "wholefile-r12-p0.log",
139:    "rc": 1,
140:    "secs": 430.0,
141:    "failed": [
142:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
143:    ],
144:    "shim_failed_to_start": 0,
145:    "another_shim": 0
146:   },
147:   {
148:    "round": 13,
149:    "log": "wholefile-r13-p0.log",
150:    "rc": 1,
151:    "secs": 438.0,
152:    "failed": [
153:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
154:    ],
155:    "shim_failed_to_start": 0,
156:    "another_shim": 0
157:   },
158:   {
159:    "round": 14,
160:    "log": "wholefile-r14-p0.log",
161:    "rc": 1,
162:    "secs": 384.7,
163:    "failed": [
164:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
165:    ],
166:    "shim_failed_to_start": 0,
167:    "another_shim": 0
168:   },
169:   {
170:    "round": 15,
171:    "log": "wholefile-r15-p0.log",
172:    "rc": 1,
173:    "secs": 421.0,
174:    "failed": [
175:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
176:    ],
177:    "shim_failed_to_start": 0,
178:    "another_shim": 0
179:   },
180:   {
181:    "round": 16,
182:    "log": "wholefile-r16-p0.log",
183:    "rc": 1,
184:    "secs": 460.0,
185:    "failed": [
186:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
187:    ],
188:    "shim_failed_to_start": 0,
189:    "another_shim": 0
190:   },
191:   {
192:    "round": 17,
193:    "log": "wholefile-r17-p0.log",
194:    "rc": 1,
195:    "secs": 431.8,
196:    "failed": [
197:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
198:    ],
199:    "shim_failed_to_start": 0,
200:    "another_shim": 0
201:   },
202:   {
203:    "round": 18,
204:    "log": "wholefile-r18-p0.log",
205:    "rc": 1,
206:    "secs": 424.7,
207:    "failed": [
208:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
209:    ],
210:    "shim_failed_to_start": 0,
211:    "another_shim": 0
212:   },
213:   {
214:    "round": 19,
215:    "log": "wholefile-r19-p0.log",
216:    "rc": 1,
217:    "secs": 422.4,
218:    "failed": [
219:     "tests/unit/test_ccsession_tiers.py::test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier"
220:    ],
221:    "shim_failed_to_start": 0,
222:    "another_shim": 0
223:   }
224:  ],
225:  "burners": 16,
226:  "parallel": 1,
227:  "load_before": [
228:   "20.82",
229:   "21.74",
230:   "15.81"
231:  ]
232: }

--- untracked evidence file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-load-notes.md (full contents, line numbers added) ---
1: # T3 load-check outcomes (honest summary, written by the implementer)
2: 
3: Seven-test load check (`t3-load-summary.json`; 8 parallel processes x 4 rounds = 32 runs, 16 busy-loop burners):
4: - "shim failed to start" (the original defect): 0 of 32 runs. Unfixed file: 8 to 19 percent of runs.
5: - 3 of 32 runs failed in `test_every_shim_launch_gets_the_port_for_its_settings` with "another shim took 127.0.0.1:<port> at the same moment" (rounds 1, 2, 3, one each).
6:   That test never calls `_free_port` and sets no `CC_SHIM_PORT` (test lines 2397 to 2419): its port is `models.shim_port(4010)`, the settings hash. Not caused by this change; cause not proven (old-versus-new comparison runs did not start: relative `.venv/bin/pytest` path). Left as a follow-up.
7: 
8: Twenty whole-file runs under load (`t3-wholefile-summary.json`; one process at a time, 16 burners, timeout 945 s; timing run 472.5 s):
9: - 20 of 20 runs: `1 failed, 218 passed`; 0 "shim failed to start"; 0 "another shim took"; run times 384.7 to 479.8 s; no timeouts.
10: - The one failure in every run is `test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier` (`--model` where `--name` expected). Cause found: the harness's 223-character `--basetemp` path. Single-test checks: plain pass; `--tb=short -rf` pass; short `--basetemp` pass; long `--basetemp` FAIL on the new file and FAIL on the old (HEAD) test file. So it is a harness path-length artifact, independent of this change and of the shims.
11: - By the plan's rule it is recorded by name, run alone unloaded (passes), counts as a failed run; no run is repeated until it passes. The literal "all 20 results rc 0" is therefore NOT met by this harness.
12: 
13: Unloaded whole file (plain pytest, no harness): `219 passed` (`t3-whole-file.log`).
14: 

Codegraph context
index_state=absent checked_at=see run state worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-352 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-352
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: no dependents outside the diff are named by this task's changes; see diff.

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
