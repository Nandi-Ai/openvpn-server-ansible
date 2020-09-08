#!/bin/bash

# Script to periodically check existence of vpn connection
path_to_ovpn_files="/etc/openvpn/files"
$SERIAL=`cat /proc/cpuinfo | grep -i serial | awk -F ': ' '{print $2}'`

cd "$path_to_ovpn_files"

if [ ! `ps ax | grep "$SERIAL.ovpn" | grep -v grep` ]; then
    echo "Connecting to OpenVPN "
    /usr/sbin/openvpn --config "$SERIAL".ovpn &
fi
