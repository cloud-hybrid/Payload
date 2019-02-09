#!/bin/bash
sudo useradd -m -d /home/windows -s /bin/bash windows
sudo mkdir -p /home/windows/.ssh
sudo touch /home/windows/.ssh/authorized_keys

sudo chown snow -R /home/windows
sudo chmod 777 -R /home/windows/.ssh

ssh-keygen -b 4096 -t rsa -C "" -f /home/windows/.ssh/id_rsa -q -N ""

scp /home/windows/.ssh/id_rsa snow@192.168.0.5:~/.ssh/id_rsa_vps

public_key=$(cat /home/windows/.ssh/id_rsa.pub)

echo 'command="ssh windows@v-fec81867df.vps.cloudhybrid.io"' $public_key >> /home/windows/.ssh/authorized_keys

sudo chmod -R 700 /home/windows/.ssh
sudo chmod 644 /home/windows/.ssh/authorized_keys
sudo chmod 644 /home/windows/.ssh/id_rsa.pub
sudo chmod 600 /home/windows/.ssh/id_rsa
sudo chown windows:windows -R /home/windows