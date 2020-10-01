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
    
    if type(sound) != str:
      sound = sound.value
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()
    
    if self.loop_sound_effect:
      while self.loop_sound_effect:
        pygame.mixer.music.play()
    else:
      pygame.mixer.music.stop()