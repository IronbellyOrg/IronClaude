# Round 2.5 Fault-Finder Notes (long form)

- Role: independent fault-finder, not an advocate. Output table: `adversarial/invariant-probe.md` (32 findings: 8 ADDRESSED, 24 UNADDRESSED; 7 UNADDRESSED HIGH).
- Inputs read: `partials/consensus-summary.md`, `convergence-r1.md`, `convergence-r2.md`, `r2-state.json`, `orchestrator-verification.md`, `point-cluster.json`, `debate-points.md` (full), `diff-analysis.md` (lines 1-470 in full), `r2-advocate-V1.md` and `r2-advocate-V2.md` (full), `r1-advocate-V1.md` (lines 1-110 and 244-413), and range reads of both variants (V2:1640-1735, 3505-3674, 4426-4493; V1:594, 2641-2657, 2862-2867, 3826-3908, 4030-4069) plus Grep over both.
- Read-only: only this file and `invariant-probe.md` were written. No git write. Nothing under `.claude/` or `~/.claude/` read. Python only through `uv run`. Two batched read-only scripts followed the batching policy (both `BATCH_OK failures=0`, private dirs removed). Test collection used `--collect-only -p no:cacheprovider` with `PYTHONDONTWRITEBYTECODE=1`. One external fetch (arXiv abstract page).
- Citation form: `V1:L` / `V2:L` = line of `variant-1-original.md` / `variant-2-original.md`; X-, C-, S-, A-, U- ids are `diff-analysis.md` ids.

## 1. Re-derived numbers

| # | What | Command or file | Result | Who was right |
|---|---|---|---|---|
| 1 | Code at HEAD equals the reports' HEADs | `git diff --stat 50d4d2b9d HEAD -- src tests scripts`; `git status --porcelain -- src tests scripts` | empty; clean | Both (cites hold at `ad8f57560`) |
| 2 | HEAD against `origin/master` | `git diff --stat origin/master HEAD -- src tests scripts`; `git rev-list --count HEAD..origin/master`; merge-base | 50 files differ; `origin/master` (`d4d1662a8`, 2026-11-14 12:42) is 3 commits past merge-base `d2d8a2d16`; HEAD is 5 commits past it | Neither report; V1:4061 "3 commits ahead" is now 5 (V2 advocate caught that); nobody noticed `origin/master` moved |
| 3 | Cited lines on `origin/master` | `git show origin/master:<file> \| sed -n` vs HEAD | `test_worker_contract.py:777`->787, `:1861`->1872, `:786`->796; `pragmatic.md:225`->229, `:231`->235; reflect `SKILL.md:343` text differs; `SKILL.md:703` same | V2's C14/C26 citations are HEAD-only |
| 4 | E2 commits | `git rev-list --count 4a22d74..6c09843`; `6c09843..e2f2ac268`; `git diff --stat 6c09843 e2f2ac268` | 4; 7; 767 files, +43,936/-152; cited E2 files untouched | V2 (pins the later tip); the 7-commit gap is new information |
| 5 | Tests collected | `uv run pytest --collect-only -q -p no:cacheprovider <dir>` | `tests/review` 651; `tests/cli/reflect` 353; `tests/pr_submit` 2258 | V1 |
| 6 | Test files | `ls tests/cli/reflect/test_*.py`, `tests/review/test_*.py`, `tests/pr_submit/test_*.py`; `git ls-files 'tests/pr_submit/*.py'` | 38; 19; 47 (49 tracked .py) | V1 G9 "38" right, V1:381 "37" wrong; V2 G14 "50 test files" wrong, V2 U-122 "47" right |
| 7 | Engine-A contract keys | `uv run python` regex over `ensemble.py:787-832` plus `panel_lint` constants | 32 literal keys; `t2_fallback` at `:833-834` (default None `:363`); outside STABLE (110) and TELEMETRY (27) = 10; outside STABLE only = 11; stable present 21 (89 absent) | Both, with basis: default run 32/10 (V2), with the fallback flag 33/11 (V1); V1's "in neither list" rules out the "outside STABLE only" reading of its 11 |
| 8 | rf-* spawn lines | `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` | 52 lines, 11 files, 8 of them `SKILL.md` | V2 (orchestrator agrees; V1's 43 is an unstated unit, not reproducible) |
| 9 | `superclaude review` in reflect skill | `grep -c` / `grep -o \| wc -l` | 5 lines, 7 occurrences | Neither (V2 "(6)" wrong) |
| 10 | Exit codes today | `ledger_cmd.py:13`; grep for 12 in `cli/review`, `cli/reflect` | `{PASS 0, REVISE 10, ESCALATE 11}`; no 12 | Both (status quo) |
| 11 | Citation-only line on the merge path | `findings.py:102-106, 186-193, 346-350`; `ledger.py:127-138` | rejected at `:104`, skipped at `:191-192`, `annotate` only on accepted findings | V1 (orchestrator agrees) |
| 12 | Clearing by silence, union | `ledger.py:186-188, 252-258` | `any(m["blocking"]...)`; `resolved_check` absent next round becomes `resolved` | Both (fact) |
| 13 | Distinctness default, re-review size | `panel.py:509, 575` (`strict_distinct: bool = False`), `:539-543`, `:600-605` | soft by default; re-review resolves fixed slots only, count 1 | Both; V2's "re-review is one reviewer" right |
| 14 | Slot key schema | `panel.py:46`, `:215` | closed `_SLOT_KEYS = {slot_id, tier, count, strategy, seed}`; unknown slot keys rejected | New fact (affects carried V1 per-slot keys) |
| 15 | Calibrator dimensions | `confidence-calibrator.md:3`; reflect `SKILL.md:1262, 1835` | 6-dimension vs 5-dimension | V1 |
| 16 | Plugin mirror size | `git ls-files plugins/superclaude \| wc -l` | 125 | V2 |
| 17 | Lint registration | `cli/review/__init__.py:19-37` | `lint_cmd`, `estimate_cmd` in the tuple; `ModuleNotFoundError` for the module itself swallowed | Both (fact) |
| 18 | Invariants in V2 7.3 | awk over V2:3962-4232 rows `^\| (C\|X)-n INV` | 244 rows: HIGH 60, MEDIUM 161, LOW 23; every HIGH row status OPEN | V2 (60) matches C-075's per-debate sum 1+3+2+0+7+4+1+13+0+5+6+2+2+12+2 = 60 |
| 19 | V1 invariants | V1:2620, V1:2862-2867 | stated 26 = 2+11+10+3; C-03 row lists one id only, so the "2" is not recountable from the table | V1 stated; partly unverifiable |
| 20 | Gates | grep of V1:4030-4056 and V2:4464-4492 | V1 19 (G1-G11 + G-all, G-bench, G-exit, G-new, G-pr, G-replay, G-skills, G-sync); V2 27 (G1-G16 code pins, G17-G27 adjudicated) | Both; different units |
| 21 | Constraints, dependency facts | grep V2:4428-4528 | C1-C29 = 29; D1-D26 = 26 | V2 |
| 22 | Open questions | `grep -oE '^\| Q-[0-9]+' \| sort -u` | V1 61 unique (122 rows incl. sub-tables); V2 93 | Both |
| 23 | Inventories | `grep -c '^\| V-'` V1; synth-08 per-source table | V1 698 (91 DROP; plus 4 parse-artefact destination cells); V2 886+868+1,685+955+796+589+171 = 5,950, DROP 1,969 (1,753 duplicates) | Both; different units |
| 24 | Debate-point denominator | `debate-points.md` vs diff-analysis Summary vs `sc-adversarial-protocol/SKILL.md:864-870, 1392` | 234 (56+97+63+18) vs 275 (all 59 A); skill counts promoted A only | 234 is right; diff-analysis Summary line is stale |
| 25 | Convergence resolution | r2-state.json | 224 agreed include 6 both-OPEN points | Resolved 218/234 = 0.932 |
| 26 | arXiv 2606.19544 | WebFetch `https://arxiv.org/abs/2606.19544`; run-2 QA P6-054 (`qa-consolidated-findings-phase6.md:76`) | "withdrawn by arXiv Admin", v1 17 Jun 2026, v2 3 Nov 2026 (withdrawn) | V1's exclusion; V2 uses it at V2:1647-1648, 1655, 2044, 2829 (and coverage rows 2072, 2078) |
| 27 | CLI tool-restriction flags | `claude --help` (2.1.325) | `--tools` = built-in set only; `--restricted` removes code-running tools and WebFetch, ignores settings files, refuses bypassPermissions, and needs `--strict-mcp-config` to skip MCP servers | V2's mechanism is right for built-in tools, incomplete for MCP; both advocates missed MCP |
| 28 | Existing restricted launcher | `pipeline/process.py:134-166`; `runner.py:488-499, 566`; `ensemble.py:535-561` | `reviewer_profile=True` drops `--dangerously-skip-permissions` and `--tools default` | Neither report mentions it |
| 29 | `unauthorized_deviation_present` producer | grep over `src/superclaude/**/*.py`; `ensemble.py:451-454, 527-561` | only defaults; the Mode-A child populates convergence and report path only | V1 (MS-14, U-001) |
| 30 | `merge_method` in debate contract | grep `src/superclaude/skills/sc-adversarial-protocol` | 0 hits for `merge_method` or `merged-verdict` | V1 (MS-24, U-002) for the src copy |
| 31 | Branch names | `git check-ref-format --branch feat_review-panel/core` and `feat_review-panel`; `git for-each-ref`; `git ls-remote --heads origin` | both names valid alone; no `feat/review-panel*` or `feat_review-panel*` ref locally or on origin; only `ironbelly/eval-tasklist-review-panel` contains `review-panel` | V2 C4 facts hold; the constraint text needs the new prefix |

## 2. Reasoning by category

### Category 1: state variables

- **Line-number base (INV-001).** Both advocates accepted A-002/A-036 after checking lines at HEAD. That is the wrong reference for a plan: by project rule and V1:4061, new branches are cut from `origin/master`, and `origin/master` has moved 3 commits since the merge base. It removes nothing the reports cite in `cli/review`, but it does move test and output-style lines that V2 cites as binding constraints (C14, C26) and as the basis of the X-15 adjudication (`pragmatic.md:225,231`). It also lacks the 3 shadow-run commits, so the reflect `SKILL.md` text at `:343` and the pins in `test_shadow_skill_contract.py` differ until `ironbelly/shadow-runs` merges. The A-036 rule "re-read every cited line before editing" protects edits but not the merged document's own cells.
- **Ledger persistence (INV-003).** This is the clearest shared error. V1's persisted-format rule (V1:3830) and V2's "keep `review-ledger/1`" (A-9) each look safe alone. Together, with V2's semantic change (silence never clears, verdict derived and no longer stored), they recreate the version skew that V1's own ledger debate closed with `min_writer` and a `/2` bump (C13-22 INV-014, V1:2657). An older installed `superclaude` (pipx installs on other machines are normal) loads the ledger because `load` checks only the schema string, then `merge_round` clears rows by silence again; `ledger.verdict` raises `KeyError` on the new round because it reads `last["verdict"]`. V2 itself records the second half (A-9 "older binaries that read `last["verdict"]` fail (INV-018, open)"). V1's reload test ("previous reader tolerates unknown keys") would pass and so would certify the hazard.
- **Debate state (INV-004).** The 10 disputed points are mostly an artefact of cluster inheritance. The V1 advocate's own R1 exceptions (C-017 V2, C-025 V2) were overwritten when the R2 cluster label became "V1". The merge must use point-level verdicts from the advocate files, not `r2-state.json` inheritance or the consensus-summary cluster column.
- **Quorum denominator (INV-005).** V2 Q-42/Q-52 leave `requested` undefined at merge time; V1 C13-06 already answers it (`panel_size`, `quorum`, `valid`, `denominator_source` on the round entry). Neither must-carry list carries that answer.

### Category 2: guard conditions

- **Read-only lane (INV-006, INV-007).** Both advocates corrected V1's `--allowedTools` to `--tools` / `--restricted` / `--disallowedTools Bash`. The local help shows the corrected set still leaves MCP servers loaded (`--tools` is "from the built-in set"; `--restricted` explicitly needs `--strict-mcp-config` to skip MCP). In this environment MCP servers include write-capable tools, so INV-G ("mechanically read-only") is not met by the agreed flags. `--restricted` also refuses `bypassPermissions`, so E2's launcher pattern cannot be reused as is, and it confines file tools to the working directories (the reviewer's snapshot root must be the cwd or an `--add-dir`). Separately, the product already has a restricted `claude --print` child (`pipeline/process.py` `reviewer_profile`), used by engine A; neither report considers reusing it or the soundness of its permission-prompt basis.
- **Fail-open claim (INV-008).** The V1 advocate's R2 concession that V2's C-06 refusal "closes the fail-open path" overstates V2. The acknowledgement is unbound (C-06 INV-006), the acknowledged-drop flag state is undefined (X-14 INV-019 HIGH), and `blocking_state` is taken from the reviewer's own flag (Q-60). The merged text must say "narrowed", not "closed".
- **Boundaries checked and found handled:** one-reviewer re-review (INV-009), duplicate models filling a quorum (INV-010, recorded as data by V2 C-03; the default itself is OPEN), zero valid blocks (`ledger.py:148-152` still refuses at zero valid blocks; V2 C18 says the quorum refusal rewrites that pin). Citation-only findings in the spec loop are rejected (fact verified) and, under C-06, a dropped blocking one triggers the refusal, which is fail-closed.
- **Reserved slot keys (INV-011).** `panel.py` rejects unknown slot keys, so "reserved" must be defined as document-only (as V2 X-13 does for its reserved items) or as a code change with golden regeneration.

### Category 3: count divergence

All disputed counts were re-derived (table above). Results: V1 is right on test counts, the 1,398 unit, the calibrator mismatch and the 33/11 key count under its basis; V2 is right on spawn lines, pr_submit file count (47, in U-122) and plugin size; both are wrong somewhere (V1 "37 files", V2 "50 test files", V2 "(6)"). Two counting-method problems were not raised by anyone: the diff-analysis Summary's 275 denominator (INV-015) and the convergence figure counting six both-OPEN points as resolved (INV-016). The cluster-level summary also masks point-level OPEN verdicts (X-058 under CL-04, X-040/X-056 under CL-03) and the 5 V2-verified points under CL-18's "V1" label (INV-017).

### Category 4: collection boundaries

- **Gate list (INV-018).** The agreed recipe for S-056 keeps V1's gate list and appends V2's G17-G27. That silently drops V2's G1-G16. Five of those have no V1 counterpart (lint-architecture, ruff, verify-deps; installed-path baseline; routing plugin parity; the rf-qa static pins under `tests/audit/`; contract-constant and generator-constraint checks). Worse, carried V2 constraints and adjudicated gates refer to V2 gate numbers (C19 "(G1)", C20/C21/C27/G17/G22 "(G8)", C23 "(G14)", C25 "(G15)", C26 "(G11)", G19 "(G3, G7)", G20 "(G1)"). Under V1 numbering those names bind to other suites or to nothing. Fix: keep both gate lists, re-keyed (for example R1-G8, R2-G8), and rewrite every cross-reference.
- **Ids (INV-019).** Report prefixes fix cross-report clashes; intra-report clashes (V1 C-nn twice; V2 AE-1 twice, G1-G3 twice, D-1 twice, M1 three ways, INV-nnn per debate) need composite keys.
- **Inventories (INV-020, INV-023).** No cross-report de-duplication rule exists; 93 V1 rows point at V1 components the merged design does not adopt; V2's rows live only in a 2 MB task-folder file, so the pointer must carry a commit.
- **Withdrawn source (INV-021).** The drop list misses V2:1655 and V2:2829 (and two coverage rows).
- **Unique rows (INV-022).** 62 Medium/Low U rows were never cross-checked; four spot checks found no error.
- **Empty or single-element cases:** CL-26 has 0 points (no verdict needed); U rows with one source were spot-checked; one-reviewer and zero-finding rounds are handled (Category 2).

### Category 5: interaction effects

- **T-c cascade (INV-024).** Both advocates found that V1's clustering remedy in both engines fires T-c. They did not trace what reopening C-01 does: by V2's own conditions it reopens C-05 and X-15 directly, reopens constraint C26, and touches C-06 and C-11 through C-02/C-03. The owner question must be stated with that cascade.
- **Exit code 12 (INV-025).** V2's adopted design already gives 12 two meanings (quorum refusal and dropped-blocking refusal, which "record nothing" in sequence); V1's carried 6.E rows use 12 for PENDING and the installed ledger uses it for CONTINUE. "One meaning for exit 12" is a V1-advocate requirement the consensus does not meet. Proposal: 12 = "refusal" with a mandatory `refusal.kind` record, or separate codes.
- **V1 G2 must-not-change pins (INV-026).** V1's G2 forbids changing the exact `verdict()` dict and the final `verdict:` line; V2's adopted axis 4 removes stored verdicts and derives new fields. V2's own rewrite list (C18) also omits these pins.
- **E2 pins in one document.** No contradiction found from mixing V1 facts at `4a22d74` with V2 facts at `6c09843`: every V1 E2 fact the consensus carries (judge sees combo name, 1,398 unit, audit D flips, Qwen 3 of 4) was verified at `6c09843` by the analysts or corrected to V2's value, and the 7 later commits do not touch the cited E2 files.
- **"No engine moves now" vs fix-in-place.** Covered as a sufficiency item (INV-028 (1)): the consensus moves the default without the invariant analysis that V2's C-04 had.
- **Branch layouts vs git-ref constraint.** Covered as INV-031.

### Category 6: sufficiency challenge

**(a) "V2 as base plus V1 insertions yields a merged document a later `/sc:workflow` plan can use."** Falsifying conditions found:
1. INV-027: 13 of V1's 48 steps conflict outright with adopted V2 outcomes and 14 partly. Carrying them "re-based" requires a step-by-step re-adjudication nobody has done; V1's gap-to-step map depends on those ids.
2. INV-018: the agreed gate recipe loses five no-regression gates and mis-binds 11 gate references.
3. INV-029: the governing core shape is conditional on an owner decision that is already due (T-c is met by the agreed D6 fact unless the v1 over-merge is accepted).
4. INV-003: the carried persistence rule plus the adopted ledger design re-open a version-skew hazard.

**(b) "The adjudicated outcomes are safe to carry as the recommended design."** V2's 60 HIGH invariants are all OPEN (verified) and are carried as plan gates and questions, which is the right treatment. But INV-028 enumerates five V2 adjudications the consensus changed without a new debate or fault-finder pass, including the replacement of V2's strongest outcome (C-04: 6.91 percent margin, no tiebreaker, no HIGH invariant) by V1's never-debated C-17 remedy. INV-030: V1's carried C-14 outcome loses its 3 HIGH invariants.

**Gates between the consensus and the merged output, and whether the consensus input passes them:**

| Gate | Passes? | Why |
|---|---|---|
| Merge executor applies per-point verdicts | No, not as handed over | consensus-summary is cluster-level; it masks point-level OPEN (INV-016), mis-labels CL-09 and CL-18 (INV-004, INV-017) |
| Precedence table rebuilt against the merged Section 7 (both R2 lists) | Not yet | the five changed adjudications (INV-028) must be rows in it |
| Id namespacing (A-006, A-058) | Partly | cross-report rule agreed; intra-report and gate cross-references not handled (INV-018, INV-019) |
| Owner scope filter: no roadmap, branch plan, PR plan or schedule | At risk | the 48 steps carry implicit order (M-numbering) and conflicting content (INV-027); V1 8.6 ordering clause is dropped (agreed) |
| Owner constraints: `feat_review-panel/<name>`, fork-only PRs | Partly | C4 carried literally for `feat/review-panel` (INV-031); fork-only rule carried (C9) |
| Facts re-verified at the base the plan will use | No | checked at HEAD only (INV-001) |
| Withdrawn or wrong sources removed | Partly | 2 of 4 arXiv-dependent sites missed (INV-021) |

## 3. Concessions and one-sided rows

- **Concessions resting on a wrong or overstated fact:** V1 advocate R2 "V2's C-06 closes the fail-open path" (INV-008); both advocates' "`--tools`/`--restricted` gives read-only" (INV-006). Earlier wrong concessions were already withdrawn in R2 (V1 advocate's "no raw-id read-only requirement"; V2 advocate's "V1 ignores open Bash", "measured H1 lever", "labels do not exist").
- **Concession slightly overstated:** "43 call sites does not reproduce" is treated as a wrong count; the orchestrator calls it an unstated unit. The merge should say "43 (unit unstated, not reproducible); 52 lines in 11 files, 44 in 8 `SKILL.md` files", not "43 is false".
- **One-sided U rows never challenged:** all 62 Medium and Low U rows (U-004, U-006..U-009, U-011..U-017, U-019, U-028, U-030, U-033, U-034, U-038, U-039, U-041, U-043, U-050, U-052, U-053, U-055, U-057, U-059..U-063, U-067, U-069, U-070, U-078..U-085, U-089..U-095, U-103..U-109, U-119..U-124). Spot-checked U-001, U-002, U-052, U-122: correct.
- **Orchestrator-verified facts vs consensus verdicts:** no conflict. Every VERIFIED-V1 / VERIFIED-V2 / VERIFIED-BOTH row maps to the matching point verdict; design-choice rows were debated, not verified.

## Corrections the merge must apply

Wrong or incomplete facts that both advocates accepted, or that nobody caught:

1. **Read-only mechanism:** a raw-id `claude -p` reviewer needs `--tools <read-only set>` (or `--restricted`) PLUS `--strict-mcp-config` with no or a read-only `--mcp-config`; `--restricted` refuses `bypassPermissions` and confines file tools to the working directories. The C-07 G2 gate must check the MCP server list from the `system/init` event. (INV-006)
2. **Existing launcher:** record `src/superclaude/cli/pipeline/process.py:145-154` (`reviewer_profile=True`) as an existing restricted `claude --print` child launcher used by reflect (`runner.py:566`, `ensemble.py:548`); the "gated, not built" launcher must say whether it reuses or replaces it. (INV-007)
3. **Ledger version skew:** do not combine "keep `review-ledger/1`" with changed clearing and verdict semantics under V1's "keep schema string, new keys optional" rule; carry V1 C13-22's `min_writer` plus `review-ledger/2` remedy (or an explicit owner acceptance of the skew), and drop the claim that an old reader tolerating unknown keys is safe. (INV-003)
4. **Quorum denominator:** carry V1 C13-06's round-entry fields (`panel_size`, `quorum`, `valid`, `denominator_source`) as the answer candidate to V2 Q-42/Q-52. (INV-005)
5. **Fail-open wording:** V2's C-06 refusal narrows, not closes, the fail-open path (unbound acknowledgement, C-06 INV-006; X-14 INV-019). (INV-008)
6. **Gate list:** keep V2 G1-G16 as well as V1's gates and V2 G17-G27, re-keyed by source, and rewrite the gate cross-references in V2 C19-C27 and G17-G22. Remove V1 G2's "must NOT change" on `test_review_ledger.py:299-304` and `:468-472` or mark it conditional on the non-adopted V1 verdict design; add them to V2 C18's rewrite list. (INV-018, INV-026)
7. **Withdrawn paper:** also remove or re-source V2:1655 (verbosity rationale) and V2:2829 (33-41 points in the Section 6 Cons cell) and fix coverage rows V2:2072 and V2:2078. (INV-021)
8. **T-c:** state that D6 (confirmed on both clusterers, V1:594) already meets T-c unless the owner accepts the v1 over-merge, and list the cascade C-01 -> C-05, X-15, C26 (and C-06, C-11 via C-02/C-03). (INV-024, INV-029)
9. **Reopened adjudications:** mark C-04, C-09, C-11, X-14 and C-01 (clustering) as "reopened or changed by the compare debate" in the rebuilt precedence table, with V1 C-17's fix-in-place labelled "never debated; no invariant probe". (INV-028)
10. **Exit 12:** state that V2's adopted design uses 12 for two refusals (C-06 INV-020) and that V1's PENDING and the installed CONTINUE are other meanings; either one code with a mandatory `refusal.kind` or separate codes; keep X-058 as an open owner question. (INV-025)
11. **Line base:** state that line numbers are valid at `ad8f57560` (`ironbelly/shadow-runs`); on `origin/master` `d4d1662a8` the pins in V2 C14/C26 sit at `test_worker_contract.py:787, :796, :1872` and `pragmatic.md:229, :235`. (INV-001)
12. **Git-ref constraint:** restate C4 for the owner's prefix: no branch `feat_review-panel` (local, packed or remote-tracking) while any `feat_review-panel/<name>` exists; an umbrella branch, if wanted later, needs a non-prefix name. (INV-031)
13. **Reserved slot keys:** say "reserved in the document only" or name the `_SLOT_KEYS` change (`panel.py:46, :215`) and its golden regeneration. (INV-011)
14. **Debate bookkeeping:** C-017 and C-025 are V2 (V1 advocate R1 exceptions); the real remaining disputes are C-005, C-076, X-051; convergence of resolved points is 0.932 (218/234), and the diff-analysis Summary's "275" denominator is wrong (234). (INV-004, INV-015, INV-016)
15. **Inventories:** de-duplicate V1's 698 rows against V2's 5,950 before carrying both; re-route the 93 V1 rows aimed at non-adopted V1 components; pin the synth-08 pointer to commit `ad8f57560`. (INV-020, INV-023)
16. **V1 C-14 invariants:** carry its 3 HIGH invariants (INV-009, INV-012 and the third, V1:2867) and Q-47..Q-50 with the C-14 outcome. (INV-030)
17. **Counts to state with units:** engine-A contract 32 keys / 10 outside both lists by default, 33 / 11 with the fallback flag; rf-* 52 lines in 11 files (44 in 8 `SKILL.md`), V1's 43 unit unstated; pr_submit 47 test files; reflect 38 test files; `superclaude review` in the reflect skill 5 lines / 7 occurrences; E2 later commits: 7 after `6c09843`. (INV-012, INV-013, INV-017)
