"""
## AWS in Docker Python Package.

Mocks EC2 API calls with moto responses and launches instances in Docker for local testing.

```py
from aws_in_docker import wrap_ec2

@wrap_ec2
def ...
```

:copyright: (c) 2021 by Leo Gallucci.
:license: Apache 2.0, see LICENSE for more details.
"""
# Do not change the version here but rather `tbump "0.0.5" --only-patch`
__version__ = "0.0.2"

# `__all__` is left here for documentation purposes and as a
# reference to which interfaces are meant to be imported.
__all__ = [
    "__version__",
]

from docker import from_env as create_docker_client_from_environment
from docker.client import DockerClient

# from aws_in_docker.ec2 import wrap_ec2


class FakeEC2UbuntuInstance:
    def __init__(
        self,
        ami_id: str,
        aws_region: str = 'eu-central-1b',
        docker_image_name: str = 'elgalu/ubuntu-focal-20.04-amd64-server',
        docker_image_tag: str = '20210610',
        ec2_client: DockerClient = create_docker_client_from_environment(),
    ) -> None:
        super().__init__()
        self.ami_id = ami_id
        self.aws_region = aws_region
        self.docker_image_name = docker_image_name
        self.docker_image_tag = docker_image_tag
        self.__ec2_client = ec2_client

    def __del__(self):
        # TODO: cleanup docker stuff here
        ...
        super().__del__()

    def __len__(self):
        return ...

    def __repr__(self):
        return f"{self.ami_id} {self.aws_region}"


def wrap_ec2() -> None:
    ...


# Monkey-patch botocore requests back to underlying urllib3 classes
# https://github.com/spulec/moto/blob/38455c8e1943/moto/__init__.py
from botocore.awsrequest import (
    HTTPSConnectionPool,
    HTTPConnectionPool,
    HTTPConnection,
    VerifiedHTTPSConnection
)
HTTPSConnectionPool.ConnectionCls = VerifiedHTTPSConnection
HTTPConnectionPool.ConnectionCls = HTTPConnection
