#!/bin/bash
{
  echo -e "192.168.1.112	v-fec81867df.vps.cloudhybrid.io" >> /etc/hosts
} || {
  echo "Target Server does not have ownership of file /etc/hosts"
}