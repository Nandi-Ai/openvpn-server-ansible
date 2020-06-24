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
