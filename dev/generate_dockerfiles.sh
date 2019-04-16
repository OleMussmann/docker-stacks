#!/bin/bash

notebooks=()
cuda_strings=()
experimental=false

while [[ $# -gt 0 ]]
do
  case $1 in
    -h | --help )    exit 1; ;;
    --cuda )         shift; cuda_strings+=("$1"); shift;;
    --cudnn )        shift; cudnn="$1"; shift;;
    --miniconda )    shift; miniconda_version="$1"; shift;;
    --tag )          shift; tag="$1"; shift;;
    --experimental ) shift; experimental=true; ;;
    * )              notebooks+=("$1"); shift;;
  esac
done

date=$(date +%Y%m%d).1
echo $date
exit

miniconda_sha=$(curl -s https://repo.continuum.io/miniconda/ | \
  grep -A3 Miniconda3-"${miniconda_version}"-Linux-x86_64 | tail -n1 | \
  sed -e 's/<[^>]*>//g' | sed -e 's/ //g')

echo "$miniconda_sha"
exit

cuda=(${cuda_string//./ })  # split the string at '.'
cuda_major=${cuda[0]}
cuda_minor=${cuda[1]}

echo ${cuda_strings[@]}
echo $cuda_strings
#${notebooks[@]}

all=$(ls ../notebook-templates)

readarray -t a < ./versions
echo ${a[@]}
