import os
import sys
import pygame

try:
    from .screens import (
        MenuScreen,
        CheckHypothesisScreen,
        CounterexamplesScreen,
        GraphScreen,
    )
except ImportError:
    from screens import (
        MenuScreen,
        CheckHypothesisScreen,
        CounterexamplesScreen,
        GraphScreen,
    )


INITIAL_WINDOW_WIDTH = 1100
INITIAL_WINDOW_HEIGHT = 720
MIN_WINDOW_WIDTH = 900
MIN_WINDOW_HEIGHT = 620

APP_TITLE = "Проверка математических гипотез"


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
        self.screen.fill((235, 238, 245))

        content_rect = pygame.Rect(
            0,
            0,
            self.width,
            self.height,
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