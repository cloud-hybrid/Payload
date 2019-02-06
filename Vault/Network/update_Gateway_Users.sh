#!/bin/bash
sudo useradd -m -d /home/bionic -s /bin/bash bionic
sudo mkdir -p /home/bionic/.ssh
sudo touch /home/bionic/.ssh/authorized_keys

sudo chown snow -R /home/bionic
sudo chmod 777 -R /home/bionic/.ssh

ssh-keygen -b 4096 -t rsa -C "" -f /home/bionic/.ssh/id_rsa -q -N ""

scp /home/bionic/.ssh/id_rsa snow@192.168.0.5:~/.ssh/id_rsa_vps

public_key=$(cat /home/bionic/.ssh/id_rsa.pub)

echo 'command="ssh bionic@v-adb35e192d.vps.cloudhybrid.io"' $public_key >> /home/bionic/.ssh/authorized_keys

sudo chmod -R 700 /home/bionic/.ssh
sudo chmod 644 /home/bionic/.ssh/authorized_keys
sudo chmod 644 /home/bionic/.ssh/id_rsa.pub
sudo chmod 600 /home/bionic/.ssh/id_rsa
sudo chown bionic:bionic -R /home/bionic



