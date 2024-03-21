
# https://github.com/lvzon/soliviamonitor/
# https://github.com/bbinet/delta-rpi

import binascii
import struct

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)

from homeassistant.const import (
    UnitOfEnergy, 
    UnitOfPower, 
    UnitOfTemperature, 
    UnitOfElectricCurrent, 
    UnitOfElectricPotential, 
    UnitOfTime, 
    UnitOfFrequency
)

# 1     byte    STX     0x02    Start of message
# 1     byte    ENQ             Enquiry type (0x05 for requests, 0x06 for responses)
# 1     byte                    Inverter ID
# 1     byte    LEN             Number of bytes to follow, excluding CRC and ETX
# 2     bytes   CMD             command and subcommand e.g. 0x10 0x02 to request the current DC voltage, 0x10 0x02>
# LEN-2 bytes                   data bytes
# 2     bytes   CRC             CRC-16, over preceding bytes excluding STX, LSB first (little-endian)
# 1     byte    ETX     0x03    End of message

STX=0x02
ENQ=0x05
ETX=0x03

ACK=0x06
NAK=0x15

# Send command 0x60 0x01 to inverter addr 1
REQ_DATA_CMD = 0x60
REQ_DATA_SUBCMD = 0x01
INVERTER_ADDR = 1
REQ_DATA_PACKET = bytes.fromhex("02050102600185fc03")

SERIAL_DEVICE = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"
BAUD_RATE = 19200

#print major, minor
def ma_mi(data):
    ma, mi = struct.unpack('>BB', data)
    return '{:02d}.{:02d}'.format(ma, mi)

#print major, minor, bugfixing
def ma_mi_bf(data):
    ma, mi, bf = struct.unpack('>BBB', data)
    return '{:02d}.{:02d}.{:02d}'.format(ma, mi, bf)

#    name,                                      bytes,  decoder,          *(10^x),      DeviceClass,                       unit,                     stateclass
DATA_TABLE = (
    ("SAP part number",                         "11s",  str,                    0,      None,                              None,                           None),
    ("SAP serial number",                       "18s",  str,                    0,      None,                              None,                           None),
    ("SAP date code",                           "4s",   binascii.hexlify,       0,      None,                              None,                           None),
    ("SAP revision",                            "2s",   binascii.hexlify,       0,      None,                              None,                           None),
    ("AC control FW rev",                       "3s",   ma_mi_bf,               0,      None,                              None,                           None),
    ("DC control FW rev",                       "3s",   ma_mi_bf,               0,      None,                              None,                           None),
    ("Display FW rev",                          "3s",   ma_mi_bf,               0,      None,                              None,                           None),
    ("SC control FW rev",                       "3s",   ma_mi_bf,               0,      None,                              None,                           None),
    ("Solar Voltage at Input 1",                "H",    float,                  0,      SensorDeviceClass.VOLTAGE,         UnitOfElectricPotential.VOLT,   SensorStateClass.MEASUREMENT),
    ("Solar Current at Input 1",                "H",    float,                  -1,     SensorDeviceClass.CURRENT,         UnitOfElectricCurrent.AMPERE,   SensorStateClass.MEASUREMENT),
    ("Solar Isolation Resistance at Input 1",   "H",    float,                  0,      "kOhm",                            "kOhm",                         SensorStateClass.MEASUREMENT),
    ("Calculated temperature at ntc (DC side)", "h",    int,                    0,      SensorDeviceClass.TEMPERATURE,     UnitOfTemperature.CELSIUS,      SensorStateClass.MEASUREMENT),
    ("Solar inout MOV resistance",              "H",    float,                  0,      "kOhm",                            "kOhm",                         SensorStateClass.MEASUREMENT),
    ("AC Current",                              "H",    float,                  -1,     SensorDeviceClass.CURRENT,         UnitOfElectricCurrent.AMPERE,   SensorStateClass.MEASUREMENT),
    ("AC Voltage",                              "H",    float,                  0,      SensorDeviceClass.VOLTAGE,         UnitOfElectricPotential.VOLT,   SensorStateClass.MEASUREMENT),
    ("AC Power",                                "H",    int,                    0,      SensorDeviceClass.POWER,           UnitOfPower.WATT,               SensorStateClass.MEASUREMENT),
    ("AC Frequency",                            "H",    float,                  -2,     SensorDeviceClass.FREQUENCY,       UnitOfFrequency.HERTZ,          SensorStateClass.MEASUREMENT),
    ("Calculated temperature at ntc (AC side)", "h",    int,                    0,      SensorDeviceClass.TEMPERATURE,     UnitOfTemperature.CELSIUS,      SensorStateClass.MEASUREMENT),
    ("SC Grid Voltage",                         "H",    float,                  -2,     SensorDeviceClass.VOLTAGE,         UnitOfElectricPotential.VOLT,   SensorStateClass.MEASUREMENT),
    ("SC Grid ens Frequency",                   "H",    float,                  -2,     SensorDeviceClass.FREQUENCY,       UnitOfFrequency.HERTZ,          SensorStateClass.MEASUREMENT),
    ("SC Grid DC injection Current",            "H",    float,                  -2,     SensorDeviceClass.CURRENT,         UnitOfElectricCurrent.AMPERE,   SensorStateClass.MEASUREMENT),
    ("AC Grid Voltage",                         "H",    float,                  -2,     SensorDeviceClass.VOLTAGE,         UnitOfElectricPotential.VOLT,   SensorStateClass.MEASUREMENT),
    ("AC Grid Frequency",                       "H",    float,                  -2,     SensorDeviceClass.FREQUENCY,       UnitOfFrequency.HERTZ,          SensorStateClass.MEASUREMENT),
    ("AC Grid DC injection Current",            "H",    float,                  -2,     SensorDeviceClass.CURRENT,         UnitOfElectricCurrent.AMPERE,   SensorStateClass.MEASUREMENT),
    ("Day supplied AC energy",                  "H",    int,                    1,      SensorDeviceClass.ENERGY,          UnitOfEnergy.WATT_HOUR,         SensorStateClass.TOTAL_INCREASING),
    ("Inverter runtime today",                  "H",    int,                    0,      SensorDeviceClass.DURATION,        UnitOfTime.MINUTES,             SensorStateClass.TOTAL_INCREASING),
    ("Max AC Current today",                    "H",    float,                  -1,     SensorDeviceClass.CURRENT,         UnitOfElectricCurrent.AMPERE,   SensorStateClass.MEASUREMENT),
    ("Min AC Voltage today",                    "H",    float,                  0,      SensorDeviceClass.VOLTAGE,         UnitOfElectricPotential.VOLT,   SensorStateClass.MEASUREMENT),
    ("Max AC Voltage today",                    "H",    float,                  0,      SensorDeviceClass.VOLTAGE,         UnitOfElectricPotential.VOLT,   SensorStateClass.MEASUREMENT),
    ("Max AC Power today",                      "H",    int,                    0,      SensorDeviceClass.POWER,           UnitOfPower.WATT,               SensorStateClass.MEASUREMENT),
    ("Min AC Frequency today",                  "H",    float,                  -2,     SensorDeviceClass.FREQUENCY,       UnitOfFrequency.HERTZ,          SensorStateClass.MEASUREMENT),
    ("Max AC Frequency today",                  "H",    float,                  -2,     SensorDeviceClass.FREQUENCY,       UnitOfFrequency.HERTZ,          SensorStateClass.MEASUREMENT),
    ("Supplied AC energy",                      "I",    int,                    -1,     SensorDeviceClass.ENERGY,          UnitOfEnergy.KILO_WATT_HOUR,    SensorStateClass.TOTAL),
    ("Inverter runtime",                        "I",    int,                    0,      SensorDeviceClass.DURATION,        UnitOfTime.HOURS,               SensorStateClass.TOTAL),
    ("Max Solar 1 input current",               "H",    float,                  -1,     SensorDeviceClass.CURRENT,         UnitOfElectricCurrent.AMPERE,   SensorStateClass.MEASUREMENT),
    ("Max solar 1 input voltage",               "H",    float,                  0,      SensorDeviceClass.VOLTAGE,         UnitOfElectricPotential.VOLT,   SensorStateClass.MEASUREMENT),
    ("Max solar 1 input power",                 "H",    int,                    0,      SensorDeviceClass.POWER,           UnitOfPower.WATT,               SensorStateClass.MEASUREMENT),
    ("Min isolation resistance solar 1",        "H",    float,                  0,      "kOhm",                            "kOhm",                         SensorStateClass.MEASUREMENT),
    ("Max isolation resistance solar 1",        "H",    float,                  0,      "kOhm",                            "kOhm",                         SensorStateClass.MEASUREMENT),
    ("Alarm status",                            "B",    int,                    0,      None,                              None,                           None),
    ("Status DC input",                         "B",    int,                    0,      None,                              None,                           None),
    ("Limits DC input",                         "B",    int,                    0,      None,                              None,                           None),
    ("Status AC output",                        "B",    int,                    0,      None,                              None,                           None),
    ("Limits AC output",                        "B",    int,                    0,      None,                              None,                           None),
    ("Warnings status",                         "B",    int,                    0,      None,                              None,                           None),
    ("DC hardware failure",                     "B",    int,                    0,      None,                              None,                           None),
    ("AC hardware failure",                     "B",    int,                    0,      None,                              None,                           None),
    ("SC hardware failure",                     "B",    int,                    0,      None,                              None,                           None),
    ("internal bulk failure",                   "B",    int,                    0,      None,                              None,                           None),
    ("internal communication failure",          "B",    int,                    0,      None,                              None,                           None),
    ("AC hardware disturbance",                 "B",    int,                    0,      None,                              None,                           None),
    ("DC HW stage error",                       "B",    int,                    0,      None,                              None,                           None),
    ("Calibration status",                      "B",    int,                    0,      None,                              None,                           None),
    ("Neutral error",                           "B",    int,                    0,      None,                              None,                           None),
    ("History status messages",                 "20s",  binascii.hexlify,       0,      None,                              None,                           None),
)
DATA_STRUCT = '>' + ''.join([item[1] for item in DATA_TABLE])

RESP_PACKET_SIZE = 157
RESP_DATA_SIZE = RESP_PACKET_SIZE - 9 # stx req addr size cmd subcmd lsb msb etx

DOMAIN = "solivia_inverter"

