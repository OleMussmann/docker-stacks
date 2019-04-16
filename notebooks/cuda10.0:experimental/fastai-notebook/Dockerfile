# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
#ARG BASE_CONTAINER=isbjornlabs/scipy-notebook-cuda10.0:20190322.1
ARG BASE_CONTAINER=isbjornlabs/scipy-notebook-cuda10.0:experimental
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Install fast.ai and pytorch
# Install GPU-optimized JPEG encoder, see:
# https://github.com/fastai/fastai#conda-install
RUN conda install --quiet --yes \
    -c pytorch -c fastai 'fastai' && \
    #    fastai_deps=$(conda list | \
    #      grep ^fastai | \
    #      awk '{system("conda search --info -c fastai "$1"="$2)}' | \
    #      grep " - " | \
    #      awk '{print $2}' | \
    #      tr '\n' ' ') && \
    #    conda uninstall --yes $fastai_deps && \
    conda uninstall --force jpeg libtiff -y && \
    conda install -c conda-forge libjpeg-turbo && \
    #    conda install --quiet --yes -c main $fastai_deps && \
    conda clean --all && \
    CC="cc -mavx2" pip install --no-cache-dir -U \
    --force-reinstall --no-binary :all: --compile pillow-simd && \
    rm -rf /home/$NB_USER/.local && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
