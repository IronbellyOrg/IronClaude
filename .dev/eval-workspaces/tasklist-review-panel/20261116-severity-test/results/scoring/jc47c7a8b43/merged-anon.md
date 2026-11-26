review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 5ba3dd1b87812b97fc608d17f1239f6174666865cc155021598afc760282dc1c
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R3 |
| L2 | open | yes | overlap | MAJOR | - | R3, R1 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MINOR | - | R3 |
| L5 | open | yes | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1-fixture)

- claim: Task 4 never updates fake_source_hooks, so _copy_scripts fails on the missing fake block-bare-python.sh and the Task 4 pytest acceptance cannot pass.
- anchor: "`test_install_hooks_installs_and_registers_block_bare_python`: call `install_hooks(target_path=tmp_path / \".claude\" / \"settings.json\")` against the real packaged sources"

### L2

#### L2.t2b-1 (F2-bashc)

- claim: Allowing bash -c "python3 ..." lets a real bare python3 execution through, contradicting the goal and Done-when text-only exemption.
- anchor: "`bash -c \"python3 ...\"` are not blocked"
- anchor2: "refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

#### L2.t3-1 (F1)

- claim: Allowing quoted code passed to `bash -c` lets a bare `python3` execute, contrary to the goal of blocking commands that run bare Python command words.
- anchor: "Text inside single quotes, and text inside double quotes, is never a command word (so commit messages, `echo \"python3 ...\"`, `grep 'pip install'` and `bash -c \"python3 ...\"` are not blocked)."

#### L2.t3-1 (F2)

- claim: The constraints assign the live-session check to Task 6, while Task 6 is the changelog and Task 7 specifies the fresh-session proof.
- anchor: "The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file"
- anchor2: "## Task 6: Add the changelog entry"

#### L2.t3-1 (F3)

- claim: The driving document requires reading issue #357 in full first, but the candidate does not state that prerequisite.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

### L5

#### L5.t4-1 (F1)

- claim: The allowed nested-shell command runs bare python3, bypassing the hook's stated block.
- anchor: "bash -c \"python3 x.py\""

## Other findings

- L3 (MAJOR, open, single): Fresh-session proof depends on the model emitting the exact command verbatim, so the acceptance evidence is nondeterministic.
- L4 (MINOR, open, single): Artifact paths are not anchored to a working directory (repo root vs task package dir).

## Reviser brief

Blocking finding ids: L1, L2, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
