# Round 2 rebuttal: Variant A (slot C-09, panel-resolution-and-tier-source)

Status: Complete

Advocate for Variant A (variant-1-original.md). Date: 2026-11-14. Code state: HEAD `50d4d2b9d` on `ironbelly/shadow-runs`; repo read-only; nothing in the worktree was written by me (checked with `git status --short`: only the pre-existing untracked paths). Tags: [CODE-VERIFIED] I read the line this session; [OBSERVED-RUNTIME] I ran a read-only command this session; [UNVERIFIED] not checked by me. Points are cited as S-, C-, X-, A-; new evidence as N1 to N8 (section 3).

How the runtime evidence was produced: a private script and a private pytest plugin under `/tmp/ironclaude-batch.sEEDF6lQ` (removed at the end) import the packaged `superclaude.cli.review.panel` read-only and, for the pin counts, monkeypatch `panel_cmd.pnl` or `panel.resolve` inside the test process to simulate each variant. No repo file was edited. `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, run ids `run1..run1000`, kind `first`. The test set is `tests/review` plus `tests/cli/reflect/test_shadow_skill_contract.py` (661 tests plus 1 skipped; the unmodified-code baseline over that set plus `tests/unit/test_ccsession_tiers.py` was 875 passed, 1 skipped, and every simulation that changes nothing a test pins passes the same 661). One unrelated flake: `test_relative_defaults_path_keeps_each_directory_on_its_own_shim` ("shim failed to start") failed in one sequential run and passed on rerun in the same mode; I do not count it.

## 1. Response to criticisms

Summary of where I stand after reading B's Round 1 and re-running the code: I concede the CLI default flip, the stderr note, the `vendors` map, the marker list, the overlay-versus-"single source" wording and the prompt edit. I keep scarcest-first, now repaired and measured. I add two facts neither Round 1 had: the always-written keys must be written in the CLI layer or 17 pins move, and a stderr line costs 5 pins (N2).

**B-W1. Strict by default has no present beneficiary and real exposure; A 2.2 says "unchanged" and A 4.2 says "4 to 2"; no edit for the prompt (X-007).** CONCEDE, and it is worse than B said. The beneficiary question: reflect passes `--strict-distinct` already (`SKILL.md:340`), and the loop is the only other caller (N4), so the flip helps no consumer that exists. In the gateway, once the order is scarcest-first, soft and strict give the same panels (N1: 1000 of 1000), so even the future consumer gains nothing there; only anthropic-only differs. The cost: 4 pins in template order, 3 with scarcest-first (N2), and a declaration in the loop prompt is 3 edits (prompt, `plugins/` mirror, the `E_FIRST` pin) plus the lag window (N3). I withdraw "the `panel resolve` default is strict" and `--allow-repeat`. A 2.2 and 4.2 are replaced by: the loop is not edited.

**B-W2. The loud shortfall does not fire in anthropic-only.** CONCEDE (already in Round 1). New: the resolve-time exit rule has no case left that the existing fixed-anchor failure (`panel.py:647-649`) does not cover; the floor belongs to merge (C-03). I withdraw "non-zero exit below `min(2, requested)`" from `panel resolve`. A's other surface, the stderr line, is also withdrawn: one stderr line on a soft repeat breaks 5 CLI tests that parse `res.output` (N2, click 8.5.1). The record in the JSON does the same job at no cost.

**B-W3. Scarcest-first is unmeasured against persona order and the byte-identity golden; it cannot be a silent default.** PARTLY CONCEDE, PARTLY REBUT, now with data.
- Persona order: real. Without re-sorting the output to emission order, 5 tests fail (3 reflect-template pins, 2 shadow-contract tests), N2, N5. With the re-sort, the strict path of the library has 0 failures and the six reflect templates keep identical picks in 1000 of 1000 runs (N1). So B's condition ("after the strict tests and the persona/parity check pass") is met in simulation for the strict path. A second requirement B did not name: `template_sha256` must stay the hash of the real template, not of the reordered copy, because the shadow manifest records it (`SKILL.md:340`, `--template-sha256 <template_sha256>`).
- Golden: real for the library soft path (4 parameters of the byte-identity golden move, N2), absent at the CLI layer (0). So scarcest-first must not change the library default order; it may be the CLI's order. The library gets a keyword that defaults to today's order.
- B's other point, that the order cannot be silent: it changes the model a run id gets (742 and 842 of 1000 soft gateway panels, N1), but the re-review anchor is identical in 1000 of 1000 and `resolve` has one production caller whose output is stored as `panel/resolution.json` (N4, and `test_shadow_skill_contract.py:285` calls that file "the raw, unmodified output"). I do not find a consumer that re-resolves a first review.

**B-W4. "One file owns the data" contradicts A 2.1 and A's own M3 (X-006).** CONCEDE (already in Round 1). One further correction in B's favour and one against: N6 shows the unfiltered-env disagreement I cited does not exist once the ccsession slot lists filter the env; so the env is not drifting from the package today, and the case for an env leg in the guard is "it would catch the next drift", not "it caught one".

**B-W5. A's drift guard is weaker (counts and first model).** CONCEDE (Round 1). I adopt B's ordered derive-and-compare as written, with the parser specified in section 6.

**B-W6. `vendors` and the marker list are schema changes (A-003).** CONCEDE and withdrawn (Round 1). With both gone the only packaged-file edit A needs is ember's. FX-14 (detection by `T3Model01` alone) stays open under both positions; I do not claim a fix. Exposure, for the record: `select_env` returns `anthropic-only` wherever `T3Model01` is unset (`panel.py:492-494`), which is the environment where the soft/strict difference is largest (N1).

**B-W7. Ember is not "a data edit"; A omits `test_ccsession_tiers.py:222`.** CONCEDE. I read `test_ccsession_tiers.py:221-222`: tier 3 is pinned to `[T3Model01, T3Model02]` and tier 4 to `T4Model01..T4Model03`; adding `T4Model04` breaks the second. The union edit list is in section 6. "No Python source change" stands; "data edit" is withdrawn as a description.

**B's concessions used as attacks.**
- B conceded the overlay is the weakest layer and should be dropped. AGREE; both Round 1 hybrids drop it.
- B's steelman point that the soft default is pinned (`test_review_panel_exclusion.py:94-99, 208-213`; `test_review_cli.py:52-61`). I said a pin records what is, not what is right. I keep that sentence, but with the cost data the pins are a legitimate reason not to flip a default for no beneficiary; the case for strictness is M1, which nobody has run.
- B's E8 (distinct requested ids, one served model, run A-r3). AGREE that requested-id distinctness is not served-id distinctness; it cuts against both variants and belongs to C-08.
- B's E10 (a strict default makes `ember + 2x luna` unrepresentable). Moot once the default stays soft; under the final hybrid the repeat is representable and recorded.
- B's concession 5 (the markdown parser is fragile). AGREE; the parser spec and its mutation tests are in section 6.

## 2. Updated assessment of Variant B

**What B got right, again, and now confirmed by my own runs.**
1. The ordered derive-and-compare guard (C-002). It is green today for all six tiers (I compared `MODEL-TIERS.md:41-46` with the packaged lists, and N6 shows the slot-filtered env agrees as well), and a swap or a substituted id that a count check cannot see is red under it. It is the single best idea in either proposal.
2. Soft by default, strict by declaration. B's measurement that soft + scarcest-first removes the gateway repeats reproduces on 1000 ids and extends: the soft+scarcest-first and strict+scarcest-first panels are identical in the gateway in 1000 of 1000 runs (N1). That is B's strongest argument and it also dissolves my strongest one ("strict costs nothing in the gateway if the order is fixed": true, but then soft costs nothing either).
3. The pins. A strict default moves 3 to 4 pins and needs 3 prompt-side edits to keep the loop panel (N2, N3). B's default moves none.
4. The class and vendor treatment (C-006): one parity test, no `vendors` map. I verified in Round 1 that `_vendor_from_model_id` classifies all 13 packaged ids and `muse-ember-1.0`.
5. The ember step list contains `test_ccsession_tiers.py:222` (B cites the pin, A did not).
6. B names its weakest layer (the overlay) itself and drops it.

**What is still weak in B.**
1. B's "pins pass unmodified" is correct for B's original text only. B's own Round 1 hybrid (always-written `requested_slots` and `distinct_models`) moves 17 pins if the keys go in the library (N7); at the CLI layer it moves none. B did not say which layer, and the layer decides whether the byte-identity golden, the proof that the soft path is untouched, survives.
2. B's per-profile `distinctness` declaration has no current effect (N4: reflect already passes the flag; the loop is soft) and costs either a closed-key template edit (`panel.py:174-176`, V-5) or a code-side profile table, and at the CLI layer it moves one pin (N2). It is code for a consumer that does not exist yet.
3. B makes scarcest-first "opt-in until M2". The one soft consumer (the loop) is the one that benefits: 345 of 1000 `default` and 693 of 1000 `live7` gateway first-review panels repeat a model, and soft + scarcest-first removes every repeat with no pin moved at the CLI layer (N1, N2). Leaving the default order is leaving a measured defect in place; the objection that picks change per run id (742 and 842 of 1000) is answered by N4 and the re-review anchor identity.
4. B's ownership statement has no mechanism either once the overlay is dropped: both proposals read the packaged file. The guard compares the packaged file with a hand-edited markdown table (`MODEL-TIERS.md:38-46`), so "owner" in B's sense is a second hand-kept copy; the machine link to what the gateway serves is the env, and B's layer 1 has no leg to it. This is a wording point and a small one (section 4(b)).
5. Both Round 1 hybrids (B's item 4, my item 3) print the shortfall on stderr. That is wrong for both of us: a stderr line on a soft repeat breaks 5 CLI tests that parse `res.output` (N2). The JSON record carries the same information at no cost. Under B's original text the denominator `requested_slots` is also written only on request, so the soft loop, the consumer C-03's quorum most needs, would not get it; both hybrids repair that.

## 3. New evidence

All N-items are [OBSERVED-RUNTIME] unless tagged otherwise. "Scarcest first" = the fixed slot first, then the other slots by ascending `len(aliases[tier].models)`, applied to a copy of the template; "emission order" = the order `resolve` emits today, `fixed + rest` in template order (`panel.py:598-605`) [CODE-VERIFIED]. Seeds are `base|slot_id|i` for random slots (`panel.py:620-622`), so the seeds do not move with the order.

### N1. Soft plus scarcest-first against strict, 1000 run ids, all eight packaged templates

| Template, env | Soft, template order: panels with a repeated model | Soft + scarcest-first: repeats, size | Strict, template order: size (runs) | Strict + scarcest-first: size |
|---|---|---|---|---|
| `default`, gateway | 345 of 1000 | 0, 4 in 1000 | 3 (345), 4 (655) | 4 in 1000 |
| `live7`, gateway | 693 of 1000 | 0, 7 in 1000 | 5 (114), 6 (579), 7 (307) | 7 in 1000 |
| `default`, anthropic-only | 1000 | 1000, 4 | 2 in 1000 | 2 |
| `live7`, anthropic-only | 1000 | 1000, 7 | 2 in 1000 | 2 |
| `reflect-lite`, anthropic-only | 1000 | 1000, 3 | 2 in 1000 | 2 |
| `reflect-pre`, `-enterprise`, `-post`, anthropic-only | 0 | 0, 3 | 3 | 3 |
| `reflect-pre-x2`, `-post-x2`, anthropic-only | 0 | 0, 2 | 2 | 2 |
| all six `reflect-*`, gateway | refused by the reflect profile in every mode (`launch` is `None`) | | | |

Further results of the same run:
- In the gateway the soft+scarcest-first panel equals the strict+scarcest-first panel in 1000 of 1000 runs for both `default` and `live7`. Soft + scarcest-first is therefore "strict wherever strict is possible, a repeat only where the model count forces one".
- The `re-review` anchor (fixed slot, resolved first in both orders) is identical under both orders in 1000 of 1000 runs for both templates.
- Scarcest-first changes which models a given run id gets: soft `default` gateway 742 of 1000, soft `live7` gateway 842 of 1000; among the strict panels that were already full in template order, 397 of 655 (`default`) and 149 of 307 (`live7`). For the six reflect templates: 0 of 1000 change.
- What only strict gives, then: (1) in anthropic-only, a panel without repeats (2 reviewers instead of 4 or 7, and `reflect-lite` 2 instead of the pinned `[sonnet, haiku, haiku]`); (2) a guarantee instead of a tendency for any tier file or template that has fewer distinct models than slots; (3) the existing `skipped_slots` and `excluded` record. In the gateway, for the two non-reflect templates, strict adds nothing once the order is scarcest-first.

### N2. Pin cost of each simulated change (661 tests, `tests/review` + shadow contract)

| Simulated change | Failing tests |
|---|---|
| CLI default strict, template order (A as written) | 4: `test_review_cli.py::test_panel_resolve_prints_json`, `::test_panel_resolve_without_the_new_flags_has_no_extra_keys`; `test_review_panel_live7.py::test_cli_resolves_live7_by_name`, `::test_cli_gateway_live7_resolves_seven_reviewers` |
| CLI default strict + scarcest-first + emission-order output | 3 (the same, without the gateway `live7` test) |
| `reflect-` templates strict by default at the CLI (B's per-profile default, code-side) | 1 (`test_panel_resolve_without_the_new_flags_has_no_extra_keys`) |
| Always-written `requested_slots`, `distinct_models`, `distinctness` added in the CLI only | 0 |
| The same keys added in the library `resolve` | 17: 16 parameters of `test_no_exclusion_is_byte_identical_to_golden` (`test_review_panel_exclusion.py:56-72`) and `test_packaged_tiers_hash_and_resolutions_are_pinned` (`test_review_panel_reflect_profile.py:74-88`) |
| Scarcest-first on the strict path of the library, output re-sorted to emission order | 0 |
| The same without the re-sort | 5: three `test_pre_resolves_to_sonnet_haiku_opus_with_three_classes[True-*]`, two in `test_shadow_skill_contract.py` |
| Scarcest-first on the soft path, CLI only, output in emission order | 0 |
| Scarcest-first on the soft path of the library default | 4 (the `gateway|first` parameters of the byte-identity golden) |
| One stderr line when a soft panel contains a repeat (CLI only, click 8.5.1) | 5 (`test_review_cli.py` three tests, `test_review_panel_live7.py` two; they `json.loads(res.output)`, and the click runner interleaves stderr into `output`) |

(A first run of the library-wrapper modes also failed `test_re_review_resolves_only_the_anchor`; that was my wrapper naming the keyword `kind` instead of `review_kind`. I fixed the wrapper and re-ran; the figures above are the re-run.)

### N3. The spec-loop prompt text is pinned and mirrored [CODE-VERIFIED]

`tests/review/test_review_rules_text.py:21` holds `E_FIRST = "Run each review with the reviewers that \`superclaude review panel resolve --run-id <loop id> --kind <first or re-review>\` prints"` and `:31` asserts `TEXT.count(E_FIRST) == 1`. Adding any flag inside that command breaks the pin. The same prompt file exists at `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` (`grep -l` over `src` and `plugins`); whether a parity test covers that mirror I did not check [UNVERIFIED]. So a prompt-side declaration of distinctness is three file edits (prompt, mirror, pin) plus the installed-copy lag, not the one-line edit A's text implied.

### N4. Call sites [CODE-VERIFIED]

`panel resolve` is named in two places under `src`: `document_review_loop_prompts.md:70` (no strictness flag, no `--env`) and `sc-reflect-protocol/SKILL.md:340` (`--env anthropic-only ... --strict-distinct`). The library `resolve` has one production caller, `panel_cmd.py:93` (a grep for `pnl.resolve(` and `panel.resolve(` over `src` and `scripts` finds only it). So the CLI layer and the library layer differ in production by nothing; they differ in which pins see the change (N2). Reflect already declares strictness by passing the flag, so a per-profile "reflect is strict" default changes no behaviour today.

### N5. Reviewer order is pinned in four places [CODE-VERIFIED]

`test_review_reflect_templates.py:88-93` (`[SONNET, HAIKU, OPUS]` for strict and soft) and `:157-161`; `test_review_panel_live7.py:48-60` (the `IDS` order, the `stand_in` list order, `reviewers[2].tier == "tier2b"`); `scripts/reflect_shadow_exit.py:133-153` (`recompute_parity` assigns `PERSONAS[i]` by reviewer index and zips the reviewers with the sorted card headers); the two byte-identity goldens. A scarcest-first pick order that leaks into the emitted list breaks the first, third and fourth (N2, "without the re-sort").

### N6. Env against package, filtered through the ccsession slot lists [OBSERVED-RUNTIME, one Coder workspace]

For each of the six tiers, the env values of the slots `ccsession-models.json` names under `tiers.<t>.models_env` equal the packaged `aliases.<t>.models`, in order. My Round 1 item "the env and the repo disagree" (A 3.1 item 3) compared the unfiltered env (`T3Model01..06`) with the repo; the slot lists are the filter, and through them all six tiers agree today. That correction weakens the X-006 evidence on A's side as well as B's claim that the env needs a filter: the filter exists and works.

### N7. B's "pins pass unmodified" claim, checked

- B's original design (output keys only when a profile or flag asks; no default change): no pin moves. True.
- B's Round 1 hybrid (always-written keys): true only if the keys are written at the CLI layer (0 failures); written in the library they move 17 pins and destroy the byte-identity proof (N2). Neither hybrid statement said where.
- B's per-profile `distinctness` with reflect strict: at the CLI it moves 1 pin; in the library it would move `test_lite_is_sonnet_haiku_haiku_soft_and_sonnet_haiku_strict` (`test_review_reflect_templates.py:127-131`, library call without `strict`, expects `[SONNET, HAIKU, HAIKU]`) [CODE-VERIFIED by reading, not run]. And it changes no behaviour today (N4).

### N8. Ember pool effect [CODE-VERIFIED + reasoning, not run]

`tier4` is a `random` slot in the reflect templates (`test_review_reflect_templates.py:64-68`) and is drawn with `random.Random(seed).choice(pool)` (`panel.py:544-545`); a fourth id changes which id a given seed draws wherever ember is available, that is in the gateway. The packaged-tier golden pins only `anthropic-only` resolutions (`test_review_panel_reflect_profile.py:77-88`, key `{name}|anthropic-only|first`), and the `anthropic-only` `available` list holds Opus, Sonnet, Haiku and Fable but not ember (`review-tiers.default.json:33`), so for that golden ember changes `tiers_sha256` and no picks. One correction to my Round 1: that `available` list names four Anthropic ids, but Fable is in no tier list and no stand-in list (`:5-10`, `:34`), so three Anthropic models are reachable in anthropic-only (Opus, Sonnet, Haiku); the strict result of 2 reviewers for `default` and `live7` there comes from one Sonnet anchor plus one Haiku, which every other slot can only repeat.

## 4. Remaining disagreements

After both Round 1 statements and my runs, one point is still genuinely contested (c), one is contested only if B insists on a placement (d), one is a build-now-or-not question (a2), and the rest I AGREE on. I state each with my final argument.

| Point | State | One line |
|---|---|---|
| (a) strict vs soft as the `panel resolve` default | AGREE with B: the CLI and library default stay soft; no `--allow-repeat`; no flip | 3 to 4 pins and 3 prompt-side edits for no present beneficiary (N2, N3, N4) |
| (a2) build a per-profile `distinctness` declaration now | CONTESTED, small | I say build nothing now; B's hybrid item 3 builds it |
| (b) ownership wording | AGREE on a merged wording; the env leg is deferred, not a test | see below |
| (c) scarcest-first as a default order vs opt-in | STILL CONTESTED | I say CLI default, library keyword defaulting to today's order |
| (d) who writes `requested_slots`, and the exit rule | AGREE on names, always-written, no exit rule, no stderr; CONTESTED only if the library is the writer | CLI-layer writer: 0 pins; library writer: 17 pins (N2) |
| (e) INV-L and golden churn | AGREE | one accounting sentence, below |
| (f) spec loop declaration | AGREE with B: the loop prompt is not edited | pin + mirror + lag (N3) |

**(a) AGREE.** I argued that soft is silent duplication. The record (always-written `distinct_models`, section 6) removes the silence at no pin cost, and the only place strictness changes the outcome is anthropic-only, where it turns a 4-reviewer panel `[sonnet, haiku, haiku, haiku]` into 2 reviewers (N1). Whether that trade is right is M1's question, which nobody has run; a default should not be flipped on an unrun measurement.

**(a2) CONTESTED, small.** B's hybrid item 3 has "a profile declares `soft` or `strict` (reflect `strict`, spec loop `soft`)", through the `reflect-` prefix or a code-side table. My final argument: reflect already declares strictness at its call site (`SKILL.md:340` passes `--strict-distinct`), the loop is soft by being left alone, and the declaration moves one pin at the CLI layer (N2) or a library pin in `test_review_reflect_templates.py:127-131` at the library layer, while changing no behaviour (N4). A future consumer states its choice the same way reflect does: by passing the flag. When a second strict consumer appears and repeats the flag, a profile field becomes worth its schema edit (`_PANEL_KEYS`, `panel.py:174-176`). B's counter, that new consumers "must declare", is met by the flag and by the always-written record, which shows a reader what happened. Confidence that nothing should be built now: 70%.

**(b) AGREE on wording; env leg deferred.** Merged text: "Which models a tier holds, and in what order, is decided in the Coder env slots that `ccsession-models.json` names and that `MODEL-TIERS.md` describes. The packaged `review-tiers.default.json` is the reviewed copy `panel resolve` reads, held in step with those by the guard; it alone holds `classes`, `names`, `available`, `stand_ins` and `launch`." That is B's ownership with my "the one input of `panel resolve`". My remaining preference: say "reviewed copy, checked by test" and not "snapshot", because "snapshot" suggests an automatic refresh and there is none; the guard is the only mechanism. The env leg: N6 shows the filtered env equals the package today, so a conditional env comparison would be green now. I do not want it as a pytest: the documented order is Coder env first, then the repo (`MODEL-TIERS.md:189-193`; ccsession stops on a listed slot the env lacks, `models.py:666-669`), so an env-equality test would turn every Coder workspace red between the Coder release and the repo merge. If drift is ever observed (M3), a read-only `panel check` that prints a difference and never alters a resolution is the form; not built now.

**(c) STILL CONTESTED.** B: scarcest-first stays opt-in until the strict tests and the persona/parity check pass. Me: the CLI orders non-fixed slots scarcest first by default, for soft and for strict; `resolve` gets a keyword (default today's order) so the library and the byte-identity goldens are untouched; output is always emitted in emission order (`panel.py:598-605`); `template_sha256` stays the hash of the real template. Final arguments:
1. B's own condition is met in simulation: the strict path in the library with the re-sort has 0 failing tests and identical reflect picks (N1, N2); the soft path at the CLI layer has 0 failing tests (N2). The two things that do fail are the ones I now exclude: the library soft default (4 golden parameters) and a missing re-sort (5 tests).
2. The benefit goes to the one consumer that is soft: the loop, in the gateway, which is where Coder workspaces resolve (`select_env`, `panel.py:492-493`; `T3Model01` is set here). 34.5% of `default` and 69.3% of `live7` first-review panels carry a repeated model today; soft + scarcest-first carries none, with the same panel size (N1). Opt-in leaves a measured defect where the benefit is.
3. B's counter: the model a given run id gets changes (742 and 842 of 1000 soft gateway panels). Answers: the re-review anchor is identical in 1000 of 1000 runs, `resolve` has one production caller and its output is stored as `resolution.json` (N4), and I found no code that re-resolves a first review. What I did not check: any external tooling outside this repo that re-resolves by run id [UNVERIFIED].
4. Limit I state, not hide: ascending model count is a heuristic. It is exact for the eight packaged templates (N1) and can fail for a custom template whose scarce tier is asked for more slots than it has models; the upgrade is the most-constrained-first ratio (models divided by slots demanded). `shortcut: ascending model count, upgrade when a custom template is skipped under it.`
Confidence that CLI-default is the right call: 65%; 35% for B's opt-in.

**(d) AGREE, with one conditional dispute.** Names: `requested_slots` (B's; it matches C-02 and C-03's `requested`), `distinct_models`. Always written. Dropped from A: `expected`, `shortfall` (derivable as `requested_slots - len(reviewers)`), the stderr line (5 pins, N2), the resolve-time exit rule (never fires where it matters; B-W2). Dropped `distinctness`: `skipped_slots` and `excluded` are written whenever an exclusion mode is on (`hard_exclude or strict_distinct`, `panel.py:700-706`), so their presence already says so. Written where: the CLI. That is the only placement with zero pin moves; the library placement moves 17 pins and removes the byte-identity proof (N2). If B wants the library as the writer, that is the dispute, and my argument is the 17. B's reason for the library placement would be a non-CLI caller; there is none in `src` or `scripts` (N4).

**(e) AGREE.** One accounting sentence for both: "INV-L holds until the first edit of the packaged file; any such edit (ember or any tier change) changes `tiers_sha256`, after which `recompute_parity` reports an earlier run as not proven (`reflect_shadow_exit.py:128-132`), by design of that script; CLI-layer keys change neither `tiers_sha256` nor `template_sha256`." Goldens: `panel-golden-packaged-tiers.json` is regenerated once, for ember; the frozen-copy golden is untouched.

**(f) AGREE.** The prompt line is pinned exactly and mirrored (N3). With scarcest-first at the CLI the loop's gateway panel gains distinctness without an edit, and its anthropic-only panel stays 4 reviewers with the repeat visible in the record.

**Two smaller agreements from the hybrids, restated.** Emission order, not raw template order, is the output order (the fixed slot is moved first today, `panel.py:598-605`); and the E2 ladder as a function of (tier, model) is deferred (it concerns the harness, not `panel resolve`).

## 5. Revised per-point table

Where my position moved since Round 1, the evidence column says "Round 1: ...".

| Point | Superior approach (A / B / hybrid / neither) | Confidence % | One-line evidence |
|---|---|---|---|
| S-001 placement of consistency with C-01..C-03 | neither | 65 | Both say no disagreement; A names the pins it rewrites, but A's rewrite list (1 test) was short: the flip moves 4 (N2). |
| S-002 shape of the ownership statement | hybrid | 65 | A's today-versus-proposed table plus B's layer split with the overlay dropped; both Round 1 hybrids agree. |
| S-003 closing structure | hybrid | 60 | A's M1 to M3 and wrongness conditions, B's "pins that must not move" list, now backed by N2. |
| C-001 owner of membership and order | hybrid (B's wording, A's "the input `panel resolve` reads") | 75 | `panel.py:615` reads the packaged list; env decides serving; N6: filtered env equals package today. (Round 1: hybrid 70.) |
| C-002 drift guard | B | 90 | Ordered compare vs `MODEL-TIERS.md:38-46` is green today and red on a swap; count check is blind to it. (Round 1: B 80.) |
| C-003 default distinctness | B | 80 | Flip = 4 pins (3 with scarcest-first) + 3 prompt-side edits, no beneficiary; gateway soft+scarce == strict+scarce 1000/1000 (N1-N4). Round 1: A 60, reversed. |
| C-004 shortfall record and failure | hybrid | 75 | `requested_slots` + `distinct_models`, always, written by the CLI (0 pins; library 17); no exit rule, no stderr (5 pins) (N2). |
| C-005 how ember enters | hybrid (union list) | 75 | Both lists incomplete (`test_ccsession_tiers.py:222`; packaged list and `MODEL-TIERS.md` row); env has `T4Model04`; slot order open (GQ-046). |
| C-006 class, vendor, env detection | B | 80 | All 13 ids and ember already map; one parity test; no `vendors` map, no marker list. FX-14 stays open under both. |
| C-007 slot resolution order | A, repaired | 70 | Scarcest-first: gateway repeats 0 and full panels in 1000 of 1000; needs emission-order output (5 pins without it) and the original `template_sha256`; library default order kept (4 golden params otherwise). |
| C-008 pins, goldens, hash parity | hybrid | 70 | B moves fewer pins; A's INV-L accounting is the accurate one (any packaged edit changes `tiers_sha256`); both folded into one sentence. |
| C-009 spec loop exposure (INV-C, INV-D) | B | 85 | The loop is not edited; its prompt is pinned and mirrored (N3). Round 1: B for risk, A for outcome, 55. |
| C-010 runtime link to the env (overlay) | A (no overlay) | 85 | B dropped it; the overlay would make `tiers_sha256` per-workspace and `recompute_parity` reports that as not proven. |
| X-001 repeat visible under soft | hybrid | 80 | Always-written `distinct_models`, at the CLI layer (N2); soft resolution has no record today (`panel.py:700-706`). |
| X-002 cost of strict in the gateway | hybrid | 90 | Order, not default, carries the gateway benefit; soft+scarce == strict+scarce in 1000 of 1000 (N1). |
| X-003 can a loud shortfall fire in anthropic-only | neither | 75 | Strict gives 2 there in 1000 of 1000; the resolve-time floor never fires; B's "unresolvable" was wrong. |
| X-004 ember "data edit" and position | hybrid | 70 | Env `T4Model04=muse-ember-1.0` supports index 4; not a one-file edit; slot order is an owner question. |
| X-005 B internal: snapshot vs ember becoming resolvable | A | 75 | `panel.py:615`; B conceded the omitted edits. |
| X-006 A internal: single source vs env as owner | B | 80 | A conceded; N6 corrects the "env disagrees" evidence; wording merged in (b). |
| X-007 A internal: does the loop panel change | B | 90 | A conceded; the loop stays unedited and soft (N3). |
| A-001 40-id counts carry over | neither (qualify) | 85 | 1000 ids: 345 and 693 per 1000 (not 18 and 30 of 40); direction unchanged. |
| A-002 one workspace's env stands for others | neither (qualify) | 75 | One env read; `select_env` returns anthropic-only when `T3Model01` is unset; N6 is also one workspace. |
| A-003 closed key sets take new keys safely | neither (qualify) | 85 | CLI-layer output keys need no validator edit; template and env-entry keys do (`panel.py:174-176`, `371-373`), and no remaining proposal adds one. |
| A-004 a 2-reviewer strict panel is acceptable | neither (qualify) | 75 | A count, not diversity (one Sonnet, one Haiku); the per-consumer minimum is C-03, C-10, C-11's to set. |
| A-005 tier order is failover order | neither (qualify) | 65 | `MODEL-TIERS.md:38` says failover order; shim skipping unchecked by me. |
| A-006 requested ids only; extra keys tolerated | neither (accept) | 80 | `recompute_parity` reads `reviewers` and `tiers_sha256` only (`reflect_shadow_exit.py:125-137`); the shadow contract test passes with CLI-layer keys (N2, 0 failures). |

## 6. Final hybrid

The hybrid changed from my Round 1 section 9 in six places: no strict CLI default and no `--allow-repeat`; no loop-prompt edit; scarcest-first is the CLI's order (library keyword); the keys are written by the CLI, named `requested_slots` and `distinct_models`, with no `shortfall`, `distinctness`, stderr line or resolve-time exit rule; the guard's parser and mutation tests are specified; no per-profile mechanism now. Exact contents:

1. **Ownership (wording).** "Which models a tier holds, and in what order, is decided in the Coder env slots that `ccsession-models.json` names and that `MODEL-TIERS.md` describes. The packaged `review-tiers.default.json` is the reviewed copy `panel resolve` reads, held in step with those by the guard in item 2; it alone holds `classes`, `names`, `available`, `stand_ins` and `launch`." No env overlay. No `vendors` map. No env marker list.
2. **Guard (replaces `_assert_tiers_match_ccsession_slots`, `test_review_panel_live7.py:92-98`).** One test. For tier1a, tier1b, tier2, tier2b, tier3, tier4 (tier0 is not packaged and is skipped): the ordered ids of `aliases.<tier>.models` equal the backticked ids of the third column ("Models in failover order (gateway id)") of the matching row of the section 1 table of `MODEL-TIERS.md` (`:38-46`), and their count equals `len(models_env)` of the matching `ccsession-models.json` tier. Parser rules: find the section 1 table by its header cell; map a row label such as `**Tier 1a**` to `tier1a`; read only column 3; a missing header, a missing row or an empty cell raises. Mutation tests: swap two ids, substitute an id, drop a row, rename the column header; each must fail. Keep the existing mutation case (`test_review_panel_live7.py:101-106`) and the ccsession slot pins (`test_ccsession_tiers.py:221-222`). The env is not a leg of any test (item 9).
3. **Distinctness.** Default soft in the library and the CLI, unchanged. `--strict-distinct` stays the opt-in flag, as `SKILL.md:340` uses it. No `--allow-repeat`. No profile field or table; a consumer that wants strictness passes the flag.
4. **Order.** `panel.resolve` gains a keyword `scarcest_first` (default `False`, today's order, so the library and the byte-identity goldens do not change). The CLI passes `True` for soft and strict. With it: the fixed slot first, then the other slots by ascending `len(aliases[tier].models)` (stable); `reviewers` is emitted in emission order (`fixed + rest` in template order, `panel.py:598-605`) so `reflect-*` personas and card parity do not move; `template_sha256` stays the hash of the real template. Tests: `reflect-pre` strict and with `--hard-exclude-class` keep today's order and picks; `template_sha256` equals `sha256_json` of the unmodified template; `default` and `live7` in the gateway contain no repeated model over `run1..run200` and keep size 4 and 7; the `re-review` anchor is identical with and without the keyword; the library default is byte-identical to the existing golden. `shortcut: ascending model count; upgrade to models-per-demanded-slot when a custom template is skipped under it.`
5. **Record.** The CLI adds to every resolution `requested_slots` (the reviewer count the template asks for this review kind, by the expand rule of `panel.py:600-605`: a re-review expects 1) and `distinct_models` (count of distinct `model` values among `reviewers`). The library's output is unchanged. No stderr line, no `shortfall`, no `distinctness`, no resolve-time exit rule beyond the existing fixed-anchor exhaustion (`panel.py:647-649`). Tests: the CLI output carries both keys for every packaged template and kind; the library output carries neither (the 16 byte-identity parameters and the packaged-tier golden stay as they are). `requested_slots` is the source of `requested` that C-02 INV-001 and C-03 INV-007 may read; what merge does with it stays C-03's.
6. **Spec loop.** Not edited: `document_review_loop_prompts.md:70`, its `plugins/` mirror and the `E_FIRST` pin (`test_review_rules_text.py:21`) stay as they are. The loop gains distinct gateway panels from item 4 and a visible record from item 5.
7. **Class and vendor.** One test: every id in `classes` maps to a non-fallback vendor in `_vendor_from_model_id` (`reflect/_diversity.py:39-61`), and the class set in `SKILL.md` is a subset of the `classes` values plus a declared extras list (`kimi`, `deepseek`; the `SKILL.md:1248` line I did not re-read [UNVERIFIED]). No vocabulary merge now. FX-14 (environment detection by `T3Model01` alone) stays open.
8. **Ember.** In this order: the Coder `defaults.sh` slot (outside this repo); in this repo, `ccsession-models.json` `T4Model04`; `aliases.tier4.models` at the index the Coder env gives; `names` and `classes` entries; the `MODEL-TIERS.md` tier 4 row (the guard needs it); `test_ccsession_tiers.py:222` and `test_review_panel_live7.py:94-96` updated; `panel-golden-packaged-tiers.json` regenerated once. No Python source change. Slot index 02 against 04 is the owner's (GQ-046); the env today has `T4Model04=muse-ember-1.0`, the E2 harness has it at 02. Accounting sentence: "INV-L holds until the first edit of the packaged file; any such edit changes `tiers_sha256`, after which `recompute_parity` reports an earlier run as not proven (`reflect_shadow_exit.py:128-132`), by design of that script; the CLI-layer keys change neither `tiers_sha256` nor `template_sha256`."
9. **Deferred, not decided here.** The env leg of the guard (a read-only `panel check`, only if M3 shows drift; not a test, because the documented order is env first, `MODEL-TIERS.md:189-193`); the E2 ladder as a function of (tier, model); the strictness default as a measured question (M1: soft, strict and declared-repeat panels at equal reviewer count on ground-truth packages); the minimum acceptable panel per consumer (A-004; C-03, C-10, C-11); the profile declaration (when a second strict consumer exists); any tooling outside this repo that re-resolves a first review by run id [UNVERIFIED].

What I did not verify: the shim's failover behaviour (A-005); whether the wheel carries `ccsession-models.json`; whether a parity test covers the `plugins/` mirror of the loop prompt; the `SKILL.md:1248` class set; the E2 and COMBO-REPORT evidence for repeated panels; any workspace other than this one (N6, `T3Model01`).

Status: Complete
