import asyncio
from web3 import Web3
import os.path
import common.constants as constants
from FilestorageContract import FilestorageContract

import time



class FilestorageClient:
    
    def __init__(self, web3Provider, privateKey, enableLogs):
        #currently configured only for HTTPProviders
        self.w3 = Web3(Web3.HTTPProvider(web3Provider))
        self.contract = FilestorageContract(self.w3)
        self.enableLogs = enableLogs
        self.account = self.w3.eth.account.privateKeyToAccount(privateKey)._address
        self.privateKey = privateKey

    async def test(self):
        time.sleep(5)


    async def uploadFile(self, path, fileName):
        fileBuffer = open(path, 'rb')
        fileSize = fileBuffer.__sizeof__()
        await self.contract.startUpload(fileName, fileSize, self.privateKey, self.account, self.enableLogs)
        if self.enableLogs:
            print('File was created!')
        await self.test()
        await self.test()
        await self.test()
        ptrPosition = 0
        i = 0
        while ptrPosition < fileSize:
            ptrPositionright = ptrPosition + min(fileSize - ptrPosition, constants.CHUNK_LENGTH)
            with open(path,'rb') as fileBuffer:
                rawChunk = fileBuffer.read()[ptrPosition : ptrPositionright]
            chunk = self.contract.Helper.bufferToHex(rawChunk)
            await self.contract.uploadChunk(fileName, ptrPosition, self.contract.Helper.addBytesSymbol(chunk), self.privateKey, self.account, self.enableLogs)
            ptrPosition += len(chunk) / 2
            if self.enableLogs:
                print('Chunk ' + str(i) + ' was loaded ' + str(ptrPosition))
                i += 1
        if self.enableLogs:
            print('Checking file validity...')
        await self.test()
        await self.test()
        await self.test()
        await self.contract.finishUpload(fileName, self.privateKey, self.account)
        if self.enableLogs:
            print('File was uploaded!')

    async def downloadToFile(self, storagePath):
        print('incomplete')
        # this function won't work because the original js version aimed to
        # ove the file to the browser downloads folder

        #fileName = os.path.basename(storagePath) # includes file extension (ex. blah.py) - could be an issue later
        #3wstream = open(fileName, 'w')
        #await self._downloadFile(storagePath, wstream);
        #wstream.close();

    async def downloadToBuffer(self,storagePath):
        print('incomplete')
        #return await self

    async def deleteFile(self, fileName):
        print('incomplete')
        if self.enableLogs:
            print('File was deleted')

    async def getFileInfoListByAddress(self):
        print('incomplete') 
        rawFiles = await self.contract.getFileInfoList(self.account)
        #files = rawFiles.map(file =
            #storagePath = path.join(Helper.rmBytesSymbol(address), file['name']);
            #chunkStatusList = file['isChunkUploaded'];
            #uploadedChunksCount = chunkStatusList.filter(x= > x == = true).length;
            #uploadingProgress = Math.floor(uploadedChunksCount / chunkStatusList.length * 100);




