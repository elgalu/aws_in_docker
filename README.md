# aws_in_docker

[![Python](docs/img/badges/language.svg)](https://devdocs.io/python/)

Mock EC2 with moto + launch instances in Docker.

## Usage

Let's say your code spins up EC2 instances:

```py
import boto3

def spin_up_ec2_servers(ami_id, count):
    ec2_client = boto3.client('ec2', region_name='eu-central-1')
    return ec2_client.run_instances(ImageId=ami_id, MinCount=count, MaxCount=count)

def terminate_ec2_servers(instance_ids):
    ec2_client = boto3.client('ec2', region_name='eu-central-1')
    resp = ec2_client.terminate_instances(InstanceIds=instance_ids)
    return resp
```

Now we want to wrap AWS and spin-up Docker containers instead of EC2 real instances:

```py
from . import spin_up_ec2_servers
from aws_in_docker import mock_ec2 # wrap_ec2

@mock_ec2
def test_spin_up_and_terminate_ec2_servers():
    spin_up_ec2_servers('ami-1234abcd', 2)

    client = boto3.client('ec2', region_name='eu-central-1')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    assert len(instances) == 2
    instance1 = instances[0]
    assert instance1['ImageId'] == 'ami-1234abcd'

    resp = terminate_ec2_servers(instances)
    self.assertEqual(instances[0], resp['TerminatingInstances'][0]['InstanceId'])
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
