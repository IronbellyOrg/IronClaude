# How should this workspace get the new sweep command?

## Question in one sentence
Once PR #539 is merged, should this workspace's `superclaude` command get the new sweep command through the Coder template or through a one-time reinstall you approve?

## Why you are being asked
The coordinator session is meant to run `/sc:sweep` (a read-only report on its workers), and one later test (the join comparison between the observer and the sweep) needs it. The installed command does not have the sweep yet, and your rule says updates reach workspaces only through the Coder template.

## Background you need
- The Coder template (`IronbellyOrg/Coder`) builds the workspace image and pins which IronClaude commit it installs. A daily workflow opens a PR to bump that pin when IronClaude master moves; after that PR is merged, the image is rebuilt and each workspace is updated.
- This workspace has two copies of the command (checked 2026-11-14): the image copy in `/usr/local/bin`, and a second copy in `/home/coder/.local/bin` installed by hand on 2026-11-12 at 22:12 (who installed it is unknown). The second copy comes first, so it is the one that runs.
- `/home/coder` survives template updates. So a template update alone would not change which copy runs here.
- A workspace update builds a new container, which ends running sessions.

## Your options

### 1. Coder template, then remove the extra copy (recommended)
- If you pick this: after the merge, start the Coder pin-bump workflow by hand, merge its PR, update the workspace between sessions, then approve removing the copy in `/home/coder/.local/bin`. The coordinator then checks that the sweep runs.
- Upside: follows your update rule; every workspace runs the same reviewed version.
- Downside: takes longer (a Coder PR, an image build and a workspace update); the update ends running sessions.

### 2. A one-time reinstall on this workspace
- If you pick this: after the merge, you approve reinstalling the command in `/home/coder/.local/bin` at the exact merge commit; you remove it later, when the template catches up.
- Upside: working within minutes; no restart.
- Downside: an exception to your update rule; this workspace runs a different version from the others until the clean-up.

### 3. Decide later
- If you pick this: the sweep is recorded as "not runnable" and the join test waits; you are asked again when that test is next.
- Upside: nothing changes now.
- Downside: the template cannot fix this workspace on its own because of the extra copy, so the question comes back unchanged.

## What the debate found
- Two of three advocates chose option 1; the third preferred option 2 for speed.
- All three agreed the extra copy in `/home/coder/.local/bin` has to go at some point, and that the check must run in the coordinator's own session.
- The spec's recommended route (the template alone) would not work on this workspace without removing that copy.

## Recommendation and confidence
Option 1. Confidence 70 percent.

## If you do not answer
Option 3 applies: the sweep duty is recorded as "not runnable" and the join comparison (XC-04) waits.

## What this answer does not authorize
Running the sweep more often than once per 5 minutes; any write by the sweep beyond its one report; a merge of PR #539; or changes to other workspaces beyond the normal template update.

## How to answer
"Q29: option 1, and yes, remove the extra copy after the update" (or "Q29: option 2", or "Q29: option 3").
