import math
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
        icon_name=None,
        icon_color=None,
        icon_size=22,
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

        self.icon_name = icon_name
        self.icon_color = icon_color if icon_color is not None else text_color
        self.icon_size = icon_size

        self.is_pressed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed:
                self.is_pressed = False

                if self.rect.collidepoint(event.pos):
                    if self.on_click is not None:
                        self.on_click()

                    return True

        return False

    def draw_icon(self, surface, center):
        if self.icon_name is None:
            return

        x, y = center
        size = self.icon_size
        color = self.icon_color
        half = size // 2

        if self.icon_name == "menu":
            for offset in [-6, 0, 6]:
                pygame.draw.line(
                    surface,
                    color,
                    (x - half + 3, y + offset),
                    (x + half - 3, y + offset),
                    3,
                )

        elif self.icon_name == "check":
            pygame.draw.circle(surface, color, (x, y), half, 2)
            pygame.draw.line(surface, color, (x - 6, y), (x - 1, y + 5), 3)
            pygame.draw.line(surface, color, (x - 1, y + 5), (x + 7, y - 6), 3)

        elif self.icon_name == "calculator":
          body = pygame.Rect(x - 10, y - 10, 20, 20)
          pygame.draw.rect(surface, color, body, 2, border_radius=4)

          screen_rect = pygame.Rect(x - 6, y - 7, 12, 4)
          pygame.draw.rect(surface, color, screen_rect, 1, border_radius=2)

          dot_size = 3
          start_x = x - 6
          start_y = y + 1
          gap = 5

          for row in range(2):
              for col in range(3):
                  dot = pygame.Rect(
                      start_x + col * gap,
                      start_y + row * gap,
                      dot_size,
                      dot_size,
                  )
                  pygame.draw.rect(surface, color, dot, border_radius=1)

        elif self.icon_name == "function":
            points = [
                (x - half + 2, y + 6),
                (x - 5, y + 2),
                (x, y + 5),
                (x + 5, y - 4),
                (x + half - 2, y - 7),
            ]
            pygame.draw.lines(surface, color, False, points, 3)
            pygame.draw.line(surface, color, (x + half - 7, y - 7), (x + half - 2, y - 7), 3)
            pygame.draw.line(surface, color, (x + half - 2, y - 7), (x + half - 2, y - 2), 3)

        elif self.icon_name == "library":
            for i in range(3):
                book = pygame.Rect(x - half + i * 7, y - half + 4, 4, size - 8)
                pygame.draw.rect(surface, color, book, border_radius=2)

        elif self.icon_name == "save":
            body = pygame.Rect(x - half + 2, y - half + 2, size - 4, size - 4)
            pygame.draw.rect(surface, color, body, 2, border_radius=3)
            pygame.draw.rect(surface, color, (body.left + 4, body.top + 3, body.width - 8, 6), 1)
            pygame.draw.rect(surface, color, (body.left + 5, body.bottom - 9, body.width - 10, 6), 1)

        elif self.icon_name == "reset":
            arc_rect = pygame.Rect(x - half + 3, y - half + 3, size - 6, size - 6)
            pygame.draw.arc(surface, color, arc_rect, math.radians(40), math.radians(315), 3)
            pygame.draw.line(surface, color, (x - 7, y - 8), (x - 1, y - 9), 3)
            pygame.draw.line(surface, color, (x - 7, y - 8), (x - 5, y - 2), 3)

        elif self.icon_name == "eye":
            pygame.draw.ellipse(surface, color, (x - half + 2, y - 8, size - 4, 16), 2)
            pygame.draw.circle(surface, color, (x, y), 4)

        elif self.icon_name == "graph":
            base_y = y + half - 3
            for i, height in enumerate([8, 14, 20]):
                bar = pygame.Rect(x - half + 5 + i * 7, base_y - height, 4, height)
                pygame.draw.rect(surface, color, bar, border_radius=2)

        elif self.icon_name == "close":
            pygame.draw.circle(surface, color, (x, y), half, 2)
            pygame.draw.line(surface, color, (x - 6, y - 6), (x + 6, y + 6), 3)
            pygame.draw.line(surface, color, (x + 6, y - 6), (x - 6, y + 6), 3)

        elif self.icon_name == "sigma":
            points = [
                (x + 8, y - 10),
                (x - 7, y - 10),
                (x + 1, y),
                (x - 7, y + 10),
                (x + 8, y + 10),
            ]
            pygame.draw.lines(surface, color, False, points, 3)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color

        if self.is_pressed:
            color = (
                max(0, color[0] - 15),
                max(0, color[1] - 15),
                max(0, color[2] - 15),
            )

        pygame.draw.rect(surface, color, self.rect, border_radius=self.radius)
        pygame.draw.rect(surface, self.border_color, self.rect, 1, border_radius=self.radius)

        text_surface = self.font.render(self.text, True, self.text_color)

        if self.icon_name is None:
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
            return

        gap = 12 if self.text else 0
        total_width = self.icon_size + gap + text_surface.get_width()

        start_x = self.rect.centerx - total_width // 2
        icon_center = (
            start_x + self.icon_size // 2,
            self.rect.centery,
        )

        self.draw_icon(surface, icon_center)

        if self.text:
            text_rect = text_surface.get_rect(
                midleft=(start_x + self.icon_size + gap, self.rect.centery)
            )
            surface.blit(text_surface, text_rect)