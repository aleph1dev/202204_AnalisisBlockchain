#!/bin/bash
docker run -v ${PWD}/Bitcoin:/home/bitcoin/.bitcoin --name "bitcoind" -p 8332:8332 -d --restart unless-stopped ruimarinho/bitcoin-core \
 -printtoconsole \
 -server=1 \
 -rpcbind=0.0.0.0 \
 -rpcallowip=0.0.0.0/0 \
 -txindex=1 \
 -rescan \
 -rpcauth='bitcoin:1eb7790f3e0ba361d60882af8f55b4af$518cc8ee455e24f900a7a1e4878eb46d98667e52c95835de5035d8fc56d248a8'
