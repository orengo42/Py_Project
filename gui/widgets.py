import pygame

try:
    from .button import Button
except ImportError:
    from button import Button


class Checkbox:
    def __init__(
        self,
        rect,
        text,
        font,
        checked=False,
        box_color=(255, 255, 255),
        border_color=(80, 80, 100),
        check_color=(40, 120, 70),
        text_color=(30, 30, 40),
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.checked = checked

        self.box_color = box_color
        self.border_color = border_color
        self.check_color = check_color
        self.text_color = text_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            text_surface = self.font.render(self.text, True, self.text_color)
            full_rect = pygame.Rect(
                self.rect.left,
                self.rect.top,
                self.rect.width + 12 + text_surface.get_width(),
                self.rect.height,
            )

            if full_rect.collidepoint(event.pos):
                self.checked = not self.checked
                return True

        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.box_color, self.rect, border_radius=4)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=4)

        if self.checked:
            start = (self.rect.left + 5, self.rect.centery)
            middle = (self.rect.left + 11, self.rect.bottom - 6)
            end = (self.rect.right - 5, self.rect.top + 6)

            pygame.draw.line(surface, self.check_color, start, middle, 3)
            pygame.draw.line(surface, self.check_color, middle, end, 3)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(midleft=(self.rect.right + 12, self.rect.centery))

        surface.blit(text_surface, text_rect)


class OnScreenKeyboard:
    def __init__(self, font, target_textbox):
        self.font = font
        self.target_textbox = target_textbox
        self.buttons = []

        self.rows = [
            ["(", ")", "==", "!=", "<=", ">="],
            ["+", "-", "*", "/", "//", "%", "**"],
            ["and", "or", "not", "True", "False"],
            ["n", "is_prime(", "is_even(", "is_odd(", "gcd(", "lcm(", "⌫"],
        ]

    def rebuild(self, x, y):
        self.buttons = []

        key_width = 92
        key_height = 40
        gap = 8

        for row_index, row in enumerate(self.rows):
            row_width = len(row) * key_width + (len(row) - 1) * gap
            row_x = x - row_width // 2
            row_y = y + row_index * (key_height + gap)

            for col_index, key in enumerate(row):
                rect = (
                    row_x + col_index * (key_width + gap),
                    row_y,
                    key_width,
                    key_height,
                )

                button = Button(
                    rect=rect,
                    text=key,
                    font=self.font,
                    on_click=lambda value=key: self.press_key(value),
                    bg_color=(245, 245, 250),
                    hover_color=(230, 230, 245),
                    text_color=(30, 30, 40),
                    border_color=(170, 170, 190),
                    radius=8,
                )

                self.buttons.append(button)

    def press_key(self, key):
        if key == "⌫":
            self.target_textbox.backspace()
            return

        if key == "and":
            self.target_textbox.insert_text(" and ")
            return

        if key == "or":
            self.target_textbox.insert_text(" or ")
            return

        if key == "not":
            self.target_textbox.insert_text(" not ")
            return

        self.target_textbox.insert_text(key)

    def handle_event(self, event):
        if not self.target_textbox.active:
            return False

        for button in self.buttons:
            if button.handle_event(event):
                return True

        return False

    def draw(self, surface):
        if not self.target_textbox.active:
            return

        for button in self.buttons:
            button.draw(surface)