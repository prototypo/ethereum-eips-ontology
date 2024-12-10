#!/bin/bash

# Change to the parent directory of this script
cd $(dirname "$0")
cd ..

file="eip-ontology.txt"
count="10" # Number of lines to look backward

# Extract last EIP using regex
for i in $(seq 1 $count);
do
    # Work backward in the file one line at a time
    j=$((i - 1))
    if [[ "$j" -eq "0" ]]; then
        line=`tail -$i $file`
    else
        line=`tail -$i $file | head -$j`
    fi

    # Look for an EIP number on the current line
    if [[ "$line" =~ \(EIP-([0-9]+)\) ]]; then
        lasteip="${BASH_REMATCH[1]}"
        echo "Last EIP processed: $lasteip"
        # Exit when the first EIP is found
        exit 0
    fi
done

echo "❌ Error: EIP not found!"
exit 1
