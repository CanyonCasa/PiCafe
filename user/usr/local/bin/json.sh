#!/bin/bash
# writes an array of arguments out as a JSON string...



printf "{"

while (( "$#" ));
  do
    x=$1
    y=$2

    shift
    shift

    printf "%g" "$y" &> /dev/null
    if [[ $? == 0 ]] ; then
      # value is a number, don't quote...
      printf "\"$x\": $y"
    else
      if [[ $y =~ ^\{ ]]; then
        # value is a nested object, don't quote...
        printf "\"$x\": $y"
      else
        # value is not a number, so quote...
        printf "\"$x\": \"$y\""
      fi
    fi

    if [[ $# -ne 0 ]]; then
      printf ", "
    fi
  done

printf "}"
echo
