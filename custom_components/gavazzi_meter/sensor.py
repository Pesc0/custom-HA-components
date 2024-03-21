

from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from . import meter
from .const import DATA_TABLE, DOMAIN

import logging
_LOGGER = logging.getLogger(__name__)


# With the assumptions that 
#   - these are the only illegal chars found in the DATA_TABLE
#   - there are no duplicate entries in DATA_TABLE
def sanitize_str(string):
    return string.replace(" ", "_").replace("(", "").replace(")", "").lower()


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = MyCoordinator(hass)
    coordinator.last_update_success = False
        
    async_add_entities(
        MyEntity(coordinator, idx) for idx in range(len(DATA_TABLE))
    )


class MyCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(hass, _LOGGER, name="Gavazzi Meter", update_interval=timedelta(seconds=60))

    async def _async_update_data(self):
        try:
            return await meter.get_data()
        except Exception as err:
            raise UpdateFailed(err)


class MyEntity(CoordinatorEntity, SensorEntity):
    """
    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available
    """

    def __init__(self, coordinator, idx):
        super().__init__(coordinator, context=idx) #Pass coordinator to CoordinatorEntity
        
        self.idx = idx
        self._attr_has_entity_name = True
        self._attr_name                         = DATA_TABLE[idx][0]
        self._attr_device_class                 = DATA_TABLE[idx][3]
        self._attr_native_unit_of_measurement   = DATA_TABLE[idx][4]
        self._attr_state_class                  = DATA_TABLE[idx][5]
        
        self._attr_unique_id = f"{DOMAIN}_{sanitize_str(self._attr_name)}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "My Awesome Gavazzi")},
            name="Gavazzi Meter",
            manufacturer="Gavazzi",
            model="WM40-96",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        if self.coordinator.data != None:
            self._attr_native_value = self.coordinator.data[self.idx]
            self.async_write_ha_state()




