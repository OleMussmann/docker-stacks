# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=isbjornlabs/minimal-notebook-cuda10.1:experimental
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
    'automat' \
    'basemap' \
    'bcolz' \
    'beautifulsoup4' \
    'bokeh' \
    'cloudpickle' \
    'configobj' \
    'constantly' \
    'cython' \
    'cython' \
    'dask' \
    'dill' \
    'freexl' \
    'ftfy' \
    'gettext' \
    'graphviz' \
    'grpcio' \
    'h5py' \
    'hdf5' \
    'hyperlink' \
    'incremental' \
    'ipywidgets' \
    'jbig' \
    'libboost' \
    'libnetcdf' \
    'libpq' \
    'libspatialite' \
    'lxml' \
    'mako' \
    'markdown' \
    'markupsafe' \
    'matplotlib' \
    'mkl-include' \
    'networkx' \
    'numba' \
    'numexpr' \
    'oauthlib' \
    'pandas' \
    'patsy' \
    'pbr' \
    'prometheus_client' \
    'protobuf' \
    'pycrypto' \
    'pyyaml' \
    'reportlab' \
    'scikit-image' \
    'scikit-learn' \
    'scipy' \
    'seaborn' \
    'simplegeneric' \
    'sqlalchemy' \
    'statsmodels' \
    'sympy' \
    'werkzeug' \
    'xerces-c' \
    'xlrd' \
    'conda-forge::altair' \
    'conda-forge::blas=*=openblas' \
    'conda-forge::blinker' \
    'conda-forge::geos' \
    'conda-forge::giflib' \
    'conda-forge::httplib2' \
    'conda-forge::jsonpatch' \
    'conda-forge::jsonpointer' \
    'conda-forge::kealib' \
    'conda-forge::libdap4' \
    'conda-forge::mkl_fft' \
    'conda-forge::mkl_random' \
    'conda-forge::mock' \
    'conda-forge::netifaces' \
    'conda-forge::proj4' \
    'conda-forge::pyjwt' \
    'conda-forge::pyproj' \
    'conda-forge::pyshp' \
    'conda-forge::simplejson' \
    'conda-forge::awscli' \
    'conda-forge::feather-format' \
    'conda-forge::importlib_metadata' \
    'conda-forge::mechanicalsoup' \
    'conda-forge::plotnine' \
    'conda-forge::progressbar2' \
    'conda-forge::pyarrow' \
    'plotly::plotly' \
    'plotly::plotly_express' \
    && conda remove --quiet --yes --force qt pyqt && \
    conda clean --all && \
    # pip installs
    pip install --no-cache-dir \
    'kaggle' \
    'opencv-contrib-python-headless' \
    'pygal' \
    'sklearn-pandas' \
    && rm -rf /home/$NB_USER/.local && \
    # Activate ipywidgets extension in the environment that runs the notebook server
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    # Also activate ipywidgets extension for JupyterLab
    # Check this URL for most recent compatibilities
    # https://github.com/jupyter-widgets/ipywidgets/tree/master/packages/jupyterlab-manager
    jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
    jupyter labextension install jupyterlab_bokeh && \
    jupyter labextension install @jupyterlab/plotly-extension && \
    jupyter lab build && \
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
