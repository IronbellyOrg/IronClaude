# A2 approach (implementer claims)
- Built driver.sh + driver-helpers.sh (Task 3): send with three stop conditions, wait-notice, answer, NEEDS_INPUT.
- A2 fix pass switched the screen parse to result.terminal.tail (F3.1) and rewrote notice_answered to require a <task-notification> prompt between Stops (F3.2).
- Believed AC4 met: driver-selftest.sh:75-91 shows both notice cases passing (verified live by the reviewer against the stub).
