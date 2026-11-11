# T1 spike: Rich Live plus stdlib key reader

Run: `uv run pytest tests/observe/test_keys_spike.py -v` gave `12 passed in 8.67s`; two more runs gave `12 passed in 8.68s` and `12 passed in 8.97s`. Python 3.11.15, Rich 15.0.0, pexpect 4.9.0, pytest 9.2.0, Linux 6.8.0 (pty from pexpect). Pass or fail below is the automated result only.

| Criterion | Result | Test |
|---|---|---|
| Lone Escape decoded as `escape`, Up-arrow sequence as `up` (also Down, and the application-mode `ESC O A` form) | pass | `test_lone_escape_and_arrow_sequences_are_told_apart` |
| 20 keystrokes sent during repainting arrive in order, none lost; at least 5 repaints during the burst | pass | `test_burst_of_keys_is_received_in_order_while_repainting` |
| Terminal attributes identical before start and after exit: normal exit on `q` | pass | `test_terminal_attributes_restored[q]` |
| ... SIGINT | pass | `test_terminal_attributes_restored[sigint]` |
| ... SIGTERM | pass | `test_terminal_attributes_restored[sigterm]` |
| ... SIGHUP | pass | `test_terminal_attributes_restored[sighup]` |
| ... exception raised inside the loop | pass | `test_terminal_attributes_restored[exception]` |
| SIGTSTP then SIGCONT: original attributes while the child is stopped, cbreak mode active again with a repaint after SIGCONT | pass | `test_sigtstp_restores_terminal_and_sigcont_reenters_cbreak` |
| Pty resize (`setwinsize` plus SIGWINCH): repaint with the new size within 1 s | pass | `test_resize_repaints_with_the_new_size_within_one_second` |
| Non-tty descriptor: `KeySource` unavailable, no exception | pass | `test_non_tty_descriptor_is_unavailable_without_raising` |

Notes:

- SIGTSTP stops the child with SIGSTOP after restoring the terminal. A process group started by pexpect is orphaned, and an orphaned group ignores the default SIGTSTP action, so SIGSTOP is what makes the stop observable. A real shell sees the same stopped state.
- Ctrl-C reaches the child as SIGINT (ISIG kept), so the decoder's `ctrl_c` key is covered by a decoder unit test, not by the pty test.
- "No visible flicker" was not automated and is UNVERIFIED. It needs a human watching a real terminal.
- The Textual fallback (AD-14) was not built or tried.

Decision: every automated criterion passed, so continue with Rich `Live(screen=True)` and the stdlib `KeySource`. Textual is not added.
