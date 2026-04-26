import pygame

class Button:
  def __init__(
    self,
    rect,
    text,
    font,
    on_click=None,
    bg_color=(235, 235, 245),
    hover_color=(220, 220, 235),
    text_color=(30, 30, 40),
    border_color=(150, 150, 170),
    radius=12,
  ):
    self.rect = pygame.Rect(rect)
    self.text = text
    self.font = font
    self.on_click = on_click
    self.bg_color = bg_color
    self.hover_color = hover_color
    self.text_color = text_color
    self.border_color = border_color
    self.radius = radius
    self.is_pressed = False

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if self.rect.collidepoint(event.pos):
            self.is_pressed = True
            return True

    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        was_pressed = self.is_pressed
        self.is_pressed = False

        if was_pressed and self.rect.collidepoint(event.pos):
            if self.on_click is not None:
                self.on_click()
            return True

    return False

  def draw(self, surface):
    mouse_pos = pygame.mouse.get_pos()
    color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color

    pygame.draw.rect(surface, color, self.rect, border_radius=self.radius)
    pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=self.radius)

    text_surface = self.font.render(self.text, True, self.text_color)
    text_rect = text_surface.get_rect(center=self.rect.center)

    surface.blit(text_surface, text_rect)