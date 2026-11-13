#!/bin/bash
E=$PWD
for P in TASK-WF-designSpec-20261107-075614 TASK-WF-makeTheAliasOnly-20261105-051649 TASK-WF-design-20261108-041415; do
 for d in $E/$P/reviews/combos/*; do
  r=$(basename $d)
  case "$r" in *contaminated*|*superseded*) continue;; esac
  case "$r" in *-src|b4-*|sol-alone-src|terra-alone-src|*-ember) ;; *) continue;; esac
  for m in $d/*.meta.json; do
   case "$m" in *attempt*) continue;; esac
   id=$(basename $m .meta.json)
   md=$d/$id.md
   mod=$(jq -r .expected_model $m); ok=$(jq -r .model_ok $m)
   tok=$(jq -r .total_output_tokens_all $d/$id.cost.json 2>/dev/null); w=$(jq -r .total_wall_s $d/$id.cost.json 2>/dev/null)
   nb=$(grep -cE '"blocking" *: *true' $md); nt=$(grep -cE '"blocking" *:' $md)
   echo "$(echo $P | cut -d- -f3)|$r|$id|$mod|$ok|$tok|$w|$nb|$nt"
  done
 done
done
