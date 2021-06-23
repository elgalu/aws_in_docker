# Based on https://github.com/spulec/moto/blob/cf3cf8b1346b4e/moto/ec2/models.py
from collections import OrderedDict
from dataclasses import dataclass


@dataclass
class InstanceBackend:
    """This is an InstanceBackend wip.

    The class is for bla bla.

    Attributes:
        reservations (OrderedDict[str, Reservation]): List of reservations.
    """
    reservations: OrderedDict[str, int] # Reservation

    def __init__(self) -> None:
        #: Doc comment for instance attribute qux.
        self.reservations = OrderedDict()
        """Docstring for instance attribute spam."""
        super(InstanceBackend, self).__init__()
        print(self.reservations)

    def get_instance(self, instance_id):
        for instance in self.all_instances():
            if instance.id == instance_id:
                return instance
        raise InvalidInstanceIdError(instance_id)

    def add_instances(self, image_id, count, user_data, security_group_names, **kwargs):
        new_reservation = Reservation()
        new_reservation.id = random_reservation_id()

        security_groups = [
            self.get_security_group_from_name(name) for name in security_group_names
        ]
        security_groups.extend(
            self.get_security_group_from_id(sg_id)
            for sg_id in kwargs.pop("security_group_ids", [])
        )
        self.reservations[new_reservation.id] = new_reservation

        tags = kwargs.pop("tags", {})
        instance_tags = tags.get("instance", {})
        volume_tags = tags.get("volume", {})

        for index in range(count):
            kwargs["ami_launch_index"] = index
            new_instance = Instance(
                self, image_id, user_data, security_groups, **kwargs
            )
            new_reservation.instances.append(new_instance)
            new_instance.add_tags(instance_tags)
            if "block_device_mappings" in kwargs:
                for block_device in kwargs["block_device_mappings"]:
                    device_name = block_device["DeviceName"]
                    volume_size = block_device["Ebs"].get("VolumeSize")
                    snapshot_id = block_device["Ebs"].get("SnapshotId")
                    encrypted = block_device["Ebs"].get("Encrypted", False)
                    delete_on_termination = block_device["Ebs"].get(
                        "DeleteOnTermination", False
                    )
                    kms_key_id = block_device["Ebs"].get("KmsKeyId")
                    new_instance.add_block_device(
                        volume_size,
                        device_name,
                        snapshot_id,
                        encrypted,
                        delete_on_termination,
                        kms_key_id,
                    )
            else:
                new_instance.setup_defaults()
            # Tag all created volumes.
            for _, device in new_instance.get_block_device_mapping:
                volumes = self.describe_volumes(volume_ids=[device.volume_id])
                for volume in volumes:
                    volume.add_tags(volume_tags)

        return new_reservation

    def run_instances(self):
        # Logic resides in add_instances
        # Fake method here to make implementation coverage script aware that this method is implemented
        pass

    def start_instances(self, instance_ids):
        started_instances = []
        for instance in self.get_multi_instances_by_id(instance_ids):
            instance.start()
            started_instances.append(instance)

        return started_instances

    def stop_instances(self, instance_ids):
        stopped_instances = []
        for instance in self.get_multi_instances_by_id(instance_ids):
            instance.stop()
            stopped_instances.append(instance)

        return stopped_instances

    def terminate_instances(self, instance_ids):
        terminated_instances = []
        if not instance_ids:
            raise EC2ClientError(
                "InvalidParameterCombination", "No instances specified"
            )
        for instance in self.get_multi_instances_by_id(instance_ids):
            instance.terminate()
            terminated_instances.append(instance)

        return terminated_instances

    def reboot_instances(self, instance_ids):
        rebooted_instances = []
        for instance in self.get_multi_instances_by_id(instance_ids):
            instance.reboot()
            rebooted_instances.append(instance)

        return rebooted_instances

    def modify_instance_attribute(self, instance_id, key, value):
        instance = self.get_instance(instance_id)
        setattr(instance, key, value)
        return instance

    def modify_instance_security_groups(self, instance_id, new_group_id_list):
        instance = self.get_instance(instance_id)
        new_group_list = []
        for new_group_id in new_group_id_list:
            new_group_list.append(self.get_security_group_from_id(new_group_id))
        setattr(instance, "security_groups", new_group_list)
        return instance

    def describe_instance_attribute(self, instance_id, attribute):
        if attribute not in Instance.VALID_ATTRIBUTES:
            raise InvalidParameterValueErrorUnknownAttribute(attribute)

        if attribute == "groupSet":
            key = "security_groups"
        else:
            key = camelcase_to_underscores(attribute)
        instance = self.get_instance(instance_id)
        value = getattr(instance, key)
        return instance, value

    def describe_instance_credit_specifications(self, instance_ids):
        queried_instances = []
        for instance in self.get_multi_instances_by_id(instance_ids):
            queried_instances.append(instance)
        return queried_instances

    def all_instances(self, filters=None):
        instances = []
        for reservation in self.all_reservations():
            for instance in reservation.instances:
                if instance.applies(filters):
                    instances.append(instance)
        return instances

    def all_running_instances(self, filters=None):
        instances = []
        for reservation in self.all_reservations():
            for instance in reservation.instances:
                if instance.state_code == 16 and instance.applies(filters):
                    instances.append(instance)
        return instances

    def get_multi_instances_by_id(self, instance_ids, filters=None):
        """
        :param instance_ids: A string list with instance ids
        :return: A list with instance objects
        """
        result = []

        for reservation in self.all_reservations():
            for instance in reservation.instances:
                if instance.id in instance_ids:
                    if instance.applies(filters):
                        result.append(instance)

        # TODO: Trim error message down to specific invalid id.
        if instance_ids and len(instance_ids) > len(result):
            raise InvalidInstanceIdError(instance_ids)

        return result

    def get_instance_by_id(self, instance_id):
        for reservation in self.all_reservations():
            for instance in reservation.instances:
                if instance.id == instance_id:
                    return instance

    def get_reservations_by_instance_ids(self, instance_ids, filters=None):
        """Go through all of the reservations and filter to only return those
        associated with the given instance_ids.
        """
        reservations = []
        for reservation in self.all_reservations():
            reservation_instance_ids = [
                instance.id for instance in reservation.instances
            ]
            matching_reservation = any(
                instance_id in reservation_instance_ids for instance_id in instance_ids
            )
            if matching_reservation:
                reservation.instances = [
                    instance
                    for instance in reservation.instances
                    if instance.id in instance_ids
                ]
                reservations.append(reservation)
        found_instance_ids = [
            instance.id
            for reservation in reservations
            for instance in reservation.instances
        ]
        if len(found_instance_ids) != len(instance_ids):
            invalid_id = list(set(instance_ids).difference(set(found_instance_ids)))[0]
            raise InvalidInstanceIdError(invalid_id)
        if filters is not None:
            reservations = filter_reservations(reservations, filters)
        return reservations

    def all_reservations(self, filters=None):
        reservations = [
            copy.copy(reservation) for reservation in self.reservations.values()
        ]
        if filters is not None:
            reservations = filter_reservations(reservations, filters)
        return reservations

class RegionsAndZonesBackend(object):
    regions_opt_in_not_required = [
        "eu-central-1",
    ]

    regions = []
    for region in Session().get_available_regions("ec2"):
        if region in regions_opt_in_not_required:
            regions.append(
                Region(
                    region, "ec2.{}.amazonaws.com".format(region), "opt-in-not-required"
                )
            )
        else:
            regions.append(
                Region(region, "ec2.{}.amazonaws.com".format(region), "not-opted-in")
            )

    zones = {
        "eu-central-1": [
            Zone(region_name="eu-central-1", name="eu-central-1a", zone_id="euc1-az2"),
            Zone(region_name="eu-central-1", name="eu-central-1b", zone_id="euc1-az3"),
            Zone(region_name="eu-central-1", name="eu-central-1c", zone_id="euc1-az1"),
        ],
    }

    def describe_regions(self, region_names=[]):
        if len(region_names) == 0:
            return self.regions
        ret = []
        for name in region_names:
            for region in self.regions:
                if region.name == name:
                    ret.append(region)
        return ret

    def describe_availability_zones(self):
        return self.zones[self.region_name]

    def get_zone_by_name(self, name):
        for zone in self.zones[self.region_name]:
            if zone.name == name:
                return zone


class EC2Backend(
    InstanceBackend,
):
    def __init__(self, region_name):
        self.region_name = region_name
        super(EC2Backend, self).__init__()

        # Default VPC exists by default, which is the current behavior
        # of EC2-VPC. See for detail:
        #
        #   docs.aws.amazon.com/AmazonVPC/latest/UserGuide/default-vpc.html
        #
        if not self.vpcs:
            vpc = self.create_vpc("172.31.0.0/16")
        else:
            # For now this is included for potential
            # backward-compatibility issues
            vpc = self.vpcs.values()[0]

        # Create default subnet for each availability zone
        ip, _ = vpc.cidr_block.split("/")
        ip = ip.split(".")
        ip[2] = 0

        for zone in self.describe_availability_zones():
            az_name = zone.name
            cidr_block = ".".join(str(i) for i in ip) + "/20"
            self.create_subnet(vpc.id, cidr_block, availability_zone=az_name)
            ip[2] += 16

    def reset(self):
        region_name = self.region_name
        self.__dict__ = {}
        self.__init__(region_name)

    # Use this to generate a proper error template response when in a response
    # handler.
    def raise_error(self, code, message):
        raise EC2ClientError(code, message)

    def raise_not_implemented_error(self, blurb):
        raise MotoNotImplementedError(blurb)

    def do_resources_exist(self, resource_ids):
        for resource_id in resource_ids:
            resource_prefix = get_prefix(resource_id)
            if resource_prefix == EC2_RESOURCE_TO_PREFIX["customer-gateway"]:
                self.get_customer_gateway(customer_gateway_id=resource_id)
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["dhcp-options"]:
                self.describe_dhcp_options(options_ids=[resource_id])
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["image"]:
                self.describe_images(ami_ids=[resource_id])
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["instance"]:
                self.get_instance_by_id(instance_id=resource_id)
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["internet-gateway"]:
                self.describe_internet_gateways(internet_gateway_ids=[resource_id])
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["launch-template"]:
                self.get_launch_template(resource_id)
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["network-acl"]:
                self.get_all_network_acls()
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["network-interface"]:
                self.describe_network_interfaces(
                    filters={"network-interface-id": resource_id}
                )
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["reserved-instance"]:
                self.raise_not_implemented_error("DescribeReservedInstances")
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["route-table"]:
                self.get_route_table(route_table_id=resource_id)
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["security-group"]:
                self.describe_security_groups(group_ids=[resource_id])
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["snapshot"]:
                self.get_snapshot(snapshot_id=resource_id)
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["spot-instance-request"]:
                self.describe_spot_instance_requests(
                    filters={"spot-instance-request-id": resource_id}
                )
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["subnet"]:
                self.get_subnet(subnet_id=resource_id)
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["volume"]:
                self.get_volume(volume_id=resource_id)
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["vpc"]:
                self.get_vpc(vpc_id=resource_id)
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["vpc-peering-connection"]:
                self.get_vpc_peering_connection(vpc_pcx_id=resource_id)
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["vpn-connection"]:
                self.describe_vpn_connections(vpn_connection_ids=[resource_id])
            elif resource_prefix == EC2_RESOURCE_TO_PREFIX["vpn-gateway"]:
                self.get_vpn_gateway(vpn_gateway_id=resource_id)
            elif (
                resource_prefix
                == EC2_RESOURCE_TO_PREFIX["iam-instance-profile-association"]
            ):
                self.describe_iam_instance_profile_associations(
                    association_ids=[resource_id]
                )
        return True

ec2_backends = {
    region.name: EC2Backend(region.name) for region in RegionsAndZonesBackend.regions
}
