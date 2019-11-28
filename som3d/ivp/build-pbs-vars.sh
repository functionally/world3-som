#!/usr/bin/env nix-shell
#!nix-shell -i bash -p protobuf

CASE=t=5-m=5-p=300

cat header.tsv > tmp.tsv
zcat ../sensitivity-01-$CASE.tsv.gz | tail -n +2 >> tmp.tsv

N=0

for i in `seq 3 20`
do
  ((N++))
  OUT=world3-$CASE-var=$i
  echo $N $OUT
  ./make-pb-vars.awk -v frame=$N -v color=$i tmp.tsv > $OUT.pbt
  protoc --encode=Infovis.Request infovis.proto3 < $OUT.pbt > $OUT.pbb
done

rm tmp.tsv
