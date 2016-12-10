
Deploy Jenkins with Docker and Ansible
######################################

:date: 2016-07-11 08:00
:category: Ops
:author: averagehuman
:tags: Ansible


.. container:: callout primary

    `Ansible`_ roles for deploying a Jenkins instance on Debian within a Docker container
    behind nginx.
    

Install Docker
--------------

Use ansible's `apt module`_ to install the `Docker`_ engine as a system service:

.. code-block:: bash

    - name: Add Docker Group
      group: name=docker state=present

    - name: Add Docker Signing Key
      apt_key:
        keyserver: 'hkp://p80.pool.sks-keyservers.net:80'
        id: 58118E89F3A912897C070ADBF76221572C52609D
        state: present

    - name: Add Docker Repo
      apt_repository:
        repo: 'deb https://apt.dockerproject.org/repo debian-jessie main'
        filename: 'docker.list'

    - name: Install Docker
      apt: name=docker-engine state=present

    - name: Install docker-py
      pip: name=docker-py version=1.9.0


Install Jenkins
---------------

The official Jenkins container image will install application files to **/var/jenkins_home** within
the container, and this directory needs to be available outside the container, so use the
Docker **-v** option to map the volume to, say, **/share/volumes/jenkins** on the host:


.. code-block:: bash

    - name: Ensure jenkins directory on docker host
      file:
        state: directory
        owner: 1000
        group: 1000
        path: /share/jenkins

    - name: Pull the latest official jenkins docker image
      docker_image:
        name: "jenkins:latest"

    - name: Create a container from the jenkins docker image
      docker_container:
        name: "jenkins-server"
        image: "jenkins"
        ports:
            - "8080:8080"
            - "50000:50000"
        volumes:
            - "/share/jenkins:/var/jenkins_home"
        state: present
        recreate: no

Create Service
--------------

Now create a service script to allow starting and stopping of the container:

.. code-block:: bash

    [Unit]
    Description=Jenkins in a Docker container
    Requires=docker.service
    After=docker.service

    [Service]
    Restart=always
    ExecStart=/usr/bin/docker start -a jenkins-server
    ExecStop=/usr/bin/docker stop -t 2 jenkins-server

    [Install]
    WantedBy=default.target

Copy this to the appropriate place and enable the service:

.. code-block:: bash

    - name: Copy systemd service script to start and stop the jenkins container
      copy: src=files/jenkins.service dest=/etc/systemd/system

    - name: Reload systemctl
      shell: systemctl reload-or-restart docker-jenkins

    - name: Enable the docker-jenkins service
      shell: systemctl enable docker-jenkins

See `the next post`_ for configuring nginx to act as a reverse proxy for the container.

.. _ansible: https://www.ansible.com/
.. _docker: https://www.docker.com/
.. _apt module: http://docs.ansible.com/ansible/apt_module.html
.. _on github: https://github.com/averagehuman/linode-saltmaster
.. _the next post: {filename}jenkins-nginx-reverse-proxy.rst
