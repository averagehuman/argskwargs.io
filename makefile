
SHELL := /bin/bash
VIRTUAL_ENV ?= $(abspath .pyenv)
VENV := $(VIRTUAL_ENV)
PYTHON := python3
PIP := $(VENV)/bin/pip
NODE := $(VENV)/bin/node
NODE_VERSION := 6.9.1
NPM := $(VENV)/bin/npm
BOWER := $(abspath node_modules/.bin/bower)
GULP := $(abspath node_modules/.bin/gulp)
INPUTDIR := $(abspath src)
BUILDDIR := $(abspath build)
OUTPUTDIR := $(abspath dist)
PELICAN := $(VENV)/bin/pelican
PELICAN_PLUGINS := $(abspath src/plugins)
PELICAN_CONFIG := $(INPUTDIR)/config.py
GREP_AWS_CREATE_KEY := grep -s "^stout," $(HOME)/.aws/credentials.csv | awk -F "," '{ print $$3 }'
GREP_AWS_CREATE_SECRET := grep -s "^stout," $(HOME)/.aws/credentials.csv | awk -F "," '{ print $$4 }'
GREP_AWS_DEPLOY_KEY := grep -s "^stout-deploy," $(HOME)/.aws/credentials.csv | awk -F "," '{ print $$3 }'
GREP_AWS_DEPLOY_SECRET := grep -s "^stout-deploy," $(HOME)/.aws/credentials.csv | awk -F "," '{ print $$4 }'


export VIRTUAL_ENV

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
		echo "Installing nodejs." && $(VENV)/bin/nodeenv -v -p --node=$(NODE_VERSION); \
	fi

install: venv nodejs
	@source $(VENV)/bin/activate && $(NPM) install && $(BOWER) install

# call the default gulp task (build assets, build site, start web server and watch files)
develop:
	@source $(VENV)/bin/activate && DEBUG=1 $(GULP)

# build the site for development (called by gulp task)
pelican:
	@DEBUG=1 $(PELICAN) $(INPUTDIR) -o $(BUILDDIR) -s $(PELICAN_CONFIG) -D

# build the site for production (called by the deploy command)
publish:
	@rm -rf $(OUTPUTDIR)
	@source $(VENV)/bin/activate && DEBUG=0 $(GULP) build
	@DEBUG=0 $(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PELICAN_CONFIG)

# stout creates the s3 bucket and cloudfront distribution correctly
stout.create:
	@source $(VENV)/bin/activate && stout create --bucket $(S3_BUCKET) --key $$($(GREP_AWS_CREATE_KEY)) --secret '$$($(GREP_AWS_CREATE_SECRET))'

# ...but has a problem parsing django syntax in blog posts so this fails
stout.deploy:
	@source $(VENV)/bin/activate && stout deploy --bucket $(S3_BUCKET) --key $$($(GREP_AWS_DEPLOY_KEY)) --secret '$$($(GREP_AWS_DEPLOY_SECRET))' --root $(OUTPUTDIR)

# ...so use s3cmd instead (expects a .s3cfg file in the current directory, use the credentials of the user created by stout)
s3.deploy:
	@s3cmd sync $(OUTPUTDIR)/ s3://$(S3_BUCKET) --acl-public --delete-removed --guess-mime-type --config=$(PWD)/.s3cfg

deploy: publish s3.deploy

environ:
	@echo "VIRTUAL_ENV = $(VIRTUAL_ENV)"
	@echo "DEBUG = $(DEBUG)"
	@echo "AWS_KEY = $$($(GREP_AWS_KEY))"
	@echo "AWS_SECRET = $$($(GREP_AWS_SECRET))"
	@echo "S3_BUCKET = $(S3_BUCKET)"

clean:
	@rm -rf $(OUTPUTDIR)
	@rm -rf src/theme/assets

nuke: clean
	@rm -rf $(VIRTUAL_ENV)
	@rm -rf ./node_modules
	@rm -rf ./bower_components

