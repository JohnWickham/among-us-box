from enum import Enum
import pygame

class SoundEffect(Enum):
  ALARM = "alarm.mp3"
  VICTORY = "victory.mp3"
  
class SoundPlayer:
  
  pygame.mixer.init()
  
  loop_sound_effect = False
  _thread = None

  def play_sound(self, sound):
    
    sound = sound.value
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy() == True:
      continue
    
    if self.loop_sound_effect:
      self.play_sound(sound)