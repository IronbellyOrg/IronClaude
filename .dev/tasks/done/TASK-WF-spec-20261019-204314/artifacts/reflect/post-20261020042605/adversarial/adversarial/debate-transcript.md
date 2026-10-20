# Adversarial Debate Transcript

## Metadata
- Depth: standard (Round 1 parallel, Round 2 sequential, Round 2.5 invariant probe; no Round 3)
- Rounds completed: 2 + probe
- Convergence achieved: (filled in Convergence Assessment below)
- Convergence threshold: 80%
- Focus areas: All (bounded to 12 diff points + D4 supplementary)
- Advocate count: 3
- Actual topology: V1 advocate = `sonnet` slot; V2 advocate = `haiku` slot; V3 advocate = `opus` slot; coordinator/judge = Fable 5.1 (differs from all advocate slots). Degradation note: the input cards were blind-calibrated by an `opus` calibrator, which collides with the V3 advocate model class, so advocate/calibrator independence is partial, not full. Round 2 reused the Round 1 advocate contexts via SendMessage (same agents, transcripts delivered as text).
- Invocation: task-agent (debate-orchestrator), invoked by the sc:reflect parent.

## Round 1: Advocate Statements

### Variant 1 Advocate (sonnet, analyzer)
**Position**: V1 is right that menu option 0 at project/local scope or non-Linux observably lost behavior and that no test covers it (`tests/cli/test_install_codebase_memory.py:944-952` is Linux/user only), but wrong to call it a regression; source.md:78+:80 together authorize the rejection. Concedes D1 to Necessary deviation and D2 to advisory-no-spec.

**Steelman of V2**: cleanest four-class discipline; advisories kept out; explicit mixed invalid scope tested (`:964-988`); other-only project/local works (`:1179-1190`); option 0 includes native (`install_mcp.py:1284-1285`) and the gate rejects (`:1311-1314`, `:486-496`); silently dropping native contradicts :78.
**Steelman of V3**: alone found D4 (`main.py:327`); frames D1 as spec consequence + doc gap; most careful D2/D3 labels.

**Strengths claimed**: (1) split disposition isolates the untested menu-0 slice; (2) names the :67 vs :78/:80 tension; (3) D2 mechanism accurate (`install_ccsession.py:37`; `install_codebase_memory.py:85-99`, `:545-552`, `:682-683`; `install_mcp.py:847-848`; retry `:597-605`); (4) honest unread regions; (5) correct "authorized" label for Linux-only.
**Weaknesses in V2**: "no menu-zero test is not a contract" sidesteps the observable loss; "necessary" label for Linux-only contradicts `operator-direction.md:7` ("may be excluded"); 20 ACs summarized without anchors.
**Weaknesses in V3**: cites source.md:90 (which lists macOS as supported) as authority; "three requirements force" relies on plan Task4 text — grep of source.md finds no explicit whole-selection sentence (closest :80, :108); doc-gap overstated since guide:73 + :46 together imply the result.
**Concessions**: withdraws "regression" on D1 (authorization by composition of :78 + :80; silence on abort-vs-skip makes it Necessary with doc/test gap); withdraws "conditional drift" on D2 (provenance runs inside `acquire_codebase_memory` `:682-701`, so failure is an acquisition failure under source.md:59); missed D4; unread fixtures and weak next-step precision are real.
**A-001**: QUALIFY (env unknowns real; mkdir-under-umask mechanism deterministic; standalone `mcp -s codebase-memory-mcp` may not run ccsession first). **A-002**: QUALIFY (:78/:80 more specific than :67; but no explicit whole-selection text in source.md).
**Votes R1**: S-001 SPLIT 55 | S-002 SPLIT 50 | C-001 SPLIT/Necessary 60 | C-002 V3/Advisory 70 | C-003 SPLIT/Not-dev 80 | C-004 V1/Authorized 70 | C-005 SPLIT 55 | X-001 SPLIT/Necessary 60 | X-002 V3/Advisory 70 | X-003 V1/Authorized 70 | A-001 SPLIT/QUALIFY 65 | A-002 SPLIT/QUALIFY 65

### Variant 2 Advocate (haiku alias, QA)
**Position**: whole-selection rejection at project/local or non-Linux is the contract, not a regression; V2 was wrong to call the macOS exclusion Necessary — the operator allowed it, did not force it.

**Steelman of V1**: splits rather than buries; menu-0 path distinct from explicit-mixed; only positive option-0 test is Linux/user; :67 preserves invocations; V1 correct on Authorized; refuses to treat unobserved 0775 as proven.
**Steelman of V3**: :78 + :80 + gate before loop (`:1311-1314` before `:1337`) make skipping native a different design; D4 real (`main.py:326-330` vs source.md:76; guide:50 discloses but disclosure is not authorization).

**Strengths claimed**: (1) :78 includes native in option 0; :80 rejects before any write and forbids silent ignore; gate returns before prerequisites (`:1331`); other-only project/local works (`:1179-1190`); :67 preserves named invocations, not an option 0 whose membership :78 changed. (2) D2 kept out of deviation classes: discovery no mode check (`:545-552`), proof/removal reject group/other write (`:85-99`, `:102-116`), receipt after upstream (`:682-683`), ValueError → failed result (`:693-700`), retry reuse (`:597-605`); no spec sentence defines the predicate. (3) D3 fail-closed per source.md:114 (`:54-55`, `:538-544`, `:606-607`). (4) separates historical 242-pass from fresh proof; canned `mcp_cli` fixture proves dispatch only.
**Weaknesses in V1**: treats :67 as senior to :78/:80; promotes D2 to Drift without a spec sentence requiring 0o022.
**Weaknesses in V3**: "Authorized plus source.md:90" unavailable (line 90 lists macOS); "Necessary deviation" still calls a spec-matching result a deviation.
**Concessions**: macOS label should be Authorized ("may" is permission; platform checks `install_mcp.py:489-495`, `install_codebase_memory.py:590-595` show nothing made macOS impossible); no test for menu option 0 at project scope or Darwin; ACs summarized; never reviewed `--list`.
**A-001**: ACCEPT. **A-002**: QUALIFY.
**Votes R1**: S-001 SPLIT 82 | S-002 V2 70 | C-001 V2/Not-dev 74 | C-002 V2/Advisory 80 | C-003 SPLIT/Not-dev 84 | C-004 V1/Authorized 88 | C-005 V2 66 | X-001 V2/Not-dev 74 | X-002 V2/Advisory 80 | X-003 V1/Authorized 88 | A-001 SPLIT 90 | A-002 V2/Not-dev 72

### Variant 3 Advocate (opus, refactorer/boundary)
**Position**: D1 is a Necessary deviation with a documentation gap, not Regression; V3 alone found D4; corrects its own source.md:90 anchor.

**Steelman of V1**: option 0 means "install everything", not an explicit native request; on macOS option 0 for every server is now unusable; :67 preserves invocations; only Linux/user is positively tested.
**Steelman of V2**: clean four-class use; only card noting the canned `mcp_cli` fixture limits dispatch-test evidence.

**Strengths claimed**: (1) D1 forced by :78 + :80 + acceptance check source.md:144 ("rejected before effects"); code `:1284-1285`, `:1311-1314`, `:486-496`; tests `:964-988` show `calls == [] and processes == []`. (2) D4 LOW Drift: `main.py:327` rejects `dry_run or scope != "user"` with `--list`; :76 limits rejection to mutation modes; `--dry-run` never invokes the lifecycle (:82); baseline per :31 accepted the flags; guide:50 discloses but documentation is not authorization. (3) only card auditing disclosures: guide:46 silent on whole-selection failure; guide:223 silent on group-writable rule (`:92-95`).
**Weaknesses in V1**: split leaves D1 open without naming a clause the skip would satisfy; "conditional drift" ignores :59. **Weaknesses in V2**: Necessary label ignores operator permission; waves away the option-0 coverage gap.
**Concessions**: source.md:90 anchor wrong — authority is operator-direction.md:5-9; D4 baseline evidence is secondhand (:31), and "incompatible" could be read broadly; macOS cost of D1 is real (supports V1's impact sense, not the label); no original Task4 anchor — whole-selection backed by :80/:144.
**A-001**: ACCEPT (grep `umask|0o022|0o775` in test file: none). **A-002**: QUALIFY (:67 co-equal with :78/:80 and conflicting; observable loss; no compliant alternative → Necessary; neither "Not a deviation" nor Regression).
**Votes R1**: S-001 SPLIT 70 | S-002 V3 55 | C-001 V3/Necessary 70 | C-002 V2/Advisory 65 | C-003 V1 65 | C-004 V1/Authorized 75 | C-005 V2 60 | X-001 V3/Necessary 70 | X-002 V2/Advisory 65 | X-003 V1/Authorized 75 | A-001 SPLIT/accept 80 | A-002 V3/Necessary 65

### Round 1 omission check
All three advocates addressed A-001 and A-002. No [OMISSION] flags.

### Round 1 per-point tally (majority ≥2/3)
| Point | V1 | V2 | V3 | Agreed? | Majority |
|---|---|---|---|---|---|
| S-001 | SPLIT | SPLIT | SPLIT | yes (unanimous: complementary partition, no winner) | none |
| S-002 | SPLIT | V2 | V3 | no | — |
| C-001 | Necessary | Not-dev | Necessary | yes on label (2/3 Necessary); winner split | Necessary |
| C-002 | Advisory | Advisory | Advisory | yes (unanimous label; V2 winner 2/3) | V2 / Advisory-no-spec |
| C-003 | Not-dev | Not-dev | Not-dev (V1 msg detail) | yes | Not a deviation |
| C-004 | Authorized | Authorized | Authorized | yes (unanimous) | V1 / Authorized |
| C-005 | SPLIT | V2 | V2 | yes (2/3) | V2 |
| X-001 | Necessary | Not-dev | Necessary | yes on label (2/3) | Necessary |
| X-002 | Advisory | Advisory | Advisory | yes | Advisory-no-spec |
| X-003 | Authorized | Authorized | Authorized | yes | V1 / Authorized |
| A-001 | QUALIFY | ACCEPT | ACCEPT | yes (all: unproven host mode) | UNSTATED, accepted |
| A-002 | QUALIFY/split | Not-dev | Necessary | no | — |
Round 1 agreement: 10/12 = 0.83 (above 0.80, but Round 2 is mandatory at depth=standard and the C-001/X-001 label split V2-vs-V3 is material).

## Round 2: Rebuttals

### Variant 1 Rebuttal (sonnet)
- To V2 (":67 does not preserve an option 0 whose membership :78 changed"): largely right; :67 is subordinate for option 0 specifically; withdraws the claim that :67 makes the loss a regression.
- To V3 (skip alternative names no clause): fair; :80 "Other servers retain their existing scopes" concerns scope when native is not selected; :78 cuts against skipping; drops skip as a compliant alternative.
- Holds: the loss is observable and untested (`:944-952` only; guide:46/73 imply but never name option 0). "Not a deviation" understates; "Necessary deviation" with test+doc gap records it.
- C-001/X-001 now a definitional choice: departure-from-spec-text (V2 right) vs behavior-change-vs-baseline-without-explicit-sentence (V3 right); sides with V3 at 55%.
- S-002: V2's strict four-class structure with advisories separated is the better base; merge V3's U-001/ordering sections; V1 should not be base.
- D4: `main.py:327` rejects on `servers|uninstall|yes|dry_run|scope!=user`; :76 first sentence says mutation modes, second sentence "reject incompatible combinations" gives latitude; :117 treats no-server `--dry-run` as a preview; nothing mutates under `--list --scope project`; baseline code not read by anyone; LOW Drift at 45%, disclosed guide:50.
- New evidence: none.
**Votes R2**: S-001 SPLIT 55 | S-002 V2 60 | C-001 V3/Necessary 55 | C-002 V2/Advisory 75 | C-003 V1/Not-dev 60 | C-004 V1/Authorized 80 | C-005 V2 55 | X-001 V3/Necessary 55 | X-002 V2/Advisory 75 | X-003 V1/Authorized 80 | A-001 SPLIT/QUALIFY 65 | A-002 V3/QUALIFY 55 | D4 Drift(LOW) 45

### Variant 2 Rebuttal (haiku alias)
- macOS concession stands: `operator-direction.md:7` "may be excluded and documented" → Authorized.
- Menu-0 criticism lands: guide:46 says option 0 installs every individual server; guide:73 says project/local native selections fail; neither says option 0 at project scope or on macOS fails every server; only option-0 success test is Linux/user (`:944-952`); mixed-flag tests (`:964-988`) do not cover the menu token.
- Label criticism lands: UC-2's four classes cover divergence from baseline or spec; "Not a deviation" fits only when nothing diverged; option 0 at project/macOS used to install other servers and now cannot (`install_mcp.py:1284-1285` → `:1311-1314` before loop `:1337`). **Concedes C-001/X-001/A-002 = Necessary deviation with doc/test gap.** :78 + :80 cannot be satisfied by skipping native; :67 preserves explicit non-native invocations (`:1179-1190`) but cannot preserve option 0 once :78 redefines it; the gap is a missing guide sentence and a missing menu test, not a fifth class.
- D4 = Drift, LOW: :76 limits list rejection to mutation modes; `main.py:327` also rejects `--dry-run` and non-user `--scope`, neither a mutation; :31 says baseline accepted the flags; guide:50 discloses, does not authorize; no data loss → not Regression; not spec-required → not Necessary.
- New evidence: none; baseline option-0 behavior taken from source.md:30-34, not pre-change code.
**Votes R2**: S-001 SPLIT 82 | S-002 SPLIT 68 | C-001 V3/Necessary 72 | C-002 V2/Advisory 80 | C-003 SPLIT/Not-dev 84 | C-004 V1/Authorized 88 | C-005 V2 66 | X-001 V3/Necessary 72 | X-002 V2/Advisory 80 | X-003 V1/Authorized 88 | A-001 SPLIT 90 | A-002 V3/Necessary 70 | D4 V3/Drift(LOW) 74

### Variant 3 Rebuttal (opus)
- To V1 (b) "forced": QUALIFY, partly conceded. source.md has no explicit "validate the whole selection" sentence; "Task4" was plan text. But :80 says reject "before ANY download or write" (not "before any native write") and :144 "rejected before effects"; with option 0, rejecting native after other servers have written violates :80 read literally. Two choices remain: reject whole selection, or skip native; skipping is not rejecting and removes an entry :78 says option 0 includes. Whole-selection rejection is the best compliant reading, not strictly forced. Necessary confidence → 62-65%.
- To V1 (c) doc gap: CONCEDE most. guide:46 + guide:73 imply the result. Remaining: LOW clarity note — neither names option 0; nothing tells a macOS user that option 0 is unavailable for every server.
- D4: DOWNGRADE to "LOW drift candidate, contract interpretation open" at ~45%. source.md:117 makes no-server `mcp --dry-run` a list-like preview, so `--list --dry-run` has no separate sanctioned meaning and :76's "incompatible combinations" can fairly cover it. The `--scope` half is stronger (a scope value is neither a mode nor redundant), but nobody read baseline code and :31 lists flags without saying they combined with `--list`.
- A-002: accepts ":67 yields to :78/:80 where they collide". Converged: Necessary deviation.
- New evidence: source.md:80, :117, :145; grep of `tests/cli/test_install_codebase_memory.py` for umask/0o022/0o775 = zero matches.
**Votes R2**: S-001 SPLIT 70 | S-002 SPLIT 65 (V2 structure + V3 U-001/ordering/D1 label) | C-001 V3/Necessary 65 | C-002 V2/Advisory 72 | C-003 V1 65 | C-004 V1/Authorized 78 | C-005 V2 62 | X-001 V3/Necessary 65 | X-002 V2/Advisory 72 | X-003 V1/Authorized 78 | A-001 SPLIT/accept 80 | A-002 SPLIT/Necessary 70 | D4 V3/LOW-drift-candidate 45

### Round 2 per-point tally (majority ≥2/3)
| Point | V1 R2 | V2 R2 | V3 R2 | Agreed? | Resolved winner / label |
|---|---|---|---|---|---|
| S-001 | SPLIT | SPLIT | SPLIT | yes (unanimous) | no winner; complementary partition |
| S-002 | V2 | SPLIT (V2+V3) | SPLIT (V2+V3) | yes (all prescribe V2 structure + V3 sections) | V2 structural base |
| C-001 | V3/Nec | V3/Nec | V3/Nec | yes (unanimous) | V3 / Necessary deviation |
| C-002 | V2/Adv | V2/Adv | V2/Adv | yes (unanimous) | V2 / Advisory-no-spec |
| C-003 | V1/Not-dev | SPLIT/Not-dev | V1 | yes (label unanimous; winner 2/3) | V1 / Not a deviation |
| C-004 | V1/Auth | V1/Auth | V1/Auth | yes (unanimous) | V1 / Authorized |
| C-005 | V2 | V2 | V2 | yes (unanimous) | V2 |
| X-001 | V3/Nec | V3/Nec | V3/Nec | yes | V3 / Necessary deviation |
| X-002 | V2/Adv | V2/Adv | V2/Adv | yes | V2 / Advisory-no-spec |
| X-003 | V1/Auth | V1/Auth | V1/Auth | yes | V1 / Authorized |
| A-001 | QUALIFY | ACCEPT | ACCEPT | yes (all: unproven host mode) | UNSTATED accepted; promoted to evidence gap |
| A-002 | V3/QUALIFY | V3/Nec | SPLIT/Nec | yes (label unanimous Necessary) | :67 yields at the intersection |
| D4 (suppl.) | Drift LOW 45 | Drift LOW 74 | candidate 45 | label majority Drift(LOW); confidence contested | LOW drift candidate, interpretation open |
Round 2 agreement: 12/12 = 1.00 (D4 supplementary excluded from the denominator; reported as contested-confidence). Stable majority on 10/12 across both rounds; S-002 and A-002 flipped to agreement in R2 by concession, not oscillation.

## Round 2.5: Invariant Probe
See `invariant-probe.md`. Result at probe time: 10 findings; 1 HIGH UNADDRESSED (INV-001: "whole-selection rejection is the only compliant reading of :78+:80" is falsified by a visible-skip alternative grounded in :67/:80/:144), 4 MEDIUM UNADDRESSED (INV-002..005), 2 LOW UNADDRESSED. **Convergence BLOCKED by INV-001.** Per the gate, one bounded forced round on INV-001/003/004 was dispatched to all three advocates.

## Forced Round (invariant gate; INV-001, INV-003, INV-004)

### V1 (sonnet)
- D1 = **Drift (low-medium), 50%**. Accepts INV-001: "all servers minus native, with a printed skip" is compliant via :67, :80 ("Other servers retain their existing scopes"), :144 (rejects only Codebase Memory's scope); a printed skip is not the silent ignore :80 forbids. Withdraws its R2 concession that no clause supports skipping. Not Regression because :78/:143 make abort a literal reading. Decisive: :67 vs :78/:143; operator-direction.md:7 excuses native macOS automation only, not collateral loss of other servers.
- D2 = **Advisory-no-spec, 55%**. Removal-ambiguous-on-reuse is already the documented design (guide:223); D2 adds one more way into that state; 0775 unobserved; a receipt gate exceeding :109 would be a separate design-level Drift.
- D3 = **Advisory, 60%**. :56 literally requires a no-op, but a symlinked HOME ancestor makes identity unestablished (`:539-544`, `install_mcp.py:573-579`); if the plan's symlink/ambiguity clauses are absent, D3 becomes the stronger Drift candidate.

### V2 (haiku alias)
- D1 = **Drift, 64%**. Decisive: :144 rejects Codebase Memory's scope before effects; :80 keeps other servers' scopes; a printed skip is not a silent drop; :78/:143 require option 0 to include native on a valid user/Linux install, not to fail Tavily and the rest. Whole-selection rejection at `:1311-1314` is wider than those clauses → not Necessary; not Regression because the spec never says option 0 at project scope must succeed.
- D2 = **Drift (conditional)**. Provenance error → failure (`:693-700`); retry reuses canonical binary with no receipt (`:597-605`); removal stays ambiguous (`:257-264`, `:305-311`); :109 reserves that stop for external/custom installs, not a canonical binary this integrator just acquired. 0775 unobserved → conditional.
- D3 = **Drift**. :56 no-op requirement; `:538-544` marks any resolved-ancestor mismatch ambiguous before the version probe → prerequisite failure (`install_mcp.py:572-579`) → exit 1; :114 allows fail-closed discovery but does not define a link above HOME as ambiguity.

### V3 (opus)
- D1 = **Regression, LOW, menu option-0 slice only, 55%**. Accepts INV-001; in :80 the subject is Codebase Memory and "before any download or write" most naturally means the native lifecycle; compliant alternative keeps :78's literal text (option 0 includes native, native alone is rejected with explanation, others proceed), so the :67 loss was unforced → a previously working invocation broken without necessity is a Regression. LOW: visible failure, nothing mutated, explicit `--servers` still works. Explicit native-plus-other selections at project scope stay Necessary deviation. Withdraws "only compliant reading".
- D2 = **Drift (conditional on A-001), 55%**. Under 0775 a canonical install IronClaude itself acquired permanently refuses removal (`_binary_identity` raises at `:258`, lands as ambiguous at `:279`; receipt mismatch `:259-264`); :109 allows a stop only for external/custom; :111 requires removing a canonical install.
- D3 = **Drift (conditional, LOW), 50%**. :56 no-op requirement vs ambiguous at `:539`; :114's fail-closed rule sits in the uninstall section; nothing in the install section authorizes rejecting trusted ancestor symlinks.

### Forced-round tally
| Point | V1 | V2 | V3 | Majority (≥2/3) | Notes |
|---|---|---|---|---|---|
| C-001 / X-001 / A-002 (D1) | Drift 50 | Drift 64 | Regression-LOW 55 | **Drift (LOW-MEDIUM), menu option-0 slice** | All three reject Necessary and Not-a-deviation. V3 dissent: LOW Regression. Explicit-mixed slice remains Necessary (tests `:964-988`). Label moved Necessary → Drift on new evidence (INV-001); revision by concession, flagged as a late flip, not back-and-forth oscillation. |
| C-002 / X-002 (D2) | Advisory 55 | Drift-cond | Drift-cond 55 | **Drift, conditional on A-001 (0775 unobserved)** | V1 dissent: advisory; anchor :109/:111 vs receipt gate; retry-reuse `:597-605`. |
| C-003 (D3) | Advisory 60 | Drift | Drift-cond-LOW 50 | **Drift (LOW), conditional on symlinked-HOME host** | V1 dissent: advisory; anchor :56 vs `:539-544`; :114 is uninstall-section text. |
INV-001 → ADDRESSED (premise withdrawn by all advocates). INV-003 → ADDRESSED (D2 lifted to conditional Drift). INV-004 → ADDRESSED (D3 lifted to conditional Drift). INV-002 and INV-005 remain MEDIUM UNADDRESSED (evidence gaps, not label disputes): logged as warnings, non-blocking. No HIGH UNADDRESSED remains.

## Scoring Matrix (final, post forced round)
| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | none (complementary) | 75% | Unanimous SPLIT across all rounds; task partition is assignment, not quality. |
| S-002 | V2 (structure) | 70% | All three prescribe V2's four-class/advisory-separated frame with V3's extra sections merged. |
| C-001 | V1 (split-slice framing) / label Drift | 60% | V1's original split (explicit-mixed refuted; menu-0 untested) survived; label settled Drift 2/3 after INV-001; V3 dissent Regression-LOW. |
| C-002 | V2 (mechanism) / label Drift-conditional | 60% | V2's predicate-split exposition adopted; label lifted to conditional Drift 2/3 after INV-003; V1 dissent advisory. |
| C-003 | V1 (message-omits-path) / label Drift-LOW-conditional | 60% | Label lifted 2/3 after INV-004; V1 dissent advisory. |
| C-004 | V1 / Authorized | 88% | Unanimous; operator-direction.md:5-7 ("may be excluded and documented"); INV-009 requires stating the permanent exit-1 cost. |
| C-005 | V2 | 70% | Unanimous; canned `mcp_cli` fixture proves dispatch only; INV-010 confirms fixtures isolate but never exercise `& 0o022`. |
| X-001 | as C-001 | 60% | — |
| X-002 | as C-002 | 60% | — |
| X-003 | V1 / Authorized | 88% | Unanimous. |
| A-001 | accepted UNSTATED → evidence gap | 90% | No umask/0775 fixture; host and upstream modes unobserved (INV-002 enumerates 8 gates). |
| A-002 | label Drift (with C-001) | 60% | ":67 yields at the intersection" was accepted in R2, then INV-001 showed :67/:80/:144 admit a compliant visible-skip reading. |
| D4 (suppl.) | V3 / LOW Drift candidate | 55% | Majority label Drift (V2 74, V1 45); V3 downgraded to candidate 45; :117 makes `--list --dry-run` redundant; `--scope` half stronger; baseline code unread. |

## Convergence Assessment
- Points resolved: 12 of 12 (majority ≥2/3 on winner and label)
- Alignment: 100% by the protocol metric; **confidence on the three D1/D2/D3 labels is 50-64% with one dissent each** — report as converged-low-confidence, not settled.
- Threshold: 80%
- Taxonomy coverage: L3 (C-001, C-002, C-003, X-001, X-002, A-001, A-002), L2 (S-001, S-002, C-004, C-005, X-003), L1 (docs/presentation slice debated inside C-001 — guide:46/73 clarity note — and S-002 presentation structure). All levels > 0.
- Invariant gate: 0 HIGH UNADDRESSED after forced round; 2 MEDIUM UNADDRESSED warnings (INV-002, INV-005).
- Status: **CONVERGED** (with flags: late label flip on D1; low confidence on D1/D2/D3; D2/D3 conditional on unobserved host state)
- Unresolved points: none at majority level. Dissents: V3 Regression-LOW on D1; V1 advisory on D2 and D3.
