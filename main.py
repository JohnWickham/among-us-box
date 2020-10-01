import RPi.GPIO as GPIO
from datetime import datetime, timedelta
from random import randint
from time import sleep
from Sounds import SoundPlayer, SoundEffect
import os

GPIO.setmode(GPIO.BCM)

# Define input and output pins
trigger_button_input = 26
relay_output = 4
shutdown_input = 25
switch_inputs = [17, 27, 22, 23, 24]
led_outputs = [5, 6, 12, 13, 16]
led_states = [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW]

GPIO.setup(trigger_button_input, GPIO.IN)
GPIO.setup(relay_output, GPIO.OUT)
GPIO.setup(shutdown_input, GPIO.IN)
GPIO.setup(switch_inputs, GPIO.IN)
GPIO.setup(led_outputs, GPIO.OUT)

running = True

sound_player = SoundPlayer()
sound_player.play_sound(SoundEffect.GAME_START)

is_trigger_button_latched = False
is_shutdown_button_latched = False

is_sabotaged = False
next_scheduled_sabotage_date = None

def schedule_next_sabotage():
  global next_scheduled_sabotage_date
  
  min_offset = 60#5 * 60 # 5 minutes
  max_offset = 5 * 60#12 * 60 * 60 # 12 hours
  random_seconds = randint(min_offset, max_offset)
  now = datetime.now()
  next_scheduled_sabotage_date = now + timedelta(seconds=random_seconds)
  print("Next sabotage scheduled for: ", next_scheduled_sabotage_date.ctime())

schedule_next_sabotage()

step_count = 0
switch_step = -1

def begin_sabotage():
  global is_sabotaged
  
  if is_sabotaged:
    return
  
  is_sabotaged = True
  GPIO.output(relay_output, GPIO.LOW)
  
  sound_player.play_sound(SoundEffect.ALARM, True)
  
def finish_sabotage():
  global is_sabotaged
  
  is_sabotaged = False
  
  sound_player.stop()
  sound_player.play_sound(SoundEffect.TASK_DONE)
  
  schedule_next_sabotage()
    
def halt_system():
  # Initiate system shutdown
  # You’re probably running this script as sudo, in which case this will work fine.
  # Otherwise, edit /etc/sudoers and add the line "<your_user_name> ALL=NOPASSWD: /sbin/shutdown"
  os.system("sudo shutdown -h now")

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
    
  if next_scheduled_sabotage_date == datetime.now():
    print("Sabotage is scheduled to begin now!")
    begin_sabotage()
    
  #if is_sabotaged:
    # if switch_step == -1:
    #   step_count = randint(5, 10)
    #   switch_step = 0
    #   
    # GPIO.output(led_outputs, GPIO.LOW)
    # Process switch input sequence