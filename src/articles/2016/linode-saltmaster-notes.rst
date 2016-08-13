
Install a SaltStack master on Linode
####################################

:date: 2016-08-07 08:00
:category: Ops
:author: averagehuman
:tags: Ansible


.. container:: callout primary

    Notes on creating a salt master on linode using a vagrant plugin.


How to provision a provisioner?
-------------------------------

`Saltstack`_ is an automation and configuration management tool with a master/slave
architecture - a single salt master creates, configures and orchestrates many salt
"minions". I've always wondered how you bootstrap this setup, ie. how do you automate
the creation and configuration of the saltmaster itself? Since salt is a python
package the installation process is a familiar one:

+ create and activate a virtualenv
+ install requirements
+ run ``python setup.py install``
  
And there is a `salt-bootstrap`_ script which will encapsulate this process. It's a
multiplatform shell script that will detect the operating system, download and install
the salt package and configure the system as either a master or minion (or both).

The following are some notes on setting up a `Linode`_ box as a saltmaster via `vagrant`_
and a `vagrant-linode`_ plugin. I'm using `ansible`_ to orchestrate the actual
provisioning of the remote environment.

Why vagrant? Obviously it's not essential here, but it's a familiar interface and a
way of transparently handling the necessary calls to the linode api. And there
are similar plugins for AWS, Digital Ocean, Vultr etc. so it wouldn't take much
to move to other vps providers.


Prerequisites
-------------

First you need to create an authentication key for the `Linode API`_ and you can do
that either via the web interface (**My Profile > API Keys**), or by a GET or POST to
the **user.getapikey** endpoint:

.. code-block:: bash

    $ curl 'https://api.linode.com/?api_action=user.getapikey&username=USERNAME&password=PASSWORD'

replacing USERNAME and PASSWORD with your linode login credentials.

Now create a new keypair:

.. code-block:: bash

    $ ssh-keygen -C "saltmaster key" -b 4096 -f ~/.ssh/saltmaster.key

And assuming that you already have vagrant available, you will also need to
install the `vagrant-linode`_ plugin:

.. code-block:: bash

    $ vagrant plugin install vagrant-linode


.. _saltstack: https://saltstack.com
.. _salt-bootstrap: https://github.com/saltstack/salt-bootstrap
.. _vagrant: https://www.vagrantup.com/
.. _vagrant-linode: https://github.com/displague/vagrant-linode
.. _linode: https://www.linode.com/
.. _linode api: https://www.linode.com/api
.. _ansible: https://www.ansible.com/
.. _this document: https://www.linode.com/docs/applications/configuration-management/vagrant-linode-environments
.. _use the salt-bootstrap script: https://github.com/saltstack/salt-bootstrap

