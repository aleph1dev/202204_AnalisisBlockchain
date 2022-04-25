import datetime
import json
import time
import os
from bitcoinlib.services.bitcoind import BitcoindClient
from bitcoinlib.transactions import transaction_deserialize
from creds import *
import sys
import queue
from transactions import *

sys.setrecursionlimit(5000)

# Configuration parameters are stored within creds.py.
# See creds_example.py for more info.

result = open("traverse_outputB_d3.csv","w+")
result.write("Source,Target,Label,Address,Weight,Origin,Date,Height,Fee\n")

# Preload Addresses
prev_result = open("cache.csv", "r")

line = prev_result.readline()

ht = {}

first = True
n = 0

while False: #line:
  n += 1
  data = line.split(",")
  if first:
    ht[data[0]] = True
    ht[data[1]] = True
    first = False
  else:
    ht[data[0]] = True
  line = prev_result.readline()

print("Nodes found: {}".format(len(ht)))

base_url = "http://{}:{}@{}:{}".format(
    rpc_user,
    rpc_pass,
    server_addr,
    server_port
  )

bdc = BitcoindClient(base_url=base_url)

def gettransaction(txid,tries=1):
  global bdc
  try_counter = 0
  response = None
  while try_counter < tries:
    try:
      response = bdc.gettransaction(txid)
    except:
      print("Error fetching transactions. Trying again...")
      time.sleep(3)
      bdc = BitcoindClient(base_url=base_url)
    try_counter += 1

  if response is None:
    raise Exception("Error: unable to fetch transaction")

  return response

def getrawtransaction(txid,tries=1):
  global bdc
  try_counter = 0
  response = None
  while try_counter < tries:
    try:
      response = bdc.getrawtransaction(txid)
    except:
      print("Error fetching transactions. Trying again...")
      time.sleep(3)
      bdc = BitcoindClient(base_url=base_url)
    try_counter += 1

  if response == None:
    raise Exception("Error: unable to fetch transaction")

  return response

not_before = datetime.datetime(2018, 1, 1)

cb_idx = 0

class TxQueueElement:
    def __init__(self, txid, depth):
        self.txid = txid
        self.depth = depth

tx_queue = queue.Queue()

def extracttransactions(txid,max_depth=3,depth=0,prev_tx=None):
    global bdc, ht, cb_idx
    if depth == max_depth:
      return

    is_origin = False
    tx = None
    if prev_tx is None:
      is_origin = True
      #raw_tx = getrawtransaction(txid,15)
      #tx = transaction_deserialize(raw_tx)
      tx = gettransaction(txid,15)
    else:
      tx = prev_tx

    print("--Current depth-- {}".format(depth))

    #if len(tx.inputs) > 10:
    #  print("Exchange candidate. Skipping")
    #  fee = '' if tx.fee is None else tx.fee
    #  output = "{},{},{},edge,{},{},\"{}\",{},{}\n".format(
    #    "exchange-{}".format(txid[-5:]),
    #    txid,
    #    "exchange-{}".format(txid[-5:]),
    #    tx.input_total,
    #    is_origin,
    #    tx.date.isoformat(),
    #    tx.block_height,
    #    fee
    #    )
    #  result.write(output)
    #  result.flush()
    #  print(output)
    #  return

    print("Outputs:")
    for tx_o in tx.outputs:
      tx_o_dict = tx_o.as_dict()
      output = "{},{},{}\n".format(txid,tx_o_dict['address'],tx_o_dict['value'])
      print(output)

    print("Inputs:")
    for tx_i in tx.inputs:
      tx_i_dict = tx_i.as_dict()
      prev_txid = tx_i_dict['prev_txid']
      value = tx_i_dict['value']
      address = ""
      position = tx_i_dict['index_n']

      if tx_i.address == "":
        cb_idx += 1
        address = "Not_supported_addr-{}".format(cb_idx)
      else:
        address = tx_i.address

      output = "{},{},{}\n".format(
        prev_txid,
        address,
        value
        )
      result.write(output)
      print(output)
      if prev_txid not in ht and (depth+1) < max_depth:
          print("{} not fully explored. Adding it to the queue.".format(prev_txid))
          tx_queue.put(TxQueueElement(prev_txid, depth+1))
    result.flush()

    ht[txid] =  True
    # We use a dictionary as a hashtable
    # to prevent traversing previously
    # explored branches

idx = 0
max_depth = 50
print("Bootstrap:")
for txid in transactions:
  idx += 1
  print("TX {} of {}:".format(str(idx),len(transactions)))
  extracttransactions(txid,max_depth=max_depth)

while not tx_queue.empty():
  size = tx_queue.qsize()
  tx_queued = tx_queue.get()
  print("Queue size {}".format(str(size)))
  extracttransactions(tx_queued.txid, depth=tx_queued.depth, max_depth=max_depth)
