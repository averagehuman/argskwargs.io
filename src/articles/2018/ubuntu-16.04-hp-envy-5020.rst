
Ubuntu - HP Envy 5020 Printer Setup
###################################

:date: 2018-02-13 10:00
:category: Ubuntu
:author: averagehuman


.. container:: callout primary

    Notes on setting up a home printer on Ubuntu 16.04.


The ``HP Envy 5020`` is a basic wireless home printer that can be set up to work
with Ubuntu via `hplip (HP Linux Imaging and Printing)`_.

``hplip`` can be installed via apt:

.. code-block:: bash
    
    $ apt-get install hplip

This is the preferred way to install (and, in hindsight, I may have been better going
this route - see below), but sometimes prebuilt packages can lag behind the latest releases, so
another option is to download the most recent source and build directly.

In addition, there is an interactive installer which `walks you through each step`_.


Run the installer:

.. code-block:: bash

    $ sh hplip-3.17.11.run


Ubuntu 16.04 Dependency Fix
---------------------------

However, I did run into a dependency mismatch with the ``hplip-3.17.11`` installer on
``Ubuntu Xenial`` which caused the process to fail at the **apt-get** stage.

The problem seems to be with packages ``libcupsimage2-dev`` and ``licupsfiltersdev``
which depend on another package ``libcupsfilters1`` at a specific version (1.8.3-2ubuntu3.1),
but something else in the dependency chain has already installed a later version of
that package.

.. code-block:: bash

     $ sudo apt-get -s install libcupsfilters-dev
       Reading package lists... Done
       Building dependency tree       
       Reading state information... Done
       Some packages could not be installed. This may mean that you have
       requested an impossible situation or if you are using the unstable
       distribution that some required packages have not yet been created
       or been moved out of Incoming.
       The following information may help to resolve the situation:

       The following packages have unmet dependencies.
        libcupsfilters-dev : Depends: libcupsfilters1 (= 1.8.3-2ubuntu3.1) but 1.8.3-2ubuntu3.3 is to be installed
       E: Unable to correct problems, you have held broken packages.

As a workaround, you can just downgrade ``libcupsfilters1`` and re-run the installer:

.. code-block:: bash

    $ sudo apt-get -y --allow-downgrades install libcupsfilters1=1.8.3-2ubuntu3.1
    $ sh hplip-3.17.11.run


/usr/bin/hp-setup
-----------------

Once ``hplip`` is installed, you then need to set up individual printers by running
``/usr/bin/hp-setup`` which brings up a GUI configuration tool. In the case of the
wireless HP Envy 5020, it was a simple matter of adding the IP address of the printer
and everything was good to go.

   
.. _hplip (HP Linux Imaging and Printing): https://developers.hp.com/hp-linux-imaging-and-printing/about
.. _walks you through each step: https://developers.hp.com/hp-linux-imaging-and-printing/install/install/index

