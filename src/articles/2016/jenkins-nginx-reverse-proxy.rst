
Nginx as Jenkins Reverse Proxy
##############################

:date: 2016-08-07 18:00
:category: Ops
:author: averagehuman
:tags: Ansible


So the last post was about setting up `jenkins`_ to run in a docker container
as a debian system service, and the steps outlined there should get you to the
point of having a new Jenkins instance running on port 8080. The next step then
is to set up nginx as a reverse proxy for the Jenkins server - ie. requests are
directed to nginx on port 80 before being passed on to Jenkins.

.. container:: callout primary

        A Proxy Server makes requests on behalf of a particular client or group of
        clients, whereas a Reverse Proxy sends responses on behalf of a particular
        server or group of servers.

This is a common setup with Django, for example, where nginx sits in front of a
number of gunicorn or uwsgi or apache/mod_wsgi servers and reduces load and
complexity on those servers by:

+ serving static files directly
+ dealing with slow clients
+ handling ssl termination


Symlink the asset directories
-----------------------------

The jenkins setup in the previous post has the jenkins root directory as virtual folder
``/var/jenkins_home`` in the docker container and this is mapped to physical folder
``/share/volumes/jenkins`` on the host. The asset folders then are ``/share/volumes/jenkins/war/images``
for image files, ``/share/volumes/jenkins/war/css`` for stylesheets and so on. You could
just expose the ``war`` directory as the server root, but there are other non-asset files
there as well which there is no need to expose, eg. java class files.  So better to create,
say, ``/var/www/jenkins`` as the server root and symlink the static files and folders as
required:

.. code-block:: bash

        - name: Ensure jenkins server root directory /var/www/jenkins
          file: path=/var/www/jenkins state=directory

        - name: Link jenkins images folder to /var/www/jenkins
          file: src=/share/volumes/jenkins/war/images dest=/var/www/jenkins/images state=link force=yes

        - name: Link jenkins css folder to /var/www/jenkins
          file: src=/share/volumes/jenkins/war/css dest=/var/www/jenkins/css state=link force=yes

        - name: Link jenkins scripts folder to /var/www/jenkins
          file: src=/share/volumes/jenkins/war/scripts dest=/var/www/jenkins/scripts state=link force=yes

        - name: Link jenkins jsbundles folder to /var/www/jenkins
          file: src=/share/volumes/jenkins/war/jsbundles dest=/var/www/jenkins/jsbundles state=link force=yes

        - name: Link jenkins help folder to /var/www/jenkins
          file: src=/share/volumes/jenkins/war/help dest=/var/www/jenkins/help state=link force=yes

        - name: Link jenkins favicon to /var/www/jenkins
          file: src=/share/volumes/jenkins/war/favicon.ico dest=/var/www/jenkins/favicon.ico state=link

        - name: Link jenkins robots.txt to /var/www/jenkins
          file: src=/share/volumes/jenkins/war/robots.txt dest=/var/www/jenkins/robots.txt state=link


nginx config
------------

Next install nginx:

.. code-block:: bash

        - name: Install nginx
          apt: name=nginx

Remove the default server config:

.. code-block:: bash

        - name: Remove default nginx site (unlink from /etc/nginx/sites-enabled)
          file: path=/etc/nginx/sites-enabled/default state=absent

And add the jenkins proxy config:

.. code-block:: bash

        server {
          listen          80;

          server_name     _;

          root            /var/www/jenkins/;

          access_log      /var/log/nginx/jenkins/access.log;
          error_log       /var/log/nginx/jenkins/error.log;

          location ~ "^/static/[0-9a-fA-F]{8}\/(.*)$" {

                #rewrite all static files into requests to the site root
                #E.g /static/12345678/css/something.css will become /css/something.css
                rewrite "^/static/[0-9a-fA-F]{8}\/(.*)" /$1 last;
          }


          location @jenkins {
              sendfile off;
              proxy_pass         http://127.0.0.1:8080;
              proxy_redirect     default;

              proxy_set_header   Host             $host;
              proxy_set_header   X-Real-IP        $remote_addr;
              proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
              proxy_max_temp_file_size 0;

              #this is the maximum upload size
              client_max_body_size       10m;
              client_body_buffer_size    128k;

              proxy_connect_timeout      90;
              proxy_send_timeout         90;
              proxy_read_timeout         90;

              proxy_buffer_size          4k;
              proxy_buffers              4 32k;
              proxy_busy_buffers_size    64k;
              proxy_temp_file_write_size 64k;
        }

        location / {

            try_files $uri @jenkins;
        }
      }


.. _jenkins: https://jenkins.io/
.. _ansible: https://www.ansible.com/
.. _apt module: http://docs.ansible.com/ansible/apt_module.html
.. _on github: https://github.com/averagehuman/linode-saltmaster

