# -*- coding: UTF-8 -*-
from enum import Enum
from pygame import mixer

class SoundEffect(Enum):
  ALARM = "alarm.ogg"
  TASK_DONE = "task_done.ogg"
  GAME_START = "game_start.ogg"
  VICTORY = "victory.ogg"
  
class SoundPlayer:
  
  def __init__(self):
    mixer.init()
  
  _thread = None

  def play_sound(self, sound, loop=False):
    
    if type(sound) != str:
      sound = sound.value
    mixer_sound = mixer.Sound(sound)
    mixer_sound.set_volume(1)
    
    count = -1 if loop else 0
    mixer_sound.play(count)
  
  def stop(self):
    mixer.stop()