
from abstract_client import AbstractInteractionClient
from aiohttp import TCPConnector
import asyncio
from marshmallow import Schema, fields


class DataSchema(Schema):
    PublicId = fields.Str()
    Amount = fields.Int()
    Currency = fields.Str()
    Description = fields.Str()
    CardCryptogramPacket = fields.Str()


class ClientCloudpayments(AbstractInteractionClient):
    def __init__(self, publicId, cardCryptogramPacket) -> None:
        self.CONNECTOR = TCPConnector()
        self.SERVICE='Cloudpayments'
        self.BASE_URL="https://api.cloudpayments.ru/"
        self.REQUEST_TIMEOUT = 5
        self.CONNECT_TIMEOUT = 5
        self.publicId = publicId
        self.cardCryptogramPacket = cardCryptogramPacket
        super().__init__()
    
    async def _create_dict_data(self, amount:int, currency:str, description:str) -> dict:
        data_dict = dict(
            PublicId=self.publicId,
            Amount=amount,
            Currency=currency, 
            Description=description, 
            CardCryptogramPacket=self.cardCryptogramPacket
        )
        return data_dict

    async def _create_json_data(self, data_dict:dict) :
        schema =DataSchema()
        json_data = schema.dump(data_dict)
        return json_data

    async def charge(self, amount:int, currency:str, description:str) -> dict:
        url = self.endpoint_url(relative_url= "payments/cards/charge")
        data_dict = await self._create_dict_data(amount, currency, description)
        data_json = await self._create_json_data(data_dict)
        result = await self.post('post', url, data=data_json)
        print(result) 
        await self.close()
        return result



if __name__=="__main__":
    
    publicId='cardCryptogramPacket='
    cardCryptogramPacket="\"{\\\"type\\\":\\\"Yandex\\\",\\\"signedMessage\\\":\\\"{\\\\\\\"encryptedMessage\\\\\\\":\\\\\\\"xqpAiS2L71BZNgH514AQDwOVawJF4gHXF8P+ECIFRqFHlDMRtxHsO9hNQSeegSssRdDMlBIyOObY5dqI3iwX99UKYP6qFD+tKEYJQkUdiKyhZCwgUsVdHBlFQA+iiXVLf7DZ5WCIaHjpl4mckrGeDg4XGDIX4FB0BorLqocbDLcl0JZi2zzkNtn9FDLPSAs1qbTEMdb3TAS0iDAIkuAy5DGJ3+4Av9PWvIllW4LRdQ34rR8MPszJxq9Xagw/jeKUglyUERQgi5cnVWIB992yPh9UFgNuCQBc+JWLMzuOIKKxFiVK6VBSsuHpDWrSZqMolN6PIeNvETxQ34g+O/u4KiwWd3IG/pb5e0FYbzn/gWzlDSPsqNSuB713qZDHCI7eFB7h7iPTdk/Wd78Vv7Vlg4oVQdMWCbgSjtWDamKeq/OMiVDW5j36CebRQWxB8/XFj4nAInHIjoUUKsEQ5gf00n9/48RUNVCbRr6qykvsfnD0XP5V4OJOeIhAZN2CAgGxgrGC5MibfjAf+D/EnunHwOvtmI6KQAsGv9QgrRC8sxTeyk7OT9vUCzK2DIRDYyCtvloGalRq1PRdJWQX\\\\\\\",\\\\\\\"tag\\\\\\\":\\\\\\\"LTx6/HA9iWaZwbYaFN1j9aDOPp2PBlR2iBMUBQ7zyUg=\\\\\\\",\\\\\\\"ephemeralPublicKey\\\\\\\":\\\\\\\"BHHBcT4SvFgxMK14Oz3/dk/uiCL2m4jeTFDEcoYHXt5gAz2wFVEnvRD4fHArkbIOcry9nlUYHWgT4GicEl9qkXY=\\\\\\\"}\\\",\\\"protocolVersion\\\":\\\"ECv2\\\",\\\"signature\\\":\\\"MEUCICyyzWnCEf2iHlUszDzvbAx/qk/sLmbTaOWPVEq1hr29AiEA0lfZ85pCofYhxVX971Xtshysawi7+KEe8ZpPVlV/Md4=\\\",\\\"intermediateSigningKey\\\":{\\\"signedKey\\\":\\\"{\\\\\\\"keyValue\\\\\\\":\\\\\\\"MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEqYNePt6BPgCv5JxfO9dF2vrSqmnp4Mhe/vF+XO+Devbs6/KVpVVoTD8LLcAo4TZh6IuODVnVpHrTObhg3HJVJA==\\\\\\\",\\\\\\\"keyExpiration\\\\\\\":\\\\\\\"1764950892000\\\\\\\"}\\\",\\\"signatures\\\":[\\\"MEQCIDRslMW7wNZbpqVw/dD7hDQh30hGhqfjfWTBvc7zAYJSAiAGAvjAslA2AxwdAEuOfacFr6DaE5yiiUuUtM6DUreZYg==\\\"]}}\""

    client1 = ClientCloudpayments(publicId, cardCryptogramPacket)

    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(client1.charge(100, "RUB", "A basket of oranges")) # передайте точку входа
    finally:
        pass

    