2ad80469c7ea3f12d6194a87dba18e6f48b95577
A1 r1-1 F1.1 note tests/vcs/test_resolution.py:1197 ac=T18.AC1 n,n,n,n the settled-state test compares two resolve-check outputs byte for byte but reads the reconcile row only once (fix: call reconcile twice and compare); byte identity of reconcile is covered by tests/vcs/test_contract.py:575.
