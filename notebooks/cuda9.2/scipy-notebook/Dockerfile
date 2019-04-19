# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=isbjornlabs/minimal-notebook-cuda9.2:20190419
FROM $BASE_CONTAINER

LABEL maintainer="Ole Mussmann <ole@isbjornlabs.com>"

USER root

# ffmpeg for matplotlib anim
RUN apt-get update && \
      apt-get install -y --no-install-recommends \
      software-properties-common && \
      add-apt-repository ppa:neovim-ppa/stable && \
      apt-get update && apt-get install -y --no-install-recommends \
      neovim \
      htop \
      ffmpeg \
      tmux \
      tree && \
      rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Install Python 3 packages
# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
# use notebook-friendly backends in these images
RUN conda install --quiet --yes \
    'conda-forge::blas=*=openblas' \
    'ipywidgets==7.4.2' \
    'pandas==0.24.2' \
    'numexpr==2.6.9' \
    'matplotlib==3.0.3' \
    'scipy==1.2.1' \
    'seaborn==0.9.0' \
    'scikit-learn==0.20.3' \
    'scikit-image==0.14.2' \
    'sympy==1.4' \
    'cython==0.29.7' \
    'patsy==0.5.1' \
    'statsmodels==0.9.0' \
    'cloudpickle==0.8.1' \
    'dill==0.2.9' \
    'dask==1.2.0' \
    'numba==0.43.1' \
    'bokeh==1.1.0' \
    'sqlalchemy==1.3.3' \
    'hdf5==1.10.4' \
    'h5py==2.9.0' \
    'vincent==0.4.4' \
    'beautifulsoup4==4.7.1' \
    'protobuf==3.6.1' \
    'xlrd==1.2.0'  && \
    conda remove --quiet --yes --force qt pyqt && \
    conda clean --all && \
    # Activate ipywidgets extension in the environment that runs the notebook server
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    # Also activate ipywidgets extension for JupyterLab
    # Check this URL for most recent compatibilities
    # https://github.com/jupyter-widgets/ipywidgets/tree/master/packages/jupyterlab-manager
    jupyter labextension install @jupyter-widgets/jupyterlab-manager@^0.38.1 && \
    jupyter labextension install jupyterlab_bokeh@^0.6.3 && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    rm -rf /home/$NB_USER/.node-gyp && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Install facets which does not have a pip or conda package at the moment
RUN cd /tmp && \
    git clone https://github.com/PAIR-code/facets.git && \
    cd facets && \
    jupyter nbextension install facets-dist/ --sys-prefix && \
    cd && \
    rm -rf /tmp/facets && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /home/$NB_USER/.cache/
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    fix-permissions /home/$NB_USER

USER $NB_UID

# folder removal warning
RUN echo "WARNING!\n\nThis home folder will vanish when the docker container is destroyed. Make sure that your working directory is mounted on the host and store your scripts and data there." > ~/WARNING.txt

# prettify command line
RUN echo "\n#prettify command line\nPS1='🐳  \[\033[1;36m\]\u \[\033[1;34m\]\W\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" >> ~/.bashrc