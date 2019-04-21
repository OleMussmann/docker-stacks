#!/usr/bin/env python
# coding: utf-8

""" Generate package list for container """

import ast
import sys

versions_file = "versions.dict"

template_file = sys.argv[1]
notebook_folder = sys.argv[2]
miniconda_version = sys.argv[3]

with open(notebook_folder + "/" + versions_file) as f:
    content = f.read()
    if content.startswith("### WARNING"):
        with open(notebook_folder + "/README.md", 'w') as f:
            f.write(content)
        exit()
    else:
        versions = ast.literal_eval(content)

possible_deep_learning_packages = ["fastai", "pytorch", "tensorflow", "keras", "mxnet"]
deep_learning_packages = []
for dl in possible_deep_learning_packages:
    for package in versions["packages"]:
        if package[0].startswith(dl):
            deep_learning_packages.append(package)

deep_learning_string = ""
for deep_learning_package in deep_learning_packages:
    new_line = "| " + deep_learning_package[0] + " | " + deep_learning_package[1] + " |\n"
    deep_learning_string += new_line

extensions_string = ""
for extension in sorted(versions["extensions"]):
    new_line = "| " + extension + " | " \
        + versions["extensions"][extension] + " |\n"
    extensions_string += new_line

packages_string = ""
for package in sorted(versions["packages"]):
    new_line = "| " + package + " | " + versions["packages"][package] + " |\n"
    packages_string += new_line

apt_string = ""
for program in sorted(versions["apt"]):
    new_line = "| " + program + " | " + versions["apt"][program] + " |\n"
    apt_string += new_line

framework_block = """### Framework
| name | version |
|-|-|
| Python | {python_version} |
| Miniconda | {miniconda_version} |
| CUDA | {cuda_version} |
| cuDNN | {cudnn_version} |
| NCCL | {nccl_version} |

""".format( \
           python_version=versions["framework"]["Python"],
           cuda_version=versions["framework"]["CUDA"],
           cudnn_version=versions["framework"]["cuDNN"],
           nccl_version=versions["framework"]["NCCL"],
           miniconda_version=miniconda_version
           )

if not deep_learning_packages == []:
    deep_learning_block = """### Deep Learning Packages
| name | version |
|-|-|
{deep_learning_string}
""".format(deep_learning_string=deep_learning_string)
else:
    deep_learning_block = ""

extensions_block = """### Extensions
| name | version |
|-|-|
{extensions_string}
""".format(extensions_string=extensions_string)

packages_block = """### Python Packages
| name | version |
|-|-|
{packages_string}
""".format(packages_string=packages_string)

apt_block = """### System Programs
| name | version |
|-|-|
{apt_string}
""".format(apt_string=apt_string)

version_info = \
    framework_block + \
    deep_learning_block + \
    extensions_block + \
    packages_block + \
    apt_block

with open(notebook_folder + "/README.md", 'w') as f:
    f.write(version_info)
