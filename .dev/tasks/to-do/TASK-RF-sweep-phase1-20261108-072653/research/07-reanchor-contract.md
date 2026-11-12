# Research: Re-anchor after fast-forward (contract side)

**Status:** Complete
**Date:** 2026-11-08
**Base:** e8db2fe6 -> 5dc29d23

---

## 1. `src/superclaude/core/WORKER-CONTRACT.md` (old 203 lines, new 327 lines)

Commits on master that touched it: #422 (`2327fbd3`, the 15 P2 conversions), #434 (`6782eee1`, v1 worker-liveness rules), #436 (`9e4e39f8`, P2 review follow-ups).

Hunks (old -> new): +1 line after old 24 (nested-result paragraph); WC-10 and WC-11 text extended in place (old 45-46); WC-3 timeout bullet, WC-5, WC-7, WC-12 text extended in place (old 57-60); WC-14 and WC-15 inserted after WC-13 (old 62 -> new 63-65); +1 bullet in WC-6 (new 79); a 107-line `### Liveness supervision` block after old 90 (new 95-201); a 6-line chain-line block in `### Brief layout` (new 210-215); later hunks in section 5. Offset for any old line after 98 and before 171: +117.

### 1.1 Citation table

| Citing file:line | Old path:line | New path:line | Status | Note |
|---|---|---|---|---|
| research/03:14 | WORKER-CONTRACT.md:9 `## 1. Terms` | :9 | CONFIRMED | |
| research/03:14 | :26 `## 2.` | :27 | MOVED | |
| research/03:14 | :30 WC-2 | :31 | MOVED | |
| research/03:14 | :31 WC-4 | :32 | MOVED | |
| research/03:14 | :39 WC-8 | :40 | MOVED | |
| research/03:14 | :40 WC-9 | :41 | MOVED | |
| research/03:14 | :45 WC-10 | :46 | CHANGED | Now says the coordinator stops, retries or releases only on Orca's stall proofs or the person's recorded stop, and absence past deadline allows only probes, a nudge and a direct question; `expect_silence_min` added. |
| research/03:14 | :46 WC-11 | :47 | CHANGED | One sentence appended: the liveness `stat` reads only the worker's own contract path and report directory. |
| research/03:14 | :48 `## 3.` | :49 | MOVED | |
| research/03:14 | :52 WC-3 | :53 | MOVED | Head bullet same; its timeout sub-bullet (new :58) gained the heartbeat-on-return and ack sentences. |
| research/03:14 | :58 WC-5 | :59 | CHANGED | Appended: the closing report is never sent as `status`, `handoff` or a reply. |
| research/03:14 | :59 WC-7 | :60 | CHANGED | Appended: a worker runs each chained `Command:` by invoking its Skill; reading the file from memory does not satisfy WC-7. |
| research/03:14 | :60 WC-12 | :61 | CHANGED | Appended: batch handling and `ack <message_id> applied`, `queued` or `refused` status lines. |
| research/03:14 | :61 WC-13 | :62 | MOVED | Text unchanged. |
| research/03:14 | :64 `## 4. Coordinator rules` | :67 | MOVED | |
| research/03:14 | :68 `### WC-6` | :71 | MOVED | One bullet added at :79 (live-attempt quiescence). |
| research/03:15, :118 | :61 "highest is WC-13" | :62 WC-13; :63 WC-14; :64 WC-15 | CHANGED | WC-14 and WC-15 now exist (worker duties, from #434). WC-13 is no longer the highest; WC-14 is NOT free. |
| research/03:19, 01:232, design 682, design 700 (R7), research/03:70, :112, :118 | :23 never-as-worker line | :23 | CONFIRMED | Text byte-identical to the old line (still `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while D3...). The design's replacement text (design :684) still applies as written. |
| research/03:24, 01:233, design 663 | :154 `### Fan-in rule` | :271 | MOVED | Text unchanged. |
| research/03:24, 01:233, design 663 | :156 fan-in paragraph | :273 | MOVED | Text unchanged ("For N input Tasks feeding one merge Task ..."). |
| research/03:24, 01:233, design 663 | :158 `### Worked example: gate hit, answer, new Task` | :275 | MOVED | Text unchanged. |
| research/01:234 | "File is 203 lines" | 327 lines | CHANGED | |
| research/03:26 | `## 5. Coordinator brief template` (contract side) | :283 | MOVED | Old line not cited in the contract; the :381 in 03:26 is a test-file line, see section 2. |

## 2. `tests/skills/test_worker_contract.py` (old 2265 lines, new 3195 lines)

New on master: `RULE_PHRASES` gained `WC-14` (:156-164), `WC-15` (:165-172), `wc6-live-attempt-settlement`, nine `liveness-*` entries, `wc10-absence-not-death`, `wc11-liveness-stat`, `heartbeat-progress-token` and a chain-line entry (the dict now closes at :374); `P2_COMMANDS` (:416-432) and 15 P2 `UNATTENDED_EXPECT` entries (dict now :438-742); P2 brief, nested-result and P2 set tests (:937-1005, :1548-1570, :1846); many more `WRITE_VERB_CLASSIFICATION` rows (now :2016-3126).

| Citing file:line | Old path:line | New path:line | Status | Note |
|---|---|---|---|---|
| research/05:70 | :18-19 `_REPO`, `CONTRACT_PATH` | :18-19 | CONFIRMED | |
| research/03:34, 05:70, 05:128, design 677, 01:293 | :25 `RULE_PHRASES = {` | :25 | CONFIRMED | |
| research/03:47, :112 | :86-92 `"never-as-worker"` entry (phrase at :89-90) | :86-92 (phrase :89-90) | CONFIRMED | Text identical. Still needs the `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard` edit when line 23 changes, or `test_contract_states_rule[never-as-worker]` fails. |
| research/03:34, design 677, 01:294 | :155 `"WC-13"` | :155 | CONFIRMED | |
| research/01:294 | :156 `"heartbeats": (` | :173 | MOVED | New :156 is the existing `"WC-14"` entry. |
| research/03:34, 01:293 | :237 dict closes | :374 | MOVED | |
| research/03:118, 05:70, 05:128, design 678, 01:295 | :245-254 `NEVER_AS_WORKER` (8 entries) | :382-391 (8 entries, `/sc:pr-submit` at :390, `)` at :391) | MOVED | Same 8 entries. |
| research/01:302 | :379 `UNATTENDED_COMMANDS` | :746 | MOVED | |
| research/03:26 | :381 `_TEMPLATE_HEADING` | :748 | MOVED | |
| research/03:34 | :388-395 `_check_rule` | :755-762 | MOVED | Logic unchanged. |
| design 686, 01:296, research/03:20 | :398-404 `_check_never_as_worker` (one-line assert :399-400) | :765-771 (:766-767) | MOVED | Logic unchanged. |
| research/03:26 | :407-410 `_template_lines` | :774-777 | MOVED | |
| research/03:25 | :430-436 setup regex | :797-803 | MOVED | Same regex. |
| research/03:25 | :446-461 `_check_repo_setup_gated` | :813-828 | MOVED | Same logic. |
| design 680, 01:297, research/03:110 | :470 equality assert | :837 | MOVED | Still `set(have) == set(UNATTENDED_COMMANDS)`; holds while `sweep.md` has no `## Unattended mode`. |
| research/03:34, 05:70, 05:128 | :540-542 `test_contract_states_rule` | :907-909 | MOVED | |
| design 679, 01:298, 05:70 | :545-546 `test_never_as_worker_list_names_all_seven_commands` | :912-913 | MOVED | Same name; tuple still has 8. |
| research/03:34 | :587-594 `test_rule_check_fails_when_rule_removed` | :1044-1051 (def :1045) | MOVED | |
| design 678, 01:299 | :624 `@pytest.mark.parametrize("cmd", NEVER_AS_WORKER)` | :1081 (test :1082) | MOVED | |
| design 680, 01:300 | :861 load test, :865 `assert "load" not in UNATTENDED_COMMANDS` | :1318, :1322 | MOVED | |
| research/03:54, :120 | :1090-1094 `AUDIT_ROOTS` | :1940-1944 | MOVED | Same three roots (skills, commands, agents). |
| research/03:54 | :1098-1101 `WRITE_VERB_RE` | :1948-1951 | MOVED | Same regex. |
| research/03:54 | :1103-1105 categories | :1953-1955 `_CATEGORY_RE` | MOVED | Same five categories. |
| research/03:54 | :1131-1152 scan | :1981 `_scan_write_verbs`, :2005 `_check_all_classified` | MOVED | |
| research/03:54 | :1166 `WRITE_VERB_CLASSIFICATION` | :2016 (closes :3126) | MOVED | |
| research/03:54, :120 | :2199 `test_every_write_verb_hit_is_classified` | :3129 | MOVED | |
| research/03:54 | :2203 stale-entries test | :3133 | MOVED | |
| research/01:289 | "file is 2265 lines" | 3195 lines | CHANGED | |

## 3. `CLAUDE.md` (repo root) and `src/superclaude/core/CLAUDE.md`

Root `CLAUDE.md` (#449): only the worktree section changed (old ~302-340). Lines before 302 keep their numbers.

| Citing file:line | Cited fact | New location | Status | Note |
|---|---|---|---|---|
| research/05:33 | worktree examples include a worktree named `integration` | `CLAUDE.md:337`, `:343` | CHANGED | Example still names `integration`, now as "created by session A with `--agent claude`". The risk note still holds. |
| research/06:110 | fork rule, `--repo IronbellyOrg/IronClaude` | `CLAUDE.md:39` | CONFIRMED | Section unchanged. |
| design 719, 876 | `.dev/tasks/` always staged | `CLAUDE.md:35` | CONFIRMED | |
| research/05:148 | `grep -rn 'src/superclaude' ...` rule | `CLAUDE.md:98` | CONFIRMED | |
| research/05:72 | `tests/skills/test_primitive_dual_surface_lookup.py` named | `CLAUDE.md:98` | CONFIRMED | |
| design 706, research/01:243, 03:75-82 | level-table copy rule (Key Documentation Files) | `CLAUDE.md:346-348` | CONFIRMED | |
| (no explicit cite) | worktree creation rule | `CLAUDE.md:308-310`, new bullet `:312` | CHANGED | `orca worktree create` now needs `--agent claude --prompt "<task>"`; a PreToolUse hook (`require-orca-worktree-agent.sh`) blocks it without `--agent`. Matters to any design step that creates a worktree, not to the sweep (read-only). |

`src/superclaude/core/CLAUDE.md` (#449): +6 lines after old line 53 (the "Every Orca worktree gets an agent" paragraph, new :55-59). The level table moved from old :65-82 to new :71-88 (markers `<!-- level-table:v1 -->` :71, `<!-- /level-table -->` :88). Its text is unchanged; no research or design line cites a line number in this file, so nothing needs re-anchoring. The design's "no level-table re-copy" (design 706) still holds.

## 4. Facts the design depends on

### (a) WC rule IDs on master

IDs in `src/superclaude/core/WORKER-CONTRACT.md`: WC-2 (:31), WC-4 (:32), WC-8 (:40), WC-9 (:41), WC-10 (:46), WC-11 (:47), WC-3 (:53), WC-5 (:59), WC-7 (:60), WC-12 (:61), WC-13 (:62), **WC-14 (:63) "No turn ends between chain steps"**, **WC-15 (:64) "Context-safe reading and handoff files"**, WC-6 (`### WC-6`, :71). No WC-1 exists. WC-14 and WC-15 are worker-session duties from #434. Both are pinned in `RULE_PHRASES` (`test_worker_contract.py:156-164`, `:165-172`) and named in the brief chain line (contract :213 and template :289).

**Next free ID: WC-16.** The design's `### WC-14. Coordinator loop` (design 668) collides with the existing WC-14. Every design and research mention of "WC-14" for the coordinator loop must become WC-16: design 663-680 (section 8 heading, text block, pins), 695 (R2 bullet), 701 (R8 changelog), 777 (FR-023 row), 926 (step 1.17), the `.gitignore` comment text (research/01:285) and research/03:15, :24, :34, :112, :118. The existing contract references to WC-14 (S6 row :124 "the WC-14 exception", chain lines :213, :289) mean the worker rule and must not change.

### (b) Never-as-worker list

`WORKER-CONTRACT.md:23`, unchanged from the old base:

> - **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode. The list changes only when the coordinator-only command set or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.

The design's replacement (design 684) applies as written. Brief-guard case 3 (:20) refuses any command on this list, so adding `/sc:sweep` makes the guard refuse it as a worker.

### (c) Master's section 4 "The sweep" and the L1 probe row

Both are in `### Liveness supervision` (`WORKER-CONTRACT.md:95-201`, new in #434).

`:110` "The sweep." paragraph, in chunks:

- "After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep:"
- "one `worker-list`, one prompt-wait listing (`worktree ps --agent-wait`) and one `stat` per worker contract path (WC-11),"
- "updating each worker's heartbeat record (arrival time, progress token, declared window)."
- "Costly probes (transcript tail, screen read) run only for workers a trigger fired for in this sweep."

Its bullets: deadline W (:112), semantic change (:113), starting values (:114). The states table S0 to S11 is at :116-129 (S4 reads `agentWait`, :122; S6 names "the WC-14 exception", :124).

`:151` L1 probe row: "| L1 probe | Read-only: `worker-show`, `worker-read --source transcript`, a screen read, the contract `stat` | A trigger fired | Every sweep; at most 2 costly probes per triggered worker per sweep |".

Orca verbs and flags named in these two places:

- `:110`: `worker-list`; `worktree ps --agent-wait` (verb `worktree ps`, flag `--agent-wait`). `stat` is a file stat, not Orca.
- `:151`: `worker-show`; `worker-read --source transcript` (verb `worker-read`, flag `--source transcript`); "a screen read" (no verb named); `stat` again.

Elsewhere in the same section: `orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000` and `--ack` (:101-104); `worker-list` after three empty waits (:107); `reply --id` (:108); `orca terminal send --text "<copy>" --enter --wait-submit <s>` (:135); `--wait-submit` for nudges (:152, :161).

Points for the design (observations, not decisions):

- Master already uses "sweep" for the coordinator's own liveness pass, bounded to "at most once every 5 minutes" and pinned by `RULE_PHRASES["liveness-sweep-and-states"]` (`test_worker_contract.py:209-219`, phrase at :212). The design's coordinator-loop text says "On every coordinator wake, the coordinator runs `/sc:sweep`" and "It sweeps on every wake". As written, that reads against the 5-minute bound. WC-16 should either say that `/sc:sweep` is how the :110 sweep is run (same cadence) or state how the two relate.
- The design's sweep classes ("stalled" only on Orca's stall proofs, otherwise "could not determine") sit beside master's S0-S11 states (:116-129) and the "Never on silence" list (:182-192). WC-10 (:46) now says the same thing as the design sentence "A missing heartbeat is absence, never death".
- The design's escalation list still matches master: third brief-guard refusal (:244), a ready Task it did not create (:246), a frozen plan (:250), a fan-in with fewer than 2 (:273).

### (d) Test-pin changes the design asks for

| Design pin | Old line | New line | Still valid? |
|---|---|---|---|
| Add `"WC-14": ("WC-14", ["WC-14. Coordinator loop", ...])` to `RULE_PHRASES` after WC-13 | dict :25, WC-13 :155 | dict :25, WC-13 :155, existing `"WC-14"` :156-164 | **No, as written.** A second `"WC-14"` key in the dict literal silently replaces the existing worker WC-14 entry (the later key wins) and drops its pins. Use key and ident `"WC-16"` with phrase `"WC-16. Coordinator loop"`, inserted after `"WC-15"` (:165-172) and before `"heartbeats"` (:173). It is then covered by `test_contract_states_rule` (:907-909) and `test_rule_check_fails_when_rule_removed` (:1044-1051) with no further change. |
| Append `"/sc:sweep"` to `NEVER_AS_WORKER`, giving 9 | :245-254 | :382-391 | Yes. Still 8 entries today. The removal test (:1081-1082) picks it up. |
| Update the `RULE_PHRASES["never-as-worker"]` phrase (research/03:112; not in the design's list of four) | :86-92 (phrase :89) | :86-92 (phrase :89) | Yes, and required. The phrase quotes `` `/sc:spawn` and `/sc:swarm-wizard`, `` verbatim, so the line-23 edit breaks it unless :89 becomes `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, ``. |
| Rename `test_never_as_worker_list_names_all_seven_commands` to `test_never_as_worker_list_names_every_listed_command` | :545 | :912 | Yes. The name is unchanged on master. |
| Add `assert "sweep" not in UNATTENDED_COMMANDS` next to the `"load"` assertion | :865 | :1322 (test def :1318) | Yes. |
| Equality check holds with no edit | :470 | :837 | Yes, while `sweep.md` has no `## Unattended mode`. |
| `_check_never_as_worker` needs one line | :398 | :765 | Yes. |

### (e) New tests that would constrain WC-16 or `/sc:sweep`

- `_check_p2_set` (`test_worker_contract.py:1556`, called by `test_p2_command_set_is_complete`, :1569) asserts that `UNATTENDED_EXPECT` has exactly 31 entries (P1 16 + P2 15). `sweep` must not be added there. `_check_p1_set` (:1355) also rejects a name outside P1 and P2.
- `_check_no_unattended_sections` (:831-839) still globs every `src/superclaude/commands/*.md`, so `sweep.md` must not have `## Unattended mode`.
- The write-verb audit (`AUDIT_ROOTS` :1940-1944; `_scan_write_verbs` :1981; `test_every_write_verb_hit_is_classified` :3129; `test_classification_table_has_no_stale_entries` :3133; `test_read_only_entries_are_not_gh_api_posts` :3150) scans all of `src/superclaude/{skills,commands,agents}` recursively. Any `git add|commit|push|merge|stash|update-ref|worktree add|worktree remove` or `gh pr|gh api` text in `sweep.md` or `sc-sweep-protocol/` needs a `WRITE_VERB_CLASSIFICATION` row (categories at :1953-1955: `wc9-allowed`, `deferred:P[1-4]`, `never-worker`, `no-command`, `read-only`). Once `/sc:sweep` is on the never-as-worker list, `never-worker` is available to it, as it is for `/sc:git`, `/sc:issue` and `/sc:pr-submit`. A `gh api` read classed `read-only` must not look like a post (`_is_gh_api_post`, :1966).
- `RULE_PHRASES["liveness-sweep-and-states"]` (:209-219) and `["liveness-ladder-and-restart"]` (:228-237) pin the existing "sweep" wording at contract :110 and :151. WC-16 must not reword those lines.
- `_check_repo_setup_gated` (:813-828) fails on any contract line with a code span starting `make`, `bash`, `sh`, `uv`, `python` and similar (regex :798-803) unless the line carries the child-setup gate phrases. In a WC-16 paragraph, `` `uv run superclaude sweep run` `` would trip it; `` `superclaude sweep run` `` would not (`superclaude` is not in the launcher list). The design text (design 670) has only `` `/sc:sweep` ``, so it has no hit.
- `_check_rule` (:755-762) needs the ident on the same line as the first phrase. A `### WC-16. Coordinator loop` heading satisfies it.
- No test counts the WC rules or checks heading order in section 4, so no count test blocks adding `### WC-16. Coordinator loop` between :273 and :275.

### Other design references checked

- Design 661 and step 1.16a (gate on the PR #422 overlap): #422 (`2327fbd3`) is now merged on master. The 15 P2 conversions are in the contract (:304) and the tests (:416-432), so the overlap check reduces to "already merged".
- Design 803 (D3 is mentioned on contract line 23): CONFIRMED, :23.
- Design 926-928 (steps 1.17-1.19): still valid, apart from the WC-14 to WC-16 rename and the new anchors above.
- Design 961 rollback command (`uv run pytest tests/skills/test_worker_contract.py ...`): still valid.

## Summary

- WORKER-CONTRACT.md: line 23 (the never-as-worker list) is unchanged. The fan-in paragraph and the worked-example heading moved from :156/:158 to :273/:275 with the same text. The other WC anchors in research/03:14 shifted by 1 to 3 lines, and WC-5, WC-7, WC-10, WC-11 and WC-12 gained text.
- **Blocking: WC-14 and WC-15 already exist on master (#434). The coordinator-loop rule must be WC-16** in the contract, the `RULE_PHRASES` key (a second `"WC-14"` key would silently override the existing one), R2, R8, FR-023, step 1.17 and the `.gitignore` comment.
- test_worker_contract.py grew from 2265 to 3195 lines. `RULE_PHRASES` :25 and WC-13 :155 are unchanged; `NEVER_AS_WORKER` is now :382-391; the "seven" test is :912; the load assertion is :1322; the removal test is :1081; the write-verb audit spans :1940-3150. All four design pins stay valid with WC-16 in place of WC-14, plus the required `never-as-worker` phrase edit at :89.
- Master's `### Liveness supervision` (:95-201) already defines a coordinator "sweep" (:110: `worker-list`, `worktree ps --agent-wait`, `stat`; at most once every 5 minutes) and an L1 probe (:151: `worker-show`, `worker-read --source transcript`, a screen read, `stat`). WC-16's "on every wake" wording should be aligned with the 5-minute bound pinned at test :212.
- Root CLAUDE.md changed only in its worktree section (an agent is now required on `orca worktree create`); every cited rule still holds. core/CLAUDE.md gained 6 lines, and its level table moved to :71-88 with the same text; nothing cited there needs a new line.
