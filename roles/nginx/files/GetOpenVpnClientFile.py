import requests
import os
import json
import subprocess
import shlex
import argparse


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-d', '--dir', default='./', help='Selected Dir')
    args = argparser.parse_args()
    DIR = args.dir
    serialNumber=os.popen('sudo dmidecode -s system-serial-number').read()
    if serialNumber.endswith("\n"):
        serialNumber=serialNumber[0:-2]

    url = 'http://3.125.230.57:5000/checkIfFileExist'
    serialObj = {'serialNumber':str(serialNumber)}

    x = requests.post(url, json =json.dumps(serialObj))
    if x.text == "true":
        # Pull client file by ftp
        subprocess.call(shlex.split('./ftp.sh '+str(serialNumber)+" "+DIR))
    else:print("Failed to get client .ovpn file")
    print(x)

