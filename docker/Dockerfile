# docker build -t "elgalu/ubuntu-focal-20.04-amd64-server:patched" .
#
# docker run --rm --name=ami -ti \
#  --mount type=bind,source=/sys/fs/cgroup,target=/sys/fs/cgroup,readonly \
#  --mount type=bind,source=/sys/fs/fuse,target=/sys/fs/fuse,readonly \
#  --mount type=tmpfs,destination=/tmp \
#  --mount type=tmpfs,destination=/run \
#  --mount type=tmpfs,destination=/run/lock \
#  "elgalu/ubuntu-focal-20.04-amd64-server:patched"

# hadolint ignore=DL3007
FROM elgalu/ubuntu-focal-20.04-amd64-server:latest

ENV container=docker

RUN pwd \
 && systemctl disable systemd-networkd.socket  \
 && systemctl disable systemd-remount-fs.service \
 && systemctl disable systemd-networkd \
 && systemctl disable lvm2-lvmpolld.socket \
 && systemctl disable ssh.service \
 && rm -f /usr/lib/systemd/system/ssh.service.d/ec2-instance-connect.conf

ENTRYPOINT ["/usr/lib/systemd/systemd"]

CMD ["--log-level=info", "--unit=sysinit.target"]
