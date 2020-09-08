import os
import sys
from ipaddress import IPv4Network
from os import listdir
from os.path import isfile, join
import argparse

# Globals
CLIENT_CONFIGS_PATH = "/root/client-configs"
MAKE_OPENVPN_CONFIG_SCRIPT_PATH = join(CLIENT_CONFIGS_PATH, "make_config.sh")
MAKE_NEW_KEYS_SCRIPT_PATH = join(CLIENT_CONFIGS_PATH, "add_new_keys.sh")
CCD = "/etc/openvpn/ccd"
NETWORK = IPv4Network('10.8.0.0/24')
RESERVED_IP = []

def get_new_client_data():

    ccd_files = [f for f in listdir(CCD) if isfile(join(CCD, f))]

    for ccd_file in ccd_files:
        with open(join(CCD, ccd_file), 'r') as ccdf:
            for line in ccdf.readlines():
                if 'ifconfig-push' in line:
                    segments = line.split()
                    RESERVED_IP.append(segments[1])

if __name__ == '__main__':
    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-n', '--name', required=True, help='Selected Name')
    ARGS = ARGPARSER.parse_args()

    NEW_CCD_FILE = ARGS.name
    if os.path.exists(os.path.join(CCD, NEW_CCD_FILE)):
        print("Name already taken")
        sys.exit(1)

    # Get reserved ip addresses
    get_new_client_data()
    HOSTS_ITERATOR = (host for host in NETWORK.hosts() if str(host) not in RESERVED_IP)
    NEW_IP = next(HOSTS_ITERATOR)
    ENTRY = "ifconfig-push %s 255.255.255.255" % (NEW_IP)

    # Generate new certs
    print("Generating new certs for %s" % NEW_CCD_FILE)

    os.system(MAKE_NEW_KEYS_SCRIPT_PATH+" "+NEW_CCD_FILE)

    # Execute script to generate new openvpn file
    os.system(MAKE_OPENVPN_CONFIG_SCRIPT_PATH+" "+NEW_CCD_FILE)

    # Create new ccd file
    with open(join(CCD, NEW_CCD_FILE), 'w') as nccd:
        nccd.write(ENTRY)

    print("Please transfer %s.ovpn file to client machine" % (
        join(CLIENT_CONFIGS_PATH, "files", NEW_CCD_FILE)))

    print("Restarting openvpn service!")
    os.system("service openvpn restart")

    print("Finished.")
