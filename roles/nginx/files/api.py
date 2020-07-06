from flask import Flask, request, render_template
import os
import logging
import os.path
from os import path
import os
import time
import shutil
import json


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/checkIfFileExist', methods=['POST'])
def checkIfFileExist():
    logger.info(f'Check if file exist - if not create it !')
    request_data = json.loads(request.get_json())
    if "serialNumber" in request_data: # Get Checks And Server
        serialNumber=str(request_data["serialNumber"])
        filePath = "/root/client-configs/files/" + str(serialNumber) + ".ovpn"
        if os.path.isfile("/home/vsftp/ftp/"+str(serialNumber)+".ovpn"):
            # Created already
            logger.info(f'File Exist Already - return true')
            return "true"
        else: # Need to create
            logger.info(f'Create client .ovpn file')
            os.system("python3 /root/client-configs/add_new_client.py -n "+str(serialNumber))
            countSeconds=0
            while True:
                if countSeconds <=30: # Waiting 30 seconds maximum
                    if checkIfFileExist(filePath):
                        shutil.move(filePath,"/home/vsftp/ftp/"+str(serialNumber)+".ovpn")
                        return "true" # Return to the post request
                    else:
                        time.sleep(1)
                        countSeconds += 1
                        print("Seconds:",countSeconds)

                else:break
            return "false"

    else:return "false" # If serialNumber is not in request_data

def checkIfFileExist(filePath):
    print("Checking if",filePath,"Exist")
    if os.path.isfile(filePath):
        return True # Not exist
    return False # Exist


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

