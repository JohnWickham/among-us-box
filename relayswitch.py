# -*- coding: UTF-8 -*-
import subprocess
import RPi.GPIO as GPIO
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_OUTLET

class RelaySwitch(Accessory):
  
  category = CATEGORY_OUTLET

  def __init__(self, pin_number, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.pin_number = pin_number
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.OUT)

    serv_switch = self.add_preload_service('Outlet')
    self.relay_on = serv_switch.configure_char('On', setter_callback=self.set_relay)

  @Accessory.run_at_interval(1)
  def run(self):
    state = GPIO.input(self.pin_number)

    if self.relay_on.value != state:
      self.relay_on.value = not state
      self.relay_on.notify()

    oldstate = 0

    if state != oldstate:
      oldstate == state

  def set_relay(self, state):
    print("Setting relay state to: ", state)
    # The relay is wired in active-low state
    if state:
      GPIO.output(self.pin_number, 1)
    else:
      GPIO.output(self.pin_number, 0)