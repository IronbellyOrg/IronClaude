4874fd7e0861dfa267ea57f5d7198aaeb6b225ea
## family control-assert (probe for r1-1)
defect form: a control test does not assert a named outcome of the AC
command: grep -n status_read tests/sweep/test_git_config_hole.py
before: <no hits>
coupled sites: tests/sweep/test_git_config_hole.py:207-218 only
## family integration-mark (probe for r1-1)
defect form: the integration mark is not module-level
command: grep -nE '^pytestmark|@integration' tests/sweep/test_git_config_hole.py
before: 100:@integration 112:@integration 126:@integration 139:@integration 153:@integration 172:@integration 189:@integration 206:@integration 235:@integration 249:@integration 
coupled sites: conftest autouse guard reads only function-level marks (tests/sweep/conftest.py:30-32), so the per-test decorators stay and a module-level line is added
after: 222:    assert state.status_read is True  # the status was read, so the branch was parsed 
after: 20:pytestmark = integration 22:# test also carries ``@integration``. 103:@integration 115:@integration 129:@integration 142:@integration 156:@integration 175:@integration 192:@integration 209:@integration 239:@integration 253:@integration 
