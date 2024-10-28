#!/bin/bash

# Change to the parent directory of this script
cd $(dirname "$0")
cd ..

file="glossary.txt"
line=`tail -2 $file | head -1`

# Extract last EIP using regex
if [[ "$line" =~ \(EIP-([0-9]+)\) ]]; then
lasteip="${BASH_REMATCH[1]}"
echo "Last EIP processed: $lasteip"
else
echo "EIP not found!"
exit 1
fi
