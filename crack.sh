#!/bin/bash

# Path to the hash file
hash_file="/hashes/hash.txt"

# Path to the wordlist
wordlist_file="/wordlist/wordlist.txt"

# Output file for the cracked hashes
output_file="/potfile/pot.txt"

# Lock file path
lock_file="/tmp/crack.lock"

# Create lock file
touch $lock_file

# Ensure hashcat is available
if ! command -v hashcat &> /dev/null
then
    echo "Hashcat could not be found"
    rm $lock_file
    exit 1
fi

# Check if hash file exists
if [ ! -f "$hash_file" ]; then
    echo "Hash file not found: $hash_file"
    rm $lock_file
    exit 1
fi

# Check if wordlist file exists
if [ ! -f "$wordlist_file" ]; then
    echo "Wordlist file not found: $wordlist_file"
    rm $lock_file
    exit 1
fi

# Run hashcat
hashcat -m 1000 -a 0 -o $output_file $hash_file $wordlist_file

# Remove lock file after hashcat finishes
rm $lock_file

echo "Cracking process complete."
