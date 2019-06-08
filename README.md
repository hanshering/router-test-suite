Setup
=====
Clone repo:
```
git clone https://github.com/hanshering/router-test-suite.git
```

Install python2 yaml module for super-smash-brogp and python3 jinja2 module for config generation:
```
sudo apt install python-yaml python3-jinja2
```

Run bootstrap.sh to get prerequisites:
```
cd router-test-suite/
./bootstrap.sh
```

Config generation
=====
Edit `generate-exabgp-config.py` if you need to customize IP addresses and AS 
numbers. Default values are:
- Router AS: 1000
- Exabgp AS: 1001-1255
- IPv4 transfer networks: 10.0.i.0/24, where i is the peer id
- IPv6 transfer networks: fd00::10:0:i:0/126, where i is the peer id
- Router always gets the .1/:1 address, exabgp always gets the .2/:2 address

Run `generate-exabgp-config.py` to generate all the configs.
```
./generate-exabgp-config.py
```
Edit `generate-router-config.py` if you need to customize interface name, 
IP addresses, and AS numbers.

Run `generate-router-config.py` to generate the interface and bgp config for the
router.
```
./generate-exabgp-config.py templates/cisco.template 255
```
Valid peer count is 1-255.

Run tests
=====
Run test with 5 peers:
```
./run-test.sh -t ROUTE-001 -n 5
```
Valid tests are: ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, LINKFAIL-001. Maximum number of peers is 255, default is 1.

Stop test:
```
./run-test.sh -s
```
