8e0aa4769daecdba07cac3080bf79ea32da9019b
A1 r1-1 F7.1 minor tests/unit/test_ccsession_tag.py:1797 ac=scope n,n,n,n the typed-ahead test does not check that the typed text is still waiting for Claude; the behaviour is right.
A1 r1-1 F7.2 minor tests/unit/test_ccsession_tag.py:2631 ac=T7.AC1 n,n,n,n the 245/246-byte CCSESSION_NAME test checks the topic, not Claude's arguments.
A1 r1-1 F7.3 minor tests/unit/test_ccsession_tag.py:2697 ac=scope n,n,n,n the terminal and no-terminal runs share one record.json (also :2666); a second launch that never started Claude would go unnoticed.
