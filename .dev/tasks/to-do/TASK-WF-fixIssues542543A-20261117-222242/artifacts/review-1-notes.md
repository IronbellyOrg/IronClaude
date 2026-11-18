# Review round 1 (Augment, PR #625)

Finding (medium, tests/cli/test_ic_launcher.py:109): the plan's Task 1 said `-p --help` must give exit 2 and the
unknown-preset message, but the test only covered `-H --help`.

Verified: `ic -p --help` exits 1 with Bash's "IC_PRESET_--help: invalid variable name" (pre-existing: apply_preset
builds a variable name from the preset argument). That is not the exit 2 the plan promised, so the plan sentence is
inaccurate for `-p`. Changing preset-name validation is outside #544, so the script is not changed.

Fix: tests now cover `-p/--preset --help` (not help, no launch, non-zero) and every value option (`-H -S -O` and long
forms) taking `--help` as its value. Mutation check: with the option-value skipping removed from the help pre-scan,
8 of these tests fail (.dev/issues/.../mutation-skip-removed.log), with it they pass.
The plan file is left unchanged (its hash is pinned in progress.md); this note records the deviation.
