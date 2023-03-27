#!/bin/bash

url="https://quelleheureestil.fr"
content=$(curl -s "$url")
regex="var currenttime = '([[:alpha:]]+ [[:digit:]]{2}, [[:digit:]]{4} [[:digit:]]{2}:[[:digit:]]{2}:[[:digit:]]{2})'"

if [[ $content =~ $regex ]]; then
    datetime="${BASH_REMATCH[1]}"
    date=$(date -d "$datetime" +"%A %d %B %Y")
    time=$(date -d "$datetime" +"%H:%M:%S")
    echo "Date: $date"
    echo "Heure: $time"
else
    echo "Impossible de récupérer l'heure actuelle."
fi
