#!/bin/sh
nc -kul 7888 &
echo "Started Listening on port 7888"
sudo python3 eBPF/rest-server.py
