import logging
import signal
import random

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
from pyhap import camera
from pyhap.const import CATEGORY_SENSOR
from RelaySwitch import RelaySwitch

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

def get_accessory(driver):
    """Call this method to get a standalone Accessory."""
    return RelaySwitch(17, driver, 'PrimaryRelaySwitch')

# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)

# Change `get_accessory` to `get_bridge` if you want to run a Bridge.
driver.add_accessory(accessory=get_accessory(driver))

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()