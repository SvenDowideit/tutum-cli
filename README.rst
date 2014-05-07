tutum
=====

CLI for Tutum. Full documentation available at `http://docs.tutum.co/reference/cli/ <http://docs.tutum.co/reference/cli/>`_


Installing the CLI
------------------

In order to install the Tutum CLI, you can use ``pip install``:

.. sourcecode:: bash

    pip install tutum

Now you can start using it:

.. sourcecode:: none

    $ tutum
    
    usage: tutum [-h] [-v] {apps,build,containers,images,login} ...
    
    Tutum's CLI
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
    
    Tutum's CLI commands:
      {apps,build,containers,images,login}
        apps                Applications related operations
        build               Build an image
        containers          Containers related operations
        images              Image related operations
        login               Login into Tutum


Docker image
^^^^^^^^^^^^

You can also install the CLI via Docker:

.. sourcecode:: bash

    docker run tutum/cli -h

You will have to pass your username and API key as environment variables, as the credentials stored via ``tutum login``
will not persist by default:

.. sourcecode:: bash

    docker run -e TUTUM_USER=username -e TUTUM_APIKEY=apikey tutum/cli apps

To make things easier, you might want to use an ``alias`` for it:

.. sourcecode:: bash

    alias tutum="docker run -e TUTUM_USER=username -e TUTUM_APIKEY=apikey tutum/cli"
    tutum apps


Authentication
--------------

In other to manage your apps and containers running on Tutum, you need to log into Tutum in any of the following ways
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


Quick examples
--------------

Applications
^^^^^^^^^^^^

.. sourcecode:: none

    $ tutum apps
    usage: tutum [-h] [-v] {app,build,container,image,login} ...

    Tutum's CLI

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit

    Tutum's CLI commands:
      {app,build,container,image,login}
        app                 Application-related operations
        build               Build an image using an existing Dockerfile, or create
                            one using buildstep
        container           Container-related operations
        image               Image-related operations
        login               Login into Tutum

    $ tutum app run tutum/redis -t 3
    5f07bce6-d285-43bc-b917-9f0fa8e1110d
    $ tutum app ps
    NAME     UUID      STATUS      IMAGE                 SIZE (#)    DEPLOYED          WEB HOSTNAME
    couchdb  da0dcfcc  ▶ Running   tutum/couchdb:latest  XS (2)      27 minutes ago
    redis    5f07bce6  ⚙ Starting  tutum/redis:latest    XS (3)
    $ tutum app ps
    NAME     UUID      STATUS     IMAGE                 SIZE (#)    DEPLOYED          WEB HOSTNAME
    couchdb  da0dcfcc  ▶ Running  tutum/couchdb:latest  XS (2)      28 minutes ago


Containers
^^^^^^^^^^

.. sourcecode:: none

    $ tutum container
    usage: tutum container [-h] {inspect,logs,ps,start,stop,terminate} ...

    Container-related operations

    optional arguments:
      -h, --help            show this help message and exit

    tutum container commands:
      {inspect,logs,ps,start,stop,terminate}
        inspect             Inspect a container
        logs                Get logs from a container
        ps                  List containers
        start               Start a container
        stop                Stop a container
        terminate           Terminate a container

    $ tutum container ps
    NAME       UUID      STATUS     IMAGE                 RUN COMMAND    SIZE      EXIT CODE  DEPLOYED        PORTS
    couchdb-2  15d412f7  ▶ Running  tutum/couchdb:latest  /run.sh        XS                   31 minutes ago  couchdb-2-admin.atlas-dev.tutum.io:49229->5984/tcp
    couchdb-3  adc068ae  ▶ Running  tutum/couchdb:latest  /run.sh        XS                   31 minutes ago  couchdb-3-admin.atlas-dev.tutum.io:49227->5984/tcp
    redis-1    20afdd70  ◼ Stopped  tutum/redis:latest    /run.sh        XS                0  3 minutes ago   redis-1-admin.atlas-dev.tutum.io:49231->6379/tcp
    redis-2    f8f75117  ◼ Stopped  tutum/redis:latest    /run.sh        XS                0  3 minutes ago   redis-2-admin.atlas-dev.tutum.io:49230->6379/tcp
    redis-3    7423cf8e  ◼ Stopped  tutum/redis:latest    /run.sh        XS                0  3 minutes ago   redis-3-admin.atlas-dev.tutum.io:49232->6379/tcp
    $ tutum container logs redis-1
    => Securing redis with a random password
    => Done!
    ========================================================================
    You can now connect to this Redis server using:
    
        redis-cli -a R8GBf2KVUU1myIlU7OQEgOetI7XTGGNQ -h <host> -p <port>
    
    Please remember to change the above password as soon as possible!
    ========================================================================
    [1] 03 May 00:47:02.069 # You requested maxclients of 10000 requiring at least 10032 max file descriptors.
    [1] 03 May 00:47:02.069 # Redis can't set maximum open files to 10032 because of OS error: Operation not permitted.
    [1] 03 May 00:47:02.069 # Current maximum open files is 1024. maxclients has been reduced to 4064 to compensate for low ulimit. If you need higher maxclients increase 'ulimit -n'.
                    _._                                                  
               _.-``__ ''-._                                             
          _.-``    `.  `_.  ''-._           Redis 2.8.8 (00000000/0) 64 bit
      .-`` .-```.  ```\/    _.,_ ''-._                                   
     (    '      ,       .-`  | `,    )     Running in stand alone mode
     |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
     |    `-._   `._    /     _.-'    |     PID: 1
      `-._    `-._  `-./  _.-'    _.-'                                   
     |`-._`-._    `-.__.-'    _.-'_.-'|                                  
     |    `-._`-._        _.-'_.-'    |           http://redis.io        
      `-._    `-._`-.__.-'_.-'    _.-'                                   
     |`-._`-._    `-.__.-'    _.-'_.-'|                                  
     |    `-._`-._        _.-'_.-'    |                                  
      `-._    `-._`-.__.-'_.-'    _.-'                                   
          `-._    `-.__.-'    _.-'                                       
              `-._        _.-'                                           
                  `-.__.-'                                               
    
    [1] 03 May 00:47:02.070 # Server started, Redis version 2.8.8
    [1] 03 May 00:47:02.070 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
    [1] 03 May 00:47:02.070 * The server is now ready to accept connections on port 6379
    [1 | signal handler] (1399078062) Received SIGTERM, scheduling shutdown...
    [1] 03 May 00:47:42.789 # User requested shutdown...
    [1] 03 May 00:47:42.789 # Redis is now ready to exit, bye bye...


Images
^^^^^^

.. sourcecode:: none

    $ tutum image
    usage: tutum images [-h] {list,register,push,rm,search,update} ...
    
    Image related operations
    
    optional arguments:
      -h, --help            show this help message and exit
    
    tutum images commands:
      {list,register,push,rm,search,update}
        list                List private images
        register            Register an image from a private repository to Tutum
        push                Push an image or a repository to Tutum registry
        rm                  Remove a private image
        search              Search for images in the Docker Index
        update              Update a private image
    $ tutum image list
    NAME                                       DESCRIPTION
    quay.io/tifayuki/redis
    quay.io/tifayuki/couchdb
    $ tutum image search tutum
    NAME                       DESCRIPTION                                                                               STARS  OFFICIAL    TRUSTED
    tutum/mysql                MySQL Server image - listens in port 3306. For the admin account password, eithe [...]       14              ✓
    tutum/wordpress            Wordpress Docker image - listens in port 80.                                                  8              ✓
    tutum/buildstep            Convert your application into a self-sufficient image using Heroku's buildpacks. [...]        8              ✓
    tutum/rabbitmq             RabbitMQ Docker image – listens in ports 5672/55672 (admin). For the admin passw [...]        7              ✓
    tutum/lamp                 LAMP image - Apache listens in port 80, and MySQL in port 3306. For the MySQL ad [...]        6              ✓
    tutum/redis                Redis Docker image image – listens in port 6379. For the server password, either [...]        5              ✓
    tutum/centos               DEPRECATED. Use tutum/centos-6.4 instead. CentOS Docker image with SSH access                 5
    tutum/postgresql           PostgreSQL Docker Image – listens on port 5432. For the admin (postgres) passwor [...]        4              ✓
    tutum/mongodb              MongoDB Docker image – listens in port 27017. For the admin password, either set [...]        4              ✓
    tutum/ubuntu               DEPRECATED. Use tutum/ubuntu-saucy instead. Ubuntu Docker image with SSH access               3
    tutum/hello-world          Image to test docker deployments. Has Apache with a 'Hello World' page listening [...]        3              ✓
    tutum/cli                  CLI tool for Tutum                                                                            3              ✓
    siedrix/tutum-docker-node  This is a basic docker image for node.\n\n                                                    2
    tutum/haproxy-http         HAProxy image that load balances between any linked container that listens in po [...]        2              ✓
    tutum/memcached            Memcached Docker image image – listens in port 11211. For the admin password, ei [...]        2              ✓
    tutum/ubuntu-quantal       Ubuntu Quantal image with SSH access. For the root password, either set the ROOT [...]        2              ✓
    tutum/apache-php           Apache+PHP base image - listens in port 80.                                                   2              ✓
    tutum/ubuntu-precise       Ubuntu Precise image with SSH access. For the root password, either set the ROOT [...]        2              ✓
    tutum/centos-6.4           Centos 6.4 image with SSH access. For the root password, either set the ROOT_PAS [...]        2              ✓
    borja/unixbench            Base Docker image for UnixBench – http://tutum.co                                             2              ✓
    tutum/couchdb              CouchDB image - listens in port 5984. For the admin account password, either set [...]        1              ✓
    tutum/ubuntu-saucy         Ubuntu Saucy image with SSH access. For the root password, either set the ROOT_P [...]        1              ✓
    tutum/debian-wheezy        Debian Wheezy image with SSH access. For the root password, either set the ROOT_ [...]        1              ✓
    tutum/fedora-20            Fedora 20 image with SSH access. For the root password, either set the ROOT_PASS [...]        1              ✓
    tutum/ubuntu-lucid         Ubuntu Lucid image with SSH access. For the root password, either set the ROOT_P [...]        1              ✓
    tutum/debian-squeeze       Debian Squeeze image with SSH access. For the root password, either set the ROOT [...]        1              ✓
    tutum/ubuntu-raring        Ubuntu Raring image with SSH access. For the root password, either set the ROOT_ [...]        1              ✓
    tutum/mariadb              MariaDB image - listens in port 3306. For the admin account password, either set [...]        1              ✓
    tutum/wordpress-stackable                                                                                                0              ✓
    tutum/registry-mirror                                                                                                    0              ✓
    ichaboddee/mytutumapache                                                                                                 0
    ichaboddee/mytutumcentos                                                                                                 0
    tutum/ubuntu-trusty        Ubuntu Trusty image with SSH access. For the root password, either set the ROOT_ [...]        0              ✓
    
