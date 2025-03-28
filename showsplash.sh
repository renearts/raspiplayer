#!/bin/sh
cd /home/mario
sudo /usr/bin/fbi -T 1 -noverbose -a /etc/splash.png & 
python3 /home/mario/playvlc.py
