# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
#ARG BASE_CONTAINER=isbjornlabs/scipy-notebook-cuda10.0:20190322.1
ARG BASE_CONTAINER=isbjornlabs/scipy-notebook-cuda10.0:experimental
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Install Tensorflow

RUN pip install --no-cache-dir \
      'mxnet-cu100mkl' && \
      rm -rf /home/$NB_USER/.local && \
      fix-permissions $CONDA_DIR && \
      fix-permissions /home/$NB_USER
