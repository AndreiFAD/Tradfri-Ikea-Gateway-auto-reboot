#!/usr/bin/python
# -*- coding: cp1250 -*-
__author__ = 'Fekete Andr�s Demeter'

import asyncio, uuid, json
from aiocoap import Message, Context
from aiocoap.numbers.codes import Code
from aiocoap.transports import tinydtls

class PatchedDTLSSecurityStore:
    def _get_psk(self, host, port):
        return PatchedDTLSSecurityStore.IDENTITY, PatchedDTLSSecurityStore.KEY

class Command(object):
    def __init__(self, path, data=None, *, process_result=None):
        self._path = path
        self._data = data
        self._process_result = process_result
        self._raw_result = None
        self._result = None

    @property
    def path(self):
        return self._path

    @property
    def data(self):
        return self._data

    @property
    def process_result(self):
        return self._process_result

    @property
    def raw_result(self):
        return self._raw_result

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        if self._process_result:
            self._result = self._process_result(value)
        self._raw_result = value

    def url(self, host):
        path = '/'.join(str(v) for v in self._path)
        return 'coaps://{}:5684/{}'.format(host, path)

class APIFactory:
    def __init__(self, host, psk_id='pytradfri', psk=None, loop=None):
        self._psk = psk
        self._host = host
        self._psk_id = psk_id
        self._loop = loop
        self._observations_err_callbacks = []
        self._protocol = None
        PatchedDTLSSecurityStore.IDENTITY = self._psk_id.encode('utf-8')
        if self._psk:
            PatchedDTLSSecurityStore.KEY = self._psk.encode('utf-8')

    async def _get_protocol(self):
        if self._protocol is None:
            self._protocol = asyncio.Task(Context.create_client_context(
                loop=self._loop))
        return (await self._protocol)

    async def _reset_protocol(self, exc=None):
        protocol = await self._get_protocol()
        await protocol.shutdown()
        self._protocol = None
        for ob_error in self._observations_err_callbacks:
            ob_error(exc)
        self._observations_err_callbacks.clear()

    async def _get_response(self, msg):
            protocol = await self._get_protocol()
            pr = protocol.request(msg)
            r = await pr.response
            return pr, r

    async def _execute(self, api_command):
        data = api_command.data
        url = api_command.url(self._host)
        kwargs = {}
        kwargs['payload'] = json.dumps(data).encode('utf-8')
        api_method = Code.POST
        msg = Message(code=api_method, uri=url, **kwargs)
        _, res = await self._get_response(msg)
        api_command.result = _process_output(res)
        return api_command.result

    async def request(self, api_commands):
        return await self._execute(api_commands)

    async def generate_psk(self, security_key):
            PatchedDTLSSecurityStore.IDENTITY = 'Client_identity'.encode('utf-8')
            PatchedDTLSSecurityStore.KEY = security_key.encode('utf-8')
            def process_result(result):
                return result[PSK]
            command = Command([GATEWAY, AUTH], {IDENTITY: self._psk_id}, process_result=process_result)
            self._psk = await self.request(command)
            PatchedDTLSSecurityStore.IDENTITY = self._psk_id.encode('utf-8')
            PatchedDTLSSecurityStore.KEY = self._psk.encode('utf-8')
            await self._reset_protocol()
            return self._psk

def _process_output(res):
    res_payload = res.payload.decode('utf-8')
    output = res_payload.strip()
    return json.loads(output)

async def run(host, key):
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host=host, psk_id=identity)
        psk = await api_factory.generate_psk(key)
        return 'coap-client -u '+identity+' -k '+psk+' -v 0 -m post "coaps://'+host+':5684/15011/9030"'

tinydtls.DTLSSecurityStore = PatchedDTLSSecurityStore
KEY = None
GATEWAY = "15011"
AUTH = "9063"
IDENTITY = "9090"
PSK = "9091"

# TODO: Change securityid and ip:
securityid = "Asd1Asd2Asd3Asd4" # Security Code - from Gateway (16 characters)
ip = "111.111.1.111"            # your device local ip

shutdown = asyncio.Future()
main = run(ip, securityid)
try:
    print("**********************************************************************************************************************************************************")
    print("**********************************************************************************************************************************************************")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------- HERE IS YOUR COMMAND --------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("\n\r----- HERE IS YOUR COMMAND: " + asyncio.get_event_loop().run_until_complete(main) + " -----\n\r")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("**********************************************************************************************************************************************************")
    print("**********************************************************************************************************************************************************")
except KeyboardInterrupt:
    shutdown.set_result(None)
    print("**********************************************************************************************************************************************************")
    print("**********************************************************************************************************************************************************")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("\n\r----- HERE IS YOUR COMMAND: " + asyncio.get_event_loop().run_until_complete(main) + " -----\n\r")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("**********************************************************************************************************************************************************")
    print("**********************************************************************************************************************************************************")


