#!/usr/bin/env python3
# coding: utf-8

""" Disable Dockerfiles """

import ast
import re
import readline
import requests
import subprocess
import sys

versions_file = "versions.dict"

notebook_name = sys.argv[1]

cuda = notebook_name.split(':')[0].split('-')[-1].split('cuda')[-1]
cuda_major, cuda_minor = cuda.split('.')

notebook_root = notebook_name.split('-cuda')[0]

if ":experimental" in notebook_name:
    notebook_folder = "notebooks/cuda" \
        + cuda_major + "." + cuda_minor + ":experimental/" + notebook_root
else:
    notebook_folder = "notebooks/cuda" \
        + cuda_major + "." + cuda_minor + "/" + notebook_root

print()
print("Please give a reason for disabling the Dockerfile for ")
print("notebook \"{}\". End with an emtpy line.".format(notebook_name))
print()

user_input = "none"
disable_message = []
while user_input != "":
      user_input = input("> ")
      disable_message.append(user_input)

disable_message_string = """###WARNING
This image is disabled.

""" + '\n'.join(disable_message[:-1])

print('Disabling "Dockerfile" of image "' + notebook_name + '"')
with open(notebook_folder + "/Dockerfile", 'w') as outfile:
    outfile.write(disable_message_string)

print('Disabling "' + versions_file + '" of image "' + notebook_name + '"')
with open(notebook_folder + "/" + versions_file, 'w') as outfile:
    outfile.write(disable_message_string)

print('Writing warning message to "README.md" of image "' + notebook_name + '"')
with open(notebook_folder + "/README.md", 'w') as outfile:
    outfile.write(disable_message_string)
