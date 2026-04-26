import os
import sys
import pygame

try:
    from pygame._sdl2 import Window
except ImportError:
    Window = None

try:
    from .button import Button
    from .screens import MenuScreen, CheckHypothesisScreen
except ImportError:
    from button import Button
    from screens import MenuScreen, CheckHypothesisScreen


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720
TOP_BAR_HEIGHT = 46

APP_TITLE = "Проверка математических гипотез"


class TitleBar:
    def __init__(self, app):
        self.app = app

        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.button_font = pygame.font.SysFont("arial", 22, bold=True)

        self.close_button = Button(
            rect=(WINDOW_WIDTH - 44, 7, 32, 32),
            text="×",
            font=self.button_font,
            on_click=self.app.close,
            bg_color=(245, 220, 220),
            hover_color=(235, 120, 120),
            text_color=(80, 30, 30),
            border_color=(180, 120, 120),
            radius=8,
        )

        self.minimize_button = Button(
            rect=(WINDOW_WIDTH - 84, 7, 32, 32),
            text="−",
            font=self.button_font,
            on_click=self.app.minimize,
            bg_color=(230, 230, 240),
            hover_color=(210, 210, 230),
            text_color=(40, 40, 60),
            border_color=(160, 160, 180),
            radius=8,
        )

        self.dragging = False

    def handle_event(self, event):
      if self.close_button.handle_event(event):
          return True

      if self.minimize_button.handle_event(event):
          return True

      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          if event.pos[1] <= TOP_BAR_HEIGHT:
              self.dragging = True
              return True

      if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
          if self.dragging:
              self.dragging = False
              return True

          return False

      if event.type == pygame.MOUSEMOTION and self.dragging:
          self.move_window(event.rel)
          return True

      return False

    def move_window(self, rel):
        if self.app.window is None:
            return

        try:
            x, y = self.app.window.position
            self.app.window.position = (x + rel[0], y + rel[1])
        except Exception:
            pass

    def draw(self, surface):
        bar_rect = pygame.Rect(0, 0, WINDOW_WIDTH, TOP_BAR_HEIGHT)

        pygame.draw.rect(surface, (245, 245, 250), bar_rect)
        pygame.draw.line(
            surface,
            (200, 200, 215),
            (0, TOP_BAR_HEIGHT - 1),
            (WINDOW_WIDTH, TOP_BAR_HEIGHT - 1),
            1,
        )

        icon_rect = self.app.icon_surface.get_rect()
        icon_rect.center = (28, TOP_BAR_HEIGHT // 2)
        surface.blit(self.app.icon_surface, icon_rect)

        title_surface = self.font.render(APP_TITLE, True, (30, 30, 45))
        title_rect = title_surface.get_rect(midleft=(58, TOP_BAR_HEIGHT // 2))
        surface.blit(title_surface, title_rect)

        self.minimize_button.draw(surface)
        self.close_button.draw(surface)


class App:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            pygame.NOFRAME,
        )

        pygame.display.set_caption(APP_TITLE)

        self.assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        self.icon_path = os.path.join(self.assets_dir, "icon.png")

        self.create_icon_if_needed()
        self.icon_surface = pygame.image.load(self.icon_path).convert_alpha()
        pygame.display.set_icon(self.icon_surface)

        self.window = None

        if Window is not None:
            try:
                self.window = Window.from_display_module()
            except Exception:
                self.window = None

        self.clock = pygame.time.Clock()
        self.running = True

        self.title_bar = TitleBar(self)

        self.screens = {
            "menu": MenuScreen(self),
            "check": CheckHypothesisScreen(self),
        }

        self.current_screen_name = "menu"
        self.current_screen = self.screens[self.current_screen_name]

    def create_icon_if_needed(self):
        os.makedirs(self.assets_dir, exist_ok=True)

        if os.path.exists(self.icon_path):
            return

        surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(surface, (220, 40, 40), (16, 16), 13)
        pygame.image.save(surface, self.icon_path)

    def set_screen(self, name):
        if name not in self.screens:
            return

        self.current_screen_name = name
        self.current_screen = self.screens[name]

    def close(self):
        self.running = False

    def minimize(self):
        pygame.display.iconify()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.title_bar.handle_event(event):
                continue

            self.current_screen.handle_event(event)

    def update(self, dt):
        self.current_screen.update(dt)

    def draw(self):
        self.screen.fill((235, 238, 245))

        self.title_bar.draw(self.screen)

        content_rect = pygame.Rect(
            0,
            TOP_BAR_HEIGHT,
            WINDOW_WIDTH,
            WINDOW_HEIGHT - TOP_BAR_HEIGHT,
        )

        self.current_screen.draw(self.screen, content_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60)

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.run()