# P2 third review: Phase 2 spec and Coder handoff (issue #323)

Reviewer: independent adversarial third review, read-only, 2026-10-29. Deliverables (all under `.dev/codegraph-migration/`): A = `specs/phase-2-codegraph-install-spec.md` (692 lines), B = `handoff/coder-handoff-prompt.md` (79 lines), C = `handoff/coder-handoff-context.md` (138 lines). Prior reviews: `decisions/P2-review/review-report.md` and `re-review-report.md`.

## Verdict: FAIL

- Re-review findings 1-15: 14 FIXED, 1 PARTLY, 0 NOT. First-review partials 1, 6, 18: all FIXED.
- New findings: 17 (1 CRITICAL, 4 IMPORTANT, 12 MINOR).
- Blocker: the coordinator's hard requirement is not met as written. The §2.12 Serena rule removes only entries with "no `env`/`headers`". But the live `serena-agent==1.7.0` entry on this workspace has `"env":{}`. Coder's bundle always writes `env: {}`, and so does `claude mcp add`. A literal implementation therefore keeps exactly the entry the requirement targets. The layer-2 seed omits `env`, so the test passes anyway (new 1).
- The new hook design holds up under fresh probes:
  - probe 9 reproduced: a killed init is healed to 904 files;
  - two simultaneous inits leave a complete index (2 of 2 trials);
  - `status` and `index` during a daemon heal are harmless.
- Two hook gaps remain:
  - A `.codegraph/` directory without a database is never indexed (new 5).
  - The "a call during init is answered" claim is wrong in the real session order (new 6).

## 1. Status of earlier findings

| # | Status | Evidence |
|---|---|---|
| RR1 (CRITICAL, `status` kills init) | FIXED | The hook has no `status`/`index`/`sync` (A:229-237, D21 A:674). The guidance forbids them while a build runs (A:253, C:57). The probe is recorded as row 6 (`probe-results.md:12`). Coder is told to start only `init` when `.codegraph` is absent and never to poll `status` (C:54). |
| RR2 (pgrep pattern) | FIXED | `codegraph\.js (init|index)` is in A:253, B:27, C:53 and C:57. My sandbox: during a live init the new pattern matched 1 process and the old one 0. The suggested real-launcher test was not added; see new 17. |
| RR3 (PID-file races) | FIXED (moot) | The PID file, marker and lock were removed (A:237). |
| RR4 (completeness test fails open) | FIXED (moot) | No completeness test remains. |
| RR5 (single quotes in the job) | FIXED (moot) | No job string remains. I rendered §3.2 steps 1-6 literally as a script, and `sh -n` and `dash -n` both pass. |
| RR6 (whole `~/.claude.json` hash) | FIXED | Only `.mcpServers` is hashed (A:317, A:373, T2 A:435/439). |
| RR7 (by-eye compare, `connected` grep) | FIXED | `diff` of `jq -S 'del(.command)'` (A:336); negative grep (A:358). |
| RR8 (T2 probe subset, hard rule) | FIXED | `jq -e '. == $e'` (A:440), real-`.mcpServers` guard (A:439), hard rule widened (A:614). Residual weakness: new 11. |
| RR9 (merge gate misses step 2) | FIXED | The pinned hash in `Dockerfile.coder` and a codegraph assertion in test-57 are checked (A:574-575). I fetched test-57 today: no match, so the gate correctly says "not yet". The Serena part of step 2, added since, is not gated: new 4. |
| RR10 (citations Phase 1 deletes) | FIXED | A:265 says `git show 55d40308:…` and cites `:411-468`. Checked: `pytest.fail` is at `:416`, and `monkeypatch.setattr(install_mcp, "_run_command", run)` is at `:468`. |
| RR11 (B duplicate sentence) | FIXED | B:20 has it once. |
| RR12 (T10 green on crash) | FIXED | A:557 requires an `N passed` line and no `INTERNALERROR`/`Interrupted`/`no tests ran`. |
| RR13 (stale codegraph first on PATH) | FIXED | A:253 and C:57: "the path in `~/.codegraph/.superclaude-bin` when that file exists, else `codegraph`". |
| RR14 (probe evidence inconsistent) | PARTLY | Row order and attribution are fixed (`probe-results.md:7-16`). Probe 2 was not re-run: row 2 still says completeness is "UNVERIFIED" (`:8`), while A:237 ("harmless (rows 2-3)") and C:50 ("index complete") rely on it. My re-run shows it is in fact complete (new 7). |
| RR15 (interrupted-install retry) | FIXED | Marked UNVERIFIED at A:106; B:57 asks Coder to confirm and to add a retry. |
| First-review 1 (hook rebuild races) | FIXED | No rebuild branch remains. My sandbox reproduced probe 9: init SIGKILLed at 1.5 s left "never finished", 0 files. After one MCP client connected, the status 50 s later was 904 files, "Index is up to date", no warning. |
| First-review 6 (nothing starts Coder) | FIXED | T0 commits, pushes and posts (A:395-403); human step 5 (A:621); T11 gate (A:573-576). Gap in the gate's scope: new 4. |
| First-review 18 (weak acceptance) | FIXED | Layer-2 checks are assertions (A:332-373); T2 `-k codegraph` has a "not 0 selected" expectation (A:447). |

## 2. New findings

1. **CRITICAL. The Serena removal rule misses the live entry: it has `"env":{}`.**
   - Locations:
     - A:188 ("stdio, no `env`/`headers`");
     - T3b near-miss test "env/headers kept" (A:468);
     - layer-2 seed `SER` (A:361);
     - C:65 ("no env/headers");
     - B:14 ("every user-scope `serena` launcher entry");
     - decision file `P2-serena-entry-removal-merged.md:10`.
   - Evidence:
     - A read-only `jq` of the real `~/.claude.json` returns the `serena` entry as `{"type":"stdio","command":"uvx","args":[…"serena-agent==1.7.0"…],"env":{}}`.
     - Coder's bundle builds the entry it expects `claude mcp add` to write with `env: $e`, where `env='{}'` by default (Coder `templates/VSCode-AIDev02/catalogue/mcp-bundle-core/install.sh:80-87`, fetched today). So every bundle-written Serena entry carries `"env":{}`.
     - No plan text says "absent or empty" for Serena. Only the codebase-memory matcher does (`phase-1-removal-spec.md:313`), and Phase 1's Tier R rule has the same wording (`:315`).
     - The layer-2 seed has no `env` key, so step 6 passes while the real entry would be "kept and reported". `./update.sh` on this workspace would then leave Serena registered.
   - Fix:
     - Define the condition as "`env` and `headers` absent or `{}`" in A §2.12, C:65 and the decision file.
     - Add `"env":{}` to `SER` (A:361), and add a T3b unit case "`env: {}` is removed; a non-empty `env` is kept".
     - Add the same correction to the Phase 1 amendment list for its Tier R rows. Old IronClaude also registered through `claude mcp add`, which writes `env: {}`.

2. **IMPORTANT. The Coder agent is told to prefer a facts file that will contradict §2.12 on Serena.**
   - Location: B:24 ("prefer it where it differs"), C:68.
   - Evidence:
     - Phase 1 T15 writes `handoffs/phase2-facts-from-phase1.md` with "the retire-step behaviour" (`phase-1-removal-spec.md:767`).
     - Phase 1's behaviour is "current-pin `serena` … kept … prints `claude mcp remove serena`" (`:290`, `:325`, `:368`).
     - T3b changes that later, and no Phase 2 task updates the file. The Coder agent would therefore read that IronClaude keeps the bundle's Serena entry, and is instructed to believe it over B and C.
   - Fix: a Phase 2 task (T3b or T7) appends a §2.12 section to `phase2-facts-from-phase1.md`, with an `rg -q codegraph_ready` acceptance check. Alternatively, B and C state "for Serena removal, Phase 2 §2.12 overrides that file".

3. **IMPORTANT. Nobody owns the Phase 1 spec amendments that §2.12 depends on.**
   - Location: F18 (A:51), §9 row (A:660), D22 (A:673), decision file `:25-27`.
   - Evidence:
     - A says "Phase 1 must also amend its own spec rows … (reported to the coordinator)", but no task in §5 does it and there is no acceptance check.
     - `phase-1-removal-spec.md` still says the current-pin entry is kept:
       - DoD-3 (`:269`) and the §2.3 row (`:290`);
       - Tier K (`:325`), whose printed hint says "Coder workspaces re-add it at start";
       - §3.4, whose re-register hint uses the name `serena`, which §2.12 would remove again (`:354`);
       - the §3.6 closing condition, "a later sunset task" (`:368`).
     - The Phase 1 executor runs first, so it implements and documents the old contract. That includes its CHANGELOG entry (T12).
   - Fix: add a task (T0 or T3b step 0) that edits those Phase 1 rows, with an acceptance check such as `! rg -n 'Legacy Serena registration kept' .dev/codegraph-migration/specs/phase-1-removal-spec.md`. Or name the coordinator or F-task as owner in A §7, with the same check.

4. **IMPORTANT. The merge gate does not check that Coder's bundle stopped re-adding Serena.**
   - Location: T11 gate (A:573-576), B:49.
   - Evidence:
     - D22 and the decision file make Coder step 2's Serena retirement "the gate for steps 3-4" (merged `:16`). Without it, every Coder boot re-registers Serena ("Register what is missing", Coder bundle `install.sh:67-75`, `SERENA_PIN=1.7.0` at `:19`).
     - The gate checks only the codegraph hash and a test-57 codegraph assertion, so it passes while the requirement fails on every Coder workspace.
   - Fix: add a gate line `! gh api repos/IronbellyOrg/Coder/contents/templates/VSCode-AIDev02/catalogue/mcp-bundle-core/install.sh -H 'Accept: application/vnd.github.raw' | grep -q 'serena-agent=='`, and mention it in B:49.

5. **IMPORTANT. A `.codegraph/` directory without a database blocks indexing forever. `.codegraph/` is not self-ignoring, so this case arises from an ordinary commit.**
   - Location:
     - A:53 ("codegraph writes a self-ignoring `.codegraph/.gitignore`");
     - hook step 4 (A:233) and its test "an existing `.codegraph/` (empty dir is enough) runs nothing" (A:241);
     - A:218, C:22, C:47.
   - Evidence (my sandbox, v1.6.2, clone of this worktree):
     - `.codegraph/.gitignore` is `*` and `!.gitignore`, so `git status --short` prints `?? .codegraph/`. Any `git add -A` or `git add .` commits `.codegraph/.gitignore`. Every later clone or worktree of that repo then starts with a `.codegraph/` that has no database.
     - On such a directory the MCP server replies "No CodeGraph project is loaded for this session". 20 s later nothing had been built: no daemon heal, unlike probe 9, where a database existed. The hook skips the directory ("exists").
     - `codegraph init --yes` on the same directory built the full index (exit 0, 904 files).
     - Recovery therefore depends on the CLAUDE.md fallback, which does not reach Coder users (A:257).
   - Fix:
     - Hook step 4 tests `[ -e "$top/.codegraph/codegraph.db" ]`. A concurrent second init is harmless, see new 7.
     - Change the test to "`.codegraph/` holding only `.gitignore` → `init` runs once".
     - Correct A:53 and C:22.
     - Add `.codegraph/` to IronClaude's own `.gitignore`, and document a `core.excludesFile` entry for users.

6. **MINOR. "A tool call during the init is answered" is false when the session starts first, which is the real order.**
   - Location: A:215 (§3.1 row 2).
   - Evidence (my sandbox): the MCP client connected before `.codegraph/` existed, `init` started 1 s later, and a tool call was made about 1.5-2 s into the init.
     - Probe PE (1 trial) and PG trial 2: "No CodeGraph project is loaded", although `.codegraph/` existed.
     - PG trial 1: a partial answer ("35 symbols") where the complete index gives 76.
     - Later calls in the same session gave full answers, and the index ended complete (3 of 3), so nothing is lost. Probe 8 started the client after the init.
   - Fix: correct the row. Add to §3.4 one clause: "in a new checkout, answers in the first minute may be missing or incomplete; ask again after the init finishes". Record PE/PG as probe rows.

7. **MINOR. `probe-results.md` row 2 still says the simultaneous-init index may be incomplete.**
   - Location: `probe-results.md:8`, relied on by A:219, A:237 and C:50.
   - Evidence: my re-run, two `init --yes` at the same instant, 2 trials. Both times one exited 0 and the other exited 1 with "Failed: UNIQUE constraint…". The final `status` showed 904 files, "Index is up to date" and no "never finished".
   - Fix: update row 2 with this result. That is also the evidence new 5's fix needs.

8. **MINOR. `codegraph_ready()` has two definitions.**
   - Location: A:187 versus T3b A:468; decision file `:9`.
   - Evidence:
     - A:187 defines it as "true when this run's codegraph phase passed", which includes a user-managed entry whose command resolves, at any version (§2.4 A:103).
     - T3b expects "not ready … wrong version".
     - `install --list` and `doctor` run no phase, so "this run's phase passed" cannot be evaluated there.
   - Fix: define it as one read-only predicate on current state: the entry is equal or owned-current, or user-managed with a resolving command (and say whether the version must be `1.6.2`). `install()` also ANDs it with the phase result.

9. **MINOR. Layer-2 step 6 never exercises the new kind-B branch.**
   - Location: A:362-366.
   - Evidence: the seeded `CBM` entry points at `$HOME/.local/bin/codebase-memory-mcp`, which does not exist in the sandbox. Phase 1 already removes that entry unconditionally ("whose binary is gone", `phase-1-removal-spec.md:313`). The §2.12 rule for a present kind-B binary (A:188) is untested.
   - Fix:
     - Before step 6, create an executable stub at that path.
     - Assert the entry is gone, the stub still exists, and `install.txt` contains the `uninstall -y` line.
     - In step 7, seed the same entry plus stub and assert it is kept.

10. **MINOR. Layer-2 steps 6-7 can pass or fail for the wrong reason, and T9 omits the script from its file list.**
    - Location: A:364, A:369-370, T9 A:537.
    - Evidence:
      - Step 7 asserts only "install exits non-zero"; any other phase failing offline satisfies it.
      - Step 6 runs under `set -e`, so a non-zero `superclaude install` exits before `cat "$S/install.txt" >> "$EV"`, and the evidence loses the cause.
      - T9 "Files" lists only `P2-layer2.md`, yet the change saves and runs `p2-layer2.sh`.
    - Fix:
      - Step 7: also `grep -q 'download' "$S/install2.txt"` (the codegraph stage) and grep for the Tier K kept line.
      - Step 6: `if ! uv run … > "$S/install.txt" 2>&1; then cat "$S/install.txt" >> "$EV"; exit 1; fi`.
      - List `p2-layer2.sh` in T9 "Files".

11. **MINOR. The T2 shape probe accepts a failed `add-json`.**
    - Location: A:438, A:442, A:448.
    - Evidence:
      - If `claude mcp add-json` fails (for example, the CLI rejects `alwaysLoad`), `jq '.mcpServers.codegraph'` writes `null` into the evidence file, and `test -s` passes.
      - The recovery text treats any mismatch as "the CLI changed or added a field".
      - A rejected field is not handled: it would make the required phase fail on every machine.
    - Fix: acceptance `jq -e 'type == "object"' …shape.json`. Treat a non-zero `add-json` exit as stop-and-decide (mid-level, §7).

12. **MINOR. The acceptance `jq` and the plan's scope differ.**
    - Location: A:202, B:79, decision file `:33`.
    - Evidence (I ran the expression against seven synthetic files and the real file; the `jq` itself is correct):
      - It includes `projects.*.mcpServers`, which §2.12 and Phase 1 never remove (A:190). A workspace with a local-scope `serena` therefore fails the check after the plan did everything it promises.
      - It passes for `serena-local`, which A's own hint tells users to create.
    - Fix: state next to the check that local-scope hits need the printed command. Add a name-independent check: no user entry whose `args` contain `serena-agent` or `start-mcp-server`, unless named `serena-local` by the user's choice.

13. **MINOR. T7 omits the §2.12 user-facing text.**
    - Location: A:191 ("stated in docs and CHANGELOG"), T7 A:515-523.
    - Evidence:
      - T7's change list and acceptance cover only §2.6, §2.10 and §3.3 and the `post-checkout` recipe.
      - Nothing documents "Serena is removed once codegraph is ready", the `serena-local` name, or the kept items.
      - Phase 1's CHANGELOG entry (its T12) will say the entry is kept.
    - Fix: add §2.12 to T7's change list and `rg -q 'serena-local' docs/user-guide/mcp-installation.md CHANGELOG.md` to its acceptance.

14. **MINOR. A:61 overstates the safety property.**
    - Location: A:61 ("a failed codegraph phase never leaves the user with neither server").
    - Evidence: Tier R `serena` rows and the `/usr/local/bin/codebase-memory-mcp` entry are removed unconditionally (A:189). A user whose only servers were those ends with neither when the codegraph phase fails.
    - Fix: "never removes the current-pin Serena entry unless codegraph is ready".

15. **MINOR. A decision-file action item was dropped from the handoff.**
    - Location: decision file `:19` against B and C.
    - Evidence: "Coder confirms which `superclaude` the slug runs, and what an outer `timeout 60` does to the retire step's process group" does not appear in B or C. Only the retry question does (B:57).
    - Fix: add one sentence to B's "Cleanup" paragraph.

16. **MINOR. B's inline fallback lacks the CLAUDE.md block.**
    - Location: B:20, B:24-27.
    - Evidence:
      - B requires Coder to seed the codegraph rule "(the exact text is in the context file §2.3)".
      - If the context file is unreachable, the inline facts give neither the text nor its source of truth (`src/superclaude/core/CLAUDE.md` at the pinned SHA, C:59).
    - Fix: add that path to B's inline facts.

17. **MINOR. Nothing runs the real hook with the real binary.**
    - Location: §3.2 tests (A:241, stub only), §4.2 (no hook step).
    - Evidence:
      - The pgrep guidance and "detach survives" are checked only against a stub.
      - Whether Claude Code leaves the hook's background child alive after the hook exits (no `setsid`, same process group) is not marked UNVERIFIED anywhere in A.
      - Layer-2 step 6 already installs the hook into the sandbox, but never runs it.
    - Fix:
      - After step 6, run `CLAUDE_PROJECT_DIR="$S/project2" sh "$HOME/.claude/hooks/codegraph-session-start.sh"` on a fresh clone.
      - Assert exit 0 and empty stdout.
      - Assert that `pgrep -f 'codegraph\.js (init|index)'` matches within 2 s, and that once it stops, `status` is up to date.
      - Mark process-group survival under Claude Code as UNVERIFIED in §3.2.

## 3. Checks that passed

- **Hook correctness.**
  - §3.2 steps 1-6, rendered literally, pass `sh -n` and `dash -n` (`/bin/sh` is dash here).
  - Every descriptor of the background `init` is redirected.
  - Exit 0 and empty stdout hold on every path.
  - Under the probed timings, no path in the hook can empty an index: it acts only when `.codegraph/` is absent, and a second concurrent init is harmless (rows 2-3 plus my re-run).
- **Daemon-heal claim.** It is well supported:
  - PA reproduced probe 9: 0 → 904 files.
  - PB: `status` twice during a heal; the heal continued (16 → 728 files) and finished at 904.
  - PF: `codegraph index` 1.5 s into a heal, 2 of 2 trials: exit 0, final status complete.
  - So the pgrep blind spot is harmless in these cases. A heal runs inside `codegraph.js serve --mcp --path <top>`, which the guidance pattern does not match.
- **Guidance (A:253, C:57).** It forbids exactly the commands that destroyed an init (rows 6-7). It prefers the pointer file, and its `init` advice is harmless when repeated. I found no path where following it empties an index, apart from new 5, which leaves an index empty without destroying one.
- **Layer-2 script (A:312-374).**
  - Extracted from `#!/usr/bin/env bash` to `echo "LAYER2_OK"` (62 lines): `bash -n` passes.
  - Under `set -euo pipefail`:
    - the shim loop tolerates a missing tool;
    - `claude` is a `/bin/sh` wrapper that execs an absolute path, and `node` is shimmed, so the reduced `PATH` works;
    - step 6 sees the codegraph pointed to by `$HOME/.local/bin` again (re-linked at A:347), so `codegraph_ready()` is true;
    - in step 7, `PATH` and `HOME` hide every codegraph and the dead proxy makes the download fail, so exit 1 is expected and the `if` form keeps `-e` from firing.
  - `superclaude install` has no interactive prompt (`click.confirm` exists only in `superclaude mcp`, `install_mcp.py:214,704,1281,1339`).
  - No `XDG_*` variable is set in this environment, so the full install stays inside the sandbox `HOME`.
  - Residual problems are new 9 and new 10.
- **Coordinator requirement, apart from new 1-4.** A names who removes the entry (IronClaude's retire step, T3b), when (the same `superclaude install` run, once codegraph is ready), and the Coder backstop (step 2). The escalated residuals are stated (A:197-200, D22): the root-owned baked binary until the step-5 image, and kind-B binary companions. The acceptance `jq` is syntactically and semantically correct.
- **Consistency.** A §2.12, A §8 steps 2 and 5, B:14/48/51, C:65-66, C §5(b) and the decision file agree on who (IronClaude when ready; Coder step 2 bundle stop plus a guarded migration; step-5 image), when, and the guard condition.
- **Brief coverage.** A has §1-§9 plus Decisions and covers brief items A1-A9. Every §5 task, T0-T11 (including T3b), has files, a change, an exact acceptance command and a commit point (T10 conditional; T11 PR only). B (79 lines) has the goal, touchpoints as leads with "verify on current main", the research instruction for new worktrees and projects, the pin, ordering, tests, commits, a PR on IronbellyOrg/Coder only, #323 comments and the autonomy rules. C covers the install facts, the contract, the pin, the registration shape and the removal list.

## 4. Self-audit

- **Read in full:**
  - A (all 692 lines), B and C;
  - both prior review reports;
  - `probe-results.md`;
  - the merged Serena decision;
  - orchestration `README.md` and the brief `P2-phase2-spec.md`;
  - Phase 1 spec `:257-381` and `:579-601`, plus T15 (`:766-768`).
- **Source checked:**
  - `main.py:28-95` and `:190-280` (install phases, no prompts);
  - `install_ccsession.py:55-110`;
  - `/usr/local/bin/claude`;
  - the codegraph launcher;
  - `git show 55d40308:tests/cli/test_install_mcp_tavily.py` (`:408-418`, `:466-469`);
  - Coder `mcp-bundle-core/install.sh:1-100` and test-57, fetched read-only with `gh api`;
  - read-only `jq` of the real `~/.claude.json`: the serena and codebase-memory shapes, and no local-scope hits.
- **Probes**, codegraph 1.6.2 from the W4 bundle, sandbox `HOME` in `mktemp -d /tmp/p2-third-review.*`, telemetry and update check off, clones of this worktree with 904 files:
  - P0 control;
  - PA probe-9 reproduction plus pgrep patterns;
  - PB `status` during a heal;
  - PC `.codegraph/` with no database, plus `init` on it;
  - PD simultaneous inits (2 trials);
  - PE and PG (2 trials plus a control): session connects first;
  - PF `index` during a heal (2 trials).
  
  All sandbox processes were killed and the sandbox removed. `git status --short` shows only `?? .dev/codegraph-migration/`.
- **Not done:**
  - no edits except this report;
  - no `superclaude install`, `claude mcp add/remove`, `update.sh`, `make sync-dev`, full suite, `tests/cli/eval/`, commit or push;
  - I did not run `claude mcp add-json` (T2's job), so whether the CLI accepts or keeps `alwaysLoad` remains UNVERIFIED;
  - process-group survival of the hook child under real Claude Code is UNVERIFIED;
  - the probes ran single or few trials and their timings are machine-dependent.
