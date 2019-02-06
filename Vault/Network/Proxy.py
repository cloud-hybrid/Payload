"""
@Infrastructure
  ↳   SSH-Keys    - SSH keys must be set from the         - Required  : (RSA-Key)
                  | - host --> client.
                  | - For testing purposes, add SSH
                  | - keys to and from localhost.
@Parameters
  ↳   Server      - The IP address or verified hostname   - Required  : (Command-Line)
                  | - of the target server hosting the
                  | - VPS. Defaults to localhost.
@Documentation
  [Note]    - When packaging the program, {script} may not work correct. The path relative
            - to its execution potentially could be the problem.
  [To-Do]   - Update @Parameters
"""

import os
import sys
import time
import textwrap

from Payload.Vault.Shell.Terminal import Terminal

class Proxy(object):
  def __init__(self, user, address):
    self.user = user
    self.IP = address

  def update_Proxy(self, VPS):
    script = "update_Proxy.sh"

    location = os.path.dirname(os.path.normpath(__file__)) + "\\" + script
    double_slash = "\\" + "\\"
    location = location.replace("\\", double_slash)

    script = open(location, "w+")

    if VPS.SSL == True:
      script.write(self.proxy_script_ssl(VPS))
    else:
      script.write(self.proxy_script(VPS))

    script.close()

    command = textwrap.dedent(
    f"""
    ssh {self.user}@{self.IP} "bash -s" -- < {script}
    """.strip()
    )

    time.sleep(1)

    Terminal(command).display()

  @staticmethod
  def proxy_script(VPS):
    open = "{"
    close = "}"

    script = textwrap.dedent(
    f"""
    #!/bin/bash

    HOST='\$host'
    URI='\$request_uri'

    sudo bash -c "cat << EOF > /etc/nginx/sites-enabled/{VPS.hostname}.conf
    server {open}
      listen 80;
      server_name {VPS.hostname};
      location / {open}
        proxy_pass http://{VPS.IP}:80;
        include proxy.conf;
      {close}
    {close}

    server {open}
      listen 443;
      server_name {VPS.hostname};
      location / {open}
        proxy_pass http://{VPS.IP}:443;
        include proxy.conf;
      {close}
    {close}
    EOF"

    sudo nginx -s reload
    """
    ).strip()

    return script

  @staticmethod
  def proxy_script_ssl(VPS):
    open = "{"
    close = "}"

    script = textwrap.dedent(
    f"""
    #!/bin/bash

    HOST='\$host'
    URI='\$request_uri'

    sudo bash -c "cat << EOF > /etc/nginx/sites-enabled/{VPS.hostname}.conf
    server {open}
      listen 80;
      server_name {VPS.hostname};
      location / {open}
        proxy_pass http://{VPS.IP}:80;
        include proxy.conf;
      {close}
    {close}
    EOF"

    sudo nginx -s reload

    sudo certbot certonly --nginx -d {VPS.hostname}

    sudo bash -c "cat << EOF > /etc/nginx/sites-enabled/{VPS.hostname}.conf
    server {open}
      listen 443;
      server_name {VPS.hostname};
      ssl_certificate /etc/letsencrypt/live/{VPS.hostname}/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/{VPS.hostname}/privkey.pem;
      include /etc/letsencrypt/options-ssl-nginx.conf;
      ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

      location / {open}
        proxy_pass http://{VPS.IP}:80;
        include proxy.conf;
      {close}
    {close}

    server {open}
      listen 80;
      server_name {VPS.hostname};
      return 301 https://$HOST$URI;
    {close}
    EOF"

    sudo nginx -s reload
    """
    ).strip()

    return script