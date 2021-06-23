# Based on https://github.com/spulec/moto/blob/cf3cf8b1346b4e/moto/ec2/__init__.py
from aws_in_docker.ec2.models import ec2_backends
from aws_in_docker.core.models import base_decorator

ec2_backend = ec2_backends["eu-central-1"]
wrap_ec2 = base_decorator(ec2_backends)
