# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=isbjornlabs/scipy-notebook-cuda10.1:experimental
FROM $BASE_CONTAINER

LABEL maintainer="Ole Mussmann <ole@isbjornlabs.com>"

# Install Tensorflow
RUN pip install --no-cache-dir \
      'mxnet-cu101mkl' && \
      rm -rf /home/$NB_USER/.local && \
      fix-permissions $CONDA_DIR && \
      fix-permissions /home/$NB_USER
