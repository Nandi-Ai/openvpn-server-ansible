# openvpn-server-ansible
Ansible playbook for setting up openvpn server and scripts for creating new users and keys

To configure server on amazon:
- Update inventory file
- Run:
`ansible-playbook playbook.yml -i inventory --private-key=/path/to/key.pem`

When server is set up you can log on and create new client keys:
cd /root/client-configs
python3 add_new_client.py

This will create new keys and config for client


# Raspberry Pi bootstrap
To bootstrap Raspberry run as root on device:

`mkdir /opt/scripts`

`curl -u access:Dahm3aisee7O  -o /opt/scripts/bootstrap.sh http://remote.nandi.io/scripts/bootstrap.sh`

`sh /opt/scripts/bootstrap.sh`

This script will install required packages, download scrips and set up cron jobs
