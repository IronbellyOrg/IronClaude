# QA Report — Research Gate (Partition 2 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339) — research evidence
**Date:** 2026-11-07
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report only; no research file edited)
**Depth tier:** Deep
**Assigned files:** `research/scope-03-cli-patterns.md`, `research/scope-04-409-layout.md`, `research/06-orca-open-questions.md`
**Checklist items applied:** 1 (file inventory), 2 (evidence density), 3 (scope coverage), 4 (documentation cross-validation)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

Pre-review checksums (md5) of the assigned files, used to prove they were not modified:

- `scope-03-cli-patterns.md` 11ae48052f171505d23a4aa36c80a8f9
- `scope-04-409-layout.md` 924801984e4c13865000ef6ba0d7f456
- `06-orca-open-questions.md` 6997f04c6493272b29fa954b89b19ea0

---

## File 1: `research/scope-03-cli-patterns.md` (200 lines, read in full)

**Status line:** `**Status:** Complete` (line 3). **Summary section:** present (lines 198-200).

Verification method: three bounded read-only batch scripts that printed every cited line range (main.py, recommend/reflect packages, the reflect test suite, the four command files, routing tests, HOW-WE-WORK, Makefile, pyproject, pre-commit, CI workflow, the issue design doc, four skills), plus Grep on `test_how_we_work_routing_table.py` for `_command_text` and on the design doc for "500 lines".

### Claims verified true (every claim in the file was checked)

| Claim (scope-03 line) | Evidence checked |
|---|---|
| Root group `main.py:18-26`; built-ins at 29, 283, 334, 432, 471, 513 (L44-45) | grep of `@main.command`/`def` in main.py: exact lines match |
| 11 deferred registrations 519/521 ... 559/561, `__main__` at 564-565, cli-portify has no `name=` (L46-55) | main.py:510-565 printed; all pairs, comment text and `main.add_command(cli_portify_group)` match |
| Lazy `__getattr__` at `recommend/__init__.py:12-20`; eager imports at `reflect/__init__.py:17-30`, docstring 1-15 (L57-58) | both files printed in full |
| Package file line counts for recommend/ and reflect/, no `__main__.py` (L64-65) | `wc -l` and `ls`: every count matches; no `__main__.py` |
| `PURE` at contract.py:397, "No Click, no subprocess" at :7; config.py:158-159 quote (L66) | grep + awk print |
| `_git` at config.py:64-78, docstring :67, fail-closed callers 103-109, 151-152, 182-183 (L80-90) | awk print of 60-112, 148-186 |
| `shutil.which("claude")` runner.py:387, `shutil.which("tmux")` commands.py:494 (L91) | grep |
| `patch_git` conftest.py:58-80, `which` patch :95, `FIXTURES_DIR` :17 (L97-100) | conftest printed 1-100 |
| `patch(...config._git...)` test_isolate_reviewers_cli.py:97, 140, 163; MagicMock 265/266, 287; preflight :53 (L97-98) | grep and awk print |
| Read-only proof pattern test_contract_status_cli.py:44-66, docstring 18-22 (L99) | printed 1-70 |
| `tests/cli/` has no `__init__.py`; `tests/cli/reflect/` has one (L96) | `ls` (error for tests/cli/__init__.py) |
| Frontmatter of reflect.md / issue.md / recommend.md; `name: sc:recommend` CONTRADICTED tag (L106-108) | `head` of all three |
| 47 `.md` command files, 14 with `allowed-tools`; validate-tests/init-lite/post-release :6, graph :9, help :6; none in reflect/issue/recommend (L109) | `ls | wc -l` = 47, `grep -l | wc -l` = 14, grep of the eight files |
| Heading lines in issue.md and reflect.md (L110) | `grep -n '^## '`: all 21 line numbers match |
| Activation blocks reflect.md:146-151, issue.md:87-93, recommend.md:52-58 with the stated CONTRADICTED difference (L111-122) | awk print of all three ranges |
| `_POST_REFRESH_ADDITIONS` :33, `_ACTIVATION_RE` :38-40, `^> Skill (\S+)$` :472, assertion :647-648 (L122, L136) | awk print |
| `_OTHER_COMMANDS` :27-40; set equality and existence at :291-311; excluded set :299-309 (L138, OQ2) | awk print; `_command_text` (:142-154) asserts `path.is_file()`, so the existence claim holds |
| HOW-WE-WORK "Other commands" :314-337, markers :318/:337 (L137) | awk print 310-339 |
| Plugin byte copy `filecmp.cmp` :38, mirrors :41-47; CLAUDE.md level-table markers :65/:82 (L139, L149) | awk print + grep |
| UTILITIES table :105, `/sc:issue` row :115, detail :347 (L140) | grep docs/user-guide/commands.md |
| `EXPECTED_TOP_LEVEL_COMMANDS` :31-49 omits swarm and reflect; `--help` loop :95-106; eval docstring fragment :69 (L71, L141) | awk print 25-108 |
| help.md:30-34 live `find -L`, Boundaries :134; test_cli_install.py:638-647 four names (L146-147) | awk print |
| Ruff pin pyproject:54 with comment :50-53; pre-commit rev v0.15.20 :109-113; ruff config :173-193; banned `anthropic` :203-206; CI :100-106 (L154-156) | awk print of all ranges |
| Makefile install 5-7, test 13-15, lint 48-50, format 53-55, sync-dev 109, verify-sync 166; no `format-check` target (L157) | target grep + awk print |
| Design doc header 1-9, 20 headings at the cited lines, :355 "Under 500 lines", :362-363, :380 "line 32 today", :384, :402, :404-410 (L128, L136, L158-187) | heading grep + awk print + Grep "500 lines" (hit at :355) |
| swarm-wizard SKILL.md:7, :35, :69, :110; sc-recommend SKILL.md:77, :309, :324 (OQ3-4) | awk print |
| 25 `sc-*-protocol` folders; no `commands/sweep.md`, no `cli/sweep/` (L56, L129) | `ls -d | wc -l` = 25; `ls` errors for both paths |

### Findings in scope-03

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| S3-1 | IMPORTANT | scope-03 L150 ("No test found that globs every `src/superclaude/skills/*/SKILL.md` for a registry ... [CODE-VERIFIED negative result, limited to that Grep]") | False negative presented as verified. Two tests glob every skill: `tests/skills/test_model_alias_policy.py:85` (`(SRC / "skills").glob("*/SKILL.md")`, with every agent and command at :84-86, asserting any frontmatter `model:` is an alias, :97-99) and `tests/commands/test_graph_command.py:222` (`_SKILLS_DIR.glob("*/SKILL.md")`, asserting no skill calls `sc:graph-protocol`, :219-225). These are suite-wide scans a new `sc-sweep-protocol/SKILL.md` and `commands/sweep.md` must pass, so the "registries and tests a new command/skill/CLI must be added to" list (L131-150) is incomplete for planning. Other suite-wide primitive scans plausibly apply and are not mentioned (research-notes.md:28 cites `tests/skills/test_worker_contract.py` `AUDIT_ROOTS :1090-1094` over skills, commands, agents; repo CLAUDE.md names `tests/skills/test_primitive_dual_surface_lookup.py`); not re-read by this QA. | Replace L150 with the two globbing tests and what they enforce; add a "suite-wide scans every new primitive must pass" list (model alias policy, sc:graph caller ban, worker-contract audit roots, dual-surface lookup) with file:line, each re-read. |
| S3-2 | MINOR | scope-03 L75 | "`click.echo(json.dumps(row, ensure_ascii=False))` (commands.py:75, 461)": line 461 is `click.echo(json.dumps(result.to_dict(), ensure_ascii=False))`, not `row`. The convention itself is true. | Write "`json.dumps(<obj>, ensure_ascii=False)` (commands.py:75 `row`, :461 `result.to_dict()`)". |

---

## File 2: `research/scope-04-409-layout.md` (331 lines, read in full)

**Status line:** `**Status:** Complete` (line 4). **Summary section:** present (lines 322-331).

Verification method: four bounded read-only batches, all `git show 495eb96d:<path>` to stdout only (no checkout, no file written):

- The seven package markdown files printed in full with `cat -n` (README, DESIGN-CONTRACT, data-dictionary, integration-gaps, concepts, PLAN, QA), plus DESIGN-CONTRACT.md:11 and integration-gaps.md:7 printed untruncated.
- `canvas.py`, `fixtures.py` and `layouts/agent_focus.py` printed in full with `cat -n`.
- The four exports (`agent-focus/exports/{116,80}/{attention-ledger,shift-brief}.txt`): `wc -l` and the cited line ranges.
- Grep of `render.py` (imports, :21, :98, :113, :116, and any mention of `sources.json`/`PREVIEWS`/`index.html`), `tests/test_designs.py` (:30-40, :50-60, :84-90), `agent-focus/manifest.json` (:30-34, :142-146), `git ls-tree` of the package, `git merge-base --is-ancestor 495eb96d origin/master` (rc=1, not an ancestor) and `git ls-tree -d origin/master` of the package path (0 entries).
- Grep of `.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md` for the branch name (hit at :44).

### Claims verified true (every claim in the file was checked)

| Claim (scope-04 line) | Evidence checked |
|---|---|
| Line counts README 52, DESIGN-CONTRACT 17, data-dictionary 50, integration-gaps 28, concepts 51, PLAN 73, QA 51, canvas.py 122, fixtures.py 122, agent_focus.py 183, each export 42 (L15-28) | `cat -n` final line numbers; `wc -l` = 42 for all four exports |
| README.md:15 set 2 names; :39-41 three quoted sentences; :48 Pillow prototype and Charm "leading production candidate"; :52 "No capacity, latency ..." (L15, L213-215, L258-259) | README printed in full; all match verbatim |
| DESIGN-CONTRACT.md:10 heading, :11 the ten "Required semantics" sentences, :14 "116 must rearrange, 80 must simplify to selected detail." (L16, L65, L198-210, L232-233, L239, L252) | :11 printed untruncated; all ten sentences match verbatim and in order |
| data-dictionary.md :3 preamble, :7-15 entity table, :17-28 ten dimensions and quoted rules, :32-40 measurements, :46 overview/historical, :50 missing-evidence paragraph (L17, L68, L163-196, L226, L244) | printed in full; every quoted value set and rule matches |
| integration-gaps.md :7 "never uses worker_done alone ...", :9-16 six "Not established" items, :12 co-location, :20 "Proposed only" sentence, :24 missing-data sentences (L18, L67, L101, L221-223, L251, L257) | :7 printed untruncated; rest printed in full |
| concepts.md :7 Fleet Quilt, :9 Worktree Atlas, :23 Attention Ledger, :31 Shift Brief, :35-40 compact modes, :36 and :38 quotes (L19, L78, L92, L98, L133, L159, L235, L245) | printed in full |
| PLAN.md :32-38 contract incl. :33, :34, :36, :38 quotes; :54 color rule; :56-57 width rules; :66 "No clipped actionable fields ..." (L20, L66, L216-220, L234, L240) | printed in full |
| QA.md :13 "Labels retain meaning without color.", :23, :27 (two quotes), :31-38 limitations, :32, :35 (L21, L220, L224, L241, L254, L258) | printed in full |
| canvas.py `sanitize` :10-17, `clip` :19-29 with "…"/"~", `header` :73-77 (rows 1-3 text, hardcoded `08:00 UTC` at :77, no `f['scope']` read), `footer` :78-81, `selected_summary` :117-122 incl. the empty-fixture sentence (L22, L39-45, L53, L71-74, L89, L219, L236, L245) | printed in full |
| fixtures.py `as_of` :13, five sources :14-18, orchestrators :19, `scope` :21, session fields :30-43 (all 27 names match), worktree fields :45-47 with `conflict: "not established"`, requests :50-55 (ages 45/20/10, `state` :55), approval set :56-57, edges :58-60, events :61-64 (`resolved` :63), source-loss `unavailable` :76, empty :84, injection :85-86, `normalize_events` :90-95, `metrics` :98-111 (total, historical, worktrees vs inventory, unmapped, set-union affected), `write_fixtures` :114-122 writing only `fixture.json` (:116) and `scenarios/*.json` (L23, L35, L60-62, L71-73, L93, L99, L165-194, L247, L255) | printed in full |
| agent_focus.py `frame` :9, `qlines` :11, `listbox` :13-17 with `shown/len lines shown` at :17, `evidence_rows` :21, `narrow` :22-24, `attention` :41-53 (narrow switch :43, panels :45/:51/:53, loop :46 in fixture order with `y=8+i*8` :47, fields :47-49, seven retained facts :53), Outcome Ledger total :107, `shift` :156-169 (no `c.w<116`), DESIGNS :171-183 with slugs/questions/omits at :174 and :182 (L24, L39, L78-89, L93, L96-97, L129, L133-143, L158-159, L236, L242-243, L247) | printed in full |
| Export lines: 116/attention-ledger :2-4 header, :9-12/:17-20/:25-28 rows, :37 "7/7 lines shown", :41-42 footer; 80/attention-ledger :7-9, :14-18, :37 "5/5 lines shown"; 116/shift-brief :9, :11, :13, :19-21, :37-38; 80/shift-brief :38 ends "operational d…" (L46-57, L104-127, L145-158, L242) | cited ranges printed; text matches the excerpts exactly |
| render.py :21 imports `layouts.group_a`/`group_b` (via importlib at :23), :98 "does not acknowledge any message", :113 denominator text, :116 empty text; no mention of `sources.json`, `PREVIEWS.md`, `index.html` (L30, L33, L100, L225, L244) | grep; the last check returned no hit |
| tests/test_designs.py :37 age assertion, :55 events, :56-57 filter denominators, :58 empty, :87 SYNTHETIC, :88 footer (L29, L62, L68, L74, L225, L227, L244) | printed ranges |
| manifest.json :32 `attention-ledger`, :144 `shift-brief` (L31, L78, L133) | printed ranges |
| The three [CODE-CONTRADICTED] findings: no sort in code (L93); wide ledger and Shift Brief have no bound and no omission count (L247); "Not read ... all generated from fixtures.py" holds only for scenario JSON (L33) | the code confirms each: no `sorted` in `attention`/`shift`; loops :46 and :164 have no slice; `write_fixtures` writes no `sources.json`/`PREVIEWS.md`/`index.html`, and `group_a.py`/`group_b.py` are source files in `git ls-tree` |
| 495eb96d not an ancestor of origin/master; package absent from master; seed-brief.md:44 names `docs/409-orca-dashboard-designs` at 495eb96d (L260) | `merge-base --is-ancestor` rc=1; `ls-tree -d origin/master` 0 entries; Grep hit at seed-brief.md:44 |

### Findings in scope-04

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| S4-1 | MINOR | scope-04 L256 | "ID formats O01/S001/W001/Q01/E01/D01 (PKG/data-dictionary.md:9-14)": the dictionary names O01, S001, W001, Q01 and E01 only; its Event row (:14) says "stable id and monotonic fixture seq" with no `D01`. `D01` comes from `fixtures.py:61`. | Cite `D01` to `fixtures.py:61-64`, or drop it from the data-dictionary citation. |
| S4-2 | MINOR | scope-04 L129 | "the wide view prints neither the request `id` nor its `evidence` reference ...; the narrow view and Shift Brief do (agent_focus.py:11, :165-167)". Shift Brief prints both for every request. The narrow view prints the `id` for every request (`qlines`, :11) but the evidence reference only for the first request, through `selected_summary` (canvas.py:122). | Write "the narrow view prints every `id` but only the first request's evidence (canvas.py:122); Shift Brief prints both for every request". |
| S4-3 | MINOR | scope-04 L129 and L247 | The overflow is understated. Past the fixture's three requests the wide layouts do not just lose an omission count. They write outside the canvas, and `Canvas.text` asserts in-bounds coordinates (canvas.py:39). At 116 columns (42 rows), a fifth request in the wide Attention Ledger puts its requester line at row 42 (`y=8+4*8`, `+2`), which raises `AssertionError`. In Shift Brief, a fifth request (`y=38`, rows 38-40) overwrites the separator and the key-hint footer that test_designs.py:88 asserts. A sixth request raises. Nothing a static report reuses depends on this, so it is a note only. | Add one sentence: with more requests than fit, the prototype crashes or overwrites its footer (canvas.py:39), so "no omission count" is the mild reading. |

No IMPORTANT or CRITICAL findings in scope-04: every file:line citation and every quoted string checked holds as stated. Evidence density is Dense (more than 95% of claims carry a path and line).

---

## File 3: `research/06-orca-open-questions.md` (182 lines, read in full)

**Status line:** `**Status:** Complete` (line 5). **Summary section:** present (lines 179-181). Gaps (L153-170) and Stale Documentation (L172-177) sections present.

Verification method:

- One bounded read-only batch printed, through `cat -n`: `orca-ide --version`, plus `--help` for `orchestration`, `check`, `ask`, `reply`, `inbox`, `worker-list` and `worker-show`, plus `status --help` and `worktree ps --help`. No message, Run or worker verb was run.
- A second batch printed the cited line ranges of `skills get orchestration` (215 lines) and of its `messaging-and-gates` (76 lines) and `recovery-and-cleanup` (186 lines) references, plus `skills get orca-cli` (289 lines).
- I read `WORKER-CONTRACT.md` lines 9-62 and 130-137 and `orca-capabilities.md` in full.
- I read `/opt/Orca/resources/app.asar.unpacked/out/cli/handlers/orchestration/message-check-handler.js` lines 10-95, the handler that the file's own Gap 1 names. I also used Glob on that directory.
- I relied on `integration-gaps.md` lines 11, 12 and 28 at 495eb96d from the File 2 batch.

### Claims verified true

| Claim (06 line) | Evidence checked |
|---|---|
| Installed version `1.4.245-aidev02.780594c521aa`; inventory `:8` has 1.4.237 dated 2026-11-02; inventory `:63` cites `[G]` 108; today it is `[G]:113` (L12) | `--version` output; inventory :8 and :63 read; `[G]:113` printed |
| `[H:ask]:3` usage, `:5` description, `:16` `--dispatch-capability`, `:23` Run mailbox default, `:24` timeout text verbatim (L23-25) | ask help printed; all five lines match |
| Inventory `:58` usage quote, `:68` UNVERIFIED default, `:177` open item 2 (L24-25) | inventory read |
| `[G]:113` wait, `[G]:140` reply, `[G:messaging]:60-63` ask/reply/helper (L26) | printed; match |
| `[H:reply]:3`, `:5` (L27) | printed; match |
| `[H:check]:35` `--types` wake-only text (L28) | printed; verbatim |
| WC-3 `:52-57`, default report-blocked `:53`, `blocked_question` `:30`, one ask `:55`, no heartbeat in ask `:57` (L29) | WORKER-CONTRACT read; match |
| `[G:messaging]:76` gate sentence (L30) | printed; match |
| `[G]:135` "replays that batch until acknowledged"; `[H:check]:37` concurrent waits text (L32) | printed; quotes match |
| `[H:check]:4`, `:5`, `:6`, `:7`, `:8`, `:24` (`--unread`), `:28`, `:36`, `:37`; `[G:messaging]:17-19`, `:26-27` (Q2 table) | printed; each quoted string matches |
| `[H:inbox]:3`, `:5`; no read-marking or cap note in `:3-14` (Q2 table, L149) | printed |
| `[G:messaging]:12-15` caller identity; inventory `:149` quoting `terminal-identity.js:213-215` (L66) | printed; inventory :149 read |
| `check` usage line has no `--cursor` (L67) | `[H:check]:3` printed |
| `[G]:42` classification row; inventory `:148`; `WORKER-CONTRACT.md:11` (L92) | printed and read; match |
| `[H:worker-list]:5`, `:20`, `:22` (L93) | printed; match |
| `[H:worktree-ps]:3`, `:5`, `:13`, `:16-17`, `:19`; `[CLI]:84` (L94) | printed; match |
| `[CLI]:227` paneKey join; `[CLI]:161`, `:162` (L95-96) | printed; match |
| `[H:status]:14`; inventory `:151` (no `caller`), `:185` open item 10 (L97) | printed and read |
| integration-gaps lines 11, 12 and 28 at 495eb96d (L67, L98, L136) | File 2 batch; text matches |
| `[H:worker-show]:16` agentWait text verbatim (L101, L124) | printed |
| WC-5 `:58`; freeze `:133`; effects `:134-136` (L123) | read; match |
| `[G]:81-83`, `[G]:62-64`, `[G:recovery]:30-31`, `:54-56`, `:58-61` (L124-125) | printed; match |
| WC-10 `:45` quote; inventory `:182` open item 7 (L127) | read; match |
| `[H:orch]:19-20` worker-show/worker-read, `:25` worker-list; `[G:recovery]:28-29` (L129) | printed; match |
| `[G]:156-161` stop/abandon needs positive proof (L135) | printed |
| Gap 16: `[G]:130-131`, `[G:messaging]:62`, inventory `:97-98` (depth 1), WC-13 `:61`, inventory `:35` (L170) | printed and read; match |
| Handler path in Gap 1 exists (L155) | Glob: 22 handler files including `message-check-handler.js`, `message-inbox-handlers.js`, `question-handler.js` |

### Findings in 06-orca-open-questions

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| 06-1 | IMPORTANT | 06 L32 ("drained only by `--ack` (`[H:check]:5`, `:37`)", "`check --wait` without `--ack` does not drain") and the Q2 table, row `check` (default) ("Not draining by itself (replays until `--ack`)" / "Draining needs `--ack`: [CODE-VERIFIED]") | False claim, contradicted by its own citations. `[H:check]:37` reads "A bound Run replays the same Delivery until --ack **or all its messages are marked read**". `[G:messaging]:17-19`, quoted in the same table cell, says the same. The file's own Q2 answer (L49) also says this, so the file contradicts itself. The file implies that a consuming check marks rows read (L55, from `[H:check]:6`). If so, a plain `check` or a `check --wait` can end the replay without `--ack`. The [CODE-VERIFIED] tag on "Draining needs `--ack`" is therefore wrong on the central question of whether reading is destructive. | At L32 and in the table cell, state that a Delivery ends on `--ack` or once all its messages are marked read. Tie whether a consuming check drains to Gap 1 (read-marking) and tag it [UNVERIFIED]; do not tag it [CODE-VERIFIED]. |
| 06-2 | IMPORTANT | 06 L175 (Stale Documentation: "the `ask` usage line now also lists `--dispatch-capability`") and L25 | False [STALE DOC] claim. Today's usage line `[H:ask]:3` does **not** list `--dispatch-capability`. The flag appears only in the Options list at `[H:ask]:16`. Today's `:3` matches the inventory quote at `orca-capabilities.md:58` word for word, so `:58` is not stale. The synthesis gate must surface every [STALE DOC] finding, so this false tag would reach the final report's gap analysis. | Remove `:58` from the [STALE DOC] bullet. Rewrite: "`--dispatch-capability` appears in today's Options list (`[H:ask]:16`) but in neither the usage line (`[H:ask]:3`) nor the inventory". Keep `:8` and `:63` as stale line numbers. |
| 06-3 | IMPORTANT | 06 L15 (label scheme), L58-59 and L79 (`--peek`/`--all` "[CODE-VERIFIED] (documented; not exercised)"), Gaps 1-3 and 15 (L155-157, L169) | Doc-sourced claims are tagged [CODE-VERIFIED] even though the code was readable read-only and contradicts or qualifies them. L15 redefines [CODE-VERIFIED] to mean "documented by the CLI's help or guide", so every help-text claim is a doc claim carrying a code tag. The handler that Gap 1 names exists, and I read `message-check-handler.js`. In it: (a) `:17` "Older runtimes ignore peek, making --unread --peek destructive", which implies `--unread` is a consuming (marking) mode; that answers most of Gap 3, which is still open in the file. (b) `:33-35` sends `unread:false` with `peek` so that "hosts that ignore peek fall back to non-consuming all mode", and `:74-84` filters read rows on the CLI side and warns "this runtime returned only its newest 100 messages for --peek". So whether `--peek` is non-marking depends on runtime support. (c) `:58-71`: after printing, the CLI makes a second `orchestration.check` call with `compatibilityAck` whenever the result carries `legacyCompatibility.ackMessageIds`. This is an undocumented acknowledgement side effect of a `check`; nothing in the file mentions it, and the file's "Allowed read modes: `check --peek` and `check --all`" (L71) does not rule it out. (d) `:38` sends `format: true` as a boolean and `:55` passes it to the text formatter. That settles Gap 15: `--format` is a text-rendering switch, and the `<png|jpeg>` help label at `[H:check]:28` is a mislabel. (e) `:30` sends every `check`, including `--peek` and `--all`, through `callOrchestrationMutation`. The Deep tier left these read-only-resolvable questions open while labelling the help-text answers [CODE-VERIFIED]. | Relabel help and guide claims as doc-sourced: use [UNVERIFIED], or [CODE-VERIFIED] only where code was read. Add the handler evidence (a)-(e) with `file:line`. Resolve Gaps 3 and 15 from it. Add a new gap and sweep constraint for the `compatibilityAck` follow-up call: a sweep must prove that `--peek`/`--all` results never carry `legacyCompatibility.ackMessageIds`, or avoid `check` entirely. Read `message-inbox-handlers.js` for Gap 4 the same way. |
| 06-4 | MINOR | 06 L24 ("new in this CLI version") | The inventory (`orca-capabilities.md:60`) quotes only the second sentence of `[H:ask]:24` from 1.4.237. Whether 1.4.237 already printed the default cannot be checked now. The [STALE DOC] tag on `:68` still holds, because the default is documented today. | Drop "new in this CLI version", or tag it [UNVERIFIED]. |
| 06-5 | MINOR | 06 L62, L169 | The quote of `[H:check]:28` is reordered. The actual line is `--format <png|jpeg>    Screenshot image format`, not "Screenshot image format <png|jpeg>". | Quote the line verbatim. Per 06-3(d), change the [CODE-CONTRADICTED] row to "help mislabel; code shows a boolean text-format switch". |
| 06-6 | MINOR | 06 L72 ("both modes are capped at 100 rows") | `[H:check]:37` caps `--all` and a **Run** `--peek`. It says nothing about a `--peek` scoped by `--terminal`. | Write "`--all` and a Run-scoped `--peek`". |

Evidence density for 06 is Dense: almost every claim carries a `[G]`/`[H:*]`/`[CLI]` line or a repo `path:line`, and every line number I checked holds. The blocking findings are about wrong conclusions and labels, not missing citations.

---

## Scope coverage (checklist item 3)

I read `research/research-notes.md` EXISTING_FILES (lines 17-108) and checked every key file and directory against the three assigned files. For partition 2, those are the S2 data sources (L48-67), the S3 rows (L69-95), the S4 rows (L97-99), and the S1/S2/SB rows that S2 cites (L41 `orca-capabilities.md`, L46 orca-ide). Grep for each path's basename across `research/` showed that every row is discussed, except two:

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| G-1 | IMPORTANT | research-notes.md L94 (`src/superclaude/output-styles/pragmatic.md`, the mandatory DONE/NEXT table, analysis F10) and L95 (`src/superclaude/hooks/scripts/launch-job-identity.sh`, PR #414 job identity), both in the S3 section | Neither key file is discussed in any research file. Grep for `pragmatic` and `launch-job-identity` in `research/` matches only `research-notes.md`. scope-03 is the S3 output and covers every other S3 row. Without coverage, the synthesis has no evidence for the orchestrator's report format (F10) or for how a launched job is identified (#414). It will either drop both or invent claims about them. | Add a scope-03 section that reads both files and records `path:line` evidence for the DONE/NEXT table contract and for the job-identity variables the script sets. Alternatively, mark both rows out of scope in research-notes.md, with a reason. |

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports. Rows in S1/SB that partition 1's files cover were not checked here.]

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File inventory | PASS | All three files show `**Status:** Complete` and have a Summary section (scope-03, scope-04, 06 L5 and L179-181). md5 checksums were recorded before review. |
| 2 | Evidence density (every claim; every cited path and line) | FAIL | scope-03: Dense, but S3-1 (IMPORTANT) is a false negative claim. scope-04: Dense, verified through `git show 495eb96d:<path>` to stdout, with three MINOR findings. 06: Dense, but 06-1 and 06-2 (IMPORTANT) are false conclusions whose own citations contradict them. |
| 3 | Scope coverage against EXISTING_FILES | FAIL | G-1: research-notes L94 and L95 are not discussed in any research file (Grep). |
| 4 | Documentation cross-validation (every [CODE-VERIFIED] claim) | FAIL | 06-3: [CODE-VERIFIED] is applied to help and guide text, and the readable handler code contradicts or qualifies it (`message-check-handler.js:17`, `:30`, `:33-35`, `:38`, `:58-71`, `:74-84`). S3-1 is also a [CODE-VERIFIED] negative that the code disproves. |

Items 5-10 of the Research Gate checklist were not assigned to this partition (the prompt names items 1-4 only).

## Summary

- Checks passed: 1 / 4
- Checks failed: 3
- Critical issues: 0
- Important (blocking) issues: 5 (S3-1, 06-1, 06-2, 06-3, G-1)
- Minor issues (notes only): 7 (S3-2, S4-1, S4-2, S4-3, 06-4, 06-5, 06-6)
- Issues fixed in-place: 0 (fix authorization: false; no research file was edited)

## Issues Found (consolidated)

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| S3-1 | IMPORTANT | scope-03 L150 | False [CODE-VERIFIED] negative (see File 1 section) | Correct the claim with the cited `path:line`, as the File 1 table describes |
| 06-1 | IMPORTANT | 06 L32; Q2 table, `check` default row | Says only `--ack` drains, but the cited help and guide say "or all its messages are marked read" | Correct both statements and retag them [UNVERIFIED] pending Gap 1 |
| 06-2 | IMPORTANT | 06 L175, L25 | False [STALE DOC]: `--dispatch-capability` is not in the usage line `[H:ask]:3` | Remove `:58` from the stale list; say the flag is in Options only (`:16`) |
| 06-3 | IMPORTANT | 06 L15, L58-59, L71, L79; Gaps 1-3, 15 | Help text tagged [CODE-VERIFIED]; handler code not read, though readable; undocumented `compatibilityAck` side effect and runtime-dependent `--peek` missed; `--format` is a boolean | Relabel; read the handlers; record evidence (a)-(e); add the `compatibilityAck` gap and sweep constraint |
| G-1 | IMPORTANT | research-notes L94, L95 | `pragmatic.md` and `launch-job-identity.sh` are not covered by any research file | Cover both in scope-03 or mark them out of scope with a reason |
| S3-2 | MINOR | scope-03 L75 | See File 1 section | See File 1 section |
| S4-1, S4-2, S4-3 | MINOR | scope-04 | See File 2 section | See File 2 section |
| 06-4 | MINOR | 06 L24 | "New in this CLI version" cannot be checked | Drop the phrase or tag it [UNVERIFIED] |
| 06-5 | MINOR | 06 L62, L169 | `[H:check]:28` quote reordered | Quote verbatim; restate as a help mislabel |
| 06-6 | MINOR | 06 L72 | 100-row cap overstated to all `--peek` | Say "Run-scoped `--peek`" |

## Actions Taken

None. Fix authorization is false. No research file, task file or other file was edited; only this report was written. Every command run was read-only: `--help` and `skills get` text, `git show` to stdout, Read, Grep and Glob. No Orca message, Run, worker, ccsession, sweep or close command was run.

## Recommendations

1. Before synthesis, correct 06-1 and 06-2 in `06-orca-open-questions.md`. Both feed the read-destructiveness constraint that the sweep design depends on.
2. Resolve 06-3: read `message-check-handler.js`, `message-inbox-handlers.js` and `question-handler.js` read-only, and record `file:line` evidence. Add the `compatibilityAck` follow-up call as a constraint: until it is proven absent for `--peek` and `--all`, the sweep must treat any `check` as possibly state-changing.
3. Fix S3-1 in scope-03, and add coverage for research-notes L94 and L95 (G-1).
4. Apply the MINOR notes when convenient; they do not block the gate.
5. Merge this report with partition 1, then run checklist items 5-10 across the full set.

## Confidence

- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 17 | Grep: 10 | Glob: 2 | Bash: 15
- No web research was performed.
- No UNCHECKED or UNVERIFIABLE items. All four assigned checklist items were checked with tool evidence; three of them fail on findings.

## Post-review integrity

md5 recheck of the three assigned files after review: scope-03 `11ae48052f171505d23a4aa36c80a8f9`, scope-04 `924801984e4c13865000ef6ba0d7f456`, 06 `6997f04c6493272b29fa954b89b19ea0`. All three match the pre-review values, so no research file changed during this review.

## Verdict: FAIL

