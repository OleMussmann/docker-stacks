# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
.PHONY: docs help test

SHELL:=bash
OWNER:=isbjornlabs
DATE_STRING:=$(date +%Y%m%d)

# Need to list the images in build dependency order
ALL_IMAGES:=base-notebook \
	minimal-notebook \
	scipy-notebook \
	fastai-notebook \
	tensorflow-notebook \
	mxnet-notebook

ALL_CUDA_VERSIONS:=9.2 \
	10.0 \
	10.1

CUDNN:=7

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo "OleMussmann/docker-stacks"
	@echo "====================="
	@echo "Replace % with a stack name (e.g., make build/minimal-notebook)"
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#image_name_with_tag=$(notdir $@)
#image_name_without_tag=$(firstword $(subst :, ,$(image_name_with_tag)))
#tag=$(subst $(image_name_without_tag):,,$(image_name_with_tag))
#cuda=$(lastword $(subst -, ,$(image_name_without_tag)))
#notebook_folder=$(subst -$(cuda),,$(image_name_without_tag))

build/%: DARGS?=
build/%: ## build the latest image for a stack
	if test $(findstring :,$(notdir $@)) ; then \
		./dev/build-notebook.sh $(notdir $@) $(DARGS) ; \
	else \
		./dev/build-notebook.sh $(notdir $@):$(DATE_STRING) $(DARGS) ; \
	fi

#	image_name_with_tag=$(notdir $@) ; \
#	image_name_without_tag=$(firstword $(subst :, ,$$image_name_with_tag)) ; \
#	if [ "$(image_name_without_tag)" = "base-notebook" ] ; then \
#		pull="--pull" ; \
#	else \
#		pull="" ; \
#	fi ; \
#	echo "pull: "$$pull ; \
#	if test $(findstring :experimental,$(image_name_with_tag)) ; then \
#		echo "building experimental image" $(image_name_with_tag) \
#		"in folder" $(cuda)":experimental/"$(notebook_folder) ; \
#		echo $(tag) ; \
#	else \
#	echo "building stable image" $(image_name_without_tag):$(tag) \
#		"in folder" $(cuda)"/"$(notebook_folder) ; \
#		echo $(tag) ; \
#	fi ; \
#	echo ; \
#	echo $$image_name_with_tag ; \
#	echo $$image_name_without_tag ;

#	@if [ "$(findstring :,$(notdir $@))" == ":" ] ; then \
#		echo "building experimental image" $(notdir $@) ; \
#		docker build $(DARGS) --rm --force-rm \
#			-t $(OWNER)/$(notdir $@):experimental \
#			./$(notdir $@) ; \
#	else \
#		echo "building stable image" $(notdir $@) ; \
#		docker build $(DARGS) --rm --force-rm \
#			-t $(OWNER)/$(notdir $@):$(DATE_STRING) \
#			-t $(OWNER)/$(notdir $@):latest \
#			./$(notdir $@) ; \
#	fi \

#	echo $(notdir $@)
#	docker build $(DARGS) --rm --force-rm \
#		-t $(OWNER)/$(notdir $@):$(DATE_STRING) \
#		-t $(OWNER)/$(notdir $@):latest \
#		./$(notdir $@)

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

echo/%:
	@echo $@

build-stable: $(foreach I,$(ALL_IMAGES),$(foreach C,$(ALL_CUDA_VERSIONS),build/$(I)-cuda$(C) )) ## build all stable stacks
build-experimental: $(foreach I,$(ALL_IMAGES),$(foreach C,$(ALL_CUDA_VERSIONS),build/$(I)-cuda$(C)\:experimental )) ## build all experimental stacks
build-test-stable: $(foreach I,$(ALL_IMAGES),$(foreach C,$(ALL_CUDA_VERSIONS),build/$(I)-cuda$(C) test/$(I)-cuda$(C) )) ## build and test all stable stacks
build-test-experimental: $(foreach I,$(ALL_IMAGES),$(foreach C,$(ALL_CUDA_VERSIONS),build/$(I)-cuda$(C)\:experimental test/$(I)-cuda$(C)\:experimental )) ## build and test all experimental stacks

#publish-stable:
#publish-experimental:

dev/%: ARGS?=
dev/%: DARGS?=
dev/%: PORT?=8888
dev/%: ## run a foreground container for a stack
	docker run -it --rm -p $(PORT):8888 $(DARGS) $(OWNER)/$(notdir $@) $(ARGS)

dev-env: ## install libraries required to build docs and run tests
	pip install -r requirements-dev.txt

dockerfile/%: ## generate new dockerfiles for a stack
	./dev/make_dockerfile.py $(notdir $@) $(DATE_STRING) $(CUDNN)
dockerfiles-stable: ## generate new version-pinned, stable dockerfiles using the latest version numbers from experimental branch
	$(foreach I,$(ALL_IMAGES),$(foreach C,$(ALL_CUDA_VERSIONS),dockerfile/$(I)-cuda$(C) ))
dockerfiles-experimental: ## generate new experimental dockerfiles, only needed if you tweaked the templates
	$(foreach I,$(ALL_IMAGES),$(foreach C,$(ALL_CUDA_VERSIONS),dockerfile/$(I)-cuda$(C)\:experimental ))

test/%: ## run tests against a stack
	@TEST_IMAGE="$(OWNER)/$(notdir $@)" pytest test

test/base-notebook: ## test supported options in the base notebook
	@TEST_IMAGE="$(OWNER)/$(notdir $@)" pytest test base-notebook/test

#test-pinned: ## run tests against all version-pinned notebooks
#test-experimental: ## run tests against all experimental notebooks
