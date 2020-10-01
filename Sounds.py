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
    
    count = -1 if self.loop_sound_effect else 0
    pygame.mixer.music.play(count)
    
    while pygame.mixer.music.get_busy(): 
      pygame.time.Clock().tick(10)