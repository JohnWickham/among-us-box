import pygame
import os

class DisplayDrawer():
  
  screen = None
  
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
      print("Failed to initialise display driver")
    else:
      width  = pygame.display.Info().current_w
      height = pygame.display.Info().current_h
      self.screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
      pygame.mouse.set_visible(False)
      pygame.display.update()
      time.sleep(10)
  
#   def __init__(self):
#     "Ininitializes a new pygame screen using the framebuffer"
#     # Based on "Python GUI in Linux frame buffer"
#     # http://www.karoltomala.com/blog/?p=679
#     disp_no = os.getenv("DISPLAY")
#     if disp_no:
#         print(f"I'm running under X display = {disp_no}")
#     
#     # Check which frame buffer drivers are available
#     # Start with fbcon since directfb hangs with composite output
#     drivers = ['fbcon', 'directfb', 'svgalib']
#     found = False
#     for driver in drivers:
#         # Make sure that SDL_VIDEODRIVER is set
#         if not os.getenv('SDL_VIDEODRIVER'):
#             os.putenv('SDL_VIDEODRIVER', driver)
#         try:
#             pygame.display.init()
#         except pygame.error:
#             print(f'Driver: {driver} failed.')
#             continue
#         found = True
#         break
# 
#     if not found:
#         raise Exception('No suitable video driver found!')
#     
#     size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
#     print(f'Framebuffer size: {size[0]} x {size[1]}')
#     self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
#     self.screen.fill((0, 0, 0))        
#     pygame.display.update()

  def __del__(self):
    "Destructor to make sure pygame shuts down, etc."

  def update(self):
    self.screen.fill((255, 0, 0))
    pygame.display.update()
    pygame.display.flip()