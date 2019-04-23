# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
.PHONY: docs help test

SHELL:=bash
OWNER:=isbjornlabs
DATE_STRING:=$(shell date +%Y-%m-%d)

# Need to list the images in build dependency order
ALL_IMAGE_FLAVOURS:=base-notebook \
	minimal-notebook \
	scipy-notebook \
	fastai-notebook \
	tensorflow-notebook \
	mxnet-notebook

ALL_CUDA_VERSIONS:=9.2 \
	10.0 \
	10.1

ALL_IMAGES:=$(foreach I,$(ALL_IMAGE_FLAVOURS), \
	$(foreach C,$(ALL_CUDA_VERSIONS),$I-cuda$C))

CUDNN:=7

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo "OleMussmann/docker-stacks"
	@echo "====================="
	@echo "Replace % with a stack name (e.g., make build/minimal-notebook)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build/%: DARGS?=
build/%: ## build the latest image for a stack
	if test $(findstring :,$(notdir $@)) ; then \
		./dev/build-notebook.sh $(notdir $@) $(OWNER) $(DARGS) ; \
	else \
		./dev/build-notebook.sh $(notdir $@):$(DATE_STRING) $(OWNER) $(DARGS) ; \
	fi

list-images: ## list all buildable docker images
	@for framework in $$(ls notebooks) ; do \
		notebooks=$$(ls notebooks/$$framework) ; \
		for notebook in $$notebooks ; do \
			available_images+=$$notebook-$$framework" " ; \
		done ; \
	done ; \
	for image in $$available_images ; do \
		echo $$image; \
	done ;

build-stable: $(foreach I,$(ALL_IMAGES),build/$(I) ) ## build all stable stacks
build-experimental: $(foreach I,$(ALL_IMAGES),build/$(I)\:experimental ) ## build all experimental stacks
dev/%: ARGS?=
dev/%: DARGS?=
dev/%: PORT?=8888
dev/%: ## run a foreground container for a stack
	docker run -it --rm -p $(PORT):8888 $(DARGS) $(OWNER)/$(notdir $@) $(ARGS)

dockerfile/%: ## generate a new dockerfile for a stack, alse enabling a disabled image
	./dev/make_dockerfile.py $(notdir $@) $(DATE_STRING) $(CUDNN)

dockerfiles-stable:	$(foreach I,$(ALL_IMAGES),dockerfile/$(I) ) ## generate version-pinned dockerfiles using version numbers from experimental

dockerfiles-experimental:	$(foreach I,$(ALL_IMAGES),dockerfile/$(I)\:experimental ) ## generate experimental dockerfiles, only needed if you tweaked the templates

disable/%: ## disable an image, e.g. for incompatibility reasons
	./dev/disable_image.py $(notdir $@) $(DATE_STRING) $(CUDNN)

#TODO

#build-test-stable: $(foreach I,$(ALL_IMAGES),build/$(I) test/$(I) ) ## build and test all stable stacks
#build-test-experimental: $(foreach I,$(ALL_IMAGES),build/$(I)\:experimental test/$(I)\:experimental ) ## build and test all experimental stacks

#publish-stable:
#publish-experimental:

#test/%: ## run tests against a stack
#	@TEST_IMAGE="$(OWNER)/$(notdir $@)" pytest test

#test/base-notebook: ## test supported options in the base notebook
#	@TEST_IMAGE="$(OWNER)/$(notdir $@)" pytest test notebooks/cuda9.2/base-notebook/test

#dev-env: ## install libraries required to build docs and run tests
#	pip install --user -r requirements-dev.txt

#test-pinned: ## run tests against all version-pinned notebooks
#test-experimental: ## run tests against all experimental notebooks
