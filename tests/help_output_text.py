TUTUM = '''usage: tutum [-h] [-v]
             {build,container,cluster,image,login,node,nodecluster} ...

Tutum's CLI

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Tutum's CLI commands:
  {build,container,cluster,image,login,node,nodecluster}
    build               Build an image using an existing Dockerfile, or create
                        one using buildstep
    container           Container-related operations
    cluster             Cluster-related operations
    image               Image-related operations
    login               Login into Tutum
    node                Node-related operations
    nodecluster         NodeCluster-related operations'''

# ##################################################

TUTUM_BUILD = '''usage: tutum build [-h] [-q] [--no-cache] [-t TAG] directory

Build an image using an existing Dockerfile, or create one using buildstep

positional arguments:
  directory          working directory

optional arguments:
  -h, --help         show this help message and exit
  -q, --quiet        print minimum information
  --no-cache         do not use the cache when building the image
  -t TAG, --tag TAG  repository name (and optionally a tag) to be applied to
                     the resulting image in case of success'''

# ##################################################

TUTUM_CONTAINER = '''usage: tutum container [-h]
                       {inspect,logs,ps,redeploy,run,start,stop,terminate} ...

Container-related operations

optional arguments:
  -h, --help            show this help message and exit

tutum container commands:
  {inspect,logs,ps,redeploy,run,start,stop,terminate}
    inspect             Inspect a container
    logs                Get logs from a container
    ps                  List containers
    redeploy            Redeploy a running container with a new version/tag
    run                 Create and run a new container
    start               Start a container
    stop                Stop a container
    terminate           Terminate a container'''

# ##################################################

TUTUM_CONTAINER_INSPECT = '''usage: tutum container inspect [-h] identifier [identifier ...]

Inspect a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CONTAINER_LOGS = '''usage: tutum container logs [-h] identifier [identifier ...]

Get logs from a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CONTAINER_PS = '''usage: tutum container ps [-h] [-i IDENTIFIER] [-q]
                          [-s {Running,Stopped,Start failed,Stopped with errors}]

List containers

optional arguments:
  -h, --help            show this help message and exit
  -i IDENTIFIER, --identifier IDENTIFIER
                        container's UUID (either long or short) or name
  -q, --quiet           print only long UUIDs
  -s {Running,Stopped,Start failed,Stopped with errors}, --status {Running,Stopped,Start failed,Stopped with errors}
                        filter containers by status'''

# ##################################################

TUTUM_CONTAINER_REDEPLOY = '''usage: tutum container redeploy [-h] [-t TAG] identifier [identifier ...]

Redeploy a running container with a new version/tag

positional arguments:
  identifier         container's UUID (either long or short) or name

optional arguments:
  -h, --help         show this help message and exit
  -t TAG, --tag TAG  tag of the image to redeploy'''

# ##################################################

TUTUM_CONTAINER_RUN = '''usage: tutum container run [-h] [-n NAME] [--cpushares CPUSHARES]
                           [--memory MEMORY] [--memoryswap MEMORYSWAP]
                           [-t TARGET_NUM_CONTAINERS] [-r RUN_COMMAND]
                           [--entrypoint ENTRYPOINT] [-p PORT] [-e ENV]
                           [--link-cluster LINK_CLUSTER]
                           [--link-container LINK_CONTAINER]
                           [--autorestart {OFF,ON_FAILURE,ALWAYS}]
                           [--autoreplace {OFF,ON_FAILURE,ALWAYS}]
                           [--autodestroy {OFF,ON_FAILURE,ALWAYS}]
                           [--role ROLE] [--sequential]
                           [--web-public-dns WEB_PUBLIC_DNS]
                           image

Create and run a new container

positional arguments:
  image                 the name of the image used to deploy this container

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  a human-readable name for the container(default:
                        image_tag without namespace)
  --cpushares CPUSHARES
                        Relative weight for CPU Shares
  --memory MEMORY       RAM memory hard limit in MB
  --memoryswap MEMORYSWAP
                        Memory swap hard limit in MB
  -t TARGET_NUM_CONTAINERS, --target-num-containers TARGET_NUM_CONTAINERS
                        the number of containers to run for this container
                        (default: 1)
  -r RUN_COMMAND, --run-command RUN_COMMAND
                        the command used to start the container containers
                        (default: as defined in the image)
  --entrypoint ENTRYPOINT
                        the command prefix used to start the container
                        containers (default: as defined in the image)
  -p PORT, --port PORT  set ports i.e. "80/tcp" (default: as defined in the
                        image)
  -e ENV, --env ENV     set environment variables i.e. "ENVVAR=foo" (default:
                        as defined in the image, plus any link- or role-
                        generated variables)
  --link-cluster LINK_CLUSTER
                        Add link to another cluster (name:alias) or
                        (uuid:alias)
  --link-container LINK_CONTAINER
                        Add link to another container (name:alias) or
                        (uuid:alias)
  --autorestart {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be restarted if they
                        stop (default: OFF)
  --autoreplace {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be replaced with a new
                        one if they stop (default: OFF)
  --autodestroy {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be terminated if they
                        stop (default: OFF)
  --role ROLE           Tutum API roles to grant the container, i.e. "global"
                        (default: none, possible values: "global")
  --sequential          whether the containers should be launched and scaled
                        sequentially
  --web-public-dns WEB_PUBLIC_DNS
                        Set your own web public dns'''

# ##################################################

TUTUM_CONTAINER_START = '''usage: tutum container start [-h] identifier [identifier ...]

Start a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CONTAINER_STOP = '''usage: tutum container stop [-h] identifier [identifier ...]

Stop a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CONTAINER_TERMINATE = '''usage: tutum container terminate [-h] identifier [identifier ...]

Terminate a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CLUSTER = '''usage: tutum cluster [-h]

                     {alias,inspect,logs,open,ps,redeploy,run,scale,set,start,stop,terminate}
                     ...

Cluster-related operations

optional arguments:
  -h, --help            show this help message and exit

tutum cluster commands:
  {alias,inspect,logs,open,ps,redeploy,run,scale,set,start,stop,terminate}
    alias               Set a custom FQDN (CNAME) to a running web cluster
    inspect             Get all details from an cluster
    logs                Get logs from an cluster
    open                Open last web cluster launched
    ps                  List clusters
    redeploy            Redeploy a running cluster with a new version/tag
    run                 Create and run a new cluster
    scale               Scale a running cluster
    set                 Enable or disable Crash Recovery and Autodestroy
                        features to an existing cluster
    start               Start a stopped cluster
    stop                Stop a running cluster
    terminate           Terminate an cluster'''

# ##################################################

TUTUM_CLUSTER_ALIAS = '''usage: tutum cluster alias [-h] identifier [identifier ...] dns

Set a custom DNS record (CNAME) to a running web cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name
  dns         custom FQDN to use for this web cluster

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CLUSTER_INSPECT = '''usage: tutum cluster inspect [-h] identifier [identifier ...]

Get all details from an cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CLUSTER_LOGS = '''usage: tutum cluster logs [-h] identifier [identifier ...]

Get logs from an cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CLUSTER_OPEN = '''usage: tutum cluster open [-h]

Open last web cluster launched

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CLUSTER_PS = '''usage: tutum cluster ps [-h] [-q]
                        [-s {Running,Partly running,Stopped,Start failed,Stopped with errors}]

List clusters

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           print only long UUIDs
  -s {Running,Partly running,Stopped,Start failed,Stopped with errors}, --status {Running,Partly running,Stopped,Start failed,Stopped with errors}
                        filter clusters by status'''

# ##################################################

TUTUM_CLUSTER_REDEPLOY = '''usage: tutum cluster redeploy [-h] [-t TAG] identifier [identifier ...]

Redeploy a running cluster with a new version/tag

positional arguments:
  identifier         cluster's UUID (either long or short) or name

optional arguments:
  -h, --help         show this help message and exit
  -t TAG, --tag TAG  tag of the image to redeploy'''

# ##################################################

TUTUM_CLUSTER_RUN = '''usage: tutum cluster run [-h] [-n NAME] [--cpushares CPUSHARES]
                         [--memory MEMORY] [--memoryswap MEMORYSWAP]
                         [-t TARGET_NUM_CONTAINERS] [-r RUN_COMMAND]
                         [--entrypoint ENTRYPOINT] [-p PORT] [-e ENV]
                         [--link-cluster LINK_CLUSTER]
                         [--link-container LINK_CONTAINER]
                         [--autorestart {OFF,ON_FAILURE,ALWAYS}]
                         [--autoreplace {OFF,ON_FAILURE,ALWAYS}]
                         [--autodestroy {OFF,ON_FAILURE,ALWAYS}] [--role ROLE]
                         [--sequential] [--web-public-dns WEB_PUBLIC_DNS]
                         image

Create and run a new cluster

positional arguments:
  image                 the name of the image used to deploy this cluster

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  a human-readable name for the cluster (default:
                        image_tag without namespace)
  --cpushares CPUSHARES
                        Relative weight for CPU Shares
  --memory MEMORY       RAM memory hard limit in MB
  --memoryswap MEMORYSWAP
                        Memory swap hard limit in MB
  -t TARGET_NUM_CONTAINERS, --target-num-containers TARGET_NUM_CONTAINERS
                        the number of containers to run for this cluster
                        (default: 1)
  -r RUN_COMMAND, --run-command RUN_COMMAND
                        the command used to start the cluster containers
                        (default: as defined in the image)
  --entrypoint ENTRYPOINT
                        the command prefix used to start the cluster
                        containers (default: as defined in the image)
  -p PORT, --port PORT  set ports i.e. "80/tcp" (default: as defined in the
                        image)
  -e ENV, --env ENV     set environment variables i.e. "ENVVAR=foo" (default:
                        as defined in the image, plus any link- or role-
                        generated variables)
  --link-cluster LINK_CLUSTER
                        Add link to another cluster (name:alias) or
                        (uuid:alias)
  --link-container LINK_CONTAINER
                        Add link to another container (name:alias) or
                        (uuid:alias)
  --autorestart {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be restarted if they
                        stop (default: OFF)
  --autoreplace {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be replaced with a new
                        one if they stop (default: OFF)
  --autodestroy {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be terminated if they
                        stop (default: OFF)
  --role ROLE           Tutum API roles to grant the cluster, i.e. "global"
                        (default: none, possible values: "global")
  --sequential          whether the containers should be launched and scaled
                        sequentially
  --web-public-dns WEB_PUBLIC_DNS
                        Set your own web public dns'''

# ##################################################

TUTUM_CLUSTER_SCALE = '''usage: tutum cluster scale [-h]
                           identifier [identifier ...] target-num-containers

Scale a running cluster

positional arguments:
  identifier            cluster's UUID (either long or short) or name
  target-num-containers
                        target number of containers to scale this cluster to

optional arguments:
  -h, --help            show this help message and exit'''

# ##################################################

TUTUM_CLUSTER_SET = '''usage: tutum cluster set [-h] [--autorestart {OFF,ON_FAILURE,ALWAYS}]
                         [--autoreplace {OFF,ON_FAILURE,ALWAYS}]
                         [--autodestroy {OFF,ON_FAILURE,ALWAYS}]
                         identifier [identifier ...]

Enable or disable Crash Recovery and Autodestroy features to an existing
cluster

positional arguments:
  identifier            cluster's UUID (either long or short) or name

optional arguments:
  -h, --help            show this help message and exit
  --autorestart {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be restarted if they
                        stop (default: OFF)
  --autoreplace {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be replaced with a new
                        one if they stop (default: OFF)
  --autodestroy {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be terminated if they
                        stop (default: OFF)'''

# ##################################################

TUTUM_CLUSTER_START = '''usage: tutum cluster start [-h] identifier [identifier ...]

Start a stopped cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CLUSTER_STOP = '''usage: tutum cluster stop [-h] identifier [identifier ...]

Stop a running cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_CLUSTER_TERMINATE = '''usage: tutum cluster terminate [-h] identifier [identifier ...]

Terminate an cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_IMAGE = '''usage: tutum image [-h] {list,register,push,rm,search,update} ...

Image-related operations

optional arguments:
  -h, --help            show this help message and exit

tutum image commands:
  {list,register,push,rm,search,update}
    list                List private images
    register            Register an image from a private repository in Tutum
    push                Push a local image to Tutum private registry
    rm                  Deregister a private image from Tutum
    search              Search for images in the Docker Index
    update              Update a private image'''

# ##################################################

TUTUM_IMAGE_LIST = '''usage: tutum image list [-h] [-q] [-j | -l]

List private images

optional arguments:
  -h, --help        show this help message and exit
  -q, --quiet       print only image names
  -j, --jumpstarts  list jumpstart images
  -l, --linux       list linux images'''

# ##################################################

TUTUM_IMAGE_REGISTER = '''usage: tutum image register [-h] [-d DESCRIPTION] image_name

Register an image from a private repository in Tutum

positional arguments:
  image_name            full image name, i.e. quay.io/tutum/test-repo

optional arguments:
  -h, --help            show this help message and exit
  -d DESCRIPTION, --description DESCRIPTION
                        Image description'''

# ##################################################

TUTUM_IMAGE_PUSH = '''usage: tutum image push [-h] [--public] name

Push a local image to Tutum private registry

positional arguments:
  name        name of the image to push

optional arguments:
  -h, --help  show this help message and exit
  --public    push image to public registry'''

# ##################################################

TUTUM_IMAGE_RM = '''usage: tutum image rm [-h] image_name [image_name ...]

Deregister a private image from Tutum

positional arguments:
  image_name  full image name, i.e. quay.io/tutum/test-repo

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_IMAGE_SEARCH = '''usage: tutum image search [-h] query

Search for images in the Docker Index

positional arguments:
  query       query to search

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_IMAGE_UPDATE = '''usage: tutum image update [-h] [-u USERNAME] [-p PASSWORD] [-d DESCRIPTION]
                          image_name [image_name ...]

Update a private image

positional arguments:
  image_name            full image name, i.e. quay.io/tutum/test-repo

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        new username to authenticate with the registry
  -p PASSWORD, --password PASSWORD
                        new password to authenticate with the registry
  -d DESCRIPTION, --description DESCRIPTION
                        new image description'''

# ##################################################

TUTUM_LOGIN = '''usage: tutum login [-h]

Login into Tutum

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_NODE = '''usage: tutum node [-h] {inspect,list,rm} ...

Node-related operations

optional arguments:
  -h, --help         show this help message and exit

tutum node commands:
  {inspect,list,rm}
    inspect          Inspect a node
    list             List nodes
    rm               Remove a node'''

# ##################################################

TUTUM_NODE_INSPECT = '''usage: tutum node inspect [-h] identifier [identifier ...]

Inspect a node

positional arguments:
  identifier  node's UUID (either long or short)

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_NODE_LIST = '''usage: tutum node list [-h] [-q]

List nodes

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  print only node uuid'''

# ##################################################

TUTUM_NODE_RM = '''usage: tutum node rm [-h] identifier [identifier ...]

Remove a container

positional arguments:
  identifier  node's UUID (either long or short)

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_NODECLUSTER = '''usage: tutum nodecluster [-h]

                         {create,inspect,list,rm,scale,provider,region,nodetype}
                         ...

NodeCluster-related operations

optional arguments:
  -h, --help            show this help message and exit

tutum node commands:
  {create,inspect,list,rm,scale,provider,region,nodetype}
    create              Create a nodecluster
    inspect             Inspect a nodecluster
    list                List node clusters
    rm                  Remove node clusters
    scale               Scale a running node cluster
    provider            Show all available infrastructure providers
    region              Show all available regions of a given provider
    nodetype            Show all available types of a given region'''

# ##################################################

TUTUM_NODECLUSTER_CREATE = '''usage: tutum nodecluster create [-h] [-t TARGET_NUM_NODES]
                                name provider_id region_id nodetype_id

Create a nodecluster

positional arguments:
  name                  name of the cluster to create
  provider_id           id of the provider
  region_id             id of the region
  nodetype_id           id of the nodetype

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET_NUM_NODES, --target-num-nodes TARGET_NUM_NODES
                        the target number of nodes to run for this cluster
                        (default: 1)'''

# ##################################################

TUTUM_NODECLUSTER_INSPECT = '''usage: tutum nodecluster inspect [-h] identifier [identifier ...]

Inspect a nodecluster

positional arguments:
  identifier  node's UUID (either long or short)

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_NODECLUSTER_LIST = '''usage: tutum nodecluster list [-h] [-q]

List node clusters

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  print only node uuid'''

# ##################################################

TUTUM_NODECLUSTER_RM = '''usage: tutum nodecluster rm [-h] identifier [identifier ...]

Remove node clusters

positional arguments:
  identifier  node's UUID (either long or short)

optional arguments:
  -h, --help  show this help message and exit'''

# ##################################################

TUTUM_NODECLUSTER_SCALE = '''usage: tutum nodecluster scale [-h]
                               identifier [identifier ...] target-num-nodes

Scale a running node cluster

positional arguments:
  identifier        node cluster's UUID (either long or short) or name
  target-num-nodes  target number of nodes to scale this node cluster to

optional arguments:
  -h, --help        show this help message and exit'''

# ##################################################

TUTUM_NODECLUSTER_PROVIDER = '''usage: tutum nodecluster provider [-h] [-q]

Show all available infrastructure providers

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  print only provider name'''

# ##################################################

TUTUM_NODECLUSTER_REGION = '''usage: tutum nodecluster region [-h] provider_id

positional arguments:
  provider_id  id of the provider (to find out id, use `tutum nodecluster
               provider`)

optional arguments:
  -h, --help   show this help message and exit'''

# ##################################################

TUTUM_NODECLUSTER_NODETYPE = '''usage: tutum nodecluster nodetype [-h] region_id

positional arguments:
  region_id   id of the region (to find out id use `tutum nodecluster region`)

optional arguments:
  -h, --help  show this help message and exit'''