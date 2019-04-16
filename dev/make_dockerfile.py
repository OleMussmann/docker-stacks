#!/usr/bin/env python3
# coding: utf-8

""" Generate Dockerfiles from template """

import ast
import requests
import subprocess
import sys

versions_file = "versions.dict"

dockerfile = "/tmp/out"

repo_url = "https://repo.continuum.io/miniconda/"

notebook_name = sys.argv[1]

date_string = sys.argv[2]
cudnn = sys.argv[3]  # optional, will use versions.dict otherwise

if ":experimental" in notebook_name:
    experimental = True
    tag = "experimental"
else:
    experimental = False
    tag = date_string

cuda = notebook_name.split(':').[0].split('-')[-1].split('cuda')[-1]
cuda_major, cuda_minor = cuda.split('.')

notebook_folder_experimental = "notebooks/cuda" \
    + cuda_major + "." + cuda_minor + ":experimental/" + notebook_name
notebook_folder_stable = "notebooks/cuda" \
    + cuda_major + "." + cuda_minor + "/" + notebook_name

notebook_stable = notebook_name.replace(":experimental", '')
template_file = "notebook-templates/" + notebook_stable + ".j2"

with open(notebook_folder + "/" + versions_file) as f:
    content = f.read()
    versions = ast.literal_eval(content)

cuda_major = versions["framework"]["CUDA"].split('.')[0]
cuda_minor = versions["framework"]["CUDA"].split('.')[1]
cudnn = versions["framework"]["cuDNN"].split('.')[0]
conda_version = versions["packages"]["conda"]

base_container = "nvidia/cuda:" + cuda_major + "." + cuda_minor + "-cudnn" \
    + cudnn + "-devel"

sha_process = subprocess.run(("docker inspect --format='{{.RepoDigests}}' " +
                             base_container).split(), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
sha_output = sha_process.stdout.decode()
base_container_sha = sha_output.split(':')[1].split(']')[0]

substitutions = []

if experimental:
    repo_website = requests.get(repo_url)
    repo_text = repo_website.text.split('\n')

#    # get lastest miniconda version
#    if miniconda_version == "":
#        sha_latest = ""
#        latest_names = []
#        latest_miniconda_version = ""
#        for idx, line in enumerate(repo_text):
#            if "Miniconda3-latest-Linux-x86_64" in line:
#                sha_latest = repo_text[idx + 3]
#        if sha_latest == "":
#            raise Exception("Can't find latest version for Miniconda3 on " \
#                            + "repo " + repo_url)
#        for idx, line in enumerate(repo_text):
#            if line == sha_latest:
#                latest_names.append(repo_text[idx - 3])
#        if latest_names == []:
#            raise Exception("Can't find latest version for Miniconda3 on " \
#                            + "repo " + repo_url)
#        for latest_name in latest_names:
#            if latest_name.split('-')[1] != "latest":
#                miniconda_version = latest_name.split('-')[1]
#        if miniconda_version == "":
#            raise Exception("Can't find latest version for Miniconda3 on " \
#                            + "repo " + repo_url)

    miniconda_version = ""

    experimental_versions_file = notebook_folder_experimental \
        + "/" + versions_file
    with open(experimental_versions_file) as f:
        exp_versions = f.readlines()
        for line in exp_versions:
            if "Miniconda" in line:
                miniconda_version = line.split('|')[2].strip()

    if miniconda_version = "":
        raise Exception("Can't find Miniconda version in experimental " \
                        + "version file.")

    miniconda_md5 = ""

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
else:
    base_container_sha_string = ""
    conda_version_string = ""
    conda_update_string = ""
    miniconda_md5_string = ""
    miniconda_version = "latest"

    for key, value in versions["packages"].items():
        substitutions.append(["{% " + key + "_version %}", ""])

    for key, value in versions["extensions"].items():
        substitutions.append(["{% " + key + "_version %}", ""])

substitutions += [
    ["{% cuda_major %}", versions["framework"]["CUDA"].split('.')[0]],
    ["{% cuda_minor %}", versions["framework"]["CUDA"].split('.')[1]],
    ["{% cudnn %}", versions["framework"]["cuDNN"].split('.')[0]],
    ["{% sha256:base %}", base_container_sha_string],
    ["{% tag %}", tag],
    ["{% miniconda_version_var %}", "MINICONDA_VERSION=" + miniconda_version],
    ["{% miniconda_md5_check %}", miniconda_md5_string],
    ["{% conda_version_var %}", "; CONDA_VERSION=" + conda_version],
    ["{% conda_version_string %}", conda_version_string],
    ["{% conda_update %}", conda_update_string],
]

with open(template_file) as t:
    dockerfile_text = t.read()

for sub in substitutions:
    dockerfile_text = dockerfile_text.replace(sub[0], sub[1])

if "{% " in dockerfile_text or " %}" in dockerfile_text:
    raise Exception("Could not replace all placeholders from template " \
                    + template_file)

if experimental:
    dockerfile = notebook_folder_experimental + "/Dockerfile"
else:
    dockerfile = notebook_folder_stable + "/Dockerfile"

with open(dockerfile, 'w') as outfile:
    outfile.write(dockerfile_text)
