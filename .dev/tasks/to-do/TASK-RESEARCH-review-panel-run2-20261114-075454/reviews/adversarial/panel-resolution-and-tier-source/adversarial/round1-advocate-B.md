# Round 1 advocate statement: Variant B (slot C-09, panel-resolution-and-tier-source)

Status: Complete

Tags: [CODE-VERIFIED] I read the line this session. [OBSERVED-RUNTIME] I ran a read-only `uv run --no-sync python` against HEAD in the worktree (run ids `run1..run40`, kind `first`). [UNVERIFIED] not checked by me. Paths are repo-relative to `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`.

## 1. Position summary

Variant B is the safer base: tier membership is owned by what decides what the gateway serves (Coder env slots named by `ccsession-models.json`, plus `MODEL-TIERS.md`), the packaged file is a checked snapshot, and strictness is a per-profile choice, so no shipped pin and no existing consumer changes. A's two measured discoveries (slot order, and the missing denominator) are real, and the best outcome is a hybrid (section 8): B's ownership and derive-and-compare check, soft default with per-profile strict, B's always-written denominator plus A's derived shortfall, and A's scarcest-first order as an opt-in. My own new measurement shows that scarcest-first with the soft default already removes every gateway repeat, which weakens the main reason A gives for flipping the default.

## 2. Steelman of Variant A

The strongest version of A: a repeated model in a panel is a decision nobody made. Under soft distinctness the duplicate is invisible in the resolution (A 3.3); under strict it becomes a named skipped slot, so the failure is on the page. A package file is also the one thing in this chain that is release-gated by tests, deterministic and hashable (`tiers_sha256`, `panel.py:694` [CODE-VERIFIED]), while `ccsession-models.json` reaches every workspace from master with no panel test at all (`models.py:6-12, 59-63` per A and B E2). A also found something B did not: the gateway shortfall (30 of 40) is a slot-order artifact, not a model-count limit. A is candid about cost (4.2 lists INV-C, INV-L and the pin it rewrites), concedes in 7.4 that the single-source claim and the strictness default can be judged apart, and names two things it cannot answer (7.5). Where A is right: the order finding (U-001), the ladder as a function of (tier, model) (U-002), the M1 measurement design (U-003), and that B's `distinct_models` does not appear in soft runs of a profile that "records neither key" (X-001).

## 3. Strengths claimed for Variant B

1. The owner statement matches what actually decides serving. `MODEL-TIERS.md:11-14` says the Coder env, `ccsession-models.json` and the page "change together" [CODE-VERIFIED]. A's own observation (3.1 item 3: env has `T3Model01..06` with a duplicate `Qwen3.8-max`, repo names two tier-3 slots) shows the env is what moves; A's M3 concedes A is "wrong on the single-source claim" if the env changes faster than releases. B asks for a check against the owner, not a claim that the package is the owner.
2. The derive-and-compare check catches what a count check cannot. [OBSERVED-RUNTIME] I prototyped it (parse the backticked ids of the third column of the `MODEL-TIERS.md` section 1 rows, compare ordered ids with `aliases.<tier>.models`, compare length with `len(models_env)`). It is green today for all six tiers (rows parsed 2, 3, 6, 4, 2, 3 ids; tier0 has 2 and is skipped). Mutations: swapping `tier2` positions 1 and 2 is caught by derive and passes the count check; replacing `tier4[2]` with `muse-ember-1.0` is caught by derive and passes the count check. The check A proposes ("counts plus first model", the shape of `test_review_panel_live7.py:92-98` [CODE-VERIFIED]) sees neither.
3. Zero existing pins move. B leaves the library default, the CLI default and the packaged file unedited, so `test_review_cli.py:52-61` (default anthropic-only prints `t1b-1, t2-1, t3-1, t3-2`, [CODE-VERIFIED]), `test_review_panel_exclusion.py:53-72` and the packaged-tier golden stay green. A rewrites `test_review_cli.py:56-61` and regenerates the packaged golden twice (A 4.2).
4. A default flip would have no present beneficiary. Reflect already passes `--strict-distinct` (`SKILL.md:340` [CODE-VERIFIED]); A's own plan (2.2) makes the spec loop declare soft. After A's change both existing consumers run the same mode as today, and only a future consumer sees a different default, at the price of a pin rewrite and a prompt-copy lag window (A 4.2, C-03 INV-013).
5. Per-profile distinctness is consistent with the adjudicated C-03 split (degrade profiles fail closed; reflect keeps `shortfall: visible`).
6. Additive output keys follow an existing precedent: `skipped_slots` and `excluded` are written only when an exclusion argument is used (`panel.py:700-707` [CODE-VERIFIED]). Resolution output is not checked against a closed key set; the closed sets are `_PANEL_KEYS` (`panel.py:37`, checked at `:175-176`) for templates and the environment keys of the tier file (`:373`) [CODE-VERIFIED by grep].
7. `requested_slots` closes the denominator for C-02 INV-001 and C-03 INV-007 without depending on `--resolution` being passed. `resolve` drops skipped slots from `reviewers` (`panel.py:647-656` [CODE-VERIFIED]), so the template count cannot be recovered from the resolution today.
8. B states the weakest part of itself (layer 2, the env overlay; E9) and keeps layer 1 standing alone.
9. Class cannot be derived from `ccsession-models.json` (B cites one `claude` profile at `:5-12`; I did not re-read that range, but I read that `models_env` carries slot names only, as A also says). B keeps class in the tier file and tests the vocabulary instead of merging it, so it needs no new schema key.

## 4. Weaknesses identified in Variant A

1. Strict-by-default has no current beneficiary and real exposure (strength 4). A's text says the spec loop's panel "does not change" (2.2) and also "changes ... from 4 reviewers to as few as 2" (4.2) (X-007). A 5.2 lists no edit or test for the prompt change at `document_review_loop_prompts.md:70`.
2. A's loud shortfall does not fire where strict bites. [OBSERVED-RUNTIME] strict in anthropic-only always resolves 2 reviewers for both `default` and `live7`. A's exit rule is "below `min(2, requested)`" (A 2.3 item 3); with `expected` 4 or 7 the floor is 2, and 2 is not below 2, so the exit code is 0 and only stderr speaks (X-003).
3. Scarcest-first is unmeasured against a real constraint. `resolve` appends reviewers in resolution order (`panel.py:666`), and `SKILL.md:341` defines reflect's persona assignment and the parity check by resolution order ("persona by resolution order: analyzer, qa, refactorer"; `review-panel.reflect-pre.json:5` repeats it) [CODE-VERIFIED]. [OBSERVED-RUNTIME] reflect-pre in anthropic-only under strict, template order: `t1b sonnet, t4 haiku, t1a opus`; scarcest-first: `t1b sonnet, t1a opus, t4 haiku`. That swaps the personas of haiku and opus and can flip `panel_parity`. A says it did not run the strict tests with its order (3.5) and does not mention personas. It also changes soft outputs (my soft/scarce run: gateway repeats 30 of 40 to 0), so the byte-identity golden and `panel-golden-default-live7.json` would move; the order cannot be a silent default.
4. "One file owns the data" is self-contradicted (X-006). A 2.1 keeps "model id behind a slot" in the Coder env, and A's M3 says the single-source claim is wrong if the env moves faster than releases.
5. A's drift fix is weaker than B's (strength 2). A 3.1 item 4 and 5.2 propose counts plus the first model only.
6. `vendors` and the marker-variable key are schema changes: `validate_tiers` rejects unknown environment keys (`panel.py:373` [CODE-VERIFIED]) and any tier-file edit changes `tiers_sha256`, which makes older shadow runs "not proven" in `recompute_parity` (A's own INV-L note, `reflect_shadow_exit.py:128-132` per A and V-6). A counts the golden regeneration but not the validator edit (A-003).
7. "Ember is a data edit" is overstated. Adding `T4Model04` to `ccsession-models.json` also breaks `tests/unit/test_ccsession_tiers.py:222`, which pins tier4 to three slots (I read `:218-232`: it pins `tier4 == [T4Model01..T4Model03]`), and the Coder slot must exist first; A cites only the live7 count test (V-4).

## 5. Concessions

1. X-001: B says the repeat "is not silent under B" and, in section 5 item 2, that the spec profile "resolves soft and records neither key". For the one soft consumer the repeat is silent. The test sentence is wrong as written; the repair is in the hybrid (always write `requested_slots` and `distinct_models`).
2. X-005: B's ember steps omit the edit to `aliases.tier4.models` and the `MODEL-TIERS.md` row. B's own check forces both co-edits (it goes red otherwise), so the ownership claim holds, but the step list was incomplete. `resolve` reads `tiers["aliases"][slot["tier"]]["models"]` (`panel.py:615` [CODE-VERIFIED]), so ember is not picked until that list names it.
3. X-002: B's E4 gateway shrinkage (18 and 30 of 40) is order-dependent and B did not test an order change. A's 0-of-40 reproduces (section 7, X-002 table). B's E4 claim should read "strict shrinks the gateway panel under template order".
4. The overlay (layer 2) is the weakest piece and is not needed for the ownership position; I recommend dropping it from the adjudicated outcome and keeping layer 1 only.
5. The derive-and-compare check parses a markdown table; it is fragile by design ("fails loudly", B section 4) and the parser needs its own mutation test, which B states but does not write.
6. FX-14 (environment detection by `T3Model01` alone, `panel.py:485-494` [CODE-VERIFIED]) is not addressed by B; A's marker-variable idea is a fair attempt, though it needs a schema key.
7. `distinctness: soft|strict` as a template field needs a schema edit (`_PANEL_KEYS`, `panel.py:37, 175`) or a code-side profile table; B did not count it (A-003). The existing `reflect-` prefix check (`panel.py:71, 588`) shows the in-repo way to avoid a schema bump.
8. Requested-id distinctness is not served-id distinctness; B says so (E8), but that cuts against both variants.

## 6. Shared-assumption responses

- A-001 (counts on `run1..run40` carry over): QUALIFY. The run id is hashed into the seed (`panel.py:606-610`), so the draws behave like independent samples; 30/40 has a 95 percent interval of roughly 59 to 87 percent. The direction (gateway shortfall under template order; anthropic-only always 2) is structural, not statistical, and I reproduced both variants' tables. The exact 18 and 30 should not be quoted as rates.
- A-002 (one workspace's env stands for others): QUALIFY. `select_env` returns `anthropic-only` whenever `T3Model01` is unset (`panel.py:492-494`), so laptops and CI are a different environment by code, not by assumption. The one observed env also differs from the repo (6 tier-3 env slots against 2), which supports B's claim that the env needs a filter (`models_env`) rather than a copy.
- A-003 (closed key sets take new keys without a version bump): QUALIFY, close to REJECT for A. B's new output keys need no validator edit; B's `distinctness` input field and A's `vendors` map plus marker key each need one (`panel.py:175, 373`). Neither variant names the edit; A's also changes `tiers_sha256`, which B's layer 1 does not.
- A-004 (a 2-reviewer one-vendor panel is acceptable under `min(2, requested)`): QUALIFY. It is acceptable as a count floor only if the profile says so; it is not a diversity result (Sonnet plus Haiku is one vendor, and reflect's single-vendor degrade, exit 11, treats it so per A 4.1). The floor needs a per-profile declaration; per-profile `distinctness` plus `requested_slots` provides that and a global default does not.
- A-005 (tier order equals failover order): QUALIFY. `MODEL-TIERS.md:38` titles the column "Models in failover order (gateway id)" [CODE-VERIFIED], so within-tier order is documented. Effective failover can still skip a model by window or cooling (B E9(b), shim internals [UNVERIFIED]). A's ladder is acceptable as the documented order; neither variant should claim it equals served order.
- A-006 (optional; requested ids only, extra resolution keys tolerated): ACCEPT with a limit. Only `recompute_parity` is checked as a reader (V-6); other readers (merge, telemetry, manifest) are not checked by either variant or by me.

## 7. Contradictions X-001 to X-007

- X-001 (repeat visible?): A is right about my text for the soft consumer (concession 1). Under strict the keys exist already (`panel.py:700-707`); under soft nothing is written. Repair: write `requested_slots` and `distinct_models` for every profile.
- X-002 (cost of strict in the gateway): both counts are correct; they differ by order. My measurement over 40 runs (cells: runs with a repeated model, then reviewer counts seen):

  | Template, env | soft, template order | soft, scarcest-first | strict, template order | strict, scarcest-first |
  |---|---|---|---|---|
  | default, gateway | 18 repeat, [4] | 0 repeat, [4] | 0 repeat, [3 or 4] | 0 repeat, [4] |
  | live7, gateway | 30 repeat, [7] | 0 repeat, [7] | 0 repeat, [5, 6 or 7] | 0 repeat, [7] |
  | default, anthropic-only | 40 repeat, [4] | 40 repeat, [4] | 0 repeat, [2] | 0 repeat, [2] |
  | live7, anthropic-only | 40 repeat, [7] | 40 repeat, [7] | 0 repeat, [2] | 0 repeat, [2] |

  [OBSERVED-RUNTIME]. Scarcest-first with the soft default removes every gateway repeat with a full panel; strict is needed only for anthropic-only, where it cuts the panel to 2. The order, not the default flip, carries the gateway benefit.
- X-003 (can a loud shortfall fire in anthropic-only?): on substance A's exit does not fire there (strict gives 2, floor is 2). B's phrase "requires a new raise rule that makes the default panel unresolvable" overstates what A proposes (a floor, not a raise at any shortfall). B concedes the wording, not the substance.
- X-004 (ember a "data edit"? slot 02 or 04): A's index 4 matches the live env (diff V-3); B's "open" matches the E2 harness order. B is right that it is not a data edit in this repo alone (Coder slot first, `ccsession-models.json` edit, `test_ccsession_tiers.py:222`).
- X-005 (internal to B): conceded and repaired (concession 2). The full ember edit list is the union of both variants' lists plus the `MODEL-TIERS.md` row.
- X-006 (internal to A): A's "single source" reduces to "one reviewed copy", which is B's snapshot position with a stronger claim attached.
- X-007 (internal to A): see weakness 1; B has no such window.

## 8. Hybrid

1. Ownership (B): Coder env slots, `ccsession-models.json` and `MODEL-TIERS.md` own membership and order; the packaged file is the reviewed snapshot and owns `classes`, `names`, `available`, `stand_ins`, `launch`. Drop B's layer 2 overlay.
2. Check (B, completed): derive-and-compare for the six tiers, with a mutation test for the markdown parser. Ember needs the co-edit of packaged list, `MODEL-TIERS.md`, `ccsession-models.json` and `test_ccsession_tiers.py:222` (the union of both variants' lists).
3. Distinctness (B, with A's declaration idea): library and CLI default stay soft; a profile declares `soft` or `strict` (reflect `strict`, spec loop `soft`). New consumers must declare. Implement through the existing `reflect-` prefix style or a code-side profile table to avoid a template schema bump.
4. Record (B plus A): always write `requested_slots`, `distinct_models` and A's derived `shortfall` for every profile (soft included), print the shortfall on stderr, and leave the exit-nonzero rule to C-03's merge-time floor, since a resolve-time floor does not fire in anthropic-only (X-003).
5. Order (A): scarcest-first as an opt-in resolution order, with the reviewers list re-sorted to template order after picking, so reflect's persona-by-resolution-order and parity stay unchanged. It becomes a default for a profile only after the strict tests and the persona/parity check pass (A's M2).
6. Class and vendor (B): the single test that every `classes` id maps to a non-fallback vendor; no `vendors` map, so no schema key and no `tiers_sha256` change. A's `vendors` map is deferred until the substring table fails that test.
7. Ladder (A): the E2 fallback ladder becomes a function of (tier, model) when the harness is productized; out of scope for the core change.
8. Measurement (A): M1 decides whether any profile's default is ever strict.

## 9. Per-point positions

| Point | Superior approach (A / B / hybrid / neither) | Confidence % | One-line evidence |
|---|---|---|---|
| S-001 | neither | 70 | Both state no disagreement with C-01 to C-03; A's note that it rewrites pins is the more candid. |
| S-002 | B | 60 | B's layer split isolates the overlay as the weakest part; A's table is clearer for today-versus-under-A. |
| S-003 | hybrid | 60 | A's concession 7.4 and M1 are better; B's "pins that must pass unmodified" list is better for test coverage. |
| C-001 | B | 70 | `MODEL-TIERS.md:11-14` plus A's own env disagreement and M3; the package file is a checked snapshot. |
| C-002 | B | 85 | Prototype: swap and replace mutations pass the count check and fail derive-and-compare; green today. |
| C-003 | B | 65 | Both consumers already declare a mode; the flip changes `test_review_cli.py:52-61` and adds a prompt-lag window. |
| C-004 | hybrid | 60 | B's always-written `requested_slots` and `distinct_models` plus A's derived shortfall; A's exit does not fire in anthropic-only. |
| C-005 | hybrid | 55 | Edit lists are incomplete in both (X-005, V-4); the union is the correct step list. |
| C-006 | B | 55 | One vocabulary test, no schema key, no `tiers_sha256` change; FX-14 stays open (concession 6). |
| C-007 | A | 80 | Scarcest-first gives 0 repeats and a full panel in the gateway in 40 of 40 runs, soft or strict; a persona/parity re-sort is a required condition. |
| C-008 | B | 75 | Layer 1 edits no packaged file; A regenerates goldens twice and degrades old shadow-run parity. |
| C-009 | B | 75 | A's own 4.2 admits a 4-to-2 reviewer exposure and a prompt-copy lag; B keeps the loop soft. |
| C-010 | A | 65 | The overlay is B's weakest layer (E9); a package-only resolve is simpler and reproducible. |
| X-001 | hybrid | 65 | A is right on B's soft consumer; always-written keys repair it. |
| X-002 | hybrid | 85 | Both counts reproduce; soft plus scarcest-first removes the gateway repeats without strict. |
| X-003 | neither | 60 | A's floor does not fire at 2 reviewers; B's "unresolvable" overstated A's rule. |
| X-004 | B | 60 | Not a data edit in this repo alone; A's index 4 matches the env, B's "open" matches the E2 order. |
| X-005 | hybrid | 70 | B's ember steps omit the packaged-list and `MODEL-TIERS.md` edits; B's own check forces them. |
| X-006 | B | 65 | A's "single source" reduces to a reviewed copy; its own M3 and env observation say so. |
| X-007 | B | 80 | A states both "does not change" and "changes from 4 to 2"; B has no window. |
| A-001 | qualify | 70 | Hash-seeded draws; interval about 59 to 87 percent for 30 of 40; direction structural. |
| A-002 | qualify | 70 | One workspace; `select_env` makes laptops and CI a different environment by code. |
| A-003 | qualify | 80 | Output keys need no validator edit; `distinctness`, `vendors`, marker key do (`panel.py:175, 373`). |
| A-004 | qualify | 70 | 2 is a count floor, not a diversity result; needs a per-profile declaration. |
| A-005 | qualify | 65 | `MODEL-TIERS.md:38` documents failover order; shim skip behaviour is [UNVERIFIED]. |
| A-006 | accept | 60 | `recompute_parity` reads only `reviewers` and `tiers_sha256`; other readers unchecked. |

## 10. Not verified by me

The E2 branch tip, `COMBO-REPORT.md`, shim internals, `reflect_shadow_exit.py` beyond what V-6 reports, whether a resumed shadow run reuses its stored `panel/resolution.json`, whether the packaged-tier golden regenerates cleanly after a reorder, and `ccsession-models.json:5-12`.

Status: Complete
