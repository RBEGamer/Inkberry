#!/bin/bash

command="pio"
if [ "$(which "$command")" != "" ]; 
then
    echo "pio found -> no installation needed"
    exit 0
else
    echo "pio not found -> install required"
fi



if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt install curl wget screen -y
apt install python3-pip -y
apt install python3.6-venv -y
apt install python3-dev libffi-dev libssl-dev -y
apt install libbz2-dev -y

cd ~
curl -fsSL -o get-platformio.py https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py
python3 get-platformio.py


mkdir -p /usr/local/bin
ln -s ~/.platformio/penv/bin/platformio /usr/local/bin/platformio
ln -s ~/.platformio/penv/bin/pio /usr/local/bin/pio
ln -s ~/.platformio/penv/bin/piodebuggdb /usr/local/bin/piodebuggdb



pio upgrade
