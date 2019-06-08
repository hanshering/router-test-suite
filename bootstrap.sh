#!/bin/bash

echo "Getting latest exabgp.."
mkdir ../exabgp/
git clone https://github.com/Exa-Networks/exabgp.git ../exabgp/
cp exabgp.env ../exabgp/etc/exabgp/
mkfifo ../exabgp/run/exabgp.{in,out}
chmod 600 ../exabgp/run/exabgp.{in,out}

echo "Getting latest super-smash-brogp.."
mkdir ../ssbgp/
git clone https://github.com/spotify/super-smash-brogp.git ../ssbgp/
# fixing ssbgp.py to work with exabgp 4.x
ex -s -c '17i|import sys' -c x ../ssbgp/ssbgp.py
ex -s -c '83i|    sys.stdout.flush()' -c x ../ssbgp/ssbgp.py
ex -s -c '95i|    sys.stdout.flush()' -c x ../ssbgp/ssbgp.py
(cd ../ssbgp && git update-index --assume-unchanged ssbgp.py)

