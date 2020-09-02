#!/bin/bash
cd /root/openvpn-ca
source vars
./build-key --batch ${1}

