#!/bin/sh
# this uses a file with start, end locations of a partition (partitions-st-end.txt) to produce a nexus file with each codon position for that file

if [ -z $1 ]; then
  echo "Please enter the amas partition file as the program argument and this program will convert it into a nexus partition file separated by position in each codon."
  exit 1
fi

AMASPART=$1

part=1
echo "#NEXUS"
echo "BEGIN SETS;"
sed -r 's/.*=(.*)-(.*)/\1 \2/' $AMASPART | \
while read line; do
  start=`echo $line | awk '{print $1}'`
  end=`echo $line | awk '{print $2}'`
  echo "CHARSET p${part}a = $start-$end\\3;"
  echo "CHARSET p${part}b = $((start+1))-$end\\3;"
  echo "CHARSET p${part}c = $((start+2))-$end\\3;"
  part=$((part+1))
done
echo "END;"
