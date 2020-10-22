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

bridge = Bridge(display_name="Among Us Box")
bridge.add_accessory(RelaySwitch(4, driver, 'PrimaryRelaySwitch'))

driver = AccessoryDriver(bridge, port=51826)

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()