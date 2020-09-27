import subprocess
import os
import RPi.GPIO as GPIO
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_OUTLET

class RelaySwitch(Accessory):
  
  category = CATEGORY_OUTLET

  def __init__(self, pin_number, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    print("Relay on pin ", pin_number)

    self.pin_number = pin_number
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.OUT)

    serv_switch = self.add_preload_service('Outlet')
    self.relay_on = serv_switch.configure_char('On', setter_callback=self.set_relay)
    self.relay_in_use = serv_switch.configure_char('OutletInUse', setter_callback=self.get_relay_in_use)

  @Accessory.run_at_interval(1)
  def run(self):
    state = GPIO.input(self.pin_number)

    if self.relay_on.value != state:
      self.relay_on.value = state
      self.relay_on.notify()
      self.relay_in_use.notify()

    oldstate = 1

    if state != oldstate:
      oldstate == state

  def set_relay(self, state):
    if GPIO.input(self.pin_number) != state:
      if state:
        GPIO.output(self.pin_number, 1)
      else:
        GPIO.output(self.pin_number, 0)

  def get_relay_in_use(self, state):
      return True
  
  # Shutdown Switch
  # Edit /etc/sudoers and add the line "orange ALL=NOPASSWD: /sbin/shutdown"

  # os.system("sudo shutdown -h now")