# Jupyter Docker Stacks

Jupyter Docker Stacks are a set of ready-to-run, [CUDA](https://developer.nvidia.com/cuda-toolkit) enabled, GPU-accelerated [Docker](https://hub.docker.com/u/isbjornlabs/) images containing Jupyter applications and interactive computing tools for deep learning.

## Quick Start

You can try a [recent build of the jupyter/base-notebook image on mybinder.org](https://mybinder.org/v2/gh/jupyter/docker-stacks/master?filepath=README.ipynb) by simply clicking the preceding link. Otherwise, the two examples below may help you get started if you [have Docker installed](https://docs.docker.com/install/) know [which Docker image](http://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html) you want to use, and want to launch a single Jupyter Notebook server in a container.

The [User Guide on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/) describes additional uses and features in detail.

**Example 1:** This command pulls the `isbjornlabs/tensorflow-notebook` image tagged `20190419` from Docker Hub if it is not already present on the local host. It then starts a container running a Jupyter Notebook server and exposes the server on host port 8888. The server logs appear in the terminal. Visiting `http://<hostname>:8888/?token=<token>` in a browser loads the Jupyter Notebook dashboard page, where `hostname` is the name of the computer running docker and `token` is the secret token printed in the console. The container remains intact for restart after the notebook server exits.

    docker run -p 8888:8888 isbjornlabs/tensorflow-notebook:20190419

**Example 2:** This command performs the same operations as **Example 1**, but it exposes the server on host port 10000 instead of port 8888. Visiting ``http://<hostname>:10000/?token=<token>`` in a browser loads JupyterLab, where ``hostname`` is the name of the computer running docker and ``token`` is the secret token printed in the console.::

    docker run -p 10000:8888 isbjornlabs/tensorflow-notebook:20190419

**Example 3:** This command pulls the `isbjornlabs/fastai-notebook` image tagged `20190419` from Docker Hub if it is not already present on the local host. It then starts an *ephemeral* container running a Jupyter Notebook server and exposes the server on host port 10000. The command mounts the current working directory on the host as `/home/jovyan/work` in the container. The server logs appear in the terminal. Visiting `http://<hostname>:10000/?token=<token>` in a browser loads JupyterLab, where `hostname` is the name of the computer running docker and `token` is the secret token printed in the console. Docker destroys the container after notebook server exit, but any files written to `/workdir` in the container remain intact on the host.

    docker run --rm -p 10000:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/workdir isbjornlabs/fastai-notebook:20190419

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
