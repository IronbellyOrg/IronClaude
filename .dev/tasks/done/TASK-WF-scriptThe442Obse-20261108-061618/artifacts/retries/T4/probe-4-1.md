ce29bcda4f5cb5efdd7b720f7e78c81cd1f36e63

# Family probe probe-4-1.md (failing review r4-1)

## family: selftest-order-partial
defect form: an AC that asserts global order but the test checks only a prefix of the sequence.
search command: grep -n -e 'order-' -e 'sent.txt' .dev/issues/442/scripts/session-a-selftest.sh
before-output (touched files):
  session-a-selftest.sh:62-68: three order edges (s1<s2, s2<s3, s3<s4) + item1 presence grep
coupled sites: session-a-selftest.sh:70-72 (presence checks), the runbook order list in the brief.
after:
  session-a-selftest.sh: one loop asserts strictly increasing positions for all 17 prompts + control strings.

## family: timeout-no-stop
defect form: a stop condition lists NEEDS_INPUT and timeout but the case arm handles only NEEDS_INPUT and notice-PENDING.
search command: grep -n -e 'NEEDS_INPUT' -e 'PENDING' -e 'TURN_END' .dev/issues/442/scripts/session-a.sh .dev/issues/442/scripts/session-a2.sh
before-output (touched files):
  session-a.sh:47-49, 57-59: case arms NEEDS_INPUT and *PENDING*
  session-a2.sh:41-43: same two arms
coupled sites: driver-helpers.sh:41-48 (TURN_END timeout output), plan line 107.
after:
  session-a.sh + session-a2.sh: TURN_END timeout arms print PENDING with the last screen file; notice-PENDING names the screen file too.

## family: a2-exit-not-sent
defect form: a runbook-prescribed /exit replaced by a terminal close, with a comment but no /exit send.
search command: grep -n -e '/exit' -e 'stop sA2' .dev/issues/442/scripts/session-a2.sh
before-output (touched files):
  session-a2.sh:45-47: stop sA2 directly, /exit removed
coupled sites: runbook line 470; session-a.sh's own /exit handling.
after:
  session-a2.sh: /exit sent with a 5s send timeout before stop.
