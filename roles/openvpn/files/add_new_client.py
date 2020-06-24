import re
import os
from ipaddress import IPv4Network
from os import listdir
from os.path import isfile, join

# Globals
CLIENT_CONFIGS_PATH = "/root/client-configs"
MAKE_OPENVPN_CONFIG_SCRIPT_PATH = join(CLIENT_CONFIGS_PATH, "make_config.sh")
MAKE_NEW_KEYS_SCRIPT_PATH = join(CLIENT_CONFIGS_PATH, "add_new_keys.sh")
CCD = "/etc/openvpn/ccd"
NETWORK = IPv4Network('10.8.0.0/24')
RESERVED_IP = []
CLIENT_PREFIX = 'client'
MAX_CLIENT_ID = 0

def get_new_client_data():

    global MAX_CLIENT_ID
    ccd_files = [f for f in listdir(CCD) if isfile(join(CCD, f))]

    for ccd_file in ccd_files:

        # get number of client
        res = re.search("^"+CLIENT_PREFIX+"(\\d+)", ccd_file)
        if int(res.group(1)) > MAX_CLIENT_ID:
            MAX_CLIENT_ID = int(res.group(1))

        with open(join(CCD, ccd_file), 'r') as ccdf:
            for line in ccdf.readlines():
                if 'ifconfig-push' in line:
                    segments = line.split()
                    RESERVED_IP.append(segments[1])

if __name__ == '__main__':

    get_new_client_data()
    MAX_CLIENT_ID += 1
    new_ccd_file = "%s%d" % (CLIENT_PREFIX, MAX_CLIENT_ID)
    hosts_iterator = (host for host in NETWORK.hosts() if str(host) not in RESERVED_IP)
    new_ip = next(hosts_iterator)
    entry = "ifconfig-push %s 255.255.255.255" % (new_ip)

    # Generate new certs
    print("Generating new certs for %s" % new_ccd_file)
    os.system(MAKE_NEW_KEYS_SCRIPT_PATH+" "+new_ccd_file)

    # Execute script to generate new openvpn file
    os.system(MAKE_OPENVPN_CONFIG_SCRIPT_PATH+" "+new_ccd_file)

    # Create new ccd file
    with open(join(CCD, new_ccd_file), 'w') as nccd:
        nccd.write(entry)

    print("Please transfer %s.ovpn file to client machine" % (
        join(CLIENT_CONFIGS_PATH, "files", new_ccd_file)))

    print("Restarting openvpn service!")
    os.system("service openvpn restart")

    print("Finished.")
