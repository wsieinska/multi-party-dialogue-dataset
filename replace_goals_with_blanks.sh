#!/bin/bash
#
# This script creates dialogue files where goal annotations are
# replaced with blanks.
#
# Input:
#     - ./dialogues/dialogue_**.txt (35 files)
#
# Output:
#     - ./dialogues-with-blanks/dialogue_**.txt (35 files)
#
######################################################################

echo "Replacing..."

rm -rf dialogues-with-blanks; mkdir dialogues-with-blanks

for infile in ./dialogues/*.txt; do
	basename=$(basename ${infile})
	outfile="./dialogues-with-blanks/${basename}"

	cat ${infile} | while read l; do
	        l_with_blank=$(echo "${l}" | sed 's/@.*$/@[BLANK]$/g')
		echo "${l_with_blank}" >> ${outfile}
	done
	echo "Created file: ${outfile}"
done

echo "Done."
