#!/bin/bash
docker exec --user bitcoin bitcoind bitcoin-cli -rpcuser=bitcoin -rpcpassword=MebsxkAhSC9eXfeTVYQWojO7V9pLMKliEQL8YxHFIPI= $@
#docker exec --user bitcoin -ti bitcoind curl --user bitcoin --data-binary '{"jsonrpc": "1.0", "id": "curltest", "method": "listtransactions", "params": ["analysis", 0, 200, true]}' -H 'content-type: text/plain;' http://127.0.0.1:8332/
