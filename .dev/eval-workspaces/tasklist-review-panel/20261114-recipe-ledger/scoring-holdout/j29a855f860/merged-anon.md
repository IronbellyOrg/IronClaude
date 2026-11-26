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
| L1 | open | yes | overlap | MAJOR | - | R3, R1, R2 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MINOR | - | R3 |
| L4 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 2 tests omit nice, time, command-without-v, and env/timeout-with-options cases that Task 1 requires, so that detection is unproven.
- anchor: "the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env`"

#### L1.t2b-1 (F2)

- claim: Whether python3.12 is blocked or allowed is left implementer-defined with no test pinning either way.
- anchor: "Versioned names such as `python3.12` are not part of issue #357 and get no test either way."

#### L1.t2b-1 (F4)

- claim: A heredoc that only writes a line starting with python3 into a file is blocked even though nothing executes it.
- anchor: "Lines of a heredoc body are scanned like ordinary lines"

#### L1.t2b-1 (F5)

- claim: No task acceptance criterion verifies the package and its artifacts are staged.
- anchor: "`.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `./artifacts/` included."

#### L1.t2b-1 (F6)

- claim: Nested quotes and escape corner cases beyond plain quoted text are neither specified nor tested.
- anchor: "Backslash escapes outside single quotes are honoured when tracking quotes."

#### L1.t3-1 (F1)

- claim: The candidate does not require reading issue #357 in full before implementation, as the source instructs.
- anchor: "Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), \"Proposed fix\" and \"Done when\"."

#### L1.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a hook that allows `echo "$(python3 x.py)"`, and that is wrong because the shell runs the bare `python3` command inside the quoted substitution.
- anchor: "Text inside single quotes, and text inside double quotes, is never a command word"
- anchor2: "A shipped PreToolUse hook on the `Bash` tool refuses any command that runs bare `python`, `python3`, `pip` or `pip3` as a command word"

## Other findings

- L2 (MAJOR, open, single): Allowing bash -c with a quoted python3 string lets the hook be bypassed by collusion the hook exists to stop.
- L3 (MINOR, open, single): Path-inequality does not prove install wrote nothing outside tmp_path, so the safety assertion is weak.
- L4 (MINOR, open, single): Sessions run from a /tmp scratch directory, where the relative artifacts path does not exist; the settings path needs an absolute form.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
