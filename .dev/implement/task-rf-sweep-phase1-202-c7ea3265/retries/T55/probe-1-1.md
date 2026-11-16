eaffe48282629956ef0fd078e1a994737748e5a5
family=row-wording-overclaim
defect form: a sentence in the added text that claims all four R3-B3 fixtures share one property that the fourth does not have.
command: grep -n -o -F -e 'each differ from the complete-negative-join control by one input' -e 'with the shared Given' docs/designs/orchestrator-mode.md
before-output:
746:each differ from the complete-negative-join control by one input
746:with the shared Given
coupled sites: none other than the test_classify row (the Fix cycle 3 R3-B3 row, written by item 4.5, will not repeat the claim).
after:
746:each differ from the complete-negative-join control by one input
