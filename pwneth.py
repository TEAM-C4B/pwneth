import bs4
import json
import requests

from web3 import Web3, HTTPProvider
from solc import compile_source
from eth_account import Account

###################### connect server ###############################

def mainnet(key):
    return Web3(Web3.HTTPProvider("https://mainnet.infura.io/" + key))


def ropsten(key):
    return Web3(Web3.HTTPProvider("https://ropsten.infura.io/" + key))


def kovan(key):
    return Web3(Web3.HTTPProvider("https://kovan.infura.io/" + key))


def rinkeby(key):
    return Web3(Web3.HTTPProvider("https://rinkeby.infura.io/" + key))


def local(ip, port):
    return Web3(HTTPProvider("http://" + ip + ":" + str(port)))

############################# get info #####################################

def get_storage_at(web3, addr, idx):
    check_addr = web3.toChecksumAddress(addr)
    data = web3.eth.getStorageAt(check_addr, idx)

    return Web3.toHex(data)


def get_bytecode(web3, addr):
    data = web3.eth.getCode(addr)

    return Web3.toHex(data)


def get_block(web3):
    block = web3.eth.getBlock("latest")

    return block

############################### transaction ##################################

def create_contract(web3, file_name, contract_name, private_key):
    compiled_sol = compile_source(open(file_name).read())
    contract_interface = compiled_sol["<stdin>:" + contract_name]

    contract = web3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])

    acct = web3.eth.account.privateKeyToAccount(private_key)

    construct_txn = contract.constructor().buildTransaction({
    		"from": acct.address,
    		"nonce": web3.eth.getTransactionCount(acct.address)
    })

    signed = acct.signTransaction(construct_txn)

    print("Tx Hash : " + web3.eth.sendRawTransaction(signed.rawTransaction).hex())

    return contract


def call_function(web3, private_key, to, value, call_func, *argv):
    name, code = parse_code(web3, to)
    compiled_sol = compile_source(Web3.toText(code))
    contract_interface = compiled_sol["<stdin>:" + Web3.toText(name)]

    contract = web3.eth.contract(abi=contract_interface["abi"],bytecode=contract_interface["bin"])

    acct = web3.eth.account.privateKeyToAccount(private_key)
    fun = contract.functions[call_func]
    tx = fun(*argv).buildTransaction({
	    "from": acct.address,
	    "to": to,
	    "value": value,
	    "nonce": web3.eth.getTransactionCount(acct.address)
    })

    signed = acct.signTransaction(tx)

    print("Tx Hash : " + web3.eth.sendRawTransaction(signed.rawTransaction).hex())

####################################  parse code #####################################

def parse_code(web3, address):
    version = web3.net.version

    if(version == "1"):
    	api_url = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=" + address
    elif(version == "3"):
    	api_url = "https://api-ropsten.etherscan.io/api?module=contract&action=getsourcecode&address=" + address
    elif(version == "42"):
    	api_url = "https://api-kovan.etherscan.io/api?module=contract&action=getsourcecode&address=" + address
    elif(version == "4"):
    	api_url = "https://api-rinkeby.etherscan.io/api?module=contract&action=getsourcecode&address=" + address

    r = requests.get(api_url)
    data = r.text.encode("utf-8")

    info = json.loads(data)["result"]
    name = info[0]["ContractName"].encode("utf-8")
    code = info[0]["SourceCode"].encode("utf-8")

    return name, code
