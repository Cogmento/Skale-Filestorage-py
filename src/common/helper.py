
#const InvalidCredentialsException = require('../exceptions/InvalidCredentialsException');
    #What is this supposed to do?
import binascii
#for bytes to string
import re
#for regex
import asyncio


PRIVATE_KEY_REGEX = '^(0x)?[0-9a-f]{64}$'

class Helper:

    def ensureStartsWith0x(self, x: str):
        if len(x) < 2:
            return False
        else:
            return x[:2]=='0x'


    def addBytesSymbol(self, x: str):
        if self.ensureStartsWith0x():
            return x
        else:
            return '0x' + x


    def rmBytesSymbol(self, x: str):
        if not self.ensureStartsWith0x():
            return x
        else:
            return x[2:]

    def bufferToHex(self, buffer: str):
        # bufferToHex gets called in index.js to convert filebuffers to Hexidecimal. I'm using binascii.hexlify()
        return binascii.hexlify(buffer)

    def concatBytes32Array(self, data, outputLength):
        #return data.map(x => this.rmBytesSymbol(x)).join('').slice(0, outputLength);
        x = []
        for i in data:
            x.append(self.rmBytesSymbol(i)[:outputLength])
        return x

    def validatePrivateKey(self, privateKey):
        # has to be used in try/except later
        if not re.match(PRIVATE_KEY_REGEX, privateKey):
            print('Incorrect privateKey')


    async def signAndSendTransaction(self, web3, account, privateKey, transactionData, gas):
        encoded = transactionData.encodeABI()
        contractAddress = transactionData['_parent']['_address']
        accountFromPrivateKey = web3.eth.accounts.privateKeyToAccount(privateKey)['address']

        if account != accountFromPrivateKey and account != self.rmBytesSymbol(accountFromPrivateKey):
            print('Keypair mismatch')

        tx = {'from': account,
            'data': encoded,
            'gas': gas,
            'to': contractAddress}
        signedTx = await web3.eth.accounts.signTransaction(tx, privateKey)
        return await web3.eth.sendSignedTransaction(signedTx.rawTransaction)


    async def sendTransaction(self, account, transactionData, gas):
        return await transactionData.send({
            'from': account,
            'gas': gas
        })

    async def sendTransactionToContract(self, web3, account, privateKey, transactionData, gas):
        result = ''
        if type(privateKey) == str and len(privateKey) > 0:
            if not self.ensureStartsWith0x(privateKey):
                privateKey = '0x' + privateKey
            self.validatePrivateKey(privateKey)
            try:
                result = await self.signAndSendTransaction(web3, account, privateKey, transactionData, gas)
            except:
                result = await self.sendTransaction(account, transactionData, gas)
        return result

#module.exports = Helper;