
SHELL := /bin/bash
GREP_AWS_CREATE_KEY := grep -s "^stout," $(HOME)/.aws/credentials.csv | awk -F "," '{ print $$2 }'
GREP_AWS_CREATE_SECRET := grep -s "^stout," $(HOME)/.aws/credentials.csv | awk -F "," '{ print $$3 }'
GREP_AWS_DEPLOY_KEY := grep -s "^stout-deploy," $(HOME)/.aws/credentials.csv | awk -F "," '{ print $$2 }'
GREP_AWS_DEPLOY_SECRET := grep -s "^stout-deploy," $(HOME)/.aws/credentials.csv | awk -F "," '{ print $$3 }'


include site.properties

export PELICAN_AUTHOR
export PELICAN_SITENAME
export PELICAN_SITEURL

.PHONY: install develop publish clean nuke environ stout.create stout.deploy deploy

install:
	@npm install

# call the default gulp task (build assets, build site, start web server and watch files)
develop:
	@npm start

# build the site for production (called by the deploy command)
publish:
	@npm run-script publish

# stout creates the s3 bucket and cloudfront distribution correctly
stout.create:
	@stout create --bucket $(S3_BUCKET) --key $$($(GREP_AWS_CREATE_KEY)) --secret '$$($(GREP_AWS_CREATE_SECRET))'

# ...but has a problem parsing django syntax in blog posts so this fails
stout.deploy:
	@stout deploy --bucket $(S3_BUCKET) --key $$($(GREP_AWS_DEPLOY_KEY)) --secret '$$($(GREP_AWS_DEPLOY_SECRET))' --root $(OUTPUTDIR)

# ...so use s3cmd instead (expects a .s3cfg file in $PWD or $HOME, use the credentials of the user created by stout)
s3.deploy:
	@s3cmd sync build/ s3://$(S3_BUCKET) --acl-public --delete-removed --guess-mime-type --config=$(PWD)/.s3cfg

deploy: publish s3.deploy

