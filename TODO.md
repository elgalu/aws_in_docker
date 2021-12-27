# Links

## Zalando Repo, Certs, Lustre-Client

https://github.bus.zalan.do/linus/salt/blob/master/salt/common/config/zalando-ca_conf.sls#L20
https://github.bus.zalan.do/linus/salt/blob/24ddca6796f3710f73570a5275e8bdd3bc106a53/salt/repositories/Ubuntu/repo-zalando.sls#L6
https://github.bus.zalan.do/linus/salt/blob/master/salt/packages/lustre-client/map.jinja#L4
https://github.bus.zalan.do/linus/salt/blob/master/salt/packages/lustre-client/installed.sls#L5

## Slurm plugins

https://github.com/aws/aws-parallelcluster-node/blob/develop/src/slurm_plugin/logging/parallelcluster_resume_logging.conf#L21
https://github.com/aws/aws-parallelcluster-node/blob/develop/src/slurm_plugin/clustermgtd.py#L870
https://github.com/aws/aws-parallelcluster-node/blob/develop/src/common/schedulers/slurm_commands.py#L88
https://github.com/aws-samples/aws-plugin-for-slurm/blob/plugin-v2/suspend.py#L33
https://github.com/aws/aws-parallelcluster-node/blob/develop/src/slurm_plugin/common.py#L303
https://github.com/aws/aws-parallelcluster-node/blob/develop/src/slurm_plugin/resume.py#L96
https://github.com/elgalu/aws-plugin-for-slurm
https://github.com/elgalu/aws-plugin-for-slurm/blob/plugin-v2/resume.py#L94
https://github.com/elgalu/aws-plugin-for-slurm/blob/plugin-v2/common.py#L76
https://github.com/elgalu/aws-plugin-for-slurm/blob/plugin-v2/generate_conf.py#L9
https://github.com/elgalu/aws-plugin-for-slurm/blob/plugin-v2/change_state.py#L47
https://github.com/elgalu/aws-plugin-for-slurm/blob/plugin-v2/template.yaml#L272

# TODO

Integrate code quality tools like https://lgtm.com/

mock_ec2 => wrap_ec2
eu-west => eu-central
unicode_literals => delete
moto.compat => remove

from moto.compat import OrderedDict
=> from collections import OrderedDict
