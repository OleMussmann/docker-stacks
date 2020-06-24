# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=isbjornlabs/minimal-notebook-cuda10.2:2020-06-24
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
    'automat==0.8.0' \
    'basemap==1.2.0' \
    'bcolz==1.2.1' \
    'beautifulsoup4==4.9.1' \
    'bokeh==2.1.0' \
    'cloudpickle==1.4.1' \
    'configobj==5.0.6' \
    'constantly==15.1.0' \
    'cython==0.29.20' \
    'cython==0.29.20' \
    'dask==2.19.0' \
    'dill==0.3.1.1' \
    'freexl==1.0.5' \
    'ftfy==5.7' \
    'gettext==0.19.8.1' \
    'graphviz==2.42.3' \
    'grpcio==1.27.2' \
    'h5py==2.10.0' \
    'hdf5==1.10.4' \
    'hyperlink==19.0.0' \
    'incremental==17.5.0' \
    'ipywidgets==7.5.1' \
    'ipympl==0.3.3' \
    'jbig==2.1' \
    'libboost==1.71.0' \
    'libnetcdf==4.7.3' \
    'libpq==12.2' \
    'libspatialite==4.3.0a' \
    'lxml==4.5.1' \
    'mako==1.1.3' \
    'markdown==3.1.1' \
    'markupsafe==1.1.1' \
    'matplotlib==3.2.1' \
    'mkl-include==2020.1' \
    'networkx==2.4' \
    'nodejs==10.13.0' \
    'numba==0.49.1' \
    'numexpr==2.7.1' \
    'oauthlib==3.1.0' \
    'pandas==1.0.5' \
    'patsy==0.5.1' \
    'pbr==5.4.4' \
    'prometheus_client==0.8.0' \
    'protobuf==3.12.3' \
    'pycrypto==2.6.1' \
    'pyyaml==5.3.1' \
    'reportlab==3.5.26' \
    'scikit-image==0.16.2' \
    'scikit-learn==0.23.1' \
    'scipy==1.4.1' \
    'seaborn==0.10.1' \
    'simplegeneric==0.8.1' \
    'sqlalchemy==1.3.17' \
    'statsmodels==0.11.1' \
    'sympy==1.6' \
    'toml==0.10.1' \
    'werkzeug==1.0.1' \
    'xerces-c==3.2.2' \
    'xlrd==1.2.0' \
    'conda-forge::altair==4.1.0' \
    'conda-forge::blas==2.14=openblas' \
    'conda-forge::blinker==1.4' \
    'conda-forge::geos==3.7.1' \
    'conda-forge::giflib==5.2.1' \
    'conda-forge::httplib2==0.18.1' \
    'conda-forge::jsonpatch==1.24' \
    'conda-forge::jsonpointer==2.0' \
    'conda-forge::kealib==1.4.10' \
    'conda-forge::libdap4==3.20.6' \
    'conda-forge::mkl_fft==1.1.0' \
    'conda-forge::mkl_random==1.1.0' \
    'conda-forge::mock==4.0.2' \
    'conda-forge::netifaces==0.10.9' \
    'conda-forge::proj4==5.2.0' \
    'conda-forge::pyjwt==1.7.1' \
    'conda-forge::pyproj==1.9.6' \
    'conda-forge::pyshp==2.1.0' \
    'conda-forge::simplejson==3.17.0' \
    'conda-forge::awscli==1.18.85' \
    'conda-forge::feather-format==0.4.1' \
    'conda-forge::importlib_metadata==1.6.1' \
    'conda-forge::mechanicalsoup==0.12.0' \
    'conda-forge::plotnine==0.7.0' \
    'conda-forge::progressbar2==3.51.3' \
    'conda-forge::pyarrow==0.11.1' \
    'plotly::plotly==4.8.1' \
    'plotly::plotly_express==0.4.1' \
    && conda remove --quiet --yes --force qt pyqt && \
    conda clean --all -f -y && \
    # pip installs
    pip install --no-cache-dir \
    'kaggle==1.5.6' \
    'opencv-contrib-python-headless==4.2.0.34' \
    'pygal==2.4.0' \
    'sklearn-pandas==1.8.0' \
    && rm -rf /home/$NB_USER/.local && \
    # Activate ipywidgets extension in the environment that runs the notebook server
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    # Also activate ipywidgets extension for JupyterLab
    # Check this URL for most recent compatibilities
    # https://github.com/jupyter-widgets/ipywidgets/tree/master/packages/jupyterlab-manager
    jupyter labextension install @jupyter-widgets/jupyterlab-manager@^2.0.0 && \
    jupyter labextension install @bokeh/jupyter_bokeh@^2.0.2 && \
    # more ram needed for jupyterlab-plotly
    export NODE_OPTIONS=--max-old-space-size=4096 && \
    jupyter labextension install jupyterlab-plotly@^4.8.1 && \
    jupyter labextension install plotlywidget@^4.8.1 && \
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
