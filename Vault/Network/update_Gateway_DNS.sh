#!/bin/bash
{
  echo -e "192.168.1.111	v-adb35e192d.vps.cloudhybrid.io" >> /etc/hosts
} || {
  echo "Target Server does not have ownership of file /etc/hosts"
}