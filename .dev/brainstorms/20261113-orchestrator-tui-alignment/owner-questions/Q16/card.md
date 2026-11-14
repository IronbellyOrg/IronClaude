# How far should the trust promise go across the three planned programs? (Q16)

## Question in one sentence
Should the project promise one shared trust design for all three planned programs, or only one shared set of permission names plus one shared audit log format, with each program checking permissions its own way?

## Why you are being asked
Three issue texts wait on this sentence: the observer dashboard issue (#409, its design decision 6 now says "Decide one design, not two."), the Orchestrator v2 issue (#423) and the workspace listener issue (Coder#477, in the separate IronbellyOrg/Coder repository). Later work also waits on it: the future trust layer, the v2 design, and the observer's planned answer screen, which must log every answer in the agreed terms. Nothing is built yet; this is a promise in issue text.

## Background you need
- "Trust" here means who may do what (for example read a status or answer a question) and how that is checked and logged.
- The three programs face different risks: the observer only reads, on one machine; the first v2 release reads only what the same user on the same machine can read; the listener would cross between separate Coder workspaces.
- A Medium-confidence (66 percent) earlier review leaned toward the narrower promise and said the point cannot be decided from documents alone.
- Signing messages does not stop harmful text being passed along; that is handled by a separate rule that relayed text stays plain typed data.
- No trust layer, permission format or signing exists today.

## Your options

### 1. One shared vocabulary and one shared audit record (recommended)
- If you pick this: #409 decision 6 becomes "Decide one grant vocabulary and one audit record."; #423 and Coder#477 promise the shared terms, not a shared design. The terms themselves are written later, in the trust-layer work, with one owner; you re-confirm when that starts.
- Upside: each program gets checks that fit its own risk; logs from all three can be read side by side; small, reversible text change.
- Downside: three mechanisms to review; the same word could mean weaker protection in one program unless each term says what it enforces.

### 2. Promise nothing yet (the default)
- If you pick this: #409 keeps "Decide one design, not two."; #423 and Coder#477 say nothing about trust; later trust work stays on hold.
- Upside: no new promise before a design exists.
- Downside: #409 still promises one design while the others say nothing, so the issues disagree; the held work waits on a step that itself waits on this answer.

### 3. One trust design for all three
- If you pick this: the permission format and checking chosen under #339 (the Orchestrator mode issue) become the only ones; #409 keeps its sentence; #423 and Coder#477 say they use it and define no second format.
- Upside: one thing to build and test; one owner; no translation between programs later.
- Downside: the spec lists one trust design as out of scope; one design either over-builds the read-only observer or under-protects the listener; it can give a false sense of safety.

## What the debate found
- All three debaters, including the ones arguing for options 2 and 3, judged option 1 best (65 to 70 percent).
- The spec itself says only the shared vocabulary and audit format are "in reach".
- The default (option 2) is not neutral: it leaves a one-design promise in #409.
- Option 1 was strengthened with option 3's single owner and option 2's "ask again when a real design exists".

## Recommendation and confidence
Option 1, 70 percent.

## If you do not answer
The default applies: #409 decision 6 is left unchanged, #423 and Coder#477 promise nothing about trust, and the trust-layer, v2 design and observer answer-screen work that needs the shared terms stays on hold.

## What this answer does not authorize
It does not authorize passing knowledge between agents (relay), any issue edit by itself (edits still go through the single editor and their own permission), or any code.

## How to answer
Type: "Q16: option 1" (or "Q16: option 2" or "Q16: option 3").
