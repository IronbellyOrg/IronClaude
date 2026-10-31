038aeed101ea35b2e5bdf1218cf7992eded2e970
A1 r1-1 F1.2 minor tests/pr_submit/test_codex_reviews.py:355 chk=n,n,n,n section 16 item 5 leak test builds a direct DetectionContract with empty Codex identities, so it does not exercise the leak check with Codex enabled
A1 r1-1 F1.3 note tests/pr_submit/test_codex_reviews.py:251 chk=n,n,n,n augment presence ignores a lone thread root; matches the Augment-unchanged rule of design section 5
A1 r1-1 F1.4 note tests/pr_submit/test_codex_reviews.py:417 chk=n,n,n,n A4 docstring says resume reads watermarks; the test computes the watermark dict itself
