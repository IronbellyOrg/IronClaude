e1bafa8877256de791a9fa834db838708d587ee9
A1 r1-1 F1.1 minor tests/observe/test_keys_spike.py:183 ac=T1.AC4 n,n,n,n resize test calls setwinsize only and never sends SIGWINCH itself; the kernel delivers it on a pty resize, pass stands
A1 r1-1 F1.2 note src/superclaude/cli/observe/view.py:5 ac=scope n,n,n,n KEY_NAMES and the Key validation go slightly past 'only the Key dataclass'; harmless
