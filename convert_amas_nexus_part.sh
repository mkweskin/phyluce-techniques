#!/bin/sh

if [ -z $1 ]; then
  echo "Please provide the amas partition file to be converted to a nexus file"
  exit 1
fi

INPUT=$1

if [ ! -f ${INPUT} ]; then
  echo "Input file was not given or was not found"
  exit 1
fi

BASENAME=`basename ${INPUT}`
DIRNAME=`dirname ${INPUT}`

cp ${DIRNAME}/${BASENAME} ${DIRNAME}/${BASENAME}.temp
sed -i -r 's/^/charset /' ${DIRNAME}/${BASENAME}.temp
sed -i -r 's/$/;/' ${DIRNAME}/${BASENAME}.temp
echo "#nexus" > ${DIRNAME}/${BASENAME}.nex
echo "begin sets;" >> ${DIRNAME}/${BASENAME}.nex
cat ${DIRNAME}/${BASENAME}.temp >>${DIRNAME}/${BASENAME}.nex
echo "end;" >> ${DIRNAME}/${BASENAME}.nex
rm ${DIRNAME}/${BASENAME}.temp

echo "Converted file: ${DIRNAME}/${BASENAME}.nex"
