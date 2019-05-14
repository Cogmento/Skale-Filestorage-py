import asyncio
from index import FilestorageClient

#get testconfig
import json 
with open('testconfig.json') as json_file:
    testconfigJson = json.load(json_file)
provider = testconfigJSON.HTTPprovider
privateKey = testconfigJSON.PrivateKey
path = testconfigJSON.Path
name = testconfigJSON.FileName


#attempt to upload
loop = asyncio.get_event_loop()
c = FilestorageClient(provider, privateKey, True)
print('xxxxxxxxxxxxxxx class initiated xxxxxxxxxxxxxxxxxxxx')
loop.run_until_complete(c.uploadFile(path, name))
loop.close()
print('xxxxxxxxxxxxxxx file uploaded xxxxxxxxxxxxxxxxxxxxxx')