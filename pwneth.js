module.exports = {
  web3 : undefined,
  Accounts : undefined,
  walletAddr : undefined,

  setWeb3(url) {
    var Web3 = require('web3');
    var res = new Web3(new Web3.providers.HttpProvider(url));
    
    this.web3 = res
    
    return res
  },

  getStorage(addr, idx) {
    var res;
    this.web3.eth.getStorageAt(addr, idx).then(e=>{res = e;});
    require('deasync').loopWhile(function() {return res == undefined});

    return res;
  },

  listStorage(addr, len) {
    for(var i=0; i<len; i++) {
      console.log(this.getStorage(addr, i));
    }
  },

  getLastBlock() {
    var lastBlockNumber;
    this.web3.eth.getBlockNumber().then(e=>{lastBlockNumber = e});
    require('deasync').loopWhile(function() {return lastBlockNumber == undefined});

    var blockInfo;
    this.web3.eth.getBlock(lastBlockNumber).then(e=>{blockInfo = e});
    require('deasync').loopWhile(function() {return blockInfo == undefined})

    return blockInfo
  },

  contract(abi, addr) {
    var res = new this.web3.eth.Contract(abi, addr);
    
    return res;
  },

  getAccounts() {
    var res;

    this.web3.eth.getAccounts().then(e=>{res = e;});
    require('deasync').loopWhile(function() {return res == undefined});
    this.Accounts = res;

    return res
  },

  addWallet(pubkey) {
    this.web3.eth.accounts.wallet.add(pubkey);

    this.walletAddr = this.web3.eth.accounts.wallet[0].address;
    return this.walletAddr;
  },

  intPack(number) {
    var str = number.toString(16).replace("0x", "");

    for(; str.length < 64;) {
      str += '0' + str
    }

    return '0x' + str
  },

  bytesPack(bytes) {
    var res = this.web3.utils.fromAscii(bytes).replace("0x", "")
    for(; res.length < 66;) {
      res += '0'
    }

    return res
  },

  toWei(val, type) {
    return this.web3.utils.toWei(val, type);
  },

  fromWei(val, type) {
    return this.web3.utils.fromWei(val, type);
  },

  sendTransaction(from, to, value) {
    var gas;
    var res;
    this.web3.eth.estimateGas({from:from, to:to, value:value}).then(e=>{gas = e});
    require('deasync').loopWhile(function() {return gas == undefined});

    this.web3.eth.sendTransaction({from:from, to:to, value:value, gas:gas}).then(e=>{res = e});
    require('deasync').loopWhile(function() {return res == undefined});

    return res;
  },

  compileContract(filename, contractName, debug=false) {
    var filedata = require('fs').readFileSync(filename);
    var compiled = require('solc').compile(filedata.toString(), 1);

    if(compiled.errors && debug) {
      for(var i = 0; i < compiled.errors.length; i++) {
        console.log(compiled.errors[i]);
      }

      return false;
    }

    if(contractName) {
      return compiled.contracts[contractName];
    } else {
      return compiled;
    }
  },
};
