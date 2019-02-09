#!/bin/bash
virt-install \
--nographics \
--noautoconsole \
--name v-feed659283.vps.cloudhybrid.io \
--ram 512 \
--disk path=/var/lib/libvirt/images/v-feed659283.vps.cloudhybrid.io.qcow2,size=50 \
--location "/var/lib/libvirt/images/Bionic-Server.iso" \
--initrd-inject=/var/lib/libvirt/images/preseed.cfg \
--vcpus 1 \
--os-type linux \
--os-variant ubuntu18.04 \
--autostart \
--extra-args="console=ttyS0, 115200n8 serial"