#!/bin/bash

XML=${1}
XML_Location=${2}
VM=${3}
VM_Location=${4}

virsh dumpxml $XML > $XML_Location

cp /var/lib/libvirt/images/$VM.qcow2 $VM_Location

echo "Successful"