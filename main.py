import RPi.GPIO as GPIO
from time import sleep
from Sounds import SoundPlayer, SoundEffect
import threading
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
sound_effect_thread = None

is_trigger_button_latched = False
is_shutdown_button_latched = False

is_sabotaged = False

step_count = 0
switch_step = -1

def begin_sabotage():
  global is_sabotaged
  
  if is_sabotaged:
    return
  
  is_sabotaged = True
  GPIO.output(relay_output, GPIO.LOW)
  
  sound_player.loop_sound_effect = True
  sound_effect_thread = threading.Thread(target=sound_player.play_sound, args=(SoundEffect.ALARM,))
  sound_effect_thread.start()
    
def halt_system():
  # Initiate system shutdown
  # Edit /etc/sudoers and add the line "<your_user_name> ALL=NOPASSWD: /sbin/shutdown"
  os.system("sudo shutdown -h now")

while running:
  if GPIO.input(shutdown_input) == GPIO.LOW:
    print("Shutdown button pressed")
    halt_system()
  
  if GPIO.input(trigger_button_input) == GPIO.HIGH and is_trigger_button_latched == False:
    print("Trigger button pressed")
    is_trigger_button_latched = True
    begin_sabotage()
    continue
  elif GPIO.input(trigger_button_input) == GPIO.LOW:
    is_trigger_button_latched = False
    
  if is_sabotaged:
    # if switch_step == -1:
    #   step_count = random(5, 10)
    #   switch_step = 0
    #   
    # GPIO.output(led_outputs, GPIO.LOW)
    # Process switch input sequence