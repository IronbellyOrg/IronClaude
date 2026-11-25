DRAFT, not posted. For IronbellyOrg/IronClaude issue 691. Posts only after the owner reads it and says go.

## Live check of Part B: a real claim left the result file

A live OB-H2 observation ran on 2026-11-21 from 02:32 to 03:36 UTC against disposable test issue 712 (a throwaway issue made for this run).

**What the claim left behind.** The claim of issue 712 at 02:57:07 UTC wrote `.dev/issues/712/launch-result.json` in the main checkout: 1269 bytes, status `launched`, enforcement hook `installed`, two layer status lines and the release text. It is identical to the launch output the claim printed.

**What the Part B scripts did with it.** They read only that file. The observation log shows:
- `OK b-layers L1 guard: effective (read from launch-result.json)`
- `OK b-launched terminal=term_7e3d9c61-9baf-4221-beda-01f49ca9753a gsid=792d0d5a-f126-48d1-9d4a-179ff6ad8cb1`
- `OK b-inode session file ... holds inode 39845895, equal to the claim's 39845895; link count 1`
- `OK release 792d0d5a-f126-48d1-9d4a-179ff6ad8cb1`
- The refusal cases (unreadable file, missing hooks, approved without unlock, ids of other sessions, a released context) were refused as designed.

**Not covered.** `shellcheck` is not installed here, so it was not run. The edge case of a result file written in the same second the claim started was not tested.

**Where the raw files are.** The run folder `/tmp/ob` is temporary and will be cleaned up by the session that owns the run, so the lines above are quoted here.

With Part A (PR 693) and Part B (PR 709) merged and this run, every item in the issue's Done when list is met.
