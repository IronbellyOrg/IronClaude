1fd69f04fe7dc34cd2fc82e8c5f168276f3cda7a
## family import-allowlist
defect form: a module import outside the Constraints module list in the kernel script (and a test allow set that admits it)
command: grep -n -e __future__ src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py tests/skills/test_review_ledger_script.py
before:
src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py:19:from __future__ import annotations
tests/skills/test_review_ledger_script.py:9:from __future__ import annotations
tests/skills/test_review_ledger_script.py:375:        "__future__",
coupled sites: the test allow set at tests/skills/test_review_ledger_script.py:375 (the test file's own __future__ import is not the script and is out of scope)

## family integrity-order
defect form: a subcommand reads its input, report or the lock before the ledger hash check
command: grep -n -e read_input( -e ledger.lock() -e "state = ledger.load()" src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py
before:
236:def read_input(path_str: str) -> tuple[object, bytes]:
404:    fh = ledger.lock()
406:        state = ledger.load()
497:    fh = ledger.lock()
649:    data, payload = read_input(args.input)
790:    state = ledger.load()
coupled sites: cmd_close checks the report file before mutate (report-not-found refusal); cmd_find reads input before mutate; mutate takes the lock before the load

## after (A1 fix pass)
family import-allowlist after:
tests/skills/test_review_ledger_script.py:9:from __future__ import annotations
(the script line is gone; the test allow set no longer lists __future__; the test file's own import is not the script)
family integrity-order after:
234:def read_input(path_str: str) -> tuple[object, bytes]:
400:    ledger.load()  # E-NO-LEDGER or E-TAMPERED before anything else is read or locked
402:    fh = ledger.lock()
404:        state = ledger.load()
495:    fh = ledger.lock()
651:        got["data"], got["payload"] = read_input(path_str)
802:    state = ledger.load()
(mutate checks the hash at :400 before read_payload and the lock; find/close read their input inside read_payload; init (:495) has no existing ledger to check; :802 is status, read-only)
