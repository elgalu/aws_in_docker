# aws_in_docker

[![](docs/img/badges/language.svg)](https://devdocs.io/python/)

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

### Contributing Setup

Simply run `contributing/contributor_setup.sh` then `source .venv/bin/activate`

If `contributor_setup.sh` didn't work on your system you can do the setup manually, step by step:

1. Clone the project locally
1. Install the corresponding [.python-version](./.python-version) using something like [pyenv](https://github.com/pyenv/pyenv)
1. Create a virtual environment named `.venv` with `python -m venv .venv`
1. Activate the virtual environment with `source .venv/bin/activate`
1. Install [poetry](https://poetry.eustace.io/docs/#installation)
1. Run `poetry install --no-root`
1. Install [invoke](https://www.pyinvoke.org/installing.html) with `pip install invoke`
1. Run `invoke setup`

### Feature branches

This project uses [towncrier](https://github.com/twisted/towncrier) for CHANGELOG automation. Start all your feature/bugs/x work with:

```sh
towncrier create ?
#=> Created news fragment at .changelog.d/initial_setup.add now edit this file
towncrier build --draft  # test first
towncrier build          # final
```

### Contributing Tests

Run `poetry run invoke tests`

### Contributing All Checks (including tests)

Run `poetry run invoke hooks`

### Build And Publish to PyPI

```sh
poetry build
poetry publish
```
