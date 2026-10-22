<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 3 (R3 refactorer/opus) -->
<!-- Merge date: 2026-10-20T06:05:00Z -->

# Merged Verdict — sc:reflect UC-2 post-execution audit (T1..T7)

Merged REFLECTION ANALYSIS, not code. No production, test, or doc edits are proposed. No tests were run and no live upstream smoke was performed at any stage.

## 1. Verdict summary

<!-- Source: Debate/forced round; Base (original, modified) — labels relabelled per forced-round tally -->

- **Convergence**: CONVERGED by the protocol metric (12/12 points at majority >= 2/3, threshold 0.80). Flags: late label flip on D1 (Necessary -> Drift after INV-001, by concession, not oscillation); low confidence (50-64%) on the D1/D2/D3 labels with one dissent each; D2 and D3 are conditional on unobserved host state.
- **Overall reflect status: PARTIAL.** Source-reading evidence supports mock-conformance of T1..T7. Three evidence surfaces are unexposed and therefore unverified: Serena `execute_shell_command` not exposed; dynamic Click reachability degraded (decorator oracle DEGRADE for two callbacks); the pre-ship live smoke gate at source.md:151 has no code anchor and is "pending".
- **Confidence caveat**: input calibrations 0.71 / 0.78 / 0.80, arithmetic mean 0.763, reused as-is. No new calibration was produced. The calibrator ran on `opus`, which collides with the V3 advocate class, so advocate/calibrator independence is degraded.
- **Canonical deviation count**: one Authorized expansion (D5), one Drift LOW-MEDIUM (D1 menu-0 slice), two conditional Drift (D2, D3), one LOW Drift candidate with interpretation open (D4), plus one Necessary deviation slice (D1 explicit-mixed). No Regression at majority; V3's Regression-LOW on D1 is recorded as dissent.

## 2. Per-task status T1..T7

<!-- Source: Variant 1, §Assigned completion; Variant 2, §Assigned completion; Base (original) §T7 — merged per Change #7 -->

Conformance wording for every task: **mock-conformant; source.md:151 live gate unverified**. "49 ACs" is the tasklist's atomic decomposition of source.md:138-149 (12 bullets); the count is not independently verifiable (INV-005).

| Task | Status | ACs | Anchors (current source/test lines) | Carried findings |
|---|---|---|---|---|
| T1 | mock-conformant | part of 20 across T1/T3/T6 (V2 card gives no per-task split) | `install_codebase_memory.py:582-595`, `:529-610`, `:612-621`, `:631-665`, `:512-522`, `:693-700`; tests `test_install_codebase_memory.py:46-76`, `:85-188` | D5 Linux-only (Authorized) |
| T2 | mock-conformant, qualified | 7 | `install_mcp.py:815-899` (sub-ranges in YAML); dispatch `:1011-1014`; tests `test_install_mcp_registry.py:192-239`, `test_install_mcp_tavily.py:479-818` | D2 conditional Drift; argv advisory. Fixture `test_install_mcp_tavily.py:382-462` READ by coordinator: isolates HOME + CLAUDE_CONFIG_DIR, stubs discovery, `pytest.fail` on `_run_bounded` |
| T3 | mock-conformant | part of 20 across T1/T3/T6 | native `:312-314`, `:304-311`, `:74-78`; `install_mcp.py:902-993`; tests `test_install_codebase_memory.py:558-564`, `:623-643`, `:646-706`; `test_install_mcp_tavily.py:920-995` | D2 conditional Drift (removal ambiguity `:257-264`, `:305-311`) |
| T4 | mock-conformant except D1 slice | 8 | `install_mcp.py:1311-1314`, `:1306-1310`, `:486-496`, `:571-583`; tests `test_install_codebase_memory.py:856-879`, `:944-1014` | **D1 Drift LOW-MEDIUM (menu-0 slice)**; D1-explicit Necessary; D4 candidate; menu/consent/non-TTY/dry-run bodies unread by R1 |
| T5 | mock-conformant, test-body qualified | 7 | `main.py:255`, `:310`, `:352`; tests `test_update_command.py:254-277`, `:293-342`, `:345-375`, `:386-424` | Fixture `test_update_command.py:31-76` READ by coordinator: autouse guard stubs the shared phase, fails on real CLI/native. Shared-phase repeats are delegation tests, not upstream proof |
| T6 | mock-conformant | part of 20 across T1/T3/T6 | `test_install_codebase_memory.py:1278-1409` (unlink by fake process boundary `:1356-1363`); canned `mcp_cli` fixture `:821-835`; historical run `t6-cli-regressions.txt:49-53` (exit 0, 242 passed, 1 gated skip; not fresh) | C-005: canned fixture proves dispatch only; no umask/0775 fixture (INV-010) |
| T7 | mock-conformant | 7 | guide `:7,9,46,48,73,121,208,221-233,309-321`; reference `:21-22`, `:47-50`; `mcp-optional-design.md:1-26`; README `:64,75`; `main.py:50-52`, `:313-322` | LOW clarity: guide:46/:73 never name option 0; guide:25/:223 silent on group-writable proof rule |

## 3. Canonical deviations (four classes only)

### D1 — Menu option 0 at project/local scope or non-Linux: **Drift, LOW-MEDIUM** (menu option-0 slice only)

<!-- Source: Variant 1, §W1-D1 split disposition — merged per Change #2; Debate/forced round -->

- **Majority**: Drift (V1 50%, V2 64%). **Dissent**: V3 Regression-LOW 55%. Reported confidence 0.57; this is a spec-interpretation call, not settled.
- **Spec anchors**: source.md:67 (keep existing invocations working), :78 (option 0 includes native), :80 (reject invalid native scope before any download or write; "Other servers retain their existing scopes"; no silent ignore), :143, :144 (Codebase Memory scope rejected before effects).
- **Source anchors**: `install_mcp.py:1284-1285` (option 0 selects every entry), `:1311-1314` (native gate blocks whole selection before loop), `:486-496` (scope/platform predicate).
- **Why Drift**: INV-001 showed a compliant alternative exists — all servers minus native with a printed skip, grounded in :67/:80/:144. Whole-selection rejection is wider than those clauses, so not Necessary; the spec never promises option 0 succeeds at project scope, so not Regression at majority. Label moved from the R2 "Necessary" consensus on new evidence; recorded as a late flip.
- **Tests**: positive option-0 case is Linux/user only (`tests/cli/test_install_codebase_memory.py:944-952`); mixed-flag rejection `:964-988` does not cover the menu token; other-only project/local works `:1179-1190`. Gap: no option-0 project/Darwin case.
- **Docs**: `docs/user-guide/mcp-installation.md:46` and `:73` imply the outcome but neither names option 0 (LOW clarity, not a documentation gap).

### D1-explicit — Explicit native-plus-other selections at project/local or non-Linux: **Necessary deviation**

<!-- Source: Variant 1, §W1-D1 (refuted slice); Variant 2, §W1-D1 — merged per Change #2 -->

Rejected before any effect by `install_mcp.py:1311-1314` / `:486-496`; tests assert `calls == [] and processes == []` at `:964-988`. All three cards agree; :78 + :80 cannot be satisfied by silently dropping an explicitly requested native install.

### D2 — Permission predicate split (discovery/reuse vs proof/removal): **Drift, conditional on A-001**

<!-- Source: Variant 2, §W1-D2 mechanism; Variant 1, §W1-D2 chain; Invariant probe INV-002/INV-003 — merged per Change #3 -->

- **Majority**: Drift conditional (V2; V3 55%). **Dissent**: V1 advisory 55%. Confidence 0.60.
- **Mechanism**: discovery accepts a user-owned canonical directory with no mode check (`install_codebase_memory.py:545-552`); proof/removal reject `mode & 0o022` (`:85-99`, `:102-116`); receipt is written after upstream succeeds (`:682-683`); ValueError becomes a failed result (`:693-700`) and the shared caller returns failure (`install_mcp.py:846-848`); retry reuses the canonical binary with no receipt (`:597-605`); removal then stays ambiguous (`:257-264`, `:305-311`).
- **Spec anchors**: source.md:109 reserves the removal stop for external/custom installs; :111 and AC :146 expect confirmed removal of a canonical install to invoke upstream.
- **Condition (A-001)**: real `~/.local/bin` mode under ccsession `mkdir` (`install_ccsession.py:37`, process umask) and whether upstream `install.sh --dir` preserves it are unknown. No umask/0775 fixture exists (grep `umask|0o022|0o775` in the test file: zero matches). The recollection that umask 002 is an Ubuntu default is unverified and must not be reported as fact.
- **Gate enumeration (INV-002, 8 gates)**: (1) ccsession runs only via `install` (`main.py:224` -> `:255`), never via `mcp -s codebase-memory-mcp`; (2) `mkdir(parents=True)` = 0o777 & ~umask; pre-existing `~/.local` equally possible; (3) both `~/.local` and `~/.local/bin` tested (`:87`); (4) binary mode tested (`:114`); (5) stale receipt `mode & 0o077` raises (`:159`); (6) `os.link` (`:192`) raises on no-hardlink filesystems; (7) verification `:674` has no mode check; (8) `install.sh --dir` directory behavior unknown.

### D3 — HOME-ancestor symlink fails closed: **Drift, LOW, conditional on a symlinked-HOME host**

<!-- Source: Variant 1, §W1-D3 (message omits path); Invariant probe INV-004; Debate/forced round — merged per Change #4 -->

- **Majority**: Drift conditional (V2; V3 50%). **Dissent**: V1 advisory 60%. Confidence 0.60.
- **Source anchors**: canonical path uses `Path.home().absolute()` (`:54-55`); `directory.resolve() != directory` at `:88`, `:489`, `:539-544` marks any resolved-ancestor mismatch ambiguous before the version probe; prerequisite error `install_mcp.py:572-579` exits 1 and omits the offending path (`:577-579`).
- **Spec anchors**: source.md:56 (working executable + registration is a no-op) vs :114 (fail-closed on symlink/ownership ambiguity — text sits in the uninstall section; nothing in the install section authorizes rejecting trusted ancestor symlinks).
- No symlinked-HOME fixture exists.

### D5 — Linux-only automation (macOS excluded): **Authorized expansion**

<!-- Source: Variant 1, §Assigned completion (label); operator-direction.md:5-7; Invariant probe INV-009 — merged per Change #5. Base (original, modified) — source.md:90 removed as support because :90 lists macOS -->

- **Unanimous** (C-004/X-003, 88%).
- **Authority**: `operator-direction.md:5-7`. Exact quote: "there is absolutely no reason to overcomplicate anything in order to preserve macOS portability" and "If Linux-specific cleanup is necessary, automated macOS support may be excluded and documented rather than driving supervision complexity." The operator permitted exclusion; it did not require it, so the label is Authorized, not Necessary.
- **Cost (must be stated, INV-009)**: every `superclaude install` on macOS exits 1 permanently (`main.py:255-275`); code asserts the necessity at `install_codebase_memory.py:594`. Disclosed at guide:9. source.md:63 puts opt-out out of scope.

### D4 — `mcp --list` rejects `--dry-run` / non-user `--scope`: **Drift, LOW — candidate, interpretation open**

<!-- Source: Base (original, modified) §Newly alleged canonical deviation — wording per Change #6; Debate R2/forced votes -->

- Majority label Drift (V2 74%, V1 45%); V3 downgraded to candidate 45%. Reported confidence 0.55.
- **Anchors**: `main.py:326-330` rejects `--list` with `dry_run or scope != "user"`; source.md:76 limits list rejection to mutation modes but "reject incompatible combinations" gives latitude; :31 says the baseline accepted the flags; :117 makes no-server `--dry-run` a list-like preview, so `--list --dry-run` is arguably redundant; the `--scope` half is stronger. guide:50 discloses; disclosure is not authorization.
- Baseline code was read by nobody; the baseline claim rests on source.md:31.

## 4. Correctness advisories and evidence gaps

<!-- Source: Variant 1, §Other observations; Variant 2, §Evidence limits and errata; Invariant probe INV-002/005/006/010 — merged per Change #8 -->

Items here are not deviations (no spec anchor) and are kept out of the four classes.

- **A-001 (evidence gap, 90%)**: real host `~/.local/bin` mode and upstream `install.sh --dir` behavior unobserved; no fixture sets umask/0o775. D2 is conditional on this.
- **INV-002 (MEDIUM, unaddressed warning)**: the eight gates above are enumerated, not exercised.
- **INV-005 (MEDIUM, unaddressed warning)**: "49 ACs" unverifiable against source.md:138-149; source.md:151 live gate has no code anchor.
- **Serena `execute_shell_command` not exposed**; **dynamic Click reachability** degraded (two callbacks DEGRADE by decorator oracle, never UNREACHED; three cross-reference risk flags; T3/T4 overlap benign).
- **No fresh tests run**; the 242-pass count at `t6-cli-regressions.txt:49-53` is historical.
- **Canned `mcp_cli` fixture** (`test_install_codebase_memory.py:821-835`) proves dispatch only; `& 0o022` branches (`:95`, `:114`) never exercised (INV-010).
- **INV-006**: option 0 at project scope never reaches `check_prerequisites` (returns at `:1311-1314` before `:1331-1332`); on user/Linux `claude --version` runs twice (`install_mcp.py:513`, `:830` via `:1012`) while `:961` asserts one call because `mcp_cli` stubs native dispatch; error `:488` does not name option 0; the menu does not re-prompt.
- **U-003**: a prior entry's secret values may travel in `add-json` argv during restore; tests check captured output only (`test_install_mcp_tavily.py:736-757`).
- **`AcquisitionResult.acquired`** is consumed only in tests (`tests/cli/test_install_codebase_memory.py:54,105,254,306`).
- INV-007/INV-008 ADDRESSED LOW; only "1,999" is tested (`:1193-1197`).

## 5. Rejected candidates

<!-- Source: refactor-plan.md "Changes NOT Being Made" — merged per plan -->

| Diff point | Rejected approach | Reason |
|---|---|---|
| C-001 (V1 original) | D1 as MEDIUM "regression candidate / debate-open" | Withdrawn by V1 in R1; final majority Drift. V3's LOW Regression kept as dissent only. |
| C-001 (V2 R1) | D1 as "Not a deviation" | Withdrawn by V2 in R2; observable baseline loss. |
| C-001 (R2 consensus) | D1 as "Necessary deviation" (menu-0 slice) | Falsified by INV-001; all three withdrew the "only compliant reading" premise. |
| X-003 (V2 original) | Linux-only as "Necessary" | Conceded; operator text is permissive. |
| X-003 (V3 original) | source.md:90 as support for macOS exclusion | Conceded; :90 lists macOS as supported. |
| D1 docs (V3 original) | "documentation gap" | Downgraded by V3 to LOW clarity note (guide:46 + :73 imply the result). |
| U-003 argv advisory | Promote to deviation | No spec anchor; tests check output, not process table. |
| INV-007/008 | Add as findings | ADDRESSED LOW; mentioned in advisories only. |

## 6. Verifiers and limits

<!-- Source: Base (original) §Ordering and limitations + recommendations; Variant 1/2 next-step lists — merged per Change #9 -->

Ordering facts: full selection validation precedes consent and non-dry prerequisites (`install_mcp.py:1299-1334`); framework native runs last and sets exit status (`main.py:254-275`); list returns without mutation (`main.py:94-187`, `:326-332`).

Strongest evidence-only verifiers (no fix implied):
1. Isolated option-0 case at project scope and on Darwin (closes the D1 test gap).
2. 0775 canonical-directory case covering first attempt, retry, and removal (resolves A-001 / D2).
3. HOME-ancestor alias case locking the intended guard behavior (resolves D3).
4. A contract decision on `--list --scope project` before any D4 change.
5. Guide edits naming option 0 limits and the group-writable permission rule.

Limits: no fresh tests run; no live upstream smoke (released installer modes, companion merge safety, background processes, MCP handshake remain a separate blocked gate per guide:309-321 and t7-live-smoke-gate.md); Serena exec not exposed; Click reachability degraded; input confidence mean 0.763 reused without new calibration.

## 7. Input provenance

<!-- Source: base-selection.md; debate-transcript.md Metadata -->

- Cards: `reviewer-cards/reviewer-1-calibrated.md` (R1 analyzer, 0.71), `reviewer-cards/reviewer-2-calibrated.md` (R2 QA, 0.78), `reviewer-cards/reviewer-3-calibrated.md` (R3 refactorer, 0.80); copied to `adversarial/variant-{1,2,3}-original.md`.
- Input confidence mean 0.763 = arithmetic mean of the three calibrated values; no new calibration.
- Base: Variant 3 (score 0.860) over Variant 2 (0.762); margin 0.098; no tiebreaker.
- Topology: advocates V1 `sonnet`, V2 `haiku` alias, V3 `opus`; fault-finder `sonnet`; coordinator Fable 5.1; calibrator `opus` collides with the V3 advocate class, so independence is degraded.
