import pygame
import os
from time import sleep
from random import randint

class DisplayDrawer():
  
  clock = None
  font = None

  screen = None
  screen_width = 0
  screen_height = 0
  
  graph_green_color = (161, 233, 73)
  
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
      
    self.clock = pygame.time.Clock()
    font = pygame.font.SysFont('Courier New', 30)
    
  top_graph_y_points = []
      
  def draw_top_graph(self):
    # Add a new point to the top graph
    graph_width = self.screen_width
    graph_height = 60
    graph_x = 0
    graph_y = self.screen_height - graph_height
    graph_point_count = 130
    
    if len(self.top_graph_y_points) == 0:
      self.top_graph_y_points.append(graph_y)
    
    new_y_point = graph_y + randint(1, graph_height)
    self.top_graph_y_points.append(new_y_point)
    
    point_count = len(self.top_graph_y_points)
    if point_count > graph_point_count:
      self.top_graph_y_points.pop(0)
      
    points = []
    for (index, y) in enumerate(self.top_graph_y_points):
      x = graph_width - (index * round(graph_width / graph_point_count))
      points.append((x, y))
    
    pygame.draw.lines(self.screen, self.graph_green_color, False, points, 1)
    
  bottom_graph_y_points = []
    
  def draw_bottom_graph(self):
    
    graph_width = self.screen_width
    graph_height = 60
    graph_x = 0
    graph_y = graph_height
    graph_point_count = 110
    
    if len(self.bottom_graph_y_points) == 0:
      self.bottom_graph_y_points.append(graph_y)
    
    new_y_point = graph_y + randint(1, graph_height / 4)
    self.bottom_graph_y_points.append(new_y_point)
    
    point_count = len(self.bottom_graph_y_points)
    if point_count > graph_point_count:
      self.bottom_graph_y_points.pop(0)
      
    points = []
    for (index, y) in enumerate(self.bottom_graph_y_points):
      x = graph_width - (index * round(graph_width / graph_point_count))
      points.append((x, y))
    
    pygame.draw.lines(self.screen, self.graph_green_color, False, points, 1)
    
  def draw_center_text(self):
    textsurface = self.font.render('Fix Lights (%0)', False, (255, 0, 0))# TODO: Alternate red and yellow
    self.screen.blit(textsurface, (0, 0))

  def update(self):
    self.screen.fill((0, 0, 0))
    
    self.draw_top_graph()
    self.draw_bottom_graph()
    
    pygame.display.flip()
    pygame.display.update()
    
    self.clock.tick(30)
