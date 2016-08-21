
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
"minions". But how do you bootstrap this setup, ie. how do you automate the deployment
of the saltmaster itself? Since salt is a python package the installation process is a
familiar one:

+ create and activate a virtualenv
+ install requirements
+ run ``python setup.py install``
  
And it turns out there is a `salt-bootstrap`_ script which will encapsulate this process.
It's a multiplatform shell script that will detect the operating system, download and install
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


The Vagrantfile
---------------

Now with the plugin available, create a `Vagrantfile`_.

Here I'm passing all necessary parameters - such as the linode api key - to vagrant
as shell environment variables (the global `ENV`_ in ruby), then passing those same
variables on to the two provisioners by converting to a dictionary via ``Hash(ENV)``:

.. code-block:: bash

    Vagrant.configure('2') do |config|

        config.vm.provider :linode do |provider, override|

            override.vm.box = 'linode'
            override.vm.box_url = "https://github.com/displague/vagrant-linode/raw/master/box/linode.box"

            # disable default synced folder
            override.vm.synced_folder ".", "/vagrant", disabled: true

            # sync local ./share directory with remote /share directory
            override.vm.synced_folder "share/", "/share", create: true, group: "saltadmin"

            ## SSH Configuration
            override.ssh.username = ENV['LINODE_SSH_USER']
            override.ssh.private_key_path = ENV['LINODE_SSH_KEY_LOCATION']
            override.ssh.port = ENV['LINODE_SSH_PORT']

            #Linode Settings
            provider.token = ENV['LINODE_API_KEY']
            provider.distribution = 'Debian 8'
            provider.datacenter = 'london'
            provider.plan = '2048'
            provider.label = ENV['HOSTNAME']

        end

        config.vm.provision "shell" do |shell|
            shell.path = 'init.sh'
            shell.env = Hash(ENV)
        end

        config.vm.provision "ansible" do |ansible|
            ansible.limit = "all"
            ansible.playbook = ENV['ANSIBLE_PLAYBOOK']
            ansible.inventory_path = ENV['ANSIBLE_INVENTORY']
            ansible.extra_vars = Hash(ENV)
        end
    end


Initial linode creation
-----------------------

Next, in the same directory as the Vagrantfile, create the new box:

.. code-block:: bash

    vagrant up --provider linode --provision-with shell 

We don't invoke the ansible provisioner straightaway in order to run an initial script
to update the hostname and the sshd config:

.. code-block:: bash

    #!/bin/bash

    ##################
    # update hostname
    ##################
    echo "$HOSTNAME" > /etc/hostname

    hostname -F /etc/hostname

    ip=$(ip addr show eth0 | grep -Po 'inet \K[\d.]+')
    grep $HOSTNAME /etc/hosts || echo "$ip $HOSTNAME" >> /etc/hosts

    ######################
    # add privileged group
    ######################
    groupadd saltadmin
    usermod -a -G saltadmin $LINODE_SSH_USER

    #################################
    # update sshd config and restart
    #################################
    origfile=/etc/ssh/sshd_config
    tmpfile=sshd_config.tmp

    cp $origfile $tmpfile

    sed "s/^Port[[:space:]]\+[[:digit:]]\+$/Port $ANSIBLE_SSH_PORT/" -i $tmpfile
    sed "s/^[#]\?PermitRootLogin[[:space:]].*$/PermitRootLogin no/" -i $tmpfile
    sed "s/^[#]\?PasswordAuthentication .*/PasswordAuthentication no/g" -i $tmpfile
    sed "s/^[#]\?ChallengeResponseAuthentication .*/ChallengeResponseAuthentication no/g" -i $tmpfile
    echo "AllowGroups saltadmin" >> $tmpfile
    echo "AddressFamily inet" >> $tmpfile

    mv $tmpfile $origfile

    systemctl restart sshd


Ansible Provisioner
-------------------

Now with the ssh port having been updated to that which the ansible config expects, run
vagrant again:

.. code-block:: bash

    vagrant provision --provision-with ansible

`See github`_ for an ansible setup that installs both `salt`_ and `jenkins`_. A successful
run gives the following output:


.. code-block:: bash

    PLAY [Provision box as saltmaster] *********************************************

    TASK [setup] *******************************************************************
    ok: [dev-saltmaster]

    TASK [common : Generate en_GB.UTF-8 locale] ************************************
    changed: [dev-saltmaster]

    TASK [common : Update System Packages] *****************************************
    changed: [dev-saltmaster]

    TASK [common : Install git client] *********************************************
    changed: [dev-saltmaster]

    TASK [common : Install ufw (firewall)] *****************************************
    changed: [dev-saltmaster]

    TASK [common : Deny all incoming] **********************************************
    ok: [dev-saltmaster]

    TASK [common : Allow incoming ssh] *********************************************
    ok: [dev-saltmaster]

    TASK [common : Allow incoming jenkins web interface] ***************************
    ok: [dev-saltmaster]

    TASK [common : Limit ssh connections] ******************************************
    ok: [dev-saltmaster]

    TASK [common : Restart ufw] ****************************************************
    changed: [dev-saltmaster]

    TASK [common : Remove rpcbind network service] *********************************
    changed: [dev-saltmaster]

    TASK [common : Remove exim4 network service] ***********************************
    changed: [dev-saltmaster]

    TASK [saltmaster : Install saltmaster from bootstrap script] *******************
    changed: [dev-saltmaster]

    TASK [python2 : Install pip] ***************************************************
    changed: [dev-saltmaster]

    TASK [python2 : Install virtualenv] ********************************************
    changed: [dev-saltmaster]

    TASK [docker : Add Docker Group] ***********************************************
    changed: [dev-saltmaster]

    TASK [docker : Add Admin User To Docker Group] *********************************
    changed: [dev-saltmaster]

    TASK [docker : Add Docker Signing Key] *****************************************
    changed: [dev-saltmaster]

    TASK [docker : Add Docker Repo] ************************************************
    changed: [dev-saltmaster]

    TASK [docker : Install Docker] *************************************************
    changed: [dev-saltmaster]

    TASK [docker : Install docker-py] **********************************************
    changed: [dev-saltmaster]

    TASK [nginx : Install nginx] ***************************************************
    changed: [dev-saltmaster]

    TASK [nginx : Remove default nginx site (unlink from /etc/nginx/sites-enabled)] 
    changed: [dev-saltmaster]

    TASK [jenkins : Ensure jenkins directory on docker host] ***********************
    changed: [dev-saltmaster]

    TASK [jenkins : Pull the latest official jenkins docker image] *****************
    changed: [dev-saltmaster]

    TASK [jenkins : Create a container from the jenkins docker image] **************
    changed: [dev-saltmaster]

    TASK [jenkins : Copy systemd service script to start and stop the jenkins container] ***
    changed: [dev-saltmaster]

    TASK [jenkins : Reload systemctl] **********************************************
    changed: [dev-saltmaster]

    TASK [jenkins : Enable the docker-jenkins service] *****************************
    changed: [dev-saltmaster]

    TASK [jenkins : Ensure nginx root directory /var/www/jenkins] ******************
    changed: [dev-saltmaster]

    TASK [jenkins : Ensure nginx log directory /var/log/nginx/jenkins] *************
    changed: [dev-saltmaster]

    TASK [jenkins : Link jenkins images folder to /var/www/jenkins] ****************
    changed: [dev-saltmaster]

    TASK [jenkins : Link jenkins css folder to /var/www/jenkins] *******************
    changed: [dev-saltmaster]

    TASK [jenkins : Link jenkins scripts folder to /var/www/jenkins] ***************
    changed: [dev-saltmaster]

    TASK [jenkins : Link jenkins jsbundles folder to /var/www/jenkins] *************
    changed: [dev-saltmaster]

    TASK [jenkins : Link jenkins help folder to /var/www/jenkins] ******************
    changed: [dev-saltmaster]

    TASK [jenkins : Link jenkins favicon to /var/www/jenkins] **********************
    changed: [dev-saltmaster]

    TASK [jenkins : Link jenkins robots.txt to /var/www/jenkins] *******************
    changed: [dev-saltmaster]

    TASK [jenkins : Copy the jenkins nginx reverse proxy config to /etc/nginx/sites-available] ***
    changed: [dev-saltmaster]

    TASK [jenkins : Link /etc/nginx/sites-available/jenkins to /etc/nginx/sites-enabled] ***
    changed: [dev-saltmaster]

    TASK [jenkins : Reload nginx] **************************************************
    changed: [dev-saltmaster]

    PLAY RECAP *********************************************************************
    dev-saltmaster             : ok=41   changed=36   unreachable=0    failed=0  


.. _salt: https://saltstack.com/
.. _saltstack: https://saltstack.com
.. _salt-bootstrap: https://github.com/saltstack/salt-bootstrap
.. _vagrant: https://www.vagrantup.com/
.. _vagrant-linode: https://github.com/displague/vagrant-linode
.. _linode: https://www.linode.com/
.. _linode api: https://www.linode.com/api
.. _ansible: https://www.ansible.com/
.. _this document: https://www.linode.com/docs/applications/configuration-management/vagrant-linode-environments
.. _use the salt-bootstrap script: https://github.com/saltstack/salt-bootstrap
.. _vagrantfile: https://www.vagrantup.com/docs/vagrantfile/
.. _env: https://ruby-doc.org/core-2.2.0/ENV.html
.. _see github: https://github.com/averagehuman/linode-saltmaster
.. _jenkins: https://jenkins.io/
