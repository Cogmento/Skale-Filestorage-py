# this is a python implementation of https://github.com/skalenetwork/filestorage.js

import asyncio
import json
from web3 import Web3

#const constants = require('./common/constants');
#const configJson = require('./contracts_config.json');
#const Helper = require('./common/helper');

from common import constants
with open('contracts_config.json') as json_file:
    configJson = json.load(json_file)
from common.helper import Helper

#const abi = configJson[constants.FILESTORAGE_CONTRACTNAME]['abi'];
#const contractAddress = configJson[constants.FILESTORAGE_CONTRACTNAME]['address'];

abi = configJson[constants.FILESTORAGE_CONTRACTNAME]['abi']
contractAddress = configJson[constants.FILESTORAGE_CONTRACTNAME]['address']


class FilestorageContract:
    #Initialization of FilestorageContract - py wrapper for solidity smart contract
    #original js:
    #constructor(web3) {
    #    this.web3 = web3;
    #    this.contract = new web3.eth.Contract(abi, contractAddress);
    #}
    def __init__(self, w3):
        self.w3 = w3
        self.contract = w3.eth.contract(abi = abi, address = contractAddress)
        self.Helper = Helper()

    #Python wrapper for solidity function startUpload. Creates empty file of a preset size on SKALE chain node
    #original js:
    #async startUpload(address, name, size, privateKey = '') {
    #    let txData = this.contract.methods.startUpload(name, size);
    #    return await Helper.sendTransactionToContract(this.web3, address, privateKey, txData, constants.STANDARD_GAS);
    #}
    async def startUpload(self, name, size, privateKey, account,  enableLogs):
        if enableLogs: 
            print('nonce: '+str(self.w3.eth.getTransactionCount(account)))
        txData = {'from':account, 'nonce':self.w3.eth.getTransactionCount(account),'gas':constants.STANDARD_GAS}
        txData = self.contract.functions.startUpload(name, size).buildTransaction(txData)
        await self.Helper.signAndSendTransaction(self.w3, privateKey, txData)

    #Python wrapper for solidity function uploadChunk. Writes chunk to the file to specific position
    #original js
    #async uploadChunk(address, name, position, data, privateKey = '') {
    #   let txData = this.contract.methods.uploadChunk(name, position, data);
    #    return await Helper.sendTransactionToContract(this.web3, address, privateKey, txData, constants.WRITING_GAS);
    #}
    async def uploadChunk(self, name, position, data, privateKey, account, enableLogs):
        if enableLogs: 
            print('nonce: '+str(self.w3.eth.getTransactionCount(account)))
        txData = {'from':account, 'nonce':self.w3.eth.getTransactionCount(account),'gas':constants.STANDARD_GAS}
        txData = self.contract.functions.uploadChunk(name, position, data).buildTransaction(txData)
        await self.Helper.signAndSendTransaction(self.w3, privateKey, txData)

    #Python wrapper for solidity function deleteFile.Deletes file from SKALE chain node
    #original js
    #async deleteFile(address, name, privateKey = '') {
    #   let txData = this.contract.methods.deleteFile(name);
    #   return await Helper.sendTransactionToContract(this.web3, address, privateKey, txData, constants.STANDARD_GAS);
    #}

    async def deleteFile(self, name, privateKey, account):
        txData = {'from':account, 'nonce':self.w3.eth.getTransactionCount(account),'gas':constants.STANDARD_GAS}
        txData = self.contract.functions.deleteFile(name).buildTransaction(txData)
        await self.Helper.signAndSendTransaction(self.w3, privateKey, txData)

    #Python wrapper for solidity function finishUpload.Finishes uploading of the file.Checks whether all chunks are uploaded correctly
    #original js
    #async finishUpload(address, name, privateKey = '') {
    #    let txData = this.contract.methods.finishUpload(name);
    #return await Helper.sendTransactionToContract(this.web3, address, privateKey, txData, constants.STANDARD_GAS);
    #}

    async def finishUpload(self, name, privateKey, account):
        txData = {'from':account, 'nonce':self.w3.eth.getTransactionCount(account),'gas':constants.STANDARD_GAS}
        txData = self.contract.functions.finishUpload(name).buildTransaction(txData)
        await self.Helper.signAndSendTransaction(self.w3, privateKey, txData)

    #Python wrapper for solidity function readChunk.Reads chunk from file from specific position
    #original js
    #async readChunk(storagePath, position, length) {
    #   let result = await this.contract.methods.readChunk(storagePath, position, length).call();
    #return result;
    #}

    def readChunk(self, storagePath, position, length):
        return self.contract.functions.readChunk(storagePath, position, length).call()

    #Python wrapper for solidity function getFileStatus.Returns status of the file:
    #0 - file does not exist,
    #1 - file is created but uploading not finished yet,
    #2 - file is fully uploaded to Filestorage
    # original js
    #async getFileStatus(storagePath){
    #   let result = await this.contract.methods.getFileStatus(storagePath).call();
    #return result;
    #}

    def getFileStatus(self, storagePath):
        return self.contract.functions.getFileStatus(storagePath).call()

    #Python wrapper for for solidity function getFileSize.Get size of the file in bytes
    #original js
    #async getFileSize(storagePath) {
    #   let result = await this.contract.methods.getFileSize(storagePath).call();
    #return result;
    #}

    async def getFileSize(self, storagePath):
        return self.contract.functions.getFileSize(storagePath).call()

    #Python wrapper for solidity function getFileInfoList.Get information about files in Filestorage of the
    #original js
    #async getFileInfoList(address){
    #   let result = await this.contract.methods.getFileInfoList(address).call();
    #return result;
    #}

    async def getFileInfoList(self, address):
        return self.contract.functions.getFileInfoList(address).call()
