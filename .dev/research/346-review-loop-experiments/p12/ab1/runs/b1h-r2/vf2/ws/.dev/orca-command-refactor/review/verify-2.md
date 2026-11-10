# Verification of finding N5 against the candidate spec

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (294 lines, sha256 `feaa1a31e42a8514d14628b790b646be58d5aee3914f33cd26e8e8f6a0037350`).

| id | found text | exists | outcome follows | verdict | reason |
|---|---|---|---|---|---|
| N5 | :60 (WC-2): "Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer, and never says STOP AND WAIT." | yes | no | reject | The contradiction is real, but the stall is not forced by the candidate. |
| N5 | :159 (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate), except that auggie-review, task, pr-submit and post-release refuse it" | yes (tdd, release-split and troubleshoot rows sit in section 3.1, lines 78-93) | no | reject | Same as above: the flag is accepted on gated commands in P1, while WC-2 forbids prompting under the flag. |
| N5 | :73 (section 2.3): "the exact command line, including `--unattended` from P1 on" | yes | no | reject | Establishes the P1 dispatch, but nothing in 2.3 makes the brief carry a bare topic. |
| N5 | :90 (tdd row): input "a precise component prompt, not a bare topic"; gate "the topic-only clarification and nested `/task` 'ask the user' lines resolve as blocked (P2)" | yes | no | reject | The example dispatch `/sc:tdd "<topic>" --unattended --output <file>` uses a bare topic, which the same row names as the wrong input. With a precise prompt the topic-only clarification does not fire by the candidate's own wording. The nested `/task` ask lines are not stated to fire on a compliant run, so the stall needs a further assumption. |
| N5 | :104 (cli-eval row): "the W0 'confirm with the user' and missing-`$1` cases resolve as blocked"; the finding's "suite menu" wording is not in the candidate. `inventory/commands-a.md:44` is cited but is not in the workspace. | candidate text yes; inventory citation no (UNVERIFIED) | no | reject | The gate exists at :104, but the candidate ties it to the `run` input and missing `--suite`, which a compliant brief supplies. |
| N5 | Other gate rows the finding lists: :89 release-split, :91 troubleshoot (`--depth deep` STOP), :105 cli-portify, :115 recommend, :117 review-translation, :118 roadmap ("Resume? [Y/n]", P3), :120 spec-panel | yes (each row exists as described) | no | reject | Each fires only on an input or state the candidate does not make certain for a compliant brief, so none is a separate confirmation. |

Summary: the two texts that the finding names as contradictory (:60 and :159) both exist as quoted, and the contradiction holds. The stated concrete stall, however, depends on a bare-topic dispatch to `/sc:tdd` (or an equivalent gate trigger) that the candidate does not require for a compliant brief, so the outcome does not follow with no further assumption.

confirmed: none
