#!/usr/bin/env python3
# coding: utf-8

""" Generate package list for container """

import os
import platform
import subprocess

def read_file(filename):
    with open(filename) as f:
        lines = f.read().strip().split('\n')
        return lines

python_version = platform.python_version()

cuda_version = read_file("/usr/local/cuda/version.txt")[0].split()[-1]

cudnn_file = read_file("/usr/include/cudnn.h")
for idx, line in enumerate(cudnn_file):
    if "CUDNN_MAJOR" in line:
        cudnn_major = cudnn_file[idx].split()[-1]
        cudnn_minor = cudnn_file[idx+1].split()[-1]
        cudnn_patch = cudnn_file[idx+2].split()[-1]
        break
cudnn_version = cudnn_major + "." + cudnn_minor + "." + cudnn_patch

files = os.listdir("/usr/lib/x86_64-linux-gnu/")
nccl_files = [f for f in files if "nccl.so" in f]

# for CUDA v10.2 the library location differs
if nccl_files == []:
    cuda_major_minor = ".".join(cuda_version.split(".")[:2])
    files = os.listdir("/usr/local/cuda-" + cuda_major_minor + \
                       "/targets/x86_64-linux/lib/")
    nccl_files = [f for f in files if "nccl.so" in f]

sorted_nccl_files = sorted(nccl_files)
nccl_version = ".".join([s for s in sorted_nccl_files[-1].split(".") if s.isdigit()])

extensions = []
ext_list_process = subprocess.run("jupyter labextension list".split(), capture_output=True, check=True)
ext_list_combined_output = ext_list_process.stdout.decode() + ext_list_process.stderr.decode()  # hack needed because of https://github.com/jupyterlab/jupyterlab/issues/6145
ext_list = ext_list_combined_output.strip().split('\n')
for ext in ext_list[3:]:
    extensions.append(ext.split()[:2])

packages = []
package_result = subprocess.run("conda list".split(), capture_output=True, check=True)
package_result_list = package_result.stdout.decode().strip().split('\n')

for line in package_result_list:
    if not line.startswith("#"):
        packages.append(line.split()[:2])

try:
    import tensorflow as tf
    keras_version = tf.keras.__version__
    packages.append(["keras (tensorflow)", keras_version])
    packages = sorted(packages)
except ImportError:
    pass

possible_deep_learning_packages = ["fastai", "pytorch", "tensorflow", "keras", "mxnet"]
deep_learning_packages = []
for dl in possible_deep_learning_packages:
    for package in packages:
        if package[0].startswith(dl):
            deep_learning_packages.append(package)

apt_list_process = subprocess.run("apt list --installed".split(), capture_output=True, check=True)
apt_list_raw = apt_list_process.stdout.decode().strip().split('\n')
apt_list = []
for program in apt_list_raw[1:]:
    program_list = program.split()
    apt_list.append([program_list[0].split('/')[0], program_list[1]])

info_dict = {}
info_dict["framework"] = {"Python": python_version,
        "CUDA": cuda_version,
        "cuDNN": cudnn_version,
        "NCCL": nccl_version}

info_dict["extensions"] = dict(extensions)
info_dict["packages"] = dict(packages)
info_dict["deep_learning"] = dict(deep_learning_packages)
info_dict["apt"] = dict(apt_list)

print(info_dict)
