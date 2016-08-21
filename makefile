
SHELL := /bin/bash
VIRTUAL_ENV ?= $(abspath .pyenv)
VENV := $(VIRTUAL_ENV)
PYTHON := python3
PIP := $(VENV)/bin/pip
NODE := $(VENV)/bin/node
NODE_VERSION := 4.4.7
NPM := $(VENV)/bin/npm
BOWER := $(abspath node_modules/.bin/bower)
GULP := $(abspath node_modules/.bin/gulp)
INPUTDIR := $(abspath src)
OUTPUTDIR := $(abspath dist)
PELICAN := $(VENV)/bin/pelican
PELICAN_PLUGINS := $(abspath plugins)
PELICAN_CONFIG := $(INPUTDIR)/config.py
PELICANOPTS=
DEBUG ?= 1

ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

export VIRTUAL_ENV
export DEBUG

include site.properties

export PELICAN_AUTHOR
export PELICAN_SITENAME
export PELICAN_SITEURL

.PHONY: venv nodejs install start serve pelican site publish clean nuke

venv:
	@if [ ! -e $(VENV) ]; then virtualenv -v -p $(PYTHON) $(VENV); fi
	@$(PIP) install -U pip
	@$(PIP) install -r requirements.txt

nodejs:
	@if [ ! -e $(NODE) ]; then \
		echo "Installing nodejs. This may take a few minutes." && $(VENV)/bin/nodeenv -v -p --node=$(NODE_VERSION); \
	fi

install: venv nodejs
	@source $(VENV)/bin/activate && $(NPM) install && $(BOWER) install

develop:
	@source $(VENV)/bin/activate && $(GULP)

pelican:
	@$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PELICAN_CONFIG) $(PELICANOPTS)

site:
	@source $(VENV)/bin/activate && $(GULP) build

publish:
	@make site DEBUG=0 && s3cmd sync $(OUTPUTDIR)/ s3://$(S3_BUCKET) --acl-public --delete-removed --guess-mime-type

environ:
	@echo "VIRTUAL_ENV = $(VIRTUAL_ENV)"
	@echo "DEBUG = $(DEBUG)"
	@source $(VENV)/bin/activate && $(GULP) environ

clean:
	@rm -rf $(OUTPUTDIR)
	@rm -rf src/theme/assets

nuke: clean
	@rm -rf $(VIRTUAL_ENV)
	@rm -rf ./node_modules
	@rm -rf ./bower_components

