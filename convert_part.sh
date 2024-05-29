#!/bin/bash
# Convert IQTREE partition names so they aren't so long

if [ -z $1 ]; then
  echo Give the name of the nexus partition file as the script argument
  exit
fi

# Extract all the lines with "charsets" into a new file:
grep -i charset ${1} >convert-in

# From the "charsets" line, just leave the original partition name
# The partition name is exepcted after "charset" and before "="
sed -r -i 's/.*charset *(.*) *=.*/\1/' convert-in

# Make a backup of the original best_scheme file
cp -a ${1} ${1}.bak

# Do the conversion
# Loop through the file with the old names, doing a substitution for each line
# The substitution looks for the original name (followed by any number of spaces
# or equal signs, semicolons or commas) and replaces with the current
# value of a counter ${PART}
PART=1
while read line; do
  sed -i -r "s/${line}([ =,;]+)/part${PART}\1/" ${1}
  PART=$((PART+1))
done < convert-in

rm -f convert-in
