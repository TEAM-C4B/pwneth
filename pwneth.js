module.exports = {
  web3(url){
      var Web3 = require('web3');
      var res = new Web3(new Web3.providers.HttpProvider(url));
      return res
    },
  getStorage(addr, idx){
      var ret_val;
      web3.eth.getStorageAt(addr, idx).then(e=>{ret_val=e;});
      require('deasync').loopWhile(function(){return ret_val == undefined});
  
      return ret_val;
    },
  listStorage(addr, len){
      for(var i=0; i<len; i++){
            /*
             *       var done = false;
             *             web3.eth.getStorageAt(addr, idx).then(e=>{console.log(e); done=true;});
             *                   require('deasync').loopWhile(function(){return !done});
             *                         */
            console.log(this.getStorage(addr, i));
          }
    },

  contract(abi, addr){
      var res = new web3.eth.Contract(abi, addr);
      return res;
    },

  getAccounts(){
      var res;
      web3.eth.getAccounts().then(e=>{res=e;});
      require('deasync').loopWhile(function(){return res == undefined});
      return res
    },

  addWallet(pubkey){
      web3.eth.accounts.wallet.add(pubkey);
      return web3.eth.accounts.wallet[0].address;
    },

  intPack(number){
      var str = number.toString(16);
  
      for(;str.length<64;){
            str += '0' + str
          }
      return '0x' + str
    },

  bytesPack(bytes){
      var res = web3.utils.fromAscii(bytes)
      for(;res.length<66;){
            res += '0'
          }
      return res
    }
};
