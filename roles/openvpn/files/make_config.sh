#!/bin/bash

# First argument: Client identifier

KEY_DIR=/etc/openvpn/client/$1
OUTPUT_DIR=/home/ubuntu/certs
BASE_CONFIG=/etc/openvpn/client/base.conf
SERVER_TA=/etc/openvpn/server/ta.key

cat ${BASE_CONFIG} \
    <(echo -e '<ca>') \
    ${KEY_DIR}/ca.crt \
    <(echo -e '</ca>\n<cert>') \
    ${KEY_DIR}/${1}.crt \
    <(echo -e '</cert>\n<key>') \
    ${KEY_DIR}/${1}.key \
    <(echo -e '</key>\n<tls-auth>') \
    ${SERVER_TA} \
    <(echo -e '</tls-auth>') \
    > ${OUTPUT_DIR}/${1}.ovpn
