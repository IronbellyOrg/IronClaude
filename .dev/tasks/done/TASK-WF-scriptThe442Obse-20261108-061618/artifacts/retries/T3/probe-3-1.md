e42b6fad93894e7144df9bd08a9a35a06d6c5e93

# Family probe probe-3-1.md (failing review r3-1)

## family: screen-shape
defect form: a jq filter written against an imagined CLI output shape; the self-test stub reinforces the wrong shape.
search command: grep -n -e '.screen' -e '.content' -e '.result.terminal' .dev/issues/442/scripts/driver-helpers.sh .dev/issues/442/scripts/selftest.sh
before-output (touched files):
  driver-helpers.sh:13: screen_json_field filter '.screen // .content // ""'
  driver-helpers.sh:63-65: needs_input reads the same filter
  selftest.sh:29-30: stub emits {"screen": ...}
coupled sites: driver-helpers.sh:16-21 (screen_block_count), driver-helpers.sh:63-70 (needs_input), selftest.sh stub 'terminal read' arm.
after:
  driver-helpers.sh: filter is '.result.terminal.tail // [] | join("\n")' everywhere; screen_block_count counts Blocked: lines over the joined tail.
  selftest.sh: stub read arm emits {"result":{"terminal":{"tail":[...]}}} with the screen text as an array element.

## family: notice-vacuous
defect form: an awk guard whose trigger variable is compared with a condition that is always true (n_in >= 0 after initialization to -1 only when unset).
search command: grep -n -e 'n_in' -e 'task-notification' .dev/issues/442/scripts/driver-helpers.sh
before-output (touched files):
  driver-helpers.sh:53-61: notice_answered awk program
coupled sites: driver-helpers.sh:23-31 (the wait_turn notice branch), driver-selftest.sh:75-85 (the two wait-notice cases pass vacuously).
after:
  driver-helpers.sh: notice_answered rewritten: awk counts prompt events strictly between Stop stop_before+1 and the last new Stop and requires a prompt containing <task-notification>; probed with Stop,Stop (no prompt) => returns 1; Stop,prompt(task-notification),Stop => returns 0.
  driver-selftest.sh: adds a negative case (Stop, non-notice prompt, Stop) that must time out to PENDING.
