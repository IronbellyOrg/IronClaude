b3c21a415583c468199eee92fb9c6c38b18a744c
A1 r1-1 F1.1 note tests/sweep/conftest.py:222 ac=scope amiss:n,false:n,harm:n,constraint:n The `package` builder appends the FINAL line to the ledger text without a newline, so a ledger text that does not end in a newline plus final=True puts FINAL: on the same line and the reader sees no FINAL line; later tests must pass newline-terminated ledger text.
