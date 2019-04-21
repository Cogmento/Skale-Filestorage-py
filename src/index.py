import asyncio
from web3 import Web3
import os.path
import common.constants as constants
from common.Helper import Helper
from FilestorageContract import FilestorageContract


#I don't understand why we are doing this yet:
#let streamSaver = null;
#if (typeof window !== 'undefined') {
#    streamSaver = require('streamsaver');
#}


class FilestorageClient:
    def __init__(self, web3Provider, enableLogs = False):
        self.web3 = Web3.__init__(web3Provider)
        self.contract = FileStorageContract(self.web3)
        self.enableLogs = enableLogs

    async def uploadFile(self, address, fileName, fileBuffer, privateKey):
        fileSize = fileBuffer.length
        await self.contract.startUpload(address, fileName, fileSize, privateKey)
        if self.enableLogs:
            print('File was created!')
        ptrPosition = 0
        i = 0
        while ptrPosition < fileSize:
            ptrPositionright = ptrPosition + min(fileSize - ptrPosition, constants.CHUNK_LENGTH)
            rawChunk = fileBuffer[ptrPosition : ptrPositionright]
            chunk = Helper.bufferToHex(rawChunk)
            await self.contract.uploadChunk(address, fileName, ptrPosition, Helper.addBytesSymbol(chunk), privateKey)
            ptrPosition += len(chunk) / 2
            if self.enableLogs:
                print('Chunk ' + str(i) + ' was loaded ' + str(ptrPosition))
                i += 1
        if self.enableLogs:
            print('Checking file validity...')
        await self.contract.finishUpload(address, fileName, privateKey)
        if self.enableLogs:
            print('File was uploaded!')
        return os.path.join(Helper.rmBytesSymbol(address), fileName)

    async def downloadToFile(self, storagePath):
        print('incomplete')
        # this function won't work because the original js version aimed to
        # ove the file to the browser downloads folder

        #fileName = os.path.basename(storagePath) # includes file extension (ex. blah.py) - could be an issue later
        3wstream = open(fileName, 'w')
        #await self._downloadFile(storagePath, wstream);
        #wstream.close();

    async def downloadToBuffer(self,storagePath):
        print('incomplete')
        #return await self

    async def deleteFile(self, address, fileName, privateKey)
        await self.contract.deleteFile(address, fileName, privateKey)
        if self.enableLogs:
            print('File was deleted')

    async def getFileInfoListByAddress(self, address):
    #incomplete - have to find and test an example of the .map for python
        rawFiles = await self.contract.getFileInfoList(address)
        #files = rawFiles.map(file =
            #storagePath = path.join(Helper.rmBytesSymbol(address), file['name']);
            #chunkStatusList = file['isChunkUploaded'];
            #uploadedChunksCount = chunkStatusList.filter(x= > x == = true).length;
            #uploadingProgress = Math.floor(uploadedChunksCount / chunkStatusList.length * 100);
            return {
                'name': file['name'],
                'size': parseInt(file['size'], 10),
                'storagePath': storagePath,
                'uploadingProgress': uploadingProgress
            };
            });
    return files;

    async def _downloadFile(self, storagePath, stream):
        print('incomplete')
        #this method was used to download files from browser downloads folder to {
