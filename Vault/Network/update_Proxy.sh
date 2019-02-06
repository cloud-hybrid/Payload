#!/bin/bash

HOST='\$host'
URI='\$request_uri'

sudo bash -c "cat << EOF > /etc/nginx/sites-enabled/v-adb35e192d.vps.cloudhybrid.io.conf
server {
  listen 80;
  server_name v-adb35e192d.vps.cloudhybrid.io;
  location / {
    proxy_pass http://192.168.1.111:80;
    include proxy.conf;
  }
}

server {
  listen 443;
  server_name v-adb35e192d.vps.cloudhybrid.io;
  location / {
    proxy_pass http://192.168.1.111:443;
    include proxy.conf;
  }
}
EOF"

sudo nginx -s reload