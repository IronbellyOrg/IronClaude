# Diff Analysis: position-paper Comparison (QG3: authority and config, OD-6, OD-10, OD-11, OD-12)

## Metadata
- Generated: 2026-11-20T09:06:00Z
- Variants compared: 2 (Variant 1 = OURS, Variant 2 = CLAY)
- Total differences found: 22
- Categories: structural (3), content (8), contradictions (4), unique (7), shared assumptions (6; UNSTATED promoted: 2)
- Taxonomy tags (AD-5): L1 surface, L2 structural, L3 state-mechanics. Each point carries one tag.

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Section skeleton | Terms, Claim, Mechanism, Cited facts (9), Costs, Risks, Gets right | Same skeleton, 8 cited facts (L1) | Low |
| S-002 | Sub-question framing | Claim lines state the answer to adopt (Yes, per-PR go, empty, both layers) | Claim lines state the alternative answer (No, standing close, standing entries, verb guard) (L2) | Low |
| S-003 | Source of facts | Cites master design, pr-a parser, closeout skill, workflows search, contract line 241, verdicts | Cites master design, pr-a parser, closeout skill; no contract or verdict cites (L2) | Medium |

## Content Differences

| # | Topic | Variant 1 (OURS) Approach | Variant 2 (CLAY) Approach | Severity |
|---|-------|---------------------------|---------------------------|----------|
| C-001 | OD-6 release (L3 guard) | Unconditional refusal of tag and publish; no `--answer-ref` pass path; reason: irreversible and `answer-check` cannot tell a person from a script (D:676, D:694, U57) | N6 passes with the `--answer-ref` of a passed `answer-check`; row 5 already sends release to the person first (D:751, D:763) | High |
| C-002 | OD-10 post-merge close (L3 guard) | One per-PR go bound to head sha names merge and close; no standing `issue.close` | Standing `issue.close` in `grants` because merge and close are off the human-only list (R10, ruling 13, D:82, D:682, D:799 (f)) | High |
| C-003 | OD-11 default grants (L3 state) | Empty list; owner says once in chat which of three standing entries to grant; agent records | Standing entries listed at install (six in the example, D:291) so the plan call works at once (D:116) | High |
| C-004 | OD-12 config protection (L3 guard, invariant) | Both: file outside coordinator's write reach or hook, and fail closed on weakening values | Guard by the `repos` verb refusing three keys without `--answer-ref`, plus a test (D:688) | High |
| C-005 | Mechanical bind on close | `E-NO-GRANT` does not see `settle.sh`, so a standing close is a permission, not a control (inference from D:696 and SKILL.md:51) | Closeout's writes "fall under" grants `issue.close` and `issue.comment` (D:799 (f)); grants are the authorization record | Medium |
| C-006 | Reversibility of close | Not argued as a benefit; close is tied to the merge go | A closed issue can be reopened; closeout never closes an issue a person reopened (SKILL.md:114) (L2) | Medium |
| C-007 | Zero-setup | Costs one chat message on a new host; refusal must explain itself | "Works at once" fits the owner's zero-setup aim; unless the one message counts as setup | Medium |
| C-008 | Parser fail-closed evidence | `grants` missing reads empty (repos.py:295-299) but `merge_safety_files: []`, `reviewers: none`, bad `reach_daily_max` read as weakening values are accepted | Same parser validates strictly: reviewers list, null merge_safety_files invalid, max_in_flight 1 to 10 (L3 validation rule) | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Is "no hook" a gap or irrelevant | OURS fact 8: no hook in master mentions the poll config; recommends "out of reach or hook" | CLAY: guard is "the verb and a test" and the gap is named (D:688) | Medium |
| X-002 | Does the grant list bind closeout | OURS: `E-NO-GRANT` covers verbs only, so a standing close is not a control | CLAY: closeout writes fall under grants (D:799 (f)); D:696 itself limits `E-NO-GRANT` to the verbs | Medium |
| X-003 | Intra-variant (OURS): layer 1 vs risk | OURS recommends the config "outside the coordinator's write reach (or behind a hook)" yet lists that a hook cannot see a Bash-written file (D:769, U42) | n/a | Medium |
| X-004 | Intra-variant (CLAY): release is person-gated vs coordinator may tag | CLAY fact 2: row 5 sends release to the person | CLAY fact 1: N6 lets the coordinator tag with a recorded OK; the recorded OK is the unproved U57 | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | OURS | A search of `.github/workflows` found no workflow that tags or publishes (a release is a person's act today) | Medium |
| U-002 | OURS | Parser accepts weakening values (`merge_safety_files: []`, `reviewers: "none"`, bad `reach_daily_max` read as 0) with line citations | High |
| U-003 | OURS | Clay's own register U57 admits the "recorded OK" for a release is unproved | High |
| U-004 | OURS | Contract line 241 requires an instruction naming the action; a standing merge or close contradicts it | Medium |
| U-005 | CLAY | Close is reversible; closeout refuses to close an issue a person reopened (SKILL.md:114) | Medium |
| U-006 | CLAY | Per-repo `release_merge_method` shows the design already treats release PRs as a special case (#658 reverted by #662, D:118) | Low |
| U-007 | CLAY | Zero-setup alignment with the owner's "nothing manual" aim | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|-------|-----------|------------------|----------------|----------|
| A-001 | The verbs `repos`, `answer-check`, `E-NO-GRANT`, `merge-gate` exist and work as the design text says; neither paper says they are unbuilt (D15 records they exist in no snapshot) | Both rely on `answer-check` and the `repos` verbs | UNSTATED | Yes (L3) |
| A-002 | The per-repo config sits in a file the coordinator's shell can write (same OS user); neither says what file permissions or ownership apply | Both discuss tamper protection | UNSTATED | Yes (L3) |
| A-003 | One GitHub login is shared by the owner and every session (U57; owner-answers line 162) | Both cite it | STATED | No |
| A-004 | Owner identity is a parameter, not Clay (D:694 hardwires Clay) | OURS states; CLAY silent | STATED (OURS) | No |
| A-005 | Merging a release PR is allowed and distinct from tagging (D:763) | Both | STATED | No |
| A-006 | A chat go, once recorded, persists across a coordinator restart between merge and closeout | Both implicit | STATED in OURS cost (restart must read the record) | No |

### Promoted [SHARED-ASSUMPTION] points

| A-NNN | Assumption | Impact | Status |
|-------|-----------|--------|--------|
| A-001 | Controls named in both papers are design text, not built code | High: every "control" answer rests on a future build | Open for debate |
| A-002 | The config file is writable by the coordinator's own shell | High: decides whether OD-12 layer 1 is achievable | Open for debate |

## Summary
- Total structural differences: 3
- Total content differences: 8
- Total contradictions: 4
- Total unique contributions: 7
- Total shared assumptions surfaced: 6 (UNSTATED: 2, STATED: 4, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, C-004, X-004, U-002, U-003, A-001, A-002
- Debate diff points (denominator): S 3 + C 8 + X 4 + A 2 promoted = 17
