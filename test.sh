#!/bin/bash
for i in ./images/* ; do
    result=$(python3 validateface.py -t $i)
    if  [[ "$result" == *"True"* ]]
    then
        echo $i $result
    fi

done