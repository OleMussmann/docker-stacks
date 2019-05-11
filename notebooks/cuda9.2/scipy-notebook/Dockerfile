# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=isbjornlabs/minimal-notebook-cuda9.2:2019-05-11
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
    'automat==0.7.0' \
    'basemap==1.2.0' \
    'bcolz==1.2.1' \
    'beautifulsoup4==4.7.1' \
    'bokeh==1.1.0' \
    'cloudpickle==1.0.0' \
    'configobj==5.0.6' \
    'constantly==15.1.0' \
    'cython==0.29.7' \
    'cython==0.29.7' \
    'dask==1.2.2' \
    'dill==0.2.9' \
    'freexl==1.0.5' \
    'ftfy==5.5.1' \
    'gettext==0.19.8.1' \
    'graphviz==2.40.1' \
    'grpcio==1.16.1' \
    'h5py==2.9.0' \
    'hdf5==1.10.4' \
    'hyperlink==19.0.0' \
    'incremental==17.5.0' \
    'ipywidgets==7.4.2' \
    'jbig==2.1' \
    'libboost==1.67.0' \
    'libnetcdf==4.6.1' \
    'libpq==11.2' \
    'libspatialite==4.3.0a' \
    'lxml==4.3.3' \
    'mako==1.0.9' \
    'markdown==3.1' \
    'markupsafe==1.1.1' \
    'matplotlib==3.0.3' \
    'mkl-include==2019.3' \
    'networkx==2.3' \
    'numba==0.43.1' \
    'numexpr==2.6.9' \
    'oauthlib==3.0.1' \
    'pandas==0.24.2' \
    'patsy==0.5.1' \
    'pbr==5.1.3' \
    'prometheus_client==0.6.0' \
    'protobuf==3.7.1' \
    'pycrypto==2.6.1' \
    'pyyaml==3.13' \
    'reportlab==3.5.19' \
    'scikit-image==0.15.0' \
    'scikit-learn==0.20.3' \
    'scipy==1.2.1' \
    'seaborn==0.9.0' \
    'simplegeneric==0.8.1' \
    'sqlalchemy==1.3.3' \
    'statsmodels==0.9.0' \
    'sympy==1.4' \
    'werkzeug==0.15.2' \
    'xerces-c==3.2.2' \
    'xlrd==1.2.0' \
    'conda-forge::altair==3.0.1' \
    'conda-forge::blas==2.8=openblas' \
    'conda-forge::blinker==1.4' \
    'conda-forge::geos==3.7.1' \
    'conda-forge::giflib==5.1.9' \
    'conda-forge::httplib2==0.12.3' \
    'conda-forge::jsonpatch==1.23' \
    'conda-forge::jsonpointer==2.0' \
    'conda-forge::kealib==1.4.10' \
    'conda-forge::libdap4==3.19.1' \
    'conda-forge::mkl_fft==1.0.13' \
    'conda-forge::mkl_random==1.0.4' \
    'conda-forge::mock==3.0.5' \
    'conda-forge::netifaces==0.10.8' \
    'conda-forge::proj4==5.2.0' \
    'conda-forge::pyjwt==1.7.1' \
    'conda-forge::pyproj==1.9.6' \
    'conda-forge::pyshp==2.1.0' \
    'conda-forge::simplejson==3.16.0' \
    'conda-forge::awscli==1.16.156' \
    'conda-forge::feather-format==0.4.0' \
    'conda-forge::importlib_metadata==0.11' \
    'conda-forge::mechanicalsoup==0.11.0' \
    'conda-forge::plotnine==0.5.1' \
    'conda-forge::progressbar2==3.38.0' \
    'conda-forge::pyarrow==0.13.0' \
    'plotly::plotly==3.9.0' \
    'plotly::plotly_express==0.2.0' \
    && conda remove --quiet --yes --force qt pyqt && \
    conda clean --all && \
    # pip installs
    pip install --no-cache-dir \
    'kaggle==1.5.3' \
    'opencv-contrib-python-headless==4.1.0.25' \
    'pygal==2.4.0' \
    'sklearn-pandas==1.8.0' \
    && rm -rf /home/$NB_USER/.local && \
    # Activate ipywidgets extension in the environment that runs the notebook server
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    # Also activate ipywidgets extension for JupyterLab
    # Check this URL for most recent compatibilities
    # https://github.com/jupyter-widgets/ipywidgets/tree/master/packages/jupyterlab-manager
    jupyter labextension install @jupyter-widgets/jupyterlab-manager@^0.38.1 && \
    jupyter labextension install jupyterlab_bokeh@^0.6.3 && \
    jupyter labextension install @jupyterlab/plotly-extension@^0.18.2 && \
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
