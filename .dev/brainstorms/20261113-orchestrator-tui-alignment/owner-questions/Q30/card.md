# Which coordinator may the questions-panel test read?

## Question in one sentence
For the one live test of the observer's questions panel, which coordinator's work may it read, and do you accept in writing that questions there might be lost?

## Why you are being asked
The observer (`superclaude observe`, the read-only dashboard of Orca workers) has a panel that shows questions workers send to their coordinator. It is switched off. Switching it on needs one live test in a real coordinator's terminal. Nobody has proved whether the panel's read removes questions from the coordinator's mailbox, so the test could make a question vanish.

## Background you need
- In Orca, a Run is one coordinated piece of work. A coordinator is the Claude session you open to hold a Run and direct its workers.
- Only the terminal that holds a Run can read its questions (a test on 2026-11-11 showed this), so the test must run in the coordinator's own terminal.
- Orca's help text says the panel's read "does not mark read", but nobody has tested it on a live coordinator (open, estimated 61 percent).
- An earlier step tests a throwaway Run with planted messages first. It cannot show what happens with a live coordinator that is waiting for questions and confirming answers.
- The program's own coordinator must never be the test subject: losing its workers' questions would break the program.

## Your options

### 1. A throwaway coordinator you open just for the test (recommended)
- If you pick this: after the planted-message test passes, you open a test coordinator and start one test worker that asks one known question. While the question is unanswered, the panel reads it. Loss is judged by whether that known question still reaches the coordinator. Then everything is closed.
- Upside: real waiting and confirming behaviour, and nothing of value can be lost.
- Downside: setup work (a test coordinator, a worker and its worktree), and Orca must be up.

### 2. A real coordinator from your other work, at a quiet moment
- If you pick this: the panel reads a coordinator you are already running for something else, when no worker is waiting.
- Upside: the most realistic test; no setup.
- Downside: a real question could be lost; the spec's own rule says the Run must carry no work whose questions matter; and a quiet moment means no question is pending, so the test shows little.

### 3. No live test for now
- If you pick this: the test is held and the panel stays off.
- Upside: nothing can be lost.
- Downside: the questions panel never ships while this holds.

## What the debate found
- All three advocates chose option 1, including the two assigned to the other options.
- They found one flaw in option 1 as first written: the question must still be unanswered when the panel reads, or the test proves nothing.
- Checking for a lost question with a plain read would itself remove messages, so loss is judged against the known test question.

## Recommendation and confidence
Option 1, and yes, accept that questions in the throwaway Run may be lost. Confidence 85 percent.

## If you do not answer
Option 3 applies: the live test is held and the PR that switches the panel on is not opened.

## What this answer does not authorize
Binding the observer to any other Run (`run-use`); reading any Run other than the one you name; reading the program's own coordinator; or switching the panel on (a separate PR with its own approval).

## How to answer
"Q30: option 1, and yes, I accept that questions in the test Run may be consumed" (or "Q30: option 2" with the Run id, or "Q30: option 3").
