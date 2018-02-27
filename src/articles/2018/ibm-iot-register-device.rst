
IBM Watson IoT Device Registration Script
#########################################

:date: 2018-02-27 10:00
:category: IoT
:author: averagehuman


.. container:: callout primary

    Register an IoT device with IBM Watson IoT service using bash and curl.

MQTT as a service
-----------------

`MQTT`_ is a lightweight publish/subscribe mechanism suitable for resource-constrained
devices and hence for ``Internet of Things`` applications.

`IBM Watson IoT`_ (like the similar `AWS IoT`_ service) is essentially:

* an MQTT Broker
* an associated API
* an administrative dashboard.

There are some complexities at the setup and configuration level but,
once up and running, the basic idea comes down to publishing and subscribing to
topic queues.

A Device/Thing may send messages to a queue in order to report its state
or its surroundings, while at the same time receiving messages
that allow it to update its state or its surroundings.
This mechanism then enables all sorts of scenarios, in particular, applications
related to the monitoring and control of remote devices.

Device Registration
-------------------

The following is a bash script that automates the process of registering Devices
and Device Types with the ``IBM IoT Service`` via curl calls to the service api. It requires
that you know your organisation id and that you have generated an api key and secret
via the IoT Dashboard.

The script is called like:

.. code-block:: bash

    $ ibm-iot-register-device <orgId> <deviceType> <deviceDescription>

or:

.. code-block:: bash

    $ ibm-iot-register-device <orgId> <deviceType> <deviceDescription> <deviceId>


If you omit the deviceId, an identifier specific to the local machine is used.

The api key and secret should be stored beforehand at:

.. code-block:: bash

    /etc/watson/<orgId>/.credentials
    
and if successful the script will write a device-specific config file at:

.. code-block:: bash

    /etc/watson/<orgId>/devices/<deviceType>/<deviceId>.cfg

The config file will be an ini-style file in the form expected by the python
client library `ibmiotf`_.

Security
++++++++

The config file created by the script will contain an authentication token and in fact
this is all that is required to initiate MQTT requests for this device, ie. you no
longer need the admin api credentials after initial device registration.

You can also set things up so that connections from the device are ``TLSv1.2``-enabled
with a custom server certificate in addition to or in place of the authentication token.

`ibm-iot-register-device`_
--------------------------

[[ gist averagehuman:c66e95ff01f9b8a3473970649c228c2c ]]


.. _mqtt: http://mqtt.org/
.. _ibm watson iot: https://www.ibm.com/internet-of-things
.. _aws iot: https://aws.amazon.com/iot/
.. _ibm-iot-register-device: https://gist.github.com/averagehuman/c66e95ff01f9b8a3473970649c228c2c
.. _ibmiotf: https://github.com/ibm-watson-iot/iot-python


