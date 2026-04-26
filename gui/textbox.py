import pygame

class TextBox:
  def __init__(
    self,
    rect,
    font,
    placeholder="Введите гипотезу",
    text_color=(30, 30, 40),
    placeholder_color=(150, 150, 160),
    bg_color=(255, 255, 255),
    border_color=(150, 150, 170),
    active_border_color=(80, 120, 220),
  ):
    self.rect = pygame.Rect(rect)
    self.font = font
    self.placeholder = placeholder

    self.text = ""
    self.active = False

    self.text_color = text_color
    self.placeholder_color = placeholder_color
    self.bg_color = bg_color
    self.border_color = border_color
    self.active_border_color = active_border_color

    self.cursor_visible = True
    self.cursor_timer = 0
    self.cursor_delay = 500

  def handle_event(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          self.active = self.rect.collidepoint(event.pos)
          return self.active

      if event.type == pygame.KEYDOWN and self.active:
          if event.key == pygame.K_BACKSPACE:
              self.backspace()
              return True

          if event.key == pygame.K_RETURN:
              self.active = False
              return True

          if event.unicode:
              self.insert_text(event.unicode)
              return True

      return False

  def insert_text(self, value):
      self.text += value

  def backspace(self):
      self.text = self.text[:-1]

  def update(self, dt):
      if not self.active:
          self.cursor_visible = False
          return

      self.cursor_timer += dt

      if self.cursor_timer >= self.cursor_delay:
          self.cursor_visible = not self.cursor_visible
          self.cursor_timer = 0

  def draw(self, surface):
      border_color = self.active_border_color if self.active else self.border_color

      pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=10)
      pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=10)

      padding_x = 14
      text_y = self.rect.centery

      if self.text:
          text_surface = self.font.render(self.text, True, self.text_color)
      else:
          text_surface = self.font.render(self.placeholder, True, self.placeholder_color)

      text_rect = text_surface.get_rect()
      text_rect.midleft = (self.rect.left + padding_x, text_y)

      surface.blit(text_surface, text_rect)

      if self.active and self.cursor_visible:
          cursor_x = text_rect.right + 2 if self.text else self.rect.left + padding_x
          cursor_top = self.rect.top + 12
          cursor_bottom = self.rect.bottom - 12

          pygame.draw.line(
              surface,
              self.text_color,
              (cursor_x, cursor_top),
              (cursor_x, cursor_bottom),
              2,
          )