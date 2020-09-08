import os
import json
import sys
import requests

def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial


if __name__ == '__main__':

    TOKEN = "iyietee6aiPh7sief7Iev0ohzeesh3"
    SERIAL_NUMBER = getserial()
    if SERIAL_NUMBER == "ERROR000000000":
        print("Could not get serial. Exiting!")
        sys.exit(1)

    CERT_DIR = "/etc/openvpn/files/"
    CERT_FILE = "/etc/openvpn/files/"+SERIAL_NUMBER+".ovpn"
    if os.path.isfile(CERT_FILE):
        print("Certificate file %s already exists. Exiting." % (CERT_FILE))
        sys.exit(0)

    print("Requesting for cert")
    URL = 'http://api.remote.nandi.io/getCertificate'
    REQUEST_OBJ = {'token':TOKEN, 'serial_number':str(SERIAL_NUMBER)}

    RESP = requests.post(URL, json=json.dumps(REQUEST_OBJ))
    RESP_JSON = RESP.json()

    if RESP_JSON['status'] == "true":
        if not os.path.isdir(CERT_DIR):
            print("Making cert dir %s" % (CERT_DIR))
            os.makedirs(CERT_DIR)

        print("Saving cert to %s" % CERT_FILE)
        with open(CERT_FILE, 'w') as CERT:
            CERT.write(RESP_JSON['certificate'])
        print('Cert file saved')
    else:
        print("Failed to get client %s.ovpn file. Reason: %s" %(SERIAL_NUMBER, RESP_JSON['status']))
        sys.exit(1)
