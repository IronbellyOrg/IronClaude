578416f74dd1a207745a4e5a09b5cb040cce71a0
family: t47-byte-identity (a test claims byte-identity with release 1 without release 1 bytes)
cmd: grep -n -F -e byte-identical -e golden_release1 -- tests/observe/test_view.py tests/observe/test_render.py
coupled sites: test_view.py T47 test (self-comparison), test_render.py T47 screen test
before:
tests/observe/test_render.py:611:# -- T47: questions off is byte-identical to release 1 (against release 1's o
tests/observe/test_render.py:618:        (Path(__file__).parent / "golden_release1_surface.json").read_text(
after:
tests/observe/test_render.py:611:# -- T47: questions off is byte-identical to release 1 (against release 1's o
tests/observe/test_render.py:618:        (Path(__file__).parent / "golden_release1_surface.json").read_text(
