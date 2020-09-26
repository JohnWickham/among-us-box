from pyhap.accessory import Accessory

class Sabotage_Trigger(Accessory):
  
  category = CATEGORY_SWITCH # This is for the icon in the iOS Home app.

  def __init__(self, *args, **kwargs):
    # If overriding this method, be sure to call the super's implementation first.
    super().__init__(*args, **kwargs)
  
    # Add the services that this Accessory will support with add_preload_service here
    switch_service = self.add_preload_service('Switch')
    self.char_on = serv_light.configure_char('On', value=self._state)
  
    serv_light.setter_callback = self._set_chars

  def _set_chars(self, char_values):
    if "On" in char_values:
      print('HomeKit is changing the value to: ', char_values["On"])

  # The `stop` method can be `async` as well
  def stop(self):
    # Do whatever you need to shut down and clean up.
    print('Stopping accessory.')