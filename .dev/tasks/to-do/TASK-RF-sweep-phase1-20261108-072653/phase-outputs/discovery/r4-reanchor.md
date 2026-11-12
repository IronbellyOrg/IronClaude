# R4 re-anchor of DESIGN section 8 (item 5.5)

Each new line number was checked by reading that line of the file on this checkout (master `5dc29d23` base). The text is the first 110 characters of the line.

| Anchor | Line text read |
|---|---|
| `src/superclaude/core/WORKER-CONTRACT.md:23` | `- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:sw` |
| `src/superclaude/core/WORKER-CONTRACT.md:273` | `For N input Tasks feeding one merge Task (for example N `/sc:troubleshoot` workers, then `/sc:adversarial --co` |
| `src/superclaude/core/WORKER-CONTRACT.md:275` | `### Worked example: gate hit, answer, new Task` |
| `tests/skills/test_worker_contract.py:25` | `RULE_PHRASES = {` |
| `tests/skills/test_worker_contract.py:89` | `            "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, "` |
| `tests/skills/test_worker_contract.py:165` | `    "WC-15": (` |
| `tests/skills/test_worker_contract.py:173` | `    "heartbeats": (` |
| `tests/skills/test_worker_contract.py:382` | `NEVER_AS_WORKER = (` |
| `tests/skills/test_worker_contract.py:391` | `)` |
| `tests/skills/test_worker_contract.py:765` | `def _check_never_as_worker(text: str) -> None:` |
| `tests/skills/test_worker_contract.py:837` | `    assert set(have) == set(UNATTENDED_COMMANDS), (` |
| `tests/skills/test_worker_contract.py:912` | `def test_never_as_worker_list_names_all_seven_commands():` |
| `tests/skills/test_worker_contract.py:1081` | `@pytest.mark.parametrize("cmd", NEVER_AS_WORKER)` |
| `tests/skills/test_worker_contract.py:1082` | `def test_never_as_worker_check_fails_when_command_removed(cmd, tmp_path, monkeypatch):` |
| `tests/skills/test_worker_contract.py:1318` | `def test_load_usage_line_declares_checkpoint_and_load_is_not_converted():` |
| `tests/skills/test_worker_contract.py:1322` | `    assert "load" not in UNATTENDED_COMMANDS` |

## Old to new

| Old anchor in DESIGN section 8 | New anchor |
|---|---|
| `WORKER-CONTRACT.md` fan-in paragraph line 156 | line 273 |
| `### Worked example: gate hit, answer, new Task` line 158 | line 275 |
| `NEVER_AS_WORKER` lines 245-254 | lines 382-391 |
| removal test line 624 | lines 1081-1082 |
| `test_never_as_worker_list_names_all_seven_commands` line 545 | line 912 |
| `"load"` assertion line 865 | line 1322 (inside the test whose def is line 1318) |
| equality check line 470 | line 837 |
| `_check_never_as_worker` line 398 | line 765 |
| (new fifth pin) `RULE_PHRASES["never-as-worker"]` phrase | line 89 |

## Verification
Section 8 is lines 666-695.
```
$ sed -n '666,695p' docs/designs/orchestrator-mode.md | grep -n '156\|158\|245-254\|:545\|:865\|:470\|:398\|line 545\|line 865\|line 470\|line 398\|line 624'
(exit 1; 1 means no old anchor remains in section 8)
```
Pin list entries under "**Pins** (five edits)": 5

## main.py insertion point (item 5.6)

Read `src/superclaude/cli/main.py` lines 559-569:
```
559: from superclaude.cli.reflect.commands import reflect_group  # noqa: E402,I001  # intentional: deferred subcommand regist
561: main.add_command(reflect_group, name="reflect")
563: from superclaude.cli.issue_watch.cli import issue_watch_group  # noqa: E402,I001  # intentional: deferred subcommand reg
565: main.add_command(issue_watch_group, name="issue-watch")
568: if __name__ == "__main__":
569:     main()
```

Line 565 is `main.add_command(issue_watch_group, name="issue-watch")`, the last registered pair. The new `sweep_group` registration goes after it. `if __name__ == "__main__":` is at line 568 and the file has 569 lines.

- `grep -n 'after line 561\|519-561' docs/designs/orchestrator-mode.md`: 0 hits (expect 0)
- `grep -c 'after line 565' docs/designs/orchestrator-mode.md`: 2 (expect at least 2: step 1.7 and the rollback row)
- DESIGN section 1 line: 28:- `src/superclaude/cli/main.py` registers deferred subcommands at lines 519-565; the last pair is `issue-watch` (563, 565); `if __name__ == "__main__":` is at 568.

## Citation re-check (item 5.10)

Filtered grep (the item's pattern) on `docs/designs/orchestrator-mode.md`: 19 hit lines now (28, 63, 654, 670, 699, 711 to 718, 729, 820, 932, 944, 968, 1041). Hits in section 8: 670, 699; section 9: 711 to 718; section 10: 729. Lines 28, 670, 932 and 968 were fixed by items 5.5 and 5.6 and are not re-listed. Line 1041 is the section 18 R4 row (item 5.11), added after the first version of this table; it cites contract line 110. Line 63 (GQ-106) cites the SPEC and GAPS, and has its own rows below. Each other cited line was read in the current file.

| DESIGN hit | File:line read | Line text read (first 100 chars) | Status |
|---|---|---|---|
| 654 (graph.md line 9) | `src/superclaude/commands/graph.md:9` | `allowed-tools: Skill, Bash(codegraph init --yes *), Bash(codegraph init -i)` | CONFIRMED |
| 654 (graph.md line 41) | `src/superclaude/commands/graph.md:41` | `## Activation` | CONFIRMED |
| 699, 820, 944 (WORKER-CONTRACT.md line 23) | `src/superclaude/core/WORKER-CONTRACT.md:23` | `- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` a` | CONFIRMED |
| 711 R1 (other-commands table start) | `src/superclaude/core/HOW-WE-WORK.md:318` | `<!-- other-commands:v1 -->` | CONFIRMED |
| 711 R1 (after /sc:spawn, line 333) | `src/superclaude/core/HOW-WE-WORK.md:333` | `\| `/sc:spawn` \| Requested decomposition with sequential/parallel/adaptive strategy and normal/deep d` | CONFIRMED |
| 711 R1 (table end, line 337) | `src/superclaude/core/HOW-WE-WORK.md:337` | `<!-- /other-commands -->` | CONFIRMED |
| 712 R2 (## Orca coordination, line 396) | `src/superclaude/core/HOW-WE-WORK.md:396` | `## Orca coordination` | CONFIRMED |
| 712 R2 (never-workers bullet, line 403) | `src/superclaude/core/HOW-WE-WORK.md:403` | `- **Some commands are never workers.** `/sc:pr-submit` and the other commands on the never-as-worker` | CONFIRMED |
| 713 R3 (parity test line 38) | `tests/commands/test_routing_plugin_parity.py:38` | `    assert filecmp.cmp(_GUIDE, _PLUG_SKILL / "refs/HOW-WE-WORK.md", shallow=False)` | CONFIRMED |
| 714 R4 (_OTHER_COMMANDS line 27) | `tests/core/test_how_we_work_routing_table.py:27` | `_OTHER_COMMANDS = {` | CONFIRMED |
| 715 R5 (_POST_REFRESH_ADDITIONS line 33) | `tests/recommend/test_routing_refresh.py:33` | `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` | CONFIRMED |
| 715 R5 (assertion line 648) | `tests/recommend/test_routing_refresh.py:648` | `    assert shipped - _POST_REFRESH_ADDITIONS == active` | CONFIRMED |
| 716 R6 (### 8. UTILITIES line 105) | `docs/user-guide/commands.md:105` | `### 8. UTILITIES` | CONFIRMED |
| 716 R6 (/sc:issue row line 115) | `docs/user-guide/commands.md:115` | `\| [`/sc:issue`](#scissue---github-issue-claim-and-create) \| Claim a GitHub issue (assign, accuracy c` | CONFIRMED (text changed by master, line unchanged) |
| 717 R7 (Developer Guide line 991) | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:991` | `- The never-as-worker list (`~/.claude/WORKER-CONTRACT.md`, section 1): `/sc:agent`, `/sc:git`, `/sc` | CONFIRMED (list still lacks /sc:sweep, as R7 expects) |
| 718 R8 (CHANGELOG.md line 5) | `CHANGELOG.md:5` | `## [Unreleased]` | CONFIRMED |
| 729 (.gitignore line 254) | `.gitignore:254` | `.dev/sprint-state/` | CONFIRMED |
| 63 GQ-106 (SPEC FR-025 line 119) | `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:119` | `\| FR-025 \| `.dev/sweeps/` is added to `.gitignore` (GQ-106). A grep on 2026-11-08 found no `sweeps` ` | CONFIRMED |
| 63 GQ-106 (SPEC line 559) | `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:559` | `\| GQ-106 \| The output folder was not ignored and not in the rollback table \| `.dev/sweeps/` in `.git` | CONFIRMED |
| 63 GQ-106 (GAPS line 129) | `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/gaps-and-questions.md:129` | `\| GQ-106 \| /ponytail-review finding 6: reports under `<root>/.dev/sweeps/` are untracked, so each sw` | CONFIRMED |
| 1041 R4 row (contract line 110) | `src/superclaude/core/WORKER-CONTRACT.md:110` | `**The sweep.** After every wake or timeout, at most once every 5 minutes, the coordinator runs one s` | CONFIRMED |

Section 8 lines between `**Pins**` and `## 9.` that cite a line of `test_worker_contract.py` or `WORKER-CONTRACT.md` (written by items 5.5 and 5.8; each line read in the current file):

| DESIGN citation | File:line read | Line text read (first 100 chars) | Status |
|---|---|---|---|
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:25` | `RULE_PHRASES = {` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:89` | `            "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-w` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:165` | `    "WC-15": (` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:173` | `    "heartbeats": (` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:209` | `    "liveness-sweep-and-states": (` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:219` | `    ),` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:228` | `    "liveness-ladder-and-restart": (` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:237` | `    ),` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:382` | `NEVER_AS_WORKER = (` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:391` | `)` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:755` | `def _check_rule(text: str, rule: str) -> None:` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:762` | `        ), f"{rule}: {ident} is not stated on the line carrying {phrases[0]!r}"` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:765` | `def _check_never_as_worker(text: str) -> None:` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:831` | `def _check_no_unattended_sections() -> None:` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:837` | `    assert set(have) == set(UNATTENDED_COMMANDS), (` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:839` | `    )` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:912` | `def test_never_as_worker_list_names_all_seven_commands():` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1081` | `@pytest.mark.parametrize("cmd", NEVER_AS_WORKER)` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1082` | `def test_never_as_worker_check_fails_when_command_removed(cmd, tmp_path, monkeypatch):` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1318` | `def test_load_usage_line_declares_checkpoint_and_load_is_not_converted():` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1322` | `    assert "load" not in UNATTENDED_COMMANDS` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1556` | `def _check_p2_set(p1, p2, expect) -> None:` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1940` | `AUDIT_ROOTS = (` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1944` | `)` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1953` | `_CATEGORY_RE = re.compile(` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1955` | `)` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:1966` | `def _is_gh_api_post(line: str) -> bool:` | CONFIRMED |
| section 8 pin or constraint | `tests/skills/test_worker_contract.py:2016` | `WRITE_VERB_CLASSIFICATION = {` | CONFIRMED |
| section 8 placement (line 273) | `src/superclaude/core/WORKER-CONTRACT.md:273` | `For N input Tasks feeding one merge Task (for example N `/sc:troubleshoot` workers, then `/sc:advers` | CONFIRMED |
| section 8 placement (line 275) | `src/superclaude/core/WORKER-CONTRACT.md:275` | `### Worked example: gate hit, answer, new Task` | CONFIRMED |
| section 8 (line 110) | `src/superclaude/core/WORKER-CONTRACT.md:110` | `**The sweep.** After every wake or timeout, at most once every 5 minutes, the coordinator runs one s` | CONFIRMED |
| section 8 (line 151) | `src/superclaude/core/WORKER-CONTRACT.md:151` | `\| L1 probe \| Read-only: `worker-show`, `worker-read --source transcript`, a screen read, the contrac` | CONFIRMED |

No hit is MOVED or CHANGED, so no further DESIGN edit was needed. Line 63 (GQ-106) cites the SPEC (FR-025 line 119, line 559) and GAPS line 129, which this task does not change; it matched the grep only through the word `.gitignore`, and it is left as it was.

## Note after R4 fix cycle 1 (item 5.23)

The fix cycle changed the DESIGN from 1041 to 1043 lines, so every DESIGN line number in this file that is after the first edited place may be off by up to 2. The cited lines of the master files (`WORKER-CONTRACT.md`, `test_worker_contract.py`, `main.py`, `HOW-WE-WORK.md`, `commands.md`, `CHANGELOG.md`, `.gitignore`) did not change, and the DESIGN anchors that matter are stated by text. Section 8 now runs from line 666 to 706.
