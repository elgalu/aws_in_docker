from docker import from_env as create_docker_client_from_environment
from docker.client import DockerClient
from boto3 import client as boto3_client

from aws_in_docker import wrap_ec2


def spin_up_ec2_servers(ami_id, count):
    ec2_client = boto3_client('ec2', region_name='eu-central-1')
    return ec2_client.run_instances(ImageId=ami_id, MinCount=count, MaxCount=count)


def terminate_ec2_servers(instance_ids):
    ec2_client = boto3_client('ec2', region_name='eu-central-1')
    resp = ec2_client.terminate_instances(InstanceIds=instance_ids)
    return resp


@wrap_ec2
def test_spin_up_and_terminate_ec2_servers() -> None:
    spin_up_ec2_servers('ami-1234abcd', 2)

    client = boto3_client('ec2', region_name='eu-central-1')
    instances = client.describe_instances()['Reservations'][0]['Instances']
    assert len(instances) == 2
    instance1 = instances[0]
    assert instance1['ImageId'] == 'ami-1234abcd'

    resp = terminate_ec2_servers(instances)
    self.assertEqual(instances[0], resp['TerminatingInstances'][0]['InstanceId'])



# def test_docker() -> None:
#     client: DockerClient = create_docker_client_from_environment()
#     # client = create_docker_client_from_environment()
#     print(client.images.list())
#     assert client


# def test_readme() -> None:
#     with open("README.md", encoding="UTF-8") as f:
#         readme_contents = f.read()
#     assert "Usage" in readme_contents
