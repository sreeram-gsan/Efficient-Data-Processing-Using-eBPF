#!/bin/sh
nc -kul 127.0.0.1 7888 &
echo "Started Listening on port 7888"
sudo python3 eBPF/rest-server.py
