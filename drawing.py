import pygame
import os
from time import sleep
from random import randint

class DisplayDrawer():
  
  clock = None
  
  screen = None
  screen_width = 0
  screen_height = 0
  
  graph_green_color = (0, 255, 0)
  
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
      
    clock = pygame.time.Clock()
    
  top_graph_points = [(0, 0)]
      
  def draw_top_graph(self):
    # Add a new point to the top graph
    graph_width = self.screen_width
    graph_height = 100
    graph_x = 0
    graph_y = self.screen_height - graph_height
    random_point = randint(1, graph_height)
    self.top_graph_points.append((graph_width, random_point))
    pygame.draw.lines(self.screen, self.graph_green_color, True, self.top_graph_points, 1)

  def update(self):
    self.screen.fill((0, 0, 0))
    
    self.draw_top_graph()
    
    pygame.display.flip()
    pygame.display.update()
    
    self.clock.tick(30)
