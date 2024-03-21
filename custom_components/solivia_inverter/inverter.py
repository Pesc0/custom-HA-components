
import struct
import serial

from . import crc16
from .const import *


def get_data():
    conn =  serial.Serial(SERIAL_DEVICE, BAUD_RATE, timeout=0.5)
    
    # Clear buffers to start clean comm
    conn.reset_input_buffer()
    conn.reset_output_buffer()

    conn.write(REQ_DATA_PACKET)
    conn.flush()
    
    packet = conn.read(RESP_PACKET_SIZE)
    
    conn.close()

    if len(packet) == 0:
        raise Exception(f"Did not recieve any reply from inverter.")

    if len(packet) != RESP_PACKET_SIZE:
        raise Exception(f"Recieved packet is not {RESP_PACKET_SIZE} bytes")

    stx, req, addr, size, cmd, cmdsub, data, lsb, msb, etx = struct.unpack(f'>BBBBBB{RESP_DATA_SIZE}sBBB', packet)

    if (stx != STX
                or req != ACK
                or addr != INVERTER_ADDR
                or size != RESP_DATA_SIZE + 2 # cmd | subcmd | msg
                or cmd != REQ_DATA_CMD
                or cmdsub != REQ_DATA_SUBCMD
                or len(data) != RESP_DATA_SIZE
                or crc16.calcData(packet[1:-3]) != (msb << 8 | lsb) # CRC of preceding bytes excluding STX
                or etx != ETX):
        raise Exception(f"Recieved packet does not pass integrity checks")

    values = struct.unpack(DATA_STRUCT, data)

    output = list()
    for i, [name, size, decoder, exponent, deviceclass, units, stateclass] in enumerate(DATA_TABLE):
        value = decoder(values[i])
        if decoder in [int, float]: value = value * pow(10, exponent) 
        output.append(value)

    return output
