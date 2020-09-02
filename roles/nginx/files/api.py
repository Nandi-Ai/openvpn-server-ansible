import os
import os.path
import logging
import json
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
TOKEN = "iyietee6aiPh7sief7Iev0ohzeesh3"

@app.route('/info', methods=['GET'])
def get_info():
    """ Returns 'Running' string. Used to test if api is running """
    LOGGER.info('Called info method')
    return "Running"


@app.route('/getCertificate', methods=['POST'])
def get_certificate():
    """ Returns openvpn certificate
        Takes serial number as param """
    LOGGER.info('Check if file exist - if not create it !')
    request_data = json.loads(request.get_json())

    if "token" in request_data:
        token = str(request_data["token"])
        if token != TOKEN:
            response_obj = {'status':'Authorization needed'}
            return response_obj

    if "serial_number" in request_data: # Get Checks And Server
        serial_number = str(request_data["serial_number"])
        file_path = "/root/client-configs/files/" + str(serial_number) + ".ovpn"
        if os.path.isfile(file_path):
            # Created already
            LOGGER.info('File Exist Already - return certificate')
            with open(file_path, 'r') as file:
                cert = file.read()
                response_obj = {'status':'true', 'certificate':cert}
                return json.dumps(response_obj)
        else:
            # Need to create new cert
            LOGGER.info('Generate new certificate for %s', serial_number)
            os.system("python3 /root/client-configs/add_new_client.py -n "+serial_number)
            if check_if_file_exist(file_path):
                with open(file_path, 'r') as file:
                    cert = file.read()
                response_obj = {'status':'true', 'certificate':cert}
                return json.dumps(response_obj)

            response_obj = {'status':'Failed to generate certificate for '+str(serial_number)}
            return json.dumps(response_obj)

    else:
        response_obj = {'status':'Bad request'}
        return response_obj # If serial_number is not in request_data

def check_if_file_exist(file_path):
    """ Check if file exists - returns true if yes """
    if os.path.isfile(file_path):
        return True # Not exist
    return False # Exist


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
