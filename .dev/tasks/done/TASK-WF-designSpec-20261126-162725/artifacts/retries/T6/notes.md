c44fc2899c2e2af9f55804273ad294cab0302ec6
A1 r1-1 F1.1 note .dev/research/jev-vs-keyword-table-611/harness/runner.py:32 ac=scope n,n,n,n runner.py does not import TransportError, which the brief's import list names; nothing in the runner needs it (the client catches it) and an unused import would fail the linter.
