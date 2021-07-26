import os
import sys
from ipaddress import IPv4Network
from os import listdir
from os.path import isfile, join
import argparse

# Globals
CLIENT_CONFIGS_PATH = "/etc/openvpn/client"
MAKE_OPENVPN_CONFIG_SCRIPT_PATH = join(CLIENT_CONFIGS_PATH, "make_config.sh")
MAKE_NEW_KEYS_SCRIPT_PATH = join(CLIENT_CONFIGS_PATH, "add_new_keys.sh")
CCD = CLIENT_CONFIGS_PATH

if __name__ == '__main__':
    ARGPARSER = argparse.ArgumentParser()
    ARGPARSER.add_argument('-n', '--name', required=True, help='Selected Name')
    ARGS = ARGPARSER.parse_args()

    NEW_CCD_FILE = ARGS.name

    # Generate new certs
    print("Generating new certs for %s" % NEW_CCD_FILE)

    os.system(MAKE_NEW_KEYS_SCRIPT_PATH+" "+NEW_CCD_FILE)

    # Execute script to generate new openvpn file
    os.system(MAKE_OPENVPN_CONFIG_SCRIPT_PATH+" "+NEW_CCD_FILE)

    print("Please transfer %s.ovpn file to client machine" % (
        join(CLIENT_CONFIGS_PATH, "files", NEW_CCD_FILE)))

    print("Restarting openvpn service!")
    os.system("systemctl restart openvpn-server@server")

    print("Finished.")
