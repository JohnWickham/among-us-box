# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import random
from time import sleep
from sounds import SoundPlayer, SoundEffect
from drawing import DisplayDrawer
import os
from homekit import HomeKitManager

GPIO.setmode(GPIO.BCM)

# Define input and output pins
trigger_button_input = 26
relay_output = 4
switch_inputs = [24, 23, 22, 27, 17] # ROYGB order
led_outputs = [16, 13, 12, 6, 5]
starting_switch_states = []
current_switch_states = []
changed_switch_inputs = []

GPIO.setup(trigger_button_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(relay_output, GPIO.OUT)
GPIO.setup(switch_inputs, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_outputs, GPIO.OUT)

running = True

display = DisplayDrawer()

sound_player = SoundPlayer()
sound_player.play_sound(SoundEffect.GAME_START)

homekit_manager = HomeKitManager()

is_trigger_button_latched = False

is_sabotaged = False
next_scheduled_sabotage_date = None

def schedule_next_sabotage():
  global next_scheduled_sabotage_date
  
  min_offset = 5 * 60 # 5 minutes
  max_offset = 12 * 60 * 60 # 12 hours
  random_seconds = random.randint(min_offset, max_offset)
  now = datetime.now()
  next_scheduled_sabotage_date = now + timedelta(seconds=random_seconds)
  print("Next sabotage scheduled for: ", next_scheduled_sabotage_date.ctime())

schedule_next_sabotage()

def begin_sabotage():
  global is_sabotaged
  
  if is_sabotaged:
    return
    
  for (index, input_pin) in enumerate(switch_inputs):
    state = GPIO.input(input_pin)
    starting_switch_states.append(state)
    current_switch_states.append(state)
      
  is_sabotaged = True
  GPIO.output(relay_output, GPIO.HIGH)
  GPIO.output(led_outputs, GPIO.LOW)
  
  homekit_manager.switch_accessory.set_state(True)# Turn the HomeKit virtual switch accessory on
  
  sound_player.play_sound(SoundEffect.ALARM, True)
  
def finish_sabotage():
  global is_sabotaged
  
  is_sabotaged = False
  GPIO.output(relay_output, GPIO.LOW) # TODO: Set the relay to whatever state it was when sabotage began
  starting_switch_states.clear()
  changed_switch_inputs.clear()
  current_switch_states.clear()
  
  homekit_manager.switch_accessory.set_state(False)# Turn the HomeKit virtual switch accessory off
  
  sound_player.stop()
  sound_player.play_sound(SoundEffect.TASK_DONE)
  
  schedule_next_sabotage()
  
def process_sabotage():
  
  if is_sabotaged == False:
    return
    
  # FIXME: When sabotage starts, the switches will be randomly on and off, not all off. You have to treat each switch’s "on" state as being opposite as its state when sabotage starts, not just GPIO.HIGH.  

  for (index, pin_number) in enumerate(switch_inputs):
    
    switch_state = GPIO.input(pin_number)
    matching_led_state = GPIO.input(led_outputs[index])
    
    if switch_state != current_switch_states[index]:
      print(f'Switch {index} was changed')
      
      # Switch has changed state! Randomly decide whether to switch a *different* one back here.
      should_undo_other = (random.randint(0, 4) > 0)
      if should_undo_other and changed_switch_inputs:
        
        index_to_undo = random.choice(changed_switch_inputs)
        print(f'     Undoing {index_to_undo}')
        
        current_state = GPIO.input(switch_inputs[index_to_undo])
        new_state = GPIO.LOW if current_state == GPIO.HIGH else GPIO.HIGH
        changed_switch_inputs.remove(index_to_undo)
        
        GPIO.output(led_outputs[index_to_undo], new_state)
        
      changed_switch_inputs.append(index)
      GPIO.output(led_outputs[index], GPIO.HIGH if matching_led_state == GPIO.LOW else GPIO.LOW)
      
    current_switch_states[index] = switch_state
  
  all_states_high = True
  for output in led_outputs:
    led_state = GPIO.input(output)
    if led_state == GPIO.LOW:
      all_states_high = False
      break
      
  if all_states_high:
    print("All lights are on; ending sabotage…")
    finish_sabotage()

while running:
  
  if GPIO.input(trigger_button_input) == GPIO.LOW and is_trigger_button_latched == False:
    print("Trigger button pressed")
    is_trigger_button_latched = True
    if is_sabotaged:
      finish_sabotage()
    else:
      begin_sabotage()
      continue
  elif GPIO.input(trigger_button_input) == GPIO.HIGH:
    is_trigger_button_latched = False
    
  # Start a sabotage if the HomeKit switch was switched remotely
  if homekit_manager.switch_accessory.state != is_sabotaged:
    if homekit_manager.switch_accessory.state:
      begin_sabotage()
    else:
      finish_sabotage()
    
  display.update(is_sabotaged)
  
  if next_scheduled_sabotage_date.ctime() == datetime.now().ctime(): # Comparing the actual datetimes doesn't work for some reason.
    print("Sabotage is scheduled to begin now!")
    begin_sabotage()
    
  if is_sabotaged:
    process_sabotage()
    
  sleep(0.001) # 1ms should be sufficiently fast to loop