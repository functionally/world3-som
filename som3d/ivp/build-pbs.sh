#!/usr/bin/env nix-shell
#!nix-shell -i bash -p protobuf

N=0

for f in ../sensitivity-01-{t=5-m=5-p=30,t=5-m=5-p=100,t=5-m=5-p=300,t=10-m=5-p=30,t=10-m=5-p=100,t=10-m=5-p=300,t=20-m=5-p=30,t=20-m=5-p=100,t=20-m=5-p=300}.tsv.gz
do
  ((N++))
  OUT=${f%%.tsv.gz}
  OUT=${OUT##../}
  NAME=$(echo ${OUT##sensitivity-01-} | sed -e 's/-/ /g')
  echo $N $OUT
  zcat $f | ./make-pb.awk -v frame=$N -v name="$NAME" > $OUT.pbt
  protoc --encode=Infovis.Request infovis.proto3 < $OUT.pbt > $OUT.pbb
done
