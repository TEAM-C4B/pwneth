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
def createcontract(web3, filename, contractname, privateKey):
	compiled_sol = compile_source(open(filename).read())
	contract_interface = compiled_sol['<stdin>:'+contractname]

	contract_ = web3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin'])

	acct = web3.eth.account.privateKeyToAccount(privateKey)

	construct_txn = contract_.constructor().buildTransaction({
		'from': acct.address,
		'nonce': web3.eth.getTransactionCount(acct.address),
		'gas': 1728712,
		'gasPrice': web3.toWei('21', 'gwei')})

	signed = acct.signTransaction(construct_txn)

	print(web3.eth.sendRawTransaction(signed.rawTransaction).hex())
	print("nice transaction")

	return contract_

def callfunction(web3, filename, contractname, privateKey, _to, callfunc, argv):
	compiled_sol = compile_source(open(filename).read())
	contract_interface = compiled_sol['<stdin>:'+contractname]

	contract_ = web3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin'])

	acct = web3.eth.account.privateKeyToAccount(privateKey)
	fun = contract_.functions[callfunc]
	tx = fun(argv).buildTransaction({
    	'from': acct.address,
    	'to': _to,
    	'nonce': web3.eth.getTransactionCount(acct.address),
   	'gas': 1728712,
    	'gasPrice': web3.toWei('21', 'gwei')})

	signed = acct.signTransaction(tx)

	print(web3.eth.sendRawTransaction(signed.rawTransaction).hex())
	print("nice transaction")
	
