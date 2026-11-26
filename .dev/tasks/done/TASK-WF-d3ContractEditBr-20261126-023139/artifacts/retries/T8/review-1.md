5e8802f5ce80ba3325b2f1f6b58da66952dcc29f tree=afa8dbe320dd58d930465b6ef994323fb182720e
T8.AC1 met tests/skills/test_confirmation_channels.py:63-115
T8.AC2 unmet F1.1 tests/skills/test_confirmation_channels.py:79
F1.1 sev=blocking trigger=B1 ac=T8.AC2 at=tests/skills/test_confirmation_channels.py:79 anchor="The test fails when the timing safeguard sentence or any nothing-else item is removed" chk=y,n,n,n family=mutation-check-coverage fix=check the nothing-else items against the "What never counts" line only and mutate that line for every item first=A1 origin=new: the mutation check skips "another agent's message" (it also sits at WORKER-CONTRACT.md:57) and presence is tested against the whole file, so removing an item from the list line alone can leave the test green.
