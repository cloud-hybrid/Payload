#!/bin/bash
virt-install \
--nographics \
--noautoconsole \
--name Windows-Test \
--ram 512 \
--disk path=/var/lib/libvirt/images/Windows-Test.qcow2,size=50 \
--location "/var/lib/libvirt/images/Bionic-Server.iso" \
--initrd-inject=/var/lib/libvirt/images/preseed.cfg \
--vcpus 1 \
--os-type linux \
--os-variant ubuntu18.04 \
--autostart \
--extra-args="console=ttyS0, 115200n8 serial"