#!/bin/bash

# make the script exit on any error that occurs
set -e

function usage(){
  echo "Usage:"
  echo "  $0 NOTEBOOK-NAME:TAG [DARGS]"
  echo
  echo "Builds a docker image with optional DARGS. This is a companion"
  echo "script to docker-stacks."
}

dev_folder="./dev/"
template_folder="./notebook-templates/"
make_readme_script="make_readme.py"
print_versions_script="print_versions.py"
versions_file="versions.dict"

if (( $# == 0 )); then
  usage
  exit 1
fi

image_name_with_tag=$1; shift;
dargs=$@
 
image_name_split=(${image_name_with_tag//:/" "})
image_name_without_tag="${image_name_split[0]}"
tag="${image_name_split[1]}"
cuda_split=(${image_name_without_tag//-/" "})
cuda="${cuda_split[-1]}"
notebook_name="${image_name_without_tag/-$cuda/}"

if [[ "$image_name_with_tag" == *":experimental" ]] ; then
  full_folder="./notebooks/$cuda:experimental/$notebook_name"
  echo "building experimental image \"$image_name_with_tag\" in folder" \
    "\"$cuda:experimental/$notebook_name\""

  if [[ "$notebook_name" == "base-notebook" ]] ; then
    docker build "$dargs" --no-cache --pull --rm --force-rm \
      -t "$image_name_with_tag" \
      "$full_folder"
  else
    docker build "$dargs" --no-cache --rm --force-rm \
      -t "$image_name_with_tag" \
      "$full_folder"
  fi

  # get the most recent miniconda version number (that corresponds to 'latest')
  repo=$(curl -s https://repo.continuum.io/miniconda/)
  miniconda_latest_sha=$(echo "$repo" | \
    grep -A3 Miniconda3-latest-Linux-x86_64.sh | tail -n1 | \
    sed -e 's/<[^>]*>//g' | sed -e 's/ //g')
  miniconda_most_recent_line=$(echo "$repo" | grep -B3 "$miniconda_latest_sha" \
    | grep Miniconda | grep -v latest)
  miniconda_version=$(echo $miniconda_most_recent_line \
    | awk -F'"' '{print $2}' | awk -F'-' '{print $2}')

else
  full_folder="./notebooks/$cuda/$notebook_name"
  echo "building version-pinned image \"$image_name_with_tag\" in folder" \
    "\"$cuda/$notebook_name\""
  docker build "$dargs" --rm --force-rm \
    -t "$image_name_with_tag" \
    -t "$image_name_without_tag":latest \
    "$full_folder"
  experimental_readme=$(cat ./notebooks/$cuda:experimental/base-notebook/README.md)
  miniconda_version=$(echo $experimental_readme | grep "Miniconda" \
    | awk -F'|' '{print $3}' | xargs)
fi

# extract version numbers
docker run -it -w /workdir \
  -v $(readlink -f $dev_folder):/workdir \
  "$image_name_with_tag" \
  bash -c "./$print_versions_script" > "$full_folder"/"$versions_file"

# generate readme including version numbers
"$dev_folder"/"$make_readme_script" \
  "$template_folder"/"$notebook_name".j2 "$full_folder"
