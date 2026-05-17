---
spec_type: validation
target_release: task-sc-task-directional-merge
stance: adversarial-attack
focus: [tradeoffs, invariants, failure-modes, evidence]
source_under_attack: .dev/releases/current/task-sc-task-directional-merge/artifacts/final-merge-plan.md
source_line_range: 1-477
claim_under_attack: "PASS. ZERO OPEN FINDINGS." (line 46)
---

# Variant-2 — Adversarial validation spec (ATTACK)

## 1. Executive indictment

The plan's headline assertion "**PASS. ZERO OPEN FINDINGS.**" (line 46) survives only under a narrow reading where every closure clause is treated as definitional rather than operational. Five structural defects rebut the claim: (a) the F-02 ordering enforcement (lines 115-118) is a `grep -n -E` against a regex with alternation, which matches occurrence-order, not positional-order, of the three tokens and is silently satisfied by any file that contains the three names in any order across multiple sections; (b) F-03's `git_status=dirty` clause (line 130) closes one of three failure modes for `git status` and leaves "tool-not-installed" and "not-a-repo" unspecified, which the closure paragraph itself silently widens via the "graceful skip" analogy without binding it; (c) F-04's trinary `absent|empty|malformed` (line 144) collapses three distinguishable disk states into one log token and never specifies which observer determines "malformed" — pytest, the YAML loader, or a schema check; (d) the row-instance count of 79 (line 69) condenses into 65 CR-IDs via 14 absorption sub-rows and CR-REF-BUCKET-A..H, but the bucket-condensation table is not enumerated anywhere in the plan, defeating the AC #1 traceability promise; (e) CR-TASK-12's "seven-diff" audit (lines 244, 367) is fragile post-CR-DEP-03 because three of the six donor diffs target files that CR-DEP-03 hard-deletes (lines 178-184, 254), and the plan does not specify whether the audit runs before, during, or after donor deletion. Each defect maps to a specific INV-01..INV-05 attack vector enumerated in §7 below.

## 2. CR-FM-* attacks (frontmatter)

### 2.1 CR-FM-01 — closed-enum default-fall-through (line 212)
**Attack.** The acceptance digest says "optional `Tier:` field; closed-enum; default `STANDARD`." This does not specify behavior when the field is present but contains whitespace, mixed-case (`Standard`), trailing comments, or a YAML alias. CR-TASK-02 (line 216) only handles "malformed Tier:" at the task-level; the closed-enum validator's normalization rules are unstated.
**Invariant broken.** INV-05 (refusal-of-definition) — by silently lower-casing or trimming, the parser would author a definition of "what counts as STRICT" at parse time. By rejecting all non-canonical forms, it widens the HALT semantic at pre-loop entry, attacking INV-01.
**Acceptance criterion missing.** A canonicalization table (input → normalized form → accept/reject) bound to CR-FM-01 and grep-verifiable against the parser source.

### 2.2 CR-FM-02 — per-item read vs dispatch boundary (lines 213, 99-105)
**Attack.** The F-01 closure (line 102) forbids the per-item marker from "re-firing Gate 1, selecting a different `rf-qa` roster, substituting a different EXECUTE path, or changing the item-type dispatch table" — but the closure does not name a positive list of permitted consumers. Any future consumer that reads the per-item marker for an effect not explicitly in the negative list (e.g., changing a logging verbosity threshold, or selecting a different baseline file path per-item) is unbounded. The ME-1 audit gate (lines 103, 424) is a procedural retro-check, not a structural one.
**Invariant broken.** INV-05 — the per-item marker becomes a soft definitional channel that propagates through "tier-conditioned reads" without a closed enumeration of which behaviors are gate-eligible. CR-TASK-07 baseline-skip is the only named consumer (line 101); everything else is open.
**Acceptance criterion missing.** A closed enumeration of authorized per-item marker consumers (current list = {CR-TASK-07 baseline-skip}); any new consumer requires a new manifest exception, audited at the row level, not at design-review time.

### 2.3 CR-FM-03 — backward-compat shim drift (line 214)
**Attack.** "existing TASK-* files validate clean; default `STANDARD`; NO migration" — but the shim's lifetime is unbounded. If a future audit row removes the default-fall-through, every TASK-* file authored under the shim becomes invalid silently. CR-FM-03 has no acceptance criterion for shim retirement.
**Invariant broken.** INV-04 (resumability) — a future commit that drops the default would brick every resumed task created under the v3.75 surface. The plan's INV-04 survival argument (line 86) leans on "CR-FM-03 compat shim" without binding its persistence.
**Acceptance criterion missing.** A sunset audit row (e.g., CR-AUDIT-FM-03-SUNSET) declaring the shim binding for at least N task generations or until an explicit migration row lands.

### 2.4 CR-FM-04 — audit scope vs grep semantics (lines 115-118, 243)
**Attack.** The ordering check `grep -n -E "(path_override_check|tier_field_validate|gate_1_dispatch)" [src]/skills/task/SKILL.md` returns lines containing ANY of the three tokens in source order. If the file contains a docstring or comment that mentions `gate_1_dispatch` above the three function calls (e.g., a "Phase 7 obligations" section that lists invariants in any order), the grep returns the tokens in the wrong line order even when the code is correctly ordered, OR returns the tokens in the right order when the code is reordered (because the docstring still appears first). The grep is occurrence-order, not call-site-order. This is a falsifiable defect.
**Invariant broken.** INV-01 — the F-02 closure's reliance on the grep produces false negatives (commits blocked when correct) and false positives (commits allowed when incorrect), eroding the structural guarantee that CR-7 / CR-8 ordering enforces F1 progress semantics.
**Acceptance criterion missing.** Either an anchored regex over the function-definition section only (delimited by `def …` or a sentinel block), or an AST-level check, or a line-range-pinned grep (`sed -n '<start>,<end>p' | grep`).

### 2.5 Per-item marker malform — CR-TASK-02 only covers task-level (line 216)
**Attack.** CR-TASK-02 rejects malformed `Tier:` at the task-level. There is no symmetric row that rejects malformed per-item `(Tier: …)` markers. A per-item marker reading `(Tier: stricT)` or `(Tier: STRICT,STANDARD)` or `(Tier:)` has unspecified behavior. CR-FM-02 says the parser "reads marker; fallback to task-level" — silently falling back on malform is a definitional decision masquerading as a parse rule.
**Invariant broken.** INV-05 — silent fallback is the parser authoring a tolerance for syntactic drift. INV-04 — different task generations under different parsers see different effective tiers for the same file.
**Acceptance criterion missing.** A CR-FM-02 sub-clause: malformed per-item markers emit `gate-1: per-item-marker malformed=<line-N> action=<reject|fallback-with-warning>` and a single binding disposition (reject is consistent with CR-TASK-02; fallback is not).

## 3. CR-TASK-* attacks

### 3.1 CR-TASK-01 / CR-TASK-04 sentinel comments (lines 118, 215, 218)
**Attack.** The sentinel `# CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder.` is a comment in markdown source (the file `[src]/skills/task/SKILL.md` is a SKILL.md, not Python). Markdown comments are not load-bearing to any interpreter — they are documentation. The "ordering" they document is procedural, not enforced. The CR-FM-04 grep checks for the presence of the comment string, not for any operational effect.
**Invariant broken.** INV-01 — relying on a markdown comment to enforce F1 ordering is type-confusion. The plan treats SKILL.md as if it were executable.
**Acceptance criterion missing.** The plan must either (a) move the load-bearing ordering into an executable artifact (e.g., a pytest fixture, a YAML schema, or a JSON ordering manifest) and grep that, or (b) downgrade the sentinel claim from "binding" (line 118) to "informational" and remove the F-02 MEDIUM-severity closure status.

### 3.2 CR-TASK-02 task-level malform — silently widens HALT (line 216)
**Attack.** "malformed Tier: rejected" is a HALT at pre-loop entry. The F-03 closure (line 130) explicitly forbids new HALT semantics on dirty-tree. CR-TASK-02 authored a HALT on parse-error without an analogous justification. Why is parse-rejection allowed to halt INV-01 progress when git-dirty is not?
**Invariant broken.** INV-01 — inconsistent HALT policy between two pre-loop conditions that are equally outside the user's immediate control.
**Acceptance criterion missing.** A unified pre-loop HALT policy table listing every pre-flight condition and its disposition (HALT vs WARN-CONTINUE vs SKIP), with a binding rule that new conditions must map to an existing row.

### 3.3 CR-TASK-03 per-item marker (lines 217, 102-105)
**Attack.** Acceptance criterion adds "per-item `(Tier: …)` overrides task-level for tier-conditioned reads only." The "tier-conditioned reads only" gate is a phrase, not a test. There is no enumerable list of tier-conditioned reads (see §2.2). The closure relies on ME-1 design-time review, not a runtime guard.
**Invariant broken.** INV-05.
**Acceptance criterion missing.** Same closed enumeration as §2.2, plus a runtime guard that emits `tier-conditioned-read: consumer=<name> per-item-tier=<value>` for every consumer and is grep-auditable.

### 3.4 CR-TASK-06 git_status — three failure modes, one named (lines 124-134)
**Attack.** F-03 closes only the `git_status=dirty` branch (line 130). Three other observable states are unspecified: (i) `git` not installed (exit 127); (ii) directory is not a git repo (`git status` exits non-zero with "not a git repository"); (iii) `git status` hangs (large repo, filesystem lock, NFS stall). The "graceful skip" analogy (line 132) is invoked but not bound to these branches.
**Invariant broken.** INV-01 — any of the three unspecified branches could produce HALT, WARN-CONTINUE, or SKIP depending on the implementer. INV-04 — resumed tasks under different runtimes see different pre-flight outcomes for the same task file.
**Acceptance criterion missing.** A four-row matrix for `git_status`: {clean, dirty, tool-absent, not-a-repo, error-other} × {emit, action}, with all five rows bound and the emitted Task Log line specified for each.

### 3.5 CR-TASK-07 baseline trinary (lines 138-148, 233)
**Attack.** AC-CR-TASK-09-F04 (line 144) collapses three distinct on-disk states — `absent` (file does not exist), `empty` (zero bytes), `malformed` (YAML parser error or schema violation) — into a single log reason field. But these states are observable at different layers: `absent` is a filesystem call, `empty` is `stat().st_size == 0`, `malformed` requires a YAML parse attempt, and "schema-violating" requires a separate schema check that the closure does not name. A file containing `null` parses to an empty Python object — is that `empty` or `malformed`?
**Invariant broken.** INV-03 — the classification floor depends on which observer fires first. A pytest fixture that loads the YAML may see `empty`; a separate schema validator may see `schema-violating`. The rf-qa escalation queue receives different content for the same on-disk state.
**Acceptance criterion missing.** A four-state table {absent, empty, parse-fail, schema-fail} with the specific observation tool named for each (e.g., `os.path.exists`, `os.path.getsize`, `yaml.safe_load`, `<schema>`), and the disposition for each.

### 3.6 CR-TASK-08 prohibitions catalog (line 234)
**Attack.** "F1 continues" — the closure does not specify behavior when a prohibition fires inside a verifier subagent context (mid-phase rf-qa invocation per F-05). Does the prohibition halt the verifier? Continue the verifier but halt the parent? Continue both?
**Invariant broken.** INV-02 (prohibited-actions catalog) — under-specified for the F-05 widened surface.
**Acceptance criterion missing.** Prohibition disposition matrix across {root F1, verifier-spawned F1, mid-phase rf-qa context}.

### 3.7 CR-TASK-09 mid-phase INV-03 widening — precedent risk (lines 25-26, 152-160, 235)
**Attack.** § 0 of the plan (lines 25-26) declares the mid-phase invocation an "authorized INV-03 surface extension" with three justifications: (a) routes to existing identity, (b) uses existing spawn pattern, (c) named by TU-7. But each of (a), (b), (c) is satisfied by any future widening that reuses the rf-qa identity and the `SKILL.md:191-198` spawn pattern. The closure establishes a **precedent template** for surface-widening that is procedurally lower-cost than authoring a manifest exception. Obligation #7 (line 425) says "any future surface widening beyond these three must be re-authorized via a fresh manifest exception" — but the F-05 widening itself was authorized without a manifest exception, just a § 0 paragraph. The obligation does not bind the F-05 author's own pattern.
**Invariant broken.** INV-03 — the floor is preserved, but the *closure mechanism* for INV-03 surface decisions is silently demoted from manifest-exception authorship to plan-paragraph authorship.
**Acceptance criterion missing.** Either (a) F-05 itself must be backed by a retroactive manifest exception (ME-10) and named in the manifest, or (b) the plan must explicitly note that § 0 mid-phase routing was authorized under a one-time procedural carve-out that does NOT generalize.

### 3.8 CR-TASK-10 side-effect file (line 236)
**Attack.** "side-effect file present on STRICT items with TFEP fire; seven-field schema." The seven fields are not enumerated in the plan. INV-04 resumability claim (line 86) names "TU-8 incident-report file on disk" but does not bind the schema. A resumed task that reads an older incident file with a different field count would see undefined behavior.
**Invariant broken.** INV-04.
**Acceptance criterion missing.** The seven field names and their types, bound in the row and verifiable via a schema file check in CR-FM-04 audits.

### 3.9 CR-TASK-11 md5sum (line 242)
**Attack.** `md5sum` is a collision-vulnerable hash. The merge gate uses it as a synchronization proof between `[src]` and `[.claude]`. Collision attack is implausible for accidental drift but defeats the audit's evidentiary value for adversarial scenarios (a malicious commit could craft a `[.claude]` mirror with matching md5 but divergent content).
**Invariant broken.** Indirect — R-RULE-10 (source-of-truth discipline), which underlies the INV-04 resumability claim if the `[.claude]` mirror is what a runtime reads.
**Acceptance criterion missing.** Replace md5sum with sha256sum or sha512sum; mechanical change.

### 3.10 CR-TASK-12 seven-diff fragility post-CR-DEP-03 (lines 244, 254, 367, 422)
**Attack.** CR-TASK-12 runs six verbatim diffs against donor strings (line 244). After CR-DEP-03 (line 253), the donor file `[src] src/superclaude/skills/sc-task-protocol/SKILL.md` is **hard-deleted**. The six diff invocations now target a non-existent file. The plan does not specify whether CR-TASK-12 runs (a) before CR-DEP-03 (Step 4 vs Step 6 — Step 4 is M-sync, Step 6 is M4-B, so Step 4 precedes Step 6; lines 365-381), or (b) is itself a regression test that must re-run on every commit. If (a), the seven diffs are a one-shot audit that cannot re-fire after Step 6 — INV-01 ordering verification has no persistent witness. If (b), the audit is broken from Step 6 onward.
**Invariant broken.** INV-01 — the load-bearing ordering audit (per F-02 closure, line 426) has a finite lifetime that ends before the build is complete.
**Acceptance criterion missing.** Either (a) snapshot the donor strings into a frozen test fixture (e.g., `tests/fixtures/donor-blocks/`) before Step 6 and re-run diffs against the fixture, or (b) explicitly mark CR-TASK-12 as Step-4-only with an obligation to re-author a successor audit at Step 6.

## 4. CR-DEP-* attacks

### 4.1 CR-DEP-03 procedural authorization chain — no verifier role bound (lines 174-188, 253)
**Attack.** The F-07 chain (lines 180-184) traces "sprint goal → T06.03 → § 2 rubric → § 4 traceability → structural precondition." Each link is a document reference; no link names a **role** (human or agent) that signs off on the hard-deletion. Compare with INV-03's rf-qa binding (line 85): a role is named and re-spawnable. F-07's chain is a paper trail with no signatory. The closure says "Future reviewers should accept the chain and not require a retroactive manifest amendment" (line 186) — this asks future reviewers to defer to a chain that has no verifier role.
**Invariant broken.** Not a load-bearing invariant directly, but it weakens the "demonstrated, not asserted" evidentiary standard (line 472). INV-04 by proxy — donor deletion is irreversible for resumed tasks that referenced the donor.
**Acceptance criterion missing.** Name a verifier role (e.g., `rf-deprecation-auditor` or rebind to `rf-qa`) that runs at commit time and confirms the chain links are intact. The role's spawn must be in the Step 6 pre-commit gate (line 387), not in a documentation paragraph.

### 4.2 S-1 PRD precondition — no time-bounded abort (lines 319-325, 373)
**Attack.** S-1 requires TASK-PRD-20260514-121039 to complete (status `🟢 Done`) before Step 5. The plan offers options (b) snapshot and (c) abort-restart from `compat-hazard-report.md` HZ-03 "if option (a) is infeasible" (line 325). But "infeasible" is undefined; there is no time-bounded abort trigger. If the PRD stalls at `🟠 Doing` for N hours / days / weeks, when does Step 5 escalate to option (b) or (c)?
**Invariant broken.** None directly, but the closure relies on an unbounded wait that could indefinitely defer the whole merge sequence.
**Acceptance criterion missing.** Either (i) a deadline (e.g., "if PRD not Done within 7 days, default to option (b) snapshot") or (ii) a named decision authority for the option (a)→(b)/(c) escalation.

### 4.3 CR-DEP-04 directory absence (line 254)
**Attack.** "both `src/` and `.claude/` directories absent" — does not specify whether absence is verified at commit time, pre-commit hook time, or CI-gate time. A directory could be re-created by `make sync-dev` between the pre-commit check and the push (S-3 mitigates this for sync, but not for human re-creation).
**Invariant broken.** INV-04 indirectly — a resumed task that references a re-appearing directory sees inconsistent state.
**Acceptance criterion missing.** A specific gate point in Step 6 (line 387) that runs the absence check.

### 4.4 CR-DEP-05 grep audit (line 257)
**Attack.** `grep returns zero matches on mcp-servers: / personas:` on `[src]` and `[.claude]`. The grep is over which file extensions? `**/*.md`? `**/*.yaml`? Binary files? Hidden directories (`.git/`)? `find ... -path '*.git*' -prune`? Unspecified scope makes the audit non-reproducible.
**Invariant broken.** None directly; weakens AC #1 evidence.
**Acceptance criterion missing.** Explicit `find` / `grep` invocation with scope flags and excluded paths.

## 5. CR-DIST-* / CR-REF-* / CR-DOC-* attacks

### 5.1 Bucket-condensation 79 → 65 unenumerated (line 69)
**Attack.** § 2.2 (line 69) reports "79 rows including bucket sub-IDs, condensed into 65 distinct CR-IDs." The 14-row delta condenses CR-REF-18 cluster (line 295: "14 sub-rows"). But this accounts for 14 of the 14; what about the CR-REF-BUCKET-A..H labels (line 18)? Eight bucket labels are referenced but their row-instance count is not given. The condensation arithmetic 14 (absorption) + 2 (mechanical/audit) + 5 (deprecation) + 39 (reference) + 6 (distribution) + 13 (documentation) = 79 is asserted on line 69, but the inverse mapping (which buckets condense to which CR-IDs) is not present.
**Invariant broken.** AC #1 (traceability) — every CR row must trace; the condensation arithmetic is opaque.
**Acceptance criterion missing.** A condensation table: 79 row-instances → 65 CR-IDs with the bucket sub-row mapping enumerated.

### 5.2 67 vs 65 mismatch — 67 PASS, 65 distinct CR-IDs (lines 17, 28, 36, 69)
**Attack.** Line 17 says "67 row-line-items / 65 distinct CR-IDs"; line 36 says "Phase 6 plan items (CR rows) — PASS 67 / 67"; line 28 says "the 67-row count, the 65 distinct CR-IDs". The verdict roll-up (line 36) asserts PASS over 67 rows, but the two extra rows (67 − 65 = 2 duplicate CR-IDs) are not named. Which CR-ID appears twice? The plan never identifies the duplicates, so the PASS claim cannot be re-verified at the CR-ID level.
**Invariant broken.** AC #1 traceability.
**Acceptance criterion missing.** Name the two row-line-items that share a CR-ID with another row, and state which row in each pair carries the PASS verdict (or whether both do, and what the duplication means).

### 5.3 CR-REF-18 cluster vs body-rewrite policy (line 295)
**Attack.** "`DEPRECATION-NOTE.md` exists at cluster root; no body rewrites in 14 files." But the cluster root is unnamed. If a future audit row depends on a specific cluster path, the audit cannot locate it.
**Acceptance criterion missing.** Name the cluster root path explicitly.

### 5.4 CR-DOC-01 atomicity with Step 5 OR Step 8 (lines 375, 397)
**Attack.** CR-DOC-01 is listed as atomic with Step 5 (line 375) AND as "if not landed in Step 5" in Step 8 (line 397). This is a defensible flexibility but the disambiguation rule is missing: under what condition does CR-DOC-01 defer from Step 5 to Step 8?
**Acceptance criterion missing.** A binding disposition: CR-DOC-01 MUST land in Step 5; Step 8 is the fallback only if Step 5's pre-commit gate fails AND a hot-fix is authorized.

### 5.5 CR-DOC-13 R-RULE-11 audit scope (line 411)
**Attack.** Final audit row over CR-DOC-01..12 — but R-RULE-11 is the ledger re-proposal rule, which spans ALL 65 CR-IDs, not just CR-DOC-*. The audit row's scope is under-cast.
**Acceptance criterion missing.** Either rename CR-DOC-13 to a scoped doc-only audit, or widen its scope to all 65.

## 6. INV-01..INV-05 attack vectors

| Invariant | Closure clause leaned on | Attack |
|---|---|---|
| INV-01 (F1 loop semantics) | F-03 dirty-tree warn-continue (line 130); F-02 sentinel comments (line 118) | §3.4 unspecified git failure modes can introduce non-progress states; §3.1 markdown comments cannot enforce executable ordering. |
| INV-02 (Prohibited-actions F2) | TU-6 "reinforces F2" (line 84) | §3.6 prohibition disposition is unspecified for verifier-spawned and mid-phase rf-qa contexts opened by F-05. |
| INV-03 (Phase-gate rf-qa) | F-05 "authorized widening" (lines 25-26) | §3.7 the closure establishes a paragraph-level surface-widening precedent that obligation #7 does not retroactively bind. |
| INV-04 (Resumability) | CR-FM-03 shim, TU-5 baseline YAML, TU-8 incident report (line 86) | §2.3 shim has no sunset binding; §3.8 incident schema unspecified; §3.4 git-failure-mode divergence between runtimes. |
| INV-05 (Refusal-of-definition) | "TU-1 Tier: is metadata, not work-definition" (line 87) | §2.1 closed-enum normalization unspecified; §2.5 per-item marker malform unspecified; §2.2 tier-conditioned-reads consumer list open. |

## 7. Concrete attack scenarios

### Scenario A — CR-FM-04 grep false positive (INV-01)
- **State before.** `[src]/skills/task/SKILL.md` contains the three function calls in the WRONG order at the row 1 site (`tier_field_validate(); path_override_check(); gate_1_dispatch()`), but a docstring 200 lines earlier reads "the canonical order is `path_override_check`, `tier_field_validate`, `gate_1_dispatch`."
- **Action.** Run `grep -n -E "(path_override_check|tier_field_validate|gate_1_dispatch)" [src]/skills/task/SKILL.md`.
- **State after.** Grep returns the three names in correct line order (because the docstring fires first). Commit gate passes. Broken code lands.
- **Invariant broken.** INV-01 (F1 progress depends on path-override firing first).

### Scenario B — git not installed on CI worker (INV-01, INV-04)
- **State before.** CI worker image has `git` removed for size optimization. STRICT pre-flight runs `git_status_clean_tree_check`.
- **Action.** Subprocess `git status` exits 127 (command not found).
- **State after.** F-03 closure (line 130) handles only `git_status=dirty`; the 127 exit is undefined. Implementer A treats it as graceful-skip (line 132); implementer B treats it as a refuse-task-entry HALT.
- **Invariant broken.** INV-01 if HALT; INV-04 if two CI runtimes diverge for the same task file.

### Scenario C — baseline file contains `null` (INV-03)
- **State before.** `research/test-baseline.yaml` exists, 5 bytes, content `null\n`.
- **Action.** AC-CR-TASK-09-F04 (line 144) fires. Observer 1 (`yaml.safe_load`) returns Python `None`; Observer 2 (`os.path.getsize`) returns 5 (not zero).
- **State after.** Observer 1 calls it `empty` (None → no entries); Observer 2 calls it not-empty. Closure logs `reason=empty` OR `reason=malformed` depending on observer order. rf-qa escalation queue receives ambiguous evidence.
- **Invariant broken.** INV-03 (floor preserved but content non-deterministic).

### Scenario D — CR-TASK-12 audit after CR-DEP-03 (INV-01)
- **State before.** Step 4 has run; CR-TASK-12 seven-diff audit passed. Step 6 lands CR-DEP-03; donor file hard-deleted (lines 253, 184).
- **Action.** Step 7 introduces a regression in row 1 ordering. A re-run of CR-TASK-12 is attempted.
- **State after.** Six of the seven diffs error on missing donor file. The audit cannot re-validate. Regression lands undetected.
- **Invariant broken.** INV-01 (load-bearing audit has finite lifetime).

### Scenario E — Per-item marker with no consumer (INV-05)
- **State before.** A future contributor adds a new behavior `verbose_logging` gated by per-item `(Tier: STRICT)`. ME-1 review is procedural and the design-time review is skipped (rushed sprint).
- **Action.** The per-item marker now drives a new consumer not in the F-01 negative list (does not re-fire Gate 1, etc.) and not in any positive list (because none exists).
- **State after.** New consumer ships. ME-1 audit gate (line 424) does not retroactively flag it because the obligation says "any FUTURE change … MUST be reviewed" but the change has already landed.
- **Invariant broken.** INV-05 (per-item marker silently becomes a definitional channel).

### Scenario F — S-1 unbounded wait (failure-mode, not invariant)
- **State before.** TASK-PRD-20260514-121039 stalls at `🟠 Doing` for 30 days. Step 5 is blocked per S-1 (line 321).
- **Action.** No deadline triggers options (b) or (c). Whole merge sequence frozen.
- **State after.** Sprint slips indefinitely. No invariant is broken — but the closure's "binding execution plan" claim (line 462) is undermined operationally.
- **Invariant broken.** None directly; AC #3 binding effectiveness eroded.

### Scenario G — md5 collision in CR-TASK-11 (R-RULE-10)
- **State before.** Adversarial commit crafts a `[.claude]` mirror file with the same md5 as the `[src]` original but different content.
- **Action.** CR-TASK-11 audit (line 242) passes. `make verify-sync` returns 0.
- **State after.** Runtime reads `[.claude]` and behaves differently from `[src]`. INV-04 (resumability) reads divergent definitions.
- **Invariant broken.** INV-04 indirectly.

## 8. Acceptance criteria for closing the attacks (what the plan must add)

The plan, to survive the variant-2 attack and earn the "ZERO OPEN FINDINGS" claim, must add (in priority order):

1. **AC-ATK-01 (highest)** — Replace the F-02 alternation grep (lines 116-117) with a line-range-pinned or AST-level check that verifies call-site order, not occurrence order. Document the line-range or AST locator in CR-FM-04 acceptance criteria.
2. **AC-ATK-02** — Add a five-row matrix for `git status` failure modes to CR-TASK-06 (clean / dirty / tool-absent / not-a-repo / error-other), with a bound Task Log line and disposition per row.
3. **AC-ATK-03** — Disambiguate the `absent|empty|malformed` trinary in AC-CR-TASK-09-F04 (line 144) into four states (absent, empty, parse-fail, schema-fail) with the observation tool named for each.
4. **AC-ATK-04** — Enumerate the 79 → 65 condensation table (CR-REF-BUCKET-A..H sub-row counts; CR-REF-18 14-row mapping; the 2 duplicate-CR-ID rows in the 67-row PASS roll-up).
5. **AC-ATK-05** — Add a closed enumeration of authorized per-item marker consumers (currently {CR-TASK-07 baseline-skip}); a new consumer requires a new manifest exception authored at row level.
6. **AC-ATK-06** — Specify CR-TASK-12 lifetime: either snapshot donor strings into a frozen fixture before Step 6, or mark the audit Step-4-only with a successor-audit obligation.
7. **AC-ATK-07** — Add a verifier role to the F-07 procedural authorization chain (lines 180-184); the role spawns at Step 6 pre-commit and confirms chain integrity.
8. **AC-ATK-08** — Add a time-bounded abort to S-1 (line 321): N-day deadline or named decision authority for option (a) → (b)/(c) escalation.
9. **AC-ATK-09** — Replace md5sum with sha256sum in CR-TASK-11 / CR-DEP-02 / CR-DIST-02 audits.
10. **AC-ATK-10** — Add a unified pre-loop HALT policy table (CR-TASK-02 parse-reject vs CR-TASK-06 dirty-tree warn-continue) and bind every new pre-flight condition to a row in it.
11. **AC-ATK-11** — Either backdate F-05 mid-phase routing to a retroactive manifest exception (ME-10) or explicitly mark the § 0 paragraph closure as a one-time non-generalizing carve-out (close the precedent loophole identified in §3.7).
12. **AC-ATK-12** — Bind CR-FM-03 shim lifetime with a sunset audit row; bind CR-TASK-10 incident schema (seven fields enumerated); bind CR-FM-01 canonicalization rules (normalization table).
13. **AC-ATK-13** — Downgrade CR-TASK-01 / CR-TASK-04 sentinel comments from "binding" (line 118) to "informational" if they remain in markdown; OR move the load-bearing ordering into an executable artifact and audit that.
14. **AC-ATK-14** — Specify CR-DEP-05 grep scope (file extensions, excluded paths) and CR-REF-18 cluster root path explicitly.
15. **AC-ATK-15** — Disambiguate CR-DOC-01 Step 5 vs Step 8 disposition (lines 375, 397).

## 9. Tradeoffs the plan does not name

The plan presents the F-01..F-08 closures as costless tightening. Each closure has a tradeoff that is unnamed and therefore unbudgeted:

- **F-01 closure (lines 99-105) tradeoff.** Naming the consumption shape "tier-conditioned read" widens the attack surface against INV-05 by making "read" semantically open-ended. The cost of closing F-01 is the implicit grant of an unbounded read channel. The plan does not enumerate the cost.
- **F-02 closure (lines 109-120) tradeoff.** Adding two greps + a sentinel comment shifts the enforcement burden from structural ordering to documentation discipline. If the SKILL.md is auto-generated by any future tool (e.g., a markdown templater), the sentinel comments could be stripped without triggering the grep — because the function names would still be present in source-order. The cost is a coupling between the audit tool and the source file's editing toolchain that no row binds.
- **F-03 closure (lines 124-134) tradeoff.** Choosing Reading A (warn-and-continue) over Reading B (refuse-entry) preserves INV-01 but exposes the runtime to dirty-tree-induced behavior divergence in downstream commits. The plan acknowledges this is a tradeoff (line 132) but does not name a mitigation: a warned-and-continued dirty tree could land partial state into the merge sequence.
- **F-04 closure (lines 138-148) tradeoff.** Over-escalate floods the rf-qa queue. The plan notes "the cost is a possibly-noisier escalation queue" (line 144). It does not specify when "noisy" becomes a refusal trigger. INV-03's floor is preserved but the verifier's throughput is unbounded.
- **F-05 closure (lines 152-160) tradeoff.** Mid-phase rf-qa routing means the verifier sees in-progress state instead of phase-complete state. The closure says this reuses the "existing spawn pattern" but does not address the semantic shift: rf-qa was designed to verify completed work, not adjudicate in-flight escalations. INV-03 floor is preserved; the verifier's evidence basis is silently changed.
- **F-06 closure (lines 164-170) tradeoff.** Citing `extension-point-contracts.md:11-17` as the INV anchor source means the line-pinned reference is brittle to any edit of that file. A formatting commit that adds one line above the anchor block silently breaks the citation. The plan's INV anchor is line-coupled, not symbol-coupled.
- **F-07 closure (lines 174-188) tradeoff.** Procedural authorization without a verifier role means the chain is auditable only by humans reading the linked docs. Automation cannot enforce it. CR-DEP-03's irreversibility (hard-delete) compounds the cost.
- **F-08 closure (lines 192-198) tradeoff.** Correcting "five" to "six" is mechanical, but the closure does not audit downstream references to "five" in other Phase 6 artifacts. If `merge-master.md:7` (line 194) still says "five," and downstream readers anchor to `merge-master.md` for any non-Phase-7-affected row, the inconsistency persists in the chain of trust.

## 10. Failure-mode coverage gaps (orthogonal to invariants)

The plan's failure-mode register lives in `compat-hazard-report.md` HZ-01..HZ-18 and is summarized in line 43 ("18 / 18 compat hazards MITIGATED"). The variant-2 attack identifies failure modes the register does not enumerate:

- **FM-01 (filesystem).** `make verify-sync` (lines 341, 387, 393) returns 0 on a successful sync, but does not check for symlink divergence between `[src]` and `[.claude]`. If `[.claude]` is symlinked to `[src]` (which would defeat R-RULE-10's source-of-truth model), md5sum / sha256sum / file-content checks all pass trivially.
- **FM-02 (timing).** Step 5 (line 371) is atomic across six rows. If any one of the six pytest invocations on line 333 (`tests/sprint/test_process.py && tests/sprint/test_tui_v2_wave2.py && tests/pipeline/test_process.py`) flakes intermittently, the atomicity guarantee creates a no-progress state where the commit cannot land but the soft-deprecation has been authored locally. Rollback policy is unspecified.
- **FM-03 (concurrent edits).** Two implementation sub-agents running in parallel (per the plan's downstream-sprint model) could land conflicting edits to SKILL.md at row 1 vs row 10. The atomic-merge obligation (line 421) is at the commit level, not at the edit level.
- **FM-04 (CI / local divergence).** `uv run pytest` (line 351) on a local machine and on CI may surface different results if env vars differ (e.g., `PYTHONHASHSEED`, locale, timezone). The pre-commit gate does not pin the env.
- **FM-05 (mkdocs build).** Step 8 gate is `mkdocs build` (line 399) returns 0 broken-link warnings. The version of mkdocs is not pinned. A mkdocs upgrade that changes broken-link detection semantics could pass or fail the same source tree.
- **FM-06 (deferred regen).** Step 10 (line 409) commits with "docs/generated/*: refresh deferred to next regenerator run." The next regenerator run is unscheduled. If it never runs, `docs/generated/*` permanently disagrees with `docs/` source. INV-04 by proxy (docs are read by resumed contributors).
- **FM-07 (encoding).** None of the greps specify text encoding. A file authored in UTF-16 (rare but observed in some Windows-authored markdown) would silently pass every grep with no matches because the byte patterns differ.
- **FM-08 (file rename).** Hard-deletion at CR-DEP-03 (line 184) is via the procedural chain. If the donor file is renamed instead of deleted (e.g., to `*.deprecated`), the absence check (line 254) passes for the original path but the file persists. R-RULE-11 violation indirect.

## 11. Evidence-completeness audit of the plan's own evidence chain

The plan cites six Phase 7 source artifacts (line 22): `plan-adversarial-review.md`, `file-reference-reverification.md`, `compat-hazard-report.md`, `traceability-gap-report.md`, `invariant-survival-walkthrough.md`, `validation-report.md`. Variant-2 makes no claim about the content of these artifacts (they are out of scope for this attack), but the plan's evidence audit has structural gaps:

- **EC-01.** Line 447 says "Grepping § 4 for each F-01..F-08 disposition." The grep pattern is unspecified. A reviewer using `grep -n "F-0"` versus `grep -n "F-01"` versus `grep -n "F-[0-9][0-9]"` gets different results.
- **EC-02.** Line 449 says "Confirming § 5 carries the same 67 row-line-items as `merge-master.md` § 1." The comparison method is unspecified — diff, manual count, hash? With four row-deltas (line 28), a textual diff returns non-zero by design; the audit cannot use diff naively.
- **EC-03.** Line 450 says "V/C/K verdicts carried forward unchanged." The carry-forward is asserted; no audit step re-derives V/C/K from `transfer-manifest.md` § 4. R-RULE-07 (line 437) requires re-scoring on drift; the plan claims zero drift (line 28), but the no-drift claim is itself unaudited in § 9 of the plan.
- **EC-04.** Line 452 says "the reviewer recomputes a sample of the no-drift V/C/K assessments by picking 3 TUs." Three of eight is a 37.5% sample. Sample-based audit cannot rule out a single drifted TU among the unsampled five.

## 12. Verdict

The plan's "ZERO OPEN FINDINGS" claim (line 46) is a definitional verdict, not an operational one. Twenty-three falsifiable attack vectors above (§§ 2-7) plus eight unnamed tradeoffs (§ 9) plus eight failure modes (§ 10) plus four evidence-completeness gaps (§ 11) identify under-specified closure predicates, ambiguous failure modes, structural fragility in the load-bearing audits (CR-FM-04 grep, CR-TASK-12 seven-diff), and unbudgeted costs across the F-01..F-08 closures. Each attack cites the specific source line(s) and names the broken or eroded invariant where applicable. The plan can survive these attacks by adding the fifteen acceptance criteria in § 8, but until they are added, the headline claim does not hold under adversarial reading. The plan is not "binding" in the strong sense the closure paragraph asserts (lines 46, 461-462); it is binding only in the procedural sense that downstream implementers have a paper trail to point at. Adversarial reviewers should require the plan to either (a) close the AC-ATK-01..15 list before authorizing a downstream implementation sprint, or (b) explicitly downgrade the "ZERO OPEN FINDINGS" claim to "ZERO HIGH-SEVERITY OPEN FINDINGS" with the residual MEDIUM/LOW items enumerated.
