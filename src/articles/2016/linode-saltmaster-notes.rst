
Install a SaltStack master on Linode
####################################

:date: 2016-08-07 08:00
:category: Ops
:author: averagehuman
:tags: Ansible


.. container:: callout primary

    Notes on creating a salt master node on linode using a vagrant plugin.


How to provision a provisioner?
-------------------------------

`Saltstack`_ is an automation and configuration management tool with a master/slave
architecture - a single salt master creates, configures and orchestrates many salt
"minions". To create the saltmaster there is a multiplatform `salt-bootstrap script`_

The following are some notes on setting up a `Linode`_
box as a saltmaster using a `vagrant-linode`_ plugin together with `ansible`_ as the
provisioner.

There are similar plugins for AWS, Digital Ocean, Vultr etc. 


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

You also need to install the `vagrant-linode`_ plugin:

.. code-block:: bash

    $ vagrant plugin install vagrant-linode


.. _saltstack: https://saltstack.com
.. _vagrant-linode: https://github.com/displague/vagrant-linode
.. _linode: https://www.linode.com/
.. _linode api: https://www.linode.com/api
.. _ansible: https://www.ansible.com/
.. _this document: https://www.linode.com/docs/applications/configuration-management/vagrant-linode-environments
.. _use the salt-bootstrap script: https://github.com/saltstack/salt-bootstrap

