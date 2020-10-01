from enum import Enum
from pygame import mixer
from time import sleep

class SoundEffect(Enum):
  ALARM = "alarm.mp3"
  VICTORY = "victory.mp3"
  
class SoundPlayer:
  
  def __init__(self):
    mixer.init()
  
  loop_sound_effect = False
  _thread = None

  def play_sound(self, sound):
    
    if type(sound) != str:
      sound = sound.value
    mixer_sound = mixer.Sound(sound)
    
    mixer_sound.play()
    
    time.sleep(5)