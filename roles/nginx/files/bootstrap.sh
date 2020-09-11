#!/bin/bash

# Script for installing required software and configuration

apt-get update
#apt-get upgrade -y
apt-get install -y openvpn

# create scripts directory
mkdir -p /opt/scripts

# download required scripts over ftp
host="remote.nandi.io"
user="access"
pass="Dahm3aisee7O"

FILE="check_openvpn.sh"
curl -u access:Dahm3aisee7O  -o /opt/scripts/$FILE http://remote.nandi.io/scripts/$FILE

FILE="GetOpenVpnClientFile.py"
curl -u access:Dahm3aisee7O  -o /opt/scripts/$FILE http://remote.nandi.io/scripts/$FILE

# Write out current crontab
crontab -l > mycron

# Adding new crons
echo "entry 1"
cat mycron | grep 'openvpn@server.service'  && echo 'Entry 1 exists' || echo "@reboot systemctl start openvpn@server.service" >> mycron

echo "entry 2"
cat mycron | grep 'check_openvpn.sh'  && echo 'Entry 2 exists' || echo '00 * * * *	root sh /opt/scripts/check_openvpn.sh' >> mycron

echo "entry 3"
ENTRY="20 */3 * * *	root python3 /opt/scripts/GetOpenVpnClientFile.py"
cat mycron | grep 'GetOpenVpnClientFile.py'  && echo 'Entry 3 exists' || echo "20 */3 * * *	root python3 /opt/scripts/GetOpenVpnClientFile.py" >> mycron

# Install new crontab
crontab mycron
rm mycron

#Enable services
systemctl enable ssh
systemctl start ssh
systemctl enable openvpn@server.service --now

echo "Rebooting system"
reboot

