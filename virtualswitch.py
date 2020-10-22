# -*- coding: UTF-8 -*-
import subprocess
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SWITCH

class VirtualSwitch(Accessory):
  
  category = CATEGORY_SWITCH
  state = False
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    serv_switch = self.add_preload_service('Switch')
    self.switch_on = serv_switch.configure_char('On', setter_callback=self.set_state)

  def set_state(self, state):
    self.state = state
    self.switch_on.value = state
    self.switch_on.notify()