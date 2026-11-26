#!/usr/bin/env bash
set -u -o pipefail
R=IronbellyOrg/IronClaude
OUT=.dev/issuecleanup/b/5/work/gh
for n in 793 808 787 776 722 727 725 781 720 719 718 789 771 791 800 801 702 723 799 782 784 534 590 706 409 698 770 761 777 757 758 796 804 806 809 813 655 665 668 669 444 421 765 726 774 773 772 775 755; do
  timeout 25 gh issue view $n --repo $R --comments > $OUT/i$n.txt 2>&1 && echo "OK i$n $(wc -l < $OUT/i$n.txt)" || echo "FAIL i$n"
done
for n in 700 701 684 683 724 707 729 584 591 514 577 592 598 539 428 378 237 243 337 735 736 693 711; do
  timeout 25 gh pr view $n --repo $R --comments > $OUT/p$n.txt 2>&1 && echo "OK p$n $(wc -l < $OUT/p$n.txt)" || echo "FAIL p$n"
done
echo BATCH_DONE
