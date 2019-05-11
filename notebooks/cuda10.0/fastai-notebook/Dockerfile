# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=isbjornlabs/scipy-notebook-cuda10.0:2019-05-11
FROM $BASE_CONTAINER

LABEL maintainer="Ole Mussmann <ole@isbjornlabs.com>"

# Install fast.ai and pytorch
# Install GPU-optimized JPEG encoder, see:
# https://github.com/fastai/fastai#conda-install
RUN conda install --quiet --yes \
    -c pytorch -c fastai 'fastai==1.0.52' && \
    conda uninstall --force jpeg libtiff -y && \
    conda install -c conda-forge 'libjpeg-turbo==2.0.2' && \
    conda clean --all && \
    CC="cc -mavx2" pip install --no-cache-dir -U \
    --force-reinstall --no-binary :all: --compile 'pillow-simd==5.3.0.post1' && \
    pip install 'torchtext==0.3.1' && \
    rm -rf /home/$NB_USER/.local && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
