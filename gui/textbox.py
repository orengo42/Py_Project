import pygame


class TextBox:
    def __init__(
        self,
        rect,
        font,
        placeholder="",
        text="",
        numbers_only=False,
        max_length=None,
        text_color=(30, 30, 40),
        placeholder_color=(150, 150, 160),
        bg_color=(255, 255, 255),
        border_color=(150, 150, 170),
        active_border_color=(80, 120, 220),
    ):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.placeholder = placeholder

        self.text = text
        self.cursor_index = len(text)
        self.active = False

        self.numbers_only = numbers_only
        self.max_length = max_length

        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.active_border_color = active_border_color

        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_delay = 500

        self.padding_x = 14
        self.scroll_offset = 0

    def set_text(self, text):
        self.text = str(text)
        self.cursor_index = len(self.text)
        self.ensure_cursor_visible()

    def clear(self):
        self.set_text("")

    def get_cursor_index_by_mouse(self, mouse_x):
        local_x = mouse_x - self.rect.left - self.padding_x + self.scroll_offset

        if local_x <= 0:
            return 0

        for index in range(len(self.text) + 1):
            current_width = self.font.size(self.text[:index])[0]

            if current_width >= local_x:
                return index

        return len(self.text)

    def can_insert(self, value):
        if self.max_length is not None:
            if len(self.text) + len(value) > self.max_length:
                return False

        if self.numbers_only:
            return value.isdigit()

        return True

    def insert_text(self, value):
        if not self.can_insert(value):
            return

        before = self.text[:self.cursor_index]
        after = self.text[self.cursor_index:]

        self.text = before + value + after
        self.cursor_index += len(value)

        self.ensure_cursor_visible()

    def backspace(self):
        if self.cursor_index == 0:
            return

        before = self.text[:self.cursor_index - 1]
        after = self.text[self.cursor_index:]

        self.text = before + after
        self.cursor_index -= 1

        self.ensure_cursor_visible()

    def delete(self):
        if self.cursor_index >= len(self.text):
            return

        before = self.text[:self.cursor_index]
        after = self.text[self.cursor_index + 1:]

        self.text = before + after

        self.ensure_cursor_visible()

    def move_cursor_left(self):
        if self.cursor_index > 0:
            self.cursor_index -= 1

        self.ensure_cursor_visible()

    def move_cursor_right(self):
        if self.cursor_index < len(self.text):
            self.cursor_index += 1

        self.ensure_cursor_visible()

    def move_cursor_home(self):
        self.cursor_index = 0
        self.ensure_cursor_visible()

    def move_cursor_end(self):
        self.cursor_index = len(self.text)
        self.ensure_cursor_visible()

    def ensure_cursor_visible(self):
        inner_width = self.rect.width - 2 * self.padding_x
        cursor_width = self.font.size(self.text[:self.cursor_index])[0]

        if cursor_width - self.scroll_offset > inner_width:
            self.scroll_offset = cursor_width - inner_width

        if cursor_width - self.scroll_offset < 0:
            self.scroll_offset = cursor_width

        if self.scroll_offset < 0:
            self.scroll_offset = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.cursor_index = self.get_cursor_index_by_mouse(event.pos[0])
                self.ensure_cursor_visible()
                self.cursor_visible = True
                self.cursor_timer = 0
                return True

            self.active = False
            return False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.backspace()
                return True

            if event.key == pygame.K_DELETE:
                self.delete()
                return True

            if event.key == pygame.K_LEFT:
                self.move_cursor_left()
                return True

            if event.key == pygame.K_RIGHT:
                self.move_cursor_right()
                return True

            if event.key == pygame.K_HOME:
                self.move_cursor_home()
                return True

            if event.key == pygame.K_END:
                self.move_cursor_end()
                return True

            if event.key == pygame.K_RETURN:
                self.active = False
                return True

            if event.unicode:
                self.insert_text(event.unicode)
                return True

        return False

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

        old_clip = surface.get_clip()
        inner_rect = pygame.Rect(
            self.rect.left + self.padding_x,
            self.rect.top + 2,
            self.rect.width - 2 * self.padding_x,
            self.rect.height - 4,
        )
        surface.set_clip(inner_rect)

        text_y = self.rect.centery

        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.midleft = (
                self.rect.left + self.padding_x - self.scroll_offset,
                text_y,
            )
            surface.blit(text_surface, text_rect)
        else:
            placeholder_surface = self.font.render(
                self.placeholder,
                True,
                self.placeholder_color,
            )
            placeholder_rect = placeholder_surface.get_rect()
            placeholder_rect.midleft = (
                self.rect.left + self.padding_x,
                text_y,
            )
            surface.blit(placeholder_surface, placeholder_rect)

        if self.active and self.cursor_visible:
            cursor_width = self.font.size(self.text[:self.cursor_index])[0]
            cursor_x = self.rect.left + self.padding_x + cursor_width - self.scroll_offset

            cursor_top = self.rect.top + 12
            cursor_bottom = self.rect.bottom - 12

            pygame.draw.line(
                surface,
                self.text_color,
                (cursor_x, cursor_top),
                (cursor_x, cursor_bottom),
                2,
            )

        surface.set_clip(old_clip)