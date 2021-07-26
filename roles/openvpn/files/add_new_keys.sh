#!/bin/bash

CLIENT_DIR="/etc/openvpn/client"
CA_DIR="/etc/easy-rsa"

cd $CA_DIR

openssl rand -writerand pki/.rnd
./easyrsa --batch build-client-full ${1} nopass

mkdir $CLIENT_DIR/${1}

cp -rp $CA_DIR/pki/ca.crt $CA_DIR/pki/issued/$1.crt $CA_DIR/pki/private/$1.key $CLIENT_DIR/${1}
