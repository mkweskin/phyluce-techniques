#!/bin/sh
if [ -z $1 ]; then
  echo "ERROR: Give the name of the nexus file as a program argument"
  echo "Example: $0 raxml/mafft-nexus-min-70per-taxa.nexus"
  exit 1
fi

if [ ! -f $1 ]; then
  echo "ERROR: input file not found"
  echo "  $1"
  exit 1
fi

echo "Making phylip file from nexus"
echo 
echo "Note: this conversion works for this nexus file output by phyluce, but it may not work on other nexus files."
echo "Removing non-sequence lines"

# get the input name without the extension
NAMENOEXT=${1%.*}

# Note: this conversion works for this nexus file output by phyluce, but it is not a generalizable method
grep -E -v "charpartition|NEXUS|begin|end|matrix|charset|datatype|^;" $1 >$NAMENOEXT.phy
# converting the dimensions line to a phylip format line with number of taxa and sites
sed -i -r 's/.*ntax=([0-9]+).*nchar=([0-9]+).*/\1 \2/g' $NAMENOEXT.phy

