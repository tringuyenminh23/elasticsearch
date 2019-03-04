#!/usr/bin/env bash

datasets=("cran")
allowedArgs=("${datasets[@]}" "all")

# Check if has arguments
if [[ $# -ne 1 ]]; then
    echo 1>&2 "Must take at least one arguments declaring:
     - $(IFS=$'|'; echo "${datasets[*]}"):  a single dataset
     - all: all dataset"
    exit 0
fi

# Chekc if allowed argument
data=$1

function arrayContains() {
    local e match="$1"
    shift
    for e; do
        [[ "$e" == "$match" ]] && return 0;
    done
    return 1
}

arrayContains "$data" "$allowedArgs"
isIn="$?"

if  [[ "$isIn" -ne 0 ]]; then
    echo "Arguments must be one of
        $(IFS=$'|'; echo "${allowedArgs[*]}")"
fi

# create data folder if not exist
if [ ! -d "./io/data" ]; then
    mkdir ./io/data
fi

function downloadcran () {
    echo "Clean cran directory if any and download cran"
    if [ -d "./io/data/cran" ]; then
        cd ./io/data/cran/
        rm -rf *
    else
        cd ./io/data
        mkdir cran && cd cran
    fi
    curl --remote-name-all http://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz
    tar xfz cran.tar.gz
    cd ../../..
}

if [ $data == "cran" ]; then
    downloadcran
elif [ $data == "all" ]; then
    downloadcran
fi