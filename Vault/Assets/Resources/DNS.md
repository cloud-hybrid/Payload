---
title: DNS
layout: post
---

# DNS Setup

## Documentation
- [PowerDNS Manual](https://doc.powerdns.com/authoritative/PowerDNS-Authoritative.pdf)

## Installation
1. Create two VPS servers. 
    - *Payload installations must be executed sequentially.*
```
python3 -m Payload --TBD
```
2. Repeat step 1.
```
python3 -m Payload --TBD
```
3. Start each VPS.
```
virsh start DNS-Master

virsh start DNS-Slave
```
4. SSH into each VPS as root.
```
ssh root@[DNS-Master/IP-Address]

ssh root@[DNS-Slave/IP-Address]
```
5. Update the systems.
```
apt update -y
apt upgrade -y
```
6. Install mySQL.
    - Note: As of 18.04, Ubuntu Server no longer uses password-based authentication against mySQL. Using the official PowerDNS manual, mySQL needs to use password-authentication rather than its Bionic default, socket-based authentication. To combat this, install the base package, *mysql-server*, and run its configuration script -- *mysql_secure_installation*. However, because we logged in as root, and therefore have access to the socket, we can automate the authentication change by executing *mysql -e "..."*.
```
apt install mysql-server -y

mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Knowledge';"
mysql -u root --password="Knowledge" -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -u root --password="Knowledge" -e "DELETE FROM mysql.user WHERE User='';"
mysql -u root --password="Knowledge" -e "DROP DATABASE test;"
mysql -u root --password="Knowledge" -e "FLUSH PRIVILEGES;"
```
7. (Optional) Check if password and installation was successful.
    - The **-u** flag proceeds the desired user.
    - The **-p** flag instructs the system to prompt for a password.
```
mysqladmin -u root -p version
```
  - Output should be similiar to:
```
Server version		5.7.24-0ubuntu0.18.04.1
Protocol version	10
Connection		Localhost via UNIX socket
UNIX socket		/var/run/mysqld/mysqld.sock
Uptime:			5 min 30 sec
```
8. (Optional) Check if authentication was set to *mysql_native_password*.
    - The authentication setting is found on in the **first row** under the **plugin column**. 
    - Changing from socket --> password authentication will change the way normal users enter the SQL client; non-root users will now have to run *mysql -u root -p*.
```
mysql -u root --password="Knowledge" -e "SELECT user,authentication_string,plugin,host FROM mysql.user;"
```
  - Example Output:
```
+------------------+-------------------------------------------+-----------------------+-----------+
| user             | authentication_string                     | plugin                | host      |
+------------------+-------------------------------------------+-----------------------+-----------+
| root             | *3946A9F1376691C1CE019436D8D404E6CCE6A622 | mysql_native_password | localhost |
| mysql.session    | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
| mysql.sys        | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE | mysql_native_password | localhost |
| debian-sys-maint | *CFD34C032E51602CB78F1F4B7F29B89624FC0123 | mysql_native_password | localhost |
+------------------+-------------------------------------------+-----------------------+-----------+
```

9. Update the systems.
```
apt update
```

10. Configure SQL for PowerDNS.
```
mysql -u root --password="Knowledge" -e "CREATE DATABASE pdns;"
mysql -u root --password="Knowledge" -e "GRANT ALL PRIVILEGES ON pdns.* TO 'pdns'@'localhost' IDENTIFIED BY 'PasswordDNS';"
mysql -u root --password="Knowledge" -e "FLUSH PRIVILEGES;"
```

11. Create the PowerDNS tables.
```
mysql -u root --password="Knowledge" -e "USE pdns;

CREATE TABLE domains (
  id                    INT AUTO_INCREMENT,
  name                  VARCHAR(255) NOT NULL,
  master                VARCHAR(128) DEFAULT NULL,
  last_check            INT DEFAULT NULL,
  type                  VARCHAR(6) NOT NULL,
  notified_serial       INT DEFAULT NULL,
  account               VARCHAR(40) DEFAULT NULL,
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE UNIQUE INDEX name_index ON domains(name);


CREATE TABLE records (
  id                    BIGINT AUTO_INCREMENT,
  domain_id             INT DEFAULT NULL,
  name                  VARCHAR(255) DEFAULT NULL,
  type                  VARCHAR(10) DEFAULT NULL,
  content               VARCHAR(64000) DEFAULT NULL,
  ttl                   INT DEFAULT NULL,
  prio                  INT DEFAULT NULL,
  change_date           INT DEFAULT NULL,
  disabled              TINYINT(1) DEFAULT 0,
  ordername             VARCHAR(255) BINARY DEFAULT NULL,
  auth                  TINYINT(1) DEFAULT 1,
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE INDEX nametype_index ON records(name,type);
CREATE INDEX domain_id ON records(domain_id);
CREATE INDEX recordorder ON records (domain_id, ordername);


CREATE TABLE supermasters (
  ip                    VARCHAR(64) NOT NULL,
  nameserver            VARCHAR(255) NOT NULL,
  account               VARCHAR(40) NOT NULL,
  PRIMARY KEY (ip, nameserver)
) Engine=InnoDB;


CREATE TABLE comments (
  id                    INT AUTO_INCREMENT,
  domain_id             INT NOT NULL,
  name                  VARCHAR(255) NOT NULL,
  type                  VARCHAR(10) NOT NULL,
  modified_at           INT NOT NULL,
  account               VARCHAR(40) NOT NULL,
  comment               VARCHAR(64000) NOT NULL,
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE INDEX comments_domain_id_idx ON comments (domain_id);
CREATE INDEX comments_name_type_idx ON comments (name, type);
CREATE INDEX comments_order_idx ON comments (domain_id, modified_at);


CREATE TABLE domainmetadata (
  id                    INT AUTO_INCREMENT,
  domain_id             INT NOT NULL,
  kind                  VARCHAR(32),
  content               TEXT,
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE INDEX domainmetadata_idx ON domainmetadata (domain_id, kind);


CREATE TABLE cryptokeys (
  id                    INT AUTO_INCREMENT,
  domain_id             INT NOT NULL,
  flags                 INT NOT NULL,
  active                BOOL,
  content               TEXT,
  PRIMARY KEY(id)
) Engine=InnoDB;

CREATE INDEX domainidindex ON cryptokeys(domain_id);


CREATE TABLE tsigkeys (
  id                    INT AUTO_INCREMENT,
  name                  VARCHAR(255),
  algorithm             VARCHAR(50),
  secret                VARCHAR(255),
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE UNIQUE INDEX namealgoindex ON tsigkeys(name, algorithm);"
```

12. (Optional) Check if tables were successfully created.
```
mysql -u root --password="Knowledge" -e "use pdns; show tables;"
```
  - Output:
```
+----------------+
| Tables_in_pdns |
+----------------+
| comments       |
| cryptokeys     |
| domainmetadata |
| domains        |
| records        |
| supermasters   |
| tsigkeys       |
+----------------+
```

13. Install recommended packages.
  - [PowerDNS Recommended Packages, gitHub](https://github.com/PowerDNS/pdns#compiling-authoritative-server)
```
apt install libcurl4-openssl-dev luajit lua-yaml-dev libyaml-cpp-dev libtolua-dev lua5.3 autoconf automake ragel bison flex g++ libboost-all-dev libtool make pkg-config libssl-dev virtualenv lua-yaml-dev libyaml-cpp-dev libluajit-5.1-dev libcurl4 gawk -y

apt install libsodium-dev -y

apt install default-libmysqlclient-dev -y

apt install libmaxminddb-dev libmaxminddb0 libgeoip1 libgeoip-dev -y
```

14. Update the systems.
```
apt update
```

15. Install PowerDNS's base package and backend. 
```
apt install pdns-server pdns-backend-mysql -y
```

16. Select *No*.
![Alt text](assets/DNS-Backend-Prompt.png?raw=true "PowerDNS Backend Prompt")

17. Configure PowerDNS Master. 
```
# --- Add Password to Backend .conf --- #
perl -p -i -e 's/gmysql-password=/gmysql-password=Knowledge/g' /etc/powerdns/pdns.d/pdns.local.gmysql.conf

# --- Create Backup of Default Configuration --- #
mv /etc/powerdns/pdns.conf /etc/powerdns/pdns.conf-orig

# --- Set Hostname --- #
hostnamectl set-hostname dns-master.vaultcipher.com

# --- Create the New Configuration --- #
cat > /etc/powerdns/pdns.conf << EOF
default-soa-name=dns-master.vaultcipher.com
include-dir=/etc/powerdns/pdns.d
launch=
security-poll-suffix=
setgid=pdns
setuid=pdns

api=yes
api-key=okc2rmeQCqHCMRirkXa6
EOF

```

18. Configure PowerDNS Slave. 
```
# --- Add Password to Backend .conf --- #
perl -p -i -e 's/gmysql-password=/gmysql-password=Knowledge/g' /etc/powerdns/pdns.d/pdns.local.gmysql.conf

# --- Create Backup of Default Configuration --- #
mv /etc/powerdns/pdns.conf /etc/powerdns/pdns.conf-orig

# --- Set Hostname --- #
hostnamectl set-hostname dns-slave.vaultcipher.com

# --- Create the New Configuration --- #
cat > /etc/powerdns/pdns.conf << EOF
default-soa-name=dns-slave.vaultcipher.com
include-dir=/etc/powerdns/pdns.d
launch=
security-poll-suffix=
setgid=pdns
setuid=pdns
EOF

```

19. Disable systemd-resolved.
```
systemctl stop systemd-resolved

systemctl disable systemd-resolved
```

20. Stop PowerDNS.
```
systemctl stop pdns
```

21. Start PowerDNS.
```
systemctl start pdns
```

22. Edit the master DNS SQL configuration file.
```
nano /etc/mysql/mysql.conf.d/mysqld.cnf

# --- Defaults --- #
bind-address            = 127.0.0.1

#server-id              = 1
#log_bin                        = /var/log/mysql/mysql-bin.log
#binlog_do_db           = include_database_name

# --- Changes --- #
bind-address = 0.0.0.0

server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
max_binlog_size = 100M
binlog_do_db = pdns
```

23. Restart MySQL.
```
systemctl restart mysql
```

24. Log into MySQL Client, on the Master, and create a user for the slave server(s).
    - IP address is the local IP of the Slave server. 
```
mysql -u root --password=Knowledge -e "GRANT REPLICATION SLAVE ON *.* TO 'pdnsslave'@'192.168.1.254' IDENTIFIED BY 'Knowledge';"

mysql -u root --password=Knowledge -e "FLUSH PRIVILEGES;"
```

25. Take note of the following values:
```
+------------------+----------+-----------------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB          | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+-----------------------+------------------+-------------------+
| mysql-bin.000001 |      606 | include_database_name |                  |                   |
+------------------+----------+-----------------------+------------------+-------------------+
```

26. Change Slave SQL Values.
    - /etc/mysql/mysql.conf.d/mysqld.cnf
```
# --- Change --- #
server-id=2

# --- Add --- #
relay-log=slave-relay-bin
relay-log-index=slave-relay-bin.index
replicate-do-db=pdns
```

27. Restart MySQL on Slave.
```
systemctl restart mysql
```

28. Configure Slave SQL client and take note of any errors.
    - Master_host is the Master's local IP address.
    - Master_user is the slave SQL user created on the master. 
    - Master_password is the password that was set for the slave user on the Master's SQL client. 
    - Master_log_file is equal to the values we previously took note of. 
```
mysql -u root --password=Knowledge -e "change master to
master_host='192.168.1.255',
master_user='pdnsslave',
master_password='Knowledge', master_log_file='mysql-bin.000001', master_log_pos=606; 
start slave;
show slave status;"
```

29. Remove and update the systems local DNS, as root.
```
ls -lh /etc/resolv.conf

rm /etc/resolv.conf

echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

30. Create a PowerDNS Admin Database.
```
mysql -u root --password=Knowledge -e "CREATE DATABASE powerdnsadmin CHARACTER SET utf8 COLLATE utf8_general_ci;"

mysql -u root --password=Knowledge -e "GRANT ALL PRIVILEGES ON powerdnsadmin.* TO 'pdnsadminuser'@'%' IDENTIFIED BY 'Knowledge';"

mysql -u root --password=Knowledge -e "FLUSH PRIVILEGES;"
```

31. Install PowerDNS Admin Dependencies.
```
apt-get install python3-dev -y 

apt-get install -y libmysqlclient-dev libsasl2-dev libldap2-dev libssl-dev libxml2-dev libxslt1-dev libxmlsec1-dev libffi-dev pkg-config -y

curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -

echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

apt-get update -y

apt-get install yarn -y
```

32. Download PowerDNS Admin.
```
apt install git -y

git clone https://github.com/ngoduykhanh/PowerDNS-Admin.git /opt/web/powerdns-admin

cd /opt/web/powerdns-admin

virtualenv -p python3 flask

. ./flask/bin/activate

pip install -r requirements.txt

cp /opt/web/powerdns-admin/config_template.py /opt/web/powerdns-admin/config.py

nano /opt/web/powerdns-admin/config.py

# --- Changes --- #
SQLA_DB_USER = 'pdnsadminuser'
SQLA_DB_PASSWORD = 'Knowledge'
SQLA_DB_HOST = '127.0.0.1'
SQLA_DB_NAME = 'powerdnsadmin'
SQLALCHEMY_TRACK_MODIFICATIONS = True

export FLASK_APP=app/__init__.py

flask db upgrade

yarn install --pure-lockfile

flask assets build

# --- Create Server File --- #
nano /etc/systemd/system/powerdns-admin.service

# --- Contents --- #
[Unit]
Description=PowerDNS-Admin
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/opt/web/powerdns-admin
ExecStart=/opt/web/powerdns-admin/flask/bin/gunicorn --workers 2 --bind unix:/opt/web/powerdns-admin/powerdns-admin.sock app:app

[Install]
WantedBy=multi-user.target

systemctl daemon-reload

systemctl start powerdns-admin

systemctl enable powerdns-admin

apt install nginx

nano /etc/nginx/sites-enabled/powerdns-admin.conf

# --- Nginx Contents --- #
server {
  listen *:80;
  server_name               propogation.vaultcipher.com;

  index                     index.html index.htm index.php;
  root                      /opt/web/powerdns-admin;
  access_log                /var/log/nginx/powerdns-admin.local.access.log combined;
  error_log                 /var/log/nginx/powerdns-admin.local.error.log;

  client_max_body_size              10m;
  client_body_buffer_size           128k;
  proxy_redirect                    off;
  proxy_connect_timeout             90;
  proxy_send_timeout                90;
  proxy_read_timeout                90;
  proxy_buffers                     32 4k;
  proxy_buffer_size                 8k;
  proxy_set_header                  Host $host;
  proxy_set_header                  X-Real-IP $remote_addr;
  proxy_set_header                  X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_headers_hash_bucket_size    64;

  location ~ ^/static/  {
    include  /etc/nginx/mime.types;
    root /opt/web/powerdns-admin/app;

    location ~*  \.(jpg|jpeg|png|gif)$ {
      expires 365d;
    }

    location ~* ^.+.(css|js)$ {
      expires 7d;
    }
  }

  location / {
    proxy_pass            http://unix:/opt/web/powerdns-admin/powerdns-admin.sock;
    proxy_read_timeout    120;
    proxy_connect_timeout 120;
    proxy_redirect        off;
  }

}

rm /etc/nginx/sites-enabled/default

systemctl restart nginx
```