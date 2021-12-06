# Getting Started with eBPF

## Setting up dependencies for BPF
- sudo apt update
- sudo apt install clang llvm libelf-dev libpcap-dev gcc-multilib build-essential -y
- sudo apt install linux-tools-$(uname -r) -y
- sudo apt install linux-tools-common linux-tools-generic -y
- sudo apt-get install bpfcc-tools linux-headers-$(uname -r) -y

## Change DNS Nameserver in Ubuntu
- sudo vi /etc/netplan/{something.yaml}
- Add :
    nameservers:
            addresses: [8.8.8.8, 8.8.4.4]
- sudo netplan apply
- systemd-resolve --status | grep 'DNS Servers' -A2

## Setting up docker
- sudo apt-get update
- sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
- curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
- echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
- sudo apt-get update
- sudo apt-get install docker-ce docker-ce-cli containerd.io

## Debugging Tips
- ip link show dev lo  -> Show all interface details
- sudo ip link set dev lo xdpgeneric off -> Remove attached XDP program from the interface

## Test your XDP program
- nc -kul 127.0.0.1 7999 -> Listening on port 7999
- nc -kul 127.0.0.1 7998
- nc -u 127.0.0.1 7999 -> Sends UDP Packets to port 7999

## Resolve Common issues (eBPF and Docker Container)
- Run docker with --privileged
- set "ulimit -l 10240"
- sudo mount -t debugfs debugfs /sys/kernel/debug
