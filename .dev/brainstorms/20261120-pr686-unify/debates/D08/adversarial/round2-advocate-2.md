# D08 Round 2: Advocate 2 (CLAY)

Read-only except this file. No GitHub or Orca writes. "A1" = round2-advocate-1.md in this folder. pr-a = /home/coder/.cache/ic-snap-20261120/pr-a.

## Response to criticisms

Steelman of A1's best point: every persisted name is free to change until PR 686 merges, and A1 has now listed all of them (A1 evidence 4), so a full rename is bounded, and the owner's R9, R10 and R17 (ZS-REQ lines 40, 41, 43) decide the word. I agree with that. A1 also fixed the errors I pointed at in Round 1: the missing nesting table, the pinned test cost, the invented `coord-<short>-<n>` tag, and "attended/standing". I checked A1's new claims and found no error: `launch.py:39` TAG_PATTERN allows `COORD-IronClaude`; the `superclaude orchestrator` verbs are not in pr-a; the wake and tier names are the ones I listed.

## Updated assessment

I withdraw the command word and the role noun. CLAY's remaining value (flags, "standing-grant coordinator", "orchestrated issue flow", unchanged report-session names, the nesting table, deciding before merge) is already in A1's final table. I see no CLAY capability that OURS-with-hybrid lacks.

## New evidence

1. pr-a `launch.py:33-35` pins the typed line `/sc:orchestrator --wake <id>` in a regex, and `launch.py:39` marks the tag pattern "[UNVERIFIED, U25] that this is the pattern ccsession applies". So `COORD-<RepoName>` as a ccsession tag is unverified against ccsession itself, not only against Coder 516.
2. pr-a `repos.py:129` derives `<short>` as lowercase letters and digits, at most 12 characters (`re.sub(r"[^a-z0-9]", "", name.lower())[:12]`). The owner's `COORD-<RepoName>` keeps case and punctuation. If the tag must equal the owner's session name, the build needs a second derivation, or the tag is `COORD-<short>[-<n>]` and the owner's name is only the Orca terminal name. This is a build detail, not a naming defect.
3. `route.py:405` and `:494` compare repos case-insensitively, but `tag_of` (route.py:92-94) builds the tag from `<prefix>-<short>-<n>` with no case rule for the prefix. With prefix `COORD`, tag lookups stay exact-match. No defect found.

## Remaining disputes

Points (a) to (e) from debate-D08:

- (a) Rename wake schemas, mailbox kind, `orchestrator_tier`, `orchestrators.json`, `.orchestrator/` and the design-only verbs before merge: AGREE. I see no CLAY benefit lost. The names are in pr-a only; master carries none (A1 evidence 4). One caution: issue 655's body and its comments say `orchestrator_tier` and cannot be edited by this debate, so GitHub text will disagree with code until the owner edits it. That is a cost to list, not a reason to keep any pr-a name. I would keep nothing from pr-a under "orchestrator" except the proper names below.
- (b) "all-sessions coordinator" instead of "host coordinator": AGREE. Issue 339's title says "ALL sessions" and nothing says "host". My word "host" was an addition.
- (c) Plain `/sc:coordinator` = person-opened mode, no grants; grants only through `--wake`, `--hourly`, `--resume`, `--take`: AGREE. It is the safe default and keeps the pinned phrase "coordinator is person-opened" true. I add one build requirement: a test that a flag-less call writes no grant and starts no merge.
- (d) The allowlist for the word "orchestrator": AGREE with A1's point (7) (a) to (e). Add one clarification: the existing sentence at `core/CLAUDE.md:58` may keep the word only with a glossary definition (TR line 2038, C9, says it has none today).
- (e) Remaining capability or verified defect in the all-coordinator scheme: NONE that I can show. The two real risks are not defects of the scheme: the tag derivation (new evidence 2) and the unverified tag pattern (new evidence 1). Both are build tasks.

A1's decisions:

1. Session name and tag one string (`COORD-<RepoName>`, `-<n>` extras): AGREE in principle, QUALIFY on form. Settle in the build whether the tag is `COORD-<RepoName>` or `COORD-<short>`; both pass `launch.py:39`; check against ccsession first (U25).
2. Rename everything session-named, keep `IronOrchestrator` and `orchestrator_repo`: AGREE.
3. Report coordinator, tag `coordinator` unchanged: AGREE. I accept A1's finding that no clash exists on Linux.
4. Species terms "person-opened coordinator", "standing-grant coordinator": AGREE.
5. "All-sessions coordinator"; "orchestrated issue flow": AGREE.
6. Plain command = no grants; one door for grants: AGREE. A1's open item, R17's launch-prompt route, should become `--wake` or `--take`; that is for D07.
7. Allowlist and pinned test: AGREE. Feasibility untested.

Final table: AGREE, with the two qualifiers above (tag form, test for flag-less call).

## Final proposed naming scheme

| Row | Difference from A1 |
|---|---|
| Session name and ccsession tag | Tag form `COORD-<RepoName>` versus `COORD-<short>` is left to the build after checking ccsession (U25). Everything else as A1 |
| Command and skill | As A1, plus a test that a call with no flag creates no grant |
| Word "orchestrator" in new text | As A1, plus: any surviving "orchestrator" sentence in `core/CLAUDE.md:58` needs a glossary definition |

All other rows agreed.
