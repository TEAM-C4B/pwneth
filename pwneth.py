from web3 import Web3, HTTPProvider
from solc import compile_source
from eth_account import Account
import bs4
import json
import requests

################## convert data #########################

def toHex(target):
	result = Web3.toHex(target)

	return result

def toText(target):
	result = Web3.toText(target)

	return result

def toBytes(target):
	result = Web3.toBytes(target)

	return result

def toInt(target):
	result = Web3.toInt(target)

	return result

def toWei(target):
	result = Web3.toWei(target)

	return result

def fromWei(target):
	result = Web3.fromWei(target)

	return result

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
	return Web3(HTTPProvider("http://" + ip + ':' + str(port)))

############################# get info #####################################

def getStorageAt(web3, addr, idx):
	checkaddr = web3.toChecksumAddress(addr)
	data = web3.eth.getStorageAt(checkaddr, idx)

	return toHex(data)

def getbytecode(web3, addr):
	data = web3.eth.getCode(addr)

	return toHex(data)

def getblock(web3):
	block = web3.eth.getBlock('latest')

	return block

############################### transaction ##################################
def create_contract(web3, filename, contractname, privateKey):
	compiled_sol = compile_source(open(filename).read())
	contract_interface = compiled_sol['<stdin>:'+contractname]

	contract_ = web3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin'])

	acct = web3.eth.account.privateKeyToAccount(privateKey)

	construct_txn = contract_.constructor().buildTransaction({
	'from': acct.address,
	'nonce': web3.eth.getTransactionCount(acct.address)})

	signed = acct.signTransaction(construct_txn)

	print("Tx Hash : " + web3.eth.sendRawTransaction(signed.rawTransaction).hex())

	return contract_

def call_function(web3, privateKey, _to, callfunc, argv):
	name, code = parse_code(web3, _to)
	compiled_sol = compile_source(toText(code))
	contract_interface = compiled_sol['<stdin>:' + toText(name)]

	contract_ = web3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin'])

	acct = web3.eth.account.privateKeyToAccount(privateKey)
	fun = contract_.functions[callfunc]
	tx = fun(argv).buildTransaction({
    	'from': acct.address,
    	'to': _to,
    	'nonce': web3.eth.getTransactionCount(acct.address)})

	signed = acct.signTransaction(tx)

	print("Tx Hash : " + web3.eth.sendRawTransaction(signed.rawTransaction).hex())

####################################  parse code #####################################3
def parse_code(web3, address):
	if(web3.net.version == '1'):
		api_url = 'https://api.etherscan.io/api?module=contract&action=getsourcecode&address=' + address
	elif(web3.net.version == '3'):
		api_url = 'https://api-ropsten.etherscan.io/api?module=contract&action=getsourcecode&address=' + address
	elif(web3.net.version == '42'):
		api_url = 'https://api-kovan.etherscan.io/api?module=contract&action=getsourcecode&address=' + address
	elif(web3.net.version == '4'):
		api_url = 'https://api-rinkeby.etherscan.io/api?module=contract&action=getsourcecode&address=' + address

	r = requests.get(api_url)
	data = r.text.encode('utf-8')

	info = json.loads(data)['result']
	name = info[0]['ContractName'].encode('utf-8')
	code = info[0]['SourceCode'].encode('utf-8')

	return name, code
