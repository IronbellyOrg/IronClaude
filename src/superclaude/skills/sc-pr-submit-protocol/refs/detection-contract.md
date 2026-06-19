# Detection Contract (DET) — the build-gated locked constant

This ref holds the **probe-locked detection contract** for the Augment Code GitHub App.
Detection is **configuration, not logic**: the three-state classifier
`classify(gh_payload, DetectionContract) → review_state` (FR-2.2) is a pure function that
keys on the data below — it never embeds a literal bot login. Every `<PROBE-LOCKED>` /
`<placeholder>` value is filled by the **R1 empirical probe** (operator runbook:
`phase-outputs/plans/r1-detection-probe-runbook.md`) and **never hard-guessed** (spec §7).

The build BLOCKS arming while `locked: false`. The pre-flight asserts `contract.locked == true`
and refuses to arm against an unlocked contract — **T-210** mechanically enforces this gate
("contract `locked:false`/absent ⇒ HALT 'probe first'").

```yaml
# detection-contract.md — locked by R1 empirical probe (build BLOCKS while locked:false)
augment_bot_login: "<PROBE-LOCKED>"                  # e.g. "augmentcode[bot]" — NOT hard-guessed; lives in data
augment_author_association: ["NONE", "CONTRIBUTOR"]  # observed associations of the Augment author
augment_app_slug: "augmentcode"                      # GitHub App slug (confirm via probe); accepted with bot login
emission_shape: "<review|issue_comment|check_run>"   # which gh surface carries findings
findings_locus: "<reviews[].body|comments[]|check_run.output>"  # JSON path to the findings
severity_field_path: "<jsonpath-or-null>"            # Augment's self-reported severity, if any (hint only)
review_completeness_signal: "<state==COMMENTED|presence-of-summary-marker>"  # "review finished" marker
probe_evidence: "<abs-path to captured gh json>"     # provenance for the lock (real captured JSON)
# V1.1 decline-detection (addendum §6.2 / FR-9.1) — baked defaults; both regexes must match an
# Augment-authored comment for a "declined". accepted_trigger_phrases = our operator re-trigger tokens.
decline_phrase_regex: 'abnormally\s+large'
decline_retrigger_regex: 'comment\s+["''`*_]*(augment|auggie|augmentcode)\s+review["''`*_]*'
accepted_trigger_phrases: ["auggie review", "augment review", "augmentcode review"]
locked: false                                        # R1 flips this to true; build BLOCKS while false
```

## Consequences

1. **The parser is generic (no literal login).** The classifier builds the non-empty identity
   set `{contract.augment_bot_login, contract.augment_app_slug}`, **never** a literal string.
   This accepts REST bot-login shape (`augmentcode[bot]`) and GraphQL app-slug shape
   (`augmentcode`) when both are probe-locked in data. A different bot login is treated as
   "review not detected" (T-211). When Augment and human reviews are interleaved, only the
   Augment author is parsed (T-212). The default retrigger regex also matches the live
   `comment "**_augment review_**"` Markdown wrapper while still requiring the separate
   `abnormally\s+large` phrase.

2. **The R1 lock gate.** The pre-flight asserts `contract.locked == true` and refuses to arm an
   unlocked contract — turning R1 from a "should" into a mechanically-enforced sequencing
   dependency. **T-210** ("contract `locked:false`/absent → HALT 'probe first'") is the
   regression test that proves the gate; it is preserved and strengthened to a `locked == true`
   assertion. This contract ships with `locked: false`: the operator must run the R1 probe and
   flip `locked: true` with a real `probe_evidence` path before the skill can arm.

3. **Mechanically-enforced build sequencing (§3 step 0).** Because arming is build-gated on
   `locked == true`, the detection contract is the DAG root: all downstream pure work (FSM,
   severity router, loop-guard, run-log, recovery, reply) proceeds on synthetic fixtures
   (§18.4), but no *live* arming/poll can occur until the probe completes. One change point on
   Augment drift: if Augment moves from review-comments to check-runs, `emission_shape` flips
   and `findings_locus` re-points — **no control-flow code changes** (spec §7 consequence 2).

4. **Purity seam (AC-9 / NFR-6).** No `gh`/`git` token appears in `state-machine.md`,
   `severity-routing.md`, or `loop-guard.md` — protecting the seam from a future maintainer
   inlining a bot-login string. Tested by **T-N50**.
