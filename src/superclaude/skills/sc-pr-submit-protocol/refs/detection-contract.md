# Detection Contract (DET) — baked Augment identity

This ref holds the **default detection contract** for the Augment Code GitHub App.
Detection is **configuration, not logic**: the three-state classifier
`classify(gh_payload, DetectionContract) → review_state` (FR-2.2) is a pure function that
keys on the data below — it never embeds a literal bot login in classifier code.

Arming does **not** require a local lock file or R1 probe. `DetectionContract.for_arming()`
loads this shipped contract (or an optional gitignored override at
`.dev/pr-monitor/detection-contract.locked.md` when present). A missing/unlocked override
is not a halt.

```yaml
# detection-contract.md — shipped defaults; optional local override may replace these
augment_bot_login: "augmentcode[bot]"                # REST bot-login shape
augment_author_association: ["NONE", "CONTRIBUTOR"]  # observed associations of the Augment author
augment_app_slug: "augmentcode"                      # GraphQL app-slug shape; accepted with bot login
emission_shape: "review"                             # documentary; classifier unused
findings_locus: "comments[]"                         # documentary; classifier unused
severity_field_path: null                            # Augment's self-reported severity, if any (hint only)
review_completeness_signal: "state==COMMENTED"       # documentary
probe_evidence: null                                 # optional provenance; not an arming gate
# V1.1 decline-detection (addendum §6.2 / FR-9.1) — baked defaults; both regexes must match an
# Augment-authored comment for a "declined". accepted_trigger_phrases = our operator re-trigger tokens.
decline_phrase_regex: 'abnormally\s+large'
decline_retrigger_regex: 'comment\s+["''`*_]*(augment|auggie|augmentcode)\s+review["''`*_]*'
accepted_trigger_phrases: ["auggie review", "augment review", "augmentcode review"]
locked: true                                         # vestigial; arming does not check this flag
```

## Consequences

1. **The parser is generic (no literal login).** The classifier builds the non-empty identity
   set `{contract.augment_bot_login, contract.augment_app_slug}`, **never** a literal string.
   This accepts REST bot-login shape (`augmentcode[bot]`) and GraphQL app-slug shape
   (`augmentcode`) when both are present in data. A different bot login is treated as
   "review not detected" (T-211). When Augment and human reviews are interleaved, only the
   Augment author is parsed (T-212). The default retrigger regex also matches the live
   `comment "**_augment review_**"` Markdown wrapper while still requiring the separate
   `abnormally\s+large` phrase.

2. **No lock gate.** Arming loads this shipped contract (or an optional local override).
   `locked: false` / a missing override is not a halt. A local override is a refinement,
   not a requisite. One change point on Augment drift: edit the identity fields here
   (or drop a local override) — **no control-flow code changes** (spec §7 consequence 2).

3. **Optional override.** `.dev/pr-monitor/detection-contract.locked.md` is still preferred
   when present (`for_arming()` / `prefer_local_override=True`) so a fork can pin a
   different bot identity without forking the shipped skill.

4. **Purity seam (AC-9 / NFR-6).** No `gh`/`git` token appears in `state-machine.md`,
   `severity-routing.md`, or `loop-guard.md` — protecting the seam from a future maintainer
   inlining a bot-login string. Tested by **T-N50**.
