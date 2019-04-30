#!/usr/bin/env python3
# coding: utf-8

""" Generate Dockerfiles from template """

import ast
import re
import requests
import subprocess
import sys

versions_file = "versions.dict"

repo_url = "https://repo.continuum.io/miniconda/"

notebook_name = sys.argv[1]
date_string = sys.argv[2]
cudnn = sys.argv[3]

cuda = notebook_name.split(':')[0].split('-')[-1].split('cuda')[-1]
cuda_major, cuda_minor = cuda.split('.')

notebook_root = notebook_name.split('-cuda')[0]

notebook_folder_experimental = "notebooks/cuda" \
    + cuda_major + "." + cuda_minor + ":experimental/" + notebook_root
notebook_folder_stable = "notebooks/cuda" \
    + cuda_major + "." + cuda_minor + "/" + notebook_root

template_file = "notebook-templates/" + notebook_root + ".j2"

with open(template_file) as t:
    dockerfile_text = t.read()

if ":experimental" in notebook_name:
    experimental = True
    tag = "experimental"
    notebook_folder = notebook_folder_experimental
else:
    experimental = False
    tag_array = notebook_name.split(':')
    if len(tag_array) == 2:
        tag = tag_array[-1]
    elif len(tag_array) == 1:
        tag = date_string
    else:
        raise SyntaxError("Notebook name invalid, multiple tags detected.")
    notebook_folder = notebook_folder_stable


substitutions = []

if experimental:
    base_container_sha_string = ""
    conda_version_string = ""
    conda_version_var = ""
    conda_update_string = ""
    miniconda_md5_string = ""
    miniconda_version = "latest"

else:
    # Use experimental versions_file, also for stable branch. We want to inherit
    # the new versions to stable after testing the experimental containers.
    with open(notebook_folder_experimental + "/" + versions_file) as f:
        content = f.read()

        disabling = False
        if content.startswith("### WARNING"):
            print('Experimental image disabled. Writing warning to '
                  + 'dockerfile "' + notebook_folder + "/Dockerfile" + '", '
                  + '"README.md" and "' + versions_file + '".')
            for file in [notebook_folder + "/Dockerfile",
                         notebook_folder + "/README.md",
                         notebook_folder + "/" + versions_file]:
                with open(file, 'w') as f:
                    f.write(content)
            exit()
        else:
            versions = ast.literal_eval(content)

    conda_version = versions["packages"]["conda"]
    miniconda_version = versions["framework"]["Miniconda"]

    base_container = "nvidia/cuda:" + cuda_major + "." + cuda_minor \
        + "-cudnn" + cudnn + "-devel"

    sha_process = subprocess.run(
        ("docker inspect --format='{{.RepoDigests}}' " +
         base_container).split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True)
    sha_output = sha_process.stdout.decode()
    base_container_sha = sha_output.split(':')[1].split(']')[0]

    miniconda_md5 = ""

    if not disabling:
        repo_website = requests.get(repo_url)
        repo_text = repo_website.text.split('\n')

        for idx, line in enumerate(repo_text):
            if "Miniconda3-" + miniconda_version + "-Linux-x86_64" in line:
                miniconda_md5 = repo_text[idx + 3].split('>')[1].split('<')[0]

        if miniconda_md5 == "":
            raise Exception("Can't find the Miniconda version \"" \
                            + miniconda_version \
                            + "\" on the repo website " \
                            + repo_url \
                            + " Please check the repo manually.")

    base_container_sha_string = "@sha256:" + base_container_sha
    conda_version_string = '="${CONDA_VERSION}.*"'
    conda_version_var = "\nENV CONDA_VERSION=" + conda_version
    conda_update_string = "$CONDA_DIR/bin/conda " + \
        "update --all --quiet --yes &&"
    miniconda_md5_string = 'echo "' + miniconda_md5 + " " + \
        '*Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh\" | ' + \
        'md5sum -c - &&'

    for key, value in versions["packages"].items():
        substitutions.append(["{% " + key + "_version %}", "==" + value])

    for key, value in versions["extensions"].items():
        # remove trailing version "v" from version number, e.g.: v0.12.0
        substitutions.append(["{% " + key + "_version %}", "@^" + value[1:]])


# cuda versions should be replaced first,
# because other packages might depend on it
substitutions = [
    ["{% cuda_major %}", cuda_major],
    ["{% cuda_minor %}", cuda_minor],
    ["{% cudnn %}", cudnn],
    ["{% sha256:base %}", base_container_sha_string],
    ["{% tag %}", tag],
    ["{% miniconda_version_var %}", "MINICONDA_VERSION=" + miniconda_version],
    ["{% miniconda_md5_check %}", miniconda_md5_string],
    ["{% conda_version_var %}", conda_version_var],
    ["{% conda_version_string %}", conda_version_string],
    ["{% conda_update %}", conda_update_string],
] + substitutions

for sub in substitutions:
    dockerfile_text = dockerfile_text.replace(sub[0], sub[1])

if experimental:
    dockerfile_text = re.sub('{% blas_version %}','=*',dockerfile_text)
    dockerfile_text = re.sub('{% .+?_version %}','',dockerfile_text)

for idx, line in enumerate(dockerfile_text.split('\n')):
    if "{%" in line or "%}" in line:
        raise Exception("Could not replace all placeholders from template \"" \
                        + template_file + "\" in line " + str(idx) \
                        + ":\n" + line)

print('Writing new dockerfile "' + notebook_folder + "/Dockerfile" + '"')
with open(notebook_folder + "/Dockerfile", 'w') as outfile:
    outfile.write(dockerfile_text)

if not experimental:
    print('Writing tag "' + tag + '" to tag file "' + notebook_folder + "/tag" + '"')
    with open(notebook_folder + "/tag", 'w') as outfile:
        outfile.write(tag)
