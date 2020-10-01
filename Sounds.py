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
    mixer.music.load(sound)
    
    count = -1 if self.loop_sound_effect else 0
    channel = mixer.music.play(count)
    
    while channel.get_busy():
      sleep(100)