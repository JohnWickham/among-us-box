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
  
  red_color = (234, 50, 35)
  green_color = (161, 233, 73)
  yellow_color = (238, 221, 74)
  
  current_text_color = red_color
  last_text_color_alternate_time = 0
  
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
    self.font = pygame.font.SysFont('Arial', 30)
    
  top_graph_y_points = []
      
  def draw_top_graph(self):
    # Add a new point to the top graph
    graph_width = self.screen_width
    graph_height = 70
    graph_x = 0
    graph_y = (self.screen_height - 50) - graph_height
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
    
    pygame.draw.lines(self.screen, self.green_color, False, points, 1)
    
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
    
    pygame.draw.lines(self.screen, self.green_color, False, points, 1)
    
  def draw_center_text(self, is_sabotaged):
    if is_sabotaged:
      
      current_clock_time = pygame.time.get_ticks()
      if current_clock_time - self.last_text_color_alternate_time >= 250:
        self.last_text_color_alternate_time = current_clock_time
        self.current_text_color = self.red_color if self.current_text_color == self.yellow_color else self.yellow_color
      
      text_surface = self.font.render('Fix Lights (%0)', False, self.current_text_color)# TODO: Alternate red and yellow every 250ms
    else:
      text_surface = self.font.render('Tasks Completed', False, self.green_color)
    text_frame = text_surface.get_rect()
    y = (self.screen_height / 2) - (text_frame.height / 2)
    self.screen.blit(text_surface, (0, y))

  def update(self, is_sabotaged=False):
    self.screen.fill((0, 0, 0))
    
    self.draw_top_graph()
    self.draw_bottom_graph()
    self.draw_center_text(is_sabotaged)
    
    pygame.display.update()
    
    self.clock.tick(30)
