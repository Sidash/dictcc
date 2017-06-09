#!/bin/bash
# simple script for executing dictcc continiously

alias dictcc='./dictcc.py' # change this line

export dict="deen"
function dictcc_prompt() {  
    clear;
    while true;
        do echo -n "Search in $dict >> ";
        read query;
        echo "\n\n--------------------------------------------------------------------------------"
        clear;
        echo "Searching in '$dict' for '$query'";
        dictcc $dict $query | less;
        echo
    done;
}
