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
from virtualswitch import VirtualSwitch

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)

bridge = Bridge(driver=driver, display_name="Among Us Box")
bridge.add_accessory(RelaySwitch(4, driver, 'PrimaryRelaySwitch'))
bridge.add_accessory(VirtualSwitch(driver, 'PrimaryVirtualSwitch'))

driver.add_accessory(accessory=bridge)

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()