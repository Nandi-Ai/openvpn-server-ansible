#!/bin/bash

# Script for installing required software and configuration

apt-get update
# apt-get upgrade -y
apt-get install -y openvpn

# create scripts directory
mkdir -p /opt/scripts

# download required scripts over ftp
host="remote.nandi.io"
user="access"
pass="Dahm3aisee7O"

for FILE in "check_openvpn.sh" "GetOpenVpnClientFile.py" "crontab.tpl"
do
	echo "Downloading $FILE..."
	curl -u access:Dahm3aisee7O  -o /opt/scripts/$FILE http://remote.nandi.io/scripts/$FILE
done

# Copy custom crontab
cp -rf /opt/scripts/crontab.tpl /etc/cron.d/custom
systemctl enable ssh
systemctl start ssh
systemctl enable openvpn@server.service --now
