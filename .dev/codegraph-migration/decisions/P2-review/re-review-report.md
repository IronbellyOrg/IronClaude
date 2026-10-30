# P2 re-review report: revised Phase 2 spec and Coder handoff (issue #323)

Reviewer: independent adversarial re-review, 2026-10-29. Deliverables: A = `specs/phase-2-codegraph-install-spec.md` (643 lines), B = `handoff/coder-handoff-prompt.md` (79 lines), C = `handoff/coder-handoff-context.md` (129 lines), all under `.dev/codegraph-migration/`. First review: `decisions/P2-review/review-report.md`.

## Verdict: FAIL

- First-review findings: 15 FIXED, 3 PARTLY FIXED, 0 NOT FIXED.
- New findings: 15 (1 CRITICAL, 3 IMPORTANT, 11 MINOR).
- The main blocker is new sandbox evidence from this re-review: running `codegraph status` while an `init` is in progress makes the init fail and leaves an empty index (3 of 3 trials). The revised hook (A §3.2) and the guidance (A §3.4, C §2.3) both rely on `status` being safe and conclusive at exactly that moment. The first review's own suggested fix ("decide from `codegraph status`") was therefore unsafe, and the author followed it.

## 1. Status of the 18 first-review findings

| # | Status | Evidence |
|---|---|---|
| 1 | PARTLY FIXED | Probes 4-6 were added (`probe-results.md:9-11`). The unconditional rebuild was replaced by a PID-file and `status` decision (A:204-220, D15 A:626). But the new logic calls `status` while a run may be building, which destroys that run (new 1). It also has PID-file races (new 3), and its guidance guard never matches (new 2). |
| 2 | FIXED | The Coder gap is stated at A:241. B:20 requires the seed and a one-time append. C:50-52 carries the exact block. Decision D19 is at A:630. |
| 3 | FIXED | The premise and probe are at A:92, and T2 step 1 is at A:402-409. A residual weakness in the probe's assertion is new 8. |
| 4 | FIXED | Shim dir at A:304-305, PATH rebuilt at A:308, `REAL_HOME` at A:301, cleanup trap at A:303, `--no-sync` at A:315/322/327. `bash -n` on the extracted A:297-344 passes. A new defect in the real-HOME check is new 6. |
| 5 | FIXED | A:526 now names the branch. I ran it: "no pull requests found for branch …", exit 1, which is not a usage error. `gh pr checks <branch> --repo …` (A:527) gives the same message. |
| 6 | PARTLY FIXED | T0 (A:363-373) commits, pushes and posts the handoff, and §7 item 5 (A:574) names the human step. But the T11 merge gate (A:529) checks only Coder step 1 (the bake), not step 2 (pin-agnostic contract tests). Its `CODEGRAPH` alternative also matches any env line (new 9). |
| 7 | FIXED | The pointer file is at A:69, and the hook reads it first (A:206). The PATH warning is at A:69, the tests at A:225 and U24 (A:278). A residual gap in the guidance is new 13. |
| 8 | FIXED | Baseline list at A:357, kept in the evidence dir and committed with T0 (A:361); the `comm -13` diff is at A:514. A residual weakness is new 12. |
| 9 | FIXED | A:478 checks each file in a loop. |
| 10 | FIXED | A:383 adds `--clobber` (the flag exists in gh 2.103.3), and A:384-390 does a heredoc `diff`. I ran the grep/diff against W4's `/tmp/codegraph-eval.fQfO/dl/SHA256SUMS`: exit 0, no output. |
| 11 | FIXED | A:59 now says the order only keeps the output readable and that the retire step runs regardless. This matches Phase 1 §3.3 (non-fatal, own try/except) and the test at A:281. |
| 12 | FIXED | A:249 cites `:410-416`. `pytest.fail` is at `tests/cli/test_install_mcp_tavily.py:416`. A related new problem is new 10: Phase 1 deletes those lines. |
| 13 | FIXED | The `cmd=` variable is gone from §3.2. A new literal-copy quoting bug is new 5. |
| 14 | FIXED | The receipt is written before the rename and the links (A:78-80), "complete" is set last, and A:112 states the "added before created" rule. |
| 15 | FIXED | Phase 1 §3 is now written (`phase-1-removal-spec.md:303-376`). A:59, A:100 and A:104 cite its §3.3. C:54-60 matches Phase 1 §3.2: the cbm matcher, Tier R rows (a)-(c), the Tier K current-pin `serena` entry KEPT with the printed hint, and placement after the codegraph phase. One unflagged claim that conflicts with Phase 1 §3.6 is new 15. |
| 16 | FIXED | The URL is quoted at B:24, with "keep the quotes". The marker sentence is at B:18. A new duplicated sentence is new 11. |
| 17 | FIXED | Headless cost and opt-out at A:223 and A:229; the T7 docs check is at A:479; the opt-out hook test is at A:225. |
| 18 | PARTLY FIXED | T2 now asserts the dispatch through `-k codegraph` (A:414), and layer-2 expectations are assertions. But A:319 still says "compared with P2-add-json-shape.json by eye", and A:340's `grep -i 'connected'` also matches "disconnected" (new 7). |

## 2. New findings

1. **CRITICAL. `codegraph status` during a running `init` destroys the init and reports a live build as "never finished". The hook and the guidance call it at exactly that moment.**
   - Locations:
     - the hook's `status` branch (A:216);
     - the §3.1 rows that rely on it: A:194 ("second session"), A:195 ("Truncated or still building: the hook does nothing") and A:193;
     - the D15 rationale (A:626);
     - the guidance "If `codegraph status` says…" (A:237, copied to C:52);
     - the Coder advice "A Coder-side init needs no marker: the hook detects a complete index" (C:48, B:18);
     - probe 4 (`probe-results.md:9`), which tested `status` only on finished or killed indexes.
   - Evidence (this re-review, codegraph 1.6.2 from the W4 bundle, fresh sandbox `HOME` under `/tmp`, telemetry off, a clone of this worktree with 904 files):
     - Control: `init` alone exits 0 in 6 s, and `status` afterwards shows "Index is up to date", 904 files.
     - `status` about 1 s into an `init`, three trials: each time `status` printed "⚠ The last index run never finished (killed mid-index?)" with exit 0. Each time the init then failed with "■ Failed: store worker: database is locked", exit 1. The final `status` showed "never finished", Files: 0.
     - `status` at about 2 s: `status` exited 1 and the init survived. The outcome depends on timing.
   - Consequences:
     - (a) In the main Coder flow (Coder or Orca creates a worktree, starts a background init, and Claude opens in it), the hook's job sees a database without a marker and runs `status`, which kills Coder's init. It then logs "truncated index not built by IronClaude" and stops, so the checkout stays empty.
     - (b) An agent following §3.4 runs `status` during the hook's own init and kills it.
     - (c) "Never finished" cannot tell "killed" from "still building".
   - Fix:
     - Never run `status` (or any other codegraph command that opens the database) on a checkout where a run may be active.
     - Drop the hook's "mark a foreign index" branch, or gate it on a verified "no codegraph process for `$top`" check (see 2) plus `.codegraph/codegraph.lock` handling. Re-probe `status` against `index`, against a live daemon and against a second `status`.
     - Rewrite §3.4, C §2.3 and B:18 to match. Tell Coder that its own automation must write a completion signal, or must avoid racing the first session.
     - Record this probe as row 7 of `probe-results.md`.

2. **IMPORTANT. The guidance's safety guard `pgrep -f 'codegraph (init|index)'` never matches a running codegraph.**
   - Location: A:237, C:52 (and therefore Coder's seed text).
   - Evidence: `~/.codegraph/versions/v1.6.2/bin/codegraph` is a `sh` launcher that ends with `exec "$DIR/node" --liftoff-only … "$DIR/lib/dist/bin/codegraph.js" "$@"`. A live init's command line is therefore `…/node … …/codegraph.js init --yes <top>`, and "codegraph" is followed by ".js", not a space.
   - Reproduced: a process with that argv tail is invisible to `pgrep -af 'codegraph (init|index)'` (exit 1). `pgrep -af 'codegraph\.js (init|index)'` finds it.
   - The hook's own job (`sh -c "$JOB" _ <cg> …`) never matches either. So the guard always says "nothing running", and the agent runs `index` concurrently with an init, which is the probe-6 empty-index outcome.
   - Fix: use `pgrep -f 'codegraph\.js (init|index)'` (or `pgrep -f "codegraph\.js (init|index).*$top"`). Add a layer-2 or hook test that runs the real launcher and asserts that the pattern matches.

3. **IMPORTANT. The PID file and the marker have races and lifecycle bugs, so the "own interrupted run" rule fails in common cases.**
   - Location: A:209-220 (steps 5-7 and the JOB), the §3.1 row A:193, the A:190/A:220 "concurrent init fails cleanly (probe 2)" claims, and the hook test list A:225.
   - Evidence, from the spec text and a new probe:
     - (a) Read-then-write is not atomic, and the job never re-checks that `prev` is dead. Two sessions starting together in a new worktree (the parallel headless case at A:223, or Orca): job B reads job A's live PID as `prev`, sees a database plus "never finished" (A is building, new 1), and runs `index`, which is the probe-6 empty-index outcome.
     - (b) `rm -f "$3"` deletes the shared per-checkout file whatever PID it now holds, not "only its own PID file" (A:219).
     - (c) If the `codegraph` child dies (an OOM kill of the up-to-1-GB init is the likeliest interruption) but the `sh` survives, the "finally" step removes the PID file. The next session then treats the truncated index as foreign and never rebuilds it, which contradicts A:193.
     - (d) After a reboot, `kill -0` on a recycled PID can return "live" indefinitely, and the hook then skips the checkout forever.
     - (e) New probe: a second `init --yes` started 1 s into a running init prints "Already initialized … Use "codegraph index" to re-index" and exits **0** (2 of 2 trials). A job whose database check ran just before A created the database therefore runs `init && touch marker` and writes the marker while A is still building. A:190 and A:220 call this case "fails cleanly". Probe 2 tested only a simultaneous start.
   - Fix:
     - Create the PID file atomically (`set -C` or a `mkdir` lock), and abort if another live owner exists.
     - Keep a separate "own run started" record that is removed only on success.
     - Remove the PID file only when it still holds `$$`.
     - Verify the PID's identity (for example `ps -p "$pid" -o args=` contains `codegraph`).
     - Write the marker only after a positive completeness check that does not race (see 1).
     - Add tests for concurrent hook starts and for "child fails, shell survives".

4. **MINOR. The job's completeness test fails open.**
   - Location: A:216.
   - Evidence: the marker is written whenever the `status` output lacks "never finished". That includes `status` failing outright: in the 2 s trial it exited 1. A broken binary or a locked database therefore leaves a permanent marker.
   - Fix: require `status` to exit 0, contain "Index is up to date", and not contain "never finished" (probe 4 shows that "up to date" alone is not enough).

5. **MINOR. The job text cannot be the "single-quoted string" the spec says it is.**
   - Location: A:213 and A:216.
   - Evidence: the job contains `grep -q 'never finished'` (and a quoted log message). Single quotes cannot appear inside a single-quoted `sh` string, so a literal copy breaks quoting. This is the same class of bug as first-review finding 13.
   - Fix: put the job in a function the script re-invokes (`nohup sh "$0" --job "$cg" "$top" "$pidf" …`), or use double quotes inside.

6. **IMPORTANT. The layer-2 real-HOME check hashes the whole `~/.claude.json`, which the executor's own Claude Code session rewrites.**
   - Location: A:301, A:343, T9 acceptance A:499-500.
   - Evidence: `stat ~/.claude.json` showed an mtime 55 s before "now" during this review session, with many concurrent sessions in the workspace. The script runs for minutes (a 63 MB download plus an index), so step 6 fails spuriously and T9 cannot reliably print `LAYER2_OK`.
   - Fix: hash only the fields the test protects, for example `jq -S '.mcpServers' "$REAL_HOME/.claude.json" | sha256sum`, before and after.

7. **MINOR. Two layer-2 checks are still not mechanical or exact.**
   - Location: A:319, A:340.
   - Evidence: A:319 compares the stored entry with `P2-add-json-shape.json` "by eye". A:340's `grep -i 'connected'` also matches "disconnected" and "not connected".
   - Fix:
     - Replace A:319 with `jq -S . P2-add-json-shape.json` against `jq -S '.mcpServers.codegraph'`, ignoring only `command`.
     - Replace A:340 with `grep -qi 'connected' && ! grep -qiE 'disconnected|not connected|failed'`, or use the JSON-RPC fallback from the Notes.

8. **MINOR. The T2 add-json probe checks a subset of fields and conflicts with the hard rule.**
   - Location: A:405-407, A:567.
   - Evidence:
     - The `jq -e` checks `alwaysLoad`, one env key and `args`. It does not check `type`, `command` or `CODEGRAPH_NO_UPDATE_CHECK`, yet the matcher compares the whole entry (A:99).
     - The probe has no guard proving the real `~/.claude.json` was untouched.
     - A:567 allows `claude mcp add` "only [in] the §4.2 sandbox", which T2 step 1 contradicts.
   - Fix: `jq -e --argjson e '<expected JSON>' '. == $e'` (falling back to a per-field report); add the `.mcpServers` hash check from new 6; widen A:567 to "sandbox HOMEs (T2 step 1, §4.2)".

9. **MINOR. The T11 merge gate does not check Coder step 2, and its pattern is weak.**
   - Location: A:529.
   - Evidence:
     - Step 2 (contract tests accept the new state, A:590) is the gate that keeps Coder CI from breaking on the pin bump, and it is not checked.
     - `grep -E 'codegraph.*v?1\.6\.2|CODEGRAPH'` passes on any `CODEGRAPH_*` env line or comment.
     - Verified: the command fetches Coder's `Dockerfile.coder` today (671 lines, 0 `codegraph` hits, so the gate correctly reports "not present").
   - Fix: also check `.github/contract-tests/test-57-catalogue-configure.sh` on Coder `main` for a codegraph assertion (or require the two Coder PR URLs in an issue #323 comment). Tighten the bake pattern to the sha256 value from §0.

10. **MINOR. §4.1's test conventions cite lines that Phase 1 deletes.**
    - Location: A:249.
    - Evidence:
      - Phase 1 row C6 (`phase-1-removal-spec.md:35`) deletes `tests/cli/test_install_mcp_tavily.py` lines 382 to the end. On the branch Phase 2 starts from, `:383-410`, `:410-416` and `:411-460` do not exist.
      - Separately, the `_run_command` fake is installed at `:468`, outside the cited `:411-460`.
    - Fix: say "read them with `git show 55d40308:tests/cli/test_install_mcp_tavily.py`", and cite `:411-468`.

11. **MINOR. B has a duplicated sentence.**
    - Location: B:20.
    - Evidence: "Full contract and removal table: see "Context file" below." appears twice in a row.
    - Fix: delete one.

12. **MINOR. The T10 gate is green when the full test run crashes.**
    - Location: A:513-514.
    - Evidence: the pytest exit code is discarded, and the gate passes when the failing-id list is a subset of the baseline. An empty list (killed run, crash before the summary, no tests collected) therefore passes.
    - Fix: save the full output, and also require a summary line (`grep -E '[0-9]+ passed'`) and the absence of `INTERNALERROR`/`Interrupted`.

13. **MINOR. The guidance keeps a stale codegraph when an older one is first on PATH.**
    - Location: A:237, C:52.
    - Evidence: the guidance uses the pointer file only "if `codegraph` is not on PATH". In the U4/U22 case (an older `codegraph` first on PATH), agents run `init`/`index` with that version, while the hook and the MCP server use 1.6.2.
    - Fix: "Use the path in `~/.codegraph/.superclaude-bin` when that file exists; otherwise `codegraph`."

14. **MINOR. The probe evidence is internally inconsistent.**
    - Location: `probe-results.md:8-9`.
    - Evidence:
      - Row 4's note attributes "500 files, 9,926 nodes" to probe 1, but that figure appears only in row 2 (probe 2).
      - The note says that measurement came from a truncated index. That leaves row 2's "index intact … same as a clean single run" unproven: row 2 never records whether `status` showed "never finished".
      - The row order is 1, 2, 4, 5, 6, 3.
    - Fix: correct the attribution, re-run probe 2 with a "never finished" check, add the probes from new 1 and new 3(e), and order the rows.

15. **MINOR. A states that an interrupted install is retried, which Phase 1 marks UNVERIFIED.**
    - Location: A:104 ("the next run sees 'absent' and repairs it").
    - Evidence: Phase 1 §3.6 (`phase-1-removal-spec.md:374`) lists "Whether a Coder SHA-change run killed at 60 s is retried with `--force` is UNVERIFIED". Coder reruns install only when the SHA changes. If it is not retried, a kill between `remove` and `add-json` leaves the workspace with no codegraph registration until the next pin bump.
    - Fix: mark it UNVERIFIED in A, and add it to B or C as a question for the Coder agent to confirm.

## 3. Consistency checks that passed

- **Phase 1 §3 and §7 against A, B and C:**
  - The retire step is non-fatal, sits in the old Codebase Memory slot after the codegraph phase, and runs whatever the codegraph result (A:35, A:59, A:281; C:56).
  - `_remove_exact_user_entry(name, matcher)` and the direct-exec bounded wrapper live in `install_mcp.py` (A:100, A:104; Phase 1 §3.5).
  - The kept and deleted helpers (A:34; Phase 1 §7) agree.
  - The CI Claude CLI step is deleted by Phase 1 row C12 and restored by T8 (A:485; `phase-1-removal-spec.md:41`).
  - The `phase2-facts-from-phase1.md` path is written by Phase 1 T15 (`:767`) and read by B:24, C:60 and A:615.
  - The current-pin `serena-agent==1.7.0` entry is **KEPT** by IronClaude, consistently in B:14, B:57, C:58 and C:83 with Phase 1 §3.2 Tier K and §2.3.
- **A, B and C against each other:** the pin hashes (A:17-20, A:385-388, B:25, C:13-14) agree, the registration JSON (A:89, A:405, B:16, C:41) agrees, the hook description (A §3.2, B:18, C:47-48) agrees, and the ordering (A §8, B:45-53, C §5) agrees.
- **B:** 79 lines, under about 150. It is self-contained: goal, touchpoints as leads, research instruction (B:41-43), ordering, the pin, tests, commits, a PR on IronbellyOrg/Coder only, #323 comments, autonomy rules, and inline fallback facts.
- **Commands run:**
  - Layer-2 script (A:297-344): `bash -n` OK.
  - T1 hash diff: exit 0.
  - T11 `gh pr view` and `gh pr checks`: "no pull requests found", no usage error.
  - T0 `gh api …contents…?ref=<branch>`: 404 now (branch not pushed yet; expected before T0).
  - T11 merge-gate fetch: works.
  - `git clone -q --no-hardlinks <worktree>` checks out `ironbelly/feat-codememory-codegraph-init`, so layer-2 step 4 indexes the right branch.
  - `cksum` (GNU 9.7) prints `CRC SIZE`, so `cut -d' ' -f1` works.
- **Layer-2 assertions checked under `set -euo pipefail`:**
  - The shim loop tolerates a missing tool (a failed `&&` list does not trigger `-e`).
  - The negative checks use `if`.
  - The `| tee` pipelines propagate failure through `pipefail`.
  - The dead proxy (`127.0.0.1:9`) makes any `urllib` download fail, so "no download" is enforced by the phase exit code, and `cmp` proves there was no registry change.
  - `claude` (`/usr/local/bin`) and `node` (`/usr/local/bin`) are shimmed.
  - `readlink`, `pkill`, `cmp` and `sha256sum` resolve under `/usr/bin`.
  - `.venv` interpreter links are absolute, so a moved `HOME` does not break `uv run --no-sync`.
- **Hook foreground cost:** steps 1-6 are `cat`, `git rev-parse`, `stat`, `mkdir`, `cksum` and `kill -0`, well within the 5 s budget. `nohup … </dev/null >>log 2>&1 &` detaches every descriptor.

## 4. Self-audit

- **Read in full:** the first review report; A (all 643 lines); B; C; `probe-results.md`; the brief `P2-phase2-spec.md`; Phase 1 spec §2-§3 (`:257-381`) and §7-§8.0 plus T0/T1 (`:579-668`); the Phase 1 rows C6, C12 and T15 (by grep).
- **Source checked:** `tests/cli/test_install_mcp_tavily.py:400-468` (the citation for finding 12, and the fake at `:468`); `install_mcp.py:714-760` (the `CLAUDE_CONFIG_DIR` path resolution used by layer 2); the codegraph launcher `bin/codegraph` (the `exec node … codegraph.js` line).
- **Probes run (sandbox `HOME` and clones under `/tmp`, telemetry and update check off, each directory removed afterwards):**
  - `init` alone;
  - `init` plus `status` at about 1 s (3 trials), at about 2 s and at 1, 2 and 3 s;
  - `init` plus a second `init` at about 1 s (3 trials);
  - a `pgrep` pattern test against a stand-in process with the launcher's argv;
  - a test of which branch a worktree clone checks out.
- **Not done:** no repository file other than this report was edited. I ran no `superclaude install`, no `claude mcp add/remove`, no `make sync-dev`, no full test suite and no git commit or push. I did not run real `claude mcp add-json` (it is forbidden here, and is T2's job), and I did not check the Coder `path:line` citations at `e25f787c`. The macOS `cksum` output format and whether Claude Code kills the hook's process group when a session ends are UNVERIFIED.
