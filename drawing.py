import pygame
import os
from time import sleep

class DisplayDrawer():
  
  screen = None
  background = None
  
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
      width  = pygame.display.Info().current_w
      height = pygame.display.Info().current_h
      self.screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
      self.background = pygame.Surface((width, height))
      pygame.mouse.set_visible(False)
      pygame.display.update()
      sleep(1)
      
  def __del__(self):
    "Destructor to make sure pygame shuts down, etc."

  def update(self):
    self.background.fill((255, 0, 0))
    self.screen.blit(self.background, (0,0))
    pygame.display.update()
    pygame.display.flip()
    pygame.time.clock.tick(30)