


from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)

from homeassistant.const import (
    UnitOfEnergy, 
    UnitOfPower, 
    UnitOfApparentPower,
    POWER_VOLT_AMPERE_REACTIVE,
    UnitOfTemperature, 
    UnitOfElectricCurrent, 
    UnitOfElectricPotential, 
    UnitOfTime, 
    UnitOfFrequency
)


#https://www.gavazziautomation.com/docs/pim/MANUALS/ENG/WM40_IM_ENG.pdf
#https://www.gavazzi.no/wp-content/uploads/WM20-WM30-WM40-COM.pdf

GAVAZZI_IP = "192.168.1.110"
REQUEST_DELAY = 0.002 #Seconds
TIMEOUT = 1 #Seconds

'''
modbus:
  - name: GAVAZZI-WM40-96
    type: tcp
    host: 192.168.1.110
    port: 502
    delay: 2
    message_wait_milliseconds: 2
    timeout: 1
    sensors:
      - name: V-L1-N
        device_class: voltage
        unit_of_measurement: V
        precision: 1
        input_type: holding
        address: 80
        data_type: float32
        swap: word
        
      - name: A-L1
        device_class: current
        unit_of_measurement: A
        precision: 1
        input_type: holding
        address: 96
        data_type: float32
        swap: word
        
      - name: W-L1
        device_class: power
        unit_of_measurement: W
        precision: 1
        input_type: holding
        address: 104
        data_type: float32
        swap: word
        
      - name: VA-L1
        device_class: apparent_power
        unit_of_measurement: VA
        precision: 1
        input_type: holding
        address: 112
        data_type: float32
        swap: word

      - name: VAR-L1
        device_class: reactive_power
        unit_of_measurement: var
        precision: 1
        input_type: holding
        address: 120
        data_type: float32
        swap: word
        
      - name: cosphi-L1
        device_class: power_factor
        precision: 1
        input_type: holding
        address: 128
        data_type: float32
        swap: word
'''


#    name,                                    Address,  decoder,      DeviceClass,                       unit,                              stateclass
DATA_TABLE = (
    ("Voltage L1-N",                            80,     float,        SensorDeviceClass.VOLTAGE,         UnitOfElectricPotential.VOLT,      SensorStateClass.MEASUREMENT),
    ("Current L1",                              96,     float,        SensorDeviceClass.CURRENT,         UnitOfElectricCurrent.AMPERE,      SensorStateClass.MEASUREMENT),
    ("Power L1",                                104,    float,        SensorDeviceClass.POWER,           UnitOfPower.WATT,                  SensorStateClass.MEASUREMENT),
    ("Apparent Power L1",                       112,    float,        SensorDeviceClass.APPARENT_POWER,  UnitOfApparentPower.VOLT_AMPERE,   SensorStateClass.MEASUREMENT),
    ("Reactive Power L1",                       120,    float,        SensorDeviceClass.REACTIVE_POWER,  POWER_VOLT_AMPERE_REACTIVE,        SensorStateClass.MEASUREMENT),
    ("Power Factor cosphi L1",                  128,    float,        SensorDeviceClass.POWER_FACTOR,    None,                              SensorStateClass.MEASUREMENT),
)

DOMAIN = "gavazzi_meter"

