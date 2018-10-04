from web3 import Web3           #pip3 install web3
from solc import compile_source #pip3 install py-solc

def HBconvert(data):
	result = str(hex(data[0]))

	for i in range(1,len(data)):
		result += str(hex(data[i])[2:])

	return result

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


def mainnet():
	return Web3(Web3.HTTPProvider("https://mainnet.infura.io"))

def ropsten():
	return Web3(Web3.HTTPProvider("https://ropsten.infura.io"))

def kovan():
	return Web3(Web3.HTTPProvider("https://kovan.infura.io"))

def rinkeby():
	return Web3(Web3.HTTPProvider("https://rinkeby.infura.io"))

def local(port):
	return Web3(HTTPProvider('http://localhost:'+str(port)))

############################# get info #####################################

def getStorageAt(web3, addr, idx):
	checkaddr = web3.toChecksumAddress(addr)
	temp = web3.eth.getStorageAt(checkaddr, idx)

	return HBconvert(temp)

def getbytecode(web3, addr):
	temp = web3.eth.getCode(addr)
	result = str(hex(temp[0]))

	return HBconvert(temp)

def getblock(web3):
	block = web3.eth.getBlock('latest')

	return block

############################### transtion ##################################
def deploy_contract(web3, contract_interface):
	tx_hash = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin']).deploy()
	address = web3.eth.getTransactionReceipt(tx_hash['contractAddress'])
	
	return address

def de(web3, filename):
	compiled_sol = compile_source_file(filename)

	contract_id, contract_interface = compiled_sol.popitem()
	address = deploy_contract(web3, contract_interface)

	print("contract_id, address")

def deploy(web3, filename, contractname, address):
	compiled_sol = compile_source(open(filename).read())
	contract_interface = compiled_sol['<stdin>:'+contractname]

	web3.eth.defaultAccount = address
	Contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])	

	tx_hash = Contract.constructor().transact()	
	tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

	contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=contract_interface['abi'],)	

def compile(web3, address, password, filename, contractname):
	web3.personal.unlockAccount(web3.toChecksumAddress(address), password, 0)
	compiled = compile_source(open(filename).read())
	interface = compiled['<stdin>:'+contractname]
	contract = web3.eth.contract(abi=interface['abi'],
				   bytecode=interface['bin'],
				   bytecode_runtime=interface['bin-runtime'])
	tx_hash = contract.deploy(transaction={'from': web3.toChecksumAddress(address)})
	web3.miner.start(2)

def sendtx(web3, _gas, _to, _value, _data, private_key):
	signed_txn = web3.eth.account.signTransaction(dict(
    	nonce=web3.eth.getTransactionCount(web3.eth.coinbase),
	gasPrice=web3.eth.gasPrice,
	gas=_gas,
	to=_to,
	value=_value,
	data=_data,),
	private_key,)

	return web3.eth.sendRawTransaction(signed_txn.rawTransaction)
