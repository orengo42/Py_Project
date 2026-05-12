import pygame

try:
    from .button import Button
except ImportError:
    from button import Button


TEXT_COLOR = (230, 235, 255)
MUTED_TEXT = (150, 158, 180)
CARD_COLOR = (32, 42, 67)
CARD_HOVER = (40, 52, 82)
BORDER_COLOR = (68, 80, 112)
CYAN = (88, 221, 255)


class Checkbox:
    def __init__(
        self,
        rect,
        text,
        font,
        checked=False,
        box_color=(255, 255, 255),
        border_color=(95, 110, 145),
        check_color=(70, 220, 255),
        text_color=TEXT_COLOR,
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
            full_rect = pygame.Rect(
                self.rect.left - 12,
                self.rect.top - 14,
                390,
                self.rect.height + 28,
            )

            if full_rect.collidepoint(event.pos):
                self.checked = not self.checked
                return True

        return False

    def draw(self, surface):
        card_rect = pygame.Rect(
            self.rect.left - 14,
            self.rect.top - 15,
            390,
            62,
        )

        mouse_pos = pygame.mouse.get_pos()
        card_color = CARD_HOVER if card_rect.collidepoint(mouse_pos) else CARD_COLOR

        pygame.draw.rect(surface, card_color, card_rect, border_radius=12)
        pygame.draw.rect(surface, BORDER_COLOR, card_rect, 1, border_radius=12)

        pygame.draw.rect(surface, self.box_color, self.rect, border_radius=3)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=3)

        if self.checked:
            start = (self.rect.left + 5, self.rect.centery)
            middle = (self.rect.left + 11, self.rect.bottom - 6)
            end = (self.rect.right - 5, self.rect.top + 6)

            pygame.draw.line(surface, self.check_color, start, middle, 3)
            pygame.draw.line(surface, self.check_color, middle, end, 3)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(midleft=(self.rect.right + 14, self.rect.centery))

        surface.blit(text_surface, text_rect)


class RadioButton:
    def __init__(
        self,
        rect,
        text,
        font,
        group,
        value,
        selected_value_getter,
        selected_value_setter,
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.group = group
        self.value = value
        self.get_selected_value = selected_value_getter
        self.set_selected_value = selected_value_setter

    def is_selected(self):
        return self.get_selected_value() == self.value

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            full_rect = pygame.Rect(
                self.rect.left - 14,
                self.rect.top - 15,
                250,
                58,
            )

            if full_rect.collidepoint(event.pos):
                self.set_selected_value(self.value)
                return True

        return False

    def draw(self, surface):
        card_rect = pygame.Rect(
            self.rect.left - 14,
            self.rect.top - 15,
            250,
            58,
        )

        mouse_pos = pygame.mouse.get_pos()
        card_color = CARD_HOVER if card_rect.collidepoint(mouse_pos) else CARD_COLOR

        pygame.draw.rect(surface, card_color, card_rect, border_radius=12)
        pygame.draw.rect(surface, BORDER_COLOR, card_rect, 1, border_radius=12)

        pygame.draw.circle(surface, (245, 245, 255), self.rect.center, self.rect.width // 2)
        pygame.draw.circle(surface, (110, 125, 160), self.rect.center, self.rect.width // 2, 2)

        if self.is_selected():
            pygame.draw.circle(surface, CYAN, self.rect.center, self.rect.width // 2 - 6)

        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(midleft=(self.rect.right + 14, self.rect.centery))
        surface.blit(text_surface, text_rect)


class OnScreenKeyboard:
    def __init__(self, font, target_textbox):
        self.font = font
        self.target_textbox = target_textbox

        self.key_width = 128
        self.key_height = 44
        self.gap = 10
        self.row_gap = 12

        self.buttons = []

        self.rows = [
            [
                ("(", "("),
                (")", ")"),
                ("==", "=="),
                ("≠", "!="),
                ("≤", "<="),
                ("≥", ">="),
            ],
            [
                ("+", "+"),
                ("-", "-"),
                ("*", "*"),
                ("/", "/"),
                ("//", "//"),
                ("**", "**"),
            ],
            [
                ("and", " and "),
                ("or", " or "),
                ("not", " not "),
                ("is_prime(", "is_prime("),
                ("is_even(", "is_even("),
                ("is_odd(", "is_odd("),
            ],
            [
                ("fact(", "fact("),
                ("gcd(", "gcd("),
                ("lcm(", "lcm("),
                ("divides(", "divides("),
                ("phi(", "phi("),
                ("tau(", "tau(")
            ],
        ]

    def get_height(self):
        return len(self.rows) * self.key_height + (len(self.rows) - 1) * self.row_gap

    def rebuild(self, center_x, top_y):
        self.buttons = []

        for row_index, row in enumerate(self.rows):
            row_width = (
                len(row) * self.key_width
                + (len(row) - 1) * self.gap
            )

            row_x = center_x - row_width // 2
            row_y = top_y + row_index * (self.key_height + self.row_gap)

            for col_index, key_data in enumerate(row):
                label, insert_value = key_data

                rect = pygame.Rect(
                    row_x + col_index * (self.key_width + self.gap),
                    row_y,
                    self.key_width,
                    self.key_height,
                )

                self.buttons.append(
                    {
                        "rect": rect,
                        "label": label,
                        "insert_value": insert_value,
                    }
                )

    def press_key(self, value):
        self.target_textbox.active = True

        if value == "BACKSPACE":
            if hasattr(self.target_textbox, "backspace"):
                self.target_textbox.backspace()
            elif self.target_textbox.text:
                self.target_textbox.text = self.target_textbox.text[:-1]
            return

        self.target_textbox.insert_text(value)

    def handle_event(self, event):
        if not self.target_textbox.active:
            return False

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False

        for button in self.buttons:
            if button["rect"].collidepoint(event.pos):
                self.press_key(button["insert_value"])
                return True

        return False

    def draw(self, surface):
        if not self.target_textbox.active:
            return

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            rect = button["rect"]
            label = button["label"]

            if rect.collidepoint(mouse_pos):
                bg_color = (50, 64, 100)
            else:
                bg_color = (38, 48, 76)

            pygame.draw.rect(surface, bg_color, rect, border_radius=10)
            pygame.draw.rect(surface, (80, 95, 130), rect, 1, border_radius=10)

            text_surface = self.font.render(label, True, (235, 238, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            surface.blit(text_surface, text_rect)