# IR-7 consequence: a missing L2 layer is a warning, not a refusal

## What was built

IR-7 is implemented as a warning. When `l2_status()` in
`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` returns
`absent` (the worktree has no executable file at git's `hooks/pre-push` path),
`cmd_launch` adds the warning `W-L2-ABSENT` with its reason to the launch
result and the launch goes ahead: the agent is started, the pending record is
written and the status stays `launched`. The remedy line says the L2 layer is
not built yet and the limits are enforced by the L1 guard only.

The claim looks for no owned-hook marker and no contract marker, and it never
creates, edits or adopts a hook file. A pre-push file that is already there
gives `present-unverified` and no warning, and stays byte-identical.

The IR-4 refusal of Task 18 (guard missing or not effective gives
`W-ENFORCEMENT-ABSENT` and no launch) is unchanged.

## What the design says

Design section 13, IR-7: when the owned L2 installation is absent, the claim
"reports W-L2-ABSENT and refuses that governed launch". Design section 19.2
says the same: "do not launch a governed pipeline advertised as protected when
accepted L2 is absent". So the design text says refuse, and this code does not.

## Why a warning

This plan builds no L2 artifact (Task 21 records that). With a refusal, `l2_status()`
would return `absent` for every worktree, so every governed claim
(`--pipeline worktree` and `--pipeline full`) would be refused. The launch
feature would be switched off, and nothing could ever start, which also makes
the OB-H2 observation impossible: it needs a real governed launch.

Ownership cannot be checked either: no owned L2 hook exists to compare
against, and design section 19.2 says "a header alone is not sufficient
ownership proof". So `present-unverified` means only "some executable hook is
there", never "protected".

The owner was asked and had not answered when work began; the warning is the
default taken (owner option b) and the owner can change it.

## The one-line change that makes it a refusal

When the L2 plan ships, in `cmd_launch` (the same function, before
`publish_pending`, so a refusal writes no pending record and starts no agent),
directly after the line

```python
l2_notes = [("W-L2-ABSENT", L2_ABSENT_WHY)] if l2 == "absent" else []
```

add the one line

```python
if l2_notes: return emit(launch_result("failed", l2_notes, enforcement_hook=hook))
```

That line is already written as a comment just above them in the code. That L2
plan also has to replace `l2_status()`'s plain "is there an executable file"
test with a check of the exact owned version and content (design section 19.2),
reword `REMEDY["W-L2-ABSENT"]` and the claim.md and SKILL.md rows (they say the
agent was started), and turn
`test_ir7_l2_absent_warns_and_the_launch_proceeds` into a refusal test.
