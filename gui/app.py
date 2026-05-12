import os
import sys
import pygame

try:
    from .screens import (
        MenuScreen,
        CheckHypothesisScreen,
        CounterexamplesScreen,
        GraphScreen,
        FunctionScreen,
    )
except ImportError:
    from screens import (
        MenuScreen,
        CheckHypothesisScreen,
        CounterexamplesScreen,
        GraphScreen,
        FunctionScreen,
    )


INITIAL_WINDOW_WIDTH = 1100
INITIAL_WINDOW_HEIGHT = 760
MIN_WINDOW_WIDTH = 980
MIN_WINDOW_HEIGHT = 680

APP_TITLE = "Проверка математических гипотез"
HEADER_HEIGHT = 0


class App:
    def __init__(self):
        pygame.init()

        self.width = INITIAL_WINDOW_WIDTH
        self.height = INITIAL_WINDOW_HEIGHT

        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.RESIZABLE,
        )

        pygame.display.set_caption(APP_TITLE)

        self.assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        self.icon_path = os.path.join(self.assets_dir, "icon.png")

        self.create_icon_if_needed()
        self.icon_surface = pygame.image.load(self.icon_path).convert_alpha()
        pygame.display.set_icon(self.icon_surface)

        self.clock = pygame.time.Clock()
        self.running = True

        self.screens = {
            "menu": MenuScreen(self),
            "check": CheckHypothesisScreen(self),
            "counterexamples": CounterexamplesScreen(self),
            "graph": GraphScreen(self),
            "function": FunctionScreen(self),
        }

        self.current_screen_name = "menu"
        self.current_screen = self.screens[self.current_screen_name]

    def create_icon_if_needed(self):
        os.makedirs(self.assets_dir, exist_ok=True)

        surface = pygame.Surface((64, 64), pygame.SRCALPHA)

        for y in range(64):
            t = y / 63
            r = int(70 + (165 - 70) * t)
            g = int(90 + (40 - 90) * t)
            b = int(230 + (255 - 230) * t)
            pygame.draw.line(surface, (r, g, b), (0, y), (64, y))

        pygame.draw.rect(
            surface,
            (255, 255, 255, 35),
            (2, 2, 60, 60),
            border_radius=14,
        )

        sigma_points = [
            (43, 15),
            (23, 15),
            (33, 31),
            (23, 48),
            (43, 48),
        ]

        pygame.draw.lines(surface, (255, 255, 255), False, sigma_points, 6)
        pygame.image.save(surface, self.icon_path)

    def set_screen(self, name):
        if name not in self.screens:
            return

        self.current_screen_name = name
        self.current_screen = self.screens[name]

    def open_counterexamples(self, expression, counterexamples):
        screen = self.screens["counterexamples"]
        screen.set_data(expression, counterexamples)
        self.set_screen("counterexamples")

    def open_graph(self, graph_number, expression, points):
        screen = self.screens["graph"]
        screen.set_data(graph_number, expression, points)
        self.set_screen("graph")

    def close(self):
        self.running = False

    def draw_header(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.VIDEORESIZE:
                self.width = max(MIN_WINDOW_WIDTH, event.w)
                self.height = max(MIN_WINDOW_HEIGHT, event.h)

                self.screen = pygame.display.set_mode(
                    (self.width, self.height),
                    pygame.RESIZABLE,
                )
                continue

            self.current_screen.handle_event(event)

    def update(self, dt):
        self.current_screen.update(dt)

    def draw(self):
        self.screen.fill((10, 14, 30))
        self.draw_header()

        content_rect = pygame.Rect(
            0,
            HEADER_HEIGHT,
            self.width,
            self.height - HEADER_HEIGHT,
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