#!/bin/sh
# this uses a file with start, end locations of a partition (partitions-st-end.txt) to produce a nexus file with each partition being a separate CODON type partition

if [ -z $1 ]; then
  echo "Please enter the amas partition file as the program argument and this program will convert it into a nexus partition file separated by codon"
  exit 1
fi

AMASPART=$1

part=1
echo "#NEXUS"
echo "BEGIN SETS;"
sed -r 's/.*=(.*-.*)/\1/' $AMASPART | \
while read line; do
  pos=`echo $line | awk '{print $1}'`
  echo "CHARSET p${part} = CODON, $pos;"
  part=$((part+1))
done
echo "END;"
