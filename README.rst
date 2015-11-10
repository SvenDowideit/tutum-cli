tutum
=====

CLI for Tutum. Full documentation available at `https://docs.tutum.co/v2/api/?shell# <https://docs.tutum.co/v2/api/?shell#>`_


Installing the CLI
------------------

In order to install the Tutum CLI, you can use ``pip install``:

.. sourcecode:: bash

    pip install tutum

For Mac OS users, you can use ``brew install``:

.. sourcecode:: bash

    brew install tutum

Now you can start using it:

.. sourcecode:: none

    $ tutum
    
    usage: tutum [-h] [-v]
        {build,container,event,exec,image,login,node,nodecluster,push,run,service,stack,tag,volume,volumegroup,trigger,up}
        ...

    Tutum's CLI
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
    
    Tutum's CLI commands:
      {build,container,event,exec,image,login,node,nodecluster,push,run,service,stack,tag,volume,volumegroup,trigger,up}
        build               Build an image using tutum/builder
        container           Container-related operations
        event               Get real time tutum events
        exec                Run a command in a running container
        image               Image-related operations
        login               Login into Tutum
        node                Node-related operations
        nodecluster         NodeCluster-related operations
        push                Push a local image to Tutum private registry
        run                 Create and run a new service
        service             Service-related operations
        stack               Stack-related operations
        tag                 Tag-related operations
        volume              Volume-related operations
        volumegroup         VolumeGroup-related operations
        trigger             Trigger-related operations
        up                  Create and deploy a stack



Docker image
^^^^^^^^^^^^

You can also install the CLI via Docker:

.. sourcecode:: bash

    docker run tutum/cli -h

You will have to pass your username and API key as environment variables, as the credentials stored via ``tutum login``
will not persist by default:

.. sourcecode:: bash

    docker run -it -e TUTUM_USER=username -e TUTUM_APIKEY=apikey tutum/cli

To make things easier, you might want to use an ``alias`` for it:

.. sourcecode:: bash

    alias tutum="docker run -it -v /usr/bin/docker:/usr/bin/docker -v /var/run/docker.sock:/var/run/docker.sock -e TUTUM_USER=username -e TUTUM_APIKEY=apikey --rm tutum/cli"

Then, you can run commands like:

.. sourcecode:: bash

    tutum service
    tutum exec


Authentication
--------------

In order to manage your apps and containers running on Tutum, you need to log into Tutum in any of the following ways
(will be used in this order):

* Login using Tutum CLI or storing it directly in a configuration file in ``~/.tutum``:

.. sourcecode:: bash

    $ tutum login
    Username: admin
    Password:
    Login succeeded!

Your login credentials will be stored in ``~/.tutum``:

.. sourcecode:: ini

    [auth]
    user = "username"
    apikey = "apikey"

* Set the environment variables ``TUTUM_USER`` and ``TUTUM_APIKEY``:

.. sourcecode:: bash

    export TUTUM_USER=username
    export TUTUM_APIKEY=apikey

* Set the environment variables ``TUTUM_AUTH``:

.. sourcecode:: bash
    export TUTUM_AUTH=tutumauth

``TUTUM_AUTH`` is the environment variable injected via API roles 

Note: ``tutum-cli`` and ``python-tutum`` will pick up the auth in the following order:
    * ``TUTUM_AUTH``
    * ``TUTUM_USER`` and ``TUTUM_APIKEY``
    * ``~/.tutum``
