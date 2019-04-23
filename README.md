# Jupyter Docker Stacks

Jupyter Docker Stacks are a set of ready-to-run, [CUDA](https://developer.nvidia.com/cuda-toolkit) enabled, GPU-accelerated [Docker](https://hub.docker.com/u/isbjornlabs/) images containing Jupyter applications and interactive computing tools for deep learning. Pre-compiled images can be found on [Docker Hub](https://hub.docker.com/u/isbjornlabs/).

## Quick Start
Whether you pull from Docker Hub or build your own, for GPU acceleration you first have to make sure that Docker containers can talk to the GPU. Right now, only Nvidia GPUs are supported. AMD GPU support will follow in the future.

### Setup
1. Install the latest [Nvidia driver](https://github.com/NVIDIA/nvidia-docker/wiki/Frequently-Asked-Questions#how-do-i-install-the-nvidia-driver). Use your [package manager](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#package-manager-installation) if possible. For recent Ubuntu versions, you can simply open `Software & Updates`, go to the tab `Additional Drivers` and install the driver from there.
2. Install [Docker CE](https://docs.docker.com/install/) - preferrably the latest version from https://docs.docker.com/install/.
3. Install and test [Nvidia Docker](https://github.com/NVIDIA/nvidia-docker#quickstart).

### Images
[![Image Overview](http://interactive.blockdiag.com/image?compression=deflate&encoding=base64&src=eJyFzL0OwjAMRtGdp4i6V6xIVRHd2BkRQk7rIKupXSUuv-LdaZgIS9f7Hdt6afuO4GJeK2MkELKCkrCpzShBA5BW89Khg8nr2QlrpCfO8yb1xhw9WPR1wVea_6zbqYPdYd8Up2r13cutsRCxZFG0In26ykISAzEN4DP035KLLY2PTOUlGUWOEpyX2wJ0EBVoAQ13Rv0x7w-jqmh4)](http://interactive.blockdiag.com/?compression=deflate&src=eJyFzL0OwjAMRtGdp4i6V6xIVRHd2BkRQk7rIKupXSUuv-LdaZgIS9f7Hdt6afuO4GJeK2MkELKCkrCpzShBA5BW89Khg8nr2QlrpCfO8yb1xhw9WPR1wVea_6zbqYPdYd8Up2r13cutsRCxZFG0In26ykISAzEN4DP035KLLY2PTOUlGUWOEpyX2wJ0EBVoAQ13Rv0x7w-jqmh4)

While this repository is the base for many Docker images, only four are recommended for actual usage:

- scipy-notebook
    - Without any deep-learning frameworks, this image satisfies your vanilla python GPU-number-crunching needs with for example [numba](https://numba.pydata.org/).
- fastai-notebook
    - Sports [fast.ai](https://docs.fast.ai/) which is built upon the included [PyTorch](https://pytorch.org/).
- tensorflow-notebook
    - Uses [Tensorflow](https://www.tensorflow.org/) which includes [Keras](https://keras.io/).
- mxnet-notebook
    - Rocking Apache's [MXNet](https://mxnet.apache.org/).

These images come in two different flavours:

- experimental
    - As raw as it gets, these images always pull the latest software versions when you build them.
- version-pinned
    - If you are not living on the edge, the version-pinned recipes will reproducibly build the same images. The latest version-pinned images will carry the tag `latest` in addition to their date-tag `YYYY-MM-DD`. Dropping the tag will always pull `latest`.

Images are based on different versions of CUDA. Supported are:

- CUDA 9.2
- CUDA 10.0
- CUDA 10.1

Choose the highest CUDA version that still works with your target notebook and your latest installed graphics driver.

| Linux x86_64 Driver Version | CUDA Toolkit |
|-----------------------------|--------------|
| >= 418.39                   | CUDA 10.1    |
| >= 410.48                   | CUDA 10.0    |
| >= 396.26                   | CUDA 9.2     |

The image that you want to use is named
```
isbjornlabs/[NAME]-notebook-cuda[CUDA_VERSION][:TAG]
```

The `experimental` version of the `fastai` notebook, based on CUDA `10.1` is thus called: `isbjornlabs/fastai-notebook-cuda10.1:experimental`.

The version-pinned version from `2019-04-21` of the `mxnet` notebook, based on CUDA `9.2` is thus called: `isbjornlabs/mxnet-notebook-cuda9.2:2019-04-21`.

The `latest` version of the version-pinned `tensorflow` notebook, based on CUDA `10.0` is thus called: `isbjornlabs/tensorflow-notebook-cuda10.0:latest`. The latest tag can be omitted for the short version: `isbjornlabs/tensorflow-notebook-cuda10.0`

#### Image Tables
Not all versions are compatible with each other. Consult the tables below to see which notebooks are buildable.

##### Version-pinned: 2019-04-21
| notebook   | [CUDA 9.2](notebooks/cuda9.2)              | [CUDA 10.0](notebooks/cuda10.0)             | [CUDA 10.1](notebooks/cuda10.1)              |
|------------|--------------------------------------------|---------------------------------------------|----------------------------------------------|
| scipy      | [✔️](notebooks/cuda9.2/scipy-notebook)      | [✔️](notebooks/cuda10.0/scipy-notebook)      | [✔️](notebooks/cuda10.1/scipy-notebook)       |
| fastai     | [✔️](notebooks/cuda9.2/fastai-notebook)     | [✔️](notebooks/cuda10.0/fastai-notebook)     | [✔️](notebooks/cuda10.1/fastai-notebook)      |
| tensorflow | [✔️](notebooks/cuda9.2/tensorflow-notebook) | [✔️](notebooks/cuda10.0/tensorflow-notebook) | [❌](notebooks/cuda10.1/tensorflow-notebook) |
| mxnet      | [✔️](notebooks/cuda9.2/mxnet-notebook)      | [✔️](notebooks/cuda10.0/mxnet-notebook)      | [❌](notebooks/cuda10.1/mxnet-notebook)      |

##### Experimental
| notebook   | [CUDA 9.2](notebooks/cuda9.2:experimental)              | [CUDA 10.0](notebooks/cuda10.0:experimental)             | [CUDA 10.1](notebooks/cuda10.1:experimental)              |
|------------|--------------------------------------------|---------------------------------------------|----------------------------------------------|
| scipy      | [✔️](notebooks/cuda9.2/scipy-notebook:experimental)      | [✔️](notebooks/cuda10.0/scipy-notebook:experimental)      | [✔️](notebooks/cuda10.1/scipy-notebook:experimental)       |
| fastai     | [✔️](notebooks/cuda9.2/fastai-notebook:experimental)     | [✔️](notebooks/cuda10.0/fastai-notebook:experimental)     | [✔️](notebooks/cuda10.1/fastai-notebook:experimental)      |
| tensorflow | [✔️](notebooks/cuda9.2/tensorflow-notebook:experimental) | [✔️](notebooks/cuda10.0/tensorflow-notebook:experimental) | [❌](notebooks/cuda10.1/tensorflow-notebook:experimental) |
| mxnet      | [✔️](notebooks/cuda9.2/mxnet-notebook:experimental)      | [✔️](notebooks/cuda10.0/mxnet-notebook:experimental)      | [❌](notebooks/cuda10.1/mxnet-notebook:experimental)      |

### Examples
The examples below may help you get started if you finished the above installation, know which image you want to use, and want to launch a single Jupyter Notebook server in a container.

The [User Guide on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/) describes additional uses and features in detail.

**Example 1:** This command pulls the `isbjornlabs/tensorflow-notebook` image tagged `2019-04-21` from Docker Hub if it is not already present on the local host. It then starts a container running a Jupyter Notebook server and exposes the server on host port 8888. The server logs appear in the terminal. Visiting `http://<hostname>:8888/?token=<token>` in a browser loads the Jupyter Notebook dashboard page, where `hostname` is the name of the computer running docker and `token` is the secret token printed in the console. The container remains intact for restart after the notebook server exits.

    docker run -p 8888:8888 isbjornlabs/tensorflow-notebook:2019-04-21

**Example 2:** This command performs the same operations as **Example 1**, but it exposes the server on host port 10000 instead of port 8888. Visiting ``http://<hostname>:10000/?token=<token>`` in a browser loads JupyterLab, where ``hostname`` is the name of the computer running docker and ``token`` is the secret token printed in the console.::

    docker run -p 10000:8888 isbjornlabs/tensorflow-notebook:2019-04-21

**Example 3:** This command pulls the `isbjornlabs/fastai-notebook` image tagged `2019-04-21` from Docker Hub if it is not already present on the local host. It then starts an *ephemeral* container running a Jupyter Notebook server and exposes the server on host port 10000. The command mounts the current working directory on the host as `/workdir` in the container. The server logs appear in the terminal. Visiting `http://<hostname>:10000/?token=<token>` in a browser loads JupyterLab, where `hostname` is the name of the computer running docker and `token` is the secret token printed in the console. Docker destroys the container after notebook server exit, but any files written to `/workdir` in the container remain intact on the host.

    docker run --rm -p 10000:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/workdir isbjornlabs/fastai-notebook:2019-04-21

## Contributing

Feel free to file bug reports and pull requests. However, you are encouraged to contribute to the [upstream jupyter docker-stacks](https://github.com/jupyter/docker-stacks) instead. See the [Contributor Guide on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/) for information about how to contribute package updates, recipes, features, tests, and community maintained stacks.

## Alternatives

* [jupyter/repo2docker](https://github.com/jupyter/repo2docker) - Turn git repositories into Jupyter-enabled Docker Images
* [openshift/source-to-image](https://github.com/openshift/source-to-image) - A tool for building/building artifacts from source and injecting into docker images
* [jupyter-on-openshift/jupyter-notebooks](https://github.com/jupyter-on-openshift/jupyter-notebooks) - OpenShift compatible S2I builder for basic notebook images

## Resources

* [Issue Tracker on GitHub](https://github.com/OleMussmann/docker-stacks)
* [Upstream Issue Tracker on GitHub](https://github.com/jupyter/docker-stacks)
* [Upstream Documentation on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/)
* [Jupyter Google Group](https://groups.google.com/forum/#!forum/jupyter)
* [Jupyter Website](https://jupyter.org)
