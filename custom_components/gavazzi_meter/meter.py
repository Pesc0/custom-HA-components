from pymodbus.client import AsyncModbusTcpClient
from pymodbus import ExceptionResponse

from .const import *

import asyncio
import struct


def size_of_data_type(data_type):
    if data_type == float:
        return 2
    else:
        raise Exception(f"Data type {data_type} not implemented")


def decoder(data, data_type):
    if data_type == float:
        byte_string = b"".join([x.to_bytes(2, byteorder="little") for x in data])
        value = struct.unpack("f", byte_string)[0]
        return round(value, 2)
    else:
        raise Exception(f"Decoder for data type {data_type} not implemented")


async def get_data():
    client = AsyncModbusTcpClient(GAVAZZI_IP, timeout=TIMEOUT)
    if not await client.connect():
        raise Exception(f"Could not connect")
    
    output = list()
    for i, [name, address, data_type, deviceclass, units, stateclass] in enumerate(DATA_TABLE):
        await asyncio.sleep(REQUEST_DELAY)
        resp = await client.read_holding_registers(address, size_of_data_type(data_type))
        if resp.isError() or resp == None or isinstance(resp, ExceptionResponse):
            raise Exception()

        output.append(decoder(resp.registers, data_type))

    client.close()

    return output




