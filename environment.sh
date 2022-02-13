#!/bin/bash

sudo apt update
sudo apt dist-upgrade -y
sudo apt-get update --allow-releaseinfo-change

sudo pip3 install --upgrade pip
sudo pip3 install --upgrade setuptools


sudo pip3 install pybind11
pip3 install -U --user six wheel mock
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list 
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install python3-pycoral -y 
sudo apt-get install python3-edgetpu -y

sudo python3 -m pip install opencv-python==4.5.4.60