import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import random
from time import sleep
from sounds import SoundPlayer, SoundEffect
from drawing import DisplayDrawer
import os

GPIO.setmode(GPIO.BCM)

# Define input and output pins
trigger_button_input = 26
relay_output = 4
shutdown_input = 25
switch_inputs = [17, 27, 22, 23, 24]
led_outputs = [5, 6, 12, 13, 16]
starting_switch_states = [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW]
output_states = [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW]
changed_switch_inputs = []

GPIO.setup(trigger_button_input, GPIO.IN)
GPIO.setup(relay_output, GPIO.OUT)
GPIO.setup(shutdown_input, GPIO.IN)
GPIO.setup(switch_inputs, GPIO.IN)
GPIO.setup(led_outputs, GPIO.OUT)

running = True

display = DisplayDrawer()

sound_player = SoundPlayer()
sound_player.play_sound(SoundEffect.GAME_START)

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
    starting_switch_states[index] = GPIO.input(input_pin)
  
  is_sabotaged = True
  GPIO.output(relay_output, GPIO.LOW)
  GPIO.output(led_outputs, GPIO.LOW)
  
  sound_player.play_sound(SoundEffect.ALARM, True)
  
def finish_sabotage():
  global is_sabotaged
  
  is_sabotaged = False
  GPIO.output(relay_output, GPIO.HIGH)
  changed_switch_inputs.clear()
  
  sound_player.stop()
  sound_player.play_sound(SoundEffect.TASK_DONE)
  
  schedule_next_sabotage()
    
def halt_system():
  # Initiate system shutdown
  # You’re probably running this script as sudo, in which case this will work fine.
  # Otherwise, edit /etc/sudoers and add the line "<your_user_name> ALL=NOPASSWD: /sbin/shutdown"
  os.system("sudo shutdown -h now")
  
def process_sabotage():
  
  if is_sabotaged == False:
    return
  
  all_states_high = True
  
  # FIXME: When sabotage starts, the switches will be randomly on and off, not all off. You have to treat each switch’s "on" state as being opposite as its state when sabotage starts, not just GPIO.HIGH.  

  for (index, pin_number) in enumerate(switch_inputs):
    
    state = GPIO.input(pin_number)
    
    if state != output_states[index]:
      # Switch has changed state! Randomly decide whether to switch a *different* one back here.
      should_undo_other = random.getrandbits(1)
      if should_undo_other and changed_switch_inputs:
        print(f'Switch {index} was changed and randomly selected to be undone')
       
        index_to_undo = random.choice(changed_switch_inputs)
        
        current_state = GPIO.input(switch_inputs[index_to_undo])
        new_state = GPIO.LOW if current_state == GPIO.HIGH else GPIO.HIGH
        
        output_states[index] = new_state
        GPIO.output(led_outputs[index_to_undo], new_state)
        
      changed_switch_inputs.append(index)
      
    GPIO.output(led_outputs[index], state)
    output_states[index] = state
    
    if state != GPIO.HIGH:
      all_states_high = False
  
  if all_states_high:
    print("All switches on; finishing sabotage…")
    finish_sabotage()

while running:
  if GPIO.input(shutdown_input) == GPIO.LOW:
    print("Shutdown button pressed")
    halt_system()
  
  if GPIO.input(trigger_button_input) == GPIO.HIGH and is_trigger_button_latched == False:
    print("Trigger button pressed")
    is_trigger_button_latched = True
    if is_sabotaged:
      finish_sabotage()
    else:
      begin_sabotage()
      continue
  elif GPIO.input(trigger_button_input) == GPIO.LOW:
    is_trigger_button_latched = False
    
  display.update(is_sabotaged)
  
  if next_scheduled_sabotage_date.ctime() == datetime.now().ctime(): # Comparing the actual datetimes doesn't work for some reason.
    print("Sabotage is scheduled to begin now!")
    begin_sabotage()
    
  if is_sabotaged:
    process_sabotage()
    
  sleep(0.001) # 1ms should be sufficiently fast to loop