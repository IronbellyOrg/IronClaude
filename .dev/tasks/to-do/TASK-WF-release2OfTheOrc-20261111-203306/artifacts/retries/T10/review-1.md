578416f74dd1a207745a4e5a09b5cb040cce71a0 tree=5d5c60a38b540168956369c09436e4e6bf8e66f5
T10.AC1 met @ tests/observe/test_render.py:442 (T47 byte-identity unproven, F1.1)
T10.AC2 met @ tests/observe/test_view.py:1044
F1.1 sev=blocking trigger=B1 ac=T10.AC1 at=tests/observe/test_render.py:492 anchor="T47 with questions off is byte-identical to release 1 output" chk=y,n,n,n family=t47-byte-identity fix=compare against a frozen release-1 reference first=A1 origin=new: the T47 tests compare the new code with itself
F1.1 resolved
