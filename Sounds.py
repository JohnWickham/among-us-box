from enum import Enum
from playsound import playsound

class SoundEffect(Enum):
  ALARM = "alarm.mp3"
  VICTORY = "victory.mp3"
  
class SoundPlayer:
  
  loop_sound_effect = False
  _thread = None

  def play_sound(self, sound):
    
    sound = sound.value
    playsound(sound)
    
    if self.loop_sound_effect:
      while self.loop_sound_effect:
        playsound(sound)