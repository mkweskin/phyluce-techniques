#!/bin/sh

# Converts SWSC output to nexus formatted partitions for input into IQTREE

echo "Converts the .cfg output from SWSC to a nexus partition file for use in
IQTREE or raxml"

input=${1}

if [ -z $input ] || [ ! -f $input ]; then
  echo "Input file not given as a parameter or file not found"
  exit 1
fi

echo "Input: $1"


echo "#nexus" > partitions.nex
echo "begin sets;" >> partitions.nex
grep -E '_[left|core|right|all]' ${input} >> partitions.nex
sed -i 's/uce-/charset uce-/' partitions.nex
echo "end;" >> partitions.nex
uniq partitions.nex > partitions-uniq.nex
mv partitions-uniq.nex partitions.nex

echo "Output: partitions.nex"
echo "Done"
