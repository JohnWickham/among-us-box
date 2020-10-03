import pygame
import os
from time import sleep

class DisplayDrawer():
  
  screen = None
  screen_width = 0
  screen_height = 0
  
  def FindDisplayDriver(self):
    for driver in ["fbcon", "directfb", "svgalib"]:
      if not os.getenv("SDL_VIDEODRIVER"):
        os.putenv("SDL_VIDEODRIVER", driver)
      try:
        pygame.display.init()
        return True
      except pygame.error:
        pass
    return False
  
  def __init__(self):
    pygame.init()
    if not self.FindDisplayDriver():
      print("Failed to initialise display driver; continuing anyway.")
    else:
      self.screen_width  = pygame.display.Info().current_w
      self.screen_height = pygame.display.Info().current_h
      self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
      pygame.mouse.set_visible(False)
      pygame.display.update()
      sleep(1)
      
  def __del__(self):
    "Destructor to make sure pygame shuts down, etc."

  def update(self):
    self.screen.fill((0, 0, 0))
    
    # Top screen
    pygame.draw.rect(self.screen, (255, 255, 255), (25, self.screen_height - 25, self.screen_width - 25, 50), 1)
    
    pygame.display.flip()
    pygame.display.update()
