from web3 import Web3
from FilestorageContract import abi, contractAddress


#get testconfig
import json 
with open('testconfig.json') as json_file:
    testconfigJson = json.load(json_file)
provider = testconfigJSON.HTTPprovider
privateKey = testconfigJSON.PrivateKey
path = testconfigJSON.Path
name = testconfigJSON.FileName


#initiate Web3 object with SKALE contract
w3 = Web3(Web3.HTTPProvider(provider))
conntest = w3.isConnected()
blocktest = w3.eth.blockNumber
print(conntest)
print(blocktest)

#interact with said contract
contract = w3.eth.contract(abi = abi, address = contractAddress)
demo = contract.functions.getFileInfoList(contractAddress).call()
print(demo)
all_functions = contract.all_functions()
print(all_functions)

#get test account features 
account = w3.eth.account.privateKeyToAccount(privateKey)._address
balance = w3.eth.getBalance(account)
print(balance)
nonce = w3.eth.getTransactionCount(account)
print(nonce)
