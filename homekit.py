# -*- coding: UTF-8 -*-
import logging
import signal
import random

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
from pyhap import camera
from pyhap.const import CATEGORY_SENSOR
from relayswitch import RelaySwitch

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)
driver.add_accessory(RelaySwitch(4, driver, 'PrimaryRelaySwitch'))

bridge = Bridge(driver=driver, display_name="Among Us Box")

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()