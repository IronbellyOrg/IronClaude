# Invariant probe (raw), slot C-12 collaboration-exchange-capability, Round 2.5 fault-finder

Probed: the emerging consensus of r2-advocate-A.md section 5(c) and r2-advocate-B.md section 4.2. Code read at HEAD 50d4d2b9d (read-only). Paths below are relative to `src/superclaude/` or `tests/` of the brainstorm-reflect-panel worktree. [POST-BASELINE] E2 facts are not used as decisive evidence; the open premise item is INV-016. Forbidden paths were not touched.

Findings: 16

---

ID: INV-001
CATEGORY: state_variables
ASSUMPTION: The build trigger (C-07 launcher, X-14 metric, C-08 served model, owner) can sit unfired indefinitely and the product state in the meantime is well defined ("unmeasured, not rejected").
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: r2-advocate-A.md 5(c) condition 3 and r2-advocate-B.md 3 (Build 3) both require a named owner, an expiry date or event, and the recorded state "unmeasured, not rejected". Residual: the owner is "the lead's decision, not C-12's" (r2-B 3), and a design note has no mechanical consumer, so an expired date triggers nothing. Acceptable for a note; it only matters if someone expects the expiry to act.

ID: INV-002
CATEGORY: state_variables
ASSUMPTION: The served-model and act-rate probe record is "cheap and needed now" (consensus 7) and has a home, so per-model capability facts survive the "unmeasured" state.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The only per-model data store at HEAD is `cli/review/data/review-tiers.default.json:18-22` `classes`, a model-to-class-name string map (`panel.py:77` reads `classes.get(model) == "fable"`). The run record (`cli/review/telemetry.py:30-80`, closed groups) records per-run facts, not a per-model capability. r2-B 3 (Build 2) says C-08 "should land independently", but C-08 is the run-record and served-model slot; an act rate per model and instruction form (E6: luna 4/5, 0.4 and 1/5 across probes) has no schema, owner file or read path named. If the build trigger never fires, the probe result is a fact with no consumer.

ID: INV-003
CATEGORY: guard_conditions
ASSUMPTION: A reserved profile key `exchange` (and the `kit` and `driving_documents` keys) is "a pin, not an implementation"; B's open question was whether an unknown profile key is already rejected (r2-B 2, push-back 3).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The question is answerable. The only validator at HEAD is `panel.py:160-176` `validate_panel`: it rejects any key outside `_PANEL_KEYS` (`panel.py:37-45`) with "unknown key", and slots the same (`panel.py:214-216`, `_SLOT_KEYS` `:46`). C-01's "unknown keys open" covers the findings parsers only, not panel templates. So an `exchange: off` key in a template fails validation today; adding it (and `kit`, `driving_documents`) means editing `_PANEL_KEYS`, which is code, and an older installed package then rejects a newer template. "Profile" as a structure holding those keys does not exist at HEAD (grep "profile" in `cli/review`: 7 hits, all `panel.py`, reflect-template rules). Neither advocate names the host. Also a template with the key present has different bytes, so `template_sha256` and `policy_sha256` change (`manifest.py:97-108`).

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: The off-state test "brief bytes with `kit: off` equal today's brief" (A 6.4) coexists with H1 shipping unconditionally (A 6.5: every brief names each driving document).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: variant-1-original.md 6.4 and 6.5 pin opposite baselines: with H1 on, no brief equals today's. The test can only compare against "today's brief plus H1 lines", which is not named. The brief template hash feeds `policy_sha256` (`manifest.py:97-108`), and a changed policy makes a resumed run a new invocation recorded in `history` (`manifest.py:443-460`), so H1 is visible in the manifest even with kit and exchange off. Stricter off-state test (consensus 6) does not list this.

ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: H1 reaches the reflect module "through the reflect brief; no call-site change" (A 3.3) while `cli/reflect` stays unchanged (C-01 result, B 2.6) and reflect results stay pinned.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The reflect Tier 2 worker brief is built inside `cli/reflect/ensemble.py:601-630`: `_load_review_target` emits only "Base ref", "Tasklist" and the tasklist body. `ReflectConfig.spec_path` exists (`cli/reflect/models.py:69`, `Path | None`) but is not written into the brief. Naming the driving spec by role, path and sha256 therefore needs an edit in `cli/reflect/ensemble.py`, contradicting "no change to `cli/reflect`" (adjudicated C-01; C-01 INV-020 left that phrase unresolved). `test_ensemble_stub_integration.py:404-417` pins the prompt prefix. Edge cases H1 has not defined: `spec_path` None (nothing to hash) and an unreadable tasklist, which `_load_review_target` turns into an empty body silently (`ensemble.py:626-629`), so a sha256 of "" would be recorded as if it were the document.

ID: INV-006
CATEGORY: count_divergence
ASSUMPTION: A single kit cost figure can gate `kit: on` per module ("inside a cap the module owner states", A 6.2).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: variant-1-original.md 4.2 table: hl2 kit elapsed +34.8%, output tokens +46.2%; el2 +10.2% and +8.8%; pinned r5 +59% elapsed and +55% tokens (one package, n=3). A cap on elapsed passes hl2 by 0.2 points at the study's +35% line, a cap on tokens fails it by 11 points. The metric choice decides the gate and the n is 2 against 4. The "+35%" is a study rule, not a product constant (A 5, last row). No rule says which dimension binds or which panel size applies; reflect allows at most 3 reviewers (`panel.py:73`) while generic panels allow 1..8 (`panel.py:247-248`).

ID: INV-007
CATEGORY: count_divergence
ASSUMPTION: "Hold-out of at least 4 unseen defects" plus a power calculation (consensus 1, 5) is a satisfiable, consistent threshold.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Two numbers, no precedence: r2-B 3 (Enable 1) admits 4 is "a floor for a sanity check, not a power guarantee" and the E2 plan cannot detect the central gain at n = 12 (`MR:1128`, [UNVERIFIED] by both). Supply side: E2 ground truth is 16 items in 3 plans, 3 items carrying 194 of 214 defect-rich catches (variant-1 6.1, r08 [UNVERIFIED]), and both catalogues were induced from ten missed issues (6.7). If those ten sit inside the 16, at most 6 unseen items remain, of which the three heavy ones may be among the ten (conditional, UNVERIFIED). A hold-out of 4 may not exist on the one module with ground truth (A-001).

ID: INV-008
CATEGORY: collection_boundaries
ASSUMPTION: A peer-origin sidecar "keyed by reviewer id and finding id" (consensus 3) identifies the tagged line unambiguously.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Finding ids are reviewer-authored and unique only inside one block (`cli/review/findings.py:91-95`, `seen` is per parse; `_ID` allows `F1`); the spec loop runs several rounds with the same reviewer ids, so the key needs the round. Ledger rows are produced after clustering of findings from several reviewers (C-01 result), so one merged row can mix an own-origin line from reviewer A with a peer-origin line from B; the sidecar keyed by (reviewer, id) cannot say which origin a row has. A line dropped or repaired by H2 may lose its id. Not in the proposed design-note contents (r2-A 4, items 1-6).

ID: INV-009
CATEGORY: interaction_effects
ASSUMPTION: H2 (one pre-merge repair step) is core "now", and its claim "survives either way because a re-ask without truncation is still a repair step" (A 3.1 item 2) is compatible with C-01's placement inside both `parse_block` functions.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: C-01 INV-003 (HIGH, UNADDRESSED, ADJUDICATION-RESULT.md) is still open: `tests/review/test_review_findings.py:113` and `:117` pin `ok` False for an anchor of 201 and a claim of 301 characters (re-read this session); rescuing those lines contradicts "T1: every pin unmodified". A re-ask is a new model attempt, which a pure parser (`parse_block`) cannot perform; it needs the dispatcher and the served-model identity check (C-08, still open). So the consensus lists H2 as buildable now while its policy (C-06) is open and its re-ask variant sits outside the place C-01 fixed. The advocates did not reopen this because they treat H2 as agreed.

ID: INV-010
CATEGORY: interaction_effects
ASSUMPTION: "One catalogue source per module, rendered by the brief builder through the installed form (`~/.claude/skills/<name>/refs/...` or project `.claude/`)" (A 5, INV-F row) and "the kit renders from X-13's single data source" (U-006).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The reflect and review briefs are built by package Python code (`cli/reflect/ensemble.py:601-616`), and package data such as the tier file loads through `importlib.resources` (`panel.py:21`, `cli/review/data/`), not from `~/.claude/skills/`. A catalogue read from the skills path can be absent when the package runs without a skills install; a catalogue held as package data is a second place beside the skill refs. `make verify-sync` covers neither (Makefile:307-325, per r2-A V4). The X-13 class-card outcome is not recorded in any adjudication I could read (`process-redesign-modules/ADJUDICATION-RESULT.md` has no class-card or kit entry), so "single data source" has no resolved target.

ID: INV-011
CATEGORY: interaction_effects
ASSUMPTION: "Quorum counts over own-origin lines only" (consensus 3, U-014) protects C-02 and C-03 once exchange exists.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: C-03 quorum counts reviewers in a complete state, not lines; C-02 counts reviewers typing `prior <lid> resolved`. "Own-origin lines" is not a quantity either slot computes. C-03 INV-006 (HIGH, open): `merge_round` unions every parsable finding including those of a reviewer whose block is invalid; C-03 INV-005: `complete` is not checked for distinct reviewers. A peer-echoed finding is therefore counted by the union today, and the sidecar would only mark it after the fact. The rule is vacuous with exchange off and unenforceable once on, without a change to `merge_round`, which the note does not mention.

ID: INV-012
CATEGORY: interaction_effects
ASSUMPTION: Kit moves written in shell form ("run grep ...") would instruct no-Bash lanes to execute something (INV-G).
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: A 5 (Endangered, INV-G) and 6.5 add a lint over the rendered briefs of every read-only lane; r2-B 4.2 adopts it. Existing guard `tests/cli/reflect/test_reviewer_brief_constraints.py:35-53` checks source text only (the READ-ONLY section and the live-execution prohibition), not rendered briefs, so the lint is a new test kind. Residual: detecting an "instruction to run a command" in prose is a heuristic; the swarm lane has no tool loop at all (`openai_compat.py:384-388`), where any shell recipe is dead text.

ID: INV-013
CATEGORY: sufficiency_challenge
ASSUMPTION: The A-layer alone gives "mutually blind reviewers" and an inert off state (INV-G, H4 principle).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Falsifier: H4 is a principle with an exclusion list "as module data" (A 3.1 item 3), but the reflect isolation snapshot that would enforce it is "PINNED OFF by default" (`cli/reflect/models.py:92-100`, `isolate_reviewers: bool = False`; read at `runner.py:730`). Reviewers with Read/Grep/Glob run in the live tree, where earlier reflect output already sits (untracked `docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md` in this worktree's git status). So a file-system channel between rounds exists with exchange off, and the byte-identical argv/brief test cannot see it. Verdict impact is unmeasured; the independence premise of C-03 is "requested, not served" already.

ID: INV-014
CATEGORY: sufficiency_challenge
ASSUMPTION: The enable trigger ("arm beats A2 on module-matched ground truth; tasklist review is the only module with ground truth", consensus 5) can be satisfied on a lane that can host exchange.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Tasklist review reaches the panel through reflect UC-1 (A 3.3). Reflect Tier 2 runs on the swarm HTTP transport, one user message, no tool loop (`openai_compat.py:384-388`, `ensemble.py:1-5` per both papers), or on `reflect-reviewer`, which has no Bash (`agents/reflect-reviewer.md:5,8`). B 2.6 and A 3.4 both keep exchange off for reflect. So the only module with ground truth has no hook-capable lane at HEAD; a "module-matched" arm can only run on the E2 raw launcher. The build trigger (C-07 launcher) does not require that tasklist review be hosted on it, so the transport could be built and still have no module on which the enable rule can be met. Depends on the reflect-tier2-engine-composition slot, not resolved here.

ID: INV-015
CATEGORY: sufficiency_challenge
ASSUMPTION: The A-layer alone is cost-safe because the kit is the only priced item and defaults `off`.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: H2 is unconditional (A 3.1 item 2) and its repair may be a re-ask, a full extra reviewer attempt; the study's dropped lines are 88 of 92 length failures, 48 of 49 blocking (variant-1 3.1 item 2, r08 [UNVERIFIED]), so re-ask frequency could be high. Re-asked attempts also sit outside `cap_reviews` (C-03 INV-001 concerns refusal spend the same way). The consensus cost gate (measurement 2) prices only the kit. H1 adds lines to every brief, which is small but not measured. No cap or counter is specified for repair re-asks.

ID: INV-016
CATEGORY: sufficiency_challenge
ASSUMPTION: The central premise of the deferral, "no exchange arm has been measured against the static kit", still holds at the current E2 head.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The team lead records commits up to `e2f2ac268` (2026-11-14 19:19, "counted results, replicates and write-up for the five collaboration designs") as [POST-BASELINE]; both advocates read only up to `c44c98a77` (r2-A "Evidence limits"; r2-B reads no post-baseline fact). The commit exists locally (`git cat-file -t e2f2ac268` prints `commit`) and was not read, per instruction. If that write-up shows an exchange arm separating from A2, the "defer" half of the consensus and the build-trigger ordering change. Open item only; the debate is not rerun on it.

---

Summary
- Findings: 16 (ADDRESSED 2: INV-001, INV-012; UNADDRESSED 14).
- Severity: HIGH 2 (INV-005, INV-009), MEDIUM 12, LOW 2 (INV-001, INV-012).
- By category: state_variables 2, guard_conditions 3, count_divergence 2, collection_boundaries 1, interaction_effects 4, sufficiency_challenge 4.
- Consensus pieces that held under probing: no hook/`_FRESHNESS_SCRIPTS`/adapter built now, owner and expiry on the trigger, design-note contents, kit lint.
- Open premise item: INV-016 (E2 write-up at `e2f2ac268` unread); unresolved dependencies: C-06 (H2 policy), C-07, C-08, X-13, reflect-tier2-engine-composition.
