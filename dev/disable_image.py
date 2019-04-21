#!/usr/bin/env python3
# coding: utf-8

""" Generate Dockerfiles from template """

import ast
import re
import readline
import requests
import subprocess
import sys

versions_file = "versions.dict"

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

print()
print("Please give a reason for disabling the Dockerfile for ")
print("notebook \"{}\". End with an emtpy line.".format(notebook_name))
print()

user_input = "none"
warning = []
while user_input != "":
      user_input = input("> ").replace('"', '\\"')
      warning.append(user_input)

warning_string = '\\n'.join(warning[:-1])

# only use until line 7
# use ENTRYPOINT to make container issue warning
dockerfile_text = '\n'.join(dockerfile_text.split('\n')[:7])
dockerfile_text += 'ENTRYPOINT ["echo", "### WARNING\\n' + warning_string + '"]'

substitutions = []

if experimental:
    base_container_sha_string = ""
    conda_version_string = ""
    conda_version_var = ""
    conda_update_string = ""
    miniconda_md5_string = ""
    miniconda_version = "latest"
else:
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

    base_container_sha_string = "@sha256:" + base_container_sha

# cuda versions should be replaced first,
# because other packages might depend on it
substitutions = [
    ["{% cuda_major %}", cuda_major],
    ["{% cuda_minor %}", cuda_minor],
    ["{% cudnn %}", cudnn],
    ["{% sha256:base %}", base_container_sha_string],
    ["{% tag %}", tag],
] + substitutions

for sub in substitutions:
    dockerfile_text = dockerfile_text.replace(sub[0], sub[1])

for idx, line in enumerate(dockerfile_text.split('\n')):
    if "{%" in line or "%}" in line:
        raise Exception("Could not replace all placeholders from template \"" \
                        + template_file + "\" in line " + str(idx) \
                        + ":\n" + line)

print('Disabling Dockerfile of image "' + notebook_name + '"')
with open(notebook_folder + "/Dockerfile", 'w') as outfile:
    outfile.write(dockerfile_text)
