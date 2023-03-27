#!/bin/bash

url="https://quelleheureestil.fr"
content=$(curl -s "$url")
regex_date="Date:[[:space:]]*([[:digit:]]{2}\.[[:digit:]]{2}\.[[:digit:]]{4})"
regex_day="Jours:[[:space:]]*([[:alpha:]]+)"
regex_month="Mois:[[:space:]]*([[:alpha:]]+)"
regex_week="Semaine:[[:space:]]*([[:digit:]]+)"
regex_dayyear="Jour de l'année:[[:space:]]*([[:digit:]]+)"

if [[ $content =~ $regex_date ]]; then
    date="${BASH_REMATCH[1]}"
    echo "Date: $date"
fi

if [[ $content =~ $regex_day ]]; then
    day="${BASH_REMATCH[1]}"
    echo "Jour: $day"
fi

if [[ $content =~ $regex_month ]]; then
    month="${BASH_REMATCH[1]}"
    echo "Mois: $month"
fi

if [[ $content =~ $regex_week ]]; then
    week="${BASH_REMATCH[1]}"
    echo "Semaine: $week"
fi

if [[ $content =~ $regex_dayyear ]]; then
    dayyear="${BASH_REMATCH[1]}"
    echo "Jour de l'année: $dayyear"
fi
