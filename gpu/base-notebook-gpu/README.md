[![docker pulls](https://img.shields.io/docker/pulls/jupyter/base-notebook.svg)](https://hub.docker.com/r/jupyter/base-notebook/) [![docker stars](https://img.shields.io/docker/stars/jupyter/base-notebook.svg)](https://hub.docker.com/r/jupyter/base-notebook/) [![image metadata](https://images.microbadger.com/badges/image/jupyter/base-notebook.svg)](https://microbadger.com/images/jupyter/base-notebook "jupyter/base-notebook image metadata")

# CUDA ready Jupyter Notebook Stack

Based on the official [Jupyter Docker Stacks](https://github.com/jupyter/docker-stacks).

Find it pre-built on Docker Hub:

[isbjornlabs/base-notebook-cuda10.1](https://hub.docker.com/r/isbjornlabs/base-notebook-cuda10.1)
[isbjornlabs/base-notebook-cuda10.0](https://hub.docker.com/r/isbjornlabs/base-notebook-cuda10.0)
[isbjornlabs/base-notebook-cuda9.2](https://hub.docker.com/r/isbjornlabs/base-notebook-cuda9.2)

## Which version do I need?

Update your driver first, if possible. Then use the highest CUDA Toolkit version that still works for your local driver. Consult the [NVIDIA documentation](https://docs.nvidia.com/deploy/cuda-compatibility/index.html) for details. Please note that CUDA 9.2 is [marked as EXPERIMENTAL](https://gitlab.com/nvidia/cuda/tree/ubuntu18.04) by NVIDIA.

| CUDA Toolkit |	Linux x86_64 Driver Version |
|-|-|
| CUDA 10.1 (10.1.105) | >= 418.39 |
| CUDA 10.0 (10.0.130) | >= 410.48 |
| CUDA 9.2 (9.2.88) | >= 396.26 |

## Which image do I need?
[![alt text](http://interactive.blockdiag.com/image?compression=deflate&encoding=base64&src=eJyFjsEKwjAQRO_9iuC9noVSsTfvXgoiskm3ZWmaLckWUfHfbTyZKvQ684Y32rLpG4JOPTOl2BM6ASF2qlQje_FAUsxNgy1MVq4tOwn0wLnexbxSZwsabbkxUwN1va0Pp2O1uRTZp8z3SkPA3LGgZu7jJAkiMZCjAWwCLbPIBUPjPaHSJDKCLrBvLd9WwBaCAK1AhofRoqT__ygW5jB14A2DYBMHC9WXfQH-6JIPCfx6Ay7SmPA)](http://interactive.blockdiag.com/?compression=deflate&src=eJyFjsEKwjAQRO_9iuC9noVSsTfvXgoiskm3ZWmaLckWUfHfbTyZKvQ684Y32rLpG4JOPTOl2BM6ASF2qlQje_FAUsxNgy1MVq4tOwn0wLnexbxSZwsabbkxUwN1va0Pp2O1uRTZp8z3SkPA3LGgZu7jJAkiMZCjAWwCLbPIBUPjPaHSJDKCLrBvLd9WwBaCAK1AhofRoqT__ygW5jB14A2DYBMHC9WXfQH-6JIPCfx6Ay7SmPA)

# Base Jupyter Notebook Stack

Please visit the documentation site for help using and contributing to this image and others.

* [Jupyter Docker Stacks on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)
* [Selecting an Image :: Core Stacks :: jupyter/base-notebook](http://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-base-notebook)
