# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=isbjornlabs/scipy-notebook-cuda10.1:2019-04-21
FROM $BASE_CONTAINER

LABEL maintainer="Ole Mussmann <ole@isbjornlabs.com>"
ENTRYPOINT ["echo", "### WARNING\nAs of 2019-04-19, tensorflow is not yet compatible with CUDA 10.1.\nPlease use \"tensorflow-notebook-cuda10.0\" instead.\n"]